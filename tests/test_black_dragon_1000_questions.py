"""Protect the 1,000 owner-approved Black Dragon design decisions (301-1300).

Approval of answers is not proof of implementation or authorization to take
external, destructive, paid, or permission-changing actions.
"""
import json
import re
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
FULL = DOCS / "BLACK_DRAGON_1000_QUESTIONS_301_TO_1300.md"
LEDGER = DOCS / "BLACK_DRAGON_APPROVED_ANSWERS_LEDGER_301_TO_1300.json"


def rows(text):
    questions = re.findall(
        r"(?m)^(\d{3,4})\. \*\*السؤال التفصيلي:\*\* (.+)$", text
    )
    answers = re.findall(
        r"(?m)^\s+\*\*إجابتي المقترحة:\*\* (.+)$", text
    )
    if len(questions) != len(answers):
        raise AssertionError("Every question must have exactly one answer")
    return [(int(n), question, answer) for (n, question), answer
            in zip(questions, answers)]


def checksum(number, question, answer):
    """FNV-1a 64-bit over UTF-8: ID + newline + question + newline + answer."""
    digest = 0xCBF29CE484222325
    for byte in f"{number}\n{question}\n{answer}".encode("utf-8"):
        digest = ((digest ^ byte) * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return f"{digest:016x}"


class BlackDragonThousandQuestionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full_text = FULL.read_text(encoding="utf-8")
        cls.questions = rows(cls.full_text)

    def test_one_thousand_numbered_owner_approved_questions(self):
        self.assertEqual([n for n, _, _ in self.questions],
                         list(range(301, 1301)))
        self.assertEqual(len(self.questions), 1000)
        self.assertEqual(len(re.findall(r"(?m)^## المحور ", self.full_text)), 50)
        self.assertIn("اعتمد المالك جميع الإجابات المقترحة للأسئلة 301–1300",
                      self.full_text)
        self.assertIn("الاعتماد لا يثبت تنفيذ", self.full_text)
        self.assertNotIn("ولم يوافق المستخدم عليها بعد", self.full_text)

    def test_five_mobile_parts_match_exact_questions_and_answers(self):
        for i in range(5):
            first = 301 + i * 200
            last = first + 199
            part = (DOCS / f"BLACK_DRAGON_QUESTIONS_{first}_TO_{last}.md"
                    ).read_text(encoding="utf-8")
            self.assertEqual(rows(part), self.questions[i * 200:(i + 1) * 200])
            self.assertIn("اعتمدها المالك", part)

    def test_approved_ledger_has_a_matching_checksum_for_every_answer(self):
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(ledger["decision_count"], 1000)
        self.assertEqual((ledger["question_min"], ledger["question_max"]),
                         (301, 1300))
        self.assertEqual(ledger["approved_on"], "2026-11-02")
        self.assertEqual(
            ledger["decision_type"],
            "owner_approved_proposed_answers_as_design_decisions")
        self.assertEqual(
            ledger["checksum_algorithm"],
            "fnv1a64_utf8_id_newline_question_newline_answer_v1")
        self.assertEqual(ledger["source_file"], f"docs/{FULL.name}")
        self.assertEqual(set(ledger["items"]), {str(n) for n in range(301, 1301)})
        for number, question, answer in self.questions:
            with self.subTest(question=number):
                self.assertEqual(ledger["items"][str(number)],
                                 checksum(number, question, answer))

    def test_index_and_review_consistently_report_approval(self):
        index = (DOCS / "BLACK_DRAGON_1000_QUESTIONS_INDEX.md"
                 ).read_text(encoding="utf-8")
        review = (DOCS / "BLACK_DRAGON_1000_QUESTIONS_REVIEW.md"
                  ).read_text(encoding="utf-8")
        for text in (index, review):
            self.assertIn("اعتمد المالك", text)
            self.assertIn(LEDGER.name, text)
        self.assertIn("لا يمكن اعتبار كل سؤال مرتبطًا بمهارة/أداة", review)
        self.assertNotIn("لم تُعتمد الإجابات 301–1300 بعد", review)


if __name__ == "__main__":
    unittest.main()
