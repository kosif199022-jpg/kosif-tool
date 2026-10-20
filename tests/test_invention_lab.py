"""Deterministic KOSIF invention engine: baseline vs candidate gates."""
import importlib.util
import unittest
from pathlib import Path
PATH=Path(__file__).resolve().parents[1]/".claude/skills/kosif-superpowers/scripts/invention_lab.py"
s=importlib.util.spec_from_file_location("kosif_invention_lab",PATH)
lab=importlib.util.module_from_spec(s)
import sys
sys.modules[s.name]=lab
s.loader.exec_module(lab)
class InventionTests(unittest.TestCase):
    def test_reproducible(self):
        a=lab.make_ideas("Improve Arabic video titles without losing quality",20)
        b=lab.make_ideas("Improve Arabic video titles without losing quality",20)
        self.assertEqual(a,b)
        self.assertEqual(len(a),20)
        self.assertEqual(len({x.id for x in a}),20)
    def test_falsifiable(self):
        x=lab.make_ideas("Create faster and more readable Arabic captions",15,["no proprietary fonts"])
        self.assertTrue(all(v.test and v.failure_threshold and v.success_metric for v in x))
        self.assertTrue(all(v.novelty_status.startswith("unverified") for v in x))
        self.assertTrue(all("no proprietary fonts" in v.risk for v in x))
    def test_every_constraint_reaches_risk(self):
        cons=[f"constraint {i}" for i in range(1,9)]
        x=lab.make_ideas("Make Arabic captions render faster on mobile",3,cons)
        self.assertTrue(all(all(c in v.risk for c in cons) for v in x))
    def test_proposal_reads_as_a_sentence(self):
        x=lab.make_ideas("Make Arabic captions render faster on mobile",64)
        self.assertEqual(len(x),64)
        for v in x:
            self.assertNotIn("optimize for improve",v.proposal)
            self.assertNotIn("optimize for reduce",v.proposal)
            self.assertIn("; aim to ",v.proposal)
    def test_input_bounds(self):
        with self.assertRaises(ValueError): lab.make_ideas("Hi",10)
        with self.assertRaises(ValueError): lab.make_ideas("Detailed problem request",65)
    def test_methods_available(self):
        self.assertGreaterEqual(len(lab.METHODS),12)
        self.assertTrue(any(p[0]=="segmentation" for p in lab.METHODS))
if __name__=="__main__":unittest.main()
