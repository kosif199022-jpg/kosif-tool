"""Static checks on templates/ (request templates, project documents, word timings)."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fixture import REAL_ROOT  # noqa: E402

TDIR = REAL_ROOT / "templates"
PLACEHOLDER = re.compile(r"\{(\w+)\}")
ARABIC = re.compile(r"[؀-ۿ]")
DOC_PLACEHOLDERS = {
    "style_name", "id", "page", "video", "creator", "origin", "type", "categories", "playbooks", "skill", "brief",
    "aspect", "resolution", "fps", "duration", "frames", "stack", "date", "repo", "difficulty",
}


class RequestTemplateTest(unittest.TestCase):
    def test_ar_and_en_share_placeholders_documented_in_readme(self):
        ar = set(PLACEHOLDER.findall((TDIR / "claude_request.ar.txt").read_text(encoding="utf-8")))
        en = set(PLACEHOLDER.findall((TDIR / "claude_request.en.txt").read_text(encoding="utf-8")))
        self.assertEqual(ar, en)
        documented = set(re.findall(r"`\{(\w+)\}`", (TDIR / "claude_request.README.md").read_text(encoding="utf-8")))
        self.assertEqual(ar, documented, "README placeholder table must match the templates")
        for key in ("repo", "id", "name", "page", "brief_line", "playbooks", "source", "aspect", "resolution", "fps", "duration", "stack", "lang", "brand", "audio", "notes"):
            self.assertIn(key, ar)


class ProjectDocumentTemplateTest(unittest.TestCase):
    def read(self, name: str) -> str:
        return (TDIR / name).read_text(encoding="utf-8")

    def test_placeholders_are_the_ones_scaffold_fills(self):
        for name in ("STYLE.md", "PLAN.md", "TEST_REPORT.md"):
            with self.subTest(template=name):
                used = set(PLACEHOLDER.findall(self.read(name)))
                self.assertTrue(used, "template must contain placeholders")
                self.assertLessEqual(used, DOC_PLACEHOLDERS, f"unknown placeholders: {used - DOC_PLACEHOLDERS}")
                for key in ("style_name", "id", "date"):
                    self.assertIn(key, used)

    def test_bilingual_headings_arabic_first(self):
        for name in ("STYLE.md", "PLAN.md", "TEST_REPORT.md"):
            headings = [h for h in re.findall(r"^#{2,3}\s+(.+)$", self.read(name), re.M)]
            self.assertGreaterEqual(len(headings), 5, name)
            for h in headings:
                with self.subTest(template=name, heading=h):
                    self.assertIn("/", h, "heading must carry Arabic and English")
                    ar_part, en_part = h.split("/", 1)
                    self.assertTrue(ARABIC.search(ar_part), "Arabic comes first")
                    self.assertTrue(re.search(r"[A-Za-z]", en_part), "English second")

    def test_style_md_separates_observed_from_assumed_and_has_token_tables(self):
        text = self.read("STYLE.md")
        self.assertLess(text.index("Observed from the reference"), text.index("## 3. ما افترضته / Assumed"))
        for section in ("الألوان / Colors", "الخطوط / Type", "Line weights", "Easing and timing", "الكاميرا / Camera"):
            self.assertIn(section, text)
        self.assertIn("Measured or estimated", text)

    def test_plan_md_scene_table_and_word_timing(self):
        text = self.read("PLAN.md")
        header = next(line for line in text.splitlines() if line.startswith("| # |"))
        for col in ("Start", "End", "Action", "Camera", "Transition", "Audio cue", "Assets"):
            self.assertIn(col, header)
        self.assertIn("## 3. توقيت الكلمات / Word timing", text)
        self.assertIn("words.json", text)
        self.assertIn("100 ms", text)

    def test_test_report_lists_required_checks_with_result_column(self):
        text = self.read("TEST_REPORT.md")
        header = next(line for line in text.splitlines() if line.startswith("| # |"))
        self.assertIn("PASS / FAIL", header)
        for check in ("Duration", "Frame rate", "Frame count", "Audio track present", "-14 LUFS", "Legibility at phone size", "RTL shaping", "Sync tolerance", "100 ms"):
            self.assertIn(check, text)
        self.assertIn("ffprobe", text)
        self.assertIn("loudnorm", text)


class WordsExampleTest(unittest.TestCase):
    def test_arabic_sentence_with_monotonic_timings(self):
        data = json.loads((TDIR / "words.example.json").read_text(encoding="utf-8"))
        self.assertEqual(data["language"], "ar")
        self.assertTrue(ARABIC.search(data["text"]))
        words = data["words"]
        self.assertGreaterEqual(len(words), 5)
        self.assertEqual(" ".join(w["word"] for w in words), data["text"])
        last_end = 0.0
        for w in words:
            self.assertTrue(ARABIC.search(w["word"]))
            self.assertGreaterEqual(w["start"], last_end)
            self.assertGreater(w["end"], w["start"])
            self.assertIsInstance(w["emphasis"], bool)
            last_end = w["end"]
        self.assertLessEqual(last_end, data["duration_s"])
        self.assertTrue(any(w["emphasis"] for w in words))


if __name__ == "__main__":
    unittest.main()
