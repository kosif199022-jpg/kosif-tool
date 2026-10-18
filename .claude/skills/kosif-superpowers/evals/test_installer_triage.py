"""Unit tests for installer_triage.py on synthetic PE/asar bytes. No real installer, 7-Zip or REA needed."""
import importlib.util
import inspect
import json
from pathlib import Path
import re
import struct
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "scripts" / "installer_triage.py"
spec = importlib.util.spec_from_file_location("installer_triage", PATH)
tri = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tri)

POWERS = Path(__file__).resolve().parents[1] / "scripts" / "powers.py"
pspec = importlib.util.spec_from_file_location("powers", POWERS)
powers = importlib.util.module_from_spec(pspec)
pspec.loader.exec_module(powers)


def fake_pe(sections=(".text",), overlay=b"", body=b"", cli=False):
    """Minimal PE32: DOS stub, PE header, optional header with 16 data dirs, N sections of 0x200 bytes."""
    e_lfanew = 0x40
    opt_size = 224
    head = bytearray(0x400)
    head[:2] = b"MZ"
    struct.pack_into("<I", head, 0x3C, e_lfanew)
    head[e_lfanew:e_lfanew + 4] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", head, e_lfanew + 4, 0x14C, len(sections), 0, 0, 0, opt_size, 0x102)
    opt = e_lfanew + 24
    struct.pack_into("<H", head, opt, 0x10B)
    if cli:
        struct.pack_into("<II", head, opt + 96 + 14 * 8, 0x2000, 0x48)
    sec = opt + opt_size
    raw = 0x400
    for i, name in enumerate(sections):
        o = sec + i * 40
        head[o:o + 8] = name.encode().ljust(8, b"\0")
        struct.pack_into("<IIII", head, o + 8, 0x200, 0x1000 * (i + 1), 0x200, raw + i * 0x200)
    data = bytes(head) + (body.ljust(0x200 * len(sections), b"\0"))
    return data + overlay


def fake_asar(files):
    """files: {path: bytes}. Builds a Chromium-pickle-style asar header the way electron/asar does."""
    tree, blobs, off = {"files": {}}, b"", 0
    for path, data in files.items():
        node = tree
        parts = path.split("/")
        for p in parts[:-1]:
            node = node["files"].setdefault(p, {"files": {}})
        node["files"][parts[-1]] = {"size": len(data), "offset": str(off)}
        blobs += data
        off += len(data)
    header = json.dumps(tree).encode()
    pad = (4 - len(header) % 4) % 4
    h = header + b"\0" * pad
    prefix = struct.pack("<IIII", 4, len(h) + 8, len(h) + 4, len(header))
    return prefix + h + blobs


class InstallerTriageTests(unittest.TestCase):
    def write(self, root, name, data):
        p = Path(root) / name
        p.write_bytes(data)
        return p

    def test_nsis_overlay_routes_to_unpack(self):
        with tempfile.TemporaryDirectory() as root:
            p = self.write(root, "setup.exe", fake_pe(overlay=b"\0\0\0\0" + tri.SIG["nsis"] + b"\0" * 64))
            r = tri.classify(p)
            self.assertIn(("installer", "nsis"), {(f["kind"], f["value"]) for f in r["findings"]})
            self.assertEqual(r["routes"][0]["step"], "unpack")
            self.assertFalse(r["verified"])
            self.assertFalse(r["analysis_executed"])

    def test_upx_is_flagged_and_pe_resources_not_proposed(self):
        with tempfile.TemporaryDirectory() as root:
            p = self.write(root, "stub.exe", fake_pe(sections=("UPX0", "UPX1", ".rsrc")))
            r = tri.classify(p)
            self.assertIn(("packer", "upx"), {(f["kind"], f["value"]) for f in r["findings"]})
            cmds = [" ".join(x["command"]) for x in r["routes"] if x["step"] == "rea"]
            self.assertFalse(any("inspect-pe-resources" in c for c in cmds))

    def test_electron_and_dotnet_are_detected(self):
        with tempfile.TemporaryDirectory() as root:
            p = self.write(root, "App.exe", fake_pe(body=b"xx" + tri.SIG["electron_fuse"] + b"\x01\x09", cli=True))
            kinds = {(f["kind"], f["value"]) for f in tri.classify(p)["findings"]}
            self.assertIn(("runtime", "electron"), kinds)
            self.assertIn(("runtime", "dotnet"), kinds)

    def test_unsigned_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            p = self.write(root, "a.exe", fake_pe())
            self.assertIn(("signature", "unsigned"), {(f["kind"], f["value"]) for f in tri.classify(p)["findings"]})

    def test_non_pe_is_not_misread(self):
        with tempfile.TemporaryDirectory() as root:
            p = self.write(root, "notes.zip", b"PK\x03\x04" + b"\0" * 40)
            r = tri.classify(p)
            self.assertEqual(r["format"], "zip")
            self.assertNotIn("pe", r)

    def test_version_strings_reject_binary_garbage(self):
        good = "ProductName".encode("utf-16-le") + b"\0\0" + "Canva".encode("utf-16-le") + b"\0\0"
        empty = "FileDescription".encode("utf-16-le") + b"\0\0" + b"0\x00\x08\x00\x01\x00" + "FileVersion".encode("utf-16-le") + b"\0\0"
        vi = tri.version_strings(good + empty)
        self.assertEqual(vi.get("ProductName"), "Canva")
        self.assertNotIn("FileDescription", vi)

    def test_unpack_gates_need_no_seven_zip(self):
        with tempfile.TemporaryDirectory() as root:
            p = self.write(root, "setup.exe", fake_pe())
            self.assertEqual(tri.unpack(p, Path(root) / "out", False)["status"], "authorization_required")
            existing = Path(root) / "exists"
            existing.mkdir()
            self.assertEqual(tri.unpack(p, existing, True)["status"], "unsafe_or_existing_output")
            self.assertEqual(tri.unpack(Path(root) / "missing.exe", Path(root) / "o2", True)["status"], "target_missing")

    def test_asar_listing_and_fingerprint(self):
        pkg = {"name": "Demo", "version": "1.0.0", "main": "dist/main.js",
               "build": {"fileAssociations": [{"ext": "mp4"}, {"ext": ["heic", "png"]}]}}
        main = b"const {desktopCapturer, autoUpdater, safeStorage} = require('electron'); app.setAsDefaultProtocolClient('demo');"
        pre = b"contextBridge.exposeInMainWorld('bridge', {requestMessagePort})"
        data = fake_asar({"package.json": json.dumps(pkg).encode(), "dist/main.js": main, "dist/preload.js": pre,
                          "dist/renderer/win_a/index.rtl.html": b"<html dir=rtl>", "dist/renderer/win_a/index.html": b"<html>"})
        with tempfile.TemporaryDirectory() as root:
            a = self.write(root, "app.asar", data)
            ls = tri.asar_list(a)
            self.assertEqual(ls["files"], 5)
            self.assertEqual(ls["package"]["main"], "dist/main.js")
            self.assertEqual(json.loads(tri.asar_list(a, "package.json")["text"])["name"], "Demo")
            fp = tri.fingerprint(a)
            feats = {f["feature"] for f in fp["features"]}
            for want in ("screen-capture", "auto-update", "secure-storage", "deep-link", "message-port", "context-bridge"):
                self.assertIn(want, feats)
            self.assertEqual(fp["file_associations"], ["heic", "mp4", "png"])
            self.assertTrue(fp["rtl_ui"])
            self.assertFalse(fp["verified"])

    def test_bad_asar_fails_closed(self):
        with tempfile.TemporaryDirectory() as root:
            a = self.write(root, "app.asar", b"\x04\0\0\0" + b"\xff" * 12)
            self.assertEqual(tri.asar_list(a)["status"], "invalid_asar")

    def test_route_maps_artifacts_to_rea(self):
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / "resources").mkdir()
            self.write(root, "resources/app.asar", fake_asar({"package.json": b'{"main":"main.js"}', "main.js": b"1"}))
            self.write(root, "data.zip", b"PK\x03\x04" + b"\0" * 30)
            plan = tri.route(root)["plan"]
            kinds = {p["kind"] for p in plan}
            self.assertEqual(kinds, {"electron-asar", "archive"})
            asar = next(p for p in plan if p["kind"] == "electron-asar")
            self.assertIn("--source-path", asar["commands"][1])

    def test_no_execution_network_or_shell(self):
        body = inspect.getsource(tri)
        self.assertNotIn("shell=True", body)
        for mod in ("urllib", "socket", "requests", "http.client"):
            self.assertIsNone(re.search(r"^\s*(import|from)\s+" + re.escape(mod), body, re.M), mod)
        # the only subprocess call is 7-Zip extraction
        self.assertEqual(body.count("subprocess.run("), 1)


class AppxRoutingTests(unittest.TestCase):
    def fams(self, prompt):
        words = re.findall(r"[\w:]+", prompt)
        return powers.intent_of(powers.expand(words, prompt))[0]

    def test_app_names_reach_appx(self):
        for q in ("ترجمة تلقائية زي كاب كات", "فقاعة كاميرا مثل كانفا", "auto reframe like premiere", "capcut speed curve"):
            with self.subTest(q=q):
                self.assertIn("APPX", self.fams(q))

    def test_installers_reach_rea(self):
        for q in ("حلل المثبت ده", "analyze this setup.exe installer", "unpack the app.asar of an electron app"):
            with self.subTest(q=q):
                self.assertIn("REA", self.fams(q))

    def test_translation_and_training_do_not_hit_rea(self):
        for q in ("ترجم هذا النص للإنجليزية", "اعمل لي برنامج تدريب رياضي", "remove the background from this photo"):
            with self.subTest(q=q):
                self.assertNotIn("REA", self.fams(q))


if __name__ == "__main__":
    unittest.main()
