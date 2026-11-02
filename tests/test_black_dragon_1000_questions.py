"""Ensure 1000 detailed Black Dragon proposals remain intact and unapproved."""
import re
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def nums(text):
    return [int(n) for n in re.findall(r"(?m)^(\d{3,4})\. \*\*السؤال التفصيلي:", text)]


class BlackDragonThousandQuestionsTests(unittest.TestCase):
    def test_one_thousand_numbered_questions_with_recommendations(self):
        doc = (DOCS / "BLACK_DRAGON_1000_QUESTIONS_301_TO_1300.md").read_text(encoding="utf-8")
        assert len(nums(doc)) == 1000
        self.assertEqual(nums(doc), list(range(301, 1301)))
        self.assertEqual(doc.count("**إجابتي المقترحة:**"), 1000)
        self.assertEqual(len(re.findall(r"(?m)^## المحور ", doc)), 50)
        self.assertIn("ولم يوافق المستخدم عليها بعد", doc)

    def test_five_mobile_parts_match_exact_full_questions(self):
        all_doc = (DOCS / "BLACK_DRAGON_1000_QUESTIONS_301_TO_1300.md").read_text(encoding="utf-8")
        for i in range(5):
            a = 301 + i * 200
            b = a + 199
            piece = (DOCS / f"BLACK_DRAGON_QUESTIONS_{a}_TO_{b}.md").read_text(encoding="utf-8")
            self.assertEqual(nums(piece), list(range(a, b + 1)))
            self.assertEqual(piece.count("**إجابتي المقترحة:**"), 200)
            self.assertIn(f"{a}", all_doc)
            self.assertIn(f"{b}", all_doc)

    def test_no_new_questions_accidentally_marked_approved(self):
        doc = (DOCS / "BLACK_DRAGON_1000_QUESTIONS_301_TO_1300.md").read_text(encoding="utf-8")
        self.assertIn("مقترحة للنقاش", doc)
        self.assertNotIn("اعتمد المالك جميع الإجابات", doc)


if __name__ == "__main__":
    unittest.main()
