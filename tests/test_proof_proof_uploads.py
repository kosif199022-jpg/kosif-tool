"""Known-answer proof for proofs/owner-uploads-20261023/proof_uploads.py (TRANS-U01, PART-U01, QA-U01).

Imports the script's own recipes and checks their numbers (slider curve, reveal field, graphics-only
layer), then runs the whole script on a byte-identical copy in a temp folder (it writes sheet.jpg and
receipt.json next to itself, so the repo copy is never touched) and reads the receipt back.
Offline: numpy + Pillow (raqm for the Arabic specimen).
"""
from __future__ import annotations

import hashlib
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
PROOFS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs"
SCRIPT = PROOFS / "owner-uploads-20261023" / "proof_uploads.py"

try:
    import numpy as np
    spec = importlib.util.spec_from_file_location("proof_uploads_under_test", SCRIPT)
    PU = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(PU)       # defines functions only; main() is not run on import
except ImportError as exc:  # pragma: no cover
    raise unittest.SkipTest(f"numpy/Pillow missing: {exc}")


class Recipes(unittest.TestCase):
    def test_easing_endpoints(self):
        for f in (PU.ease_out, PU.ease_in_out, PU.smoothstep):
            self.assertAlmostEqual(float(f(0.0)), 0.0)
            self.assertAlmostEqual(float(f(1.0)), 1.0)
        self.assertAlmostEqual(float(PU.ease_in_out(0.5)), 0.5)
        self.assertAlmostEqual(float(PU.ease_out(0.5)), 0.875)

    def test_slider_glide_crawl_reveal(self):
        self.assertAlmostEqual(float(PU.slider_progress(0.0)), 0.0)
        # 0.8 s: the glide is complete (0.46) plus 0.3/2.05 of the crawl's smoothstep
        x = 0.3 / 2.05
        self.assertAlmostEqual(float(PU.slider_progress(0.8)), 0.46 + 0.10 * x * x * (3 - 2 * x), places=9)
        ts = np.linspace(0, 3.5, 351)
        p = PU.slider_progress(ts)
        self.assertTrue(np.all(np.diff(p) >= -1e-9))
        crawl = p[(ts >= 0.9) & (ts <= 2.2)]
        self.assertTrue(np.all(np.diff(crawl) > 0))                   # never stops
        self.assertAlmostEqual(float(p[-1]), 1.0, places=9)

    def test_reveal_field_coverage(self):
        cov = [float(PU.reveal_alpha(p, 96, 54).mean()) for p in (0.0, 0.5, 1.0)]
        self.assertEqual(cov[0], 0.0)
        self.assertEqual(cov[2], 1.0)
        self.assertTrue(0.0 < cov[1] < 1.0)
        a = PU.reveal_alpha(0.45, 96, 54)
        self.assertGreater(a[:, 40:56].mean(), a[:, :8].mean())      # centre reveals before the edges

    def test_graphics_layer_recovers_exact_boxes(self):
        o, g = PU.plates()
        alpha = PU.graphics_layer(o, g)[..., 3]
        truth = np.zeros(alpha.shape, bool)
        truth[60:120, 40:300] = True
        truth[150:230, 330:440] = True
        self.assertTrue(np.array_equal(alpha > 0.5, truth))


class WholeRun(unittest.TestCase):
    def test_script_on_a_copy(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            run_dir = base / "owner-uploads-20261023"
            run_dir.mkdir()
            copy = run_dir / SCRIPT.name
            shutil.copy2(SCRIPT, copy)
            (base / "_shared").mkdir()
            os.symlink(PROOFS / "_shared" / "fonts", base / "_shared" / "fonts")
            self.assertEqual(hashlib.sha256(copy.read_bytes()).hexdigest(),
                             hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
            done = subprocess.run([sys.executable, "-B", str(copy)], capture_output=True, text=True, timeout=60)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertIn("PASS", done.stdout)
            rec = json.loads((run_dir / "receipt.json").read_text(encoding="utf-8"))
            self.assertTrue((run_dir / "sheet.jpg").is_file())
        self.assertTrue(rec["pass"])
        self.assertEqual(set(rec["checks"]), {"slider_curve", "reveal_field", "graphics_layer", "fonts"})
        self.assertEqual(rec["checks"]["graphics_layer"]["iou_vs_truth"], 1.0)
        self.assertEqual(rec["checks"]["reveal_field"]["coverage_at_p"][0], 0.0)
        self.assertEqual(rec["checks"]["reveal_field"]["coverage_at_p"][-1], 1.0)
        self.assertEqual(rec["checks"]["slider_curve"]["p_end"], 1.0)


if __name__ == "__main__":
    unittest.main()
