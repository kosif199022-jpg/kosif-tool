"""Tests for scripts/craft_anything.py, the opt-in Craft Anything bridge.

The stub CLI answers like craft-anything-cli 0.4.0 does, so these run without the Rust build.
When the real binary is present (CRAFT_ANYTHING_CLI or PATH) one more test drives it.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "craft_anything.py"
spec = importlib.util.spec_from_file_location("craft_anything", PATH)
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)


class StubCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        stub = self.root / ca.BIN_NAME
        stub.write_text(f"#!{sys.executable}\n" + ca.STUB.split("\n", 1)[1], encoding="utf-8")
        stub.chmod(0o755)
        self.old = os.environ.get("CRAFT_ANYTHING_CLI")
        os.environ["CRAFT_ANYTHING_CLI"] = str(stub)

    def tearDown(self):
        if self.old is None:
            os.environ.pop("CRAFT_ANYTHING_CLI", None)
        else:
            os.environ["CRAFT_ANYTHING_CLI"] = self.old
        self.tmp.cleanup()

    def test_doctor_summary(self):
        d = ca.doctor()
        self.assertTrue(d["installed"])
        self.assertEqual(d["engines_ok"], ["gdb"])
        self.assertEqual(d["status_counts"], {"info": 1, "ok": 3})
        self.assertEqual(d["problems"], [])

    def test_tools_filter(self):
        t = ca.list_tools("", toolset="core")
        self.assertEqual(t["matched"], 2)
        self.assertEqual({r["command"] for r in t["tools"]}, {"core-target-open", "core-target-triage"})

    def test_agent_and_setup_commands_are_refused(self):
        for tool in ("rebuild", "chat", "setup", "mcp", "settings-set"):
            with self.subTest(tool=tool):
                r = ca.run_tool(tool, [], str(self.root / f"{tool}.json"), authorized=True)
                self.assertEqual(r["status"], "refused")
                self.assertFalse(r["executed"])
                self.assertFalse((self.root / f"{tool}.json").exists())

    def test_deep_needs_authorization(self):
        r = ca.run_tool("triage", ["x"], str(self.root / "a.json"), deep=True)
        self.assertEqual(r["status"], "authorization_required")
        self.assertFalse((self.root / "a.json").exists())

    def test_deep_run_writes_hashed_output_once(self):
        out = self.root / "deep.json"
        r = ca.run_tool("triage", ["x"], str(out), deep=True, authorized=True)
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["sha256"], ca.sha256_bytes(out.read_bytes()))
        self.assertFalse(r["verified"])
        again = ca.run_tool("triage", ["x"], str(out), deep=True, authorized=True)
        self.assertEqual(again["status"], "output_exists")

    def test_clean_room_refusal_is_a_tool_error(self):
        r = ca.run_tool("triage", ["x"], str(self.root / "c.json"))
        self.assertEqual(r["status"], "tool_error")
        self.assertIn("feature_missing", json.dumps(r["error"]))

    def test_never_passes_allow_run(self):
        argv = ca.plan("core-target-open", ["f"])["command"]
        self.assertNotIn("--allow-run", argv)
        self.assertIn("--clean-room", argv)

    def test_mcp_config_runs_nothing(self):
        cfg = ca.mcp_config()
        self.assertFalse(cfg["executed"])
        self.assertEqual(cfg["mcpServers"]["craft-anything"]["args"], ["mcp"])

    def test_self_test_cli(self):
        done = subprocess.run([sys.executable, "-B", str(PATH), "--self-test"], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn('"self_test": "pass"', done.stdout)


class MissingCase(unittest.TestCase):
    def test_missing_binary_gives_install_steps(self):
        old = os.environ.get("CRAFT_ANYTHING_CLI")
        os.environ["CRAFT_ANYTHING_CLI"] = "/nonexistent/craft-anything-cli"
        try:
            d = ca.doctor()
            self.assertFalse(d["installed"])
            self.assertTrue(any("cargo install" in s for s in d["install"]))
            r = ca.run_tool("triage", ["x"], "/nonexistent/out.json")
            self.assertEqual(r["status"], "not_installed")
        finally:
            if old is None:
                os.environ.pop("CRAFT_ANYTHING_CLI", None)
            else:
                os.environ["CRAFT_ANYTHING_CLI"] = old


@unittest.skipUnless(ca.find_binary(), "craft-anything-cli not installed here")
class RealBinaryCase(unittest.TestCase):
    def test_real_doctor_and_tools(self):
        d = ca.doctor()
        self.assertTrue(d["installed"] and d["doctor_ok"])
        t = ca.list_tools()
        self.assertGreater(t["total"], 200)


if __name__ == "__main__":
    unittest.main()
