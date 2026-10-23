"""USIP v5.4 reasoning tools in scripts/think.py (appendix A24): modes, bayes, gate and audit."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "kosif-superpowers"
SCRIPT = SKILL / "scripts" / "think.py"
spec = importlib.util.spec_from_file_location("think_reasoning", SCRIPT)
think = importlib.util.module_from_spec(spec)
spec.loader.exec_module(think)


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, timeout=120)


class ModesTest(unittest.TestCase):
    def test_library_is_complete(self):
        modes = json.loads((SKILL / "data" / "reasoning_modes.json").read_text(encoding="utf-8"))["modes"]
        ids = [m["id"] for m in modes]
        self.assertEqual(len(ids), len(set(ids)))
        for want in ("deductive", "inductive", "abductive", "analogical", "causal", "systems", "lateral", "bayesian"):
            self.assertIn(want, ids)
        for m in modes:
            with self.subTest(mode=m["id"]):
                self.assertGreaterEqual(len(m["procedure"]), 3)
                for k in ("ar", "en", "use_when", "trap", "check"):
                    self.assertTrue(m[k])
                self.assertRegex(m["ar"], r"[؀-ۿ]")

    def test_ranking_follows_the_task(self):
        self.assertEqual(think.rank_modes("why does the render crash with an error?", 1)[0]["id"], "abductive")
        self.assertEqual(think.rank_modes("اقترح فكرة جديدة ومبتكرة للحملة", 1)[0]["id"], "lateral")
        self.assertEqual(think.rank_modes("what is the probability this risk happens given the evidence", 1)[0]["id"], "bayesian")
        self.assertEqual(think.rank_modes("إعادة تنظيم المنظومة ومعمارية خط الإنتاج", 1)[0]["id"], "systems")

    def test_default_kit_fills_up_to_n(self):
        got = think.rank_modes("hello", 3)
        self.assertEqual([m["id"] for m in got], ["abductive", "causal", "bayesian"])
        self.assertIn("trap:", run("modes", "hello").stdout)


class BayesTest(unittest.TestCase):
    def test_binary_update_is_exact(self):
        r = think.bayes_binary(0.2, [("a", 4), ("b", 0.5)], threshold=0.5)
        self.assertAlmostEqual(r["steps"][0]["posterior"], 0.5)
        self.assertAlmostEqual(r["posterior"], 1 / 3, places=4)
        self.assertEqual(r["steps"][0]["bits"], 2.0)
        self.assertEqual(r["decision"], "DO_NOT_ACT")
        self.assertFalse(r["robust"])     # doubling either ratio reaches the threshold

    def test_robust_when_far_from_threshold(self):
        r = think.bayes_binary(0.5, [("strong", 20), ("strong2", 10)], threshold=0.7)
        self.assertEqual(r["decision"], "ACT")
        self.assertTrue(r["robust"])

    def test_multi_hypothesis(self):
        r = think.bayes_multi({"config": 1, "code": 1, "data": 2}, [{"name": "fails only in CI", "likelihood": {"config": 0.9, "code": 0.2, "data": 0.1}}])
        self.assertEqual(r["leader"], "config")
        self.assertAlmostEqual(sum(r["posterior"].values()), 1.0, places=3)

    def test_bad_input_is_refused(self):
        for bad in (lambda: think.bayes_binary(1.0, []), lambda: think.bayes_binary(0.5, [("x", 0)]),
                    lambda: think.bayes_multi({"a": 1, "b": 1}, [{"name": "e", "likelihood": {"a": 0.5}}])):
            with self.assertRaises(ValueError):
                bad()
        p = run("bayes", "--prior", "0.3", "--lr", "noequals")
        self.assertEqual(p.returncode, 2)

    def test_cli_json_spec(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "s.json"
            f.write_text(json.dumps({"prior": 0.1, "evidence": [{"name": "e", "lr": 9}], "threshold": 0.4}), encoding="utf-8")
            out = json.loads(run("bayes", "--json", str(f)).stdout)
            self.assertAlmostEqual(out["posterior"], 0.5)
            self.assertEqual(out["decision"], "ACT")


class GateTest(unittest.TestCase):
    def spec(self, **kw):
        s = {"decision": "x", "reversible": True,
             "go": [{"name": "errors", "op": "==", "threshold": 0, "observed": 0}],
             "pivot": [{"name": "orphans", "op": ">", "threshold": 0, "observed": 0}],
             "kill": [{"name": "broken", "op": ">", "threshold": 20, "observed": 0}]}
        s.update(kw)
        return s

    def test_verdicts(self):
        self.assertEqual(think.gate(self.spec())["verdict"], "GO")
        s = self.spec(); s["pivot"][0]["observed"] = 3
        self.assertEqual(think.gate(s)["verdict"], "PIVOT")
        s["kill"][0]["observed"] = 50
        self.assertEqual(think.gate(s)["verdict"], "KILL")     # kill beats pivot
        s = self.spec(); s["go"][0]["observed"] = None
        self.assertEqual(think.gate(s)["verdict"], "HOLD")
        s = self.spec(); s["go"][0]["observed"] = 2
        self.assertEqual(think.gate(s)["verdict"], "HOLD")

    def test_one_way_door(self):
        s = self.spec(reversible=False); s["kill"][0]["observed"] = None
        self.assertEqual(think.gate(s)["verdict"], "HOLD")     # irreversible: any unknown holds
        r = think.gate(self.spec(reversible=False))
        self.assertEqual(r["verdict"], "GO")
        self.assertTrue(r["needs_explicit_approval"])

    def test_needs_go_criteria_and_known_ops(self):
        with self.assertRaises(ValueError):
            think.gate({"go": []})
        with self.assertRaises(ValueError):
            think.gate({"go": [{"name": "x", "op": "≈", "threshold": 1, "observed": 1}]})
        self.assertIn('"go"', run("gate", "--template").stdout)


class AuditTest(unittest.TestCase):
    def test_ledger(self):
        text = "\n".join(["# Report", "All tests passed.", "All tests passed (`python3 -m unittest`).",
                          "تم رفع الجهارة إلى -14 LUFS", "Plain sentence without claims.", "```", "123 inside code", "```"])
        r = think.audit(text)
        self.assertEqual(r["claims"], 3)
        self.assertEqual([u["line"] for u in r["unsupported"]], [2, 4])
        self.assertEqual(len(r["calibration"]), 5)

    def test_strict_exit(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "r.md"
            f.write_text("Everything works.\n", encoding="utf-8")
            self.assertEqual(run("audit", str(f)).returncode, 0)
            self.assertEqual(run("audit", str(f), "--strict").returncode, 1)
            f.write_text("Everything works (evidence: out/test.log).\n", encoding="utf-8")
            self.assertEqual(run("audit", str(f), "--strict").returncode, 0)


if __name__ == "__main__":
    unittest.main()
