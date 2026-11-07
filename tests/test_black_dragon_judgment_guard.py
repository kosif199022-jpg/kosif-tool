"""Tests for the book-informed Black Dragon judgment guard."""
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT / ".claude/skills/kosif-black-dragon/scripts/judgment_guard.py"
spec=importlib.util.spec_from_file_location("judgment_guard",SCRIPT)
guard=importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

class JudgmentGuardTests(unittest.TestCase):
    def test_high_stakes_prompts_deliberation(self):
        r=guard.review({"goal":"Choose a video route","stakes":"high","reversible":False})
        self.assertEqual(r["mode"],"deliberate_review")
        self.assertIn("hard_to_reverse",r["deliberation_reasons"])
        self.assertEqual(len(r["review_checks"]),11)

    def test_complete_simple_case_keeps_lightweight_path(self):
        r=guard.review({"goal":"A quick transition","stakes":"low","options":["fade"],
                        "known_evidence":["preview"],"reference_class":"past short edits","sample_size":10})
        self.assertEqual(r["mode"],"lightweight_review")

    def test_question_substitution_and_anchoring_are_flagged(self):
        r=guard.review({"goal":"Cost","known_evidence":["invoice"],
                        "target_question":"What will this job cost?",
                        "proxy_question":"Does the effect look nice?", "anchor":200})
        self.assertIn("question_substitution",r["checks_needing_attention"])
        self.assertIn("anchoring",r["checks_needing_attention"])

    def test_outside_view_median_is_descriptive(self):
        r=guard.review({"goal":"Edit plan","outside_view_examples":[18,7,15,9]})
        self.assertEqual(r["reference_class_benchmark_median"],12)
        self.assertEqual(r["reference_class_sample_count"],4)

    def test_intuition_requires_feedback_context(self):
        r=guard.review({"goal":"Predict scene reaction","trusted_intuition":True,
                        "stable_environment":False,"feedback_history":False})
        self.assertIn("intuition",r["checks_needing_attention"])

    def test_does_not_fabricate_council_or_video_output(self):
        r=guard.review({"goal":"Create cinematic teaser"})
        self.assertNotIn("winning_route",r)
        self.assertNotIn("video_path",r)
        self.assertTrue(all(c["owner"] in guard.SEATS for c in r["review_checks"]))

    def test_validation(self):
        for x in ({},{"goal":"x","options":["a","a"]},{"goal":"x","stakes":"extreme"},
                  {"goal":"x","outside_view_examples":[-1]},{"goal":"x","sample_size":-2},
                  {"goal":"x","reversible":"false"}):
            with self.subTest(x=x), self.assertRaises(ValueError):
                guard.review(x)

if __name__=="__main__":
    unittest.main()
