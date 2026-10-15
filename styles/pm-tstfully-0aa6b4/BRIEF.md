# إعلان منتج: من رابط يوتيوب إلى نص كامل — YouTube transcript product ad

> إعلان أفقي مدته 15 ثانية يشرح أداة تحوّل رابط فيديو يوتيوب إلى نصّ مفرّغ كامل، مع عدّادات ومخططات تلخّص النتيجة.
>
> A 15 s landscape product ad for a tool that turns a pasted YouTube link into a full transcript, closing with counters and small charts that quantify the result.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/tstfully-0aa6b4
- التصنيفات / Categories: product-ui, charts
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع أداة تفريغ: يلصق المستخدم رابط فيديو فيحصل على كل كلمة قيلت فيه. الهدف إثبات أن العملية بثلاث خطوات (لصق، معالجة، تنزيل) وأن النص دقيق ومنظّم بطوابع زمنية. اللغة الحركية تتبع تدفق البيانات نفسه: الرابط يتحول إلى بطاقة فيديو، والموجة الصوتية تتحول إلى أسطر نص تتدفق بترتيب، ثم تتكثف الأسطر إلى أرقام ومخططات صغيرة تُقاس بها القيمة.

## Concept
The subject is a transcription tool: paste a video link, receive every spoken word. The goal is to prove a three-step flow (paste, process, download) and that the text is accurate and time-stamped. The motion language follows the data itself: the link morphs into a video card, the waveform turns into cascading text lines, and the lines condense into counters and small charts that measure the value.

## المشاهد المقترحة
- 0-2ث: حقل إدخال عريض على خلفية داكنة؛ يومض المؤشر كل 500 مللي ثانية، ثم ينزلق نص الرابط من أيقونة الحافظة خلال 300 مللي ثانية ويومض الحقل مرة واحدة.
- 2-5ث: يتحوّل الحقل إلى بطاقة صورة مصغّرة للفيديو (تدرّج في نصف القطر والعرض خلال 450 مللي ثانية، easeInOutCubic)؛ شريط موجة صوتية يتدحرج تحته بسرعة 120 بكسل في الثانية.
- 5-9ث: شلال النص: أسطر تسقط في عمود أيمن بتأخير 60 مللي ثانية، طوابع زمنية تتزايد على اليسار، وكلمة مميّزة واحدة تنتقل عبر النص بأسلوب الكاريوكي.
- 9-12ث: لحظة الأرقام: عدّاد يصل إلى إجمالي الكلمات خلال 1400 مللي ثانية (easeOutExpo)، مخطط من أربعة أعمدة للكلمات في الدقيقة ينمو من خط الأساس، وحلقة دائرية تمتلئ بنسبة اللغة المكتشفة.
- 12-15ث: أزرار التصدير (TXT وSRT ونسخ) تظهر بتأخير 80 مللي ثانية بينها، يهبط الشعار النصي بكلمتين، ويستقر الشعار أسفل اليمين.

## Proposed scenes
- 0-2s: A wide input field sits on a dark stage; a cursor blinks at 500 ms intervals, then a link string slides in from a clipboard icon over 300 ms and the field flashes once.
- 2-5s: The field morphs into a video thumbnail card (border-radius and width tween, 450 ms, easeInOutCubic); a waveform strip scrolls beneath it at 120 px per second.
- 5-9s: Transcript cascade: text lines fall into a right-hand column with 60 ms stagger, timestamps count up on the left, and a single highlighted word travels through the text karaoke-style.
- 9-12s: Numbers moment: a counter rolls to the total word count over 1400 ms (easeOutExpo), a four-bar chart of words per minute grows from the baseline, and a doughnut ring fills to the detected language share.
- 12-15s: Export buttons (TXT, SRT, copy) pop in with 80 ms stagger, the tagline lands in two words, and the logo settles bottom-right.

## قواعد الحركة
- تدرّجات الواجهة تستخدم cubic-bezier(0.22, 1, 0.36, 1) بين 300 و450 مللي ثانية؛ أسطر النص تدخل خلال 220 مللي ثانية بإزاحة عمودية 12 بكسل وتأخير 60 مللي ثانية، ولا أسرع من ذلك.
- العدّادات وأعمدة المخطط تستخدم easeOutExpo خلال 1200 إلى 1400 مللي ثانية وتبدأ معًا في الإطار نفسه لتُقرأ الأرقام كحدث واحد.
- الكاميرا: تأطير ثابت 1280×720 مع دفعة اقتراب واحدة 4 بالمئة أثناء شلال النص (5-9ث)؛ لا دوران ولا ثلاثي الأبعاد.
- الانتقالات بين المشاهد تحوّلات للعنصر نفسه (حقل إلى بطاقة، بطاقة إلى عمود) لا قطعات؛ القطع مسموح فقط قبل الشعار الختامي.
- الطباعة: أسطر النص المفرّغ بخط sans مقروء لا يقل عن 28 بكسل؛ الكلمة النشطة تغيّر لونها فقط ولا تغيّر حجمها.
- اللون: قاعدة داكنة ونص فاتح ولون تمييز واحد محجوز للكلمة النشطة وتعبئة المخططات وزر الدعوة؛ الصور المصغّرة تبقى باهتة ليتقدّم تصميم الواجهة.
- ممنوع: اهتزاز الغليتش، رجّ الشاشة، نسب دقة مختلقة تُعرض كحقائق، وأكثر من كلمة مميّزة واحدة في الوقت نفسه.

## Motion rules
- UI tweens use cubic-bezier(0.22, 1, 0.36, 1) at 300 to 450 ms; text lines enter at 220 ms with a 12 px vertical offset and 60 ms stagger, never faster.
- Counters and chart bars use easeOutExpo over 1200 to 1400 ms and start together on the same frame so the numbers read as one event.
- Camera: static 1280x720 framing with one 4 percent push-in during the transcript cascade (5-9 s); no rotation, no 3D.
- Scene transitions are morphs of the same element (field to card, card to column), not cuts; a cut is allowed only before the final logo.
- Typography: transcript lines in a readable sans at 28 px minimum; the active karaoke word changes colour only, never size.
- Colour: dark base, light text, one accent reserved for the active word, the chart fills and the CTA; thumbnails stay desaturated so the UI leads.
- Banned: glitch jitter, screen shake, fake accuracy percentages presented as fact, and more than one highlighted word at a time.

## Facts stated by the source (rewritten in our words)
- The requested piece is a motion-graphics product advertisement of fifteen seconds.
- The product promise is that pasting a YouTube video link returns the complete spoken text.
- The listing tags it as product UI plus charts and lists a 1280x720 frame.

## Assumptions
The three-step structure, the karaoke highlight and the closing stats are proposed; the source states only the 15 s length and the paste-link-get-words promise.

## Keywords
تفريغ صوتي, رابط فيديو, نص مفرّغ, طوابع زمنية, كاريوكي, عدّاد, transcript, youtube link, waveform, word highlight, counter, bar chart, export srt, product ad
