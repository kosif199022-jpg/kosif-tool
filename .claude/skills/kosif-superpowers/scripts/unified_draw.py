#!/usr/bin/env python3
"""Unified KOSIF drawing entrypoint: assisted strokes + explicit shapes + exports.

Original code composition of smart_draw and creative_paint, not a commercial clone.
This does not imply that the entire drawing capability group is implemented.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from creative_paint import paint, svg, validate as validate_paint
from smart_draw import to_scene as smart_to_scene

SCHEMA = "kosif.unified-draw.v1"
MAX_ELEMENTS = 100


def compile_scene(data):
    """Convert an ordered mixture of strokes and geometric shapes to a paint scene."""
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValueError("expected kosif.unified-draw.v1")
    w, h = data.get("width"), data.get("height")
    if type(w) is not int or type(h) is not int or not (128 <= w <= 2048 and 128 <= h <= 2048):
        raise ValueError("width and height must be integers from 128 through 2048")
    elements = data.get("elements")
    if not isinstance(elements, list) or not (1 <= len(elements) <= MAX_ELEMENTS):
        raise ValueError("elements must contain 1..100 ordered drawing elements")
    scene = {"schema": "kosif.paint.v1", "width": w, "height": h,
             "background": data.get("background", "#F4F0E6"), "layers": []}
    details = []
    for i, element in enumerate(elements):
        if not isinstance(element, dict):
            raise ValueError(f"element {i+1}: expected object")
        typ = element.get("type")
        if typ == "stroke":
            stroke = {k:v for k,v in element.items() if k != "type"}
            native, labels = smart_to_scene({"schema": "kosif.smartdraw.v1",
                        "width":w, "height":h, "background":scene["background"], "strokes":[stroke]})
            layer = native["layers"][0]
            layer["name"] = f"{i+1}: {labels[0]['recognized']} ({labels[0]['brush']})"
            details.append({"element":i+1, "type":"stroke",
                            "recognized":labels[0]["recognized"]})
        elif typ == "shape":
            shape = {k:v for k,v in element.items() if k != "type"}
            kind = shape.get("kind")
            layer = {"name": f"{i+1}: {kind}", "visible": True,
                     "opacity": 1, "shapes": [shape]}
            details.append({"element":i+1, "type":"shape", "kind":kind})
        else:
            raise ValueError(f"element {i+1}: type must be stroke or shape")
        scene["layers"].append(layer)
    validate_paint(scene)
    return scene, details


def render(data, png=None, svg_file=None, scene_file=None):
    """Validate every output first; never overwrite existing files."""
    if not any((png, svg_file, scene_file)):
        raise ValueError("provide --png, --svg or --scene-out")
    paths = [Path(p) for p in (png, svg_file, scene_file) if p]
    if len({p.resolve() for p in paths}) != len(paths):
        raise ValueError("output paths must be different")
    for p in paths:
        if p.exists():
            raise ValueError(f"refusing to overwrite: {p}")
        if not p.parent.is_dir():
            raise ValueError(f"output folder does not exist: {p.parent}")
    for val, ext in ((png, ".png"), (svg_file, ".svg"), (scene_file, ".json")):
        if val and Path(val).suffix.lower() != ext:
            raise ValueError(f"expected {ext} output")
    scene, details = compile_scene(data)
    outputs = {}
    if png:
        paint(scene).save(png)
        outputs["png"] = str(Path(png))
    if svg_file:
        Path(svg_file).write_text(svg(scene), encoding="utf-8")
        outputs["svg"] = str(Path(svg_file))
    if scene_file:
        Path(scene_file).write_text(json.dumps(scene, ensure_ascii=False, indent=2)+"\n",
                                   encoding="utf-8")
        outputs["scene"] = str(Path(scene_file))
    return {"schema": SCHEMA, "elements": len(details), "recognized": details,
            "outputs": outputs, "engine": "smart_draw+creative_paint"}


def main():
    p = argparse.ArgumentParser(description="One KOSIF CLI for strokes and shapes")
    p.add_argument("action", choices=["doctor", "render"])
    p.add_argument("--input", help="ordered kosif.unified-draw.v1 document")
    p.add_argument("--png")
    p.add_argument("--svg")
    p.add_argument("--scene-out")
    a = p.parse_args()
    try:
        if a.action == "doctor":
            result = {"ready":True, "engines":["smart_draw", "creative_paint"],
                      "elements":["stroke", "shape"], "outputs":["png","svg","paint-scene-json"]}
        else:
            if not a.input: raise ValueError("--input is required for render")
            data=json.loads(Path(a.input).read_text(encoding="utf-8-sig"))
            result=render(data, a.png, a.svg, a.scene_out)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError) as err:
        print(json.dumps({"error":str(err)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
