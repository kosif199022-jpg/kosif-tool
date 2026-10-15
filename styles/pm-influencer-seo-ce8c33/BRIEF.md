# ريل استعراضي لمنصة fal في 15 ثانية — fal motion design showreel

> شريط استعراضي كثيف في 15 ثانية بأسلوب السيرة الذاتية للمصمم، يمزج الطباعة الحركية برسوم السرعة وأصولًا مولَّدة عبر fal API.
>
> A dense 15-second showreel in portfolio style that blends kinetic type with speed charts and assets generated live through the fal API.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/influencer-seo-ce8c33
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: Remotion, React, WebGL

## الفكرة
الموضوع منصة استدلال للوسائط التوليدية تقدَّم عبر شريط استعراضي يُفترض أنه يعرض مهارة المصمم نفسه بقدر ما يعرض المنتج. الهدف هو إبهار المشاهد في 15 ثانية بثلاث رسائل: تنوّع المخرجات، والسرعة الفائقة، وسهولة الاستدعاء من الكود. تتميّز لغة الحركة بأن الأصول البصرية ليست جاهزة بل تُولَّد فعلًا عبر fal API أثناء البناء، وبطباعة حركية تضرب الكلمة على النبضة، وسباق أعمدة للزمن بالمللي ثانية يتجاوز حدود الإطار، ونبضة ضوء تسافر على خط من مقتطف كود إلى عقدة النموذج.

## Concept
The subject is a generative-media inference platform, pitched through a showreel that is meant to display the designer's own skill as much as the product. The goal is to impress in 15 seconds with three messages: range of outputs, extreme speed, and easy calls from code. The motion language is distinctive because the visuals are not stock but actually generated through the fal API during the build, paired with kinetic type that hits a word per beat, a latency bar race that overshoots the frame edge, and a light pulse travelling along a line from a code snippet to a model node.

## المشاهد المقترحة
- 0-2 ث: سواد. يُكتب اسم العلامة خلال 200 مللي ثانية ثم يتناثر إلى 400 جسيم يعود تجمّعها خلال 600 مللي ثانية في شبكة 6×4 من صور مولَّدة.
- 2-6 ث: طباعة حركية: أربع كلمات قدرة تنقضّ كلمة على كل نبضة من مقياس 1.4 إلى 1.0، وتكشف كل منها صورة مصغّرة مولَّدة خلفها؛ وتدفع الكلمة التالية سابقتها خارج الإطار.
- 6-10 ث: رسم السرعة: سباق أعمدة أفقي لزمن الاستدلال بين أربعة منافسين؛ ينطلق عمود العلامة متجاوزًا الحافة اليمنى بينما تزحف البقية، ويتناقص عدّاد المللي ثانية.
- 10-13 ث: لحظة الـ API: يُكتب طلب من ثلاثة أسطر في لوحة كود، وتسافر نبضة ضوء على خط طوله 1200 بكسل إلى عقدة النموذج، وتتفتّح الصورة الناتجة من العقدة خلال 400 مللي ثانية.
- 13-15 ث: الختام: تتوسّع شبكة صور الافتتاح لتملأ الإطار ثم تقطع إلى لون العلامة مع الشعار وسطر بُني بواسطة.

## Proposed scenes
- 0-2s: Black. The brand name is typed in 200ms, then shatters into 400 particles that reassemble over 600ms into a 6x4 grid of generated images.
- 2-6s: Kinetic type: four capability words slam in one per beat at 1.4 to 1.0 scale, each revealing a generated thumbnail behind it; the previous word is shoved off-frame by the next.
- 6-10s: Speed chart: a horizontal bar race of inference latency across four competitors; the brand bar shoots past the right edge while others crawl, and the millisecond readout counts down.
- 10-13s: API moment: a three-line request types in a code panel, a light pulse travels along a 1200px line to a model node, and the resulting image blooms from the node in 400ms.
- 13-15s: Lockup: the image grid from the opening tiles outward to fill the frame, then cuts to the brand colour with the logo and a 'built with' credit.

## قواعد الحركة
- تُولَّد كل صورة ومصغّرة عبر fal API وقت البناء ببذور ثابتة وتُخزَّن مؤقتًا؛ ويجب ألا يحوي التصيير النهائي أي صورة مؤقتة.
- تقع ضربات الطباعة الحركية على نبضات شبكة بسرعة 140 BPM؛ تدخل كل كلمة بمنحنى cubic-bezier(0.16, 1, 0.3, 1) خلال 220 مللي ثانية وتدفعها الكلمة التالية خلال 160 مللي ثانية.
- يعمل تناثر الجسيمات وتجمّعها على طبقة GPU بنسخ متماثلة (400-800 جسيم) بتأخير عشوائي لكل جسيم حتى 150 مللي ثانية؛ وجسيمات DOM على المعالج ممنوعة.
- تتسابق أعمدة الرسم بمنحنى ease-in-expo خلال 1200 مللي ثانية؛ يُسمح لعمود العلامة بتجاوز الإطار حتى 20% من العرض؛ وتبقى أعمدة المنافسين دون 60%.
- تتحرك نبضة الـ API بسرعة ثابتة 2400 بكسل في الثانية على مسار SVG عبر stroke-dashoffset مع توهّج 40 بكسل؛ وتتدرّج صورة النتيجة من 0.6 إلى 1.0 بتجاوز 5%.
- الكاميرا ثابتة باستثناء دفعة اقتراب واحدة بمقياس 1.10 عند لحظة تجاوز العمود، 200 مللي ثانية دخولًا و500 مللي ثانية خروجًا.
- اللون: قاعدة شبه سوداء، ولون تمييز واحد للنصوص والعمود الفائز، وتُعرض الصور المولَّدة دون مرشّحات بكامل تشبّعها؛ لا تدرّجات على النص.
- ممنوع: لقطات تتجاوز 2.5 ثانية، ولقطات مخزون، ونص lorem في لوحة الكود، وأي إحصاء لا يُذكر مع وحدته.

## Motion rules
- Generate every image and thumbnail through the fal API at build time with fixed seeds and cache them; the final render must contain zero placeholder art.
- Kinetic type hits land on beats of a 140 BPM grid; each word enters with cubic-bezier(0.16, 1, 0.3, 1) over 220ms and is pushed out by the next in 160ms.
- Particle shatter and reassembly run on a GPU instanced layer (400-800 particles) with per-particle random delay up to 150ms; CPU DOM particles are banned.
- Chart bars race with ease-in-expo over 1200ms; the brand bar is allowed to exceed the frame by up to 20% of width; competitor bars stay within 60%.
- The API pulse moves at a constant 2400px per second along an SVG path using stroke-dashoffset, with a 40px glow; the result image scales from 0.6 to 1.0 with a 5% overshoot.
- Camera is static except one 1.10 push-in on the chart overshoot moment, 200ms in and 500ms out.
- Colour: near-black base, one brand accent for type and the winning bar, generated images shown unfiltered at full saturation; no gradients on text.
- Banned: shots longer than 2.5s, stock footage, lorem text in the code panel, and any statistic that is not labelled with its unit.

## Facts stated by the source (rewritten in our words)
- Fixed length of 15 seconds.
- It is made for fal and framed as a showreel that proves the designer's ability, in the spirit of a portfolio piece.
- The creator explicitly asks that the fal API be used in producing it.
- Tagged under charts and kinetic type.

## Assumptions
The source names the platform, the duration and the API requirement but no scenes; the particle opener, the latency bar race, the code-to-node pulse and the 140 BPM grid are the director's proposals. Competitor latency figures must come from real benchmarks before publishing.

## Keywords
showreel, generative media, fal api, kinetic typography, bar race, latency chart, particle text, portfolio reel, شريط استعراضي, وسائط توليدية, طباعة حركية, سباق أعمدة, جسيمات, واجهة برمجية
