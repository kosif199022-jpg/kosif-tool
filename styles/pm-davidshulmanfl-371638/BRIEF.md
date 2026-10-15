# فيديو موسيقي بأسلوب الصلصال المتحرّك بمراجع معاصرة — Clay-style music video

> فيديو موسيقي لدقيقة واحدة بمظهر تحريك الصلصال الإيقافي مع أغنية أصلية بروح البوب الفني الثمانيني ورموز حياتنا الرقمية الحالية.
>
> A 60 s music video with a code-built stop-motion clay look, an original 1980s art-pop style song, and today's digital life as the cast of objects.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/davidshulmanfl-371638
- التصنيفات / Categories: music
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 60 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: HTML Canvas, Remotion, Web Audio

## الفكرة
الموضوع فيديو موسيقي يستحضر روح أفلام الصلصال الإيقافية في فيديوهات البوب الفني الثمانينية، لكن شخصياته وأشياءه من اليوم: هاتف، سمّاعات لاسلكية، درون توصيل، سكوتر مشترك، فقاعة محادثة ذكية. الهدف إمتاع المشاهد بإحساس يدوي محسوس يستحيل تمييزه عن العجينة الحقيقية رغم أنه مولّد بالكود. اللغة الحركية تقوم على الإطارات المتدرّجة (التحريك على اثنين وثلاثة)، واهتزاز موضعي طفيف، وأشكال كروية متكتلة تندمج كالصلصال، وتبديل أفواه الشخصية حسب مقاطع الكلمات؛ والأغنية أصلية تُؤلَّف بطبول مقفلة ومزامير نحاسية وجهير صاعد.

## Concept
The subject is a music video that channels the hand-made stop-motion spirit of 1980s art-pop videos, recast with today's objects: a phone, wireless earbuds, a delivery drone, a shared scooter, an AI chat bubble. The goal is tactile delight, a clay feel so convincing it hides its code origin. The motion language rests on stepped frames (animating on twos and threes), seeded positional jitter, blobby metaball shapes that merge like clay, and mouth-tile replacement timed to lyric syllables; the song is original, built with gated drums, brass stabs and a sliding bass.

## المشاهد المقترحة
- 0-6ث: رأس من الصلصال يتكوّن من ست كتل تتدحرج وتندمج (تحريك عتبة metaball على Canvas)؛ العينان ترمشان على ثلاثة إطارات؛ حروف العنوان تصعد كشرائط صلصال مترنّحة.
- 6-18ث: المقطع الأول: هاتف وسمّاعات وكوب قهوة تدور حول الرأس، ويُستبدل كل منها بإطارات بديلة كل نبضتين؛ الفم يتنقل بين ست بلاطات صوتية متزامنة مع مقاطع الكلمات.
- 18-30ث: اللازمة الأولى: كلمات الأغنية من شرائط صلصال تملأ الإطار وتنضغط عند كل ضربة إيقاع؛ موكب من أيقونات معاصرة صغيرة (سكوتر، درون، حقيبة توصيل) يسير عبر الثلث السفلي.
- 30-42ث: المقطع الثاني: يُعاد بناء الرأس بثلاثة نماذج معاصرة (مُبثّ بحلقة إضاءة، لاعب بسمّاعة، عامل عن بُعد بحاسوب) عبر مسح تغيير المشهد كل 8 نبضات.
- 42-54ث: اللازمة الثانية والجسر: يذوب كل شيء في كتلة واحدة دوّارة، ثم تسارع زمني للوحة السماء المرسومة تتغير ألوانها خلفها، مع بصمات أصابع ظاهرة على الصلصال.
- 54-60ث: الخاتمة: تتقلص الكتلة إلى كرة واحدة، تعود بطاقة العنوان، وتهبط ضربة النحاس الأخيرة على قطع حاد إلى الأسود.

## Proposed scenes
- 0-6s: A clay head assembles from six blobs that roll in and merge (metaball threshold animation on Canvas); eyes blink on threes; the title letters rise as clay strips with a wobble.
- 6-18s: Verse 1: a phone, earbuds and a coffee cup orbit the head, each swapped by replacement frames every 2 beats; the mouth cycles through six phoneme tiles in sync with the lyric syllables.
- 18-30s: Chorus 1: lyric words made of clay strips fill the frame and squash on every beat hit; a parade of small modern icons (scooter, drone, delivery bag) marches across the bottom third.
- 30-42s: Verse 2: the head rebuilds as three modern archetypes (streamer with ring light, gamer with headset, remote worker with laptop) via set-change wipes every 8 beats.
- 42-54s: Chorus 2 and bridge: everything melts into one rotating blob, then a time-lapse of the painted sky board changing colour behind it, with fingerprints visible in the clay.
- 54-60s: Outro: the blob shrinks to a single sphere, the title card returns, and the final brass sting lands on a hard cut to black.

## قواعد الحركة
- الخط الزمني بمعدل 24 إطارًا في الثانية لكن كل عنصر دمية يتحدّث فقط على إطارات محجوزة: استخدم Math.floor(frame / 2) للاثنين وMath.floor(frame / 3) للثلاثة؛ التدرّج الناعم لكل إطار على الدمى ممنوع.
- كل إطار محجوز يأخذ اهتزازًا حتميًا ±1.5 بكسل و±0.6 درجة من ضجيج مبذور كي يتنفس المشهد كالتحريك الإيقافي الحقيقي.
- حركة الدمى خطوات خطية بلا easing؛ الـ easing محجوز للكاميرا التي تؤدي اقترابًا واحدًا بنسبة 6 بالمئة في كل لازمة على كامل مدتها.
- شبكة الإيقاع: اختر سرعة قريبة من 110 نبضة في الدقيقة (545 مللي ثانية للنبضة) واشتق منها كل ضربة وتبديل فم وتغيير مشهد؛ لا شيء يتحرك خارج الشبكة.
- حروف الكلمات الصلصالية تنضغط إلى 0.85 على المحور الرأسي عند كل ضربة وتتعافى خلال ثلاثة إطارات محجوزة؛ الكلمات لا تتلاشى أبدًا بل تُوضع أو تُرفع.
- اللون: ألوان أولية مشبعة على لوحة سماء مرسومة، طبقة ملمس بصمات بشفافية 12 بالمئة، وإضاءة رئيسية ناعمة من أعلى اليسار مدموجة في التظليل.
- الانتقالات قطعات استبدال ومسح تغيير مشهد فقط؛ ممنوع: ضبابية الحركة، التوهّج، التدرّجات التي توحي بثلاثي أبعاد ناعم، وأي تلاشٍ متقاطع.

## Motion rules
- Timeline runs at 24 fps but every puppet element updates only on held frames: use Math.floor(frame / 2) for twos and Math.floor(frame / 3) for threes; smooth per-frame tweening on puppets is banned.
- Each held frame gets a deterministic jitter of plus or minus 1.5 px and plus or minus 0.6 degrees from seeded noise so the set breathes like real stop-motion.
- Puppet motion uses linear steps with no easing; easing is reserved for the camera, which performs one 6 percent dolly-in per chorus over its full length.
- Beat grid: pick a tempo near 110 BPM (545 ms per beat) and derive every hit, mouth swap and set change from it; nothing moves on an off-grid time.
- Lyric clay letters squash to 0.85 y-scale on each beat hit and recover over three held frames; words never fade, they are placed or removed.
- Colour: saturated primaries on a painted sky board, a fingerprint texture overlay at 12 percent opacity, and a soft top-left key light baked into shading.
- Transitions are replacement cuts and set-change wipes only; banned: motion blur, glow, gradients that imply smooth 3D, and any cross-dissolve.

## Facts stated by the source (rewritten in our words)
- The requested length is sixty seconds.
- The visual reference is the stop-motion clay style of two well-known 1980s art-pop music videos, updated with present-day figures and references.
- The song itself must also be created, in a style that would sit on that era's art-pop album.
- The listing tags it as music and lists a 1280x720 frame.

## Assumptions
The specific modern objects, the 110 BPM grid, the six-part structure and the metaball technique are proposals; the source fixes only the duration, the clay stop-motion reference and the need for an original 1980s-flavoured song.

## Keywords
صلصال, تحريك إيقافي, فيديو موسيقي, أغنية أصلية, بوب فني, ثمانينات, stop motion, claymation, metaball, animate on twos, lyric sync, art pop, replacement animation, music video
