"""blender_cinema.py: preset table, Kelvin colours and CLI shape always; real Cycles renders of every cinematic preset,
an animated camera move and the live inventory when Blender (or the bpy module) is on this machine. Proof behind
APPX-114…APPX-117. Set KOSIF_BLENDER_FULL=1 to render every preset (about 2 minutes on a laptop CPU)."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "scripts" / "blender_cinema.py"
spec = importlib.util.spec_from_file_location("blender_cinema", PATH)
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)
HAVE = bool(bc.find_blender() or bc.bpy_python())


def cli(*args):
    p = subprocess.run([sys.executable, str(PATH), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("{")]
    return p.returncode, (json.loads(line[-1]) if line else {"stdout": p.stdout, "stderr": p.stderr})


class Offline(unittest.TestCase):
    def test_presets_complete(self):
        self.assertEqual(set(bc.PRESETS), {"product-hero", "golden-hour", "noir-volumetric", "neon-night", "anamorphic-epic"})
        for name, p in bc.PRESETS.items():
            for key in ("lens", "fstop", "blades", "ratio", "look", "set", "material", "lights", "cam", "finish", "ar"):
                self.assertIn(key, p, f"{name}.{key}")
            self.assertTrue(p["look"].startswith("AgX"))

    def test_kelvin(self):
        warm, cool = bc.kelvin_rgb(3200), bc.kelvin_rgb(9000)
        self.assertGreater(warm[0], warm[2])
        self.assertGreater(cool[2], cool[0] * 0.9)

    def test_presets_cli(self):
        p = subprocess.run([sys.executable, str(PATH), "presets"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(p.returncode, 0)
        self.assertIn("anamorphic-epic", p.stdout)


@unittest.skipUnless(HAVE, "Blender not found (KOSIF_BLENDER / PATH / pip install bpy)")
class WithBlender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.d = Path(cls.tmp.name) / "رندر"
        cls.d.mkdir()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_doctor(self):
        code, r = cli("doctor")
        self.assertEqual(code, 0)
        self.assertTrue(r["ready"])

    def test_inventory(self):
        out = self.d / "inventory.json"
        code, r = cli("inventory", "-o", str(out))
        self.assertTrue(r["verified"], r)
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertGreater(data["operators_total"], 1000)
        self.assertIn("CompositorNodeGlare", data["compositor_nodes"])
        self.assertIn("MULTIPLE_SCATTERING", data["sky_types"])

    def test_render_presets(self):
        presets = sorted(bc.PRESETS) if os.environ.get("KOSIF_BLENDER_FULL") else ["neon-night", "golden-hour"]
        for preset in presets:
            with self.subTest(preset=preset):
                code, r = cli("render", "--preset", preset, "--res", "320x180", "--quality", "preview", "--samples", "8",
                              "-o", str(self.d / f"{preset}.png"))
                self.assertTrue(r.get("verified"), r)
                m = r["metrics"]
                self.assertEqual(m["engine"], "CYCLES")
                self.assertEqual(m["view_transform"], "AgX")
                self.assertEqual(m["warnings"], [])
                self.assertGreater(max(m["image"]["mean"]), 10, preset)    # not a black frame

    def test_animated_orbit(self):
        out = self.d / "orbit.mp4"
        code, r = cli("render", "--preset", "product-hero", "--res", "160x90", "--quality", "preview", "--samples", "4",
                      "--frames", "6", "--move", "orbit", "--save-blend", str(self.d / "orbit.blend"), "-o", str(out))
        self.assertTrue(r.get("verified"), r)
        self.assertEqual(r["metrics"]["frames"], 6)
        self.assertTrue((self.d / "orbit.blend").exists())


if __name__ == "__main__":
    unittest.main()
