"""USIP v5.5 protocol library (references/library/, built by scripts/smart_capabilities.py library; appendix A28)."""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "kosif-superpowers"
SCRIPT = SKILL / "scripts" / "smart_capabilities.py"
LIB = SKILL / "references" / "library"
CELL = r"(?:[^|\\]|\\.)*\| "   # a table cell whose text may hold escaped pipes (\|)
spec = importlib.util.spec_from_file_location("smart_capabilities_lib", SCRIPT)
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)


class LibraryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = sc.load()
        cls.pages = sc.library_pages(cls.index)

    def test_library_is_fresh(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "library-check"], capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_deterministic(self):
        self.assertEqual(self.pages, sc.library_pages(self.index))

    def test_one_chapter_per_group_and_every_power_once(self):
        groups = [g["id"] for g in self.index["groups"]]
        self.assertEqual(sorted(p.stem for p in self.pages if p.stem != "INDEX"), sorted(groups))
        seen = []
        for p, text in self.pages.items():
            if p.stem != "INDEX":
                seen += re.findall(r"^\| `([^`]+)` \| " + CELL + CELL + r"(?:proven|ready|documented|seen|install|key|idea) \|", text, re.M)
        ids = [x["id"] for x in self.index["powers"]]
        self.assertEqual(len(seen), len(ids))
        self.assertEqual(sorted(seen), sorted(ids))

    def test_links_resolve(self):
        for p, text in self.pages.items():
            for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
                if target.startswith("http"):
                    continue
                with self.subTest(page=p.name, link=target):
                    self.assertTrue((p.parent / target).exists())

    def test_tools_are_real_registry_entries(self):
        reg = {t["id"] for t in json.loads((SKILL / "data" / "tools.json").read_text(encoding="utf-8"))["tools"]}
        motion = self.pages[LIB / "motion.md"]
        listed = re.findall(r"^\| `([a-z0-9-]+)` \| [^|]+\| `", motion, re.M)
        self.assertTrue(listed)
        self.assertTrue(set(listed) <= reg)


class FullLibraryTest(unittest.TestCase):
    """usip-library/ at the repo root: a protocol card per power and per tool (smart_capabilities.py cards)."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(SKILL / "scripts"))
        import _usip_cards
        cls.uc = _usip_cards
        cls.pages = _usip_cards.build()

    def test_fresh_and_large(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "cards-check"], capture_output=True, text=True, timeout=600)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr)
        self.assertGreaterEqual(sum(t.count("\n") for t in self.pages.values()), 300_000)

    def test_every_power_and_tool_has_a_card(self):
        text = "\n".join(t for p, t in self.pages.items() if p.startswith("cards/"))
        ids = re.findall(r"^### `([^`]+)` — ", text, re.M)
        cat = [x["id"] for x in sc.load()["powers"]]
        self.assertEqual(sorted(ids), sorted(cat))
        tools = "\n".join(t for p, t in self.pages.items() if p.startswith("tools/"))
        reg = [t["id"] for t in json.loads((SKILL / "data" / "tools.json").read_text(encoding="utf-8"))["tools"]]
        self.assertEqual(sorted(re.findall(r"^### `([^`]+)` — ", tools, re.M)), sorted(reg))

    def test_links_resolve(self):
        out = self.uc.OUT
        for p, text in self.pages.items():
            for target in set(re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text)):
                if not target.startswith("http"):
                    with self.subTest(page=p, link=target):
                        self.assertTrue(((out / p).parent / target).exists())

    def test_single_file(self):
        one = self.uc.single(self.pages)
        self.assertTrue(one.startswith("<!-- usip-library/README.md -->"))
        self.assertEqual(one.count("<!-- usip-library/"), len(self.pages))


if __name__ == "__main__":
    unittest.main()
