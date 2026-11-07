# نفق إطارات يشرح التحريك بالأرقام الدقيقة — Remotion workflow with precise timing

> فيديو عمودي 4:5 مدته 20 ثانية بأسلوب واجهة مطور داكنة: عنوان أبيض وبنفسجي ثابت في الأعلى، عداد إطارات ضخم يعد من 0 إلى 600، قائمة خطوات تُعلَّم بالأخضر واحدة تلو الأخرى، ونفق من مستطيلات بنفسجية متداخلة في الوسط تظهر داخله لقطات واجهة (زر تصدير، نقرة، اكتمال) ثم دورة مراحل، وطرفية أسفل تكتب الأوامر؛ وينتهي بـ600/600 أخضر ومعادلة الثواني بالإطارات.
>
> A 20 s 4:5 dark developer-UI piece: a fixed white-and-violet headline, a big frame counter ticking 0 to 600, a five-step checklist ticking green, a tunnel of nested violet rectangles where UI moments appear (export, click, done) and then a loop of stages, a terminal typing commands below, ending on a green 600/600.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/yarad-ai-8a2c4c
- التصنيفات / Categories: diagrams, kinetic-type, code
- النسبة المقترحة / Aspect: 4:5 · المدة / Duration: 20 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
الفكرة أن التوقيت في الفيديو المبني بالكود أرقام وليس إحساساً: كل حدث له رقم إطار. لذلك الرقم هو البطل، يعد في الأعلى طوال الوقت، وكل لحظة في النفق موسومة برقم إطارها، والطرفية تكتب القرارات نفسها كأوامر. النفق المتداخل يوحي بالغوص إطاراً بعد إطار.

## Concept
The idea is that timing in code-built video is numbers, not feel: every event has a frame number. So the counter is the hero, ticking at the top the whole time, every moment inside the tunnel is stamped with its frame, and the terminal types the same decisions as commands. The nested tunnel suggests diving frame by frame.

## المشاهد المقترحة
- 0-2 ث: مجال نيلي داكن: العنوان بسطرين (أبيض فوق بنفسجي) أعلى اليسار بسطر فرعي صغير بخط أحادي؛ يبدأ عداد الإطارات، ولوحة قائمة فارغة يميناً، ونفق المستطيلات المتداخلة يُرسم نحو المركز بينما تكتب الطرفية تعليقاً.
- 2-4 ث: الخطوة الأولى تُعلَّم بالأخضر؛ الطرفية تحدد معدل الإطارات والمدة؛ وداخل النفق بطاقة واجهة صغيرة تطير نحو الكاميرا وتستقر كبطاقة «دخول» بزر تصدير، وإطار النفق يتوهج بالنعناعي.
- 4-7 ث: الخطوتان الثانية والثالثة تُعلَّمان؛ الطرفية تسرد ترتيب اللحظات والإطارات الدقيقة؛ البطاقة تبتعد ثم تعود كبطاقة «فعل» بمؤشر ينقر زر التصدير مع رقم إطارها.
- 7-9 ث: بطاقة «النتيجة»: دائرة صح نعناعية كبيرة ورسالة اكتمال التصدير بتفاصيل الملف؛ الإطار كله يومض بحد نعناعي؛ والطرفية تؤكد وضوح القراءة ومدة الثبات.
- 9-14 ث: النفق يفرغ وينبض؛ الخطوة الرابعة تُعلَّم بينما تثبّت الطرفية المهارات؛ ثم تصطف ثلاث صور مصغرة لقصة مصورة أسفل النفق (فتح، نقر، نهائي) وتأخذ كل منها علامة خضراء.
- 14-18 ث: الخطوة الخامسة تُعلَّم؛ حلقة من أسماء المراحل (إطارات، طلب، توليد، لقطات، مراجعة، تصيير) تدور داخل النفق مع عداد دورات في الوسط؛ الأسماء تضيء بالنعناعي بالتناوب والعداد ينتقل من x1 إلى x2.
- 18-20 ث: اللوحات تتلاشى؛ العداد ينتقل إلى الوسط ويكبر؛ وعند 600 يصير نعناعياً مع سطر يساوي 20 ثانية بـ600 إطار وإشارة صغيرة إلى التفصيل الكامل، بينما تعلن الطرفية انتهاء التصيير.

## Proposed scenes
- 0-2s: Dark indigo field: the two-line headline (white over violet) sits top-left with a small monospace subline; the frame counter starts, an empty checklist panel at right, and the nested-rectangle tunnel draws in toward the centre while the terminal types a comment.
- 2-4s: Step one ticks green; the terminal sets fps and duration; inside the tunnel a tiny UI card flies toward camera and lands as an 'entrance' keyframe card with an export button, the tunnel frame glowing mint.
- 4-7s: Step two and three tick; the terminal lists the beat order and exact frames; the card recedes and returns as an 'action' card with a cursor clicking the export button, its frame stamped.
- 7-9s: The 'result' card: a big mint check circle and an export-complete message with file details; the whole frame flashes a mint border; the terminal confirms readability and a hold length.
- 9-14s: The tunnel empties and pulses; step four ticks as the terminal installs skills; then three small storyboard thumbnails line up at the bottom of the tunnel (open, click, final) each getting a green check.
- 14-18s: Step five ticks; a ring of stage labels (frames, brief, generate, stills, revision, render) orbits inside the tunnel with a loop counter in the centre; labels light mint in turn and the counter goes from x1 to x2.
- 18-20s: Panels fade; the counter moves to centre and grows; at 600 it turns mint with a line equating 20 s to 600 frames and a small 'full breakdown' cue, while the terminal reports the finished render.

## قواعد الحركة
- اللوحة: نيلي عميق من #0e0b1e إلى #151129، بنفسجي النفق #6b4ee6 بشفافيات متفاوتة، بنفسجي العنوان #8b6cff، نعناعي النجاح #3ee6a8، أبيض #f2f0ff، ورمادي لافندر خافت #8a84a8.
- الخط: سانس هندسي ثقيل للعنوان (سطران، الثاني بنفسجي)، وخط أحادي للعداد والقائمة وأرقام الإطارات والطرفية؛ والعداد مكمّل بالأصفار إلى أربع خانات.
- العداد يزيد كل إطار بمعدل 30 إطاراً في الثانية وهو المرجع الوحيد؛ وكل حدث على الشاشة يُظهر رقم إطاره.
- النفق: 12-16 مستطيلاً مستدير الزوايا متحدة المركز بتصغير منظوري، تتنفس ببطء دخولاً وخروجاً؛ والبطاقات تطير من نقطة التلاشي إلى الأمام بتباطؤ خلال نحو 15 إطاراً.
- بنود القائمة تُعلَّم عند إطارات محددة بتعبئة نعناعية وإبراز قصير للصف؛ والطرفية تكتب بنحو 40 حرفاً في الثانية، وأسطر التأكيد بعلامة صح خضراء.
- لحظات النجاح تتوهج بالنعناعي عبر النفق وحد الإطار نحو 10 إطارات؛ والنهاية تخلي كل اللوحات للتركيز على الرقم الأخير.

## Motion rules
- Palette: deep indigo #0e0b1e to #151129, tunnel violet #6b4ee6 at varying opacity, headline violet #8b6cff, mint success #3ee6a8, white #f2f0ff, dim lavender grey #8a84a8.
- Type: heavy geometric sans for the headline (two lines, second in violet), monospace for the counter, checklist, frame stamps and terminal; the counter is zero-padded to four digits.
- The counter increments every frame at 30 fps and is the single source of truth; every on-screen event shows its frame number.
- Tunnel: 12-16 concentric rounded rectangles with perspective scaling, slowly breathing in and out; cards fly from the vanishing point to the front with ease-out over ~15 frames.
- Checklist items tick at fixed frames with a mint fill and a brief row highlight; the terminal types at ~40 characters per second, green check lines for confirmations.
- Success beats glow mint across the tunnel and frame border for ~10 frames; the ending clears all panels to focus on the final number.

## Facts stated by the source (rewritten in our words)
- The piece explains a workflow for making Remotion videos with a coding agent where timing is decided in exact frame numbers.
- It is listed as a skill and tagged under diagrams, kinetic type and code; the technology named is Remotion.

## Assumptions
Observed from 24 frames sampled every ~0.84 s over 20 s: the fixed headline, frame counter to 600, five-step checklist, nested violet tunnel with entrance/action/result cards, storyboard thumbnails, stage loop and terminal lines. Assumed: exact tick frames and typing speed; an audio track exists but was not analysed. The delivered file is 720x888 (roughly 4:5), matching the catalogue aspect.

## Keywords
frame counter, developer UI, terminal, checklist, nested tunnel, keyframes, Remotion workflow, vertical video, عداد إطارات, واجهة مطور, طرفية, توقيت دقيق, فيديو عمودي, شرح سير عمل
