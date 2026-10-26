# KOSIF Studio: drawing pixel by pixel (skill 109 guide)

Everything below runs from this skill's `scripts/` folder: `cd scripts` first. The motion studio described below is skill 110 (`hyperframes-animation-studio`).

KOSIF Studio is a desktop drawing program. You give it a picture as **an image**, as **code from any AI**, as **a
description**, or as **a change to a picture it already drew**, and it draws that picture in front of you one pixel
at a time, in the order a painter would: brush strokes for the sky, shapes growing outward from their centre,
figures rising from their feet, sparks scattered last. An image ends **identical to the original, pixel for pixel**.

![](../assets/zoom_compare.png)

## The window

The toolbar has four groups, and the menu bar repeats them with shortcuts.

| Group | Buttons | What they do |
|---|---|---|
| **المصدر** (source) | scene list · **🖼 صورة** (Ctrl+O) · **📝 كود** (Ctrl+K) · mode | A hand-written scene, an image (default mode **"مطابق تماماً"**: painted from nothing, identical at the end; **"متجه قابل للتكبير"**: traced into vector shapes), or code pasted from any AI. Ctrl+V pastes a copied picture or code straight onto the window |
| **الرسم** (drawing) | **▶ ارسم** (F5) · **⏸** · speed | Redraw, pause, and the painting speed (بطيء / عادي / سريع / فوري) |
| **الذكاء الاصطناعي** (AI) | **🧩 عدّل الصورة** (Ctrl+E) · **🤖 صورة من وصف** (Ctrl+G) · **↩ تراجع** (Ctrl+Z) · **⚙** | Change the picture on the canvas by describing the change; get a picture from a description; go back one edit; see and set which AI the studio can reach |
| **التصدير** (export) | **💾 PNG** (Ctrl+S) · **⤢ دقة عالية** · **📤 كود الصورة** · **🎬 فيلم** | Save; export at 3840×2560; write a standalone Python program that makes the image again; record the drawing as an MP4 |

**❓** (F1) shows a quick guide. The status lines at the bottom say what is happening and, for images, the
exact-match check: **"✅ مطابقة للأصل تماماً (N بيكسل)"**.

## 🧩 Editing a picture

Press **🧩 عدّل الصورة** and type the change: "غيّر الذهبي إلى الأزرق", "make the grey shirt red", "اجعل الخلفية
أفتح". The studio always works on **what is on the canvas** — the opened image, the result of code, the previous
edit — at its own resolution. It describes the picture (every colour layer with its colour, share, bounding box
and centre), writes a small Pillow **edit program**, and fills in the edit in one of three ways:

1. **Colour changes are done at once, locally, without any AI.** "Change A to B" in Arabic or English (feminine
   forms, tanween and "ال" are understood) finds the layer nearest to colour A and recolours it to B, keeping
   folds, shadows and highlights.
2. **Anything else is asked of Claude**, when an AI is connected (see ⚙ below). The package sent is: instructions,
   the picture's description, your request and the program. The reply's code block is taken out of whatever text
   surrounds it.
3. **With no AI connected**, the same package is copied to the clipboard and the panel opens: paste it into Claude,
   ChatGPT or any AI, paste the reply back (📋 لصق), press ▶ ارسم الكود. A dialog shows these steps.

The result is drawn: the original first, then the edit over it. **↩ تراجع** returns to the picture before the
edit. The edit program's tools are `recolor` (keeps shading), `adjust` (brightness, contrast, saturation,
sharpness), `tint`, `paint`, `write`, `erase`, `flip`, and a `draw` for free drawing. The original image is **not**
inside the program (an AI could not read megabytes of base64); the program holds a key `<<KOSIF:ORIGINAL:…>>`
instead, and the original's bytes stay in `code/originals/`. The studio puts them back when it runs the program.
`python edit_pack.py photo.jpg "make the shirt red"` prints the package.

## 🤖 A picture from a description

Press **🤖 صورة من وصف** and describe the picture. With an AI connected, Claude writes the code (SVG, PIL or a
KOSIF scene, as the studio's own instructions ask) and the studio draws it. Without one, the instructions are
copied for you to paste into any AI, and its code goes into the panel. Code written from a description is a
drawing, not a photograph; for realism see the guide and `judge.py` below.

## ⚙ Which AI

`ai_bridge.py` tries, in order: **Claude Code's own CLI** (`claude -p`, when it is installed and logged in; no key
needed), then **the Anthropic API** (a key in ⚙ or `ANTHROPIC_API_KEY`), else **none** (local colour edits and the
copy-paste path). ⚙ shows the current state and how to connect: open a terminal, type `claude`, then `/login`
once. `settings.json` keeps the choice (`backend`: auto / cli / api / none), the key and the model.

## 📝 Code from any AI

Press **📝 كود**, paste, press **ارسم الكود** (or Ctrl+V on the window). The kinds of code it accepts:

- **SVG.** Every AI writes it well. It is drawn element by element and exports at any size without losing quality.
- **Python with PIL.** Every drawing command is recorded, so the picture is drawn **in the order the code draws
  it**. Consecutive commands of the same kind are grouped, so 360 sky lines become 18 brush strokes.
- **matplotlib / turtle.** The finished picture is drawn in brush strokes.
- **A KOSIF scene.** A `build()` function returns `Step`s, with lighting effects such as glow, rim light and soft
  gradients: the cinematic quality of the dragon scene.
- **An HTML / Three.js page.** Rendered in headless Edge, then painted (see below).

All Python code is drawn at the **picture's own size, without resampling**, and ends identical to what the code
itself produces; the studio checks this at the end. The panel's **🤖 انسخ تعليمات** copies the studio's own prompt
for any AI; the panel strips the ``` fences AIs wrap around code and takes the code block out of a longer reply.

### Safety

Pasted code runs **on your computer with your permissions**. It runs in a separate process with a 120-second
limit, and in a scratch folder so the files it writes don't land next to the program. Before running, the studio
scans the code. If it finds commands beyond drawing (deleting files, running programs, internet access, low-level
system access), it shows them and asks you. SVG is data, so it is never checked. Code that an AI returns through
🧩 or 🤖 goes through the same check.

## 📤 Image code: a Python program that makes the image again

Press **📤 كود الصورة** (or `python studio.py --image-code photo.jpg`) and you get a **standalone Python program**
(Pillow only). `python name.py` anywhere writes `name.png`, **identical to the original**, and the program checks
that itself. It has two parts: the picture's colour regions as `draw.polygon(...)` calls, largest first, readable
and editable; then the original's own bytes, from which every pixel the drawing did not get exactly right is
completed. Verified on a 900×900 ad (3,394 polygons, 0 differing pixels) and on a logo. Opened in the studio, the
program's own polygons are drawn in the code's order and then the details. `--data-only` gives the older
pure-data form (`TITLE` / `SIZE` / `IMAGE_B64`), which the studio reads as data (`ast.literal_eval`) without
running anything.

## Exact match with the original ("مطابق تماماً")

The image is painted from a blank, transparent sheet the way a painter works, in three stages:

1. **Blocking in.** The large shapes go down in a few flat colours: the logo's own colours, or a photo's main tones.
2. **Refining.** For photos, tones are added: shadows, then mid-tones, then lights.
3. **Final touches.** Every pixel that still differs gets its exact original value, including transparency, from
   most visible to least.

At the end the studio compares the result with the original pixel by pixel, shows **"✅ مطابقة للأصل تماماً"** with
the pixel count, and saves `out/<name>_exact.png`, identical to the original in every pixel.

**Jev chooses the painting plan for photos.** A photo has no colours of its own the way a logo does, so the studio
measures four plans on a reduced copy (block in with 6, 10, 16 or 24 colours, refine with 32 to 128 tones) in
about 3 s, then asks Jev which plan paints most like an artist with the least visible correction left — twice,
with the options reversed, averaged. Jev's choice and confidence appear in the window's top line; if Jev is
unreachable a rule decides, and the result is still identical.

Drawing happens at the image's own resolution and is shown fitted to the window. **⤢ دقة عالية** for a photo is a
faithful enlargement; for a logo it is the vector version (SVG + 3840×2560).

## Real 3D (HTML / Three.js) and film

Inspired by [HyperFrames](https://github.com/heygen-com/hyperframes): write HTML, render deterministic frames. Paste
a Three.js page into the code panel (or open `scenes/*.html`): `html_render.py` renders one frame in headless Edge
(WebGL through SwiftShader; waits for `window.__ready`), and the studio paints that frame pixel by pixel, checks it,
and can write its Python program. Physically based materials, shadows, fog, bloom and tone mapping come from the
browser's renderer, and HTML exports at any size. `scenes/whale_dragon_3d.html` is the showcase. Contract:
`window.__ready = true` when the frame is drawn; `window.render(t)` and `window.__duration` for animation.

**🎬 فيلم** (or `film.py drawing <scene | code file | image>`) records the current picture forming pixel by pixel as
an MP4 with FFmpeg; `film.py animate page.html` seeks `render(t)` frame by frame (a scene file can define
`build_t(t)` instead).

## 🎬 KOSIF Motion: professional animation (HyperFrames + GSAP)

`motion/` turns a request like "a 5-second animation about X" into a deterministic MP4. A film is **one HTML
composition** in [HyperFrames](https://github.com/heygen-com/hyperframes) format (`data-composition-id`,
`data-width/height/duration`, GSAP timelines registered on `window.__timelines`, seconds everywhere) written with
`motion/kit/motion-kit.js`: Arabic-safe word masks, pen-drawn paths with landing arrowheads, flowing dashes, seeded
rain / vapour / sparkle, one camera that moves the whole stage, flash, film grain and vignette, four easings
(slam / snap / drive / settle). The same file renders through HyperFrames' CLI (Puppeteer + FFmpeg, installed with
`npm install hyperframes gsap` in `motion/`) or through the studio's own renderer (`window.render(t)`).

```bash
python motion/motion.py new rocket --seconds 6 --title "الانطلاق"      # a project from the template
python motion/motion.py frames rocket --times 1,3,5                     # key frames: the 8-second gate
python motion/motion.py check rocket                                    # HyperFrames lint + runtime + contrast
python motion/motion.py render rocket --out out/rocket.mp4              # 1080p30, "looks" quality
python motion/motion.py measure out/rocket.mp4                          # motion energy report
python motion/ambience.py out.wav --seconds 6 --whoosh 0.5 --chords 0:A # a deterministic soundtrack
```

**Cinematic 3D** is the same pipeline with a Three.js scene: `motion/projects/water_cycle_3d/` (sky model with a
rising sun, a reflective sea, PBR terrain with shadows, raymarched volumetric clouds, vapour and rain particles,
a river that grows along its valley, lightning, bloom / depth of field / grain / grade), all driven by `t`,
bundled with `motion.py bundle` (esbuild) and rendered on the machine's GPU: headless Edge through ANGLE/D3D11
renders a heavy 1080p frame in ~0.15 s where SwiftShader needs 4 s, so a 17 s film takes minutes, not hours.
The studio engine muxes the composition's `<audio>` clips into the MP4 and normalises the mix to −14 LUFS / −1 dBTP;
`--blur 4` renders four sub-frames per frame on the GPU for a real shutter smear (≈ +30 % time here). The kit's v2
adds springs (`MOTION.spring`, `track`, `zoomTrack`), a beat clock (`beats`) and clip-path word masks; the craft rules
distilled from the HyperFrames, Motion Director and LottieFiles skills are in `motion/references/motion-craft.md`.

The 3D blocks live in **`motion/kit/three-kit.js`** (ES module, bundled by esbuild): seeded noise and generated
textures, `makeRenderer`, `makeSky` (sun by elevation/azimuth), `makeSunLight`/`makeFill`, `makeTerrain` (height function +
colour rule + tiled detail maps; `alpineColour` built in), `makeForest` (instanced two-tier conifers), `makeSea` (reflective
Water), `makeRibbon` (a river revealed along a curve), `makeCloudSlab` (raymarched), `makeVapour`/`makeRain`, `makeLensflare`,
`makePost` (bloom, god rays, DOF, grade/vignette/CA, grain, ACES, `sunOnScreen`), `cameraKeys`, and `makeFrameLoop` (the
render(t) with GPU sub-frame motion blur). `python motion/motion.py new NAME --3d` scaffolds a film on it; the water-cycle
scene is ~90 lines on top of the kit and renders pixel-identically to the hand-written version. v3 of the kit adds
`coniferCrown` (four jagged tiers + spire) and `makeFlock` (instanced flapping birds on a keyed path, placed near the
focus plane and against the sky); `ambience.py --birds t0:t1` synthesises dawn birdsong. The studio window has an
**أنيميشن** menu: new 2D/3D project, a key frame drawn in the studio, render with optional motion blur.

`motion/projects/water_cycle/` is the flat showcase: 17 s, five scenes (dawn, evaporation, condensation, precipitation,
collection, the loop), synthesised ambience, checked and rendered by HyperFrames. `motion/references/` holds the
authoring contract as the checker enforces it and a distilled 500-tool catalog.

## Realism: primitives, a guide and a measured gate

`render.py` has `shade` (form shading toward a light), `noise` (fractal texture: skin, rock, water, clouds),
`scales`, `relief` (height-field lighting with subsurface scattering, bumps, roughness and Fresnel), `water`, and
the camera stack `defocus`, `motion_blur`, `bloom`, `flare`, `chroma`, `filmic`. `references/drawing-guide.md` is
the agent's guide: which code to write for which input, the full scene language, the realism recipe, the review
loop and the edit loop. `judge.py` measures a render (flat fills, one-pixel edges, distinct colours, tonal range)
against thresholds calibrated on real photographs, shaded scenes and flat cartoons, then asks Jev which
description fits the numbers. `scenes/whale_dragon.py` was built with it.

## Running it

```bash
python studio.py                         # the studio with the dragon scene
```

```bash
python studio.py --image photo.jpg       # open the studio and redraw this image
```

```bash
python studio.py --code drawing.py       # draw a code file (SVG / PIL / matplotlib / turtle / scene / HTML)
```

```bash
python studio.py dragon_girl --render out/x.png --scale 3.2   # no window: 3840x2560
```

```bash
python ai_bridge.py                      # which AI the studio can reach right now
```

```bash
python -m unittest discover -s tests     # 42 tests
```

Requirements: Python 3.11+, Pillow, numpy, opencv-python, arabic-reshaper, python-bidi. matplotlib only for
matplotlib code; Playwright or Edge for HTML; FFmpeg for films; Claude Code or an API key for automatic AI.

## Files

| File | Role |
|---|---|
| `studio.py` | The window: menu, toolbar groups, drawing, the code panel, images, AI actions, saving and exporting |
| `ai_bridge.py` | The AI behind 🧩 and 🤖: Claude Code CLI, Anthropic API, or none; `settings.json` |
| `edit_pack.py` | The edit loop: picture description, keyed edit program with tools, package for any AI, local colour edits, key restore |
| `render.py` | The vector renderer: shapes (the full SVG path language, holes, strokes), gradients, light, text (shaped Arabic), relief, water, camera, finishing, and the painter's drawing order |
| `svg_import.py` | SVG → steps (shapes, transforms, CSS, gradients, text) |
| `runner.py` | Runs code from any AI in its own process and records PIL commands in order; HTML frames; image code |
| `exact.py` | Exact redraw: blocking in → refining → final touches, ending identical to the original; plans measured for Jev |
| `to_python.py` | Image → standalone Pillow program (polygons + embedded original), identical output |
| `html_render.py` | HTML/Three.js page → PNG in headless Edge (Playwright or Edge's own screenshot) |
| `film.py` | Drawing films (scenes, code, images) and animations to MP4 via FFmpeg |
| `motion/` | KOSIF Motion: `motion.py` (new / frames / check / render / measure), `kit/motion-kit.js`, `ambience.py`, templates, references, `projects/water_cycle` |
| `judge.py` | Realism gate: measured flat fills, hard edges, colours, tonal range; calibrated thresholds; Jev reads the numbers |
| `jev_client.py` | Jev, the fast judge: asked twice with the options reversed, averaged; a rule when unreachable |
| `vectorize.py` | Image → vector colour layers (+ SVG). Logos: true colours with exact edges. Photos: 24 colours |
| `vector_scene.py` | Builds the drawing steps from a traced image |
| `references/drawing-guide.md` | The agent's guide: prompt or image → code, scene language, realism recipe, review loop, edit loop |
| `scenes/` | `dragon_girl.py`, `duck_dragon.py`, `whale_dragon.py`, `whale_dragon_3d.html`; traced images and saved code land here too |
| `examples/` | AI-style examples: a PIL house, an SVG rocket, a matplotlib flower, and code with a deliberate error |

## Honest limits

- **Exact and enlargeable at once is impossible for an image.** The exact version is the original at its own
  resolution. The enlargeable version is vector with simplified colours. The studio gives you both.
- **Pictures from PIL, matplotlib and turtle are raster.** They match the code's own output exactly at its size,
  but cannot be enlarged without loss. SVG, KOSIF scenes and traced images enlarge without limit.
- **Local edits understand colours, not things.** "Make the grey red" works without an AI; "make the shirt red"
  needs one, because only an AI can tell from the description which grey is the shirt.
- **Tracing is only as detailed as its source.** A 155-pixel logo traces approximately; a high-resolution original
  traces perfectly. In vector mode, photos become a poster in 24 colours.
- **SVG features not drawn:** filters, masks, clip paths, patterns, embedded images.
- **Turtle is captured from its window** at the end, so the window appears briefly.

## Adding a scene by hand

```python
TITLE = "My scene"

def build():                     # everything in render.py is available without import
    return [
        Step("Sky", [fill(rect(0, 0, 1200, 800), lin((0, 0), (0, 800), [(0, "#0a0a2a"), (1, "#3a1a3a")]))], "sweep"),
        Step("Moon", [fill(ellipse(900, 200, 90), "#fff3d0"), glow(ellipse(900, 200, 90), "#8a7ad0", 40, .5)],
             "grow", origin=(900, 200)),
        Step("Title", [text("ليلة هادئة", 600, 700, 64, "#ffffff", anchor="mm", bold=True)], "sweep"),
    ]
```

The sheet is 1200×800. Drawing orders are `sweep`, `grow`, `rise`, `down`, `left`, `right` and `sparkle`.
