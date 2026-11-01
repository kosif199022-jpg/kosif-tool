"""Can Claude see and reach every project skill? (USIP v6.5)

Claude Code lists a skill only when `.claude/skills/<name>/SKILL.md` opens with YAML frontmatter that has a
`name` and a `description`; the light map LOADER.md and `skill_loader.py need` are how a session finds the
right one without reading every file. These checks fail when a new skill would be invisible or unreachable.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / ".claude" / "skills"
sys.path.insert(0, str(SKILLS / "kosif-superpowers" / "scripts"))
import skill_loader as SL  # noqa: E402

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(md: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if kv:
            key = kv.group(1)
            out[key] = kv.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    for k, v in out.items():
        if v[:1] in "|>":
            out[k] = v[1:].lstrip("-+ ").strip()
        elif len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            out[k] = v[1:-1]
    return out


class SkillDiscoveryTest(unittest.TestCase):
    def setUp(self):
        self.files = sorted(SKILLS.glob("*/SKILL.md"))

    def test_every_skill_has_valid_frontmatter(self):
        self.assertGreaterEqual(len(self.files), 8)
        for f in self.files:
            fm = frontmatter(f.read_text(encoding="utf-8"))
            with self.subTest(skill=f.parent.name):
                self.assertTrue(fm, "SKILL.md must open with --- frontmatter ---")
                self.assertEqual(fm.get("name"), f.parent.name, "name must equal the folder name")
                self.assertRegex(fm["name"], NAME_RE)
                self.assertLessEqual(len(fm["name"]), 64)
                desc = fm.get("description", "")
                self.assertGreaterEqual(len(desc), 40, "a description says when to use the skill")
                self.assertLessEqual(len(desc), 1024, "Claude Code truncates longer descriptions")

    def test_every_folder_under_skills_is_a_skill(self):
        for d in sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith(".")):
            with self.subTest(folder=d.name):
                self.assertTrue((d / "SKILL.md").is_file(), "a folder without SKILL.md is invisible to Claude")

    def test_light_map_lists_every_skill(self):
        loader = (SKILLS / "kosif-superpowers" / "LOADER.md").read_text(encoding="utf-8")
        for f in self.files:
            with self.subTest(skill=f.parent.name):
                self.assertIn(f.relative_to(REPO).as_posix(), loader, "run skill_loader.py build")

    def test_each_skill_is_found_from_its_own_purpose(self):
        """`skill_loader.py need` with the first words of a skill's description finds that skill."""
        for s in SL.skills():
            if s["name"] == "kosif-superpowers":
                continue   # the hub itself is loaded first, never routed to
            words = " ".join(re.findall(r"\w+", s["description"])[:25])
            got = [p["id"] for p in SL.need(words, n=12) if p["kind"] == "skill"]
            with self.subTest(skill=s["name"]):
                self.assertIn(s["name"], got)


if __name__ == "__main__":
    unittest.main()
