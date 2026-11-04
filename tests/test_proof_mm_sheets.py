"""Known-answer proof for mm_sheets.py (scripts/mimic): review contact sheets.

Builds synthetic keyframes and checks the exact sheet geometry, where each tile lands and that labels
(Latin and Arabic) put ink under the tiles. Offline: numpy + Pillow.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
SCRIPT = MIMIC / "mm_sheets.py"
os.environ.setdefault("MIMIC_QUIET", "1")
sys.path.insert(0, str(MIMIC))

try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import mm_sheets as S
    from mm_common import work_paths
except ImportError as exc:  # pragma: no cover
    raise unittest.SkipTest(f"mimic dependencies missing: {exc}")

BG = (18, 18, 22)


def tile(color, w=20, h=10):
    return Image.new("RGB", (w, h), color)


class Grid(unittest.TestCase):
    def test_script_present(self):
        self.assertTrue(SCRIPT.is_file())

    def test_grid_geometry_and_placement(self):
        tiles = [tile((255, 0, 0)), tile((0, 255, 0)), tile((0, 0, 255))]
        sheet = S.grid(tiles, ["a", "b", "c"], cols=2)
        # W = cols*(tw+pad)+pad, H = rows*(th+label_h+pad)+pad with pad 8, label_h 44
        self.assertEqual(sheet.size, (2 * (20 + 8) + 8, 2 * (10 + 44 + 8) + 8))
        a = np.asarray(sheet)
        self.assertEqual(tuple(a[8 + 5, 8 + 10]), (255, 0, 0))           # tile 0 at (8, 8)
        self.assertEqual(tuple(a[8 + 5, 36 + 10]), (0, 255, 0))          # tile 1 at (36, 8)
        self.assertEqual(tuple(a[70 + 5, 8 + 10]), (0, 0, 255))          # tile 2 on row 2 at (8, 70)
        self.assertEqual(tuple(a[0, 0]), BG)
        self.assertEqual(S.grid([], [], cols=3).size, (200, 80))

    def test_labels_draw_ink(self):
        sheet = S.grid([tile((90, 90, 90), 120, 20)], ["SHOT 1\nسطر عربي"], cols=1)
        a = np.asarray(sheet).astype(int)
        label = a[8 + 20 + 2:8 + 20 + 44, 8:8 + 120]
        self.assertGreater(int((label.max(-1) > 150).sum()), 30)         # both label lines left ink

    def test_font_resolves_a_bundled_face(self):
        f = S.font(16)
        self.assertIsInstance(f, ImageFont.FreeTypeFont)
        self.assertIs(S.font(16), f)                                      # cached

    def test_side_by_side(self):
        a = np.zeros((40, 80, 3), np.uint8)
        b = np.full((60, 60, 3), 200, np.uint8)
        im = S.side_by_side(a, b, w=100)
        self.assertEqual(im.size, (2 * 100 + 12, 100 + 30))               # b fitted to 100x100
        arr = np.asarray(im)
        self.assertEqual(tuple(arr[26 + 10, 4 + 10]), (0, 0, 0))
        self.assertEqual(tuple(arr[26 + 50, 108 + 50]), (200, 200, 200))


class SpecSheets(unittest.TestCase):
    def test_shots_and_transitions_sheets(self):
        with tempfile.TemporaryDirectory() as td:
            P = work_paths(td)
            P["sheets"].mkdir(parents=True)
            spec = {"shots": [], "transitions": []}
            for i, col in enumerate([(200, 30, 30), (30, 200, 30)]):
                rel = f"kf{i}.png"
                Image.new("RGB", (110, 196), col).save(P["root"] / rel)
                spec["shots"].append({"id": i + 1, "start_s": i * 2.0, "end_s": i * 2.0 + 2, "dur_s": 2.0,
                                      "motion": {"speed": 0.1}, "keyframes": [{"tag": "mid", "clean": rel}]})
            out = S.shots_sheet(spec, P)
            with Image.open(out) as f:
                im = np.asarray(f.convert("RGB"))
            th = 392                                                         # 110x196 fitted to width 220
            self.assertEqual(im.shape[:2], (th + 44 + 8 + 8, 2 * (220 + 8) + 8))
            self.assertEqual(tuple(im[8 + 100, 8 + 100]), (200, 30, 30))
            self.assertEqual(tuple(im[8 + 100, 236 + 100]), (30, 200, 30))
            empty = S.transitions_sheet(spec, P, {"small": [np.zeros((10, 10, 3), np.uint8)]})
            with Image.open(empty) as f:
                self.assertEqual(f.size, (400, 60))
            spec["transitions"] = [{"id": 1, "type": "fade", "frames": 4, "ts": 3, "te": 7, "ts_s": 0.1,
                                    "confidence": 0.9}]
            small = [np.full((20, 10, 3), k * 20, np.uint8) for k in range(10)]
            with Image.open(S.transitions_sheet(spec, P, {"small": small})) as strip:
                self.assertEqual(strip.size, (7 * (110 + 4) + 12, 1 * (220 + 30) + 10))


if __name__ == "__main__":
    unittest.main()
