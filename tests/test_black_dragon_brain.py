"""Tests for the cognitive planner: ALL entries remain in the plan and dependencies matter."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
sys.path.insert(0, str(SCRIPTS))
import _black_dragon_brain as brain
import _black_dragon_activation as activation


class CognitivePlannerTests(unittest.TestCase):
    def setUp(self):
        self.catalog = {
            "tool:research": {"source": "research"},
            "skill:animation": {"source": "animation"},
            "power:QA-01": {"source": "qa-verification"},
            "power:THINK-01": {"source": "thinking"},
        }

    def test_all_entries_including_low_relevance_stay_in_plan(self):
        result = brain.plan("اعمل فيديو animation", self.catalog, {})
        self.assertEqual(set(result["items"]), set(self.catalog))
        self.assertEqual(sum(map(len, result["waves"])), len(self.catalog))
        self.assertEqual(result["selected_out"], 0)
        self.assertEqual(result["total"], 4)

    def test_dependency_waves_and_role_ranking(self):
        adapters = {
            "skill:animation": {"depends_on": ["tool:research"]},
            "power:QA-01": {"depends_on": ["skill:animation"]},
        }
        result = brain.plan("animation video", self.catalog, adapters)
        waves = result["waves"]
        self.assertLess(next(i for i, w in enumerate(waves) if "tool:research" in w),
                        next(i for i, w in enumerate(waves) if "skill:animation" in w))
        self.assertLess(next(i for i, w in enumerate(waves) if "skill:animation" in w),
                        next(i for i, w in enumerate(waves) if "power:QA-01" in w))
        self.assertEqual(result["items"]["skill:animation"]["role"], "build")

    def test_cycle_rejected_instead_of_silent_omission(self):
        adapters = {
            "tool:research": {"depends_on": ["skill:animation"]},
            "skill:animation": {"depends_on": ["tool:research"]},
        }
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            brain.plan("all", self.catalog, adapters)

    def test_unknown_and_self_dependencies_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid dependency"):
            brain.plan("all", self.catalog, {"tool:research": {"depends_on": ["power:unknown"]}})
        with self.assertRaisesRegex(ValueError, "Invalid dependency"):
            brain.plan("all", self.catalog, {"tool:research": {"depends_on": ["tool:research"]}})

    def test_metadata_can_change_priority_but_never_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data/powers").mkdir(parents=True)
            (root / "data/powers/sample.json").write_text(json.dumps([
                {"id": "THINK-01", "title": "music rhythm video"}]))
            (root / "data/tools.json").write_text(json.dumps({"tools": [
                {"id": "research", "summary_en": "music rhythm video"}]}))
            result = brain.plan("music rhythm video", self.catalog, {}, root)
            self.assertEqual(result["total"], 4)
            self.assertEqual(result["selected_out"], 0)
            self.assertGreater(result["items"]["tool:research"]["priority"], 0)

    def test_every_item_gets_part_mode_weight_and_application(self):
        result = brain.plan("اعمل مونتاج فيديو وتحقق الجودة", self.catalog, {})
        parts = {p["id"] for p in brain.PARTS}
        for item in result["items"].values():
            self.assertIn(item["part"], parts)
            self.assertIn(item["mode"], brain.MODES)
            self.assertIn(item["weight"], ("lead", "core", "support"))
            self.assertTrue(item["application"])
        self.assertEqual(sum(result["weights"].values()), 4)
        self.assertEqual(result["items"]["power:QA-01"]["mode"], "quality-gate")

    def test_adapter_changes_mode_to_execute_and_kind_sets_mode(self):
        catalog = dict(self.catalog, **{"style:neon": {"kind": "style", "source": "styles"},
                                        "protocol:A1": {"kind": "protocol", "source": "p"}})
        result = brain.plan("any", catalog, {"tool:research": {}})
        self.assertEqual(result["items"]["tool:research"]["mode"], "execute")
        self.assertEqual(result["items"]["style:neon"]["mode"], "visual-reference")
        self.assertEqual(result["items"]["protocol:A1"]["mode"], "protocol-rule")

    def test_assignment_is_deterministic(self):
        a = brain.plan("animation video", self.catalog, {})
        b = brain.plan("animation video", self.catalog, {})
        self.assertEqual(a["assignment_sha256"], b["assignment_sha256"])

    def test_metadata_ignores_non_dict_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(brain.metadata({"a": 1}, Path(tmp)), {})

    def test_arabic_prefixes_are_normalised(self):
        self.assertIn("مونتاج", brain.tokens("والمونتاج"))
        self.assertIn("صوت", brain.tokens("بصوت"))



class ToolInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.skill = self.repo / "skill_root"
        self.skill.mkdir()
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts" / "first.py").write_text(
            "raise RuntimeError('static inspection must not execute')\n", encoding="utf-8")
        (self.repo / "scripts" / "second.py").write_text(
            "raise RuntimeError('never execute imported scripts')\n", encoding="utf-8")
        self.inv = {
            "tool:first": {"kind": "tool", "source": "data/tools.json"},
            "tool:second": {"kind": "tool", "source": "data/tools.json"},
            "skill:kosif-infinite-matrices": {"kind": "skill", "source": "SKILL.md"},
            "protocol:A38": {"kind": "protocol", "source": "PROTOCOL.md"},
        }
        self.records = {
            "tool:first": {"kind": "cli", "root": "repo", "path": "scripts/first.py",
                           "summary_en": "Analyze text and prepare task", "safety": "read-only"},
            "tool:second": {"kind": "cli", "root": "repo", "path": "scripts/second.py",
                            "summary_en": "Generate output", "safety": "read-only"},
        }
        self.adapters = {
            "tool:first": {"script": "scripts/first.py", "args": ["{task}"]},
            "tool:second": {"script": "scripts/second.py", "args": ["{task}"],
                            "depends_on": ["tool:first"]},
        }

    def inspect(self, mode="all"):
        return activation.inspect_and_schedule("analyze output", self.inv, self.adapters,
                                                self.records, self.repo, self.skill,
                                                mode=mode)

    def test_full_coverage_inspection_order_and_no_execution(self):
        result = self.inspect()
        self.assertEqual(result["catalog"]["examined"], len(self.inv))
        self.assertEqual(result["counts"]["catalog_tools"], 2)
        self.assertEqual(result["counts"]["statically_inspected"], 2)
        self.assertEqual(result["counts"]["tool_candidates_after_dependencies"], 2)
        self.assertEqual(result["counts"]["execution_attempts"], 0)
        self.assertFalse(result["approval_gate"]["approved"])
        self.assertEqual(result["status"], "planned_not_executed")
        self.assertEqual(result["tools"]["tool:first"]["inspection"]["status"], "inspected")
        self.assertEqual(len(result["tools"]["tool:first"]["inspection"]["source_sha256"]), 64)
        self.assertEqual(result["catalog"]["assigned"], 4)
        waves = result["dependency_waves"]
        self.assertLess(next(i for i, w in enumerate(waves) if "tool:first" in w),
                        next(i for i, w in enumerate(waves) if "tool:second" in w))
        self.assertEqual(len(result["council"]["members"]), 5)
        self.assertEqual(result["plan_sha256"], self.inspect()["plan_sha256"])

    def test_missing_source_or_metadata_blocks_execution_but_keeps_inventory(self):
        self.records["tool:first"]["path"] = "scripts/missing.py"
        result = self.inspect()
        self.assertEqual(result["counts"]["catalog_tools"], 2)
        self.assertEqual(result["tools"]["tool:first"]["readiness"], "inspection_blocked")
        self.assertEqual(result["tools"]["tool:second"]["readiness"], "dependency_blocked")
        self.assertEqual(result["counts"]["tool_candidates_after_dependencies"], 0)
        self.records.pop("tool:second")
        result = self.inspect()
        self.assertEqual(result["tools"]["tool:second"]["inspection"]["status"],
                         "missing_metadata")

    def test_traversal_and_symlink_are_rejected(self):
        self.records["tool:first"]["path"] = "../secrets.py"
        self.assertEqual(self.inspect()["tools"]["tool:first"]["inspection"]["status"],
                         "unsafe_path")
        self.records["tool:first"]["path"] = "scripts/link.py"
        (self.repo / "scripts/link.py").symlink_to(self.repo / "scripts/first.py")
        self.assertEqual(self.inspect()["tools"]["tool:first"]["inspection"]["status"],
                         "unsafe_path")

    def test_smart_still_inspects_all_tools(self):
        result = self.inspect("smart")
        self.assertEqual(len(result["tools"]), 2)
        self.assertEqual(result["counts"]["statically_inspected"], 2)
        self.assertEqual(result["mode"], "smart")
        self.assertFalse(result["activation"]["execution_authorized"])

    def test_invalid_mode_or_cycle_rejected_before_planning(self):
        with self.assertRaisesRegex(ValueError, "activation"):
            self.inspect("invalid")
        self.adapters["tool:first"]["depends_on"] = ["tool:second"]
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            self.inspect()


if __name__ == "__main__":
    unittest.main()
