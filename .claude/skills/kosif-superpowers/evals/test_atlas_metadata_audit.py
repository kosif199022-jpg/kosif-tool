"""Metadata only: fixed fixtures, no network or execution."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
SK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/"scripts"))
import atlas_metadata_audit as m

class AtlasMetadataTests(unittest.TestCase):
    def make_fixture(self,dir):
        item={"id":1,"plugin":"a","skill":"test","description":"test text",
              "license":"MIT","source":"https://github.com/o/r","path":"skills/1-a",
              "verdict":"REVIEW_BEFORE_INSTALL","complete":True,"risk_flags":["external-code"]}
        other={**item,"id":"x2","license":"GPL-3.0","verdict":"REVIEW_BEFORE_INSTALL"}
        p=Path(dir)/"index.json";q=Path(dir)/"copyleft.json"
        p.write_text(json.dumps({"count":1,"skills":[item]}))
        q.write_text(json.dumps({"count":1,"skills":[other]}))
        return p,q
    def test_counts_reviews_no_code(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.make_fixture(d);r=m.audit(a,b)
            self.assertEqual(r["examined"],2)
            self.assertEqual(r["main_records"],1)
            self.assertEqual(r["copyleft_records"],1)
            self.assertEqual(r["structural_errors"],[])
            self.assertEqual(r["inventory_counts"]["review_before_install"],2)
            self.assertFalse(r["executes_skills"])
            self.assertEqual(r["live_capabilities_verified"],0)
    def test_count_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.make_fixture(d);src=json.loads(a.read_text());src["count"]=3;a.write_text(json.dumps(src))
            self.assertTrue(m.audit(a,b)["structural_errors"])
    def test_reject_invalid_index(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=self.make_fixture(d);a.write_text(json.dumps([]))
            with self.assertRaises(ValueError):
                m.audit(a,b)
    def test_no_repository_code_execution(self):
        script=(SK/"scripts/atlas_metadata_audit.py").read_text(encoding="utf-8-sig")
        for bad in ("subprocess.run","os.system","eval(","exec(","requests.get"):
            self.assertNotIn(bad,script)
if __name__=="__main__":unittest.main()
