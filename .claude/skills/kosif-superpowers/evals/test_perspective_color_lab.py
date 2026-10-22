"""Real deterministic tests for 2-point projection & measurable palette contrast."""
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

SK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/"scripts"))
import perspective_color_lab as P


class AppliedBookPrinciples(unittest.TestCase):
    def scene(self):
        return dict(width=800,height=800,horizon_y=300,left_vp_x=30,right_vp_x=760,
                    front_bottom=[400,650],front_height=240,depth_left=.40,depth_right=.5)

    def test_projection_vertices_collinear_to_vanishing_points(self):
        svg,d=P.perspective(self.scene())
        self.assertIn('<svg',svg)
        ftop=d["vertices"]["front_top"]
        fbot=d["vertices"]["front_bottom"]
        for vp, side in (("left","left"),("right","right")):
            v=d["vanishing_points"][vp]
            for front, edge in ((ftop,d["vertices"][side+"_top"]),(fbot,d["vertices"][side+"_bottom"])):
                cross=(edge[0]-front[0])*(v[1]-front[1])-(edge[1]-front[1])*(v[0]-front[0])
                self.assertAlmostEqual(cross,0,places=7)

    def test_determinism(self):
        self.assertEqual(P.perspective(self.scene()),P.perspective(self.scene()))

    def test_no_impossible_geometry_or_injection(self):
        for bad in ({"left_vp_x":450}, {"front_height":800}, {"depth_left":-1}):
            scene=self.scene();scene.update(bad)
            with self.assertRaises(ValueError):
                P.perspective(scene)
        with self.assertRaises(ValueError):
            P.perspective({**self.scene(),"front_bottom":[0,"evil"]})

    def test_contrast_math_black_white(self):
        result=P.palette({"colors":["#000000","#FFFFFF"]})
        self.assertAlmostEqual(result["pairs"][0]["contrast"],21)
        self.assertTrue(result["pairs"][0]["wcag_normal_text_AA_4_5"])

    def test_gray_has_no_hue(self):
        result=P.palette({"colors":["#888888","#CCCCCC"]})
        self.assertIsNone(result["colors"][0]["hue_degrees_hsv"])
        self.assertFalse(result["pairs"][0]["wcag_normal_text_AA_4_5"])

    def test_reject_invalid_color_and_nan(self):
        for colors in (["#gggggg","#ffffff"],["#ffffff","#FFFFFF"],["red","#ffffff"],["#fff"]):
            with self.assertRaises(ValueError):
                P.palette({"colors":colors})
        with self.assertRaises(ValueError):
            P.real(float("nan"),"nan",0,1)

    def test_cli_artifact_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder)
            i=base/"input.json";out=base/"draw.svg"
            i.write_text(json.dumps(self.scene()),encoding="utf-8")
            self.assertEqual(P.main(["perspective","--input",str(i),"--out",str(out)]),0)
            self.assertTrue(out.exists())
            self.assertTrue(out.with_suffix(".json").exists())
            self.assertEqual(P.main(["perspective","--input",str(i),"--out",str(out)]),2)

    def test_pairwise_count(self):
        p=P.palette({"colors":["#000000","#f7f7f7","#123456"]})
        self.assertEqual(len(p["pairs"]),3)
        self.assertIn("NOT Munsell",p["calculation_method"])


if __name__=="__main__":
    unittest.main()
