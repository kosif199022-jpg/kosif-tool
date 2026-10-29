"""USIP v5.5 intelligence tools in scripts/think.py (appendices A25-A29): intake, decompose, qa and recover."""
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
spec = importlib.util.spec_from_file_location("think_intel", SCRIPT)
think = importlib.util.module_from_spec(spec)
spec.loader.exec_module(think)
DATA = json.loads((SKILL / "data" / "usip_intelligence.json").read_text(encoding="utf-8"))
CLASSES = ("missing_dependency", "wrong_input_kind", "quality_below_threshold", "timeout",
           "permission_denied", "license_blocked", "tool_error", "other")


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, timeout=120)


class DataTest(unittest.TestCase):
    def test_every_kind_is_complete(self):
        self.assertGreaterEqual(len(DATA["kinds"]), 12)
        for kid, k in DATA["kinds"].items():
            with self.subTest(kind=kid):
                self.assertRegex(k["ar"], r"[؀-ۿ]")
                self.assertTrue(k["keywords"] and k["slots"] and k["quality"])
                ids = [c["id"] for c in k["quality"]]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(any(c["hard"] for c in k["quality"]), "every kind has at least one hard check")
                for s in k["slots"]:
                    self.assertIn(s["severity"], ("assume", "ask", "blocker"))
                    self.assertTrue(s["default"])

    def test_recovery_classes_match_fusionforge(self):
        self.assertEqual(tuple(DATA["recovery"]), CLASSES)
        ff = (SKILL / "scripts" / "fusionforge.py").read_text(encoding="utf-8")
        for c in CLASSES:
            self.assertIn(c, ff, f"{c} is not a FusionForge --error-class")
        for c, r in DATA["recovery"].items():
            with self.subTest(cls=c):
                self.assertGreaterEqual(r["budget"], 1)
                self.assertTrue(r["diagnose"] and r["fix"] and r["fallback"] and r["escalate"])


class IntakeTest(unittest.TestCase):
    def test_reel_request(self):
        r = think.intake("اعمل لي ريلز 30 ثانية من صوتي", "L2")
        self.assertEqual(r["kinds"][0], "video")
        filled = {x["slot"] for x in r["filled"] if x["kind"] == "video"}
        self.assertTrue({"aspect", "duration", "audio"} <= filled)
        self.assertFalse(r["sensitive"])

    def test_blocker_and_question_budget(self):
        r = think.intake("analyze my sales data and make a chart", "L1")
        self.assertEqual(r["kinds"][0], "data")
        self.assertLessEqual(len(r["questions"]), DATA["question_budget"]["L1"])
        r0 = think.intake("analyze the sales data", "L0")
        self.assertEqual(r0["questions"], [], "L0 asks nothing")
        r2 = think.intake("حلل البيانات وقل لي السبب")
        self.assertIn("source", {x["slot"] for x in r2["blockers"]}, "data without a file is a blocking input")

    def test_sensitive_words_force_the_safe_default(self):
        self.assertTrue(think.intake("اعمل فيديو وانشره على حسابي")["sensitive"])
        self.assertTrue(think.intake("build the site and deploy it")["sensitive"])

    def test_unknown_level_is_refused(self):
        with self.assertRaises(ValueError):
            think.intake("x", "L9")


class DecomposeTest(unittest.TestCase):
    def test_template_is_valid(self):
        r = think.decompose(think.DECOMPOSE_TEMPLATE)
        self.assertEqual(r["verdict"], "OK")
        self.assertEqual(r["order"][0], "T1")
        self.assertEqual(r["one_way_doors"], ["T5"])
        lo, hi = r["critical_path"]["optimistic"][0], r["critical_path"]["pessimistic"][0]
        self.assertAlmostEqual(lo, 2.3)
        self.assertAlmostEqual(hi, 6.2)

    def test_parallel_branches_pick_the_longer_chain(self):
        spec = {"tasks": [
            {"id": "a", "deps": [], "est": [1, 1], "done": "x", "verify": "y"},
            {"id": "b", "deps": ["a"], "est": [5, 5], "done": "x", "verify": "y"},
            {"id": "c", "deps": ["a"], "est": [1, 1], "done": "x", "verify": "y"},
            {"id": "d", "deps": ["b", "c"], "est": [1, 1], "done": "x", "verify": "y"}]}
        r = think.decompose(spec)
        self.assertEqual(r["critical_path"]["pessimistic"], [7.0, ["a", "b", "d"]])

    def test_cycles_and_gaps(self):
        with self.assertRaises(ValueError):
            think.decompose({"tasks": [{"id": "a", "deps": ["b"]}, {"id": "b", "deps": ["a"]}]})
        r = think.decompose({"tasks": [{"id": "a", "deps": ["zz"], "est": [1, 2]}]})
        self.assertEqual(r["verdict"], "FIX")
        self.assertTrue(any("unknown task zz" in p for p in r["problems"]))
        self.assertTrue(any("no verify" in p for p in r["problems"]))

    def test_late_risk_is_flagged(self):
        spec = {"tasks": [
            {"id": "a", "deps": [], "est": [1, 1], "risk": 0, "done": "x", "verify": "y"},
            {"id": "b", "deps": ["a"], "est": [1, 1], "risk": 0, "done": "x", "verify": "y"},
            {"id": "c", "deps": ["b"], "est": [1, 1], "risk": 3, "done": "x", "verify": "y"}]}
        self.assertTrue(any("spike" in a for a in think.decompose(spec)["advice"]))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            ok, bad = Path(d) / "ok.json", Path(d) / "bad.json"
            ok.write_text(json.dumps(think.DECOMPOSE_TEMPLATE), encoding="utf-8")
            bad.write_text(json.dumps({"tasks": [{"id": "a"}]}), encoding="utf-8")
            self.assertEqual(run("decompose", str(ok)).returncode, 0)
            self.assertEqual(run("decompose", str(bad)).returncode, 1)


class QaTest(unittest.TestCase):
    def test_verdicts(self):
        hard = [c["id"] for c in DATA["kinds"]["code"]["quality"] if c["hard"]]
        soft = [c["id"] for c in DATA["kinds"]["code"]["quality"] if not c["hard"]]
        allok = {i: True for i in hard + soft}
        self.assertEqual(think.qa("code", allok)["verdict"], "PASS")
        self.assertEqual(think.qa("code", {**allok, soft[0]: False})["verdict"], "PASS", "a soft failure is reported, not fatal")
        self.assertEqual(think.qa("code", {**allok, hard[0]: False})["verdict"], "FAIL")
        self.assertEqual(think.qa("code", {i: True for i in soft})["verdict"], "INCOMPLETE")
        self.assertEqual(think.qa("code", {**allok, hard[0]: "n/a"})["verdict"], "INCOMPLETE", "a hard check cannot be waived")

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            think.qa("nope")
        with self.assertRaises(ValueError):
            think.qa("code", {"made_up": True})
        self.assertEqual(run("qa", "nope").returncode, 2)


class RecoverTest(unittest.TestCase):
    def test_guess_and_budget(self):
        r = think.recover(message="ModuleNotFoundError: No module named 'cv2'")
        self.assertEqual(r["error_class"], "missing_dependency")
        self.assertTrue(r["guessed"])
        self.assertTrue(think.recover("timeout", attempts=0)["next"].startswith("attempt 1"))
        self.assertTrue(think.recover("permission_denied", attempts=1)["next"].startswith("STOP"))
        self.assertEqual(think.recover(message="something odd")["error_class"], "other")
        mcp = think.recover(message="InputValidationError: mcp__Higgsfield__generate_image was called with input that could not be parsed as JSON.")
        self.assertEqual(mcp["error_class"], "wrong_input_kind")
        self.assertTrue(any("params" in s for s in mcp["fix"]))
        sbx = think.recover(message='MCP server "Higgsfield" tool "sandbox_exec" timed out after 60s')
        self.assertEqual(sbx["error_class"], "timeout")
        self.assertTrue(any("background:true" in s for s in sbx["fix"]))
        self.assertEqual(run("recover", "tool_error", "--attempts", "3").returncode, 1)
        with self.assertRaises(ValueError):
            think.recover("made_up")


if __name__ == "__main__":
    unittest.main()
