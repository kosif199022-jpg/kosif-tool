"""No-network/no-clone smoke tests for the Claude skill fallback."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import local_first as local


class OfflineFallback(unittest.TestCase):
    def test_bundled_skill_doctor(self):
        paths = local.discover(SK)
        report = local.doctor(paths)
        self.assertTrue(report["local_only"])
        self.assertFalse(report["network"])
        self.assertGreater(report["power_records"], 4500)
        self.assertEqual(report["power_records"], sum(report["status_counts"].values()))

    def test_standalone_skill_never_requires_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "kosif-superpowers"
            (dest / "scripts").mkdir(parents=True)
            shutil.copy(SK / "SKILL.md", dest / "SKILL.md")
            shutil.copy(SK / "scripts" / "powers.py", dest / "scripts" / "powers.py")
            paths = local.discover(dest)
            self.assertIsNone(paths["styles"])
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = local.main(["--skill-dir", str(dest), "search", "silhouette",
                                   "--scope", "styles"])
            self.assertEqual(code, 2)
            self.assertIn("authorized existing repo checkout", out.getvalue())

    def test_no_shell_injection_or_external_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "kosif-superpowers"
            (dest / "scripts").mkdir(parents=True)
            shutil.copy(SK / "SKILL.md", dest / "SKILL.md")
            shutil.copy(SK / "scripts" / "powers.py", dest / "scripts" / "powers.py")
            paths = local.discover(dest)
            self.assertIsNone(paths["styles"])
            # Code never shells out, and user arguments are single argv strings.
            text = (SK / "scripts" / "local_first.py").read_text(encoding="utf-8-sig")
            self.assertIn("shell=False", text)
            self.assertNotIn("git clone", text)
            self.assertNotIn("shell=True", text)

    def test_catalog_is_not_mislabeled_as_verified(self):
        data = local.doctor(local.discover(SK))
        self.assertTrue(data["catalog_records_are_not_executed_capabilities"])
        self.assertIn("proven", data["status_counts"])

    def test_local_missing_skill_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                local.discover(Path(tmp))


if __name__ == "__main__":
    unittest.main()
