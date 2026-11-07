# آلة موسيقية فيزيائية تعزف فيها الكرات بالارتطام — Collision-driven music machine

> مقطع مدته 47 ثانية لآلة موسيقية فيزيائية على خلفية كحلية شبه سوداء: أربعة صفوف آلات مرسومة بخطوط رفيعة (أجراس معدنية زرقاء، ماريمبا برونزية مع أنابيب رنين، صنجات ذهبية، قضبان باص بنفسجية، وطبول حمراء)، ومدافع صغيرة تطلق كرات متوهجة بذيول تسقط بالجاذبية على المفاتيح فتضيء كل مفتاح عند الضرب، مع عنوان مقطوعة وعداد نوتات وزمن في الأعلى.
>
> A 47-second physics music machine on a near-black navy ground: four rows of thin-line instruments (blue glockenspiel bars, bronze marimba with resonator tubes, gold cymbals, violet bass bars and red drums) while small cannons fire glowing comet-tailed balls that fall under gravity onto the keys, each key flashing as it is struck, with a piece title, note counter and timer at the top.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://www.promptsmotion.com/kamstudiolabs-447565
- التصنيفات / Categories: music, particles, shapes
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 47 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: HTML Canvas, Web Audio, React, Remotion

## الفكرة
الفكرة أن الموسيقى «مرئية وصادقة»: كل نوتة تسمعها هي ارتطام كرة حقيقي بمفتاح محدد، محسوب بالجاذبية بحيث يصل في وقته. كل آلة لها لون (أزرق جليدي، برونزي، ذهبي، بنفسجي، أحمر) والكرات بلون آلتها. اللقطة ثابتة طوال الوقت، والدراما تأتي من كثافة الكرات وتوهج الضربات.

## Concept
Music made visible and honest: every note you hear is a real ball hitting a specific key, solved with gravity so it arrives on time. Each instrument has a colour (ice blue, bronze, gold, violet, red) and the balls share their instrument's colour. The shot is locked throughout; drama comes from ball density and hit glows.

## المشاهد المقترحة
- 0-4 ث: الآلة كاملة معروضة وخافتة؛ أولى الكرات البرونزية تنطلق بأقواس من مدافع الماريمبا وتضيء مفاتيح منفردة؛ وكتلة العنوان وعداد يبدأ من الصفر أعلى اليسار واليمين.
- 4-10 ث: مدافع الأجراس والباص تنضم: كرات زرقاء جليدية وبنفسجية بذيول قصيرة تسقط على قضبانها؛ والمفاتيح المضروبة تضيء وترتد قليلاً.
- 10-18 ث: تدخل الصنجات والطبول: كرات ذهبية تضرب الصنج بوهج حلقي متلألئ؛ وكرات حمراء تقع على الطبل والطبلة الكبيرة بهالة حمراء تتسع.
- 18-38 ث: الفرقة كاملة: عدة كرات في الهواء معاً عبر كل الصفوف والضربات تتوهج بالتتابع؛ شريط تقدم مقسم أعلى الشاشة يمتلئ قسماً قسماً وعداد النوتات يصعد.
- 38-45 ث: الكثافة تقل؛ دفعة أخيرة من الكرات من المدافع اليمنى تقع عبر الصفوف وتنتهي في أكواب التجميع عند الأطراف.
- 45-47 ث: آخر الكرات تسقط في الأكواب والمفاتيح تعود خافتة؛ العداد والزمن يكتملان؛ وثبات.

## Proposed scenes
- 0-4s: The full machine is laid out and dim; the first few bronze balls arc from the marimba cannons and light single bars; the title block and a '0 notes' counter sit top-left/right.
- 4-10s: Glockenspiel and bass cannons join: ice-blue and violet balls with short comet tails fall onto their bars; struck keys brighten and bounce slightly.
- 10-18s: Cymbals and drums enter: gold balls hit the hi-hat and crash with a shimmering ring glow; red balls land on snare and kick with an expanding red halo.
- 18-38s: Full ensemble: several balls in flight at once across all rows, hits glowing in sequence; a segmented progress bar along the top fills section by section and the note counter climbs.
- 38-45s: Density thins; a last flurry of balls from the right side cannons lands across rows into catch cups at the ends.
- 45-47s: The final balls drop into the cups, keys fade back to dim; the counter and timer read complete; hold.

## قواعد الحركة
- لقطة عريضة ثابتة بلا قطع ولا حركة كاميرا طوال المدة؛ وكل شيء تقوده النوتة الموسيقية.
- كل نوتة = كرة واحدة تنطلق من مدفع صفها في قوس مقذوف (جاذبية ثابتة) محسوب لتصل تماماً عند بداية النوتة؛ والمدفع يرتد قليلاً عند الإطلاق.
- رد فعل الضربة: المفتاح المضروب يومض بكامل سطوعه مع توهج ناعم وانخفاض 2-4 بكسل، ويخبو في نحو 300 مللي ثانية؛ الطبول بحلقة هالة تتسع والصنجات بقطع ناقص متلألئ.
- الكرات نقاط متوهجة بذيول مذنب تتلاشى (8-12 عينة أثر) وتنتهي في أكواب تجميع عند أطراف الصفوف.
- اللوحة: خلفية #0b0f1a بتظليل ناعم؛ أجراس أزرق جليدي #7fc4d8، ماريمبا برونزي #c9954a، صنجات ذهبي #e0c060، باص بنفسجي #8f7ae6، طبول أحمر #e0585a؛ وتسميات خافتة #6f7690.
- الخط: سيريف مائل أنيق لعنوان المقطوعة، وخط أحادي المسافة صغير لتسميات المفاتيح ومعلومات الإيقاع والمقام والزمن وعداد النوتات؛ وشريط تقدم مقسم رفيع أعلى الإطار.

## Motion rules
- Locked wide shot, no cuts, no camera moves for the full length; everything is driven by the score.
- Each note = one ball launched from its row's cannon on a ballistic arc (constant gravity) timed to land exactly on the note onset; the cannon recoils slightly on fire.
- Hit feedback: the struck key flashes to full brightness with a soft bloom and a 2-4 px dip, decaying over ~300 ms; drums get an expanding halo ring, cymbals a shimmering ellipse.
- Balls are glowing dots with fading comet tails (~8-12 trail samples) and end in catch cups at row ends.
- Palette: background #0b0f1a with soft vignette; glockenspiel ice blue #7fc4d8, marimba bronze #c9954a, cymbals gold #e0c060, bass violet #8f7ae6, drums red #e0585a; labels muted #6f7690.
- Type: elegant italic serif for the piece title, small monospace for key labels, tempo/key info, timer and note counter; thin segmented progress bar at the top edge.

## Facts stated by the source (rewritten in our words)
- The piece is a music machine in which collisions between objects produce the notes.
- The record tags it under music only; the prompt is short (about 19 words).

## Assumptions
Observed from 24 frames sampled every ~1.96 s across 47 s plus two full-resolution stills: the five colour-coded instrument rows, cannons and catch cups, comet-tailed balls, hit glows, title/counter/timer HUD and segmented progress bar. Assumed: that hits are exactly synced to the audio (the audio track exists but was not analysed), the section boundaries (estimated from ball density) and hex values.

## Keywords
music machine, physics, bouncing balls, audio visualizer, glockenspiel, marimba, generative music, collision, glow, آلة موسيقية, فيزياء, كرات مرتدة, تصوير الموسيقى, ارتطام, موسيقى توليدية
