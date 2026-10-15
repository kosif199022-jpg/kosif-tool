# برومو Nohandslabs: العمل يمضي بلا أيدٍ — Nohandslabs brand promo

> برومو 15 ثانية لعلامة Nohandslabs يستعمل زوج أيدٍ يترك المهام فتكمل نفسها، مع رسوم بيانية للوقت المستعاد.
>
> A 15-second brand promo for Nohandslabs where a pair of hands lets go and the work keeps running on its own, backed by reclaimed-time charts.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/robvjourney-ce3e1a
- التصنيفات / Categories: charts
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع برومو لعلامة تحمل اسمًا يوحي بالأتمتة الكاملة، والهدف إقناع المشاهد في 15 ثانية بأن المنتج يُنجز المهام دون تدخل بشري. اللغة الحركية تقوم على استعارة واحدة متكررة: يدان مرسومتان بخط رفيع تمسكان بشيء ثم تتركانه، فيستمر في الحركة وحده. تُدعم الاستعارة برسوم بيانية تنمو من الصفر وتُقرأ بسرعة: أعمدة للساعات المستعادة وحلقة نسبة للمهام المؤتمتة، كي يحمل الإطار دليلًا رقميًا لا شعارًا فقط.

## Concept
The subject is a promo for a brand whose name implies full automation, and the goal is to convince the viewer within 15 seconds that the product completes tasks without human intervention. The motion language rests on one recurring metaphor: two thin-outlined hands hold something, release it, and it keeps moving by itself. The metaphor is backed by charts that grow from zero and read instantly, bars for hours reclaimed and a ring for automated tasks, so the frame carries numeric proof rather than only a slogan.

## المشاهد المقترحة
- 0-2 ث: يدان مرسومتان بخط رفيع تدخلان من حافتي الإطار وتحملان بطاقة مهمة مضيئة؛ تتركانها وتنسحبان، فتواصل البطاقة حركتها وحدها.
- 2-5 ث: البطاقة تتضاعف إلى شبكة من 12 بطاقة تعالج نفسها: كل بطاقة تنقلب من 'للتنفيذ' إلى علامة صح بتتابع 90 ms.
- 5-8 ث: رسم أعمدة عمودي لـ'الساعات المستعادة أسبوعيًا' يرتفع من الصفر؛ الأعمدة تنمو بـ ease-out بينما يصعد عدّاد بجانبها إلى القيمة النهائية.
- 8-11 ث: شعار NOHANDSLABS الكتابي يتجمع حرفًا حرفًا من شظايا البطاقات؛ الحروف تستقر بنابض خفيف.
- 11-13 ث: حلقة donut تمتلئ حتى المقياس الرئيسي (مثل 'المهام المنجزة آليًا') خلال 800 ms، مع نسبة مئوية تعدّ بخط monospace.
- 13-15 ث: الشعار النصي والرابط يظهران؛ اليدان تعودان لحظة عند الحواف بإيماءة إعجاب ثم تخرجان.

## Proposed scenes
- 0-2s: Two outlined hands enter from the frame edges holding a glowing task card; they release it and withdraw, and the card keeps moving on its own.
- 2-5s: The card multiplies into a grid of 12 task cards that process themselves: each flips from 'to do' to a checkmark on a 90 ms cascade.
- 5-8s: A vertical bar chart of 'hours reclaimed per week' rises from zero; bars grow with ease-out while a counter beside them climbs to the final value.
- 8-11s: The wordmark NOHANDSLABS assembles letter by letter from the card fragments; the letters settle with a light spring.
- 11-13s: A donut ring fills to the key metric (e.g. 'tasks handled automatically') in 800 ms, with the percentage counting up in a monospace face.
- 13-15s: Tagline and URL fade up; the hands reappear briefly at the edges, give a thumbs-up gesture, and exit.

## قواعد الحركة
- اليدان تتحركان بـ cubic-bezier(0.33, 1, 0.68, 1) خلال 900 ms؛ لحظة الترك توقف 120 ms ثم تواصل البطاقة بسرعة خطية كي يُقرأ التسليم بوضوح.
- انقلاب البطاقات rotateY بمقدار 180° خلال 350 ms بتتابع 90 ms عبر شبكة الـ 12 بطاقة؛ لا تنقلب بطاقة قبل جارتها اليسرى.
- الرسوم البيانية تبدأ من الصفر وتتحرك خلال 700 ms بـ ease-out؛ العدّادات بأرقام monospace جدولية وتنتهي بعد 100 ms من العمود الذي تصفه.
- حروف الشعار تتجمع بنابض (stiffness 160 وdamping 15) وتفاوت 60 ms؛ يستقر الحرف الأخير قبل دخول أي عنصر جديد.
- الكاميرا ثابتة؛ العمق يوحى به فقط بـ parallax من طبقتين (شبكة الخلفية بسرعة 0.5) وبتكبير شبكة البطاقات من 0.92 إلى 1.0 عند الوصول.
- اللوحة: أساس داكن، وخطوط بيضاء لليدين، ولون تمييز واحد للبطاقات النشطة وتعبئة الرسوم؛ لا تتجاوز تغطية التمييز 25% من الإطار.
- الطباعة: sans هندسي عريض للشعار بحجم 140 px، وmonospace بحجم 32 px للمقاييس؛ نص العنوان لا يتجاوز ست كلمات في الإطار.
- ممنوع: أيدٍ واقعية فوتوغرافية، وصور روبوتات عامة، وإحصاءات مختلقة دون وسم 'عينة'، وأي مقطع يتجاوز 3 ثوانٍ دون تغيير مرئي.

## Motion rules
- Hands move on cubic-bezier(0.33, 1, 0.68, 1) over 900 ms; the release moment is a 120 ms hold followed by the card continuing at linear velocity, so the hand-off reads clearly.
- Card flips are rotateY 180° over 350 ms with a 90 ms cascade across the 12-card grid; no card flips before its left neighbour.
- Charts start at zero and animate over 700 ms with ease-out; counters use tabular monospace figures and finish 100 ms after the bar they describe.
- Wordmark letters assemble with a spring (stiffness 160, damping 15) and a 60 ms stagger; the final letter settles before any new element enters.
- Camera is locked; depth is suggested only by a 2-layer parallax (background grid at 0.5 speed) and by the card grid scaling 0.92 to 1.0 on arrival.
- Palette: a dark base, white line-art for the hands, one accent for active cards and chart fills; accent coverage never exceeds 25% of the frame.
- Typography: wide geometric sans for the wordmark at 140 px, monospace at 32 px for metrics; headline copy is never more than six words per frame.
- Banned: photoreal hands, generic robot imagery, invented statistics presented without a 'sample' label, and any beat longer than 3 s without a visible change.

## Facts stated by the source (rewritten in our words)
- A 15-second motion piece was requested about a website reached through a shortened link.
- The creator wanted the most ambitious execution available, using every technique on hand.
- Catalogued under charts; the text gives no scenes, colours, stack or product details.

## Assumptions
The hands-free automation theme, the metrics and the task-card motif are inferred from the brand name alone; the linked site was not inspected, so product facts must be substituted before production.

## Keywords
brand promo, automation, hands-free, task cards, bar chart, donut chart, wordmark assembly, line-art hands, برومو علامة, أتمتة, بطاقات مهام, رسم بياني, شعار متحرك
