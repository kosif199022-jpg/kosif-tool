#!/usr/bin/env python3
"""Tests for scripts/charter_ingest.py (the 500-expert charter as an INDEX) and the council's roster consultation.

A small synthetic roster is written in a temp dir; the full charter text is checked only when it is present
on this machine (KOSIF_CHARTER_TXT, or a session scratch copy under the temp dir). Temp dirs only.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
INGEST = SKILL / "scripts" / "charter_ingest.py"
COUNCIL = SKILL / "scripts" / "council.py"


def _full_txt() -> Path:
    """KOSIF_CHARTER_TXT, else a session scratch copy (<tmp>/claude-*/<project>/<session>/scratchpad/attach/f545.txt)."""
    env = os.environ.get("KOSIF_CHARTER_TXT")
    if env:
        return Path(env)
    hits = sorted(Path(tempfile.gettempdir()).glob("claude-*/*/*/scratchpad/attach/f545.txt"))
    return hits[0] if hits else Path("<absent>")


FULL_TXT = _full_txt()


def run(script, *args, ok=True):
    r = subprocess.run([sys.executable, str(script), *args], text=True, capture_output=True, timeout=120)
    if ok and r.returncode != 0:
        raise AssertionError(f"{args} -> {r.returncode}\n{r.stderr}")
    return r


def entry(n, name, role, tasks, traits):
    return f"{n}. {name}\n\nالدور: {role}\n\nالمهام: {tasks}\n\nالخصائص: {traits}\n\n"


def fixture() -> str:
    """Sectors 1 and 50 × 6 entries: boilerplate traits, a duplicate role, consent and regulated roles."""
    t = "عقد تجريبي\n\nالباب الثالث : أعضاء\n\nالقطاع 1: كتابة القصص والسيناريو (Story & Script Writing)\n\n"
    t += entry(1, "كاتب الرعب (Horror Writer)", "كتابة قصص الرعب", "بناء التوتر والمشاهد المخيفة", "متخصص ومحترف")
    t += entry(2, "مخرج المشاهد (Scene Director)", "إدارة المشاهد", "تقسيم القصة إلى مشاهد", "متخصص ومحترف")
    t += entry(3, "متخصص استنساخ الصوت (Voice Cloning Specialist)", "استنساخ الأصوات", "إنشاء نسخة من صوت شخص", "متخصص ومحترف")
    t += entry(4, "خبير Face Swap AI", "تبديل الوجوه", "ثبات الوجوه عبر المشاهد", "متخصص ومحترف")
    t += entry(5, "مراجع جودة القصة (Story QA Reviewer)", "مراجعة القصة", "فحص الحبكة والاتساق", "متخصص ومحترف")
    t += entry(6, "كاتب الرعب (Horror Writer)", "كتابة الرعب مرة أخرى", "نص آخر", "دقيق ومبدع")
    t += "القطاع 50: الإدارة العامة والحوكمة (General Administration & Governance)\n\n"
    t += entry(7, "متخصص محتوى الضرائب", "إنتاج محتوى ضريبي", "شرح الضرائب", "حذر")
    t += entry(8, "مصمم المناظر الطبيعية (Landscape Designer)", "تصميم المناظر الطبيعية", "طبيعة", "فنان")
    t += entry(9, "مدير المخاطر (Risk Manager)", "تحديد المخاطر", "إدارة المخاطر", "حذر")
    t += entry(10, "المستشار القانوني (Legal Counsel)", "تقديم الاستشارات القانونية", "مراجعة العقود", "حذر")
    t += entry(11, "محلل البيانات (Data Analyst)", "تحليل البيانات", "تقارير", "يعتمد على البيانات")
    t += entry(12, "مؤرشف المحتوى (Archivist)", "حفظ الملفات", "أرشفة", "منظم")
    t += "الخاتمة\n\nتم التوقيع والاعتماد.\n"
    return t


class CharterIndexTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.txt = self.root / "roster.txt"
        self.txt.write_text(fixture(), encoding="utf-8")
        self.out = self.root / "idx.json"

    def ingest(self):
        run(INGEST, str(self.txt), "--out", str(self.out), "--allow-partial")
        return json.loads(self.out.read_text(encoding="utf-8"))

    def test_partial_roster_is_refused_without_flag(self):
        r = run(INGEST, str(self.txt), "--out", str(self.out), ok=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("SHAPE", r.stderr)
        self.assertFalse(self.out.exists(), "nothing is written on refusal")

    def test_fixture_parse_and_flags(self):
        idx = self.ingest()
        self.assertEqual(idx["schema"], "kosif.experts-index.v1")
        self.assertIn("not executed", idx["note"])
        self.assertEqual(len(idx["source"]["sha256"]), 64)
        self.assertEqual([len(s["experts"]) for s in idx["sectors"]], [6, 6])
        ex = {e["n"]: e for s in idx["sectors"] for e in s["experts"]}
        self.assertEqual(ex[1]["name_ar"], "كاتب الرعب")
        self.assertEqual(ex[1]["name_en"], "Horror Writer")
        self.assertEqual(ex[1]["role"], "كتابة قصص الرعب")
        self.assertTrue(ex[1]["flags"]["boilerplate"])          # «متخصص ومحترف» × 5
        self.assertFalse(ex[6]["flags"]["boilerplate"])
        self.assertEqual(ex[6]["flags"]["duplicate_of"], 1)
        self.assertEqual(ex[3]["flags"]["sensitive"], "consent")
        self.assertEqual(ex[4]["flags"]["sensitive"], "consent")
        self.assertEqual(ex[7]["flags"]["sensitive"], "regulated")
        self.assertEqual(ex[10]["flags"]["sensitive"], "regulated")
        self.assertIsNone(ex[2]["flags"]["sensitive"])
        self.assertIsNone(ex[8]["flags"]["sensitive"], "طبيعية is not medical")
        self.assertIsNone(ex[9]["flags"]["sensitive"])
        known = {p.stem for p in (SKILL / "data" / "powers").glob("*.json")}
        for e in ex.values():
            self.assertLessEqual(set(e["kosif_families"]), known)
        self.assertIn("story-direction-ideas", ex[1]["kosif_families"])
        rc = idx["receipt"]
        self.assertEqual((rc["sectors"], rc["experts"], rc["boilerplate"], rc["duplicates"]), (2, 12, 5, 1))

    def test_council_plan_records_consulted_index_and_minutes_wording(self):
        self.ingest()
        cdir = self.root / "council"
        out = json.loads(run(COUNCIL, "plan", "اكتب قصة رعب 5 مشاهد مع استنساخ صوت", "--dir", str(cdir),
                             "--roster", str(self.out)).stdout)
        self.assertIn("index consulted:", out["index_consulted"])
        c = json.loads((cdir / "council.json").read_text(encoding="utf-8"))
        ci = c["consulted_index"]
        self.assertTrue(ci)
        for p in ci:
            self.assertTrue({"sector", "n", "name_ar", "member"} <= set(p))
        self.assertTrue(all(sum(1 for p in ci if p["member"] == m) <= 3 for m in ("M1", "M2", "M3", "M4", "M5")))
        self.assertEqual(len({p["n"] for p in ci}), len(ci), "each card goes to one member")
        self.assertNotIn(6, [p["n"] for p in ci], "a duplicate card is represented by its original")
        guard = [p for p in ci if p["member"] == "M5"]
        self.assertIn(3, [p["n"] for p in guard], "the Guardian gets the consent card the request names")
        self.assertTrue(any(p["sector"] == 50 for p in guard), "the Guardian gets a governance card")
        self.assertFalse([p for p in ci if p["member"] != "M5" and p.get("sensitive")], "sensitive cards stay with M5")
        self.assertEqual(len(c["roster"]), 5, "the index adds no members")
        run(COUNCIL, "prompts", "--dir", str(cdir), "--round", "1")
        p1 = json.loads((cdir / "prompts_r1.json").read_text(encoding="utf-8"))
        self.assertIn("Personas to consult (an index, not extra members)", p1["M5"])
        # a simulated full run: the minutes report the index and never claim that experts ran
        r1 = {"position": "p", "claims": [{"claim": "c", "evidence": "opinion"}], "proposal": "x", "risks": []}
        r2 = {"attacks": [], "steelman": {"target": "M1", "why_strong": "w"}, "concessions": []}
        for rnd, body in ((1, r1), (2, r2), (3, None)):
            for m in ("M1", "M2", "M3", "M4", "M5"):
                obj = body or {"final_proposal": "f", "scores": {"A": 3, "B": 4, "C": 2}, "remaining_objection": "consent"}
                f = self.root / f"{m}{rnd}.json"
                f.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
                run(COUNCIL, "ingest", "--dir", str(cdir), "--round", str(rnd), "--member", m, "--file", str(f), "--simulated")
        v = json.loads(run(COUNCIL, "verdict", "--dir", str(cdir)).stdout)
        self.assertEqual(v["status"], "COUNCIL_SIMULATED")
        self.assertEqual(v["index_consulted"], len(ci))
        minutes = (cdir / "minutes.md").read_text(encoding="utf-8")
        self.assertIn(f"index consulted: {len(ci)} personas", minutes)
        for claim in ("experts ran", "500 experts", "خبير شارك", "الخبراء صوّتوا"):
            self.assertNotIn(claim, minutes)

    def test_no_roster_and_secret_refusal(self):
        cdir = self.root / "c2"
        out = json.loads(run(COUNCIL, "plan", "سؤال", "--dir", str(cdir), "--no-roster").stdout)
        self.assertEqual(out["index_consulted"], "index consulted: 0 personas (an index, not executed experts)")
        miss = run(COUNCIL, "plan", "سؤال", "--dir", str(self.root / "c3"), "--roster", str(self.root / "nope.json"), ok=False)
        self.assertIn("ROSTER_MISSING", miss.stderr)
        self.ingest()
        sec = run(COUNCIL, "plan", "use api_key=" + "sk-" + "ant-" + "Q7x9" * 6, "--dir", str(self.root / "c4"),
                  "--roster", str(self.out), ok=False)
        self.assertEqual(sec.returncode, 2)
        self.assertIn("SECRET", sec.stderr)
        leak = self.root / "leak.txt"
        leak.write_text(fixture().replace("شرح الضرائب", "api_key=" + "sk-" + "ant-" + "Q7x9" * 6), encoding="utf-8")
        r = run(INGEST, str(leak), "--out", str(self.root / "leak.json"), "--allow-partial", ok=False)
        self.assertIn("SECRET", r.stderr)


@unittest.skipUnless(FULL_TXT.is_file(), "the full charter text is not on this machine")
class FullCharterTest(unittest.TestCase):
    def test_full_parse_is_50_by_10(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "e.json"
            run(INGEST, str(FULL_TXT), "--out", str(out))
            idx = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(len(idx["sectors"]), 50)
        self.assertTrue(all(len(s["experts"]) == 10 for s in idx["sectors"]))
        nums = [e["n"] for s in idx["sectors"] for e in s["experts"]]
        self.assertEqual(nums, list(range(1, 501)))
        rc = idx["receipt"]
        self.assertEqual((rc["sectors"], rc["experts"]), (50, 500))
        self.assertGreaterEqual(rc["boilerplate"], 180)
        self.assertGreaterEqual(rc["duplicates"], 1)
        ex = {e["n"]: e for s in idx["sectors"] for e in s["experts"]}
        for n in (124, 129, 143):
            self.assertEqual(ex[n]["flags"]["sensitive"], "consent", n)
        for n in (290, 411, 469, 495):
            self.assertEqual(ex[n]["flags"]["sensitive"], "regulated", n)
        self.assertEqual(ex[427]["flags"]["duplicate_of"], 345)
        self.assertIsNone(ex[25]["flags"]["sensitive"], "landscape (طبيعية) is not medical")
        for e in ex.values():
            dup = e["flags"]["duplicate_of"]
            if dup:
                self.assertLess(dup, e["n"])

    def test_committed_index_matches_source(self):
        committed = SKILL / "data" / "experts_500.json"
        if not committed.is_file():
            self.skipTest("data/experts_500.json not built")
        import hashlib
        idx = json.loads(committed.read_text(encoding="utf-8"))
        self.assertEqual(idx["source"]["sha256"], hashlib.sha256(FULL_TXT.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
