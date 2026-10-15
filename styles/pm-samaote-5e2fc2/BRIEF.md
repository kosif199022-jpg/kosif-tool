# فيديو كلمات أغنية متزامن مع الصوت — Synced lyrics motion video

> كلمات الأغنية تظهر على نبرة المغني بالضبط بينما تتنفس الخلفية مع الإيقاع، بأسلوب يليق بعرض أعمال مصمم موشن.
>
> Lyric words land exactly on each vocal onset while the backdrop breathes with the beat, built to read like a motion designer's showreel piece.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/samaote-5e2fc2
- التصنيفات / Categories: charts, kinetic-type, music
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 30 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, Web Audio, SVG

## الفكرة
الموضوع هو فيديو كلمات لأغنية يقدمها المستخدم، والهدف أن يشعر المشاهد بأن النص يُغنّى أمامه لا أنه يُعرض فحسب. تُبنى اللغة الحركية على ساعتين منفصلتين: ساعة الصوت البشري التي تحكم دخول كل كلمة، وساعة الإيقاع التي تحكم نبض الخلفية والأشكال والكاميرا. ما يميز الاتجاه المقترح أن كل حركة تُشتق من ملف توقيت الكلمات، فلا توجد مؤقتات يدوية، وأن التباين الطباعي يتبدل مع أقسام الأغنية (كوبليه، لازمة، كسر).

## Concept
The subject is a lyric video over a user-supplied track; the goal is that the viewer feels the words being sung rather than displayed. The motion language runs on two clocks: the vocal clock drives every word's entrance, and the beat clock drives the backdrop pulse, shapes and camera. The proposed direction derives every move from a word-timing file, with no hand-typed timers, and shifts the typographic contrast with the song's sections (verse, hook, breakdown).

## المشاهد المقترحة
- 0-3 ث: افتتاحية على خلفية داكنة؛ حلقة موجة صوتية دائرية تتجمع ضربة بعد ضربة، ويظهر اسم الأغنية والفنان، ولا كلمات بعد.
- 3-12 ث: الكوبليه. تظهر الكلمات واحدة تلو الأخرى عند بداية نطقها وتتراصّ في أسطر؛ كل سطر مكتمل ينجرف للأعلى ببطء بينما تنبض الأعمدة خلفه مع الطبلة.
- 12-14 ث: ما قبل اللازمة. تدفع الكاميرا للداخل، وتنضغط الأسطر إلى كلمة واحدة كبيرة لكل نطق، وتضيق الأعمدة إلى شبكة مشدودة.
- 14-24 ث: اللازمة. تملأ الكلمات الكادر من طرفه إلى طرفه؛ تنقلب الألوان على أول ضربة في المقطع، وكلمة اللازمة المتكررة تكبر بنابض في كل عودة.
- 24-28 ث: الكسر. تتفكك الكلمات إلى جسيمات تتبعثر مع الإيقاع؛ تعود حلقة الموجة وتفقد الألوان إشباعها.
- 28-30 ث: الخاتمة. تعود بطاقة العنوان بالألوان المقلوبة؛ تثبت آخر كلمة حتى الضربة الأخيرة ثم تنغلق الحلقة.

## Proposed scenes
- 0-3s: Cold open on a dark field; a circular waveform ring assembles beat by beat, the track title and artist fade in, no lyrics yet.
- 3-12s: Verse. Words appear one at a time on their vocal onsets and stack into lines; each finished line drifts slowly upward while vertical bars behind it pulse on the kick.
- 12-14s: Pre-hook. The camera pushes in, lines compress to a single large word per onset, bars narrow into a tight grid.
- 14-24s: Hook. Words fill the frame edge to edge; the palette inverts on the section downbeat, and the repeated hook word scales with a spring every time it returns.
- 24-28s: Breakdown. Words dissolve into particles that scatter on the beat; the waveform ring returns and the palette desaturates.
- 28-30s: Outro. Title card returns in the inverted palette; the last word holds until the final beat, then the ring closes.

## قواعد الحركة
- تدخل كل كلمة خلال 40 ms من زمن بداية نطقها في ملف التوقيت؛ مدة الدخول 180 ms بمنحنى cubic-bezier(0.2, 0.9, 0.2, 1) (تكبير من 0.92 إلى 1 مع ظهور تدريجي).
- يبقى السطر حتى أول نطق في السطر التالي، ثم يخرج خلال 240 ms بمنحنى cubic-bezier(0.6, 0, 0.9, 0.4)؛ لا يُخرج السطر أثناء كلمة.
- العناصر المرتبطة بالإيقاع تنبض من 1.0 إلى 1.06 مع كل ضربة طبلة وتتلاشى أسيًا خلال 300 ms؛ لا شيء ينبض في كل إطار.
- الكاميرا: دفع بطيء بنسبة 2 بالمئة كل أربع مازورات؛ القطع الحاد مسموح فقط على الضربة الأولى التي تفتح مقطعًا جديدًا.
- الطباعة: خط sans ثقيل واحد للكلمات، بحد أقصى 6 كلمات ظاهرة؛ الكلمات العربية محاذاة لليمين مع تشكيل صحيح للحروف وتتحرك بالكلمة لا بالحرف.
- اللون: لوحة من لونين لكل مقطع؛ الانقلاب اللوني يتم في إطار واحد على الضربة الأولى للمقطع دون انتقال تدريجي.
- الصوت: مسار المستخدم يبقى كما هو؛ لا إعادة مزج ولا خفض ولا تمديد زمني.
- ممنوع: ظهور الكلمات قبل غنائها، تأثير الآلة الكاتبة، الاهتزاز العشوائي، أكثر من خط واحد.

## Motion rules
- Every word enters within 40 ms of its onset timestamp from the word-timing file; entrance lasts 180 ms with cubic-bezier(0.2, 0.9, 0.2, 1) (scale 0.92 to 1 plus fade).
- A line holds until the next line's first onset, then exits over 240 ms with cubic-bezier(0.6, 0, 0.9, 0.4); never exit mid-word.
- Beat-driven elements pulse scale 1.0 to 1.06 on each kick and decay exponentially over 300 ms; nothing pulses on every frame.
- Camera: a slow push of 2 percent per four bars; a hard cut is allowed only on the downbeat that opens a new section.
- Typography: one heavy sans for lyrics, max 6 words visible at once; Arabic lyrics align right, keep proper shaping and animate by word, never by letter.
- Colour: a two-tone palette per section; inversion happens in a single frame on the section downbeat, no tween.
- Audio: the user's track is untouched; no re-mixing, ducking or time-stretching.
- Banned: words appearing before they are sung, typewriter effects, random jitter, more than one typeface.

## Facts stated by the source (rewritten in our words)
- The piece is a lyric video driven by a music track the user attaches.
- Both the words and the animation must line up with the singer's voice and the beat.
- It is meant to feel like a showreel piece good enough for a designer's résumé.
- No duration, resolution or stack is stated.

## Assumptions
The 30 s length, the two-clock structure and the section breakdown are proposals; the source only states the sync requirement and the showreel ambition. Word timings are assumed to come from a transcription file supplied with the track.

## Keywords
lyrics video, kinetic typography, beat sync, word timing, showreel, كلمات أغنية, تزامن صوتي, طباعة حركية, إيقاع, waveform, remotion, موجة صوتية
