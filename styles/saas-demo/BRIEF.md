# استعراض SaaS — جولة سريعة داخل واجهة تطبيق ويب — استعراض SaaS

> ريل عمودي 9:16 يعرض منتجاً برمجياً: نافذة تطبيق ويب نظيفة بزوايا مستديرة وظل ناعم تطفو على خلفية متدرجة فاتحة، ومؤشر فأرة يتحرك وينقر بحلقة ضغط، والكاميرا تقترب من كل ميزة بينما تظهر عناوين عربية قصيرة فوقها، وتمتلئ البيانات والرسوم داخل الواجهة كأنها حية، وتنتهي بالشعار وزر الاشتراك.
>
> A 9:16 reel showcasing a software product: a clean, rounded web-app window with a soft shadow floating on a light gradient, a cursor that glides and clicks with a press ring, camera zooms into each feature while short Arabic headlines appear above, data and charts fill inside the UI as if live, ending on the logo and a sign-up button.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: product-ui, ads
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 30 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
أفضل إعلان لمنتج برمجي هو أن ترى المشكلة تُحل داخل المنتج نفسه في ثوانٍ. الفيديو جولة موجّهة: سؤال أو ألم، ثم ثلاث ميزات تُعرض عبر نقرات حقيقية داخل الواجهة، ثم النتيجة. الكاميرا هي المذيع؛ تقترب حيث يجب أن تنظر وتبتعد لتُظهر الصورة الكاملة.

## Concept
The best ad for software is watching the problem get solved inside the product in seconds. The video is a guided tour: a pain or question, then three features shown through real clicks in the UI, then the outcome. The camera is the presenter; it zooms where you should look and pulls back to show the whole picture.

## المشاهد المقترحة
- 0-3 ث: عنوان جذب عريض بالعربية على التدرج: مشكلة المستخدم في خمس كلمات؛ وتصعد نافذة التطبيق من الأسفل بارتداد نابض.
- 3-9 ث: الميزة الأولى: المؤشر يتحرك في مسار منحنٍ إلى زر وينقر (نبضة حلقة)؛ والكاميرا تقترب 1.6 مرة من لوحة بينما يمتلئ نموذج وحده.
- 9-15 ث: الميزة الثانية: ابتعاد ثم انزلاق إلى الشريط الجانبي؛ جدول يمتلئ صفاً صفاً وشارة حالة تتحول إلى الأخضر.
- 15-21 ث: الميزة الثالثة: رسم بياني يكبر داخل بطاقة، وبطاقة معلومات تخرج من النافذة إلى الأمام بعمق ثلاثي الأبعاد.
- 21-26 ث: النتيجة: رقم كبير (مثل «وفّر 6 ساعات أسبوعياً») يعدّ فوق خلفية التطبيق المموهة.
- 26-30 ث: الشعار واسم المنتج وزر «جرّب مجاناً» مع نقرة أخيرة من المؤشر.

## Proposed scenes
- 0-3s: Hook headline in bold Arabic on the gradient: the user's pain in five words; the app window rises from below with a spring.
- 3-9s: Feature 1: the cursor moves along a curved path to a button and clicks (ring pulse); the camera zooms 1.6x into a panel as a form fills itself.
- 9-15s: Feature 2: pull back, slide to the sidebar; a table populates row by row and a status chip flips to green.
- 15-21s: Feature 3: a chart grows inside a card while a floating tooltip card pops out of the window in 3D depth.
- 21-26s: Outcome: a big metric (e.g. 'وفّر 6 ساعات أسبوعياً') counts up over a blurred app background.
- 26-30s: Logo, product name and a 'جرّب مجاناً' button with a final cursor click.

## قواعد الحركة
- تدرج الخلفية من #eef2ff إلى #f8fafc؛ نافذة التطبيق بيضاء #ffffff بزوايا 20 بكسل وظل ناعم؛ ولون العلامة #4f46e5 مع لون النجاح #10b981.
- الواجهة تُبنى كمكونات حقيقية (حادة عند أي تكبير) وليست لقطة شاشة مموهة؛ وبتخطيط من اليمين لليسار للواجهات العربية.
- المؤشر: سهم بأسلوب ماك يتحرك على مسارات منحنية خلال 0.5-0.8 ث، والنقرة = تصغير إلى 0.9 ثم حلقة 24 بكسل تتلاشى في 0.3 ث.
- الكاميرا تقترب 1.3-2 مرة من المنطقة النشطة (0.7 ث)؛ ميزة واحدة في التركيز كل مرة وبقية الواجهة تخفت إلى 60٪.
- العناوين: خط عربي بسيط (IBM Plex Sans Arabic 700 أو كايرو 800)، ست كلمات على الأكثر، فوق النافذة، تدخل بارتفاع 16 بكسل وظهور 0.3 ث.
- البيانات داخل الواجهة تتحرك كأنها حية: عدادات، وصفوف تُضاف بتأخير 50 مللي ث، وأعمدة رسوم تكبر.
- الفرق عن التفاعلات الدقيقة (تفاعل مكون واحد) والواجهة الزجاجية (جمالية الزجاج المصنفر): جولة كاملة في المنتج بمؤشر وكاميرا.

## Motion rules
- Background gradient #eef2ff to #f8fafc; app window white #ffffff, radius 20 px, shadow 0 30px 60px rgba(15,23,42,.15); brand accent #4f46e5 with success #10b981.
- UI is rebuilt as real HTML/React components (crisp at any zoom), never a blurry screenshot; right-to-left layout for Arabic UIs.
- Cursor: macOS-style arrow, moves on bezier paths in 0.5-0.8 s with easeInOutCubic, click = scale 0.9 then a 24 px ring that fades in 0.3 s.
- Camera zooms 1.3-2x into the active area (0.7 s, easeInOutQuart); only one feature in focus at a time, the rest of the UI dims to 60%.
- Headlines: Arabic sans (IBM Plex Sans Arabic 700 / Cairo 800), max 6 words, placed above the window, enter with an 16 px rise and 0.3 s fade.
- Data inside the UI animates as if live: counters, row inserts with 50 ms stagger, chart bars growing.
- Different from ui-micro (one component's micro-interaction) and glass-ui (frosted glass aesthetic): a full product walkthrough with cursor and camera.

## Facts stated by the source (rewritten in our words)
- Catalogued as a KOSIF original style named SaaS showcase, in the Product UI category.

## Assumptions
Authored KOSIF definition, not an observed reference: there is no reference video for this base style (its page is the KOSIF repo root), so palette hex values, type choices, timings and scene beats are original KOSIF design decisions, not measurements. Assumed a 9:16 reel of about 30 s for one product with three features; the UI is recreated from the user's screenshots or design files.

## Keywords
saas, product demo, app walkthrough, ui animation, cursor, feature tour, startup ad, استعراض منتج, تطبيق ويب, شرح تطبيق, واجهة مستخدم, إعلان برمجي, SaaS
