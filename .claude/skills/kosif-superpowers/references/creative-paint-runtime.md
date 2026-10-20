# KOSIF Creative Paint — callable original drawing and animation runtime

## Status: executable + independently tested on Windows 11 (2026-10-19)

This module is an **independent Pillow + FFmpeg implementation**, not a copy of Microsoft Paint, Adobe Animate, Lightroom, Canva or any proprietary editor. REA/Ghidra analysis identified design requirements, not transferable source code.

Command-line entrypoint: `scripts/creative_paint.py`.

### Preconditions

- Python 3.9+ and Pillow (the laptop's runtime used Python 3.13 + Pillow 12.3.0)
- FFmpeg for MP4 only. PNG, SVG and GIF run without it.
- `doctor` checks Pillow, FFmpeg and supported output formats.
- Source scene must be a validated declarative JSON object with `schema: "kosif.paint.v1"` (UTF-8, with or without a BOM).

### Callable commands for Claude Code

From repository root:

```powershell
$P = ".claude/skills/kosif-superpowers/scripts/creative_paint.py"
$S = ".claude/skills/kosif-superpowers/templates/creative-paint-demo.json"
python $P doctor
python $P render --scene $S --output "sample.png" --time 0
python $P render --scene $S --output "sample.svg" --time 0.5
python $P animate --scene $S --output "motion.gif" --fps 10 --duration 1.5
python $P animate --scene $S --output "motion.mp4" --fps 24 --duration 2
```

**No output is overwritten.** Use a fresh path for each run.

### Verified scope

- Raster PNG images; scalable **editable SVG** layers.
- Layer ordering, visibility, opacity, normal/multiply/screen compositing (raster), transparent backgrounds.
- Rectangles, ellipses, polygons, lines, pressure-varying brush strokes and text.
- Per-layer x/y movement, scale, rotation and opacity on timestamped linear/ease-in-out keyframes. Scale works from the canvas origin; a positive `angle` turns the layer clockwise about the centre of its scaled canvas box, and PNG/GIF/MP4 and SVG place rotated layers in the same spot (within about a pixel).
- Animated GIF and H.264 MP4 frame sequence export.
- Per-output SHA-256, simple validation; input is declarative JSON only (no code execution).
- Boundaries: 2048×2048 dimensions, 150 layers, 1500 shapes, 300 animation frames.

### Important limitations

This tool is a **usable first-stage drawing engine**. It is not equivalent to the feature set of Adobe Animate, Microsoft Paint or Lightroom. It does **not** supply AI text-to-image, photorealistic character generation, motion capture, advanced body-part IK, PSD interchange, native SVG animation timelines, real-time Wacom pressure ingestion, optical flow, rotoscoping, commercial stock libraries, audio-synced lip movements, or full video editing UI. For detailed character body parts, use the separate `scripts/code_drawing_master.py` which builds a procedural actor and animation storyboard. Audio/video composition is handled by the existing KOSIF motion/render modules.

SVG strokes use constant width for brushes, whereas PNG/GIF/MP4 paint strokes reflect per-point pressure. SVG also does not preserve raster blend-mode semantics in every browser.

Arabic and complex-script font shaping depends on the active Pillow/FreeType libraqm configuration; verify it before claiming correct Arabic typography.

### Verification

```powershell
python -m unittest discover -s .claude/skills/kosif-superpowers/evals -p test_creative_paint.py -v
```

16 tests cover scene and keyframe validation, unsafe shape rejection, image pixel positions, brush strokes, time interpolation, in-place rotation that matches between PNG and SVG, SVG escaping, PNG/SVG/GIF/MP4 export, no-overwrite behavior and the actual CLI invocation (including a scene saved with a UTF-8 BOM).

### Suggested use by Claude

1. Load this file and `templates/creative-paint-demo.json`.
2. Generate a JSON scene from the requested shapes, colors and layers; never construct executable code from user text.
3. Run the requested command, inspect the output file, correct visual issues and verify using the tests and output digest.
4. If a user wants real character animation or an edited video, route to `code_drawing_master.py` and the existing render pipeline. Never advertise this as AI image generation.
5. For large graphics, render a small preview before expensive MP4 output.

### Provenance

Original implementation written 2026-10-19. Static audits of private proprietary program files are held outside this public repository. No commercial application binaries or decompiled code are included.
