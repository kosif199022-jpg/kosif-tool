"""Structural verification of the 1,000 new Black Dragon questionnaire items.

Question count/unique strings are NOT evidence that answers are good, or that
proposed capabilities are already implemented. A separate quality review exists.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BLACK_DRAGON_1000_QUESTIONS_301_TO_1300.md"
REVIEW = ROOT / "docs" / "BLACK_DRAGON_1000_QUESTIONS_REVIEW.md"


class Questions1000Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = DOC.read_text(encoding="utf-8")
        cls.questions = [(int(n), q.strip()) for n, q in
                         re.findall(r"(?m)^(\d{3,4})\. \*\*السؤال التفصيلي:\*\* (.+)$",
                                    cls.content)]
        cls.answers = re.findall(r"(?m)^\s+\*\*إجابتي المقترحة:\*\* (.+)$",
                                 cls.content)
        cls.headers = [(int(i), name) for i, name in
                       re.findall(r"(?m)^## المحور (\d{2}): (.+)$", cls.content)]

    def test_exactly_1000_numbered_questions_with_one_answer_each(self):
        self.assertEqual([number for number, _ in self.questions],
                         list(range(301, 1301)))
        self.assertEqual(len(self.answers), 1000)
        self.assertTrue(all(answer.strip() for answer in self.answers))

    def test_exactly_50_domains_each_with_20_questions(self):
        self.assertEqual([i for i, _ in self.headers], list(range(1, 51)))
        for index, (_, title) in enumerate(self.headers):
            begin = 301 + index * 20
            self.assertIn(f"{begin}–{begin+19}", title)

    def test_no_exact_duplicate_question_or_answer_strings(self):
        questions = [q for _, q in self.questions]
        self.assertEqual(len(set(questions)), len(questions))
        self.assertEqual(len(set(self.answers)), len(self.answers))

    def test_review_distinguishes_proposal_from_approved_prior_decisions(self):
        self.assertIn("لم يوافق المستخدم عليها بعد", self.content)
        review = REVIEW.read_text(encoding="utf-8")
        self.assertIn("الربط", review)
        self.assertIn("لم تُعتمد الإجابات 301–1300 بعد", review)
        self.assertIn("لا يمكن اعتبار كل سؤال مرتبطًا بمهارة/أداة", review)


if __name__ == "__main__":
    unittest.main()
