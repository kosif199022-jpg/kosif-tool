"""Tests for scripts/skill_loader.py — the light loading map (USIP v6.3)."""
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import skill_loader as sl  # noqa: E402


class SkillLoaderTest(unittest.TestCase):
    def test_every_skill_is_on_the_map(self):
        text = sl.render()
        for f in sl.SKILLS_ROOT.glob("*/SKILL.md"):
            self.assertIn(f.relative_to(sl.REPO).as_posix(), text)

    def test_every_appendix_and_group_is_on_the_map(self):
        text = sl.render()
        self.assertGreaterEqual(len(sl.appendices()), 30)
        for a in sl.appendices():
            self.assertIn(a["title"], text)
        for h in sl.hubs():
            self.assertIn(f"`{h['id']}`", text)

    def test_section_ranges_cover_skill_md(self):
        secs = sl.sections(sl.SKILL / "SKILL.md")
        self.assertTrue(secs)
        for a, b in zip(secs, secs[1:]):
            self.assertEqual(a["end"] + 1, b["start"])

    def test_full_mode_line_first(self):
        text = sl.render()
        self.assertLess(text.index("Full-power mode"), text.index("## "))
        self.assertIn("بلا إذن", sl.FULL_MODE_LINE)

    def test_need_routes_council_and_montage(self):
        ids = {p["id"] for p in sl.need("council devil advocate")}
        self.assertTrue({"A13", "A30"} & ids)
        kinds = {p["id"] for p in sl.need("اعمل مونتاج ريلز من فيديو")}
        self.assertIn("motion", kinds)

    def test_loader_md_is_current(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(sl.main(["build", "--check"]), 0)

    def test_protocol_and_portables_open_with_full_mode(self):
        for f in (sl.SKILL / "PROTOCOL.md", sl.REPO / "docs/protocol/USIP_PORTABLE_v6_3.md", sl.SKILL / "USIP_PORTABLE.md"):
            head = f.read_text(encoding="utf-8")[:1500]
            self.assertIn("وضع التفعيل الكامل", head, f.name)


if __name__ == "__main__":
    unittest.main()
