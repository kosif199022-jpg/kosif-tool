"""Motion engine integration tests, including executable animation contract and input limits."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"motion_director.py"
ENGINE=Path(__file__).resolve().parents[1]/"assets"/"motion_engine.js"
spec=importlib.util.spec_from_file_location("motion_director",SCRIPT)
motion=importlib.util.module_from_spec(spec)
spec.loader.exec_module(motion)


class MotionDirectorTests(unittest.TestCase):
    def setUp(self):
        self.data=motion.sample()

    def test_sample_is_complete_audio_timed_spec(self):
        stats=motion.validate(self.data)
        self.assertEqual(stats["scenes"],3)
        self.assertEqual(stats["frames"],270)
        self.assertEqual(stats["format"],"1080x1920")

    def test_all_required_motion_types_present(self):
        types={e["type"] for s in self.data["scenes"] for e in s["elements"]}
        self.assertTrue({"text","circle","path","character"}.issubset(types))

    def test_scene_gap_rejected(self):
        self.data["scenes"][1]["start"]=3.1
        with self.assertRaises(ValueError):
            motion.validate(self.data)

    def test_overlapping_captions_rejected(self):
        self.data["scenes"][0]["words"][1]["start"]=0.5
        with self.assertRaises(ValueError):
            motion.validate(self.data)

    def test_untrusted_svg_path_rejected(self):
        self.data["scenes"][0]["elements"][1]["d"]="<script>alert(1)</script>"
        with self.assertRaises(ValueError):
            motion.validate(self.data)

    def test_link_or_style_injection_rejected(self):
        self.data["scenes"][0]["elements"][1]["stroke"]="url(https://attacker.example/payload)"
        with self.assertRaises(ValueError):
            motion.validate(self.data)

    def test_excessive_elements_rejected(self):
        self.data["scenes"][0]["elements"]=[self.data["scenes"][0]["elements"][1]]*81
        with self.assertRaises(ValueError):
            motion.validate(self.data)

    def test_time_must_not_be_nan(self):
        self.data["duration"]=float("nan")
        with self.assertRaises(ValueError):
            motion.validate(self.data)

    def test_invalid_fps_rejected(self):
        self.data["fps"]=120
        with self.assertRaises(ValueError):
            motion.validate(self.data)

    def test_no_html_script_breakout(self):
        # Text content is data, never privileged markup. It must remain escaped in JSON.
        self.data["scenes"][0]["elements"][0]["text"]="</script><script>evil()</script>"
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/"movie.html"
            result=motion.compile_spec(self.data,target)
            html=target.read_text(encoding="utf-8")
            self.assertNotIn("</script><script>evil()",html)
            self.assertIn("\\u003c/script\\u003e",html)
            self.assertEqual(result["status"],"html_compiled_not_rendered")
            self.assertIn("window.__kosif",html)

    def test_compile_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/"x.html"
            motion.compile_spec(self.data,target)
            with self.assertRaises(ValueError):
                motion.compile_spec(self.data,target)

    def test_cli_sample_then_compile(self):
        with tempfile.TemporaryDirectory() as d:
            src=str(Path(d)/"scene.json")
            out=str(Path(d)/"movie.html")
            r=subprocess.run([sys.executable,str(SCRIPT),"sample","--out",src],
                             capture_output=True,text=True,timeout=8)
            self.assertEqual(r.returncode,0,r.stderr)
            r=subprocess.run([sys.executable,str(SCRIPT),"compile",src,"--out",out],
                             capture_output=True,text=True,timeout=8)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertTrue(Path(out).is_file())

    def test_renderer_refuses_unavailable_or_missing_html(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                motion.render(Path(d)/"does-not-exist.html",Path(d)/"out.mp4")

    def test_engine_contract_has_seek_and_draw_features(self):
        code=ENGINE.read_text(encoding="utf-8")
        for feature in ("window.__kosif","strokeDashoffset","data-scene",
                        "getTotalLength","captions.replaceChildren","setAttribute('transform'"):
            self.assertIn(feature,code)

    def test_no_external_network_or_package_download(self):
        for body in (SCRIPT.read_text(encoding="utf-8"),ENGINE.read_text(encoding="utf-8")):
            self.assertNotIn("shell=True",body)
            self.assertNotIn("npm install",body)
            self.assertNotIn("fetch(",body)


if __name__=="__main__":
    unittest.main()
