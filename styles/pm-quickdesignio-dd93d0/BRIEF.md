# ترويج علامة QuickDesign: السرعة كحجّة بصرية — QuickDesign brand promo

> ترويج أفقي مدته 15 ثانية لأداة تصميم سريعة، يبني الشعار من أشكال أولية ثم يبرهن على توفير الوقت بمخططات وعدّادات متحركة.
>
> A 15 s landscape brand promo for a fast design tool: the wordmark assembles from primitives, then animated charts and counters prove the time saved.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/quickdesignio-dd93d0
- التصنيفات / Categories: charts
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع علامة أداة تصميم تعد بالسرعة، والهدف مزدوج: إقناع المشاهد بقيمة الأداة وإظهار براعة حركية في الوقت نفسه. اللغة الحركية تجعل السرعة محسوسة بدل أن تُقال: أشكال أولية تلتقط مواضعها كالمغناطيس، لوحة تصميم تمتلئ تلقائيًا ببطاقات، ثم تتحول بيانات الوقت الموفّر إلى مخططات تنمو أمام العين. كل مشهد ينتهي بعنصر يصبح بذرة المشهد التالي كي لا يوجد انقطاع.

## Concept
The subject is the brand of a design tool that promises speed, and the goal is twofold: sell the tool and show off motion craft at once. The motion language makes speed felt rather than stated: primitive shapes snap into place like magnets, a design canvas auto-fills with cards, and the time-saved data becomes charts that grow on screen. Every scene ends with an element that seeds the next one so there is never a dead cut.

## المشاهد المقترحة
- 0-2ث: مستطيلات ودوائر ومثلثات تطير من حواف الإطار وتلتقط مواضعها داخل حروف الشعار النصي بزنبرك (تخميد 14)، كل شكل يصل بعد سابقه بـ50 مللي ثانية.
- 2-5ث: يتقلص الشعار إلى زاوية وتنفتح لوحة الأداة؛ مؤشر يسحب إطارًا، فيمتلئ تلقائيًا باثنتي عشرة بطاقة بتأخير 80 مللي ثانية بينها بينما تظهر خطوط الشبكة بشفافية 30 بالمئة.
- 5-9ث: قسم البرهان: مقارنة بعمودين (يدوي مقابل الأداة) تنمو من خط الأساس خلال 1000 مللي ثانية، مخطط خطي للإنتاج الأسبوعي يُرسم عبر stroke-dashoffset خلال 1200 مللي ثانية، وعدّاد يصل إلى الساعات الموفّرة.
- 9-12ث: مجموعة بطاقات قوالب تنقلب بمنظور CSS ثلاثي الأبعاد، كل انقلاب 300 مللي ثانية بتأخير 90 مللي ثانية، كاشفة تخطيطات منشور اجتماعي وشريحة وملصق.
- 12-15ث: تنطوي كل البطاقات إلى أشكال الشعار من المشهد الأول، يهبط الشعار النصي بكلمتين ويظهر عنوان الموقع بتلاشٍ خلال 400 مللي ثانية.

## Proposed scenes
- 0-2s: Rectangles, circles and triangles fly in from the frame edges and snap into the wordmark letterforms with a spring (damping 14), each shape arriving 50 ms after the previous one.
- 2-5s: The wordmark shrinks to a corner and a tool canvas unfolds; a cursor drags a frame, and an auto-layout fills it with twelve cards at 80 ms stagger while grid lines fade in at 30 percent.
- 5-9s: Proof section: a two-bar comparison (manual vs tool) grows from the baseline over 1000 ms, a line chart of weekly output draws on via stroke-dashoffset over 1200 ms, and a counter rolls to the hours saved.
- 9-12s: A deck of template cards flips in CSS 3D perspective, each flip 300 ms with 90 ms stagger, revealing social post, slide and poster layouts.
- 12-15s: All cards collapse into the wordmark shapes from scene one, the tagline lands in two words and the URL fades up at 400 ms.

## قواعد الحركة
- التقاط الأشكال يستخدم زنبركًا بصلابة 220 وتخميد 14 (تجاوز واحد مرئي)؛ تدرّجات الواجهة تستخدم cubic-bezier(0.16, 1, 0.3, 1) بين 400 و600 مللي ثانية.
- المخططات تبدأ دائمًا من الصفر في الإطار نفسه وتكتمل خلال 1200 مللي ثانية؛ العدّادات تستخدم easeOutExpo وتتوقف عند رقم مدوّر يطابق ارتفاع العمود.
- الكاميرا: انجراف بطيء مستمر بنسبة 5 بالمئة على كامل العمل مع دفعة 10 بالمئة في قسم البرهان؛ لا اهتزاز يدوي.
- الانتقالات تحوّلات: آخر عنصر في المشهد يتغير حجمه أو شكله ليصبح أول عنصر في المشهد التالي؛ القطع الحاد ممنوع.
- الطباعة: خط sans هندسي، كلمات العنوان تدخل بتأخير 60 مللي ثانية وصعود 20 بكسل، لا حرفًا حرفًا؛ النسخة العربية تحتفظ بالتوقيتات نفسها باتجاه RTL.
- اللون: خلفية لوحة فاتحة، لون علامة مشبع واحد على الأشكال والأعمدة، وواجهة رمادية محايدة؛ لون التمييز لا يغطي أكثر من 20 بالمئة من الإطار.
- ممنوع: انفجارات الجسيمات، وهج العدسة، الشعارات المرتدّة، والإحصاءات غير الموسومة بأنها توضيحية.

## Motion rules
- Shape snaps use a spring with stiffness 220 and damping 14 (visible single overshoot); UI tweens use cubic-bezier(0.16, 1, 0.3, 1) at 400 to 600 ms.
- Charts always start from zero on the same frame and finish within 1200 ms; counters use easeOutExpo and stop on a round number that matches the bar height.
- Camera: one continuous 5 percent slow drift across the whole piece plus a 10 percent push on the proof section; no handheld shake.
- Transitions are morphs: the last element of a scene scales or reshapes into the first element of the next; hard cuts are banned.
- Typography: a geometric sans, headline words enter with 60 ms stagger and 20 px rise, never letter-by-letter; Arabic version keeps the same timings with RTL direction.
- Colour: a light canvas background, one saturated brand accent on the shapes and bars, and neutral grey UI; the accent never covers more than 20 percent of the frame.
- Banned: particle bursts, lens flares, bouncing logos, and stats that are not labelled as illustrative.

## Facts stated by the source (rewritten in our words)
- The requested piece is a dynamic motion-graphics video of fifteen seconds.
- It must present the QuickDesign brand as impressive and simultaneously demonstrate the maker's motion-design skill.
- The listing tags it as charts and lists a 1920x1080 frame.

## Assumptions
That QuickDesign is a fast template-driven design tool, and every scene, timing and chart type, are proposals; the source fixes only the 15 s length and the dual promo-plus-showreel intent.

## Keywords
ترويج علامة, أداة تصميم, أشكال أولية, لوحة تصميم, مخطط مقارنة, قوالب, brand promo, design tool, shape snap, auto layout, bar chart, card flip, counter, wordmark build
