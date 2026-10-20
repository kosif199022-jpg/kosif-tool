# Unified Draw: animated strokes, shapes, and video

The original, source-level KOSIF integration now has **one CLI for drawing and 2D animation**. `scripts/unified_draw.py` compiles mixed strokes and geometric shapes into a layered `kosif.paint.v1` scene and calls the existing `creative_paint.animate` engine for rendered frames.

## Working commands

From `.claude/skills/kosif-superpowers/`:

```powershell
python scripts/unified_draw.py doctor
python scripts/unified_draw.py render --input templates/unified-draw-motion-demo.json --png ./frame.png --time 1
python scripts/unified_draw.py animate --input templates/unified-draw-motion-demo.json --output ./scene.gif --fps 12 --duration 2
python scripts/unified_draw.py animate --input templates/unified-draw-motion-demo.json --output ./scene.mp4 --fps 12 --duration 2
python scripts/test_unified_draw.py
python scripts/test_unified_draw_animation.py
```

Choose new filenames; existing outputs are never overwritten.

## Real integrated functionality

Input `schema=kosif.unified-draw.v1`: 128–2048 px canvas, ordered 1–100 `stroke` and `shape` elements. A stroke accepts Smart Draw's `points`, `assist`, `brush`, `width` and `color`. A shape accepts Creative Paint's `kind` and shape-specific geometry, including ellipse, rectangle, line, polygon and text. Each element can also specify `keyframes`, `opacity`, `blend`, `visible`, and `name`; the same layer stack works for PNG/SVG stills, GIF and MP4.

Example keyframes: `"keyframes":[{"time":0,"x":0,"y":0},{"time":2,"x":80,"y":30}]`.

Animation runs at 1–60 fps, up to 30 seconds, with a **hard maximum of 300 frames** in the underlying Creative Paint engine. MP4 uses FFmpeg; GIF uses Pillow. Seekable stills use `--time`. This animation is 2D layer transformation, not Blender/Cycles raytracing or AI-generated photorealistic footage.

## Verification evidence

2026-10-20 Windows laptop: previous still drawing integration **6/6**, new animation regression suite **7/7**, including actual 8-frame H.264 video inspected by FFprobe, animated GIF, keyframe pixel changes, still-frame seek, missing-FFmpeg fail-closed, no-overwrite and invalid frame limits. Additional preexisting engine tests are executed independently before publishing. See `proofs/unified-draw-motion-20261020.json` for the separately rendered acceptance clip's hashes and FFprobe details.

The existing Smart Draw and Creative Paint CLIs are preserved unchanged. This is a **verified fusion of two existing KOSIF engines** for this workflow; it does not make all 297 catalog abilities in the drawing group executable. No compiled binary reverse engineering was required or claimed for this Python-to-Python integration.
