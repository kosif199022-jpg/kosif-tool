# الخطوط والنصوص العربية واللاتينية — Typography & localization

[← الفهرس الدقيق / micro index](README.md) · 215 powers

## الفهرس / contents

- [arabic-language (craft)](#arabic-language-craft)
- [typography-arabic (motion)](#typography-arabic-motion)
- [typography-latin (motion)](#typography-latin-motion)


## arabic-language (craft)

chapter: [arabic-language](../powers/arabic-language.md) · card: `usip-library/cards/type/arabic-language.md` · tools: `anchor-gate` · `quran-text` · `tell-scan`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| ARL-01 | ✅ | تطبيع العربية للبحث والمطابقة · Normalize Arabic for search and matching | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | python3 |
| ARL-02 | ✅ | طابِق على نسخة مطبّعة واعرض بالإملاء الأصلي · Match normalized, report in the original spelling | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | — |
| ARL-03 | ✅ | حدود الكلمة العربية مع السوابق · Clitic-aware Arabic word boundaries | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | python3 |
| ARL-04 | ✅ | قراءة الأرقام العربية: هندية وفارسية وفواصل ونسبة · Parse Arabic numerals, separators and percent | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | — |
| ARL-05 | ✅ | أسماء الشهور والأيام: ميلادية وشامية وهجرية · Month and weekday names (Gregorian, Levantine, Hijri) | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | — |
| ARL-06 | ✅ | تشكيل الحروف للعرض: محرك واحد فقط · Shaping Arabic for display: exactly one engine | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:pillow, pip:matplotlib, pip:office, fonts:arabic … |
| ARL-08 | ✅ | خطوط عربية: فحص وتثبيت · Arabic fonts: check and install | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | fonts:arabic |
| ARL-10 | ✅ | أدوات CAMeL Tools الخفيفة بلا نماذج · camel-tools character utilities without models | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:torch, pip:camel-tools |
| ARL-12 | ✅ | PyArabic للتنظيف والتقطيع (رخصة GPL) · PyArabic for cleanup and tokenizing (GPL) | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | python3 |
| ARL-16 | ✅ | إصلاح الترميز المشوّه · Mojibake repair | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | python3 |
| ARL-18 | ✅ | النقل الحرفي والرومنة · Transliteration and romanization | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:camel-tools |
| ARL-21 | ✅ | spaCy: تقطيع العربية ومطابقة القواعد؛ واستخراج الكيانات مع · spaCy: Tokenise Arabic and match rules (blank 'ar'); NER with downloaded models | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:spacy |
| ARL-11 | 📦 | تحليل صرفي وتعرّف اللهجة والكيانات (CAMeL Tools كاملة) · Morphology, dialect ID and NER with full camel-tools | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:torch, pip:camel-tools |
| ARL-13 | 📦 | مقطّع Farasa عبر farasapy · Farasa segmenter via farasapy | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:camel-tools |
| ARL-20 | 📦 | CAMeL Tools: تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد · CAMeL Tools: Tokenise, lemmatise, diacritise and dialect-identify Arabic text | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:camel-tools |
| ARL-22 | 📦 | Argos Translate: ترجمة عربي-إنجليزي دون اتصال تمامًا · Argos Translate: Translate Arabic↔English fully offline | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:argos |
| ARL-07 | 📄 | الاتجاه الثنائي في النصوص المختلطة · Bidi in mixed Arabic/Latin text | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | tesseract |
| ARL-09 | 📄 | سياسة التشكيل (الحركات) · Tashkeel policy | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:pillow, fonts:arabic |
| ARL-17 | 📄 | التعامل مع اللهجات وتحديد السجل · Dialect handling and register choice | SP-0033 CAMeL Tools: Tokenise, lemmatise, diacr… | pip:camel-tools |
| ARL-15 | ✅ | تحقق من أرقام OCR ببوابة المراسي · Verify OCR numbers with the anchor gate | SP-0034 Verify OCR numbers with the anchor gate | python3, tesseract |
| ARL-19 | 📄 | مراجعة المطابقة النحوية بعد التعديل · Agreement check after editing | SP-0034 Verify OCR numbers with the anchor gate | — |
| ARL-14 | ✅ | التعرف الضوئي على العربية (tesseract) · Arabic OCR with tesseract | SP-0158 Arabic + English OCR with tesseract | tesseract, pip:torch, fonts:arabic |

## typography-arabic (motion)

chapter: [typography-arabic](../powers/typography-arabic.md) · card: `usip-library/cards/type/typography-arabic.md` · tools: `app-studio` · `caption-lines` · `design-tells` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime` · `quran-text` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| ARAB-44 | 👁 | ختم أحمر يرتطم · Rubber-stamp slam | SP-0258 Four named eases slam/snap/drive/settle | — |
| ARAB-35 | 📄 | كلمة ترتطم وتستقر · Slam-and-settle word | SP-0258 Four named eases slam/snap/drive/settle | — |
| ARAB-01 | ✅ | الكلمة كاملة لا الحرف · Whole-word law | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-02 | ✅ | حصر الاتجاه في عناصر النص · RTL scoping for renderers | SP-0453 RTL whole-word lyric reveal with key-wo… | python3, npm:hyperframes |
| ARAB-06 | ✅ | توجيه محرك التشكيل · Shaping-engine routing | SP-0453 RTL whole-word lyric reveal with key-wo… | ffmpeg, chromium, pip:pillow, npm:remotion … |
| ARAB-08 | ✅ | مفتاح لغة المحتوى · Content-language switch ar/en/both | SP-0453 RTL whole-word lyric reveal with key-wo… | python3 |
| ARAB-19 | ✅ | أقنعة الكلمات: إظهار وإخفاء · Word-mask reveal & hide | SP-0453 RTL whole-word lyric reveal with key-wo… | npm:gsap |
| ARAB-49 | ✅ | قوالب الموشن العربية الثمانية · Eight Arabic motion templates | SP-0453 RTL whole-word lyric reveal with key-wo… | python3, chromium, npm:gsap, fonts:arabic |
| ARAB-50 | ✅ | شريط اسم سفلي تلقائي الاتجاه · Auto-RTL lower third | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-62 | ✅ | كاريوكي ASS عربي بثلاثة أنماط · Arabic ASS karaoke captions (reels · cinema · punchy) | SP-0453 RTL whole-word lyric reveal with key-wo… | ffmpeg, python3, imagemagick, fonts:arabic |
| ARAB-67 | ✅ | تقسيم الأسطر بالبرمجة الديناميكية · DP line breaking for lyrics & dua | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-81 | ✅ | إصلاح أسماء الملفات العربية المشوّهة · Arabic file-name mojibake repair | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-05 | 🟢 | مساحة التشكيل وحواف الأقنعة · Harakat headroom & mask padding | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-07 | 🟢 | كشف الاتجاه تلقائيًا · Auto RTL detection | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-18 | 🟢 | قواعد التايبوغرافي العربي الحركي · Kinetic Arabic grammar | SP-0453 RTL whole-word lyric reveal with key-wo… | node, python3, chromium |
| ARAB-20 | 🟢 | صعود الكلمات من الضباب · Rise-from-blur words | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-25 | 🟢 | انزلاق سطور عربية على Canvas · Canvas RTL staggered line slide | SP-0453 RTL whole-word lyric reveal with key-wo… | fonts:arabic |
| ARAB-28 | 🟢 | دخول الكلمة من العمق · 3D word turn-in from depth | SP-0453 RTL whole-word lyric reveal with key-wo… | chromium, npm:gsap |
| ARAB-34 | 🟢 | ضربة الكلمة المفتاحية بقناع صاعد · Keyword slam with upward mask | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-41 | 🟢 | تمييز الكلمة بالنجمة · *Asterisk* emphasis convention | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-55 | 🟢 | مكدّس عربي/إنجليزي · Bilingual Arabic/English stacks & HUD | SP-0453 RTL whole-word lyric reveal with key-wo… | fonts:arabic |
| ARAB-60 | 🟢 | كاروسيل عربي PNG/PDF · Arabic carousel renderer | SP-0453 RTL whole-word lyric reveal with key-wo… | pip:pillow, fonts:arabic |
| ARAB-72 | 🟢 | العزل الاتجاهي · Bidi isolation | SP-0453 RTL whole-word lyric reveal with key-wo… | ffmpeg |
| ARAB-76 | 🟢 | صيغ الجمع ومطابقة العدد · Plural & count agreement | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-83 | 🟢 | تسمية الألوان بالعربية · Arabic colour naming | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-89 | 🟢 | طبقات نص عربي على Canvas · Canvas RTL text-layer helpers | SP-0453 RTL whole-word lyric reveal with key-wo… | fonts:arabic |
| ARAB-22 | 📦 | كتابة بقناع ناعم ورأس قلم · Feathered RTL write-on with pen head | SP-0453 RTL whole-word lyric reveal with key-wo… | node |
| ARAB-66 | 📦 | فيلم الكلمات من الصوت · Verse film from sound (song · poem · dua) | SP-0453 RTL whole-word lyric reveal with key-wo… | pip:faster-whisper, fonts:arabic |
| ARAB-71 | 📦 | ستايل الكلمات العاطفي · Emotional lyric style preset | SP-0453 RTL whole-word lyric reveal with key-wo… | node, fonts:arabic |
| ARAB-80 | 📦 | تسميات عربية مُسقطة على الخرائط والعوالم · Projected Arabic labels (maps · isometric · charts) | SP-0453 RTL whole-word lyric reveal with key-wo… | npm:maplibre |
| ARAB-91 | 📦 | مصمم: نص عربي قابل للتعديل بتشكيل HarfRust وكشيدة · Mosamem: editable Arabic text with HarfRust shaping and kashida justification | SP-0453 RTL whole-word lyric reveal with key-wo… | pip:pillow |
| ARAB-32 | 👁 | كشف بالحبر وسحب التركيز · Ink-bleed / focus-pull word reveal | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-36 | 👁 | ضربة الكلمة البطلة بتوهج · Hero-word punch with bloom | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-42 | 👁 | خط متموّج تحت الكلمة المفتاحية · Squiggle underline highlight | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-43 | 👁 | ممسحة التظليل من اليمين · RTL highlighter swipe | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-56 | 👁 | بطاقة شخصية من اليمين · RTL character card | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-65 | 👁 | الكلمة المنطوقة تضيء · Spoken-word illumination (HTML captions) | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-03 | 📄 | لا تباعد ولا مطّ — الكشيدة فقط · No tracking, no stretch — kashida only | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-10 | 📄 | العربية داخل مشهد ثلاثي الأبعاد · Arabic inside 3D scenes | SP-0453 RTL whole-word lyric reveal with key-wo… | npm:three |
| ARAB-21 | 📄 | مسح القناع من اليمين · RTL clip wipe | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-23 | 📄 | قناع ضربة فرشاة · Brush-stroke mask write-on | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-37 | 📄 | الكلمة تمثّل معناها · Word acts out its meaning | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-70 | 📄 | النص المشكول مصدرًا للتوقيت · Vowelled source text over ASR | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-X01 | 📄 | كشف الكلمة العربية كاملة من اليمين · RTL whole-word lyric reveal with key-word pop | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-X03 | 📄 | الزخرفة والكشيدة للنبذة فقط · Unicode ornaments and kashida: bios only | SP-0453 RTL whole-word lyric reveal with key-wo… | — |
| ARAB-09 | ✅ | نص حقيقي فوق لوحات التوليد · Real type over generated plates | SP-0454 Legibility veils over footage | npm:remotion, key:video-gen, fonts:arabic |
| ARAB-68 | ✅ | اختيار الكلمة المفتاحية بالنبر · Stress-based keyword picking | SP-0454 Legibility veils over footage | — |
| ARAB-69 | ✅ | توحيد النص العربي للمطابقة · Arabic normalisation for alignment & matching | SP-0454 Legibility veils over footage | — |
| ARAB-39 | 🟢 | تعبئات مذهّبة ومتدرجة ولمعة عابرة · Gilded, gradient & sweeping fills | SP-0454 Legibility veils over footage | — |
| ARAB-40 | 🟢 | هرمية بثلاث مستويات · Three-level type hierarchy | SP-0454 Legibility veils over footage | — |
| ARAB-61 | 🟢 | طبقات نص الخط الزمني JSON · Timeline-JSON text overlays | SP-0454 Legibility veils over footage | — |
| ARAB-85 | 🟢 | قياس حركة النص وتصنيفها · Text-animation measurement & replay | SP-0454 Legibility veils over footage | ffmpeg, pip:numpy, pip:pillow, pip:opencv |
| ARAB-87 | 🟢 | ملاءمة العرض والتصغير التلقائي · Fit-width & shrink-to-fit | SP-0454 Legibility veils over footage | — |
| ARAB-16 | 📄 | سلّم أحجام الفيديو · Video type scale at 1080 px | SP-0454 Legibility veils over footage | — |
| ARAB-33 | 📄 | كلمات على مسار دائري · Words on a circular path | SP-0454 Legibility veils over footage | — |
| ARAB-64 | 📄 | منطقة الترجمة الآمنة وشكلها · Caption safe zone & look | SP-0454 Legibility veils over footage | fonts:arabic |
| ARAB-88 | 📄 | نص مشكّل في المشاهد المرسومة واستيراد SVG · Shaped text in painted scenes & SVG import | SP-0454 Legibility veils over footage | pip:pillow, fonts:arabic |
| ARAB-90 | 💡 | دوران كتلة النص 90° ككاميرا · Type-block 90° rotation as camera move | SP-0454 Legibility veils over footage | — |
| ARAB-12 | ✅ | كايرو المقسوم بنطاق يونيكود · Cairo split by unicode-range | SP-0455 Arabic font voice map | fonts:arabic |
| ARAB-15 | ✅ | اقترانات الخطوط · Type pairings | SP-0455 Arabic font voice map | fonts:arabic |
| ARAB-U01 | ✅ | خط El Messiri العربي مضمّن · El Messiri Arabic display font bundled (OFL) | SP-0455 Arabic font voice map | pip:pillow, fonts:arabic |
| ARAB-X04 | ✅ | مطابقة الخط عبر محرك تشكيل حقيقي · Font matching through a real shaper (Chromium/HarfBuzz) | SP-0455 Arabic font voice map | node, chromium, pip:pillow, fonts:arabic |
| ARAB-X05 | ✅ | تجميع عائلة خط مطابقة من مصدرين OFL · Assemble a matched OFL family from two masters | SP-0455 Arabic font voice map | pip:fonttools, fonts:arabic |
| ARAB-04 | 🟢 | بوابة تحميل الخط قبل الإطار الأول · Font-ready gate before frame 0 | SP-0455 Arabic font voice map | npm:remotion, fonts:arabic |
| ARAB-11 | 🟢 | خريطة أصوات الخطوط · Arabic font voice map | SP-0455 Arabic font voice map | fonts:arabic |
| ARAB-13 | 🟢 | اكتشاف الخطوط وسلسلة البدائل · Font discovery & fallback chain | SP-0455 Arabic font voice map | ffmpeg, pip:pillow, pip:fonttools, npm:remotion … |
| ARAB-14 | 🟢 | محمّل الخطوط الحي ومنتقي الخط · Live Google Fonts loader & picker | SP-0455 Arabic font voice map | fonts:arabic |
| ARAB-17 | 🟢 | سلّم القراءة للشاشات · Screen reading scale (v17 / SQC) | SP-0455 Arabic font voice map | fonts:arabic |
| ARAB-86 | 🟢 | مطابقة الخط بالحبر · Font matching by ink | SP-0455 Arabic font voice map | — |
| ARAB-92 | 📄 | أربعة خطوط عربية مفتوحة يرفقها مصمم · Four open Arabic fonts bundled by Mosamem (IBM Plex Sans Arabic, Cairo, Tajawal, Amiri) | SP-0455 Arabic font voice map | fonts:arabic |
| ARAB-X02 | 📄 | ترشيح الخط لا الجزم به · Font matches are candidates, not identities | SP-0455 Arabic font voice map | pip:pillow, npm:three |
| ARAB-24 | ✅ | سطور تصعد من خلف خط قطع · Lines rising behind a cut line | SP-0456 Stacked headline lines that dim | — |
| ARAB-47 | 🟢 | خط مضيء يتمدد تحت العنوان · Growing glow rule under the title | SP-0456 Stacked headline lines that dim | — |
| ARAB-57 | 🟢 | عنوان عربي سينمائي فوق الفيديو · Cinematic Arabic headline over footage | SP-0456 Stacked headline lines that dim | — |
| ARAB-59 | 🟢 | غلاف بعنوان عربي مشكّل · Shaped Arabic cover / thumbnail | SP-0456 Stacked headline lines that dim | pip:pillow, pip:arabic-reshaper |
| ARAB-48 | 👁 | سطور تتكدس وتخفت · Stacked headline lines that dim | SP-0456 Stacked headline lines that dim | — |
| ARAB-77 | 📄 | رقم يتحول إلى عنوان · Number → headline | SP-0456 Stacked headline lines that dim | — |
| ARAB-79 | 📄 | الدعوة والسعر بالعربية · Arabic CTA & price isolation | SP-0456 Stacked headline lines that dim | — |
| ARAB-74 | ✅ | منسّق الأرقام الهندية الحتمي · Deterministic Arabic-Indic money formatter | SP-0457 One digit system + tabular figures | node |
| ARAB-54 | 🟢 | أقراص وشارات وأرقام مرقّمة · Pills, chips & numbered badges | SP-0457 One digit system + tabular figures | — |
| ARAB-73 | 🟢 | نظام أرقام واحد وأرقام جدولية · One digit system + tabular figures | SP-0457 One digit system + tabular figures | — |
| ARAB-75 | 🟢 | قراءة الأرقام والوحدات العربية · Digit parsing & number/unit detection | SP-0457 One digit system + tabular figures | — |
| ARAB-27 | 📦 | عنوان Remotion بنابض وأقراص كلمات · Remotion spring title + keyword pills | SP-0457 One digit system + tabular figures | npm:remotion, npm:react |
| ARAB-31 | 👁 | كبسولة الكلمات الدوّارة · Rolling word pill with growing rings | SP-0457 One digit system + tabular figures | — |
| ARAB-84 | ✅ | التقاط ستايل النص وإعادة تركيبه · Text-style capture & compositing | SP-0458 Giant outlined question mark | tesseract |
| ARAB-45 | 🟢 | علامة استفهام عملاقة مفرّغة · Giant outlined question mark | SP-0458 Giant outlined question mark | — |
| ARAB-30 | 👁 | كلمة ضخمة من الضباب تنكمش إلى سطر · Blur-in hero word that shrinks into the sentence | SP-0458 Giant outlined question mark | — |
| ARAB-46 | 👁 | ظل مزدوج مزاح · Offset duotone shadow hero | SP-0458 Giant outlined question mark | — |
| ARAB-38 | 📄 | صدى طباعي يتلاشى · Typographic echo | SP-0458 Giant outlined question mark | — |
| ARAB-78 | 📄 | حوار طباعي · Typographic dialogue | SP-0458 Giant outlined question mark | — |
| ARAB-X06 | ✅ | عنوان خطي مركّب من حدود حروف مفتوحة · Composed calligraphic title from OFL outlines | SP-0459 Per-shot ASS animated title card | python3, fonts:arabic |
| ARAB-53 | 🟢 | ترويسة اليوم بالهجري والميلادي · Hijri + Gregorian day header | SP-0459 Per-shot ASS animated title card | fonts:arabic |
| ARAB-58 | 🟢 | عنوان ASS متحرك لكل لقطة · Per-shot ASS animated title card | SP-0459 Per-shot ASS animated title card | ffmpeg |
| ARAB-82 | 🟢 | سطر الحقوق الآمن · Safe credit-line burn | SP-0459 Per-shot ASS animated title card | ffmpeg |
| ARAB-63 | 📄 | قانون زمن القراءة والكثافة · Reading-time & density law | SP-0459 Per-shot ASS animated title card | — |
| ARAB-26 | ✅ | عنوان كلمات بنابض كل 160 مللي ثانية · Spring word-stagger title | SP-0460 Hook title looks: box · kinetic · minim… | npm:remotion, fonts:arabic |
| ARAB-29 | 🟢 | الآلة الكاتبة بمؤشر · Typewriter with caret | SP-0460 Hook title looks: box · kinetic · minim… | — |
| ARAB-51 | 📦 | ثلاثة أشكال لعنوان الخطاف · Hook title looks: box · kinetic · minimal | SP-0460 Hook title looks: box · kinetic · minim… | node, fonts:arabic |
| ARAB-52 | 📄 | صندوق عنوان يحافظ على مركزه · Centre-locked resizing title box | SP-0460 Hook title looks: box · kinetic · minim… | — |

## typography-latin (motion)

chapter: [typography-latin](../powers/typography-latin.md) · card: `usip-library/cards/type/typography-latin.md` · tools: `font-fidelity-lab` · `render-text` · `telegram-typography-atlas`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| TYPE-79 | ✅ | عنوان سينمائي متباعد الحروف · Letter-spaced cinematic title | SP-0461 Multi-voice type systems | node |
| TYPE-11 | 🟢 | خطوط لاتينية مدمجة جاهزة · Owner-bundled Latin fonts (offline) | SP-0461 Multi-voice type systems | fonts:arabic |
| TYPE-12 | 🟢 | تضمين الخطوط داخل الملف · Offline font inlining (base64) | SP-0461 Multi-voice type systems | npm:gsap, npm:hyperframes, key:openai |
| TYPE-13 | 🟢 | مجموعة Google Fonts للتبديل الحي · Curated Google Fonts swap set | SP-0461 Multi-voice type systems | — |
| TYPE-53 | 🟢 | غروتسك عريض مع كلمة سيريف مائلة · Grotesk + italic-serif accent | SP-0461 Multi-voice type systems | fonts:arabic |
| TYPE-82 | 🟢 | الشرائط السفلية ولوحات الأسماء · Lower-thirds & name plates | SP-0461 Multi-voice type systems | — |
| TYPE-07 | 📦 | ملاءمة النص للعرض وقياسه · Fit-to-width & text measuring | SP-0461 Multi-voice type systems | npm:remotion, npm:hyperframes |
| TYPE-80 | 📦 | بطاقة عنوان هادئة وقفل الشعار · Calm title card & lockup | SP-0461 Multi-voice type systems | npm:hyperframes |
| TYPE-10 | 🔑 | حدود النص داخل صور الذكاء الاصطناعي · Text-in-AI-image ladder | SP-0461 Multi-voice type systems | key:video-gen |
| TYPE-54 | 👁 | عنوان سيريف تحريري بكلمة مائلة · Editorial serif headline & keyword title | SP-0461 Multi-voice type systems | fonts:arabic |
| TYPE-81 | 👁 | بطاقات الفصول والأرقام الضخمة · Numbered chapter blocks & giant-number cards | SP-0461 Multi-voice type systems | — |
| TYPE-83 | 👁 | أنظمة الأصوات الطباعية · Multi-voice type systems | SP-0461 Multi-voice type systems | pip:faster-whisper |
| TYPE-85 | 👁 | تكديس هرمي بأحجام متدرجة · Size-stepped hierarchy stacks | SP-0461 Multi-voice type systems | — |
| TYPE-86 | 👁 | عنوان سيريف متراكب يُبنى كلمة كلمة · Stacked serif title build | SP-0461 Multi-voice type systems | — |
| TYPE-87 | 👁 | بطاقة حرف أو كلمة بملء الشاشة · Full-bleed glyph & word cards | SP-0461 Multi-voice type systems | — |
| TYPE-88 | 👁 | تجميع المعادلات · Equation assembly | SP-0461 Multi-voice type systems | — |
| TYPE-01 | 📄 | مقاسات الخط للفيديو · Video type sizing & contrast | SP-0461 Multi-voice type systems | — |
| TYPE-02 | 📄 | ميزانية الكلمات والأسطر · Word & line budgets (on-screen copy ≠ narration) | SP-0461 Multi-voice type systems | — |
| TYPE-03 | 📄 | زمن القراءة والثبات · Read-time & hold rules | SP-0461 Multi-voice type systems | — |
| TYPE-05 | 📄 | اختيار الخط وتزويجه · Choosing & pairing faces | SP-0461 Multi-voice type systems | fonts:arabic |
| TYPE-06 | 📄 | أرقام جدولية وخصائص OpenType · Tabular numerals & OpenType features | SP-0461 Multi-voice type systems | — |
| TYPE-08 | 📄 | نص SVG حاد وهالات التسميات · Crisp SVG text & label halos | SP-0461 Multi-voice type systems | — |
| TYPE-09 | 📄 | تراخيص الخطوط ونظافتها · Font licensing & font hygiene | SP-0461 Multi-voice type systems | pip:pillow, npm:hyperframes, fonts:arabic |
| TYPE-89 | 📄 | استايلات حركية في الكتالوج · Catalog kinetic styles: brutalist · minimal · typewriter | SP-0461 Multi-voice type systems | node, python3, chromium |
| TYPE-90 | 📄 | تزويجات ولوحات جاهزة للعناوين · Preset pairings & palettes for title systems | SP-0461 Multi-voice type systems | npm:hyperframes |
| TYPE-X02 | 📄 | ثلاث عائلات خطوط بمصدر واحد · Three font families from one source of truth | SP-0461 Multi-voice type systems | — |
| TYPE-14 | 🟢 | صعود من خلف خط القاعدة · Baseline mask rise (lines & words) | SP-0462 Baseline mask rise (lines & words) | python3, npm:gsap |
| TYPE-15 | 🟢 | صعود من حالة جزئية · Rise from a partial state (riseWords) | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-27 | 🟢 | عنوان قماشي من 1–4 كلمات مع اتجاه تلقائي · Canvas 1–4-word headline with auto-RTL | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-16 | 📦 | ظهور من الضباب (سحب البؤرة) · Blur-to-sharp focus pull | SP-0462 Baseline mask rise (lines & words) | npm:hyperframes |
| TYPE-18 | 📦 | تتابع الحروف سقوطًا وصعودًا · Per-letter drop & rise cascades | SP-0462 Baseline mask rise (lines & words) | npm:hyperframes |
| TYPE-19 | 📦 | تبعثر وتدحرج وتجميع · Scatter, tumble & gravity assemble | SP-0462 Baseline mask rise (lines & words) | npm:hyperframes |
| TYPE-20 | 📦 | تقارب الحروف · Tracking-in collapse (Latin only) | SP-0462 Baseline mask rise (lines & words) | npm:hyperframes |
| TYPE-21 | 📦 | تكديس الأسطر ودفعها وتبديلها · Line stack, push & swap | SP-0462 Baseline mask rise (lines & words) | npm:hyperframes |
| TYPE-23 | 📦 | بناء من المركز · Kinetic center build | SP-0462 Baseline mask rise (lines & words) | npm:hyperframes |
| TYPE-17 | 👁 | إضاءة الكلمات بترتيب القراءة · Reading-order light-up & blur manifesto | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-25 | 👁 | كشف بالشرائح · Strip-slice letter reveal | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-26 | 👁 | بناء الكلمة على شبكة إنشائية · Construction-grid & guide-line build | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-28 | 👁 | موجة الحروف · Per-letter sine bounce & wave | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-22 | 📄 | الدخول الشلالي · Waterfall entry cascade | SP-0462 Baseline mask rise (lines & words) | npm:gsap |
| TYPE-24 | 📄 | مسح الكلمة الكبيرة بالقناع · Clip-path big-word wipe | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-29 | 📄 | مفردات حركة النص للستوري بورد · Text-motion vocabulary for storyboards | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-30 | 📄 | الكلمة المختفية · Invisible-word blink | SP-0462 Baseline mask rise (lines & words) | — |
| TYPE-63 | 🟢 | طباعة شبحية خلفية · Giant ghost background type & ghost rows | SP-0463 Extruded & stacked-shadow type | npm:hyperframes |
| TYPE-61 | 📦 | الخط المتغير: محاور ووزن متموج وعرض · Variable-font motion: axis tween, weight wave, width swell | SP-0463 Extruded & stacked-shadow type | npm:hyperframes, fonts:arabic |
| TYPE-62 | 📦 | خط مفرّغ: أرقام مجوفة ومن محيط إلى تعبئة · Outline type: hollow numerals, outline → fill, glowing outline | SP-0463 Extruded & stacked-shadow type | npm:hyperframes |
| TYPE-67 | 📦 | نص لزج متحول · Gooey morph text | SP-0463 Extruded & stacked-shadow type | npm:gsap, npm:hyperframes |
| TYPE-68 | 📦 | حروف منفوخة بالفيزياء · Inflated physics letterforms | SP-0463 Extruded & stacked-shadow type | npm:matter |
| TYPE-64 | 👁 | نص بارز بظلال مكدسة · Extruded & stacked-shadow type | SP-0463 Extruded & stacked-shadow type | npm:hyperframes |
| TYPE-65 | 👁 | أثر الصدى والنسخ المحيطية · Echo trail & outline echo stack | SP-0463 Extruded & stacked-shadow type | — |
| TYPE-66 | 👁 | نص مملوء بصورة أو فيديو · Image- & video-filled text | SP-0463 Extruded & stacked-shadow type | — |
| TYPE-69 | 👁 | جسيمات تتجمع لتكوّن كلمة · Particles assemble into a word | SP-0463 Extruded & stacked-shadow type | — |
| TYPE-70 | 👁 | خط الخلايا: ASCII ونقاط المصفوفة · Cell-based type: ASCII blocks & dot-matrix numerals | SP-0463 Extruded & stacked-shadow type | — |
| TYPE-04 | 📄 | سلّم الأحجام والأوزان والتباعد · Scale, weight, leading & tracking tokens | SP-0463 Extruded & stacked-shadow type | npm:react |
| TYPE-X01 | 📄 | نص يعبر القطع · Type that keeps moving through cuts | SP-0463 Extruded & stacked-shadow type | — |
| TYPE-49 | 📦 | قلم التظليل والخط السفلي · Highlighter & underline swipe | SP-0464 Two-tone lines & accent-word colour | npm:hyperframes |
| TYPE-51 | 📦 | شطب واستبدال · Strike-through & replace | SP-0464 Two-tone lines & accent-word colour | npm:hyperframes |
| TYPE-50 | 👁 | كلمات داخل كبسولات · Keyword pills | SP-0464 Two-tone lines & accent-word colour | — |
| TYPE-52 | 👁 | عنوان بلونين وكلمة لون · Two-tone lines & accent-word colour | SP-0464 Two-tone lines & accent-word colour | — |
| TYPE-55 | 👁 | تعبئة متدرجة ومعدنية · Gradient & metallic word fills | SP-0464 Two-tone lines & accent-word colour | — |
| TYPE-56 | 👁 | أقواس تحديد وصندوق أداة تصميم · Selection brackets & design-tool bounding box | SP-0464 Two-tone lines & accent-word colour | — |
| TYPE-57 | 👁 | صور ووجوه وأيقونات داخل السطر · Inline avatars & icons inside a headline | SP-0464 Two-tone lines & accent-word colour | — |
| TYPE-58 | 👁 | الكلمة تؤدي معناها · Word performs its meaning | SP-0464 Two-tone lines & accent-word colour | — |
| TYPE-59 | 👁 | قوائم تخفت السابق · Dim-previous stacks & active-item lists | SP-0464 Two-tone lines & accent-word colour | — |
| TYPE-60 | 👁 | النقطة الختامية وإبدال الحرف · Full-stop dot & glyph substitution | SP-0464 Two-tone lines & accent-word colour | — |
| TYPE-31 | 🟢 | آلة كاتبة متدرجة بمؤشر · Eased typewriter with caret (typeOn) | SP-0465 Human typing: typos, backspace, caret s… | npm:gsap, npm:hyperframes |
| TYPE-33 | 🟢 | فك التشفير · Scramble / decode reveal | SP-0465 Human typing: typos, backspace, caret s… | — |
| TYPE-37 | 🟢 | عدّاد بأرقام جدولية · Tabular counter (MOTION.counter) | SP-0465 Human typing: typos, backspace, caret s… | — |
| TYPE-32 | 📦 | كتابة بشرية: أخطاء ومسح ومؤشر ملوّن · Human typing: typos, backspace, caret swap | SP-0465 Human typing: typos, backspace, caret s… | npm:hyperframes |
| TYPE-35 | 📦 | لوحة المطار القلّابة · Split-flap (Solari) board | SP-0465 Human typing: typos, backspace, caret s… | npm:gsap, npm:hyperframes |
| TYPE-38 | 📦 | بكرة الكلمات وعدّاد نابض · Slot-machine word roll & spring ticker | SP-0465 Human typing: typos, backspace, caret s… | npm:gsap, npm:hyperframes |
| TYPE-39 | 📦 | تبديل كلمة في خانة ثابتة واستيلاء الشريط · Word-slot swap & ticker takeover | SP-0465 Human typing: typos, backspace, caret s… | npm:hyperframes |
| TYPE-36 | 👁 | عدّاد الأسطوانة الدوّار · Odometer digit roll | SP-0465 Human typing: typos, backspace, caret s… | — |
| TYPE-34 | 📄 | قلب الحروف ثلاثي الأبعاد · Hacker-flip 3D decode | SP-0465 Human typing: typos, backspace, caret s… | npm:gsap |
| TYPE-40 | ✅ | إيقاع البادئة/البطل/الذيل · Lead / hero / tail beat splitter | SP-0466 Headline slam & beat word punch | node |
| TYPE-46 | 🟢 | كلمة بانفصال RGB وتشويش · RGB-split glitch word | SP-0466 Headline slam & beat word punch | — |
| TYPE-41 | 📦 | صدمة العنوان وضربة الكلمة على الإيقاع · Headline slam & beat word punch | SP-0466 Headline slam & beat word punch | npm:hyperframes |
| TYPE-47 | 📦 | بدائيات حركة النص على الموسيقى · Music-anchored type primitives & templates | SP-0466 Headline slam & beat word punch | npm:gsap, npm:hyperframes |
| TYPE-42 | 👁 | متتاليات الضرب وجمل تُبنى بالضربات · Beat-slam sequences & stacked statements | SP-0466 Headline slam & beat word punch | npm:hyperframes |
| TYPE-44 | 👁 | ختم وملصق وكلمة مؤثر صوتي · Stamp, sticker & SFX word pop | SP-0466 Headline slam & beat word punch | — |
| TYPE-45 | 👁 | انزلاق بضبابية حركة ولطخة لونية · Motion-blur slide, smear & stretch | SP-0466 Headline slam & beat word punch | — |
| TYPE-43 | 📄 | وصفة سطر الافتتاح · Hook-line recipe & kinetic-type beats | SP-0466 Headline slam & beat word punch | — |
| TYPE-48 | 💡 | نص بإطارات ممسوكة · Held-frame stepped type | SP-0466 Headline slam & beat word punch | — |
| TYPE-72 | 👁 | نص على حلقات ومدارات · Text rings & orbiting words | SP-0467 Text rings & orbiting words | — |
| TYPE-73 | 👁 | نفق النص ودوامته · Circular text tunnel & spiral vortex | SP-0467 Text rings & orbiting words | — |
| TYPE-74 | 👁 | أسطوانة نص ثلاثية الأبعاد وشرائط حلزونية · 3D text cylinder & helix ribbons | SP-0467 Text rings & orbiting words | — |
| TYPE-75 | 👁 | جدار الشرائط المتعاكسة · Bidirectional marquee wall | SP-0467 Text rings & orbiting words | — |
| TYPE-76 | 👁 | شريط مائل وجدار منظوري · Tilted ticker band & perspective word wall | SP-0467 Text rings & orbiting words | — |
| TYPE-78 | 👁 | كلمات كعمارة ودوران الأرباع · Words as architecture & quadrant rotation | SP-0467 Text rings & orbiting words | — |
| TYPE-77 | 💡 | جدار نص يندفع وينضغط إلى شعار · Text-wall rush & compress into a logo | SP-0467 Text rings & orbiting words | — |
| TYPE-U01 | ✅ | خط Poppins مضمّن · Poppins bundled (OFL) | SP-0468 Caption readability rules over footage | pip:pillow, fonts:arabic |
| TYPE-84 | 👁 | مظهر الترجمة حسب النبرة والعالم · Caption look by tone & theme | SP-0468 Caption readability rules over footage | — |
| TYPE-71 | 📄 | كلمات مدمجة داخل اللقطة · Words embedded in footage (composition craft) | SP-0468 Caption readability rules over footage | — |
| TYPE-U02 | 📄 | قواعد قراءة الترجمة فوق اللقطات · Caption readability rules over footage | SP-0468 Caption readability rules over footage | — |
