# برومو تطبيق Lidlezz لخلاصة X المربعة — Lidlezz app promo

> برومو مربع 15 ثانية لتطبيق Lidlezz مصمم للتشغيل الصامت في خلاصة X: هاتف واحد يعرض ثلاث ميزات ودعوة واضحة للتنزيل.
>
> A 15-second square promo for the Lidlezz app, built for silent autoplay in the X feed: one phone, three feature callouts and a clear CTA.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/cansincengiz-me-cf68dd
- التصنيفات / Categories: product-ui
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
الموضوع برومو لتطبيق سيُعرض على جمهور يقارب عشرة آلاف شخص في خلاصة X، لذا الهدف أن يُفهم في أول ثانيتين دون صوت وبإطار مربع. اللغة الحركية مبنية حول هاتف واحد يميل قليلًا وتتبدل شاشاته بانتقالات حقيقية من الهيكل الرمادي إلى الواجهة الفعلية، مع تعليقات ميزات تشير إلى مناطق محددة في الشاشة. ما يميزها الانضباط: نص كبير داخل هوامش آمنة، وحركة واحدة مهيمنة في كل لحظة، وإطار أخير ثابت يصلح صورة مصغرة.

## Concept
The subject is a promo for an app that will reach an audience of around ten thousand in the X feed, so the goal is to be understood in the first two seconds, without sound, inside a square frame. The motion language is built around one slightly tilted phone whose screens change through real transitions from grey skeleton to live UI, with feature callouts pointing at specific regions of the screen. Its distinctive trait is discipline: large text inside safe margins, one dominant motion at a time, and a still end frame that doubles as a thumbnail.

## المشاهد المقترحة
- 0-1.5 ث: أيقونة التطبيق تهبط في مركز الإطار المربع بارتداد ناعم؛ اسم التطبيق يُختم أسفلها بخط sans مستدير بحجم 120 px.
- 1.5-5 ث: هيكل هاتف يرتفع من الحافة السفلية بميل 8° على المحور Y؛ الشاشة الأولى تُحمَّل بانتقال من الهيكل الرمادي إلى المحتوى الفعلي خلال 400 ms.
- 5-9 ث: ثلاث تعليقات ميزات تظهر واحدة تلو الأخرى على اليسار، كل منها تشير إلى منطقة مميزة في الواجهة؛ الشاشة تتمرر 240 px بين كل تعليق وآخر.
- 9-12 ث: الهاتف ينقلب 180° ليكشف شاشة ثانية؛ تموّج لمسة يطلق حالة نجاح (علامة صح تتشكل من دائرة).
- 12-15 ث: الهاتف يتقلص إلى الزاوية، والفائدة الرئيسية تملأ المربع، وزر الدعوة ينبض مرتين قبل أن يتجمد الإطار الأخير 500 ms.

## Proposed scenes
- 0-1.5s: The app icon drops into the centre of the square frame with a soft bounce; the app name stamps in below in a 120 px rounded sans.
- 1.5-5s: A phone mockup rises from the bottom edge, tilted 8° on Y; the first screen loads with a skeleton-to-content transition (grey blocks fill with real UI in 400 ms).
- 5-9s: Three feature callouts appear one by one on the left, each pointing to a highlighted UI region; the screen scrolls 240 px between callouts.
- 9-12s: The phone flips 180° to reveal a second screen; a tap ripple triggers a success state (checkmark morphing from a circle).
- 12-15s: The phone shrinks into the corner, the headline benefit fills the square, and a CTA button pulses twice before the end frame freezes for 500 ms.

## قواعد الحركة
- مصمم للتشغيل الصامت: كل مقطع يجب أن يُقرأ دون صوت؛ الإطار الأول يُظهر الأيقونة واسم التطبيق بعتامة كاملة بعد 300 ms.
- المنطقة الآمنة: هوامش 80 px من الجهات الأربع في إطار 1080×1080؛ لا نص أصغر من 48 px؛ العنوان 96 px أو أكبر.
- ارتداد الأيقونة بـ cubic-bezier(0.34, 1.56, 0.64, 1) خلال 600 ms؛ وكل دخول آخر بـ cubic-bezier(0.2, 0.8, 0.2, 1) خلال 500 ms.
- ميل الهاتف لا يتجاوز ±8° على المحور Y؛ الانقلاب 180° يستغرق 700 ms مع تبديل محتوى الشاشة عند منتصف الدوران 90°.
- التمرير داخل الشاشة 240 px خلال 600 ms بـ ease-in-out؛ التعليقات تظهر بعد 150 ms من انتهاء التمرير، لا أثناءه.
- اللوحة: لون هوية التطبيق الحقيقي، والأبيض، ولون محايد داكن واحد؛ التمييز محجوز لعلامات التعليقات وزر الدعوة.
- الإطار الأخير يثبت تمامًا آخر 500 ms كي تكون الصورة المصغرة في الخلاصة نظيفة.
- ممنوع: فقاعات إشعارات مزيفة، والوميض أو الومضات، والنص الدقيق، وعرض أكثر من هاتف في اللحظة نفسها.

## Motion rules
- Designed for muted autoplay: every beat must be legible without audio; the first frame already shows the icon and app name at full opacity after 300 ms.
- Safe area: 80 px margins on all four sides of the 1080×1080 frame; no text smaller than 48 px; headline at 96 px or larger.
- Icon bounce uses cubic-bezier(0.34, 1.56, 0.64, 1) over 600 ms; every other entrance uses cubic-bezier(0.2, 0.8, 0.2, 1) over 500 ms.
- Phone tilt stays within ±8° on Y; the 180° flip takes 700 ms with the screen content swapping at the 90° midpoint.
- In-screen scrolling moves 240 px over 600 ms with ease-in-out; callouts appear 150 ms after the scroll ends, never during it.
- Palette: the app's real brand colour, white and one dark neutral; the accent is reserved for callout markers and the CTA button.
- The end frame holds completely still for the final 500 ms so the feed thumbnail is clean.
- Banned: fake notification bubbles, flashing or strobing, fine print, and showing more than one phone at a time.

## Facts stated by the source (rewritten in our words)
- The request is written in Turkish.
- A 15-second length is stated explicitly.
- The video promotes a product behind a shortened link, which the catalogue identifies as Lidlezz.
- The creator plans to show it to roughly ten thousand people on X.
- Tagged product UI; features, screens and colours are not described.

## Assumptions
The app's purpose, screens and brand colour are unknown and must come from the real product; the feed-first, silent-autoplay structure is a proposal driven by the stated X audience, and the 1:1 aspect is taken from the input dimensions.

## Keywords
app promo, phone mockup, feature callouts, skeleton loading, square video, x feed, silent autoplay, cta, برومو تطبيق, هاتف, واجهة مستخدم, فيديو مربع, دعوة لاتخاذ إجراء
