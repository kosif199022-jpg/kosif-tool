"""Guard REA intent routing against unrelated image, video and marketing prompts."""
import importlib.util
from pathlib import Path
import re
import unittest

PATH = Path(__file__).resolve().parents[1] / "scripts" / "powers.py"
spec = importlib.util.spec_from_file_location("powers", PATH)
powers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(powers)


def families(prompt):
    words = re.findall(r"[\w:]+", prompt)
    expanded = powers.expand(words, prompt)
    selected, _, _ = powers.intent_of(expanded)
    return selected


class ReaRoutingTests(unittest.TestCase):
    def test_positive_reverse_engineering_requests(self):
        for prompt in (
            "افحص تطبيق باستخدام هندسة عكسية",
            "تحليل برنامج Electron",
            "reverse engineering of an APK",
            "decompile a binary I own",
            "rea-agents static inspection",
        ):
            with self.subTest(prompt=prompt):
                self.assertIn("CODE", families(prompt))

    def test_unrelated_requests_must_not_trigger_code(self):
        for prompt in (
            "تقليد فيديو موشن جرافيك",
            "عدل هذه الصورة بشكل احترافي",
            "reverse marketing funnel campaign",
            "عايز ملف Excel للمبيعات",
        ):
            with self.subTest(prompt=prompt):
                self.assertNotIn("CODE", families(prompt))


if __name__ == "__main__":
    unittest.main()
