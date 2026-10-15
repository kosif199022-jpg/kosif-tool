# ساحر بكسل يستحضر العملات الرقمية — Pixel wizard crypto animation

> مقطع بكسل آرت لساحر صغير يستحضر عملات رقمية وشموع سعرية بتعويذة واحدة، بحركة إطارات مقطّعة على طريقة ألعاب الثمانينيات.
>
> A pixel-art wizard conjures crypto coins and candlestick charts with one spell, animated in stepped 8-bit frames with a retro game feel.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/0xevinho-3777d8
- التصنيفات / Categories: —
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 10 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: HTML Canvas, Remotion

## الفكرة
الموضوع ساحر مرسوم بالبكسل يؤدي تعويذة تتحول إلى عملات رقمية ورموز بلوكتشين، وهو نسخة من فكرة سابقة أُعيد توجيهها نحو عالم الكريبتو. الهدف الترفيه السريع وبناء شخصية قابلة لإعادة الاستخدام في محتوى مجتمعات العملات. لغة الحركة تلتزم بقيود ألعاب الكونسول القديمة: إطارات مقطّعة لا مُنعَّمة، شبكة بكسل ثابتة، ألوان محدودة، وتضخيم كوميدي في لحظة انطلاق التعويذة.

## Concept
The subject is a pixel-drawn wizard whose spell turns into crypto coins and blockchain symbols, a remix of an earlier idea redirected toward the crypto world. The goal is quick entertainment and a reusable character for crypto-community content. The motion language obeys old console constraints: stepped frames instead of smooth tweens, a fixed pixel grid, a limited palette, and comic exaggeration at the moment the spell fires.

## المشاهد المقترحة
- 0-1.5 ث: سماء ليلية بنجوم 2x2 بكسل تومض بمعدل 4 إطارات/ث؛ الساحر يدخل من اليسار بدورة مشي من 4 إطارات ويتوقف في المنتصف.
- 1.5-3.5 ث: العصا ترتفع عبر 6 إطارات مقطّعة؛ دائرة رونية تدور تحته بمعدل 8 إطارات/ث مع تصاعد طنين.
- 3.5-6 ث: تنطلق التعويذة: انفجار شرارات بكسل (24 جزيئاً، عمر 3 إطارات) وعملات تنبثق واحدة كل 150 مللي ثانية، كل منها تنقلب بدورة من 6 إطارات.
- 6-8.5 ث: تتراكم العملات في مخطط شموع يتصاعد؛ قبعة الساحر ترتفع دهشةً مع تجاوز من إطارين.
- 8.5-10 ث: صاروخ بكسل يعبر خلفه؛ تجميد على وضعية، وميض بأربعة ألوان، بطاقة ختام.

## Proposed scenes
- 0-1.5s: A night sky of 2x2-pixel stars twinkles at 4 fps; the wizard walks in from the left on a 4-frame cycle and stops centre.
- 1.5-3.5s: The staff rises over 6 stepped frames; a rune circle rotates under him at 8 fps while a hum builds.
- 3.5-6s: The spell fires: a burst of pixel sparks (24 particles, 3-frame life) and coins pop out one per 150ms, each flipping on a 6-frame cycle.
- 6-8.5s: Coins stack into a candlestick chart that climbs; the wizard's hat lifts in surprise with a 2-frame overshoot.
- 8.5-10s: A pixel rocket crosses behind him; freeze on a pose, a 4-colour flash, end card.

## قواعد الحركة
- لا حركة دون البكسل: كل عنصر يتحرك بخطوات بكسل كاملة على شبكة صحيحة، ويُكبَّر بأسلوب nearest-neighbour؛ تُمنع مرشحات التنعيم.
- معدلات الإطارات: حلقات السكون 4 إطارات/ث، دورات المشي 8، انفجارات التعويذة 12؛ لا استيفاء بين الإطارات المفتاحية بمنحنيات easing.
- اللوحة محدودة بـ 16 لوناً؛ التعويذة تستخدم لوني تمييز فقط يومضان على إطارات متناوبة لثلاثة إطارات.
- الجزيئات تعيش 3-5 إطارات وتموت بالانكماش بكسلاً واحداً في كل إطار، لا بتلاشي الشفافية.
- الكاميرا ثابتة؛ يُسمح باهتزاز الشاشة مرة واحدة بإزاحة بكسلين لثلاثة إطارات عند هبوط التعويذة.
- العملات والشموع تُرسم كـ sprites بحجم 8x8؛ المخطط ينمو شمعة كل 250 مللي ثانية مع وميض أبيض لإطار واحد على كل شمعة.
- النص بخط بكسل نقطي يُكشف حرفاً حرفاً كل 60 مللي ثانية؛ يُمنع الخط المنعَّم.

## Motion rules
- No sub-pixel motion: every element moves in whole-pixel steps on an integer grid, scaled up with nearest-neighbour; smoothing filters are banned.
- Frame rates: idle loops at 4 fps, walk cycles at 8 fps, spell bursts at 12 fps; never interpolate between keyframes with easing curves.
- Palette capped at 16 colours; the spell uses 2 accent colours only, flashing on alternate frames for 3 frames.
- Particles live 3-5 frames and die by shrinking one pixel per frame, not by fading alpha.
- Camera is fixed; screen shake is allowed once, as a 2-pixel offset for 3 frames when the spell lands.
- Coins and chart candles are drawn as 8x8 sprites; the chart grows one candle per 250ms with a 1-frame white flash on each.
- Text is a bitmap pixel font revealed letter by letter at 60ms per character; anti-aliased type is banned.

## Facts stated by the source (rewritten in our words)
- The source only asks for a variant of an earlier piece with a crypto reference; the pixel-wizard subject comes from the public title.

## Assumptions
Nothing about duration, palette, stack or scenes is stated; the 10-second length, the 8-bit framing and the coin-to-chart gag are all proposed direction.

## Keywords
pixel art, 8-bit, retro game, sprite animation, crypto coins, candlestick, stepped frames, nearest neighbour, بكسل آرت, ساحر, عملات رقمية, تعويذة, رسوم ريترو
