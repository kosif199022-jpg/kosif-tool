"""Known-answer proof for mm_text.py (scripts/mimic): overlay-text analysis primitives.

Synthetic masks with known answers: line splitting (diacritic dots merge into their line), RTL word
columns, IoU and 2x downsampling, plateau segmentation into text events (including a word-by-word
growing reveal), curve resampling, sub-frame ramp extrapolation and the Otsu threshold.
Offline: numpy (+ OpenCV or SciPy through mm_img).
"""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
SCRIPT = MIMIC / "mm_text.py"
os.environ.setdefault("MIMIC_QUIET", "1")
sys.path.insert(0, str(MIMIC))

try:
    import numpy as np
    import mm_text as T
except ImportError as exc:  # pragma: no cover
    raise unittest.SkipTest(f"mimic dependencies missing: {exc}")


class Lines(unittest.TestCase):
    def test_script_present(self):
        self.assertTrue(SCRIPT.is_file())

    def test_split_lines_merges_dots(self):
        m = np.zeros((100, 60), bool)
        m[10:30, 5:55] = True      # line 1
        m[32:35, 20:24] = True     # a dot under line 1 (small segment, merged)
        m[60:80, 5:55] = True      # line 2
        self.assertEqual(T.split_lines(m), [(10, 35), (60, 80)])
        self.assertEqual(T.split_lines(np.zeros((10, 10), bool)), [])
        self.assertAlmostEqual(T._line_height(m), 22.5)

    def test_word_columns_right_to_left(self):
        C = np.zeros((40, 100), bool)
        C[10:30, 5:25] = True      # left word
        C[10:30, 60:90] = True     # right word (read first in Arabic)
        words = T.word_columns(C, 0, 100, 0, 40, 20)
        self.assertEqual(words, [{"x0": 60, "x1": 90, "y0": 10, "y1": 30}, {"x0": 5, "x1": 25, "y0": 10, "y1": 30}])

    def test_iou_and_half(self):
        a = np.zeros((4, 4), bool); a[:2] = True
        b = np.zeros((4, 4), bool); b[1:3] = True
        self.assertAlmostEqual(T._iou(a, b), 4 / 12)
        self.assertEqual(T._iou(np.zeros((2, 2), bool), np.zeros((2, 2), bool)), 0.0)
        m = np.zeros((5, 6), bool); m[3, 5] = True
        h = T._half(m)
        self.assertEqual(h.shape, (2, 3))
        self.assertTrue(h[1, 2])
        self.assertEqual(int(h.sum()), 1)
        self.assertEqual(T._odd(4), 5)
        self.assertEqual(T._odd(7.2), 7)


class Events(unittest.TestCase):
    def test_two_separate_events(self):
        N, Hh, Ww = 40, 60, 80
        M = np.zeros((N, Hh, Ww), bool)
        M[5:15, 10:20, 10:70] = True          # caption 1, frames 5..14
        M[22:32, 40:50, 10:70] = True         # caption 2 elsewhere, frames 22..31
        ev = T.segment_events(M, 10)
        self.assertEqual([(e["first"], e["last"]) for e in ev], [(5, 14), (22, 31)])
        self.assertEqual(ev[0]["core_frame"], 9)
        self.assertEqual(int(ev[0]["core_mask_half"].sum()), 600)

    def test_growing_reveal_is_one_event(self):
        M = np.zeros((30, 40, 80), bool)
        M[2:10, 10:30, 50:70] = True          # word 1
        M[10:20, 10:30, 50:70] = True
        M[10:20, 10:30, 20:40] = True         # word 2 joins: area doubles
        ev = T.segment_events(M, 25)
        self.assertEqual(len(ev), 1)
        e = ev[0]
        self.assertEqual((e["first"], e["last"], e["core_start"]), (2, 19, 10))
        self.assertEqual(e["steps"], [{"frame": 2, "area": 400}])


class Curves(unittest.TestCase):
    def test_resample(self):
        self.assertEqual(T._resample([]), [1.0] * T.CURVE_N)
        self.assertEqual(T._resample([0.3], 3), [0.3, 0.3, 0.3])
        self.assertEqual(T._resample([0, 1], 5), [0, 0.25, 0.5, 0.75, 1.0])

    def test_ramp_zero_extrapolates(self):
        frames = list(range(10, 20))
        vals = [min(1.0, max(0.0, (f - 11.5) / 5)) for f in frames]   # 0 at 11.5, full at 16.5
        self.assertAlmostEqual(T._ramp_zero(frames, vals, rising=True), 11.5, places=6)
        down = [min(1.0, max(0.0, (17.0 - f) / 4)) for f in frames]   # exit ends at 17
        self.assertAlmostEqual(T._ramp_zero(frames, down, rising=False), 17.0, places=6)
        self.assertIsNone(T._ramp_zero([1, 2], [0.5, 0.6], rising=True))

    def test_settled_and_visible(self):
        m = {"vis": 1.0, "dx": 0, "dy": 0, "scale": 1.0, "sharp": 0.9, "words": [], "match": 1.0}
        self.assertTrue(T._settled(m))
        self.assertFalse(T._settled(dict(m, dx=3)))
        self.assertTrue(T._visible(dict(m, vis=0.2)))
        self.assertFalse(T._visible(dict(m, vis=0.01)))
        self.assertFalse(T._visible(None))

    def test_otsu_splits_two_modes(self):
        rng = np.random.default_rng(0)
        v = np.concatenate([rng.normal(20, 3, 2000), rng.normal(200, 3, 2000)])
        thr = T._otsu(v)
        self.assertTrue(25 < thr < 195, thr)                    # inside the empty gap between the modes
        correct = (v[:2000] < thr).mean() + (v[2000:] >= thr).mean()
        self.assertGreater(correct / 2, 0.995)


if __name__ == "__main__":
    unittest.main()
