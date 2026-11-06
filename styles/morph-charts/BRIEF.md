# تحولات بيانات — رسم بياني يتحول من شكل لآخر — تحولات بيانات

> ريل عمودي 9:16 على خلفية كحلية داكنة تعرض فيه نفس مجموعة البيانات وهي تتحول بسلاسة من شكل لآخر: نقاط تتجمع إلى أعمدة، والأعمدة تلتف إلى دائرة نسب، والدائرة تنبسط إلى خط زمني، مع رقم كبير يعدّ في الأعلى وألوان ثابتة لكل فئة طوال الفيديو.
>
> A 9:16 reel on a dark navy background where one dataset keeps morphing smoothly between forms: scattered dots gather into bars, the bars curl into a donut of shares, the donut unrolls into a line over time, with a big counting number at the top and one fixed colour per category throughout.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: charts, shapes
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 34 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG, GSAP

## الفكرة
الفكرة أن البيانات كائن واحد يغيّر شكله ليجيب عن سؤال جديد كل مرة: كم؟ ثم ما النسبة؟ ثم كيف تغيّر مع الوقت؟ لا قطع بين الرسوم؛ كل عنصر يحتفظ بلونه وهويته وهو يتحول، فيتابع المشاهد الفئة نفسها عبر كل الأشكال. يناسب شرح الأرقام والتقارير والمقارنات.

## Concept
The data is one object that changes shape to answer a new question each time: how much? then what share? then how did it change over time? There are no cuts between charts; every element keeps its colour and identity as it morphs, so the viewer follows the same category through every form. Good for explaining numbers, reports and comparisons.

## المشاهد المقترحة
- 0-3 ث: سحابة نقاط (نقطة لكل وحدة) تنجرف على #0f1729؛ وعنوان السؤال يظهر في الأعلى بخط عربي عريض بسيط.
- 3-9 ث: تطير النقاط إلى أكوام وتندمج الأكوام في أعمدة مستديرة الأطراف (1.2 ث، بتأخير 60 مللي ث لكل عمود)؛ والقيم تعدّ فوق كل عمود.
- 9-16 ث: تنحني الأعمدة حول مركز وتصير قطاعات دائرة نسب (تحول 1.4 ث)؛ ورقم في المركز يُظهر النسبة الأكبر.
- 16-24 ث: تنبسط الدائرة إلى رسم خطي على محور زمني؛ الخط يُرسم من اليسار لليمين ونقطة نهايته تحمل قيمتها.
- 24-30 ث: إبراز فئة واحدة: الباقي يخفت إلى 25٪، ويزداد سُمك السلسلة المبرزة وتظهر ملاحظة تشرح الاستنتاج.
- 30-34 ث: ينهار كل شيء في رقم كبير واحد يصبح جملة الختام.

## Proposed scenes
- 0-3s: A cloud of dots (one per unit) drifts on #0f1729; the question title fades in at the top in bold Arabic sans.
- 3-9s: Dots fly into stacks and the stacks fuse into rounded bars (1.2 s, staggered 60 ms per bar); values count up above each bar.
- 9-16s: Bars bend around a centre and become donut segments (1.4 s morph); a centre number shows the leading share in %.
- 16-24s: The donut unrolls into a line chart over a time axis; the line draws left to right while its end dot carries a value label.
- 24-30s: One category is highlighted: others dim to 25%, the highlighted series thickens and a callout states the insight.
- 30-34s: Everything collapses back into one big number that becomes the closing statement.

## قواعد الحركة
- الخلفية #0f1729 مع إضاءة شعاعية خفيفة #18233d في المنتصف؛ والمحاور وخطوط الشبكة #2b3a5c بسُمك 1 بكسل.
- ألوان ثابتة للفئات طوال الفيديو: #4cc9f0، #f72585، #ffd166، #06d6a0، #9b5de5؛ ولا تغيّر الفئة لونها بين الأشكال.
- التحولات تكون بتحويل الشكل الهندسي نفسه وليس بالتلاشي المتقاطع؛ مدتها 1.0-1.5 ث بتسارع وتباطؤ ناعم وتأخير 40-80 مللي ث بين العناصر.
- الأرقام تعدّ بأرقام متساوية العرض (هندية أو لاتينية، تُختار مرة واحدة للفيديو) خلال نفس مدة التحول.
- الخطوط: عربي عريض بسيط (كايرو أو IBM Plex Sans Arabic بوزن 700) للعناوين ووزن متوسط للتسميات؛ العناوين من اليمين لليسار، والمحور الزمني يتبع اتجاه البيانات الطبيعي.
- كل شكل مكتمل يثبت 2.5 ث على الأقل حتى يُقرأ قبل التحول التالي.
- الفرق عن سباق الرسوم البيانية (أعمدة مرتبة تتسابق عبر الزمن) والإنفوجرافيك (أيقونات وتخطيط ثابت): التوقيع هنا مجموعة بيانات واحدة تتحول بين أنواع الرسوم.

## Motion rules
- Background #0f1729 with a faint radial lift #18233d at centre; axes and gridlines #2b3a5c at 1 px.
- Fixed categorical colours for the whole video: #4cc9f0, #f72585, #ffd166, #06d6a0, #9b5de5; a category never changes colour between forms.
- Morphs interpolate geometry (path morphing or shared vertex counts), never crossfade; 1.0-1.5 s with easeInOutCubic and 40-80 ms stagger.
- Numbers count with tabular figures (Arabic-Indic or Latin, chosen once per video) over the same duration as the morph.
- Typography: bold Arabic sans (Cairo or IBM Plex Sans Arabic 700) for titles, medium weight for labels; RTL titles, while time axes may read in the data's natural direction.
- Hold each finished form at least 2.5 s so it can be read before the next morph.
- Different from chart-race (ranked bars racing over time) and infographic (icons and static layout): here the signature is one dataset morphing between chart types.

## Facts stated by the source (rewritten in our words)
- Catalogued as a KOSIF original style named for data transformations, in the Charts and Shapes categories.

## Assumptions
Authored KOSIF definition, not an observed reference: there is no reference video for this base style (its page is the KOSIF repo root), so palette hex values, type choices, timings and scene beats are original KOSIF design decisions, not measurements. Assumed a single small dataset (3-5 categories) per reel of about 34 s; the user supplies the real numbers.

## Keywords
data morph, chart transition, bar to donut, line chart, data story, shape morph, statistics, تحولات بيانات, رسم بياني, بيانات, إحصاءات, تحول الأشكال, دائرة نسب
