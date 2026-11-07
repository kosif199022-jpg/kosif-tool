# إنفوجرافيك متحرك: أيقونات وأرقام ومخططات مسطحة تشرح معلومة — إنفوجرافيك

> ريل عمودي بأسلوب الإنفوجرافيك المسطح: أيقونات بسيطة بألوان محدودة، أرقام كبيرة تعد صعوداً، أشرطة ودوائر نسب تمتلئ، أسهم تربط بين الخطوات، وعنوان لكل قسم على خلفية فاتحة منظمة.
>
> A vertical flat-design infographic reel: simple icons in a limited palette, large numbers counting up, bars and percentage rings filling, arrows linking steps, and a header for each section on a tidy light background.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/infographic
- التصنيفات / Categories: charts, diagrams
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 30 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
يحول موضوعاً معلوماتياً (إحصائية، خطوات، مقارنة) إلى سلسلة بطاقات بصرية واضحة، كل بطاقة معلومة واحدة تُبنى أمام المشاهد. التركيز على الوضوح: لون لكل فئة، أيقونة لكل مفهوم، رقم واحد بارز. يختلف عن «سباق المخططات» الذي يعرض بيانات زمنية تتسابق، وعن «المخططات المتحولة» التي تتحول من نوع مخطط لآخر، وعن «الخريطة الوثائقية»؛ هنا المزيج متنوع (أيقونات وأرقام ورسوم صغيرة) والقصة قصة شرح.

## Concept
It turns an informational topic (a statistic, steps, a comparison) into a series of clear visual cards, each one a single fact built in front of the viewer. The focus is clarity: one colour per category, one icon per concept, one standout number. It differs from chart-race, which shows time-series data racing, from morph-charts, which morph from one chart type into another, and from documentary-map; here the mix is varied (icons, numbers, small charts) and the story is an explanation.

## المشاهد المقترحة
- 0-2 ث: الافتتاح: رقم كبير يتصاعد من الصفر في المنتصف وفوقه سؤال في سطر واحد.
- 2-8 ث: القسم الأول: شريط عنوان ينزلق؛ ثلاث أيقونات تظهر في صف، لكل منها تسمية قصيرة، يربطها سهم يُرسم.
- 8-14 ث: القسم الثاني: مخطط أشرطة أفقي ينمو شريطاً شريطاً والقيم تتصاعد عند أطرافها.
- 14-20 ث: القسم الثالث: حلقة دائرية تمتلئ إلى نسبة مئوية والجزء الباقي معنون؛ وشبكة صغيرة من أيقونات الأشخاص تبرز 3 من 10.
- 20-26 ث: المقارنة: عمودان متجاوران بأيقونات وقيم، وبينهما شارة «مقابل».
- 26-30 ث: الملخص: كل الأرقام المهمة تصغر في بطاقة ملخص؛ ويظهر سطر المصدر والحساب أسفلها.

## Proposed scenes
- 0-2s: Hook: a big number counts up from 0 in the centre with a one-line question above it.
- 2-8s: Section 1: a header bar slides in; three icons pop in a row, each with a short label, connected by a drawn arrow.
- 8-14s: Section 2: a horizontal bar chart grows bar by bar with values ticking at the ends.
- 14-20s: Section 3: a donut ring fills to a percentage while the remaining slice is labelled; a small person-icon grid highlights 3 of 10.
- 20-26s: Comparison: two columns side by side with icons and values, a 'vs' badge in between.
- 26-30s: Summary: all key numbers shrink into a recap card; the source line and handle appear at the bottom.

## قواعد الحركة
- الألوان: خلفية #f7f9fc، بطاقات #ffffff، نص #1b2433، فئات #2f80ed / #27ae60 / #f2994a / #eb5757، خطوط شبكة #e3e8ef.
- رسوم متجهة مسطحة فقط: بلا تدرجات ولا ثلاثي أبعاد؛ والأيقونات بخط ثابت 3 بكسل أو بتعبئة مسطحة، وزوايا البطاقات مستديرة 16-24 بكسل.
- الأرقام تتصاعد في 20-30 إطاراً بتباطؤ وتستقر بقفزة 1.06؛ والأشرطة والحلقات تمتلئ بالتسهيل نفسه بفارق 4-6 إطارات.
- الأسهم والوصلات تُرسم في 10-14 إطاراً بترتيب القراءة من اليمين لليسار.
- التسميات العربية بخط واضح بلا زوائد (مثل Tajawal أو IBM Plex Sans Arabic) بحجم 36-44 بكسل، والعناوين 64-72 بكسل عريض؛ ونظام أرقام واحد طوال الفيديو؛ والوحدات بجانب الأرقام بترتيب اليمين لليسار.
- تغيير القسم بانزلاق البطاقة (البطاقة كلها تخرج يساراً والتالية تدخل من اليمين) في 12 إطاراً.
- كل مخطط يُظهر مقياسه أو تسمياته؛ وسطر المصدر يظهر دائماً في النهاية.

## Motion rules
- Palette: background #f7f9fc, cards #ffffff, text #1b2433, categories #2f80ed / #27ae60 / #f2994a / #eb5757, grid lines #e3e8ef.
- Flat vector only: no gradients or 3D; icons use a consistent 3 px stroke or flat filled style, rounded corners 16-24 px on cards.
- Numbers count up over 20-30 frames with an ease-out and land with a 1.06 pop; bars and rings fill with the same ease, staggered 4-6 frames.
- Arrows and connectors draw on (stroke dash) over 10-14 frames in reading order right to left.
- Arabic labels in a clear sans (e.g. Tajawal or IBM Plex Sans Arabic) 36-44 px, headers 64-72 px Bold; keep one digit system throughout; units next to numbers stay in RTL order.
- Section changes use a card slide (whole card exits left, next enters from right) of 12 frames.
- Every chart must show its scale or labels; a source line is always shown at the end.

## Facts stated by the source (rewritten in our words)
- KOSIF lists this as an original style named infographic, tagged charts and diagrams, pointing to the motion-starter-kit infographic reference.

## Assumptions
Authored KOSIF definition, not an observed reference: the record points to a motion-starter-kit reference video, but fetching it was blocked (GitHub access not enabled for this session), so nothing was watched. Palette hex values, fonts, timings and scene beats are design choices written for this style, not measurements.

## Keywords
infographic, data explainer, icons, statistics, flat design, bar chart, donut chart, إنفوجرافيك, معلومات, إحصائيات, أيقونات, رسوم بيانية, شرح
