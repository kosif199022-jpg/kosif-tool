"""Tests for the owned-repositories map; reads only the committed registry and the capability groups."""
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import owned_repos as O


class OwnedReposTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = O.load()

    def test_registry_consistent(self):
        self.assertEqual(O.problems(self.reg), [])

    def test_rendered_doc_current(self):
        self.assertEqual(O.DOC.read_text(encoding="utf-8"), O.render(self.reg))

    def test_private_repos_keep_only_counts(self):
        for r in self.reg["repos"]:
            if r["visibility"] == "private":
                self.assertLessEqual(set(r.get("measured", {})), set(O.PRIVATE_MEASURED) | {"secret_like_hits"}, r["repo"])

    def test_skill_map_covers_every_group(self):
        rows = O.skill_map(self.reg)
        self.assertEqual({r["group"] for r in rows}, set(O.groups()))
        for r in rows:
            self.assertLessEqual(r["have_now"] + r["learn_by_install"] + r["learn_by_key"], r["powers"])

    def test_find_routes_drawing_and_audit(self):
        self.assertIn("kosif199022-jpg/kosif-studio", [x["repo"] for x in O.rank("رسم شخصيات", self.reg)])
        top = O.rank("audit materiality sampling", self.reg)
        self.assertEqual(top[0]["repo"], "kosif199022-jpg/moon")

    def test_services_connected(self):
        ids = {v["id"] for v in self.reg["services"]}
        self.assertIn("kosif-think-mcp", ids)
        self.assertTrue(any(e["to"] == "kosif-think-mcp" and e["kind"] == "requires-for-full-pro" for e in self.reg["relations"]))
        self.assertNotIn("workers.dev", O.DOC.read_text(encoding="utf-8"))

    def test_digest_never_writes_secret_values(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "o_r"
            root.mkdir()
            fake = "gh" + "p_" + "A" * 36
            (root / "a.py").write_text(f"T = '{fake}'\n", encoding="utf-8")
            d = O.digest_repo(root)
            self.assertEqual(d["secret_like"], {"github-token": 1})
            self.assertNotIn(fake, repr(d))


if __name__ == "__main__":
    unittest.main()
