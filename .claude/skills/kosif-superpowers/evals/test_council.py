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


    # ------------------------------------------------------------------ devil's advocate, groupthink, calibration, lenses
    DEVIL = {"target_option": "B",
             "steelman": "B ships the Arabic reel this week with the measured sync tool already installed on this machine.",
             "failure_modes": [
                 {"mode": "the voice drifts out of sync after minute 1", "likelihood": 3, "impact": 5, "test": "verify_video.py on a 90 s cut", "evidence": "opinion"},
                 {"mode": "the font licence forbids commercial reels", "likelihood": 2, "impact": 4, "test": "read the font licence file", "evidence": "fonts/LICENSE"},
                 {"mode": "TikTok crops the captions", "likelihood": 4, "impact": 4, "test": "export a 9:16 frame and check safe zones", "evidence": "opinion"}],
             "premortem": "It is six months later and B failed because the captions were cropped on every phone and nobody checked.",
             "kill_criterion": "drop B if the sync drift exceeds 80 ms on the 90 s test cut"}

    def rounds_1_2(self, r1=R1, simulated=False):
        run("plan", "اعمل ريلز موشن عربي", "--dir", self.dir, "--options", "A,B,C")
        extra = ["--simulated"] if simulated else []
        for rnd, body in ((1, r1), (2, R2)):
            for m in ("M1", "M2", "M3", "M4", "M5"):
                run("ingest", "--dir", self.dir, "--round", str(rnd), "--member", m, "--file", self.put(f"{m}{rnd}.json", body), *extra)

    def round3(self, scores, objections=None, answers=None):
        for m, sc in scores.items():
            obj = r3(sc, (objections or {}).get(m, "none"))
            if answers and m in answers:
                obj["devil_answers"] = answers[m]
            run("ingest", "--dir", self.dir, "--round", "3", "--member", m, "--file", self.put(f"{m}3.json", obj))
        return json.loads(run("verdict", "--dir", self.dir).stdout)

    SCORES = {"M1": {"A": 2, "B": 4, "C": 5}, "M2": {"A": 3, "B": 5, "C": 2}, "M3": {"A": 4, "B": 5, "C": 1},
              "M4": {"A": 3, "B": 4, "C": 4}, "M5": {"A": 5, "B": 4, "C": 2}}

    def test_devil_prompt_contract_and_validation(self):
        run("plan", "سؤال", "--dir", self.dir, "--options", "A,B,C")
        r = run("devil", "--dir", self.dir, ok=False)
        self.assertIn("ROUND_INCOMPLETE", r.stderr, "the devil needs round 1 first")
        for m in ("M1", "M2", "M3", "M4", "M5"):
            run("ingest", "--dir", self.dir, "--round", "1", "--member", m, "--file", self.put(f"{m}.json", dict(R1, top_choice="B" if m != "M5" else "A")))
        out = json.loads(run("devil", "--dir", self.dir).stdout)
        self.assertEqual((out["devil"], out["leading_option"], out["basis"]), ("M2", "B", "round-1 top choices"))
        prompt = json.loads((Path(self.dir) / "prompts_devil.json").read_text(encoding="utf-8"))["M2"]
        for need in ("steelman the leading option", "likelihood and impact", "DISCONFIRM", "six months later", "kill criterion"):
            self.assertIn(need, prompt)
        self.assertLess(prompt.index("steelman"), prompt.index("failure modes"), "steelman comes before the attack")
        bad = dict(self.DEVIL, steelman="weak", failure_modes=self.DEVIL["failure_modes"][:2], kill_criterion="")
        r = run("devil", "--dir", self.dir, "--file", self.put("bad.json", bad), ok=False)
        self.assertIn("DEVIL_INVALID", r.stderr)
        for frag in ("steelman", "at least 3", "kill_criterion"):
            self.assertIn(frag, r.stderr)
        worse = dict(self.DEVIL, failure_modes=[dict(f, likelihood=9) for f in self.DEVIL["failure_modes"]])
        self.assertIn("likelihood must be an integer from 1 to 5", run("devil", "--dir", self.dir, "--file", self.put("w.json", worse), ok=False).stderr)
        ok = json.loads(run("devil", "--dir", self.dir, "--file", self.put("d.json", self.DEVIL)).stdout)
        self.assertEqual(ok["strongest_objection"], "TikTok crops the captions", "ranked by likelihood x impact (16 > 15 > 8)")
        self.assertEqual([x.split(".")[0] for x in ok["ranked"]], ["1", "2", "3"])
        self.assertEqual(ok["warnings"], [])

    def test_unanswered_strongest_objection_blocks_a_clean_pass(self):
        self.rounds_1_2()
        run("devil", "--dir", self.dir, "--file", self.put("d.json", self.DEVIL))
        run("prompts", "--dir", self.dir, "--round", "3")
        p3 = json.loads((Path(self.dir) / "prompts_r3.json").read_text(encoding="utf-8"))
        self.assertIn("devil_answers", p3["M1"])
        self.assertIn("TikTok crops the captions", p3["M1"])
        v = self.round3(self.SCORES, {"M2": "the sync is not measured"})
        self.assertEqual(v["status"], "COUNCIL_CONTESTED")
        self.assertFalse(v["clean_pass"])
        self.assertIn("UNANSWERED_OBJECTION", v["clean_pass_blockers"])
        self.assertEqual([u["rank"] for u in v["devil"]["unanswered"]], [1, 2, 3])
        self.assertEqual(v["winner"], "B", "the vote itself is unchanged")
        minutes = (Path(self.dir) / "minutes.md").read_text(encoding="utf-8")
        self.assertIn("## الخلاصة", minutes)
        self.assertIn("بلا جواب", minutes)
        self.assertIn("معيار الإيقاف", minutes)
        # an answer with evidence to the strongest objection lifts the block
        r = run("answer", "--dir", self.dir, "--file", self.put("a.json", {"answers": [{"rank": 9, "answer": "x", "evidence": "y"}]}), ok=False)
        self.assertIn("ANSWER_INVALID", r.stderr)
        run("answer", "--dir", self.dir, "--file", self.put("a.json", {"answers": [
            {"rank": 1, "by": "M4", "answer": "captions sit inside the 9:16 safe zone", "evidence": "ran safe_zone check on frame 0042.png"}]}))
        v = json.loads(run("verdict", "--dir", self.dir).stdout)
        self.assertEqual(v["status"], "COUNCIL_RUN")
        self.assertTrue(v["clean_pass"], v["clean_pass_blockers"])
        self.assertEqual(v["devil"]["answered_ranks"], [1])

    def test_round3_devil_answers_count_and_target_mismatch_is_flagged(self):
        self.rounds_1_2()
        run("devil", "--dir", self.dir, "--file", self.put("d.json", dict(self.DEVIL, target_option="C")))
        ans = {"M3": [{"rank": 1, "answer": "safe zones checked", "evidence": "opinion"}]}
        v = self.round3(self.SCORES, {"M2": "risk"}, ans)
        self.assertEqual(v["status"], "COUNCIL_RUN")
        self.assertTrue(v["devil"]["strongest_answered"])
        self.assertEqual(v["devil"]["answered_by_opinion_only"], [1])
        self.assertTrue(any(w.startswith("DEVIL_TARGET_MISMATCH") for w in v["warnings"]))
        self.assertFalse(v["clean_pass"], "the devil attacked C but B won")

    def test_groupthink_calibration_and_evidence_quality(self):
        r1 = {"position": "p", "proposal": "x", "risks": ["r"], "top_choice": "B",
              "claims": [{"claim": "c1", "evidence": "opinion", "confidence": 0.9},
                         {"claim": "c2", "evidence": "https://example.org/spec", "confidence": 0.7},
                         {"claim": "c3", "evidence": "ran verify_video.py", "confidence": 0.8, "evidence_quality": "reproduced"}]}
        self.rounds_1_2(r1)
        same = {m: {"A": 2, "B": 5, "C": 1} for m in ("M1", "M2", "M3", "M4", "M5")}
        v = self.round3(same)
        self.assertTrue(any(g.startswith("EARLY_CONVERGENCE") for g in v["groupthink"]))
        self.assertTrue(any(g.startswith("UNANIMOUS_NO_DISSENT") for g in v["groupthink"]))
        self.assertEqual(v["evidence_quality"]["opinion"], 5)
        self.assertEqual(v["evidence_quality"]["sourced"], 5)
        self.assertEqual(v["evidence_quality"]["reproduced"], 5)
        self.assertTrue(v["calibration"]["M1"]["overconfident"])
        self.assertEqual(v["calibration"]["M1"]["evidenced_mean"], 0.75)
        self.assertTrue(any(w.startswith("OVERCONFIDENT_OPINION") for w in v["warnings"]))
        self.assertIn("NO_DEVIL_CASE", v["clean_pass_blockers"])
        self.assertFalse(v["clean_pass"])
        self.assertIn("تفكير القطيع", (Path(self.dir) / "minutes.md").read_text(encoding="utf-8"))

    def test_optional_round_fields_are_validated(self):
        run("plan", "سؤال", "--dir", self.dir)
        for bad, frag in ((dict(R1, top_choice="Z"), "top_choice"),
                          (dict(R1, claims=[{"claim": "c", "evidence": "e", "confidence": 1.5}]), "confidence"),
                          (dict(R1, claims=[{"claim": "c", "evidence": "e", "evidence_quality": "vibes"}]), "evidence_quality")):
            r = run("ingest", "--dir", self.dir, "--round", "1", "--member", "M1", "--file", self.put("b.json", bad), ok=False)
            self.assertIn("MEMBER_INVALID", r.stderr)
            self.assertIn(frag, r.stderr)

    def test_members_get_distinct_mental_model_lenses_and_the_devil_seat(self):
        out = json.loads(run("plan", "هل نطلق خطة التسعير الجديدة للعملاء؟", "--dir", self.dir, "--no-roster").stdout)
        self.assertEqual(out["devil"], "M2")
        self.assertEqual(out["lenses"]["M2"], ["MODEL-02 Inversion", "MODEL-24 Pre-mortem"])
        allx = [x for v in out["lenses"].values() for x in v]
        self.assertTrue(all(1 <= len(v) <= 2 for v in out["lenses"].values()))
        self.assertEqual(len(allx), len(set(allx)), "no two members share a lens")
        run("prompts", "--dir", self.dir, "--round", "1")
        p1 = json.loads((Path(self.dir) / "prompts_r1.json").read_text(encoding="utf-8"))
        self.assertIn("Your thinking lenses", p1["M3"])
        self.assertIn("Misuse warning", p1["M3"])
        self.assertIn("DEVIL'S ADVOCATE seat", p1["M2"])
        self.assertNotIn("DEVIL'S ADVOCATE seat", p1["M1"])
        big = self.root / "big"
        out = json.loads(run("plan", "قرار", "--dir", str(big), "--seats", "15", "--no-roster").stdout)
        c = json.loads((big / "council.json").read_text(encoding="utf-8"))
        self.assertEqual(next(m for m in c["roster"] if m["id"] == out["devil"])["lane"], "verification")
        allx = [x for v in out["lenses"].values() for x in v]
        self.assertEqual(len(allx), len(set(allx)), "fifteen seats, thirty distinct lenses")
        r = run("plan", "x", "--dir", str(self.root / "d2"), "--devil", "M9", ok=False)
        self.assertIn("UNKNOWN_MEMBER", r.stderr)
        self.assertEqual(json.loads(run("plan", "x", "--dir", str(self.root / "d3"), "--devil", "m4", "--no-roster").stdout)["devil"], "M4")


if __name__ == "__main__":
    unittest.main()
