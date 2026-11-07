# كلمات متحركة — ترجمة كلمة بكلمة تضرب مع الصوت — كلمات متحركة

> ريل عمودي 9:16 فوق فيديو متحدث، تظهر فيه الترجمة العربية كلمة أو كلمتين في كل مرة في منتصف الثلث السفلي بخط عريض أبيض بحد أسود سميك، كل كلمة تقفز بضربة تكبير صغيرة لحظة نطقها، والكلمة المهمة تتلون بالأصفر وتكبر أكثر مع إيموجي أو زوم خفيف على الفيديو.
>
> A 9:16 reel over talking-head footage where Arabic captions appear one or two words at a time, centred in the lower third in bold white with a thick black outline; each word pops with a small scale punch the moment it is spoken, and key words turn yellow and punch bigger with an emoji or a slight zoom on the footage.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: kinetic-type, photos
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 30 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: Remotion, React, CSS, Web Audio

## الفكرة
أغلب الناس يشاهدون بلا صوت، فالترجمة هي الفيديو. نجعلها إيقاعية: الكلمة تظهر في نفس لحظة نطقها، فيقرأ المشاهد بسرعة الكلام وتبقى عينه على الشاشة. الإبراز اللوني للكلمات المفتاحية يصنع التشديد الذي يصنعه الصوت، والفيديو نفسه يبقى هو البطل.

## Concept
Most people watch muted, so the captions are the video. They are rhythmic: each word appears exactly when spoken, so the viewer reads at speaking speed and stays on screen. Colour emphasis on key words recreates vocal stress, while the footage itself stays the hero.

## المشاهد المقترحة
- 0-2 ث: جملة الجذب: أول 3-4 كلمات تقفز واحدة تلو الأخرى، وكلمة الجذب بالأصفر #ffe14d بحجم 120٪ مع زوم 3٪ على الوجه.
- 2-10 ث: التدفق العادي: مجموعات من كلمة أو كلمتين تحل محل بعضها حسب توقيت الكلمات من النص المفرغ؛ كل منها تقفز من 85٪ إلى 100٪ خلال 0.12 ث.
- 10-12 ث: التشديد: رقم أو كلمة مفتاحية تأخذ عرضاً أكبر بالأصفر مع ملصق إيموجي يرتد بجانبها.
- 12-25 ث: استمرار التدفق مع زوم قفزي (من 100٪ إلى 112٪) على الفيديو كل 3-5 ث للحفاظ على الطاقة.
- 25-30 ث: الخلاصة: آخر مجموعة كلمات تضرب بالأحمر #ff3b3b أو الأصفر وتثبت 0.8 ث، ثم ترجمة الدعوة للتفاعل.

## Proposed scenes
- 0-2s: Hook line: the first 3-4 words punch in one by one, the hook word in yellow #ffe14d at 120% with a 3% zoom-in on the face.
- 2-10s: Normal flow: 1-2 word groups replace each other on word timings from a transcript; each pops 85% to 100% in 0.12 s.
- 10-12s: Emphasis: a key number or word fills more width, yellow, with an emoji sticker bouncing beside it.
- 12-25s: Continued flow with a jump-cut zoom (100% to 112%) on the footage every 3-5 s to keep energy.
- 25-30s: Punchline: the final word group hits in red #ff3b3b or yellow, holds 0.8 s, then the call to action caption.

## قواعد الحركة
- التوقيت من طوابع زمنية لكل كلمة (محاذاة تلقائية لصوت المستخدم)؛ تظهر الكلمة خلال إطار واحد من بداية نطقها وتبقى حتى المجموعة التالية.
- المجموعة من 1-3 كلمات، ونحو 14 حرفاً على الأكثر في السطر، دون تقسيم كلمة؛ مع الحفاظ على تشكيل الحروف العربية واتجاه اليمين لليسار وبلا تحريك حرف بحرف.
- الشكل: كايرو بلاك أو تجوال إكسترا بولد، أبيض #ffffff بحد أسود #000 سُمكه 8-10 بكسل وظل ناعم، بحجم نحو 7٪ من ارتفاع الإطار، في المنتصف عند 68-72٪ من الارتفاع.
- القفزة: تكبير من 0.85 إلى 1.0 خلال 0.12 ث مع تجاوز خفيف (1.04)؛ وكلمات التشديد من 1.0 إلى 1.2 باللون #ffe14d.
- الفيديو تحتها يأخذ زوماً قفزياً (8-12٪) عند كلمات التشديد وقطعات قفزية؛ والترجمة لا تتحرك مع الفيديو أبداً.
- الصوت هو صوت المستخدم دون تعديل إلا ضبط العلو إلى -14 LUFS؛ وموسيقى خفيفة اختيارية تنخفض 12 ديسيبل تحت الكلام.
- الفرق عن التايبوغرافي العربي المتحرك (النص هو التكوين كله بلا فيديو) والآلة الكاتبة (حرفاً حرفاً): هذه ترجمة متزامنة فوق متحدث.

## Motion rules
- Timing comes from word-level timestamps (forced alignment of the user's audio); a word appears within one frame of its spoken onset and stays until the next group.
- Group size 1-3 words, max about 14 characters per line, never splitting a word; Arabic shaping and RTL preserved, no per-letter animation.
- Style: Cairo Black or Tajawal ExtraBold, white #ffffff, 8-10 px black #000 outline plus a soft shadow, size about 7% of frame height, centred at 68-72% height.
- Pop: scale 0.85 to 1.0 in 0.12 s with easeOutBack (overshoot 1.04); emphasis words use 1.0 to 1.2 and colour #ffe14d.
- Footage beneath gets punch-in zooms (8-12%) on emphasis words and jump cuts; captions never move with the footage.
- Audio is the user's voice, untouched except loudness normalisation to -14 LUFS; optional light music ducked 12 dB under speech.
- Different from kinetic-arabic (typography is the whole composition, no footage) and typewriter (character-by-character): these are synced captions over a speaker.

## Facts stated by the source (rewritten in our words)
- Catalogued as a KOSIF original style named moving words, in the Kinetic type and Music categories.

## Assumptions
Authored KOSIF definition, not an observed reference: there is no reference video for this base style (its page is the KOSIF repo root), so palette hex values, type choices, timings and scene beats are original KOSIF design decisions, not measurements. Assumed a 9:16 talking-head reel of about 30 s; word timings come from a transcript aligned to the user's audio. The Music category fits weakly; Kinetic type plus Photos (footage) may be a better fit.

## Keywords
captions, subtitles, word by word, talking head, reels captions, karaoke, emphasis, ترجمة, كلمات متحركة, ترجمة كلمة بكلمة, كابشن, متحدث, ريلز
