# لوحات كوميكس بحبر وتظليل نقطي وفقاعات حوار عربية — لوحات كوميكس

> ريل عمودي يُروى عبر صفحة كوميكس: إطارات بحدود حبر سوداء سميكة على ورق كريمي، تظليل نقطي بألوان CMYK باهتة، فقاعات حوار عربية تنفتح بالكلام، والكاميرا تنتقل من لوحة إلى أخرى داخل الصفحة نفسها.
>
> A vertical reel told across a comic-book page: thick black-ink panel borders on cream paper, faded CMYK halftone shading, Arabic speech balloons that pop open with each line, and a camera that glides panel to panel across the same page.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: characters, hand-drawn
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 30 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG, CSS

## الفكرة
القصة كلها صفحة كوميكس واحدة أو صفحتان، والكاميرا هي عين القارئ: تقفز من لوحة إلى التالية بترتيب القراءة العربي (من اليمين إلى اليسار ومن الأعلى إلى الأسفل). كل لوحة لقطة ثابتة تقريباً، والحياة تأتي من حركات صغيرة داخلها: فقاعة تنفتح، خطوط سرعة، مؤثر صوتي مرسوم يرتد، وظل نقطي يتحرك ببطء. يختلف عن الأنمي أكشن بأن الإيقاع إيقاع قراءة وليس قتال، وعن الدودل بأن الرسم مكتمل بالحبر والألوان من البداية ولا يُرسم أمامنا.

## Concept
The whole story is one or two comic pages and the camera is the reader's eye: it moves panel to panel in Arabic reading order (right to left, top to bottom). Each panel is nearly a still, and life comes from small moves inside it: a balloon opening, speed lines, a drawn sound effect bouncing, a halftone shadow drifting. It differs from anime-action because the rhythm is reading, not fighting, and from doodle because the art is fully inked and coloured from the start rather than drawn on screen.

## المشاهد المقترحة
- 0-3 ث: الافتتاح: الكاميرا قريبة على لوحة البطل؛ كلمة مؤثر صوتي ضخمة مرسومة تضرب الشاشة مع اهتزاز 3 إطارات، ثم تتراجع الكاميرا لتكشف شبكة الصفحة كلها.
- 3-9 ث: التمهيد: انزلاق إلى اللوحة العليا اليمنى؛ فقاعة الشخصية تنفتح من ذيلها (تكبير من 0 إلى 1.08 ثم 1 في 8 إطارات) والنص يظهر كلمة كلمة.
- 9-16 ث: التطور: لوحتان ضيقتان تُقرآن بالتتابع، لكل منهما صندوق تعليق في الزاوية العليا؛ ونقاط التظليل في الخلفية تنزلق ببطء لتوحي بالعمق.
- 16-24 ث: المنعطف: لوحة كبيرة تكسر حدود الشبكة؛ خطوط سرعة تنطلق من المركز وكلمة مؤثر ثانية تظهر مائلة.
- 24-30 ث: الخاتمة: الكاميرا تستقر على اللوحة الأخيرة؛ مسح عبر الفاصل يغلق الصفحة كقلب ورقة، وتنتهي بغلاف عدد يحمل العنوان واسم صانع المحتوى.

## Proposed scenes
- 0-3s: Hook: the camera starts tight on one hero panel; a big drawn sound-effect word slams in with a 3-frame shake, then the camera pulls back to reveal the full page grid.
- 3-9s: Setup: glide into the top-right panel; the character's balloon pops from its tail (scale 0 to 1.08 to 1, 8 frames) and text appears word by word.
- 9-16s: Development: two narrow panels read in sequence, each with a caption box in the top corner; halftone dots in the background slide slowly to suggest depth.
- 16-24s: Turn: a splash panel breaks the grid border; speed lines radiate and a second sound-effect word pops at an angle.
- 24-30s: Payoff: the camera settles on the last panel; a gutter wipe closes the page like turning a sheet, ending on a title card styled as the issue cover with the creator's handle.

## قواعد الحركة
- الألوان: ورق #f4ecd8، حبر #111111، أحمر تظليل #d6453d، أصفر #f2c230، سماوي #2e8bc0؛ الألوان مزاحة قليلاً عن الحدود (2 بكسل) لإحساس الطباعة.
- حدود اللوحات حبر أسود بسمك 6-8 بكسل بحواف غير منتظمة كالتحبير اليدوي؛ والفواصل 18-24 بكسل بلون الورق.
- الكاميرا تنتقل من لوحة إلى لوحة بتسارع وتباطؤ في 14-18 إطاراً؛ ولا قطع إلا في لقطة الافتتاح.
- نص الفقاعات عربي من اليمين إلى اليسار بخط عريض مستدير (مثل Lalezar أو Baloo Bhaijaan 2) بحجم 44-56 بكسل؛ والكلمات تظهر كاملة ولا تُفصل حروفها.
- كلمات المؤثرات الصوتية بخط عربي عريض جداً بحد أسود 4 بكسل وظل؛ تظهر بارتداد 1.15 واهتزاز 2-3 إطارات.
- داخل اللوحة حركة صغيرة فقط: تباين عمق بين 2-3 طبقات، خطوط سرعة، رمش عين؛ والشخصيات تثبت على أوضاع رئيسية بدلاً من حركة كاملة.
- قلب الصفحة أو المسح عبر الفاصل (10-12 إطاراً) هو الانتقال الوحيد بين الصفحات.

## Motion rules
- Palette: paper #f4ecd8, ink #111111, halftone red #d6453d, yellow #f2c230, cyan #2e8bc0; colours sit slightly off-register (2 px) for a printed feel.
- Panel borders are 6-8 px black ink with uneven hand-inked edges; gutters 18-24 px of paper colour.
- Camera moves panel to panel with a 14-18 frame ease-in-out; it never cuts, except for the opening hook.
- Arabic balloon text is RTL in a bold rounded Arabic face (e.g. Lalezar or Baloo Bhaijaan 2) at 44-56 px; words appear whole, never split letters.
- Sound-effect words: heavy display Arabic with a 4 px black outline and drop shadow; pop with overshoot 1.15 and a 2-3 frame shake.
- Inside panels only small motion: parallax of 2-3 layers, speed lines, blinking eyes; characters hold key poses rather than animate fully.
- Page turn or gutter wipe (10-12 frames) is the only transition between pages.

## Facts stated by the source (rewritten in our words)
- KOSIF lists this as an original style named for comic panels, tagged characters and hand-drawn.

## Assumptions
Authored KOSIF definition, not an observed reference: the record points only to the repo root, so there was no video to watch. Palette hex values, fonts, timings and scene beats are design choices written for this style, not measurements.

## Keywords
comics, comic panels, halftone, speech balloon, sound effect, page layout, graphic novel, كوميكس, قصص مصورة, فقاعة حوار, تظليل نقطي, لوحات, رسم بالحبر
