# سبورة مرسومة باليد تشرح كسر تناظر النسخ في نموذج SK — Replica symmetry breaking whiteboard

> شرح بأسلوب السبورة البيضاء، تُرسم فيه الخطوط أمام المشاهد مع تعليق صوتي، لفكرة كسر تناظر النسخ في نموذج شيرينغتون-كيركباتريك للزجاج المغزلي.
>
> A narrated whiteboard explainer where strokes are drawn live, walking from a frustrated spin glass to Parisi's hierarchical overlap matrix.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/tak3sh8-be5012
- التصنيفات / Categories: diagrams
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 60 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: SVG, Remotion, Web Audio

## الفكرة
الموضوع فيزيائي متقدّم: نموذج شيرينغتون-كيركباتريك (SK) للزجاج المغزلي، حيث تتفاعل كل المغازل مع بعضها بأوزان عشوائية، وحلّه عبر خدعة النسخ (replica trick) ثم اكتشاف أن الحل المتناظر بين النسخ غير مستقر، فيُكسر التناظر هرميًا كما اقترح باريزي. الهدف أن يخرج مشاهد غير متخصص بحدس بصري: المشهد الطاقي له وديان كثيرة، والمصفوفة التي تقيس تشابه النسخ تتحوّل من قيمة واحدة إلى كتل متداخلة ثم إلى شجرة. اللغة الحركية هي سبورة بيضاء يرسمها قلم ماركر خطًا خطًا بتزامن مع كلمات التعليق الصوتي، بلا مؤثرات لامعة، مع لون واحد فقط للتأكيد على لحظة الكسر.

## Concept
The subject is advanced physics: the Sherrington-Kirkpatrick spin glass, where every spin couples to every other with random weights, the replica trick used to average over disorder, and the discovery that the replica-symmetric solution is unstable, leading to Parisi's hierarchical symmetry breaking. The goal is to leave a non-specialist with a visual intuition: an energy landscape with many valleys, and an overlap matrix that goes from one uniform value to nested blocks and finally to a tree. The motion language is a whiteboard drawn stroke by stroke by a marker in sync with narration, with no glossy effects and a single accent colour reserved for the moment symmetry breaks.

## المشاهد المقترحة
- 0-8ث: يُكتب العنوان بخط اليد أعلى اليسار؛ تظهر حلقة من 8-10 مغازل كأسهم صغيرة، وتربط خطوط الماركر كل زوج منها، بعضها موسوم بزائد وبعضها بناقص لبيان الأوزان العشوائية.
- 8-18ث: يُرسم منحنى مشهد طاقي خشن بوديان كثيرة متفاوتة العمق؛ كرة صغيرة تجرّب واديين وتعلق، لتجسيد الإحباط (frustration) وتعدد الحالات القريبة من الأرضية.
- 18-30ث: تُكتب خدعة النسخ على إيقاع المعلّق: n نسخة من النظام كمستطيلات متراصّة، ويُكتب التداخل بين نسختين كرمز q بمؤشرين.
- 30-42ث: تُرسم مصفوفة تداخل n×n؛ يملأ الحل المتناظر كل خلية خارج القطر بالقيمة نفسها، ثم يظهر تحتها خط مرتجف بلون التأكيد يحمل كلمة غير مستقر.
- 42-55ث: تُعاد المصفوفة بكتل متداخلة على طول القطر (مستوى أول ثم مستوى ثانٍ داخله)، وتُرسم إلى جانبها شجرة متفرّعة تبيّن هرمية الحالات.
- 55-60ث: تُسحب السبورة إلى لقطة واسعة؛ تُحاط ثلاث خلاصات من سطر واحد بدوائر، ويُسطّر العنوان مع اختتام التعليق الصوتي.

## Proposed scenes
- 0-8s: Title is handwritten top-left; a ring of 8-10 spins appears as small arrows, and marker lines connect every pair, some labelled plus and some minus to show random couplings.
- 8-18s: A rough energy-landscape curve is drawn with many valleys of different depths; a small ball tries two valleys and gets stuck, visualising frustration and many near-ground states.
- 18-30s: The replica trick is written out in the narrator's rhythm: n copies of the system sketched as stacked rectangles, and the overlap between two copies written as q with two indices.
- 30-42s: An n-by-n overlap matrix is drawn; the replica-symmetric guess fills every off-diagonal cell with the same value, then a wobbling 'unstable' underline appears in the accent colour.
- 42-55s: The matrix is redrawn with nested blocks along the diagonal (one level, then a second level inside), and a branching tree is drawn beside it to show the hierarchy of states.
- 55-60s: The board is panned back to a wide view; three one-line takeaways are circled and the title is underlined as the narration closes.

## قواعد الحركة
- يُكشف كل خط عبر SVG stroke-dashoffset بسرعة قلم ثابتة تقارب 500-700 بكسل في الثانية بمنحنى linear؛ لا يظهر أي منحنى مكتملًا دفعة واحدة.
- يبدأ كل خط عند الطابع الزمني للكلمة التي يوضّحها؛ عند توفّر توقيت الكلمات يُعاد ضبط الرسم عليها ولا يسبق الصوت بأكثر من 150 مللي ثانية.
- تتحرك الكاميرا فقط بين مناطق السبورة: تحريك أفقي أو تقريب خلال 800 مللي ثانية بمنحنى easeInOutQuad، بحد أقصى خمس حركات في الفيلم كله، وما عدا ذلك ثابتة.
- الطباعة: خط يحاكي الكتابة اليدوية للتسميات وخط monospace نظيف للمعادلات؛ تظهر الحروف بالرسم لا بالتلاشي.
- الألوان: سبورة بيضاء، ماركر شبه أسود، ولون تأكيد دافئ واحد (مقترح أحمر) يُستعمل فقط لخط عدم الاستقرار ولكتل التناظر المكسور.
- المسح يتم بمسحة 400 مللي ثانية تتبع شكل الممحاة لا بتلاشي الشفافية؛ تُمسح المنطقة قبل إعادة الرسم فيها.
- ممنوع: التلاشي المتقاطع بأسلوب الشرائح، والظلال، والتدرّجات اللونية، والأيقونات المرتدّة، وأي حركة ليست رسمًا أو مسحًا أو تحريك كاميرا.

## Motion rules
- Every line is revealed with SVG stroke-dashoffset at a constant pen speed of roughly 500-700 px per second with linear easing; curves never pop in fully formed.
- Each stroke starts on the timestamp of the word it illustrates; when word timings are provided, the drawing is retimed to them and never leads the voice by more than 150 ms.
- Camera moves only between board regions: a pan or a zoom of 800 ms with easeInOutQuad, at most five moves in the whole film, otherwise static.
- Typography is a handwritten-style font for labels and a clean monospace for the formulas; letters appear by stroke, not by fade.
- Colour: white board, near-black marker, one warm accent (proposed red) used only for the unstable underline and the broken-symmetry blocks.
- Erasing uses a 400 ms wipe that follows an eraser shape, not an opacity fade; a region is erased before it is redrawn.
- Banned: slide-style crossfades, drop shadows, gradients, bouncing icons, and any motion that is not either drawing, erasing or panning.

## Facts stated by the source (rewritten in our words)
- The creator asked for a quick, hand-drawn whiteboard-style animation explaining how replica symmetry gets broken in the Sherrington-Kirkpatrick spin-glass model.
- A second prompt asked for the result to be built as an MP4 file with narration.
- No duration, stack or scene structure is stated; the page lists diagrams as its only tag.

## Assumptions
Only the whiteboard look, the physics topic and the narrated MP4 output are stated; the 60-second length, the six-beat structure, the accent colour and all timings are my proposed direction.

## Keywords
زجاج مغزلي, فيزياء إحصائية, شرح علمي, رسم يدوي, تعليق صوتي, مصفوفة التداخل, باريزي, spin glass, parisi, overlap matrix, whiteboard, hand drawn, narration, physics explainer
