"""Structural verification of 1,000 owner-approved Black Dragon design decisions.

Question counts and unique strings do not prove implementation or quality.
Separate execution receipts and content-quality reviews remain required.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BLACK_DRAGON_1000_QUESTIONS_301_TO_1300.md"
REVIEW = ROOT / "docs" / "BLACK_DRAGON_1000_QUESTIONS_REVIEW.md"
LEDGER = ROOT / "docs" / "BLACK_DRAGON_APPROVED_ANSWERS_LEDGER_301_TO_1300.json"


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

    def test_owner_approval_is_documented_but_not_equated_to_shipping(self):
        self.assertIn("اعتمد المالك جميع الإجابات المقترحة", self.content)
        self.assertIn(LEDGER.name, self.content)
        self.assertIn("الاعتماد لا يثبت تنفيذ", self.content)
        self.assertNotIn("لم يوافق المستخدم عليها بعد", self.content)
        review = REVIEW.read_text(encoding="utf-8")
        self.assertIn("الربط", review)
        self.assertIn("1300 قرار تصميم معتمد", review)
        self.assertIn("لا يمكن اعتبار كل سؤال مرتبطًا بمهارة/أداة", review)
        self.assertNotIn("لم تُعتمد الإجابات 301–1300 بعد", review)


if __name__ == "__main__":
    unittest.main()
