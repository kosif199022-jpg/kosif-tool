"""Atlas ledger: every Atlas skill gets exactly one status, and the committed ledger matches the inputs."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import atlas_ledger as al  # noqa: E402


class AtlasLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.led = al.build()

    def test_self_test_passes(self):
        r = subprocess.run([sys.executable, str(SK / "scripts/atlas_ledger.py"), "--self-test"],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_skill_has_one_status(self):
        idx = al.atlas_5000.load_index()
        self.assertEqual(self.led["total"], len(idx["skills"]))
        self.assertEqual(sum(self.led["counts"].values()), self.led["total"])
        self.assertEqual(len({r[0] for r in self.led["rows"]}), self.led["total"])
        self.assertTrue({r[1] for r in self.led["rows"]} <= set(al.STATUSES))

    def test_pattern_rules_point_at_real_powers(self):
        ids = {p["id"] for f in (SK / "data" / "powers").glob("*.json")
               for p in json.loads(f.read_text(encoding="utf-8"))}
        for rule in al.load_decisions():
            self.assertIn(rule["status"], ("pattern", "skipped"), rule)
            self.assertTrue(rule["reason"], rule)
            if rule["status"] == "pattern":
                self.assertTrue(rule["powers"], rule)
                self.assertTrue(set(rule["powers"]) <= ids, rule)
            else:
                self.assertFalse(rule.get("powers"), rule)

    def test_unsafe_skills_never_pattern_or_pending(self):
        idx = {s["id"]: s for s in al.atlas_5000.load_index()["skills"]}
        for i, st, _, _ in self.led["rows"]:
            if st in ("pattern", "pending"):
                self.assertTrue(al.atlas_5000.is_safe(idx[i]), i)

    def test_committed_ledger_is_complete(self):
        # Freshness is checked by `atlas_ledger.py build --check`, not here: other branches may add
        # powers that cite Atlas folders, and that must not fail their CI.
        led = al.load()
        self.assertEqual(led["schema"], al.SCHEMA)
        self.assertEqual(led["total"], self.led["total"])
        self.assertEqual(sum(led["counts"].values()), led["total"])

    def test_rea_receipt_covers_every_skill(self):
        rec = json.loads((SK / "proofs" / "atlas-rea" / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(rec["schema"], "kosif.rea-receipt.v1")
        self.assertFalse(rec["executed_target_code"])
        self.assertEqual(rec["skill_md_hashed_by_rea"], self.led["total"])


if __name__ == "__main__":
    unittest.main()
