# `charts-data-infographic` — البيانات والرسوم والمواقع (105 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/charts-data-infographic.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/data.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`DATA-01` اختيار المخطط حسب السؤال](#data-01--اختيار-المخطط-حسب-السؤال--chart-choice-by-analytical-question)
- [`DATA-02` المسار أم الميل](#data-02--المسار-أم-الميل--line-path-vs-slope-net-change)
- [`DATA-03` اختيار مخطط التوزيع](#data-03--اختيار-مخطط-التوزيع--distribution-chart-choice)
- [`DATA-04` رسم واحد لخلاصة واحدة وقوس القصة](#data-04--رسم-واحد-لخلاصة-واحدة-وقوس-القصة--one-insight-per-chart--data-story-arc)
- [`DATA-05` صفر حقيقي ومقياس موحد](#data-05--صفر-حقيقي-ومقياس-موحد--true-zero-baseline--shared-scale)
- [`DATA-06` أمانة المقاييس: المساحة واللوغاريتم والتطبيع](#data-06--أمانة-المقاييس-المساحة-واللوغاريتم-والتطبيع--scale-honesty-area-log-normalization)
- [`DATA-07` أشكال ممنوعة أو خطرة](#data-07--أشكال-ممنوعة-أو-خطرة--forbidden-and-risky-chart-forms)
- [`DATA-08` قواعد الرسم الدائري](#data-08--قواعد-الرسم-الدائري--pie-rules)
- [`DATA-09` المفقود ليس صفرًا](#data-09--المفقود-ليس-صفرًا--missing-zero-and-censored-are-different)
- [`DATA-10` لا أرقام مخترعة: مصدر أو «توضيحي»](#data-10--لا-أرقام-مخترعة-مصدر-أو-توضيحي--no-invented-figures-source-line-or-illustrative)
- [`DATA-100` تخطيطات إنفوجرافيك العمليات](#data-100--تخطيطات-إنفوجرافيك-العمليات--process-infographic-layouts)
- [`DATA-101` الخطوط الزمنية المتحركة](#data-101--الخطوط-الزمنية-المتحركة--animated-timelines--gantt-traces)
- [`DATA-102` الشبكات والمحاور والأقواس](#data-102--الشبكات-والمحاور-والأقواس--networks-hubs--brackets)
- [`DATA-103` أدوات التحليل الخلفية](#data-103--أدوات-التحليل-الخلفية--analysis-back-office-skills)
- [`DATA-104` تقاطع فن والأشرطة الطيفية](#data-104--تقاطع-فن-والأشرطة-الطيفية--venn-overlap--spectrum-indicator)
- [`DATA-105` أيقونة مخطط أعمدة](#data-105--أيقونة-مخطط-أعمدة--mini-bar-chart-hero-icon)
- [`DATA-11` التسمية المباشرة بدل وسيلة الإيضاح](#data-11--التسمية-المباشرة-بدل-وسيلة-الإيضاح--direct-labels-over-legends)
- [`DATA-12` الترتيب حسب القيمة ونسبة الأبعاد](#data-12--الترتيب-حسب-القيمة-ونسبة-الأبعاد--sort-by-value--aspect-by-task)
- [`DATA-13` البيانات المتحركة لها وزن واستمرارية](#data-13--البيانات-المتحركة-لها-وزن-واستمرارية--data-in-motion-weight--continuity)
- [`DATA-14` ربط البيانات بقنوات الحركة](#data-14--ربط-البيانات-بقنوات-الحركة--mapping-data-to-motion-channels)
- [`DATA-15` قيمة واحدة تقود الشكل والرقم](#data-15--قيمة-واحدة-تقود-الشكل-والرقم--one-scalar-rule-no-bar-springs)
- [`DATA-16` اتجاه المحاور في العربية](#data-16--اتجاه-المحاور-في-العربية--rtl-chart-axis-conventions)
- [`DATA-17` أحجام نصوص الرسوم](#data-17--أحجام-نصوص-الرسوم--chart-type-sizes)
- [`DATA-18` نبضة التمييز وهرمية التركيز](#data-18--نبضة-التمييز-وهرمية-التركيز--highlight-pulse--focus-hierarchy)
- [`DATA-19` العدّاد التصاعدي بأرقام ثابتة العرض](#data-19--العدّاد-التصاعدي-بأرقام-ثابتة-العرض--tabular-count-up-counter)
- [`DATA-20` قالب stat-counter: رقم مع حلقة](#data-20--قالب-stat-counter-رقم-مع-حلقة--stat-counter-template-count--drawn-ring)
- [`DATA-21` عداد الأسطوانة (أودوميتر)](#data-21--عداد-الأسطوانة-أودوميتر--odometer-digit-roll)
- [`DATA-22` العدّاد المتخلخل والوميض](#data-22--العدّاد-المتخلخل-والوميض--scramble--flicker-counter)
- [`DATA-23` عدّاد يكبر مع قيمته ونبضة الهبوط](#data-23--عدّاد-يكبر-مع-قيمته-ونبضة-الهبوط--count-up-with-growing-scale--landing-punch)
- [`DATA-24` ظهور الرقم بضبابية ورفع](#data-24--ظهور-الرقم-بضبابية-ورفع--number-pop-in-with-blur--lift)
- [`DATA-25` تنسيق الأرقام المختصر والمحلي](#data-25--تنسيق-الأرقام-المختصر-والمحلي--compact--locale-number-formatting)
- [`DATA-26` عدّاد يتلوّن مع تصاعد المشكلة](#data-26--عدّاد-يتلوّن-مع-تصاعد-المشكلة--threshold-colour-escalation-counter)
- [`DATA-27` عدّاد التكلفة التراكمي](#data-27--عدّاد-التكلفة-التراكمي--cost-stack-accumulation-counter)
- [`DATA-28` عدّادات HUD والسنوات والمسافة](#data-28--عدّادات-hud-والسنوات-والمسافة--hud-year--distance-counters)
- [`DATA-29` الرقم المنطوق يصبح حلقة ساعة](#data-29--الرقم-المنطوق-يصبح-حلقة-ساعة--spoken-number--clock-ring-motif)
- [`DATA-30` شطب القيمة واستبدالها](#data-30--شطب-القيمة-واستبدالها--strike-and-replace-value)
- [`DATA-31` حاسبة حيّة بشريط تمرير](#data-31--حاسبة-حيّة-بشريط-تمرير--slider-driven-live-calculator)
- [`DATA-32` أرقام KPI بتدرج أو نيون](#data-32--أرقام-kpi-بتدرج-أو-نيون--gradient-clipped--neon-kpi-numerals)
- [`DATA-33` عدّاد حي فوق اللقطات](#data-33--عدّاد-حي-فوق-اللقطات--live-stat-over-footage)
- [`DATA-34` كومة أرقام الضرر](#data-34--كومة-أرقام-الضرر--mmo-damage-number-stack)
- [`DATA-35` نمو الأعمدة المتدرج](#data-35--نمو-الأعمدة-المتدرج--staggered-bar-growth)
- [`DATA-36` أعمدة أفقية مرتبة مع تمييز واحد](#data-36--أعمدة-أفقية-مرتبة-مع-تمييز-واحد--ranked-horizontal-bars-with-one-highlight)
- [`DATA-37` سباق الأعمدة](#data-37--سباق-الأعمدة--bar-chart-race)
- [`DATA-38` أعمدة مجمّعة أو مكدّسة مع خط](#data-38--أعمدة-مجمّعة-أو-مكدّسة-مع-خط--grouped--stacked-columns--line)
- [`DATA-39` مخطط الشلال (الجسر)](#data-39--مخطط-الشلال-الجسر--waterfall--bridge-chart)
- [`DATA-40` شريط النسب المقسّم (كبسولة)](#data-40--شريط-النسب-المقسّم-كبسولة--proportional-split-bar-segmented-pill)
- [`DATA-41` زووم لوغاريتمي داخل شريحة](#data-41--زووم-لوغاريتمي-داخل-شريحة--log-domain-zoom-into-a-slice)
- [`DATA-42` أعمدة بفترات ثقة](#data-42--أعمدة-بفترات-ثقة--bars-with-interval-whiskers)
- [`DATA-43` مقاييس وأشرطة تقدم بلون الحكم](#data-43--مقاييس-وأشرطة-تقدم-بلون-الحكم--verdict-coloured-meters--rtl-safe-progress)
- [`DATA-44` أشرطة مقسّمة إلى خانات](#data-44--أشرطة-مقسّمة-إلى-خانات--segmented--dotted-meters)
- [`DATA-45` سباق المقارنة والسرعة](#data-45--سباق-المقارنة-والسرعة--speed--latency-comparison-race)
- [`DATA-46` لوحة احتمالات الكلمة التالية](#data-46--لوحة-احتمالات-الكلمة-التالية--next-token-probability-panel)
- [`DATA-47` ترتيب يتغير والقوائم المرتبة](#data-47--ترتيب-يتغير-والقوائم-المرتبة--rank-swap--ranked-lists)
- [`DATA-48` مخطط أعمدة دائري / شعاعي](#data-48--مخطط-أعمدة-دائري--شعاعي--radial--clockwise-bar-chart)
- [`DATA-49` المضاعفات الصغيرة](#data-49--المضاعفات-الصغيرة--small-multiples)
- [`DATA-50` خط يُرسم مع مساحة ونقاط تقفز](#data-50--خط-يُرسم-مع-مساحة-ونقاط-تقفز--line-draw-on-with-area-fade--dot-pops)
- [`DATA-51` خط يرسمه رأس قلم يحمل العدّاد](#data-51--خط-يرسمه-رأس-قلم-يحمل-العدّاد--pen-tip-counter-line)
- [`DATA-52` منحنى ناعم في Remotion](#data-52--منحنى-ناعم-في-remotion--remotion-smooth-cubic-line)
- [`DATA-53` مؤشر قراءة متحرك على المخطط](#data-53--مؤشر-قراءة-متحرك-على-المخطط--chart-scrub-readout-playhead)
- [`DATA-54` خط/مساحة مع مؤشر تقاطع](#data-54--خطمساحة-مع-مؤشر-تقاطع--skcharts-linearea-with-crosshair)
- [`DATA-55` الخطوط المصغرة](#data-55--الخطوط-المصغرة--sparklines--micro-charts)
- [`DATA-56` صعود ثم انهيار](#data-56--صعود-ثم-انهيار--rise-then-crash-line-metaphor)
- [`DATA-57` الشموع وشريط الأسعار](#data-57--الشموع-وشريط-الأسعار--candlesticks--price-ticker)
- [`DATA-58` طبقة التعليقات والإبراز](#data-58--طبقة-التعليقات-والإبراز--annotation--highlight-layer)
- [`DATA-59` تحوّل المخططات](#data-59--تحوّل-المخططات--chart-morph-bars--donut--line--scatter)
- [`DATA-60` رسم بياني بخط اليد](#data-60--رسم-بياني-بخط-اليد--hand-drawn-axis-plot)
- [`DATA-61` مروحة مونت كارلو وعدم اليقين](#data-61--مروحة-مونت-كارلو-وعدم-اليقين--monte-carlo-fan--uncertainty)
- [`DATA-62` هيستوغرام نقاط يصير منحنى جرس](#data-62--هيستوغرام-نقاط-يصير-منحنى-جرس--dot-histogram-resolving-to-a-bell-curve)
- [`DATA-63` رسم الدوال والمشتقة حيًّا](#data-63--رسم-الدوال-والمشتقة-حيًّا--live-function--derivative-tracer)
- [`DATA-64` راكب على خط المخطط](#data-64--راكب-على-خط-المخطط--glyph-riding-the-chart-path)
- [`DATA-65` حقل خطوط الجبال](#data-65--حقل-خطوط-الجبال--ridge-line-wave-field)
- [`DATA-66` مبعثر الحد الفعّال](#data-66--مبعثر-الحد-الفعّال--scatter-with-frontier-curve)
- [`DATA-67` حلقة التقدم المخروطية](#data-67--حلقة-التقدم-المخروطية--conic-gradient-progress-ring)
- [`DATA-68` دونات بخدعة المحيط 100](#data-68--دونات-بخدعة-المحيط-100--donut-via-r--15915-dasharray)
- [`DATA-69` مسح الدائرة بزاوية واحدة](#data-69--مسح-الدائرة-بزاوية-واحدة--pie-sweep-one-eased-angle)
- [`DATA-70` دونات متوهجة مع قائمة](#data-70--دونات-متوهجة-مع-قائمة--glowing-donut-with-legend)
- [`DATA-71` حلقة قياس مع عدّاد متزامن](#data-71--حلقة-قياس-مع-عدّاد-متزامن--arc-gauge-with-synced-counter)
- [`DATA-72` مقاييس HUD الدائرية](#data-72--مقاييس-hud-الدائرية--hud-radial-gauges)
- [`DATA-73` مقياس السائل والمنسوب](#data-73--مقياس-السائل-والمنسوب--liquid-fill--level-gauges)
- [`DATA-74` تعبئة النجوم والتقييم](#data-74--تعبئة-النجوم-والتقييم--star-rating-fill)
- [`DATA-75` رادار المسح](#data-75--رادار-المسح--radar-sweep-with-pings)
- [`DATA-76` نصف دائرة البرلمان وحلقة النقاط](#data-76--نصف-دائرة-البرلمان-وحلقة-النقاط--parliament-hemicycle--dot-ring)
- [`DATA-77` مخطط الوافل: 100 نقطة](#data-77--مخطط-الوافل-100-نقطة--waffle--100-dots-with-synced-percent)
- [`DATA-78` مصفوفة الوحدات: نقطة لكل عنصر](#data-78--مصفوفة-الوحدات-نقطة-لكل-عنصر--unit-dot-matrix-one-dot-per-item)
- [`DATA-79` مقياس إلى شيء مألوف](#data-79--مقياس-إلى-شيء-مألوف--scale-to-a-familiar-object)
- [`DATA-80` خريطة حرارية تقويمية](#data-80--خريطة-حرارية-تقويمية--calendar-heatmap-grid)
- [`DATA-81` خريطة المخاطر 3×3 بأربع درجات](#data-81--خريطة-المخاطر-33-بأربع-درجات--33-risk-heatmap-with-4-step-scale)
- [`DATA-82` جدول حرارة الصفوف × الأعمدة](#data-82--جدول-حرارة-الصفوف--الأعمدة--matrix-intensity-table)
- [`DATA-83` مخطط بنفورد للرقم الأول](#data-83--مخطط-بنفورد-للرقم-الأول--benford-first-digit-chart)
- [`DATA-84` جدول يتكشف صفًّا صفًّا](#data-84--جدول-يتكشف-صفًّا-صفًّا--progressive-table--status-pills)
- [`DATA-85` تشريح بطاقة المؤشر](#data-85--تشريح-بطاقة-المؤشر--kpi-card-anatomy)
- [`DATA-86` ثلاثية بطاقات الأرقام والإثبات](#data-86--ثلاثية-بطاقات-الأرقام-والإثبات--stat-tile-trio--proof-cards)
- [`DATA-87` افتتاحية الرقم البطل](#data-87--افتتاحية-الرقم-البطل--hero-number-opener-card)
- [`DATA-88` سجل HyperFrames للبيانات](#data-88--سجل-hyperframes-للبيانات--hyperframes-data-registry-components--blocks)
- [`DATA-89` مخططات مشاهد البيانات في HyperFrames](#data-89--مخططات-مشاهد-البيانات-في-hyperframes--hyperframes-data-blueprints--categories)
- [`DATA-90` ستايل الإنفوجرافيك بأسلوب أبل](#data-90--ستايل-الإنفوجرافيك-بأسلوب-أبل--keynote-infographic-style)
- [`DATA-91` ستايل البيانات المتحركة الداكن](#data-91--ستايل-البيانات-المتحركة-الداكن--data-in-motion-dark-style)
- [`DATA-92` لوحات ألوان الرسوم](#data-92--لوحات-ألوان-الرسوم--chart-palettes-categorical-sequential-semantic)
- [`DATA-93` رموز بطاقات البيانات التقنية](#data-93--رموز-بطاقات-البيانات-التقنية--tech-doc-data-card-tokens)
- [`DATA-94` لوحة التوأم الإنشائي](#data-94--لوحة-التوأم-الإنشائي--structural-twin-dashboard--utilisation-ramp)
- [`DATA-95` ملف إكسل برسوم أصلية](#data-95--ملف-إكسل-برسوم-أصلية--excel-workbook-with-native-charts)
- [`DATA-96` مكتبات الرسوم كإطارات فيديو](#data-96--مكتبات-الرسوم-كإطارات-فيديو--chart-libraries-as-video-frames)
- [`DATA-97` مشاهد بسمة للبيانات وقوالب أفلامها](#data-97--مشاهد-بسمة-للبيانات-وقوالب-أفلامها--basma-chart-scenes--data-film-templates)
- [`DATA-98` إنفوجرافيك مولَّد مستند إلى بحث](#data-98--إنفوجرافيك-مولَّد-مستند-إلى-بحث--search-grounded-infographic-generation)
- [`DATA-99` مشاهد السرد بالتمرير كبيانات](#data-99--مشاهد-السرد-بالتمرير-كبيانات--scrollytelling-scenes-as-data)

## البطاقات / cards

### `DATA-01` — اختيار المخطط حسب السؤال / Chart choice by analytical question

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر شكل الرسم من العلاقة التي تعرضها لا من الذوق: اتجاه، ترتيب، تركيب، توزيع، ارتباط، تدفق أو هدف. / Pick the chart from the relationship shown: trend, ranking, composition, distribution, correlation, flow or target.

**متى:** حين يسأل المستخدم أي نوع رسم بياني يناسب بياناته: اتجاه أو ترتيب أو توزيع أو تدفق / when the user asks which chart type fits the data: trend, ranking, composition, distribution or flow

**كيف:** Lookup: trend → line (area only if cumulative); compare categories → vertical bars, many categories → horizontal bars or lollipop; ranking → sorted horizontal bars; two periods → slope; part-to-whole → stacked bar / waffle / (pie ≤5); composition over time → stacked area; distribution → histogram/strip; correlation → scatter; flow → sankey/arrows; target → bullet/progress. Video rule: comparison = bars, trend = line, share = stacked bar (data-in-motion skill).

**المعاملات:** ≤6–8 categorical hues; pie <6 slices (video: ≤3–5)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** اختيار المخطط · chart choice · dataviz · سؤال · رسم بياني · تشارت · نوع المخطط · chart type · which chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/references/chart-selection-patterns.md`
- `100-superskills/skills/data-in-motion/SKILL.md`
- `100-superskills/skills/dashboards-dataviz/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-02` المسار أم الميل / Line path vs slope net-change (documented)
- `DATA-03` اختيار مخطط التوزيع / Distribution chart choice (documented)

### `DATA-02` — المسار أم الميل / Line path vs slope net-change

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سؤال «كيف تغيّر؟» له جوابان: الرحلة كاملة (خط) أو البداية مقابل النهاية لكل سلسلة (ميل). / 'How did it change' is either the full journey (line) or start-vs-end per series (slope chart).

**متى:** حين يريد المستخدم إظهار التغير بين فترتين أو انقلاب الترتيب بدل الرحلة الكاملة / when showing net change or rank flips between two periods instead of the full journey

**كيف:** Journey (dips, spikes, when) → draw the line left→right; net change or rank flips → slope chart: two vertical axes, one segment per series, signed change labelled at the right end; draw segments with 60–80 ms stagger, highlight one in accent, grey the rest.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** slope · ميل · line · تغير · قبل وبعد · مقارنة فترتين · تغير صافي · slope chart · before after

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2957-posthog/12277-choosing-trend-or-slope-view/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-01` اختيار المخطط حسب السؤال / Chart choice by analytical question (documented)
- `DATA-03` اختيار مخطط التوزيع / Distribution chart choice (documented)
- `DATA-04` رسم واحد لخلاصة واحدة وقوس القصة / One insight per chart & data story arc (documented)

### `DATA-03` — اختيار مخطط التوزيع / Distribution chart choice

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طابق مخطط التوزيع مع السؤال (الشكل، الشواذ، الانتشار، المركز) واعرض النقاط الخام متى أمكن. / Match the distribution view to shape/outliers/spread/center and show raw points when feasible.

**متى:** حين يطلب المستخدم عرض توزيع القيم أو الشواذ أو الانتشار لمجموعة أو عدة مجموعات / when the user wants to show how values spread or where outliers sit across one or more groups

**كيف:** One group: histogram ≈30 bins with white edges + dashed mean/median lines; several groups: box/violin/strip; many distributions: small multiples not stacking; never a mean-only bar when spread is the story. Animate bins rising left→right 30–40 ms stagger, then draw the median line.

**المعاملات:** bins=30; mean/median dashed 1.5 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** histogram · توزيع · box plot · مدرج تكراري · القيم الشاذة · انتشار · violin · outliers

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/distribution-and-summary-choices.md`

#### 7. قدرات قريبة في العائلة

- `DATA-01` اختيار المخطط حسب السؤال / Chart choice by analytical question (documented)
- `DATA-02` المسار أم الميل / Line path vs slope net-change (documented)
- `DATA-04` رسم واحد لخلاصة واحدة وقوس القصة / One insight per chart & data story arc (documented)
- `DATA-05` صفر حقيقي ومقياس موحد / True-zero baseline & shared scale (documented)

### `DATA-04` — رسم واحد لخلاصة واحدة وقوس القصة / One insight per chart & data story arc

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اكتب الخلاصة جملةً واحدة واجعلها آخر ما يُقرأ، ورتّب المشاهد: صدمة → خط أساس → بناء → ذروة → دعوة. / Write the insight as one sentence, make it the last thing read; arc: hook → baseline → build → climax → call to action.

**متى:** عند التخطيط لفيديو بيانات يحتاج خلاصة واحدة لكل رسم وتسلسلًا قصصيًا من الصدمة إلى الذروة / when planning a data video that needs one takeaway per chart and a hook-to-climax story order

**كيف:** PLAN.md gets one sentence per chart ('sales doubled after March'); three questions = three charts, never overlays. Map arc stages to chart states: baseline chart → highlighted delta → annotated climax. If nobody would act differently after the number, show the sentence instead.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** insight · خلاصة · story arc · قصة البيانات · سرد بالبيانات · رسالة الرسم · حكاية الأرقام · data storytelling · takeaway

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:11`
- `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-02` المسار أم الميل / Line path vs slope net-change (documented)
- `DATA-03` اختيار مخطط التوزيع / Distribution chart choice (documented)
- `DATA-05` صفر حقيقي ومقياس موحد / True-zero baseline & shared scale (documented)
- `DATA-06` أمانة المقاييس: المساحة واللوغاريتم والتطبيع / Scale honesty: area, log, normalization (documented)

### `DATA-05` — صفر حقيقي ومقياس موحد / True-zero baseline & shared scale

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأعمدة والمساحات تبدأ من صفر حقيقي، والخط المقطوع يطبع مداه وعلامة كسر، والرسوم المتقارنة تشترك في مقياس ووحدة. / Bars/areas start at a true zero; a truncated line axis prints its range and a break mark; compared charts share scale and unit.

**متى:** حين تُرسم أعمدة أو رسوم متقارنة ويجب ألا يضلل المحور المقطوع أو اختلاف المقياس / when bars or compared charts must not mislead through a cut axis or mismatched scales

**كيف:** Anchor bars at the baseline (transform-origin bottom, scaleY 0→1); x spacing proportional to real time with gaps visible (MG-042); same y-limits across panels; unit printed on the axis or beside the number (٪, ر.س, k), never left to narration.

**المعاملات:** bars from 0; MG-041 7 s: 0–1 axis, 1–3 grow, 3–7 read

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** baseline · صفر · axis · مقياس · محور مقطوع · وحدة القياس · تضليل · truncated axis · shared scale

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:17-18`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`
- `kosif-tool/styles/pm-ceowinkz-7c776b/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DATA-03` اختيار مخطط التوزيع / Distribution chart choice (documented)
- `DATA-04` رسم واحد لخلاصة واحدة وقوس القصة / One insight per chart & data story arc (documented)
- `DATA-06` أمانة المقاييس: المساحة واللوغاريتم والتطبيع / Scale honesty: area, log, normalization (documented)
- `DATA-07` أشكال ممنوعة أو خطرة / Forbidden and risky chart forms (documented)

### `DATA-06` — أمانة المقاييس: المساحة واللوغاريتم والتطبيع / Scale honesty: area, log, normalization

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الفقاعة والأيقونة تُرمَّز بالمساحة، والمحور اللوغاريتمي يُعلَن، والقيم المطبَّعة تذكر صيغتها. / Bubble/icon size encodes value by area, log axes are announced, normalized values state their formula.

**متى:** عند تحجيم الفقاعات أو الأيقونات بالقيمة أو استخدام محور لوغاريتمي أو قيم مطبعة / when sizing bubbles or icons by value, using a log axis or showing normalized values

**كيف:** r = sqrt(value)·k, never linear radius; label log base and zero handling; name the interval (SD/SE/CI) and n; disclose smoothing window and bin edges; never compare length with area without converting (MG-050).

**المعاملات:** r ∝ √value

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** log · area · sqrt · أمانة · فقاعات · لوغاريتمي · تطبيع · bubble size · normalization

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/SKILL.md`
- `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/references/publication_guidelines.md`

#### 7. قدرات قريبة في العائلة

- `DATA-04` رسم واحد لخلاصة واحدة وقوس القصة / One insight per chart & data story arc (documented)
- `DATA-05` صفر حقيقي ومقياس موحد / True-zero baseline & shared scale (documented)
- `DATA-07` أشكال ممنوعة أو خطرة / Forbidden and risky chart forms (documented)
- `DATA-08` قواعد الرسم الدائري / Pie rules (documented)

### `DATA-07` — أشكال ممنوعة أو خطرة / Forbidden and risky chart forms

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قائمة سوداء قصيرة: لا ثلاثي أبعاد زخرفي، لا محورين مزدوجين مخادعين، لا أعمدة مكدسة كثيرة الشرائح، ولا لوحات ويب. / Blacklist: no decorative 3D, no deceptive dual axes, no many-segment stacks, no web dashboard patterns.

**متى:** قبل اعتماد شكل الرسم لتجنب الثلاثي الأبعاد الزخرفي والمحورين المزدوجين والدوائر المزدحمة / before settling on a chart form, to avoid decorative 3D, deceptive dual axes and crowded pies

**كيف:** Reject: 3D bars/pies; pie/donut beyond 3–5 slices (use bars); dual axis unless both labelled and not engineered to fake correlation (prefer two aligned panels); stacked bars with many middle segments (small multiples); 6-panel dashboards, gridline forests, detached legends, raw chart-library default output; no animated pie (data-in-motion style).

**المعاملات:** pie ≤3 slices for video; bars baseline 0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ممنوع · 3D · dual axis · forbidden · أخطاء الرسوم · محور مزدوج · رسم مضلل · chart mistakes · misleading chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`
- `kosif-atlas/skills/2354-power-platform/9080-report-visualization-design/SKILL.md`
- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/data-in-motion.md`
- `100-superskills/skills/trend-animation-styles/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `DATA-05` صفر حقيقي ومقياس موحد / True-zero baseline & shared scale (documented)
- `DATA-06` أمانة المقاييس: المساحة واللوغاريتم والتطبيع / Scale honesty: area, log, normalization (documented)
- `DATA-08` قواعد الرسم الدائري / Pie rules (documented)
- `DATA-09` المفقود ليس صفرًا / Missing, zero and censored are different (documented)

### `DATA-08` — قواعد الرسم الدائري / Pie rules

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خمس شرائح كحد أقصى مع «أخرى»، مرتبة من الساعة 12 مع عقارب الساعة، والشرائح المتقاربة تصبح عمودًا مكدسًا. / Max five slices + 'other', sorted from 12 o'clock clockwise; near-equal slices become a stacked bar.

**متى:** حين يطلب المستخدم رسمًا دائريًا لعرض نسب أجزاء من كل / when the user asks for a pie chart to show shares of a whole

**كيف:** Sort by size; slices within 5 points of each other → stacked bar (the eye cannot rank close angles); only use a ring when there is a fixed whole (MG-047).

**المعاملات:** ≤5 slices; within 5 pts → stacked bar

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pie · دائري · slices · رسم الفطيرة · نسب مئوية · أجزاء من كل · pie chart · part to whole

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:21`
- `kosif-tool/playbooks/charts.md:193`

#### 7. قدرات قريبة في العائلة

- `DATA-06` أمانة المقاييس: المساحة واللوغاريتم والتطبيع / Scale honesty: area, log, normalization (documented)
- `DATA-07` أشكال ممنوعة أو خطرة / Forbidden and risky chart forms (documented)
- `DATA-09` المفقود ليس صفرًا / Missing, zero and censored are different (documented)
- `DATA-10` لا أرقام مخترعة: مصدر أو «توضيحي» / No invented figures: source line or 'illustrative' (documented)

### `DATA-09` — المفقود ليس صفرًا / Missing, zero and censored are different

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الفجوة في البيانات تبدو فجوة: لا صفر ولا خط موصول بصمت. / Gaps must look like gaps, not zeros or silently connected lines.

**متى:** حين تحتوي البيانات على قيم مفقودة أو فترات بلا تسجيل ويجب ألا تظهر كأصفار / when the data has missing values or unrecorded periods that must not be drawn as zeros

**كيف:** Break the path at missing points (separate M commands), or draw interpolated stretches dashed and labelled; no-data cells in neutral #777777; state exclusions in the source note; empty source → empty-state text, never sample numbers.

**المعاملات:** missing colour #777777

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** missing · مفقود · gaps · بيانات ناقصة · قيم فارغة · فجوات · null values · no data

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/missingness-and-confidence.md`

#### 7. قدرات قريبة في العائلة

- `DATA-07` أشكال ممنوعة أو خطرة / Forbidden and risky chart forms (documented)
- `DATA-08` قواعد الرسم الدائري / Pie rules (documented)
- `DATA-10` لا أرقام مخترعة: مصدر أو «توضيحي» / No invented figures: source line or 'illustrative' (documented)
- `DATA-100` تخطيطات إنفوجرافيك العمليات / Process infographic layouts (documented)

### `DATA-10` — لا أرقام مخترعة: مصدر أو «توضيحي» / No invented figures: source line or 'illustrative'

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل رقم من سجل أو مصدر، والبيانات الحقيقية لها سطر مصدر، والمخترعة تُوسم «توضيحية» داخل الإطار، والمصدر الفارغ يعرض حالة فارغة. / Every figure comes from a record; real data carries a source line, invented data says 'illustrative' in-frame; empty sources show an empty state.

**متى:** حين تُعرض أرقام في فيديو أو إنفوجرافيك ويجب ذكر مصدرها أو وسمها بأنها توضيحية / when figures appear in a video or infographic and need a source line or an 'illustrative' label

**كيف:** Source line in the corner (mono 18–22 px, 60% ink); MG-044 counter stops then shows unit and source; empty-state copy: 'لا توجد بيانات مسجلة لهذه الفترة بعد.'; AI-generated infographics (DATA-98) are unverified until every number is re-set in code.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** source · مصدر · honesty · توضيحي · سطر المصدر · أرقام وهمية · حالة فارغة · citation · empty state

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`
- `kosif-earth-ci-fork/ui/components/charts.js:1`
- `kosif-tool/playbooks/charts.md:23`
- `kosif-tool/playbooks/charts.md:25`

#### 7. قدرات قريبة في العائلة

- `DATA-08` قواعد الرسم الدائري / Pie rules (documented)
- `DATA-09` المفقود ليس صفرًا / Missing, zero and censored are different (documented)
- `DATA-100` تخطيطات إنفوجرافيك العمليات / Process infographic layouts (documented)
- `DATA-101` الخطوط الزمنية المتحركة / Animated timelines & Gantt traces (seen)

### `DATA-100` — تخطيطات إنفوجرافيك العمليات / Process infographic layouts

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | source package declared copyleft/WTFPL-like (x4919): use the ideas only, write your own code |

**ما هي:** إنفوجرافيك خطوات مرقمة: خط زمني عمودي، مراحل أفقية أو شبكة بطاقات، يُرندر HTML إلى صورة. / Numbered-step infographics as vertical timeline, horizontal phases or a card grid, HTML rendered to PNG.

**متى:** حين يطلب المستخدم صورة إنفوجرافيك لخطوات مرقمة كخط زمني أو مراحل أو بطاقات / when the user asks for a numbered-steps infographic image as a timeline, phases or card grid

**كيف:** Step = 2–5 word title + <15-word description; 3–4 steps grid, 5–6 vertical timeline, 7–9 vertical with phases, 10+ compact; height 630 + 135 per step above 4 (cap 1500) at 1200 px; numbered circle markers 36 px on a 2 px rail. Rebuild from these ideas — do not copy the source code.

**المعاملات:** 1200 × (630…1500); marker 36 px; rail 2 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** process · خطوات · infographic · PNG · مراحل · خطوات العمل · صورة · numbered steps · workflow steps

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-100` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/x4919-visual-gen/x20319-process-infographic/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-09` المفقود ليس صفرًا / Missing, zero and censored are different (documented)
- `DATA-10` لا أرقام مخترعة: مصدر أو «توضيحي» / No invented figures: source line or 'illustrative' (documented)
- `DATA-101` الخطوط الزمنية المتحركة / Animated timelines & Gantt traces (seen)
- `DATA-102` الشبكات والمحاور والأقواس / Networks, hubs & brackets (install)

### `DATA-101` — الخطوط الزمنية المتحركة / Animated timelines & Gantt traces

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط زمني تُرسم موصلاته المتوهجة مع دخول البطاقات، أو نقطة حمراء تنتقل إلى سنة كل فصل، أو أشرطة جانت تنمو بالتتابع. / Timelines whose glowing connectors draw as cards spring in, a red dot hopping to each chapter year, or Gantt bars growing in sequence.

**متى:** حين يريد المستخدم خطًا زمنيًا متحركًا لأحداث أو فصول أو مخطط جانت لمهام بتواريخ / when the user wants an animated timeline of events or chapters, or a Gantt chart of dated tasks

**كيف:** Gantt only when the data has real start/end dates (task grid left, time right, milestones distinct from spans, restrained dependencies, today/deadline line only when it answers a question), else a milestone timeline; MG-042: 0–1 axes, 1–5 draw, 5–8 milestone, x proportional to real time; connectors stroke-dashoffset 600 ms with a 30% blurred duplicate glow; scrubber: 1 px line with ticks, red dot ease inOut 0.8 s, year label bottom-left; execution trace bars grow 200 ms stagger 120 ms, retry in amber; commit timeline: line 900 ms, nodes scale 0→1 150 ms; Arabic timeline with coloured year tags (time axis stays LTR).

**المعاملات:** connector 600 ms; dot hop 0.8 s; bars 200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** timeline · خط زمني · Gantt · milestones · تسلسل زمني · جدول مشروع · محطات · project schedule · chronology

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-101` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10323-gantt-chart-visualization/references/gantt-chart-design-and-use-cases.md`
- `style:pm-aschapmann-131210`
- `style:pm-buildfastwithai-53234e`
- `style:pm-sachaarbonel-8f14f4`

#### 7. قدرات قريبة في العائلة

- `DATA-10` لا أرقام مخترعة: مصدر أو «توضيحي» / No invented figures: source line or 'illustrative' (documented)
- `DATA-100` تخطيطات إنفوجرافيك العمليات / Process infographic layouts (documented)
- `DATA-102` الشبكات والمحاور والأقواس / Networks, hubs & brackets (install)
- `DATA-103` أدوات التحليل الخلفية / Analysis back-office skills (documented)

### `DATA-102` — الشبكات والمحاور والأقواس / Networks, hubs & brackets

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** صور رمزية على حلقة بيضاوية بخطوط منقطة إلى محور مركزي، عناقيد شبكية متوهجة، وشجرة مسابقات تسري فيها نبضات ضوء نحو المركز. / Avatars on an elliptical ring with dashed lines to a hub, glowing network clusters, and tournament brackets with light pulses travelling to the centre.

**متى:** حين يريد المستخدم إظهار مجتمع حول محور مركزي أو شبكة متصلة أو شجرة مسابقات بنبضات ضوء / when the user wants a community around a central hub, a connected network or a tournament bracket with light pulses

**كيف:** Hub scale 0.8→1 back.out, avatars 0→1 back.out with stagger, lines draw after (avatarCount 6–16, label '50k builders'); bracket: lines draw 500 ms, pulses ~600 px/s leaf → final, final node flares with bloom; calendar fan-out: one event chip sends 4 curved Béziers (2 px, 100 ms stagger) to channel badges; week-in-merges: avatar bounces across its row at speed ∝ merged PRs (speed encodes value only with labels — DATA-14).

**المعاملات:** avatars 6–16; pulse ~600 px/s

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add avatar-cloud

**الوسوم:** network · شبكة · hub · bracket · مجتمع · شجرة المسابقات · روابط · tournament · connections

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-102` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/avatar-cloud-network.md`
- `kosif-one/vendor/hyperframes/registry/blocks/week-in-merges/week-in-merges.html`
- `style:pm-madhav-xo-f97f20`
- `style:pm-bizibeast-10f264`

#### 7. قدرات قريبة في العائلة

- `DATA-100` تخطيطات إنفوجرافيك العمليات / Process infographic layouts (documented)
- `DATA-101` الخطوط الزمنية المتحركة / Animated timelines & Gantt traces (seen)
- `DATA-103` أدوات التحليل الخلفية / Analysis back-office skills (documented)
- `DATA-104` تقاطع فن والأشرطة الطيفية / Venn overlap & spectrum indicator (seen)

### `DATA-103` — أدوات التحليل الخلفية / Analysis back-office skills

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مهارات المالك لتحضير البيانات قبل التحريك: SQL، دفاتر بايثون، نماذج إكسل مالية، وتقدير الاحتمالات. / Owner skills for preparing data before animating: SQL, Python notebooks, Excel financial models, forecasting.

**متى:** عند تجهيز البيانات بالاستعلامات أو دفاتر بايثون أو نماذج إكسل قبل تحريكها في رسم / when preparing data with SQL, Python notebooks or Excel models before animating it in a chart

**كيف:** Load the matching SKILL.md (sql-data-analysis, notebooks-python-analysis, excel-financial-models, forecasting-probability) and follow its steps; output a clean CSV/JSON that the chart scene reads at the top of the composition (data arrays first, so values are easy to swap).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** SQL · notebooks · analysis · تحليل · تنظيف البيانات · بايثون · توقعات · csv · data prep

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-103` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/sql-data-analysis/SKILL.md`
- `100-superskills/skills/notebooks-python-analysis/SKILL.md`
- `100-superskills/skills/excel-financial-models/SKILL.md`
- `100-superskills/skills/forecasting-probability/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-101` الخطوط الزمنية المتحركة / Animated timelines & Gantt traces (seen)
- `DATA-102` الشبكات والمحاور والأقواس / Networks, hubs & brackets (install)
- `DATA-104` تقاطع فن والأشرطة الطيفية / Venn overlap & spectrum indicator (seen)
- `DATA-105` أيقونة مخطط أعمدة / Mini bar-chart hero icon (ready)

### `DATA-104` — تقاطع فن والأشرطة الطيفية / Venn overlap & spectrum indicator

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دائرتان بمزج multiply تنزلقان لتلتقيا، وشريط طيفي بعلامة تنزلق إلى الموضع. / Two multiply-blended circles slide together; a rainbow spectrum bar with a sliding marker.

**متى:** حين يريد المستخدم إظهار تقاطع مجموعتين بدائرتين تلتقيان أو موضعًا على شريط طيفي / when the user wants two overlapping circles for a shared set, or a marker sliding along a spectrum bar

**كيف:** Venn: mix-blend-mode multiply, 700 ms ease, overlap label appears after contact; spectrum: 20 gradient segments, marker slides with the one-scalar rule and a value label.

**المعاملات:** 700 ms; 20 segments

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** venn · spectrum · طيف · overlap · دوائر متقاطعة · تشابه · مؤشر طيفي · venn diagram · scale marker

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-104` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-rneayan-474bcf`
- `style:pm-reflex-cloud-72ffe5`
- `style:pm-madebyjmayala-b9204d`

#### 7. قدرات قريبة في العائلة

- `DATA-102` الشبكات والمحاور والأقواس / Networks, hubs & brackets (install)
- `DATA-103` أدوات التحليل الخلفية / Analysis back-office skills (documented)
- `DATA-105` أيقونة مخطط أعمدة / Mini bar-chart hero icon (ready)
- `DATA-11` التسمية المباشرة بدل وسيلة الإيضاح / Direct labels over legends (documented)

### `DATA-105` — أيقونة مخطط أعمدة / Mini bar-chart hero icon

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقة متجهة بأربعة أعمدة صاعدة تصلح استعارة مالية/بيانات (بلا بيانات حقيقية). / A vector card with four rising accent bars as a finance/data metaphor (no data binding).

**متى:** حين يحتاج المستخدم أيقونة رسم بياني رمزية لموضوع مالي أو بيانات دون أرقام حقيقية / when a finance or data topic needs a symbolic bar-chart icon with no real numbers

**كيف:** icon(ctx,'chart',r,…) bars height r·(.26 + .35·i); if numbers are shown next to it, replace it with a real chart.

**المعاملات:** 4 bars

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** icon · أيقونة · metaphor · رمز مالي · رسم رمزي · أعمدة صاعدة · chart icon · growth icon

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-105` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `fastify-motion-bro/web/editorial.js:26`

#### 7. قدرات قريبة في العائلة

- `DATA-103` أدوات التحليل الخلفية / Analysis back-office skills (documented)
- `DATA-104` تقاطع فن والأشرطة الطيفية / Venn overlap & spectrum indicator (seen)
- `DATA-11` التسمية المباشرة بدل وسيلة الإيضاح / Direct labels over legends (documented)
- `DATA-12` الترتيب حسب القيمة ونسبة الأبعاد / Sort by value & aspect by task (documented)

### `DATA-11` — التسمية المباشرة بدل وسيلة الإيضاح / Direct labels over legends

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سمِّ السلسلة عند نهاية الخط أو طرف العمود؛ وسيلة الإيضاح المنفصلة تجعل المشاهد يبحث. / Name series at line ends/bar ends; a detached legend makes viewers hunt.

**متى:** حين يحتوي الرسم على عدة سلاسل ويحتاج المشاهد لمعرفة كل خط دون البحث في المفتاح / when a chart has several series and viewers should identify each without hunting a legend

**كيف:** Label in series colour next to the mark; one accent + grey rest so the focal series needs no key; if unavoidable embed the key inside the plot near the data; selective labels (endpoint, extreme, the one figure), never a number on every mark.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** labels · تسمية · legend · مفتاح الرسم · تسميات مباشرة · ليجند · direct labeling · series names

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`
- `kosif-tool/playbooks/charts.md:23`

#### 7. قدرات قريبة في العائلة

- `DATA-104` تقاطع فن والأشرطة الطيفية / Venn overlap & spectrum indicator (seen)
- `DATA-105` أيقونة مخطط أعمدة / Mini bar-chart hero icon (ready)
- `DATA-12` الترتيب حسب القيمة ونسبة الأبعاد / Sort by value & aspect by task (documented)
- `DATA-13` البيانات المتحركة لها وزن واستمرارية / Data-in-motion weight & continuity (documented)

### `DATA-12` — الترتيب حسب القيمة ونسبة الأبعاد / Sort by value & aspect by task

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رتّب الفئات حسب الحجم إلا إن كان لها ترتيب طبيعي، وارسم السلاسل الزمنية عريضة. / Order categories by magnitude unless naturally ordered; draw time series wide.

**متى:** عند ترتيب أعمدة الفئات أو اختيار أبعاد مساحة الرسم لسلسلة زمنية أو مقارنة / when ordering category bars or choosing plot proportions for a time series or comparison

**كيف:** Descending sort (barh: largest on top); months/stages keep natural order; time-series plot area 2:1–3:1; comparisons squarer; same axis range across compared panels.

**المعاملات:** time-series aspect 2:1–3:1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sort · ترتيب · aspect · ترتيب تنازلي · أبعاد الرسم · نسبة العرض · descending order · plot proportions

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-105` أيقونة مخطط أعمدة / Mini bar-chart hero icon (ready)
- `DATA-11` التسمية المباشرة بدل وسيلة الإيضاح / Direct labels over legends (documented)
- `DATA-13` البيانات المتحركة لها وزن واستمرارية / Data-in-motion weight & continuity (documented)
- `DATA-14` ربط البيانات بقنوات الحركة / Mapping data to motion channels (documented)

### `DATA-13` — البيانات المتحركة لها وزن واستمرارية / Data-in-motion weight & continuity

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إحصاءات الفيديو تحتاج وزنًا بصريًا واستمرارًا: كل رقم مع شكل يتناسب معه، والأرقام المتتالية في نفس الفضاء البصري. / Video stats need weight and continuity: pair every number with a proportional visual and keep successive stats in the same space.

**متى:** حين يعرض فيديو عدة إحصاءات متتالية ويحتاج كل رقم شكلًا يوازيه دون قطع بينها / when a video shows several stats in a row and each number needs a matching visual without cuts

**كيف:** Hero numbers 80–120 px (1080p) counting from 0; build bars/counters by hand in SVG/CSS + a timeline (no chart-library output, tables or small legends); morph the previous stat's shape into the next instead of cutting (style:infographic does this for 28 s with no cuts).

**المعاملات:** numbers 80–120 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** data in motion · استمرارية · hero number · إحصائيات فيديو · أرقام متحركة · موشن جرافيك · animated stats · stat sequence

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/data-in-motion.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/data-in-motion.md`
- `style:infographic`

#### 7. قدرات قريبة في العائلة

- `DATA-11` التسمية المباشرة بدل وسيلة الإيضاح / Direct labels over legends (documented)
- `DATA-12` الترتيب حسب القيمة ونسبة الأبعاد / Sort by value & aspect by task (documented)
- `DATA-14` ربط البيانات بقنوات الحركة / Mapping data to motion channels (documented)
- `DATA-15` قيمة واحدة تقود الشكل والرقم / One-scalar rule (no bar springs) (documented)

### `DATA-14` — ربط البيانات بقنوات الحركة / Mapping data to motion channels

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أي خاصية حركة تحمل أي معنى: الكمية للطول واللون والتسمية، والسرعة للاتجاه، والجسيم يجب أن يكون كيانًا أو عيّنة أو حاملًا. / Quantities go to length/colour/labels; speed shows direction; each particle must be an entity, sample, carrier or focus cue.

**متى:** عند تحويل كميات أو تدفقات إلى حركة وجسيمات بحيث تحمل كل خاصية حركة معنى واحدًا / when turning quantities or flows into motion and particles so each motion property carries one meaning

**كيف:** Never encode quantity with speed alone; emission rate may encode volume only if capped and documented; trail length = recency; opacity decay = one meaning (age OR uncertainty); stroke width/saturation may encode era activity (2 px / 40% sat quiet → 6 px / full busy, kloss brief); always a static fallback frame.

**المعاملات:** stroke 2→6 px, saturation 40%→100%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** encoding · particles · قنوات الحركة · flow · ترميز البيانات · جسيمات · حركة البيانات · motion encoding · data mapping

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/webgl-2d-animation-patterns.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md`
- `kosif-tool/styles/pm-kloss-xyz-fe0c31/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DATA-12` الترتيب حسب القيمة ونسبة الأبعاد / Sort by value & aspect by task (documented)
- `DATA-13` البيانات المتحركة لها وزن واستمرارية / Data-in-motion weight & continuity (documented)
- `DATA-15` قيمة واحدة تقود الشكل والرقم / One-scalar rule (no bar springs) (documented)
- `DATA-16` اتجاه المحاور في العربية / RTL chart axis conventions (documented)

### `DATA-15` — قيمة واحدة تقود الشكل والرقم / One-scalar rule (no bar springs)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قيمة مُسهَّلة واحدة تقود طول العمود والعدّاد والتسمية فيتفقون في كل إطار؛ العمود الذي يتجاوز قيمته يكذب. / One eased value drives geometry, counter and label so they agree every frame; an overshooting bar lies.

**متى:** حين يجب أن يتطابق طول العمود والعداد والتسمية في كل إطار دون ارتداد يتجاوز القيمة / when bar length, counter and label must agree every frame with no overshoot past the value

**كيف:** shown = value·p(t); width = shown/max·track; counter text = format(shown). No springs/backOut on data marks (springs are for pills and chrome only). Synchronised set: all charts start on the same frame and finish ≤1200 ms, counters land on the exact figure (quickdesignio brief). (code snippet in references/powers/charts-data-infographic.md)

**المعاملات:** bars 600–800 ms cubic-bezier(.22,1,.36,1); set lands ≤1200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scalar · no spring · تزامن · truth · مزامنة العداد · بدون ارتداد · قيمة واحدة · synced counter · overshoot

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:32`
- `kosif-tool/playbooks/charts.md:127`
- `kosif-tool/styles/pm-quickdesignio-dd93d0/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DATA-13` البيانات المتحركة لها وزن واستمرارية / Data-in-motion weight & continuity (documented)
- `DATA-14` ربط البيانات بقنوات الحركة / Mapping data to motion channels (documented)
- `DATA-16` اتجاه المحاور في العربية / RTL chart axis conventions (documented)
- `DATA-17` أحجام نصوص الرسوم / Chart type sizes (documented)

### `DATA-16` — اتجاه المحاور في العربية / RTL chart axis conventions

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** محور الزمن يبقى من اليسار لليمين حتى في العربية؛ اعكس فقط التخطيطات الفئوية (التسميات يمينًا والأعمدة تنمو يسارًا). / Time axis stays LTR even in RTL; mirror only categorical layouts (labels right, bars grow leftwards).

**متى:** حين يكون نص الرسم البياني بالعربية ويلزم تحديد اتجاه المحاور والأرقام العربية أو اللاتينية / when chart text is Arabic and axis direction and Arabic vs Latin digits must be decided

**كيف:** SVG text with dir='rtl' + unicode-bidi:isolate; one digit system per film (toLocaleString('ar-EG') → ٠–٩, 'ar-u-nu-latn' or 'en-US' → 0–9); ٪ and ر.س follow the number; arrows start right; two-line labels lh ≥1.6; record the choice in STYLE.md; meters anchored inline-end in RTL UIs.

**المعاملات:** lh ≥ 1.6

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** RTL · عربي · axis · اتجاه · من اليمين لليسار · أرقام عربية · رسم عربي · arabic chart · arabic digits

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:189-195`
- `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`
- `kosif-audit-studio/styles.css:718`

#### 7. قدرات قريبة في العائلة

- `DATA-14` ربط البيانات بقنوات الحركة / Mapping data to motion channels (documented)
- `DATA-15` قيمة واحدة تقود الشكل والرقم / One-scalar rule (no bar springs) (documented)
- `DATA-17` أحجام نصوص الرسوم / Chart type sizes (documented)
- `DATA-18` نبضة التمييز وهرمية التركيز / Highlight pulse & focus hierarchy (documented)

### `DATA-17` — أحجام نصوص الرسوم / Chart type sizes

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حدود دنيا لنصوص الرسوم على شاشة الهاتف، وكلها بأرقام ثابتة العرض. / Minimum chart text sizes for phone screens, all tabular figures.

**متى:** حين يُصمم رسم بياني لشاشة الهاتف أو فيديو عمودي ويجب أن تبقى التسميات والأرقام مقروءة / when designing a chart for phone screens or vertical video so labels and numbers stay readable

**كيف:** At 1080 px width: labels ≥28 px, ticks ≥24 px, counters 72–160 px; portrait 9:16 chart ≤920 px wide and ≤45% of frame height, title above, one-line caption below; chrome at 20–30% contrast, data at full contrast; font-variant-numeric: tabular-nums everywhere.

**المعاملات:** labels ≥28 px; ticks ≥24 px; counters 72–160 px; portrait ≤920 px × 45%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sizes · أحجام · tabular-nums · 9:16 · حجم الخط · فيديو عمودي · مقروئية · font size · mobile readability

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:22`
- `kosif-tool/playbooks/charts.md:26`

#### 7. قدرات قريبة في العائلة

- `DATA-15` قيمة واحدة تقود الشكل والرقم / One-scalar rule (no bar springs) (documented)
- `DATA-16` اتجاه المحاور في العربية / RTL chart axis conventions (documented)
- `DATA-18` نبضة التمييز وهرمية التركيز / Highlight pulse & focus hierarchy (documented)
- `DATA-19` العدّاد التصاعدي بأرقام ثابتة العرض / Tabular count-up counter (proven)

### `DATA-18` — نبضة التمييز وهرمية التركيز / Highlight pulse & focus hierarchy

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنصر واحد بكامل الوضوح والباقي 35–45٪، نبضة واحدة ثم ثبات؛ لا تمييزين في وقت واحد. / One element at 100%, the rest at 35–45%, one pulse then hold; never two highlights at once.

**متى:** حين يريد المستخدم لفت النظر إلى عمود أو نقطة واحدة في الرسم مع تعتيم الباقي / when the user wants to draw attention to one bar or point in a chart while dimming the rest

**كيف:** Dim others to 35% over 300 ms; pulse key once 300 ms up / 500 ms down; hold 1200 ms before the next highlight; every final state holds ≥1500 ms; variants seen: verdict stamp slam scale 1.6→1, rot −8°, slight shake over the bars (style:pm-kloss-xyz-15182a); record bar solid amber among grey #555 bars (style:pm-kyonax-on-tech-aabc1d).

**المعاملات:** dim 35% / 300 ms; pulse 300+500 ms; hold ≥1500 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** highlight · تمييز · pulse · stamp · إبراز · تعتيم الباقي · لفت الانتباه · focus · dim others

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:41`
- `style:pm-kloss-xyz-15182a`
- `style:pm-kyonax-on-tech-aabc1d`

#### 7. قدرات قريبة في العائلة

- `DATA-16` اتجاه المحاور في العربية / RTL chart axis conventions (documented)
- `DATA-17` أحجام نصوص الرسوم / Chart type sizes (documented)
- `DATA-19` العدّاد التصاعدي بأرقام ثابتة العرض / Tabular count-up counter (proven)
- `DATA-20` قالب stat-counter: رقم مع حلقة / stat-counter template (count + drawn ring) (proven)

### `DATA-19` — العدّاد التصاعدي بأرقام ثابتة العرض / Tabular count-up counter

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رقم يعدّ من 0 إلى قيمته بتسهيل خروج وأرقام ثابتة العرض ويصل إلى الرقم الدقيق في الإطار الأخير. / A number counts 0 → target with ease-out and tabular figures, landing on the exact value on the last frame.

**متى:** حين يطلب المستخدم رقمًا يعد من الصفر حتى قيمته في فيديو أو موشن جرافيك / when the user wants a number counting up from zero to its value in a video or motion graphic

**كيف:** Canvas/HTML starter: n = round(lerp(0,128, prog(local,0.2,2.6,outQuint))) at 200 px Cairo 900 #ffb86b, direction ltr — rendered here with tools/render_html.cjs --preview (frames 45→103→122→127→128). Owner kit: MOTION.counter(tl, el, from, to, at, dur, {decimals, sep, prefix, suffix, ease}) sets tabular-nums, seek-safe, dur 1.0 s E.out; start near the final value for long numbers. Seen styles: 1.5 s easeOutCubic (alex-prompter), 0→1,284,302 in 900–1200 ms easeOutExpo (sudeepsd). (code snippet in references/powers/charts-data-infographic.md)

**المعاملات:** counters 700–1000 ms ease-out cubic (playbook); 80–160 px; tabular-nums

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** counter · عداد · count-up · tabular-nums · عداد أرقام · رقم يعد · عداد تصاعدي · number animation · counting number

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/starters/html-canvas/index.html:163`
- `kosif-tool/playbooks/charts.md:36`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:227`
- `kosif-studio/motion/kit/motion-kit.js:227`

#### 7. قدرات قريبة في العائلة

- `DATA-17` أحجام نصوص الرسوم / Chart type sizes (documented)
- `DATA-18` نبضة التمييز وهرمية التركيز / Highlight pulse & focus hierarchy (documented)
- `DATA-20` قالب stat-counter: رقم مع حلقة / stat-counter template (count + drawn ring) (proven)
- `DATA-21` عداد الأسطوانة (أودوميتر) / Odometer digit roll (install)

### `DATA-20` — قالب stat-counter: رقم مع حلقة / stat-counter template (count + drawn ring)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard no-charge license (not OSI) for the vendored gsap.min.js |

**ما هي:** قالب موشن عربي: رقم يعدّ بينما تُرسم حلقة بنفس المنحنى، وميض وانضغاط عند الوصول، والتسمية ترتفع. / Arabic-first template: number counts while a ring draws on the same ease, flash + squash on landing, label rises.

**متى:** حين يريد المستخدم مشهدًا جاهزًا لرقم إحصائي يعد مع حلقة تُرسم وتسمية عربية / when the user wants a ready stat scene: a counting number with a drawn ring and an Arabic label

**كيف:** python scripts/mtemplates.py new NAME --template stat-counter --set value=1250 --set label='عميل يثق بنا' --set suffix=+ [--seconds 6 --size 1080x1920 --fps 30] → projects/NAME/index.html; preview in browser; render with motion.py render. Count runs 1.0–2.2 s (35% of D).

**المعاملات:** 6 s; value 1250; suffix '+'; decimals 0; accent #5BD1A5; bg #10233a→#071321; number 15u Cairo 800

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** template · قالب · stat-counter · ring · رقم إحصائي · عداد بحلقة · مشهد جاهز · stat scene · circle counter

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/templates/motion/stat-counter.html`
- `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:42`
- `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:14`

#### 7. قدرات قريبة في العائلة

- `DATA-18` نبضة التمييز وهرمية التركيز / Highlight pulse & focus hierarchy (documented)
- `DATA-19` العدّاد التصاعدي بأرقام ثابتة العرض / Tabular count-up counter (proven)
- `DATA-21` عداد الأسطوانة (أودوميتر) / Odometer digit roll (install)
- `DATA-22` العدّاد المتخلخل والوميض / Scramble / flicker counter (seen)

### `DATA-21` — عداد الأسطوانة (أودوميتر) / Odometer digit roll

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** كل خانة شريط عمودي 0–9 يتدحرج بتأخير لكل خانة وضبابية حركة عمودية، والخانة اليمنى تدور أكثر. / Each digit is a 0–9 strip rolling with per-digit lag and vertical motion blur; lower digits spin more.

**متى:** حين يريد المستخدم عدادًا تتدحرج خاناته كعداد المسافات أو تنقلب كلوحة النتائج / when the user wants digits that roll like an odometer or flip like a scoreboard

**كيف:** Masked column per digit; translateY = −(digit + 10·extraTurns)·lineH, extraTurns grows toward the rightmost digit; filter blur 0→8 px vertical proportional to velocity; leading zeros at 30% opacity; final number gets gradient fill + glow. Scoreboard flip: per-digit flip with 90 ms stagger. Ready-made: HyperFrames number-wheel (spin single\|double\|triple) and slot-machine-roll (result 'A7K', up\|down). (code snippet in references/powers/charts-data-infographic.md)

**المعاملات:** 0→1,000,000 in 4 s expo.out; digit lag 40 ms; blur 0–8 px; roll 1.2–3 s; size ~14vh

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add number-wheel

**الوسوم:** odometer · عداد أسطواني · digit roll · slot · عداد المسافات · تدحرج الأرقام · لوحة النتائج · scoreboard · rolling numbers

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/components/number-wheel/number-wheel.html`
- `kosif-one/vendor/hyperframes/registry/components/slot-machine-roll/slot-machine-roll.html`
- `style:pm-viktoroddy-98c1d8`
- `style:infographic`

#### 7. قدرات قريبة في العائلة

- `DATA-19` العدّاد التصاعدي بأرقام ثابتة العرض / Tabular count-up counter (proven)
- `DATA-20` قالب stat-counter: رقم مع حلقة / stat-counter template (count + drawn ring) (proven)
- `DATA-22` العدّاد المتخلخل والوميض / Scramble / flicker counter (seen)
- `DATA-23` عدّاد يكبر مع قيمته ونبضة الهبوط / Count-up with growing scale & landing punch (install)

### `DATA-22` — العدّاد المتخلخل والوميض / Scramble / flicker counter

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الخانات تتبدل عشوائيًا ثم تثبت من اليسار لليمين حتى القيمة النهائية. / Digits randomise then lock left-to-right into the final value.

**متى:** حين يريد المستخدم أرقامًا تتبدل عشوائيًا ثم تثبت خانة خانة على القيمة النهائية / when the user wants digits that shuffle randomly then lock one by one into the final value

**كيف:** Seeded PRNG (never Math.random in renders) picks digits each frame; lock digit k at t0 + 40·k ms; slight vertical blur on unlocked digits; playbook cap: flicker ≤150 ms if the style is calm.

**المعاملات:** lock 40 ms per digit; ~1 s total; flicker ≤150 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scramble · متخلخل · flicker · أرقام عشوائية · تبديل الأرقام · وميض · random digits · number shuffle

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-adamdesgns-478d6d`
- `style:pm-influencer-seo-ce8c33`
- `kosif-tool/playbooks/charts.md:36`

#### 7. قدرات قريبة في العائلة

- `DATA-20` قالب stat-counter: رقم مع حلقة / stat-counter template (count + drawn ring) (proven)
- `DATA-21` عداد الأسطوانة (أودوميتر) / Odometer digit roll (install)
- `DATA-23` عدّاد يكبر مع قيمته ونبضة الهبوط / Count-up with growing scale & landing punch (install)
- `DATA-24` ظهور الرقم بضبابية ورفع / Number pop-in with blur & lift (install)

### `DATA-23` — عدّاد يكبر مع قيمته ونبضة الهبوط / Count-up with growing scale & landing punch

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** الرقم يكبر في الحجم مع القيمة على نفس المنحنى، ثم نبضة صغيرة عند الهبوط، ويمكن ربط الهبوط بضربة الموسيقى. / The counter scales up with the value on the same ease, then punches on landing; landing can lock to a downbeat.

**متى:** حين يريد المستخدم رقمًا يكبر أثناء العد وينبض عند الوصول، ويمكن ربطه بضربة الموسيقى / when the user wants a counter that grows while counting and punches on landing, optionally on a music beat

**كيف:** Two tweens, same start and same ease: value proxy onUpdate writes Math.round(v).toLocaleString(), and scale START_SCALE→1; landing punch scale 1.04 for 60 ms then back; beat variant counting-punch anchors roll → downbeat (best span 1.0–2.5 s); BPM variant: numeral ticks 0→130 in ~1 s while beat-energy bars grow with 40 ms stagger, current beat bar red, later bars grey (style:pm-ayushunleashed-ece3e3).

**المعاملات:** 700 ms easeOutExpo + 60 ms punch to 1.04

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add count-up

**الوسوم:** punch · نبضة · beat · scale · ضربة الموسيقى · تكبير الرقم · إيقاع · downbeat · bpm

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/counting-dynamic-scale.md`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/counting-punch/scene.html`
- `kosif-one/vendor/hyperframes/registry/components/count-up/count-up.html`
- `kosif-tool/styles/pm-ajith-io-ea7f2d/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DATA-21` عداد الأسطوانة (أودوميتر) / Odometer digit roll (install)
- `DATA-22` العدّاد المتخلخل والوميض / Scramble / flicker counter (seen)
- `DATA-24` ظهور الرقم بضبابية ورفع / Number pop-in with blur & lift (install)
- `DATA-25` تنسيق الأرقام المختصر والمحلي / Compact & locale number formatting (ready)

### `DATA-24` — ظهور الرقم بضبابية ورفع / Number pop-in with blur & lift

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** خانات الرقم تظهر بضبابية وارتفاع وتتابع، والرقم النهائي يأخذ توهجًا ذهبيًا. / Digits pop in with blur, lift and stagger; the final number gets a gold glow.

**متى:** حين يريد المستخدم ظهورًا ناعمًا للرقم بضبابية وارتفاع ثم توهجًا ذهبيًا في النهاية / when the user wants a number to pop in with blur and lift, ending with a gold glow

**كيف:** Pop-in scale .4 + blur 16 px → 1 / 0 px while counting via a seek-safe proxy tween; finish with textShadow 0 0 80px rgba(245,201,122,.75); HyperFrames number-pop-in (value 5.7, unit k, lift close\|standard\|far).

**المعاملات:** 0→1000 in 0.7 s; $0→25,000,000 in 0.9 s; 0→600 in 0.75 s at 330 px

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add number-pop-in

**الوسوم:** pop-in · blur · glow · ظهور · ظهور الأرقام · توهج ذهبي · ضبابية · number reveal · digit stagger

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/projects/whatsapp-motion/projects/success/index.html:226`
- `kosif-one/vendor/hyperframes/registry/components/number-pop-in/number-pop-in.html`
- `style:pm-andginja-333d32`

#### 7. قدرات قريبة في العائلة

- `DATA-22` العدّاد المتخلخل والوميض / Scramble / flicker counter (seen)
- `DATA-23` عدّاد يكبر مع قيمته ونبضة الهبوط / Count-up with growing scale & landing punch (install)
- `DATA-25` تنسيق الأرقام المختصر والمحلي / Compact & locale number formatting (ready)
- `DATA-26` عدّاد يتلوّن مع تصاعد المشكلة / Threshold-colour escalation counter (seen)

### `DATA-25` — تنسيق الأرقام المختصر والمحلي / Compact & locale number formatting

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 1.2K / 3.4M / 5.6B أو ألف/مليون/مليار، مع نظام أرقام واحد للفيلم كله. / 1.2K / 3.4M / 5.6B or ألف/مليون/مليار, with one digit system for the whole film.

**متى:** حين تُعرض أرقام كبيرة تحتاج اختصارًا كألف ومليون ومليار أو اختيار أرقام عربية أو لاتينية / when large numbers need K/M/B shortening or a choice between Arabic and Latin digits

**كيف:** \|v\|≥1e9 → v/1e9 1 decimal + B (مليار); ≥1e6 → M (مليون); ≥1e3 → K (ألف); else thousands separators; percent 1 decimal. Intl.NumberFormat('ar-EG') gives ٠١٢, 'ar-u-nu-latn' keeps 0–9; keep tnum so counting width is stable. (code snippet in references/powers/charts-data-infographic.md)

**المعاملات:** 1 decimal; thresholds 1e3/1e6/1e9

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** format · تنسيق · Intl · ar-EG · مليون · اختصار الأرقام · مليار · فواصل الآلاف · number format · thousands separator

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/1180-token-activity-graph/2788-token-activity-graph/graph.js`
- `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`
- `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md`
- `kosif-tool/playbooks/charts.md:190`

#### 7. قدرات قريبة في العائلة

- `DATA-23` عدّاد يكبر مع قيمته ونبضة الهبوط / Count-up with growing scale & landing punch (install)
- `DATA-24` ظهور الرقم بضبابية ورفع / Number pop-in with blur & lift (install)
- `DATA-26` عدّاد يتلوّن مع تصاعد المشكلة / Threshold-colour escalation counter (seen)
- `DATA-27` عدّاد التكلفة التراكمي / Cost-stack accumulation counter (seen)

### `DATA-26` — عدّاد يتلوّن مع تصاعد المشكلة / Threshold-colour escalation counter

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رقم ضخم يتسارع ولونه ينتقل أبيض → برتقالي → أحمر عند تجاوز العتبات، والكلمة تحته تتبدل. / A giant numeral accelerates while its colour lerps white → orange → red past thresholds; the caption swaps each step.

**متى:** حين يريد المستخدم رقمًا يتصاعد بسرعة ويتحول لونه إلى الأحمر ليوحي بتفاقم مشكلة أو هبوط سعر / when the user wants a fast-climbing number turning red to signal a worsening problem or a falling price

**كيف:** easeInExpo for escalation (not ease-out); colour from threshold stops; falling-price variant: card counts 34.99 → 24.99 over ~2 s with a red '9% AND FALLING' delta while competitor pins pop (scale 0→1, 120 ms).

**المعاملات:** 1 → 5000 over ~3 s; numeral 25% frame height; pins 12–20

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** escalation · تصاعد · threshold colour · price · تفاقم · تحذير · لون أحمر · warning · alarm counter

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-0xfemyn-e114d3`
- `style:pm-ceowinkz-7c776b`

#### 7. قدرات قريبة في العائلة

- `DATA-24` ظهور الرقم بضبابية ورفع / Number pop-in with blur & lift (install)
- `DATA-25` تنسيق الأرقام المختصر والمحلي / Compact & locale number formatting (ready)
- `DATA-27` عدّاد التكلفة التراكمي / Cost-stack accumulation counter (seen)
- `DATA-28` عدّادات HUD والسنوات والمسافة / HUD, year & distance counters (seen)

### `DATA-27` — عدّاد التكلفة التراكمي / Cost-stack accumulation counter

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقات أسعار تسقط واحدة تلو الأخرى وكل قيمة تُضاف إلى عدّاد كبير حتى المجموع، ثم تنهار كلها في منتج واحد. / Price cards drop one by one, each adding to a big counter up to the total, then collapse into one product.

**متى:** حين يريد المستخدم جمع تكاليف أو أسعار متعددة في عداد واحد ثم دمجها في منتج واحد / when the user wants many costs or prices to add up into one total, then collapse into a single product

**كيف:** Card stagger 120 ms with motion blur on drop; counter tweens 300 ms per step; list variant appends a row every 150 ms beside a fixed plan card.

**المعاملات:** card stagger 120 ms; 300 ms per step

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cost · تكلفة · sum · stack · تراكم · مجموع الأسعار · بطاقات الأسعار · total cost · price comparison

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-bizibeast-10f264`
- `style:pm-thayto-dev-44b911`

#### 7. قدرات قريبة في العائلة

- `DATA-25` تنسيق الأرقام المختصر والمحلي / Compact & locale number formatting (ready)
- `DATA-26` عدّاد يتلوّن مع تصاعد المشكلة / Threshold-colour escalation counter (seen)
- `DATA-28` عدّادات HUD والسنوات والمسافة / HUD, year & distance counters (seen)
- `DATA-29` الرقم المنطوق يصبح حلقة ساعة / Spoken number → clock-ring motif (proven)

### `DATA-28` — عدّادات HUD والسنوات والمسافة / HUD, year & distance counters

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عدّاد سنة أو عمر أو عمق أو مسافة مربوط بالزمن أو بموضع الكاميرا، بخط mono في زاوية الإطار. / Year/age/depth/distance counters bound to scene time or camera position, in a mono HUD corner.

**متى:** حين يحتاج المشهد عداد سنوات أو مسافة أو عمق مرتبطًا بالزمن أو حركة الكاميرا في زاوية الإطار / when a scene needs a year, distance or depth readout tied to time or camera movement in a corner

**كيف:** Year roll 2006→2026 in 800 ms easeOut; year = f(cameraX) for position-tied clocks; map-journey: real km by haversine between stops distributed along arc length, toLocaleString, 7 progress dots filling per stop; depth badge flips up on dive, down on return (~15% frame height).

**المعاملات:** 2006→2026 / 800 ms; 7 dots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** HUD · year counter · haversine · مسافة · عداد السنوات · رحلة على الخريطة · عمق · map journey · depth badge

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:map-journey`
- `style:pm-deebeeeff-50fcd0`
- `style:pm-emollick-8661a8`
- `kosif-tool/styles/pm-kloss-xyz-fe0c31/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DATA-26` عدّاد يتلوّن مع تصاعد المشكلة / Threshold-colour escalation counter (seen)
- `DATA-27` عدّاد التكلفة التراكمي / Cost-stack accumulation counter (seen)
- `DATA-29` الرقم المنطوق يصبح حلقة ساعة / Spoken number → clock-ring motif (proven)
- `DATA-30` شطب القيمة واستبدالها / Strike-and-replace value (seen)

### `DATA-29` — الرقم المنطوق يصبح حلقة ساعة / Spoken number → clock-ring motif

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عندما يُقال رقم تظهر بجانب المتحدث حلقة بـ24 علامة وعقرب يدور، وتنتقل إلى تكراره إن تكرر. / When a number is spoken, a 24-tick ring with a sweeping hand appears on the free side of the subject.

**متى:** حين يذكر المتحدث رقمًا في فيديو حديث ويراد إبرازه بحلقة ساعة بجانبه / when a speaker says a number in a talking-head video and it should appear in a clock ring beside them

**كيف:** direct.plan emits motifs [{type:'ring', cx, cy, r, text, t, end}]; cx = free side, cy = eye line; ring drawn 0.9 s power2.inOut via MOTION.drawPath, ticks stagger 0.03 s, accent hand 360° over the span, number 0.95r.

**المعاملات:** r 150 px; 1.4 s; stroke 2.4·k

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** motif · حلقة الساعة · spoken number · talking head · فيديو متحدث · مزامنة الكلام · رقم مسموع · clock ring · speaker overlay

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/motion/direct.py:177`
- `kosif-studio/tests/test_studio.py:910`
- `100-superskills/skills/kosif-montage-motion/templates/directed.html:96`

#### 7. قدرات قريبة في العائلة

- `DATA-27` عدّاد التكلفة التراكمي / Cost-stack accumulation counter (seen)
- `DATA-28` عدّادات HUD والسنوات والمسافة / HUD, year & distance counters (seen)
- `DATA-30` شطب القيمة واستبدالها / Strike-and-replace value (seen)
- `DATA-31` حاسبة حيّة بشريط تمرير / Slider-driven live calculator (seen)

### `DATA-30` — شطب القيمة واستبدالها / Strike-and-replace value

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** القيمة القديمة تُشطب بخط ثم تظهر الجديدة بخط عريض. / The old value gets a strike line, then the new value appears in bold.

**متى:** حين يريد المستخدم شطب قيمة قديمة وإظهار القيمة الجديدة مكانها بخط عريض / when the user wants an old value struck through and replaced by a new one in bold

**كيف:** Strike line scaleX 0→1 over 200 ms from the reading start side (right in Arabic), old value to 40% opacity, new value fades/rises 200 ms.

**المعاملات:** strike 200 ms; new value 200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** strike · شطب · before after · قبل وبعد · القيمة القديمة · خط الشطب · strikethrough · old vs new

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-sachaarbonel-8f14f4`

#### 7. قدرات قريبة في العائلة

- `DATA-28` عدّادات HUD والسنوات والمسافة / HUD, year & distance counters (seen)
- `DATA-29` الرقم المنطوق يصبح حلقة ساعة / Spoken number → clock-ring motif (proven)
- `DATA-31` حاسبة حيّة بشريط تمرير / Slider-driven live calculator (seen)
- `DATA-32` أرقام KPI بتدرج أو نيون / Gradient-clipped & neon KPI numerals (ready)

### `DATA-31` — حاسبة حيّة بشريط تمرير / Slider-driven live calculator

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مؤشر يسحب شريط تمرير، والعدد والمبلغ الكبير محسوبان من نفس التقدم بفواصل آلاف، والمبلغ السنوي تحته. / A cursor drags a slider; the count and the big currency number derive from the same progress.

**متى:** حين يريد المستخدم حاسبة متحركة يسحب فيها مؤشر شريطًا فيتغير العدد والمبلغ معًا / when the user wants an animated calculator where dragging a slider updates the count and amount together

**كيف:** progress p drives thumb x, N = round(p·Nmax), amount = rate·N formatted; drag ~2 s easeInOutCubic; currency conversion variant: value → arrow → counter 0.8 s easeOut.

**المعاملات:** drag ~2 s; $50 × N

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** calculator · حاسبة · slider · currency · حاسبة تفاعلية · تحويل عملات · سحب المؤشر · price calculator · currency conversion

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-paulo-kombucha-96431c`
- `style:pm-jayscambler-3f8889`

#### 7. قدرات قريبة في العائلة

- `DATA-29` الرقم المنطوق يصبح حلقة ساعة / Spoken number → clock-ring motif (proven)
- `DATA-30` شطب القيمة واستبدالها / Strike-and-replace value (seen)
- `DATA-32` أرقام KPI بتدرج أو نيون / Gradient-clipped & neon KPI numerals (ready)
- `DATA-33` عدّاد حي فوق اللقطات / Live stat over footage (seen)

### `DATA-32` — أرقام KPI بتدرج أو نيون / Gradient-clipped & neon KPI numerals

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أرقام المؤشرات مملوءة بتدرج عبر قص النص، أو بتوهج نيون، بأرقام ثابتة العرض. / KPI numerals filled with a gradient via text clipping, or neon-glowed, in tabular figures.

**متى:** حين يريد المستخدم أرقام مؤشرات أداء بتدرج لوني داخل النص أو بتوهج نيون / when the user wants KPI numbers filled with a gradient inside the text or given a neon glow

**كيف:** background: linear-gradient(135deg,#312e81,#6d28d9); background-clip:text; -webkit-text-fill-color:transparent; weight 900; card min-height 124 px with radial corner glow 110 px rgba(99,102,241,.13). Neon variant: extended font, text-shadow 0 0 30px lime, count 2 s ease-out. Keynote variant: vertical gradient #C9F4FF→#64D2FF→#1AA7EC, % smaller at right.

**المعاملات:** clamp(24px,3vw,36px) UI; line-height 1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** gradient text · نيون · KPI · glow · مؤشرات الأداء · نص متدرج · أرقام ملونة · background-clip · metric numbers

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-audit-studio/dashboard-capabilities.css:3`
- `style:pm-marklaunches-3b9492`
- `style:infographic`
- `style:pm-polydao-7a572b`

#### 7. قدرات قريبة في العائلة

- `DATA-30` شطب القيمة واستبدالها / Strike-and-replace value (seen)
- `DATA-31` حاسبة حيّة بشريط تمرير / Slider-driven live calculator (seen)
- `DATA-33` عدّاد حي فوق اللقطات / Live stat over footage (seen)
- `DATA-34` كومة أرقام الضرر / MMO damage-number stack (seen)

### `DATA-33` — عدّاد حي فوق اللقطات / Live stat over footage

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard no-charge license (not OSI) for the vendored gsap.min.js |

**ما هي:** رقم مكثف ضخم يعدّ فوق لقطات معتمة مع شارة LIVE حمراء وتسمية صغيرة، أو بطاقة مقاييس تنزلق بجانب اللقطة. / A big condensed number counts over dimmed footage with a red-dot LIVE pill, or a metrics card slides in beside shrunken footage.

**متى:** حين يريد المستخدم رقمًا كبيرًا يعد فوق لقطات معتمة مع شارة مباشر أو بطاقة مقاييس جانبية / when the user wants a big number counting over dimmed footage with a LIVE pill or a side metrics card

**كيف:** Dim footage 45%; count ~1.2 s easeOutExpo with separators; metrics card: .metric 44 px/600 LTR + 26 px RTL Arabic subline #9aa29d, x 40→0, opacity .4→1, .4 s E.out, stagger .12 s, scramble on '60 fps'.

**المعاملات:** dim 45%; 1.2 s; stagger 120 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** footage · LIVE · overlay · فوق اللقطات · فوق الفيديو · بث مباشر · تعتيم اللقطة · video overlay · metrics card

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-deifosv-04e4d3`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:52`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:123`

#### 7. قدرات قريبة في العائلة

- `DATA-31` حاسبة حيّة بشريط تمرير / Slider-driven live calculator (seen)
- `DATA-32` أرقام KPI بتدرج أو نيون / Gradient-clipped & neon KPI numerals (ready)
- `DATA-34` كومة أرقام الضرر / MMO damage-number stack (seen)
- `DATA-35` نمو الأعمدة المتدرج / Staggered bar growth (install)

### `DATA-34` — كومة أرقام الضرر / MMO damage-number stack

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل ضربة تدفع رقمًا إلى عمود (الأحدث يدفع الباقي) مع مجموع حرج كبير يلمع، بألوان حسب النوع. / Each hit pops a number into a column (newest pushes the rest) plus a big sparkling crit total.

**متى:** حين يريد المستخدم أرقام ضرر متراكمة على طريقة الألعاب مع مجموع ضربة حرجة / when the user wants game-style damage numbers stacking per hit with a big critical total

**كيف:** New hit every 150–250 ms; 4 visible rows; pop scale 1.3→1 in 2 frames; colour by category; total counter rides below.

**المعاملات:** 150–250 ms per hit; 4 rows

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** damage numbers · ألعاب · stack · ضربة حرجة · أرقام الضرر · جيمنج · critical hit · mmo

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-0xevinho-3777d8`

#### 7. قدرات قريبة في العائلة

- `DATA-32` أرقام KPI بتدرج أو نيون / Gradient-clipped & neon KPI numerals (ready)
- `DATA-33` عدّاد حي فوق اللقطات / Live stat over footage (seen)
- `DATA-35` نمو الأعمدة المتدرج / Staggered bar growth (install)
- `DATA-36` أعمدة أفقية مرتبة مع تمييز واحد / Ranked horizontal bars with one highlight (ready)

### `DATA-35` — نمو الأعمدة المتدرج / Staggered bar growth

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Remotion company license (free for individuals and small teams; companies above the threshold need a paid license) |

**ما هي:** أعمدة تنمو من القاعدة بسرعة ثم استقرار طويل، بتدرج يجعل المجموعة تهبط خلال ثانية تقريبًا. / Bars grow from the baseline fast-then-long-settle, staggered so the set lands within ~1 s.

**متى:** حين يطلب المستخدم مخطط أعمدة متحركًا تنمو فيه الأعمدة من القاعدة بالتتابع / when the user asks for an animated bar chart whose bars grow from the baseline one after another

**كيف:** Remotion Bars component in the playbook: interpolate with easeOutQuint ≈ cubic-bezier(.22,1,.36,1), step = min(80, 700/n) ms, RTL bars grow leftwards, value text toLocaleString('ar-EG') counting with the bar. HTML: transform-origin bottom, GSAP scaleY 0→1 only, heights authored in CSS (bar 48 px, gap 14 px, height 280 px); last bar accent. Story-integrated variant: ≤3 bars 700 ms, numbers settle +100 ms, axis draws 300 ms; character-tally variant: characters stand on pencil-textured columns. Seen styles often use springs/backOut (stiffness 170, damping 22) — KOSIF keeps data bars spring-free (one-scalar rule).

**المعاملات:** 600–800 ms; stagger min(80,700/n) ms; row 72 px; bar 34 px rx 6; font 26

**التثبيت:** npm i remotion@4.0.536 @remotion/cli@4.0.536

**الوسوم:** bars · أعمدة · stagger · Remotion · رسم أعمدة · أعمدة متحركة · تشارت أعمدة · bar chart · animated bars

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:107-145`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/stat-bars-and-fills.md`
- `app/public/js/00_editor.js:469`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`

#### 7. قدرات قريبة في العائلة

- `DATA-33` عدّاد حي فوق اللقطات / Live stat over footage (seen)
- `DATA-34` كومة أرقام الضرر / MMO damage-number stack (seen)
- `DATA-36` أعمدة أفقية مرتبة مع تمييز واحد / Ranked horizontal bars with one highlight (ready)
- `DATA-37` سباق الأعمدة / Bar-chart race (install)

### `DATA-36` — أعمدة أفقية مرتبة مع تمييز واحد / Ranked horizontal bars with one highlight

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أعمدة أفقية مرتبة بالقيمة المطلقة والقيمة عند الطرف، وواحد يبقى مضاءً حين يذكره التعليق. / Horizontal bars sorted by \|value\| with the value at the tip; the named bar stays lit.

**متى:** حين يريد المستخدم ترتيب فئات في أعمدة أفقية مع إبقاء عمود واحد مضاءً عند ذكره / when the user wants categories ranked as horizontal bars with one bar lit when the narration names it

**كيف:** SKCharts.hbars({rows:[{label,value,sub,color}],sort,fmt}) → width = \|v\|/max·100% (min .8%), grid 34%/1fr/auto, track 12 px r4; animate width with one scalar. Recipe A: title 0–350 ms (24 px slide), bars 200–1000 ms 80 ms stagger, dim/pulse 1200–1500, hold + 2% push to 3200, exit 3200–3500.

**المعاملات:** track 12 px r 4 px; recipe 3.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ranked bars · ترتيب · hbars · highlight · أعمدة أفقية · أعلى القيم · تصنيف · horizontal bar · top list

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/components/charts.js:113`
- `kosif-tool/playbooks/charts.md:49-59`
- `style:pm-charlesmendez-73b6e4`

#### 7. قدرات قريبة في العائلة

- `DATA-34` كومة أرقام الضرر / MMO damage-number stack (seen)
- `DATA-35` نمو الأعمدة المتدرج / Staggered bar growth (install)
- `DATA-37` سباق الأعمدة / Bar-chart race (install)
- `DATA-38` أعمدة مجمّعة أو مكدّسة مع خط / Grouped / stacked columns + line (ready)

### `DATA-37` — سباق الأعمدة / Bar-chart race

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** أعمدة مرتبة تنمو وتتبادل المراتب عبر الفترات، والمحور يعيد قياسه، وتسمية الفترة تعمل كساعة. / Ranked bars grow and overtake across periods while the axis rescales and the period label acts as a clock.

**متى:** حين يريد المستخدم فيديو سباق أعمدة تتبادل فيه الفئات المراكز عبر السنوات أو الفترات / when the user wants a bar race video where categories overtake each other across years or periods

**كيف:** Values linear between periods; rank = sort at each t, y eased with 500 ms in-out swaps (FLIP in HTML); axis max rescales ease-out 600 ms; period label crossfades 120 ms; ≤10 bars; freeze, losers dim to 40%, winner settles on its exact figure. Expose window.__kosif={duration,seek(t)} and render with tools/render_html.cjs. Ready block: HyperFrames bar-chart-race (periods 2019–2024, 'Name: v1, v2…', 12 s). Variants seen: avatar initials per row, row h 20 px, reorder 300 ms, ticks every 250 ms with a faint date watermark; vertical race columns with avatar tiles, checker finish line and a glowing 'You'. (code snippet in references/powers/charts-data-infographic.md)

**المعاملات:** period 800–1200 ms (recipe 1000); ≤10 bars; bar ≤24 px, gap ~10 px

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add bar-chart-race

**الوسوم:** bar race · سباق الأعمدة · ranking · FLIP · سباق · تغير المراكز · ترتيب عبر الزمن · racing bar chart · overtake

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:73-83`
- `kosif-tool/styles/chart-race/SKILL.md`
- `kosif-one/vendor/hyperframes/registry/blocks/bar-chart-race/bar-chart-race.html`
- `style:pm-ratheejaisal-1f4538`

#### 7. قدرات قريبة في العائلة

- `DATA-35` نمو الأعمدة المتدرج / Staggered bar growth (install)
- `DATA-36` أعمدة أفقية مرتبة مع تمييز واحد / Ranked horizontal bars with one highlight (ready)
- `DATA-38` أعمدة مجمّعة أو مكدّسة مع خط / Grouped / stacked columns + line (ready)
- `DATA-39` مخطط الشلال (الجسر) / Waterfall / bridge chart (ready)

### `DATA-38` — أعمدة مجمّعة أو مكدّسة مع خط / Grouped / stacked columns + line

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مولّد SVG بلا مكتبات لأعمدة مجمعة أو مكدسة مع خط اختياري على نفس المحور وأرقام محاور «لطيفة». / Dependency-free SVG generator for grouped/stacked columns with an optional line on the same axis and nice-number ticks.

**متى:** حين يحتاج المستخدم أعمدة مجمعة أو مكدسة مع خط على نفس المحور دون مكتبة رسوم / when the user needs grouped or stacked columns with an optional line on one axis without a chart library

**كيف:** SKCharts.bars({labels, series:[{name,color,values}], line, stacked, height, width, fmt}); nice() rounds to 1/2/2.5/5/10×10ⁿ; 4 gridlines; padding l46 r8 t12 b30; data-end corner r=min(4,w/2,h); empty-state text when all zero. For video, wrap each rect in a scaleY tween from the baseline.

**المعاملات:** default 720×260

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stacked · grouped · مكدسة · SVG · أعمدة مجمعة · أعمدة وخط · مقارنة سلاسل · combo chart · column chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/components/charts.js:52`
- `kosif-earth-ci-fork/ui/components/charts.js:26`

#### 7. قدرات قريبة في العائلة

- `DATA-36` أعمدة أفقية مرتبة مع تمييز واحد / Ranked horizontal bars with one highlight (ready)
- `DATA-37` سباق الأعمدة / Bar-chart race (install)
- `DATA-39` مخطط الشلال (الجسر) / Waterfall / bridge chart (ready)
- `DATA-40` شريط النسب المقسّم (كبسولة) / Proportional split bar (segmented pill) (seen)

### `DATA-39` — مخطط الشلال (الجسر) / Waterfall / bridge chart

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل خطوة تحرك المجموع الجاري، والمجاميع تقف على القاعدة. / Each step moves a running total; total steps stand on the baseline.

**متى:** حين يريد المستخدم شرح كيف تنتقل قيمة من البداية إلى النهاية عبر زيادات ونقصانات متتالية / when the user wants to explain how a total moves from start to end through successive gains and losses

**كيف:** SKCharts.waterfall({steps:[{label,value,total}]}); up = c1, down = c8, total = ink-2; bar width min(40, band·.62); connectors between steps. In motion reveal step by step (300–400 ms each), connector draws before the next bar.

**المعاملات:** 720×260; padding l52 b44

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** waterfall · شلال · bridge · finance · مخطط جسر · أرباح وخسائر · مجموع جاري · running total · profit loss

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/components/charts.js:124`

#### 7. قدرات قريبة في العائلة

- `DATA-37` سباق الأعمدة / Bar-chart race (install)
- `DATA-38` أعمدة مجمّعة أو مكدّسة مع خط / Grouped / stacked columns + line (ready)
- `DATA-40` شريط النسب المقسّم (كبسولة) / Proportional split bar (segmented pill) (seen)
- `DATA-41` زووم لوغاريتمي داخل شريحة / Log-domain zoom into a slice (seen)

### `DATA-40` — شريط النسب المقسّم (كبسولة) / Proportional split bar (segmented pill)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريط واحد ينقسم إلى أجزاء بنسبها مع قيمة كل جزء، وكل جزء بتدرج عمودي خاص. / One bar splits into proportional segments with each value; each segment has its own vertical gradient.

**متى:** حين يريد المستخدم إظهار تقسيم كل إلى أجزاء بنسبها في شريط واحد مستدير / when the user wants one rounded bar split into proportional parts showing each share

**كيف:** Rounded pill, height ~6% frame, radius full; segment boundaries lerp from 0 to cumulative shares; big % above/below each; check parts sum to the total and print remainder/rounding (MG-048: 0–1 total, 1–4 split, 4–8 read).

**المعاملات:** height ~6% frame; MG-048 8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** split bar · شريط مقسم · composition · pill · نسب الأجزاء · شريط النسب · تقسيم · part to whole · 100% bar

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:infographic`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`

#### 7. قدرات قريبة في العائلة

- `DATA-38` أعمدة مجمّعة أو مكدّسة مع خط / Grouped / stacked columns + line (ready)
- `DATA-39` مخطط الشلال (الجسر) / Waterfall / bridge chart (ready)
- `DATA-41` زووم لوغاريتمي داخل شريحة / Log-domain zoom into a slice (seen)
- `DATA-42` أعمدة بفترات ثقة / Bars with interval whiskers (seen)

### `DATA-41` — زووم لوغاريتمي داخل شريحة / Log-domain zoom into a slice

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تكبير محور الشريط من 100 إلى 1.2 في الفضاء اللوغاريتمي لتظهر شريحة صغيرة جدًا دون تمطيط الحواف المستديرة. / Animate the bar domain from 100 to 1.2 in log space so a tiny slice fills the frame without stretching rounded caps.

**متى:** حين تكون شريحة صغيرة جدًا في شريط لا تكاد تُرى ويراد تكبيرها لتملأ الإطار / when a tiny share in a bar is barely visible and must be zoomed in to fill the frame

**كيف:** max(t) = exp(lerp(ln a, ln b, e(t))); recompute every segment's x/width per frame (never scale the group) so radius stays round; announce the zoom on screen. (code snippet in references/powers/charts-data-infographic.md)

**المعاملات:** ~1.2 s ease-in-out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** log zoom · زووم · tiny share · تكبير · نسبة صغيرة · مقياس لوغاريتمي · zoom in · small share

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:infographic`

#### 7. قدرات قريبة في العائلة

- `DATA-39` مخطط الشلال (الجسر) / Waterfall / bridge chart (ready)
- `DATA-40` شريط النسب المقسّم (كبسولة) / Proportional split bar (segmented pill) (seen)
- `DATA-42` أعمدة بفترات ثقة / Bars with interval whiskers (seen)
- `DATA-43` مقاييس وأشرطة تقدم بلون الحكم / Verdict-coloured meters & RTL-safe progress (ready)

### `DATA-42` — أعمدة بفترات ثقة / Bars with interval whiskers

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أعمدة سميكة تنمو من المحور (أخضر فوق العتبة وأحمر تحتها) مع خط رفيع لفترة 95٪ وقيمة «n من N» عند الطرف. / Thick bars grow from the axis (green above threshold, red below) with a thin 95% interval whisker and 'n of N' at the tip.

**متى:** حين تُعرض نتائج بأعمدة ويجب إظهار فترة الثقة وعدد العينة فوق عتبة أو تحتها / when results shown as bars must display a confidence interval and sample size against a threshold

**كيف:** Serif labels left; grow 800 ms easeOutCubic, stagger 200 ms; whisker draws after the bar; italic annotation; palette paper #eee8dc, ink #2b2622, red #c9463d, green #1f7a4f.

**المعاملات:** 800 ms; stagger 200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** confidence interval · فترات ثقة · whiskers · editorial · هامش الخطأ · حجم العينة · إحصاء · error bars · sample size

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-henkvaness-0e06af`

#### 7. قدرات قريبة في العائلة

- `DATA-40` شريط النسب المقسّم (كبسولة) / Proportional split bar (segmented pill) (seen)
- `DATA-41` زووم لوغاريتمي داخل شريحة / Log-domain zoom into a slice (seen)
- `DATA-43` مقاييس وأشرطة تقدم بلون الحكم / Verdict-coloured meters & RTL-safe progress (ready)
- `DATA-44` أشرطة مقسّمة إلى خانات / Segmented / dotted meters (seen)

### `DATA-43` — مقاييس وأشرطة تقدم بلون الحكم / Verdict-coloured meters & RTL-safe progress

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صفوف أعمدة متدرجة حسب الخطورة، ومقياس يتغير لونه حسب الحكم، وشريط تقدم ينمو من جهة البداية بالتحويل فقط. / Severity gradient bar rows, a meter whose colour follows the verdict, and a progress bar that grows from the start side via transform.

**متى:** حين يريد المستخدم أشرطة تقدم أو مقاييس يتغير لونها حسب الخطورة أو الحكم وتعمل في الواجهات العربية / when the user wants progress bars or meters coloured by severity or verdict that work in RTL interfaces

**كيف:** Rows: grid minmax(80px,1fr) 2.5fr 42px, fill = round(n/max·100)%; track 9 px #f1f5f9; fills 90deg critical #f43f5e→#ef4444, high #f59e0b→#f97316, medium #06b6d4→#6366f1, low #10b981→#14b8a6. Meter: width transition .5s ease, data-verdict approaching → warning, material → danger, anchored inline-end. Progress: translateX(-(100-value)%) height 8 px, 500 ms ease-out, aria-valuetext.

**المعاملات:** 500 ms ease; track 9 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** meter · مقياس · progress · severity · شريط تقدم · مستوى الخطورة · تحذير · progress bar · rtl

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-audit-studio/v5/continuous-dashboard.js:31`
- `kosif-audit-studio/styles.css:718`
- `kosif-audit-pro/components/ui/progress.tsx`
- `kosif-audit-pro/tests/ui-components.test.mjs`

#### 7. قدرات قريبة في العائلة

- `DATA-41` زووم لوغاريتمي داخل شريحة / Log-domain zoom into a slice (seen)
- `DATA-42` أعمدة بفترات ثقة / Bars with interval whiskers (seen)
- `DATA-44` أشرطة مقسّمة إلى خانات / Segmented / dotted meters (seen)
- `DATA-45` سباق المقارنة والسرعة / Speed / latency comparison race (seen)

### `DATA-44` — أشرطة مقسّمة إلى خانات / Segmented / dotted meters

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صف مربعات أو نقاط يضيء واحدًا تلو الآخر حتى المستوى مع عدّاد مربوط، أو دلو بخانات يفرغ ويمتلئ. / A row of squares/dots lights up cell by cell to a level with a bound counter, or a slotted bucket drains and refills.

**متى:** حين يريد المستخدم شريط مهارات أو حصة من مربعات أو نقاط تضيء واحدة تلو الأخرى / when the user wants skill or quota bars made of cells or dots lighting up one by one

**كيف:** Cells light left→right (right→left in Arabic) 30–50 ms each, rows stagger 120 ms, end tag 'MAX' or '[x] Ready'; bucket: 10 rounded slots, blue #5aa8ff, partial top slot as thin bar, stroke red #f85149 at zero; lease bars drain linearly over 10 s, refill on check-in, 'EXPIRED' sticker at 0; trading-card variant: 3 labelled bars 600 ms ease-out stagger 150 ms.

**المعاملات:** 16–20 cells; 30–50 ms per cell; 0→98% in 1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** segmented · خانات · skill bars · quota · شريط مهارات · نقاط · مستوى · level meter · cells

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-anthonyriera-9b1b2a`
- `style:pm-ibrahimwasim240-809370`
- `style:pm-parkerrex-1a54fe`
- `style:pm-gigabit-million-16b3a0`

#### 7. قدرات قريبة في العائلة

- `DATA-42` أعمدة بفترات ثقة / Bars with interval whiskers (seen)
- `DATA-43` مقاييس وأشرطة تقدم بلون الحكم / Verdict-coloured meters & RTL-safe progress (ready)
- `DATA-45` سباق المقارنة والسرعة / Speed / latency comparison race (seen)
- `DATA-46` لوحة احتمالات الكلمة التالية / Next-token probability panel (seen)

### `DATA-45` — سباق المقارنة والسرعة / Speed / latency comparison race

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريطان أو أكثر يتسابقان: واحد يمتلئ فورًا أو يتجاوز حافة الإطار، والمنافسون يزحفون، وعدّاد الزمن ينزل. / Two+ bars race: one fills instantly or overshoots the frame edge, competitors crawl, a ms readout counts down.

**متى:** حين يريد المستخدم مقارنة سرعة منتج بمنافسيه في سباق أشرطة مع عداد زمن / when the user wants to compare a product's speed against competitors as a bar race with a timer

**كيف:** ease-in-expo on the brand bar to ≤120% width (breaking the frame is the joke), others ≤60%; timer counters per bar; before/after: two segmented timelines, the 'after' shorter in green.

**المعاملات:** 1–1.2 s; brand ≤120% width; others ≤60%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** race · سرعة · latency · before after · مقارنة السرعة · أداء · منافسين · speed comparison · competitors

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-influencer-seo-ce8c33/BRIEF.md`
- `style:pm-heyiammallik-e72d17`
- `style:pm-polydao-7a572b`
- `style:pm-prasad-pilla-2c0cba`

#### 7. قدرات قريبة في العائلة

- `DATA-43` مقاييس وأشرطة تقدم بلون الحكم / Verdict-coloured meters & RTL-safe progress (ready)
- `DATA-44` أشرطة مقسّمة إلى خانات / Segmented / dotted meters (seen)
- `DATA-46` لوحة احتمالات الكلمة التالية / Next-token probability panel (seen)
- `DATA-47` ترتيب يتغير والقوائم المرتبة / Rank swap & ranked lists (seen)

### `DATA-46` — لوحة احتمالات الكلمة التالية / Next-token probability panel

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 4 كلمات مرشحة بأشرطة تنمو إلى احتمالاتها، والمختارة بشريط برتقالي وسهم، ثم تُكتب في سطر الأمر. / Four candidate tokens with bars growing to their probabilities; the chosen one turns orange with an arrow, then types into the prompt.

**متى:** حين يشرح الفيديو كيف يختار نموذج لغوي الكلمة التالية أو يعرض احتمالات متنافسة / when a video explains how a language model picks the next token, or shows competing probabilities

**كيف:** Bars grow 400 ms staggered 80 ms; values like 0.55/0.21/0.11/0.01; chosen bar accent + arrow; then typewriter with cursor; same pattern for prediction-market probability bars (600 ms easeOut, values count).

**المعاملات:** 400 ms; stagger 80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** probability · احتمال · LLM · tokens · ذكاء اصطناعي · الكلمة التالية · نسب الاحتمال · next token · prediction market

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:plotter`
- `style:pm-polydao-7a572b`

#### 7. قدرات قريبة في العائلة

- `DATA-44` أشرطة مقسّمة إلى خانات / Segmented / dotted meters (seen)
- `DATA-45` سباق المقارنة والسرعة / Speed / latency comparison race (seen)
- `DATA-47` ترتيب يتغير والقوائم المرتبة / Rank swap & ranked lists (seen)
- `DATA-48` مخطط أعمدة دائري / شعاعي / Radial / clockwise bar chart (idea)

### `DATA-47` — ترتيب يتغير والقوائم المرتبة / Rank swap & ranked lists

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقات مرتبة تنتقل إلى ترتيب جديد مع تحديث أرقامها، أو بطاقات أرقام تتحول إلى قائمة «الأضعف أولًا». / Ranked cards move to a new order while numbers update, or stat tiles cross-fade into a weakest-first list.

**متى:** حين يريد المستخدم إظهار تغير ترتيب العناصر بين فترتين أو تحويل بطاقات أرقام إلى قائمة مرتبة / when the user wants items to reorder between two periods or stat tiles to turn into a ranked list

**كيف:** MG-049: 0–2 s period one, 2–5 s reorder, 5–8 s period two; fixed slot positions per rank, paths that cross least, identity colour kept (FLIP). Tiles→list: opacity/translateY 30→0 then rows translateX 40→0 stagger .08 s; ranked rows 80–120 ms stagger with right-aligned scores and status pills (bg #fbe3e3, text #a8484a).

**المعاملات:** MG-049 8 s; rows 80–120 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** rank swap · ترتيب · leaderboard · FLIP · لوحة الصدارة · تغيير الترتيب · قائمة مرتبة · reorder · ranked list

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:102`
- `style:pm-palashbagchi11-0a4b6b`
- `style:pm-twoclipping-6dd14e`

#### 7. قدرات قريبة في العائلة

- `DATA-45` سباق المقارنة والسرعة / Speed / latency comparison race (seen)
- `DATA-46` لوحة احتمالات الكلمة التالية / Next-token probability panel (seen)
- `DATA-48` مخطط أعمدة دائري / شعاعي / Radial / clockwise bar chart (idea)
- `DATA-49` المضاعفات الصغيرة / Small multiples (documented)

### `DATA-48` — مخطط أعمدة دائري / شعاعي / Radial / clockwise bar chart

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أعمدة تمتد من المركز للخارج أو قطاعات تنمو مع عقارب الساعة واحدًا تلو الآخر مع تسميات متأخرة. / Bars extend outward from the centre, or segments grow clockwise one at a time with delayed labels.

**متى:** حين يريد المستخدم أعمدة دائرية تمتد من المركز أو قطاعات تنمو مع عقارب الساعة / when the user wants circular bars radiating from the centre or segments growing clockwise

**كيف:** SVG arcs from −90°; each 300–500 ms cubic-bezier(0.33,1,0.68,1), 60 ms stagger, label +100–150 ms; length from the inner radius (area grows faster than value — say so or use constant-width wedges).

**المعاملات:** 300–500 ms/segment; stagger 60 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** radial · شعاعي · polar · أعمدة دائرية · رسم قطبي · دائري · circular bar · arc chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-marouanegazouzi-6071d5/BRIEF.md`
- `kosif-tool/styles/pm-monokern-ade5b6/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DATA-46` لوحة احتمالات الكلمة التالية / Next-token probability panel (seen)
- `DATA-47` ترتيب يتغير والقوائم المرتبة / Rank swap & ranked lists (seen)
- `DATA-49` المضاعفات الصغيرة / Small multiples (documented)
- `DATA-50` خط يُرسم مع مساحة ونقاط تقفز / Line draw-on with area fade & dot pops (proven)

### `DATA-49` — المضاعفات الصغيرة / Small multiples

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرّر نفس المخطط الصغير لكل فئة بمحاور مشتركة بدل تحميل مخطط واحد. / Repeat the same mini-chart per category with shared axes instead of overloading one chart.

**متى:** حين تزدحم فئات كثيرة في رسم واحد ويحسن تقسيمها إلى رسوم صغيرة متكررة بمحاور مشتركة / when too many categories crowd one chart and should split into repeated mini charts with shared axes

**كيف:** Grid columns = min(3, n), shared x and y, empty cells hidden; one neutral hue + accent; reveal panels in reading order (right-to-left rows in Arabic) with 60–100 ms stagger.

**المعاملات:** cols=min(3,n); stagger 60–100 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** small multiples · مضاعفات · grid · شبكة رسوم · رسوم صغيرة · مقارنة فئات · facets · panel grid

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/distribution-and-summary-choices.md`

#### 7. قدرات قريبة في العائلة

- `DATA-47` ترتيب يتغير والقوائم المرتبة / Rank swap & ranked lists (seen)
- `DATA-48` مخطط أعمدة دائري / شعاعي / Radial / clockwise bar chart (idea)
- `DATA-50` خط يُرسم مع مساحة ونقاط تقفز / Line draw-on with area fade & dot pops (proven)
- `DATA-51` خط يرسمه رأس قلم يحمل العدّاد / Pen-tip counter line (ready)

### `DATA-50` — خط يُرسم مع مساحة ونقاط تقفز / Line draw-on with area fade & dot pops

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سلسلة 12 نقطة تُرسم بـ pathLength=1 والمساحة المتدرجة تظهر وكل نقطة تقفز حين يمر القلم. / A 12-point series draws via pathLength=1 dashoffset, a gradient area fades in, each dot pops as the pen passes.

**متى:** حين يريد المستخدم رسمًا خطيًا يرسم نفسه مع مساحة متدرجة ونقاط تقفز أثناء الرسم / when the user wants a line chart that draws itself with a gradient area and dots popping along

**كيف:** series → path d; line.strokeDashoffset = 1 − prog(local,0.2,2.4,inOutCubic); dot r = 12·prog(draw, i/(n−1), +0.08, outBack); area gradient #7ee8d2 .35→0. Rendered here (preview frames 3.8–7.0 s: line, dots and counter 45→128). Honest note: in the starter the area gradient leads the pen slightly — reveal the area with a clip that follows the pen if that matters.

**المعاملات:** viewBox 900×620; stroke #7ee8d2 14 px round; dots #ffb86b r12; 2.2 s draw

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** line chart · draw-on · خط بياني · dashoffset · رسم خطي · خط يرسم نفسه · مساحة متدرجة · animated line · line animation

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/starters/html-canvas/index.html:88`
- `kosif-tool/starters/html-canvas/index.html:157`
- `kosif-tool/playbooks/charts.md:37`

#### 7. قدرات قريبة في العائلة

- `DATA-48` مخطط أعمدة دائري / شعاعي / Radial / clockwise bar chart (idea)
- `DATA-49` المضاعفات الصغيرة / Small multiples (documented)
- `DATA-51` خط يرسمه رأس قلم يحمل العدّاد / Pen-tip counter line (ready)
- `DATA-52` منحنى ناعم في Remotion / Remotion smooth cubic line (install)

### `DATA-51` — خط يرسمه رأس قلم يحمل العدّاد / Pen-tip counter line

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الخط يُرسم والعدّاد يقرأ قيمة رأس القلم المستوفاة، والنقاط تقفز عند المرور، والمساحة تُملأ بعده. / The line draws while a counter reads the interpolated pen value; dots pop as it passes; area fills after.

**متى:** حين يريد المستخدم خطًا يرسم نفسه وعدادًا يقرأ قيمة رأس الخط لحظة بلحظة / when the user wants a self-drawing line with a counter reading the value at the tip as it moves

**كيف:** Canvas drawFrame(t): axes alpha 0.2–0.6 s; head = ease((t−0.6)/1.2)·(n−1); tip value = lerp between neighbours; counter Noto Kufi Arabic 600 72 px; stroke #19c37d 6 px; axis #5a5a5a. Recipe B: axes 0–400, draw 400–1700, area to 18% 1700–2000, caption 2000–2400, hold to 4000 ms. Leading dot rides the tip, glow 6 px; tooltip pops at the max.

**المعاملات:** 1000–1400 ms per 1000 px ease-out cubic; dots spring {14,160,0.8} ≈250 ms; area 300 ms → 18%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pen tip · رأس القلم · counter · Canvas · رسم خطي · عداد على الخط · قيمة لحظية · line chart · leading dot

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:151-181`
- `kosif-tool/playbooks/charts.md:61-71`
- `style:pm-sudeepsd-1a3485`
- `style:pm-viktoroddy-98c1d8`

#### 7. قدرات قريبة في العائلة

- `DATA-49` المضاعفات الصغيرة / Small multiples (documented)
- `DATA-50` خط يُرسم مع مساحة ونقاط تقفز / Line draw-on with area fade & dot pops (proven)
- `DATA-52` منحنى ناعم في Remotion / Remotion smooth cubic line (install)
- `DATA-53` مؤشر قراءة متحرك على المخطط / Chart scrub readout (playhead) (install)

### `DATA-52` — منحنى ناعم في Remotion / Remotion smooth cubic line

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Remotion company license (free for individuals and small teams; companies above the threshold need a paid license) |

**ما هي:** 9 نقاط ببذرة ثابتة بمنحنى تكعيبي، تُرسم خطيًا مع كشف المساحة بقص، وشبكة منقطة تنمو، ونقاط بنابض، وعدّاد عربي. / Nine seeded points joined by a cubic path, drawn linearly with a clip-path area reveal, dashed grid growing, spring dots, Arabic counter.

**متى:** حين يعمل المستخدم في Remotion ويريد منحنى بيانات ناعمًا يرسم نفسه مع عداد عربي / when working in Remotion and wanting a smooth self-drawing data curve with an Arabic counter

**كيف:** makeSeries('kosif-chart') via remotion random(); smoothPath() with handles at 1/3; DRAW_START 12, DRAW_LENGTH 66 frames; dot spring damping 10 stiffness 180; counter 124 px 800 easeOutExpo Intl.NumberFormat('ar-EG').

**المعاملات:** 920×620 viewBox; pad 60/40/50/70; stroke 10; grid 0/.25/.5/.75/1 dash '6 10'

**التثبيت:** npm i remotion@4.0.536 @remotion/cli@4.0.536

**الوسوم:** Remotion · cubic · منحنى ناعم · منحنى بيانات · رسم خطي · ريموشن · smooth curve · line chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/starters/remotion/src/Film.tsx:253`
- `kosif-tool/starters/remotion/src/Film.tsx:266`
- `kosif-tool/starters/remotion/src/Film.tsx:281`

#### 7. قدرات قريبة في العائلة

- `DATA-50` خط يُرسم مع مساحة ونقاط تقفز / Line draw-on with area fade & dot pops (proven)
- `DATA-51` خط يرسمه رأس قلم يحمل العدّاد / Pen-tip counter line (ready)
- `DATA-53` مؤشر قراءة متحرك على المخطط / Chart scrub readout (playhead) (install)
- `DATA-54` خط/مساحة مع مؤشر تقاطع / SKCharts line/area with crosshair (ready)

### `DATA-53` — مؤشر قراءة متحرك على المخطط / Chart scrub readout (playhead)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** خط تتبع وعلامة يتحركان على المنحنى وتلميح تاريخ/قيمة يتنقل عبر البيانات ويتوقف عند القمة. / A tracking line + marker moves along the baked polyline while a date/value tooltip steps through the data and stops on the peak.

**متى:** حين يريد المستخدم مؤشرًا يتحرك على الخط ويعرض التاريخ والقيمة ويتوقف عند القمة / when the user wants a marker sweeping along a line, showing date and value, stopping at the peak

**كيف:** Scrub 1.5–3 s, ≥0.8 s hold after; peak stop power3.out; series B lights up 0.25 s power2.out when crossed; tooltip pill snaps to the nearest point. Step-chart variant: state history as a step line up to t, vertical playhead, event ticks below coloured by outcome, dashed max line.

**المعاملات:** SCRUB_DUR 1.5–3 s; hold ≥0.8 s

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add mk-line-graph

**الوسوم:** scrub · playhead · tooltip · مؤشر · تلميح · أعلى قيمة · قراءة القيم · peak · step chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/chart-scrub-readout.md`
- `style:pm-steventey-0d20e4`
- `style:pm-twoclipping-5cba86`
- `style:pm-parkerrex-1a54fe`

#### 7. قدرات قريبة في العائلة

- `DATA-51` خط يرسمه رأس قلم يحمل العدّاد / Pen-tip counter line (ready)
- `DATA-52` منحنى ناعم في Remotion / Remotion smooth cubic line (install)
- `DATA-54` خط/مساحة مع مؤشر تقاطع / SKCharts line/area with crosshair (ready)
- `DATA-55` الخطوط المصغرة / Sparklines & micro-charts (proven)

### `DATA-54` — خط/مساحة مع مؤشر تقاطع / SKCharts line/area with crosshair

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مخطط خطي SVG بمساحة 10٪ ونقاط نهاية وتسميات نهاية وتخفيف للتسميات ومؤشر تقاطع. / SVG line chart with optional 10% area, end dots and end labels, label thinning and a crosshair tooltip.

**متى:** حين يحتاج المستخدم رسمًا خطيًا أو مساحيًا بصيغة SVG بتسميات نهاية ومؤشر تقاطع / when the user needs an SVG line or area chart with end labels and a crosshair tooltip

**كيف:** SKCharts.line({labels, series, area, endLabels, height, width}); label step = ceil(n / max(3, floor(iw/56))); end labels when ≤4 series (pr 70); point r 4; line 2 px.

**المعاملات:** 720×240

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** line · crosshair · area · SVG · رسم خطي · رسم مساحي · مؤشر تقاطع · line chart · area chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/components/charts.js:89`

#### 7. قدرات قريبة في العائلة

- `DATA-52` منحنى ناعم في Remotion / Remotion smooth cubic line (install)
- `DATA-53` مؤشر قراءة متحرك على المخطط / Chart scrub readout (playhead) (install)
- `DATA-55` الخطوط المصغرة / Sparklines & micro-charts (proven)
- `DATA-56` صعود ثم انهيار / Rise-then-crash line metaphor (install)

### `DATA-55` — الخطوط المصغرة / Sparklines & micro-charts

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خطوط بحجم الكلمة بجانب الرقم الذي تشرحه، بعلامة آخر قيمة وحلقة ورقية. / Word-sized trend lines beside the number they explain, end marker with a paper ring.

**متى:** حين يريد المستخدم خطًا صغيرًا يوضح اتجاه رقم بجانبه في بطاقة أو جملة / when the user wants a tiny word-sized trend line next to the number it explains in a card or sentence

**كيف:** PRESS primitives (Python → SVG string): sparkline 300×68, 2 px round-cap line, end dot r≥4 with 2 px paper ring, hairline grid; dual_sparkline for two series; SKCharts.spark(values,{w,h,color,accent}) 90×28 stroke 1.8 end r 3; trendSvg: x(i)=p+i(w−2p)/(n−1), evidence #6366f1 vs issues #ec4899 3 px. Animate by revealing the path then pulsing the end dot.

**المعاملات:** 300×68 px; end r≥4 + 2 px ring; draw 800 ms; area α .15

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sparkline · خط صغير · micro chart · PRESS · اتجاه مصغر · رسم صغير · ترند · mini chart · trend line

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2622-city-report/9999-city-report/scripts/charts.py`
- `kosif-earth-ci-fork/ui/components/charts.js:242`
- `kosif-audit-studio/v5/continuous-dashboard.js:34`
- `kosif-atlas/skills/2690-build-web-data-visualization/10319-canvas2d-data-visualization/references/sparklines-and-microcharts.md`

#### 7. قدرات قريبة في العائلة

- `DATA-53` مؤشر قراءة متحرك على المخطط / Chart scrub readout (playhead) (install)
- `DATA-54` خط/مساحة مع مؤشر تقاطع / SKCharts line/area with crosshair (ready)
- `DATA-56` صعود ثم انهيار / Rise-then-crash line metaphor (install)
- `DATA-57` الشموع وشريط الأسعار / Candlesticks & price ticker (seen)

### `DATA-56` — صعود ثم انهيار / Rise-then-crash line metaphor

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** خط يصعد كالسهم أثناء ذكر الهدف، ثم مقطع أحمر سميك يهوي عند ذكر الفشل، والخلفية تُعتم مع الهبوط. / A line climbs while the goal is mentioned, then a thick red segment plunges on the failure line; background darkens with the decline.

**متى:** حين يروي الفيديو قصة صعود ثم فشل أو انهيار ويحتاج خطًا يصعد ثم يهوي مع الكلام / when a video tells a rise-then-failure story and needs a line climbing then plunging on the spoken word

**كيف:** drawPath(chartUp, 15.5 s, 2.8 s) stroke #7fd0ff 7 px; chartDown #ff5a5a 9 px drawn in 0.45 s at 19.64 s (on the spoken word); both fade at 23.6 s. HyperFrames decline-chart counts 82 → 34 while drawing down. Pixel variant: 12 green candles every 80–120 ms then 6 red ones and a falling line (style:pm-0xevinho-3777d8); crash comparison end labels −20% vs −28%.

**المعاملات:** up 2.8 s; crash 0.45 s

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add decline-chart

**الوسوم:** crash · انهيار · decline · metaphor · صعود وهبوط · سقوط · فشل · rise and fall · downturn

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/projects/whatsapp-motion/projects/success/index.html:234-237`
- `kosif-one/vendor/hyperframes/registry/components/decline-chart/decline-chart.html`
- `style:pm-0xevinho-3777d8`
- `style:pm-rammanq-f5a90f`

#### 7. قدرات قريبة في العائلة

- `DATA-54` خط/مساحة مع مؤشر تقاطع / SKCharts line/area with crosshair (ready)
- `DATA-55` الخطوط المصغرة / Sparklines & micro-charts (proven)
- `DATA-57` الشموع وشريط الأسعار / Candlesticks & price ticker (seen)
- `DATA-58` طبقة التعليقات والإبراز / Annotation & highlight layer (ready)

### `DATA-57` — الشموع وشريط الأسعار / Candlesticks & price ticker

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شموع تظهر يسارًا ليمين بألوان صعود/هبوط، وحبة سعر حي تتبع آخر نقطة، وشريط رموز يمر. / Candles appear left→right in up/down colours, a live price pill tracks the last point, a ticker strip scrolls.

**متى:** حين يحتاج فيديو مالي شموعًا يابانية أو سعرًا حيًا أو شريط رموز يمر / when a finance video needs candlesticks, a live price pill or a scrolling ticker tape

**كيف:** Candles 20 ms stagger, green #2ee6a6 / red #e5486b; price pill ticks every 100 ms with tabular nums; ticker tape rotated strip with mono symbols at 200 px/s; price-target scale: axis from→target with a green glowing marker; payoff curve: trapezoid green above zero, pink below.

**المعاملات:** 20 ms/candle; ticker 200 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** candlestick · شموع · ticker · finance · بورصة · أسهم · شموع يابانية · stock chart · price chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-dale-vaz-cc612a`
- `style:pm-aistocksavvy-3fb9f5`
- `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DATA-55` الخطوط المصغرة / Sparklines & micro-charts (proven)
- `DATA-56` صعود ثم انهيار / Rise-then-crash line metaphor (install)
- `DATA-58` طبقة التعليقات والإبراز / Annotation & highlight layer (ready)
- `DATA-59` تحوّل المخططات / Chart morph (bars → donut / line / scatter) (install)

### `DATA-58` — طبقة التعليقات والإبراز / Annotation & highlight layer

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تعليقات مربوطة بنقاط البيانات، فترات مظللة، وخطوط هدف متقطعة تشرح نقاط التحول. / Callouts tied to data points, shaded spans and dashed target lines that explain turning points.

**متى:** حين يحتاج الرسم شرح نقطة تحول بسهم تعليق أو فترة مظللة أو خط هدف متقطع / when a chart needs a turning point explained with a callout arrow, shaded period or dashed target line

**كيف:** Separate layer above marks: arrow callout label → point; shaded span ~20% alpha for a period (era bands); dashed grey target line with value label; short straight or gently elbowed leaders 0.75–1.25 px; label halo 2–3 px background stroke (paint-order stroke). Draw annotations after the data lands (+200 ms).

**المعاملات:** span α ~0.2; halo 2–3 px; leader 0.75–1.25 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** annotation · تعليقات · target line · callout · تعليق توضيحي · سهم · فترة مظللة · arrow callout · shaded band

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md`
- `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/references/details.md`
- `style:pm-kloss-xyz-fe0c31`

#### 7. قدرات قريبة في العائلة

- `DATA-56` صعود ثم انهيار / Rise-then-crash line metaphor (install)
- `DATA-57` الشموع وشريط الأسعار / Candlesticks & price ticker (seen)
- `DATA-59` تحوّل المخططات / Chart morph (bars → donut / line / scatter) (install)
- `DATA-60` رسم بياني بخط اليد / Hand-drawn axis plot (seen)

### `DATA-59` — تحوّل المخططات / Chart morph (bars → donut / line / scatter)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نفس البيانات تتحول من عرض إلى آخر: أعمدة تنثني إلى أقواس، أو أعمدة تصير خطًا، أو منحنى يتحول من شكل لآخر. / The same dataset morphs between views: bars bend into arcs, bars become a line, a curve changes generator.

**متى:** حين يريد المستخدم تحويل نفس البيانات من أعمدة إلى دونات أو خط أو مبعثر دون قطع / when the user wants the same data to morph from bars into a donut, line or scatter without a cut

**كيف:** Recipe D: axes fade 1600–1800 ms, labels detach 12 px; bend 1800–2700 cubic-bezier(.65,0,.35,1) keeping colour+label; centre total counts 2700–3000. Resample both paths to equal point counts (flubber or own resampler) then lerp; waveform morph between flat/sine/gaussian/square in 800 ms easeInOutCubic; ceiling → logistic S-curve 800 ms after a 250 ms strike scribble. Morph only between views of the same data.

**المعاملات:** 800–1000 ms in-out; old axis out 200 ms before, new in 200 ms after

**التثبيت:** npm i flubber@0.4.2

**الوسوم:** morph · تحول · flubber · bars to donut · تحويل الشكل · انتقال سلس · مورف · shape morph · chart transition

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:85-95`
- `kosif-tool/styles/morph-charts/SKILL.md`
- `style:pm-rneayan-ea6129`
- `style:pm-ik-builds-b8bdcf`

#### 7. قدرات قريبة في العائلة

- `DATA-57` الشموع وشريط الأسعار / Candlesticks & price ticker (seen)
- `DATA-58` طبقة التعليقات والإبراز / Annotation & highlight layer (ready)
- `DATA-60` رسم بياني بخط اليد / Hand-drawn axis plot (seen)
- `DATA-61` مروحة مونت كارلو وعدم اليقين / Monte Carlo fan & uncertainty (seen)

### `DATA-60` — رسم بياني بخط اليد / Hand-drawn axis plot

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** محاور بأسهم وتسميات بخط اليد ثم منحنى ناعم أو مهتز يُرسم من اليسار لليمين بحبر لوني. / Axes with arrowheads and handwritten labels, then a smooth or noisy curve traced left→right in accent ink.

**متى:** حين يريد المستخدم رسمًا بيانيًا بأسلوب السبورة وخط اليد بمحاور ومنحنى يرسم نفسه / when the user wants a whiteboard or hand-drawn style graph with axes and a self-tracing curve

**كيف:** Axes draw 300 ms each; curve 1.5–2.5 s; wobble jitter 1 px per frame for sketch feel (seeded); 'now $X' label updates with the pen; can use roughjs for the sketchy stroke.

**المعاملات:** curve 1.5–2.5 s; jitter 1 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hand-drawn · خط اليد · sketch · whiteboard · سبورة · رسم يدوي · اسكتش · roughjs · doodle chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-tak3sh8-be5012`
- `style:pm-nikolajankovic-ce4ff4`
- `style:pm-ik-builds-b8bdcf`

#### 7. قدرات قريبة في العائلة

- `DATA-58` طبقة التعليقات والإبراز / Annotation & highlight layer (ready)
- `DATA-59` تحوّل المخططات / Chart morph (bars → donut / line / scatter) (install)
- `DATA-61` مروحة مونت كارلو وعدم اليقين / Monte Carlo fan & uncertainty (seen)
- `DATA-62` هيستوغرام نقاط يصير منحنى جرس / Dot histogram resolving to a bell curve (seen)

### `DATA-61` — مروحة مونت كارلو وعدم اليقين / Monte Carlo fan & uncertainty

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ألف مسار عشوائي رفيع بشفافية 0.1 مع خط الوسيط وشارات المئينات. / 1000 thin random-walk paths at alpha 0.1 with a median line and percentile pills.

**متى:** حين يريد المستخدم إظهار عدم اليقين بآلاف المسارات العشوائية مع الوسيط ونطاق المئينات / when the user wants to show uncertainty with many random-walk paths, a median line and a percentile band

**كيف:** Seeded random walks on Canvas (lighter alpha 0.1), draw over 1.5 s; median bold; shade the 5th–95th band; label the interval and n (scale honesty).

**المعاملات:** 1000 paths; α 0.1; 1.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** monte carlo · uncertainty · عدم يقين · fan chart · محاكاة · مسارات عشوائية · احتمالات · simulation · random walk

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-rammanq-f5a90f`
- `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/missingness-and-confidence.md`

#### 7. قدرات قريبة في العائلة

- `DATA-59` تحوّل المخططات / Chart morph (bars → donut / line / scatter) (install)
- `DATA-60` رسم بياني بخط اليد / Hand-drawn axis plot (seen)
- `DATA-62` هيستوغرام نقاط يصير منحنى جرس / Dot histogram resolving to a bell curve (seen)
- `DATA-63` رسم الدوال والمشتقة حيًّا / Live function & derivative tracer (seen)

### `DATA-62` — هيستوغرام نقاط يصير منحنى جرس / Dot histogram resolving to a bell curve

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل محاكاة تُسقط نقطة في عمودها والعدّاد يصل إلى N، ثم يُرسم منحنى طبيعي فوق الأكوام ويُظلل نطاق 5–95٪. / Each simulated result drops a dot into its bin while a counter ticks to N; then a normal curve draws over the stacks with the 5–95% band shaded.

**متى:** حين يريد المستخدم إظهار نتائج محاكاة تتراكم نقاطًا ثم تكشف منحنى التوزيع الطبيعي / when the user wants simulated results piling up as dots, then revealing a normal bell curve

**كيف:** N=500, dot 4 px, 20–40 ms stagger, mono counter; curve draw 600 ms; bright marker rises 400 ms ease-out; stacked-dot variant sorted descending with long tail in black (dot 6 px, 1.2 s); particle histogram with labelled spike.

**المعاملات:** N=500; dot 4 px; curve 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** histogram · bell curve · منحنى جرس · dots · توزيع طبيعي · محاكاة · تراكم النقاط · normal distribution · simulation

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-marouanegazouzi-6071d5`
- `style:pm-palashbagchi11-0a4b6b`
- `style:pm-ismailfahmi-557268`

#### 7. قدرات قريبة في العائلة

- `DATA-60` رسم بياني بخط اليد / Hand-drawn axis plot (seen)
- `DATA-61` مروحة مونت كارلو وعدم اليقين / Monte Carlo fan & uncertainty (seen)
- `DATA-63` رسم الدوال والمشتقة حيًّا / Live function & derivative tracer (seen)
- `DATA-64` راكب على خط المخطط / Glyph riding the chart path (seen)

### `DATA-63` — رسم الدوال والمشتقة حيًّا / Live function & derivative tracer

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** محوران: الأيسر للدالة مع مماس ونقطة تتبع x، والأيمن يرسم المشتقة أثرًا، وتسمية الميل تتحدث حيًّا. / Left axes show f with a tangent + dot following x(t); right axes trace f'(x); slope label updates live.

**متى:** حين يشرح الفيديو دالة رياضية ومشتقتها أو منحنى تسهيل بمؤشر يتحرك حيًا / when a video explains a math function and its derivative, or an easing curve, with a live tracer

**كيف:** x from −2 to 2 over 8–10 s linear; tangent ~1.2 units; slope label 2 decimals; progressive value table rows fade in with shift up; easing-graph variant: position vs time axes, cubic-bezier(.65,0,.35,1) with handles, playhead sweeping 1.5 s while a box moves with the same easing. manim is installable for this genre (pip install manim).

**المعاملات:** 8–10 s sweep; 2-decimal slope

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** math · مشتقة · function plot · easing graph · رياضيات · ميل المماس · تفاضل · derivative · manim

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-linearuncle-5d2bae`
- `style:pm-chatgptastra-0d95c7`

#### 7. قدرات قريبة في العائلة

- `DATA-61` مروحة مونت كارلو وعدم اليقين / Monte Carlo fan & uncertainty (seen)
- `DATA-62` هيستوغرام نقاط يصير منحنى جرس / Dot histogram resolving to a bell curve (seen)
- `DATA-64` راكب على خط المخطط / Glyph riding the chart path (seen)
- `DATA-65` حقل خطوط الجبال / Ridge-line wave field (seen)

### `DATA-64` — راكب على خط المخطط / Glyph riding the chart path

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أيقونة أو نقطة تُأخذ إحداثياتها من الخط أثناء رسمه (طائرة، كرة، نقطة تحويل من أ إلى ب). / A glyph or dot sampled from the drawing line (plane, ball, transfer dot A→B).

**متى:** حين يريد المستخدم أيقونة أو نقطة تسير على خط الرسم أثناء رسمه، كطائرة أو كرة من أ إلى ب / when the user wants an icon or dot travelling along a chart line as it draws, like a plane or ball from A to B

**كيف:** pos = path.getPointAtLength(p·L); angle from a second sample 1 px ahead; 1800 ms ease-in-out; chips spring 180/14/1 ≤600 ms; ring pulse at arrival; journey bar: dot on a line between labelled endpoints.

**المعاملات:** 1800 ms; spring 180/14/1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** path follow · getPointAtLength · راكب · تتبع المسار · أيقونة متحركة · حركة على خط · follow path · moving icon

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-utopyaszx-1b2f94/BRIEF.md`
- `style:pm-davidmarcus-a28a60`
- `style:pm-apoorvjain25-d24184`

#### 7. قدرات قريبة في العائلة

- `DATA-62` هيستوغرام نقاط يصير منحنى جرس / Dot histogram resolving to a bell curve (seen)
- `DATA-63` رسم الدوال والمشتقة حيًّا / Live function & derivative tracer (seen)
- `DATA-65` حقل خطوط الجبال / Ridge-line wave field (seen)
- `DATA-66` مبعثر الحد الفعّال / Scatter with frontier curve (seen)

### `DATA-65` — حقل خطوط الجبال / Ridge-line wave field

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 30–40 خطًا أفقيًا متراكبًا يزيحها ضجيج مع نتوء مركزي، والخطوط السفلى محجوبة، والتدرج من السماوي للأحمر. / 30–40 stacked horizontal lines displaced by noise with a central bump, lower lines occluded, cyan→red by row.

**متى:** حين يريد المستخدم خطوطًا أفقية متراكبة تتموج بالضجيج حول نتوء مركزي كقمم الجبال / when the user wants stacked horizontal lines rippling with noise around a central bump like mountain ridges

**كيف:** Each row: fill below the polyline with the background to occlude rows beneath; noise amplitude × gaussian centre bump; animate noise time 0.5; colour by row index.

**المعاملات:** amp centre 60 px; speed 0.5; 30–40 rows

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ridgeline · joy division · جبال خطوط · أمواج · تموج · خطوط متراكبة · waves · noise lines

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-shinskinakamoto-20190b`
- `style:pm-eyishazyer-af035b`

#### 7. قدرات قريبة في العائلة

- `DATA-63` رسم الدوال والمشتقة حيًّا / Live function & derivative tracer (seen)
- `DATA-64` راكب على خط المخطط / Glyph riding the chart path (seen)
- `DATA-66` مبعثر الحد الفعّال / Scatter with frontier curve (seen)
- `DATA-67` حلقة التقدم المخروطية / Conic-gradient progress ring (ready)

### `DATA-66` — مبعثر الحد الفعّال / Scatter with frontier curve

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط تقفز بتتابع ثم يُرسم المنحنى الحدّي وتُبرز أفضل نقطة. / Dots pop in sequence, then the frontier curve draws and the best point is highlighted.

**متى:** حين يريد المستخدم رسمًا مبعثرًا تظهر نقاطه بالتتابع ثم يُرسم المنحنى الحدي وتبرز أفضل نقطة / when the user wants a scatter plot whose dots pop in, then a frontier curve draws and the best point is highlighted

**كيف:** Dots scale 0→1 with 10 ms stagger (order by x for reading flow); curve stroke-dashoffset after the last dot; best point ring pulse + label.

**المعاملات:** stagger 10 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scatter · مبعثر · frontier · correlation · نقاط مبعثرة · أفضل خيار · علاقة متغيرين · scatter plot · best point

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-rammanq-f5a90f`

#### 7. قدرات قريبة في العائلة

- `DATA-64` راكب على خط المخطط / Glyph riding the chart path (seen)
- `DATA-65` حقل خطوط الجبال / Ridge-line wave field (seen)
- `DATA-67` حلقة التقدم المخروطية / Conic-gradient progress ring (ready)
- `DATA-68` دونات بخدعة المحيط 100 / Donut via r = 15.915 dasharray (ready)

### `DATA-67` — حلقة التقدم المخروطية / Conic-gradient progress ring

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة نسبة مرسومة بتدرج مخروطي زاويته متغير CSS مع قرص داخلي ورقم كبير في الوسط. / A percentage ring drawn with a conic gradient whose sweep is a CSS variable, inner disc and big centred numeral.

**متى:** حين يريد المستخدم حلقة نسبة مئوية بسيطة بتدرج مخروطي ورقم كبير في وسطها / when the user wants a simple percentage ring drawn with a conic gradient and a big centred number

**كيف:** el.style.setProperty('--progress', pct·3.6+'deg'); background: conic-gradient(colour var(--progress), track 0); ::after inner disc inset 13 px (v4: 4 px). Variants: quality dial conic-gradient(#6366f1 calc(var(--score)*1%), #e0e7ff 0) 110 px value 30 px #4338ca; SKCharts.ring 56 px (48 px phones) with ok/warn/bad classes. Animate the variable from one scalar (register it with @property for smooth CSS interpolation).

**المعاملات:** legacy 190 px #72dbc4 / inner #351848 / 38 px; KOSIF4 210 px #d9f3c7 / 43 px weight 500

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ring · conic-gradient · حلقة · progress · نسبة مئوية · دائرة تقدم · مؤشر جودة · percentage circle · css ring

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-audit-studio/styles.css:177`
- `kosif-audit-studio/app.js:514`
- `kosif-audit-studio/dashboard-capabilities.css`
- `kosif-earth-ci-fork/ui/components/charts.js:218`

#### 7. قدرات قريبة في العائلة

- `DATA-65` حقل خطوط الجبال / Ridge-line wave field (seen)
- `DATA-66` مبعثر الحد الفعّال / Scatter with frontier curve (seen)
- `DATA-68` دونات بخدعة المحيط 100 / Donut via r = 15.915 dasharray (ready)
- `DATA-69` مسح الدائرة بزاوية واحدة / Pie sweep (one eased angle) (documented)

### `DATA-68` — دونات بخدعة المحيط 100 / Donut via r = 15.915 dasharray

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دائرة نصف قطرها 15.915 محيطها 100 فيصبح طول الشرطة هو النسبة مباشرة، مع دخول القطاعات بدوران وتتابع. / A circle with r = 15.915 has circumference 100, so each dash length is the percentage; segments spin in staggered.

**متى:** حين يحتاج المستخدم رسم دونات SVG يكون فيه طول كل شرطة هو النسبة مباشرة / when the user needs an SVG donut where each dash length equals its percentage

**كيف:** SKCharts.donut(segs,{center,sub}): viewBox 42, stroke-width 6, dasharray (p−.6) (100−p+.6), dashoffset −cumulative; centre total + caption; entrance .dn-seg 0.75 s from opacity 0 scale(.84) rotate(−12°), delay i·50 ms; hover dims others to .26. (code snippet in references/powers/charts-data-infographic.md)

**المعاملات:** gap .6; 0.75 s; 50 ms stagger

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** donut · دونات · dasharray · 15.915 · حلقة مقسمة · نسب · رسم دائري · donut chart · svg circle

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/components/charts.js:223`
- `kosif-earth-ci-fork/ui/ds/components.css:322`

#### 7. قدرات قريبة في العائلة

- `DATA-66` مبعثر الحد الفعّال / Scatter with frontier curve (seen)
- `DATA-67` حلقة التقدم المخروطية / Conic-gradient progress ring (ready)
- `DATA-69` مسح الدائرة بزاوية واحدة / Pie sweep (one eased angle) (documented)
- `DATA-70` دونات متوهجة مع قائمة / Glowing donut with legend (seen)

### `DATA-69` — مسح الدائرة بزاوية واحدة / Pie sweep (one eased angle)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** زاوية مُسهَّلة واحدة تدور حول الدائرة والشرائح تُقطع منها فتبقى النسب صحيحة في كل إطار. / One eased angle sweeps the circle; slices are cut from it so proportions are true every frame.

**متى:** حين يريد المستخدم رسمًا دائريًا يتكشف بمسح زاوية واحدة لتبقى النسب صحيحة في كل إطار / when the user wants a pie chart revealed by one sweeping angle so proportions stay true every frame

**كيف:** A(t) = 360·e(t); slice k visible arc = clamp(A − start_k, 0, size_k); labels appear 120 ms after their slice completes; sorted from 12 o'clock clockwise.

**المعاملات:** 900 ms cubic-bezier(.65,0,.35,1); labels +120 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pie sweep · مسح الدائرة · رسم دائري متحرك · فطيرة · كشف دائري · pie chart · pie reveal

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/charts.md:38`

#### 7. قدرات قريبة في العائلة

- `DATA-67` حلقة التقدم المخروطية / Conic-gradient progress ring (ready)
- `DATA-68` دونات بخدعة المحيط 100 / Donut via r = 15.915 dasharray (ready)
- `DATA-70` دونات متوهجة مع قائمة / Glowing donut with legend (seen)
- `DATA-71` حلقة قياس مع عدّاد متزامن / Arc gauge with synced counter (install)

### `DATA-70` — دونات متوهجة مع قائمة / Glowing donut with legend

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قطاعات بشرطات تراكمية، والمميزة لها نسخة أعرض شفافة خلفها كتوهج، وقائمة صفوف بنقطة وتسمية وقيمة. / Segments as cumulative dashes; highlighted ones get a wider translucent duplicate behind for glow; legend rows with dot, label, value.

**متى:** حين يريد المستخدم دونات متوهجة على خلفية سوداء مع قائمة فئات بقيمها / when the user wants a glowing donut on black with a legend list of categories and their values

**كيف:** strokeDasharray=[len, C] with cumulative offset; glow copy width ×2 opacity 0.3; highlighted legend rows white, others #86868b; bg #000 with navy radial glow #0d2944; bar bends into this ring with no cut.

**المعاملات:** 8 categories; glow ×2 / 0.3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** donut · glow · legend · keynote · حلقة متوهجة · قائمة الفئات · خلفية سوداء · donut chart · category breakdown

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:infographic`

#### 7. قدرات قريبة في العائلة

- `DATA-68` دونات بخدعة المحيط 100 / Donut via r = 15.915 dasharray (ready)
- `DATA-69` مسح الدائرة بزاوية واحدة / Pie sweep (one eased angle) (documented)
- `DATA-71` حلقة قياس مع عدّاد متزامن / Arc gauge with synced counter (install)
- `DATA-72` مقاييس HUD الدائرية / HUD radial gauges (seen)

### `DATA-71` — حلقة قياس مع عدّاد متزامن / Arc gauge with synced counter

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** قوس رفيع يُرسم بينما تعدّ النسبة من نفس الاستدعاء، مع تلوين حسب الحالة وتجاوز 100٪ بالأحمر. / A thin arc draws while its percentage counts from the same call; colour by status, red past 100%.

**متى:** حين يريد المستخدم قوسًا يُرسم بينما تعد نسبته ويتلون حسب الحالة أو يحمر بعد 100٪ / when the user wants an arc that draws as its percentage counts, coloured by status and red past 100%

**كيف:** Basma ring: easeInOut over max(0.7, 0.55·d) s, arc from −90°, line width 0.2R, round caps, Rubik 900 %, label after 0.3 s, spring scale 0.7→1. Score ring 65→92 in 600 ms; amber→green when full (1.2 s); overage gauge: 60 outer ticks, stroke 10 px, colour lerps to red after 100%; stopwatch: arc + mm:ss counter 1.2 s; gauge arc cubic-bezier(0.22,1,0.36,1) 900 ms with the numeral on the same curve; at 100% swap to a check and burst 30 confetti pieces.

**المعاملات:** 600–1200 ms; stroke 10–14 px

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add mk-usage-arc

**الوسوم:** gauge · مقياس · arc · counter · عداد دائري · نسبة الإنجاز · ساعة إيقاف · score ring · stopwatch

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/components/mk-usage-arc/mk-usage-arc.html`
- `app/public/js/00_editor.js:508`
- `style:pm-sudeepsd-1a3485`
- `style:pm-gabrielbuzziv-4ff0c6`

#### 7. قدرات قريبة في العائلة

- `DATA-69` مسح الدائرة بزاوية واحدة / Pie sweep (one eased angle) (documented)
- `DATA-70` دونات متوهجة مع قائمة / Glowing donut with legend (seen)
- `DATA-72` مقاييس HUD الدائرية / HUD radial gauges (seen)
- `DATA-73` مقياس السائل والمنسوب / Liquid-fill & level gauges (seen)

### `DATA-72` — مقاييس HUD الدائرية / HUD radial gauges

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قوس خارجي للتقدم وحلقة علامات داخلية تدور و16 معينًا يمتلئ بالتتابع، أو حلقة بأربعة أقواس ملونة وخانة أخيرة تتدحرج. / Outer progress arc, rotating inner tick ring and 16 diamonds filling in sequence; or a 4-colour segmented ring with a rolling last digit.

**متى:** حين يريد المستخدم مقياسًا دائريًا بطابع الخيال العلمي بحلقات علامات تدور ومعينات تمتلئ / when the user wants a sci-fi HUD circular gauge with rotating tick rings and diamonds filling in

**كيف:** Arc 2 px white, ring 60 ticks; diamonds fill blue in sequence; centre dot; % counter below. Segmented ring: stroke 14 px, ticks every 30°, marker dot rides the ring, last digit rolls 300 ms easeInOut.

**المعاملات:** 60 ticks; stroke 2–14 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** HUD · gauge · radial · sci-fi · خيال علمي · واجهة مستقبلية · عداد دائري · futuristic ui · tick ring

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-himanshutwtxs-5f4b43`
- `style:pm-leonkohli-6dc01b`

#### 7. قدرات قريبة في العائلة

- `DATA-70` دونات متوهجة مع قائمة / Glowing donut with legend (seen)
- `DATA-71` حلقة قياس مع عدّاد متزامن / Arc gauge with synced counter (install)
- `DATA-73` مقياس السائل والمنسوب / Liquid-fill & level gauges (seen)
- `DATA-74` تعبئة النجوم والتقييم / Star-rating fill (install)

### `DATA-73` — مقياس السائل والمنسوب / Liquid-fill & level gauges

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دائرة أو أنبوب يمتلئ بسائل بسطح متموج وفقاعات، والرقم مربوط بنفس التقدم (حتى بكسور ¼ ½ ¾). / A circle or tube fills with wavy liquid and bubbles; the number is bound to the same progress (even ¼ ½ ¾ fractions).

**متى:** حين يريد المستخدم نسبة تُعرض كسائل يملأ دائرة أو أنبوبًا أو بطارية أو ميزان حرارة / when the user wants a percentage shown as liquid filling a circle, tube, battery or thermometer

**كيف:** Liquid: fill 1.2 s, wave amplitude 6 px, lime; pour 1.5–2.5 s easeInOutSine with a ruler arrow following the surface y and ticks appearing as the level passes; thermometer: hatched 45° 6 px fill, user threshold blue line, red dashed danger line with handwritten labels (range 100–260%); battery fill with % count ~600 ms; gradient bar green→red with threshold ticks.

**المعاملات:** fill 1.2 s; wave 6 px; pour 1.5–2.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** liquid · سائل · level · thermometer · امتلاء · بطارية · ميزان حرارة · fill gauge · battery

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-leadnotifi-e83f94`
- `style:pm-sarut0bisasuke-cefa43`
- `style:pm-nikolajankovic-ce4ff4`
- `style:pm-cansincengiz-me-cf68dd`

#### 7. قدرات قريبة في العائلة

- `DATA-71` حلقة قياس مع عدّاد متزامن / Arc gauge with synced counter (install)
- `DATA-72` مقاييس HUD الدائرية / HUD radial gauges (seen)
- `DATA-74` تعبئة النجوم والتقييم / Star-rating fill (install)
- `DATA-75` رادار المسح / Radar sweep with pings (seen)

### `DATA-74` — تعبئة النجوم والتقييم / Star-rating fill

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** طبقة لون تمسح صف النجوم حتى التقييم مع الحفاظ على النجمة الكسرية الأخيرة، والقيمة تعدّ معها. / A colour layer sweeps the star row to the rating, keeping the fractional last star, value counting in sync.

**متى:** حين يريد المستخدم عرض تقييم بالنجوم مثل 4.8 من 5 مع نجمة جزئية وعداد مرافق / when the user wants a star rating such as 4.8 of 5 with a partial last star and a synced count

**كيف:** Clip a filled star row to width = rating/count·100%; 600 ms; proof tiles flip in rotateX 90→0 400 ms with 120 ms stagger (star meter, % ring, count).

**المعاملات:** rating 4.8 / 5; star fill 600 ms

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add star-rating-fill

**الوسوم:** stars · تقييم · rating · social proof · نجوم · مراجعات · آراء العملاء · reviews · star rating

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/components/star-rating-fill/star-rating-fill.html`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/stat-bars-and-fills.md`
- `kosif-tool/styles/pm-ceowinkz-7c776b/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DATA-72` مقاييس HUD الدائرية / HUD radial gauges (seen)
- `DATA-73` مقياس السائل والمنسوب / Liquid-fill & level gauges (seen)
- `DATA-75` رادار المسح / Radar sweep with pings (seen)
- `DATA-76` نصف دائرة البرلمان وحلقة النقاط / Parliament hemicycle & dot ring (seen)

### `DATA-75` — رادار المسح / Radar sweep with pings

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقات متحدة المركز ووتد مخروطي يدور، والنقاط تضيء حين يمر المسح مع شارات تسمية. / Concentric rings with a rotating conic wedge; dots light up as the sweep passes, label chips fade in.

**متى:** حين يريد المستخدم رادارًا يدور ويضيء النقاط عند مرور المسح مع تسميات تظهر / when the user wants a rotating radar sweep that lights up dots as it passes, with labels fading in

**كيف:** 4 rings 1 px; conic-gradient wedge 6–8 s/rev (or 1 rev/2 s for urgency); dot pulse 300 ms when \|angle − sweep\| < 3°; orbital variant: ellipse ry = 0.4 rx with tags (STEADY/RISING) and a growing green line chart beside it.

**المعاملات:** 6–8 s/rev; pulse 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** radar · رادار · sweep · مسح · رصد · شاشة رادار · radar scan · ping

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-xelandre-363f00`
- `style:pm-blueoctopusai-dd17bd`
- `style:pm-marouanegazouzi-6071d5`

#### 7. قدرات قريبة في العائلة

- `DATA-73` مقياس السائل والمنسوب / Liquid-fill & level gauges (seen)
- `DATA-74` تعبئة النجوم والتقييم / Star-rating fill (install)
- `DATA-76` نصف دائرة البرلمان وحلقة النقاط / Parliament hemicycle & dot ring (seen)
- `DATA-77` مخطط الوافل: 100 نقطة / Waffle — 100 dots with synced percent (seen)

### `DATA-76` — نصف دائرة البرلمان وحلقة النقاط / Parliament hemicycle & dot ring

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط على أقواس متحدة المركز ملونة حسب الحزب مع العدد في الوسط، أو آلاف النقاط على حلقة ملونة حسب حصة الفئة. / Dots on concentric arcs coloured by party with the centre count, or thousands of dots on an annulus coloured by share.

**متى:** حين يريد المستخدم عرض مقاعد برلمان أو نتائج انتخابات بنقاط ملونة حسب الحزب / when the user wants parliament seats or election results shown as dots coloured by party

**كيف:** Place seats row by row on arcs (outer rows more seats), sort by party angle; fill in order with 5–10 ms stagger; dot ring: 4500 dots scattered in an annulus, category by cumulative angle.

**المعاملات:** 4500 dots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hemicycle · برلمان · dot ring · election · انتخابات · مقاعد · أحزاب · seats · parliament chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-triglyceee-bd5b08`
- `style:pm-jesscaroline7-1ff7cb`

#### 7. قدرات قريبة في العائلة

- `DATA-74` تعبئة النجوم والتقييم / Star-rating fill (install)
- `DATA-75` رادار المسح / Radar sweep with pings (seen)
- `DATA-77` مخطط الوافل: 100 نقطة / Waffle — 100 dots with synced percent (seen)
- `DATA-78` مصفوفة الوحدات: نقطة لكل عنصر / Unit dot matrix (one dot per item) (seen)

### `DATA-77` — مخطط الوافل: 100 نقطة / Waffle — 100 dots with synced percent

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة 10×10 والعدد المطابق للنسبة يتلون بالتتابع بينما عدّاد النسبة يصل معه في نفس الإطار. / A 10×10 grid where the matching count takes colour in sequence while a percent counter lands with it.

**متى:** حين يريد المستخدم إظهار نسبة مئوية كشبكة 10×10 تتلون نقاطها مع عداد النسبة / when the user wants a percentage shown as a 10×10 grid whose dots fill in sync with a percent counter

**كيف:** MG-043: 0–1 s grid, 1–3 s colouring with computed delay, 3–6 s explanation; state the unit ('كل نقطة = 1٪'); explain rounding; fill order right-to-left rows for Arabic (or random seeded order); 172-dot variant: dot 14 px gap 8 px, fill 1.5 s, salmon #e07b78 on grey #d9d9d9, outliers black; pictogram variant: 10×10 people icons, 10 ms stagger; isometric variant: 100 iso tiles, chosen ones extrude 50 ms stagger. (code snippet in references/powers/charts-data-infographic.md)

**المعاملات:** 10×10 = 100 cells; colouring 1.5–2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** waffle · وافل · dot grid · percent · شبكة نقاط · نسبة من مئة · أيقونات أشخاص · pictogram · 100 dots

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`
- `style:pm-palashbagchi11-0a4b6b`
- `style:infographic`
- `style:pm-blushpetal795-0c85c2`

#### 7. قدرات قريبة في العائلة

- `DATA-75` رادار المسح / Radar sweep with pings (seen)
- `DATA-76` نصف دائرة البرلمان وحلقة النقاط / Parliament hemicycle & dot ring (seen)
- `DATA-78` مصفوفة الوحدات: نقطة لكل عنصر / Unit dot matrix (one dot per item) (seen)
- `DATA-79` مقياس إلى شيء مألوف / Scale to a familiar object (documented)

### `DATA-78` — مصفوفة الوحدات: نقطة لكل عنصر / Unit dot matrix (one dot per item)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة لكل عنصر حقيقي (مثلًا 40×30) وتمييز مجموعة فرعية بلون التمييز. / One dot per real item (e.g. 40×30) with a subset highlighted in accent.

**متى:** حين يريد المستخدم تمثيل كل عنصر حقيقي بنقطة وإبراز مجموعة فرعية منها / when the user wants each real item shown as one dot with a highlighted subset

**كيف:** Canvas for >500 dots; state the unit; highlight subset with a 5–10 ms stagger or a sweep; can later become particles that fly into a bar (DATA-14 rules: particle = entity).

**المعاملات:** 40×30 = 1200 dots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** unit chart · وحدات · dot matrix · نقطة لكل عنصر · شبكة نقاط · مجموعة فرعية · dot grid · item dots

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-jesscaroline7-1ff7cb`
- `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md`

#### 7. قدرات قريبة في العائلة

- `DATA-76` نصف دائرة البرلمان وحلقة النقاط / Parliament hemicycle & dot ring (seen)
- `DATA-77` مخطط الوافل: 100 نقطة / Waffle — 100 dots with synced percent (seen)
- `DATA-79` مقياس إلى شيء مألوف / Scale to a familiar object (documented)
- `DATA-80` خريطة حرارية تقويمية / Calendar heatmap grid (ready)

### `DATA-79` — مقياس إلى شيء مألوف / Scale to a familiar object

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قيمة موثقة تتحول إلى صف وحدات بصرية مع مثال مقارنة واضح. / A documented value becomes a row of visual units with a clear comparison example.

**متى:** حين يكون الرقم كبيرًا أو مجردًا ويريد المستخدم تقريبه بمقارنته بشيء مألوف / when a number is large or abstract and the user wants it made tangible by comparing it to a familiar object

**كيف:** MG-050: 0–1 s value, 1–4 s units form, 4–7 s comparison; write 'تقريبًا' when rounding; never compare length with area without converting; icon size by area if sized (DATA-06).

**المعاملات:** 7 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scale · مقارنة · familiar object · مقياس · تشبيه · تقريب الأرقام · وحدات بصرية · comparison · visual units

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### 7. قدرات قريبة في العائلة

- `DATA-77` مخطط الوافل: 100 نقطة / Waffle — 100 dots with synced percent (seen)
- `DATA-78` مصفوفة الوحدات: نقطة لكل عنصر / Unit dot matrix (one dot per item) (seen)
- `DATA-80` خريطة حرارية تقويمية / Calendar heatmap grid (ready)
- `DATA-81` خريطة المخاطر 3×3 بأربع درجات / 3×3 risk heatmap with 4-step scale (ready)

### `DATA-80` — خريطة حرارية تقويمية / Calendar heatmap grid

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة أيام على طريقة GitHub (الأسابيع أعمدة والأيام صفوف) ملونة بمقياس يومي. / A GitHub-style grid of days (weeks as columns, weekdays as rows) coloured by a daily metric.

**متى:** حين يريد المستخدم شبكة أيام ملونة على طريقة GitHub تُظهر نشاطًا أو مقياسًا يوميًا / when the user wants a GitHub-style grid of days coloured by a daily metric or activity

**كيف:** Build week arrays from the first date; row = (weekday+6)%7 (Monday first); squares 10 px with 2 px gaps, left gutter 24 px, top 14 px for months; sequential ramp; animate fill by week column or random seeded order 40 ms stagger; Arabic month labels; serif-counter variant: 12×8 grid fill accelerating easeInExpo ~1.8 s with a big numeral in sync.

**المعاملات:** CELL 10, GAP 2, LEFT 24, TOP 14

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** calendar heatmap · تقويم · contribution grid · نشاط يومي · شبكة الأيام · خريطة حرارية · github · daily activity

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/1180-token-activity-graph/2788-token-activity-graph/graph.js`
- `style:pm-astrodevil-3f2054`
- `style:pm-fionntobin-97b7af`

#### 7. قدرات قريبة في العائلة

- `DATA-78` مصفوفة الوحدات: نقطة لكل عنصر / Unit dot matrix (one dot per item) (seen)
- `DATA-79` مقياس إلى شيء مألوف / Scale to a familiar object (documented)
- `DATA-81` خريطة المخاطر 3×3 بأربع درجات / 3×3 risk heatmap with 4-step scale (ready)
- `DATA-82` جدول حرارة الصفوف × الأعمدة / Matrix intensity table (ready)

### `DATA-81` — خريطة المخاطر 3×3 بأربع درجات / 3×3 risk heatmap with 4-step scale

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مصفوفة احتمال × أثر يتحدد لون خليتها من الدرجة، بتدرج أخضر → أحمر بأربع درجات للفاتح والداكن. / A likelihood × impact matrix whose cell colour comes from the score, 4-step green → red in light and dark.

**متى:** حين يحتاج المستخدم مصفوفة مخاطر بالاحتمالية والأثر ملونة من الأخضر إلى الأحمر / when the user needs a likelihood × impact risk matrix coloured green to red

**كيف:** SKCharts.heatmap(grid,{sel}): score ≥6 h4, ≥4 h3, ≥3 h2 else h1; cells ≥52 px, 700 16 px Latin digits; labels منخفض/متوسط/مرتفع, axes الأثر/الاحتمالية; hover scale 1.04; for video light cells in score order 60 ms stagger.

**المعاملات:** light #cfe8d6 #f3e2a6 #f1b98a #e98a86; dark #1f5a3b #6b5a17 #7a4219 #7f2626

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** risk matrix · خريطة المخاطر · heatmap · مصفوفة المخاطر · تقييم المخاطر · احتمالية · likelihood impact · risk assessment

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/components/charts.js:232`
- `kosif-earth-ci-fork/ui/ds/tokens.css:48`
- `kosif-earth-ci-fork/ui/ds/luxe.css:168`

#### 7. قدرات قريبة في العائلة

- `DATA-79` مقياس إلى شيء مألوف / Scale to a familiar object (documented)
- `DATA-80` خريطة حرارية تقويمية / Calendar heatmap grid (ready)
- `DATA-82` جدول حرارة الصفوف × الأعمدة / Matrix intensity table (ready)
- `DATA-83` مخطط بنفورد للرقم الأول / Benford first-digit chart (proven)

### `DATA-82` — جدول حرارة الصفوف × الأعمدة / Matrix intensity table

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول صفوف × أعمدة شفافية لون كل خلية تعبّر عن قيمتها (مثل البنود × الأشهر). / Rows × columns table where each cell's brand-colour alpha encodes its value (items × months).

**متى:** حين يريد المستخدم جدولًا تعبر فيه كثافة لون كل خلية عن قيمتها، كبنود مقابل أشهر / when the user wants a table whose cell colour intensity encodes values, such as items by month

**كيف:** SKCharts.matrix({rows, cols, values, fmt}); --a = max(.08, v/max); class hi (white text) when a > .55; reveal column by column.

**المعاملات:** min α .08; highlight > .55

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** matrix · heat table · جدول حرارة · جدول ملون · كثافة اللون · بنود وأشهر · heatmap table · color intensity

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/components/charts.js:260`

#### 7. قدرات قريبة في العائلة

- `DATA-80` خريطة حرارية تقويمية / Calendar heatmap grid (ready)
- `DATA-81` خريطة المخاطر 3×3 بأربع درجات / 3×3 risk heatmap with 4-step scale (ready)
- `DATA-83` مخطط بنفورد للرقم الأول / Benford first-digit chart (proven)
- `DATA-84` جدول يتكشف صفًّا صفًّا / Progressive table & status pills (seen)

### `DATA-83` — مخطط بنفورد للرقم الأول / Benford first-digit chart

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أعمدة SVG لتكرارات الرقم الأول المرصودة مقابل خط توقع بنفورد، مع تعليم الأرقام التي تنحرف بأكثر من 3 نقاط. / SVG bars of observed first-digit frequencies against the Benford expectation, flagging digits off by >3 points.

**متى:** حين يراجع المستخدم مبالغ ويريد كشف الشذوذ بمقارنة تكرار الرقم الأول بتوقع بنفورد / when auditing amounts for anomalies by comparing first-digit frequencies with the Benford expectation

**كيف:** benfordAnalysis(amounts) → template-string SVG: per digit a rect bar, a short expected line, an axis text; classes .bar/.hot/.expected/.axis. Animate bars rising, then expected ticks draw, then hot digits pulse.

**المعاملات:** viewBox 420×186; bar 26 / pitch 44 / rx 5; expected 30.1/17.6/12.5/9.7/7.9/6.7/5.8/5.1/4.6%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Benford · بنفورد · audit · fraud · تدقيق · احتيال · كشف التلاعب · anomaly detection · first digit

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-audit-studio/analytics.js:160`
- `kosif-audit-studio/app.js:1290`
- `kosif-audit-studio/styles.css:688`

#### 7. قدرات قريبة في العائلة

- `DATA-81` خريطة المخاطر 3×3 بأربع درجات / 3×3 risk heatmap with 4-step scale (ready)
- `DATA-82` جدول حرارة الصفوف × الأعمدة / Matrix intensity table (ready)
- `DATA-84` جدول يتكشف صفًّا صفًّا / Progressive table & status pills (seen)
- `DATA-85` تشريح بطاقة المؤشر / KPI card anatomy (documented)

### `DATA-84` — جدول يتكشف صفًّا صفًّا / Progressive table & status pills

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول بعمودين وترويسة يُضاف صف مع كل خطوة، أو جدول مرتب برؤوس mono وشارات حالة حمراء. / A two-column table appends a row each step, or a ranked table with mono headers and red status pills.

**متى:** حين يريد المستخدم جدولًا قصيرًا يظهر صفًا صفًا في الفيديو أو جدولًا مرتبًا بشارات حالة / when the user wants a short table revealed row by row in video, or a ranked table with status pills

**كيف:** Row height ~6% H; each row fades in with shift up 12–20 px; header coloured like its series; ranked variant: rows slide up 120 ms stagger, right-aligned values, dead row tinted pink, pills #fbe3e3/#a8484a; end with an arrow note. Keep ≤6 rows on screen (no web tables).

**المعاملات:** row stagger 120 ms; ≤6 rows

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** table · جدول · status pills · جدول متحرك · صفوف · شارات الحالة · animated table · rows

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-linearuncle-5d2bae`
- `style:pm-palashbagchi11-0a4b6b`

#### 7. قدرات قريبة في العائلة

- `DATA-82` جدول حرارة الصفوف × الأعمدة / Matrix intensity table (ready)
- `DATA-83` مخطط بنفورد للرقم الأول / Benford first-digit chart (proven)
- `DATA-85` تشريح بطاقة المؤشر / KPI card anatomy (documented)
- `DATA-86` ثلاثية بطاقات الأرقام والإثبات / Stat-tile trio & proof cards (seen)

### `DATA-85` — تشريح بطاقة المؤشر / KPI card anatomy

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الرقم يستحق الشاشة فقط إن قال أيضًا: جيد أم سيئ (الفجوة عن الهدف) وأفضل أم أسوأ (الاتجاه). / A headline number earns screen time only with good/bad (gap to target) and better/worse (trend).

**متى:** حين يصمم المستخدم بطاقة مؤشر أداء ويحتاج الرقم مع الهدف والفرق والاتجاه / when designing a KPI card where the number needs its target, signed gap and trend

**كيف:** Three layers: Number (right units, minimal decimals) · Meaning (target or prior period + signed gap with arrow) · Context (sparkline or tiny breakdown, only if useful). Neutral colour on target, deep red only when off. Tile = value + unit + delta + period + source. ≤3 tiles per frame, spring 14-120 pop, counters offset 600 ms, one highlighted at the end.

**المعاملات:** ≤3–4 tiles/frame; counters offset 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** KPI · بطاقة · delta · target · مؤشر أداء · الهدف · الاتجاه · metric card · trend

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/3455-business-analytics/14162-kpi-dashboard-design/SKILL.md`
- `kosif-one/tools/kosif-omni/skills/kosif-web-design/references/web-playbook.md`
- `kosif-tool/playbooks/charts.md:97`

#### 7. قدرات قريبة في العائلة

- `DATA-83` مخطط بنفورد للرقم الأول / Benford first-digit chart (proven)
- `DATA-84` جدول يتكشف صفًّا صفًّا / Progressive table & status pills (seen)
- `DATA-86` ثلاثية بطاقات الأرقام والإثبات / Stat-tile trio & proof cards (seen)
- `DATA-87` افتتاحية الرقم البطل / Hero-number opener card (seen)

### `DATA-86` — ثلاثية بطاقات الأرقام والإثبات / Stat-tile trio & proof cards

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاث بطاقات ملونة تعدّ إلى قيمها بينما خط يُرسم تحتها، أو عمود أرقام بجانب بطاقة أعمدة وخط وشارة «+301٪». / Three coloured tiles count up while a line draws beneath, or a column of numbers beside a bars+line card with a '+301%' chip.

**متى:** حين يريد المستخدم ثلاث بطاقات أرقام تعد مع خط يُرسم أو بطاقة إثبات بنسبة نمو / when the user wants three stat tiles counting up with a line drawing, or a proof card with a growth chip

**كيف:** Count 800 ms easeOutExpo, line dashoffset 1.2 s; stats row: 3 columns split by 1 px rules drawing downward, count 600–800 ms, mono source tag; stacked cards slide 400 ms ease-out stagger 250 ms, number counts 600 ms as it lands; analytics card: header 'Views last 30 days', big number, green delta chip, line 700 ms, endpoint pops; card radius 16 px, stagger 120 ms; inspector panel slides x 100%→0 400 ms with +35%→+50% metric; analytics drawer slides up while the line draws 900 ms ease-out and counters tick 800 ms easeOutQuart.

**المعاملات:** 800 ms count; 1.2 s line; stagger 120–250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stat tiles · بطاقات · dashboard reveal · proof card · بطاقات الأرقام · نسبة النمو · لوحة تحليلات · analytics card · growth

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-86` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-bizibeast-10f264`
- `style:pm-jasonzhou1993-8595e0`
- `style:pm-samuel-yostt-891f87`
- `style:pm-motiondsgnr-9dcfa6`

#### 7. قدرات قريبة في العائلة

- `DATA-84` جدول يتكشف صفًّا صفًّا / Progressive table & status pills (seen)
- `DATA-85` تشريح بطاقة المؤشر / KPI card anatomy (documented)
- `DATA-87` افتتاحية الرقم البطل / Hero-number opener card (seen)
- `DATA-88` سجل HyperFrames للبيانات / HyperFrames data registry (components & blocks) (install)

### `DATA-87` — افتتاحية الرقم البطل / Hero-number opener card

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رقم ضخم في الوسط أو اليسار مع سطرين تحته وشارات مصدر تقفز، أو رقم رفيع بخط serif. / A huge number centred or left with a two-line caption and source pills popping in, or a thin serif numeral.

**متى:** حين يبدأ الفيديو برقم ضخم يلفت الانتباه مع تعليق قصير وشارات مصدر / when a video opens on a huge attention-grabbing number with a short caption and source pills

**كيف:** Number 18–25% of frame height; tracked caption below; source pills pop (spring); italic byline; counter 600 ms easeOut; supporting graphic on the other side; metric-pair variant: two big numbers in columns beside a screenshot.

**المعاملات:** number 18–25% H; count 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hero number · افتتاحية · opener · big number · رقم كبير · بداية الفيديو · مقدمة · intro stat · headline number

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-87` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:pm-henkvaness-0e06af`
- `style:pm-blushpetal795-0c85c2`
- `style:pm-madebyjmayala-b9204d`

#### 7. قدرات قريبة في العائلة

- `DATA-85` تشريح بطاقة المؤشر / KPI card anatomy (documented)
- `DATA-86` ثلاثية بطاقات الأرقام والإثبات / Stat-tile trio & proof cards (seen)
- `DATA-88` سجل HyperFrames للبيانات / HyperFrames data registry (components & blocks) (install)
- `DATA-89` مخططات مشاهد البيانات في HyperFrames / HyperFrames data blueprints & categories (documented)

### `DATA-88` — سجل HyperFrames للبيانات / HyperFrames data registry (components & blocks)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI) |

**ما هي:** مكوّنات وكتل جاهزة للبيانات في نسخة HyperFrames المحلية: عدّادات، حلقات، أعمدة، خطوط، سباقات، وجدران شعارات. / Ready data components/blocks in the local HyperFrames copy: counters, rings, bars, lines, races, logo walls.

**متى:** حين يحتاج المستخدم مكونات بيانات جاهزة في HyperFrames كعدادات وحلقات وأعمدة وسباقات / when the user needs ready HyperFrames data blocks: counters, rings, bars, lines, races or logo walls

**كيف:** npx hyperframes add <name> copies into compositions/; mount on a class="clip" div with data-composition-src + data-start/data-duration/data-track-index; overrides as JSON in data-variable-values; one paused GSAP timeline, fromTo explicit states, transforms/opacity only. See the table below for every item and its variables. Chip-grid variant (5×N rounded chips coloured by category, 40 ms stagger) fits the same mount pattern.

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add chart-story

**الوسوم:** HyperFrames · registry · components · GSAP · مكونات جاهزة · كتل · جدار الشعارات · ready blocks · logo wall

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-88` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/components/chart-story/chart-story.html`
- `kosif-one/vendor/hyperframes/registry/blocks/data-chart/data-chart.html`
- `kosif-one/vendor/hyperframes/docs/catalog/components/count-up.mdx`
- `kosif-one/vendor/hyperframes/registry/examples/nyt-graph/index.html`

#### 7. قدرات قريبة في العائلة

- `DATA-86` ثلاثية بطاقات الأرقام والإثبات / Stat-tile trio & proof cards (seen)
- `DATA-87` افتتاحية الرقم البطل / Hero-number opener card (seen)
- `DATA-89` مخططات مشاهد البيانات في HyperFrames / HyperFrames data blueprints & categories (documented)
- `DATA-90` ستايل الإنفوجرافيك بأسلوب أبل / Keynote infographic style (seen)

### `DATA-89` — مخططات مشاهد البيانات في HyperFrames / HyperFrames data blueprints & categories

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** وصفات متعددة المراحل: عدّ تصاعدي مع كاميرا تخترق شبكة إحصاءات، محور نجوم، فئة «رقم إحصائي»، فئة «رسوم»، و«الأصل يصبح الرسم». / Multi-phase recipes: count-up with a camera pushing through a tilted stat grid, constellation hub, 'stat hit', 'charts', and 'asset fusion' (the object becomes the chart).

**متى:** عند تخطيط مشهد بيانات متعدد المراحل في HyperFrames واختيار وصفة جاهزة لكل لقطة / when planning a multi-phase HyperFrames data scene and picking a ready blueprint for each beat

**كيف:** Pick by role from blueprints-index.md and cite the blueprint id per beat: dataviz-countup (4–12 s: ring/number → trend chart → tilted stat grid → land on hero metric); constellation-hub (5–8 s, end card ~2.5 s); category stat (~4–6 s hero count + ring); charts (one chart one message); asset-fusion (~5–8 s: straw → gauge, liquid → pie).

**المعاملات:** 4–12 s per blueprint

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** blueprint · asset fusion · stat hit · shot plan · وصفة مشهد · خطة اللقطات · عد تصاعدي · dataviz countup · scene recipe

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-89` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/dataviz-countup.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/constellation-hub.md`
- `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/asset-fusion/module.md`
- `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/stat/module.md`

#### 7. قدرات قريبة في العائلة

- `DATA-87` افتتاحية الرقم البطل / Hero-number opener card (seen)
- `DATA-88` سجل HyperFrames للبيانات / HyperFrames data registry (components & blocks) (install)
- `DATA-90` ستايل الإنفوجرافيك بأسلوب أبل / Keynote infographic style (seen)
- `DATA-91` ستايل البيانات المتحركة الداكن / Data-in-Motion dark style (documented)

### `DATA-90` — ستايل الإنفوجرافيك بأسلوب أبل / Keynote infographic style

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قصة بيانات على أسود بتوهج أزرق: كل شكل يتحول إلى التالي بلا قطع، أرقام تتدحرج كعداد المسافات، وتمييز واحد بكامل الوضوح. / A data story on black with blue glow: every shape morphs into the next with no cuts, odometer numbers, one highlight at 100%.

**متى:** حين يريد المستخدم إنفوجرافيك بأسلوب أبل على خلفية سوداء بتوهج أزرق وتحولات بلا قطع / when the user wants a keynote-style data story on black with blue glow and cut-free morphs

**كيف:** Palette #000000 bg, glow #0d2944/#021422, accents #4b89d1 #1239a0 #5b5be0, highlight #64d2ff, text #f5f5f7 / grey #86868b; IBM Plex Sans Arabic 300/500/700 (eyebrow grey ~2.5% H over bold white headline ~5%, hero number ~12–15% H with vertical cyan→blue gradient); lines rise from a mask translateY 70%→0 with blur clearing; counters 700–1000 ms ease-out cubic; one highlight 100%, others 35–45%; sfx whoosh/tick/drop; 16:9 ~28 s; scaffold python3 tools/kosif.py scaffold infographic <dir>.

**المعاملات:** 28 s; 30 fps; 2.0 wps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** keynote · أبل · infographic · morph · عرض تقديمي · تحول بلا قطع · خلفية سوداء · dark data story · odometer

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-90` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `style:infographic`
- `kosif-tool/styles/infographic/SKILL.md`
- `app/public/js/10_studio.js:701`

#### 7. قدرات قريبة في العائلة

- `DATA-88` سجل HyperFrames للبيانات / HyperFrames data registry (components & blocks) (install)
- `DATA-89` مخططات مشاهد البيانات في HyperFrames / HyperFrames data blueprints & categories (documented)
- `DATA-91` ستايل البيانات المتحركة الداكن / Data-in-Motion dark style (documented)
- `DATA-92` لوحات ألوان الرسوم / Chart palettes (categorical, sequential, semantic) (proven)

### `DATA-91` — ستايل البيانات المتحركة الداكن / Data-in-Motion dark style

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوح داكن بلوحة فئات آمنة لعمى الألوان، أعمدة تنمو بتسهيل خروج، أرقام تعد، ومحور ثابت. / Dark board with a CVD-safe categorical palette, ease-out bars, counting numbers, fixed axis.

**متى:** حين يريد المستخدم ستايل جاهزًا لفيديو بيانات داكن بألوان آمنة لعمى الألوان وأعمدة وعدادات / when the user wants a ready dark data-video style with colour-blind-safe series, growing bars and counters

**كيف:** bg #0D1B2A; series #3B82F6 #F59E0B #10B981 #EF4444 #A855F7; stagger 60 ms; tabular-nums; IBM Plex Sans Arabic 700; no animated pie, no 3D; values computed in code from clean CSV; source in the corner.

**المعاملات:** stagger 60 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** style · dark · ستايل · palette · خلفية داكنة · عمى الألوان · فيديو بيانات · colorblind safe · data video

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-91` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/trend-animation-styles/references/styles.md`
- `100-superskills/skills/data-in-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-89` مخططات مشاهد البيانات في HyperFrames / HyperFrames data blueprints & categories (documented)
- `DATA-90` ستايل الإنفوجرافيك بأسلوب أبل / Keynote infographic style (seen)
- `DATA-92` لوحات ألوان الرسوم / Chart palettes (categorical, sequential, semantic) (proven)
- `DATA-93` رموز بطاقات البيانات التقنية / Tech-doc data-card tokens (documented)

### `DATA-92` — لوحات ألوان الرسوم / Chart palettes (categorical, sequential, semantic)

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوحات فئات بترتيب ثابت للهوية لا للترتيب، مختبرة لعمى الألوان، مع تدرجات حرارة ومخاطر وإجهاد. / Fixed-order categorical palettes (identity, never rank), CVD-checked, plus heat, risk and utilisation ramps.

**متى:** حين يختار المستخدم ألوان سلاسل الرسم أو تدرجات الحرارة والمخاطر مع مراعاة عمى الألوان / when choosing chart series colours or heat and risk ramps that stay colour-blind safe

**كيف:** See the palette table below. Series colours bound to semantic anchors with a uniqueness test (passed in this container: node --test kosif-audit-pro/tests/palette.test.mjs → fail 0). 8-slot set worst adjacent ΔE 9.1 light / 8.4 dark; slots in identity order; kosif looks override c1/c2 with brand colours. Theme-aware series: shadcn ChartContainer injects per-series CSS vars with separate light/dark values (Recharts; recharts itself was not probed in this container).

**المعاملات:** ≤4 hues per chart (playbook); ≤6–8 total

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** palette · ألوان · CVD · categorical · لوحة ألوان · عمى الألوان · تدرج لوني · color scheme · sequential ramp

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-92` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-audit-pro/tests/palette.test.mjs`
- `kosif-audit-pro/app/globals.css:40`
- `kosif-earth-ci-fork/ui/ds/tokens.css:111`
- `kosif-audit-pro/components/ui/chart.tsx`

#### 7. قدرات قريبة في العائلة

- `DATA-90` ستايل الإنفوجرافيك بأسلوب أبل / Keynote infographic style (seen)
- `DATA-91` ستايل البيانات المتحركة الداكن / Data-in-Motion dark style (documented)
- `DATA-93` رموز بطاقات البيانات التقنية / Tech-doc data-card tokens (documented)
- `DATA-94` لوحة التوأم الإنشائي / Structural-twin dashboard & utilisation ramp (proven)

### `DATA-93` — رموز بطاقات البيانات التقنية / Tech-doc data-card tokens

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مظهر توثيق فاتح ثابت: IBM Plex Sans للنص وIBM Plex Mono بأرقام ثابتة للأرقام، وصفحة رمادية زرقاء ولوحة بيضاء. / A consistent light documentation look: IBM Plex Sans body, Plex Mono tabular numbers, blue-grey page and white panel.

**متى:** حين يريد المستخدم مظهر توثيق تقني فاتحًا وموحدًا لبطاقات البيانات وأرقامها / when the user wants a consistent light technical-docs look for data cards and numbers

**كيف:** CSS custom properties; Arabic pairs with IBM Plex Sans Arabic; page #e8ecf2, panel border #cdd5e1, ink #1d2632, muted #5d6a7a / #98a3b3, accents #1f6fe5 #e2640f #15a05a #2f6fe0 #dc2b3e.

**المعاملات:** #e8ecf2 #cdd5e1 #1d2632 …

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tokens · IBM Plex · figure · توثيق تقني · خطوط · ألوان الواجهة · design tokens · light theme

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-93` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/3186-create-figure/13532-create-figure/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-91` ستايل البيانات المتحركة الداكن / Data-in-Motion dark style (documented)
- `DATA-92` لوحات ألوان الرسوم / Chart palettes (categorical, sequential, semantic) (proven)
- `DATA-94` لوحة التوأم الإنشائي / Structural-twin dashboard & utilisation ramp (proven)
- `DATA-95` ملف إكسل برسوم أصلية / Excel workbook with native charts (proven)

### `DATA-94` — لوحة التوأم الإنشائي / Structural-twin dashboard & utilisation ramp

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صفحة HTML مستقلة: مخطط جملون ملون حسب نسبة الإجهاد، شريط حمل، تبويبات قبل/بعد، ترتيب الانهيار، وبطاقات أرقام تتحول إلى قائمة. / Self-contained HTML lab: truss coloured by utilisation, load slider, baseline/swap tabs, failure ranking, stat tiles turning into a list.

**متى:** حين يريد المستخدم لوحة HTML هندسية تلون الجملون حسب نسبة الإجهاد مع شريط حمل / when the user wants an engineering HTML dashboard colouring a truss by utilisation with a load slider

**كيف:** python twin_dashboard.py report.json --out lab.html; embedded JSON; SVG 660×400 projected from node bounds; load .10–4.00× step .05; colour(u): u≥1 #ff907a (dashed 12/9), ≥.72 #ffe083, ≥.35 #b4ed88, else #8cffc0; HUD peak text same thresholds; grid 1.85fr/1fr collapses under 850 px; prefers-reduced-motion respected; bg #081213, lime #D0FF6A, mint #9DFFB4.

**المعاملات:** thresholds .35/.72/1.0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dashboard · توأم · utilisation · engineering · هندسة إنشائية · جملون · إجهاد · truss · structural

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-94` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/examples/structural-twin-demo.html:1`
- `kosif-studio/motion/twin_dashboard.py:1`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:107`

#### 7. قدرات قريبة في العائلة

- `DATA-92` لوحات ألوان الرسوم / Chart palettes (categorical, sequential, semantic) (proven)
- `DATA-93` رموز بطاقات البيانات التقنية / Tech-doc data-card tokens (documented)
- `DATA-95` ملف إكسل برسوم أصلية / Excel workbook with native charts (proven)
- `DATA-96` مكتبات الرسوم كإطارات فيديو / Chart libraries as video frames (install)

### `DATA-95` — ملف إكسل برسوم أصلية / Excel workbook with native charts

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ملف .xlsx كامل في استدعاء واحد: جداول إكسل حقيقية، ترتيب، تنسيقات، مجاميع SUM حية، أوراق RTL، ورسم أعمدة/خط/دائري. / A finished .xlsx in one call: real Excel tables, sorting, formats, live SUM totals, RTL sheets and a bar/column/line/pie chart.

**متى:** حين يطلب المستخدم ملف إكسل جاهزًا بجداول ومجاميع ورسم بياني أصلي داخله / when the user asks for a ready Excel file with tables, totals and a native chart inside

**كيف:** kosif_sheet_build sheets=[{name, headers, rows, sort, formats{money\|percent\|date\|integer\|code}, totals, chart{type:bar\|column\|line\|pie, labels, values[], title}, rtl:true}] (openpyxl); kosif_db exports a SELECT to xlsx/csv with chart. Live Excel automation (kosif_excel, COM) works only on Windows with Excel open — not here.

**المعاملات:** chart 18×9 cm beside the table; TableStyleMedium2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Excel · xlsx · إكسل · openpyxl · ملف اكسل · جدول بيانات · شيت · spreadsheet · excel chart

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-95` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/office.py:226`
- `kosif-one/tools/kosif-omni/mcp-server/tests/test_office.py:56`
- `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/office_live.py`

#### 7. قدرات قريبة في العائلة

- `DATA-93` رموز بطاقات البيانات التقنية / Tech-doc data-card tokens (documented)
- `DATA-94` لوحة التوأم الإنشائي / Structural-twin dashboard & utilisation ramp (proven)
- `DATA-96` مكتبات الرسوم كإطارات فيديو / Chart libraries as video frames (install)
- `DATA-97` مشاهد بسمة للبيانات وقوالب أفلامها / Basma chart scenes & data-film templates (key)

### `DATA-96` — مكتبات الرسوم كإطارات فيديو / Chart libraries as video frames

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | d3 ISC; echarts Apache-2.0; chart.js MIT; vega/vega-lite BSD-3-Clause |

**ما هي:** D3 أو ECharts أو Chart.js أو Vega-Lite داخل صفحة تُرندر إطارًا إطارًا، بشرط تعطيل حركتها الداخلية وقيادتها بالزمن. / D3, ECharts, Chart.js or Vega-Lite inside a page rendered frame by frame, with their own animation disabled and driven by time.

**متى:** حين يريد المستخدم استخدام D3 أو ECharts أو Chart.js داخل فيديو يُرندر إطارًا إطارًا / when the user wants D3, ECharts or Chart.js charts inside a video rendered frame by frame

**كيف:** Set animation:false (Chart.js/ECharts) and redraw from data(t) inside window.__kosif.seek(t); D3: compute layouts (d3-hierarchy treemap, d3-sankey, d3-geo) and interpolate attributes yourself; never ship default library styling (restyle: no legends, direct labels, palette DATA-92); render with node tools/render_html.cjs.

**التثبيت:** npm i d3@7.9.0 # or: echarts@6.1.0 \| chart.js@4.5.1 \| vega@6.4.0 vega-lite@6.5.0

**الوسوم:** d3 · echarts · chart.js · vega · libraries · مكتبات الرسوم · رندر فيديو · تحويل الرسم لفيديو · frame render · vega-lite

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-96` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md`
- `kosif-tool/tools/render_html.cjs`

#### 7. قدرات قريبة في العائلة

- `DATA-94` لوحة التوأم الإنشائي / Structural-twin dashboard & utilisation ramp (proven)
- `DATA-95` ملف إكسل برسوم أصلية / Excel workbook with native charts (proven)
- `DATA-97` مشاهد بسمة للبيانات وقوالب أفلامها / Basma chart scenes & data-film templates (key)
- `DATA-98` إنفوجرافيك مولَّد مستند إلى بحث / Search-grounded infographic generation (key)

### `DATA-97` — مشاهد بسمة للبيانات وقوالب أفلامها / Basma chart scenes & data-film templates

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | owner code; scenes generated via the Anthropic API |

**ما هي:** مشاهد جاهزة في محرر بسمة (عدّاد، أعمدة، حلقة، قائمة) وفئة «أفلام البيانات» بخمسة قوالب يكتب Claude مشاهدها. / Ready scenes in the Basma editor (counter, bars, ring, list) and a 'charts' film category with five templates whose scenes Claude codes.

**متى:** حين يعمل المستخدم في محرر بسمة ويريد مشاهد بيانات جاهزة أو قالب فيلم بيانات / when working in the Basma editor and wanting ready data scenes or a data-film template

**كيف:** TEMPLATES.counter (lerp easeOut over max(0.6, 0.6d) s, Rubik 900 at 20% of min side), TEMPLATES.bars (2–5 bars, spring z .6 w 12, stagger 0.12 s from 0.25 s, IBM Plex Sans Arabic 700 labels), TEMPLATES.ring, TEMPLATES.list (0.32 s stagger, drawn tick). Film templates: data-story 12 s, bar-race 12 s, report-card (tiles + ring + sparkline), price-move (candle/line follow cam), survey (100-dot grid wave), plus milestone, dashboard-reveal, compare, math; rule: never invent figures. Coded film scenes call the Anthropic API (needs a key); the app itself needs its npm install.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Basma · بسمة · templates · Anthropic API · فيلم بيانات · قوالب جاهزة · مشاهد جاهزة · data film · bar race

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-97` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `app/public/js/00_editor.js:458`
- `app/public/js/00_editor.js:469`
- `app/public/js/00_editor.js:2007`
- `app/public/js/00_editor.js:1777`

#### 7. قدرات قريبة في العائلة

- `DATA-95` ملف إكسل برسوم أصلية / Excel workbook with native charts (proven)
- `DATA-96` مكتبات الرسوم كإطارات فيديو / Chart libraries as video frames (install)
- `DATA-98` إنفوجرافيك مولَّد مستند إلى بحث / Search-grounded infographic generation (key)
- `DATA-99` مشاهد السرد بالتمرير كبيانات / Scrollytelling scenes as data (documented)

### `DATA-98` — إنفوجرافيك مولَّد مستند إلى بحث / Search-grounded infographic generation

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | needs a Google Gemini API key (paid service) |

**ما هي:** نماذج صور Gemini تبحث عن حقائق حالية وترسمها إنفوجرافيك في طلب واحد. / Gemini image models look up current facts and render them as an infographic in one request.

**متى:** حين يريد المستخدم توليد إنفوجرافيك بالذكاء الاصطناعي من حقائق حديثة يبحث عنها النموذج / when the user wants an AI-generated infographic built from current facts the model looks up

**كيف:** Prompt in three parts: what to search, what to extract/analyse, how to render (chart type, theme). Treat every number as unverified: re-set exact figures in code (DATA-10) before publishing; never ship the raster as the chart.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Gemini · AI infographic · مولد · ذكاء اصطناعي · توليد صورة · بحث · image generation · fact lookup

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-98` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`

#### 7. قدرات قريبة في العائلة

- `DATA-96` مكتبات الرسوم كإطارات فيديو / Chart libraries as video frames (install)
- `DATA-97` مشاهد بسمة للبيانات وقوالب أفلامها / Basma chart scenes & data-film templates (key)
- `DATA-99` مشاهد السرد بالتمرير كبيانات / Scrollytelling scenes as data (documented)

### `DATA-99` — مشاهد السرد بالتمرير كبيانات / Scrollytelling scenes as data

| الحقل | القيمة |
|---|---|
| العائلة | `charts-data-infographic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/charts-data-infographic.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قصص بيانات يتغير فيها المشهد مع التقدم: كل مشهد يعلن نصه وحالته البصرية وطبقة بياناته ومدى تقدمه. / Author-led data stories where state changes with progress: each scene declares text, visual state, data layer and progress range.

**متى:** حين يريد المستخدم قصة بيانات تتغير مشاهدها مع التمرير أو تحويلها إلى فيديو بخط زمني / when the user wants a scroll-driven data story, or wants to turn one into a timeline video

**كيف:** Techniques: graphic sequence, animated transition, pan-and-zoom, sticky side-by-side, parallax depth. For video replace scroll progress with timeline time: progress = (t − scene.start)/scene.dur; keep a reduced-motion/static fallback frame per scene.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scrollytelling · سرد · scenes · قصة تفاعلية · تمرير · بارالاكس · scroll story · parallax

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:DATA-99` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `starter-remotion`.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DATA-97` مشاهد بسمة للبيانات وقوالب أفلامها / Basma chart scenes & data-film templates (key)
- `DATA-98` إنفوجرافيك مولَّد مستند إلى بحث / Search-grounded infographic generation (key)

