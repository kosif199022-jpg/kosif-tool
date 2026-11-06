# سباق أعمدة بيانات عبر الزمن — سباق رسوم

> سباق أعمدة أفقية مرتبة: الأعمدة تطول وتتبادل المراكز بانزلاق ناعم مع مرور السنوات، عداد سنة ضخم في الزاوية، أعلام أو شعارات على رؤوس الأعمدة، قيم تعدّ حيًّا، ولحظات تثبيت تبرز التجاوزات المهمة.
>
> A ranked horizontal bar chart race: bars grow and swap positions with smooth slides as the years tick by, a huge year counter sits in the corner, icons or flags ride the bar ends, values count live, and brief pauses highlight the key overtakes before the final ranking holds.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: charts
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 40 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
تحويل جدول بيانات ممل إلى منافسة يتابعها المشاهد كمباراة: من يتصدر؟ متى حدث التجاوز؟ كل عمود شخصية لها لون ثابت وأيقونة، والزمن هو المحرك الوحيد. القصة تُروى بالتجاوزات وليس بالأرقام.

## Concept
Turn a dull data table into a contest the viewer follows like a match: who leads, and when did the overtake happen? Each bar is a character with a fixed colour and icon, and time is the only engine. The story is told through overtakes, not numbers.

## المشاهد المقترحة
- 0-3 ث: عنوان جاذب في الأعلى («من تصدّر 20 سنة؟»)، المحور والمسارات الفارغة تنزلق للداخل، وعداد السنة يظهر بقيمته الأولى.
- 3-12 ث: الزمن يجري: الأعمدة تستكمل قيمها كل إطار، وتبادل المراكز ينزلق رأسيًا في 400-500 مللي ثانية، والقيم تعدّ بفواصل الآلاف.
- 12-15 ث: أول تجاوز مهم: التشغيل يبطؤ إلى 30%، العمودان يومضان بإطار، وتسمية توضيحية تشرح الحدث.
- 15-30 ث: التشغيل يعود أسرع؛ المحور يعيد تحجيمه بنعومة مع نمو المتصدر؛ والعناصر الخارجة تنزلق للأسفل والجديدة تدخل.
- 30-35 ث: السنة الأخيرة: السباق يتوقف، المتصدر يحصل على تاج أو توهج، وسطر خلاصة يُمسح للداخل.
- 35-40 ث: ثبات على الترتيب النهائي مع ذكر المصدر بخط صغير.

## Proposed scenes
- 0-3s: Hook title on top ('who led for 20 years?'), axis and empty lanes slide in; the year counter appears at its first value.
- 3-12s: Timeline plays: bars interpolate values each frame, rank swaps slide vertically in 400-500 ms, values count with thousands separators.
- 12-15s: First key overtake: playback slows to 30%, the two bars flash an outline and a callout label explains the event.
- 15-30s: Playback resumes faster; the axis rescales smoothly as the leader grows; dropped entries slide out the bottom, new ones slide in.
- 30-35s: Final year: the race stops, the leader gets a crown or glow, a summary line wipes in.
- 35-40s: Hold on the final ranking with source credit in small type.

## قواعد الحركة
- القيم تُستكمل باستمرار بين نقاط البيانات (خطيًا مع الزمن، والتباطؤ فقط عند التوقفات)؛ والترتيب يُعاد كل إطار ومواقع الأعمدة تنزلق بنابض إلى أماكنها في 400-500 مللي ثانية.
- 8-10 أعمدة على الأكثر في 9:16؛ ارتفاع العمود 70-90 بكسل وفجوات 16-20 بكسل؛ والتسميات داخل العمود إن اتسعت وإلا خارجه.
- كل عنصر يحتفظ بلون واحد طوال الفيديو؛ واللوحة مجموعة من 10 ألوان فئوية على خلفية داكنة #0f1115 وخطوط شبكة #2a2e36.
- عداد السنة: أرقام جدولية بحجم 220-300 بكسل وشفافية 30%، أسفل اليمين في التخطيط العربي (وأسفل اليسار في اللاتيني).
- المحور يعيد تحجيمه بتباطؤ 600 مللي ثانية عندما تتغير القيمة القصوى بأكثر من 15%؛ ولا قفزات أبدًا.
- اللحظات المهمة: إبطاء إلى 25-35% لمدة 2-3 ثوانٍ مع تسمية توضيحية؛ وثلاث لحظات على الأكثر.
- العربية: الأسماء ككلمات كاملة، والمسارات محاذاة لليمين؛ والأرقام بنظام واحد ثابت (غربية أو هندية) معزولة بعلامات الاتجاه.
- الفرق عن تحولات البيانات والإنفوجرافيك: سباق الأعمدة رسم واحد مرتب يحركه الزمن؛ تحولات البيانات تحوّل نوع رسم إلى آخر؛ والإنفوجرافيك يمزج الأيقونات والإحصاءات.

## Motion rules
- Values interpolate continuously between data points (linear in time, eased only at pauses); ranks re-sort every frame and bar Y positions spring to new slots in 400-500 ms.
- Show 8-10 bars max on 9:16; bar height 70-90 px with 16-20 px gaps; labels inside the bar if they fit, else outside.
- Each entity keeps one colour for the whole video; the palette is a 10-colour categorical set on dark #0f1115 with grid lines #2a2e36.
- Year counter: tabular figures, 220-300 px, 30% opacity, bottom-right in RTL layouts (bottom-left in LTR).
- Axis rescales with a 600 ms ease when the max changes by more than 15%; never jump.
- Key moments: slow to 25-35% speed for 2-3 s with a callout; at most 3 per video.
- Arabic: names as whole words, right-aligned lanes for RTL layouts; numbers in Western or Arabic-Indic digits consistently, isolated with bidi marks.
- Difference from morph-charts and infographic: chart-race is one ranked bar chart driven by time; morph-charts transform one chart type into another; infographic mixes icons and stats.

## Facts stated by the source (rewritten in our words)
- The public description states nothing specific beyond the title.

## Assumptions
This is an authored KOSIF definition, not an observed reference: there is no reference video for this base style, so palette, type, timings and beats are a design decision written for KOSIF, to be refined per project. Requires a clean time-series table from the user; data accuracy is the user's responsibility.

## Keywords
bar chart race, chart race, ranking, data over time, overtake, year counter, سباق أعمدة, سباق بيانات, ترتيب, بيانات عبر الزمن, تجاوز, رسوم بيانية
