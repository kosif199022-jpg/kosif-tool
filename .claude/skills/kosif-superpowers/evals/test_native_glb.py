"""Tests for the original KOSIF Blender-free glTF 2.0 binary exporter."""
import json
import struct
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
from native_glb import glb


class BlenderFreeGLBTests(unittest.TestCase):
    def scene(self):
        return {
            "schema": "kosif.blender.v1", "frames": 48, "fps": 24,
            "size": [512,512],
            "objects": [
                {"shape": "cube", "color": [0.2,0.48,0.36,1],
                 "keyframes": [
                     {"frame":1, "location":[-1,0,0]},
                     {"frame":48, "location":[1,0,0]}]},
                {"shape": "sphere", "location": [1,0,0],
                 "color": [0.7,0.47,0.28,1]},
            ],
        }

    def test_gltf_binary_header_and_geometry(self):
        content = glb(self.scene())
        self.assertEqual(content[:4], b"glTF")
        self.assertEqual(struct.unpack_from("<I", content, 4)[0], 2)
        self.assertEqual(struct.unpack_from("<I", content, 8)[0], len(content))
        length = struct.unpack_from("<I", content, 12)[0]
        doc = json.loads(content[20:20+length])
        self.assertEqual(doc["asset"]["version"], "2.0")
        self.assertEqual(len(doc["nodes"]), 2)
        self.assertEqual(len(doc["meshes"]), 2)
        self.assertEqual(len(doc["materials"]), 2)
        self.assertEqual(len(doc["animations"]), 1)
        self.assertEqual(doc["buffers"][0]["byteLength"], len(content)-(20+length+8))
        self.assertEqual(doc["meshes"][0]["primitives"][0]["attributes"].keys(), {"POSITION"})

    def test_no_blender_binary_or_bpy_dependency(self):
        import native_glb
        source = Path(native_glb.__file__).read_text(encoding="utf-8")
        self.assertNotIn("import bpy", source)
        self.assertNotIn("subprocess", source)
        self.assertNotIn("blender.exe", source)

    def test_rejects_invalid_and_unbounded_inputs(self):
        base = self.scene()
        for field, value in [
            ("frames", 999), ("fps", 0), ("objects", []),
            ("objects", [{"shape":"shader_code"}]),
            ("objects", [{"shape":"cube","location":[float("nan"),0,0]}]),
            ("objects", [{"shape":"cube","keyframes":[
                {"frame":20,"location":[0,0,0]},
                {"frame":10,"location":[1,0,0]}]}]),
        ]:
            with self.subTest(field=field, value=str(value)[:30]):
                with self.assertRaises(ValueError):
                    glb({**base, field:value})

    def test_deterministic_bytes(self):
        a = self.scene()
        self.assertEqual(glb(a), glb(a))

    def test_blender_demo_scene_compatibility(self):
        sample = SKILL / "templates" / "blender-demo.json"
        self.assertTrue(sample.is_file())
        content = glb(json.loads(sample.read_text(encoding="utf-8-sig")))
        self.assertTrue(content.startswith(b"glTF"))
        self.assertGreater(len(content), 1000)


class GLBAxisAndCLITests(unittest.TestCase):
    SCRIPT = SKILL / "scripts" / "native_glb.py"

    @staticmethod
    def parse(content):
        length = struct.unpack_from("<I", content, 12)[0]
        doc = json.loads(content[20:20+length])
        return doc, content[20+length+8:]

    @staticmethod
    def vec3(doc, binary, accessor_id):
        item = doc["accessors"][accessor_id]
        view = doc["bufferViews"][item["bufferView"]]
        raw = binary[view["byteOffset"]:view["byteOffset"]+view["byteLength"]]
        return [list(struct.unpack_from("<3f", raw, 12*i)) for i in range(item["count"])]

    def test_blender_z_up_becomes_gltf_y_up(self):
        doc, binary = self.parse(glb({
            "schema": "kosif.blender.v1", "frames": 24, "fps": 24,
            "objects": [
                {"shape": "cube", "location": [0, 0, 3]},
                {"shape": "sphere", "location": [1, 2, 3], "scale": [1, 2, 3],
                 "keyframes": [{"frame": 1, "location": [1, 2, 3]},
                               {"frame": 24, "location": [0, 0, 5]}]},
            ]}))
        self.assertEqual(doc["nodes"][0]["translation"], [0.0, 3.0, 0.0])
        self.assertEqual(doc["nodes"][1]["translation"], [1.0, 3.0, -2.0])
        self.assertEqual(doc["nodes"][1]["scale"], [1.0, 3.0, 2.0])
        sampler = doc["animations"][0]["samplers"][0]
        self.assertEqual(self.vec3(doc, binary, sampler["output"]),
                         [[1.0, 3.0, -2.0], [0.0, 5.0, 0.0]])
        sphere = self.vec3(doc, binary,
                           doc["meshes"][1]["primitives"][0]["attributes"]["POSITION"])
        self.assertEqual(sphere[0], [0.0, 1.0, 0.0])  # the Z-up north pole now points up +Y

    def run_cli(self, scene, output):
        return subprocess.run([sys.executable, str(self.SCRIPT), "--scene", str(scene),
                               "--output", str(output)], capture_output=True, text=True)

    def test_cli_reports_bad_scene_and_missing_folder_without_traceback(self):
        with TemporaryDirectory() as folder:
            bad = Path(folder) / "cylinder.json"
            bad.write_text(json.dumps({"schema": "kosif.blender.v1",
                                       "objects": [{"shape": "cylinder"}]}), encoding="utf-8")
            run = self.run_cli(bad, Path(folder) / "cyl.glb")
            self.assertEqual(run.returncode, 1)
            self.assertNotIn("Traceback", run.stderr)
            self.assertFalse(json.loads(run.stderr)["ok"])
            self.assertFalse((Path(folder) / "cyl.glb").exists())
            run = self.run_cli(SKILL / "templates" / "blender-demo.json",
                               Path(folder) / "missing" / "scene.glb")
            self.assertEqual(run.returncode, 2)
            self.assertNotIn("Traceback", run.stderr)
            run = self.run_cli(SKILL / "templates" / "blender-demo.json", Path(folder) / "ok.glb")
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue((Path(folder) / "ok.glb").read_bytes().startswith(b"glTF"))


if __name__ == "__main__":
    unittest.main()
