# رحلة على الخريطة — خريطة ورقية قديمة يرسم عليها المسافر طريقه — رحلة على الخريطة

> خريطة مرسومة بألوان ورق قديم (رملي وبحار زرقاء باهتة) تُرى بميل منظوري خفيف، يتحرك عليها جمل صغير مرسوم بينما يُرسم خلفه مسار أحمر متقطع، وتُغرس رايات حمراء في كل مدينة مع بطاقة ورقية تحمل اسمها وجملة قصيرة، وبطاقة ثابتة في الزاوية تعدّ المسافة والسنة، وتنتهي بابتعاد يكشف الرحلة كلها.
>
> An illustrated old-paper map (sand land, pale blue seas) seen with a slight perspective tilt, where a small drawn camel travels while a dashed red route draws behind it, red flags plant at each city with a paper label card holding its name and a short line, a fixed corner card counts distance and year, and a final pull-out reveals the whole journey.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/map-journey
- التصنيفات / Categories: diagrams
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 34 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG, CSS

## الفكرة
القصة تُروى كرحلة: المشاهد يرافق المسافر محطة بعد محطة، فيتذكر المكان والترتيب والمسافة معاً. الخريطة مرسومة بإحساس المخطوطات (أسماء أقاليم بخط عربي يدوي، جبال صغيرة مرسومة، بوصلة)، والكاميرا تتبع المسافر عن قرب ثم تبتعد في النهاية لتكشف حجم الرحلة.

## Concept
The story is told as a journey: the viewer travels with the traveller stop by stop, remembering place, order and distance together. The map has a manuscript feel (region names in hand-lettered Arabic, little drawn mountains, a compass rose), and the camera follows the traveller closely, then pulls back at the end to reveal the scale of the trip.

## المشاهد المقترحة
- 0-3 ث: الخريطة كاملة؛ بطاقة ورقية في المنتصف تحمل اسم الرحلة بخط عربي وسطراً فرعياً بالمسار والسنوات.
- 3-6 ث: تختفي البطاقة وتنزلق الكاميرا وتميل نحو مدينة البداية؛ وبوصلة في أعلى اليسار.
- 6-9 ث: المحطة الأولى: راية حمراء تُغرس، بطاقة اسم تقفز فوقها، وبطاقة العداد في الزاوية تظهر (المسافة 0 والسنة).
- 9-24 ث: مراحل السفر: الجمل يمشي على الساحل ويُرسم خلفه خط أحمر متقطع؛ الكاميرا تتبعه؛ وكل مدينة تأخذ راية وبطاقة اسم وتحديثاً للعداد (المسافة تعدّ صعوداً).
- 24-28 ث: الوجهة الأخيرة: راية خضراء تحدد الهدف مع بطاقة بمعنى المحطة.
- 28-34 ث: ابتعاد إلى الإقليم كاملاً يُظهر كل الرايات والمسار بأكمله؛ وبطاقة ختام تذكر المسافة الكلية والسنوات.

## Proposed scenes
- 0-3s: Wide map; a parchment title card centred with the journey name in Arabic calligraphy and a subtitle with route and years.
- 3-6s: The card clears and the camera glides and tilts down to the start city; a compass rose sits top-left.
- 6-9s: First stop: a red flag plants, a label card pops above it, and the corner counter card appears (distance 0, year).
- 9-24s: Travel legs: the camel walks along the coast with a dashed red line drawing behind; the camera trucks with it; each city gets a flag, label card and counter update (distance counts up).
- 24-28s: Final destination: a green flag marks the goal, label card with the stop's meaning.
- 28-34s: Pull-out to the full region showing every flag and the complete route; a closing card states the total distance and years.

## قواعد الحركة
- ألوان الخريطة (مأخوذة من المرجع): اليابسة #e4d3b0، رمل أغمق #cfbe9e، البحر #b8c8c6 إلى رمادي مزرق باهت، خطوط الحبر #736450، المسار والرايات أحمر #b8322a، والراية الأخيرة أخضر #3f8a3c؛ مع تعتيم ورقي على الأطراف.
- الخريطة مستوى مرسوم مسطح يُرى بميل ثلاثي الأبعاد خفيف (نحو 15-25 درجة) يتغير قليلاً مع حركة الكاميرا؛ ولا تُقطع أبداً.
- المسار: خط أحمر متقطع يُرسم خلف المسافر تماماً؛ والمسافر يمشي بدورة اهتزاز صغيرة ويتجه نحو اتجاه السفر.
- الرايات تُغرس بسقوط سريع واستقرار (0.3 ث)؛ وبطاقات الأسماء ورق كريمي بحد رفيع، الاسم العربي عريض في الأعلى وتعليق من سطر واحد تحته، تظهر بتكبير 0.25 ث.
- بطاقة العداد ثابتة أعلى اليمين: العنوان، والمسافة بأرقام تعدّ، والسنة، وصف نقاط تقدم.
- أسماء الأقاليم والبحار على الخريطة بخط عربي يدوي؛ ونص البطاقات بخط نسخ؛ وكلها من اليمين لليسار ومتصلة صحيحاً.
- الفرق عن الخريطة الوثائقية: خريطة مرسومة بروح المخطوطات مع شخصية مسافرة وعدادات، لا تضاريس حقيقية وصور أرشيفية؛ وفي 9:16 يبقى المسافر في العمود الأوسط وبطاقة العداد في الأعلى.

## Motion rules
- Map palette (sampled from the reference): land #e4d3b0, darker sand #cfbe9e, sea #b8c8c6 to pale blue-grey, ink lines #736450, route and flags red #b8322a, final flag green #3f8a3c; paper vignette at the edges.
- Map is a flat illustrated plane viewed with a gentle 3D tilt (about 15-25 degrees) that changes slightly as the camera moves; it never cuts.
- Route: dashed red line that draws exactly behind the traveller sprite; the sprite walks with a small bob cycle and faces the direction of travel.
- Flags plant with a quick drop and settle (0.3 s); label cards are cream paper with a thin border, Arabic name bold on top and a one-line caption below, popping in with a 0.25 s scale.
- Corner counter card stays fixed top-right: title, distance with counting digits, year, and a row of progress dots.
- Hand-lettered Arabic for region and sea names on the map; Naskh-style serif for card text; all RTL and correctly joined.
- Different from documentary-map: an illustrated manuscript-style map with a travelling character and counters, not real terrain and archival photos; for 9:16, keep the traveller in the centre column and stack the counter card at the top.

## Facts stated by the source (rewritten in our words)
- The reference in the starter kit is a 1280x720, 30 fps, 34 s silent clip.
- Its subject is a historical traveller's first journey from the Maghreb to Mecca, with cities marked along the North African coast, Egypt, the Levant and the Hijaz.

## Assumptions
Observed from a 24-frame grid of the starter-kit reference video (34 s, 16:9, no audio track): the parchment map, perspective tilt, camel traveller, dashed red route, flags, label cards, corner counter card and the closing pull-out with summary card. Assumed: exact timings between samples, the easing curves and the specific fonts; hex values are sampled from one frame and approximate.

## Keywords
map journey, travel route, old map, illustrated map, route animation, history trip, camel, رحلة على الخريطة, خريطة قديمة, مسار الرحلة, رحالة, تاريخ, خريطة مرسومة, رايات
