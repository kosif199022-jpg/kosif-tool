# كرة تهرب من اثنتي عشرة حلقة — Ball escaping twelve rings

> محاكاة فيزيائية عمودية: كرة ترتد داخل حلقات متحدة المركز وتفلت منها واحدة تلو الأخرى، مع عدّاد ونغمة تصعد عند كل هروب.
>
> A vertical physics loop: a ball bounces inside twelve concentric rings and escapes them one by one, with a countdown and a rising note on every escape.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/kantamk-61f410
- التصنيفات / Categories: —
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 25 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: HTML Canvas, Web Audio

## الفكرة
الموضوع فيديو قصير عمودي من نوع المحاكاة المُرضية: كرة محبوسة داخل اثنتي عشرة حلقة دوّارة، في كل حلقة فجوة، وكلما مرّت الكرة عبر فجوة تحطمت الحلقة ونقص العداد. الهدف هو جذب الانتباه في الثانية الأولى والإبقاء عليه حتى الهروب الأخير عبر توتر متصاعد. ما يميز اللغة الحركية أن كل شيء محسوب بشكل حتمي من خطوة زمنية ثابتة، وأن الصوت جزء من البنية: نغمة لكل اصطدام ودرجة سلمية أعلى لكل هروب.

## Concept
The subject is a vertical short in the satisfying-simulation genre: a ball trapped inside twelve rotating concentric rings, each with a gap; whenever the ball slips through a gap the ring shatters and the counter drops. The goal is to hook within the first second and hold attention until the final escape through rising tension. The motion language is strictly deterministic from a fixed time step, and sound is structural: one note per collision and one scale degree higher per escape.

## المشاهد المقترحة
- 0-2 ث: تتجمع الحلقات الاثنتا عشرة من المركز إلى الخارج بتأخير 60 ms بين كل واحدة؛ تسقط الكرة في المنتصف؛ ويظهر عدّاد كبير يقرأ 12 في الأعلى.
- 2-18 ث: الحلقة الرئيسية. ترتد الكرة؛ كل اصطدام يضيء القوس المضروب؛ وعند كل مرور عبر فجوة تتفجر الحلقة إلى شظايا، وينقص العداد، وترتفع النغمة.
- 18-22 ث: بقيت ثلاث حلقات. يتضاعف دوران الحلقات، وتضيق الكاميرا بنسبة 25 بالمئة، ويرافق كل اصطدام اهتزاز خفيف بمقدار 2 px.
- 22-25 ث: الهروب الأخير. تخرج الكرة من آخر فجوة وتطير خارج الحافة العليا؛ يصل العداد إلى 0، وتظهر كلمة (هربت) بقفزة، ثم يعود الكادر لبدايته لتكرار الحلقة.

## Proposed scenes
- 0-2s: The twelve rings assemble from the centre outward with staggered 60 ms delays; the ball drops in at the middle; a large counter reads 12 at the top.
- 2-18s: Main loop. The ball ricochets; every hit lights the struck arc; on each gap pass the ring bursts into shards, the counter decrements and the pitch climbs.
- 18-22s: Three rings left. Ring spin doubles, the camera tightens 25 percent, a subtle 2 px shake accompanies each hit.
- 22-25s: Final escape. The ball exits through the last gap and flies off the top edge; the counter hits 0, an 'ESCAPED' word snaps in, and the frame resets for a loop.

## قواعد الحركة
- الفيزياء بخطوة فرعية ثابتة 120 Hz وتُرسم عند 60 fps؛ معامل الارتداد 1.0 حتى لا تفقد الكرة طاقتها؛ الجاذبية معطلة أو بحد أقصى 200 px/s².
- تدور الحلقة رقم i بسرعة 0.3 + 0.08 × i rad/s باتجاهات متناوبة؛ عرض الفجوة 28 درجة في كل حلقة.
- وميض الاصطدام: يصبح القوس المضروب أبيض لمدة 80 ms ويتلاشى خطيًا؛ تحتفظ الكرة بثمانية أشباح كذيل على مدى 120 ms.
- إزالة الحلقة: تنقسم إلى 24 شظية قوسية تطير للخارج بسرعة 400-600 px/s بمنحنى ease-out quad وتلاشٍ خلال 500 ms.
- العدّاد: يكبر الرقم من 1.3 إلى 1.0 خلال 150 ms بمنحنى cubic-bezier(0.34, 1.56, 0.64, 1)؛ وهذا التجاوز الوحيد المسموح في العمل.
- الكاميرا: ثابتة حتى تبقى ثلاث حلقات، ثم تقريب من 1.0 إلى 1.25 خلال 3 ث بمنحنى ease-in-out؛ كل اصطدام يضيف اهتزاز 2 px يخمد خلال 100 ms.
- اللون: أرضية شبه سوداء، لكل حلقة لون خاص يتدرج 30 درجة على عجلة الألوان، والكرة بيضاء نقية.
- ممنوع: القطع، التعليقات الشارحة، العشوائية غير المبذورة، ضبابية الحركة على الكرة، وأي تشغيل لا يمكن إعادته إطارًا بإطار.

## Motion rules
- Physics at a fixed 120 Hz sub-step rendered at 60 fps; restitution 1.0 so the ball never loses energy; gravity off or at most 200 px/s squared.
- Ring i rotates at 0.3 + 0.08 × i rad/s with alternating directions; gap width 28 degrees on every ring.
- Collision flash: the struck arc goes white for 80 ms and fades linearly; the ball keeps 8 ghost copies as a trail over 120 ms.
- Ring removal: the ring splits into 24 arc shards flying outward at 400-600 px/s with ease-out quad and a 500 ms fade.
- Counter: the number scales 1.3 to 1.0 in 150 ms with cubic-bezier(0.34, 1.56, 0.64, 1); this is the only overshoot allowed in the piece.
- Camera: locked until three rings remain, then zoom 1.0 to 1.25 over 3 s ease-in-out; hits add a 2 px shake decaying in 100 ms.
- Colour: near-black ground, each ring its own hue stepping 30 degrees around the wheel, ball pure white.
- Banned: cuts, explanatory captions, unseeded randomness, motion blur on the ball, any run that cannot be reproduced frame for frame.

## Facts stated by the source (rewritten in our words)
- The only stated goal is a video with the potential to spread widely.
- The ball-and-twelve-rings subject comes from the public title, not from the prompt body.
- No duration, stack or structure is stated.

## Assumptions
The ring mechanics, the 25 s length, the countdown and the rising-pitch audio are all proposals built on the title; the source text itself says nothing about how the video looks or sounds. The vertical format follows the listed 720x1280 video.

## Keywords
physics simulation, bouncing ball, concentric rings, satisfying loop, viral short, countdown, كرة مرتدة, محاكاة فيزيائية, حلقات, فيديو عمودي, canvas, نغمات تصاعدية
