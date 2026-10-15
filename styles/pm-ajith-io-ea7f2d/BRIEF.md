# ديستيل بوك: ريل ثلاثين ثانية على شبكة قاسية — Distilbook motion showreel

> ريل منتج بارد الإيقاع مدته 30 ثانية يعرض Distilbook في ثلاث حركات: صدمة رقمية، جولة بطاقات، ثم برهان بالأرقام، على شبكة ثابتة بلون تمييز واحد.
>
> A cold, tight 30-second product reel presenting Distilbook in three acts: a numeric hook, a card tour, then proof by numbers, on a persistent grid with one accent colour.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/ajith-io-ea7f2d
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 30 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع منتج Distilbook (نفترضه أداة لاختصار الكتب؛ المصدر يطلب البحث عنه ومحاكاة أسلوب فيديو مرجعي لم نره). الهدف أن يبدو الريل أنيقاً وحاداً بما يكفي ليُشارك كقطعة أسلوبية بحد ذاتها، مع إيصال وعد المنتج في ثلاث حركات واضحة. اللغة الحركية مبنية على الدقة: شبكة خلفية ثابتة تُقاس عليها كل حركة، قطع حادة على الإيقاع، وحركات قصيرة تستقر بلا ارتداد؛ هي نقيض الانسيابية الدافئة، أقرب إلى ريل أدوات المطورين.

## Concept
The subject is the Distilbook product (assumed to be a book-condensing tool; the source asks to research it and to mimic a reference video we have not seen). The goal is a reel sharp and elegant enough to be shared as a style piece in its own right, while delivering the product promise in three clear acts. The motion language is about precision: a persistent background grid that every move is measured against, hard cuts on the beat, and short moves that settle without bounce; the opposite of warm fluidity, closer to a developer-tools reel.

## المشاهد المقترحة
- 0-2 ث: افتتاح بارد على شبكة: عدّاد يدور من عدد صفحات بالمئات نزولاً إلى رقم دقائق أحادي، ثم يتوقف بضربة.
- 2-8 ث: يُرسم الشعار ضربة ضربة على الشبكة؛ يُكتب تحته وعد من سطر واحد بتباعد حروف يضيق من فضفاض إلى طبيعي.
- 8-16 ث: جولة البطاقات: غلاف كتاب ينزلق للداخل، بطاقة ملخّص تتفتح بجانبه، سطور النقاط المفتاحية تُكتب واحدة كل 400 ms، ومؤشر يقفز بين البطاقات على قطع حاد.
- 16-23 ث: برهان الأرقام: عمودان يتسابقان (قراءة كاملة مقابل خلاصة)، sparkline لعدد الكتب المنجزة أسبوعياً يُرسم، وثلاث بلاطات إحصائية تُختم على ضربات متتالية.
- 23-28 ث: انفجار نصي: خمس صفات قصيرة تُقطع بملء الإطار، واحدة لكل ضربة، بينما تدور الكاميرا 15 درجة حول مستوى الشبكة.
- 28-30 ث: يخرج كل شيء للأعلى بمسحة واحدة؛ الشعار ودعوة إجراء قصيرة يثبتان على الشبكة.

## Proposed scenes
- 0-2s: Cold open on a grid: a counter spins from a page count in the hundreds down to a single-digit minute figure, then slams to a stop.
- 2-8s: The logo is drawn stroke by stroke on the grid; a one-line promise types in beneath it with tracking tightening from loose to normal.
- 8-16s: Card tour: a book cover slides in, a summary card unfolds beside it, key-point lines type in one per 400 ms, and a cursor flicks between cards on hard cuts.
- 16-23s: Proof by numbers: two bars race (full read versus summary), a sparkline of books finished per week draws, and three stat tiles stamp in on consecutive beats.
- 23-28s: Kinetic burst: five short adjectives cut in at full frame, one per beat, while the camera orbits 15 degrees around the grid plane.
- 28-30s: Everything exits upward on a single wipe; logo lockup and a short call to action hold on the grid.

## قواعد الحركة
- الحركات قصيرة وحاسمة: 300-450 ms بمنحنى cubic-bezier(0.22, 1, 0.36, 1)؛ لا تجاوز ولا ارتداد.
- القطع الحاد مسموح ويجب أن يقع تماماً على ضربات مسار بإيقاع 120 BPM؛ يمكن أن يسبق القطع ثبات إطارين لكن لا إطار وميض أبداً.
- الشبكة (خلايا 24 px عند 1080p بشفافية 8 بالمئة) تبقى في كل لقطة؛ تلتصق العناصر بمواضع الشبكة عند السكون ولا تغادرها إلا أثناء الحركة.
- الطباعة: grotesk ثقيل للعناوين وmonospace للأرقام؛ تباعد العناوين يتحرك من +8 بالمئة إلى 0 عند الدخول خلال 400 ms.
- العدّادات تستخدم easeOutExpo خلال 700 ms وتنتهي بضربة مقياس إلى 1.04 والعودة خلال 60 ms.
- الكاميرا مستوى ثنائي مسطح مع مدار واحد بحد أقصى 15 درجة في القطعة كلها؛ لا dolly zoom ولا ضجيج يد.
- اللون: خلفية شبه سوداء، نص أبيض مائل، ولون تمييز كهربائي واحد على الشعار والأعمدة والمؤشر؛ لا تدرجات.
- ممنوع: crossfade، توهج أو bloom، غبار جسيمات، motion blur أعلى من مكافئ غالق 180 درجة، وأي لون تمييز ثانٍ.

## Motion rules
- Moves are short and decisive: 300-450 ms with cubic-bezier(0.22, 1, 0.36, 1); nothing overshoots, nothing bounces.
- Hard cuts are allowed and must land exactly on beats of a 120 BPM track; a cut may be preceded by a 2-frame hold but never by a flash frame.
- The grid (24 px cells at 1080p, 8 percent opacity) persists in every shot; elements snap to grid positions at rest and only leave the grid while in motion.
- Typography: a heavy grotesk for headlines and a monospace for numbers; headline tracking animates from +8 percent to 0 on entry over 400 ms.
- Counters use easeOutExpo over 700 ms and end with a 60 ms scale punch to 1.04 and back.
- Camera is a flat 2D plane with at most one 15-degree orbit in the whole piece; no dolly zooms, no handheld noise.
- Colour: near-black background, off-white type, a single electric accent used on the logo, bars and the cursor; no gradients.
- Banned: crossfades, glow or bloom, particle dust, motion blur over 180-degree shutter equivalent, any second accent colour.

## Facts stated by the source (rewritten in our words)
- The creator asked for a 30-second motion graphics video about Distilbook in the manner of a showreel.
- A reference video was supplied to the AI and its visual style was to be matched; that reference is not available to us.
- The AI was asked to research the product; the creator wanted the result to feel exceptionally cool.
- Site tags: charts and kinetic type.

## Assumptions
Stated: 30 seconds, Distilbook subject, a reference video to mimic, showreel framing. Assumed: the grid-and-hard-cut direction (chosen as a deliberately different take from the 40-second sibling brief), the three-act structure, BPM, easings and the single-accent palette.

## Keywords
product reel, grid system, hard cut, شبكة, قطع على الإيقاع, book summary, تلخيص, monospace, stat tiles, sparkline, ريل منتج, نص حركي, counter, distilbook, tracking animation
