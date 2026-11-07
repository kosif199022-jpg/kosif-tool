# بيكسل آرت — مشهد لعبة 16 بت بشخصيات صغيرة — بيكسل آرت

> ريل عمودي 9:16 بأسلوب ألعاب 16 بت: عالم من البكسلات المكبّرة بلوحة ألوان محدودة، وشخصية صغيرة تمشي وتقفز بإطارات متقطعة، وخلفيات متعددة الطبقات تتحرك أفقياً، ونصوص عربية بخط بكسل داخل صناديق حوار، وعدادات نقاط وقلوب في الأعلى، وانتقالات بتلاشٍ متدرج على شكل مربعات.
>
> A 9:16 reel styled as a 16-bit game: an upscaled pixel world in a limited palette, a small character walking and jumping on stepped frames, multi-layer side-scrolling backgrounds, Arabic text in a pixel font inside dialogue boxes, score and heart counters at the top, and blocky dissolve transitions.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: characters
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 32 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, HTML Canvas, Web Audio

## الفكرة
نحكي القصة كأنها مرحلة في لعبة: الشخصية هي البطل، وكل نقطة في القصة عقبة أو عملة أو باب لمرحلة جديدة. الحنين لألعاب الطفولة يجذب الانتباه، والقيود الصارمة (شبكة بكسل، ألوان قليلة، حركة متقطعة) هي ما يصنع الأسلوب، فلا نعيمها ولا نضيف تدرجات.

## Concept
The story is told as a game level: the character is the hero and each story point is an obstacle, coin or door to a new stage. Nostalgia for childhood games grabs attention, and the strict constraints (a pixel grid, few colours, stepped motion) are what make the style, so nothing is smoothed and no gradients are added.

## المشاهد المقترحة
- 0-3 ث: شاشة البداية: شعار بكسل ينزل على 4 خطوات، ورسالة «ابدأ» تومض، ونغمة بداية بأسلوب موسيقى الألعاب.
- 3-9 ث: المرحلة الأولى: البطل يمشي من اليمين لليسار عبر منظر يتحرك؛ وصندوق حوار يكتب النقطة الأولى.
- 9-15 ث: تظهر عقبة؛ يقفز البطل في قوس من 8 إطارات ويجمع عملة تضيف إلى عداد النقاط (+1).
- 15-21 ث: انتقال باب أو أنبوب: تلاشٍ بمربعات إلى المرحلة الثانية بمجموعة ألوان جديدة (ليل أو كهف).
- 21-27 ث: الزعيم أو اللحظة الكبرى: شخصية أكبر، واهتزاز الشاشة ببكسلات كاملة، وشريط صحة يفرغ.
- 27-32 ث: الفوز: البطل يقفز مع انفجار نجوم ولافتة «مرحلة مكتملة» والدعوة للتفاعل في صندوق الحوار الأخير.

## Proposed scenes
- 0-3s: Title screen: a pixel logo drops in 4 steps, a blinking 'ابدأ' prompt, chiptune-style start chime.
- 3-9s: Level 1: the hero walks right-to-left (RTL-friendly) across a scrolling landscape; a dialogue box types the first point.
- 9-15s: An obstacle appears; the hero jumps on an 8-frame arc and collects a coin that adds to the score counter (+1 pop).
- 15-21s: A door or pipe transition: square-block dissolve into Level 2 with a new palette set (night or cave).
- 21-27s: Boss or big moment: a larger sprite, screen shake by whole pixels, a health bar empties.
- 27-32s: Victory: the hero jumps with a star burst, a 'مرحلة مكتملة' banner, and the call to action as the final dialogue box.

## قواعد الحركة
- لوحة أصلية 180×320 (أو 270×480) تُكبَّر بمعامل صحيح دون تنعيم؛ وكل موضع يلتصق ببكسلات الرسم الكاملة.
- لوحة من 16-24 لوناً، مثل سماء #5fcde4، عشب #6abe30، تراب #8f563b، حد داكن #222034، إضاءة #fbf236، أحمر #d95763؛ بلا تدرجات ولا تنعيم حواف.
- الشخصيات تتحرك على إطارات متقطعة بمعدل 8-12 إطاراً في الثانية (دورة المشي 4-6 إطارات والقفزة 8)، بينما تتحرك طبقات الخلفية بخطوات بكسل كاملة.
- خلفية بعمق من 3-4 طبقات بسرعات 0.25 و0.5 و0.75 و1؛ واهتزاز الشاشة والضربات 1-3 بكسلات رسم فقط.
- النص العربي بخط بكسل عربي بحجمه الأصلي ثم يُكبّر؛ والحوار يُكتب كلمة كلمة (دون فصل الحروف) مع صوت قصير لكل كلمة.
- الواجهة: النقاط والقلوب واسم المرحلة في شريط علوي ثابت؛ وصناديق حوار بحد بكسل واحد #222034 وتعبئة #f4f4f4.
- الفرق عن إطار بإطار (خطوط مرسومة باليد) والرجل العصوي: كل شيء بكسلات ملتصقة بالشبكة مع واجهة لعبة.

## Motion rules
- Native canvas 180x320 (or 270x480) upscaled by an integer factor with nearest-neighbour sampling; every position snaps to whole art pixels.
- Palette of 16-24 colours, e.g. sky #5fcde4, grass #6abe30, dirt #8f563b, dark outline #222034, highlight #fbf236, red #d95763; no gradients or anti-aliasing.
- Sprites animate on stepped frames at 8-12 fps (walk cycle 4-6 frames, jump 8 frames) while scrolling layers move at 60 fps in whole-pixel steps.
- Parallax background in 3-4 layers at 0.25x, 0.5x, 0.75x and 1x; screen shake and impacts move by 1-3 art pixels only.
- Arabic text in a pixel Arabic bitmap font, rendered at its native size and scaled up; dialogue types word by word (not letter-split) with a blip per word.
- UI: score, hearts and a level label in a fixed top bar; dialogue boxes with a 1-art-pixel border #222034 and #f4f4f4 fill.
- Different from frame-by-frame (hand-drawn lines) and stickman: everything is grid-locked pixels with game UI.

## Facts stated by the source (rewritten in our words)
- Catalogued as a KOSIF original style named pixel art, in the Characters category.

## Assumptions
Authored KOSIF definition, not an observed reference: there is no reference video for this base style (its page is the KOSIF repo root), so palette hex values, type choices, timings and scene beats are original KOSIF design decisions, not measurements. Assumed a 9:16 reel of about 32 s told as a game level; a pixel Arabic font with correct joining must be chosen or drawn, since many pixel fonts lack proper Arabic shaping.

## Keywords
pixel art, 16-bit, retro game, sprite, chiptune, 8-bit, platformer, بيكسل آرت, ألعاب قديمة, بكسل, شخصية لعبة, ريترو, مرحلة
