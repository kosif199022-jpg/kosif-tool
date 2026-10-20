"""Unit tests for KOSIF headless Blender animation exporter."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import blender_motion_video as m
SCENE = SK / "templates" / "blender-demo.json"

class VideoTests(unittest.TestCase):
    def test_sample(self):
        scene = json.loads(SCENE.read_text(encoding="utf-8-sig"))
        self.assertEqual(len(m.validate(scene)["objects"]), 2)

    def test_invalid_extension(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaisesRegex(ValueError, "MP4 only"):
                m.encode(SCENE, Path(t) / "bad.exe")

    def test_existing_output_is_unchanged(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "existing.mp4"
            out.write_bytes(b"keep this video")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                m.encode(SCENE, out)
            self.assertEqual(out.read_bytes(), b"keep this video")

    def test_missing_blender_no_implicit_install(self):
        with tempfile.TemporaryDirectory() as t:
            with mock.patch.object(m, "blender_exe", return_value=None):
                with self.assertRaisesRegex(ValueError, "required"):
                    m.encode(SCENE, Path(t) / "out.mp4")

    def test_invalid_scene_refused(self):
        with tempfile.TemporaryDirectory() as t:
            scene = Path(t) / "bad.json"
            data = json.loads(SCENE.read_text(encoding="utf-8-sig"))
            data["frames"] = 10000
            scene.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                m.encode(scene, Path(t) / "out.mp4")

    def test_cli_safe_subprocess_and_worker_compiles(self):
        import py_compile
        with tempfile.TemporaryDirectory() as t:
            py_compile.compile(str(SK / "scripts" / "blender_worker.py"),
                               cfile=str(Path(t) / "worker.pyc"), doraise=True)
        code = (SK / "scripts" / "blender_motion_video.py").read_text(encoding="utf-8-sig")
        self.assertIn('"--disable-autoexec"', code)
        self.assertIn("shell=False", code)
        self.assertIn("nb_read_frames", code)

if __name__ == "__main__":
    unittest.main()
