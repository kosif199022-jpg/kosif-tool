"""Tests for scripts/image_local_ai.py. Nothing is downloaded: the ONNX models are tiny synthetic
graphs built here (with onnx.helper when installed, else encoded by hand in protobuf wire format).
The inference tests skip when onnxruntime, numpy or Pillow is missing."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "scripts" / "image_local_ai.py"
spec = importlib.util.spec_from_file_location("image_local_ai", PATH)
ila = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ila)


def have(*mods):
    for m in mods:
        if importlib.util.find_spec(m) is None:
            return False
    return True


INFER = have("onnxruntime", "numpy", "PIL")


# ---- a minimal ONNX writer (protobuf wire format, only the fields these graphs need) ----

def _varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def _key(field, wire):
    return _varint(field << 3 | wire)


def _ld(field, payload):
    if isinstance(payload, str):
        payload = payload.encode()
    return _key(field, 2) + _varint(len(payload)) + payload


def _vi(field, n):
    return _key(field, 0) + _varint(n)


FLOAT, UINT8 = 1, 2


def _value_info(name, elem, dims):
    shape = b"".join(_ld(1, _vi(1, d)) for d in dims)            # TensorShapeProto.dim{dim_value}
    tensor = _vi(1, elem) + _ld(2, shape)                         # TypeProto.Tensor
    return _ld(1, name) + _ld(2, _ld(1, tensor))                  # ValueInfoProto{name, type}


def _node(op, inputs, outputs, attrs=b""):
    return b"".join(_ld(1, i) for i in inputs) + b"".join(_ld(2, o) for o in outputs) + _ld(4, op) + attrs


def _ints_attr(name, values):
    return _ld(5, _ld(1, name) + _vi(20, 7) + b"".join(_vi(8, v) for v in values))  # AttributeProto INTS


def _int_attr(name, value):
    return _ld(5, _ld(1, name) + _vi(20, 2) + _vi(3, value))  # AttributeProto INT


def onnx_bytes(nodes, inputs, outputs, opset=13):
    graph = b"".join(_ld(1, n) for n in nodes) + _ld(2, "g")
    graph += b"".join(_ld(11, v) for v in inputs) + b"".join(_ld(12, v) for v in outputs)
    return _vi(1, 7) + _ld(8, _ld(1, "") + _vi(2, opset)) + _ld(7, graph)  # ir_version 7, opset, graph


def matte_model(side):
    """A 'subject' model: logits = 4 * mean over the three normalised channels."""
    nodes = [_node("ReduceMean", ["input"], ["m"], _ints_attr("axes", [1]) + _int_attr("keepdims", 1)),
             _node("Add", ["m", "m"], ["m2"]), _node("Add", ["m2", "m2"], ["logits"])]
    return onnx_bytes(nodes, [_value_info("input", FLOAT, [1, 3, side, side])],
                      [_value_info("logits", FLOAT, [1, 1, side, side])])


def fill_model(h, w):
    """A 'fill' model with MI-GAN's I/O names: result = min(image, mask), so holes come back black."""
    nodes = [_node("Min", ["image", "mask"], ["result"])]
    return onnx_bytes(nodes, [_value_info("image", UINT8, [1, 3, h, w]), _value_info("mask", UINT8, [1, 1, h, w])],
                      [_value_info("result", UINT8, [1, 3, h, w])])


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ila.main(argv)
    return code, out.getvalue(), err.getvalue()


class ModelFactsTests(unittest.TestCase):
    def test_three_models_with_licences_and_pins(self):
        code, out, _ = run(["models", "--json"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertFalse(data["downloads"])
        by = {m["id"]: m for m in data["models"]}
        self.assertEqual(set(by), {"subject", "select", "fill"})
        self.assertEqual(by["subject"]["license"], "MIT")
        self.assertEqual(by["select"]["license"], "Apache-2.0")
        self.assertTrue(by["fill"]["license"].startswith("MIT"))
        self.assertEqual(by["subject"]["files"][0]["sha256"],
                         "d39b897ceb16ae654c1731f3dba0cf9b368d9cae74b5a57459b455cc8bfec402")
        self.assertEqual(by["fill"]["files"][0]["size"], 28079181)
        self.assertEqual(len(by["select"]["files"]), 4)
        for m in data["models"]:
            for f in m["files"]:
                self.assertRegex(f["sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(f["url"].startswith("https://huggingface.co/"))
                self.assertRegex(f["url"], r"/resolve/[0-9a-f]{40}/")  # pinned to a commit

    def test_text_listing(self):
        code, out, _ = run(["models"])
        self.assertEqual(code, 0)
        self.assertIn("BiRefNet", out)
        self.assertIn("Nothing is downloaded", out)


class VerifyModelTests(unittest.TestCase):
    def test_sha_match_and_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "m.onnx"
            f.write_bytes(b"not really a model")
            good = hashlib.sha256(b"not really a model").hexdigest()
            code, out, _ = run(["verify-model", str(f), "--sha256", good])
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(out)["match"])
            code, out, _ = run(["verify-model", str(f), "--sha256", "0" * 64])
            self.assertEqual(code, 1)
            self.assertFalse(json.loads(out)["match"])

    def test_known_pin_by_file_name(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "migan_pipeline_v2.onnx"
            f.write_bytes(b"fake")
            code, out, _ = run(["verify-model", str(f)])
            self.assertEqual(code, 1)  # a fake file never matches the real pin
            r = json.loads(out)
            self.assertEqual(r["known_pin"], "fill")
            self.assertEqual(r["expected"], "6f1f3530a1a2324b19752018ce756088b07973cda8d7d890034ace5c8a48c40b")

    def test_missing_file_exits_2(self):
        code, _, err = run(["verify-model", "/nonexistent/x.onnx", "--sha256", "0" * 64])
        self.assertEqual(code, 2)


class MissingModelTests(unittest.TestCase):
    def test_missing_model_prints_url_and_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            code, _, err = run(["remove-bg", "--model", str(Path(d) / "absent.onnx"), "in.png", "out.png"])
            self.assertEqual(code, 2)
            if INFER:
                self.assertIn("never downloads", err)
                self.assertIn("BiRefNet_lite-ONNX/resolve/de15b22", err)


@unittest.skipUnless(INFER, "onnxruntime, numpy and Pillow are needed for inference")
class InferenceTests(unittest.TestCase):
    def test_remove_bg_end_to_end(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            model = d / "matte.onnx"
            model.write_bytes(matte_model(32))
            src = Image.new("RGB", (64, 48), (0, 0, 0))
            for x in range(20, 44):
                for y in range(12, 36):
                    src.putpixel((x, y), (255, 255, 255))
            src.save(d / "in.png")
            code, out, err = run(["remove-bg", "--model", str(model), str(d / "in.png"), str(d / "out.png"),
                                  "--mask-out", str(d / "matte.png")])
            self.assertEqual(code, 0, err)
            r = json.loads(out)
            self.assertEqual(r["model_input"], 32)
            self.assertFalse(r["network"])
            res = Image.open(d / "out.png")
            self.assertEqual(res.mode, "RGBA")
            self.assertEqual(res.size, (64, 48))
            self.assertGreater(res.getpixel((32, 24))[3], 230)   # subject kept
            self.assertLess(res.getpixel((2, 2))[3], 20)         # background removed
            self.assertTrue((d / "matte.png").is_file())

    def test_inpaint_replaces_only_the_hole(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            model = d / "fill.onnx"
            model.write_bytes(fill_model(40, 40))
            Image.new("RGB", (40, 40), (200, 120, 60)).save(d / "in.png")
            mask = Image.new("L", (40, 40), 0)
            for x in range(15, 25):
                for y in range(15, 25):
                    mask.putpixel((x, y), 255)
            mask.save(d / "mask.png")
            code, out, err = run(["inpaint", "--model", str(model), "--mask", str(d / "mask.png"),
                                  str(d / "in.png"), str(d / "out.png")])
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)["hole_pixels"], 100)
            res = Image.open(d / "out.png")
            self.assertEqual(res.getpixel((20, 20)), (0, 0, 0))        # filled by the model
            self.assertEqual(res.getpixel((13, 13)), (200, 120, 60))   # grown margin not pasted back
            self.assertEqual(res.getpixel((0, 0)), (200, 120, 60))

    def test_corrupt_model_exits_2_with_plain_message(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            model = d / "broken.onnx"
            model.write_bytes(b"not an onnx file")
            Image.new("RGB", (8, 8)).save(d / "in.png")
            code, out, err = run(["remove-bg", "--model", str(model), str(d / "in.png"), str(d / "out.png")])
            self.assertEqual(code, 2)
            self.assertIn("cannot load", err)
            self.assertNotIn("Traceback", err)
            self.assertFalse((d / "out.png").exists())

    def test_onnx_helper_graph_when_available(self):
        if not have("onnx"):
            self.skipTest("onnx not installed; the hand-encoded graph covers inference")
        import onnx
        onnx.checker.check_model(onnx.load_from_string(matte_model(16)))
        onnx.checker.check_model(onnx.load_from_string(fill_model(8, 8)))


if __name__ == "__main__":
    unittest.main()
