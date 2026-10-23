"""Prompt lab (scripts/prompt_lab.py): build, lint, refine, eval and the order-swapped judge."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SK / "scripts"))
import prompt_lab as P  # noqa: E402

CLI = [sys.executable, str(SK / "scripts" / "prompt_lab.py")]


class PromptLabTest(unittest.TestCase):
    def test_self_test(self):
        p = subprocess.run(CLI + ["--self-test"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_every_kind_builds_and_its_full_build_lints_clean_of_missing_slots(self):
        for kind, spec in P.KINDS.items():
            skeleton = P.build(kind, "", {})
            self.assertIn("[[", skeleton, kind)
            rep = P.lint(skeleton, kind)
            self.assertIn(rep["band"], ("ship", "fix-lowest", "rewrite", "fail-gate"))

    def test_weak_prompt_scores_below_strong_and_hype_is_flagged(self):
        weak = P.lint("Make a nice image of a dog, 8k, masterpiece", "image")
        strong = P.lint("A black dog running on a wet beach at sunset. Wide shot, 35mm, low angle. Golden light from behind, "
                        "long shadows. Muted teal and orange palette, film grain style. Aspect 16:9.", "image")
        self.assertLess(weak["score"], strong["score"])
        self.assertIn("hype", {f["code"] for f in weak["findings"]})

    def test_gates(self):
        self.assertEqual(P.lint("token ghp_" + "a" * 30, "agent")["band"], "fail-gate")
        self.assertEqual(P.lint("Show your reasoning in full, then answer.", "writing")["band"], "fail-gate")
        self.assertEqual(P.lint("Summarise this.\n" + "data " * 400, "writing")["band"], "fail-gate")
        self.assertNotEqual(P.lint("Summarise this.\n<document>\n" + "data " * 400 + "\n</document>", "writing")["band"], "fail-gate")

    def test_arabic_vague_words(self):
        rep = P.lint("اكتب بوست حلو وجامد شوية عن المنتج", "writing")
        self.assertIn("vague", {f["code"] for f in rep["findings"]})

    def test_eval_keep_or_revert(self):
        cases = [{"id": "a", "assert": [{"type": "json-keys", "value": ["title"]}]},
                 {"id": "b", "assert": [{"type": "not-contains", "value": "As an AI"}]}]
        outs = {"old": {"a": "{\"title\": 1}", "b": "As an AI I cannot"}, "new": {"a": "{\"title\": 2}", "b": "Here it is"},
                "worse": {"a": "oops", "b": "Here it is"}}
        rep = P.evaluate(cases, outs, baseline="old")
        self.assertTrue(rep["verdict"]["new"]["keep"])
        self.assertEqual(rep["verdict"]["worse"]["regressions"], ["a"])
        with self.assertRaises(ValueError):
            P.check_assert({"type": "nope"}, "x")

    def test_cli_eval_and_pairwise_files(self):
        with tempfile.TemporaryDirectory() as d:
            c, o, v = Path(d, "c.json"), Path(d, "o.json"), Path(d, "v.json")
            c.write_text(json.dumps([{"id": "x", "assert": [{"type": "regex", "value": "^OK"}]}]))
            o.write_text(json.dumps({"A": {"x": "no"}, "B": {"x": "OK done"}}))
            v.write_text(json.dumps([{"case": "x", "first": "B", "second": "B"}]))
            p = subprocess.run(CLI + ["eval", "--cases", str(c), "--outputs", str(o), "--baseline", "A"], capture_output=True, text=True, timeout=60)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue(json.loads(p.stdout)["verdict"]["B"]["keep"])
            p = subprocess.run(CLI + ["pairwise", "--verdicts", str(v)], capture_output=True, text=True, timeout=60)
            self.assertEqual(json.loads(p.stdout)["winner"], "B")

    def test_lint_exit_codes(self):
        p = subprocess.run(CLI + ["lint", "-", "--kind", "image"], input="nice cat 8k", capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 1)


if __name__ == "__main__":
    unittest.main()
