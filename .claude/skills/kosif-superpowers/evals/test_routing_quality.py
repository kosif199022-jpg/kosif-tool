"""USIP v5.3 routing quality on the real catalog: the 10 requests of the routing audit, shadow cases for each defect found
by the audit and by the adversarial reviews, and a held-out set of fresh requests.

Cases live in evals/routing_cases.json. Superpowers are matched by case-insensitive substrings of name_en (SP ids are
positional and change on rebuild). Every brief is built once per run.
"""
import json, sys, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import skill_intelligence as S  # noqa: E402

DATA = json.loads((SK / "evals" / "routing_cases.json").read_text(encoding="utf-8"))
CASES = {c["id"]: c for c in DATA["cases"]}
_BRIEFS = {}


def brief(case):
    if case["id"] not in _BRIEFS:
        _BRIEFS[case["id"]] = S.build_brief(case["request"])
    return _BRIEFS[case["id"]]


def has(names, keyword):
    k = keyword.lower()
    return [n for n in names if k in n.lower()]


def bc_rule(b):
    """Contract §1: C is a different method, not B plus extras. Returns a reason string when the rule is broken."""
    p = b["plans"]
    ids = {k: {x["id"] for x in v["superpowers"]} for k, v in p.items()}
    if p["C"].get("unavailable"):
        return None if not ids["C"] else "an unavailable C lists superpowers"
    if p["C"].get("depth_of") == "B":
        return None if ids["C"] != ids["B"] else "C labelled a depth level of B is B itself"
    fixed = {i for m in b["must_have_coverage"] for i in m["superpowers"]} | {v["id"] for v in b["verifiers"]}
    b_core, c_core = ids["B"] - fixed, ids["C"] - fixed
    if not c_core - ids["B"]:
        return "C has no pick of its own"
    if 2 * len(b_core & c_core) > len(b_core):
        return f"C keeps {len(b_core & c_core)} of B's {len(b_core)} own picks (B plus extras)"
    if ids["B"] <= ids["C"]:
        return "C is a superset of B"
    return None


class RoutingQuality(unittest.TestCase):
    maxDiff = None

    def check(self, case):
        e = case["expect"]
        if case["brief"]:
            b = brief(case)
            an = b["analysis"]
        else:
            b, an = None, S.analyse(case["request"])
        tag = f'{case["id"]}: {case["request"]}'
        if "primary" in e:
            self.assertEqual(an["primary"], e["primary"], tag)
        if "primary_in" in e:
            self.assertIn(an["primary"], e["primary_in"], tag)
        if "primary_not" in e:
            self.assertNotEqual(an["primary"], e["primary_not"], tag)
        if "level_in" in e:
            self.assertIn(an["level"], e["level_in"], tag)
        for lv in e.get("level_not", []):
            self.assertNotEqual(an["level"], lv, tag)
        if "ambition_not" in e:
            self.assertNotEqual(an["ambition"], e["ambition_not"], tag)
        if "style_includes" in e:
            self.assertIn(e["style_includes"], an["style"], tag)
        if "intent" in e:
            self.assertEqual(an["intent"], e["intent"], tag)
        if "silent" in e:
            self.assertEqual(an["silent"], e["silent"], tag)
        for key, field in (("own_voice", "voice"), ("own_footage", "footage")):
            if key in e:
                self.assertEqual(an["constraints"]["own_assets"][field], e[key], tag)
        for d in e.get("deliverables_exclude", []):
            self.assertNotIn(d, an["deliverables"], tag)
        for d in e.get("deliverables_include", []):
            self.assertIn(d, an["deliverables"], tag)
        needs = [m["need"] for m in an["must_haves"]]
        for pre in e.get("must_haves_include", []):
            self.assertTrue(any(n.startswith(pre) for n in needs), (tag, pre, needs))
        for pre in e.get("must_haves_exclude", []):
            self.assertFalse(any(n.startswith(pre) for n in needs), (tag, pre, needs))
        qs = [q["question"] for q in an["questions"]]
        for k in e.get("questions_include", []):
            self.assertTrue(has(qs, k), (tag, k, qs))
        for k in e.get("questions_exclude", []):
            self.assertFalse(has(qs, k), (tag, k, qs))
        if b is None:
            return
        rec = b["recommended"]
        rec_names = [x["name_en"] for x in b["plans"][rec]["superpowers"]] if rec else []
        all_names = [x["name_en"] for p in b["plans"].values() for x in p["superpowers"]]
        names_of = {x["id"]: x["name_en"] for x in b["shortlist"]}
        if e.get("excluded_empty"):
            self.assertEqual(b["excluded"], [], tag)
        for pre, st in e.get("must_status", {}).items():
            self.assertEqual(next(m for m in b["must_have_coverage"] if m["need"].startswith(pre))["status"], st, (tag, pre))
        for pre, bad in e.get("must_pick_exclude", {}).items():
            cov = next(m for m in b["must_have_coverage"] if m["need"].startswith(pre))
            self.assertEqual(cov["status"], "covered", (tag, pre))
            picks = [names_of.get(i, i) for i in cov["superpowers"]]
            for k in bad:
                self.assertFalse(has(picks, k), (tag, pre, k, picks))
        if e.get("rec_include_any"):
            self.assertTrue(any(has(rec_names, k) for k in e["rec_include_any"]), (tag, rec, e["rec_include_any"], rec_names))
        # A superpower's display name is its medoid member, which can flip between near-tied members when the
        # catalog grows; "the plan includes X" therefore also counts the members the brief says it matched.
        rec_seen = rec_names + [c for x in b["plans"][rec]["superpowers"] for c in x.get("contains", [])] if rec else []
        for k in e.get("rec_include_all", []):
            self.assertTrue(has(rec_seen, k), (tag, rec, k, rec_seen))
        for k in e.get("rec_exclude", []):
            self.assertFalse(has(rec_names, k), (tag, rec, k))
        if e.get("rec_verify_include_any"):
            ver_stage = [x["name_en"] for x in b["plans"][rec]["superpowers"] if x["stage"] == "verify"]
            self.assertTrue(any(has(ver_stage, k) for k in e["rec_verify_include_any"]), (tag, ver_stage))
        for k in e.get("all_plans_exclude", []):
            self.assertFalse(has(all_names, k), (tag, k))
        for g in e.get("plans_exclude_groups", []):
            self.assertFalse([x["name_en"] for p in b["plans"].values() for x in p["superpowers"] if x["group"] == g], (tag, g))
        ver = [v["name_en"] for v in b["verifiers"]]
        for k in e.get("verifiers_exclude", []):
            self.assertFalse(has(ver, k), (tag, k, ver))
        if e.get("verifiers_include_any"):
            self.assertTrue(any(has(ver, k) for k in e["verifiers_include_any"]), (tag, ver))
        if e.get("shortlist_top_include_any"):
            top = [n for x in b["shortlist"][:e["shortlist_top_include_any"]["n"]] for n in [x["name_en"], *x.get("contains", [])]]
            self.assertTrue(any(has(top, k) for k in e["shortlist_top_include_any"]["any"]), (tag, top))
        if "recommended_not" in e:
            self.assertNotEqual(rec, e["recommended_not"], tag)
        if "reason_not_contains" in e:
            self.assertNotIn(e["reason_not_contains"], b["recommended_reason"], tag)
        if b["plans"]:
            self.assertIsNone(bc_rule(b), tag)
            for k in "ABC":
                self.assertEqual(b["plans"][k]["definition"], S.PLAN_DEFINITIONS[k])
                if not b["plans"][k].get("unavailable"):
                    self.assertTrue(b["plans"][k]["meets_must_haves"], (tag, k))

    def test_aggregate_precision_of_recommended_plans(self):
        """Clearly-irrelevant picks (curated name keywords) across the recommended plans of every labelled case."""
        total, hits = 0, []
        for c in DATA["cases"]:
            if not c.get("irrelevant"):
                continue
            b = brief(c)
            names = [x["name_en"] for x in b["plans"][b["recommended"]]["superpowers"]]
            total += len(names)
            hits += [(c["id"], n) for n in names if any(k.lower() in n.lower() for k in c["irrelevant"])]
        self.assertLessEqual(len(hits), DATA["aggregate"]["max_irrelevant_in_recommended_plans"], hits)
        self.assertGreater(total, 0)

    def test_aggregate_heldout_offdomain_groups(self):
        """Held-out requests (labels written before their briefs were inspected): picks from off-domain groups."""
        total, hits = 0, []
        for c in DATA["cases"]:
            if not c.get("heldout"):
                continue
            b = brief(c)
            for x in b["plans"][b["recommended"]]["superpowers"] if b["recommended"] else []:
                total += 1
                if x["group"] in c["irrelevant_groups"]:
                    hits.append((c["id"], x["group"], x["name_en"]))
        self.assertLessEqual(len(hits), DATA["aggregate"]["max_offgroup_in_heldout_recommended_plans"], hits)
        self.assertGreater(total, 0)


def _make(case):
    def t(self):
        self.check(case)
    t.__doc__ = f'{case["id"]}: {case.get("defect") or case["request"]}'
    return t


for _c in DATA["cases"]:
    setattr(RoutingQuality, f'test_{_c["id"]}', _make(_c))


if __name__ == "__main__":
    unittest.main()
