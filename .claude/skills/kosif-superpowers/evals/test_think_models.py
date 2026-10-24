#!/usr/bin/env python3
"""Regression tests for `think.py models` (mental-model selection): diverse disciplines, reserved Inversion and
second-order lenses, and a usable lens (question, do-now action, misuse warning) for every pick. Read-only."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SCRIPT = SCRIPTS / "think.py"
sys.path.insert(0, str(SCRIPTS))
import think  # noqa: E402


def run(*args):
    r = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True, timeout=60)
    if r.returncode != 0:
        raise AssertionError(f"{args} -> {r.returncode}\n{r.stderr}")
    return r.stdout


class ThinkModelsTest(unittest.TestCase):
    def test_data_schema_is_intact(self):
        ms = think.load_models()
        self.assertEqual(len({m["id"] for m in ms}), len(ms))
        for m in ms:
            for k in ("id", "name_en", "name_ar", "discipline", "triggers", "question", "steps", "output", "pitfall"):
                self.assertTrue(m.get(k), f"{m.get('id')}: {k}")

    def test_pick_is_diverse_across_disciplines(self):
        for problem in ("find the root cause of the recurring bug", "should we launch the new pricing plan to our users",
                        "هل نطلق خطة التسعير الجديدة للعملاء؟", "brainstorm a creative new idea for the reel"):
            ms = think.rank_models(problem, 5)
            self.assertEqual(len(ms), 5)
            self.assertEqual(len({m["id"] for m in ms}), 5)
            per = {}
            for m in ms:
                per[m["discipline"]] = per.get(m["discipline"], 0) + 1
            self.assertLessEqual(max(per.values()), 2, f"{problem}: {per}")
            self.assertGreaterEqual(len(per), 3, problem)

    def test_plain_mode_keeps_score_order(self):
        plain = think.rank_models("brainstorm a creative new idea for the reel", 5, diverse=False)
        self.assertGreaterEqual(sum(m["discipline"] == "creativity" for m in plain), 3, "the v1 order clusters near-duplicates")
        div = think.rank_models("brainstorm a creative new idea for the reel", 5)
        self.assertLessEqual(sum(m["discipline"] == "creativity" for m in div), 2)

    def test_inversion_and_second_order_are_reserved_when_relevant(self):
        ids = [m["id"] for m in think.rank_models("should we launch the new pricing plan to our users", 5)]
        self.assertIn("MODEL-02", ids)
        self.assertIn("MODEL-03", ids)
        ids = [m["id"] for m in think.rank_models("find the root cause of the recurring bug", 4)]
        self.assertNotIn("MODEL-03", ids, "a pure diagnosis does not get the change lens forced in")

    def test_each_model_is_a_usable_lens(self):
        out = json.loads(run("models", "should we migrate the database this week", "-n", "4", "--json"))
        self.assertEqual(len(out), 4)
        for m in out:
            L = m["lens"]
            self.assertEqual(L["question"], m["question"])
            self.assertEqual(L["action"], m["steps"][0])
            self.assertTrue(L["misuse"].startswith("Misuse warning: "))
            self.assertTrue(L["why"])
        text = run("models", "should we migrate the database this week")
        self.assertIn("▶ do now:", text)
        self.assertIn("⚠ Misuse warning:", text)
        self.assertIn("disciplines covered:", text)

    def test_deterministic_and_never_short(self):
        a = [m["id"] for m in think.rank_models("x", 7)]
        self.assertEqual(a, [m["id"] for m in think.rank_models("x", 7)])
        self.assertEqual(len(a), 7)
        self.assertEqual(len(think.rank_models("x", 70)), len(think.load_models()))
        self.assertNotIn("MODEL-01", [m["id"] for m in think.rank_models("x", 5, exclude=("MODEL-01",))])


if __name__ == "__main__":
    unittest.main()
