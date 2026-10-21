#!/usr/bin/env python3
"""Read-only regression harness for the FusionForge CLI; uses isolated temp data."""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"fusionforge.py"

class FusionForgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.catalog=self.root/"fake-superpowers.json"
        self.catalog.write_text(json.dumps({
            "superpowers":3,"atoms":30,
            "items":[
                {"id":"SP-0001","name_en":"video montage typography","name_ar":"مونتاج فيديو","domain":"motion","size":8,"ready_now":3,"status_mix":{"ready":3},"links":[{"id":"SP-0004","sim":0.55}]},
                {"id":"SP-0002","name_en":"video audio alignment","name_ar":"صوت فيديو","domain":"media","size":7,"ready_now":3},
                {"id":"SP-0003","name_en":"video validation quality","name_ar":"فحص فيديو","domain":"data","size":6,"ready_now":2},
                {"id":"SP-0004","name_en":"financial reconciliation invariant","name_ar":"تسوية مالية مستقلة","domain":"data","size":3,"ready_now":2}
            ]},ensure_ascii=False),encoding="utf-8")
        self.prefix=[sys.executable,str(SCRIPT),"--root",str(self.root/"out"),
                     "--catalog-file",str(self.catalog)]

    def run_cli(self,*args,success=True):
        r=subprocess.run(self.prefix+list(args),text=True,capture_output=True,timeout=20)
        if success:self.assertEqual(r.returncode,0,r.stderr)
        else:self.assertNotEqual(r.returncode,0,"should reject unsafe/invalid operation")
        return json.loads(r.stdout) if success else r.stderr

    def make(self,project="alpha",goal="مونتاج فيديو وصوت"):
        return self.run_cli("propose",goal,"--project",project)

    def test_new_recipe_and_index(self):
        d=self.make()
        self.assertEqual(d["status"],"candidate")
        self.assertGreaterEqual(len(d["capabilities"]),1)
        self.assertEqual(len(d["workflow"]),8)
        self.assertIn("SP-0004", {c["id"] for c in d["capabilities"]}, "cross-domain linked capability should be considered")
        self.assertTrue(any(edge["to"]=="SP-0004" for edge in d["integration_graph"]))
        self.assertEqual(len(d["methods"]),3)
        index=self.run_cli("catalog","--project","alpha")
        self.assertEqual(index["total"],1)
        self.assertEqual(index["verified"],0)

    def test_verified_requires_evidence_and_explicit_pass(self):
        d=self.make()
        base=("record","--project","alpha","--id",d["id"],"--status","verified")
        self.run_cli(*base,success=False)
        evidence=self.root/"QA.json";evidence.write_text('{"measured": true}',encoding="utf-8")
        self.run_cli(*base,"--evidence",str(evidence),success=False)
        v=self.run_cli(*base,"--evidence",str(evidence),"--qa-pass")
        self.assertEqual(v["status"],"verified")
        index=self.run_cli("catalog","--project","alpha")
        self.assertEqual(index["verified"],1)
        self.run_cli("record","--project","alpha","--id",d["id"],"--status","failed","--evidence",str(evidence),success=False)

    def test_self_learning_only_same_project(self):
        d=self.make()
        e=self.root/"QA";e.write_text("QA checked",encoding="utf-8")
        self.run_cli("record","--project","alpha","--id",d["id"],"--status","verified",
                     "--evidence",str(e),"--qa-pass")
        m=self.make(goal="مونتاج فيديو جديد")
        self.assertIn(d["id"],m["lessons_used_same_project_verified_only"])
        isolated=self.make(project="beta",goal="مونتاج فيديو جديد")
        self.assertEqual(isolated["lessons_used_same_project_verified_only"],[])

    def test_execution_trace_and_secret_block(self):
        d=self.make()
        p=self.root/"frame.png";p.write_bytes(b"not-an-image-only-proof-test")
        tr=self.run_cli("trace","--project","alpha","--id",d["id"],
                         "--stage","create","--action","Produced an intermediate asset",
                         "--tool","mock-render","--observed","file exists",
                         "--capabilities","SP-0001","--evidence",str(p))
        self.assertEqual(tr["stage"],"create")
        self.assertEqual(len(tr["evidence"]["sha256"]),64)
        stored=self.run_cli("show","--project","alpha","--id",d["id"])
        self.assertEqual(len(stored["execution_trace"]),1)
        self.run_cli("trace","--project","alpha","--id",d["id"],"--stage","create",
                     "--action","Bearer abcdefghijklmnopqrstuvwxyz",success=False)
        self.run_cli("show","--project","alpha","--id","../../bad",success=False)

if __name__=="__main__":
    unittest.main(verbosity=2)
