"""Tests for independent per-pixel depth buffering (no Blender)."""
from pathlib import Path
import copy
import sys
import tempfile
import unittest
from PIL import Image, ImageChops

SK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/"scripts"))
import native_3d as n


def example():
    return {"schema":"kosif.native3d.v1", "width":160,"height":160,
            "fps":10,"frames":20,"background":"#142231",
            "render_mode":"zbuffer",
            "camera":{"position":[0,-6,2],"target":[0,0,0],
                      "ortho_scale":4.5},
            "objects":[
                {"shape":"cube","color":"#E04646","scale":[2,2,2],
                 "location":[0,0,0]},
                {"shape":"cube","color":"#46B079","scale":[2,2,2],
                 "location":[0,3,0]},
            ]}


class ZBufferProof(unittest.TestCase):
    def test_depth_output_renders_color_and_shapes(self):
        img=n.render(example(),1)
        self.assertEqual(img.size,(160,160))
        self.assertGreater(len(img.getcolors(160*160)),3)

    def test_object_order_independence_for_overlapping_depth(self):
        scene=example()
        a=n.render(scene,1)
        rev=copy.deepcopy(scene)
        rev["objects"].reverse()
        b=n.render(rev,1)
        self.assertIsNone(ImageChops.difference(a,b).getbbox())

    def test_invalid_mode_is_rejected(self):
        scene=example()
        scene["render_mode"]="eval(code)"
        with self.assertRaisesRegex(ValueError,"render mode"):
            n.validate(scene)

    def test_png_is_real_not_mock(self):
        scene=example()
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"proof.png"
            out=n.export(scene,path)
            self.assertFalse(out["uses_blender"])
            self.assertGreater(path.stat().st_size,400)
            with Image.open(path) as img:
                self.assertEqual(img.size,(160,160))

    def test_existing_painter_mode_still_available(self):
        scene=example()
        scene["render_mode"]="painter"
        self.assertIsInstance(n.render(scene,1),Image.Image)


if __name__=="__main__":
    unittest.main()
