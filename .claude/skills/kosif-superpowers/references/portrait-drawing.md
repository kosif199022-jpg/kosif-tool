# رسم البورتريه وأي صورة أو مشهد متخيَّل — Portrait, any photo and imagined scenes

أداة `scripts/portrait_pipeline.py` تحوّل صورة شخص إلى بورتريه بالقلم الرصاص مبني خطًا بخط، بمناهج كتب البورتريه الكلاسيكية. البطاقات في `data/portrait_methods.json` (24 بطاقة، كل بطاقة تذكر المرحلة التي تنفذها في الكود).

`scripts/portrait_pipeline.py` turns a photo of a person into a pencil portrait built stroke by stroke, following the classical portrait methods. The cards live in `data/portrait_methods.json` (24 cards; each names the pipeline stage that executes it).

## الفهرس / contents

1. [What it is and what it is not](#what-it-is-and-what-it-is-not)
2. [Stages and the cards behind them](#stages-and-the-cards-behind-them)
3. [Running it](#running-it)
4. [Any photo, imagined scenes and media](#any-photo-imagined-scenes-and-media)
5. [Colour: coloured pencil, oil brush, watercolour](#colour-coloured-pencil-oil-brush-watercolour)
6. [The iteration loop (art-director rules)](#the-iteration-loop-art-director-rules)
7. [Sources](#sources)

## What it is and what it is not

- **What it is:** algorithmic rendering from a measured construction and a value map. The canvas starts as blank paper; every mark is a generated, tapered pencil stroke deposited through simulated paper tooth. The receipt records `canvas_source: strokes_only` and `photo_pixels_in_output: false`.
- **What it is not:** a human hand, a filter over the photo, a neural style transfer or an image-generation model. The photo is measured (landmarks, regions, values) the way an atelier student measures a sitter, never pasted.
- **Composition:** unchanged. The crop only trims phone-screenshot bars; nothing is moved or removed. The background is held lighter and looser (focal hierarchy, PM-06), not deleted.
- **Consent:** a photo of a real person is personal data. Draw people with their consent and never publish without the user's permission.

## Stages and the cards behind them

| stage | what the code does | cards |
|---|---|---|
| measure | MediaPipe face landmarks (468) and hair / skin / clothes segmentation (optional; Haar face box fallback); thirds, eye spacing, head roll | PM-01, PM-02 |
| construct | faint Loomis guides (cranium ball, centre line, brow / eye / nose / chin lines) and a straight-line envelope as the first, lightest layer | PM-02, PM-03, PM-15 |
| value plan | value map from the photo's lightness; flesh keyed lighter; background weighted down and its lightest lights left as paper | PM-04, PM-05, PM-06 |
| render | four tonal passes (lay-in, cross-hatch, deep shadow, accents) of tapered strokes that follow the form's direction field; skin uses near-parallel layers; architecture uses straight level/plumb strokes; strokes stop at region and tone edges and overshoot a little | PM-07, PM-08 |
| blend | stump pass on skin, fine re-hatching, then a lighter second stump pass | PM-09 |
| edges | lost-and-found contour lines: weight from local contrast times region importance | PM-10 |
| accents | lash line, lower lid, line between the lips and nostrils on the measured landmarks | PM-11 |
| lift | kneaded-eraser pass where the paper is darker than the value map, one catchlight per eye | PM-12 |
| paper | warm paper with fine tooth; graphite catches peaks at light pressure | PM-14 |
| review | rule-27 anatomy gate (head, neck, torso and hand form one body; the saluting hand touches the head) plus value and texture checks | PM-13, PM-16 |

## Running it

```bash
pip install numpy opencv-python-headless mediapipe        # mediapipe optional
# optional models (from storage.googleapis.com/mediapipe-models):
#   face_landmarker/face_landmarker/float16/1/face_landmarker.task
#   image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite  -> save as selfie_multiclass.tflite
python3 scripts/portrait_pipeline.py draw --photo photo.png --out out/portrait --models models/ [--scale 1.5] [--blend 0.75]
python3 scripts/portrait_pipeline.py review --dir out/portrait
python3 scripts/portrait_pipeline.py cards [--id PM-02]
```

On Linux without a display, MediaPipe needs `libegl1` (`apt-get install libegl1`). A 1320×2345 reference takes about three minutes at scale 1.0 on one CPU core (≈ 320,000 strokes).

Outputs: `portrait.png`, `portrait.svg` (one `<g>` per stage, strokes binned by width and opacity, plus a hidden `data-figure` group for the rule-27 gate), `receipt.json`, `review.json`.

## Any photo, imagined scenes and media

- **Any photo.** When no person is found (`--subject auto`), the drawing switches to scene mode: GrabCut separates subject from surroundings, a colour clustering gives the big shapes that strokes may not cross, the value range is spread over the full pencil range with the lights keyed up, and hatching is done in short straight strokes at the form's angle (long flowing curves read as a filter, short straight strokes read as a hand). `--background straight` is for architecture; `flow` follows the form.
- **From imagination (PM-17, PM-18).** Draw what does not exist the way Gurney does: build a maquette first. Claude writes the scene as an SVG with one light direction, gradients for the light and shadow families (light side, core shadow, reflected light), cast shadows away from the light, and far planes lighter and lower in contrast than near ones. `imagine --svg scene.svg --out out/scene` renders it (rsvg-convert or headless Chromium), keeps `_reference.png` as the receipt and draws it from strokes. Any renderer can be the maquette: `imagine --png` takes output from `unified_draw.py`, `drawing_methods.py draw ...` (construction SVGs become pencil or ink sketches), Blender or the native 3D tools. A flat vector maquette gives an illustration-like drawing; richer gradients and a real 3D render give a more realistic one.
- **Media.** `--medium graphite` (default), `charcoal` (wider, darker, blended everywhere, heavier tooth), `ink` (fine black hatching, no blending, little tooth) and `sepia` (red-brown on cream).

```bash
python3 scripts/portrait_pipeline.py draw --photo landscape.jpg --out out/landscape --medium ink
python3 scripts/portrait_pipeline.py imagine --svg scene.svg --out out/scene --medium charcoal
python3 scripts/drawing_methods.py draw head --out out/head.svg && python3 scripts/portrait_pipeline.py imagine --svg out/head.svg --out out/head --medium ink
```

## Colour: coloured pencil, oil brush, watercolour

الألوان الخشبية والفرشاة (زيت) والألوان المائية تستعمل نفس القياس ونفس اتجاه الشكل، ويتغير نموذج الصبغة وترتيب العمل كما يُدرَّس كل وسيط (البطاقات PM-19..PM-24، الكود في `scripts/color_media.py`).

| medium | order of work | what makes it read as the medium | cards |
|---|---|---|---|
| `colored-pencil` | four hatched layers light to dark in four directions; burnish on skin after layer 2; dark edges and accents last; white-pencil catchlights | 30 named pencils; each stroke picks the pencil whose wax layer (part glaze, part cover) moves the paper's local colour closest to the reference in OKLab; darks built from colour, greys and black only for neutral areas; wax sits on the paper tooth | PM-19, PM-20 |
| `oil` | toned umber ground, then brushes from max(h,w)/48 down to /380 (and /640 on the face only), each layer only where the canvas still differs from the reference seen at that brush size | Hertzmann curved strokes: one colour per stroke, follows the form, stops when the reference matches the canvas better than the brush; bristle streaks, dry-brush gaps at the end, impasto relief lit from the upper left, canvas weave in thin paint | PM-21, PM-22 |
| `watercolor` | light pencil underdrawing, a wet-in-wet wash that never goes darker than the local light, flat washes over whole shapes, smaller dark shapes, a last accent glaze; background fades out to the paper edge | transparent glazes multiply; each wash is flat over its shape; pigment collects at shape edges; granulation in the tooth; wobbly hand-laid edges; whites are paper | PM-23, PM-24 |

```bash
python3 scripts/portrait_pipeline.py draw --photo photo.png --out out/pencil --medium colored-pencil --models models/
python3 scripts/portrait_pipeline.py draw --photo photo.png --out out/oil --medium oil --models models/
python3 scripts/portrait_pipeline.py imagine --svg scene.svg --out out/scene --medium watercolor
python3 scripts/color_media.py palette          # the 30 pencils
```

`review` adds a `colour-fidelity` check for colour media (squinted OKLab distance to the reference). Honest limits: the oil brush takes each stroke's colour from a blurred reference (the colour a painter would mix), and each watercolour wash is the mean colour its shape needs, so both follow the photo's colours closely; impasto, canvas weave, edge darkening and granulation are simulated. The coloured-pencil SVG keeps every stroke grouped by pencil; oil and watercolour ship as PNG with a small SVG that carries the figure group for the rule-27 gate.

## The iteration loop (art-director rules)

Several rounds are normal (PM-16). Three rules keep rounds from making the drawing worse:

1. **Compare with the best earlier round, and revert when worse.** Keep the best image; a round that loses something the best one had (for example, the building disappearing when the background was lightened too far) is reverted, not stacked on.
2. **Pin the style.** Graphite on warm paper, the same pass structure and the same seed across rounds, so differences come from the change being tested.
3. **Every finding names the code value to change.** For example: "swirls in the background" → `REGION_STYLE["background"]["straight"] = True`; "mottled skin" → finer `paper_tooth` octaves; "halo around the figure" → overshoot in `trace`.

`review` measures value fidelity, texture and connectivity; it does not judge beauty. Open the PNG and look at it before any claim.

## Sources

Method cards restate widely taught methods in original words; no book text or image is copied. Public-domain sources located: Harold Speed, *The Practice and Science of Drawing* (Project Gutenberg 14264); George B. Bridgman, *Constructive Anatomy* (archive.org); John H. Vanderpoel, *The Human Figure*; Charles Bargue and Jean-Léon Gérôme, *Drawing Course*. Also summarised: Andrew Loomis, *Drawing the Head and Hands* and *Fun with a Pencil*; Michael Hampton; Glenn Vilppu; James Gurney, *Color and Light*; Bert Dodson, *Keys to Drawing*; Juliette Aristides; William Maughan; Burne Hogarth; Lee Hammond; Harry Borgman; Richard Schmid; the sight-size atelier tradition. Colour media: Alyona Nickelsen, *Colored Pencil Painting Bible*; Arthur L. Guptill, *Watercolor Painting Step-by-Step*; Aaron Hertzmann, *Painterly Rendering with Curved Brush Strokes of Multiple Sizes* (SIGGRAPH 1998, the brush algorithm reimplemented); Curtis et al., *Computer-Generated Watercolor* (SIGGRAPH 1997, effects approximated); Björn Ottosson's OKLab colour space. `review_status` on each source says how much was actually read.
