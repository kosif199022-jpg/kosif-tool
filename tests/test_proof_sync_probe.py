"""Known-answer proof for proofs/arabic-voice-kinetic/sync_probe.cjs (SYNC-05: frame-by-frame sync probe).

Writes two tiny seekable pages (the window.__kosif seek contract of the KOSIF renderer) whose `.w`
words become visible at known frames, runs the probe in headless Chromium (Playwright, offline,
file:// only) and checks its per-word report: an on-time page gives SYNC OK with the exact first
visible frames; a page that shows one word early gives SYNC FAIL with exit code 1.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "arabic-voice-kinetic" / "sync_probe.cjs"
PW_CANDIDATES = [os.environ.get("KOSIF_PLAYWRIGHT"), "/opt/node-tools/node_modules/playwright"]


def have_playwright() -> bool:
    if not shutil.which("node"):
        return False
    for p in ["playwright", *[c for c in PW_CANDIDATES if c]]:
        ok = subprocess.run(["node", "-e", f"require({json.dumps(p)}).chromium"], capture_output=True,
                            timeout=30).returncode == 0
        if ok:
            return True
    return False


PAGE = """<!doctype html><meta charset="utf-8"><body dir="rtl">
<span class="w">بسم</span> <span class="w">الله</span> <span class="w">الرحمن</span>
<script>
window.KOSIF_WORDS = %(words)s;
const shows = %(shows)s;  // second at which each word turns visible
const els = [...document.querySelectorAll('.w')];
window.__kosif = { duration: 1.0, seek: async (t) => {
  els.forEach((el, i) => { el.style.opacity = t + 1e-9 >= shows[i] ? '1' : '0'; });
} };
window.__kosifReady = Promise.resolve(true);
</script>"""

WORDS = [{"word": "بسم", "start": 0.10}, {"word": "الله", "start": 0.40}, {"word": "الرحمن", "start": 0.70}]


@unittest.skipUnless(have_playwright(), "node + Playwright (Chromium) needed")
class SyncProbe(unittest.TestCase):
    def run_page(self, shows):
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "index.html"
            page.write_text(PAGE % {"words": json.dumps(WORDS, ensure_ascii=False), "shows": json.dumps(shows)},
                            encoding="utf-8")
            env = dict(os.environ)
            env.setdefault("KOSIF_PLAYWRIGHT", "/opt/node-tools/node_modules/playwright")
            return subprocess.run(["node", str(SCRIPT), str(page), "30", "100"], capture_output=True, text=True,
                                  encoding="utf-8", timeout=90, env=env)

    def test_on_time_page_passes_with_exact_frames(self):
        done = self.run_page([0.10, 0.40, 0.70])
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        frames = [int(x) for x in re.findall(r"first visible frame (\d+)", done.stdout)]
        self.assertEqual(frames, [3, 12, 21])                      # ceil(start * 30)
        self.assertIn("SYNC OK words=3 max|delta|=0 ms (limit 100 ms, frame=33.3 ms) early=0", done.stdout)

    def test_early_word_fails(self):
        done = self.run_page([0.10, 0.20, 0.70])                   # word 2 shown 200 ms before it is spoken
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertIn("SYNC FAIL words=3 max|delta|=200 ms", done.stdout)
        self.assertIn("early=1", done.stdout)


if __name__ == "__main__":
    unittest.main()
