#!/usr/bin/env python3
"""Regression tests for scripts/council.py (KOSIF Pro Council, USIP appendix A13). Temp dirs only."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "council.py"


def run(*args, ok=True):
    r = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True, timeout=120)
    if ok and r.returncode != 0:
        raise AssertionError(f"{args} -> {r.returncode}\n{r.stderr}")
    return r


R1 = {"position": "p", "claims": [{"claim": "c", "evidence": "ran verify_video.py", "confidence": 0.7}], "proposal": "x", "risks": ["r"]}
R2 = {"attacks": [{"target": "M1", "claim": "c", "counter": "k", "evidence": "test"}], "steelman": {"target": "M3", "why_strong": "w"}, "concessions": []}


def r3(scores, objection="none"):
    return {"final_proposal": "f", "scores": scores, "changed_mind": "none", "remaining_objection": objection}


class CouncilTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.dir = str(self.root / "council")

    def put(self, name, obj):
        p = self.root / name
        p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return str(p)

    def full_run(self, scores_by_member, objections=None, simulated=False):
        run("plan", "اعمل ريلز موشن عربي", "--dir", self.dir, "--options", "A,B,C")
        extra = ["--simulated"] if simulated else []
        for rnd, body in ((1, R1), (2, R2)):
            for m in ("M1", "M2", "M3", "M4", "M5"):
                run("ingest", "--dir", self.dir, "--round", str(rnd), "--member", m, "--file", self.put(f"{m}{rnd}.json", body), *extra)
        for m, sc in scores_by_member.items():
            obj = r3(sc, (objections or {}).get(m, "none"))
            run("ingest", "--dir", self.dir, "--round", "3", "--member", m, "--file", self.put(f"{m}3.json", obj), *extra)
        return json.loads(run("verdict", "--dir", self.dir).stdout)

    def test_plan_has_five_opposing_members_and_specialists(self):
        out = json.loads(run("plan", "اعمل ريلز موشن جرافيك عربي على صوتي", "--dir", self.dir).stdout)
        self.assertEqual(len(out["members"]), 5)
        c = json.loads((Path(self.dir) / "council.json").read_text(encoding="utf-8"))
        self.assertEqual(len({m["lane"] for m in c["roster"]}), 5, "each member owns a different evidence lane")
        self.assertEqual(c["options"], ["A", "B", "C"])

    def test_round_order_and_isolation(self):
        run("plan", "سؤال", "--dir", self.dir)
        r = run("prompts", "--dir", self.dir, "--round", "2", ok=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("ROUND_INCOMPLETE", r.stderr)
        run("prompts", "--dir", self.dir, "--round", "1")
        p1 = json.loads((Path(self.dir) / "prompts_r1.json").read_text(encoding="utf-8"))
        self.assertNotIn("other members' round-1 answers", p1["M1"])

    def test_invalid_member_answers_are_refused(self):
        run("plan", "سؤال", "--dir", self.dir)
        bad = run("ingest", "--dir", self.dir, "--round", "1", "--member", "M1", "--file", self.put("b.json", {"position": "p"}), ok=False)
        self.assertIn("MEMBER_INVALID", bad.stderr)
        unknown = run("ingest", "--dir", self.dir, "--round", "1", "--member", "M9", "--file", self.put("u.json", R1), ok=False)
        self.assertIn("UNKNOWN_MEMBER", unknown.stderr)
        leak = dict(R1, proposal="use api_key=" + "sk-" + "ant-" + "Q7x9" * 6 + " here")
        sec = run("ingest", "--dir", self.dir, "--round", "1", "--member", "M1", "--file", self.put("s.json", leak), ok=False)
        self.assertIn("SECRET", sec.stderr)

    def test_verdict_scores_records_dissent_and_receipt(self):
        scores = {"M1": {"A": 2, "B": 4, "C": 5}, "M2": {"A": 3, "B": 5, "C": 2}, "M3": {"A": 4, "B": 5, "C": 1},
                  "M4": {"A": 3, "B": 4, "C": 4}, "M5": {"A": 5, "B": 4, "C": 2}}
        v = self.full_run(scores, {"M2": "the sync is not measured"})
        self.assertEqual(v["status"], "COUNCIL_RUN")
        self.assertEqual(v["winner"], "B")
        self.assertEqual(v["totals"]["B"], 22.0)
        self.assertEqual(v["dissent"], [{"member": "M2", "objection": "the sync is not measured"}])
        self.assertEqual(len(v["rounds_sha256"]), 64)
        self.assertTrue((Path(self.dir) / "minutes.md").read_text(encoding="utf-8").startswith("# محضر المجلس"))

    def test_no_dissent_and_simulated_are_labelled(self):
        same = {m: {"A": 3, "B": 3, "C": 3} for m in ("M1", "M2", "M3", "M4", "M5")}
        v = self.full_run(same, simulated=True)
        self.assertEqual(v["status"], "COUNCIL_SIMULATED")
        self.assertTrue(any(w.startswith("NO_DISSENT") for w in v["warnings"]))
        self.assertTrue(any(w.startswith("CLOSE_CALL") for w in v["warnings"]))

    def test_incomplete_council_is_not_a_run(self):
        run("plan", "سؤال", "--dir", self.dir)
        r = run("verdict", "--dir", self.dir, ok=False)
        self.assertIn("ROUND_INCOMPLETE", r.stderr)

    def test_roster_of_100_unique_personas(self):
        doc = json.loads((SCRIPT.parents[1] / "data" / "council_100.json").read_text(encoding="utf-8"))
        ps = doc["personas"]
        self.assertEqual(doc["schema"], "kosif.council-personas.v1")
        self.assertEqual(len(ps), 100)
        for key in ("id", "name_ar", "name_en", "title_ar", "title_en", "character_ar", "lens_en", "blind_spot"):
            self.assertEqual(len({p[key] for p in ps}), 100, f"{key} must be unique")
        lanes = {}
        for p in ps:
            lanes[p["lane"]] = lanes.get(p["lane"], 0) + 1
            self.assertEqual(len(p["superpowers"]), 3)
            self.assertEqual(len(p["signature_questions"]), 3)
            self.assertGreaterEqual(len(p["character_ar"]), 120, p["id"])
            self.assertIn(p["counterpart"], {q["id"] for q in ps})
            self.assertNotEqual(p["counterpart"], p["id"])
        self.assertEqual(lanes, {l: 20 for l in ("cross_domain", "verification", "feasibility", "audience", "guardrails")})
        powers = [x for p in ps for x in p["superpowers"]]
        self.assertEqual(len(set(powers)), 300, "every superpower is distinct")

    def test_seats_pick_a_task_fitted_council_with_every_lane(self):
        out = json.loads(run("plan", "اعمل ريلز موشن جرافيك عربي على صوتي للتيك توك", "--dir", self.dir, "--seats", "7").stdout)
        self.assertEqual((out["mode"], out["seats"]), ("seats", 7))
        c = json.loads((Path(self.dir) / "council.json").read_text(encoding="utf-8"))
        self.assertEqual(len({m["lane"] for m in c["roster"]}), 5)
        self.assertEqual([m["id"] for m in c["roster"]], [f"M{i}" for i in range(1, 8)])
        self.assertTrue(all(m["persona_id"].startswith("P") for m in c["roster"]))
        again = self.root / "again"
        run("plan", "اعمل ريلز موشن جرافيك عربي على صوتي للتيك توك", "--dir", str(again), "--seats", "7")
        c2 = json.loads((again / "council.json").read_text(encoding="utf-8"))
        self.assertEqual([m["persona_id"] for m in c["roster"]], [m["persona_id"] for m in c2["roster"]], "deterministic")
        run("prompts", "--dir", self.dir, "--round", "1")
        p1 = json.loads((Path(self.dir) / "prompts_r1.json").read_text(encoding="utf-8"))
        self.assertIn("7-member KOSIF Pro council", p1["M1"])
        self.assertIn("Your known blind spot", p1["M1"])
        self.assertIn("signature questions", p1["M1"])

    def test_seat_limits_picks_and_full_council(self):
        r = run("plan", "x", "--dir", self.dir, "--seats", "3", ok=False)
        self.assertIn("SEATS_RANGE", r.stderr)
        r = run("plan", "x", "--dir", self.dir, "--seats", "7", "--full", ok=False)
        self.assertIn("MODE_CONFLICT", r.stderr)
        r = run("plan", "x", "--dir", self.dir, "--personas", "P001,P999,P003,P004,P005", ok=False)
        self.assertIn("UNKNOWN_PERSONA", r.stderr)
        out = json.loads(run("plan", "x", "--dir", self.dir, "--personas", "P001,P021,P041,P061,P081").stdout)
        self.assertEqual(out["mode"], "picked")
        full = self.root / "full"
        out = json.loads(run("plan", "قرار كبير", "--dir", str(full), "--full", "--no-roster").stdout)
        self.assertEqual((out["mode"], out["seats"]), ("full", 100))

    def test_large_council_round_two_uses_a_digest_and_names_the_counterpart(self):
        run("plan", "قرار", "--dir", self.dir, "--seats", "11", "--no-roster")
        c = json.loads((Path(self.dir) / "council.json").read_text(encoding="utf-8"))
        ids = [m["id"] for m in c["roster"]]
        long_r1 = dict(R1, risks=["r" * 50] * 5)
        for m in ids:
            run("ingest", "--dir", self.dir, "--round", "1", "--member", m, "--file", self.put(f"{m}.json", long_r1))
        run("prompts", "--dir", self.dir, "--round", "2")
        p2 = json.loads((Path(self.dir) / "prompts_r2.json").read_text(encoding="utf-8"))
        self.assertNotIn("r" * 50, p2["M1"], "large councils see a digest of round 1")
        for m in ids:
            run("ingest", "--dir", self.dir, "--round", "2", "--member", m, "--file", self.put(f"{m}2.json", R2))
        for i, m in enumerate(ids):
            run("ingest", "--dir", self.dir, "--round", "3", "--member", m,
                "--file", self.put(f"{m}3.json", r3({"A": 3, "B": 4 if i % 2 else 3, "C": 2}, "risk" if i == 0 else "none")))
        v = json.loads(run("verdict", "--dir", self.dir).stdout)
        self.assertEqual((v["seats"], v["mode"], v["winner"]), (11, "seats", "B"))
        self.assertEqual(len(v["personas"]), 11)

    def test_personas_command(self):
        out = json.loads(run("personas").stdout)
        self.assertEqual(out["count"], 100)
        one = json.loads(run("personas", "--id", "p021").stdout)
        self.assertEqual(one["lane"], "verification")
        fit = json.loads(run("personas", "--find", "راجع أمان الكود وتسريب المفاتيح", "--seats", "6").stdout)
        self.assertEqual(fit["seats"], 6)
        self.assertTrue(any("P083" in row for row in fit["council"]), "the secrets keeper sits on a secrets question")


if __name__ == "__main__":
    unittest.main()
