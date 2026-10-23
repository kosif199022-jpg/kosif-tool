"""Offline tests for A20 book-distilled methods (registry + rest/bayes/clarity/ledger/persona helpers)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import book_methods as M  # noqa: E402


class BookMethodsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = M.load()

    def test_registry_scope_and_provenance(self):
        self.assertEqual(len(self.d["sources"]), 10)
        self.assertEqual(len(self.d["methods"]), 45)
        st = {s["id"]: s["status"] for s in self.d["sources"]}
        self.assertEqual(st["SRC-HP"], "excluded")
        self.assertEqual(st["SRC-BY"], "teaser-only")
        used = {m["source"] for m in self.d["methods"]}
        self.assertTrue(used >= {"SRC-LT", "SRC-PP", "SRC-PS", "SRC-AC", "SRC-KV", "SRC-SH", "SRC-IM", "SRC-OU"})
        self.assertEqual({m["domain"] for m in self.d["methods"]}, M.DOMAINS)

    def test_annex_lists_every_source_file(self):
        annex = (SK / "references" / "protocol" / "A20-book-distilled-methods.md").read_text(encoding="utf-8")
        for s in self.d["sources"]:
            self.assertIn("(%d pp)" % s["pages"], annex, s["id"])

    def test_search_arabic(self):
        self.assertEqual(M.search(self.d, "محاسبة")[0]["domain"], "accounting")
        self.assertIn(M.search(self.d, "قصيدة")[0]["id"], {"AR-01", "AR-02"})
        with self.assertRaises(ValueError):
            M.resolve(self.d, "XX-99")

    def test_rest_is_seeded(self):
        a, b = M.rest("p", 3, 7), M.rest("p", 3, 7)
        self.assertEqual(a["words"], b["words"])
        self.assertEqual(len(a["prompts"]), 12)

    def test_bayes_posterior_and_db(self):
        r = M.bayes({"H": 0.5, "K": 0.5}, [("e", {"H": 0.9, "K": 0.1})])
        self.assertAlmostEqual(r["posterior"]["H"], 0.9, places=6)
        self.assertAlmostEqual(r["ledger"][0]["H_dB"], 9.54, places=2)
        with self.assertRaises(ValueError):
            M.bayes({"H": 0.0, "K": 1.0}, [])

    def test_clarity_gate(self):
        self.assertEqual(M.clarity("صورة جميلة لشخص")["verdict"], "REVISE")
        good = ("Woman in her 40s in a small 1950s kitchen at dawn, warm light from the left window, slow push-in, "
                "nostalgic and lonely, to establish her grief. HARD LOCK: grey dress; SOFT LATITUDE: expression")
        self.assertEqual(M.clarity(good)["verdict"], "GENERATE")

    def test_ledger_settlement_vat_and_floats(self):
        inv = {"id": "J1", "source": "invoice", "party": "Nour", "event_key": "INV-104",
               "vat": {"net": "1000", "tax": "150", "rate": "0.15"},
               "lines": [{"account": "1201", "debit": "1150"}, {"account": "4101", "credit": "1000"},
                         {"account": "2201", "credit": "150"}]}
        bank_rev = {"id": "J2", "source": "bank", "party": "Nour",
                    "lines": [{"account": "1101", "debit": "1150"}, {"account": "4101", "credit": "1150"}]}
        settle = {"id": "J3", "source": "bank", "party": "Nour",
                  "lines": [{"account": "1101", "debit": "1150"}, {"account": "1201", "credit": "1150"}]}
        self.assertTrue(M.ledger([inv, settle], "4101", "1201")["ok"])
        r = M.ledger([inv, bank_rev], "4101", "1201")
        self.assertFalse(r["ok"])
        self.assertIn("settlement", r["errors"][0])
        bad_vat = json.loads(json.dumps(inv))
        bad_vat["vat"]["tax"] = "160"
        self.assertFalse(M.ledger([bad_vat])["ok"])
        self.assertFalse(M.ledger([inv, inv])["ok"])
        with self.assertRaises(ValueError):
            M.ledger([{"id": "F", "lines": [{"account": "1", "debit": 1.5}]}])
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "e.json"
            f.write_text(json.dumps([inv, bank_rev]), encoding="utf-8")
            self.assertEqual(M.main(["ledger", "--file", str(f), "--revenue", "4101", "--receivable", "1201"]), 1)

    def test_persona_guard(self):
        p = M.persona("x", {"O": 4, "C": 2, "E": 5, "A": 2, "N": 3})
        self.assertEqual(len(p["speech_rules"]), 5)
        self.assertIn("never", p["guard"])
        with self.assertRaises(ValueError):
            M.persona("x", {"O": 9})


if __name__ == "__main__":
    unittest.main()
