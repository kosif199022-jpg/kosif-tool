"""Proofs for original exercise algorithms inspired by analyzed public-domain art principles."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "scripts" / "creative_principles.py"
spec = importlib.util.spec_from_file_location("creative_principles", FILE)
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

class OriginalDrawingMethods(unittest.TestCase):
    def test_staged_svg_are_real_drawings(self):
        spec = {"width":400,"height":500,"shapes":[
            {"kind":"circle","x":200,"y":170,"r":40,"stage":"guide"},
            {"kind":"rect","x":145,"y":215,"w":110,"h":110,"stage":"mass"},
            {"kind":"circle","x":200,"y":170,"r":38,"stage":"outline"},
            {"kind":"line","x1":185,"y1":173,"x2":215,"y2":173,"stage":"detail"}]}
        frames=P.staged_svg(spec)
        self.assertEqual(len(frames),4)
        self.assertIn("data-layer=\"guide\"",frames[0])
        self.assertNotIn("data-layer=\"detail\"",frames[1])
        self.assertNotIn("data-layer=\"guide\"",frames[3])
        self.assertIn("data-layer=\"detail\"",frames[3])
        self.assertTrue(all(s.startswith("<svg") and "</svg>" in s for s in frames))

    def test_no_script_or_negative_coordinates_injected(self):
        for bad in [
            {"kind":"circle","x":"<script>","y":5,"r":3,"stage":"mass"},
            {"kind":"rect","x":490,"y":10,"w":50,"h":50,"stage":"mass"},
            {"kind":"line","x1":10000,"y1":5,"x2":20,"y2":10,"stage":"outline"},
        ]:
            with self.assertRaises(ValueError):
                P.staged_svg({"width":500,"height":500,"shapes":[bad]})

    def test_three_tone_mass_study(self):
        pgm, receipt=P.quantize_pgm("P2\n# example\n4 2\n255\n0 20 200 250\n10 80 120 255\n")
        self.assertTrue(pgm.startswith("P2\n"))
        self.assertEqual(receipt["counts"],{"0":4,"127":1,"255":3})
        self.assertEqual(receipt["dark_distribution_left"],4)
        self.assertEqual(receipt["dark_distribution_right"],0)
        self.assertEqual(receipt["dark_balance_index_0_to_1"],0)
        self.assertIn("0 0 255 255",pgm)

    def test_invalid_pgm_rejected(self):
        for bad in ["P3\n1 1\n255\n25", "P2\n2 2\n255\n0 30", "P2\n1 1\n255\n999"]:
            with self.assertRaises(ValueError):
                P.quantize_pgm(bad)

    def test_frame_to_frame_tone_difference_not_auto_quality(self):
        seq=[
          {"time_seconds":0,"tone_ratio":{"0":0.2,"127":0.3,"255":0.5}},
          {"time_seconds":0.5,"tone_ratio":{"0":0.7,"127":0.2,"255":0.1}},
          {"time_seconds":1.2,"tone_ratio":{"0":0.7,"127":0.2,"255":0.1}},
        ]
        result=P.visual_cuts(seq)
        self.assertEqual(len(result["cuts"]),2)
        self.assertTrue(result["cuts"][0]["flag_large_change"])
        self.assertFalse(result["cuts"][1]["flag_large_change"])
        self.assertIn("intentional",result["warning"])

    def test_time_and_ratio_validation(self):
        with self.assertRaises(ValueError):
            P.visual_cuts([{"time_seconds":1,"tone_ratio":{"0":0,"127":0,"255":1}},
                           {"time_seconds":1,"tone_ratio":{"0":0,"127":0,"255":1}}])
        with self.assertRaises(ValueError):
            P.visual_cuts([{"time_seconds":1,"tone_ratio":{"0":0,"127":0,"255":1}},
                           {"time_seconds":2,"tone_ratio":{"0":0,"127":0,"255":0.5}}])

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"drawing.svg"
            P.safe_write(p,"test")
            with self.assertRaises(ValueError):
                P.safe_write(p,"overwrite")

if __name__=="__main__":
    unittest.main()
