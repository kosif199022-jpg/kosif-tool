#!/usr/bin/env python3
"""Regression tests for read-only KOSIF Atlas fusion."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("atlas_deep_fusion", HERE / "atlas_deep_fusion.py")
fusion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fusion)

class AtlasFusionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.main = self.root / "index.json"
        self.copy = self.root / "index-copyleft.json"
        self.sample = {"id":1,"plugin":"example","skill":"agent-orchestration",
            "description":"Agent orchestration guide with workflows","license":"MIT",
            "path":"skills/example/agent-orchestration","source":"https://example.org/a",
            "files":["SKILL.md"],"verdict":"READ_ONLY_OK","risk_flags":[],"complete":True}
        self.main.write_text(json.dumps({"count":1,"skills":[self.sample]}),encoding="utf-8")
        self.copy.write_text(json.dumps({"count":0,"skills":[]}),encoding="utf-8")
    def tearDown(self): self.temp.cleanup()
    def report(self,**kwargs):
        return fusion.build_report(self.main,self.copy,**kwargs)
    def test_inventory_and_selection(self):
        o=self.report(query="agent",domain="agents")
        self.assertEqual(o["inventory"]["total"],1)
        self.assertEqual(len(o["selected"]),1)
        self.assertEqual(o["selected"][0]["eligibility"],"metadata_candidate_only")
        self.assertFalse(o["selected"][0]["execution_verified"])
    def test_copyleft_cannot_merge(self):
        self.copy.write_text(json.dumps({"count":1,"skills":[dict(self.sample,id=2,license="GPL-3.0")]}),encoding="utf-8")
        o=self.report(query="agent")
        self.assertEqual(o["inventory"]["copyleft"],1)
        self.assertEqual(len(o["selected"]),1)
        self.assertFalse(o["trust"]["copyleft_merge_allowed"])
    def test_risk_blocks_promotion(self):
        self.main.write_text(json.dumps({"count":1,"skills":[dict(self.sample,risk_flags=["shell_exec"])]}),encoding="utf-8")
        o=self.report(query="agent")
        self.assertEqual(o["selected"][0]["eligibility"],"reference_only_manual_review")
    def test_unknown_query_no_hallucinated_matches(self):
        self.assertEqual(self.report(query="nonexistentrandomterm2026")["selected_count"],0)
    def test_traversal_rejected(self):
        self.assertIsNone(fusion._validate_path(self.root,"skills/../../etc/passwd"))
    def test_actual_source_static_check(self):
        folder=self.root/"skills/example/agent-orchestration"
        folder.mkdir(parents=True)
        (folder/"SKILL.md").write_text("---\nname: test\n---\n# Example\nOnly read text.\n",encoding="utf-8")
        o=self.report(query="agent",source_root=self.root)
        self.assertEqual(o["selected"][0]["source_inspection"]["source_state"],"inspected_text_only")
        self.assertTrue(o["selected"][0]["source_inspection"]["has_frontmatter"])
    def test_manifest_count_mismatch_is_hard_fail(self):
        self.main.write_text('{"count":2,"skills":[]}',encoding="utf-8")
        with self.assertRaises(ValueError): self.report()
    def test_no_query_is_not_full_injection(self):
        self.assertEqual(self.report()["selected_count"],0)
    def test_output_is_deterministic(self):
        self.assertEqual(self.report(query="agent"),self.report(query="agent"))

if __name__=="__main__": unittest.main()
