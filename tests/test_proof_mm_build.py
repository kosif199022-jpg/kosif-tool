"""Known-answer proof for mm_build.py (scripts/mimic): fit filters, look solver, placeholder plates and a
tiny end-to-end placeholder build encoded with ffmpeg and read back frame by frame.

Offline: numpy, ffmpeg/ffprobe. Runs in a few seconds.
"""
from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
SCRIPT = MIMIC / "mm_build.py"
os.environ.setdefault("MIMIC_QUIET", "1")
sys.path.insert(0, str(MIMIC))
HAVE_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))

try:
    import numpy as np
    import mm_build as B
except ImportError as exc:  # pragma: no cover
    raise unittest.SkipTest(f"mimic dependencies missing: {exc}")


def ff_frames(path: Path, w: int, h: int) -> "np.ndarray":
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True, timeout=60).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


class FitFilters(unittest.TestCase):
    def test_script_present(self):
        self.assertTrue(SCRIPT.is_file())

    def test_cover_and_contain_strings(self):
        self.assertEqual(B._fit_filter(1920, 1080, 1080, 1920, "cover"),
                         "scale=3414:1920:flags=lanczos,crop=1080:1920:1167:0,setsar=1")
        self.assertEqual(B._fit_filter(1920, 1080, 1080, 1920, "cover", focus=(0.0, 0.5)),
                         "scale=3414:1920:flags=lanczos,crop=1080:1920:0:0,setsar=1")
        self.assertEqual(B._fit_filter(1920, 1080, 1080, 1920, "contain"),
                         "scale=1080:608:flags=lanczos,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1")
        self.assertIn("boxblur", B._fit_filter(1920, 1080, 1080, 1920, "blur"))

    def test_chain(self):
        rep = {"fit": "cover", "flip": True}
        c = B._chain(rep, {"w": 640, "h": 360}, 360, 640, Fraction(30), 2.0, None)
        self.assertEqual(c, "setpts=(PTS-STARTPTS)/2.000000,fps=30/1,"
                            "scale=1138:640:flags=lanczos,crop=360:640:389:0,setsar=1,hflip")
        self.assertNotIn("setpts", B._chain({"fit": "contain"}, {"w": 640, "h": 360}, 360, 640, Fraction(30), 1.0, None))

    @unittest.skipUnless(HAVE_FF, "ffmpeg/ffprobe missing")
    def test_filters_run_in_ffmpeg(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=white:s=192x108:d=0.2:r=10",
                            "-pix_fmt", "yuv420p", str(src)], check=True, timeout=60)
            for fit in ("cover", "contain", "blur"):
                out = Path(td) / f"{fit}.mp4"
                vf = B._fit_filter(192, 108, 108, 192, fit)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-filter_complex", f"[0:v]{vf}[v]",
                                "-map", "[v]", "-pix_fmt", "yuv444p", str(out)], check=True, timeout=60)
                fr = ff_frames(out, 108, 192)[0].astype(int)
                if fit == "cover":
                    self.assertGreater(fr.mean(), 240)          # white everywhere
                if fit == "contain":
                    self.assertLess(fr[:30].mean(), 20)          # black pad above the 108x60 picture
                    self.assertGreater(fr[90:100].mean(), 240)   # picture in the middle


class LookSolver(unittest.TestCase):
    def test_vignette_mask_values(self):
        m = B.vignette_mask(97, 171, 0.4)
        self.assertEqual(m.shape, (171, 97, 1))
        self.assertAlmostEqual(float(m[85, 48, 0]), 1.0, places=2)
        self.assertAlmostEqual(float(m[0, 0, 0]), 0.6, places=2)   # corner radius 1 -> 1 - strength

    def test_solve_vignette_inverts_its_model(self):
        W, H = 96, 170
        r = B._radial(W, H)
        cr = float((r[r > 0.85] ** 2.2).mean())
        cc = float((r[r < 0.25] ** 2.2).mean())
        for v in (0.2, 0.45, 0.7):
            ratio = (1 - v * cr) / (1 - v * cc)   # flat plate darkened by strength v
            self.assertAlmostEqual(B.solve_vignette(ratio, 1.0), v, places=6)
        self.assertEqual(B.solve_vignette(1.0, 1.0), 0.0)
        self.assertEqual(B.solve_vignette(0.0, 1.0), 0.9)          # clamped

    def test_scale_style_and_event(self):
        st = {"fill": "#FFFFFF", "shadow": {"dx_px": 2, "blur_px": 4, "opacity": 0.5}}
        s2 = B._scale_style(st, 0.5)
        self.assertEqual(s2["shadow"], {"dx_px": 1.0, "blur_px": 2.0, "opacity": 0.5})
        self.assertIs(B._scale_style(st, 1), st)
        ev = {"lines": [{"bbox": [10, 20, 30, 40], "ink_h": 8}], "style": st,
              "anim_in": {"curves": {"dx": [4, 0]}, "word_onsets": [{"box": [2, 2, 6, 6]}]}}
        e2 = B._scaled_event(ev, 0.5)
        self.assertEqual(e2["lines"][0]["bbox"], [5, 10, 15, 20])
        self.assertEqual(e2["lines"][0]["ink_h"], 4)
        self.assertEqual(e2["anim_in"]["curves"]["dx"], [2, 0])
        self.assertEqual(e2["anim_in"]["word_onsets"][0]["box"], [1, 1, 3, 3])
        self.assertEqual(ev["lines"][0]["bbox"], [10, 20, 30, 40])   # deep copy

    def test_placeholder_gradient(self):
        shot = {"palette": [{"hex": "#FF0000"}, {"hex": "#0000FF"}]}
        frames = list(B.placeholder_frames(shot, 8, 11, 3))
        self.assertEqual(len(frames), 3)
        f0 = frames[0]
        self.assertEqual(f0.shape, (11, 8, 3))
        np.testing.assert_allclose(f0[0, 0], [255, 0, 0], atol=1e-3)
        np.testing.assert_allclose(f0[-1, 0], [0, 0, 255], atol=1e-3)
        np.testing.assert_allclose(f0[5, 3], [127.5, 0, 127.5], atol=1e-3)


@unittest.skipUnless(HAVE_FF, "ffmpeg/ffprobe missing")
class PlaceholderBuild(unittest.TestCase):
    def test_end_to_end_placeholder_build(self):
        W, H, N = 64, 112, 20
        spec = {"reference": {"fps": "10", "w": W, "h": H, "frames": N, "path": "none.mp4"},
                "shots": [{"id": 1, "start": 0, "end": 10, "palette": [{"hex": "#FF0000"}, {"hex": "#FF0000"}]},
                          {"id": 2, "start": 10, "end": 20, "palette": [{"hex": "#00FF00"}, {"hex": "#00FF00"}]}],
                "transitions": [], "texts": [], "look": {"letterbox": {"top": 0.125, "bottom": 0.125}}}
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            (work / "spec.json").write_text(json.dumps(spec), encoding="utf-8")
            out = work / "remake.mp4"
            rep = B.build(str(work), out=str(out), placeholder=True, crf=12, preset="ultrafast")
            self.assertEqual(rep["frames_written"], N)
            self.assertEqual((rep["w"], rep["h"]), (W, H))
            self.assertEqual(rep["audio"], "none")
            fr = ff_frames(out, W, H).astype(int)
        self.assertEqual(len(fr), N)
        bar = int(round(0.125 * H))
        self.assertLess(fr[5, :bar - 2].mean(), 20)                  # letterbox top
        self.assertLess(fr[5, H - bar + 2:].mean(), 20)              # letterbox bottom
        mid = fr[5, H // 2 - 4:H // 2 + 4, W // 2 - 4:W // 2 + 4].reshape(-1, 3).mean(0)
        self.assertGreater(mid[0], 200)
        self.assertLess(mid[1], 60)                                  # shot 1 is red
        mid = fr[15, H // 2 - 4:H // 2 + 4, W // 2 - 4:W // 2 + 4].reshape(-1, 3).mean(0)
        self.assertGreater(mid[1], 200)
        self.assertLess(mid[0], 60)                                  # shot 2 is green


if __name__ == "__main__":
    unittest.main()
