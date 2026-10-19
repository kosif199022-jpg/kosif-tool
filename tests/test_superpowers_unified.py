"""Regression tests for the MIT-licensed Superpowers process integration."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SRC = (Path(__file__).resolve().parents[1] / ".claude" / "skills" /
       "kosif-superpowers" / "scripts" / "superpowers_unified.py")
spec = importlib.util.spec_from_file_location("kosif_superpowers_unified", SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class UnificationTests(unittest.TestCase):
    def test_vendor_inventory_and_license(self):
        self.assertEqual(m.verify_source(), [])
        self.assertEqual(len(m.SKILLS), 15)
        self.assertIn("MIT License", m.SOURCE_LICENSE.read_text(encoding="utf-8"))

    def test_debugging_pipeline(self):
        p = m.plan("Fix the crash and investigate the bug in the app")
        self.assertEqual(p["master"], "kosif-superpowers")
        self.assertIn("systematic-debugging", p["process_skills"])
        self.assertIn("test-driven-development", p["process_skills"])
        self.assertEqual(p["process_skills"][-1], "verification-before-completion")

    def test_creative_video_pipeline(self):
        p = m.plan("Design a cinematic montage with original audio and stock video")
        self.assertIn("brainstorming", p["process_skills"])
        self.assertIn("writing-plans", p["process_skills"])
        self.assertNotIn("systematic-debugging", p["process_skills"])

    def test_arabic_planning(self):
        p = m.plan("اعمل خطة لتطوير برنامج المونتاج")
        self.assertIn("writing-plans", p["process_skills"])
        self.assertIn("test-driven-development", p["process_skills"])

    def test_install_and_existing_content_preservation(self):
        with tempfile.TemporaryDirectory() as t:
            home = Path(t)
            claude = home / ".claude"
            claude.mkdir()
            (claude / "CLAUDE.md").write_text("# My personal settings\n", encoding="utf-8")
            target = claude / "skills" / "my-private-skill"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("do not touch", encoding="utf-8")
            result = m.install(home)
            self.assertEqual(result["verified"]["installed_process_count"], 15)
            self.assertTrue(result["verified"]["installed_kosif"])
            self.assertEqual((target / "SKILL.md").read_text(), "do not touch")
            instructions = (claude / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertTrue(instructions.startswith("# My personal settings"))
            self.assertEqual(instructions.count(m.GLOBAL_START), 1)
            again = m.install(home)
            self.assertEqual(again["instructions"], "already_present")
            self.assertEqual((claude / "CLAUDE.md").read_text(encoding="utf-8").count(m.GLOBAL_START), 1)

    def test_portable_package_excludes_nested_skills(self):
        package_path = SRC.with_name("package_skill.py")
        pkg_spec = importlib.util.spec_from_file_location("kosif_package_skill", package_path)
        package = importlib.util.module_from_spec(pkg_spec)
        pkg_spec.loader.exec_module(package)
        files, _ = package.collect(lite=True, with_evals=True)
        self.assertTrue(any(str(f).replace("\\\\", "/") == "SKILL.md" for f in files))
        self.assertFalse(any(f.parts[0] == "vendor" for f in files))

    def test_collision_requires_force(self):
        with tempfile.TemporaryDirectory() as t:
            home = Path(t)
            bad = home / ".claude" / "skills" / "brainstorming"
            bad.mkdir(parents=True)
            (bad / "SKILL.md").write_text("private version", encoding="utf-8")
            result = m.install(home, global_instructions=False)
            statuses = {x["skill"]: x["result"] for x in result["results"]}
            self.assertEqual(statuses["brainstorming"], "skipped_existing_use_force")
            self.assertEqual((bad / "SKILL.md").read_text(), "private version")
            self.assertFalse((home / ".claude" / "CLAUDE.md").exists())

if __name__ == "__main__":
    unittest.main()
