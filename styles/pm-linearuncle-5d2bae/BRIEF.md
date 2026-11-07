# شرح رياضي هادئ لمفهوم المشتقة على خلفية كحلية بأسلوب مانيم — Derivative concept explainer

> درس رياضيات أفقي طويل (نحو 7 دقائق و37 ثانية) على خلفية كحلية داكنة بأسلوب مانيم: سيارة صغيرة وعداد سرعة، ثم منحنى s=t² تُرسم عليه قاطعة برتقالية تضيق حتى تصير مماساً أصفر، وجدول قيم يقترب من 2، ثم صيغة التعريف بإطارات ملونة، ودالة المشتقة بجانب الأصلية، وعدسة مكبرة تُظهر استقامة المنحنى، وملخص وأسئلة. العناوين صفراء أعلى اليسار والترجمة بالصينية أسفل الشاشة.
>
> A 7.5-minute Manim-style maths lesson on dark navy: a car and speedometer, an s=t² curve where an orange secant shrinks into a yellow tangent beside a table converging on 2, the colour-boxed limit definition, the derivative plotted beside the original, a magnifier that straightens the curve, and a recap; yellow titles top-left, subtitles at the bottom.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/linearuncle-5d2bae
- التصنيفات / Categories: diagrams, charts
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 457 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: SVG, Remotion, React

## الفكرة
الهدف بناء معنى المشتقة من الحدس قبل الرموز: لغز سرعة السيارة في لحظة (صفر على صفر) يقود إلى السرعة المتوسطة، ثم تقصير الفترة حتى تظهر السرعة اللحظية، ثم ترجمة ذلك إلى التعريف الرسمي ومثال محسوب، ثم قراءة المنحنيات بالميل، ثم نظرة «تحت المجهر» على النعومة. لكل لون دور ثابت، والشاشة تبقى نظيفة بمساحات سوداء واسعة وتعليق متزامن بالترجمة.

## Concept
The goal is to build the meaning of the derivative from intuition before symbols: the puzzle of a car's speed at an instant (zero over zero) leads to average speed, then shrinking the interval until the instantaneous speed emerges, then the formal definition and a worked example, then reading curves by their slope, then a 'under the microscope' look at smoothness. Each colour has a fixed role, and the screen stays clean with wide dark space and narration-synced subtitles.

## المشاهد المقترحة
- 0-35 ث: الخطّاف: سيارة كرتونية تسير على طريق وعداد سرعة عند 60؛ تظهر صيغة السرعة وتنهار حالة «اللحظة» إلى سؤال أحمر: 0 ÷ 0 = ؟
- 35-95 ث: الخطوة الأولى، السرعة المتوسطة: السيارة على مسار مرقّم، ثم منحنى s=t² يُرسم على محورين؛ نقطتان A وB بينهما مثلث قائم متقطع وتسميات Δs وΔt وقاطعة برتقالية، والحساب يُكتب يميناً.
- 95-150 ث: الخطوة الثانية، من المتوسط إلى اللحظي: Δt تصغر تدريجياً والقاطعة تدور نحو المنحنى وجدول Δt مقابل السرعة المتوسطة يمتلئ، ثم يحل محلها مماس أصفر ميله 2 وسهم يشير إلى أن القيم تقترب من 2.
- 150-230 ث: التعريف: صيغة النهاية تُكتب، ثم إطارات ملونة وتسميات تشرح البسط والمقام والنهاية؛ ومثال محسوب يفك (x+h)² خطوة خطوة ويختصر h لينتهي بإطار (x²)'=2x مع علامة صح خضراء تربطه بالسيارة.
- 230-300 ث: دالة المشتقة: قطع مكافئ يساراً وخط مستقيم ينمو يميناً بينما ينزلق مماس على القطع ويُرسم ميله نقطة نقطة؛ وعند x=0 يصبح المماس أفقياً.
- 300-340 ث: قراءة المنحنيات: موجة تشبه الدالة التكعيبية بمماس متحرك وقراءة حية للميل وتسميات صعود وهبوط؛ القمم والقيعان موسومة f'=0 مع قائمة قصيرة لاستخدامات التحسين في الواقع.
- 340-400 ث: تحت العدسة: عدسة دائرية تكبّر ×100 على منحنى حتى يبدو مستقيماً، ثم على |x| حيث تبقى الزاوية حادة بميلين −1 و+1 بالأحمر والأخضر.
- 400-457 ث: ملخص الدقيقة الواحدة في سطرين مرقمين، ثم بطاقة «فكّر» بثلاثة أسئلة تظهر واحداً تلو الآخر ثم تتلاشى.

## Proposed scenes
- 0-35s: Hook: a cartoon car drives along a road with a speedometer at 60; the speed formula appears and the 'instant' case collapses to a red 0 ÷ 0 = ?.
- 35-95s: Step 1, average speed: the car on a numbered track, then the s=t² curve drawn on axes; two points A and B get a dashed right triangle, Δs and Δt labels and an orange secant, with the arithmetic written at right.
- 95-150s: Step 2, from average to instant: Δt shrinks frame by frame, the secant rotates towards the curve and a table of Δt vs average speed fills in, then a yellow tangent with slope 2 replaces it and an arrow notes the values approach 2.
- 150-230s: The definition: the limit formula writes on, then coloured boxes and labels annotate the numerator, denominator and limit; a worked example expands (x+h)² step by step, cancels h and lands on a boxed (x²)'=2x with a green check tying back to the car.
- 230-300s: Derivative function: a parabola left and a growing straight line right as a tangent slides along the parabola and its slope is plotted point by point; at x=0 the tangent goes flat.
- 300-340s: Reading curves: a cubic-like wave with a moving tangent, live slope readout and up/down labels; peaks and valleys tagged f'=0 and a short list of real-world optimisation uses.
- 340-400s: Under the magnifier: a circular lens zooms ×100 on a curve until it looks straight, then on |x| where a corner stays sharp with slopes −1 and +1 in red and green.
- 400-457s: One-minute recap in two numbered lines, then a 'think about it' card with three questions that fade in one by one and out.

## قواعد الحركة
- الخلفية كحلية مسطحة #0f1524 بلا ملمس؛ المحاور والنصوص بلون أبيض مكسور #e6e8ee.
- أدوار الألوان: المنحنيات سماوي #5cc6e8، القاطعة والمتوسطات برتقالي #f08a3c، المماس وعناوين الأقسام أصفر #f2d264، الفروق والتأكيد أخضر #8cc97a، الأخطاء والسالب أحمر #e0605a.
- كل شيء يُرسم بحركات رسم وكتابة على طريقة مانيم: الخطوط تُتتبع في 0.6–1.2 ثانية، والنص يُكتب من بدايته لنهايته، والمعادلات تتحول حداً بحد.
- عنوان القسم ثابت أعلى اليسار بالأصفر؛ سطر الترجمة أسفل المنتصف داخل كبسولة داكنة ويتبدل مع كل جملة تعليق.
- تغير القيم (Δt وقراءات الميل) يحدث حياً بينما الهندسة تتحرك باستمرار، لا بالقطع.
- إيقاع محاضرة: وقفات طويلة 10–20 ثانية على رسم مكتمل بينما يستمر التعليق؛ تغيير المشهد بتلاشي كل العناصر (نحو نصف ثانية) ثم بناء جديد.
- إبراز المصطلحات المهمة بمستطيلات ملونة رفيعة تُرسم حولها لا بتعبئة لونية.

## Motion rules
- Background #0f1524 flat navy with no texture; axes and text in off-white #e6e8ee.
- Colour roles: curves cyan #5cc6e8, secant/averages orange #f08a3c, tangent and section titles yellow #f2d264, differences/checks green #8cc97a, errors/negatives red #e0605a.
- Everything is drawn with Manim-like Create/Write animations: strokes trace in 0.6–1.2 s, text writes on left to right, equations transform term by term.
- Section title fixed top-left in yellow; subtitle line bottom-centre in a dark pill, swapped per narration sentence.
- Value changes (Δt, slope readouts) update live while geometry moves continuously, never by cuts.
- Lecture pace: long holds of 10–20 s on finished diagrams while narration continues; scene changes by fade-out of all elements (~0.5 s) then fresh build.
- Highlight important terms with thin coloured rectangles drawn around them rather than colour fills.

## Facts stated by the source (rewritten in our words)
- The title says it explains the concept of the derivative.
- The source lists Manim as the technology used.

## Assumptions
Observed from 24 frames sampled every ~19 s across about 457 s: the car hook, average-to-instant steps, definition and worked example, derivative plots, slope reading, magnifier and recap. On-screen language is Chinese; a KOSIF version would swap to Arabic subtitles. The audio track (quiet, mean about −23 dB) was not analysed, so narration is assumed from the subtitles. Scene boundaries are estimates between samples.

## Keywords
manim style, math explainer, derivative, calculus, tangent line, secant, limit, dark navy, subtitles, مشتقة, تفاضل, شرح رياضيات, مماس, درس تعليمي
