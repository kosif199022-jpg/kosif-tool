# خمسة أقسام ويب تتحرك مع التمرير: عرض تصميم تفاعلي — Five scroll-based sections

> تسجيل شاشة مدته 30 ثانية لصفحة ويب واحدة تمر عبر خمسة أقسام بأسلوب مختلف لكل منها: فهرس مشاريع معمارية تتبدل صورته مع تمييز كل اسم، صفحة منتج لجهاز تسجيل ببطاقات حية (بطارية، موجة صوتية)، خريطة رحلة قطار ليلي تُرسم على خلفية برقوقية داكنة، مروحة عينات ألوان دهان تدور، ثم تذييل أخضر داكن بكلمة علامة ضخمة.
>
> A 30-second screen capture of one web page scrolling through five sections, each with its own look: an architecture project index where the photo swaps as each name highlights, a product page for a recorder with live cards (battery count, waveform), a night-train route map drawing across a dark plum panel, a fanned deck of paint swatches that rotates, and a deep green footer with a giant wordmark.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/ercankeskinx-ec2568
- التصنيفات / Categories: product-ui, kinetic-type, photos
- النسبة المقترحة / Aspect: 1920x972 · المدة / Duration: 30 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: React, CSS, GSAP, SVG

## الفكرة
الفكرة عرض حِرفة تصميم الويب: كيف يمكن لكل قسم أن يروي قصته بالتمرير وحده. كل قسم يلتصق بالشاشة (pinned) أثناء التمرير وتتحول حركة العجلة إلى تقدم داخلي: تمييز اسم تلو اسم، عداد بطارية يملأ، مسار قطار يتقدم محطة بمحطة، عينة لون تخرج من المروحة. القوة في التباين بين الأقسام (رمادي معماري، أبيض تقني، برقوقي ليلي، بيج دافئ، أخضر داكن) مع ثبات نظام الشبكة والخطوط الصغيرة.

## Concept
The idea is a showcase of web craft: how each section can tell its story through scrolling alone. Each section pins to the viewport while scroll progress drives an internal timeline: highlighting one name after another, filling a battery counter, advancing a train route station by station, pulling a swatch out of a fan. The strength is the contrast between sections (architectural grey, technical white, night plum, warm beige, deep green) while the grid and the small type system stay constant.

## المشاهد المقترحة
- 0-4.5 ث: صفحة رمادية دافئة: فقرة تعريف صغيرة بخط أحادي أعلى اليسار، قائمة عمودية من ستة أسماء مشاريع؛ الاسم النشط يغمق مع خط رفيع على يساره بينما تتبدل صورة معمار حداثي أبيض بزوايا مستديرة على اليمين مع كل اسم، وتحتها ثلاثة أعمدة بيانات صغيرة.
- 4.5-13.5 ث: قسم منتج أبيض بارد: عنوان عريض من سطرين، سعر وزر «طلب مسبق» أسود على شكل حبة أعلى اليمين؛ صورة منتج كبيرة مستديرة يساراً؛ ويميناً بطاقات متراصة تتحرك: رقم ساعات البطارية يعدّ مع شريط تقدم أزرق متقطع، موجة صوتية تُرسم مع عداد تسجيل، وبطاقة صورة صغيرة؛ ثم تُعاد البطاقات وتتكرر.
- 13.5-18.5 ث: قسم برقوقي داكن: عنوان سيريف عن النوم في بلد والاستيقاظ في آخر؛ خط مسار بنقاط محطات يُرسم من اليسار إلى اليمين، وعلامة متوهجة تتحرك عليه، وبطاقة صورة يساراً تتحدث مع كل اسم محطة ووقت.
- 18.5-23 ث: قسم بيج فاتح: بطاقة عينة عمودية ترتفع، ثم مروحة من ست عينات دهان تدور؛ اسم اللون النشط ونقطته ووصفه تتحدث بينما تتلون خلفية الصفحة نحو اللون النشط.
- 23.5-30 ث: تذييل أخضر شبه أسود يظهر من الظلام: عنوان تواصل من سطرين، زر صغير «راسلنا»، أربعة أعمدة عنوان وروابط، وكلمة علامة ضخمة تخرج من الحافة السفلية.

## Proposed scenes
- 0-4.5s: Warm grey page: a small mono intro paragraph top-left, a vertical list of six project names; the active name darkens with a thin left rule while a rounded photo of white modernist architecture on the right swaps per name, with three tiny metadata columns beneath.
- 4.5-13.5s: Cool white product section: a two-line bold headline, price and black pill 'pre-order' button top-right; a large rounded product photo on the left; on the right stacked cards animate: a battery hours number counting with a dashed blue progress bar, a waveform that draws as a recording timer runs, and a small photo card; the cards reset and replay.
- 13.5-18.5s: Dark plum section: a serif headline about falling asleep in one country and waking in another; a route line with station dots draws left to right, a glowing marker moves along it and a photo card on the left updates with each station name and time.
- 18.5-23s: Light beige section: a vertical swatch card rises in, then a fan of six paint swatches rotates; the active colour name, dot and description update while the page background tints toward the active colour.
- 23.5-30s: Near-black green footer fades up from dark: a two-line contact headline, a small 'write to us' pill, four columns of address and links, and an oversized wordmark bleeding off the bottom edge.

## قواعد الحركة
- كل قسم مشهد تمرير مثبت: تقدم التمرير (0-1) يقود خطاً زمنياً داخلياً؛ والتمرير الظاهر ناعم لا يقفز.
- ألوان الأقسام: رمادي معماري #e7e6e2 مع حبر #1b1b1b؛ أبيض المنتج #e9ebee مع خطوط زرقاء #3a4fd8 وأزرار سوداء؛ برقوقي ليلي #2a1d2b إلى #1d1626 مع ضوء دافئ #f3d9a4؛ بيج الدهان #ece7df يتلون نحو العينة النشطة (مغرة #c9952f، صدئي #a8432f، طحلبي #6f7d3a، باذنجاني #5a2e4a، أردوازي #3f4f5c، طباشيري #e9e4d6)؛ تذييل أخضر أسود #0e1712.
- الخط: غروتسك محايد واحد للعناوين (عريض ومتقارب)، وسيريف ناعم لقسم السفر، وخط أحادي صغير للبيانات والوسوم والعدادات.
- تمييز القائمة يتحرك بخط عمودي رفيع وتلاشي لون (نحو 200 مللي ثانية)؛ والصورة المرتبطة تتلاشى تبادلياً مع تكبير خفيف.
- بطاقات بيانات حية: الأرقام تعدّ، أشرطة التقدم تمتلئ بقطع متقطعة، والموجات الصوتية تُرسم من اليسار إلى اليمين مع رأس تشغيل.
- خريطة المسار: الخط يُرسم بإزاحة الخط المتقطع، والعلامة تتوهج وتترك خطاً مصمتاً خلفها؛ وبطاقة الصورة تتبدل مع كل محطة.
- مروحة العينات تدور حول محور سفلي بإزاحة 4-6° لكل بطاقة؛ البطاقة النشطة ترتفع ولون الخلفية ينتقل خلال نحو 400 مللي ثانية.

## Motion rules
- Every section is a pinned scroll scene: scroll progress (0-1) maps to an internal timeline; the visible scroll is smooth, never jumpy.
- Section palettes: architecture grey #e7e6e2 with ink #1b1b1b; product white #e9ebee with blue #3a4fd8 dashes and black pills; night plum #2a1d2b to #1d1626 with warm light #f3d9a4; paint beige #ece7df tinting toward the active swatch (ochre #c9952f, rust #a8432f, moss #6f7d3a, aubergine #5a2e4a, slate #3f4f5c, chalk #e9e4d6); footer green-black #0e1712.
- Type: one neutral grotesk for headlines (bold, tight), a soft serif for the travel section, and tiny monospace for metadata, labels and timers.
- List highlight moves with a thin vertical rule and a colour fade (~200 ms); paired image crossfades with a slight scale-in.
- Live data cards: numbers count, progress bars fill in dashed segments, waveforms draw left to right with a playhead.
- Route map: path draws with stroke-dashoffset, the marker glows and leaves a solid line behind it; the photo card swaps per station.
- Swatch fan rotates around a bottom pivot with a 4-6° offset per card; the active card lifts and the background colour tweens over ~400 ms.

## Facts stated by the source (rewritten in our words)
- The request was for five different scroll-driven website sections.
- The prompt is very short (about a dozen words) and names no technology.

## Assumptions
Observed from 24 frames sampled every ~1.25 s across the 30 s capture: the five sections, their palettes, the list highlight, the live product cards, the route map, the swatch fan and the footer wordmark. The file has no audio track. Assumed: that it is a real browser scroll recording (GSAP ScrollTrigger-style pinning), exact hex values and fonts. For a 9:16 KOSIF reel, render each section as a full-screen scene driven by a virtual scroll value rather than recording a browser.

## Keywords
scroll animation, pinned sections, web design showcase, screen recording, route map, paint swatches, product page, portfolio index, تمرير, أقسام موقع, تصميم ويب, تسجيل شاشة, خريطة مسار, عينات ألوان, صفحة منتج
