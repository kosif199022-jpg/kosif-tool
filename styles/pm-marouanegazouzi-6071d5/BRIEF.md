# ريل Crux: كل شيء يدور حول النقطة الحاسمة — Crux motion design showreel

> ريل 15 ثانية لاستوديو Crux تدور فيه الحروف والرسوم البيانية حول نقطة مركزية واحدة، فيتحول الشعار إلى محور الحركة.
>
> A 15-second reel for Crux where letters and charts all pivot around a single centre point, turning the studio mark into the axis of motion.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/marouanegazouzi-6071d5
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع ريل تعريفي يحمل اسم Crux، أي النقطة الجوهرية، والهدف أن يترجم هذا الاسم إلى قاعدة حركية واحدة: لا شيء يتحرك إلا حول المركز. الحروف تدور في أرباع الإطار، ورسم الأعمدة يصبح شعاعيًا، والكلمات المهارية تدور في حلقات بسرعات زاوية مختلفة. ما يميز اللغة الحركية هو صرامتها: محور دوران واحد، ولوحة من لونين تنقلب مرة واحدة فقط، وقطع حاد واحد يفصل النصف الأول عن الثاني، ما يمنح الريل طابع الهوية أكثر من طابع الاستعراض.

## Concept
The subject is a résumé reel named Crux, the decisive point, and the goal is to turn that name into a single motion rule: nothing moves except around the centre. Letters rotate into the four quadrants, the bar chart becomes radial, and skill words orbit on rings at different angular speeds. The distinctive trait is strictness: one pivot, a two-colour palette that inverts exactly once, and a single hard cut dividing the first half from the second, which gives the reel the feel of an identity system rather than a showcase.

## المشاهد المقترحة
- 0-2 ث: نقطة تصويب واحدة تنبض في مركز الإطار تمامًا؛ خطان رفيعان يمتدان منها إلى الحواف فيكوّنان صليبًا خلال 600 ms.
- 2-5 ث: الحروف C وR وU وX تصل كلٌّ إلى ربع من الإطار، ويدور كل حرف 90° حول المركز ليستقر، بتفاوت 120 ms.
- 5-8 ث: الصليب يصبح محاور رسم بياني: رسم أعمدة شعاعي يكتسح حول المركز، وكل عمود يمتد إلى قيمته بـ ease-out مع تسمية رقمية.
- 8-11 ث: تايبوغرافي حركي: كلمات مهارات قصيرة تدور حول المركز على ثلاث حلقات بسرعات زاوية مختلفة؛ تضيق الحلقات أثناء الدوران حتى تتراص الكلمات في عمود.
- 11-13 ث: كل شيء ينهار إلى النقطة؛ النقطة تتمدد إلى إطار كامل بلون التمييز مع قطع حاد 250 ms إلى اللوحة المعكوسة.
- 13-15 ث: شعار CRUX يثبت في المركز بينما تُرسم حلقة رفيعة حوله؛ الاسم ومعلومات التواصل تظهر أسفله.

## Proposed scenes
- 0-2s: A single crosshair dot pulses at the exact centre; two thin lines extend from it to the frame edges, forming a cross in 600 ms.
- 2-5s: The letters C, R, U and X arrive one per quadrant, each rotating 90° into place around the centre with a 120 ms stagger.
- 5-8s: The cross becomes chart axes: a radial bar chart sweeps around the centre, each bar extending to its value with an ease-out and a numeric label.
- 8-11s: Kinetic type: short skill words orbit the centre on three rings at different angular speeds; the rings tighten as they spin until the words stack into a column.
- 11-13s: Everything collapses into the dot; the dot expands into a full-bleed accent frame with a 250 ms hard cut to the inverse palette.
- 13-15s: The CRUX wordmark sits still at the centre while a thin ring draws around it; name and contact appear below.

## قواعد الحركة
- كل transform-origin هو مركز الإطار بالضبط (960, 540)؛ لا يدور أي عنصر أو يتكبر حول صندوقه الخاص.
- الدورانات بـ cubic-bezier(0.76, 0, 0.24, 1) خلال 700 ms؛ تفاوت الحروف 120 ms ويستقر الحرف الأخير قبل بدء الرسم البياني.
- الأعمدة الشعاعية تمتد خلال 500 ms لكل عمود بتفاوت 60 ms، دائمًا من المركز إلى الخارج، وتظهر تسمية القيمة بعد 100 ms من توقف العمود.
- السرعات الزاوية للحلقات 12 و-18 و24 درجة في الثانية؛ تضيق الحلقات من نصف قطر 420 px إلى 0 خلال 1400 ms بـ ease-in.
- لا حركة كاميرا؛ الانتقال الوحيد قطع حاد 250 ms إلى اللوحة المعكوسة عند لحظة الانهيار.
- اللوحة: لونان فقط (داكن وتمييز) يتبادلان الأدوار مرة واحدة؛ لا تدرجات ولا لون ثالث ولا ظلال.
- الطباعة: sans هندسي عريض بتباعد حروف +0.1 em؛ حروف CRUX بحجم 220 px، وكلمات المهارات 40 px، وسطر التواصل 28 px.
- ممنوع: الحركات القطرية خارج المركز، والظلال الساقطة، والضبابية، وأي عنصر يدخل من خارج الإطار بدل الخروج من المركز.

## Motion rules
- Every transform-origin is the exact frame centre (960, 540); no element rotates or scales around its own box.
- Rotations use cubic-bezier(0.76, 0, 0.24, 1) over 700 ms; the letter stagger is 120 ms and the last letter settles before the chart begins.
- Radial bars extend over 500 ms each with a 60 ms stagger, always from the centre outward, with their value label appearing 100 ms after the bar stops.
- Ring angular speeds are 12, -18 and 24 degrees per second; rings tighten from radius 420 px to 0 over 1400 ms with ease-in.
- No camera movement; the only transition is one 250 ms hard cut to the inverted palette at the collapse point.
- Palette: exactly two colours (one dark, one accent) that swap roles once; no gradients, no third tone, no shadows.
- Typography: a wide geometric sans with +0.1 em letter-spacing; CRUX letters at 220 px, skill words at 40 px, contact line at 28 px.
- Banned: off-centre diagonal moves, drop shadows, blur, and any element that enters from outside the frame instead of from the centre.

## Facts stated by the source (rewritten in our words)
- A dynamic 15-second résumé reel is the stated brief.
- The catalogue titles it a Crux showreel and tags it charts plus kinetic type.
- No colours, scenes, stack or structure are described.

## Assumptions
Treating Crux as a studio name and building a centre-pivot system around it is a creative proposal; the actual meaning of Crux and any existing branding were not available.

## Keywords
showreel, centre pivot, radial bar chart, orbiting type, two-colour palette, hard cut, studio identity, kinetic type, ريل استوديو, دوران حول المركز, رسم شعاعي, هوية بصرية, طباعة حركية
