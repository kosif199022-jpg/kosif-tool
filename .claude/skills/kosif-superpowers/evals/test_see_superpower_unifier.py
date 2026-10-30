#!/usr/bin/env python3
"""Regression tests for SEE → Superpowers fusion, without network/model access."""
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "see_superpower_unifier.py"
spec = importlib.util.spec_from_file_location("see_superpower_unifier", PATH)
fusion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fusion)


class SeeSuperpowerFusionTests(unittest.TestCase):
    def test_coverage_is_full_but_loading_is_selective(self):
        p = fusion.fuse("مراجعة فواتير البنك والاكسل", {"tools": [], "powers": []})
        self.assertEqual(len(p["thinking_lenses"]), 11)
        self.assertEqual(len(p["see_domain_coverage"]), 9)
        self.assertLessEqual(len(p["selected_see_methods"]), 2)
        self.assertIn("kosif-finance-data", {m["name"] for m in p["selected_see_methods"]})

    def test_deep_load_limit(self):
        self.assertLessEqual(len(fusion.select_methods(
            "بحث برمجة محاسبة فيديو برومبت تخطيط مهارات اتمتة اختبار", "deep")), 4)
        self.assertEqual(fusion.select_methods("finance", "fast"), [])

    def test_hub_ids_are_not_duplicated_or_replaced(self):
        p = fusion.fuse("develop", {"powers": [
            {"id": "SP-002", "family": "dev"}, {"id": "SP-002"}, {"id": "SP-003"}
        ], "tools": []})
        self.assertEqual([x["id"] for x in p["existing_superpowers"]], ["SP-002", "SP-003"])

    def test_tool_exposure_is_not_execution(self):
        p = fusion.fuse("code test", {"tools": [
            {"id": "TOOL-1", "readiness": {"state": "ready"}},
            {"id": "TOOL-2", "readiness": {"state": "missing"}}
        ]})
        self.assertEqual(p["existing_tools"][0]["status"], "executor_exposed")
        self.assertEqual(p["existing_tools"][1]["status"], "candidate_only")
        self.assertTrue(all(x["executed"] is False for x in p["existing_tools"]))
        self.assertFalse(p["claims"]["executed"])
        self.assertFalse(p["verified"])
        self.assertEqual(p["graph"]["nodes"][-1]["state"], "pending_execution")

    def test_full_pro_is_never_implicitly_complete(self):
        p = fusion.fuse("Full Pro", {}, mode="full_pro")
        self.assertEqual(p["full_pro"]["status"], "NOT_FULL_PRO")
        self.assertFalse(p["full_pro"]["completed"])
        self.assertEqual(p["claims"]["reviewers_executed"], 0)

    def test_query_does_not_echo_secret(self):
        secret = "ghp_" + "a" * 25
        p = fusion.fuse("please test " + secret, {})
        self.assertNotIn(secret, p["query"])
        self.assertIn("[REDACTED]", p["query"])

    def test_bad_mode_and_input_fail_closed(self):
        with self.assertRaises(ValueError):
            fusion.select_methods("x", "impossible")
        with self.assertRaises(ValueError):
            fusion.fuse("x", [], "standard")

    def test_latin_keywords_match_whole_words_only(self):
        names = lambda q: [m["name"] for m in fusion.select_methods(q, "deep")]
        self.assertNotIn("kosif-eval-trust", names("the latest approach"))          # latest != test
        self.assertNotIn("kosif-skill-orchestrator", names("a poem I have seen"))   # seen != see
        self.assertEqual(names("a rapid approach"), ["kosif-research-evidence"])   # rapid/approach != api/app
        self.assertIn("kosif-eval-trust", names("run the tests"))                   # plural still matches
        self.assertIn("kosif-finance-data", names("راجع الفواتير"))                  # Arabic stems keep prefixes

    def test_hub_find_prints_a_real_newline_before_the_see_block(self):
        import subprocess, sys
        hub = PATH.parent / "hub.py"
        out = subprocess.run([sys.executable, str(hub), "find", "fix the python code"],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("SEE × Superpowers", out)
        self.assertNotIn("\\n🧠", out)

if __name__ == "__main__":
    unittest.main(verbosity=2)
