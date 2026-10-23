# الرسم والشخصيات — Drawing, painting and characters

رسم شخصيات ومشاهد أصلية بالكود، والطلاء بالفرشاة، وتحريك الذراع بـ IK والجسم كاملًا على توقيت الكلمات.

Original code-drawn characters and scenes, brush painting, arm IK and full-body animation on word timing.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:draw:start -->

**الأدوات / tools (13)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `character-fullbody` | Renders a layered 2D full-body character that walks, runs, waves, smiles, blinks and nods on time or word cues, using two-bone IK for legs and arms, and exports PNG/SVG stills or GIF/H.264 MP4 with optional packet-verified original AAC audio. | `python3 scripts/character_fullbody.py doctor` | tested-here |
| `character-ik` | Animates a simple drawn character's arm with analytic two-bone inverse kinematics toward targets cued by time or verified word timestamps, exporting PNG/SVG stills or GIF/H.264 MP4, optionally with the original AAC narration stream-copied and checked by packet hashes. | `python3 scripts/character_ik.py doctor` | tested-here |
| `code-drawing-master` | Generates an editable 1080x1920 Motion Director storyboard JSON, plus an optional self-contained seekable HTML preview, in which procedural vector human and/or cat characters draw on in a street or park with six actions, three moods and optional real word timestamps. | `python3 scripts/code_drawing_master.py --cast human+cat --expression happy --location street --action walk --out ./story.json --html ./story.html` | tested-here |
| `creative-paint` | Paints a strict JSON layered scene (rectangles, ellipses, lines, polygons, pressure brush strokes, text) with Pillow into PNG/SVG stills, or animates whole layers with keyframes into a GIF or H.264 MP4. | `python3 scripts/creative_paint.py doctor` | tested-here |
| `smart-draw` | Turns freehand stroke JSON into a layered drawing, optionally snapping each stroke to a rectangle, ellipse or straight line with deterministic geometry, then reports the recognized shapes or renders the drawing to PNG/SVG. | `python3 scripts/smart_draw.py doctor` | tested-here |
| `unified-draw` | Combines Smart Draw freehand stroke snapping, Creative Paint layered shapes and text, and keyframed GIF/MP4 animation behind one ordered scene and CLI. | `python3 scripts/unified_draw.py doctor` | tested-here |
| `creative-principles` | Builds original SVG drawing stages, three-value tone breakdown, and intercut tonal distribution flags from supplied arrays. | `python3 scripts/creative_principles.py construct --input original-shapes.json --out-prefix out/stage` | tested-elsewhere |
| `drawing-academy` | Eight source-anchored skill lessons, rights-scoped text keyword scans, scores tied to actual artifacts and provenance. | `python3 scripts/drawing_academy.py index` | tested-elsewhere |
| `drawing-methods` | 48 original method cards distilled from drawing books, including 41 books from the user's own library read on 2026-10-23 (text, OCR or sample pages) (gesture, proportion, Loomis head, mannequin, shape language, silhouette, expression, light, cast shadows, hatching, anime heads, hair and cel shading, animation timing, walks, urban sketching, plants, products, creatures, practice); ranks them for an Arabic or English request, builds an ordered drawing plan or an image prompt, draws a head, figure, character, forms, a bouncing ball or a constructed cast shadow as a deterministic layered SVG (guide, construction, final, silhouette) and checks the drawing's geometry against the cards. | `python3 scripts/drawing_methods.py find "ارسم وش شخصية بتضحك"` | tested-here |
| `portrait-pipeline` | Turns any photo (portrait, object, place) or any scene Claude imagines into a hand-drawn-looking drawing without copying a single photo pixel: it measures the sitter (MediaPipe face landmarks and hair/skin/clothes segmentation, optional), lays in faint Loomis construction and a straight-line envelope, plans values with the background held back, renders four tonal passes of tapered strokes that follow the form and stop at edges, blends the skin with a stump pass, adds lost-and-found edges and feature accents, lifts highlights and catchlights with an eraser pass, and deposits graphite through simulated paper tooth. Writes PNG, a layered editable SVG (one group per stage) and a receipt; review runs the rule-27 anatomy/contact gate plus value-fidelity checks. 16 portrait method cards (Loomis, Bridgman, Bargue, Speed, Vanderpoel, Hampton, Gurney, Dodson, Hammond, atelier sight-size) in data/portrait_methods.json name the stage that executes each. Non-portrait photos switch to scene mode (GrabCut subject + colour-cluster shape boundaries, short straight hatching). `imagine` draws scenes from imagination: Claude writes the scene as an SVG maquette (one light, gradients for the light and shadow families, far planes lighter) or passes any rendered PNG (unified_draw, drawing_methods, Blender or native 3D), and it is drawn like a photo. Media: graphite, charcoal, ink, sepia. | `python3 scripts/portrait_pipeline.py draw --photo photo.png --out out/portrait --models <dir with face_landmarker.task and selfie_multiclass.tflite>` | tested-here |
| `drawing-council` | PROTOCOL law 27 gate after drawing_methods.py review. Groups the 48 drawing-book method cards into eleven experts (construction, anatomy and proportion, gesture, logic and physics, perspective, light, colour, composition, line, character design, animals and nature), runs the automated gates (law-27 contact review, card checks, tone metrics), writes one prompt per expert with its card checks, common errors and veto conditions, records each expert's pass/fix/veto with correctness, craft and beauty scores, and computes a deterministic PASS/FAIL verdict with the fixes still required; it also exports the experts in the general council persona schema. | `python3 scripts/drawing_council.py roster --markdown` | tested-here |
| `perspective-color-lab` | Draws a geometrically constrained two-vanishing-point SVG and measures HSV/WCAG contrast of brand color swatches. | `python3 scripts/perspective_color_lab.py perspective --input scene.json --out out/scene.svg` | tested-elsewhere |
| `drawing-visual-qa` | Routes art tasks to four original-book sections read in full chapter context, measures real raster three-value tone groups, transparency and color proxies, and checks that edited pixels remain in the user-authorized rectangular region. Separate from the PR92 SVG authoring engine; its PASS is not an aesthetic verdict. | `python3 scripts/drawing_visual_qa.py curriculum "ارسم شخصية كرتونية بمنظور وإضاءة" --out out/lessons.json` | tested-here |

<!-- hub:area:draw:end -->

## الفهرس / contents

1. [KOSIF Code Drawing Master — مهارة رسم وتحريك فعلية](#kosif-code-drawing-master--مهارة-رسم-وتحريك-فعلية)
2. [Creative Paint runtime — verified callable drawing and short animations (2026-10-19)](#creative-paint-runtime--verified-callable-drawing-and-short-animations-2026-10-19)
3. [Verified character arm IK and word-triggered motion (2026-10-19)](#verified-character-arm-ik-and-word-triggered-motion-2026-10-19)
4. [Original full-body character animation (2026-10-19)](#original-full-body-character-animation-2026-10-19)
5. [Drawing-book methods atlas — كيف يفكر الرسام قبل أن يرسم](#drawing-book-methods-atlas--كيف-يفكر-الرسام-قبل-أن-يرسم)

## KOSIF Code Drawing Master — مهارة رسم وتحريك فعلية

لو المستخدم طلب **ارسم شخصية بالكود، قطة، رسم وجه وملابس، Whiteboard، تحريك مفاصل، تغيير تعابير، أو تحويل شكل SVG إلى آخر**، لا تكتفِ بروابط المشاريع؛ افتح [المهارة التنفيذية](../code-drawing-master.md) وشغّل منشئ الرسوم الموجود فعليًا داخل هذا المجلد. يوجد مولّد مشاهد أصلية يفهم ثلاث تعابير، ست حركات، شخصيات بشرية/قطط، شارع/حديقة، وتحريك كاميرا ورسم بالقلم. رمز الشخصية الأصلية يُولّد وفق أجزاء ومفاصل قابلة للتعديل، ولا يُنسخ من مستودع آخر.

    python3 $SKILL_DIR/scripts/code_drawing_master.py --cast human+cat --expression happy --location street --action walk --out ./scene.json --html ./scene.html

يمكن استيراد كلمات مرتبطة بوقت حقيقي من خرج WhisperX بعد إجراء التفريغ والمحاذاة بشكل منفصل:

    python3 $SKILL_DIR/scripts/code_drawing_master.py --cast human --action wave --words-json ./whisperx.json --out ./speech.json --html ./speech.html

توليد ملف HTML ≠ إنتاج فيديو MP4، ومزامنة الكلمات المستوردة ≠ تفريغ صوت آلي. لإخراج MP4 يستعمل محرك الرندر الموجود وتُقاس جودة الإطارات والصوت فعليًا. يدعم محرك SVG الأصلي أيضًا مورف مقيّد لضلوع متطابقة ومؤشر سن قلم مرسوم يتتبع المسار؛ لا تدّعِ وجود morph لأي مسارات عشوائية أو يد فوتوغرافية. مصدر التعلم والتحقق من التراخيص: Theatre.js، Flubber، WhisperX، PySceneDetect، AnimatedDrawings، SVG.js وغيرها موثقة بالدليل، وليست كلها مثبتة أو منسوخة. لا تزيد عداد قدرات KOSIF الرسمي بمجرد ظهور أسماء مستودعات.

## Creative Paint runtime — verified callable drawing and short animations (2026-10-19)

For user tasks asking Claude to **draw shapes, design an original character illustration, paint strokes, make layered PNG/SVG artwork or animate a keyframed drawing**, consult [Creative Paint runtime](../creative-paint-runtime.md). Run `python scripts/creative_paint.py doctor` from the skill directory, or invoke the script using its repository-root path. Start from `templates/creative-paint-demo.json`. Render via `render --scene ... --output ... --time ...`; animate via `animate --scene ... --output ... --fps ... --duration ...`. The engine is an independent Python/Pillow implementation with optional FFmpeg for MP4: **not** a reimplementation of Adobe Animate, Microsoft Paint or Photoshop. 13 dedicated real CLI/pixel/video tests and one verified 18-frame, H.264 MP4 demo have passed on Windows 11. SVG vector path width and raster pressure-brush rendering are not identical; Arabic shaping depends on FreeType/raqm availability. Verify inputs and outputs; do not claim generative-AI or advanced character IK capability on this basis. For more detailed character/body rigs use `code_drawing_master.py`; for audio-synced motion compositing use the existing film pipeline.

## Verified character arm IK and word-triggered motion (2026-10-19)

For a request to **move a drawn character's arm, solve elbow/hand joints, animate a gesture at a specified word from timestamped narration, or export an IK animation** consult [KOSIF Character IK](../character-ik-motion.md). Use `scripts/character_ik.py doctor`, inspect `templates/ik-wave-demo.json` and `templates/ik-wave-words.json`, then call `render --scene ... --words ... --output ...`. It uses analytic two-bone IK and the original `creative_paint.py` renderer, produces PNG/SVG/GIF/H.264 MP4, and optionally stream-copies original AAC narration after independently comparing all audio packet data hashes. It does **not** auto-transcribe or implement a full-body mocap/Adobe Animate engine. The word-cue file must come from real audio timestamps, not inferred timings. On the Windows laptop, 18 automated tests and a real 48-frame, 24fps MP4 proof passed. Do not overstate it as full-body rigging or AI image generation.

## Original full-body character animation (2026-10-19)

For a Claude task requiring a drawn person to walk, run, wave, smile, blink or nod using time cues or verified word timings, use [KOSIF Full Body Animator](../fullbody-character-motion.md). Run scripts/character_fullbody.py doctor, inspect templates/fullbody-demo.json, and supply templates/fullbody-demo-words.json only for the synthetic example. Produces layered SVG, PNG, GIF and MP4, optionally stream-copying AAC narration with packet hash verification. This is original 2D IK and drawing code, not 3D mocap or Adobe/CapCut clone; no automatic transcription or lip sync. Local Windows tests 14/14 successful.

## Drawing-book methods atlas — كيف يفكر الرسام قبل أن يرسم

قبل رسم أي شخصية أو وجه أو جسم، شغّل `python3 scripts/drawing_methods.py plan "<الطلب>"` لتحصل على مناهج كتب الرسم المناسبة (الإيماءة، النسب بوحدة الرأس، بناء الرأس بالكرة، المانيكان، لغة الأشكال، السيلويت، التعبير، الضوء والقيم، الظل الساقط، التهشير، رأس الأنمي وشعره وتلوينه، توقيت التحريك والمشي، المدن والنبات والمنتجات والمخلوقات) مرتبة من النية إلى التحقق. ثم ابدأ من هيكل صحيح بـ `draw head|figure|character|forms|bounce|shadow --out <file.svg>` وافحصه بـ `check --svg <file.svg>`. للصور المولّدة استعمل `prompt` (لا يستدعي أي نموذج). التفاصيل والجدول الكامل للكتب في [أطلس مناهج كتب الرسم](../drawing-methods-atlas.md).

Before drawing a character, face or figure, run `plan` for the matching drawing-book methods in order (gesture, head-unit proportion, ball-and-plane head, mannequin, shape language, silhouette, expression, light and value), start from a correct structure with `draw`, and verify it with `check`. The cards are original summaries, not copied book text; `check` measures geometry, not artistic quality.


## Realistic portrait from a photo — بورتريه واقعي من صورة

لرسم شخص حقيقي من صورته بالقلم الرصاص كأنه مرسوم باليد، دون تغيير التكوين: `python3 scripts/portrait_pipeline.py draw --photo <صورة> --out out/<مجلد> --models <مجلد النماذج>` ثم `review --dir out/<مجلد>` حتى PASS، ثم افتح الـPNG وانظر إليه وقارنه بأفضل جولة سابقة قبل التسليم. اللوحة تبدأ ورقًا فارغًا وكل علامة فيها خط مولَّد (لا بكسل من الصورة). البطاقات PM-01..PM-16 والخطوات في [رسم البورتريه](../portrait-drawing.md).

To draw a real person from a photo as a pencil portrait, run `portrait_pipeline.py draw`, then `review` until PASS, then open the PNG and compare it with the best earlier round before delivery. The canvas is paper plus generated strokes only; the method cards and the loop rules are in [Portrait drawing](../portrait-drawing.md).

