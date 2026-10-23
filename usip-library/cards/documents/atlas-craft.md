# `atlas-craft` — المستندات والكتابة (24 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/atlas-craft.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/documents.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

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

