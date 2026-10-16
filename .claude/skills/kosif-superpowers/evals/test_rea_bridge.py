"""Unit tests for the read-only/opt-in REA bridge. REA itself is not required."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "scripts" / "rea_bridge.py"
spec = importlib.util.spec_from_file_location("rea_bridge", PATH)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class ReaBridgeTests(unittest.TestCase):
    def test_node_version_matrix(self):
        for v, valid in [("v22.16.0", False), ("v22.19.0", True),
                         ("v24.10.0", False), ("v24.11.0", True),
                         ("v25.1.0", False), ("v26.0.0", True),
                         ("unknown", False)]:
            with self.subTest(v=v):
                self.assertEqual(bridge.node_ready(v), valid)

    def test_static_plan_is_not_execution(self):
        with tempfile.TemporaryDirectory() as root:
            sample = Path(root) / "app.js"
            sample.write_text("const hello = 1;", encoding="utf8")
            plan = bridge.inspect_plan("javascript", str(sample))
            self.assertEqual(plan["status"], "plan_only")
            self.assertEqual(plan["command"][1], "analyze-javascript-application")
            self.assertFalse(plan["analysis_executed"])
            self.assertFalse(plan["verified"])

    def test_documented_only_never_returns_executable(self):
        for kind in bridge.DOCUMENTED_ONLY:
            with self.subTest(kind=kind):
                plan = bridge.inspect_plan(kind, "ignored")
                self.assertNotIn("command", plan)
                self.assertFalse(plan["verified"])

    def test_missing_target_cannot_be_planned(self):
        with tempfile.TemporaryDirectory() as root:
            plan = bridge.inspect_plan("sqlite", str(Path(root) / "missing.sqlite"))
            self.assertEqual(plan["status"], "target_missing")

    def test_run_requires_authorization(self):
        with tempfile.TemporaryDirectory() as root:
            sample = Path(root) / "file.dll"
            sample.write_bytes(b"not a real assembly")
            result = bridge.run_static("dotnet", str(sample), str(Path(root) / "out.json"), False)
            self.assertEqual(result["status"], "authorization_required")
            self.assertFalse(result["analysis_executed"])

    def test_no_install_side_effect_and_no_secret_echo(self):
        import inspect
        body = inspect.getsource(bridge)
        self.assertNotIn("shell=True", body)
        self.assertNotIn("npm install", body)
        self.assertNotIn("npx ", body)


    def test_stubbed_local_cli_creates_unverified_receipt(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as root:
            sample = Path(root) / "demo.js"
            sample.write_text("const ok = true;", encoding="utf8")
            dst = Path(root) / "evidence.json"
            stub = SimpleNamespace(returncode=0, stdout=b'{"ok":true}', stderr=b'')
            with patch.object(bridge, "environment", return_value={"rea_installed": True, "node_compatible": True}), \
                 patch.object(bridge.subprocess, "run", return_value=stub) as execute:
                result = bridge.run_static("javascript", str(sample), str(dst), True)
            self.assertEqual(result["status"], "executed_not_verified")
            self.assertFalse(result["verified"])
            self.assertTrue(dst.is_file())
            self.assertEqual(dst.read_bytes(), stub.stdout)
            execute.assert_called_once()

    def test_existing_output_is_preserved(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as root:
            sample = Path(root) / "demo.js"
            sample.write_bytes(b"x")
            dst = Path(root) / "evidence.json"
            dst.write_bytes(b"original")
            with patch.object(bridge, "environment", return_value={"rea_installed": True, "node_compatible": True}), \
                 patch.object(bridge.subprocess, "run") as execute:
                result = bridge.run_static("javascript", str(sample), str(dst), True)
            self.assertEqual(result["status"], "unsafe_or_existing_output")
            self.assertEqual(dst.read_bytes(), b"original")
            execute.assert_not_called()

    def test_invalid_json_cannot_produce_success_receipt(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as root:
            sample = Path(root) / "demo.js"
            sample.write_bytes(b"x")
            dst = Path(root) / "evidence.json"
            with patch.object(bridge, "environment", return_value={"rea_installed": True, "node_compatible": True}), \
                 patch.object(bridge.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout=b"not-json", stderr=b"")):
                result = bridge.run_static("javascript", str(sample), str(dst), True)
            self.assertEqual(result["status"], "non_json_response")
            self.assertFalse(dst.exists())

    def test_unknown_kind_fails_closed(self):
        result = bridge.run_static("execute-binary", "something", "evidence.json", True)
        self.assertEqual(result["status"], "unsupported_kind")
        self.assertFalse(result["verified"])

if __name__ == "__main__":
    unittest.main()
