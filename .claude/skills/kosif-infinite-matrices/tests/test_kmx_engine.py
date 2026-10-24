"""Tests for the KOSIF Infinite Matrices engine, memory, sources and code-brick data.

Fast by default (small grid / short run). The full recipe experiment is exercised with a
reduced seed list so CI stays under a minute. Rendering is not tested here (needs Chromium).
"""
import copy
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import kmx_engine as E  # noqa: E402
import kmx_memory as M  # noqa: E402

RECIPE = ROOT / "recipes" / "glass-remembers-light.json"
CATALOG = json.loads((ROOT / "data" / "86_style_research_database.json").read_text(encoding="utf-8"))["styles"]


def small(rec):
    r = copy.deepcopy(rec)
    r["grid"] = {"w": 24, "h": 14}
    r["particles"] = 40
    r["duration"] = 4.0
    r["stimulus"]["on"] = [0.0, 2.0]
    r["stimulus"]["center"] = [12.0, 7.0]
    r["stimulus"]["radius"] = [8.0, 4.0]
    r["stimulus"]["period"] = 2.0
    r["structure"]["tiles"] = 8
    r["metrics"]["settle_after_off"] = 0.5
    return r


class TestRecipe(unittest.TestCase):
    def setUp(self):
        self.rec = E.load_recipe(RECIPE)

    def test_recipe_is_valid_against_86_index(self):
        self.assertEqual(E.validate_recipe(self.rec, CATALOG), [])

    def test_missing_brick_or_same_family_is_rejected(self):
        bad = copy.deepcopy(self.rec)
        del bad["bricks"]["feedback"]
        self.assertTrue(any("feedback" in e for e in E.validate_recipe(bad)))
        bad = copy.deepcopy(self.rec)
        bad["parents"][1]["family"] = bad["parents"][0]["family"]
        self.assertTrue(any("famil" in e for e in E.validate_recipe(bad)))

    def test_unknown_operator_is_rejected(self):
        bad = copy.deepcopy(self.rec)
        bad["parents"][0]["operator"] = "teleport"
        self.assertTrue(any("not tagged" in e for e in E.validate_recipe(bad, CATALOG)))

    def test_hash_ignores_labels_but_not_physics(self):
        a = copy.deepcopy(self.rec); a["title_en"] = "renamed"
        self.assertEqual(E.recipe_hash(a), E.recipe_hash(self.rec))
        b = copy.deepcopy(self.rec); b["memory"]["decay"] = 0.5
        self.assertNotEqual(E.recipe_hash(b), E.recipe_hash(self.rec))


class TestCausality(unittest.TestCase):
    def setUp(self):
        self.rec = small(E.load_recipe(RECIPE))

    def test_deterministic(self):
        a = E.simulate(self.rec, "A_full")["particles"][-1]
        b = E.simulate(self.rec, "A_full")["particles"][-1]
        self.assertEqual(a, b)

    def test_b_has_identical_memory_and_c_has_none_after_off(self):
        runs, ref, m = E.run_conditions(self.rec)
        self.assertTrue(m["B_no_coupling"]["same_memory_as_A"])
        self.assertEqual(m["C_no_memory"]["memory_after_off"], 0)
        self.assertGreater(m["A_full"]["memory_after_off"], 0)
        self.assertNotEqual(runs["A_full"]["particles"][-1], runs["B_no_coupling"]["particles"][-1])

    def test_memory_persists_and_decays_after_beam_off(self):
        mem = E.memory_frames(self.rec)
        off = int(self.rec["stimulus"]["on"][1] * self.rec["fps"])
        self.assertGreater(sum(mem[off + 5]), 0)
        self.assertLess(sum(mem[-1]), sum(mem[off]))

    def test_no_light_written_means_no_memory(self):
        r = copy.deepcopy(self.rec); r["memory"]["write"] = 0.0
        self.assertTrue(all(v == 0 for v in E.memory_frames(r)[-1]))

    def test_lead_lines_block_diffusion_between_tiles(self):
        # light only inside one tile: after diffusion, every other tile must still hold zero memory
        r = copy.deepcopy(self.rec)
        tile, absorb = E.build_tiles(r)
        W = r["grid"]["w"]
        target = tile[7 * W + 12]
        mask = [1.0 if t == target else 0.0 for t in tile]
        orig = E.light_field
        try:
            E.light_field = lambda rec, t: [m * orig(rec, t)[i] if orig(rec, t) else 0.0 for i, m in enumerate(mask)] if E.beam_on(rec, t) else None
            mem = E.memory_frames(r, (tile, absorb))
        finally:
            E.light_field = orig
        self.assertGreater(sum(v for v, t in zip(mem[-1], tile) if t == target), 0)  # the lit tile did store light
        self.assertTrue(all(v == 0 for v, t in zip(mem[-1], tile) if t != target))

    def test_full_recipe_confirms_with_reduced_seeds(self):
        rec = E.load_recipe(RECIPE)
        report, _, _ = E.experiment(rec, seeds=[1, 2], dose=[0.0, 0.5, 1.0])
        self.assertEqual(report["verdict"], "CONFIRMED_IN_MODEL", report["checks"])
        self.assertGreater(report["effect"]["B_no_coupling"]["min"], 0.15)


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = pathlib.Path(self.tmp.name) / "ledger.jsonl"
        self.reg = pathlib.Path(self.tmp.name) / "registry.json"

    def tearDown(self):
        self.tmp.cleanup()

    def report(self):
        return {"recipe_id": "KMX-R-T", "recipe_hash": "abc", "verdict": "CONFIRMED_IN_MODEL", "status": "NUMERIC_TESTED",
                "checks": {"x": True}, "effect": {}, "dose_response": {"spearman_rho": 1.0}, "roles": {"structure": "tessellate"}}

    def test_chain_and_no_duplicate_experiment(self):
        e1 = M.record_experiment(self.report(), {}, path=self.ledger)
        self.assertEqual(e1["id"], "EXP-0001")
        with self.assertRaises(ValueError):
            M.record_experiment(self.report(), {}, path=self.ledger)
        e2 = M.record_experiment(self.report(), {}, path=self.ledger, replication=True)
        self.assertEqual((e2["type"], e2["replicates"]), ("replication", "EXP-0001"))
        self.assertTrue(M.verify_ledger(self.ledger)["ok"])

    def test_tampering_breaks_chain(self):
        M.record_experiment(self.report(), {}, path=self.ledger)
        M.record_rating("EXP-0001", 4, "tester", path=self.ledger)
        lines = self.ledger.read_text().splitlines()
        lines[0] = lines[0].replace("CONFIRMED_IN_MODEL", "NOT_CONFIRMED")
        self.ledger.write_text("\n".join(lines) + "\n")
        self.assertFalse(M.verify_ledger(self.ledger)["ok"])
        with self.assertRaises(RuntimeError):
            M.record_rating("EXP-0001", 5, "tester", path=self.ledger)

    def test_rating_needs_existing_experiment_and_name(self):
        with self.assertRaises(ValueError):
            M.record_rating("EXP-9999", 4, "x", path=self.ledger)
        M.record_experiment(self.report(), {}, path=self.ledger)
        with self.assertRaises(ValueError):
            M.record_rating("EXP-0001", 4, " ", path=self.ledger)
        M.record_rating("EXP-0001", 5, "king", path=self.ledger)
        self.assertGreater(M.operator_scores(self.ledger)["structure:tessellate"]["posterior_mean"], 0.5)

    def test_283_hypotheses_stay_untested_without_evidence(self):
        status, counts = M.hypothesis_status(self.ledger)
        self.assertEqual(counts, {"UNTESTED_UNRENDERED": 283})
        with self.assertRaises(ValueError):
            M.mark_hypothesis("KMX-SEED-001", "RENDER_TESTED", None, path=self.ledger)

    def test_duplicate_idea_signature_is_refused(self):
        seeds = json.loads(M.SEEDS.read_text(encoding="utf-8"))["hypotheses"]
        h = seeds[0]
        with self.assertRaises(ValueError):
            M.record_idea({"id": "X", "parents": [p["style_id"] for p in h["parents"]], "roles": h["roles"]}, path=self.ledger)

    def test_source_registry_dedupes_by_hash(self):
        f = pathlib.Path(self.tmp.name) / "a.txt"; f.write_text("same bytes")
        g = pathlib.Path(self.tmp.name) / "b.txt"; g.write_text("same bytes")
        s1, new1 = M.add_source("A", "core", "own", ["x"], file=f, path=self.reg)
        s2, new2 = M.add_source("B", "core", "own", ["y"], file=g, path=self.reg)
        self.assertTrue(new1); self.assertFalse(new2)
        self.assertEqual(s1["id"], s2["id"])
        self.assertEqual(sorted(s2["names"]), ["a.txt", "b.txt"])
        self.assertEqual(M.verify_source(g, path=self.reg)["id"], s1["id"])


class TestCommittedData(unittest.TestCase):
    def test_code_bricks_cover_86_with_rea(self):
        d = json.loads((ROOT / "data" / "86_style_code_bricks.json").read_text(encoding="utf-8"))
        self.assertEqual(d["style_count"], 86)
        self.assertEqual(sum(1 for s in d["styles"] if "rea" in s), 86)
        for s in d["styles"]:
            self.assertEqual(set(s["bricks"]), set(E.BRICKS))
        self.assertNotIn("function ", json.dumps(d))  # derived numbers only, no source text

    def test_committed_ledger_and_registry_are_consistent(self):
        chk = M.verify_ledger()
        self.assertTrue(chk["ok"], chk["problems"])
        exps = [e for e in M.read_ledger() if e["type"] == "experiment"]
        self.assertTrue(any(e["recipe_id"] == "KMX-R-0001" for e in exps))
        ids = {s["id"] for s in M.read_registry()["sources"]}
        for e in exps:
            self.assertTrue(set(e["sources"]) <= ids)
            base = ROOT.parents[2] / e["artifacts"]["dir"]
            for rel, digest in e["artifacts"]["sha256"].items():
                p = base / rel
                if p.exists():  # large media may be left out of a checkout
                    self.assertEqual(M.sha256_file(p), digest, rel)


if __name__ == "__main__":
    unittest.main()
