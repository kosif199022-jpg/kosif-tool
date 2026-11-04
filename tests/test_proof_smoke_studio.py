"""Known-answer proof for proofs/app-feature-transfer/smoke_studio.py (APPX-31 .. APPX-50).

Runs a byte-identical copy of the script in a temp folder (it writes results_studio.json next to itself,
so the repository copy is never touched). Every recipe builds its own synthetic data and checks a
measurable postcondition; this test requires all twenty to pass and checks the exact answers of the
deterministic ones (the PDG-style task graph APPX-47, the font build APPX-44, the vector booleans
APPX-45, the 6-part resumable download APPX-48 on a localhost server). Offline: numpy, OpenCV, Pillow,
fontTools, shapely, stdlib.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "app-feature-transfer" / "smoke_studio.py"
DEPS = ("numpy", "cv2", "PIL", "fontTools", "shapely")


@unittest.skipUnless(all(importlib.util.find_spec(m) for m in DEPS), "needs " + ", ".join(DEPS))
class StudioRecipes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as td:
            copy = Path(td) / SCRIPT.name
            shutil.copy2(SCRIPT, copy)
            cls.same = hashlib.sha256(copy.read_bytes()).hexdigest() == hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
            cls.done = subprocess.run([sys.executable, "-B", str(copy)], capture_output=True, text=True,
                                      encoding="utf-8", timeout=120, cwd=td)
            out = Path(td) / "results_studio.json"
            cls.report = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {}
        cls.by_id = {r["id"]: r for r in cls.report.get("results", [])}

    def test_copy_is_identical_and_all_pass(self):
        self.assertTrue(self.same)
        self.assertEqual(self.done.returncode, 0, self.done.stdout[-2000:] + self.done.stderr[-2000:])
        self.assertEqual(sorted(self.by_id), [f"APPX-{i}" for i in range(31, 51)])
        failed = [r["id"] + ": " + str(r["detail"]) for r in self.by_id.values() if not r["ok"]]
        self.assertEqual(failed, [])
        self.assertIn("20/20", self.done.stdout)

    def test_task_graph_caching(self):
        self.assertEqual(self.by_id["APPX-47"]["detail"],
                         "first run ['fetch', 'denoise', 'grade', 'thumb', 'sheet']; rerun cached []; "
                         "after a grade change only ['grade', 'sheet']")

    def test_deterministic_answers(self):
        self.assertIn("kern A/V -80 in GPOS", self.by_id["APPX-44"]["detail"])
        self.assertIn("circle − box = 3927 (half disc 3927)", self.by_id["APPX-45"]["detail"])
        self.assertIn("3000000 bytes in 6 ranged parts", self.by_id["APPX-48"]["detail"])
        self.assertIn("SHA-256 match True", self.by_id["APPX-48"]["detail"])
        self.assertIn("rating 4, label Green", self.by_id["APPX-42"]["detail"])


if __name__ == "__main__":
    unittest.main()
