"""Synthetic and repository-grounded checks for the flexible creative council."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/kosif-black-dragon/scripts/creative_council.py"
SPEC = importlib.util.spec_from_file_location("dragon_creative_council", SCRIPT)
council = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(council)


class CreativeCouncilTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.put(council.DRAGON, {"frameworks": [
            {"id": "first-principles", "family": "frame", "name_ar": "فهم المعنى"},
            {"id": "scamper", "family": "diverge", "name_ar": "التفكير الجانبي"},
            {"id": "pre-mortem", "family": "risk", "name_ar": "توقع الإخفاق"},
        ]})
        self.put(council.MODELS, [
            {"id": "MODEL-01", "discipline": "reasoning", "name_ar": "التفكير بالمبادئ"},
            {"id": "MODEL-02", "discipline": "people", "name_ar": "فهم المشاهد"},
        ])
        self.put(council.POWERS, [
            {"id": "THINK-01", "section": "حلقة التفكير — Thinking Loop", "status": "documented"},
            {"id": "THINK-34", "section": "الأنماط المضادة — Anti-patterns", "status": "documented"},
        ])

    def put(self, name, data):
        dest = self.root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_twelve_seats_without_rights_role_or_orphaned_skills(self):
        records = council.inventory(self.root)
        self.assertEqual(len(council.SEATS), 12)
        self.assertNotIn("rights", council.SEATS)
        self.assertEqual(len(records), 7)
        self.assertEqual(len({r["id"] for r in records}), len(records))
        self.assertTrue(all(r["primary"] in council.SEATS for r in records))
        self.assertEqual(next(r for r in records if r["id"] == "framework:pre-mortem")["primary"], "critic")
        self.assertEqual(next(r for r in records if r["id"] == "model:MODEL-02")["primary"], "audience")
        self.assertEqual(next(r for r in records if r["id"] == "power:THINK-01")["primary"], "chair")

    def test_plan_flexible_routes_and_optional_discussion(self):
        report = council.plan("صمّم فيديو حزين", self.root, options=["hybrid"])
        self.assertEqual(report["primary_assigned"], 7)
        self.assertEqual(len(report["roles"]), 12)
        self.assertEqual(report["status"], "PLANNED_NOT_DEBATED")
        self.assertNotIn("rights_gate", report)
        self.assertEqual(report["options"], ["hybrid"])
        self.assertEqual(report["source_counts"], {"framework": 3, "model": 2, "power": 2})
        self.assertEqual(report["fingerprint"], council.plan("صمّم فيديو حزين", self.root, options=["hybrid"])["fingerprint"])

    def test_same_title_records_share_one_focus_with_both_sources(self):
        self.put(council.DRAGON, {"frameworks": [
            {"id": "inversion", "family": "frame", "name_en": "Inversion"},
            {"id": "scamper", "family": "diverge", "name_en": "SCAMPER"}]})
        self.put(council.MODELS, [
            {"id": "MODEL-01", "discipline": "reasoning", "name_en": "Inversion"}])
        draft = council.plan("Inversion of a cinematic story", self.root)
        self.assertEqual(draft["repeated_title_group_count"], 1)
        self.assertEqual(draft["repeated_title_groups"]["inversion"],
                         ["framework:inversion", "model:MODEL-01"])
        analyst = next(x for x in draft["roles"] if x["id"] == "analyst")
        methods = [x for x in analyst["focus"] if x["title_key"] == "inversion"]
        self.assertEqual(len(methods), 1)
        self.assertEqual(set(methods[0]["source_ids"]),
                         {"framework:inversion", "model:MODEL-01"})
        self.assertEqual(draft["primary_assigned"], len(council.inventory(self.root)))

    def test_one_round_is_advisory_not_falsely_debated(self):
        report = council.plan("مونتاج", self.root)
        outcome = council.verdict(report, {"rounds": {"1": {
            "creative": {"proposal": "Use images and kinetic type"}
        }}})
        self.assertEqual(outcome["status"], "ADVISORY_INCOMPLETE_NOT_EXECUTED")
        self.assertEqual(outcome["participating_seats"], ["creative"])
        self.assertIsNone(outcome["winning_route"])
        self.assertFalse(outcome["evidence_attested_by_caller"])

    def test_optional_score_with_partial_criteria_and_no_veto(self):
        report = council.plan("فيديو", self.root, options=["footage", "hybrid"])
        outcome = council.verdict(report, {"mode": "UNVERIFIED", "rounds": {"3": {
            "creative": {"scores": {"footage": {"meaning": 2}, "hybrid": {"drama": 5}},
                         "remaining_objection": "Needs reference footage"},
        }}})
        self.assertEqual(outcome["winning_route"], "hybrid")
        self.assertIn("creative", outcome["dissent"])
        self.assertNotIn("rights_vetoed", outcome)
        self.assertEqual(outcome["status"], "ADVISORY_INCOMPLETE_NOT_EXECUTED")

    def test_independence_claim_without_receipt_rejected(self):
        report = council.plan("فيديو", self.root)
        with self.assertRaisesRegex(ValueError, "real run IDs"):
            council.verdict(report, {"mode": "INDEPENDENT", "rounds": {
                "1": {"analyst": {"proposal": "A"}}
            }})

    def test_invalid_foreign_persona_rejected(self):
        report = council.plan("فيديو", self.root)
        with self.assertRaisesRegex(ValueError, "unrecognized council member"):
            council.verdict(report, {"rounds": {"1": {"rights": {"proposal": "veto"}}}})

    def test_extra_sources_are_read_with_no_omitted_role(self):
        self.put(council.EXTRA_POWER_FILES["creativity-engine"],
                 [{"id": x, "name_en": x, "status": "documented"} for x in council.CREATIVITY_ROLE])
        self.put(council.BOOK_METHODS, {"methods": [
            {"id": "TB01-1", "stage": "forecast", "name_en": "Forecast"}, 
            {"id": "TB02-1", "stage": "verify", "name_en": "Verify"}]})
        self.put(council.REASONING_MODES, {"modes": [
            {"id": k, "en": k} for k in council.MODE_ROLE]})
        rows = council.inventory(self.root)
        self.assertEqual(len(rows), 7 + len(council.CREATIVITY_ROLE) + 2 + len(council.MODE_ROLE))
        self.assertEqual({x["primary"] for x in rows if x["id"].startswith("reasoning-mode:")},
                         {"analyst", "research", "creative", "systems"})
        self.assertTrue(all(x["primary"] in council.SEATS for x in rows))

    def test_optional_personas_are_roles_not_ghost_agents(self):
        self.put(council.PERSONA_FILE, {"personas": [
            {"id": "P001", "lane": "cross_domain", "title_ar": "مخرجة بصرية"},
            {"id": "P002", "lane": "audience", "title_ar": "ممثل الجمهور"},
            {"id": "P003", "lane": "guardrails", "title_ar": "ناقد إجراءات"},
        ]})
        report = council.plan("فيديو بصري", self.root)
        specialists = report["optional_specialists"]
        self.assertEqual(specialists["profile_count"], 3)
        self.assertEqual(specialists["assigned"], 3)
        self.assertEqual(specialists["by_role"]["visual"], 1)
        self.assertEqual(specialists["by_role"]["audience"], 1)
        self.assertEqual(specialists["by_role"]["critic"], 1)
        self.assertNotIn("rights", specialists["by_role"])
        self.assertTrue(all(row["profile_not_agent"] for entries in specialists["suggested"].values()
                            for row in entries))

    def test_extra_family_change_fails_closed(self):
        self.put(council.EXTRA_POWER_FILES["creativity-engine"],
                 [{"id": "IDEA-01", "name_en": "Only first one"}])
        with self.assertRaisesRegex(ValueError, "unreviewed thinking IDs"):
            council.inventory(self.root)

    def test_atlas_mind_82_contextual_methods_mapped_without_new_seats(self):
        self.put(council.ATLAS_MIND, [
            {"id": f"AMIND-{n:02d}", "name_en": f"Example thinking skill {n}",
             "section": "سير عمل الوكلاء — Agent workflows & orchestration",
             "status": "documented"} for n in range(1, 83)
        ])
        records = council.inventory(self.root)
        atlas = [x for x in records if x["id"].startswith("atlas-mind:")]
        self.assertEqual(len(atlas), 82)
        self.assertEqual(len({x["id"] for x in atlas}), 82)
        self.assertTrue(all(x["contextual_only"] for x in atlas))
        self.assertTrue(all(x["primary"] in council.SEATS for x in atlas))
        result = council.plan("فيديو", self.root)
        self.assertEqual(result["core_cognitive_records"], 7)
        self.assertEqual(result["atlas_mind_contextual_records"], 82)
        self.assertEqual(result["total_source_records"], 89)

    def test_real_repository_has_no_unassigned_entries(self):
        original = council.inventory(ROOT)
        framework = json.loads((ROOT / council.DRAGON).read_text(encoding="utf-8"))["frameworks"]
        models = json.loads((ROOT / council.MODELS).read_text(encoding="utf-8"))
        powers = json.loads((ROOT / council.POWERS).read_text(encoding="utf-8"))
        extras = sum(len(json.loads((ROOT / x).read_text(encoding="utf-8")))
                     for x in council.EXTRA_POWER_FILES.values())
        books = json.loads((ROOT / council.BOOK_METHODS).read_text(encoding="utf-8"))["methods"]
        modes = json.loads((ROOT / council.REASONING_MODES).read_text(encoding="utf-8"))["modes"]
        core = len(framework) + len(models) + len(powers) + extras + len(books) + len(modes)
        atlas = json.loads((ROOT / council.ATLAS_MIND).read_text(encoding="utf-8"))
        self.assertEqual(core, 443)  # 404 prior records + 39 book-derived framework operators
        self.assertEqual(len(atlas), 106)  # 82 originals + 24 from the 2026-11-07 core-work pass
        expected = core + len(atlas)
        self.assertEqual(expected, 549)
        self.assertEqual(len(original), expected)
        self.assertEqual(sum(x["id"].startswith("framework:tfs-") for x in original), 39)
        gate_report = council.kahneman_review("احسب خطة إطلاق المنتج من آخر سعر", ROOT)
        self.assertEqual(gate_report["book_frameworks"], 42)  # 39 new plus three existing methods updated
        self.assertEqual(gate_report["traps_catalogued"], 31)
        self.assertEqual(gate_report["book_page_count"], 468)
        self.assertTrue(gate_report["review_gates"])
        self.assertTrue(all(x["source_id"].startswith("framework:tfs-") for x in gate_report["review_gates"]))
        self.assertTrue(all(x["primary"] in council.SEATS and "critic" in x["reviewers"] for x in gate_report["review_gates"]))
        combined = council.plan("احسب خطة إطلاق المنتج من آخر سعر", ROOT)
        self.assertEqual(combined["total_source_records"], 549)
        self.assertEqual(sum(s["primary_count"] for s in combined["roles"]), 549)
        self.assertEqual(combined["kahneman_review"]["book_frameworks"], 42)
        self.assertEqual(sum(len(s["kahneman_review_questions"]) for s in combined["roles"]),
                         sum(len(x["reviewers"]) for x in combined["kahneman_review"]["review_gates"]))
        self.assertEqual(len({x["id"] for x in original}), expected)
        self.assertEqual(set(x["primary"] for x in original), set(council.SEATS))
        self.assertTrue(all(x["source"] for x in original))
        self.assertEqual(len(json.loads((ROOT / council.MODEL_POWER_MIRROR).read_text(encoding="utf-8"))),
                         len(models))


if __name__ == "__main__":
    unittest.main()
