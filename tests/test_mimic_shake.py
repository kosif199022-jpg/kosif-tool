"""Regression: mm_analyze must not read camera shake as transitions, and must still find a hard cut.

A continuous shaking-camera clip (testsrc2 under a moving crop, no cuts) used to give two phantom
"gradual" transitions with confidence 0.05. Both copies of the analyzer (vendor kosif-mimic and the
scripts/mimic port) are checked. Clips are made with ffmpeg in a temp dir outside the checkout.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "kosif-superpowers"
COPIES = [SKILL / "vendor" / "100-superskills" / "skills" / "kosif-mimic" / "scripts", SKILL / "scripts" / "mimic"]
HAVE_DEPS = all(importlib.util.find_spec(m) for m in ("numpy", "PIL", "cv2")) and shutil.which("ffmpeg") and shutil.which("ffprobe")
RUN = ("import sys, json; sys.path.insert(0, sys.argv[1]); import mm_analyze; "
       "s = mm_analyze.analyze(sys.argv[2], sys.argv[3], skip_text=True); "
       "print(json.dumps({'shots': len(s['shots']), 'transitions': "
       "[[t['type'], t['ts_s'], t['confidence']] for t in s['transitions']]}))")


def _ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True, capture_output=True, timeout=120)


@unittest.skipUnless(HAVE_DEPS, "needs numpy, Pillow, OpenCV, ffmpeg, ffprobe")
class MimicShakeRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="mimic-shake-"))
        cls.shake = cls.tmp / "shake.mp4"
        # same shaking camera as the Black Dragon self-test clip (_black_dragon_media.self_test_clip)
        _ffmpeg("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=6",
                "-vf", "crop=600:336:20+15*sin(2*PI*3.1*t):12+9*sin(2*PI*2.3*t+1),scale=640:360",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(cls.shake))
        cls.cut = cls.tmp / "cut.mp4"
        # one hard cut at exactly 3.0 s (testsrc2 -> mandelbrot), as in _black_dragon_skill._cut_clip
        _ffmpeg("-f", "lavfi", "-i", "testsrc2=s=640x360:r=30:d=3", "-f", "lavfi", "-i", "mandelbrot=s=640x360:r=30",
                "-filter_complex", "[1]trim=duration=3,setpts=PTS-STARTPTS[b];[0][b]concat=n=2:v=1:a=0[v]",
                "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.cut))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _analyze(self, copy: Path, clip: Path) -> dict:
        work = self.tmp / f"{copy.parent.name}-{copy.name}-{clip.stem}"
        out = subprocess.run([sys.executable, "-c", RUN, str(copy), str(clip), str(work)],
                             capture_output=True, text=True, timeout=600)
        self.assertEqual(out.returncode, 0, out.stderr[-2000:])
        return json.loads(out.stdout.strip().splitlines()[-1])

    def test_shaking_camera_has_no_transitions(self):
        for copy in COPIES:
            with self.subTest(copy=str(copy.relative_to(ROOT))):
                res = self._analyze(copy, self.shake)
                self.assertEqual(res["transitions"], [], res)
                self.assertEqual(res["shots"], 1, res)

    def test_hard_cut_at_three_seconds_is_found(self):
        for copy in COPIES:
            with self.subTest(copy=str(copy.relative_to(ROOT))):
                res = self._analyze(copy, self.cut)
                self.assertEqual(len(res["transitions"]), 1, res)
                kind, ts, _ = res["transitions"][0]
                self.assertEqual(kind, "cut", res)
                self.assertLessEqual(abs(ts - 3.0), 0.1, res)
                self.assertEqual(res["shots"], 2, res)


if __name__ == "__main__":
    unittest.main()
