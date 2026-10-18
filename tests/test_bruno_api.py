"""Bruno API proof (proofs/bruno-api): the owned collection is well-formed and the recorded run passed."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROOF = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "bruno-api"


class BrunoApiTest(unittest.TestCase):
    def test_collection_is_well_formed(self):
        col = PROOF / "collection"
        self.assertTrue((col / "bruno.json").is_file())
        brus = list(col.glob("*.bru"))
        self.assertGreaterEqual(len(brus), 6)
        for b in brus:
            text = b.read_text(encoding="utf-8")
            self.assertIn("meta {", text)
            self.assertRegex(text, r"\b(get|post|put|delete|patch)\s*\{")
        self.assertTrue((col / "environments" / "local.bru").is_file())

    def test_server_is_stdlib_only(self):
        src = (PROOF / "server.py").read_text(encoding="utf-8")
        for banned in ("import flask", "import fastapi", "import django", "requests."):
            self.assertNotIn(banned, src)

    def test_recorded_run_passed(self):
        res = json.loads((PROOF / "results.json").read_text(encoding="utf-8"))
        s = res["full_run"]["summary"]
        self.assertEqual(s["failedRequests"], 0)
        self.assertEqual(s["passedAssertions"], s["totalAssertions"])
        self.assertEqual(s["passedTests"], s["totalTests"])
        self.assertEqual(res["failure_gate"]["exit_code"], 1)
        self.assertEqual(res["csv_run"]["iterations"], 3)
        self.assertEqual(res["openapi_import"]["bru_files"], 10)

    def test_secret_not_committed(self):
        env = (PROOF / "collection" / "environments" / "local.bru").read_text(encoding="utf-8")
        self.assertIn("vars:secret", env)
        self.assertNotIn("demo", env.split("vars:secret")[0])


if __name__ == "__main__":
    unittest.main()
