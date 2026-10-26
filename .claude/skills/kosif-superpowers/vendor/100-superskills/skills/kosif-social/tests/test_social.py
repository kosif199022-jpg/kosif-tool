"""Offline tests for KOSIF Social: python tests/test_social.py"""
import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import social  # noqa: E402

EX = ROOT / "examples"


class CheckTests(unittest.TestCase):
    def test_example_pack_passes(self):
        rep = social.check(json.loads((EX / "pack.example.json").read_text(encoding="utf-8")))
        self.assertTrue(rep["ok"], rep)

    def test_hashtag_rules(self):
        self.assertEqual(social.check_tag("#عروض_الخريف"), [])
        self.assertEqual(len(social.check_tag("#عروض الخريف")), 1)          # one problem: the space
        self.assertTrue(social.check_tag("#عُروض"))                          # diacritics
        self.assertTrue(social.check_tag("#2026"))                           # digits only
        self.assertTrue(social.check_tag("عروض"))                            # no #
        self.assertEqual(social.tag_key("#أجمل_حلوي"), social.tag_key("#اجمل_حلوى"))

    def test_limits_and_hook(self):
        doc = {"posts": {"reels": {"caption": "ا" * 130 + "\nاحفظ", "hashtags": [f"#t{i}" for i in range(6)]},
                         "shorts": {"title": "", "description": "x"},
                         "x": {"caption": "😀" * 141}}}
        rep = social.check(doc)["platforms"]
        self.assertFalse(rep["reels"]["ok"])
        self.assertTrue(any("الخطّاف" in w for w in rep["reels"]["warnings"]))
        self.assertIn("العنوان فاضي", rep["shorts"]["errors"])
        self.assertEqual(rep["x"]["length"], 282)                            # emoji weigh 2 on X

    def test_x_url_weight(self):
        self.assertEqual(social.x_length("شوف https://example.com/a/very/long/path"), 4 + 23)

    def test_unknown_platform(self):
        self.assertFalse(social.check({"posts": {"myspace": {"caption": "x"}}})["ok"])

    def test_fit(self):
        self.assertEqual(social.fit("reels", {"w": 1080, "h": 1920, "seconds": 60}), [])
        self.assertEqual(len(social.fit("shorts", {"w": 1920, "h": 1080, "seconds": 200})), 2)
        self.assertTrue(social.fit("tiktok", {"w": 720, "h": 1280, "seconds": 20}))


class FileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="kosif_social_test_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_calendar(self):
        plan = json.loads((EX / "plan.json").read_text(encoding="utf-8"))
        rep = social.calendar(plan, self.tmp)
        self.assertEqual(rep["posts"], (4 + 3 + 2 + 1) * 4)
        rows = list(csv.reader(open(self.tmp / "calendar.csv", encoding="utf-8-sig")))[1:]
        self.assertFalse(any(r[1] == "الجمعة" for r in rows))              # days_off respected
        self.assertEqual(rep["pillars"], {"نصايح سريعة": 20, "وراء الكواليس": 13, "عروض المتجر": 7})
        ics = (self.tmp / "calendar.ics").read_text(encoding="utf-8")
        self.assertEqual(ics.count("BEGIN:VEVENT"), rep["posts"])
        self.assertEqual(social.calendar(plan, self.tmp / "again")["posts"], rep["posts"])   # deterministic

    def test_carousel(self):
        try:
            import PIL  # noqa: F401
        except ImportError:
            self.skipTest("Pillow missing")
        spec = json.loads((EX / "carousel.json").read_text(encoding="utf-8"))
        rep = social.carousel(spec, self.tmp, EX)
        self.assertEqual(len(rep["slides"]), len(spec["slides"]))
        self.assertTrue(Path(rep["pdf"]).stat().st_size > 0)
        from PIL import Image
        self.assertEqual(Image.open(rep["slides"][0]).size, (1080, 1350))
        too_many = {**spec, "slides": spec["slides"] * 4}
        self.assertTrue(social.carousel(too_many, self.tmp / "many", EX)["warnings"])

    def test_ab(self):
        self.assertTrue(6000 < social.sample_size(0.03, 0.3) < 7000)
        self.assertAlmostEqual(social._z(0.975), 1.959964, places=5)
        rep = social.abread(EX / "ab_results.example.csv", need=6000)
        self.assertLess(rep["p_value"], 0.01)
        self.assertTrue(rep["verdict"].startswith("B"))
        plan = social.abplan(json.loads((EX / "ab.json").read_text(encoding="utf-8")), self.tmp)
        self.assertTrue((self.tmp / "ab_results.csv").exists())
        self.assertGreater(plan["impressions_per_variant"], 0)

    def test_besttime(self):
        p = self.tmp / "export.csv"
        with open(p, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Post time", "Video views"])
            for d in range(1, 29):
                hour = 19 if d % 7 == 2 else 10
                views = 9000 if hour == 19 else 3000
                w.writerow([f"2026-07-{d:02d} {hour}:15", f"{views:,}"])
        rep = social.besttime(p)
        self.assertEqual(rep["top"][0]["hours"], "18:00–21:00")
        small = self.tmp / "small.csv"
        small.write_text("date,views\n2026-07-01 10:00,5\n", encoding="utf-8")
        self.assertEqual(social.besttime(small)["top"], [])

    def test_cli_limits(self):
        self.assertEqual(social.main(["limits", "--platform", "reels"]), 0)
        self.assertEqual(social.main(["limits", "--platform", "nope"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
