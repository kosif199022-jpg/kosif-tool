"""End-to-end test for the KOSIF Mimic port (.claude/skills/kosif-superpowers/scripts/mimic).

Builds the synthetic ground-truth reference, analyses it and checks the
scorecard against the thresholds recorded in proofs/mimic-synthetic. Skipped
when numpy, Pillow or ffmpeg are missing; the heavy run takes ~2 minutes.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIMIC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "mimic"
HAVE_DEPS = all(importlib.util.find_spec(m) for m in ("numpy", "PIL", "cv2", "fontTools")) and shutil.which("ffmpeg") and shutil.which("ffprobe")
HEAVY = os.environ.get("KOSIF_SKIP_HEAVY") != "1"


class MimicLayoutTest(unittest.TestCase):
    def test_modules_import_and_fonts_resolve(self):
        self.assertTrue((MIMIC / "mm_analyze.py").exists())
        self.assertIn("LGPL-2.1", (MIMIC / "mm_transitions.py").read_text(encoding="utf-8")[:1200])
        src = (MIMIC / "mm_common.py").read_text(encoding="utf-8")
        self.assertIn('"proofs" / "_shared" / "fonts"', src)
        if not HAVE_DEPS:
            self.skipTest("numpy/Pillow/OpenCV/fontTools/ffmpeg missing")
        out = subprocess.run([sys.executable, "-c", "import mm_common, mm_fonts_lib; "
                              "print(len(mm_common.FONT_DIRS), len(mm_fonts_lib.library(include_system=False)))"],
                             cwd=MIMIC, capture_output=True, text=True, check=True)
        dirs, faces = map(int, out.stdout.split())
        self.assertGreaterEqual(dirs, 1)
        self.assertGreaterEqual(faces, 6)


@unittest.skipUnless(HAVE_DEPS and HEAVY, "needs numpy, Pillow, OpenCV, fontTools, ffmpeg (set KOSIF_SKIP_HEAVY=1 to skip)")
class MimicSyntheticTest(unittest.TestCase):
    def test_synthetic_scorecard(self):
        with tempfile.TemporaryDirectory() as tmp:
            ref, work = Path(tmp, "ref"), Path(tmp, "work")
            subprocess.run([sys.executable, "synthetic/make_reference.py", str(ref)], cwd=MIMIC, check=True,
                           capture_output=True, text=True)
            truth = json.loads((ref / "truth.json").read_text(encoding="utf-8"))
            run = subprocess.run([sys.executable, "synthetic/run_synthetic.py", str(ref), str(work)], cwd=MIMIC,
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr[-2000:])
            spec = json.loads((work / "spec.json").read_text(encoding="utf-8"))
            got = [(t["type"], t["ts"], t["te"]) for t in spec["transitions"]]
            want = [(t["type"], t["ts"], t["te"]) for t in truth["transitions"]]
            self.assertEqual(len(got), len(want))
            for g, w in zip(got, want):
                self.assertEqual(g[0], w[0])
                self.assertLessEqual(abs(g[1] - w[1]) + abs(g[2] - w[2]), 2)
            self.assertEqual(len(spec["texts"]), len(truth["texts"]))
            norm = lambda s: s.replace("_", "")
            self.assertEqual([norm(t["anim_in"]["type"]) for t in spec["texts"]], [norm(t["in"]) for t in truth["texts"]])
            self.assertEqual(spec["reference"]["frames"], truth["frames"])
            self.assertIn("TEXT EVENTS", run.stdout)
            self.assertIn("FONTS  5/5", run.stdout)


if __name__ == "__main__":
    unittest.main()
