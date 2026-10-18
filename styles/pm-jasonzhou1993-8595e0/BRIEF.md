# ريل موشن ذاتي: عرض مهارات في 15 ثانية — Claude motion reel

> ريل ذاتي مدته 15 ثانية مقسم إلى فصول مرقمة داخل إطار HUD: نقطة برتقالية على خط زمني، خط حركي TIMING وSPACING وEASING على البرتقالي والكريمي مع صفوف نصية محيطية متحركة وتعليق برمجي، شبكة مربعات ودوائر تدور، انفجار جسيمات يبني كلمة FLOW، كرة سحابة نقاط فوق أرضية شبكية، مسح بأشرطة لونية إلى بطاقة بيانات، موجات خطوط خلف عبارة سيريف مائلة، وبطاقة ختام.
>
> A 15-second self-showreel split into numbered chapters inside a HUD frame: an orange dot on a timeline, kinetic type TIMING / SPACING / EASING over orange and cream with outlined marquee rows and a code comment, a grid of rotating squares and circles, a particle burst that assembles FLOW, a 3D point-cloud sphere over a floor grid, vertical colour-stripe wipes into a data card, flowing line ribbons behind an italic serif phrase, and an end card.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-10-16)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-10-16); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://www.promptsmotion.com/jasonzhou1993-8595e0
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, Three.js, SVG

## الفكرة
الموضوع ريل يرافق السيرة الذاتية ويستعرض أكبر قدر من المهارات في 15 ثانية: خط حركي، أنظمة أشكال، جسيمات، أبعاد ثلاثة، بيانات وحركة سائلة. كل فصل نحو 1.8 ثانية بخلفية مختلفة (أسود، برتقالي، كريمي، كحلي) داخل HUD دائم بعدّاد إطارات حتى 900 وشريط تقدم. الخطوط ثلاث عائلات: غروتسك ثقيل، أحادي للـ HUD، وسيريف مائل للعبارات الهادئة.

## Concept
The subject is a reel to accompany a CV that shows as many skills as possible in 15 seconds: kinetic type, shape systems, particles, 3D, data and fluid motion. Each chapter lasts about 1.8 s on a different ground (black, orange, cream, navy) inside a persistent HUD with a frame counter to 900 and a progress line. Type uses three families: a heavy grotesk, a mono for HUD and an italic serif for calm phrases.

## المشاهد المقترحة
- 0-1 ث: شبه أسود بحبيبات: نقطة برتقالية تسقط على خط زمني رفيع داخل إطار الـ HUD.
- 1-3.5 ث: خط حركي: كلمة TIMING تُبنى حرفاً حرفاً بضبابية حركة أفقية (نحو 60 مللي ثانية للحرف)، ثم SPACING وEASING على البرتقالي والكريمي مع صفوف محيطية بأحرف كبيرة تتحرك خلفها؛ وEASING تنضغط وتتجاوز بجانب تعليق برمجي يسمي منحنى easeOutBack.
- 3.5-5.5 ث: الأنظمة: شبكة مربعات تتحول إلى دوائر مع موجة دوران تكنسها.
- 5.5-7.5 ث: جسيمات تنفجر من نقطة ثم تتدفق لتشكل حروف FLOW.
- 7.5-8.5 ث: كحلي عميق بتظليل حواف: كرة نقاط فيبوناتشي تدور فوق أرضية شبكية بمنظور مع دوران كاميرا خفيف.
- 8.5-11 ث: أشرطة لونية عمودية تسقط بتتابع نحو 150 مللي ثانية بالبرتقالي والكريمي والأزرق وتمسح إلى فصل البيانات: عدادات أرقام كبيرة يساراً وبطاقة بأعمدة تنمو وخط يُرسم ووسم نسبة يميناً.
- 11-13.5 ث: مئات الخطوط الجيبية الرفيعة تتدفق بالضجيج خلف عبارة سيريف مائلة من سطرين عن أن كل شيء يتحرك، بلونين منفصلين؛ ودفعة قطعات سريعة متقطعة حول 12.7-13 ث.
- 13.5-15 ث: بطاقة ختام هادئة: اسم بأحرف صغيرة ثقيلة مع نقطة، سطر أحادي يفك ترميزه من حروف مبعثرة، وسطر سيريف مائل عن الإتاحة للعمل.

## Proposed scenes
- 0-1s: Near-black with grain: an orange dot drops onto a thin timeline line inside the HUD frame.
- 1-3.5s: Kinetic type: TIMING builds letter by letter with horizontal motion blur (~60 ms per letter), then SPACING and EASING on orange and cream with outlined uppercase rows marqueeing behind; EASING squashes and overshoots beside a code comment naming the easeOutBack curve.
- 3.5-5.5s: Systems: a grid of squares morphs into circles with a rotation wave sweeping across it.
- 5.5-7.5s: Particles explode from a point and flow into the letters FLOW.
- 7.5-8.5s: Deep navy with vignette: a rotating Fibonacci point sphere hovers over a perspective floor grid with a slight camera orbit.
- 8.5-11s: Vertical colour stripes drop in on a ~150 ms stagger cycling orange, cream and blue, wiping into a data chapter: big stat counters on the left and a card with growing bars, a drawing line and a percentage tag on the right.
- 11-13.5s: Hundreds of thin sine-line ribbons flow with noise behind a two-line italic serif phrase about everything moving, colour split across the lines; a glitchy burst of rapid cuts around 12.7-13 s.
- 13.5-15s: Calm end card: a heavy lowercase name with a full stop, a mono subtitle that decodes from scrambled characters and an italic serif availability line.

## قواعد الحركة
- فصول بطول نحو 1.8 ثانية لكل منها أرضية لونية خاصة، مع نحو سبع قطعات حادة على الإيقاع تتجمع حول 2.3-3.3 ث و12.7-13 ث، إضافة إلى مسح بالأشرطة وجسيمات تعيد تشكيل العنصر التالي.
- HUD دائم: أقواس زوايا، عنوان الريل أعلى اليسار، عدّاد زمني أعلى اليمين، الفصل «0X — الاسم» أسفل اليسار، وعدّاد إطارات «n / 900» بخط تقدم أسفل اليمين.
- التخفيف يُعرض لا يُستخدم فقط: EASING تنضغط وتتجاوز بينما يسمي تعليق برمجي المنحنى.
- أنظمة إجرائية: تحول الشبكة بموجة دوران، جسيمات تبني الحروف، كرة نقاط فيبوناتشي، وخطوط يقودها الضجيج.
- فصل البيانات: العدادات تعدّ، الأعمدة تنمو، الخط يُرسم ووسم النسبة ينبثق، كل ذلك في نحو ثانيتين.
- اللوحة: شبه أسود #070709، كحلي #14173a، كريمي #efece1، برتقالي #f05a1e، أزرق #2f45f5، مرجاني #eb8a63، صدئي #c04923 ونص أبيض مائل للرمادي #f2efe6 مع حبيبات دقيقة.
- الخط: نيو غروتسك ثقيل 800-900 للكلمات الرئيسية والأرقام، أحرف كبيرة محيطية للصفوف المتحركة، أحادي للـ HUD، وسيريف مائل للعبارات الهادئة.

## Motion rules
- Chapters of about 1.8 s, each on its own ground colour, with about seven hard cuts on the beat clustered around 2.3-3.3 s and 12.7-13 s, plus a stripe wipe and particles reforming into the next element.
- Persistent HUD: corner brackets, reel title top-left, timecode top-right, chapter '0X — NAME' bottom-left and an 'n / 900' frame counter with progress line bottom-right.
- Easing is shown, not just used: EASING squashes and overshoots while a code comment names the curve.
- Procedural systems: grid morph with a rotation wave, particles that assemble letterforms, a Fibonacci point sphere, noise-driven line ribbons.
- Data chapter: counters tick, bars grow, a line draws and a percentage tag pops, all within about 2 s.
- Palette: near-black #070709, navy #14173a, cream #efece1, orange #f05a1e, blue #2f45f5, coral #eb8a63, rust #c04923 and off-white text #f2efe6, with fine grain.
- Type: heavy neo-grotesk 800-900 for hero words and stats, outlined uppercase for marquee rows, mono for HUD, italic serif for the calm phrases.

## Facts stated by the source (rewritten in our words)
- Requested length is 15 seconds.
- The piece is meant to work as a personal showreel attached to a résumé.
- The creator asked for a dynamic, maximal result rather than a restrained one.
- Tagged on the site under charts and kinetic type; listed at 1920x1080.

## Assumptions
Observed from the watched video: the chapter order (type, systems, particles, 3D, data, flow), the HUD with a 900-frame counter, the alternating grounds and the end card. Assumed: music and exact cut positions beyond the detected clusters; colour hexes are estimates from compressed frames.

## Keywords
showreel, portfolio reel, chapter reel, hud overlay, kinetic typography, easing demo, particles to text, point sphere, stripe wipe, data card, line ribbons, ريل تعريفي, طباعة حركية, جسيمات
