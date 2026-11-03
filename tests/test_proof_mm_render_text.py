"""Known-answer proof for mm_render_text.py (scripts/mimic): Arabic-correct line rendering and styling.

Checks shaping-engine routing, that per-word alphas add up to the full line and follow Arabic reading
order (first word on the right), size fitting to a target ink height, the libass engine agreeing with the
Pillow engine on the word's shape, style composition (outline, box) and exact alpha compositing.
Offline: numpy, Pillow (raqm), OpenCV or SciPy, ffmpeg with libass for the ass engine.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
SCRIPT = MIMIC / "mm_render_text.py"
AMIRI = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "_shared" / "fonts" / "Amiri-Regular.ttf"
os.environ.setdefault("MIMIC_QUIET", "1")
sys.path.insert(0, str(MIMIC))

try:
    import numpy as np
    import mm_render_text as RT
except ImportError as exc:  # pragma: no cover
    raise unittest.SkipTest(f"mimic dependencies missing: {exc}")


def have_libass() -> bool:
    if not shutil.which("ffmpeg"):
        return False
    out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True, timeout=30).stdout
    return " ass " in out


class Routing(unittest.TestCase):
    def test_script_present(self):
        self.assertTrue(SCRIPT.is_file())

    def test_engine_name(self):
        self.assertEqual(RT.engine_name("pil"), "pil")
        self.assertEqual(RT.engine_name("ass"), "ass")
        self.assertEqual(RT.engine_name("auto"), "pil" if RT.HAVE_RAQM else "ass")

    def test_ink_bbox(self):
        a = np.zeros((10, 20), np.float32)
        a[2:5, 7:12] = 1
        self.assertEqual(RT._ink_bbox(a), (7, 2, 12, 5))
        self.assertEqual(RT._ink_bbox(np.zeros((4, 4), np.float32)), (0, 0, 1, 1))


@unittest.skipUnless(RT.HAVE_RAQM, "Pillow without raqm")
class PilEngine(unittest.TestCase):
    def test_words_sum_to_line_in_rtl_order(self):
        L = RT.render_line_pil("سلام عليكم", str(AMIRI), 48)
        self.assertEqual(len(L.words), 2)
        total = np.clip(sum(L.words), 0, 1)
        self.assertLess(float(np.abs(total - L.alpha).max()), 1e-5)
        first, second = L.word_boxes
        self.assertGreater(first[0], second[2] - 1)          # reading order: word 1 sits right of word 2
        x0, y0, x1, y1 = L.ink
        self.assertEqual((x0, y0), (RT.PAD, RT.PAD))            # cropped with PAD margin around the ink
        self.assertEqual(L.alpha.shape, (y1 + RT.PAD, x1 + RT.PAD))
        self.assertEqual(L.ink_w, x1 - x0)

    def test_latin_is_left_to_right(self):
        L = RT.render_line_pil("Hello world", str(AMIRI), 40)
        self.assertLess(L.word_boxes[0][0], L.word_boxes[1][0])

    def test_fit_size_hits_target_ink_height(self):
        for target in (24, 40, 63):
            size, L = RT.fit_size("سلام", str(AMIRI), target, engine="pil")
            self.assertLessEqual(abs(L.ink_h - target), 1, (target, size, L.ink_h))
        s1, _ = RT.fit_size("سلام", str(AMIRI), 24, engine="pil")
        s2, _ = RT.fit_size("سلام", str(AMIRI), 48, engine="pil")
        self.assertGreater(s2, s1)

    @unittest.skipUnless(have_libass(), "ffmpeg without libass")
    def test_ass_engine_agrees_on_shape(self):
        p = RT.render_line("سلام", str(AMIRI), 48, engine="pil")
        a = RT.render_line("سلام", str(AMIRI), 48, engine="ass")
        self.assertGreater(a.ink_h, 5)
        ratio_p, ratio_a = p.ink_w / p.ink_h, a.ink_w / a.ink_h
        self.assertLess(abs(ratio_p - ratio_a) / ratio_p, 0.15)


class Styling(unittest.TestCase):
    def setUp(self):
        self.alpha = np.zeros((20, 30), np.float32)
        self.alpha[5:15, 5:25] = 1.0

    def test_fill_only(self):
        out, (ox, oy) = RT.compose(self.alpha, {"fill": "#FF0000"})
        self.assertEqual((ox, oy), (2, 2))
        self.assertEqual(out.shape, (24, 34, 4))
        np.testing.assert_allclose(out[oy + 10, ox + 15], [1, 0, 0, 1], atol=1e-6)
        np.testing.assert_allclose(out[0, 0], [0, 0, 0, 0], atol=1e-6)

    def test_outline_and_box(self):
        out, (m, _) = RT.compose(self.alpha, {"fill": "#FFFFFF", "outline": {"color": "#0000FF", "width_px": 2}})
        self.assertEqual(m, 5)                                  # width + 3
        np.testing.assert_allclose(out[m + 10, m + 15], [1, 1, 1, 1], atol=1e-6)   # fill inside
        np.testing.assert_allclose(out[m + 10, m + 4], [0, 0, 1, 1], atol=1e-6)    # outline ring left of ink
        out, (m, _) = RT.compose(self.alpha, {"fill": "#FFFFFF", "box": {"color": "#00FF00", "opacity": 0.5,
                                                                         "pad_px": 4}})
        self.assertEqual(m, 8)
        np.testing.assert_allclose(out[m + 3, m + 3], [0, 0.5, 0, 0.5], atol=1e-6)  # inside the pad, outside ink

    def test_composite_exact(self):
        frame = np.zeros((10, 10, 3), np.uint8)
        layer = np.zeros((4, 4, 4), np.float32)
        layer[...] = [1, 1, 1, 1]
        layer[0, 0] = [0.5, 0.5, 0.5, 0.5]                      # premultiplied 50 % white
        RT.composite(frame, layer, 2, 3)
        self.assertEqual(int(frame[3, 2, 0]), 127)
        self.assertEqual(int(frame[4, 3, 1]), 255)
        self.assertEqual(int(frame[2, 2, 0]), 0)
        self.assertEqual(int(frame[7, 2, 0]), 0)
        before = frame.copy()
        RT.composite(frame, layer, -50, -50)                    # fully outside: unchanged, no error
        self.assertTrue(np.array_equal(frame, before))


if __name__ == "__main__":
    unittest.main()
