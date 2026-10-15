# فيلم إطلاق نموذج صور بأسلوب مختبرات الذكاء — Ora 2 image model launch film

> فيلم إطلاق مربع مدته 22 ثانية: لوحة بيضاء، خط واحد، صور حقيقية، تعليق صوتي مُولَّد وترجمة تُكتب كلمةً بكلمة وقت نطقها، وعناصر تحكم زجاجية.
>
> A 22-second square launch film in the AI-lab idiom: white canvas, one typeface, real imagery, generated voiceover with word-synced captions and liquid-glass controls.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/rossaxbt-3085b7
- التصنيفات / Categories: product-ui, kinetic-type, shapes, characters, photos, music, code
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 22 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: HTML Canvas, Web Audio

## الفكرة
الموضوع إطلاق نموذج توليد صور، والرسالة أن النموذج يملك «ذوقاً» ويتكيف مع أي أسلوب. الهدف التواصلي هو إيصال تسع جمل قصيرة من التعليق الصوتي بثقة ودون ضجيج بصري. ما يميز لغة الحركة أن جدول الكلمات يقود كل شيء: الترجمة تُكتب في لحظة النطق تماماً، الصور تتبدل على أنصاف النبضات (16th notes)، عناصر التحكم زجاج سائل يكسر المشهد خلفه، والكاميرا تنجرف باستمرار وتورّث قيمة التكبير من مشهد إلى الذي يليه.

## Concept
The subject is an image-model launch whose message is that the model has taste and adapts to any style. The communication goal is to land nine short voiceover lines confidently with no visual noise. The distinctive motion language: the word table drives everything. Captions type at the exact moment of speech, images switch on 16th notes, controls are liquid glass refracting the scene behind them, and the camera drifts continuously, inheriting its zoom from scene to scene.

## المشاهد المقترحة
- 0-3 ث: «هذا هو [الاسم]»: كولاج فضفاض من صور المنتج ينجرف للخارج بينما يُكتب الاسم بحجم كبير؛ سطر الفئة يحل محله مع انتهاء العبارة الأولى.
- 3-6 ث: «مصنوع من أجل [القيمة]»: صور بطلة بملء الإطار تتبدل مع نقرات على أنصاف النبضات، متسارعة نحو الدروب الموسيقي، والسطر يُكتب بالأبيض فوقها.
- 6-9.5 ث: الدروب على سطر [الفعل]: شريط أوامر زجاجي يكتب طلباً قصيراً؛ بطاقة النتيجة تغيّر أسلوبها على كل نصف نبضة بينما تتدحرج شريحة سوداء إلى اسم كل أسلوب فوق شريط مصغرات.
- 9.5-12.5 ث: لوحة الإلهام: تسع صور تطير إلى شبكة 3×3 ثم تدور حول النتيجة المولّدة بينما تُكتب عبارة «إنه يفهمك».
- 12.5-15 ث: سطران من الترجمة؛ الكلمة المؤكدة الوحيدة تُكتب بتدرج ألوان العلامة مع توهج خافت وصوت هبوط ناعم.
- 15-22 ث: لوحة إعدادات بثلاثة منزلقات زجاجية تتحرك مع ذكر كل منها (تغيير الصبغة، إعادة البذرة على أنصاف النبضات، تحويل إلى ملصق)؛ ثم تنفجر 120 صورة من المركز خلف كبسولة ترجمة زجاجية وتتجمع في الشعار مع كتابة الاسم؛ «متاح الآن» أسفله مع ثبات ثانيتين.

## Proposed scenes
- 0-3s: 'This is [name]': a loose collage of the product's images drifts outward while the name types in large; the category line replaces it as the first phrase ends.
- 3-6s: 'built for [value]': full-bleed hero images flip on 16th-note clicks, accelerating into the music drop, with the line typed in white over them.
- 6-9.5s: The drop on the [Verb] line: a glass prompt bar types a short request; the result card restyles on every 16th while a black chip rolls to each style name above a thumbnail strip.
- 9.5-12.5s: Moodboard: nine images fly into a 3x3 grid, then orbit the generated result as the 'it understands' caption types on.
- 12.5-15s: Two caption lines; the single emphasised word types in a brand-colour gradient with a faint glow and a soft landing sound.
- 15-22s: Settings panel with three glass sliders moving as each is named (hue shift, seed re-roll on 16ths, poster conversion); then 120 images burst from the centre behind a glass caption pill and gather into the logo as the name types; 'Out now' beneath, hold 2 s.

## قواعد الحركة
- لا شيء يظهر فجأة: كل عنصر يدخل بمنحدر شفافية لا يقل عن 300 مللي ثانية (ease-out quad أو ألين)؛ التلاشي خلال 50 مللي ثانية يُقرأ كظهور مفاجئ ويُرفض.
- الكاميرا تنجرف باستمرار: كل مشهد يدفع من 1.00 إلى نحو 1.04، والمشهد التالي يبدأ من قيمة التكبير التي انتهى عندها السابق؛ إعادة الضبط إلى 1.00 عند التسليم ممنوعة.
- تبديل الصور يقع فقط على أنصاف النبضات في شبكة إيقاع المقطوعة، مع مؤثر نقرة موضوع عند ذروته المقاسة؛ هذه السلاسل هي المواضع الوحيدة المسموح فيها بقفزات إطار واحد.
- تغييرات المشاهد تهبط على بدايات العبارات من جدول الكلمات؛ الدروب الموسيقي يوضع على سطر [الفعل] وتُثبّت شبكة الإيقاع عنده.
- الترجمة تُكتب كلمة كلمة عند أزمنة البدء المقاسة (محاذاة Whisper لكل مقطع مفصول بوقفة)؛ النقاط الختامية لا تظهر على الشاشة أبداً.
- الزجاج السائل: ضبّب المشهد خلف الشكل (نحو 14 بكسل)، ضع فوقه نسخة مضببة قليلاً ومكبّرة بنحو 1.06x ضمن شريط ضيق قرب الحافة (نحو 12 بكسل)، ثم أضف طبقة حليبية ولمعة علوية وحافة مضيئة وظلاً مرفوعاً؛ على الأبيض الخالص ضع هالة باستيل بطيئة أو غسلة صورة مضببة خلفه ليُقرأ الزجاج.
- الخط: خط العلامة الواحد (Geist افتراضياً)، حبر أسود على أبيض؛ الكلمة المؤكدة الوحيدة بتدرج ألوان العلامة؛ لا صناديق تظليل لأنها تُقرأ كتحديد نص.
- ممنوع: الصدمات المثبتة على النبضة، الومضات البيضاء، الأبعاد الثلاثية، تظليل التحديد، القوالب؛ الصوت يُخفض بـ sidechain ثلاثي النطاقات ويُطبّع إلى -14 LUFS.

## Motion rules
- Nothing pops: every element fades in with an eased opacity ramp of at least 300 ms (ease-out quad or softer); a 50 ms fade reads as a pop and is rejected.
- The camera drifts continuously: each scene pushes from 1.00 to about 1.04, and the next scene starts at the zoom the previous one ended on; resetting to 1.00 at a handoff is forbidden.
- Image swaps happen only on 16th-note subdivisions of the track's beat grid, each with a click SFX positioned at its measured peak; these runs are the only places single-frame jumps are allowed.
- Scene changes land on phrase onsets from the word table; the music drop is placed on the [Verb] line and the beat grid is anchored there.
- Captions type word by word at measured onset times (Whisper alignment per pause-split segment); full stops are never shown on screen.
- Liquid glass: blur the scene behind the shape (~14 px), overlay a faintly blurred, slightly enlarged (~1.06x) copy within a narrow ~12 px band at the rim, then layer milkiness, a top sheen, a bright edge and a lifted shadow; on plain white, place a slow pastel aura or a blurred photo wash behind it so the glass reads.
- Typography: one brand typeface (Geist by default), black ink on white; the one emphasised word is a gradient of brand colours; no highlight boxes, which read as text selection.
- Banned: beat-snapped slams, white flashes, 3D, selection-box highlights, templates; audio is ducked with a 3-band sidechain and normalised to -14 LUFS.

## Facts stated by the source (rewritten in our words)
- Square 1440x1440 film at 60 fps lasting 22 seconds, built on one HTML canvas with a seek(t) function and rendered with Playwright using 8 motion-blur subframes.
- Visual idiom: white canvas, a single typeface, black ink, real photographs or product outputs; controls are rendered as liquid glass.
- A nine-line voiceover template is adapted to the product and synthesised with ElevenLabs (four takes, per-line regeneration), then aligned with Whisper per pause-split segment.
- Seven scenes timed to the voice: name collage, value flashes, prompt-bar drop, moodboard grid, emphasised-word lines, settings sliders, image burst into logo with an 'Out now' hold.
- Camera drift 1.0 to 1.04 per scene, eased fades of 0.3 s minimum, image changes on 16th notes with clicks, scene changes on phrase starts, drop on the verb line.
- Sound: 3-band sidechain ducking, voice about 9 dB over music in the speech band, one SFX per event, loudnorm to -14 LUFS.
- The agent must gather inputs, write the script, offer four voice takes and eight stills before rendering.

## Assumptions
Scene durations in seconds are proposed to fit 22 s and will shift with the actual voice read; the default product name, voice, images and track named in the source are placeholders to be replaced by the client's own licensed assets. The listing's duration tags (39, 28, 2) are ignored in favour of the stated 22 s.

## Keywords
ai launch film, image model, liquid glass, word-synced captions, voiceover, elevenlabs, 16th note cuts, sidechain ducking, canvas, فيلم إطلاق, ترجمة متزامنة, تعليق صوتي, زجاج سائل, نموذج صور
