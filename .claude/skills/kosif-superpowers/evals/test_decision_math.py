"""Offline tests for decision_math.py (Monte Carlo, break-even, ICE, NPV/IRR, decision flip)."""
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "decision_math.py"
sys.path.insert(0, str(SK / "scripts"))
import decision_math as D  # noqa: E402

MODEL = {"inputs": {"price": {"dist": "triangular", "low": 8, "mode": 10, "high": 13},
                    "units": {"dist": "uniform", "low": 800, "high": 1200},
                    "cost": {"dist": "normal", "mean": 6, "sd": 0.5}, "fixed": 2500},
         "profit": "(price - cost) * units - fixed"}


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class DecisionMathTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "m.json").write_text(json.dumps(MODEL))

    def tearDown(self):
        self.tmp.cleanup()

    def test_percentile_known(self):
        self.assertEqual(D.percentile([1, 2, 3, 4], 0.5), 2.5)
        self.assertAlmostEqual(D.percentile([10, 20, 30, 40, 50], 0.9), 46.0)

    def test_montecarlo_constant_model(self):
        m = D.parse_model({"inputs": {"a": 3, "b": 2}, "profit": "a + b"})
        r = D.montecarlo(m, runs=100, seed=1)
        self.assertEqual((r["p10"], r["p50"], r["p90"], r["prob_below_target"]), (5, 5, 5, 0))

    def test_montecarlo_uniform_loss_probability(self):
        # profit = 4*u - 400 with u ~ U(0,200): loss iff u < 100 -> P = 0.5; P50 ~ 0, P90 ~ 4*180-400 = 320
        m = D.parse_model({"inputs": {"u": {"dist": "uniform", "low": 0, "high": 200}}, "profit": "4*u - 400"})
        r = D.montecarlo(m, runs=40000, seed=11)
        self.assertAlmostEqual(r["prob_below_target"], 0.5, delta=0.015)
        self.assertAlmostEqual(r["p50"], 0, delta=8)
        self.assertAlmostEqual(r["p90"], 320, delta=8)
        self.assertEqual(r["base_case_profit"], 0)

    def test_montecarlo_deterministic_cli(self):
        a = run("montecarlo", str(self.d / "m.json"), "--runs", "5000", "--seed", "7")
        b = run("montecarlo", str(self.d / "m.json"), "--runs", "5000", "--seed", "7")
        c = run("montecarlo", str(self.d / "m.json"), "--runs", "5000", "--seed", "8")
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(a.stdout, b.stdout)
        self.assertNotEqual(a.stdout, c.stdout)
        r = json.loads(a.stdout)
        self.assertTrue(r["p10"] < r["p50"] < r["p90"])
        self.assertEqual(r["base_case_profit"], 1500.0)  # (10-6)*1000-2500

    def test_breakeven(self):
        r = D.breakeven(25, 10000, 15)
        self.assertEqual((r["units"], r["revenue"], r["contribution_margin"]), (1000, 25000.0, 10))
        r = D.breakeven(10, 1000, 7)
        self.assertEqual(r["units"], 334)
        self.assertAlmostEqual(r["units_exact"], 333.333333, places=5)
        self.assertAlmostEqual(r["revenue"], 3333.3333, places=3)
        p = run("breakeven", "--price", "5", "--fixed", "100", "--variable", "6")
        self.assertEqual(p.returncode, 2)
        self.assertEqual(len(p.stderr.strip().splitlines()), 1)

    def test_ice(self):
        f = self.d / "b.csv"
        f.write_text("name,impact,confidence,ease\nA,8,7,5\nB,9,9,9\nC,3,4,10\n")
        r = D.ice(str(f))
        self.assertEqual([(x["name"], x["ice"], x["rank"]) for x in r["items"]],
                         [("B", 729, 1), ("A", 280, 2), ("C", 120, 3)])
        f.write_text("name,impact,confidence,ease\nA,11,7,5\n")
        self.assertEqual(run("ice", str(f)).returncode, 2)
        f.write_text("name,impact,ease\nA,1,1\n")
        self.assertEqual(run("ice", str(f)).returncode, 2)

    def test_npv_irr(self):
        r = D.npv(0.1, "-1000,300,400,500")
        # 300/1.1 + 400/1.21 + 500/1.331 - 1000 = -21.0368
        self.assertAlmostEqual(r["npv"], -21.0368, places=4)
        self.assertEqual(r["decision"], "reject")
        self.assertAlmostEqual(D.irr([-100, 110]), 0.1, places=8)
        self.assertAlmostEqual(D.irr([-100, 0, 121]), 0.1, places=8)
        self.assertIsNone(D.npv(0.1, "100,200")["irr"])
        p = run("npv", "--rate", "0.1", "--flows", "-100,110")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertAlmostEqual(json.loads(p.stdout)["irr"], 0.1, places=6)
        self.assertEqual(run("npv", "--rate", "-1", "--flows", "-1,2").returncode, 2)

    def test_flip(self):
        m = D.parse_model(MODEL)
        r = D.flip(m, "price")
        self.assertAlmostEqual(r["threshold"], 8.5, places=6)  # (p-6)*1000 = 2500
        self.assertEqual((r["go_side"], r["base_decision"]), ("above", "go"))
        r = D.flip(m, "cost")
        self.assertAlmostEqual(r["threshold"], 7.5, places=6)
        self.assertEqual(r["go_side"], "below")
        r = D.flip(m, "units", 2000, 3000)
        self.assertFalse(r["flips"])
        p = run("flip", str(self.d / "m.json"), "--var", "nope")
        self.assertEqual(p.returncode, 2)

    def test_refuses_unsafe_expression(self):
        for expr in ("__import__('os').system('x')", "price.real", "[price]"):
            with self.assertRaises(D.BadInput):
                D.parse_model({"inputs": {"price": 1}, "profit": expr})
        with self.assertRaises(D.BadInput):
            D.parse_model({"inputs": {"price": 1}, "profit": "price - ghost"})
        bad = self.d / "bad.json"
        bad.write_text("{not json")
        p = run("montecarlo", str(bad))
        self.assertEqual(p.returncode, 2)
        self.assertEqual(p.stdout, "")

    def test_stdin_input(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "ice", "-"], input="name,impact,confidence,ease\nX,2,5,10\n",
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["items"][0]["ice"], 100)

    def test_self_test(self):
        p = run("--self-test")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["self_test"], "ok")


if __name__ == "__main__":
    unittest.main()
