"""Tests for scripts/photocraft_mcp.py (PhotoCraft MCP helper, annex A39)."""
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import photocraft_mcp  # noqa: E402


def run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = photocraft_mcp.main(list(argv))
    return rc, buf.getvalue()


class PhotoCraftMcpTest(unittest.TestCase):
    def test_steps_ask_first(self):
        for mode in ("headless", "bridge", "release"):
            rc, out = run("steps", mode)
            self.assertEqual(rc, 0)
            self.assertTrue(out.startswith("1. "))
        self.assertIn("Ask the user first", run("steps", "headless")[1])

    def test_config_claude_code_headless(self):
        rc, out = run("config", "--client", "claude-code", "--read-root", "/w/in", "--write-root", "/w/out")
        self.assertEqual(rc, 0)
        self.assertEqual(out.strip(), "claude mcp add photocraft -- photocraft-cli mcp "
                         "--automation-read-root /w/in --automation-write-root /w/out")

    def test_config_json_bridge_uses_token_file(self):
        rc, out = run("config", "--client", "json", "--bridge", "127.0.0.1:7878", "--token-file", "/p/t")
        cfg = json.loads(out)["mcpServers"]["photocraft-live"]
        self.assertEqual(cfg["args"], ["mcp", "--bridge", "127.0.0.1:7878", "--control-token-file", "/p/t"])

    def test_relative_root_and_tokenless_bridge_refused(self):
        with self.assertRaises(SystemExit):
            run("config", "--read-root", "relative/dir")
        with self.assertRaises(SystemExit):
            run("config", "--bridge", "127.0.0.1:7878")

    def test_actions_are_valid_batch_steps(self):
        for name in photocraft_mcp.ACTIONS:
            steps = json.loads(run("actions", name)[1])
            self.assertTrue(all("command" in s and "params" in s for s in steps))

    def test_doctor_and_recipes_run(self):
        self.assertEqual(run("doctor")[0], 0)
        self.assertEqual(len(run("recipes")[1].strip().splitlines()), 6)


if __name__ == "__main__":
    unittest.main()
