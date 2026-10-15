# ريل المصمم المبني من سياق المشروع — Motion designer showreel

> ريل 15 ثانية يستمد محتواه من ملفات المشروع نفسه: شجرة المجلدات تصبح رسمًا بيانيًا، وأسماء المكوّنات تصبح تايبوغرافي حركيًا.
>
> A 15-second reel whose content is mined from the project itself: the folder tree becomes a chart and component names become kinetic type.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/danilowm-d3720d
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع ريل تعريفي يُثبت قدرة المصمم عبر تحويل المشروع الحقيقي إلى مادة بصرية بدل استخدام محتوى عام. الهدف أن يرى المشاهد في 15 ثانية مهارات الطباعة والرسوم البيانية والانتقالات وهي تعمل على بيانات حقيقية: عدد الأسطر، وأسماء الوحدات، وخط زمني للـ commits. ما يميز اللغة الحركية هو الانتقال المتواصل من واجهة الطرفية إلى تصميم عرض كبير، مع ثلاث مسارات تايبوغرافية متوازية بسرعات مختلفة تمنح الإطار عمقًا دون 3D.

## Concept
The subject is a résumé reel that proves the designer's range by turning the real project into visual material instead of generic content. The goal is to let a viewer watch typography, charts and transitions operate on real data within 15 seconds: line counts, module names and a commit timeline. The distinctive motion language is a continuous shift from terminal UI into large display design, with three parallel type lanes moving at different speeds to give depth without 3D.

## المشاهد المقترحة
- 0-2 ث: مؤشر بأسلوب الطرفية يكتب اسم المشروع؛ النص يقفز إلى خط عرض بحجم 160 px بينما تنقلب الخلفية من الداكن إلى محايد دافئ.
- 2-5 ث: شجرة مجلدات المشروع تتكشف كخطوط متداخلة؛ عدد أسطر كل مجلد يمتد إلى رسم أعمدة أفقي وتعدّ القيم تصاعديًا خلال 600 ms.
- 5-8 ث: أسماء المكوّنات أو الوحدات تطير كتايبوغرافي حركي على ثلاث مسارات متدرجة، كل مسار بسرعة مختلفة (نسبة parallax 1 : 0.7 : 0.45).
- 8-11 ث: خط زمني للـ commits يُرسم من اليسار إلى اليمين كرسم خطي بست إلى ثماني نقاط؛ تظهر تسميات بالتاريخ وملخص من كلمة واحدة.
- 11-13 ث: المسارات الثلاثة والأعمدة والخط تتجمع في بلاطة مربعة واحدة تدور 90° لتصبح monogram المصمم.
- 13-15 ث: الاسم واللقب وجملة تعريف واحدة تنزلق تحت الـ monogram، وشريط تقدم رفيع يكمل الإطار.

## Proposed scenes
- 0-2s: A terminal-style cursor types the project name; the text snaps to a 160 px display face as the background flips from dark to a warm neutral.
- 2-5s: The project folder tree unfolds as nested lines; each folder's line count extrudes into a horizontal bar chart with values counting up over 600 ms.
- 5-8s: Component or module names fly in as kinetic type on three staggered lanes, each lane scrolling at a different speed (parallax ratio 1 : 0.7 : 0.45).
- 8-11s: A commit timeline draws left to right as a line chart with 6-8 node dots; labels pop with the date and a one-word summary.
- 11-13s: The three lanes, the bars and the line converge into a single square tile that rotates 90° and becomes the designer's monogram.
- 13-15s: Name, title and a one-line pitch slide in beneath the monogram, and a thin progress bar completes the frame.

## قواعد الحركة
- الدخول بـ cubic-bezier(0.16, 1, 0.3, 1) خلال 700 ms؛ عناصر القوائم بتفاوت 50 ms؛ الخروج تلاشٍ 300 ms مع انزياح 20 px.
- كتابة الطرفية بسرعة 40 ms لكل حرف مع مؤشر يومض كل 500 ms؛ القفزة إلى خط العرض قفزة تكبير واحدة 250 ms وليست crossfade.
- مسارات الـ parallax تتحرك بنسبة سرعات 1 : 0.7 : 0.45 ولا تتوقف في منتصف كلمة؛ الكلمات المغادرة تتلاشى في آخر 120 px.
- قيم رسم الأعمدة تعدّ تصاعديًا خلال 600 ms بأرقام جدولية؛ خط الـ commits يُرسم خلال 900 ms وتظهر كل عقدة بتكبير من 0 إلى 1 خلال 150 ms.
- الكاميرا: دفعة بطيئة واحدة من 1.0 إلى 1.06 على مدى 15 ثانية؛ لا حركات كاميرا أخرى ولا دوران سوى دوران البلاطة 90°.
- اللوحة: لونان محايدان ولون تمييز واحد مأخوذ من هوية المشروع نفسها؛ بيانات الـ monospace تبقى محايدة، وخط العرض يستعمل التمييز في المقطع الأخير فقط.
- الطباعة: خط عرض واحد للأسماء والعناوين، وخط monospace واحد لكل البيانات؛ خط العرض لا يقل عن 96 px والـ monospace لا يقل عن 28 px.
- ممنوع: لقطات الأرشيف، وتصييرات 3D عامة، وتأثيرات glitch لا علاقة لها بالمشروع، وأي رقم غير مستخرج من المستودع الفعلي.

## Motion rules
- Entrances use cubic-bezier(0.16, 1, 0.3, 1) over 700 ms; list items stagger by 50 ms; exits are 300 ms fades combined with a 20 px drift.
- Terminal typing runs at 40 ms per character with a 500 ms blinking cursor; the jump to display type is a single 250 ms scale snap, not a crossfade.
- Parallax lanes scroll at a 1 : 0.7 : 0.45 speed ratio and never stop mid-word; words leaving a lane fade over the last 120 px.
- Bar chart values count up over 600 ms with tabular figures; the commit line draws over 900 ms and each node pops with a 150 ms scale from 0 to 1.
- Camera: a single slow push-in from 1.0 to 1.06 across the full 15 s; no other camera moves and no rotation except the 90° tile turn.
- Palette: two neutrals plus one accent taken from the project's own brand colour; monospace data stays neutral, display type uses the accent only on the final beat.
- Typography: one display face for names and titles, one monospace face for all data; display never below 96 px, monospace never below 28 px.
- Banned: stock footage, generic 3D renders, glitch effects unrelated to the project, and any number not derived from the real repository.

## Facts stated by the source (rewritten in our words)
- A fast 15-second résumé-style reel was requested.
- The request was issued through a /hyperframes command and ends with a Portuguese instruction to draw on the whole project's context.
- Catalogued as charts and kinetic type; no colours, scenes or stack are given.

## Assumptions
The idea of mining file trees, module names and commit history as content is a proposal built on the instruction to use project context; the actual project, its colour and its data were not seen.

## Keywords
showreel, project context, terminal typing, folder tree chart, commit timeline, parallax lanes, monogram, kinetic type, ريل مصمم, سياق المشروع, خط زمني, رسم أعمدة, طباعة حركية
