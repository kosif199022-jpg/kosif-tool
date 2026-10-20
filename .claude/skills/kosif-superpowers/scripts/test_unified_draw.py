"""Regression tests for the unified KOSIF drawing entrypoint."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from unified_draw import compile_scene, render
from PIL import Image


def fixture():
    return {
        "schema": "kosif.unified-draw.v1", "width": 320, "height": 240,
        "background": "#F4F0E6",
        "elements": [
            {"type":"stroke", "assist":True, "color":"#226644", "width":4,
             "points":[[10,10],[100,10],[100,60],[10,60],[10,10]]},
            {"type":"shape", "kind":"ellipse", "x":145,"y":18,"width":50,"height":40,
             "fill":"#FFAABB", "stroke":"#000000", "stroke_width":3},
            {"type":"stroke", "assist":True,"points":[[20,100],[60,100],[105,100]]},
            {"type":"shape", "kind":"polygon","points":[[140,100],[190,100],[165,135]],
             "fill":"#11AACC","stroke":"#121212","stroke_width":2},
            {"type":"shape","kind":"text","x":25,"y":160,"text":"KOSIF","size":22,
             "fill":"#111111","stroke_width":0}
        ]}


class UnifiedDrawingTests(unittest.TestCase):
    def test_compiles_ordered_strokes_and_shapes(self):
        inp=fixture()
        before=copy.deepcopy(inp)
        scene, info=compile_scene(inp)
        self.assertEqual(inp,before)
        self.assertEqual(len(scene["layers"]),5)
        self.assertEqual([e["type"] for e in info],
                         ["stroke","shape","stroke","shape","shape"])
        self.assertEqual(info[0]["recognized"],"rectangle")
        self.assertEqual(info[2]["recognized"],"line")
        self.assertEqual(scene["layers"][1]["shapes"][0]["kind"],"ellipse")

    def test_exports_png_svg_and_native_scene(self):
        with tempfile.TemporaryDirectory() as d:
            png,svg,scene=[str(Path(d)/("drawing."+ext)) for ext in ("png","svg","json")]
            result=render(fixture(),png,svg,scene)
            self.assertEqual(len(result["recognized"]),5)
            with Image.open(png) as pic:
                self.assertEqual(pic.size,(320,240))
                self.assertNotEqual(pic.convert("RGBA").getpixel((165,40)),
                                    pic.convert("RGBA").getpixel((250,200)))
            self.assertIn("<svg",Path(svg).read_text(encoding="utf-8"))
            native=json.loads(Path(scene).read_text(encoding="utf-8"))
            self.assertEqual(native["schema"],"kosif.paint.v1")
            self.assertEqual(len(native["layers"]),5)

    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"drawing.svg"
            p.write_text("KEEP",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"overwrite"):
                render(fixture(),svg_file=str(p))
            self.assertEqual(p.read_text(encoding="utf-8"),"KEEP")

    def test_rejects_unsupported_shape_and_oversized_scene(self):
        data=fixture()
        data["elements"][1]["kind"]="unknown"
        with self.assertRaises(ValueError):
            compile_scene(data)
        data=fixture()
        data["width"]=5000
        with self.assertRaisesRegex(ValueError,"width"):
            compile_scene(data)

    def test_rejects_bad_points_and_invalid_schema(self):
        data=fixture()
        data["elements"][0]["points"]=[[1,2]]
        with self.assertRaises(ValueError):
            compile_scene(data)
        data=fixture()
        data["schema"]="random"
        with self.assertRaises(ValueError):
            compile_scene(data)

    def test_requires_output_and_distinct_paths(self):
        with self.assertRaisesRegex(ValueError,"provide"):
            render(fixture())
        with tempfile.TemporaryDirectory() as d:
            p=str(Path(d)/"drawing.svg")
            with self.assertRaisesRegex(ValueError,"different"):
                render(fixture(),svg_file=p,scene_file=p)


if __name__=="__main__":
    unittest.main(verbosity=2)
