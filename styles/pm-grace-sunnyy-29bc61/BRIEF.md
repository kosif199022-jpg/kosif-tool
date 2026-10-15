# ريل الكي فريم: من داخل الخط الزمني — Keyframe motion design reel

> ريل 15 ثانية يجعل معيّن الـ keyframe ومنحنيات المحرر بطلَي الإطار، ورأس التشغيل يعبر الشاشة طوال المدة لتثبت كل ثانية قيمتها.
>
> A 15-second reel where the keyframe diamond and editor curves are the heroes, and a playhead crossing the frame makes every second accountable.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/grace-sunnyy-29bc61
- التصنيفات / Categories: charts
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع ريل بورتفوليو يُشاهَد كأنه من داخل أداة التحريك: مسطرة زمنية، ورأس تشغيل، ومعيّنات keyframe، ومنحنيات bezier تُرسم ثم تُنفَّذ أمام العين. الهدف إبراز الاتجاه الفني والتكوين والحركة القوية التي طلبها المصدر، عبر إثبات أن كل حركة على الشاشة مطابقة للمنحنى المرسوم. ما يميز اللغة الحركية هو الصرامة التكوينية: شبكة من 12 عمودًا، وعنصر مهيمن واحد في كل إطار، ومساحة سلبية لا تقل عن 60%، مع رسم بياني حي يقارن ثلاثة منحنيات في اللحظة نفسها.

## Concept
The subject is a portfolio reel seen as if from inside the animation tool: a timeline ruler, a playhead, keyframe diamonds and bezier curves that are drawn and then executed in front of the viewer. The goal is to deliver the art direction, composition and powerful motion the source asks for by proving that every movement on screen matches the curve drawn beside it. The distinctive motion language is compositional rigour: a 12-column grid, one dominant element per frame, at least 60% negative space, and a live chart comparing three easing curves at the same instant.

## المشاهد المقترحة
- 0-2 ث: مسطرة زمنية تمتد على الحافة السفلية؛ رأس التشغيل يبدأ من الصفر وسيقطع العرض الكامل خلال 15 ثانية. معيّن keyframe يضيء عند الصفر.
- 2-5 ث: منحنى bezier يُرسم بين معيّنين في الثلثين العلويين؛ كرة تتبع المنحنى بدقة لتثبت التسهيل في الزمن الحقيقي.
- 5-8 ث: ثلاثة منحنيات تتراكم (linear وease-out وspring) وثلاثة أشرطة تتسابق: الأشرطة تكوّن رسمًا بيانيًا حيًا يقارن المسافة التي قطعها كل منها في اللحظة نفسها.
- 8-11 ث: المعيّنات تتضاعف إلى شبكة؛ كل معيّن ينقلب ليكشف تكوينًا مصغرًا (نص، شكل، رسم بياني) مبنيًا على شبكة صارمة من 12 عمودًا.
- 11-13.5 ث: الشبكة تميل 12° وتنهار على طول المنحنى في معيّن كبير واحد يصبح علامة المصمم.
- 13.5-15 ث: رأس التشغيل يبلغ النهاية؛ الاسم والدور يظهران؛ معيّن keyframe أخير يغلق المسطرة.

## Proposed scenes
- 0-2s: A timeline ruler spans the bottom edge; a playhead starts at 0 and will travel the full width across the 15 s. A diamond keyframe lights up at 0.
- 2-5s: A bezier curve draws between two diamonds in the upper two-thirds; a ball follows the curve exactly, proving the easing in real time.
- 5-8s: Three curves stack (linear, ease-out, spring) and three bars race: the bars form a live comparison chart of how far each has travelled at the same moment.
- 8-11s: Diamonds multiply into a grid; each flips to reveal a mini-composition (type, shape, chart) built on a strict 12-column grid.
- 11-13.5s: The grid tilts 12° and collapses along the curve into one large diamond that becomes the designer's mark.
- 13.5-15s: The playhead reaches the end; name and role appear; a final keyframe diamond closes the ruler.

## قواعد الحركة
- رأس التشغيل يتحرك خطيًا عبر عرض الإطار الكامل خلال 15 ثانية بالضبط ولا يتوقف؛ كل حد بين مقطعين يُعلَّم بمعيّن يضيء على المسطرة.
- المنحنيات تُرسم بـ stroke-dashoffset خلال 600 ms؛ الكرة التابعة تأخذ عيناتها من دالة cubic-bezier نفسها المرسومة كي يتطابق الرسم مع الحركة دائمًا.
- المنحنيات الثلاثة المقارنة: linear وcubic-bezier(0.22, 1, 0.36, 1) ونابض (stiffness 200 وdamping 12)؛ وتعمل الثلاثة للمدة نفسها 1200 ms.
- التخطيط شبكة من 12 عمودًا بفواصل 24 px؛ عنصر مهيمن واحد في كل إطار ومساحة سلبية لا تقل عن 60% في أي لحظة.
- الكاميرا ثابتة باستثناء ميل واحد 12° خلال 500 ms أثناء الانهيار؛ لا تكبير ولا اهتزاز.
- اللوحة: خلفية عميقة، ونص فاتح، ولون تمييز واحد عالي التشبع محجوز للمعيّنات والمنحنيات ورأس التشغيل؛ لا يستعمله أي عنصر آخر.
- الطباعة: خط عرض مضغوط بحجم 200 px للعلامة والاسم، وmonospace بحجم 28 px للأكواد الزمنية التي تتحرك في الزمن الحقيقي.
- ممنوع: لون تمييز ثانٍ، والجسيمات الزخرفية، واهتزاز الكاميرا العشوائي، وأي حركة لا يُعرض منحناها أو يُلمَّح إليه على الشاشة.

## Motion rules
- The playhead moves linearly across the full frame width over exactly 15 s and never pauses; every beat boundary is marked by a diamond lighting up on the ruler.
- Curves draw with stroke-dashoffset over 600 ms; the follower ball samples the same cubic-bezier function as the drawn curve so motion and graph always agree.
- The three compared curves are linear, cubic-bezier(0.22, 1, 0.36, 1) and a spring (stiffness 200, damping 12); all three run for the same 1200 ms.
- Layout is a 12-column grid with 24 px gutters; one dominant element per frame and at least 60% negative space at any moment.
- Camera is locked except one 12° tilt over 500 ms during the collapse; no zooms, no shakes.
- Palette: a deep background, pale type and one high-saturation accent reserved for diamonds, curves and the playhead; nothing else may use the accent.
- Typography: condensed display at 200 px for the mark and name, 28 px monospace for timecodes that tick in real time.
- Banned: a second accent colour, decorative particles, random camera shake, and any motion whose curve is not shown or implied on screen.

## Facts stated by the source (rewritten in our words)
- A 15-second piece intended as a portfolio item attached to a résumé.
- Any tools or techniques are allowed and creative freedom is total.
- The creator prioritises strong visual design, bold art direction, striking composition and powerful motion, with no wasted second.
- Catalogued under charts; the keyframe theme comes from the catalogue title.

## Assumptions
The inside-the-timeline concept, the curve comparison chart and the palette are proposals; the source states priorities and length but no scenes, colours or stack.

## Keywords
portfolio reel, keyframe diamond, bezier curve, graph editor, playhead, easing comparison chart, 12-column grid, negative space, ريل بورتفوليو, منحنى بيزييه, خط زمني, شبكة تخطيط, مقارنة تسهيل
