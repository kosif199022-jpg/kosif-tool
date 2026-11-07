# شخصية فوكسل تُبنى وتُركّب لها مفاصل وترقص مع لوحة سجل حية — Dancing voxel character built in Blender

> فيديو عمودي مدته 16 ثانية بقسمين: في الأعلى مشهد فوكسل ثلاثي الأبعاد على أرضية بنفسجية بنجوم، فيه مكعب برتقالي لطيف بوجه يشير بشعاع ليبني رجلاً بنظارة شمسية وشارب وبدلة خردلية طبقة طبقة، ثم تُضاف المفاصل ويرقص الاثنان؛ وفي الأسفل لوحة داكنة بتبويبات المراحل وشريط تقدم وخط إيقاع بنقاط مفاتيح وسجل أوامر يُكتب سطراً سطراً.
>
> A 16-second vertical split: on top, a voxel 3D scene on a periwinkle floor with stars where a cute orange cube character beams a builder ray to assemble a moustached, sunglassed man in a mustard suit layer by layer, rigs him and both dance; below, a dark dashboard with stage tabs, a progress bar, a beat grid of key-pose diamonds and a command log typing line by line.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://www.promptsmotion.com/y0urdumble-f06276
- التصنيفات / Categories: 3d, characters, code
- النسبة المقترحة / Aspect: 1080x1500 · المدة / Duration: 16 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Three.js, React, Remotion

## الفكرة
الفكرة إظهار عملية الصنع والنتيجة معاً: النصف العلوي هو «ما يحدث في برنامج ثلاثي الأبعاد»، والنصف السفلي هو «ما يُرسل إليه من أوامر». كل سطر في السجل يقابله جزء جديد يظهر في المشهد، وشريط الإيقاع يتقدم مع الرقص، فيفهم المشاهد البناء ثم التركيب ثم الحركة دون شرح.

## Concept
The idea is to show the making and the result together: the top half is 'what happens in the 3D app', the bottom half is 'the commands sent to it'. Every log line matches a new part appearing in the scene, and the beat bar advances with the dance, so the viewer gets build, rig and animate without narration.

## المشاهد المقترحة
- 0-1 ث: الاتصال: المكعب يلوّح على الأرضية البنفسجية؛ أعلى اليسار وسم أسود ووسم فرعي برتقالي؛ والسجل يطبع سطر الاتصال وتبويب «العملية كاملة» مضاء.
- 1-7 ث: البناء: شعاع برتقالي من المكعب يرسم مستطيلاً سلكياً تتراكم فيه المكعبات: حذاء أخضر، ساقان خردليتان، بدلة، قميص وربطة، ذراعان، رأس، نظارة وشارب، وتسريحة وردية؛ وعداد المكعبات وشريط التقدم يصعدان مع كتابة كل سطر في السجل.
- 7-10 ث: المفاصل: يضيء تبويب «التركيب»؛ علامات مفاصل برتقالية تنبثق على الشخصية، فتأخذ وضعية T للاختبار ثم تعود.
- 10-15 ث: الرقص على 120 نبضة في الدقيقة: الشخصيتان تقفزان مع الإيقاع، الرجل يرفع يديه ويدور، والمكعب ينضغط ويبتسم؛ نجوم وردية وخضراء وقصاصات تنجرف؛ ورأس التشغيل يعبر معينات الوضعيات الوردية.
- 15-16 ث: يُطبع سطر التصيير مع علامة نجاح؛ والشخصيتان تثبتان في وضعية سعيدة.

## Proposed scenes
- 0-1s: Connect: the cube character waves on the periwinkle floor; top-left a black label and an orange sub-label; the log prints a connect line and the 'Full process' tab is lit.
- 1-7s: Build: an orange beam from the cube draws a wire rectangle where voxels stack up: green shoes, mustard legs, suit, shirt and tie, arms, head, sunglasses and moustache, a pink pompadour; the voxel counter and progress bar climb as each log line types.
- 7-10s: Rig: the 'Rig' tab lights; orange joint markers pop on the figure, it snaps to a T-pose test and back.
- 10-15s: Dance at 120 bpm: both characters bounce on the beat, the man raises the roof and spins, the cube squashes and grins; pink and green stars and confetti drift; the playhead crosses the pink key-pose diamonds.
- 15-16s: Render line prints with an OK; both characters hold a happy pose.

## قواعد الحركة
- تخطيط منقسم في إطار عمودي: نحو 55% مشهد ثلاثي الأبعاد في الأعلى و45% لوحة واجهة داكنة في الأسفل، يفصلهما خط برتقالي رفيع.
- المظهر الثلاثي: مكعبات فوكسل كبيرة بحد أبيض وتظليل كرتوني ناعم، أرضية بنفسجية #7b7fe6 بنقش أغمق، المكعب برتقالي محمر #d9563a بخدود وردية، البدلة خردلية #c9a12a، الحذاء أخضر #2fb36a، والشعر وردي #e05aa8.
- الواجهة: لوحة #141418، برتقالي #ff7a2f للتبويبات النشطة والتقدم والمؤشر، وردي #ff5c8a لمفاتيح الرقص، ونص سجل أحادي المسافة رمادي فاتح؛ مع وسوم صغيرة متباعدة وقراءة للإطار والنبضة أعلى اليمين.
- تزامن البناء: كل سطر أمر يُكتب في نحو 300-500 مللي ثانية والكتلة المقابلة تظهر داخل صندوق الشعاع في اللحظة نفسها.
- الرقص على شبكة 120 نبضة في الدقيقة (500 مللي ثانية للنبضة): القفزات تهبط على النبضات، ووضعيات مفتاحية كل 2-4 نبضات، وانضغاط وتمدد للمكعب.
- الكاميرا: زاوية ثلاثة أرباع ثابتة بانجراف خفيف؛ بلا قطع في 16 ثانية.

## Motion rules
- Split layout in a portrait frame: about 55% 3D viewport on top, 45% dark UI panel below, separated by a thin orange line.
- 3D look: chunky voxels with white outline stroke, soft toon shading, floor periwinkle #7b7fe6 with darker speckle, cube character orange-red #d9563a with pink blush, suit mustard #c9a12a, shoes green #2fb36a, hair pink #e05aa8.
- UI: panel #141418, orange #ff7a2f for active tabs, progress and caret, pink #ff5c8a for dance keys, light grey monospace log text; small tracked labels and a frame/beat readout top-right.
- Build sync: each command line types in about 300-500 ms and the matching voxel block appears within the beam's wire box at the same moment.
- Dance on a 120 bpm grid (500 ms per beat): bounces land on beats, key poses every 2-4 beats, squash-and-stretch on the cube.
- Camera: fixed three-quarter view with slight drift; no cuts in 16 s.

## Facts stated by the source (rewritten in our words)
- It shows a voxel character being built, rigged and made to dance through an AI agent controlling Blender.
- The listing tags characters, music and code; it is shared as a skill.

## Assumptions
Observed from 24 frames sampled every ~0.67 s across 16 s: the connect, build, rig and dance stages, the beam and wire box, the dashboard tabs, beat grid and typed log. The original was rendered in Blender; KOSIF would rebuild it with Three.js voxels and a React panel. The 120 bpm figure is read from the on-screen panel; an audio track exists but was not analysed. Source frame is 720x1000 (record lists 1080x1500).

## Keywords
voxel, 3D character, build process, auto rig, dance loop, command log, beat grid, split screen, vertical, فوكسل, شخصية ثلاثية الأبعاد, بناء الشخصية, رقص, سجل أوامر, شاشة منقسمة
