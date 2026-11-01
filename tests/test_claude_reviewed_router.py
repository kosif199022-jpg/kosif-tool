"""Focused reviewed-tool routing and execution: safety, scope and receipts."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
sys.path.insert(0, str(SCRIPTS))
import black_dragon as dragon
import _claude_reviewed_router as router
import _claude_tool_bridge as bridge


class ReviewedToolRouterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.scripts = self.root / "scripts"
        self.scripts.mkdir()
        (self.scripts / "ok.py").write_text(
            "import pathlib,sys\npathlib.Path(sys.argv[1]).write_text('real reviewed evidence')\n",
            encoding="utf-8")
        (self.scripts / "fail.py").write_text("import sys\nsys.exit(3)\n", encoding="utf-8")
        self.source = self.root / "adapters.json"
        self.source.write_text('{"adapters":{}}')
        self.catalog = {
            "tool:finance": {"kind": "tool", "source": "finance.py"},
            "tool:verify": {"kind": "tool", "source": "verify.py"},
            "power:no-exec": {"kind": "power", "source": "powers.json"},
        }
        self.adapters = {
            "tool:finance": {"script": "scripts/ok.py", "args": ["{artifact}", "{task}"],
                             "why": "finance report analysis tax accounting"},
            "tool:verify": {"script": "scripts/ok.py", "args": ["{artifact}"],
                            "depends_on": ["tool:finance"], "why": "quality verification"},
        }
        self.patches = [
            patch.object(router, "REPO", self.root),
            patch.object(dragon, "REPO", self.root),
            patch.object(dragon, "REVIEWED_ADAPTERS", self.source),
            patch.object(router, "_inventory", return_value=self.catalog),
            patch.object(router, "_registry", return_value=self.adapters),
            patch.object(router, "_records", return_value={"tool:finance": {
                "title_en": "finance review", "keywords": ["financial", "accounting"]}}),
        ]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def test_route_returns_only_matching_reviewed_and_no_execution_claim(self):
        result = router.route("finance report", 4)
        self.assertEqual(result["catalog_total"], 3)
        self.assertEqual(result["reviewed_adapter_total"], 2)
        self.assertEqual(result["candidates"][0]["id"], "tool:finance")
        self.assertFalse(result["candidates"][0]["runtime_verified"])
        self.assertNotIn("power:no-exec", [r["id"] for r in result["candidates"]])

    def test_empty_query_and_bad_limit_rejected(self):
        with self.assertRaises(ValueError):
            router.route("")
        with self.assertRaises(ValueError):
            router.route("finance", True)

    def test_unreviewed_tool_cannot_execute(self):
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            router._select(["power:no-exec"], self.catalog, self.adapters)

    def test_duplicate_tool_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "distinct"):
            router._select(["tool:finance", "tool:finance"], self.catalog, self.adapters)

    def test_dependencies_must_be_explicit(self):
        with self.assertRaisesRegex(ValueError, "Explicit prerequisite"):
            router._select(["tool:verify"], self.catalog, self.adapters)

    def test_consent_required_even_if_env_enabled(self):
        with patch.dict(os.environ, {"KOSIF_ALLOW_ADAPTER_EXECUTION": "1"}):
            with self.assertRaises(PermissionError):
                router.execute("finance", ["tool:finance"], "noapproval", permission=False)
        self.assertFalse((self.root / "out" / "claude-reviewed-tools" / "noapproval").exists())

    def test_environment_gate_cannot_be_bypassed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(PermissionError):
                router.execute("finance", ["tool:finance"], "noenv", permission=True)

    def test_explicit_tool_success_receipt_and_scope(self):
        with patch.dict(os.environ, {"KOSIF_ALLOW_ADAPTER_EXECUTION": "1"}):
            response = router.execute("finance report", ["tool:finance", "tool:verify"],
                                      "good-job", permission=True, workers=2)
        self.assertEqual(response["scope"], "selected-reviewed-only")
        self.assertEqual(response["review"]["verified_executed"], 2)
        self.assertTrue(response["review"]["selected_subset_fully_executed"])
        self.assertFalse(response["review"]["entire_catalog_executed"])
        self.assertTrue(router.review("good-job")["passed"])
        with self.assertRaises(FileExistsError):
            with patch.dict(os.environ, {"KOSIF_ALLOW_ADAPTER_EXECUTION": "1"}):
                router.execute("finance", ["tool:finance"], "good-job", permission=True)

    def test_review_detects_tampered_artifact(self):
        with patch.dict(os.environ, {"KOSIF_ALLOW_ADAPTER_EXECUTION": "1"}):
            router.execute("finance", ["tool:finance"], "tamper", permission=True)
        job = self.root / "out" / "claude-reviewed-tools" / "tamper"
        next((job / "artifacts").iterdir()).write_text("changed")
        result = router.review("tamper")
        self.assertFalse(result["passed"])
        self.assertIn("integrity mismatch", " ".join(result["issues"]))

    def test_failure_blocks_dependent(self):
        self.adapters["tool:finance"] = {"script": "scripts/fail.py", "args": ["{artifact}"]}
        with patch.dict(os.environ, {"KOSIF_ALLOW_ADAPTER_EXECUTION": "1"}):
            result = router.execute("finance", ["tool:finance", "tool:verify"],
                                    "failure", permission=True)
        self.assertEqual(result["review"]["failed"], 1)
        self.assertEqual(result["review"]["blocked"], 1)

    def test_bridge_has_focused_mcp_actions_with_strict_server_approval(self):
        listed = {x["name"] for x in bridge.TOOLS}
        self.assertTrue({"kosif_route_reviewed", "kosif_execute_reviewed",
                         "kosif_review_execution"}.issubset(listed))
        with self.assertRaisesRegex(PermissionError, "server"):
            bridge.call_tool("kosif_execute_reviewed", {
                "task": "finance", "ids": ["tool:finance"],
                "job_name": "blocked", "allow_execution": True,
                "approval_digest": "0" * 64}, False)
        with self.assertRaises(PermissionError):
            bridge.call_tool("kosif_execute_reviewed", {
                "task": "finance", "ids": ["tool:finance"],
                "job_name": "blocked", "allow_execution": False,
                "approval_digest": "0" * 64}, True)

    def test_preview_is_read_only_and_deterministic(self):
        before = self.root / "out" / "claude-reviewed-tools"
        a = router.preview("finance report", ["tool:verify", "tool:finance"])
        b = router.preview("finance report", ["tool:finance", "tool:verify"])
        self.assertEqual(a["approval_digest"], b["approval_digest"])
        self.assertEqual(len(a["approval_digest"]), 64)
        self.assertEqual(a["waves"], [["tool:finance"], ["tool:verify"]])
        self.assertEqual(a["selected"], ["tool:finance", "tool:verify"])
        self.assertFalse(a["execution_performed"])
        self.assertFalse(before.exists())

    def test_preview_changes_on_task_tool_content_or_runtime(self):
        first = router.preview("finance", ["tool:finance"])
        self.assertNotEqual(first["approval_digest"],
                            router.preview("tax", ["tool:finance"])["approval_digest"])
        self.assertNotEqual(first["approval_digest"],
                            router.preview("finance", ["tool:finance"], timeout=61)["approval_digest"])
        self.assertNotEqual(first["approval_digest"],
                            router.preview("finance", ["tool:finance", "tool:verify"])["approval_digest"])
        (self.scripts / "ok.py").write_text("print('new version')\n")
        self.assertNotEqual(first["approval_digest"],
                            router.preview("finance", ["tool:finance"])["approval_digest"])

    def test_execution_rejects_changed_approval_plan_before_job(self):
        digest = router.preview("finance", ["tool:finance"])["approval_digest"]
        target = self.root / "out" / "claude-reviewed-tools" / "stale"
        with patch.dict(os.environ, {"KOSIF_ALLOW_ADAPTER_EXECUTION": "1"}):
            with self.assertRaisesRegex(PermissionError, "Approval plan changed"):
                router.execute("modified finance", ["tool:finance"], "stale",
                               permission=True, approval_digest=digest)
        self.assertFalse(target.exists())

    def test_execution_with_matching_preview_evidence(self):
        plan = router.preview("finance report", ["tool:finance"])
        with patch.dict(os.environ, {"KOSIF_ALLOW_ADAPTER_EXECUTION": "1"}):
            completed = router.execute("finance report", ["tool:finance"],
                                       "approved", permission=True,
                                       approval_digest=plan["approval_digest"])
        self.assertTrue(completed["review"]["selected_subset_fully_executed"])
        data = json.loads((self.root / "out" / "claude-reviewed-tools" /
                           "approved" / "reviewed_execution.json").read_text())
        self.assertEqual(data["approval_digest"], plan["approval_digest"])

    def test_preview_rejects_unreviewed_prerequisites_and_bad_runtime(self):
        with self.assertRaisesRegex(ValueError, "Explicit prerequisite"):
            router.preview("finance", ["tool:verify"])
        with self.assertRaisesRegex(ValueError, "workers must"):
            router.preview("finance", ["tool:finance"], workers=True)

    def test_review_rejects_forged_empty_selection(self):
        job = self.root / "out" / "claude-reviewed-tools" / "empty"
        job.mkdir(parents=True)
        (job / "reviewed_execution.json").write_text(json.dumps({
            "schema": router.SCHEMA, "scope": "selected-reviewed-only",
            "selected": [], "entries": {},
        }))
        with self.assertRaisesRegex(ValueError, "Invalid selected IDs"):
            router.review("empty")

    def test_mcp_preview_and_matching_digest_enforcement(self):
        params = {"task": "finance", "ids": ["tool:finance"]}
        p = bridge.call_tool("kosif_preview_reviewed", params)
        self.assertEqual(p["approval_digest"], router.preview(**params)["approval_digest"])
        with patch.dict(os.environ, {"KOSIF_ALLOW_ADAPTER_EXECUTION": "1"}):
            with self.assertRaisesRegex(ValueError, "Invalid tool arguments"):
                bridge.call_tool("kosif_execute_reviewed", {
                    **params, "job_name": "needs-preview", "allow_execution": True}, True)
            result = bridge.call_tool("kosif_execute_reviewed", {
                **params, "job_name": "mcp-approved", "allow_execution": True,
                "approval_digest": p["approval_digest"]}, True)
        self.assertEqual(result["review"]["verified_executed"], 1)

    def test_unsafe_job_name_rejected(self):
        with self.assertRaisesRegex(ValueError, "job_name"):
            router.review("../../evil")
        with self.assertRaisesRegex(ValueError, "job_name"):
            router.review("bad/name")


if __name__ == "__main__":
    unittest.main()
