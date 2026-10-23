# أدوات المجال `draw` (12 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `character-fullbody` — تحريك الشخصية بكامل الجسم / Full-body character animator

| الحقل | القيمة |
|---|---|
| المسار | `scripts/character_fullbody.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `characters-rigs`, `audio-sync-captions`, `engines-render-pipeline` |

**ما تفعله:** يرسم شخصية ثنائية الأبعاد كاملة الجسم مكوّنة من طبقات، تمشي وتركض وتلوّح وتبتسم وترمش وتومئ برأسها وفق أزمنة أو كلمات محددة، مستخدمًا الحركية العكسية ذات العظمتين للساقين والذراعين، ويصدّرها صورًا ثابتة PNG أو SVG أو GIF أو MP4 بترميز H.264 مع إمكانية إرفاق الصوت الأصلي بصيغة AAC والتحقق من حزمه.

**What it does:** Renders a layered 2D full-body character that walks, runs, waves, smiles, blinks and nods on time or word cues, using two-bone IK for legs and arms, and exports PNG/SVG stills or GIF/H.264 MP4 with optional packet-verified original AAC audio.

#### متى تُستدعى

- «خلّي الشخصية تمشي وتلوّح وتبتسم على كلمات التعليق»
- «عايز كاركتر يجري ويرمش في فيديو قصير»
- «أبي شخصية كاملة تهزّ راسها على كلمة معينة»
- «Animate a 2D character that walks, waves, smiles, blinks and nods»
- «Render a full-body character animation to MP4 with my original AAC voice-over»

#### الأوامر

- **doctor**: Prints JSON with the schema, ffmpeg availability (not ffprobe), export formats and the supported actions.
  - `python3 scripts/character_fullbody.py doctor`
- **render-still**: Draws the 5-layer character pose at t=1.55 s to a new PNG (use .svg for a vector still).
  - `python3 scripts/character_fullbody.py render --scene templates/fullbody-demo.json --words templates/fullbody-demo-words.json --time 1.55 --output ./still.png`
- **render-gif**: Renders every frame of the scene (24 frames for the 3 s demo) to a looping GIF.
  - `python3 scripts/character_fullbody.py render --scene templates/fullbody-demo.json --words templates/fullbody-demo-words.json --fps 8 --output ./walk.gif`
- **render-mp4-audio**: Encodes an H.264 MP4 and stream-copies the user's AAC audio, failing unless the packet hashes match. --audio is optional.
  - `python3 scripts/character_fullbody.py render --scene templates/fullbody-demo.json --words templates/fullbody-demo-words.json --fps 24 --audio ./voice.m4a --output ./fullbody.mp4`

#### المتطلبات والأمان

- optional: bin:ffmpeg, bin:ffprobe
- python: Pillow
- الأمان: runs-external-programs
- الموافقة: --audio muxes the user's narration into the output: use only audio the user supplied and has rights to.
- الحدود: One stylized 2D figure with six preset actions and simple leg/arm IK; no 3D, mocap, lip sync, transcription, multiple characters or custom artwork.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_character_fullbody.py`
- مرجع: `.claude/skills/kosif-superpowers/references/fullbody-character-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/draw.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:character-fullbody --evidence <ملف>`.

### `character-ik` — تحريك ذراع الشخصية بالحركية العكسية / Character IK arm animator

| الحقل | القيمة |
|---|---|
| المسار | `scripts/character_ik.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `characters-rigs`, `audio-sync-captions`, `engines-render-pipeline` |

**ما تفعله:** يحرّك ذراع شخصية مرسومة بسيطة بالحركية العكسية التحليلية ذات العظمتين نحو أهداف تحدّدها أزمنة أو توقيتات كلمات موثّقة، ويصدّر صورًا ثابتة PNG أو SVG أو GIF أو MP4 بترميز H.264، مع إمكانية نسخ التعليق الصوتي الأصلي بصيغة AAC دون إعادة ترميز والتحقق منه ببصمات الحزم.

**What it does:** Animates a simple drawn character's arm with analytic two-bone inverse kinematics toward targets cued by time or verified word timestamps, exporting PNG/SVG stills or GIF/H.264 MP4, optionally with the original AAC narration stream-copied and checked by packet hashes.

#### متى تُستدعى

- «حرّك ذراع الشخصية لما يقول كلمة ارفع»
- «عايز الشخصية ترفع إيدها على كلمة معينة في التعليق الصوتي»
- «أبي إشارة يد متزامنة مع الصوت وأحافظ على الصوت الأصلي»
- «Make the character raise its arm on a specific word from my narration»
- «Solve elbow and hand positions with inverse kinematics and export a GIF»

#### الأوامر

- **doctor**: Prints JSON with the schema, Pillow version, ffmpeg availability (not ffprobe), formats and the 600-frame limit.
  - `python3 scripts/character_ik.py doctor`
- **render-still**: Resolves the word-cued targets, solves the arm IK at t=0.8 s and paints a new PNG (use .svg for a vector still).
  - `python3 scripts/character_ik.py render --scene templates/ik-wave-demo.json --words templates/ik-wave-words.json --time 0.8 --output ./pose.png`
- **render-video**: Renders the full duration as frames and encodes an H.264 MP4 (or a GIF when the output ends in .gif), then checks the codec with ffprobe.
  - `python3 scripts/character_ik.py render --scene templates/ik-wave-demo.json --words templates/ik-wave-words.json --fps 24 --output ./wave.mp4`
- **render-with-audio**: Muxes the user's AAC narration by stream copy and fails unless every audio packet hash matches the source.
  - `python3 scripts/character_ik.py render --scene templates/ik-wave-demo.json --words templates/ik-wave-words.json --fps 24 --audio ./narration.m4a --output ./wave-voice.mp4`
- **library**: Uses solve_ik, words_from_file, resolve, probe and packet_hashes as a library; character_fullbody.py reuses them.
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); from character_ik import solve_ik; print(solve_ik((320,310),(400,190),120,115,-1))"`

#### المتطلبات والأمان

- optional: bin:ffmpeg, bin:ffprobe
- python: Pillow
- الأمان: runs-external-programs
- الموافقة: --audio muxes the user's narration into the output: use only audio the user supplied and has rights to.
- الحدود: Animates one two-bone arm on an otherwise static simple figure; it is not full-body rigging, lip sync, transcription or AI character generation.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_character_ik.py`
- `.claude/skills/kosif-superpowers/evals/test_character_fullbody.py`
- مرجع: `.claude/skills/kosif-superpowers/references/character-ik-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/draw.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:character-ik --evidence <ملف>`.

### `code-drawing-master` — رسم الشخصيات والمشاهد بالكود / Code Drawing Master storyboards

| الحقل | القيمة |
|---|---|
| المسار | `scripts/code_drawing_master.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `characters-rigs`, `shapes-morph-geometry`, `audio-sync-captions` |

**ما تفعله:** يولّد لوحة قصصية (storyboard) قابلة للتحرير بصيغة JSON لأداة Motion Director بمقاس 1080×1920، مع معاينة HTML مستقلة اختيارية يمكن التنقّل فيها زمنيًا، تُرسم فيها تدريجيًا شخصيات متجهية لإنسان أو قطة أو كليهما في شارع أو حديقة، بست حركات وثلاثة تعابير وتوقيتات كلمات حقيقية اختيارية.

**What it does:** Generates an editable 1080x1920 Motion Director storyboard JSON, plus an optional self-contained seekable HTML preview, in which procedural vector human and/or cat characters draw on in a street or park with six actions, three moods and optional real word timestamps.

#### متى تُستدعى

- «ارسم لي شخص وقطة يمشون في شارع كموشن جرافيك»
- «عايز رسمة كرتون لراجل بيلوّح في حديقة»
- «أبي ستوري بورد مرسوم بالكود لقطة تركض في الحديقة»
- «Draw a hand-drawn style character walking down a street as an editable animation»
- «Make a vertical draw-on storyboard of a person waving, synced to my word timestamps»

#### الأوامر

- **generate**: Writes a new storyboard JSON and a self-contained seekable HTML preview of a human and a cat walking on a street. The HTML is compiled, not rendered to video.
  - `python3 scripts/code_drawing_master.py --cast human+cat --expression happy --location street --action walk --out ./story.json --html ./story.html`
- **generate-with-words**: Embeds pre-aligned word timestamps (here the bundled synthetic demo words) as the scene's captions. Accepts words[{word\|text,start,end}] or WhisperX segments[].words and fails on missing, overlapping or out-of-range timings instead of synthesizing them.
  - `python3 scripts/code_drawing_master.py --cast human --action wave --duration 9 --words-json templates/ik-wave-words.json --out ./talk.json --html ./talk.html`
- **generate-json-only**: Writes only the editable storyboard JSON (a cat running in a park, 12 s at 30 fps).
  - `python3 scripts/code_drawing_master.py --cast cat --expression determined --location park --action run --duration 12 --fps 30 --out ./cat-park.json`
- **library**: Uses human_parts, cat_parts, scene_paths, load_words and make_story as a library (prints 20 14); motion_kit_bridge.py reuses human_parts this way.
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); import code_drawing_master as d; print(len(d.human_parts('happy')), len(d.cat_parts('sad')))"`
- **help**: Lists the allowed values for cast, expression, location, action and fps.
  - `python3 scripts/code_drawing_master.py --help`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: —
- الحدود: Produces a fixed, stylized procedural storyboard (two locations, preset human/cat rigs, six actions) and only compiles HTML; it does not render MP4, transcribe speech, lip-sync or accept custom artwork.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_code_drawing_master.py`
- مرجع: `.claude/skills/kosif-superpowers/references/code-drawing-master.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/draw.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-operating-manual.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:code-drawing-master --evidence <ملف>`.

### `creative-paint` — الرسم الإبداعي بالطبقات / Creative Paint layered renderer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/creative_paint.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `engines-render-pipeline`, `easing-timing-rhythm` |

**ما تفعله:** يرسم مشهدًا من طبقات معرّفًا بصيغة JSON صارمة (مستطيلات وأشكال بيضاوية وخطوط ومضلعات وضربات فرشاة حساسة للضغط ونصوص) باستخدام Pillow ويصدّره صورًا ثابتة PNG أو SVG، أو يحرّك الطبقات كاملةً بإطارات مفتاحية ويصدّرها GIF أو MP4 بترميز H.264.

**What it does:** Paints a strict JSON layered scene (rectangles, ellipses, lines, polygons, pressure brush strokes, text) with Pillow into PNG/SVG stills, or animates whole layers with keyframes into a GIF or H.264 MP4.

#### متى تُستدعى

- «ارسم لوحة بطبقات وصدّرها PNG وSVG»
- «عايز أحرّك دائرة بكي فريمز وأطلّعها GIF»
- «سوّ لي رسمة بسيطة بأشكال وفرشاة وطلّعها فيديو»
- «Paint a layered illustration from JSON and export PNG and SVG»
- «Animate a layer with keyframes and export an MP4»

#### الأوامر

- **doctor**: Prints JSON with the schema, Pillow version, ffmpeg availability, frame limit and supported formats.
  - `python3 scripts/creative_paint.py doctor`
- **render**: Validates the scene and paints one frame at the given time to a new PNG. Prints the path, sha256, byte count and verified flag.
  - `python3 scripts/creative_paint.py render --scene templates/creative-paint-demo.json --output ./paint.png --time 0.5`
- **render-svg**: Writes an editable SVG with one <g data-layer> group per layer.
  - `python3 scripts/creative_paint.py render --scene templates/creative-paint-demo.json --output ./paint.svg`
- **animate-gif**: Renders the layer keyframes to a looping GIF (at most 300 frames).
  - `python3 scripts/creative_paint.py animate --scene templates/creative-paint-demo.json --output ./paint.gif --fps 12 --duration 2`
- **animate-mp4**: Renders the frames and encodes an H.264 yuv420p MP4 (CRF 18) with the local ffmpeg.
  - `python3 scripts/creative_paint.py animate --scene templates/creative-paint-demo.json --output ./paint.mp4 --fps 24 --duration 2`
- **library**: Uses the module as a library (validate, paint, svg, render, animate, pose); character_ik, character_fullbody and smart_draw build on it this way.
  - `python3 -c "import sys,json; sys.path.insert(0,'scripts'); import creative_paint as cp; print(cp.validate(json.load(open('templates/creative-paint-demo.json'))))"`

#### المتطلبات والأمان

- optional: bin:ffmpeg
- python: Pillow
- الأمان: runs-external-programs
- الموافقة: —
- الحدود: A simple 2D primitive painter with whole-layer keyframes only (no AI generation, per-shape animation or PSD); SVG drops brush pressure and blend modes, and rotated layers do not land in the same place in PNG and SVG.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_creative_paint.py`
- `.claude/skills/kosif-superpowers/evals/test_smart_draw.py`
- `.claude/skills/kosif-superpowers/evals/test_character_fullbody.py`
- مرجع: `.claude/skills/kosif-superpowers/references/creative-paint-runtime.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/draw.md`
- مرجع: `docs/CREATIVE_PAINT_CAPABILITY_TRANSFER_20261019.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:creative-paint --evidence <ملف>`.

### `creative-principles` — دراسة الرسم التدريجي والظل الأصلي / Staged drawing and original three-value visual studies

| الحقل | القيمة |
|---|---|
| المسار | `scripts/creative_principles.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-elsewhere` |
| العائلات | `hand-drawn-draw-on`, `story-direction-ideas` |

**ما تفعله:** دراسة الرسم التدريجي والظل الأصلي؛ Builds original SVG drawing stages, three-value tone breakdown, and intercut tonal distribution flags from supplied arrays.

**What it does:** Builds original SVG drawing stages, three-value tone breakdown, and intercut tonal distribution flags from supplied arrays.

#### متى تُستدعى

- «رسم تدريجي من أشكال أصلية»
- «احسب توزيع الظل في الرسم»
- «Construct layered SVG doodles»
- «Review a cut's value distribution»

#### الأوامر

- **command 1**: Executes a local deterministic method only; no web or model spend.
  - `python3 scripts/creative_principles.py construct --input original-shapes.json --out-prefix out/stage`
- **command 2**: Run on user-supplied or local authorized input.
  - `python3 scripts/creative_principles.py values --input gray.pgm --out out/tonal.pgm`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes new output files in explicitly selected locations only; refuses overwrite; no network, paid tools or private downloads.
- الحدود: Construct/values/cut-tones are narrow deterministic exercises, not content understanding or an automatic professional drawing engine.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_creative_principles.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A14-drawing-cinematic-academy.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:creative-principles --evidence <ملف>`.

### `drawing-academy` — أكاديمية الرسم والدروس المبنية على مصادر / Source-aware drawing school and user-authorized book audits

| الحقل | القيمة |
|---|---|
| المسار | `scripts/drawing_academy.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-elsewhere` |
| العائلات | `hand-drawn-draw-on`, `story-direction-ideas` |

**ما تفعله:** أكاديمية الرسم والدروس المبنية على مصادر؛ Eight source-anchored skill lessons, rights-scoped text keyword scans, scores tied to actual artifacts and provenance.

**What it does:** Eight source-anchored skill lessons, rights-scoped text keyword scans, scores tied to actual artifacts and provenance.

#### متى تُستدعى

- «علم كلود الرسم من الكتب»
- «درس عن الظل والإضاءة»
- «Drawing book curriculum»
- «Audit my own art book text»

#### الأوامر

- **command 1**: Executes a local deterministic method only; no web or model spend.
  - `python3 scripts/drawing_academy.py index`
- **command 2**: Run on user-supplied or local authorized input.
  - `python3 scripts/drawing_academy.py lesson --id build_shapes --out out/lesson.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes new output files in explicitly selected locations only; refuses overwrite; no network, paid tools or private downloads.
- الحدود: Not 200 fully-read books, not model training and not evidence of visual mastery.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_drawing_academy.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A14-drawing-cinematic-academy.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:drawing-academy --evidence <ملف>`.

### `drawing-methods` — أطلس مناهج كتب الرسم مع رسم بنائي بالطبقات / Drawing-book methods atlas with layered construction SVGs

| الحقل | القيمة |
|---|---|
| المسار | `scripts/drawing_methods.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `story-direction-ideas` |

**ما تفعله:** 48 بطاقة منهج أصلية مستخلصة من كتب الرسم، ومنها 41 كتابًا من مكتبة المستخدم قُرئت في 2026-10-23 (نصًا أو OCR أو صفحات عينة) (الإيماءة، النسب، رأس لوميس، المانيكان، لغة الأشكال، السيلويت، التعبير، الضوء، الظل الساقط، التهشير، رأس الأنمي وشعره وتلوينه، توقيت التحريك، المشي، رسم المدن، النبات، المنتجات، المخلوقات، التمرين)؛ يرتبها لطلبك، ويبني خطة رسم أو برومبت صورة، ويرسم رأسًا أو جسمًا أو شخصية أو أشكالًا أو كرة تنط أو ظلًا ساقطًا مبنيًا SVG بطبقات، ثم يفحص هندستها مقابل البطاقات.

**What it does:** 48 original method cards distilled from drawing books, including 41 books from the user's own library read on 2026-10-23 (text, OCR or sample pages) (gesture, proportion, Loomis head, mannequin, shape language, silhouette, expression, light, cast shadows, hatching, anime heads, hair and cel shading, animation timing, walks, urban sketching, plants, products, creatures, practice); ranks them for an Arabic or English request, builds an ordered drawing plan or an image prompt, draws a head, figure, character, forms, a bouncing ball or a constructed cast shadow as a deterministic layered SVG (guide, construction, final, silhouette) and checks the drawing's geometry against the cards.

#### متى تُستدعى

- «ارسم شخصية كرتونية بلغة أشكال واضحة»
- «علمني أرسم الوجه من زاوية»
- «ارسم جسم بنسب صحيحة ووضعية ديناميكية»
- «Draw a character using drawing-book methods»
- «Plan a figure drawing with gesture and proportion»
- «اعمل انيميشن كرة بتنط بالانضغاط والتمدد»
- «ارسم ظل ساقط صح من مصباح»
- «Plan an anime head at a low angle with cel shading»

#### الأوامر

- **find**: Ranks the method cards for a request; prints JSON.
  - `python3 scripts/drawing_methods.py find "ارسم وش شخصية بتضحك"`
- **plan**: Ordered intent-to-verify drawing plan with the chosen cards' steps and checks, plus the demo and check commands.
  - `python3 scripts/drawing_methods.py plan "ارسم شخصية كرتونية طفل سعيد"`
- **prompt**: Image-generation prompt and review checks from the cards; calls no model.
  - `python3 scripts/drawing_methods.py prompt "a brave girl explorer" --methods DM-13,DM-16`
- **draw**: Writes a layered SVG (head, figure, character, forms, bounce or shadow); refuses to overwrite without --force.
  - `python3 scripts/drawing_methods.py draw character --shape circle --age child --expression happy --out out/character.svg`
- **draw-bounce**: Bouncing-ball key drawings on an arc with gravity spacing, stretch near contact and a constant-area squash.
  - `python3 scripts/drawing_methods.py draw bounce --frames 13 --out out/bounce.svg`
- **draw-shadow**: A box and a pole with cast shadows built by intersecting rays from a point light and its foot.
  - `python3 scripts/drawing_methods.py draw shadow --light-x 0.15 --light-height 0.4 --out out/shadow.svg`
- **check**: Measures the SVG's stages, proportions, tilts, shapes, expression, ball volume and spacing, and shadow-ray intersections against the cards; exits 1 on a failed check.
  - `python3 scripts/drawing_methods.py check --svg out/character.svg`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only the SVG or JSON path you pass; refuses to overwrite without --force; no network, model calls or spend.
- الحدود: Method cards paraphrase methods in original words. Cards marked user_copy_read_paraphrased rest on the user's own books read on 2026-10-23 through their text layer, OCR or sample pages (not a line-by-line study; some OCR was garbled); the others summarise widely taught methods. The SVGs are construction demonstrations, and check measures geometry only, not artistic quality.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_drawing_methods.py`
- مرجع: `.claude/skills/kosif-superpowers/references/drawing-methods-atlas.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:drawing-methods --evidence <ملف>`.

### `drawing-visual-qa` — مدرب الرسم من فصول الكتب والتشخيص البصري المستقل / Book-chapter drawing coach and independent raster visual QA

| الحقل | القيمة |
|---|---|
| المسار | `scripts/drawing_visual_qa.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `story-direction-ideas` |

**ما تفعله:** يبني تمارين من أربعة فصول موثّقة في كتب الرسم والتكوين والمنظور والألوان؛ ويفحص التدرج الداكن والمتوسط والفاتح والشفافية ودرجة اللون في الصور، ثم يقارن صور قبل/بعد ويكشف التعديل خارج النطاق المسموح. أداة تشخيص وليست شهادة احتراف.

**What it does:** Routes art tasks to four original-book sections read in full chapter context, measures real raster three-value tone groups, transparency and color proxies, and checks that edited pixels remain in the user-authorized rectangular region. Separate from the PR92 SVG authoring engine; its PASS is not an aesthetic verdict.

#### متى تُستدعى

- «علّمني الرسم من الكتب بتطبيق عملي»
- «حلّل توزيع الظل في رسمي»
- «قارن صورة قبل وبعد واحفظ بقية الصورة»
- «طوّر شخصية ورسومات من مناهج الفن»
- «Review drawing book exercises with measurable evidence»
- «Check unwanted edits outside a poster region»

#### الأوامر

- **curriculum**: Produces staged source-linked exercises from four chapter-read public-domain books. Reports that 200 other entries are not fully reviewed.
  - `python3 scripts/drawing_visual_qa.py curriculum "ارسم شخصية كرتونية بمنظور وإضاءة" --out out/lessons.json`
- **diagnose**: Reads authorized raster locally and measures three-value histogram, visible alpha fraction and dark-mass balance. No aesthetic confidence claim.
  - `python3 scripts/drawing_visual_qa.py diagnose out/character.png --out out/visual-qa.json`
- **compare**: Compares real image pixels and SHA-256s; fails if edits leak outside allowed rectangle beyond the tiny pixel tolerance.
  - `python3 scripts/drawing_visual_qa.py compare original.png edited.png --roi 120 230 360 180 --out out/scope-check.json`

#### المتطلبات والأمان

- python: Pillow
- الأمان: writes-files
- الموافقة: Only reads paths supplied by the user or explicit workspace; outputs a new JSON report and refuses overwrites. Never uploads photos.
- الحدود: The four named Gutenberg chapters were reviewed; the 200-index is not fully read. HSV is not Munsell HVC. Pixel changes do not establish beauty, facial identity, Arabic spelling or semantic faithfulness.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_drawing_visual_qa.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A14-drawing-cinematic-academy.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:drawing-visual-qa --evidence <ملف>`.

### `perspective-color-lab` — منظور هندسي ومقاييس التباين اللوني / Original two-point perspective and numeric palette analysis

| الحقل | القيمة |
|---|---|
| المسار | `scripts/perspective_color_lab.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-elsewhere` |
| العائلات | `hand-drawn-draw-on`, `story-direction-ideas` |

**ما تفعله:** منظور هندسي ومقاييس التباين اللوني؛ Draws a geometrically constrained two-vanishing-point SVG and measures HSV/WCAG contrast of brand color swatches.

**What it does:** Draws a geometrically constrained two-vanishing-point SVG and measures HSV/WCAG contrast of brand color swatches.

#### متى تُستدعى

- «ارسم المنظور بنقطتين تلاشي»
- «اختبر التباين اللوني»
- «Two point vanishing perspective»
- «Palette HSV color ratios»

#### الأوامر

- **command 1**: Executes a local deterministic method only; no web or model spend.
  - `python3 scripts/perspective_color_lab.py perspective --input scene.json --out out/scene.svg`
- **command 2**: Run on user-supplied or local authorized input.
  - `python3 scripts/perspective_color_lab.py palette --input colors.json --out out/palette.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes new output files in explicitly selected locations only; refuses overwrite; no network, paid tools or private downloads.
- الحدود: HSV is not native Munsell color; these are geometric/color metrics, not image beautification.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_perspective_color_lab.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A14-drawing-cinematic-academy.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:perspective-color-lab --evidence <ملف>`.

### `portrait-pipeline` — بورتريه واقعي من صورة مرسوم خطًا بخط بالجرافيت / Realistic portrait from a photo, drawn stroke by stroke in graphite

| الحقل | القيمة |
|---|---|
| المسار | `scripts/portrait_pipeline.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `story-direction-ideas` |

**ما تفعله:** يحوّل صورة مرجعية إلى بورتريه بالقلم الرصاص يبدو مرسومًا باليد دون نسخ أي بكسل من الصورة: يقيس الشخص (نقاط ملامح الوجه وتقسيم الشعر والجلد والملابس، اختياري)، ويضع بناء لوميس الخفيف وغلافًا بخطوط مستقيمة، ويخطط القيم مع تخفيف الخلفية، ويرسم أربع طبقات تهشير بخطوط مستدقة تتبع الشكل وتتوقف عند الحواف، ويموّه البشرة، ويضيف حوافًا ضائعة وظاهرة ولمسات الملامح، ويرفع الإضاءات ولمعة العين بالممحاة، ويرسب الجرافيت عبر ملمس ورق. يكتب PNG وSVG بطبقات قابلة للتحرير وإيصالًا، والمراجعة تشغّل بوابة القاعدة 27 وفحوص دقة القيم. 16 بطاقة منهج للبورتريه في data/portrait_methods.json.

**What it does:** Turns a photo reference into a hand-drawn-looking pencil portrait without copying a single photo pixel: it measures the sitter (MediaPipe face landmarks and hair/skin/clothes segmentation, optional), lays in faint Loomis construction and a straight-line envelope, plans values with the background held back, renders four tonal passes of tapered strokes that follow the form and stop at edges, blends the skin with a stump pass, adds lost-and-found edges and feature accents, lifts highlights and catchlights with an eraser pass, and deposits graphite through simulated paper tooth. Writes PNG, a layered editable SVG (one group per stage) and a receipt; review runs the rule-27 anatomy/contact gate plus value-fidelity checks. 16 portrait method cards (Loomis, Bridgman, Bargue, Speed, Vanderpoel, Hampton, Gurney, Dodson, Hammond, atelier sight-size) in data/portrait_methods.json name the stage that executes each.

#### متى تُستدعى

- «ارسم الصورة دي بورتريه بالقلم الرصاص كأنها مرسومة باليد»
- «حوّل صورتي لرسم واقعي بالرصاص من غير ما تغير التكوين»
- «Draw this photo as a realistic pencil portrait from scratch»
- «Make a graphite portrait drawing of this person»
- «ارسم بورتريه واقعي بالتهشير»

#### الأوامر

- **draw**: Measures the photo and writes portrait.png, portrait.svg (layers construction, lay-in, cross-hatch, deep-shadow, accents, edges + a hidden rule-27 figure group) and receipt.json.
  - `python3 scripts/portrait_pipeline.py draw --photo photo.png --out out/portrait --models <dir with face_landmarker.task and selfie_multiclass.tflite>`
- **review**: Rule-27 anatomy/contact gate (drawing_methods review) plus value-mass, value-detail, face-likeness, value-range and stroke-texture checks; writes review.json; exit 1 on any failure.
  - `python3 scripts/portrait_pipeline.py review --dir out/portrait`
- **cards**: Lists or shows the portrait method cards.
  - `python3 scripts/portrait_pipeline.py cards --id PM-02`

#### المتطلبات والأمان

- optional: mediapipe (+ face_landmarker.task, selfie_multiclass_256x256.tflite from storage.googleapis.com/mediapipe-models)
- python: numpy, opencv-python-headless
- الأمان: writes-files
- الموافقة: Writes only into --out; no network, model calls or spend. A photo of a real person is personal data: draw people only with their consent and never publish without the user's permission.
- الحدود: Algorithmic rendering from measured construction and a value map, not a human hand and not a neural model; likeness depends on the measurement step. Method cards paraphrase widely taught methods (only those marked user_copy_read_paraphrased rest on books read). review measures value fidelity, texture and figure connectivity, not beauty.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_portrait_pipeline.py`
- مرجع: `.claude/skills/kosif-superpowers/references/portrait-drawing.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:portrait-pipeline --evidence <ملف>`.

### `smart-draw` — الرسم الذكي ومساعد الأشكال / Smart Draw shape assist

| الحقل | القيمة |
|---|---|
| المسار | `scripts/smart_draw.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `shapes-morph-geometry` |

**ما تفعله:** يحوّل ضربات الرسم الحر المعرّفة بصيغة JSON إلى رسمة من طبقات، ويطابق كل ضربة اختياريًا مع مستطيل أو شكل بيضاوي أو خط مستقيم بهندسة حتمية، ثم يعرض الأشكال المتعرَّف عليها أو يصدّر الرسمة بصيغة PNG أو SVG.

**What it does:** Turns freehand stroke JSON into a layered drawing, optionally snapping each stroke to a rectangle, ellipse or straight line with deterministic geometry, then reports the recognized shapes or renders the drawing to PNG/SVG.

#### متى تُستدعى

- «حوّل خربشاتي إلى مستطيل ودائرة وخط مستقيم»
- «عايز أرسم بإيدي والأداة تظبّط الأشكال لوحدها»
- «أبي أعرف وش الشكل اللي رسمته: دائرة ولا مستطيل؟»
- «Snap my rough freehand strokes into clean shapes»
- «Turn sketch strokes into a layered SVG with pen, marker and highlighter»

#### الأوامر

- **doctor**: Prints JSON describing the engine, shape classes, brushes and output formats (is_ml:false).
  - `python3 scripts/smart_draw.py doctor`
- **analyze**: Read-only. Prints each stroke's recognized shape and brush plus the layer count.
  - `python3 scripts/smart_draw.py analyze --scene templates/smart-draw-demo.json`
- **render-svg**: Converts the strokes to Creative Paint layers (one per stroke) and writes a new SVG.
  - `python3 scripts/smart_draw.py render --scene templates/smart-draw-demo.json --output ./sketch.svg`
- **render-png**: Writes a new raster PNG with pressure-aware brush strokes and the brush opacities.
  - `python3 scripts/smart_draw.py render --scene templates/smart-draw-demo.json --output ./sketch.png`
- **library**: Uses classify, simplify and to_scene as a library; this example prints 'rectangle'.
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); import smart_draw as sd; print(sd.classify([[20,20],[130,20],[130,100],[20,100],[20,20]]))"`

#### المتطلبات والأمان

- python: Pillow
- الأمان: writes-files
- الموافقة: —
- الحدود: Heuristic geometric snapping into three shape classes plus freehand (rectangle, ellipse, line); no ML object recognition like AutoDraw, no eraser, collaboration or template library.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_smart_draw.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/draw.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/3d.md`
- مرجع: `.claude/skills/kosif-superpowers/references/blender-smartdraw-research-20261019.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:smart-draw --evidence <ملف>`.

### `unified-draw` — الرسم الموحد: خطوط وأشكال وطبقات وتصدير / Unified Draw: freehand + geometry + layered export

| الحقل | القيمة |
|---|---|
| المسار | `scripts/unified_draw.py` (جذر: skill) |
| المجال | `draw` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `shapes-morph-geometry` |

**ما تفعله:** ??? ?????? ???????? ??????? ?????? ??????? ??????? ?????? ?????? PNG ?SVG ?JSON ?GIF ?MP4.

**What it does:** Combines Smart Draw freehand stroke snapping, Creative Paint layered shapes and text, and keyframed GIF/MP4 animation behind one ordered scene and CLI.

#### متى تُستدعى

- «Draw lines and shapes in one file»
- «Combine freehand strokes, ellipses, rectangles, polygons or text and export»
- «ارسم خطوط وأشكال ودوائر ونصوص في لوحة واحدة»

#### الأوامر

- **doctor**: Show engines, supported element types and output formats.
  - `python3 scripts/unified_draw.py doctor`
- **render**: Compile ordered strokes and explicit geometric shapes into one layered paint scene and write requested new outputs.
  - `python3 scripts/unified_draw.py render --input templates/unified-draw-demo.json --png ./drawing.png --svg ./drawing.svg --scene-out ./drawing.json`
- **tests**: Run six integration and validation regression tests.
  - `python3 scripts/test_unified_draw.py`
- **animated-gif**: Render ordered strokes and shapes with per-element keyframes into a GIF using Creative Paint.
  - `python3 scripts/unified_draw.py animate --input templates/unified-draw-motion-demo.json --output ./drawing.gif --fps 12 --duration 2`
- **animated-mp4**: Render a mixed animated scene into an H.264 MP4 using Creative Paint + FFmpeg; max 300 frames.
  - `python3 scripts/unified_draw.py animate --input templates/unified-draw-motion-demo.json --output ./drawing.mp4 --fps 12 --duration 2`
- **still-at-time**: Render a still PNG from animated layers at a requested timestamp.
  - `python3 scripts/unified_draw.py render --input templates/unified-draw-motion-demo.json --png ./frame.png --time 1.5`

#### المتطلبات والأمان

- optional: ffmpeg (needed for MP4 only)
- python: Pillow
- الأمان: writes-files
- الموافقة: —
- الحدود: Tested Smart Draw + Creative Paint integration for layered stills and bounded keyframed animations; max 300 frames; no ML, full 3D or all 297 drawing catalog powers.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/scripts/test_unified_draw.py`
- `.claude/skills/kosif-superpowers/scripts/test_unified_draw_animation.py`
- مرجع: `.claude/skills/kosif-superpowers/references/unified-draw-integration.md`
- مرجع: `.claude/skills/kosif-superpowers/references/unified-draw-animation.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:unified-draw --evidence <ملف>`.

