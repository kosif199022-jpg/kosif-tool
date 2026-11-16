"""Animation Principles (Dylan Tarre, MIT) vendored into Superpowers: files, licence, index and routing."""
import json
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import animation_principles as AP  # noqa: E402
import hub  # noqa: E402


class AnimationPrinciples(unittest.TestCase):
    def test_licence_and_attribution_kept(self):
        lic = (AP.VENDOR / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", lic)
        self.assertIn("Dylan Tarre", lic)
        man = json.loads(AP.MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(man["upstream"], "https://github.com/dylantarre/animation-principles")
        self.assertEqual(len(man["upstream_commit"]), 40)
        notices = (SK.parents[2] / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        self.assertIn("dylantarre/animation-principles", notices)

    def test_every_file_matches_its_hash(self):
        self.assertEqual(AP.cmd_verify(None), 0)

    def test_index_has_all_144_skills(self):
        recs = AP.load()
        self.assertEqual(len(recs), 144)
        self.assertEqual(len({r["slug"] for r in recs}), 144)
        self.assertEqual(len({r["category"] for r in recs}), 12)
        for r in recs:
            self.assertTrue((SK / r["path"] / "SKILL.md").is_file(), r["slug"])
            self.assertTrue(r["description"], r["slug"])

    def test_find_in_arabic_and_english(self):
        self.assertEqual(AP.find("حركة زرار لما الماوس يقف عليه")[0][1]["slug"], "hover-interactions")
        self.assertEqual(AP.find("framer motion react")[0][1]["slug"], "framer-motion")
        self.assertEqual(AP.find("الانيميشن بيعمل دوخة للناس")[0][1]["slug"], "motion-sickness")

    def test_front_door_lists_them(self):
        res = hub.find("hover animation for a button", 5, 5, hub.load_registry())
        slugs = [k["slug"] for k in res["animation_principles"]]
        self.assertIn("hover-interactions", slugs)


if __name__ == "__main__":
    unittest.main()
