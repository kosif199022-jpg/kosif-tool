#!/usr/bin/env python3
"""USIP v5.5 Pro intelligence passes in scripts/think.py (appendix A30): think.py pro and its fitted council."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "think.py"


def run(*args, ok=True):
    r = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True, timeout=120)
    if ok and r.returncode != 0:
        raise AssertionError(f"{args} -> {r.returncode}\n{r.stderr}")
    return r


class ProPassesTest(unittest.TestCase):
    def test_depths_grow_passes_and_seats(self):
        got = {}
        for depth in ("standard", "deep", "max"):
            r = json.loads(run("pro", "اعمل فيديو موشن جرافيك عربي لإطلاق منتج", "--depth", depth, "--json").stdout)
            got[depth] = (len(r["passes"]), r["council"]["seats"], len(r["council"]["members"]))
            for x in r["passes"]:
                for k in ("question", "artifact", "falsifier", "tool"):
                    self.assertTrue(x[k], f"{x['id']} needs {k}")
        self.assertEqual(got, {"standard": (4, 5, 5), "deep": (8, 9, 9), "max": (12, 15, 15)})

    def test_max_council_covers_every_lane_and_is_deterministic(self):
        a = json.loads(run("pro", "راجع أمان الكود", "--depth", "max", "--json").stdout)
        b = json.loads(run("pro", "راجع أمان الكود", "--depth", "max", "--json").stdout)
        self.assertEqual(a["council"]["members"], b["council"]["members"])
        lanes = {m.rsplit("[", 1)[1].rstrip("]") for m in a["council"]["members"]}
        self.assertEqual(lanes, {"cross_domain", "verification", "feasibility", "audience", "guardrails"})
        self.assertIn("--seats 15", a["council"]["command"])
        self.assertEqual(len(a["modes"]), 2)
        self.assertEqual(len(a["models"]), 3)

    def test_text_output_and_bad_depth(self):
        out = run("pro", "قرار تسعير").stdout
        self.assertIn("PRO ·", out)
        self.assertIn("COUNCIL_SIMULATED", out)
        self.assertNotEqual(run("pro", "x", "--depth", "huge", ok=False).returncode, 0)


if __name__ == "__main__":
    unittest.main()
