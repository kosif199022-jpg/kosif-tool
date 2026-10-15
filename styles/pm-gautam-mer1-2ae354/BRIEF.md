# ترويج تطبيق Matra للترجمة النصية بأسلوب Apple — Matra caption app promo

> فيديو عمودي مدته 30 ثانية بهدوء إعلانات Apple يقدّم تطبيق ترجمة نصية للفيديو: هاتف واحد عائم، نص كبير شحيح، وكلمات تظهر متزامنة مع الكلام.
>
> A 30 s vertical, Apple-calm product film for a caption app: one floating phone, sparse large type, and captions that land word by word in sync with speech.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/gautam-mer1-2ae354
- التصنيفات / Categories: product-ui
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 30 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
الموضوع تطبيق يولّد ترجمات نصية متزامنة للفيديو، والهدف أن يبدو المنتج فاخرًا وموثوقًا بأسلوب أفلام Apple: استوديو مظلم، جهاز واحد، ضوء يمسح الزجاج، وعبارات قصيرة تطفو بخط ضخم. اللغة الحركية بطيئة ومتعمّدة: حركة كاميرا واحدة في كل مشهد، ومنحنى easing واحد لكل الحركات الكبيرة، بينما تكون الترجمة النصية العنصر الوحيد السريع لأنها تتبع إيقاع الكلام. الدعم العربي من اليمين إلى اليسار جزء أصيل من العرض لا إضافة.

## Concept
The subject is an app that generates synced captions for video, and the goal is to make it feel premium and trustworthy in the manner of Apple product films: a dark studio, a single device, light sweeping across glass, and short phrases floating in huge type. The motion language is slow and deliberate, one camera move per scene and one easing curve for every large motion, while the captions are the only fast element because they follow the rhythm of speech. Right-to-left Arabic support is a native part of the demo, not an afterthought.

## المشاهد المقترحة
- 0-4ث: أسود؛ يبرز هاتف من الظلام بينما يمسح شعاع ضوء زجاجه خلال 1800 مللي ثانية؛ يظهر اسم التطبيق صغيرًا في الأسفل بتلاشٍ خلال 600 مللي ثانية.
- 4-10ث: على الشاشة مقطع صامت لمتحدث؛ موجة صوتية رفيعة في الأسفل؛ كلمات الترجمة تظهر واحدة واحدة تحت المتحدث، كل كلمة تهبط خلال 120 مللي ثانية بتكبير من 0.96 إلى 1 وفق حدود الكلمات.
- 10-16ث: تدوير أنماط الترجمة: ثلاثة أنماط (نظيف، مؤطّر، محدّد) تتبدل كل ثانيتين بتلاشٍ متقاطع 240 مللي ثانية، مع مثال عربي ومثال إنجليزي بالتناوب.
- 16-22ث: عبارات رئيسية تطفو بخط ضخم بجوار الجهاز، واحدة كل ثانيتين، تصعد 30 بكسل خلال 900 مللي ثانية، بينما تقترب الكاميرا 8 بالمئة على مدى المشهد.
- 22-27ث: مسار التصدير: تموّج لمسة، شريط تقدّم 1600 مللي ثانية، ولوحة مشاركة تنزلق لأعلى؛ يدور الجهاز 12 درجة حول محوره الرأسي ليلتقط الضوء.
- 27-30ث: يستقر الشعار النصي ودعوة بأسلوب متجر التطبيقات في المنتصف بتلاشٍ 400 مللي ثانية؛ كل ما عداهما يخفت إلى 20 بالمئة.

## Proposed scenes
- 0-4s: Black; a phone emerges from darkness as a light sweep crosses the glass over 1800 ms; the app name fades in small at the bottom at 600 ms.
- 4-10s: On screen a muted clip of a speaker; a thin waveform at the bottom; caption words appear one by one beneath the speaker, each landing in 120 ms with a 0.96 to 1 scale, timed to the word boundaries.
- 10-16s: Caption styles cycle: three presets (clean, boxed, outlined) swap every 2 s with a 240 ms crossfade, showing an Arabic example and an English example alternately.
- 16-22s: Headline statements float in huge type beside the device, one per 2 s, rising 30 px over 900 ms, while the camera pushes in 8 percent across the scene.
- 22-27s: Export flow: a tap ripple, a 1600 ms progress bar, a share sheet sliding up; the device rotates 12 degrees on its Y axis to catch the light.
- 27-30s: The wordmark and a store-style call to action settle at centre with a 400 ms fade; everything else dims to 20 percent.

## قواعد الحركة
- easing واحد لكل حركة كبيرة: cubic-bezier(0.16, 1, 0.3, 1) بين 900 و1400 مللي ثانية؛ لا يجوز لأي عنصر كبير أن يتحرك أسرع من 900 مللي ثانية.
- الترجمة النصية هي الاستثناء: كل كلمة تهبط خلال 120 مللي ثانية بتكبير من 0.96 إلى 1 وشفافية من 0 إلى 1 عند وقت بدايتها من words.json؛ لا تظهر كلمة مبكرًا أو تتأخر أكثر من 40 مللي ثانية.
- الكاميرا: حركة واحدة لكل مشهد (مسح، دفع، دوران)، بحد أقصى دفعة 8 بالمئة ودوران 12 درجة؛ لا يغادر الجهاز الثلث الأوسط من الإطار 720×1280.
- الانتقالات تلاشٍ متقاطع 400 مللي ثانية فقط؛ لا مسح ولا قطع ولا انتقالات بالاختراق.
- الطباعة: خط واحد بوزنين، العناوين بحد أدنى 96 بكسل في الإطار العمودي، العربية باتجاه RTL مع تشكيل حروف صحيح وبلا إمالة مصطنعة؛ الترجمة على الشاشة بحجم 48 بكسل وفجوة أمان 6 بكسل من حافة الهاتف.
- اللون: خلفية شبه سوداء، نص أبيض، ولون تمييز واحد يُستخدم فقط لكلمة الترجمة النشطة وشريط التقدّم؛ شعاع الضوء تدرّج أبيض بشفافية 25 بالمئة.
- ممنوع: الزنبركات المرتدّة، القصاصات الملوّنة، الرموز التعبيرية، أكثر من عنصر متحرك واحد خارج الترجمة في أي لحظة، وضربات موسيقية تنافس إيقاع الكلام.

## Motion rules
- One easing for every large move: cubic-bezier(0.16, 1, 0.3, 1) at 900 to 1400 ms; nothing large may move faster than 900 ms.
- Captions are the exception: each word lands in 120 ms with scale 0.96 to 1 and opacity 0 to 1 on its start time from words.json; no word may appear early or hang late by more than 40 ms.
- Camera: one move per scene (sweep, push, rotate), maximum 8 percent push and 12 degrees rotation; the device never leaves the central third of the 720x1280 frame.
- Transitions are 400 ms cross-dissolves only; no wipes, no cuts, no zoom-through transitions.
- Typography: one typeface in two weights, headlines at 96 px minimum in the vertical frame, Arabic set RTL with proper shaping, never faux-italic; captions on screen use a 48 px size with a 6 px safe gap from the phone's edge.
- Colour: near-black background, white type, and a single accent used only for the active caption word and the progress bar; the light sweep is a white gradient at 25 percent opacity.
- Banned: bounce springs, confetti, emoji, more than one moving element outside the captions at any moment, and music hits that compete with the spoken rhythm.

## Facts stated by the source (rewritten in our words)
- The creator wants a thirty-second video of their own app.
- The requested look is the Apple product-film style.
- The listing tags it as product UI and lists a 720x1280 vertical frame.

## Assumptions
That Matra is a video-caption app with Arabic support, plus every scene, timing and the words.json sync rule, are proposals; the source states only the 30 s length, the Apple-style direction and the app subject.

## Keywords
ترجمة نصية, تطبيق كابشن, أسلوب Apple, هاتف عائم, مزامنة كلمات, استوديو مظلم, caption app, word sync, device film, light sweep, minimal product video, rtl captions, export flow, vertical promo
