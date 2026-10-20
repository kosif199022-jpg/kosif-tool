# Unified Draw — tested integration of Smart Draw and Creative Paint

This is **one executable front door** for the original KOSIF drawing engines:
- `scripts/smart_draw.py`: freehand strokes, optional deterministic snapping to line/rectangle/ellipse.
- `scripts/creative_paint.py`: layered vector/raster rendering of polygons, lines, shapes and text.
- `scripts/unified_draw.py`: compiles an ordered mixture of strokes and shape objects into one `kosif.paint.v1` scene, outputs `PNG`, `SVG` and/or editable scene `JSON`.

## Quick start

From `.claude/skills/kosif-superpowers/`:

```bash
python scripts/unified_draw.py doctor
python scripts/unified_draw.py render --input templates/unified-draw-demo.json --png ./drawing.png --svg ./drawing.svg --scene-out ./drawing.json
python scripts/test_unified_draw.py
```

Choose unused output paths: **existing files are never overwritten**. Exports are deterministic under fixed environment. Demo renders a stroked rectangle, ellipse, horizontal line, triangle and text in their specified layer order.

## Input contract

`schema=kosif.unified-draw.v1`, `width` and `height` between 128 and 2048 pixels, `background` (color or transparent), and 1–100 ordered `elements`. `{"type":"stroke","points":[...],"assist":true}` goes to the original Smart Draw shape assistant. `{"type":"shape","kind":"ellipse",...}`, similarly rectangle, line, polygon, brush or text, goes to Creative Paint. Both kinds render to a common layer stack.

## Evidence and boundaries

Local Windows + Python 3.13 / Pillow integration tests, 2026-10-20: **6 passed** (stroke-to-rectangle, stroke-to-line, ordered mixed scene, PNG/SVG/native scene export, image pixels, output overwrite refusal, invalid dimensions/schema/shapes/points/paths). This verifies the **specific integrated workflow**, *not* full coverage of the 297 catalog records in the drawing group. Legacy CLI interfaces remain unchanged, preserving compatibility.

No binary target was involved: Python source/test verification is appropriate here; REA and Ghidra are reserved for authorized compiled executables where reverse engineering adds information. No claims of ML object recognition, Photoshop compatibility, or full AutoDraw/Canva parity.
