# `story-direction-ideas` — الموشن والمونتاج والسينما (95 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/story-direction-ideas.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/motion.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`STORY-01` استقبال عربي بجولة واحدة](#story-01--استقبال-عربي-بجولة-واحدة--one-round-arabic-intake-with-defaults)
- [`STORY-02` موجّه الطلب الواحد (16 مسارًا)](#story-02--موجّه-الطلب-الواحد-16-مسارًا--one-request-router-16-routes--add-ons)
- [`STORY-03` مخطط اللقطات الحتمي ProPlan](#story-03--مخطط-اللقطات-الحتمي-proplan--deterministic-shot-planner-proplan)
- [`STORY-04` مولّد طلب Claude من الأسلوب](#story-04--مولّد-طلب-claude-من-الأسلوب--style--claude-request-generator)
- [`STORY-05` بوابة اختيار الأسلوب قبل التخطيط](#story-05--بوابة-اختيار-الأسلوب-قبل-التخطيط--style-choice-gate-35-directions-max-2-blended)
- [`STORY-06` جدول الرد قبل البناء](#story-06--جدول-الرد-قبل-البناء--talk-before-build-response-table)
- [`STORY-07` قائمة القوة الكاملة وفرصة الوسائط](#story-07--قائمة-القوة-الكاملة-وفرصة-الوسائط--full-power-checklist--media-opportunity-pass)
- [`STORY-08` STYLE.md وPLAN.md: المرصود والمفترض والجدول الموقوت](#story-08--stylemd-وplanmd-المرصود-والمفترض-والجدول-الموقوت--stylemd--planmd-observed-vs-assumed--timed-scene-table)
- [`STORY-09` عقد المشهد كبيانات](#story-09--عقد-المشهد-كبيانات--scene-contract-as-data-scene-cards)
- [`STORY-10` اللوحات قبل الرندر](#story-10--اللوحات-قبل-الرندر--boards-first-production-gate)
- [`STORY-11` جدول النبضات بعمود «المعلومة الجديدة»](#story-11--جدول-النبضات-بعمود-المعلومة-الجديدة--timed-beat-sheet-with-a-new-information-column)
- [`STORY-12` نوتة الحركة](#story-12--نوتة-الحركة--motion-score-table)
- [`STORY-13` حزمة المخرج السينمائي ومواصفة المشهد بسبع طبقات](#story-13--حزمة-المخرج-السينمائي-ومواصفة-المشهد-بسبع-طبقات--cinema-deliverable-package--7-layer-scene-spec)
- [`STORY-14` كتل القفل الحرفية للاستمرارية](#story-14--كتل-القفل-الحرفية-للاستمرارية--verbatim-lock-block-continuity)
- [`STORY-15` ذاكرة الذوق والوصفات](#story-15--ذاكرة-الذوق-والوصفات--taste-memory--recipe-freeze)
- [`STORY-16` قانون الثانية الأولى](#story-16--قانون-الثانية-الأولى--one-second-hook-law-013-s)
- [`STORY-17` مكتبة الخطافات المسماة](#story-17--مكتبة-الخطافات-المسماة--named-hook-library)
- [`STORY-18` خطاف الفلوج الصامت](#story-18--خطاف-الفلوج-الصامت--silent-vlog-hook-anatomy)
- [`STORY-19` الإطار الأول دليل لا تدرّج](#story-19--الإطار-الأول-دليل-لا-تدرّج--product-proof-first-frame)
- [`STORY-20` افتتاحيات مرصودة: سؤال، سطران متعاكسان، إشعارات الألم](#story-20--افتتاحيات-مرصودة-سؤال-سطران-متعاكسان-إشعارات-الألم--observed-openers-question-two-line-reversal-pain-notifications)
- [`STORY-21` محرك الصراع وstory_lint](#story-21--محرك-الصراع-وstory_lint--conflict-engine--story_lint-gmcs)
- [`STORY-22` منتقي الإطار السردي](#story-22--منتقي-الإطار-السردي--story-framework-chooser)
- [`STORY-23` قوس القطعة القصيرة](#story-23--قوس-القطعة-القصيرة--short-piece-arc-hook--development--pressure--lift--payoff--end)
- [`STORY-24` وصفة فيلم الخمس ثوانٍ](#story-24--وصفة-فيلم-الخمس-ثوانٍ--five-second-film-recipe)
- [`STORY-25` هيكل الإعلان ووصفة إعلان التطبيق 15 ث](#story-25--هيكل-الإعلان-ووصفة-إعلان-التطبيق-15-ث--ad-beat-skeleton--15-s-app-ad-recipe)
- [`STORY-26` أقواس العروض والإطلاق](#story-26--أقواس-العروض-والإطلاق--demo--launch-arcs-with-second-budgets)
- [`STORY-27` فيلم العلامة: من المشكلة إلى الكشف](#story-27--فيلم-العلامة-من-المشكلة-إلى-الكشف--brand-film-arc-problem--reveal-6-beats)
- [`STORY-28` هياكل الشرح](#story-28--هياكل-الشرح--explainer-structures)
- [`STORY-29` مقاييس أساليب المونتاج الطويل](#story-29--مقاييس-أساليب-المونتاج-الطويل--long-form-edit-style-metrics-essay--diary--reflection)
- [`STORY-30` هيكل يوتيوب الطويل والاحتفاظ](#story-30--هيكل-يوتيوب-الطويل-والاحتفاظ--long-form-youtube-skeleton--retention-holds)
- [`STORY-31` التريلر بالمازورات وقوس الطاقة](#story-31--التريلر-بالمازورات-وقوس-الطاقة--trailer-beat-sheet-in-bars--energy-arc)
- [`STORY-32` قوس قصة البيانات](#story-32--قوس-قصة-البيانات--data-story-arc--progressive-layering)
- [`STORY-33` أقواس العروض التقديمية كهياكل فيديو](#story-33--أقواس-العروض-التقديمية-كهياكل-فيديو--deck--pitch-arcs-as-video-skeletons)
- [`STORY-34` قصص الأطفال: كتاب مصور ويوم كامل](#story-34--قصص-الأطفال-كتاب-مصور-ويوم-كامل--kids-stories-picture-book--day-to-night-arc)
- [`STORY-35` منهج المخرج: أطروحة ونقش ونوتة](#story-35--منهج-المخرج-أطروحة-ونقش-ونوتة--motion-director-method-thesis-motif-score)
- [`STORY-36` جرأة في مكان واحد](#story-36--جرأة-في-مكان-واحد--spend-boldness-in-one-place)
- [`STORY-37` قائمة «المظهر المولَّد» الممنوعة](#story-37--قائمة-المظهر-المولَّد-الممنوعة--generated-look-blacklist-anti-slop)
- [`STORY-38` شخصية حركة واحدة لكل فيلم](#story-38--شخصية-حركة-واحدة-لكل-فيلم--one-motion-personality-per-film)
- [`STORY-39` من الشعور إلى الأرقام](#story-39--من-الشعور-إلى-الأرقام--feeling--motion-vocabulary-map)
- [`STORY-40` الأساليب المسماة الثمانية](#story-40--الأساليب-المسماة-الثمانية--eight-named-visual-styles-swiss-pulse-)
- [`STORY-41` أنظمة جمالية جاهزة ولا تخلطها](#story-41--أنظمة-جمالية-جاهزة-ولا-تخلطها--aesthetic-systems--presets--never-mix)
- [`STORY-42` قواعد تصميم الحركة](#story-42--قواعد-تصميم-الحركة--choreography-rules-build--breathe--resolve-13-rules)
- [`STORY-43` إخراج النبضة بأفعال الطاقة](#story-43--إخراج-النبضة-بأفعال-الطاقة--beat-direction-with-energy-verbs)
- [`STORY-44` عدسات النقد قبل الرندر](#story-44--عدسات-النقد-قبل-الرندر--creative-review-lenses--aesthetics-council)
- [`STORY-45` التعلم من المرجع دون نسخه](#story-45--التعلم-من-المرجع-دون-نسخه--learn-from-references-without-cloning)
- [`STORY-46` قواعد الصدق في الوعود](#story-46--قواعد-الصدق-في-الوعود--honesty-rules-for-claims)
- [`STORY-47` الشيء المحمول عبر الفيلم](#story-47--الشيء-المحمول-عبر-الفيلم--travelling-device--hero-object-thread)
- [`STORY-48` كشف جملة الذروة](#story-48--كشف-جملة-الذروة--payoff-line-detection)
- [`STORY-49` من المعنى إلى الرمز](#story-49--من-المعنى-إلى-الرمز--concept-to-symbol-motifs)
- [`STORY-50` أنظمة الفصول المرقّمة](#story-50--أنظمة-الفصول-المرقّمة--chapter-label-systems)
- [`STORY-51` خواتيم الملخص](#story-51--خواتيم-الملخص--recap-endings-grid--collage--board--progress)
- [`STORY-52` الإطار المغلق والحلقة](#story-52--الإطار-المغلق-والحلقة--bookends--loop-endings)
- [`STORY-53` بطاقات الجملة والصمت](#story-53--بطاقات-الجملة-والصمت--statement-cards-caption-beats--silence)
- [`STORY-54` تبدّل المزاج: ظلام/نور، نهار/ليل](#story-54--تبدّل-المزاج-ظلامنور-نهارليل--mood-shifts-darklight-acts-daynight-interludes)
- [`STORY-55` نبضات كوميدية وعاطفية](#story-55--نبضات-كوميدية-وعاطفية--comic--emotional-beats)
- [`STORY-56` نبضات الحجة](#story-56--نبضات-الحجة--argument-beats-pain-triptych--the-fix-bar--cost-reframing--paper-form)
- [`STORY-57` جسر الوميض والسحب للخلف إلى ملصق](#story-57--جسر-الوميض-والسحب-للخلف-إلى-ملصق--flash-bridge--poster-pull-back-reveal)
- [`STORY-58` نبضات العالم والحالة](#story-58--نبضات-العالم-والحالة--world-beats-surreal-props-overload-one-take-beacon)
- [`STORY-59` مونتاج مُخرَج لمقطع كلام](#story-59--مونتاج-مُخرَج-لمقطع-كلام--directed-edit-of-a-talking-clip)
- [`STORY-60` قوس الريل التحفيزي (FINAL_EDIT)](#story-60--قوس-الريل-التحفيزي-final_edit--motivational-talking-reel-arc-final_edit)
- [`STORY-61` فيلم الإطلاق من الموقع أو الكود](#story-61--فيلم-الإطلاق-من-الموقع-أو-الكود--launch-video-from-a-site-or-codebase-brag)
- [`STORY-62` بنية ريل العرض 15 ث](#story-62--بنية-ريل-العرض-15-ث--showreel-beat-structure-120-bpm)
- [`STORY-63` فيلم المختبر SHAPE→RANK](#story-63--فيلم-المختبر-shaperank--product-lab-film-shape--joint--load--break--swap--rank)
- [`STORY-64` قصة بلا كلام: مرشد وقفزة](#story-64--قصة-بلا-كلام-مرشد-وقفزة--wordless-short-a-guide-and-a-leap)
- [`STORY-65` ستة أقواس لأنواع الستيكمان](#story-65--ستة-أقواس-لأنواع-الستيكمان--stickman-six-genre-arcs)
- [`STORY-66` قوس الحب بخمس نبضات وإطارين](#story-66--قوس-الحب-بخمس-نبضات-وإطارين--five-beat-love-arc-with-paired-frames)
- [`STORY-67` ملاءمة عدد المقاطع لخطوات الطبخ](#story-67--ملاءمة-عدد-المقاطع-لخطوات-الطبخ--clip-count-fitting-food-flow)
- [`STORY-68` مخرج الفيرال بخمس بوابات](#story-68--مخرج-الفيرال-بخمس-بوابات--viral-five-stage-gated-director)
- [`STORY-69` أفلام الدعاء والجمعة](#story-69--أفلام-الدعاء-والجمعة--dua--friday-reels)
- [`STORY-70` مونتاج الغربة بمعنى الأغنية](#story-70--مونتاج-الغربة-بمعنى-الأغنية--meaning-matched-song-montage-ghorba)
- [`STORY-71` مستقبل مصر 2120: خطاف وقاعدة تراث](#story-71--مستقبل-مصر-2120-خطاف-وقاعدة-تراث--egypt-2120-one-second-concept--heritage-rule)
- [`STORY-72` شرح «تعريفان للنجاح» على لوحات مولدة](#story-72--شرح-تعريفان-للنجاح-على-لوحات-مولدة--two-definitions-of-success-voice-explainer)
- [`STORY-73` أشكال فيديو صانع المحتوى](#story-73--أشكال-فيديو-صانع-المحتوى--creator-video-shapes--faceless-vo)
- [`STORY-74` قواعد مونتاج المدينة](#story-74--قواعد-مونتاج-المدينة--city-montage-shot-grammar)
- [`STORY-75` معرض قوالب الأفلام (52) وقوالب البداية](#story-75--معرض-قوالب-الأفلام-52-وقوالب-البداية--film-template-gallery-52--starter-briefs)
- [`STORY-76` لوحات المشهد المرسوم وموجّه الرسم](#story-76--لوحات-المشهد-المرسوم-وموجّه-الرسم--painted-scene-showcases--drawing-request-router)
- [`STORY-77` كتاب العالم والكائنات الأصلية](#story-77--كتاب-العالم-والكائنات-الأصلية--creature--world-bible-kit)
- [`STORY-78` توليد أفكار بعشوائية حقيقية](#story-78--توليد-أفكار-بعشوائية-حقيقية--lateral-ideation-with-real-randomness)
- [`STORY-79` استخراج القصص والنُّقَط من النص](#story-79--استخراج-القصص-والنُّقَط-من-النص--story-mine--transcript-nuggets)
- [`STORY-80` العناوين: التوتر الصادق وخمسة اختبارات](#story-80--العناوين-التوتر-الصادق-وخمسة-اختبارات--titles-honest-charge--five-tests)
- [`STORY-81` خريطة الدعوة للفعل](#story-81--خريطة-الدعوة-للفعل--cta-placement-map)
- [`STORY-82` الغلاف يبدأ من النفس لا من الصورة](#story-82--الغلاف-يبدأ-من-النفس-لا-من-الصورة--psychology-first-thumbnail-brainstorm)
- [`STORY-83` أعمدة المحتوى والتقويم](#story-83--أعمدة-المحتوى-والتقويم--content-pillars--publishing-calendar)
- [`STORY-84` موجة الموشن 2026: أنماط الطلب والميزانيات](#story-84--موجة-الموشن-2026-أنماط-الطلب-والميزانيات--motion-wave-prompt-patterns--effort-budgets)
- [`STORY-85` وكلاء الإبداع الفرعيون وقرارات Jev](#story-85--وكلاء-الإبداع-الفرعيون-وقرارات-jev--creative-sub-agents--jev-decisions)
- [`STORY-P01` عشرون وصفة أسلوب موشن بمحركاتها](#story-p01--عشرون-وصفة-أسلوب-موشن-بمحركاتها--20-motion-style-recipes-s01s20-with-engine-candidates)
- [`STORY-P02` الإحاطة السينمائية بثماني خانات](#story-p02--الإحاطة-السينمائية-بثماني-خانات--eight-slot-cinematic-brief-product----output)
- [`STORY-P03` قاموس تحويل وصف الهواة إلى أوامر حركة](#story-p03--قاموس-تحويل-وصف-الهواة-إلى-أوامر-حركة--amateur--pro-motion-lexicon-adjective--code-direction)
- [`STORY-U01` خط فيلم الأغنية الكرتوني](#story-u01--خط-فيلم-الأغنية-الكرتوني--cartoon-music-video-pipeline)
- [`STORY-X01` السيناريو أولًا وخريطة المحفزات](#story-x01--السيناريو-أولًا-وخريطة-المحفزات--scenario-first-beat-grid-shot-table-and-trigger-map)
- [`STORY-X02` ذوق العميل: من الرفض إلى قاعدة](#story-x02--ذوق-العميل-من-الرفض-إلى-قاعدة--client-taste-from-rejection-to-rule)
- [`STORY-X03` انضباط التكرار والنسخ](#story-x03--انضباط-التكرار-والنسخ--iteration-and-version-discipline)
- [`STORY-X04` تقديرات وقت واقعية](#story-x04--تقديرات-وقت-واقعية--realistic-time-estimates)
- [`STORY-X05` استعارات بصرية من فيلم الأغنية](#story-x05--استعارات-بصرية-من-فيلم-الأغنية--visual-metaphors-from-the-owners-song-film)
- [`STORY-X06` اعرض ثلاث معاينات بدل الأسئلة](#story-x06--اعرض-ثلاث-معاينات-بدل-الأسئلة--show-three-previews-instead-of-a-questionnaire)

## البطاقات / cards

### `STORY-01` — استقبال عربي بجولة واحدة / One-round Arabic intake with defaults

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسالة عربية واحدة قصيرة فيها الأسئلة الناقصة فقط، كل سؤال باقتراح افتراضي، ثم انتظار. / One short Arabic message with only the missing questions, each with a default, then wait.

**متى:** حين يصل طلب فيديو ناقص المعلومات وتحتاج سؤال المستخدم مرة واحدة مع اقتراحات افتراضية / when a video request is missing details and you need to ask once, offering defaults, before starting

**كيف:** Diff the request against what the user already gave (audio, references, timing, style); ask only from the seven: message/audience/script, production type, duration + platform, language/dialect (فصحى/مصري/سعودي/English), supplied assets, realism/rhythm/likes-dislikes, preview-vs-final. Unanswered non-blocking items take your stated default (9:16, 30 s). For novices offer only 2–3 decision surfaces (where it plays, how long, how it should feel) with 2–4 options each; for data/map jobs infer then ask 1–3 either/or questions. Interactive CLI: `npm run intake` writes project/brief.json (defaults kinetic, 9:16, 30 s, ar-EG). Never re-ask known facts; a BRIEF.md or STORYBOARD.md already in the project means resume, not interview.

**المعاملات:** 1 message · ≤7 questions · defaults offered

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** استقبال · أسئلة · بريف · intake · questions · defaults · brief · أسئلة توضيحية · متطلبات · لهجة · clarify · requirements

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
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `fastify-motion-bro/docs/QUESTIONS.md:1-10`
- `fastify-motion-bro/scripts/cli.mjs:9-19`
- `kosif-one/vendor/hyperframes/skills/hyperframes/references/pitch-round.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-02` موجّه الطلب الواحد (16 مسارًا) / One-request router (16 routes + add-ons) (proven)
- `STORY-03` مخطط اللقطات الحتمي ProPlan / Deterministic shot planner (ProPlan) (proven)

### `STORY-02` — موجّه الطلب الواحد (16 مسارًا) / One-request router (16 routes + add-ons)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يطبّع الطلب العربي/الإنجليزي، يرتب المسارات بالكلمات، يلتقط الإضافات (ترجمة، صوت، موسيقى، 9:16، غلاف، خصوصية…) ويدمج حتى 4 مسارات في خط إنتاج واحد. / Normalises an Arabic/English request, ranks 16 routes by keyword evidence, detects add-ons and merges up to 4 routes into one pipeline.

**متى:** حين يكتب المستخدم طلبًا عامًا بالعربية أو الإنجليزية وتريد تحديد المسار المناسب وإضافاته كالترجمة والموسيقى / when a free-form Arabic or English request must be routed to the right production pipeline with its add-ons

**كيف:** `python3 plan.py --json "عايز ريل من فيديو كلام مع ترجمة وموسيقى"` → main_route talking_reel (ran here). Routes: reel_from_web, edit_my_footage, talking_reel, motion_2d, cinematic_3d, launch_video, sound_to_film, song_reel, mimic_reel, analyze_reference, ai_video_prompts, image_graphics, pixel_redraw … ; `--combine MAIN A B` runs shared steps once with one ratio/palette/font set; Jev keeps an extra route at p_yes ≥ 0.6, 0.4–0.6 only with a stated reason, < 0.4 dropped; explicit user words always win. Basma has the no-AI equivalent (KIT.guess regex votes: تقني→plotter, قصة→doodle, درس→whiteboard, رياض→chalkboard) and a local content classifier (music: silence < 6% + beat conf ≥ 1.35; screen: ≥ 55% still frames; edited: ≥ 2.5 cuts/10 s). Fastify asks which of nine profile modes to run and loads only that skill.

**المعاملات:** max 4 routes · p_yes 0.6/0.4 · ~0.1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** موجه · توجيه · router · routes · add-ons · intent · classifier · تصنيف الطلب · مسار الإنتاج · ريل · ترجمة · pipeline · request routing

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-one/scripts/plan.py:37`
- `kosif-one/tools/kosif-one/scripts/plan.py:39`
- `app/public/js/10_studio.js:928`
- `fastify-motion-bro/docs/PROFILE_CATALOG.md:5-17`

#### 7. قدرات قريبة في العائلة

- `STORY-01` استقبال عربي بجولة واحدة / One-round Arabic intake with defaults (ready)
- `STORY-03` مخطط اللقطات الحتمي ProPlan / Deterministic shot planner (ProPlan) (proven)
- `STORY-04` مولّد طلب Claude من الأسلوب / Style → Claude request generator (proven)

### `STORY-03` — مخطط اللقطات الحتمي ProPlan / Deterministic shot planner (ProPlan)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جملة المهمة ← خطة قراءة فقط: النية، الأوامر، القيود، و5 نبضات بإطارات دقيقة وحركة كاميرا لكل لقطة ونية صوت. / A task sentence becomes a read-only plan: intent, commands, limits and a 5-beat frame-exact storyboard with a camera move per shot.

**متى:** عند تحويل جملة مهمة إلى ستوريبورد بخمس نبضات بإطارات دقيقة وحركة كاميرا لكل لقطة قبل التنفيذ / when turning a one-line task into a frame-exact 5-beat storyboard with a camera move per shot

**كيف:** `python3 scripts/kmotion.py proplan --task "…" --seconds 12 --fps 30 --aspect 9:16 --out plan.json` (also POST /api/plan, MCP motion_plan). Cuts at 0/.12/.36/.62/.84/1 of frames: hook, setup, contrast, payoff, end_card; 2D moves fast_reveal/slow_push/match_cut/focus_lift/still_hold; 3D dolly_in/orbit/side_track…; audio_intent "impact" on beats 1 and 4; text safe area 15–80% on 9:16, 8% inset otherwise; `--require-full-pro` exits 3 without verified receipts. Ran here: 11 s 3D → frames 0/40/119/205/277, intent 3d_motion, side_effects_performed false. Simpler 3-shot scaffold (ultra_animator): 30/40/30% wide dolly-in → medium orbit 45° → payoff.

**المعاملات:** seconds 2–600 · fps 24/25/30/50/60 · cuts 0/12/36/62/84/100%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خطة · لقطات · storyboard · shot plan · proplan · frames · beats · ستوريبورد · حركة كاميرا · تقطيع اللقطات · camera moves · beat plan

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/proplan.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_core.py:54`
- `kosif-studio/motion/proplan.py:84`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/ultra_animator.py:104`

#### 7. قدرات قريبة في العائلة

- `STORY-01` استقبال عربي بجولة واحدة / One-round Arabic intake with defaults (ready)
- `STORY-02` موجّه الطلب الواحد (16 مسارًا) / One-request router (16 routes + add-ons) (proven)
- `STORY-04` مولّد طلب Claude من الأسلوب / Style → Claude request generator (proven)
- `STORY-05` بوابة اختيار الأسلوب قبل التخطيط / Style-choice gate: 3–5 directions, max 2 blended (ready)

### `STORY-04` — مولّد طلب Claude من الأسلوب / Style → Claude request generator

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يملأ قالب طلب ثنائي اللغة من سجل الأسلوب: المستودع، الأسلوب، الكتيبات، المصدر، المقاس، المحرك، اللغة، الصوت. / Fills a bilingual request template from a style record and options.

**متى:** حين تريد صياغة طلب جاهز ثنائي اللغة من سجل أسلوب مع المقاس والمدة والمصدر والصوت / when you need a ready bilingual request built from a style record with aspect, duration, source and audio options

**كيف:** `python3 tools/kosif.py prompt <id> --lang ar --aspect 9:16 --fps 30 --duration 15 --source "audio voice.mp3"\|"video x.mp4"\|"text s.md"\|none --stack auto\|remotion\|canvas\|svg\|three --audio keep\|music\|sfx\|silent --content-lang ar\|en\|both` (ran here for whiteboard). Source phrases: audio = master clock, transcribe and sync; video = study cuts/motion/speech; text = script supplied; none = write original narration + timed plan. web/generator.js mirrors it (buildRequest, cliCommand). Basma buildMotionPrompt adds a second-by-second timeline, spring 0.42/16 rad/s or ease-out 0.25–0.5 s, exits 0.2–0.3 s, stagger 0.06–0.12 s.

**المعاملات:** 15 placeholders · 5-step workflow

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طلب · برومبت · request · prompt generator · handoff · style · صياغة الطلب · قالب طلب · تعليمات · prompt template · bilingual

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
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-tool/tools/kosif.py:425`
- `kosif-tool/templates/claude_request.ar.txt`
- `kosif-tool/web/generator.js`
- `kosif-tool/tests/test_generator.mjs`

#### 7. قدرات قريبة في العائلة

- `STORY-02` موجّه الطلب الواحد (16 مسارًا) / One-request router (16 routes + add-ons) (proven)
- `STORY-03` مخطط اللقطات الحتمي ProPlan / Deterministic shot planner (ProPlan) (proven)
- `STORY-05` بوابة اختيار الأسلوب قبل التخطيط / Style-choice gate: 3–5 directions, max 2 blended (ready)
- `STORY-06` جدول الرد قبل البناء / Talk-before-build response table (documented)

### `STORY-05` — بوابة اختيار الأسلوب قبل التخطيط / Style-choice gate: 3–5 directions, max 2 blended

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قبل أي ستوريبورد اعرض 3–5 اتجاهات مختلفة حقًا (صورة النتيجة، لماذا تناسب، الكلفة) وانتهِ بـ «أي أسلوب؟»؛ والمزج = أساس + لمسة واحدة بنطاق محدد. / Before any storyboard offer 3–5 genuinely different directions and end with "which style?"; blending = one base + one scoped accent.

**متى:** حين يكون الطلب مفتوحًا قبل الستوريبورد وتحتاج عرض 3–5 اتجاهات أسلوب ليختار المستخدم أو يمزج اثنين / when an open brief needs 3–5 distinct style directions offered before storyboarding, letting the user pick or blend two

**كيف:** Map the brief to the S01–S14 menu or the 288-style catalogue (`python3 tools/kosif.py search <words>`); mark one as recommended. For unformed asks sample five concepts with ≥2 from the unusual tail before recommending (pitch round); each pitch names the capability it rides. Record base=S02, accent=S03 (titles only); never blend more than two; a described look outside the menu is labelled CUSTOM. When the user cannot describe a look, show 2–4 quick variant stills/3 s loops and revise only from marked ones.

**المعاملات:** 3–5 options · 1 recommended · ≤2 blended

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** اتجاهات · خيارات · directions · style menu · pitch round · custom · اختيار الأسلوب · مزج الأساليب · ستايل · style choice · blend

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes/references/pitch-round.md`
- `kosif-atlas/skills/1995-hypotyposis/7163-sketch`
- `kosif-tool/STYLE_INDEX.md`

#### 7. قدرات قريبة في العائلة

- `STORY-03` مخطط اللقطات الحتمي ProPlan / Deterministic shot planner (ProPlan) (proven)
- `STORY-04` مولّد طلب Claude من الأسلوب / Style → Claude request generator (proven)
- `STORY-06` جدول الرد قبل البناء / Talk-before-build response table (documented)
- `STORY-07` قائمة القوة الكاملة وفرصة الوسائط / Full-power checklist & media-opportunity pass (documented)

### `STORY-06` — جدول الرد قبل البناء / Talk-before-build response table

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تغيير مسمّى = نفّذه؛ ملاحظة شعورية = اعثر على السبب القابل للقياس وغيّره واشرح؛ سؤال = أجب فقط؛ «ثبّت» = لا تغيّر شيئًا؛ فكرة = اقترح وأضف للخطة؛ موافقة = ابنِ. / Named change → do it; felt note → find the measurable cause; question → answer only; hold → change nothing; approval → build.

**متى:** عند تلقي ملاحظات المستخدم على مسودة: تعديل محدد أو إحساس عام أو سؤال أو تثبيت أو موافقة / when handling user feedback on a draft — a named change, a vague feeling, a question, a hold or an approval

**كيف:** Translate felt notes ("مش فخم كفاية") into numbers: durations, easing, contrast, type weight, hold length. The review page composes all unsent edits/notes into one prompt with sections Edits (apply exactly), Notes (timecode/scene/element), Links, Scenes, Do; motion requests go to notes because only Claude changes motion.

**المعاملات:** 7 response types

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مراجعة · ملاحظات · feedback · revision · review loop · تعديلات · رأي العميل · تحسين المسودة · notes · edits

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-studio/SKILL.md`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:883`

#### 7. قدرات قريبة في العائلة

- `STORY-04` مولّد طلب Claude من الأسلوب / Style → Claude request generator (proven)
- `STORY-05` بوابة اختيار الأسلوب قبل التخطيط / Style-choice gate: 3–5 directions, max 2 blended (ready)
- `STORY-07` قائمة القوة الكاملة وفرصة الوسائط / Full-power checklist & media-opportunity pass (documented)
- `STORY-08` STYLE.md وPLAN.md: المرصود والمفترض والجدول الموقوت / STYLE.md + PLAN.md: observed vs assumed + timed scene table (proven)

### `STORY-07` — قائمة القوة الكاملة وفرصة الوسائط / Full-power checklist & media-opportunity pass

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قبل البناء مُرّ على: المادة، الفهم، الصورة، الصوت، التشطيب، الأفكار — ومرة واحدة اعرض كل التحسينات الممكنة في طلب واحد. / Walk material, understanding, picture, sound, finish and ideas; make one consolidated media-upgrade ask.

**متى:** عند الاستعداد للبناء لمراجعة المادة والصورة والصوت والتشطيب، واقتراح كل تحسينات الوسائط في طلب واحد / when about to build and you want to sweep material, picture, sound and finish and offer all media upgrades in one ask

**كيف:** Checklist: 2–3 directions, hook ≤2 s, one carried device, payoff, deliberate end, poster, credits, post pack, deliver ≥1080p. Media pass (one grounded scan): script without voice → TTS; emoji icons → real icons; placeholder image → better image; silent cuts → transition SFX; >10 s without music → bed; user approves all/some/none.

**المعاملات:** ≥1080p · one consolidated ask

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قائمة فحص · checklist · full power · media pass · upgrade · مراجعة قبل البناء · تحسينات · موسيقى خلفية · مؤثرات صوتية · pre-build · sfx

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/tools/kosif-one/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/media-use/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-05` بوابة اختيار الأسلوب قبل التخطيط / Style-choice gate: 3–5 directions, max 2 blended (ready)
- `STORY-06` جدول الرد قبل البناء / Talk-before-build response table (documented)
- `STORY-08` STYLE.md وPLAN.md: المرصود والمفترض والجدول الموقوت / STYLE.md + PLAN.md: observed vs assumed + timed scene table (proven)
- `STORY-09` عقد المشهد كبيانات / Scene contract as data (scene cards) (documented)

### `STORY-08` — STYLE.md وPLAN.md: المرصود والمفترض والجدول الموقوت / STYLE.md + PLAN.md: observed vs assumed + timed scene table

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ورقة أسلوب تفصل ما رُصد (بدليل زمني) عما افتُرض، وجدول مشاهد بلا فجوات ينتهي بالضبط عند المدة. / A style sheet separating observed (timestamped) from assumed, and a gap-free scene table ending exactly at duration.

**متى:** عند بدء مشروع وتحتاج ورقة أسلوب تفصل المرصود عن المفترض وجدول مشاهد موقوتًا ينتهي عند المدة بالضبط / when starting a project and you need a style sheet (observed vs assumed) and a gap-free timed scene table

**كيف:** `python3 tools/kosif.py scaffold <id> <dir>` fills both. STYLE: tokens for colour, type, line weights, easing, camera, Arabic rules, do-nots. PLAN: start/end, action, camera, transition, audio cue, assets; one clear motion per scene; word-timing table; licence checklist. Timing defaults: entrances 250–600 ms, accents 120–300 ms, transitions 300–800 ms. Fastify `npm run plan` writes storyboard.json, STYLE.md and a PLAN.md checklist (the agent must then rewrite it creatively).

**المعاملات:** entrances 250–600 ms · accents 120–300 · transitions 300–800

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خطة · أسلوب · style sheet · plan · scene table · scaffold · جدول المشاهد · ورقة الأسلوب · توقيت المشاهد · timing · plan.md

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
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-tool/templates/STYLE.md`
- `kosif-tool/templates/PLAN.md`
- `kosif-tool/tests/test_templates.py`
- `fastify-motion-bro/scripts/planner.mjs:25-35`

#### 7. قدرات قريبة في العائلة

- `STORY-06` جدول الرد قبل البناء / Talk-before-build response table (documented)
- `STORY-07` قائمة القوة الكاملة وفرصة الوسائط / Full-power checklist & media-opportunity pass (documented)
- `STORY-09` عقد المشهد كبيانات / Scene contract as data (scene cards) (documented)
- `STORY-10` اللوحات قبل الرندر / Boards-first production gate (documented)

### `STORY-09` — عقد المشهد كبيانات / Scene contract as data (scene cards)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل مشهد سجل JSON: النص، الخلاصة، طبقات البيانات، الوسائط، الكاميرا، المدى الزمني أو كلمات words.json، فعل الحركة، وإطار ثابت للفحص. / Every scene is a JSON record: text, takeaway, layers, media, camera, time range or word ids, motion verb, static QA frame.

**متى:** حين تريد وصف كل مشهد كسجل JSON فيه النص والطبقات والكاميرا والتوقيت وفعل الحركة قبل التحريك / when every scene should be a structured JSON card with text, layers, camera, timing and a motion verb

**كيف:** Fields: id, viewer text/VO line, takeaway, dataLayers (visible/dimmed/highlighted), media, annotations, cameraOrTransform, triggerRange (s or word ids), motionVerb (reveal, compare, accumulate, transform, move, zoom, pan, highlight, play), reducedMotion/static key frame. Generated-scene cards add base image, camera (static/pan/dolly/orbital), on-screen text + safe position, caption, motion prompt; mark "SPECIFIED, NOT GENERATED" when no key exists. The renderer reads durations and text from the same JSON so storyboard and film never drift; brief.json per-beat fields (time, composition, camera, subjects, text, typography, icons_ui, lighting_texture, motion, transition_out, audio) follow the same idea.

**المعاملات:** 9 motion verbs

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عقد المشهد · بطاقة مشهد · scene contract · json · storyboard data · بطاقات المشاهد · تخطيط المشاهد · توقيت الكلمات · scene cards · words.json

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/story-patterns-and-scene-contracts.md`
- `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen/SKILL.md`
- `100-superskills/skills/kosif-montage-motion/references/video-breakdown.md`

#### 7. قدرات قريبة في العائلة

- `STORY-07` قائمة القوة الكاملة وفرصة الوسائط / Full-power checklist & media-opportunity pass (documented)
- `STORY-08` STYLE.md وPLAN.md: المرصود والمفترض والجدول الموقوت / STYLE.md + PLAN.md: observed vs assumed + timed scene table (proven)
- `STORY-10` اللوحات قبل الرندر / Boards-first production gate (documented)
- `STORY-11` جدول النبضات بعمود «المعلومة الجديدة» / Timed beat sheet with a “new information” column (documented)

### `STORY-10` — اللوحات قبل الرندر / Boards-first production gate

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا رندر قبل موافقة المستخدم على البريف ودليل الأسلوب واللوحة وأوراق الشخصيات ولوحات الستوريبورد. / No render until the user approves brief, style guide, palette, character sheets and storyboard panels.

**متى:** حين تحتاج موافقة المستخدم على البريف ودليل الأسلوب والألوان والشخصيات ولوحات الستوريبورد قبل أي رندر / when you need user sign-off on brief, style guide, palette, characters and storyboard before any render

**كيف:** brief.md → boards/(style-guide, palette.json {ink, paper, tones}, models, storyboard.json panels {shot, panel, t, png, action, camera}) → approval → shots.json {fps, size, shots[t0,t1]} (shot1 t0=0; each t1 = next t0) → render → review. An approval digest invalidates when boards change; scene modules expose renderFrame(t)/renderDrawing(k); audio muxed afterwards. Lighter version: DESIGN.md (style prompt, colour roles, type, motion rules, don’ts) + STORYBOARD.md beat table; storyboard.html cells drawn as static sketches at the key moment.

**المعاملات:** approval digest · contiguous shots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لوحات · موافقة · boards · approval · storyboard · animatic · اعتماد · لوحة ألوان · أوراق الشخصيات · pre-production · sign-off

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/2414-animation/9356-produce/SKILL.md`
- `kosif-one/projects/water-cycle-animation/DESIGN.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/storyboard-recipe.md`

#### 7. قدرات قريبة في العائلة

- `STORY-08` STYLE.md وPLAN.md: المرصود والمفترض والجدول الموقوت / STYLE.md + PLAN.md: observed vs assumed + timed scene table (proven)
- `STORY-09` عقد المشهد كبيانات / Scene contract as data (scene cards) (documented)
- `STORY-11` جدول النبضات بعمود «المعلومة الجديدة» / Timed beat sheet with a “new information” column (documented)
- `STORY-12` نوتة الحركة / Motion score table (documented)

### `STORY-11` — جدول النبضات بعمود «المعلومة الجديدة» / Timed beat sheet with a “new information” column

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الوقت \| الكلام بالضبط \| ما على الشاشة \| ما الجديد الذي عرفه المشاهد؛ النبضة التي لا تضيف شيئًا تُحذف. / Time \| exact words \| screen action \| new information; a beat that adds nothing is cut.

**متى:** عند كتابة النص قبل التحريك وتريد التأكد أن كل نبضة تضيف معلومة جديدة وإلا تُحذف / when scripting before animating and you want every beat to add new information, cutting the ones that don't

**كيف:** Write before animating; change framing or add evidence as soon as the image has made its point; proof before long explanation; one CTA that follows from what was shown. Convert rows to timeline cues (words.json timings when audio exists). Shot-list variant: # · time · shot type · lens · move · action · lighting · sound · text · transition; reels ≤ one shot per 2.5 s, hook ≤1.5 s. Pencil storyboard frames: grey sketch, thin red lines for camera axis, dashed frame rectangle.

**المعاملات:** 10 shot-list columns · ≤1 shot / 2.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جدول نبضات · beat sheet · shot list · new information · storyboard · سكريبت · قائمة لقطات · تقطيع · script · timed beats

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md`
- `100-superskills/skills/storyboard-shotlist/SKILL.md:23`
- `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard`

#### 7. قدرات قريبة في العائلة

- `STORY-09` عقد المشهد كبيانات / Scene contract as data (scene cards) (documented)
- `STORY-10` اللوحات قبل الرندر / Boards-first production gate (documented)
- `STORY-12` نوتة الحركة / Motion score table (documented)
- `STORY-13` حزمة المخرج السينمائي ومواصفة المشهد بسبع طبقات / Cinema deliverable package & 7-layer scene spec (documented)

### `STORY-12` — نوتة الحركة / Motion score table

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لكل نبضة: العنصر والغرض، البداية والنهاية، المدة والتأخير، المنحنى، المحفّز، البديل، وسلوك المقاطعة — قبل الكود. / Per beat: subject/purpose, start/end state, duration/delay, ease, trigger, fallback, interruption — before code.

**متى:** عند التخطيط لكود الحركة لتحديد بداية كل نبضة ونهايتها ومدتها ومنحناها ومحفّزها وبديلها / when planning animation code and you must specify each beat's states, duration, delay, easing, trigger and fallback

**كيف:** Stagger by semantic grouping; define reduced-motion and interruption. Example (Arabic finance "ledger finding its structure"): warm paper, charcoal Arabic type, restrained blue rules; the selected account’s rule grows inline-start in 280 ms decelerating; the detail panel follows +80 ms with a 12 px translate settling in 360 ms; reduced motion = instant update. Product example: "aperture discovers the object", 700 ms mask.

**المعاملات:** rule 280 ms · panel +80 ms / 12 px / 360 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نوتة حركة · motion score · easing · timing table · ledger · توقيت الحركة · منحنى الحركة · تتابع · reduced motion · animation spec

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/references/motion-director.md`
- `100-superskills/skills/kosif-montage-motion/references/motion-director.md`

#### 7. قدرات قريبة في العائلة

- `STORY-10` اللوحات قبل الرندر / Boards-first production gate (documented)
- `STORY-11` جدول النبضات بعمود «المعلومة الجديدة» / Timed beat sheet with a “new information” column (documented)
- `STORY-13` حزمة المخرج السينمائي ومواصفة المشهد بسبع طبقات / Cinema deliverable package & 7-layer scene spec (documented)
- `STORY-14` كتل القفل الحرفية للاستمرارية / Verbatim lock-block continuity (proven)

### `STORY-13` — حزمة المخرج السينمائي ومواصفة المشهد بسبع طبقات / Cinema deliverable package & 7-layer scene spec

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** العنوان والـ logline وخطة المنصة، أوراق مرجعية مقفلة، قائمة لقطات، أوامر لكل لقطة، خطة إضاءة وتدرج، قائمة استمرارية ومخاطر. / Title, logline, platform plan, locked reference sheets, shot list, per-shot prompts, lighting plan + grade, continuity checklist, risks.

**متى:** حين يطلب المستخدم فيلمًا سينمائيًا بلقطات متعددة ويحتاج حزمة كاملة من المرجعيات والأوامر وخطة الإضاءة / for a multi-shot cinematic film needing reference sheets, per-shot prompts, a lighting plan and continuity checks

**كيف:** Seven layers written before any prompt: identity, world, action & physics, camera & lens, lighting, materials & atmosphere, colour & story. Shot list # size angle lens motion duration purpose; lighting setup/ratio/Kelvin; English prompts, Arabic explanations; per-shot clips 5–10 s; edit plan cuts on 60/BPM. Continuity: fixed light direction per scene, fixed wardrobe/props, lens matches stated distance. Hand-off folder for another engine: PROMPT.md, START-HERE.md, ATTACH/ parts ≥1600 px, frames/, missing assets named not invented.

**المعاملات:** 7 layers · clips 5–10 s · parts ≥1600 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سينما · لقطات · cinema package · shot list · continuity · 7 layers · handoff · فيلم سينمائي · إضاءة · تدرج لوني · أوامر اللقطات · lighting plan · logline

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/SKILL.md`
- `100-superskills/skills/cinema-director-7layers/SKILL.md:12`
- `kosif-one/tools/kosif-omni/skills/kosif-video/SKILL.md`
- `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-11` جدول النبضات بعمود «المعلومة الجديدة» / Timed beat sheet with a “new information” column (documented)
- `STORY-12` نوتة الحركة / Motion score table (documented)
- `STORY-14` كتل القفل الحرفية للاستمرارية / Verbatim lock-block continuity (proven)
- `STORY-15` ذاكرة الذوق والوصفات / Taste memory & recipe freeze (install)

### `STORY-14` — كتل القفل الحرفية للاستمرارية / Verbatim lock-block continuity

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أوصاف الشخصية والخلفية والعالم والكاميرا والإضاءة والأسلوب تُجمَّد نصًا ثابتًا يُلصق كما هو في كل أمر، والكود يتأكد من وجودها. / Character, world, camera, light and style descriptions are frozen text pasted unchanged into every prompt; code asserts their presence.

**متى:** حين تحتاج ثبات الشخصية والخلفية والإضاءة عبر كل الأوامر بلصق وصف مجمّد في كل أمر / when character, world and lighting must stay identical across every prompt via frozen pasted descriptions

**كيف:** core.repeated(piece, prompts) / lockCheck(text, lock) + ensure() throw if a lock is missing; used by stickman, romance, fitness, vox, food and kinetic profiles. Proven by the Fastify production-profile tests here (10/10).

**المعاملات:** lock blocks per prompt

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قفل · استمرارية · lock block · continuity · character consistency · ثبات الشخصية · تطابق الشخصيات · وصف ثابت · consistency · prompt lock

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `fastify-motion-bro/scripts/profiles/core.mjs:6,12`
- `fastify-motion-bro/tests/production-profiles.test.mjs`
- `fastify-motion-bro/docs/PRODUCTION-GATES.md:5`

#### 7. قدرات قريبة في العائلة

- `STORY-12` نوتة الحركة / Motion score table (documented)
- `STORY-13` حزمة المخرج السينمائي ومواصفة المشهد بسبع طبقات / Cinema deliverable package & 7-layer scene spec (documented)
- `STORY-15` ذاكرة الذوق والوصفات / Taste memory & recipe freeze (install)
- `STORY-16` قانون الثانية الأولى / One-second hook law (0–1–3 s) (documented)

### `STORY-15` — ذاكرة الذوق والوصفات / Taste memory & recipe freeze

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تتذكر اختيارات المستخدم المتكررة (أنيميشن الترجمة، الإبراز، اللوك، الانتقال) وتجمّد التشغيل المعتمد كوصفة مسماة. / Remembers repeated choices and freezes an approved run as a named recipe.

**متى:** حين يكرر المستخدم نفس الاختيارات وتريد حفظها كافتراضيات أو تجميد تشغيل معتمد كوصفة مسماة / when the user keeps repeating choices and you want to remember them or freeze an approved run as a named recipe

**كيف:** Basma tasteKeep on export: a value counts when ≥2 times and ≥60% of the last 12 exports, appended to the brief as an Arabic line. HyperFrames media-use: `node scripts/recipe.mjs freeze --name <n>`, `recipe.mjs list`, `prefs.mjs get --json` promote preset/voice/caption identity to defaults.

**المعاملات:** last 12 exports · ≥60%

**التثبيت:** cd app && npm install

**الوسوم:** ذاكرة · تفضيلات · taste · preferences · recipe · series · حفظ الإعدادات · وصفة · افتراضيات · presets · saved settings

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `app/public/js/00_editor.js:2839`
- `kosif-one/vendor/hyperframes/skills/media-use/scripts/recipe.mjs`
- `kosif-one/vendor/hyperframes/skills/media-use/references/memory.md`

#### 7. قدرات قريبة في العائلة

- `STORY-13` حزمة المخرج السينمائي ومواصفة المشهد بسبع طبقات / Cinema deliverable package & 7-layer scene spec (documented)
- `STORY-14` كتل القفل الحرفية للاستمرارية / Verbatim lock-block continuity (proven)
- `STORY-16` قانون الثانية الأولى / One-second hook law (0–1–3 s) (documented)
- `STORY-17` مكتبة الخطافات المسماة / Named hook library (documented)

### `STORY-16` — قانون الثانية الأولى / One-second hook law (0–1–3 s)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الثانية الأولى تُفهم وحدها: فعل أو نتيجة، والصورة والكلام والعنوان يخدمون فكرة واحدة دون تكرار نفس الكلمات. / The first second stands alone: an action or result; picture, line and title support one idea without repeating words.

**متى:** حين تريد افتتاحًا يشد المشاهد من أول ثانية في ريل أو فيديو قصير دون البدء بالشعار / when the opening must grab viewers in the first second of a reel or short without starting on the logo

**كيف:** Something moves on frame 1 (motion within the first 3 frames: zoom-in, hand move, falling object, light shift); major change before 1.5 s; never open on the logo; hook text ≤4–5 words, bold, high contrast; develop 1–3 s, deliver after 3 s. Pattern interrupt ≤0.5 s for viral formats. Validate by watching the first second muted and with sound. Expectation cue: lock one timing/easing system — inconsistent timing reads as cobbled together.

**المعاملات:** hook 0–1 s (short) / 0–3 s (general) · ≤4–5 words

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خطاف · أول ثانية · hook · first frame · opener · muted · افتتاحية · شد الانتباه · ريلز · intro · pattern interrupt

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md`
- `kosif-tool/playbooks/ads.md:25`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md`
- `kosif-atlas/skills/1503-universal-design-principles/3791-expectation-effect-design-cues`

#### 7. قدرات قريبة في العائلة

- `STORY-14` كتل القفل الحرفية للاستمرارية / Verbatim lock-block continuity (proven)
- `STORY-15` ذاكرة الذوق والوصفات / Taste memory & recipe freeze (install)
- `STORY-17` مكتبة الخطافات المسماة / Named hook library (documented)
- `STORY-18` خطاف الفلوج الصامت / Silent-vlog hook anatomy (documented)

### `STORY-17` — مكتبة الخطافات المسماة / Named hook library

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أنماط افتتاح بشروط نجاحها: نتيجة أولًا، اختبار مرئي، مشكلة محددة، فعل مفاجئ، سؤال مباشر، رقم دقيق غريب، اعتراف، قبل/بعد، ادعاء مخالف، رقم صادم، استعارة حسية. / Named openers with conditions: result-first, visible test, specific problem, surprising action, direct question, odd-precision number, confession, before/after, contrarian, shocking stat, visceral metaphor.

**متى:** حين تحتاج عدة صيغ افتتاح مختلفة لنفس الفيديو للاختيار بينها: سؤال، رقم صادم، قبل/بعد، اعتراف / when you need several labelled opener variants — question, shocking stat, before/after, confession — to pick from

**كيف:** Generate 5–7 variants in different patterns (never five of one kind), label each, recommend one; use verbatim audience language. Viral-opener classifier: 11 shapes (flat contrarian one-liner, odd-precision number, build-in-public confession, quote reframe, mini-list, relatable cold open, listicle promise, story at the tension…). PR/launch extras: concept announcement, before/after teaser, stakes. Ship three distinct 3 s hooks per script as alternate first scenes of the same composition (props switch) for A/B without re-editing the body.

**المعاملات:** 5–7 variants · 3 hooks × 3 s · 11 formulas

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خطافات · hook patterns · opener · a/b hooks · curiosity gap · جملة افتتاحية · سؤال افتتاحي · قبل وبعد · viral opener · hook ideas

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/2964-pwdev-copy/12448-copy-hooks/SKILL.md`
- `kosif-atlas/skills/3035-x-skills/13065-x-hook-extractor/references/classification-rules.md`
- `kosif-one/vendor/hyperframes/skills/faceless-explainer/references/story-design.md`
- `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-15` ذاكرة الذوق والوصفات / Taste memory & recipe freeze (install)
- `STORY-16` قانون الثانية الأولى / One-second hook law (0–1–3 s) (documented)
- `STORY-18` خطاف الفلوج الصامت / Silent-vlog hook anatomy (documented)
- `STORY-19` الإطار الأول دليل لا تدرّج / Product-proof first frame (documented)

### `STORY-18` — خطاف الفلوج الصامت / Silent-vlog hook anatomy

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خطاف بلا كلام قبل فلوج جاهز: افتتاح بارد 5–7 ث، سياق 3–6، فضول 8–12، لقطة فريدة، تشويق — الكل ≤45 ث. / A speech-free hook before a finished vlog: cold open 5–7 s, context 3–6, curiosity 8–12, unique 5–8, teaser 3–5; ≤45 s.

**متى:** حين يكون لديك فلوج جاهز بلا كلام وتريد مقدمة تشويقية قصيرة قبله لا تتجاوز 45 ثانية / when a finished speech-free vlog needs a teaser intro hook of up to 45 s placed before it

**كيف:** First cut shows the thumbnail subject, title within the first second; cuts 1.5–4 s (no run of sub-1 s cuts in calm films); last intro cut matches motion/direction of the first main-body cut; hook scenes stay in the body; if no material creates curiosity, propose a cold open only rather than faking tension. Candidate types: result-first, contrast (ordinary vs peak, day vs night), interruption (cut before completion), list. Implement as a hook segment list prepended via ffmpeg concat or composition.

**المعاملات:** cold 5–7 · context 3–6 · curiosity 8–12 · total ≤45 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فلوج · افتتاح بارد · cold open · vlog hook · silent · مقدمة فلوج · تشويق · بدون كلام · teaser · vlog intro

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/references/hook-principles.md`

#### 7. قدرات قريبة في العائلة

- `STORY-16` قانون الثانية الأولى / One-second hook law (0–1–3 s) (documented)
- `STORY-17` مكتبة الخطافات المسماة / Named hook library (documented)
- `STORY-19` الإطار الأول دليل لا تدرّج / Product-proof first frame (documented)
- `STORY-20` افتتاحيات مرصودة: سؤال، سطران متعاكسان، إشعارات الألم / Observed openers: question, two-line reversal, pain notifications (seen)

### `STORY-19` — الإطار الأول دليل لا تدرّج / Product-proof first frame

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الافتتاح يُظهر المنتج أو الدليل أو الأطروحة، لا خلفية متدرجة عامة؛ ومشهد المنتج = مُدخل + فعل + نتيجة مرئية. / Open on the product, evidence or thesis, never a generic gradient; product scenes need input, action and a visible consequence.

**متى:** حين يبدأ فيديو منتج أو ديمو وتريد أن يظهر المنتج أو الدليل من الإطار الأول بدل خلفية متدرجة / when a product or demo video should open on the product or evidence from frame 0, not a generic gradient

**كيف:** Check frame 0 of every film against this rule; label fictional data and never invent metrics. Do-it-first demo: open on the compelling "after", then peel back only the layers the audience needs; map every beat to a pain and cut beats without one. Result-first social recipe (MG-066) lives in FMT.

**المعاملات:** frame 0 check

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أول إطار · دليل · proof · first frame · result first · demo · فيديو منتج · عرض المنتج · افتتاحية · product video · evidence

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director`
- `kosif-atlas/skills/2375-sales-engineering/9185-demo-design/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-17` مكتبة الخطافات المسماة / Named hook library (documented)
- `STORY-18` خطاف الفلوج الصامت / Silent-vlog hook anatomy (documented)
- `STORY-20` افتتاحيات مرصودة: سؤال، سطران متعاكسان، إشعارات الألم / Observed openers: question, two-line reversal, pain notifications (seen)
- `STORY-21` محرك الصراع وstory_lint / Conflict engine + story_lint (GMC+S) (proven)

### `STORY-20` — افتتاحيات مرصودة: سؤال، سطران متعاكسان، إشعارات الألم / Observed openers: question, two-line reversal, pain notifications

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سؤال من سطرين بكلمة ملونة ثم المنتج؛ سطر حقيقة عام ثم سطر بلون مميز يعكسه؛ ثلاث إشعارات مائلة تحكي الألم ثم تطير أيقونة المنتج للمنتصف. / Centred two-line question with one coloured word; neutral fact line then an accent line that reverses it; three tilted OS notifications voicing the pain, then the product icon flies in.

**متى:** حين تريد افتتاحية لإعلان منتج بسؤال بكلمة ملونة أو سطرين متعاكسين أو إشعارات تحكي ألم المستخدم / when opening a product promo with a coloured-word question, a two-line reversal or pain-point notifications

**كيف:** Question: hold ~2 s, accent green on the key word, then move into the product. Reversal: same size, line 2 enters ~1 s later in the accent colour only. Notifications: radius 18 px, shadow 0 12px 30px rgba(0,0,0,.08), tilt ±4°, stagger 300 ms. Ironic cold open: sterile white compliance UI held 2.3 s with a hovering cursor, then hard cut to loud visuals. Space-to-earth opener: starfield + planet with title, then cut to the world. One dot to thought swarm: lone dot + typewriter caption, ripple rings, word count doubling every 0.5 s.

**المعاملات:** hold 2 s · line 2 +1 s · stagger 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سؤال · إشعارات · question hook · reversal · notifications · cold open · افتتاحية · نقطة الألم · إعلان منتج · pain points · product intro

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-justincooperman-e7bbc4`
- `style:pm-kloss-xyz-b9b3f6`
- `style:pm-wozu-co-242285`
- `style:pm-spearwtf-3c1fd1`
- `style:pm-gizakdag-b8c59e`

#### 7. قدرات قريبة في العائلة

- `STORY-18` خطاف الفلوج الصامت / Silent-vlog hook anatomy (documented)
- `STORY-19` الإطار الأول دليل لا تدرّج / Product-proof first frame (documented)
- `STORY-21` محرك الصراع وstory_lint / Conflict engine + story_lint (GMC+S) (proven)
- `STORY-22` منتقي الإطار السردي / Story framework chooser (documented)

### `STORY-21` — محرك الصراع وstory_lint / Conflict engine + story_lint (GMC+S)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل نبضة لها هدف ودافع وصراع ورهان، والبطل يقرر، والرهان يتصاعد، والتأمل ≈20%، والذروة تحل الصراع الخارجي عبر الداخلي. / Every beat has goal, motivation, conflict and stakes; the hero chooses; stakes escalate; ~20% introspection; the climax resolves outer through inner conflict.

**متى:** حين تكتب قصة أو سيناريو وتريد فحص أن لكل نبضة هدفًا وصراعًا ورهانًا يتصاعد وذروة تحل الصراع / when writing a story and you want to check each beat for goal, conflict, rising stakes and a resolving climax

**كيف:** Pipe JSON to `python3 scripts/omni/story_lint.py` (exit 1 on issues): {central_conflict, protagonist, beats[{goal, motivation, conflict, stakes, stakes_level, choice, mode, level, stage}], climax{outer, inner}, plot}. central_conflict must be one of "character vs character\|society\|nature\|technology\|supernatural\|self". Ran here: a 3-beat Arabic sample scored 72 (flagged a non-canonical conflict label, choices that do not name the protagonist, missing inner-conflict beat). Escalation levers: uncertain outcome, withheld need, personal stakes, no-win choice, no safe haven, team shake-up, tighter clock; four levels (central, story, scene, inner); ~80% action / 20% reflection.

**المعاملات:** score = 100 − 12·issues − 4·warnings · ≥3 beats · introspection warn >30%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صراع · قصة · conflict · story lint · gmc · stakes · escalation · سيناريو · حبكة · فحص القصة · storytelling · plot

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:32`
- `kosif-one/tools/kosif-omni/skills/kosif-video/scripts/story_lint.py:32`
- `kosif-one/tools/kosif-omni/skills/kosif-video/references/story-conflict.md`

#### 7. قدرات قريبة في العائلة

- `STORY-19` الإطار الأول دليل لا تدرّج / Product-proof first frame (documented)
- `STORY-20` افتتاحيات مرصودة: سؤال، سطران متعاكسان، إشعارات الألم / Observed openers: question, two-line reversal, pain notifications (seen)
- `STORY-22` منتقي الإطار السردي / Story framework chooser (documented)
- `STORY-23` قوس القطعة القصيرة / Short-piece arc (hook → development → pressure → lift → payoff → end) (ready)

### `STORY-22` — منتقي الإطار السردي / Story framework chooser

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رحلة البطل المضغوطة، StoryBrand، PAS للإعلانات القصيرة، BAB للمزايا، ABT للشرح، قوس التحول، دراسة الحالة، وحبكات بوكر السبع. / Compressed hero’s journey, StoryBrand, PAS, BAB, ABT, transformation arc, case study and Booker’s seven plots.

**متى:** حين تحتار في بناء قصة الفيديو وتريد إطارًا مناسبًا للهدف: إعلان قصير، شرح، دراسة حالة، قصة علامة / when choosing a narrative structure by goal — short ad, explainer, case study, feature or brand story

**كيف:** Pick by job: recognition → transformation arc; clarity → ABT (And-But-Therefore); proof → case study; short ad → PAS; feature → Before-After-Bridge; brand story → hero’s journey in 8 stages (ordinary world, call, hesitation, mentor, threshold, trials, reward, return) with the viewer as hero and the product as mentor; never skip the trials. Booker plots: Overcoming the Monster (stages checked by story_lint), Rags to Riches, Quest, Voyage and Return, Comedy, Tragedy, Rebirth. Scene outcomes yes / no / yes-but / no-and — prefer complicating ones in the middle. Run a 3-second "who is the protagonist?" check.

**المعاملات:** hero 8 stages · StoryBrand 7 · plots 7

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إطار سردي · رحلة البطل · pas · abt · bab · storybrand · plots · بناء القصة · هيكل سردي · دراسة حالة · narrative structure · hero journey

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1503-universal-design-principles/3732-archetypes-storytelling-arcs/references/narrative-frameworks.md`
- `kosif-atlas/skills/1164-leaderize-storytelling-framework/2746-leaderize-storytelling-framework/instructions.md`
- `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:24`
- `kosif-atlas/skills/1213-story-skills/2883-scene-craft/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-20` افتتاحيات مرصودة: سؤال، سطران متعاكسان، إشعارات الألم / Observed openers: question, two-line reversal, pain notifications (seen)
- `STORY-21` محرك الصراع وstory_lint / Conflict engine + story_lint (GMC+S) (proven)
- `STORY-23` قوس القطعة القصيرة / Short-piece arc (hook → development → pressure → lift → payoff → end) (ready)
- `STORY-24` وصفة فيلم الخمس ثوانٍ / Five-second film recipe (ready)

### `STORY-23` — قوس القطعة القصيرة / Short-piece arc (hook → development → pressure → lift → payoff → end)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إطار أول مكوَّن ومتحرك، تطوير، ضغط، انفراج، دفعة، ونهاية مقصودة؛ 4–7 نبضات وشيء واحد محمول. / Frame 0 composed and moving, development, pressure, lift, payoff, deliberate end; 4–7 beats, one carried device.

**متى:** حين تبني فيديو قصيرًا أو ريل قصصيًا وتريد قوسًا من الخطاف إلى الضغط ثم الانفراج والدفعة ونهاية مقصودة / when structuring a short piece or story reel from hook through pressure and lift to payoff and a deliberate end

**كيف:** Choreography acts: anticipation 10–20%, action 30–50%, reaction 10–20%, resolution 20–30%; something new every 2–4 s. Reel story formula: conflict hook ≤2 s → one escalation → protagonist choice → payoff/CTA, product as the tool of the choice, 15–60 s, ~80% action. kosif-montage-motion lint warns on banned defaults.

**المعاملات:** 4–7 beats · new thing every 2–4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قوس · نبضات · arc · payoff · beats · short film · هيكل الريل · قصة قصيرة · تصاعد · reel structure · story arc

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`
- `kosif-one/tools/kosif-studio/motion/references/motion-craft.md`
- `kosif-one/tools/kosif-omni/skills/kosif-video/references/story-conflict.md`

#### 7. قدرات قريبة في العائلة

- `STORY-21` محرك الصراع وstory_lint / Conflict engine + story_lint (GMC+S) (proven)
- `STORY-22` منتقي الإطار السردي / Story framework chooser (documented)
- `STORY-24` وصفة فيلم الخمس ثوانٍ / Five-second film recipe (ready)
- `STORY-25` هيكل الإعلان ووصفة إعلان التطبيق 15 ث / Ad beat skeleton & 15 s app-ad recipe (ready)

### `STORY-24` — وصفة فيلم الخمس ثوانٍ / Five-second film recipe

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فكرة واحدة، ≤3 نبضات، حامل واحد مرسوم، حركة كاميرا واحدة، ≤8 كلمات، ثم قزحية تغمر إلى العلامة. / One idea, ≤3 beats, one drawn carrier, one camera move, ≤8 words, an iris flood to the brand.

**متى:** حين يطلب المستخدم فيديو قصيرًا جدًا من خمس ثوانٍ لفكرة واحدة ينتهي بكشف اسم العلامة / when the user wants a 5-second, one-idea film that ends by revealing the brand

**كيف:** Beat 1 0–1.2 s: ring draws in 0.9 s + halo + lines rise; beat 2 1.2–3.6 s: push 1→1.09 and slow ring rotation; beat 3 3.6–5 s: words leave, ring → iris, gold flood + flash, brand words reveal. 1080×1920 30 fps; reference project five_sec.

**المعاملات:** entrance 0–1.2 · hold 1.2–3.8 · payoff 3.8–5 s · ≤8 words

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** 5 ثوان · ستينغ · five second · sting · iris · brand · فيديو خمس ثوان · كشف الشعار · لوجو · brand reveal · 5s video

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:31`
- `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### 7. قدرات قريبة في العائلة

- `STORY-22` منتقي الإطار السردي / Story framework chooser (documented)
- `STORY-23` قوس القطعة القصيرة / Short-piece arc (hook → development → pressure → lift → payoff → end) (ready)
- `STORY-25` هيكل الإعلان ووصفة إعلان التطبيق 15 ث / Ad beat skeleton & 15 s app-ad recipe (ready)
- `STORY-26` أقواس العروض والإطلاق / Demo & launch arcs with second budgets (documented)

### `STORY-25` — هيكل الإعلان ووصفة إعلان التطبيق 15 ث / Ad beat skeleton & 15 s app-ad recipe

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خطاف، وعد، 2–4 مزايا، دليل، دعوة، شعار — ووصفة تطبيق من سبع نبضات بالإطار. / Hook, promise, 2–4 features, proof, CTA, logo — and a seven-beat app ad timed to frames.

**متى:** حين يطلب المستخدم إعلانًا قصيرًا لتطبيق أو منتج بخطاف ومزايا ودليل ودعوة للفعل وشعار / when building a short app or product ad with hook, promise, features, proof, CTA and logo timed to frames

**كيف:** Skeleton: hook 0–1.5 s, problem/promise 1.5–4 s, 2–4 features × 2–3 s, proof, CTA 2–3 s, logo 1–1.5 s. 15 s app ad at 30 fps: Sequences at 0/45/120/195/270/345/405 frames with durations 45/75/75/75/75/60/45 — hook ease-out quint, tap spring 14/160, chart 4–6.5 s, notification 6.5–9 s, rating 4.8 counting 9–11.5 s ease-out cubic, CTA 11.5–13.5 s. 30 s spot: 0–3 hook, 3–10 problem, 10–22 solution + proof, 22–30 CTA, VO ≤70 words. Store product: drops on a coloured plinth, turns 30°, three benefit tags pop, price lands. Observed 10 s: 0–1.6 title, 1.6–4.8 day 1, 4.8–7.4 day 2, 7.4–10 title + CTA, each beat holds 0.8 s. Locked shouty lines: hook, thesis, twist, proof, command, handle — ≤4 words each, one per 4 s.

**المعاملات:** frames 0/45/120/195/270/345/405 · VO ≤70 words

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إعلان · تطبيق · ad structure · app ad · cta · features · remotion · إعلان تطبيق · اعلان 15 ثانية · دعوة للفعل · promo · commercial

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-tool/playbooks/ads.md:36-70`
- `kosif-tool/playbooks/ads.md:15-19`
- `100-superskills/skills/ad-creative-30s/SKILL.md:23`
- `style:pm-gonzalomacagno-2de1a9`
- `style:pm-techhalla-7acbc2`

#### 7. قدرات قريبة في العائلة

- `STORY-23` قوس القطعة القصيرة / Short-piece arc (hook → development → pressure → lift → payoff → end) (ready)
- `STORY-24` وصفة فيلم الخمس ثوانٍ / Five-second film recipe (ready)
- `STORY-26` أقواس العروض والإطلاق / Demo & launch arcs with second budgets (documented)
- `STORY-27` فيلم العلامة: من المشكلة إلى الكشف / Brand film arc: problem → reveal (6 beats) (documented)

### `STORY-26` — أقواس العروض والإطلاق / Demo & launch arcs with second budgets

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلاسيكي 30–60 ث، مشكلة-حل 20–40 ث، تشويق 15 ث، وخمسة أقواس إطلاق (PAS، Future Pacing، Demo Loop…). / Classic 30–60 s, problem-solution 20–40 s, 15 s teaser, and five launch arcs.

**متى:** حين تحتاج تقسيمًا زمنيًا بالثواني لفيديو عرض منتج أو مشكلة وحل أو تشويق أو إطلاق / when you need per-second budgets for a product demo, problem-solution video, teaser or launch arc

**كيف:** Classic: hook 3, problem 5, magic moment 5, proof 15, social proof 4, invite 4 s. Problem-solution: before 6, after 6, how 10, CTA 4. Teaser: hook 2, demo 8, logo 3, tagline 2. Launch arcs: PAS (hook → pain → agitation → tease → product → proof → CTA), Future Pacing (imagine → name → remove pain → mechanism → outcome → CTA), Demo Loop (question → intro → demo 1 → demo 2 → trust → CTA)… Problem scenes chaotic/red, solution scenes spacious/green; vary durations (short hooks, long proof). Observed SaaS arc 6/6/7/6/5 s (why, tangled UI fragments, snap into real UI, outcomes, logo); problem → obvious fix (show its flaw) → real fix with chapter pills, 8–10 scenes of 5–6 s; promo from a codebase: hook question → logo → N features ×≈4.6 s → social proof → CTA.

**المعاملات:** classic 3/5/5/15/4/4 s · PS 6/6/10/4 · teaser 2/8/3/2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عرض منتج · إطلاق · demo · launch · saas · problem solution · teaser · فيديو إطلاق · تشويق · مشكلة وحل · product demo · pas

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/166-demo-video/535-demo-video/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/product-launch-video/references/story-design.md`
- `kosif-tool/styles/pm-aschapmann-131210/BRIEF.md`
- `style:pm-0xnfrith-5be616`
- `style:pm-ai-baymax-0ef9dd`

#### 7. قدرات قريبة في العائلة

- `STORY-24` وصفة فيلم الخمس ثوانٍ / Five-second film recipe (ready)
- `STORY-25` هيكل الإعلان ووصفة إعلان التطبيق 15 ث / Ad beat skeleton & 15 s app-ad recipe (ready)
- `STORY-27` فيلم العلامة: من المشكلة إلى الكشف / Brand film arc: problem → reveal (6 beats) (documented)
- `STORY-28` هياكل الشرح / Explainer structures (documented)

### `STORY-27` — فيلم العلامة: من المشكلة إلى الكشف / Brand film arc: problem → reveal (6 beats)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشكلة، تصعيد، منعطف، كشف، دليل، هبوط — ادعاء واحد لكل نبضة، واستعارة بصرية تحمل المشكلة، والمنتج الحقيقي هو الدليل. / Problem, escalation, turn, reveal, proof, landing — one claim per beat; a metaphor carries the problem; the real product is the proof.

**متى:** حين تصنع فيلم علامة تجارية ينتقل من عالم المشكلة إلى كشف المنتج كدليل عبر استعارة بصرية / for a brand film that moves from a problem world to the product reveal as proof, carried by a visual metaphor

**كيف:** Storyboard major frames and one motivated transition from "problem world" to "product world"; recurring limited shape set; never redraw the logo from memory; rough-cut for clarity before polish; must still read muted. Metaphor chapters (observed): frame the product as a scientific metaphor (fission → fusion), 2 chapters of 15–18 s, climax at ~60% of runtime; overload beats via HyperFrames overwhelm-surround / scroll-feed blocks (6–9 s).

**المعاملات:** 6 beats · 1 claim per beat · climax ≈60%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فيلم علامة · brand film · reveal · metaphor · problem world · فيلم العلامة التجارية · كشف المنتج · استعارة بصرية · product reveal · brand story

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/101-video-skills/212-brand-film/SKILL.md`
- `style:pm-ajith-io-4c248f`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/overwhelm-surround.md`

#### 7. قدرات قريبة في العائلة

- `STORY-25` هيكل الإعلان ووصفة إعلان التطبيق 15 ث / Ad beat skeleton & 15 s app-ad recipe (ready)
- `STORY-26` أقواس العروض والإطلاق / Demo & launch arcs with second budgets (documented)
- `STORY-28` هياكل الشرح / Explainer structures (documented)
- `STORY-29` مقاييس أساليب المونتاج الطويل / Long-form edit style metrics (essay · diary · reflection) (documented)

### `STORY-28` — هياكل الشرح / Explainer structures

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرح مفهوم (طبقة بعد طبقة)، كيف تُعمل (3–6 خطوات على مسرح واحد)، قائمة، قصة شارحة؛ وخمسة أسطر سردية للشرح القصير. / Concept, how-to (3–6 steps on one stage), listicle, story explainer; plus a five-line narration arc for short explainers.

**متى:** حين تكتب فيديو شرح: شرح مفهوم، طريقة عمل بخطوات، قائمة، أو شرح قصير بسرد من خمسة أسطر / when scripting an explainer — concept, step-by-step how-to, listicle, story or a five-line short narration

**كيف:** Five-line arc for 15–30 s: hook → misconception → hidden mechanism → example/contrast → memorable truth, second person, longest line ≤14 words, one sentence per 6 s scene (Fastify viral profile, tested). Essay explainer 5–7 min: hook 0:15 (question + personal line), why it matters 0:30, 3–5 principles × 0:35–0:45, my take 0:40, evidence 0:45, misconceptions 0:30, conclusion 0:20, next action 0:15. Observed: 12 chapters × 12 s (establishing move → headline → one visual proof → data panel, hard cuts); question → scan (suspense) → flash lock → big answer → data → restate (30 s: 4/9/6/6/5 s); calm silent 30 s: question → 3 numbered steps ≈8 s each → logo, works muted.

**المعاملات:** ≤14 words/line · 5 lines/30 s · 12×12 s chapters

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شرح · explainer · how-to · listicle · narration · faceless · فيديو تعليمي · شرح خطوات · تعليق صوتي · tutorial · essay video

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/vendor/hyperframes/skills/faceless-explainer/references/story-design.md`
- `fastify-motion-bro/skills/viral-editorial/SKILL.md:8`
- `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md`
- `style:pm-blueoctopusai-dd17bd`
- `style:pm-tankazunori0914-0fc886`
- `style:pm-majorbaguette-fb11d7`

#### 7. قدرات قريبة في العائلة

- `STORY-26` أقواس العروض والإطلاق / Demo & launch arcs with second budgets (documented)
- `STORY-27` فيلم العلامة: من المشكلة إلى الكشف / Brand film arc: problem → reveal (6 beats) (documented)
- `STORY-29` مقاييس أساليب المونتاج الطويل / Long-form edit style metrics (essay · diary · reflection) (documented)
- `STORY-30` هيكل يوتيوب الطويل والاحتفاظ / Long-form YouTube skeleton & retention holds (documented)

### `STORY-29` — مقاييس أساليب المونتاج الطويل / Long-form edit style metrics (essay · diary · reflection)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** متوسط طول اللقطة وعدد القطعات في الدقيقة الأولى وحد البقاء على نفس الشاشة لكل نوع. / Average shot length, first-minute cuts and max same-screen time per long-form style.

**متى:** عند مونتاج فيديو طويل بأسلوب مقال أو يوميات أو تأمل وتحتاج أرقام طول اللقطة وعدد القطعات / when editing long-form essay, diary or reflection videos and you need shot-length and cut-rate targets

**كيف:** Essay: ASL 3.3 s (2.5–4), 20 cuts in minute one, max same screen 8 s, cards 40% (principles 15, source docs 10, tables 10, logos 5), cuts only. Diary/project: ASL 8 s, 3 cuts in minute one, max 40 s, B-roll 30%, 12-frame dissolves only around timelapses, never hide what got stuck. Reflection: ASL 3.8 s, 15 cuts/min, voice 70% of runtime, 12–20 frame dissolves at beat changes, subtitles bottom-centre 8% margin, 5.5% glyph height, ~18 chars/line. Talking-head cadence: return to the face within 30–45 s of B-roll.

**المعاملات:** ASL 3.3 / 8 / 3.8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طول اللقطة · إيقاع المونتاج · asl · cut rate · essay · vlog · pacing · مونتاج طويل · سرعة القطع · يوميات · shot length · long form

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2462-davinciresolve-style-project/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2463-davinciresolve-style-reflection/SKILL.md`
- `kosif-atlas/skills/3067-youtube/13229-creator-visual-director`

#### 7. قدرات قريبة في العائلة

- `STORY-27` فيلم العلامة: من المشكلة إلى الكشف / Brand film arc: problem → reveal (6 beats) (documented)
- `STORY-28` هياكل الشرح / Explainer structures (documented)
- `STORY-30` هيكل يوتيوب الطويل والاحتفاظ / Long-form YouTube skeleton & retention holds (documented)
- `STORY-31` التريلر بالمازورات وقوس الطاقة / Trailer beat sheet in bars & energy arc (documented)

### `STORY-30` — هيكل يوتيوب الطويل والاحتفاظ / Long-form YouTube skeleton & retention holds

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خطاف 3 ث بلا لقطات مساندة، افتتاح بارد بوعد صريح، أقسام موسومة، وعلامات خطر انسحاب مع «إمساك» عند كل منها. / Hook in 3 s, cold open with an explicit promise, labelled segments, and 2–3 named drop points each with a hold.

**متى:** حين تكتب سكريبت فيديو يوتيوب طويل وتريد خطافًا وأقسامًا موسومة وإمساكًا عند نقاط انسحاب المشاهدين / when scripting a long YouTube video with a fast hook, labelled chapters and holds at viewer drop-off points

**كيف:** Spoken sentences tagged [CHAPTER: name ~m:s], [B-ROLL: …], [IMPROVISE: …] become timeline markers and motion-graphics cue lists. ~150 wpm (15 min ≈2250 words). Retention: hook 0–30 s, context 30–90 s, body = Problem → Solution → Example → Result per point, CTA in the final 60 s, chapters past 6–8 min, promise in 15 s and a re-hook every 2 min; drop points (setup stretch, mid sag, pre-CTA fade) get a re-hook, open loop or pattern interrupt (scene-style switch, camera jolt, kinetic stat card). Tutorial types: feature 15–30 min, update 10–20, use-case 15–30, reaching the first "wow" fast. Six-stage creator pipeline: research → script → SEO → visual brief → editor brief → thumbnail brief, missing inputs marked [MISSING: …].

**المعاملات:** ~150 wpm · 2–3 risk points · re-hook /2 min

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** يوتيوب · احتفاظ · retention · long form · script · chapters · tutorial · سكريبت يوتيوب · مدة المشاهدة · فصول الفيديو · drop-off · youtube

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/3067-youtube/13226-creator-script-agent/SKILL.md`
- `kosif-atlas/skills/192-marketing-skills/617-video-content-strategist/SKILL.md`
- `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`
- `kosif-atlas/skills/1817-youtube-strategy/4867-yt-outline/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-28` هياكل الشرح / Explainer structures (documented)
- `STORY-29` مقاييس أساليب المونتاج الطويل / Long-form edit style metrics (essay · diary · reflection) (documented)
- `STORY-31` التريلر بالمازورات وقوس الطاقة / Trailer beat sheet in bars & energy arc (documented)
- `STORY-32` قوس قصة البيانات / Data story arc & progressive layering (documented)

### `STORY-31` — التريلر بالمازورات وقوس الطاقة / Trailer beat sheet in bars & energy arc

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تريلر 35–45 ث مكتوب بالمازورات: افتتاح بارد 1–2، سْتينغ اختياري، هبوط 6–8 بلقطة لكل مازورة، جولة، ذروة، نهاية مع إمساك ≥1.5 ث. / A 35–45 s trailer written in bars: cold open 1–2, optional sting, drop 6–8 (one shot per bar), tour, climax, end holding ≥1.5 s.

**متى:** حين تصنع تريلر أو برومو من 35–45 ثانية على موسيقى وتريد توزيع اللقطات والكتابة على المازورات / when cutting a 35–45 s trailer to music and planning shots, captions and the climax bar by bar

**كيف:** Cold open = most striking moment already in motion, ending on a downbeat hit with flash/hit-stop, no logo first; captions 1–3 words, at most one per bar, nothing that must be read in under a beat; half-bar cuts in the last bars; timeline.json tiling the bar grid; render native 16:9 and 9:16. Energy arc (observed): quiet wides 0–8 s → build with day-night shift 8–20 → fast beat-cut climax 20–32 → silence → title card 32–38. Darkness beat: near-black frame (mean luminance <3%) with one warm ember for 2–3 s before the climax.

**المعاملات:** bars: cold 1–2 · drop 6–8 · tour 3–4 · climax 4–6 · end 2–3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تريلر · مازورة · trailer · bars · energy arc · climax · silence · برومو · إعلان تشويقي · إيقاع الموسيقى · music sync · promo

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/concept-and-music.md`
- `style:pm-theparuchh-6e08c3`
- `style:pm-kamstudiolabs-0b0824`

#### 7. قدرات قريبة في العائلة

- `STORY-29` مقاييس أساليب المونتاج الطويل / Long-form edit style metrics (essay · diary · reflection) (documented)
- `STORY-30` هيكل يوتيوب الطويل والاحتفاظ / Long-form YouTube skeleton & retention holds (documented)
- `STORY-32` قوس قصة البيانات / Data story arc & progressive layering (documented)
- `STORY-33` أقواس العروض التقديمية كهياكل فيديو / Deck & pitch arcs as video skeletons (documented)

### `STORY-32` — قوس قصة البيانات / Data story arc & progressive layering

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** افتح على الرقم المفاجئ، ضع خط الأساس، 2–3 أدلة، استبصار واحد، ثم التوصية — وكل نبضة تضيف طبقة واحدة. / Open on the surprising number, set the baseline, 2–3 evidence beats, one insight, end on the recommendation — one new layer per beat.

**متى:** حين تحوّل أرقامًا أو بيانات إلى فيديو يبدأ بالرقم المفاجئ ويضيف طبقة في كل نبضة حتى التوصية / when turning data into a video that opens on a surprising number and layers evidence toward a recommendation

**كيف:** Insight-first title: [number] + [impact] + [context] ("الصادرات +23% بعد الميناء الجديد"), subtitle carries unit, dates, source — if it cannot be written the scene is not ready. Same axes across beats; dim previous layers to 30–40%; before/after panels with identical row order, after values counting from before values, delta in accent only. Every chart must answer a question in the script; a beat that only adds drama is cut; pause any frame and the claim still reads.

**المعاملات:** 3 evidence beats · prior layers 30–40%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قصة بيانات · data story · insight title · layering · before after · قصة الأرقام · رسوم بيانية · عنوان الاستبصار · charts · data video

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/SKILL.md`
- `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/references/details.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-30` هيكل يوتيوب الطويل والاحتفاظ / Long-form YouTube skeleton & retention holds (documented)
- `STORY-31` التريلر بالمازورات وقوس الطاقة / Trailer beat sheet in bars & energy arc (documented)
- `STORY-33` أقواس العروض التقديمية كهياكل فيديو / Deck & pitch arcs as video skeletons (documented)
- `STORY-34` قصص الأطفال: كتاب مصور ويوم كامل / Kids stories: picture book & day-to-night arc (seen)

### `STORY-33` — أقواس العروض التقديمية كهياكل فيديو / Deck & pitch arcs as video skeletons

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مستثمر، مبيعات، مؤتمر، SCQA داخلي — بعناوين ادعاء لا عناوين موضوع. / Investor, sales, conference and internal SCQA arcs with claim headlines.

**متى:** حين تحوّل عرضًا تقديميًا للمستثمرين أو المبيعات أو مؤتمر إلى هيكل فيديو بعناوين ادعاء / when turning an investor, sales, conference or internal deck into a video skeleton with claim headlines

**كيف:** Investor: problem, solution, market, product, traction, model, competition, team, numbers, ask (10–12 slides → 60–90 s). Sales: problem, solution, proof, offer, next step. Conference: hook ~30 s, context, insight, evidence, takeaway. SCQA: situation, complication, question, answer. Landing frameworks PAS / AIDA / BAB with alternating proof modes (demonstration, metric, customer, mechanism). Lock the narrative before visuals.

**المعاملات:** 10–12 slides → 60–90 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عرض تقديمي · pitch · deck · investor · aida · scqa · عرض مستثمرين · بيتش · مبيعات · presentation · slides

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1567-tonone/4422-form-deck/SKILL.md`
- `100-superskills/skills/pitch-deck-investor/SKILL.md`
- `kosif-atlas/skills/198-product-skills/634-landing-page-generator`

#### 7. قدرات قريبة في العائلة

- `STORY-31` التريلر بالمازورات وقوس الطاقة / Trailer beat sheet in bars & energy arc (documented)
- `STORY-32` قوس قصة البيانات / Data story arc & progressive layering (documented)
- `STORY-34` قصص الأطفال: كتاب مصور ويوم كامل / Kids stories: picture book & day-to-night arc (seen)
- `STORY-35` منهج المخرج: أطروحة ونقش ونوتة / Motion-director method: thesis, motif, score (documented)

### `STORY-34` — قصص الأطفال: كتاب مصور ويوم كامل / Kids stories: picture book & day-to-night arc

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشكلة، ثلاث محاولات، حل، درس ضمني؛ أو فيلم ينظم كيوم من الصباح إلى ليل القرية المضيء. / Problem, three attempts, resolution, implicit lesson; or a film structured as one day from morning to a glowing night village.

**متى:** حين يطلب المستخدم قصة أطفال مصورة أو فيلمًا للأطفال يمتد من الصباح إلى ليل القرية / when making a children's picture-book story or a kids film structured as one day from morning to night

**كيف:** Picture book: 12–32 pages, ≤25 words per page, cliffhanger at the end of each right page. Day arc (observed, 60–80 s, ~6 acts): morning greeting → play → nature → sunset wash with a typewriter line → night village with lit windows and a goodnight line → finale gathering every character. Time-of-day icons (moon + Zzz → sun + coffee steam) signal passing time without text.

**المعاملات:** ≤25 words/page · 6 acts / 60–80 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أطفال · قصة · kids · picture book · bedtime · day night · حكاية أطفال · قصة قبل النوم · كتاب مصور · children · storybook

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/comics-picture-books/SKILL.md:21`
- `style:pm-abderrahmen-g-9e8ed0`
- `style:pm-nikolajankovic-ce4ff4`

#### 7. قدرات قريبة في العائلة

- `STORY-32` قوس قصة البيانات / Data story arc & progressive layering (documented)
- `STORY-33` أقواس العروض التقديمية كهياكل فيديو / Deck & pitch arcs as video skeletons (documented)
- `STORY-35` منهج المخرج: أطروحة ونقش ونوتة / Motion-director method: thesis, motif, score (documented)
- `STORY-36` جرأة في مكان واحد / Spend boldness in one place (documented)

### `STORY-35` — منهج المخرج: أطروحة ونقش ونوتة / Motion-director method: thesis, motif, score

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قِس حجم المهمة، اقترح 2–3 اتجاهات باستعارة وتكوين وسلوك توقيع ومقايضة، ثم التزم بأطروحة ونقش ومادة وحركة. / Size the job, propose 2–3 directions (metaphor, composition, signature behaviour, trade-off), then commit to thesis, motif, material and movement.

**متى:** عند بدء مشروع موشن وتحتاج اقتراح 2–3 اتجاهات ثم الالتزام بأطروحة ونقش ومادة وحركة / when starting a motion piece and you need 2–3 directions, then a commitment to one thesis, motif, material and movement

**كيف:** Strong still frame first, then animate to reveal relationships; choose the smallest capable engine; write the motion score (STORY motion score) before code; answer in the user’s language. Visual-argument test: remove the image — if nothing is lost it only decorates; write one sentence of what the viewer must understand in 2 s; define what repeats across a campaign vs what varies; avoid literal illustration (arrow up for growth).

**المعاملات:** 2–3 directions · 2 s comprehension

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أطروحة · نقش · thesis · motif · direction · concept · فكرة بصرية · اتجاه إبداعي · موشن جرافيك · art direction · visual idea

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/references/motion-director.md`
- `kosif-atlas/skills/2976-pwdev-social-media/12583-creative-concept/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-33` أقواس العروض التقديمية كهياكل فيديو / Deck & pitch arcs as video skeletons (documented)
- `STORY-34` قصص الأطفال: كتاب مصور ويوم كامل / Kids stories: picture book & day-to-night arc (seen)
- `STORY-36` جرأة في مكان واحد / Spend boldness in one place (documented)
- `STORY-37` قائمة «المظهر المولَّد» الممنوعة / Generated-look blacklist (anti-slop) (ready)

### `STORY-36` — جرأة في مكان واحد / Spend boldness in one place

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لحظة توقيع واحدة لكل فيلم (كشف منسّق أو تفاعل)، وكل ما حولها هادئ؛ التأثيرات المبعثرة تبدو قالبًا. / One signature moment per film; everything else quiet — scattered effects read as template.

**متى:** حين يبدو الفيلم مزدحمًا بالمؤثرات أو كقالب جاهز وتريد لحظة توقيع واحدة وكل ما حولها هادئ / when a film feels cluttered with effects or template-like and you want one signature moment with the rest quiet

**كيف:** Mark one "signature beat" in the storyboard; other beats use utility motion. Brand-moment flags in creator videos: return with the find, reveal of what was built, verdict — hold on the face, colour push, longer hold or sting.

**المعاملات:** 1 signature / film · 1–2 per product

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** توقيع · لحظة · signature moment · restraint · hero beat · مؤثرات كثيرة · بساطة · لحظة مميزة · minimal · focus

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1420-frontend-design-skills/3376-anthropic-frontend-design`
- `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/signature-moments.md`
- `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-34` قصص الأطفال: كتاب مصور ويوم كامل / Kids stories: picture book & day-to-night arc (seen)
- `STORY-35` منهج المخرج: أطروحة ونقش ونوتة / Motion-director method: thesis, motif, score (documented)
- `STORY-37` قائمة «المظهر المولَّد» الممنوعة / Generated-look blacklist (anti-slop) (ready)
- `STORY-38` شخصية حركة واحدة لكل فيلم / One motion personality per film (documented)

### `STORY-37` — قائمة «المظهر المولَّد» الممنوعة / Generated-look blacklist (anti-slop)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان في المنتصف على تدرج، كل شيء يظهر بتلاشٍ، نص يظهر من الضبابية، تلاشيات متقاطعة، مشهد داكن بتوهج أخضر/بنفسجي، جسيمات ووميض عدسة بلا سبب، Inter/Roboto للعناوين، #6366f1، ثلاث بطاقات متساوية. / Centred title on gradient, everything fading in, blur-in text, crossfades, dark scene with green/purple glow, gratuitous particles/flares, Inter/Roboto display, indigo #6366f1, three equal cards.

**متى:** حين يبدو التصميم أو الموشن كأنه مولّد أو قالب عام وتريد فحصه من الكليشيهات الشائعة / when a design or motion piece looks generic or machine-generated and you want to check it against known clichés

**كيف:** If a choice would appear for any similar brief, replace it with one specific to the subject. Also flagged: gradient text, left accent stripes, cyan-on-dark, pure #000/#fff (tint toward the accent), cream ~#F4F1EA + clay ~#D97757, everything centred, Syne; uppercase eyebrows ≤ ceil(sections/3); ≤2 zigzag rows; grain >3%, uniform chromatic aberration, glass on light backgrounds, springs without overshoot read cheap. `motion.py lint` warns on several of these unless the brand owns them.

**المعاملات:** grain ≤3% · eyebrows ≤ ceil(sections/3)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ممنوعات · مظهر مولد · anti slop · ai look · cliches · lint · كليشيهات · شكل القوالب · تصميم عام · generic look · template look

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/references/motion-craft.md`
- `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`
- `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/references/anti-slop.md`
- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-35` منهج المخرج: أطروحة ونقش ونوتة / Motion-director method: thesis, motif, score (documented)
- `STORY-36` جرأة في مكان واحد / Spend boldness in one place (documented)
- `STORY-38` شخصية حركة واحدة لكل فيلم / One motion personality per film (documented)
- `STORY-39` من الشعور إلى الأرقام / Feeling → motion vocabulary map (documented)

### `STORY-38` — شخصية حركة واحدة لكل فيلم / One motion personality per film

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر شخصية واحدة واستخرج كل حركة من مسموحاتها ومحظوراتها: حقل المؤشر، الجولة الكبرى، الآلة المسكونة، النَفَس المحبوس، التايب الحركي، المادة السائلة، السطح الواحد، الوزن الحقيقي. / Pick one personality and derive every move from its allowed moves and bans.

**متى:** حين تريد أن تخرج كل حركات الفيلم من طابع واحد متسق بمسموحات ومحظورات واضحة / when every move in a film should follow one consistent motion personality with explicit allowed moves and bans

**كيف:** cursor-field: nothing moves until the pointer does, instant response, long settle. grand-tour: film in ≤6 acts, one evolving background world, 2–3 depth layers. haunted-machine: decode/glitch, scanline/dither, split-flap, quantised ticks, no smooth easing. held-breath: one near-imperceptible drift, instant cuts, never two moving things, no springs. kinetic-type: only letterforms move, one text behaviour per view. liquid-material: one viscous substance, recovery slower than disturbance. one-surface: shared-element morphs, no entrance choreography. real-weight: overshoot, 1–2 bounces, one gravity, arrive by moving never fading. Render any of them with kosif-tool render_html.cjs.

**المعاملات:** 8 personalities

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شخصية الحركة · personality · held breath · real weight · kinetic · glitch · طابع الحركة · أسلوب الحركة · اتساق · motion style · consistency

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
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/342-kernel/1223-frontend/motion/held-breath.md`
- `kosif-atlas/skills/342-kernel/1223-frontend/motion/real-weight.md`
- `kosif-atlas/skills/342-kernel/1223-frontend/motion/haunted-machine.md`
- `kosif-tool/tools/render_html.cjs`

#### 7. قدرات قريبة في العائلة

- `STORY-36` جرأة في مكان واحد / Spend boldness in one place (documented)
- `STORY-37` قائمة «المظهر المولَّد» الممنوعة / Generated-look blacklist (anti-slop) (ready)
- `STORY-39` من الشعور إلى الأرقام / Feeling → motion vocabulary map (documented)
- `STORY-40` الأساليب المسماة الثمانية / Eight named visual styles (Swiss Pulse …) (documented)

### `STORY-39` — من الشعور إلى الأرقام / Feeling → motion vocabulary map

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حين يقول المستخدم فخم/تقني/مرح/رسمي/هادئ/صحفي ترجمها إلى مدد ومؤثرات وطابع حركة حسب نوع العميل. / Translate فخم/تقني/مرح/رسمي/هادئ/صحفي into durations, effects and a motion character by client archetype.

**متى:** حين يصف المستخدم الإحساس بكلمات مثل فخم أو تقني أو مرح أو هادئ وتحتاج ترجمتها إلى مدد وحركة / when the user describes a feeling like luxurious, techy, playful or calm and you must turn it into timings and motion

**كيف:** Dramatic: 1–1.5 s fades, scale 0.9→1, spotlight. Techy: neon glow, scramble, grid reveals, particles. Playful: spring bounce, bobbing. Corporate: clean slides. Archetypes: product-led SaaS crisp state changes (120–250 ms feedback); developer tools instrument-like terminal/data progressions; fintech calm, no overshoot; commerce tactile material. Typography by mood: high impact = per-word type + velocity transitions + counters; premium = variable-font + slow transitions; technical = typing + canvas + motion path. Brand archetype (hero, sage, jester…) sets palette temperature and motion energy.

**المعاملات:** feedback 120–250 ms · dramatic fades 1–1.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فخم · تقني · مرح · هادئ · mood · feeling · archetype · رسمي · صحفي · إحساس الفيديو · luxury · playful · corporate

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md`
- `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/motion.md`
- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`
- `kosif-atlas/skills/1503-universal-design-principles/3731-archetypes-brand-voice`

#### 7. قدرات قريبة في العائلة

- `STORY-37` قائمة «المظهر المولَّد» الممنوعة / Generated-look blacklist (anti-slop) (ready)
- `STORY-38` شخصية حركة واحدة لكل فيلم / One motion personality per film (documented)
- `STORY-40` الأساليب المسماة الثمانية / Eight named visual styles (Swiss Pulse …) (documented)
- `STORY-41` أنظمة جمالية جاهزة ولا تخلطها / Aesthetic systems & presets — never mix (documented)

### `STORY-40` — الأساليب المسماة الثمانية / Eight named visual styles (Swiss Pulse …)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** Swiss Pulse، Velvet Standard، Deconstructed، Maximalist Type، Data Drift، Soft Signal، Folk Frequency، Shadow Cut — لكل منها لوحة وخط ومنحنى وانتقال. / Eight designer-inspired styles, each with palette, type, ease signature and transition.

**متى:** حين تريد أسلوبًا بصريًا جاهزًا بلوحة ألوان وخط ومنحنى وانتقال محدد من ثمانية أساليب مسماة / when you want a ready visual style with a set palette, typeface, easing and transition from eight named looks

**كيف:** Swiss Pulse: #1a1a1a + one accent #0066FF or #FFB300, 12-column grid, numbers 80–120 px counting up, expo.out/power4.out, hard cut or iris/zoom. Velvet Standard: navy #1a237e or gold #c9a84c, ALL CAPS tracking ≥0.15em (Latin only), long holds, sine.inOut glide, cross-warp morph. Data Drift: #0a0a0a, #7c3aed, #06b6d4, particles settle into the readable figure, warp transitions. Maximalist Type: loud launches, ridged burn. Deconstructed: raw industrial, glitch/whip pan. Map a mood to a style with the mood→style table.

**المعاملات:** 8 styles

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أساليب · swiss pulse · velvet · data drift · named styles · ستايل جاهز · لوحة ألوان · خطوط · visual style · look

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/visual-styles.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/visual-styles.md`

#### 7. قدرات قريبة في العائلة

- `STORY-38` شخصية حركة واحدة لكل فيلم / One motion personality per film (documented)
- `STORY-39` من الشعور إلى الأرقام / Feeling → motion vocabulary map (documented)
- `STORY-41` أنظمة جمالية جاهزة ولا تخلطها / Aesthetic systems & presets — never mix (documented)
- `STORY-42` قواعد تصميم الحركة / Choreography rules (build · breathe · resolve, 1/3 rules) (ready)

### `STORY-41` — أنظمة جمالية جاهزة ولا تخلطها / Aesthetic systems & presets — never mix

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحريري بسيط، سويسري صناعي، تليمتري CRT، زجاج أثيري، فخامة تحريرية، هيكلية ناعمة، تقييد معايَر — وكل فيلم يتكلم لغة واحدة. / Editorial minimal, Swiss industrial, CRT telemetry, ethereal glass, editorial luxury, soft structuralism, calibrated restraint — one language per film.

**متى:** حين تختار لغة بصرية واحدة للفيلم (تحريري، سويسري، CRT، زجاجي، فخامة) دون خلط الأنظمة / when picking one aesthetic system for a film — editorial, Swiss, CRT, glass, luxury — without mixing systems

**كيف:** Editorial: bone #F7F6F3, ink #111111, border #EAEAEA, pastel pairs FDEBEC/9F2F2D, E1F3FE/1F6C9F; motion translateY 12 px + fade 600 ms cubic-bezier(0.16,1,0.3,1). Swiss industrial: paper #F4F4F0, ink #050505, one red #E61919, radius 0. CRT: bg #0A0A0A, green #4AF626 on one element, scanlines 2 px period 4 px. Ethereal glass: #050505, backdrop blur ~40 px, white/10 hairlines, rise 64 px + blur over ~800 ms cubic-bezier(0.32,0.72,0,1). Calibrated restraint: #F9FAFB/#18181B, one accent (emerald #10B981, blue #3B82F6, rose #E11D48, amber #F59E0B), spring 100/20, stagger index×100 ms. Seed presets (run WCAG checks): neobrutalism #FDC800/#432DD7, neon #BBF351/#00BCFF, vintage OS #008080/#C0C0C0, arcade #2A3FE5 on black, luxury mono #000/#FAFAFA, dramatic #8B5CF6/#F43F5E. Colour dosage: restrained ≤10% accent, committed 30–60%, full palette 3–4 roles, drenched 100%. Decide dark vs light from one sentence about who watches, where, under what light.

**المعاملات:** dosage ≤10 / 30–60 / 100%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نظام جمالي · aesthetic system · editorial · brutalist · glass · presets · dosage · هوية بصرية · زجاجي · سويسري · crt · swiss

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:axe` ← npm ls axe أو وجود node_modules/axe
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`
- `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/neobrutalism/DESIGN.md`
- `kosif-atlas/skills/342-kernel/1223-frontend/variants/abyss.md`
- `kosif-atlas/skills/1394-stark/3329-web-design`

#### 7. قدرات قريبة في العائلة

- `STORY-39` من الشعور إلى الأرقام / Feeling → motion vocabulary map (documented)
- `STORY-40` الأساليب المسماة الثمانية / Eight named visual styles (Swiss Pulse …) (documented)
- `STORY-42` قواعد تصميم الحركة / Choreography rules (build · breathe · resolve, 1/3 rules) (ready)
- `STORY-43` إخراج النبضة بأفعال الطاقة / Beat direction with energy verbs (documented)

### `STORY-42` — قواعد تصميم الحركة / Choreography rules (build · breathe · resolve, 1/3 rules)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل مشهد: بناء متتابع 0–30%، تنفّس بحركة محيطية واحدة 30–70%، حسم 70–100%؛ البطل يقود، حركة مضادة، العمق بالسرعة. / Every scene: staggered build 0–30%, one ambient motion 30–70%, decisive resolve 70–100%; hero leads, counter-motion, depth by speed.

**متى:** حين يبدو التحريك كعرض شرائح وتريد قواعد بناء وتنفّس وحسم وتتابع وحركة مضادة لكل مشهد / when the animation feels like a slideshow and you need build-breathe-resolve, stagger and counter-motion rules per scene

**كيف:** Enter ~0.4 s, exit ~0.25 s (exits ≈40% faster); total stagger <500 ms regardless of count; slowest scene ≈3× slower than fastest. Counter-motion 20–30%; depth speeds 1× / 0.5× / 0.2×; no move over 1/3 of the frame without an intermediate key; with 3+ elements ≤1/3 move at once (observed cap: ≤3 independently moving groups); something new every 2–4 s; one origin per group. Anti-slideshow rule: every meaningful shot carries continuous time-driven motion — verify with frame-hash differences across a scene. Object test per beat: on-screen phrase, a weighted body doing a named verb, the surface — a word is not a body.

**المعاملات:** 30/40/30% · enter 0.4 / exit 0.25 s · stagger <500 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تصميم حركة · choreography · build breathe resolve · stagger · counter motion · anti slideshow · تتابع العناصر · عرض شرائح · حركة مضادة · slideshow · timing rules

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md`
- `kosif-studio/motion/references/motion-craft.md`
- `fastify-motion-bro/AGENTS.md:13`
- `100-superskills/skills/motion-director-pro/references/motion-floor.md`

#### 7. قدرات قريبة في العائلة

- `STORY-40` الأساليب المسماة الثمانية / Eight named visual styles (Swiss Pulse …) (documented)
- `STORY-41` أنظمة جمالية جاهزة ولا تخلطها / Aesthetic systems & presets — never mix (documented)
- `STORY-43` إخراج النبضة بأفعال الطاقة / Beat direction with energy verbs (documented)
- `STORY-44` عدسات النقد قبل الرندر / Creative review lenses & aesthetics council (documented)

### `STORY-43` — إخراج النبضة بأفعال الطاقة / Beat direction with energy verbs

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل نبضة تجربة: مفهوم، إشارة الصوت، وصف سينمائي بخمسة عناصر على الأقل في المقدمة والوسط والخلفية، وكل عنصر له فعل. / Each beat is an experience: concept, VO cue, ≥5 elements across FG/MG/BG, and a verb for every element.

**متى:** حين تكتب توجيه كل نبضة بأفعال طاقة وعناصر موزعة على المقدمة والوسط والخلفية / when directing each beat with energy verbs and 5+ elements spread across foreground, midground and background

**كيف:** Energy verbs: high SLAMS/CRASHES/PUNCHES/STAMPS/SHATTERS; medium CASCADES/SLIDES/DROPS/FILLS/DRAWS; low types on/FLOATS/morphs/COUNTS UP. 8–10 visual elements per beat, 2–3 techniques per beat, ≥2 depth layers, slow push 1→1.04 per beat; declare rhythm up front (fast-fast-SLOW-fast-SHADER-hold). Technique combos by energy: high impact = per-word type + velocity transitions + counters; cinematic = path drawing + video compositing + CSS 3D; technical = typing + procedural canvas. Website films: use ≥50% of captured screenshots, logo in first and last beat, ≤2 consecutive text-only beats; print an asset table first.

**المعاملات:** 8–10 elements · 2–3 techniques · push 1→1.04

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إخراج النبضة · energy verbs · beat direction · depth layers · website film · أفعال الحركة · طبقات العمق · إيقاع المشاهد · foreground background · rhythm

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/beat-direction.md`
- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### 7. قدرات قريبة في العائلة

- `STORY-41` أنظمة جمالية جاهزة ولا تخلطها / Aesthetic systems & presets — never mix (documented)
- `STORY-42` قواعد تصميم الحركة / Choreography rules (build · breathe · resolve, 1/3 rules) (ready)
- `STORY-44` عدسات النقد قبل الرندر / Creative review lenses & aesthetics council (documented)
- `STORY-45` التعلم من المرجع دون نسخه / Learn from references without cloning (proven)

### `STORY-44` — عدسات النقد قبل الرندر / Creative review lenses & aesthetics council

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مروران: اطرح حتى يقول كل إطار نية واحدة (سبعة صفوف ← درجة من 10)، ثم 12 عدسة فنية تتحدى المشهد. / Two passes: subtract until each frame states one intent (7 rows → score /10), then 12 art-direction lenses challenge the scene.

**متى:** حين تريد قبل الرندر نقد المشهد وتقييمه من 10 وتحديه بعدسات فنية كالإضاءة والتكوين واللون / when you want to critique and score a scene before render and challenge it through lenses like lighting, composition and colour

**كيف:** Score: 7/7 → 10, 6/7 → 9, 5/7 → 7. Lenses VA01–VA12: spatial worldbuilder, character designer, action choreographer, cinematographer, lighting artist, colourist, VFX designer, atmosphere & weather, materials & texture, production designer, composition director, beauty critic. Basma autopilot critique: a 6-frame contact sheet (3 columns, 264 px tiles, timestamps) scored on hook, readability, motion, variety, safe zones, brief, sound sync, identity, then fixes the three worst problems (needs its AI key).

**المعاملات:** 7 rows → /10 · 12 lenses · 6-frame sheet

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقد · مراجعة · critique · review · contact sheet · lenses · تقييم · نقد فني · تكوين · art direction · quality check

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/3438-ux-design/14123-steve-jobs-design-review/SKILL.md`
- `kosif-one/tools/kosif-omni/skills/kosif-visual-aesthetics-council/SKILL.md`
- `app/public/js/00_editor.js:2394`

#### 7. قدرات قريبة في العائلة

- `STORY-42` قواعد تصميم الحركة / Choreography rules (build · breathe · resolve, 1/3 rules) (ready)
- `STORY-43` إخراج النبضة بأفعال الطاقة / Beat direction with energy verbs (documented)
- `STORY-45` التعلم من المرجع دون نسخه / Learn from references without cloning (proven)
- `STORY-46` قواعد الصدق في الوعود / Honesty rules for claims (documented)

### `STORY-45` — التعلم من المرجع دون نسخه / Learn from references without cloning

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لكل مرجع وظيفة واحدة (حركة، كاميرا وإيقاع، أو هوية) مع قائمة «لا تنسخ»، واستعر القواعد لا المحتوى. / Give each reference one job with a do-not-copy list; borrow grammar, never content.

**متى:** حين يعطي المستخدم فيديو مرجعيًا ويريد أسلوبًا مشابهًا دون نسخ محتواه / when the user shares a reference video and wants a similar style without copying its content

**كيف:** `python3 motion.py study REFERENCE.mp4 --out DIR` measures cuts, shot lengths, first change, motion energy, stillness and palette into style_guide.md (verified here on a 6 s test clip: wrote style_guide.md, study.json, contact.png, first_frame.png, review.md). Keep only what is constant across ≥3 films; anything unique to one is its costume; state "do not average the references". Never copy scripts, logos, characters, footage or people; if you cannot open the frames, say so and ask for 5–8 screenshots. For famous infographics, redesign so it could not be mistaken for the reference (palette, type, layout, cadence). Basma DNA.toStyle turns a measured fingerprint into caption, zoom, transition and grade settings without a model.

**المعاملات:** constant across ≥3 refs · 5–8 screenshots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مرجع · محاكاة · reference · study · style guide · imitation · فيديو مرجعي · نفس الستايل · تحليل مرجع · inspiration · similar style

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/tools/kosif-studio/motion/qa.py:1`
- `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`
- `fastify-motion-bro/AGENTS.md:8`
- `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-43` إخراج النبضة بأفعال الطاقة / Beat direction with energy verbs (documented)
- `STORY-44` عدسات النقد قبل الرندر / Creative review lenses & aesthetics council (documented)
- `STORY-46` قواعد الصدق في الوعود / Honesty rules for claims (documented)
- `STORY-47` الشيء المحمول عبر الفيلم / Travelling device / hero-object thread (ready)

### `STORY-46` — قواعد الصدق في الوعود / Honesty rules for claims

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** «واقعي» = لوحة رقمية مضاءة بواقعية لا صورة فوتوغرافية؛ الأرقام من المصدر فقط؛ لا تدّعي رؤية ما لم تفتحه. / "Realistic" means a realistically lit painting, not a photo; numbers only from the source; never claim to have seen what you did not open.

**متى:** حين يطلب المستخدم نتيجة «واقعية» أو أرقامًا أو تلخيص مستند وتحتاج توضيح الحدود دون اختراع / when the user asks for 'realistic' output, figures or a document summary and you must state limits without inventing

**كيف:** State limits up front (code from a description never matches a photo; exact match only via image code or exact mode). Facts only from the cue: scene headline is the number the cue said, else its longest word — never a demo value (audio2motion.head, tested). Document → film: summarise faithfully, never invent facts; image-only PDFs are rejected with an OCR hint. Label fictional data.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صدق · لا اختراع · honesty · no invented numbers · limits · أمانة · حدود · واقعي · accuracy · fact check

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/references/drawing-guide.md:93`
- `kosif-studio/motion/audio2motion.py:49`
- `kosif-studio/tests/test_audio2motion.py:43`
- `app/public/js/10_studio.js:2787`

#### 7. قدرات قريبة في العائلة

- `STORY-44` عدسات النقد قبل الرندر / Creative review lenses & aesthetics council (documented)
- `STORY-45` التعلم من المرجع دون نسخه / Learn from references without cloning (proven)
- `STORY-47` الشيء المحمول عبر الفيلم / Travelling device / hero-object thread (ready)
- `STORY-48` كشف جملة الذروة / Payoff-line detection (proven)

### `STORY-47` — الشيء المحمول عبر الفيلم / Travelling device / hero-object thread

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جسم واحد (نقطة، كرة، شمس) يعيش في كل لقطة: يهبط، ينبض على الإيقاع، يصير زرًا ثم نقطة الجملة ثم نقطة الشعار. / One object survives every cut — lands, pulses on beats, becomes a button, a full stop, the logo dot.

**متى:** حين تريد عنصرًا واحدًا يربط الفيلم كله، كنقطة تنبض مع الإيقاع وتصير زرًا ثم نقطة الشعار / when one object should carry through every cut — a dot that pulses on beat, becomes a button and ends as the logo dot

**كيف:** KOSIF showreel: dot #E4342F on #0F1211, rides a sampled path (60 samples) on a 120 BPM clock, pulses 1.25/1.2 scale (0.06 s out, 0.22 s settle), squashes on landing, opens the iris onto footage, ends as the lockup’s full stop (15 s 1080p60, rendered kosif_motion_showreel.mp4). Observed: coral dot ≈2.5–3% of height reused as i-dot, full stop and decimal with squash 0.7/1.3; orange ball #ff5a1f at the same screen position at each cut for a match. Dua film variant: the sun climbs and on the key line lifts with a heavy spring into the rosette (flash peak .55, scale 1→1.18→1). Evolution chain: each scene’s object is born from the previous (point → line → circle → sphere → lens → ball → world → full stop), 2.5–3 s per step, no cuts.

**المعاملات:** pulse 1.25 / 0.06 + 0.22 s · squash 0.7/1.3 · 120 BPM

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حامل · نقطة · travelling device · hero object · match cut · continuity · عنصر رابط · ربط اللقطات · نبض على الإيقاع · transition · thread

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/projects/showreel/index.html:66`
- `kosif-studio/out/kosif_motion_showreel.mp4`
- `kosif-one/projects/thursday-dua-animation/source/index.html:153-161`
- `style:pm-1littlecoder-9fef89`
- `style:pm-leonkohli-6dc01b`
- `style:pm-hbcoop-de365c`

#### 7. قدرات قريبة في العائلة

- `STORY-45` التعلم من المرجع دون نسخه / Learn from references without cloning (proven)
- `STORY-46` قواعد الصدق في الوعود / Honesty rules for claims (documented)
- `STORY-48` كشف جملة الذروة / Payoff-line detection (proven)
- `STORY-49` من المعنى إلى الرمز / Concept-to-symbol motifs (ready)

### `STORY-48` — كشف جملة الذروة / Payoff-line detection

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يجد سطر الذروة: بعد سطر قصير متكرر (كافح… كافح) الجملة التالية تحسمه؛ في الأغاني آخر عودة للازمة؛ وإلا أكثر جملة منبورة في آخر 40%. / Finds the climax line: after a repeated short line the next sentence resolves it; in songs the last refrain return; else the most stressed sentence in the last 40%.

**متى:** حين تريد إيجاد جملة الذروة في كلام أو أغنية لتكبيرها وإبرازها وتثبيتها قبل الإظلام / when you need to find the climax line in a speech or song to enlarge, highlight and hold it before the dip

**كيف:** direct.plan / verse.plan: refrain = line heard ≥2×; payoff line size ×1.22, light sweep, flare, held +2.2 s, then dip to black. Tested here (test_direct_plans_like_an_editor, test_verse_reads_a_text_like_a_lyricist).

**المعاملات:** size ×1.22 · hold +2.2 s · last 40%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ذروة · لازمة · payoff · climax · refrain · stress · جملة مهمة · كلمات الأغنية · إبراز · lyrics · key line

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/direct.py:116`
- `kosif-studio/motion/verse.py:280`
- `kosif-studio/tests/test_studio.py:910`

#### 7. قدرات قريبة في العائلة

- `STORY-46` قواعد الصدق في الوعود / Honesty rules for claims (documented)
- `STORY-47` الشيء المحمول عبر الفيلم / Travelling device / hero-object thread (ready)
- `STORY-49` من المعنى إلى الرمز / Concept-to-symbol motifs (ready)
- `STORY-50` أنظمة الفصول المرقّمة / Chapter label systems (seen)

### `STORY-49` — من المعنى إلى الرمز / Concept-to-symbol motifs

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** معنى الكلمة المفتاحية يختار رمزًا يُرسم بجوار السطر، والأرقام المنطوقة تصير عدّادًا، والرموز مقننة كي لا تصير ورق حائط. / A keyword’s meaning picks a symbol drawn beside the line; spoken numbers become a counter; symbols are rationed.

**متى:** حين تريد رسم رمز بجوار الكلام حسب معنى الكلمة المفتاحية وتحويل الأرقام المنطوقة إلى عدّاد / when a keyword's meaning should trigger a drawn symbol beside the line and spoken numbers become a counter

**كيف:** verse.concept_of: 12 concepts (sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light) matched by Arabic roots + English prefixes, stripping و ف ب ل ال. Hero metaphor objects for kinetic beats (Fastify, tested): rocket, chess piece, hourglass, blank glass cube, magnifying glass, paper staircase, generic interface — "no text on the object".

**المعاملات:** 12 concepts · 7 metaphor objects

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رمز · استعارة · symbol · motif · metaphor · icon · أيقونات · عداد · رسومات توضيحية · counter · keyword

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/verse.py:173`
- `kosif-studio/motion/verse.py:322`
- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:103,110-111`

#### 7. قدرات قريبة في العائلة

- `STORY-47` الشيء المحمول عبر الفيلم / Travelling device / hero-object thread (ready)
- `STORY-48` كشف جملة الذروة / Payoff-line detection (proven)
- `STORY-50` أنظمة الفصول المرقّمة / Chapter label systems (seen)
- `STORY-51` خواتيم الملخص / Recap endings (grid · collage · board · progress) (seen)

### `STORY-50` — أنظمة الفصول المرقّمة / Chapter label systems

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رقم الفصل + اسم بأحرف كبيرة + عنوان فرعي مائل، أو «• 0N / فعل الاسم» فوق العنوان، أو دائرة سوداء برقم أبيض. / Chapter number + caps label + italic subtitle, "• 0N / VERB THE NOUN" eyebrow, or a black circle with a white number.

**متى:** حين يحتاج فيديو طويل أو درس أو ريل عرض عناوين فصول مرقمة تفصل الأقسام / when a long video, lesson or showreel needs numbered chapter labels to separate sections

**كيف:** Variants seen: mono label at 1.2% frame height with accent dot; "[0N] WORD" heavy caps top-left; 14 px numbered chip; yellow numbered title top-left, FadeOut all, short empty beat (12–14 sections for a 7 min lesson, fade 0.5–1 s); per-unit framing that resets an "elapsed 0 → 1.000 s" bar each chapter; showreel chapters named by skill, 8 × 1.6 s + 2 s end. For Arabic use Arabic-Indic or Latin digits consistently (ARAB-73).

**المعاملات:** eyebrow 1.2% h · 8 × 1.6 s showreel

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فصول · ترقيم · chapters · chapter card · numbered · sections · عناوين الفصول · أقسام · عنوان فرعي · section titles · lesson

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-codestackr-c071bf`
- `style:pm-elliot-garreffa-f334bc`
- `style:pm-moguzbulbul-6311b6`
- `style:pm-linearuncle-5d2bae`
- `style:pm-nolkeeg-bf062e`
- `style:pm-shinskinakamoto-20190b`

#### 7. قدرات قريبة في العائلة

- `STORY-48` كشف جملة الذروة / Payoff-line detection (proven)
- `STORY-49` من المعنى إلى الرمز / Concept-to-symbol motifs (ready)
- `STORY-51` خواتيم الملخص / Recap endings (grid · collage · board · progress) (seen)
- `STORY-52` الإطار المغلق والحلقة / Bookends & loop endings (seen)

### `STORY-51` — خواتيم الملخص / Recap endings (grid · collage · board · progress)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة من عمودين لكل العناصر، أو كولاج للمشاهد السابقة يطير إلى شبكة 3×3، أو لوحة خلاصات ملونة، أو عداد رندر وهمي يملأ شريط الفصول. / Two-column summary grid, collage of earlier scenes flying into a 3×3, colour-coded takeaway board, or a fake render-progress recap.

**متى:** عند ختام فيديو شرح أو قائمة بملخص: شبكة عناصر أو كولاج للمشاهد أو لوحة خلاصات / when ending an explainer or list video with a recap — summary grid, scene collage, takeaway board or progress bar

**كيف:** Grid: index in accent, title, one-line hook, rating, recommendation bar, row stagger 120 ms. Collage: tilted thumbnails rotate ±4°, stagger 50 ms, 500 ms easeOutBack. Board: 5 one-line takeaways each in its chapter colour + boxed footnote, one line per narration sentence. Progress: blue screen, spinner + filename, rolling percent 0 → 99 in ≈1.5 s with digit motion blur, filmstrip of chapters filling left-to-right (RTL for Arabic). Reflective ending: 2–3 numbered open questions held ~8–10 s each.

**المعاملات:** row 120 ms · collage 50 ms / ±4° / 500 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ملخص · خاتمة · recap · summary grid · collage · takeaways · خلاصة · نهاية الفيديو · كولاج · ending · wrap-up

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-gigabit-million-16b3a0`
- `style:pm-motiondsgnr-9dcfa6`
- `style:pm-tak3sh8-be5012`
- `style:pm-levabashidze-2d713a`
- `style:pm-linearuncle-5d2bae`

#### 7. قدرات قريبة في العائلة

- `STORY-49` من المعنى إلى الرمز / Concept-to-symbol motifs (ready)
- `STORY-50` أنظمة الفصول المرقّمة / Chapter label systems (seen)
- `STORY-52` الإطار المغلق والحلقة / Bookends & loop endings (seen)
- `STORY-53` بطاقات الجملة والصمت / Statement cards, caption beats & silence (seen)

### `STORY-52` — الإطار المغلق والحلقة / Bookends & loop endings

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** افتح وأغلق على نفس البطاقة أو العنوان أو الإطار الهادئ، أو عُد لنفس الفيلم ليتكرر الفيديو بلا نهاية. / Open and close on the same card/title/calm frame, or return to the opening so the video loops.

**متى:** حين تريد نهاية تعود لنفس بطاقة البداية أو إطارها، أو فيديو يعود لأوله ليتكرر كحلقة / when the ending should mirror the opening card or frame, or return to the start so the video loops

**كيف:** Title bookend: same tracked title + subtitle, ending version over the darkened final image, fade 1.5 s (Latin tracking only). Control → escape → chaos → control: acts named in a HUD, bookended by the same calm frame (5 acts / 30 s). Loop bookend: open on rapid output previews (~0.5 s cuts), explain, end on the same film. Code-loop outro: only a blinking cursor remains. Calm porthole ending: circle mask with slow loop, italic word, title. Seamless technical loop: FMT seamless loop.

**المعاملات:** fade 1.5 s · intro cuts ~0.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إطار مغلق · حلقة · bookend · loop · outro · ending · تكرار · بداية ونهاية · لوب · looping video · closing

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-rebutonepress-810f78`
- `style:pm-pankajkumar-dev-0bee87`
- `style:pm-lemomo-ai-0d9cff`
- `style:pm-web3wesley-7bb108`
- `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `STORY-50` أنظمة الفصول المرقّمة / Chapter label systems (seen)
- `STORY-51` خواتيم الملخص / Recap endings (grid · collage · board · progress) (seen)
- `STORY-53` بطاقات الجملة والصمت / Statement cards, caption beats & silence (seen)
- `STORY-54` تبدّل المزاج: ظلام/نور، نهار/ليل / Mood shifts: dark↔light acts, day/night interludes (seen)

### `STORY-53` — بطاقات الجملة والصمت / Statement cards, caption beats & silence

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قطع إلى أسود بجملة واحدة عريضة لتغيير الفصل، أو سطر قصير على أسود يتلاشى ويثبت، أو صمت في ظلام قبل الذروة. / Hard cut to black with one bold sentence to change chapter; short line on black; silence in darkness before the climax.

**متى:** حين تحتاج فاصلًا بجملة واحدة على شاشة سوداء لتغيير الفصل أو لحظة صمت في الظلام قبل الذروة / when you need a bold one-line card on black to change chapter, or a dark silent beat before the climax

**كيف:** Statement card: white weight 800, hold 1.5–2 s, then cut back to UI. Narrative caption beat: fade 400 ms, hold 2 s. Darkness beat: mean luminance <3% with one ember for 2–3 s. Calm lock-up outro after a frenzy: black, centred wordmark, 3-line tagline, handles, hold 3–4 s, fade 400 ms. Made-with-code end card: three short bold lines + muted credits row, hold 3–5 s. Arabic: no tracking on the tagline.

**المعاملات:** hold 1.5–2 s · fade 400 ms · luminance <3%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بطاقة · أسود · statement card · black card · silence · outro · شاشة سوداء · فاصل · جملة واحدة · end card · pause

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-lester-tyy-f897f7`
- `style:pm-marklaunches-3b9492`
- `style:pm-kamstudiolabs-0b0824`
- `style:pm-micheleharmonic-77628e`
- `style:pm-kantamk-61f410`

#### 7. قدرات قريبة في العائلة

- `STORY-51` خواتيم الملخص / Recap endings (grid · collage · board · progress) (seen)
- `STORY-52` الإطار المغلق والحلقة / Bookends & loop endings (seen)
- `STORY-54` تبدّل المزاج: ظلام/نور، نهار/ليل / Mood shifts: dark↔light acts, day/night interludes (seen)
- `STORY-55` نبضات كوميدية وعاطفية / Comic & emotional beats (seen)

### `STORY-54` — تبدّل المزاج: ظلام/نور، نهار/ليل / Mood shifts: dark↔light acts, day/night interludes

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بدّل الثيم في منتصف الفيلم ليعلن انتقال المشكلة إلى الحل، أو أدخل مشهدًا نيليًا واحدًا «بينما تنام» ثم عد للنور. / Switch theme mid-film to mark problem → solution, or insert one indigo "while you sleep" scene.

**متى:** حين تريد قلب مزاج الفيلم من المشكلة إلى الحل بتبديل الثيم من ظلام لنور أو إدراج مشهد ليلي / when switching the film's theme from dark to light to mark problem → solution, or inserting a night interlude

**كيف:** Crossfade 600 ms into the interlude; 3D world moods (earth crystal world, tested): locked glow .25 speed .55, open glow .6 speed 1, unlock glow 1.6 speed 1.6, lerp k=.04 per frame, pulse adds up to 3 and decays ×0.92 per frame. Genre-hop: keep one message but re-skin each beat in a distinct genre (palette, font, texture, framing) for 6–8 s each; climax gag: hold a browser-default page (Times, white) for 3–5 s.

**المعاملات:** crossfade 600 ms · lerp .04 · genre 6–8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مزاج · ليل · نهار · mood shift · dark light · genre hop · interlude · ثيم · تحول · ظلام ونور · theme switch · night scene

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-sudo-kiran-b055de`
- `style:pm-sachaarbonel-8f14f4`
- `kosif-earth-ci-fork/ui/art/crystal-world.js:96`
- `kosif-earth-ci-fork/tools/crystal_world.test.mjs`
- `style:pm-emollick-8661a8`

#### 7. قدرات قريبة في العائلة

- `STORY-52` الإطار المغلق والحلقة / Bookends & loop endings (seen)
- `STORY-53` بطاقات الجملة والصمت / Statement cards, caption beats & silence (seen)
- `STORY-55` نبضات كوميدية وعاطفية / Comic & emotional beats (seen)
- `STORY-56` نبضات الحجة / Argument beats (pain triptych · THE FIX bar · cost reframing · paper-form) (seen)

### `STORY-55` — نبضات كوميدية وعاطفية / Comic & emotional beats

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فقاعة كلام مضحكة، ختم ميم، مؤشر عملاق خصم، اعتراف بالكليشيه، انقلاب شخصية لتختبئ، نقل التوهج من الشخصية للشيء. / Speech-bubble gag, meme stamp, giant cursor antagonist, self-aware cliché, character flip to hide, glow transferred from character to object.

**متى:** حين تريد لحظة مضحكة أو عاطفية في الموشن مثل فقاعة كلام أو ختم ميم أو قلب الشخصية / when adding a comic or emotional beat — speech-bubble gag, meme stamp, giant cursor or character flip

**كيف:** Bubble: anchored to the projected character position, pop 0→1.1→1 back-out, hold 1.5 s, white fill, 2 px black stroke, radius 10 px, tail triangle. Stamp: scale 1.4→1 in 3 frames, hold 2 s after escalating damage. Flip: rotate 180° to a blank back face in 600 ms easeInOut, then return. Paper airplane: bezier flight 800 ms, unfold scaleX 0→1 in 300 ms with crease lines. Accumulating props: each compliment adds a persistent prop (text-on-path sash, clips), drop-in 400 ms back-out. Question-mark twist: assumption 1.5 s → scramble + strike 1.5 s → "?" hold 1 s → promise.

**المعاملات:** pop 0→1.1→1 · stamp 3 frames · flip 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كوميديا · فقاعة · gag · speech bubble · stamp · emotional beat · ميم · ضحك · إفيه · meme · humor

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-gorden-sun-041f56`
- `style:pm-0xevinho-3777d8`
- `style:pm-kamstudiolabs-c9bb28`
- `style:pm-anilraok-eff262`
- `style:pm-jake11moran-a269c4`
- `style:pm-robj3d3-b18fad`

#### 7. قدرات قريبة في العائلة

- `STORY-53` بطاقات الجملة والصمت / Statement cards, caption beats & silence (seen)
- `STORY-54` تبدّل المزاج: ظلام/نور، نهار/ليل / Mood shifts: dark↔light acts, day/night interludes (seen)
- `STORY-56` نبضات الحجة / Argument beats (pain triptych · THE FIX bar · cost reframing · paper-form) (seen)
- `STORY-57` جسر الوميض والسحب للخلف إلى ملصق / Flash bridge + poster pull-back reveal (seen)

### `STORY-56` — نبضات الحجة / Argument beats (pain triptych · THE FIX bar · cost reframing · paper-form)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة أعمدة ألم بأمثلة واجهة صغيرة، شريط «الحل» بقاعدة واحدة وإحصاء تكرار، رقم خسارة كبير أمام سعر يومي صغير، واستمارة ورقية تمثل الطريقة القديمة تُشطب بالأحمر. / Three pain columns with mini-UI proof, a "THE FIX" bar with a frequency stat, big loss vs tiny daily price, and an old-way paper form struck in red.

**متى:** حين تبني فيديو إقناعيًا يعرض نقاط الألم ثم الحل وإعادة تأطير التكلفة والطريقة القديمة المشطوبة / when building a persuasive video showing pain points, the fix, a cost reframe and the old way struck out

**كيف:** Triptych: icon chip, short title, mini UI, one-line caption, built right-to-left for Arabic, stagger 300 ms, radius 12 px. FIX bar: cream full-width card, green pill, one-sentence rule, divider, "≈1 in N" stat, slide-up 400 ms easeOutCubic. Paper form: hard cut from the dark world to an off-white form (black header bar, numbered fields), red marker strike drawn in 400 ms. Phase captions: steady / burst / recovery with a final takeaway in accent.

**المعاملات:** stagger 300 ms · slide-up 400 ms · strike 400 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حجة · ألم · pain points · the fix · reframing · persuasion · إقناع · مشكلة وحل · مقارنة السعر · argument · old vs new

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-aschapmann-131210`
- `style:pm-henkvaness-0e06af`
- `style:pm-thayto-dev-44b911`
- `style:plotter`
- `style:pm-parkerrex-1a54fe`

#### 7. قدرات قريبة في العائلة

- `STORY-54` تبدّل المزاج: ظلام/نور، نهار/ليل / Mood shifts: dark↔light acts, day/night interludes (seen)
- `STORY-55` نبضات كوميدية وعاطفية / Comic & emotional beats (seen)
- `STORY-57` جسر الوميض والسحب للخلف إلى ملصق / Flash bridge + poster pull-back reveal (seen)
- `STORY-58` نبضات العالم والحالة / World beats: surreal props, overload, one-take, beacon (seen)

### `STORY-57` — جسر الوميض والسحب للخلف إلى ملصق / Flash bridge + poster pull-back reveal

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ادفع داخل الضوء حتى يملأ الإطار، وميض بلونه، ثم ابدأ المشهد التالي مكبَّرًا داخل ملصق صغير لنفس المشهد وارجع لتكشف الحائط والعنوان. / Push into light until full frame, flash to its colour, start the next scene zoomed inside a small poster of itself and pull back to reveal wall + headline.

**متى:** حين تريد انتقالًا بين مشهدين بالدفع داخل الضوء ثم وميض ثم سحب للخلف يكشف المشهد كملصق على حائط / for a transition that pushes into light, flashes, then pulls back to reveal the next scene as a poster on a wall

**كيف:** Flash ~200 ms; pull-back ~2 s easeOutCubic from inside a small <svg viewBox> poster. Step-out-of-painting outro: the 3D scene flattens back into a framed canvas on a wall.

**المعاملات:** flash 200 ms · pull-back 2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وميض · سحب للخلف · flash bridge · pull back · poster reveal · انتقال · ترانزيشن · ملصق · transition · zoom out

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:fake3d`
- `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `STORY-55` نبضات كوميدية وعاطفية / Comic & emotional beats (seen)
- `STORY-56` نبضات الحجة / Argument beats (pain triptych · THE FIX bar · cost reframing · paper-form) (seen)
- `STORY-58` نبضات العالم والحالة / World beats: surreal props, overload, one-take, beacon (seen)
- `STORY-59` مونتاج مُخرَج لمقطع كلام / Directed edit of a talking clip (proven)

### `STORY-58` — نبضات العالم والحالة / World beats: surreal props, overload, one-take, beacon

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أشياء قديمة تطفو في السماء، كل شيء يتسارع حول مركز هادئ، لقطة واحدة بلا قطع يقودها قسم الموسيقى، ومنارة تنبض لتصوير مفهوم مجرد. / Floating vintage props, overload closing in on a calm centre, a cut-free single take driven by music sections, a beacon visualising an abstract concept.

**متى:** حين تريد مشهدًا سرياليًا أو ازدحامًا حول مركز هادئ أو لقطة واحدة بلا قطع أو منارة لمفهوم مجرد / for a surreal floating-props scene, overload around a calm centre, a cut-free single take or a beacon for an abstract idea

**كيف:** Drift 10–30 px/s, rotation 2–8 °/s. Overwhelm surround (HyperFrames block, count 16 (8–24), intensity 0.5–2). Single take: density of launches rises toward the climax, HUD shows state names. Beacon: proper interval 1 s × 1/√(1−r_s/r) — observed interval grows and redshifts near the horizon. Life-as-a-game metaphor: skills as levels, progress as score, end card "Player 1".

**المعاملات:** drift 10–30 px/s · 2–8 °/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سريالي · ازدحام · surreal · overwhelm · single take · metaphor · خيال · لقطة واحدة · مفهوم مجرد · one take · floating

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `style:pm-koldo2k-5cff87`
- `kosif-one/vendor/hyperframes/registry/components/overwhelm-surround/overwhelm-surround.html`
- `style:pm-kamstudiolabs-447565`
- `style:pm-rebutonepress-810f78`
- `style:pm-ibrahimwasim240-809370`

#### 7. قدرات قريبة في العائلة

- `STORY-56` نبضات الحجة / Argument beats (pain triptych · THE FIX bar · cost reframing · paper-form) (seen)
- `STORY-57` جسر الوميض والسحب للخلف إلى ملصق / Flash bridge + poster pull-back reveal (seen)
- `STORY-59` مونتاج مُخرَج لمقطع كلام / Directed edit of a talking clip (proven)
- `STORY-60` قوس الريل التحفيزي (FINAL_EDIT) / Motivational talking-reel arc (FINAL_EDIT) (ready)

### `STORY-59` — مونتاج مُخرَج لمقطع كلام / Directed edit of a talking clip

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يبني تكوينًا قابلًا للتحرير من مقطع كلام: لوحة نظيفة، سلسلة صوت، دفع نحو المتكلم، كلمة مفتاحية لكل جملة بخط كبير وضربة، أرقام كحلقات ساعة، كلمة القطع كسطح انتقال، ودفعة ثم إظلام. / Builds an editable composition: clean plate, voice chain, subject push, a stressed keyword per sentence with a punch, numbers as clock rings, the cut word as a transition plane, payoff then dip.

**متى:** حين يعطي المستخدم فيديو كلام ويريد ريلًا مُمنتجًا بكلمات مفتاحية كبيرة وترجمة وأرقام وانتقالات / when the user gives a talking clip and wants an edited reel with big keywords, captions, number rings and transitions

**كيف:** `python3 direct.py CLIP.mp4 --name NAME --size 1080x1920 --words X.words.json --accent "#E7B65A" --credit "…" [--fix "a=b"] [--render]` → projects/NAME/edit.js (also `kmotion direct`). Plate libx264 slow crf 15 -g 1; keyword 190 px; captions 54 px ≤6 words; hook releases at the second word; end = last word + 0.35 s; stress = loudness × length. Planning is tested here; full render needs faster-whisper (pip install faster-whisper) and the clip.

**المعاملات:** keyword 190 px · captions 54 px ≤6 w · end +0.35 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مونتاج مُخرج · مقطع كلام · talking head · directed edit · keyword · reel · فيديو متكلم · ترجمة · كابشن · captions · talking video

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/direct.py:231`
- `kosif-studio/tests/test_studio.py:910`
- `100-superskills/skills/kosif-montage-motion/scripts/direct.py`

#### 7. قدرات قريبة في العائلة

- `STORY-57` جسر الوميض والسحب للخلف إلى ملصق / Flash bridge + poster pull-back reveal (seen)
- `STORY-58` نبضات العالم والحالة / World beats: surreal props, overload, one-take, beacon (seen)
- `STORY-60` قوس الريل التحفيزي (FINAL_EDIT) / Motivational talking-reel arc (FINAL_EDIT) (ready)
- `STORY-61` فيلم الإطلاق من الموقع أو الكود / Launch video from a site or codebase (/brag) (ready)

### `STORY-60` — قوس الريل التحفيزي (FINAL_EDIT) / Motivational talking-reel arc (FINAL_EDIT)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قوس مثبت 20 ث: تجميد خطاف ← رسم الإدراك ← دفء الحلم ← أمثلة دقيقة ≈1.2 ث ← ضربات ضغط ← انفراج بلون مميز ← كلمة ضخمة كانتقال ← دفعة ← إظلام. / A proven 20 s arc: hook freeze → realisation graphic → dream warmth → micro examples ≈1.2 s → pressure punches → lift in accent → giant-word transition → payoff → dip.

**متى:** حين يريد المستخدم ريلًا تحفيزيًا من مقطع كلام بقوس 20 ثانية من الخطاف إلى الانفراج والدفعة / when the user wants a motivational talking reel built on a 20 s arc from hook freeze to lift, payoff and dip

**كيف:** Time map: 0 hook, 1.56 clock, 3.28 dream, 5.22 weight, 7.24 car, 9.5 pressure, 11.3 lift, 13.14 word transition, 14.62 time drain, 16.02 build, 17.26 payoff, 18.42 close, 20.06 dip. Delivered at 20.57 s 1080×1920 30 fps, −14.4 LUFS, TP −2.7 dBTP. Premium edit by hand: decaption, Lanczos restore, push 100→108%, 3 text levels, micro-graphics ≤1.5 s, payoff alone, two reviewers P0/P1/P2.

**المعاملات:** 20.57 s · −14.4 LUFS · push 100→108%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحفيزي · ريل · motivational · talking reel · arc · premium edit · فيديو تحفيزي · مونتاج احترافي · ريلز · motivation · speech reel

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:188`
- `kosif-studio/out/FINAL_EDIT/EDIT_NOTES.txt`
- `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-58` نبضات العالم والحالة / World beats: surreal props, overload, one-take, beacon (seen)
- `STORY-59` مونتاج مُخرَج لمقطع كلام / Directed edit of a talking clip (proven)
- `STORY-61` فيلم الإطلاق من الموقع أو الكود / Launch video from a site or codebase (/brag) (ready)
- `STORY-62` بنية ريل العرض 15 ث / Showreel beat structure (120 BPM) (ready)

### `STORY-61` — فيلم الإطلاق من الموقع أو الكود / Launch video from a site or codebase (/brag)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اجمع مادة المنتج، أجب عن 9 أسئلة فحص، ابنِ ستوريبورد من رحلة المستخدم الحقيقية، ثم سلّم بغلاف ونص مشاركة — 15–25 ث. / Gather product material, answer a 9-question rubric, storyboard the real user flow, deliver with poster and share copy — 15–25 s.

**متى:** حين يريد المستخدم فيديو إطلاق قصيرًا لمنتجه من رابط موقعه أو من الكود مع غلاف ونص مشاركة / when the user wants a 15–25 s launch video built from their website or codebase, with poster and share copy

**كيف:** `python3 scripts/kmotion.py brag init DIR\|URL --tone default\|polished\|yc-parody\|chaotic\|deadpan\|cinematic\|app-store --format landscape\|vertical\|square --duration 20` → storyboard; `brag deliver OUT --film film.mp4` (poster + gate; share copy ≤280 chars tested by test_launch). Shape: hook 2–3 s, reveal 2–4 s, 2–3 highlights (entry → action → result), outro 2–4 s, 18–22 s ideal. Tones: default 4–5 scenes soft; polished 3–4 long holds, crossfade 0.6–0.8 s; yc-parody deadpan hard cuts; chaotic 6–8 scenes some <2 s, flash/zoom cut 1.2→1.0; deadpan 3–4 scenes, 0.8–1.0 s fades; cinematic big type, dramatic wipes, 0.95→1.0; app-store 4–6 feature cards, 0.35–0.45 s slides. Website 7-step variant: capture → brand cheat sheet → narration → beat storyboard → VO + timestamps → compositions → validate.

**المعاملات:** 15–25 s · share ≤280 chars · 7 tones

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إطلاق · brag · launch video · tones · website to video · share copy · إطلاق منتج · فيديو من موقع · نص مشاركة · product launch · url to video

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29`
- `100-superskills/skills/kosif-montage-motion/references/launch-video.md`
- `100-superskills/skills/kosif-montage-motion/tests/test_launch.py`
- `kosif-one/vendor/brag/skills/brag/references/step-1-inspect.md`

#### 7. قدرات قريبة في العائلة

- `STORY-59` مونتاج مُخرَج لمقطع كلام / Directed edit of a talking clip (proven)
- `STORY-60` قوس الريل التحفيزي (FINAL_EDIT) / Motivational talking-reel arc (FINAL_EDIT) (ready)
- `STORY-62` بنية ريل العرض 15 ث / Showreel beat structure (120 BPM) (ready)
- `STORY-63` فيلم المختبر SHAPE→RANK / Product-lab film (SHAPE → JOINT → LOAD → BREAK → SWAP → RANK) (ready)

### `STORY-62` — بنية ريل العرض 15 ث / Showreel beat structure (120 BPM)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ادعاء خطاف، ضغطة زر، عدّاد تقدم، منحنى نابض يُرسم بالقلم، قانون يُكتب، قزحية تسقط إلى لقطات حقيقية، بطاقة حقائق، انهيار للداخل، شعار. / Hook claim, button press, progress counter, pen-drawn spring curve, typed law, iris to real footage, fact card, implode, lockup.

**متى:** حين تريد ريل عرض 15 ثانية لاستوديو أو أداة تقع لقطاته على شبكة إيقاع 120 BPM / when making a 15 s studio showreel whose cues land on a 120 BPM beat grid

**كيف:** 1920×1080 60 fps on beats b4, b6, b9, b12, b15.8, b21, b24.6, b26 of a 120 BPM grid; Arabic claims «كل إطار برنامج», «نابض، لا منحنى», «الإطار دالة في الزمن». Project files projects/showreel + score.json + cues.json; rendered mp4 kept in kosif-studio/out.

**المعاملات:** 15 s · 60 fps · 8 beat cues

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ريل عرض · showreel · 120 bpm · beats · studio reel · ريل استوديو · عرض أعمال · إيقاع · portfolio · beat grid

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/projects/showreel/index.html:66`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:38`
- `kosif-studio/out/kosif_motion_showreel.mp4`

#### 7. قدرات قريبة في العائلة

- `STORY-60` قوس الريل التحفيزي (FINAL_EDIT) / Motivational talking-reel arc (FINAL_EDIT) (ready)
- `STORY-61` فيلم الإطلاق من الموقع أو الكود / Launch video from a site or codebase (/brag) (ready)
- `STORY-63` فيلم المختبر SHAPE→RANK / Product-lab film (SHAPE → JOINT → LOAD → BREAK → SWAP → RANK) (ready)
- `STORY-64` قصة بلا كلام: مرشد وقفزة / Wordless short: a guide and a leap (ready)

### `STORY-63` — فيلم المختبر SHAPE→RANK / Product-lab film (SHAPE → JOINT → LOAD → BREAK → SWAP → RANK)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فيلم تعليمي بنطاقات مراحل مسماة تقود الرقائق والترجمة والكاميرا والمؤثرات معًا، بعدسة تتوقف عند كل جزء. / An educational film cut into named stage bands that drive chips, captions, camera and effects together.

**متى:** حين تصنع فيلمًا تعليميًا عن منتج بمراحل مسماة (حمل، كسر، استبدال، ترتيب) تقود الكاميرا والتعليقات والمؤثرات / for an educational product film cut into named stage bands that drive camera, captions and effects together

**كيف:** Bands B = {joint .85, load 1.65, brk 2.55, swap 3.35, rank 4.15, end 5.0} (5 s twin), T_BREAK 2.66; load ramps easeInOut to 3.0× then back; 20 s lab: lens stops at 0/3/6.5/9.5/13/16/18 s, fov 30, bilingual callouts, deliberate dip #0f1512 for .6 s. Animation illustrates, it is not proof.

**المعاملات:** stops 0/3/6.5/9.5/13/16/18 s · fov 30

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مختبر · مراحل · lab film · stage bands · educational · structural · فيلم تعليمي · اختبار التحمل · شرح المنتج · stress test · callouts

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:8`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:40`
- `100-superskills/skills/kosif-montage-motion/references/STRUCTURAL_TWIN.md`

#### 7. قدرات قريبة في العائلة

- `STORY-61` فيلم الإطلاق من الموقع أو الكود / Launch video from a site or codebase (/brag) (ready)
- `STORY-62` بنية ريل العرض 15 ث / Showreel beat structure (120 BPM) (ready)
- `STORY-64` قصة بلا كلام: مرشد وقفزة / Wordless short: a guide and a leap (ready)
- `STORY-65` ستة أقواس لأنواع الستيكمان / Stickman six genre arcs (proven)

### `STORY-64` — قصة بلا كلام: مرشد وقفزة / Wordless short: a guide and a leap

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطل يتبع ضوءًا (فراشة) في عالم معادٍ وجميل، يتوقع العقبة، يقفز، يهبط، ويلتفت للجمهور؛ العنوان يتلاشى مبكرًا والشعار في النهاية. / Hero follows a light through a hostile-but-beautiful world, anticipates, leaps, lands, looks back; title early, tagline last.

**متى:** حين تريد فيلمًا قصيرًا بلا حوار عن بطل يتبع ضوءًا ويقفز فوق عقبة وينتهي بسطر الشعار / for a short wordless film where a hero follows a light, leaps an obstacle and ends on a tagline

**كيف:** Beats: walk 0–4.1 s, notice/crouch 4.1–5.2, leap 5.2–6.9, land 6.9–7.35, walk 7.35–9.7, look back 9.7–12; end line from 10.4 s. MIDNIGHT vector short: CinematicCat.sceneSVG(t) per frame, 1280×720, 12 s, 24 fps (288 frames), title fades 2.2–3.2 s, window.render(t) contract.

**المعاملات:** 12 s · 24 fps · 6 beats

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بلا كلام · قصة قصيرة · wordless · silent short · leap · cat · فيلم صامت · بدون حوار · قطة · animated short · no dialogue

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/README.txt:12`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:124`

#### 7. قدرات قريبة في العائلة

- `STORY-62` بنية ريل العرض 15 ث / Showreel beat structure (120 BPM) (ready)
- `STORY-63` فيلم المختبر SHAPE→RANK / Product-lab film (SHAPE → JOINT → LOAD → BREAK → SWAP → RANK) (ready)
- `STORY-65` ستة أقواس لأنواع الستيكمان / Stickman six genre arcs (proven)
- `STORY-66` قوس الحب بخمس نبضات وإطارين / Five-beat love arc with paired frames (proven)

### `STORY-65` — ستة أقواس لأنواع الستيكمان / Stickman six genre arcs

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مضحك، حب، مؤثر، مفاجأة حبكة، كوميديا سوداء، انقلاب الواقع — كل منها بخمس نبضات. / Funny, love, heart-touching, plot twist, dark comedy, surprise — five beats each.

**متى:** حين يطلب المستخدم قصة ستيكمان مضحكة أو رومانسية أو مؤثرة أو بمفاجأة وتحتاج خمس نبضات للنوع / when the user wants a stickman story — funny, love, touching, twist, dark comedy or reality flip — in five beats

**كيف:** genre 1–6 → arcs[genre−1]; beats map to setup/build/turn/peak/payoff (commute misunderstanding, shy small gesture, unseen kindness, bad luck helps, shortcut backfires, reality flips); clips 7 s; lock blocks enforced. Tested by production-profiles tests here.

**المعاملات:** 6 genres × 5 beats · 7 s clips

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ستيكمان · stickman · genres · plot twist · comedy · رجل العصا · كوميديا · مفاجأة · stick figure · short story

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `fastify-motion-bro/scripts/profiles/stickman.mjs:9-17`
- `fastify-motion-bro/tests/production-profiles.test.mjs`

#### 7. قدرات قريبة في العائلة

- `STORY-63` فيلم المختبر SHAPE→RANK / Product-lab film (SHAPE → JOINT → LOAD → BREAK → SWAP → RANK) (ready)
- `STORY-64` قصة بلا كلام: مرشد وقفزة / Wordless short: a guide and a leap (ready)
- `STORY-66` قوس الحب بخمس نبضات وإطارين / Five-beat love arc with paired frames (proven)
- `STORY-67` ملاءمة عدد المقاطع لخطوات الطبخ / Clip-count fitting (food flow) (proven)

### `STORY-66` — قوس الحب بخمس نبضات وإطارين / Five-beat love arc with paired frames

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لقاء، ثقة، بُعد، عودة، وعد حول طائر ورقي؛ لكل نبضة لقطة 35 مم واسعة ولقطة 85 مم عاطفية وسطر سرد. / Meeting, trust, distance, return, promise around a paper-crane motif; each beat a 35 mm wide + 85 mm close-up + one narration line.

**متى:** حين يريد المستخدم قصة حب قصيرة عمودية بخمس نبضات، لكل نبضة لقطة واسعة وأخرى قريبة وسطر سرد / when the user wants a short vertical love story in five beats, each with a wide and a close-up frame plus a narration line

**كيف:** `npm run profile -- start character-romance`; answer "<emotion/setting or DEFAULT>" → 5 scenes × 2 frames = 10 prompts, 9:16. Tested here.

**المعاملات:** 5 × 2 frames · 35 + 85 mm

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حب · رومانسي · romance · paired frames · paper crane · قصة حب · عاطفي · لقطة قريبة · love story · 9:16

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
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `fastify-motion-bro/scripts/profiles/character-romance.mjs:10-29`
- `fastify-motion-bro/skills/character-romance/SKILL.md:12`

#### 7. قدرات قريبة في العائلة

- `STORY-64` قصة بلا كلام: مرشد وقفزة / Wordless short: a guide and a leap (ready)
- `STORY-65` ستة أقواس لأنواع الستيكمان / Stickman six genre arcs (proven)
- `STORY-67` ملاءمة عدد المقاطع لخطوات الطبخ / Clip-count fitting (food flow) (proven)
- `STORY-68` مخرج الفيرال بخمس بوابات / Viral five-stage gated director (proven)

### `STORY-67` — ملاءمة عدد المقاطع لخطوات الطبخ / Clip-count fitting (food flow)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يوزع N مقطعًا على خطوات التحضير الحقيقية: يدمج الخطوات عندما المقاطع قليلة، ويضيف لقطات ماكرو (لمعان، بخار، دوران الطبق، تزيين) عندما كثيرة. / Maps N requested clips onto real preparation steps, merging or adding macro inserts; never repeats an action.

**متى:** حين يطلب المستخدم عددًا محددًا من مقاطع وصفة طبخ وتحتاج توزيعها على خطوات التحضير الحقيقية / when the user asks for a set number of cooking clips that must map onto the real preparation steps

**كيف:** pickStages(food, n): assembly = n−1; chunk or extend; the last clip is always the plated result; 1–200 clips; 10 s clips. Tested (production-profiles).

**المعاملات:** 1–200 clips · 10 s each

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طبخ · food · clips · recipe reel · macro · وصفة طبخ · أكل · خطوات التحضير · cooking · food video

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `fastify-motion-bro/scripts/profiles/food-flow.mjs:62-80`
- `fastify-motion-bro/tests/production-profiles.test.mjs:48-55`

#### 7. قدرات قريبة في العائلة

- `STORY-65` ستة أقواس لأنواع الستيكمان / Stickman six genre arcs (proven)
- `STORY-66` قوس الحب بخمس نبضات وإطارين / Five-beat love arc with paired frames (proven)
- `STORY-68` مخرج الفيرال بخمس بوابات / Viral five-stage gated director (proven)
- `STORY-69` أفلام الدعاء والجمعة / Dua & Friday reels (ready)

### `STORY-68` — مخرج الفيرال بخمس بوابات / Viral five-stage gated director

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 5 عناوين ← سكربت 5 أسطر ← 3 لوحات ← 5 أوامر ملصقات ← 5 أوامر حركة، وكل مرحلة تنتظر رد المستخدم. / 5 titles → 5-line script → 3 palettes → 5 poster prompts → 5 motion prompts, each waiting for the user.

**متى:** حين يريد المستخدم فيديو تحريريًا للانتشار عبر مراحل يختار فيها العنوان والسكريبت والألوان / when the user wants a viral editorial video built in gated stages — titles, script, palettes, poster and motion prompts

**كيف:** `npm run viral -- start \| reply 1..5 \| reply NEXT \| status \| compile \| preview-project \| approve-render`; session projects/viral-editorial/session.json; schema fmb.viral-editorial.v1; 1080×1920 30 fps; 5 ready topics (Attention Trap, Why Saving Money Feels So Hard, Stop Learning Technology the Wrong Way, Real Reason Some Ideas Spread, Motivation Myth). Tested (7/7).

**المعاملات:** 5 stages · 1080×1920 30 fps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فيرال · viral · gated · stages · editorial · انتشار · ترند · خطوة بخطوة · step by step · short video

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
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `fastify-motion-bro/scripts/viral-editorial.mjs:35-46`
- `fastify-motion-bro/tests/viral-editorial.test.mjs`
- `fastify-motion-bro/skills/viral-editorial/SKILL.md:7-13`

#### 7. قدرات قريبة في العائلة

- `STORY-66` قوس الحب بخمس نبضات وإطارين / Five-beat love arc with paired frames (proven)
- `STORY-67` ملاءمة عدد المقاطع لخطوات الطبخ / Clip-count fitting (food flow) (proven)
- `STORY-69` أفلام الدعاء والجمعة / Dua & Friday reels (ready)
- `STORY-70` مونتاج الغربة بمعنى الأغنية / Meaning-matched song montage (Ghorba) (ready)

### `STORY-69` — أفلام الدعاء والجمعة / Dua & Friday reels

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ريل جمعة بلقطات هادئة وسطر ديواني لكل لقطة، وفيلم دعاء الخميس بقلم ذهبي يرسم المحراب وسماء من الليل إلى الفجر. / A Friday reel with calm B-roll and one Diwani line per shot; a Thursday dua film where a gold pen draws a mihrab while the sky turns night to dawn.

**متى:** حين يطلب المستخدم ريل جمعة أو فيديو دعاء هادئًا بخط عربي ولقطات ساكنة أو رسم محراب / when the user wants a calm Friday reel or dua video with Arabic calligraphy lines, quiet B-roll or a drawn mihrab

**كيف:** Friday (mimic rebuild): 28.2 s, 1080×1920 30 fps, 11 shots, 10 fade-black transitions 0.70–0.80 s, text 135 px #fdfbf3 with 7 px #000 stroke. Thursday: 24.7 s, gold pen draws arch + eight-point rosette, mosque silhouette with lit windows, two swaying lanterns, petals and gold dust; AmiriB 84/104/130 px in #fff6e2/#ffd77a/#ffe39a, Aldhabi 170 px day name, sky #0b1033 → #34509a/#f2a079/#ffd890; key line on downbeat 10.987 s with the sun carrier.

**المعاملات:** 28.2 s / 24.7 s · fades 0.7–0.8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دعاء · جمعة · dua · friday · mihrab · islamic · calm · إسلامي · ديني · خط ديواني · جمعة مباركة · religious · calligraphy

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/projects/mimic-jumuah/study/mimic.json`
- `kosif-one/projects/thursday-dua-animation/source/index.html`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### 7. قدرات قريبة في العائلة

- `STORY-67` ملاءمة عدد المقاطع لخطوات الطبخ / Clip-count fitting (food flow) (proven)
- `STORY-68` مخرج الفيرال بخمس بوابات / Viral five-stage gated director (proven)
- `STORY-70` مونتاج الغربة بمعنى الأغنية / Meaning-matched song montage (Ghorba) (ready)
- `STORY-71` مستقبل مصر 2120: خطاف وقاعدة تراث / Egypt 2120: one-second concept + heritage rule (ready)

### `STORY-70` — مونتاج الغربة بمعنى الأغنية / Meaning-matched song montage (Ghorba)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مونتاج عمودي 48 ث عن الغربة: سبعة مقاطع بترتيب عاطفي تحت الأغنية الأصلية، تدرج باهت، وعنوان ASS لكل لقطة. / A 48 s vertical montage about living abroad: seven clips in emotional order under the untouched song, muted grade, per-shot ASS titles.

**متى:** حين يريد المستخدم مونتاجًا على أغنية بترتيب اللقطات حسب معناها العاطفي مع ترك الأغنية كما هي / when montaging clips to a song in emotional order by its meaning, keeping the song untouched

**كيف:** Exile order: departure (plane window 6.8 s) → goodbye (airport 5.2) → foreign streets (night drive 7.0) → memory (rain on glass 5.0) → loneliness (walking in rain 7.6) → family voices (6.8) → hope (sunrise from plane 9.6). 540×960 or 720×1280, 24 fps, contrast 1.06–1.08, saturation 0.86–0.95; concat demuxer, song muxed untouched. 18-step reuse runbook: inspect, transcribe with review, pitch 2–3 ideas, source footage (20–35 clean vertical shots for a full song), triage, beat/meaning shot list, Arabic motion type, export 9:16 and 16:9 on request.

**المعاملات:** 7 shots / 48 s · 24 fps · sat 0.86–0.95

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غربة · أغنية · montage · song · emotional order · exile · سفر · حنين · مونتاج أغنية · music video · vertical

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:19-27`
- `kosif-one/projects/KOSIF_Motion_Ghorba/MONTAGE_REUSE_RUNBOOK_AR.md`

#### 7. قدرات قريبة في العائلة

- `STORY-68` مخرج الفيرال بخمس بوابات / Viral five-stage gated director (proven)
- `STORY-69` أفلام الدعاء والجمعة / Dua & Friday reels (ready)
- `STORY-71` مستقبل مصر 2120: خطاف وقاعدة تراث / Egypt 2120: one-second concept + heritage rule (ready)
- `STORY-72` شرح «تعريفان للنجاح» على لوحات مولدة / Two-definitions-of-success voice explainer (ready)

### `STORY-71` — مستقبل مصر 2120: خطاف وقاعدة تراث / Egypt 2120: one-second concept + heritage rule

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** افتح على المفهوم في ثانية بسؤال، وكل لقطة تضيف حقيقة برقاقة مرقمة، وختام بسطر وإخلاء «تصور فني تخيلي»؛ والأهرامات الحقيقية لا تُمس. / Open on the concept in a second, each shot adds one fact with a numbered chip, end with one line + disclaimer; real monuments stay untouched.

**متى:** حين تصنع فيديو تخيليًا عن المستقبل حول معالم حقيقية كالأهرامات مع رقائق حقائق وإخلاء «تصور فني» / for a speculative future video around real monuments like the pyramids, with fact chips and an artistic-concept disclaimer

**كيف:** Hook 0–2.6 s («مصر ٢١٢٠» + «كيف سنعيش بعد مئة عام؟»), chips «٠١ · الجيزة» …, captions start 0.25 s after each cut and leave 0.3 s before the next, 18 s total. Heritage: Khufu, Khafre, Menkaure at 1:5 in their real diagonal (ConeGeometry(base/√2, h, 4) rotated 45°, stone #E3BC86) — futurism around them, never on them.

**المعاملات:** 18 s · captions +0.25 s / −0.3 s · scale 1:5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مصر · أهرامات · heritage · speculative · disclaimer · chips · المستقبل · تراث · خيال علمي · futuristic · pyramids

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/projects/egypt-2120-animation/index.html:448-453`
- `kosif-one/projects/egypt-2120-animation/index.html:218-221`

#### 7. قدرات قريبة في العائلة

- `STORY-69` أفلام الدعاء والجمعة / Dua & Friday reels (ready)
- `STORY-70` مونتاج الغربة بمعنى الأغنية / Meaning-matched song montage (Ghorba) (ready)
- `STORY-72` شرح «تعريفان للنجاح» على لوحات مولدة / Two-definitions-of-success voice explainer (ready)
- `STORY-73` أشكال فيديو صانع المحتوى / Creator-video shapes & faceless VO (documented)

### `STORY-72` — شرح «تعريفان للنجاح» على لوحات مولدة / Two-definitions-of-success voice explainer

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرح صوتي 47 ث: سؤال بعلامة استفهام ضخمة، قاعة ألف شخص، عالم المال البارد يبهت للرمادي عند «غير سعيد»، وعالم ذهبي دافئ. / A 47 s voice explainer on generated plates: giant outlined question mark, a hall of 1,000 people, a cold money world draining to grey, a warm golden world.

**متى:** حين تحتاج شرحًا صوتيًا عن معنى النجاح يقابل عالم المال البارد بعالم ذهبي دافئ على لوحات مولّدة / for a voice-led explainer about the meaning of success contrasting a cold money world with a warm golden one

**كيف:** GSAP + Motion Kit composition with three text levels; base #05070b, gold #f5c97a, cold #7fd0ff, alarm #ff6b6b, cream #e9dcc4; synthesised 90 BPM D-minor score (vol .42) under the voice with designed SFX cues; 1080×1920 30 fps.

**المعاملات:** 47 s · 90 BPM · 3 text levels

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نجاح · تنمية · explainer · voice · cold warm · question mark · تعليق صوتي · مال وسعادة · مقارنة · success · gsap

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
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/projects/whatsapp-motion/projects/success/index.html`

#### 7. قدرات قريبة في العائلة

- `STORY-70` مونتاج الغربة بمعنى الأغنية / Meaning-matched song montage (Ghorba) (ready)
- `STORY-71` مستقبل مصر 2120: خطاف وقاعدة تراث / Egypt 2120: one-second concept + heritage rule (ready)
- `STORY-73` أشكال فيديو صانع المحتوى / Creator-video shapes & faceless VO (documented)
- `STORY-74` قواعد مونتاج المدينة / City montage shot grammar (documented)

### `STORY-73` — أشكال فيديو صانع المحتوى / Creator-video shapes & faceless VO

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الاختبار (نفس المهمة بطريقتين)، المهمة الحقيقية، اليوم، الشاشة الموجّهة — ومونتاج صوتي بلا وجه يُفحص بكاشف وجوه. / The Test, The Real Task, The Day, The Guided Screen — and faceless VO edits verified by a face detector.

**متى:** حين يريد صانع محتوى شكلًا لفيديو مثل الاختبار أو اليوم، أو فيديو بتعليق صوتي دون إظهار الوجه / when a creator needs a video shape (The Test, The Day) or a faceless voice-over edit checked for faces

**كيف:** Choose the shape the footage can actually prove; never stage results; record each beat twice (precise + natural), lens near eye level, leave caption/UI space. Faceless: V1 screen recordings and face-free B-roll, voice A1, cards V2, captions V3; sample 1 fps frames through a face detector and replace flagged segments. Transcript-first assembly: inventory (file, camera, face flag, length, sentence count, gist) → beat sheet from what was actually said (voice clip = speech >50%) → approval → timeline.

**المعاملات:** 2 takes / beat · 1 fps face check

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صانع محتوى · بلا وجه · creator · faceless · transcript first · b-roll · بدون وجه · يوتيوبر · تسجيل شاشة · screen recording · voiceover

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/101-video-skills/214-creator-video/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-71` مستقبل مصر 2120: خطاف وقاعدة تراث / Egypt 2120: one-second concept + heritage rule (ready)
- `STORY-72` شرح «تعريفان للنجاح» على لوحات مولدة / Two-definitions-of-success voice explainer (ready)
- `STORY-74` قواعد مونتاج المدينة / City montage shot grammar (documented)
- `STORY-75` معرض قوالب الأفلام (52) وقوالب البداية / Film template gallery (52) & starter briefs (install)

### `STORY-74` — قواعد مونتاج المدينة / City montage shot grammar

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** افتح على شارع/مرور/لافتات/ضوء، بدّل بين الواسع والمتوسط والتفاصيل، واربط اتجاه الحركة عبر القطعات على ضربات الإيقاع. / Open on establishing street/traffic/signage/light, alternate wide, mid and detail, chain motion direction across cuts on downbeats.

**متى:** عند مونتاج لقطات مدينة أو سفر على الإيقاع وتريد ترتيب الواسع والمتوسط والتفاصيل وربط اتجاه الحركة / when editing city or travel footage to music, alternating wide, mid and detail shots and matching motion direction

**كيف:** Shot list tagged wide/medium/detail with motion vectors (train passes, camera moves, water); cut to downbeats from a beat map. Travel-note captions: place, time and mood ("9 AM, market alley"), commas only, chapter title bottom-left 0.5 s after scene start for 3 s, ≤2 lines, ≈18 chars/line, bottom margin 8%.

**المعاملات:** captions ≤2 lines · 18 chars · margin 8%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مدينة · سفر · city montage · travel · shot grammar · downbeats · فلوج سفر · لقطات الشارع · أحجام اللقطات · travel vlog · beat cuts

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2433-akbun-davinciresolve-cut-new-york/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-72` شرح «تعريفان للنجاح» على لوحات مولدة / Two-definitions-of-success voice explainer (ready)
- `STORY-73` أشكال فيديو صانع المحتوى / Creator-video shapes & faceless VO (documented)
- `STORY-75` معرض قوالب الأفلام (52) وقوالب البداية / Film template gallery (52) & starter briefs (install)
- `STORY-76` لوحات المشهد المرسوم وموجّه الرسم / Painted-scene showcases & drawing request router (ready)

### `STORY-75` — معرض قوالب الأفلام (52) وقوالب البداية / Film template gallery (52) & starter briefs

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 52 بريفًا أصليًا في 7 أنواع عربية بخانات للموضوع والسطر والرقم — والملء لا يخترع أرقامًا؛ وثلاثة قوالب بداية في Workbench. / 52 original brief templates in 7 Arabic genres with slots for subject, line and figure; three Workbench starter briefs.

**متى:** حين يريد المستخدم البدء من قالب فيلم جاهز (ريل، إطلاق، شرح…) بخانات للموضوع والسطر والرقم / when the user wants to start from a ready film brief template — showreel, launch, explainer — with slots to fill

**كيف:** Basma TPL: showreels (reel-designer 15 s, reel-type 12, logo-sting 5 …), launch (app-launch 15, saas-promo 15, pricing 12, milestone 8, dashboard-reveal 12 …), explainers and more; per-style script contracts (plotter 4–7 lines of 2–5 words; doodle 4–8 sentences with «dialogue»; whiteboard 4–6 steps; stickman 4–7 lines with a twist; infographic 3–6 lines with one real figure each). Workbench GET /api/templates: kinetic «حروف وحركة» #a7e8d0, cinematic «لقطة سينمائية» #d3c0fa, montage «مونتاج بإيقاع» #f5ce91.

**المعاملات:** 52 templates · 7 genres

**التثبيت:** cd app && npm install

**الوسوم:** قوالب · templates · gallery · starter · script contract · قالب جاهز · نماذج · بداية سريعة · brief templates · presets

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
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `app/public/js/00_editor.js:1777`
- `app/public/js/10_studio.js:913`
- `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:24`

#### 7. قدرات قريبة في العائلة

- `STORY-73` أشكال فيديو صانع المحتوى / Creator-video shapes & faceless VO (documented)
- `STORY-74` قواعد مونتاج المدينة / City montage shot grammar (documented)
- `STORY-76` لوحات المشهد المرسوم وموجّه الرسم / Painted-scene showcases & drawing request router (ready)
- `STORY-77` كتاب العالم والكائنات الأصلية / Creature & world-bible kit (documented)

### `STORY-76` — لوحات المشهد المرسوم وموجّه الرسم / Painted-scene showcases & drawing request router

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** برامج لوحات خيالية (فتاة وتنين، حوت وتنين في عاصفة، بطة تهاجم تنينًا) وموجّه يحدد أي كود لأي طلب رسم. / Fantasy painting programs and a router mapping each drawing ask to a pipeline.

**متى:** حين يطلب المستخدم رسم صورة كما هي أو لوحة سينمائية من وصف أو مشهدًا ثلاثي الأبعاد أو فيلمًا للرسم / when a drawing request must be routed — copy an image as code, a cinematic painting, a 3D scene or a painter film

**كيف:** Router: "draw this image as is / give me its code" → to_python; cinematic painting from a prompt → KOSIF scene + judge; realistic 3D/reflections → Three.js page; film of the drawing → painter film. Recipe: value before colour (range >150/255), three lights (cool key, warm key, dim ambient) each with rim, aerial depth (screen fill blur 30 at 0.2), then grade/vignette/grain; brief as must-show elements + light sources + prohibitions, built back to front. whale_dragon passes its judge test (letterbox 62/738); dragon_girl sky #05071a → #8c3a2e, 280 stars.

**المعاملات:** value range >150 · 3 lights + rims

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لوحة · رسم · painting · dragon · drawing router · painted realism · رسمة · تنين · لوحة خيالية · fantasy art · three.js

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
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/references/drawing-guide.md:6`
- `kosif-studio/scenes/whale_dragon.py:1`
- `kosif-studio/scenes/dragon_girl.py:129`

#### 7. قدرات قريبة في العائلة

- `STORY-74` قواعد مونتاج المدينة / City montage shot grammar (documented)
- `STORY-75` معرض قوالب الأفلام (52) وقوالب البداية / Film template gallery (52) & starter briefs (install)
- `STORY-77` كتاب العالم والكائنات الأصلية / Creature & world-bible kit (documented)
- `STORY-78` توليد أفكار بعشوائية حقيقية / Lateral ideation with real randomness (ready)

### `STORY-77` — كتاب العالم والكائنات الأصلية / Creature & world-bible kit

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قوالب لكائنات وعوالم أصلية: بطاقة كائن (الندرة، البيئة، الصورة الظلية، الحركة المميزة، التطور، نقطة الضعف) وكتاب عالم. / Templates for original creatures and world bibles — no trademarked characters.

**متى:** حين يريد المستخدم ابتكار كائنات أو عالم خيالي أصلي ببطاقات ندرة وبيئة وحركة مميزة / when designing original creatures or a fantasy world bible with rarity, biome and signature moves, no trademarked characters

**كيف:** 19 element types; rarity Common 60 / Uncommon 25 / Rare 10 / Epic 4 / Legendary 0.9 / Mythical 0.1 %; 8 biomes; creature card: name, type, rarity, biome, silhouette + 3 features, palette, signature move + VFX, evolution trigger, weakness, lore hook, 7-layer prompt + CHR code; world bible: premise, map zones, factions, magic/tech limits, economy, conflicts, 5 LOC + 5 CHR. Anime shot grammar (observed): intro each unit → launch → transform → close-ups → pose.

**المعاملات:** rarity 60/25/10/4/0.9/0.1 % · 8 biomes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كائنات · عالم · creature · world bible · fantasy · lore · وحوش · عالم خيالي · تصميم كائنات · character design · rarity

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/creative-worlds.md`
- `style:pm-allforbigfire-86ff3c`

#### 7. قدرات قريبة في العائلة

- `STORY-75` معرض قوالب الأفلام (52) وقوالب البداية / Film template gallery (52) & starter briefs (install)
- `STORY-76` لوحات المشهد المرسوم وموجّه الرسم / Painted-scene showcases & drawing request router (ready)
- `STORY-78` توليد أفكار بعشوائية حقيقية / Lateral ideation with real randomness (ready)
- `STORY-79` استخراج القصص والنُّقَط من النص / Story-mine & transcript nuggets (documented)

### `STORY-78` — توليد أفكار بعشوائية حقيقية / Lateral ideation with real randomness

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمات محفزة عشوائية فعلًا وأوامر استفزاز لتفلت من الأفكار المتوقعة؛ أو 100 فكرة عبر 10 اتجاهات ثم تصفية. / Genuinely random stimulus words and provocation prompts; or 100 ideas across 10 directions, then filter.

**متى:** حين تحتاج أفكارًا غير متوقعة وتريد محفزات عشوائية فعلًا وأوامر استفزاز أو 100 فكرة ثم تصفية / when you need unexpected ideas and want genuinely random stimuli, provocations or 100 ideas followed by a filter

**كيف:** kosif_ideate {problem, concepts[], n ≤30, seed} → definition checklist, n stimuli with contiguity/similarity/contrast prompts, concept challenges, provocation operators, stage-2 filter (reproducible seed). 100-ideas skill: reverse, combine, constrain, exaggerate, swap audience… Idea tiering: 15–20 raw ideas via gap analysis, trend riding, format innovation, audience questions; 60–70% growth tier; each with working title, angle, timeliness. Discovery intent per idea: search (front-load the answer, real query phrasing) vs browse (opening + thumbnail pattern-break) — no discovery logic, no idea yet.

**المعاملات:** n ≤30 · 15–20 ideas · 60–70% tier 1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أفكار · عصف ذهني · ideation · random stimuli · brainstorm · 100 ideas · أفكار جديدة · إبداع · فكرة فيديو · creativity · idea generation

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-think-pro/scripts/ideate.py`
- `100-superskills/skills/ideation-100-ideas/SKILL.md`
- `kosif-atlas/skills/1817-youtube-strategy/4866-yt-ideation/SKILL.md`
- `kosif-atlas/skills/1520-digital-marketing-pro/4132-video-packaging/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-76` لوحات المشهد المرسوم وموجّه الرسم / Painted-scene showcases & drawing request router (ready)
- `STORY-77` كتاب العالم والكائنات الأصلية / Creature & world-bible kit (documented)
- `STORY-79` استخراج القصص والنُّقَط من النص / Story-mine & transcript nuggets (documented)
- `STORY-80` العناوين: التوتر الصادق وخمسة اختبارات / Titles: honest charge & five tests (documented)

### `STORY-79` — استخراج القصص والنُّقَط من النص / Story-mine & transcript nuggets

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** القصة المعاشة تخفي: الدرس، الرأي المخالف، الإطار، الدليل، اللحظة القريبة؛ والتفريغ يعطي 15–25 نقطة بثلاثة مرشحات. / A lived story hides lesson, contrarian take, framework, proof and relatable moment; a transcript yields 15–25 nuggets via three filters.

**متى:** حين تريد استخراج نقاط واقتباسات من تفريغ نصي أو قصة شخصية لتحويلها إلى مقاطع قصيرة / when mining a transcript or lived story for 15–25 nuggets to turn into short clips and quote cards

**كيف:** Filters: what surprised, what challenged an assumption, what you would repeat over coffee; provisional headline + signal per nugget; pick 2–4 for clips and animated quote cards. Lead drafts with the surprise, number or reversal — never chronology ("بدأ الأمر عندما…"); never improve facts; anonymise client details by default.

**المعاملات:** 15–25 nuggets · pick 2–4 · 5 angle types

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقاط · تفريغ · nuggets · story mine · quote cards · angles · اقتباسات · مقاطع قصيرة · قصة شخصية · clips · transcript

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1181-transcript-to-content-pipeline/2789-transcript-to-content-pipeline/instructions.md`
- `kosif-atlas/skills/1520-digital-marketing-pro/4122-story-mine/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-77` كتاب العالم والكائنات الأصلية / Creature & world-bible kit (documented)
- `STORY-78` توليد أفكار بعشوائية حقيقية / Lateral ideation with real randomness (ready)
- `STORY-80` العناوين: التوتر الصادق وخمسة اختبارات / Titles: honest charge & five tests (documented)
- `STORY-81` خريطة الدعوة للفعل / CTA placement map (documented)

### `STORY-80` — العناوين: التوتر الصادق وخمسة اختبارات / Titles: honest charge & five tests

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** العنوان القوي يعبّر عن توتر حقيقي (متوقع مقابل فعلي، وعد مقابل كلفة)، ويمر بخمسة اختبارات: يكمل «أريد ___»، وضوح فوري، طاقة إيجابية، لغة الجمهور، يُعاد شفهيًا. / Strong titles express a true tension and pass five tests.

**متى:** حين تكتب عنوان فيديو وتريد عنوانًا جذابًا صادقًا يعبّر عن توتر حقيقي ويمر بخمسة اختبارات / when writing a video title that carries an honest tension and passes five tests, without clickbait

**كيف:** State 2–4 charges plainly, generate 10–20 raw candidates, keep 3–5 with the supporting fact; cut words until cutting removes truth. Strategy families: direct benefit, honest curiosity gap, authority, trending/urgency; 5–10 titles <60 chars labelled by strategy. Weak priors only: numbers, concreteness and individual stories lift clicks; ≈2.3% CTR per negative word is not a licence for fear. Arabic copy: PAS / AIDA / 4U, 10 headlines → pick 3, one CTA, consistent dialect, Arabic punctuation.

**المعاملات:** 10–20 raw → 3–5 · <60 chars

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عناوين · titles · headline · ctr · copywriting · arabic copy · عنوان الفيديو · عنوان جذاب · نسبة النقر · video title · click-through

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/2218-majestic-writing/8393-headline-generator/SKILL.md`
- `kosif-atlas/skills/3067-youtube/13227-creator-seo-agent/SKILL.md`
- `kosif-atlas/skills/1817-youtube-strategy/4868-yt-packaging/SKILL.md`
- `100-superskills/skills/arabic-copywriting/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-78` توليد أفكار بعشوائية حقيقية / Lateral ideation with real randomness (ready)
- `STORY-79` استخراج القصص والنُّقَط من النص / Story-mine & transcript nuggets (documented)
- `STORY-81` خريطة الدعوة للفعل / CTA placement map (documented)
- `STORY-82` الغلاف يبدأ من النفس لا من الصورة / Psychology-first thumbnail brainstorm (documented)

### `STORY-81` — خريطة الدعوة للفعل / CTA placement map

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** القصير: دعوة واحدة عند الذروة الطبيعية؛ الطويل: دعوة ناعمة في المنتصف وقوية في آخر 60 ث، عبر الكلام والشاشة وبطاقة النهاية والتعليق المثبت. / Short: one CTA at the climax; long: soft mid-roll + strong end within the last 60 s.

**متى:** حين تحدد أين تضع الدعوة للفعل في فيديو قصير أو طويل: عند الذروة أو في المنتصف وآخر دقيقة / when deciding where to place calls to action in short or long videos — at the climax, mid-roll or the final minute

**كيف:** Mark CTA cues on the timeline with rationale; the end card is a reusable component held long enough to read; one offer, one audience, one action.

**المعاملات:** short 1 CTA · long mid + end ≤60 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دعوة · cta · call to action · end card · conversion · دعوة للفعل · بطاقة النهاية · تعليق مثبت · pinned comment · mid-roll

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`
- `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-79` استخراج القصص والنُّقَط من النص / Story-mine & transcript nuggets (documented)
- `STORY-80` العناوين: التوتر الصادق وخمسة اختبارات / Titles: honest charge & five tests (documented)
- `STORY-82` الغلاف يبدأ من النفس لا من الصورة / Psychology-first thumbnail brainstorm (documented)
- `STORY-83` أعمدة المحتوى والتقويم / Content pillars & publishing calendar (proven)

### `STORY-82` — الغلاف يبدأ من النفس لا من الصورة / Psychology-first thumbnail brainstorm

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ابدأ بما يجب أن يتساءل عنه المشاهد ويشعر به: 2–3 أسئلة، 1–2 عاطفة، مشكلة في عبارة واحدة كبطل، ثم 2–3 اتجاهات. / Start from what the viewer should wonder and feel: 2–3 questions, 1–2 emotions, the problem as hero, then 2–3 directions.

**متى:** حين تصمم صورة غلاف لفيديو وتريد البدء من السؤال والعاطفة التي يجب أن يشعر بها المشاهد / when designing a video thumbnail starting from the question and emotion the viewer should feel, then 2–3 directions

**كيف:** Emotions: curiosity, unease, trust, vulnerability, surprise; turn each direction into an HTML/CSS layout and render variants with Playwright at 1280×720.

**المعاملات:** 2–3 questions · 1–2 emotions · 1280×720

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غلاف · نفسية · thumbnail · emotion · curiosity · صورة مصغرة · ثمنيل · تصميم الغلاف · cover · playwright

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
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-atlas/skills/1101-akbun-writing/2486-akbun-thumbnail-review/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-80` العناوين: التوتر الصادق وخمسة اختبارات / Titles: honest charge & five tests (documented)
- `STORY-81` خريطة الدعوة للفعل / CTA placement map (documented)
- `STORY-83` أعمدة المحتوى والتقويم / Content pillars & publishing calendar (proven)
- `STORY-84` موجة الموشن 2026: أنماط الطلب والميزانيات / Motion-wave prompt patterns & effort budgets (documented)

### `STORY-83` — أعمدة المحتوى والتقويم / Content pillars & publishing calendar

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خليط أعمدة (رؤى 30%، كواليس 25%، تعليم 25%، شخصي 15%، ترويج 5%) يوزَّع بالأوزان على المنصات والأيام إلى تقويم يُستورد كتذكيرات. / A pillar mix spread by weight across platforms and allowed days into an importable calendar.

**متى:** حين يريد المستخدم خطة نشر على السوشيال ميديا بأعمدة محتوى موزعة على المنصات والأيام في تقويم / when the user wants a social posting plan with weighted content pillars spread across platforms and days

**كيف:** `python3 social.py calendar plan.json --out DIR` → calendar.csv/.xlsx/.md/.ics (ran here on the example plan). Promotion above ~20% reduces reach; 3–5 pillars each tied to a metric; plan one motion template series per pillar so cost per post drops.

**المعاملات:** 30/25/25/15/5 % · CSV/XLSX/MD/ICS

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أعمدة المحتوى · تقويم · pillars · calendar · ics · series · خطة محتوى · جدول نشر · سوشيال ميديا · content plan · social media

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `100-superskills/skills/kosif-social/scripts/social.py:471`
- `kosif-one/tools/kosif-social/examples/plan.json`
- `kosif-atlas/skills/192-marketing-skills/611-social-content/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-81` خريطة الدعوة للفعل / CTA placement map (documented)
- `STORY-82` الغلاف يبدأ من النفس لا من الصورة / Psychology-first thumbnail brainstorm (documented)
- `STORY-84` موجة الموشن 2026: أنماط الطلب والميزانيات / Motion-wave prompt patterns & effort budgets (documented)
- `STORY-85` وكلاء الإبداع الفرعيون وقرارات Jev / Creative sub-agents & Jev decisions (key)

### `STORY-84` — موجة الموشن 2026: أنماط الطلب والميزانيات / Motion-wave prompt patterns & effort budgets

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خمسة أنماط طلب نجحت: ريل بسطر واحد، أشِر إلى رابط علامة، سمِّ لوكًا ومرجعًا، مواصفة XML، بريف مخرج طويل ببوابات — مع توقعات واقعية للوقت والكلفة. / Five prompt patterns that worked, with realistic time/cost expectations.

**متى:** حين يسأل المستخدم كيف يصيغ طلب موشن ناجحًا أو كم من الوقت والكلفة يحتاج، بأنماط طلب نجحت / when the user asks how to phrase a motion request that works, or what time and cost to expect

**كيف:** Corpus 3,984 posts / 203M views: 3D 487 posts 52.0M, seek(t) 70 / 34.9M, UI 217 / 16.3M, Arabic only 11 / 0.13M — Arabic motion done right is open ground. Patterns: one-liner showreel (~15 s); brand URL with real assets + music; name a look + reference (frame every 0.5 s → style_guide.md); XML spec (<inputs> <direction> <structure> at 120 BPM <build> <gotchas> <start>); long brief 9.5k–19k chars with a payoff every 3–5 s and gates plan → stills → animatic → pass → polish → audio → render. Budgets: median 20 min (p90 57) for a short clip from one prompt; median 4 h for celebrated pieces; median $10 in tokens (p90 $200).

**المعاملات:** 3,984 posts · 20 min / 4 h medians

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترند · أنماط الطلب · trend · prompt patterns · effort · budget · كتابة الطلب · تكلفة · وقت التنفيذ · how to prompt · cost

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-studio/motion/references/x-trend-2026.md`
- `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### 7. قدرات قريبة في العائلة

- `STORY-82` الغلاف يبدأ من النفس لا من الصورة / Psychology-first thumbnail brainstorm (documented)
- `STORY-83` أعمدة المحتوى والتقويم / Content pillars & publishing calendar (proven)
- `STORY-85` وكلاء الإبداع الفرعيون وقرارات Jev / Creative sub-agents & Jev decisions (key)
- `STORY-P01` عشرون وصفة أسلوب موشن بمحركاتها / 20 motion style recipes (S01–S20) with engine candidates (documented)

### `STORY-85` — وكلاء الإبداع الفرعيون وقرارات Jev / Creative sub-agents & Jev decisions

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شخصيات وكلاء جاهزة (مخرج سينمائي، منتج فيديو بفحص إطار بإطار، مصمم إضاءة، مهندس صوت، ناقد بصري، راوي) ومحرك قرار يعطي احتمالًا لكل خيار. / Ready sub-agent personas and a decision engine that gives each option a probability.

**متى:** حين تريد توزيع العمل على وكلاء متخصصين كمخرج سينمائي ومهندس صوت وناقد بصري، أو ترجيح خيار باحتمال / when delegating to specialist agent personas — director, sound engineer, critic — or scoring options by probability

**كيف:** Launch via the Agent tool as kosif-omni:<agent>; each delegates to inner roles (prompt engineer, camera-move expert, rhythm expert, frame consistency, edit director, Arabic captions engineer). Jev (owner service) scored design choices, e.g. IBM Plex Sans Arabic p=0.99, ram emblem 0.97; combine-route thresholds 0.6/0.4. Owner-built planning skills (curriculum, research with citations, red-team pre-mortem, market research, decks) support the video job as instruction-only playbooks.

**المعاملات:** p_yes 0.6 / 0.4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وكلاء · subagents · jev · decision · roles · مخرج · توزيع المهام · فريق وكلاء · personas · agents

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `kosif-one/tools/kosif-omni/agents/kosif-video-producer.md`
- `kosif-one/tools/kosif-omni/agents/kosif-cinema-director.md`
- `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`
- `100-superskills/skills/red-team-premortem/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-83` أعمدة المحتوى والتقويم / Content pillars & publishing calendar (proven)
- `STORY-84` موجة الموشن 2026: أنماط الطلب والميزانيات / Motion-wave prompt patterns & effort budgets (documented)
- `STORY-P01` عشرون وصفة أسلوب موشن بمحركاتها / 20 motion style recipes (S01–S20) with engine candidates (documented)
- `STORY-P02` الإحاطة السينمائية بثماني خانات / Eight-slot cinematic brief (PRODUCT → … → OUTPUT) (documented)

### `STORY-P01` — عشرون وصفة أسلوب موشن بمحركاتها / 20 motion style recipes (S01–S20) with engine candidates

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner package (own work) |

**ما هي:** قائمة أصلية بعشرين أسلوبًا، لكل واحد هدف بصري ومحركات مرشحة ومعاينة مفهومية مربوطة؛ للاختيار السريع لا كإثبات تنفيذ. / An original list of 20 styles, each with a visual goal, candidate engines and a linked concept preview — for quick choice, not proof of execution.

**متى:** حين تريد اختيارًا سريعًا بين عشرين أسلوب موشن (جسيمات، نيون، سلكي ثلاثي الأبعاد…) مع المحركات المرشحة / when picking quickly among 20 motion styles — particles, neon, wireframe 3D — with candidate engines for each

**كيف:** S01 particles (Pixi/Three/Canvas, A24) · S02 liquid-morph (Flubber/GLSL/SVG, A13) · S03 holographic (Three/OGL/Blender, A36) · S04 neon-glow (SVG/Canvas/FFmpeg, A03) · S05 wireframe-3d exploded parts (Three/Blender, A31) · S06 glassmorphism (CSS/Three, A34) · S07 kinetic-type word by word, Arabic shaped (Remotion/SVG/HarfBuzz, A08) · S08 isometric process (SVG/Three, A32) · S09 clay-3d (Blender/Three, A35) · S10 ascii terminal (Canvas/SVG, A10) · S11 gradient-mesh (GLSL/OGL, A28) · S12 comic-book panels with camera moves (SVG/Remotion, A41) · S13 split-flap stats (Canvas/Remotion, A19) · S14 retro-vhs (FFmpeg/GLSL, A49) · S15 halftone (Canvas/GLSL, A25) · S16 bauhaus primitives (D3/SVG/Motion Canvas, A17) · S17 pixel-art grid (Canvas/Pixi, A51) · S18 blueprint (SVG/Manim/Blender, A02) · S19 art-deco metallic ornament (SVG/Canvas, A23) · S20 neo-brutalism blocks (HTML/CSS/Remotion, A09). Every linked preview is flagged example_is_exact_style=false. Source: distilled from the owner-supplied Google Doc (Tyler Mommsen, motion-graphics prompts). For build numbers open the matching existing powers (e.g. TYPE-35 split-flap, SHAPE-73 bauhaus, RETRO-33 ascii, 3D-106 isometric).

**المعاملات:** 20 presets · fields id, slug, name_ar, visual_goal, engine_candidates, example_reference_id

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** style presets · styles · وصفات أسلوب · أساليب · art deco · holographic · blueprint · split-flap · أسلوب موشن · جسيمات · نيون · particles · neon

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `blender` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- `npm:p5` ← npm ls p5 أو وجود node_modules/p5
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-P01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

#### 6. الأدلة

- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/STYLE_PRESETS_20.json`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/style_gallery.html`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/GOOGLE_DOC_DISTILLATION.md`

#### 7. قدرات قريبة في العائلة

- `STORY-84` موجة الموشن 2026: أنماط الطلب والميزانيات / Motion-wave prompt patterns & effort budgets (documented)
- `STORY-85` وكلاء الإبداع الفرعيون وقرارات Jev / Creative sub-agents & Jev decisions (key)
- `STORY-P02` الإحاطة السينمائية بثماني خانات / Eight-slot cinematic brief (PRODUCT → … → OUTPUT) (documented)
- `STORY-P03` قاموس تحويل وصف الهواة إلى أوامر حركة / Amateur → pro motion lexicon (adjective → code direction) (documented)

### `STORY-P02` — الإحاطة السينمائية بثماني خانات / Eight-slot cinematic brief (PRODUCT → … → OUTPUT)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner package (own work) |

**ما هي:** قبل أي كود اكتب الإحاطة في ثماني خانات ثابتة حتى لا يبقى قرار بصري أو صوتي مفتوحًا. / Before any code, fill eight fixed slots so no visual or sound decision stays open.

**متى:** حين تحتاج قبل أي كود إحاطة بثماني خانات تحسم القصة والمقاس والشكل والحركة والصوت والمخرجات / when you need an eight-slot brief before any code, fixing story, format, look, motion, sound, quality and output

**كيف:** PRODUCT/TOPIC → STORY → FORMAT (aspect, duration, fps) → LOOK (hex colours, fonts, camera angle) → MOTION (easing family, transitions, the one continuous thread object — see STORY-175) → SOUND (who is the master clock: the voice if there is speech; real beat map, never an assumed 120 BPM) → QUALITY (acceptance list) → OUTPUT (files, codecs, editable source). Then choose the engine: UI/logo/type in React → Remotion; DOM-seekable → HyperFrames; diagrams/maths → Motion Canvas or Manim; real 3D camera → Three.js/Blender after a GPU check; existing footage → FFmpeg + ffprobe + scene detect/ASR; photoreal generated shots → an external generator that is actually available.

**المعاملات:** 8 slots · hex colours required · voice = master clock

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** brief · creative brief · إحاطة · تخطيط · engine choice · بريف · خطة الفيلم · مواصفات · spec · master clock

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `blender` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-P02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

#### 6. الأدلة

- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/GOOGLE_DOC_DISTILLATION.md`

#### 7. قدرات قريبة في العائلة

- `STORY-85` وكلاء الإبداع الفرعيون وقرارات Jev / Creative sub-agents & Jev decisions (key)
- `STORY-P01` عشرون وصفة أسلوب موشن بمحركاتها / 20 motion style recipes (S01–S20) with engine candidates (documented)
- `STORY-P03` قاموس تحويل وصف الهواة إلى أوامر حركة / Amateur → pro motion lexicon (adjective → code direction) (documented)
- `STORY-U01` خط فيلم الأغنية الكرتوني / Cartoon music-video pipeline (documented)

### `STORY-P03` — قاموس تحويل وصف الهواة إلى أوامر حركة / Amateur → pro motion lexicon (adjective → code direction)

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner package (own work) |

**ما هي:** يحوّل كلمات مثل «ناعم» و«متتابع» و«مع الإيقاع» إلى تعليمات قابلة للبرمجة، مع متى لا تُستخدم. / Turns words like "smooth", "staggered" or "on the beat" into programmable instructions, with when not to use them.

**متى:** حين يستخدم المستخدم كلمات عامة مثل «ناعم» أو «متتابع» أو «مع الإيقاع» وتحتاج تحويلها لتعليمات حركة / when the user says vague words like smooth, staggered or on the beat and you must turn them into programmable motion

**كيف:** smooth → closed-form damped spring or cubic-bezier(0.16,1,0.3,1), bounded overshoot (not everything needs a spring) · staggered → overlapping timeline with measured offsets synced to voice/beat, not a hard-coded 125 ms · alive hold → bounded micro-motion that never hurts reading · on the beat → detected onsets from the real audio · motion blur → sub-frame sampling (tmix over whole adjacent frames is not shutter blur) · Arabic writing → word/run spring + clip-path, never split("") · glyph scramble → seeded, Latin or unjoined glyphs only · line draw → getTotalLength + dashoffset + tip at getPointAtLength · elastic transition → shared geometry into the next scene (a cut is sometimes better) · mask wipe → clipPath/canvas compositing · gooey → feGaussianBlur + feColorMatrix · liquid glass → background distortion + rim light only if GPU justifies it · camera move → deterministic matrix, text inside safe zones · UI demo → rebuilt layered components, not a zoomed screenshot · seamless loop → every animated state incl. velocities periodic at the seam · deterministic seek → frame = f(t, seed, assets), verified by shuffled frame order · voice to motion → forced alignment → events → meaning → keys, ±100 ms only once measured · 3D trailer → camera spline, light rig, verified hardware.

**المعاملات:** 18 mappings

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lexicon · vocabulary · قاموس · مصطلحات · direction · brief translation · ناعم · سلس · مع الإيقاع · smooth · easing

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-P03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/MOTION_TECHNIQUE_LEXICON.md`

#### 7. قدرات قريبة في العائلة

- `STORY-P01` عشرون وصفة أسلوب موشن بمحركاتها / 20 motion style recipes (S01–S20) with engine candidates (documented)
- `STORY-P02` الإحاطة السينمائية بثماني خانات / Eight-slot cinematic brief (PRODUCT → … → OUTPUT) (documented)
- `STORY-U01` خط فيلم الأغنية الكرتوني / Cartoon music-video pipeline (documented)
- `STORY-X01` السيناريو أولًا وخريطة المحفزات / Scenario first: beat-grid shot table and trigger map (documented)

### `STORY-U01` — خط فيلم الأغنية الكرتوني / Cartoon music-video pipeline

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied |

**ما هي:** أغنية ~40 ث (مقطع بين شخصيتين ولازمة واحدة معًا، سطور حرفية بسيطة) ← صفحة شخصيات وبيئات 2×2 ومؤثرات 5×2 مولّدة ← تُعاد رسمها بالكود ولا تُلصق ← رندر بقطع متداخلة قابلة للاستئناف ← لقطات ثابتة بأفواه مغلقة لمزامنة الشفاه. — Song → sheets → repaint in code → resumable render → lip-sync plates.

**متى:** فيديو أغنية كرتوني من الصفر / a cartoon music video from nothing

**كيف:** لكل قسم من الأغنية بيئة؛ كلمات بأسلوب «كود» متوهج؛ كاميرا مدارية.

**المعاملات:** ~40 s; env sheet 2×2; props 5×2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** music video · فيديو أغنية · cartoon · كرتون · characters · شخصيات · lyrics · كلمات · suno

#### 1. الاستقبال (A25)

- المقاس والمنصة: افتراض مكتوب ← 9:16 لمنصات المقاطع القصيرة
- المدة: افتراض مكتوب ← مدة الصوت المرفوع، وإلا 30 ثانية
- الصوت المصدر: سؤال بإجابة مقترحة ← بلا صوت مرفوع: موسيقى مرخصة هادئة أو صمت، يُسأل عنها
- اللقطات والأصول: افتراض مكتوب ← لقطات مجانية مرخصة مع تسجيل رخصة كل لقطة
- الأسلوب البصري: افتراض مكتوب ← أسلوب واحد متسق يقترحه التقرير
- النص الظاهر واللغة: افتراض مكتوب ← عربية RTL بلغة الطلب
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-U01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`

#### 7. قدرات قريبة في العائلة

- `STORY-P02` الإحاطة السينمائية بثماني خانات / Eight-slot cinematic brief (PRODUCT → … → OUTPUT) (documented)
- `STORY-P03` قاموس تحويل وصف الهواة إلى أوامر حركة / Amateur → pro motion lexicon (adjective → code direction) (documented)
- `STORY-X01` السيناريو أولًا وخريطة المحفزات / Scenario first: beat-grid shot table and trigger map (documented)
- `STORY-X02` ذوق العميل: من الرفض إلى قاعدة / Client taste: from rejection to rule (documented)

### `STORY-X01` — السيناريو أولًا وخريطة المحفزات / Scenario first: beat-grid shot table and trigger map

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** قبل البناء: جدول لقطات على شبكة الإيقاع وخريطة محفزات (زمن · سبب · نتيجة · كاميرا) وسؤالان على الأكثر، ثم معايرة نحو خمسة إطارات مفتاحية قبل التوسع. — Before building: a shot table on the beat grid, a trigger map (time · cause · effect · camera), at most two questions, then calibrate about five key frames before fanning out.

**متى:** بداية أي فيلم حركة أو إعلان — the start of any motion film or ad.

**كيف:** Show something visible within 10–15 minutes; the trigger map makes every transition motivated (TRANS-X01); key frames are approved before scenes are built in parallel; status answers give clock time, what changed, the stage, an image and a clock-time ETA, and offer to stop. 'Stop' halts everything, including credit spend.

**المعاملات:** first visible result ≤ 10–15 min; ≤ 2 questions; ~5 calibration frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scenario · storyboard · trigger map · shot list · سيناريو · خريطة محفزات · قائمة لقطات

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
- `owner-upload:motion-skill-claude/higgsfield-motion-claude/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-P03` قاموس تحويل وصف الهواة إلى أوامر حركة / Amateur → pro motion lexicon (adjective → code direction) (documented)
- `STORY-U01` خط فيلم الأغنية الكرتوني / Cartoon music-video pipeline (documented)
- `STORY-X02` ذوق العميل: من الرفض إلى قاعدة / Client taste: from rejection to rule (documented)
- `STORY-X03` انضباط التكرار والنسخ / Iteration and version discipline (documented)

### `STORY-X02` — ذوق العميل: من الرفض إلى قاعدة / Client taste: from rejection to rule

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** كل رفض من العميل يتحول إلى قاعدة مكتوبة تُطبق في الأفلام التالية. — Every client rejection becomes a written rule applied to later films.

**متى:** مشروع مع عميل يتكرر أو مراجعات متعددة — repeat clients or multi-round reviews.

**كيف:** Rules that transferred: flat clean vector reads cheap → add a photographed pass (GLOW-X01) and tint bloom cores; write 'differences from the references' on the storyboard (palette, shape, type, story); an era palette may be borrowed, a brand identity never; one world per film with 6–12 small true details near the hero; the single accent colour and the frame centre are reserved for the story event; 'as in the reference' = sample that range every 0.08 s and copy the motion grammar beat by beat in your own palette and type; 'code-based' means no 3D app at all, so state the toolchain in the first reply; characters idle at about 2× the amplitude that looks right in a still.

**المعاملات:** ref sampling every 0.08 s; 6–12 true details

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** client taste · rejection · rules · references · ذوق العميل · قواعد · مراجع

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`
- `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/client-taste.md`

#### 7. قدرات قريبة في العائلة

- `STORY-U01` خط فيلم الأغنية الكرتوني / Cartoon music-video pipeline (documented)
- `STORY-X01` السيناريو أولًا وخريطة المحفزات / Scenario first: beat-grid shot table and trigger map (documented)
- `STORY-X03` انضباط التكرار والنسخ / Iteration and version discipline (documented)
- `STORY-X04` تقديرات وقت واقعية / Realistic time estimates (documented)

### `STORY-X03` — انضباط التكرار والنسخ / Iteration and version discipline

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** رقّم النسخ ولا تكتب فوقها، وغيّر فقط ما سُمّي، وإذا قيل «النسخة السابقة أفضل» انسخ كودها وأرقامها حرفيًا. — Number versions and never overwrite; change only named items; if told 'vN was better', copy vN's code and numbers verbatim.

**متى:** كل جولة تعديل — every revision round.

**كيف:** Back up the approved version; a new reference mid-project → merge its beats into the approved cut with a beat → reference table; patch-render only the changed ranges; never ship silent and never ship without frame-level QA (QA-X01 plus stills every 2 frames ±0.5 s around each cut); fix diagnosed defects before new ideas.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** versions · revision · iteration · نسخ · تعديل · مراجعة

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-X03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`

#### 7. قدرات قريبة في العائلة

- `STORY-X01` السيناريو أولًا وخريطة المحفزات / Scenario first: beat-grid shot table and trigger map (documented)
- `STORY-X02` ذوق العميل: من الرفض إلى قاعدة / Client taste: from rejection to rule (documented)
- `STORY-X04` تقديرات وقت واقعية / Realistic time estimates (documented)
- `STORY-X05` استعارات بصرية من فيلم الأغنية / Visual metaphors from the owner's song film (documented)

### `STORY-X04` — تقديرات وقت واقعية / Realistic time estimates

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** قدّر وقت العمل من أرقام فعلية لا من حدس؛ التقديرات السابقة كانت أعلى من الواقع بثلاث إلى أربع مرات. — Estimate from measured actuals, not intuition; past estimates were 3–4× too high.

**متى:** حين يسأل المستخدم «كم سيستغرق؟» أو عند التخطيط — when the user asks how long, or when planning.

**كيف:** Storyboard 15–25 min; film 25–45 min after the go for 4–7 scene files; revision 15–40 min; an agent round 30–60 min. Actuals on four owner films: 39 min (estimated 1.5–2 h), 63 min, 1 h 53 min (two rounds), 4 h 50 min (four versions). Masters with 8 sub-frames and a 0.5 shutter take about 20 s of render per film second.

**المعاملات:** storyboard 15–25 min; film 25–45 min; revision 15–40 min

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** estimate · time · planning · تقدير الوقت · تخطيط

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-X04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`
- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/launch-film.md`
- `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`

#### 7. قدرات قريبة في العائلة

- `STORY-X02` ذوق العميل: من الرفض إلى قاعدة / Client taste: from rejection to rule (documented)
- `STORY-X03` انضباط التكرار والنسخ / Iteration and version discipline (documented)
- `STORY-X05` استعارات بصرية من فيلم الأغنية / Visual metaphors from the owner's song film (documented)
- `STORY-X06` اعرض ثلاث معاينات بدل الأسئلة / Show three previews instead of a questionnaire (documented)

### `STORY-X05` — استعارات بصرية من فيلم الأغنية / Visual metaphors from the owner's song film

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (song audio and lyrics are third-party; not included) |

**ما هي:** أدوات سرد مرسومة بالكود: وجهان متقابلان بينهما ضوء، ونجوم ترسم وجهًا، وبورتريه مصنوع من كلمات الأغنية، وسماء تمر عليها ساعات اليوم. — Code-drawn story devices: two facing profiles with light between them, stars that draw a face, a portrait made of the lyric's words, and a time-lapse sky.

**متى:** فيلم أغنية رومانسية أو قصة بلا لقطات حقيقية — a love-song film or a story without real footage.

**كيف:** Rubin-vase profiles: his profile fills bottom → top with her words (portrait made of text). Constellation profile: chosen profile points become stars that draw her face before they meet and complete in the finale. Time-lapse sky colour keys with sun and moon, a blossoming tree, a moon ring pulsing with the audio, meteors on the climactic word. The README traces which catalog styles inspired each idea: keep that catalog → film traceability. The whole 56.92 s 9:16 film is one deterministic canvas file with seek(t) plus three small Python tools; the song stays untouched.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** metaphor · song film · portrait of words · constellation · استعارة بصرية · فيلم أغنية · بورتريه كلمات

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-X05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

#### 6. الأدلة

- `owner-upload:film_project/film/README_AR.md`
- `owner-upload:film_project/film/film.js`

#### 7. قدرات قريبة في العائلة

- `STORY-X03` انضباط التكرار والنسخ / Iteration and version discipline (documented)
- `STORY-X04` تقديرات وقت واقعية / Realistic time estimates (documented)
- `STORY-X06` اعرض ثلاث معاينات بدل الأسئلة / Show three previews instead of a questionnaire (documented)

### `STORY-X06` — اعرض ثلاث معاينات بدل الأسئلة / Show three previews instead of a questionnaire

| الحقل | القيمة |
|---|---|
| العائلة | `story-direction-ideas` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/story-direction-ideas.md)) |
| المجموعة | الموشن والمونتاج والسينما (`motion`) |
| نوع المخرج (A25، A27) | فيديو وموشن ومونتاج (`video`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | MIT (ECC, (c) 2026 Affaan Mustafa) |

**ما هي:** لاكتشاف الذوق ابنِ ثلاثة إطارات معاينة مختلفة فعلًا ودع المستخدم يختار، بدل قائمة أسئلة. — To discover taste, build three genuinely different single-frame previews and let the user pick, instead of a questionnaire.

**متى:** بداية مشروع والمستخدم لا يعرف ما يريد — the start of a project when the user cannot describe the look.

**كيف:** Each preview is small (under ~100 lines) and shows one direction: palette, type and motion feel. Then build the chosen one with tokens. Works for decks, title cards and film looks alike.

**المعاملات:** 3 previews; < ~100 lines each

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** previews · style discovery · options · معاينات · اكتشاف الذوق

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

- عقدة منمّطة: المدخل `audio` ← المخرج `video`، والمنفّذ `method:STORY-X06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `atlas-render` · `creative-reasoning-bridge` · `drawing-methods` · `drawing-visual-qa` · `repo-kosif` · `style-atlas-bridge`.
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

- `https://github.com/affaan-m/ECC/tree/main/skills/frontend-slides/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `STORY-X04` تقديرات وقت واقعية / Realistic time estimates (documented)
- `STORY-X05` استعارات بصرية من فيلم الأغنية / Visual metaphors from the owner's song film (documented)

