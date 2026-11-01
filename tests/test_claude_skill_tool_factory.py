"""No-execution factory unit tests: skill scanning, proposals, ZIP and MCP registration."""
import hashlib
import json
import os
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
sys.path.insert(0, str(SCRIPTS))
import black_dragon as dragon
import _claude_skill_tool_factory as factory
import _claude_tool_bridge as bridge


class SkillToolFactoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.skills = self.repo / ".claude" / "skills"
        self.skill = self.skills / "sample"
        self.skill.mkdir(parents=True)
        (self.skill / "scripts").mkdir()
        (self.skill / "references").mkdir()
        self.md = self.skill / "SKILL.md"
        self.md.write_text(
            "---\nname: sample\ndescription: Test tool factory\n---\n\n"
            "# Sample\n[good](references/readme.md) [missing](references/nope.md)\n",
            encoding="utf-8")
        (self.skill / "references" / "readme.md").write_text("Authorized reference.")
        (self.skill / "scripts" / "build.py").write_text(
            "import argparse\n"
            "def main():\n"
            "  p = argparse.ArgumentParser()\n"
            "  p.add_argument('--output')\n"
            "  p.parse_args()\n"
            "if __name__ == '__main__':\n"
            "  main()\n",
            encoding="utf-8")
        (self.skill / "scripts" / "library.py").write_text("def x():\n  return 42\n", encoding="utf-8")
        (self.repo / "out").mkdir()
        self.patches = [patch.object(factory, "REPO", self.repo),
                        patch.object(factory, "SKILLS", self.skills),
                        patch.object(dragon, "REPO", self.repo)]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def test_inspection_proves_discovery_not_execution(self):
        result = factory.inspect("sample")
        self.assertEqual(result["candidate_count"], 1)
        self.assertFalse(result["tool_ready"])
        self.assertEqual(result["status"], "static-inspection-only")
        c = result["cli_candidates"][0]
        self.assertEqual(c["script"], "scripts/build.py")
        self.assertEqual(len(c["sha256"]), 64)
        self.assertFalse(c["executable"])
        self.assertIn("references/nope.md", result["missing_local_links"])
        self.assertIn("sample", result["source"])
        self.assertEqual(result["metadata"]["name"], "sample")

    def test_invalid_name_and_script_limit(self):
        for name in ("../sample", "bad/name", "", ".hidden"):
            with self.assertRaises(ValueError):
                factory.inspect(name)
        for val in (0, 601, True):
            with self.assertRaises(ValueError):
                factory.inspect("sample", val)

    def test_untrusted_script_is_never_imported_or_executed(self):
        target = self.skill / "scripts" / "evil.py"
        marker = self.repo / "EXECUTED"
        target.write_text(
            "import argparse\nfrom pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('bad')\n"
            "if __name__ == '__main__':\n"
            "  argparse.ArgumentParser().parse_args()\n",
            encoding="utf-8")
        scanned = factory.inspect("sample")
        self.assertEqual(scanned["candidate_count"], 2)
        self.assertFalse(marker.exists())

    def test_draft_is_non_executable_and_no_overwrite(self):
        out = self.repo / "out" / "skill-tool-proposals" / "sample.json"
        data = factory.draft("sample", out)
        self.assertEqual(data["candidate_count"], 1)
        self.assertFalse(data["executable"])
        spec = json.loads(out.read_text(encoding="utf-8"))
        self.assertFalse(spec["register_automatically"])
        self.assertIsNone(spec["draft_adapters"][0]["args"])
        self.assertEqual(spec["status"], "PENDING_HUMAN_REVIEW_NOT_EXECUTABLE")
        with self.assertRaises(FileExistsError):
            factory.draft("sample", out)
        with self.assertRaisesRegex(ValueError, "under out"):
            factory.draft("sample", self.repo / "bad.json")

    def test_suspicious_imports_flagged_without_executing(self):
        path = self.skill / "scripts" / "build.py"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "import argparse\n", "import argparse, requests, subprocess\n"), encoding="utf-8")
        report = factory.inspect("sample")
        self.assertEqual(report["cli_candidates"][0]["review_flags"],
                         ["requests", "subprocess"])

    def test_zip_verifier_checks_exported_files_and_manifest(self):
        archive = self.repo / "out" / "sample.zip"
        bridge.export_skill("sample", archive)
        result = factory.verify_zip(archive)
        self.assertTrue(result["verified"], result["errors"])
        self.assertGreater(result["files"], 2)
        self.assertEqual(len(result["zip_sha256"]), 64)

    def test_zip_verifier_detects_manifest_hash_tamper(self):
        archive = self.repo / "out" / "tampered.zip"
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("SKILL.md", "evil content")
            z.writestr("KOSIF_EXPORT_MANIFEST.json", json.dumps({
                "files": {"SKILL.md": hashlib.sha256(b"original").hexdigest()}}))
        result = factory.verify_zip(archive)
        self.assertFalse(result["verified"])
        self.assertIn("SHA-256 mismatch", " ".join(result["errors"]))

    def test_zip_verifier_rejects_unsafe_archive_paths_and_duplicates(self):
        archive = self.repo / "out" / "unsafe.zip"
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("../SKILL.md", "bad")
            z.writestr("SKILL.md", "normal")
            z.writestr("KOSIF_EXPORT_MANIFEST.json", '{"files":{}}')
        self.assertFalse(factory.verify_zip(archive)["verified"])
        with self.assertRaisesRegex(ValueError, "under repository out"):
            factory.verify_zip(self.repo / "not-in-out.zip")

    def test_zip_verifier_does_not_extract_or_execute_python(self):
        archive = self.repo / "out" / "safe.zip"
        marker = self.repo / "executed"
        content = "from pathlib import Path\nPath("+repr(str(marker))+").write_text('bad')"
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("SKILL.md", "Hello")
            z.writestr("scripts/run.py", content)
            z.writestr("KOSIF_EXPORT_MANIFEST.json", json.dumps({
                "files": {"SKILL.md": hashlib.sha256(b"Hello").hexdigest(),
                          "scripts/run.py": hashlib.sha256(content.encode()).hexdigest()}}))
        self.assertTrue(factory.verify_zip(archive)["verified"])
        self.assertFalse(marker.exists())

    def test_factory_mcp_tools_registered_and_read_only(self):
        names = {x["name"] for x in bridge.TOOLS}
        self.assertTrue({"kosif_toolify_skill", "kosif_verify_skill_package",
                         "kosif_bridge_doctor"}.issubset(names))
        result = bridge.call_tool("kosif_toolify_skill", {"name": "sample"})
        self.assertFalse(result["tool_ready"])
        packages = self.repo / "out" / "test.zip"
        bridge.export_skill("sample", packages)
        self.assertTrue(bridge.call_tool("kosif_verify_skill_package", {
            "path": str(packages)})["verified"])
        self.assertEqual(bridge.TOOLS[0]["name"], "kosif_search")

    def test_bridge_doctor_checks_registered_adapter_contract(self):
        path = self.repo / "scripts" / "adapter.py"
        path.parent.mkdir()
        path.write_text("import sys\n", encoding="utf-8")
        catalog = {"tool:a": {"kind": "tool", "source": "a"}}
        with patch.object(factory.dragon, "full_inventory", return_value=catalog), \
             patch.object(factory.dragon, "_load_adapters", return_value={
                 "tool:a": {"script": "scripts/adapter.py", "args": ["{task}"]}}):
            result = factory.doctor()
        self.assertFalse(result["passed"])
        self.assertIn("missing artifact", " ".join(result["issues"]))
        self.assertEqual(result["executions_performed"], 0)


if __name__ == "__main__":
    unittest.main()
