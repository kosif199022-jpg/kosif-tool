# بارالاكس — صورة مقطّعة إلى طبقات تتحرك بعمق — بارالاكس

> ريل عمودي 9:16 تتحول فيه صور ثابتة إلى مشاهد ذات عمق: كل صورة مقطّعة إلى ثلاث أو أربع طبقات (مقدمة وشخص وخلفية وسماء) تنزلق بسرعات مختلفة مع دفع بطيء للكاميرا، وضباب وجزيئات غبار بين الطبقات، وانتقالات تمر فيها الكاميرا عبر طبقة المقدمة إلى الصورة التالية.
>
> A 9:16 reel that turns still photos into scenes with depth: each image is cut into three or four layers (foreground, subject, background, sky) that slide at different speeds under a slow camera push, with haze and dust particles between layers, and transitions where the camera passes through the foreground layer into the next picture.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: photos, 3d
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 27 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS, HTML Canvas

## الفكرة
ذكريات وصور قديمة أو صور منتج تعود للحياة دون تصوير جديد: نفصل الشخص عن الخلفية ونملأ ما خلفه، ثم نحرك الطبقات بفروق سرعة صغيرة فيشعر المشاهد بعمق حقيقي. القوة في الهدوء: حركة بطيئة مستمرة، ونص قليل، ومشاعر حنين أو فخامة.

## Concept
Memories, old photos or product shots come alive without new filming: the subject is separated from the background, the gap behind it is filled, then the layers move with small speed differences so the viewer feels real depth. Its strength is calm: slow continuous motion, little text, and a feeling of nostalgia or luxury.

## المشاهد المقترحة
- 0-4 ث: الصورة الأولى: السماء تنجرف ببطء، والخلفية بسرعة 0.3، والشخص 0.6، والمقدمة 1، بينما تقترب الكاميرا 8٪ خلال 4 ث.
- 4-5 ث: انتقال عبر الطبقة: تتسارع الكاميرا داخل عنصر داكن في المقدمة (باب أو ورقة شجر أو كتف) يملأ الإطار فتظهر الصورة الثانية خلفه.
- 5-10 ث: الصورة الثانية: انزلاق جانبي من اليمين لليسار مع انفصال الطبقات؛ وجزيئات غبار تطفو بين الشخص والخلفية.
- 10-15 ث: الصورة الثالثة: صعود رأسي من الأرض إلى السماء؛ والعنوان على طبقة وسطى تحجبه المقدمة جزئياً.
- 15-22 ث: الصورتان الرابعة والخامسة على نبضات أسرع (3 ث) بنفس الانتقالات عبر الطبقة مع الموسيقى.
- 22-27 ث: الصورة الأخيرة: ابتعاد بطيء، تتقارب الطبقات حتى تبدو مسطحة، يرتفع ضباب دافئ ويظهر سطر الختام.

## Proposed scenes
- 0-4s: First photo: sky drifts slowly, background at 0.3x, subject at 0.6x, foreground at 1x speed as the camera pushes in 8% over 4 s.
- 4-5s: Through-transition: the camera accelerates into a dark foreground element (a doorway, leaf or shoulder) that fills the frame, revealing photo two behind it.
- 5-10s: Photo two: a lateral truck right-to-left with layers separating; dust particles float between subject and background.
- 10-15s: Photo three: a vertical crane up from ground to sky; title text sits on a middle layer, partly hidden by the foreground.
- 15-22s: Photos four and five on faster 3 s beats with the same through-transitions on the music.
- 22-27s: Final photo: slow pull-out, layers converge to flat, warm haze rises and the closing line fades in.

## قواعد الحركة
- 3-4 طبقات لكل صورة بنسب سرعة تقريبية 0.15 (السماء) و0.3 (الخلفية) و0.6 (الشخص) و1.0 (المقدمة)؛ وتُكبر المقدمة 1.1 لإخفاء الحواف.
- حركة الكاميرا مستمرة وبطيئة (6-10٪ خلال اللقطة) بتسارع خطي أو ناعم جداً؛ ولا تتوقف فجأة داخل اللقطة.
- حواف الشخص بنعومة 1-2 بكسل مع ملء الخلفية خلفه حتى لا تظهر فجوات عند انفصال الطبقات.
- الأجواء: طبقة ضباب (#f4e3c8 بشفافية 10-20٪) بين الخلفية والشخص، و20-60 جزيء غبار ناعم، وتلوين دافئ لطيف.
- النص: خط عربي أنيق (نوتو كوفي عربي 500 أو أميري للمحتوى العاطفي)، أبيض #fffaf2 بظل ناعم، على طبقة وسطى ليشارك في العمق.
- الطبقات تنتقل وتكبر فقط؛ بلا دوران ولا تشويه منظور (فهذا من أسلوب الثلاثي الأبعاد المزيف).
- الفرق عن الثلاثي الأبعاد المزيف والسينمائي ثلاثي الأبعاد: مستويات ثنائية مسطحة من صور، والعمق من فرق السرعة فقط.

## Motion rules
- 3-4 layers per image with speed ratios about 0.15 (sky), 0.3 (background), 0.6 (subject), 1.0 (foreground); scale foreground 1.1x to hide edges.
- Camera moves are continuous and slow (6-10% over a shot) with linear or very soft easing; never stop dead inside a shot.
- Subject edges get a 1-2 px feather and inpainted background behind them so no holes show when layers separate.
- Atmosphere: a haze layer (#f4e3c8 at 10-20%) between background and subject, 20-60 soft dust particles; a gentle warm grade.
- Text: elegant Arabic (Noto Kufi Arabic 500 or Amiri for emotional pieces), white #fffaf2 with soft shadow, placed on a middle layer so it shares the depth.
- Layers translate and scale only; no rotation or perspective warping (that belongs to fake3d).
- Different from fake3d and cinematic-3d: flat 2D planes from photos, depth only from speed differences.

## Facts stated by the source (rewritten in our words)
- Catalogued as a KOSIF original style named parallax, in the Photos and 3D categories.

## Assumptions
Authored KOSIF definition, not an observed reference: there is no reference video for this base style (its page is the KOSIF repo root), so palette hex values, type choices, timings and scene beats are original KOSIF design decisions, not measurements. Assumed 5-6 user photos per reel of about 27 s; layer cut-outs and background fill are prepared beforehand.

## Keywords
parallax, 2.5d photo, layered photo, depth, ken burns, nostalgia, photo animation, بارالاكس, طبقات, عمق, صور متحركة, ذكريات, تحريك الصور
