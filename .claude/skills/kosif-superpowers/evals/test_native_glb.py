"""Tests for the original KOSIF Blender-free glTF 2.0 binary exporter."""
import json
import struct
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


if __name__ == "__main__":
    unittest.main()
