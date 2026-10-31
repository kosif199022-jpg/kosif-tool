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


if __name__ == "__main__":
    unittest.main()
