# ريفلكس: ريل رد الفعل في خمس عشرة ثانية — Reflex brand motion reel

> ريل علامة لشركة reflex. inc في 15 ثانية مقطوع على الإيقاع: خطّاف في الثانية الأولى، ثم حروف وأشكال وكاميرا وتحولات لون، وإطار ختامي نظيف.
>
> A 15-second brand reel for reflex. inc cut to music: a one-second hook, then typography, shape play, camera whips and colour flips, landing on a clean final frame.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/reflex-cloud-72ffe5
- التصنيفات / Categories: charts, kinetic-type, shapes, photos, music
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, Web Audio

## الفكرة
الموضوع ريل ترويجي لعلامة reflex. inc، يطلبه صاحبه بصيغة سيرة ذاتية لمصمم حركة من الطراز الأول. الهدف إيصال ثقة وسرعة استجابة في 15 ثانية، مع تدرج معلن عبر تقنيات متمايزة وإطار نهائي يسهل تذكره. لغة الحركة تبني على معنى الاسم: كل عنصر يتصرف كرد فعل انعكاسي لضربة إيقاعية، فلا يسبقها ولا يتأخر عنها أكثر من إطار واحد، والألوان تنقلب فجأة لا بتدرج، والكاميرا تنتقل بحركات خاطفة قصيرة.

## Concept
The subject is a promotional reel for the brand reflex. inc, requested in the voice of a top-tier motion designer's résumé piece. The goal is to convey confidence and responsiveness in 15 seconds, with a stated progression through distinct techniques and a final frame that is easy to remember. The motion language builds on the name itself: every element behaves like a reflex to a musical hit, never leading or trailing the beat by more than one frame, colours flip instantly rather than tween, and the camera moves in short whips.

## المشاهد المقترحة
- 0-1 ث: الخطّاف: حلقة رفيعة تندفع من المركز للخارج خلال 300ms، اسم العلامة يثبت في الإطار السادس مع تجاوز لإطارين، وتسقط معه ضربة جهير.
- 1-4.5 ث: الحروف: عبارات من ثلاث كلمات تندفع على الضربات؛ كل كلمة مثير يهتز إطاراً واحداً ثم يثبت، وتتبدل كل 500ms؛ تتمدد الحروف 15% عند الضربة ثم تعود.
- 4.5-8 ث: لعب الأشكال: شبكة نقاط 12×7 تتموج للخارج من نقرة مؤشر (تكبير النقاط من 1 إلى 1.8 ثم 1 في موجات 240ms)؛ مخطط أعمدة لزمن الاستجابة يرتفع ثم ينضغط في خط واحد.
- 8-11.5 ث: الكاميرا واللون: حركة خاطفة أفقية عبر أربع بلاطات صور (بدائل لصور العلامة) مع ضبابية اتجاهية 8px، ولكل بلاطة طبقتان بعمق مختلف؛ عند الذروة يدور لون اللوحة 180 درجة في إطار واحد.
- 11.5-15 ث: الحسم: ينحسر اللون إلى ثنائية العلامة، يتركب اللوغو مع عبارة reflex. inc وسطر الموقع تحتها، ويثبت الإطار تماماً 1.5 ثانية.

## Proposed scenes
- 0-1s: Hook: a thin ring punches outward from centre in 300ms, the brand name snaps in on frame 6 with a two-frame overshoot, and a sub-bass hit lands with it.
- 1-4.5s: Typography: three-word statements punch in on beats; each word is a stimulus that jitters for one frame and then locks, swapping every 500ms; letterforms stretch 15% on the hit and recover.
- 4.5-8s: Shape play: a 12x7 dot grid ripples outward from a cursor tap (dots scale 1 to 1.8 to 1 in 240ms waves); a reaction-time bar chart rises and then compresses into a single line.
- 8-11.5s: Camera and colour: a whip-pan across four photo tiles (brand imagery placeholders) with 8px directional blur, each tile parallaxing two layers; on the drop the palette hue-rotates 180 degrees in a single frame.
- 11.5-15s: Resolve: colour drains to the brand duo-tone, the logo and the words reflex. inc lock up with a URL line underneath, and the frame holds perfectly still for 1.5s.

## قواعد الحركة
- شبكة موسيقية بسرعة 128 BPM (مقترح، 469ms للضربة)؛ كل رد فعل ينطلق خلال إطار أو إطارين من علامة الضربة اعتماداً على جدول توقيت مشترك.
- لا منحنى دخول للحروف: قطع حاد إلى حجم 110% ثم استقرار خلال 150ms بمنحنى cubic-bezier(0.2, 0.9, 0.3, 1).
- الأشكال تتحرك بنوابض (stiffness 220، damping 12) ليظهر تجاوز الموجات بوضوح؛ جبهة موجة شبكة النقاط تسير بسرعة 900px/s.
- الحركات الخاطفة تستغرق 180ms مع ضبابية اتجاهية 8px وثبات لإطارين عند الوصول؛ لا توجد حركة كاميرا أخرى.
- تحولات اللون فورية على الضربات ولا تُدرَّج أبداً، وبحد أقصى انقلاب لوني واحد لكل مقطع موسيقي.
- الصور من مواد العلامة المرخصة فقط، تُعرض كبلاطات كاملة بطبقتي عمق بفارق 12px.
- الإطار الأخير ثابت 1.5 ثانية على الأقل بلا أي حركة، بما فيها الخلفية.
- ممنوع: التلاشي البطيء، انفجارات الجسيمات، وهج العدسة، وأي عنصر يتحرك خارج الإيقاع.

## Motion rules
- Music grid at 128 BPM (proposed, 469ms per beat); every reaction fires within 1-2 frames of its beat marker, read from a shared timing table.
- Type has no entry easing: hard cut to 110% scale, then a 150ms settle to 100% using cubic-bezier(0.2, 0.9, 0.3, 1).
- Shapes use springs (stiffness 220, damping 12) so ripples overshoot visibly; the dot-grid wave front travels at 900px/s.
- Whip-pans last 180ms with 8px directional blur and a 2-frame hold on arrival; no other camera motion exists.
- Colour shifts are instantaneous on beats, never tweened, and at most one hue flip per bar.
- Photos are supplied or licensed brand imagery only, shown as full-bleed tiles with a 2-layer parallax of 12px.
- The final frame is static for at least 1.5s with nothing animating, including the background.
- Banned: slow fades, particle explosions, lens flares, and any element that moves off-beat.

## Facts stated by the source (rewritten in our words)
- Length is 15 seconds and the tone should be dynamic and confident.
- Structure is stated: a strong hook inside the first second, a run of distinct techniques (type, shapes, camera moves, colour changes), then a clean memorable closing frame.
- Pacing should feel edited to music; the reel must promote the brand reflex. inc.
- The creator asked the tool to start from scratch rather than rely on existing, possibly outdated, tooling.
- Site tags: charts, kinetic type, shapes, photos, music.

## Assumptions
The 128 BPM grid, the reflex/stimulus idea, the dot-grid ripple, the 180-degree hue flip and all durations are proposed; the source states the structure and purpose but no colours, timings or stack. 1920x1080 is read as 16:9.

## Keywords
brand reel, ريل علامة, beat sync, مزامنة الإيقاع, whip pan, حركة خاطفة, dot grid, شبكة نقاط, hue flip, انقلاب لوني, hook, reaction time, خطّاف افتتاحي, kinetic type
