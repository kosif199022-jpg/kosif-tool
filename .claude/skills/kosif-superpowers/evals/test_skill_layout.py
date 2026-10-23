"""The skill layout map (data/skill_layout.json, scripts/skill_layout.py, references/LAYOUT.md) — USIP v5.4."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SK / "scripts"))
import skill_layout as SL  # noqa: E402


class SkillLayoutTest(unittest.TestCase):
    def test_self_test(self):
        p = subprocess.run([sys.executable, str(SK / "scripts" / "skill_layout.py"), "--self-test"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_live_layout_is_clean(self):
        errs = [m for lv, m in SL.problems() if lv == "error"]
        self.assertEqual(errs, [])

    def test_every_reference_file_has_one_section(self):
        got = SL.assign(SL.load(), SL.disk_files())
        self.assertTrue(got)
        self.assertEqual({f: s for f, s in got.items() if len(s) != 1}, {})

    def test_entry_documents_and_protocol_stay_in_place(self):
        lay = {s["id"]: s for s in SL.load()["sections"]}
        self.assertIsNone(lay["entry"]["target"])
        self.assertIsNone(lay["protocol"]["target"])
        for f in ("references/INDEX.md", "START.md", "PROTOCOL.md", "USIP_PORTABLE.md"):
            self.assertIn(f, lay["entry"]["files"])
        moved = {src for src, _dst in SL.planned_moves(SL.load())}
        for keep in ("references/INDEX.md", "references/superpowers.md", "references/hubs.md", "references/telegram-typography-knowledge-library.md"):
            self.assertNotIn(keep, moved, "pasted prompts and raw links name this path; it must not move")


if __name__ == "__main__":
    unittest.main()
