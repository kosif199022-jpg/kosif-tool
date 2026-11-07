# شخصية متجهية بتحريك هيكلي ومزامنة شفاه — تحريك هيكلي

> شخصية كرتونية متجهية مسطحة مركّبة على هيكل عظمي: تتحرك بمفاصل وإيماءات واضحة، ترمش وتتكلم بمزامنة شفاه مع الصوت، مع حركة ثانوية للشعر والملابس، على خلفية بسيطة بألوان دافئة وتسميات تظهر بجانبها.
>
> A flat vector cartoon character on a bone rig: clear joint-based gestures, blinks and lip sync to the voice-over, secondary motion on hair and clothes, a simple warm background set and short labels or props appearing beside the character as it explains.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: characters
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 30 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
شخصية واحدة ثابتة الهوية تصبح مقدّم المحتوى: تشرح وتشير وتتفاعل مع العناصر. القوة في التمثيل وليس في كثرة المشاهد: وضعيات واضحة، توقيت كوميدي، وتعابير وجه. الهيكل العظمي يسمح بإعادة استخدام الشخصية في كل الفيديوهات بلا إعادة رسم.

## Concept
One character with a fixed identity becomes the presenter: explaining, pointing and reacting to elements. The strength is acting, not many scenes: clear poses, comic timing and facial expressions. The rig lets the character be reused across every video without redrawing.

## المشاهد المقترحة
- 0-2 ث: الشخصية تقفز إلى الكادر بانضغاط وتمدد وتلوّح؛ وترمش بعد الهبوط مباشرة.
- 2-8 ث: وضعية الكلام: مزامنة شفاه مع الصوت، ميل الرأس على الكلمات المنبورة، ويد تشير مع كل فكرة.
- 8-14 ث: أداة أو أيقونة تظهر بجانبها؛ الشخصية تلتفت وتشير وتتفاعل (رفع الحاجبين، الميل للخلف).
- 14-20 ث: حركة من وضعية لوضعية: دورة مشي عبر المكان أو جلوس، مع حركة متداخلة للشعر والأكمام.
- 20-26 ث: النقطة الأساسية: الكاميرا تقترب إلى لقطة قريبة، تعبير قوي يثبت نصف ثانية، وتسمية تُمسح بجانب الوجه.
- 26-30 ث: وضعية الختام بإبهام مرفوع أو انحناءة؛ ثم تخرج الشخصية أو تتجمد لبطاقة النهاية.

## Proposed scenes
- 0-2s: The character pops into frame with a squash-and-stretch hop and a wave; a blink right after landing.
- 2-8s: Talking pose: lip sync to the voice, head tilts on stressed words, one hand gestures on each idea.
- 8-14s: A prop or icon appears beside them; the character turns, points and reacts (eyebrows up, lean back).
- 14-20s: Pose-to-pose action: walk cycle across the set or a sit-down, with overlapping motion on hair and sleeves.
- 20-26s: Key point: the camera pushes to a close-up, a strong expression held 0.5 s, a label wipes in next to the face.
- 26-30s: Sign-off pose with a thumbs-up or bow; the character exits or freezes for the end card.

## قواعد الحركة
- الهيكل: الأجزاء مجموعات SVG منفصلة بنقاط ارتكاز عند المفاصل (الرأس، الجذع، الذراع العليا والسفلى، اليد، الساقان)؛ وتدور هرميًا، ولا يُشوَّه رسم الوجه.
- مزامنة الشفاه: 6-8 أشكال فم تتبدل من توقيتات الكلمات والأصوات، كل شكل يثبت إطارين على الأقل؛ ورمشة كل 2-5 ثوانٍ عشوائيًا (3 إطارات).
- الوضعيات: وضعية رئيسية كل 0.5-1.5 ثانية مع تمهيد (حركة عكسية 5-10%) وتجاوز؛ وتسهيل بين الوضعيات.
- الحركة الثانوية: الشعر والأكمام والإكسسوارات تتأخر عن الجزء الأم 2-4 إطارات بنابض مُخمَّد.
- تنفّس السكون: تكبير رأسي للجذع 1.0-1.015 على موجة جيبية 3 ثوانٍ كي لا تتجمد الشخصية.
- اللوحة: خلفية كريمية دافئة #fff4e6 وأشكال المكان #ffd9b3 و#f5b38a، خط حدود #2b2233 بسمك 4-6 بكسل، والبشرة والملابس من ورقة شخصية ثابتة؛ والتأكيد فيروزي #1fa3a3.
- الخط: التسميات بـCairo أو Tajawal 700 بحجم 48-64 بكسل في شارات مستديرة؛ والكلمات العربية كاملة تُمسح من اليمين لليسار.
- الفرق عن الشخصيات العصوية وإطار بإطار والقصاصات الورقية: العصوية شخصيات خطية؛ وإطار بإطار يُعاد رسمه كل إطار؛ والقصاصات بخامة ورق وحركة متقطعة؛ أما التحريك الهيكلي فشخصية متجهية نظيفة بحركة عظام ناعمة ومزامنة شفاه.

## Motion rules
- Rig: parts as separate SVG groups with pivots at joints (head, torso, upper/lower arm, hand, legs); rotate hierarchically, never deform the face art.
- Lip sync: 6-8 mouth visemes switched from word/phoneme timestamps, hold each at least 2 frames; blink every 2-5 s randomly (3-frame blink).
- Poses: key poses every 0.5-1.5 s with anticipation (5-10% counter move) and overshoot; ease-in-out between keys.
- Secondary motion: hair, sleeves and accessories lag the parent by 2-4 frames with damped spring.
- Idle breathing: torso scale Y 1.0-1.015 on a 3 s sine so the character never freezes.
- Palette: background warm cream #fff4e6 with set shapes #ffd9b3 and #f5b38a, outline #2b2233 at 4-6 px, skin and clothes from a fixed character sheet; accent teal #1fa3a3.
- Type: labels in Cairo or Tajawal 700, 48-64 px, in rounded chips; Arabic words whole, wipe right to left.
- Difference from stickman, frame-by-frame and cutout-paper: stickman is line figures; frame-by-frame is redrawn every frame; cutout-paper has paper textures and stepped motion; character-rig is a clean vector rig with smooth bone animation and lip sync.

## Facts stated by the source (rewritten in our words)
- The public description states nothing specific beyond the title.

## Assumptions
This is an authored KOSIF definition, not an observed reference: there is no reference video for this base style, so palette, type, timings and beats are a design decision written for KOSIF, to be refined per project. Lip sync quality depends on word or phoneme timestamps from the user's audio.

## Keywords
character rig, rigged character, lip sync, vector character, explainer character, pose to pose, تحريك هيكلي, شخصية كرتونية, مزامنة شفاه, شخصية متحركة, مقدم كرتوني, تحريك شخصيات
