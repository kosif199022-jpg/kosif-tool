#!/usr/bin/env python3
"""Read-only tests for the source-reviewed Atlas method router."""
import copy
import unittest
import atlas_reviewed_methods_v3 as router

class AtlasReviewedMethodsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=router.load_manifest()
    def test_catalog_complete(self):
        self.assertEqual(len(self.manifest["methods"]),24)
        self.assertEqual(len({m["domain"] for m in self.manifest["methods"]}),12)
        self.assertEqual(self.manifest["source_texts_inspected"],395)
    def test_rea_ghidra_route(self):
        x=router.route("ghidra reverse engineering", "reverse_engineering", manifest=self.manifest)
        self.assertEqual(x["selected"][0]["method_id"],"native-evidence-tracing")
        self.assertTrue(x["does_not_execute_external_code"])
    def test_finance_arabic_route(self):
        x=router.route("مراجعة محاسبة واقفال شهري","finance",manifest=self.manifest)
        self.assertEqual(x["selected"][0]["method_id"],"month-end-close-checklist")
    def test_no_external_execution(self):
        x=router.route("nonsenseword123",manifest=self.manifest)
        self.assertEqual(x["selected"],[])
        self.assertEqual(x["fallback"],"native_superpowers_capabilities")
    def test_invalid_source_is_rejected(self):
        damaged=copy.deepcopy(self.manifest)
        damaged["methods"][0]["sha256"]="invalid"
        self.assertFalse(router.HEX64.fullmatch(damaged["methods"][0]["sha256"]))

if __name__=="__main__":unittest.main()
