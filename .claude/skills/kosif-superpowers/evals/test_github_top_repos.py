"""GitHub top-1000 review tracker (scripts/github_top_repos.py, data/github_top1000*.json, references/github-top-1000.md)."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SK / "scripts"))
import github_top_repos as G  # noqa: E402

CLI = [sys.executable, str(SK / "scripts" / "github_top_repos.py")]


class GithubTopReposTest(unittest.TestCase):
    def test_self_test(self):
        p = subprocess.run(CLI + ["--self-test"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_tracker_and_table_are_up_to_date(self):
        p = subprocess.run(CLI + ["build", "--check"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_snapshot_has_1000_unique_ranked_rows(self):
        rows = json.loads(G.SNAPSHOT.read_text(encoding="utf-8"))["rows"]
        self.assertEqual(len(rows), 1000)
        self.assertEqual([r["rank"] for r in rows], list(range(1, 1001)))
        self.assertEqual(len({r["repo"].lower() for r in rows}), 1000)
        stars = [r["stars"] for r in rows]
        self.assertEqual(stars, sorted(stars, reverse=True))

    def test_every_row_has_a_decision_and_transfers_point_at_real_records(self):
        ids = set()
        for f in (SK / "data" / "powers").glob("*.json"):
            ids |= {r["id"] for r in json.loads(f.read_text(encoding="utf-8"))}
        tools = {t["id"] for t in json.loads((SK / "data" / "tools.json").read_text(encoding="utf-8"))["tools"]}
        tracker = json.loads(G.TRACKER.read_text(encoding="utf-8"))
        for r in tracker["rows"] + tracker.get("extra", []):
            self.assertIn(r["decision"], G.DECISIONS, r["repo"])
            for t in r["transferred"]:
                self.assertTrue(t in ids or t in tools, f"{r['repo']} → {t} is not a power or tool id")
            if r["transferred"]:
                self.assertEqual(r["decision"], "transferred", r["repo"])

    def test_copyleft_is_never_marked_mine(self):
        for r in json.loads(G.TRACKER.read_text(encoding="utf-8"))["rows"]:
            if r["license_class"] == "copyleft":
                self.assertNotEqual(r["decision"], "mine", r["repo"])


if __name__ == "__main__":
    unittest.main()
