# عمق 2.5D لقصة رمزية بالمفتاح والباب — عمق 2.5D

> رسم مسطح يتحرك كأنه ثلاثي الأبعاد: مفتاح ذهبي يُرسم بخط ثم يمتلئ ويطفو بتوهج فوق خلفية نعناعية، ثم يدور بسماكة حقيقية في سماء غروب بنفسجية، يطير إلى باب أخضر في غرفة بنفسجية، يدور في القفل فيُفتح الباب على ضوء ذهبي يغمر الكادر، وينتهي ببطاقة صورة وجملة.
>
> Flat illustration that moves as if 3D: a gold key draws as an outline, fills and floats with a glow over mint, then turns with real thickness against a violet sunset sky, flies to a teal door in a purple room, turns in the lock and the door opens onto golden light that floods the frame, ending on a framed picture beside a short line.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/fake3d
- التصنيفات / Categories: 3d, photos
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 18 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG, CSS

## الفكرة
قصة رمزية قصيرة في 18 ثانية بلا شخصيات: الأشياء نفسها تحكي. المفتاح رمز المعرفة والباب رمز الفرصة. التقنية هي «العمق المزيف»: أشكال متجهية مسطحة بطبقات وسماكة مبثوقة ودوران منظوري وظلال ناعمة، فتبدو مجسمة دون نمذجة ثلاثية كاملة.

## Concept
A short symbolic story in 18 seconds with no characters: objects tell it. The key stands for knowledge, the door for opportunity. The technique is 'fake depth': flat vector shapes with layered extrusion, perspective rotation and soft shadows, so they read as solid without full 3D modelling.

## المشاهد المقترحة
- 0-1.5 ث: خلفية نعناعية متدرجة؛ ولمعة رباعية صغيرة تومض في المنتصف.
- 1.5-4.5 ث: حدود مفتاح تُرسم بخط ذهبي رفيع، ثم تمتلئ بتدرج ذهبي وهالة دافئة؛ وظل تلامس ناعم يظهر تحته وهو يطفو؛ وسطر عربي صغير يظهر في الأعلى (كل الأبواب كانت مغلقة).
- 4.5-6 ث: المفتاح ينقلب على حافته فتظهر سماكته المبثوقة بينما تتغير الخلفية.
- 6-9 ث: أمام غروب من البنفسجي إلى الخوخي بنجوم خافتة، المفتاح يدور بمنظور ويندفع نحو العدسة حتى تملأ حلقته الكادر وتؤطر المشهد التالي.
- 9-13 ث: غرفة بنفسجية بباب فيروزي: المفتاح يطير ويستقيم وينزلق في ثقب القفل، ثم يدور 90° فتظهر حافته.
- 13-15.5 ث: الباب ينفتح؛ ضوء دافئ يتدفق بأشعة قطرية وذرات غبار؛ والكاميرا تندفع عبره إلى ضوء كريمي.
- 15.5-18 ث: قطع إلى صفحة كريمية: صورة الباب في إطار أبيض على جانب وعنوان يظهر كلمة بكلمة بجانبها (المفتاح كان معك)، ثم سطر صغير وتوقيع.

## Proposed scenes
- 0-1.5s: Mint gradient background; a small four-point sparkle twinkles at centre.
- 1.5-4.5s: A key outline draws in thin gold line, then fills with a gold gradient and a warm halo; a soft contact shadow appears under it as it floats; a small Arabic line fades in at the top (all doors were locked).
- 4.5-6s: The key flips edge-on, showing extruded thickness, as the background changes.
- 6-9s: Against a violet-to-peach sunset with faint stars, the key spins in perspective and rushes toward the lens until its bow fills the frame and frames the next scene.
- 9-13s: Purple room with a teal door: the key flies in, aligns and slides into the keyhole, then turns 90° showing its edge.
- 13-15.5s: The door swings open; warm light pours out in diagonal rays with dust specks; the camera pushes through into cream light.
- 15.5-18s: Cut to a cream page: the door picture sits in a white frame on one side while a headline types in word by word beside it (the key was with you), then a small sub-line and a signature.

## قواعد الحركة
- وصفة العمق المزيف: يُكرَّر الشكل المسطح 6-12 مرة بإزاحة على متجه عمق لبناء السماكة مع تغميق النسخ الخلفية؛ والتدوير بتحويلات ثلاثية في CSS أو SVG (دوران رأسي ومنظور 900-1400 بكسل)؛ ويُعاد حساب اتجاه الإزاحة من الدوران في كل إطار.
- ظلال التلامس: قطع ناقص مضبّب تحت الأجسام الطافية يكبر ويخفت مع الارتفاع (طفو 6-10 بكسل على موجة جيبية مدتها ثانيتان).
- الرسم أولًا ثم التعبئة: خط الحدود 400-700 مللي ثانية، ثم تعبئة متدرجة تظهر في 300 مللي ثانية، ثم توهج الهالة.
- الانتقالات يقودها الجسم: المفتاح يندفع نحو العدسة وحلقته تؤطر المشهد التالي (قطع مطابق)، وضوء الباب يبيّض الكادر إلى صفحة النهاية.
- أشعة الضوء: 3-5 حزم قطرية متدرجة ناعمة بشفافية 15-30% مع 20-40 ذرة غبار بطيئة.
- اللوحة: نعناعي #dff1e6 إلى #a9d8c6، ذهبي #e0a03a بإضاءة #f7cf6b وظل #b06c1f، غروب بنفسجي #3b1f5c إلى خوخي #f6c9a8، غرفة بنفسجية #2d1a47، باب فيروزي #1f7f73، ضوء كريمي #fff3d6، صفحة النهاية #eee8dc، والنص #2b2b33.
- الخط: عربي خفيف هادئ (Tajawal أو Readex Pro بوزن 300-500) صغير وساكن؛ وعنوان النهاية 72-96 بكسل؛ والنص لا ينافس الجسم أبدًا.
- المرجع 16:9؛ وفي 9:16 توضع الصورة المؤطرة فوق عنوان النهاية.

## Motion rules
- Fake depth recipe: duplicate the flat shape 6-12 times offset along a depth vector to build extrusion, darken back copies; rotate with CSS/SVG 3D transforms (rotateY, perspective 900-1400 px); recompute the offset direction from the rotation each frame.
- Contact shadows: a blurred ellipse under floating objects, scaling and fading with height (bob of 6-10 px on a 2 s sine).
- Draw-on first, fill second: outline stroke 400-700 ms, gradient fill fade 300 ms, halo bloom after.
- Transitions are object-led: the key rushing to the lens and its ring framing the next scene (match cut), and the door light whiting out to the end page.
- Light rays: 3-5 soft diagonal gradient beams at 15-30% opacity with 20-40 slow dust particles.
- Palette: mint #dff1e6 to #a9d8c6, gold #e0a03a with highlight #f7cf6b and shadow #b06c1f, sunset violet #3b1f5c to peach #f6c9a8, room purple #2d1a47, door teal #1f7f73, light cream #fff3d6, end page #eee8dc, text #2b2b33.
- Type: light, airy Arabic (Tajawal or Readex Pro 300-500), small and quiet; the end headline 72-96 px; text never competes with the object.
- Reference is 16:9; for 9:16 stack the framed picture above the end headline.

## Facts stated by the source (rewritten in our words)
- The reference is a short symbolic piece about a key and a locked door, ending on the idea that the key was with you all along, tied to learning.

## Assumptions
Observed from 24 frames sampled across the 18 s 16:9 reference (fetched from the motion-starter-kit repository): the sparkle, key draw-on and fill, sunset spin and lens rush, door and lock, light flood and framed end page. Hex values are estimated from frames. An audio stream exists but was not analysed. The extrusion technique is inferred from how the key edge appears; the reference may use another method.

## Keywords
2.5d, fake 3d, extrusion, symbolic story, key and door, match cut, light rays, عمق مزيف, ثنائي ونصف الأبعاد, قصة رمزية, مفتاح وباب, ضوء ذهبي, تحريك أجسام
