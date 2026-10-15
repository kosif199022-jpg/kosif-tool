# إطلاق GenVizu: من الوصف إلى التصوّر — GenVizu product launch

> فيديو إطلاق 20 ثانية لمنتج GenVizu يصلح كخلفية Hero ومادة تسويقية: وصف نصي يتحول إلى رسوم بيانية داخل واجهة المنتج ثم يدور بحلقة نظيفة.
>
> A 20-second launch film for GenVizu usable as a website hero and GTM asset: a typed prompt becomes charts inside the product UI, then loops cleanly.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/listudio-820c7b
- التصنيفات / Categories: product-ui
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 20 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع فيديو إصدار لمنتج اسمه GenVizu، وسيُستخدم على رأس الصفحة وفي مواد الذهاب إلى السوق، لذا الهدف أن يعمل بلا صوت، ويبدأ وينتهي بالإطار نفسه كي يدور في حلقة. الفرضية الإبداعية أن المنتج يولّد تصورات بيانية من وصف نصي، فتُبنى اللغة الحركية على تحوّل: نص يُكتب فيذوب إلى جسيمات تعيد تشكيل نفسها كرسم أعمدة ثم خطي ثم مبعثر، وتظهر واجهة المنتج حول الرسم تدريجيًا. ما يميزها أن الواجهة تُعرض كما شُحنت فعلًا بألوانها وخطها، والحركة تبقى هادئة بما يناسب خلفية موقع.

## Concept
The subject is a release film for a product called GenVizu, meant for a website hero and go-to-market materials, so the goal is to work silently and to start and end on the same frame for a clean loop. The creative premise is that the product generates visualisations from a text description, so the motion language is built on transformation: typed text dissolves into particles that reform as a bar chart, then a line, then a scatter, while the product UI fades in around the chart. Its distinctive trait is fidelity, the UI appears exactly as shipped with its own colours and font, and motion stays calm enough to sit behind a headline.

## المشاهد المقترحة
- 0-2 ث: لوحة فارغة بمؤشر إدخال يومض؛ وصف قصير يكتب نفسه بسرعة 35 ms لكل حرف.
- 2-6 ث: نص الوصف يذوب إلى جسيمات تعيد التشكل كرسم أعمدة، ثم تتحول إلى رسم خطي، ثم إلى مخطط مبعثر؛ كل تحول 700 ms.
- 6-10 ث: إطار واجهة المنتج يظهر حول الرسم: شريط جانبي وشريط أدوات ولوحة بيانات؛ عناصر الواجهة تنزلق من حوافها بتفاوت 60 ms.
- 10-14 ث: مؤشر يعدّل معامِلًا واحدًا؛ الرسم يتحدث فورًا، وتُفتح لوحة مشاركة مع تحريك للتصدير.
- 14-18 ث: ثلاث بطاقات رسوم تتفرّد كمروحة لإظهار التنوع؛ شعار GenVizu يرتفع والبطاقات تنطوي خلفه.
- 18-20 ث: الشعار النصي والدعوة يثبتان 1.5 ثانية؛ الإطار الأخير يطابق خلفية الإطار الأول ليدور بحلقة نظيفة كخلفية Hero.

## Proposed scenes
- 0-2s: An empty canvas with a blinking input cursor; a short prompt types itself at 35 ms per character.
- 2-6s: The prompt text dissolves into particles that re-form as a bar chart, then morph into a line chart, then a scatter plot, each morph taking 700 ms.
- 6-10s: The product UI frame fades in around the chart: sidebar, toolbar, data panel; UI elements slide in from their own edges with a 60 ms stagger.
- 10-14s: A cursor edits one parameter; the chart updates live, and a share panel opens with an export animation.
- 14-18s: Three chart cards fan out to show variety; the GenVizu wordmark rises and the cards tuck behind it.
- 18-20s: Tagline and CTA hold for 1.5 s; the final frame matches the first frame's background so it loops cleanly as a hero.

## قواعد الحركة
- مبني كحلقة متصلة 20 ثانية: الإطار الأول والأخير متطابقان بكسلًا بكسل، والثبات الأخير 1.5 ثانية لا يحمل حركة سوى تنفس عتامة 2% على زر الدعوة.
- الدخول بـ cubic-bezier(0.25, 1, 0.5, 1) خلال 600 ms؛ لوحات الواجهة بتفاوت 60 ms من الحافة التي تنتمي إليها.
- تحولات الرسوم تُدخل مسارات SVG بعدد نقاط متساوٍ خلال 700 ms؛ تبقى نقاط البيانات موسومة أثناء التحول كي يظل الرسم مقروءًا.
- الكتابة بسرعة 35 ms لكل حرف مع وميض مؤشر كل 530 ms؛ الوصف لا يتجاوز ثماني كلمات.
- الكاميرا: dolly بطيء من 1.0 إلى 1.04 عبر المقاطع 2-5، ويُعاد إلى 1.0 أثناء إظلام قصير 200 ms قبل المقطع الأخير.
- اللوحة والطباعة من المنتج نفسه: ألوان الواجهة كما شُحنت، وخط الواجهة لنصوصها، وخط عرض واحد للشعار فقط؛ لا ألوان مختلقة.
- يجب أن يعمل صامتًا: كل مقطع يحمل تسمية مرئية أو حالة واجهة تفسر نفسها دون تعليق صوتي.
- ممنوع: بيانات مزيفة دون وسم، ومقاطع تعتمد على الصوت، والوميض، وأي عنصر واجهة غير موجود في المنتج الحقيقي.

## Motion rules
- Built as a 20 s seamless loop: the first and last frames are pixel-identical, and the final 1.5 s hold uses no motion except a 2% opacity breathe on the CTA.
- Entrances use cubic-bezier(0.25, 1, 0.5, 1) over 600 ms; UI panels stagger by 60 ms from the edge they belong to.
- Chart morphs interpolate SVG paths with equal point counts over 700 ms; data points stay labelled during the morph so the chart remains readable.
- Typing runs at 35 ms per character with a 530 ms cursor blink; the prompt never exceeds eight words.
- Camera: a slow dolly from 1.0 to 1.04 across beats 2-5, reset to 1.0 during a 200 ms dark dip before the final beat.
- Palette and typography are the product's own: UI colours as shipped, the UI font for interface text, one display face only for the wordmark; no invented hues.
- Must work muted: every beat carries a visible label or UI state that explains itself without narration.
- Banned: unlabeled fake data, beats that rely on sound, flashing, and any UI element that does not exist in the real product.

## Facts stated by the source (rewritten in our words)
- The creator asked for the project at a supplied link, GenVizu, to be studied first.
- The output is a product-release video.
- It will serve as a website hero and in go-to-market materials.
- Tagged product UI; no duration, colours or stack are stated.

## Assumptions
GenVizu is assumed to be a text-to-visualisation tool based on its name; the 20-second loop, the prompt-to-chart premise and the UI beats are proposals pending a look at the real product.

## Keywords
product launch, hero video, seamless loop, prompt to chart, path morph, product ui, gtm asset, data visualisation, إطلاق منتج, فيديو hero, حلقة متصلة, تحويل رسوم, واجهة منتج, تصوّر بيانات
