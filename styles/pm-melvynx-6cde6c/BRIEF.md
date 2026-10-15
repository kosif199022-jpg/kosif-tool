# ريل ترويجي لأداة بريد إلكتروني — Email tool promo reel

> ريل مدته 15 ثانية يجعل واجهة أداة البريد هي البطل: نافذة إنشاء تتفتح، رسالة تنطلق، صندوق وارد يرتّب نفسه، ومنحنى معدل الفتح يصعد.
>
> A 15-second promo where the email tool's own interface is the hero: a composer unfolds, a message launches, the inbox sorts itself and an open-rate curve climbs.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/melvynx-6cde6c
- التصنيفات / Categories: product-ui, charts
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
الموضوع أداة بريد إلكتروني (العنوان في المصدر عام وعنوان الموقع مُستبدَل بحافظ مكان، لذلك نفترض أداة لإرسال البريد ومتابعته). الهدف أن يفهم المشاهد في 15 ثانية ماذا تفعل الأداة ولماذا تبدو سريعة وموثوقة. اللغة الحركية تعتمد على تحريك مكونات الواجهة الحقيقية نفسها بدل الرسوم التجريدية: الأزرار تُضغط فعلاً، البطاقات تعيد ترتيبها بحركة FLIP، والرسوم البيانية تخرج من لوحة التحليلات لا من فراغ.

## Concept
The subject is an email tool (the source title is generic and the site URL is a placeholder, so we assume a sending-and-tracking product). The goal is that in 15 seconds a viewer understands what the tool does and feels it is fast and dependable. The motion language animates the real interface components themselves instead of abstract graphics: buttons actually press, cards reorder with FLIP moves, and charts grow out of the analytics panel rather than from nowhere.

## المشاهد المقترحة
- 0-2 ث: مؤشر كتابة يومض على سطح فارغ؛ تتفتح نافذة إنشاء الرسالة من هذا السطر الواحد، الترويسة أولاً ثم الجسم.
- 2-6 ث: يُكتب سطر الموضوع تلقائياً، يُضغط زر الإرسال، وينطلق ظرف خارج الإطار ثم يتحول إلى شارة إشعار على أيقونة صندوق وارد صغيرة.
- 6-10 ث: يتسع صندوق الوارد لعرض الشاشة؛ اثنتا عشرة بطاقة رسالة تتدفق بتدرج 45 ms، يتبدل تبويب تصفية فتعيد البطاقات ترتيبها في مكانها.
- 10-13 ث: ينزلق درج تحليلات من الأسفل: خط معدل الفتح يرسم نفسه من اليسار إلى اليمين، ثلاثة عدّادات تصل إلى قيمها، وsparkline ينبض مرة واحدة.
- 13-15 ث: تنطوي لوحات الواجهة إلى بلاطة مدورة واحدة تصبح الشعار؛ يستقر عنوان الموقع ودعوة إجراء قصيرة تحتها.

## Proposed scenes
- 0-2s: A caret blinks on an empty surface; a composer window unfolds from that single line, header first, body second.
- 2-6s: A subject line types itself, the send button depresses, and an envelope streaks off-screen, morphing into a notification badge on a tiny inbox icon.
- 6-10s: The inbox grows to full width; twelve message cards cascade in with a 45 ms stagger, a filter tab switches and the cards reorder in place.
- 10-13s: An analytics drawer slides up from the bottom: an open-rate line draws left to right, three counters tick to their values, a sparkline pulses once.
- 13-15s: The interface panels collapse into a single rounded tile that becomes the logo; the URL and a short call to action settle beneath it.

## قواعد الحركة
- لوحات الواجهة تدخل بنابض (stiffness 170، damping 22، mass 1) وتستقر خلال 700 ms؛ لا يرتد أي عنصر أكثر من مرة.
- عناصر القوائم تتدرج بفارق 40-60 ms؛ إعادة الترتيب عبر تحويلات FLIP بمدة 450 ms مع cubic-bezier(0.2, 0.8, 0.2, 1) بحيث تنزلق البطاقات ولا تختفي ثم تظهر.
- المؤشر عنصر فعلي يتحرك على مسارات bezier بمدة 250-400 ms؛ النقرة انخفاض مقياس إلى 0.94 لمدة 90 ms على الهدف.
- خطوط الرسوم ترسم عبر stroke-dashoffset خلال 900 ms بتباطؤ خروج؛ العدّادات تعمل بـeaseOutQuart خلال 800 ms وتستخدم أرقاماً جدولية.
- الكاميرا parallax ثنائية ونصف فقط: تحريك جانبي ودفعة واحدة من 1.0 إلى 1.08 في لقطة التحليلات؛ الواجهة المسطحة لا تدور أكثر من 8 درجات في الفضاء الثلاثي.
- الطباعة بخط واجهة واحد بأحجام منتج حقيقية (14، 16، 24، 40 px مع التحجيم)؛ النص يجب أن يكون نص منتج معقولاً، لا lorem ipsum.
- اللون: أسطح رمادية محايدة مع لون علامة واحد على الأزرار الرئيسية والظرف المرسل وخط الرسم البياني؛ الأخضر والأحمر الحالتيان داخل البيانات فقط.
- ممنوع: انتقالات معتمدة على blur، مؤشرات تحميل وهمية فوق 300 ms، نماذج واجهة بنص غير مقروء، تأثيرات glitch أو اهتزاز.

## Motion rules
- UI panels enter with a spring (stiffness 170, damping 22, mass 1) and settle within 700 ms; nothing bounces more than once.
- List items stagger 40-60 ms apart; reorders use FLIP transforms over 450 ms with cubic-bezier(0.2, 0.8, 0.2, 1) so cards slide, never fade and reappear.
- The cursor is a real pointer element moving on bezier paths of 250-400 ms; a click is a 90 ms scale dip to 0.94 on the target.
- Chart strokes draw via stroke-dashoffset over 900 ms ease-out; counters run easeOutQuart over 800 ms and use tabular figures.
- Camera is 2.5D parallax only: pans and a single 1.0 to 1.08 push-in on the analytics beat; flat UI never rotates beyond 8 degrees in 3D.
- Typography uses one UI sans at real product sizes (14, 16, 24, 40 px scaled); copy must be plausible product text, never lorem ipsum.
- Colour: neutral grey surfaces with one brand accent on primary buttons, the sent envelope and the chart line; status greens and reds only inside the data.
- Banned: blur-based transitions, fake loading spinners over 300 ms, mockups with unreadable text, glitch or shake effects.

## Facts stated by the source (rewritten in our words)
- The creator asked for a 15-second dynamic motion graphics video promoting a website whose URL was left as a placeholder.
- The site lists it under product UI and charts, and titles it as an email tool promo.

## Assumptions
Stated: 15 seconds, promo for a website, product-UI and charts tags, email-tool title. Assumed: the sending-and-analytics feature set, the composer-to-inbox-to-chart structure, all timings, easings and the neutral-plus-one-accent palette.

## Keywords
product ui, saas promo, inbox animation, واجهة منتج, بريد إلكتروني, flip animation, spring, open rate, analytics, ريل ترويجي, cursor, مؤشر, رسم خطي, composer
