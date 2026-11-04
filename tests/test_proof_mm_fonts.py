"""Known-answer proof for mm_fonts.py (scripts/mimic): font matching by ink.

A reference line is rendered in a known bundled OFL face; match() must rank that same face first among
every bundled face. Also checks the stroke-width and similarity primitives on synthetic masks.
Offline: numpy, Pillow (raqm), fontTools, OpenCV or SciPy.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
SCRIPT = MIMIC / "mm_fonts.py"
FONTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "_shared" / "fonts"
os.environ.setdefault("MIMIC_QUIET", "1")
# a cache folder that does not exist: only the bundled faces take part
os.environ["MIMIC_FONT_CACHE"] = os.path.join(tempfile.gettempdir(), f"no-mimic-font-cache-{os.getpid()}")
sys.path.insert(0, str(MIMIC))

try:
    import numpy as np
    from PIL import Image, features
    import mm_fonts as F
    import mm_render_text as RT
except ImportError as exc:  # pragma: no cover
    raise unittest.SkipTest(f"mimic dependencies missing: {exc}")

TEXT = "بسم الله الرحمن الرحيم"


class Primitives(unittest.TestCase):
    def test_script_present(self):
        self.assertTrue(SCRIPT.is_file())

    def test_tight_crop(self):
        m = np.zeros((20, 30), bool)
        m[5:9, 10:22] = True
        self.assertEqual(F._tight(m).shape, (4, 12))
        self.assertIsNone(F._tight(np.zeros((5, 5), bool)))

    def test_stroke_width_of_a_bar(self):
        m = np.zeros((60, 60), bool)
        m[10:50, 20:29] = True                         # a 9-px-wide vertical stroke
        self.assertGreater(F._stroke(m), 8.0)
        self.assertLess(F._stroke(m), 11.0)
        self.assertEqual(F._stroke(np.zeros((10, 10), bool)), 0.0)

    def test_signature_and_similarity(self):
        m = np.zeros((40, 100), bool)                  # a glyph-like comb, 80x20 px of ink box
        m[10:30, 10:16] = True
        m[10:30, 40:46] = True
        m[10:16, 10:90] = True
        m[24:30, 60:90] = True
        sig = F.signature(m)
        self.assertAlmostEqual(sig["aspect"], 80 / 20)
        self.assertEqual(sig["norm"].shape[0], F.NORM_H)
        score, parts = F.similarity(sig, sig)
        self.assertAlmostEqual(score, 1.0, places=6)
        self.assertEqual(parts["iou"], 1.0)


@unittest.skipUnless(features.check("raqm"), "Pillow without raqm cannot shape Arabic")
class MatchKnownFont(unittest.TestCase):
    def _work(self, td: Path, face: str) -> Path:
        work = td / face.split(".")[0]
        (work / "sheets").mkdir(parents=True)
        L = RT.render_line_pil(TEXT, str(FONTS / face), 64)
        Image.fromarray((255 - L.alpha * 255).astype(np.uint8)).save(work / "l0.png")   # dark ink on white
        Image.fromarray((L.alpha * 255).astype(np.uint8)).convert("RGB").save(work / "zone.png")
        spec = {"texts": [{"id": 1, "lines": [{"text": TEXT, "ink_h": L.ink_h}],
                           "crops": {"lines": ["l0.png"], "zone": "zone.png"}, "font": {}}]}
        (work / "spec.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        return work

    def test_reference_face_ranks_first(self):
        with tempfile.TemporaryDirectory() as td:
            for face, family in (("Lalezar-Regular.ttf", "Lalezar"), ("Tajawal-Bold.ttf", "Tajawal"),
                                 ("ArefRuqaa-Regular.ttf", "Aref Ruqaa")):
                work = self._work(Path(td), face)
                res = F.match(str(work), include_system=False)
                self.assertEqual(res["events"], 1)
                self.assertTrue(Path(res["sheets"][0]).is_file())
                font = json.loads((work / "spec.json").read_text(encoding="utf-8"))["texts"][0]["font"]
                best = font["candidates"][0]
                self.assertEqual(best["family"], family, font["candidates"][:3])
                self.assertEqual(font["confidence"], "high")
                self.assertGreater(best["score"], font["candidates"][2]["score"] * 3)
                if family != "Aref Ruqaa":                  # Regular and Bold of Aref Ruqaa are near twins
                    self.assertEqual(Path(font["chosen"]).name, face)


if __name__ == "__main__":
    unittest.main()
