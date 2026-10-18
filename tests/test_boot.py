"""Boot entry point: live self-briefing and the generated CAPABILITIES.md / llms.txt for a bare repository link."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOT = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "boot.py"


def run(*args):
    return subprocess.run([sys.executable, str(BOOT), *args], capture_output=True, text=True, timeout=120)


class BootTest(unittest.TestCase):
    def test_live_json(self):
        proc = run("--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        d = json.loads(proc.stdout)
        self.assertGreater(d["catalog"]["powers"], 4000)
        self.assertEqual(d["catalog"]["domains"], 10)
        self.assertLessEqual(d["ready_now"], d["catalog"]["powers"])
        for u in d["top_unlocks"]:
            self.assertTrue(u["install"])

    def test_static_files_are_current(self):
        proc = run("--static", "--check")
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_capabilities_md_is_bilingual_and_links_every_family(self):
        text = (ROOT / "CAPABILITIES.md").read_text(encoding="utf-8")
        self.assertIn("إلى Claude", text)
        self.assertIn("To Claude", text)
        for f in (ROOT / ".claude" / "skills" / "kosif-superpowers" / "data" / "powers").glob("*.json"):
            self.assertIn(f"references/powers/{f.stem}.md", text)

    def test_llms_txt_shape(self):
        text = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# "))
        self.assertIn("\n> ", text)
        self.assertIn("CAPABILITIES.md", text)


if __name__ == "__main__":
    unittest.main()
