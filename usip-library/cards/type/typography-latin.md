# `typography-latin` — الخطوط والنصوص العربية واللاتينية (94 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/typography-latin.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/type.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`TYPE-01` مقاسات الخط للفيديو](#type-01--مقاسات-الخط-للفيديو--video-type-sizing--contrast)
- [`TYPE-02` ميزانية الكلمات والأسطر](#type-02--ميزانية-الكلمات-والأسطر--word--line-budgets-on-screen-copy--narration)
- [`TYPE-03` زمن القراءة والثبات](#type-03--زمن-القراءة-والثبات--read-time--hold-rules)
- [`TYPE-04` سلّم الأحجام والأوزان والتباعد](#type-04--سلّم-الأحجام-والأوزان-والتباعد--scale-weight-leading--tracking-tokens)
- [`TYPE-05` اختيار الخط وتزويجه](#type-05--اختيار-الخط-وتزويجه--choosing--pairing-faces)
- [`TYPE-06` أرقام جدولية وخصائص OpenType](#type-06--أرقام-جدولية-وخصائص-opentype--tabular-numerals--opentype-features)
- [`TYPE-07` ملاءمة النص للعرض وقياسه](#type-07--ملاءمة-النص-للعرض-وقياسه--fit-to-width--text-measuring)
- [`TYPE-08` نص SVG حاد وهالات التسميات](#type-08--نص-svg-حاد-وهالات-التسميات--crisp-svg-text--label-halos)
- [`TYPE-09` تراخيص الخطوط ونظافتها](#type-09--تراخيص-الخطوط-ونظافتها--font-licensing--font-hygiene)
- [`TYPE-10` حدود النص داخل صور الذكاء الاصطناعي](#type-10--حدود-النص-داخل-صور-الذكاء-الاصطناعي--text-in-ai-image-ladder)
- [`TYPE-11` خطوط لاتينية مدمجة جاهزة](#type-11--خطوط-لاتينية-مدمجة-جاهزة--owner-bundled-latin-fonts-offline)
- [`TYPE-12` تضمين الخطوط داخل الملف](#type-12--تضمين-الخطوط-داخل-الملف--offline-font-inlining-base64)
- [`TYPE-13` مجموعة Google Fonts للتبديل الحي](#type-13--مجموعة-google-fonts-للتبديل-الحي--curated-google-fonts-swap-set)
- [`TYPE-14` صعود من خلف خط القاعدة](#type-14--صعود-من-خلف-خط-القاعدة--baseline-mask-rise-lines--words)
- [`TYPE-15` صعود من حالة جزئية](#type-15--صعود-من-حالة-جزئية--rise-from-a-partial-state-risewords)
- [`TYPE-16` ظهور من الضباب (سحب البؤرة)](#type-16--ظهور-من-الضباب-سحب-البؤرة--blur-to-sharp-focus-pull)
- [`TYPE-17` إضاءة الكلمات بترتيب القراءة](#type-17--إضاءة-الكلمات-بترتيب-القراءة--reading-order-light-up--blur-manifesto)
- [`TYPE-18` تتابع الحروف سقوطًا وصعودًا](#type-18--تتابع-الحروف-سقوطًا-وصعودًا--per-letter-drop--rise-cascades)
- [`TYPE-19` تبعثر وتدحرج وتجميع](#type-19--تبعثر-وتدحرج-وتجميع--scatter-tumble--gravity-assemble)
- [`TYPE-20` تقارب الحروف](#type-20--تقارب-الحروف--tracking-in-collapse-latin-only)
- [`TYPE-21` تكديس الأسطر ودفعها وتبديلها](#type-21--تكديس-الأسطر-ودفعها-وتبديلها--line-stack-push--swap)
- [`TYPE-22` الدخول الشلالي](#type-22--الدخول-الشلالي--waterfall-entry-cascade)
- [`TYPE-23` بناء من المركز](#type-23--بناء-من-المركز--kinetic-center-build)
- [`TYPE-24` مسح الكلمة الكبيرة بالقناع](#type-24--مسح-الكلمة-الكبيرة-بالقناع--clip-path-big-word-wipe)
- [`TYPE-25` كشف بالشرائح](#type-25--كشف-بالشرائح--strip-slice-letter-reveal)
- [`TYPE-26` بناء الكلمة على شبكة إنشائية](#type-26--بناء-الكلمة-على-شبكة-إنشائية--construction-grid--guide-line-build)
- [`TYPE-27` عنوان قماشي من 1–4 كلمات مع اتجاه تلقائي](#type-27--عنوان-قماشي-من-14-كلمات-مع-اتجاه-تلقائي--canvas-14-word-headline-with-auto-rtl)
- [`TYPE-28` موجة الحروف](#type-28--موجة-الحروف--per-letter-sine-bounce--wave)
- [`TYPE-29` مفردات حركة النص للستوري بورد](#type-29--مفردات-حركة-النص-للستوري-بورد--text-motion-vocabulary-for-storyboards)
- [`TYPE-30` الكلمة المختفية](#type-30--الكلمة-المختفية--invisible-word-blink)
- [`TYPE-31` آلة كاتبة متدرجة بمؤشر](#type-31--آلة-كاتبة-متدرجة-بمؤشر--eased-typewriter-with-caret-typeon)
- [`TYPE-32` كتابة بشرية: أخطاء ومسح ومؤشر ملوّن](#type-32--كتابة-بشرية-أخطاء-ومسح-ومؤشر-ملوّن--human-typing-typos-backspace-caret-swap)
- [`TYPE-33` فك التشفير](#type-33--فك-التشفير--scramble--decode-reveal)
- [`TYPE-34` قلب الحروف ثلاثي الأبعاد](#type-34--قلب-الحروف-ثلاثي-الأبعاد--hacker-flip-3d-decode)
- [`TYPE-35` لوحة المطار القلّابة](#type-35--لوحة-المطار-القلّابة--split-flap-solari-board)
- [`TYPE-36` عدّاد الأسطوانة الدوّار](#type-36--عدّاد-الأسطوانة-الدوّار--odometer-digit-roll)
- [`TYPE-37` عدّاد بأرقام جدولية](#type-37--عدّاد-بأرقام-جدولية--tabular-counter-motioncounter)
- [`TYPE-38` بكرة الكلمات وعدّاد نابض](#type-38--بكرة-الكلمات-وعدّاد-نابض--slot-machine-word-roll--spring-ticker)
- [`TYPE-39` تبديل كلمة في خانة ثابتة واستيلاء الشريط](#type-39--تبديل-كلمة-في-خانة-ثابتة-واستيلاء-الشريط--word-slot-swap--ticker-takeover)
- [`TYPE-40` إيقاع البادئة/البطل/الذيل](#type-40--إيقاع-البادئةالبطلالذيل--lead--hero--tail-beat-splitter)
- [`TYPE-41` صدمة العنوان وضربة الكلمة على الإيقاع](#type-41--صدمة-العنوان-وضربة-الكلمة-على-الإيقاع--headline-slam--beat-word-punch)
- [`TYPE-42` متتاليات الضرب وجمل تُبنى بالضربات](#type-42--متتاليات-الضرب-وجمل-تُبنى-بالضربات--beat-slam-sequences--stacked-statements)
- [`TYPE-43` وصفة سطر الافتتاح](#type-43--وصفة-سطر-الافتتاح--hook-line-recipe--kinetic-type-beats)
- [`TYPE-44` ختم وملصق وكلمة مؤثر صوتي](#type-44--ختم-وملصق-وكلمة-مؤثر-صوتي--stamp-sticker--sfx-word-pop)
- [`TYPE-45` انزلاق بضبابية حركة ولطخة لونية](#type-45--انزلاق-بضبابية-حركة-ولطخة-لونية--motion-blur-slide-smear--stretch)
- [`TYPE-46` كلمة بانفصال RGB وتشويش](#type-46--كلمة-بانفصال-rgb-وتشويش--rgb-split-glitch-word)
- [`TYPE-47` بدائيات حركة النص على الموسيقى](#type-47--بدائيات-حركة-النص-على-الموسيقى--music-anchored-type-primitives--templates)
- [`TYPE-48` نص بإطارات ممسوكة](#type-48--نص-بإطارات-ممسوكة--held-frame-stepped-type)
- [`TYPE-49` قلم التظليل والخط السفلي](#type-49--قلم-التظليل-والخط-السفلي--highlighter--underline-swipe)
- [`TYPE-50` كلمات داخل كبسولات](#type-50--كلمات-داخل-كبسولات--keyword-pills)
- [`TYPE-51` شطب واستبدال](#type-51--شطب-واستبدال--strike-through--replace)
- [`TYPE-52` عنوان بلونين وكلمة لون](#type-52--عنوان-بلونين-وكلمة-لون--two-tone-lines--accent-word-colour)
- [`TYPE-53` غروتسك عريض مع كلمة سيريف مائلة](#type-53--غروتسك-عريض-مع-كلمة-سيريف-مائلة--grotesk--italic-serif-accent)
- [`TYPE-54` عنوان سيريف تحريري بكلمة مائلة](#type-54--عنوان-سيريف-تحريري-بكلمة-مائلة--editorial-serif-headline--keyword-title)
- [`TYPE-55` تعبئة متدرجة ومعدنية](#type-55--تعبئة-متدرجة-ومعدنية--gradient--metallic-word-fills)
- [`TYPE-56` أقواس تحديد وصندوق أداة تصميم](#type-56--أقواس-تحديد-وصندوق-أداة-تصميم--selection-brackets--design-tool-bounding-box)
- [`TYPE-57` صور ووجوه وأيقونات داخل السطر](#type-57--صور-ووجوه-وأيقونات-داخل-السطر--inline-avatars--icons-inside-a-headline)
- [`TYPE-58` الكلمة تؤدي معناها](#type-58--الكلمة-تؤدي-معناها--word-performs-its-meaning)
- [`TYPE-59` قوائم تخفت السابق](#type-59--قوائم-تخفت-السابق--dim-previous-stacks--active-item-lists)
- [`TYPE-60` النقطة الختامية وإبدال الحرف](#type-60--النقطة-الختامية-وإبدال-الحرف--full-stop-dot--glyph-substitution)
- [`TYPE-61` الخط المتغير: محاور ووزن متموج وعرض](#type-61--الخط-المتغير-محاور-ووزن-متموج-وعرض--variable-font-motion-axis-tween-weight-wave-width-swell)
- [`TYPE-62` خط مفرّغ: أرقام مجوفة ومن محيط إلى تعبئة](#type-62--خط-مفرّغ-أرقام-مجوفة-ومن-محيط-إلى-تعبئة--outline-type-hollow-numerals-outline--fill-glowing-outline)
- [`TYPE-63` طباعة شبحية خلفية](#type-63--طباعة-شبحية-خلفية--giant-ghost-background-type--ghost-rows)
- [`TYPE-64` نص بارز بظلال مكدسة](#type-64--نص-بارز-بظلال-مكدسة--extruded--stacked-shadow-type)
- [`TYPE-65` أثر الصدى والنسخ المحيطية](#type-65--أثر-الصدى-والنسخ-المحيطية--echo-trail--outline-echo-stack)
- [`TYPE-66` نص مملوء بصورة أو فيديو](#type-66--نص-مملوء-بصورة-أو-فيديو--image---video-filled-text)
- [`TYPE-67` نص لزج متحول](#type-67--نص-لزج-متحول--gooey-morph-text)
- [`TYPE-68` حروف منفوخة بالفيزياء](#type-68--حروف-منفوخة-بالفيزياء--inflated-physics-letterforms)
- [`TYPE-69` جسيمات تتجمع لتكوّن كلمة](#type-69--جسيمات-تتجمع-لتكوّن-كلمة--particles-assemble-into-a-word)
- [`TYPE-70` خط الخلايا: ASCII ونقاط المصفوفة](#type-70--خط-الخلايا-ascii-ونقاط-المصفوفة--cell-based-type-ascii-blocks--dot-matrix-numerals)
- [`TYPE-71` كلمات مدمجة داخل اللقطة](#type-71--كلمات-مدمجة-داخل-اللقطة--words-embedded-in-footage-composition-craft)
- [`TYPE-72` نص على حلقات ومدارات](#type-72--نص-على-حلقات-ومدارات--text-rings--orbiting-words)
- [`TYPE-73` نفق النص ودوامته](#type-73--نفق-النص-ودوامته--circular-text-tunnel--spiral-vortex)
- [`TYPE-74` أسطوانة نص ثلاثية الأبعاد وشرائط حلزونية](#type-74--أسطوانة-نص-ثلاثية-الأبعاد-وشرائط-حلزونية--3d-text-cylinder--helix-ribbons)
- [`TYPE-75` جدار الشرائط المتعاكسة](#type-75--جدار-الشرائط-المتعاكسة--bidirectional-marquee-wall)
- [`TYPE-76` شريط مائل وجدار منظوري](#type-76--شريط-مائل-وجدار-منظوري--tilted-ticker-band--perspective-word-wall)
- [`TYPE-77` جدار نص يندفع وينضغط إلى شعار](#type-77--جدار-نص-يندفع-وينضغط-إلى-شعار--text-wall-rush--compress-into-a-logo)
- [`TYPE-78` كلمات كعمارة ودوران الأرباع](#type-78--كلمات-كعمارة-ودوران-الأرباع--words-as-architecture--quadrant-rotation)
- [`TYPE-79` عنوان سينمائي متباعد الحروف](#type-79--عنوان-سينمائي-متباعد-الحروف--letter-spaced-cinematic-title)
- [`TYPE-80` بطاقة عنوان هادئة وقفل الشعار](#type-80--بطاقة-عنوان-هادئة-وقفل-الشعار--calm-title-card--lockup)
- [`TYPE-81` بطاقات الفصول والأرقام الضخمة](#type-81--بطاقات-الفصول-والأرقام-الضخمة--numbered-chapter-blocks--giant-number-cards)
- [`TYPE-82` الشرائط السفلية ولوحات الأسماء](#type-82--الشرائط-السفلية-ولوحات-الأسماء--lower-thirds--name-plates)
- [`TYPE-83` أنظمة الأصوات الطباعية](#type-83--أنظمة-الأصوات-الطباعية--multi-voice-type-systems)
- [`TYPE-84` مظهر الترجمة حسب النبرة والعالم](#type-84--مظهر-الترجمة-حسب-النبرة-والعالم--caption-look-by-tone--theme)
- [`TYPE-85` تكديس هرمي بأحجام متدرجة](#type-85--تكديس-هرمي-بأحجام-متدرجة--size-stepped-hierarchy-stacks)
- [`TYPE-86` عنوان سيريف متراكب يُبنى كلمة كلمة](#type-86--عنوان-سيريف-متراكب-يُبنى-كلمة-كلمة--stacked-serif-title-build)
- [`TYPE-87` بطاقة حرف أو كلمة بملء الشاشة](#type-87--بطاقة-حرف-أو-كلمة-بملء-الشاشة--full-bleed-glyph--word-cards)
- [`TYPE-88` تجميع المعادلات](#type-88--تجميع-المعادلات--equation-assembly)
- [`TYPE-89` استايلات حركية في الكتالوج](#type-89--استايلات-حركية-في-الكتالوج--catalog-kinetic-styles-brutalist--minimal--typewriter)
- [`TYPE-90` تزويجات ولوحات جاهزة للعناوين](#type-90--تزويجات-ولوحات-جاهزة-للعناوين--preset-pairings--palettes-for-title-systems)
- [`TYPE-U01` خط Poppins مضمّن](#type-u01--خط-poppins-مضمّن--poppins-bundled-ofl)
- [`TYPE-U02` قواعد قراءة الترجمة فوق اللقطات](#type-u02--قواعد-قراءة-الترجمة-فوق-اللقطات--caption-readability-rules-over-footage)
- [`TYPE-X01` نص يعبر القطع](#type-x01--نص-يعبر-القطع--type-that-keeps-moving-through-cuts)
- [`TYPE-X02` ثلاث عائلات خطوط بمصدر واحد](#type-x02--ثلاث-عائلات-خطوط-بمصدر-واحد--three-font-families-from-one-source-of-truth)

## البطاقات / cards

### `TYPE-01` — مقاسات الخط للفيديو / Video type sizing & contrast

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** النص المرمَّز في الفيديو يحتاج حجمًا أكبر وتباينًا أقوى وتباعدًا أضيق من نص الويب. / Encoded-video type must be larger, higher-contrast and tighter than web type.

**متى:** قبل وضع أي عنوان أو ترجمة أو تسمية بيانات / before laying out any title, caption or data label.

**كيف:** At 1920 w: headline ≥60 px, body ≥20 px, data labels ≥16 px. At 1080 w: headline 84 px, support 44 px, safe area 80 px sides / 100 px top-bottom. Feed post 4:5 1080×1350: idea 72–120 px (read in 1 s), support 36–48 px (3 s), tertiary 24–28 px (never <24); data card number 120–200 px, meaning 36–44 px, source + date 24 px mandatory. B2B promo: 120 / 64 / 28 px, ≤7 words on screen. Weight contrast 300 vs 900 (not 400 vs 700); display tracking −0.03…−0.05em; on dark grounds body weight 350 and +0.05–0.1 line-height. Charts: web ticks 11 px / labels 12 / title 18 → ×2–2.5 for 1080p (ticks 24–28, labels 28–34, data lines ~4 px). Frosted glass: build hierarchy with casing, tracking and opacity (white .9 primary, .5 secondary, mono uppercase 11 px labels, weight ≤500).

**المعاملات:** ≥60/20/16 px @1920; 84/44 px @1080; feed 72–120/36–48/24–28; weights 300 vs 900; tracking −0.03…−0.05em

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** size · contrast · safe area · hierarchy · مقاسات · تباين · هوامش

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/typography.md`
- `kosif-atlas/skills/2712-remotion/10432-remotion-create/video-layout.md`
- `kosif-atlas/skills/2976-pwdev-social-media/12589-post-visual/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/references/svg-polish-and-crispness.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-02` ميزانية الكلمات والأسطر / Word & line budgets (on-screen copy ≠ narration) (documented)
- `TYPE-03` زمن القراءة والثبات / Read-time & hold rules (documented)

### `TYPE-02` — ميزانية الكلمات والأسطر / Word & line budgets (on-screen copy ≠ narration)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فكرة واحدة لكل شاشة، كلمات وأسطر محدودة، والنص الظاهر كلمة بطلة لا تكرار للتعليق الصوتي. / One idea per screen, capped words and lines; on-screen copy is a hero word, never a re-print of the narration.

**متى:** عند كتابة السكربت المرئي / when writing the on-screen script.

**كيف:** ≤7 words visible on 9:16, ≤12 on 16:9. Portrait lines 14–22 characters, broken at phrase boundaries; caption lines ~32–42 characters; body 45–75 ch (65 default), never >80 (eyes jump in 7–9-character saccades). A display face carries ≤~6 words. Visible MG copy is a hero word, stat or one-word emphasis (‘$83K’, ‘2x faster’, ‘INSTANT’); the caption track already prints the spoken words, so never double-print narration. Avoid AI tells: single-word accent styling in every headline, all-caps micro labels above every block.

**المعاملات:** ≤7 words 9:16; ≤12 words 16:9; 14–22 chars portrait; 32–42 chars caption; ≤6 words display

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** words per screen · line length · copy · ميزانية · طول السطر · نص قصير

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-tool/playbooks/kinetic-type.md:15`
- `kosif-one/vendor/hyperframes/skills/hyperframes/references/frame-worker-core.md`
- `kosif-atlas/skills/3438-ux-design/14126-web-typography/SKILL.md`
- `kosif-atlas/skills/1420-frontend-design-skills/3376-anthropic-frontend-design`

#### 7. قدرات قريبة في العائلة

- `TYPE-01` مقاسات الخط للفيديو / Video type sizing & contrast (documented)
- `TYPE-03` زمن القراءة والثبات / Read-time & hold rules (documented)
- `TYPE-04` سلّم الأحجام والأوزان والتباعد / Scale, weight, leading & tracking tokens (documented)

### `TYPE-03` — زمن القراءة والثبات / Read-time & hold rules

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كم كلمة في البطاقة وكم تبقى، وكيف يكون الخروج أقصر من الدخول. / How much text per card, how long it holds, and why exits are shorter than entrances.

**متى:** عند توقيت كل بطاقة نصية / when timing every text card.

**كيف:** 3–4 words per card (range 1–7); ~0.4 s per word and ≥0.5 s per card; a URL ≥1.7 s. A line stays readable ≥ 0.3 s + 0.06 s × characters after its last word lands; 3 s on screen must read in 2 s. Exits 200–300 ms ease-in cubic, 30 px opposite to the entrance — always shorter than entrances. Text rarely fades out alone; it leaves with its scene. \| code (js): const holdAfterLanding = (line) => 0.3 + 0.06 * line.length; // seconds const cardSeconds = (nWords) => Math.max(0.5, 0.4 * nWords);

**المعاملات:** 0.4 s/word; ≥0.5 s/card; URL ≥1.7 s; hold 0.3 s + 0.06 s × chars; exit 200–300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** timing · hold · read time · توقيت · زمن القراءة · ثبات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/references/craft-numbers.md`
- `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`
- `kosif-tool/playbooks/kinetic-type.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/typography.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-01` مقاسات الخط للفيديو / Video type sizing & contrast (documented)
- `TYPE-02` ميزانية الكلمات والأسطر / Word & line budgets (on-screen copy ≠ narration) (documented)
- `TYPE-04` سلّم الأحجام والأوزان والتباعد / Scale, weight, leading & tracking tokens (documented)
- `TYPE-05` اختيار الخط وتزويجه / Choosing & pairing faces (documented)

### `TYPE-04` — سلّم الأحجام والأوزان والتباعد / Scale, weight, leading & tracking tokens

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل الأحجام من أساس واحد ونسبة واحدة، مع سلم أوزان وتباعد أسطر وحروف حسب الدور. / All sizes from one base and ratio, plus a weight ladder and role-based leading and tracking.

**متى:** عند إنشاء ملف التوكنز لأي ستايل / when writing a style's token file.

**كيف:** Ratios 1.125 / 1.2 / 1.25 / 1.333 / 1.414 / 1.5 / 1.618; for 1080p video base 42–48 px with 1.333–1.618 for display (base 16 × 1.25 → 10, 13, 16, 20, 25, 31, 39, 49, 61). Fluid web stage: base clamp(1rem, 0.857rem + 0.714vw, 1.25rem), display clamp(3rem, 1.5rem + 6vw, 9rem), hero clamp(4rem, 2rem + 8vw, 12rem) — on fixed video stages compute once per aspect. Weights: 100/300 display only, 400 body, 500 labels, 600 headings, 700/900 display; most frames need 3 weights; define 4–6 ranks as (size, weight, leading). Leading: display 1.0–1.25, h3–h4 1.25–1.4, body 1.5–1.75, caption 1.4–1.6 (Arabic +0.1–0.2 for dots and harakat). Block gap 0.75–1 em beyond leading. Tracking: display −1…−3 %, small text +0.5–1 %, all caps +0.04–0.08em; Arabic letter-spacing always 0 (use width or kashida). Web snap: Tailwind steps 12–128 px with paired line-heights.

**المعاملات:** ratio 1.25–1.618; base 42–48 px @1080p; leading 1.0–1.25 display / 1.5–1.75 body; tracking −3 %…+0.08em; Arabic 0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** type scale · weight · leading · tracking · tokens · سلم الأحجام · الأوزان · تباعد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/1503-universal-design-principles/3823-hierarchy-typographic/SKILL.md`
- `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md`
- `kosif-atlas/skills/3438-ux-design/14124-top-design/references/typography.md`
- `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md:170`

#### 7. قدرات قريبة في العائلة

- `TYPE-02` ميزانية الكلمات والأسطر / Word & line budgets (on-screen copy ≠ narration) (documented)
- `TYPE-03` زمن القراءة والثبات / Read-time & hold rules (documented)
- `TYPE-05` اختيار الخط وتزويجه / Choosing & pairing faces (documented)
- `TYPE-06` أرقام جدولية وخصائص OpenType / Tabular numerals & OpenType features (documented)

### `TYPE-05` — اختيار الخط وتزويجه / Choosing & pairing faces

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر الخط من الغرض لا من الذوق، وزوّج خطين متباينين فقط، وافحص جودته قبل الاستخدام. / Choose type from purpose, not taste; pair at most two clearly different families; screen quality first.

**متى:** في بداية كل ستايل أو هوية / at the start of every style or identity.

**كيف:** Tone (legal/playful/luxury/tech) → class (serif/sans/slab/mono/display) → shortlist 3 → render a specimen frame with real copy at final size. Display face for moments (hooks, titles ≤6 words), workhorse for sustained text (captions, lower-thirds). Quality screen: even stroke, kerning pairs AV/To/Ty, full glyph set, regular/bold/italic, generous x-height, open apertures, distinct Il1/O0/rn (Arabic: dots, harakat, lam-alef). Max two families; pair by contrast — Playfair Display + Source Sans, Lora + Inter, Oswald + Merriweather, PT Serif + PT Sans; never near-twins (Helvetica + Arial) and never two sans. Bilingual superfamilies: IBM Plex Sans + IBM Plex Sans Arabic, Noto Sans + Noto Naskh/Kufi Arabic. Anti-monoculture: don't default to Inter/Roboto/Open Sans/Noto Sans/Arimo/Lato; one landing-page system prefers Geist/Manrope/Geist Mono/Poppins and forbids 900.

**المعاملات:** 2 families max; 3 shortlist; display ≤6 words

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pairing · font choice · superfamily · تزويج الخطوط · اختيار الخط · عائلة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/3438-ux-design/14126-web-typography/references/pairing-strategies.md`
- `kosif-atlas/skills/3438-ux-design/14126-web-typography/references/evaluating-typefaces.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/typography.md`
- `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md:152`

#### 7. قدرات قريبة في العائلة

- `TYPE-03` زمن القراءة والثبات / Read-time & hold rules (documented)
- `TYPE-04` سلّم الأحجام والأوزان والتباعد / Scale, weight, leading & tracking tokens (documented)
- `TYPE-06` أرقام جدولية وخصائص OpenType / Tabular numerals & OpenType features (documented)
- `TYPE-07` ملاءمة النص للعرض وقياسه / Fit-to-width & text measuring (install)

### `TYPE-06` — أرقام جدولية وخصائص OpenType / Tabular numerals & OpenType features

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أرقام متساوية العرض لكل عداد أو عمود أرقام متحرك، مع التحكم في الربط والمجموعات الأسلوبية. / Equal-width digits for every moving or stacked number, plus control of ligatures and stylistic sets.

**متى:** أي عداد أو لوحة نتائج أو جدول أرقام / any counter, scoreboard or number column.

**كيف:** font-variant-numeric: tabular-nums (or font-feature-settings 'tnum') so digits don't jitter while counting; keep 'kern' and 'liga' on; 'ss01'… stylistic sets for display. Check that the Arabic font has tabular Arabic-Indic digits; otherwise reserve a fixed-width box and right-align. MOTION.counter already sets tabular-nums (TYPE-37).

**المعاملات:** tnum on counters; kern/liga on; ss01 for display

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tabular · tnum · opentype · numbers · أرقام جدولية · عداد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/3438-ux-design/14126-web-typography/references/css-implementation.md`
- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/typography.md`
- `kosif-studio/motion/kit/motion-kit.js:227`

#### 7. قدرات قريبة في العائلة

- `TYPE-04` سلّم الأحجام والأوزان والتباعد / Scale, weight, leading & tracking tokens (documented)
- `TYPE-05` اختيار الخط وتزويجه / Choosing & pairing faces (documented)
- `TYPE-07` ملاءمة النص للعرض وقياسه / Fit-to-width & text measuring (install)
- `TYPE-08` نص SVG حاد وهالات التسميات / Crisp SVG text & label halos (documented)

### `TYPE-07` — ملاءمة النص للعرض وقياسه / Fit-to-width & text measuring

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** احسب أكبر حجم يُبقي النص الديناميكي داخل عرض محدد بدل كسر الأسطر يدويًا. / Compute the largest size that keeps a dynamic string inside a max width instead of hard line breaks.

**متى:** عناوين متغيرة الطول، قوالب، ترجمات / variable-length titles, templates, captions.

**كيف:** HyperFrames runtime: window.__hyperframes.fitTextFontSize(text, {fontFamily, fontWeight, maxWidth: 1600 (16:9) \| 900 (9:16), baseFontSize: 78, minFontSize: 42, step: 2}); measure without reflow with pretext.prepare(text, '700 90px Inter') → pretext.layout(prepared, maxWidth, lineHeight) → {lineCount, height}. Remotion: fitText({text, withinWidth, fontFamily, fontWeight}) and measureText() from @remotion/layout-utils, capped with Math.min(size, 80). Build the visible end state in static CSS first, then animate from/to it; no <br> in body text; transformed elements block-level and sized. Arabic: load the real shaping font before measuring.

**المعاملات:** maxWidth 1600/900; base 78; min 42; step 2

**التثبيت:** npm i @remotion/layout-utils@4.0.536 # MIT; or use the HyperFrames runtime via npx -y hyperframes@0.8.164

**الوسوم:** fit text · measure · autosize · ملاءمة · قياس النص

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`
- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/measuring-text.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/determinism-rules.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-05` اختيار الخط وتزويجه / Choosing & pairing faces (documented)
- `TYPE-06` أرقام جدولية وخصائص OpenType / Tabular numerals & OpenType features (documented)
- `TYPE-08` نص SVG حاد وهالات التسميات / Crisp SVG text & label halos (documented)
- `TYPE-09` تراخيص الخطوط ونظافتها / Font licensing & font hygiene (documented)

### `TYPE-08` — نص SVG حاد وهالات التسميات / Crisp SVG text & label halos

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قواعد تمنع المحاور الضبابية والمنحنيات المسننة وتفصل التسمية عن الخلفية المزدحمة. / Rules that stop blurry axes and jagged curves and lift labels off busy marks.

**متى:** مخططات وواجهات ونص SVG مُصيَّر / charts, UI and rendered SVG text.

**كيف:** shape-rendering: crispEdges only on axes, ticks, gridlines and rectangular cells; geometricPrecision for curves and circles; integer dimensions and a fixed viewBox; never scale a group that contains text (recompute positions); label halo = paint-order: stroke fill with a 2–3 px background-coloured stroke.

**المعاملات:** halo 2–3 px; crispEdges on axes only

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** svg · crisp · halo · labels · حدة · هالة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/references/svg-polish-and-crispness.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-06` أرقام جدولية وخصائص OpenType / Tabular numerals & OpenType features (documented)
- `TYPE-07` ملاءمة النص للعرض وقياسه / Fit-to-width & text measuring (install)
- `TYPE-09` تراخيص الخطوط ونظافتها / Font licensing & font hygiene (documented)
- `TYPE-10` حدود النص داخل صور الذكاء الاصطناعي / Text-in-AI-image ladder (key)

### `TYPE-09` — تراخيص الخطوط ونظافتها / Font licensing & font hygiene

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اعرف ما يحق لك تضمينه، ولا تعتمد على خطوط النظام التي تتبدل من جهاز لآخر. / Know what you may embed, and never rely on system fonts that alias differently per machine.

**متى:** قبل أي تسليم أو رندر على خادم / before any delivery or headless render.

**كيف:** OFL/Apache (most Google Fonts): self-host and commercial use OK. Adobe Fonts: no self-hosting, needs a subscription (catalogue search via the Adobe for creativity MCP tools font_search / font_recommend / font_preview is 🔑). Monotype web fonts are pageview-metered; a desktop licence is not a web licence. Record each family's licence class in the token file. Hygiene: every font-family needs an @font-face (HyperFrames lint rules font_family_without_font_face, system_font_will_alias; localise with hyperframes-localize-fonts). KOSIF Studio's Pillow painter maps sans → segoeui/arial/tahoma, serif → times/georgia, mono → consola/cour from %WINDIR%/Fonts and otherwise falls back to Pillow's default — so ship TTF/woff2 files for Linux renders.

**المعاملات:** OFL/Apache only for embedding; 1 @font-face per family

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** license · OFL · font-face · fallback · ترخيص · خطوط النظام

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/2248-brand-identity-studio/8558-brand-legal-and-licensing`
- `kosif-one/vendor/hyperframes/packages/lint/src/rules/fonts.ts`
- `kosif-studio/render.py:428`
- `kosif-atlas/skills/103-adobe-for-creativity/237-adobe-fonts/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-07` ملاءمة النص للعرض وقياسه / Fit-to-width & text measuring (install)
- `TYPE-08` نص SVG حاد وهالات التسميات / Crisp SVG text & label halos (documented)
- `TYPE-10` حدود النص داخل صور الذكاء الاصطناعي / Text-in-AI-image ladder (key)
- `TYPE-11` خطوط لاتينية مدمجة جاهزة / Owner-bundled Latin fonts (offline) (ready)

### `TYPE-10` — حدود النص داخل صور الذكاء الاصطناعي / Text-in-AI-image ladder

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Needs: an image-generation service (Gemini / Ideogram API key) |

**ما هي:** النماذج ترسم نصوصًا قصيرة فقط؛ كل ما هو أطول أو رقمي أو قابل للتعديل يُركَّب كنص حقيقي فوقها. / Image models draw only short strings; anything longer, numeric or editable is overlaid as real type.

**متى:** عند توليد صور أو خلفيات تحتوي نصًا / when generating images or plates that contain text.

**كيف:** Rung 1 (model-rendered): Gemini ≤25 characters and 2–3 phrases, Ideogram 3–5 words, labels ≤4 words, titles ≤8; isolate the string in its own line — Text (verbatim, render exactly, no extra characters): "Panel A" — give role and placement, quality high. Rung 2: SVG/HTML overlay for dense labels. Rung 3: real vector/plot type for numbers with units and equations. Video models cannot render readable text at all: generate clean plates and set the words with this chapter.

**المعاملات:** ≤25 chars (Gemini); 3–5 words (Ideogram); label ≤4; title ≤8 words

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ai image · text rendering · overlay · نص في الصورة · ذكاء اصطناعي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/2657-figures/10108-ai-full-figure`
- `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`
- `kosif-atlas/skills/1446-marketing-skills/3504-image`

#### 7. قدرات قريبة في العائلة

- `TYPE-08` نص SVG حاد وهالات التسميات / Crisp SVG text & label halos (documented)
- `TYPE-09` تراخيص الخطوط ونظافتها / Font licensing & font hygiene (documented)
- `TYPE-11` خطوط لاتينية مدمجة جاهزة / Owner-bundled Latin fonts (offline) (ready)
- `TYPE-12` تضمين الخطوط داخل الملف / Offline font inlining (base64) (ready)

### `TYPE-11` — خطوط لاتينية مدمجة جاهزة / Owner-bundled Latin fonts (offline)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | OFL-1.1 (licence texts ship beside the woff2 files). |

**ما هي:** خطوط لاتينية مرخّصة OFL موجودة في المستودعات وتعمل بلا إنترنت. / OFL Latin fonts already in the repos, working offline.

**متى:** أي رندر يحتاج ثباتًا بلا شبكة / any render that must be deterministic and offline.

**كيف:** Space Grotesk 500/700 (≈12.8–13.3 KB woff2) for display and marks; JetBrains Mono 500/700 (≈21.8–22 KB) for HUD, code and stats; Montserrat 600/700/800 for Latin wordmarks (800 with letter-spacing .02–.09em; stack "Montserrat", "IBM Plex Sans Arabic", -apple-system, "Segoe UI", sans-serif); Cairo latin 600/800 woff2 plus Cairo[slnt,wght].ttf variable in this skill's proofs/_shared/fonts. HUD recipe (bunny_twin): Grotesk 30 px bar mark; Mono stat value 50 px/700, tabular-nums, letter-spacing .06–.14em; keys 17–23 px; chip 21 px/700. \| code (css): @font-face { font-family: Grotesk; font-weight: 700; src: url(assets/fonts/space-grotesk-latin-700-normal.woff2) format('woff2'); } @font-face { font-family: Mono; font-weight: 500; src: url(assets/fonts/jetbrains-mono-latin-500-normal.woff2) format('woff2'); } .stat { font: 700 50px Mono; font-variant-numeric: tabular-nums; letter-spacing: .08em; }

**المعاملات:** Space Grotesk 500/700; JetBrains Mono 500/700; Montserrat 600–800; Cairo latin 600/800

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** fonts · space grotesk · jetbrains mono · montserrat · خطوط مدمجة · HUD

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/kit/fonts/OFL-SpaceGrotesk.txt`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:16`
- `kosif-earth-ci-fork/ui/ds/fonts.css`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts`

#### 7. قدرات قريبة في العائلة

- `TYPE-09` تراخيص الخطوط ونظافتها / Font licensing & font hygiene (documented)
- `TYPE-10` حدود النص داخل صور الذكاء الاصطناعي / Text-in-AI-image ladder (key)
- `TYPE-12` تضمين الخطوط داخل الملف / Offline font inlining (base64) (ready)
- `TYPE-13` مجموعة Google Fonts للتبديل الحي / Curated Google Fonts swap set (ready)

### `TYPE-12` — تضمين الخطوط داخل الملف / Offline font inlining (base64)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | OFL-1.1 fonts, but the licence texts are not shipped beside them — add them to any deliverable. Vendored GSAP = GSAP standard ‘no charge’ licence. |

**ما هي:** حقن الخطوط كـ base64 داخل المشروع ليُرندر بلا أي طلب شبكة. / Inline fonts as base64 so the project renders with zero network requests.

**متى:** ترجمات وأفلام تُرندر على خوادم بلا إنترنت / captions and films rendered on offline servers.

**كيف:** node scripts/inject-fonts.cjs <project> (embedded-captions) inlines latin-subset woff2 — 44 faces / 24 families, ~875 KB: Anton, Audiowide, Baloo 2, Bangers, Bodoni Moda, Caveat, Chakra Petch, Cinzel, Cormorant Garamond, Creepster, Fredoka, Inter, Monoton, Orbitron, Permanent Marker, Press Start 2P, Rajdhani, Saira Stencil One, Shippori Mincho, Sora…; char-widths.json supports measuring. The HyperFrames compiler (📦) auto-embeds Inter, Roboto, Lato, Nunito, Montserrat, Poppins, Outfit, Playfair Display 400/700/900, Open Sans, Oswald, EB Garamond, Space Mono, IBM Plex Mono, JetBrains Mono, Source Code Pro, League Gothic, Archivo Black. talking-head-recut bundles Caveat 400/700, Inter 400/700, Virgil (hand) + a vendored gsap.min.js. Latin subsets only — Arabic needs its own files.

**المعاملات:** 24 families / 44 faces / ~875 KB latin subset

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** base64 · inline fonts · offline · captions · تضمين الخطوط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/inject-fonts.cjs`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/modes/standard/fonts/fonts.css`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/assets/fonts/char-widths.json`
- `kosif-one/vendor/hyperframes/skills/talking-head-recut/assets/fonts/Virgil.woff2`

#### 7. قدرات قريبة في العائلة

- `TYPE-10` حدود النص داخل صور الذكاء الاصطناعي / Text-in-AI-image ladder (key)
- `TYPE-11` خطوط لاتينية مدمجة جاهزة / Owner-bundled Latin fonts (offline) (ready)
- `TYPE-13` مجموعة Google Fonts للتبديل الحي / Curated Google Fonts swap set (ready)
- `TYPE-14` صعود من خلف خط القاعدة / Baseline mask rise (lines & words) (ready)

### `TYPE-13` — مجموعة Google Fonts للتبديل الحي / Curated Google Fonts swap set

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | OFL (Google Fonts). |

**ما هي:** صفحة المراجعة تحمّل سبع عائلات لاتينية للتبديل الحي بين الخطوط أثناء المعاينة. / The review page loads seven Latin families for live font swaps during preview.

**متى:** عند تجربة الخطوط مع المالك / when auditioning faces with the owner.

**كيف:** Style → Fonts swaps between Bricolage Grotesque 500/700/800 · Inter Tight 600/800 · Instrument Serif · Space Grotesk 500/700 · DM Sans 400/500/700 · Inter 400/500/600 · Geist 400–700 (+ Geist Mono 400/500 for UI). Loaded from fonts.googleapis.com (reachable from this container); after choosing, self-host the files (raw.githubusercontent.com/google/fonts is reachable) so the final render needs no network.

**المعاملات:** 7 families; Geist + Geist Mono

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** google fonts · geist · font swap · خطوط جوجل · تبديل الخط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:9`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:336`
- `kosif-atlas/skills/2722-vercel/10536-geist/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-11` خطوط لاتينية مدمجة جاهزة / Owner-bundled Latin fonts (offline) (ready)
- `TYPE-12` تضمين الخطوط داخل الملف / Offline font inlining (base64) (ready)
- `TYPE-14` صعود من خلف خط القاعدة / Baseline mask rise (lines & words) (ready)
- `TYPE-15` صعود من حالة جزئية / Rise from a partial state (riseWords) (ready)

### `TYPE-14` — صعود من خلف خط القاعدة / Baseline mask rise (lines & words)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard ‘no charge’ licence (vendored gsap.min.js) — fine for client work, not for tools that compete with GSAP. |

**ما هي:** الأسطر أو الكلمات تصعد من قناع تحت خط قاعدتها — أنظف كشف فاخر، والكلمة العربية تبقى متصلة. / Lines or words rise out of a clip under their baseline — the cleanest premium reveal; Arabic words stay joined.

**متى:** العناوين والاقتباسات والسطور الداعمة / headlines, quotes, supporting lines.

**كيف:** MOTION.maskRise(tl, els, at, {dur: 0.5, stagger: 0.08, out, outDur: 0.27}) sets clip-path inset(-0.1em -0.1em 0 -0.1em) and tweens yPercent 110 → 0 with E.out = cubic-bezier(.16,1,.3,1); exit yPercent −110 in 0.27 s with E.in (.7,0,.84,0) at half the stagger. Per word: MOTION.revealWords(tl, el, at, {dur: 0.7, stagger: 0.07, from: 'top'\|'bottom'}) wraps each word in a mask (padding .06em .04em .18em) and slides yPercent ±115 → 0 with expo.out; MOTION.hideWords exits in 0.45 s, stagger 0.04. Seen: per-word line mask 250 ms/word, stagger 80 ms, cubic-bezier(.2,.8,.2,1), second line muted grey (pm-palashbagchi11-0a4b6b); letters 350 ms power3.out, stagger 40–60 ms above a drawn rule (pm-1littlecoder-9fef89). Web split-text: words y 100 % stagger 0.05, 0.8 s expo.out; Latin chars y 100 stagger 0.02; title words y 120 stagger 0.1, 1.2 s. Masks need ≥0.2em padding so descenders and diacritics don't clip. Engine: python3 scripts/kmotion.py new NAME --seconds 10 (flat HTML + GSAP + motion-kit) → kmotion frames → kmotion render.

**المعاملات:** yPercent 110→0; 0.5 s; stagger 0.08 s; exit −110 in 0.27 s; words ±115, 0.7 s, stagger 0.07

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mask · reveal · baseline · split text · قناع · كشف · صعود

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/kit/motion-kit.js:184`
- `kosif-studio/motion/kit/motion-kit.js:156`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:184`
- `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-12` تضمين الخطوط داخل الملف / Offline font inlining (base64) (ready)
- `TYPE-13` مجموعة Google Fonts للتبديل الحي / Curated Google Fonts swap set (ready)
- `TYPE-15` صعود من حالة جزئية / Rise from a partial state (riseWords) (ready)
- `TYPE-16` ظهور من الضباب (سحب البؤرة) / Blur-to-sharp focus pull (install)

### `TYPE-15` — صعود من حالة جزئية / Rise from a partial state (riseWords)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard ‘no charge’ licence (vendored gsap.min.js) — fine for client work, not for tools that compete with GSAP. |

**ما هي:** الكلمات تصل من شفافية 40% مع صعود صغير وضباب يتلاشى مبكرًا ثم تستقر — وصول «فيلم الإطلاق الفاخر». / Words arrive from 40 % opacity with a small rise and early-clearing blur — the premium launch-film arrival.

**متى:** سطور هادئة، شعارات، نهايات / calm lines, taglines, end cards.

**كيف:** MOTION.riseWords(tl, el, at, {rise: 26, blur: 6, dur: 0.4, stagger: 0.1}) → y 26 px, opacity 0.4, blur 6 px → 0, ease E.out. Craft range: arrivals from 40 % opacity, 6–120 px rise, blur 4–12 px clearing by 60 % of the move. Reads calmer than a fade from zero; whole words, so Arabic-safe.

**المعاملات:** y 26 px; opacity .4→1; blur 6→0 px; 0.4 s; stagger 0.1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** rise · blur · premium · صعود · ضباب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/kit/motion-kit.js:175`
- `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:175`
- `kosif-studio/motion/references/craft-numbers.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-13` مجموعة Google Fonts للتبديل الحي / Curated Google Fonts swap set (ready)
- `TYPE-14` صعود من خلف خط القاعدة / Baseline mask rise (lines & words) (ready)
- `TYPE-16` ظهور من الضباب (سحب البؤرة) / Blur-to-sharp focus pull (install)
- `TYPE-17` إضاءة الكلمات بترتيب القراءة / Reading-order light-up & blur manifesto (seen)

### `TYPE-16` — ظهور من الضباب (سحب البؤرة) / Blur-to-sharp focus pull

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** كل كلمة تتضح من ضبابية مضبوطة إلى حدة كاملة، كأن العدسة تسحب البؤرة. / Each word resolves from controlled blur to crisp, like a lens pulling focus.

**متى:** شعارات ونصوص مقتبسة وغنائية / taglines, quotes, lyrics.

**كيف:** Per word: filter blur(B) → 0, opacity 0 → 1, small y/x offset → 0; keep ≤ ~12 live-blurred elements at once (for paragraphs see TYPE-17). Zero-install fallback: TYPE-15 with blur 12–20. Ready-mades: blur-in (size 52, 24–120; tone strong\|muted\|accent; align), soft-blur-in (distance close\|standard\|far; direction up\|down; blur soft\|standard\|heavy), focus-blur-resolve (heavy blur → crisp → soft blur-out), per-word-rise (IN 1.45 s, OUT 0.50 s, split word\|char, cues lock landings to narration), per-word-crossfade (calm keynote drift), blur-out-up (exit: blur grows while leaving up\|down\|left\|right). \| 20 px · – · 400 ms · 120 ms · ease-out · pm-danilowm-d3720d ; 20 px · y 20 · 450 ms · 80 ms · easeOutCubic · pm-sudo-kiran-4f8b59 ; 16 px · y 8 · 300 ms · 120 ms · power2.out · pm-viktoroddy-98c1d8 ; 12 px · x 10 · 350 ms · 90 ms · pm-robj3d3-b18fad ; 12 px · – · 500 ms · ease-out (second word italic) · pm-gabrielbuzziv-4ff0c6 ; 8 px · y 6 · 220 ms at each vocal onset · cubic-bezier(.2,.9,.2,1); next word waits blurred · pm-samaote-5e2fc2 ; 6 px (from 30 % opacity) · – · stagger 120 ms · pm-tstfully-0aa6b4 ; 4 px · y 24 · clears in 180 ms · letters 30–40 ms · brief pm-samuel-spitz-974923

**المعاملات:** blur 4–20 px; 220–500 ms; stagger 80–120 ms

**التثبيت:** npx -y hyperframes@0.8.164 add blur-in # also soft-blur-in, focus-blur-resolve, per-word-rise, per-word-crossfade, blur-out-up

**الوسوم:** blur · focus · reveal · ضباب · بؤرة · وضوح

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/blur-in/blur-in.html`
- `kosif-one/vendor/hyperframes/registry/components/focus-blur-resolve/focus-blur-resolve.html`
- `kosif-one/vendor/hyperframes/registry/components/per-word-rise/per-word-rise.html`
- `style:pm-samaote-5e2fc2`

#### 7. قدرات قريبة في العائلة

- `TYPE-14` صعود من خلف خط القاعدة / Baseline mask rise (lines & words) (ready)
- `TYPE-15` صعود من حالة جزئية / Rise from a partial state (riseWords) (ready)
- `TYPE-17` إضاءة الكلمات بترتيب القراءة / Reading-order light-up & blur manifesto (seen)
- `TYPE-18` تتابع الحروف سقوطًا وصعودًا / Per-letter drop & rise cascades (install)

### `TYPE-17` — إضاءة الكلمات بترتيب القراءة / Reading-order light-up & blur manifesto

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | The landing-page motion.ts that does the scroll light-up ships with no licence — rebuild it, never copy it. |

**ما هي:** فقرة كاملة باهتة تضيء كلماتها بالترتيب مع القراءة أو مع الصوت. / A whole dim paragraph lights up word by word in reading order or on speech onsets.

**متى:** بيانات، اقتباسات طويلة، نصوص صوتية / manifestos, long quotes, voice-led text.

**كيف:** Set the paragraph at 25–35 % opacity (or grey #bcbcba); words go to 100 % in reading order (lit = round(progress × words)) or at their words.json start. Grey-to-ink sequence .25 → 1 (pm-prasad-pilla-2c0cba). Manifesto variant: stack a pre-blurred ghost layer (6–10 px) under the sharp layer and animate only opacity/transform — never live blur on dozens of words; key words become filled pills; measure 960–1080 px, text-wrap: balance.

**المعاملات:** dim 25–35 %; ghost blur 6–10 px; measure 960–1080 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** light-up · paragraph · manifesto · إضاءة الكلمات · فقرة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-prasad-pilla-2c0cba`
- `kosif-atlas/skills/100-ui-motion/210-scroll-blur-manifesto`
- `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md:341`

#### 7. قدرات قريبة في العائلة

- `TYPE-15` صعود من حالة جزئية / Rise from a partial state (riseWords) (ready)
- `TYPE-16` ظهور من الضباب (سحب البؤرة) / Blur-to-sharp focus pull (install)
- `TYPE-18` تتابع الحروف سقوطًا وصعودًا / Per-letter drop & rise cascades (install)
- `TYPE-19` تبعثر وتدحرج وتجميع / Scatter, tumble & gravity assemble (install)

### `TYPE-18` — تتابع الحروف سقوطًا وصعودًا / Per-letter drop & rise cascades

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** حروف الكلمة اللاتينية تسقط أو تصعد إلى خط القاعدة بتتابع متداخل. / A Latin word's letters drop or rise onto the baseline in an overlapping stagger.

**متى:** شعارات قصيرة وعناوين ≤12 حرفًا (لاتيني فقط) / short wordmarks and ≤12-glyph titles (Latin only).

**كيف:** Split into letter spans (never Arabic); each letter from y ±(60 px…120 %) to 0. Rule: letters 40 ms stagger + 12 px offset, never opacity alone (brief pm-jasonzhou1993-8595e0 — Inter / IBM Plex Sans Arabic 500/800). Ready-mades: bottom-up-letters (unit letter\|word, direction up\|down, travel close\|standard\|far), top-down-letters (pronounced staircase, no blur), music primitive kinetic-letter-in (downbeat/phrase, 0.4–1.2 s). \| y −120 % · back.out(1.6) · 400 ms · 45 ms (overlap) · final period pops into a blue dot · pm-chatgptastra-0d95c7 ; y −60 px · back.out · 45 ms · Anton 800 caps, coloured dot pop · pm-himanshutwtxs-5f4b43 ; rotateX ~60°, y −40, blur 8 · ease-out · 350 ms · 25–35 ms · second line coloured · pm-ceowinkz-7c776b ; y +60 %, rotate 8–12° · circ.out · 500 ms · 22 ms · red underline wipes in after · pm-grace-sunnyy-29bc61 ; y offset · spring · 50 ms · wordmark bounce · pm-amol909s-27533e ; y −100 %, vertical blur decaying · expo.out · 200 ms · 80 ms · directional blur · pm-web3wesley-7bb108, pm-eyishazyer-af035b

**المعاملات:** stagger 22–80 ms; 200–500 ms; ≤12 glyphs

**التثبيت:** npx -y hyperframes@0.8.164 add bottom-up-letters # also top-down-letters

**الوسوم:** letters · stagger · drop · حروف · تتابع · سقوط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/bottom-up-letters/bottom-up-letters.html`
- `kosif-one/vendor/hyperframes/registry/components/top-down-letters/top-down-letters.html`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/kinetic-letter-in/scene.html`
- `style:pm-chatgptastra-0d95c7`

#### 7. قدرات قريبة في العائلة

- `TYPE-16` ظهور من الضباب (سحب البؤرة) / Blur-to-sharp focus pull (install)
- `TYPE-17` إضاءة الكلمات بترتيب القراءة / Reading-order light-up & blur manifesto (seen)
- `TYPE-19` تبعثر وتدحرج وتجميع / Scatter, tumble & gravity assemble (install)
- `TYPE-20` تقارب الحروف / Tracking-in collapse (Latin only) (install)

### `TYPE-19` — تبعثر وتدحرج وتجميع / Scatter, tumble & gravity assemble

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** كل حرف يبدأ في موضع ودوران عشوائيين مُبذَّرين ثم يرتطم بمكانه، أو يسقط بالجاذبية على خط. / Glyphs start at seeded random offsets/rotations and slam home, or fall with gravity onto a line.

**متى:** افتتاحيات طاقية وشعارات مرحة / energetic openers, playful wordmarks.

**كيف:** Each glyph from a seeded random offset/rotation to rest with easeOutBack plus per-frame motion blur: ±300 px, ±25°, stagger 40 ms, 500 ms (pm-leonkohli-6dc01b); ±60° tumble, stagger 30–40, then stacked offset shadows 4 px & 8 px in two accents (pm-ik-builds-b8bdcf); rotateZ/Y −40° + drop shadow, stagger 70 (pm-sudo-kiran-49176d); gravity drop 30–60 px, ±25°, stagger 40, contrasted with a calm italic serif word (pm-levabashidze-2d713a); signature letters fall 500 ms bounce-lite with irregular 60–120 ms stagger onto a visible grid baseline (pm-fionntobin-97b7af); a letter falls onto notebook rules (pm-lexnlin-038035). Vortex variant: each glyph on a polar spiral (r, θ) around its target, animate r → 0 and θ → 0 with rotation and motion blur, stagger 30 ms, ~700 ms ease-out (pm-1littlecoder-9fef89). Ready-made char-slam-explode: seeded scatter hold → overshooting slam + 3-frame landing shake (spread tight\|wild). \| code (js): const r = MOTION.rng(7); // seeded: identical every render letters.forEach((el, i) => tl.from(el, { x: (r() * 2 - 1) * 300, y: (r() * 2 - 1) * 300, rotation: (r() * 2 - 1) * 25, opacity: 0, duration: 0.5, ease: "back.out(1.6)" }, at + i * 0.04));

**المعاملات:** ±300 px; ±25°; stagger 30–120 ms; 500–700 ms; 3-frame shake

**التثبيت:** npx -y hyperframes@0.8.164 add char-slam-explode

**الوسوم:** scatter · assemble · gravity · vortex · تبعثر · تجميع · جاذبية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/char-slam-explode/char-slam-explode.html`
- `style:pm-leonkohli-6dc01b`
- `style:pm-fionntobin-97b7af`
- `style:pm-1littlecoder-9fef89`

#### 7. قدرات قريبة في العائلة

- `TYPE-17` إضاءة الكلمات بترتيب القراءة / Reading-order light-up & blur manifesto (seen)
- `TYPE-18` تتابع الحروف سقوطًا وصعودًا / Per-letter drop & rise cascades (install)
- `TYPE-20` تقارب الحروف / Tracking-in collapse (Latin only) (install)
- `TYPE-21` تكديس الأسطر ودفعها وتبديلها / Line stack, push & swap (install)

### `TYPE-20` — تقارب الحروف / Tracking-in collapse (Latin only)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** المسافة بين الحروف تنكمش من واسعة إلى نهائية أثناء الظهور — لمسة فخامة. / Letter-spacing collapses from wide to final as the heading appears — a premium touch.

**متى:** عناوين فاخرة وبطاقات علامة لاتينية / premium headings, Latin brand cards.

**كيف:** Playbook: +0.08em → 0 over 600 ms. Briefs: +8 % → 0 over 400 ms (pm-ajith-io-ea7f2d); +0.2em → 0 over 400 ms with a 180 px grotesk over a 36 px mono (pm-tolgayhickiran-e90799); letter stagger 60 ms with tracking +8 → 0 on settle, ≤12 glyphs (pm-mrtanviir-132457). Combined with a wght 200 → 800 sweep, 800 ms (pm-sahildesigner23-ee3155). HyperFrames tracking-in: tracking tight (0.6×)\|standard\|wide (1.8×), rise subtle 4 px\|standard 8 px\|bold 18 px, tone inherit\|ink\|paper\|accent. Never on Arabic — it breaks joining; use width/kashida or a word mask.

**المعاملات:** +0.08em→0 / 600 ms; +0.2em→0 / 400 ms; rise 4–18 px

**التثبيت:** npx -y hyperframes@0.8.164 add tracking-in

**الوسوم:** tracking · letter-spacing · premium · تباعد · تقارب الحروف

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/tracking-in/tracking-in.html`
- `kosif-tool/playbooks/kinetic-type.md:32`
- `kosif-tool/styles/pm-tolgayhickiran-e90799/BRIEF.md`
- `kosif-tool/styles/pm-mrtanviir-132457/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-18` تتابع الحروف سقوطًا وصعودًا / Per-letter drop & rise cascades (install)
- `TYPE-19` تبعثر وتدحرج وتجميع / Scatter, tumble & gravity assemble (install)
- `TYPE-21` تكديس الأسطر ودفعها وتبديلها / Line stack, push & swap (install)
- `TYPE-22` الدخول الشلالي / Waterfall entry cascade (documented)

### `TYPE-21` — تكديس الأسطر ودفعها وتبديلها / Line stack, push & swap

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** الأسطر تتكدس وتدفع بعضها وتتبادل الأماكن على نفس الضربة. / Lines stack, push each other up and swap places on the same beat.

**متى:** قوائم، جمل متتالية، مقارنة قبل/بعد / lists, running sentences, before/after statements.

**كيف:** Stack-and-replace (playbook C): three short lines stack downward 120 ms apart; on the next phrase the stack slides up 80 px, the top line exits and the new line enters at the bottom, 350 ms total. Stacked push: each new line slides from below in 400 ms expo-out while older lines move up one line-height (pm-hqmank-7c61f1). Line swap: line A exits up through an overflow mask as line B rises on the same beat (swap_at 1.5 s), optional accent underline under one word (underline_word). Line-by-line slide: lines enter from the left in stagger and exit right (size compact\|standard\|display, density fine\|standard\|coarse).

**المعاملات:** 120 ms apart; slide 80 px; 350 ms; push 400 ms expo-out; swap_at 1.5 s

**التثبيت:** npx -y hyperframes@0.8.164 add line-swap # also line-by-line-slide

**الوسوم:** stack · push · line swap · تكديس · تبديل السطر

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-tool/playbooks/kinetic-type.md:49`
- `kosif-one/vendor/hyperframes/registry/components/line-swap/line-swap.html`
- `kosif-one/vendor/hyperframes/registry/components/line-by-line-slide/line-by-line-slide.html`
- `style:pm-hqmank-7c61f1`

#### 7. قدرات قريبة في العائلة

- `TYPE-19` تبعثر وتدحرج وتجميع / Scatter, tumble & gravity assemble (install)
- `TYPE-20` تقارب الحروف / Tracking-in collapse (Latin only) (install)
- `TYPE-22` الدخول الشلالي / Waterfall entry cascade (documented)
- `TYPE-23` بناء من المركز / Kinetic center build (install)

### `TYPE-22` — الدخول الشلالي / Waterfall entry cascade

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عناصر تندفع من الأسفل وكل واحد يبدأ قبل أن يستقر سابقه، بظهور ثنائي بلا تلاشٍ. / Elements whip in from below, each starting before the previous settles, with binary (unfaded) opacity.

**متى:** قوائم سريعة ولقطات مزدحمة / fast lists and dense frames.

**كيف:** Binary opacity via tl.set — never fade an arrival. By density (loose / medium / dense): Y offset 60–80 / 40–50 / 30–48 px; duration 0.16–0.20 / 0.13–0.16 / 0.10–0.13 s; ease power4.out (expo.out for snap); never .inOut on an entry. One paused GSAP timeline, fromTo with explicit states, transforms/opacity only.

**المعاملات:** y 30–80 px; 0.10–0.20 s; power4.out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** waterfall · cascade · list · شلالي · قائمة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/waterfall-entry.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-20` تقارب الحروف / Tracking-in collapse (Latin only) (install)
- `TYPE-21` تكديس الأسطر ودفعها وتبديلها / Line stack, push & swap (install)
- `TYPE-23` بناء من المركز / Kinetic center build (install)
- `TYPE-24` مسح الكلمة الكبيرة بالقناع / Clip-path big-word wipe (documented)

### `TYPE-23` — بناء من المركز / Kinetic center build

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | MIT component; GSAP standard licence for the gsap it loads. |

**ما هي:** الكلمات تدخل من اليمين وتدفع العبارة النامية يسارًا حتى يستقر السطر الأخير في المنتصف. / Words enter from the right and shove the growing phrase left until the final line sits centred.

**متى:** شعار يُبنى كلمة كلمة / taglines built word by word.

**كيف:** Vars: font_size 72 (36–160), entry_offset 88 (20–160), font_weight 500\|600\|700\|800, color #171717, Geist from Google Fonts. Arabic mirror: enter from the left and shove right, whole words.

**المعاملات:** 72 px; entry_offset 88; weight 500–800

**التثبيت:** npx -y hyperframes@0.8.164 add kinetic-center-build

**الوسوم:** center build · push · phrase · بناء من المركز

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/kinetic-center-build/kinetic-center-build.html`

#### 7. قدرات قريبة في العائلة

- `TYPE-21` تكديس الأسطر ودفعها وتبديلها / Line stack, push & swap (install)
- `TYPE-22` الدخول الشلالي / Waterfall entry cascade (documented)
- `TYPE-24` مسح الكلمة الكبيرة بالقناع / Clip-path big-word wipe (documented)
- `TYPE-25` كشف بالشرائح / Strip-slice letter reveal (seen)

### `TYPE-24` — مسح الكلمة الكبيرة بالقناع / Clip-path big-word wipe

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة واحدة ضخمة تُكشف بمسح قناع باتجاه القراءة، تثبت، ثم تُمسح في الاتجاه نفسه. / One huge word revealed by a clip-path wipe in reading direction, held, then wiped out the same way.

**متى:** كلمة مفتاحية، نهاية علامة / a keyword moment, brand end card.

**كيف:** Playbook D: a 200 px word wiped in over 450 ms (ease-out quart), held 1 s, wiped out the same direction in 250 ms; mask wipes 350–500 ms in reading direction (L→R Latin, R→L Arabic). Brand end card: 3–4 lines, no invented tagline, revealed by a horizontal mask, not typing; name the substitute face if the brand font is missing. \| code (css): .word { clip-path: inset(0 100% 0 0); } /* Latin: tween to inset(0 0 0 0) in 450 ms, cubic-bezier(.25,1,.5,1) */ /* hold 1 s, then exit to inset(0 0 0 100%) in 250 ms — same direction; Arabic: mirror the insets */

**المعاملات:** 200 px; in 450 ms; hold 1 s; out 250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** wipe · clip-path · mask · مسح · قناع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-tool/playbooks/kinetic-type.md:51`
- `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-22` الدخول الشلالي / Waterfall entry cascade (documented)
- `TYPE-23` بناء من المركز / Kinetic center build (install)
- `TYPE-25` كشف بالشرائح / Strip-slice letter reveal (seen)
- `TYPE-26` بناء الكلمة على شبكة إنشائية / Construction-grid & guide-line build (seen)

### `TYPE-25` — كشف بالشرائح / Strip-slice letter reveal

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حروف عملاقة مقسومة إلى شرائح أفقية مزاحة تنتظم لتكوّن الكلمة. / Giant letters cut into horizontal strips, each offset in x, that align into the word.

**متى:** افتتاحيات جريئة / bold openers.

**كيف:** N clones of the word, each clipped with clip-path inset(top% 0 bottom% 0) to one strip; tween each strip x ±80 → 0 with 40 ms stagger; remove clones after alignment.

**المعاملات:** stagger 40 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** slice · strips · شرائح

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-lukasersil-0ed38e`

#### 7. قدرات قريبة في العائلة

- `TYPE-23` بناء من المركز / Kinetic center build (install)
- `TYPE-24` مسح الكلمة الكبيرة بالقناع / Clip-path big-word wipe (documented)
- `TYPE-26` بناء الكلمة على شبكة إنشائية / Construction-grid & guide-line build (seen)
- `TYPE-27` عنوان قماشي من 1–4 كلمات مع اتجاه تلقائي / Canvas 1–4-word headline with auto-RTL (ready)

### `TYPE-26` — بناء الكلمة على شبكة إنشائية / Construction-grid & guide-line build

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خطوط إرشاد الطباعة ترسم نفسها ثم تصطف الحروف عليها. / Type guide lines draw themselves, then the letters snap onto them.

**متى:** شرح شعار أو خط، هويات تقنية / logo or type explainers, technical identities.

**كيف:** Thin guides (baseline, x-height, cap, ascender, stems) draw in at 30–40 % white, 1 px, ~300 ms each (600 ms total), with red end dots and italic serif labels at the right; letters appear one by one aligned to them; guides fade.

**المعاملات:** 1 px at 30–40 %; 300–600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** grid · guides · construction · شبكة · خطوط إرشاد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-1littlecoder-9fef89`
- `style:pm-vanshwtfff-db0466`

#### 7. قدرات قريبة في العائلة

- `TYPE-24` مسح الكلمة الكبيرة بالقناع / Clip-path big-word wipe (documented)
- `TYPE-25` كشف بالشرائح / Strip-slice letter reveal (seen)
- `TYPE-27` عنوان قماشي من 1–4 كلمات مع اتجاه تلقائي / Canvas 1–4-word headline with auto-RTL (ready)
- `TYPE-28` موجة الحروف / Per-letter sine bounce & wave (seen)

### `TYPE-27` — عنوان قماشي من 1–4 كلمات مع اتجاه تلقائي / Canvas 1–4-word headline with auto-RTL

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان قصير يتلاشى ويصعد إلى مكانه على Canvas ويتحول تلقائيًا إلى RTL عند وجود العربية. / A short bold canvas headline that fades and rises into place and flips to RTL for Arabic.

**متى:** مشاهد تحريرية مرسومة على Canvas / canvas-painted editorial scenes.

**كيف:** headline = words.slice(0, 4); ctx.font = '900 {0.114 w}px Arial, Tahoma'; alpha = clamp((local − 0.58) / 0.55) × exit; y = 0.735 h + (1 − easeOutCubic(p)) × 0.065 h over 0.65 s; maxWidth 0.84 w; ctx.direction = 'rtl' when /[\u0600-\u06ff]/ matches. Pure function of local time, so seekable. Arial/Tahoma are system fonts — load a real font for Linux renders (TYPE-09).

**المعاملات:** start 0.58 s; fade 0.55 s; rise 6.5 % h; 11.4 % w

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** canvas · headline · rtl · عنوان · اتجاه تلقائي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `fastify-motion-bro/web/editorial.js:72-79`

#### 7. قدرات قريبة في العائلة

- `TYPE-25` كشف بالشرائح / Strip-slice letter reveal (seen)
- `TYPE-26` بناء الكلمة على شبكة إنشائية / Construction-grid & guide-line build (seen)
- `TYPE-28` موجة الحروف / Per-letter sine bounce & wave (seen)
- `TYPE-29` مفردات حركة النص للستوري بورد / Text-motion vocabulary for storyboards (documented)

### `TYPE-28` — موجة الحروف / Per-letter sine bounce & wave

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حروف العنوان تقفز على خط القاعدة في موجة متتابعة. / Headline letters bounce on the baseline in a travelling wave.

**متى:** حلقات مرحة، إيقاع موسيقي خفيف / playful loops, light music beds.

**كيف:** y_i(t) = −A·\|sin(ω t + i φ)\| with A 12 px, φ 0.4 rad, ω 8 rad/s on white bold uppercase over the scene (pm-ajith-io-4c248f). Vocabulary ‘wave’ = letters stagger 0.04 s; for held notes use the text-wave-distort primitive (1.0–2.5 s, 📦). \| code (js): const bounce = (t, i, A = 12, w = 8, phi = 0.4) => -A * Math.abs(Math.sin(w * t + i * phi)); letters.forEach((el, i) => { el.style.transform = `translateY(${bounce(t, i)}px)`; });

**المعاملات:** A 12 px; φ 0.4 rad; ω 8 rad/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** wave · bounce · loop · موجة · قفز

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-ajith-io-4c248f`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/text-wave-distort/scene.html`
- `kosif-one/vendor/hyperframes/skills/motion-graphics/references/motion-vocabulary.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-26` بناء الكلمة على شبكة إنشائية / Construction-grid & guide-line build (seen)
- `TYPE-27` عنوان قماشي من 1–4 كلمات مع اتجاه تلقائي / Canvas 1–4-word headline with auto-RTL (ready)
- `TYPE-29` مفردات حركة النص للستوري بورد / Text-motion vocabulary for storyboards (documented)
- `TYPE-30` الكلمة المختفية / Invisible-word blink (documented)

### `TYPE-29` — مفردات حركة النص للستوري بورد / Text-motion vocabulary for storyboards

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أسماء موحدة لحركات النص تكتبها في الستوري بورد فيُبنى كل مشهد بلا لبس. / Shared names for text moves so every storyboard beat is unambiguous to build.

**متى:** عند كتابة STORYBOARD.md / when writing STORYBOARD.md.

**كيف:** Entry: slide_bottom/top/left/right (y ±150, x ±200, power4.out), scale_grow (0.6 s power2.out), scale_punch (0.6 → 1, back.out(2.2)), fade_in 0.4 s, fade_blur (blur 14 px), typewriter, word_reveal (stagger 0.1), wave (letters 0.04), bounce_in (y −120, bounce.out), slam (y −300, power4.out). animate-text IDs (24): per-char soft-blur-in, per-character-rise, typewriter, bottom-up-letters, top-down-letters, stagger-from-center, stagger-from-edges; per-word per-word-crossfade, spring-scale-in, shared-axis-y, blur-out-up, kinetic-center-build, short-slide… Line masks need 0.2em padding.

**المعاملات:** 24 IDs; y ±150 / x ±200

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** vocabulary · storyboard · مفردات · ستوري بورد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/motion-graphics/references/motion-vocabulary.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/animate-text.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-27` عنوان قماشي من 1–4 كلمات مع اتجاه تلقائي / Canvas 1–4-word headline with auto-RTL (ready)
- `TYPE-28` موجة الحروف / Per-letter sine bounce & wave (seen)
- `TYPE-30` الكلمة المختفية / Invisible-word blink (documented)
- `TYPE-31` آلة كاتبة متدرجة بمؤشر / Eased typewriter with caret (typeOn) (ready)

### `TYPE-30` — الكلمة المختفية / Invisible-word blink

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة مختارة تختفي حرفًا حرفًا ثم تعود إلى مكانها. / A chosen word vanishes letter by letter, holds absent, then refocuses.

**متى:** تأكيد ساخر أو فكرة «غائبة» / ironic emphasis, an ‘absent’ idea.

**كيف:** Per letter (Latin): blur 0 → 8 px, opacity 1 → 0.05, rotate ±3°, y ±6 px, staggered; hold 0.4 s absent; reverse. Arabic: the whole word with blur + opacity.

**المعاملات:** blur 8 px; opacity .05; ±3°; ±6 px; hold 0.4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** vanish · blink · defocus · اختفاء · كلمة مختفية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-28` موجة الحروف / Per-letter sine bounce & wave (seen)
- `TYPE-29` مفردات حركة النص للستوري بورد / Text-motion vocabulary for storyboards (documented)
- `TYPE-31` آلة كاتبة متدرجة بمؤشر / Eased typewriter with caret (typeOn) (ready)
- `TYPE-32` كتابة بشرية: أخطاء ومسح ومؤشر ملوّن / Human typing: typos, backspace, caret swap (install)

### `TYPE-31` — آلة كاتبة متدرجة بمؤشر / Eased typewriter with caret (typeOn)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | GSAP standard ‘no charge’ licence (vendored gsap.min.js) — fine for client work, not for tools that compete with GSAP. Typed.js is GPL-3.0 — do not ship it; use typeOn. |

**ما هي:** كتابة حرفًا حرفًا بعدد حروف متسارع في البداية ومؤشر يومض أثناء القراءة، وتتحمل التقديم والتأخير. / Character-by-character typing with an eased count (most letters early) and a caret that blinks during the read; seek-safe.

**متى:** أوامر، أكواد، أسئلة، شاشات طرفية / prompts, code, questions, terminals.

**كيف:** MOTION.typeOn(tl, el, text, at, {cps: 46, dur, caret: true, blink: true, hold: 1.0, ease: E.type}) → duration clamp(len / cps, 0.5, 1.2) s; count eased by E.type = bezier(.5,1,.89,1) so 55–75 % of the characters land in the first fifth; caret ‘\|’ blinks at 2 Hz through the 1.0 s read-hold; driven by GSAP modifiers, so seeking works; pair with the kit SFX key-1…key-6. Speeds: headlines 15–22 cps; prompts ~46 cps + 72–120 f hold; showreel code line 22 cps, hold 0.5 s. Feel: 3–5 cps dramatic, 8–12 conversational, 15–20 energetic, 30+ instant. Catalog typewriter style: 25–45 cps ±20 % seeded jitter, 250–400 ms pause after punctuation, caret 530 ms; one caret visible, solid while typing, blinking when idle. Arabic: reveal by word or clip mask, never per character. Alternatives: GSAP TextPlugin {text: {value}, duration: len / cps, ease: 'none'}; HyperFrames typewriter (caret line\|block\|none). \| terminal chip, ‘>’ accent, dark rounded · 35–45 ms/char · block, 500 ms · pm-0xfemyn-e114d3 ; bold mono uppercase hype line · ~35 ms/char · solid block, 500 ms · pm-micheleharmonic-77628e ; editorial serif · ~40 ms/char · 2 px rust, 530 ms · pm-ho-ba-f3f0e9 ; question + giant ghost translation at 6 % behind · ~90 ms/char · 4 px accent bar, 2 Hz · pm-tankazunori0914-0fc886 ; ‘FIG. n’ red small caps + italic serif noun, deleted before the next · ~60 ms/char · red #c9452c · pm-hbcoop-de365c ; result card slides up 30 px, ‘⚡ 2.1s’ chip, ‘Copied’ toast 200 ms · 30–40 chars/s · – · pm-mehul4795-4a7007 ; prompt ≤8 words · 35 ms/char · 530 ms · pm-listudio-820c7b ; handwriting font, corner note · 40–60 ms/letter · – · pm-abderrahmen-g-9e8ed0 ; pixel spell banner, gold + 1 px dark outline, anti-aliasing off · 60–80 ms/char · – · pm-0xevinho-3777d8, pm-hoyoyoda-3a5c08

**المعاملات:** 46 cps default; headlines 15–22 cps; dur 0.5–1.2 s; caret 2 Hz; hold 1.0 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** typewriter · caret · typing · terminal · آلة كاتبة · مؤشر · كتابة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/kit/motion-kit.js:193`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:107`
- `kosif-tool/styles/typewriter/SKILL.md`
- `100-superskills/skills/audio-reactive-captions-studio/references/captions-rules.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-29` مفردات حركة النص للستوري بورد / Text-motion vocabulary for storyboards (documented)
- `TYPE-30` الكلمة المختفية / Invisible-word blink (documented)
- `TYPE-32` كتابة بشرية: أخطاء ومسح ومؤشر ملوّن / Human typing: typos, backspace, caret swap (install)
- `TYPE-33` فك التشفير / Scramble / decode reveal (ready)

### `TYPE-32` — كتابة بشرية: أخطاء ومسح ومؤشر ملوّن / Human typing: typos, backspace, caret swap

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | caret-swap is MIT AND OFL-1.1 (bundled Geist); rules Apache-2.0; GSAP standard licence. |

**ما هي:** كتابة مؤلفة كحالات متقطعة تسمح بالأخطاء والمسح واللصق، ومؤشر يتغير لونه أو يمسح العبارة ويكتب بديلها. / Typing authored as discrete states — typos, backspace, pastes — and a caret that recolours or erases a phrase and types its replacement.

**متى:** عروض منتجات وذكاء اصطناعي، تصحيح فكرة / AI/product demos, reframing an idea.

**كيف:** Sparse array of {t, text}; onUpdate reverse-searches the latest passed state (no interpolation) → typos, holds, bulk pastes and backspaces; first keystrokes 3–5 characters 0.1–0.2 s apart; driver ease none. Context caret: its background colour switches at segment boundaries; blink = (tl.time() % cycle) < cycle / 2; 4–8 s per typed line. Caret Swap: a gradient caret #FF4DAA → #8A5CF6 spreads over a phrase, collapses left, then types the replacement (font_size 72, 36–160; weight 400–700; Geist bundled). Terminal-then-display: 40 ms/char, caret blink 500 ms, then a 250 ms scale snap to a 160 px display face — not a crossfade (brief pm-danilowm-d3720d). Typewriter-reveal blueprint (3.6–7 s): the caret types and edits like a human, then collapses into the brand payoff or types a CTA rail under a standing logo; icon slides left, name typed, tagline fades (pm-tdinh-me-815acb). \| code (js): const STATES = [{t: 0, text: ""}, {t: .12, text: "Shp"}, {t: .45, text: "Sh"}, {t: .6, text: "Ship it"}, {t: 1.3, text: "Ship it today."}]; // typo → backspace → fix const textAt = (s) => STATES.reduce((cur, st) => (st.t <= s ? st : cur), STATES[0]).text; tl.to({}, { duration: 2, onUpdate() { el.textContent = textAt(this.time()); } }, at);

**المعاملات:** first keys 0.1–0.2 s apart; caret #FF4DAA→#8A5CF6; 4–8 s per line; snap 250 ms

**التثبيت:** npx -y hyperframes@0.8.164 add caret-swap

**الوسوم:** typing · typo · backspace · caret · كتابة بشرية · مسح · مؤشر

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/discrete-text-sequence.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/context-sensitive-cursor.md`
- `kosif-one/vendor/hyperframes/registry/components/caret-swap/caret-swap.html`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/typewriter-reveal.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-30` الكلمة المختفية / Invisible-word blink (documented)
- `TYPE-31` آلة كاتبة متدرجة بمؤشر / Eased typewriter with caret (typeOn) (ready)
- `TYPE-33` فك التشفير / Scramble / decode reveal (ready)
- `TYPE-34` قلب الحروف ثلاثي الأبعاد / Hacker-flip 3D decode (documented)

### `TYPE-33` — فك التشفير / Scramble / decode reveal

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard ‘no charge’ licence (vendored gsap.min.js) — fine for client work, not for tools that compete with GSAP. |

**ما هي:** الحروف تدور بين رموز من نفس الفئة ثم تقفل من اليسار إلى اليمين — مُبذَّرة وقابلة للتقديم. / Glyphs cycle through same-class glyphs and lock left to right — seeded and seekable.

**متى:** عناوين HUD، أرقام، تقنية وأمن / HUD labels, metrics, tech and security.

**كيف:** MOTION.scramble(tl, el, text, at, {dur: 0.9, pool: 'ABCDEFGHJKLMNPQRSTUVWXYZ023456789'}) → digits stay digits, look-alikes (I, O, 1) excluded; lock position = p × len × 1.15; glyphs change in 40 hashed steps across the tween. Showreel: scramble ‘60 fps’ in 0.45 s. Ready-mades: matrix-decode (size 64, glow none\|standard\|strong) and scramble-reveal (terminal\|clean). \| 30 ms per tick · stagger 25 ms · mono line · pm-jasonzhou1993-8595e0 ; 30 ms per swap · stagger 40 ms · label · pm-shneural-2abdfa ; 40 ms per change · 300 ms total · ‘L<*1 → LISTINGS’, ‘01 PRICE WAR’ HUD · pm-ceowinkz-7c776b ; 30 ms/char, 3–5 flips · L→R · base64 ciphertext · pm-agonaliu-466a8f ; every 2 frames · 40 ms, on the beat · accent colour · pm-techhalla-7acbc2 ; 40–60 ms · 60 ms, ~1 s · 30 % ghost duplicates for smear · pm-robj3d3-b18fad ; 3 frames per digit · – · number scramble · pm-aistocksavvy-3fb9f5

**المعاملات:** dur 0.9 s; lock ×1.15; 40 steps; pool A–Z (no I/O) + 0,2–9

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scramble · decode · hacker · HUD · فك التشفير · خلط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/kit/motion-kit.js:208`
- `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:207-225`
- `kosif-one/vendor/hyperframes/registry/components/matrix-decode/matrix-decode.html`
- `style:pm-ceowinkz-7c776b`

#### 7. قدرات قريبة في العائلة

- `TYPE-31` آلة كاتبة متدرجة بمؤشر / Eased typewriter with caret (typeOn) (ready)
- `TYPE-32` كتابة بشرية: أخطاء ومسح ومؤشر ملوّن / Human typing: typos, backspace, caret swap (install)
- `TYPE-34` قلب الحروف ثلاثي الأبعاد / Hacker-flip 3D decode (documented)
- `TYPE-35` لوحة المطار القلّابة / Split-flap (Solari) board (install)

### `TYPE-34` — قلب الحروف ثلاثي الأبعاد / Hacker-flip 3D decode

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل حرف ينقلب على مفصل أفقي من 90° إلى 0 وهو يعرض رموزًا عشوائية حتى يظهر الحرف الحقيقي. / Each character hinges from rotateX 90° to 0 while showing seeded random glyphs until it resolves.

**متى:** كشف كلمة سر، ميزة أمنية، شعار تقني / password reveals, security features, tech logos.

**كيف:** perspective 1500 px on the scene root; per-char stagger rotateX 90° → 0, power3.out; seeded glyphs until a reveal threshold; optional two-pass decode symbols → letters → real. One paused GSAP timeline, transforms/opacity only, deterministic hashes.

**المعاملات:** perspective 1500 px; power3.out; per-char stagger

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** flip · 3d · decode · قلب · ثلاثي الأبعاد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/hacker-flip-3d.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-32` كتابة بشرية: أخطاء ومسح ومؤشر ملوّن / Human typing: typos, backspace, caret swap (install)
- `TYPE-33` فك التشفير / Scramble / decode reveal (ready)
- `TYPE-35` لوحة المطار القلّابة / Split-flap (Solari) board (install)
- `TYPE-36` عدّاد الأسطوانة الدوّار / Odometer digit roll (seen)

### `TYPE-35` — لوحة المطار القلّابة / Split-flap (Solari) board

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** كل خانة تدير أسطوانتها عبر أبجدية ثابتة حتى حرفها المستهدف في شلال ميكانيكي. / Each cell walks its drum through a fixed alphabet to its target in a mechanical cascade.

**متى:** مواعيد، وجهات، إعلان أرقام / schedules, destinations, announcements.

**كيف:** Alphabet " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,'"; flipDuration 0.09 s (0.03–1.2), cellStagger 0.05 s (0–0.5), cellCount 12 (1–24); 1920×1080, 3.5 s; GSAP paused timeline. Seen: dark bevelled tiles with a centre hinge line, the top half folds down, 3–6 random flips per tile at 60 ms, 40 ms L→R stagger, second line in accent (pm-marouanegazouzi-6071d5). Stepped timing; digits slide, never fade.

**المعاملات:** flip 0.09 s; stagger 0.05 s; 12 cells; 3–6 flips × 60 ms

**التثبيت:** npx -y hyperframes@0.8.164 add split-flap-board

**الوسوم:** split-flap · solari · board · لوحة قلابة · مطار

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/blocks/split-flap-board/split-flap-board.html`
- `style:pm-marouanegazouzi-6071d5`
- `kosif-atlas/skills/342-kernel/1223-frontend/motion/kinetic-type.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-33` فك التشفير / Scramble / decode reveal (ready)
- `TYPE-34` قلب الحروف ثلاثي الأبعاد / Hacker-flip 3D decode (documented)
- `TYPE-36` عدّاد الأسطوانة الدوّار / Odometer digit roll (seen)
- `TYPE-37` عدّاد بأرقام جدولية / Tabular counter (MOTION.counter) (ready)

### `TYPE-36` — عدّاد الأسطوانة الدوّار / Odometer digit roll

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل خانة رقمية عمود من 0–9 خلف قناع يدور إلى رقمه، والخانات الأسرع تلف أكثر. / Each digit is a masked 0–9 column that rolls to its value; faster columns spin extra turns.

**متى:** أرقام بطولية، أسعار، إحصاءات / hero numbers, prices, stats.

**كيف:** Each digit = a column of repeated 0–9 inside overflow:hidden; translateY by eased progress; faster (lower-order) columns add extra full turns (10 rows each). Tunings: right → left stagger 40–60 ms, ~400 ms each easeOutCubic (pm-sudeepsd-1a3485); ~1 s easeOutExpo with gradient fill #c9f4ff → #1aa7ec via background-clip:text and a smaller % at the right (infographic); last digit overshoots and settles 500–700 ms ease-out-back (pm-melvynx-6cde6c); 40 ms per digit step with an ease-out end (brief pm-steventey-0d20e4). Always tabular figures (TYPE-06).

**المعاملات:** stagger 40–60 ms; 400 ms–1 s; easeOutCubic/Expo

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** odometer · digits · counter · عداد · أرقام

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:infographic`
- `style:pm-sudeepsd-1a3485`
- `style:pm-melvynx-6cde6c`
- `kosif-tool/styles/pm-steventey-0d20e4/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-34` قلب الحروف ثلاثي الأبعاد / Hacker-flip 3D decode (documented)
- `TYPE-35` لوحة المطار القلّابة / Split-flap (Solari) board (install)
- `TYPE-37` عدّاد بأرقام جدولية / Tabular counter (MOTION.counter) (ready)
- `TYPE-38` بكرة الكلمات وعدّاد نابض / Slot-machine word roll & spring ticker (install)

### `TYPE-37` — عدّاد بأرقام جدولية / Tabular counter (MOTION.counter)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard ‘no charge’ licence (vendored gsap.min.js) — fine for client work, not for tools that compete with GSAP. |

**ما هي:** عداد يبدأ قريبًا من القيمة النهائية ويتباطأ ويثبت بأرقام جدولية وفواصل ولاحقات. / A counter that starts near its final value, eases out and holds, with tabular digits, separators and units.

**متى:** أي رقم يتغير على الشاشة / any number that changes on screen.

**كيف:** MOTION.counter(tl, el, from, to, at, dur, {sep: ',', prefix, suffix, decimals, ease}) sets font-variant-numeric: tabular-nums and tweens a proxy with E.out; seek-safe. Craft: start near the final value (94 → 76 kg, not 0 → 76), 1.0–1.1 s. Examples: M.counter(tl, el, 0, 900, at, 1.1, {sep: ','}); M.counter(tl, el, 94, 76, at, 1.0, {suffix: ' kg', sep: false}). Seen: count 900 ms tabular after a weight-900 verb pop (brief pm-utopyaszx-1b2f94); count-up 800 ms under a 25 %-height numeral (pm-palashbagchi11-0a4b6b); mono frame counter + progress bar (pm-codestackr-c071bf); centred stat punch with digits overlapping in blur (pm-twoclipping-6dd14e).

**المعاملات:** 1.0–1.1 s; E.out; tabular-nums; sep/prefix/suffix/decimals

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** counter · count-up · numbers · عداد · أرقام

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/kit/motion-kit.js:227`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:125`
- `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`
- `style:pm-palashbagchi11-0a4b6b`

#### 7. قدرات قريبة في العائلة

- `TYPE-35` لوحة المطار القلّابة / Split-flap (Solari) board (install)
- `TYPE-36` عدّاد الأسطوانة الدوّار / Odometer digit roll (seen)
- `TYPE-38` بكرة الكلمات وعدّاد نابض / Slot-machine word roll & spring ticker (install)
- `TYPE-39` تبديل كلمة في خانة ثابتة واستيلاء الشريط / Word-slot swap & ticker takeover (install)

### `TYPE-38` — بكرة الكلمات وعدّاد نابض / Slot-machine word roll & spring ticker

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 primitive; vendored GSAP under the GSAP standard licence. |

**ما هي:** خيارات مكدسة في عمود مقنّع تدور خطوة خطوة بنابض حتى تستقر على الكلمة النهائية. / Options stacked in a masked column step through with springs and land on the final word.

**متى:** «أسرع/أذكى/معًا»، تعدد اللغات، اختيار / ‘faster/smarter/together’, languages, choices.

**كيف:** Vertical spring ticker rule: TICKER_WIDTH 30–60 % of the viewport, STEP_DUR 0.3–0.7 s, STEP_SPACING 0.3–0.5 s (≤ STEP_DUR so springs overlap), stepped back.out; reference 204 px step at 0.45 s. Seen: ~150 ms per step with 6 px vertical blur and opacity falloff above/below (pm-1littlecoder-9fef89); lands on the final word in accent, 600 ms back.out (pm-kentcdodds-6fa8cf); item gap 1.4em, neighbour opacity 1 / 0.5 / 0.15 plus blur by distance, settle spring (pm-lester-tyy-f897f7); language carousel with the centre line sharp white and others blurred 6 px (pm-itisrazak-3ad902); vertical list fading at the edges (pm-lexnlin-6161a6). Music primitive slot-machine-reveal: roll → downbeat, 0.8–2.0 s.

**المعاملات:** STEP_DUR 0.3–0.7 s; spacing 0.3–0.5 s; 204 px @ 0.45 s; neighbours 1/.5/.15

**التثبيت:** npx -y hyperframes@0.8.164 preview # copy music-to-video motion-primitives/slot-machine-reveal/scene.html (gsap vendored in motion-primitives/assets)

**الوسوم:** slot machine · ticker · word roll · بكرة · آلة الحظ

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/vertical-spring-ticker.md`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/slot-machine-reveal/scene.html`
- `style:pm-lester-tyy-f897f7`
- `style:pm-kentcdodds-6fa8cf`

#### 7. قدرات قريبة في العائلة

- `TYPE-36` عدّاد الأسطوانة الدوّار / Odometer digit roll (seen)
- `TYPE-37` عدّاد بأرقام جدولية / Tabular counter (MOTION.counter) (ready)
- `TYPE-39` تبديل كلمة في خانة ثابتة واستيلاء الشريط / Word-slot swap & ticker takeover (install)
- `TYPE-40` إيقاع البادئة/البطل/الذيل / Lead / hero / tail beat splitter (proven)

### `TYPE-39` — تبديل كلمة في خانة ثابتة واستيلاء الشريط / Word-slot swap & ticker takeover

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** الجملة ثابتة وخانة واحدة مقنّعة تتبدل كلماتها، أو شريط يقفل على كلمة فيكبرها إلى عنوان كامل. / A fixed sentence with one masked slot cycling words, or a ticker that locks a word and promotes it to a full-frame headline.

**متى:** مزايا متعددة لمنتج، إعادة صياغة، إعلان نهائي / multi-benefit products, reframes, payoffs.

**كيف:** kinetic-type-swap: fixed prefix/suffix, one masked slot sized to the widest option rolls and settles on the last (options ‘faster,smarter,together’, cues lock to narration, exit none\|fade\|up). Variants: fixed ‘RE-’ with a swapping suffix in a new colour every 830 ms (pm-kentcdodds-6fa8cf); last-word swap — headline static, final word rolls/crossfades 300 ms ease-in-out, y 0.4em, grey → black, width animates so centring re-balances (pm-samuel-yostt-891f87); text-state-swap ‘Saving draft’ → ‘Saved’ (outgoing blurs away, incoming lifts in); currency codes replaced every ~150 ms (pm-davidmarcus-a28a60). Ticker takeover: a mono ticker rolls options, locks the final word with an accent flash and promotes it to a full-frame headline (blueprint 5–7 s: typed lead-in + cycling accent word, then a hero crashes in and shoves the text aside). Fixed-anchor cycle blueprint (6.6–11.1 s): one pinned element never moves while its neighbour cycles discrete states, steady or accelerating, into a lockup.

**المعاملات:** 830 ms per swap; 300 ms ease-in-out; y 0.4em; takeover 5–7 s

**التثبيت:** npx -y hyperframes@0.8.164 add kinetic-type-swap # also ticker-takeover, text-state-swap

**الوسوم:** word swap · slot · ticker · takeover · تبديل الكلمة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/kinetic-type-swap/kinetic-type-swap.html`
- `kosif-one/vendor/hyperframes/registry/components/ticker-takeover/ticker-takeover.html`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/fixed-anchor-cycle.md`
- `style:pm-samuel-yostt-891f87`

#### 7. قدرات قريبة في العائلة

- `TYPE-37` عدّاد بأرقام جدولية / Tabular counter (MOTION.counter) (ready)
- `TYPE-38` بكرة الكلمات وعدّاد نابض / Slot-machine word roll & spring ticker (install)
- `TYPE-40` إيقاع البادئة/البطل/الذيل / Lead / hero / tail beat splitter (proven)
- `TYPE-41` صدمة العنوان وضربة الكلمة على الإيقاع / Headline slam & beat word punch (install)

### `TYPE-40` — إيقاع البادئة/البطل/الذيل / Lead / hero / tail beat splitter

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقسم السكربت إلى 3–5 إيقاعات لكل مقطع، وفي كل إيقاع بادئة صغيرة وكلمة بطلة ضخمة وذيل صغير في نوافذ زمنية متساوية. / Splits a script into 3–5 beats per clip; each beat shows a small lead, one huge hero word and a small tail in equal windows.

**متى:** ريلز طباعية حركية من سكربت أو تعليق / kinetic-type reels from a script or voice-over.

**كيف:** beatsFor(tokens): n = min(5, max(3, ceil(words / 6))) beats per clip; ≤6 words per beat, ≤30 words per clip (hard error beyond); hero = first word with 3–10 alphanumerics, lead = words before it, tail = words after; beat j owns [j·len/n, (j+1)·len/n] s and is fully cleared before the next; small type = ¼ of the headline height; pace 2.5 words/s fast, 1.8 relaxed; timestamped scripts (‘0–3s: …’) must be ordered and non-overlapping. Part of the kinetic-flow profile (17 themes A–Q, 8/10 s clips, 9:16 / 16:9 / 1:1), which emits Google Flow prompts — the beat grid itself is engine-agnostic: render it with TYPE-14 + TYPE-41. Proven: node --test tests/production-profiles.test.mjs → 10/10 pass in this container. Gap: hero detection uses [a-zA-Z0-9], so Arabic words fall back to the first word — use \p{L} as below. \| code (js): function beats(tokens) { // own sketch, Unicode-safe hero pick const n = Math.min(5, Math.max(3, Math.ceil(tokens.length / 6))); const parts = Array.from({ length: n }, (_, j) => tokens.slice(Math.round(j * tokens.length / n), Math.round((j + 1) * tokens.length / n))); return parts.map((w) => { const core = (x) => x.replace(/[^\p{L}\p{N}]/gu, ""); const h = Math.max(0, w.findIndex((x) => core(x).length >= 3 && core(x).length <= 10)); return { lead: w.slice(0, h).join(" "), hero: w[h], tail: w.slice(h + 1).join(" ") }; }); }

**المعاملات:** 3–5 beats; ≤6 words/beat; ≤30 words/clip; hero 3–10 letters; small = ¼ headline

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** beat · hero word · kinetic · script · إيقاع · كلمة بطلة · تقسيم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:78-84`
- `fastify-motion-bro/tests/production-profiles.test.mjs`
- `fastify-motion-bro/skills/kinetic-flow/SKILL.md:13`

#### 7. قدرات قريبة في العائلة

- `TYPE-38` بكرة الكلمات وعدّاد نابض / Slot-machine word roll & spring ticker (install)
- `TYPE-39` تبديل كلمة في خانة ثابتة واستيلاء الشريط / Word-slot swap & ticker takeover (install)
- `TYPE-41` صدمة العنوان وضربة الكلمة على الإيقاع / Headline slam & beat word punch (install)
- `TYPE-42` متتاليات الضرب وجمل تُبنى بالضربات / Beat-slam sequences & stacked statements (seen)

### `TYPE-41` — صدمة العنوان وضربة الكلمة على الإيقاع / Headline slam & beat word punch

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** كلمة أو كلمتان ثقيلتان بعرض الإطار تقريبًا تنكمشان إلى مكانهما على الضربة ثم قطع حاد. / One or two heavy words at near frame width scale down onto the beat, then a hard cut.

**متى:** مونتاج حماسي، إعلانات، ريلز موسيقية / hype edits, ads, music reels.

**كيف:** 1–2-word chunks in heavy uppercase grotesk at ~90–100 % frame width, scale 1.15 → 1.0 easeOutExpo in 150–250 ms, hold to the next beat (~300–500 ms), hard cut, tracking −0.03em (pm-micheleharmonic-77628e: #030303 / #ffffff with violet #8a6cff). Ready-mades: headline-slam (scales down into frame, 3-frame landing shake, subtle drift, whip-up exit; accent_word_index, shadow) and music primitive braam-punch (scale + weight slam on drop/surge, 0.2–0.9 s; hero 900, 280 px, −0.04em, glow #7c3aed on #0a0a0f). Pair with a background colour flip on the same beat (pm-prasenx-8d9323). \| 1.2 → 1 · 200 ms · giant heavy italic on flat blue · pm-cansincengiz-me-cf68dd ; 1.3 → 1 + motion blur · 200–300 ms · fills the frame · pm-stephanlivera-df17a2 ; oversized 300 px, 900 · slide in · cropped beyond the frame edge · pm-mrtanviir-132457 ; drop, rotate −8° · 120 ms overshoot · black 900 on red · pm-rendesr-86be44 ; 1.3 → 1.0 · 2 frames · no fade-out, exit by hard cut · brief pm-micheleharmonic-77628e ; hard cut at 110 % · 150 ms cubic-bezier(0.2,0.9,0.3,1) · final frame static ≥1.5 s · brief pm-reflex-cloud-72ffe5 ; 1.4 → 1 · 220 ms in (0.16,1,0.3,1) / 160 ms out @ 140 BPM · each word shoves the previous out · brief pm-influencer-seo-ce8c33 ; single wide 900 word · cut on the beat, hold 0.5–1.2 s · flat saturated field + grain · pm-crazyalphaaa-bc7e75 ; wide 900 caps 1.15 → 1 + blur · slam 180 ms, underline 250 ms, gloss 200 ms · orange bar wipes under, small italic serif definition · pm-ghinaiya-nirmal-5d8fec

**المعاملات:** 1.15→1.0; 150–250 ms easeOutExpo; hold 300–500 ms; 3-frame shake

**التثبيت:** npx -y hyperframes@0.8.164 add headline-slam

**الوسوم:** slam · punch · beat · hype · صدمة · ضربة · إيقاع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/headline-slam/headline-slam.html`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/braam-punch/scene.html`
- `style:pm-micheleharmonic-77628e`
- `style:pm-ghinaiya-nirmal-5d8fec`

#### 7. قدرات قريبة في العائلة

- `TYPE-39` تبديل كلمة في خانة ثابتة واستيلاء الشريط / Word-slot swap & ticker takeover (install)
- `TYPE-40` إيقاع البادئة/البطل/الذيل / Lead / hero / tail beat splitter (proven)
- `TYPE-42` متتاليات الضرب وجمل تُبنى بالضربات / Beat-slam sequences & stacked statements (seen)
- `TYPE-43` وصفة سطر الافتتاح / Hook-line recipe & kinetic-type beats (documented)

### `TYPE-42` — متتاليات الضرب وجمل تُبنى بالضربات / Beat-slam sequences & stacked statements

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عبارات قصيرة تضرب على مصفوفة إيقاع واحدة بمداخل مختلفة ثم تنتهي بقفل ثابت. / Short phrases slam in on one shared beat array with distinct entrances, ending in a locked finale.

**متى:** بيانات حماسية، جمل من 3–6 كلمات / manifestos, 3–6-word statements.

**كيف:** One BEATS array (PULSE seconds per sub-beat) drives distinct entrances per phrase — scale-slam, side-snap, rise-rotate — with optional metronome ticks or a beat bar, then a locked finale; title-safe padding 120 × 160 px, 150 px type (HyperFrames rule). Stacked statement: heavy uppercase words appear one per beat stacking vertically, overshoot 1.1 → 1, word every 250–500 ms, the final word gets a highlight bar wiping under it, skill marquees scroll at the top and bottom edges at 60 px/s (pm-teslachartz-c58b32). Chaos collage: words drop in large with 2–4° rotation and motion blur, each slam 150–200 ms at 1.3 → 1, one vertical word, shapes orbit, then everything blurs out (pm-pankajkumar-dev-0bee87).

**المعاملات:** word every 250–500 ms; 1.1→1 / 1.3→1; 150–200 ms; padding 120×160 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** beat slam · sequence · statement · متتالية · ضربات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-teslachartz-c58b32`
- `style:pm-pankajkumar-dev-0bee87`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/kinetic-beat-slam.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-40` إيقاع البادئة/البطل/الذيل / Lead / hero / tail beat splitter (proven)
- `TYPE-41` صدمة العنوان وضربة الكلمة على الإيقاع / Headline slam & beat word punch (install)
- `TYPE-43` وصفة سطر الافتتاح / Hook-line recipe & kinetic-type beats (documented)
- `TYPE-44` ختم وملصق وكلمة مؤثر صوتي / Stamp, sticker & SFX word pop (seen)

### `TYPE-43` — وصفة سطر الافتتاح / Hook-line recipe & kinetic-type beats

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | If you build it in Remotion: free for individuals and small teams, a company licence above that. |

**ما هي:** الثانيتان الأوليان بجدول زمني دقيق: وميض على أول نبضة، صعود الكلمات، نبضة التأكيد، ثبات مع دفع كاميرا. / The first two seconds on an exact timetable: flash on the first transient, words rise, emphasis pops, hold with a push.

**متى:** أول ثانيتين من أي ريل / the first two seconds of any reel.

**كيف:** Playbook A: 0–120 ms background flash or cut on the first audio transient (linear) → 80–500 ms words rise, 90 ms stagger, ease-out quint → 500–780 ms the emphasis word pops (spring damping 12 / stiffness 180) and turns accent → 780–2000 ms hold with a 2 % camera push. Word entrance 300–450 ms, translateY 40–70 px, cubic-bezier(0.22,1,0.36,1), opacity done in the first 60 %; stagger 70–120 ms, or start = words.json start − 60 ms; emphasis 1 → 1.12 → 1 over 280 ms. Kinetic-type-beats blueprint (3.0–12.9 s, workhorse for 6 roles): flat bold centred type whose motion is the words changing, onto a spring-pop payoff. intro-kinetic-cascade template (3.5–7 s, 📦): big editorial phrases, one enlarged hero word, hard cuts, keyword + icon climax.

**المعاملات:** flash 0–120 ms; rise 80–500 ms / 90 ms stagger; pop 500–780 ms spring 12/180; hold to 2 s + 2 % push

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hook · opening · recipe · افتتاحية · هوك

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-tool/playbooks/kinetic-type.md:38-45`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/kinetic-type-beats.md`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/templates/intro-kinetic-cascade/index.html`
- `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/kinetic-type/module.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-41` صدمة العنوان وضربة الكلمة على الإيقاع / Headline slam & beat word punch (install)
- `TYPE-42` متتاليات الضرب وجمل تُبنى بالضربات / Beat-slam sequences & stacked statements (seen)
- `TYPE-44` ختم وملصق وكلمة مؤثر صوتي / Stamp, sticker & SFX word pop (seen)
- `TYPE-45` انزلاق بضبابية حركة ولطخة لونية / Motion-blur slide, smear & stretch (seen)

### `TYPE-44` — ختم وملصق وكلمة مؤثر صوتي / Stamp, sticker & SFX word pop

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة ثقيلة تنطبع بدوران وتجاوز واهتزاز، أو ملصق مائل ينبثق. / A heavy word stamps in with rotation, overshoot and shake, or a tilted sticker pops.

**متى:** مؤثرات صوتية، أسعار، «جديد»، كوميكس / SFX words, prices, ‘NEW’, comics.

**كيف:** Outlined bold word 1.6 → 1 with rotation (pm-allforbigfire-86ff3c); heavy display 2.0 → 1.0 with overshoot, rotate −4°, neon glow 12 px lime + dark outline, small shake on impact, 200 ms in, hold 0.8 s (pm-ibrahimwasim240-809370); stamp label rotate −8°, 1.4 → 1 in 200 ms with a hard shadow block (pm-polydao-7a572b); SFX word 0 → 1.2 → 1 with −10° tilt and thick outline (pm-topi-003-b0e12c); pixel onomatopoeia with outline, scale punch + 6 px shake (pm-pluginplay-3d4006); tilted sticker — rounded orange/magenta rect, bold white text, −4…−8°, from 0.6 with overshoot 1.1 in 250 ms (pm-paulo-kombucha-96431c); huge digits with an 8 px dark stroke and offset shadow, 0 → 1.1 → 1 easeOutBack(1.6) 400 ms (pm-deebeeeff-50fcd0); scale-punch over scrolling diagonal yellow/black hazard stripes (pm-m1n9-k7-ff9ab9).

**المعاملات:** 1.4–2.0 → 1; −4…−10°; 200–400 ms; shake 6 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stamp · sticker · sfx · comic · ختم · ملصق · مؤثر صوتي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-ibrahimwasim240-809370`
- `style:pm-paulo-kombucha-96431c`
- `style:pm-polydao-7a572b`
- `style:pm-deebeeeff-50fcd0`

#### 7. قدرات قريبة في العائلة

- `TYPE-42` متتاليات الضرب وجمل تُبنى بالضربات / Beat-slam sequences & stacked statements (seen)
- `TYPE-43` وصفة سطر الافتتاح / Hook-line recipe & kinetic-type beats (documented)
- `TYPE-45` انزلاق بضبابية حركة ولطخة لونية / Motion-blur slide, smear & stretch (seen)
- `TYPE-46` كلمة بانفصال RGB وتشويش / RGB-split glitch word (ready)

### `TYPE-45` — انزلاق بضبابية حركة ولطخة لونية / Motion-blur slide, smear & stretch

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الحروف أو الكلمة تنزلق بضبابية اتجاهية تتناسب مع السرعة ثم تحتد، أو تتمطط كلطخة ثم ترتد. / Letters or a word slide in with velocity-scaled directional blur, or smear and stretch, then snap sharp.

**متى:** انتقالات سريعة وكلمات على الإيقاع / fast transitions and on-beat words.

**كيف:** Letter by letter from +x, 60 ms stagger, 120 ms per letter, blur 12 → 0 (pm-jasonzhou1993-8595e0); letters from +200 px, 250 ms, stagger 50 ms, then an orange dot pops back.out(2) (pm-tequilafunks-97f6c9); word x-offset 15 %, blur 30 → 0 px in 120–180 ms, one word per beat at 120–130 BPM (pm-prasenx-8d9323); huge word on the beat, blur 0 → 24 px, 180 ms in, 300 ms expo-out settle, coral dot as the period (pm-roundtablespace-d3a1be); smear scaleX 1 → 2.5 + 40 px horizontal blur for 3–5 frames (~200 ms) then snap back (pm-himanshutwtxs-5f4b43); spring slam (stiffness ~300, damping ~18) from +60 % height with a magenta copy stretched scaleY 3 → 1, opacity .8 → 0 trailing for 300 ms (pm-techhalla-7acbc2); silver-gradient condensed 800 headline sliding with 150 ms horizontal blur (pm-adamdesgns-478d6d). Kit helpers to build it now: MOTION.speedBlur (SVG blur filter driven by speed) and MOTION.squash (scaleX 1.08 / scaleY 0.90 → 1 in 0.13 s at an edge).

**المعاملات:** blur 12–40 px; 120–300 ms; smear ×2.5 for 3–5 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** motion blur · smear · stretch · ضبابية حركة · لطخة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-jasonzhou1993-8595e0`
- `style:pm-techhalla-7acbc2`
- `style:pm-himanshutwtxs-5f4b43`
- `kosif-studio/motion/kit/motion-kit.js:372`

#### 7. قدرات قريبة في العائلة

- `TYPE-43` وصفة سطر الافتتاح / Hook-line recipe & kinetic-type beats (documented)
- `TYPE-44` ختم وملصق وكلمة مؤثر صوتي / Stamp, sticker & SFX word pop (seen)
- `TYPE-46` كلمة بانفصال RGB وتشويش / RGB-split glitch word (ready)
- `TYPE-47` بدائيات حركة النص على الموسيقى / Music-anchored type primitives & templates (install)

### `TYPE-46` — كلمة بانفصال RGB وتشويش / RGB-split glitch word

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard ‘no charge’ licence (vendored gsap.min.js) — fine for client work, not for tools that compete with GSAP. |

**ما هي:** تأتأة رقمية قصيرة مُبذَّرة: انزياح وانفصال ألوان وشرائح ثم عودة إلى النص النظيف. / A short seeded digital stutter — jitter, RGB split and slices — then back to clean type.

**متى:** تقنية، أخطاء، انتقال حاد — لمرة واحدة لا على النص الطويل / tech, errors, a hard switch — once, never on body text.

**كيف:** MOTION.glitch(tl, el, at, {dur: 0.3, amp: 10, seed: 3}) → ~30 steps per second of seeded x jitter fading by (1 − i/n), twin drop-shadows ±4 px rgba(255,0,80,.7) / rgba(0,200,255,.7), random clip-path slices, clean again at at + dur (≤0.4 s). Seen: RGB offset 4 px decaying over 200 ms (pm-apoorvjain25-d24184); word drawn 3× (red, black, cream) with 4–8 px offsets and 2–3-frame slice jitter on saturated blue (pm-ayushunleashed-ece3e3); condensed title glitches in for 6–10 frames with 4 slices at 4–8 px (pm-madhav-xo-f97f20); ±6 px R/G/B and band displacement for 2–4 frames in 200 ms bursts (pm-tolgayhickiran-e90799). Premium cousin (📦): yt-prism-title — blur-focus entrance, red/blue fringe settles then breathes, perspective bow, slow scale drift, 6 s.

**المعاملات:** dur 0.3 s (≤0.4); amp 10 px; RGB ±4 px; ~30 steps/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** glitch · rgb split · chromatic · تشويش · غليتش

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/kit/motion-kit.js:548`
- `100-superskills/skills/kosif-montage-motion/SKILL.md:95`
- `kosif-one/vendor/hyperframes/registry/blocks/yt-prism-title/yt-prism-title.html`
- `style:pm-ayushunleashed-ece3e3`

#### 7. قدرات قريبة في العائلة

- `TYPE-44` ختم وملصق وكلمة مؤثر صوتي / Stamp, sticker & SFX word pop (seen)
- `TYPE-45` انزلاق بضبابية حركة ولطخة لونية / Motion-blur slide, smear & stretch (seen)
- `TYPE-47` بدائيات حركة النص على الموسيقى / Music-anchored type primitives & templates (install)
- `TYPE-48` نص بإطارات ممسوكة / Held-frame stepped type (idea)

### `TYPE-47` — بدائيات حركة النص على الموسيقى / Music-anchored type primitives & templates

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0; vendored GSAP under the GSAP standard licence. |

**ما هي:** مكتبة مشاهد نصية جاهزة تُربط بأحداث الموسيقى (ضربة، انفجار، لفّة، بداية جملة). / Ready text scenes anchored to music events — downbeat, drop, roll, phrase start.

**متى:** فيديو على أغنية أو موسيقى إعلان / a film cut to a song or ad track.

**كيف:** Read music-to-video motion-primitive-catalog.md and template-catalog.md; copy scene.html / index.html (gsap vendored in motion-primitives/assets); anchor each primitive to audiomap events (beat grid from BEAT). \| kinetic-letter-in · per-letter entrance · downbeat / phrase · 0.4–1.2 s ; braam-punch · scale + weight slam · drop / surge · 0.2–0.9 s ; slot-machine-reveal · spin-to-land characters · roll → downbeat · 0.8–2.0 s ; outline-to-fill · stroke → solid fill · downbeat / reveal · 0.8–1.8 s ; text-wave-distort · wavy distortion · hold / texture · 1.0–2.5 s ; typewriter-reveal · type-on with caret · roll / build · 1.0–3.0 s ; word-grid-burst · word grid revealed per onset, one refocuses · onsets → downbeat · 1.8–3.2 s ; held-text-strobe-burst (template) · a still word's letters flip through 66 texture fills every ~3 frames · roll · 1.2–3.5 s (cap ~4) ; roll-flipbook-word-cycle (template) · centred word flips every 16th note, may lock into a phrase · hi-hat roll · 1.2–3.8 s ; typewriter-phrase-keyword-shuffle (template) · words type one per onset, then a keyword cycles typefaces · onsets / beat · 2.5–5 s ; split-anchor-word-slot (template) · held left anchor + torn-paper slot cycling word groups · beat · 3–6 s ; held-message-living-field (template) · readable mark held still over a breathing colour field · phrase · 6–16 s ; card-flyby (template) · depth column of cards, coloured wipe per landing (4–7 landings) · beat · 4–6.5 s ; poster-tile-mosaic (template) · tessellating colour tiles, recolour, snake-fill · beat · 4–7 s (8 max)

**المعاملات:** 7 primitives + 7 templates; spans 0.2–16 s

**التثبيت:** npx -y hyperframes@0.8.164 preview # render: npx -y hyperframes@0.8.164 render

**الوسوم:** music · beat · primitives · templates · موسيقى · قوالب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/template-catalog.md`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/templates/held-text-strobe-burst/index.html`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/word-grid-burst/scene.html`

#### 7. قدرات قريبة في العائلة

- `TYPE-45` انزلاق بضبابية حركة ولطخة لونية / Motion-blur slide, smear & stretch (seen)
- `TYPE-46` كلمة بانفصال RGB وتشويش / RGB-split glitch word (ready)
- `TYPE-48` نص بإطارات ممسوكة / Held-frame stepped type (idea)
- `TYPE-49` قلم التظليل والخط السفلي / Highlighter & underline swipe (install)

### `TYPE-48` — نص بإطارات ممسوكة / Held-frame stepped type

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ظهور الكلمات بتثبيت إطارات صريح بدل التلطيف — إحساس رسوم يدوية. / Words appear with explicit held frames instead of easing — a hand-animated feel.

**متى:** صلصال، بكسل، ستوب موشن / claymation, pixel, stop-motion looks.

**كيف:** Wordmark word by word with hard 3-frame holds (brief pm-ceowinkz-7c776b); clay lyric letters squash scaleY 0.85 on the beat and recover in 3 held frames, never fade (brief pm-davidshulmanfl-371638); bitmap type at 60 ms per character with anti-aliasing banned (brief pm-0xevinho-3777d8). Build with tl.set() at frame multiples (on twos/threes) — no tweened ease.

**المعاملات:** 3 frames per step; scaleY 0.85; 60 ms/char

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stepped · held frames · on twos · إطارات ممسوكة · صلصال

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-tool/styles/pm-ceowinkz-7c776b/BRIEF.md`
- `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`
- `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-46` كلمة بانفصال RGB وتشويش / RGB-split glitch word (ready)
- `TYPE-47` بدائيات حركة النص على الموسيقى / Music-anchored type primitives & templates (install)
- `TYPE-49` قلم التظليل والخط السفلي / Highlighter & underline swipe (install)
- `TYPE-50` كلمات داخل كبسولات / Keyword pills (seen)

### `TYPE-49` — قلم التظليل والخط السفلي / Highlighter & underline swipe

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** مستطيل أو خط يكبر خلف الكلمة المفتاحية من جهة بداية القراءة. / A box or bar grows behind or under the keyword from the reading-start edge.

**متى:** الكلمة الأهم في السطر — مرة واحدة لكل سطر / the one key word per line.

**كيف:** scaleX 0 → 1 with transform-origin at the reading start (left for Latin, right for Arabic), 300 ms ease-out / power3.out, padding ~0.15em; invert the text colour if needed. HyperFrames inline-highlight: tint yellow\|green\|blue\|violet, thickness thin\|standard\|thick, origin left\|right\|center (driven by a CSS scale variable). \| yellow box with black border · 300 ms, padding 0.15em · pm-0xnfrith-5be616 ; red #f0442c behind a phrase in a mono block, text → white, camera pushed in · 300 ms ease-out · pm-antonio-kodheli-490109 ; blue box, word stays white on blue · 300 ms power3.out · pm-arjunsh1607-93005d ; pastel rounded rect at 60 % · 300 ms ease-out · pm-itisrazak-3ad902 ; accent box behind the last word, word turns dark · 300 ms, padding 4 px · pm-majorbaguette-fb11d7 ; lime box · 400 ms · pm-prasad-pilla-2c0cba ; rounded white rect r 8, text inverts to brand blue · 300 ms ease-out · pm-thismacapital-dfba20 ; slanted teal bar, skew −6°, under the newest line · 200 ms · pm-deifosv-04e4d3 ; translucent underline bar = 35 % of line height · 400 ms easeOutCubic · pm-gigabit-million-16b3a0 ; 2 px underline drawn after an italic serif word · +300 ms · pm-blushpetal795-0c85c2 ; SVG swoosh under a green keyword · draw 400 ms · pm-macrohou-33959d ; copper italic line with a sweeping underline · 0.4 s · pm-francoxavier33-d2dfd2 ; green box · 300 ms · pm-imthatcarlos-e04bfe ; yellow box, origin left · 300 ms ease-out · pm-kangaroohere-b10f8d

**المعاملات:** scaleX 0→1; 300–400 ms; padding 0.15em; bar 35 % line height

**التثبيت:** npx -y hyperframes@0.8.164 add inline-highlight

**الوسوم:** highlighter · underline · marker · emphasis · تظليل · خط سفلي · تأكيد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/inline-highlight/inline-highlight.html`
- `style:pm-arjunsh1607-93005d`
- `style:pm-gigabit-million-16b3a0`
- `style:pm-thismacapital-dfba20`

#### 7. قدرات قريبة في العائلة

- `TYPE-47` بدائيات حركة النص على الموسيقى / Music-anchored type primitives & templates (install)
- `TYPE-48` نص بإطارات ممسوكة / Held-frame stepped type (idea)
- `TYPE-50` كلمات داخل كبسولات / Keyword pills (seen)
- `TYPE-51` شطب واستبدال / Strike-through & replace (install)

### `TYPE-50` — كلمات داخل كبسولات / Keyword pills

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمات المهمة داخل كبسولات ملونة تنبثق على إيقاعها. / Key words sit in coloured pills that pop on their beat.

**متى:** مزايا منتج، كلمات مفتاحية متعددة في جملة / product benefits, several keywords in a sentence.

**كيف:** Rounded rects in brand colours with a 4–6 px darker bottom extrusion, radius 14 px, padding 0.15em 0.35em, each pops 0 → 1.1 → 1 in 350 ms on its beat (pm-bizibeast-10f264: #2481fa, #fc504e, #ffc21a); violet pill (radius 999 px) scales in while the rest pops word by word at 120 ms (pm-emollick-8661a8); accent pill 0.6 → 1.05 → 1 in 300 ms back-out, radius 12 (pm-sudo-kiran-6609ed); stacked colour pill words with darker borders, spring stagger 150 ms (pm-sudo-kiran-b055de). Karaoke pill: 0.96 → 1.08 over 140 ms at the word's start (playbook B).

**المعاملات:** radius 12–14 px / 999 px; pad .15em .35em; 0→1.1→1 in 300–350 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pill · capsule · keyword · كبسولة · كلمة مفتاحية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-bizibeast-10f264`
- `style:pm-emollick-8661a8`
- `style:pm-sudo-kiran-6609ed`
- `kosif-tool/playbooks/kinetic-type.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-48` نص بإطارات ممسوكة / Held-frame stepped type (idea)
- `TYPE-49` قلم التظليل والخط السفلي / Highlighter & underline swipe (install)
- `TYPE-51` شطب واستبدال / Strike-through & replace (install)
- `TYPE-52` عنوان بلونين وكلمة لون / Two-tone lines & accent-word colour (seen)

### `TYPE-51` — شطب واستبدال / Strike-through & replace

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** خط يرسم نفسه فوق الكلمة القديمة ثم تظهر الكلمة البديلة. / A strike draws across the old word, then the replacement reveals.

**متى:** «ليس هذا بل ذاك»، مشكلة → حل، أسعار قديمة / ‘not this but that’, problem → fix, old prices.

**كيف:** Line draws L → R in 300 ms ease-out, then the replacement slides up / swaps in accent (400 ms). Looks: red 6 px #e5484d over one word, final keyword violet, display 800 at −0.04em (pm-kmasiff-cc72cb); rounded red bar 10 px #f05a4a at −2°, then subtitle words fade one by one (pm-mehul4795-4a7007); thick rounded bar drawn diagonally in 250 ms (pm-zheke-38deff); struck number that then dims, 300 ms (pm-reyzostyle-b55864); pain list — ✕ icon + line-through 200 ms per item (pm-imthatcarlos-e04bfe); 300 + 400 ms strike-then-swap (pm-theviableedge-9065be). HyperFrames strikethrough-replace: tint red\|amber\|blue\|violet, thickness, origin, tone ink\|paper. Arabic: draw R → L.

**المعاملات:** strike 250–300 ms; swap 400 ms; 6–10 px bar

**التثبيت:** npx -y hyperframes@0.8.164 add strikethrough-replace

**الوسوم:** strikethrough · replace · correction · شطب · استبدال

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/strikethrough-replace/strikethrough-replace.html`
- `style:pm-kmasiff-cc72cb`
- `style:pm-mehul4795-4a7007`
- `style:pm-theviableedge-9065be`

#### 7. قدرات قريبة في العائلة

- `TYPE-49` قلم التظليل والخط السفلي / Highlighter & underline swipe (install)
- `TYPE-50` كلمات داخل كبسولات / Keyword pills (seen)
- `TYPE-52` عنوان بلونين وكلمة لون / Two-tone lines & accent-word colour (seen)
- `TYPE-53` غروتسك عريض مع كلمة سيريف مائلة / Grotesk + italic-serif accent (ready)

### `TYPE-52` — عنوان بلونين وكلمة لون / Two-tone lines & accent-word colour

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** السطر الأول بلون الحبر يطرح المشكلة والثاني بلون التمييز يقدم المفارقة، أو كلمة واحدة فقط ملوّنة. / Line one in ink states the problem, line two in accent delivers the twist — or exactly one word takes the accent.

**متى:** عناوين المزايا والإعلانات / feature and ad headlines.

**كيف:** Line 2 arrives 250–400 ms after line 1 with a 12–30 px rise (optional blur 8 → 0). One accent word per line. Single-word variants: last word in brand blue #1a8fd6 (pm-fractadev-149adc); final line lime (pm-robvjourney-ce3e1a); condensed caps with the last word in accent (pm-devius-maximus-beab45); [bracketed] caption with the key phrase red, fade-up 200 ms (pm-melvynx-6cde6c); mono caption with the last phrase green, y 12 px 400 ms (pm-jazzen-chen-4542ae). Dim-bright body: primary words white, rest #666 (pm-reyzostyle-b55864); paragraph #bcbcba 400 with one phrase #000 600 and a cursor pointing under it (pm-notdwd-7de38a). \| navy → blue · 400 ms apart, y 12, 500 ms ease-out · pm-alex-prompter-1ea044 ; #1a1f1c → #1b6fe0, weight 600, −0.04em · fade + rise 24 px, 400 ms · pm-elliot-garreffa-f334bc ; #3e251b → #e85a9e, rounded 800, leading 1.05 · +250 ms, y 30, blur 8→0 · pm-thilina-a-891c09 ; black → mid-grey benefit, 700, −0.03em · +1 s, y 20, 400 ms · pm-wozu-co-242285 ; off-white → orange + full stop, condensed, leading 0.9 · – · pm-kloss-xyz-b9b3f6 ; #111 problem → #2a7fd4 fix · 8 px, 300 ms, 1 s gap · pm-moguzbulbul-6311b6 ; white → #d6f04a clause, 36 px caption · y 12, 400 ms after the UI action · pm-majorbaguette-fb11d7 ; white 800 → violet clause · 300 ms apart · pm-misbahsy-80eaec ; black → brand blue + numbered eyebrow · 400 ms, stagger 120 · pm-rammanq-f5a90f ; white → gold clause + numbered tag pill · – · pm-ezshine-c90d73

**المعاملات:** +250–400 ms; y 12–30 px; one accent word per line

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** two-tone · accent · colour · emphasis · لونين · لون التمييز

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-elliot-garreffa-f334bc`
- `style:pm-thilina-a-891c09`
- `style:pm-notdwd-7de38a`
- `kosif-tool/playbooks/kinetic-type.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-50` كلمات داخل كبسولات / Keyword pills (seen)
- `TYPE-51` شطب واستبدال / Strike-through & replace (install)
- `TYPE-53` غروتسك عريض مع كلمة سيريف مائلة / Grotesk + italic-serif accent (ready)
- `TYPE-54` عنوان سيريف تحريري بكلمة مائلة / Editorial serif headline & keyword title (seen)

### `TYPE-53` — غروتسك عريض مع كلمة سيريف مائلة / Grotesk + italic-serif accent

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان غروتسك ثقيل وكلمة واحدة بخط سيريف مائل عالي التباين وبلون التمييز — التوقيع التحريري الأشهر. / A heavy grotesk headline with one word in a high-contrast italic serif and the accent colour — the signature editorial pairing.

**متى:** عروض منتجات وأفلام عرض أعمال / product films, showreels.

**كيف:** Heavy neo-grotesk 600–900 at −0.04em with one key word in italic high-contrast serif + accent, same cap height (serif ≈1.15× size), sentence case with full stops; stagger the serif word ~150 ms; optional 2 px underline drawn 300 ms later. Code in hand: the fastify editorial painter draws a ‘900 {11.4 % w}px’ headline plus an ‘italic 600 {4.8 % w}px Georgia’ accent line at y 0.81 h in the accent colour — its text is hard-coded (‘THE HIDDEN MECHANISM’), pass your own before use. Seen widely: sans 700 / serif italic 400 (pm-listudio-820c7b); heavy ink word + large italic serif blue line, 150 ms (pm-agonaliu-466a8f); upright dark serif + italic purple with blur 12 → 0 in 500 ms (pm-gabrielbuzziv-4ff0c6); italic serif white + bold sans violet in lower case with a full stop, ~6 % height (pm-influencer-seo-ce8c33); wide black grotesk wordmark + italic serif descriptor ≈4 : 1, +200 ms (pm-roundtablespace-d3a1be); heavy black word + underlined italic serif sub on flat orange, 1.1 → 1 (pm-itsuki-dev-10942d). Arabic analogue: Cairo / IBM Plex Sans Arabic heavy + an Amiri or Aref Ruqaa accent word.

**المعاملات:** serif ≈1.15×; −0.04em; +150 ms; underline 2 px / 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** italic serif · pairing · editorial · accent · سيريف مائل · تحريري

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `fastify-motion-bro/web/editorial.js:79-80`
- `style:pm-listudio-820c7b`
- `style:pm-agonaliu-466a8f`
- `style:pm-roundtablespace-d3a1be`

#### 7. قدرات قريبة في العائلة

- `TYPE-51` شطب واستبدال / Strike-through & replace (install)
- `TYPE-52` عنوان بلونين وكلمة لون / Two-tone lines & accent-word colour (seen)
- `TYPE-54` عنوان سيريف تحريري بكلمة مائلة / Editorial serif headline & keyword title (seen)
- `TYPE-55` تعبئة متدرجة ومعدنية / Gradient & metallic word fills (seen)

### `TYPE-54` — عنوان سيريف تحريري بكلمة مائلة / Editorial serif headline & keyword title

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان بخط سيريف كتب بكلمة أخيرة مائلة أو ملونة، وعين علوية صغيرة متباعدة. / A book-serif headline with the last key word in italic or accent, under a small tracked kicker.

**متى:** أفلام هادئة فاخرة، وثائقيات، علامات أدبية / calm premium films, documentaries, literary brands.

**كيف:** Book/transitional serif 400 (or heavy serif 800 at ~110–130 px with a closing period); numbered tracked-caps kicker above (12 px, 0.2em) and a spec caption below; headline 64–72 px at 1080p (pm-bogdandragomir-35e024). Accent changes per scene to match the feature — purple #8b3fe0, green, red #c8102e (pm-iammxfschr-d68f90). Eyebrow (uppercase sans + small orange star, 1.4 % H) + 2-line serif at 7.5 % H + grey subline, group fade-up 500 ms, stagger 80 (pm-sachaarbonel-8f14f4). Serif 800, one word accent blue, y 20 px + fade 300 ms (pm-marouanegazouzi-6071d5); one large serif word per beat, period in accent (pm-lexnlin-038035); serif 400 sentence, key noun #e8641e, one clause per scene (pm-xelandre-363f00); terracotta italic (pm-wani-shola-16ca7a); micro-caps eyebrow 10 px 0.2em + one orange word (pm-manuelogomigo-f33ca9). Keyword title (akbun template): a small white lead-in, then a pale-yellow #FFE67A serif keyword 2–3× the lead size, lead first (Amiri for Arabic).

**المعاملات:** headline 64–72 px @1080p; kicker 12 px 0.2em; keyword 2–3× lead, #FFE67A

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** serif · editorial · kicker · سيريف · عين علوية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-bogdandragomir-35e024`
- `style:pm-sachaarbonel-8f14f4`
- `style:pm-iammxfschr-d68f90`
- `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-52` عنوان بلونين وكلمة لون / Two-tone lines & accent-word colour (seen)
- `TYPE-53` غروتسك عريض مع كلمة سيريف مائلة / Grotesk + italic-serif accent (ready)
- `TYPE-55` تعبئة متدرجة ومعدنية / Gradient & metallic word fills (seen)
- `TYPE-56` أقواس تحديد وصندوق أداة تصميم / Selection brackets & design-tool bounding box (seen)

### `TYPE-55` — تعبئة متدرجة ومعدنية / Gradient & metallic word fills

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة واحدة مملوءة بتدرج لوني أو فضي، أحيانًا مع نسخة ضبابية متوهجة خلفها. / One word filled with a colour or silver gradient, sometimes over a blurred glowing duplicate.

**متى:** الكلمة المميزة في إعلانات الذكاء الاصطناعي والتقنية / the hero word in AI/tech promos.

**كيف:** background-clip:text + linear gradient on the key word and a blurred duplicate behind at 30 % (glow 24 px): #f06aa8 → #8a6cf5 → #5d8cf7, grey setup line above, black punch line below (pm-rossaxbt-3085b7); weight 200 gradient words (#f6a5b8 → #e47ad0 → #9a80ff, 90°) beside weight 700 white words in one line (pm-viktoroddy-98c1d8); line 2 gradient #7b3fe4 → #e85fa0 (pm-gautam-mer1-2ae354); last of 3 lines in an orange gradient + underline, 150 ms stagger (pm-astrodevil-3f2054); condensed 800 caps with a vertical silver gradient (pm-adamdesgns-478d6d); hero numerals with a vertical cyan → blue gradient and a smaller % (infographic).

**المعاملات:** glow duplicate 30 % / 24 px; 90° gradients

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** gradient · metallic · fill · تدرج · معدني

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-rossaxbt-3085b7`
- `style:pm-viktoroddy-98c1d8`
- `style:pm-gautam-mer1-2ae354`
- `style:infographic`

#### 7. قدرات قريبة في العائلة

- `TYPE-53` غروتسك عريض مع كلمة سيريف مائلة / Grotesk + italic-serif accent (ready)
- `TYPE-54` عنوان سيريف تحريري بكلمة مائلة / Editorial serif headline & keyword title (seen)
- `TYPE-56` أقواس تحديد وصندوق أداة تصميم / Selection brackets & design-tool bounding box (seen)
- `TYPE-57` صور ووجوه وأيقونات داخل السطر / Inline avatars & icons inside a headline (seen)

### `TYPE-56` — أقواس تحديد وصندوق أداة تصميم / Selection brackets & design-tool bounding box

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** زوايا تحديد أو صندوق بمقابض كأداة تصميم يحيط بالكلمة المهمة. / Selection corners or a handle box like a design tool frame the key word.

**متى:** أدوات تصميم، دقة، «انظر هنا» / design tools, precision, ‘look here’.

**كيف:** Four L-shaped corner marks snap in from outside with slight overshoot, 200 ms backOut, stroke 3 px (pm-leadnotifi-e83f94); 1 px blue #3d4df0 rect with 8 square 6 px handles around a hero word, width/height animate while a live ‘W × H’ pill (radius 4 px) updates beneath (pm-shneural-2abdfa).

**المعاملات:** 200 ms backOut; stroke 1–3 px; handles 6 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** brackets · bounding box · selection · أقواس · تحديد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-leadnotifi-e83f94`
- `style:pm-shneural-2abdfa`

#### 7. قدرات قريبة في العائلة

- `TYPE-54` عنوان سيريف تحريري بكلمة مائلة / Editorial serif headline & keyword title (seen)
- `TYPE-55` تعبئة متدرجة ومعدنية / Gradient & metallic word fills (seen)
- `TYPE-57` صور ووجوه وأيقونات داخل السطر / Inline avatars & icons inside a headline (seen)
- `TYPE-58` الكلمة تؤدي معناها / Word performs its meaning (seen)

### `TYPE-57` — صور ووجوه وأيقونات داخل السطر / Inline avatars & icons inside a headline

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صف صور دائرية متداخلة أو أيقونة داخل سطر العنوان بين الكلمات. / A row of overlapping avatars or an icon set inline between the headline's words.

**متى:** مجتمع، عملاء، دليل اجتماعي / community, customers, social proof.

**كيف:** 3–4 circular avatars: d = 0.9em, overlap −0.25em, 2 px white border, each pops 0 → 1 with a spring (stiffness ~200), 80 ms stagger (pm-samuel-yostt-891f87); brand-red keywords carry an inline icon (pm-aschapmann-131210). Use inline-flex with vertical-align ≈ −0.15em so the line box doesn't jump.

**المعاملات:** d 0.9em; overlap −0.25em; stagger 80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** avatars · inline icon · صور داخل السطر

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-samuel-yostt-891f87`
- `style:pm-aschapmann-131210`

#### 7. قدرات قريبة في العائلة

- `TYPE-55` تعبئة متدرجة ومعدنية / Gradient & metallic word fills (seen)
- `TYPE-56` أقواس تحديد وصندوق أداة تصميم / Selection brackets & design-tool bounding box (seen)
- `TYPE-58` الكلمة تؤدي معناها / Word performs its meaning (seen)
- `TYPE-59` قوائم تخفت السابق / Dim-previous stacks & active-item lists (seen)

### `TYPE-58` — الكلمة تؤدي معناها / Word performs its meaning

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل كلمة تتحرك بالخاصية التي تسميها: «اضغط» تنضغط، «تمدد» تتمدد، «ضبابي» يتضبب. / Each word moves with the property it names: squash squashes, stretch stretches, blur blurs.

**متى:** شرح مزايا أداة تصميم أو حركة / explaining features of a design or motion tool.

**كيف:** ~1 s per word: squash → scaleY 0.6, stretch → scaleY 1.6 (pm-zheke-38deff); stretch / stagger / blur / weight (pm-hanifproduktif-54bdee); click → hotspot + tooltip, blur → blur box over half the letters, zoom → scale-through, embed → the word inside a card with code (pm-jhylee95-e1152f).

**المعاملات:** ~1 s per word; scaleY 0.6 / 1.6

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** verb · literal · meaning · الكلمة تؤدي معناها

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-jhylee95-e1152f`
- `style:pm-hanifproduktif-54bdee`
- `style:pm-zheke-38deff`

#### 7. قدرات قريبة في العائلة

- `TYPE-56` أقواس تحديد وصندوق أداة تصميم / Selection brackets & design-tool bounding box (seen)
- `TYPE-57` صور ووجوه وأيقونات داخل السطر / Inline avatars & icons inside a headline (seen)
- `TYPE-59` قوائم تخفت السابق / Dim-previous stacks & active-item lists (seen)
- `TYPE-60` النقطة الختامية وإبدال الحرف / Full-stop dot & glyph substitution (seen)

### `TYPE-59` — قوائم تخفت السابق / Dim-previous stacks & active-item lists

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل سطر جديد يضيء والأسطر السابقة تخفت إلى الرمادي، أو عنصر نشط واحد في قائمة. / Each new line lights up while earlier lines dim to grey, or one active item glows in a list.

**متى:** ثلاثيات، قوائم مزايا، عملاء / triads, benefit lists, client rows.

**كيف:** Triad ‘See it. / Copy it. / Make it yours.’ — y 20 px + fade 400 ms, ~1.3 s per line, older dim to 30 % (pm-listudio-820c7b); stacked negation — newest cream line on a slanted teal bar (skew −6°, 200 ms), previous at 40 % (pm-deifosv-04e4d3); scrolling list with a red bar on the current item, others 30 %, row 0.4 s (pm-heyiammallik-e72d17); client row of small mono names at 40 %, current goes 100 % every 250 ms in sync with its card (pm-arjunsh1607-93005d); 3 bold lines with check badges, stagger 180 ms, slide-up 16 px, prices violet (pm-kmasiff-cc72cb); new line white, previous grey 40 % (pm-davidmarcus-a28a60). Build now with MOTION.stagger (gap 0.07 s, from y 28 / opacity 0 / scale 0.96).

**المعاملات:** dim to 30–40 %; 0.25–1.3 s per item; stagger 180 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** list · dim · triad · قائمة · تخفيت

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-listudio-820c7b`
- `style:pm-deifosv-04e4d3`
- `style:pm-heyiammallik-e72d17`
- `kosif-studio/motion/kit/motion-kit.js:557`

#### 7. قدرات قريبة في العائلة

- `TYPE-57` صور ووجوه وأيقونات داخل السطر / Inline avatars & icons inside a headline (seen)
- `TYPE-58` الكلمة تؤدي معناها / Word performs its meaning (seen)
- `TYPE-60` النقطة الختامية وإبدال الحرف / Full-stop dot & glyph substitution (seen)
- `TYPE-61` الخط المتغير: محاور ووزن متموج وعرض / Variable-font motion: axis tween, weight wave, width swell (install)

### `TYPE-60` — النقطة الختامية وإبدال الحرف / Full-stop dot & glyph substitution

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة بطلة تسقط في موضع النقطة الختامية، أو حرف يُستبدل بشكل متحرك. / A hero dot drops into the sentence's full stop, or a letter is replaced by a moving shape.

**متى:** ختام الجمل والشعارات / closing lines and wordmarks.

**كيف:** Typewrite the closing line, keep a hovering hero dot, then drop it into the period slot with a small 300 ms ease-out bounce (pm-hbcoop-de365c); after a letter drop the final period becomes a blue dot that pops (pm-chatgptastra-0d95c7) or an orange dot back.out(2) (pm-tequilafunks-97f6c9); coral dot as the period of a slammed word (pm-roundtablespace-d3a1be); a conic-gradient ring replaces the ‘O’ and rotates 360° every 2 s (pm-oliahmed205-3e31c4). Headlines in this school end with a full stop for finality.

**المعاملات:** drop 300 ms; back.out(2); ring 360°/2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** full stop · dot · glyph · نقطة · إبدال حرف

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-hbcoop-de365c`
- `style:pm-chatgptastra-0d95c7`
- `style:pm-oliahmed205-3e31c4`

#### 7. قدرات قريبة في العائلة

- `TYPE-58` الكلمة تؤدي معناها / Word performs its meaning (seen)
- `TYPE-59` قوائم تخفت السابق / Dim-previous stacks & active-item lists (seen)
- `TYPE-61` الخط المتغير: محاور ووزن متموج وعرض / Variable-font motion: axis tween, weight wave, width swell (install)
- `TYPE-62` خط مفرّغ: أرقام مجوفة ومن محيط إلى تعبئة / Outline type: hollow numerals, outline → fill, glowing outline (install)

### `TYPE-61` — الخط المتغير: محاور ووزن متموج وعرض / Variable-font motion: axis tween, weight wave, width swell

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | weight-wave ships the Recursive font (OFL-1.1); components Apache-2.0; GSAP standard licence. |

**ما هي:** الحروف تتشكل في مكانها بتحريك محاور الخط المتغير (الوزن، العرض، الحجم البصري، الميل) بدل تحريكها. / Glyphs reshape in place by tweening variable axes (weight, width, optical size, slant) instead of moving.

**متى:** تأكيد بلا تكبير، شعارات حية، ضربات إيقاع / emphasis without scaling, living wordmarks, beat hits.

**كيف:** Tween CSS custom properties that feed font-variation-settings (or @property) — no layout shift. Emphasis rule: jump weight 500 → 900 (150 ms crossfade) rather than scaling past 1.3×. Fonts on hand: Cairo[slnt,wght].ttf (200–1000, Latin + Arabic) and ReemKufi[wght].ttf in this skill's proofs/_shared/fonts; Arabic VFs also Noto Kufi/Naskh Arabic and Readex Pro. \| optical settle (Fraunces) · opsz 144 → 72, wght 440 → 300, 0.45 s power2.out, local @font-face · hyperframes techniques ; emphasis without scale · wght 500 → 900, 150 ms; never >1.3× · kinetic-type playbook ; axis beat · wght or wdth 200 → 900 (Roboto Flex) · HF variable-axis-type ; per-character flex · weight + width hairline-condensed → black-wide, font-size eases inversely to hold the box, stagger 0.06 s · HF variable-font-flex ; weight wave · Recursive VF, crest wght 400 → 1000 travels the line, slnt −12, crestWidth 4, sweepSpeed 0.5, ltr or rtl, #f5f5f7 on #0b0b0d · HF weight-wave (canvas) ; width swell · wdth 62 → 125 with font-size until the word overflows, Archivo 900, 2–3 s power2.inOut · pm-pankajkumar-dev-0bee87 ; weight sweep + readout · wght 100 → 900, 0.6–0.8 s power2.inOut, mono caption shows the values · pm-tequilafunks-97f6c9 ; weight + tracking · wght 200 → 800 easeInOut 800 ms, letter-spacing 0.1em → 0, one letter accent · pm-sahildesigner23-ee3155 ; fast pops · wght 200 → 900 in 220 ms; 2 s major / 500 ms minor pulse · brief pm-zheke-38deff ; hero glyph stagger · 300 → 800, 30 ms per glyph, ≤12 glyphs · brief pm-itisrazak-3ad902 ; weight morph · wght 300 → 900 over 400 ms ease-out · pm-souravbhar871-61f424 \| code (css): @font-face { font-family: CairoVF; src: url(Cairo[slnt,wght].ttf); font-weight: 200 1000; } .hero { font-family: CairoVF; font-variation-settings: "wght" var(--w, 500); } /* tl.to(".hero", { "--w": 900, duration: 0.15, ease: "power2.out" }, beat) — emphasis, no scale */

**المعاملات:** wght 200–1000; opsz 144→72; wdth 62→125; 0.15–3 s

**التثبيت:** npx -y hyperframes@0.8.164 add variable-axis-type # also variable-font-flex, weight-wave

**الوسوم:** variable font · weight · axis · wdth · الخط المتغير · الوزن

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/variable-axis-type/variable-axis-type.html`
- `kosif-one/vendor/hyperframes/registry/blocks/weight-wave/weight-wave.html`
- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`
- `style:pm-pankajkumar-dev-0bee87`

#### 7. قدرات قريبة في العائلة

- `TYPE-59` قوائم تخفت السابق / Dim-previous stacks & active-item lists (seen)
- `TYPE-60` النقطة الختامية وإبدال الحرف / Full-stop dot & glyph substitution (seen)
- `TYPE-62` خط مفرّغ: أرقام مجوفة ومن محيط إلى تعبئة / Outline type: hollow numerals, outline → fill, glowing outline (install)
- `TYPE-63` طباعة شبحية خلفية / Giant ghost background type & ghost rows (ready)

### `TYPE-62` — خط مفرّغ: أرقام مجوفة ومن محيط إلى تعبئة / Outline type: hollow numerals, outline → fill, glowing outline

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 primitive; vendored GSAP under the GSAP standard licence. |

**ما هي:** الحرف كحد فقط: أرقام فصول مجوفة، كلمة تتحول من محيط إلى تعبئة على الضربة، أو عنوان محيطي متوهج. / Type as stroke only: hollow chapter numerals, a word that fills from outline on the beat, or a glowing outline headline.

**متى:** أرقام فصول، سنوات، ضربة كشف / chapter numbers, years, reveal hits.

**كيف:** CSS: -webkit-text-stroke 2px; color transparent → fill. Outline → fill on a downbeat (0.8–1.8 s, music primitive). Giant 2-digit chapter numeral ~25 % frame height as a 2 px grey stroke, then fill amber #f2c230 with bloom in 250 ms ease-out (glow 12 px) while a white 800-caps label appears beneath (pm-kyonax-on-tech-aabc1d). Glowing outline: fillText off, strokeText 1.5 px green + glow, fade in 400 ms with blur 6 → 0, previous line kept at 15 % for 600 ms as afterglow; use 700–800 weights so outlines read — works for bold Kufi/Naskh (pm-rneayan-ea6129). Hollow numerals: centred outline serif number ~20 % height, stroke 2 px, red line icon beside, serif chapter title + italic teaser (pm-henkvaness-0e06af); ghost index 01…06 at 4–6 % opacity, ~45 % frame height, slight parallax (pm-gigabit-million-16b3a0); huge ‘0N’ at 8 % behind a product carousel with an ‘N / 12’ HUD, swapping every 0.4–0.5 s (pm-maxalexweber-67688b); full-height outline condensed year (pm-kloss-xyz-fe0c31) or an oversized year stamp top-left (pm-triglyceee-bd5b08); split block — two colour bands, outlined vs filled condensed type (pm-blue-clarity-ef56d0).

**المعاملات:** stroke 1.5–2 px; fill 250 ms; numeral 20–45 % height; ghost 4–8 %

**التثبيت:** npx -y hyperframes@0.8.164 preview # copy music-to-video motion-primitives/outline-to-fill/scene.html

**الوسوم:** outline · stroke · hollow · numeral · مفرغ · محيط · أرقام

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/outline-to-fill/scene.html`
- `style:pm-kyonax-on-tech-aabc1d`
- `style:pm-henkvaness-0e06af`
- `style:pm-gigabit-million-16b3a0`

#### 7. قدرات قريبة في العائلة

- `TYPE-60` النقطة الختامية وإبدال الحرف / Full-stop dot & glyph substitution (seen)
- `TYPE-61` الخط المتغير: محاور ووزن متموج وعرض / Variable-font motion: axis tween, weight wave, width swell (install)
- `TYPE-63` طباعة شبحية خلفية / Giant ghost background type & ghost rows (ready)
- `TYPE-64` نص بارز بظلال مكدسة / Extruded & stacked-shadow type (seen)

### `TYPE-63` — طباعة شبحية خلفية / Giant ghost background type & ghost rows

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نسخة ضخمة باهتة من العنوان تنجرف خلفه عكس اتجاهه، أو صفوف نص شبحية تملأ الإطار. / A huge faint copy of the headline drifts behind it the other way, or ghost rows of text fill the frame.

**متى:** عمق تحريري بلا صور / editorial depth without imagery.

**كيف:** fastify painter: '900 {0.16 w}px', alpha 0.075 × heroAlpha, x = 0.5 w + sin(phase × 0.22) × 0.035 w, y = 0.18 h, maxWidth 0.9 w. HyperFrames mk-emphasis-type (📦): an oversized low-contrast word drifting slowly behind the subject. Ghost rows: the headline repeated in rows over the whole frame at 8–12 % (outline or dim fill), rows offset by half a word, 20–40 px/s alternating, hero on top at full contrast (pm-marouanegazouzi-6071d5); two rows ‘FRIDAY —’ at 8–12 %, opposite at ~80 px/s (pm-tankazunori0914-0fc886); 6–8 rows ‘WORD — WORD —’ in 1.5 px orange stroke at 30 %, 60–120 px/s (pm-tequilafunks-97f6c9); outlined caps 1.5 px at 15 %, ~110 px, top/bottom bands at 120 px/s (pm-jasonzhou1993-8595e0); stroke 1.5 px accent 40 %, 120 px/s (pm-sahildesigner23-ee3155); outline rows above/below a solid centre word, opposite at 40 px/s, stroke 2 px (pm-zaqailo-212ad3).

**المعاملات:** alpha 7.5 %; size 16 % w; rows 8–30 %; 20–120 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ghost type · background · rows · depth · شبحي · خلفية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `fastify-motion-bro/web/editorial.js:52-53`
- `kosif-one/vendor/hyperframes/registry/components/mk-emphasis-type/mk-emphasis-type.html`
- `style:pm-marouanegazouzi-6071d5`
- `style:pm-tequilafunks-97f6c9`

#### 7. قدرات قريبة في العائلة

- `TYPE-61` الخط المتغير: محاور ووزن متموج وعرض / Variable-font motion: axis tween, weight wave, width swell (install)
- `TYPE-62` خط مفرّغ: أرقام مجوفة ومن محيط إلى تعبئة / Outline type: hollow numerals, outline → fill, glowing outline (install)
- `TYPE-64` نص بارز بظلال مكدسة / Extruded & stacked-shadow type (seen)
- `TYPE-65` أثر الصدى والنسخ المحيطية / Echo trail & outline echo stack (seen)

### `TYPE-64` — نص بارز بظلال مكدسة / Extruded & stacked-shadow type

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نسخ مزاحة متتالية تحت الكلمة تصنع بثقًا ثلاثي الأبعاد أو ظلًا ملونًا متدرجًا. / Successive offset copies under the word fake a 3D extrusion or a stepped colour shadow.

**متى:** عناوين ريترو ومرحة وإعلانات جريئة / retro, playful and bold ad titles.

**كيف:** N copies at (i·dx, i·dy) with decreasing alpha; 1–3 px per layer (>4 px reads as glitch); static stack fades in at scale 0.94–0.98 → 1 over 0.5–0.8 s; heartbeat depth 1 + sin(p) × 0.2–0.6, one beat per 0.7–1.5 s (HyperFrames rule). Looks: cream #f1efe3 condensed 800 with 6–10 text-shadows +2,+2 in #e8501f, 1.15 → 1 with a 120 ms impact (pm-tankazunori0914-0fc886); cream fill + 3 px black stroke + 4–6 shadows 3 px apart in yellow/orange/red/blue, jitter 1–2 px per frame (pm-gizakdag-b8c59e); 10–20 layers 1–2 px in dark ink with a contrasting outline every few layers, front face solid blue, depth 20–30 px (pm-teslachartz-c58b32); teal/rust shadows at 4 & 8 px (pm-ik-builds-b8bdcf); yellow extruded red-outlined chunky title with badges (pm-davidshulmanfl-371638); rounded display + darker offset duplicate (pm-ror-fly-9950f1); extruded bevel + flare sweep + ring opener (pm-ryzoft-4f85bd, see 3D). \| code (js): const depth = (n = 8, dx = 2, dy = 2, c = "#e8501f") => Array.from({ length: n }, (_, i) => `${(i + 1) * dx}px ${(i + 1) * dy}px 0 ${c}`).join(", "); hero.style.textShadow = depth(); // cream #f1efe3 condensed 800 face on top

**المعاملات:** 1–3 px per layer; 6–20 layers; pulse 0.2–0.6 per 0.7–1.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** extrude · shadow · 3d text · retro · بثق · ظل مكدس

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-tankazunori0914-0fc886`
- `style:pm-gizakdag-b8c59e`
- `style:pm-teslachartz-c58b32`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/3d-text-depth-layers.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-62` خط مفرّغ: أرقام مجوفة ومن محيط إلى تعبئة / Outline type: hollow numerals, outline → fill, glowing outline (install)
- `TYPE-63` طباعة شبحية خلفية / Giant ghost background type & ghost rows (ready)
- `TYPE-65` أثر الصدى والنسخ المحيطية / Echo trail & outline echo stack (seen)
- `TYPE-66` نص مملوء بصورة أو فيديو / Image- & video-filled text (seen)

### `TYPE-65` — أثر الصدى والنسخ المحيطية / Echo trail & outline echo stack

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نسخ متأخرة تتبع الحروف المتحركة بإضاءة متناقصة، أو نسخ محيطية تتكرر حول الكلمة. / Lagging copies trail moving letters with falling brightness, or outline copies repeat around the word.

**متى:** سرعة، صدى، دقة / speed, echo, precision.

**كيف:** Echo trail: 6–10 copies of each letter at previous positions (1 frame apart), lightness 100 % → 30 % (pm-chatgptastra-0d95c7); 8–10 copies offset by velocity × Δt with Δt = 1 frame (pm-himanshutwtxs-5f4b43); 3–5 copies offset 20–40 px, decreasing opacity, lag 2–3 frames (pm-raphaelaubryy-4b137e). Outline echo stack: a solid word with 2–6 stroke-only copies above/below (1 px, 15 %) sliding apart (pm-shneural-2abdfa, pm-codestackr-c071bf, pm-topi-003-9ca6b5, pm-web3wesley-7bb108); stroked duplicates at scale 1.05, stagger 40 ms (pm-safarkhanshuvo-ffd52d); outline copies scrolling vertically one line per beat, 2 px (pm-ghinaiya-nirmal-5d8fec). Sample the timeline back in time — never accumulate frame history — so renders stay deterministic. \| code (js): for (let k = 8; k >= 0; k--) { // oldest first, current on top const p = pos(t - k / FPS); // same timeline, sampled back in time ctx.fillStyle = `hsl(0 0% ${100 - k * 8.75}%)`; // 100 % → 30 % ctx.fillText(word, p.x, p.y); }

**المعاملات:** 6–10 copies; 1 frame apart; 100→30 % lightness; outline 1 px at 15 %

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** echo · trail · outline · صدى · أثر

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-chatgptastra-0d95c7`
- `style:pm-himanshutwtxs-5f4b43`
- `style:pm-shneural-2abdfa`
- `style:pm-raphaelaubryy-4b137e`

#### 7. قدرات قريبة في العائلة

- `TYPE-63` طباعة شبحية خلفية / Giant ghost background type & ghost rows (ready)
- `TYPE-64` نص بارز بظلال مكدسة / Extruded & stacked-shadow type (seen)
- `TYPE-66` نص مملوء بصورة أو فيديو / Image- & video-filled text (seen)
- `TYPE-67` نص لزج متحول / Gooey morph text (install)

### `TYPE-66` — نص مملوء بصورة أو فيديو / Image- & video-filled text

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمة قناع يظهر من خلاله فيديو أو صورة أو خامة. / The word is a mask that shows video, a photo or a texture through it.

**متى:** افتتاحيات، أسماء مدن، علامات / openers, place names, brands.

**كيف:** background-clip:text for images; SVG clipPath or CSS mask for <video>. Word ~80 % width with a 1.5 px violet outline #9a6cf0 and the same clip blurred and dimmed behind (pm-influencer-seo-ce8c33); photo fill with a slowly moving background-position and text scale 1.05 → 1, ~1.2 s hold on full-bleed blue (pm-arjunsh1607-93005d); footage-filled word (pm-andginja-333d32); metal texture video in letters (pm-samuel-spitz-974923); giant numeral (900, 600 px) clipping a photo with floating cards (pm-sudo-kiran-6609ed); stripe-fill numerals with repeating-linear-gradient(45deg) 6 px (pm-rneayan-474bcf). Heavy 800–900 weights only, or the fill can't read.

**المعاملات:** word ~80 % width; outline 1.5 px; scale 1.05→1; stripes 6 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** video fill · mask · clip text · نص مملوء · قناع فيديو

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-influencer-seo-ce8c33`
- `style:pm-arjunsh1607-93005d`
- `style:pm-sudo-kiran-6609ed`
- `style:pm-rneayan-474bcf`

#### 7. قدرات قريبة في العائلة

- `TYPE-64` نص بارز بظلال مكدسة / Extruded & stacked-shadow type (seen)
- `TYPE-65` أثر الصدى والنسخ المحيطية / Echo trail & outline echo stack (seen)
- `TYPE-67` نص لزج متحول / Gooey morph text (install)
- `TYPE-68` حروف منفوخة بالفيزياء / Inflated physics letterforms (install)

### `TYPE-67` — نص لزج متحول / Gooey morph text

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** الكلمات تذوب في بعضها كالسائل عبر مرشح عتبة SVG. / Words melt into each other like liquid through an SVG threshold filter.

**متى:** تبديل كلمات ناعم، علامات سائلة / soft word swaps, liquid brands.

**كيف:** feGaussianBlur + feColorMatrix alpha threshold; GSAP raises blur on the outgoing word, swaps, lowers blur on the incoming; words from a list; Figtree from Google Fonts.

**المعاملات:** blur up/down around each swap

**التثبيت:** npx -y hyperframes@0.8.164 add morph-text

**الوسوم:** gooey · morph · liquid · لزج · تحول

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/morph-text/morph-text.html`

#### 7. قدرات قريبة في العائلة

- `TYPE-65` أثر الصدى والنسخ المحيطية / Echo trail & outline echo stack (seen)
- `TYPE-66` نص مملوء بصورة أو فيديو / Image- & video-filled text (seen)
- `TYPE-68` حروف منفوخة بالفيزياء / Inflated physics letterforms (install)
- `TYPE-69` جسيمات تتجمع لتكوّن كلمة / Particles assemble into a word (seen)

### `TYPE-68` — حروف منفوخة بالفيزياء / Inflated physics letterforms

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حروف ضخمة ناعمة تنجرف وتتصادم وتنضغط وتستقر كأجسام حقيقية. / Oversized soft letters drift, collide, squash and settle like physical objects.

**متى:** أبطال مرحة وهويات جريئة بلونين / playful heroes, bold two-colour identities.

**كيف:** Strict two-colour saturated field (e.g. electric blue + white, full 100svh); Matter.js bodies per glyph group with copy/UI blocks as static obstacles; opentype.js outlines for soft-body deformation; SVG goo/dilate filter (feGaussianBlur + feColorMatrix). For video: seed the world and step a fixed dt per frame (Engine.update(engine, 1000 / fps)) — never wall-clock rAF time. Arabic: whole-word bodies to keep joins.

**المعاملات:** dt = 1000/fps; two colours; 100svh

**التثبيت:** npm i matter-js@0.20.0 opentype.js@2.0.0 # both MIT

**الوسوم:** physics · inflated · matter.js · فيزياء · منفوخ

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:matter` ← npm ls matter أو وجود node_modules/matter
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-66` نص مملوء بصورة أو فيديو / Image- & video-filled text (seen)
- `TYPE-67` نص لزج متحول / Gooey morph text (install)
- `TYPE-69` جسيمات تتجمع لتكوّن كلمة / Particles assemble into a word (seen)
- `TYPE-70` خط الخلايا: ASCII ونقاط المصفوفة / Cell-based type: ASCII blocks & dot-matrix numerals (seen)

### `TYPE-69` — جسيمات تتجمع لتكوّن كلمة / Particles assemble into a word

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** آلاف النقاط تطير من مواضع عشوائية لتملأ أشكال الحروف. / Hundreds of dots fly from random spots to fill the glyph shapes.

**متى:** ختام شعار، كشف اسم / logo endings, name reveals.

**كيف:** Sample ~300–1500 points inside the glyphs (draw the text to an offscreen canvas, keep pixels with alpha > 128 on a grid); fly particles from seeded random positions to targets with ease-out, 800 ms, per-particle delay 0–300 ms, multicoloured 2–3 px dots (pm-vanshwtfff-db0466). Reverse for a dissolve. Engine and forces: PART family. \| code (js): off.font = "900 300px Grotesk"; off.fillText("MOTION", 40, 300); const d = off.getImageData(0, 0, W, H).data, pts = []; for (let y = 0; y < H; y += 6) for (let x = 0; x < W; x += 6) if (d[(y * W + x) * 4 + 3] > 128) pts.push([x, y]); // targets on a 6 px grid

**المعاملات:** 300–1500 points; 800 ms; delay 0–300 ms; dots 2–3 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** particles · assemble · جسيمات · تجمع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-vanshwtfff-db0466`

#### 7. قدرات قريبة في العائلة

- `TYPE-67` نص لزج متحول / Gooey morph text (install)
- `TYPE-68` حروف منفوخة بالفيزياء / Inflated physics letterforms (install)
- `TYPE-70` خط الخلايا: ASCII ونقاط المصفوفة / Cell-based type: ASCII blocks & dot-matrix numerals (seen)
- `TYPE-71` كلمات مدمجة داخل اللقطة / Words embedded in footage (composition craft) (documented)

### `TYPE-70` — خط الخلايا: ASCII ونقاط المصفوفة / Cell-based type: ASCII blocks & dot-matrix numerals

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شعار أو رقم مبني من خلايا: رموز ASCII مضيئة تتجمع، أو نقاط مصفوفة 5×7. / A logo or number built from cells: glowing ASCII glyphs that assemble, or 5×7 dot-matrix digits.

**متى:** هويات تقنية، لوحات نتائج، ريترو / tech identities, scoreboards, retro.

**كيف:** ASCII assemble: rasterise the logo to a ~60 × 40 grid (cells 10–14 px); each cell shows a random glyph from A–Z0–9%#@ or a solid block; cells fly from random positions with random glyphs to the final grid over 1.2–1.5 s, staggered by distance, amber #f2c230 + white, bloom 6–10 px (pm-kyonax-on-tech-aabc1d). Dot matrix: digits from 5 × 7 square cells in lime with a 20 % gap, cells flicker on (pm-robvjourney-ce3e1a) or pop in scale (pm-sudiyasa-f48ac9).

**المعاملات:** 60×40 cells, 10–14 px; 1.2–1.5 s; 5×7 cells, gap 20 %

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ascii · dot matrix · cells · مصفوفة نقاط · ASCII

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-kyonax-on-tech-aabc1d`
- `style:pm-robvjourney-ce3e1a`
- `style:pm-sudiyasa-f48ac9`

#### 7. قدرات قريبة في العائلة

- `TYPE-68` حروف منفوخة بالفيزياء / Inflated physics letterforms (install)
- `TYPE-69` جسيمات تتجمع لتكوّن كلمة / Particles assemble into a word (seen)
- `TYPE-71` كلمات مدمجة داخل اللقطة / Words embedded in footage (composition craft) (documented)
- `TYPE-72` نص على حلقات ومدارات / Text rings & orbiting words (seen)

### `TYPE-71` — كلمات مدمجة داخل اللقطة / Words embedded in footage (composition craft)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قواعد تجعل الكلمة تبدو جزءًا من المشهد المصوَّر لا ملصقًا فوقه. / Rules that make a word sit inside the filmed scene instead of on top of it.

**متى:** عناوين داخل لقطات حقيقية / titles placed inside real shots.

**كيف:** Size vs text length and frame-height-relative sizing; named moves per word group; narrative arcs; position and layer vocabulary (behind the subject, on a surface, in the air); contact shadows along the scene's light; blur matched to the depth of field.

**المعاملات:** size ∝ frame height; DOF-matched blur

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** embedded · footage · composition · مدمج · لقطة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/skills/embedded-captions/references/composition-craft.md`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/references/typographic-moves.md`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/references/aesthetic-principles.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-69` جسيمات تتجمع لتكوّن كلمة / Particles assemble into a word (seen)
- `TYPE-70` خط الخلايا: ASCII ونقاط المصفوفة / Cell-based type: ASCII blocks & dot-matrix numerals (seen)
- `TYPE-72` نص على حلقات ومدارات / Text rings & orbiting words (seen)
- `TYPE-73` نفق النص ودوامته / Circular text tunnel & spiral vortex (seen)

### `TYPE-72` — نص على حلقات ومدارات / Text rings & orbiting words

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمات على مسارات دائرية تدور بسرعات واتجاهات متعاكسة حول مركز أو صورة. / Words on circular paths rotating at different speeds and opposite directions around a centre or portrait.

**متى:** شعارات دائرية، مهارات حول صورة شخصية، فكرة «مدار» / badges, skills around a portrait, orbit metaphors.

**كيف:** SVG <textPath> on circles (or tilted ellipses), ‘·’ separators, inner rings smaller, alternate directions. Tunings: 3–4 rings at 6–12°/s alternating with a centre accent dot (pm-leadnotifi-e83f94); orbit caption at 1.25× portrait radius, 20°/s, 12 px tracked (pm-blushpetal795-0c85c2); 3 rings at 15°/s with 3D tilt (pm-umangratani-57f86a); circle at ~1.3× the sun's radius with an arc + ticks every 6° drawn via stroke-dashoffset as words appear (pm-samaote-5e2fc2); spinning disc with radial streaks (pm-johnsavage-ai-b091c0); max 2 opposing rotations, 15°/s (brief pm-monokern-ade5b6). Orbiting words: words on rings with rotation = angle + 90°, 20–60°/s, bold italic serif alternating yellow/pink/cream (pm-gizakdag-b8c59e); glyphs on 2–3 ellipses tilted 30–70°, 3–4 rings, 0.1 rev/s, ring thickness modulated by the audio waveform (pm-ajith-io-4c248f). Idea: rings at 12 / −18 / 24°/s tighten radius 420 → 0 over 1400 ms ease-in into a column (brief pm-marouanegazouzi-6071d5). \| code (html): <svg viewBox="-500 -500 1000 1000"><defs><path id="r1" d="M-360,0a360,360 0 1,1 720,0a360,360 0 1,1 -720,0"/></defs> <g id="ring1"><text font-family="JetBrains Mono" font-size="28" letter-spacing="6" fill="#f2f0ea"> <textPath href="#r1">MOTION · TYPE · RHYTHM · MOTION · TYPE · RHYTHM ·</textPath></text></g></svg> <!-- per frame: ring1.setAttribute("transform", `rotate(${12 * t})`); ring2 at −9°/s -->

**المعاملات:** 6–60°/s; 3–4 rings; radius 1.25–1.3× subject

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** circular text · textPath · orbit · rings · نص دائري · مدار · حلقات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-leadnotifi-e83f94`
- `style:pm-blushpetal795-0c85c2`
- `style:pm-gizakdag-b8c59e`
- `kosif-tool/styles/pm-monokern-ade5b6/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-70` خط الخلايا: ASCII ونقاط المصفوفة / Cell-based type: ASCII blocks & dot-matrix numerals (seen)
- `TYPE-71` كلمات مدمجة داخل اللقطة / Words embedded in footage (composition craft) (documented)
- `TYPE-73` نفق النص ودوامته / Circular text tunnel & spiral vortex (seen)
- `TYPE-74` أسطوانة نص ثلاثية الأبعاد وشرائط حلزونية / 3D text cylinder & helix ribbons (seen)

### `TYPE-73` — نفق النص ودوامته / Circular text tunnel & spiral vortex

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقات نصية متحدة المركز تكبر لتعبر الكاميرا خلالها كنفق. / Concentric text rings scale up so the camera flies through them like a tunnel.

**متى:** انتقال بين فصول، افتتاحية منومة / chapter transitions, hypnotic openers.

**كيف:** 6–8 concentric textPath rings of repeated words with dot separators, alternating rotation at 20–40°/s; scale rings 1.0 → 2.5 over 1.2 s for a zoom-through; colours cycle per ring (pm-motiondsgnr-9dcfa6: #ff5020, #2f55ff, #ffc81e on #0d0e12). Spiral variant: concentric ellipse paths rotating with opacity fading outward (pm-sudo-kiran-b055de).

**المعاملات:** 6–8 rings; 20–40°/s; scale 1.0→2.5 in 1.2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tunnel · vortex · zoom-through · نفق · دوامة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-motiondsgnr-9dcfa6`
- `style:pm-sudo-kiran-b055de`

#### 7. قدرات قريبة في العائلة

- `TYPE-71` كلمات مدمجة داخل اللقطة / Words embedded in footage (composition craft) (documented)
- `TYPE-72` نص على حلقات ومدارات / Text rings & orbiting words (seen)
- `TYPE-74` أسطوانة نص ثلاثية الأبعاد وشرائط حلزونية / 3D text cylinder & helix ribbons (seen)
- `TYPE-75` جدار الشرائط المتعاكسة / Bidirectional marquee wall (seen)

### `TYPE-74` — أسطوانة نص ثلاثية الأبعاد وشرائط حلزونية / 3D text cylinder & helix ribbons

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صفوف نص تلتف حول أسطوانة أو شرائط حلزونية تمر الكاميرا بجانبها. / Rows of text wrap a rotating cylinder, or helical ribbons sweep past an orbiting camera.

**متى:** لغات متعددة، قوائم مزايا، افتتاحيات تقنية / many languages, feature lists, tech openers.

**كيف:** Rows of text on a rotateY ring, neighbouring rows in opposite directions, 10 s per turn (pm-3xtihor-0f6911); letters on a circle with rotateY + translateZ, the group rotates and back letters read mirrored (pm-ultimaxbt-bbebf5); language names along 3 neon helical tubes (pink/green/blue), helix radius 2–4 units, 1 turn per 3 s, camera orbiting so ribbons sweep past with motion blur (pm-ajith-io-4c248f). CSS 3D: transform-style: preserve-3d; glyph i at rotateY(i·360/N) translateZ(R). For true 3D see the 3D family.

**المعاملات:** 10 s/turn; helix r 2–4; 1 turn / 3 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** 3d text · cylinder · helix · أسطوانة · حلزون

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-3xtihor-0f6911`
- `style:pm-ultimaxbt-bbebf5`
- `style:pm-ajith-io-4c248f`

#### 7. قدرات قريبة في العائلة

- `TYPE-72` نص على حلقات ومدارات / Text rings & orbiting words (seen)
- `TYPE-73` نفق النص ودوامته / Circular text tunnel & spiral vortex (seen)
- `TYPE-75` جدار الشرائط المتعاكسة / Bidirectional marquee wall (seen)
- `TYPE-76` شريط مائل وجدار منظوري / Tilted ticker band & perspective word wall (seen)

### `TYPE-75` — جدار الشرائط المتعاكسة / Bidirectional marquee wall

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صفوف من الكلمة نفسها تنزلق باتجاهات وسرعات متعاكسة وتتبدل بين ممتلئ ومفرّغ وملوّن. / Rows of the same word slide in opposite directions and speeds, alternating filled, outlined and accent.

**متى:** فواصل حماسية، خلفيات علامة، نهايات / hype breaks, brand backdrops, end cards.

**كيف:** 5–9 rows, dot separators, alternate fill/outline/accent; loop seamlessly by translating modulo one repeat width. Tunings: 5 rows at 200–400 px/s, stroke 2 px (pm-shinskinakamoto-20190b); 6–8 rows blue-on-white / white-on-red, row height ~13 % (pm-shneural-2abdfa); 9 rows at 400–800 px/s with velocity blur (pm-ndhabarde11-f155b4); 6–8 rows at 80–300 px/s varying weight/colour grey/white/accent (pm-levabashidze-2d713a); bold/outline-grey alternation with a band overlay (pm-raphaelaubryy-4b137e); a circular ‘lens’ mask showing the rows recoloured yellow, 100–200 px/s (pm-kangaroohere-b10f8d); filled/outlined tag-pill rows at 40 px/s (pm-techyoutbe-945b56); star separators (pm-topi-003-b0e12c); a continuous red ticker at 60 px/s (pm-henkpoley-3d3407). Idea: three lanes at speed ratio 1 : 0.7 : 0.45 fading over the last 120 px (brief pm-danilowm-d3720d). \| code (js): rows.forEach((r, i) => { // seamless loop in either direction const dir = i % 2 ? 1 : -1; const off = (((dir * t * r.speed) % r.repeatW) + r.repeatW) % r.repeatW; r.el.style.transform = `translateX(${-off}px)`; // el holds ≥2 copies of the phrase });

**المعاملات:** 5–9 rows; 40–800 px/s; stroke 1.5–2 px; row ~13 % height

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** marquee · ticker · type wall · شريط · جدار نصي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-shinskinakamoto-20190b`
- `style:pm-ndhabarde11-f155b4`
- `style:pm-kangaroohere-b10f8d`
- `kosif-tool/styles/pm-danilowm-d3720d/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-73` نفق النص ودوامته / Circular text tunnel & spiral vortex (seen)
- `TYPE-74` أسطوانة نص ثلاثية الأبعاد وشرائط حلزونية / 3D text cylinder & helix ribbons (seen)
- `TYPE-76` شريط مائل وجدار منظوري / Tilted ticker band & perspective word wall (seen)
- `TYPE-77` جدار نص يندفع وينضغط إلى شعار / Text-wall rush & compress into a logo (idea)

### `TYPE-76` — شريط مائل وجدار منظوري / Tilted ticker band & perspective word wall

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريط نصي مائل يعبر الإطار، أو جدار كلمات على مستوى مائل بمنظور. / A tilted text band crossing the frame, or a word wall on a plane tilted in perspective.

**متى:** أغلفة ريلز، إعلانات شبابية / reel covers, youthful ads.

**كيف:** Strip rotated −4° with a repeating mono slogan and ‘///’ separators scrolling at 100 px/s (pm-robvjourney-ce3e1a, lime on dark); keyword rows with dots, alternating filled/outline/accent, on a plane rotated ~−8° with perspective, rows scrolling in alternate directions at 200–400 px/s (pm-prasenx-8d9323).

**المعاملات:** −4° / −8°; 100–400 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tilted · ticker · perspective · مائل · منظور

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-robvjourney-ce3e1a`
- `style:pm-prasenx-8d9323`

#### 7. قدرات قريبة في العائلة

- `TYPE-74` أسطوانة نص ثلاثية الأبعاد وشرائط حلزونية / 3D text cylinder & helix ribbons (seen)
- `TYPE-75` جدار الشرائط المتعاكسة / Bidirectional marquee wall (seen)
- `TYPE-77` جدار نص يندفع وينضغط إلى شعار / Text-wall rush & compress into a logo (idea)
- `TYPE-78` كلمات كعمارة ودوران الأرباع / Words as architecture & quadrant rotation (seen)

### `TYPE-77` — جدار نص يندفع وينضغط إلى شعار / Text-wall rush & compress into a logo

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدار فقرات يندفع نحو العدسة ثم ينطوي في عنوان واحد تصنع خطوطه الشعار. / A wall of paragraphs rushes at the lens, then folds into one headline whose strokes form the logo.

**متى:** ختام فيلم علامة / brand-film finale.

**كيف:** translateZ rush with cubic-bezier(0.65,0,0.35,1) over 1200 ms, then squeeze to one line and morph strokes into the mark (SHAPE family for the morph).

**المعاملات:** 1200 ms; cubic-bezier(0.65,0,0.35,1)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** text wall · rush · logo · جدار نص · شعار

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-tool/styles/pm-itisrazak-3ad902/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-75` جدار الشرائط المتعاكسة / Bidirectional marquee wall (seen)
- `TYPE-76` شريط مائل وجدار منظوري / Tilted ticker band & perspective word wall (seen)
- `TYPE-78` كلمات كعمارة ودوران الأرباع / Words as architecture & quadrant rotation (seen)
- `TYPE-79` عنوان سينمائي متباعد الحروف / Letter-spaced cinematic title (proven)

### `TYPE-78` — كلمات كعمارة ودوران الأرباع / Words as architecture & quadrant rotation

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمات ثقيلة تدور لتصبح أعمدة وعتبات بناء على شبكة. / Heavy words rotate to become columns and lintels of a building on a grid.

**متى:** مفاهيم «البناء» والبنية / ‘building’ and structure metaphors.

**كيف:** Rotate bold words −90° to stand as columns, another word as lintel/floor, all grid-snapped (pm-gdgtify-287ddf). Idea variant: letters rotate 90° into quadrants, cubic-bezier(0.76,0,0.24,1), 700 ms, 120 ms stagger, 220 px (brief pm-marouanegazouzi-6071d5).

**المعاملات:** −90°; grid-snap; 700 ms / 120 ms stagger

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** architecture · rotation · grid · عمارة · دوران

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-gdgtify-287ddf`
- `kosif-tool/styles/pm-marouanegazouzi-6071d5/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-76` شريط مائل وجدار منظوري / Tilted ticker band & perspective word wall (seen)
- `TYPE-77` جدار نص يندفع وينضغط إلى شعار / Text-wall rush & compress into a logo (idea)
- `TYPE-79` عنوان سينمائي متباعد الحروف / Letter-spaced cinematic title (proven)
- `TYPE-80` بطاقة عنوان هادئة وقفل الشعار / Calm title card & lockup (install)

### `TYPE-79` — عنوان سينمائي متباعد الحروف / Letter-spaced cinematic title

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان فيلم هادئ: أحرف كبيرة رفيعة متباعدة جدًا، سطر فرعي صغير متباعد، وخط تمييز قصير دافئ. / A quiet film title: thin, widely tracked caps, a tiny tracked tagline and a short warm accent rule.

**متى:** افتتاح فيلم قصير أو وثائقي / opening a short film or documentary.

**كيف:** Proven code (MIDNIGHT, a 12 s 2.5D short): SVG <text> 43 px, weight 300, letter-spacing 10, #dcebe5; tagline 10 px, letter-spacing 4, #84afb5; 49 px accent rule #ed9f64, 2 px; group opacity 1 − smooth((t − 2.2) / 1.0). Deterministic sceneSVG(t) — node test.cjs passed here: 289 geometry samples, deterministic, 1280 × 720, 12 s timeline. Serif variants: light serif caps tracked 0.5em, 1 px rule beneath, fade in 1 s, hold 2 s, fade out, #e9e4da on #060505 at 2.35 : 1 (pm-kamstudiolabs-0b0824); centred light didone at 7 % H with wide tracking, 80 px × 1 px rule, second-language subtitle, micro tagline 1.2 % H tracked 0.3em, 1 s fade over the final wide (pm-axtonliu-0b861d); letter-spaced per-letter reveal at 0.4em, 60–90 ms stagger, opacity + 4 px rise for held notes (pm-samaote-5e2fc2). Latin only — never track Arabic. \| code (js): const title = 1 - smooth((t - 2.2) / 1.0); // smooth = smoothstep clamped 0..1 svg += `<g opacity="${title}"><text x="88" y="139" fill="#dcebe5" font-size="43" font-weight="300" letter-spacing="10">MIDNIGHT</text><text x="91" y="165" fill="#84afb5" font-size="10" letter-spacing="4"> A LITTLE COURAGE. A VERY BIG CITY.</text><path d="M92 183h49" stroke="#ed9f64" stroke-width="2"/></g>`;

**المعاملات:** 43 px / w300 / ls 10; tagline 10 px / ls 4; rule 49×2 px #ed9f64; fade 1 s from 2.2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cinematic title · tracking · film · serif · عنوان سينمائي · تباعد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:142`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/test.cjs`
- `style:pm-kamstudiolabs-0b0824`
- `style:pm-axtonliu-0b861d`

#### 7. قدرات قريبة في العائلة

- `TYPE-77` جدار نص يندفع وينضغط إلى شعار / Text-wall rush & compress into a logo (idea)
- `TYPE-78` كلمات كعمارة ودوران الأرباع / Words as architecture & quadrant rotation (seen)
- `TYPE-80` بطاقة عنوان هادئة وقفل الشعار / Calm title card & lockup (install)
- `TYPE-81` بطاقات الفصول والأرقام الضخمة / Numbered chapter blocks & giant-number cards (seen)

### `TYPE-80` — بطاقة عنوان هادئة وقفل الشعار / Calm title card & lockup

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Component Apache-2.0; it loads gsap@3.14.2 from jsdelivr under the GSAP standard ‘no charge’ licence. |

**ما هي:** بطاقة استراحة: حركة واحدة متحفظة ثم سكون حقيقي، مع خط رفيع يُرسم وعين أحادية المسافة. / A breather card: exactly one restrained move, then true stillness, with a hairline rule and a mono kicker.

**متى:** بين المشاهد الكثيفة، شاشة المبدأ، الشعار الختامي / between dense scenes, principle cards, end lockups.

**كيف:** titlecard-calm: mono kicker + generous grotesk headline fade up, drift almost imperceptibly, exit clean (e.g. ‘Less, but better’ / ‘DESIGN PRINCIPLE’). titlecard-lockup: kicker fades, wordmark settles centre, hairline rule draws L → R, mono label fades, then stillness (rule show\|hide, exit none\|fade\|up). Blueprint titlecard-reveal (3–5 s): one restrained move then a still hold, or a chain of 2–3 near-still cards by hard cuts.

**المعاملات:** 3–5 s; one move; hairline rule L→R

**التثبيت:** npx -y hyperframes@0.8.164 add titlecard-lockup # also titlecard-calm

**الوسوم:** title card · lockup · calm · بطاقة عنوان · هادئ

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-one/vendor/hyperframes/registry/components/titlecard-calm/titlecard-calm.html`
- `kosif-one/vendor/hyperframes/registry/components/titlecard-lockup/titlecard-lockup.html`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/titlecard-reveal.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-78` كلمات كعمارة ودوران الأرباع / Words as architecture & quadrant rotation (seen)
- `TYPE-79` عنوان سينمائي متباعد الحروف / Letter-spaced cinematic title (proven)
- `TYPE-81` بطاقات الفصول والأرقام الضخمة / Numbered chapter blocks & giant-number cards (seen)
- `TYPE-82` الشرائط السفلية ولوحات الأسماء / Lower-thirds & name plates (ready)

### `TYPE-81` — بطاقات الفصول والأرقام الضخمة / Numbered chapter blocks & giant-number cards

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عين مرقمة وخط رفيع يكبر وعنوان مكثف وفقرة قصيرة، أو رقم ضخم مع شرح هادئ. / A numbered eyebrow, a growing rule, a condensed title and a short paragraph — or a giant number with a calm caption.

**متى:** شرح بفصول، وثائقي بيانات / chaptered explainers, data documentaries.

**كيف:** Thin yellow rule 200 × 2 px grows, mono eyebrow ‘NN · TOPIC’, two-line condensed caps title 800, then a 3–4-line paragraph, top-left safe area, stagger 150 ms (pm-blueoctopusai-dd17bd: #f2d21b on #070911); ‘05 BENCHMARKS’ blue small caps 0.15em over a 2-line headline (pm-rammanq-f5a90f); ‘01’ small index + bold short sentence top-left (pm-miskinho-443898); ‘n of 13’ + bold headline + 2-line body bottom-left (pm-mdaman010-e7226a); eyebrow ‘0n · TOPIC’ in mono, a 25 %-height numeral (600) in deep red or black, 2-line bold caption, mono footnote with raw counts, count-up 800 ms (pm-palashbagchi11-0a4b6b); bold grotesk number + italic serif sentence + tiny tracked grey mono footnote under an orange mono chapter label, ratio 14 : 4 : 1.2 vh (pm-nolkeeg-bf062e). Hollow-numeral chapter cards: TYPE-62.

**المعاملات:** rule 200×2 px; stagger 150 ms; numeral 25 % height; 14:4:1.2 vh

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** chapter · eyebrow · numbered · فصل · عين مرقمة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-blueoctopusai-dd17bd`
- `style:pm-palashbagchi11-0a4b6b`
- `style:pm-nolkeeg-bf062e`
- `style:pm-rammanq-f5a90f`

#### 7. قدرات قريبة في العائلة

- `TYPE-79` عنوان سينمائي متباعد الحروف / Letter-spaced cinematic title (proven)
- `TYPE-80` بطاقة عنوان هادئة وقفل الشعار / Calm title card & lockup (install)
- `TYPE-82` الشرائط السفلية ولوحات الأسماء / Lower-thirds & name plates (ready)
- `TYPE-83` أنظمة الأصوات الطباعية / Multi-voice type systems (seen)

### `TYPE-82` — الشرائط السفلية ولوحات الأسماء / Lower-thirds & name plates

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard ‘no charge’ licence (vendored gsap.min.js) — fine for client work, not for tools that compete with GSAP. |

**ما هي:** اسم ودور في المنطقة السفلية الآمنة بشريط تمييز ينمو، ويتحول تلقائيًا إلى RTL مع العربية. / Name and role in the lower safe area behind a growing accent bar, auto-RTL for Arabic.

**متى:** مقابلات، متحدثون، عناوين مقطوعات / interviews, speakers, track titles.

**كيف:** MOTION.lowerThird(tl, root, at, {title, sub, accent: '#E7B65A', size: 44, side, inset: 72, bottom: 160, hold}) → 4 px bar grows 0 → 120 px in 0.4 s, title 44 px/700 rises 16 px at +0.12 s, sub at 0.55× size at +0.24 s, exit −10 px in 0.3 s; RTL and right-side placement switch on automatically for Arabic. Seen: 4 px yellow #f2c230 vertical bar + 14 px kicker ‘No.N · Composer’ + bold 36 px white title + italic subtitle, sliding in 400 ms on each track change (pm-gorden-sun-041f56); ‘NAME · ACTION’ 16 px caps tracked 0.4em, opacity 0.8, bottom-centre, crossfade 400 ms (pm-nft-chen-5f8bb0); skewed dark bar with a colour tab sliding in 0.3 s (pm-allforbigfire-86ff3c); brand stripe + one heavy italic uppercase word with a period + tiny joke subline, bottom-left at 8 % / 2 % height, 6 % margin (pm-spearwtf-3c1fd1); mono era subtitle tracked 0.3em with ‘·’ and an arrow between years, ~1 % height at 70 %, fading in 0.8 s after the title (pm-kloss-xyz-b9b3f6); vertical move-name column + tiny English (pm-chrisjdimarco-f068db).

**المعاملات:** bar 4 px → 120 px / 0.4 s; title 44 px +0.12 s; sub 0.55× +0.24 s; bottom 160 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lower third · name plate · caption · شريط سفلي · اسم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-studio/motion/kit/motion-kit.js:562`
- `100-superskills/skills/kosif-montage-motion/SKILL.md:95`
- `style:pm-gorden-sun-041f56`
- `style:pm-nft-chen-5f8bb0`

#### 7. قدرات قريبة في العائلة

- `TYPE-80` بطاقة عنوان هادئة وقفل الشعار / Calm title card & lockup (install)
- `TYPE-81` بطاقات الفصول والأرقام الضخمة / Numbered chapter blocks & giant-number cards (seen)
- `TYPE-83` أنظمة الأصوات الطباعية / Multi-voice type systems (seen)
- `TYPE-84` مظهر الترجمة حسب النبرة والعالم / Caption look by tone & theme (seen)

### `TYPE-83` — أنظمة الأصوات الطباعية / Multi-voice type systems

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لكل عاطفة صوت طباعي: أوامر بخط مكثف أسود، سرد بخط عريض، نظام بخط أحادي، همس بسيريف مائل. / One typographic voice per emotion: condensed black for commands, wide sans for narration, mono for system, italic serif for whispers.

**متى:** أفلام بشخصية قوية، أغانٍ، بيانات / films with strong character, songs, manifestos.

**كيف:** Max 3–4 voices, one per card, switched on the beat. Four voices: condensed black caps (commands), wide geometric sans 800 lowercase (narration), mono (system/UI), italic serif (intimate asides) (pm-kloss-xyz-15182a). Three voices: ultra-black condensed scream, wide extended ExtraBold secondary, mono crumbs; tracking −40…−80 for display, +20 for mono (pm-techhalla-7acbc2: #c5fc34 / #ff2bd6 on #0a0a0a). Editorial: condensed serif for headlines and quotes (italic for emphasis), monospace only for user-typed text, tracked small-caps sans labels at 1.2 % H, 0.12em, coloured dot bullets, 3 families max (pm-henkvaness-0e06af). Whisper vs shout: light italic serif ~5 % H for soft lines, black soft serif lowercase 20–25 % H for climactic words, per lyric emotion (pm-samaote-5e2fc2). Light serif narration vs heavy caps keyword at 1 : 5 (pm-gdgtify-287ddf); marker-script display + giant numerals ~2.5× with tracked mono metadata at ~1/6 size, 0.15em (pm-sarut0bisasuke-cefa43). Mixed-typeface sentence — every word a different family/size/position, hero word 25 % H, ~200 ms stagger, one word retyped (pm-fionntobin-97b7af) — a deliberate one-sentence exception to the two-family rule.

**المعاملات:** 3–4 voices; one per card; display −40…−80 / mono +20 tracking

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** type system · voices · pairing · أصوات طباعية · نظام

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-kloss-xyz-15182a`
- `style:pm-techhalla-7acbc2`
- `style:pm-henkvaness-0e06af`
- `style:pm-samaote-5e2fc2`

#### 7. قدرات قريبة في العائلة

- `TYPE-81` بطاقات الفصول والأرقام الضخمة / Numbered chapter blocks & giant-number cards (seen)
- `TYPE-82` الشرائط السفلية ولوحات الأسماء / Lower-thirds & name plates (ready)
- `TYPE-84` مظهر الترجمة حسب النبرة والعالم / Caption look by tone & theme (seen)
- `TYPE-85` تكديس هرمي بأحجام متدرجة / Size-stepped hierarchy stacks (seen)

### `TYPE-84` — مظهر الترجمة حسب النبرة والعالم / Caption look by tone & theme

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر خط الترجمة وحركتها من نبرة النص، وبدّلها مع عالم كل مقطع. / Pick caption face and motion from the transcript's tone, and swap them per segment's world.

**متى:** أي فيديو بترجمة / any captioned video.

**كيف:** Tone map: hype = heavy condensed 800–900, scale-pop back.out(1.7) 0.1–0.2 s, 72–96 px; corporate = clean sans 600–700, fade + slide power3.out 0.3 s, 56–72 px; tutorial = mono/sans 500–600 typewriter 0.4–0.5 s, 48–64 px; storytelling = serif 400–500 slow fade power2. Per-word emphasis on brand names, numbers, CAPS, emotional words, CTA. Theme map per segment: italic serif for lo-fi, bubble 3D for viral, slab serif sepia for cartoon, comic balloon for manga, engraved gold serif for a card (pm-sab8a-364a5a). Diary system: amber #F2B84B with a 50 % #1A1A1A shadow, title 8 % / subtitle 5 % of frame height for 3–4 s, bottom comment 5 % ≤18 chars/line, a top-left list adding one line per spoken item at 8 % margin. Word-timing mechanics live in SYNC.

**المعاملات:** hype 72–96 px / 0.1–0.2 s; corporate 56–72 / 0.3 s; tutorial 48–64 / 0.4–0.5 s; diary #F2B84B

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** captions · tone · subtitles · ترجمة · نبرة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`
- `style:pm-sab8a-364a5a`
- `kosif-atlas/skills/1096-akbun-editvideo/2462-davinciresolve-style-project/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-82` الشرائط السفلية ولوحات الأسماء / Lower-thirds & name plates (ready)
- `TYPE-83` أنظمة الأصوات الطباعية / Multi-voice type systems (seen)
- `TYPE-85` تكديس هرمي بأحجام متدرجة / Size-stepped hierarchy stacks (seen)
- `TYPE-86` عنوان سيريف متراكب يُبنى كلمة كلمة / Stacked serif title build (seen)

### `TYPE-85` — تكديس هرمي بأحجام متدرجة / Size-stepped hierarchy stacks

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صفوف تتناقص أحجامها بنسبة ثابتة: ملصق مهرجان أو سلّم أحجام الخط. / Rows that shrink by a fixed step: a festival lineup or a type-scale staircase.

**متى:** قوائم مشاركين، شرح أنظمة تصميم / lineups, design-system explainers.

**كيف:** Festival lineup: headliner in wide 900 caps, then rows at 100 % → 45 % → 30 % → 22 % → 18 % joined by middle dots; rows stagger 100 ms with fade + translateY 12 px; line-height 1.25; max width 90 % (pm-gonzalomacagno-2de1a9: #1c1838 on #c4a4ed / #f3daed). Type-scale staircase: a row of ‘Aa’ samples at a ~1.2× geometric ratio, 10–11 steps, baseline-aligned, popping in L → R with 60–80 ms stagger, mono token + ratio labels in red/grey beneath (pm-ddryo-loos-300829).

**المعاملات:** 100→45→30→22→18 %; stagger 60–100 ms; ratio ~1.2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lineup · hierarchy · type scale · هرم · سلم الأحجام

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-gonzalomacagno-2de1a9`
- `style:pm-ddryo-loos-300829`

#### 7. قدرات قريبة في العائلة

- `TYPE-83` أنظمة الأصوات الطباعية / Multi-voice type systems (seen)
- `TYPE-84` مظهر الترجمة حسب النبرة والعالم / Caption look by tone & theme (seen)
- `TYPE-86` عنوان سيريف متراكب يُبنى كلمة كلمة / Stacked serif title build (seen)
- `TYPE-87` بطاقة حرف أو كلمة بملء الشاشة / Full-bleed glyph & word cards (seen)

### `TYPE-86` — عنوان سيريف متراكب يُبنى كلمة كلمة / Stacked serif title build

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أربع كلمات متراكبة بأوزان متبادلة تظهر واحدة كل ~0.8 ث ثم تذوب في شعار هادئ. / Four stacked words in alternating weights appear one every ~0.8 s, then dissolve into a calm tagline.

**متى:** أفلام استرخاء وطبيعة وتأمل / relaxation, nature and meditation films.

**كيف:** Didone serif, centred: bold caps 72 px / light caps 40 / light caps 40 / bold caps 72, line-height 0.95; one word per ~0.8 s with fade + tiny rise; crossfade to one lowercase tagline (‘just breathe.’ ~36 px) and a tracked 16 px caption (pm-nft-chen-5f8bb0: #2a1c38 ground, #8a5cc8 / #f0a050 accents).

**المعاملات:** 72/40/40/72 px; lh 0.95; 0.8 s per word

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** serif · stacked · calm · سيريف · متراكب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-86` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-nft-chen-5f8bb0`

#### 7. قدرات قريبة في العائلة

- `TYPE-84` مظهر الترجمة حسب النبرة والعالم / Caption look by tone & theme (seen)
- `TYPE-85` تكديس هرمي بأحجام متدرجة / Size-stepped hierarchy stacks (seen)
- `TYPE-87` بطاقة حرف أو كلمة بملء الشاشة / Full-bleed glyph & word cards (seen)
- `TYPE-88` تجميع المعادلات / Equation assembly (seen)

### `TYPE-87` — بطاقة حرف أو كلمة بملء الشاشة / Full-bleed glyph & word cards

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حرف واحد أو كلمة واحدة ضخمة تملأ الإطار كفاصل بين المشاهد. / One glyph or one huge word fills the frame as a break between scenes.

**متى:** فواصل الفصول، بداية فكرة جديدة / chapter breaks, a new idea.

**كيف:** One ultra-bold serif glyph at ~80 % height, black on paper-white with vignette 0.5 and 6 % grain, or white on black (pm-majin-appsheet-2d3c1a); flat orange field, heavy black word + underlined italic serif sub, scale 1.1 → 1 (pm-itsuki-dev-10942d).

**المعاملات:** glyph 80 % height; vignette 0.5; grain 6 %

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** full-bleed · glyph · card · حرف ضخم · فاصل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-87` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-majin-appsheet-2d3c1a`
- `style:pm-itsuki-dev-10942d`

#### 7. قدرات قريبة في العائلة

- `TYPE-85` تكديس هرمي بأحجام متدرجة / Size-stepped hierarchy stacks (seen)
- `TYPE-86` عنوان سيريف متراكب يُبنى كلمة كلمة / Stacked serif title build (seen)
- `TYPE-88` تجميع المعادلات / Equation assembly (seen)
- `TYPE-89` استايلات حركية في الكتالوج / Catalog kinetic styles: brutalist · minimal · typewriter (documented)

### `TYPE-88` — تجميع المعادلات / Equation assembly

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حدود المعادلة تظهر بالتتابع حتى تكتمل. / An equation's terms fade in one after another until it is complete.

**متى:** شرح رياضي أو علمي / math and science explainers.

**كيف:** Typeset as real vector type (KaTeX/MathJax to SVG, or hand-set SVG), then fade terms in reading order; keep operators still. Timing was not measured in the reference — start from the 70–120 ms word stagger (TYPE-43) and hold per TYPE-03. Never let an image model draw it (TYPE-10).

**المعاملات:** term-by-term; stagger from 70–120 ms (unmeasured)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** equation · math · katex · معادلة · رياضيات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-88` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `style:pm-math-files-39c9d0`

#### 7. قدرات قريبة في العائلة

- `TYPE-86` عنوان سيريف متراكب يُبنى كلمة كلمة / Stacked serif title build (seen)
- `TYPE-87` بطاقة حرف أو كلمة بملء الشاشة / Full-bleed glyph & word cards (seen)
- `TYPE-89` استايلات حركية في الكتالوج / Catalog kinetic styles: brutalist · minimal · typewriter (documented)
- `TYPE-90` تزويجات ولوحات جاهزة للعناوين / Preset pairings & palettes for title systems (documented)

### `TYPE-89` — استايلات حركية في الكتالوج / Catalog kinetic styles: brutalist · minimal · typewriter

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة استايلات طباعية أصلية في KOSIF لها وصفات مكتوبة وأمر scaffold يعمل هنا. / Three original KOSIF type styles with written recipes and a scaffold command that runs here.

**متى:** عندما يطلب المالك أحد هذه الأساليب بالاسم / when the owner names one of these looks.

**كيف:** python3 tools/kosif.py scaffold <brutalist\|minimal\|typewriter> <dir> --starter html-canvas (verified here: writes STYLE.md, PLAN.md, REQUEST.md, words.json, TEST_REPORT.md + the html-canvas starter), then node tools/render_html.cjs --preview. Brutalist: hero 120–220 px weight 900, hard cuts on beats, few colours, no easing softness. Minimal: 24 px grid, ≥30 % empty frame, two sizes, entrances 300–450 ms ease-out. Typewriter: 25–45 cps ±20 % seeded jitter, 250–400 ms pause after punctuation, caret 530 ms; Arabic by word or mask. The motion itself is written from each SKILL.md — no prebuilt animation ships.

**المعاملات:** brutalist 120–220 px/900; minimal 24 px grid ≥30 % empty; typewriter 25–45 cps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** brutalist · minimal · typewriter · scaffold · بروتالي · مينيمال

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-89` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-tool/styles/brutalist/SKILL.md`
- `kosif-tool/styles/minimal/SKILL.md`
- `kosif-tool/styles/typewriter/SKILL.md`
- `kosif-tool/playbooks/kinetic-type.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-87` بطاقة حرف أو كلمة بملء الشاشة / Full-bleed glyph & word cards (seen)
- `TYPE-88` تجميع المعادلات / Equation assembly (seen)
- `TYPE-90` تزويجات ولوحات جاهزة للعناوين / Preset pairings & palettes for title systems (documented)
- `TYPE-U01` خط Poppins مضمّن / Poppins bundled (OFL) (proven)

### `TYPE-90` — تزويجات ولوحات جاهزة للعناوين / Preset pairings & palettes for title systems

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | Clash Display / Satoshi come from Fontshare under the Fontshare licence (not OFL) — check before embedding. |

**ما هي:** اثنا عشر مزيجًا جاهزًا من الخطوط والألوان، ومثالان من HyperFrames، تبدأ منها أي هوية عناوين. / Twelve ready font + colour positions and two HyperFrames examples to start any title system from.

**متى:** عندما لا يوجد دليل هوية / when there is no brand guide.

**كيف:** Pair each Latin preset with an Arabic face of similar voice (heavy geometric Kufi for Bold Signal, Naskh for Paper & Ink). HyperFrames examples (style references only — their local copies lack sub-compositions): kinetic-type — 15 s, Inter on #0a0a0f, 1920 × 1080; vignelli — 10 s, 1080 × 1920, bold Helvetica with red #cc0000 on #1a1a1a. \| Bold Signal · Archivo Black + Space Grotesk · #FF5722 card on #1a1a1a ; Electric Studio · Manrope · #0a0a0a / #ffffff split, #4361ee ; Creative Voltage · Syne + Space Mono · #0066ff, #1a1a2e, neon #d4ff00 ; Dark Botanical · Cormorant + IBM Plex Sans · #0f0f0f, #e8e4df, #d4a574 / #e8b4b8 / #c9b896 ; Notebook Tabs · Bodoni Moda + DM Sans · page #f8f6f1, tabs #98d4bb #c7b8ea #f4b8c5 #a8d8ea #ffe6a7 ; Pastel Geometry · Plus Jakarta Sans · #c8d9e6, #faf9f7, pills #f0b4d4 #a8d4c4 #9b8dc4 ; Split Pastel · Outfit · #f5e6dc / #e4dff0, badges #c8f0d8 #f0f0c8 #f0d4e0 ; Vintage Editorial · Fraunces + Work Sans · #f5f3ee, #1a1a1a, #e8d4c0 ; Neon Cyber · Clash Display + Satoshi (Fontshare) · #0a0f1c, #00ffcc, #ff00aa ; Terminal Green · JetBrains Mono · #0d1117, #39d353 ; Swiss Modern · Archivo 800 + Nunito 400 · white, black, #ff3300 ; Paper & Ink · Cormorant Garamond + Source Serif 4 · #faf9f7, #1a1a1a, #c41e3a

**المعاملات:** 12 presets; 2 HF examples

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** presets · palettes · pairings · لوحات · تزويجات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-90` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-atlas/skills/345-visuals/1241-html-deck/references/style-presets.md`
- `kosif-one/vendor/hyperframes/registry/examples/vignelli/index.html`
- `kosif-one/vendor/hyperframes/registry/examples/kinetic-type/index.html`

#### 7. قدرات قريبة في العائلة

- `TYPE-88` تجميع المعادلات / Equation assembly (seen)
- `TYPE-89` استايلات حركية في الكتالوج / Catalog kinetic styles: brutalist · minimal · typewriter (documented)
- `TYPE-U01` خط Poppins مضمّن / Poppins bundled (OFL) (proven)
- `TYPE-U02` قواعد قراءة الترجمة فوق اللقطات / Caption readability rules over footage (documented)

### `TYPE-U01` — خط Poppins مضمّن / Poppins bundled (OFL)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | SIL OFL 1.1 |

**ما هي:** Poppins Regular وBold مضمنان في proofs/_shared/fonts مع OFL-Poppins.txt؛ رسمتُهما بـPillow في إثبات الرفع. — Geometric sans for Latin captions and UI labels, bundled under OFL 1.1.

**متى:** خط لاتيني نظيف للترجمات واللوحات / a clean Latin font for captions

**كيف:** ImageFont.truetype('proofs/_shared/fonts/Poppins-Bold.ttf', size)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** poppins · font · خط · latin · sans · caption

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-U01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts/Poppins-Bold.ttf`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts/OFL-Poppins.txt`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/owner-uploads-20261023/sheet.jpg`

#### 7. قدرات قريبة في العائلة

- `TYPE-89` استايلات حركية في الكتالوج / Catalog kinetic styles: brutalist · minimal · typewriter (documented)
- `TYPE-90` تزويجات ولوحات جاهزة للعناوين / Preset pairings & palettes for title systems (documented)
- `TYPE-U02` قواعد قراءة الترجمة فوق اللقطات / Caption readability rules over footage (documented)
- `TYPE-X01` نص يعبر القطع / Type that keeps moving through cuts (documented)

### `TYPE-U02` — قواعد قراءة الترجمة فوق اللقطات / Caption readability rules over footage

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied |

**ما هي:** نص أبيض عريض بظل ناعم قوي وتدرج داكن أسفل الإطار؛ ترجمة ~56 px، عبارة مفتاح ~96 px، تسميات 32–40 px؛ أسفل الوسط لا أعلى الإطار؛ نفس الارتفاع للترجمات المتتالية؛ كبسولة الكلمة المفتاح موسّطة على حدود الحبر؛ لا قطع بين لقطتين والترجمة ظاهرة؛ كل كلمة تصعد قبل وقتها بـ0.04–0.1 ث. — Readability defaults learned from creator revisions.

**متى:** ترجمات أو عناوين فوق فيديو / captions or titles over footage

**كيف:** قِس حدود الحبر بـtextbbox لا صندوق التخطيط.

**المعاملات:** 56/96/32–40 px at 1080p; words lead by 0.04–0.1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** caption · ترجمة · subtitle · readability · قراءة · size · حجم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-U02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `TYPE-90` تزويجات ولوحات جاهزة للعناوين / Preset pairings & palettes for title systems (documented)
- `TYPE-U01` خط Poppins مضمّن / Poppins bundled (OFL) (proven)
- `TYPE-X01` نص يعبر القطع / Type that keeps moving through cuts (documented)
- `TYPE-X02` ثلاث عائلات خطوط بمصدر واحد / Three font families from one source of truth (documented)

### `TYPE-X01` — نص يعبر القطع / Type that keeps moving through cuts

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | unknown (reference only) |

**ما هي:** طبقات النص التوكيدي لها حركة مستمرة خاصة (انجراف، تأرجح، تباعد حروف) مستقلة عن شبكة اللقطات، فتحمل العين عبر القطع. — Emphasis type layers carry their own continuous motion (drift, sway, tracking) independent of the shot grid, so they carry the eye across cuts.

**متى:** مونتاج متحدث مع نصوص تأكيد ولقطات مساندة — a talking-head edit with emphasis type and B-roll.

**كيف:** Enter styles: soft, blur, rise, cut, type, wipe, slam, pop, blurpop, draw, flicker; exits cut (default), blur, fade 0.12 s, drift 0.28 s. Reveal per word on the spoken word; *word* → italic serif accent. Use a readability halo instead of a hard drop shadow, and do not put dark plates under text: darken the background exposure and add a soft shadow (0 8px 48px rgba(0,0,0,.45)).

**المعاملات:** fade 0.12 s; drift exit 0.28 s; shadow 0 8 48 px α .45

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** kinetic type · continuity · cut · emphasis · نص متحرك · استمرار · قطع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/typeLayers.js`
- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-U01` خط Poppins مضمّن / Poppins bundled (OFL) (proven)
- `TYPE-U02` قواعد قراءة الترجمة فوق اللقطات / Caption readability rules over footage (documented)
- `TYPE-X02` ثلاث عائلات خطوط بمصدر واحد / Three font families from one source of truth (documented)

### `TYPE-X02` — ثلاث عائلات خطوط بمصدر واحد / Three font families from one source of truth

| الحقل | القيمة |
|---|---|
| العائلة | `typography-latin` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-latin.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | unknown (reference only) |

**ما هي:** ثلاث عائلات فقط (بلا تذييل، بتذييل، أحادية)، والوزن الثقيل وزن 800 من العائلة نفسها لا عائلة رابعة، ومصدر واحد يكتب متغيرات CSS للـDOM والـcanvas معًا. — Exactly three families (sans, serif, mono); 'heavy' is weight 800 of the sans, not a fourth family; one source writes the CSS variables for both DOM and canvas.

**متى:** أي فيلم يجمع نص DOM ونص canvas — any film mixing DOM text and canvas text.

**كيف:** Write the tokens once (CSS custom properties) and read them for canvas too, so the two can never drift; audit with a familyOf() check that every rendered run uses one of the three; pick faces from a rendered specimen in the real copy, and keep a face the client liked. Force-load every face before capture (ENG-X03).

**المعاملات:** 3 families; heavy = 800

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** font tokens · typography system · canvas · css variables · خطوط · نظام خطوط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:TYPE-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `font-fidelity-lab` · `telegram-typography-atlas` · `render-text`.
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

- `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/fonts.js`
- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`

#### 7. قدرات قريبة في العائلة

- `TYPE-U02` قواعد قراءة الترجمة فوق اللقطات / Caption readability rules over footage (documented)
- `TYPE-X01` نص يعبر القطع / Type that keeps moving through cuts (documented)

