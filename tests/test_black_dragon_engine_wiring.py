"""The council and the book's trap scanner are reachable from the Black Dragon engine, not just present."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / ".claude/skills/kosif-black-dragon/scripts/black_dragon.py"
ADAPTERS = ROOT / ".claude/skills/kosif-superpowers/data/black_dragon_adapters.json"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class EngineWiring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bd = load(NATIVE, "_bd_native_wiring")

    def test_council_skill_has_a_reviewed_engine_adapter(self):
        raw = json.loads(ADAPTERS.read_text(encoding="utf-8"))
        ad = raw.get("adapters", raw)["skill:kosif-black-dragon"]
        self.assertEqual(ad["args"][0], "creative-council")
        self.assertTrue(ad["skill_program"])

    def test_thinking_guards_run_the_real_trap_scanner(self):
        g = self.bd.thinking_guards("anchor the price estimate from the first number the client said")
        ids = [x["id"] for x in g["gates"]]
        self.assertEqual(g["traps_catalogued"], 31)
        self.assertIn("tfs-anchoring", ids)
        self.assertTrue({"tfs-wysiati", "tfs-substitution", "tfs-optimism-overconfidence"} <= set(ids))
        hit = next(x for x in g["gates"] if x["id"] == "tfs-anchoring")
        self.assertIn("critic", hit["reviewers"])
        self.assertTrue(hit["pages"])

    def test_think_review_adds_the_book_trap_scan(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            brief = Path(d) / "brief.json"
            out = Path(d) / "review.json"
            brief.write_text(json.dumps({"goal": "pick an edit plan", "options": ["a", "b"]}), encoding="utf-8")
            import contextlib, io
            with contextlib.redirect_stdout(io.StringIO()):
                rc = self.bd.main(["think-review", "--input", str(brief), "--out", str(out)])
            self.assertEqual(rc, 0)
            review = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(len(review["review_checks"]), 11)
        self.assertEqual(review["book_trap_scan"]["traps_catalogued"], 31)
        self.assertGreaterEqual(len(review["book_trap_scan"]["gates"]), 3)


if __name__ == "__main__":
    unittest.main()
