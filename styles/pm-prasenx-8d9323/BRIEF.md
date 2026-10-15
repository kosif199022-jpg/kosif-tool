# عرض أعمال بموسيقى مُركّبة بالكود بالكامل — Motion showreel with a fully code-synthesized soundtrack

> خمس عشرة ثانية يقود فيها جدول نوتات واحد الصوت والصورة معًا: كل ضربة طبلة نبضة، وكل قطع يقع على الإيقاع حتمًا.
>
> Fifteen seconds where one note table drives both audio and picture: each kick is a pulse, each cut sits on the grid, and the soundtrack is pure code.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/prasenx-8d9323
- التصنيفات / Categories: charts, kinetic-type, music, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: Remotion, Web Audio, SVG

## الفكرة
الموضوع عرض أعمال لمصمم موشن مدته 15 ثانية بدقة 1920x1080 وبمعدل 60 إطارًا، لكن الشرط الذي يصنع الفكرة أن الموسيقى تُولَّد برمجيًا دون أي عينات أو ملفات صوت أو آلات افتراضية. الاتجاه المقترح: مسار بسرعة 128 BPM يُبنى من مذبذبات بسيطة (طبلة جيبية، هاي هات من ضجيج مُرشَّح، بيس منشاري، لحن مربّع)، ويُشتق كل عنصر بصري من بيانات النوتات نفسها. ما يميز اللغة الحركية أن التزامن مضمون بالبناء لا بالضبط اليدوي، فالصورة والصوت يقرآن الجدول ذاته.

## Concept
The subject is a 15-second motion showreel at 1920x1080 and 60 fps, but the idea-defining constraint is that the music must be generated in code with no samples, audio files or virtual instruments. Proposed direction: a 128 BPM track built from simple oscillators (sine kick, filtered-noise hat, saw bass, square lead), with every visual element derived from the same note data. The distinctive quality is that sync is guaranteed by construction rather than by hand alignment, because picture and sound read one table.

## المشاهد المقترحة
- 0-1.9 ث (المازورة 1): عدّ تمهيدي بالطبلة وحدها؛ نقطة واحدة تنبض مع كل ضربة بينما يظهر اسم المصمم حرفًا حرفًا على ضربات الهاي هات.
- 1.9-5.6 ث (المازورتان 2-3): يدخل البيس؛ شكل مركزي يتحول مرة كل ضربة (دائرة، مربع، مثلث، سداسي) وسماكة الخط تتبع غلاف البيس.
- 5.6-9.4 ث (المازورتان 4-5): أربيجيو اللحن؛ كلمات المهارات تقفز على نوتات الثُمن كطباعة حركية؛ وتدور الكاميرا 90 درجة عند كل خط مازورة.
- 9.4-13.1 ث (المازورتان 6-7): الذروة؛ مخطط أعمدة يرتفع من سعات المذبذبات الفعلية، وتنقلب اللوحة اللونية عند كل مازورة.
- 13.1-15 ث (المازورة 8): ينهار كل شيء نحو المركز في مونوغرام؛ ضربة أخيرة واحدة؛ 200 ms ذيل ثم أسود.

## Proposed scenes
- 0-1.9s (bar 1): Count-in with kick only; a single dot pulses on each kick while the designer's name appears letter by letter on the hats.
- 1.9-5.6s (bars 2-3): Bass enters; a central shape morphs once per beat (circle, square, triangle, hexagon) with the stroke weight following the bass envelope.
- 5.6-9.4s (bars 4-5): Lead arpeggio; skill words snap in on eighth notes as kinetic type; the camera rotates 90 degrees on each bar line.
- 9.4-13.1s (bars 6-7): The drop; a bar-chart equaliser rises from the actual oscillator amplitudes and the palette inverts at every bar.
- 13.1-15s (bar 8): Everything collapses toward the centre into a monogram; one final hit; 200 ms of tail then black.

## قواعد الحركة
- السرعة 128 BPM عند 60 fps تعطي 28.125 إطارًا لكل ضربة؛ تُحسب كل الإطارات المفتاحية من فهرس الضربة ولا تُكتب بالثواني يدويًا.
- القطع الحاد يقع على الإطار floor(beat × 28.125) وعلى الضربتين 1 و3 من المازورة فقط؛ وأي انتقال أطول من نوتة سدس عشر (117 ms) يكون تحولًا لا تلاشيًا متقاطعًا.
- استجابة الطبلة: تكبير من 1.08 إلى 1.0 خلال 220 ms بتلاشٍ أسي يحاكي غلاف سعة الطبلة.
- تحولات الأشكال: 350 ms بمنحنى cubic-bezier(0.65, 0, 0.35, 1)، ومسارات SVG بعدد نقاط متساوٍ حتى تنزلق الرؤوس بدل أن تقفز.
- الطباعة: تدخل الكلمات على شبكة الثُمن (234 ms)، تبقى مازورة واحدة، وتخرج بالتشريح الأفقي على الضربة الأولى التالية؛ خط واحد بوزنين.
- الكاميرا: دورات 90 درجة على حدود المازورات خلال 450 ms بمنحنى ease-in-out؛ لا حركة كاميرا داخل المازورة.
- وصفة الصوت: الطبلة موجة جيبية تنزلق من 150 إلى 50 Hz خلال 120 ms؛ الهاي هات دفقة ضجيج بمرشح علوي مدتها 40 ms؛ البيس موجة منشارية عبر مرشح سفلي عند 300 Hz؛ اللحن موجة مربعة بهجوم 8 ms؛ يُصدَّر عبر OfflineAudioContext أو مُركّب رقمي ويُعاير قرب -14 LUFS.
- ممنوع: العينات، ملفات الصوت، المسارات المسبقة، القطع خارج الشبكة، العشوائية غير المبذورة، وتراكم التوهجات.

## Motion rules
- Tempo 128 BPM at 60 fps gives 28.125 frames per beat; all keyframes are computed from beat indices, never typed as seconds.
- Hard cuts land on frame floor(beat × 28.125) and only on beats 1 and 3 of a bar; any transition longer than a sixteenth note (117 ms) is a morph, not a crossfade.
- Kick response: scale 1.08 to 1.0 over 220 ms with an exponential decay that mirrors the kick's amplitude envelope.
- Shape morphs: 350 ms, cubic-bezier(0.65, 0, 0.35, 1), SVG paths with equal point counts so vertices glide instead of jumping.
- Typography: words enter on the eighth-note grid (234 ms), hold one bar, exit by horizontal slicing on the next downbeat; one typeface, two weights.
- Camera: 90-degree rotations on bar boundaries over 450 ms ease-in-out; no camera motion inside a bar.
- Audio recipe: kick = sine sweeping 150 to 50 Hz over 120 ms; hat = high-passed noise burst of 40 ms; bass = saw through a 300 Hz low-pass; lead = square with 8 ms attack; rendered with OfflineAudioContext or a numeric synth and normalised near -14 LUFS.
- Banned: samples, audio files, pre-rendered stems, cuts off the grid, unseeded randomness, glow stacks.

## Facts stated by the source (rewritten in our words)
- Runtime is 15 seconds at 1920x1080 and 60 fps.
- The soundtrack must be synthesised entirely in code: no samples, no audio files, no plugin instruments.
- Every cut and transition is required to fall on the beat.
- The final deliverable is an MP4 with the music mixed in, and the maker must report where it was saved.
- The piece is framed as a designer's showreel for a résumé.

## Assumptions
The 128 BPM tempo, the oscillator recipe and the bar-by-bar structure are proposals; the source fixes only the duration, resolution, frame rate, code-only audio rule and the on-beat cut rule.

## Keywords
procedural audio, code synth, beat grid, showreel, oscillators, audio reactive, 60fps, صوت مولّد بالكود, مذبذبات, شبكة إيقاع, عرض أعمال, تزامن حتمي, web audio
