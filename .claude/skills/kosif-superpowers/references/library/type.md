# الخطوط والنصوص العربية واللاتينية — Typography & localization (`type`)

> مكتبة بروتوكول USIP v5.6، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: arabic text typography font subtitle rtl letter line خط خطوط عربي كتابة تنسيق نص

لا خط عمل مسجّل لهذه المجموعة؛ ركّبه من الأدوات أدناه.

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 40 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 49 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 45 | 📄 documented: a described method; needs building or wiring before it runs |
| `seen` | 46 | 👁 seen: observed in a reference or demo, not executed here |
| `install` | 31 | 📦 install: needs a package, binary or model first |
| `key` | 1 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 3 | 💡 idea: not built |
| **المجموع** | **215** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `anchor-gate` | بوابة حفظ الحقائق عند إعادة الصياغة | `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/en_before.txt --after proofs/general-writing/pairs/en_after_drift.txt --text` | tested-here |
| `app-studio` | استوديو التطبيقات للصور والتصميم | `python3 scripts/app_studio.py --help` | tested-here |
| `font-fidelity-lab` | مختبر مطابقة الخطوط العربية | `python3 scripts/font_fidelity_lab.py inspect proofs/_shared/fonts/Amiri-Regular.ttf --text "جمعة مباركة"` | tested-here |
| `image-local-ai` | ذكاء الصور المحلي: إزالة الخلفية والملء الذكي بنموذج ONNX تختاره | `python3 scripts/image_local_ai.py models --json` | tested-here |
| `mimic` | محرك محاكاة الفيديو المرجعي | `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_analyze; mm_analyze.analyze('./in.mp4','./work')"` | tested-here |
| `motion-runtime` | إنشاء فيلم سبورة مرسوم وتصييره | `python3 scripts/motion_runtime.py doctor` | tested-here |
| `reel-factory` | مصنع الريلز: صوت وتوقيت كلمات ولقطات مرخصة ← ريلز 9:16 مفحوص | `python3 scripts/reel_factory.py plan --audio ./voice.m4a --audio-rights owned --words ./words.json --shots-manifest ./stock/manifest.json --shot-ids 17928486,8165467,20382699 --title "دعاء يوم الخميس" --handle @kosif` | tested-here |
| `render-text` | أداة عرض النص بخطوط مرشّحة | `node scripts/render_text.cjs ./spec.json ./out/` | tested-elsewhere |
| `starter-html-canvas` | قالب فيلم HTML Canvas | `python3 tools/kosif.py scaffold kinetic-arabic ./my-film --starter html-canvas` | tested-elsewhere |
| `starter-remotion` | قالب فيلم Remotion | `python3 tools/kosif.py scaffold product ./my-film --starter remotion` | tested-elsewhere |
| `telegram-typography-atlas` | مكتبة KOSIF الشاملة للخطوط وأفكار التصميم من صادرات تيليجرام | `python3 scripts/telegram_typography_atlas.py find --index data/telegram-typography-catalog-complete-20261020.json "خط رقعة" --arabic-only --limit 15` | tested-here |
| `tell-scan` | فاحص العبارات الكتابية النمطية | `python3 scripts/tell_scan.py proofs/general-writing/samples/en_ai.txt` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `arabic-language` | 22 | [arabic-language.md](../powers/arabic-language.md) |
| `typography-arabic` | 99 | [typography-arabic.md](../powers/typography-arabic.md) |
| `typography-latin` | 94 | [typography-latin.md](../powers/typography-latin.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `ARL-01` | تطبيع العربية للبحث والمطابقة | Normalize Arabic for search and matching | proven | python3 |
| `ARL-02` | طابِق على نسخة مطبّعة واعرض بالإملاء الأصلي | Match normalized, report in the original spelling | proven |  |
| `ARL-03` | حدود الكلمة العربية مع السوابق | Clitic-aware Arabic word boundaries | proven | python3 |
| `ARL-04` | قراءة الأرقام العربية: هندية وفارسية وفواصل ونسبة | Parse Arabic numerals, separators and percent | proven |  |
| `ARL-05` | أسماء الشهور والأيام: ميلادية وشامية وهجرية | Month and weekday names (Gregorian, Levantine, Hijri) | proven |  |
| `ARL-06` | تشكيل الحروف للعرض: محرك واحد فقط | Shaping Arabic for display: exactly one engine | proven | pip:pillow, pip:matplotlib, pip:office, fonts:arabic |
| `ARL-08` | خطوط عربية: فحص وتثبيت | Arabic fonts: check and install | proven | fonts:arabic |
| `ARL-10` | أدوات CAMeL Tools الخفيفة بلا نماذج | camel-tools character utilities without models | proven | pip:torch, pip:camel-tools |
| `ARL-12` | PyArabic للتنظيف والتقطيع (رخصة GPL) | PyArabic for cleanup and tokenizing (GPL) | proven | python3 |
| `ARL-14` | التعرف الضوئي على العربية (tesseract) | Arabic OCR with tesseract | proven | tesseract, pip:torch, fonts:arabic |
| `ARL-15` | تحقق من أرقام OCR ببوابة المراسي | Verify OCR numbers with the anchor gate | proven | python3, tesseract |
| `ARL-16` | إصلاح الترميز المشوّه | Mojibake repair | proven | python3 |
| `ARL-18` | النقل الحرفي والرومنة | Transliteration and romanization | proven | pip:camel-tools |
| `ARL-21` | spaCy: تقطيع العربية ومطابقة القواعد؛ واستخراج الكيانات مع | spaCy: Tokenise Arabic and match rules (blank 'ar'); NER with downloaded models | proven | pip:spacy |
| `ARAB-01` | الكلمة كاملة لا الحرف | Whole-word law | proven |  |
| `ARAB-02` | حصر الاتجاه في عناصر النص | RTL scoping for renderers | proven | python3, npm:hyperframes |
| `ARAB-06` | توجيه محرك التشكيل | Shaping-engine routing | proven | ffmpeg, chromium, pip:pillow, npm:remotion |
| `ARAB-08` | مفتاح لغة المحتوى | Content-language switch ar\|en\|both | proven | python3 |
| `ARAB-09` | نص حقيقي فوق لوحات التوليد | Real type over generated plates | proven | npm:remotion, key:video-gen, fonts:arabic |
| `ARAB-12` | كايرو المقسوم بنطاق يونيكود | Cairo split by unicode-range | proven | fonts:arabic |
| `ARAB-15` | اقترانات الخطوط | Type pairings | proven | fonts:arabic |
| `ARAB-19` | أقنعة الكلمات: إظهار وإخفاء | Word-mask reveal & hide | proven | npm:gsap |
| `ARAB-24` | سطور تصعد من خلف خط قطع | Lines rising behind a cut line | proven |  |
| `ARAB-26` | عنوان كلمات بنابض كل 160 مللي ثانية | Spring word-stagger title | proven | npm:remotion, fonts:arabic |
| `ARAB-49` | قوالب الموشن العربية الثمانية | Eight Arabic motion templates | proven | python3, chromium, npm:gsap, fonts:arabic |
| `ARAB-50` | شريط اسم سفلي تلقائي الاتجاه | Auto-RTL lower third | proven |  |
| `ARAB-62` | كاريوكي ASS عربي بثلاثة أنماط | Arabic ASS karaoke captions (reels · cinema · punchy) | proven | ffmpeg, python3, imagemagick, fonts:arabic |
| `ARAB-67` | تقسيم الأسطر بالبرمجة الديناميكية | DP line breaking for lyrics & dua | proven |  |
| `ARAB-68` | اختيار الكلمة المفتاحية بالنبر | Stress-based keyword picking | proven |  |
| `ARAB-69` | توحيد النص العربي للمطابقة | Arabic normalisation for alignment & matching | proven |  |
| `ARAB-74` | منسّق الأرقام الهندية الحتمي | Deterministic Arabic-Indic money formatter | proven | node |
| `ARAB-81` | إصلاح أسماء الملفات العربية المشوّهة | Arabic file-name mojibake repair | proven |  |
| `ARAB-84` | التقاط ستايل النص وإعادة تركيبه | Text-style capture & compositing | proven | tesseract |
| `ARAB-U01` | خط El Messiri العربي مضمّن | El Messiri Arabic display font bundled (OFL) | proven | pip:pillow, fonts:arabic |
| `ARAB-X04` | مطابقة الخط عبر محرك تشكيل حقيقي | Font matching through a real shaper (Chromium/HarfBuzz) | proven | node, chromium, pip:pillow, fonts:arabic |
| `ARAB-X05` | تجميع عائلة خط مطابقة من مصدرين OFL | Assemble a matched OFL family from two masters | proven | pip:fonttools, fonts:arabic |
| `ARAB-X06` | عنوان خطي مركّب من حدود حروف مفتوحة | Composed calligraphic title from OFL outlines | proven | python3, fonts:arabic |
| `TYPE-40` | إيقاع البادئة/البطل/الذيل | Lead / hero / tail beat splitter | proven | node |
| `TYPE-79` | عنوان سينمائي متباعد الحروف | Letter-spaced cinematic title | proven | node |
| `TYPE-U01` | خط Poppins مضمّن | Poppins bundled (OFL) | proven | pip:pillow, fonts:arabic |
| `ARAB-04` | بوابة تحميل الخط قبل الإطار الأول | Font-ready gate before frame 0 | ready | npm:remotion, fonts:arabic |
| `ARAB-05` | مساحة التشكيل وحواف الأقنعة | Harakat headroom & mask padding | ready |  |
| `ARAB-07` | كشف الاتجاه تلقائيًا | Auto RTL detection | ready |  |
| `ARAB-11` | خريطة أصوات الخطوط | Arabic font voice map | ready | fonts:arabic |
| `ARAB-13` | اكتشاف الخطوط وسلسلة البدائل | Font discovery & fallback chain | ready | ffmpeg, pip:pillow, pip:fonttools, npm:remotion |
| `ARAB-14` | محمّل الخطوط الحي ومنتقي الخط | Live Google Fonts loader & picker | ready | fonts:arabic |
| `ARAB-17` | سلّم القراءة للشاشات | Screen reading scale (v17 / SQC) | ready | fonts:arabic |
| `ARAB-18` | قواعد التايبوغرافي العربي الحركي | Kinetic Arabic grammar | ready | node, python3, chromium |
| `ARAB-20` | صعود الكلمات من الضباب | Rise-from-blur words | ready |  |
| `ARAB-25` | انزلاق سطور عربية على Canvas | Canvas RTL staggered line slide | ready | fonts:arabic |
| `ARAB-28` | دخول الكلمة من العمق | 3D word turn-in from depth | ready | chromium, npm:gsap |
| `ARAB-29` | الآلة الكاتبة بمؤشر | Typewriter with caret | ready |  |
| `ARAB-34` | ضربة الكلمة المفتاحية بقناع صاعد | Keyword slam with upward mask | ready |  |
| `ARAB-39` | تعبئات مذهّبة ومتدرجة ولمعة عابرة | Gilded, gradient & sweeping fills | ready |  |
| `ARAB-40` | هرمية بثلاث مستويات | Three-level type hierarchy | ready |  |
| `ARAB-41` | تمييز الكلمة بالنجمة | *Asterisk* emphasis convention | ready |  |
| `ARAB-45` | علامة استفهام عملاقة مفرّغة | Giant outlined question mark | ready |  |
| `ARAB-47` | خط مضيء يتمدد تحت العنوان | Growing glow rule under the title | ready |  |
| `ARAB-53` | ترويسة اليوم بالهجري والميلادي | Hijri + Gregorian day header | ready | fonts:arabic |
| `ARAB-54` | أقراص وشارات وأرقام مرقّمة | Pills, chips & numbered badges | ready |  |
| `ARAB-55` | مكدّس عربي/إنجليزي | Bilingual Arabic/English stacks & HUD | ready | fonts:arabic |
| `ARAB-57` | عنوان عربي سينمائي فوق الفيديو | Cinematic Arabic headline over footage | ready |  |
| `ARAB-58` | عنوان ASS متحرك لكل لقطة | Per-shot ASS animated title card | ready | ffmpeg |
| `ARAB-59` | غلاف بعنوان عربي مشكّل | Shaped Arabic cover / thumbnail | ready | pip:pillow, pip:arabic-reshaper |
| `ARAB-60` | كاروسيل عربي PNG/PDF | Arabic carousel renderer | ready | pip:pillow, fonts:arabic |
| `ARAB-61` | طبقات نص الخط الزمني JSON | Timeline-JSON text overlays | ready |  |
| `ARAB-72` | العزل الاتجاهي | Bidi isolation | ready | ffmpeg |
| `ARAB-73` | نظام أرقام واحد وأرقام جدولية | One digit system + tabular figures | ready |  |
| `ARAB-75` | قراءة الأرقام والوحدات العربية | Digit parsing & number/unit detection | ready |  |
| `ARAB-76` | صيغ الجمع ومطابقة العدد | Plural & count agreement | ready |  |
| `ARAB-82` | سطر الحقوق الآمن | Safe credit-line burn | ready | ffmpeg |
| `ARAB-83` | تسمية الألوان بالعربية | Arabic colour naming | ready |  |
| `ARAB-85` | قياس حركة النص وتصنيفها | Text-animation measurement & replay | ready | ffmpeg, pip:numpy, pip:pillow, pip:opencv |
| `ARAB-86` | مطابقة الخط بالحبر | Font matching by ink | ready |  |
| `ARAB-87` | ملاءمة العرض والتصغير التلقائي | Fit-width & shrink-to-fit | ready |  |
| `ARAB-89` | طبقات نص عربي على Canvas | Canvas RTL text-layer helpers | ready | fonts:arabic |
| `TYPE-11` | خطوط لاتينية مدمجة جاهزة | Owner-bundled Latin fonts (offline) | ready | fonts:arabic |
| `TYPE-12` | تضمين الخطوط داخل الملف | Offline font inlining (base64) | ready | npm:gsap, npm:hyperframes, key:openai |
| `TYPE-13` | مجموعة Google Fonts للتبديل الحي | Curated Google Fonts swap set | ready |  |
| `TYPE-14` | صعود من خلف خط القاعدة | Baseline mask rise (lines & words) | ready | python3, npm:gsap |
| `TYPE-15` | صعود من حالة جزئية | Rise from a partial state (riseWords) | ready |  |
| `TYPE-27` | عنوان قماشي من 1–4 كلمات مع اتجاه تلقائي | Canvas 1–4-word headline with auto-RTL | ready |  |
| `TYPE-31` | آلة كاتبة متدرجة بمؤشر | Eased typewriter with caret (typeOn) | ready | npm:gsap, npm:hyperframes |
| `TYPE-33` | فك التشفير | Scramble / decode reveal | ready |  |
| `TYPE-37` | عدّاد بأرقام جدولية | Tabular counter (MOTION.counter) | ready |  |
| `TYPE-46` | كلمة بانفصال RGB وتشويش | RGB-split glitch word | ready |  |
| `TYPE-53` | غروتسك عريض مع كلمة سيريف مائلة | Grotesk + italic-serif accent | ready | fonts:arabic |
| `TYPE-63` | طباعة شبحية خلفية | Giant ghost background type & ghost rows | ready | npm:hyperframes |
| `TYPE-82` | الشرائط السفلية ولوحات الأسماء | Lower-thirds & name plates | ready |  |
| `ARL-07` | الاتجاه الثنائي في النصوص المختلطة | Bidi in mixed Arabic/Latin text | documented | tesseract |
| `ARL-09` | سياسة التشكيل (الحركات) | Tashkeel policy | documented | pip:pillow, fonts:arabic |
| `ARL-17` | التعامل مع اللهجات وتحديد السجل | Dialect handling and register choice | documented | pip:camel-tools |
| `ARL-19` | مراجعة المطابقة النحوية بعد التعديل | Agreement check after editing | documented |  |
| `ARAB-03` | لا تباعد ولا مطّ — الكشيدة فقط | No tracking, no stretch — kashida only | documented |  |
| `ARAB-10` | العربية داخل مشهد ثلاثي الأبعاد | Arabic inside 3D scenes | documented | npm:three |
| `ARAB-16` | سلّم أحجام الفيديو | Video type scale at 1080 px | documented |  |
| `ARAB-21` | مسح القناع من اليمين | RTL clip wipe | documented |  |
| `ARAB-23` | قناع ضربة فرشاة | Brush-stroke mask write-on | documented |  |
| `ARAB-33` | كلمات على مسار دائري | Words on a circular path | documented |  |
| `ARAB-35` | كلمة ترتطم وتستقر | Slam-and-settle word | documented |  |
| `ARAB-37` | الكلمة تمثّل معناها | Word acts out its meaning | documented |  |
| `ARAB-38` | صدى طباعي يتلاشى | Typographic echo | documented |  |
| `ARAB-52` | صندوق عنوان يحافظ على مركزه | Centre-locked resizing title box | documented |  |
| `ARAB-63` | قانون زمن القراءة والكثافة | Reading-time & density law | documented |  |
| `ARAB-64` | منطقة الترجمة الآمنة وشكلها | Caption safe zone & look | documented | fonts:arabic |
| `ARAB-70` | النص المشكول مصدرًا للتوقيت | Vowelled source text over ASR | documented |  |
| `ARAB-77` | رقم يتحول إلى عنوان | Number → headline | documented |  |
| `ARAB-78` | حوار طباعي | Typographic dialogue | documented |  |
| `ARAB-79` | الدعوة والسعر بالعربية | Arabic CTA & price isolation | documented |  |
| `ARAB-88` | نص مشكّل في المشاهد المرسومة واستيراد SVG | Shaped text in painted scenes & SVG import | documented | pip:pillow, fonts:arabic |
| `ARAB-92` | أربعة خطوط عربية مفتوحة يرفقها مصمم | Four open Arabic fonts bundled by Mosamem (IBM Plex Sans Arabic, Cairo, Tajawal, Amiri) | documented | fonts:arabic |
| `ARAB-X01` | كشف الكلمة العربية كاملة من اليمين | RTL whole-word lyric reveal with key-word pop | documented |  |
| `ARAB-X02` | ترشيح الخط لا الجزم به | Font matches are candidates, not identities | documented | pip:pillow, npm:three |
| `ARAB-X03` | الزخرفة والكشيدة للنبذة فقط | Unicode ornaments and kashida: bios only | documented |  |
| `TYPE-01` | مقاسات الخط للفيديو | Video type sizing & contrast | documented |  |
| `TYPE-02` | ميزانية الكلمات والأسطر | Word & line budgets (on-screen copy ≠ narration) | documented |  |
| `TYPE-03` | زمن القراءة والثبات | Read-time & hold rules | documented |  |
| `TYPE-04` | سلّم الأحجام والأوزان والتباعد | Scale, weight, leading & tracking tokens | documented | npm:react |
| `TYPE-05` | اختيار الخط وتزويجه | Choosing & pairing faces | documented | fonts:arabic |
| `TYPE-06` | أرقام جدولية وخصائص OpenType | Tabular numerals & OpenType features | documented |  |
| `TYPE-08` | نص SVG حاد وهالات التسميات | Crisp SVG text & label halos | documented |  |
| `TYPE-09` | تراخيص الخطوط ونظافتها | Font licensing & font hygiene | documented | pip:pillow, npm:hyperframes, fonts:arabic |
| `TYPE-22` | الدخول الشلالي | Waterfall entry cascade | documented | npm:gsap |
| `TYPE-24` | مسح الكلمة الكبيرة بالقناع | Clip-path big-word wipe | documented |  |
| `TYPE-29` | مفردات حركة النص للستوري بورد | Text-motion vocabulary for storyboards | documented |  |
| `TYPE-30` | الكلمة المختفية | Invisible-word blink | documented |  |
| `TYPE-34` | قلب الحروف ثلاثي الأبعاد | Hacker-flip 3D decode | documented | npm:gsap |
| `TYPE-43` | وصفة سطر الافتتاح | Hook-line recipe & kinetic-type beats | documented |  |
| `TYPE-71` | كلمات مدمجة داخل اللقطة | Words embedded in footage (composition craft) | documented |  |
| `TYPE-89` | استايلات حركية في الكتالوج | Catalog kinetic styles: brutalist · minimal · typewriter | documented | node, python3, chromium |
| `TYPE-90` | تزويجات ولوحات جاهزة للعناوين | Preset pairings & palettes for title systems | documented | npm:hyperframes |
| `TYPE-U02` | قواعد قراءة الترجمة فوق اللقطات | Caption readability rules over footage | documented |  |
| `TYPE-X01` | نص يعبر القطع | Type that keeps moving through cuts | documented |  |
| `TYPE-X02` | ثلاث عائلات خطوط بمصدر واحد | Three font families from one source of truth | documented |  |
| `ARAB-30` | كلمة ضخمة من الضباب تنكمش إلى سطر | Blur-in hero word that shrinks into the sentence | seen |  |
| `ARAB-31` | كبسولة الكلمات الدوّارة | Rolling word pill with growing rings | seen |  |
| `ARAB-32` | كشف بالحبر وسحب التركيز | Ink-bleed / focus-pull word reveal | seen |  |
| `ARAB-36` | ضربة الكلمة البطلة بتوهج | Hero-word punch with bloom | seen |  |
| `ARAB-42` | خط متموّج تحت الكلمة المفتاحية | Squiggle underline highlight | seen |  |
| `ARAB-43` | ممسحة التظليل من اليمين | RTL highlighter swipe | seen |  |
| `ARAB-44` | ختم أحمر يرتطم | Rubber-stamp slam | seen |  |
| `ARAB-46` | ظل مزدوج مزاح | Offset duotone shadow hero | seen |  |
| `ARAB-48` | سطور تتكدس وتخفت | Stacked headline lines that dim | seen |  |
| `ARAB-56` | بطاقة شخصية من اليمين | RTL character card | seen |  |
| `ARAB-65` | الكلمة المنطوقة تضيء | Spoken-word illumination (HTML captions) | seen |  |
| `TYPE-17` | إضاءة الكلمات بترتيب القراءة | Reading-order light-up & blur manifesto | seen |  |
| `TYPE-25` | كشف بالشرائح | Strip-slice letter reveal | seen |  |
| `TYPE-26` | بناء الكلمة على شبكة إنشائية | Construction-grid & guide-line build | seen |  |
| `TYPE-28` | موجة الحروف | Per-letter sine bounce & wave | seen |  |
| `TYPE-36` | عدّاد الأسطوانة الدوّار | Odometer digit roll | seen |  |
| `TYPE-42` | متتاليات الضرب وجمل تُبنى بالضربات | Beat-slam sequences & stacked statements | seen | npm:hyperframes |
| `TYPE-44` | ختم وملصق وكلمة مؤثر صوتي | Stamp, sticker & SFX word pop | seen |  |
| `TYPE-45` | انزلاق بضبابية حركة ولطخة لونية | Motion-blur slide, smear & stretch | seen |  |
| `TYPE-50` | كلمات داخل كبسولات | Keyword pills | seen |  |
| `TYPE-52` | عنوان بلونين وكلمة لون | Two-tone lines & accent-word colour | seen |  |
| `TYPE-54` | عنوان سيريف تحريري بكلمة مائلة | Editorial serif headline & keyword title | seen | fonts:arabic |
| `TYPE-55` | تعبئة متدرجة ومعدنية | Gradient & metallic word fills | seen |  |
| `TYPE-56` | أقواس تحديد وصندوق أداة تصميم | Selection brackets & design-tool bounding box | seen |  |
| `TYPE-57` | صور ووجوه وأيقونات داخل السطر | Inline avatars & icons inside a headline | seen |  |
| `TYPE-58` | الكلمة تؤدي معناها | Word performs its meaning | seen |  |
| `TYPE-59` | قوائم تخفت السابق | Dim-previous stacks & active-item lists | seen |  |
| `TYPE-60` | النقطة الختامية وإبدال الحرف | Full-stop dot & glyph substitution | seen |  |
| `TYPE-64` | نص بارز بظلال مكدسة | Extruded & stacked-shadow type | seen | npm:hyperframes |
| `TYPE-65` | أثر الصدى والنسخ المحيطية | Echo trail & outline echo stack | seen |  |
| `TYPE-66` | نص مملوء بصورة أو فيديو | Image- & video-filled text | seen |  |
| `TYPE-69` | جسيمات تتجمع لتكوّن كلمة | Particles assemble into a word | seen |  |
| `TYPE-70` | خط الخلايا: ASCII ونقاط المصفوفة | Cell-based type: ASCII blocks & dot-matrix numerals | seen |  |
| `TYPE-72` | نص على حلقات ومدارات | Text rings & orbiting words | seen |  |
| `TYPE-73` | نفق النص ودوامته | Circular text tunnel & spiral vortex | seen |  |
| `TYPE-74` | أسطوانة نص ثلاثية الأبعاد وشرائط حلزونية | 3D text cylinder & helix ribbons | seen |  |
| `TYPE-75` | جدار الشرائط المتعاكسة | Bidirectional marquee wall | seen |  |
| `TYPE-76` | شريط مائل وجدار منظوري | Tilted ticker band & perspective word wall | seen |  |
| `TYPE-78` | كلمات كعمارة ودوران الأرباع | Words as architecture & quadrant rotation | seen |  |
| `TYPE-81` | بطاقات الفصول والأرقام الضخمة | Numbered chapter blocks & giant-number cards | seen |  |
| `TYPE-83` | أنظمة الأصوات الطباعية | Multi-voice type systems | seen | pip:faster-whisper |
| `TYPE-84` | مظهر الترجمة حسب النبرة والعالم | Caption look by tone & theme | seen |  |
| `TYPE-85` | تكديس هرمي بأحجام متدرجة | Size-stepped hierarchy stacks | seen |  |
| `TYPE-86` | عنوان سيريف متراكب يُبنى كلمة كلمة | Stacked serif title build | seen |  |
| `TYPE-87` | بطاقة حرف أو كلمة بملء الشاشة | Full-bleed glyph & word cards | seen |  |
| `TYPE-88` | تجميع المعادلات | Equation assembly | seen |  |
| `ARL-11` | تحليل صرفي وتعرّف اللهجة والكيانات (CAMeL Tools كاملة) | Morphology, dialect ID and NER with full camel-tools | install | pip:torch, pip:camel-tools |
| `ARL-13` | مقطّع Farasa عبر farasapy | Farasa segmenter via farasapy | install | pip:camel-tools |
| `ARL-20` | CAMeL Tools: تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد | CAMeL Tools: Tokenise, lemmatise, diacritise and dialect-identify Arabic text | install | pip:camel-tools |
| `ARL-22` | Argos Translate: ترجمة عربي-إنجليزي دون اتصال تمامًا | Argos Translate: Translate Arabic↔English fully offline | install | pip:argos |
| `ARAB-22` | كتابة بقناع ناعم ورأس قلم | Feathered RTL write-on with pen head | install | node |
| `ARAB-27` | عنوان Remotion بنابض وأقراص كلمات | Remotion spring title + keyword pills | install | npm:remotion, npm:react |
| `ARAB-51` | ثلاثة أشكال لعنوان الخطاف | Hook title looks: box · kinetic · minimal | install | node, fonts:arabic |
| `ARAB-66` | فيلم الكلمات من الصوت | Verse film from sound (song · poem · dua) | install | pip:faster-whisper, fonts:arabic |
| `ARAB-71` | ستايل الكلمات العاطفي | Emotional lyric style preset | install | node, fonts:arabic |
| `ARAB-80` | تسميات عربية مُسقطة على الخرائط والعوالم | Projected Arabic labels (maps · isometric · charts) | install | npm:maplibre |
| `ARAB-91` | مصمم: نص عربي قابل للتعديل بتشكيل HarfRust وكشيدة | Mosamem: editable Arabic text with HarfRust shaping and kashida justification | install | pip:pillow |
| `TYPE-07` | ملاءمة النص للعرض وقياسه | Fit-to-width & text measuring | install | npm:remotion, npm:hyperframes |
| `TYPE-16` | ظهور من الضباب (سحب البؤرة) | Blur-to-sharp focus pull | install | npm:hyperframes |
| `TYPE-18` | تتابع الحروف سقوطًا وصعودًا | Per-letter drop & rise cascades | install | npm:hyperframes |
| `TYPE-19` | تبعثر وتدحرج وتجميع | Scatter, tumble & gravity assemble | install | npm:hyperframes |
| `TYPE-20` | تقارب الحروف | Tracking-in collapse (Latin only) | install | npm:hyperframes |
| `TYPE-21` | تكديس الأسطر ودفعها وتبديلها | Line stack, push & swap | install | npm:hyperframes |
| `TYPE-23` | بناء من المركز | Kinetic center build | install | npm:hyperframes |
| `TYPE-32` | كتابة بشرية: أخطاء ومسح ومؤشر ملوّن | Human typing: typos, backspace, caret swap | install | npm:hyperframes |
| `TYPE-35` | لوحة المطار القلّابة | Split-flap (Solari) board | install | npm:gsap, npm:hyperframes |
| `TYPE-38` | بكرة الكلمات وعدّاد نابض | Slot-machine word roll & spring ticker | install | npm:gsap, npm:hyperframes |
| `TYPE-39` | تبديل كلمة في خانة ثابتة واستيلاء الشريط | Word-slot swap & ticker takeover | install | npm:hyperframes |
| `TYPE-41` | صدمة العنوان وضربة الكلمة على الإيقاع | Headline slam & beat word punch | install | npm:hyperframes |
| `TYPE-47` | بدائيات حركة النص على الموسيقى | Music-anchored type primitives & templates | install | npm:gsap, npm:hyperframes |
| `TYPE-49` | قلم التظليل والخط السفلي | Highlighter & underline swipe | install | npm:hyperframes |
| `TYPE-51` | شطب واستبدال | Strike-through & replace | install | npm:hyperframes |
| `TYPE-61` | الخط المتغير: محاور ووزن متموج وعرض | Variable-font motion: axis tween, weight wave, width swell | install | npm:hyperframes, fonts:arabic |
| `TYPE-62` | خط مفرّغ: أرقام مجوفة ومن محيط إلى تعبئة | Outline type: hollow numerals, outline → fill, glowing outline | install | npm:hyperframes |
| `TYPE-67` | نص لزج متحول | Gooey morph text | install | npm:gsap, npm:hyperframes |
| `TYPE-68` | حروف منفوخة بالفيزياء | Inflated physics letterforms | install | npm:matter |
| `TYPE-80` | بطاقة عنوان هادئة وقفل الشعار | Calm title card & lockup | install | npm:hyperframes |
| `TYPE-10` | حدود النص داخل صور الذكاء الاصطناعي | Text-in-AI-image ladder | key | key:video-gen |
| `ARAB-90` | دوران كتلة النص 90° ككاميرا | Type-block 90° rotation as camera move | idea |  |
| `TYPE-48` | نص بإطارات ممسوكة | Held-frame stepped type | idea |  |
| `TYPE-77` | جدار نص يندفع وينضغط إلى شعار | Text-wall rush & compress into a logo | idea |  |
