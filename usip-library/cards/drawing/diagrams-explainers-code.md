# `diagrams-explainers-code` — الرسم والأشكال والتصميم (69 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/diagrams-explainers-code.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/drawing.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`EXPL-01` قواعد تركيب مخطط الشرح](#expl-01--قواعد-تركيب-مخطط-الشرح--explainer-diagram-composition)
- [`EXPL-02` قواعد العقد والروابط](#expl-02--قواعد-العقد-والروابط--node--edge-grammar)
- [`EXPL-03` اختيار نوع المخطط والتخطيط](#expl-03--اختيار-نوع-المخطط-والتخطيط--diagram-type--layout-chooser)
- [`EXPL-04` ترتيب البناء السببي وحالات العقد](#expl-04--ترتيب-البناء-السببي-وحالات-العقد--causal-build-order--node-states)
- [`EXPL-05` عكس المخطط للعربية](#expl-05--عكس-المخطط-للعربية--mirrored-rtl-diagrams)
- [`EXPL-06` ألوان دلالية للأدوار](#expl-06--ألوان-دلالية-للأدوار--semantic-role-colours)
- [`EXPL-07` إطار الشرح الأحادي](#expl-07--إطار-الشرح-الأحادي--learning-mono-explainer-frame)
- [`EXPL-08` حدود الأيقونات المختصرة](#expl-08--حدود-الأيقونات-المختصرة--closure-limits-for-minimal-icons)
- [`EXPL-09` توليد أيقونات بخلفية شفافة](#expl-09--توليد-أيقونات-بخلفية-شفافة--transparent-icon-generation)
- [`EXPL-10` مخططات SVG برمجية بالملليمتر](#expl-10--مخططات-svg-برمجية-بالملليمتر--programmatic-svg-schematics)
- [`EXPL-11` مخططات Mermaid من نص](#expl-11--مخططات-mermaid-من-نص--mermaid-text-to-diagram)
- [`EXPL-12` مخططات D2](#expl-12--مخططات-d2--d2-declarative-diagrams)
- [`EXPL-13` سبورة Excalidraw ولوحات JSON Canvas](#expl-13--سبورة-excalidraw-ولوحات-json-canvas--excalidraw--json-canvas-boards)
- [`EXPL-14` شبكة مفاهيم بقوة الجذب](#expl-14--شبكة-مفاهيم-بقوة-الجذب--force-directed-concept-graph)
- [`EXPL-15` خريطة الكيان في المنتصف](#expl-15--خريطة-الكيان-في-المنتصف--entity-node-map-with-flow-edges)
- [`EXPL-16` عملية من ثلاث خطوات](#expl-16--عملية-من-ثلاث-خطوات--three-step-process-recipe)
- [`EXPL-17` نبضة بيانات على الرابط](#expl-17--نبضة-بيانات-على-الرابط--data-pulse-along-edges)
- [`EXPL-18` خطوط تدفق متحركة](#expl-18--خطوط-تدفق-متحركة--marching-dash-flow-edges)
- [`EXPL-19` محور وأذرع ومدارات](#expl-19--محور-وأذرع-ومدارات--hub-and-spoke-constellations--orbits)
- [`EXPL-20` التفرع إلى عدة](#expl-20--التفرع-إلى-عدة--fan-out-branches--tree-cascades)
- [`EXPL-21` مخطط يُبنى مع الصوت](#expl-21--مخطط-يُبنى-مع-الصوت--voice-synced-diagram-build)
- [`EXPL-22` التكبير على مكوّن وقبل/بعد](#expl-22--التكبير-على-مكوّن-وقبلبعد--zoom-into-component--beforeafter-diagram)
- [`EXPL-23` الخط الزمني برأس تشغيل](#expl-23--الخط-الزمني-برأس-تشغيل--timeline-with-playhead)
- [`EXPL-24` مسار قرار ومخطط انسيابي](#expl-24--مسار-قرار-ومخطط-انسيابي--decision-path--flowchart)
- [`EXPL-25` دورة ورمز ينتقل](#expl-25--دورة-ورمز-ينتقل--cycle-diagram-travelling-token--loop-arrow)
- [`EXPL-26` شريط المراحل ومؤشر الخطوات](#expl-26--شريط-المراحل-ومؤشر-الخطوات--stage-tracker-pills--steppers)
- [`EXPL-27` خطأ ثم تصحيح](#expl-27--خطأ-ثم-تصحيح--mistake-then-correction)
- [`EXPL-28` مقارنة سرعة عادلة](#expl-28--مقارنة-سرعة-عادلة--fair-speed-comparison)
- [`EXPL-29` تسميات بخطوط قائدة](#expl-29--تسميات-بخطوط-قائدة--leader-line-callouts-2d--3d)
- [`EXPL-30` طبقات شفافة إيزومترية](#expl-30--طبقات-شفافة-إيزومترية--isometric-translucent-layer-stack)
- [`EXPL-31` التضخيم والمقارنة بالمقياس](#expl-31--التضخيم-والمقارنة-بالمقياس--exaggerated-scale--size-comparison)
- [`EXPL-32` طباعة الكود على الشاشة](#expl-32--طباعة-الكود-على-الشاشة--on-screen-code-typography)
- [`EXPL-33` كتابة بتذبذب مزروع](#expl-33--كتابة-بتذبذب-مزروع--seeded-typing-animation)
- [`EXPL-34` جلسة الطرفية](#expl-34--جلسة-الطرفية--terminal-session-scene)
- [`EXPL-35` إبراز السطر والتمرير والخطأ](#expl-35--إبراز-السطر-والتمرير-والخطأ--line-highlight-scroll--error-sweep)
- [`EXPL-36` كشف الفرق](#expl-36--كشف-الفرق--diff-reveal)
- [`EXPL-37` نافذة كود مشروحة](#expl-37--نافذة-كود-مشروحة--annotated-code-window-figure)
- [`EXPL-38` كود ومعاينة حية](#expl-38--كود-ومعاينة-حية--code--live-preview-split)
- [`EXPL-39` كود مجرد ورقائق](#expl-39--كود-مجرد-ورقائق--abstract-code-pills--token-chips)
- [`EXPL-40` كتل HyperFrames للكود](#expl-40--كتل-hyperframes-للكود--hyperframes-code-blocks)
- [`EXPL-41` من طلب دمج أو نص إلى فيديو شرح](#expl-41--من-طلب-دمج-أو-نص-إلى-فيديو-شرح--pr-to-video--faceless-explainer-pipelines)
- [`EXPL-42` حرّك ما يفعله الكود](#expl-42--حرّك-ما-يفعله-الكود--mechanism-beat-animate-behaviour-not-code)
- [`EXPL-43` شجرة ملفات تتحول إلى أعمدة](#expl-43--شجرة-ملفات-تتحول-إلى-أعمدة--folder-tree-to-bar-chart)
- [`EXPL-44` معادلة تتكون خطوة خطوة](#expl-44--معادلة-تتكون-خطوة-خطوة--equation-built-step-by-step-bidi-safe)
- [`EXPL-45` Manim للاشتقاق والنهايات](#expl-45--manim-للاشتقاق-والنهايات--manim-derivations--limits)
- [`EXPL-46` دوائر فورييه والجيب](#expl-46--دوائر-فورييه-والجيب--fourier-epicycles--unit-circle-sine)
- [`EXPL-47` برهان بصري بطيران الخلايا](#expl-47--برهان-بصري-بطيران-الخلايا--cell-flight-visual-proof)
- [`EXPL-48` شروح تعلم الآلة](#expl-48--شروح-تعلم-الآلة--ml-explainer-devices)
- [`EXPL-49` لوحة قياسات حية](#expl-49--لوحة-قياسات-حية--live-telemetry--math-hud)
- [`EXPL-50` التوأم الإنشائي: حلّال الجملونات](#expl-50--التوأم-الإنشائي-حلّال-الجملونات--structural-twin-truss-solver)
- [`EXPL-51` فيلم التوأم الإنشائي](#expl-51--فيلم-التوأم-الإنشائي--structural-twin-film-truss-on-a-character)
- [`EXPL-52` منظر تخطيطي ومفكك](#expl-52--منظر-تخطيطي-ومفكك--schematic-wireframe--exploded-view)
- [`EXPL-53` شرح علمي ثلاثي الأبعاد بأربع مراحل](#expl-53--شرح-علمي-ثلاثي-الأبعاد-بأربع-مراحل--four-stage-3d-science-explainer)
- [`EXPL-54` دورة الماء التعليمية المسطحة](#expl-54--دورة-الماء-التعليمية-المسطحة--flat-educational-water-cycle)
- [`EXPL-55` قواعد الدقة والوضوح للأطفال](#expl-55--قواعد-الدقة-والوضوح-للأطفال--science-accuracy--causal-step-rules)
- [`EXPL-56` نظام بطاقات الفيديو الشارح](#expl-56--نظام-بطاقات-الفيديو-الشارح--explainer-card-system)
- [`EXPL-57` الوثيقة المصدر وقلم التظليل](#expl-57--الوثيقة-المصدر-وقلم-التظليل--source-document--article-excerpt-overlay)
- [`EXPL-58` فئات المخططات والكود في بصمة](#expl-58--فئات-المخططات-والكود-في-بصمة--basma-diagram--code-film-categories)
- [`EXPL-59` رسومات استعارية لكل جملة](#expl-59--رسومات-استعارية-لكل-جملة--metaphor-graphic-per-spoken-claim)
- [`EXPL-60` بطاقات المقارنة والتشبيه والقوائم](#expl-60--بطاقات-المقارنة-والتشبيه-والقوائم--trade-off-analogy--checklist-cards)
- [`EXPL-61` أدوات بصرية للشرح](#expl-61--أدوات-بصرية-للشرح--explainer-visual-devices)
- [`EXPL-62` أسلوب الرسومات التقنية](#expl-62--أسلوب-الرسومات-التقنية--tech-blueprint-style)
- [`EXPL-63` لوحات ستوري بورد SVG مصغرة](#expl-63--لوحات-ستوري-بورد-svg-مصغرة--svg-thumbnail-storyboards)
- [`EXPL-64` نموذج مجرة الأدلة](#expl-64--نموذج-مجرة-الأدلة--evidence-galaxy-graph-model)
- [`EXPL-G01` قواعد مشهد الشرح الرياضي](#expl-g01--قواعد-مشهد-الشرح-الرياضي--explainer-scene-grammar)
- [`EXPL-G02` مخطط بنية سحابية بالكود ثم كشفه](#expl-g02--مخطط-بنية-سحابية-بالكود-ثم-كشفه--architecture-diagram-as-code-revealed-by-cluster)
- [`EXPL-U01` قائمة الأساليب الخمسة للموشن بالكود](#expl-u01--قائمة-الأساليب-الخمسة-للموشن-بالكود--five-code-rendered-motion-graphics-styles-menu)
- [`EXPL-U02` لقطة التحليل المجمّدة](#expl-u02--لقطة-التحليل-المجمّدة--frozen-analysis-beat-overlay)
- [`EXPL-X01` فيديو شرح بـManim](#expl-x01--فيديو-شرح-بـmanim--manim-explainer-workflow)

## البطاقات / cards

### `EXPL-01` — قواعد تركيب مخطط الشرح / Explainer diagram composition

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختزل النظام إلى 3–7 مكونات و5 خطوات كحد أقصى، باتجاه قراءة واحد وأقل تقاطعات، والأحمر للمشكلات فقط والأصفر لبطل واحد. / Reduce a system to 3–7 components and ≤5 steps, one reading direction, fewest crossings; red only for problems, one yellow hero.

**متى:** أي مخطط شرح / any explainer diagram.

**كيف:** ≤7 nodes visible at once (bigger systems in chapters with camera moves); density ~4/10 — more than ~9 nodes means two diagrams; circled step numbers only when order matters; neutral lines for normal flow; accent on ≤2 nodes; reuse one fixed layout JSON across scenes and animate only highlight changes; if a table says it better, use the table.

**المعاملات:** 3–7 nodes; ≤5 steps; ≤2 accents

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** diagram · composition · nodes · مخطط · قواعد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/diagrams.md:16`
- `kosif-atlas/skills/1098-akbun-presentation/2476-akbun-presentation-visual/SKILL.md`
- `kosif-atlas/skills/345-visuals/1242-html-diagram/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-02` قواعد العقد والروابط / Node & edge grammar (documented)
- `EXPL-03` اختيار نوع المخطط والتخطيط / Diagram type & layout chooser (documented)

### `EXPL-02` — قواعد العقد والروابط / Node & edge grammar

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عائلة أشكال واحدة وسماكة خط واحدة، روابط مستقيمة أو بانحناءة قائمة واحدة، والمنحنيات لحلقات الرجوع فقط. / One shape family, one stroke width, straight or one-bend orthogonal edges, curves only for feedback loops.

**متى:** رسم أي عقد وروابط / drawing any nodes and links.

**كيف:** radius 16–24 px; stroke 3–4 px; arrowheads 14–18 px (SVG marker orient="auto", refX near the tip, ~3–4× stroke); node labels 32–44 px, edge labels 24–28 px at 1080 width; right-angle rounded elbows, no diagonals; 6–10 px gap between an arrow label and its line; ≥12 px between attach points on one edge; no connector behind a non-endpoint box; 4 px grid; editorial palette paper #f5f5f5, ink #2d3142, muted #4f5d75, soft #7a8399, accent #eb6c36, link #2e5aa8.

**المعاملات:** stroke 3–4; heads 14–18; labels 32–44 / 24–28 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** nodes · edges · arrowheads · elbows · روابط · عقد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/diagrams.md:15`
- `kosif-atlas/skills/345-visuals/1242-html-diagram/references/svg-primitives.md`
- `kosif-atlas/skills/2657-figures/10114-svg-primitives`

#### 7. قدرات قريبة في العائلة

- `EXPL-01` قواعد تركيب مخطط الشرح / Explainer diagram composition (documented)
- `EXPL-03` اختيار نوع المخطط والتخطيط / Diagram type & layout chooser (documented)
- `EXPL-04` ترتيب البناء السببي وحالات العقد / Causal build order & node states (documented)

### `EXPL-03` — اختيار نوع المخطط والتخطيط / Diagram type & layout chooser

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثمانية أنواع تغطي معظم الشروح، ولكل بنية خوارزمية تخطيط تناسبها، والشكل نفسه يجب أن يحمل الحجة. / Eight types cover most explainers; each structure has its layout algorithm; shape carries the argument.

**متى:** أول قرار في أي شرح بصري / the first decision in any visual explanation.

**كيف:** branching decisions → flowchart; messages over time → sequence; components + links → architecture; dated events → timeline; parent–child → tree; cross-team handoffs → swimlane; two-axis positioning → quadrant; reinforcing cycle → loop; data → ER. Layouts: rooted trees → tidy tree (Reingold–Tilford/Buchheim); flows/state machines → layered Sugiyama (+ orthogonal routing for ports/ERDs); undirected networks → stress / Kamada–Kawai / Fruchterman–Reingold; distance from root → radial; cycles → circular; prefer stable layouts when animating revisions. Patterns: fan-out, convergence, cycle, assembly line chaos → order, side-by-side, gap (DRAW-43).

**المعاملات:** 8 types; ≤12 nodes in Mermaid

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** diagram type · flowchart · sequence · tree · layout algorithm · نوع المخطط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/345-visuals/1242-html-diagram/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10326-node-link-and-diagram-layout/references/algorithm-selection.md`
- `100-superskills/skills/diagrams-mermaid-architecture/SKILL.md:21`

#### 7. قدرات قريبة في العائلة

- `EXPL-01` قواعد تركيب مخطط الشرح / Explainer diagram composition (documented)
- `EXPL-02` قواعد العقد والروابط / Node & edge grammar (documented)
- `EXPL-04` ترتيب البناء السببي وحالات العقد / Causal build order & node states (documented)
- `EXPL-05` عكس المخطط للعربية / Mirrored RTL diagrams (documented)

### `EXPL-04` — ترتيب البناء السببي وحالات العقد / Causal build order & node states

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تظهر العقدة، يُرسم رابطها الخارج، وتقفز التالية حين يصلها القلم؛ النشطة بلون التأكيد، المزورة 70%، والمستقبلية غير مرسومة. / Node appears, outgoing edge draws, next node pops when the pen arrives; active accent, visited 70%, future not drawn.

**متى:** كل مخطط يُبنى أمام المشاهد / every diagram built on screen.

**كيف:** paint order background → connectors → boxes → labels (lines pass under shapes) in named <g> layers, animated in the same order; node stagger 0.08–0.15 s; reading order RTL for Arabic; front-load nothing — reveal each node on its spoken word (EXPL-21). The whiteboard-draw proof film (verified 13/13) builds a cause → effect diagram this way: sun and water drop, then two causal arrows, then the plant and the circled result.

**المعاملات:** stagger 0.08–0.15 s; visited 70%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** build order · causal · node states · ترتيب · active

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/diagrams.md:19`
- `kosif-tool/playbooks/diagrams.md:26`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md`
- `kosif-atlas/skills/2657-figures/10114-svg-primitives`

#### 7. قدرات قريبة في العائلة

- `EXPL-02` قواعد العقد والروابط / Node & edge grammar (documented)
- `EXPL-03` اختيار نوع المخطط والتخطيط / Diagram type & layout chooser (documented)
- `EXPL-05` عكس المخطط للعربية / Mirrored RTL diagrams (documented)
- `EXPL-06` ألوان دلالية للأدوار / Semantic role colours (documented)

### `EXPL-05` — عكس المخطط للعربية / Mirrored RTL diagrams

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** العقدة الأولى يمينًا والأسهم تشير يسارًا ورؤوسها معكوسة، والمعرفات اللاتينية معزولة. / First node on the right, arrows point left, mirrored markers, Latin ids isolated.

**متى:** كل مخطط بنص عربي / every diagram with Arabic labels.

**كيف:** mirror x positions (x' = W − x) or lay out with direction rtl; flip arrow marker paths; flows read right → left and top → bottom; Latin/code labels wrapped in dir="ltr" + unicode-bidi:isolate; stage-tracker pills ordered right → left (EXPL-26).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** RTL · mirrored · Arabic diagram · عكس · اتجاه

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/diagrams.md:18`
- `kosif-tool/playbooks/diagrams.md:71`

#### 7. قدرات قريبة في العائلة

- `EXPL-03` اختيار نوع المخطط والتخطيط / Diagram type & layout chooser (documented)
- `EXPL-04` ترتيب البناء السببي وحالات العقد / Causal build order & node states (documented)
- `EXPL-06` ألوان دلالية للأدوار / Semantic role colours (documented)
- `EXPL-07` إطار الشرح الأحادي / Learning-mono explainer frame (documented)

### `EXPL-06` — ألوان دلالية للأدوار / Semantic role colours

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | source folder declares WTFPL (copyleft-flagged in the atlas) — use the idea, not the files |

**ما هي:** اللون يرمّز نوع المكون، والمستطيلات المتقطعة تحدد الحدود. / Colour encodes component type; dashed rectangles mark boundaries.

**متى:** مخططات بنية تقنية / system architecture diagrams.

**كيف:** dark theme: frontend cyan #22d3ee, backend emerald #34d399, data violet #a78bfa, cloud amber #fbbf24, security rose #fb7185, message bus orange #fb923c, external slate #94a3b8; regions dashed 8,4 amber rx 12, security groups dashed 4,4; light/print theme via plain divs. Role colours (source / processing / storage / external) via Mermaid classDef with measured contrast. Ideas only from a copyleft-declared folder — re-author, do not copy files.

**المعاملات:** dash 8,4 / 4,4; rx 12

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** semantic colour · architecture · roles · ألوان دلالية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/x4919-visual-gen/x20317-architecture-diagram/SKILL.md`
- `100-superskills/skills/diagrams-mermaid-architecture/SKILL.md:24`

#### 7. قدرات قريبة في العائلة

- `EXPL-04` ترتيب البناء السببي وحالات العقد / Causal build order & node states (documented)
- `EXPL-05` عكس المخطط للعربية / Mirrored RTL diagrams (documented)
- `EXPL-07` إطار الشرح الأحادي / Learning-mono explainer frame (documented)
- `EXPL-08` حدود الأيقونات المختصرة / Closure limits for minimal icons (documented)

### `EXPL-07` — إطار الشرح الأحادي / Learning-mono explainer frame

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إطارات دراسة 16:9 بالأبيض والأسود: عنوان أعلى اليسار (يمين للعربية)، صناديق بخط 1–2 بكسل، أسهم رفيعة، ولون تأكيد أحمر واحد أقل من 5%. / Minimal black-and-white study frames with one red accent under 5%.

**متى:** دروس جادة وشروح أكاديمية / serious lessons.

**كيف:** white ground, title #111111 (≤40 chars), body #333333, annotations #767676, unfilled 1–2 px boxes, dashed grey grouping, thin arrows with small triangular heads and 2–4-word labels, accent #D93025 (second accent #1A73E8 only when needed), margins 5–7%, 3–5 points; build natively in SVG/HTML so text is exact; arrows and labels draw on with stagger; narration carries the long explanation.

**المعاملات:** accent < 5%; margin 5–7%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mono · minimal · study frame · أحادي اللون

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1094-akbun-draw/2418-akbun-draw-learning-mono/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-05` عكس المخطط للعربية / Mirrored RTL diagrams (documented)
- `EXPL-06` ألوان دلالية للأدوار / Semantic role colours (documented)
- `EXPL-08` حدود الأيقونات المختصرة / Closure limits for minimal icons (documented)
- `EXPL-09` توليد أيقونات بخلفية شفافة / Transparent icon generation (key)

### `EXPL-08` — حدود الأيقونات المختصرة / Closure limits for minimal icons

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأشكال الضمنية تتوقف عن العمل تحت 24 بكسل تقريبًا، وللجمهور المبتدئ وفي المعلومات الحساسة. / Implied shapes fail below ~24 px, for novices and in high-stakes info.

**متى:** أيقونات صغيرة في فيديو عمودي / small icons in vertical video.

**كيف:** pair minimal icons with labels, make critical marks explicit, render a contact sheet at the final 9:16 scale and inspect at phone size.

**المعاملات:** < ~24 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** icons · closure · legibility · أيقونات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1503-universal-design-principles/3811-closure-completion-cost/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-06` ألوان دلالية للأدوار / Semantic role colours (documented)
- `EXPL-07` إطار الشرح الأحادي / Learning-mono explainer frame (documented)
- `EXPL-09` توليد أيقونات بخلفية شفافة / Transparent icon generation (key)
- `EXPL-10` مخططات SVG برمجية بالملليمتر / Programmatic SVG schematics (documented)

### `EXPL-09` — توليد أيقونات بخلفية شفافة / Transparent icon generation

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أيقونات مسطحة بقناة ألفا للشروح، بلوحة ألوان مشتركة. / Flat alpha icons themed by a shared palette.

**متى:** حين لا توجد أيقونة SVG مناسبة / when no SVG icon fits.

**كيف:** request a transparent background from the image model (key needed) with a template 'a flat icon of a {item}', 1024 px square; if it returns opaque, remove near-white by threshold in Pillow or use rembg (BiRefNet, pip install rembg onnxruntime); prefer drawing simple icons as SVG strokes (DRAW-13) when possible.

**المعاملات:** 1024 px; threshold or BiRefNet

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** icons · transparent · rembg · توليد أيقونات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:onnxruntime` ← python3 -c "import onnxruntime" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:rembg` ← python3 -c "import rembg" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2657-figures/10115-transparent-icons`

#### 7. قدرات قريبة في العائلة

- `EXPL-07` إطار الشرح الأحادي / Learning-mono explainer frame (documented)
- `EXPL-08` حدود الأيقونات المختصرة / Closure limits for minimal icons (documented)
- `EXPL-10` مخططات SVG برمجية بالملليمتر / Programmatic SVG schematics (documented)
- `EXPL-11` مخططات Mermaid من نص / Mermaid text-to-diagram (install)

### `EXPL-10` — مخططات SVG برمجية بالملليمتر / Programmatic SVG schematics

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | BSD-3-Clause (atlas source) |

**ما هي:** صناديق تتسع لنصها، أسهم تلتصق بحافة الهدف ورأسها يتبع مماس المنحنى، ووحدات ملليمتر، وترتيب طبقات ثابت. / Auto-fit boxes, edge-snapped tangent-correct arrows, mm units and fixed layer order.

**متى:** مخططات دقيقة قابلة للطباعة والتحريك / precise schematics.

**كيف:** width/height in mm with an equal viewBox so coordinates and font-size are mm (font pt × 25.4/72, 7 pt = 2.47 mm); LabeledBox = measured text bbox + 2 mm padding (fontTools advances, or canvas measureText — browser measuring for Arabic shaping); Arrow.connect snaps to box edges, modes straight / cubic with perpendicular bow / orthogonal / waypoints, marker orient=auto; layers registered in paint order; save SVG (+ PNG via cairosvg); the same ideas are short to hand-write in JS for animation.

**المعاملات:** padding 2 mm; marker 3 mm; 7 pt

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** svg · schematic · auto-fit · arrows · mm · مخطط برمجي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:fonttools` ← python3 -c "import fonttools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2657-figures/10114-svg-primitives/SKILL.md`
- `kosif-atlas/skills/2657-figures/10113-svg-figure`

#### 7. قدرات قريبة في العائلة

- `EXPL-08` حدود الأيقونات المختصرة / Closure limits for minimal icons (documented)
- `EXPL-09` توليد أيقونات بخلفية شفافة / Transparent icon generation (key)
- `EXPL-11` مخططات Mermaid من نص / Mermaid text-to-diagram (install)
- `EXPL-12` مخططات D2 / D2 declarative diagrams (documented)

### `EXPL-11` — مخططات Mermaid من نص / Mermaid text-to-diagram

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مخططات انسيابية وتسلسلية وفئات وحالات وعلاقات وجانت من نص، والرندر نفسه يتحقق من الصياغة. / Flowchart, sequence, class, state, ER, Gantt from text; rendering validates syntax.

**متى:** مخطط سريع يُبنى من وصف / a quick diagram from a description.

**كيف:** mmdc -i x.mmd -o x.svg -t dark\|forest\|neutral -b transparent; one direction (TB or LR, RL for Arabic), ≤12 nodes, every arrow labelled, readable in B/W; then animate the SVG nodes in reading order (stagger opacity, draw-on edges with DRAW-01); fall back to hand SVG when mmdc is absent.

**المعاملات:** ≤12 nodes; themes default/dark/forest/neutral

**التثبيت:** npm i -g @mermaid-js/mermaid-cli

**الوسوم:** mermaid · text to diagram · flowchart · sequence

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1245-mermaid-cli/2925-mermaid-cli`
- `100-superskills/skills/diagrams-mermaid-architecture/SKILL.md:21`

#### 7. قدرات قريبة في العائلة

- `EXPL-09` توليد أيقونات بخلفية شفافة / Transparent icon generation (key)
- `EXPL-10` مخططات SVG برمجية بالملليمتر / Programmatic SVG schematics (documented)
- `EXPL-12` مخططات D2 / D2 declarative diagrams (documented)
- `EXPL-13` سبورة Excalidraw ولوحات JSON Canvas / Excalidraw & JSON Canvas boards (install)

### `EXPL-12` — مخططات D2 / D2 declarative diagrams

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لغة مخططات تصريحية بتخطيط dagre أو elk وسمات كثيرة، تخرج SVG وPNG وPDF وGIF متحرك. / Declarative diagrams with dagre/elk layouts and many themes.

**متى:** مخططات بنية كبيرة / large architecture diagrams.

**كيف:** d2 --theme N --layout elk in.d2 out.svg (tala layout is paid); the d2 binary is not installed here and its installer host is unverified — prefer Mermaid or hand SVG unless the user supplies d2.

**المعاملات:** layouts dagre / elk / tala (paid)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** d2 · declarative · elk · architecture

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2173-tools-plugin/7914-d2-diagrams`

#### 7. قدرات قريبة في العائلة

- `EXPL-10` مخططات SVG برمجية بالملليمتر / Programmatic SVG schematics (documented)
- `EXPL-11` مخططات Mermaid من نص / Mermaid text-to-diagram (install)
- `EXPL-13` سبورة Excalidraw ولوحات JSON Canvas / Excalidraw & JSON Canvas boards (install)
- `EXPL-14` شبكة مفاهيم بقوة الجذب / Force-directed concept graph (install)

### `EXPL-13` — سبورة Excalidraw ولوحات JSON Canvas / Excalidraw & JSON Canvas boards

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشاهد .excalidraw بأشكال وأسهم ونص حر بمظهر يدوي قابل للتحرير، ولوحات JSON Canvas مكانية تصلح مصدرًا لستوري بورد أو خريطة ذهنية. / Editable whiteboard scenes and spatial boards as storyboard sources.

**متى:** شرح بإحساس سبورة أو خريطة ذهنية / whiteboard-feel explainers, mind maps.

**كيف:** write elements per schema (rectangles, ellipses, diamonds, arrows, lines, text; roughness 1, fontFamily 1 hand / 3 mono); render through @excalidraw/excalidraw exportToSvg in headless Chromium, then draw strokes on (DRAW-01/27); large diagrams section by section. JSON Canvas: nodes {text\|file\|link\|group, x, y, width, height} and edges {fromSide, toSide, arrows} → a script turns them into animated SVG with camera moves.

**المعاملات:** roughness 1; fontFamily 1/3

**التثبيت:** npm i @excalidraw/excalidraw

**الوسوم:** excalidraw · json canvas · whiteboard · mind map

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2790-work/11181-draw-excalidraw`
- `kosif-atlas/skills/2966-pwdev-excalidraw/12488-excalidraw`
- `kosif-atlas/skills/3013-obsidian-second-brain/12869-json-canvas`

#### 7. قدرات قريبة في العائلة

- `EXPL-11` مخططات Mermaid من نص / Mermaid text-to-diagram (install)
- `EXPL-12` مخططات D2 / D2 declarative diagrams (documented)
- `EXPL-14` شبكة مفاهيم بقوة الجذب / Force-directed concept graph (install)
- `EXPL-15` خريطة الكيان في المنتصف / Entity node map with flow edges (ready)

### `EXPL-14` — شبكة مفاهيم بقوة الجذب / Force-directed concept graph

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مخطط ذهني (جذر، فروع، أبناء، ألوان) يُرسم كشبكة قوى تستقر متحركة. / A mind-map outline rendered as an animated force graph.

**متى:** خرائط معرفة، علاقات كثيرة / knowledge maps.

**كيف:** convert the JSON outline to nodes/links; run d3-force OFFLINE for N ticks (seeded) and store positions per tick, then animate nodes settling from the centre in branch order by indexing the stored ticks with t (never a live simulation during render); colour per top-level branch; depth ≤6.

**المعاملات:** depth ≤6; seeded ticks

**التثبيت:** npm i d3-force

**الوسوم:** force graph · d3-force · mind map · knowledge graph

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/30-learning/39-forcegraph-exporter/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10326-node-link-and-diagram-layout/references/algorithm-selection.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-12` مخططات D2 / D2 declarative diagrams (documented)
- `EXPL-13` سبورة Excalidraw ولوحات JSON Canvas / Excalidraw & JSON Canvas boards (install)
- `EXPL-15` خريطة الكيان في المنتصف / Entity node map with flow edges (ready)
- `EXPL-16` عملية من ثلاث خطوات / Three-step process recipe (documented)

### `EXPL-15` — خريطة الكيان في المنتصف / Entity node map with flow edges

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قالب يرسم كيانًا في المنتصف وما يغذيه من جهة وما ينتجه من الأخرى كعقد تحمل أرقامًا فوق شبكة نقاط، بخطوط تدفق متحركة. / An entity with inputs on one side and outputs on the other as number-carrying nodes over a dot grid.

**متى:** شرح نظام محاسبي أو عملية أعمال / business/process systems.

**كيف:** SK.studio.mount(root, spec) → {paint, focus, focused}; nodes 150 px × ≥80 px positioned translate(−50%, −50%), hover scale 1.025; edges as SVG lines classed in / draft / out / note; inputs dasharray 7 6 (warn colour), drafts 3 5 (violet), outputs solid; @keyframes flow to stroke-dashoffset −26 over 1.6 s linear; vector-effect non-scaling-stroke; dot grid radial-gradient 1 px every 24 px.

**المعاملات:** dash 7/6, 3/5; 1.6 s; grid 24 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** node map · entity · marching ants · flow · خريطة العقد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/components/studio.js`
- `kosif-earth-ci-fork/ui/components/studio.css:25`

#### 7. قدرات قريبة في العائلة

- `EXPL-13` سبورة Excalidraw ولوحات JSON Canvas / Excalidraw & JSON Canvas boards (install)
- `EXPL-14` شبكة مفاهيم بقوة الجذب / Force-directed concept graph (install)
- `EXPL-16` عملية من ثلاث خطوات / Three-step process recipe (documented)
- `EXPL-17` نبضة بيانات على الرابط / Data pulse along edges (documented)

### `EXPL-16` — عملية من ثلاث خطوات / Three-step process recipe

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سلسلة عقدة-رابط-عقدة مع خفوت السابق ونبضة بيانات ختامية. / Node-edge-node chain with dimming and a final data pulse.

**متى:** «كيف يعمل» في 4 ثوانٍ / 'how it works' in 4 s.

**كيف:** nodes pop at 0 / 900 / 1800 ms (scale .85 → 1, spring damping 14 stiffness 160, ~300 ms + 150 ms fade); edges draw 300–900 and 1200–1800 ms at 900–1200 px/s ease-in-out cubic with the arrowhead in the last 80 ms (DRAW-05); hold 2100–3600 ms with a data pulse; previous nodes dim to 70%.

**المعاملات:** 0/900/1800 ms; spring 14/160

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** process · three steps · node pop · recipe · خطوات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/diagrams.md:37`
- `kosif-tool/playbooks/diagrams.md:27`

#### 7. قدرات قريبة في العائلة

- `EXPL-14` شبكة مفاهيم بقوة الجذب / Force-directed concept graph (install)
- `EXPL-15` خريطة الكيان في المنتصف / Entity node map with flow edges (ready)
- `EXPL-17` نبضة بيانات على الرابط / Data pulse along edges (documented)
- `EXPL-18` خطوط تدفق متحركة / Marching-dash flow edges (ready)

### `EXPL-17` — نبضة بيانات على الرابط / Data pulse along edges

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة أو نقاط متوهجة تجري على مسار الرابط مرارًا أثناء وصف التدفق. / Dots travel the edge path repeatedly while the flow is described.

**متى:** تدفق بيانات، إشارة، طلب شبكة / data flow, signals, requests.

**كيف:** dot 10–14 px at getPointAtLength(p·L), 600–900 ms in-out, 400 ms gaps; variants: 3–5 glowing dots offset along a dashed quadratic arc (dash 4/6, r 4, ~1.5 s); orange dot on the active orthogonal wire with an orange ✗ on an invalid route (draw 500 ms, travel 800 ms); sine-wave segments scrolling 60 px/s between boxes for signal chains; glowing route to the chosen target (600 ms).

**المعاملات:** dot 10–14 px; 600–900 ms; gaps 400 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** data pulse · travelling dot · signal · flow · نبضة بيانات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/diagrams.md:29`
- `kosif-tool/styles/isometric`
- `kosif-tool/styles/plotter`
- `kosif-tool/styles/pm-blueoctopusai-dd17bd`

#### 7. قدرات قريبة في العائلة

- `EXPL-15` خريطة الكيان في المنتصف / Entity node map with flow edges (ready)
- `EXPL-16` عملية من ثلاث خطوات / Three-step process recipe (documented)
- `EXPL-18` خطوط تدفق متحركة / Marching-dash flow edges (ready)
- `EXPL-19` محور وأذرع ومدارات / Hub-and-spoke, constellations & orbits (install)

### `EXPL-18` — خطوط تدفق متحركة / Marching-dash flow edges

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرطات تسير على الخط لتبيّن التدفق: تيار، ماء، طاقة، بيانات. / Marching dashes show flow along a line.

**متى:** أنابيب، كهرباء، حرارة، طلبات / pipes, current, heat, requests.

**كيف:** MOTION.flowDash(tl, path, at, dur, {pattern:'28 22', cycles:6}) linear; seek-safe CSS/JS: dashoffset = −speed·t; water-cycle heat arrows #FF9E2C 7 px dasharray '20 18' dashoffset −140t with fade windows, sun rays rotating 18°/s and pulsing 1 + .06·sin(4πt); colour-code power / data / heat.

**المعاملات:** '28 22' × 6; '20 18' at −140 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** flowDash · marching ants · flow · dashes · تدفق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/motion-kit.js:247`
- `kosif-one/projects/water-cycle-animation/index.html`
- `kosif-earth-ci-fork/ui/components/studio.css:25`

#### 7. قدرات قريبة في العائلة

- `EXPL-16` عملية من ثلاث خطوات / Three-step process recipe (documented)
- `EXPL-17` نبضة بيانات على الرابط / Data pulse along edges (documented)
- `EXPL-19` محور وأذرع ومدارات / Hub-and-spoke, constellations & orbits (install)
- `EXPL-20` التفرع إلى عدة / Fan-out branches & tree cascades (seen)

### `EXPL-19` — محور وأذرع ومدارات / Hub-and-spoke, constellations & orbits

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كيان مركزي تُرسم منه خطوط إلى عقد حوله بالتتابع، أو بطاقات تتجمع على إهليلج، أو أقمار تستقر حول نواة. / A central hub drawing connectors to surrounding nodes, chips on an ellipse, satellites settling around a nucleus.

**متى:** تكاملات منتج، فريق، منظومة / product integrations, ecosystems.

**كيف:** lines draw from centre outward 300–600 ms with 50–150 ms stagger, then nodes fade in and count; hub glow blur 30–40 px; travelling dots on dashed spokes; gooey arms (6–7, stagger 80 ms); hero card centre with ~10 satellites on an ellipse and tag pills on the lines; reverse version: labels on a top arc stroke to the centre, then the hub logo pops with a ring. HyperFrames components: constellation-hub (nodes light in narration order), radial-surround (chips converge inward), locked-nucleus-orbit (3–6 satellites).

**المعاملات:** draw 300–600 ms; stagger 50–150 ms

**التثبيت:** npx hyperframes add constellation-hub

**الوسوم:** hub and spoke · integrations · constellation · orbit · محور

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/components/constellation-hub/constellation-hub.html`
- `kosif-one/vendor/hyperframes/registry/components/radial-surround/radial-surround.html`
- `kosif-tool/styles/pm-kmasiff-cc72cb`
- `kosif-tool/styles/pm-agonaliu-466a8f`

#### 7. قدرات قريبة في العائلة

- `EXPL-17` نبضة بيانات على الرابط / Data pulse along edges (documented)
- `EXPL-18` خطوط تدفق متحركة / Marching-dash flow edges (ready)
- `EXPL-20` التفرع إلى عدة / Fan-out branches & tree cascades (seen)
- `EXPL-21` مخطط يُبنى مع الصوت / Voice-synced diagram build (seen)

### `EXPL-20` — التفرع إلى عدة / Fan-out branches & tree cascades

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** منتج متوهج تتفرع منه منحنيات إلى منصات، أو حسابات تقفز من مركز، أو شجرة عقد متداخلة تظهر واحدة تلو الأخرى بروابط قائمة. / One-to-many curves, springing avatars, or nested tree cascades with elbow connectors.

**متى:** «من مكان واحد إلى كل مكان»، بنية ملفات / one-to-many stories, file/AST trees.

**كيف:** bezier curves draw 400–500 ms with 150 ms stagger to stacked cards, travelling light dots (700 ms) and signal-bar meters filling; N = 5 avatars spring out along straight lines (120 ms stagger, overshoot 1.1); AST cascade: indented boxed nodes (document > heading > paragraph > codeBlock) appear every 120 ms with elbow connectors and key:value mono metadata; hand-drawn branches from an address chip to N boxes (0.8 s each) with the focus box circled in yellow.

**المعاملات:** 400–500 ms; stagger 120–150 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** fan out · branches · tree · cascade · تفرع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-ceowinkz-7c776b`
- `kosif-tool/styles/pm-anthonyriera-9b1b2a`
- `kosif-tool/styles/pm-kyonax-on-tech-aabc1d`
- `kosif-tool/styles/pm-elliot-garreffa-f334bc`

#### 7. قدرات قريبة في العائلة

- `EXPL-18` خطوط تدفق متحركة / Marching-dash flow edges (ready)
- `EXPL-19` محور وأذرع ومدارات / Hub-and-spoke, constellations & orbits (install)
- `EXPL-21` مخطط يُبنى مع الصوت / Voice-synced diagram build (seen)
- `EXPL-22` التكبير على مكوّن وقبل/بعد / Zoom into component & before/after diagram (documented)

### `EXPL-21` — مخطط يُبنى مع الصوت / Voice-synced diagram build

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل سهم وأيقونة وتسمية يظهر ويُرسم عند الطابع الزمني لكلمته المنطوقة. / Each labelled arrow/icon draws at its word timestamp.

**متى:** شرح بتعليق صوتي / narrated explainers.

**كيف:** map each diagram element to a keyword in words.json (faster-whisper word timestamps); start its draw-on 60 ms before the word; never front-load more than ~25% (EASE-44); hold the full diagram for a final 1–2 s read.

**المعاملات:** word − 60 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** voice sync · words.json · narrated diagram · مزامنة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-sudo-kiran-6609ed`
- `kosif-tool/playbooks/audio-sync.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-19` محور وأذرع ومدارات / Hub-and-spoke, constellations & orbits (install)
- `EXPL-20` التفرع إلى عدة / Fan-out branches & tree cascades (seen)
- `EXPL-22` التكبير على مكوّن وقبل/بعد / Zoom into component & before/after diagram (documented)
- `EXPL-23` الخط الزمني برأس تشغيل / Timeline with playhead (documented)

### `EXPL-22` — التكبير على مكوّن وقبل/بعد / Zoom into component & before/after diagram

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثبات على النظام كله، الكاميرا تذهب لعقدة واحدة فتنفتح مخططًا فرعيًا؛ أو نسخة «بعد» تعيد رسم الروابط المتغيرة فقط بلون التأكيد. / Hold the system, camera to one node that opens into a sub-diagram; or redraw only the changed edges.

**متى:** أنظمة متداخلة، تحسينات / nested systems, improvements.

**كيف:** 2 s hold; scale 1.5 (zoom ≤1.8) in 900 ms then a 300 ms crossfade into the sub-diagram; camera pans 700–1000 ms cubic-bezier(.65,0,.35,1); before/after: duplicate the diagram and redraw only changed edges in the accent.

**المعاملات:** hold 2 s; ×1.5 / 900 ms; xfade 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** zoom · sub-diagram · before after · تكبير

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/diagrams.md:48`
- `kosif-tool/playbooks/diagrams.md:52`

#### 7. قدرات قريبة في العائلة

- `EXPL-20` التفرع إلى عدة / Fan-out branches & tree cascades (seen)
- `EXPL-21` مخطط يُبنى مع الصوت / Voice-synced diagram build (seen)
- `EXPL-23` الخط الزمني برأس تشغيل / Timeline with playhead (documented)
- `EXPL-24` مسار قرار ومخطط انسيابي / Decision path & flowchart (install)

### `EXPL-23` — الخط الزمني برأس تشغيل / Timeline with playhead

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رأس تشغيل بسرعة ثابتة، علامات تقفز عند وصوله والتسميات بعدها، وشريط الحقبة الحالية. / Constant-speed playhead; markers pop on arrival, labels after.

**متى:** تاريخ، سيرة، مراحل مشروع / history, biographies, project phases.

**كيف:** axis draws 600 ms; marker pop 200 ms; label +120 ms; current era band; one continuous lateral camera along the track slowing to 30% speed near dense clusters (cubic-bezier(.4,0,.2,1) per segment); milestone cards rise 400 ms / 40 px on a spring (damping 20) with a 1–1.5 s micro-animation; process timeline with doodle icons popping 200 ms back.out.

**المعاملات:** axis 600 / pop 200 / label +120 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** timeline · playhead · milestones · خط زمني

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/diagrams.md:31`
- `kosif-tool/styles/pm-kloss-xyz-fe0c31/BRIEF.md`
- `kosif-tool/styles/pm-lemomo-ai-0d9cff`

#### 7. قدرات قريبة في العائلة

- `EXPL-21` مخطط يُبنى مع الصوت / Voice-synced diagram build (seen)
- `EXPL-22` التكبير على مكوّن وقبل/بعد / Zoom into component & before/after diagram (documented)
- `EXPL-24` مسار قرار ومخطط انسيابي / Decision path & flowchart (install)
- `EXPL-25` دورة ورمز ينتقل / Cycle diagram, travelling token & loop arrow (ready)

### `EXPL-24` — مسار قرار ومخطط انسيابي / Decision path & flowchart

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سؤال، فرعان ملونان، ومثال يسير إلى نتيجته؛ أو شجرة قرار بملاحظات لاصقة ومؤشر يتفاعل. / A question, two coloured branches, an example travelling to its outcome.

**متى:** «ماذا أفعل لو…»، استكشاف أخطاء / decision guides, troubleshooting.

**كيف:** MG-087: 0–2 s question, 2–5 branches, 5–8 example path, 8–10 result, chosen branch highlighted (high-stakes advice needs expert review); failover: request pill → diamond, red failed branch then green success branch draws in 400 ms; faded options with a line to the highlighted pill. HyperFrames blocks flowchart (12 s, 1920×1080) and flowchart-vertical (1440×2560) with sticky-note nodes and typing correction.

**المعاملات:** 10 s; branch draw 400 ms

**التثبيت:** npx hyperframes add flowchart

**الوسوم:** decision tree · flowchart · branches · قرار

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md`
- `kosif-one/vendor/hyperframes/registry/blocks/flowchart/flowchart.html`
- `kosif-tool/styles/pm-misbahsy-80eaec`

#### 7. قدرات قريبة في العائلة

- `EXPL-22` التكبير على مكوّن وقبل/بعد / Zoom into component & before/after diagram (documented)
- `EXPL-23` الخط الزمني برأس تشغيل / Timeline with playhead (documented)
- `EXPL-25` دورة ورمز ينتقل / Cycle diagram, travelling token & loop arrow (ready)
- `EXPL-26` شريط المراحل ومؤشر الخطوات / Stage tracker pills & steppers (ready)

### `EXPL-25` — دورة ورمز ينتقل / Cycle diagram, travelling token & loop arrow

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أربع أيقونات على دائرة وأسهم تنمو بينها بالترتيب، وكرة تنقل الفكرة بين المحطات وتغير لونها، وسهم دائري ختامي يقول «وتتكرر». / Icons on a circle with arrows growing in order, a travelling token, and a closing loop arrow.

**متى:** دورات طبيعية، دورة حياة منتج / natural cycles, lifecycles.

**كيف:** MG-081: 0–1 s title, 1–7 stages, 7–10 full cycle (direction readable muted); MG-083: ball on a Bezier with stops, colour change only when it means something; water-cycle recap: big orange loop pathLength=1 drawn 8.9–9.8 s eased, marker-end attached only when progress > .98, #FF7A00 9 px.

**المعاملات:** 10 s; loop 8.9–9.8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cycle · loop arrow · token · دورة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/water-cycle-animation/index.html`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-23` الخط الزمني برأس تشغيل / Timeline with playhead (documented)
- `EXPL-24` مسار قرار ومخطط انسيابي / Decision path & flowchart (install)
- `EXPL-26` شريط المراحل ومؤشر الخطوات / Stage tracker pills & steppers (ready)
- `EXPL-27` خطأ ثم تصحيح / Mistake then correction (documented)

### `EXPL-26` — شريط المراحل ومؤشر الخطوات / Stage tracker pills & steppers

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريط حبوب مرقمة من اليمين يمتلئ فيه الحالي بالبرتقالي، ودوائر خطوات مترابطة، وعقد رحلة تقفز بالتتابع. / Numbered RTL stage pills, linked step circles and journey nodes popping in sequence.

**متى:** شروح بمراحل، إجراءات / staged explainers, procedures.

**كيف:** water cycle: 4 pills 260×70 rx 35 at y 968, x = 1395 − i·290, fill mix(#FFFFFF, #FF7A00, on), text mix(#0B2545, #FFFFFF, on), all light together in the recap; audit-pro journey: 5 nodes 36 px pop 260 ms spring (translate 7 px + scale .88 → 1) with delays 180–360 ms (45 ms step) after the line starts — done = teal + check, current = violet with 4 px halo; trace chain cards 260 ms at 50 ms steps with 8×2 px connectors scaling from the right; numbered step cards (yellow badge, outline icon) 1.2–1.5 s apart; 4-segment top bar filling with big mono 01–04.

**المعاملات:** pills 260×70; pop 260 ms; 45–50 ms steps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stepper · stage tracker · pills · مراحل · خطوات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/water-cycle-animation/index.html`
- `kosif-audit-pro/app/globals.css:998`
- `kosif-audit-pro/app/globals.css:2191`

#### 7. قدرات قريبة في العائلة

- `EXPL-24` مسار قرار ومخطط انسيابي / Decision path & flowchart (install)
- `EXPL-25` دورة ورمز ينتقل / Cycle diagram, travelling token & loop arrow (ready)
- `EXPL-27` خطأ ثم تصحيح / Mistake then correction (documented)
- `EXPL-28` مقارنة سرعة عادلة / Fair speed comparison (documented)

### `EXPL-27` — خطأ ثم تصحيح / Mistake then correction

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مثال خاطئ يتجمد ويُحاط بدائرة وينزاح، ثم تظهر النسخة الصحيحة؛ أو قاعدة خاطئة تُشطب وبجانبها الصحيحة بعلامة صح. / A wrong example freezes, is ringed and slides aside; the correct version appears.

**متى:** تصحيح مفاهيم شائعة / correcting common misconceptions.

**كيف:** MG-084: 0–2 s example, 2–3 alert, 3–6 fix, 6–8 summary (freeze frame, masks, sequential comparison; illustrate dangerous actions instead of filming them); strike: red line draws over the wrong rule in 250 ms, then the right one with a drawn check in 300 ms (DRAW-19/21).

**المعاملات:** 8 s; strike 250 / check 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mistake · correction · wrong right · تصحيح

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md`
- `kosif-tool/styles/pm-chatgptastra-0d95c7`

#### 7. قدرات قريبة في العائلة

- `EXPL-25` دورة ورمز ينتقل / Cycle diagram, travelling token & loop arrow (ready)
- `EXPL-26` شريط المراحل ومؤشر الخطوات / Stage tracker pills & steppers (ready)
- `EXPL-28` مقارنة سرعة عادلة / Fair speed comparison (documented)
- `EXPL-29` تسميات بخطوط قائدة / Leader-line callouts (2D & 3D) (ready)

### `EXPL-28` — مقارنة سرعة عادلة / Fair speed comparison

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جسمان يقطعان المسافة نفسها بجانب ساعة ظاهرة، وأي اختلاف في الزمن أو المسافة يُذكر. / Two objects cover the same distance beside a visible clock.

**متى:** «أيهما أسرع»، أداء / performance comparisons.

**كيف:** MG-088: 0–1 s conditions, 1–6 motion, 6–8 result; identical paths and fixed distances with on-screen timers; performance bars racing for code (EXPL-42).

**المعاملات:** 8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** comparison · race · fair · مقارنة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-26` شريط المراحل ومؤشر الخطوات / Stage tracker pills & steppers (ready)
- `EXPL-27` خطأ ثم تصحيح / Mistake then correction (documented)
- `EXPL-29` تسميات بخطوط قائدة / Leader-line callouts (2D & 3D) (ready)
- `EXPL-30` طبقات شفافة إيزومترية / Isometric translucent layer stack (seen)

### `EXPL-29` — تسميات بخطوط قائدة / Leader-line callouts (2D & 3D)

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة وخط وتسمية تشير إلى جزء من واجهة أو مجسم، مع قياس حي يتغير مع الزمن. / Dot + leader line + label anchored to a UI point or projected 3D point, with live measurements.

**متى:** شرح أجزاء منتج أو واجهة / explaining product or UI parts.

**كيف:** 2D: thin amber elbow lines from page points to mono labels at the frame sides, draw-on 300 ms each, stagger 80 ms, small square end-cap; feature labels: 1 px line 250 ms, text +150 ms, 2–4 words, shadow blur 40 px at 8%. 3D: h.addCallout({anchor, label:'THE EAR · الأذن', title, text, side, radius, measure: t → '0.42 m'}) projects a dashed ring (4.5% H) to screen with a leader (dx 9% W, dy −14% H) and a card 14–22% W; callout.show 0..1 per frame. Corner crop brackets (L-marks, arm 12 px, 300 ms ease-out) and dimension arrows with tiny mono labels.

**المعاملات:** draw 250–300 ms; stagger 80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** callout · leader line · label · 3D annotation · تسمية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/lab-kit.js`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:233`
- `kosif-tool/styles/pm-kyonax-on-tech-aabc1d`
- `kosif-tool/styles/pm-techyoutbe-945b56/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-27` خطأ ثم تصحيح / Mistake then correction (documented)
- `EXPL-28` مقارنة سرعة عادلة / Fair speed comparison (documented)
- `EXPL-30` طبقات شفافة إيزومترية / Isometric translucent layer stack (seen)
- `EXPL-31` التضخيم والمقارنة بالمقياس / Exaggerated scale & size comparison (seen)

### `EXPL-30` — طبقات شفافة إيزومترية / Isometric translucent layer stack

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ألواح مدورة مائلة بزاوية إيزومترية تتدرج من شفافة إلى زرقاء مصمتة، واللوح العلوي مرفوع بإطار متقطع وتسميات بخطوط قائدة. / Rounded plates in isometric tilt stacked with an opacity ramp; the top plate lifts.

**متى:** طبقات برمجيات، مكدسات / software layers, stacks.

**كيف:** CSS transform rotateX(55deg) rotateZ(−45deg), 6–7 plates offset 18 px, light → solid blue #1f7bf2 with a glow below; top plate lifted with a dashed outline; leader lines draw right then mono labels fade in.

**المعاملات:** 6–7 plates; offset 18 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** isometric · layers · stack · طبقات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-ddryo-loos-300829`

#### 7. قدرات قريبة في العائلة

- `EXPL-28` مقارنة سرعة عادلة / Fair speed comparison (documented)
- `EXPL-29` تسميات بخطوط قائدة / Leader-line callouts (2D & 3D) (ready)
- `EXPL-31` التضخيم والمقارنة بالمقياس / Exaggerated scale & size comparison (seen)
- `EXPL-32` طباعة الكود على الشاشة / On-screen code typography (documented)

### `EXPL-31` — التضخيم والمقارنة بالمقياس / Exaggerated scale & size comparison

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضخّم خاصية دقيقة رأسيًا ×N مع تسمية «مُضخّم ×9.6»، أو صفّ كرات أحجامها جذر القيمة. / Exaggerate a subtle property ×N with an honest label, or size spheres by √value.

**متى:** فروقات صغيرة جدًا أو كبيرة جدًا / tiny or huge differences.

**كيف:** scale ×5–10 with a teal 40% tint and the label 'shown ×N' plus callout tags; spheres sized by sqrt(value) with a minimum clamp for tiny values, staggered pop-in right → left (250 ms) with arrows and % captions — always state the exaggeration on screen.

**المعاملات:** ×5–10; sqrt sizing; stagger 250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scale · exaggeration · comparison · مقياس

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-blueoctopusai-dd17bd`
- `kosif-tool/styles/infographic`

#### 7. قدرات قريبة في العائلة

- `EXPL-29` تسميات بخطوط قائدة / Leader-line callouts (2D & 3D) (ready)
- `EXPL-30` طبقات شفافة إيزومترية / Isometric translucent layer stack (seen)
- `EXPL-32` طباعة الكود على الشاشة / On-screen code typography (documented)
- `EXPL-33` كتابة بتذبذب مزروع / Seeded typing animation (install)

### `EXPL-32` — طباعة الكود على الشاشة / On-screen code typography

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط أحادي العرض حقيقي، أسطر محدودة، سمة ألوان واحدة، إبراز 1–3 أسطر، وكود صحيح معقول. / Real monospace, limited lines, one syntax theme, 1–3 highlighted lines, plausible correct code.

**متى:** كل مشهد كود / every code scene.

**كيف:** mono 28–40 px at 1080 width, ≤14 lines, line-height 1.6, tinted background; JetBrains Mono / Geist Mono / IBM Plex Mono; code is always LTR, even inside an Arabic film (wrap in dir="ltr"); render with pre-tokenised spans so text is exact (never an image model).

**المعاملات:** 28–40 px; ≤14 lines; lh 1.6

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** code typography · monospace · syntax · كود

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/code.md:15`
- `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-30` طبقات شفافة إيزومترية / Isometric translucent layer stack (seen)
- `EXPL-31` التضخيم والمقارنة بالمقياس / Exaggerated scale & size comparison (seen)
- `EXPL-33` كتابة بتذبذب مزروع / Seeded typing animation (install)
- `EXPL-34` جلسة الطرفية / Terminal session scene (documented)

### `EXPL-33` — كتابة بتذبذب مزروع / Seeded typing animation

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Remotion company license |

**ما هي:** كتابة حرفًا حرفًا بتذبذب مزروع ووقفات بعد علامات الترقيم ومؤشر يومض، والكود الطويل يُلصق كتلة. / Per-character typing with seeded jitter, punctuation pauses and a blinking caret.

**متى:** أوامر وكود قصير / commands and short code.

**كيف:** per-char delay = (1/cps)·(0.8 + random(`k${i}`)·0.4) + 0.3 s after [.,;:]; 25–45 cps (default 35); caret ▍ 530 ms; long code pasted as a block with a 200 ms fade; Arabic never per letter — whole words or a mask (ARAB-01). Remotion Typed component in the playbook; the canvas port below needs nothing installed. (code snippet in references/powers/diagrams-explainers-code.md)

**المعاملات:** 35 cps ±20%; +250–400 ms punctuation; caret 530 ms

**التثبيت:** cd kosif-tool/starters/remotion && npm i

**الوسوم:** typing · typewriter · caret · seeded · كتابة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/code.md:25`
- `kosif-tool/playbooks/code.md:55`
- `kosif-tool/starters/html-canvas/timeline.js`

#### 7. قدرات قريبة في العائلة

- `EXPL-31` التضخيم والمقارنة بالمقياس / Exaggerated scale & size comparison (seen)
- `EXPL-32` طباعة الكود على الشاشة / On-screen code typography (documented)
- `EXPL-34` جلسة الطرفية / Terminal session scene (documented)
- `EXPL-35` إبراز السطر والتمرير والخطأ / Line highlight, scroll & error sweep (documented)

### `EXPL-34` — جلسة الطرفية / Terminal session scene

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نافذة طرفية تكبر، أمر يُكتب، وميض Enter، مخرجات على دفعات، وإبراز النجاح مع دفع كاميرا. / Terminal scales in, command types, enter flash, output in blocks, success highlight with a push.

**متى:** أدوات المطورين وافتتاحيات تقنية / dev tools and tech openers.

**كيف:** 0–300 ms scale from 0.96; 300–1300 ms type at 35 cps; 1300–1600 ms caret/enter flash; 1600–2400 ms 3 output blocks; 2400–3000 ms success highlight + 3% push. Openers: '$ command' typed 30–50 ms/char with a block cursor on black; compile rows whose block bars fill (300 ms each, rows 150 ms apart); log lines every 120 ms with the last one green; colour-coded event log (6 rows, fixed char widths, new rows push old up); terminal left 60% + definition card right. Real sessions can be captured as an asciinema .cast and replayed (external tools).

**المعاملات:** 0/300/1300/1600/2400/3000 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** terminal · command · output · طرفية · CLI

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/code.md:35`
- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`
- `kosif-tool/styles/pm-madhav-xo-f97f20`

#### 7. قدرات قريبة في العائلة

- `EXPL-32` طباعة الكود على الشاشة / On-screen code typography (documented)
- `EXPL-33` كتابة بتذبذب مزروع / Seeded typing animation (install)
- `EXPL-35` إبراز السطر والتمرير والخطأ / Line highlight, scroll & error sweep (documented)
- `EXPL-36` كشف الفرق / Diff reveal (documented)

### `EXPL-35` — إبراز السطر والتمرير والخطأ / Line highlight, scroll & error sweep

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريط ينزلق خلف السطر المهم والباقي يخفت، والتمرير بأسطر كاملة، وشريط أحمر مع خط متموج للخطأ. / A band behind the key line with others dimmed, whole-line scrolling, and a red error sweep.

**متى:** شرح سطر بعينه / explaining a specific line.

**كيف:** highlight band 250 ms ease-out cubic, others to 50%; scroll 200–300 ms per line ease-in-out (never fractional lines); error: red band scaleX 0 → 1 + squiggle draw 0.6 s; prompt card: cream mono typed ~30 ms/char, then red rectangles wipe behind faulty words (250 ms each, 300 ms apart) and the text turns light; file tree: a highlight bar steps rows.

**المعاملات:** 250 ms; 50% dim; 200–300 ms/line

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** highlight line · scroll · error · إبراز

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/code.md:26`
- `kosif-tool/playbooks/code.md:27`
- `kosif-tool/styles/pm-henkvaness-0e06af`

#### 7. قدرات قريبة في العائلة

- `EXPL-33` كتابة بتذبذب مزروع / Seeded typing animation (install)
- `EXPL-34` جلسة الطرفية / Terminal session scene (documented)
- `EXPL-36` كشف الفرق / Diff reveal (documented)
- `EXPL-37` نافذة كود مشروحة / Annotated code-window figure (documented)

### `EXPL-36` — كشف الفرق / Diff reveal

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأسطر المحذوفة تنطوي بالأحمر، المضافة تتمدد بالأخضر، والثابتة تنزلق. / Removed lines collapse red, added expand green, unchanged slide.

**متى:** شرح تغيير في الكود / explaining a code change.

**كيف:** removed 250 ms, added 300 ms, staggered; exactly 2 states; variant: green wipe over a red diff, test dots fill one by one, bracket burst on pass.

**المعاملات:** 250 / 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** diff · code change · red green · فرق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/code.md:49`
- `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-34` جلسة الطرفية / Terminal session scene (documented)
- `EXPL-35` إبراز السطر والتمرير والخطأ / Line highlight, scroll & error sweep (documented)
- `EXPL-37` نافذة كود مشروحة / Annotated code-window figure (documented)
- `EXPL-38` كود ومعاينة حية / Code + live preview split (seen)

### `EXPL-37` — نافذة كود مشروحة / Annotated code-window figure

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نافذة محرر داكنة مدورة بثلاث نقاط، ألوان صياغة محددة، وحتى 3 إبرازات بإطار أخضر وأسهم صفراء يدوية إلى ملاحظات. / A dark rounded editor window with ≤3 green-box highlights and hand-drawn yellow arrows.

**متى:** شرح مقتطف كود في ريل / a code snippet in a reel.

**كيف:** window #2A2622 with three traffic-light dots; keys #E06C9F, strings #E5A86B, numbers #A78BFA, punctuation light grey; highlights as green outline boxes #7EE787 with yellow curved arrows to callouts; 4:3, 4–12 lines, 60/35 split; animate window in → lines reveal → box draws → arrow draws → callout pops; Prism/highlight.js from a CDN or pre-tokenised spans.

**المعاملات:** ≤3 callouts; 4–12 lines

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** code window · annotation · syntax colours · نافذة كود

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1094-akbun-draw/2426-akbun-generateimage-code/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-35` إبراز السطر والتمرير والخطأ / Line highlight, scroll & error sweep (documented)
- `EXPL-36` كشف الفرق / Diff reveal (documented)
- `EXPL-38` كود ومعاينة حية / Code + live preview split (seen)
- `EXPL-39` كود مجرد ورقائق / Abstract code pills & token chips (seen)

### `EXPL-38` — كود ومعاينة حية / Code + live preview split

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوح يكتب الكود بألوانه وأرقام أسطره، ولوح بجانبه يُظهر النتيجة تتفاعل لحظة اكتمال السطر. / One pane types code; the other shows the result reacting as each line completes.

**متى:** دروس برمجة، ألعاب، رسم بالكود / coding lessons, creative coding.

**كيف:** ~25 chars/s, caret blink 500 ms; the result pane reads the same t (the sprite jumps when the jump() line completes); test checklist ticks below; triptych variant: framed canvas with ruler and red playhead + mono code with orange literals + serif formula, the playhead time ('t = 1.97 s') drives both the shapes and the highlighted code line.

**المعاملات:** ~25 cps; caret 500 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** live preview · code split · creative coding · معاينة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-ibrahimwasim240-809370`
- `kosif-tool/styles/plotter`

#### 7. قدرات قريبة في العائلة

- `EXPL-36` كشف الفرق / Diff reveal (documented)
- `EXPL-37` نافذة كود مشروحة / Annotated code-window figure (documented)
- `EXPL-39` كود مجرد ورقائق / Abstract code pills & token chips (seen)
- `EXPL-40` كتل HyperFrames للكود / HyperFrames code blocks (install)

### `EXPL-39` — كود مجرد ورقائق / Abstract code pills & token chips

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكود كأشرطة ملونة مجردة، أو رقائق رموز بأرقامها، أو سحابة رقائق كود عائمة، أو بطاقة JSON تُكتب. / Code as abstract coloured pills, token chips with ids, a floating chip cloud, or a typed JSON card.

**متى:** ذكاء اصطناعي، نماذج لغوية، APIs / AI, LLMs, APIs.

**كيف:** rows of rounded rects in syntax colours with bracket glyphs; tokens as pastel mono chips (radius 8 px) with grey ids beneath, stagger 90 ms, scale .8 → 1 back-out; 20–30 mono pills drifting 4–8 px sine at .4–.9 opacity around hero text; lime-bordered JSON card with a pink filename tab typed ~30 chars/s and chips drifting 10 px; JSON response lines + '200 OK' pill.

**المعاملات:** chips stagger 90 ms; drift 4–8 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tokens · chips · JSON · abstract code · رقائق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-kloss-xyz-15182a`
- `kosif-tool/styles/pm-misbahsy-80eaec`
- `kosif-tool/styles/pm-techhalla-7acbc2`

#### 7. قدرات قريبة في العائلة

- `EXPL-37` نافذة كود مشروحة / Annotated code-window figure (documented)
- `EXPL-38` كود ومعاينة حية / Code + live preview split (seen)
- `EXPL-40` كتل HyperFrames للكود / HyperFrames code blocks (install)
- `EXPL-41` من طلب دمج أو نص إلى فيديو شرح / PR-to-video & faceless explainer pipelines (install)

### `EXPL-40` — كتل HyperFrames للكود / HyperFrames code blocks

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (GSAP standard no-charge license inside) |

**ما هي:** كتل جاهزة لكل حركة كود شائعة: كتابة، فرق، تحول، إبراز، تمرير، لوح ثلاثي، جسيمات، ذوبان بالشيدر، ومحررات وطرفيات. / Ready blocks for every common code motion.

**متى:** فيديو تقني سريع بجودة عالية / fast, polished tech videos.

**كيف:** npx hyperframes add <name>, fill __TOKENS states / __BLOCK params: code-typing (5 s, caret tracks the frontier), code-diff (6 s, 2 states), code-morph (7 s, Shiki-Magic-Move-style token glide), code-highlight (5 s, line 0-based), code-scroll (6 s, line 1-based), code-3d-extrude (8 s WebGL slab), code-particle-assemble (8 s GPU points to glyph pixels), code-shader-dissolve (7 s), code-snippet-apple-terminal-pro (12 s), code-snippet-dark-2026 / dark-modern (11 s VS Code workbench), code-terminal-run (cadence uniform\|human), terminal-simulator, grid-card-assemble (capability cards). All 1920×1080, GSAP paused timeline (WebGL ones load three 0.147 from a CDN).

**المعاملات:** 13 blocks; 5–12 s

**التثبيت:** npx hyperframes add code-morph

**الوسوم:** code blocks · hyperframes · code morph · VS Code · terminal

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md`
- `kosif-one/vendor/hyperframes/registry/blocks/code-morph/code-morph.html`
- `kosif-one/vendor/hyperframes/registry/components/code-terminal-run/code-terminal-run.html`
- `kosif-one/vendor/hyperframes/registry/blocks/code-3d-extrude/code-3d-extrude.html`

#### 7. قدرات قريبة في العائلة

- `EXPL-38` كود ومعاينة حية / Code + live preview split (seen)
- `EXPL-39` كود مجرد ورقائق / Abstract code pills & token chips (seen)
- `EXPL-41` من طلب دمج أو نص إلى فيديو شرح / PR-to-video & faceless explainer pipelines (install)
- `EXPL-42` حرّك ما يفعله الكود / Mechanism beat: animate behaviour, not code (documented)

### `EXPL-41` — من طلب دمج أو نص إلى فيديو شرح / PR-to-video & faceless explainer pipelines

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طلب دمج على GitHub أو نص حر يتحول إلى فيديو شرح مروي بإطارات مخترعة (طباعة، مخططات، بيانات) وترجمة وانتقالات. / A GitHub PR or free text becomes a narrated explainer of invented frames.

**متى:** سجل تغييرات، إعلان ميزة، شرح 30–90 ث / changelogs, feature reveals, 30–90 s explainers.

**كيف:** PR: node fetch-pr.mjs --pr <ref> (gh) → ingest.mjs (tokens/text/people) → fetch-people-avatars.mjs → frames hook, problem, change, diff, before_after, mechanism, impact, evidence (+N/−M, passing test, benchmark), credits, cta in code-editorial treatments. Faceless: build-frame.mjs --preset → storyboard + SCRIPT.md → audio.mjs (voice; Kokoro local or HeyGen key) → frame-packets → captions → assemble → transitions inject/verify → lint/check/snapshot → render. Arabic voice and captions need the KOSIF voice and caption powers instead of the defaults.

**المعاملات:** sweet spot 30–90 s; ≤~3 min

**التثبيت:** npm i -g hyperframes

**الوسوم:** PR to video · faceless explainer · pipeline · changelog

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:kokoro` ← python3 -c "import kokoro" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/pr-to-video/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/faceless-explainer/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/pr-to-video/references/story-design.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-39` كود مجرد ورقائق / Abstract code pills & token chips (seen)
- `EXPL-40` كتل HyperFrames للكود / HyperFrames code blocks (install)
- `EXPL-42` حرّك ما يفعله الكود / Mechanism beat: animate behaviour, not code (documented)
- `EXPL-43` شجرة ملفات تتحول إلى أعمدة / Folder tree to bar chart (idea)

### `EXPL-42` — حرّك ما يفعله الكود / Mechanism beat: animate behaviour, not code

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أظهر سلوك التشغيل بدل الكود: دورة إعادة المحاولة، حارات الذاكرة المؤقتة، تحول التسلسلي إلى متوازٍ، سباق أداء، فك تشابك الاستدعاءات. / Show runtime behaviour instead of code.

**متى:** شرح تحسين أو إصلاح / explaining an optimisation or fix.

**كيف:** retry/backoff: fire → 500 → growing wait → retry → 200; cache lanes: cold DB vs cached racing; serial lane reshaping into parallel lanes; race bug then fixed flow; performance bars racing; tangled call graph untangling; build as invented SVG/GSAP diagrams; agent tool events (read/search/edit/test/error) as cards snapping on beats (enter (.22,1,.36,1) 420 ms, exit (.4,0,1,1) 260 ms, ≥900 ms on screen, ≤3 stacked) and a call-stack breadcrumb HUD of mono chips (push 200 ms).

**المعاملات:** cards ≥900 ms; ≤3 stacked

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mechanism · runtime behaviour · retry · cache · آلية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md`
- `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`
- `kosif-tool/styles/pm-emollick-8661a8`

#### 7. قدرات قريبة في العائلة

- `EXPL-40` كتل HyperFrames للكود / HyperFrames code blocks (install)
- `EXPL-41` من طلب دمج أو نص إلى فيديو شرح / PR-to-video & faceless explainer pipelines (install)
- `EXPL-43` شجرة ملفات تتحول إلى أعمدة / Folder tree to bar chart (idea)
- `EXPL-44` معادلة تتكون خطوة خطوة / Equation built step by step (bidi-safe) (install)

### `EXPL-43` — شجرة ملفات تتحول إلى أعمدة / Folder tree to bar chart

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أسطر شجرة المجلدات تنبثق أعمدة بعدد أسطر الكود الحقيقي في المستودع. / Nested folder lines extrude into bars of real line counts.

**متى:** «حجم مشروعي» / showing a codebase's size.

**كيف:** count lines per folder from the real repo (cloc or wc -l), draw the tree, then extrude each row into a bar counting up in 600 ms; numbers must come from the repo, never invented.

**المعاملات:** count 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** folder tree · bar chart · codebase · cloc

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-danilowm-d3720d/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-41` من طلب دمج أو نص إلى فيديو شرح / PR-to-video & faceless explainer pipelines (install)
- `EXPL-42` حرّك ما يفعله الكود / Mechanism beat: animate behaviour, not code (documented)
- `EXPL-44` معادلة تتكون خطوة خطوة / Equation built step by step (bidi-safe) (install)
- `EXPL-45` Manim للاشتقاق والنهايات / Manim derivations & limits (install)

### `EXPL-44` — معادلة تتكون خطوة خطوة / Equation built step by step (bidi-safe)

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المعطيات ثم العملية ثم النتيجة، والحد المشروح ملوّن، والمعادلة لا تنعكس أبدًا داخل جملة عربية. / Givens, operator, result, the explained term tinted; never mirrored inside Arabic.

**متى:** رياضيات وفيزياء / maths and physics.

**كيف:** MG-090: 0–2 s givens, 2–5 operation, 5–8 result, 8–10 read; render with KaTeX (renderToString → HTML/SVG) or pre-rendered SVG; wrap formulas in an LTR isolate (dir="ltr", unicode-bidi:isolate) inside RTL captions; reveal terms by opacity/colour keys with constant spacing between separate layers; define each symbol before use.

**المعاملات:** 10 s

**التثبيت:** npm i katex

**الوسوم:** equation · KaTeX · math · bidi · معادلة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md`
- `kosif-atlas/skills/994-write-math/2278-write-math/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-42` حرّك ما يفعله الكود / Mechanism beat: animate behaviour, not code (documented)
- `EXPL-43` شجرة ملفات تتحول إلى أعمدة / Folder tree to bar chart (idea)
- `EXPL-45` Manim للاشتقاق والنهايات / Manim derivations & limits (install)
- `EXPL-46` دوائر فورييه والجيب / Fourier epicycles & unit-circle sine (seen)

### `EXPL-45` — Manim للاشتقاق والنهايات / Manim derivations & limits

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اشتقاق جبري بألوان دلالية يتحول سطرًا إلى سطر، قاطع يصير مماسًا، وإطارات حول أجزاء المعادلة بشروح. / Colour-coded derivations, secant-to-tangent limits and boxed annotations.

**متى:** شروح رياضية بأسلوب 3Blue1Brown الأصلي / maths explainers.

**كيف:** MathTex with isolated substrings, cancelling terms red, result green, TransformMatchingTex between lines (line spacing ~12% H, Write ~1.5 s per line); ValueTracker dt 2 → 1 → 0.1 → 0.01 → 0.001 (each ~2–3 s, smooth) with always_redraw secant and DecimalNumber slope readout; SurroundingRectangle around numerator/denominator (stroke 2 px, buff .08) with captions in the matching colour (Create ~0.6 s); render with -qh at the target fps and mux the user's audio separately; Arabic text via Text() with an Arabic font, never inside MathTex.

**المعاملات:** Write 1.5 s; dt → 0.001

**التثبيت:** pip install manim

**الوسوم:** manim · derivation · limit · tangent · رياضيات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`
- `kosif-tool/styles/pm-linearuncle-5d2bae`

#### 7. قدرات قريبة في العائلة

- `EXPL-43` شجرة ملفات تتحول إلى أعمدة / Folder tree to bar chart (idea)
- `EXPL-44` معادلة تتكون خطوة خطوة / Equation built step by step (bidi-safe) (install)
- `EXPL-46` دوائر فورييه والجيب / Fourier epicycles & unit-circle sine (seen)
- `EXPL-47` برهان بصري بطيران الخلايا / Cell-flight visual proof (seen)

### `EXPL-46` — دوائر فورييه والجيب / Fourier epicycles & unit-circle sine

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سلسلة متجهات دوّارة من تحويل فورييه ترسم مسارًا بأثر متوهج، ونقطة على دائرة تُسقط موجة جيبية متحركة. / Rotating DFT vectors draw a path with a glowing trail; a point on a circle projects a scrolling sine.

**متى:** رياضيات جميلة، إشارات / beautiful maths, signals.

**كيف:** sample the target path to N points, DFT → (freq, amp, phase) sorted by amplitude, at time t chain vectors amp·e^{i(freq·2πt/T + phase)} and draw the tip's trail (fading); unit circle: point (cos ωt, sin ωt) with a projection line to a sine scrolling right; all from t, no accumulation.

**المعاملات:** N terms; period T

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** fourier · epicycles · sine · unit circle · فورييه

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-math-files-39c9d0`

#### 7. قدرات قريبة في العائلة

- `EXPL-44` معادلة تتكون خطوة خطوة / Equation built step by step (bidi-safe) (install)
- `EXPL-45` Manim للاشتقاق والنهايات / Manim derivations & limits (install)
- `EXPL-47` برهان بصري بطيران الخلايا / Cell-flight visual proof (seen)
- `EXPL-48` شروح تعلم الآلة / ML explainer devices (seen)

### `EXPL-47` — برهان بصري بطيران الخلايا / Cell-flight visual proof

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل خلية من مربع تطير إلى موضعها في مربع الوتر بالتتابع، وعداد للخلايا الواصلة، ووهج عند الاكتمال. / Each cell flies to its place in the hypotenuse square, with a counter and completion glow.

**متى:** براهين هندسية، تحويل مساحات / geometric proofs.

**كيف:** lerp source → target cell centre, rotate to the hypotenuse angle, hop = h·sin(πu); 25 cells, stagger ~120 ms, hop 20 px; counter = arrived count; glow square at the end.

**المعاملات:** 25 cells; 120 ms; hop 20 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** visual proof · pythagoras · cells · برهان

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/chalkboard`

#### 7. قدرات قريبة في العائلة

- `EXPL-45` Manim للاشتقاق والنهايات / Manim derivations & limits (install)
- `EXPL-46` دوائر فورييه والجيب / Fourier epicycles & unit-circle sine (seen)
- `EXPL-48` شروح تعلم الآلة / ML explainer devices (seen)
- `EXPL-49` لوحة قياسات حية / Live telemetry & math HUD (seen)

### `EXPL-48` — شروح تعلم الآلة / ML explainer devices

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تمرير نواة على رقم بكسلي إلى خريطة حرارية، أقواس انتباه بين الكلمات، مصفوفة تتفرع كتلًا، شبكة بحواف موجبة وسالبة، وشجرة هرمية بمستويات. / Convolution scans, attention arcs, recursive block matrices, signed graphs and level trees.

**متى:** شرح الذكاء الاصطناعي والفيزياء الإحصائية / AI and statistical-physics explainers.

**كيف:** convolution: pixel digit, kernel square scanning, heatmap output; attention: arcs from one word to others, stroke width = weight; hatched square → 2×2 blocks with cross-hatched diagonal → nested sub-blocks (3 stages, hatch ~8 px); N = 7–8 nodes on a circle with ±-signed edges drawing 80 ms apart; binary tree root-down with dashed coloured level lines and leaf dots last; camera 800 ms easeInOutQuad, ≤5 moves.

**المعاملات:** edge stagger 80 ms; ≤5 camera moves

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** machine learning · attention · convolution · matrix · ذكاء اصطناعي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-kloss-xyz-fe0c31`
- `kosif-tool/styles/pm-tak3sh8-be5012`
- `kosif-tool/styles/pm-tak3sh8-be5012/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-46` دوائر فورييه والجيب / Fourier epicycles & unit-circle sine (seen)
- `EXPL-47` برهان بصري بطيران الخلايا / Cell-flight visual proof (seen)
- `EXPL-49` لوحة قياسات حية / Live telemetry & math HUD (seen)
- `EXPL-50` التوأم الإنشائي: حلّال الجملونات / Structural twin truss solver (proven)

### `EXPL-49` — لوحة قياسات حية / Live telemetry & math HUD

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوحتان أحاديتا العرض بقيم جدولية تُحدَّث من نموذج فيزيائي كل إطار، أو مخطط هندسي بقيم تُحسب أمامك. / Mono panels with tabular values updated each frame from a model.

**متى:** فيزياء، فضاء، هندسة / physics, space, engineering.

**كيف:** amber labels #e0a060, white right-aligned tabular values (2 decimals), 1 px rule; values computed from the same t as the picture; switch to ∞ / 'lost' at a horizon; wireframe isometric box with a highlighted vector and a side panel of values computing to a result counter.

**المعاملات:** 2 decimals; tabular-nums

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** telemetry · HUD · live values · physics · قياسات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-rebutonepress-810f78`
- `kosif-tool/styles/pm-adamdesgns-478d6d`

#### 7. قدرات قريبة في العائلة

- `EXPL-47` برهان بصري بطيران الخلايا / Cell-flight visual proof (seen)
- `EXPL-48` شروح تعلم الآلة / ML explainer devices (seen)
- `EXPL-50` التوأم الإنشائي: حلّال الجملونات / Structural twin truss solver (proven)
- `EXPL-51` فيلم التوأم الإنشائي / Structural twin film (truss on a character) (ready)

### `EXPL-50` — التوأم الإنشائي: حلّال الجملونات / Structural twin truss solver

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحليل جملونات خطي مرن بمفاصل في 2D و3D: إزاحات، ردود أفعال، قوى محورية، شد وضغط، نسب استخدام، معاملات انهيار، وترتيب الأعضاء الأضعف، ومبادلة جزء وإعادة الحساب / أرقامه تقود فيلمًا ولوحة. — Linear-elastic pin-jointed truss analysis whose numbers drive a film and a dashboard.

**متى:** «لماذا ينكسر هذا؟» شرح هندسي تعليمي / educational engineering explainers.

**كيف:** python structural_twin.py --sample\|--model m.json [--swap AB --area 0.0002 --young E --strength S --fracture-scale 2 --out r.json] (or kmotion.py structural); schema kosif.structural-twin.v0.1, ≤400 nodes / ≤1600 members; run here: sample triangle A(0,0) B(1,1) C(2,0) under 12 kN → first_failure_multiplier 2.946; tests 17/17 passed; twin_dashboard.py / kmotion twinview r.json --out twin.html gives an offline dashboard (baseline, swap, load slider; checked at 1365 and 390 px). Illustrative only — axial, no buckling/bending/fatigue, never for safety decisions (the output says so).

**المعاملات:** ≤400 nodes; sample 2.946×

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** truss · structural · engineering · FEA · توأم إنشائي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/structural_twin.py:128`
- `100-superskills/skills/kosif-montage-motion/tests/test_structural_twin.py`
- `100-superskills/skills/kosif-montage-motion/references/STRUCTURAL_TWIN.md`
- `100-superskills/skills/kosif-montage-motion/scripts/twin_dashboard.py:763`

#### 7. قدرات قريبة في العائلة

- `EXPL-48` شروح تعلم الآلة / ML explainer devices (seen)
- `EXPL-49` لوحة قياسات حية / Live telemetry & math HUD (seen)
- `EXPL-51` فيلم التوأم الإنشائي / Structural twin film (truss on a character) (ready)
- `EXPL-52` منظر تخطيطي ومفكك / Schematic, wireframe & exploded view (ready)

### `EXPL-51` — فيلم التوأم الإنشائي / Structural twin film (truss on a character)

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جسم لطيف يصبح جملونًا ثلاثي الأبعاد توضيحيًا تقود حساباته الفيلم: المفاصل تظهر، الأعضاء تنمو، الحمل يرتفع، الأضعف ينكسر، جزء أثخن يُستبدل، وتُرتب أنماط الانهيار. / A cute object becomes a 3D truss whose solver output drives the film.

**متى:** شرح هندسي ممتع / fun engineering explainers.

**كيف:** build_truss.py lays the truss on anatomy (ground contacts pinned, pelvis/chest four-node rings cross-braced, skull nodes with 4-nearest-neighbour bracing, ear triangles; areas 1.2e-4 body, 4.0e-5 ear roots; plush E 8 MPa, strength 2 MPa; loads crown −1.9 N) → model.json (35 nodes, 109 members, 5 supports); K3S.trussOverlay(model, {nodeParts, radius .0015–.0022, jointRadius .0032–.0042}) rides rig parts, members coloured by utilisation (0 (.35,1,.72) → .5 (.75,1,.45) → .8 (1,.86,.35) → 1 (1,.36,.28)), flash on the weak member; load arrows (cylinder r .0032 + cone .011×.022) grow and shift hue yellow → red; six beats SHAPE → JOINT → LOAD → BREAK → SWAP → RANK; baseline first limit 2.38× (earL_out–crown, tension), break at 3.0× → mechanism, ×2.6 area swap → 3.77×.

**المعاملات:** 35 nodes / 109 members; 2.38× → 3.77×

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** truss film · utilisation · load arrows · bunny twin · هندسة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/twin/build_truss.py:46`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:395`
- `kosif-studio/motion/references/STRUCTURAL_TWIN.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-49` لوحة قياسات حية / Live telemetry & math HUD (seen)
- `EXPL-50` التوأم الإنشائي: حلّال الجملونات / Structural twin truss solver (proven)
- `EXPL-52` منظر تخطيطي ومفكك / Schematic, wireframe & exploded view (ready)
- `EXPL-53` شرح علمي ثلاثي الأبعاد بأربع مراحل / Four-stage 3D science explainer (ready)

### `EXPL-52` — منظر تخطيطي ومفكك / Schematic, wireframe & exploded view

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأجزاء تتحول من قطيفة إلى خطوط حواف ليمونية فوق شبح، وتنفصل عن الجسم، وتظهر حلقات متقطعة عند المفاصل. / Parts fade to lime edge lines over a ghost, explode from the body, and show dashed joint rings.

**متى:** «كيف صُنع»، تشريح منتج / 'how it's made', product anatomy.

**كيف:** const s = K3.schematic(root, {color:'#a8ff3c', ghost:'#f7f8f2', lineOpacity:.42, angle}); s.set(k, camera) (solids fade to 8%, ghost .55), s.explode(k) (×1.1 radial), s.joints(k) (camera-facing dashed rings .1–.125).

**المعاملات:** lines ≤.42; explode ×1.1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** schematic · exploded view · wireframe · تفكيك

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/lab-kit.js:135`
- `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:135`

#### 7. قدرات قريبة في العائلة

- `EXPL-50` التوأم الإنشائي: حلّال الجملونات / Structural twin truss solver (proven)
- `EXPL-51` فيلم التوأم الإنشائي / Structural twin film (truss on a character) (ready)
- `EXPL-53` شرح علمي ثلاثي الأبعاد بأربع مراحل / Four-stage 3D science explainer (ready)
- `EXPL-54` دورة الماء التعليمية المسطحة / Flat educational water cycle (proven)

### `EXPL-53` — شرح علمي ثلاثي الأبعاد بأربع مراحل / Four-stage 3D science explainer

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فيلم سينمائي يوقّت تسميات المراحل العربية المرقمة على ما يُظهره العالم ثلاثي الأبعاد: تبخر، تكاثف، هطول، جريان. / Numbered Arabic stage labels timed to what the 3D world shows.

**متى:** دورات طبيعية وعمليات علمية / natural cycles and science processes.

**كيف:** labels revealWords/hideWords: ١ 3.3–6.1 s, ٢ 6.9–9.3 s, ٣ 10.1–12.5 s, ٤ 13.1–15.1 s aligned with world states (vapour 2.6–7.2, clouds 5.8–9.4, storm 9.5–13.4, river 12.6–14.4); end title 15.7 s; 17 s 1920×1080 30 fps.

**المعاملات:** 17 s; 4 stages

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** science · 3D explainer · water cycle · stages · علوم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/index.html:59`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:83`

#### 7. قدرات قريبة في العائلة

- `EXPL-51` فيلم التوأم الإنشائي / Structural twin film (truss on a character) (ready)
- `EXPL-52` منظر تخطيطي ومفكك / Schematic, wireframe & exploded view (ready)
- `EXPL-54` دورة الماء التعليمية المسطحة / Flat educational water cycle (proven)
- `EXPL-55` قواعد الدقة والوضوح للأطفال / Science accuracy & causal-step rules (documented)

### `EXPL-54` — دورة الماء التعليمية المسطحة / Flat educational water cycle

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرح صفي مسطح: منظر ثابت لبحر وشمس وجبل، أربع مراحل لكل منها حركة رئيسية واحدة، شريط تسمية أعلى، شريط مراحل أسفل، وسهم دورة ختامي. / A flat classroom explainer with one main motion per stage.

**متى:** دروس أطفال علمية / kids' science lessons.

**كيف:** kosif-one: single SVG + render(t), Cairo 700/800, 1920×1080 30 fps 300 frames, stages 1.5–4.0 / 4.0–6.1 / 6.1–8.0 / 8.0–8.9 / recap 8.9–10 s; kosif-studio water_cycle (17 s): M.drawPath ×9, flowDash, vapour, rain, flash, camera push, grain, vignette; beats 0–2.7 / 2.8–6.4 / 6.2–9.4 / 9.5–12.8 / 12.4–15.1 / 15.2–17 s; palette #FFD166 #FFE8C2 #7FD4FF #5EC8FF #2A6F97 #0D1B2A. The studio composition passes the static rules here (test run).

**المعاملات:** 10 s / 17 s; 1 motion per stage

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** water cycle · kids · flat explainer · دورة الماء · تعليمي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/water-cycle-animation/index.html`
- `kosif-studio/motion/projects/water_cycle/index.html:152`
- `kosif-studio/tests/test_studio.py:629`
- `100-superskills/skills/trend-animation-styles/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-52` منظر تخطيطي ومفكك / Schematic, wireframe & exploded view (ready)
- `EXPL-53` شرح علمي ثلاثي الأبعاد بأربع مراحل / Four-stage 3D science explainer (ready)
- `EXPL-55` قواعد الدقة والوضوح للأطفال / Science accuracy & causal-step rules (documented)
- `EXPL-56` نظام بطاقات الفيديو الشارح / Explainer card system (documented)

### `EXPL-55` — قواعد الدقة والوضوح للأطفال / Science accuracy & causal-step rules

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا علم خاطئ أبدًا، حركة رئيسية واحدة لكل مرحلة، لا وميض، نص ≥40 بكسل وتباين ≥4.5:1، والمفهوم في 3–6 خطوات سببية. / Never wrong science, one main motion per stage, no flashing, text ≥40 px, contrast ≥4.5:1, 3–6 causal steps.

**متى:** كل شرح تعليمي / every educational explainer.

**كيف:** vapour rises from the sea, clouds form by cooling, rain falls on land, water returns to the sea; narration ~2.5 words/s with on-screen text shorter than spoken; fixed camera, one mover per stage, stage bar at the bottom; fact-check every claim; test the script on an imaginary student; supporting planning skills: math-science-tutor, software-architecture-adr.

**المعاملات:** ≥40 px; ≥4.5:1; 2.5 w/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** accuracy · kids · legibility · causal steps · دقة علمية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/water-cycle-animation/DESIGN.md`
- `100-superskills/skills/explainer-edu-animation/SKILL.md`
- `100-superskills/skills/math-science-tutor/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-53` شرح علمي ثلاثي الأبعاد بأربع مراحل / Four-stage 3D science explainer (ready)
- `EXPL-54` دورة الماء التعليمية المسطحة / Flat educational water cycle (proven)
- `EXPL-56` نظام بطاقات الفيديو الشارح / Explainer card system (documented)
- `EXPL-57` الوثيقة المصدر وقلم التظليل / Source document & article excerpt overlay (documented)

### `EXPL-56` — نظام بطاقات الفيديو الشارح / Explainer card system

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقات فصول ملونة، بطاقات مبادئ يتلون فيها العنصر المنطوق، جداول قبل/بعد بدائرة حمراء على الصف المنطوق، كلمات مفتاحية قافزة، وعناوين مرقمة. / Chapter, principle, table, keyword and numbered-title cards.

**متى:** مقالات مصورة ويوتيوب تعليمي / video essays.

**كيف:** chapter card: pastel #EFE6F7, #FFD400 heavy type outlined #1A1A1A at 6% of glyph height, glyphs 14% of frame height, 3–4 s, 1–2 stickers; principle card: white, labels 3.5% H #1A1A1A, the spoken element turns #E53935 0.3 s after it is said; table: rows × 2 s; keyword pop #FFD400 + outline, 1–3 words, 6% H, 0.8–2 s; numbered title 8% H, 2–3 s; author each card as HTML in the kosif scaffold and render with render_html.cjs.

**المعاملات:** 14/8/6/3.5% H; +0.3 s highlight

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** explainer cards · chapter card · keyword pop · بطاقات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2458-davinciresolve-gfx-hyperframes/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-54` دورة الماء التعليمية المسطحة / Flat educational water cycle (proven)
- `EXPL-55` قواعد الدقة والوضوح للأطفال / Science accuracy & causal-step rules (documented)
- `EXPL-57` الوثيقة المصدر وقلم التظليل / Source document & article excerpt overlay (documented)
- `EXPL-58` فئات المخططات والكود في بصمة / Basma diagram & code film categories (ready)

### `EXPL-57` — الوثيقة المصدر وقلم التظليل / Source document & article excerpt overlay

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الوثيقة الأصلية كما هي مع قلم تظليل أصفر شفاف يمسح الجملة المنطوقة، أو مقتطف مقال على لوح ورقي فوق الفيديو. / The unchanged source page with a translucent highlighter on the spoken sentence, or an article excerpt panel over footage.

**متى:** أخبار، تحقيقات، مقالات رأي / news, investigations, op-eds.

**كيف:** highlighter: semi-transparent yellow rect (multiply) growing along the line timed to words.json, right → left for Arabic, held 3–5 s; excerpt: paper panel #FAFAF6 with #171717 text, 75–90% width, ≥5% margins, body 3–4% H, in 0.15–0.3 s, hold to read, out 0.15–0.25 s; optional red underline #D92D20 (0.25–0.4% H), ellipse callout 20–35% padding; news module: article slides up at readable size, keyword highlighted in place + source card.

**المعاملات:** hold 3–5 s; panel 75–90% W

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** source document · highlighter · article overlay · news · وثيقة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1096-akbun-editvideo/2430-akbun-davinciresolve-article-overlay/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/news/module.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-55` قواعد الدقة والوضوح للأطفال / Science accuracy & causal-step rules (documented)
- `EXPL-56` نظام بطاقات الفيديو الشارح / Explainer card system (documented)
- `EXPL-58` فئات المخططات والكود في بصمة / Basma diagram & code film categories (ready)
- `EXPL-59` رسومات استعارية لكل جملة / Metaphor graphic per spoken claim (ready)

### `EXPL-58` — فئات المخططات والكود في بصمة / Basma diagram & code film categories

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فئتا أفلام جاهزتان: مخططات من 3–5 عقد تظهر بالترتيب بروابط ونقاط تدفق، ومحرر كود داكن بأرقام أسطر وكتابة رمزًا رمزًا ولوح نتيجة. / Two film categories: ordered 3–5-node diagrams with flow dots, and dark code editors typing token by token with a result panel.

**متى:** طلب سريع من محرر بصمة / quick requests in the Basma editor.

**كيف:** FILM_CATS 'diagrams' and 'code' with templates concept, what-is, timeline, how-to, code-explain, dev-tool; code is LTR monospace with palette syntax colours.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** basma · templates · diagrams · code editor · بصمة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/00_editor.js:2007`
- `app/public/js/00_editor.js:1777`

#### 7. قدرات قريبة في العائلة

- `EXPL-56` نظام بطاقات الفيديو الشارح / Explainer card system (documented)
- `EXPL-57` الوثيقة المصدر وقلم التظليل / Source document & article excerpt overlay (documented)
- `EXPL-59` رسومات استعارية لكل جملة / Metaphor graphic per spoken claim (ready)
- `EXPL-60` بطاقات المقارنة والتشبيه والقوائم / Trade-off, analogy & checklist cards (seen)

### `EXPL-59` — رسومات استعارية لكل جملة / Metaphor graphic per spoken claim

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل فكرة منطوقة تحصل على استعارة مرسومة واحدة بجانب المتحدث تظهر فقط أثناء كلماتها: ساعة 24، مسار حلم، ميزان 94←76 كجم، سيارة، شريط وقت ينضب. / Each spoken idea gets one drawn metaphor that lives only while its words are spoken.

**متى:** مونتاج متحدث تحفيزي / motivational talking-head edits.

**كيف:** SVG groups #clock #dream #scale #car #timebar #endring, each drawn/animated only inside its speech() window; numbers count (94 → 76 kg) with tabular digits; time bar drains right → left; drawing details in DRAW-12.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** metaphor · talking head · spoken claim · استعارة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:58`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:267`

#### 7. قدرات قريبة في العائلة

- `EXPL-57` الوثيقة المصدر وقلم التظليل / Source document & article excerpt overlay (documented)
- `EXPL-58` فئات المخططات والكود في بصمة / Basma diagram & code film categories (ready)
- `EXPL-60` بطاقات المقارنة والتشبيه والقوائم / Trade-off, analogy & checklist cards (seen)
- `EXPL-61` أدوات بصرية للشرح / Explainer visual devices (seen)

### `EXPL-60` — بطاقات المقارنة والتشبيه والقوائم / Trade-off, analogy & checklist cards

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقتان متجاورتان بصفوف ✓/✗ وملصقات ملخصة، ثلاث لوحات تشبيه تتوهج النشطة منها، وقائمة بعلامات صح مرسومة ومؤشر ينتقل للصف النشط. / Side-by-side ✓/✗ cards, analogy triptychs and checklists with drawn ticks.

**متى:** «هذا أم ذاك»، مكونات، خطوات وصفة / 'this or that', ingredients, recipe steps.

**كيف:** trade-off: coloured headers, rows stagger 120 ms with green check / black cross boxes, rotated summary stickers, cost note below; analogy: 3 bordered cards each with its accent, icon + title + caption, active one glows; checklist: rows of circle + amount + name, upcoming at 45%, an arrow glyph slides to the active row (300 ms easeOutCubic), check drawn inside the circle (~250 ms).

**المعاملات:** rows 120 ms; tick 250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** comparison cards · analogy · checklist · مقارنة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-0xnfrith-5be616`
- `kosif-tool/styles/pm-yunn260414-60d996`
- `kosif-tool/styles/pm-sarut0bisasuke-cefa43`

#### 7. قدرات قريبة في العائلة

- `EXPL-58` فئات المخططات والكود في بصمة / Basma diagram & code film categories (ready)
- `EXPL-59` رسومات استعارية لكل جملة / Metaphor graphic per spoken claim (ready)
- `EXPL-61` أدوات بصرية للشرح / Explainer visual devices (seen)
- `EXPL-62` أسلوب الرسومات التقنية / Tech blueprint style (ready)

### `EXPL-61` — أدوات بصرية للشرح / Explainer visual devices

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صفحة كلمات كأشرطة تمتلئ، تحديد منقط بطمس، فرز عناصر صورة في سلال، خريطة فقاعات لمنظومة، وسلسلة معاملة تستقيم. / Word-bar pages, dashed marquee blur, photo-object sorting, bubble ecosystem maps, straightening transaction chains.

**متى:** شروح مفاهيم مجردة / abstract concept explainers.

**كيف:** text as rounded rects of word widths filling dark row by row (120–200 ms/row, bar 8 px r 4) with the unknown word in accent; dashed 4/4 selection rect + 12 px backdrop blur in 300 ms; corner-bracket boxes on photo items, 'identifying' status, thumbnails fly 500 ms into 4 labelled buckets with counts; ~9 named hand-drawn ellipses + 12 empty blobs joined by dotted paths with a tiny boat traversing; paper chips rotated ±6° straighten into a vertical chain inside a dashed 'one transaction' box (0.6 s stagger); clock-face grid duplicates a scene to show monotony.

**المعاملات:** 120–200 ms/row; blur 12 px; fly 500 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** explainer devices · sorting · ecosystem · marquee · أدوات شرح

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-1stnoel-c20a89`
- `kosif-tool/styles/pm-jhylee95-e1152f`
- `kosif-tool/styles/pm-gabrielbuzziv-4ff0c6`
- `kosif-tool/styles/pm-nikolajankovic-ce4ff4`

#### 7. قدرات قريبة في العائلة

- `EXPL-59` رسومات استعارية لكل جملة / Metaphor graphic per spoken claim (ready)
- `EXPL-60` بطاقات المقارنة والتشبيه والقوائم / Trade-off, analogy & checklist cards (seen)
- `EXPL-62` أسلوب الرسومات التقنية / Tech blueprint style (ready)
- `EXPL-63` لوحات ستوري بورد SVG مصغرة / SVG thumbnail storyboards (documented)

### `EXPL-62` — أسلوب الرسومات التقنية / Tech blueprint style

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مظهر الرسم الهندسي: خطوط سماوية وبيضاء رفيعة على شبكة زرقاء داكنة ترسم نفسها، مع خطوط أبعاد وتسميات. / Engineering-drawing look: thin cyan/white line art on a dark blue grid that draws itself.

**متى:** منتجات تقنية، هندسة، «كيف يعمل» / tech products, engineering.

**كيف:** python3 tools/kosif.py scaffold tech-blueprint <dir>; SVG paths on a 24 px grid; draw-on 900–1200 px/s; nodes pop spring d14 s160; camera pans 700–1000 ms cubic-bezier(.65,0,.35,1); stroke 3–4 px, arrowheads 14–18 px, zoom ≤1.8.

**المعاملات:** grid 24 px; 900–1200 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** blueprint · engineering drawing · tech · رسومات تقنية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/tech-blueprint/SKILL.md`
- `kosif-tool/styles/tech-blueprint/STYLE.json`
- `kosif-tool/playbooks/diagrams.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-60` بطاقات المقارنة والتشبيه والقوائم / Trade-off, analogy & checklist cards (seen)
- `EXPL-61` أدوات بصرية للشرح / Explainer visual devices (seen)
- `EXPL-63` لوحات ستوري بورد SVG مصغرة / SVG thumbnail storyboards (documented)
- `EXPL-64` نموذج مجرة الأدلة / Evidence galaxy graph model (idea)

### `EXPL-63` — لوحات ستوري بورد SVG مصغرة / SVG thumbnail storyboards

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مستطيلات ودوائر بسيطة في SVG تبيّن تكوين كل لقطة قبل البناء. / Simple rect/circle SVG thumbnails per shot.

**متى:** اعتماد الخطة مع المستخدم / approving the plan.

**كيف:** write thumbs.svg with one 16:9 or 9:16 frame per shot (subject boxes, text zones, arrows for camera moves) and show it before building.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** storyboard · thumbnails · planning · ستوري بورد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/storyboard-shotlist/SKILL.md:24`

#### 7. قدرات قريبة في العائلة

- `EXPL-61` أدوات بصرية للشرح / Explainer visual devices (seen)
- `EXPL-62` أسلوب الرسومات التقنية / Tech blueprint style (ready)
- `EXPL-64` نموذج مجرة الأدلة / Evidence galaxy graph model (idea)
- `EXPL-G01` قواعد مشهد الشرح الرياضي / Explainer scene grammar (documented)

### `EXPL-64` — نموذج مجرة الأدلة / Evidence galaxy graph model

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سلسلة من أربع عقد: حساب ← دليل ← معيار ← نتيجة، لتقود مرئيًا شبكيًا لتتبع التدقيق / لا يوجد عارض بعد. — A four-node account → evidence → standard → finding model meant to drive a node-link visual; no renderer exists.

**متى:** شرح تتبع الأدلة في التدقيق / audit traceability explainers.

**كيف:** data object with nodes[] and links[] plus traceEvidence(id); render with EXPL-19/17 (hub + data pulses) when needed.

**المعاملات:** 4 nodes, 3 links

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** evidence graph · audit · traceability · تدقيق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/cinema/evidenceGalaxy.js`

#### 7. قدرات قريبة في العائلة

- `EXPL-62` أسلوب الرسومات التقنية / Tech blueprint style (ready)
- `EXPL-63` لوحات ستوري بورد SVG مصغرة / SVG thumbnail storyboards (documented)
- `EXPL-G01` قواعد مشهد الشرح الرياضي / Explainer scene grammar (documented)
- `EXPL-G02` مخطط بنية سحابية بالكود ثم كشفه / Architecture diagram as code, revealed by cluster (documented)

### `EXPL-G01` — قواعد مشهد الشرح الرياضي / Explainer scene grammar

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** فكرة واحدة لكل مشهد: اكتب أو ارسم العنصر عند تقديمه، حوّله عند تغيّر معناه، تتابع بنسبة تأخير للمجموعات، حرّك الكاميرا نحو التفصيلة، واترك وقفة بعد كل خطوة. — One idea per scene: write or draw an element when it is introduced, transform it when its meaning changes, lag groups, move the camera to the detail, and hold a beat after each step.

**متى:** فيديو شرح رياضي أو علمي أو تقني / a maths, science or technical explainer

**كيف:** Grammar: Create/Write (introduce) → Transform (same thing, new form) → FadeOut (done) ; LaggedStart(lag_ratio≈0.1-0.25) for lists; camera frame moves rather than shrinking content; wait 0.5-1 s after each idea; colour = meaning (same quantity, same colour across scenes). Narration first, then animate to the words (words.json).

**المعاملات:** lag_ratio 0.1-0.25; hold 0.5-1 s per idea

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** manim · explainer · laggedstart · scene grammar · 3blue1brown · فيديو شرح · رياضيات · مشهد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-G01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `EXPL-63` لوحات ستوري بورد SVG مصغرة / SVG thumbnail storyboards (documented)
- `EXPL-64` نموذج مجرة الأدلة / Evidence galaxy graph model (idea)
- `EXPL-G02` مخطط بنية سحابية بالكود ثم كشفه / Architecture diagram as code, revealed by cluster (documented)
- `EXPL-U01` قائمة الأساليب الخمسة للموشن بالكود / Five code-rendered motion-graphics styles menu (documented)

### `EXPL-G02` — مخطط بنية سحابية بالكود ثم كشفه / Architecture diagram as code, revealed by cluster

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** اكتب مخطط البنية كودًا (عُقد بأيقونات مزود الخدمة ومجموعات وحواف)، ولّده صورة متجهة، ثم اكشفه مجموعة بعد مجموعة مع السرد. — Write the architecture as code (provider-icon nodes, clusters, edges), render it to a vector image, then reveal it cluster by cluster with the narration.

**متى:** شرح بنية نظام أو تدفق بيانات / explaining a system architecture or data flow

**كيف:** Clusters = boundaries the viewer must understand (VPC, service, team); edges labelled with what flows; render to SVG; give every cluster an id; animate in narration order: cluster outline draws on, then its nodes stagger in (EASE-G03), then edges draw along their direction. Keep ≤ 12 nodes on screen at once; split bigger systems into scenes.

**المعاملات:** ≤ 12 nodes per shot

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** diagrams as code · architecture · cloud · svg · mingrammer · مخطط · بنية · سحابة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-G02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `EXPL-64` نموذج مجرة الأدلة / Evidence galaxy graph model (idea)
- `EXPL-G01` قواعد مشهد الشرح الرياضي / Explainer scene grammar (documented)
- `EXPL-U01` قائمة الأساليب الخمسة للموشن بالكود / Five code-rendered motion-graphics styles menu (documented)
- `EXPL-U02` لقطة التحليل المجمّدة / Frozen analysis beat overlay (documented)

### `EXPL-U01` — قائمة الأساليب الخمسة للموشن بالكود / Five code-rendered motion-graphics styles menu

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied |

**ما هي:** اختر أسلوبًا وسمِّه قبل البناء: Editorial Explainer (ريلز 9:16 بطابع Vox، فحم وورق، لون تمييز أحمر واحد)، AI Film FX (رسوم داخل لقطات مولّدة)، 2D Animated Explainer (ظل 2.5D بشرائح لونية، من تعليق صوتي)، 3D Voxel Animation (زوم لوغاريتمي عبر المقاييس)، Cartoon Music Video. التبديل يغيّر اللوحة والخط والتخطيط والصوت معًا. — Name one of five styles before building; switching swaps palette, type, layouts and sound together.

**متى:** طلب موشن جرافيك مفتوح أو شرح متحرك / an open motion-graphics or explainer request

**كيف:** عند طلب مفتوح اعرض القائمة واسأل؛ ومع لقطات اقترح الأرجح. الأرقام في الملحق §4.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** explainer · شرح · vox · editorial · voxel · cartoon · music video · أسلوب · motion graphics · موشن

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-U01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-G01` قواعد مشهد الشرح الرياضي / Explainer scene grammar (documented)
- `EXPL-G02` مخطط بنية سحابية بالكود ثم كشفه / Architecture diagram as code, revealed by cluster (documented)
- `EXPL-U02` لقطة التحليل المجمّدة / Frozen analysis beat overlay (documented)
- `EXPL-X01` فيديو شرح بـManim / Manim explainer workflow (install)

### `EXPL-U02` — لقطة التحليل المجمّدة / Frozen analysis beat overlay

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied |

**ما هي:** للحظة «التحليل» جمّد إطارًا حادًا واحدًا بدل الإبطاء، عتّمه 30٪ وانزع إشباعه 40٪، ثم شبكة أرض بيضاء بحد داكن، 20–30 نقطة مميزة، و3–4 صناديق بأقواس زوايا سميكة وبطاقات اسم وإحداثيات. — Hold one sharp frame, dim 30 % and desaturate 40 %, then grid, 20–30 feature points and 3–4 bracketed landmark boxes.

**متى:** لقطة تحليل داخل فيديو شرح / an analysis moment in an explainer

**كيف:** أقل وأجرأ أفضل من كثير ورفيع؛ امسحها قبل لقطات الحركة.

**المعاملات:** dim 0.30; desaturate 0.40; 20–30 points; 3–4 boxes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** analysis · تحليل · overlay · hud · freeze · تجميد · explainer

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-U02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-G02` مخطط بنية سحابية بالكود ثم كشفه / Architecture diagram as code, revealed by cluster (documented)
- `EXPL-U01` قائمة الأساليب الخمسة للموشن بالكود / Five code-rendered motion-graphics styles menu (documented)
- `EXPL-X01` فيديو شرح بـManim / Manim explainer workflow (install)

### `EXPL-X01` — فيديو شرح بـManim / Manim explainer workflow

| الحقل | القيمة |
|---|---|
| العائلة | `diagrams-explainers-code` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/diagrams-explainers-code.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `url` |
| الرخصة | MIT (ECC, (c) 2026 Affaan Mustafa); Manim Community MIT |

**ما هي:** لشرح فكرة رياضية أو تقنية: جملة بصرية واحدة، ثم 3–6 مشاهد يثبت كل منها شيئًا واحدًا، ورندر سريع منخفض الجودة قبل الصقل. — For a math or technical idea: one visual thesis sentence, 3–6 scenes each proving one thing, and a fast low-quality render before polish.

**متى:** شرح معادلة أو خوارزمية أو مفهوم علمي — explaining an equation, algorithm or scientific concept.

**كيف:** Outline before code; smoke-render with `manim -ql`; motion explains a state change, reveal progressively; polish typography and pacing; hand off to ffmpeg or Remotion only if it adds value. Deliver a 16:9 MP4, a thumbnail readable at social size and the storyboard. Needs ffmpeg; LaTeX only for TeX formulas; system cairo/pango may need apt packages.

**المعاملات:** 3–6 scenes; -ql smoke render

**التثبيت:** pip install manim

**الوسوم:** manim · explainer · math · animation · شرح · رياضيات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `latex` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:EXPL-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `diagram-layout`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `https://github.com/affaan-m/ECC/tree/main/skills/manim-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `EXPL-U01` قائمة الأساليب الخمسة للموشن بالكود / Five code-rendered motion-graphics styles menu (documented)
- `EXPL-U02` لقطة التحليل المجمّدة / Frozen analysis beat overlay (documented)

