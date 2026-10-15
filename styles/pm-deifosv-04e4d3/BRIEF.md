# إطلاق لعبة تنس بإحصاءات حية — Tennis game launch video

> فيديو إطلاق عالي الطاقة للعبة تنس على الويب يعرض إحصاءات حية من الموقع واللعب على الحاسوب والهاتف وتبديل السمات على الإيقاع.
>
> A high-energy launch film for a web tennis game, pulling live stats from the site and showing desktop and mobile play plus theme switching, all cut to music.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/deifosv-04e4d3
- التصنيفات / Categories: product-ui, phone, music
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 30 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, Web Audio

## الفكرة
الموضوع لعبة تنس تعمل في المتصفح، ويريد صاحبها فيلم إطلاق صاخبًا يثبت ثلاث حقائق: اللعبة حيّة (إحصاءات حقيقية من الموقع)، وتعمل على سطح المكتب والهاتف، ولها سمات متعددة. الهدف هو إشعار المشاهد بأن المباراة بدأت الآن ودعوته للانضمام. تتميّز لغة الحركة بكرة لا تتوقف أبدًا عن الحركة: هي التي تقود الكاميرا وتفرض القطع، وكل تغيير في الواجهة أو السمة يحدث على ارتدادة أو نبضة طبل، مع إمكانية إرفاق موجّه لتوليد الأغنية.

## Concept
The subject is a browser tennis game whose owner wants a loud launch film proving three things: the game is alive (real stats from the site), it runs on desktop and phone, and it ships with several themes. The goal is to make the viewer feel the match is on right now and invite them in. The motion language is a ball that never stops moving: it leads the camera and forces the cuts, and every UI or theme change lands on a bounce or a drum hit, with an optional music-generation prompt delivered alongside.

## المشاهد المقترحة
- 0-3 ث: كرة تندفع من أعلى اليمين، تنضغط 20% عند الاصطدام، ويظهر شعار اللعبة داخل الانبعاج؛ يُرسم خط ملعب تحته خلال 300 مللي ثانية.
- 3-9 ث: الإحصاءات الحية: ثلاثة عدّادات (مباريات اليوم، لاعبون متصلون، أطول تبادل) تُجلب من الموقع وتتصاعد كلوحة نتائج ملعب، وتنقلب الأرقام بتأخير 90 مللي ثانية بين رقم وآخر.
- 9-16 ث: اللعب على سطح المكتب: إطار متصفح عريض يعرض تبادلًا؛ تتبع الكاميرا الكرة عبر الملعب بينما يبقى إطار المتصفح مثبّتًا.
- 16-22 ث: اللعب على الهاتف: يتحوّل إطار المتصفح إلى هاتف خلال 600 مللي ثانية، ويستمر التبادل نفسه بالوضع الرأسي وتنزلق أزرار الإبهام من الحافة السفلية.
- 22-27 ث: السمات: مع كل نبضة يتبدّل كساء الملعب (عشب، تراب، ملعب صلب، ليلي) بمسح لوني ينبثق من الشبكة؛ وتواصل الكرة ارتدادها عبر كل مسح.
- 27-30 ث: الشعار والعنوان وزر العب الآن؛ ترتدّ الكرة ثلاث مرات أصغر في كل مرة وتتوقف كنقطة نهاية الشعار النصي.

## Proposed scenes
- 0-3s: A ball slams in from top-right, squashes 20% on impact, and the game logo appears inside the dent; a court line draws under it in 300ms.
- 3-9s: Live stats: three counters (matches today, players online, longest rally) fetched from the site roll up like a stadium scoreboard, digits flipping with a 90ms stagger.
- 9-16s: Desktop play: a wide browser frame shows a rally; the camera tracks the ball across the court while the browser chrome stays pinned to the frame.
- 16-22s: Mobile play: the browser frame tweens into a phone over 600ms, the same rally continues in portrait and thumb controls slide up from the bottom edge.
- 22-27s: Themes: on each beat the court re-skins (grass, clay, hard court, night) with a colour wipe radiating from the net; the ball keeps bouncing through every wipe.
- 27-30s: Logo, URL and a 'play now' button; the ball bounces three times, smaller each time, and stops as the full stop of the tagline.

## قواعد الحركة
- تتبع الكرة قوسًا فيزيائيًا: قطع مكافئ بفعل الجاذبية مع ارتداد 85%، وانضغاط 20% عند الاصطدام، وتمدّد 10% عند ذروة السرعة؛ وتظهر الكرة في 80% من الإطارات على الأقل.
- شبكة الإيقاع أولًا: يُستخرج الـ BPM من المقطوعة (الهدف 128-140)، ويُوضع كل قطع وكل بداية عدّاد وكل مسح سمة على نبضة قوية؛ الانحراف المسموح إطار واحد عند 30 إطارًا في الثانية.
- تتبع الكاميرا الكرة بتأخير 120 مللي ثانية وتجاوز 15% ثم تعود للمركز بمنحنى cubic-bezier(0.2, 0.9, 0.3, 1)؛ لا اهتزاز يدوي.
- الإحصاءات قيم حقيقية تُقرأ من واجهة الموقع وقت التصيير وتُنسَّق بفواصل الآلاف؛ القيم المؤقتة ممنوعة في النسخة النهائية.
- تحوّل المتصفح إلى هاتف تحريك واحد للعرض والارتفاع ونصف قطر الزوايا خلال 600 مللي ثانية بمنحنى ease-in-out؛ محتوى اللعبة لا يُصغَّر بل يُعاد تدفّقه.
- مسحات السمات شعاعية من مركز الشبكة، 280 مللي ثانية لكل منها، ولا يتغيّر إلا لوحة ألوان الملعب؛ نص الواجهة يحتفظ بلون واحد ثابت عالي التباين.
- الخط: sans مضغوط ثقيل للأرقام والعناوين بحجم 96 بكسل فأكثر، بحروف لاتينية كبيرة، والعربية بخط كوفي عريض بارتفاع حروف مطابق.
- ممنوع: الحركة البطيئة، والتلاشي، وأي لقطة بلا كرة أو إحصاء، وأكثر من إطار هاتف واحد على الشاشة.

## Motion rules
- The ball follows a physics arc: gravity-driven parabola with 85% restitution, 20% squash on impact and 10% stretch at peak speed; it is on screen in at least 80% of frames.
- Beat grid first: detect BPM from the track (target 128-140), place every cut, counter start and theme wipe on a downbeat; allowed drift is 1 frame at 30fps.
- Camera tracks the ball with a 120ms lag and a 15% overshoot, then recentres with cubic-bezier(0.2, 0.9, 0.3, 1); no handheld shake.
- Stats are real values read from the site API at render time and formatted with thousands separators; placeholders are banned in the final.
- The browser-to-phone morph is a single tween of width, height and corner radius over 600ms with ease-in-out; the game content inside is not scaled, it reflows.
- Theme wipes are radial from the net centre, 280ms each, and only the court palette changes; UI text keeps one fixed high-contrast colour.
- Type: a condensed heavy sans for numbers and headlines at 96px or larger, uppercase in Latin, with Arabic in a bold Kufi-style face at matching x-height.
- Banned: slow motion, fades, any shot without the ball or a stat, and more than one phone frame on screen.

## Facts stated by the source (rewritten in our words)
- The tone requested is high energy.
- The film must display live statistics taken from the game's website.
- It must demonstrate play on both desktop and mobile, and show more than one visual theme.
- The creator also wants, if needed, a text prompt they can paste into Suno to generate the soundtrack.
- Tagged under product UI, phone and music; no duration is given.

## Assumptions
The 30s length, the ball-led camera and the four named themes are proposals; the source does not say which themes exist or how the stats are exposed, so a site API read at render time is assumed. The Suno prompt is treated as a deliverable alongside the film.

## Keywords
tennis game, game launch, live stats, responsive play, theme switch, beat sync, suno prompt, sports motion, لعبة تنس, إطلاق لعبة, إحصاءات حية, هاتف وحاسوب, تبديل السمات, مزامنة إيقاع
