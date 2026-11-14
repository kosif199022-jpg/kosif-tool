"""The arena is a required Black Dragon step: arena_gate.py sizes it, picks the models and gates delivery."""
import importlib.util
import os
import subprocess
import sys
import unittest
from pathlib import Path

GATE = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "arena" / "arena_gate.py"
spec = importlib.util.spec_from_file_location("arena_gate", GATE)
AG = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AG)


class ArenaGateTest(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual(AG.size("حمّل الفيديو ده وحوّله mp3")["agents"], 0)
        self.assertEqual(AG.size("اكتب هوك لريل عن الإصرار")["agents"], 4)
        self.assertEqual(AG.size("الإجابة وحشة، هاتلي أحسن من كده")["agents"], 16)
        r = AG.size("خليهم يتعاركوا 100 وكيل على السكريبت")
        self.assertEqual(r["agents"], 100)
        self.assertTrue(r["ask_first"])

    def test_model_plan_matches_upstream_call_counts(self):
        self.assertEqual(AG.model_plan(16)["calls"], 91)
        self.assertEqual(AG.model_plan(100)["calls"], 595)
        p = AG.model_plan(16)
        self.assertEqual((p["haiku"], p["sonnet"], p["main"]), (48, 28, 15))

    def test_judges_never_on_haiku(self):
        for rnd in range(1, 8):
            self.assertIsNone(AG.agent_for("judge", rnd)["model"])
        self.assertIsNone(AG.agent_for("final", 0)["model"])
        self.assertEqual(AG.agent_for("spawn", 0)["subagent_type"], "arena-fighter")

    def test_selftest_runs_a_real_bracket(self):
        r = subprocess.run([sys.executable, str(GATE), "selftest"], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), cwd="/tmp")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
