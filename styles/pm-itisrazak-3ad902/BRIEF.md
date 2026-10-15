# ريل ديستيل بوك: من كتاب كامل إلى خلاصة — Distilbook motion showreel

> ريل منتج مدته 40 ثانية يحوّل فكرة اختصار الكتب إلى لغة حركية: جدران نص تنضغط إلى عناوين، وبطاقات ملخّصات، ورسوم بيانية تعدّ الوقت الموفَّر.
>
> A 40-second product showreel where the idea of condensing books becomes motion: text walls compress into headlines, summary cards flip and charts count saved time.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/itisrazak-3ad902
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 40 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع هو منتج Distilbook (نفترض أنه أداة لتلخيص الكتب واستخلاص أفكارها، لأن النص المصدري يطلب البحث عنه دون وصفه). الهدف التواصلي أن يشعر المشاهد بأن قراءة مئات الصفحات تتحول إلى دقائق، وأن المصمم قادر على الإبهار. اللغة الحركية تقوم على مبدأ الانضغاط: كل عنصر يبدأ كثيفاً ومزدحماً ثم ينضغط إلى شكل نقي وواضح، مع كاميرا واحدة تتحرك بلا انقطاع.

## Concept
The subject is the Distilbook product (assumed to be a book-summarising tool; the source only asks to research it). The goal is to make the viewer feel hundreds of pages collapsing into minutes while proving the designer's range. The motion language is built on compression: every element starts dense and crowded, then squeezes into a clean, legible form, carried by one continuous camera move.

## المشاهد المقترحة
- 0-3 ث: إطار أسود. كلمة واحدة تتفتح حرفاً حرفاً، ثم يندفع جدار من الفقرات نحو العدسة حتى يملأ الشاشة.
- 3-9 ث: يطوى جدار النص سطراً بعد سطر وينضغط إلى عنوان واحد عريض؛ ينشق العنوان ليكشف الشعار المبني من ضرباته.
- 9-17 ث: ثلاث لقطات للمنتج: كومة أغلفة كتب تنقلب إلى بطاقات ملخّص، مسحة قلم تمييز تعزل الجمل المفتاحية، ورسم أعمدة يقارن زمن القراءة بزمن الخلاصة مع عدّاد صاعد.
- 17-26 ث: جولة نص حركي: عبارات فائدة قصيرة تضرب على الإيقاع بينما تتقدم الكاميرا داخل ممر من الكلمات الضخمة.
- 26-34 ث: لحظة البيانات: رسم خطي لعدد الكتب المنجزة شهرياً يرسم نفسه، وقطاعات دائرية تمتلئ، وثلاث بطاقات شهادات ترتفع بتوقيت متدرج.
- 34-40 ث: تتقارب العناصر كلها إلى نقطة واحدة، تتمدد النقطة إلى الشعار، ويثبت الشعار مع السطر الختامي ودعوة الإجراء آخر ثانيتين.

## Proposed scenes
- 0-3s: Black frame. A single word blooms letter by letter, then a wall of paragraphs rushes toward the lens until it fills the screen.
- 3-9s: The text wall folds inward line by line and compresses into one bold headline; the headline splits to reveal the logo built from its strokes.
- 9-17s: Three product beats: a stack of book covers flips into summary cards, a highlighter sweep isolates key sentences, a bar chart of reading time versus summary time counts up.
- 17-26s: Kinetic type run: short benefit phrases punch in on the beat while the camera dollies down a corridor of oversized words.
- 26-34s: Data moment: a line chart of books finished per month draws itself, donut segments fill, and three testimonial cards rise with staggered timing.
- 34-40s: Every element converges back into a single dot, the dot expands into the logo lockup, tagline and call to action hold for the final 2 seconds.

## قواعد الحركة
- الدخولات تستخدم cubic-bezier(0.16, 1, 0.3, 1) بمدة 600-800 ms؛ أما لقطات الانضغاط فتستخدم ease-in-out بقيمة cubic-bezier(0.65, 0, 0.35, 1) بمدة 1200 ms ليبدو العصر مقصوداً.
- كاميرا افتراضية واحدة متصلة طوال 40 ثانية: تقدم وتحريك جانبي فقط، الدوران لا يتجاوز 12 درجة، بلا قطع؛ تغيّر المشاهد عبر match-cut بالتكبير حيث يملأ عنصر الإطار ويتحول إلى خلفية المشهد التالي.
- الطباعة بعائلة grotesk واحدة؛ الوزن يتحرك حياً من 300 إلى 800 على الكلمات البطلة، والتدرج بين الحروف 30 ms لكل حرف، ولا يتحرك أكثر من 12 حرفاً معاً.
- الرسوم البيانية ترسم من الصفر عبر stroke-dashoffset خلال 900 ms؛ العدّادات تستخدم easeOutExpo وتستقر على قيمتها النهائية قبل اكتمال الرسم بـ150 ms.
- اللون: قاعدة داكنة واحدة، سطح فاتح ورقي، ولون تمييز واحد؛ لون التمييز محجوز للبيانات والشعار ولا يستخدم للزينة.
- لا تزيد المجموعات المتحركة باستقلال عن ثلاث في أي إطار؛ العناصر الثانوية تثبت بينما يتحرك العنصر البطل.
- مزامنة الصوت: كل ضربة دخول تقع ضمن إطارين من علامة الإيقاع عند 100-110 BPM؛ تثبيت الشعار الختامي 48 إطاراً على الأقل.
- ممنوع: crossfade، طبقات glitch، ظلال أسمك من 2 px، أصوات whoosh جاهزة، أكثر من عائلة خط واحدة.

## Motion rules
- Entrances use cubic-bezier(0.16, 1, 0.3, 1) over 600-800 ms; the compression beats use ease-in-out cubic-bezier(0.65, 0, 0.35, 1) over 1200 ms so the squeeze reads as deliberate.
- One continuous virtual camera for the whole 40 s: dolly and pan only, rotation capped at 12 degrees, no cuts; scene changes happen through scale match-cuts where an element fills the frame and becomes the next scene's background.
- Typography is a single grotesk family; weight animates live from 300 to 800 on hero words, and letter stagger is 30 ms per glyph, never more than 12 glyphs animating at once.
- Charts draw from zero with stroke-dashoffset over 900 ms; counters use easeOutExpo and land on their final value 150 ms before the chart finishes.
- Colour: one dark base, one paper-light surface, one accent; the accent is reserved for data and the logo, never for decoration.
- Maximum three independently moving groups on screen at any frame; secondary elements hold still while a hero element moves.
- Audio sync: every punch-in lands within 2 frames of a beat marker at 100-110 BPM; hold the final lockup for 48 frames minimum.
- Banned: crossfades, glitch overlays, drop shadows thicker than 2 px, stock whoosh sounds, more than one font family.

## Facts stated by the source (rewritten in our words)
- The creator asked for a 40-second motion graphics piece about Distilbook, framed as a designer's showreel.
- The creator asked the AI to research the product itself; no features, colours or structure are described in the prompt.
- Tagged on the site as charts and kinetic type.

## Assumptions
Stated: 40-second duration, Distilbook as subject, showreel framing, chart and kinetic-type tags. Assumed: that Distilbook condenses books, the compression metaphor, the six-beat structure, all timings, easing values and colour roles.

## Keywords
showreel, product reel, book summary, تلخيص كتب, نص حركي, compression, match cut, bar chart, counter, ريل منتج, grotesk, عدّاد, رسم بياني, distilbook
