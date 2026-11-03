"""kosif-kling-director: the prompt pack adds up, passes the Kling lint, and planted mistakes are caught."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / ".claude/skills/kosif-kling-director/scripts/kling_director.py"


def run(*args, cwd=None):
    return subprocess.run([sys.executable, "-I", "-B", str(TOOL), *args], capture_output=True, text=True,
                          timeout=120, cwd=cwd)


class KlingDirector(unittest.TestCase):
    def test_self_test(self):
        done = run("--self-test")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn("SELF-TEST PASS", done.stdout)

    def test_plan_blocks(self):
        self.assertEqual(json.loads(run("plan", "90", "--json").stdout)["blocks"], [[0, 30], [30, 60], [60, 90]])
        self.assertEqual(json.loads(run("plan", "45", "--flash", "--json").stdout)["blocks"], [[0, 15], [15, 30], [30, 45]])
        self.assertEqual(run("plan", "2").returncode, 2)

    def test_build_writes_lint_clean_blocks_with_the_story(self):
        with tempfile.TemporaryDirectory() as tmp:
            done = run("build", "--task", "ساعي بريد يسابق المطر", "--seconds", "45", "--out", tmp, "--json")
            self.assertEqual(done.returncode, 0, done.stdout[-800:])
            plan = json.loads((Path(tmp) / "plan.json").read_text(encoding="utf-8"))
            self.assertEqual([b["film_range_s"] for b in plan["blocks"]], [[0, 23], [23, 45]])
            self.assertEqual(plan["credits_spent"], 0)
            block = (Path(tmp) / "block_02.txt").read_text(encoding="utf-8")
            self.assertIn("ساعي بريد يسابق المطر", block.split("ACTIVE REFERENCES")[0])
            self.assertEqual((Path(tmp) / "storyboard_01.txt").read_text(encoding="utf-8").count("Panel "), 9)

    def test_story_with_polish_and_brand_words_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            done = run("build", "--task", "flawless 8K shot on a Zeiss lens", "--seconds", "10", "--out", tmp, "--json")
            self.assertEqual(done.returncode, 1)
            self.assertTrue({"polish", "brands"} <= set(json.loads(done.stdout)["blocks"][0]["lint"]["failed"]))

    def test_check_catches_a_gap_in_the_clock(self):
        with tempfile.TemporaryDirectory() as tmp:
            run("build", "--task", "a quiet duel at dawn", "--seconds", "30", "--out", tmp)
            p = Path(tmp) / "block_01.txt"
            p.write_text(p.read_text(encoding="utf-8").replace("6.0-12.0s", "7.0-12.0s"), encoding="utf-8")
            done = run("check", str(p), "--json")
            self.assertEqual(done.returncode, 1)
            failed = {t["name"] for t in json.loads(done.stdout)["tests"] if t["status"] == "FAIL"}
            self.assertEqual(failed, {"timing"})


if __name__ == "__main__":
    unittest.main()
