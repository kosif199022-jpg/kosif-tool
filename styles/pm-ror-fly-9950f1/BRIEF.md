# وصفة نيغروني متحركة من الكأس الفارغة إلى الكوكتيل — Negroni recipe animation

> فيلم شرح مربع مدته 30 ثانية يبني كوكتيل نيغروني مكوناً بعد مكون مع المقادير وهي تُسكب في الكأس.
>
> A 30-second square explainer that builds a Negroni ingredient by ingredient, with measurements appearing as each pour fills the glass.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/ror-fly-9950f1
- التصنيفات / Categories: charts, diagrams, code
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 30 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: SVG, CSS, Remotion

## الفكرة
الموضوع وصفة كوكتيل نيغروني الكلاسيكي بمقاديره الثلاثة المتساوية، والهدف أن يفهم المشاهد الوصفة كاملة دون كلمة منطوقة: ماذا يُضاف، بأي كمية، وبأي ترتيب. اللغة الحركية مبنية على فيزياء السكب: مستوى السائل في الكأس يرتفع بالضبط بمقدار المكون، وكل مقدار يظهر كعلامة قياس على جانب الكأس، والألوان تمتزج طبقة فوق طبقة حتى يتوحد اللون الأحمر البرتقالي المميز عند التقليب.

## Concept
The subject is the classic Negroni with its three equal parts, and the goal is for a viewer to grasp the whole recipe without narration: what goes in, how much and in what order. The motion language is pour physics: the liquid level rises by exactly the amount added, each measure appears as a tick on the side of the glass, and the colours stack as layers until stirring blends them into the drink's signature amber red.

## المشاهد المقترحة
- 0-3 ث: يصعد عنوان 'نيغروني' من خط قناع فوق سطح بار داكن؛ تُرسم كأس روكس فارغة كخط حدودي ثم يسقط فيها مكعب ثلج كبير بارتداد زنبركي (ارتداد 1.2 واستقرار خلال 500 مللي ثانية).
- 3-10 ث: الجن: تميل زجاجة ظلية 35 درجة، ينساب سائل شفاف بتموج خفيف، يرتفع المستوى إلى الثلث الأول بينما يعد وسم القياس تصاعدياً حتى 30 مل بجانب علامة شريطية.
- 10-17 ث: الكامباري: تسكب زجاجة ثانية لوناً أحمر مشبعاً يغوص ويدور تحت طبقة الجن؛ يمتد سلم العلامات ويقرأ الوسم 30 مل؛ شريحة دائرية صغيرة في الزاوية تظهر امتلاء جزء من ثلاثة أجزاء متساوية.
- 17-23 ث: الفيرموث الحلو: سكبة كهرمانية داكنة تكمل الطبقات الثلاث؛ تُغلق الشريحة الدائرية إلى دائرة كاملة بوسم 1:1:1، ويصل المستوى إلى خط الامتلاء النهائي.
- 23-27 ث: تدخل ملعقة بار وتقلب؛ تمتزج الأشرطة الثلاثة إلى لون موحد خلال 1.5 ثانية، تظهر حبيبات تكاثف على الكأس، وتتلوى قشرة برتقال من الحافة العلوية.
- 27-30 ث: تُرتب قائمة المكونات والطريقة بجانب الشراب المكتمل كبطاقة وصفة نظيفة؛ تتمايل الكأس ببطء 3 درجات وتثبت البطاقة في الثانية الأخيرة.

## Proposed scenes
- 0-3s: Title lockup 'Negroni' rises from a mask line over a dark bar surface; an empty rocks glass draws itself as a stroke, then fills with a single large ice cube dropping in on a spring (bounce 1.2, settle 500 ms).
- 3-10s: Gin: a bottle silhouette tilts 35 degrees, a clear stream pours with a slight wobble, the level rises to the first third while a measurement tag counts up to 30 ml / 1 oz beside a tick mark.
- 10-17s: Campari: a second bottle pours a saturated red that sinks and swirls under the gin layer; the tick ladder extends and the tag reads 30 ml; a small pie wedge in the corner shows one of three equal parts filled.
- 17-23s: Sweet vermouth: a dark amber pour completes the three layers; the pie wedge closes to a full circle labelled 1:1:1, and the level reaches the final fill line.
- 23-27s: A bar spoon enters and stirs; the three bands blend into one uniform colour over 1.5 s, condensation beads appear on the glass, and an orange-peel twist curls in from the top edge.
- 27-30s: Ingredient list and method stack beside the finished drink as a clean recipe card; the glass gets a slow 3-degree rock and the card holds for the last second.

## قواعد الحركة
- مستوى السائل رقم واحد لكل مكون، مسهّل بمنحنى cubic-bezier(0.33, 0, 0.2, 1) على مدى السكب؛ يحصل السطح على تموج جيبي 2-4 بكسل بتردد 1.5 هرتز أثناء السكب ويخمد إلى الصفر خلال 600 مللي ثانية بعده.
- كل سكبة تستغرق 2.5-3 ثوانٍ؛ يبدأ عداد القياس مع أول قطرة وينتهي بالضبط عند توقف المستوى، فيبقى الرقم والسائل متزامنين دائماً.
- تدخل الزجاجات من خارج الإطار بتسهيل خروج 400 مللي ثانية، تميل خلال 300 مللي ثانية، وتغادر بالمسار نفسه معكوساً؛ لا تظهر زجاجتان معاً أبداً.
- طبقات اللون محددة لكل مكون (شفاف، أحمر، كهرماني) وتمتزج فقط أثناء التقليب؛ يستخدم المزج تدرجاً رأسياً ينهار إلى تعبئة مسطحة.
- الكاميرا مثبتة على الكأس مع دفع 5% عند التقليب؛ لا قطع، وكل تغيير مشهد هو تبديل وسم أو دخول عنصر.
- الطباعة: اسم المكون بخط sans ثقيل في الأعلى، والكمية برقم أحادي المسافة بجانب العلامة؛ تظهر الوسوم خلال 200 مللي ثانية وتختفي خلال 150 ولا تتداخل.
- ممنوع: زجاجات فوتوغرافية، جسيمات لامعة، وهج عدسة، أي مكون بلا كمية ظاهرة، وسكب يتجاوز خط الامتلاء.

## Motion rules
- Liquid level is a single number per ingredient, eased with cubic-bezier(0.33, 0, 0.2, 1) over the pour duration; the surface gets a 2-4 px sine wobble at 1.5 Hz while pouring and damps to zero within 600 ms after.
- Each pour runs 2.5-3 s; the measurement counter starts on the first drop and finishes exactly when the level stops, so number and liquid are always in sync.
- Bottles enter from off-frame with a 400 ms ease-out, tilt in 300 ms, and leave by the same path reversed; never two bottles on screen at once.
- Colour layers are stated per ingredient (clear, red, amber) and blend only during the stir; the blend uses a vertical gradient that collapses to a flat fill.
- Camera is locked on the glass with a 5% push-in at the stir; no cuts, every scene change is a label swap or an object entering.
- Typography: ingredient name in a heavy sans at the top, quantity in a mono numeral beside the tick; labels fade in 200 ms and out 150 ms, never overlapping.
- Banned: photographic bottles, sparkle particles, lens flares, any ingredient without its on-screen quantity, and pours that overshoot the fill line.

## Facts stated by the source (rewritten in our words)
- The requested length is 30 seconds and the format is an explainer-style motion graphic.
- The animation must run from an empty glass through to the finished cocktail.
- Ingredients and their quantities should appear on screen as they are added.
- The creator left the implementation open between JavaScript and HTML, whichever renders best.

## Assumptions
The 1:1:1 proportions, 30 ml measures, rocks glass, stir and orange twist come from the standard Negroni recipe rather than the source; colours and timings per pour are proposed.

## Keywords
cocktail recipe, liquid fill animation, pour physics, measurement callout, explainer, ingredient steps, bar spoon stir, وصفة كوكتيل, فيلم شرح, سكب السوائل, مقادير, رسوم توضيحية, مربع
