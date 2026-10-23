# `characters-rigs` — الموشن والمونتاج والسينما (51 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/characters-rigs.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/motion.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`CHAR-01` ورقة تصميم الشخصية واختبار الظل](#char-01--ورقة-تصميم-الشخصية-واختبار-الظل--model-sheet--silhouette-test)
- [`CHAR-02` وصفة اللطافة](#char-02--وصفة-اللطافة--cute-character-recipe)
- [`CHAR-03` أقفال الهوية النصية](#char-03--أقفال-الهوية-النصية--identity-lock-text-chrloc-sheets)
- [`CHAR-04` قفل الشخصية النفسي](#char-04--قفل-الشخصية-النفسي--personality-lock)
- [`CHAR-05` بايبلات شخصيات fastify](#char-05--بايبلات-شخصيات-fastify--fastify-character-bibles--reference-locks)
- [`CHAR-06` ثبات الشخصية في التوليد بالمراجع](#char-06--ثبات-الشخصية-في-التوليد-بالمراجع--reference-based-consistency-in-generators)
- [`CHAR-07` شريط حركة كامل من إطار واحد](#char-07--شريط-حركة-كامل-من-إطار-واحد--whole-strip-sprite-from-one-seed-frame)
- [`CHAR-08` الأفاتار الناطق](#char-08--الأفاتار-الناطق--ai-talking-avatars)
- [`CHAR-09` شخصية ذكاء اصطناعي بالحالات](#char-09--شخصية-ذكاء-اصطناعي-بالحالات--stateful-ai-persona-orb)
- [`CHAR-10` هيكل SVG بنقاط دوران](#char-10--هيكل-svg-بنقاط-دوران--svg-cut-out-rig-with-pivots)
- [`CHAR-11` أطراف بـ IK بعظمتين](#char-11--أطراف-بـ-ik-بعظمتين--two-bone-ik-limbs)
- [`CHAR-12` انحناء الجسم والمط حسب السرعة](#char-12--انحناء-الجسم-والمط-حسب-السرعة--velocity-driven-body-bend--squash)
- [`CHAR-13` وجوه بتبديل الأشكال](#char-13--وجوه-بتبديل-الأشكال--swap-shape-faces-mouths--expressions)
- [`CHAR-14` شخصية قصاصات بمؤشر اتجاه](#char-14--شخصية-قصاصات-بمؤشر-اتجاه--cut-out-rig-with-facing-dial)
- [`CHAR-15` الشخصية في إطارها المحلي](#char-15--الشخصية-في-إطارها-المحلي--character-built-in-its-own-local-frame)
- [`CHAR-16` أدوات تفاصيل المخلوقات](#char-16--أدوات-تفاصيل-المخلوقات--creature-detail-builders)
- [`CHAR-17` الرجل العصوي الكوميدي](#char-17--الرجل-العصوي-الكوميدي--stickman-comic-style)
- [`CHAR-18` تحريك رسمة واحدة بعظام](#char-18--تحريك-رسمة-واحدة-بعظام--2d-mesh-bone-rig-from-one-image)
- [`CHAR-19` أشياء بوجوه وتمائم](#char-19--أشياء-بوجوه-وتمائم--object-as-character-faces--mascots)
- [`CHAR-20` مسرح شخصية بديكور واحد](#char-20--مسرح-شخصية-بديكور-واحد--single-set-character-stage)
- [`CHAR-21` شخصيات ظلية مسطحة](#char-21--شخصيات-ظلية-مسطحة--flat-silhouette-characters)
- [`CHAR-22` تمائم البكسل والسبرايت](#char-22--تمائم-البكسل-والسبرايت--pixel--sprite-mascots)
- [`CHAR-23` تحولات الشخصية](#char-23--تحولات-الشخصية--character-transformations--variants)
- [`CHAR-24` دورة المشي بلا انزلاق](#char-24--دورة-المشي-بلا-انزلاق--walk-cycle-without-foot-sliding)
- [`CHAR-25` ساق مشي إجرائية](#char-25--ساق-مشي-إجرائية--procedural-walk-cycle-leg)
- [`CHAR-26` آلة حالات الوضعية](#char-26--آلة-حالات-الوضعية--keyframed-pose-state-machine)
- [`CHAR-27` مولد المشي للسبرايت](#char-27--مولد-المشي-للسبرايت--procedural-sprite-walk-generator)
- [`CHAR-28` الوضعيات المفتاحية أولًا](#char-28--الوضعيات-المفتاحية-أولًا--pose-to-pose-blocking)
- [`CHAR-29` لحظة رد الفعل والقفزة](#char-29--لحظة-رد-الفعل-والقفزة--reaction--jump-recipe)
- [`CHAR-30` الإشارة والكشف](#char-30--الإشارة-والكشف--point-and-reveal)
- [`CHAR-31` الحديث للكاميرا](#char-31--الحديث-للكاميرا--talk-to-camera-behaviours)
- [`CHAR-32` ظهور التمائم وقفزاتها](#char-32--ظهور-التمائم-وقفزاتها--mascot-pop-ins--hop-arcs)
- [`CHAR-33` لمسات تمثيل](#char-33--لمسات-تمثيل--acting-accents-celebrate-sleep-run)
- [`CHAR-34` مبادئ التحريك للهياكل](#char-34--مبادئ-التحريك-للهياكل--animation-principles-for-rigs)
- [`CHAR-35` الشخصية العربية وفقاعة كلامها](#char-35--الشخصية-العربية-وفقاعة-كلامها--rtl-staging--arabic-speech-bubble)
- [`CHAR-36` حياة الخمول](#char-36--حياة-الخمول--idle-life-breath-blink-glances)
- [`CHAR-37` حركة ثانوية بالنوابض والسلاسل](#char-37--حركة-ثانوية-بالنوابض-والسلاسل--spring--chain-secondary-motion)
- [`CHAR-38` فراشة ويراعة مرافقة](#char-38--فراشة-ويراعة-مرافقة--winged-companions-butterfly-firefly)
- [`CHAR-39` سرب طيور](#char-39--سرب-طيور--flock-of-birds)
- [`CHAR-40` الأرنب القطيفة المنحوت](#char-40--الأرنب-القطيفة-المنحوت--sdf-plush-bunny-rigged)
- [`CHAR-41` عيون لامعة وعيون برمش](#char-41--عيون-لامعة-وعيون-برمش--glossy--blinking-eyes)
- [`CHAR-42` أرنب وأسد المختبر](#char-42--أرنب-وأسد-المختبر--lab-rabbit--lion-characters)
- [`CHAR-43` سمكة كوي إجرائية](#char-43--سمكة-كوي-إجرائية--procedural-koi)
- [`CHAR-44` شخصيات من أشكال أولية](#char-44--شخصيات-من-أشكال-أولية--primitive-toon-figures)
- [`CHAR-45` دوران 360 لورقة الشخصية](#char-45--دوران-360-لورقة-الشخصية--turntable-character-sheet)
- [`CHAR-46` جسد من الجسيمات بحركة حقيقية](#char-46--جسد-من-الجسيمات-بحركة-حقيقية--particle-body-from-real-motion-mocap)
- [`CHAR-47` تمثيل الشخصيات بلوتي](#char-47--تمثيل-الشخصيات-بلوتي--lottie-character-acting)
- [`CHAR-48` لوحات الكوميكس](#char-48--لوحات-الكوميكس--comics-panels)
- [`CHAR-49` أنمي أكشن](#char-49--أنمي-أكشن--anime-action)
- [`CHAR-50` صفحات ويبتون بشخصيات حيوانية](#char-50--صفحات-ويبتون-بشخصيات-حيوانية--webtoon-pages-with-arabic-overlay)
- [`CHAR-X01` شخصيات حية ببصمات حركة](#char-x01--شخصيات-حية-ببصمات-حركة--alive-characters-personality-motion-signatures)

## البطاقات / cards

### `CHAR-01` — ورقة تصميم الشخصية واختبار الظل / Model sheet & silhouette test

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اكتب النسب واللوحة وسماكة الخط والزوايا قبل التحريك، وكل وضعية مفتاحية يجب أن تُقرأ كظل أسود مصمت. / Lock proportions, palette, line weight and views before animating; every key pose must read as a solid black shape.

**متى:** قبل أول إطار لأي شخصية متكررة / before the first frame of any recurring character.

**كيف:** STYLE.md: 3–5 colours, outline weight and colour, views front / side / three-quarter (+ rear and the in-video camera view) on one ground line and scale, 3–5 key expressions; one canonical spec per character kept apart from style skills (silhouette, fixed features, proportions, default palette, e.g. whale mascot #FFFFFF belly, #D9D9D9 back, #F0F0F0 cheek, #1A1A1A outline); build the SVG rig with grouped parts and pivots so every video reuses the same character; fill the pose with black to check readability.

**المعاملات:** 3–5 colours; 3–5 views

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** model sheet · silhouette · turnaround · ورقة الشخصية · mascot bible

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/characters.md:15`
- `kosif-atlas/skills/1094-akbun-draw/2427-akbun-mascot-whale/SKILL.md`
- `kosif-atlas/skills/1526-gamegen/4166-game-concept-art/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-02` وصفة اللطافة / Cute character recipe (documented)
- `CHAR-03` أقفال الهوية النصية / Identity lock text (CHR/LOC sheets) (documented)

### `CHAR-02` — وصفة اللطافة / Cute character recipe

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نسب وقواعد شكل جعلت الأرنب يُقرأ لطيفًا: الرأس أعرض من الجسم، عيون منخفضة متباعدة، خدود، أنف صغير، أطراف قصيرة، باستيل مع لون تأكيد واحد. / Proportion and look rules that made the bunny read as cute.

**متى:** أي تميمة أو شخصية أطفال / any mascot or kids' character.

**كيف:** head width ≥ body (.16 vs .14); eyes at ~45% of head height, spacing 0.4 × head width, tall 1.12, two catch-lights; cheeks k ≈ .02; nose ≤ 1/8 head width; soft blends 10–30 mm; short limbs, big feet; pastel + one accent; warm key front-left-top with mint + pink rims, neutral tone curve, bloom threshold ≥ .9; alive acting: breathing ±0.6%, blinks, ear flop.

**المعاملات:** head .16 vs torso .14; eyes 45% / 0.4×

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cute · kawaii · proportions · لطيف · mascot

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/references/shape-kit.md`
- `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-01` ورقة تصميم الشخصية واختبار الظل / Model sheet & silhouette test (documented)
- `CHAR-03` أقفال الهوية النصية / Identity lock text (CHR/LOC sheets) (documented)
- `CHAR-04` قفل الشخصية النفسي / Personality lock (documented)

### `CHAR-03` — أقفال الهوية النصية / Identity lock text (CHR/LOC sheets)

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فقرة قفل واحدة لكل شخصية ومكان تُلصق حرفيًا في كل وصف لاحق، مع صحائف 360° للزوايا والتعابير. / One lock paragraph per character and location pasted verbatim into every later prompt, with 360° sheets.

**متى:** أي سلسلة مشاهد مولدة لنفس الشخصية / any generated series with a recurring character.

**كيف:** CHR-001: name · age · skin tone · face shape · eyes · brows · nose · lips · hair · build/height · signature outfit · accessories · marks · MUST NOT CHANGE: …; views front, 3/4 left, profile, back, full-body contrapposto; expressions neutral, joy, anger, fear, determination; LOC-001: era, scale, left/right/centre landmarks, time-of-day variants. Models have no memory: copy the CHARACTER sentence byte-for-byte, keep background tone and the 3–5 colour palette identical, vary only the SCENE line. identity_reference.py checks 5 views (front, left, right, back, three_quarter).

**المعاملات:** 5 views; 5 expressions

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** character lock · continuity · CHR · identity · قفل الشخصية

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/continuity-protocols.md`
- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`
- `100-superskills/skills/kosif-montage-motion/references/continuity-protocols.md`
- `kosif-atlas/skills/2976-pwdev-social-media/12595-visual-consistency`

#### 7. قدرات قريبة في العائلة

- `CHAR-01` ورقة تصميم الشخصية واختبار الظل / Model sheet & silhouette test (documented)
- `CHAR-02` وصفة اللطافة / Cute character recipe (documented)
- `CHAR-04` قفل الشخصية النفسي / Personality lock (documented)
- `CHAR-05` بايبلات شخصيات fastify / Fastify character bibles & reference locks (proven)

### `CHAR-04` — قفل الشخصية النفسي / Personality lock

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحويل سمات شخصية خيالية إلى وقفة ونظرة وملبس ثابتة حتى يبقى تمثيلها متسقًا عبر اللقطات. / Map a fictional character's personality facets to posture, gaze and styling cues.

**متى:** شخصيات قصصية بأكثر من مشهد / story characters across scenes.

**كيف:** pick 4–6 Big-Five facets and map to cues (assertive: squared shoulders, direct gaze, centre frame; anxious: guarded arms, off-camera glance, tense jaw; ordered: pressed clothes, symmetrical workspace…); add 3 if-then behaviour signatures and the driving need (autonomy / competence / relatedness). Fictional characters only.

**المعاملات:** 4–6 facets; 3 if-then rules

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** personality · acting · posture · gaze · شخصية نفسية

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/character-psychology.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-02` وصفة اللطافة / Cute character recipe (documented)
- `CHAR-03` أقفال الهوية النصية / Identity lock text (CHR/LOC sheets) (documented)
- `CHAR-05` بايبلات شخصيات fastify / Fastify character bibles & reference locks (proven)
- `CHAR-06` ثبات الشخصية في التوليد بالمراجع / Reference-based consistency in generators (key)

### `CHAR-05` — بايبلات شخصيات fastify / Fastify character bibles & reference locks

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مواصفات ثابتة مختبرة تُلصق في كل وصف: رجل عصوي أصلي، شخصيتان أصليتان ثلاثيتا الأبعاد، ورياضي بلا وجه / مع قفل الصورة المرجعية للمستخدم. — Tested fixed specs pasted into every prompt, plus the user's reference-image lock.

**متى:** ملفات الإنتاج المرحلية stickman / character-romance / fitness / the staged production profiles.

**كيف:** Stickman BIBLE: charcoal-black 5 px brush strokes at 1080 px width, circular head = 1/4 of height, slim straight torso, single-line limbs each half a torso long, two dot eyes + one mouth stroke, tiny teal scarf at the left of the neck, palette black/teal + one muted warm accent. If the user has their own figure, prompts reference the attached image unchanged and text-only tools are refused (referenceTool 'text-only' throws). Romance: A = young woman (warm brown skin, curly dark shoulder hair with pale-blue ribbon, emerald jacket, cream boots), B = waist-high doll (porcelain face, lilac bob, coral/turquoise patchwork, amber buttons, teal boots) in all 10 prompts. Fitness: faceless muscular sculpt-render, black cap and shorts, dark gym, one overhead teal-blue rim light, shallow DOF. Profile tests 15/15 passed here.

**المعاملات:** stroke 5 px @1080; head 25% height; limb 0.5 torso

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** character bible · stickman · reference lock · fastify · بايبل

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/scripts/profiles/stickman.mjs`
- `fastify-motion-bro/scripts/profiles/character-romance.mjs`
- `fastify-motion-bro/scripts/profiles/fitness.mjs`
- `fastify-motion-bro/tests/production-profiles.test.mjs`

#### 7. قدرات قريبة في العائلة

- `CHAR-03` أقفال الهوية النصية / Identity lock text (CHR/LOC sheets) (documented)
- `CHAR-04` قفل الشخصية النفسي / Personality lock (documented)
- `CHAR-06` ثبات الشخصية في التوليد بالمراجع / Reference-based consistency in generators (key)
- `CHAR-07` شريط حركة كامل من إطار واحد / Whole-strip sprite from one seed frame (key)

### `CHAR-06` — ثبات الشخصية في التوليد بالمراجع / Reference-based consistency in generators

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مراجع متعددة مسماة لكل شخصية، تعديل صورة الأفاتار الموجودة بدل توليد شخص جديد، وIP-Adapter لنقل الهوية أو الأسلوب، وأوراق الشخصيات كمراسٍ قبل الفيديو. / Named multi-reference inputs, editing the supplied avatar, IP-Adapter conditioning and character sheets as anchors.

**متى:** حين يملك المستخدم مفتاح خدمة صور/فيديو / when the user has an image/video service.

**كيف:** 4–5 references per character from different angles, labelled ('Character A: the red-haired knight'), repeat 2–3 identifiers every turn; when the setting does not change say 'Edit @Image1: …' keeping face/hair/light; ComfyUI IPAdapterAdvanced weight 0.55–0.65 for characters (> 0.75 copies pose, < 0.4 drifts), FaceID 0.7–0.85, plus ControlNet for pose; one image call per sheet (front, 3/4, profile on plain ground with one telling prop) — redo off-style sheets before animating (an image costs cents, a clip dollars). Needs Gemini/OpenAI image API keys, or a GPU ComfyUI host.

**المعاملات:** 4–5 refs; IPA 0.55–0.65; FaceID 0.7–0.85

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** consistency · IP-Adapter · references · avatar edit · ثبات

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2173-tools-plugin/7917-generate-image`
- `kosif-atlas/skills/259-quickdesign/865-quickdesign`
- `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`
- `kosif-atlas/skills/1511-homie/3889-art`

#### 7. قدرات قريبة في العائلة

- `CHAR-04` قفل الشخصية النفسي / Personality lock (documented)
- `CHAR-05` بايبلات شخصيات fastify / Fastify character bibles & reference locks (proven)
- `CHAR-07` شريط حركة كامل من إطار واحد / Whole-strip sprite from one seed frame (key)
- `CHAR-08` الأفاتار الناطق / AI talking avatars (key)

### `CHAR-07` — شريط حركة كامل من إطار واحد / Whole-strip sprite from one seed frame

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ولّد شريط حركة التميمة كاملًا في طلب تعديل واحد حول إطار معتمد، لأن التوليد إطارًا إطارًا ينجرف. / Generate the whole animation strip in one edit request around an approved frame.

**متى:** سبرايتات ألعاب أو تميمة بكسل / game sprites, pixel mascots.

**كيف:** place the seed on a transparent 1024 canvas with 4 slots of 256; prompt invariants (same character, facing, palette, silhouette, outfit, transparent background, exact frame count, no scenery); normalise to fixed frames (e.g. 64 px) with one shared scale and bottom-centre anchor; optionally lock frame 1 to the seed; review a preview sheet. Needs an image-edit model key.

**المعاملات:** 1024 canvas; 4 × 256 slots; 64 px frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sprite strip · seed frame · pixel mascot · سبرايت

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2696-game-studio/10368-sprite-pipeline`

#### 7. قدرات قريبة في العائلة

- `CHAR-05` بايبلات شخصيات fastify / Fastify character bibles & reference locks (proven)
- `CHAR-06` ثبات الشخصية في التوليد بالمراجع / Reference-based consistency in generators (key)
- `CHAR-08` الأفاتار الناطق / AI talking avatars (key)
- `CHAR-09` شخصية ذكاء اصطناعي بالحالات / Stateful AI persona orb (install)

### `CHAR-08` — الأفاتار الناطق / AI talking avatars

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فيديو مقدّم بمزامنة شفاه من نص دون تصوير، ثم يُركّب تحت رسوم متحركة مكتوبة بالكود. / Script-driven lip-synced presenters composited under coded motion graphics.

**متى:** مقدم بلا تصوير / a presenter without filming.

**كيف:** HeyGen (MCP/API: script, avatar, language; 230+ avatars, 140+ languages; personal twin from a 2–5 min recording) or Synthesia for full-body corporate presenters; keep the presenter clip as project media and lay editable scenes and Arabic captions on top. Needs a HeyGen/Synthesia account key; check Arabic lip-sync on a still before committing.

**المعاملات:** twin from 2–5 min video

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** avatar · HeyGen · Synthesia · presenter · lip sync · أفاتار

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1446-marketing-skills/3531-video`
- `kosif-one/vendor/hyperframes/docs/guides/avatar-presenter.mdx`

#### 7. قدرات قريبة في العائلة

- `CHAR-06` ثبات الشخصية في التوليد بالمراجع / Reference-based consistency in generators (key)
- `CHAR-07` شريط حركة كامل من إطار واحد / Whole-strip sprite from one seed frame (key)
- `CHAR-09` شخصية ذكاء اصطناعي بالحالات / Stateful AI persona orb (install)
- `CHAR-10` هيكل SVG بنقاط دوران / SVG cut-out rig with pivots (ready)

### `CHAR-09` — شخصية ذكاء اصطناعي بالحالات / Stateful AI persona orb

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مقدم على شكل كرة بخمس حالات: سكون، استماع، تفكير، كلام، نوم / تقودها حالة الصوت. — A narrator orb with five states driven by audio state.

**متى:** شرح منتجات الذكاء الاصطناعي / AI product explainers.

**كيف:** Vercel ai-elements Persona (Rive WebGL2) via npx ai-elements add persona; local stand-in with no install: SVG/CSS state classes switched from words.json speaking segments (speaking while a word is active, thinking in gaps > 0.7 s, idle otherwise), rendered with render_html.cjs.

**المعاملات:** 5 states

**التثبيت:** npx ai-elements add persona

**الوسوم:** persona · AI orb · states · speaking · شخصية ذكاء

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2722-vercel/10522-ai-elements/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-07` شريط حركة كامل من إطار واحد / Whole-strip sprite from one seed frame (key)
- `CHAR-08` الأفاتار الناطق / AI talking avatars (key)
- `CHAR-10` هيكل SVG بنقاط دوران / SVG cut-out rig with pivots (ready)
- `CHAR-11` أطراف بـ IK بعظمتين / Two-bone IK limbs (proven)

### `CHAR-10` — هيكل SVG بنقاط دوران / SVG cut-out rig with pivots

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مجموعات SVG منفصلة لكل طرف بنقاط دوران صريحة ودورانات متداخلة، والكوع يتأخر إطارين ليصنع المتابعة. / Separate SVG groups per limb with explicit pivots and nested rotations; the elbow lags 2 frames.

**متى:** أي شخصية مسطحة تتحرك / any flat character.

**كيف:** python3 tools/kosif.py scaffold character-rig <dir>; parts head, torso, upper/lower arm, hand, upper/lower leg, foot; transform rotate(θ px py) in nested <g>; Remotion arm: shoulder interpolate(frame, [0,6,14,24], [0,8,−55,−48]), elbow ([2,10,18,26] → [0,5,−30,−24]) with Easing.inOut(Easing.sin); walk 12 frames/step at 24 fps; 5–7 mouth shapes; moving hold 1–2%.

**المعاملات:** elbow +2 f; 12 f/step

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** rig · pivots · cut-out · SVG · هيكل · مفاصل

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/characters.md:54`
- `kosif-tool/styles/character-rig/SKILL.md`
- `100-superskills/skills/character-animation-2d/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-08` الأفاتار الناطق / AI talking avatars (key)
- `CHAR-09` شخصية ذكاء اصطناعي بالحالات / Stateful AI persona orb (install)
- `CHAR-11` أطراف بـ IK بعظمتين / Two-bone IK limbs (proven)
- `CHAR-12` انحناء الجسم والمط حسب السرعة / Velocity-driven body bend & squash (seen)

### `CHAR-11` — أطراف بـ IK بعظمتين / Two-bone IK limbs

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تُعطى الوركَ وأهداف اليدين والقدمين في العالم، فيُحل الكوع والركبة بـ IK بعظمتين، ويُرسم الطرف منحنى يمر بالمفصل. / Give hip and world targets; solve elbow/knee with 2-bone IK and draw each limb as a curve through the joint.

**متى:** رجل عصوي، دراجة بدواسات، شخصية تمسك أشياء / stickmen, pedalling, grabbing.

**كيف:** bend direction from facing (elbows back, knees forward); quadratic control point = 2J − (S + E)/2 so the curve passes through the joint J; stroke ~3 px round caps. Bicycle: crank θ = ω·t (ω ≈ 2π·1 Hz), pedals at θ and θ + π, legs solved hip → pedal, wheels at gear ratio ~2.5 × ω, wheel radius 0.33 m. Proof film character-rig (rendered and verified here, 13/13) uses law-of-cosines ik() for legs and arms: thigh and shin 116 px each, upper arm 84 px, forearm 80 px, knees bend forward and elbows back; open index.html?bones=1 to see the bones. (code snippet in references/powers/characters-rigs.md)

**المعاملات:** ω ≈ 2π rad/s; gear 2.5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** IK · two-bone · limbs · stickman · bicycle · حركة عكسية

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/character-rig/README.md`
- `kosif-tool/styles/stickman`
- `kosif-tool/styles/pm-axtonliu-0b861d`

#### 7. قدرات قريبة في العائلة

- `CHAR-09` شخصية ذكاء اصطناعي بالحالات / Stateful AI persona orb (install)
- `CHAR-10` هيكل SVG بنقاط دوران / SVG cut-out rig with pivots (ready)
- `CHAR-12` انحناء الجسم والمط حسب السرعة / Velocity-driven body bend & squash (seen)
- `CHAR-13` وجوه بتبديل الأشكال / Swap-shape faces, mouths & expressions (proven)

### `CHAR-12` — انحناء الجسم والمط حسب السرعة / Velocity-driven body bend & squash

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الجذع أنبوب منحنٍ يُرسم مرتين، انحناؤه من سرعة الميل، ومطه وضغطه من سرعة الورك وصدمات الهبوط، والرأس يتأخر قليلًا. / Torso as a bent tube; bend from tilt velocity, squash/stretch from hip velocity and landings; head lags.

**متى:** شخصيات خطية مرنة كوميدية / rubbery comic characters.

**كيف:** torso = quadratic bezier hip → neck drawn wide black then thinner white on top (~38 px); bend = k·d(tilt)/dt computed from seek(t) and seek(t − 1/fps) (never accumulated); stretch/squash 0.85–1.15 from vertical hip velocity plus landing impulses; head follows 1–2 frames late.

**المعاملات:** tube ~38 px; squash 0.85–1.15

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** body bend · squash · velocity · rubbery · مط

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/stickman`

#### 7. قدرات قريبة في العائلة

- `CHAR-10` هيكل SVG بنقاط دوران / SVG cut-out rig with pivots (ready)
- `CHAR-11` أطراف بـ IK بعظمتين / Two-bone IK limbs (proven)
- `CHAR-13` وجوه بتبديل الأشكال / Swap-shape faces, mouths & expressions (proven)
- `CHAR-14` شخصية قصاصات بمؤشر اتجاه / Cut-out rig with facing dial (seen)

### `CHAR-13` — وجوه بتبديل الأشكال / Swap-shape faces, mouths & expressions

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** العيون والفم أشكال تُبدَّل لا مسارات تُشوَّه: 5–7 أفواه، فم مغلق على م/ب، رمش، حواجب بزاوية لكل عاطفة. / Eyes and mouth are swapped shapes, not distorted paths.

**متى:** كل شخصية تتكلم أو تتفاعل / every talking or reacting character.

**كيف:** mouth index from phoneme/word timing (words.json), switch within 1 frame, closed on M/B/P (م ب ف in Arabic); eyes as dots blinking scaleY → 0.1 for 80 ms every 2.5–4 s; brows as short strokes angled per emotion; mouth per emotion (smile, flat, O + sweat drop, grit, content); up to 8 expression states (dots, ^ ^ joy, angry brows, hearts, wink + tongue) swapped on beats with a 6 px bounce, sweat-drop and sparkle overlays; screen-face robots swap glyph eyes per emotion. Proven in character-rig: neutral → surprised → determined → happy → talking, each swap with a head-scale pulse 1 + 0.07·e^(−14τ)·cos(30τ), 3 blinks, mouth opening on each word's timing (open/close only — no visemes).

**المعاملات:** 5–7 mouths; switch ≤1 f; blink 80 ms / 2.5–4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lip flap · mouth shapes · expressions · blink · وجه · تعابير

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/character-rig/README.md`
- `kosif-tool/playbooks/characters.md:18`
- `kosif-tool/styles/stickman`
- `kosif-tool/styles/pm-jake11moran-a269c4`

#### 7. قدرات قريبة في العائلة

- `CHAR-11` أطراف بـ IK بعظمتين / Two-bone IK limbs (proven)
- `CHAR-12` انحناء الجسم والمط حسب السرعة / Velocity-driven body bend & squash (seen)
- `CHAR-14` شخصية قصاصات بمؤشر اتجاه / Cut-out rig with facing dial (seen)
- `CHAR-15` الشخصية في إطارها المحلي / Character built in its own local frame (proven)

### `CHAR-14` — شخصية قصاصات بمؤشر اتجاه / Cut-out rig with facing dial

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قيمة اتجاه واحدة من −1 إلى 1 تزيح ملامح الوجه وتبدّل الذراع القريبة والبعيدة، وطور المشي مشتق من المسافة المقطوعة فلا تنزلق القدمان. / One facing value shifts features and swaps near/far arm; walk phase from distance so feet never slide.

**متى:** دودل وقصص بشخصية تتجول / doodle stories with a walking character.

**كيف:** parts head, near/far arm, legs, body around pivots; phase = distance / stepLength (~40 px) so speed changes never slide feet; arm swing ±20°, head bob 2–3 px; at facing 0 show both eyes centred.

**المعاملات:** step ~40 px; arm ±20°; bob 2–3 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** facing · cut-out · no foot sliding · doodle · قصاصات

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/doodle`

#### 7. قدرات قريبة في العائلة

- `CHAR-12` انحناء الجسم والمط حسب السرعة / Velocity-driven body bend & squash (seen)
- `CHAR-13` وجوه بتبديل الأشكال / Swap-shape faces, mouths & expressions (proven)
- `CHAR-15` الشخصية في إطارها المحلي / Character built in its own local frame (proven)
- `CHAR-16` أدوات تفاصيل المخلوقات / Creature detail builders (ready)

### `CHAR-15` — الشخصية في إطارها المحلي / Character built in its own local frame

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ارسم الجسم حول أصله الخاص (قدميه أو رأسه) ثم ضعه وأدره وكبّره كمجموعة واحدة، فيسهل إعادة وضعه وتحريكه. / Design a body around its own origin, then place/rotate/scale it as one group.

**متى:** كل شخصية تُعاد في لقطات مختلفة / every character reused across shots.

**كيف:** SVG: collect parts then wrap <g transform="translate(560 392) rotate(-16) scale(1.3)"> with a blurred warm rim-glow ellipse behind (#fb923c rx 80 ry 54 at .55); Pillow scenes: whale W(x,y)/WS(shape) rotate along HEAD (700,290) → TAIL (1200,760); dragon girl xf() scales 1.4× around her feet (380,619). The whale scene passes the studio judge gate (test run here).

**المعاملات:** translate/rotate/scale as one group

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** local coordinates · group transform · re-pose · إطار محلي

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/duck-vs-dragon/duck_dragon.py`
- `kosif-studio/scenes/whale_dragon.py:46`
- `kosif-studio/scenes/dragon_girl.py:288`
- `kosif-studio/tests/test_studio.py:227`

#### 7. قدرات قريبة في العائلة

- `CHAR-13` وجوه بتبديل الأشكال / Swap-shape faces, mouths & expressions (proven)
- `CHAR-14` شخصية قصاصات بمؤشر اتجاه / Cut-out rig with facing dial (seen)
- `CHAR-16` أدوات تفاصيل المخلوقات / Creature detail builders (ready)
- `CHAR-17` الرجل العصوي الكوميدي / Stickman comic style (ready)

### `CHAR-16` — أدوات تفاصيل المخلوقات / Creature detail builders

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جناح خفاش من عظام وغشاء متدلٍّ بين الأطراف، أشواك ظهر، صفائح بطن، وريشة منحنية / تشريح فوري للتنانين والطيور. — Bat wing, dorsal spikes, belly plates and feather leaves.

**متى:** تنانين، طيور، كائنات خيالية / dragons, birds, fantasy creatures.

**كيف:** wing(shoulder, elbow, wrist, tips, attach, sag=0.28) → (membrane, bones, veins): bone tubes 8/6/4.5, fingers 3.4 → 0.7, scallops of 12 samples, wrist claw; spikes(spine, radii, every, size) with height (4 + r·.45)·size; belly_plates(spine, radii) ribbed every 4th sample; leaf(base, tip, width, bend, n=10) for each feather of a spread wing.

**المعاملات:** sag 0.28; scallop 12

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dragon · wing · spikes · feathers · تنين · مخلوقات

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/scenes/dragon_girl.py:88`
- `kosif-studio/scenes/dragon_girl.py:46`
- `kosif-studio/scenes/duck_dragon.py:34`
- `100-superskills/skills/pixel-studio-painter/scripts/scenes/dragon_girl.py`

#### 7. قدرات قريبة في العائلة

- `CHAR-14` شخصية قصاصات بمؤشر اتجاه / Cut-out rig with facing dial (seen)
- `CHAR-15` الشخصية في إطارها المحلي / Character built in its own local frame (proven)
- `CHAR-17` الرجل العصوي الكوميدي / Stickman comic style (ready)
- `CHAR-18` تحريك رسمة واحدة بعظام / 2D mesh bone rig from one image (seen)

### `CHAR-17` — الرجل العصوي الكوميدي / Stickman comic style

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رجل عصوي مرن، بطاقات تسقط وتتكدس، وضربة كوميدية لنصيحة بمفارقة. / A flexible stick figure, cards that drop and stack, a comic beat with a twist.

**متى:** نصائح ومواقف ساخرة / tips and comic situations.

**كيف:** python3 tools/kosif.py scaffold stickman <dir> (SVG line rig with pivots, arcs, squash; on twos optional). Basma STY.stickman: 16:9, bright, 2.1 wps, Readex Pro, bg #FBF9F4, ink #1F2328, accent #F2C94C, floor #EFEAE0, colours #EB5757 / #F2C94C / #5B8DEF / #9B51E0 / #27AE60; sfx pop/hit/tick/shimmer; question lines end with ؟. style:stickman: pose keys with Easing.inOut(cubic) + procedural layers (breath 0.3 Hz 2 px, thumb scroll, leg kicks, 2-step walk); card flies to hand, flips at mid (250 ms), thrown 500 ms with ghosts, box squash, counter +1.

**المعاملات:** 2.1 wps; breath 0.3 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stickman · رجل عصوي · comic · cards · tips

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/stickman/SKILL.md`
- `app/public/js/10_studio.js:504`
- `kosif-tool/styles/stickman`

#### 7. قدرات قريبة في العائلة

- `CHAR-15` الشخصية في إطارها المحلي / Character built in its own local frame (proven)
- `CHAR-16` أدوات تفاصيل المخلوقات / Creature detail builders (ready)
- `CHAR-18` تحريك رسمة واحدة بعظام / 2D mesh bone rig from one image (seen)
- `CHAR-19` أشياء بوجوه وتمائم / Object-as-character faces & mascots (seen)

### `CHAR-18` — تحريك رسمة واحدة بعظام / 2D mesh bone rig from one image

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تُقسم الرسمة إلى أجزاء وتُشوَّه شبكتها بنحو 16 عظمة، مع دورات رقص جيبية على الإيقاع. / Split an illustration into parts and deform its mesh with ~16 bones, sine dance cycles on the beat.

**متى:** تحريك رسمة المستخدم أو شخصية ثابتة / animating a user's drawing.

**كيف:** parts on separate layers with pivots; per-bone rotation = A·sin(2π·(BPM/60)·t + φ) (150 BPM in the reference); mesh deform via a skinned plane (three.js SkinnedMesh or PIXI mesh) or per-part rotation if the drawing is flat; keep amplitudes small at joints to avoid tearing.

**المعاملات:** ~16 bones; 150 BPM

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mesh deform · bones · dance · puppet · عظام

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:p5` ← npm ls p5 أو وجود node_modules/p5
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-topi-003-b0e12c`

#### 7. قدرات قريبة في العائلة

- `CHAR-16` أدوات تفاصيل المخلوقات / Creature detail builders (ready)
- `CHAR-17` الرجل العصوي الكوميدي / Stickman comic style (ready)
- `CHAR-19` أشياء بوجوه وتمائم / Object-as-character faces & mascots (seen)
- `CHAR-20` مسرح شخصية بديكور واحد / Single-set character stage (seen)

### `CHAR-19` — أشياء بوجوه وتمائم / Object-as-character faces & mascots

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حوّل أي شيء إلى شخصية بعينين لامعتين وحاجبين: بلاطة، كرة، فقاعة كلام، كتلة شوكية / مع رمش وانضغاط وتمايل. — Turn any object into a character with glossy eyes and brows.

**متى:** تمائم العلامات، شرح ودود / brand mascots, friendly explainers.

**كيف:** two glossy black spheres (metalness .6, roughness .15, radius ~8% of the tile width) slightly protruding + capsule brows animated in y/rotation; blink scaleY 100 ms every 2–4 s; egg sphere scale (1, 1.25, 1) with emissive orange and a headlamp point light, landing squash y .75 for 80 ms; speech-bubble blob with kawaii eyes, blush, bounce 1.1/0.9; spiky SVG blob idle wobble ±4° and scale .97–1.03 in a 1.2 s loop, 8–15% of frame, hopping between corners and reacting; googly eyes on everyday props.

**المعاملات:** eye r ~8% tile; blink 100 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mascot · googly eyes · object character · تميمة

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-anilraok-eff262`
- `kosif-tool/styles/pm-gorden-sun-041f56`
- `kosif-tool/styles/pm-anthonyriera-9b1b2a`
- `kosif-tool/styles/pm-anas0ra-e57aea`

#### 7. قدرات قريبة في العائلة

- `CHAR-17` الرجل العصوي الكوميدي / Stickman comic style (ready)
- `CHAR-18` تحريك رسمة واحدة بعظام / 2D mesh bone rig from one image (seen)
- `CHAR-20` مسرح شخصية بديكور واحد / Single-set character stage (seen)
- `CHAR-21` شخصيات ظلية مسطحة / Flat silhouette characters (seen)

### `CHAR-20` — مسرح شخصية بديكور واحد / Single-set character stage

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** غرفة واحدة مرسومة كطبقات SVG، والشخصية بين ظهر المكتب وواجهته فتختفي ذراعاها خلفه طبيعيًا. / One illustrated room as SVG layers with the character between desk back and desk front.

**متى:** سلسلة حلقات بنفس المكان / episodic series in one place.

**كيف:** ~6 layers (wall, window, props, desk back, character, desk front); character pivot at the desk line; characters on twos while UI elements stay smooth — never mix the two cadences on one element (steps(12) per second).

**المعاملات:** ~6 layers; 2-frame holds

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** set · stage · layers · desk · ديكور

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-jake11moran-a269c4`
- `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-18` تحريك رسمة واحدة بعظام / 2D mesh bone rig from one image (seen)
- `CHAR-19` أشياء بوجوه وتمائم / Object-as-character faces & mascots (seen)
- `CHAR-21` شخصيات ظلية مسطحة / Flat silhouette characters (seen)
- `CHAR-22` تمائم البكسل والسبرايت / Pixel & sprite mascots (seen)

### `CHAR-21` — شخصيات ظلية مسطحة / Flat silhouette characters

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شخصية بتعبئة داكنة واحدة ومفصلين أو ثلاثة، تُقرأ بالمحيط فقط أمام خلفية مضيئة. / A single dark-fill character with 2–3 joints, read only by outline.

**متى:** قصص هادئة وأجواء ليلية / quiet stories, night moods.

**كيف:** fill ~#0d0c0b, no internal detail, side profile (cap, long coat); walk 12 frames per step at 24 fps cadence; galloping silhouettes loop over speed lines; glowing stroke figures (lime with blur glow) for logos.

**المعاملات:** #0d0c0b; 12 f/step

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** silhouette · flat · shadow · ظل

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-kamstudiolabs-0b0824`
- `kosif-tool/styles/pm-kamstudiolabs-0b0824/BRIEF.md`
- `kosif-tool/styles/pm-utopyaszx-1b2f94`

#### 7. قدرات قريبة في العائلة

- `CHAR-19` أشياء بوجوه وتمائم / Object-as-character faces & mascots (seen)
- `CHAR-20` مسرح شخصية بديكور واحد / Single-set character stage (seen)
- `CHAR-22` تمائم البكسل والسبرايت / Pixel & sprite mascots (seen)
- `CHAR-23` تحولات الشخصية / Character transformations & variants (seen)

### `CHAR-22` — تمائم البكسل والسبرايت / Pixel & sprite mascots

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تميمة بكسل تمشي بتبديل رجلين وإطارين، وساحر بكسل يرفع عصاه بست خطوات، وتبديل الشخصية بنفخة دخان. / Pixel mascots with 2-frame leg swaps, stepped staff raises and smoke-puff swaps.

**متى:** ألعاب، تقنية، حنين ريترو / games, tech, retro nostalgia.

**كيف:** walking brick sprite: two eyes, four legs, 2-frame leg swap + 2 px bob at ~6 fps, colour #d17c55, slides with the camera; wizard: walk, staff raise in 6 stepped frames, 2-frame hat overshoot, rune circle at 8 fps; class swap wizard → knight → rogue behind a 6–8 frame pixel smoke puff; index = floor(frame·fps_target/30) % n.

**المعاملات:** 6–8 fps; puff 6–8 f

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pixel · sprite · mascot · retro · بكسل

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-lemomo-ai-0d9cff`
- `kosif-tool/styles/pm-0xevinho-3777d8`
- `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-20` مسرح شخصية بديكور واحد / Single-set character stage (seen)
- `CHAR-21` شخصيات ظلية مسطحة / Flat silhouette characters (seen)
- `CHAR-23` تحولات الشخصية / Character transformations & variants (seen)
- `CHAR-24` دورة المشي بلا انزلاق / Walk cycle without foot sliding (proven)

### `CHAR-23` — تحولات الشخصية / Character transformations & variants

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نفس الشخصية تكبر عبر مراحل بنفس الألوان، أو أجزاؤها تنفصل وتتركب في مواضعها مع اهتزاز الكاميرا عند التلامس. / The same character ages through variants, or its parts dock into slots with a contact shake.

**متى:** قصص النمو، روبوتات تتجمع / growth stories, assembling robots.

**كيف:** swap rig variants per stage keeping palette and silhouette cues; transform & dock: parts tween rotation/position into slots, camera shake 6 px for 150 ms on each contact (EASE-51 hitPulse).

**المعاملات:** shake 6 px / 150 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** transformation · aging · dock · تحول

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-loicrambo-ad6830`
- `kosif-tool/styles/pm-allforbigfire-86ff3c`

#### 7. قدرات قريبة في العائلة

- `CHAR-21` شخصيات ظلية مسطحة / Flat silhouette characters (seen)
- `CHAR-22` تمائم البكسل والسبرايت / Pixel & sprite mascots (seen)
- `CHAR-24` دورة المشي بلا انزلاق / Walk cycle without foot sliding (proven)
- `CHAR-25` ساق مشي إجرائية / Procedural walk-cycle leg (proven)

### `CHAR-24` — دورة المشي بلا انزلاق / Walk cycle without foot sliding

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تلامس ← نزول ← عبور ← صعود، مع اهتزاز الجسم، والمشي في المكان مع خلفية تتحرك بسرعة الخطوة. / Contact-down-passing-up with body bob; walk in place with background parallax at stride speed.

**متى:** كل شخصية تمشي / every walking character.

**كيف:** 24 frames per two steps at 24 fps (12 per step); bob 3–5% of height; background speed = stride / 0.5 s; clip names, durations, loop flag and event markers (contact, footsteps); check body bob and limb separation; phase = f(t) so any frame renders directly; walk/idle/talk as functions of phase returning limb angles and body height with distinct contact and passing poses. Proven in character-rig: each foot's phase c = (d/C) mod 1 from the distance actually travelled; stance half pins the foot in world coordinates, swing half moves it on an inOutSine arc lifting 44 px; stride 118 px at 290 px/s (2.46 steps/s); hip bob 9·cos(4πd/C) lowest at contact; arms swing ±26° opposite the legs; the stop ends with a settling step of the rear foot; 3-layer parallax 0.25 / 0.5 / 1.0.

**المعاملات:** 12 f/step; bob 3–5%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** walk cycle · contact · passing · دورة المشي · gait

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/character-rig/README.md`
- `kosif-tool/playbooks/characters.md:27`
- `kosif-atlas/skills/1526-gamegen/4162-game-animation/SKILL.md`
- `100-superskills/skills/character-animation-2d/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-22` تمائم البكسل والسبرايت / Pixel & sprite mascots (seen)
- `CHAR-23` تحولات الشخصية / Character transformations & variants (seen)
- `CHAR-25` ساق مشي إجرائية / Procedural walk-cycle leg (proven)
- `CHAR-26` آلة حالات الوضعية / Keyframed pose state machine (proven)

### `CHAR-25` — ساق مشي إجرائية / Procedural walk-cycle leg

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ساق مرسومة كضربة منحنية، قدمها تتأرجح بجيب الطور وترتفع في النصف الأمامي فقط، والأرجل البعيدة أغمق، وأربع أرجل بإزاحة π تعطي مشية طبيعية. / A curved-stroke leg whose foot swings with sin(phase) and lifts only on the forward half.

**متى:** حيوانات رباعية مسطحة / flat quadrupeds.

**كيف:** leg(x, phase, far): foot = x + 22·sin(phase), knee = x + 12·sin(phase), lift = max(0, cos(phase))·15; quadratic path stroke 23, round caps, paw stroke 15; step 1.5 Hz, bob cos(2p)·2 px, tail ±9° at half step rate, blink 0.095 s every 4 s; the 8 s loop walks right→left (x = 680 − 145t with a copy 1160 px behind). Captured frames here at 0 / 2 / 5.5 s with Playwright (window.render(t)) show the gait advancing. (code snippet in references/powers/characters-rigs.md)

**المعاملات:** swing ±22 px; lift 15 px; 1.5 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** walk leg · quadruped · gait · cat · ساق

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.html`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.mp4`

#### 7. قدرات قريبة في العائلة

- `CHAR-23` تحولات الشخصية / Character transformations & variants (seen)
- `CHAR-24` دورة المشي بلا انزلاق / Walk cycle without foot sliding (proven)
- `CHAR-26` آلة حالات الوضعية / Keyframed pose state machine (proven)
- `CHAR-27` مولد المشي للسبرايت / Procedural sprite walk generator (documented)

### `CHAR-26` — آلة حالات الوضعية / Keyframed pose state machine

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تمثيل الشخصية كمقاطع زمنية: مشي، انحناء تمهيدي، قفزة بقوس، ضغط هبوط، مشي، ثم نظرة للأعلى / والأطراف تعاد وضعيتها لكل مقطع. — Character action as time segments with limbs re-posed per segment.

**متى:** مشهد قصير بقصة حركية / a short scene with a physical story.

**كيف:** pose(t): walk x = 430 + 59t (gait 1.12 Hz) until 4.1 s; crouch 14·smoothstep((t − 4.65)/0.55); jump u ∈ [5.2, 6.9] s: x 671.9 → 1050, height 147·4u(1 − u), body angle −14° → +12°; land crouch 18·sin; walk 48 px/s at 0.98 Hz; tail 12 sin 2.2t + 3 sin 5t; look = smoothstep((t − 9.7)/0.7) with a 3/4 look-back. Four legs separately articulated (stance 60% of cycle, swing lift 21·sin(πv)). Frame captured here at 5.5 s shows the cat mid-leap over the puddle.

**المعاملات:** apex 147 px; flight 1.7 s; 1.12 → 0.98 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pose state machine · jump · crouch · acting · آلة حالات

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:59`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/midnight-cat.mp4`

#### 7. قدرات قريبة في العائلة

- `CHAR-24` دورة المشي بلا انزلاق / Walk cycle without foot sliding (proven)
- `CHAR-25` ساق مشي إجرائية / Procedural walk-cycle leg (proven)
- `CHAR-27` مولد المشي للسبرايت / Procedural sprite walk generator (documented)
- `CHAR-28` الوضعيات المفتاحية أولًا / Pose-to-pose blocking (documented)

### `CHAR-27` — مولد المشي للسبرايت / Procedural sprite walk generator

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دالة رسم واحدة بمعاملات زوايا الأطراف وطور الخطوة واهتزاز الجسم وأرجحة الذراع والضغط تبقي كل إطار على النموذج. / One draw(direction, pose) function keeps every frame on-model.

**متى:** شخصيات بكسل وألعاب / pixel characters, games.

**كيف:** Python/Pillow or canvas; proportion presets chibi / standard / tall; walk 4–8 frames, bob 1 px; RPG-style 3 patterns 0-1-2-1; mirror the side view only if symmetric and shade after mirroring with light from top-left.

**المعاملات:** 4–8 frames; bob 1 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sprite walk · pixel · procedural · chibi

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2460-pixel-art/9525-animate`

#### 7. قدرات قريبة في العائلة

- `CHAR-25` ساق مشي إجرائية / Procedural walk-cycle leg (proven)
- `CHAR-26` آلة حالات الوضعية / Keyframed pose state machine (proven)
- `CHAR-28` الوضعيات المفتاحية أولًا / Pose-to-pose blocking (documented)
- `CHAR-29` لحظة رد الفعل والقفزة / Reaction & jump recipe (proven)

### `CHAR-28` — الوضعيات المفتاحية أولًا / Pose-to-pose blocking

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضع الوضعيات المفتاحية ثم الوسيطة، كل 8–16 إطارًا. / Block keys, then breakdowns.

**متى:** كل تمثيل شخصية / all character acting.

**كيف:** keys every 8–16 frames at 24–30 fps; stick rig: joint angles per pose interpolated easeInOut over 400 ms, hold 1 s; follow-through 2–4 frames, anticipation 4–8 frames (EASE-49).

**المعاملات:** keys 8–16 f; 400 ms + 1 s hold

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pose to pose · blocking · keys · وضعيات

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/characters.md:24`
- `kosif-tool/styles/pm-chrisjdimarco-f068db`

#### 7. قدرات قريبة في العائلة

- `CHAR-26` آلة حالات الوضعية / Keyframed pose state machine (proven)
- `CHAR-27` مولد المشي للسبرايت / Procedural sprite walk generator (documented)
- `CHAR-29` لحظة رد الفعل والقفزة / Reaction & jump recipe (proven)
- `CHAR-30` الإشارة والكشف / Point and reveal (documented)

### `CHAR-29` — لحظة رد الفعل والقفزة / Reaction & jump recipe

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** هبوط، قفزة، هبوط بانضغاط، متابعة للشعر، ثبات متنفس. / Sink, jump, land with squash, hair follow-through, breathing hold.

**متى:** دهشة، فرح، اكتشاف / surprise, joy, discovery.

**كيف:** 0–200 ms sink 4% ease-in sine; 200–450 ms jump ease-out cubic; 450–700 ms land squash 8% on a spring (damping 12, stiffness 200); 450–800 ms follow-through; 800–2000 ms breathing hold. Hop with anticipation: 120 ms crouch, squash .80–.85 / stretch 1.15, landing cubic-bezier(.34,1.56,.64,1) 450 ms, limbs overlap 60 ms, area preserved (sx·sy = 1). Proven in character-rig: anticipation crouch lowers the hip 62 px in 0.44 s and squashes the torso to sy 0.87; take-off stretch +16%; ballistic flight under constant gravity to a 300 px apex; landing sy = 1 − 0.24·e^(−6.5τ)·cos(13τ) with sx ≈ 1/sy; head lag 26·e^(−5τ)·sin(13(τ − 0.05)); arms overshoot rest then settle; a '!' pops when the box appears.

**المعاملات:** 0/200/450/700/800/2000 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** reaction · jump · squash · رد فعل · hop

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/character-rig/README.md`
- `kosif-tool/playbooks/characters.md:36`
- `kosif-tool/styles/pm-abderrahmen-g-9e8ed0/BRIEF.md`
- `kosif-tool/styles/pm-paulo-kombucha-96431c/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-27` مولد المشي للسبرايت / Procedural sprite walk generator (documented)
- `CHAR-28` الوضعيات المفتاحية أولًا / Pose-to-pose blocking (documented)
- `CHAR-30` الإشارة والكشف / Point and reveal (documented)
- `CHAR-31` الحديث للكاميرا / Talk-to-camera behaviours (documented)

### `CHAR-30` — الإشارة والكشف / Point and reveal

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الذراع تمتد على قوس، والهدف يقفز بعد توقف الإصبع بـ 80 ملّي ثانية. / The arm extends on an arc; the target pops 80 ms after the finger stops.

**متى:** شخصية تقدم بطاقات أو ميزات / a character presenting cards.

**كيف:** arm 350 ms on an arc; target pops at +80 ms; Basma 'character' template: hop in, point at 3 cards, react, wave (circle body, dot eyes, squash & stretch, anticipation, blinking, reacting to on-screen text).

**المعاملات:** arm 350 ms; +80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** point · reveal · present · إشارة

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/characters.md:50`
- `app/public/js/00_editor.js:2007`

#### 7. قدرات قريبة في العائلة

- `CHAR-28` الوضعيات المفتاحية أولًا / Pose-to-pose blocking (documented)
- `CHAR-29` لحظة رد الفعل والقفزة / Reaction & jump recipe (proven)
- `CHAR-31` الحديث للكاميرا / Talk-to-camera behaviours (documented)
- `CHAR-32` ظهور التمائم وقفزاتها / Mascot pop-ins & hop arcs (seen)

### `CHAR-31` — الحديث للكاميرا / Talk-to-camera behaviours

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ميل الرأس على النبر، رمش دوري، والفم من توقيت الأصوات. / Head tilts on stress, periodic blinks, mouth from phoneme timing.

**متى:** شخصية تشرح بصوت المستخدم / a character narrating the user's voice.

**كيف:** tilt ±3° on stressed words (from the emphasis picker ARAB-68 / words.json), blink every 2.5–4 s with a 3-frame blink, mouth index from word timing (CHAR-13); add a small head nod on sentence ends.

**المعاملات:** ±3°; blink 2.5–4 s, 3 f

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** talking · lip sync · blink · tilt · كلام

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/characters.md:48`

#### 7. قدرات قريبة في العائلة

- `CHAR-29` لحظة رد الفعل والقفزة / Reaction & jump recipe (proven)
- `CHAR-30` الإشارة والكشف / Point and reveal (documented)
- `CHAR-32` ظهور التمائم وقفزاتها / Mascot pop-ins & hop arcs (seen)
- `CHAR-33` لمسات تمثيل / Acting accents: celebrate, sleep, run (seen)

### `CHAR-32` — ظهور التمائم وقفزاتها / Mascot pop-ins & hop arcs

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الشخصيات تصعد من خلف الأفق بتجاوز، أو تقفز بداخل دائرة ملونة، أو تقفز على قوس منقط. / Characters rise from behind a hill, pop in on a colour disc, or hop along a dotted parabola.

**متى:** تقديم شخصيات أو فريق / introducing characters or a team.

**كيف:** horizon rise: masked below the hill line, 350 ms easeOutBack(1.6), stagger 150–250 ms left→right (start right for Arabic), then idle bob ±3 px; disc pop: cut-out PNG 0.8 → 1.05 → 1 in 300 ms while a pastel circle grows 400 ms, name pill 'الاسم: الدور' below; hop arc ~1 s along a dotted parabola drawn trailing behind, landing squash.

**المعاملات:** 350 ms backOut 1.6; pop 300 / disc 400 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pop in · horizon · mascot intro · قفزة

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-abderrahmen-g-9e8ed0`
- `kosif-tool/styles/pm-paulo-kombucha-96431c`
- `kosif-tool/styles/pm-kangaroohere-b10f8d`

#### 7. قدرات قريبة في العائلة

- `CHAR-30` الإشارة والكشف / Point and reveal (documented)
- `CHAR-31` الحديث للكاميرا / Talk-to-camera behaviours (documented)
- `CHAR-33` لمسات تمثيل / Acting accents: celebrate, sleep, run (seen)
- `CHAR-34` مبادئ التحريك للهياكل / Animation principles for rigs (documented)

### `CHAR-33` — لمسات تمثيل / Acting accents: celebrate, sleep, run

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مزج من وضعية الركوب إلى بسط الجناحين بتجاوز، حروف Z طافية للنوم، وعدّاء بتمويه حركة يقفز الحواجز. / Celebration blends, floating Z glyphs, a motion-blurred hurdler.

**متى:** ختام فرح، شخصية نائمة، رياضة / happy endings, sleepy characters, sports.

**كيف:** celebration: blend riding → wings-spread over ~0.8 s back.out (wing rotation ~70°), hold, return; sleep: Z glyphs rise, scale up and fade, stagger 250 ms; runner: 8-frame cycle along a baseline, jump arc 400 ms, directional blur (EASE-61).

**المعاملات:** 0.8 s; Z stagger 250 ms; cycle 8 f

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** celebrate · sleep · run · acting · تمثيل

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/pm-axtonliu-0b861d`
- `kosif-tool/styles/pm-cansincengiz-me-cf68dd`
- `kosif-tool/styles/pm-fionntobin-97b7af`

#### 7. قدرات قريبة في العائلة

- `CHAR-31` الحديث للكاميرا / Talk-to-camera behaviours (documented)
- `CHAR-32` ظهور التمائم وقفزاتها / Mascot pop-ins & hop arcs (seen)
- `CHAR-34` مبادئ التحريك للهياكل / Animation principles for rigs (documented)
- `CHAR-35` الشخصية العربية وفقاعة كلامها / RTL staging & Arabic speech bubble (proven)

### `CHAR-34` — مبادئ التحريك للهياكل / Animation principles for rigs

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تمهيد، ضغط عند الهبوط، متابعة للشعر والقماش، أقواس، وحجم ثابت / ولحظة الاصطدام تُثبَّت. — Anticipation, landing squash, hair/cloth follow-through, arcs, constant volume; hold impact frames.

**متى:** مراجعة أي حركة شخصية / reviewing any character motion.

**كيف:** locomotion needs contact / passing / extreme poses with planted feet; actions need readable anticipation, contact and recovery (player-facing attacks avoid long anticipation); hold the impact frame; keep volumes constant; verify encoded frame count, fps and duration after render.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** principles · anticipation · follow-through · arcs · مبادئ

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1526-gamegen/4162-game-animation/SKILL.md`
- `100-superskills/skills/character-animation-2d/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-32` ظهور التمائم وقفزاتها / Mascot pop-ins & hop arcs (seen)
- `CHAR-33` لمسات تمثيل / Acting accents: celebrate, sleep, run (seen)
- `CHAR-35` الشخصية العربية وفقاعة كلامها / RTL staging & Arabic speech bubble (proven)
- `CHAR-36` حياة الخمول / Idle life (breath, blink, glances) (ready)

### `CHAR-35` — الشخصية العربية وفقاعة كلامها / RTL staging & Arabic speech bubble

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** في الأفلام العربية تدخل الشخصيات من اليمين وتنظر يسارًا، وفقاعات الكلام تحمل جملًا عربية كاملة من اليمين. / In Arabic films characters enter from the right and look left; bubbles hold whole RTL phrases.

**متى:** كل فيلم شخصيات عربي / every Arabic character film.

**كيف:** mirror the staging plan (entrances, look direction, reading path); balloons pop with a spring and contain whole shaped phrases (never per letter); stagger group entrances right → left. Proven in character-rig: the bubble springs out from its tail tip (k 230, ζ ≈ 0.5) and the line «قفزةٌ واحدة… وصارت العقبةُ خلفي!» appears word by word right → left in Cairo 800 at 50 px, each word whole and shaped, popping with outBack on its spoken time; the camera eases to ×1.18–1.26 while the character talks.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** RTL · staging · speech bubble · عربي · اتجاه

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/character-rig/README.md`
- `kosif-tool/playbooks/characters.md:75`

#### 7. قدرات قريبة في العائلة

- `CHAR-33` لمسات تمثيل / Acting accents: celebrate, sleep, run (seen)
- `CHAR-34` مبادئ التحريك للهياكل / Animation principles for rigs (documented)
- `CHAR-36` حياة الخمول / Idle life (breath, blink, glances) (ready)
- `CHAR-37` حركة ثانوية بالنوابض والسلاسل / Spring & chain secondary motion (proven)

### `CHAR-36` — حياة الخمول / Idle life (breath, blink, glances)

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تنفس صغير، تمايل الرأس على عدة موجات، رمش مجدول، أذنان وذيل / كلها دالة للزمن. — Breathing, head sway, scheduled blinks, ears and tail as a pure function of t.

**متى:** أي ثبات للشخصية / any character hold.

**كيف:** K3.idle(root, t, {amount, phase}): breath ±1.2% at 2.2 rad/s, blink every 3.7 s lasting 0.3 s, ears ±.12 rad at 2.6, tail ±.35 rad at 3.1; bunny project: breath .006·sin(2π·0.9t), head (.05 sin 1.7t, .12 sin(1.1t + .5), .05 sin 1.3t), blink windows 1.18–1.34 s and 4.62–4.76 s with eye scaleY 1 − .85·bl, a 0.25 rad head turn toward camera at its stop; 2D moving hold: torso scale 1–2% over 2 s.

**المعاملات:** breath 0.6–1.2%; blink /3.7 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** idle · breathing · blink · moving hold · تنفس · رمش

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/lab-kit.js:280`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:118`
- `kosif-tool/playbooks/characters.md:28`

#### 7. قدرات قريبة في العائلة

- `CHAR-34` مبادئ التحريك للهياكل / Animation principles for rigs (documented)
- `CHAR-35` الشخصية العربية وفقاعة كلامها / RTL staging & Arabic speech bubble (proven)
- `CHAR-37` حركة ثانوية بالنوابض والسلاسل / Spring & chain secondary motion (proven)
- `CHAR-38` فراشة ويراعة مرافقة / Winged companions (butterfly, firefly) (proven)

### `CHAR-37` — حركة ثانوية بالنوابض والسلاسل / Spring & chain secondary motion

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مجموعات مفاصل تقودها نوابض (تردد وتخميد) لارتخاء الأذن وارتداد الذيل، تحت حد سرعة. / Pivot groups driven by frequency/ζ springs under a speed gate.

**متى:** آذان، ذيول، شعر، إكسسوارات متدلية / ears, tails, hair, dangling props.

**كيف:** angle = A·(1 − spring(t, t0, f, ζ)) on each pivot (EASE-25); ear flop f 1.5 Hz ζ 0.42 passes; f 2.2 Hz ζ 0.28 failed the 80 px/frame gate at 1080×1920 — measure with motion.py speed (EASE-60). Chains: character-rig's scarf is a 9-link Verlet chain re-simulated from t = 0 at a fixed step on every seek, so any frame is identical whatever order it renders in (verified film).

**المعاملات:** 1.5 Hz ζ .42 ok; 2.2/.28 fails

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Verlet · scarf · secondary motion · spring · ears · follow through · حركة ثانوية

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/character-rig/README.md`
- `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js`

#### 7. قدرات قريبة في العائلة

- `CHAR-35` الشخصية العربية وفقاعة كلامها / RTL staging & Arabic speech bubble (proven)
- `CHAR-36` حياة الخمول / Idle life (breath, blink, glances) (ready)
- `CHAR-38` فراشة ويراعة مرافقة / Winged companions (butterfly, firefly) (proven)
- `CHAR-39` سرب طيور / Flock of birds (ready)

### `CHAR-38` — فراشة ويراعة مرافقة / Winged companions (butterfly, firefly)

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فراشة متوهجة ترشد البطل: جناحاها يرفرفان بتحجيم أفقي وتتمايل على مسار جيبي بهالة سماوية. / A glowing butterfly leads the hero, flapping by horizontal scale on a sine path.

**متى:** مرشد صغير في مشهد ليلي / a small guide in night scenes.

**كيف:** wing scaleX = \|sin(2π·4.5t)\|·0.85 + 0.13; y = 348 − 20 sin 1.8t − 48·smooth((t − 4.2)/1.8) + 55·smooth((t − 7)/2); fill #86fff0 at .87, halo r 28; firefly: oval body, big eyes, flap 8 Hz, radial-gradient glow on the tail. Visible in the frame captured here at 5.5 s.

**المعاملات:** 4.5 Hz (butterfly), 8 Hz (firefly)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** butterfly · firefly · wing flap · companion · فراشة

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:107`
- `kosif-tool/styles/pm-kamstudiolabs-c9bb28`

#### 7. قدرات قريبة في العائلة

- `CHAR-36` حياة الخمول / Idle life (breath, blink, glances) (ready)
- `CHAR-37` حركة ثانوية بالنوابض والسلاسل / Spring & chain secondary motion (proven)
- `CHAR-39` سرب طيور / Flock of birds (ready)
- `CHAR-40` الأرنب القطيفة المنحوت / SDF plush bunny (rigged) (proven)

### `CHAR-39` — سرب طيور / Flock of birds

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طيور على شكل V مكررة بالمثيلات ترفرف في الشيدر وتتبع مسارًا مفتاحيًا. / Instanced V-shaped birds flapping in a shader along a keyed path.

**متى:** سماء حية، غروب، رحلة / living skies, sunsets, journeys.

**كيف:** K3.makeFlock({n:18, path:[[t,x,y,z],…], t0, t1, spread:120, size:9, color:'#1a1d22', seed}); mesh.userData.set(t); flap sin(t·9).

**المعاملات:** n 18; spread 120; flap sin 9t

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** birds · flock · instancing · سرب

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:203`

#### 7. قدرات قريبة في العائلة

- `CHAR-37` حركة ثانوية بالنوابض والسلاسل / Spring & chain secondary motion (proven)
- `CHAR-38` فراشة ويراعة مرافقة / Winged companions (butterfly, firefly) (proven)
- `CHAR-40` الأرنب القطيفة المنحوت / SDF plush bunny (rigged) (proven)
- `CHAR-41` عيون لامعة وعيون برمش / Glossy & blinking eyes (ready)

### `CHAR-40` — الأرنب القطيفة المنحوت / SDF plush bunny (rigged)

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أرنب لطيف منحوت إجرائيًا بأجزاء مفصلية مسماة (جسم، رأس، أذنان، ذيل، عينان، فم، وشاح) وعيون موضوعة بإصابة الأشعة. / A procedurally sculpted plush bunny with named rig parts.

**متى:** تميمة ثلاثية الأبعاد، قصص أطفال، إعلانات لطيفة / 3D mascots, kids' stories.

**كيف:** const b = K3S.bunny({fur:'#f2e4d8', belly:'#fbf3ea', pink:'#ff9fb8', nose:'#ff7c9c', scarf:'#7fe7b4', cells:132}); animate b.parts.head / earL / earR / tail rotations (neck pivot [0, .152, .004], ears pivot from the skull); ~0.33 m tall; stage disc (r .24, #9dffb4, shadow .5) and studio backdrop (#22504a / #0d2627 / #040b0c); 'w' mouth and stitches as Catmull-Rom tubes (32 segments, r 1.1 mm). test_shape_kit passed here (96 cells > 50,000 triangles; 183,752 triangles at full res, ~4.6 s mesh time).

**المعاملات:** ~0.33 m; 132 cells

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** bunny · SDF · plush · rigged · 3D mascot · أرنب

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/shape-kit.js:453`
- `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:40`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:29`

#### 7. قدرات قريبة في العائلة

- `CHAR-38` فراشة ويراعة مرافقة / Winged companions (butterfly, firefly) (proven)
- `CHAR-39` سرب طيور / Flock of birds (ready)
- `CHAR-41` عيون لامعة وعيون برمش / Glossy & blinking eyes (ready)
- `CHAR-42` أرنب وأسد المختبر / Lab rabbit & lion characters (ready)

### `CHAR-41` — عيون لامعة وعيون برمش / Glossy & blinking eyes

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مقلة لامعة بحلقة قزحية دافئة ونقطتي ضوء، أو عين بطبقات (صلبة، قزحية مضيئة، بؤبؤ، قرنية) برمش. / Glossy eyeballs with two catch-lights, or layered eyes with a blink.

**متى:** كل شخصية ثلاثية الأبعاد / every 3D character.

**كيف:** K3S.eye({r:.012, tall:1.12, color, iris:'#5a3a2c'}) — iris at 55%, catch-lights .3r and .14r upper-outer, gloss roughness .08, clearcoat 1, ior 1.5, env 1.6; K3.makeEye(r, {iris}): sclera #f4f6f2, iris #8fe02a (emissive 12%), pupil #05070a, cornea opacity .22; eye.userData.blink(k) scales y by 1 − .92k.

**المعاملات:** r .012; catch-lights .3/.14 r

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** eyes · catch-light · blink · glossy · عيون

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/shape-kit.js:311`
- `kosif-studio/motion/kit/lab-kit.js:56`

#### 7. قدرات قريبة في العائلة

- `CHAR-39` سرب طيور / Flock of birds (ready)
- `CHAR-40` الأرنب القطيفة المنحوت / SDF plush bunny (rigged) (proven)
- `CHAR-42` أرنب وأسد المختبر / Lab rabbit & lion characters (ready)
- `CHAR-43` سمكة كوي إجرائية / Procedural koi (ready)

### `CHAR-42` — أرنب وأسد المختبر / Lab rabbit & lion characters

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حيوانان قطيفة بمفاصل مسماة وفرو بطبقات قشرية على أرضية استوديو كريمية، مع HUD يسمي الأجزاء ومبادلة أجزاء. / Two plush animals with named joints and shell fur on a cream sweep, with a part-naming HUD.

**متى:** شرح «كيف صُنع»، مقارنة، علوم للأطفال / 'how it's made', comparisons, kids' science.

**كيف:** K3.makeRabbit({color:'#f1f0ea', inner:'#f3b6c0', iris:'#3a7bd5', furLength:.09, layers:7}); K3.makeLion({color:'#e3b05a', mane:'#8a4a1c', iris:'#d9a21b', muzzle:'#f5e2b8', furLength:.07, layers:8, mane ×2.6, gravity .5}); root.userData.joints; studio(scene); labPost(renderer, …, {bloom:0}); six HUD beats SHAPE → JOINT → LOAD → BREAK → SWAP → RANK; swap: rabbit tail colour lerps to 0x8a4a1c and scales 1 + .45·sw over 16.4–17.2 s; materials leather 0x15171a, metal 0xd8dde3; motion.py new NAME --lab scaffolds it (960×540, 24 fps, 20 s).

**المعاملات:** fur .07–.09; 7–8 layers

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** rabbit · lion · shell fur · lab · joints · أسد

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/lab-kit.js:74`
- `kosif-studio/motion/kit/lab-kit.js:101`
- `kosif-studio/motion/projects/lab_rabbit_lion/README.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-40` الأرنب القطيفة المنحوت / SDF plush bunny (rigged) (proven)
- `CHAR-41` عيون لامعة وعيون برمش / Glossy & blinking eyes (ready)
- `CHAR-43` سمكة كوي إجرائية / Procedural koi (ready)
- `CHAR-44` شخصيات من أشكال أولية / Primitive toon figures (ready)

### `CHAR-43` — سمكة كوي إجرائية / Procedural koi

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سمكة كوي بجسم مرفوع وزعانف وجلد بنقوش حراشف ببذرة في أربعة أنواع، وانحناء سباحة يميل في المنعطفات. / A lofted koi with seeded scale skin in four varieties and a swim bend that leans into turns.

**متى:** برك، حدائق يابانية، هدوء / ponds, calm scenes.

**كيف:** const k = K3.makeKoi({length:.62, seed, kind:'kohaku'\|'sanke'\|'showa'\|'ogon', amp:.11, caustics}); k.userData.set(t, path(t, out), 1.6); 28 rings × 18 segments, skin 256 px, clearcoat .6; base #f4eee4 (ogon #e8be5a), red #e25620 (showa #c4341c), black #181618.

**المعاملات:** .62 m; swim 1.6 Hz; amp .11

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** koi · fish · swim · procedural · سمكة

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/three-kit.js:629`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:613`

#### 7. قدرات قريبة في العائلة

- `CHAR-41` عيون لامعة وعيون برمش / Glossy & blinking eyes (ready)
- `CHAR-42` أرنب وأسد المختبر / Lab rabbit & lion characters (ready)
- `CHAR-44` شخصيات من أشكال أولية / Primitive toon figures (ready)
- `CHAR-45` دوران 360 لورقة الشخصية / Turntable character sheet (ready)

### `CHAR-44` — شخصيات من أشكال أولية / Primitive toon figures

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شخصيات كرتونية من كرات وكبسولات بعيون كبيرة ومفاصل هرمية، أو صياد من الخلف يكفي ليُقرأ إنسانًا. / Toon characters from spheres and capsules with hierarchical joints.

**متى:** مشاهد ثلاثية الأبعاد سريعة تحتاج إنسانًا / quick 3D scenes needing a figure.

**كيف:** fisherman: torso Capsule(.2, .42) rotated −.18, head sphere .13 + half-sphere cap 0xcfc6b2, leg capsules, rod cylinder .008 → .02 oriented by a quaternion base → tip, Line to the water; toon material + big eyes for cartoon figures; keep pivots at joints for rotation.

**المعاملات:** capsule .2/.42; head .13

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** primitive · toon · capsule · figure · شخصيات بسيطة

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:96`
- `kosif-tool/styles/pm-ryzoft-4f85bd`

#### 7. قدرات قريبة في العائلة

- `CHAR-42` أرنب وأسد المختبر / Lab rabbit & lion characters (ready)
- `CHAR-43` سمكة كوي إجرائية / Procedural koi (ready)
- `CHAR-45` دوران 360 لورقة الشخصية / Turntable character sheet (ready)
- `CHAR-46` جسد من الجسيمات بحركة حقيقية / Particle body from real motion (mocap) (ready)

### `CHAR-45` — دوران 360 لورقة الشخصية / Turntable character sheet

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكاميرا تتوقف أمام وجانب وظهر وجانب الشخصية بثبات، كورقة دوران قبل التحريك. / Camera steps front, side, back, side with holds, like a turnaround sheet.

**متى:** اعتماد الشخصية مع المستخدم قبل الفيلم / approving a character before the film.

**كيف:** K3.shot('turntable', {subject, size, t0, t1}): 4 quarter turns, each holding 70% of its quarter and turning in the last 30%; frame at 80% of height; render once and show the user as a contact sheet.

**المعاملات:** 4 holds; turn in last 30%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** turntable · 360 · character sheet · دوران

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/three-kit.js:1066`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1067`

#### 7. قدرات قريبة في العائلة

- `CHAR-43` سمكة كوي إجرائية / Procedural koi (ready)
- `CHAR-44` شخصيات من أشكال أولية / Primitive toon figures (ready)
- `CHAR-46` جسد من الجسيمات بحركة حقيقية / Particle body from real motion (mocap) (ready)
- `CHAR-47` تمثيل الشخصيات بلوتي / Lottie character acting (install)

### `CHAR-46` — جسد من الجسيمات بحركة حقيقية / Particle body from real motion (mocap)

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مؤدٍّ مصوّر بكاميرا ثابتة يصبح جسيمات متوهجة داخل ظله مع أشباح متتبعة. / A performer on a fixed camera becomes glowing particles inside the silhouette, with tracer ghosts.

**متى:** رقص، رياضة، لحظة سحرية / dance, sport, magical moments.

**كيف:** python motion.py mocap VIDEO --out body.json [--points 1200] (background difference, threshold 28, coords 0..1000; OpenCV 5.0 is installed here) → K3.makeParticleBody(json, {height:4, depth:.35, ghosts:3, ghostStep:3, color:'#ffb36b', size:26}); userData.set(t, pulse); ghost alpha .35/k.

**المعاملات:** 1200 pts; 3 ghosts every 3 f

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mocap · particle body · silhouette · dance · جسيمات

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/kit/three-kit.js:938`
- `kosif-studio/motion/motion.py`
- `100-superskills/skills/kosif-montage-motion/scripts/qa.py:605`

#### 7. قدرات قريبة في العائلة

- `CHAR-44` شخصيات من أشكال أولية / Primitive toon figures (ready)
- `CHAR-45` دوران 360 لورقة الشخصية / Turntable character sheet (ready)
- `CHAR-47` تمثيل الشخصيات بلوتي / Lottie character acting (install)
- `CHAR-48` لوحات الكوميكس / Comics panels (ready)

### `CHAR-47` — تمثيل الشخصيات بلوتي / Lottie character acting

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تمثيل الشخصية (مشي، توقف، إشارة، سكون) في ملف Lottie واحد، وGSAP يملك البطاقات والكاميرا موقوتة على علامات الملف. / The character's acting lives in one Lottie; GSAP owns cards and camera timed to its markers.

**متى:** شخصية مصممة في After Effects أو مرخصة / AE-made or licensed characters.

**كيف:** lottie-web or dotLottie player registered for seeking (goToAndStop(frame, true) from seek(t)); read beat times from markers (tm frames / fr); 1 s walk cycle loop:true moved with GSAP x matched to stride; offset actions inside the file; HyperFrames block lottie-character-walk (planted feet, stops and points at a card, 7.5 s); license the character.

**المعاملات:** walk loop 1 s; block 7.5 s

**التثبيت:** npm i lottie-web

**الوسوم:** lottie · after effects · walk · character acting · لوتي

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `npm:lottie` ← npm ls lottie أو وجود node_modules/lottie
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/lottie.md`
- `kosif-one/vendor/hyperframes/registry/blocks/lottie-character-walk/lottie-character-walk.html`

#### 7. قدرات قريبة في العائلة

- `CHAR-45` دوران 360 لورقة الشخصية / Turntable character sheet (ready)
- `CHAR-46` جسد من الجسيمات بحركة حقيقية / Particle body from real motion (mocap) (ready)
- `CHAR-48` لوحات الكوميكس / Comics panels (ready)
- `CHAR-49` أنمي أكشن / Anime action (ready)

### `CHAR-48` — لوحات الكوميكس / Comics panels

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قصة في لوحات بفواصل وفقاعات كلام، والكاميرا تتنقل بين اللوحات. / A story in comic panels with gutters and balloons; the camera travels panel to panel.

**متى:** قصص قصيرة وحكايات تعليمية / short stories, lessons.

**كيف:** python3 tools/kosif.py scaffold comics-panels <dir>; Canvas/SVG panel grid, each panel a scene with a pose-to-pose rig (keys every 8–16 frames, anticipation 4–8 frames); camera rig pans between panels; balloons pop with a spring and hold whole Arabic phrases; ink outlines. Panels generated without text, bubbles drawn in code (ARAB-09).

**المعاملات:** keys 8–16 f

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** comics · panels · speech balloons · كوميكس

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/comics-panels/SKILL.md`
- `kosif-tool/styles/comics-panels/STYLE.json`
- `kosif-atlas/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`

#### 7. قدرات قريبة في العائلة

- `CHAR-46` جسد من الجسيمات بحركة حقيقية / Particle body from real motion (mocap) (ready)
- `CHAR-47` تمثيل الشخصيات بلوتي / Lottie character acting (install)
- `CHAR-49` أنمي أكشن / Anime action (ready)
- `CHAR-50` صفحات ويبتون بشخصيات حيوانية / Webtoon pages with Arabic overlay (key)

### `CHAR-49` — أنمي أكشن / Anime action

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أكشن مستوحى من الأنمي: خطوط سرعة، إطارات اصطدام، لطخات حركة. / Speed lines, impact frames and smears.

**متى:** لحظات قتال أو انطلاق رياضي / fights, sports bursts.

**كيف:** python3 tools/kosif.py scaffold anime-action <dir>; 2D rig + smear frames, speed-line overlays, camera shake; anticipation 4–8 frames, overshoot 5–10%; hold impact frames 2–3 frames with an inverted flash; original designs only.

**المعاملات:** anticipation 4–8 f; overshoot 5–10%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** anime · action · smear · speed lines · impact frame · أنمي

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/anime-action/SKILL.md`
- `kosif-tool/styles/anime-action/STYLE.json`

#### 7. قدرات قريبة في العائلة

- `CHAR-47` تمثيل الشخصيات بلوتي / Lottie character acting (install)
- `CHAR-48` لوحات الكوميكس / Comics panels (ready)
- `CHAR-50` صفحات ويبتون بشخصيات حيوانية / Webtoon pages with Arabic overlay (key)
- `CHAR-X01` شخصيات حية ببصمات حركة / Alive characters: personality motion signatures (documented)

### `CHAR-50` — صفحات ويبتون بشخصيات حيوانية / Webtoon pages with Arabic overlay

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أوصاف شخصيات حيوانية ثابتة تُكرر حرفيًا في كل وصف، خلفية بيضاء، والحوار طبقة SVG قابلة للتحرير بعربية صحيحة. / Fixed animal character descriptions repeated verbatim, white background, dialogue as an editable SVG overlay.

**متى:** قصص أطفال مصورة / illustrated kids' stories.

**كيف:** art from an image model (needs a key) with no text; dialogue balloons and Arabic lettering drawn in SVG over the panels; animate panels with gentle push-ins and balloon pops.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** webtoon · chibi · kids · dialogue overlay · ويبتون

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`

#### 7. قدرات قريبة في العائلة

- `CHAR-48` لوحات الكوميكس / Comics panels (ready)
- `CHAR-49` أنمي أكشن / Anime action (ready)
- `CHAR-X01` شخصيات حية ببصمات حركة / Alive characters: personality motion signatures (documented)

### `CHAR-X01` — شخصيات حية ببصمات حركة / Alive characters: personality motion signatures

| الحقل | القيمة |
|---|---|
| العائلة | `characters-rigs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/characters-rigs.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** لكل شخصية بصمة حركة رياضية (عصبي يرتجف، متعلق يقفز، نعسان يطفو)، وحركة الخمول ضعف ما يبدو صحيحًا في صورة ثابتة. — Each character gets a motion signature (grumpy jitters, clingy hops, sleepy floats), and idle motion runs at about twice what looks right in a still.

**متى:** شخصيات صغيرة لطيفة أو تمائم في فيلم منتج — small mascots or pets in a product film.

**كيف:** Grumpy: jitter sin(83t)·8 + sin(61t)·5 px with huffs max(0, sin 5t)^5 and a 2.5 Hz stomp. Clingy: hops at 1.9 Hz, landing squash 1.19 / 0.83. Sleepy: float sin(2.4t)·32 px. Hyper: hops 2.6 Hz, saccade eyes sign(sin 5.2t)·\|sin\|^0.2·26. Arrival squash 0.1·e^(−7a)·sin(19a); blink every 1.7–2.3 s and hide awkward shape intermediates behind a blink. Vector idle: breath scaleY 1 + 0.014·sin(2.4t), head 2.5 px / 1.2°, tail 4°·sin(1.9t). SDF bodies on the CPU at ⅓ resolution, upscaled with blur(5px); snap colour-mixed backgrounds with smoothstep(.38,.62) to avoid muddy grey. Judge on 2-frame contact sheets.

**المعاملات:** idle ×2; blink 1.7–2.3 s; squash 1.19/0.83; breath 1.4 %

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** character · idle · squash · blink · personality · شخصية · خمول · رمش

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:CHAR-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `character-fullbody` · `character-ik` · `code-drawing-master` · `motion-engine-js` · `motion-toolkit`.
- مراحل النوع: قياس الصوت والأصول ← ستوريبورد ← بناء المشهد ← معاينة رخيصة ← رندر ← تحقق ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المدة والمقاس وfps مطابقة بالقياس ← tools/verify_video.py أو ffprobe
- إلزامي: صوت المستخدم منسوخ بلا تعديل (MD5 مطابق) ← ffmpeg -f md5
- جودة: تزامن الكلمات ضمن ±2 إطار من words.json ← سجل seek
- إلزامي: العربية متصلة الحروف وصحيحة الاتجاه ← لوحة لقطات
- إلزامي: حركة حقيقية (كاميرا أو رسم أو تحويل) لا شرائح ثابتة ← لوحة لقطات كل ثانيتين
- جودة: النص داخل المنطقة الآمنة للمنصة ← لقطة بإطار المنطقة الآمنة
- إلزامي: رخصة كل لقطة وموسيقى وخط مسجلة ← rights.json أو جدول المصادر
- جودة: معاينة رخيصة قبل الرندر الكامل ← render_html.cjs --preview
- أمر الحكم في الوضع 1: `think.py qa video --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md`

#### 7. قدرات قريبة في العائلة

- `CHAR-49` أنمي أكشن / Anime action (ready)
- `CHAR-50` صفحات ويبتون بشخصيات حيوانية / Webtoon pages with Arabic overlay (key)

