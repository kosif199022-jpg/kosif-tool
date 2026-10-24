"""Tests for the four typed causal laws ported from the owner's v0.2 causal studio (SRC-024)."""
import copy
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import kmx_laws as L  # noqa: E402
import kmx_memory as M  # noqa: E402

RECIPES = sorted((ROOT / "recipes" / "laws").glob("*.json"))
CATALOG = {s["style_id"] for s in json.loads((ROOT / "data" / "86_style_research_database.json").read_text(encoding="utf-8"))["styles"]}


class TestLaws(unittest.TestCase):
    def test_four_recipes_one_per_law(self):
        self.assertEqual(sorted(L.load_plan(p)["law"] for p in RECIPES), sorted(L.LAWS))

    def test_reproduces_owner_v02_receipts_exactly(self):
        for path in RECIPES:
            doc = json.loads(path.read_text(encoding="utf-8"))
            plan, want = doc["recipes"][0], doc["provenance"]["v0_2_demo_receipt"]
            with self.subTest(law=plan["law"]):
                self.assertEqual(L.digest(plan), want["recipe_sha256"])
                a, b, got = L.simulate(plan)
                self.assertEqual(got, want["metrics"])
                for label, hist, flag in (("a_coupled", a, True), ("b_control", b, False)):
                    for name, sha in want["frame_sha256"][label].items():
                        svg = L.frame_svg(hist, int(name[:3]), plan["law"], flag)
                        self.assertEqual(L.hashlib.sha256(svg.encode("utf8")).hexdigest(), sha)

    def test_parents_exist_in_86_index_and_sources_registered(self):
        ids = {s["id"] for s in M.read_registry()["sources"]}
        for path in RECIPES:
            doc = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(set(doc["provenance"]["parents_as_style_ids"]) <= CATALOG)
            self.assertIn(doc["provenance"]["source"], ids)

    def test_every_law_confirms_with_dose(self):
        for path in RECIPES:
            rep = L.experiment(L.load_plan(path), frames=16, n=32)
            with self.subTest(law=rep["law"]):
                self.assertEqual(rep["verdict"], "CONFIRMED_IN_MODEL", rep["checks"])
                self.assertEqual(rep["dose"][0]["mean_post_light_effect"], 0.0)

    def test_self_imprinting_isolates_the_write_edge(self):
        plan = L.load_plan(ROOT / "recipes" / "laws" / "self-imprinting.json")
        plan = copy.deepcopy(plan)
        plan["parameters"]["gain"] = 0.0
        _, _, m = L.simulate(plan, frames=16, n=32)
        self.assertFalse(m["effect_detected"])  # the field differs, but nothing reads it

    def test_validation(self):
        plan = L.load_plan(RECIPES[0])
        for key, val in (("law", "unimplemented"),):
            bad = copy.deepcopy(plan); bad[key] = val
            self.assertTrue(L.validate_plan(bad))
        for k, v in (("gain", 1.5), ("decay", 1.0), ("geometry", "torus"), ("gain", True)):
            bad = copy.deepcopy(plan); bad["parameters"][k] = v
            self.assertTrue(L.validate_plan(bad), (k, v))
        bad = copy.deepcopy(plan); bad["causal_contract"]["output"] = "Nothing"
        self.assertTrue(L.validate_plan(bad))
        with self.assertRaises(ValueError):
            L.simulate(plan, frames=4)

    def test_render_receipt_detects_tampering(self):
        plan = L.load_plan(ROOT / "recipes" / "laws" / "material-memory.json")
        with tempfile.TemporaryDirectory() as d:
            L.render(plan, d, frames=12, n=20)
            rep = pathlib.Path(d) / "report.json"
            self.assertTrue(L.verify_render(rep))
            f = pathlib.Path(d) / "a_coupled" / "011.svg"
            f.write_text(f.read_text() + " ")
            self.assertFalse(L.verify_render(rep))

    def test_197_atoms_are_concepts(self):
        atoms = L.atoms()
        self.assertEqual(len(atoms), 197)
        self.assertEqual(len({a["id"] for a in atoms}), 197)
        self.assertTrue(all(a["status"] == "CONCEPT_NOT_EXECUTABLE" for a in atoms))
        self.assertEqual(len({a["axis"] for a in atoms}), 12)


if __name__ == "__main__":
    unittest.main()
