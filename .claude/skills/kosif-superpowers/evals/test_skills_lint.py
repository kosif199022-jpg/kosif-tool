"""Repo-wide SKILL.md lint (scripts/skills_lint.py): no new errors may appear."""
import json
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import skills_lint  # noqa: E402

KNOWN = set(json.loads((SK / "data" / "skills_lint_known.json").read_text(encoding="utf-8"))["known_errors"])


class SkillsLint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rep = skills_lint.lint()

    def test_covers_every_group(self):
        self.assertEqual(set(self.rep["summary"]), {"top-level", "atlas", "superskills", "obra", "styles"})
        self.assertGreater(sum(s["skills"] for s in self.rep["summary"].values()), 700)

    def test_no_new_errors(self):
        found = {f"{r['path']}\t{e}" for r in self.rep["skills"] for e in r["errors"]}
        new = sorted(found - KNOWN)
        self.assertEqual(new, [], "new skill lint errors (fix them; do not add them to data/skills_lint_known.json)")

    def test_links_in_code_are_ignored(self):
        text = "see `[x](missing.md)` and\n```\n[y](also-missing.md)\n```\n[z](https://example.com)"
        self.assertEqual(skills_lint.broken_links(text, SK), [])
        self.assertEqual(skills_lint.broken_links("[a](nope/missing.md)", SK), ["nope/missing.md"])

    def test_json_frontmatter_is_read(self):
        fm, _ = skills_lint.parse_frontmatter('---\n{"name": "x", "description": "does y"}\n---\nbody')
        self.assertEqual(fm, {"name": "x", "description": "does y"})


if __name__ == "__main__":
    unittest.main()
