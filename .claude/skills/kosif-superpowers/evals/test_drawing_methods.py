import json
import re
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
        ext = {b["id"] for b in self.data["external_books"]} | {b["id"] for b in self.data["user_library"]}
        levels = set(self.data["review_status_levels"])
        self.assertGreaterEqual(len(self.data["methods"]), 20)
        for m in self.data["methods"]:
            for k in FIELDS:
                self.assertTrue(m.get(k), f"{m['id']} lacks {k}")
            for b in m["books"]:
                self.assertIn(b, books | ext, f"{m['id']} names unknown book {b}")
            self.assertIn(m["review_status"], levels)
        for b in self.data["external_books"] + self.data["user_library"]:
            self.assertIn(b["review_status"], levels, b["id"])

    def test_status_never_claims_training_or_copied_text(self):
        self.assertIn("NOT_fulltext_copy", self.data["status"])
        self.assertIn("NOT_model_training", self.data["status"])

    def test_user_library_is_metadata_only_and_read_cards_cite_it(self):
        lib = {b["id"]: b for b in self.data["user_library"]}
        self.assertGreaterEqual(len(lib), 40)
        for b in lib.values():
            self.assertEqual(set(b) - {"id", "title", "author", "pages", "read_via", "index_id", "review_status"}, set(), b["id"])
        index = dm.book_ids()
        for b in lib.values():
            if "index_id" in b:
                self.assertIn(b["index_id"], index, b["id"])
        read = [m for m in self.data["methods"] if m["review_status"] == "user_copy_read_paraphrased"]
        self.assertGreaterEqual(len(read), 20)
        mapped = {b["index_id"] for b in lib.values() if "index_id" in b}
        for m in read:
            self.assertTrue(any(b in lib or b in mapped for b in m["books"]), m["id"])
        cited = {b for m in self.data["methods"] for b in m["books"]}
        unused = [i for i, b in lib.items() if i not in cited and b.get("index_id") not in cited]
        self.assertEqual(unused, [], "every book read must feed at least one card")

    def test_every_card_is_reachable_from_the_pipeline(self):
        staged = {mid for st in self.data["pipeline"] for mid in st["methods"]}
        self.assertEqual([m["id"] for m in self.data["methods"] if m["id"] not in staged and int(m["id"][3:]) > 26], [])

    def test_arabic_requests_route_to_the_right_cards(self):
        cases = {"ارسم وش شخصية بتضحك": "DM-16", "عايز أرسم بورتريه وجه من زاوية": "DM-09",
                 "وضعية جسم ديناميكية وخط الفعل": "DM-06", "منظور ونقطة تلاشي للمدينة": "DM-05",
                 "draw a cute character with clear shape language": "DM-13", "ظل وإضاءة على كرة": "DM-19",
                 "عايز أعمل انيميشن كرة بتنط": "DM-27", "توقيت الحركة والإطارات": "DM-28", "ارسم ظل ساقط لصندوق من مصباح": "DM-32",
                 "شعر أنمي بيطير في الهوا": "DM-35", "تلوين بشرة أنمي": "DM-36", "رسم شارع ومباني": "DM-37",
                 "ارسم وردة": "DM-38", "تهشير بالحبر": "DM-33", "شخص بيجري للأمام": "DM-29"}
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
                    ("character", "--shape", "square", "--age", "elder", "--expression", "surprised"), ("forms",),
                    ("bounce",), ("bounce", "--frames", "9", "--bounce-height", "0.3"), ("shadow",),
                    ("shadow", "--light-x", "0.85", "--light-height", "0.3")]
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

    def test_check_catches_lost_volume_and_a_wrong_shadow(self):
        svg = dm.draw_bounce()[0]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "b.svg"
            p.write_text(re.sub(r'rx="([\d.]+)"(?=[^>]*data-part="ball" data-frame="3")',
                                lambda m: f'rx="{float(m.group(1)) * 1.3}"', svg, count=1), encoding="utf-8")
            res = dm.check_svg(p)
            self.assertFalse(next(c for c in res["checks"] if c["id"] == "volume-preserved")["pass"])
            svg = dm.draw_shadow()[0]
            moved = re.sub(r'(<circle class="sh" cx=")([\d.]+)', lambda m: m.group(1) + str(float(m.group(2)) + 25), svg, count=1)
            p.write_text(moved, encoding="utf-8")
            res = dm.check_svg(p)
            self.assertFalse(next(c for c in res["checks"] if c["id"] == "shadow-rays-meet")["pass"])

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
