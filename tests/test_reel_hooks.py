"""Offline tests for the kosif-reel-hooks skill (Arabic-first Reel tools)."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude/skills/kosif-reel-hooks"
spec = importlib.util.spec_from_file_location("reel_tools", SKILL / "scripts/reel_tools.py")
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)


class TestHookScore(unittest.TestCase):
    def test_arabic_hook_is_read(self):
        r = rt.score_hook("خسرت ٤٠٠٠ جنيه في عقد ناقصه سطر واحد.")
        self.assertEqual(r["language"], "ar")
        self.assertEqual(r["verdict"], "STRONG")
        self.assertGreater(r["checks"]["LENGTH"]["score"], 0)

    def test_arabic_indic_digits_are_numbers(self):
        self.assertIn("4000", " ".join(rt.concrete_markers("خسرت ٤٠٠٠ جنيه")))

    def test_greeting_and_preamble_are_dealbreakers(self):
        for line in ("أهلاً بيكم يا جماعة، النهارده هنتكلم عن العقود.",
                     "في الفيديو ده هوريكم إزاي تكتب كابشن.",
                     "استنى متقلبش! 🔥 #ريلز",
                     "Hey guys, in this video I'll show you how."):
            r = rt.score_hook(line)
            self.assertEqual(r["verdict"], "WEAK", line)
            self.assertTrue(r["flags"], line)

    def test_ranking_puts_specific_hook_first(self):
        rows = sorted((rt.score_hook(h) for h in (
            "أهلاً، النهارده هنتكلم عن العقود.",
            "خسرت ٤٠٠٠ جنيه في عقد ناقصه سطر واحد.")), key=lambda r: -r["score"])
        self.assertTrue(rows[0]["hook"].startswith("خسرت"))

    def test_negative_command_addresses_viewer(self):
        r = rt.score_hook("متبعتش عرض سعر لعميل قبل ما تعمل الحاجة دي.")
        self.assertGreaterEqual(r["checks"]["ADDRESS"]["score"], 90)

    def test_screen_card_word_limit(self):
        r = rt.score_hook("خسرت ٤٠٠٠ جنيه.", screen="استنى قبل ما تبعت العرض ده للعميل")
        self.assertFalse(r["screen"]["ok"])
        self.assertTrue(rt.score_hook("خسرت ٤٠٠٠ جنيه.", screen="٤٠٠٠ جنيه ضاعوا")["screen"]["ok"])

    def test_library_examples_are_usable(self):
        lib = json.loads((SKILL / "data/hooks_ar.json").read_text(encoding="utf-8"))
        self.assertEqual(len(lib["hooks"]), 16)
        for h in lib["hooks"]:
            r = rt.score_hook(h["example"], h["on_screen"])
            self.assertNotEqual(r["verdict"], "WEAK", h["name"])
            self.assertTrue(r["screen"]["ok"], h["name"])


class TestBeats(unittest.TestCase):
    SCRIPT = ("العرض كان بياخد مني خمس ساعات. دلوقتي عشرين دقيقة.\n"
              "لو بتبيع خدمات، ده يوم إجازتك راجع.\n"
              "اكتب كلمة قالب وأنا أبعتهولك. عشرين دقيقة بس.\n")

    def test_arabic_rate_and_loop(self):
        a = rt.beat_sheet(self.SCRIPT, target=12)
        self.assertEqual(a["wpm"], 140)
        self.assertTrue(any("لوب" in n for n in a["notes"]))

    def test_long_hook_and_missing_loop_are_flagged(self):
        a = rt.beat_sheet("أنا النهارده عايز أحكيلكم عن حاجة حصلت معايا من فترة طويلة في الشغل بتاعي.\n"
                          "وفي الآخر اتعلمت درس.\n")
        joined = " ".join(a["flags"])
        self.assertIn("الهوك", joined)
        self.assertIn("مفيش لوب", joined)

    def test_target_mismatch(self):
        a = rt.beat_sheet(self.SCRIPT, target=60)
        self.assertTrue(any("أقصر" in f for f in a["flags"]))


class TestClean(unittest.TestCase):
    def test_strips_hidden_chars_and_dashes(self):
        r = rt.clean_text("المحتوى — هو الملك.​", fix=True)
        self.assertNotIn("​", r["fixed"])
        self.assertNotIn("—", r["fixed"])
        self.assertIn("invisible", r["auto_fixed"])

    def test_flags_written_arabic(self):
        r = rt.clean_text("في عالم اليوم، لا شك أن المحتوى مهم. دعونا نبدأ رحلة النجاح.")
        phrases = {f.get("phrase") for f in r["found"]}
        self.assertTrue({"في عالم اليوم", "لا شك أن", "دعونا", "رحلة"} <= phrases)
        self.assertEqual(r["verdict"], "FIX")

    def test_plain_egyptian_passes(self):
        r = rt.clean_text("خسرت ٤٠٠٠ جنيه. العقد كان ناقصه سطر. دلوقتي بكتب السطر ده في كل عقد.")
        self.assertEqual(r["verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
