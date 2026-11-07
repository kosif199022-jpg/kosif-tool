"""Tests for the Dragon Mind's full-text book reading (Thinking, Fast and Slow) and its trap scan."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIND = ROOT / ".claude/skills/kosif-dragon-mind"
sys.path.insert(0, str(MIND / "scripts"))
import dragon_mind as dm  # noqa: E402
import _mind_vocab as V  # noqa: E402

SLUG = "thinking_fast_slow"


class BookReadingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book = json.loads((MIND / "data" / ("book_%s.json" % SLUG)).read_text(encoding="utf-8"))
        cls.lib = json.loads((MIND / "data" / "frameworks.json").read_text(encoding="utf-8"))["frameworks"]

    def test_every_page_was_read(self):
        total = self.book["pages_total"]
        self.assertEqual(total, 468)
        self.assertEqual(self.book["pages_read"], total)
        self.assertEqual([p["page"] for p in self.book["pages"]], list(range(1, total + 1)))
        self.assertTrue(all(p["gist"].strip() for p in self.book["pages"]))
        self.assertEqual(self.book["readers"], len(self.book["chunks"]))
        covered = {p for a, b in self.book["chunks"] for p in range(a, b + 1)}
        self.assertEqual(covered, set(range(1, total + 1)))

    def test_insights_cite_real_pages_and_known_operators(self):
        ids = {f["id"] for f in self.lib}
        self.assertEqual(self.book["insights_total"], len(self.book["insights"]))
        for i in self.book["insights"]:
            self.assertTrue(all(1 <= p <= self.book["pages_total"] for p in i["pages"]), i["concept"])
            self.assertTrue(i["operator"] is None or i["operator"] in ids, i["operator"])

    def test_book_operators_are_valid_frameworks(self):
        ops = [f for f in self.lib if f.get("full_text_read") == SLUG]
        self.assertGreaterEqual(len(ops), 40)
        stages = {s["id"] for s in V.CYCLE}
        for f in ops:
            self.assertIn(f["stage"], stages)
            self.assertEqual(len(f["questions_ar"]), 3, f["id"])
            self.assertTrue(f["page_refs"] and f["debias_ar"] and f["check"], f["id"])
            self.assertTrue(all(1 <= p <= 468 for p in f["page_refs"]))
            self.assertTrue(f["triggers_ar"] and f["triggers_en"], f["id"])
        self.assertGreaterEqual(sum(1 for f in ops if f.get("trap")), 20)
        for fid in dm.TRAP_GATE:
            self.assertIn(fid, {f["id"] for f in ops if f.get("trap")})

    def test_receipt_matches_book_record(self):
        rec = json.loads((MIND / "data" / "research_receipt.json").read_text(encoding="utf-8"))
        entry = next(b for b in rec["full_text_books"] if b["slug"] == SLUG)
        self.assertEqual(entry["pages_read"], self.book["pages_read"])
        self.assertEqual(entry["insights"], self.book["insights_total"])
        self.assertEqual(entry["pdf_sha256"], self.book["pdf_sha256"])
        self.assertEqual(rec["frameworks"]["count"], len(self.lib))


class TrapScanTests(unittest.TestCase):
    def test_gate_traps_always_present(self):
        ids = [t["id"] for t in dm.scan_traps("hello")]
        for fid in dm.TRAP_GATE:
            self.assertIn(fid, ids)

    def test_detects_planning_and_anchoring_traps(self):
        ids = {t["id"] for t in dm.scan_traps("estimate the budget and deadline for the launch plan, starting from last price", deep=True)}
        self.assertIn("tfs-planning-fallacy", ids)

    def test_arabic_hamza_spelling_does_not_hide_a_trap(self):
        a = [t["id"] for t in dm.scan_traps("أفضل إعلان لإطلاق المنتج", deep=True)]
        b = [t["id"] for t in dm.scan_traps("افضل اعلان لاطلاق المنتج", deep=True)]
        self.assertEqual(a, b)

    def test_traps_are_deterministic_and_carry_pages(self):
        task = "قرار سريع: هل نطلق المنتج بناء على تجربة صغيرة نجحت؟"
        a, b = dm.scan_traps(task, True), dm.scan_traps(task, True)
        self.assertEqual(a, b)
        self.assertTrue(all(t["pages"] and t["debias_ar"] for t in a))
        self.assertLessEqual(len([t for t in a if t["score"]]), dm.TRAP_LIMIT[True])

    def test_think_report_has_trap_section(self):
        tr = dm.think("plan a product launch with a tight deadline and budget")
        self.assertTrue(tr["traps"])
        self.assertIn("## 6.", dm.report_md(tr))
        if any(t["score"] for t in tr["traps"]):
            self.assertTrue(any(i["kind"] == "bias" for i in tr["critic"]))

    def test_book_lookup_by_page_and_query(self):
        res = dm.book_lookup(SLUG, page=100)
        self.assertEqual(res["page"]["page"], 100)
        q = dm.book_lookup(SLUG, query="anchoring")
        self.assertGreater(q["matches"], 0)
        with self.assertRaises(ValueError):
            dm.book_lookup(SLUG, page=9999)

    def test_doctor_checks_the_book(self):
        checks = {c["check"]: c for c in dm.doctor()["checks"]}
        self.assertTrue(checks["book_" + SLUG]["pass"], checks["book_" + SLUG]["detail"])
        self.assertTrue(checks["traps"]["pass"])


if __name__ == "__main__":
    unittest.main()
