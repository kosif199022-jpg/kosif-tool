"""Repo map (scripts/repo_map.py): static, ranked, budgeted map of a codebase."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SK / "scripts"))
import repo_map as R  # noqa: E402

CLI = [sys.executable, str(SK / "scripts" / "repo_map.py")]


class RepoMapTest(unittest.TestCase):
    def test_self_test(self):
        p = subprocess.run(CLI + ["--self-test"], capture_output=True, text=True, timeout=120)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_never_executes_the_target(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            marker = root / "PWNED"
            (root / "evil.py").write_text(f"open({str(marker)!r}, 'w').write('x')\ndef payload_runner():\n    pass\n", encoding="utf-8")
            res = R.build_map(root)
            self.assertFalse(marker.exists())
            self.assertIn("payload_runner", res["map"])

    def test_budget_and_json_cli(self):
        p = subprocess.run(CLI + ["map", str(SK / "scripts"), "--budget", "800", "--json"], capture_output=True, text=True, timeout=300)
        self.assertEqual(p.returncode, 0, p.stderr)
        res = json.loads(p.stdout)
        self.assertLessEqual(res["chars"], 800)
        self.assertGreater(res["files_scanned"], 50)

    def test_nested_helpers_are_not_listed(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "m.py").write_text("def outer_api():\n    def inner_helper():\n        pass\n    return inner_helper\n", encoding="utf-8")
            names = [x["name"] for x in R.scan(Path(d))["m.py"]["defs"]]
            self.assertEqual(names, ["outer_api"])


if __name__ == "__main__":
    unittest.main()
