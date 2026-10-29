"""llm_council.py hard constraints and context reporting (USIP v5.8, A38 §7). Offline, stdlib only.

The bug of 2026-10-29: `frame --context` keeps at most MAX_CONTEXT items, so a user rule passed there
(«لا ترجمة للآيات») was dropped without a word and none of the five advisors saw it. `--constraints` now
carries such rules, never truncated, in their own section right after the question in every prompt; what
--context drops is listed in `dropped_context`, with a stderr warning when the user's own items are cut.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_llm_council.py' -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "llm_council.py"
sys.path.insert(0, str(SK / "scripts"))
import llm_council as lc  # noqa: E402

RULE = "لا ترجمة للآيات"
def sample(adv: str) -> str:
    """A distinct, grounded 170-word answer per advisor (identical answers would be DUPLICATE_VOICE)."""
    return " ".join(f"w{adv}{n}" for n in range(170)) + " evidence brief.json backs الخطة B"


def cli(*args, cwd):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, cwd=cwd,
                          timeout=120)


class CouncilConstraintsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.brief = self.root / "brief.json"
        self.brief.write_text(json.dumps({"plans": {"A": {"idea": "calligraphy only"}, "B": {"idea": "mosque footage"},
                                                    "C": {"idea": "light painting"}}, "recommended": "B",
                                          "analysis": {"request": "a Quran recitation reel"}}), encoding="utf-8")
        for n in range(4):
            (self.root / f"f{n}.md").write_text("notes", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def frame(self, *extra, d="c", level="L3"):
        return cli("frame", "Which look for the recitation reel?", "--dir", str(self.root / d), "--level", level,
                   "--root", str(self.root), "--from-brief", str(self.brief), *extra, cwd=self.root)

    def prompt(self, d, name):
        return (self.root / d / "prompts" / name).read_text(encoding="utf-8")

    def head(self, d):
        c = json.loads((self.root / d / "council5.json").read_text(encoding="utf-8"))
        return f"{c['question']}\n\n{lc.CONSTRAINTS_HEAD}"

    def test_self_test(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--self-test"], capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("self-test: OK", r.stdout)

    def test_help_lists_constraints(self):
        for sub in ("frame", "light"):
            r = cli(sub, "--help", cwd=self.root)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("--constraints", r.stdout)

    def test_rule_passed_as_context_is_reported_not_lost(self):
        """The real bug: brief + four files + the rule as --context. The rule is cut, and that is said."""
        r = self.frame("--context", "f0.md", "f1.md", "f2.md", "f3.md", RULE)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["context"], [str(self.brief), "f0.md", "f1.md", "f2.md"])
        self.assertEqual(out["dropped_context"], ["f3.md", RULE])
        self.assertIn("llm_council: warning:", r.stderr)
        self.assertIn(f"dropped: f3.md; {RULE}", r.stderr)
        self.assertIn("--constraints", r.stderr)
        self.assertIn("not files", r.stderr)
        self.assertEqual(out["constraints"], [])

    def test_constraints_reach_every_prompt_right_after_the_question(self):
        rules = [RULE, "no audio-reactive pulsing"]
        r = self.frame("--constraints", *rules, "--context", "f0.md")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout)["constraints"], rules)
        self.assertEqual(r.stderr, "")
        head = self.head("c")
        for adv in lc.IDS:
            text = self.prompt("c", f"advisor_{adv}.txt")
            with self.subTest(advisor=adv):
                self.assertIn(head, text)
                for rule in rules:
                    self.assertIn(f"- {rule}\n", text)
        outsider = self.prompt("c", "advisor_outsider.txt")
        self.assertNotIn("Context worth reading", outsider)
        self.assertNotIn("f0.md", outsider)
        d = str(self.root / "c")
        for adv in lc.IDS:
            f = self.root / f"{adv}.md"
            f.write_text(sample(adv), encoding="utf-8")
            self.assertEqual(cli("ingest", "--dir", d, "--advisor", adv, "--file", str(f), cwd=self.root).returncode, 0)
        self.assertEqual(cli("review", "--dir", d, cwd=self.root).returncode, 0)
        review = self.prompt("c", "review_R3.txt")
        self.assertIn(head, review)
        self.assertIn("cannot be the strongest", review)
        rv = self.root / "r.md"
        rv.write_text("1. Response B is strongest. 2. Response D misses cost. 3. All five missed timing.",
                      encoding="utf-8")
        for rid in lc.REVIEWERS:
            self.assertEqual(cli("ingest-review", "--dir", d, "--reviewer", rid, "--file", str(rv),
                                 cwd=self.root).returncode, 0)
        self.assertEqual(cli("chair", "--dir", d, cwd=self.root).returncode, 0)
        chair = self.prompt("c", "chair.txt")
        self.assertIn(head, chair)
        self.assertIn("overruled on that point", chair)
        st = json.loads(cli("status", "--dir", d, cwd=self.root).stdout)
        self.assertEqual(st["constraints"], rules)

    def test_constraints_are_never_truncated(self):
        rules = [f"rule number {n}" for n in range(25)]
        r = self.frame("--constraints", *rules)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["constraints"], rules)
        for adv in lc.IDS:
            text = self.prompt("c", f"advisor_{adv}.txt")
            self.assertTrue(all(f"- {rule}\n" in text for rule in rules), adv)

    def test_light_carries_constraints(self):
        r = cli("light", "Which font?", "--dir", str(self.root / "l"), "--root", str(self.root),
                "--constraints", RULE, cwd=self.root)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(f"Which font?\n\n{lc.CONSTRAINTS_HEAD}\n- {RULE}\n", self.prompt("l", "light.txt"))

    def test_auto_context_dropped_is_listed_without_a_user_warning(self):
        (self.root / "CLAUDE.md").write_text("entry", encoding="utf-8")
        r = self.frame("--context", "f0.md", "f1.md", "f2.md")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["dropped_context"], ["CLAUDE.md"])
        self.assertEqual(out["warnings"], [])
        self.assertEqual(r.stderr, "")

    def test_without_constraints_the_prompts_do_not_change(self):
        r = self.frame("--context", "f0.md")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("Hard constraints", self.prompt("c", "advisor_executor.txt"))
        framed = lc.framed_text("q", ["f0.md"], "", [], [])
        self.assertEqual(framed, lc.framed_text("q", ["f0.md"], "", [], [], constraints=[]))

    def test_documented(self):
        a38 = (SK / "references/protocol/A38-v58-thinking-books-github-pulse.md").read_text(encoding="utf-8")
        self.assertIn("--constraints", a38)
        self.assertIn("dropped_context", a38)
        tools = json.loads((SK / "data/tools.json").read_text(encoding="utf-8"))
        entry = next(t for t in (tools["tools"] if isinstance(tools, dict) else tools) if t["id"] == "llm-council")
        self.assertIn("--constraints", json.dumps(entry, ensure_ascii=False))
        self.assertIn(".claude/skills/kosif-superpowers/evals/test_llm_council.py", entry["tests"])


if __name__ == "__main__":
    unittest.main()
