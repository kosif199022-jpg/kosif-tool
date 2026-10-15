# خط زمني متحرك لتاريخ الذكاء الاصطناعي — History of AI animated timeline video

> رحلة كاميرا على خط زمني أفقي تتوقف عند محطات الذكاء الاصطناعي الكبرى، وكل محطة تُرسم كمخطط صغير حي.
>
> A camera ride along a horizontal timeline that stops at the major AI milestones, each drawn as a small living diagram rather than a slide.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/kloss-xyz-b9b3f6
- التصنيفات / Categories: —
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 60 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, SVG

## الفكرة
الموضوع فيديو يبرز المحطات المفصلية في تاريخ الذكاء الاصطناعي، والهدف أن يستوعب المشاهد غير المتخصص تسلسل القفزات والركود في دقيقة واحدة. الاتجاه المقترح خط زمني واحد متصل تسافر عليه الكاميرا دون قطع، وعند كل محطة يُرسم مخطط رمزي بسيط (شريط آلة تورنغ، شبكة بيرسبترون، رقعة شطرنج، طبقات شبكة عصبية، خطوط انتباه بين كلمات). ما يميز اللغة الحركية أن فترات الركود تُعبَّر عنها بصريًا بخفوت الألوان وتقطّع الخط لا بالنص فقط.

## Concept
The subject is a video highlighting the turning points of AI history; the goal is that a non-specialist viewer grasps the sequence of leaps and slumps in about a minute. The proposed direction is one continuous timeline the camera travels without cuts; at each stop a small symbolic diagram draws itself (a Turing tape, a perceptron web, a chessboard, neural layers, attention lines between words). The distinctive move is that the slow periods are expressed visually, with dimmed colour and a dashed line, not only by text.

## المشاهد المقترحة
- 0-4 ث: العنوان فوق نقطة واحدة نابضة؛ يُرسم خط الزمن من اليسار إلى اليمين عبر الكادر وتبدأ الكاميرا بالتحرك.
- 4-16 ث: منتصف القرن. شريط برموز يتحرك لسؤال تورنغ (1950)، وتتجمع مجموعة نقاط لورشة صيف 1956، وتتلاقى خطوط موزونة في عقدة بيرسبترون (1958).
- 16-26 ث: الشتاء الأول. يهبط الإشباع، يصبح الخط متقطعًا، وتتفرع شجرة قرارات لنظام خبير ببطء في الثمانينيات، ثم يعود اللون.
- 26-40 ث: الآلات تفوز بالألعاب. رقعة شطرنج تضيء كشّ ملك (1997)، شبكة صور تتبلط بتسميات لقفزة التعلم العميق 2012، وأحجار غو تملأ الرقعة (2016).
- 40-52 ث: عصر اللغة. خطوط انتباه تتفرع بين رموز الكلمات (2017)، فقاعة محادثة تكتب ردًا (2022)، وعدّاد معاملات يصعد مع شريط لوغاريتمي.
- 52-60 ث: تتراجع الكاميرا لتكشف الخط كاملًا؛ عقدة فارغة بعنوان (التالي) تومض في النهاية؛ بطاقة ختامية.

## Proposed scenes
- 0-4s: Title over a single pulsing dot; the timeline line draws left to right across the frame and the camera starts rolling.
- 4-16s: Mid-century. A tape with symbols scrolls for the Turing question (1950), a cluster of dots gathers for the 1956 summer workshop, weighted lines converge into a perceptron node (1958).
- 16-26s: First winter. Saturation drops, the line turns dashed, an expert-system decision tree branches slowly in the 1980s, then colour returns.
- 26-40s: Machines win games. A chessboard lights up a checkmate (1997), an image grid tiles with labels for the 2012 deep-learning jump, Go stones fill a board (2016).
- 40-52s: The language era. Attention lines fan out between word tokens (2017), a chat bubble types a reply (2022), a parameter counter climbs with a log-scale bar.
- 52-60s: The camera pulls back to reveal the full line; one empty node labelled 'next' blinks at the end; closing card.

## قواعد الحركة
- تسافر الكاميرا على المحور x بسرعة ثابتة بين العقد وتتباطأ حتى التوقف عند كل عقدة خلال 900 ms بمنحنى cubic-bezier(0.4, 0, 0.2, 1)؛ لا قطع سوى التراجع الأخير.
- وصول العقدة: تكبر النقطة من 0 إلى 1 خلال 300 ms بنابض (صلابة 180، تخميد 14)؛ ويرتفع رقم السنة 20 px خلال 250 ms بمنحنى ease-out.
- تُرسم المخططات عبر stroke-dashoffset خلال 600-900 ms بمنحنى شبه خطي لتبدو كضربات قلم؛ مخطط واحد فقط يتحرك في كل لحظة.
- تبقى كل عقدة 3-5 ث؛ العناوين بحد أقصى 8 كلمات؛ السنوات بخط monospace والعناوين بخط grotesk ولا شيء غيرهما.
- فترات الركود: يهبط الإشباع إلى 20 بالمئة خلال 1 ث، ويصبح الخط متقطعًا بنمط 12 px، وتتباطأ الحركة المحيطة إلى نصف سرعتها.
- اللون: درجة مميزة واحدة لكل حقبة مع انزياح لوني متصل على طول الخط حتى تتشارك الحقب المتجاورة الدرجات.
- ممنوع: شعارات الشركات الحقيقية، لقطات شاشة المنتجات، صور الأشخاص، وفوضى التوازي الحركي خلف الخط.

## Motion rules
- Camera travels along x at constant velocity between nodes and decelerates to a stop at each one over 900 ms with cubic-bezier(0.4, 0, 0.2, 1); no cuts except the final pull-back.
- Node arrival: the dot scales 0 to 1 in 300 ms on a spring (stiffness 180, damping 14); the year label rises 20 px in 250 ms ease-out.
- Diagrams draw with stroke-dashoffset over 600-900 ms, nearly linear, so they read as pen strokes; only one diagram animates at a time.
- Each node holds 3-5 s; titles are at most 8 words; years in a monospace face, titles in a grotesk, nothing else.
- Winter periods: saturation falls to 20 percent over 1 s, the line becomes dashed with a 12 px pattern, ambient motion slows to half speed.
- Colour: one accent hue per era with a continuous hue drift along the line, so neighbouring eras share tints.
- Banned: real company logos, product screenshots, photographs of people, parallax clutter behind the line.

## Facts stated by the source (rewritten in our words)
- The subject is a video that highlights the key moments in the history of AI.
- No duration, stack, visual style or list of moments is stated.

## Assumptions
The milestone list, the 60 s runtime and the continuous-camera structure are the director's proposal; the source only names the subject. Dates are drawn from general knowledge and should be fact-checked before production.

## Keywords
timeline, explainer, ai milestones, camera travel, self-drawing diagrams, education, خط زمني, شرح متحرك, ذكاء اصطناعي, محطات تاريخية, مخططات ترسم نفسها, remotion, svg
