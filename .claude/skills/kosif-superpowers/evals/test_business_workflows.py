"""Offline tests for A18 business workflows (64 playbooks routed to Claude-native executors)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import business_workflows as B  # noqa: E402


class BusinessWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = B.load()

    def test_registry_scope(self):
        w = self.d["workflows"]
        self.assertEqual(sum(x["kind"] == "library" for x in w), 36)
        self.assertEqual(sum(x["kind"] == "creator_playbook" for x in w), 28)
        self.assertEqual(len(self.d["business_functions"]), 9)
        self.assertEqual({f["adoption_pct"] for f in self.d["business_functions"]} >= {85, 83, 80, 69, 63, 60, 20, 25, 33}, True)
        self.assertEqual(self.d["courses"]["count"], 27)
        for x in w:
            self.assertTrue(3 <= len(x["steps"]) <= 6, x["id"])
            for s in x["steps"]:
                self.assertNotIn("prompt", s)

    def test_no_prompts_stored(self):
        raw = (SK / "data" / "futurepedia_business_workflows.json").read_text(encoding="utf-8")
        self.assertNotIn('"prompt"', raw)
        self.assertNotIn('"tip"', raw)

    def test_search_arabic(self):
        self.assertEqual(B.search(self.d, "بودكاست")[0]["id"], "FW-07")
        self.assertIn(B.search(self.d, "اجتماع")[0]["id"], {"FP-07", "FP-09", "FW-10"})

    def test_coverage_numbers(self):
        cs = [B.coverage(x) for x in self.d["workflows"]]
        self.assertEqual(sum(c["steps"] for c in cs), 286)
        self.assertEqual(sum(c["claude_native"] for c in cs), 220)
        self.assertEqual(sum(c["native_pct"] == 100 for c in cs), 28)

    def test_plan_has_gates_and_refuses_overwrite(self):
        x = B.resolve(self.d, "FW-35")
        text = B.plan(self.d, x, "شركة برمجيات صغيرة")
        self.assertIn("PLAN_ONLY", text)
        self.assertIn("موافقة صريحة", text)
        with tempfile.TemporaryDirectory() as t:
            out = str(Path(t) / "p.md")
            args = ["plan", "--workflow", "FW-35", "--context", "x", "--out", out]
            self.assertEqual(B.main(args), 0)
            self.assertEqual(B.main(args), 2)
        with self.assertRaises(ValueError):
            B.resolve(self.d, "FW-99")


if __name__ == "__main__":
    unittest.main()
