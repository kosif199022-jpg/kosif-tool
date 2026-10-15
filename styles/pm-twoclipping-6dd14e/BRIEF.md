# إعلان منتج توليد محتوى UGC على شبكة إيقاعية — UGC ad generator promo

> إعلان عالي الجودة بأسلوب بسيط مدته 20 ثانية، فكرة واحدة لكل لقطة، مقاطع حقيقية فقط، وكل قطع على نبضة.
>
> A 20-second high-end minimal promo for a UGC ad generator: one idea per shot, real vertical footage only, every cut on a downbeat.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/twoclipping-6dd14e
- التصنيفات / Categories: product-ui, phone, kinetic-type, shapes, particles, photos, music, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 20 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: HTML Canvas, CSS, WebGL

## الفكرة
الموضوع أداة تولد إعلانات بأسلوب المحتوى الذي ينتجه المستخدمون من مقاطع رأسية حقيقية، والهدف إظهار النتيجة لا الخوارزمية: مقاطع كثيرة تدخل، وإعلان فائز واحد يخرج. اللغة الحركية بسيطة ومتقشفة: لون تمييز واحد، خط sans واحد بتباعد ضيق، فراغ كبير، كشف للنص عبر الأقنعة، وقطع مطابقة تقود العين من كلمة إلى واجهة إلى مقطع. كل لقطة تشغل شريطاً موسيقياً واحداً من عشرة.

## Concept
The subject is a tool that generates user-generated-content style ads from real vertical clips, and the goal is to show the outcome rather than the algorithm: many clips go in, one winning ad comes out. The motion language is minimal and disciplined: one accent colour, one tight-tracked sans, generous negative space, masked type reveals and match cuts that lead the eye from a word to a UI to a clip. Each shot owns exactly one bar of the ten-bar track.

## المشاهد المقترحة
- 0-2 ث (الشريط 1): تهبط جملة الجذب كلمة كلمة على النبضات الأربع، كل كلمة تُكشف عبر قناع أفقي؛ لا علامات ترقيم على الشاشة.
- 2-4 ث (الشريط 2): تتحول إحدى كلمات الجذب إلى حقل الإدخال في المنتج؛ يكتب المؤشر الموجز وينقر توليد.
- 4-6 ث (الشريط 3، الذروة): تنفتح دائرة من الزر إلى الخارج ويظلم الإطار؛ داخل الدائرة يتجمع جدار من مقاطع رأسية حقيقية بينما يمسح خط ماسح وتضيء ثلاث بلاطات بلون التمييز كفائزة.
- 6-10 ث (الشريطان 4-5): يظهر الناتج الرئيسي بخط ضخم، ثم يدور كاروسيل ثلاثي الأبعاد من مقاطع حقيقية بانعكاسات أرضية وتهبط حركة سريعة بضبابية حركية على مقطع بطل واحد.
- 10-16 ث (الأشرطة 6-8): يجلس المقطع البطل داخل إطار هاتف بجانب لوحة تنقلب إلى نتائج؛ تتوالى الإحصاءات بقطع دفع على النبضات القوية مع تدحرج عدادات.
- 16-20 ث (الشريطان 9-10): ينزلق شريط من ثلاث كلمات، يتبلور الشعار من نقطة التمييز، ويتلاشى الإطار إلى الأسود على النبضة الأخيرة.

## Proposed scenes
- 0-2s (bar 1): The hook sentence lands word by word on the four beats, each word revealed through a horizontal mask; no punctuation on screen.
- 2-4s (bar 2): One hook word morphs into the product's input field; a cursor types the brief and clicks generate.
- 4-6s (bar 3, the drop): A circle opens outward from the button and the frame goes dark; inside the circle a wall of real vertical clips assembles while a scan line sweeps and three tiles light up in the accent colour as winners.
- 6-10s (bars 4-5): The key output appears as oversized type, then a 3D carousel of real clips rotates with floor reflections and a motion-blurred whip lands on one hero clip.
- 10-16s (bars 6-8): The hero sits inside a phone frame next to a panel that flips into results; stats push-cut one after another on the downbeats with a counter roll.
- 16-20s (bars 9-10): A three-word ticker slides through, the logo resolves from the accent dot, and the frame fades to black on the final beat.

## قواعد الحركة
- كل شيء يُحسب من الزمن داخل seek(t) على مستوى النافذة: لا CSS animations ولا مؤقتات ولا حالة محمولة بين الإطارات.
- الشبكة 10 أشرطة بإيقاع 120 نبضة في الدقيقة، ثانيتان لكل شريط؛ كل قطع على نبضة قوية وكل ضربة واجهة على نبضة، مع معايرة على ضربات الطبل الحقيقية للمقطوعة.
- التسهيل cubic-bezier(0.16, 1, 0.3, 1) للكشف (400-600 مللي ثانية) وخطي لخط المسح؛ التسهيل الارتدادي أو المطاطي ممنوع.
- كشف النص بالأقنعة فقط: انزلاق لأعلى داخل مستطيل قص خلال 350 مللي ثانية بتدرج 60 مللي ثانية لكل كلمة؛ يغادر النص الخارج قبل وصول الداخل بمئة مللي ثانية.
- لغة الكاميرا حركة واحدة متصلة لكل لقطة: دفع بطيء أو حركة سريعة أو قطع دفع؛ الضبابية الحركية من مزج ثلاثة إطارات فرعية عند زائد وناقص 1/240 ثانية، وليس من مرشحات CSS.
- اللون: أرضية داكنة أو بيضاء، ولون تمييز واحد يُستخدم فقط على الفائزين والأزرار ونقطة الشعار؛ اللقطات الحقيقية تُعرض كتسلسل JPEG دقيق الإطار، لا بطاقات بديلة أبداً.
- الأغلفة الحاوية للكاروسيل ثلاثي الأبعاد هي ما يتلاشى، لا عنصر preserve-3d نفسه، كي لا ينبسط ويظهر وجهاه معاً.
- حظر المبدع: حلقات الصدمة، انفجارات الجسيمات، انقسام RGB، اهتزاز الكاميرا، وهج العدسة، التوهج النيوني، الأرضيات الشبكية، الخلفيات الوامضة، والنقاط في نهاية النص على الشاشة.

## Motion rules
- Everything is computed from time inside a window-level seek(t): no CSS animations, no timers and no state carried across frames.
- Grid is 10 bars at 120 BPM, 2 s per bar; every cut sits on a downbeat and every UI hit on a beat, calibrated to the real kick hits of the track.
- Easing is cubic-bezier(0.16, 1, 0.3, 1) for reveals (400-600 ms) and linear for the scan line; bouncy or elastic easing is banned.
- Type reveals are masked only: slide-up inside a clip rect over 350 ms with 60 ms per-word stagger; outgoing text leaves 100 ms before incoming text arrives.
- Camera language is one continuous move per shot: slow push, whip or push-cut; motion blur comes from blending three subframes at plus and minus 1/240 s, never from CSS filters.
- Colour: dark or white ground, one accent used only on winners, buttons and the logo dot; real footage is shown as frame-accurate JPEG sequences, never placeholder cards.
- 3D carousel wrappers are faded, never the preserve-3d element itself, so both faces do not flatten and show through.
- Banned by the creator: shockwave rings, particle bursts, RGB split, camera shake, lens flares, neon glows, grid floors, flashing backgrounds and full stops in on-screen text.

## Facts stated by the source (rewritten in our words)
- Ten bars at 120 BPM with two seconds per bar, giving a 20-second film at 1920 by 1080.
- Built as one HTML file where every style is derived from time; real clips are converted to 30 fps JPEG sequences and swapped per frame.
- The song is analysed with numpy for tempo, beat grid, energy per bar and the drop; cuts land on downbeats.
- Rendered through Playwright at 60 fps with three subframes blended for motion blur; sound effects aligned by measured peak and the mix normalised to -14 LUFS.
- Visual direction is minimal: one accent colour, one clean sans with tight tracking, masked reveals, match cuts and real footage only.
- The structure runs hook words, a word-to-UI morph with cursor, a circle-open drop into a clip wall with three winners, big output type, a reflective 3D carousel, a phone plus results panel, stat push cuts, a ticker, a logo and a fade to black.
- Inputs requested: product name and promise, 3-5 UI moments, an accent colour, 10-20 owned vertical clips and a licensed track with a clear drop.

## Assumptions
Bar-to-scene allocation after the drop and the specific easing values are my proposal; the source fixes the beat grid and the shot list but not how many bars each middle shot takes.

## Keywords
saas promo, beat grid, match cut, masked type, real footage, 3d carousel, scan line, motion blur subframes, إعلان منتج, مقاطع حقيقية, قطع مطابق, شبكة نبضات, تصميم بسيط, مولد إعلانات
