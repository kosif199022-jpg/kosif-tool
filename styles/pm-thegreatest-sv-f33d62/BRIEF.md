# لوحة واجهة سرية لدماغ آلي: صور متوهجة ونوافذ تقريب منبثقة — HyperFrames motion setup for Claude Code

> مقطع مدته نحو 25 ثانية لواجهة معلومات علمية خيالية بلون أبيض بارد مليئة بلوحات صغيرة (مناظر الدماغ، طبقات القشرة، خريطة الشبكة العصبية، العين، جذع الدماغ، التدفق العصبي، الكود)، وفي وسطها دماغ آلي متوهج بالأزرق مع كابلات يتبدل منظره كل ثانية تقريباً، بينما تنبثق من الشبكة نوافذ تقريب تكبّر لوحة ما ثم تعود إلى مكانها.
>
> A ~25-second sci-fi 'top secret' dashboard in cool white packed with small panels (brain views, cortical layers, neural map, eye, brain stem, signal flow, code), with a glowing blue cyborg brain wrapped in cables at the centre that swaps viewing angle about every second, while zoom windows pop out of the grid to enlarge one panel and then return.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/thegreatest-sv-f33d62
- التصنيفات / Categories: diagrams, photos, product-ui
- النسبة المقترحة / Aspect: 720x1020 · المدة / Duration: 25 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: HTML Canvas, CSS, GSAP, React

## الفكرة
الفكرة ملف استخباراتي عن تقنية غير أرضية: لوحة معلومات واحدة ثابتة يملؤها التفصيل، والحركة تأتي من شيئين فقط: الدماغ المركزي الذي يتبدل منظره كأنه يُفحص من زوايا مختلفة، والنوافذ التي تقفز من الشبكة لتكبير جزء ما. الطابع صورة مولّدة بالذكاء الاصطناعي بأزرق متوهج على أبيض، مع نصوص صغيرة كثيفة توحي بالدقة.

## Concept
The idea is an intelligence file on alien technology: one fixed, detail-dense dashboard, with motion coming from only two things: the central brain changing view as if being scanned from different angles, and windows jumping out of the grid to enlarge one part. The look is AI-generated imagery in glowing blue on white, with dense tiny text that suggests precision.

## المشاهد المقترحة
- 0-3 ث: لوحة المعلومات كاملة على الشاشة منذ البداية: ترويسة بوسم سري ورموز، وصفوف من اللوحات حول دماغ آلي كبير في المنتصف بمنظر جانبي؛ ونافذة صغيرة تنبثق أعلى اليسار تعرض لوحة المكعب مكبرة.
- 3-6 ث: الدماغ يتبدل إلى منظر أمامي، ثم نسخة زجاجية هولوغرافية بتشويش مسح أفقي؛ ونافذة عين مكبرة وكومة عتاد دوارة تنبثقان فوق اللوحات الجانبية.
- 6-9 ث: الدماغ بمنظر علوي وفي قلبه كرة متوهجة، ثم منظر خلفي؛ ونافذة خلية عصبية مكبرة تصعد من أسفل اليسار وخريطة الشبكة مكبرة من أعلى اليمين.
- 9-13 ث: نافذة تقريب كبيرة بإطار تكبر فوق المنتصف مع قراءة لمعامل التكبير، وتتعمق في الأسلاك والخيوط المتوهجة على مرحلتين، بينما يظهر بجوارها رسم تخطيطي للدماغ.
- 13-19 ث: الدماغ يواصل التبدل (ثلاثة أرباع، خلفي، جانبي) مع وسوم بيانات داكنة صغيرة تظهر قرب أجزائه؛ ونوافذ تنبثق من صف مناظر الدماغ ولوحة المشابك وشاشة الكود.
- 19-25 ث: مزيد من تبديل الزوايا مع إبراز فص متوهج، ونوافذ رسوم خطية للدماغ تنبثق على الجانبين، ونافذة طويلة لجذع الدماغ؛ وتنتهي الحلقة على المنظر الجانبي الذي بدأت به.

## Proposed scenes
- 0-3s: The full dashboard is already on screen: a header with a classified label and codes, rows of panels around a large central cyborg brain in side view; a small window pops out top-left showing an enlarged cube panel.
- 3-6s: The brain swaps to a front view, then a glassy holographic version with a horizontal scan glitch; an enlarged eye window and a spinning hardware stack pop out over the side panels.
- 6-9s: The brain shows a top view with a glowing sphere at its core, then a back view; an enlarged neuron window rises from the bottom-left and an enlarged network map from the top-right.
- 9-13s: A large framed zoom window grows over the centre with a magnification readout, pushing deeper into wires and glowing filaments in two steps, while a sketch of the brain appears beside it.
- 13-19s: The brain continues cycling (three-quarter, rear, side views) with small dark data tags appearing near its parts; windows pop out from the brain-overview row, the synaptic panel and the code console.
- 19-25s: More angle swaps with a glowing lobe highlight, line-drawing brain windows popping out at the sides, and a tall brain-stem window; the loop ends on the side view it began with.

## قواعد الحركة
- لوحة معلومات كثيفة ثابتة: لوحات بيضاء باردة #eef1f4 بخطوط رمادية رفيعة #b8c0c8، ووسوم صغيرة داكنة بخط أحادي #1c2430، وصور متوهجة من الأزرق #3aa0ff إلى السماوي #8fd8ff، ولوحات شاشة شبه سوداء #0b1320.
- الدماغ المركزي سلسلة صور تتبدل زاويتها كل ثانية تقريباً بمزج سريع أو تشويش أفقي قصير، وليس دوراناً ثلاثي الأبعاد سلساً.
- نوافذ التقريب تنبثق من لوحة في الشبكة بتكبير سريع (~200 مللي ثانية) وشريط عنوان رفيع، تثبت 1-2 ثانية، ثم تنكمش عائدة إلى مكانها.
- نافذة التقريب الكبيرة تزيد التكبير على قفزتين مع وسم قراءة، كأنها مجهر.
- وسوم بيانات داكنة صغيرة تومض قرب أجزاء الدماغ؛ شاشات الكود تتمرر ببطء؛ والرسوم البيانية ترتجف.
- لا حركة كاميرا ولا قطعات: العمل كله إطار واحد ثابت لنحو 25 ثانية، مصمم ليتكرر.
- الخط تقني أحادي صغير وحروف كبيرة مكثفة، وكلها صغيرة؛ والنص الكبير الوحيد هو ترويسة السرية.

## Motion rules
- A fixed dense dashboard: cool white #eef1f4 panels with thin grey #b8c0c8 rules, tiny dark mono labels #1c2430, glowing blue #3aa0ff to cyan #8fd8ff imagery and near-black #0b1320 console panels.
- The central brain is an image sequence that swaps view about every 1 s with a quick crossfade or a short horizontal glitch, never a smooth 3D rotation.
- Zoom windows pop out of a grid panel with a fast scale-up (~200 ms) and a thin title bar, hold 1-2 s, then shrink back to their slot.
- The big zoom window steps magnification in two jumps with a readout label, like a microscope.
- Small dark data tags blink on near parts of the brain; code consoles scroll slowly; graphs jitter.
- No camera movement and no cuts: the whole piece is one locked frame for about 25 s, designed to loop.
- Type is a small technical mono and condensed caps, all tiny; the only large text is the classified header.

## Facts stated by the source (rewritten in our words)
- The page presents a setup for making motion pieces with an HTML-based video framework inside an AI coding agent, shown through this sci-fi dashboard example.
- Technologies listed on the page include GSAP, HTML, Lottie and Remotion; tags are product UI and code.

## Assumptions
Observed from 24 frames sampled every ~1.05 s plus cut detection (no cuts): the fixed dashboard, the brain swapping views about once a second, the pop-out zoom windows and the two-step magnification window over 25 s. Assumed: that the brain and panel images are pre-generated stills, that it is built in HTML, and the soundtrack, which is present but was not listened to.

## Keywords
sci-fi hud, dashboard, top secret, cyborg brain, glowing blue, zoom windows, pop-out panels, loop, ai imagery, واجهة خيال علمي, لوحة معلومات, دماغ آلي, أزرق متوهج, نوافذ تقريب, ملف سري
