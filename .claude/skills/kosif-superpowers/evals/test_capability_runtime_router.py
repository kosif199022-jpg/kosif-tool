"""KOSIF executable capability discovery, matching, security and truth-label tests."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "capability_runtime_router.py"
spec=importlib.util.spec_from_file_location("capability_runtime_router",SCRIPT)
router=importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)

class CapabilityRouterTests(unittest.TestCase):
    def test_all_registered_capabilities_load_and_ids_unique(self):
        rows=router.load_registry()
        self.assertGreaterEqual(len(rows),22)
        self.assertEqual(len(set(x["id"] for x in rows)),len(rows))

    def test_arabic_katana_routes_to_editable_original_engine(self):
        hits=router.route("اعمل محاكاة مونتاج فيديو بكاتانا لكن بالكود",router.load_registry())
        self.assertEqual(hits[0]["id"],"reference-edit-remix")
        self.assertIn("scripts/reference_edit_engine.py",hits[0]["runbook"])

    def test_practical_drawing_route_exists(self):
        hits=router.route("ارسم شخصية وقطة في مشهد بالموشن",router.load_registry())
        self.assertTrue(any(x["id"]=="code-drawing" for x in hits))

    def test_user_audio_routes_to_measured_audio(self):
        hits=router.route("حلل أغنية وصوت audio وتغيّرات الطاقة",router.load_registry(),limit=15)
        self.assertIn("sound-energy",[x["id"] for x in hits])

    def test_real_script_report_does_not_claim_completed_execution(self):
        row=next(x for x in router.load_registry() if x["id"]=="code-drawing")
        res=router.assess(row)
        self.assertTrue(res["source_present"])
        self.assertEqual(res["status"],"source_present_not_executed")
        self.assertFalse(res["executed_in_current_request"])
        self.assertFalse(res["verified_in_current_request"])

    def test_missing_ffmpeg_is_not_marked_ready(self):
        row=next(x for x in router.load_registry() if x["id"]=="reference-video-scan")
        with patch.object(router.shutil,"which",side_effect=lambda s: "/usr/bin/python3" if s=="python3" else None):
            info=router.assess(row)
        self.assertEqual(info["status"],"missing_host_prerequisites")
        self.assertEqual(info["missing_binaries"],["ffprobe","ffmpeg"])

    def test_ml_models_are_never_automatically_ready(self):
        for ident in ("pixel-tracking","segmentation","generated-video"):
            row=next(x for x in router.load_registry() if x["id"]==ident)
            info=router.assess(row)
            self.assertEqual(info["status"],"external_not_integrated")
            self.assertIsNone(info["runbook"])
            self.assertFalse(info["verified_in_current_request"])

    def test_no_permissions_auto_granted(self):
        for row in router.load_registry():
            report=router.assess(row)
            self.assertEqual(report["permission_status"],"not_verified_requires_host_or_user_authorization")
            self.assertEqual(report["permissions_required_not_granted"],row["permissions"])

    def test_reference_visual_route_is_source_not_authorized_video_access(self):
        rows=router.load_registry()
        row=next(x for x in rows if x["id"]=="reference-visual-style")
        info=router.assess(row)
        self.assertEqual(row["script"],"scripts/reference_visual_fingerprint.py")
        self.assertIn("ffmpeg",row["requires"])
        self.assertIn("media_usage_rights",info["permissions_required_not_granted"])
        self.assertFalse(info["executed_in_current_request"])
        self.assertFalse(info["verified_in_current_request"])

    def test_task_is_untrusted_plain_text_not_shell(self):
        text="'; rm -rf /; echo '"
        hits=router.route(text,router.load_registry())
        self.assertEqual(hits,[])
        src=SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("subprocess.run",src)
        self.assertNotIn("shell=True",src)
        self.assertNotIn("os.system",src)

    def test_schema_disallows_duplicate_ids_and_directory_traversal(self):
        rows=router.load_registry()
        with tempfile.TemporaryDirectory() as root:
            f=Path(root)/"bad.json"
            obj={"schema":"kosif.capability-routes.v1","routes":[rows[0],rows[0]]}
            f.write_text(json.dumps(obj))
            with self.assertRaises(ValueError):router.load_registry(f)
            changed=dict(rows[0],id="other",script="scripts/../../etc/passwd")
            obj["routes"]=[changed]
            f.write_text(json.dumps(obj))
            with self.assertRaises(ValueError):router.load_registry(f)

    def test_cli_returns_json_and_reports_missing_unknown_id(self):
        a=subprocess.run([sys.executable,str(SCRIPT),"--task","مونتاج كاتانا",
                          "--json"],capture_output=True,text=True,timeout=12)
        self.assertEqual(a.returncode,0,a.stderr)
        r=json.loads(a.stdout)
        self.assertEqual(r["choices"][0]["id"],"reference-edit-remix")
        b=subprocess.run([sys.executable,str(SCRIPT),"--id","no-such-capability"],
                         capture_output=True,text=True,timeout=12)
        self.assertEqual(b.returncode,2)
        self.assertEqual(json.loads(b.stderr)["status"],"failed")

    def test_doctor_does_not_use_network_or_make_changes(self):
        with patch.object(router.shutil,"which",return_value=None):
            info=[router.assess(x) for x in router.load_registry()]
        self.assertEqual(len(info),len(router.load_registry()))
        self.assertTrue(any(x["status"]=="missing_host_prerequisites" for x in info))
        self.assertTrue(any(x["status"]=="external_not_integrated" for x in info))

if __name__=="__main__": unittest.main()
