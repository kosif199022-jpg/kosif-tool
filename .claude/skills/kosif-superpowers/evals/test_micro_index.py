#!/usr/bin/env python3
"""Regression tests for scripts/micro_index.py (the micro index: one line per power, tool and superpower)."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "micro_index.py"
sys.path.insert(0, str(SKILL / "scripts"))
import micro_index as M  # noqa: E402
import powers as P  # noqa: E402


def run(*args):
    r = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True, timeout=300)
    return r.returncode, r.stdout, r.stderr


class MicroIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.idx = M.build_index()

    def test_build_is_fresh(self):
        code, out, err = run("build", "--check")
        self.assertEqual(code, 0, out + err)

    def test_every_power_tool_and_superpower_once(self):
        ids = [r["id"] for r in self.idx["powers"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), len(P.load_powers()))
        tools = json.loads((SKILL / "data" / "tools.json").read_text(encoding="utf-8"))["tools"]
        self.assertEqual(len(self.idx["tools"]), len(tools))
        sp = json.loads((SKILL / "data" / "superpowers.json").read_text(encoding="utf-8"))["items"]
        self.assertEqual(len(self.idx["superpowers"]), len(sp))
        self.assertEqual(self.idx["counts"]["powers"], len(ids))

    def test_every_power_has_an_address(self):
        sp_ids = {s["id"] for s in self.idx["superpowers"]}
        for r in self.idx["powers"]:
            self.assertIn(r["family"], self.idx["families"], r["id"])
            self.assertIn(r["sp"], sp_ids, r["id"])
            self.assertTrue(r["group"], r["id"])
            self.assertIn(r["status"], P.STATUSES, r["id"])

    def test_tool_records_point_at_their_tool(self):
        tools = {t["id"]: t for t in self.idx["tools"]}
        linked = [r for r in self.idx["powers"] if r.get("tool")]
        self.assertTrue(linked)
        for r in linked:
            self.assertEqual(tools[r["tool"]]["power_id"], r["id"])

    def test_pages_cover_every_group_and_every_power(self):
        pages = M.render(self.idx)
        self.assertIn("README.md", pages)
        for g in self.idx["groups"]:
            self.assertIn(f"{g['id']}.md", pages)
        body = "\n".join(pages.values())
        missing = [r["id"] for r in self.idx["powers"] if f"| {r['id']} |" not in body]
        self.assertEqual(missing, [])

    def test_find_and_show(self):
        code, out, _ = run("find", "قص على الإيقاع", "--top", "5")
        self.assertEqual(code, 0)
        self.assertTrue(out.strip())
        code, out, _ = run("find", "council", "--kind", "tool", "--json")
        self.assertEqual(code, 0)
        self.assertIn("council", [r["id"] for r in json.loads(out)])
        sp = self.idx["superpowers"][0]["id"]
        code, out, _ = run("show", sp)
        self.assertEqual(code, 0)
        self.assertIn("links:", out)
        code, _, _ = run("show", "NOPE-999")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
