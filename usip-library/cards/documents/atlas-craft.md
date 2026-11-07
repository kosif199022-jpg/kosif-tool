# `atlas-craft` — المستندات والكتابة (38 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/atlas-craft.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/documents.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`ACRAFT-01` مخطط أولي ومنظمات بصرية ملائمة](#acraft-01--مخطط-أولي-ومنظمات-بصرية-ملائمة--low-fi-wireframe-and-adhd-friendly-visual-organizers)
- [`ACRAFT-02` نظام ألوان يدعم الوصولية والوضع الداكن](#acraft-02--نظام-ألوان-يدعم-الوصولية-والوضع-الداكن--color-system-with-accessibility-and-dark-mode)
- [`ACRAFT-03` اختبار تحمل الواجهة للمحتوى المتطرف](#acraft-03--اختبار-تحمل-الواجهة-للمحتوى-المتطرف--content-stress-and-edge-case-ui-hardening)
- [`ACRAFT-04` تخطيط جشتالت: الشبكة والمحاذاة والتجميع](#acraft-04--تخطيط-جشتالت-الشبكة-والمحاذاة-والتجميع--gestalt-layout-grid-alignment-grouping)
- [`ACRAFT-05` تدقيق التسلسل البصري والمسافات](#acraft-05--تدقيق-التسلسل-البصري-والمسافات--refactoring-ui-hierarchy-and-spacing-audit)
- [`ACRAFT-06` تدقيق الضجيج البصري وإزالة الزخرفة](#acraft-06--تدقيق-الضجيج-البصري-وإزالة-الزخرفة--signal-to-noise-decoration-audit)
- [`ACRAFT-07` قواعد الخط والمقروئية للويب](#acraft-07--قواعد-الخط-والمقروئية-للويب--typography-and-legibility-rules-for-web)
- [`ACRAFT-08` بطاقة إخبارية مرسومة بأسلوب ثابت (موجّه صورة + SVG قابل للتعديل)](#acraft-08--بطاقة-إخبارية-مرسومة-بأسلوب-ثابت-موجّه-صورة--svg-قابل-للتعديل--fixed-style-doodle-card-news-image-prompt-plus-editable-svg-twin)
- [`ACRAFT-09` صفحات ويبتون بشخصية ثابتة وألوان باستيل](#acraft-09--صفحات-ويبتون-بشخصية-ثابتة-وألوان-باستيل--webtoon--essay-toon-pages-with-a-locked-character-sheet)
- [`ACRAFT-10` قصة مصورة وثائقية: مقابلة أولاً وجملة شخصية تُنسخ حرفياً](#acraft-10--قصة-مصورة-وثائقية-مقابلة-أولاً-وجملة-شخصية-تُنسخ-حرفياً--documentary-story-scenes-interview-first-verbatim-character-sentence)
- [`ACRAFT-11` رسم توضيحي للكتب بقوالب تخطيط ثابتة ونص محدد حرفياً](#acraft-11--رسم-توضيحي-للكتب-بقوالب-تخطيط-ثابتة-ونص-محدد-حرفياً--book-and-sketchbook-card-illustration-with-fixed-layout-templates)
- [`ACRAFT-12` مشهد قلم رصاص هادئ بلون واحد](#acraft-12--مشهد-قلم-رصاص-هادئ-بلون-واحد--quiet-pencil-scene-with-a-single-colour-accent)
- [`ACRAFT-13` رسومات مدونة سفر: مصغّرة وخريطة مسار ومشهد](#acraft-13--رسومات-مدونة-سفر-مصغّرة-وخريطة-مسار-ومشهد--travel-blog-illustration-kit-thumbnail-route-sketch-scene)
- [`ACRAFT-14` نظام بصري للكتاب: دليل فني ورسوم بالكود وحلقة رفض](#acraft-14--نظام-بصري-للكتاب-دليل-فني-ورسوم-بالكود-وحلقة-رفض--book-visual-system-art-bible-code-rendered-figures-art-director-loop)
- [`ACRAFT-15` تصميم الأيقونات بالتشابه والإغلاق البصري](#acraft-15--تصميم-الأيقونات-بالتشابه-والإغلاق-البصري--icon-design-by-resemblance-and-gestalt-closure)
- [`ACRAFT-16` نظام ألوان دلالي: درجات الحالة ودور واحد لكل لون](#acraft-16--نظام-ألوان-دلالي-درجات-الحالة-ودور-واحد-لكل-لون--semantic-colour-system-status-ramps-one-role-per-colour)
- [`ACRAFT-17` مقاييس الوضوح والقراءة: التباين والتباعد وطول السطر](#acraft-17--مقاييس-الوضوح-والقراءة-التباين-والتباعد-وطول-السطر--legibility-and-readability-numbers-contrast-spacing-measure)
- [`ACRAFT-18` التدرج الطباعي بسلم مقاسات](#acraft-18--التدرج-الطباعي-بسلم-مقاسات--typographic-hierarchy-from-a-modular-type-scale)
- [`ACRAFT-19` الأنماط الأصلية للعلامة والشخصية والتميمة](#acraft-19--الأنماط-الأصلية-للعلامة-والشخصية-والتميمة--brand-archetypes-for-voice-mascot-and-character-design)
- [`ACRAFT-20` رسم أيقونة التطبيق بالكود](#acraft-20--رسم-أيقونة-التطبيق-بالكود--app-icon-drawn-in-code-as-flat-layers)
- [`ACRAFT-21` تصميم واجهة غير قالبي وملف DESIGN.md](#acraft-21--تصميم-واجهة-غير-قالبي-وملف-designmd--anti-template-interface-design-and-a-designmd-north-star)
- [`ACRAFT-22` التفاعلات الدقيقة: المحفّز والقواعد والاستجابة والحلقات](#acraft-22--التفاعلات-الدقيقة-المحفّز-والقواعد-والاستجابة-والحلقات--microinteractions-trigger-rules-feedback-loops-and-modes)
- [`ACRAFT-23` شرح بصري بصيغة واحدة مناسبة للسؤال](#acraft-23--شرح-بصري-بصيغة-واحدة-مناسبة-للسؤال--visual-explanation-one-format-chosen-by-the-question)
- [`ACRAFT-24` الإفصاح التدريجي للمعلومات والأدوات](#acraft-24--الإفصاح-التدريجي-للمعلومات-والأدوات--progressive-disclosure-of-information-and-controls)
- [`ACRAFT-25` حوكمة البرومبتات في الإنتاج: سجل وتقييمات وترقية وتراجع](#acraft-25--حوكمة-البرومبتات-في-الإنتاج-سجل-وتقييمات-وترقية-وتراجع--prompt-governance-registry-evals-promotion-and-rollback)
- [`ACRAFT-26` استخراج أسلوب كاتب إلى دليل أسلوب قابل للتطبيق](#acraft-26--استخراج-أسلوب-كاتب-إلى-دليل-أسلوب-قابل-للتطبيق--extract-a-writing-style-into-a-reusable-style-guide)
- [`ACRAFT-27` طابق شكل التعليمة مع نوع الفشل واختبر الصياغة باختبارات دقيقة](#acraft-27--طابق-شكل-التعليمة-مع-نوع-الفشل-واختبر-الصياغة-باختبارات-دقيقة--match-the-instruction-form-to-the-failure-then-micro-test-the-wording)
- [`ACRAFT-28` صمّم شكل المهارة: نمط الاستدعاء وتصنيف الخطوات ومعيار الإنجاز وقسم المطبّات](#acraft-28--صمّم-شكل-المهارة-نمط-الاستدعاء-وتصنيف-الخطوات-ومعيار-الإنجاز-وقسم-المطبّات--design-a-skills-shape-invocation-mode-step-typing-completion-criteria-growing-gotchas)
- [`ACRAFT-29` أعد هيكلة مهارة كبيرة دون فقدان سلوكها: سجل الثوابت ومصدر واحد للحقيقة](#acraft-29--أعد-هيكلة-مهارة-كبيرة-دون-فقدان-سلوكها-سجل-الثوابت-ومصدر-واحد-للحقيقة--refactor-a-large-skill-without-losing-behaviour-invariant-ledger-single-source-of-truth-earned-labels)
- [`ACRAFT-30` حوّل جلسة ناجحة إلى مهارة سير عمل قابلة للإعادة](#acraft-30--حوّل-جلسة-ناجحة-إلى-مهارة-سير-عمل-قابلة-للإعادة--skillify-a-finished-session-into-a-reusable-workflow-skill)
- [`ACRAFT-31` ملف صوت المالك: قابل للقياس ومدعوم باقتباسات وينمو من تعديلاته](#acraft-31--ملف-صوت-المالك-قابل-للقياس-ومدعوم-باقتباسات-وينمو-من-تعديلاته--owner-voice-file-measurable-quote-backed-grows-from-edits)
- [`ACRAFT-32` إعادة كتابة على مستوى الخطاب مع قارئ بارد معزول](#acraft-32--إعادة-كتابة-على-مستوى-الخطاب-مع-قارئ-بارد-معزول--discourse-level-rewrite-with-an-isolated-cold-reader)
- [`ACRAFT-33` إصلاح الترجمة الحرفية في العربية بعد الترجمة أو التعريب](#acraft-33--إصلاح-الترجمة-الحرفية-في-العربية-بعد-الترجمة-أو-التعريب--arabic-translationese-repair-after-translation-or-localization)
- [`ACRAFT-34` بنك القصص: مقابلة تحفظ الأرقام ونقاط التحول والمواقف](#acraft-34--بنك-القصص-مقابلة-تحفظ-الأرقام-ونقاط-التحول-والمواقف--story-bank-interview-numbers-turning-points-positions)
- [`ACRAFT-35` من شرارة إلى فكرة قابلة للتصوير: احتمالات، لوجلاين، رهانات](#acraft-35--من-شرارة-إلى-فكرة-قابلة-للتصوير-احتمالات-لوجلاين-رهانات--from-spark-to-filmable-premise-what-ifs-logline-tests-stakes)
- [`ACRAFT-36` حرفة مشهد الحوار: نص فرعي، ادخل متأخرًا، فعل مرئي فقط](#acraft-36--حرفة-مشهد-الحوار-نص-فرعي-ادخل-متأخرًا-فعل-مرئي-فقط--dialogue-scene-craft-subtext-late-entry-visible-only-action)
- [`ACRAFT-37` من شذرات إلى سكريبت: استكشاف ثم استغلال](#acraft-37--من-شذرات-إلى-سكريبت-استكشاف-ثم-استغلال--from-fragments-to-a-script-explore-then-exploit)
- [`ACRAFT-38` مراجعة الكوبي في سبعة تمريرات مع إعادة التحقق](#acraft-38--مراجعة-الكوبي-في-سبعة-تمريرات-مع-إعادة-التحقق--seven-sweep-copy-review-with-revalidation)

## البطاقات / cards

### `ACRAFT-01` — مخطط أولي ومنظمات بصرية ملائمة / Low-fi wireframe and ADHD-friendly visual organizers

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إنتاج مخططات ASCII ومنظمات Mermaid مبسطة. — Produce ASCII or sketch wireframes and simple Mermaid organizers for focus.

**متى:** User wants screen wireframe, whiteboard sketch or task breakdown visual.

**كيف:** 1. Default to ASCII wireframe; hand-drawn HTML on request. 2. Keep few nodes, color-code, chunk steps. 3. Mermaid for timelines, flows, checklists. 4. Iterate sketch until recognized.

**المعاملات:** style

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** wireframe · sketch · adhd · نموذج

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4396-draft-wireframe`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1806-neurodivergent-visual-org/4844-neurodivergent-visual-org`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1995-hypotyposis/7163-sketch`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-02` نظام ألوان يدعم الوصولية والوضع الداكن / Color system with accessibility and dark mode (documented)
- `ACRAFT-03` اختبار تحمل الواجهة للمحتوى المتطرف / Content-stress and edge-case UI hardening (documented)

### `ACRAFT-02` — نظام ألوان يدعم الوصولية والوضع الداكن / Color system with accessibility and dark mode

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تصميم تدرجات ألوان للعلامة والحياد والحالات تحقق التباين في الوضعين الفاتح والداكن. — Design brand, neutral and status colour ramps that meet contrast needs in light and dark modes.

**متى:** Choosing a palette, status semantics, dark-mode, colour-blind support.

**كيف:** 1) Pick brand primary and a neutral ramp. 2) Define success/warning/error semantics with icon or text backup. 3) Check pairs against 4.5:1 text and 3:1 UI. 4) Re-derive dark mode rather than inverting. 5) Test with colour-blind simulation.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** color · contrast · ألوان · dark-mode

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3813-color`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3814-color-accessibility-and-mode`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-01` مخطط أولي ومنظمات بصرية ملائمة / Low-fi wireframe and ADHD-friendly visual organizers (documented)
- `ACRAFT-03` اختبار تحمل الواجهة للمحتوى المتطرف / Content-stress and edge-case UI hardening (documented)
- `ACRAFT-04` تخطيط جشتالت: الشبكة والمحاذاة والتجميع / Gestalt layout: grid, alignment, grouping (documented)

### `ACRAFT-03` — اختبار تحمل الواجهة للمحتوى المتطرف / Content-stress and edge-case UI hardening

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختبار الواجهة بأسماء طويلة وأرقام كبيرة وصور مفقودة ونصوص مترجمة. — Stress UI against long names, big numbers, missing images and localized strings.

**متى:** Before shipping components, i18n or RTL checks.

**كيف:** 1) List variable content slots. 2) Test extremes: long, empty, huge, multi-line. 3) Define truncation/wrap rules. 4) Provide image fallbacks. 5) Verify RTL and expanded translations.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** edge-cases · i18n · حالات حدية · components

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3847-factor-of-safety-content-stress`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-01` مخطط أولي ومنظمات بصرية ملائمة / Low-fi wireframe and ADHD-friendly visual organizers (documented)
- `ACRAFT-02` نظام ألوان يدعم الوصولية والوضع الداكن / Color system with accessibility and dark mode (documented)
- `ACRAFT-04` تخطيط جشتالت: الشبكة والمحاذاة والتجميع / Gestalt layout: grid, alignment, grouping (documented)
- `ACRAFT-05` تدقيق التسلسل البصري والمسافات / Refactoring-UI hierarchy and spacing audit (documented)

### `ACRAFT-04` — تخطيط جشتالت: الشبكة والمحاذاة والتجميع / Gestalt layout: grid, alignment, grouping

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تطبيق المحاذاة والشبكات والتقارب والتشابه لتنظيم التخطيط. — Apply alignment, grid systems, proximity and similarity so layouts read as organized groups.

**متى:** Layout review, form field grouping, picking columns/gutters/breakpoints.

**كيف:** 1) Align every element to shared edges. 2) Choose columns, gutters, breakpoints and a baseline grid. 3) Group by proximity: gap between groups larger than within. 4) Use similarity for same-function items. 5) Keep labels close to their fields.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** grid · alignment · شبكة · gestalt

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3807-alignment`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3808-alignment-grid-systems`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-02` نظام ألوان يدعم الوصولية والوضع الداكن / Color system with accessibility and dark mode (documented)
- `ACRAFT-03` اختبار تحمل الواجهة للمحتوى المتطرف / Content-stress and edge-case UI hardening (documented)
- `ACRAFT-05` تدقيق التسلسل البصري والمسافات / Refactoring-UI hierarchy and spacing audit (documented)
- `ACRAFT-06` تدقيق الضجيج البصري وإزالة الزخرفة / Signal-to-noise decoration audit (documented)

### `ACRAFT-05` — تدقيق التسلسل البصري والمسافات / Refactoring-UI hierarchy and spacing audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تدقيق واجهة من حيث التسلسل والمسافات واللون والعمق وتقييمها بقائمة فحص. — Audit a UI for hierarchy, spacing, color and depth and score it with a yes/no checklist.

**متى:** UI looks amateur, spacing/colour inconsistency, component styling review.

**كيف:** 1) Judge hierarchy in grayscale/blurred first. 2) Limit emphasis levers (size, weight, colour) to one or two per element. 3) Use spacing scale 4/8/16/24/32/48/64 with group gaps larger than inner gaps. 4) Cap text width at 45-75 chars. 5) Score = round(passed/8*10) from 8 checks. 6) Add colour and shadows last.

**المعاملات:** screenshot or code

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hierarchy · spacing · تسلسل بصري · ui-audit

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3438-ux-design/14122-refactoring-ui`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3840-snr-emphasis-economy`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-03` اختبار تحمل الواجهة للمحتوى المتطرف / Content-stress and edge-case UI hardening (documented)
- `ACRAFT-04` تخطيط جشتالت: الشبكة والمحاذاة والتجميع / Gestalt layout: grid, alignment, grouping (documented)
- `ACRAFT-06` تدقيق الضجيج البصري وإزالة الزخرفة / Signal-to-noise decoration audit (documented)
- `ACRAFT-07` قواعد الخط والمقروئية للويب / Typography and legibility rules for web (documented)

### `ACRAFT-06` — تدقيق الضجيج البصري وإزالة الزخرفة / Signal-to-noise decoration audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إزالة الزخرفة الزائدة وتوزيع التأكيد بحيث يكسب كل عنصر مكانه. — Remove or densify decoration and budget emphasis so each cue earns its place.

**متى:** Cluttered or sterile screens, deciding what to delete.

**كيف:** 1) List each decorative element. 2) Ask what information it carries; delete if none. 3) If too sparse, densify. 4) Allocate emphasis (colour, weight, size, motion) sparingly. 5) Re-check hierarchy.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** clutter · minimalism · ضجيج بصري · audit

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3838-snr-decoration-removal`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3744-wabi-sabi-restraint`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-04` تخطيط جشتالت: الشبكة والمحاذاة والتجميع / Gestalt layout: grid, alignment, grouping (documented)
- `ACRAFT-05` تدقيق التسلسل البصري والمسافات / Refactoring-UI hierarchy and spacing audit (documented)
- `ACRAFT-07` قواعد الخط والمقروئية للويب / Typography and legibility rules for web (documented)
- `ACRAFT-08` بطاقة إخبارية مرسومة بأسلوب ثابت (موجّه صورة + SVG قابل للتعديل) / Fixed-style doodle card-news: image prompt plus editable SVG twin (documented)

### `ACRAFT-07` — قواعد الخط والمقروئية للويب / Typography and legibility rules for web

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختيار الخطوط والأحجام والمقاييس وطول السطر لمقروئية أفضل. — Choose typefaces, sizes, scales and line lengths for legible web typography.

**متى:** Setting type scale, readability complaints, font pairing.

**كيف:** 1) Pick a modular type scale. 2) Body size at least 16px, line-height about 1.5. 3) Line length 45-75 characters. 4) Limit to 1-2 families and few weights. 5) Establish typographic hierarchy via size/weight contrast.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** typography · legibility · خطوط · web

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3438-ux-design/14126-web-typography`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3826-legibility-typeface-and-size`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-05` تدقيق التسلسل البصري والمسافات / Refactoring-UI hierarchy and spacing audit (documented)
- `ACRAFT-06` تدقيق الضجيج البصري وإزالة الزخرفة / Signal-to-noise decoration audit (documented)
- `ACRAFT-08` بطاقة إخبارية مرسومة بأسلوب ثابت (موجّه صورة + SVG قابل للتعديل) / Fixed-style doodle card-news: image prompt plus editable SVG twin (documented)
- `ACRAFT-09` صفحات ويبتون بشخصية ثابتة وألوان باستيل / Webtoon / essay-toon pages with a locked character sheet (documented)

### `ACRAFT-08` — بطاقة إخبارية مرسومة بأسلوب ثابت (موجّه صورة + SVG قابل للتعديل) / Fixed-style doodle card-news: image prompt plus editable SVG twin

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يرسم بطاقة شرح أو تحذير بأسلوب ثابت لا يتغير، ويسلّم موجّه صورة إنجليزياً وملف SVG بالنص نفسه لتعديله في Figma أو Canva. — Draws an explainer or warning card in one locked house style and ships two twins: an English image-model prompt and an SVG with the same text as editable layers.

**متى:** بطاقة إخبارية، كارد نيوز، بطاقة شرح مرسومة / card news, doodle explainer card, issue card

**كيف:** 1) Lock the style sheet before drawing: one ink colour (#1A1A1A-ish), two neutral fills, one background treatment (flat cream or a vertical grey gradient), and exactly ONE accent colour reserved for the single key object. 2) Lock the layout as ratios of the canvas: inset frame about 2%, drawing zone top 3-62%, headline block bottom-left from about 7% margin, or title 9-17% / body 24-38% / diagram 45-90% for explainer cards. 3) Text the user gave is used verbatim; a reference image only tells you the subject, never copy its composition. 4) Explainer rules: things removed, saved or not yet existing are drawn as dashed outlines; emphasis is 2-3 short radial strokes; causes left, results right; body line 2 starts with an arrow. 5) Output the prompt in one fenced block with every in-image string as reading exactly: "...", plus the SVG with <text> elements in an OFL handwriting font.

**المعاملات:** accent colour, layout ratios, headline lines

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** card news · doodle · SVG · بطاقة · رسم · كارد نيوز · illustration

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2417-akbun-draw-cartoon-b`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2416-akbun-draw-cardnews-cream`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-06` تدقيق الضجيج البصري وإزالة الزخرفة / Signal-to-noise decoration audit (documented)
- `ACRAFT-07` قواعد الخط والمقروئية للويب / Typography and legibility rules for web (documented)
- `ACRAFT-09` صفحات ويبتون بشخصية ثابتة وألوان باستيل / Webtoon / essay-toon pages with a locked character sheet (documented)
- `ACRAFT-10` قصة مصورة وثائقية: مقابلة أولاً وجملة شخصية تُنسخ حرفياً / Documentary story scenes: interview first, verbatim CHARACTER sentence (documented)

### `ACRAFT-09` — صفحات ويبتون بشخصية ثابتة وألوان باستيل / Webtoon / essay-toon pages with a locked character sheet

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحوّل قصة أو خاطرة إلى صفحات ويبتون عمودية بشخصية ثابتة الملامح، مع سيناريو صفحات وموجّه صورة لكل صفحة وطبقة نص SVG. — Turns a story or short essay into vertical webtoon pages with a fixed-look character, a page script, one image prompt per page and an SVG text layer.

**متى:** ويبتون، قصة مصورة، كوميك، رسم قصة / webtoon, comic page, essay toon, illustrated story

**كيف:** 1) Write the page script first (pages, panels, narration, dialogue) and show it when you invented the story. 2) Character sheet: protagonist and counterpart described once; crowd figures faceless. 3) Canvas 4:5 (1080x1350) or tall page; layout per page type: two contrasting scenes = two panels split by a slightly tilted divider; big emotion = one borderless panel on white; dialogue = upper bodies plus hand-drawn balloons. 4) Style lock: thin warm-grey wobbly line, transparent watercolour or flat fills, 3-4 colours per page, one warm accent, manga symbols (sweat drop, motion arcs) used sparingly. 5) Narration is calm and factual; the feeling lives in the picture and in at most one short inner-thought bubble (about 10 characters) per page. 6) Keep in-image text short (models misspell long lines) and duplicate it in the SVG so wrong letters can be covered.

**المعاملات:** panels per page, palette, narration voice

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** webtoon · comic · ويبتون · قصة مصورة · character · شخصية

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2424-akbun-draw-webtoon-c`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-07` قواعد الخط والمقروئية للويب / Typography and legibility rules for web (documented)
- `ACRAFT-08` بطاقة إخبارية مرسومة بأسلوب ثابت (موجّه صورة + SVG قابل للتعديل) / Fixed-style doodle card-news: image prompt plus editable SVG twin (documented)
- `ACRAFT-10` قصة مصورة وثائقية: مقابلة أولاً وجملة شخصية تُنسخ حرفياً / Documentary story scenes: interview first, verbatim CHARACTER sentence (documented)
- `ACRAFT-11` رسم توضيحي للكتب بقوالب تخطيط ثابتة ونص محدد حرفياً / Book and sketchbook-card illustration with fixed layout templates (documented)

### `ACRAFT-10` — قصة مصورة وثائقية: مقابلة أولاً وجملة شخصية تُنسخ حرفياً / Documentary story scenes: interview first, verbatim CHARACTER sentence

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يرسم قصة حقيقية مشهداً بمشهد دون اختراع أحداث: يسأل أولاً ثم يثبّت وصف كل شخصية في جملة تُنسخ في كل موجّه. — Illustrates a real story scene by scene without inventing events: asks first, then pins each character in one sentence copied into every prompt.

**متى:** قصة حقيقية مرسومة، مشاهد متتالية بنفس الشخصية / story illustration series, consistent character across scenes

**كيف:** 1) No material, no drawing: ask when/where, who, what happened (start, event, end), the mood and how many scenes. 2) At most 4 characters with distinct faces; everyone else is a faceless mid-grey silhouette (near) or light outline ghost (far). 3) Write one English CHARACTER sentence per lead (hair, hat, glasses, build, clothes) and paste it word for word into every scene where they appear, because the image model has no memory between prompts. 4) One scene = one message; emotion through body (raised arms, hunched posture); a big metaphor prop (mountain, seed, scale) can be the hero of a concept scene. 5) Deliver a scene table (number, caption, in-image text, composition) for approval, then one fenced prompt per scene with a DO NOT list (realistic render, flat vector, pure white, extra faces).

**المعاملات:** scene count, lead characters ≤4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** storyboard · character consistency · ثبات الشخصية · قصة · مشاهد

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2425-akbun-draw-webtoon-d`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2421-akbun-draw-storytellingimage`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-08` بطاقة إخبارية مرسومة بأسلوب ثابت (موجّه صورة + SVG قابل للتعديل) / Fixed-style doodle card-news: image prompt plus editable SVG twin (documented)
- `ACRAFT-09` صفحات ويبتون بشخصية ثابتة وألوان باستيل / Webtoon / essay-toon pages with a locked character sheet (documented)
- `ACRAFT-11` رسم توضيحي للكتب بقوالب تخطيط ثابتة ونص محدد حرفياً / Book and sketchbook-card illustration with fixed layout templates (documented)
- `ACRAFT-12` مشهد قلم رصاص هادئ بلون واحد / Quiet pencil scene with a single colour accent (documented)

### `ACRAFT-11` — رسم توضيحي للكتب بقوالب تخطيط ثابتة ونص محدد حرفياً / Book and sketchbook-card illustration with fixed layout templates

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختار قالب تخطيط من مجموعة ثابتة (شريط أيقونات، تكبير، مقارنة…) ويرسم بأسلوب رمادي بنقطة لون واحدة، مع تحديد كل نص داخل الصورة حرفاً بحرف. — Picks one of a small fixed set of layouts (icon strip, zoom-in, comparison...) and draws in monogray with one accent, spelling out every in-image string exactly.

**متى:** رسومات كتاب، رسم توضيحي لمفهوم، بطاقة سكتشبوك / book illustration, concept sketch card, explainer drawing

**كيف:** 1) Choose the layout from a fixed catalogue instead of free composition, and reuse its spacing numbers. 2) Palette: dark-grey ink line, flat greys, one orange (or teal) accent on 1-3 spots only. 3) Sketchbook card anatomy: optional index number top-left, UPPERCASE handwritten title, optional subtitle in brackets, short underline, 1-2 line description, 2-4 checklist items, then a pencil drawing in the lower two thirds inside a thin frame. 4) The scene carries mood, a bold geometric overlay carries the definition (dashed ellipse for orbit, arrows for movement, zoom circle for detail, frame-in-frame for composition). 5) Every in-image string is written as reading exactly: "..."; prompt in English, labels in the user's language, kept short.

**المعاملات:** layout id, accent spots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** book illustration · sketch · رسم توضيحي · سكتش · pencil

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2415-akbun-draw-book-illustration`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2420-akbun-draw-sketchbook-card`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-09` صفحات ويبتون بشخصية ثابتة وألوان باستيل / Webtoon / essay-toon pages with a locked character sheet (documented)
- `ACRAFT-10` قصة مصورة وثائقية: مقابلة أولاً وجملة شخصية تُنسخ حرفياً / Documentary story scenes: interview first, verbatim CHARACTER sentence (documented)
- `ACRAFT-12` مشهد قلم رصاص هادئ بلون واحد / Quiet pencil scene with a single colour accent (documented)
- `ACRAFT-13` رسومات مدونة سفر: مصغّرة وخريطة مسار ومشهد / Travel-blog illustration kit: thumbnail, route sketch, scene (documented)

### `ACRAFT-12` — مشهد قلم رصاص هادئ بلون واحد / Quiet pencil scene with a single colour accent

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يرسم لحظة ساكنة بقلم رصاص رمادي على ورق كريمي مع مساحة فارغة كبيرة ولون واحد فقط على قطعة صغيرة تحمل المعنى. — Draws one still moment in grey pencil on cream paper with large empty space and a single colour on one small meaningful prop.

**متى:** رسم هادئ بالقلم الرصاص، لوحة بسيطة حزينة أو تأملية / quiet pencil drawing, minimal contemplative illustration

**كيف:** 1) Pick the stillest moment of the input and reduce it to 1-3 subjects. 2) Put them small on a ground line in the lower part; leave the top two thirds and the space around them empty. 3) One subject sits off-centre; several are split left/right. 4) Give one small prop a teal (#2E7D8C-like) accent; everything else greyscale pencil. 5) People only from behind or in profile, no front faces or emotion symbols, no text in the image. 6) Fill only the <...> slots of a fixed prompt template; never edit the style words.

**المعاملات:** subjects 1-3, accent prop

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pencil · رصاص · minimal · هادئ · سكتش

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2419-akbun-draw-quiet-pencil`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-10` قصة مصورة وثائقية: مقابلة أولاً وجملة شخصية تُنسخ حرفياً / Documentary story scenes: interview first, verbatim CHARACTER sentence (documented)
- `ACRAFT-11` رسم توضيحي للكتب بقوالب تخطيط ثابتة ونص محدد حرفياً / Book and sketchbook-card illustration with fixed layout templates (documented)
- `ACRAFT-13` رسومات مدونة سفر: مصغّرة وخريطة مسار ومشهد / Travel-blog illustration kit: thumbnail, route sketch, scene (documented)
- `ACRAFT-14` نظام بصري للكتاب: دليل فني ورسوم بالكود وحلقة رفض / Book visual system: art bible, code-rendered figures, art-director loop (documented)

### `ACRAFT-13` — رسومات مدونة سفر: مصغّرة وخريطة مسار ومشهد / Travel-blog illustration kit: thumbnail, route sketch, scene

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يولّد مصغرة وخريطة مسار مبسطة ومشهداً لمقالة سفر بألوان محددة الأدوار، ولا يضيف جغرافيا لم ترد في النص. — Produces a thumbnail, a simplified route map and scene art for a travel post with role-coded colours, never adding geography the text did not give.

**متى:** صور مدونة سفر، خريطة رحلة مرسومة، غلاف مقال / travel blog thumbnail, illustrated route map

**كيف:** 1) Formats: thumbnail 1:1 (16:9 on request) with short title, route sketch 3:4 with numbers only, scene 4:3 with no text. 2) Colours by role: cream paper, grey confirmed paths, three route colours (leaf green, purple, orange), greens for trees, sky blue for water, ink for lines and letters; thumbnail background chosen by subject (forest teal, sea blue, old town brown, cafe magenta, market olive). 3) Paths are rough crayon strokes; props flat shapes with no outline; people only as 1-3 faceless silhouettes. 4) Keep at least 35% of the canvas empty; title height 8-12% of canvas, subtitle 40-50% of the title, safe margin 8%. 5) Places, order and connections come only from the input; without directions draw a top-to-bottom visit order, never invent roads, coastlines or walking times.

**المعاملات:** format, route count ≤3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** travel · map · thumbnail · خريطة · سفر · مصغرة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2422-akbun-draw-travel-blog`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-11` رسم توضيحي للكتب بقوالب تخطيط ثابتة ونص محدد حرفياً / Book and sketchbook-card illustration with fixed layout templates (documented)
- `ACRAFT-12` مشهد قلم رصاص هادئ بلون واحد / Quiet pencil scene with a single colour accent (documented)
- `ACRAFT-14` نظام بصري للكتاب: دليل فني ورسوم بالكود وحلقة رفض / Book visual system: art bible, code-rendered figures, art-director loop (documented)
- `ACRAFT-15` تصميم الأيقونات بالتشابه والإغلاق البصري / Icon design by resemblance and Gestalt closure (documented)

### `ACRAFT-14` — نظام بصري للكتاب: دليل فني ورسوم بالكود وحلقة رفض / Book visual system: art bible, code-rendered figures, art-director loop

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يضبط شكل كل صور الكتاب بدليل فني واحد، ويرسم المخططات والرسوم البيانية بالكود لا بنماذج التوليد، ويرفض الصور المخالفة ويعيدها. — Keeps every book image consistent through one art bible, renders diagrams and charts in code instead of diffusion, and rejects and regenerates off-spec images.

**متى:** صور كتاب، رسوم كتاب متسقة، مخططات للكتاب / book images, consistent illustrations for a book, figure plan

**كيف:** 1) Write art-bible.md once: look, palette, medium, composition rules, character and setting sheets. 2) Compile one structured image spec into each backend's prompt syntax rather than hand-writing prompts per model. 3) Diagrams, charts, technical drawings and map bases are never generated by diffusion: Mermaid / D2 / Graphviz to SVG, matplotlib or Vega-Lite from a data file. 4) Plan figures in the outline; the writer places references and captions while drafting. 5) A reviewer reads every generated image, scores it against the art bible and regenerates with a corrected prompt. 6) Pre-export check: dimensions, aspect, size, alt text, broken references, manifest coverage.

**المعاملات:** art bible, figure plan

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** book · art bible · كتاب · دليل فني · figures · diagram

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `graphviz` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:matplotlib` ← python3 -c "import matplotlib" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1376-velith/3231-book-visuals`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-12` مشهد قلم رصاص هادئ بلون واحد / Quiet pencil scene with a single colour accent (documented)
- `ACRAFT-13` رسومات مدونة سفر: مصغّرة وخريطة مسار ومشهد / Travel-blog illustration kit: thumbnail, route sketch, scene (documented)
- `ACRAFT-15` تصميم الأيقونات بالتشابه والإغلاق البصري / Icon design by resemblance and Gestalt closure (documented)
- `ACRAFT-16` نظام ألوان دلالي: درجات الحالة ودور واحد لكل لون / Semantic colour system: status ramps, one role per colour (documented)

### `ACRAFT-15` — تصميم الأيقونات بالتشابه والإغلاق البصري / Icon design by resemblance and Gestalt closure

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يصمم أيقونات تشبه ما تمثله أو تعتمد على إكمال العين للشكل الناقص، ويعرف متى يفشل التبسيط. — Designs icons that look like what they mean or let the eye complete a partial outline, and knows when simplification fails.

**متى:** تصميم أيقونة، أيقونات واضحة، شعار بمساحة سلبية / icon design, negative-space logo, partial-outline icon

**كيف:** 1) Use resemblance when the object has a stable, widely known look (camera, lock, folder); switch to a convention icon when the thing is abstract. 2) Distinguish near neighbours by one decisive feature (camera vs video: add the record dot or a film frame). 3) Closure: suggest the shape with a partial outline or negative space; the viewer completes it, which lowers visual weight. 4) Do not rely on closure when completion costs the user effort in high-stakes UI, or when the icon becomes so reduced it is ambiguous. 5) Test at the smallest real size and with people who have not seen the brief.

**المعاملات:** icon size, metaphor

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** icon · أيقونة · logo · شعار · gestalt · closure

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3761-iconic-resemblance`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3810-closure`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-13` رسومات مدونة سفر: مصغّرة وخريطة مسار ومشهد / Travel-blog illustration kit: thumbnail, route sketch, scene (documented)
- `ACRAFT-14` نظام بصري للكتاب: دليل فني ورسوم بالكود وحلقة رفض / Book visual system: art bible, code-rendered figures, art-director loop (documented)
- `ACRAFT-16` نظام ألوان دلالي: درجات الحالة ودور واحد لكل لون / Semantic colour system: status ramps, one role per colour (documented)
- `ACRAFT-17` مقاييس الوضوح والقراءة: التباين والتباعد وطول السطر / Legibility and readability numbers: contrast, spacing, measure (documented)

### `ACRAFT-16` — نظام ألوان دلالي: درجات الحالة ودور واحد لكل لون / Semantic colour system: status ramps, one role per colour

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني ألوان الحالة والفئات والعلامة التجارية بحيث يعني كل لون شيئاً واحداً فقط. — Builds status, category and brand colours so each colour means exactly one thing.

**متى:** ألوان الحالة، نظام ألوان، ألوان نجاح وخطأ / status colours, semantic palette, colour tokens

**كيف:** 1) Separate three encodings: status (success, warning, error, info), category (project tags, teams) and brand role (primary CTA, accent, light emphasis). 2) Give each status a ramp: 50 tinted background, 300 border or icon, 500 main use, 700 text on tint, 900 text on dark. 3) Rules: one colour per role; destructive red never used for marketing emphasis; category hues never reused as status. 4) Category palettes: 5-7 distinguishable hues at most, then add shape or label. 5) Never rely on hue alone; pair with icon or text and check contrast. 6) Document every colour and its role on one spec page.

**المعاملات:** ramp steps 50/300/500/700/900

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** colour · color · ألوان · palette · tokens · status

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3815-color-semantic-systems`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-14` نظام بصري للكتاب: دليل فني ورسوم بالكود وحلقة رفض / Book visual system: art bible, code-rendered figures, art-director loop (documented)
- `ACRAFT-15` تصميم الأيقونات بالتشابه والإغلاق البصري / Icon design by resemblance and Gestalt closure (documented)
- `ACRAFT-17` مقاييس الوضوح والقراءة: التباين والتباعد وطول السطر / Legibility and readability numbers: contrast, spacing, measure (documented)
- `ACRAFT-18` التدرج الطباعي بسلم مقاسات / Typographic hierarchy from a modular type scale (documented)

### `ACRAFT-17` — مقاييس الوضوح والقراءة: التباين والتباعد وطول السطر / Legibility and readability numbers: contrast, spacing, measure

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يضبط تباين النص وتباعد الحروف والأسطر وطول السطر بقيم مرجعية قابلة للقياس. — Sets text contrast, tracking, leading and line length to measurable reference values.

**متى:** النص غير مقروء، تباين، حجم الخط، تباعد الأسطر / text hard to read, contrast ratio, line height

**كيف:** 1) Contrast: 4.5:1 normal text, 3:1 large text (18pt or 14pt bold) and UI graphics, 7:1 for AAA or poor viewing; check with a contrast tool or axe/Lighthouse. 2) Measure: 45-75 characters per line for prose, about 66 ideal. 3) Leading: headings 1.1-1.3, body 1.5-1.7, UI labels 1.2-1.4. 4) Loosen tracking slightly on ALL-CAPS and small text, tighten large display type; avoid long all-caps navigation. 5) Paragraph spacing large enough to see chunks. 6) Legibility (each glyph) is not readability (sustained reading): a display face may pass one and fail the other.

**المعاملات:** contrast 4.5/3/7; measure 45-75; leading 1.5-1.7

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** contrast · تباين · readability · قراءة · typography · WCAG

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:axe` ← npm ls axe أو وجود node_modules/axe
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3832-readability`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3529-ui-design/14313-visual-design-foundations`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-15` تصميم الأيقونات بالتشابه والإغلاق البصري / Icon design by resemblance and Gestalt closure (documented)
- `ACRAFT-16` نظام ألوان دلالي: درجات الحالة ودور واحد لكل لون / Semantic colour system: status ramps, one role per colour (documented)
- `ACRAFT-18` التدرج الطباعي بسلم مقاسات / Typographic hierarchy from a modular type scale (documented)
- `ACRAFT-19` الأنماط الأصلية للعلامة والشخصية والتميمة / Brand archetypes for voice, mascot and character design (documented)

### `ACRAFT-18` — التدرج الطباعي بسلم مقاسات / Typographic hierarchy from a modular type scale

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني تسلسل العناوين والنص من سلم نسب ثابت ووزن الخط بدلاً من أحجام عشوائية. — Builds heading and body ranks from a fixed ratio scale plus weight instead of arbitrary sizes.

**متى:** عناوين غير واضحة، سلم خطوط، أحجام الخط / type scale, heading hierarchy, font sizes

**كيف:** 1) Pick one ratio for the product: 1.125 dense app UI, 1.2 gentle software UI, 1.25 general web default, 1.333 editorial, 1.414 print, 1.5 magazine, 1.618 hero/marketing. 2) Generate tokens display, h1-h4, body-lg, body, body-sm, caption, micro from it. 3) Use weight as the second axis and combine it with size (24px semibold reads higher than 24px regular). 4) In monochrome or one-colour palettes, hierarchy must come from size, weight and space alone. 5) Review: each rank must be distinguishable at a glance from its neighbours.

**المعاملات:** scale ratio

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** type scale · typography · خطوط · عناوين · hierarchy

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3823-hierarchy-typographic`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-16` نظام ألوان دلالي: درجات الحالة ودور واحد لكل لون / Semantic colour system: status ramps, one role per colour (documented)
- `ACRAFT-17` مقاييس الوضوح والقراءة: التباين والتباعد وطول السطر / Legibility and readability numbers: contrast, spacing, measure (documented)
- `ACRAFT-19` الأنماط الأصلية للعلامة والشخصية والتميمة / Brand archetypes for voice, mascot and character design (documented)
- `ACRAFT-20` رسم أيقونة التطبيق بالكود / App icon drawn in code as flat layers (documented)

### `ACRAFT-19` — الأنماط الأصلية للعلامة والشخصية والتميمة / Brand archetypes for voice, mascot and character design

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختار نمطاً أصلياً واحداً من اثني عشر (الحكيم، المستكشف، المهرّج…) ليوجّه صوت العلامة وتصميم الشخصية أو التميمة. — Chooses one of twelve archetypes (Sage, Explorer, Jester...) to steer brand voice and mascot or character design.

**متى:** تصميم شخصية للعلامة، تميمة، ماسكوت، هوية / mascot design, brand character, brand personality

**كيف:** 1) Name the core motivation first, then map to one archetype: Innocent (safety), Sage (truth), Explorer (freedom), Outlaw (disruption), Magician (transformation), Hero (mastery), Lover (intimacy), Jester (joy), Everyman (belonging), Caregiver, Creator, Ruler. 2) Derive shape language, colour, posture and voice from that motivation (Jester: round forms, bright accents, playful copy). 3) Keep one primary archetype, at most one secondary. 4) Test across cultures: reactions to archetypes vary, so validate with the actual audience.

**المعاملات:** primary archetype

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** archetype · mascot · ماسكوت · تميمة · brand · شخصية

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3730-archetypes`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-17` مقاييس الوضوح والقراءة: التباين والتباعد وطول السطر / Legibility and readability numbers: contrast, spacing, measure (documented)
- `ACRAFT-18` التدرج الطباعي بسلم مقاسات / Typographic hierarchy from a modular type scale (documented)
- `ACRAFT-20` رسم أيقونة التطبيق بالكود / App icon drawn in code as flat layers (documented)
- `ACRAFT-21` تصميم واجهة غير قالبي وملف DESIGN.md / Anti-template interface design and a DESIGN.md north star (documented)

### `ACRAFT-20` — رسم أيقونة التطبيق بالكود / App icon drawn in code as flat layers

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يرسم أيقونة التطبيق من 1-4 أشكال بسيطة بالكود، طبقة لكل شكل، ثم يقارنها بأيقونات النظام بكل المقاسات. — Draws the app icon from 1-4 simple shapes in code, one layer per shape, then previews it beside system icons at every size.

**متى:** أيقونة تطبيق، app icon، رسم أيقونة بالكود / app icon, draw icon in code, macOS icon

**كيف:** 1) Say what the app is in one object or scene users recognise. 2) Sketch it as 1-4 shapes on a grid; each shape becomes its own layer. 3) Choose a background gradient and 3-5 accents; dark or saturated fills make light shapes pop. 4) Canvas 1024x1024, keep the artwork in the middle ~60% (at ~78% it looks oversized), draw flat (solid or gentle two-stop gradient) and let the platform add the material. 5) Avoid motifs that read as the platform's own apps. 6) Render previews from 256 down to 16 pt beside system icons before shipping.

**المعاملات:** 1024 canvas, 60% art area

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** app icon · أيقونة · icon · SVG · logo

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1527-nativeapps/4178-macos-app-icons`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-18` التدرج الطباعي بسلم مقاسات / Typographic hierarchy from a modular type scale (documented)
- `ACRAFT-19` الأنماط الأصلية للعلامة والشخصية والتميمة / Brand archetypes for voice, mascot and character design (documented)
- `ACRAFT-21` تصميم واجهة غير قالبي وملف DESIGN.md / Anti-template interface design and a DESIGN.md north star (documented)
- `ACRAFT-22` التفاعلات الدقيقة: المحفّز والقواعد والاستجابة والحلقات / Microinteractions: trigger, rules, feedback, loops and modes (documented)

### `ACRAFT-21` — تصميم واجهة غير قالبي وملف DESIGN.md / Anti-template interface design and a DESIGN.md north star

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يتجنب الأشكال الافتراضية المكررة للواجهات، ويكتب ملف تصميم واحد واضح الرأي بالألوان والخطوط والتخطيط يرجع إليه البشر والنماذج. — Avoids the stock look of generated interfaces and writes one opinionated design file (palette, type, layout, principles) that people and models follow.

**متى:** تصميم موقع مميز، واجهة ليست مكررة، دليل تصميم / distinctive UI, design guide, avoid generic look

**كيف:** 1) Ground the design in the subject matter, not a template. 2) List and avoid default looks: cream + serif + terracotta, near-black + one acid accent, broadsheet hairlines, identical rounded SaaS cards with the same grey shadow, tracked ALL-CAPS eyebrows above every heading, meta strings joined by middle dots. 3) Plan, review against the brief, build, critique: palette as 4-6 named hex values, typefaces and roles, a layout concept compared in ASCII wireframes, then principles. 4) Capture it in DESIGN.md with a theme or north star, the why behind each rule and concrete tokens; hedging guides are ignored.

**المعاملات:** palette 4-6 hex

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** DESIGN.md · UI · واجهة · تصميم · frontend · design system

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1420-frontend-design-skills/3376-anthropic-frontend-design`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1530-webcraft/4189-design-guide-authoring`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-19` الأنماط الأصلية للعلامة والشخصية والتميمة / Brand archetypes for voice, mascot and character design (documented)
- `ACRAFT-20` رسم أيقونة التطبيق بالكود / App icon drawn in code as flat layers (documented)
- `ACRAFT-22` التفاعلات الدقيقة: المحفّز والقواعد والاستجابة والحلقات / Microinteractions: trigger, rules, feedback, loops and modes (documented)
- `ACRAFT-23` شرح بصري بصيغة واحدة مناسبة للسؤال / Visual explanation: one format chosen by the question (documented)

### `ACRAFT-22` — التفاعلات الدقيقة: المحفّز والقواعد والاستجابة والحلقات / Microinteractions: trigger, rules, feedback, loops and modes

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يصمم التفاصيل الصغيرة للأزرار والمفاتيح والتحميل ويقيّمها بثمانية بنود. — Designs the small details of toggles, buttons and loaders and scores them on eight rows.

**متى:** تفاعل زر، حركة صغيرة في الواجهة، micro interaction / microinteraction, button feedback, toggle animation

**كيف:** 1) Trigger: shows that it exists, what it does and its state; prominence matches stakes; gestures get a visible alternative; default/hover/active/disabled/loading states look different. 2) Rules: simple and predictable, constrain inputs instead of erroring. 3) Feedback under 100 ms, scaled to the event's importance (not uniform). 4) Loops and modes: define what repeats or expires, avoid hidden modes. 5) Score 9-10 when all eight rows pass, 5-6 for generic feel, ≤3 when feedback or triggers are missing.

**المعاملات:** feedback < 100 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** microinteraction · تفاعل · animation · UX · button

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3438-ux-design/14121-microinteractions`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-20` رسم أيقونة التطبيق بالكود / App icon drawn in code as flat layers (documented)
- `ACRAFT-21` تصميم واجهة غير قالبي وملف DESIGN.md / Anti-template interface design and a DESIGN.md north star (documented)
- `ACRAFT-23` شرح بصري بصيغة واحدة مناسبة للسؤال / Visual explanation: one format chosen by the question (documented)
- `ACRAFT-24` الإفصاح التدريجي للمعلومات والأدوات / Progressive disclosure of information and controls (documented)

### `ACRAFT-23` — شرح بصري بصيغة واحدة مناسبة للسؤال / Visual explanation: one format chosen by the question

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يجيب عن «وضّح لي» برسم واحد مناسب (شجرة استدعاء، مخطط Mermaid، فرق كود…) مبني فقط على ما ثبت. — Answers 'show me' with one fitting visual (call tree, Mermaid diagram, focused diff...) built only from verified facts.

**متى:** وضّح بالرسم، ارسم لي مخطط، اشرح بصرياً / show me, sketch it, visualize this flow

**كيف:** 1) Name the question the visual must answer. 2) Pick one format: pseudocode for logic and state transitions; indented call tree for runtime flow; shallow tree for ownership; Mermaid for actors and data flow; focused diff for a proposed change; HTML only when asked or previewable. 3) Extract only verified calls, files, states and actors. 4) One labelled visual next to the sentence it supports, plus one or two sentences of explanation. 5) Mark unknowns as unknown, never fill gaps with plausible architecture.

**المعاملات:** format

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** diagram · Mermaid · مخطط · شرح بصري · visualize

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2212-majestic-misc/8300-show-me`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-21` تصميم واجهة غير قالبي وملف DESIGN.md / Anti-template interface design and a DESIGN.md north star (documented)
- `ACRAFT-22` التفاعلات الدقيقة: المحفّز والقواعد والاستجابة والحلقات / Microinteractions: trigger, rules, feedback, loops and modes (documented)
- `ACRAFT-24` الإفصاح التدريجي للمعلومات والأدوات / Progressive disclosure of information and controls (documented)
- `ACRAFT-25` حوكمة البرومبتات في الإنتاج: سجل وتقييمات وترقية وتراجع / Prompt governance: registry, evals, promotion and rollback (documented)

### `ACRAFT-24` — الإفصاح التدريجي للمعلومات والأدوات / Progressive disclosure of information and controls

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يقسّم الواجهة أو الشرح إلى طبقات: ما يلزم للقرار الحالي أولاً، والباقي خلف خطوة واحدة. — Layers an interface or explanation: what the current decision needs first, the rest one step away.

**متى:** واجهة مزدحمة، إخفاء الخيارات المتقدمة / cluttered UI, advanced options, layered help

**كيف:** 1) Every visible element costs noticing, reading and evaluating. 2) Sort options by frequency and relevance; show the primary layer, tuck advanced ones behind one clear disclosure (expand, 'more', a second step). 3) Make the hidden layer discoverable and its trigger explicit. 4) Do not hide what most users need often, and do not nest more than two levels. 5) Same rule applies to documents and skills: summary first, references one level deep.

**المعاملات:** layers ≤2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** progressive disclosure · UX · تبسيط · واجهة · layers

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3768-progressive-disclosure`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-22` التفاعلات الدقيقة: المحفّز والقواعد والاستجابة والحلقات / Microinteractions: trigger, rules, feedback, loops and modes (documented)
- `ACRAFT-23` شرح بصري بصيغة واحدة مناسبة للسؤال / Visual explanation: one format chosen by the question (documented)
- `ACRAFT-25` حوكمة البرومبتات في الإنتاج: سجل وتقييمات وترقية وتراجع / Prompt governance: registry, evals, promotion and rollback (documented)
- `ACRAFT-26` استخراج أسلوب كاتب إلى دليل أسلوب قابل للتطبيق / Extract a writing style into a reusable style guide (documented)

### `ACRAFT-25` — حوكمة البرومبتات في الإنتاج: سجل وتقييمات وترقية وتراجع / Prompt governance: registry, evals, promotion and rollback

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يعامل البرومبتات ككود: سجل بإصدارات وترقية بين البيئات، مجموعة ذهبية وتقييمات آلية في CI، اختبار A/B مسبق التعريف، وتراجع بأمر واحد. — Treats prompts as code: a versioned registry with environment promotion, a golden set with automated evals in CI, pre-defined A/B tests and one-command rollback.

**متى:** برومبتات مكتوبة داخل الكود، تراجع جودة بعد تعديل برومبت، اختبار A/B لبرومبت / prompts hard-coded in app code, a prompt change regressed quality, prompt A/B tests

**كيف:** 1) Registry: prompts/<id>/vX.Y.Z.md plus registry.yaml with owner, model, status and who promoted when. 2) A golden dataset per prompt (20 examples minimum, 100+ for production) covering edge cases, reviewed by a domain expert and versioned with the prompt. 3) Pick eval type by task: exact match, contains, schema validation, embedding similarity, model-as-judge, human; set thresholds (e.g. 95% extraction, 100% schema). 4) Lifecycle: branch, develop, eval in CI, compare with production score, review diff plus scores, promote with approval, monitor 24-48 h, rollback. 5) A/B: stable hash assignment, metric and sample size fixed in advance, at least a week or 1,000 requests per arm. 6) Re-run evals on a schedule because model updates break prompts silently.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** prompt management · evals · regression · حوكمة البرومبت · تقييم · A/B test · registry

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/179-prompt-governance/548-prompt-governance`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-23` شرح بصري بصيغة واحدة مناسبة للسؤال / Visual explanation: one format chosen by the question (documented)
- `ACRAFT-24` الإفصاح التدريجي للمعلومات والأدوات / Progressive disclosure of information and controls (documented)
- `ACRAFT-26` استخراج أسلوب كاتب إلى دليل أسلوب قابل للتطبيق / Extract a writing style into a reusable style guide (documented)
- `ACRAFT-27` طابق شكل التعليمة مع نوع الفشل واختبر الصياغة باختبارات دقيقة / Match the instruction form to the failure, then micro-test the wording (documented)

### `ACRAFT-26` — استخراج أسلوب كاتب إلى دليل أسلوب قابل للتطبيق / Extract a writing style into a reusable style guide

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحلل نصًا مصدرًا عبر 17 بعدًا أسلوبيًا (و10 سردية للأدب) من عينات موزعة، وينتج دليلًا وبطاقة صوت وقائمة افعل/لا تفعل ومعيار تقييم. — Analyses a source text across 17 style dimensions (plus 10 narrative ones for fiction) from spread samples and produces a guide, a voice card, a do/don't list and a scoring rubric.

**متى:** 'حلل أسلوب هذا الكاتب'، صوت علامة تجارية، كتابة بأسلوب مرجع / analyse an author's voice, brand voice, write in the style of a reference

**كيف:** 1) Sample 5-7 points spread across the text (opening, 25-35%, middle, 65-75%, end), not one chapter. 2) Record patterns, not content, across tone, sentence and paragraph length, register, transitions, humour, directness, warmth, explanation order, openings, closings, punctuation, rhetorical moves, reader address, examples, references and how the style adapts to difficulty. 3) For fiction add plot architecture, time structure, character introduction, emotional conveyance, theme handling, revelation pacing and where the author departs from AI defaults. 4) Keep only features seen in several samples; never claim absent traits. 5) Deliver full guide (800-1500 words), voice card (~300), 20-30 do/don't items and a 1-5 rubric, each with 2-3 neutral passages rewritten in the style. 6) Never copy signature phrases as rules; describe the pattern they exemplify.

**المعاملات:** source text

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** writing style · voice · style guide · أسلوب الكتابة · صوت العلامة · rubric

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1268-style-extractor/2946-style-extractor`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-24` الإفصاح التدريجي للمعلومات والأدوات / Progressive disclosure of information and controls (documented)
- `ACRAFT-25` حوكمة البرومبتات في الإنتاج: سجل وتقييمات وترقية وتراجع / Prompt governance: registry, evals, promotion and rollback (documented)
- `ACRAFT-27` طابق شكل التعليمة مع نوع الفشل واختبر الصياغة باختبارات دقيقة / Match the instruction form to the failure, then micro-test the wording (documented)
- `ACRAFT-28` صمّم شكل المهارة: نمط الاستدعاء وتصنيف الخطوات ومعيار الإنجاز وقسم المطبّات / Design a skill's shape: invocation mode, step typing, completion criteria, growing gotchas (documented)

### `ACRAFT-27` — طابق شكل التعليمة مع نوع الفشل واختبر الصياغة باختبارات دقيقة / Match the instruction form to the failure, then micro-test the wording

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (Apache-2.0, MIT); nothing copied |

**ما هي:** قبل كتابة أي قاعدة في مهارة أو برومبت، صنّف الفشل الملاحظ واختر الشكل المناسب له (منع، وصفة، خانة إلزامية، شرط)، ثم اختبر الصياغة مقابل نسخة بلا توجيه. — Classify the observed failure, pick the instruction form that fixes that failure type, and micro-test the wording against a no-guidance control before shipping it.

**متى:** كتابة قاعدة في مهارة، البرومبت يتجاهل تعليمة، المخرج شكله غلط / writing a rule into a skill or prompt, a rule keeps being ignored, output has the wrong shape

**كيف:** 1) Run the task without the new guidance first; if the failure does not appear, write nothing. 2) Classify the failure: skips a known rule under pressure → short prohibition plus a table of the excuses seen and a red-flags list; right behaviour but wrong output shape → a positive recipe that states the parts of the output in order (prohibitions here make it worse); a required element is missing → a required slot in the template being filled; behaviour should depend on a condition → a conditional keyed to an observable fact ('if the brief exists, cite it'). 3) No nuance clauses ('don't X unless it matters') and no exemption clauses ('this limit doesn't apply to code'): they reopen negotiation or leak; restructure so the rule cannot reach the exempt part. 4) Give every rule its reason in one clause; reasons transfer to unseen cases where bare rules do not. 5) End a reference list with a non-exhaustive licence ('covers common cases; reason from the whys'), and mark any enumerated read-list as a floor, otherwise the list becomes the model's blind spot. 6) Prefer a strong pretrained word ('tight', 'red', 'relentless') over a restated triad; say the target behaviour positively and keep negatives only as hard guardrails. 7) Micro-test: one fresh context per sample, the real surrounding skill as context, a task that tempts the failure, 5+ samples per variant plus the no-guidance control; read every flagged hit by hand. 8) Variance is a metric: if 5 samples give 5 interpretations, tighten the form before adding words. 9) Calm craft register: threat/urgency language and ALL-CAPS drive corner-cutting. Failure modes go in the skill only after they really happened. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2679-superpowers/10268-writing-skills, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1457-aegis/3581-writing-skills, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14000-writing-great-skills, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3121-batterie/13382-skill-forge.

**المعاملات:** failure sample, candidate wordings, 5+ reps per arm

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** prompt wording · skill authoring · prohibition vs recipe · micro-test · negation · leading words · صياغة التعليمات · اختبار الصياغة · كتابة المهارات

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2679-superpowers/10268-writing-skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1457-aegis/3581-writing-skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14000-writing-great-skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3121-batterie/13382-skill-forge`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-25` حوكمة البرومبتات في الإنتاج: سجل وتقييمات وترقية وتراجع / Prompt governance: registry, evals, promotion and rollback (documented)
- `ACRAFT-26` استخراج أسلوب كاتب إلى دليل أسلوب قابل للتطبيق / Extract a writing style into a reusable style guide (documented)
- `ACRAFT-28` صمّم شكل المهارة: نمط الاستدعاء وتصنيف الخطوات ومعيار الإنجاز وقسم المطبّات / Design a skill's shape: invocation mode, step typing, completion criteria, growing gotchas (documented)
- `ACRAFT-29` أعد هيكلة مهارة كبيرة دون فقدان سلوكها: سجل الثوابت ومصدر واحد للحقيقة / Refactor a large skill without losing behaviour: invariant ledger, single source of truth, earned labels (documented)

### `ACRAFT-28` — صمّم شكل المهارة: نمط الاستدعاء وتصنيف الخطوات ومعيار الإنجاز وقسم المطبّات / Design a skill's shape: invocation mode, step typing, completion criteria, growing gotchas

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (MIT); nothing copied |

**ما هي:** قرارات بنية المهارة قبل كتابة نصها: من يستدعيها، أي خطوة كود وأيها استدلال وأيها قرار بشري، ومتى تُعتبر كل خطوة منتهية. — Structural decisions for a skill before writing prose: who invokes it, which steps are code vs model reasoning vs human decision, and a checkable done-condition per step.

**متى:** إنشاء مهارة جديدة أو تقسيم مهارة كبيرة / creating a new skill, splitting a big skill, a skill whose steps get rushed

**كيف:** 1) Pick one category per skill (reference, verification, data/analysis, automation, scaffolding, review, deploy, runbook, ops); a skill straddling several is confused. 2) Invocation: model-invoked only if the agent or another skill must reach it alone (its description is paid every turn); otherwise user-invoked with a one-line human description, and when manual skills multiply add one router skill. 3) Description = trigger condition with one phrase per distinct branch, the neighbour skill named in a NOT-for clause; never a workflow summary. 4) Type each step code / inference / hybrid / human; any output that must be byte-identical on rerun (tables, sorting, templates) goes to a script; every inference step states input, output and why code can't do it. 5) Who-does-what table plus explicit human confirmation points; never proceed on silence; missing values stay null, unreadable inputs go to a separate list. 6) Each step ends with a checkable, exhaustive completion criterion ('every modified file accounted for'); if the agent still rushes, split the later steps out so they are not in view. 7) Hub SKILL.md short; spokes one level deep, each link saying when to read it; inline what every branch needs, push behind pointers what only some branches use. 8) Start a Gotchas section and add one line every time Claude trips; it becomes the highest-signal part. 9) First-run setup in a config file (ask if missing); persistent state outside the skill folder; optional session-scoped hooks for guardrails. 10) Status labels honestly: needs-verification until behaviour was tested. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2462-playbooks/9547-skill-authoring, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2462-playbooks/9548-thariq-skills, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14000-writing-great-skills, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/114-discovery/299-writing-skills.

**المعاملات:** skill purpose, trigger examples

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** skill design · progressive disclosure · invocation · step typing · gotchas · تصميم المهارة · الإفصاح التدريجي · معيار الإنجاز

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2462-playbooks/9547-skill-authoring`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2462-playbooks/9548-thariq-skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14000-writing-great-skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/114-discovery/299-writing-skills`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-26` استخراج أسلوب كاتب إلى دليل أسلوب قابل للتطبيق / Extract a writing style into a reusable style guide (documented)
- `ACRAFT-27` طابق شكل التعليمة مع نوع الفشل واختبر الصياغة باختبارات دقيقة / Match the instruction form to the failure, then micro-test the wording (documented)
- `ACRAFT-29` أعد هيكلة مهارة كبيرة دون فقدان سلوكها: سجل الثوابت ومصدر واحد للحقيقة / Refactor a large skill without losing behaviour: invariant ledger, single source of truth, earned labels (documented)
- `ACRAFT-30` حوّل جلسة ناجحة إلى مهارة سير عمل قابلة للإعادة / Skillify a finished session into a reusable workflow skill (documented)

### `ACRAFT-29` — أعد هيكلة مهارة كبيرة دون فقدان سلوكها: سجل الثوابت ومصدر واحد للحقيقة / Refactor a large skill without losing behaviour: invariant ledger, single source of truth, earned labels

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (Apache-2.0, MIT); nothing copied |

**ما هي:** تقليص وتنظيم مهارة أو ملف تعليمات طويل مع حفظ المحفزات والقواعد الأمنية والبدائل، ودمج النصوص المكررة في مصدر واحد بقاعدة الثلاث. — Shrink and reorganise a long skill or instruction file while preserving triggers, safety rules and fallbacks, deduplicating repeated prose into one source only under the Rule of Three.

**متى:** المهارة طويلة ومكررة، قواعد متناقضة بين الملفات، تنظيف دوري للتعليمات / skill is long or repetitive, rules contradict across files, periodic instruction cleanup

**كيف:** 1) Baseline: lines, chars, approx tokens, trigger and no-trigger cases, and an invariant ledger (triggers, counter-triggers, safety/authorization rules, tool fallbacks, stop and honesty criteria, output contract), each marked confirmed/inferred/unknown. Snapshot the files first. 2) Findings by class with line refs: duplication, contradiction (core vs reference), unconditional reading, over-broad or narrow description, steps no requirement explains, internal inconsistencies (numbering, terms, stale refs). 3) Dedup: classify each file as DESCRIBE (owns the concept), USE (must cite it by exact heading) or EXPOSE (may restate for humans with a pointer); create a new shared file only at 3+ real instances found by your own grep; at 1–2 instances only trim-to-citation, normalize wording or name an owner. 4) A block moved out of the core takes its guard rules and required terms with it; pointers one level deep; no ../ or symlinks across components. 5) For test-verifiable fixes write failing assertions first, then edit, then green. 6) Three sequential reviews: contract & safety; selection & disclosure; metrics & portability; re-check each fix. 7) Re-measure on the same cases; size reduction never pays for a lost invariant or a lost trigger. 8) Close with only the labels earned: refactored, statically validated, behaviorally evaluated (only after paired runs). 9) For scheduled sweeps: one commit per file with a ledger of cuts; files from a rejected earlier sweep are skipped next time; never edit frontmatter or fenced code in a tightening pass. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2975-pwdev-skills/12576-skill-refactor, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2972-pwdev-power/12533-power-skill-refactor, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2434-docs-hygiene/9449-extract-ssot, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1547-plugin-creator/4290-shared-content-references.

**المعاملات:** target skill path, eval cases

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** skill refactor · single source of truth · rule of three · invariants · instruction tightening · إعادة هيكلة المهارة · إزالة التكرار · مصدر واحد للحقيقة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2975-pwdev-skills/12576-skill-refactor`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2972-pwdev-power/12533-power-skill-refactor`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2434-docs-hygiene/9449-extract-ssot`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1547-plugin-creator/4290-shared-content-references`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-27` طابق شكل التعليمة مع نوع الفشل واختبر الصياغة باختبارات دقيقة / Match the instruction form to the failure, then micro-test the wording (documented)
- `ACRAFT-28` صمّم شكل المهارة: نمط الاستدعاء وتصنيف الخطوات ومعيار الإنجاز وقسم المطبّات / Design a skill's shape: invocation mode, step typing, completion criteria, growing gotchas (documented)
- `ACRAFT-30` حوّل جلسة ناجحة إلى مهارة سير عمل قابلة للإعادة / Skillify a finished session into a reusable workflow skill (documented)
- `ACRAFT-31` ملف صوت المالك: قابل للقياس ومدعوم باقتباسات وينمو من تعديلاته / Owner voice file: measurable, quote-backed, grows from edits (documented)

### `ACRAFT-30` — حوّل جلسة ناجحة إلى مهارة سير عمل قابلة للإعادة / Skillify a finished session into a reusable workflow skill

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (Apache-2.0, MIT); nothing copied |

**ما هي:** بعد إنجاز عمل متكرر (مونتاج ريل، حزمة برومبتات)، استخرج خطواته ومدخلاته ومعايير نجاح كل خطوة وتصحيحات المستخدم إلى مهارة، أو إلى ذاكرة إن كان مجرد معلومة. — After a repeated job is done, capture its steps, inputs, per-step success criteria and the user's corrections as a skill — or as a memory note if it is only a fact.

**متى:** 'احفظ ده كمهارة'، 'إيه اللي اتعلمناه'، نفس الشغل اتكرر في أكثر من جلسة / 'save this as a skill', 'what did we learn', same workflow repeated across sessions

**كيف:** 1) Gate: a repeatable multi-step procedure with judgment calls → skill; a single cause→fix, gotcha or config fact → memory/one-line rule, not a skill (most learnings are memory). Must be reusable, non-trivial, specific and verified to have worked. 2) Evidence: prefer repeated occurrences across sessions (same instructions repeated, recurring corrections, near-misses of an existing skill) over one session; weak evidence → no recommendation; an existing skill that fits → update it. 3) Analyze before asking: inputs, ordered steps, artifacts each step hands on, where the user steered or corrected, tools and permissions used. 4) Interview briefly in rounds only as needed: name + trigger phrases; goal and success criteria; step list and inline vs forked execution; per non-obvious step what proves it is done and whether to pause for the user (irreversible actions, publishing, paid generation). 5) Write: every step gets a Success criteria line; optional Artifacts, Human checkpoint, Rules (from the user's corrections), parallel steps as 3a/3b; minimum tool permissions. 6) Show a plain confirmation card (name, trigger, inputs, output, checkpoints, acceptance checks) and the full file before saving. 7) Never overwrite an existing skill; diff it. Strip client data, paths with usernames and secrets. 8) Validate structure and run 5 should-trigger and 3 should-not-trigger prompts plus one real end-to-end run; report separately what is structurally valid vs proven by a run. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2585-system-prompt-skillify-current-session, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3285-claudeception/13796-claudeception, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2487-codex-operations/9651-find-skill-candidates, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1544-agentskill-kaizen/4235-kaizen-improvement.

**المعاملات:** session transcript or summary, target location

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** skillify · session to skill · continuous learning · workflow capture · memory vs skill · حفظ كمهارة · استخراج سير العمل · التعلم من الجلسة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2585-system-prompt-skillify-current-session`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3285-claudeception/13796-claudeception`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2487-codex-operations/9651-find-skill-candidates`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1544-agentskill-kaizen/4235-kaizen-improvement`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-28` صمّم شكل المهارة: نمط الاستدعاء وتصنيف الخطوات ومعيار الإنجاز وقسم المطبّات / Design a skill's shape: invocation mode, step typing, completion criteria, growing gotchas (documented)
- `ACRAFT-29` أعد هيكلة مهارة كبيرة دون فقدان سلوكها: سجل الثوابت ومصدر واحد للحقيقة / Refactor a large skill without losing behaviour: invariant ledger, single source of truth, earned labels (documented)
- `ACRAFT-31` ملف صوت المالك: قابل للقياس ومدعوم باقتباسات وينمو من تعديلاته / Owner voice file: measurable, quote-backed, grows from edits (documented)
- `ACRAFT-32` إعادة كتابة على مستوى الخطاب مع قارئ بارد معزول / Discourse-level rewrite with an isolated cold reader (documented)

### `ACRAFT-31` — ملف صوت المالك: قابل للقياس ومدعوم باقتباسات وينمو من تعديلاته / Owner voice file: measurable, quote-backed, grows from edits

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (MIT); nothing copied |

**ما هي:** ملف صوت قصير يصف كيف يكتب/يتكلم المالك بأرقام واقتباسات لا بصفات — Build a ≤150-line voice file from 3–5 of the owner's own pieces that every writing skill loads.

**متى:** اكتب بصوتي، الريل لازم يبقى بطريقتي، out/voice.md / write like me, my voice, voice profile, before any reel script

**كيف:** 1) Collect 3–5 of the owner's own pieces in the SAME genre but DIFFERENT topics (same-topic samples narrow the range and hurt); <3 → mark confidence: low; 0 → refuse. 2) Measure, don't describe: median sentence length and spread, shortest sentence, paragraph length, connector rate, concrete-anchor density, dialect markers (مش/هـ/اللي), digit system, dash/emoji rate. 3) Habits section: how he opens, gives examples, signals doubt, closes — each habit must quote one real line; no quote → drop the habit. 4) Never-say list: words/structures that appear 0 times in his samples but are common model defaults, each with his replacement (not just a ban). 5) 3–5 positive excerpts + 1 negative: the model's own default draft on the same topic with a line on what differs (contrastive example). 6) No personality adjectives (دافئ/حاد) — they are not checkable. 7) Use it as completion: continue his text rather than 'imitate his style'. 8) Update loop: after each session diff his edits against the draft; corrections that repeat become new never-say/habit lines with a dated log entry; do not rewrite the whole file. 9) If samples disagree strongly (e.g. caption vs voiceover), keep two profiles instead of averaging. 10) Only the owner's own voice (or a team he represents) — never a named third party. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3597-humanize/14430-voice-profile, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3034-linkedin-skills/13055-linkedin-humanizer, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2537-unslop/9835-unslop.

**المعاملات:** 3–5 samples; out/voice.md

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** voice profile · owner voice · ملف الصوت · أسلوب المالك · never-say list · few-shot completion

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3597-humanize/14430-voice-profile`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3034-linkedin-skills/13055-linkedin-humanizer`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2537-unslop/9835-unslop`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-29` أعد هيكلة مهارة كبيرة دون فقدان سلوكها: سجل الثوابت ومصدر واحد للحقيقة / Refactor a large skill without losing behaviour: invariant ledger, single source of truth, earned labels (documented)
- `ACRAFT-30` حوّل جلسة ناجحة إلى مهارة سير عمل قابلة للإعادة / Skillify a finished session into a reusable workflow skill (documented)
- `ACRAFT-32` إعادة كتابة على مستوى الخطاب مع قارئ بارد معزول / Discourse-level rewrite with an isolated cold reader (documented)
- `ACRAFT-33` إصلاح الترجمة الحرفية في العربية بعد الترجمة أو التعريب / Arabic translationese repair after translation or localization (documented)

### `ACRAFT-32` — إعادة كتابة على مستوى الخطاب مع قارئ بارد معزول / Discourse-level rewrite with an isolated cold reader

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (MIT); nothing copied |

**ما هي:** إصلاح ما يجعل القارئ يفقد الخيط رغم فهمه كل كلمة — Fix the thread, not the vocabulary: old→new flow, topic chain, emphasis position, lists that replace argument; judged by a fresh-context reader.

**متى:** النص مفهوم كلمة كلمة بس مش ماشي، القارئ بيتوه / reader loses the thread, reads like AI after word-level cleanup

**كيف:** 1) Three layers: words (WRITE-02/03 scans), syntax (nominalised shells like تم القيام بـ, participle tails, uniform length), discourse (this card). 2) Paragraph checks: first sentence = the paragraph's claim (reading first sentences alone must carry the piece); each sentence starts with something already known and puts the new item at the end; one key term reused, never rotated. 3) Document checks: the trigger/problem with a date or number opens, the decision appears within 3 paragraphs, no closing summary paragraph, delete-test (a paragraph whose removal loses nothing is a repeat), headings as claims not category names. 4) A list whose items depend on each other (premise, cause, trade-off) becomes prose with the relation words; scan-read genres (reports, README, reference) keep their skeleton — edit sentences only and diff heading levels, list item counts and table shapes before/after. 5) The only allowed information gain is digging out specifics already in the source; missing ones become [يحتاج تحقق: …]. 6) Certainty check: count hedges/commitments before and after; 'سوف' must not become 'قد' or vice versa. 7) Review in a separate agent that gets only the rewrite, the reader and the genre (never the source or the brief); it reports per paragraph: expected / got / where lost. 8) Max 2 rounds; still failing → deliver with the list of paragraphs that need the author to add content, not more polishing. 9) For key openings: draft 5 candidates, drop the most predictable one first (typicality bias), then choose. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3597-humanize/14428-humanize, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2218-majestic-writing/8391-copy-editor.

**المعاملات:** draft, reader, genre

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** discourse · cold reader · old-new · topic chain · قارئ بارد · تماسك النص · list replaces argument

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3597-humanize/14428-humanize`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2218-majestic-writing/8391-copy-editor`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-30` حوّل جلسة ناجحة إلى مهارة سير عمل قابلة للإعادة / Skillify a finished session into a reusable workflow skill (documented)
- `ACRAFT-31` ملف صوت المالك: قابل للقياس ومدعوم باقتباسات وينمو من تعديلاته / Owner voice file: measurable, quote-backed, grows from edits (documented)
- `ACRAFT-33` إصلاح الترجمة الحرفية في العربية بعد الترجمة أو التعريب / Arabic translationese repair after translation or localization (documented)
- `ACRAFT-34` بنك القصص: مقابلة تحفظ الأرقام ونقاط التحول والمواقف / Story bank interview: numbers, turning points, positions (documented)

### `ACRAFT-33` — إصلاح الترجمة الحرفية في العربية بعد الترجمة أو التعريب / Arabic translationese repair after translation or localization

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (Apache-2.0, MIT); nothing copied |

**ما هي:** تنعيم نص عربي مترجم دون تغيير معناه أو سجله — Post-edit translated Arabic (scripts, subtitles, UI strings) to remove calques while locking facts, modality and register.

**متى:** النص مترجم وباين، ترجمة حرفية، تعريب واجهة، ترجمة سكريبت أو ترجمة / translationese, calques, localize UI, translated subtitles

**كيف:** 1) Translate first, naturalize second; never do both in one pass. For long sources: pin a glossary (key terms, chapter/section titles, names) before translating, translate per section, sanity-check length ratio per section, and read one finished section against the source before running the rest. 2) Mask protected spans byte-for-byte: numbers, dates, URLs, code, names, placeholders like {count}, quotes. 3) Calque families to fix: يلعب دورًا/يعتبر بمثابة → plain verb; من خلال/عن طريق chains; تمّ + مصدر → named actor; بالإضافة إلى ذلك/علاوة على ذلك at every paragraph; human adverbs on programs (بصمت، بشفافية، بأناقة) → say what actually happens; English word order (adjective chains, sentence-final 'حيث'); English punctuation (, ? ; and em dashes). 4) Lock modality: must stays يجب, may stays قد; conditions, negations, order unchanged. 5) Keep register (MSA vs Egyptian) and one spelling/digit convention; do not convert. 6) Edit budget: character change ≲30% normal, 30–50% re-verify every claim, >50% stop — you are rewriting, not naturalizing. 7) UI-string mode suspends the budget: labels become noun phrases, short and uniform within one screen; but never add a behavior or warning the source did not state; unknown term → flag, leave as is. 8) Arabic plural/gender: ICU needs zero/one/two/few/many/other; check every category reads naturally. 9) Optional: keep a per-owner rules file (signal, exception, rewrite) that grows from his corrections; apply only when context matches. 10) Report: final text, then only 'needs check' items. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/880-superloopy/1935-humanize-korean, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1101-akbun-writing/2489-akbun-writing-naturalize, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3549-xm/14339-humanize, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3193-ru-text/13542-ru-text.

**المعاملات:** source+target, glossary

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** translationese · ترجمة حرفية · calque · تعريب · localization · UI strings · subtitles translation

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/880-superloopy/1935-humanize-korean`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1101-akbun-writing/2489-akbun-writing-naturalize`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3549-xm/14339-humanize`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3193-ru-text/13542-ru-text`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-31` ملف صوت المالك: قابل للقياس ومدعوم باقتباسات وينمو من تعديلاته / Owner voice file: measurable, quote-backed, grows from edits (documented)
- `ACRAFT-32` إعادة كتابة على مستوى الخطاب مع قارئ بارد معزول / Discourse-level rewrite with an isolated cold reader (documented)
- `ACRAFT-34` بنك القصص: مقابلة تحفظ الأرقام ونقاط التحول والمواقف / Story bank interview: numbers, turning points, positions (documented)
- `ACRAFT-35` من شرارة إلى فكرة قابلة للتصوير: احتمالات، لوجلاين، رهانات / From spark to filmable premise: what-ifs, logline tests, stakes (documented)

### `ACRAFT-34` — بنك القصص: مقابلة تحفظ الأرقام ونقاط التحول والمواقف / Story bank interview: numbers, turning points, positions

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (MIT); nothing copied |

**ما هي:** مقابلة مرة واحدة تملأ ملفًا دائمًا بالمادة الحقيقية للمحتوى — One structured interview fills a persistent story bank so hooks never need invented facts.

**متى:** مش لاقي أقول إيه، اعملي مقابلة، الفكرة رفيعة / interview me, I have nothing to post, thin idea, the one true thing

**كيف:** 1) Read the bank first; ask only thin sections — never re-ask. 2) Open wide with one question and follow what he gets animated about; one question at a time. 3) Press every soft answer exactly once: 'improved' → by how much, over what period; 'a while ago' → which month; 'a big client' → can it be named. 4) Chase the reversal: what he believed a year ago and no longer does, and what it cost. 5) Find the position: what he thinks is true that peers dispute, and the cost of holding it. 6) Collect the 3 stories he already tells in person (pre-tested). 7) Settle naming limits explicitly; 'rather not say' is recorded as off-limits forever. 8) Write verbatim phrasing where vivid, date the file, list thin sections; leave unknown numbers empty, never inferred. 9) Mining a single story: return 3–5 genuinely distinct angles (lesson, contrarian, method, proof, relatable moment) plus 'not worth angling' (e.g. no proof angle until numbers are final); anonymize clients by default; openings start at the surprise/number, never chronology. 10) Post mode: moment not theme → number and date → what he got wrong → who disagrees → what viewer should do; read back a 5-line spine. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3034-linkedin-skills/13056-linkedin-interviewer, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4122-story-mine.

**المعاملات:** out/story-bank.md

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** story bank · interview · بنك القصص · مقابلة · angles · specifics · reel material

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3034-linkedin-skills/13056-linkedin-interviewer`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4122-story-mine`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-32` إعادة كتابة على مستوى الخطاب مع قارئ بارد معزول / Discourse-level rewrite with an isolated cold reader (documented)
- `ACRAFT-33` إصلاح الترجمة الحرفية في العربية بعد الترجمة أو التعريب / Arabic translationese repair after translation or localization (documented)
- `ACRAFT-35` من شرارة إلى فكرة قابلة للتصوير: احتمالات، لوجلاين، رهانات / From spark to filmable premise: what-ifs, logline tests, stakes (documented)
- `ACRAFT-36` حرفة مشهد الحوار: نص فرعي، ادخل متأخرًا، فعل مرئي فقط / Dialogue scene craft: subtext, late entry, visible-only action (documented)

### `ACRAFT-35` — من شرارة إلى فكرة قابلة للتصوير: احتمالات، لوجلاين، رهانات / From spark to filmable premise: what-ifs, logline tests, stakes

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (MIT); nothing copied |

**ما هي:** تحويل صورة أو إحساس إلى فرضية فيلم/ريل تحمل صراعًا — Turn a spark into a premise that can carry a short film or series before any boards.

**متى:** عندي فكرة فيلم، لو حصل كذا، هل الفكرة قوية / film idea, what if, is this premise strong, logline

**كيف:** 1) Record the spark in his words and classify it: image, what-if, character, setting, feeling; ask what drew him — that answer must survive later changes. 2) Generate 8–12 what-ifs by angle: invert it, raise the cost, move it in time or place, give it to the wrong person; flag which already imply conflict; he picks 1–3. 3) Logline = protagonist + want + obstacle + stakes. 4) Stress tests, each pass/weak/fail with one reason and one fix: active protagonist, opposition that can win, a choice at the end, personal stakes, situation that sustains the target length (5 s, 30 s, 3 min, series). 5) Stakes on three levels: external, relational, internal; at least two concrete. 6) Controlling idea + its counter-argument as working hypotheses. 7) For a contrarian angle: decompose into falsifiable claims, attack each; if objections reduce it to a tautology it is not an insight; refine to more precise wording, never retreat to weaker. 8) Hand a one-screen brief (title, logline, stakes, form, language/dialect) to STORY-01 intake. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2878-premise-workshop, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2630-hot-take-forge.

**المعاملات:** spark

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** premise · logline · what if · فكرة فيلم · stakes · رهانات · concept test

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2878-premise-workshop`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2630-hot-take-forge`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-33` إصلاح الترجمة الحرفية في العربية بعد الترجمة أو التعريب / Arabic translationese repair after translation or localization (documented)
- `ACRAFT-34` بنك القصص: مقابلة تحفظ الأرقام ونقاط التحول والمواقف / Story bank interview: numbers, turning points, positions (documented)
- `ACRAFT-36` حرفة مشهد الحوار: نص فرعي، ادخل متأخرًا، فعل مرئي فقط / Dialogue scene craft: subtext, late entry, visible-only action (documented)
- `ACRAFT-37` من شذرات إلى سكريبت: استكشاف ثم استغلال / From fragments to a script: explore, then exploit (documented)

### `ACRAFT-36` — حرفة مشهد الحوار: نص فرعي، ادخل متأخرًا، فعل مرئي فقط / Dialogue scene craft: subtext, late entry, visible-only action

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (Apache-2.0, MIT); nothing copied |

**ما هي:** قواعد كتابة مشاهد وحوار لفيلم قصير أو إعلان تمثيلي — Rules and model tells for scripted scenes with characters.

**متى:** سكريبت فيه حوار، مشهد بين شخصيتين، فيلم قصير، إعلان تمثيلي / dialogue scene, short film script, screenplay

**كيف:** 1) Every scene: someone wants something, something blocks it, the situation ends changed; outcomes yes-but / no-and / no-but; a clean yes kills tension. 2) Enter late, leave early: cut arrivals, greetings, goodbyes, and the summarizing last line. 3) Action lines in present tense, only what can be seen or heard, ≤3–4 lines; never 'she feels devastated'. 4) Subtext: characters talk around the thing; nobody answers the question directly; nobody explains what both know ('as you know…'). 5) Each character has a verbal signature (rhythm, words, what they never say, register/dialect fixed per pair — a shift is a story event); cover names and you should still know who speaks. 6) Monologues ≤5 lines; one physical reaction at most; withhold one thing per scene. 7) Model tells to scan: characters stating motive or theme, convenient coincidences, emotion on schedule, uniform scene length, final scene mirroring the first with one word changed, metaphors that explain themselves. 8) Timing: ~1 page ≈ 1 minute; for shorts one turn, no subplot. 9) Voiceover/audiobook version: add a pronunciation respelling list for names, and re-read for what fails aloud (visual-only jokes, tables, long untagged dialogue). Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1376-velith/3228-book-screenplay, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1376-velith/3218-book-fiction, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2869-adaptation.

**المعاملات:** scene list

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** dialogue · screenplay · subtext · حوار · سيناريو · مشهد · short film

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1376-velith/3228-book-screenplay`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1376-velith/3218-book-fiction`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2869-adaptation`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-34` بنك القصص: مقابلة تحفظ الأرقام ونقاط التحول والمواقف / Story bank interview: numbers, turning points, positions (documented)
- `ACRAFT-35` من شرارة إلى فكرة قابلة للتصوير: احتمالات، لوجلاين، رهانات / From spark to filmable premise: what-ifs, logline tests, stakes (documented)
- `ACRAFT-37` من شذرات إلى سكريبت: استكشاف ثم استغلال / From fragments to a script: explore, then exploit (documented)
- `ACRAFT-38` مراجعة الكوبي في سبعة تمريرات مع إعادة التحقق / Seven-sweep copy review with revalidation (documented)

### `ACRAFT-37` — من شذرات إلى سكريبت: استكشاف ثم استغلال / From fragments to a script: explore, then exploit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (MIT); nothing copied |

**ما هي:** جمع شذرات بلا ترتيب ثم بناء النص فقرة فقرة على مفاهيم مؤسسة — Separate idea-mining from shaping; build explainer scripts block by block on grounded concepts.

**متى:** عندي أفكار متفرقة، فويس أوفر شرح، حول ملاحظاتي لسكريبت / scattered notes to script, explainer voiceover

**كيف:** 1) Explore: append every fragment (sharp line, claim, vignette, half-thought, quote) to one file separated by ---; no structure; re-read the file before each write, never overwrite. 2) Hunt the leading word: one coinage or metaphor the whole piece can hang on — it later shapes title and transitions. 3) Exploit in a separate file: agree what the viewer already knows (prerequisites); keep a running list of grounded concepts. 4) Draft 2–3 openings, each implying a different thesis; he picks or merges. 5) Grow block by block: 'given this, what does the viewer need next?'; a block may lean only on grounded concepts — otherwise ground it first. 6) Pull from the pile as a quarry (split, merge, rework); if the pile lacks an example, say so: give one now or cut the section. 7) Ask per block: what does this do that the last didn't; if I cut it what breaks; is this one job or two. 8) For argument-heavy pieces check the pyramid: one-sentence governing answer, 2–4 non-overlapping supports, evidence matched to each, gaps labeled. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2224-mattpocock-skills/8433-writing-fragments, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2224-mattpocock-skills/8434-writing-shape, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2218-majestic-writing/8394-minto-pyramid.

**المعاملات:** notes file

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** fragments · explore exploit · leading word · grounding · سكريبت شرح · تنظيم الأفكار · minto

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `lean` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2224-mattpocock-skills/8433-writing-fragments`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2224-mattpocock-skills/8434-writing-shape`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2218-majestic-writing/8394-minto-pyramid`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-35` من شرارة إلى فكرة قابلة للتصوير: احتمالات، لوجلاين، رهانات / From spark to filmable premise: what-ifs, logline tests, stakes (documented)
- `ACRAFT-36` حرفة مشهد الحوار: نص فرعي، ادخل متأخرًا، فعل مرئي فقط / Dialogue scene craft: subtext, late entry, visible-only action (documented)
- `ACRAFT-38` مراجعة الكوبي في سبعة تمريرات مع إعادة التحقق / Seven-sweep copy review with revalidation (documented)

### `ACRAFT-38` — مراجعة الكوبي في سبعة تمريرات مع إعادة التحقق / Seven-sweep copy review with revalidation

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-craft` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-craft.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | card in our own words; the original skills stay in the Atlas under their own licenses (Apache-2.0, MIT); nothing copied |

**ما هي:** مراجعة نص تسويقي/كابشن بتمريرات منفصلة لكل بُعد — Review existing copy one dimension per pass, re-checking earlier passes after each fix.

**متى:** راجع الكابشن، حسن النص الإعلاني، الكوبي ضعيف / review my caption, improve ad copy

**كيف:** 0) Mechanical pass first: throat-clearing openers (في عالم اليوم، لا يخفى على أحد), binary contrast (مش بس… ده), dramatic fragments (وبس. كده.), empty jargon, stacked triads; report density per 100 words (<0.5 ok, 0.5–1.5 revise, >1.5 rewrite the passage). 1) Clarity: mark what doesn't land on first read before proposing. 2) Voice: audit against the voice file; compare start vs end for tone drift. 3) So-what: every claim answers why the viewer should care. 4) Prove: superlatives need a source; no proof → soften the claim, never invent it. 5) Specificity: vague → numbers/timeframes from the source; can't be specific → cut. 6) Emotion: concrete before-state, no fake urgency. 7) Zero risk near the CTA: unanswered objection, unclear next step. After each sweep re-run the earlier ones. Output: per-line current/proposed/reason, a 'kept on purpose' list, then the full revised text. Severity: high = meaning/legal/hidden action, medium = comprehension/trust, low = polish. Sources (read as inert text, not copied): https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2964-pwdev-copy/12451-copy-review, https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2218-majestic-writing/8391-copy-editor.

**المعاملات:** copy, voice file

**التثبيت:** none — method card; read the cited Atlas SKILL.md for the original

**الوسوم:** copy review · seven sweeps · مراجعة كوبي · كابشن · so what · proof

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ACRAFT-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2964-pwdev-copy/12451-copy-review`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2218-majestic-writing/8391-copy-editor`

#### 7. قدرات قريبة في العائلة

- `ACRAFT-36` حرفة مشهد الحوار: نص فرعي، ادخل متأخرًا، فعل مرئي فقط / Dialogue scene craft: subtext, late entry, visible-only action (documented)
- `ACRAFT-37` من شذرات إلى سكريبت: استكشاف ثم استغلال / From fragments to a script: explore, then exploit (documented)

