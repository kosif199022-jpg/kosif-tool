"""Link audit: every catalog capability owns a real SKILL.md, with honest specialist hints."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
sys.path.insert(0, str(SCRIPTS))
import _black_dragon_skill_links as skill_links
import black_dragon as dragon


class SkillLinkAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.skill = self.repo / ".claude" / "skills" / "kosif-superpowers"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("# Canonical KOSIF Superpowers")
        specialised = self.skill.parent / "cinematic-video-editing"
        specialised.mkdir()
        (specialised / "SKILL.md").write_text("# Cinematic Video Editing")
        (self.skill / "data" / "powers").mkdir(parents=True)
        (self.skill / "data" / "powers" / "video.json").write_text("[]")
        (self.skill / "data" / "tools.json").write_text('{"tools":[]}')
        self.inventory = {
            "skill:kosif-superpowers": {"kind": "skill", "source": "kosif-superpowers/SKILL.md"},
            "skill:cinematic-video-editing": {"kind": "skill", "source": "cinematic-video-editing/SKILL.md"},
            "power:VIDEO-001": {"kind": "power", "source": "data/powers/video.json"},
            "tool:edit": {"kind": "tool", "source": "data/tools.json"},
        }

    def audit(self, entries=None, desc=None):
        return skill_links.build(entries or self.inventory, self.skill, self.repo, desc)

    def test_every_capability_has_real_owner_and_installed_skills_have_self_links(self):
        r = self.audit()
        self.assertEqual(r["summary"]["catalog_total"], 4)
        self.assertEqual(r["summary"]["canonical_owner_linked"], 4)
        self.assertEqual(r["summary"]["installed_skills"], 2)
        self.assertTrue(r["summary"]["all_owned"])
        self.assertTrue(r["summary"]["all_sources_present"])
        self.assertEqual(r["links"]["skill:cinematic-video-editing"]["skill_links"],
                         ["skill:kosif-superpowers", "skill:cinematic-video-editing"])

    def test_specialist_hints_are_not_claimed_as_verified(self):
        r = self.audit(desc={"power:VIDEO-001": "cinematic video editing"})
        hints = r["links"]["power:VIDEO-001"]["specialist_candidates"]
        self.assertEqual(hints[0]["skill"], "skill:cinematic-video-editing")
        self.assertEqual(hints[0]["status"], "suggested_not_verified")
        self.assertFalse(r["summary"]["all_specialist_links_proven"])

    def test_description_signal_requires_an_independent_name_match(self):
        specialised = self.skill.parent / "cinematic-video-editing" / "SKILL.md"
        specialised.write_text("---\nname: cinematic-video-editing\n"
                               "description: >-\n  Detailed color grading timelines and sound mixing\n"
                               "---\n# Cinematic Video Editing\n", encoding="utf-8")
        hit = self.audit(desc={"power:VIDEO-001": "cinematic sound mixing"})
        candidates = hit["links"]["power:VIDEO-001"]["specialist_candidates"]
        self.assertEqual(candidates[0]["skill"], "skill:cinematic-video-editing")
        self.assertGreaterEqual(candidates[0]["matching_description_terms"], 1)
        self.assertEqual(candidates[0]["status"], "suggested_not_verified")
        # The same word in the slug and the frontmatter cannot count twice.
        alternate = {**self.inventory, "power:OTHER-001": {"kind": "power", "source": "data/powers/video.json"}}
        weak = self.audit(entries=alternate, desc={"power:OTHER-001": "cinematic"})
        self.assertEqual(weak["links"]["power:OTHER-001"]["specialist_candidates"], [])

    def test_bare_description_cannot_fabricate_specialist_link(self):
        specialised = self.skill.parent / "cinematic-video-editing" / "SKILL.md"
        specialised.write_text("---\ndescription: editing filters tools and timelines\n---\n", encoding="utf-8")
        alternate = {**self.inventory, "power:OTHER-001": {"kind": "power", "source": "data/powers/video.json"}}
        r = self.audit(entries=alternate, desc={"power:OTHER-001": "filters color and timelines"})
        self.assertEqual(r["links"]["power:OTHER-001"]["specialist_candidates"], [])

    def test_missing_source_is_reported_not_silently_linked_as_working(self):
        (self.skill / "data" / "tools.json").unlink()
        r = self.audit()
        self.assertTrue(r["summary"]["all_owned"])
        self.assertFalse(r["summary"]["all_sources_present"])
        self.assertIn("tool:edit", r["summary"]["missing_source_examples"])
        self.assertFalse(r["links"]["tool:edit"]["source_exists"])

    def test_untrusted_source_traversal_is_refused(self):
        inventory = {**self.inventory,
                     "tool:edit": {"kind": "tool", "source": "../credentials.txt"}}
        r = self.audit(inventory)
        self.assertEqual(r["summary"]["missing_sources"], 1)
        self.assertFalse(r["links"]["tool:edit"]["source_exists"])

    def test_no_canonical_installed_skill_fails_closed(self):
        inventory = {k: v for k, v in self.inventory.items()
                     if k != "skill:kosif-superpowers"}
        with self.assertRaisesRegex(ValueError, "canonical"):
            self.audit(inventory)

    def test_deterministic_digest_and_complete_identity_keys(self):
        a = self.audit()
        b = self.audit(dict(reversed(list(self.inventory.items()))))
        self.assertEqual(a["sha256"], b["sha256"])
        self.assertEqual(set(a["links"]), set(self.inventory))


class RealSkillLinkInventoryTest(unittest.TestCase):
    def test_all_installed_capabilities_map_to_real_skills(self):
        inventory = dragon.full_inventory()
        report = skill_links.build(inventory, dragon.audit.SKILL, ROOT,
                                   dragon.brain.metadata(inventory, dragon.audit.SKILL))
        summary = report["summary"]
        self.assertEqual(summary["catalog_total"], len(inventory))
        self.assertEqual(summary["canonical_owner_linked"], len(inventory))
        self.assertEqual(summary["installed_skills"],
                         sum(meta["kind"] == "skill" for meta in inventory.values()))
        self.assertEqual(summary["orphan_links"], 0)
        self.assertEqual(summary["missing_sources"], 0,
                         "Fix catalog paths instead of marking missing sources as connected")
        self.assertFalse(summary["all_specialist_links_proven"])


if __name__ == "__main__":
    unittest.main()
