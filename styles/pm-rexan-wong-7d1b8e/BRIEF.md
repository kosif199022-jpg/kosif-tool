# جولة سريعة مصوّرة من الشاشة عبر معرض فيديوهات ومكتبة مكونات — Professional motion workflow breakdown

> تسجيل شاشة سلس مدته 11 ثانية بنسبة 4:3 على واجهات ويب بيضاء: يبدأ بتصغير من رأس معرض فيديوهات إطلاق إلى شبكة بطاقات تمر لأعلى بتمرير متواصل، ثم قطع إلى عرض منقسم بقائمة يساراً ولوحة تفاصيل يميناً، ثم قطع إلى مكتبة مكونات واجهة بشريط جانبي تُمرَّر بطاقاتها حتى النهاية، بلا نصوص مضافة ولا صوت.
>
> An 11-second 4:3 screen-capture tour of white web interfaces: it pulls back from a launch-video gallery header into a card grid that scrolls upward continuously, hard-cuts to a split view with a list on the left and a detail drawer on the right, then hard-cuts to a UI component library with a sidebar whose cards scroll past to the end, with no added captions and no audio.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/rexan-wong-7d1b8e
- التصنيفات / Categories: product-ui
- النسبة المقترحة / Aspect: 4:3 · المدة / Duration: 11 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
الفكرة عرض سير عمل مصمم موشن كما هو: بدل الرسوم الشارحة، الفيديو يمر بسرعة على الأدوات والمراجع التي يستعملها (معرض مراجع، صفحة تفاصيل لمرجع واحد، مكتبة مكونات جاهزة). القيمة في الإيقاع: تمرير عمودي ناعم ثابت السرعة، ومعاينات الفيديو داخل البطاقات تتحرك وحدها فتبدو الصفحة حية، وقطعتان حادتان فقط تفصلان المراحل الثلاث.

## Concept
The idea is to show a motion designer's workflow as it really looks: instead of explanatory graphics, the video skims the tools and references in use (a reference gallery, a detail page for one reference, a ready-made component library). The value is in the rhythm: a smooth, constant-speed vertical scroll, looping video previews inside the cards that keep the page alive, and only two hard cuts separating the three stages.

## المشاهد المقترحة
- 0-1.4 ث: رأس صفحة المعرض بعنوان في المنتصف وشريط بحث؛ ثم تتصغر الصفحة لتصبح شبكة كثيفة من أربعة أعمدة لبطاقات فيديو.
- 1.4-4.9 ث: تمرير متواصل لأعلى عبر شبكة المعرض؛ والمصغرات (لقطات منتجات داكنة، بطاقات خطوط ملونة، أشخاص أمام الكاميرا) تشغّل معايناتها وهي تمر.
- 4.9-7.9 ث: قطع حاد إلى تخطيط منقسم: القائمة تستمر في التمرير يساراً بينما درج تفاصيل ثابت يميناً يعرض بطاقة عنوان زرقاء كبيرة وشارات وتبويبات وكتلة نص بخط ثابت العرض.
- 7.9-11 ث: قطع حاد إلى مكتبة مكونات: عمود تنقل يساراً بزر أزرق، وشبكة معاينات بطاقات واجهة (إحصاءات، لوحات تحكم، ملفات شخصية، بطاقات متدرجة) تُمرَّر لأعلى حتى نهاية المقطع.

## Proposed scenes
- 0-1.4s: Gallery page header with a centred title and search bar; the view scales down so the page shrinks into a dense four-column grid of video cards.
- 1.4-4.9s: Continuous upward scroll through the gallery grid; thumbnails (dark product shots, colourful type tiles, people on camera) play their own previews as they pass.
- 4.9-7.9s: Hard cut to a split layout: the card list keeps scrolling on the left while a fixed detail drawer on the right shows a big blue title card, tag chips, tabs and a monospace prompt block.
- 7.9-11s: Hard cut to a component library: a left nav column with a blue CTA, and a grid of UI card previews (stats, dashboards, profiles, gradient cards) scrolling up until the clip ends.

## قواعد الحركة
- تمرير عمودي ثابت السرعة بتسهيل خفيف، بنحو ارتفاع شاشة كل ثانيتين؛ بلا ميل كاميرا ولا عمق، فقط إزاحة عمودية وتصغير واحد في البداية.
- قطعتان حادتان فقط (عند نحو 4.9 و7.9 ث)؛ بلا تلاشٍ أو مسح أو عناوين بين الأقسام.
- المصغرات المضمّنة تكرر معايناتها فلا تبدو الصفحة ساكنة أثناء التمرير.
- الألوان هي ألوان الصفحات نفسها: خلفيات بيضاء #ffffff ورمادي فاتح #f4f4f5، نص شبه أسود #111111، أزرق مميز #2f3fd6 في بطاقة التفاصيل و#2563eb في زر المكتبة.
- الخطوط أصلية من الصفحات: خط واجهة بسيط صغير للتسميات وخط ثابت العرض لكتلة النص؛ لا شيء مضاف فوق الصورة.
- الإطار 4:3 بدقة 960x720، فتظهر الصفحات أضيق من عرض الحاسوب وتملأ الكادر من الحافة للحافة.

## Motion rules
- Constant, eased vertical scroll at roughly one viewport height every 2 s; no camera tilt or 3D, only translateY and one initial scale-down.
- Exactly two hard cuts (about 4.9 s and 7.9 s); no fades, wipes or titles between sections.
- Embedded thumbnails loop their own previews so the scrolling page never looks static.
- Palette is whatever the pages use: white #ffffff and light grey #f4f4f5 backgrounds, near-black text #111111, an accent blue #2f3fd6 on the detail card and #2563eb on the library CTA.
- Type stays native to the pages: small grotesk UI sans for labels, monospace for the prompt block; nothing is overlaid.
- Framing is 4:3 at 960x720, so pages are shown narrower than desktop width and fill the frame edge to edge.

## Facts stated by the source (rewritten in our words)
- The title presents the clip as a breakdown of a professional motion-design workflow.
- The listing names Remotion as the tool; the creator is not credited by handle on the page.

## Assumptions
Observed from 24 frames sampled every ~0.46 s plus close sampling around both cuts: the gallery pull-back and scroll, the split list/detail view, the component library scroll and the two hard cuts over 11 s; the file has no audio track. Assumed: that the scroll is rendered (e.g. pages captured then animated in Remotion) rather than a live recording; the brief deliberately does not reproduce the readable prompt text visible on screen.

## Keywords
screen recording, website scroll, workflow breakdown, gallery tour, component library, split view, hard cut, تسجيل شاشة, تمرير صفحة, سير العمل, معرض فيديوهات, مكتبة مكونات
