"""Known-answer proof for proofs/neon-glow/schedule.js (GLOW-01, GLOW-02): the shared neon ignition schedule.

The file must evaluate in a browser-like context (node, with a `window` object) to exactly the JSON that
the Python sound generator extracts with its regex, and the schedule must keep its contract: segments are
[start, end, level] with 0 <= level <= 1, ordered and non-overlapping, each tube's last segment ends at
99 (stays lit), and the Latin letters, the faulty letter, cup and steam fit inside the film.
The audio renderer itself is not run here (it needs soundfile and pyloudnorm).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "neon-glow" / "schedule.js"
# the same pattern the neon-glow audio generator uses to read this file
PY_PATTERN = re.compile(r"^window\.NEON_SCHEDULE = (\{.*\})\s*;", re.S | re.M)


def python_view() -> dict:
    return json.loads(PY_PATTERN.search(SCRIPT.read_text(encoding="utf-8")).group(1))


class Schedule(unittest.TestCase):
    def setUp(self):
        self.S = python_view()

    def check_segments(self, segs, lit_forever=True):
        prev_end = -1.0
        for a, b, v in segs:
            self.assertLess(a, b)
            self.assertGreaterEqual(a, prev_end - 1e-9)
            self.assertTrue(0.0 <= v <= 1.0)
            prev_end = b
        if lit_forever:
            self.assertEqual(segs[-1][1], 99)
            self.assertEqual(segs[-1][2], 1)

    def test_known_values(self):
        S = self.S
        self.assertEqual((S["duration"], S["fps"], S["fadeIn"], S["warmup"]), (10, 30, 0.6, 0.5))
        self.assertEqual(S["arabic"][-1], [1.50, 99, 1])
        self.assertEqual(S["faulty"]["index"], 6)
        self.assertEqual(S["sweep"], [5.6, 7.4])

    def test_segment_contract(self):
        S = self.S
        self.check_segments(S["arabic"])
        self.check_segments(S["latinPattern"])
        self.check_segments(S["faulty"]["pattern"])
        self.check_segments(S["faulty"]["dropouts"], lit_forever=False)

    def test_timeline_fits_the_film(self):
        S = self.S
        letters = len("OPENLATE")
        self.assertLess(S["faulty"]["index"], letters)
        last_latin = S["latinStart"] + (letters - 1) * S["latinStep"]
        self.assertLess(last_latin, S["duration"])
        for a, b in (S["cup"]["body"], S["cup"]["handle"], S["cup"]["saucer"], S["sweep"]):
            self.assertTrue(0 <= a < b <= S["duration"])
        self.assertLess(S["cup"]["body"][0], S["cup"]["saucer"][1])
        self.assertTrue(all(0 <= a < b <= S["duration"] for a, b, _ in S["faulty"]["dropouts"]))
        self.assertTrue(all(len(st) == 3 and set(st) <= {0, 1} for st in S["steam"]["states"]))

    @unittest.skipUnless(shutil.which("node"), "node missing")
    def test_browser_and_python_views_agree(self):
        js = ("const vm=require('vm'),fs=require('fs');const ctx={window:{}};"
              "vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),ctx);"
              "process.stdout.write(JSON.stringify(ctx.window.NEON_SCHEDULE));")
        done = subprocess.run(["node", "-e", js, str(SCRIPT)], capture_output=True, text=True, timeout=30)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(json.loads(done.stdout), self.S)


if __name__ == "__main__":
    unittest.main()
