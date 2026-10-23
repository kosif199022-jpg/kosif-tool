import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import drawing_methods as dm  # noqa: E402

FIELDS = ("id", "domain", "name_en", "name_ar", "books", "principle_ar", "principle_en", "steps", "code_recipe",
          "prompt_terms", "checks", "common_errors", "tags", "review_status")


class AtlasTests(unittest.TestCase):
    def setUp(self):
        self.data = dm.load_atlas()

    def test_cards_are_complete_and_sourced(self):
        books = dm.book_ids()
        ext = {b["id"] for b in self.data["external_books"]}
        levels = set(self.data["review_status_levels"])
        self.assertGreaterEqual(len(self.data["methods"]), 20)
        for m in self.data["methods"]:
            for k in FIELDS:
                self.assertTrue(m.get(k), f"{m['id']} lacks {k}")
            for b in m["books"]:
                self.assertIn(b, books | ext, f"{m['id']} names unknown book {b}")
            self.assertIn(m["review_status"], levels)
        for b in self.data["external_books"]:
            self.assertIn(b["review_status"], levels, b["id"])

    def test_status_never_claims_training_or_fulltext(self):
        self.assertIn("NOT_fulltext_review", self.data["status"])
        self.assertIn("NOT_model_training", self.data["status"])

    def test_arabic_requests_route_to_the_right_cards(self):
        cases = {"ارسم وش شخصية بتضحك": "DM-16", "عايز أرسم بورتريه وجه من زاوية": "DM-09",
                 "وضعية جسم ديناميكية وخط الفعل": "DM-06", "منظور ونقطة تلاشي للمدينة": "DM-05",
                 "draw a cute character with clear shape language": "DM-13", "ظل وإضاءة على كرة": "DM-19"}
        for q, want in cases.items():
            got = [r["id"] for r in dm.find(self.data, q, top=3)]
            self.assertIn(want, got, q)

    def test_plan_orders_stages_and_names_a_demo(self):
        p = dm.plan(self.data, "ارسم شخصية كرتونية طفل سعيد")
        self.assertEqual(p["kind"], "character")
        order = [s["stage"] for s in p["stages"]]
        self.assertEqual(order[0], "intent")
        self.assertEqual(order[-1], "verify")
        self.assertLessEqual(len(p["methods"]), 4)
        self.assertEqual(p["status"], "PLAN_ONLY_NOTHING_DRAWN")

    def test_prompt_uses_cards_and_rejects_unknown_ids(self):
        out = dm.prompt(self.data, "a brave girl", ["DM-13", "DM-16"])
        self.assertIn("clear shape language", out["prompt"])
        self.assertIn("no image model was called", out["note"])
        with self.assertRaises(ValueError):
            dm.prompt(self.data, "x", ["DM-99"])


class DrawTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SK / "scripts" / "drawing_methods.py"), *args],
                              capture_output=True, text=True)

    def test_every_kind_draws_and_passes_its_checks(self):
        variants = [("head",), ("head", "--yaw", "-45", "--pitch", "15"), ("figure",),
                    ("figure", "--pose", "action", "--heads", "7.5"), ("figure", "--pose", "stand", "--heads", "3"),
                    ("character",), ("character", "--shape", "triangle", "--age", "adult", "--expression", "angry"),
                    ("character", "--shape", "square", "--age", "elder", "--expression", "surprised"), ("forms",)]
        with tempfile.TemporaryDirectory() as tmp:
            for i, v in enumerate(variants):
                out = Path(tmp) / f"{i}.svg"
                r = self.run_cli("draw", *v, "--out", str(out))
                self.assertEqual(r.returncode, 0, r.stderr)
                res = dm.check_svg(out)
                self.assertEqual(res["status"], "PASS", (v, [c for c in res["checks"] if not c["pass"]]))
                for st in dm.STAGES:
                    self.assertIn(f'id="stage-{st}"', out.read_text(encoding="utf-8"))

    def test_output_is_deterministic(self):
        self.assertEqual(dm.draw_figure(8, "walk")[0], dm.draw_figure(8, "walk")[0])
        self.assertEqual(dm.draw_head(20, -10)[0], dm.draw_head(20, -10)[0])

    def test_check_catches_a_broken_proportion(self):
        svg = dm.draw_figure(8, "contrapposto")[0].replace('data-heads="8"', 'data-heads="6"', 1)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.svg"
            p.write_text(svg, encoding="utf-8")
            res = dm.check_svg(p)
            self.assertEqual(res["status"], "FAIL")
            self.assertFalse(next(c for c in res["checks"] if c["id"] == "heads-tall")["pass"])

    def test_refuses_overwrite_and_bad_parameters(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "a.svg"
            out.write_text("keep", encoding="utf-8")
            r = self.run_cli("draw", "forms", "--out", str(out))
            self.assertEqual(r.returncode, 2)
            self.assertEqual(out.read_text(encoding="utf-8"), "keep")
            r = self.run_cli("draw", "head", "--yaw", "120", "--out", str(Path(tmp) / "b.svg"))
            self.assertEqual(r.returncode, 2)
            self.assertIn("yaw", r.stderr)

    def test_cli_find_returns_json(self):
        r = self.run_cli("find", "تحبير وسمك الخط")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["results"][0]["id"], "DM-24")


if __name__ == "__main__":
    unittest.main()
