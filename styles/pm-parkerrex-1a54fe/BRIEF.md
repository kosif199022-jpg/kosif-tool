# شرح محدد المعدل بدلو الرموز بلوحة طرفية حية — Token bucket rate limiter

> مخطط مربع صامت مدته 18 ثانية بأسلوب الطرفية الداكنة يشرح محدد المعدل بدلو الرموز: دلو من عشر خانات زرقاء بجانب رقم ضخم للرموز المتبقية وسجل طلبات يتدحرج (مأخوذ بالأخضر، مرفوض بالأحمر)، ومخطط درجات أسفلها يرسم مستوى الدلو مع علامات الطلبات على خط زمني 12 ثانية، عبر أربع مراحل: حركة ثابتة، اندفاع يفرغه، رفض حتى يمتلئ، ثم تعافٍ وخلاصة.
>
> A silent 18-second square terminal-style diagram of a token-bucket rate limiter: a ten-slot blue bucket beside a huge remaining-token number and a scrolling request log (green 'taken', red 'refused'), above a step chart tracing bucket level with request ticks on a 12 s axis, through four phases: steady traffic, a burst that drains it, refusals until refill, then recovery and the takeaway.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/parkerrex-1a54fe
- التصنيفات / Categories: diagrams, charts, code
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 18 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: HTML Canvas, React

## الفكرة
خوارزمية تُفهم بمشاهدتها تعمل. كل شيء على الشاشة يعرض الحالة نفسها من ثلاث زوايا متزامنة: الدلو كصورة، الرقم والسجل كنص، والمخطط كتاريخ. سطر عنوان واحد يتغير مع كل مرحلة ليقول ما يحدث، والنهاية سطر خلاصة بلون ذهبي.

## Concept
An algorithm understood by watching it run. Everything on screen shows the same state from three synchronised angles: the bucket as a picture, the number and log as text, and the chart as history. One caption line changes with each phase to say what is happening, and the ending is a takeaway line in gold.

## المشاهد المقترحة
- 0-2 ث: حركة ثابتة: دلو ممتلئ بعشرة أشرطة زرقاء و«10 / 10 رموز»، وأول طلبات بطيئة تُسجل مأخوذة؛ والمنحنى ينخفض قليلاً ثم يمتلئ، وعلامات خضراء تظهر على مسار الطلبات.
- 2-3 ث: اندفاع: يتغير العنوان، وتصل الطلبات في عنقود سريع، والخانات تفرغ من الأعلى خانة لكل طلب، والرقم يعد تنازلياً من 9 إلى 0 والخط يهبط بحدة.
- 3-6.5 ث: الدلو فارغ: الرقم يصير أحمر عند 0 وحد الدلو أحمر، والسجل يمتلئ بصفوف رفض حمراء تتخللها صفوف قبول خضراء كلما امتلأ رمز واحد وصُرف فوراً؛ وعلامات حمراء كثيفة على المسار.
- 6.5-11.5 ث: التعافي: الحركة تهدأ والعنوان يقول إن إعادة الملء تلحق؛ الرقم يصعد 2، 4، 5، 7، 8، 10 والخانات الزرقاء تمتلئ من الأسفل والمخطط يصعد درجاً حتى القمة.
- 11.5-18 ث: الخلاصة: العنوان يصير ذهبياً ويقول إن السعة تحدد الاندفاع ومعدل الملء يحدد الحد؛ والشاشة كلها تثبت والتاريخ كاملاً ظاهر.

## Proposed scenes
- 0-2s: Steady traffic: a full bucket of ten blue bars, '10 / 10 tokens', and the first slow requests logging as taken; the chart line dips slightly and refills, green ticks appear on the request lane.
- 2-3s: Burst: the caption switches, requests arrive in a rapid cluster, slots empty from the top one per request, the number counts down from 9 to 0 and the line drops steeply.
- 3-6.5s: Empty: the number turns red at 0, the bucket border turns red, the log fills with red refused rows interleaved with occasional green taken rows as single tokens refill and are spent at once; dense red ticks on the lane.
- 6.5-11.5s: Recovery: traffic eases, the caption says refill catches up; the number climbs 2, 4, 5, 7, 8, 10 as blue slots fill from the bottom and the chart steps up a staircase to the top.
- 11.5-18s: Takeaway: the caption turns gold and states that capacity sets the burst and refill rate sets the limit; the whole display holds still with the full history visible.

## قواعد الحركة
- اللوحة: خلفية #0d1117، خطوط اللوحة #30363d، نص رمادي #c9d1d9، رمادي خافت #6e7681، أزرق الرموز #58a6ff وخانة نصف فارغة #1f4a7a، أخضر القبول #3fb950، أحمر الرفض #f85149، وذهبي الخلاصة #e3b341.
- كل النصوص بخط أحادي واحد (شبيه JetBrains Mono): رأس وعنوان صغيران بحروف صغيرة، ورقم الرموز المتبقية بحجم نحو 120 بكسل مع لاحقة صغيرة «/ 10 رموز».
- تقودها محاكاة حقيقية بمعدل 30 إطاراً: سعة 10، ملء 2 في الثانية، وطلبات بأوقات محددة؛ وكل العروض تقرأ من الحالة نفسها بلا حركات مزيفة.
- الخانات تمتلئ من الأسفل وتفرغ من الأعلى؛ والخانة التي تمتلئ جزئياً تظهر بلون أغمق؛ والرقم يصير أحمر عند الصفر فقط.
- سجل الطلبات يحتفظ بآخر ستة صفوف ويتدحرج صفاً مع كل حدث؛ والمخطط يُرسم من اليسار إلى اليمين بمؤشر عمودي وعلامات خضراء وحمراء على مسار تحت المحور.
- لا قطعات ولا حركة كاميرا: تخطيط واحد ثابت طوال القطعة، والذي يتغير بين المراحل هو سطر العنوان فقط؛ بلا صوت.

## Motion rules
- Palette: background #0d1117, panel lines #30363d, text grey #c9d1d9, dim grey #6e7681, token blue #58a6ff with partially drained slot #1f4a7a, taken green #3fb950, refused red #f85149, takeaway gold #e3b341.
- All type in one monospace (JetBrains Mono-like): small lowercase header and caption, a ~120 px number for remaining tokens with a small '/ 10 tokens' suffix.
- Driven by a real simulation at 30 fps: capacity 10, refill 2 per second, timestamped requests; every view reads from the same state, no tweened fakes.
- Bucket slots fill bottom-up and drain top-down; a slot mid-refill shows a darker partial fill; the number turns red only at zero.
- The request log keeps the last six rows and scrolls up one row per event; the chart draws left to right with a vertical playhead and green/red ticks on a lane below the axis.
- No cuts, no camera moves: one locked layout for the whole piece, only the caption line changes between phases; no audio.

## Facts stated by the source (rewritten in our words)
- The subject is an animated explanation of how a token-bucket rate limiter works.
- The page lists Canvas as the technology and tags it under diagrams.

## Assumptions
Observed from 24 frames sampled every 0.75 s over 18 s: the locked layout, bucket, number, request log, step chart, four phase captions and gold takeaway. The file has no audio stream. Assumed: the exact request schedule beyond what the log showed, and that it is generated by a live simulation.

## Keywords
token bucket, rate limiter, algorithm visualisation, terminal UI, step chart, request log, simulation, monospace, محدد المعدل, دلو الرموز, شرح خوارزمية, محاكاة, مخطط, واجهة طرفية
