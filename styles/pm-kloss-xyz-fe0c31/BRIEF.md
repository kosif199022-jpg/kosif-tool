# خط زمني متحرك لأبرز محطات الذكاء الاصطناعي — History of AI timeline

> فيلم خط زمني مدته 45 ثانية يسافر على مسار واحد عبر محطات الذكاء الاصطناعي الكبرى من اختبار تورنغ إلى نماذج اللغة الحديثة.
>
> A 45-second timeline film that rides a single track through the big AI milestones, from the Turing test to modern language models.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/kloss-xyz-fe0c31
- التصنيفات / Categories: —
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 45 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع تاريخ الذكاء الاصطناعي عبر لحظاته المفصلية، والهدف أن يخرج المشاهد بخريطة ذهنية واضحة للترتيب والسببية: ما الذي مهد لماذا. اللغة الحركية مبنية على مسار زمني واحد متصل تسير عليه الكاميرا جانبياً بلا قطع، وتتفرع منه بطاقات محطات تنبثق من علامات التاريخ، وتتغير كثافة المسار لتعكس 'شتاء' الذكاء الاصطناعي وانفجاره اللاحق، مع عداد سنوات يتسارع ويتباطأ حسب كثافة الأحداث.

## Concept
The subject is the history of AI through its turning points, and the goal is to leave the viewer with a clear mental map of order and causality: what paved the way for what. The motion language is one continuous timeline track the camera travels sideways along without cuts; milestone cards sprout from date markers, the track thins and thickens to reflect the AI winters and the later explosion, and a year counter speeds up and slows down with event density.

## المشاهد المقترحة
- 0-4 ث: يُرسم مسار أفقي من اليسار؛ يدور عداد السنوات من 1940 إلى 1950 وترتفع البطاقة الأولى: اختبار تورنغ، مع علامة استفهام تتحول إلى مؤشر طرفية.
- 4-12 ث: تتحرك الكاميرا يميناً عبر 1956 (بطاقة ورشة عمل تتجمع فيها دائرة كراسٍ) و1966 (بطاقة روبوت محادثة مبكر تظهر فيها أسطر مكتوبة وترد)؛ ينخفض المسار ويفقد تشبعه مع شتاء الذكاء الاصطناعي الأول.
- 12-20 ث: يسطع المسار عند 1997 (رقعة شطرنج تنزلق فيها قطعة واحدة إلى كش مات) و2011 (بطاقة برنامج مسابقات يضيء فيها زر الإجابة).
- 20-30 ث: تزداد الكثافة: 2012 التعرف على الصور بالتعلم العميق (شبكة صور مصغرة تسمي نفسها)، 2016 الانتصار في لعبة اللوح (أحجار سوداء وبيضاء تملأ اللوح حلزونياً)، 2017 بنية الانتباه (خطوط تربط الكلمات بالكلمات).
- 30-40 ث: يتسع المسار إلى مستوى: تصل نماذج اللغة الكبيرة 2020-2022 كفقاعة محادثة تكتب فقرة خلال ثانيتين، وبطاقة توليد صور ترسم نفسها من الضجيج إلى الصورة.
- 40-45 ث: تتراجع الكاميرا لتكشف الخط الزمني كله كخط واحد بكل علاماته مضاءة؛ يهبط عداد السنوات على 'اليوم' ويثبت العنوان الختامي ثانية واحدة.

## Proposed scenes
- 0-4s: A horizontal track draws from the left; the year counter spins from 1940 to 1950 and the first card rises: the Turing test, with a question mark morphing into a terminal cursor.
- 4-12s: The camera tracks right through 1956 (a workshop card with a circle of chairs assembling) and 1966 (an early chatbot card where typed lines appear and reply); the track dips and desaturates for the first AI winter.
- 12-20s: The track brightens for 1997 (a chessboard where a single piece slides to checkmate) and 2011 (a quiz-show card with a buzzer lighting up).
- 20-30s: Density increases: 2012 deep-learning image recognition (a grid of thumbnails labels itself), 2016 the board-game victory (black and white stones fill a board in a spiral), 2017 the attention architecture (lines connect words to words).
- 30-40s: The track widens into a plane: 2020-2022 large language models arrive as a chat bubble that types a paragraph in 2 s, and an image-generation card paints itself from noise to picture.
- 40-45s: The camera pulls back to reveal the whole timeline as one line with all markers lit; the year counter lands on 'today' and the closing title holds 1 s.

## قواعد الحركة
- الكاميرا حركة جانبية واحدة متصلة على المسار، مسهّلة لكل مقطع بمنحنى cubic-bezier(0.4, 0, 0.2, 1)؛ تبطئ إلى 30% من سرعتها حول التجمعات الكثيفة ولا تعود للخلف حتى السحبة النهائية.
- ترتفع بطاقات المحطات من علامة تاريخها خلال 400 مللي ثانية (translateY من 40 بكسل إلى صفر، تخميد زنبركي 20)؛ رسم كل بطاقة SVG يكمل حركته الدقيقة خلال 1-1.5 ثانية قبل مغادرة الكاميرا.
- عداد السنوات رقم متدحرج مرتبط بموضع الكاميرا لا بزمن الساعة، فتُقرأ تغيرات الإيقاع كسفر.
- سماكة خط المسار وتشبعه يرمزان للنشاط: 2 بكسل و40% تشبع أثناء فترات الشتاء، و6 بكسل ولون كامل من عقد 2010 فصاعداً.
- الطباعة: السنة برقم جدولي كبير، عنوان المحطة بخط sans عريض، وشرح من سطر واحد بوزن أخف؛ لا يتجاوز الشرح 8 كلمات.
- اللون: خلفية كحلية عميقة، نص فاتح، ولون دافئ واحد للمسار والعلامة النشطة؛ لون بارد ثانوي واحد لمقاطع الشتاء فقط.
- ممنوع: القطع الحاد بين الحقب، صور الأشخاص الحقيقيين، كليشيهات الروبوتات، تأثيرات الخلل، وتلاشي النص دخولاً وخروجاً بلا حركة.

## Motion rules
- The camera is one continuous lateral dolly along the track, eased per segment with cubic-bezier(0.4, 0, 0.2, 1); it slows to 30% speed around dense clusters and never reverses until the final pull-back.
- Milestone cards rise from their date marker in 400 ms (translateY 40 px to 0, spring damping 20); each card's illustration is an SVG that completes its own 1-1.5 s micro-animation before the camera leaves.
- The year counter is a rolling numeral tied to camera position, not to wall-clock time, so pacing changes read as travel.
- Track stroke width and saturation encode activity: 2 px and 40% saturation during the winters, 6 px and full colour from the 2010s onward.
- Typography: year in a large tabular numeral, milestone title in a bold sans, a one-line caption in a lighter weight; captions never exceed 8 words.
- Colour: a deep navy canvas, light text and a single warm accent for the track and active marker; one secondary cool accent for the winter segments only.
- Banned: hard cuts between eras, photographs of real people, robot clichés, glitch effects and fading text in and out without movement.

## Facts stated by the source (rewritten in our words)
- The creator asked for a video that highlights the key moments in AI history; no duration, stack or structure is specified.

## Assumptions
The milestone list, the 45-second length, the navy palette and the single-track camera are all my proposal; the source gives only the subject in one sentence.

## Keywords
timeline, history explainer, milestones, lateral dolly, year counter, turing test, deep learning, ai winter, خط زمني, تاريخ الذكاء الاصطناعي, محطات, فيلم تعليمي, كاميرا جانبية, بطاقات معلومات
