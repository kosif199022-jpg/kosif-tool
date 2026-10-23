"""Independent art QA / preservation tests, using real generated PNG pixels."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw

SK=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("drawing_visual_qa",SK/"scripts"/"drawing_visual_qa.py")
lab=importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class QualityLabTests(unittest.TestCase):
    def test_four_verified_readings_not_full_library(self):
        c=lab.curriculum("ارسم شخصية بمنظور وألوان")
        self.assertEqual(c["books_reviewed_in_this_module"],4)
        self.assertIn("NOT_200_BOOKS",c["status"])
        for lesson in c["lessons"]:
            self.assertEqual(lesson["review_status"],"source_section_read")
            self.assertIn("gutenberg.org",lesson["source"])
            self.assertTrue(lesson["practice"])
            self.assertTrue(lesson["verify"])

    def test_perspective_route(self):
        c=lab.curriculum("اصنع منظور مبنى")
        self.assertEqual(c["lessons"][0]["author"],"G. A. Storey")

    def test_palette_route(self):
        c=lab.curriculum("راجع الألوان")
        self.assertEqual(c["lessons"][0]["author"],"Albert H. Munsell")
        self.assertIn("NOT Munsell",c["lessons"][0]["verify"])

    def test_reject_empty_goal(self):
        with self.assertRaises(ValueError):lab.curriculum("")

    def test_real_pixels_detect_three_tones(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"study.png"
            im=Image.new("RGBA",(120,90),(250,250,250,255))
            draw=ImageDraw.Draw(im)
            draw.rectangle((10,10,50,70),fill=(10,10,10,255))
            draw.rectangle((50,10,90,70),fill=(120,120,120,255))
            im.save(p)
            report=lab.diagnostic(p)
            tone=report["three_value_ratio"]
            self.assertGreater(tone["dark"],0)
            self.assertGreater(tone["middle"],0)
            self.assertGreater(tone["light"],0)
            self.assertAlmostEqual(sum(tone.values()),1,places=3)
            self.assertEqual(report["status"],"MEASURED_NOT_ART_JUDGMENT")
            self.assertEqual(len(report["file_sha256"]),64)

    def test_alpha_fraction(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"subject.png"
            im=Image.new("RGBA",(100,100),(0,0,0,0))
            ImageDraw.Draw(im).rectangle((25,25,74,74),fill=(24,24,24,255))
            im.save(p)
            report=lab.diagnostic(p)
            self.assertTrue(report["transparent_background_detected"])
            self.assertAlmostEqual(report["visible_fraction"],.25,places=2)

    def samples(self,d,region=(12,12,28,28)):
        a=Path(d)/"before.png";b=Path(d)/"after.png"
        Image.new("RGB",(96,80),"white").save(a)
        im=Image.new("RGB",(96,80),"white")
        ImageDraw.Draw(im).rectangle(region,fill="black")
        im.save(b)
        return a,b

    def test_compare_restricted_change_pass(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.samples(d)
            r=lab.compare(a,b,[10,10,20,20])
            self.assertEqual(r["status"],"SCOPE_PRESERVED")
            self.assertTrue(r["pass"])
            self.assertEqual(r["changed_outside_sample_fraction"],0)
            self.assertGreater(r["changed_inside_sample_fraction"],0)

    def test_compare_outside_change_detected(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.samples(d,(50,50,65,65))
            r=lab.compare(a,b,[10,10,20,20])
            self.assertEqual(r["status"],"OUT_OF_SCOPE_CHANGE")
            self.assertFalse(r["pass"])
            self.assertGreater(r["changed_outside_sample_fraction"],0)

    def test_bad_roi_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.samples(d)
            with self.assertRaises(ValueError):lab.compare(a,b,[-1,0,20,20])
            with self.assertRaises(ValueError):lab.compare(a,b,[1.2,0,10,10])
            with self.assertRaises(ValueError):lab.compare(a,b,[0,0,0,10])

    def test_dimension_change_detected(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.samples(d)
            Image.new("RGB",(48,40),"white").save(b)
            r=lab.compare(a,b,[1,1,10,10])
            self.assertFalse(r["pass"])
            self.assertEqual(r["status"],"SIZE_MISMATCH")

    def test_no_roi_not_automatic_pass(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.samples(d)
            r=lab.compare(a,b)
            self.assertFalse(r["pass"])
            self.assertEqual(r["status"],"CHANGE_MEASURED")

    def test_write_report_without_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"qa.json"
            lab.fresh(p,{"ok":True})
            with self.assertRaises(ValueError):lab.fresh(p,{"ok":False})
            self.assertEqual(json.loads(p.read_text())["ok"],True)

    def test_reject_nonimage_extension(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bad.html";p.write_text("<html>x</html>")
            with self.assertRaises(ValueError):lab.check_file(p)

    def test_same_image_zero_changes(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.samples(d)
            r=lab.compare(a,a,[0,0,12,12])
            self.assertEqual(r["changed_sample_fraction"],0)
            self.assertTrue(r["pass"])

if __name__=="__main__":
    unittest.main()
