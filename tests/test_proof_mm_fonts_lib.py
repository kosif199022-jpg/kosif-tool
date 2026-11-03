"""Known-answer proof for mm_fonts_lib.py (scripts/mimic): the Arabic font library.

Checks weight parsing, Arabic-coverage detection on bundled OFL faces (Amiri covers Arabic, Poppins
does not), folder scanning with and without a fonts.json, static instancing of a variable font with
fontTools (Cairo -> Cairo Bold, weight class 700, no fvar) and the de-duplicated library.
Offline: fontTools only. fetch() is not called (it needs the network).
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
SCRIPT = MIMIC / "mm_fonts_lib.py"
FONTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "_shared" / "fonts"
os.environ.setdefault("MIMIC_QUIET", "1")
os.environ["MIMIC_FONT_CACHE"] = os.path.join(tempfile.gettempdir(), f"no-mimic-font-cache-{os.getpid()}")
sys.path.insert(0, str(MIMIC))

try:
    from fontTools.ttLib import TTFont
    import mm_fonts_lib as FL
except ImportError as exc:  # pragma: no cover
    raise unittest.SkipTest(f"fontTools missing: {exc}")


class Names(unittest.TestCase):
    def test_script_present(self):
        self.assertTrue(SCRIPT.is_file())

    def test_weight_from_name(self):
        self.assertEqual(FL._weight_from_name("Lateef-ExtraBold.ttf"), 800)   # not 700: longest name wins
        self.assertEqual(FL._weight_from_name("Amiri-Bold.ttf"), 700)
        self.assertEqual(FL._weight_from_name("Cairo-SemiBold.ttf"), 600)
        self.assertEqual(FL._weight_from_name("Mada-ExtraLight.ttf"), 200)
        self.assertEqual(FL._weight_from_name("Zain-Black.ttf"), 900)
        self.assertEqual(FL._weight_from_name("Lalezar.ttf"), 400)

    def test_catalog_is_consistent(self):
        fams = [row[1] for row in FL.CATALOG]
        self.assertEqual(len(fams), len(set(fams)))
        for _, _, style, spec in FL.CATALOG:
            self.assertIn(style, FL.STYLE_AR)
            self.assertTrue(("static" in spec) ^ ("var" in spec))


class Coverage(unittest.TestCase):
    def test_covers_arabic(self):
        ok, fam, w = FL._covers_arabic(FONTS / "Amiri-Regular.ttf")
        self.assertEqual((ok, fam, w), (True, "Amiri", 400))
        ok, fam, w = FL._covers_arabic(FONTS / "Amiri-Bold.ttf")
        self.assertEqual((ok, w), (True, 700))
        self.assertFalse(FL._covers_arabic(FONTS / "Poppins-Regular.ttf")[0])
        self.assertFalse(FL._covers_arabic(FONTS / "OFL-Amiri.txt")[0])          # not a font: no crash

    def test_scan_dir_keeps_only_arabic_faces(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            for f in ("Amiri-Bold.ttf", "Poppins-Bold.ttf", "Tajawal-Bold.ttf"):
                shutil.copy(FONTS / f, d / f)
            got = FL.scan_dir(d, "user", style="user")
            self.assertEqual(sorted((e["file"], e["family"], e["weight"]) for e in got),
                             [("Amiri-Bold.ttf", "Amiri", 700), ("Tajawal-Bold.ttf", "Tajawal", 700)])
            self.assertTrue(all(e["source"] == "user" and e["style_ar"] == "user" for e in got))
            # a fonts.json entry is taken as written (style, family) and the file is not rescanned
            (d / "fonts.json").write_text(json.dumps([{"file": "Amiri-Bold.ttf", "family": "Amiri", "weight": 700,
                                                       "style": "naskh", "style_ar": "نسخ", "source": "core"}]),
                                          encoding="utf-8")
            got = {e["file"]: e for e in FL.scan_dir(d, "user")}
            self.assertEqual(got["Amiri-Bold.ttf"]["style"], "naskh")
            self.assertEqual(got["Amiri-Bold.ttf"]["path"], str(d / "Amiri-Bold.ttf"))
            self.assertIn("Tajawal-Bold.ttf", got)

    def test_library_without_system_fonts(self):
        lib = FL.library(include_system=False)
        keys = [(e["family"], e["weight"], Path(e["path"]).name) for e in lib]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertIn(("Amiri", 400, "Amiri-Regular.ttf"), keys)
        self.assertIn(("Amiri", 700, "Amiri-Bold.ttf"), keys)
        self.assertNotIn("Poppins", {k[0] for k in keys})
        self.assertGreaterEqual(len(lib), 6)


class Instancing(unittest.TestCase):
    def test_variable_font_to_static_bold(self):
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td) / "Cairo-Bold.ttf"
            self.assertTrue(FL.instance_variable(FONTS / "Cairo[slnt,wght].ttf", dst, "Cairo", {"wght": 700, "slnt": 0}))
            with TTFont(str(dst)) as f:
                self.assertNotIn("fvar", f)
                self.assertEqual(f["OS/2"].usWeightClass, 700)
                self.assertEqual(f["name"].getDebugName(1), "Cairo Bold")
                self.assertEqual(f["name"].getDebugName(6), "Cairo-Bold")
            ok, fam, w = FL._covers_arabic(dst)
            self.assertEqual((ok, fam, w), (True, "Cairo Bold", 700))
            # axis values outside the font's range are clamped (Cairo wght is 200..1000)
            dst2 = Path(td) / "Cairo-X.ttf"
            self.assertTrue(FL.instance_variable(FONTS / "Cairo[slnt,wght].ttf", dst2, "Cairo", {"wght": 5000}))
            with TTFont(str(dst2)) as f:
                self.assertEqual(f["OS/2"].usWeightClass, 1000)


if __name__ == "__main__":
    unittest.main()
