"""Thinking engine of the kosif-superpowers skill (scripts/think.py) and its mental-model library."""
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
spec = importlib.util.spec_from_file_location("think", SCRIPT)
think = importlib.util.module_from_spec(spec)
spec.loader.exec_module(think)


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, timeout=120)


class ThinkTest(unittest.TestCase):
    def test_model_library_is_complete(self):
        models = json.loads((SKILL / "data" / "mental_models.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(models), 60)
        ids = [m["id"] for m in models]
        self.assertEqual(len(ids), len(set(ids)))
        for m in models:
            with self.subTest(model=m["id"]):
                for k in ("name_en", "name_ar", "discipline", "question", "output", "pitfall"):
                    self.assertTrue(m[k])
                self.assertGreaterEqual(len(m["steps"]), 3)
                self.assertRegex(m["name_ar"], r"[؀-ۿ]")

    def test_ladder_levels(self):
        self.assertIn("L5", run("ladder", "Which is better for my project, Remotion or HyperFrames? choose one").stdout)
        self.assertIn("L3", run("ladder", "why does the render drop frames? debug it").stdout)
        self.assertIn("L6", run("ladder", "اقترح فكرة مبتكرة لحملة رمضان").stdout)

    def test_models_rank_arabic_with_prefixes(self):
        ids = [m["id"] for m in think.rank_models("مش متأكدين من التسعير والربح في السوق", 6)]
        self.assertIn("MODEL-55", ids)  # unit economics via "التسعير" → "تسعير"

    def test_decide_detects_flips(self):
        close = {"criteria": {"q": 1, "c": -1}, "scores": {"A": {"q": 4, "c": 2}, "B": {"q": 3, "c": 1}}}
        r = think.decide(close)
        self.assertEqual(r["totals"]["A"], r["totals"]["B"])
        clear = {"criteria": {"q": 3, "c": -1}, "scores": {"A": {"q": 5, "c": 1}, "B": {"q": 1, "c": 1}}}
        r = think.decide(clear)
        self.assertEqual(r["winner"], "A")
        self.assertTrue(r["robust"])

    def test_fermi_range_is_ordered(self):
        out = json.loads(run("fermi", "a*b", "--range", "a=1:10", "b=2:4", "--samples", "2000").stdout)
        self.assertLess(out["p10"], out["p50"])
        self.assertLess(out["p50"], out["p90"])
        self.assertGreaterEqual(out["p10"], 2.0)

    def test_fermi_refuses_attribute_access_and_calls(self):
        names = ["a", "__class__", "__base__", "__subclasses__", "__len__"]
        proc = run("fermi", "a.__class__.__base__.__subclasses__().__len__()", "--range", *[f"{n}=1:2" for n in names], "--samples", "3")
        self.assertEqual(proc.returncode, 2, proc.stdout)
        self.assertNotIn("p50", proc.stdout)
        ok = json.loads(run("fermi", "-a ** 2 + b / 4", "--range", "a=1:2", "b=4:8", "--samples", "100").stdout)
        self.assertLess(ok["p10"], 0)

    def test_critic_sees_through_tanween(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "ar.md"
            f.write_text("هذا جيد جدًا ويعمل دائمًا.\n", encoding="utf-8")
            out = run("critic", str(f)).stdout
        self.assertIn("جدا", out)
        self.assertIn("دائما", out)

    def test_fermi_rejects_code(self):
        self.assertEqual(run("fermi", "__import__('os')", "--range", "os=1:2").returncode, 2)

    def test_ideas_mix_near_and_far(self):
        out = run("ideas", "Arabic Friday reel", "-n", "4", "--seed", "3").stdout
        self.assertEqual(out.count("\n    + "), 4)

    def test_plan_and_frame_scaffolds(self):
        self.assertIn("kill / pivot", run("plan", "launch the course", "--weeks", "6").stdout)
        self.assertIn("done-criteria", run("frame", "a 15 s reel at 30 fps").stdout)

    def test_critic_flags(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("This is really the best, perfect solution. It should work, etc.\n")
        out = run("critic", f.name).stdout
        self.assertGreaterEqual(out.count("—"), 4)


if __name__ == "__main__":
    unittest.main()
