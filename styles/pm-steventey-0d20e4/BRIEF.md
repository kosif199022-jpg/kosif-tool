# فيلم إطلاق منصة اختصار الروابط وتحليلاتها — Dub promo video

> فيلم إطلاق SaaS مدته 15 ثانية يحول رابطاً طويلاً إلى رابط قصير ثم يفتح تحليلات النقرات كواجهة حية.
>
> A 15-second SaaS launch film that squeezes a long URL into a short link, then unfolds its click analytics as a living product UI.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/steventey-0d20e4
- التصنيفات / Categories: product-ui, charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع منصة لإدارة الروابط القصيرة وتتبعها، والهدف إيصال وعدها خلال 15 ثانية: رابط أقصر، وبيانات أوضح، وتحكم كامل. اللغة الحركية مبنية على فكرة الضغط والتمدد: الرابط الطويل ينضغط حرفياً إلى رابط قصير، ثم يتمدد الرابط القصير إلى لوحة تحليلات تنمو من داخله. الواجهة تتحرك بزنبركات مضبوطة، والرسوم البيانية تُرسم كاستجابة لنقرات مرئية، لا كزينة.

## Concept
The subject is a link-management platform with analytics, and the goal is to deliver its promise in 15 seconds: shorter links, clearer data, full control. The motion language is compression and expansion: a long URL physically squeezes into a short one, then the short link expands into an analytics dashboard that grows from inside it. The UI moves on tuned springs and the charts are drawn as responses to visible clicks, never as decoration.

## المشاهد المقترحة
- 0-3 ث: يُكتب رابط طويل قبيح عبر الإطار بخط أحادي المسافة؛ تنهار الحروف نحو المركز كالأكورديون وينقر رابط قصير بالعلامة التجارية في مكانه بتجاوز زنبركي 1.1 وصوت نقرة ناعم.
- 3-6 ث: يحوم المؤشر فوق الرابط القصير؛ تنقلب بطاقة تحته تظهر رمز QR يُرسم خطاً خطاً وحقل نطاق مخصص يمتلئ.
- 6-10 ث: تمتد البطاقة إلى لوحة تحكم: يُرسم خط بياني للنقرات من اليسار إلى اليمين خلال 700 مللي ثانية، تضيء خريطة العالم نقاطها مدينة مدينة بخطوات 60 مللي ثانية، وتُغلق دائرة توزيع الأجهزة بمسح.
- 10-13 ث: تدفع ثلاث رقائق ميزات (النطاقات المخصصة، QR، التحليلات) من اليمين بزنبركات متدرجة؛ يتدحرج عداد إلى رقم إجمالي نقرات كبير بينما تنبض آخر نقطة في الخط مرة واحدة.
- 13-15 ث: تنكمش لوحة التحكم مرة أخرى إلى الرابط القصير الذي يصبح ترويسة الشعار مع شعار الإطلاق؛ يثبت الإطار الأخير 800 مللي ثانية على خلفية نظيفة.

## Proposed scenes
- 0-3s: A long, ugly URL types itself across the frame in mono type; the characters collapse toward the center like an accordion and a short branded link snaps into place with a 1.1 spring overshoot and a soft click.
- 3-6s: A cursor hovers the short link; a card flips up beneath it showing a QR code drawing stroke by stroke and a custom-domain field filling in.
- 6-10s: The card stretches into a dashboard: a clicks line chart draws left to right over 700 ms, a world map lights up dots city by city in 60 ms steps, and a device breakdown donut sweeps closed.
- 10-13s: Three feature chips (custom domains, QR, analytics) push in from the right on staggered springs; a counter rolls to a large total-clicks number while the chart's last point pulses once.
- 13-15s: The dashboard contracts back into the short link, which becomes the logo lockup with a 'launch' tagline; final frame holds 800 ms on a clean canvas.

## قواعد الحركة
- زنبركات الواجهة: صلابة 200 وتخميد 24 للبطاقات والرقائق؛ انضغاط الرابط يستخدم cubic-bezier(0.7, 0, 0.2, 1) خلال 500 مللي ثانية ليتسارع الضغط ثم يهبط بقوة.
- الرسوم البيانية تُرسم كدوال في الزمن: الخط عبر stroke-dashoffset (700 مللي ثانية)، الدائرة عبر مسح قوسي (600 مللي ثانية)، نقاط الخريطة عبر تكبير متدرج من الصفر (بفاصل 60 مللي ثانية)؛ لا تحريك رسم بياني بالتلاشي أبداً.
- تؤدي الكاميرا دفعة واحدة 6% أثناء كشف لوحة التحكم وسحبة واحدة أثناء الانكماش؛ لا دوران ولا اهتزاز.
- كل انتقال تحول للحاوية: الرابط يصبح البطاقة، البطاقة تصبح اللوحة، اللوحة تصبح الرابط؛ القطع الحاد ممنوع.
- الطباعة: خط أحادي المسافة للروابط والأرقام، وخط sans هندسي لتسميات الواجهة؛ تتدحرج العدادات رقماً رقماً بخطوة 40 مللي ثانية مع تسهيل خروج في النهاية.
- اللون: خلفية شبه سوداء مع واجهة بيضاء ولون علامة تجارية واحد محجوز للرابط القصير وخط الرسم البياني وزر الدعوة.
- ممنوع: مؤشرات تحميل وهمية تتجاوز 300 مللي ثانية، لقطات شاشة ضبابية، صور أشخاص جاهزة، انفجارات جسيمات، وأكثر من لون تمييز واحد.

## Motion rules
- UI springs: stiffness 200, damping 24 for cards and chips; URL compression uses cubic-bezier(0.7, 0, 0.2, 1) over 500 ms so the squeeze accelerates then lands hard.
- Charts draw as functions of time: line via stroke-dashoffset (700 ms), donut via arc sweep (600 ms), map dots via staggered scale-from-zero (60 ms apart); never animate a chart with a fade.
- Camera performs one push-in of 6% during the dashboard reveal and one pull-back during the contraction; no rotation, no shake.
- Every transition is a container morph: the link becomes the card, the card becomes the dashboard, the dashboard becomes the link; hard cuts are banned.
- Typography: mono for URLs and numbers, a geometric sans for UI labels; counters roll digit by digit with 40 ms per step and ease-out at the end.
- Colour: a near-black canvas with white UI and one brand accent reserved for the short link, the chart line and the CTA.
- Banned: fake loading spinners longer than 300 ms, blurry screenshots, stock photos of people, particle bursts, and more than one accent colour.

## Facts stated by the source (rewritten in our words)
- The requested length is 15 seconds.
- The film is positioned as a launch video for a SaaS link-management product.
- Public tags are product UI, charts and kinetic type.

## Assumptions
The product features shown (short links, QR codes, custom domains, click analytics) are inferred from the product category; the dark palette, scene order and spring values are proposed, not stated.

## Keywords
link shortener, saas launch, analytics dashboard, url compression, qr code draw, world map dots, line chart draw-on, spring ui, اختصار الروابط, لوحة تحليلات, إطلاق منتج, واجهة منتج متحركة, عداد رقمي
