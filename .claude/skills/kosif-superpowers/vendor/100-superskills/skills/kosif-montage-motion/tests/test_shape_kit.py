"""shape-kit.js (SDF sculpting → surface-nets meshes) checked numerically under Node: a sphere's volume, area and
radius, a closed (watertight) surface, smooth union filling the gap, carving with a tint, and the rigged bunny."""
import json
import shutil
import subprocess
import unittest
from pathlib import Path

CHECK = Path(__file__).resolve().parent / "js" / "shape_kit_check.cjs"


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class ShapeKitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        out = subprocess.run(["node", str(CHECK)], capture_output=True, text=True, timeout=300)
        if out.returncode != 0:
            raise AssertionError(out.stderr[-2000:])
        cls.r = json.loads(out.stdout.strip().splitlines()[-1])

    def test_sphere_is_accurate_and_closed(self):
        s = self.r["sphere"]
        self.assertAlmostEqual(s["volRatio"], 1.0, delta=0.02)
        self.assertAlmostEqual(s["areaRatio"], 1.0, delta=0.03)
        self.assertLess(s["maxRadiusErr"], 1e-3)          # vertices projected onto the true surface
        self.assertEqual(s["openEdges"], 0)               # watertight: every edge shared by exactly two triangles

    def test_coarse_to_fine_skips_empty_space(self):
        s = self.r["sphere"]
        self.assertLess(s["evals"], 0.6 * s["full"])

    def test_smooth_union_and_carving(self):
        self.assertAlmostEqual(self.r["hardUnionGap"], 0.0, delta=1e-9)   # two spheres just touching
        self.assertLess(self.r["smoothUnionGap"], -0.005)                  # the blend fills the waist
        c = self.r["carved"]
        self.assertEqual(c["openEdges"], 0)
        self.assertGreater(c["tintRed"], 0.5)          # the carve is tinted red inside
        self.assertLess(abs(c["plainRed"]), 1e-6)      # the untouched side keeps the base colour

    def test_bunny_rig(self):
        b = self.r["bunny"]
        for part in ("body", "head", "earL", "earR", "tail", "eyeL", "eyeR", "mouth", "scarf"):
            self.assertIn(part, b["parts"])
        self.assertGreater(b["triangles"], 50000)
        for fn in ("sculpt", "plushMaterial", "trussOverlay", "makeLitePost", "bunny", "stageDisc"):
            self.assertIn(fn, self.r["api"])


if __name__ == "__main__":
    unittest.main()
