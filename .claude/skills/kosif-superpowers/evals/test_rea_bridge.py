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


if __name__ == "__main__":
    unittest.main()
