# سباق مركبة فوكسل في صحراء بشمسين — Voxel pod-racer run

> تسجيل شاشة مدته نحو 10 ثوانٍ للعبة سباق ثلاثية الأبعاد في المتصفح بعالم مكعبات (فوكسل): بطاقة عنوان داكنة بحروف برتقالية، ثم كاميرا خلف مركبة سباق بمحركين مشتعلين تنطلق بين أعمدة وأقواس صخرية بنية فوق رمال برتقالية وسماء زرقاء بشمسين، وتترك ذيولاً من مكعبات صفراء متطايرة مع خطوط سرعة وعداد سرعة وشريط دفع.
>
> A roughly 10-second browser screen capture of a voxel 3D racer: a dark title card with orange pixel lettering gives way to a chase camera behind a twin-engine pod that weaves between brown block rock pillars and arches over orange sand under a two-sun blue sky, trailing yellow cube sparks with speed streaks, a speed readout and a boost bar.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/ivanfioravanti-bd9261
- التصنيفات / Categories: 3d, particles
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 10 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Three.js, WebGL, HTML Canvas

## الفكرة
الموضوع لعبة سباق مركبات صحراوية مبنية كلها من مكعبات، تُعرض كلقطة لعب حقيقية مسجلة من المتصفح. الجمال هنا في البساطة: كل شيء مكعبات بألوان دافئة، والإحساس بالسرعة يأتي من الذيول المتطايرة وخطوط الريح وانعطافات الكاميرا، لا من التفاصيل. المركبة محركان مشتعلان يربطهما شعاع وردي وقمرة رمادية بينهما.

## Concept
The subject is a desert pod-racing game built entirely from cubes, shown as real gameplay captured in the browser. The appeal is its simplicity: everything is warm-coloured blocks, and the sense of speed comes from scattering spark trails, wind streaks and banking camera moves rather than detail. The craft is two flaming engines tethered by a pink beam with a grey cockpit between them.

## المشاهد المقترحة
- 0-0.4 ث: لوحة عنوان بنية داكنة شبه شفافة بحروف مكعبة برتقالية «VOXEL PODRACER» مع تلميحات تحكم صغيرة وطلب البدء، فوق صحراء ضبابية.
- 0.4-1.5 ث: تختفي اللوحة؛ الكاميرا منخفضة خلف المركبة وهي تنطلق بين كتلتين صخريتين بنيتين نحو قوس بعيد، والمكعبات الصفراء تتناثر من المحركين.
- 1.5-3 ث: مراوغة في وادٍ بجدران صخرية متدرجة تملأ أطراف الكادر؛ ورقم السرعة أعلى اليسار يقفز مع الدفع.
- 3-5 ث: المركبة تصعد وتميل بقوة نحو السماء، والمحركان يرسمان أقواساً من مكعبات صفراء وداكنة، بينما الكاميرا تبقى على الأرض والأقواس.
- 5-7.5 ث: دفع بأقصى سرعة: خطوط سرعة بيضاء تعبر الكادر، والمركبة تمر فوق أبراج أعمدة مكدسة بذيول شرر طويلة، وشريط الدفع يفرغ.
- 7.5-10 ث: عودة منخفضة عبر أقواس الصخر، والمرور من بوابة مع دفقة شرر أخيرة.

## Proposed scenes
- 0-0.4s: A dark brown translucent title panel with orange blocky 'VOXEL PODRACER' lettering, small control hints and a start prompt, over a blurred desert.
- 0.4-1.5s: The panel fades; the chase camera sits low behind the pod as it launches between two large brown rock masses toward a distant arch, yellow cubes spraying from both engines.
- 1.5-3s: Weaving through a canyon of stepped rock walls that fill the frame edges; the speed number top-left jumps as boost kicks in.
- 3-5s: The pod climbs and banks hard into the sky, engines looping in arcs of yellow and dark cubes, while the camera holds on the ground and arches.
- 5-7.5s: High-speed boost: white speed streaks cross the frame, the pod skims over stacked pillar towers with long spark trails and the boost bar drains.
- 7.5-10s: Back low through rock arches, threading a gate with a final burst of sparks.

## قواعد الحركة
- كل شيء فوكسل: أرض بمربعات رملية بدرجتين متناوبتين، صخور ككتل مكدسة، وجسيمات كمكعبات صغيرة؛ بلا مجسمات ناعمة.
- كاميرا مطاردة على بعد 2-4 أمتار خلف المركبة مع تأخر وميل في الانعطافات؛ وتبقى قرب الأرض حين تقفز المركبة فتخرج أحياناً من أعلى الكادر.
- كل محرك يطلق ذيل مكعبات: مكعبات صفراء ساطعة #f2d548 تتحول إلى زيتوني وداكن #2a2418، تعيش نحو 0.6 ثانية وتتناثر للخارج.
- إشارات السرعة: خطوط بيضاء رفيعة تمر أثناء الدفع واتساع خفيف لزاوية الرؤية؛ بلا ضبابية حركة.
- اللوحة: سماء #8fbbd9 تتدرج إلى ضباب #f0d3a8 عند الأفق، رمل #d99b5c / #c98a4f، صخر #6e3d24 / #4e2a18، لهب #ff9a2a، شعاع وردي #ff7bd0، مركبة #4a4a4e.
- شمسان باهتتان ثابتتان أعلى السماء بتوهج ناعم؛ إضاءة دافئة مسطحة مع ضباب خفيف نحو الأفق.
- الواجهة بسيطة: رقم السرعة أعلى اليسار بخط أحادي أبيض، وشريط دفع برتقالي رفيع أسفل الوسط.

## Motion rules
- Everything is voxel: terrain tiles in two alternating sand tones, rocks as stacked blocks, particles as small cubes; no smooth meshes.
- Chase camera 2-4 m behind the pod with lag and roll on turns; it stays near the ground when the pod jumps, so the craft can leave the frame upward.
- Each engine emits a cube trail: bright yellow #f2d548 cubes fading to olive and dark #2a2418 cubes, living about 0.6 s and scattering outward.
- Speed cues: thin white streak lines flying past at boost, and slight FOV widening; no motion blur.
- Palette: sky #8fbbd9 to haze #f0d3a8 at the horizon, sand #d99b5c / #c98a4f, rock #6e3d24 / #4e2a18, flame #ff9a2a, beam pink #ff7bd0, pod #4a4a4e.
- Two pale suns sit fixed in the upper sky with a soft bloom; light is warm and flat with mild fog toward the horizon.
- HUD is minimal: speed number top-left in white mono, a thin orange boost bar bottom centre.

## Facts stated by the source (rewritten in our words)
- The piece is titled as a voxel pod-racer run.
- It is listed as made with the Kimi K3 model.
- No category, duration or tech stack is stated on the record.

## Assumptions
Observed from 24 frames sampled every ~0.42 s over the full 10 s: the title panel, the chase-camera run through rocks and arches, cube spark trails, speed streaks and the HUD. The source is a macOS browser screen recording (720x466 with browser chrome), so the 16:9 aspect is assumed for a clean reproduction; there is no audio track. Exact physics, controls and the meaning of the HUD numbers are inferred.

## Keywords
voxel, racing game, pod racer, desert, chase camera, particle trail, browser game, 3d gameplay, فوكسل, لعبة سباق, صحراء, مكعبات, لقطة لعب, ثلاثي الأبعاد
