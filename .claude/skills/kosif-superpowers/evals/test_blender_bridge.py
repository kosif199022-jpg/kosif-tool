"""Scene validation and process invocation tests; no Blender runtime is simulated as verified."""
import json
from pathlib import Path
import sys
import tempfile
from unittest import TestCase, mock

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import blender_bridge as bridge


class BlenderBridgeTests(TestCase):
    def setUp(self):
        self.scene = {
            "schema": "kosif.blender.v1", "size": [512, 512], "fps": 24,
            "frames": 48, "objects": [
                {"shape": "cube", "keyframes": [
                    {"frame": 1, "location": [0, 0, 0]},
                    {"frame": 48, "location": [2, 0, 0]}]}]}

    def test_sample_scene(self):
        path = SK / "templates" / "blender-demo.json"
        self.assertEqual(len(bridge.validate(json.loads(path.read_text(encoding="utf-8-sig")))["objects"]), 2)

    def test_reject_unsafe_or_unbounded_values(self):
        cases = [
            {"objects": [{"shape": "__import__('os').system('calc')"}]},
            {"objects": [{"shape": "cube", "location": [float("inf"), 0, 0]}]},
            {"objects": [{"shape": "cube"}] * 13},
            {"size": [12000, 12000]},
            {"frames": 9999},
            {"objects": [{"shape": "cube", "keyframes": [
                {"frame": 20, "location": [0, 0, 0]},
                {"frame": 10, "location": [0, 0, 0]}]}]}]
        for change in cases:
            with self.subTest(change=str(change)[:60]):
                with self.assertRaises(ValueError):
                    bridge.validate({**self.scene, **change})

    def test_no_automatic_install_or_unavailable_fallback(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(bridge, "blender_exe", return_value=None):
            base = Path(temp)
            source = base / "scene.json"
            source.write_text(json.dumps(self.scene))
            with self.assertRaisesRegex(ValueError, "not installed"):
                bridge.render(source, base / "out.glb")

    def test_refuse_overwrite_and_nonstandard_output(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source, out = base / "s.json", base / "o.png"
            source.write_text(json.dumps(self.scene))
            out.write_text("existing")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                bridge.render(source, out)
            with self.assertRaisesRegex(ValueError, "PNG, BLEND, or GLB"):
                bridge.render(source, base / "output.exe")

    def test_command_is_argv_and_autoexec_is_disabled(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source, out = base / "s.json", base / "o.glb"
            source.write_text(json.dumps(self.scene))
            def fake_process(cmd, **kwargs):
                self.assertEqual(cmd[1:4], ["--background", "--factory-startup", "--disable-autoexec"])
                self.assertEqual(cmd[-2:], [str(source.resolve()), str(out.resolve())])
                self.assertFalse(kwargs["shell"])
                out.write_bytes(b"mocked-output-is-not-actual-Blender-render-123")
                return mock.Mock(returncode=0, stderr="", stdout="")
            with mock.patch.object(bridge, "blender_exe", return_value="blender"), mock.patch.object(
                bridge.subprocess, "run", side_effect=fake_process
            ):
                result = bridge.render(source, out)
            self.assertTrue(result["verified_file"])
            self.assertEqual(result["format"], "glb")

    def test_worker_compiles_without_bpy(self):
        import py_compile
        with tempfile.TemporaryDirectory() as temp:
            py_compile.compile(str(SK / "scripts" / "blender_worker.py"),
                               cfile=str(Path(temp) / "worker.pyc"), doraise=True)
