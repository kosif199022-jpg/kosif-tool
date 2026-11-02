"""Owner-approved Black Dragon decisions must be complete, unique and intact."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class DecisionContractTests(unittest.TestCase):
    def test_approved_decisions_1_to_300_are_contiguous_and_unique(self):
        old = (DOCS / "BLACK_DRAGON_100_DESIGN_DECISIONS.md").read_text(encoding="utf-8")
        new = (DOCS / "BLACK_DRAGON_200_MORE_DECISIONS_101_TO_300.md").read_text(encoding="utf-8")
        extract = lambda text: [int(m) for m in re.findall(r"(?m)^(\d{1,3})\. \*\*السؤال:", text)]
        self.assertEqual(extract(old), list(range(1, 101)))
        self.assertEqual(extract(new), list(range(101, 301)))
        self.assertIn("اعتمد المالك", old)
        self.assertIn("اعتمد المالك", new)

    def test_full_mode_override_preserved_and_not_mislabeled_executed(self):
        old = (DOCS / "BLACK_DRAGON_100_DESIGN_DECISIONS.md").read_text(encoding="utf-8")
        new = (DOCS / "BLACK_DRAGON_200_MORE_DECISIONS_101_TO_300.md").read_text(encoding="utf-8")
        four = re.search(r"(?m)^4\. (.*)$", old)
        self.assertIsNotNone(four)
        self.assertIn("تشغيل جميع الأدوات", four.group(1))
        self.assertIn("كل مهارة", four.group(1))
        self.assertIn("غير القابلة للتشغيل", four.group(1))
        self.assertIn("قرارات تصميم معتمدة", new)
        self.assertIn("ليست", new)


if __name__ == "__main__":
    unittest.main()
