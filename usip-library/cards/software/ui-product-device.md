# `ui-product-device` — البرمجة وبناء التطبيقات (93 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/ui-product-device.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/software.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`UI-01` العرض الصامت: الواجهة تحكي](#ui-01--العرض-الصامت-الواجهة-تحكي--silent-product-demo--the-ui-tells-the-story)
- [`UI-02` ثلاثية النية والفعل والاستجابة](#ui-02--ثلاثية-النية-والفعل-والاستجابة--intent--action--response-with-real-latency)
- [`UI-03` محتوى واجهة حقيقي ومحلي](#ui-03--محتوى-واجهة-حقيقي-ومحلي--real-locale-correct-ui-content)
- [`UI-04` إعادة بناء الشاشة كطبقات](#ui-04--إعادة-بناء-الشاشة-كطبقات--layered-screen-rebuild)
- [`UI-05` حقيبة أصول من أجزاء حقيقية](#ui-05--حقيبة-أصول-من-أجزاء-حقيقية--animation-kit-from-real-parts)
- [`UI-06` عكس الواجهة للعربية](#ui-06--عكس-الواجهة-للعربية--rtl-product-ui-mirroring)
- [`UI-07` لوحة البيانات داخل الإطار](#ui-07--لوحة-البيانات-داخل-الإطار--dashboard-composition-for-a-frame)
- [`UI-08` تشريح التفاعل الدقيق كوحدة مشهد](#ui-08--تشريح-التفاعل-الدقيق-كوحدة-مشهد--microinteraction-anatomy-as-a-beat)
- [`UI-09` مقطع حلقة لمكوّن واحد](#ui-09--مقطع-حلقة-لمكوّن-واحد--seamless-ui-component-loop-36-s)
- [`UI-10` عناوين أفعال بسيطة في الشروحات](#ui-10--عناوين-أفعال-بسيطة-في-الشروحات--plain-action-labels-in-tutorials)
- [`UI-11` مؤشر بفيزياء في motion-kit](#ui-11--مؤشر-بفيزياء-في-motion-kit--motion-kit-physics-cursor--press--typeon)
- [`UI-12` واجهة منتج على Canvas بدالة draw(t)](#ui-12--واجهة-منتج-على-canvas-بدالة-drawt--canvas-product-ui-drawt-recipe)
- [`UI-13` تصميم حركة المؤشر](#ui-13--تصميم-حركة-المؤشر--cursor-choreography-rules)
- [`UI-14` حلقة الضغط والتموج](#ui-14--حلقة-الضغط-والتموج--press-ring--click-ripple)
- [`UI-15` مؤشر ماك معبّر يتجه مع حركته](#ui-15--مؤشر-ماك-معبّر-يتجه-مع-حركته--expressive-directional-macos-cursor)
- [`UI-16` مؤشر بهالة لونية يلاحق هدفًا متحركًا](#ui-16--مؤشر-بهالة-لونية-يلاحق-هدفًا-متحركًا--cursor-with-accent-halo-homing-on-a-live-target)
- [`UI-17` المؤشر المغناطيسي](#ui-17--المؤشر-المغناطيسي--magnetic-cursor--magnetic-buttons)
- [`UI-18` سحب وإفلات](#ui-18--سحب-وإفلات--cursor-drag--drop)
- [`UI-19` تحديد نص ومستطيل وقائمة يمين](#ui-19--تحديد-نص-ومستطيل-وقائمة-يمين--text-select-marquee-select--context-menu)
- [`UI-20` مؤشرات متعاونين بأسمائها](#ui-20--مؤشرات-متعاونين-بأسمائها--named-multiplayer-cursors)
- [`UI-21` مؤشر وكيل ذكي](#ui-21--مؤشر-وكيل-ذكي--ai-agent-cursor)
- [`UI-22` مؤشر اللمس على الهاتف](#ui-22--مؤشر-اللمس-على-الهاتف--touch-indicator-tap--swipe)
- [`UI-23` ضغط اختصار لوحة المفاتيح](#ui-23--ضغط-اختصار-لوحة-المفاتيح--keycap-shortcut-trigger)
- [`UI-24` تحكم وهدف يتغيران معًا](#ui-24--تحكم-وهدف-يتغيران-معًا--control--target-live-sync)
- [`UI-25` كتابة بإيقاع بشري](#ui-25--كتابة-بإيقاع-بشري--human-rhythm-typing-with-caret)
- [`UI-26` طلب يُكتب ثم يُرسل ثم يولّد](#ui-26--طلب-يُكتب-ثم-يُرسل-ثم-يولّد--prompt-type--submit--generate)
- [`UI-27` وكيل ينجز قائمة مهام](#ui-27--وكيل-ينجز-قائمة-مهام--agent-progress-theater--tool-call-checklist)
- [`UI-28` محادثة: فقاعات وكتابة جارية](#ui-28--محادثة-فقاعات-وكتابة-جارية--chat-thread-bubbles--typing-dots)
- [`UI-29` طرفية ومحرر كود](#ui-29--طرفية-ومحرر-كود--terminal--ide-scenes-24-theme-blocks)
- [`UI-30` لوحة أوامر وبحث يصفّي النتائج](#ui-30--لوحة-أوامر-وبحث-يصفّي-النتائج--command-palette--search-filter)
- [`UI-31` إجابة متدفقة وسجل حي](#ui-31--إجابة-متدفقة-وسجل-حي--streaming-answer--live-log)
- [`UI-32` كتابة في تطبيق الملاحظات](#ui-32--كتابة-في-تطبيق-الملاحظات--notes-app-typing-story)
- [`UI-33` جدول ردود الفعل الدقيقة](#ui-33--جدول-ردود-الفعل-الدقيقة--micro-feedback-timing-table)
- [`UI-34` ضغط ومرور بمنطق القراءة](#ui-34--ضغط-ومرور-بمنطق-القراءة--press--hover-with-reading-direction-nudges)
- [`UI-35` ضغط وتحرير زر نابض](#ui-35--ضغط-وتحرير-زر-نابض--press-release-spring-button)
- [`UI-36` قلب المفتاح وتبديل الثيم](#ui-36--قلب-المفتاح-وتبديل-الثيم--toggle-flip--theme-switch)
- [`UI-37` من التحميل إلى علامة صح](#ui-37--من-التحميل-إلى-علامة-صح--spinner--success-check)
- [`UI-38` حقل إدخال: خطأ واهتزاز ونجاح](#ui-38--حقل-إدخال-خطأ-واهتزاز-ونجاح--input-feedback-error-shake--valid-state)
- [`UI-39` هيكل لامع يتحول إلى محتوى](#ui-39--هيكل-لامع-يتحول-إلى-محتوى--skeleton-shimmer--content)
- [`UI-40` إشعارات: نظام وجزيرة ورصّة](#ui-40--إشعارات-نظام-وجزيرة-ورصّة--notifications-native-pop-dynamic-island-stacks)
- [`UI-41` تحول بطاقة إلى لوحة (FLIP)](#ui-41--تحول-بطاقة-إلى-لوحة-flip--shared-element-morph-card--panel-flip)
- [`UI-42` إعادة ترتيب قائمة وسطور](#ui-42--إعادة-ترتيب-قائمة-وسطور--flip-list-reorder--self-reordering-lines)
- [`UI-43` مؤشرات التبويب والشريط النشط](#ui-43--مؤشرات-التبويب-والشريط-النشط--tab-slide-indicator--active-rail-bar)
- [`UI-44` شريط المراحل والحلقة والتقدم](#ui-44--شريط-المراحل-والحلقة-والتقدم--stepper-progress-ring--progress-bars)
- [`UI-45` نقطة حالة بهالة وشارة مباشرة](#ui-45--نقطة-حالة-بهالة-وشارة-مباشرة--status-dot-with-halo--live-pill)
- [`UI-46` لحظة احتفال توقيعية](#ui-46--لحظة-احتفال-توقيعية--signature-celebration-moment)
- [`UI-47` ثوابت الهاتف البارامتري](#ui-47--ثوابت-الهاتف-البارامتري--parametric-phone-constants)
- [`UI-48` منظور الجهاز وسرعة دورانه](#ui-48--منظور-الجهاز-وسرعة-دورانه--device-perspective-rotation-caps--idle-hover)
- [`UI-49` دخول الجهاز وكشف البطل](#ui-49--دخول-الجهاز-وكشف-البطل--device-entrance--hero-reveal)
- [`UI-50` هاتف 2.5D على Canvas](#ui-50--هاتف-25d-على-canvas--canvas-25d-phone-drawphone)
- [`UI-51` مكوّن Device في Remotion](#ui-51--مكوّن-device-في-remotion--remotion-device-component)
- [`UI-52` تسليم بين جهازين](#ui-52--تسليم-بين-جهازين--two-device-turntable-handoff)
- [`UI-53` نافذة متصفح أو ماك وهمية](#ui-53--نافذة-متصفح-أو-ماك-وهمية--browser-chrome--macos-frame-mock)
- [`UI-54` مروحة أجهزة وانفراد الهواتف](#ui-54--مروحة-أجهزة-وانفراد-الهواتف--multi-device-splay--phone-fan-out)
- [`UI-55` آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية](#ui-55--آيفون-وماك-بوك-ثلاثيا-الأبعاد-بشاشات-حية--3d-gltf-iphone--macbook-with-live-screens)
- [`UI-56` موك أب HTML بلقطة 2×](#ui-56--موك-أب-html-بلقطة-2--htmlcss-device--package-mockup-screenshot)
- [`UI-57` قلب الهاتف وتبديل الشاشة](#ui-57--قلب-الهاتف-وتبديل-الشاشة--phone-flip-with-mid-swap)
- [`UI-58` جولة تمرير مع شروحات](#ui-58--جولة-تمرير-مع-شروحات--scroll-tour-with-callouts)
- [`UI-59` خطوط شرح قائدة](#ui-59--خطوط-شرح-قائدة--callout-leader-lines)
- [`UI-60` اقتراب يقوده المؤشر](#ui-60--اقتراب-يقوده-المؤشر--cursor-led-push-in--focus-zoom)
- [`UI-61` وصفة النقر وفتح نافذة](#ui-61--وصفة-النقر-وفتح-نافذة--click--modal-recipe)
- [`UI-62` صفحة ويب مائلة تتمرر](#ui-62--صفحة-ويب-مائلة-تتمرر--3d-tilted-webpage-scroll--perspective-pan)
- [`UI-63` جدار بطاقات واجهة يطفو بعمق](#ui-63--جدار-بطاقات-واجهة-يطفو-بعمق--floating-ui-card-wall-in-depth)
- [`UI-64` عدسة تكبير التفاصيل](#ui-64--عدسة-تكبير-التفاصيل--magnifier-lens-pass)
- [`UI-65` نقطة ساخنة مع فقاعة إرشاد](#ui-65--نقطة-ساخنة-مع-فقاعة-إرشاد--hotspot-tooltip-walkthrough)
- [`UI-66` مقارنة قبل وبعد](#ui-66--مقارنة-قبل-وبعد--beforeafter-wipe--comparison-split)
- [`UI-67` دوار الشاشات والموكاب الثابت](#ui-67--دوار-الشاشات-والموكاب-الثابت--screen-flow-carousel--sticky-mock-swap)
- [`UI-68` شبكة بنتو للميزات](#ui-68--شبكة-بنتو-للميزات--bento-feature-grid)
- [`UI-69` لوحة قياس HUD وشروح مسقطة من 3D](#ui-69--لوحة-قياس-hud-وشروح-مسقطة-من-3d--instrument-panel-hud--projected-callouts)
- [`UI-70` مربع تتبع وماسح ضوئي](#ui-70--مربع-تتبع-وماسح-ضوئي--ai-tracking-box--scanner-brackets)
- [`UI-71` مسرح أداة تصميم ومقابض تحديد](#ui-71--مسرح-أداة-تصميم-ومقابض-تحديد--design-tool-canvas-selection-handles--size-tags)
- [`UI-72` تسجيل صفحة بخطوات مبرمجة](#ui-72--تسجيل-صفحة-بخطوات-مبرمجة--scripted-page-recording-playwright)
- [`UI-73` التقاط موقع إلى فيديو](#ui-73--التقاط-موقع-إلى-فيديو--website-capture--video)
- [`UI-74` فيلم إطلاق kmotion brag](#ui-74--فيلم-إطلاق-kmotion-brag--kmotion-brag-launch-film)
- [`UI-75` وصفة فيديو ميزة حقيقية](#ui-75--وصفة-فيديو-ميزة-حقيقية--real-feature-video-recipe)
- [`UI-76` من فيجما إلى طبقات متحركة](#ui-76--من-فيجما-إلى-طبقات-متحركة--figma-frame--animatable-layers)
- [`UI-77` تسجيل المتصفح بمؤشر ولوحة لقطات](#ui-77--تسجيل-المتصفح-بمؤشر-ولوحة-لقطات--browser-recording-cli-with-cursor--contact-sheet)
- [`UI-78` فيديو تعليمي من ملف YAML](#ui-78--فيديو-تعليمي-من-ملف-yaml--yaml-defined-tutorial-video)
- [`UI-79` رموز تصميم الواجهة وسلالمها](#ui-79--رموز-تصميم-الواجهة-وسلالمها--ui-tokens--refactoring-ui-scales)
- [`UI-80` سطح زجاجي للواجهات](#ui-80--سطح-زجاجي-للواجهات--glass-surface-stack)
- [`UI-81` معمارية الثيمات: الشكل × الوضع × العلامة](#ui-81--معمارية-الثيمات-الشكل--الوضع--العلامة--look--theme--brand-token-architecture)
- [`UI-82` ستايل برومو المنتج](#ui-82--ستايل-برومو-المنتج--product-promo-style-neon-prompt--glass-orb)
- [`UI-83` واجهة ملصقات بظل صلب](#ui-83--واجهة-ملصقات-بظل-صلب--sticker-ui-with-hard-offset-shadow)
- [`UI-84` مكتبة مكوّنات HyperFrames للواجهات](#ui-84--مكتبة-مكوّنات-hyperframes-للواجهات--hyperframes-ui-component-registry)
- [`UI-85` مخططات مشاهد الواجهة](#ui-85--مخططات-مشاهد-الواجهة--ui-scene-blueprints)
- [`UI-86` أساليب KOSIF للواجهات](#ui-86--أساليب-kosif-للواجهات--kosif-ui-styles-to-scaffold)
- [`UI-87` مشغّل HTML مستقل بشريط تقديم](#ui-87--مشغّل-html-مستقل-بشريط-تقديم--standalone-html-player-with-seek--reduced-motion)
- [`UI-88` مراجعة على الإطار: سحب وتحجيم واختصارات](#ui-88--مراجعة-على-الإطار-سحب-وتحجيم-واختصارات--frame-review-drag-resize--arabic-safe-shortcuts)
- [`UI-89` قواعد صفحات الويب المسلَّمة](#ui-89--قواعد-صفحات-الويب-المسلَّمة--web-deliverable-rules-landing-perf-hover-gating)
- [`UI-X01` المؤشر بطلًا](#ui-x01--المؤشر-بطلًا--cursor-as-protagonist)
- [`UI-X02` تسليم المجسم وطبقات منفجرة](#ui-x02--تسليم-المجسم-وطبقات-منفجرة--mockup-hand-off-and-exploded-layers)
- [`UI-X03` تسجيل عرض واجهة بـPlaywright](#ui-x03--تسجيل-عرض-واجهة-بـplaywright--playwright-ui-demo-recording-webm)
- [`UI-X04` رموز الحركة وصقل الواجهة](#ui-x04--رموز-الحركة-وصقل-الواجهة--motion-tokens-and-interface-polish-react-uis)

## البطاقات / cards

### `UI-01` — العرض الصامت: الواجهة تحكي / Silent product demo — the UI tells the story

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الواجهة والمؤشر والكاميرا يحملون القصة، والكلمات تسمّي الخطوة أو النتيجة فقط. / Interface, cursor and camera carry the story; words only name a beat or an outcome.

**متى:** حين يطلب المستخدم فيديو عرض منتج بلا تعليق صوتي تحكي فيه الواجهة والمؤشر القصة / when the user wants a product demo with no voiceover where the UI and cursor tell the story

**كيف:** Storyboard five columns: time · screen state · pointer action · camera focus · text. Frame 1 must already be legible. The camera moves toward the current action, then settles before the next one; one subject per beat; clear old props before the next beat. Animate from time only (deterministic). Before the full export render stills at: frame 0, each action, every transition midpoint, last frame — and watch it once muted.

**المعاملات:** stills: first · per action · transition midpoints · last

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عرض منتج · ديمو صامت · product demo · silent demo · storyboard · feature video · فيديو منتج · شرح تطبيق · بدون تعليق · app demo · ui walkthrough

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/101-video-skills/217-silent-product-demo/SKILL.md`
- `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md`
- `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video`

#### 7. قدرات قريبة في العائلة

- `UI-02` ثلاثية النية والفعل والاستجابة / Intent → action → response with real latency (documented)
- `UI-03` محتوى واجهة حقيقي ومحلي / Real, locale-correct UI content (documented)

### `UI-02` — ثلاثية النية والفعل والاستجابة / Intent → action → response with real latency

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المؤشر يصل، يضغط، ثم تستجيب الواجهة بعد زمن استجابة واقعي. / The pointer arrives, presses, and the UI answers after a believable latency.

**متى:** عند تحريك نقرة على الواجهة وتحديد متى تستجيب الشاشة بعد الضغط حتى لا تبدو كعرض شرائح أو خلل / when timing how soon the UI reacts after a click so it reads neither as a slideshow nor a bug

**كيف:** Response starts 60–120 ms after the press frame. 0 ms reads as a slideshow, more than 200 ms reads as a bug. Never animate success before the action completes. Direct-manipulation feedback lands within 100 ms; UI animations stay under 500 ms and look interruptible.

**المعاملات:** latency 60–120 ms; >200 ms = bug; feedback <100 ms; anim <500 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زمن الاستجابة · latency · feedback · click response · توقيت النقرة · رد فعل الواجهة · تأخير · response timing · ui delay

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/product-ui.md:29`
- `kosif-tool/playbooks/product-ui.md:58`
- `kosif-atlas/skills/3438-ux-design/14121-microinteractions`

#### 7. قدرات قريبة في العائلة

- `UI-01` العرض الصامت: الواجهة تحكي / Silent product demo — the UI tells the story (documented)
- `UI-03` محتوى واجهة حقيقي ومحلي / Real, locale-correct UI content (documented)
- `UI-04` إعادة بناء الشاشة كطبقات / Layered screen rebuild (ready)

### `UI-03` — محتوى واجهة حقيقي ومحلي / Real, locale-correct UI content

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أسماء ومبالغ وتواريخ معقولة بلغة المشاهد؛ لا lorem ولا مؤشرات متناقضة ولا ميزة مخترعة. / Plausible locale-correct names, amounts and dates; no lorem, no contradictory KPIs, no invented features.

**متى:** حين تحتاج الواجهة المعروضة أسماء ومبالغ وتواريخ واقعية بلغة المشاهد بدل نص تجريبي / when a shown UI needs realistic, locale-correct names, amounts and dates instead of placeholder text

**كيف:** Write the strings first (Arabic UI labels ≥ 28 px at 1080 wide, line-height 1.6–1.8, letter-spacing 0). Use disposable test data when capturing a real app. Prices, countdowns and claims must be confirmed by the user — a fake price or countdown is forbidden. Saudi/Gulf money: SAR with tabular digits from one numeral system.

**المعاملات:** Arabic UI text ≥ 28 px; lh 1.6–1.8

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محتوى حقيقي · lorem · real data · localisation · ui copy · بيانات واقعية · نص تجريبي · تعريب الواجهة · placeholder text · test data

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/product-ui.md:19`
- `kosif-tool/playbooks/product-ui.md:209-214`
- `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-01` العرض الصامت: الواجهة تحكي / Silent product demo — the UI tells the story (documented)
- `UI-02` ثلاثية النية والفعل والاستجابة / Intent → action → response with real latency (documented)
- `UI-04` إعادة بناء الشاشة كطبقات / Layered screen rebuild (ready)
- `UI-05` حقيبة أصول من أجزاء حقيقية / Animation kit from real parts (ready)

### `UI-04` — إعادة بناء الشاشة كطبقات / Layered screen rebuild

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الشاشة تُبنى طبقات: خلفية ← إطار ← محتوى ← أدوات ← طبقات عائمة ← مؤشر ← شروح، ولكل طبقة جدولها الزمني. / Build the screen as background → chrome → content → controls → overlays → pointer → callouts, each with its own timeline.

**متى:** عند تحويل لقطة شاشة إلى واجهة حية متحركة تُبنى طبقة طبقة لكل منها توقيتها / when turning a screenshot into a live, layered UI where each layer gets its own timeline

**كيف:** Rebuild the UI as live DOM/SVG/Canvas with real strings at 2× density; keep a flattened screenshot only as the reference to match. If zoom makes a screenshot unreadable, re-capture at higher resolution or rebuild it as DOM. Depth comes from elevation tiers and overlap, plus 2–4% chrome/content parallax — not from tilt or glass.

**المعاملات:** 2× density; parallax 2–4%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طبقات · إعادة بناء الواجهة · ui rebuild · layers · dom · لقطة شاشة · تحريك الواجهة · عمق · screenshot to ui · parallax

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/product-ui.md:17`
- `kosif-tool/playbooks/product-ui.md:23`
- `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-02` ثلاثية النية والفعل والاستجابة / Intent → action → response with real latency (documented)
- `UI-03` محتوى واجهة حقيقي ومحلي / Real, locale-correct UI content (documented)
- `UI-05` حقيبة أصول من أجزاء حقيقية / Animation kit from real parts (ready)
- `UI-06` عكس الواجهة للعربية / RTL product-UI mirroring (documented)

### `UI-05` — حقيبة أصول من أجزاء حقيقية / Animation kit from real parts

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قبل التحريك: أعد بناء الواجهة كـ DOM، صوّرها بدقة 3–5×، واقطع كل زر وأيقونة وشريحة كقطعة شفافة ≥ 1600 بكسل. / Before animating, rebuild the UI as DOM, shoot it at 3–5× and cut every button, chip and icon into a transparent part ≥ 1600 px.

**متى:** حين تحتاج قطع واجهة شفافة عالية الدقة (أزرار وأيقونات وشرائح) قبل التحريك / when you need high-res transparent cut-outs of buttons, chips and icons before animating

**كيف:** Playwright element screenshots with omitBackground:true for transparent parts (Playwright + Chromium are installed here). Split the official SVG mark into layers and re-stack them; a PIL difference check must stay ≤ 1/255. Watch aspect: rendering 1200×800 parts into a 224×160 slot stretches 7%.

**المعاملات:** parts ≥ 1600 px; capture 3–5×; layer diff ≤ 1/255

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أصول · قطع شفافة · asset kit · omitBackground · playwright screenshot · قص الأيقونات · خلفية شفافة · عناصر الواجهة · ui parts · transparent cutouts

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-03` محتوى واجهة حقيقي ومحلي / Real, locale-correct UI content (documented)
- `UI-04` إعادة بناء الشاشة كطبقات / Layered screen rebuild (ready)
- `UI-06` عكس الواجهة للعربية / RTL product-UI mirroring (documented)
- `UI-07` لوحة البيانات داخل الإطار / Dashboard composition for a frame (documented)

### `UI-06` — عكس الواجهة للعربية / RTL product-UI mirroring

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اعكس التفاعل لا العتاد: الشريط الجانبي يمين، الزر الأساسي يسار، الأسهم مقلوبة، والتقدم يمتلئ من اليمين. / Mirror interaction, not hardware: sidebar right, primary action left, chevrons flipped, progress fills right-to-left.

**متى:** عند تحويل واجهة منتج أو تطبيق هاتف إلى العربية وعكس اتجاه التفاعل من اليمين لليسار / when localising a product or phone UI to Arabic and mirroring interaction right-to-left

**كيف:** Use dir=rtl on the UI container only (not <html> in renders) with logical CSS (margin-inline-start, inset-inline-end). The cursor starts bottom-right; forward navigation pushes the new screen in from the left; toasts enter top-left (top-end). Phones: back chevron on the right, toggles 'on' at the left, tab order RTL; the island, camera and hardware buttons are NOT mirrored; hero copy sits right of the device with positive yaw. Phone numbers and times get unicode-bidi:plaintext. Cut typed text at graphemes with Intl.Segmenter. Narrow tab rows: 44 px fade on the inline-start edge plus proximity scroll-snap.

**المعاملات:** Arabic compact rows +10% line height; tab fade 44 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عربي · اتجاه · rtl · mirroring · arabic ui · logical css · تعريب · يمين لليسار · عكس الواجهة · right to left · localization

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/product-ui.md:209-214`
- `kosif-tool/playbooks/phone.md:187-192`
- `kosif-audit-pro/patch/kosif-v17.css`

#### 7. قدرات قريبة في العائلة

- `UI-04` إعادة بناء الشاشة كطبقات / Layered screen rebuild (ready)
- `UI-05` حقيبة أصول من أجزاء حقيقية / Animation kit from real parts (ready)
- `UI-07` لوحة البيانات داخل الإطار / Dashboard composition for a frame (documented)
- `UI-08` تشريح التفاعل الدقيق كوحدة مشهد / Microinteraction anatomy as a beat (documented)

### `UI-07` — لوحة البيانات داخل الإطار / Dashboard composition for a frame

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سؤال واحد يسيطر واللوحة كلها تتراجع خلفه. / One question dominates; everything else recedes.

**متى:** حين يظهر في الفيديو لوحة بيانات ويجب أن يتصدر مؤشر رئيسي واحد وتتراجع البقية / when a video frame shows a dashboard and one headline metric must lead while the rest recede

**كيف:** One focal view + subordinate context; 5–7 KPIs max (4–6 for an executive summary); legends next to the evidence; no wall of equal tiles. Animate the headline tile first, then the rest. Operations scenes show live/stale states explicitly (status dot with halo, see UI-45).

**المعاملات:** 5–7 KPIs; headline first

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لوحة بيانات · dashboard · kpi · focal view · داشبورد · مؤشرات الأداء · ملخص تنفيذي · metrics · executive summary

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/3455-business-analytics/14162-kpi-dashboard-design/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-05` حقيبة أصول من أجزاء حقيقية / Animation kit from real parts (ready)
- `UI-06` عكس الواجهة للعربية / RTL product-UI mirroring (documented)
- `UI-08` تشريح التفاعل الدقيق كوحدة مشهد / Microinteraction anatomy as a beat (documented)
- `UI-09` مقطع حلقة لمكوّن واحد / Seamless UI component loop (3–6 s) (documented)

### `UI-08` — تشريح التفاعل الدقيق كوحدة مشهد / Microinteraction anatomy as a beat

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل لحظة واجهة = مُطلِق ← قاعدة ← تغذية راجعة ← حالة مستقرة. / Every UI moment is trigger → rule → feedback → settled state.

**متى:** عند تخطيط كل لحظة تفاعل في الواجهة من المُطلِق إلى الحالة المستقرة وضبط مدتها / when storyboarding each UI moment from trigger to settled state and choosing its duration

**كيف:** Storyboard each UI beat as trigger → visible change → settled state, and score it with an 8-row checklist (score = passed/8 × 10). Physical metaphors stay shortened: drawers slide from their side, modals rise like cards, momentum scroll settles on a spring. Standard ranges: 150 ms micro, 250–300 ms transitions, 400–500 ms larger moves; whole-UI motion ≤ 700 ms, ≤ 3 flashes per second.

**المعاملات:** 150 / 250–300 / 400–500 ms; ≤ 700 ms; ≤ 3 flashes/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تفاعل دقيق · microinteraction · beat · timing ranges · حركة الواجهة · توقيت الحركة · تغذية راجعة · ui animation · motion timing

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/3438-ux-design/14121-microinteractions`
- `kosif-atlas/skills/1503-universal-design-principles/3766-mimicry-behavioral`
- `100-superskills/skills/ui-motion-microinteractions/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-06` عكس الواجهة للعربية / RTL product-UI mirroring (documented)
- `UI-07` لوحة البيانات داخل الإطار / Dashboard composition for a frame (documented)
- `UI-09` مقطع حلقة لمكوّن واحد / Seamless UI component loop (3–6 s) (documented)
- `UI-10` عناوين أفعال بسيطة في الشروحات / Plain action labels in tutorials (documented)

### `UI-09` — مقطع حلقة لمكوّن واحد / Seamless UI component loop (3–6 s)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مكوّن حقيقي واحد يؤدي فعلًا واحدًا ويعود لبدايته بلا قفزة. / One real component performs one action and loops without a jump.

**متى:** حين يطلب المستخدم مقطعًا قصيرًا يتكرر بلا قفزة لمكوّن واجهة واحد يؤدي فعلًا واحدًا / when the user wants a short seamless loop of one UI component doing one action

**كيف:** Use the component's real size, colours, shadows and timing; fit whole periodic cycles into the duration; one-shot actions return via a plausible reverse. Locked camera or one subtle push. Compare the first and last frames and watch several repeats for jumps or double triggers.

**المعاملات:** 3–6 s; one action; first frame == last frame

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حلقة · loop · component clip · seamless · تكرار · لوب · مكون واجهة · looping clip · short clip

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/101-video-skills/219-ui-component-clip/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-07` لوحة البيانات داخل الإطار / Dashboard composition for a frame (documented)
- `UI-08` تشريح التفاعل الدقيق كوحدة مشهد / Microinteraction anatomy as a beat (documented)
- `UI-10` عناوين أفعال بسيطة في الشروحات / Plain action labels in tutorials (documented)
- `UI-11` مؤشر بفيزياء في motion-kit / motion-kit physics cursor + press + typeOn (proven)

### `UI-10` — عناوين أفعال بسيطة في الشروحات / Plain action labels in tutorials

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** التسمية تقول الفعل («اختر ملفًا»، «اضغط تسجيل») لا رقم الخطوة. / Captions name the action ('CHOOSE A FILE', 'PRESS RECORD'), not decorative step numbers.

**متى:** عند كتابة عناوين خطوات فيديو تعليمي أو شرح تطبيق بحيث تسمّي الفعل لا رقم الخطوة / when writing captions for a tutorial or app walkthrough that name the action, not a step number

**كيف:** Open with the payoff, then explain steps over the action. One short line per decision; the pointer reaches the exact target and holds through the press; keep menus and overlays where the app places them.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شرح · تعليمي · tutorial · action labels · onboarding · فيديو تعليمي · شرح خطوات · عناوين الخطوات · captions · how-to

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-08` تشريح التفاعل الدقيق كوحدة مشهد / Microinteraction anatomy as a beat (documented)
- `UI-09` مقطع حلقة لمكوّن واحد / Seamless UI component loop (3–6 s) (documented)
- `UI-11` مؤشر بفيزياء في motion-kit / motion-kit physics cursor + press + typeOn (proven)
- `UI-12` واجهة منتج على Canvas بدالة draw(t) / Canvas product UI draw(t) recipe (proven)

### `UI-11` — مؤشر بفيزياء في motion-kit / motion-kit physics cursor + press + typeOn

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سهم مرسوم يمر بمحطات زمنية على منحنى Hermite ويتوقف بسرعة صفر، ويضغط مع انضغاط الهدف. / A drawn arrow travels timed stops on a Hermite curve (zero velocity at holds) and presses with the target dipping.

**متى:** حين تحتاج مؤشرًا مرسومًا يتنقل بين محطات زمنية ويضغط الأهداف ويكتب نصًا داخل motion-kit / when you need a drawn cursor that travels timed stops, presses targets and types text with motion-kit

**كيف:** c = M.cursor(stage,{size:30}); M.moveCursor(tl, c, [{t,x,y},…], {hold:[t…]}) samples the path at 60 fps into keyframes; M.press(tl, c, at, {target, down:.97}); M.typeOn(tl, el, text, at, {cps:46, hold:.6}). Rendered here: kit_v3_demo through render_html.cjs (6 s, 180 frames, VERIFY OK) after adding one bridge line, because the kit exposes window.__kosifSeek, not window.__kosif. (code snippet in references/powers/ui-product-device.md)

**المعاملات:** size 28–34 px (h ×1.22), drop-shadow 0 6px 8px rgba(0,0,0,.28); travel 36–48 f, arc 15–25% of the path; press 0.88 over 4 f, recover 8 f; target 0.97

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مؤشر · ماوس · cursor · press · hermite · motion-kit · typeOn · سهم الماوس · نقرة · كتابة نص · pointer animation · click

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-studio/motion/kit/motion-kit.js:403`
- `kosif-studio/motion/kit/motion-kit.js:426`
- `kosif-studio/motion/projects/kit_v3_demo/index.html:39`
- `kosif-studio/tests/test_studio.py:637`

#### 7. قدرات قريبة في العائلة

- `UI-09` مقطع حلقة لمكوّن واحد / Seamless UI component loop (3–6 s) (documented)
- `UI-10` عناوين أفعال بسيطة في الشروحات / Plain action labels in tutorials (documented)
- `UI-12` واجهة منتج على Canvas بدالة draw(t) / Canvas product UI draw(t) recipe (proven)
- `UI-13` تصميم حركة المؤشر / Cursor choreography rules (documented)

### `UI-12` — واجهة منتج على Canvas بدالة draw(t) / Canvas product UI draw(t) recipe

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شاشة تصعد، بطاقات تتتابع كل 50 ms، مؤشر يقطع 560 ms بقوس، وزر ينضغط 80 ms ويتحرر 140 ms — كله دالة نقية للزمن. / Screen rises, cards stagger 50 ms apart, a cursor arcs in 560 ms, the button presses 80 ms and releases 140 ms — all a pure function of time.

**متى:** عند بناء مشهد واجهة منتج على Canvas بشاشة تصعد وبطاقات متتابعة ومؤشر وزر ينضغط، كدالة للزمن / when building a canvas product-UI scene (rising screen, staggered cards, cursor, button press) as a function of time

**كيف:** Copy the playbook block into starters/html-canvas and render: node tools/render_html.cjs --in index.html --out film.mp4 --width 1080 --height 1920 --fps 30 --mode seek. Rendered here: 120 frames, VERIFY OK. Lesson from the frames: the 23 px arrow is tiny at 1080 wide — scale the cursor ×1.5–2 for phone-sized output.

**المعاملات:** bg #0b0d12, panel #161a23, cards #1f2430, button #19c37d; push 1.00→1.05 over 4 s; screen rise 48 px in 0.52 s expoOut

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كانفس · canvas · seek · draw(t) · product ui · deterministic · مشهد واجهة · فيديو عمودي · بطاقات متتابعة · vertical video · html canvas

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/product-ui.md:163-203`
- `kosif-tool/tools/render_html.cjs`
- `kosif-tool/starters/html-canvas/index.html`

#### 7. قدرات قريبة في العائلة

- `UI-10` عناوين أفعال بسيطة في الشروحات / Plain action labels in tutorials (documented)
- `UI-11` مؤشر بفيزياء في motion-kit / motion-kit physics cursor + press + typeOn (proven)
- `UI-13` تصميم حركة المؤشر / Cursor choreography rules (documented)
- `UI-14` حلقة الضغط والتموج / Press ring & click ripple (ready)

### `UI-13` — تصميم حركة المؤشر / Cursor choreography rules

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يظهر عند القرار، يسير بسرعة شبه ثابتة على منحنى ناعم، يستقر على الهدف 200–400 ms ثم يضغط. / Appears only for decisions, glides at near-constant speed on a smooth curve, dwells 200–400 ms on target, then presses.

**متى:** حين تخطط مسار المؤشر في عرض منتج: متى يظهر وكيف ينزلق وكم يتوقف على الهدف قبل الضغط / when planning a demo cursor's path: when it appears, how it glides, and how long it dwells before clicking

**كيف:** Plan waypoints per beat; interpolate with Catmull-Rom + arc-length so speed is constant; the tip (not the arrow's centre) lands on the hit target; hold through the pressed state; the UI response is visible before the cursor moves on. First appearance glides in from a short offset (−140, +90 px). Check tip-on-target in stills. Arrow for desktop scenes, translucent tap circle on phones — never an arrow on a phone.

**المعاملات:** glide ~450 ms per hop (380–700 ms cubic-bezier(.2,.8,.2,1)); dwell 200–400 ms; arrow 22–26 px with 1.5 px outline; tap circle 40–48 px at 25–35% opacity

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مسار المؤشر · cursor path · catmull-rom · arc length · dwell · حركة الماوس · توقف المؤشر · سهم · mouse movement · click target

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/101-video-skills/217-silent-product-demo`
- `kosif-tool/playbooks/product-ui.md:20`
- `kosif-tool/playbooks/product-ui.md:152`
- `kosif-tool/styles/saas-demo/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-11` مؤشر بفيزياء في motion-kit / motion-kit physics cursor + press + typeOn (proven)
- `UI-12` واجهة منتج على Canvas بدالة draw(t) / Canvas product UI draw(t) recipe (proven)
- `UI-14` حلقة الضغط والتموج / Press ring & click ripple (ready)
- `UI-15` مؤشر ماك معبّر يتجه مع حركته / Expressive directional macOS cursor (seen)

### `UI-14` — حلقة الضغط والتموج / Press ring & click ripple

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عند النقرة تنكمش الحلقة من المؤشر وتتلاشى، أو تنطلق موجتان صغيرتان. / On click a ring scales out from the tip and fades, or two small ripples release.

**متى:** عند إظهار أثر النقرة بحلقة تتسع أو تموج تحت المؤشر أو اللمس في فيديو واجهة / when showing a click with an expanding ring or ripple under the cursor or tap in a UI video

**كيف:** Inject a fixed-position div so the ring is captured in frames; element.animate keyframes scale 0.45→1.25, opacity 1→0, 420 ms ease-out. The ripple element exists in the DOM from t=0 at opacity 0 (no creation mid-render). Product-UI style: ripple 0→48 px in 320–400 ms; phone tap ripple 0→64 px, opacity 0.6→0 over 300 ms.

**المعاملات:** ring 0.45→1.25 / 420 ms; ripple 48 px desktop, 64 px phone

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقرة · تموج · ripple · click ring · press feedback · أثر النقرة · دائرة الضغط · ضغطة · click effect · tap ripple

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/1511-homie/3903-video/scripts/record-page.mjs`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/cursor-click-ripple.md`
- `kosif-tool/styles/ui-micro/SKILL.md`
- `kosif-tool/playbooks/phone.md:36`

#### 7. قدرات قريبة في العائلة

- `UI-12` واجهة منتج على Canvas بدالة draw(t) / Canvas product UI draw(t) recipe (proven)
- `UI-13` تصميم حركة المؤشر / Cursor choreography rules (documented)
- `UI-15` مؤشر ماك معبّر يتجه مع حركته / Expressive directional macOS cursor (seen)
- `UI-16` مؤشر بهالة لونية يلاحق هدفًا متحركًا / Cursor with accent halo homing on a live target (seen)

### `UI-15` — مؤشر ماك معبّر يتجه مع حركته / Expressive directional macOS cursor

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سهم أسود بحد أبيض يدور نحو اتجاه السرعة، يكبر عند المرور وينكمش عند الضغط، والكاميرا تقترب من النقرة. / Black arrow with white outline that rotates toward its velocity, grows on hover, shrinks on press while the camera zooms toward the click.

**متى:** حين تريد مؤشر ماك يدور مع اتجاه حركته ويكبر عند المرور بينما تقترب الكاميرا من النقرة / when you want a macOS arrow that turns with its motion and grows on hover while the camera zooms to the click

**كيف:** Rotation lerps toward atan2(vy, vx); decelerating glide; hover scale 1.55; press −15% for 3 frames; 32×39 px arrow with soft shadow. The 'oversized cursor' variant draws a 3.5× macOS arrow that lands, clicks and settles below the control.

**المعاملات:** hover ×1.55; press −15% / 3 f; arrow 32×39 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مؤشر ماك · macos cursor · directional · oversized cursor · سهم ماك · ماوس كبير · زوم على النقرة · mac pointer · click zoom

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `os:macos` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-notdwd-7de38a`
- `style:pm-notdwd-c2037d`
- `kosif-one/vendor/hyperframes/registry/components/oversized-cursor/oversized-cursor.html`

#### 7. قدرات قريبة في العائلة

- `UI-13` تصميم حركة المؤشر / Cursor choreography rules (documented)
- `UI-14` حلقة الضغط والتموج / Press ring & click ripple (ready)
- `UI-16` مؤشر بهالة لونية يلاحق هدفًا متحركًا / Cursor with accent halo homing on a live target (seen)
- `UI-17` المؤشر المغناطيسي / Magnetic cursor & magnetic buttons (install)

### `UI-16` — مؤشر بهالة لونية يلاحق هدفًا متحركًا / Cursor with accent halo homing on a live target

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المؤشر يعيد حساب موضع الهدف كل إطار والكاميرا تنجرف، مع دائرة شفافة خلفه تنبض عند النقر. / The arrow re-reads the live element position every frame while the camera drifts; a translucent accent halo pulses on click.

**متى:** عند متابعة المؤشر لعنصر يتحرك مع انجراف الكاميرا، وإبراز النقرة بهالة لونية نابضة / when the cursor must chase a moving element while the camera drifts, with a pulsing accent halo on click

**كيف:** Every frame read the target's transformed rect and steer toward it (no stale coordinates). Halo #f0442c at 40% alpha, 36 px; on click it shrinks and pulses 150 ms while the target shows its pressed state.

**المعاملات:** halo 36 px 40% alpha; pulse 150 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالة · cursor halo · homing · camera drift · تتبع الهدف · نبضة النقرة · هدف متحرك · moving target · click pulse

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-antonio-kodheli-490109`

#### 7. قدرات قريبة في العائلة

- `UI-14` حلقة الضغط والتموج / Press ring & click ripple (ready)
- `UI-15` مؤشر ماك معبّر يتجه مع حركته / Expressive directional macOS cursor (seen)
- `UI-17` المؤشر المغناطيسي / Magnetic cursor & magnetic buttons (install)
- `UI-18` سحب وإفلات / Cursor drag & drop (install)

### `UI-17` — المؤشر المغناطيسي / Magnetic cursor & magnetic buttons

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** نقطة ناعمة تنجذب إلى الأزرار وتتحول إلى لوحة التمرير، والأيقونات تميل نحوها. / A soft dot is pulled into buttons, morphing into their hover plate while icons lean toward it.

**متى:** حين يطلب المستخدم أزرارًا تنجذب نحو المؤشر ونقطة ناعمة تتحول إلى خلفية الزر عند المرور / when the user wants buttons pulled toward the cursor and a soft dot morphing into the hover plate

**كيف:** HyperFrames component magnetic-cursor (vars visits '0,3', press 2, accent #3b82f6, tone light\|dark). Hand-built rule: element offset = (cursor − centre) × factor, tween 0.3 s power2.out; leave → elastic.out(1,0.5) 0.5 s. Drive it from the scripted cursor path, never from a real mouse.

**المعاملات:** buttons factor 0.3, cards 0.1; return 0.5 s elastic.out(1,0.5)

**التثبيت:** npx hyperframes add magnetic-cursor

**الوسوم:** مغناطيسي · magnetic · hover · cursor · انجذاب · أزرار تفاعلية · مرور الماوس · hover effect · button attraction

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `lean` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/magnetic-cursor/magnetic-cursor.html`
- `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md`

#### 7. قدرات قريبة في العائلة

- `UI-15` مؤشر ماك معبّر يتجه مع حركته / Expressive directional macOS cursor (seen)
- `UI-16` مؤشر بهالة لونية يلاحق هدفًا متحركًا / Cursor with accent halo homing on a live target (seen)
- `UI-18` سحب وإفلات / Cursor drag & drop (install)
- `UI-19` تحديد نص ومستطيل وقائمة يمين / Text select, marquee select & context menu (install)

### `UI-18` — سحب وإفلات / Cursor drag & drop

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** المؤشر يمسك بطاقة، يرفعها ويميلها، يحملها لعمود فارغ، يفلتها فتستقر وتغلق القائمة الفجوة. / The cursor grabs a card, lifts and tilts it, carries it to an empty column and drops it while the list closes the gap.

**متى:** عند تصوير سحب بطاقة وإفلاتها في عمود آخر، أو سحب مقبض تعبئة أو تغيير الحجم من الزاوية / when showing a card dragged into another column, or a fill-handle or corner-resize drag

**كيف:** Grab = press dip + lift; the ghost travels on tweens matched to the cursor (same position, duration, ease; immediateRender:false); drop = snap with selection chrome. Variants: fill-handle and corner-resize. HyperFrames component cursor-drag-drop (card_label, accent #0a84ff, tone light\|dark).

**المعاملات:** matched tweens; drop settle spring

**التثبيت:** npx hyperframes add cursor-drag-drop

**الوسوم:** سحب · إفلات · drag and drop · kanban · سحب البطاقات · لوحة مهام · نقل عنصر · drag · resize

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/cursor-drag.md`
- `kosif-one/vendor/hyperframes/registry/components/cursor-drag-drop/cursor-drag-drop.html`

#### 7. قدرات قريبة في العائلة

- `UI-16` مؤشر بهالة لونية يلاحق هدفًا متحركًا / Cursor with accent halo homing on a live target (seen)
- `UI-17` المؤشر المغناطيسي / Magnetic cursor & magnetic buttons (install)
- `UI-19` تحديد نص ومستطيل وقائمة يمين / Text select, marquee select & context menu (install)
- `UI-20` مؤشرات متعاونين بأسمائها / Named multiplayer cursors (install)

### `UI-19` — تحديد نص ومستطيل وقائمة يمين / Text select, marquee select & context menu

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** السهم يصير I-beam ويحدد نصًا ثم يضغط Bold؛ أو يسحب مستطيل تحديد على شبكة صور؛ أو يفتح قائمة نقر أيمن. / The arrow becomes an I-beam and selects text then clicks Bold; or drags a marquee over a photo grid; or blooms a right-click menu.

**متى:** حين يحتاج المشهد تحديد نص وتنسيقه، أو سحب مستطيل تحديد على صور، أو فتح قائمة النقر الأيمن / when a scene needs text selection and formatting, a marquee drag over photos, or a right-click menu

**كيف:** HyperFrames components: cursor-text-select (title, text, phrase, accent), cursor-marquee-select (start/end x,y in %, each touched tile rings and checks while a pill counts), cursor-context-menu (items list, pick index, the menu blooms from the cursor tip). For Arabic text select by whole words, never split letters.

**المعاملات:** positions in % of frame

**التثبيت:** npx hyperframes add cursor-text-select

**الوسوم:** تحديد نص · text select · marquee · context menu · تظليل النص · قائمة النقر الأيمن · تحديد متعدد · right click · highlight text

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/cursor-text-select/cursor-text-select.html`
- `kosif-one/vendor/hyperframes/registry/components/cursor-marquee-select/cursor-marquee-select.html`
- `kosif-one/vendor/hyperframes/registry/components/cursor-context-menu/cursor-context-menu.html`

#### 7. قدرات قريبة في العائلة

- `UI-17` المؤشر المغناطيسي / Magnetic cursor & magnetic buttons (install)
- `UI-18` سحب وإفلات / Cursor drag & drop (install)
- `UI-20` مؤشرات متعاونين بأسمائها / Named multiplayer cursors (install)
- `UI-21` مؤشر وكيل ذكي / AI agent cursor (install)

### `UI-20` — مؤشرات متعاونين بأسمائها / Named multiplayer cursors

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** 2–4 مؤشرات ملونة بأسماء تعمل على لوحة واحدة بنبضات متناوبة. / 2–4 coloured, named cursors work one canvas on alternating beats.

**متى:** عند إظهار عدة مستخدمين يعملون معًا على لوحة واحدة بمؤشرات ملونة تحمل أسماءهم / when showing several people working one canvas together with coloured, named cursors

**كيف:** Partition the canvas into zones so paths never cross; actions on alternating beats (~1.2 / 2.6 / 4.0 s); legs power2.inOut; press scale 0.88 for 0.07 s yoyo; one payoff at a time. Name tags are pills (radius 999) in each user's colour. Components: multiplayer-cursors (cursorCount 2–6, labels).

**المعاملات:** beats 1.2/2.6/4.0 s; press 0.88 / 0.07 s

**التثبيت:** npx hyperframes add multiplayer-cursors

**الوسوم:** تعاون · multiplayer · named cursor · figma style · عمل جماعي · مؤشرات متعددة · مستخدمين · collaboration · shared canvas

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/multi-cursor-choreography.md`
- `kosif-one/vendor/hyperframes/registry/components/multiplayer-cursors/multiplayer-cursors.html`
- `style:pm-kikelopezdesign-7cc9e8`
- `style:pm-sachaarbonel-8f14f4`

#### 7. قدرات قريبة في العائلة

- `UI-18` سحب وإفلات / Cursor drag & drop (install)
- `UI-19` تحديد نص ومستطيل وقائمة يمين / Text select, marquee select & context menu (install)
- `UI-21` مؤشر وكيل ذكي / AI agent cursor (install)
- `UI-22` مؤشر اللمس على الهاتف / Touch indicator: tap & swipe (install)

### `UI-21` — مؤشر وكيل ذكي / AI agent cursor

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** مؤشر يحمل اسم وكيل يمر على قائمة خطوات، يكتب اسم كل خطوة، يحلّق حول كل هدف وينتهي بعلامة صح. / A named agent pointer walks a list of steps, types each step label, rings each click target and ends on a check.

**متى:** حين يطلب المستخدم إظهار وكيل ذكاء اصطناعي يتنقل بين خطوات وينقر الأهداف وينتهي بعلامة صح / when the user wants an AI agent pointer that walks steps, clicks targets and ends on a check

**كيف:** Component agent-cursor: agent_name, steps 'Reading the page,Opening Settings,…', targets 'x,y;x,y' in %, accent #0a84ff; extra duration becomes hold, never time-stretch. Render with npx hyperframes render — tested here: rendering its demo.html with render_html --mode virtual gives a frozen frame, because the paused window.__timelines and data-composition-src need the HyperFrames runtime.

**المعاملات:** targets as % pairs

**التثبيت:** npx hyperframes add agent-cursor

**الوسوم:** وكيل · agent · ai cursor · automation · ذكاء اصطناعي · وكيل ذكي · خطوات تلقائية · ai agent · task steps

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/agent-cursor/agent-cursor.html`
- `kosif-one/vendor/hyperframes/registry/components/agent-cursor/demo.html`

#### 7. قدرات قريبة في العائلة

- `UI-19` تحديد نص ومستطيل وقائمة يمين / Text select, marquee select & context menu (install)
- `UI-20` مؤشرات متعاونين بأسمائها / Named multiplayer cursors (install)
- `UI-22` مؤشر اللمس على الهاتف / Touch indicator: tap & swipe (install)
- `UI-23` ضغط اختصار لوحة المفاتيح / Keycap shortcut trigger (seen)

### `UI-22` — مؤشر اللمس على الهاتف / Touch indicator: tap & swipe

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** دائرة تلامس شفافة تلمس الزجاج على إطار الاستجابة، نقرًا أو سحبًا. / A translucent contact circle touches the glass on the response frame, as tap or swipe.

**متى:** عند عرض تطبيق هاتف والحاجة لدائرة لمس تُظهر النقر أو السحب على الشاشة / when demoing a phone app and you need a touch circle showing taps or swipes on screen

**كيف:** Cue 60 ms before the press; press 90 ms cubic-bezier(0.4,0,1,1) with device 0.96 and button 0.92; release spring {stiffness 240, damping 14}; ripple 0→64 px, 0.6→0 opacity over 300 ms. Components: touch-indicator (gesture tap\|swipe, polarity), gesture-tap (Follow → Following), swipe-rail (momentum carry, snap), pull-to-refresh (rubber band, pullDistance 120).

**المعاملات:** circle 40–48 px; press 90 ms; ripple 64 px / 300 ms

**التثبيت:** npx hyperframes add touch-indicator

**الوسوم:** لمس · هاتف · tap · swipe · touch indicator · لمسة · سحب للتحديث · تطبيق جوال · mobile gesture · pull to refresh

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:36`
- `kosif-tool/playbooks/phone.md:59-68`
- `kosif-one/vendor/hyperframes/registry/components/touch-indicator/touch-indicator.html`
- `kosif-one/vendor/hyperframes/registry/components/swipe-rail/swipe-rail.html`

#### 7. قدرات قريبة في العائلة

- `UI-20` مؤشرات متعاونين بأسمائها / Named multiplayer cursors (install)
- `UI-21` مؤشر وكيل ذكي / AI agent cursor (install)
- `UI-23` ضغط اختصار لوحة المفاتيح / Keycap shortcut trigger (seen)
- `UI-24` تحكم وهدف يتغيران معًا / Control ↔ target live sync (documented)

### `UI-23` — ضغط اختصار لوحة المفاتيح / Keycap shortcut trigger

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة أزرار مفاتيح تنضغط بالتتابع، والأخير يمتلئ بلون التمييز ويطلق الحركة التالية. / Three rounded keycaps press in sequence; the last fills with the accent and triggers the next animation.

**متى:** حين تريد إظهار اختصار لوحة مفاتيح بأزرار تنضغط بالتتابع ثم تطلق الحركة التالية / when you want to show a keyboard shortcut as keycaps pressing in sequence and triggering the next move

**كيف:** Each key: translateY 3 px + shadow shrink for 120 ms, 80 ms gap; last key fill accent then cut. Pair with a command palette (UI-30).

**المعاملات:** 120 ms per key; 80 ms gap

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** اختصار · keyboard · shortcut · keycaps · لوحة المفاتيح · أزرار الكيبورد · كيبورد · hotkey · key press

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-agonaliu-466a8f`

#### 7. قدرات قريبة في العائلة

- `UI-21` مؤشر وكيل ذكي / AI agent cursor (install)
- `UI-22` مؤشر اللمس على الهاتف / Touch indicator: tap & swipe (install)
- `UI-24` تحكم وهدف يتغيران معًا / Control ↔ target live sync (documented)
- `UI-25` كتابة بإيقاع بشري / Human-rhythm typing with caret (ready)

### `UI-24` — تحكم وهدف يتغيران معًا / Control ↔ target live sync

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** منزلق أو حقل يتغير والسطح المرتبط به يتغير في النبضة نفسها. / A scrubbed or typed control and its bound target change in the same beat.

**متى:** عند تحريك منزلق أو حقل إعدادات بحيث يتغير العنصر المرتبط به في النبضة نفسها / when a slider or settings field changes and its bound element must update in the same beat

**كيف:** Readout tween and target transform share one label, duration and ease (tl.addLabel('edit1'), shared SCRUB_DUR/SCRUB_EASE). While dragging, the control value is derived from cursor x; on release it springs to rest. Seen variants: settings sliders that move when the narration names them (knob 500 ms ease-in-out, inactive label 40% grey) and an accent swatch ring hopping every 350 ms while the whole UI recolours.

**المعاملات:** knob 500 ms; swatch hop 350 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** منزلق · slider · live sync · inspector · control · إعدادات · سلايدر · معاينة مباشرة · settings panel · real-time preview

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/control-target-sync.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/panel-edit-live-sync.md`
- `style:pm-rossaxbt-3085b7`
- `style:pm-iammxfschr-d68f90`

#### 7. قدرات قريبة في العائلة

- `UI-22` مؤشر اللمس على الهاتف / Touch indicator: tap & swipe (install)
- `UI-23` ضغط اختصار لوحة المفاتيح / Keycap shortcut trigger (seen)
- `UI-25` كتابة بإيقاع بشري / Human-rhythm typing with caret (ready)
- `UI-26` طلب يُكتب ثم يُرسل ثم يولّد / Prompt type → submit → generate (documented)

### `UI-25` — كتابة بإيقاع بشري / Human-rhythm typing with caret

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حروف تظهر بإيقاع شبه بشري مع مؤشر كتابة يومض، ومُحددة بالبذرة لا بالعشوائية. / Characters appear on a near-human rhythm with a blinking caret, seeded rather than random.

**متى:** حين يحتاج المشهد نصًا يُكتب حرفًا حرفًا بإيقاع بشري مع مؤشر كتابة وامض، بما فيه العربي / when a scene needs text typed character by character on a human rhythm with a blinking caret, Arabic included

**كيف:** reveal = text.slice(0, floor(t·cps)) with a 1-frame hold every 2–3 chars from a seeded pattern (no Math.random in renders). Caret blink 500–530 ms (2 Hz), always visible while typing. Speeds: prompts 35–50 ms/char, terminals 35–45, human forms 70 ms ±20, search ~12 cps. Arabic: cut at grapheme clusters with Intl.Segmenter. motion-kit typeOn (cps 46) is rendered and proven in UI-11. (code snippet in references/powers/ui-product-device.md)

**المعاملات:** 35–50 ms/char prompts; 70 ±20 ms forms; caret 500–530 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كتابة · آلة كاتبة · typewriter · typing · caret · seeded · كتابة حرف بحرف · مؤشر الكتابة · نص يكتب · type on · text reveal

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-studio/motion/kit/motion-kit.js:193`
- `kosif-tool/playbooks/product-ui.md:104-116`
- `style:pm-notdwd-c2037d`
- `style:product`

#### 7. قدرات قريبة في العائلة

- `UI-23` ضغط اختصار لوحة المفاتيح / Keycap shortcut trigger (seen)
- `UI-24` تحكم وهدف يتغيران معًا / Control ↔ target live sync (documented)
- `UI-26` طلب يُكتب ثم يُرسل ثم يولّد / Prompt type → submit → generate (documented)
- `UI-27` وكيل ينجز قائمة مهام / Agent progress theater & tool-call checklist (seen)

### `UI-26` — طلب يُكتب ثم يُرسل ثم يولّد / Prompt type → submit → generate

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طلب يُكتب في حقل حقيقي، المؤشر يضغط إرسال، ثم تجيب الآلة: حالة تحميل ← إجابة متدفقة أو ناتج. / A prompt types into a real input, the cursor presses send, and the machine answers: status theater → streaming answer or artifact.

**متى:** عند تصوير أداة ذكاء اصطناعي: كتابة طلب في الحقل ثم الضغط على إرسال ثم ظهور التحميل والنتيجة / when showing an AI tool: typing a prompt, pressing send, then loading and the generated result

**كيف:** Blueprint prompt-type-submit-generate (5.2–12 s). Type ~35–50 ms/char with caret, send = button scale 0.9 + accent ring pulse 300 ms, then a thin progress bar fills ~1 s while a tile grid resolves tile by tile, or the result fades/scales in full-frame. Seen: centred 600×48 px pill on a dark frame; gradient-rim glowing search pill (1.5 px conic pink→violet→blue border + blurred copy below, blur 24 px at 0.35).

**المعاملات:** blueprint 5.2–12 s; ring 300 ms; progress ~1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طلب · برومبت · prompt · generate · ai tool · send button · ذكاء اصطناعي · توليد · حقل الكتابة · prompt box · ai generation

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/prompt-type-submit-generate.md`
- `style:pm-listudio-820c7b`
- `style:pm-influencer-seo-ce8c33`
- `style:pm-lester-tyy-f897f7`

#### 7. قدرات قريبة في العائلة

- `UI-24` تحكم وهدف يتغيران معًا / Control ↔ target live sync (documented)
- `UI-25` كتابة بإيقاع بشري / Human-rhythm typing with caret (ready)
- `UI-27` وكيل ينجز قائمة مهام / Agent progress theater & tool-call checklist (seen)
- `UI-28` محادثة: فقاعات وكتابة جارية / Chat thread, bubbles & typing dots (install)

### `UI-27` — وكيل ينجز قائمة مهام / Agent progress theater & tool-call checklist

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسالة المستخدم ← خطة الوكيل ← صفوف أدوات تدور ثم تتحول لعلامة صح بالتتابع ← بطاقة جاهزة. / User bubble → agent plan → tool-call rows spin then turn into checks in sequence → 'Ready' card.

**متى:** حين تريد إظهار وكيل ينفذ خطة خطوة بخطوة بصفوف أدوات تدور ثم تتحول لعلامات صح / when you want an agent working through a plan, tool rows spinning then turning into checks

**كيف:** Rows (mono 11–13 px, 'namespace · function') appear 250–600 ms apart; each spinner becomes a green check #2bb673 with a 0.6→1 scale pop; footer counters tick; optional terminal pane types output alongside. Status words can swap first (Queued → Reading → Drafting → Done) with HyperFrames state-chip-rail. Blueprint agent-progress-theater (4.2–11.6 s).

**المعاملات:** ticks 250–600 ms apart; check pop 250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وكيل · قائمة مهام · agent · checklist · tool calls · ai · تقدم المهام · خطوات التنفيذ · ذكاء اصطناعي · task progress · progress theater

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/agent-progress-theater.md`
- `style:pm-ddryo-loos-300829`
- `style:pm-majorbaguette-fb11d7`
- `style:pm-bizibeast-10f264`
- `style:pm-listudio-820c7b`

#### 7. قدرات قريبة في العائلة

- `UI-25` كتابة بإيقاع بشري / Human-rhythm typing with caret (ready)
- `UI-26` طلب يُكتب ثم يُرسل ثم يولّد / Prompt type → submit → generate (documented)
- `UI-28` محادثة: فقاعات وكتابة جارية / Chat thread, bubbles & typing dots (install)
- `UI-29` طرفية ومحرر كود / Terminal & IDE scenes (24 theme blocks) (install)

### `UI-28` — محادثة: فقاعات وكتابة جارية / Chat thread, bubbles & typing dots

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** مشهد مراسلة كامل: شريط حالة، اسم جهة الاتصال، فقاعات بذيل، علامة استلام، رموز، بطاقة رابط ونقاط كتابة. / A full messaging scene: status bar, contact pill, tailed bubbles, receipt, emoji, link card and typing dots.

**متى:** عند بناء مشهد مراسلة أو دردشة بفقاعات رسائل ونقاط كتابة جارية وعلامة استلام / when building a messaging or chat scene with message bubbles, typing dots and a receipt mark

**كيف:** Components chat-thread (messages 'recv:…\|sent:…\|card:title~domain\|emoji:…', beat 1.7 s), chat-message (entry scale 0.75 in 0.12 s from the sender corner), typing-indicator (three dots, vanish when the message lands). Hand-built: bubbles slide y+12 and fade, alternate sides, stagger 500 ms; Q&A answer bubble 300 ms back.out. Arabic: received bubbles on the left, sent on the right in RTL apps — mirror the tail.

**المعاملات:** beat 1.7 s; bubble 0.12 s from 0.75

**التثبيت:** npx hyperframes add chat-thread

**الوسوم:** محادثة · دردشة · chat · bubbles · typing dots · messaging · رسائل · شات · فقاعات الرسائل · text messages · message thread

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/chat-thread/chat-thread.html`
- `kosif-one/vendor/hyperframes/registry/components/chat-message/chat-message.html`
- `kosif-one/vendor/hyperframes/registry/components/typing-indicator/typing-indicator.html`
- `style:pm-fractadev-149adc`

#### 7. قدرات قريبة في العائلة

- `UI-26` طلب يُكتب ثم يُرسل ثم يولّد / Prompt type → submit → generate (documented)
- `UI-27` وكيل ينجز قائمة مهام / Agent progress theater & tool-call checklist (seen)
- `UI-29` طرفية ومحرر كود / Terminal & IDE scenes (24 theme blocks) (install)
- `UI-30` لوحة أوامر وبحث يصفّي النتائج / Command palette & search filter (seen)

### `UI-29` — طرفية ومحرر كود / Terminal & IDE scenes (24 theme blocks)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** نافذة طرفية بأضواء المرور وموجه ~ $ وحروف تُكتب ومؤشر كتلة، أو محرر VS Code كامل بثيماته. / A terminal window with traffic lights, a '~ $' prompt, typed characters and a block cursor — or a full VS Code workbench in its themes.

**متى:** حين يتضمن الفيديو كتابة كود في محرر VS Code أو أوامر في طرفية ماك، أو عرض فرق بين سطرين / when a video shows code typed in VS Code, commands in a macOS terminal, or a line diff

**كيف:** 24 ready ~11–12 s blocks: VS Code (12 themes: dark-plus, light-plus, dark-modern, monokai, solarized-light…) with per-char typing and a pytest terminal, or macOS Terminal.app (12 profiles). Edit codeLines. Hand-built: 35–45 ms/char, block cursor in the accent colour, blink 500 ms. Diff rows: old line struck through grey (strike draw 250 ms), new line types in orange, rows 1.2 s apart.

**المعاملات:** 24 themes; 35–45 ms/char

**التثبيت:** npx hyperframes add code-snippet-dark-modern

**الوسوم:** طرفية · كود · terminal · ide · vs code · diff · محرر أكواد · سطر الأوامر · برمجة · code editor · command line

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `os:macos` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-dark-modern`
- `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md`
- `style:pm-viktoroddy-98c1d8`
- `style:plotter`

#### 7. قدرات قريبة في العائلة

- `UI-27` وكيل ينجز قائمة مهام / Agent progress theater & tool-call checklist (seen)
- `UI-28` محادثة: فقاعات وكتابة جارية / Chat thread, bubbles & typing dots (install)
- `UI-30` لوحة أوامر وبحث يصفّي النتائج / Command palette & search filter (seen)
- `UI-31` إجابة متدفقة وسجل حي / Streaming answer & live log (seen)

### `UI-30` — لوحة أوامر وبحث يصفّي النتائج / Command palette & search filter

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حقل بحث يُكتب فيه، صفوف النتائج تنزلق، الصف الأول مميز، وEnter يتحول لإشعار. / Characters type into a search field, result rows slide in, the first row highlights and Enter collapses into a toast.

**متى:** عند تصوير كتابة في حقل بحث تتصفى معه النتائج ويبرز الأول ثم يتحول الإدخال إلى إشعار / when showing typing into a search field that filters results, highlights the top row, then becomes a toast

**كيف:** ~70 ms per char (or one char per beat subdivision on music); rows fade/slide 12 px in 250 ms; non-matching rows fade to 30% and collapse in 400 ms; matches move up with a yellow keyword highlight and a '1 result' label.

**المعاملات:** 70 ms/char; filter 400 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بحث · لوحة أوامر · command palette · search · filter · تصفية النتائج · نتائج البحث · سيرش · search results · keyword highlight

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-twoclipping-5cba86`
- `style:pm-mehul4795-4a7007`
- `style:pm-brainextends-e19ac3`
- `style:pm-agonaliu-466a8f`

#### 7. قدرات قريبة في العائلة

- `UI-28` محادثة: فقاعات وكتابة جارية / Chat thread, bubbles & typing dots (install)
- `UI-29` طرفية ومحرر كود / Terminal & IDE scenes (24 theme blocks) (install)
- `UI-31` إجابة متدفقة وسجل حي / Streaming answer & live log (seen)
- `UI-32` كتابة في تطبيق الملاحظات / Notes-app typing story (install)

### `UI-31` — إجابة متدفقة وسجل حي / Streaming answer & live log

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الإجابة تظهر سطرًا سطرًا، أو سجل أحادي الخط تُضاف إليه سطور بوسوم ملونة. / The answer appears line by line, or a mono log appends rows with coloured verb tags.

**متى:** حين تظهر إجابة سطرًا بسطر بعد فقاعة السؤال، أو سجل حي تُضاف إليه سطور بوسوم ملونة / when an answer appears line by line after a question bubble, or a live log keeps appending tagged rows

**كيف:** Bullet lines every ~120 ms after the question bubble. Live log: dark card radius 16 px, green live dot, mono endpoint rows with ✓ and '200' appended every ~120 ms; verb tags OBSERVE/CLICK/SCROLL. Skeleton reply: 3 grey bars (30 px high, 40–70% wide) grow to imply loading.

**المعاملات:** lines ~120 ms; card radius 16 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تدفق · سجل · streaming · live log · skeleton reply · ظهور الإجابة · سجل العمليات · رد تدريجي · line by line · activity log

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-wani-shola-16ca7a`
- `style:pm-0xfemyn-e114d3`
- `style:pm-hqmank-7c61f1`
- `style:pm-kloss-xyz-15182a`

#### 7. قدرات قريبة في العائلة

- `UI-29` طرفية ومحرر كود / Terminal & IDE scenes (24 theme blocks) (install)
- `UI-30` لوحة أوامر وبحث يصفّي النتائج / Command palette & search filter (seen)
- `UI-32` كتابة في تطبيق الملاحظات / Notes-app typing story (install)
- `UI-33` جدول ردود الفعل الدقيقة / Micro-feedback timing table (documented)

### `UI-32` — كتابة في تطبيق الملاحظات / Notes-app typing story

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** عنوان عريض ثم سطور تُكتب بإيقاع ضربات مقاس، والصفحة تتمرر لكل سطر ثم قطع إلى بطاقة ورقية. / A bold title then body lines typed on a measured keystroke rhythm, the page scrolling per line, then a cut to a paper card.

**متى:** عند سرد قصة بالكتابة في تطبيق ملاحظات: عنوان عريض ثم سطور تُكتب والصفحة تتمرر مع كل سطر / when telling a story by typing in a notes app: a bold title, then lines typed while the page scrolls

**كيف:** Component notes-typing (lines 'a\|b\|c', speed 0.5–2) and the 24.85 s 1080×1920 block notes-reveal (Courier Prime + Permanent Marker). Arabic version: swap the fonts for Arabic faces and type by grapheme.

**المعاملات:** speed 0.5–2; block 24.85 s 9:16

**التثبيت:** npx hyperframes add notes-reveal

**الوسوم:** ملاحظات · notes · typing story · 9:16 · كتابة قصة · مذكرات · فيديو عمودي · notes app · vertical video

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/notes-typing/notes-typing.html`
- `kosif-one/vendor/hyperframes/registry/blocks/notes-reveal/notes-reveal.html`

#### 7. قدرات قريبة في العائلة

- `UI-30` لوحة أوامر وبحث يصفّي النتائج / Command palette & search filter (seen)
- `UI-31` إجابة متدفقة وسجل حي / Streaming answer & live log (seen)
- `UI-33` جدول ردود الفعل الدقيقة / Micro-feedback timing table (documented)
- `UI-34` ضغط ومرور بمنطق القراءة / Press & hover with reading-direction nudges (ready)

### `UI-33` — جدول ردود الفعل الدقيقة / Micro-feedback timing table

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أزمنة دقيقة لكل لحظة: ضغط، مرور، تبديل، فتح، إشعار، درج، هيكل، علامة صح، اهتزاز خطأ. / Exact timings for press, hover, toggle, expand, toast, drawer, skeleton, success check, error shake.

**متى:** حين تحتاج أزمنة جاهزة لردود فعل الواجهة: ضغط ومرور وتبديل وإشعار ودرج وهيكل واهتزاز خطأ / when you need ready timings for UI feedback: press, hover, toggle, toast, drawer, skeleton, error shake

**كيف:** CSS transitions or WAAPI; the error shake is keyframes on x. Animate only transform and opacity (plus colour), never width/height in renders.

**المعاملات:** press scale 0.97–0.98 in 50–100 ms; hover 1.02; toggle 150–250 ms; expand 200–300 ms; fade 150–300 ms; drawer in 300 / out 250; modal 250 ms .95→1 (out 200); skeleton→content 200–400 ms; check draw 300–500 ms; shake x [0,−10,10,−10,10,0] 0.4 s; arrival bounce spring 200–400 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تفاعل دقيق · microinteraction · press · hover · toggle · shake · timing · مدة الحركة · أزمنة الحركة · اهتزاز الخطأ · durations · ui feedback

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md`
- `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/microinteraction-patterns.md`
- `kosif-tool/styles/ui-micro/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-31` إجابة متدفقة وسجل حي / Streaming answer & live log (seen)
- `UI-32` كتابة في تطبيق الملاحظات / Notes-app typing story (install)
- `UI-34` ضغط ومرور بمنطق القراءة / Press & hover with reading-direction nudges (ready)
- `UI-35` ضغط وتحرير زر نابض / Press-release spring button (documented)

### `UI-34` — ضغط ومرور بمنطق القراءة / Press & hover with reading-direction nudges

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأزرار تنخفض وتنكمش قليلًا عند الضغط وترتفع عند المرور، والأيقونات تدفع باتجاه القراءة. / Buttons press down and shrink, lift on hover, and inline icons nudge in the reading direction.

**متى:** عند ضبط ضغط الأزرار والمرور عليها، مع دفع الأيقونات في اتجاه القراءة / when tuning button press and hover states and nudging inline icons in the reading direction

**كيف:** active: translateY(1px) scale(.985), svg scale(.92); hover (only under @media (hover:hover) and (pointer:fine)): translateY(−1px); inline-end icon translateX(−3px), inline-start 2px; icon action rotate(−7deg) scale(1.06); metric cards lift −2px with icon rotate(−4deg). Transition only colour, background, border, shadow, transform, opacity at 150 ms ease-out. Touch targets ≥ 44 px.

**المعاملات:** 150 ms ease-out; press .985; touch ≥ 44 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ضغط · مرور · press · hover · rtl icons · حالة الزر · مرور الماوس · اتجاه القراءة · button states · hover lift

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-audit-pro/app/globals.css:215`
- `kosif-audit-pro/app/globals.css:223`
- `kosif-audit-pro/app/globals.css:1256`

#### 7. قدرات قريبة في العائلة

- `UI-32` كتابة في تطبيق الملاحظات / Notes-app typing story (install)
- `UI-33` جدول ردود الفعل الدقيقة / Micro-feedback timing table (documented)
- `UI-35` ضغط وتحرير زر نابض / Press-release spring button (documented)
- `UI-36` قلب المفتاح وتبديل الثيم / Toggle flip & theme switch (install)

### `UI-35` — ضغط وتحرير زر نابض / Press-release spring button

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** انضغاط خطي ثم ارتداد نابض على الخاصية نفسها، مع انكماش الظل ودفقة وتوهج خلفي. / Linear compression then spring recovery on the same property, with shadow shrink, release burst and background glow.

**متى:** حين يطلب المستخدم زر دعوة لإجراء ينضغط ثم يرتد بنابض، أو يتحول إلى شريط تقدم / when the user wants a CTA button that compresses then springs back, or flattens into a progress bar

**كيف:** Press linear scale 1 → PRESS_SCALE (~0.9) power1.in while the cursor compresses with it; release back.out(BOUNCE). Product-UI tokens: press 80 ms, release 140 ms spring k300 d20; the showreel pill flattens into a progress bar (scaleX 2.0 / scaleY .24 in .34 s) that fills linearly 1.1 s while a counter climbs.

**المعاملات:** press 80 ms; release 140 ms spring 300/20

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زر · نابض · cta · press spring · release · زر الدعوة · ارتداد · بوتون · bounce · button animation

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/press-release-spring.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/physics-press-reaction.md`
- `kosif-studio/motion/projects/showreel/index.html:78`

#### 7. قدرات قريبة في العائلة

- `UI-33` جدول ردود الفعل الدقيقة / Micro-feedback timing table (documented)
- `UI-34` ضغط ومرور بمنطق القراءة / Press & hover with reading-direction nudges (ready)
- `UI-36` قلب المفتاح وتبديل الثيم / Toggle flip & theme switch (install)
- `UI-37` من التحميل إلى علامة صح / Spinner → success check (install)

### `UI-36` — قلب المفتاح وتبديل الثيم / Toggle flip & theme switch

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** مفتاح كبير يقلب مع تجاوز الإبهام وتلاشي لون المسار؛ أو تبديل الثيم يصبح حدثًا بصريًا. / An oversized toggle flips with thumb overshoot and a track-colour crossfade; or a theme switch becomes the event.

**متى:** عند تحريك مفتاح تشغيل وإيقاف أو جعل التبديل بين الوضع الفاتح والداكن حدثًا بصريًا في الفيديو / when animating an on/off switch or making a light/dark theme switch the visual event

**كيف:** Component toggle-flip (direction on\|off, label, size 20–70). Theme switch: segmented thumb slides 300 ms easeOutCubic then the whole palette crosses cream → chocolate; sun/moon icon orbits in from 75° at .72 scale over 260 ms spring. Gag variant: 'FULL BODY MODE ON' toggle 250 ms while the frame zooms out 400 ms.

**المعاملات:** thumb 300 ms; icon orbit 260 ms from 75°

**التثبيت:** npx hyperframes add toggle-flip

**الوسوم:** مفتاح · وضع داكن · toggle · theme switch · dark mode · تبديل الوضع · الوضع الليلي · سويتش · on off switch · light mode

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/toggle-flip/toggle-flip.html`
- `kosif-audit-pro/app/globals.css:403`
- `style:pm-thilina-a-891c09`
- `style:pm-sab8a-364a5a`

#### 7. قدرات قريبة في العائلة

- `UI-34` ضغط ومرور بمنطق القراءة / Press & hover with reading-direction nudges (ready)
- `UI-35` ضغط وتحرير زر نابض / Press-release spring button (documented)
- `UI-37` من التحميل إلى علامة صح / Spinner → success check (install)
- `UI-38` حقل إدخال: خطأ واهتزاز ونجاح / Input feedback: error shake & valid state (install)

### `UI-37` — من التحميل إلى علامة صح / Spinner → success check

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** قوس يدور ثم ينكمش لدائرة وترسم علامة صح بخطها، مع نبضة حلقة. / A rotating arc collapses into a circle and a check draws by its stroke, with a ring pop.

**متى:** حين يجب أن ينتهي التحميل بعلامة صح تُرسم بخطها مع نبضة حلقة لتأكيد نجاح العملية / when a loading spinner should resolve into a drawn check with a ring pop to confirm success

**كيف:** Arc rotation 0.8 s → collapse → stroke-dashoffset check draw 250 ms (300–500 ms for hero checks). Component success-check (tint, ring subtle\|standard\|bold, spin). Pair with a toast or a 'Saved' label swap.

**المعاملات:** spinner 0.8 s; check 250–500 ms

**التثبيت:** npx hyperframes add success-check

**الوسوم:** نجاح · علامة صح · success · checkmark · spinner · تحميل · تم الحفظ · اكتمال العملية · loading · done state

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/success-check/success-check.html`
- `style:pm-demonugc-4c5753`

#### 7. قدرات قريبة في العائلة

- `UI-35` ضغط وتحرير زر نابض / Press-release spring button (documented)
- `UI-36` قلب المفتاح وتبديل الثيم / Toggle flip & theme switch (install)
- `UI-38` حقل إدخال: خطأ واهتزاز ونجاح / Input feedback: error shake & valid state (install)
- `UI-39` هيكل لامع يتحول إلى محتوى / Skeleton shimmer → content (install)

### `UI-38` — حقل إدخال: خطأ واهتزاز ونجاح / Input feedback: error shake & valid state

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** حقل يهتز عند الخطأ، يعرض اقتراح تصحيح، ثم يتحول حده للأخضر. / A field shakes on error, offers a 'Did you mean…?' pill, then its border turns green.

**متى:** عند إظهار حقل إدخال يهتز عند الخطأ ويقترح تصحيحًا ثم يتحول للأخضر، أو تعبئة نموذج كاملة / when showing an input field that shakes on error, suggests a fix and turns green, or a full form fill

**كيف:** Form recipe: focus ring, type 16 chars at 70 ms ±20, tick 240 ms, focus jumps on spring 170/20, submit, spinner crossfade 120 ms, toast spring 200/22 held ~2 s. Component input-feedback (status valid\|error). Suggestion flow: type 45 ms/char, cursor clicks the pill, border colour change 200 ms.

**المعاملات:** shake 0.4 s; tick 240 ms; toast hold ~2 s

**التثبيت:** npx hyperframes add input-feedback

**الوسوم:** نموذج · تحقق · form · validation · error shake · حقل إدخال · خطأ إدخال · تعبئة نموذج · input field · form fill

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/input-feedback/input-feedback.html`
- `kosif-tool/playbooks/product-ui.md:104-116`
- `style:pm-kmasiff-cc72cb`

#### 7. قدرات قريبة في العائلة

- `UI-36` قلب المفتاح وتبديل الثيم / Toggle flip & theme switch (install)
- `UI-37` من التحميل إلى علامة صح / Spinner → success check (install)
- `UI-39` هيكل لامع يتحول إلى محتوى / Skeleton shimmer → content (install)
- `UI-40` إشعارات: نظام وجزيرة ورصّة / Notifications: native pop, dynamic island, stacks (install)

### `UI-39` — هيكل لامع يتحول إلى محتوى / Skeleton shimmer → content

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** عناصر رمادية يمر عليها ضوء مائل ثم تتلاشى إلى المحتوى الحقيقي. / Grey placeholders with a diagonal light sweep crossfade into real content.

**متى:** حين تحتاج حالة تحميل بعناصر رمادية لامعة تتحول إلى المحتوى، أو اختيار مؤشر التحميل حسب مدة الانتظار / when you need a shimmering skeleton that reveals content, or to pick a loading indicator by wait time

**كيف:** Shimmer = moving linear-gradient 30% wide, 1.2–1.5 s loop; reveal crossfade + slight scale-in 200–400 ms per block. Loading ladder by wait: < 0.3 s nothing; 0.3–1 s inline spinner; 1–5 s skeleton; 5–30 s determinate bar; > 30 s bar + % + ETA; a blank 600–800 ms reads as broken. Component skeleton-reveal.

**المعاملات:** shimmer 1.2–1.5 s; reveal 200–400 ms

**التثبيت:** npx hyperframes add skeleton-reveal

**الوسوم:** تحميل · هيكل · skeleton · shimmer · loading · انتظار · شاشة تحميل · لودينج · placeholder · loading state

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/skeleton-reveal/skeleton-reveal.html`
- `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md`
- `style:pm-justincooperman-e7bbc4`

#### 7. قدرات قريبة في العائلة

- `UI-37` من التحميل إلى علامة صح / Spinner → success check (install)
- `UI-38` حقل إدخال: خطأ واهتزاز ونجاح / Input feedback: error shake & valid state (install)
- `UI-40` إشعارات: نظام وجزيرة ورصّة / Notifications: native pop, dynamic island, stacks (install)
- `UI-41` تحول بطاقة إلى لوحة (FLIP) / Shared-element morph: card → panel (FLIP) (install)

### `UI-40` — إشعارات: نظام وجزيرة ورصّة / Notifications: native pop, dynamic island, stacks

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** إشعار iOS/macOS يسقط بنابض، جزيرة ديناميكية تتمدد، أو رصّة إشعارات تتسارع حتى برج قلق. / An iOS/macOS banner drops on a spring, a dynamic island expands, or notifications pile faster into an anxious tower.

**متى:** عند تصوير إشعار iOS أو macOS ينزل، أو جزيرة ديناميكية تتمدد، أو إشعارات تتراكم فوق بعضها / when showing an iOS or macOS notification drop, a dynamic island expanding, or notifications piling up

**كيف:** Island: 120×36 → 300×80 on spring {stiffness 180, damping 16} ≈ 260 ms; content from 180 ms with 60 ms stagger; hold to 2.4 s; collapse 300 ms. Components native-notification-pop (os ios\|macos, at 0.3 s), notification-stack (1–5 cards, newest on top, one grows as focus), notification-pileup (count 4–10, speed), badge-pop (elastic count). Blocks notification-cascade (14 s, 9:16) and slack-notification-ad (12 s).

**المعاملات:** island 260 ms spring 180/16; hold 2.4 s

**التثبيت:** npx hyperframes add native-notification-pop

**الوسوم:** إشعار · جزيرة ديناميكية · notification · dynamic island · toast · stack · تنبيه · نوتيفيكيشن · شارة العدد · alert · badge

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `os:macos` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:41`
- `kosif-tool/playbooks/phone.md:89-96`
- `kosif-one/vendor/hyperframes/registry/components/native-notification-pop/native-notification-pop.html`
- `kosif-one/vendor/hyperframes/registry/components/notification-stack/notification-stack.html`
- `kosif-one/vendor/hyperframes/registry/blocks/notification-cascade/notification-cascade.html`

#### 7. قدرات قريبة في العائلة

- `UI-38` حقل إدخال: خطأ واهتزاز ونجاح / Input feedback: error shake & valid state (install)
- `UI-39` هيكل لامع يتحول إلى محتوى / Skeleton shimmer → content (install)
- `UI-41` تحول بطاقة إلى لوحة (FLIP) / Shared-element morph: card → panel (FLIP) (install)
- `UI-42` إعادة ترتيب قائمة وسطور / FLIP list reorder & self-reordering lines (seen)

### `UI-41` — تحول بطاقة إلى لوحة (FLIP) / Shared-element morph: card → panel (FLIP)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** بطاقة صغيرة تصبح لوحة كاملة بالتحويل وحده، وأبناؤها يعوّضون المقياس ويعاد ترتيبهم. / A small card becomes a full panel by transform only; children counter-scale and reflow onto measured targets.

**متى:** حين تتوسع بطاقة صغيرة إلى لوحة كاملة أو نافذة بانتقال واحد متصل يحافظ على العنصر نفسه / when a small card should expand into a full panel or modal through one continuous shared-element move

**كيف:** Measure both layouts, animate transform (never width/height in renders), counter-scale children, crossfade content in 150 ms. Component modal-morph (expand_at 1.2 s, register calm\|snappy), card-resize, panel-reveal, menu-morph (hamburger → menu). Single-element morph chain: one container whose width/height/radius/fill are springs retargeted every beat (stiffness ~300, damping ratio ~0.8). Edge-pinned growth uses mask + sheet slide or proxy scaleY with inverse counter-scale.

**المعاملات:** 400–700 ms easeInOutCubic; spring ~300 / ζ 0.8

**التثبيت:** npx hyperframes add modal-morph

**الوسوم:** تحول · flip · shared element · morph · modal · توسيع البطاقة · انتقال سلس · نافذة منبثقة · expand card · card to panel

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/modal-morph/modal-morph.html`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/anchored-layout-expand.md`
- `style:pm-twoclipping-5cba86`
- `style:pm-en-ra-81c6dd`
- `style:pm-antonio-kodheli-490109`

#### 7. قدرات قريبة في العائلة

- `UI-39` هيكل لامع يتحول إلى محتوى / Skeleton shimmer → content (install)
- `UI-40` إشعارات: نظام وجزيرة ورصّة / Notifications: native pop, dynamic island, stacks (install)
- `UI-42` إعادة ترتيب قائمة وسطور / FLIP list reorder & self-reordering lines (seen)
- `UI-43` مؤشرات التبويب والشريط النشط / Tab slide indicator & active rail bar (ready)

### `UI-42` — إعادة ترتيب قائمة وسطور / FLIP list reorder & self-reordering lines

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** البطاقات تنزلق لأماكنها الجديدة، أو سطور مستند تعيد ترتيب نفسها. / Cards slide to new slots, or document lines re-order themselves.

**متى:** عند إعادة ترتيب بطاقات أو عناصر قائمة لتنزلق لأماكنها الجديدة، أو سطور مستند ترتب نفسها / when list items or cards should slide into a new order, or document lines re-order themselves

**كيف:** FLIP 450 ms cubic-bezier(0.2,0.8,0.2,1), stagger 40–60 ms (45 ms cascade). Lines: spring 160/20 with 50 ms offsets; highlight wipe 180 ms with the colour switch at 50%.

**المعاملات:** 450 ms; stagger 40–60 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترتيب · reorder · flip · list · sort · فرز · ترتيب العناصر · تبديل المواقع · rearrange · card order

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/styles/pm-melvynx-6cde6c/BRIEF.md`
- `style:pm-thayto-dev-44b911`

#### 7. قدرات قريبة في العائلة

- `UI-40` إشعارات: نظام وجزيرة ورصّة / Notifications: native pop, dynamic island, stacks (install)
- `UI-41` تحول بطاقة إلى لوحة (FLIP) / Shared-element morph: card → panel (FLIP) (install)
- `UI-43` مؤشرات التبويب والشريط النشط / Tab slide indicator & active rail bar (ready)
- `UI-44` شريط المراحل والحلقة والتقدم / Stepper, progress ring & progress bars (proven)

### `UI-43` — مؤشرات التبويب والشريط النشط / Tab slide indicator & active rail bar

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كبسولة تنزلق بين التبويبات، وشريط رفيع ينمو بجانب العنصر النشط. / A pill slides between tabs; a thin bar grows beside the active nav item.

**متى:** حين يتنقل المشهد بين تبويبات أو عناصر قائمة تنقل ويحتاج مؤشرًا ينزلق إلى العنصر النشط / when switching tabs or nav items and you need an indicator that slides to the active one

**كيف:** Rail: ::after 3 px bar scaleY(0.2)→1 on a 260 ms spring, opacity 160 ms; mobile bottom nav uses a top bar scaleX .25→1; icon lifts translateY(−2px) scale(1.06). Component tabs-slide-indicator (labels, shape pill\|rounded\|square).

**المعاملات:** spring 260 ms; opacity 160 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تبويب · tabs · nav indicator · active state · قائمة التنقل · شريط التبويبات · تابات · navigation bar · bottom nav

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-audit-pro/app/globals.css:527`
- `kosif-audit-pro/app/globals.css:2765`
- `kosif-one/vendor/hyperframes/registry/components/tabs-slide-indicator/tabs-slide-indicator.html`

#### 7. قدرات قريبة في العائلة

- `UI-41` تحول بطاقة إلى لوحة (FLIP) / Shared-element morph: card → panel (FLIP) (install)
- `UI-42` إعادة ترتيب قائمة وسطور / FLIP list reorder & self-reordering lines (seen)
- `UI-44` شريط المراحل والحلقة والتقدم / Stepper, progress ring & progress bars (proven)
- `UI-45` نقطة حالة بهالة وشارة مباشرة / Status dot with halo & live pill (ready)

### `UI-44` — شريط المراحل والحلقة والتقدم / Stepper, progress ring & progress bars

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عقد على خط يمتلئ وتتحول لعلامات صح، حلقة تقدم تدور، وشريط تقدم يساوي t/المدة. / Nodes on a line fill and turn into checks, a progress ring sweeps, and a progress bar equals t/duration.

**متى:** عند إظهار التقدم عبر مراحل بخط يمتلئ وعقد تتحول لعلامات صح، أو حلقة تقدم، أو شريط تقدم للفيلم / when showing progress through steps with filling nodes and checks, a progress ring, or a film progress bar

**كيف:** Film progress bar in the tested starter: #progress width = t/DURATION × 100%, 14 px, #7ee8d2 (rendered in every proof film). Stepper: 5 circles (18 px) on a 3 px line that fills accent node to node, each node pops into a filled check ~150 ms; mono labels under each. Ring: SVG stroke-dashoffset 1200 ms with Arabic status labels crossfading 150 ms (expand 400 ms easeOutQuint). Segmented step bar: N thin 3 px rounded bars, active one fills linearly. Chips: Mono 21 px/700, radius 14, done = mint text, on = lime #d0ff6a with 34 px glow, bad = coral #ff907a.

**المعاملات:** bar 14 px #7ee8d2; node pop ~150 ms; ring 1200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مراحل · شريط تقدم · stepper · progress bar · progress ring · chips · نسبة الإنجاز · خطوات · بروجرس · steps · completion

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/starters/html-canvas/index.html:46`
- `kosif-tool/starters/html-canvas/index.html:211`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:30`
- `style:pm-kmasiff-cc72cb`
- `style:isometric`

#### 7. قدرات قريبة في العائلة

- `UI-42` إعادة ترتيب قائمة وسطور / FLIP list reorder & self-reordering lines (seen)
- `UI-43` مؤشرات التبويب والشريط النشط / Tab slide indicator & active rail bar (ready)
- `UI-45` نقطة حالة بهالة وشارة مباشرة / Status dot with halo & live pill (ready)
- `UI-46` لحظة احتفال توقيعية / Signature celebration moment (idea)

### `UI-45` — نقطة حالة بهالة وشارة مباشرة / Status dot with halo & live pill

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة 8–9 بكسل بلون الحالة مع هالة ناعمة 4 بكسل، أو كبسولة «متصل» بنقطة نابضة. / An 8–9 px state-coloured dot with a soft 4 px halo, or an 'online' pill with a pulsing dot.

**متى:** حين تحتاج الواجهة نقطة حالة ملونة بهالة ناعمة أو شارة «متصل» بنقطة نابضة / when a UI needs a coloured status dot with a soft halo or an online/live pill with a pulsing dot

**كيف:** ::before circle + box-shadow 0 0 0 4px <soft colour>; studio green #54d89c with rgba(84,216,156,.12) halo; verified teal, attention amber, default muted. Live pill: pale-green pill with dot pulse 1.2 s loop.

**المعاملات:** dot 8–9 px; halo 4 px; pulse 1.2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حالة · نقطة · status dot · live · halo · متصل · مباشر · مؤشر الحالة · online indicator · live badge

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-audit-pro/app/globals.css:855`
- `kosif-audit-studio/styles.css:116`
- `style:pm-jhylee95-e1152f`

#### 7. قدرات قريبة في العائلة

- `UI-43` مؤشرات التبويب والشريط النشط / Tab slide indicator & active rail bar (ready)
- `UI-44` شريط المراحل والحلقة والتقدم / Stepper, progress ring & progress bars (proven)
- `UI-46` لحظة احتفال توقيعية / Signature celebration moment (idea)
- `UI-47` ثوابت الهاتف البارامتري / Parametric phone constants (documented)

### `UI-46` — لحظة احتفال توقيعية / Signature celebration moment

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رد فعل مميز للعلامة (انفجار إعجاب، علامة صح مع قصاصات) على الفعل الأكثر ظهورًا. / A distinctive branded reaction (like-burst, check with confetti) on the most visible action.

**متى:** عند إضافة لحظة احتفال مميزة للعلامة كقصاصات أو انفجار إعجاب على أكثر فعل ظهورًا في المنتج / when adding a signature branded celebration, like confetti or a like-burst, on the product's most visible action

**كيف:** One or two per product, always skippable; removal test: if nobody misses it, it is decoration. Build with seeded canvas particles (see PART) — canvas-confetti/tsparticles are installable but use your own seeded burst in renders.

**المعاملات:** 1–2 per product

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** احتفال · قصاصات · celebration · confetti · signature moment · كونفيتي · إعجاب · فرحة · like burst · particles

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/signature-moments.md`

#### 7. قدرات قريبة في العائلة

- `UI-44` شريط المراحل والحلقة والتقدم / Stepper, progress ring & progress bars (proven)
- `UI-45` نقطة حالة بهالة وشارة مباشرة / Status dot with halo & live pill (ready)
- `UI-47` ثوابت الهاتف البارامتري / Parametric phone constants (documented)
- `UI-48` منظور الجهاز وسرعة دورانه / Device perspective, rotation caps & idle hover (documented)

### `UI-47` — ثوابت الهاتف البارامتري / Parametric phone constants

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** هاتف واحد بمقاس شاشة وزوايا متحدة المركز وإطار وجزيرة أو نوتش. / One parametric phone: screen size, concentric radii, bezel, island or notch.

**متى:** حين تحتاج رسم هاتف بمقاسات صحيحة للشاشة والزوايا والإطار والجزيرة أو النوتش لعرض تطبيق / when you need a correctly proportioned phone (screen, radii, bezel, island or notch) to show an app

**كيف:** Screen 390×844 (19.5:9); screen radius 12–14% of width; bezel 2–3%; frame radius = screen radius + bezel; island 120×36 at 12 px from top; notch 210×34 r 20. The screen is clipped live DOM/SVG/Canvas at 2× density; island and home indicator painted after the UI; in-screen text ≥ 30 px, callouts ≥ 36 px; message text lives outside the device.

**المعاملات:** 390×844; radius 12–14% W; bezel 2–3%; island 120×36

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هاتف · phone · device frame · mockup · island · notch · موبايل · جوال · إطار هاتف · phone frame · app screen

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:17`
- `kosif-tool/playbooks/phone.md:19`
- `kosif-tool/playbooks/phone.md:110`

#### 7. قدرات قريبة في العائلة

- `UI-45` نقطة حالة بهالة وشارة مباشرة / Status dot with halo & live pill (ready)
- `UI-46` لحظة احتفال توقيعية / Signature celebration moment (idea)
- `UI-48` منظور الجهاز وسرعة دورانه / Device perspective, rotation caps & idle hover (documented)
- `UI-49` دخول الجهاز وكشف البطل / Device entrance & hero reveal (documented)

### `UI-48` — منظور الجهاز وسرعة دورانه / Device perspective, rotation caps & idle hover

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مسافة منظور وحدود دوران، والهاتف لا يستقر أبدًا على 0°. / Perspective distance and yaw/pitch caps; the rest pose is never 0°.

**متى:** عند تدوير هاتف في منظور ثلاثي الأبعاد وضبط حدود الميل وسرعة الدوران وطفوه الهادئ أثناء الثبات / when rotating a phone in 3D perspective and capping its tilt, rotation speed and idle float

**كيف:** perspective 1200–1600 px (~1.3× width); yaw ±28°, pitch ±8°; rest yaw −6° to −10°. Rotation ≤ 40°/s for reveals, ≤ 4°/s idle; settle overshoot 1–2°; idle hover 6·sin(2πt/3.2) px (≤ 6 px, period ≥ 3.2 s).

**المعاملات:** yaw ±28°; pitch ±8°; ≤ 40°/s; hover ≤ 6 px / 3.2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** منظور · perspective · yaw · rotation · hover · دوران الهاتف · ميلان · طفو · 3d tilt · idle float

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:21`
- `kosif-tool/playbooks/phone.md:34-35`

#### 7. قدرات قريبة في العائلة

- `UI-46` لحظة احتفال توقيعية / Signature celebration moment (idea)
- `UI-47` ثوابت الهاتف البارامتري / Parametric phone constants (documented)
- `UI-49` دخول الجهاز وكشف البطل / Device entrance & hero reveal (documented)
- `UI-50` هاتف 2.5D على Canvas / Canvas 2.5D phone (drawPhone) (ready)

### `UI-49` — دخول الجهاز وكشف البطل / Device entrance & hero reveal

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الهاتف يصعد وزاويته تستقر، يمر انعكاس، تتتابع الواجهة، ثم العنوان ودفعة كاميرا. / The phone rises while yaw settles, a reflection passes, UI rows stagger in, then the headline and a slow push.

**متى:** حين يطلب المستخدم افتتاحية يصعد فيها الهاتف ويستقر ثم تظهر الواجهة والعنوان مع اقتراب الكاميرا / when the user wants an opening where the phone rises and settles, then UI rows, headline and a slow push

**كيف:** Entrance 700–900 ms: rise 120–160 px, yaw −22°→−8°, opacity done by 250 ms; Remotion spring {damping 18, stiffness 90, mass 1.1} or cubic-bezier(0.16,1,0.3,1). Hero recipe (ms): 0–900 rise 140 px; 350–1550 reflection pass; 600–1300 UI rows 70 ms apart; 1200–1800 headline spring 14/120; 900–4000 push to 1.04 with yaw drift ±1.5°. Seen variants: rise from 40% below on black in 600 ms ease-out cubic; overshoot 1.08 in 700 ms with a 2 px squash land.

**المعاملات:** 700–900 ms; rise 120–160 px; yaw −22→−8°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دخول الهاتف · كشف · device entrance · hero reveal · spring · ظهور الهاتف · لقطة افتتاحية · عرض تطبيق · app reveal · phone intro

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:33`
- `kosif-tool/playbooks/phone.md:49-57`
- `style:pm-gautam-mer1-2ae354`
- `kosif-tool/styles/pm-l3d1c-0e35a3/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `UI-47` ثوابت الهاتف البارامتري / Parametric phone constants (documented)
- `UI-48` منظور الجهاز وسرعة دورانه / Device perspective, rotation caps & idle hover (documented)
- `UI-50` هاتف 2.5D على Canvas / Canvas 2.5D phone (drawPhone) (ready)
- `UI-51` مكوّن Device في Remotion / Remotion Device component (install)

### `UI-50` — هاتف 2.5D على Canvas / Canvas 2.5D phone (drawPhone)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** Canvas ثنائي الأبعاد يزيّف دوران الهاتف بضغط العرض cos(yaw) مع ميل خفيف، وظل وقص وجزيرة ولمعة. / 2D canvas fakes yaw by cos(yaw) width squash plus slight shear, with shadow, clip, screen canvas, island and glare.

**متى:** عند رسم هاتف على Canvas ثنائي الأبعاد يوحي بالدوران دون محرك ثلاثي الأبعاد، بزاوية أقل من 28° / when drawing a phone on a 2D canvas that fakes rotation without a 3D engine, under 28° yaw

**كيف:** ctx.transform(cos(rad), sin(rad)·0.12, 0, 1, 0, 0); roundRect clip; drawImage(screenCanvas); glare as a moving linear gradient. Valid below 28° yaw; above that use CSS 3D or a GLTF model.

**المعاملات:** PHONE 420×900 r 60 bezel 12; shadowBlur 90; yaw < 28°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هاتف كانفس · canvas phone · 2.5d · fake 3d · drawPhone · هاتف مرسوم · دوران وهمي · موك أب · pseudo 3d · phone mockup

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:146-179`
- `kosif-tool/starters/html-canvas/index.html`

#### 7. قدرات قريبة في العائلة

- `UI-48` منظور الجهاز وسرعة دورانه / Device perspective, rotation caps & idle hover (documented)
- `UI-49` دخول الجهاز وكشف البطل / Device entrance & hero reveal (documented)
- `UI-51` مكوّن Device في Remotion / Remotion Device component (install)
- `UI-52` تسليم بين جهازين / Two-device turntable handoff (documented)

### `UI-51` — مكوّن Device في Remotion / Remotion Device component

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Remotion برخصة الشركة: مجانية للأفراد والفرق الصغيرة، وتحتاج ترخيصًا للشركات الأكبر / Remotion company license — free for individuals and small teams, paid above that. |

**ما هي:** هاتف React بنابض دخول وضغط ولمعة وظل معاكس للدوران وجزيرة. / A React phone with spring entrance, tap press, glare pass, yaw-opposed shadow and island overlay.

**متى:** حين تبني الفيديو في Remotion وتحتاج مكوّن هاتف React بدخول نابض وضغط ولمعة وظل / when building in Remotion and you need a React phone with spring entrance, tap press, glare and shadow

**كيف:** Inside CameraRig; uses easing.ts progress / easeOutExpo; perspective 1400; rotateX 4deg; glare progress over frames 10–36; R 52, BEZEL 12, frame #15171c.

**المعاملات:** perspective 1400; glare f10–36

**التثبيت:** cd kosif-tool/starters/remotion && npm install

**الوسوم:** ريموشن · remotion · device · react phone · هاتف متحرك · مكون رياكت · لمعة الشاشة · phone component · glare

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:106-143`
- `kosif-tool/starters/remotion/package.json`

#### 7. قدرات قريبة في العائلة

- `UI-49` دخول الجهاز وكشف البطل / Device entrance & hero reveal (documented)
- `UI-50` هاتف 2.5D على Canvas / Canvas 2.5D phone (drawPhone) (ready)
- `UI-52` تسليم بين جهازين / Two-device turntable handoff (documented)
- `UI-53` نافذة متصفح أو ماك وهمية / Browser chrome & macOS frame mock (seen)

### `UI-52` — تسليم بين جهازين / Two-device turntable handoff

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الجهاز الأول يستدير وينزلق، الثاني يدخل، وعنصر مشترك يطير بينهما على قوس. / Device A turns away and slides, B enters, a shared element flies between them on an arc.

**متى:** عند الانتقال من جهاز إلى آخر، كمتصفح إلى هاتف، مع عنصر مشترك يطير بينهما على قوس / when moving from one device to another, such as browser to phone, with a shared element flying between them

**كيف:** A yaw −8°→+28° and slide 220 px; B +30°→+8°, scale 0.9→1 over 1400 ms cubic-bezier(0.65,0,0.35,1); specular pass 500–700 ms; shared element 700–1000 ms; settle with a 1.5° overshoot spring 16/100. Browser→phone morph alternative: one tween of width/height/radius in 600 ms with content reflowing, not scaling.

**المعاملات:** 1400 ms; shared element 700–1000 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جهازان · handoff · turntable · browser to phone · انتقال بين الأجهزة · من المتصفح للجوال · دوران الجهاز · device transition · cross device

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:79-87`
- `kosif-tool/styles/pm-deifosv-04e4d3/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `UI-50` هاتف 2.5D على Canvas / Canvas 2.5D phone (drawPhone) (ready)
- `UI-51` مكوّن Device في Remotion / Remotion Device component (install)
- `UI-53` نافذة متصفح أو ماك وهمية / Browser chrome & macOS frame mock (seen)
- `UI-54` مروحة أجهزة وانفراد الهواتف / Multi-device splay & phone fan-out (install)

### `UI-53` — نافذة متصفح أو ماك وهمية / Browser chrome & macOS frame mock

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نافذة مستديرة بأضواء المرور وشريط رابط، أو شريط قوائم ماك بأيقوناته وخلفية متدرجة. / A rounded window with traffic-light dots and a URL pill, or a macOS menu bar with status icons over a gradient wallpaper.

**متى:** حين تحتاج نافذة متصفح أو ماك وهمية بأضواء المرور وشريط رابط لعرض موقع أو تطبيق ويب / when you need a mock browser or macOS window with traffic-light dots and a URL bar to show a site or web app

**كيف:** Window radius 12 px, shadow 0 20–30px 60px rgba(0,0,0,.12), slide up 20 px + fade 500 ms; inner grid scrolls 600 px over 3 s ease-in-out. macOS frame: black bezel band, navy menu bar ~60 px on a 1080 stage, three coloured dots, date/time. Component browser-device-stage (chrome browser\|window\|phone, screen slot with skeleton default, optional crossfade to a second screen at swap_at).

**المعاملات:** radius 12 px; slide 20 px / 500 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** متصفح · نافذة · browser mockup · macos · window chrome · موقع ويب · شريط العنوان · إطار المتصفح · website mockup · url bar

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `os:macos` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-ai-baymax-0ef9dd`
- `style:pm-wani-shola-16ca7a`
- `style:pm-notdwd-c2037d`
- `kosif-one/vendor/hyperframes/registry/components/browser-device-stage/browser-device-stage.html`

#### 7. قدرات قريبة في العائلة

- `UI-51` مكوّن Device في Remotion / Remotion Device component (install)
- `UI-52` تسليم بين جهازين / Two-device turntable handoff (documented)
- `UI-54` مروحة أجهزة وانفراد الهواتف / Multi-device splay & phone fan-out (install)
- `UI-55` آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية / 3D GLTF iPhone & MacBook with live screens (install)

### `UI-54` — مروحة أجهزة وانفراد الهواتف / Multi-device splay & phone fan-out

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** هاتف وجهاز لوحي وحاسوب تنفرد من رصّة مركزية، أو هاتف واحد يتكاثر لخمسة كالمروحة. / Phone, tablet and desktop fan out from a centred stack, or one phone multiplies into five like a fan.

**متى:** عند عرض المنتج على هاتف وجهاز لوحي وحاسوب معًا، أو هاتف يتكاثر إلى خمسة كالمروحة / when showing a product on phone, tablet and desktop together, or one phone multiplying into a fan of five

**كيف:** Fan-out: duplicate into 5 phones translating outward with rotation ±6°/±12°, outer ones slightly lower and smaller, soft shadow, 600 ms spring, 40 ms stagger from the centre. Components multi-device-splay and device-frame-stage (phone\|tablet, cutout none\|island\|notch, body graphite\|silver, idle float).

**المعاملات:** rotate ±6/±12°; 600 ms; 40 ms stagger

**التثبيت:** npx hyperframes add multi-device-splay

**الوسوم:** أجهزة · مروحة · multi device · fan out · splay · هاتف وتابلت · شاشات متعددة · تابلت · tablet · desktop

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/multi-device-splay/multi-device-splay.html`
- `kosif-one/vendor/hyperframes/registry/components/device-frame-stage/device-frame-stage.html`
- `style:pm-samuel-yostt-891f87`

#### 7. قدرات قريبة في العائلة

- `UI-52` تسليم بين جهازين / Two-device turntable handoff (documented)
- `UI-53` نافذة متصفح أو ماك وهمية / Browser chrome & macOS frame mock (seen)
- `UI-55` آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية / 3D GLTF iPhone & MacBook with live screens (install)
- `UI-56` موك أب HTML بلقطة 2× / HTML/CSS device & package mockup screenshot (ready)

### `UI-55` — آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية / 3D GLTF iPhone & MacBook with live screens

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). Apple-style device models are look-alikes — never imply Apple endorsement. |

**ما هي:** نماذج GLTF لآيفون وماك بوك مع شاشات HTML حية وعدسة زجاج وكاميرا مراجعة منتج ودوران 360. / GLTF iPhone 15 Pro Max and MacBook Pro with live HTML-in-Canvas screens, a glass lens, review-style camera moves and a 360 turntable.

**متى:** حين يطلب المستخدم آيفون أو ماك بوك ثلاثي الأبعاد بشاشة حية ودوران 360 بأسلوب مراجعات المنتجات / when the user wants a 3D iPhone or MacBook with a live screen and a 360 turntable, product-review style

**كيف:** Blocks vfx-iphone-device (15 s), ios26-liquid-glass (15 s home screen with liquid-glass icons), macos-tahoe-liquid-glass (15 s). Engine: Three.js 0.147 from CDN + HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage — an experimental Chromium API: verify it in this Chromium before promising) + GSAP paused timeline.

**المعاملات:** 15 s; 1920×1080

**التثبيت:** npx hyperframes add vfx-iphone-device

**الوسوم:** آيفون · ماك بوك · 3d phone · gltf · liquid glass · turntable · مجسم ثلاثي الأبعاد · دوران 360 · لابتوب · three.js · 360 spin

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `os:macos` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/blocks/vfx-iphone-device/vfx-iphone-device.html`
- `kosif-one/vendor/hyperframes/registry/blocks/ios26-liquid-glass/ios26-liquid-glass.html`
- `kosif-one/vendor/hyperframes/registry/blocks/macos-tahoe-liquid-glass/macos-tahoe-liquid-glass.html`

#### 7. قدرات قريبة في العائلة

- `UI-53` نافذة متصفح أو ماك وهمية / Browser chrome & macOS frame mock (seen)
- `UI-54` مروحة أجهزة وانفراد الهواتف / Multi-device splay & phone fan-out (install)
- `UI-56` موك أب HTML بلقطة 2× / HTML/CSS device & package mockup screenshot (ready)
- `UI-57` قلب الهاتف وتبديل الشاشة / Phone flip with mid-swap (idea)

### `UI-56` — موك أب HTML بلقطة 2× / HTML/CSS device & package mockup screenshot

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضع الصورة داخل جهاز أو عبوة بظلال CSS والتقط بكثافة 2×. / Place an image inside a device or package with CSS shadows and capture at 2× DPR.

**متى:** عند وضع صورة أو تصميم داخل إطار جهاز أو عبوة منتج والتقاطها صورة عالية الدقة / when placing an image or design inside a device or package frame and capturing it as a high-res still

**كيف:** Playwright page.screenshot with deviceScaleFactor 2 (Playwright + Chromium installed here). The KOSIF approved mockups (iMac dashboard, four iPhones on a stone plinth, audit laptop, 1448×1086 WebP) are the visual reference for Arabic RTL product composites: navy rail, white cards, blue/green bars.

**المعاملات:** 2× DPR; reference 1448×1086

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** موك أب · mockup · screenshot · device composite · 2x · عبوة منتج · عرض التصميم · صورة عالية الدقة · package mockup · playwright

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `100-superskills/skills/product-photo-mockups/SKILL.md:24`
- `kosif-earth-ci-fork/docs/design/mockups/kosif-iphone.webp`
- `kosif-earth-ci-fork/docs/design/mockups/kosif-laptop-dashboard.webp`

#### 7. قدرات قريبة في العائلة

- `UI-54` مروحة أجهزة وانفراد الهواتف / Multi-device splay & phone fan-out (install)
- `UI-55` آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية / 3D GLTF iPhone & MacBook with live screens (install)
- `UI-57` قلب الهاتف وتبديل الشاشة / Phone flip with mid-swap (idea)
- `UI-58` جولة تمرير مع شروحات / Scroll tour with callouts (documented)

### `UI-57` — قلب الهاتف وتبديل الشاشة / Phone flip with mid-swap

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الهاتف ينقلب 180° وتتبدل الشاشة عند 90°. / The phone flips 180° and swaps its screen at 90°.

**متى:** حين تريد قلب الهاتف 180° لتبديل الشاشة في منتصف الدوران والانتقال لواجهة أخرى / when you want to flip a phone 180° and swap its screen at the midpoint to reveal another view

**كيف:** CSS 3D rotateY 700 ms; swap content exactly at the 90° frame (backface hidden); keep tilt ≤ ±8° on the other axis.

**المعاملات:** 700 ms; swap at 90°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قلب · flip · phone · swap · انقلاب الهاتف · تغيير الشاشة · لف الجهاز · rotate · screen swap

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/styles/pm-cansincengiz-me-cf68dd/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `UI-55` آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية / 3D GLTF iPhone & MacBook with live screens (install)
- `UI-56` موك أب HTML بلقطة 2× / HTML/CSS device & package mockup screenshot (ready)
- `UI-58` جولة تمرير مع شروحات / Scroll tour with callouts (documented)
- `UI-59` خطوط شرح قائدة / Callout leader lines (documented)

### `UI-58` — جولة تمرير مع شروحات / Scroll tour with callouts

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرح يُرسم، توقف، ثم يتمرر المحتوى بينما يبقى الإطار ثابتًا والخلفية تتحرك قليلًا. / A callout draws, dwells, then content scrolls while the chrome stays fixed and the background parallaxes.

**متى:** عند جولة في صفحة أو تطبيق بالتمرير مع شروحات تظهر بعد توقف كل تمريرة / when touring a page or app by scrolling, with callouts appearing after each scroll stops

**كيف:** Scroll −720 px in 800 ms cubic-bezier(0.45,0,0.15,1), bg parallax −24 px; callouts appear only after the scroll ends (+150 ms). Phone version: card-per-beat steps of 450 ms ≈ 62% of the screen height, hold ≥ 600 ms, device counter-rotates 2°, ≤ 5 cards, never linear scroll over 2 s.

**المعاملات:** −720 px / 800 ms; hold ≥ 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تمرير · جولة · scroll tour · callouts · parallax · سكرول · شرح الصفحة · تمرير الشاشة · page tour · scrolling

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/product-ui.md:91-102`
- `kosif-tool/playbooks/phone.md:38`
- `kosif-tool/playbooks/phone.md:72-77`
- `kosif-tool/styles/pm-cansincengiz-me-cf68dd/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `UI-56` موك أب HTML بلقطة 2× / HTML/CSS device & package mockup screenshot (ready)
- `UI-57` قلب الهاتف وتبديل الشاشة / Phone flip with mid-swap (idea)
- `UI-59` خطوط شرح قائدة / Callout leader lines (documented)
- `UI-60` اقتراب يقوده المؤشر / Cursor-led push-in & focus zoom (seen)

### `UI-59` — خطوط شرح قائدة / Callout leader lines

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الشروح خارج الجهاز تتبع عنصرها، وخطوطها تُرسم. / Callouts outside the device follow their element and their leader lines draw on.

**متى:** حين تحتاج شروحًا خارج الجهاز تشير لعناصر الواجهة بخطوط تُرسم وتتبع عنصرها / when you need labels outside the device pointing to UI elements with drawn leader lines that track them

**كيف:** Rows 60–90 ms stagger; callout +120 ms; leader 260 ms cubic-bezier(0.16,1,0.3,1); mono caps labels; dotted variant dash 2/4 drawn in 400 ms, 120 ms stagger from input chips into the phone UI.

**المعاملات:** leader 260 ms; stagger 60–90 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شرح · خط قائد · callout · leader line · annotation · تعليقات توضيحية · أسهم الشرح · تسميات · labels · pointer lines

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/phone.md:39`
- `style:pm-jesscaroline7-1ff7cb`
- `style:pm-gabrielbuzziv-4ff0c6`

#### 7. قدرات قريبة في العائلة

- `UI-57` قلب الهاتف وتبديل الشاشة / Phone flip with mid-swap (idea)
- `UI-58` جولة تمرير مع شروحات / Scroll tour with callouts (documented)
- `UI-60` اقتراب يقوده المؤشر / Cursor-led push-in & focus zoom (seen)
- `UI-61` وصفة النقر وفتح نافذة / Click → modal recipe (documented)

### `UI-60` — اقتراب يقوده المؤشر / Cursor-led push-in & focus zoom

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكاميرا تقترب نحو موضع النقرة ثم تتوقف لحظة. / The camera pushes toward the click point and holds.

**متى:** عند اقتراب الكاميرا من موضع النقرة في عرض واجهة لإبراز التفاصيل ثم التوقف لحظة / when the camera should push toward the click point in a UI demo to highlight detail, then hold

**كيف:** Push cubic-bezier(0.22,1,0.36,1) 900 ms, max 1.6×, 300 ms hold; focus zoom up to 1.4× needs a 2× render of the UI (1→1.3 in the modal recipe). Cursor 24 px quad-bezier 350–450 ms, click squash 0.9 in 90 ms.

**المعاملات:** 900 ms; ≤ 1.6×; render 2× for zoom

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** اقتراب · زوم · push in · focus zoom · camera · تقريب · تكبير الشاشة · حركة كاميرا · zoom in · click focus

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/styles/pm-techyoutbe-945b56/BRIEF.md`
- `kosif-tool/styles/ui-micro/SKILL.md`
- `kosif-tool/playbooks/product-ui.md:77-89`

#### 7. قدرات قريبة في العائلة

- `UI-58` جولة تمرير مع شروحات / Scroll tour with callouts (documented)
- `UI-59` خطوط شرح قائدة / Callout leader lines (documented)
- `UI-61` وصفة النقر وفتح نافذة / Click → modal recipe (documented)
- `UI-62` صفحة ويب مائلة تتمرر / 3D tilted webpage scroll & perspective pan (documented)

### `UI-61` — وصفة النقر وفتح نافذة / Click → modal recipe

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قوس المؤشر، مرور، ضغط، تحرير، خلفية معتمة، لوحة بنابض، حقول متتابعة، اقتراب، توقف. / Cursor arc, hover, press, release, backdrop, panel spring, field stagger, focus zoom, dwell.

**متى:** حين يضغط المؤشر زرًا فتفتح نافذة منبثقة بنابض وتتتابع حقولها ثم تقترب الكاميرا / when the cursor clicks a button that opens a spring modal with staggered fields and a focus zoom

**كيف:** Times (ms): 0 / 560 / 700 / 780 / 860 / 880 / 1000 / 1600 / 2200. Remotion CursorPress: travel 17 frames, pressAt 21, ripple 48 px, accent #19c37d; modal at pressAt+5; focus 1→1.3. Arrival recipe before it: 0–520 rise, chrome 400–900 with 60 ms stagger, 6 cards 700–1300 at 50 ms, push 1.05 over 4 s.

**المعاملات:** press at 700–780 ms; modal +5 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نافذة · modal · click recipe · remotion · نافذة منبثقة · بوب أب · فتح نافذة · popup · dialog

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/product-ui.md:77-89`
- `kosif-tool/playbooks/product-ui.md:124-158`
- `kosif-tool/playbooks/product-ui.md:66-75`

#### 7. قدرات قريبة في العائلة

- `UI-59` خطوط شرح قائدة / Callout leader lines (documented)
- `UI-60` اقتراب يقوده المؤشر / Cursor-led push-in & focus zoom (seen)
- `UI-62` صفحة ويب مائلة تتمرر / 3D tilted webpage scroll & perspective pan (documented)
- `UI-63` جدار بطاقات واجهة يطفو بعمق / Floating UI card wall in depth (seen)

### `UI-62` — صفحة ويب مائلة تتمرر / 3D tilted webpage scroll & perspective pan

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صفحة كاملة كبطاقة مائلة في المنظور يتمرر محتواها بنابض. / A full webpage as a tilted 3D card whose content scrolls with spring easing.

**متى:** حين تريد عرض صفحة ويب كاملة مائلة في المنظور يتمرر محتواها أو تنزلق عبر الإطار كلحظة مغايرة / when showing a full webpage tilted in 3D perspective, scrolling or panning across frame as a contrast moment

**كيف:** perspective + rotateX/rotateY; radius 24 px; shadow 40px 30px 80px rgba(0,0,0,.45); one paused GSAP timeline with fromTo explicit states, transforms/opacity only. Pan variant: rotateX 20° rotateY −15°, translate the parent across in 3 s ease-in-out. Use as a contrast moment, not the main idea — tilt cards are a tired default.

**المعاملات:** rotateX 20° / rotateY −15°; 3 s pan

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** منظور · صفحة مائلة · 3d page scroll · tilted ui · perspective pan · عرض موقع · ميلان ثلاثي الأبعاد · تمرير الصفحة · website showcase · webpage scroll

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/3d-page-scroll.md`
- `style:pm-daniel-haida-8691d4`
- `style:pm-jayscambler-3f8889`

#### 7. قدرات قريبة في العائلة

- `UI-60` اقتراب يقوده المؤشر / Cursor-led push-in & focus zoom (seen)
- `UI-61` وصفة النقر وفتح نافذة / Click → modal recipe (documented)
- `UI-63` جدار بطاقات واجهة يطفو بعمق / Floating UI card wall in depth (seen)
- `UI-64` عدسة تكبير التفاصيل / Magnifier lens pass (documented)

### `UI-63` — جدار بطاقات واجهة يطفو بعمق / Floating UI card wall in depth

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة بطاقات بمستويات Z مختلفة والكاميرا تتقدم، والضبابية تتبع بعد البطاقة عن مستوى التركيز. / A grid of cards at varied translateZ; the camera dollies in; blur follows distance from the focal plane.

**متى:** عند عرض جدار بطاقات أو صور مصغرة في عمق ثلاثي الأبعاد تتقدم نحوه الكاميرا مع ضبابية حسب البعد / when showing a wall of cards or thumbnails in 3D depth as the camera dollies in with distance blur

**كيف:** perspective 1200 px; 3–5 columns of skeleton post cards; blur 0–8 px by \|z − focus\|; dolly 2 s. Wall-of-thumbnails variant: dim all but the chosen to 0.3 opacity and scale it 1.05.

**المعاملات:** perspective 1200; blur 0–8 px; dolly 2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جدار بطاقات · card wall · depth of field · dolly · شبكة بطاقات · عمق · صور مصغرة · thumbnails · blur

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-robj3d3-b18fad`
- `style:pm-reyzostyle-b55864`
- `style:pm-aistocksavvy-3fb9f5`

#### 7. قدرات قريبة في العائلة

- `UI-61` وصفة النقر وفتح نافذة / Click → modal recipe (documented)
- `UI-62` صفحة ويب مائلة تتمرر / 3D tilted webpage scroll & perspective pan (documented)
- `UI-64` عدسة تكبير التفاصيل / Magnifier lens pass (documented)
- `UI-65` نقطة ساخنة مع فقاعة إرشاد / Hotspot tooltip walkthrough (seen)

### `UI-64` — عدسة تكبير التفاصيل / Magnifier lens pass

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دائرة مكبرة تنزلق على سطح المنتج فتكشف الملمس مع تسمية. / A magnified circle glides over the product surface revealing texture with a label.

**متى:** حين تريد إبراز ملمس أو تفاصيل دقيقة في المنتج بعدسة مكبرة تنزلق على سطحه مع تسمية / when you want to reveal texture or fine detail on a product with a magnifying lens gliding over it

**كيف:** 0–1 s product, 1–4 s lens pass, 4–6 s detail hold. Enlarged copy inside clip-path:circle() whose centre follows the lens path, with compensating background-position. Never present invented detail as real photography.

**المعاملات:** 6 s; lens pass 3 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عدسة · تكبير · magnifier · lens · detail · عدسة مكبرة · إبراز التفاصيل · زووم · zoom lens · close-up

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md`

#### 7. قدرات قريبة في العائلة

- `UI-62` صفحة ويب مائلة تتمرر / 3D tilted webpage scroll & perspective pan (documented)
- `UI-63` جدار بطاقات واجهة يطفو بعمق / Floating UI card wall in depth (seen)
- `UI-65` نقطة ساخنة مع فقاعة إرشاد / Hotspot tooltip walkthrough (seen)
- `UI-66` مقارنة قبل وبعد / Before/after wipe & comparison split (install)

### `UI-65` — نقطة ساخنة مع فقاعة إرشاد / Hotspot tooltip walkthrough

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة بلون العلامة تنبض على الهدف، المؤشر يصل، وتظهر فقاعة إرشاد بعدّاد «1 من 4». / A pulsing brand dot marks the target, the cursor arrives, and a tooltip card with an 'n of 4' counter pops below.

**متى:** عند شرح ميزات تطبيق خطوة بخطوة بنقطة نابضة على الهدف وفقاعة إرشاد بعداد الخطوات / when explaining app features step by step with a pulsing hotspot and a tooltip card with a step counter

**كيف:** Pulse 1 s loop; tooltip pop 200 ms with Back/Next buttons. Split variant: chat bubbles on the left (40%) drive the product UI on the right (60%), bubble stagger ~600 ms. Component onboarding-stepper-flow (milestone rail + step card).

**المعاملات:** pulse 1 s; pop 200 ms; split 40/60

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إرشاد · تهيئة · hotspot · tooltip · onboarding tour · جولة تعريفية · شرح الميزات · تلميح · product tour · walkthrough

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-jhylee95-e1152f`
- `kosif-one/vendor/hyperframes/registry/components/onboarding-stepper-flow/onboarding-stepper-flow.html`

#### 7. قدرات قريبة في العائلة

- `UI-63` جدار بطاقات واجهة يطفو بعمق / Floating UI card wall in depth (seen)
- `UI-64` عدسة تكبير التفاصيل / Magnifier lens pass (documented)
- `UI-66` مقارنة قبل وبعد / Before/after wipe & comparison split (install)
- `UI-67` دوار الشاشات والموكاب الثابت / Screen-flow carousel & sticky mock swap (install)

### `UI-66` — مقارنة قبل وبعد / Before/after wipe & comparison split

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** طبقتان كاملتان وخط فاصل يمسح الطبقة الثانية ويستقر عند نسبة. / Two full-bleed layers; a divider wipes the 'after' across and rests at a split.

**متى:** حين يطلب المستخدم مقارنة قبل وبعد بخط فاصل يمسح الصورة ويستقر عند نسبة / when the user wants a before/after comparison with a divider wiping across and resting at a split

**كيف:** clip-path: inset() on the top layer, divider x 0→100% ease-in-out 1.2 s, rest at 50%. Components before-after-wipe (rest_split, wipe_at 0.25 s, labels) and comparison-split (muted before vs vivid after, horizontal\|vertical). Arabic: the 'after' enters from the right.

**المعاملات:** wipe 1.2 s; rest 50%

**التثبيت:** npx hyperframes add before-after-wipe

**الوسوم:** قبل وبعد · before after · wipe · comparison · مقارنة النتائج · خط فاصل · الفرق · split screen · reveal slider

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/before-after-wipe/before-after-wipe.html`
- `kosif-one/vendor/hyperframes/registry/components/comparison-split/comparison-split.html`
- `style:pm-oliahmed205-3e31c4`

#### 7. قدرات قريبة في العائلة

- `UI-64` عدسة تكبير التفاصيل / Magnifier lens pass (documented)
- `UI-65` نقطة ساخنة مع فقاعة إرشاد / Hotspot tooltip walkthrough (seen)
- `UI-67` دوار الشاشات والموكاب الثابت / Screen-flow carousel & sticky mock swap (install)
- `UI-68` شبكة بنتو للميزات / Bento feature grid (seen)

### `UI-67` — دوار الشاشات والموكاب الثابت / Screen-flow carousel & sticky mock swap

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** 2–5 شاشات على سكة، الوسطى أساسية والجيران يتراجعون؛ أو موكاب ثابت تتبدل ميزاته مع العناوين. / 2–5 app screens ride a rail with the centre primary and neighbours receding; or a pinned mock crossfades through features while captions rise.

**متى:** عند عرض عدة شاشات تطبيق على سكة متحركة، أو موكاب ثابت تتبدل ميزاته مع العناوين / when showing several app screens on a moving rail, or a pinned mock swapping features as captions change

**كيف:** Advance on cues with a velocity-matched throw and long-tail catch; caption swaps with each stop. Seen: covers sliding x with 80 ms stagger and slight 3D tilt; cropped-edge strip moving ~120 px/s; slot-reel portrait scroller decelerating onto one card in 1.0 s (blur 0→30→0 px, overshoot 1.1). Components screen-flow-carousel, sticky-mock-swap; block app-showcase (three floating phone screens, 5.5 s).

**المعاملات:** strip ~120 px/s; slot reel 1.0 s

**التثبيت:** npx hyperframes add screen-flow-carousel

**الوسوم:** دوار · carousel · screens · feature swap · شاشات التطبيق · سلايدر شاشات · عرض الميزات · app screens · slider

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/screen-flow-carousel/screen-flow-carousel.html`
- `kosif-one/vendor/hyperframes/registry/components/sticky-mock-swap/sticky-mock-swap.html`
- `kosif-one/vendor/hyperframes/registry/blocks/app-showcase/app-showcase.html`
- `style:pm-brainextends-e19ac3`
- `style:pm-samuel-yostt-891f87`

#### 7. قدرات قريبة في العائلة

- `UI-65` نقطة ساخنة مع فقاعة إرشاد / Hotspot tooltip walkthrough (seen)
- `UI-66` مقارنة قبل وبعد / Before/after wipe & comparison split (install)
- `UI-68` شبكة بنتو للميزات / Bento feature grid (seen)
- `UI-69` لوحة قياس HUD وشروح مسقطة من 3D / Instrument-panel HUD & projected callouts (ready)

### `UI-68` — شبكة بنتو للميزات / Bento feature grid

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقات مستديرة بواجهات مصغرة متحركة تظهر بالتتابع. / Rounded cards with mini animated UIs pop in staggered.

**متى:** حين تحتاج عرض ميزات المنتج في شبكة بطاقات مستديرة بواجهات مصغرة متحركة تظهر بالتتابع / when presenting product features in a grid of rounded cards with mini animated UIs popping in

**كيف:** Stagger 80–100 ms, radius 20 px. Design-system bento: 12-column grid, 24 px gutter; modules = frame counter 'f 047/900' with progress, palette swatches, 'Aa' type specimen, easing plots (expo.out, power3.inOut, back.out(1.7)), BPM meter.

**المعاملات:** stagger 80–100 ms; radius 20 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بنتو · bento · feature grid · design system · ميزات المنتج · شبكة بطاقات · بطاقات · features · card grid

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-sudo-kiran-4f8b59`
- `style:pm-grace-sunnyy-29bc61`
- `style:pm-thayto-dev-44b911`

#### 7. قدرات قريبة في العائلة

- `UI-66` مقارنة قبل وبعد / Before/after wipe & comparison split (install)
- `UI-67` دوار الشاشات والموكاب الثابت / Screen-flow carousel & sticky mock swap (install)
- `UI-69` لوحة قياس HUD وشروح مسقطة من 3D / Instrument-panel HUD & projected callouts (ready)
- `UI-70` مربع تتبع وماسح ضوئي / AI tracking box & scanner brackets (seen)

### `UI-69` — لوحة قياس HUD وشروح مسقطة من 3D / Instrument-panel HUD & projected callouts

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريط عنوان وساعة وأشرطة زمنية وثلاث لوحات رسوم حية، وشروح بحلقات منقطة مسقطة من نقاط ثلاثية الأبعاد. / Title strip, clock, timeline bars, three live chart panels and dashed-ring callouts projected from 3D anchors.

**متى:** عند بناء لوحة قياس تقنية بأشرطة زمنية ورسوم حية وشروح مسقطة من نقاط في مشهد ثلاثي الأبعاد / when building a technical HUD with live chart panels and callouts projected from 3D scene anchors

**كيف:** H = K3.hud(root, W, H, {title, subtitle, panels, accent, ink, paper, font, seed}); H.addCallout({anchor, label, title, text, side, measure}); H.update(t, camera, {stage, side, duration}) — call camera.updateMatrixWorld() first. Floor: K3S.stageDisc({radius .32, color #9dffb4}) with grid, rings, 36 ticks and a uScan sweep. Lighter version: component telemetry-hud (mono label:value lines, corner brackets).

**المعاملات:** lime #a8ff3c, ink #0f1512, paper #f4f2ec; IBM Plex Mono; top 8.5% H, bottom 20% H

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hud · لوحة قياس · instrument panel · callouts · 3d labels · واجهة تقنية · رسوم حية · تسميات المشهد · heads-up display · live charts

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-studio/motion/kit/lab-kit.js:207`
- `kosif-studio/motion/kit/shape-kit.js:343`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:207`
- `kosif-one/vendor/hyperframes/registry/components/telemetry-hud/telemetry-hud.html`

#### 7. قدرات قريبة في العائلة

- `UI-67` دوار الشاشات والموكاب الثابت / Screen-flow carousel & sticky mock swap (install)
- `UI-68` شبكة بنتو للميزات / Bento feature grid (seen)
- `UI-70` مربع تتبع وماسح ضوئي / AI tracking box & scanner brackets (seen)
- `UI-71` مسرح أداة تصميم ومقابض تحديد / Design-tool canvas, selection handles & size tags (seen)

### `UI-70` — مربع تتبع وماسح ضوئي / AI tracking box & scanner brackets

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** زوايا L صفراء تتبع هدفًا مع نسبة ثقة متذبذبة، أو أربع زوايا تنقفل على بطاقة وخط مسح يكتسحها. / Yellow L-bracket corners follow a target with a fluctuating confidence label, or four corners snap onto a card while a scan line sweeps.

**متى:** حين تريد مربع تتبع بزوايا ونسبة ثقة يلاحق هدفًا، أو ماسحًا ينقفل على بطاقة بخط مسح / when you want an AI-style box tracking a target with a confidence label, or scanner corners with a sweep line

**كيف:** Tracking box: #facc15, corners 48×48 px with 6 px border, confidence 95–99% (seeded), box derived from the target each frame. Scanner: corners 14 px stroke r12 snap in 250 ms back-out, green glowing line sweeps 900 ms, then lavender line highlights #c9cdf5 @0.6 with 70 ms stagger. Beat lock: an outlined box with 0 0 24px #e8501f glow hops cards per beat, overshoots, locks, dims the rest to 30%. Component camera-scan-gate ends on 'Verified'.

**المعاملات:** corners 48 px / 6 px; sweep 900 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تتبع · ماسح · tracking box · scanner · ocr · qr · تتبع هدف · مسح ضوئي · نسبة الثقة · target lock · scan line

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/ai-tracking-box.md`
- `style:pm-mehul4795-4a7007`
- `style:pm-tankazunori0914-0fc886`
- `kosif-one/vendor/hyperframes/registry/components/camera-scan-gate/camera-scan-gate.html`

#### 7. قدرات قريبة في العائلة

- `UI-68` شبكة بنتو للميزات / Bento feature grid (seen)
- `UI-69` لوحة قياس HUD وشروح مسقطة من 3D / Instrument-panel HUD & projected callouts (ready)
- `UI-71` مسرح أداة تصميم ومقابض تحديد / Design-tool canvas, selection handles & size tags (seen)
- `UI-72` تسجيل صفحة بخطوات مبرمجة / Scripted page recording (Playwright) (ready)

### `UI-71` — مسرح أداة تصميم ومقابض تحديد / Design-tool canvas, selection handles & size tags

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل العمل كإطارات على لوحة فاتحة بشبكة نقاط، وكاميرا افتراضية تتنقل، ومستطيل تحديد بمقابض ووسم مقاس. / All work as labelled frames on a light dotted canvas with a virtual camera, plus selection boxes with handles and a 'W × H' tag.

**متى:** عند عرض عمل تصميم كإطارات على لوحة منقطة بكاميرا تتنقل، مع مستطيل تحديد بمقابض ووسم مقاس / when showing design work as frames on a dotted canvas with a moving camera, plus selection handles and a size tag

**كيف:** Dot grid 24 px on #e8e7e3; file chip top-right, zoom % badge bottom-left; move a container (scale + translate) instead of cutting. Selection: 1.5 px accent rect, 4 (or 8) square handles, filled tag below, appear 120–150 ms. Blueprint overlay: duplicate the UI as 1 px cyan #3fb6d2 strokes with 8% fill and crossfade 400 ms. Component vector-editor-rig (pen path, anchors, bezier handles).

**المعاملات:** dot grid 24 px; handles appear 120–150 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أداة تصميم · design tool · selection handles · canvas · figma style · لوحة التصميم · مقابض التحجيم · شبكة نقاط · design canvas · resize handles

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-kikelopezdesign-7cc9e8`
- `style:pm-moguzbulbul-6311b6`
- `style:pm-arjunsh1607-93005d`
- `kosif-one/vendor/hyperframes/registry/components/vector-editor-rig/vector-editor-rig.html`

#### 7. قدرات قريبة في العائلة

- `UI-69` لوحة قياس HUD وشروح مسقطة من 3D / Instrument-panel HUD & projected callouts (ready)
- `UI-70` مربع تتبع وماسح ضوئي / AI tracking box & scanner brackets (seen)
- `UI-72` تسجيل صفحة بخطوات مبرمجة / Scripted page recording (Playwright) (ready)
- `UI-73` التقاط موقع إلى فيديو / Website capture → video (install)

### `UI-72` — تسجيل صفحة بخطوات مبرمجة / Scripted page recording (Playwright)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ملف خطوات JSON يقود صفحة حقيقية: انتظار، نقر بمؤشر منزلق، سحب، كتابة، تمرير، مع ترجمة لكل خطوة. / A JSON steps file drives a real page — wait, click with a gliding cursor, drag, type, wheel scroll, captions per step.

**متى:** حين تحتاج تسجيل صفحة ويب حقيقية بخطوات مبرمجة: نقر وسحب وكتابة وتمرير مع ترجمة لكل خطوة / when you need to record a real web page through scripted steps (click, drag, type, scroll) with per-step captions

**كيف:** Write your own Playwright script (Playwright + Chromium are installed here) mirroring the step grammar: wait, waitFor selector/text/js, click, tap, drag (hold), hover, held keys, type, wheel scroll over time, goto, caption → captions.vtt. Frames the page did not repaint are held and counted, never interpolated; warn under 20 fps. The atlas record-page.mjs is reference only (needs puppeteer-core; do not run unreviewed). Prep: native resolution, enlarged cursor, editor font ≥ 16 pt, notifications off, disposable data, lead-in and lead-out.

**المعاملات:** settle 1.5 s; glide 450 ms; type 70 ms/key; caption 3 s; step timeout 20 s; max 600 s; phone = 360×640 at 3×

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تسجيل شاشة · playwright · screen recording · steps · walkthrough · تصوير موقع · سكرين ريكورد · أتمتة المتصفح · browser automation · captions

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/1511-homie/3903-video/references/RECORD.md`
- `kosif-atlas/skills/1511-homie/3903-video/references/examples/site-walkthrough.json`
- `kosif-atlas/skills/1096-akbun-editvideo/2447-akbun-vlog-shootplan/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-70` مربع تتبع وماسح ضوئي / AI tracking box & scanner brackets (seen)
- `UI-71` مسرح أداة تصميم ومقابض تحديد / Design-tool canvas, selection handles & size tags (seen)
- `UI-73` التقاط موقع إلى فيديو / Website capture → video (install)
- `UI-74` فيلم إطلاق kmotion brag / kmotion brag launch film (ready)

### `UI-73` — التقاط موقع إلى فيديو / Website capture → video

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 |

**ما هي:** زحف متصفح بلا واجهة على رابط يخرج لقطات وألوان وخطوط ونصوص وأصول، ثم فيلم من مرئيات الموقع نفسه. / A headless crawl of a URL yields screenshots, brand tokens (colours, fonts), text and assets; the film is built from the site's own visuals.

**متى:** حين يعطي المستخدم رابط موقع ويريد فيديو إطلاق مبنيًا من لقطات الموقع نفسه وألوانه وخطوطه / when the user gives a website URL and wants a launch video built from the site's own screenshots, colours and fonts

**كيف:** npx hyperframes capture https://site -o ./capture --json [--skip-vision] [--max-screenshots 12] [--timeout 60000]; gate on ok:true and no capture/BLOCKED.md — a failed capture is a hard stop, never invent a page. Then capture → design → script → storyboard → voice → build → validate (product-launch-video skill, 30–90 s sweet spot, up to ~3 min). Tone mixes: high impact = per-word type + velocity cuts + counters; premium = variable font + Lottie + slow cuts. Vision captions need an external service.

**المعاملات:** sweet spot 30–90 s

**التثبيت:** npx hyperframes capture <url> -o ./capture --json

**الوسوم:** التقاط موقع · website to video · capture · launch video · hyperframes · فيديو من رابط · رابط موقع · هوية الموقع · url to video · site screenshots

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `npm:lottie` ← npm ls lottie أو وجود node_modules/lottie
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/packages/cli/src/commands/capture.ts`
- `kosif-one/vendor/hyperframes/skills/product-launch-video/SKILL.md`
- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-71` مسرح أداة تصميم ومقابض تحديد / Design-tool canvas, selection handles & size tags (seen)
- `UI-72` تسجيل صفحة بخطوات مبرمجة / Scripted page recording (Playwright) (ready)
- `UI-74` فيلم إطلاق kmotion brag / kmotion brag launch film (ready)
- `UI-75` وصفة فيديو ميزة حقيقية / Real-feature video recipe (documented)

### `UI-74` — فيلم إطلاق kmotion brag / kmotion brag launch film

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** من مجلد أو رابط إلى خطة ثم بناء ثم تسليم لفيلم إطلاق موقع أو تطبيق. / From a folder or URL to plan → build → deliver for a site/app launch film.

**متى:** عند إنتاج فيلم إطلاق لموقع أو تطبيق من مجلد أو رابط بقصة: خطاف ثم مشكلة ثم كشف وميزات ودعوة / when producing a site or app launch film from a folder or URL with a hook, pain, reveal, features and CTA story

**كيف:** kmotion brag init DIR\|URL → plan → build → deliver (scripts/launch.py, covered by tests/test_launch.py). Basma studio alternative: AGENT.TOOLS.launch_film {product, pitch, duration} writes hook → pain → reveal → 3 features → CTA and cuts uploaded recordings on the beat under big kinetic titles (needs the app's AI service).

**المعاملات:** story: hook · pain · reveal · 3 features · CTA

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إطلاق · launch film · brag · product launch · فيديو إطلاق · تطبيق جديد · برومو · kmotion · launch video

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `100-superskills/skills/kosif-montage-motion/scripts/launch.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_launch.py`
- `app/public/js/10_studio.js:4306`

#### 7. قدرات قريبة في العائلة

- `UI-72` تسجيل صفحة بخطوات مبرمجة / Scripted page recording (Playwright) (ready)
- `UI-73` التقاط موقع إلى فيديو / Website capture → video (install)
- `UI-75` وصفة فيديو ميزة حقيقية / Real-feature video recipe (documented)
- `UI-76` من فيجما إلى طبقات متحركة / Figma frame → animatable layers (key)

### `UI-75` — وصفة فيديو ميزة حقيقية / Real-feature video recipe

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** «المستخدم يفعل كذا، والمنتج يفعل كذا بوضوح» — التقط التطبيق الحقيقي لا موك أب. / 'The user does X; the product visibly does Y' — capture the real app, not a mockup.

**متى:** حين يريد المستخدم فيديو يعرض ميزة حقيقية من تطبيقه الفعلي لا موك أب، بعدة مقاسات للنشر / when the user wants a video of a real feature captured from the actual app, not a mockup, in several aspect ratios

**كيف:** Leave a little time before/after the action; cut waits only where it does not misrepresent the experience; one visual focus at a time; words only when the picture can't say it. Capture with Playwright recordVideo, edit/reframe with ffmpeg, overlays with render_html.cjs. Deliver 16:9, 4:5, 9:16 and 1:1.

**المعاملات:** formats 16:9 · 4:5 · 9:16 · 1:1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ميزة · feature video · real app · reframe · تصوير التطبيق · مقاسات متعددة · عمودي ومربع · aspect ratios · screen capture

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-73` التقاط موقع إلى فيديو / Website capture → video (install)
- `UI-74` فيلم إطلاق kmotion brag / kmotion brag launch film (ready)
- `UI-76` من فيجما إلى طبقات متحركة / Figma frame → animatable layers (key)
- `UI-77` تسجيل المتصفح بمؤشر ولوحة لقطات / Browser recording CLI with cursor & contact sheet (install)

### `UI-76` — من فيجما إلى طبقات متحركة / Figma frame → animatable layers

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اسحب بنية الإطار وألوانه وظلاله وخطوطه ومسافاته من فيجما وأعد بناءه HTML/CSS جاهزًا للتحريك. / Pull a frame's structure, fills, shadows, type, auto-layout spacing and variables from Figma and rebuild it as animatable HTML/CSS.

**متى:** عند تحويل إطار من فيجما إلى طبقات HTML/CSS قابلة للتحريك بألوانه وخطوطه ومسافاته / when converting a Figma frame into animatable HTML/CSS layers with its colours, type and spacing

**كيف:** File key after /design/ or /file/; node-id 123-456 == 123:456; auto-layout → flexbox; RGBA floats 0–1 → hex; REST /v1/images/:key?ids=…&format=png&scale=2. Needs a Figma token or the Figma MCP (external service).

**المعاملات:** PNG export scale 2; variables per light/dark

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فيجما · figma · handoff · design to code · تصميم إلى كود · تصدير التصميم · طبقات · html css · auto layout

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/1381-figma/3252-figma-implementing`
- `kosif-atlas/skills/1381-figma/3252-figma-implementing/references/figma-mcp-tools.md`

#### 7. قدرات قريبة في العائلة

- `UI-74` فيلم إطلاق kmotion brag / kmotion brag launch film (ready)
- `UI-75` وصفة فيديو ميزة حقيقية / Real-feature video recipe (documented)
- `UI-77` تسجيل المتصفح بمؤشر ولوحة لقطات / Browser recording CLI with cursor & contact sheet (install)
- `UI-78` فيديو تعليمي من ملف YAML / YAML-defined tutorial video (documented)

### `UI-77` — تسجيل المتصفح بمؤشر ولوحة لقطات / Browser recording CLI with cursor & contact sheet

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سجّل التبويب النشط إلى webm/mp4 بـ 1–60 إطارًا مع مؤشر متحرك ولوحة لقطات تلقائية. / Record the active tab to webm/mp4 at 1–60 fps with an animated pointer and an automatic contact sheet.

**متى:** حين تريد تسجيل تبويب المتصفح فيديو بمؤشر متحرك ولوحة لقطات، مع توفر أداة agent-browser / when you want to record a browser tab to video with an animated pointer and a contact sheet via agent-browser

**كيف:** agent-browser record start demo.webm --cursor --contact-sheet --fps 60 (needs the agent-browser install + ffmpeg). Default 30 fps; 60 for motion studies; 1–15 for long timelines. In this container prefer your own Playwright script (UI-72); desktop recorders (wf-recorder on Wayland, OBS, x11grab) are not usable headless here.

**المعاملات:** 30 fps default; 60 motion; 1–15 long

**التثبيت:** npm i -g agent-browser

**الوسوم:** تسجيل · agent-browser · browser recording · contact sheet · تسجيل الشاشة · تسجيل تبويب · لقطات مصغرة · screen recording · webm

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/1412-agent-browser/3350-agent-browser/references/video-recording.md`

#### 7. قدرات قريبة في العائلة

- `UI-75` وصفة فيديو ميزة حقيقية / Real-feature video recipe (documented)
- `UI-76` من فيجما إلى طبقات متحركة / Figma frame → animatable layers (key)
- `UI-78` فيديو تعليمي من ملف YAML / YAML-defined tutorial video (documented)
- `UI-79` رموز تصميم الواجهة وسلالمها / UI tokens & Refactoring-UI scales (documented)

### `UI-78` — فيديو تعليمي من ملف YAML / YAML-defined tutorial video

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صف الشرائح وخطوات الشاشة والتعليق في YAML ثم يُرندر مع صوت وترجمة. / Describe slides, screencast steps and narration in YAML, then render with TTS narration and subtitles.

**متى:** عند إنتاج فيديو تعليمي من ملف YAML يصف الشرائح وخطوات الشاشة والتعليق، مع صوت آلي وترجمة / when producing a tutorial video from a YAML file describing slides, screen steps and narration, with TTS and subtitles

**كيف:** docker compose run video-guide-creator validate\|generate guides/<slug>.yml (Edge TTS voices; edge-tts looks blocked from this container). Rule worth keeping: narration describes the action before it happens; brand presets hold colours, voice and logo.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تعليمي · yaml · tutorial · docker · شرح بالفيديو · تعليق صوتي · ترجمة · tts · subtitles

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `docker` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-76` من فيجما إلى طبقات متحركة / Figma frame → animatable layers (key)
- `UI-77` تسجيل المتصفح بمؤشر ولوحة لقطات / Browser recording CLI with cursor & contact sheet (install)
- `UI-79` رموز تصميم الواجهة وسلالمها / UI tokens & Refactoring-UI scales (documented)
- `UI-80` سطح زجاجي للواجهات / Glass surface stack (proven)

### `UI-79` — رموز تصميم الواجهة وسلالمها / UI tokens & Refactoring-UI scales

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة 8 بكسل، زوايا 8/16/24، خط عنوان + مقاسان، وأربعة مستويات ظل. / 8 px grid, radii 8/16/24, one headline + two UI sizes, four elevation tiers.

**متى:** حين تحتاج قيمًا ثابتة لتصميم الواجهة قبل البناء: شبكة المسافات والزوايا وسلم الخطوط ومستويات الظل / when you need fixed UI design values before building: spacing grid, radii, type scale and shadow tiers

**كيف:** Write them into STYLE.md first. Spacing 4, 8, 16, 24, 32, 48, 64; type 12–36 on a ~1.2 scale (hero 36 px lh 1.1, body 16 px lh 1.75); measure 45–75ch. Shadows: sm 0 1px 2px .05 · md 0 4px 6px .1 · lg 0 10px 15px .1 · xl 0 20px 25px .15; product tiers 0 2px 8px rgba(0,0,0,.12) → 0 24px 64px rgba(0,0,0,.35).

**المعاملات:** 8 px grid; radii 8/16/24; 4 shadow tiers

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رموز تصميم · tokens · spacing · shadows · type scale · مسافات · ظلال · أحجام الخطوط · design tokens · elevation

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/playbooks/product-ui.md:18`
- `kosif-atlas/skills/3438-ux-design/14122-refactoring-ui`

#### 7. قدرات قريبة في العائلة

- `UI-77` تسجيل المتصفح بمؤشر ولوحة لقطات / Browser recording CLI with cursor & contact sheet (install)
- `UI-78` فيديو تعليمي من ملف YAML / YAML-defined tutorial video (documented)
- `UI-80` سطح زجاجي للواجهات / Glass surface stack (proven)
- `UI-81` معمارية الثيمات: الشكل × الوضع × العلامة / Look × theme × brand token architecture (ready)

### `UI-80` — سطح زجاجي للواجهات / Glass surface stack

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوحة ضبابية بطبقات فوق خلفيات داكنة: ضبابية خلفية، تعبئة 5%، حد متدرج 1 بكسل، وظل محيطي كبير. / Layered frosted panels on dark scenes: backdrop blur, 5% fill, 1 px gradient border, large soft ambient shadow.

**متى:** حين يطلب المستخدم واجهة زجاجية ضبابية فوق خلفية داكنة ببطاقات شفافة وحد رفيع وظل ناعم / when the user wants frosted-glass UI panels over a dark background with translucent cards, a thin border and soft shadow

**كيف:** backdrop-filter blur(22–28px) saturate(150%) (40 px for modals); fill rgba(255,255,255,.05–.08); 1 px border gradient .12→.02 plus a 1 px inner highlight; box-shadow 0 24px 80px rgba(0,0,0,.25). Dark backgrounds only, max 3 cards, cards rise y 40→0 and unblur 12→0 with 80 ms stagger. Proven here: four glass cards on three parallax depths in the glass-luxury-logo film (13/13 checks). Needs Chromium's backdrop-filter. HyperFrames liquid-glass blocks need WebGPU/HTML-in-Canvas — unverified here.

**المعاملات:** blur 22–28 px (40 modals); fill 5–8%; shadow 0 24px 80px .25

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج · glassmorphism · backdrop blur · frosted · glass ui · زجاج ضبابي · شفافية · بطاقات زجاجية · translucent · blur panel

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md`
- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`
- `100-superskills/skills/trend-animation-styles/references/styles.md`
- `kosif-tool/styles/glass-ui/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-78` فيديو تعليمي من ملف YAML / YAML-defined tutorial video (documented)
- `UI-79` رموز تصميم الواجهة وسلالمها / UI tokens & Refactoring-UI scales (documented)
- `UI-81` معمارية الثيمات: الشكل × الوضع × العلامة / Look × theme × brand token architecture (ready)
- `UI-82` ستايل برومو المنتج / Product promo style (neon prompt + glass orb) (seen)

### `UI-81` — معمارية الثيمات: الشكل × الوضع × العلامة / Look × theme × brand token architecture

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مجموعة رموز واحدة تُعاد كسوتها بـ 14 شكلًا ووضعين وعلامات، مع استوديو للخط واللون والزوايا والتباين. / One token set re-skinned by 14 looks, light/dark and brand variants, plus a studio for font, accent, radius, scale and contrast.

**متى:** عند بناء نظام ثيمات واحد يتبدل بين أشكال ووضع فاتح وداكن وهويات علامات دون تثبيت الألوان / when building one token system that switches looks, light/dark modes and brand variants without hard-coded colours

**كيف:** html[data-look] × [data-theme] × [data-brand]; looks: kosif, cobalt, navygold, najd, heritage, executive, audit, midnight, notebook, aurora, vivid, oasis, graphite, onyx (+ night pairs, auto); radii sharp 4/6/8 or round 12/16/22; --sk-zoom; data-contrast; screens never hard-code colour. KPI tile: white on mist, soft shadow, 4 px tone edge on the reading side, radius 18 px.

**المعاملات:** 14 looks; radii 4/6/8 or 12/16/22

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثيم · هوية · tokens · themes · dark mode · brand · ألوان العلامة · سمات · تخصيص الواجهة · theming · light dark

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-earth-ci-fork/ui/layouts/shell.js:29`
- `kosif-earth-ci-fork/ui/ds/tokens.css`
- `kosif-earth-ci-fork/ui/ds/surfaces.css`

#### 7. قدرات قريبة في العائلة

- `UI-79` رموز تصميم الواجهة وسلالمها / UI tokens & Refactoring-UI scales (documented)
- `UI-80` سطح زجاجي للواجهات / Glass surface stack (proven)
- `UI-82` ستايل برومو المنتج / Product promo style (neon prompt + glass orb) (seen)
- `UI-83` واجهة ملصقات بظل صلب / Sticker UI with hard offset shadow (seen)

### `UI-82` — ستايل برومو المنتج / Product promo style (neon prompt + glass orb)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تايبوغرافي حركي لإطلاق منتج مع صندوق طلب نيون وكرة زجاجية وتقلب فاتح/داكن. / Launch-promo kinetic type with a neon prompt box, a glass orb and light/dark flips.

**متى:** حين يطلب المستخدم برومو إطلاق منتج بتايبوغرافي حركي وصندوق طلب نيون وكرة زجاجية وتقلب فاتح/داكن / when the user wants a product-launch promo with kinetic type, a neon prompt box, a glass orb and light/dark flips

**كيف:** 16:9, 2.2 words/s, Readex Pro; bg #05050A, light #F8F7FF, ink #F5F3FF, grey #8B88A6, violet #A88BFF/#6C3BFF, blue #2F5BFF, pink #D946EF, orange #FF6A1A. Modes cycle big → prompt → orb → capsule → end; typing + click SFX on prompt lines, impact on the end card. Typewriter with a 3 px purple caret at ~18 chars/s while the parent scales 2.5→1 from the first character (camera pull-back synced to typing).

**المعاملات:** 2.2 wps; ~18 cps; pull-back 2.5→1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** برومو · إطلاق · product promo · neon prompt · readex pro · إعلان منتج · نص متحرك · نيون · kinetic typography · launch promo

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `app/public/js/10_studio.js:794`
- `style:product`

#### 7. قدرات قريبة في العائلة

- `UI-80` سطح زجاجي للواجهات / Glass surface stack (proven)
- `UI-81` معمارية الثيمات: الشكل × الوضع × العلامة / Look × theme × brand token architecture (ready)
- `UI-83` واجهة ملصقات بظل صلب / Sticker UI with hard offset shadow (seen)
- `UI-84` مكتبة مكوّنات HyperFrames للواجهات / HyperFrames UI component registry (install)

### `UI-83` — واجهة ملصقات بظل صلب / Sticker UI with hard offset shadow

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقات وأزرار بحد داكن سميك وزوايا كبيرة وظل صلب مزاح بلا ضبابية. / Cards, pills and buttons with a thick dark outline, big radii and a solid offset shadow with no blur.

**متى:** حين تريد واجهة بأسلوب الملصقات: حدود داكنة سميكة وزوايا كبيرة وظل صلب بلا ضبابية / when you want a sticker-style UI with thick dark outlines, big radii and a hard offset shadow with no blur

**كيف:** 4–6 px outline #2a1711, radius 24–40 px, same-hue shadow offset y 6 px; brutalist variant: 2 px black border, header strip, mono label.

**المعاملات:** outline 4–6 px; shadow offset 6 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ملصقات · sticker ui · neo brutalism · offset shadow · ظل صلب · حدود سميكة · بروتاليزم · brutalist · hard shadow

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `style:pm-thilina-a-891c09`
- `style:pm-polydao-7a572b`

#### 7. قدرات قريبة في العائلة

- `UI-81` معمارية الثيمات: الشكل × الوضع × العلامة / Look × theme × brand token architecture (ready)
- `UI-82` ستايل برومو المنتج / Product promo style (neon prompt + glass orb) (seen)
- `UI-84` مكتبة مكوّنات HyperFrames للواجهات / HyperFrames UI component registry (install)
- `UI-85` مخططات مشاهد الواجهة / UI scene blueprints (documented)

### `UI-84` — مكتبة مكوّنات HyperFrames للواجهات / HyperFrames UI component registry

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). |

**ما هي:** أكثر من 40 مكوّن واجهة جاهزًا (مؤشرات، إشعارات، أجهزة، محادثات، تبويبات…) تُركّب في أي مشهد. / 40+ ready UI components (cursors, notifications, devices, chats, tabs…) that mount into any scene.

**متى:** عند الحاجة لمكوّن واجهة جاهز (مؤشر أو إشعار أو جهاز أو محادثة أو تبويب) يُركّب في المشهد مباشرة / when you need a ready UI component (cursor, notification, device, chat, tabs) to mount straight into a scene

**كيف:** npx hyperframes add <name> copies compositions/components/<name>.html; mount on a class='clip' div with data-composition-src + data-start/data-duration/data-track-index; overrides as JSON in data-variable-values; colours come from 18 theme tokens (accent green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch. Preview npx hyperframes preview, render npx hyperframes render. The vendored copies are readable locally for study. Table below.

**التثبيت:** npx hyperframes add <component>

**الوسوم:** مكونات · hyperframes · registry · components · ui kit · مكتبة جاهزة · عناصر واجهة · قوالب · ready made · ui library

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/registry/components/agent-cursor/registry-item.json`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### 7. قدرات قريبة في العائلة

- `UI-82` ستايل برومو المنتج / Product promo style (neon prompt + glass orb) (seen)
- `UI-83` واجهة ملصقات بظل صلب / Sticker UI with hard offset shadow (seen)
- `UI-85` مخططات مشاهد الواجهة / UI scene blueprints (documented)
- `UI-86` أساليب KOSIF للواجهات / KOSIF UI styles to scaffold (ready)

### `UI-85` — مخططات مشاهد الواجهة / UI scene blueprints

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** وصفات متعددة المراحل لمشاهد الواجهة الشائعة، تُختار حسب الدور وتُذكر في الستوري بورد. / Multi-phase recipes for common UI scenes, picked by role and cited per beat in the storyboard.

**متى:** حين تخطط ستوري بورد لمشهد واجهة شائع وتريد وصفة مراحل جاهزة تختارها حسب دور المشهد / when storyboarding a common UI scene and you want a ready multi-phase recipe picked by the scene's role

**كيف:** Pick from blueprints-index.md by role: cursor-ui-demo (4.0–12.9 s), device-surface-showcase (5–11.3 s), prompt-type-submit-generate (5.2–12 s), agent-progress-theater (4.2–11.6 s), panel-edit-live-sync (5.3–11.9 s), transcript-scroll-artifact-reveal (5–11.8 s), zoom-out-workspace-reveal, cta-morph-press. 13 runnable 1920×1080 examples (hook-counter-burst 3.5 s … demo-page-scroll-spotlight 9 s) are the ground truth.

**المعاملات:** durations 3.5–12.9 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مخطط · blueprint · storyboard · ui scenes · وصفة مشهد · تخطيط المشهد · قوالب مشاهد · scene recipe · templates

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/cursor-ui-demo.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/device-surface-showcase.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/examples/hook-counter-burst.html`

#### 7. قدرات قريبة في العائلة

- `UI-83` واجهة ملصقات بظل صلب / Sticker UI with hard offset shadow (seen)
- `UI-84` مكتبة مكوّنات HyperFrames للواجهات / HyperFrames UI component registry (install)
- `UI-86` أساليب KOSIF للواجهات / KOSIF UI styles to scaffold (ready)
- `UI-87` مشغّل HTML مستقل بشريط تقديم / Standalone HTML player with seek & reduced motion (proven)

### `UI-86` — أساليب KOSIF للواجهات / KOSIF UI styles to scaffold

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة أساليب جاهزة للبناء: عرض SaaS، تفاعلات دقيقة، وواجهة زجاجية — مع كتيبي product-ui وphone. / Three ready styles — SaaS demo, UI micro-interactions, glass UI — backed by the product-ui and phone playbooks.

**متى:** عند بدء مشروع عرض SaaS أو تفاعلات واجهة دقيقة أو واجهة زجاجية وتريد أسلوبًا جاهزًا للبناء / when starting a SaaS demo, UI micro-interaction or glass UI project and you want a ready style to scaffold

**كيف:** python3 tools/kosif.py scaffold saas-demo <dir> (or ui-micro, glass-ui); python3 tools/kosif.py list --category product-ui (82 entries) / --category phone (8). saas-demo: cursor 380–700 ms cubic-bezier(.2,.8,.2,1), press 80/140 ms, 8 px grid. ui-micro: hover 120–160 ms, press 0.96, ripple 0→48 px in 320–400 ms, focus zoom ≤ 1.4× with a 2× render.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سكافولد · scaffold · saas demo · ui micro · glass ui · kosif styles · قالب جاهز · بدء مشروع · أسلوب جاهز · starter · template

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-86` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/styles/saas-demo/STYLE.json`
- `kosif-tool/styles/ui-micro/STYLE.json`
- `kosif-tool/styles/glass-ui/STYLE.json`
- `kosif-tool/playbooks/product-ui.md`
- `kosif-tool/playbooks/phone.md`

#### 7. قدرات قريبة في العائلة

- `UI-84` مكتبة مكوّنات HyperFrames للواجهات / HyperFrames UI component registry (install)
- `UI-85` مخططات مشاهد الواجهة / UI scene blueprints (documented)
- `UI-87` مشغّل HTML مستقل بشريط تقديم / Standalone HTML player with seek & reduced motion (proven)
- `UI-88` مراجعة على الإطار: سحب وتحجيم واختصارات / Frame review: drag, resize & Arabic-safe shortcuts (ready)

### `UI-87` — مشغّل HTML مستقل بشريط تقديم / Standalone HTML player with seek & reduced motion

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الفيلم يُسلَّم صفحة ويب offline بتشغيل/إيقاف وإعادة ومنزلق 0.01 ث ورابط تحميل MP4 واحترام الحركة المخفضة. / The film ships as an offline web page with play/pause, restart, a 0.01 s range slider, an MP4 download link and prefers-reduced-motion support.

**متى:** حين يجب تسليم الفيلم صفحة ويب تعمل بلا إنترنت بأزرار تشغيل وإيقاف وشريط تقديم ورابط تحميل / when the film must ship as an offline web page with play/pause, a seek slider and an MP4 download link

**كيف:** build.cjs templates an Arabic RTL page; rAF advances by min(dt, 0.1 s) and auto-stops at the end; window.render(t) clamps; window.setPlaying(bool); ?capture hides the chrome for rendering. Ran here: node player-test.cjs → PASS (initialisation, reduced motion, seek, deterministic frame, play/pause, restart, automatic stop, bounds).

**المعاملات:** theme #060d17/#08121c, focus ring #ffb769, accent #71e5d2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مشغل · player · html deliverable · reduced motion · seek · مشغل فيديو · صفحة ويب · بدون إنترنت · offline page · video player

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-87` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/build.cjs:6`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/player-test.cjs:1`

#### 7. قدرات قريبة في العائلة

- `UI-85` مخططات مشاهد الواجهة / UI scene blueprints (documented)
- `UI-86` أساليب KOSIF للواجهات / KOSIF UI styles to scaffold (ready)
- `UI-88` مراجعة على الإطار: سحب وتحجيم واختصارات / Frame review: drag, resize & Arabic-safe shortcuts (ready)
- `UI-89` قواعد صفحات الويب المسلَّمة / Web deliverable rules (landing, perf, hover gating) (documented)

### `UI-88` — مراجعة على الإطار: سحب وتحجيم واختصارات / Frame review: drag, resize & Arabic-safe shortcuts

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | MIT (Motion OS) |

**ما هي:** في وضع التحرير يُسحب العنصر ويُحجّم من زاويته وتُحفظ القيم كنسب من الإطار، والاختصارات تعمل بلوحة مفاتيح عربية. / In edit mode elements drag and corner-resize with values saved as % of frame; shortcuts work on an Arabic keyboard layout.

**متى:** عند مراجعة الفيلم وتعديل مواضع العناصر بالسحب والتحجيم، مع اختصارات تعمل على لوحة مفاتيح عربية / when reviewing a film and adjusting element placement by drag and resize, with shortcuts that work on an Arabic keyboard

**كيف:** Edits stored as '<id>.@box' = [x,y,w,h] in % (one decimal), 14 px corner grab radius, uniform scale ≥ 0.1. Keys bound to ev.code (KeyE, KeyN, BracketLeft/Right) so they survive the Arabic layout: Space play, ←/→ one frame, Shift+←/→ one second, [ ] scene, E edit, N note; speeds ½×/1×/2×; studio app keeps 60-step undo/redo.

**المعاملات:** box in % of frame; undo depth 60

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مراجعة · review · shortcuts · arabic keyboard · undo · تعديل المواضع · ملاحظات المراجعة · تراجع · drag resize · edit mode

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-88` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:600`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:954`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:159`

#### 7. قدرات قريبة في العائلة

- `UI-86` أساليب KOSIF للواجهات / KOSIF UI styles to scaffold (ready)
- `UI-87` مشغّل HTML مستقل بشريط تقديم / Standalone HTML player with seek & reduced motion (proven)
- `UI-89` قواعد صفحات الويب المسلَّمة / Web deliverable rules (landing, perf, hover gating) (documented)
- `UI-X01` المؤشر بطلًا / Cursor as protagonist (documented)

### `UI-89` — قواعد صفحات الويب المسلَّمة / Web deliverable rules (landing, perf, hover gating)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عندما يكون الناتج صفحة: أنماط هبوط، ميزانية أداء، والمرور فقط على مؤشر دقيق. / When the deliverable is a page: landing patterns, a performance budget, and hover only on fine pointers.

**متى:** حين يكون الناتج صفحة ويب أو صفحة هبوط وتحتاج ترتيب الأقسام وميزانية أداء وتقييد المرور / when the deliverable is a web or landing page needing section order, a performance budget and hover only on fine pointers

**كيف:** Hero (≤ 10-word outcome headline, one CTA, product in use) → social proof → 3–6 benefits → 3 steps → offer → FAQ → final CTA; container max 72rem; H1 clamp(28px,5vw,44px); breakpoints 360/768/1024/1280; 375 px without sideways scroll. Budget: LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms, JS ≤ 170 KB gz. @media (hover:hover) and (pointer:fine) for hover lifts; touch targets ≥ 44 px; respect prefers-reduced-motion.

**المعاملات:** LCP ≤ 2.5 s; CLS ≤ 0.1; INP ≤ 200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صفحة هبوط · landing page · performance · hover · web · سرعة الموقع · لاندنج بيج · تصميم متجاوب · responsive · page speed

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-89` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-one/tools/kosif-omni/skills/kosif-web-design/references/web-playbook.md`
- `100-superskills/skills/landing-page-premium/SKILL.md`
- `kosif-audit-pro/app/globals.css:223`

#### 7. قدرات قريبة في العائلة

- `UI-87` مشغّل HTML مستقل بشريط تقديم / Standalone HTML player with seek & reduced motion (proven)
- `UI-88` مراجعة على الإطار: سحب وتحجيم واختصارات / Frame review: drag, resize & Arabic-safe shortcuts (ready)
- `UI-X01` المؤشر بطلًا / Cursor as protagonist (documented)
- `UI-X02` تسليم المجسم وطبقات منفجرة / Mockup hand-off and exploded layers (documented)

### `UI-X01` — المؤشر بطلًا / Cursor as protagonist

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** في أفلام الواجهات المؤشر هو البطل: كبير، ينقر برأس السهم، لا يغطي ما ينقره، ويتغير الزر بعد النقرة بإطارين. — In UI films the cursor is the hero: large, clicks with the arrow tip, never covers what it clicks, and the button changes two frames after the click.

**متى:** عرض منتج أو تعليمي لواجهة — a product or tutorial demo of an interface.

**كيف:** Size 128–176 px at 1920 wide; hover 150–250 ms; press 1 → 0.96 → 1; state change 2 frames after the click; drag = lift + arc + target highlight + shrink into the slot; touch indicator 56–72 px. Headless browser recordings do not draw the pointer (seen here, QA-X02), so draw the cursor as its own layer.

**المعاملات:** 128–176 px; hover 150–250 ms; press 0.96; +2 frames to state change

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cursor · click · drag · ui demo · مؤشر · نقرة · سحب

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
- `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md`

#### 7. قدرات قريبة في العائلة

- `UI-88` مراجعة على الإطار: سحب وتحجيم واختصارات / Frame review: drag, resize & Arabic-safe shortcuts (ready)
- `UI-89` قواعد صفحات الويب المسلَّمة / Web deliverable rules (landing, perf, hover gating) (documented)
- `UI-X02` تسليم المجسم وطبقات منفجرة / Mockup hand-off and exploded layers (documented)
- `UI-X03` تسجيل عرض واجهة بـPlaywright / Playwright UI demo recording (WebM) (proven)

### `UI-X02` — تسليم المجسم وطبقات منفجرة / Mockup hand-off and exploded layers

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** انتقل من شاشة جهاز إلى الواجهة المسطحة بقلب القطبية (فاتح ↔ داكن)، وافصل طبقات الواجهة في العمق بمسافات متزايدة. — Move from a device screen to the flat UI with a polarity flip (light ↔ dark), and explode UI layers in depth with growing gaps.

**متى:** كشف بنية تطبيق أو الانتقال من الهاتف إلى الشاشة الكاملة — revealing an app's structure or going from phone to full screen.

**كيف:** Exploded layers at z = k·(70 + 150·i); stagger in-plane movement only, 0.03 s per layer; keep text layers frontal (counter-transform) so they stay readable.

**المعاملات:** z = k·(70 + 150 i); 0.03 s per layer

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mockup · exploded view · layers · phone · طبقات · مجسم · هاتف

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### 7. قدرات قريبة في العائلة

- `UI-89` قواعد صفحات الويب المسلَّمة / Web deliverable rules (landing, perf, hover gating) (documented)
- `UI-X01` المؤشر بطلًا / Cursor as protagonist (documented)
- `UI-X03` تسجيل عرض واجهة بـPlaywright / Playwright UI demo recording (WebM) (proven)
- `UI-X04` رموز الحركة وصقل الواجهة / Motion tokens and interface polish (React UIs) (install)

### `UI-X03` — تسجيل عرض واجهة بـPlaywright / Playwright UI demo recording (WebM)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT (ECC, (c) 2026 Affaan Mustafa); Playwright Apache-2.0 |

**ما هي:** سجّل تطبيق ويب حقيقي وهو يُستخدم إلى فيديو WebM عبر Playwright، ثم حوّله إلى MP4. — Record a real web app being used to a WebM video with Playwright, then convert to MP4.

**متى:** عرض سريع لواجهة حقيقية حين لا يلزم إطار دقيق بالزمن — a quick demo of a real interface when frame-exact timing is not needed.

**كيف:** newContext({recordVideo: {dir, size: {width: 1280, height: 720}}}); drive the page (mouse.move with steps, down/up, typing); close the context to flush the file; `ffmpeg -i demo.webm -c:v libx264 -pix_fmt yuv420p -r 30 demo.mp4`. Ran here (V9) with the preinstalled Node Playwright and its bundled Chromium: VP8 1280×720, 25 fps, 2.2 s. Limits: real-time capture (not seek(t), so not deterministic) and no pointer drawn — draw a cursor layer (UI-X01) or use the seek(t) capture pipeline for films.

**المعاملات:** 1280×720 VP8 25 fps; convert to H.264 30 fps

**التثبيت:** npm i -D playwright && npx playwright install chromium

**الوسوم:** playwright · screen recording · webm · ui demo · تسجيل الشاشة · عرض واجهة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-X03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md`
- `https://github.com/affaan-m/ECC/tree/main/skills/ui-demo/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-X01` المؤشر بطلًا / Cursor as protagonist (documented)
- `UI-X02` تسليم المجسم وطبقات منفجرة / Mockup hand-off and exploded layers (documented)
- `UI-X04` رموز الحركة وصقل الواجهة / Motion tokens and interface polish (React UIs) (install)

### `UI-X04` — رموز الحركة وصقل الواجهة / Motion tokens and interface polish (React UIs)

| الحقل | القيمة |
|---|---|
| العائلة | `ui-product-device` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ui-product-device.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `url` |
| الرخصة | MIT (ECC, (c) 2026 Affaan Mustafa); motion library MIT |

**ما هي:** لواجهات React: مدد من رموز ثابتة، ونوابض من خمسة إعدادات مسبقة، وتحريك transform وopacity فقط، واحترام تقليل الحركة؛ مع تفاصيل صقل تظهر في الفيديو. — For React UIs: durations from fixed tokens, springs from five presets, animate only transform and opacity, respect reduced motion; plus polish details that show on video.

**متى:** بناء واجهة تفاعلية أو صفحة هبوط ستُصوَّر — building an interactive UI or landing page that will be filmed.

**كيف:** Import from motion/react; durations from a motionTokens object (instant / fast / normal / slow / crawl); springs from five presets (snappy, gentle, bouncy, instant, release); `initial` equals the server-rendered state; reduced motion → opacity only; never animate width/height/top/left/margin/padding. Polish: enter = opacity + small translateY (+ blur), exit shorter (~150 ms); press scale 0.96; icon swap = crossfade with scale and blur; never `transition: all`; tabular-nums for counters and timers; text-wrap: balance on headings; concentric radii (outer = inner + padding); hit areas ≥ 40–44 px.

**المعاملات:** exit ~150 ms; press 0.96; hit area ≥ 44 px

**التثبيت:** npm i motion

**الوسوم:** motion tokens · react · framer motion · reduced motion · polish · رموز الحركة · واجهة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:animejs` ← npm ls animejs أو وجود node_modules/animejs
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:UI-X04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
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

- `https://github.com/affaan-m/ECC/tree/main/skills/motion-foundations/SKILL.md`
- `https://github.com/affaan-m/ECC/tree/main/skills/make-interfaces-feel-better/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `UI-X02` تسليم المجسم وطبقات منفجرة / Mockup hand-off and exploded layers (documented)
- `UI-X03` تسجيل عرض واجهة بـPlaywright / Playwright UI demo recording (WebM) (proven)

