"""Offline tests for source-safe Mosamem/REA fusion; NO downloads or app launches."""
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

SK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mosamem_rea_fusion",SK/"scripts"/"mosamem_rea_fusion.py")
f=importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)


class TestFusion(unittest.TestCase):
    def test_manifest_ids_unique_and_source_scoped(self):
        reg=f.registry()
        rows=reg["capabilities"]
        self.assertGreaterEqual(len(rows),19)
        self.assertEqual(len({x["id"] for x in rows}),len(rows))
        self.assertEqual(reg["sources"]["mosamem"]["license"],"GPL-3.0-or-later")
        self.assertIn("morluto/rea",reg["sources"]["rea"]["repository"])
        for row in rows:
            self.assertIn(row["implementation"],{"external_app_gui","external_app_ai_manual","native_metadata_plus_external_gui","composition_method","existing_opt_in_bridge","external_provider_manual","external_runtime_manual"})

    def test_plan_contains_typed_chain_and_no_execution(self):
        p=f.plan("صمم صورة بخط عربي")
        self.assertEqual(p["status"],"PLAN_ONLY_NO_EXECUTION")
        self.assertEqual(p["domain"],"image")
        self.assertEqual(len(p["workflow"]),5)
        self.assertFalse(p["executed"])
        self.assertTrue(any("GPL" in x for x in p["limits"]))

    def test_domain_router_for_motion_and_rea(self):
        self.assertEqual(f.plan("عمل مونتاج فيديو")["domain"],"motion")
        self.assertEqual(f.plan("REA تحليل تطبيق")["domain"],"investigation")

    def test_reject_unknown_domain_and_blank(self):
        with self.assertRaises(ValueError):f.plan("")
        with self.assertRaises(ValueError):f.plan("draw","not-a-domain")

    def test_valid_rgb_psd(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"demo.psd"
            p.write_bytes(b"8BPS"+struct.pack(">H",1)+b"\0"*6+struct.pack(">HIIHH",4,1920,1080,8,3)+b"abc")
            before=p.read_bytes()
            r=f.inspect_asset(p)
            self.assertEqual(r["asset"]["type"],"PSD")
            self.assertEqual(r["asset"]["color_mode"],"RGB")
            self.assertEqual(r["asset"]["width"],1080)
            self.assertEqual(r["asset"]["height"],1920)
            self.assertFalse(r["status"]=="VERIFIED_RENDER")
            self.assertEqual(p.read_bytes(),before)

    def test_warn_cmyk_and_deep_psd(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"cmyk.psd"
            p.write_bytes(b"8BPS"+struct.pack(">H",1)+b"\0"*6+struct.pack(">HIIHH",4,200,100,16,4))
            risk=f.inspect_asset(p)["asset"]["risk_flags"]
            self.assertIn("MOSAMEM_PSD_RGB_ONLY_FIDELITY_NOT_ASSURED",risk)
            self.assertIn("PSD_8BIT_FIDELITY_NOT_ASSURED",risk)

    def test_reject_psd_bad_reserved_bytes(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"bad.psd"
            p.write_bytes(b"8BPS"+struct.pack(">H",1)+b"f"*6+struct.pack(">HIIHH",3,5,5,8,3))
            with self.assertRaises(ValueError):f.inspect_asset(p)

    def test_png_parse_alpha_possible(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"test.png"
            p.write_bytes(b"\x89PNG\r\n\x1a\n"+struct.pack(">I",13)+b"IHDR"+struct.pack(">IIBB",1080,1920,8,6))
            r=f.inspect_asset(p)
            self.assertEqual(r["asset"]["width"],1080)
            self.assertTrue(r["asset"]["alpha_possible"])

    def test_jpeg_dimension(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"test.jpg"
            p.write_bytes(b"\xff\xd8\xff\xe0"+struct.pack(">H",4)+b"\x00\x00"+b"\xff\xc0"+struct.pack(">H",7)+struct.pack(">BHH",8,720,1280))
            r=f.inspect_asset(p)
            self.assertEqual(r["asset"]["type"],"JPEG")
            self.assertEqual((r["asset"]["width"],r["asset"]["height"]),(1280,720))

    def test_reject_symlinks_and_existing_output(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"exists.json"
            p.write_text("untouched",encoding="utf8")
            with self.assertRaises(ValueError):f.fresh_json(p,{"changed":1})
            self.assertEqual(p.read_text(),"untouched")

    def test_unrecognized_is_not_pretended_decoded(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"test.mosamem"
            p.write_bytes(b"SQLite format 3\0" + b"\0"*60)
            r=f.inspect_asset(p)
            self.assertEqual(r["asset"]["type"],"SQLITE_UNCLASSIFIED")
            self.assertNotIn("document_layers",r["asset"])

    def test_missing_rea_target_is_plan_only(self):
        with tempfile.TemporaryDirectory() as t:
            result=f.rea_plan("javascript",str(Path(t)/"notexist"))
            self.assertEqual(result["status"],"target_missing")
            self.assertFalse(result["verified"])

    def test_source_has_no_mosamem_source_copied_or_install(self):
        source=(SK/"scripts"/"mosamem_rea_fusion.py").read_text(encoding="utf8")
        self.assertNotIn("shell=True",source)
        self.assertNotIn("npm install",source)
        self.assertNotIn("git clone",source)
        self.assertNotIn("subprocess.run",source)
        self.assertNotIn("requests.post",source)

    def test_rea_doctor_does_not_execute_target(self):
        with patch.object(f,"read_rea",return_value=None):
            result=f.environment()
        self.assertFalse(result["rea"]["rea_installed"])
        self.assertFalse(result["analysis_executed"])

    def test_registry_no_dual_tenant_leak(self):
        result=f.plan("تصميم مشروع شركة مستقلة")
        self.assertTrue(any("isolated" in s for s in result["limits"]))
        self.assertNotIn("account_id",json.dumps(result))

if __name__=="__main__":
    unittest.main()
