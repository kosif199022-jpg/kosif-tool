"""Functional checks for the standalone KOSIF Superpowers MCP runtime."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).with_name("kosif_remote_superpowers.py")
spec = importlib.util.spec_from_file_location("kosif_remote_superpowers", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = patch.dict(os.environ, {
            "KOSIF_REMOTE_ROOT": self.temp.name,
            "KOSIF_ALLOW_WRITES": "0",
            "KOSIF_ALLOW_EXEC": "0",
        })
        self.env.start()
        self.addCleanup(self.env.stop)
        (Path(self.temp.name) / "sample.txt").write_text("first\nsecond\n", encoding="utf-8")

    def test_read_search_list(self):
        self.assertEqual(mod.execute("read_file", {"path": "sample.txt", "offset": 1})["lines"], ["second"])
        self.assertEqual(len(mod.execute("search_text", {"query": "second"})["hits"]), 1)
        self.assertEqual(len(mod.execute("list_directory")["items"]), 1)

    def test_denied_outside_workspace(self):
        with self.assertRaises(PermissionError):
            mod.execute("file_info", {"path": ".."})

    def test_denied_write_and_commands_by_default(self):
        with self.assertRaises(PermissionError):
            mod.execute("write_file", {"path": "a", "content": "x"})
        with self.assertRaises(PermissionError):
            mod.execute("run_command", {"argv": ["python", "--version"]})

    def test_allowlisted_write_and_replace(self):
        os.environ["KOSIF_ALLOW_WRITES"] = "1"
        mod.execute("write_file", {"path": "new.txt", "content": "apple"})
        mod.execute("replace_block", {"path": "new.txt", "old_string": "apple", "new_string": "pear"})
        self.assertEqual((Path(self.temp.name) / "new.txt").read_text(), "pear")
        mod.execute("move_file", {"source": "new.txt", "destination": "next.txt"})
        self.assertTrue((Path(self.temp.name) / "next.txt").exists())

    def test_disallow_arbitrary_command(self):
        os.environ["KOSIF_ALLOW_EXEC"] = "1"
        with self.assertRaises(PermissionError):
            mod.execute("run_command", {"argv": ["python", "-c", "print(1)"]})

    def test_stdio_transport(self):
        reqs = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "health", "arguments": {}}},
        ]
        r = subprocess.run(
            [sys.executable, str(SOURCE), "serve"],
            input="\n".join(json.dumps(q) for q in reqs) + "\n",
            capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        results = [json.loads(line) for line in r.stdout.splitlines()]
        self.assertEqual(len(results[1]["result"]["tools"]), 11)
        self.assertEqual(results[2]["result"]["content"][0]["type"], "text")

    def test_demo(self):
        r = subprocess.run([sys.executable, str(SOURCE), "demo"], capture_output=True, text=True, timeout=5)
        self.assertEqual(r.returncode, 0, r.stderr)
        obj = json.loads(r.stdout)
        self.assertEqual(obj["status"], "PASS")
        self.assertTrue(obj["default_write_denied"])


if __name__ == "__main__":
    unittest.main()
