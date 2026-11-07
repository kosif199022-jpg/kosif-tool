# جولة مقربة في صفحة مستودع كود تعرض مهارة لرسم المخططات — Diagram Design: 44 kinds of diagrams

> تسجيل شاشة مكبّر مدته 26 ثانية لصفحة مستودع على منصة كود بخلفية بيضاء: الكاميرا تقترب من اسم المستودع وتظلله، تنزلق إلى عدد النجوم، تبتعد لتعرض الصفحة كاملة، ثم تنزل إلى ملف التعريف بغلاف تحريري ومعرض لأنواع المخططات وجدول مقارنة وأوامر تثبيت، مع ضبابية حركة في التمرير وشارة اسم الناشر أسفل اليمين طوال الوقت.
>
> A 26-second zoomed screen walkthrough of a code-hosting repository page on white: the camera pushes in to highlight the repo name, slides to the star count, pulls back to the whole page, then scrolls the README past an editorial cover, a diagram-type gallery, a comparison table and install commands, with a handle badge bottom-right.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/kirillk-web3-af21f3
- التصنيفات / Categories: product-ui, diagrams, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 26 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
الفكرة إعلان بسيط لأداة مفتوحة المصدر بلا تصميم إضافي: الصفحة الحقيقية هي المحتوى، والكاميرا تصنع القصة بالاقتراب مما يهم (الاسم، الشعبية، الوصف، أمثلة المخرجات، المقارنة، التثبيت). أسلوب «زووم على تسجيل الشاشة» الشائع في منشورات التقنية، مع تظليل نص كأن أحداً يحدده بالفأرة.

## Concept
The idea is a plain promo for an open-source tool with no added design: the real page is the content, and the camera makes the story by moving in on what matters (the name, the popularity, the description, sample outputs, the comparison, installation). It is the familiar 'zoom on a screen recording' style of tech posts, with text selection highlights as if someone dragged the mouse over it.

## المشاهد المقترحة
- 0-1.5 ث: لقطة قريبة على رأس المستودع: المؤشر يحدد اسم المستودع فيظلل بالأزرق.
- 1.5-3.5 ث: الكاميرا تنساب يميناً إلى أزرار الرأس، والمؤشر يمر فوق عدد النسخ والنجوم.
- 3.5-5.5 ث: انسياب لأسفل في لوحة التعريف: الوصف والرابط وشارات المواضيع؛ ويُحدد رقم النجوم.
- 5.5-8 ث: ابتعاد إلى الصفحة كاملة داخل نافذة المتصفح، ثم تمرير لأسفل عبر قائمة الملفات.
- 8-12 ث: غلاف ملف التعريف: عنوان كبير بخط مذيل فوق رسم متساوي القياس، ثم بطاقة معرض تعرض عدد أنواع المخططات في صور مصغرة.
- 12-17 ث: تمرير بضبابية عبر أمثلة الاستخدام وأوامر التثبيت؛ والكاميرا تميل نحو زر النسخ.
- 17-20 ث: جدول مقارنة بين ثلاث طرق يُقرأ صفاً صفاً مع نزول المؤشر.
- 20-26 ث: شبكة صور مصغرة لمخططات مسماة تمر، ثم فقرات كثيفة وتذييل الصفحة بينما تبتعد الكاميرا إلى إطار المتصفح.

## Proposed scenes
- 0-1.5s: Close on the repo header: the cursor selects the repo name, which turns blue-highlighted.
- 1.5-3.5s: The camera pans right to the header actions and the cursor hovers the fork and star counts.
- 3.5-5.5s: Pan down the about panel: description, link, topic chips; the star count text gets selected.
- 5.5-8s: Pull back to the full page in the browser window, then scroll down past the file list.
- 8-12s: The README cover: a large serif title over an isometric sketch, then a gallery card showing a count of diagram types in thumbnails.
- 12-17s: Scroll with blur through usage examples and install commands; the camera nudges toward a copy button.
- 17-20s: A comparison table of three approaches, read row by row as the cursor moves down.
- 20-26s: A grid of named diagram thumbnails scrolls past, then dense paragraphs and the page footer as the camera drifts out to the browser frame.

## قواعد الحركة
- كاميرا افتراضية فوق صفحة مسجلة: تكبير بين نحو 1x و2.5x مع انسياب ناعم يستغرق 1-2 ث، وإبقاء منطقة الاهتمام قرب المركز.
- التمرير السريع يحصل على ضبابية حركة عمودية لمدة 2-4 إطارات؛ والقراءة البطيئة بلا ضبابية.
- الإبراز بتحديد النص الأصلي (أزرق فاتح #b6d4fe خلف النص) ومؤشر ظاهر، لا برسوم مضافة.
- شارة ثابتة أسفل اليمين: كبسولة داكنة مستديرة #1f1f1f بصورة رمزية صغيرة واسم الناشر بالأبيض.
- الألوان ألوان الصفحة نفسها: أبيض #ffffff، حدود رمادية فاتحة #d0d7de، نص #1f2328، أزرق روابط #0969da، زر أخضر #1f883d؛ وغلاف ملف التعريف أبيض دافئ #f5f3ee بعنوان أسود مذيل.
- لا قطعات على الموسيقى: لقطة واحدة متصلة مع ابتعاد قصير واحد، نحو 26 ث إجمالاً.

## Motion rules
- Virtual camera over a recorded page: zoom between about 1x and 2.5x with eased pans of 1-2 s, keeping the area of interest near centre.
- Fast scrolls get vertical motion blur for 2-4 frames; slow reads have none.
- Emphasis is native text selection (light blue #b6d4fe behind the text) and a visible cursor, not drawn overlays.
- Persistent badge bottom-right: a dark rounded pill #1f1f1f with a small avatar and the poster's handle in white.
- Palette is the page's own: white #ffffff, light grey borders #d0d7de, text #1f2328, link blue #0969da, green action button #1f883d; the README cover is a warm off-white #f5f3ee with a black serif title.
- No music-driven cuts: one continuous shot with a single brief pull-back, about 26 s total.

## Facts stated by the source (rewritten in our words)
- The source presents an agent skill that produces many kinds of editorial diagrams as self-contained HTML and SVG.
- It is listed as a skill rather than a prompt, with HTML and SVG named as tech.

## Assumptions
Observed from 24 frames sampled every ~1.1 s: the repo-name selection, the star-count hover, the pull-back, the README cover, the diagram gallery, the install section, the comparison table and the closing scroll over 26 s, with a handle badge throughout. An audio track is present (mean about -14 dB) but was not listened to. Assumed: the zooms are added in post over a plain recording. The diagram outputs themselves are only seen as small thumbnails, so this brief describes the promo video, not the diagram style.

## Keywords
screen recording, zoom pan, repository page, README tour, diagram tool, open source, text selection, motion blur, تسجيل شاشة, تكبير وانسياب, صفحة مستودع, أداة مخططات, مفتوح المصدر, تحديد النص
