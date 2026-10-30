#!/usr/bin/env python3
"""SEE capability routing regression tests: no executor side effects."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "see_capability_bridge.py"
spec = importlib.util.spec_from_file_location("see_capability_bridge", SCRIPT)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class SeeCapabilityBridgeTests(unittest.TestCase):
    def test_self_tests(self):
        self.assertGreaterEqual(bridge.self_test(), 19)

    def test_catalog_contract(self):
        self.assertEqual(len(bridge.PACKS), 9)
        self.assertEqual(len(bridge.STAGE0), 11)
        self.assertEqual(len(set(bridge.PACKS)), 9)

    def test_image_not_video(self):
        result = bridge.route("اصنع صورة احترافية")
        self.assertEqual(result["branch"], "image_prompt")
        self.assertNotIn("kosif-media-motion", result["selected_method_packs"])

    def test_text_imitation_not_video(self):
        result = bridge.route("قلّد صياغة البريد", has_reference_video=True)
        self.assertEqual(result["branch"], "humanize")

    def test_reference_video_gate(self):
        self.assertEqual(bridge.route("قلد مونتاج الفيديو")["branch"],
                         "video_reference_missing")
        r = bridge.route("قلد مونتاج الفيديو", has_reference_video=True)
        self.assertEqual(r["branch"], "video_imitation")
        self.assertEqual(r["execution"]["owner"], "KOSIF Montage & Motion")

    def test_full_pro_not_fake(self):
        r = bridge.route("فعّل البرو", mode="standard")
        self.assertEqual(r["mode"], "full_pro")
        self.assertEqual(r["full_pro"]["state"], "NOT_FULL_PRO")
        self.assertFalse(r["execution"]["verified"])

    def test_limits(self):
        for mode, limit in (("fast", 2), ("standard", 2), ("deep", 4),
                            ("full_pro", 4)):
            r = bridge.route("طور مهارات SEE", mode)
            self.assertLessEqual(len(r["selected_method_packs"]), limit)
            self.assertLessEqual(r["dynamic_specialist_lookup"]["max_dynamic"],
                                 1 if limit == 2 else 2)

    def test_no_fake_execution_for_external(self):
        for task in ("ارسال رسالة واتساب", "تحكم في الكمبيوتر", "نشر الإصدار"):
            r = bridge.route(task)
            self.assertTrue(r["execution"]["requires_live_exposure_and_authorization"])
            self.assertEqual(r["execution"]["status"], "NOT_EXECUTED")

    def test_specialist_gap_no_automatic_install(self):
        r = bridge.route("احتاج مهندس FPGA")
        self.assertTrue(r["dynamic_specialist_lookup"]["eligible"])
        self.assertFalse(r["dynamic_specialist_lookup"]["activated"])

    def test_numeric_lock(self):
        self.assertTrue(bridge.route("طابق دفتر الحسابات")[
            "deterministic_numeric_verification"])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            bridge.route("")
        with self.assertRaises(ValueError):
            bridge.route("test", mode="no-such-mode")


if __name__ == "__main__":
    unittest.main()
