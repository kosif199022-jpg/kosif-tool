# تراك دبستب يُكتب بالكود على الشاشة مع مقاطع فن ASCII ملونة — UK dubstep track with ASCII visuals

> فيديو مربع دقيقة واحدة لمحرر كود موسيقي حي على خلفية سوداء: سطور برمجة تُكتب وتتمرر بخط أحادي مع مقابض منزلقة صغيرة وتظليل للمقاطع النشطة على الإيقاع، يتلوث النص بحروف عشوائية ثم تنفجر الشاشة إلى لوحات فن ASCII ملونة (أحمر وأزرق وذهبي ثم أخضر فاقع) تنبض، وتعود الشاشة للكود مصغراً وتنتهي بسطر تعليق أخير.
>
> A one-minute square video of a live-coding music editor on black: monospace code lines type and scroll with tiny inline sliders and boxes that light up on active pattern steps, the text glitches into random characters, then the screen erupts into pulsing coloured ASCII-art panels (red, blue and gold, then acid green), before returning to zoomed-out code and a final comment line.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/rames-jusso-589f80
- التصنيفات / Categories: code, music, kinetic-type
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 61 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: HTML Canvas, React, Remotion, Web Audio

## الفكرة
الفكرة أن الأغنية هي الكود: نرى سطور البرنامج الذي يولّد التراك (الإيقاع، الباص، الطبول) كأنه أداء حي، وكل خطوة نشطة في النمط تضيء بإطار صغير. في لحظة 'الدروب' يتحول نص الكود نفسه إلى صورة ASCII ضخمة، فيصبح الحرف وحدة الرسم والموسيقى معاً.

## Concept
The song is the code: we watch the program that generates the track (tempo, bass, drums, vocal chops) as a live performance, and every active pattern step flashes a small box. At the drop the code text itself turns into giant ASCII imagery, so the character becomes the unit of both picture and music.

## المشاهد المقترحة
- 0-3 ث: شاشة سوداء، سطر تعليق يُكتب مع مؤشر يومض، ثم سطور السرعة وجذور الأكوردات بأرقام أسطر في هامش رمادي.
- 3-12 ث: المحرر يتمرر عبر كتل الآلات؛ مقابض منزلقة صغيرة داخل السطر وأشرطة أفقية كبطاقات مثقبة تحت بعض الكتل؛ والخلفية تنبض من الأسود إلى الرمادي الأزرق مع الضربات.
- 12-22 ث: رموز النمط النشطة تحصل على إطارات في كل خطوة؛ لون أخضر يتسلل والحروف تبدأ بالتلف إلى رموز وكتل مظللة.
- 22-37 ث: الدروب: فن ASCII يملأ الإطار بحروف صفراء ووردية حمراء وزرقاء تكوّن أشكالاً جريئة وكلمة كبيرة تنبض وتتزحزح على الإيقاع.
- 37-44 ث: عودة للكود على خلفية بيضاء مائلة للبنفسجي، مع استمرار التشويش بكتل حروف معكوسة.
- 44-56 ث: دروب ثانٍ بالأخضر: حقول ASCII خضراء داكنة ثم خضراء فاقعة بأشكال حروف كبيرة أفتح تومض.
- 56-61 ث: البرنامج كاملاً صغيراً ومبتعداً على الأسود، ثم نظرة قريبة على الكتلة الأخيرة وسطر تعليق ختامي.

## Proposed scenes
- 0-3s: Black screen, a comment line types with a blinking caret, then tempo and chord-root lines appear with line numbers in a grey gutter.
- 3-12s: The editor scrolls through instrument blocks; inline slider widgets and horizontal punch-card bars render under some blocks; the background pulses from black to slate grey on hits.
- 12-22s: Active mini-notation tokens get outlined boxes on each step; a green tint creeps in and characters start corrupting into symbols and highlighted blocks.
- 22-37s: Drop: full-frame ASCII art in yellow, red-pink and blue characters forms bold shapes and a large word that pulse and shift on the beat.
- 37-44s: Back to code on a pale lavender-white ground, still glitching with inverted character blocks.
- 44-56s: Second drop in green: dark-green then acid-green ASCII fields with large lighter glyph shapes flickering.
- 56-61s: The whole program shown tiny and zoomed out on black, then a close view of the final block and a closing comment line.

## قواعد الحركة
- كل شيء نص بخط أحادي المسافة (يشبه JetBrains Mono أو Fira Code) على شبكة ثابتة؛ الصورة مصنوعة فقط من الحروف والإطارات والأشرطة الرفيعة.
- ألوان الكود: أسود #050607، رمادي الهامش #5b6470، النص #c9d1d9، الإطارات والمنزلقات سماوي #5ac8fa، والتعليقات رمادي أخفت؛ وتومض اللوحات إلى رمادي أزرق #5f6b75 مع الضربات القوية.
- خطوات النمط النشطة يظهر حولها إطار بسمك بكسل واحد لمدة خطوة واحدة، فيتحرك التظليل مع الإيقاع.
- التشويش: استبدال عشوائي للحروف برموز وكتل معكوسة بكثافة تزداد خلال 3-5 ثوانٍ قبل كل دروب.
- مقاطع ASCII: حقول حروف كثيفة تتحول فيها الإضاءة إلى كثافة رموز؛ اللوحة الأولى أصفر #e8c64a ووردي أحمر #d0306a وأزرق #3a4fd8 على الأسود؛ والثانية أخضر داكن #1d3a10 إلى أخضر فاقع #6ad13a.
- حركة الكاميرا فقط تمرير وتكبير للمحرر؛ لا انتقالات أخرى غير تحويل التشويش إلى ASCII.

## Motion rules
- Everything is monospace text (JetBrains Mono / Fira Code-like) at a fixed grid; the image is made only from characters, boxes and thin bars.
- Code palette: black #050607, gutter grey #5b6470, text #c9d1d9, highlight boxes and sliders cyan #5ac8fa, comments dimmer grey; panels flash to slate #5f6b75 on strong hits.
- Active pattern steps get a 1 px outline box that appears for one step length, so highlights move in tempo.
- Glitch: characters are randomly replaced by symbols and inverted blocks in growing density over 3-5 s before each drop.
- ASCII drops: dense character fields where luminance maps to glyph density; palette 1 yellow #e8c64a, pink-red #d0306a, blue #3a4fd8 on black; palette 2 dark green #1d3a10 to acid green #6ad13a.
- Camera moves are only scrolls and zooms of the editor; no other transitions besides the glitch-to-ASCII swap.

## Facts stated by the source (rewritten in our words)
- The source describes it as a UK dubstep track with ASCII visuals.
- The creator's prompt was a single short line; the page lists no category tags.

## Assumptions
Observed from 24 frames sampled every ~2.6 s across the ~61 s video: the typed code editor, inline sliders and step boxes, glitch corruption, the coloured and green ASCII drops and the zoomed-out ending. The file carries an audio track (only its level was measured; its content was not analysed). That the music is generated by the code on screen and that highlights follow the beat is inferred from the visuals, not heard. Drop timings between samples estimated; hex values estimated. No code text was copied.

## Keywords
live coding, dubstep, ASCII art, code music, glitch, monospace, pattern sequencer, audio visual, برمجة حية, دبستب, فن ASCII, موسيقى بالكود, تشويش, خط أحادي
