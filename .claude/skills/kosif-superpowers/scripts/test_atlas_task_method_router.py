#!/usr/bin/env python3
"""Executable routing regression tests for the 15 reviewed Atlas method candidates."""
import importlib.util
import unittest
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("atlas_task_method_router",HERE/"atlas_task_method_router.py")
router=importlib.util.module_from_spec(spec);spec.loader.exec_module(router)
MANIFEST=json.loads((HERE.parent/"data/atlas-method-provenance-20261020.json").read_text(encoding="utf-8-sig"))

class RoutingTests(unittest.TestCase):
    def test_manifest_has_15_reviewed_candidates(self):self.assertEqual(len(MANIFEST["method_candidates"]),15)
    def test_no_trigger_keeps_native(self):
        r=router.route("2+2",MANIFEST)
        self.assertEqual(r["selected_count"],0);self.assertEqual(r["fallback"],"native_kosif_superpowers")
    def test_root_cause(self):
        r=router.route("حلل السبب الجذري للخطأ",MANIFEST)
        self.assertEqual(r["selected"][0]["method"],"cause_chain_and_reversal_check")
    def test_finance_specific(self):
        r=router.route("أعمل توقع التدفق النقدي لمدة 13 أسبوع",MANIFEST)
        self.assertEqual(r["selected"][0]["method"],"weekly_liquidity_projection")
    def test_rea_binaries(self):
        r=router.route("استخدم ghidra للهندسة العكسية",MANIFEST)
        self.assertIn("binary_trace_evidence_checklist",[x["method"] for x in r["selected"]])
    def test_video_render(self):
        r=router.route("فحص تصدير الفيديو باستخدام ffmpeg",MANIFEST)
        self.assertIn("media_transcode_probe_validation",[x["method"] for x in r["selected"]])
    def test_ui_regression(self):
        r=router.route("استخدم playwright اختبار الواجهات",MANIFEST)
        self.assertIn("interactive_ui_regression",[x["method"] for x in r["selected"]])
    def test_security_collision_bounded(self):
        r=router.route("Agent security and threat model, prompt injection and agent guardrail",MANIFEST)
        self.assertLessEqual(r["selected_count"],2)
    def test_license_sensitive_ias_not_auto_route(self):
        r=router.route("اشرح معيار IAS 16",MANIFEST)
        self.assertEqual(r["selected_count"],0)
    def test_no_fake_execution(self):
        r=router.route("أعمل توقع السيولة",MANIFEST)
        self.assertFalse(r["selected"][0]["third_party_code_executed"])
        self.assertFalse(r["selected"][0]["executor_exposed"])
    def test_all_references_exist(self):
        for v in MANIFEST["method_candidates"]:
            self.assertTrue(v["sha256"])
            self.assertTrue(v["source_path"].endswith("/SKILL.md"))
    def test_unsupported_max_fails_closed(self):
        with self.assertRaises(ValueError):router.route("ffmpeg",MANIFEST,100)
if __name__=="__main__":unittest.main()
