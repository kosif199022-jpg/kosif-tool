# لعبة بطاقات قتالية بأسلوب البكسل: لعب أدوار على طاولة خضراء — Pixel art card battle game

> لقطة لعب مدتها 15 ثانية للعبة بطاقات قتالية بفن البكسل على أرضية من بلاط حجري كحلي: طاولة خضراء بإطار خشبي يجلس عليها توكنات وحوش دائرية للطرفين، بطل كل طرف في الأعلى والأسفل بنقاط حياته، يد من البطاقات الزرقاء في الأسفل؛ بطاقة كرة نار تُسحب بسهم منقط نحو هدف، بطاقات وحوش تُكبَّر عند التمرير، توكنات تومض وتهتز عند الضربة، شريط دور العدو يمر، ثم بطاقة إعدام حمراء تقضي على وحش.
>
> A 15 s gameplay capture of a pixel-art card battler on navy stone tiles: a green felt table in a wood frame with round creature tokens, heroes above and below, a fanned hand of blue cards, a fireball dragged along a dotted arc, hover card previews, hit flashes and particle deaths, an enemy-turn banner and a red execute spell.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/aisongman-71ffac
- التصنيفات / Categories: characters, product-ui
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: HTML Canvas, React, CSS

## الفكرة
الفيديو ليس رسوماً متحركة سردية بل لعبة تعمل تُعرض كما يراها اللاعب: نظام بصري كامل بفن البكسل بلوحة ألوان محدودة (كحلي وأخضر طاولة وخشب وأحمر للعدو وأزرق للاعب). كل فعل له تغذية راجعة واضحة: سهم استهداف، تكبير البطاقة، وميض الضرر، جسيمات صغيرة عند الموت، ولافتة الدور. الإيقاع إيقاع لعب حقيقي بتبادل الأدوار.

## Concept
This is not a narrative animation but a working game shown as the player sees it: a complete pixel-art visual system with a limited palette (navy, felt green, wood, red for the enemy, blue for the player). Every action has clear feedback: a targeting arrow, card zoom, damage flash, small death particles, and a turn banner. The pacing is real play with alternating turns.

## المشاهد المقترحة
- 0-1 ث: دور اللاعب: ثلاثة توكنات للعدو في الصف العلوي واثنان للاعب أسفلها على الطاولة الخضراء؛ بطاقة كرة نار تُرفع من اليد وتُكبَّر ثم تُسحب على قوس برتقالي منقط نحو بطل العدو.
- 1-2 ث: التمرير فوق توكن صديق يظهر معاينة بطاقة كبيرة بصورة وعنوان وصندوق نص وشارات الهجوم والحياة.
- 2-5 ث: توكن شبح في صف العدو يُضرب وينفجر جسيمات بكسل؛ تُلعب بطاقة سحر زرقاء فيُستدعى مخلوق ثالث صديق بحلقة خضراء؛ وزر إنهاء الدور يضيء بالبرتقالي.
- 5-7 ث: المخلوقات الصديقة تهاجم على خطوط منقطة؛ التوكنات تومض بالأبيض وتهتز، وأرقام الضرر تقفز، وبطاقة وحش للعدو تظهر بمعاينة جانبية مع تلميح.
- 7-9.5 ث: مزيد من التبادل: معاينة مخلوق جليدي، ومخلوق داكن يُضرب بوميض أحمر ويذوب توكنه في شرر.
- 10-11 ث: لافتة داكنة لدور العدو تمر عبر الطاولة؛ والعدو يلعب بطاقة بطل حارس كبيرة تظهر معاينتها يساراً ثم تهبط على اللوحة كتوكن.
- 12-15 ث: بطاقة سحر إعدام حمراء تنزلق من اليسار وتستهدف وحشاً صديقاً فيتحطم إلى جسيمات خضراء؛ وتستقر اللوحة والبطل المعادي في مواجهة توكنين صديقين.

## Proposed scenes
- 0-1s: Player turn: three enemy tokens on the top row and two friendly tokens below on the green table; a fireball card is lifted from the hand, enlarged, then dragged along a dotted orange arc to an enemy hero.
- 1-2s: Hovering a friendly token pops a large card preview with portrait, title, text box and attack/health badges.
- 2-5s: A ghost token on the enemy row is hit and bursts into pixel particles; a blue spell card is played, summoning a third friendly creature with a green outline ring; the end-turn button highlights orange.
- 5-7s: Friendly creatures attack along dotted lines; tokens flash white and shake, damage numbers pop, and an enemy minion card previews at the side with a tooltip.
- 7-9.5s: More trades: a frost creature preview, a dark creature hit with a red flash, its token dissolving into sparks.
- 10-11s: A dark 'enemy turn' banner sweeps across the table; the enemy plays a large taunt champion card that previews at left, then drops onto the board as a token.
- 12-15s: A red execute spell card slides in from the left and targets a friendly minion, which shatters into green particles; the board settles with the enemy champion facing two friendly tokens.

## قواعد الحركة
- الألوان: بلاط حجري كحلي #1f2550 بفواصل أفتح #2e3670، طاولة خضراء #1f6b3a بخط أوسط أغمق، إطار خشبي #7a4a28، بطاقات اللاعب زرقاء #2d55c8، العدو أحمر #c8323c، واجهة ذهبية #f2b33a، وصناديق نص بلون الرق #efe0b8.
- فن بكسل حاد بمقياس صحيح وعرض بأقرب جار؛ بلا تنعيم ولا حركة دون البكسل للشخصيات؛ وخط بكسل عريض لكل التسميات والأرقام.
- لغة التغذية الراجعة: تكبير عند التمرير إلى معاينة بطاقة كبيرة (نحو 0.1 ثانية)، أقواس استهداف منقطة، وميض أبيض عند الضربة مع اهتزاز 2 إلى 3 بكسل، أرقام ضرر طافية، وانفجار جسيمات بكسل عند الموت.
- كاميرا ثابتة من الأعلى؛ اللوحة لا تتحرك أبداً، فقط التوكنات والبطاقات واللافتات.
- بنية الأدوار ظاهرة: زر إنهاء الدور يضيء عند انتهاء الأفعال، ولافتة بعرض الشاشة تعلن دور العدو نحو ثانية.
- الإيقاع يتبع اللعب: فعل كل 0.6 إلى 1.2 ثانية تقريباً في دور اللاعب، وحركات أبطأ ومتأنية في دور العدو.

## Motion rules
- Palette: navy stone tiles #1f2550 with lighter #2e3670 mortar, felt green #1f6b3a with a darker centre line, wood frame #7a4a28, player blue cards #2d55c8, enemy red #c8323c, gold UI #f2b33a, parchment text boxes #efe0b8.
- Crisp pixel art at integer scale with nearest-neighbour rendering; no smoothing, no sub-pixel motion on sprites; chunky pixel font for all labels and numbers.
- Feedback language: hover zoom to a large card preview (about 0.1 s), dotted targeting arcs, white hit flash plus a 2-3 px shake, floating damage numbers, and pixel particle bursts on death.
- Fixed top-down camera; the board never moves, only tokens, cards and banners do.
- Turn structure is visible: the end-turn button lights when actions run out, and a full-width banner announces the enemy turn for about 1 s.
- Pacing follows play: an action roughly every 0.6-1.2 s during the player's turn, slower deliberate plays on the enemy's turn.

## Facts stated by the source (rewritten in our words)
- The creator asked for a pixel-art card battle game, built with Claude.

## Assumptions
Observed from 24 frames sampled every ~0.63 s across the 15 s video, which has no audio track: the board layout, tokens, hand, card previews, targeting arcs, hit flashes, enemy-turn banner and execute spell. Exact game rules and small card text were not read and are not reproduced; whether play was scripted or live is unknown. Hex values are estimates. The record has no categories; characters and shapes are suggested.

## Keywords
pixel art, card battler, card game, gameplay capture, turn-based, game UI, targeting arrow, 8-bit, فن البكسل, لعبة بطاقات, لعبة أدوار, واجهة لعبة, قتال, ألعاب
