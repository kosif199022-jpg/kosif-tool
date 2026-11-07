# جولة ثلاثية الأبعاد داخل مركز بيانات للذكاء الاصطناعي — AI data centre 3D tour

> تسجيل شاشة مدته نحو 98 ثانية لصفحة شرح تفاعلية ثلاثية الأبعاد بدرجات الرمادي الفاتح: الكاميرا تطير من مبنى المركز وسط أشجار منخفضة الأضلاع إلى خطوط الكهرباء والمحطة الفرعية، ثم قاعة الخوادم والرف الواحد، ثم صينية الحوسبة والشريحة المفككة طبقة طبقة، ثم الشبكة بين الرفوف، ثم أنابيب التبريد إلى أبراج التبريد، مع تدفقات متحركة ملونة (أصفر للطاقة، أزرق للبيانات، أحمر وفيروزي للحرارة) وعنوان فصل ووصف أسفل اليسار وشريط تحكم أسفل الشاشة.
>
> A ~98-second capture of an interactive 3D explainer in pale greys: the camera flies from a data-centre building to power lines, the server hall, one rack, a compute tray and an exploded chip, the network between racks and the cooling pipes, with colour-coded animated flows (yellow power, blue data, red/teal heat) and chapter captions bottom-left.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/sayan-shanky-f850d8
- التصنيفات / Categories: 3d, diagrams, charts
- النسبة المقترحة / Aspect: 1920x982 · المدة / Duration: 98 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: Three.js, React, WebGL

## الفكرة
الفكرة تتبع طلباً واحداً عبر المبنى الذي يجيب عنه: ثلاثة أشياء تتحرك داخله (طاقة تدخل، بيانات تمر، حرارة تخرج). العالم كله مجسم أبيض رمادي نظيف كنموذج معماري، والألوان مخصصة فقط للتدفقات المتحركة، فيقرأ المشاهد الفكرة من اللون. كل فصل لقطة كاميرا واحدة طويلة إلى مستوى أصغر ثم أكبر، كأنها رحلة من المبنى إلى الترانزستور وعودة.

## Concept
The idea follows a single request through the building that answers it: three things move inside (power in, data through, heat out). The whole world is a clean white-grey model like an architectural maquette, and colour is reserved for the moving flows, so the viewer reads the idea through colour. Each chapter is one long camera move to a smaller and then larger scale, like a trip from the building to the silicon and back.

## المشاهد المقترحة
- 0-8 ث: الفصل 1: منظر جوي لمبنى مركز بيانات مسطح بوحدات على السطح وألواح شمسية وسط أشجار منخفضة الأضلاع؛ خيوط حرارة حمراء تصعد وتدفق طاقة أصفر يتلوى نحو المبنى؛ عنوان مكثف عريض ووصف قصير أسفل اليسار، ومفتاح صغير أعلى اليمين.
- 8-20 ث: الطاقة تصل أولاً: الكاميرا تتبع نبضات صفراء على خطوط الضغط العالي من برج كهرباء إلى محطة فرعية في الموقع، ثم على جانب المبنى مروراً بمحولات ومولدات معنونة.
- 20-28.6 ث: الداخل: أنابيب تبريد حمراء وفيروزية وممرات طاقة صفراء فوق صفوف الرفوف؛ والكاميرا تنزلق إلى قاعة البيانات بصفوف طويلة من الرفوف الداكنة تحت أضواء السقف.
- 28.6-48.5 ث: رف واحد: رف طويل يدور ويفرد صوانيه كأوراق اللعب، تعليقات تسمي صواني المحولات، صينية مبردة بالسائل تنزلق للخارج، ثم تهبط الكاميرا على لوحة صينية الحوسبة الخضراء بصفائح التبريد والأنابيب.
- 48.5-64 ث: تفكيك الشريحة: غلاف الشريحة يرتفع إلى طبقات مفككة بوسوم للأنوية ورصات الذاكرة، ثم تغوص الكاميرا في شبكة كتل حوسبة مضاءة بالأزرق تضيء بلاطاتها لتوضح أين تجري الحسابات.
- 64-80 ث: عمود الكابلات النحاسي في الرف بالبرتقالي، ثم تصبح الرفوف عنقوداً: محولات طرفية ومركزية تطفو فوق صفوف الرفوف وحزم بيانات زرقاء تندفع بينها.
- 80-98 ث: إخراج الحرارة: أنابيب حمراء وفيروزية تتعرج من وحدة التبريد صعوداً عبر المبنى إلى مبردات السطح التي تنفث خيوطاً حمراء؛ ثم يتلاشى الإطار إلى الأبيض مع بداية عنوان الفصل التالي.

## Proposed scenes
- 0-8s: Chapter 1: an aerial view of a flat data-centre building with rooftop units and solar panels among low-poly trees; red heat wisps rise and a yellow power flow snakes in; a bold condensed title and short caption sit bottom-left, a small legend top-right.
- 8-20s: Power arrives first: the camera follows yellow pulses along high-voltage lines from a pylon to an on-site substation, then along the building's side past labelled transformers and generators.
- 20-28.6s: Inside: coolant pipes in red and teal and yellow power trays run over rack rows; the camera glides into the data hall with long rows of dark racks under ceiling lights.
- 28.6-48.5s: One rack: a tall rack rotates and fans its trays out like a deck, callouts label switch trays, one liquid-cooled tray slides out, and the view drops onto the compute tray's green board with cold plates and pipes.
- 48.5-64s: Taken apart: a chip package lifts into exploded layers with labels for dies and memory stacks, then the camera dives into a blue-lit grid of compute blocks where tiles light up to show where the maths happens.
- 64-80s: The rack's copper spine of cables in orange, then racks become a cluster: leaf and spine switches float above rack rows with blue data packets streaking between them.
- 80-98s: Getting the heat out: red and teal pipes zig-zag from a coolant unit up through the building to rooftop coolers venting red wisps; the frame then fades to white as the next chapter title starts.

## قواعد الحركة
- عالم كنموذج معماري: أشكال مطفأة من الأبيض إلى الرمادي #f2f3f5 حتى #8d939b على سماء رمادية فاتحة #e6e8eb، ظلال ناعمة، أشجار مستديرة منخفضة الأضلاع؛ ورفوف داكنة #2a2e34.
- اللون للتدفقات فقط: أصفر الطاقة #f3c43c، أزرق البيانات #3d7df0، أحمر الحرارة #ef6b5e، فيروزي التبريد #3cc8b4، برتقالي النحاس #c97a3a؛ والتدفقات تتحرك كشرطات ونبضات على مسارات.
- كل فصل طيران كاميرا واحد مستمر متباطئ (نحو 8-20 ثانية) مع دوران بطيء؛ ونحو ثلاث قطعات حادة فقط في 98 ثانية.
- المناظر المفككة: الأجزاء تنفصل على محور واحد بخطوط إشارة معنونة وتعليقات صغيرة من سطرين بالعريض والرمادي.
- نص الفصل أسفل اليسار: خط ملون صغير وعداد خطوات، عنوان مكثف عريض، ووصف رمادي من 3-4 أسطر؛ ومفتاح ألوان صغير أعلى اليمين يتغير مع كل فصل.
- واجهة الصفحة التفاعلية ظاهرة (شريط تشغيل وتمرير بالوقت، خيارات العرض ومؤشر الفأرة)، لأن هذا تسجيل لصفحة ويب.
- إيقاع هادئ وثائقي: نحو 8-10 ثوانٍ لكل فصل، والنص يظهر بعد أن تستقر الكاميرا.

## Motion rules
- Maquette world: matte white-to-grey geometry #f2f3f5 to #8d939b on a light grey sky #e6e8eb, soft shadows, low-poly round trees; dark racks #2a2e34.
- Colour only on flows: power yellow #f3c43c, data blue #3d7df0, heat red #ef6b5e, coolant teal #3cc8b4, copper orange #c97a3a; flows animate as moving dashes and pulses along paths.
- Each chapter is one continuous eased camera fly-through (about 8-20 s) with slow orbits; only about three hard cuts in 98 s.
- Exploded views: parts separate along one axis with labelled leader lines and small two-line callouts in bold and grey.
- Chapter text bottom-left: a small coloured rule and step counter, a bold condensed headline, and a 3-4 line grey caption; a small colour legend top-right changes per chapter.
- Interactive-page chrome is visible (a play/scrub bar with time, view options and a cursor), because this is a capture of a web page.
- Pacing is calm and documentary: about 8-10 s per chapter with text fading in after the camera settles.

## Facts stated by the source (rewritten in our words)
- The piece is an interactive 3D tour through an AI data centre, following power, data and heat.
- The page tags it under charts only.

## Assumptions
Observed from 24 frames sampled every ~4 s plus cut detection (cuts near 28.6, 48.5 and 59 s): the maquette look, the chapter sequence (building, power, hall, rack, tray, chip, interconnect, cluster, cooling), colour-coded flows and the page's player bar over about 98 s. Assumed: that this is a browser capture of a real-time page (cursor and scrub bar visible), the remaining chapters after the recording ends, and the sound, which is present but was not listened to.

## Keywords
data centre, 3D explainer, scrollytelling, fly-through, exploded view, server rack, gpu, cooling flow, infographic, مركز بيانات, شرح ثلاثي الأبعاد, جولة كاميرا, منظر مفكك, تبريد, بنية تحتية
