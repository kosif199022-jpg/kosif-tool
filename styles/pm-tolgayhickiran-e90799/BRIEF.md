# ريل مبادئ الموشن: الحركة تشرح نفسها — Motion design principles reel

> ريل 15 ثانية يعرض مبادئ التحريك كأمثلة حية، حيث تؤدي الكلمة والرسم البياني المبدأ الذي يسمّيانه.
>
> A 15-second résumé reel in which each animation principle is performed live by the very word and chart that name it.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/tolgayhickiran-e90799
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع ريل تعريفي للمصمم يُبنى على مبادئ التحريك الأساسية: التسهيل، والتهيئة، والتجاوز، والمتابعة، والتمثيل المسرحي. الهدف إثبات الحرفة في 15 ثانية دون كلام، فكل مبدأ تؤديه الكلمة التي تحمل اسمه والرسم البياني المجاور لها. ما يميز اللغة الحركية هنا أن منحنى الـ easing يُرسم على الشاشة في اللحظة نفسها التي يُطبَّق فيها، فيتحول الريل إلى درس مرئي وبطاقة مهارات في آن واحد.

## Concept
The subject is a résumé reel built on core animation principles: easing, anticipation, overshoot, follow-through and staging. The goal is to prove craft in 15 seconds without narration, so each principle is performed by the word that names it and by the chart beside it. What makes the motion language distinctive is that the easing curve is drawn on screen at the same moment it is applied, turning the reel into both a visual lesson and a skills card.

## المشاهد المقترحة
- 0-2 ث: إطار أسود؛ كلمة EASING تدخل على مسار خطي فتتعثر، ثم تعود بدخول cubic ease-out بينما يُرسم منحنى صغير في الزاوية.
- 2-5 ث: ANTICIPATION: الكلمة تنخفض 8% قبل أن تقفز خارج الإطار؛ ورسم أعمدة أسفلها يضغط أعمدته قبل أن ترتفع إلى طولها الكامل.
- 5-8 ث: OVERSHOOT: ثلاثة عدّادات إحصائية (مثل +120 و98% و4.9) تهبط بنابض، والأعمدة تتجاوز قيمتها 12% ثم تستقر، مع رسم منحنى النابض بجوارها.
- 8-11 ث: FOLLOW-THROUGH: رسم خطي يندفع إلى الإطار؛ طرفه يتخطى القيمة النهائية ثم يعود، ومعه تسمية تتأخر 80 ms.
- 11-13.5 ث: STAGING: كل شيء ينهار إلى كلمة واحدة MOTION في المنتصف بخط grotesk ثقيل، مع تظليل خفيف يركّز النظر.
- 13.5-15 ث: الاسم والدور ومعرّف التواصل تنزلق أسفلها، ومنحنى الرسم ينغلق ليصبح علامة شعار صغيرة.

## Proposed scenes
- 0-2s: Black frame; the word EASING slides in on a linear path, stutters, then re-enters on a cubic ease-out while a small curve graph draws itself in the corner.
- 2-5s: ANTICIPATION: the word crouches 8% downward before leaping up and out of frame; a bar chart below pre-compresses its bars before they shoot to full height.
- 5-8s: OVERSHOOT: three stat counters (e.g. 120+, 98%, 4.9) land with a spring, bars overshoot 12% then settle; the spring curve is drawn beside them.
- 8-11s: FOLLOW-THROUGH: a line chart whips in; its endpoint continues past the final value and drifts back, with a trailing label that lags by 80 ms.
- 11-13.5s: STAGING: everything collapses to one centred word MOTION set in a heavy grotesk, with a thin spotlight vignette pulling focus.
- 13.5-15s: Name, role and contact handle slide in beneath, and the curve graph closes into a tiny logo mark.

## قواعد الحركة
- التسهيل الأساسي للدخول cubic-bezier(0.22, 1, 0.36, 1)؛ والخروج cubic-bezier(0.64, 0, 0.78, 0) بمدة أقصر بنسبة 40% من الدخول.
- مبدأ واحد لكل مقطع؛ تظهر تسمية المبدأ 600 ms على الأقل قبل بدء أي عرض كي يقرأها المشاهد أولًا.
- النوابض بقيم stiffness 180 وdamping 14 وmass 1؛ ولا يتجاوز التجاوز 12% من مسافة الحركة.
- الرسوم البيانية تنمو من خط الصفر فقط؛ الأعمدة خلال 500 ms بتفاوت 60 ms، والخطوط تُرسم بـ stroke-dashoffset خلال 700 ms.
- الكاميرا إطار ثنائي الأبعاد ثابت بلا دوران ثلاثي الأبعاد؛ العمق يأتي من التكبير (حد أقصى 1.08) وظل بعمق 6 px يكبر مع الارتفاع.
- اللوحة: خلفية داكنة واحدة، ونص أبيض مائل للدفء، ولون تمييز واحد للمنحنى وتعبئة الرسوم؛ لا يتجاوز لون التمييز 20% من مساحة الإطار.
- الطباعة: grotesk ثقيل بحجم 180 px لأسماء المبادئ و36 px monospace للتسميات؛ تباعد الحروف يتحرك من +0.2 em إلى 0 عند الدخول خلال 400 ms.
- ممنوع: motion blur، والتوهجات العدسية، وانفجارات الجسيمات، وأي قطع دون خروج مرئي للعنصر السابق.

## Motion rules
- Primary easing is cubic-bezier(0.22, 1, 0.36, 1) for all entrances; exits use cubic-bezier(0.64, 0, 0.78, 0) and are 40% shorter than entrances.
- One principle per beat; the principle label appears for at least 600 ms before any demonstration starts so the viewer can read it first.
- Springs use stiffness 180, damping 14, mass 1; cap overshoot at 12% of the travel distance.
- Charts animate from a zero baseline only; bars grow over 500 ms with a 60 ms stagger, lines draw via stroke-dashoffset over 700 ms.
- Camera is a locked 2D frame; no 3D rotation. Depth comes from scale (max 1.08) and a 6 px drop-shadow that scales with elevation.
- Palette: one dark background, one off-white text, a single accent for the curve graph and chart fills; the accent never exceeds 20% of frame area.
- Typography: a heavy grotesk at 180 px for principle names, 36 px monospace for labels; letter-spacing animates from +0.2 em to 0 on entrance over 400 ms.
- Banned: motion blur, lens flares, particle bursts, and any cut without the previous element visibly exiting.

## Facts stated by the source (rewritten in our words)
- Requested as a fast-paced 15-second motion piece.
- Framed as a personal showreel meant to accompany a résumé.
- Tagged in the catalogue as charts and kinetic type; no stack or structure is specified.
- The creator asked for maximum effort with no further constraints.

## Assumptions
The principles-based structure, the curve-graph overlay and the palette are proposed directions; the source only asks for a 15-second résumé reel and states no scenes, colours or stack.

## Keywords
showreel, easing, anticipation, overshoot, follow-through, bar chart, kinetic typography, résumé reel, ريل تعريفي, مبادئ التحريك, منحنيات التسهيل, رسوم بيانية متحركة, تايبوغرافي حركي
