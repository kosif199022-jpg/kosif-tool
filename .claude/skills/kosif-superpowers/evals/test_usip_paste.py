#!/usr/bin/env python3
"""USIP_PASTE.md, the short protocol pasted into any assistant (appendix A34 §3 and §11): read first, run only with consent."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
PASTE = SKILL / "USIP_PASTE.md"
RAW = "https://raw.githubusercontent.com/kosif199022-jpg/kosif-tool/main/"
TREE = "https://github.com/kosif199022-jpg/kosif-tool/tree/main/"


class UsipPasteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PASTE.read_text(encoding="utf-8")

    def test_short(self):
        self.assertLess(len(self.text), 7000)

    def test_no_clone_and_run(self):
        # a pasted prompt must never make the assistant fetch the repository and execute it on its own
        self.assertNotIn("git clone", self.text)
        self.assertNotRegex(self.text, r"clone[^\n]*(&&|;)[^\n]*python")

    def test_read_first_and_consent(self):
        self.assertIn("اقرأ أولًا", self.text)
        self.assertIn("إذن", self.text)
        self.assertIn("لا تلتف", self.text)

    def test_every_link_points_at_a_file_on_main(self):
        links = re.findall(r"https://[^\s)>]+", self.text)
        self.assertTrue(links)
        for url in links:
            with self.subTest(url=url):
                if url.startswith(RAW):
                    self.assertTrue((REPO / url[len(RAW):]).is_file(), url)
                elif url.startswith(TREE):
                    self.assertTrue((REPO / url[len(TREE):]).is_dir(), url)
                else:
                    self.fail(f"unexpected link {url}")


if __name__ == "__main__":
    unittest.main()
