"""Known-answer proof for proofs/general-writing/arabic_probe.py (ARL family).

Runs the probe and checks each deterministic line against its known answer (normalisation, original
spelling, numbers glued to clitics, RAQM shaping, reshaper+bidi, mojibake repair, bundled fonts).
The optional checks (camel-tools, pyarabic, tesseract OCR) must report PASS or an honest SKIP with the
install hint, never FAIL; when their library is absent here the matching test is skipped, so the log
shows they were not exercised. Offline; the probe writes only to a temp dir.
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "general-writing" / "arabic_probe.py"
LINE = re.compile(r"^(PASS|SKIP|FAIL)\s+(.+?)\s{2,}(.*)$")


def run_probe():
    done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT)], capture_output=True, text=True,
                          encoding="utf-8", timeout=120, cwd=str(ROOT))
    rows = {}
    for ln in done.stdout.splitlines():
        m = LINE.match(ln)
        if m:
            rows[m.group(2).strip()] = (m.group(1), m.group(3))
    return done, rows


class ArabicProbe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.done, cls.rows = run_probe()

    def status(self, name):
        self.assertIn(name, self.rows, self.done.stdout + self.done.stderr)
        return self.rows[name]

    def test_ran_ten_checks_without_failure(self):
        self.assertEqual(len(self.rows), 10, self.done.stdout)
        self.assertEqual(self.done.returncode, 0, self.done.stdout + self.done.stderr)
        self.assertRegex(self.done.stdout, r"\n\d+ pass, \d+ skip, 0 fail")

    def test_normalisation(self):
        st, detail = self.status("normalize for matching")
        self.assertEqual(st, "PASS")
        self.assertIn('-> "ختاما الي مستشفي المدينه"', detail)

    def test_original_spelling(self):
        st, detail = self.status("report in original spelling")
        self.assertEqual(st, "PASS")
        self.assertIn("['وفي الختامِ', 'تُعزّز']", detail)

    def test_numbers_glued_to_clitics(self):
        st, detail = self.status("numbers glued to clitics")
        self.assertEqual(st, "PASS")
        self.assertTrue(detail.endswith("['100', '15%', '2024', '5']"), detail)

    def test_mojibake_repair(self):
        st, detail = self.status("mojibake repair")
        self.assertEqual(st, "PASS")
        self.assertIn("d3e1c7e3", detail)                   # 'سلام' in cp1256
        self.assertIn('-> "سلام عليكم"', detail)

    def test_bundled_fonts(self):
        st, detail = self.status("Arabic fonts")
        self.assertEqual(st, "PASS")
        self.assertIn("Amiri-Regular.ttf", detail)

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Pillow missing")
    def test_raqm_shaping(self):
        from PIL import features
        st, detail = self.status("Pillow RAQM shaping")
        if not features.check("raqm"):
            self.assertEqual(st, "FAIL")                     # the probe must not claim shaping without raqm
            return
        self.assertEqual(st, "PASS")
        self.assertRegex(detail, r'"سلام" width \d+px')

    @unittest.skipUnless(importlib.util.find_spec("arabic_reshaper") and importlib.util.find_spec("bidi"),
                         "arabic-reshaper / python-bidi missing")
    def test_reshaper_bidi(self):
        st, detail = self.status("arabic-reshaper + python-bidi")
        self.assertEqual(st, "PASS")
        self.assertIn("['0xfeb3', '0xfefc', '0xfee1', '0x20']", detail)   # seen, lam-alef ligature, meem
        self.assertIn('visual order "2024', detail)

    @unittest.skipUnless(importlib.util.find_spec("camel_tools"), "camel-tools not installed here: ARL-10/ARL-18 not exercised")
    def test_camel_tools(self):
        self.assertEqual(self.status("camel-tools utils (no models)")[0], "PASS")

    @unittest.skipUnless(importlib.util.find_spec("pyarabic"), "pyarabic not installed here: ARL-12 not exercised")
    def test_pyarabic(self):
        self.assertEqual(self.status("pyarabic (GPL)")[0], "PASS")

    @unittest.skipUnless(shutil.which("tesseract"), "tesseract not installed here: ARL-14 not exercised")
    def test_tesseract(self):
        self.assertIn(self.status("tesseract Arabic OCR")[0], ("PASS", "SKIP"))

    def test_missing_optionals_are_honest_skips(self):
        for name, mod in (("camel-tools utils (no models)", "camel_tools"), ("pyarabic (GPL)", "pyarabic")):
            if importlib.util.find_spec(mod) is None:
                st, detail = self.status(name)
                self.assertEqual(st, "SKIP")
                self.assertIn("pip install", detail)
        if not shutil.which("tesseract"):
            st, detail = self.status("tesseract Arabic OCR")
            self.assertEqual(st, "SKIP")
            self.assertIn("apt-get install", detail)


if __name__ == "__main__":
    unittest.main()
