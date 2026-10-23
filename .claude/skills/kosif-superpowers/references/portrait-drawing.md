# رسم البورتريه الواقعي — Realistic portrait drawing

أداة `scripts/portrait_pipeline.py` تحوّل صورة شخص إلى بورتريه بالقلم الرصاص مبني خطًا بخط، بمناهج كتب البورتريه الكلاسيكية. البطاقات في `data/portrait_methods.json` (16 بطاقة، كل بطاقة تذكر المرحلة التي تنفذها في الكود).

`scripts/portrait_pipeline.py` turns a photo of a person into a pencil portrait built stroke by stroke, following the classical portrait methods. The cards live in `data/portrait_methods.json` (16 cards; each names the pipeline stage that executes it).

## الفهرس / contents

1. [What it is and what it is not](#what-it-is-and-what-it-is-not)
2. [Stages and the cards behind them](#stages-and-the-cards-behind-them)
3. [Running it](#running-it)
4. [The iteration loop (art-director rules)](#the-iteration-loop-art-director-rules)
5. [Sources](#sources)

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

## The iteration loop (art-director rules)

Several rounds are normal (PM-16). Three rules keep rounds from making the drawing worse:

1. **Compare with the best earlier round, and revert when worse.** Keep the best image; a round that loses something the best one had (for example, the building disappearing when the background was lightened too far) is reverted, not stacked on.
2. **Pin the style.** Graphite on warm paper, the same pass structure and the same seed across rounds, so differences come from the change being tested.
3. **Every finding names the code value to change.** For example: "swirls in the background" → `REGION_STYLE["background"]["straight"] = True`; "mottled skin" → finer `paper_tooth` octaves; "halo around the figure" → overshoot in `trace`.

`review` measures value fidelity, texture and connectivity; it does not judge beauty. Open the PNG and look at it before any claim.

## Sources

Method cards restate widely taught methods in original words; no book text or image is copied. Public-domain sources located: Harold Speed, *The Practice and Science of Drawing* (Project Gutenberg 14264); George B. Bridgman, *Constructive Anatomy* (archive.org); John H. Vanderpoel, *The Human Figure*; Charles Bargue and Jean-Léon Gérôme, *Drawing Course*. Also summarised: Andrew Loomis, *Drawing the Head and Hands* and *Fun with a Pencil*; Michael Hampton; Glenn Vilppu; James Gurney, *Color and Light*; Bert Dodson, *Keys to Drawing*; Juliette Aristides; William Maughan; Burne Hogarth; Lee Hammond; Harry Borgman; Richard Schmid; the sight-size atelier tradition. `review_status` on each source says how much was actually read.
