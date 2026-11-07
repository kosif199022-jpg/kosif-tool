# شاشة فتح شارة إنجاز ذهبية في تطبيق جوال مع بريق متساقط ومؤشر تفاعلي — Badge unlock screen animation

> لقطة واجهة جوال قصيرة (نحو 11 ثانية) بنسبة قريبة من 4:3: هاتف في المنتصف على خلفية رمادية فاتحة يعرض صفحة «الشارات» بسماء كحلية، شارة سداسية ذهبية يُرسم داخلها شروق ونهر ثم تنفجر حلقة ذهبية وبريق يتساقط ويظهر اسم الشارة، ثم تقترب الكاميرا ومؤشر يد أصفر يلمس الشارة فتنبض وتلمع، وتحتها صف شارات أخرى بعضها مقفل.
>
> A short (about 11 s) near-4:3 mobile UI clip: a phone centred on a light grey canvas shows a 'Badges' screen with a navy sky, a gold hexagon badge whose sunrise-and-river art draws in, then a gold ring burst, falling sparkles and the badge name fading up; the camera pushes in as a yellow hand cursor taps the badge so it pulses and gleams, with a row of other badges, one locked, below.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/bthreeagency-b9b8d9
- التصنيفات / Categories: phone, product-ui, particles
- النسبة المقترحة / Aspect: 1408:1080 · المدة / Duration: 11 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: React, CSS, HTML Canvas, Remotion

## الفكرة
لحظة مكافأة في تطبيق مشي: المستخدم أنهى سبع جولات قبل الفجر فيفتح شارة «المستكشف المبكر». المشهد مبني كاحتفال صغير هادئ بدل الألعاب النارية الصاخبة: ذهب دافئ على كحلي ليلي، والشارة تقف على منصة مضيئة كتحفة في متحف، والبريق يتساقط ببطء على باقي الواجهة. الكاميرا تقترب لتُظهر الملمس ثم تبتعد لتضع اللحظة في سياق الشاشة.

## Concept
A reward moment in a walking app: the user finished seven walks before dawn and unlocks an 'early explorer' badge. The scene is a quiet little celebration rather than loud fireworks: warm gold on night navy, the badge standing on a lit pedestal like a museum piece, and sparkles drifting down over the rest of the interface. The camera moves in to show the texture, then pulls back to place the moment in the screen.

## المشاهد المقترحة
- 0-1.4 ث: إطار سداسي ذهبي فارغ فوق منصة مضيئة أعلى شاشة «الشارات» الكحلية؛ يُرسم الرسم الداخلي: نهر متعرج ثم شمس تشرق بوهج ناعم.
- 1.4-2.4 ث: الفتح: حلقة ذهبية رفيعة تتسع من الشارة وجسيمات ذهبية تنفجر للخارج؛ ويظهر تحتها سطر صغير «شارة جديدة» واسم الشارة مع وصف قصير.
- 2.4-4.5 ث: الوهج اللاحق: بريق ينجرف ويتساقط على الشاشة فوق صف «المناطق» (شارتان مكتسبتان وثالثة باهتة مقفلة بشريط تقدم) وقسم «الأوائل»؛ ومؤشر سهم أصفر كبير ينتظر يميناً.
- 4.5-5.6 ث: المؤشر ينزلق فوق الشارة ويتحول إلى يد تشير.
- 5.6-7.5 ث: الكاميرا تقترب من أعلى الهاتف؛ اليد تنقر فتنبض حلقة هالة ويقفز بريق جديد حول الشارة، ثم تبتعد الكاميرا بهدوء.
- 7.5-11.2 ث: اليد تتحرك حول الشارة وتحتها فتميل الشارة قليلاً مع لمعة متحركة؛ نبضة حلقة ثانية ونثرة بريق أخيرة قبل أن يهدأ الإطار.

## Proposed scenes
- 0-1.4s: The empty gold hexagon outline sits on a glowing pedestal at the top of a navy 'Badges' screen; the illustration draws in: a winding river, then a rising sun with a soft glow.
- 1.4-2.4s: Unlock: a thin gold ring expands from the badge and gold particles burst outward; a small 'new badge unlocked' label and the badge name with a subtitle fade up beneath.
- 2.4-4.5s: Afterglow: sparkles drift and fall across the screen, over the 'Territory' row (two earned badges, one dim locked badge with a progress bar) and the 'Firsts' section; a large yellow arrow cursor waits at the right.
- 4.5-5.6s: The cursor glides in over the badge and changes to a pointing hand.
- 5.6-7.5s: The camera pushes in on the top of the phone; the hand taps, a halo ring pulses and new sparkles pop around the badge, then the camera eases back out.
- 7.5-11.2s: The hand drifts around and under the badge, which tilts slightly with a moving glint; a second ring pulse and a last scatter of sparkles before the frame settles.

## قواعد الحركة
- الخلفية #e7e7ec؛ شاشة الهاتف بتدرج من كحلي عميق #1b2a5e في الأعلى إلى أسود #050608 في الأسفل؛ الذهبي من #e8b85a إلى #f7dc8f مع لمعة دافئة #fff1c4.
- الشارة سداسي بإطار ذهبي فوق قرص منصة داكن بإضاءة حافة زرقاء ناعمة؛ خطوط الرسم الداخلي تُرسم في نحو 0.8 ثانية.
- انفجار الفتح: حلقة رفيعة واحدة تتسع حتى نحو 2.5 ضعف حجم الشارة وتتلاشى في 0.8 ثانية، مع 40–80 جسيم نجمة أو نقطة بسرعة للخارج وجاذبية ووميض.
- تساقط البريق يستمر عدة ثوانٍ بكثافة منخفضة، فوق الواجهة وتحت المؤشر.
- النص: خط نظام بسيط على طريقة iOS؛ التسمية رمادية، اسم الشارة أبيض نصف عريض، الوصف خافت؛ يظهر بارتفاع 8 بكسل.
- الكاميرا: اقتراب ناعم واحد (تكبير من 1.0 إلى نحو 1.8 في 0.8 ثانية بتسارع وتباطؤ)، ثم ثبات، ثم ابتعاد مماثل.
- المؤشر: سهم أو يد صفراء كبيرة بحد داكن وظل؛ النقر = المؤشر يصغر إلى 0.9 مع نبضة حلقة على الشارة؛ والشارة تميل ±6 درجات نحو المؤشر.

## Motion rules
- Canvas #e7e7ec; phone screen gradient from deep navy #1b2a5e at the top to black #050608 at the bottom; gold #e8b85a to #f7dc8f with a warm highlight #fff1c4.
- The badge is a gold-rimmed hexagon on a dark pedestal disc with a soft blue rim light; illustration strokes draw in over ~0.8 s.
- Unlock burst: one thin ring expanding to ~2.5× badge size and fading over 0.8 s, plus 40–80 star/dot particles with outward velocity, gravity and twinkle.
- Sparkle fall continues for several seconds at low density, drawn above the UI but under the cursor.
- Text: small iOS-like system sans; label in grey, badge name semibold white, subtitle muted; fades up with an 8 px rise.
- Camera: one smooth push-in (scale ~1.0 → 1.8 over 0.8 s, ease-in-out), a hold, then a matching pull-back.
- Cursor: oversized yellow arrow/hand with dark outline and drop shadow; tap = cursor scales to 0.9 and a ring pulse on the badge; badge tilts ±6° toward the pointer.

## Facts stated by the source (rewritten in our words)
- The title describes a badge unlock screen animation.

## Assumptions
Observed from 24 frames sampled every ~0.47 s across 11.25 s: the badge draw-in, ring burst, sparkle fall, cursor tap and camera push-in/pull-back. There is no audio track. Badge tilt toward the pointer is inferred from small changes between frames. The 1408×1080 frame is close to 4:3.

## Keywords
badge unlock, achievement, mobile UI, gold sparkle, particles, phone mockup, gamification, cursor tap, شارة إنجاز, فتح إنجاز, واجهة جوال, بريق ذهبي, تحفيز, تطبيق مشي
