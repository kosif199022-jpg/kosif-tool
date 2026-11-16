"""Offline regression tests: no pip/npm installs, renders, network or user data."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reel12", ROOT / "toolchain.py")
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class ToolchainTests(unittest.TestCase):
    def test_registry_has_exact_twelve_unique_tools(self):
        names = list(tool.TOOLS)
        self.assertEqual(len(names), 12)
        self.assertEqual(len(set(names)), 12)
        self.assertEqual(set(names), {
            "remotion", "hyperframes", "motion-canvas", "threejs", "manim",
            "roughjs", "gsap", "animejs", "mojs", "whisperx", "auto-editor", "ffmpeg",
        })

    def test_plan_provides_real_protocol_and_no_execution_claim(self):
        p = tool.plan("فيديو 3D مع تعليق صوتي وصمت وموشن مرسوم يدوي")
        self.assertEqual(p["execution_status"], "planning_only")
        self.assertEqual(len(p["stages"]), 7)
        self.assertTrue({"threejs", "whisperx", "auto-editor", "motion-canvas",
                         "roughjs", "ffmpeg"}.issubset(set(p["recommended"])))

    def test_doctor_reconciles_all_registry_items(self):
        d = tool.doctor()
        self.assertEqual(d["total_count"], 12)
        self.assertEqual(len(d["tools"]), 12)
        self.assertEqual(d["available_count"], sum(t["available"] for t in d["tools"]))
        self.assertTrue(d["dependency_resolution_only"])

    def test_install_needs_scope_and_does_not_mutate(self):
        class Args:
            all = False
            node = False
            python = False
            dry_run = True
            yes = False
        self.assertEqual(tool.install(Args()), 2)

    def test_refuse_library_without_cli(self):
        self.assertEqual(tool.execute("threejs", ["--help"]), 2)

    def test_manager_packages_are_populated(self):
        for x in tool.TOOLS.values():
            self.assertIn(x["manager"], {"npm", "pip", "system-or-npm"})
            self.assertTrue(x["packages"])
            self.assertTrue(x["url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
