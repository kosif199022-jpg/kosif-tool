"""blender_cinema.py: preset table, Kelvin colours and CLI shape always; real Cycles renders of every cinematic preset,
an animated camera move and the live inventory when Blender (or the bpy module) is on this machine. Proof behind
APPX-114…APPX-117. Set KOSIF_BLENDER_FULL=1 to render every preset (about 2 minutes on a laptop CPU)."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zlib

PATH = Path(__file__).resolve().parents[1] / "scripts" / "blender_cinema.py"
spec = importlib.util.spec_from_file_location("blender_cinema", PATH)
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)
HAVE = bool(bc.find_blender() or bc.bpy_python())


def cli(*args):
    p = subprocess.run([sys.executable, str(PATH), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("{")]
    return p.returncode, (json.loads(line[-1]) if line else {"stdout": p.stdout, "stderr": p.stderr})


class Offline(unittest.TestCase):
    def test_presets_complete(self):
        self.assertEqual(set(bc.PRESETS), {"product-hero", "golden-hour", "noir-volumetric", "neon-night", "anamorphic-epic"})
        for name, p in bc.PRESETS.items():
            for key in ("lens", "fstop", "blades", "ratio", "look", "set", "material", "lights", "cam", "finish", "ar"):
                self.assertIn(key, p, f"{name}.{key}")
            self.assertTrue(p["look"].startswith("AgX"))

    def test_kelvin(self):
        warm, cool = bc.kelvin_rgb(3200), bc.kelvin_rgb(9000)
        self.assertGreater(warm[0], warm[2])
        self.assertGreater(cool[2], cool[0] * 0.9)

    def test_presets_cli(self):
        p = subprocess.run([sys.executable, str(PATH), "presets"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(p.returncode, 0)
        self.assertIn("anamorphic-epic", p.stdout)


def encode_png(width, rows, chans, filters):
    """Minimal PNG writer for fixtures: 8-bit gray/RGB/RGBA rows, each row filtered with filters[y % len]."""
    out, prev = bytearray(), bytes(width * chans)
    for y, row in enumerate(rows):
        kind = filters[y % len(filters)]
        out.append(kind)
        for x, value in enumerate(row):
            a = row[x - chans] if x >= chans else 0
            b, c = prev[x], (prev[x - chans] if x >= chans else 0)
            pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
            paeth = a if pa <= pb and pa <= pc else b if pb <= pc else c
            out.append((value - (0, a, b, (a + b) // 2, paeth)[kind]) & 255)
        prev = row

    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
    head = struct.pack(">IIBBBBB", width, len(rows), 8, {1: 0, 3: 2, 4: 6}[chans], 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head) + chunk(b"IDAT", zlib.compress(bytes(out))) + chunk(b"IEND", b"")


def gradient_rows(width, height, chans):
    return [bytes((x * 7 + y * 13 + k * 50) % 256 if k < 3 else 255 for x in range(width) for k in range(chans))
            for y in range(height)]


FAKE_BLENDER = """
import json, shutil, sys
mode = sys.argv[1]
job = json.load(open(sys.argv[sys.argv.index("--job") + 1], encoding="utf-8"))
if mode == "error":
    rec = {"error": "ValueError: boom inside Blender", "trace": "Traceback (most recent call last):\\nValueError: boom"}
else:
    shutil.copy(mode, job["still"])
    rec = {"preset": job["preset"], "engine": "CYCLES", "warnings": []}
json.dump(rec, open(job["receipt"], "w", encoding="utf-8"))
sys.exit(1 if mode == "error" else 0)
"""


class StdlibPng(unittest.TestCase):
    def test_every_filter_matches_exact_stats(self):
        for chans in (1, 3, 4):
            with self.subTest(chans=chans):
                rows = gradient_rows(23, 11, chans)
                got = bc.png_stats_stdlib(encode_png(23, rows, chans, [0, 1, 2, 3, 4]))
                planes = [[row[x * chans + (0 if chans == 1 else k)] for row in rows for x in range(23)] for k in range(3)]
                mean = [sum(p) / len(p) for p in planes]
                std = [(sum(v * v for v in p) / len(p) - m * m) ** 0.5 for p, m in zip(planes, mean)]
                self.assertEqual(got["size"], [23, 11])
                self.assertEqual(got["mean"], [round(m, 1) for m in mean])
                self.assertEqual(got["std"], [round(v, 1) for v in std])

    def test_blank_and_not_png(self):
        flat = bc.png_stats_stdlib(encode_png(8, [bytes([40, 40, 40] * 8)] * 6, 3, [4, 3]))
        self.assertEqual(flat["std"], [0.0, 0.0, 0.0])
        self.assertNotIn("std", bc.png_stats_stdlib(b"not a png"))
        whole = encode_png(8, gradient_rows(8, 6, 3), 3, [1, 4])
        for broken in (whole[:60], whole[:33] + b"\x00\x00\x00\x05IDATxxxxx"):
            got = bc.png_stats_stdlib(broken)
            self.assertNotIn("std", got)
            self.assertIn("unsupported", got)

    def test_measure_png_without_pillow(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "g.png"
            path.write_bytes(encode_png(16, gradient_rows(16, 9, 4), 4, [1, 4, 2, 3]))
            with mock.patch.dict(sys.modules, {"PIL": None}):
                got = bc.measure_png(path)
            self.assertEqual(got["decoder"], "stdlib")
            self.assertGreater(max(got["std"]), 2)


class CliWithoutRealBlender(unittest.TestCase):
    """CLI failure paths and receipt handling; a stand-in runner replaces Blender, so nothing is rendered here."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.scratch = self.base / "tmp"
        self.scratch.mkdir()
        self.fake = self.base / "fake_blender.py"
        self.fake.write_text(FAKE_BLENDER, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, mode=None, missing=False):
        buf = io.StringIO()
        patches = [mock.patch.object(bc.tempfile, "tempdir", str(self.scratch))]
        if missing:
            patches += [mock.patch.object(bc, "find_blender", return_value=None),
                        mock.patch.object(bc, "bpy_python", return_value=None)]
        else:
            patches.append(mock.patch.object(bc, "blender_runner",
                                             return_value=([sys.executable, str(self.fake), mode], "fake", None)))
        with contextlib.ExitStack() as stack, contextlib.redirect_stdout(buf):
            for patch in patches:
                stack.enter_context(patch)
            code = bc.cli(list(args))
        lines = [ln for ln in buf.getvalue().splitlines() if ln.startswith("{")]
        return code, json.loads(lines[-1])

    def test_malformed_res_is_a_usage_error_and_creates_nothing(self):
        for res in ("640", "axb", "0x480", "1x2x3"):
            with self.subTest(res=res), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as stop:
                    bc.cli(["render", "--res", res, "-o", str(self.base / "out" / "x.png")])
                self.assertEqual(stop.exception.code, 2)
        self.assertFalse((self.base / "out").exists())

    def test_missing_blender_is_json_error_without_folders(self):
        code, rec = self.run_cli("render", "--frames", "4", "-o", str(self.base / "out" / "t.mp4"), missing=True)
        self.assertEqual((code, rec["status"]), (1, "error"))
        self.assertIn("Blender not found", rec["error"])
        code, rec = self.run_cli("inventory", "-o", str(self.base / "inv.json"), missing=True)
        self.assertEqual((code, rec["op"], rec["status"]), (1, "inventory", "error"))
        self.assertFalse((self.base / "out").exists())
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_error_inside_blender_is_reported_and_temp_removed(self):
        for args in (["render", "-o", str(self.base / "s.png")],
                     ["render", "--frames", "3", "-o", str(self.base / "a.mp4")],
                     ["inventory", "-o", str(self.base / "inv.json")]):
            with self.subTest(args=args[:3]):
                code, rec = self.run_cli(*args, mode="error")
                self.assertEqual((code, rec["status"]), (1, "error"))
                self.assertIn("boom inside Blender", rec["error"])
                self.assertIn("Traceback", rec["trace"])
                self.assertEqual(list(self.scratch.iterdir()), [])

    def test_still_verified_without_pillow(self):
        png = self.base / "rendered.png"
        png.write_bytes(encode_png(32, gradient_rows(32, 18, 4), 4, [0, 1, 2, 3, 4]))
        with mock.patch.dict(sys.modules, {"PIL": None}):
            code, rec = self.run_cli("render", "-o", str(self.base / "shot.png"), mode=str(png))
        self.assertEqual(code, 0, rec)
        self.assertTrue(rec["verified"])
        self.assertEqual(rec["metrics"]["image"]["decoder"], "stdlib")
        self.assertEqual(list(self.scratch.iterdir()), [])


@unittest.skipUnless(HAVE, "Blender not found (KOSIF_BLENDER / PATH / pip install bpy)")
class WithBlender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.d = Path(cls.tmp.name) / "رندر"
        cls.d.mkdir()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_doctor(self):
        code, r = cli("doctor")
        self.assertEqual(code, 0)
        self.assertTrue(r["ready"])

    def test_inventory(self):
        out = self.d / "inventory.json"
        code, r = cli("inventory", "-o", str(out))
        self.assertTrue(r["verified"], r)
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertGreater(data["operators_total"], 1000)
        self.assertIn("CompositorNodeGlare", data["compositor_nodes"])
        self.assertIn("MULTIPLE_SCATTERING", data["sky_types"])

    def test_render_presets(self):
        presets = sorted(bc.PRESETS) if os.environ.get("KOSIF_BLENDER_FULL") else ["neon-night", "golden-hour"]
        for preset in presets:
            with self.subTest(preset=preset):
                code, r = cli("render", "--preset", preset, "--res", "320x180", "--quality", "preview", "--samples", "8",
                              "-o", str(self.d / f"{preset}.png"))
                self.assertTrue(r.get("verified"), r)
                m = r["metrics"]
                self.assertEqual(m["engine"], "CYCLES")
                self.assertEqual(m["view_transform"], "AgX")
                self.assertEqual(m["warnings"], [])
                self.assertGreater(max(m["image"]["mean"]), 10, preset)    # not a black frame

    def test_animated_orbit(self):
        out = self.d / "orbit.mp4"
        code, r = cli("render", "--preset", "product-hero", "--res", "160x90", "--quality", "preview", "--samples", "4",
                      "--frames", "6", "--move", "orbit", "--save-blend", str(self.d / "orbit.blend"), "-o", str(out))
        self.assertTrue(r.get("verified"), r)
        self.assertEqual(r["metrics"]["frames"], 6)
        self.assertTrue((self.d / "orbit.blend").exists())


if __name__ == "__main__":
    unittest.main()
