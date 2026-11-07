# ملصقات لامعة تفاعلية تميل مع المؤشر وتُقشَّر عن ورقتها في مقارنة بين نموذجين — Interactive glitter sticker with peel animation

> مقطع عمودي قصير (نحو 13 ثانية) مقسوم أفقياً إلى لوحتين بيضاوين فوق بعض، كل منهما باسم نموذج ذكاء اصطناعي: ملصقات بحواف بيضاء وجليتر هولوغرافي (عبارة ملونة بنجوم، علبة مشروب، شعار كروم، كوكب ديسكو) تميل وتلمع مع حركة يد المؤشر، ثم تُسحب زاويتها فتُقشَّر وتكشف ورقة خلفية رمادية، مع شريط مصغرات بالأسفل.
>
> A short 13-second portrait clip split into two stacked white panels, each labelled with an AI model name: die-cut stickers with white borders and holographic glitter (a rainbow star slogan, a drink can, a chrome logo, a disco planet) tilt and shimmer as a hand cursor moves over them, then get peeled by a corner to reveal grey backing paper, with a thumbnail tray below.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/ann-nnng-d69f71
- التصنيفات / Categories: product-ui, photos
- النسبة المقترحة / Aspect: 480:636 · المدة / Duration: 13 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: React, CSS, WebGL

## الفكرة
الفكرة لعبة مقارنة: نفس الطلب (ملصق لامع يمكن تقشيره) نُفذ مرتين، والفيديو يعرض النتيجتين متزامنتين فوق بعض ليحكم المشاهد. المتعة كلها في الملمس: لمعة قوس قزح تتحرك مع زاوية الميل، حبيبات جليتر على الحافة، وظل ناعم يرفع الملصق عن الصفحة، ثم لحظة التقشير الواقعية حيث تنثني الورقة وتنكشف الخلفية.

## Concept
The idea is a comparison game: the same request (a shiny, peelable sticker) built twice, shown in sync, one above the other, so the viewer can judge. The pleasure is all texture: a rainbow sheen that shifts with the tilt angle, glitter grains along the border, a soft shadow lifting the sticker off the page, then the realistic peel where the paper curls and the backing shows.

## المشاهد المقترحة
- 0-4 ث: اللوحتان تعرضان ملصق العبارة الملونة؛ مؤشر على شكل يد يحوم ويسحب فيميل الملصق ثلاثي الأبعاد وتجتاحه لمعة هولوغرافية.
- 4-5 ث: في اللوحة العليا يمسك المؤشر حافة الملصق فيُقشَّر قطرياً وتنثني الورقة لتكشف خلفية رمادية منقوشة، ثم يعود لمكانه.
- 5-7 ث: يتقدم الاختيار في شريط المصغرات وتتحول اللوحتان إلى ملصق علبة مشروب معدنية مع دوامة دخان لامعة؛ والمؤشر يميلها.
- 7-10 ث: تقشير للعلبة، ثم الانتقال إلى ملصق شعار سباقات هولوغرافي بخطوط سرعة؛ يميل يميناً ويساراً ثم يُقشَّر من زاويته حتى ينفصل تقريباً.
- 10-13 ث: ملصق كوكب على شكل كرة ديسكو بحلقة وبريق يظهر في اللوحتين؛ يلمع تحت المؤشر، ثم يُقشَّر العلوي حتى خلفيته مع عودة المقطع للبداية.

## Proposed scenes
- 0-4s: Both panels show the rainbow slogan sticker; a hand cursor hovers and drags, and the sticker tilts in 3D so the holographic sheen sweeps across it.
- 4-5s: In the top panel the cursor grabs an edge and the sticker peels diagonally, curling to show patterned grey backing, then snaps back into place.
- 5-7s: The selection in the thumbnail tray advances and both panels switch to a chrome drink-can sticker with a swirl of glitter smoke; the cursor tilts it.
- 7-10s: A peel on the can, then a switch to a holographic racing-logo sticker with speed lines; it tilts left and right, then peels from its corner almost entirely off.
- 10-13s: A disco-ball planet sticker with ring and sparkles appears in both panels; it shimmers under the cursor, then the top one is peeled away to its backing as the clip loops.

## قواعد الحركة
- المسرح أبيض بسيط #fbfbfb؛ لكل ملصق حافة بيضاء سميكة مقصوصة وظل ناعم (#000 بشفافية نحو 15% وتمويه 20 بكسل) وحبيبات جليتر على الحافة.
- اللمعة الهولوغرافية: تدرج قوس قزح (#ff6ad5 ← #8ec5ff ← #b6ffb0 ← #ffe36e) تتبع زاويته وموضعه المؤشر، بدمج إضاءة أو تراكب.
- الميل: دوران منظوري حتى ±15 درجة على المحورين حسب موضع المؤشر، بنابض يستقر في نحو 200 مللي ثانية.
- التقشير: خط انثناء يتحرك من الزاوية الممسوكة؛ الجزء المقلوب يُظهر خلفية رمادية (#d9d9d9) بشعارات مكررة باهتة ولمعة على الانحناء.
- المؤشر يد مخصصة للإمساك؛ وعند الإمساك تظهر حلقة صغيرة حوله.
- عناصر الواجهة قليلة: اسم النموذج مع أيقونته أعلى يسار كل لوحة، شريط مصغرات أو نقاط تنقل بالأسفل، وسطر اعتماد بين اللوحتين.

## Motion rules
- Stage is plain white #fbfbfb; each sticker has a thick white die-cut border, a soft drop shadow (#000 at ~15%, 20 px blur) and glitter speckle along the edge.
- Holographic sheen: a rainbow gradient overlay (#ff6ad5 → #8ec5ff → #b6ffb0 → #ffe36e) whose angle and position follow the pointer, blended in screen/overlay mode.
- Tilt: perspective rotation up to ±15° on X and Y driven by pointer position, eased with a spring (~200 ms settle).
- Peel: a fold line travels from the grabbed corner; the flipped part shows grey backing (#d9d9d9) with faint repeated logos and a highlight on the curl.
- Pointer is a custom hand/grab cursor; on grab a small ring appears around it.
- UI chrome stays minimal: model label with icon top-left of each panel, thumbnail tray or dot pager at the bottom, a footer credit line between panels.

## Facts stated by the source (rewritten in our words)
- The title describes an interactive glitter sticker with a peel animation.
- The clip compares two AI models' versions of the same piece.

## Assumptions
Observed from 24 frames sampled every ~0.53 s across 12.7 s: the stacked two-panel comparison, four sticker designs, cursor-driven tilt and the peel reveal. Sticker art appears to be images rather than vector drawings; whether the sheen uses WebGL or CSS gradients is inferred. No audio track. Brand names and logos visible in the stickers should not be reused; replace with original artwork.

## Keywords
sticker, holographic, glitter, peel animation, 3D tilt, cursor interaction, model comparison, split screen, ملصق, هولوغرافي, تقشير, لمعة, مقارنة نماذج, تفاعلي
