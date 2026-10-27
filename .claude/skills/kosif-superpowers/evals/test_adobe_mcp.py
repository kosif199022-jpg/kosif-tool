"""Tests for scripts/adobe_mcp.py (vetted Adobe MCP bridges: steps, config, doctor)."""
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import adobe_mcp  # noqa: E402


def run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = adobe_mcp.main(list(argv))
    return rc, buf.getvalue()


class AdobeMcpTest(unittest.TestCase):
    def test_every_app_has_a_recommended_bridge(self):
        apps = {b["app"] for b in adobe_mcp.BRIDGES.values() if b["status"] == "recommended"}
        self.assertEqual(apps, {"Adobe After Effects", "Adobe Premiere Pro", "Adobe Photoshop"})
        for b in adobe_mcp.BRIDGES.values():
            self.assertTrue(b["repo"].startswith("https://github.com/"))
            self.assertEqual(b["license"], "MIT")
            self.assertGreaterEqual(len(b["steps"]), 3)

    def test_list_json(self):
        rc, out = run("list", "--json")
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertEqual(set(data["bridges"]), {"after-effects", "premiere", "photoshop", "adb-mcp"})
        self.assertTrue(data["rejected"])

    def test_desktop_config_is_valid_json(self):
        for bid in ("after-effects", "premiere", "photoshop"):
            for os_key in ("win", "mac"):
                rc, out = run("config", bid, "--os", os_key)
                self.assertEqual(rc, 0)
                body = "\n".join(l for l in out.splitlines() if not l.startswith("//"))
                cfg = json.loads(body)
                self.assertEqual(len(cfg["mcpServers"]), 1)

    def test_after_effects_path(self):
        cfg = adobe_mcp.desktop_config("after-effects", "win", "D:\\tools\\after-effects-mcp")
        self.assertEqual(cfg["mcpServers"]["AfterEffectsMCP"]["args"], ["D:\\tools\\after-effects-mcp\\build\\index.js"])
        cmd = adobe_mcp.claude_code_command("after-effects", "mac", "/Users/me/ae/")
        self.assertEqual(cmd, "claude mcp add AfterEffectsMCP -- node /Users/me/ae/build/index.js")

    def test_claude_code_commands(self):
        self.assertEqual(adobe_mcp.claude_code_command("premiere", "mac"), "claude mcp add premiere-pro -- premiere-pro-mcp")
        self.assertEqual(adobe_mcp.claude_code_command("photoshop", "mac"), "claude mcp add photoshop -- npx -y @alisaitteke/photoshop-mcp")
        self.assertIn("cmd /c npx", adobe_mcp.claude_code_command("photoshop", "win"))

    def test_no_secrets_in_output(self):
        for bid in adobe_mcp.BRIDGES:
            _, out = run("show", bid, "--json")
            self.assertNotRegex(out.lower(), r"api[_-]?key\s*[:=]")
            self.assertNotIn("env", json.loads(out).get("needs", {}))

    def test_doctor_shape(self):
        r = adobe_mcp.doctor()
        self.assertIn("found", r)
        self.assertEqual(set(r["bridges"]), set(adobe_mcp.BRIDGES))

    def test_unknown_id(self):
        with self.assertRaises(SystemExit):
            run("show", "illustrator-x")


if __name__ == "__main__":
    unittest.main()
