# العين المنوّمة: ريل سايكدلي عشرون ثانية — Psychedelic hypnotic eye showreel

> ريل مدته 20 ثانية يدور حول عين مركزية: حلقات تنبض، تكبير لا نهائي داخل البؤبؤ، تناظر كاليدوسكوبي، ونص يدور حولها ورسم شعاعي ينمو في القزحية.
>
> A 20-second reel built around one central eye: pulsing rings, an endless zoom into the pupil, kaleidoscope symmetry, text orbiting it and a radial chart growing inside the iris.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/monokern-ade5b6
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 20 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: HTML Canvas, WebGL, Remotion

## الفكرة
الموضوع ريل شخصي بطابع سايكدلي منوّم، يلتقط الانتباه ويمسكه بالتكرار والتناظر. الهدف أن يثبت المصمم سيطرته على الإيقاع البصري: الصورة لا تتوقف عن الحركة لكنها لا تتعب العين. اللغة الحركية تعتمد على عين واحدة كبؤرة ثابتة تُبنى حولها كل الحركة: تكبير مستمر بسرعة ثابتة نحو البؤبؤ يخلق إحساس النفق، تناظر سداسي يحوّل أي شكل إلى زخرفة، ودوران ألوان بطيء بدلاً من القطع؛ كل البيانات والنصوص تُرسم بشكل شعاعي حول المركز لا في صفوف.

## Concept
The subject is a personal reel with a psychedelic, hypnotic character that grabs attention and holds it through repetition and symmetry. The goal is to prove command of visual rhythm: the image never stops moving yet never tires the eye. The motion language uses one eye as a fixed focal point around which everything is built: a constant-speed zoom toward the pupil creates a tunnel feeling, six-fold symmetry turns any shape into ornament, and slow hue rotation replaces cuts; all data and text are laid out radially around the centre rather than in rows.

## المشاهد المقترحة
- 0-3 ث: نقطة على الأسود تتسع إلى قزحية؛ حلقات متحدة المركز تنبض للخارج مع كل ضربة بإيقاع 120 BPM، ويرسم الجفنان نفسيهما كقوسين.
- 3-8 ث: تدفع الكاميرا بثبات داخل البؤبؤ؛ نفق من حلقات ومثلثات وأقواس متداخلة يمر بينما تدور الألوان ببطء.
- 8-12 ث: ينطوي النفق إلى كاليدوسكوب سداسي؛ حلقة من كلمات قصيرة تدور حول المركز على مسار دائري، عكس اتجاه دوران النمط.
- 12-16 ث: داخل القزحية ينمو رسم أعمدة شعاعي قطعة قطعة، وتدور قيمه كتسميات صغيرة؛ ينقبض البؤبؤ عند اكتمال الرسم.
- 16-19 ث: يضيق لولب من الحافة نحو الداخل، يفقد النمط تشبعه، وترمش العين مرتين.
- 19-20 ث: أسود مع اسم المصمم وحلقة رفيعة واحدة تكمل دورة ثم تتوقف.

## Proposed scenes
- 0-3s: A dot on black dilates into an iris; concentric rings pulse outward on every beat at 120 BPM and the eyelids draw themselves as two arcs.
- 3-8s: The camera pushes steadily into the pupil; a tunnel of nested rings, triangles and arcs scrolls past while hues cycle slowly.
- 8-12s: The tunnel folds into a six-fold kaleidoscope; a ring of short words rotates around the centre on a circular path, counter-rotating against the pattern.
- 12-16s: Inside the iris a radial bar chart grows segment by segment, with values orbiting as small labels; the pupil contracts as the chart completes.
- 16-19s: A spiral tightens from the edge inward, the pattern desaturates and the eye blinks twice.
- 19-20s: Black with the designer's name and a single thin ring that completes a rotation and stops.

## قواعد الحركة
- التكبير للداخل يعمل بمعدل ثابت (المقياس يتضاعف كل 2.5 ثانية) بلا easing طوال مدته؛ البداية والنهاية فقط تستخدمان ease-in-out بمدة 600 ms.
- النبضات جيبية بتردد 2 Hz وسعة 6 بالمئة من المقياس؛ لا يومض شيء على الشاشة أسرع من 3 Hz للبقاء تحت عتبات الحساسية الضوئية.
- تدور درجة اللون 360 درجة كاملة خلال 10 ثوان على نمط الخلفية؛ النص وخطوط الرسم تحافظ على تباين إضاءة لا يقل عن 4.5:1 مع ما خلفها.
- التناظر سداسي أو ثماني فقط، مبني من قطاع مصدر واحد يُعكس في الـshader؛ يمكن للقطاع نفسه أن يدور 10 درجات في الثانية.
- النص يجلس على مسارات دائرية ويدور 15 درجة في الثانية؛ الدوران المعاكس للنمط إلزامي لتبقى الكلمات مقروءة.
- الرسم الشعاعي ينمو مع عقارب الساعة، قطعة كل 300 ms بمنحنى cubic-bezier(0.33, 1, 0.68, 1)؛ تظهر التسميات بعد قطعتها بـ150 ms.
- الكاميرا دفعة واحدة للداخل بلا حركات جانبية؛ مركز العين لا يغادر مركز الإطار تماماً.
- ممنوع: glitch عشوائي، قطع وميضي، أكثر من دورانين متعاكسين معاً، ظلال ساقطة، وأي نص غير موزع شعاعياً.

## Motion rules
- The inward zoom runs at a constant rate (scale doubles every 2.5 s) with no easing while it lasts; only its start and end use a 600 ms ease-in-out.
- Pulses are sinusoidal at 2 Hz with an amplitude of 6 percent scale; nothing on screen flashes faster than 3 Hz, to stay below photosensitivity thresholds.
- Hue rotates a full 360 degrees over 10 s on the background pattern; text and chart strokes keep luminance contrast of at least 4.5:1 against whatever is behind them.
- Symmetry is six- or eight-fold only, built from one source wedge mirrored in the shader; the wedge itself may rotate at 10 degrees per second.
- Text sits on circular paths and rotates at 15 degrees per second; counter-rotation against the pattern is mandatory so the words stay readable.
- The radial chart grows clockwise, one segment per 300 ms with cubic-bezier(0.33, 1, 0.68, 1); labels fade in 150 ms after their segment.
- The camera is a single push-in with no lateral moves; the eye centre never leaves the exact frame centre.
- Banned: random noise glitch, strobe cuts, more than two opposing rotations at once, drop shadows, and any text not laid out radially.

## Facts stated by the source (rewritten in our words)
- The creator asked for a 20-second dynamic motion graphics piece with a psychedelic and hypnotic feel, framed as a showreel.
- Site tags: charts and kinetic type; the site title mentions an eye motif.
- No stack, colours or structure are described.

## Assumptions
Stated: 20 seconds, psychedelic and hypnotic mood, showreel framing, chart and kinetic-type tags, the eye as motif from the title. Assumed: the constant-rate zoom, kaleidoscope symmetry, BPM, hue-cycle timing, the radial chart and the photosensitivity limits.

## Keywords
psychedelic, hypnotic, kaleidoscope, كاليدوسكوب, infinite zoom, تكبير لا نهائي, radial chart, رسم شعاعي, circular text, نص دائري, hue rotation, تناظر, eye motif, showreel, دوران ألوان
