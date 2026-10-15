# إعلان عمودي لتطبيق PicTwin للصور بالذكاء الاصطناعي — PicTwin AI app ad

> إعلان عمودي قصير يُظهر كيف تتحوّل صورة شخصية واحدة إلى نسخة توأم مولّدة بالذكاء الاصطناعي داخل واجهة هاتف حيّة بكشف قبل/بعد.
>
> A vertical 15 s app ad where one selfie becomes an AI-generated twin inside a live phone UI, told as a split-screen before/after reveal.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/l3d1c-0e35a3
- التصنيفات / Categories: product-ui
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 15 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع تطبيق ويب يستقبل صورة شخصية ويُخرج نسخة توأم منها بأساليب مختلفة، والهدف إقناع المشاهد في ثوانٍ بأن النتيجة فورية ومبهرة. اللغة الحركية مبنية على واجهة هاتف حقيقية تتفاعل كأن إصبعًا خفيًا يضغطها: رفع، تحميل، حلقة تقدّم، ثم كشف جانبي يفصل الأصل عن التوأم. كل عنصر واجهة يتحرك بزنبرك خفيف واحد لا يتكرر، ولا توجد لقطات ثابتة أبدًا.

## Concept
The subject is a web app that takes one selfie and returns an AI twin in several looks; the goal is to convince a scrolling viewer within seconds that the result is instant and striking. The motion language is a real phone UI driven by an invisible finger: upload, progress ring, then a vertical split reveal separating original from twin. Every UI element moves with a single light spring and nothing ever sits still.

## المشاهد المقترحة
- 0-2ث: إطار أسود؛ يصعد نموذج الهاتف من الحافة السفلية بزنبرك (تجاوز 1.08 خلال 700 مللي ثانية) بينما تسقط صورة شخصية مصغّرة في خانة الرفع وتنضغط 2 بكسل عند الهبوط.
- 2-5ث: تتمدد خانة الرفع إلى كامل العرض (400 مللي ثانية، easeOutQuint)؛ تدور حلقة التقدّم من 0 إلى 360 درجة خلال 1200 مللي ثانية مع تبدّل عبارات حالة عربية قصيرة بتلاشٍ متقاطع 150 مللي ثانية.
- 5-9ث: كشف منقسم: خط مسح عمودي ينتقل من اليسار إلى اليمين خلال 900 مللي ثانية ليظهر التوأم بجوار الأصل؛ ثبات 600 مللي ثانية ثم تتبدّل ثلاثة أنماط كل 500 مللي ثانية مع نبضة تكبير 3 بالمئة.
- 9-12ث: ثلاث كبسولات مزايا (السرعة، الخصوصية، الأنماط) تنزلق من اليمين بتأخير 120 مللي ثانية بينها؛ أيقونة كل كبسولة تُرسم بخط SVG خلال 350 مللي ثانية.
- 12-15ث: يستقر الشعار في المنتصف، ويُكتب عنوان الموقع حرفًا حرفًا بمعدل 40 مللي ثانية للحرف، وينبض زر الدعوة مرة واحدة (1 إلى 1.04 إلى 1 خلال 500 مللي ثانية).

## Proposed scenes
- 0-2s: Black frame; a phone mock-up rises from the bottom edge with a spring (overshoot 1.08, 700 ms) while a selfie thumbnail drops into the upload slot and lands with a 2 px squash.
- 2-5s: The upload tile expands to full width (400 ms, easeOutQuint); a progress ring sweeps 0 to 360 degrees over 1200 ms while short Arabic status labels swap with 150 ms crossfades.
- 5-9s: Split reveal: a vertical wipe line travels left to right over 900 ms uncovering the AI twin beside the original; hold 600 ms, then three style presets swap every 500 ms with a 3 percent scale pop.
- 9-12s: Three benefit pills (speed, privacy, styles) slide in from the right with 120 ms stagger; each pill icon draws on with an SVG stroke over 350 ms.
- 12-15s: Logo lockup settles at centre, the site URL types on letter by letter at 40 ms per character, and a CTA button pulses once (scale 1 to 1.04 to 1, 500 ms).

## قواعد الحركة
- كل مداخل الواجهة تستخدم زنبركًا واحدًا (صلابة 180، تخميد 18) أو cubic-bezier(0.22, 1, 0.36, 1) بين 350 و700 مللي ثانية؛ الخروج أسرع من الدخول بنسبة 40 بالمئة.
- يبقى الهاتف داخل منطقة آمنة 1080×1920 بهامش 120 بكسل أعلى وأسفل حتى لا تغطي واجهة المنصة محتوى الشاشة.
- الكاميرا: ثابتة، مع دفعة اقتراب واحدة بنسبة 6 بالمئة أثناء الكشف المنقسم (5-9ث) ولا حركة كاميرا أخرى.
- الانتقالات تشبه سلوك الجهاز: مسح وتمدد داخل الهاتف؛ لا تلاشي متقاطع بين المشاهد الكاملة.
- الطباعة: عناوين الواجهة العربية بعائلة sans واحدة ووزنين فقط؛ كلمات العنوان تهبط بتأخير 60 مللي ثانية ولا تتجاوز ثلاثة أسطر.
- اللون: خلفية شبه سوداء، لون تمييز واحد للتقدّم وزر الدعوة، والصور تبقى بدون صبغة؛ لا يظهر لون التمييز على أكثر من عنصرين في آن واحد.
- ممنوع: التوهّج المصطنع، القصاصات الملوّنة، مؤثرات الصوت الجاهزة، النص فوق منطقة الوجه في الصورة، وأي ضبابية على نتيجة التوأم.

## Motion rules
- All UI entrances use one spring (stiffness 180, damping 18) or cubic-bezier(0.22, 1, 0.36, 1) between 350 and 700 ms; exits are 40 percent faster than entrances.
- The phone stays within a 1080x1920 safe area with 120 px top and bottom margins so platform UI never covers the screen content.
- Camera: locked, with a single 6 percent push-in on the split reveal (5-9 s) and no other camera movement.
- Transitions are hardware-like: wipes and expands inside the phone; no cross-dissolves between full scenes.
- Typography: Arabic UI labels in one sans family, two weights only; headline words land with a 60 ms stagger and never exceed three lines.
- Colour: a near-black background, one accent for progress and CTA, photos remain untinted; the accent must not appear on more than two elements at once.
- Banned: fake glow, confetti, stock whoosh cues, text over the face region of the selfie, and any blur on the twin result.

## Facts stated by the source (rewritten in our words)
- The creator asked for a motion-design advertisement for their own website; nothing else is specified.
- The listing tags the piece as product UI and lists a vertical 1080x1920 frame.

## Assumptions
The product function (an AI twin generated from one photo), the 15 s length and the split-reveal structure are assumptions drawn from the app name; only the ad purpose and vertical format are given.

## Keywords
إعلان تطبيق, صورة شخصية, توأم بالذكاء الاصطناعي, واجهة هاتف, قبل وبعد, app ad, selfie, ai avatar, phone mockup, split reveal, progress ring, vertical ad, reels
