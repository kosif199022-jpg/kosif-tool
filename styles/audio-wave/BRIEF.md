# موجة صوت متفاعلة مع التعليق أو الموسيقى وسط شاشة داكنة — موجة صوت

> ريل عمودي داكن تتوسطه موجة صوت حية تتفاعل مع الصوت الفعلي: أعمدة طيف دائرية أو خط موجي متوهج، ترجمة عربية كبيرة تتزامن مع الكلام، وصورة المتحدث أو غلاف الأغنية داخل الحلقة، مناسب للبودكاست ومقاطع الكلام والأغاني.
>
> A dark vertical reel centred on a live audio waveform driven by the real soundtrack: a circular spectrum of bars or a glowing wave line, large Arabic captions synced to speech, and the speaker's photo or cover art inside the ring; built for podcast clips, spoken quotes and songs.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: music, shapes
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 40 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: Remotion, React, Web Audio, HTML Canvas

## الفكرة
الصوت هو البطل والصورة تترجمه: كل ما يتحرك على الشاشة مشتق من تحليل الصوت (الشدة والترددات والنبضات)، فلا حركة عشوائية. مناسب لتحويل مقطع بودكاست أو خاطرة صوتية أو أغنية إلى فيديو عمودي جذاب بلا تصوير. يختلف عن أنماط التايبوغرافي في أن الكلمات عنصر مساعد والموجة هي مركز التكوين.

## Concept
Sound is the hero and the picture translates it: everything that moves is derived from audio analysis (loudness, frequency bands, onsets), so there is no random motion. It turns a podcast clip, a voice note or a song into an engaging vertical video without filming. It differs from the type styles because words support the frame while the waveform is the centre of the composition.

## المشاهد المقترحة
- 0-2 ث: الافتتاح: شاشة سوداء والخط الموجي مسطح؛ مع أول كلمة ينفجر بالحركة وتتسع الحلقة من صفر إلى حجمها الكامل في 10 إطارات.
- 2-10 ث: صورة المتحدث الدائرية داخل حلقة من 64-96 عموداً شعاعياً تتفاعل مع الطيف؛ وأول سطر ترجمة يظهر تحتها.
- 10-25 ث: المتن: الترجمة تتغير مع كل عبارة؛ ومع الكلمات المؤكدة يتوهج إطار الحلقة وتتحرك درجة لون الخلفية قليلاً.
- 25-35 ث: الذروة: الأعمدة تتحول إلى موجة أفقية متناظرة بعرض الشاشة للاقتباس الأهم، والاقتباس بخط أكبر.
- 35-40 ث: الختام: الموجة تهدأ إلى خط رفيع، يكتمل شريط التقدم، ويظهر اسم البرنامج والحساب.

## Proposed scenes
- 0-2s: Hook: black screen, the wave line flat; on the first word it bursts into motion and the ring expands from 0 to full size in 10 frames.
- 2-10s: The speaker's circular photo sits inside a ring of 64-96 radial bars reacting to the spectrum; the first caption line appears under it.
- 10-25s: Body: captions change per phrase; on emphasised words the ring glow flares and the background gradient shifts hue slightly.
- 25-35s: Peak moment: bars switch to a mirrored horizontal waveform across the full width for the key quote, with the quote in larger type.
- 35-40s: Outro: the wave settles back to a thin line, a progress bar completes, and the show name plus handle fade up.

## قواعد الحركة
- الألوان: خلفية #0b0d17 بتدرج شعاعي بطيء نحو #1b1f3b، لون الموجة من #36e2c4 إلى #7b5cff، الترجمة #ffffff والكلمة المؤكدة #ffcf4a.
- كل الحركة مشتقة من تحليل الصوت: ارتفاع الأعمدة من نطاقات FFT (مُنعّمة على 3-4 إطارات)، حجم الحلقة من شدة الصوت (1.0-1.08)، والتوهج من قمم بدايات الأصوات.
- الأعمدة بأطراف مستديرة وعرض 6-8 بكسل، ولا تتجاوز 30% من نصف قطر الحلقة كي تبقى الصورة واضحة.
- الترجمة العربية بخط شبه عريض بلا زوائد (مثل IBM Plex Sans Arabic أو Noto Kufi Arabic) بحجم 56-64 بكسل من اليمين لليسار، سطران كحد أقصى، تتبدل مع كل عبارة بظهور في 4 إطارات؛ والكلمة المنطوقة قد تضيء لكن حروفها لا تُفصل أبداً.
- الخلفية تنساب ببطء شديد (دورة لون كاملة في أكثر من 20 ثانية) لتبقى الموجة العنصر السريع الوحيد.
- شريط تقدم رفيع أسفل الشاشة يتبع زمن المقطع، فوق المنطقة الآمنة للمنصة.

## Motion rules
- Palette: background #0b0d17 with a slow radial gradient to #1b1f3b, wave colour #36e2c4 grading to #7b5cff, captions #ffffff with the emphasised word in #ffcf4a.
- All motion is driven by audio analysis: bar heights from FFT bands (smoothed over 3-4 frames), ring scale from RMS loudness (1.0-1.08), glow from onset peaks.
- Bars have rounded caps, 6-8 px width, and never exceed 30% of ring radius so the photo stays readable.
- Arabic captions: semi-bold sans (e.g. IBM Plex Sans Arabic or Noto Kufi Arabic) 56-64 px, RTL, max two lines, changed per phrase with a 4-frame fade-up; the spoken word may brighten but letters are never split.
- Background drifts very slowly (a full hue shift over 20+ s) so the wave stays the only fast element.
- A thin progress bar at the bottom tracks clip time; keep it above the platform's safe area.

## Facts stated by the source (rewritten in our words)
- KOSIF lists this as an original style named for sound waves, tagged music and shapes.

## Assumptions
Authored KOSIF definition, not an observed reference: the record points only to the repo root, so there was no video to watch. Palette hex values, fonts, timings and scene beats are design choices written for this style, not measurements.

## Keywords
audio waveform, audiogram, spectrum, podcast clip, music visualizer, captions, موجة صوت, بودكاست, طيف صوتي, تعليق صوتي, موسيقى, ترجمة
