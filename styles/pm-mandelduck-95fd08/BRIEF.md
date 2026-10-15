# ليلة النجوم: نزهة ثلاثية الأبعاد لاصطياد القطط — Starry Night cat-spotting game

> مشهد ثلاثي الأبعاد قابل للمشي داخل قرية لوحة ليلة النجوم بلمسة فرشاة متحركة، حيث يبحث اللاعب عن قطط مختبئة بين البيوت وشجرة السرو.
>
> A walkable 3D scene inside the village of Starry Night rendered in moving brush strokes, where the player hunts for cats hidden among the houses and the cypress.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/mandelduck-95fd08
- التصنيفات / Categories: characters
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 30 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: Three.js, WebGL, Web Audio

## الفكرة
الموضوع لعبة استكشاف من منظور الشخص الأول داخل لوحة ليلة النجوم لفان غوخ (عمل في الملك العام) وقريتها، مهمتها الوحيدة رصد قطط مخبأة. الهدف التواصلي هو متعة الاكتشاف الهادئ وإحساس المشي داخل لوحة لا داخل محاكاة واقعية. اللغة الحركية تقوم على أن كل سطح يُرسم بضربات فرشاة حية تتنفس، والسماء دوامات تدور ببطء لا تتوقف، والقطط شخصيات بسيطة الشكل تكشف نفسها بحركة ذيل أو وميض عينين قبل أن تظهر كاملة.

## Concept
The subject is a first-person exploration game set inside Van Gogh's Starry Night (a public-domain painting) and its village, whose only objective is to spot hidden cats. The goal is calm discovery and the feeling of walking inside a painting rather than a realistic simulation. The motion language rests on every surface being drawn with living, breathing brush strokes, a sky of slowly turning swirls that never stop, and cats as simple-shaped characters that give themselves away with a tail flick or an eye glint before fully appearing.

## المشاهد المقترحة
- 0-3 ث: ترتفع الكاميرا من حقل قمح معتم؛ تبدأ دوامات السماء بالدوران وتنبض هالة الهلال حتى تظهر.
- 3-10 ث: يمشي اللاعب في الزقاق نحو القرية بسرعة 1.4 م/ث؛ تضيء النوافذ واحدة تلو الأخرى، تتمايل شجرة السرو، وتتلألأ ضربات كل جدار مع تغير زاوية النظر.
- 10-20 ث: حلقة الرصد: ذيل يتحرك خلف مدخنة، يلتف مؤشر ناعم عليه، تنبثق القطة بحجمها الكامل مع رنة، ويتقدم العداد من 2 إلى 3 من 7.
- 20-27 ث: صعود إلى برج الكنيسة؛ يشتد حقل الدوامات في الأعلى، تنمو للنجوم ذيول من ضربات الفرشاة، وتظهر ثلاث قطط أخرى على الأسطح من هذه الإطلالة.
- 27-30 ث: الحصيلة النهائية 7 من 7؛ ينبسط المشهد كله عائداً إلى اللوحة المعلقة في إطار على جدار، كأن اللاعب خرج منها.

## Proposed scenes
- 0-3s: The camera rises from a dark wheat field; the sky's swirls begin rotating and the crescent moon's halo pulses into view.
- 3-10s: The player walks the lane into the village at 1.4 m/s; windows glow on one by one, the cypress sways, every wall's strokes shimmer as the view angle changes.
- 10-20s: Spotting loop: a tail flicks behind a chimney, a reticle softens onto it, the cat pops to full size with a chime and the counter ticks from 2 to 3 of 7.
- 20-27s: Climb to the church tower; the swirl field above intensifies, stars grow stroke-tails, and three more cats are visible on rooftops from this vantage.
- 27-30s: Final tally 7 of 7; the whole scene flattens back into the painted canvas framed on a wall, as if the player stepped out of it.

## قواعد الحركة
- التصيير بـshader قائم على ضربات الفرشاة: ثلاثة أحجام (كبير للسماء، متوسط للجدران، صغير للتفاصيل)، كل ضربة تهتز 1-2 px بتردد 6 Hz لتبدو الأسطح مرسومة باليد وحية.
- السماء مدفوعة بـcurl noise مع دوران عام نحو 0.15 rad/s؛ لا تتوقف أبداً حتى في القوائم أو بطاقة النهاية.
- سرعة المشي 1.4 م/ث مع اهتزاز رأس 2 سم بتردد 1.8 Hz؛ مجال رؤية الكاميرا ثابت عند 70 درجة؛ لا قطع، وكل تغيير مكان يتم مشياً أو تسلقاً.
- كشف القطة: مقياس من 0.8 إلى 1.0 بتجاوز back-out بقيمة cubic-bezier(0.34, 1.56, 0.64, 1) خلال 350 ms، مع بريق من ثلاث ضربات ورنة قصيرة عبر Web Audio.
- القطط تلمّح قبل أن تظهر: حركة ذيل كل 2-4 ثوان أو وميض عين بومضة 120 ms، ولا تُرى إلا ضمن 20 متراً.
- اللون يبقى داخل عائلة اللوحة: أزرق عميق، أصفر باهت، لمسة خضراء ومغرة دافئة؛ لا أبيض خالص ولا رمادي محايد.
- الواجهة مقتصرة على عدّاد داخل إطار مرسوم؛ يظهر 1.5 ثانية عند كل اكتشاف ويختفي بقية الوقت.
- ممنوع: خامات واقعية، حواف مستقيمة بلا اهتزاز فرشاة، تأثيرات عدسة، قطع مفاجئ، وأي عنصر واجهة أثقل من العدّاد.

## Motion rules
- Rendering is a stroke-based shader: three stroke sizes (large for sky, medium for walls, small for details), each stroke jittering 1-2 px at 6 Hz so surfaces feel hand-painted and alive.
- The sky is driven by curl noise with a global rotation of about 0.15 rad/s; it never pauses, even in menus or on the end card.
- Walk speed 1.4 m/s with a head bob of 2 cm at 1.8 Hz; camera field of view fixed at 70 degrees; no cuts, every change of place is walked or climbed.
- Cat reveal: scale from 0.8 to 1.0 with a back-out overshoot (cubic-bezier(0.34, 1.56, 0.64, 1)) over 350 ms, plus a 3-stroke sparkle and a short Web Audio chime.
- Cats hint before they reveal: a tail flick every 2-4 s or an eye glint on a 120 ms flash, visible only within 20 m.
- Colour stays inside the painting's family: deep blues, pale yellows, a touch of green and warm ochre; no pure white and no neutral grey.
- UI is limited to a counter in a painted frame; it fades in for 1.5 s on each find and otherwise stays hidden.
- Banned: photoreal textures, straight edges without stroke jitter, lens effects, jump cuts, and any UI element heavier than the counter.

## Facts stated by the source (rewritten in our words)
- The creator asked for a 3D game in which the player walks around and spots cats inside a Van Gogh painting.
- The starting point is Starry Night together with its town.
- The site tags it under characters; no duration, stack or colours are stated.

## Assumptions
Stated: 3D walkable game, cat spotting, Starry Night and its village as the first level. Assumed: the 30-second demo capture structure, the seven-cat count, stroke shader parameters, walk and camera values, and the restricted painterly palette.

## Keywords
3d game, van gogh, painterly shader, brush stroke, ضربات فرشاة, لعبة استكشاف, first person, hidden object, قطط, شخصيات, curl noise, swirl sky, سماء دوامات, impasto
