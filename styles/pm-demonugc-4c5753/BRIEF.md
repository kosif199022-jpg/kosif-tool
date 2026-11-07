# حلقة تحولات عناصر الواجهة من حالة إلى أخرى — Morphing UI states loop

> حلقة مربعة صامتة مدتها 14 ثانية على خلفية بيضاء مكسورة: عنصر واجهة أسود صغير واحد يتحول باستمرار من حالة إلى أخرى بنقرات مؤشر: زر «Continue» يصبح مؤشر تحميل دائري، ثم مشغل موسيقى صغير بشريط تقدم أخضر، ثم شريط تقدم، ثم مفتاح يتحول إلى الأخضر، ثم شريط ألسنة، ثم بطاقة رسم بياني يُرسم خطها الأخضر، ثم لوحة أوامر تكتب «export chart»، ثم إشعار صغير، ثم يعود إلى زر.
>
> A silent 14-second square loop on off-white where one small black UI element keeps morphing under cursor clicks: a 'Continue' button becomes a spinner, a mini music player, a progress bar, a green toggle, a tab bar, a chart card drawing a green line, a command palette exporting the chart, then a toast and back to a pill.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/demonugc-4c5753
- التصنيفات / Categories: product-ui
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 14 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: React, CSS, Remotion

## الفكرة
الفكرة أن الواجهة كائن واحد حي: لا يوجد قطع بين المكونات، بل جسم واحد يغير حجمه وشكله ومحتواه بسلاسة، وكل نقرة تلد الحالة التالية. المساحة الفارغة الواسعة حول العنصر الصغير تجعل العين تتبع التحول فقط. اللون محصور في الأسود والأبيض مع أخضر واحد للحالات الناجحة والبيانات.

## Concept
The idea is that the interface is one living object: there are no cuts between components, just one body smoothly changing size, shape and content, with every click giving birth to the next state. The wide empty space around the small element makes the eye follow only the morph. Colour is limited to black and white with a single green for success states and data.

## المشاهد المقترحة
- 0-2.2 ث: كبسولة سوداء صغيرة «Continue»؛ المؤشر ينقرها فتصغر إلى مؤشر تحميل دائري يدور، ثم تتضبب وهي تبدأ في التمدد.
- 2.2-5 ث: يتسع المؤشر إلى بطاقة مشغل موسيقى داكنة (اسم المقطع، أيقونة تشغيل، خط تقدم رفيع بتعبئة خضراء ونقطة سحب تُجر).
- 5-6.8 ث: تنضغط البطاقة إلى شريط تقدم أخضر، ثم إلى مفتاح داكن يقلبه المؤشر إلى الأخضر.
- 6.8-8 ث: يكبر المفتاح إلى شريط ألسنة مقسم؛ تُنقر الألسنة واحداً تلو الآخر وكبسولة التحديد السوداء تنزلق بينها.
- 8-9.6 ث: يتمدد شريط الألسنة إلى بطاقة رسم بياني بيضاء؛ خط أخضر يُرسم من اليسار إلى اليمين وتلميح صغير يتبع المؤشر.
- 9.6-12 ث: تصغر البطاقة إلى لوحة أوامر: يُكتب استعلام، حلقة تحميل، ثم قائمة خيارات تصدير ويُميَّز الصف الأول ويُختار.
- 12-14 ث: إشعار أبيض صغير بنقطة خضراء ينزل قرب الأسفل، ثم يتحول إلى كبسولة سوداء أسفل اليمين جاهزة لتكرار الحلقة.

## Proposed scenes
- 0-2.2s: A small black 'Continue' pill; the cursor clicks it and it shrinks into a circular spinner that turns, then blurs as it starts to stretch.
- 2.2-5s: The spinner widens into a dark music player card (track title, play icon, thin progress line with a green fill and a scrub dot being dragged).
- 5-6.8s: The card compresses into a green progress bar, then into a dark toggle that the cursor flips green.
- 6.8-8s: The toggle grows into a segmented tab bar; tabs are clicked one after another, the black selection pill sliding between them.
- 8-9.6s: The tab bar expands into a white chart card; a green line chart draws left to right and a small tooltip follows the cursor.
- 9.6-12s: The card shrinks into a command palette: a query types in, a loader ring, then export options list and the first row gets highlighted and chosen.
- 12-14s: A small white toast with a green dot drops near the bottom, then morphs into a black pill at the lower right, ready to loop.

## قواعد الحركة
- عنصر واحد متصل: كل تغيير حالة هو تحوّل شكل (العرض والارتفاع والزاوية والتعبئة) خلال 300-450 مللي ثانية بزنبرك ناعم، ولا قطع أو تلاشٍ بين مكونات منفصلة أبداً.
- المحتوى داخل العنصر يتلاشى متبادلاً مع ضبابية خفيفة (نحو 150 مللي ثانية) بينما يتحول الإطار.
- لوحة بيضاء مكسورة #f3f2ee بمساحة فارغة كبيرة؛ وأحجام العناصر صغيرة (نحو 10-25% من عرض الإطار).
- الألوان: واجهة سوداء #141414، بطاقات بيضاء #ffffff بظل ناعم، أخضر واحد #2e9e5b للتقدم والمفاتيح وخطوط الرسم ونقاط النجاح، ورمادي #9a9893 للنص الثانوي.
- مؤشر سهم صغير يطلق كل تغيير؛ والنقرات تعطي العنصر انكماش ضغط سريع (نحو 0.96).
- الخط: خط واجهة محايد صغير (متوسط للوسوم)؛ بلا عناوين إطلاقاً. ولا يوجد مسار صوتي.

## Motion rules
- One continuous element: every state change is a shape morph (width, height, radius, fill) over 300-450 ms with a soft spring, never a cut or crossfade between separate components.
- Content inside the element crossfades with a slight blur (~150 ms) while the container morphs.
- Canvas off-white #f3f2ee with lots of empty space; element sizes stay small (roughly 10-25% of frame width).
- Colours: black UI #141414, white cards #ffffff with soft shadow, a single green #2e9e5b for progress, toggles, chart lines and success dots, grey #9a9893 secondary text.
- A small arrow cursor triggers each change; clicks give the element a quick press scale (~0.96).
- Type: small neutral UI sans (medium for labels); no headlines at all. No audio track.

## Facts stated by the source (rewritten in our words)
- The piece is a loop of morphing UI states, per its title.
- The listing states it was built with HTML, CSS and Canvas.
- No duration is stated.

## Assumptions
Observed from 24 frames sampled every ~0.58 s over 14 s: the sequence of states from button to spinner, player, progress bar, toggle, tabs, chart, command palette and toast. The file has no audio stream. Hex values estimated; whether the last state morphs exactly back into the first button is inferred.

## Keywords
UI morph, component states, micro interactions, spinner, toggle, tab bar, command palette, toast, seamless loop, تحولات الواجهة, تفاعلات دقيقة, حالات المكونات, مفتاح تبديل, لوحة أوامر, حلقة متكررة
