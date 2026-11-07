# واجهات زجاجية شفافة فوق تدرجات لونية — واجهة زجاجية

> بطاقات واجهة من زجاج مصنفر شفاف تطفو فوق كتل لونية متدرجة تتحرك ببطء: حدود لامعة رفيعة، ضبابية خلفية، أيقونات ومؤشرات تنبثق داخل البطاقات، انعكاس ضوء ينزلق على الزجاج، وحركة ناعمة هادئة لعرض التطبيقات والمزايا.
>
> Frosted glass UI cards float over slowly drifting colour gradient blobs: thin glossy borders, background blur, icons and stats popping inside the cards, a light reflection gliding over the glass and calm, smooth easing for presenting apps and features.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: product-ui, shapes
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 30 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
الواجهة تبدو كقطع زجاج فاخرة، والجمال يأتي من الضوء والألوان التي تظهر خلفها. البطاقات تحمل المعلومة، والخلفية الحية تعطي الإحساس. مناسب لإعلانات التطبيقات والخدمات الرقمية وعرض الأرقام بطريقة أنيقة وهادئة.

## Concept
The interface looks like premium pieces of glass, and the beauty comes from the light and colour seen through them. Cards carry the information, the living background carries the mood. It suits app and digital service ads and elegant, calm stat presentations.

## المشاهد المقترحة
- 0-3 ث: كتل متدرجة تنجرف على خلفية عميقة؛ وبطاقة زجاجية كبيرة تظهر وترتفع مع ضبابية من 0 إلى 24 بكسل وفيها العنوان.
- 3-9 ث: ثلاث بطاقات أصغر تتكدس من اليمين بتتابع 120 مللي ثانية، كل واحدة بأيقونة وتسمية؛ وخط ضوء ينزلق عليها.
- 9-15 ث: بطاقة واحدة تتمدد لتملأ الكادر؛ وفيها خط بياني يُرسم ورقم يعدّ صعودًا؛ ومفاتيح وشارات تتحرك بتغيّر الحالة.
- 15-21 ث: البطاقات تميل بعمق خفيف (دوران ±8°) تتبع مؤشرًا افتراضيًا، والانعكاس يتحرك معها.
- 21-26 ث: إشعار زجاجي على شكل كبسولة ينزل من الأعلى بارتداد ناعم: الفائدة الأساسية.
- 26-30 ث: البطاقات تتجمع في مربع أيقونة تطبيق واحد؛ الشعار والدعوة لفعل على الزجاج؛ والكتل تتباطأ.

## Proposed scenes
- 0-3s: Gradient blobs drift on a deep background; a large glass card fades and rises in with blur 0→24 px, the headline inside.
- 3-9s: Three smaller cards stack in from the right with 120 ms stagger, each holding an icon and a label; a light streak slides across them.
- 9-15s: One card expands to fill the frame; inside, a chart line draws and a number counts up; toggles and chips animate state changes.
- 15-21s: The cards tilt in slight 3D (rotateY ±8°) following a virtual pointer, the reflection shifting with them.
- 21-26s: A notification glass pill drops from the top with a soft bounce: the key benefit.
- 26-30s: Cards gather into a single app-icon tile; logo and call to action on glass; blobs slow down.

## قواعد الحركة
- وصفة الزجاج: تعبئة بيضاء بشفافية 8-14%، ضبابية خلفية 20-32 بكسل، حد 1 بكسل بتدرج من أبيض 40% أعلى اليسار إلى 5% أسفل اليمين، لمعة داخلية، استدارة 28-40 بكسل، وظل ناعم 0 20 60 بشفافية 25%.
- كتل الخلفية: 3-4 تدرجات شعاعية كبيرة تنجرف 10-30 بكسل في الثانية وتتشكل ببطء؛ ولا تثبت أبدًا.
- التسهيل ناعم: تباطؤ خماسي 500-700 مللي ثانية للدخول، ونوابض منخفضة الصلابة للتمدد؛ ولا قطع حاد داخل المشهد.
- خط ضوء لامع يعبر الزجاج مرة واحدة على الأكثر في المشهد (600-900 مللي ثانية).
- اللوحة: خلفية #0b0b1a، كتل بنفسجية #7b5cff، وردية #ff6fb5، مائية #3fe0d0، كهرمانية #ffb86b؛ ونص أبيض #ffffff وثانوي #c9c9e3.
- الخط: العربية بـIBM Plex Sans Arabic أو Readex Pro بوزن 500-700، العناوين 84-120 بكسل والتسميات 36-44 بكسل؛ والأرقام جدولية.
- ملاحظة تصيير: ضبابية الخلفية قد تكون بطيئة؛ لذلك تُضبَّب طبقة الخلفية مسبقًا بقناع كل بطاقة في الفيديوهات الطويلة.
- الفرق عن الواجهات الدقيقة واستعراض SaaS: الواجهات الدقيقة تركّز على تفاصيل التفاعل الصغيرة؛ واستعراض SaaS يتجول في شاشة منتج حقيقي؛ أما الواجهة الزجاجية فلغة بصرية من بطاقات مصنفرة فوق ألوان حية.

## Motion rules
- Glass recipe: fill white at 8-14% opacity, backdrop blur 20-32 px, 1 px border with a top-left white 40% to bottom-right 5% gradient, inner highlight, radius 28-40 px, soft shadow 0 20px 60px at 25%.
- Background blobs: 3-4 large radial gradients drifting 10-30 px/s and slowly morphing; never static.
- Easing is soft: ease-out quint 500-700 ms for entrances, springs with low stiffness for expansions; no hard cuts inside a scene.
- A specular light streak crosses glass at most once per scene (600-900 ms).
- Palette: background #0b0b1a, blobs violet #7b5cff, pink #ff6fb5, aqua #3fe0d0, amber #ffb86b; text white #ffffff and secondary #c9c9e3.
- Type: Arabic in IBM Plex Sans Arabic or Readex Pro 500-700, titles 84-120 px, labels 36-44 px; numbers tabular.
- Render note: backdrop-filter can be slow; pre-blur the background layer per card mask when rendering long videos.
- Difference from ui-micro and saas-demo: ui-micro focuses on tiny interaction details; saas-demo walks through a real product screen; glass-ui is a visual language of frosted cards over living colour.

## Facts stated by the source (rewritten in our words)
- The public description states nothing specific beyond the title.

## Assumptions
This is an authored KOSIF definition, not an observed reference: there is no reference video for this base style, so palette, type, timings and beats are a design decision written for KOSIF, to be refined per project.

## Keywords
glassmorphism, glass ui, frosted glass, gradient blobs, app ad, ui cards, واجهة زجاجية, زجاج مصنفر, بطاقات واجهة, إعلان تطبيق, تدرجات لونية, واجهات
