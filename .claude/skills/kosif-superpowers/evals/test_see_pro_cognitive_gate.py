#!/usr/bin/env python3
"""Deterministic regression tests for the SEE Pro cognitive packet validation gate."""
import copy
import importlib.util
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "scripts" / "see_pro_cognitive_gate.py"
spec = importlib.util.spec_from_file_location("see_cognitive", SRC)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

def sample():
    return {
        "schema": c.SCHEMA, "level": "L3", "mode": "deep", "phase": "planning",
        "stage0": {"goal": "Produce a video", "artifact": "video",
                   "success_criteria": ["Final MP4 checks pass"]},
        "methods": [{"name": "kosif-media-motion"}, {"name": "kosif-eval-trust"}],
        "composition": {"nodes": [
            {"id": "N1", "input_kind": "audio", "output_kind": "video"},
            {"id": "N2", "input_kind": "video", "output_kind": "report"}
        ], "edges": [{"from": "N1", "to": "N2", "kind": "video", "relation": "verify"}]},
        "options": [{"id": "A", "strategy_key": "direct-composition"},
                    {"id": "B", "strategy_key": "cross-domain-typed-pipeline"},
                    {"id": "C", "strategy_key": "alternative-multimodal-engine"}],
        "claims": {"executed": False, "verified": False,
                   "full_pro_completed": False, "reviewers_executed": 0},
        "privacy": {"cross_tenant_data": False}
    }

class CognitiveGateTests(unittest.TestCase):
    def assert_bad(self, doc, expected):
        errors,_,_ = c.validate(doc)
        self.assertIn(expected,errors)

    def test_base_deep_packet(self):
        e,w,s=c.validate(sample())
        self.assertEqual(e,[])
        self.assertEqual(s["status"],"PASS")

    def test_fullpro_not_inferred_from_metadata(self):
        p=sample()
        p["mode"]="full_pro"
        p["claims"]["full_pro_completed"]=True
        p["receipts"]={"full_pro":{"request_id":"mock","status":"available"}}
        self.assert_bad(p,"FULL_PRO_CLAIM_UNPROVEN")

    def test_five_packs_over_deep_budget(self):
        p=sample()
        p["methods"]=[{"name":n} for n in sorted(c.PACKS)[:5]]
        self.assert_bad(p,"METHOD_PACK_LIMIT")

    def test_dynamic_requires_source_and_gap(self):
        p=sample()
        p["methods"].append({"name":"Atlas method","type":"dynamic"})
        self.assert_bad(p,"DYNAMIC_SOURCE_NOT_READ")
        self.assert_bad(p,"DYNAMIC_WITHOUT_NAMED_GAP")

    def test_type_safe_handoff(self):
        p=sample()
        p["composition"]["edges"][0]["kind"]="audio"
        self.assert_bad(p,"EDGE_SOURCE_KIND_MISMATCH")

    def test_three_real_architectures(self):
        p=sample()
        p["options"]=[{"id":i,"strategy_key":"same"} for i in "ABC"]
        self.assert_bad(p,"PLANS_NOT_MEANINGFULLY_DISTINCT")

    def test_numeric_deterministic_lock(self):
        p=sample()
        p["numeric"]={"exact_claim":True}
        self.assert_bad(p,"EXACT_NUMERIC_CLAIM_UNPROVEN")

    def test_isolation(self):
        p=sample()
        p["privacy"]["cross_tenant_data"]=True
        self.assert_bad(p,"CROSS_TENANT_DENIED")
        p["privacy"]["cross_tenant_data"]=False
        p["privacy"]["export_raw_client_data"]=True
        self.assert_bad(p,"RAW_CLIENT_DATA_EXPORT_DENIED")

    def test_500_experts_not_500_executions(self):
        p=sample()
        p["claims"]["reviewers_executed"]=500
        self.assert_bad(p,"REVIEWERS_CLAIM_UNPROVEN")

    def test_execution_and_verification_evidence(self):
        p=sample()
        p["claims"]["executed"]=True
        self.assert_bad(p,"EXECUTION_CLAIM_UNPROVEN")
        p["claims"]["verified"]=True
        self.assert_bad(p,"VERIFIED_CLAIM_UNPROVEN")

    def test_provenance(self):
        p=sample()
        p["facts"]=[{"claim":"unproved source","status":"supported"}]
        self.assert_bad(p,"FACT_SOURCE_MISSING")

    def test_no_secrets(self):
        p=sample()
        p["private_reference"]="Bearer abcdefghijklmnopqrstuvwxyz0123456789"
        self.assert_bad(p,"SECRET_PATTERN_DETECTED")

    def test_fast_does_not_force_plans(self):
        p=sample()
        p.update(level="L0",mode="fast",phase="answer",methods=[],options=[])
        self.assertNotIn("THREE_PLANS_MISSING",c.validate(p)[0])

if __name__ == "__main__":
    unittest.main(verbosity=2)
