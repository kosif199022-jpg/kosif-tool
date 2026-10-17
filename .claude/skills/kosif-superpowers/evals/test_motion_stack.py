"""Test third-party motion stack scaffolds, manifest truthfulness, and no install."""
import importlib.util
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"motion_stack.py"
spec=importlib.util.spec_from_file_location("motion_stack",SCRIPT)
stack=importlib.util.module_from_spec(spec)
spec.loader.exec_module(stack)


class MotionStackTests(unittest.TestCase):
    def test_manifest_25_source_repos_unique(self):
        sources=stack.validate_registry()
        self.assertEqual(len(sources),25)
        self.assertEqual(len({s["repo"].lower() for s in sources}),25)
        self.assertTrue(any(s["repo"]=="remotion-dev/remotion" and s["license_hint"]=="special-license" for s in sources))
        self.assertTrue(all(s["runtime_state"]=="not_probed" for s in sources))

    def test_three_original_scaffold_backends_exist(self):
        self.assertEqual(set(stack.recipes()),{"gsap","remotion","manim","three","pixi","p5"})

    def test_all_backends_create_editable_sources_without_install(self):
        for name in stack.recipes():
            with self.subTest(name=name),tempfile.TemporaryDirectory() as root:
                dest=Path(root)/name
                receipt=stack.scaffold(name,dest)
                self.assertEqual(receipt["status"],"scaffold_created_not_installed")
                self.assertFalse(receipt["runtime_ready"])
                self.assertTrue(receipt["installation_requires_user_approval"])
                self.assertTrue(all((dest/p).exists() for p in receipt["files"]))

    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as root:
            dest=Path(root)/"scaffold"
            stack.scaffold("gsap",dest)
            with self.assertRaises(ValueError):
                stack.scaffold("gsap",dest)

    def test_gsap_integrates_three_libraries_and_deterministic_seek(self):
        s=stack.recipes()["gsap"]["src/main.js"]
        for term in ["'gsap'","'roughjs'","'vivus'","window.__kosif","seek(sec)",
                     "strokeDashoffset","setFrameProgress"]:
            self.assertIn(term,s)

    def test_remotion_composition_has_frame_contract(self):
        files=stack.recipes()["remotion"]
        self.assertEqual(files["package.json"][:1],"{")
        self.assertIn("durationInFrames={270}",files["src/root.jsx"])
        self.assertIn("useCurrentFrame",files["src/video.jsx"])

    def test_manin_has_scene_with_path(self):
        self.assertIn("class KOSIFExplain(Scene)",stack.recipes()["manim"]["main.py"])
        self.assertIn("MoveAlongPath",stack.recipes()["manim"]["main.py"])

    def test_three_pixi_and_p5_use_real_frame_seek_contract(self):
        for name, module in (("three","three"),("pixi","pixi.js"),("p5","p5")):
            with self.subTest(backend=name):
                files=stack.recipes()[name]
                source=files["src/main.js"]
                pkg=json.loads(files["package.json"])
                self.assertIn(module,pkg["dependencies"])
                self.assertIn("window.__kosif",source)
                self.assertIn("seek(",source)
                self.assertIn("vite",pkg["scripts"]["build"])

    def test_doctor_does_not_claim_runtime(self):
        self.assertFalse(stack.doctor()["third_party_motion_engines_verified"])

    def test_no_shell_exec_or_auto_install(self):
        content=SCRIPT.read_text(encoding="utf8")
        self.assertNotIn("shell=True",content)
        self.assertNotIn("subprocess.run(",content)
        self.assertNotIn("npm install",content)

    def test_cli_list_is_truthful(self):
        p=subprocess.run([sys.executable,str(SCRIPT),"list"],capture_output=True,text=True,timeout=10)
        self.assertEqual(p.returncode,0,p.stderr)
        info=json.loads(p.stdout)
        self.assertEqual(info["count"],25)
        self.assertEqual(info["runtime_status"],"not_probed")


if __name__=="__main__":
    unittest.main()
