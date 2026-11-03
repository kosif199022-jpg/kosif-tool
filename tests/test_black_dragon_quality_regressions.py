"""Regression cases from Black Dragon incident report dated 2026-11-03.

Tests use synthetic fixtures only: no paid API, uploads or third-party media.
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SUPER = ROOT / ".claude/skills/kosif-superpowers"
SCRIPTS = SUPER / "scripts"
VENDOR = SUPER / "vendor/100-superskills/skills"
sys.path.insert(0, str(SCRIPTS))
import black_dragon as dragon

HAS_NUMPY = importlib.util.find_spec("numpy") is not None
HAS_OPENPYXL = importlib.util.find_spec("openpyxl") is not None
HAS_PIL = importlib.util.find_spec("PIL") is not None
HAS_CV2 = importlib.util.find_spec("cv2") is not None


class BlackDragonQualityRegressions(unittest.TestCase):
    def test_probe_never_runs_import_time_code_even_for_argparse_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / "EXECUTED.txt"
            cli = root / "malicious.py"
            cli.write_text(
                "from pathlib import Path\n"
                + "Path(" + repr(str(marker)) + ").write_text('unsafe')\n"
                + "import argparse\n"
                + "p = argparse.ArgumentParser()\n"
                + "p.parse_args()\n", encoding="utf-8"
            )
            with patch.object(dragon, "REPO", root):
                result = dragon._probe(
                    "tool:untrusted", {"kind": "cli", "root": "repo", "path": "malicious.py"},
                    root / "job"
                )
            self.assertEqual(result["status"], "static-only", result)
            self.assertFalse(marker.exists(), "AST probe executed untrusted module-level code")
            receipt = json.loads(Path(result["output"]).read_text(encoding="utf-8"))
            self.assertFalse(receipt["executed"])

    @unittest.skipUnless(HAS_OPENPYXL, "openpyxl optional in this CI lane; exercised in Black Dragon checks")
    def test_excel_planted_statement_constant_is_high_and_not_pass(self):
        from openpyxl import Workbook
        with tempfile.TemporaryDirectory() as temp:
            tmp = Path(temp)
            wb = Workbook()
            pnl = wb.active
            pnl.title = "PnL"
            pnl["D5"] = "=C5*2"
            pnl["D6"] = 12345  # simulates overwriting a calculated formula
            wb.create_sheet("Checks")
            src = tmp / "planted.xlsx"
            wb.save(src)
            script = VENDOR / "excel-model-architect/scripts/model_audit.py"
            p = subprocess.run([sys.executable, str(script), str(src), "--json"],
                               text=True, capture_output=True, timeout=30)
            self.assertEqual(p.returncode, 1, p.stderr)
            result = json.loads(p.stdout)
            self.assertEqual(result["verdict"], "REVISE")
            self.assertGreaterEqual(result["stats"]["hardcoded"], 1)
            self.assertTrue(any(x["sev"] == "HIGH" and x["cell"] == "PnL!D6"
                                and "12345" in x["issue"] for x in result["findings"]), result)

    @unittest.skipUnless(HAS_NUMPY and HAS_PIL, "numpy/Pillow optional in generic CI; exercised in Black Dragon checks")
    def test_pixel_studio_headless_code_renders_supplied_svg_not_default_scene(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            tmp = Path(temp)
            svg = tmp / "custom.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">'
                           '<rect x="0" y="0" width="1200" height="800" fill="#ff0000"/>'
                           '</svg>', encoding="utf-8")
            output = tmp / "out.png"
            script = VENDOR / "pixel-studio-painter/scripts/studio.py"
            p = subprocess.run([sys.executable, str(script), "--code", str(svg),
                                "--render", str(output), "--scale", "0.1"],
                               text=True, capture_output=True, timeout=120)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertTrue(output.is_file())
            with Image.open(output) as im:
                r, g, b = im.convert("RGB").getpixel((im.width // 2, im.height // 2))
            self.assertGreater(r, 150)
            self.assertLess(g, 80)
            self.assertLess(b, 80)

    @unittest.skipUnless(HAS_NUMPY and HAS_PIL, "numpy/Pillow optional in generic CI; exercised in Black Dragon checks")
    def test_pixel_studio_never_silently_renders_default_for_python_code(self):
        with tempfile.TemporaryDirectory() as temp:
            tmp = Path(temp)
            source = tmp / "untrusted.py"
            source.write_text("print('SHOULD NOT RUN')\n", encoding="utf-8")
            output = tmp / "out.png"
            script = VENDOR / "pixel-studio-painter/scripts/studio.py"
            p = subprocess.run([sys.executable, str(script), "--code", str(source),
                                "--render", str(output), "--scale", "0.1"],
                               text=True, capture_output=True, timeout=30)
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(output.exists())
            self.assertIn("SVG/scene JSON only", p.stderr)

    @unittest.skipUnless(HAS_NUMPY and HAS_PIL and HAS_CV2, "OpenCV/numpy/Pillow optional in generic CI")
    def test_camera_translation_does_not_look_like_a_new_shot(self):
        import numpy as np
        mimic = VENDOR / "kosif-mimic/scripts"
        sys.path.insert(0, str(mimic))
        import mm_analyze
        rng = np.random.default_rng(42)
        base = rng.integers(0, 256, (96, 144, 3), dtype=np.uint8)
        moved = np.roll(base, 5, axis=1)
        other = rng.integers(0, 256, (96, 144, 3), dtype=np.uint8)
        feats = {"small": np.stack([base, moved, other])}
        camera = mm_analyze.translation_residual(feats, 0, 1)
        new_scene = mm_analyze.translation_residual(feats, 0, 2)
        self.assertLess(camera, 2.0)
        self.assertGreater(new_scene, 30.0)

    @unittest.skipUnless(HAS_NUMPY, "numpy optional in generic CI; exercised in Black Dragon checks")
    def test_beat_estimator_does_not_invent_tempo_from_irregular_transients(self):
        import numpy as np
        path = VENDOR / "pro-video-editor-ffmpeg/scripts/beat_cuts.py"
        spec = importlib.util.spec_from_file_location("beat_cuts_under_test", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertAlmostEqual(mod.estimate_bpm(np.arange(0, 6, 0.5)), 120.0, delta=1.0)
        rng = np.random.default_rng(7)
        irregular = np.r_[0.0, np.cumsum(rng.uniform(0.31, 1.15, 32))]
        self.assertIsNone(mod.estimate_bpm(irregular))


if __name__ == "__main__":
    unittest.main()
