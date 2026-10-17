"""Tests for executable KOSIF Motion Runtime (no network, no library install)."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL=Path(__file__).resolve().parents[1]
SCRIPT=SKILL/"scripts"/"motion_runtime.py"
spec=importlib.util.spec_from_file_location("motion_runtime",SCRIPT)
motion=importlib.util.module_from_spec(spec)
spec.loader.exec_module(motion)


class MotionRuntimeTests(unittest.TestCase):
    def test_25_engine_capability_registry(self):
        rows=motion.read_engines()
        self.assertEqual(len(rows),25)
        self.assertEqual(len({x["repo"] for x in rows}),25)
        self.assertTrue(all(x["status"]=="source_understood_adapter_or_recipe_not_bundled" for x in rows))
        self.assertEqual(len({x["id"] for x in rows}),25)

    def test_runtime_has_no_external_dependency(self):
        self.assertTrue(motion.TEMPLATE.is_file())
        self.assertIsInstance(motion.make_html("قصيف","الرسم بالكود"),str)

    def test_arabic_and_html_are_escaped(self):
        film=motion.make_html("<script>alert(1)</script>","& ومرحبًا")
        self.assertNotIn("<script>alert(1)</script>",film)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;",film)
        self.assertIn("&amp; ومرحبًا",film)

    def test_scaffold_creates_editable_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"film"
            result=motion.scaffold(target,"رسوم قصيف","تعمل بالكود",8,30)
            self.assertEqual(result["status"],"scaffold_created_not_rendered")
            self.assertFalse(result["render_verified"])
            self.assertTrue((target/"film.html").is_file())
            meta=json.loads((target/"motion.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["aspect"],"9:16")
            self.assertFalse(meta["render_verified"])

    def test_prevents_overwrite_of_existing_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"film"
            target.mkdir()
            (target/"important.txt").write_text("keep me")
            with self.assertRaises(ValueError):
                motion.scaffold(target,"Test","Example",8,30)
            self.assertEqual((target/"important.txt").read_text(),"keep me")

    def test_has_deterministic_seek_contract_and_stroke_paths(self):
        sample=motion.make_html("film","captions",8,30)
        self.assertIn("window.__kosif={duration,fps,seek};",sample)
        self.assertIn("getPointAtLength",sample)
        self.assertIn("strokeDashoffset",sample)
        self.assertIn('id="camera"',sample)
        self.assertIn('id="character"',sample)
        self.assertGreaterEqual(sample.count('data-start='),12)
        self.assertIn("document.fonts.ready",sample)

    def test_duration_fps_validation(self):
        for duration,fps in ((7,30),(121,30),(8,23),(8,61),(0,30)):
            with self.subTest(duration=duration,fps=fps),self.assertRaises(ValueError):
                motion.make_html("title","subtitle",duration,fps)

    def test_long_text_rejected_not_clipped(self):
        with self.assertRaises(ValueError):
            motion.make_html("A"*37,"OK")

    def test_render_is_opt_in(self):
        result=motion.render("fake.html","fake.mp4")
        self.assertEqual(result["status"],"approval_required")
        self.assertFalse(result["executed"])

    def test_render_never_replaces_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/"film.html";src.write_text(motion.make_html("X","Y"))
            dst=Path(tmp)/"film.mp4";dst.write_bytes(b"original")
            with patch.object(motion.subprocess,"run") as run:
                with self.assertRaises(ValueError):
                    motion.render(src,dst,approved=True)
                run.assert_not_called()
            self.assertEqual(dst.read_bytes(),b"original")

    def test_render_disallows_arbitrary_output_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/"film.html";src.write_text("ok")
            with self.assertRaises(ValueError):
                motion.render(src,Path(tmp)/"script.sh",approved=True)

    def test_cli_doctor_reports_real_probes_not_rendered(self):
        p=subprocess.run([sys.executable,str(SCRIPT),"doctor"],capture_output=True,
                         text=True,timeout=8)
        self.assertEqual(p.returncode,0,p.stderr)
        status=json.loads(p.stdout)
        self.assertFalse(status["mp4_render_verified"])

    def test_cli_scaffold_and_engines(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"scene"
            r=subprocess.run([sys.executable,str(SCRIPT),"scaffold","--out",str(target),
                             "--title","قصيف","--subtitle","موشن جرافيك"],
                              capture_output=True,text=True,timeout=8)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertTrue((target/"film.html").is_file())
            e=subprocess.run([sys.executable,str(SCRIPT),"engines","--family","whiteboard"],
                             capture_output=True,text=True,timeout=8)
            self.assertEqual(e.returncode,0,e.stderr)
            data=json.loads(e.stdout)
            self.assertTrue(all(x["family"]=="whiteboard" for x in data["engines"]))
            self.assertFalse(data["installed_runtime_verified"])


if __name__=="__main__":
    unittest.main()
