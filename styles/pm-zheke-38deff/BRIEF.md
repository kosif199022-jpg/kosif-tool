# طباعة حركية مربعة: جملة واحدة تعيد بناء نفسها — Kinetic type showreel

> قطعة مربعة 12 ثانية من الطباعة الحركية الثنائية اللغة: جملة واحدة تتفكك وتتجمع وتغير وزنها على إيقاع ثابت دون أي عنصر غير الحروف.
>
> A 12s square kinetic-type piece: one bilingual sentence breaks apart, reflows and changes weight on a steady pulse, with nothing on screen but letters.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/zheke-38deff
- التصنيفات / Categories: kinetic-type
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 12 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, SVG, CSS

## الفكرة
الموضوع هو الحرف ذاته: جملة واحدة ثنائية اللغة (عربية ولاتينية) تُعرض في إطار مربع وتتفكك وتتجمع وتغير وزنها طوال اثنتي عشرة ثانية. الهدف إثبات الإتقان بأقل العناصر: لا صور، لا أشكال، لا تأثيرات، الحروف وحدها تحمل الإيقاع. ما يميز اللغة الحركية الوعي بنظام الكتابة: الحروف العربية متصلة فلا تُقسم حرفاً حرفاً بل تُحرك بالكلمة أو بسلسلة الأشكال المرسومة، بينما يُحرك النص اللاتيني حرفاً حرفاً، وتُستخدم محاور الخط المتغير لتبديل الوزن بدلاً من التكبير.

## Concept
The subject is the letterform itself: one bilingual sentence (Arabic and Latin) in a square frame that breaks apart, regroups and changes weight across twelve seconds. The goal is to prove mastery with the fewest possible ingredients: no images, no shapes, no effects, only letters carrying the rhythm. What makes the motion language distinctive is script awareness: Arabic letters connect, so they move by word or by shaped glyph run while Latin text moves per letter, and weight shifts ride a variable-font axis instead of scaling.

## المشاهد المقترحة
- 0-2ث: كلمة واحدة بوزن ثقيل تهبط من مقياس 1.6x إلى 1.0 مع تجاوز قصير بمقدار إطارين؛ الإطار فارغ خلاف ذلك.
- 2-5ث: الكلمة تنفتح إلى جملة: كل كلمة جديدة تدفع السابقة على خط الأساس؛ الكلمات العربية تدخل من اليمين إلى اليسار واللاتينية من اليسار إلى اليمين وتلتقي في المنتصف.
- 5-8ث: مسح الوزن: شريط ضوئي عمودي يعبر الجملة وكل حرف تحته يهبط لحظياً إلى أرفع وزن (محور الخط المتغير) ثم يستعيد وزنه.
- 8-10ث: الجملة تدور 90 درجة وتتراص عموداً؛ الحروف تسقط من العمود واحداً تلو الآخر وتتكوم عند الحافة السفلى بهبوط ناعم.
- 10-12ث: الكومة تعيد تشكيل الكلمة الافتتاحية في موضعها الأصلي تماماً؛ ثبات 600ms، ثم يطابق الإطار الأخير الإطار الأول لتكرار الحلقة.

## Proposed scenes
- 0-2s: A single word in heavy weight slams in from 1.6x scale to 1.0 with a two-frame overshoot; the frame is otherwise empty.
- 2-5s: The word unpacks into a sentence: each new word pushes the previous one along the baseline; Arabic words enter right-to-left, Latin words left-to-right, meeting at the centre.
- 5-8s: Weight sweep: a vertical light band passes across the sentence and every letter under it momentarily drops to the thinnest weight (variable font axis), then recovers.
- 8-10s: The sentence rotates 90 degrees and stacks as a column; letters fall out of the column one by one and pile at the bottom edge with a soft landing.
- 10-12s: The pile reassembles into the opening word at its exact opening position; hold 600ms, then the final frame matches frame one for looping.

## قواعد الحركة
- النص العربي لا يُقسم حرفاً حرفاً أبداً: يُحرك بالكلمة أو بسلسلة الأشكال المتصلة (مع خطوة تحويل النص إلى مسار لبقاء الحروف متصلة)؛ النص اللاتيني يجوز تحريكه حرفاً حرفاً بتدرج 25ms.
- الدخول: إزاحة 40px في اتجاه القراءة مع عتامة من 0 إلى 1 خلال 320ms بمنحنى cubic-bezier(0.2, 0.9, 0.2, 1)؛ الخروج 180ms وأسرع من الدخول دائماً.
- تغيير الوزن عبر محور الخط المتغير (wght من 200 إلى 900) خلال 220ms؛ لا تسميك مزيف ولا تكبير بديل عن الوزن.
- القطعة كلها على نبض ثانيتين: حدث رئيسي كل ثانيتين وحدث ثانوي كل 500ms؛ لا شيء يتحرك بين الأحداث سوى ذيل المنحنى.
- الكاميرا ثابتة؛ الإطار المربع لا يتحرك أفقياً أبداً؛ الحركة الوحيدة الشبيهة بالكاميرا هي دوران كتلة النص نفسها 90 درجة.
- اللون (مقترح): لونان فقط، خلفية مسطحة وحبر واحد؛ الشريط الضوئي هو لون الخلفية بعتامة 60% فوق الحروف؛ لا تدرجات.
- ممنوع: البثق ثلاثي الأبعاد، الظلال، انتقالات ضبابية أطول من 120ms، أكثر من عائلة خط واحدة لكل نظام كتابة، ونص يبقى غير مقروء أكثر من 300ms.

## Motion rules
- Arabic text is never split per character: animate per word or per shaped glyph run (add a text-to-path step so joined letters stay joined); Latin text may animate per letter with a 25ms stagger.
- Entrances: translate 40px along the reading direction plus opacity 0 to 1 over 320ms with cubic-bezier(0.2, 0.9, 0.2, 1); exits take 180ms and are always faster than entrances.
- Weight changes use a variable font axis (wght 200 to 900) tweened over 220ms; no faux bold, no scale standing in for weight.
- The whole piece runs on a 2-second pulse: one major event every 2s, one minor event every 500ms; nothing moves between events except the tail of an easing.
- Camera: fixed; the square frame never pans; the only camera-like move is the 90-degree rotation of the type block itself.
- Colour (proposed): two colours only, a flat background and a single ink; the light band is the background colour at 60% over the letters; no gradients.
- Banned: 3D extrusion, drop shadows, blur transitions longer than 120ms, more than one type family per script, text left unreadable for more than 300ms.

## Facts stated by the source (rewritten in our words)
- The creator's entire request was an open challenge addressed to the model to prove its motion-design ability.
- The source tags the result as kinetic type only; the frame is square (1080x1080).

## Assumptions
Every scene, the 12s duration, the bilingual sentence idea and the two-colour palette are my proposal; the source states no content, timing or colours.

## Keywords
kinetic type, طباعة متحركة, variable font, خط متغير, arabic typography, خط عربي, square loop, حلقة مربعة, letter stagger, type reel, bilingual, ثنائي اللغة, text-to-path
