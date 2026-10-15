# نظام حركي تقوده نقطة برتقالية واحدة — Orange dot motion system

> فيلم 2D مدته 15 ثانية تربط فيه نقطة برتقالية واحدة كل المشاهد: من مفتاح تبديل إلى حرف إلى رسم زنبركي إلى شكل إلى بطاقة ختامية.
>
> A 15-second 2D film where one orange dot threads every scene: toggle, letter, spring graph, shape, halftone field and end card, looping back to the start.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/ultimaxbt-bbebf5
- التصنيفات / Categories: product-ui, charts, diagrams, kinetic-type, shapes, particles, characters, music, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: HTML Canvas, CSS, SVG

## الفكرة
الموضوع عرض لقدرات التصميم الحركي بلا إطارات مفتاحية يدوية، بطله نقطة برتقالية واحدة تنتقل من واجهة مستخدم إلى حرف إلى رسم بياني إلى شكل كبير ثم تعود. الهدف إقناع المشاهد بأن الحركة المتصلة أقوى من أي انتقال عشوائي. اللغة الحركية حادة ومضبوطة: تجاوزات زنبركية صغيرة، لا زمن ميت، وكل حركة متولدة من عنصر موجود على الشاشة بالفعل، ولوحة محصورة في خلفية فاتحة دافئة وأسطح شبه سوداء ولون برتقالي واحد.

## Concept
The subject is a demonstration of motion craft without hand-set keyframes, starring a single orange dot that travels from a UI toggle to a letter to a graph to a giant shape and back. The goal is to convince the viewer that connected motion beats any random transition. The language is sharp and controlled: small spring overshoots, zero dead time, every move born from something already on screen, and a palette locked to a warm off-white canvas, near-black surfaces and one orange.

## المشاهد المقترحة
- 0-2.5 ث: يصل المؤشر وينقر مفتاح التبديل البرتقالي بجانب تسمية إعدادات الحركة؛ يقفز مقبض المفتاح بزنبرك، تنحني الحروف المحيطة وتنزلق حتى لا تبقى سوى كلمة واحدة، وتستقر النقطة كنقطة فوق حرف 'i'.
- 2.5-5.5 ث: تقفز النقطة من الكلمة إلى رسم بياني؛ يُرسم مسار طيرانها خلفها كمنحنى استجابة زنبركية يتجاوز الهدف ثم يستقر بجانب وسم نسبة مئوية موجبة.
- 5.5-9 ث: تندفع النقطة على خط، تنتفخ إلى دائرة تغمر الإطار؛ يدور بداخلها مربع مستدير الزوايا شبه أسود، يتمدد إلى كبسولة، ثم ينكمش المشهد إلى نقطة برتقالية واحدة على أسود.
- 9-12 ث: تدور كلمات القدرات حول النقطة على مسار دائري؛ تنفتح حلقة الحروف إلى الخارج وتسلم الإطار إلى شبكة نقاط نصفية صغيرة تتجاوب أحجامها مع موضع النقطة البرتقالية.
- 12-14 ث: يتسع حقل النقاط النصفية متجاوزاً حواف الإطار وينقلب إلى الأسود كاشفاً البطاقة الختامية: اسم نموذج، ودور المصمم، وادعاء صفر إطارات مفتاحية.
- 14-15 ث: تعود النقطة على مسارها عبر النقاط النصفية والرسم البياني والمفتاح ليطابق الإطار الأخير إطار البداية في حلقة سلسة.

## Proposed scenes
- 0-2.5s: A cursor arrives and clicks the orange toggle beside a motion-settings label; the toggle knob springs across, the surrounding letters bend and slide until only the single word remains, and the dot settles as the tittle over its 'i'.
- 2.5-5.5s: The dot leaps off the word onto a graph; its flight path is drawn behind it as a spring response curve that overshoots the target and settles next to a positive percentage callout.
- 5.5-9s: The dot races along a line, swells into a circle that floods the frame; a near-black rounded square rotates inside it, stretches into a pill, and the scene contracts to one orange dot on black.
- 9-12s: Capability words orbit the dot on a circular path; the ring of letters opens outward and hands the frame to a halftone grid of tiny dots whose sizes react to the orange dot's position.
- 12-14s: The halftone field expands past the frame edges and flips to black, revealing the end card: a model name, the designer role and a zero-keyframes claim.
- 14-15s: The dot retraces its route through halftone, graph and toggle so the final frame matches the opening frame for a seamless loop.

## قواعد الحركة
- كل المرئيات تُحسب من الزمن داخل seek(t) بدقة 1920 في 1080 و60 إطاراً في الثانية: لا CSS transitions ولا مؤقتات ولا حالة بين الإطارات.
- الزنبركات مغلقة الصيغة (صلابة 150 وتخميد 14 لقفزة النقطة؛ 220 و26 للمفتاح)؛ منحنى الرسم البياني يُرسم من دالة الزنبرك نفسها التي تحرك النقطة ليتفق الحركة والرسم.
- تتحرك الحروف فرادى بتدرج 30 مللي ثانية أثناء اختزال الكلمة؛ تحصل الحروف الخارجة والداخلة على توقيت منفصل كي لا يتداخل شيء.
- الدائرة والمربع المستدير والكبسولة شكل واحد في حالات مختلفة؛ يُحفظ موضعه وسرعته عبر كل تحول، ويجب أن يتجاوز الغمر الزوايا الأربع قبل الانكماش.
- الكاميرا مثبتة؛ كل الحركة الظاهرة تأتي من الشكل نفسه. لا دوران ولا دفع ولا اهتزاز.
- اللون ثابت كما حدد المبدع: خلفية فاتحة دافئة، أسطح شبه سوداء، ولون برتقالي واحد يُعاد استخدامه بالتطابق في كل مشهد.
- كل نبضة رئيسية تحمل تغييراً بصرياً؛ النقرة وهبوط النقطة وذروة الرسم وتحولات الشكل والعنوان الختامي كل منها على نبضة مقاسة.
- حظر المبدع: اللقطات الجاهزة، التدرجات اللونية، الوهج، انفجارات الجسيمات، الانتقالات العشوائية، وأي حركة غير مرتبطة بعنصر موجود على الشاشة.

## Motion rules
- All visuals are computed from time inside seek(t) at 1920 by 1080 and 60 fps: no CSS transitions, timers or state between frames.
- Springs are closed-form (stiffness 150, damping 14 for the dot's jump; 220 and 26 for the toggle); the graph curve is drawn from the exact same spring function that moves the dot, so motion and plot agree.
- Letters animate individually with 30 ms stagger during the word reduction; outgoing and incoming glyphs get separate timing so nothing overlaps.
- Circle, rounded square and pill are one shape in different states; its position and velocity are preserved through every transformation, and fills must overscale past all four corners before contracting.
- Camera stays locked; all apparent movement comes from the shape itself. No orbit, no push, no shake.
- Colour is fixed as the creator specified: warm off-white canvas, near-black surfaces and one orange accent reused identically in every scene.
- Every major beat carries a visual change; click, dot landing, graph peak, shape changes and final title are each placed on a measured beat.
- Banned by the creator: stock footage, gradients, glows, particle bursts, random transitions and any motion not connected to an element already on screen.

## Facts stated by the source (rewritten in our words)
- A 16:9 2D film of about 15 seconds at 1920 by 1080 and 60 fps, built as one HTML file driven purely by time.
- Palette stated by the creator: warm off-white canvas, near-black backgrounds, bold type and one vivid orange accent that links every scene.
- Structure: a cursor clicks a motion toggle, the label reduces to one word, the dot jumps onto a spring graph with a percentage callout, grows into a shape that fills the frame, is orbited by capability words, hands over to a halftone field, reveals an end card and returns to the first frame.
- Springs are closed-form; the graph and the dot share the same spring function; letters are animated individually; the halftone dots respond to the orange dot.
- Key events are synced to measured beats and one frame per beat is rendered to check pacing before the full export.
- Inputs requested: a toggle label, a hero word, a percentage, end-card text, an accent colour and a track with a clear beat.

## Assumptions
Per-scene second ranges and the spring constants are proposed; the source fixes the structure, palette and build method but not exact timings or stiffness values.

## Keywords
connected motion, spring graph, halftone grid, toggle click, shape morph, seamless loop, orbiting type, one accent, نقطة واحدة, حركة متصلة, رسم زنبركي, شبكة نقاط نصفية, حلقة سلسة, نص دائري
