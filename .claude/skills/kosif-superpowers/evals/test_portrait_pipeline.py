import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "portrait_pipeline.py"
CARDS = ROOT / "data" / "portrait_methods.json"

try:
    import cv2
    import numpy as np
except ImportError:  # optional heavy deps
    cv2 = None


class PortraitCardsTest(unittest.TestCase):
    def test_cards_resolve_and_name_a_stage(self):
        data = json.loads(CARDS.read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], "kosif.portrait.methods.v1")
        src = {s["id"] for s in data["sources"]}
        ids = [m["id"] for m in data["methods"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 16)
        for m in data["methods"]:
            self.assertTrue(set(m["sources"]) <= src, m["id"])
            for k in ("principle_en", "principle_ar", "pipeline_stage", "executed_by", "checks"):
                self.assertTrue(m[k], f"{m['id']} {k}")

    def test_help_and_cards_without_heavy_deps(self):
        out = subprocess.run([sys.executable, str(SCRIPT), "cards"], capture_output=True, text=True, check=True)
        self.assertIn("PM-02", out.stdout)


@unittest.skipIf(cv2 is None, "numpy + opencv not installed")
class PortraitDrawTest(unittest.TestCase):
    def test_draw_is_strokes_only_and_follows_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            h, w = 220, 180
            yy, xx = np.mgrid[0:h, 0:w]
            img = np.full((h, w, 3), 200, np.uint8)
            img[..., :] = (60 + 150 * xx / w)[..., None].astype(np.uint8)   # left dark -> right light
            cv2.circle(img, (90, 110), 40, (30, 30, 30), -1)
            cv2.imwrite(str(tmp / "ref.png"), img)
            subprocess.run([sys.executable, str(SCRIPT), "draw", "--photo", str(tmp / "ref.png"),
                            "--out", str(tmp / "o"), "--seed", "3"], check=True, capture_output=True)
            rec = json.loads((tmp / "o" / "receipt.json").read_text())
            self.assertEqual(rec["canvas_source"], "strokes_only")
            self.assertFalse(rec["photo_pixels_in_output"])
            self.assertGreater(rec["strokes"], 200)
            ET.parse(tmp / "o" / "portrait.svg")
            out = cv2.imread(str(tmp / "o" / "portrait.png"), cv2.IMREAD_GRAYSCALE).astype(float)
            self.assertLess(out[100:120, 80:100].mean(), out[20:40, 150:170].mean() - 40)  # dark disc vs light side
            # the drawing is not the photo: pixel values differ and paper texture is present
            ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)
            self.assertGreater(abs(out - ref).mean(), 8)
            rv = subprocess.run([sys.executable, str(SCRIPT), "review", "--dir", str(tmp / "o")],
                                capture_output=True, text=True)
            self.assertTrue((tmp / "o" / "review.json").exists(), rv.stderr)
            checks = {c["id"]: c for c in json.loads((tmp / "o" / "review.json").read_text())["checks"]}
            self.assertTrue(checks["value-masses"]["pass"], checks["value-masses"])


if __name__ == "__main__":
    unittest.main()
