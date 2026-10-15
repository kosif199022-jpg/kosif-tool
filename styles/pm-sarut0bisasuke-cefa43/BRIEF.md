# وصفة الوايت روشن من الكأس الفارغة إلى الكوكتيل — White Russian recipe animation

> فيلم شرح من لقطة واحدة متصلة يبني كوكتيل الوايت روشن مكوّنًا بعد مكوّن مع إظهار الكمية ومستوى الامتلاء في الكأس خلال 30 ثانية.
>
> A 30-second single-shot explainer that builds a White Russian layer by layer, showing each pour, its measurement and the rising fill level in the glass.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/sarut0bisasuke-cefa43
- التصنيفات / Categories: charts, diagrams, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 30 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: HTML Canvas, SVG, CSS

## الفكرة
الموضوع هو وصفة كوكتيل الوايت روشن بثلاثة مكوّنات: فودكا، ليكيور قهوة، وقشدة، تُسكب تباعًا فوق الثلج في كأس قصيرة. الهدف أن يفهم المشاهد الترتيب والكميات من مجرد مشاهدة الكأس تمتلئ، فيكون مستوى السائل هو المؤشر الرئيسي بدل النص. ما يميّز لغة الحركة أنها لقطة واحدة لا تُقطع: الكاميرا ثابتة أمام الكأس، وكل ما يتغيّر هو الطبقات السائلة وعدّادات الملّيلتر وبطاقات الأسماء، وتُرسم السوائل بتموّج سطحي بسيط عبر Canvas.

## Concept
The subject is a three-ingredient White Russian: vodka, coffee liqueur and cream poured in turn over ice in a short rocks glass. The communication goal is that a viewer understands order and quantities just by watching the glass fill, so the liquid level, not the text, is the primary indicator. The motion language is a single uncut shot: the camera stays fixed on the glass while liquid layers, millilitre counters and ingredient labels do all the work, with the liquids drawn as gently rippling surfaces in Canvas.

## المشاهد المقترحة
- 0-3ث: يظهر العنوان مع كأس قصيرة فارغة في المنتصف؛ خط أفقي رفيع يمثّل سطح البار، وقائمة مكوّنات باهتة تقف على اليمين.
- 3-7ث: تسقط أربع مكعبات ثلج واحدة تلو الأخرى، ترتدّ مرة ثم تستقر؛ تظهر هالة صقيع خفيفة على حافة الكأس.
- 7-13ث: تميل زجاجة الفودكا من أعلى اليسار؛ ينساب خيط شفاف بينما يعدّ العدّاد من 0 إلى 50 مل ويرتفع خط الامتلاء إلى نحو ثلث الكأس.
- 13-19ث: يُسكب ليكيور القهوة كطبقة داكنة؛ يعدّ العدّاد من 0 إلى 20 مل، يغمق السائل من الأسفل وتضيء بطاقة المكوّن على اليمين.
- 19-25ث: تُسكب القشدة ببطء فوق ظهر ملعقة؛ تطفو كغطاء فاتح ثم تتموّج داخل الطبقة الداكنة بدوّامات ناعمة (30 مل).
- 25-30ث: تحريك واحد خفيف بملعقة البار، وتضيء قائمة الوصفة على اليمين بالكميات الثلاث كاملة، ويعود العنوان كبطاقة ختام.

## Proposed scenes
- 0-3s: Title and an empty rocks glass fade up at centre; a thin horizontal rule marks the counter top and a small ingredient list sits dimmed on the right.
- 3-7s: Four ice cubes drop one after another, bounce once and settle; the glass gets a faint frosted rim.
- 7-13s: A vodka bottle tilts in from top-left; a clear stream pours while a counter runs 0 to 50 ml and the fill line rises to about a third of the glass.
- 13-19s: Coffee liqueur pours as a dark layer; the counter runs 0 to 20 ml, the liquid darkens from the bottom and the label on the right lights up.
- 19-25s: Cream is poured slowly over the back of a spoon; it floats as a pale cap, then marbles into the dark layer with soft swirls (30 ml).
- 25-30s: A bar spoon gives one gentle stir, the recipe list on the right is now fully lit with all three amounts, and the title returns as an end card.

## قواعد الحركة
- امتلاء السائل بمنحنى easeOutCubic خلال 1400-1800 مللي ثانية لكل سكبة؛ يحمل السطح تموّجًا جيبيًا بارتفاع 2-3 بكسل يخمد تمامًا بعد 600 مللي ثانية من توقّف السكب.
- تسقط مكعبات الثلج بمنحنى easeOutBounce (ارتداد 12 بكسل) خلال 700 مللي ثانية لكل مكعب، بفاصل 180 مللي ثانية بينها.
- عدّادات الملّيلتر مربوطة بقيمة التقدّم نفسها التي تحرّك ارتفاع السائل، فلا ينفصل الرقم عن المستوى أبدًا.
- تنزلق بطاقات المكوّنات 24 بكسل من اليمين بمنحنى easeOutQuint خلال 450 مللي ثانية، وتخفت إلى 40% شفافية بعد انتهاء السكب.
- الكاميرا: لقطة واحدة متصلة بإطار ثابت مع دفعة بطيئة واحدة من مقياس 1.00 إلى 1.06 على مدى 30 ثانية كاملة؛ لا قطع ولا اهتزاز يدوي.
- تدخل الزجاجة بمنحنى easeOutBack (تجاوز 1.15) خلال 600 مللي ثانية، وتميل إلى 35 درجة بمنحنى easeInOutSine، وتخرج من حيث دخلت.
- اتجاه الألوان (مقترح): خلفية بار داكنة دافئة، فودكا شفافة، ليكيور بني عميق، قشدة عاجية؛ يجب أن تبقى السوائل الثلاثة متمايزة في الإضاءة بوضوح.
- ممنوع: الصور الفوتوغرافية الجاهزة، والتصيير ثلاثي الأبعاد، والانتقالات بين المشاهد، وأي نص يظهر قبل أن يكون مكوّنه داخل الكأس فعلًا.

## Motion rules
- Liquid fill uses easeOutCubic over 1400-1800 ms per pour; the surface carries a 2-3 px sine ripple that damps to zero 600 ms after the pour stops.
- Ice cubes fall with easeOutBounce (bounce height 12 px) over 700 ms each, staggered 180 ms apart.
- Millilitre counters are bound to the same progress value as the fill height, so number and level never drift apart.
- Ingredient labels slide in 24 px from the right with easeOutQuint over 450 ms and dim to 40% opacity once the pour ends.
- Camera: one continuous shot, fixed framing, with a single slow push-in from scale 1.00 to 1.06 across the full 30 s; no cuts and no handheld shake.
- The bottle enters with easeOutBack (overshoot 1.15) over 600 ms, tilts to 35 degrees with easeInOutSine, and leaves the way it came.
- Colour direction (proposed): warm dark bar backdrop, clear vodka, deep brown liqueur, ivory cream; keep the three liquids clearly distinct in luminance.
- Banned: stock photos, 3D renders, transitions between scenes, and any text that appears before its ingredient is actually in the glass.

## Facts stated by the source (rewritten in our words)
- The requested length is 30 seconds.
- The creator left the choice between JavaScript and HTML to the model, asking for whichever gives the best result.
- The film must cover the whole recipe, starting with an empty glass and ending with the finished drink.
- Ingredients and their measurements should appear as each one goes into the glass, in an explainer-video manner.

## Assumptions
The source states duration, subject and explainer framing; the measurements (50/20/30 ml), the single-shot approach, colours and timings are my proposed direction and not observed from the video.

## Keywords
كوكتيل, وصفة متحركة, سكب السوائل, فودكا, قشدة, ليكيور قهوة, شرح, cocktail recipe, liquid animation, pour, measurements, explainer, canvas, bar
