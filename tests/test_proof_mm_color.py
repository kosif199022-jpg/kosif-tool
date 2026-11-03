"""Known-answer proof for mm_color.py (scripts/mimic): sRGB<->Lab, stats, Reinhard LUT, .cube, palette, names.

Offline, numpy only. The expected Lab values are the published CIE values for D65 sRGB primaries.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
SCRIPT = MIMIC / "mm_color.py"
os.environ.setdefault("MIMIC_QUIET", "1")
sys.path.insert(0, str(MIMIC))

try:
    import numpy as np
    import mm_color as C
except ImportError as exc:  # pragma: no cover - numpy is a hard dependency here
    raise unittest.SkipTest(f"numpy missing: {exc}")


class LabConversion(unittest.TestCase):
    def test_script_present(self):
        self.assertTrue(SCRIPT.is_file())

    def test_known_lab_values(self):
        white = C.rgb_to_lab(np.array([1.0, 1.0, 1.0]))
        black = C.rgb_to_lab(np.array([0.0, 0.0, 0.0]))
        red = C.rgb_to_lab(np.array([1.0, 0.0, 0.0]))
        np.testing.assert_allclose(white, [100.0, 0.0, 0.0], atol=0.05)
        np.testing.assert_allclose(black, [0.0, 0.0, 0.0], atol=0.05)
        # CIE Lab of sRGB red (D65): L 53.24, a 80.09, b 67.20
        np.testing.assert_allclose(red, [53.24, 80.09, 67.20], atol=0.05)

    def test_round_trip(self):
        rgb = np.random.default_rng(1).random((500, 3)).astype(np.float32)
        back = C.lab_to_rgb(C.rgb_to_lab(rgb))
        self.assertLess(float(np.abs(back - rgb).max()), 2e-3)

    def test_delta_e(self):
        self.assertAlmostEqual(C.delta_e((10, 20, 30), (10, 20, 30)), 0.0, places=6)
        self.assertAlmostEqual(C.delta_e((0, 0, 0), (255, 255, 255)), 100.0, delta=0.05)


class HexAndNames(unittest.TestCase):
    def test_hex_round_trip_and_clamp(self):
        self.assertEqual(C.hex_of((255, 128, 0)), "#FF8000")
        self.assertEqual(C.rgb_of("#FF8000"), (255, 128, 0))
        self.assertEqual(C.rgb_of("0a0B0c"), (10, 11, 12))
        self.assertEqual(C.hex_of((300, -5, 127.6)), "#FF0080")

    def test_named_colours_name_themselves(self):
        for name, rgb in C._NAMES.items():
            self.assertEqual(C.color_name(rgb), name)
        self.assertEqual(C.color_name((250, 250, 250)), "white")
        self.assertEqual(C.color_name((5, 5, 5)), "black")


class Statistics(unittest.TestCase):
    def test_lab_stats_flat_grey(self):
        img = np.full((40, 40, 3), 128, np.uint8)
        st = C.lab_stats(img)
        expect = C.rgb_to_lab(np.array([128 / 255] * 3, np.float32))
        np.testing.assert_allclose(st["mean"], expect, atol=0.01)
        np.testing.assert_allclose(st["std"], [1e-3] * 3, atol=1e-3)

    def test_merge_stats_pools_variance(self):
        a = {"mean": [40, 0, 0], "std": [0, 0, 0], "p05": 10, "p95": 90}
        b = {"mean": [60, 0, 0], "std": [0, 0, 0], "p05": 20, "p95": 80}
        m = C.merge_stats([a, b])
        self.assertAlmostEqual(m["mean"][0], 50.0)
        self.assertAlmostEqual(m["std"][0], 10.0, places=3)  # variance of the means: 100
        self.assertAlmostEqual(m["p05"], 15.0)
        self.assertEqual(C.merge_stats([])["mean"], [50, 0, 0])


class LutTransfer(unittest.TestCase):
    def test_identity_lut_when_stats_match(self):
        st = {"mean": [50, 0, 0], "std": [20, 10, 10]}
        size = 9
        lut = C.reinhard_lut(st, st, size=size, strength=1.0)
        self.assertEqual(lut.shape, (size ** 3, 3))
        g = np.linspace(0, 1, size)
        # .cube order: red fastest, then green, then blue
        self.assertTrue(np.allclose(lut[1], [g[1], 0, 0], atol=2e-3))
        self.assertTrue(np.allclose(lut[size], [0, g[1], 0], atol=2e-3))
        self.assertTrue(np.allclose(lut[size * size], [0, 0, g[1]], atol=2e-3))
        img = np.random.default_rng(3).integers(0, 256, (16, 16, 3)).astype(np.uint8)
        out = C.apply_lut(img, lut, size)
        self.assertLessEqual(int(np.abs(out.astype(int) - img.astype(int)).max()), 2)

    def test_mean_shift_lifts_lightness(self):
        src = {"mean": [50, 0, 0], "std": [20, 10, 10]}
        dst = {"mean": [60, 0, 0], "std": [20, 10, 10]}
        lut = C.reinhard_lut(src, dst, size=17, strength=1.0)
        grey = np.full((4, 4, 3), 119, np.uint8)  # L ~ 50
        l_in = C.rgb_to_lab(grey[0, 0] / 255.0)[0]
        l_out = C.rgb_to_lab(C.apply_lut(grey, lut, 17)[0, 0] / 255.0)[0]
        self.assertAlmostEqual(float(l_out - l_in), 10.0, delta=0.6)

    def test_write_cube(self):
        lut = C.reinhard_lut({"mean": [50, 0, 0], "std": [20, 10, 10]}, {"mean": [50, 0, 0], "std": [20, 10, 10]}, size=5)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "t.cube"
            C.write_cube(p, lut, 5, title="proof")
            lines = p.read_text(encoding="ascii").splitlines()
        self.assertEqual(lines[0], 'TITLE "proof"')
        self.assertEqual(lines[1], "LUT_3D_SIZE 5")
        self.assertEqual(len(lines), 4 + 125)
        self.assertEqual([round(float(v), 3) for v in lines[4].split()], [0.0, 0.0, 0.0])
        self.assertEqual([round(float(v), 3) for v in lines[-1].split()], [1.0, 1.0, 1.0])


class Palette(unittest.TestCase):
    def test_two_colour_image(self):
        img = np.zeros((40, 40, 3), np.uint8)
        img[:, :20] = (255, 0, 0)
        img[:, 20:] = (0, 0, 255)
        pal = C.palette(img, k=2)
        self.assertEqual(len(pal), 2)
        self.assertEqual(sorted(p["hex"] for p in pal), ["#0000FF", "#FF0000"])
        self.assertEqual([p["share"] for p in pal], [0.5, 0.5])
        self.assertEqual({p["name"] for p in pal}, {"red", "blue"})


if __name__ == "__main__":
    unittest.main()
