# عرض Winkz: لماذا نبيع منتجاتكم على أمازون — Amazon wholesale pitch video

> فيديو عرض 15 ثانية من شركة Winkz Enterprises لعلامة تجارية: مسار توريد متحرك ورسوم مبيعات وأدلة ثقة تقنع العلامة بمنحها حق البيع.
>
> A 15-second B2B pitch from Winkz Enterprises to a brand: an animated supply route, sales charts and trust proofs that argue for the right to sell its products.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/ceowinkz-7c776b
- التصنيفات / Categories: charts
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع عرض تقديمي موجَّه من شركة بيع بالجملة على أمازون إلى علامة تجارية، والهدف إقناع العلامة في 15 ثانية بأن الشركة شريك موثوق يبيع منتجاتها بانضباط. اللغة الحركية تعتمد على الأدلة الرقمية لا الشعارات: خط توريد يُرسم من العلامة إلى المستودع إلى أمازون إلى العميل، ورسم خطي للوحدات المباعة مع خط ثابت لأرضية السعر، وثلاث بلاطات إثبات تمتلئ بقيمها. ما يميزها أن كل رقم ينمو من الصفر مع محور واضح، وأن لون التمييز البرتقالي يُستخدم بشح كي يبقى الطابع رسميًا.

## Concept
The subject is a pitch from an Amazon wholesale company to a brand, and the goal is to convince that brand within 15 seconds that the company is a disciplined, trustworthy seller of its products. The motion language relies on numeric evidence rather than slogans: a supply route drawn from brand to warehouse to Amazon to customer, a line chart of units sold with a flat price-floor line, and three proof tiles filling to their values. Its distinctive trait is that every number grows from zero with a visible axis, and the orange accent is rationed so the tone stays corporate.

## المشاهد المقترحة
- 0-2 ث: شعار WINKZ ENTERPRISES يُثبَّت بتوقف 3 إطارات على كل كلمة؛ عنوان فرعي 'شريك بيع بالجملة على أمازون' ينزلق تحته.
- 2-5 ث: أيقونة صندوق منتج تسير على خط مسار من 'العلامة' إلى 'مستودع Winkz' إلى 'أمازون' إلى 'العميل'، وكل عقدة تضيء عند وصوله.
- 5-8 ث: رسم خطي للوحدات المباعة شهريًا يصعد عبر الإطار مع عدّاد؛ خط ثانٍ (أرضية سعر العلامة) يبقى مستويًا للدلالة على انضباط التسعير.
- 8-11 ث: ثلاث بلاطات إثبات تنقلب: مقياس تقييم خمس نجوم يمتلئ إلى قيمته، وحلقة نسبة للشحن في الموعد، وعدد العلامات التي تمثلها الشركة.
- 11-13 ث: إطار مقسوم: مكان شعار العلامة على اليسار وWinkz على اليمين، وخط مصافحة يُرسم بينهما.
- 13-15 ث: دعوة 'لنتحدث' مع بيانات التواصل؛ خط المسار من المقطع الثاني يدور مرة واحدة في الخلفية.

## Proposed scenes
- 0-2s: The WINKZ ENTERPRISES wordmark snaps in with a 3-frame hold on each word; the subtitle 'Amazon wholesale partner' slides under it.
- 2-5s: A product box icon travels along a route line from 'brand' to 'Winkz warehouse' to 'Amazon' to 'customer', each node lighting up as it arrives.
- 5-8s: A line chart of monthly units sold climbs across the frame with a counter; a second line (the brand's price floor) stays flat to signal price discipline.
- 8-11s: Three proof tiles flip in: a 5-star rating meter filling to its value, a percentage ring for on-time shipping, and a count of brands represented.
- 11-13s: A split frame: the brand's logo placeholder on the left, Winkz on the right, and a handshake line draws between them.
- 13-15s: CTA 'Let's talk' with contact details; the route line from beat 2 loops once in the background.

## قواعد الحركة
- الدخول بـ cubic-bezier(0.2, 0.9, 0.3, 1) خلال 500 ms؛ الشعار يستعمل توقفات حادة 3 إطارات لكل كلمة بدل التسهيل كي يبدو حاسمًا.
- الرسوم البيانية تبدأ دائمًا من الصفر وتُظهر تسميات المحاور وتتحرك خلال 800 ms؛ العدّادات بأرقام جدولية وتستقر بعد 100 ms من رسمها.
- مسار التوريد يُرسم خلال 1200 ms مع ظهور العقد خلال 150 ms؛ أيقونة الصندوق تتحرك بسرعة ثابتة وتتوقف 200 ms عند كل عقدة.
- بلاطات الإثبات تنقلب بـ rotateX من 90° إلى 0° خلال 400 ms بتفاوت 120 ms؛ مقياس النجوم يمتلئ من اليسار إلى اليمين خلال 600 ms.
- الكاميرا ثابتة ثنائية الأبعاد؛ التأكيد يأتي من التكبير (حد أقصى 1.05) وخط سفلي بلون التمييز بسمك بكسل واحد، لا من الزوم.
- اللوحة: أساس كحلي، ونص أبيض، ولون تمييز برتقالي واحد لا يتجاوز 15% من مساحة الإطار؛ الأحمر والأخضر داخل الرسوم البيانية فقط.
- الطباعة: عناوين grotesk ثقيلة بحجم 120 px، وأرقام جدولية 64 px، وتعليقات 28 px؛ لا أكثر من سبع كلمات على الشاشة في آن واحد.
- ممنوع: شعار أمازون أو مظهرها التجاري (الكلمة فقط)، والادعاءات المعروضة كحقائق دون وسم مؤقت، والوميض السريع أو الومضات.

## Motion rules
- Entrances use cubic-bezier(0.2, 0.9, 0.3, 1) over 500 ms; the wordmark uses hard 3-frame holds per word instead of easing so it feels decisive.
- Charts always start from zero, show axis labels, and animate over 800 ms; counters use tabular figures and settle 100 ms after their chart.
- The supply route draws over 1200 ms with node pops of 150 ms; the box icon moves at constant speed and pauses 200 ms at each node.
- Proof tiles flip in with rotateX from 90° to 0° over 400 ms and a 120 ms stagger; the star meter fills left to right over 600 ms.
- Camera is locked 2D; emphasis comes from scale (max 1.05) and a one-pixel accent underline, never from zoom.
- Palette: navy base, white type, one orange accent capped at 15% of frame area; red and green appear only inside charts.
- Typography: bold grotesk headlines at 120 px, tabular numerals at 64 px, captions at 28 px; no more than seven words on screen at once.
- Banned: Amazon's logo or trade dress (the word only), claims shown as facts without a placeholder label, and rapid flicker or strobing.

## Facts stated by the source (rewritten in our words)
- A dynamic 15-second motion piece is requested.
- The sender is Winkz Enterprises, an Amazon wholesale business.
- The audience is a brand, and the message is why it should authorise the company to sell its products.
- Catalogued under charts; no colours, scenes or stack are described.

## Assumptions
All metrics, the supply-route structure and the navy-and-orange palette are proposals; the company's real figures, logo and brand colours were not provided.

## Keywords
b2b pitch, wholesale, supply route, line chart, proof tiles, star rating meter, handshake, corporate motion, عرض تقديمي, بيع بالجملة, مسار توريد, رسم خطي, أدلة ثقة, شراكة
