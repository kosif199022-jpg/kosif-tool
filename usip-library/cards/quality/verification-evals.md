# `verification-evals` — الاختبارات والجودة والأمان (35 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/verification-evals.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/quality.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`CHECK-01` حلقة التحقق الثمانية](#check-01--حلقة-التحقق-الثمانية--verification-loop-8-steps-until-done-criteria-pass)
- [`CHECK-02` بوابة ما بعد الرندر](#check-02--بوابة-ما-بعد-الرندر--postcondition-gate-on-the-delivered-file-ffprobe--verify_videopy--measured-sync)
- [`CHECK-03` انظر إلى المخرَج بعينك](#check-03--انظر-إلى-المخرَج-بعينك--look-at-the-output-contact-sheets-frames-screenshots)
- [`CHECK-04` التقييم الذاتي بخمسة محاور](#check-04--التقييم-الذاتي-بخمسة-محاور--five-axis-self-evaluation-accuracy-completeness-clarity-actionability-concision)
- [`CHECK-05` هاجم مخرَجك بنفسك](#check-05--هاجم-مخرَجك-بنفسك--red-team-your-own-output-edge-inputs--sceptical-expert)
- [`CHECK-06` حلقة تحقق الكود](#check-06--حلقة-تحقق-الكود--code-verification-loop-build--types--lint--tests--secrets--diff)
- [`CHECK-07` قاعدة التوقف](#check-07--قاعدة-التوقف--stop-rule-done-means-checks-pass-or-the-budget-ends-with-risks-stated)
- [`CHECK-08` سُلَّم الأدلة للادعاءات](#check-08--سُلَّم-الأدلة-للادعاءات--evidence-ladder-for-claims-badges-are-earned-leased-and-downgraded)
- [`CHECK-09` الإيصال المنمَّط](#check-09--الإيصال-المنمَّط--typed-receipt-after-consequential-actions)
- [`CHECK-10` كلمات الحالة الصادقة](#check-10--كلمات-الحالة-الصادقة--honest-status-words-stage-by-stage)
- [`CHECK-11` التقييم أولًا](#check-11--التقييم-أولًا--eval-first-capability-evals--regression-evals)
- [`CHECK-12` pass@k مقابل pass^k](#check-12--passk-مقابل-passk--passk-vs-passk-any-success-vs-always-success)
- [`CHECK-13` بوابة الفشل القاطع](#check-13--بوابة-الفشل-القاطع--hard-fail-gate-one-must-never-happen-failure-blocks-release)
- [`CHECK-14` انضباط المحكِّم](#check-14--انضباط-المحكِّم--judge-discipline-assertions-first-one-criterion-per-judgement-cited-evidence)
- [`CHECK-15` طريقة سانتا: مراجعان معزولان](#check-15--طريقة-سانتا-مراجعان-معزولان--santa-method-two-isolated-reviewers-both-must-pass)
- [`CHECK-16` حلقة المولِّد والمقيِّم](#check-16--حلقة-المولِّد-والمقيِّم--generatorevaluator-loop-weighted-rubric-threshold-iteration-cap)
- [`CHECK-17` المتحقق العدائي](#check-17--المتحقق-العدائي--adversarial-verifier-that-defaults-to-refuted)
- [`CHECK-18` حلقة تحسين الأداء بالقياس](#check-18--حلقة-تحسين-الأداء-بالقياس--benchmark-optimisation-loop-one-hypothesis-per-variant)
- [`CHECK-19` فحص تصميم الحلقة](#check-19--فحص-تصميم-الحلقة--loop-design-check-before-automating-anything)
- [`CHECK-20` اختبار الطفرات للمدقِّق](#check-20--اختبار-الطفرات-للمدقِّق--mutation-test-your-validator-seed-defects-count-catches)
- [`CHECK-21` مصفوفة اختبار التفعيل](#check-21--مصفوفة-اختبار-التفعيل--trigger-eval-matrix-for-a-skill--withwithout-ab)
- [`CHECK-22` لقطة الفهرس والمدقِّق](#check-22--لقطة-الفهرس-والمدقِّق--catalog-snapshot-powerspy-stats--repo-validator)
- [`CHECK-23` بوابة السجلات الحتمية](#check-23--بوابة-السجلات-الحتمية--deterministic-record-gate-for-the-power-catalog-mutation-tested)
- [`CHECK-24` حلقة التطوير الذاتي للمهارة](#check-24--حلقة-التطوير-الذاتي-للمهارة--self-evolution-loop-for-this-skill-evolve-with-evidence)
- [`CHECK-25` دروس بموافقة ونطاق مشروع](#check-25--دروس-بموافقة-ونطاق-مشروع--consent-scoped-lessons-growth-log)
- [`CHECK-26` سجل القرارات المتكرر](#check-26--سجل-القرارات-المتكرر--decision-ledger-for-repeated-rollouts)
- [`CHECK-27` تصنيف الأعطال وأصغر إصلاح](#check-27--تصنيف-الأعطال-وأصغر-إصلاح--failure-taxonomy--smallest-repair)
- [`CHECK-28` سجل الحادثة](#check-28--سجل-الحادثة--incident-record-expected-vs-actual-vs-evidence)
- [`CHECK-29` قواعد الإصلاح الذاتي](#check-29--قواعد-الإصلاح-الذاتي--self-repair-rules-retry-once-narrower-never-relax-a-safety-gate)
- [`CHECK-30` حَكَم مغلق الخيارات مرتين بترتيب معكوس](#check-30--حَكَم-مغلق-الخيارات-مرتين-بترتيب-معكوس--closed-set-judge-asked-twice-with-reversed-options-a-none-option-and-a-declared-fallback)
- [`CHECK-31` امتحان مختوم قبل العمل](#check-31--امتحان-مختوم-قبل-العمل--exam-sealed-before-the-work)
- [`CHECK-32` خادم نموذج وهمي مسجِّل](#check-32--خادم-نموذج-وهمي-مسجِّل--recording-mock-model-server)
- [`CHECK-33` قائمة سطح الملاحظة](#check-33--قائمة-سطح-الملاحظة--observable-surface-checklist)
- [`CHECK-34` المصحّح يعطي 100% على نفسه أولًا](#check-34--المصحّح-يعطي-100-على-نفسه-أولًا--scorer-must-score-100-on-itself-first)
- [`CHECK-35` ملاحظات استرداد صادقة وخط أساس](#check-35--ملاحظات-استرداد-صادقة-وخط-أساس--honest-recovery-notes-and-a-measured-baseline)

## البطاقات / cards

### `CHECK-01` — حلقة التحقق الثمانية / Verification loop (8 steps until done-criteria pass)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** البيئة لا قناعتك هي الحقيقة: حوّل كل معيار إنجاز إلى فحص، وشغّل الفحوص بالأدوات ثم بالعين، وكرر حتى تنجح أو تنتهي الميزانية. — The environment, not your belief, is ground truth: turn each done-criterion into a check, run checks with tools and then with eyes, loop until they pass or the budget ends.

**متى:** VERIFY step of THINK-01; before any 'done', 'fixed', 'rendered' or 'works'.

**كيف:** 1 Define checks before building: each done-criterion → an observable test (unit test, ffprobe value, screenshot, row count, link opens). 2 Objective checks with tools: tests/linters/build, ffprobe, checksums (user audio untouched), schema validators, repo validators. 3 Perceptual checks: render a frame strip or screenshot and look at it (CHECK-03). 4 Rubric self-critique, with at least one concrete weakness per pass (CHECK-04). 5 Red-team with edge inputs (CHECK-05). 6 Diff against the request: coverage ledger (THINK-18). 7 Record evidence: command → output → badge. 8 Stop rule (CHECK-07).

**المعاملات:** 8 steps · ≥1 weakness found per pass · 2–3 visual iterations

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** verification · testing · qa · evidence · double check · تحقق · تأكد · اختبار · جودة · دليل

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-02` بوابة ما بعد الرندر / Postcondition gate on the delivered file (ffprobe / verify_video.py / measured sync) (proven)
- `CHECK-03` انظر إلى المخرَج بعينك / Look at the output: contact sheets, frames, screenshots (proven)

### `CHECK-02` — بوابة ما بعد الرندر / Postcondition gate on the delivered file (ffprobe / verify_video.py / measured sync)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** افحص الملف المُسلَّم نفسه لا الخطوة الوسيطة: المدة والإطارات والصوت والجهارة، وقِس المزامنة على الـMP4 النهائي. — Check the delivered file itself, not an intermediate step: duration, frames, audio, loudness, and measure sync on the final MP4.

**متى:** Every video, audio or image deliverable; any claim of 'synced', 'right length', '-14 LUFS'.

**كيف:** From the repo root: `python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration <s> --audio voice.wav` (13 checks: codec, size, fps, frame count, duration, AAC, loudness, true peak, audio length = master). Without the repo: `ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames -of json film.mp4` and `ffmpeg -i film.mp4 -af ebur128=peak=true -f null -`. Sync claims: measure on the muxed file (audio onsets vs pixel-change events), as proofs/beat-sync does. General rule for any domain: check the artefact the user receives (open the .docx, load the page, re-read the CSV).

**المعاملات:** 13/13 checks · −14 LUFS ±1 · max sync offset < ½ frame

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** postcondition · ffprobe · verify_video · loudness · sync · فحص الملف · مدة · جهارة · مزامنة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/beat-sync/README.md`
- `kosif-tool/tools/verify_video.py`
- `session-2026-10-16:see-atlas.md#15`

#### 7. قدرات قريبة في العائلة

- `CHECK-01` حلقة التحقق الثمانية / Verification loop (8 steps until done-criteria pass) (documented)
- `CHECK-03` انظر إلى المخرَج بعينك / Look at the output: contact sheets, frames, screenshots (proven)
- `CHECK-04` التقييم الذاتي بخمسة محاور / Five-axis self-evaluation (accuracy, completeness, clarity, actionability, concision) (documented)

### `CHECK-03` — انظر إلى المخرَج بعينك / Look at the output: contact sheets, frames, screenshots

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** الأرقام لا تكفي: صوّر لوحة إطارات أو لقطة شاشة وافتحها وانظر إليها فعلًا قبل الادعاء. — Numbers are not enough: make a contact sheet or screenshot, open it and actually look before claiming.

**متى:** Any visual deliverable: video, page, chart, slide, image; after each preview render.

**كيف:** Make a sheet: `ffmpeg -i film.mp4 -vf "fps=2,scale=320:-1,tile=6x4" -frames:v 1 sheet.png` (or QA-58 `motion.py sheet`), or a Playwright screenshot of the page at 390 and 1440 px. Open it with the Read tool and check: text overflow and clipping, Arabic letters joined and RTL order, contrast, safe zones, tofu boxes, frozen or black stretches. Iterate 2–3 times against the target. Never report a look you did not perform; say 'not viewed' instead.

**المعاملات:** 2 fps sheet · 2–3 iterations · phone width 360–390 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** visual check · contact sheet · screenshot · frames · فحص بصري · لوحة لقطات · لقطة شاشة · إطارات

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/beat-sync/sheet.jpg`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/sheet.jpg`
- `session-2026-10-16:see-atlas.md#15`

#### 7. قدرات قريبة في العائلة

- `CHECK-01` حلقة التحقق الثمانية / Verification loop (8 steps until done-criteria pass) (documented)
- `CHECK-02` بوابة ما بعد الرندر / Postcondition gate on the delivered file (ffprobe / verify_video.py / measured sync) (proven)
- `CHECK-04` التقييم الذاتي بخمسة محاور / Five-axis self-evaluation (accuracy, completeness, clarity, actionability, concision) (documented)
- `CHECK-05` هاجم مخرَجك بنفسك / Red-team your own output (edge inputs + sceptical expert) (documented)

### `CHECK-04` — التقييم الذاتي بخمسة محاور / Five-axis self-evaluation (accuracy, completeness, clarity, actionability, concision)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قيّم عملك على خمسة محاور من 1 إلى 5 كلٌّ على حدة، ومع كل درجة أقل من 5 سطر دليل، وأصلح فورًا ما كان 3 أو أقل. — Score your work 1–5 on five axes independently, add an evidence line for every score below 5, and fix anything at 3 or below.

**متى:** After 3+ files or 50+ lines changed, multi-step workflows, debugging with 3+ attempts, any written analysis, or 'rate yourself'.

**كيف:** Collect: original request, deliverable, verifying outputs (exit codes, tests), user corrections. Score each axis fresh (do not decide an average first): Accuracy (invented APIs or facts?), Completeness (missed sub-tasks, edge cases), Clarity, Actionability (can the user act now; is a verification path given?), Concision. Each score <5 gets one sentence of evidence. Any axis ≤3: fix now if it takes <30 s, otherwise flag it with the fix. Ask 'would the user agree with these scores?'. Not a pass/fail gate.

**المعاملات:** 5 axes × 1–5 · fix if ≤3 and <30 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** self evaluation · rubric · review · التقييم الذاتي · مراجعة · معايير

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-02` بوابة ما بعد الرندر / Postcondition gate on the delivered file (ffprobe / verify_video.py / measured sync) (proven)
- `CHECK-03` انظر إلى المخرَج بعينك / Look at the output: contact sheets, frames, screenshots (proven)
- `CHECK-05` هاجم مخرَجك بنفسك / Red-team your own output (edge inputs + sceptical expert) (documented)
- `CHECK-06` حلقة تحقق الكود / Code verification loop: build → types → lint → tests → secrets → diff (documented)

### `CHECK-05` — هاجم مخرَجك بنفسك / Red-team your own output (edge inputs + sceptical expert)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حاول كسر ما صنعته بمدخلات حدّية، واسأل: ماذا سيقول خبير متشكك إنه خطأ؟ — Try to break what you made with edge inputs, and ask what a sceptical expert would say is wrong.

**متى:** Code, data pipelines, published pages, captions, anything others will rely on.

**كيف:** Edge inputs: empty, huge, malformed, Arabic + digits mixed, long unbroken words, RTL + LTR in one line, mobile width, slow network, missing font, silence in audio. Check each claim against its source. Write the expert's top 3 objections and answer or fix them. Keep at least one concrete weakness per pass — 'looks great' is not a review.

**المعاملات:** ≥8 edge inputs · top 3 objections

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** red team · edge cases · adversarial · robustness · اختبار الحدود · حالات حدية · نقد · متانة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-03` انظر إلى المخرَج بعينك / Look at the output: contact sheets, frames, screenshots (proven)
- `CHECK-04` التقييم الذاتي بخمسة محاور / Five-axis self-evaluation (accuracy, completeness, clarity, actionability, concision) (documented)
- `CHECK-06` حلقة تحقق الكود / Code verification loop: build → types → lint → tests → secrets → diff (documented)
- `CHECK-07` قاعدة التوقف / Stop rule: done means checks pass, or the budget ends with risks stated (documented)

### `CHECK-06` — حلقة تحقق الكود / Code verification loop: build → types → lint → tests → secrets → diff

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** ست مراحل متتالية تنتهي بحكم «جاهز» أو «غير جاهز»، وتتوقف عند أول فشل في البناء. — Six phases ending in READY or NOT READY, stopping at the first build failure.

**متى:** After code changes, before commits, after each major change on long tasks.

**كيف:** Run with `set -o pipefail`: 1 build (stop if it fails) · 2 types (`tsc --noEmit`, `pyright`) · 3 lint (`ruff`, `npm run lint`; cut output with `sed -n '1,30p'` instead of `head` so a passing command is not killed by SIGPIPE) · 4 tests (+ coverage where the project sets a target) · 5 secret grep (`rg -n 'sk-\|api_key\|BEGIN .*PRIVATE KEY'`) · 6 `git diff --stat` review for scope creep. Report a block: Build / Types / Lint / Tests / Security / Diff → READY or NOT READY + issues. In this repo also run `python3 tools/validate.py` after catalog changes.

**المعاملات:** 6 phases · re-run after each major change

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** code verification · tests · lint · build · ci · تحقق الكود · اختبارات · فحص · بناء

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `git` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-04` التقييم الذاتي بخمسة محاور / Five-axis self-evaluation (accuracy, completeness, clarity, actionability, concision) (documented)
- `CHECK-05` هاجم مخرَجك بنفسك / Red-team your own output (edge inputs + sceptical expert) (documented)
- `CHECK-07` قاعدة التوقف / Stop rule: done means checks pass, or the budget ends with risks stated (documented)
- `CHECK-08` سُلَّم الأدلة للادعاءات / Evidence ladder for claims (badges are earned, leased and downgraded) (documented)

### `CHECK-07` — قاعدة التوقف / Stop rule: done means checks pass, or the budget ends with risks stated

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** توقف عندما تنجح كل الفحوص أو تنتهي الميزانية، ثم أبلغ بالمخاطر الباقية بصدق؛ «يعمل عندي» ليس نهاية. — Stop when all checks pass or the budget ends, then report residual risks honestly; 'it compiles' is not the end.

**متى:** Deciding whether to keep iterating or deliver.

**كيف:** Done = every done-criterion check passed with evidence. Budget hit = deliver the best verified slice + a list of what is unverified and why + the next step. Do not stop at: first draft, 'it compiles', 'the command ran', a success message, a plan. Do not loop forever either: cap iterations (2–4 review rounds for renders, ≤3 fix loops for reviewers) and escalate to the user.

**المعاملات:** 2–4 rounds · explicit budget

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stop rule · done · budget · iteration cap · قاعدة التوقف · إنجاز · ميزانية · حد التكرار

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-05` هاجم مخرَجك بنفسك / Red-team your own output (edge inputs + sceptical expert) (documented)
- `CHECK-06` حلقة تحقق الكود / Code verification loop: build → types → lint → tests → secrets → diff (documented)
- `CHECK-08` سُلَّم الأدلة للادعاءات / Evidence ladder for claims (badges are earned, leased and downgraded) (documented)
- `CHECK-09` الإيصال المنمَّط / Typed receipt after consequential actions (documented)

### `CHECK-08` — سُلَّم الأدلة للادعاءات / Evidence ladder for claims (badges are earned, leased and downgraded)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** كل ادعاء يحمل شارة أدنى حالة صحيحة؛ لا تُرفع الشارة من رسالة نجاح بل من فحص منجز، والإثبات القديم صالح بتاريخه فقط حتى يُعاد فحصه. — Every claim carries the badge of its lowest true state; a badge rises from a checked postcondition, never from a success message, and old proof is a dated lease.

**متى:** Writing any status, catalog record, report or 'what can you do' answer.

**كيف:** Ladder: 💡 idea → 📄 documented → 📦 install (one documented command away) → 🔑 key/account → 🟢 ready (code here runs with usual tools) → ✅ proven (ran, with a proof path); 👁 seen applies to motion references only. Rules: (1) use the lowest true badge; (2) upgrade only with a proof file or a dated run record; (3) a ✅ from another container is a lease — re-probe before relying on it; a failed probe downgrades the claim for this answer only and goes into the environment snapshot, history is not rewritten; (4) separate 'proven in this container', 'on claude.ai', 'API-only'.

**المعاملات:** 7 badges · proof path required for ✅

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** evidence ladder · badges · proof · honesty · سُلَّم الأدلة · شارات · إثبات · صدق

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-06` حلقة تحقق الكود / Code verification loop: build → types → lint → tests → secrets → diff (documented)
- `CHECK-07` قاعدة التوقف / Stop rule: done means checks pass, or the budget ends with risks stated (documented)
- `CHECK-09` الإيصال المنمَّط / Typed receipt after consequential actions (documented)
- `CHECK-10` كلمات الحالة الصادقة / Honest status words (stage by stage) (documented)

### `CHECK-09` — الإيصال المنمَّط / Typed receipt after consequential actions

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** بعد كل فعل مهم أعد إيصالًا: الحالة، الملخص، المنفِّذ، أدلة مكتوبة بنوعها ومرجعها، المخرجات، الخطوة التالية، وهل الإعادة آمنة، وهل تحققتَ. — After any consequential action return a receipt: status, summary, owner, typed evidence, artefacts, next actions, whether a retry is safe, and whether the postcondition was checked.

**متى:** Renders, deployments, file conversions, publishes, data writes, subagent hand-offs.

**كيف:** Shape: {status: success\|warning\|error, summary, owner, evidence: [{type, ref}], artifacts: [], next_actions: [], retryable: bool, verified: bool}. Rules: verified:true needs status success AND ≥1 evidence item with a type and a reference (command output line, file path, ffprobe JSON); error can never be verified; warning + verified:false is an honest partial. Evidence must be typed objects — free text such as 'I checked it' does not count (an owner gate tool was found to accept it in session-2026-10-16, a gap to avoid).

**المعاملات:** 8 fields · evidence items {type, ref}

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** receipt · status · evidence · postcondition · إيصال · حالة · دليل · شرط لاحق

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-07` قاعدة التوقف / Stop rule: done means checks pass, or the budget ends with risks stated (documented)
- `CHECK-08` سُلَّم الأدلة للادعاءات / Evidence ladder for claims (badges are earned, leased and downgraded) (documented)
- `CHECK-10` كلمات الحالة الصادقة / Honest status words (stage by stage) (documented)
- `CHECK-11` التقييم أولًا / Eval-first: capability evals + regression evals (documented)

### `CHECK-10` — كلمات الحالة الصادقة / Honest status words (stage by stage)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** صِف كل مرحلة بكلمتها الدقيقة: فُحص، عُدّل محليًا، تُحقق منه محليًا، أُودع (commit)، دُفع (push)، متوقف بمانع؛ وللموشن: كُتب الكود، عُرضت المعاينة، رُندر الفيديو، اجتاز الفحص. — Describe each stage with its exact word: inspected, changed locally, verified locally, committed, pushed, blocked; for motion: written, previewed, rendered, verified.

**متى:** Every progress update and final report.

**كيف:** Code: inspected · changed locally · verified locally (which command) · committed · pushed · blocked (reason + next step). Motion: CODE_WRITTEN ≠ PREVIEWED ≠ VIDEO_RENDERED ≠ QA_PASS. Documents: drafted · exported · opened and checked. Never merge stages ('done') when only the first happened.

**المعاملات:** 6 code words · 4 motion stages

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** status words · reporting · stages · honesty · كلمات الحالة · مراحل · تقرير · صدق

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-08` سُلَّم الأدلة للادعاءات / Evidence ladder for claims (badges are earned, leased and downgraded) (documented)
- `CHECK-09` الإيصال المنمَّط / Typed receipt after consequential actions (documented)
- `CHECK-11` التقييم أولًا / Eval-first: capability evals + regression evals (documented)
- `CHECK-12` pass@k مقابل pass^k / pass@k vs pass^k (any success vs always success) (documented)

### `CHECK-11` — التقييم أولًا / Eval-first: capability evals + regression evals

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** عرّف التقييمات قبل البناء: تقييمات قدرة للسلوك الجديد وتقييمات انحدار لما كان يعمل، بمقيّمين من كود ونموذج وإنسان. — Define evals before building: capability evals for new behaviour and regression evals for what already worked, graded by code, model and human.

**متى:** New features, prompt or skill changes, any 'make it better' work.

**كيف:** Capability eval: checklist criteria for the new behaviour. Regression eval: baseline commit + X/Y cases passing. Graders: code (grep, test, build → PASS/FAIL) first; model (1–5 rubric: solves the problem, structure, edge cases, errors) for what code cannot check; human for risk LOW/MED/HIGH. Start with ≈20 real queries; an LLM judge giving 0–1 per criterion plus pass/fail in one call matched human judgement best in Anthropic's research eval.

**المعاملات:** ≈20 real cases to start · code graders before model graders

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** evals · regression · graders · benchmark · تقييم · انحدار · مقيّم · اختبارات

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-09` الإيصال المنمَّط / Typed receipt after consequential actions (documented)
- `CHECK-10` كلمات الحالة الصادقة / Honest status words (stage by stage) (documented)
- `CHECK-12` pass@k مقابل pass^k / pass@k vs pass^k (any success vs always success) (documented)
- `CHECK-13` بوابة الفشل القاطع / Hard-fail gate: one must-never-happen failure blocks release (documented)

### `CHECK-12` — pass@k مقابل pass^k / pass@k vs pass^k (any success vs always success)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** pass@k يقيس نجاح محاولة واحدة على الأقل من k، وpass^k يقيس نجاح كل المحاولات؛ استخدم الثاني حين يهم الثبات. — pass@k measures at least one success in k tries; pass^k measures all k succeeding; use the latter when consistency matters.

**متى:** Judging reliability of a prompt, skill, agent or pipeline; deciding whether 'it worked once' is enough.

**كيف:** Run the same case k times (k = 3 is a good default). Exploratory or creative work: pass@3 > 90% is fine. Critical paths and regressions: require pass^3 = 100%. Remember the gap (computed in code, independent runs): with a 70% single-run rate, pass@2 = 91%, pass@3 ≈ 97.3%, but pass^3 ≈ 34.3% and pass^5 ≈ 16.8% — 'it worked once' says little about 'it works'. Note: the ECC guide pairs 91% with k = 3; that figure is the k = 2 value — an example of why numbers go to code (THINK-17). Compute these from a results table, not by hand.

**المعاملات:** k = 3 · pass@3 > 90% exploratory · pass^3 = 100% critical · p = 0.7 → pass@3 0.973, pass^3 0.343

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pass@k · pass^k · reliability · consistency · موثوقية · ثبات · تكرار التجربة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-10` كلمات الحالة الصادقة / Honest status words (stage by stage) (documented)
- `CHECK-11` التقييم أولًا / Eval-first: capability evals + regression evals (documented)
- `CHECK-13` بوابة الفشل القاطع / Hard-fail gate: one must-never-happen failure blocks release (documented)
- `CHECK-14` انضباط المحكِّم / Judge discipline: assertions first, one criterion per judgement, cited evidence (documented)

### `CHECK-13` — بوابة الفشل القاطع / Hard-fail gate: one must-never-happen failure blocks release

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** عرّف معايير النجاح نعم/لا قبل رؤية النتائج، وأي فشل قاطع واحد يمنع التسليم مهما كان المتوسط. — Define yes/no success criteria before seeing results; one hard failure blocks delivery whatever the average.

**متى:** Releases, skill updates, published content, anything with must-never-happen cases.

**كيف:** Write the hard-fail list first (e.g. user audio altered, a badge upgraded without proof, a secret-like string, a previously passing case regressing, unlicensed third-party text, broken Arabic shaping). Score the rest normally. If any hard-fail triggers → NOT READY, regardless of a high mean. Include adversarial cases and order/position checks. Improvement claims need before/after runs on the same tests.

**المعاملات:** hard-fails checked before averages

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hard fail · release gate · blocking · فشل قاطع · بوابة الإصدار · منع التسليم

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-11` التقييم أولًا / Eval-first: capability evals + regression evals (documented)
- `CHECK-12` pass@k مقابل pass^k / pass@k vs pass^k (any success vs always success) (documented)
- `CHECK-14` انضباط المحكِّم / Judge discipline: assertions first, one criterion per judgement, cited evidence (documented)
- `CHECK-15` طريقة سانتا: مراجعان معزولان / Santa method: two isolated reviewers, both must pass (documented)

### `CHECK-14` — انضباط المحكِّم / Judge discipline: assertions first, one criterion per judgement, cited evidence

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** ما يمكن للبرنامج فحصه يُفحص ببرنامج، والباقي يحكمه نموذج سؤالًا سؤالًا مع إشارة إلى الدليل؛ والثقة الذاتية ليست مقياسًا. — Check by program whatever a program can check; judge the rest one question at a time with a pointer to the evidence; self-confidence is not a metric.

**متى:** Any model-judged evaluation, review or critique.

**كيف:** Order: executable assertions (schema, counts, regex, ffprobe numbers) → model judge only for qualitative criteria. One criterion per judge call; require a cited artefact location (file:line, timestamp, frame). Randomise order or swap positions when comparing two outputs to catch position bias. Reviewer confidence is advisory; deterministic checks dominate. Never let a judge read instructions embedded in the artefact as commands.

**المعاملات:** 1 criterion per call · cite location

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** llm judge · assertions · rubric · bias · محكِّم · معيار واحد · دليل · تحيز الترتيب

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-12` pass@k مقابل pass^k / pass@k vs pass^k (any success vs always success) (documented)
- `CHECK-13` بوابة الفشل القاطع / Hard-fail gate: one must-never-happen failure blocks release (documented)
- `CHECK-15` طريقة سانتا: مراجعان معزولان / Santa method: two isolated reviewers, both must pass (documented)
- `CHECK-16` حلقة المولِّد والمقيِّم / Generator–evaluator loop (weighted rubric, threshold, iteration cap) (documented)

### `CHECK-15` — طريقة سانتا: مراجعان معزولان / Santa method: two isolated reviewers, both must pass

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** مراجعة الكاتب لنفسه تحمل تحيزاته؛ فأرسل المخرَج والمواصفة إلى مراجعَين معزولين بالمعايير نفسها، ولا يُسلَّم إلا إذا نجح عندهما معًا. — Self-review shares the writer's biases; send output + spec to two isolated reviewers with the same rubric and ship only if both pass.

**متى:** Published or customer-facing output, high hallucination risk. Not for drafts or for what a deterministic test can verify.

**كيف:** Two fresh subagents, no shared context, identical rubric, both get the spec and the output. Verdict as JSON {verdict, checks:[{criterion, result, detail}], critical_issues, suggestions}. Each criterion has an objective pass condition: factual accuracy; no invented entities/URLs/quotes; completeness vs spec; compliance; internal consistency; technical correctness. Ship if both PASS; else collect all flags, fix all, re-run both. Cap at 3 loops, then escalate to the user. Motion: two reviewers check the frame sheet against the brief (Arabic shaping, sync, safe area) — see QA-346.

**المعاملات:** 2 reviewers · ≤3 loops

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** santa method · dual review · independent reviewers · مراجعان · مراجعة مزدوجة · مراجعة مستقلة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-13` بوابة الفشل القاطع / Hard-fail gate: one must-never-happen failure blocks release (documented)
- `CHECK-14` انضباط المحكِّم / Judge discipline: assertions first, one criterion per judgement, cited evidence (documented)
- `CHECK-16` حلقة المولِّد والمقيِّم / Generator–evaluator loop (weighted rubric, threshold, iteration cap) (documented)
- `CHECK-17` المتحقق العدائي / Adversarial verifier that defaults to 'refuted' (documented)

### `CHECK-16` — حلقة المولِّد والمقيِّم / Generator–evaluator loop (weighted rubric, threshold, iteration cap)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** افصل الصانع عن الناقد: مقيّم صارم يختبر المخرَج الحي بمعايير موزونة، والحلقة تستمر حتى عتبة أو حد أقصى. — Separate maker from critic: a strict evaluator tests the live artefact against weighted criteria, looping until a threshold or a cap.

**متى:** Visual or interactive work where quality is judged (pages, apps, motion previews); not for one-file fixes.

**كيف:** Planner writes the spec and the evaluator's rubric first. Generator builds and agrees a 'sprint contract' with the evaluator. Evaluator tests the LIVE artefact (Playwright clicks/forms, screenshots, rendered frames), never just the code. Weights: design 0.3 · originality 0.2 · craft 0.3 · functionality 0.2. Anchors: 1–3 generic, 4–6 competent, 7–8 distinctive and polished, 9–10 professional and novel. Loop until weighted ≥ 7.0 or 15 iterations (5–15 typical). Expensive: use when the deliverable's value justifies it.

**المعاملات:** weights 0.3/0.2/0.3/0.2 · stop at ≥7.0 or 15 iterations

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** generator evaluator · gan · critic · iteration · مولد ومقيم · ناقد · تكرار · معايير موزونة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-14` انضباط المحكِّم / Judge discipline: assertions first, one criterion per judgement, cited evidence (documented)
- `CHECK-15` طريقة سانتا: مراجعان معزولان / Santa method: two isolated reviewers, both must pass (documented)
- `CHECK-17` المتحقق العدائي / Adversarial verifier that defaults to 'refuted' (documented)
- `CHECK-18` حلقة تحسين الأداء بالقياس / Benchmark-optimisation loop (one hypothesis per variant) (documented)

### `CHECK-17` — المتحقق العدائي / Adversarial verifier that defaults to 'refuted'

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** لكل ملاحظة حرجة متحقق مستقل يفترض أنها غير مثبتة حتى يرى الدليل؛ وغياب مراجع يعني «تغييرات مطلوبة» لا نجاحًا. — Each critical finding goes to an independent verifier that assumes it is unproven until it sees evidence; a missing reviewer means 'changes requested', never a pass.

**متى:** Reviews with many findings, security or correctness claims, merging parallel reviewer outputs.

**كيف:** Parallel reviewers per dimension → deduplicate findings by normalised evidence snippet → for each CRITICAL/HIGH, an adversarial verifier tries to refute it and defaults to refuted on uncertainty (avoids false alarms) — the same stance applies to success claims (unproven until evidence). Fail closed: a reviewer that did not return → CHANGES_REQUESTED, incomplete = true. A human approves the final gate.

**المعاملات:** default = refuted / unproven

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** adversarial · verifier · fail closed · review · متحقق عدائي · فشل آمن · مراجعة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-15` طريقة سانتا: مراجعان معزولان / Santa method: two isolated reviewers, both must pass (documented)
- `CHECK-16` حلقة المولِّد والمقيِّم / Generator–evaluator loop (weighted rubric, threshold, iteration cap) (documented)
- `CHECK-18` حلقة تحسين الأداء بالقياس / Benchmark-optimisation loop (one hypothesis per variant) (documented)
- `CHECK-19` فحص تصميم الحلقة / Loop design check before automating anything (documented)

### `CHECK-18` — حلقة تحسين الأداء بالقياس / Benchmark-optimisation loop (one hypothesis per variant)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** حسّن بالقياس لا بالحدس: خط أساس، ثم متغيرات كل منها يختبر فرضية واحدة على المدخل نفسه، ثم ترقية أسرع متغير آمن. — Optimise by measurement: baseline, variants testing one hypothesis each on the same input, then promote the fastest safe one.

**متى:** Render speed, query time, cost per run, memory — any 'make it faster/cheaper'.

**كيف:** Before: operation, correctness gate, metric (wall time, p95, rows/s, cost/run, memory), baseline, budget (max variants/time/spend). Loop: measure baseline → locate the bottleneck from evidence → variants with ONE change each → same input shape → reject incorrect, unsafe or irreproducible → promote the fastest safe → codify it in a script/config → re-run baseline vs winner. Keep a table: variant \| hypothesis \| command \| time \| correct? \| notes. Stop when gains are within noise, correctness fails, the budget is spent or too many variables move. Say 'best measured safe variant', never 'optimal'.

**المعاملات:** 1 hypothesis per variant · repeat the winning delta

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** benchmark · optimization · performance · measurement · قياس الأداء · تحسين · سرعة · خط أساس

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-16` حلقة المولِّد والمقيِّم / Generator–evaluator loop (weighted rubric, threshold, iteration cap) (documented)
- `CHECK-17` المتحقق العدائي / Adversarial verifier that defaults to 'refuted' (documented)
- `CHECK-19` فحص تصميم الحلقة / Loop design check before automating anything (documented)
- `CHECK-20` اختبار الطفرات للمدقِّق / Mutation-test your validator (seed defects, count catches) (documented)

### `CHECK-19` — فحص تصميم الحلقة / Loop design check before automating anything

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قبل بناء حلقة آلية تأكد أن المهمة تتكرر، وأن التحقق آلي، وأن الهدف قابل للحسم بأمر واحد، وأن للحلقة حدودًا وسقف محاولات. — Before building an automated loop, make sure the task repeats, verification is automatic, the goal is decidable by one command, and the loop has boundaries and a retry cap.

**متى:** Scheduled tasks, render/QA loops, auto-fixers, 'keep doing X until Y'.

**كيف:** Gate (all must hold, else do it by hand): repeats ≥ weekly · verification automatable · token budget fits · the agent has tools that really run and observe. Goal: (1) machine-decidable done ('96 tests green AND change-list produced', not 'make it good'); (2) boundary list of what must NOT happen (anti-Goodhart: no deleted or weakened tests, never touch user audio); (3) retry cap N then escalate; (4) layered goals; (5) reconcile against an external fact over self-assertion. Five failure modes to review: platitude goal, self-judging verification, 'tests pass' only, relying on mid-run clarification, stale bloated memory. Irreversible steps (merge, publish, spend) stay with a human.

**المعاملات:** 4-part gate · 5-point goal · 5 failure modes · retry cap ≈3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** loop design · automation · goodhart · guardrails · تصميم الحلقة · أتمتة · حدود · سقف المحاولات

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-17` المتحقق العدائي / Adversarial verifier that defaults to 'refuted' (documented)
- `CHECK-18` حلقة تحسين الأداء بالقياس / Benchmark-optimisation loop (one hypothesis per variant) (documented)
- `CHECK-20` اختبار الطفرات للمدقِّق / Mutation-test your validator (seed defects, count catches) (documented)
- `CHECK-21` مصفوفة اختبار التفعيل / Trigger eval matrix for a skill (+ with/without A/B) (documented)

### `CHECK-20` — اختبار الطفرات للمدقِّق / Mutation-test your validator (seed defects, count catches)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** لا تثق بمدقِّق لم تختبره: أدخل عيوبًا معروفة في نسخ ووثّق كم منها التقط. — Do not trust an untested validator: seed known defects into copies and record how many it catches.

**متى:** Writing or relying on any check script, gate, schema validator or eval runner.

**كيف:** Make 8–12 mutated copies, one defect each (version drift, missing field, removed item, secret-like string, broken path, emptied list, wrong type). Run the validator on each; table: mutation \| caught? \| message. Fix the blind spots or document them. Real example from session-2026-10-16: an owner gate tool caught 8/12 seeded defects and missed 4 (unscanned files, an unchecked cap, an emptied list, a second manifest); its secret regex missed ghp_, AKIA and 'Bearer' tokens.

**المعاملات:** 8–12 mutations · report caught/total

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mutation testing · validator · test the test · اختبار الطفرات · مدقق · اختبار الاختبار

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-18` حلقة تحسين الأداء بالقياس / Benchmark-optimisation loop (one hypothesis per variant) (documented)
- `CHECK-19` فحص تصميم الحلقة / Loop design check before automating anything (documented)
- `CHECK-21` مصفوفة اختبار التفعيل / Trigger eval matrix for a skill (+ with/without A/B) (documented)
- `CHECK-22` لقطة الفهرس والمدقِّق / Catalog snapshot: powers.py stats + repo validator (proven)

### `CHECK-21` — مصفوفة اختبار التفعيل / Trigger eval matrix for a skill (+ with/without A/B)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** اختبر المهارة بحالات إيجابية وسلبية مجاورة وتصادمات وفجوات وآثار جانبية وحالات قديمة، وافصل الحالات الحتمية عن المحكومة بنموذج. — Test a skill with positive, adjacent-negative, collision, gap, side-effect and stale cases, separating deterministic cases from model-judged ones.

**متى:** Before and after editing a skill's description, SKILL.md or routing; when a skill seems to over- or under-trigger.

**كيف:** Cases (examples): trivial 'احسب 37+15' → answer directly, load nothing · 'اعمل ريلز من الصوت ده' + audio → audio-sync + Arabic type, render + verify · 'what can you do?' → capability summary with badges, flag ✅ items not present now · missing library → install in venv then verify, never 'can't' · paid voice → name the key 🔑 and offer a keyless option · a ✅ binary missing here → re-probe and downgrade for this answer · 'احسب ضريبة القيمة المضافة على 1000' → compute in code. Deterministic cases get a runner script; judged cases run with and without the change in a fresh subagent against a rubric written before the run. Record dated results per version. Keyword triggers are recall hints: a naive substring router reproduced only 15/24 expectations of an owner eval set.

**المعاملات:** 6 case types · deterministic vs judged · dated results

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** trigger eval · skill testing · routing · a/b · اختبار التفعيل · تقييم المهارة · توجيه

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-19` فحص تصميم الحلقة / Loop design check before automating anything (documented)
- `CHECK-20` اختبار الطفرات للمدقِّق / Mutation-test your validator (seed defects, count catches) (documented)
- `CHECK-22` لقطة الفهرس والمدقِّق / Catalog snapshot: powers.py stats + repo validator (proven)
- `CHECK-23` بوابة السجلات الحتمية / Deterministic record gate for the power catalog (mutation-tested) (proven)

### `CHECK-22` — لقطة الفهرس والمدقِّق / Catalog snapshot: powers.py stats + repo validator

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** قبل تعديل المهارة وبعده خذ لقطة: الإيداع الحالي، وإحصاءات القوى، ونتيجة المدقِّق. — Before and after changing the skill take a snapshot: current commit, power stats and validator result.

**متى:** Step 1 of any skill or catalog change (CHECK-24); after the change for the before/after diff.

**كيف:** From the repo root: `git rev-parse --short HEAD` · `python3 .claude/skills/kosif-superpowers/scripts/powers.py stats` (powers per family and status) · `python3 tools/validate.py` (repo catalog checks) · the record gate snippet in references/verification.md (IDs unique, required keys, status valid, ✅ has proof, no secret-like strings) · list proofs (`ls .claude/skills/kosif-superpowers/proofs`) · environment snapshot (re-run scripts/probe_env.py). Save the outputs in the change note; compare after.

**المعاملات:** 5 outputs saved before and after

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** snapshot · baseline · stats · validator · لقطة · خط أساس · إحصاءات · مدقق

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `session-2026-10-16:skill-audit.md#2`
- `session-2026-10-16:skill-audit.md#4`
- `kosif-tool/.claude/skills/kosif-superpowers/scripts/powers.py`
- `kosif-tool/tools/validate.py`

#### 7. قدرات قريبة في العائلة

- `CHECK-20` اختبار الطفرات للمدقِّق / Mutation-test your validator (seed defects, count catches) (documented)
- `CHECK-21` مصفوفة اختبار التفعيل / Trigger eval matrix for a skill (+ with/without A/B) (documented)
- `CHECK-23` بوابة السجلات الحتمية / Deterministic record gate for the power catalog (mutation-tested) (proven)
- `CHECK-24` حلقة التطوير الذاتي للمهارة / Self-evolution loop for this skill (evolve with evidence) (documented)

### `CHECK-23` — بوابة السجلات الحتمية / Deterministic record gate for the power catalog (mutation-tested)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** سكربت قصير يفحص كل سجلات القوى: معرّفات فريدة، حقول مطلوبة، حالة صحيحة، إثبات لكل ✅، لا أسرار، لا أسماء نماذج، ووصف ثنائي اللغة. — A short script that checks every power record: unique IDs, required keys, valid status, proof for every ✅, no secrets, no model names, bilingual 'what'.

**متى:** Before committing any change to data/powers/*.json; as the deterministic half of CHECK-21 and step 5 of CHECK-24.

**كيف:** Copy the snippet from references/verification.md §5 and run it from the repo root (stdlib only; env KOSIF_SK / KOSIF_HOME point it at a copy). Exit 0 = clean, 1 = problems listed. Legacy motion records (no 'domain') need only the 13 base keys; new-domain records also need domain, when, section, source and an 'AR — EN' what. Limits: it does not judge Arabic correctness, proof paths outside kosif-tool/, session-distill citations or cross-references between IDs — review those by eye.

**المعاملات:** 13 base keys + 4 new-domain keys · 10/10 seeded defects caught, 2/2 controls clean

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** validator · catalog · json · gate · mutation tested · مدقق · فهرس · بوابة · اختبار الطفرات

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/references/verification.md`

#### 7. قدرات قريبة في العائلة

- `CHECK-21` مصفوفة اختبار التفعيل / Trigger eval matrix for a skill (+ with/without A/B) (documented)
- `CHECK-22` لقطة الفهرس والمدقِّق / Catalog snapshot: powers.py stats + repo validator (proven)
- `CHECK-24` حلقة التطوير الذاتي للمهارة / Self-evolution loop for this skill (evolve with evidence) (documented)
- `CHECK-25` دروس بموافقة ونطاق مشروع / Consent-scoped lessons (growth log) (documented)

### `CHECK-24` — حلقة التطوير الذاتي للمهارة / Self-evolution loop for this skill (evolve with evidence)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** طوّر المهارة بالأدلة: لقطة، فرضية بجملة، أصغر تغيير قابل للتراجع، مصفوفة تقييم، قائمة فشل قاطع، قرار، قراءة راجعة، وسجل تغييرات. — Evolve the skill with evidence: snapshot, one-sentence hypothesis, smallest reversible change, eval matrix, hard-fail list, decision, read-back, changelog.

**متى:** Any request to improve, extend or fix kosif-superpowers (or any skill); after a session reveals a missing power or a wrong badge.

**كيف:** 1 Snapshot (CHECK-22). 2 Hypothesis: 'Claude forgets X; after the change, case Y routes to Z'. 3 Smallest reversible change on a branch: extend an existing family before adding one; never renumber IDs; new IDs append. 4 Rebuild generated files (chapters from JSON via scripts/build_chapters.py). 5 Eval matrix (CHECK-21): deterministic record gate (CHECK-23) + judged with/without cases. 6 Hard-fails (CHECK-13): validator fails, badge upgraded without proof, a passing case regresses, secret-like string, third-party text without a compatible licence, model names in skill files, SKILL.md description loses Arabic or English triggers. 7 Decide on evidence only. 8 Commit when asked, then read back the changed files from disk (a skill edited mid-session may not reload — read the file, do not republish blindly). 9 Changelog: date, hypothesis, change, cases run, expected vs actual, what is still unverified.

**المعاملات:** 9 steps · 7 hard-fails

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** self evolution · improve skill · changelog · regression · تطوير ذاتي · تحسين المهارة · سجل التغييرات · انحدار

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-22` لقطة الفهرس والمدقِّق / Catalog snapshot: powers.py stats + repo validator (proven)
- `CHECK-23` بوابة السجلات الحتمية / Deterministic record gate for the power catalog (mutation-tested) (proven)
- `CHECK-25` دروس بموافقة ونطاق مشروع / Consent-scoped lessons (growth log) (documented)
- `CHECK-26` سجل القرارات المتكرر / Decision ledger for repeated rollouts (documented)

### `CHECK-25` — دروس بموافقة ونطاق مشروع / Consent-scoped lessons (growth log)

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** سجّل الدرس فقط بموافقة المستخدم وداخل المشروع، بصيغة «في المرة القادمة حين أرى X سأفعل Y»، ولا تعمّمه إلا بعد ثبوته في مشروعين مختلفين. — Record a lesson only with the user's consent and inside the project, as 'next time I see X I will do Y'; generalise it only after it holds in two unrelated projects.

**متى:** After a failure, a user correction, a discovered method, or a capability change.

**كيف:** Extract: one-sentence event → 3–5 whys → generalise the class → rule → a named observable signal. Entry 4–8 sentences; title names the pattern; types: failure, method, pattern, capability change (before/after). Search existing lessons first and merge same-root-cause entries. Keep it project-scoped with consent; no secrets or personal data. Promote to the skill catalog only after evidence in ≥2 distinct projects, a negative-case test and user approval; then it becomes a power record with a badge and proof.

**المعاملات:** ≥2 projects before promotion · 4–8 sentences

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lessons · growth log · learning · memory · دروس · سجل التعلم · موافقة · تعميم

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-23` بوابة السجلات الحتمية / Deterministic record gate for the power catalog (mutation-tested) (proven)
- `CHECK-24` حلقة التطوير الذاتي للمهارة / Self-evolution loop for this skill (evolve with evidence) (documented)
- `CHECK-26` سجل القرارات المتكرر / Decision ledger for repeated rollouts (documented)
- `CHECK-27` تصنيف الأعطال وأصغر إصلاح / Failure taxonomy → smallest repair (documented)

### `CHECK-26` — سجل القرارات المتكرر / Decision ledger for repeated rollouts

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** للقرارات التي تتكرر أضف سطرًا لكل جولة في سجل لا يُمحى، وتذكّر أن تكرار الثقة ليس موافقة. — For decisions that recur, append one line per round to an append-only ledger; repeated confidence is not approval.

**متى:** Repeated tuning (thresholds, style packs, prompts), staged rollouts, A/B iterations.

**كيف:** Append JSONL per round: prior winner, new information, search-space size, trials, mark (accept / watch / reject / decay / replay), coherence with the prior, promotion gate. Default to dry-run or paper mode until the gate passes. Lead every summary with the decision. Never overwrite history; corrections are new lines.

**المعاملات:** 1 line per round · append-only

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** decision ledger · rollout · append-only · سجل القرارات · جولات · إطلاق تدريجي

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-24` حلقة التطوير الذاتي للمهارة / Self-evolution loop for this skill (evolve with evidence) (documented)
- `CHECK-25` دروس بموافقة ونطاق مشروع / Consent-scoped lessons (growth log) (documented)
- `CHECK-27` تصنيف الأعطال وأصغر إصلاح / Failure taxonomy → smallest repair (documented)
- `CHECK-28` سجل الحادثة / Incident record: expected vs actual vs evidence (documented)

### `CHECK-27` — تصنيف الأعطال وأصغر إصلاح / Failure taxonomy → smallest repair

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** سمِّ العطل باسمه من الدليل، ثم طبّق أصغر إصلاح معروف له بدل إعادة المحاولة العمياء. — Name the failure from evidence, then apply its smallest known repair instead of blind retrying.

**متى:** Any error, failed check, odd tool result or broken render.

**كيف:** UNVERIFIED_SUCCESS → downgrade the claim to 'executed, not verified' and run the postcondition check · STALE_STATE → re-probe live state · BAD_TOOL_ARGS → read the schema, fix once, never resend identical args · PROBE_ABORT → run independent probes separately · MISSING_DEP → install in an isolated env, verify import/version · NEEDS_AUTH → name the exact key/connector; never ask for secrets casually in chat · NUMERIC_CONTAMINATION → recompute in code, keep the frozen value · REVIEWERS_FAILED → answer from verified evidence only and say review was not obtained · SUPPLY_CHAIN_RISK → read the source, do not run third-party scripts · REGRESSION → roll back · CATALOG_STALE → read the file on disk, do not republish · HALLUCINATED_FLAG → `--help` first · WRONG_CWD → print pwd/branch before writes. Full table with symptoms in references/verification.md.

**المعاملات:** 13 named failures

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** failure taxonomy · errors · repair · debugging · تصنيف الأعطال · أخطاء · إصلاح · تشخيص

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-25` دروس بموافقة ونطاق مشروع / Consent-scoped lessons (growth log) (documented)
- `CHECK-26` سجل القرارات المتكرر / Decision ledger for repeated rollouts (documented)
- `CHECK-28` سجل الحادثة / Incident record: expected vs actual vs evidence (documented)
- `CHECK-29` قواعد الإصلاح الذاتي / Self-repair rules: retry once, narrower; never relax a safety gate (documented)

### `CHECK-28` — سجل الحادثة / Incident record: expected vs actual vs evidence

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** لكل عطل مهم سطر: العَرَض، الأمر المجرَّب، المتوقع، الفعلي، الدليل، السبب (مؤكد أم فرضية)، الإصلاح، طريقة التحقق، والحالة. — For each significant failure write one row: symptom, command tried, expected, actual, evidence, cause (verified or hypothesis), fix, how to verify, status.

**متى:** Failures that took more than one attempt, recurring pipeline problems, anything a later session should not rediscover.

**كيف:** Row: ID · date · symptom · exact command · expected · actual · evidence (path/output line) · cause [verified \| hypothesis] · fix · acceptance check · status OPEN / BLOCKED / VERIFIED. Never set VERIFIED without the acceptance check output; writing a log does not repair anything. Example: 'Arabic letters disconnected in burned captions → libass/raqm missing → `ffmpeg -filters \| grep subtitles` → use the HarfBuzz path → frame grab shows joined letters → VERIFIED'.

**المعاملات:** 11 fields · VERIFIED needs acceptance output

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** incident · troubleshooting · postmortem · حادثة · استكشاف الأعطال · تحليل لاحق

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-26` سجل القرارات المتكرر / Decision ledger for repeated rollouts (documented)
- `CHECK-27` تصنيف الأعطال وأصغر إصلاح / Failure taxonomy → smallest repair (documented)
- `CHECK-29` قواعد الإصلاح الذاتي / Self-repair rules: retry once, narrower; never relax a safety gate (documented)
- `CHECK-30` حَكَم مغلق الخيارات مرتين بترتيب معكوس / Closed-set judge asked twice with reversed options, a 'none' option and a declared fallback (documented)

### `CHECK-29` — قواعد الإصلاح الذاتي / Self-repair rules: retry once, narrower; never relax a safety gate

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** أعد محاولة الجزء الفاشل وحده مرة واحدة بتعليمات أضيق، واحتفظ بنتائج الأجزاء الناجحة، ولا تُضعف بوابات الأمان أو الإذن أو التكلفة لتكمل. — Retry only the failed piece, once, with a narrower instruction; keep successful peers; never weaken safety, permission or cost gates to finish.

**متى:** After any failure in a multi-step or parallel task.

**كيف:** Classify from evidence (CHECK-27) → smallest reversible repair within current authority → regression check → retry only the failed step, once, smaller → continue the preserved request. Never: identical retry after a schema error; blind retry after an uncertain consequential mutation (check the actual state first); relaxing auth, paid, destructive or publishing gates; claiming a repair you did not perform. If still failing: quarantine and report it as failed with the evidence.

**المعاملات:** 1 retry · narrower brief

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** self repair · retry · safety · recovery · إصلاح ذاتي · إعادة المحاولة · أمان · تعافٍ

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-27` تصنيف الأعطال وأصغر إصلاح / Failure taxonomy → smallest repair (documented)
- `CHECK-28` سجل الحادثة / Incident record: expected vs actual vs evidence (documented)
- `CHECK-30` حَكَم مغلق الخيارات مرتين بترتيب معكوس / Closed-set judge asked twice with reversed options, a 'none' option and a declared fallback (documented)
- `CHECK-31` امتحان مختوم قبل العمل / Exam sealed before the work (documented)

### `CHECK-30` — حَكَم مغلق الخيارات مرتين بترتيب معكوس / Closed-set judge asked twice with reversed options, a 'none' option and a declared fallback

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** لاختيار بين مرشحين (مهارة، خطة، أداة) اسأل الحكم بخيارات مغلقة ومعها «لا شيء»، مرتين بالتوازي والترتيب معكوس في الثانية؛ الاتفاق = حكم ثابت، الاختلاف = متوسط الترتيبين، غياب الحكم = الترتيب الحتمي، وسجّل decided_by. — Pick among candidates with a closed-set judge asked twice (options reversed) plus 'none'; agreement is stable, disagreement averages the rankings, an unavailable judge falls back to the deterministic ranking, and the reply says which path decided.

**متى:** عند اختيار مهارة أو خطة أو أداة من عدة مرشحين بحكم نموذج / when a model judge picks among several candidates

**كيف:** Validate the packet first: refuse approval questions about payment, deletion, publishing or sending; require non-empty evidence; redact keys, emails, phones and card numbers. Cache by packet digest. Report decided_by (stable / mean_ranking / deterministic) and a receipt per call. A judgement is an opinion, never permission (A2).

**المعاملات:** 2 calls, reversed order; 'none' always offered; cache 7 days

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** judge · حكم · stability · ثبات · closed set · خيارات مغلقة · jev · selection · اختيار · position bias · انحياز الترتيب

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-28` سجل الحادثة / Incident record: expected vs actual vs evidence (documented)
- `CHECK-29` قواعد الإصلاح الذاتي / Self-repair rules: retry once, narrower; never relax a safety gate (documented)
- `CHECK-31` امتحان مختوم قبل العمل / Exam sealed before the work (documented)
- `CHECK-32` خادم نموذج وهمي مسجِّل / Recording mock model server (documented)

### `CHECK-31` — امتحان مختوم قبل العمل / Exam sealed before the work

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** اكتب الامتحان قبل أن يبدأ المنفّذ، وأخفه عنه، واختمه ببصمات الملفات. — Write the exam before the builder starts, hide it, and seal it with file hashes.

**متى:** إعادة بناء أداة أو استنساخ سلوك أو أي ادعاء «مطابق للأصل» / rebuilding a tool, cloning behaviour, any 'matches the original' claim

**كيف:** python3 scripts/differential_exam.py seal EXAM --out seal.json before the work; verify-seal EXAM seal.json at grading time (exit 1 if any file changed, vanished or appeared). Keep the seal outside the exam folder. Card HX-01.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hidden test · sealed exam · sha256 · امتحان خفي · ختم · بصمة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/evals/test_differential_exam.py`

#### 7. قدرات قريبة في العائلة

- `CHECK-29` قواعد الإصلاح الذاتي / Self-repair rules: retry once, narrower; never relax a safety gate (documented)
- `CHECK-30` حَكَم مغلق الخيارات مرتين بترتيب معكوس / Closed-set judge asked twice with reversed options, a 'none' option and a declared fallback (documented)
- `CHECK-32` خادم نموذج وهمي مسجِّل / Recording mock model server (documented)
- `CHECK-33` قائمة سطح الملاحظة / Observable-surface checklist (documented)

### `CHECK-32` — خادم نموذج وهمي مسجِّل / Recording mock model server

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** لاختبار حزام وكيل لا نموذجه: خادم يرد من سيناريو مكتوب ويحفظ كل طلب يصله. — To test an agent harness, not its model: a server that answers from a script and saves every request it receives.

**متى:** اختبار CLI أو وكيل يتصل بواجهة نموذج / testing a CLI or agent that calls a model API

**كيف:** Script the model's replies per scenario (text, tool calls, server errors 500/401, bad JSON). Save every request body and headers to the scenario folder; save stdout, stderr, exit code and the workdir effects. Then compare runs with differential_exam.py. Card HX-02.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mock server · fake model · responses api · harness test · خادم وهمي · اختبار الحزام

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-30` حَكَم مغلق الخيارات مرتين بترتيب معكوس / Closed-set judge asked twice with reversed options, a 'none' option and a declared fallback (documented)
- `CHECK-31` امتحان مختوم قبل العمل / Exam sealed before the work (documented)
- `CHECK-33` قائمة سطح الملاحظة / Observable-surface checklist (documented)
- `CHECK-34` المصحّح يعطي 100% على نفسه أولًا / Scorer must score 100% on itself first (documented)

### `CHECK-33` — قائمة سطح الملاحظة / Observable-surface checklist

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** لكل سيناريو فحوص مسماة لكل ما يرسله البرنامج وما يفعله، لا حكم واحد. — Per scenario, named checks for everything the program sends and does, not one verdict.

**متى:** تصميم امتحان مقارنة / designing a comparison exam

**كيف:** Thirteen checks: request count, request shape, instructions, tools, environment context, user messages, tool results, file effects, final answer, JSON events, exit code, stderr errors, headers. Cover hard paths too: model matrix, stdin, -C, images, env/PATH, server errors, unknown tool, long output truncation, non-zero exit. Cards HX-03, HX-05.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** observable surface · checks · scenarios · error paths · فحوص · سيناريوهات · مسارات الخطأ

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-31` امتحان مختوم قبل العمل / Exam sealed before the work (documented)
- `CHECK-32` خادم نموذج وهمي مسجِّل / Recording mock model server (documented)
- `CHECK-34` المصحّح يعطي 100% على نفسه أولًا / Scorer must score 100% on itself first (documented)
- `CHECK-35` ملاحظات استرداد صادقة وخط أساس / Honest recovery notes and a measured baseline (documented)

### `CHECK-34` — المصحّح يعطي 100% على نفسه أولًا / Scorer must score 100% on itself first

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** لا تثق في المصحّح قبل أن يعطي الأصل ضد نفسه 100% بعد إخفاء القيم المتغيرة. — Do not trust a scorer until the reference against itself scores 100% after masking volatile values.

**متى:** قبل نشر أي نسبة مطابقة / before reporting any match percentage

**كيف:** python3 scripts/differential_exam.py self-check REF REF2 (two reference runs) — exits 1 and prints the remaining differences until ids, timestamps and paths are masked with --rule REGEX=>TOKEN, --root PATH or --skip-key KEY; then compare REF CAND [--min N]. In the test kit the reference first scored 84.5%/95.7% against itself. Card HX-04.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scorer validation · normalisation · self-check · differential testing · تحقق المصحّح · تطبيع · مقارنة تفاضلية

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/evals/test_differential_exam.py`

#### 7. قدرات قريبة في العائلة

- `CHECK-32` خادم نموذج وهمي مسجِّل / Recording mock model server (documented)
- `CHECK-33` قائمة سطح الملاحظة / Observable-surface checklist (documented)
- `CHECK-35` ملاحظات استرداد صادقة وخط أساس / Honest recovery notes and a measured baseline (documented)

### `CHECK-35` — ملاحظات استرداد صادقة وخط أساس / Honest recovery notes and a measured baseline

| الحقل | القيمة |
|---|---|
| العائلة | `verification-evals` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/verification-evals.md)) |
| المجموعة | الاختبارات والجودة والأمان (`quality`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** لكل ما استُرد: الأداة التي أظهرته وما تغيّر وما تُحقق منه وما بقي، مع رقم قبل ورقم بعد على الامتحان نفسه. — For every recovery: the tool call that showed it, what changed, what was verified, what is missing, plus before/after numbers on the same exam.

**متى:** تقرير هندسة عكسية أو استنساخ أو تحسين / reverse-engineering, cloning or improvement reports

**كيف:** Separate what came from the tool (e.g. REA reads) from what came from your own scripts. List what was not tested. When a tool chokes on a huge target, shrink the target (carve one section) and confirm bulk findings with tool reads. Report baseline vs upgrade (kit: 75.4% → 98.5% with REA mandatory). Cards HX-06…HX-08.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** honest notes · baseline · not tested · REA · ملاحظات صادقة · خط أساس · لم يُختبر

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:rea` ← npm ls rea أو وجود node_modules/rea
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CHECK-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `council` · `differential-exam` · `package-skill` · `prompt-pack` · `repo-validate` · `repo-verify-video`.
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

- `CHECK-33` قائمة سطح الملاحظة / Observable-surface checklist (documented)
- `CHECK-34` المصحّح يعطي 100% على نفسه أولًا / Scorer must score 100% on itself first (documented)

