# عالم أيزومتريك — مدينة صغيرة بألوان باستيل تشرح رحلة خطوة بخطوة — عالم أيزومتريك

> مدينة أيزومترية صغيرة بألوان باستيل (بيوت وأبراج وردية وبنفسجية وفيروزية ومستودع برتقالي وأشجار مستديرة) على خلفية لافندر فاتحة، تنتقل الكاميرا بين مبانيها لتشرح رحلة طلب أونلاين: هاتف يظهر فوق بيت، خط منقط إلى سحابة، مستودع تخرج منه شاحنة، ثم الوصول للباب، مع شريط مراحل في الأسفل يتقدم وفقاعات عربية صغيرة.
>
> A tiny pastel isometric city (pink, violet and teal towers, an orange warehouse, round trees) on pale lavender, where the camera moves between buildings to explain an online order's journey: a phone pops over a house, a dotted line arcs to a cloud, a truck leaves the warehouse, and it reaches the door, while a bottom progress bar advances and small Arabic speech chips appear.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/isometric
- التصنيفات / Categories: 3d, diagrams
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 28 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG, CSS

## الفكرة
نحوّل عملية مجردة (طلب، دفع، شحن، وصول) إلى مكان يمكن التجول فيه. كل مرحلة مبنى، والكاميرا تزوره، وشريط المراحل يذكّر المشاهد أين هو في القصة. الألوان الباستيل والأشكال المستديرة تجعل الشرح ودوداً، والنهاية تبتعد لترى المدينة والرحلة كاملة.

## Concept
An abstract process (order, payment, shipping, delivery) becomes a place you can tour. Each stage is a building the camera visits, and the stage bar reminds the viewer where they are in the story. Pastel colours and rounded shapes keep it friendly, and the ending pulls out to show the whole city and journey.

## المشاهد المقترحة
- 0-3 ث: لقطة قريبة على ركن من المدينة؛ العنوان بخط عربي عريض أعلى اليمين مع سطر فرعي صغير؛ وشخصية تقف بجوار بيت.
- 3-7 ث: يظهر هاتف بجوار الشخصية يعرض بطاقة منتج؛ ضغطة زر تتحول إلى شارة تأكيد؛ ويضيء شريط المراحل الخطوة الأولى.
- 7-11 ث: قوس منقط يسافر من البيت إلى مجموعة خوادم «سحابة» عائمة؛ تظهر شارة تأكيد الدفع؛ وتضيء الخطوة الثانية.
- 11-17 ث: الكاميرا تنزلق إلى المستودع البرتقالي؛ رافعة تحمل صناديق إلى شاحنة صغيرة؛ تقفز شارة «تم التجهيز»؛ وتضيء الخطوة الثالثة.
- 17-22 ث: الشاحنة تسير في الطريق بين الأبراج وتتوقف عند إشارة مرور؛ وشارات الحالة تتحدث («في الطريق»).
- 22-25 ث: الوصول: الشاحنة تصل إلى البيت، الشخصية تستلم الصندوق، وتنفجر قصاصات احتفال؛ وتضيء الخطوة الأخيرة.
- 25-28 ث: ابتعاد إلى المدينة الأيزومترية كاملة مع المسار كله؛ ويعود العنوان بسطره الفرعي.

## Proposed scenes
- 0-3s: Close on a corner of the city; the title in bold Arabic top-right with a small subtitle; a character stands by a house.
- 3-7s: A phone mockup pops up beside the character showing a product card; a button tap turns into a confirmation chip; the stage bar lights step 1.
- 7-11s: A dotted arc travels from the house to a floating 'cloud' server cluster; a payment-confirmed chip appears; step 2 lights.
- 11-17s: The camera glides to the orange warehouse; a forklift loads boxes into a small truck; a 'packed' chip pops; step 3 lights.
- 17-22s: The truck drives along the road between towers and stops at a traffic light; status chips update ('on the way').
- 22-25s: Arrival: the truck reaches the house, the character receives the box, confetti bursts; final step lights.
- 25-28s: Pull-out to the whole isometric city with the full route; title returns with its subtitle.

## قواعد الحركة
- إسقاط أيزومتري حقيقي (محاور 30 درجة) بلا منظور؛ والكاميرا تنزلق وتقترب فقط في بُعدين عبر المشهد (1-1.5 ث).
- الألوان (مأخوذة من المرجع): خلفية #edeefa، أرض #e7f3e5، طريق #eae6e3، أبراج وردية #f2a7c8 وبنفسجية #8f8ff0 وفيروزية #7fe0c8، مستودع برتقالي #f5a623 بسقف بني #a5521f، أشجار #2fbf71؛ ولكل مجسم ثلاث درجات (الأعلى أفتح، اليسار متوسط، اليمين أغمق).
- العناصر تدخل بالصعود من الأرض مع تجاوز صغير (0.4 ث) أو بالظهور بالتكبير؛ والمركبات تتحرك على محاور الطرق فقط.
- خطوط الربط أقواس منقطة تسافر عليها نقطة؛ وشارات الحالة كبسولات بيضاء بأيقونة ملونة ونص عربي قصير تظهر في 0.25 ث.
- شريط تقدم ثابت في الأسفل بخمس مراحل معنونة؛ والمرحلة النشطة تمتلئ بلون التمييز مع نبضة حلقة.
- الخطوط: عربي عريض مستدير (كايرو 800 للعنوان و600 للشارات) بلون كحلي داكن #1f2148؛ من اليمين لليسار والحروف متصلة.
- الفرق عن اللو بولي والسينمائي ثلاثي الأبعاد: أيزومتري باستيل بتظليل مسطح بلا منظور ولا مؤثرات إضاءة ولا دوران كاميرا؛ وفي 9:16 نؤطر شريحة أضيق من المدينة مع العنوان في الأعلى والشريط في الأسفل.

## Motion rules
- True isometric projection (30-degree axes), no perspective; the camera only pans and zooms in 2D across the scene (1-1.5 s, easeInOutCubic).
- Palette (sampled): background #edeefa, ground #e7f3e5, road #eae6e3, towers pink #f2a7c8, violet #8f8ff0, teal #7fe0c8, warehouse orange #f5a623 with brown roof #a5521f, trees #2fbf71; each solid has three tones (top lightest, left mid, right darkest).
- Objects enter by rising from the ground with a small overshoot (0.4 s) or by popping in at scale; vehicles move along road axes only.
- Connection lines are dotted arcs with a travelling dot; status chips are white pills with a coloured icon and short Arabic text, popping at 0.25 s.
- A fixed bottom progress bar with 5 labelled steps; the active step fills with the accent and a ring pulse.
- Typography: bold rounded Arabic sans (Cairo 800 for the title, 600 for chips), dark navy #1f2148; RTL, joined letters intact.
- Different from lowpoly-3d and cinematic-3d: flat-shaded pastel isometric with no perspective, no lighting effects and no camera rotation; for 9:16, frame a narrower slice of the city and stack title top, bar bottom.

## Facts stated by the source (rewritten in our words)
- The reference in the starter kit is a 1280x720, 30 fps, 28 s silent clip.
- Its subject is the journey of an online order from a tap on the phone to delivery at the door.

## Assumptions
Observed from a 24-frame grid of the starter-kit reference video (28 s, 16:9, no audio track): the pastel isometric city, phone pop-up, dotted arc to a cloud, warehouse and truck, status chips, bottom progress bar, arrival confetti and final pull-out. Assumed: exact beat timings between samples, easing and fonts; hex values are approximate samples.

## Keywords
isometric, isometric city, pastel, process explainer, delivery journey, e-commerce flow, progress bar, أيزومتريك, مدينة أيزومترية, شرح عملية, رحلة الطلب, باستيل, توصيل, تجارة إلكترونية
