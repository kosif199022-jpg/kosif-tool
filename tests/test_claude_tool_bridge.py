"""Integration checks for MCP skill-tool bridge and Black Dragon Pro Max."""
import json
import os
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
import _black_dragon_pro_max as pro_max
import _claude_tool_bridge as bridge


class BridgeTests(unittest.TestCase):
    def test_mcp_initialize_list_and_missing_method(self):
        req = lambda method, params=None: {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
        init = bridge.respond(req("initialize", {"protocolVersion": "2025-11-25"}))
        self.assertEqual(init["result"]["serverInfo"]["name"], "kosif-superpowers-bridge")
        names = {x["name"] for x in bridge.respond(req("tools/list"))["result"]["tools"]}
        self.assertEqual(names, {"kosif_search", "kosif_describe", "kosif_plan_pro_max", "kosif_run_pro_max",
                                 "kosif_route_reviewed", "kosif_execute_reviewed", "kosif_review_execution",
                                 "kosif_toolify_skill", "kosif_verify_skill_package", "kosif_bridge_doctor"})
        self.assertEqual(bridge.respond(req("unknown"))["error"]["code"], -32601)
        self.assertIsNone(bridge.respond({"jsonrpc": "2.0", "method": "notifications/initialized"}))

    def test_unknown_and_unapproved_execution_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown MCP tool"):
            bridge.call_tool("bad", {})
        with self.assertRaisesRegex(ValueError, "Invalid tool arguments"):
            bridge.call_tool("kosif_search", {"query": "hi", "extra": "bad"})
        with self.assertRaisesRegex(PermissionError, "read-only"):
            bridge.call_tool("kosif_run_pro_max",
                             {"task": "test", "job_name": "test", "allow_execution": True})
        with self.assertRaisesRegex(PermissionError, "KOSIF_ALLOW_ADAPTER_EXECUTION"):
            with patch.dict(os.environ, {}, clear=True):
                bridge.run_pro_max("test", "a-safe-name", allow_execution=True)

    def test_search_rank_does_not_claim_execution(self):
        fake = {"skill:finance": {"kind": "skill", "source": "finance/SKILL.md"},
                "power:VIDEO": {"kind": "power", "source": "data/powers/a.json"}}
        with patch.object(bridge, "inventory", return_value=fake), \
             patch.object(bridge.brain, "metadata", return_value={
                 "skill:finance": "financial reporting accountant",
                 "power:VIDEO": "video montage"}):
            result = bridge.search("finance")
            self.assertEqual(result["results"][0]["id"], "skill:finance")
            self.assertEqual(result["total_catalogued"], 2)
            self.assertIn("not necessarily executable", result["meaning"])

    def test_export_is_complete_and_reproducible_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / ".claude" / "skills" / "sample"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: sample\n---\n# Sample\n")
            (skill / "templates").mkdir()
            (skill / "templates" / "template.json").write_text('{"x": 1}')
            target = root / "out" / "sample.zip"
            with patch.object(bridge, "SKILLS", skill.parent), patch.object(bridge, "REPO", root):
                result = bridge.export_skill("sample", target)
                self.assertEqual(result["files"], 2)
                with zipfile.ZipFile(target) as z:
                    self.assertIn("SKILL.md", z.namelist())
                    self.assertIn("templates/template.json", z.namelist())
                    manifest = json.loads(z.read("KOSIF_EXPORT_MANIFEST.json"))
                    self.assertEqual(set(manifest["files"]), {"SKILL.md", "templates/template.json"})
                with self.assertRaises(FileExistsError):
                    bridge.export_skill("sample", target)

    def test_export_refuses_unsafe_path_and_partial_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / ".claude" / "skills" / "sample"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("A" * (2 * 1024 * 1024))
            with patch.object(bridge, "SKILLS", skill.parent), patch.object(bridge, "REPO", root):
                with self.assertRaisesRegex(ValueError, "exceeds max_mb"):
                    bridge.export_skill("sample", root / "out" / "small.zip", max_mb=1)
                self.assertFalse((root / "out" / "small.zip").exists())
                with self.assertRaisesRegex(ValueError, "inside repository out"):
                    bridge.export_skill("sample", root / "outside.zip")


class ProMaxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        old = dragon.REPO
        dragon.REPO = self.root
        self.addCleanup(setattr, dragon, "REPO", old)
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "adapter.py").write_text(
            "import pathlib,sys\npathlib.Path(sys.argv[1]).write_text('verified')\n")
        self.entries = {"tool:one": {"kind": "tool", "source": "tools.json"},
                        "skill:two": {"kind": "skill", "source": "two/SKILL.md"}}
        self.job = self.root / "out" / "test"

    def test_all_entries_assigned_pro_max_without_faking_exec(self):
        report = dragon.run("deep thinking", self.job, {}, 2, False, 5,
                            entries=self.entries, mode="pro-max")
        self.assertEqual(report["mode"], "pro-max")
        self.assertFalse(report["pro_max"]["every_capability_executed"])
        self.assertTrue(report["pro_max"]["integrity_passed"])
        self.assertFalse(report["pro_max"]["external_full_pro_verified"])
        gate = json.loads((self.job / "black_dragon_pro_max_qa.json").read_text())
        self.assertEqual(gate["assigned"], 2)
        self.assertEqual(gate["blocked"], 2)

    def test_verified_full_coverage_and_tampering_detected(self):
        adapters = {key: {"script": "scripts/adapter.py", "args": ["{artifact}"]}
                    for key in self.entries}
        report = dragon.run("run", self.job, adapters, 2, True, 5,
                            entries=self.entries, mode="pro-max")
        self.assertTrue(report["pro_max"]["every_capability_executed"])
        self.assertEqual(report["executed"], 2)
        artifacts = sorted((self.job / "artifacts").glob("*"))
        self.assertEqual(len(artifacts), 2)
        artifacts[0].write_text("TAMPERED")
        qa = pro_max.verify(self.job, self.entries, report)
        self.assertFalse(qa["integrity_passed"])
        self.assertIn("artifact/digest mismatch", " ".join(qa["issues"]))


if __name__ == "__main__":
    unittest.main()
