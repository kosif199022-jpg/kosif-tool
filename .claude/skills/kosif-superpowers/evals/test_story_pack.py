"""Story / screenplay / scene-sequence question pack (data/question_packs.json, A17) in the USIP brief.

The pack adds questions WITH suggested defaults inside the one report: the core five at L1, all ten at L2/L3, none
at L0; it never blocks, never makes a dialect a rule and never defaults to spending.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_story_pack.py' -v
"""
import json
import re
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import skill_intelligence as S  # noqa: E402

PACK_FILE = SK / "data" / "question_packs.json"
PACK = json.loads(PACK_FILE.read_text(encoding="utf-8"))["packs"]["story"]
CORE = [q["question"] for q in PACK["questions"] if q["tier"] == "core"]
ALL = [q["question"] for q in PACK["questions"]]


def pack_qs(an):
    return [q for q in an["questions"] if q["question"] in ALL]


class TestPackFile(unittest.TestCase):
    def test_schema_and_counts(self):
        data = json.loads(PACK_FILE.read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], "kosif.question_packs.v1")
        self.assertEqual(len(CORE), 5)
        self.assertEqual(len(ALL), 10)
        self.assertEqual([q["tier"] for q in PACK["questions"]], ["core"] * 5 + ["extended"] * 5)
        self.assertEqual(PACK["levels"], {"L0": 0, "L1": 5, "L2": 10, "L3": 10})
        for q in PACK["questions"]:
            self.assertTrue(q["suggested_default"].strip(), q["id"])
            self.assertTrue(q["changes"].strip(), q["id"])
        self.assertTrue((SK / PACK["appendix"]).is_file())

    def test_ids_cover_the_charter_topics(self):
        self.assertEqual([q["id"] for q in PACK["questions"]],
                         ["scenes", "characters", "genre", "visual_style", "atmosphere",
                          "audience", "message", "dialogue_language", "ending", "reference_policy"])

    def test_money_question_has_only_the_safe_default(self):
        ref = next(q for q in PACK["questions"] if q["id"] == "reference_policy")
        self.assertEqual(ref.get("sensitive"), "money")
        self.assertIn("برومنتات", ref["suggested_default"])
        self.assertIn("صفر صرف", ref["suggested_default"])

    def test_dialect_is_a_suggestion_not_a_rule(self):
        d = next(q for q in PACK["questions"] if q["id"] == "dialogue_language")["suggested_default"]
        self.assertIn("مصرية", d)
        self.assertIn("قابل للتغيير", d)

    def test_style_default_names_no_studio(self):
        blob = json.dumps(PACK["questions"], ensure_ascii=False)
        self.assertIsNone(re.search(r"pixar|disney|ghibli|بيكسار|ديزني|جيبلي|unreal|8k", blob, re.I))


class TestBriefQuestions(unittest.TestCase):
    def test_l1_story_gets_the_core_five_with_defaults(self):
        an = S.analyse("اكتب لي قصة رعب 3 مشاهد")
        self.assertEqual(an["level"], "L1")
        got = pack_qs(an)
        self.assertEqual([q["question"] for q in got], CORE)
        self.assertTrue(all(q["suggested_default"] for q in got))
        self.assertEqual(got[0]["suggested_default"], "3 مشاهد (من طلبك)")

    def test_l2_screenplay_gets_all_ten(self):
        an = S.analyse("اعمل سيناريو فيلم قصير عن الصداقة لطفلين في القرية مع حوار ونهاية")
        self.assertEqual(an["level"], "L2")
        self.assertEqual([q["question"] for q in pack_qs(an)], ALL)

    def test_l3_story_gets_all_ten(self):
        an = S.analyse("اكتب قصة بأقصى قوة")
        self.assertEqual(an["level"], "L3")
        self.assertEqual(len(pack_qs(an)), 10)

    def test_english_keywords(self):
        self.assertEqual(len(pack_qs(S.analyse("write a story about a cat"))), 5)
        self.assertEqual(len(pack_qs(S.analyse("storyboard for a 30 second ad video"))), 10)

    def test_l0_asks_nothing(self):
        an = S.analyse("ما هي القصة في فيلم X؟")
        self.assertEqual(an["level"], "L0")
        self.assertEqual(an["questions"], [])

    def test_no_pack_outside_story_requests(self):
        for req in ("write user stories for my app", "عايز قصة شعر جديدة", "اعمل فيديو موشن 9:16",
                    "ابني لي تطبيق ويب بسيط لمحاسبة محل صغير"):
            self.assertEqual(pack_qs(S.analyse(req)), [], req)

    def test_no_default_spends_or_publishes(self):
        an = S.analyse("اعمل سيناريو حلقة كرتون 6 مشاهد بشخصيات وحوار")
        for q in pack_qs(an):
            self.assertNotRegex(q["suggested_default"], r"اشحن|ادفع|انشر|ولّد الآن|spend|publish")

    def test_report_prints_pack_inside_the_one_report(self):
        b = S.build_brief("اكتب قصة مغامرة 4 مشاهد")
        txt = S.render(b)
        self.assertIn("كم عدد الشخصيات ومن هي؟ ← شخصيتان رئيسيتان", txt)
        self.assertEqual(len(pack_qs(b["analysis"])), 5)

    def test_missing_pack_file_fails_open_to_no_questions(self):
        old = S.QPACKS
        try:
            S.QPACKS = SK / "data" / "__no_such_pack__.json"
            self.assertEqual(pack_qs(S.analyse("اكتب لي قصة رعب 3 مشاهد")), [])
        finally:
            S.QPACKS = old


if __name__ == "__main__":
    unittest.main()
