# `hand-drawn-draw-on` — الرسم والأشكال والتصميم (65 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/hand-drawn-draw-on.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/drawing.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`DRAW-01` رسم المسار بإزاحة الشرطة](#draw-01--رسم-المسار-بإزاحة-الشرطة--svg-stroke-draw-on)
- [`DRAW-02` قلم مكتبة الحركة برأس يهبط](#draw-02--قلم-مكتبة-الحركة-برأس-يهبط--kit-drawpath-with-landing-head--flowdash)
- [`DRAW-03` سرعة القلم والرفع](#draw-03--سرعة-القلم-والرفع--pen-speed--lifts)
- [`DRAW-04` ترتيب الرسم البشري ووصفة «ارسم وسمِّ»](#draw-04--ترتيب-الرسم-البشري-ووصفة-ارسم-وسمِّ--human-draw-order--draw-and-label)
- [`DRAW-05` رابط مخطط برأس سهم](#draw-05--رابط-مخطط-برأس-سهم--diagram-edge-draw-on-with-arrowhead)
- [`DRAW-06` رأس يتبع الخط: يد، ماركر، طباشيرة](#draw-06--رأس-يتبع-الخط-يد-ماركر-طباشيرة--pen-tip-followers-hand-marker-chalk)
- [`DRAW-07` رأس متوهج يجرّ الخط](#draw-07--رأس-متوهج-يجرّ-الخط--glowing-head-draw)
- [`DRAW-08` كشف متعدد الأجزاء بالطول التراكمي](#draw-08--كشف-متعدد-الأجزاء-بالطول-التراكمي--cumulative-length-multi-segment-reveal)
- [`DRAW-09` سلامة رسم المسارات](#draw-09--سلامة-رسم-المسارات--svg-draw-on-safety)
- [`DRAW-10` نهر يمتلئ ثم يجري](#draw-10--نهر-يمتلئ-ثم-يجري--river-fill-then-flow)
- [`DRAW-11` المحراب بقلم ذهبي](#draw-11--المحراب-بقلم-ذهبي--gold-pen-arch-draw-on)
- [`DRAW-12` رسوم خطية صغيرة فوق الفيديو](#draw-12--رسوم-خطية-صغيرة-فوق-الفيديو--line-micro-graphics-over-footage)
- [`DRAW-13` أيقونات المعنى المرسومة](#draw-13--أيقونات-المعنى-المرسومة--meaning-icons-drawn-on)
- [`DRAW-14` قوالب موشن بالقلم](#draw-14--قوالب-موشن-بالقلم--pen-drawn-motion-templates)
- [`DRAW-15` كتابة بقناع فرشاة من اليمين](#draw-15--كتابة-بقناع-فرشاة-من-اليمين--brush-mask-write-on-rtl)
- [`DRAW-16` كتابة حقيقية بترتيب الضربات (لاتيني)](#draw-16--كتابة-حقيقية-بترتيب-الضربات-لاتيني--true-glyph-write-on-with-stroke-order-latin)
- [`DRAW-17` ترجمة بخط اليد تُكتب](#draw-17--ترجمة-بخط-اليد-تُكتب--handwritten-typewriter-caption)
- [`DRAW-18` أنماط قلم التحديد](#draw-18--أنماط-قلم-التحديد--marker-emphasis-modes)
- [`DRAW-19` دائرة يدوية مرتعشة](#draw-19--دائرة-يدوية-مرتعشة--hand-drawn-circle-emphasis)
- [`DRAW-20` خربشة توضيحية فوق الصورة](#draw-20--خربشة-توضيحية-فوق-الصورة--doodle-annotations-on-footage)
- [`DRAW-21` شطب بخربشة ثم إعادة كتابة](#draw-21--شطب-بخربشة-ثم-إعادة-كتابة--scribble-strike-through-rewrite)
- [`DRAW-22` ملاحظة يدوية داخل إطار](#draw-22--ملاحظة-يدوية-داخل-إطار--boxed-handwritten-callout)
- [`DRAW-23` علامات rough-notation](#draw-23--علامات-rough-notation--rough-notation-marks)
- [`DRAW-24` خط الرحلة من اليمين](#draw-24--خط-الرحلة-من-اليمين--journey-line-draw-on-rtl)
- [`DRAW-25` عدم الكمال المقصود](#draw-25--عدم-الكمال-المقصود--deliberate-imperfection)
- [`DRAW-26` غليان الخط](#draw-26--غليان-الخط--line-boil)
- [`DRAW-27` رسم خشن بأسلوب Rough.js](#draw-27--رسم-خشن-بأسلوب-roughjs--roughjs--excalidraw-sketch-rendering)
- [`DRAW-28` خطوط بضغط على طريقة perfect-freehand](#draw-28--خطوط-بضغط-على-طريقة-perfect-freehand--pressure-strokes--clipped-hatching)
- [`DRAW-29` حبر بصمة بضغط وتظليل](#draw-29--حبر-بصمة-بضغط-وتظليل--basma-ink-pressure-strokes--hatching)
- [`DRAW-30` محرك فرشاة الحبر الحتمي](#draw-30--محرك-فرشاة-الحبر-الحتمي--deterministic-ink-brush-engine)
- [`DRAW-31` ملمس الرصاص والطباشير بالمرشحات](#draw-31--ملمس-الرصاص-والطباشير-بالمرشحات--pencil--chalk-texture-filters)
- [`DRAW-32` خطوط ماء موازية للساحل](#draw-32--خطوط-ماء-موازية-للساحل--triple-coastline-water-lines)
- [`DRAW-33` سبورة بيضاء](#draw-33--سبورة-بيضاء--whiteboard)
- [`DRAW-34` سبورة سينمائية](#draw-34--سبورة-سينمائية--whiteboard-cinematic)
- [`DRAW-35` سبورة الطباشير](#draw-35--سبورة-الطباشير--chalkboard)
- [`DRAW-36` قصص الدودل](#draw-36--قصص-الدودل--doodle-stories)
- [`DRAW-37` قلم البلوتر](#draw-37--قلم-البلوتر--plotter-pen)
- [`DRAW-38` إطار بإطار على اثنين](#draw-38--إطار-بإطار-على-اثنين--frame-by-frame-on-twos)
- [`DRAW-39` رسومات الماركر للقصص](#draw-39--رسومات-الماركر-للقصص--marker-doodle-story-illustrations)
- [`DRAW-40` مشهد الرصاص الهادئ بلون واحد](#draw-40--مشهد-الرصاص-الهادئ-بلون-واحد--quiet-pencil-one-accent-scene)
- [`DRAW-41` إطارات ستوري بورد بالرصاص](#draw-41--إطارات-ستوري-بورد-بالرصاص--pencil-storyboard-frames)
- [`DRAW-42` خريطة رحلة مرسومة باليد](#draw-42--خريطة-رحلة-مرسومة-باليد--hand-drawn-route-sketch-map)
- [`DRAW-43` مخططات تجادل لا تعرض](#draw-43--مخططات-تجادل-لا-تعرض--diagrams-that-argue-sketch-patterns)
- [`DRAW-44` رسوم خطية استعارية تتحرك](#draw-44--رسوم-خطية-استعارية-تتحرك--line-art-metaphor-motions)
- [`DRAW-45` قص الرسومات من صفحة الكراسة](#draw-45--قص-الرسومات-من-صفحة-الكراسة--sketch-cut-out-lift--eraser-wipe)
- [`DRAW-46` شريط مخطط يُرسم](#draw-46--شريط-مخطط-يُرسم--striped-ribbon-draw-on)
- [`DRAW-47` من مخطط سلكي إلى مجسم](#draw-47--من-مخطط-سلكي-إلى-مجسم--wireframe-draw--solid-formation)
- [`DRAW-48` ترتيب الرسام في الكشف](#draw-48--ترتيب-الرسام-في-الكشف--painter-reveal-orders)
- [`DRAW-49` فيلم الرسم](#draw-49--فيلم-الرسم--drawing-film-picture-forming-as-mp4)
- [`DRAW-50` الرسم بترتيب الكود نفسه](#draw-50--الرسم-بترتيب-الكود-نفسه--pil-command-recorder)
- [`DRAW-51` الرسم المطابق تمامًا](#draw-51--الرسم-المطابق-تمامًا--exact-match-painting)
- [`DRAW-52` صورة إلى برنامج بايثون](#draw-52--صورة-إلى-برنامج-بايثون--image-to-standalone-pillow-program)
- [`DRAW-53` استيراد SVG والتحويل إلى متجهات](#draw-53--استيراد-svg-والتحويل-إلى-متجهات--svg-import--vectorize-to-draw-steps)
- [`DRAW-54` محوّل مسارات SVG إلى نقاط](#draw-54--محوّل-مسارات-svg-إلى-نقاط--svg-path-sampler)
- [`DRAW-55` الرسم بالفأرة في برنامج الرسام](#draw-55--الرسم-بالفأرة-في-برنامج-الرسام--drawing-by-mouse-in-windows-paint)
- [`DRAW-56` رسم فوق لقطات مولدة](#draw-56--رسم-فوق-لقطات-مولدة--draw-over-film-on-generated-bases)
- [`DRAW-57` دراسة أسلوب مرسوم بالتتبع](#draw-57--دراسة-أسلوب-مرسوم-بالتتبع--rotoscope-style-study--style-pack)
- [`DRAW-58` إعادة رسم مخرجات مولدة كمتجهات](#draw-58--إعادة-رسم-مخرجات-مولدة-كمتجهات--generated-raster--hand-vector-recreation)
- [`DRAW-59` مكونات HyperFrames للرسم اليدوي](#draw-59--مكونات-hyperframes-للرسم-اليدوي--hyperframes-hand-drawn-components)
- [`DRAW-60` مكتبات الرسم التدريجي](#draw-60--مكتبات-الرسم-التدريجي--draw-on-libraries)
- [`DRAW-G01` رسم يدوي خشن ثابت البذرة](#draw-g01--رسم-يدوي-خشن-ثابت-البذرة--seeded-rough-hand-drawn-rendering)
- [`DRAW-G02` زخم السحب والارتداد المطاطي](#draw-g02--زخم-السحب-والارتداد-المطاطي--drag-momentum-and-rubber-band-edges)
- [`DRAW-P01` قصة الخط الواحد المستمر حتى الشعار](#draw-p01--قصة-الخط-الواحد-المستمر-حتى-الشعار--continuous-line-logo-story-one-stroke--three-beats--wordmark-loop)
- [`DRAW-U01` فيلم يد مرسومة حتمي بـmake_frame(t)](#draw-u01--فيلم-يد-مرسومة-حتمي-بـmake_framet--deterministic-hand-drawn-film-via-make_framet)
- [`DRAW-X01` ريشة تكتب السطر الفعلي](#draw-x01--ريشة-تكتب-السطر-الفعلي--quill-that-writes-the-actual-line-ink-frontier)

## البطاقات / cards

### `DRAW-01` — رسم المسار بإزاحة الشرطة / SVG stroke draw-on

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المسار يُرسم كضربة قلم بتحريك stroke-dashoffset من الطول الكامل إلى الصفر. / A path traces itself by animating its dash offset from full length to zero.

**متى:** أسهم، روابط، شعارات، خطوط تحتية، منحنيات بيانات، خرائط / arrows, connectors, logos, underlines, data lines, maps.

**كيف:** Easiest seek-safe form: pathLength="1", stroke-dasharray 1, stroke-dashoffset = 1 − ease(p) where p = prog(t, t0, t1); otherwise len = path.getTotalLength() measured after d is set and fonts are loaded. Round caps, fill none; fill fades in after the stroke completes; never draw all paths at once — stagger them, each segment starting at 70–80% of the previous one; rings rotate −90° to start at 12 o'clock. Typical 0.5–0.9 s power2.out, logos 1–2 s inOut, data/route lines cubic-bezier(.645,.045,.355,1) then the end label pops. Proof film glass-luxury-logo draws its khatam emblem this way from 4.0 to 5.6 s. (code snippet in references/powers/hand-drawn-draw-on.md)

**المعاملات:** 0.5–0.9 s; segments start at 70–80%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** draw on · stroke-dashoffset · رسم المسار · pathLength · svg · self drawing

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md`
- `kosif-tool/playbooks/hand-drawn.md`
- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/svg-path-draw.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-02` قلم مكتبة الحركة برأس يهبط / Kit drawPath with landing head & flowDash (ready)
- `DRAW-03` سرعة القلم والرفع / Pen speed & lifts (proven)

### `DRAW-02` — قلم مكتبة الحركة برأس يهبط / Kit drawPath with landing head & flowDash

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard no-charge license (vendored) |

**ما هي:** أي مسار يُرسم كقلم، ورأس سهم أو نقطة يقفز بنابض قبل النهاية بعُشر ثانية، وشرطات تجري لتبيّن التدفق. / Any path drawn like a pen with a head that springs in 0.1 s before the end, plus marching dashes for flow.

**متى:** أسهم الشرح، دوائر الساعة، مسارات الحلم، تيار في سلك / explainer arrows, clock rings, flow lines.

**كيف:** MOTION.drawPath(tl, path, at, dur, {ease, head, headOrigin, opacity}) → dasharray = len, offset len → 0, default ease power4.inOut; head scale 0→1 in 0.35 s with spring('snappy') at at + dur − 0.1. MOTION.flowDash(tl, path, at, dur, {pattern:'28 22', cycles:6}). Used in the house projects: gold ring 0.9 s E.out, clock ring 1.0 s, dream path 0.9 s, car body 0.75 s, wheels 0.4 s, spring curve 1.15 s, end ring 0.62 s.

**المعاملات:** power4.inOut; head 0.35 s at end − 0.1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** drawPath · arrowhead · flowDash · pen · motion kit

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/motion/kit/motion-kit.js:237`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:237`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:204`
- `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js`

#### 7. قدرات قريبة في العائلة

- `DRAW-01` رسم المسار بإزاحة الشرطة / SVG stroke draw-on (proven)
- `DRAW-03` سرعة القلم والرفع / Pen speed & lifts (proven)
- `DRAW-04` ترتيب الرسم البشري ووصفة «ارسم وسمِّ» / Human draw order & draw-and-label (proven)

### `DRAW-03` — سرعة القلم والرفع / Pen speed & lifts

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** القلم يسير بسرعة شبه ثابتة على طول المسار مع تسهيل لكل ضربة ووقفات رفع قصيرة، والمدة = الطول ÷ السرعة. / Near-constant pen speed per stroke, short lifts, duration = length / speed.

**متى:** كل سبورة ورسم يدوي / every whiteboard and hand-drawn scene.

**كيف:** pen 800–1400 px/s with ease-in-out per stroke; lift 60–120 ms between strokes; hatching 2000 px/s or a 300 ms wipe; narrated whiteboards 500–700 px/s with the stroke leading the word by ≤150 ms; plotter = constant speed, no easing, pen-up travel lines at 10% opacity; text paths ~0.6–1.5 s per line. Proof film whiteboard-draw (rendered and verified here, 13/13) times every stroke by arc length: strokes 3000 px/s, hatching 5600 px/s, progress e(u) = 0.55·inOutSine(u) + 0.45·u whose derivative is the pen speed (it drives width and the marker squeak), gaps 55 ms between strokes, 30 ms between short ones, 170 ms between groups — editing a shape re-times the whole film.

**المعاملات:** 800–1400 px/s; lift 60–120 ms; hatch 2000 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pen speed · px/s · lift · سرعة القلم · plotter

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md`
- `kosif-tool/playbooks/hand-drawn.md:25`
- `kosif-tool/styles/pm-tak3sh8-be5012/BRIEF.md`
- `kosif-tool/styles/plotter/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-01` رسم المسار بإزاحة الشرطة / SVG stroke draw-on (proven)
- `DRAW-02` قلم مكتبة الحركة برأس يهبط / Kit drawPath with landing head & flowDash (ready)
- `DRAW-04` ترتيب الرسم البشري ووصفة «ارسم وسمِّ» / Human draw order & draw-and-label (proven)
- `DRAW-05` رابط مخطط برأس سهم / Diagram edge draw-on with arrowhead (ready)

### `DRAW-04` — ترتيب الرسم البشري ووصفة «ارسم وسمِّ» / Human draw order & draw-and-label

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المحيط أولًا ثم التفاصيل ثم التعبئة ثم الاسم المكتوب ثم الثبات، والكتابة العربية من اليمين. / Outline, details, fill, handwritten label, hold; Arabic writing right to left.

**متى:** أي عنصر يُشرح بالرسم / any object explained by drawing.

**كيف:** 0–900 ms outline (ease-in-out per stroke) → 900–1300 details → 1300–1600 highlight fill wipe (ease-out) → 1600–2300 label writes beside it (constant) → 2300–4000 hold while the hand leaves (ease-in). 3D-ish objects: outline dash 0.6 s → face opacity 0.3 s → extrusion depth 0.5 s, starting from a sparkle (style:fake3d). One pen weight family (e.g. 4 and 8 px), one ink + one highlight; primary path 6 px round, secondary 3 px, grid 1.5 px at 1080 width. Proof film whiteboard-draw follows a human order: title (RTL mask) → red underline from the right → sun circle overshooting its start, then hatching, then 8 rays → water drop → two causal arrows → cross-hatched pot and plant → 'النتيجة: نمو' with a red circle.

**المعاملات:** 0/900/1300/1600/2300/4000 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** draw order · draw and label · outline fill · ترتيب الرسم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md`
- `kosif-tool/playbooks/hand-drawn.md:36`
- `kosif-tool/templates/STYLE.md`
- `kosif-tool/styles/fake3d`

#### 7. قدرات قريبة في العائلة

- `DRAW-02` قلم مكتبة الحركة برأس يهبط / Kit drawPath with landing head & flowDash (ready)
- `DRAW-03` سرعة القلم والرفع / Pen speed & lifts (proven)
- `DRAW-05` رابط مخطط برأس سهم / Diagram edge draw-on with arrowhead (ready)
- `DRAW-06` رأس يتبع الخط: يد، ماركر، طباشيرة / Pen-tip followers: hand, marker, chalk (proven)

### `DRAW-05` — رابط مخطط برأس سهم / Diagram edge draw-on with arrowhead

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رابط بين عقدتين يُرسم ثم يظهر رأس السهم في آخر 80 ملّي ثانية. / A connector draws, then its arrowhead appears in the last 80 ms.

**متى:** مخططات انسيابية وخرائط ذهنية / flowcharts and mind maps.

**كيف:** Remotion Edge: strokeDasharray = len, strokeDashoffset = len·(1 − p), markerEnd only when p > 0.95; html-canvas: pathLength="1", dashoffset = 1 − KOSIF.prog(t, t0, t1, Ease.inOutCubic); 900–1200 px/s ease-in-out cubic; stroke #9fb0cc 4 px.

**المعاملات:** 900–1200 px/s; arrowhead last 80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** edge · connector · arrowhead · flowchart · رابط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/playbooks/diagrams.md:28`
- `kosif-tool/starters/html-canvas/timeline.js`

#### 7. قدرات قريبة في العائلة

- `DRAW-03` سرعة القلم والرفع / Pen speed & lifts (proven)
- `DRAW-04` ترتيب الرسم البشري ووصفة «ارسم وسمِّ» / Human draw order & draw-and-label (proven)
- `DRAW-06` رأس يتبع الخط: يد، ماركر، طباشيرة / Pen-tip followers: hand, marker, chalk (proven)
- `DRAW-07` رأس متوهج يجرّ الخط / Glowing head draw (proven)

### `DRAW-06` — رأس يتبع الخط: يد، ماركر، طباشيرة / Pen-tip followers: hand, marker, chalk

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صورة يد أو ماركر أو طباشيرة مثبتة على طرف الخط الجاري، تميل معه وتُرفع بين الضربات. / A hand, marker or chalk sprite pinned to the live stroke tip, tilting with it and lifting between strokes.

**متى:** سبورة، شرح بالماركر، معادلات طباشير / whiteboard, marker explainers, chalk formulas.

**كيف:** tip = path.getPointAtLength(p·len) (clamp to len − 1e-4 to avoid null); hand lags 1 frame and rotates ±5° with direction, removed during holds; marker sprite (body + coloured cap) at −35°…−40°, cap recoloured to the active ink, lift 200 ms with a growing shadow (2→10 px offset); chalk 60×12 px rounded rect tinted to the stroke, lift scale 1→1.08 over 250 ms along an eased path; the playbook's Remotion DrawnPath draws a 5 px tip circle. Proof film whiteboard-draw draws the marker in code (felt tip, collar, gradient barrel, ink-coloured band and cap), lifts it between strokes with sin(πu) on an inOutCubic travel while its shadow moves away, recolours it on pen swaps, and the camera follows 7% of its mean position over the last 0.9 s (zoom 1.02 → 1.06).

**المعاملات:** lag 1 f; ±5°; marker −35°; lift 200–250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hand overlay · marker · chalk · pen tip · يد · ماركر

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md`
- `kosif-tool/playbooks/hand-drawn.md:27`
- `kosif-tool/styles/whiteboard`
- `kosif-tool/styles/chalkboard`
- `kosif-tool/styles/pm-lemomo-ai-0d9cff`

#### 7. قدرات قريبة في العائلة

- `DRAW-04` ترتيب الرسم البشري ووصفة «ارسم وسمِّ» / Human draw order & draw-and-label (proven)
- `DRAW-05` رابط مخطط برأس سهم / Diagram edge draw-on with arrowhead (ready)
- `DRAW-07` رأس متوهج يجرّ الخط / Glowing head draw (proven)
- `DRAW-08` كشف متعدد الأجزاء بالطول التراكمي / Cumulative-length multi-segment reveal (documented)

### `DRAW-07` — رأس متوهج يجرّ الخط / Glowing head draw

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة أو شرارة مضيئة تركب رأس الخط، مع نسخة شبحية أو هالة، كخط نبض أو شعاع يرسم شعارًا. / A glowing dot or spark rides the line head, with a ghost copy or halo — ECG pulses, beams drawing a logo.

**متى:** تقنية، صحة، نيون، ختام فيديو / tech, health, neon, end cards.

**كيف:** stroke 1.5–4 px plus a duplicate path blurred 8–12 px at ~60% for glow; head dot r 4–6 px with 10–20 px glow (+4–6 tiny sparks for a plotter look, core #f27525); optional grey offset ghost copy trailing; ECG: flat line with one spike drawn left→right, a white dot + ring 0→60 px over 800 ms at each beat; closing arc glows 8 px. Proof film neon-glow draws its amber cup with light running along the tube (3.40–4.65 s inOutCubic) through a 5-layer additive glow.

**المعاملات:** head r 4–6 px; glow 10–20 px; 1–2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** glowing head · spark · ECG · neon line · شرارة · نبض

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md`
- `kosif-tool/styles/plotter`
- `kosif-tool/styles/pm-marouanegazouzi-6071d5`
- `kosif-tool/styles/pm-ghinaiya-nirmal-5d8fec`

#### 7. قدرات قريبة في العائلة

- `DRAW-05` رابط مخطط برأس سهم / Diagram edge draw-on with arrowhead (ready)
- `DRAW-06` رأس يتبع الخط: يد، ماركر، طباشيرة / Pen-tip followers: hand, marker, chalk (proven)
- `DRAW-08` كشف متعدد الأجزاء بالطول التراكمي / Cumulative-length multi-segment reveal (documented)
- `DRAW-09` سلامة رسم المسارات / SVG draw-on safety (install)

### `DRAW-08` — كشف متعدد الأجزاء بالطول التراكمي / Cumulative-length multi-segment reveal

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ارسم حدود بلد بكل جزره، أو شبكة من مسارات كثيرة، كضربة واحدة موقوتة بالطول التراكمي دون اختراع وصلات. / Draw many rings/segments as one timed stroke by cumulative length, never inventing joins.

**متى:** حدود دول، شبكات، مسارات متعددة M / borders, grids, multi-M paths.

**كيف:** Store each segment, its length and cumulative start; for a reveal window slice every overlapping segment (emit a MultiLineString); skip slivers < 0.0008 km; never clip the border to the viewport. For freehand renderers split a path with several M commands into separate strokes and distribute progress proportional to length so the brush never bridges them with a scribble.

**المعاملات:** sliver 0.0008 km; length-weighted progress

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** border reveal · cumulative length · multi segment · حدود

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md`
- `kosif-tool/styles/chalkboard`

#### 7. قدرات قريبة في العائلة

- `DRAW-06` رأس يتبع الخط: يد، ماركر، طباشيرة / Pen-tip followers: hand, marker, chalk (proven)
- `DRAW-07` رأس متوهج يجرّ الخط / Glowing head draw (proven)
- `DRAW-09` سلامة رسم المسارات / SVG draw-on safety (install)
- `DRAW-10` نهر يمتلئ ثم يجري / River fill then flow (ready)

### `DRAW-09` — سلامة رسم المسارات / SVG draw-on safety

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قِس المسار بعد ضبط d، ولا تجعل dasharray في CSS يتصارع مع التحريك. / Measure the path after d is set; never fight CSS dasharray.

**متى:** قبل رندر أي مسار يُرسم / before rendering any draw-on.

**كيف:** HyperFrames lint rules svg_measure_before_path_d and svg_drawon_css_dasharray_conflict catch both bugs; in your own pages measure inside the font/asset ready gate, set dasharray from JS only, and check a still at p = 0 (no stray dot) and p = 1 (no gap).

**التثبيت:** npx hyperframes lint

**الوسوم:** lint · svg · dasharray · safety

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-one/vendor/hyperframes/packages/lint/src/rules/gsap.ts`

#### 7. قدرات قريبة في العائلة

- `DRAW-07` رأس متوهج يجرّ الخط / Glowing head draw (proven)
- `DRAW-08` كشف متعدد الأجزاء بالطول التراكمي / Cumulative-length multi-segment reveal (documented)
- `DRAW-10` نهر يمتلئ ثم يجري / River fill then flow (ready)
- `DRAW-11` المحراب بقلم ذهبي / Gold-pen arch draw-on (ready)

### `DRAW-10` — نهر يمتلئ ثم يجري / River fill then flow

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مجرى يمتلئ من الجبل إلى البحر ثم تجري عليه شرطات ضوء، وفي 3D شريط يتقدم بنطاق الرسم. / A river fills mountain→sea then light dashes run along it; in 3D a ribbon advances by draw range.

**متى:** دورة المياه، أنهار، خطوط أنابيب / water cycle, rivers, pipelines.

**كيف:** same path three times: dry bed #CDE7F7 20 px; water #2B8CE6 pathLength=1 dasharray '1 1' dashoffset 1→0 (7.3–8.7 s); flow #A9DBFF 6 px dasharray '0.04 0.07' dashoffset −0.35·t, fading in at 8.4 s. three-kit: makeRibbon(curve, {segments:220, radius:11, radial:10}) revealed with geometry.setDrawRange.

**المعاملات:** dashes .04/.07; −0.35·t

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** river · flow dashes · water cycle · نهر · ribbon

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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
- `kosif-studio/motion/kit/three-kit.js`

#### 7. قدرات قريبة في العائلة

- `DRAW-08` كشف متعدد الأجزاء بالطول التراكمي / Cumulative-length multi-segment reveal (documented)
- `DRAW-09` سلامة رسم المسارات / SVG draw-on safety (install)
- `DRAW-11` المحراب بقلم ذهبي / Gold-pen arch draw-on (ready)
- `DRAW-12` رسوم خطية صغيرة فوق الفيديو / Line micro-graphics over footage (ready)

### `DRAW-11` — المحراب بقلم ذهبي / Gold-pen arch draw-on

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قوس المحراب وقوس داخلي يُرسمان كقلم ذهبي في البداية، ثم يثخن الخط عند «آمين». / The mihrab arch draws like a gold pen and thickens on the final 'آمين'.

**متى:** أدعية، مناسبات دينية، بطاقات إسلامية / duas and Islamic occasions.

**كيف:** stroke url(#gold) linear gradient #fff0b3 / #e8b04a / #fff0b3, width 7 round caps; drawPath(tl, path, 0, 1.7, {ease:E.out}); inner arch #f3c766 opacity .55 width 3 at 0.25 s; at the amen word stroke-width 7 → 9; arch d = 'M150,1760 L150,1010 C150,770 370,610 540,520 C710,610 930,770 930,1010 L930,1760' (1080×1920).

**المعاملات:** 1.7 s E.out; 7 → 9 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mihrab · gold pen · دعاء · arch · محراب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-one/projects/thursday-dua-animation/source/index.html`

#### 7. قدرات قريبة في العائلة

- `DRAW-09` سلامة رسم المسارات / SVG draw-on safety (install)
- `DRAW-10` نهر يمتلئ ثم يجري / River fill then flow (ready)
- `DRAW-12` رسوم خطية صغيرة فوق الفيديو / Line micro-graphics over footage (ready)
- `DRAW-13` أيقونات المعنى المرسومة / Meaning icons drawn on (ready)

### `DRAW-12` — رسوم خطية صغيرة فوق الفيديو / Line micro-graphics over footage

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسوم عاجية رفيعة توضح كل مثال منطوق لنحو 1.2 ث: ساعة 24 علامة، مسار حلم، مسطرة قياس، سيارة بخط واحد، شريط وقت ينضب. / Thin ivory line drawings illustrating each spoken example for ~1.2 s.

**متى:** مونتاج متكلم فاخر / premium talking-head edits.

**كيف:** stroke 2–3 px #F5F0E6 with #E7B65A accents; car body stroke 2.6 round joins + wheels r 19, road = 6 gold dashes sliding −70 px; clock ring r 150 with 24 ticks (every 6th longer, 3 px) and a hand rotating 360° in 1 s; ticks appear right after the ring: opacity .9, 0.08 s each, stagger .035 s; rail 460 px with 18 ticks sliding x −24→0.

**المعاملات:** ~1.2 s per example; ticks stagger 35 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** line art · micro graphics · clock · footage overlay · رسوم خطية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/motion/projects/premium_edit/index.html:56`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:198`
- `kosif-studio/out/FINAL_EDIT/EDIT_NOTES.txt`

#### 7. قدرات قريبة في العائلة

- `DRAW-10` نهر يمتلئ ثم يجري / River fill then flow (ready)
- `DRAW-11` المحراب بقلم ذهبي / Gold-pen arch draw-on (ready)
- `DRAW-13` أيقونات المعنى المرسومة / Meaning icons drawn on (ready)
- `DRAW-14` قوالب موشن بالقلم / Pen-drawn motion templates (proven)

### `DRAW-13` — أيقونات المعنى المرسومة / Meaning icons drawn on

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أيقونة خطية تُختار من معنى السطر وتُرسم فوقه ثم تتنفس مع الإيقاع، والأرقام تعدّ بدلًا منها. / A stroke icon picked from the line's meaning, drawn on and breathing on the beat.

**متى:** قصائد، أغانٍ، دروس بنص عربي / poems, songs, Arabic text lessons.

**كيف:** verse.html: 12 icons (sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light) in a 200×200 box, stroke 5 round, accent colour; drawPath per stroke 0.7 s, stagger 0.06 s; breathe 1 + .06·beat + .04·rms; kind 'count' with a value counts up (150 px). Basma: 16 stroke motifs (sun, cloud, wave, drop, bulb, heart, star, check, chart, target, clock, mountain, phone, people, doc, arrow) with fill outlines for hatching and an Arabic keyword matcher MK.motifFor (شمس/سحاب/بحر/فكر/قلب/نمو/هدف/وقت/جبل…) else 8 defaults.

**المعاملات:** 0.7 s, stagger .06 s; 200×200, stroke 5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** icons · motif · meaning · أيقونات · verse

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/motion/templates/verse.html`
- `100-superskills/skills/kosif-montage-motion/templates/verse.html:258`
- `app/public/js/10_studio.js:245`

#### 7. قدرات قريبة في العائلة

- `DRAW-11` المحراب بقلم ذهبي / Gold-pen arch draw-on (ready)
- `DRAW-12` رسوم خطية صغيرة فوق الفيديو / Line micro-graphics over footage (ready)
- `DRAW-14` قوالب موشن بالقلم / Pen-drawn motion templates (proven)
- `DRAW-15` كتابة بقناع فرشاة من اليمين / Brush-mask write-on (RTL) (proven)

### `DRAW-14` — قوالب موشن بالقلم / Pen-drawn motion templates

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قالبان جاهزان: كشف الشعار بالقلم (رسم ← تعبئة ← اسم وشعار نصي) وقائمة نقاط بعلامات صح مرسومة. / Two ready templates: pen logo reveal and a bullet list with drawn ticks.

**متى:** شعار بسيط أو خطوات قصيرة في دقائق / a quick logo sting or short steps.

**كيف:** python scripts/mtemplates.py new NAME --template logo-reveal --set name=… tagline=… (6 s; default hexagon path viewBox 120×136, accent #E7B65A, bg #0f1a2b→#06101c, tagline 'حركة لها معنى') or --template bullet-list (8 s; ≤6 items each with a drawn check; 'ثلاث خطوات' / 'خطّط\|نفّذ\|راجع'; accent #5BD1A5). Also from the web studio Projects tab or MCP kosif_project_create. Every template generated and linted here (TemplateTests).

**المعاملات:** 6 s / 8 s; ≤6 items

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** logo reveal · bullet list · checkmarks · template · قالب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:48`
- `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:14`
- `100-superskills/skills/kosif-montage-motion/tests/test_v6.py`

#### 7. قدرات قريبة في العائلة

- `DRAW-12` رسوم خطية صغيرة فوق الفيديو / Line micro-graphics over footage (ready)
- `DRAW-13` أيقونات المعنى المرسومة / Meaning icons drawn on (ready)
- `DRAW-15` كتابة بقناع فرشاة من اليمين / Brush-mask write-on (RTL) (proven)
- `DRAW-16` كتابة حقيقية بترتيب الضربات (لاتيني) / True glyph write-on with stroke order (Latin) (install)

### `DRAW-15` — كتابة بقناع فرشاة من اليمين / Brush-mask write-on (RTL)

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضربة فرشاة سميكة تكشف عبارة عربية مكتملة من اليمين إلى اليسار / كشف لنص مُشكّل لا توليد حروف. — A thick brush stroke reveals a finished Arabic phrase right to left — a reveal of shaped text, not generated glyphs.

**متى:** افتتاحيات دافئة، عناوين بخط يدوي، شعار نصي / warm openings, handwritten titles.

**كيف:** Typeset the phrase in a real Arabic face (Aref Ruqaa, Marhey, Amiri), then animate a thick SVG stroke (dashoffset) or a soft-edged rect used as a mask: 0–0.5 s stroke starts, 0.5–2.5 s reveal, 2.5–4 s read; script headlines: mask wipe ~800 ms with gold gradient #f5c542→#d8a664 and soft shadow; sticky-note handwriting: one line per 500 ms; Latin goes left→right. Proven in whiteboard-draw: each Aref Ruqaa line is drawn whole and shaped, revealed right → left by a 46 px gradient mask (destination-in) while the pen tip walks the ink centre of each pixel column with a 7 Hz writing tremor. See ARAB-22 for the soft-mask + pen-tip version.

**المعاملات:** 4 s MG-015; wipe 500–800 ms per line

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** write on · brush mask · handwriting · كتابة يدوية · RTL

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-tool/playbooks/hand-drawn.md`
- `kosif-tool/styles/pm-deebeeeff-50fcd0`

#### 7. قدرات قريبة في العائلة

- `DRAW-13` أيقونات المعنى المرسومة / Meaning icons drawn on (ready)
- `DRAW-14` قوالب موشن بالقلم / Pen-drawn motion templates (proven)
- `DRAW-16` كتابة حقيقية بترتيب الضربات (لاتيني) / True glyph write-on with stroke order (Latin) (install)
- `DRAW-17` ترجمة بخط اليد تُكتب / Handwritten typewriter caption (documented)

### `DRAW-16` — كتابة حقيقية بترتيب الضربات (لاتيني) / True glyph write-on with stroke order (Latin)

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0; Hershey fonts carry a public-domain-style notice (unverified) |

**ما هي:** حروف Caveat معبأة تُكشف بخطوط مركزية مخبوزة لكل حرف بترتيب الكتابة الحقيقي وسرعة قلم تتكيف مع الانحناء ورفع القلم. / Filled Caveat letters revealed by baked per-glyph centrelines in real stroke order.

**متى:** عناوين إنجليزية بخط اليد / handwritten English titles.

**كيف:** HyperFrames block hw-write-title (Caveat 700, 1920×1080, 6 s, GSAP paused timeline); single-stroke alternative: HersheyScript1 / HersheyScriptMed SVG stroke fonts through gen-stroke-path.py to write apex words (neon, chalk, graffiti); seen equivalents: handwriting paths ~40–120 ms per glyph with a marker following. Latin only — Arabic uses the mask (DRAW-15).

**المعاملات:** ~40–120 ms/glyph

**التثبيت:** npx hyperframes add hw-write-title

**الوسوم:** write on · stroke order · Hershey · handwriting · Caveat

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-one/vendor/hyperframes/registry/blocks/hw-write-title/hw-write-title.html`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/assets/strokefonts/HersheyScript1.svg`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/gen-stroke-path.py`

#### 7. قدرات قريبة في العائلة

- `DRAW-14` قوالب موشن بالقلم / Pen-drawn motion templates (proven)
- `DRAW-15` كتابة بقناع فرشاة من اليمين / Brush-mask write-on (RTL) (proven)
- `DRAW-17` ترجمة بخط اليد تُكتب / Handwritten typewriter caption (documented)
- `DRAW-18` أنماط قلم التحديد / Marker emphasis modes (documented)

### `DRAW-17` — ترجمة بخط اليد تُكتب / Handwritten typewriter caption

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جملة بخط يدوي تُكشف تدريجيًا بعد تثبيت تخطيطها كاملًا فلا يعاد توسيطها أثناء الكتابة، مع خط تحتي أو دائرة. / A handwritten-style sentence revealed progressively after its full layout is fixed.

**متى:** ملاحظات فوق فيديو سفر أو فلوج / notes over travel/vlog footage.

**كيف:** lay out the whole sentence first, then reveal over 65% of the clip (delay + duration ≤ 1); place 8–12% inside frame edges on empty area; glyph height 4–5% of H; Latin per character 25–30 ms (Kalam/Caveat 600); Arabic per word or by RTL mask; optional circle via a draw-on ellipse.

**المعاملات:** reveal 0.65 of clip; glyph 4–5% H

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** handwritten caption · typewriter · notes · ملاحظة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template/SKILL.md`
- `kosif-tool/styles/pm-himanshutwtxs-5f4b43`

#### 7. قدرات قريبة في العائلة

- `DRAW-15` كتابة بقناع فرشاة من اليمين / Brush-mask write-on (RTL) (proven)
- `DRAW-16` كتابة حقيقية بترتيب الضربات (لاتيني) / True glyph write-on with stroke order (Latin) (install)
- `DRAW-18` أنماط قلم التحديد / Marker emphasis modes (documented)
- `DRAW-19` دائرة يدوية مرتعشة / Hand-drawn circle emphasis (proven)

### `DRAW-18` — أنماط قلم التحديد / Marker emphasis modes

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خمسة أنماط حتمية على كلمة: مسح تظليل، دائرة يدوية، خطوط انفجار، خط متموج، شطب تخطيطي. / Five deterministic emphasis styles on a word.

**متى:** الكلمة المفتاحية في عنوان أو جملة / the key word in a title or sentence.

**كيف:** highlight: span inset 0 −6px, radius 3 px, scaleX 0→1 in 0.5 s power2.out at ~0.6 s, multiply blend, colour rgba(255,236,79,.62); multi-line stagger 0.3 s; Arabic starts the swipe from the RIGHT (transform-origin right) and checks contrast; circle: 3 px ellipse border-radius 50% with slight rotation, back.out(1.7) 0.6 s; burst: 12 lines at 30° steps, 40–80 px, stagger 0.03 s; scribble: wavy path 3 px round caps drawn by dashoffset; sketch-out: rough rectangle. Underlines: ::after scaleX 0→1 swapping transform-origin (enter from one side, leave from the other) 0.4 s expo-out, or background-size 0%→100% 1px; thick 4 px rule 400 ms ease-out under the last line.

**المعاملات:** 0.5 s sweep; 12 burst lines; underline 0.3–0.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** highlighter · marker · underline · circle · burst · تظليل · تأكيد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/css-marker-patterns.md`
- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/css-patterns.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-16` كتابة حقيقية بترتيب الضربات (لاتيني) / True glyph write-on with stroke order (Latin) (install)
- `DRAW-17` ترجمة بخط اليد تُكتب / Handwritten typewriter caption (documented)
- `DRAW-19` دائرة يدوية مرتعشة / Hand-drawn circle emphasis (proven)
- `DRAW-20` خربشة توضيحية فوق الصورة / Doodle annotations on footage (seen)

### `DRAW-19` — دائرة يدوية مرتعشة / Hand-drawn circle emphasis

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إهليلج غير منتظم بحلقتين يتجاوز بدايته يُرسم حول خطأ أو رابط أو معادلة، مع علامات انفجار أو ✗. / An irregular, overshooting double-loop ellipse drawn around a target.

**متى:** إبراز خطأ، رابط الدعوة، وجه في صورة مصغرة / errors, CTAs, faces in thumbnails.

**كيف:** jittered ellipse path (start and end overlap ~15%), stroke 2–3 px, draw 300–700 ms by dashoffset after the content lands; extras: burst ticks around a label, a short underline and a red ✗; clickbait variant: red ring around the head (300 ms) + curved red arrow sliding in (250 ms) + yellow Impact caption with black stroke. Proven in whiteboard-draw: a red circle closes around «نمو» as the final beat, drawn by the pressure-stroke builder (DRAW-28).

**المعاملات:** 300–700 ms; 2–3 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** circle · emphasis · دائرة · ellipse · CTA

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md`
- `kosif-tool/styles/pm-0xnfrith-5be616`
- `kosif-tool/styles/pm-ik-builds-b8bdcf`
- `kosif-tool/styles/pm-sab8a-364a5a`

#### 7. قدرات قريبة في العائلة

- `DRAW-17` ترجمة بخط اليد تُكتب / Handwritten typewriter caption (documented)
- `DRAW-18` أنماط قلم التحديد / Marker emphasis modes (documented)
- `DRAW-20` خربشة توضيحية فوق الصورة / Doodle annotations on footage (seen)
- `DRAW-21` شطب بخربشة ثم إعادة كتابة / Scribble strike-through rewrite (seen)

### `DRAW-20` — خربشة توضيحية فوق الصورة / Doodle annotations on footage

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سهم ودائرة وخط تحتي تُرسم فوق الشيء المقصود، وملاحظات بخط اليد بالأزرق للصحيح والأحمر للخطأ. / Arrows, circles and underlines drawn over the referenced object; handwritten notes, blue right / red wrong.

**متى:** شرح لقطات شاشة، تصحيح أخطاء، دروس / screenshot explainers, corrections, lessons.

**كيف:** MG-105 timing: 0–1 s shot, 1–4 s marks, 4–6 s read; each mark explains one point and never covers the subject (track it if the shot moves); curved arrow drawn first (250–300 ms) then the note types (25–30 ms/char Latin, by word in Arabic); a strike line drawn over the wrong statement; blue #2f7bf5, red #ef3b55.

**المعاملات:** arrow 250–300 ms; 6 s beat

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** annotation · arrow · doodle · footage · تعليق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`
- `kosif-tool/styles/pm-chatgptastra-0d95c7`
- `kosif-tool/styles/pm-himanshutwtxs-5f4b43`

#### 7. قدرات قريبة في العائلة

- `DRAW-18` أنماط قلم التحديد / Marker emphasis modes (documented)
- `DRAW-19` دائرة يدوية مرتعشة / Hand-drawn circle emphasis (proven)
- `DRAW-21` شطب بخربشة ثم إعادة كتابة / Scribble strike-through rewrite (seen)
- `DRAW-22` ملاحظة يدوية داخل إطار / Boxed handwritten callout (seen)

### `DRAW-21` — شطب بخربشة ثم إعادة كتابة / Scribble strike-through rewrite

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خربشة ملتفة تُرسم فوق الكلمات القديمة فتخفت إلى النصف، ثم يصعد السطر الجديد تحتها. / A looping scribble crosses out the old words, then the new line slides up.

**متى:** «لا… بل…»، تصحيح مفهوم / 'not this, but that' moments.

**كيف:** magenta looping scribble path drawn by dashoffset in 300 ms, old words fade to 50%, new line 250 ms easeOutBack from below.

**المعاملات:** 300 ms; 250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** strike · scribble · rewrite · شطب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/pm-paulo-kombucha-96431c`

#### 7. قدرات قريبة في العائلة

- `DRAW-19` دائرة يدوية مرتعشة / Hand-drawn circle emphasis (proven)
- `DRAW-20` خربشة توضيحية فوق الصورة / Doodle annotations on footage (seen)
- `DRAW-22` ملاحظة يدوية داخل إطار / Boxed handwritten callout (seen)
- `DRAW-23` علامات rough-notation / Rough-notation marks (install)

### `DRAW-22` — ملاحظة يدوية داخل إطار / Boxed handwritten callout

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مستطيل مدوّر مرتعش يُرسم أولًا بلون التأكيد ثم تظهر الكلمات بداخله. / A jittered rounded rectangle draws first, then the handwritten words appear inside.

**متى:** نصيحة جانبية، تعريف مصطلح / side tips, term definitions.

**كيف:** rough rounded-rect path 400 ms in #d17c55, then text 600 ms; HyperFrames hw-box-label also drops the box in with a volume-preserving squash and spring.

**المعاملات:** 400 + 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** callout · box · note · ملاحظة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/pm-lemomo-ai-0d9cff`
- `kosif-one/vendor/hyperframes/registry/components/hw-box-label/hw-box-label.html`

#### 7. قدرات قريبة في العائلة

- `DRAW-20` خربشة توضيحية فوق الصورة / Doodle annotations on footage (seen)
- `DRAW-21` شطب بخربشة ثم إعادة كتابة / Scribble strike-through rewrite (seen)
- `DRAW-23` علامات rough-notation / Rough-notation marks (install)
- `DRAW-24` خط الرحلة من اليمين / Journey line draw-on (RTL) (ready)

### `DRAW-23` — علامات rough-notation / Rough-notation marks

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تظليل ودائرة وخط تحتي وشطب وإطار وقوس بخطوط خشنة حول الكلمات مع قيمة تقدّم. / Sketchy highlight/circle/underline/strike/box/bracket around words driven by a progress value.

**متى:** Remotion أو صفحة HTML تحتاج علامات جاهزة / Remotion or HTML pages needing ready marks.

**كيف:** Remotion @remotion/rough-notation <Highlight/Circle/Underline/StrikeThrough/CrossedOff/Box/Bracket progress={interpolate(frame,[15,40],[0,1],{extrapolateRight:'clamp'})}>; highlight rgba(255,236,79,0.62); plain HTML: rough-notation npm driven by seek(t), never its own timers.

**المعاملات:** draw window ~25 frames

**التثبيت:** npm i rough-notation

**الوسوم:** rough notation · highlight · remotion · annotation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-21` شطب بخربشة ثم إعادة كتابة / Scribble strike-through rewrite (seen)
- `DRAW-22` ملاحظة يدوية داخل إطار / Boxed handwritten callout (seen)
- `DRAW-24` خط الرحلة من اليمين / Journey line draw-on (RTL) (ready)
- `DRAW-25` عدم الكمال المقصود / Deliberate imperfection (documented)

### `DRAW-24` — خط الرحلة من اليمين / Journey line draw-on (RTL)

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط تقدم 2 بكسل ينمو من الحافة اليمنى، ألوانه تعني الحالة: رمادي قادم، بنفسجي حالي، أخضر مزرق منجز. / A 2 px progress line grows from the right edge; colour stops encode state.

**متى:** مراحل رحلة أو برنامج بالعربية / Arabic step journeys.

**كيف:** ::before line, transform-origin right center, keyframe scaleX 0→1 with opacity .2→1 over 680 ms ease-cinematic (.22,.8,.26,1), delay 160 ms; gradient to left: border 0–38%, primary 38–64%, teal 64–100%; inset 10%.

**المعاملات:** 680 ms; delay 160 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** journey line · RTL · progress · رحلة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-audit-pro/app/globals.css:981`
- `kosif-audit-pro/app/globals.css:1082`

#### 7. قدرات قريبة في العائلة

- `DRAW-22` ملاحظة يدوية داخل إطار / Boxed handwritten callout (seen)
- `DRAW-23` علامات rough-notation / Rough-notation marks (install)
- `DRAW-25` عدم الكمال المقصود / Deliberate imperfection (documented)
- `DRAW-26` غليان الخط / Line boil (documented)

### `DRAW-25` — عدم الكمال المقصود / Deliberate imperfection

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ارتعاش 1–2 بكسل، أطراف مدورة، تجاوز عند الزوايا، وأجسام من 5–30 ضربة فقط. / 1–2 px wobble, round caps, corner overshoot, objects from 5–30 strokes.

**متى:** كل رسم يدوي / every hand-drawn look.

**كيف:** offset path vertices with seeded noise ±0.5–2 px (Catmull-Rom smoothed), width variation ±10–20%, stroke 2–6 px warm dark ink (#1a1a18, #2a2a2a, #3a2a1e); flat fills that slightly miss the outline; paper/board texture 5–10%, static unless the style boils; keep the seed fixed per stroke so frames do not jitter by accident.

**المعاملات:** wobble 1–2 px; 5–30 strokes; texture 5–10%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** wobble · imperfection · jitter · ink · ارتعاش

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/playbooks/hand-drawn.md:16`
- `kosif-tool/styles/map-journey`
- `kosif-tool/styles/pm-hbcoop-de365c`

#### 7. قدرات قريبة في العائلة

- `DRAW-23` علامات rough-notation / Rough-notation marks (install)
- `DRAW-24` خط الرحلة من اليمين / Journey line draw-on (RTL) (ready)
- `DRAW-26` غليان الخط / Line boil (documented)
- `DRAW-27` رسم خشن بأسلوب Rough.js / Rough.js / Excalidraw sketch rendering (install)

### `DRAW-26` — غليان الخط / Line boil

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الخطوط تعيد ارتعاشها كل إطارين أو ثلاثة فيبدو الرسم حيًا مرسومًا باليد. / Lines re-wobble every 2–3 frames so the drawing feels hand-animated.

**متى:** دودل، رسوم أطفال، رصاص / doodles, kids' stories, pencil looks.

**كيف:** seed = floor(t·12) (on twos at 24 fps) or floor(t·8) (on threes); amplitude 0.5–1.5 px at 1080p (graphite ±1.2 px, roughness 1.5); or cycle 3 pre-made stroke variants; boil only the drawing, never Arabic text outlines; HyperFrames hw-boil provides the same seeded, seek-safe jitter (off/calm/lively).

**المعاملات:** 8–12 fps; 0.5–1.5 px; 3 variants

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** boil · jitter · on twos · غليان · hand drawn

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/playbooks/hand-drawn.md:28`
- `kosif-atlas/skills/2414-animation/9355-learn-style`
- `kosif-tool/styles/pm-nikolajankovic-ce4ff4`
- `kosif-one/vendor/hyperframes/registry/components/hw-boil/hw-boil.html`

#### 7. قدرات قريبة في العائلة

- `DRAW-24` خط الرحلة من اليمين / Journey line draw-on (RTL) (ready)
- `DRAW-25` عدم الكمال المقصود / Deliberate imperfection (documented)
- `DRAW-27` رسم خشن بأسلوب Rough.js / Rough.js / Excalidraw sketch rendering (install)
- `DRAW-28` خطوط بضغط على طريقة perfect-freehand / Pressure strokes & clipped hatching (proven)

### `DRAW-27` — رسم خشن بأسلوب Rough.js / Rough.js / Excalidraw sketch rendering

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أشكال SVG/Canvas بارتعاش متحكم وتعبئة بخطوط مائلة أو متقاطعة. / Sketchy SVG/Canvas shapes with controllable wobble and hachure/cross-hatch fills.

**متى:** مخططات بإحساس يدوي، سبورة ذهنية / hand-feel diagrams, mind boards.

**كيف:** rough.svg(svg).rectangle(x,y,w,h,{roughness:0–2, fill, fillStyle:'hachure'\|'cross-hatch'\|'solid', hachureGap, seed}) — fixed seed per element (no accidental boil) or seed = floor(t·12) for deliberate boil; Excalidraw JSON elements carry the same fields (roughness 0/1/2, strokeStyle solid\|dashed\|dotted). Reveal drawn elements with DRAW-01.

**المعاملات:** roughness 0–2; fixed seed

**التثبيت:** npm i roughjs

**الوسوم:** roughjs · excalidraw · hachure · sketch · خشن

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`
- `kosif-atlas/skills/2790-work/11181-draw-excalidraw`

#### 7. قدرات قريبة في العائلة

- `DRAW-25` عدم الكمال المقصود / Deliberate imperfection (documented)
- `DRAW-26` غليان الخط / Line boil (documented)
- `DRAW-28` خطوط بضغط على طريقة perfect-freehand / Pressure strokes & clipped hatching (proven)
- `DRAW-29` حبر بصمة بضغط وتظليل / Basma INK pressure strokes & hatching (ready)

### `DRAW-28` — خطوط بضغط على طريقة perfect-freehand / Pressure strokes & clipped hatching

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** النقاط على المسار تتحول إلى مضلع خط بعرض متغير كالحبر أو الماركر أو الطباشير، ويُرسم تدريجيًا بتمرير جزء من النقاط. / Path points become a variable-width ink/marker/chalk polygon, drawn progressively by passing a prefix of the points.

**متى:** سبورة ودودل وطباشير بجودة يدوية / premium whiteboard, doodle and chalk.

**كيف:** sample with getPointAtLength (clamp to L − 1e-4); getStroke(points.slice(0, n·ease(p)), {size, thinning, simulatePressure}) → fill the outline polygon; marker size 8–10 thinning .6; chalk size 6–8 thinning .5 drawn twice (halo ×2.2 at ~0.12 opacity, then the stroke); doodle 3–6 px at 720 w ink #2f2820 with pressure from sin over arc length; cache static shapes. No install needed — whiteboard-draw (verified 13/13) ships its own builder: resample every 2.5 px, width = size × pressure × start taper × end taper, pressure 1.10 − 0.32·(v/vmax) (faster = thinner), start taper 0.42 + 0.58·min(1, s/16), end taper 0.30 + 0.70·min(1, (L − s)/22), felt-tip grain, outline = left/right offsets + two round caps filled with multiply so crossings darken; hatching = wavy parallel zig-zag lines drawn without lifting, then ctx.clip() to the shape (sun −35° gap 19 px, drop 35°, pot ±45° cross-hatch gap 24 px, leaves 70°/110° gap 15 px). The npm library (npm i perfect-freehand) is an alternative.

**المعاملات:** marker 8–10/.6; chalk 6–8/.5; halo ×2.2; resample 2.5 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hatching · perfect-freehand · pressure · marker · chalk · ink

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md`
- `kosif-tool/styles/whiteboard`
- `kosif-tool/styles/chalkboard`
- `kosif-tool/styles/doodle`

#### 7. قدرات قريبة في العائلة

- `DRAW-26` غليان الخط / Line boil (documented)
- `DRAW-27` رسم خشن بأسلوب Rough.js / Rough.js / Excalidraw sketch rendering (install)
- `DRAW-29` حبر بصمة بضغط وتظليل / Basma INK pressure strokes & hatching (ready)
- `DRAW-30` محرك فرشاة الحبر الحتمي / Deterministic ink-brush engine (documented)

### `DRAW-29` — حبر بصمة بضغط وتظليل / Basma INK pressure strokes & hatching

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط يُرسم تدريجيًا بطول القوس بأطراف مدببة وضغط متغير ويعيد رأس القلم، وتعبئة شكل مغلق بتظليل مائل تدريجي كالماركر. / Progressive tapered pressure strokes returning the pen head, plus progressive diagonal hatching.

**متى:** محرر بصمة وأفلام السبورة فيه / the Basma editor and its board films.

**كيف:** INK.stroke(c, pts, k, w, col, seed, {plain, alpha}): cumulative length; taper = min(1, .35 + 5u, .35 + 5(1 − u)); pressure .74 + .26·sin(0.9i + 3.7·seed); INK.strokes runs a list sequentially sharing progress by length; INK.at returns the point at fraction k. INK.hatch(c, outline, k, col, gap, w, alpha=.5) clips to the outline and draws diagonal lines up to k of the span.

**المعاملات:** taper .35 + 5u; pressure .74 ± .26

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ink · pressure · taper · hatching · تظليل · بصمة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `app/public/js/10_studio.js:208`
- `app/public/js/10_studio.js:232`

#### 7. قدرات قريبة في العائلة

- `DRAW-27` رسم خشن بأسلوب Rough.js / Rough.js / Excalidraw sketch rendering (install)
- `DRAW-28` خطوط بضغط على طريقة perfect-freehand / Pressure strokes & clipped hatching (proven)
- `DRAW-30` محرك فرشاة الحبر الحتمي / Deterministic ink-brush engine (documented)
- `DRAW-31` ملمس الرصاص والطباشير بالمرشحات / Pencil & chalk texture filters (documented)

### `DRAW-30` — محرك فرشاة الحبر الحتمي / Deterministic ink-brush engine

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المسارات تُرسم بكبسولات فرشاة مع ضبابية JS قابلة للفصل وطبقات نغمية وحبيبات ورق، فيعطي المدخل نفسه نفس البكسلات. / Paths rendered through capsule dabs, separable JS blur, tone layers and paper grain — identical pixels every time.

**متى:** أسلوب حبر وفرشاة جافة فاخر / premium ink and dry-brush looks.

**كيف:** capsule dabs of width 2·bias along contours; implement blur in JS because Chromium ctx.filter blur silently no-ops below ~0.8 px (source blur σ ≈ 0.85 px); tone layers at several greys for dry-brush; paperGrain opacity (off for a faithful copy); expose window.renderFrame(t) for frame capture.

**المعاملات:** blur floor 0.8 px; σ 0.85

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ink brush · capsule · dry brush · paper grain · فرشاة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/2414-animation/9357-rotoscope/SKILL.md`
- `kosif-atlas/skills/2414-animation/9357-rotoscope/reference/method.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-28` خطوط بضغط على طريقة perfect-freehand / Pressure strokes & clipped hatching (proven)
- `DRAW-29` حبر بصمة بضغط وتظليل / Basma INK pressure strokes & hatching (ready)
- `DRAW-31` ملمس الرصاص والطباشير بالمرشحات / Pencil & chalk texture filters (documented)
- `DRAW-32` خطوط ماء موازية للساحل / Triple coastline water lines (seen)

### `DRAW-31` — ملمس الرصاص والطباشير بالمرشحات / Pencil & chalk texture filters

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ملمس رصاص من feTurbulence + feDisplacementMap، وغبار طباشير صغير ينفث عند اكتمال كل حد في المعادلة. / Pencil texture via SVG turbulence + displacement, and a chalk-dust puff on each completed term.

**متى:** مشهد رصاص هادئ، معادلات طباشير / quiet pencil scenes, chalk formulas.

**كيف:** <filter><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="1.5–3"/></filter> on strokes, static seed; chalk: dusty stroke texture + 6–10 small particles that puff out and fade over ~300 ms at each term's completion.

**المعاملات:** displacement 1.5–3; puff ~300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pencil texture · feTurbulence · chalk dust · رصاص · طباشير

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/1094-akbun-draw/2419-akbun-draw-quiet-pencil/SKILL.md`
- `kosif-tool/playbooks/hand-drawn.md:50`

#### 7. قدرات قريبة في العائلة

- `DRAW-29` حبر بصمة بضغط وتظليل / Basma INK pressure strokes & hatching (ready)
- `DRAW-30` محرك فرشاة الحبر الحتمي / Deterministic ink-brush engine (documented)
- `DRAW-32` خطوط ماء موازية للساحل / Triple coastline water lines (seen)
- `DRAW-33` سبورة بيضاء / Whiteboard (proven)

### `DRAW-32` — خطوط ماء موازية للساحل / Triple coastline water lines

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يُخطّ حد البحر ثلاث مرات بعروض متناقصة بالتناوب بين الحبر ولون البحر داخل مضلع البحر، فتظهر ثلاث تموجات موازية. / The sea boundary stroked three times inside the sea polygon for three parallel ripples.

**متى:** خرائط مرسومة وقصص رحلات / hand-drawn maps and journeys.

**كيف:** clip to the sea polygon; stroke widths ~18 / 12 / 6 px alternating ink #5d5140 then sea #bfcdbe on top.

**المعاملات:** 18/12/6 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** coastline · water lines · map · ساحل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/map-journey`

#### 7. قدرات قريبة في العائلة

- `DRAW-30` محرك فرشاة الحبر الحتمي / Deterministic ink-brush engine (documented)
- `DRAW-31` ملمس الرصاص والطباشير بالمرشحات / Pencil & chalk texture filters (documented)
- `DRAW-33` سبورة بيضاء / Whiteboard (proven)
- `DRAW-34` سبورة سينمائية / Whiteboard cinematic (ready)

### `DRAW-33` — سبورة بيضاء / Whiteboard

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسم بالماركر على سبورة خطوة بخطوة بيد أو بلا يد، متزامن مع الصوت، ثم انتقال إلى مساحة نظيفة. / Marker drawing step by step with or without a hand, synced to the voice, then a pan to clean space.

**متى:** دروس وشروحات بتعليق صوتي / narrated lessons.

**كيف:** python3 tools/kosif.py scaffold whiteboard <dir> (playbook hand-drawn); hold 1.5–2 s at sentence end, then pan one board-width in 800 ms ease-in-out; each sentence triggers its element's draw-on (start = sentence onset). Basma STY.whiteboard: 16:9, calm, 2.0 wps, font Marhey, bg #F4F4F1, ink #23272E, accent #E0412E, colours #1E63D6 / #E0412E / #F28C12 / #2E9B4F; sfx write=pen, line=click, end=shimmer; lines revealed right→left behind the pen. style:whiteboard wrote an Arabic title with a soft mask and marker tip. Proof film whiteboard-draw (1080×1920, 10 s, 300 frames, −14.1 LUFS, 13/13): 'كيف تنمو النبتة؟' cause → effect lesson on an ivory board #f6f3ec with ±2.5% value-noise texture, fibres and faint old erase marks; inks black #1e2330, blue #1f5fd1, red #d6332b; marker squeak synthesised from the same stroke schedule.

**المعاملات:** hold 1.5–2 s; pan 800 ms; 2.0 wps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** whiteboard · سبورة · marker · lesson · explainer

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md`
- `kosif-tool/styles/whiteboard/SKILL.md`
- `kosif-tool/playbooks/hand-drawn.md:29`
- `app/public/js/10_studio.js:342`

#### 7. قدرات قريبة في العائلة

- `DRAW-31` ملمس الرصاص والطباشير بالمرشحات / Pencil & chalk texture filters (documented)
- `DRAW-32` خطوط ماء موازية للساحل / Triple coastline water lines (seen)
- `DRAW-34` سبورة سينمائية / Whiteboard cinematic (ready)
- `DRAW-35` سبورة الطباشير / Chalkboard (ready)

### `DRAW-34` — سبورة سينمائية / Whiteboard cinematic

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرح السبورة مع دفع كاميرا وعمق وتأطير درامي بين الرسومات. / Whiteboard explainer upgraded with camera dolly, depth and dramatic framing.

**متى:** شرح أطول يحتاج طاقة / longer explainers that need energy.

**كيف:** python3 tools/kosif.py scaffold whiteboard-cinematic <dir>; draw-on 800–1400 px/s with a hand pinned to the tip; after a 1.5–2 s hold the camera pushes/pans to clean board space; pen 4/8 px; texture 5–10%.

**المعاملات:** pen 4/8 px; texture 5–10%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** whiteboard cinematic · camera dolly · سبورة سينمائية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/whiteboard-cinematic/SKILL.md`
- `kosif-tool/styles/whiteboard-cinematic/STYLE.json`

#### 7. قدرات قريبة في العائلة

- `DRAW-32` خطوط ماء موازية للساحل / Triple coastline water lines (seen)
- `DRAW-33` سبورة بيضاء / Whiteboard (proven)
- `DRAW-35` سبورة الطباشير / Chalkboard (ready)
- `DRAW-36` قصص الدودل / Doodle stories (ready)

### `DRAW-35` — سبورة الطباشير / Chalkboard

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسم بالطباشير على سبورة خضراء أو سوداء بحبر معكوس، لدروس الرياضيات والعلوم. / Chalk on a green/black board with inverted ink.

**متى:** رياضيات، علوم، معادلات / maths, science, formulas.

**كيف:** python3 tools/kosif.py scaffold chalkboard <dir>; draw-on 800–1400 px/s, chalk-textured strokes, board texture 5–10%. Basma STY.chalkboard: 16:9, calm, 1.9 wps, font Aref Ruqaa, bg #264A3E, ink #F3F1E7, accent #F6E07A, colours #F6E07A / #F4A9BC / #9AD3F0 / #A9E6A2; sfx write=chalk, line=tick, end=shimmer. All timings × one slowness factor TS (EASE-08).

**المعاملات:** 1.9 wps; #264A3E / #F3F1E7

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** chalkboard · طباشير · maths · lesson

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/chalkboard/SKILL.md`
- `app/public/js/10_studio.js:471`

#### 7. قدرات قريبة في العائلة

- `DRAW-33` سبورة بيضاء / Whiteboard (proven)
- `DRAW-34` سبورة سينمائية / Whiteboard cinematic (ready)
- `DRAW-36` قصص الدودل / Doodle stories (ready)
- `DRAW-37` قلم البلوتر / Plotter pen (ready)

### `DRAW-36` — قصص الدودل / Doodle stories

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عالم مرسوم بالحبر في لقطة واحدة مستمرة، شخصية تمشي، وكلام كلمة بكلمة مع كلمة متوهجة. / An ink world in one continuous take with a walking character and word-by-word speech.

**متى:** حكايات وقصص أطفال وأمثال / tales, kids' stories, proverbs.

**كيف:** python3 tools/kosif.py scaffold doodle <dir>; boil 3 stroke variants every 2–3 frames; continuous camera through the world; every sentence spawns one prop (sign, question bubble, heart card) popping 0→1.08→1. Basma STY.doodle: 9:16, calm, 1.9 wps, Tajawal; sky #AFDCF0→#EAF6F4, sand #F1D9AE, grass #BCDB92, water #6FB3C8, ink #3A2A1E, text #1E2B45, emphasis #F07F2E, glow #FFD0A0, robe #F6F0E4, turban #2F4E86, skin #C98B5B; sfx pop/shimmer/swish/swell.

**المعاملات:** 9:16; 1.9 wps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** doodle · دودل · story · ink world · kids

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/doodle/SKILL.md`
- `app/public/js/10_studio.js:854`

#### 7. قدرات قريبة في العائلة

- `DRAW-34` سبورة سينمائية / Whiteboard cinematic (ready)
- `DRAW-35` سبورة الطباشير / Chalkboard (ready)
- `DRAW-37` قلم البلوتر / Plotter pen (ready)
- `DRAW-38` إطار بإطار على اثنين / Frame-by-frame on twos (ready)

### `DRAW-37` — قلم البلوتر / Plotter pen

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قلم بلوتر ميكانيكي يرسم منحنى بسرعة ثابتة على ورق شبكي داكن بشرارة برتقالية وتعليقات أحادية العرض. / A mechanical pen plotter traces a curve at constant speed with an orange spark and mono annotations.

**متى:** شرح تقني وبرمجي / tech explainers.

**كيف:** python3 tools/kosif.py scaffold plotter <dir>; constant pen speed, no easing, optional pen-up travel lines at 10%. Basma STY.plotter: 16:9, tech, 2.2 wps, Readex Pro + IBM Plex Mono, bg #0B0B0C, ink #F4F4F2, dim #3A3A3E, accent #FF5A1F, grid rgba(255,255,255,.055) at 6.2% drifting 3 px/s, 180-point seeded curve, timeline ruler and STEP counters, vignette 0.5 + grain 0.08; style:plotter spark: line 1.5 px bone-white, core 6 px #f27525, glow 10 px, 1–2 s per stroke.

**المعاملات:** 2.2 wps; spark 6 px; grid drift 3 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** plotter · بلوتر · constant speed · tech · spark

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/plotter/SKILL.md`
- `app/public/js/10_studio.js:292`
- `kosif-tool/styles/plotter`

#### 7. قدرات قريبة في العائلة

- `DRAW-35` سبورة الطباشير / Chalkboard (ready)
- `DRAW-36` قصص الدودل / Doodle stories (ready)
- `DRAW-38` إطار بإطار على اثنين / Frame-by-frame on twos (ready)
- `DRAW-39` رسومات الماركر للقصص / Marker-doodle story illustrations (documented)

### `DRAW-38` — إطار بإطار على اثنين / Frame-by-frame on twos

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إحساس الرسوم التقليدية المرسومة لكل إطار: رسمة جديدة كل إطارين وغليان بثلاث نسخ. / Traditional per-frame drawn feel: a new drawing every 2 frames, boil with 3 variants.

**متى:** لحظات عاطفية أو فنية / emotional or artistic moments.

**كيف:** python3 tools/kosif.py scaffold frame-by-frame <dir>; swap drawings every 2 frames (12 drawings/s at 24 fps); boil with 3 stroke variants every 2–3 frames; camera moves stay on ones (EASE-77).

**المعاملات:** 12 dps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** frame by frame · on twos · traditional · إطار بإطار

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/frame-by-frame/SKILL.md`
- `kosif-tool/styles/frame-by-frame/STYLE.json`

#### 7. قدرات قريبة في العائلة

- `DRAW-36` قصص الدودل / Doodle stories (ready)
- `DRAW-37` قلم البلوتر / Plotter pen (ready)
- `DRAW-39` رسومات الماركر للقصص / Marker-doodle story illustrations (documented)
- `DRAW-40` مشهد الرصاص الهادئ بلون واحد / Quiet pencil one-accent scene (documented)

### `DRAW-39` — رسومات الماركر للقصص / Marker-doodle story illustrations

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مظهر التسجيل البصري: ورق كريمي، حدود كحلية مرتعشة، تظليل ماركر يتجاوز الخطوط، 3–5 ألوان زاهية، حشود بيضاء بلا وجوه، وأسهم تأكيد حمراء. / The graphic-recording look.

**متى:** قصة من 2–5 مشاهد: مقدمة ← مشكلة ← حل / 2–5 scene stories.

**كيف:** Procedural here: SVG jittered strokes + hatch patterns + draw-on; or one generated plate per beat with a fixed CHARACTER sentence reused verbatim (models have no memory), English prompt slots only, 1–2 short labels max, then reveal the plate with a draw-on mask or wipe — set any Arabic as real type on top (ARAB-09).

**المعاملات:** 3–5 colours; 2–5 scenes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** graphic recording · marker doodle · story · رسوم ماركر

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/1094-akbun-draw/2421-akbun-draw-storytellingimage/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-37` قلم البلوتر / Plotter pen (ready)
- `DRAW-38` إطار بإطار على اثنين / Frame-by-frame on twos (ready)
- `DRAW-40` مشهد الرصاص الهادئ بلون واحد / Quiet pencil one-accent scene (documented)
- `DRAW-41` إطارات ستوري بورد بالرصاص / Pencil storyboard frames (documented)

### `DRAW-40` — مشهد الرصاص الهادئ بلون واحد / Quiet pencil one-accent scene

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشهد رصاص رمادي على ورق كريمي، ثلثاه الأعليان فارغان، 1–3 أشخاص صغار على خط أرض منخفض، وشيء واحد فقط بلون أزرق مخضر حيث يقع المعنى. / Graphite scene on cream paper, top two-thirds empty, one teal object where the meaning lands.

**متى:** سرد تأملي، بطاقات نهاية / reflective narration B-roll, end cards.

**كيف:** paper #F4ECDC, 4:3, graphite #4A4A4A–#9A9A9A hatching only, figure seen from behind, ONE flat teal #2E7D8C prop; pencil texture (DRAW-31) with slow draw-on; in motion animate only the coloured object or use it as the transition anchor; the subject changes, the style never does.

**المعاملات:** #F4ECDC; #2E7D8C; top 2/3 empty

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** quiet pencil · graphite · one accent · رصاص هادئ · minimal

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/1094-akbun-draw/2419-akbun-draw-quiet-pencil/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-38` إطار بإطار على اثنين / Frame-by-frame on twos (ready)
- `DRAW-39` رسومات الماركر للقصص / Marker-doodle story illustrations (documented)
- `DRAW-41` إطارات ستوري بورد بالرصاص / Pencil storyboard frames (documented)
- `DRAW-42` خريطة رحلة مرسومة باليد / Hand-drawn route sketch map (documented)

### `DRAW-41` — إطارات ستوري بورد بالرصاص / Pencil storyboard frames

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إطارات 16:9 بالرصاص الرمادي بلا لون إلا خطوط حمراء رفيعة لمحور الكاميرا وخط النظر، وكاميرا مرسومة على حامل بسهم اتجاه. / Grey-pencil 16:9 storyboard frames with red camera-axis lines.

**متى:** تخطيط لقطات قبل التصوير أو التوليد / planning shots before filming or generating.

**كيف:** per shot fill props, camera position, person view, action, frame cut line; render procedurally (jittered SVG strokes, dashed frame rectangle, handwritten dimension notes) or via an image model (external).

**المعاملات:** 16:9; grey pencil + red axis

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** storyboard · pencil · shot planning · ستوري بورد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2448-akbun-vlog-shotsketch/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-39` رسومات الماركر للقصص / Marker-doodle story illustrations (documented)
- `DRAW-40` مشهد الرصاص الهادئ بلون واحد / Quiet pencil one-accent scene (documented)
- `DRAW-42` خريطة رحلة مرسومة باليد / Hand-drawn route sketch map (documented)
- `DRAW-43` مخططات تجادل لا تعرض / Diagrams that argue (sketch patterns) (documented)

### `DRAW-42` — خريطة رحلة مرسومة باليد / Hand-drawn route sketch map

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسم مسطح بملمس الطباشير الملون لمسار رحلة: محطات مرقمة على ورق كريمي وخطوط ملونة بلا طرق مخترعة. / Crayon-textured trip map with numbered stops and no invented roads.

**متى:** قصص سفر ومدونات / travel stories.

**كيف:** paper #FBF6E9, confirmed path #B9AEA6, routes #8CC63F / #8E6BB0 / #F2A03D, greenery #DDE8B5 #7FB241 #3F6B2A, water #A9CDE8, ink #2B2B2B, panel #F7F1DC; 3:4; numbers only as text; without direction info stops flow top→bottom; draw with a rough stroke filter and animate route draw-on (DRAW-01).

**المعاملات:** 3:4; 3 route colours

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** route map · travel · sketch map · خريطة رحلة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/1094-akbun-draw/2422-akbun-draw-travel-blog/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-40` مشهد الرصاص الهادئ بلون واحد / Quiet pencil one-accent scene (documented)
- `DRAW-41` إطارات ستوري بورد بالرصاص / Pencil storyboard frames (documented)
- `DRAW-43` مخططات تجادل لا تعرض / Diagrams that argue (sketch patterns) (documented)
- `DRAW-44` رسوم خطية استعارية تتحرك / Line-art metaphor motions (seen)

### `DRAW-43` — مخططات تجادل لا تعرض / Diagrams that argue (sketch patterns)

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الشكل يحمل المعنى: تفرّع، تقارب، شجرة، دورة، سحابة، خط إنتاج، مقارنة، فجوة / ولو حذفت النص يبقى المعنى. — Shape carries the argument; remove the text and it still communicates.

**متى:** شرح فكرة معقدة بالرسم / explaining an idea by drawing.

**كيف:** timelines as a line with 10–20 px dots and free labels; trees as trunk + branch lines; assembly line chaos → process → order; Excalidraw-style roughness 0 smooth / 1 default / 2 rough; reveal strokes in argument order. See EXPL for full diagram powers.

**المعاملات:** dots 10–20 px; roughness 0–2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** visual patterns · diagrams · excalidraw · isomorphism

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/2790-work/11181-draw-excalidraw/references/visual-patterns.md`
- `kosif-atlas/skills/2790-work/11181-draw-excalidraw/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-41` إطارات ستوري بورد بالرصاص / Pencil storyboard frames (documented)
- `DRAW-42` خريطة رحلة مرسومة باليد / Hand-drawn route sketch map (documented)
- `DRAW-44` رسوم خطية استعارية تتحرك / Line-art metaphor motions (seen)
- `DRAW-45` قص الرسومات من صفحة الكراسة / Sketch cut-out lift & eraser wipe (documented)

### `DRAW-44` — رسوم خطية استعارية تتحرك / Line-art metaphor motions

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسم خطي بسيط يتحرك ليقول الفكرة: ناسخة تُخرج نسخًا وبقعة حمراء تنتشر، حديقة تنمو من جذورها، أقواس تحريك حول كوب، يدان تطلقان شيئًا يكمل وحده. / Simple line art that moves to state the idea.

**متى:** استعارات في الشرح والإعلان / metaphors in explainers and ads.

**كيف:** copier: 2 px charcoal outline, pages slide out 600 ms, a red blot spreads to show the error copied everywhere; garden: flowers scaleY from the root (transform-origin bottom) 500–700 ms easeOut, stagger 80 ms, insects on Lissajous paths with wing flap scaleX at 8 Hz; stirring: two thin elliptical arcs rotating ~1 turn/s; hands release: 900 ms cubic-bezier(.33,1,.68,1), 120 ms hold, then linear drift; hang strings: 1 px gold lines draw down, then the word drops on a spring.

**المعاملات:** 600 ms; 8 Hz flap; 900 ms release

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** line art · metaphor · growing · رسم خطي · استعارة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/pm-henkvaness-0e06af`
- `kosif-tool/styles/pm-abderrahmen-g-9e8ed0`
- `kosif-tool/styles/pm-sarut0bisasuke-cefa43`
- `kosif-tool/styles/pm-robvjourney-ce3e1a/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-42` خريطة رحلة مرسومة باليد / Hand-drawn route sketch map (documented)
- `DRAW-43` مخططات تجادل لا تعرض / Diagrams that argue (sketch patterns) (documented)
- `DRAW-45` قص الرسومات من صفحة الكراسة / Sketch cut-out lift & eraser wipe (documented)
- `DRAW-46` شريط مخطط يُرسم / Striped ribbon draw-on (seen)

### `DRAW-45` — قص الرسومات من صفحة الكراسة / Sketch cut-out lift & eraser wipe

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسومات ممسوحة تُرفع عن صفحة كراسة مصورة بأقنعة شفافية وتتحرك كقصاصات، والمسح بشكل ممحاة. / Scanned drawings lifted off a sketchbook page via alpha masks; eraser-shaped wipes.

**متى:** كولاج يدوي من رسومات المستخدم / handmade collage from the user's own drawings.

**كيف:** PNG alpha cut-outs moved only by translate, rotate ≤ ±12° and uniform scale — never recolour or trace the user's art; line boil by cycling 2–3 scan variants or 2 px jitter held on threes (8 fps); eraser wipe: a 400 ms mask following an eraser sprite's path.

**المعاملات:** rotate ≤ ±12°; boil 8 fps 2 px; wipe 400 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cut-out · sketchbook · eraser · قصاصات · ممحاة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/pm-abderrahmen-g-9e8ed0/BRIEF.md`
- `kosif-tool/styles/pm-tak3sh8-be5012/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-43` مخططات تجادل لا تعرض / Diagrams that argue (sketch patterns) (documented)
- `DRAW-44` رسوم خطية استعارية تتحرك / Line-art metaphor motions (seen)
- `DRAW-46` شريط مخطط يُرسم / Striped ribbon draw-on (seen)
- `DRAW-47` من مخطط سلكي إلى مجسم / Wireframe draw → solid formation (ready)

### `DRAW-46` — شريط مخطط يُرسم / Striped ribbon draw-on

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة خطوط متوازية بالأحمر والأبيض والأزرق تُرسم معًا على منحنى. / Three parallel offset strokes draw together along a curve.

**متى:** رياضة، أعلام، مناسبات / sports, flags, occasions.

**كيف:** one curve, three strokes at offsets (width ~30 px total) drawn by dashoffset over 1.5 s; for Arab flags swap to their real colours.

**المعاملات:** 1.5 s; ~30 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ribbon · stripes · flag · شريط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/styles/pm-mrtanviir-132457`
- `kosif-tool/styles/pm-umangratani-57f86a`

#### 7. قدرات قريبة في العائلة

- `DRAW-44` رسوم خطية استعارية تتحرك / Line-art metaphor motions (seen)
- `DRAW-45` قص الرسومات من صفحة الكراسة / Sketch cut-out lift & eraser wipe (documented)
- `DRAW-47` من مخطط سلكي إلى مجسم / Wireframe draw → solid formation (ready)
- `DRAW-48` ترتيب الرسام في الكشف / Painter reveal orders (proven)

### `DRAW-47` — من مخطط سلكي إلى مجسم / Wireframe draw → solid formation

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حواف شبكة سلكية تُرسم متتابعة، وشريط مسح يصعد على المجسم بحافة لامعة، ثم يتشكل المجسم النهائي من المخطط. / Mesh edges draw on, a scan band sweeps up the model, and the finished object forms from the schematic.

**متى:** «رقمنة» منتج أو شخصية، تقنية / digitising a product/character.

**كيف:** SVG edges dashoffset staggered (~1.5 s total); three.js: wireframe ShaderMaterial on the same geometry, band = smoothstep(.09, 0, scan − y)·step(y, scan + .004), edge = smoothstep(.012, 0, \|y − scan\|), colour (.62,1,.72)→(.95,1,.8), scanY lerp(−.02, .4) over .78 s, ground ring 0xd0ff6a scale 1.15→0.6; schematic(obj).set(form = 1 − ease(ramp(t, .4, 2.8))), explode(.35·pulse), joints glow (three-kit bundle in the kit folder).

**المعاملات:** scan .78 s; form ramp .4–2.8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** wireframe · scan band · schematic · mesh draw · سلكي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:59`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:19`
- `kosif-tool/styles/pm-tdinh-me-815acb`

#### 7. قدرات قريبة في العائلة

- `DRAW-45` قص الرسومات من صفحة الكراسة / Sketch cut-out lift & eraser wipe (documented)
- `DRAW-46` شريط مخطط يُرسم / Striped ribbon draw-on (seen)
- `DRAW-48` ترتيب الرسام في الكشف / Painter reveal orders (proven)
- `DRAW-49` فيلم الرسم / Drawing film (picture forming as MP4) (proven)

### `DRAW-48` — ترتيب الرسام في الكشف / Painter reveal orders

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بكسلات كل خطوة تُرتب كما يضعها الرسام: فرشاة ذهابًا وإيابًا، نمو من نقطة، صعود من القدمين، نزول، يمين، يسار، أو تناثر للتفاصيل. / Each step's changed pixels laid down in painter order.

**متى:** فيلم «الصورة تُرسم» / 'picture being painted' films.

**كيف:** Step(name, ops, order='sweep'\|'grow'\|'rise'\|'down'\|'left'\|'right'\|'sparkle', origin=(x,y), weight); reveal_order(idx, W, step, scale, seed) returns a permutation; sweep bands round(7·scale) px boustrophedon with jitter 26·scale; grow = distance to origin + jitter 9·scale; rise/down/left/right jitter 7·scale; sparkle random. Permutation test passed here.

**المعاملات:** band 7·scale px; jitter 7–26·scale

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** painter · reveal order · sweep · grow · ترتيب الرسام

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/render.py:846`
- `kosif-studio/tests/test_studio.py:93`
- `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-46` شريط مخطط يُرسم / Striped ribbon draw-on (seen)
- `DRAW-47` من مخطط سلكي إلى مجسم / Wireframe draw → solid formation (ready)
- `DRAW-49` فيلم الرسم / Drawing film (picture forming as MP4) (proven)
- `DRAW-50` الرسم بترتيب الكود نفسه / PIL command recorder (proven)

### `DRAW-49` — فيلم الرسم / Drawing film (picture forming as MP4)

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يسجّل أي مشهد أو ملف كود أو صورة وهو يُرسم بكسلًا بكسلًا إلى فيديو H.264 ويثبت الإطار الأخير. / Records any scene, code file or image being painted into H.264, holding the final frame.

**متى:** تايم لابس رسم، «كيف رُسمت هذه» / painting timelapses.

**كيف:** python film.py drawing <scene\|code\|image> --out x.mp4 [--fps 30 --speed slow\|normal\|fast]; python film.py animate page.html\|scene.py --out x.mp4 --seconds 6; dur per step = SPEEDS[speed]·weight·√(n/area) (EASE-82); images wrapped as image code; native canvases fit into 1280×720 on #1b1b1b; libx264 preset medium crf 18 yuv420p, GOP 2·fps, +faststart; hold 1.5 s. Encode test passed here.

**المعاملات:** 30 fps; crf 18; hold 1.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** drawing film · timelapse · painting video · فيلم الرسم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/film.py:59`
- `kosif-studio/tests/test_studio.py:305`
- `100-superskills/skills/pixel-studio-painter/scripts/film.py:229`

#### 7. قدرات قريبة في العائلة

- `DRAW-47` من مخطط سلكي إلى مجسم / Wireframe draw → solid formation (ready)
- `DRAW-48` ترتيب الرسام في الكشف / Painter reveal orders (proven)
- `DRAW-50` الرسم بترتيب الكود نفسه / PIL command recorder (proven)
- `DRAW-51` الرسم المطابق تمامًا / Exact-match painting (proven)

### `DRAW-50` — الرسم بترتيب الكود نفسه / PIL command recorder

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يلتقط كل أمر مستطيل/إهليلج/مضلع/خط/قوس/نص في Pillow فتتكون الصورة بالترتيب الذي رسمها به الكود. / Every Pillow draw call is snapshotted so the picture forms in the code's own order.

**متى:** «اكتب كود يرسم… وأرني وهو يرسم» / showing code-drawn art being drawn.

**كيف:** Recorder.install() wraps ImageDraw methods, Image.paste/alpha_composite and save/show; consecutive calls of one kind are grouped (RUN = 20 commands per stroke: 360 sky lines → 18 strokes); stream thinned above 300 snapshots; labels are Arabic call names with counts; final job 'اللمسات الأخيرة'; image code is read as data, never executed. Runner tests passed here.

**المعاملات:** 20 commands/stroke; ≤300 snapshots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** PIL · recorder · code order · Pillow · مسجل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/runner.py:247`
- `kosif-studio/runner.py:39`
- `kosif-studio/tests/test_studio.py:331`

#### 7. قدرات قريبة في العائلة

- `DRAW-48` ترتيب الرسام في الكشف / Painter reveal orders (proven)
- `DRAW-49` فيلم الرسم / Drawing film (picture forming as MP4) (proven)
- `DRAW-51` الرسم المطابق تمامًا / Exact-match painting (proven)
- `DRAW-52` صورة إلى برنامج بايثون / Image to standalone Pillow program (proven)

### `DRAW-51` — الرسم المطابق تمامًا / Exact-match painting

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يعيد رسم أي صورة من ورقة شفافة على مراحل رسام وينتهي مطابقًا للأصل في كل قيمة RGBA: كتل لونية ثم تدقيق نغمي ثم تصحيح كل بكسل متبقٍ. / Repaints any image in painter stages and ends identical in every RGBA value.

**متى:** إعادة رسم شعار أو صورة كفيلم «يدوي» قابل للإثبات / a provable hand-made recreation.

**كيف:** exact.plan(rgba, block_k, fine_k): block-in uses the logo's own palette or Lab k-means on a bilateral-filtered copy (+median 5) with jobs 'grow' weight .9; refine splits changed pixels into luminance tertiles (shadows, mid-tones, lights) as 'sparkle' weight .7 (change threshold Σ\|diff\| > 12); final touches go from visible to invisible; asserts array_equal; photos try 4 plans (6/10/16/24 block colours) in ~3 s. Exact and JevPlan tests passed here.

**المعاملات:** bilateral 9/40/9; k-means ≤60000 samples, 40 iters

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** exact redraw · zero diff · painter · مطابق · block-in

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/exact.py:1`
- `kosif-studio/exact.py:151`
- `kosif-studio/tests/test_studio.py:157`
- `100-superskills/skills/pixel-studio-painter/scripts/exact.py`

#### 7. قدرات قريبة في العائلة

- `DRAW-49` فيلم الرسم / Drawing film (picture forming as MP4) (proven)
- `DRAW-50` الرسم بترتيب الكود نفسه / PIL command recorder (proven)
- `DRAW-52` صورة إلى برنامج بايثون / Image to standalone Pillow program (proven)
- `DRAW-53` استيراد SVG والتحويل إلى متجهات / SVG import & vectorize to draw steps (proven)

### `DRAW-52` — صورة إلى برنامج بايثون / Image to standalone Pillow program

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يكتب برنامج Pillow فقط يرسم مضلعات ثم يكمل البكسلات من الأصل المضمّن ويتحقق من نفسه. / Writes a Pillow-only program that draws polygons, completes pixels from the embedded original and self-verifies.

**متى:** «حوّل الصورة إلى كود» / 'turn this image into code'.

**كيف:** python3 to_python.py <image> (or studio.py --image-code); --data-only form; the program reproduces the image with plain Python (ImageToPython test passed here).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** image to code · Pillow · program · صورة إلى كود

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/tests/test_studio.py:185`
- `100-superskills/skills/pixel-studio-painter/scripts/to_python.py`

#### 7. قدرات قريبة في العائلة

- `DRAW-50` الرسم بترتيب الكود نفسه / PIL command recorder (proven)
- `DRAW-51` الرسم المطابق تمامًا / Exact-match painting (proven)
- `DRAW-53` استيراد SVG والتحويل إلى متجهات / SVG import & vectorize to draw steps (proven)
- `DRAW-54` محوّل مسارات SVG إلى نقاط / SVG path sampler (proven)

### `DRAW-53` — استيراد SVG والتحويل إلى متجهات / SVG import & vectorize to draw steps

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل عنصر SVG يصبح خطوة رسم بالترتيب، والشعار المسطح يتحول إلى متجهات بألوانه وثقوبه. / Every SVG element becomes a drawing step; flat logos vectorize keeping colours and holes.

**متى:** رسم شعار المستخدم أمام العين / drawing the user's logo on screen.

**كيف:** svg_import.py honours shapes, styles, transforms (rect, circle, ellipse, polygon, path arcs/smooth curves, gradients, text); vectorize keeps a flat logo's palette and its holes and treats noise as a photo; holes and even-odd compounds render correctly. Svg, Vectorize and Renderer tests passed here.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** svg import · vectorize · logo · draw steps · متجهات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-studio/svg_import.py:369`
- `kosif-studio/tests/test_studio.py:105`
- `100-superskills/skills/pixel-studio-painter/scripts/svg_import.py`

#### 7. قدرات قريبة في العائلة

- `DRAW-51` الرسم المطابق تمامًا / Exact-match painting (proven)
- `DRAW-52` صورة إلى برنامج بايثون / Image to standalone Pillow program (proven)
- `DRAW-54` محوّل مسارات SVG إلى نقاط / SVG path sampler (proven)
- `DRAW-55` الرسم بالفأرة في برنامج الرسام / Drawing by mouse in Windows Paint (documented)

### `DRAW-54` — محوّل مسارات SVG إلى نقاط / SVG path sampler

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحويل بيانات مسار SVG (مطلق/نسبي، منحنيات مكعبة وتربيعية) إلى نقاط بايثون خالصة لإعادة استخدامها في رسم تدريجي. / Pure-Python sampling of SVG path data into polylines for draw-on.

**متى:** رسم مسار في Pillow أو أي محرك بلا متصفح / draw-on outside the browser.

**كيف:** desktop._svg_paths(d) → list of point lists (M/L/H/V/C/Q/T/Z, curves sampled not chorded, closed paths return to start); _shape_paths(shapes); _fit_tf(paths, box, margin=0.08, viewbox); reveal points up to t in a render(t). Drawing tests 4/4 passed here.

**المعاملات:** margin 0.08; arcs every 6° (≥12 points)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** svg sampler · polyline · path points · python

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/desktop.py:1032`
- `kosif-one/tools/kosif-omni/mcp-server/tests/test_desktop.py:259`

#### 7. قدرات قريبة في العائلة

- `DRAW-52` صورة إلى برنامج بايثون / Image to standalone Pillow program (proven)
- `DRAW-53` استيراد SVG والتحويل إلى متجهات / SVG import & vectorize to draw steps (proven)
- `DRAW-55` الرسم بالفأرة في برنامج الرسام / Drawing by mouse in Windows Paint (documented)
- `DRAW-56` رسم فوق لقطات مولدة / Draw-over film on generated bases (documented)

### `DRAW-55` — الرسم بالفأرة في برنامج الرسام / Drawing by mouse in Windows Paint

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يرسم مسارات SVG أو أشكالًا ضربة بضربة في برنامج Paint بقلم صناعي، أو يعيد رسم صورة بكسلًا بكسلًا ويتحقق حتى التطابق. / Draws SVG paths stroke by stroke into Paint, or redraws an image pixel by pixel until identical.

**متى:** على جهاز ويندوز للمستخدم فقط / only on the user's Windows desktop.

**كيف:** kosif_mouse_act window=Paint actions=[{do:'draw', target:'canvas', viewbox:[0,0,100,100], svg:'M…'}]; closed shapes run on 30% past start to seal bucket fills; hatch gap 2 px; kosif_paint_copy image=<png> [zoom 4] [colors 64]: ~0.6–0.68 s per colour, ~1,030 px/s, 85×98 logo with 2,650 colours = 100% in ~25 min, 64 colours ~1.3 min mean ΔE 2.4. Not runnable in this Linux container.

**المعاملات:** limit 200,000 px; 64 colours ≈1.3 min

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Paint · mouse drawing · desktop · Windows · الرسام

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-mouse/SKILL.md`
- `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/replicate.py:1003`

#### 7. قدرات قريبة في العائلة

- `DRAW-53` استيراد SVG والتحويل إلى متجهات / SVG import & vectorize to draw steps (proven)
- `DRAW-54` محوّل مسارات SVG إلى نقاط / SVG path sampler (proven)
- `DRAW-56` رسم فوق لقطات مولدة / Draw-over film on generated bases (documented)
- `DRAW-57` دراسة أسلوب مرسوم بالتتبع / Rotoscope style study & style pack (documented)

### `DRAW-56` — رسم فوق لقطات مولدة / Draw-over film on generated bases

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المقاطع المولدة تعطي الحركة، وطبقة رسم بالكود هي الصورة الفعلية: حبران على ورق، نقاط هافتون، خطوط تغلي 12 مرة/ث، وكتابة كلمات حركية. / Generated clips give motion; a coded drawing layer is the actual picture.

**متى:** كليب أغنية بطابع مطبوع/مرسوم / a printed/drawn-look music video.

**كيف:** extract base frames with ffmpeg; renderAt(t) draws two inks on paper, halftone, line work, boil 12×/s, fixed paper tooth; shots.json {at, dur, base, baseStart, focus 0..1, type big\|quiet\|none, side}; render frame-exact in headless Chromium; mux the original audio; contact-sheet every cell; 16:9 and 1080×1920 from the same film.

**المعاملات:** boil 12 fps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** draw over · generated video · halftone · two inks · رسم فوق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/1511-homie/3903-video/SKILL.md`
- `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-54` محوّل مسارات SVG إلى نقاط / SVG path sampler (proven)
- `DRAW-55` الرسم بالفأرة في برنامج الرسام / Drawing by mouse in Windows Paint (documented)
- `DRAW-57` دراسة أسلوب مرسوم بالتتبع / Rotoscope style study & style pack (documented)
- `DRAW-58` إعادة رسم مخرجات مولدة كمتجهات / Generated raster → hand vector recreation (ready)

### `DRAW-57` — دراسة أسلوب مرسوم بالتتبع / Rotoscope style study & style pack

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | study tool — do not redistribute traced third-party art |

**ما هي:** فك رسوم مرجعية إلى رسمات مميزة، تتبعها إلى متجهات، إعادة رسمها وقياسها، ثم حفظ إحصاءات الأسلوب فقط (لوحة، خشونة، سماكة، غليان، ثبات). / Decode, trace, re-render and measure a reference, keeping only style statistics.

**متى:** «اعمل بنفس أسلوب الرسم هذا» دون نسخ الرسوم / 'match this drawn style' without copying it.

**كيف:** dedup drawings by large-grey-step pixel count; threshold at the ink/paper grey midpoint; supersample 4× (8× adds nothing) after an unsharp mask; findContours + approxPolyDP; measure XOR vs codec floor (~0.22%) and SSIM; store p10/p50/p90 bands in style.json and check new scenes against them. Study only — never ship traced third-party geometry or store source frames.

**المعاملات:** S = 4; XOR ~0.22%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** rotoscope · style pack · tracing · measure · دراسة أسلوب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-atlas/skills/2414-animation/9357-rotoscope/reference/method.md`
- `kosif-atlas/skills/2414-animation/9355-learn-style/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-55` الرسم بالفأرة في برنامج الرسام / Drawing by mouse in Windows Paint (documented)
- `DRAW-56` رسم فوق لقطات مولدة / Draw-over film on generated bases (documented)
- `DRAW-58` إعادة رسم مخرجات مولدة كمتجهات / Generated raster → hand vector recreation (ready)
- `DRAW-59` مكونات HyperFrames للرسم اليدوي / HyperFrames hand-drawn components (install)

### `DRAW-58` — إعادة رسم مخرجات مولدة كمتجهات / Generated raster → hand vector recreation

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حين لا يمكن تنزيل الصورة المولدة أو يجب أن تبقى حادة بأي حجم، تُعاد يدويًا كـ SVG صغير وتُقيَّم مقابل الأصل. / Recreate a generated raster as a compact SVG and score it against the render.

**متى:** خلفيات وشعارات تحتاج حدة وحركة طبقات / backgrounds and emblems needing sharpness and layers.

**كيف:** valley-dusk.svg: three dune paths with gradients (sky #8f8ae0 → #c9c3f5 → #f1e9fb), palms #4e46a8, flock ellipses, crescent and stars, 1200×600 xMinYMax slice — each dune is a parallax layer; scoring: Canva render 3.84/4 vs vector 3.79/4 for the emblem.

**المعاملات:** sky 2.6 KB SVG

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** vector recreation · svg · parallax layers · متجه

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-earth-ci-fork/ui/art/valley-dusk.svg`
- `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-56` رسم فوق لقطات مولدة / Draw-over film on generated bases (documented)
- `DRAW-57` دراسة أسلوب مرسوم بالتتبع / Rotoscope style study & style pack (documented)
- `DRAW-59` مكونات HyperFrames للرسم اليدوي / HyperFrames hand-drawn components (install)
- `DRAW-60` مكتبات الرسم التدريجي / Draw-on libraries (install)

### `DRAW-59` — مكونات HyperFrames للرسم اليدوي / HyperFrames hand-drawn components

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (GSAP standard no-charge license inside) |

**ما هي:** مكتبة مكونات وكتل يدوية جاهزة تُضاف بأمر واحد، كلها بمحرك GSAP متوقف وقابلة للبحث. / A ready library of hand-drawn components and blocks.

**متى:** تركيبات HyperFrames تحتاج علامات يدوية سريعة / HyperFrames compositions.

**كيف:** npx hyperframes add <name>, mount on a class="clip" div (data-composition-src, data-start/duration/track-index, JSON in data-variable-values). Components: hw-arrow (straight/gentle/swoop, plain/soft/sharp/spray, stretch pulse on arrival), hw-boil (seeded jitter off/calm/lively, wobbly ellipse, curvature-adaptive pen ease), hw-box-label, hw-callout-circle (scribble fill + curved connector), hw-underline (squiggle, double strike, bracket), cursor-annotate (pen draws loop/underline/arrow, #f43f5e, target in %), marker-highlight (highlight\|circle\|underline\|scribble at 0.9 s), vox-annotate (marker + connector to a mono label in one beat), whiteboard-ink (bulb\|flow\|rocket, pen nib), marker-checklist-card, yt-circle-pointer, svg-stroke-trace (stroke 12), svg-line-draw-loader, stitched-text-draw (fine\|coarse needle). Blocks: hw-frame (8 s), hw-path-text (6 s), hw-pipeline (flowchart 7 s), hw-scribble-transition (2.2 s), hw-text-cloud (speech bubble), hw-title, hw-write-title. Latin fonts bundled (Caveat, Permanent Marker, Courier Prime) — swap to an Arabic face and RTL masks for Arabic.

**المعاملات:** 21 items

**التثبيت:** npx hyperframes add hw-callout-circle

**الوسوم:** hyperframes · hw components · annotate · scribble transition · speech bubble

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/components`
- `kosif-one/vendor/hyperframes/registry/blocks`
- `kosif-one/vendor/hyperframes/registry/components/cursor-annotate/cursor-annotate.html`
- `kosif-one/vendor/hyperframes/registry/blocks/hw-scribble-transition/hw-scribble-transition.html`

#### 7. قدرات قريبة في العائلة

- `DRAW-57` دراسة أسلوب مرسوم بالتتبع / Rotoscope style study & style pack (documented)
- `DRAW-58` إعادة رسم مخرجات مولدة كمتجهات / Generated raster → hand vector recreation (ready)
- `DRAW-60` مكتبات الرسم التدريجي / Draw-on libraries (install)
- `DRAW-G01` رسم يدوي خشن ثابت البذرة / Seeded rough hand-drawn rendering (documented)

### `DRAW-60` — مكتبات الرسم التدريجي / Draw-on libraries

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مكتبات بديلة للرسم التدريجي والخشونة حين لا تكفي dashoffset المكتوبة يدويًا. / Alternative draw-on and roughness libraries.

**متى:** مشاريع npm أو Remotion / npm/Remotion projects.

**كيف:** vivus 0.4 (path draw-on scenarios), roughjs 4.6, rough-notation 0.5, perfect-freehand, @remotion/paths (getLength, evolvePath for draw-on in Remotion), @excalidraw/excalidraw (scene JSON → SVG). Wire every one to seek(t) (set progress directly), never their own requestAnimationFrame timers.

**التثبيت:** npm i vivus roughjs rough-notation perfect-freehand @remotion/paths

**الوسوم:** vivus · roughjs · perfect-freehand · remotion paths · libraries

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-58` إعادة رسم مخرجات مولدة كمتجهات / Generated raster → hand vector recreation (ready)
- `DRAW-59` مكونات HyperFrames للرسم اليدوي / HyperFrames hand-drawn components (install)
- `DRAW-G01` رسم يدوي خشن ثابت البذرة / Seeded rough hand-drawn rendering (documented)
- `DRAW-G02` زخم السحب والارتداد المطاطي / Drag momentum and rubber-band edges (documented)

### `DRAW-G01` — رسم يدوي خشن ثابت البذرة / Seeded rough hand-drawn rendering

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** ارسم الأشكال بمظهر يدوي (خشونة، انحناء، تهشير) ببذرة ثابتة لكل شكل حتى لا يرتعش عند إعادة الرسم، ثم اكشفه بطول المسار. — Draw shapes with a hand-made look (roughness, bowing, hachure) with one fixed seed per shape so it does not jitter on redraw, then reveal it by path length.

**متى:** شرح بأسلوب السبورة أو الكراسة / whiteboard or notebook-style explainers

**كيف:** Parameters: roughness 1-2, bowing 1, hachure fill with angle −41° and gap 4-8 px, stroke width 1.5-2.5; a seed per shape id (never Math.random per frame); animate with stroke-dasharray/offset over each generated path in drawing order (outline, then fill). For a lively loop change the seed every 3-4 frames on purpose ('boiling line'), not every frame.

**المعاملات:** roughness 1-2; boil every 3-4 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** excalidraw · rough.js · hand-drawn · sketchy · hachure · seed · رسم يدوي · سبورة · خشن

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-G01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `DRAW-59` مكونات HyperFrames للرسم اليدوي / HyperFrames hand-drawn components (install)
- `DRAW-60` مكتبات الرسم التدريجي / Draw-on libraries (install)
- `DRAW-G02` زخم السحب والارتداد المطاطي / Drag momentum and rubber-band edges (documented)
- `DRAW-P01` قصة الخط الواحد المستمر حتى الشعار / Continuous-line logo story (one stroke → three beats → wordmark loop) (documented)

### `DRAW-G02` — زخم السحب والارتداد المطاطي / Drag momentum and rubber-band edges

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** بعد إفلات السحب تستمر الحركة بسرعتها ثم تتباطأ أسيًا، وعند الحافة تقاوم بمعامل مطاطي ثم ترتد. — After a drag is released motion continues at its speed and decays exponentially; at the edge it resists with a rubber-band factor and springs back.

**متى:** محاكاة تمرير أو سلايدر داخل فيديو منتج أو تطبيق / simulating a scroll or slider inside a product or app video

**كيف:** Release velocity v0 from the last ~100 ms of drag; position x(t) = x0 + v0·τ·(1 − e^(−t/τ)) with τ ≈ 0.325 s; overscroll displayed = (1 − 1/(d·0.55/W + 1))·W for distance d past the edge and width W; return with a critically damped spring (EASE-G01). Feels like a real phone, so screen recordings and mock-ups read as genuine.

**المعاملات:** τ ≈ 0.325 s; rubber-band 0.55

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** momentum · rubber band · scroll physics · swiper · ui animation · زخم · سحب · ارتداد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-G02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `DRAW-60` مكتبات الرسم التدريجي / Draw-on libraries (install)
- `DRAW-G01` رسم يدوي خشن ثابت البذرة / Seeded rough hand-drawn rendering (documented)
- `DRAW-P01` قصة الخط الواحد المستمر حتى الشعار / Continuous-line logo story (one stroke → three beats → wordmark loop) (documented)
- `DRAW-U01` فيلم يد مرسومة حتمي بـmake_frame(t) / Deterministic hand-drawn film via make_frame(t) (documented)

### `DRAW-P01` — قصة الخط الواحد المستمر حتى الشعار / Continuous-line logo story (one stroke → three beats → wordmark loop)

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner package (own work) |

**ما هي:** خط واحد لا ينقطع يمر بثلاث محطات مرقّمة ثم يلتف حول الشعار، مع صوت مولّد بالكود. / One unbroken line travels through three numbered beats and closes into a loop around the wordmark, with code-synthesised sound.

**متى:** حين نريد خطا واحدا متصلا يمر بثلاث محطات ثم يلتف حول الشعار / when one unbroken line should pass three numbered beats and loop around the wordmark

**كيف:** 13 waypoints interpolated 18 steps each; drawn length = smoothstep(t/4.1); beat dots grow with smoothstep((t−(0.9+0.85k))/0.55) and their labels (01 CAPTURE, 02 CONNECT, 03 RESURFACE) appear at the same instants; from 4.25 s an ellipse (rx 100, ry 42) draws over 1.1 s around the wordmark. Editorial palette: paper (246,241,230), ink (31,36,34), one accent (213,70,48), 6 px stroke, pen-tip dot. Audio generated in NumPy (see BEAT-P01). Re-ran here: 6.000 s, 360×640, 24 fps, H.264 + AAC 96k. Status note: the code is owner material that is not vendored in this skill; the numbers above are from one run on the owner's copy on 2026-10-16 and cannot be re-run from here, so this is 📄 documented, not ✅.

**المعاملات:** 360×640 · 24 fps · 6 s · draw 4.1 s · beats at 0.9/1.75/2.6 s · loop 4.25–5.35 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** continuous line · one line · logo story · خط واحد · خيط بصري · editorial · رسم خط · قصة الشعار · ثلاث خطوات · draw on · line animation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-P01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/render_continuous_line.py`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Continuous_Line_Logo_Story.mp4`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/INTEGRATION_REPORT.json`

#### 7. قدرات قريبة في العائلة

- `DRAW-G01` رسم يدوي خشن ثابت البذرة / Seeded rough hand-drawn rendering (documented)
- `DRAW-G02` زخم السحب والارتداد المطاطي / Drag momentum and rubber-band edges (documented)
- `DRAW-U01` فيلم يد مرسومة حتمي بـmake_frame(t) / Deterministic hand-drawn film via make_frame(t) (documented)
- `DRAW-X01` ريشة تكتب السطر الفعلي / Quill that writes the actual line (ink frontier) (documented)

### `DRAW-U01` — فيلم يد مرسومة حتمي بـmake_frame(t) / Deterministic hand-drawn film via make_frame(t)

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** كل إطار يُحسب من الزمن المطلق (لا ساعة متراكمة): القفز والإعادة بلا انجراف والرندر المتوازي ممكن؛ سنّ القلم مربوط بنهاية الخط النشط وكشف الحبر على المسار وملمس ورق؛ الصوت الأصلي مسار رئيسي. اذكر دقة الرسم الأصلية (720×1280 مكبّرة إلى 1080×1920 في المشروع) وأن المشاهد تقريبية حين لا توجد محاذاة كلمات. — From the owner's doodle and hand-drawn projects.

**متى:** فيلم رسم باليد على تسجيل صوتي / a hand-drawn film over a voice recording

**كيف:** render.py --fps 30 --resolution 1080x1920؛ ثم ffprobe في تقرير QA.

**المعاملات:** 97.88 s, 13 beats, 30 fps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hand drawn · يد مرسومة · doodle · دودل · draw on · رسم · pen · قلم · whiteboard

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-U01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`

#### 7. قدرات قريبة في العائلة

- `DRAW-G02` زخم السحب والارتداد المطاطي / Drag momentum and rubber-band edges (documented)
- `DRAW-P01` قصة الخط الواحد المستمر حتى الشعار / Continuous-line logo story (one stroke → three beats → wordmark loop) (documented)
- `DRAW-X01` ريشة تكتب السطر الفعلي / Quill that writes the actual line (ink frontier) (documented)

### `DRAW-X01` — ريشة تكتب السطر الفعلي / Quill that writes the actual line (ink frontier)

| الحقل | القيمة |
|---|---|
| العائلة | `hand-drawn-draw-on` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/hand-drawn-draw-on.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (song audio and lyrics are third-party; not included) |

**ما هي:** يد بريشة تتبع حافة الحبر المتقدمة للسطر نفسه، فتبدو كأنها تكتب كلمات الأغنية حقًا. — A quill hand follows the advancing ink frontier of the line itself, so it truly seems to write the lyric.

**متى:** مشهد حبر على ورق في فيلم كلمات — an ink-on-paper scene in a lyric film.

**كيف:** Compute inkFrontier(t) from the line's reveal progress and place the hand's nib on it every frame (RTL for Arabic, so the hand moves right to left); keep the hand slightly behind the frontier so ink appears under the nib.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** quill · handwriting · ink · draw-on · ريشة · كتابة يدوية · حبر

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:DRAW-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `atlas-render` · `code-drawing-master` · `creative-paint` · `creative-reasoning-bridge` · `drawing-council`.
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

- `owner-upload:film_project/film/film.js`

#### 7. قدرات قريبة في العائلة

- `DRAW-P01` قصة الخط الواحد المستمر حتى الشعار / Continuous-line logo story (one stroke → three beats → wordmark loop) (documented)
- `DRAW-U01` فيلم يد مرسومة حتمي بـmake_frame(t) / Deterministic hand-drawn film via make_frame(t) (documented)

