"""Motion physics (scripts/motion_physics.py): springs, CSS cubic-bezier, stagger and keyframe sampling."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SK / "scripts"))
import motion_physics as M  # noqa: E402

CLI = [sys.executable, str(SK / "scripts" / "motion_physics.py")]


class MotionPhysicsTest(unittest.TestCase):
    def test_self_test(self):
        p = subprocess.run(CLI + ["--self-test"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_spring_regimes(self):
        firm = M.spring(0, 1, 170, 26)
        self.assertTrue(firm["settled"])
        self.assertLess(firm["overshoot_pct"], 1.0)
        self.assertEqual(firm["values"][0], 0)
        self.assertEqual(firm["values"][-1], 1)
        wobbly = M.spring(0, 1, 180, 8)
        self.assertLess(wobbly["damping_ratio"], 1)
        self.assertGreater(wobbly["overshoot_pct"], 20)
        self.assertGreater(wobbly["seconds"], firm["seconds"])
        down = M.spring(100, 0, 170, 26)
        self.assertEqual(down["values"][-1], 0)
        with self.assertRaises(ValueError):
            M.spring(0, 1, 0, 10)

    def test_bezier_matches_css(self):
        ease = M.parse_ease("ease")
        self.assertAlmostEqual(ease(0.5), 0.8024, places=3)
        lin = M.parse_ease("linear")
        for x in (0.1, 0.37, 0.9):
            self.assertAlmostEqual(lin(x), x, places=5)
        self.assertEqual(M.parse_ease("steps(4)")(0.3), 0.25)
        with self.assertRaises(ValueError):
            M.bezier(1.5, 0, 0, 1)
        with self.assertRaises(ValueError):
            M.parse_ease("wobble")

    def test_stagger_origins(self):
        self.assertEqual(M.stagger(4, 0.1), [0.0, 0.1, 0.2, 0.3])
        self.assertEqual(M.stagger(5, 0.1, origin="center"), [0.2, 0.1, 0.0, 0.1, 0.2])
        self.assertEqual(M.stagger(5, 0.1, origin="edges"), [0.0, 0.1, 0.2, 0.1, 0.0])
        grid = M.stagger(9, 0.1, origin="center", grid=(3, 3))
        self.assertEqual(grid[4], 0.0)
        self.assertAlmostEqual(grid[0], grid[8])
        with self.assertRaises(ValueError):
            M.stagger(10, 0.1, grid=(3, 3))

    def test_keyframes_cli_and_css(self):
        p = subprocess.run(CLI + ["keyframes", "--track", "0:0,1:100", "--fps", "10"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        vals = json.loads(p.stdout)["values"]
        self.assertEqual(len(vals), 11)
        self.assertEqual(vals[5], 50.0)
        p = subprocess.run(CLI + ["spring", "--css", "pop"], capture_output=True, text=True, timeout=60)
        self.assertIn("@keyframes pop", p.stdout)
        p = subprocess.run(CLI + ["keyframes", "--track", "1:0,0:5"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
