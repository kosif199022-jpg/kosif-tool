"""Generalization of the USIP request card and plans to fresh everyday requests (evals/routing_generalization.json).

Batch 3 was written after the routing changes and measured once before this gate was set; keep adding untouched
batches rather than tuning on a case and editing its label. Measured on 2026-10-24 (original → now):
  request card 26/50 → 46/50 · off-domain plan picks 46/337 → 2/312 · untouched batch 3: 8/14 → 10/14, 11/95 → 1/89.
"""
import sys, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
sys.path.insert(0, str(SK / "evals"))
import routing_generalization as R  # noqa: E402

MIN_CARD_ACCURACY = 0.9      # measured 0.92
MAX_OFF_DOMAIN_PICKS = 3     # measured 2


class RoutingGeneralization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = R.evaluate()

    def test_request_card_accuracy(self):
        bad = [(r["id"], r["request"], r["errors"]) for r in self.res["cases"] if not r["card_ok"]]
        self.assertGreaterEqual(self.res["card_accuracy"], MIN_CARD_ACCURACY, bad)

    def test_plans_stay_in_domain(self):
        bad = [(r["id"], r["off_domain"]) for r in self.res["cases"] if r["off_domain"]]
        self.assertLessEqual(self.res["off_domain_picks"], MAX_OFF_DOMAIN_PICKS, bad)
        self.assertGreater(self.res["plan_picks"], 0)

    def test_business_decisions_are_strategy_not_motion(self):
        """The defect that started this set: a pricing decision was planned with spring easing and paper textures."""
        row = next(r for r in self.res["cases"] if r["id"] == "G10")
        self.assertEqual(row["primary"], "strategy")
        self.assertEqual(row["off_domain"], [])

    def test_bug_fix_is_work_not_a_question(self):
        row = next(r for r in self.res["cases"] if r["id"] == "G06")
        self.assertEqual((row["primary"], row["level"] != "L0"), ("code", True))


if __name__ == "__main__":
    unittest.main()
