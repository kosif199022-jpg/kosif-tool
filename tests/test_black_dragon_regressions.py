"""Regressions for the five Black Dragon findings from the Nov 3 technical report.

Runs locally in the existing Black Dragon CI; no network, purchases or API keys.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills"


def load_script(name: str, path: Path):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ModelAuditRegression(unittest.TestCase):
    def test_bare_zero_formula_is_reported_as_high_severity(self):
        from openpyxl import Workbook

        with tempfile.TemporaryDirectory() as d:
            xlsx = Path(d) / "model.xlsx"
            wb = Workbook()
            wb.active.title = "Assumptions"
            forecast = wb.create_sheet("Forecast")
            forecast["D4"] = "=0"
            forecast["D5"] = "=A1+B1"  # ordinary references must not be flagged
            wb.create_sheet("Checks")
            wb.save(xlsx)

            script = VENDOR / "excel-model-architect/scripts/model_audit.py"
            result = subprocess.run([sys.executable, str(script), str(xlsx), "--json"],
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["verdict"], "REVISE")
            self.assertEqual(report["stats"]["hardcoded"], 1, report)
            self.assertTrue(any(
                item["cell"] == "Forecast!D4" and item["sev"] == "HIGH"
                for item in report["findings"]
            ), report)


class PixelStudioRegression(unittest.TestCase):
    def test_headless_render_uses_code_file_not_default_scene(self):
        from PIL import Image

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "red.svg"
            dest = root / "actual.png"
            source.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">'
                '<rect x="0" y="0" width="1200" height="800" fill="#ff0000"/>'
                '</svg>', encoding="utf-8")
            script = VENDOR / "pixel-studio-painter/scripts/studio.py"
            done = subprocess.run([sys.executable, str(script), "--code", str(source),
                                   "--render", str(dest), "--scale", "0.2"],
                                  capture_output=True, text=True, timeout=150)
            self.assertEqual(done.returncode, 0, done.stderr[-1500:])
            self.assertTrue(dest.is_file())
            with Image.open(dest) as picture:
                r, g, b = picture.convert("RGB").getpixel(
                    (picture.width // 2, picture.height // 2))
                self.assertGreater(r, 210)
                self.assertLess(g, 60)
                self.assertLess(b, 60)

    def test_missing_code_fails_without_rendering_a_default_scene(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            dest = root / "should-not-exist.png"
            script = VENDOR / "pixel-studio-painter/scripts/studio.py"
            done = subprocess.run([sys.executable, str(script), "--code", str(root / "missing.svg"),
                                   "--render", str(dest)], capture_output=True, text=True, timeout=45)
            self.assertNotEqual(done.returncode, 0)
            self.assertFalse(dest.exists())


class MimicRegression(unittest.TestCase):
    def test_shaky_camera_low_confidence_is_not_counted_as_edit(self):
        analyzer = load_script("dragon_mimic_analysis", VENDOR / "kosif-mimic/scripts/mm_analyze.py")
        self.assertFalse(analyzer.accept_transition({"type": "wipeleft", "confidence": 0.05}))
        self.assertFalse(analyzer.accept_transition({"type": "fade", "confidence": None}))
        self.assertTrue(analyzer.accept_transition({"type": "cut", "confidence": 0.8}))


class BeatCutsRegression(unittest.TestCase):
    def test_periodic_clicks_have_stable_bpm(self):
        import numpy as np
        beat = load_script("dragon_beat_cuts", VENDOR / "pro-video-editor-ffmpeg/scripts/beat_cuts.py")
        times = np.arange(0.1, 7.0, 0.5)
        self.assertGreaterEqual(beat.tempo_consistency(times), 0.95)
        self.assertAlmostEqual(beat.estimate_bpm(times), 120.0, delta=3.0)

    def test_irregular_impacts_do_not_invent_bpm(self):
        import numpy as np
        beat = load_script("dragon_beat_cuts_irregular", VENDOR / "pro-video-editor-ffmpeg/scripts/beat_cuts.py")
        irregular = np.array([0.1, 0.46, 1.19, 1.77, 2.81, 3.17, 4.1, 5.55])
        self.assertLess(beat.tempo_consistency(irregular), 0.70)
        self.assertIsNone(beat.estimate_bpm(irregular))


if __name__ == "__main__":
    unittest.main()
