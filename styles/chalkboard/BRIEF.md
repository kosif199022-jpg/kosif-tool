# سبورة طباشير خضراء تشرح درسًا — سبورة طباشير

> سبورة طباشير خضراء داكنة بإطار خشبي: قطعة طباشير ملونة تتحرك فتكتب العنوان العربي بخط يدوي وترسم المثلث والمربعات بالأبيض والوردي والأزرق والأصفر، مربعات صغيرة تنتقل لتملأ مربعًا آخر كإثبات، ثم تُكتب المعادلة والأرقام وعلامة صح وخلاصة، والكاميرا تتحرك بين أجزاء اللوح.
>
> A dark green chalkboard in a wooden frame: a moving stick of coloured chalk writes an Arabic handwritten title and draws a triangle and gridded squares in white, pink, blue and yellow, small unit squares travel to fill another square as visual proof, then the equation, numbers, a tick and a summary line are written while the camera pans around the board.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/chalkboard
- التصنيفات / Categories: hand-drawn
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 26 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
درس حقيقي كأنه في فصل دراسي، والطباشير هو المعلم: كل ما يظهر تكتبه قطعة طباشير مرئية بلونها. الإثبات بصري وليس كلاميًا: المربعات الصغيرة تتحرك وتُعدّ أمام الطالب. الكاميرا تقترب من الجزء الذي يُشرح ثم تبتعد لتجمع الدرس كله في النهاية.

## Concept
A real lesson as if in a classroom, and the chalk is the teacher: everything that appears is written by a visible chalk stick of that colour. The proof is visual, not verbal: small unit squares move and are counted in front of the learner. The camera moves in on the part being explained, then pulls back to gather the whole lesson at the end.

## المشاهد المقترحة
- 0-1.5 ث: سبورة خضراء فارغة بإطار خشبي بني وقطع طباشير على الحافة؛ وقطعة طباشير صفراء تنزلق للداخل.
- 1.5-4 ث: الطباشير يكتب العنوان العربي بخط يدوي من اليمين لليسار ثم يضع تحته خطًا منحنيًا قليلًا.
- 4-7 ث: طباشير أبيض يرسم مثلثًا قائمًا ضلعًا بضلع؛ وحروف صغيرة تسمي أضلاعه وتظهر علامة الزاوية القائمة.
- 7-12 ث: طباشير وردي يرسم مربعًا مقسمًا على أحد الضلعين مع عدده؛ وأزرق يرسم مربعًا أكبر على الضلع الآخر مع عدده؛ وأصفر يرسم مربعًا مائلًا مقسمًا على الوتر.
- 12-16 ث: مربعات الوحدة ترتفع من المربعين الوردي والأزرق وتنزلق لتملأ المربع المائل بينما يصعد عدّاده إلى المجموع.
- 16-22 ث: الكاميرا تتحرك؛ الأبيض يكتب المعادلة بالأسس، والأصفر يكتب صورتها الرقمية، وعلامة صح خضراء تُرسم، والوردي يكتب القاعدة بالكلمات.
- 22-26 ث: الكاميرا تبتعد لتؤطر السبورة كلها: العنوان والرسم والمعادلات معًا؛ والطباشير يعود إلى الحافة.

## Proposed scenes
- 0-1.5s: Empty green board in a brown wooden frame with chalk pieces resting on the ledge; a yellow chalk stick slides in.
- 1.5-4s: The chalk writes the Arabic title in handwritten script right to left, then underlines it with a slightly curved stroke.
- 4-7s: White chalk draws a right triangle edge by edge; small letters label its sides and a right-angle mark appears.
- 7-12s: Pink chalk draws a gridded square on one leg with its count; blue chalk draws a larger gridded square on the other leg with its count; yellow chalk draws a tilted grid square on the hypotenuse.
- 12-16s: Unit squares lift off the pink and blue squares, glide and fill the tilted square while its counter climbs to the total.
- 16-22s: The camera pans; white chalk writes the equation with superscripts, yellow writes the numeric version, a green tick is drawn, pink writes the rule in words.
- 22-26s: The camera pulls back to frame the whole board: title, diagram and equations together; the chalk returns to the ledge.

## قواعد الحركة
- قطعة طباشير ظاهرة (مستطيل قصير مستدير بلونها) تقود رأس الخط دائمًا؛ تدخل من خارج الكادر وتتبع المسار وتميل قليلًا مع الاتجاه.
- خطوط الطباشير: رسم بإزاحة الخط مع خامة خشنة محببة (قناع ضوضاء أو مرشح اضطراب)، سمك 5-8 بكسل وتفاوت خفيف في الشفافية؛ وذرات غبار صغيرة عند أطراف الخطوط.
- الكتابة العربية اليدوية: تُرسم الكلمة كاملة مشكّلة بخط عربي يدوي وتُكشف بقناع يتبع رأس الطباشير من اليمين لليسار؛ ولا تقسيم للحروف.
- ترميز الألوان دلالي وثابت: الأبيض للبنية، والوردي والأزرق للجزأين، والأصفر للنتيجة والعنوان، والأخضر للتحقق.
- حركة الإثبات: مربعات الوحدة ترتفع (تكبير 1.05 وظل صغير)، تنزلق 500-800 مللي ثانية على أقواس مُسهّلة، وتستقر في مكانها بينما يزيد العداد مع كل مربع.
- الكاميرا: تحريك وتقريب هادئ 800-1200 مللي ثانية بين مناطق السبورة، وينتهي بابتعاد يُظهر السبورة كاملة؛ وعلى السبورة آثار مسح خافتة.
- اللوحة: سبورة #2f5a4a إلى #3b6b58 مع تعتيم الأطراف، خشب الإطار #6b3a1f، طباشير أبيض #f1f1e8، وردي #f4a6b8، أزرق #9fd3ec، أصفر #f2df7a، أخضر #9fe0a0.
- الفرق عن الوايتبورد والبلوتر: الوايتبورد قلم أسود على أبيض مع يد؛ والبلوتر قلم تقني دقيق على داكن أو ورق؛ أما الطباشير فألوان محببة على أخضر مع قطعة طباشير ظاهرة وإطار فصل دراسي.

## Motion rules
- A visible chalk stick (a short rounded rectangle in its colour) always leads the stroke tip; it enters from off-frame, follows the path, and tilts slightly with direction.
- Chalk strokes: stroke-dashoffset draw with a rough, grainy texture (noise mask or turbulence filter), width 5-8 px, slight opacity variation; a little dust specks at stroke ends.
- Arabic handwriting: render the whole shaped word in a handwritten Arabic face and reveal it with a mask that follows the chalk tip right to left; never split letters.
- Colour coding is semantic and fixed: white for structure, pink and blue for the two parts, yellow for the result and title, green for the check.
- Proof motion: unit squares lift (scale 1.05, small shadow), glide 500-800 ms on eased arcs, and drop into place while a counter increments per square.
- Camera: gentle pans and zooms 800-1200 ms between board regions, ending on a full-board pull-back; board texture shows faint eraser smudges.
- Palette: board #2f5a4a to #3b6b58 vignette, frame wood #6b3a1f, chalk white #f1f1e8, pink #f4a6b8, blue #9fd3ec, yellow #f2df7a, green #9fe0a0.
- Difference from whiteboard and plotter: whiteboard is black marker on white with a hand; plotter is a precise technical pen on dark or paper; chalkboard is coloured grainy chalk on green with a visible chalk stick and classroom framing.

## Facts stated by the source (rewritten in our words)
- The reference lesson explains the Pythagorean theorem with squares on the sides of a right triangle.

## Assumptions
Observed from 24 frames sampled across the 26 s 16:9 reference (fetched from the motion-starter-kit repository): chalk-led title, triangle, coloured gridded squares, unit squares moving into the hypotenuse square, equation, tick and full-board pull-back. Hex values are estimated. An audio stream exists but was not analysed. The chalk texture method is inferred.

## Keywords
chalkboard, chalk, blackboard, math lesson, visual proof, education, handwriting, سبورة طباشير, طباشير, درس رياضيات, إثبات بصري, تعليم, شرح, نظرية فيثاغورس
