# سبورة بيضاء — أقلام ماركر ملونة ترسم شرحاً بسيطاً يتراكم — سبورة بيضاء

> سبورة بيضاء نظيفة تملأ الإطار، يرسم عليها قلم ماركر ظاهر يتغير لونه مع كل عنصر: عنوان عربي أسود بخط عريض مع نجمتين وخط أحمر تحته، ثم أمواج زرقاء، وشمس صفراء مبتسمة، وأسهم بخار حمراء، وسحابة ومطر، وجبل أسود بعشب أخضر، وسهم جريان أخضر، مع تسميات عربية ملونة، حتى يكتمل رسم دورة كاملة بأسهم منقطة وقطرة تتحرك فيها.
>
> A clean whiteboard filling the frame, drawn by a visible marker that changes colour per element: a bold black Arabic title with two stars and a red underline, then blue waves, a smiling yellow sun, red rising vapour arrows, a cloud with rain, a black mountain with green grass and a green runoff arrow, with coloured Arabic labels, until a full cycle closes with dotted arrows and a moving droplet.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/whiteboard
- التصنيفات / Categories: hand-drawn
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 23 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
شرح علمي بسيط يُبنى أمام المشاهد عنصراً بعد عنصر، فيفهم السبب والنتيجة بترتيب الرسم نفسه. القلم الظاهر وتغيّر لونه يجعلان المشاهد يشعر أن معلماً يرسم الآن، وكل لون له معنى (أزرق للماء، أحمر للحرارة، أخضر للأرض). لا قطعات؛ السبورة تتراكم حتى تصبح الصورة الكاملة هي الملخص.

## Concept
A simple science explanation built in front of the viewer element by element, so cause and effect are understood from the drawing order itself. The visible, colour-changing marker makes it feel like a teacher drawing right now, and each colour means something (blue for water, red for heat, green for land). No cuts; the board accumulates until the complete picture is the summary.

## المشاهد المقترحة
- 0-3 ث: سبورة فارغة؛ يدخل قلم أسود ويكتب العنوان العربي من اليمين لليسار، ثم يتحول إلى البرتقالي لإضافة نجمتين صغيرتين وإلى الأحمر لخط تحته.
- 3-6 ث: يصعد العنوان ويصغر إلى الأعلى؛ قلم أزرق يرسم خطوط أمواج متراصة أسفل اليسار مع تسمية «البحر».
- 6-9 ث: قلم برتقالي ثم أصفر يرسم شمساً دائرية بأشعة؛ وتظهر ابتسامة.
- 9-12 ث: قلم أحمر يرسم ثلاثة أسهم متموجة صاعدة فوق البحر مع تسمية «تبخر».
- 12-15 ث: قلم أزرق يرسم حدود سحابة تمتلئ بالأزرق الفاتح، وتسقط شرطات مطر؛ مع تسميتي «تكاثف» و«هطول».
- 15-19 ث: قلم أسود يرسم جبلاً على اليمين، ويمتلئ أسفله بالأخضر؛ وسهم أخضر منحنٍ يعود إلى البحر مع تسمية «جريان».
- 19-23 ث: ثبات واسع على الدورة كاملة؛ تظهر أسهم ربط منقطة وقطرة زرقاء تدور في الحلقة.

## Proposed scenes
- 0-3s: Empty board; a black marker enters and writes the Arabic title right to left, then switches to orange to add two small stars and to red for an underline.
- 3-6s: The title slides up and shrinks to the top; a blue marker draws stacked wave lines at the bottom-left, labelled 'البحر'.
- 6-9s: An orange then yellow marker draws a circle sun with rays; a smile pops in.
- 9-12s: A red marker draws three wavy rising arrows above the sea, labelled 'تبخر'.
- 12-15s: A blue marker draws a cloud outline, it fills light blue, rain dashes fall; labels 'تكاثف' and 'هطول'.
- 15-19s: A black marker draws a mountain on the right, green fills its base; a green curved arrow runs back to the sea, labelled 'جريان'.
- 19-23s: Wide hold of the full cycle; dotted connector arrows appear and a blue droplet travels around the loop.

## قواعد الحركة
- السبورة #fbfaf7 بأثر مسح رمادي خفيف وتعتيم بارد ناعم نحو الأطراف (#d3dce0)؛ بلا إطار ولا جدار ظاهر؛ والكاميرا ثابتة إلا حركة واحدة عند صعود العنوان.
- ألوان الماركر بمعانٍ: أسود #1e1e1e (العنوان والبنية)، أزرق #2f6fd6 (الماء)، أحمر #d8342c (الحرارة والخط السفلي)، أصفر برتقالي #f4b223 (الشمس والنجوم)، أخضر #3a9a4a (الأرض والجريان).
- قلم ماركر واقعي يركب رأس الخط مائلاً نحو 30 درجة؛ ويتبدل إلى اللون التالي بين العناصر (خروج ودخول في 0.2 ث)، ولا يرسم أبداً بلون غير لون الخط.
- الخطوط تُرسم باهتزاز خفيف بسرعة اليد؛ الحدود أولاً ثم تعبئة مسطحة تمسح في اتجاه الرسم (0.3-0.5 ث).
- العنوان والتسميات العربية بخط عريض مستدير بروح الماركر (مثل لاله‌زار أو خط ماركر يدوي)، تُكتب من اليمين لليسار كلمة كلمة والحروف المتصلة سليمة؛ والتسميات بلون عنصرها.
- كل عنصر يأخذ نحو 2-4 ث؛ وترتيب الرسم يتبع تسلسل السبب والنتيجة في الشرح؛ وحركة دائرية أخيرة (القطرة) تثبت معنى الدورة.
- الفرق عن السبورة السينمائية (حركة كاميرا وعمق وإضاءة) والسبورة الطباشيرية (طباشير على لوح داكن) والشخبطة (رسوم فضفاضة بلا قلم ظاهر): رسم ماركر صفّي مشرق ونظيف بكاميرا ثابتة؛ وفي 9:16 نرص العناصر رأسياً ونبقي العنوان في الأعلى.

## Motion rules
- Board #fbfaf7 with a faint grey smudge and soft cool vignette toward the edges (#d3dce0); no frame or wall visible; static camera except one move when the title shifts up.
- Marker inks with meaning: black #1e1e1e (title, structure), blue #2f6fd6 (water), red #d8342c (heat, underline), yellow-orange #f4b223 (sun, stars), green #3a9a4a (land, runoff).
- A realistic marker sprite rides the stroke tip, tilted about 30 degrees; it swaps to the next colour between elements (0.2 s exit and enter), never draws with the wrong colour.
- Strokes draw on with slight wobble at hand speed; outlines first, then flat fills that wipe in along the stroke direction (0.3-0.5 s).
- Arabic title and labels in a bold rounded marker-style face (e.g. Lalezar or a hand-marker font), written right to left word by word with joined letters intact; labels are coloured to match their element.
- Each element takes about 2-4 s; the drawing order follows the cause-and-effect sequence of the explanation; a final looping motion (droplet) proves the cycle.
- Different from whiteboard-cinematic (camera moves, depth and lighting), chalkboard (chalk on dark board) and doodle (loose sketches without a visible marker): bright, clean, static-camera classroom marker drawing; for 9:16, stack elements vertically and keep the title at the top.

## Facts stated by the source (rewritten in our words)
- The reference in the starter kit is a 1280x720, 30 fps, 23 s silent clip.
- Its subject is the water cycle, drawn with labels for sea, evaporation, condensation, precipitation and runoff.

## Assumptions
Observed from a 24-frame grid of the starter-kit reference video (23 s, 16:9, no audio track): the visible colour-changing marker, the title with stars and red underline, the drawing order of sea, sun, vapour, cloud and rain, mountain and runoff, the labels and the closing droplet loop. Assumed: exact timings between samples, stroke speeds and the fonts; hex values are approximate.

## Keywords
whiteboard, marker, whiteboard animation, explainer, science, water cycle, draw-on, سبورة بيضاء, ماركر, رسم على السبورة, شرح علمي, دورة الماء, رسم يدوي, تعليمي
