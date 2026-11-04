"""Known-answer proof for mm_textfx.py (scripts/mimic): text events typeset and animated frame by frame.

One Arabic line is placed at a known box with a known ink height, fades in on a linear alpha curve,
holds, and slides out to the right. The drawn frames must put the ink at the box centre with the
target height, at half strength halfway through the fade, and shifted by the curve's dx on the exit.
Offline: numpy, Pillow (raqm) and the bundled OFL fonts.
"""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
SCRIPT = MIMIC / "mm_textfx.py"
AMIRI = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "_shared" / "fonts" / "Amiri-Bold.ttf"
os.environ.setdefault("MIMIC_QUIET", "1")
sys.path.insert(0, str(MIMIC))

try:
    import numpy as np
    import mm_textfx as FX
    import mm_render_text as RT
except ImportError as exc:  # pragma: no cover
    raise unittest.SkipTest(f"mimic dependencies missing: {exc}")

W = H = 240


def event(**over):
    ev = {"id": 1, "font": {"chosen": str(AMIRI)}, "style": {"fill": "#FFFFFF"},
          "time": {"in_start": 0, "full_in": 10, "full_out": 20, "out_end": 30},
          "lines": [{"text": "سلام", "ink_h": 40, "bbox": [80, 100, 160, 140]}],
          "anim_in": {"type": "fade", "curves": {"alpha": [0.0, 1.0]}},
          "anim_out": {"type": "slide", "curves": {"alpha": [1.0, 1.0], "dx": [0.0, 44.0]}}}
    ev.update(over)
    return ev


def ink(frame):
    g = frame.max(-1)
    ys, xs = np.nonzero(g > 60)
    return g, ((xs.min() + xs.max() + 1) / 2, (ys.min() + ys.max() + 1) / 2), ys.max() + 1 - ys.min()


class Helpers(unittest.TestCase):
    def test_script_present(self):
        self.assertTrue(SCRIPT.is_file())

    def test_interp(self):
        self.assertIsNone(FX._interp([], 0.5))
        self.assertAlmostEqual(FX._interp([0, 10], 0.25), 2.5)
        self.assertAlmostEqual(FX._interp([0, 10, 0], 0.5), 10.0)
        self.assertAlmostEqual(FX._interp([0, 10], 2.0), 10.0)          # clamped

    def test_consensus_style(self):
        evs = [{"style": {"shadow": {"dx_px": 2, "dy_px": 2, "blur_px": 1, "opacity": 0.4, "fit": 0.9}}},
               {"style": {"shadow": {"dx_px": 4, "dy_px": 6, "blur_px": 3, "opacity": 0.6, "fit": 0.7}}},
               {"style": {"shadow": {"dx_px": 99, "dy_px": 99, "blur_px": 99, "opacity": 1, "fit": 0.1}}}]
        c = FX.consensus_style(evs)
        self.assertEqual(c["shadow"], {"dx_px": 3.0, "dy_px": 4.0, "blur_px": 2.0, "opacity": 0.5, "color": "#000000"})
        self.assertNotIn("outline", c)
        self.assertEqual(FX.consensus_style([{"style": {"outline": {"width_px": 2}}}]), {"outline": {"width_px": 2}})


@unittest.skipUnless(RT.HAVE_RAQM, "Pillow without raqm")
class EventReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.L = FX.EventLayer(event(), W, H, analysis_w=W)

    def test_layer_ready_and_skips_empty_events(self):
        self.assertTrue(self.L.ok)
        self.assertEqual(Path(self.L.font).name, "Amiri-Bold.ttf")
        self.assertFalse(FX.EventLayer(event(lines=[{"text": " ", "ink_h": 10, "bbox": [0, 0, 1, 1]}]), W, H, W).ok)

    def test_timeline_states(self):
        self.assertIsNone(self.L.state(-1))
        self.assertIsNone(self.L.state(30))
        self.assertAlmostEqual(self.L.state(0)["alpha"], 0.0)
        self.assertAlmostEqual(self.L.state(5)["alpha"], 0.5)
        self.assertEqual(self.L.state(15), {"alpha": 1.0, "dx": 0.0, "dy": 0.0, "scale": 1.0, "sigma": 0.0, "words": None})
        u = (25 - 19) / 11
        self.assertAlmostEqual(self.L.state(25)["dx"], 44.0 * u, places=6)

    def test_drawn_frames(self):
        held = self.L.draw(np.zeros((H, W, 3), np.uint8), 15)
        g, (cx, cy), ih = ink(held)
        self.assertAlmostEqual(cx, 120, delta=2)                        # box centre
        self.assertAlmostEqual(cy, 120, delta=2)
        self.assertAlmostEqual(ih, 40, delta=2)                         # measured ink height
        self.assertEqual(int(g.max()), 255)
        half = self.L.draw(np.zeros((H, W, 3), np.uint8), 5).max()
        self.assertAlmostEqual(int(half), 127, delta=2)                 # alpha 0.5
        self.assertEqual(int(self.L.draw(np.zeros((H, W, 3), np.uint8), 0).max()), 0)
        self.assertEqual(int(self.L.draw(np.zeros((H, W, 3), np.uint8), 40).max()), 0)
        _, (cx2, cy2), _ = ink(self.L.draw(np.zeros((H, W, 3), np.uint8), 25))
        self.assertAlmostEqual(cx2 - cx, 44.0 * (25 - 19) / 11, delta=1.5)
        self.assertAlmostEqual(cy2, cy, delta=1)


if __name__ == "__main__":
    unittest.main()
