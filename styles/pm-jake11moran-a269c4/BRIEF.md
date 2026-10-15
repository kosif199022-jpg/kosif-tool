# حكاية جلسة الوكيل البرمجي — Animated agent session story

> فيلم قصير مُلحَّن يحوّل سجل جلسة حقيقية بين مطوّر ووكيل برمجي إلى حكاية متحركة بشخصيتين وأحداث كود.
>
> A short scored animated film that turns a real developer-and-agent coding session log into a two-character story told through code events.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/jake11moran-a269c4
- التصنيفات / Categories: characters, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 45 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: CSS, GSAP, Web Audio

## الفكرة
الموضوع هو جلسة برمجة فعلية مستخرجة من سجل Claude Code المحلي، تُروى كقصة قصيرة بطلاها مطوّر ووكيل برمجي على هيئة شخصيتين كرتونيتين. الهدف هو جعل سير العمل التقني (طلب، قراءة ملفات، تعديل، اختبار، خطأ، إصلاح) مادة عاطفية ممتعة تُفهم في أقل من دقيقة. تتميّز لغة الحركة بالمزج بين تحريك شخصيات متقطّع يشبه الرسم اليدوي وواجهة طرفية ناعمة الحركة، مع موسيقى تُبنى على قوس الجلسة من الهدوء إلى الذروة إلى الحلّ.

## Concept
The subject is an actual coding session mined from the local Claude Code history, retold as a short story whose two leads are a developer and an agent drawn as cartoon characters. The goal is to make the technical workflow (request, file reads, edits, tests, an error, the fix) emotionally legible and fun in under a minute. The motion language mixes stepped, hand-drawn-feeling character animation with smooth terminal UI motion, and a score that follows the session arc from calm to crisis to resolution.

## المشاهد المقترحة
- 0-4 ث: مؤشر يومض على خلفية سوداء؛ يُكتب اسم المشروع حرفًا حرفًا بمعدل 40 مللي ثانية للحرف، ثم تبتعد الكاميرا لتكشف عالم مكتب صغير فيه شخصية المطوّر وشخصية الوكيل.
- 4-12 ث: يكتب المطوّر طلبه الأول؛ تلتفّ الكلمات في لفافة تطير عبر المكتب، فيلتقطها الوكيل وتضيء عيناه عند فتحها.
- 12-24 ث: مونتاج استدعاءات الأدوات: أحداث القراءة والبحث والتعديل تصل كبطاقات تنغرز على الإيقاع، وتنبض العقدة المعنية في شجرة ملفات مصغّرة، ثم تأتي بطاقة خطأ تصبغ المشهد بالكهرماني ويحكّ الوكيل رأسه.
- 24-34 ث: الإصلاح: كتلة diff تمسح الأخضر فوق الأحمر، ونقاط مشغّل الاختبارات تمتلئ واحدة تلو الأخرى، وينفجر رذاذ من الأقواس والفواصل المنقوطة احتفالًا بالنجاح.
- 34-42 ث: لوحة النتائج: عدد الأدوار والملفات المعدَّلة والاختبارات الناجحة تتصاعد في لوحة بينما تتصافح الشخصيتان بقفزة ضغط وتمدّد.
- 42-45 ث: بطاقة ختامية بتاريخ الجلسة؛ يتلاشى كل شيء إلا المؤشر الذي يستمر في الوميض لنهاية قابلة للتكرار.

## Proposed scenes
- 0-4s: A blinking cursor on black; the project name types in at 40ms per glyph, then the camera pulls back to reveal a tiny desk world with the developer and the agent character.
- 4-12s: The developer types the first request; the words roll up into a scroll that flies across the desk, the agent catches it and its eyes light up as it unrolls.
- 12-24s: Tool-call montage: read, search and edit events arrive as cards snapping in on beats, the touched node in a mini file tree pulses, then an error card turns the scene amber and the agent scratches its head.
- 24-34s: The fix: a diff block wipes green over red, test-runner dots fill one by one, and a burst of brackets and semicolons celebrates the pass.
- 34-42s: Scoreboard: turns, files touched and tests passed count up in a panel while the two characters high-five with a squash-and-stretch bounce.
- 42-45s: Outro card with the session date; everything fades except the cursor, which keeps blinking for a loop-friendly end.

## قواعد الحركة
- تدخل بطاقات الواجهة بمنحنى cubic-bezier(0.22, 1, 0.36, 1) خلال 420 مللي ثانية وتخرج بمنحنى cubic-bezier(0.4, 0, 1, 1) خلال 260 مللي ثانية.
- تتحرك الشخصيات بمنحنى متدرّج (steps(12) في الثانية أي ثبات إطارين) لتبدو مرسومة باليد؛ وتبقى عناصر الواجهة ناعمة؛ لا يُجمع الأسلوبان على عنصر واحد.
- حركة كاميرا واحدة لكل مشهد: دولي بطيء من مقياس 1.00 إلى 1.08؛ الانتقال بين المشاهد قطع حاد يقع ضمن 40 مللي ثانية من النبضة الموسيقية القوية؛ لا سحبات سريعة ولا اهتزاز.
- تبقى كل بطاقة استدعاء أداة 900 مللي ثانية على الأقل ليُقرأ مسار الملف، بحدّ أقصى ثلاث بطاقات متراكبة على الشاشة.
- خط أحادي العرض لكل ما يُقتبس من السجل؛ خط عرض مستدير لتعليقات السرد؛ التعليقات العربية بخط نسخي وتُبقي الخط أحادي العرض للكود فقط.
- قاعدة طرفية داكنة مع لون تمييز واحد لكل نوع حدث (قراءة، تعديل، اختبار، خطأ)؛ يجوز لحالة الخطأ أن تصبغ الإطار كله بنسبة لا تتجاوز 15%.
- تُلحَّن الموسيقى على قوس الجلسة: خفيفة تحت الطلب، أكثف تحت استدعاءات الأدوات، وتنحلّ عند نجاح الاختبار؛ ويُخفض المزج 6 ديسيبل تحت أي صوت كتابة.
- ممنوع: عرض محتوى ملفات حقيقي أو أسرار من السجل، وتعليقات تتجاوز 8 كلمات، وأي إطار ثابت يدوم أكثر من ثانيتين.

## Motion rules
- UI cards enter with cubic-bezier(0.22, 1, 0.36, 1) over 420ms and exit with cubic-bezier(0.4, 0, 1, 1) over 260ms.
- Characters animate on a stepped curve (steps(12) per second, i.e. 2-frame holds) to feel hand-drawn; UI elements stay smooth; never mix both on one element.
- One camera move per scene: a slow dolly from scale 1.00 to 1.08; scene changes are hard cuts placed within 40ms of a musical downbeat; no whip pans or shake.
- Each tool-call card stays at least 900ms so its file path is readable, with at most three cards stacked on screen.
- Monospace type for anything quoted from the log; a rounded display face for narrative captions; Arabic captions use a Naskh-style face and keep monospace only for code.
- Dark terminal base with one accent per event type (read, edit, test, error); the error state may tint the whole frame by at most 15%.
- The score is composed to the session arc: sparse under the prompt, denser under tool calls, resolving on the green test run; the mix ducks 6dB under any typed text sound.
- Banned: showing real file contents or secrets from the log, captions over 8 words, and any still frame held longer than 2s.

## Facts stated by the source (rewritten in our words)
- Distributed as an installable skill rather than a single prompt.
- It reads the user's local Claude Code history and picks a representative session as the story material.
- The output is a short animated film with its own musical score, rendered through HyperFrames.
- The creator tagged it under characters and code.

## Assumptions
The source states only the pipeline (local history in, scored HyperFrames film out); the two-character cast, the 45s length, the stepped-animation look and the scene order are proposed directions, not observed facts.

## Keywords
claude code, session replay, agent story, hyperframes, terminal animation, code montage, character animation, قصة برمجية, وكيل ذكاء اصطناعي, شخصيات كرتونية, سجل الجلسة, موسيقى تصويرية, مونتاج كود
