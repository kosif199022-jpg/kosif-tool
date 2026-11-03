"""Fast synthetic tests for the new independent Black Dragon source linker."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / ".claude/skills/kosif-black-dragon/scripts/black_dragon.py"
SPEC = importlib.util.spec_from_file_location("native_black_dragon", PROGRAM)
native = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(native)


class NativeFusionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / ".claude/skills/kosif-superpowers"
        self.skill.mkdir(parents=True)
        self.write(".claude/skills/example/SKILL.md", "---\ndescription: image editing\n---\n# Draw\n## Render\n")
        self.write(".claude/skills/kosif-black-dragon/SKILL.md", "# Self must not be in its own sources\n")
        self.write(".claude/skills/kosif-superpowers/data/powers/one.json", json.dumps([{
            "id": "BEAT-001", "name_ar": "مونتاج الإيقاع", "name_en": "Beat montage",
            "what": "Align animation to the beat", "how": "Find beats and edit video",
            "family": "music-beat", "requires": ["ffmpeg"], "tags": ["music", "video"]
        }]))
        self.write(".claude/skills/kosif-superpowers/scripts/real.py", "print('do not execute')\n")
        self.write(".claude/skills/kosif-superpowers/data/tools.json", json.dumps({"tools": [{
            "id": "rhythm", "root": "skill", "path": "scripts/real.py",
            "title_en": "Beat detector", "summary_en": "Detect audio beats",
            "area": "audio"
        }]}))
        self.write(".claude/skills/kosif-superpowers/data/superpowers.json",
                   json.dumps({"items": [{"id": "SP-001", "name_en": "Motion producer",
                                           "pipeline": [{"id": "BEAT-001"}]}]}))
        self.write("catalog/styles.json", json.dumps([{"id": "neon", "name": "Neon", "category": ["glow"]}]))
        self.write("playbooks/video.md", "# Editing\n## Verify the output\n")
        self.write(".claude/skills/kosif-superpowers/PROTOCOL.md", "# Operating protocol\n")

    def write(self, rel, content):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_all_kinds_are_linked_and_self_is_excluded(self):
        rows = native.inventory(self.root)
        self.assertEqual(len(rows), 7, rows.keys())
        self.assertEqual({x.split(":", 1)[0] for x in rows},
                         {"skill", "power", "tool", "superpower", "style", "playbook", "protocol"})
        self.assertNotIn("skill:kosif-black-dragon", rows)
        self.assertEqual(rows["tool:rhythm"]["code"]["inspection"], "bytes-fingerprinted-not-executed")
        self.assertEqual(rows["power:BEAT-001"]["coverage"]["native_implemented"], False)

    def test_build_verify_and_compose_without_legacy_execution(self):
        out = self.root / "out/report"
        summary = native.build(self.root, out)
        self.assertEqual(summary["total_source_linked"], 7)
        self.assertEqual(summary["native_implemented"], 0)
        self.assertTrue(native.verify(self.root, out)["integrity_passed"])
        plan = native.compose("Beat montage video", out / "sources.jsonl")
        self.assertEqual(plan["status"], "native-thinking-blueprint-not-execution")
        self.assertEqual(plan["legacy_compatibility"], "disabled")
        self.assertTrue(plan["selected"])
        self.assertNotIn("legacy_entry", plan["selected"][0])
        opt_in = native.compose("Beat montage", out / "sources.jsonl", legacy=True)
        self.assertEqual(opt_in["selected"][0]["legacy_entry"], opt_in["selected"][0]["id"])

    def test_native_dragon_mind_has_six_stages_and_faculties(self):
        out = self.root / "out/brain"
        native.build(self.root, out)
        plan = native.compose("Beat montage video", out / "sources.jsonl")
        mind = plan["native_mind"]
        self.assertEqual(mind["engine"], "black-dragon-independent-native-mind")
        self.assertFalse(mind["runtime_legacy_imports"])
        self.assertEqual(len(native.native_reasoner().FACULTIES), 26)
        self.assertEqual([p["stage"] for p in mind["cognitive_cycle"]],
                         ["frame", "explore", "decide", "build", "verify", "learn"])
        self.assertTrue(mind["provenance_preserved"])
        self.assertTrue(mind["typed_handoffs"])
        self.assertIn("execution-not-proven", [x["kind"] for x in mind["critic"]])
        self.assertEqual(plan, native.compose("Beat montage video", out / "sources.jsonl"))

    def test_native_mind_reconciles_duplicates_without_losing_unique_rules(self):
        mind = native.native_reasoner()
        inputs = [
            {"id": "power:first", "kind": "power", "title": "Beat music mix",
             "purpose": "Align beats", "method": "Find beats; Preserve original audio"},
            {"id": "power:second", "kind": "power", "title": "Beat music mix",
             "purpose": "Align beats", "method": "Find beats; Never normalize the source"},
        ]
        synthesis = mind.fuse("Edit audio to a beat", inputs, 7393)
        self.assertTrue(synthesis["provenance_preserved"])
        self.assertEqual(synthesis["method_fusion"]["source_fragments"], 4)
        self.assertEqual(synthesis["method_fusion"]["distinct_fragments"], 3)
        self.assertEqual(synthesis["method_fusion"]["deduplicated_exact_fragments"], 1)
        used = [m for f in synthesis["faculties"] for m in f["merged_methods"]]
        self.assertEqual(len([m for m in used if m["method"] == "Find beats"]), 1)
        self.assertEqual(len(next(m for m in used if m["method"] == "Find beats")["source_ids"]), 2)
        self.assertIn("Never normalize the source", [m["method"] for m in used])
        self.assertEqual(synthesis["catalog_total"], 7393)
        self.assertEqual(synthesis["selected_source_count"], 2)

    def test_catalog_wide_fusion_covers_every_source_and_uses_no_old_executor(self):
        out = self.root / "out/full-atlas"
        summary = native.build(self.root, out)
        atlas = native.read_json(out / "fusion_atlas.json")
        sources = native.load_index(out / "sources.jsonl")
        self.assertEqual(summary["fused_source_count"], len(sources))
        self.assertEqual(atlas["selected_source_count"], len(sources))
        self.assertTrue(atlas["provenance_preserved"])
        self.assertFalse(atlas["runtime_legacy_imports"])
        self.assertEqual({row["source_id"] for row in atlas["affiliation"]},
                         {row["id"] for row in sources})
        self.assertTrue(native.verify(self.root, out)["fusion_atlas_integrity_passed"])
        response = native.compose("Beat montage video", out / "sources.jsonl")
        self.assertEqual(response["catalog_wide_fusion"]["source_count"], len(sources))
        self.assertEqual(summary["native_implemented"], 0)

    def test_catalog_fusion_preserves_full_document_and_every_method(self):
        long_document = "# Full source\\n" + "\\n".join(
            "Preserve rule number %d" % n for n in range(40))
        self.write(".claude/skills/example/SKILL.md", long_document)
        rows = native.inventory(self.root)
        self.assertIn("Preserve rule number 39", rows["skill:example"]["method"])
        mind = native.native_reasoner().fuse("Preserve all rules",
                                             [rows["skill:example"]], len(rows))
        methods = [m["method"] for faculty in mind["faculties"]
                   for m in faculty["merged_methods"]]
        self.assertIn("Preserve rule number 39", methods)

    def test_detect_fusion_atlas_tampering(self):
        out = self.root / "out/tamper-atlas"
        native.build(self.root, out)
        atlas_path = out / "fusion_atlas.json"
        atlas = native.read_json(atlas_path)
        atlas["selected_source_count"] = 0
        atlas_path.write_text(json.dumps(atlas, ensure_ascii=False), encoding="utf-8")
        self.assertFalse(native.verify(self.root, out)["fusion_atlas_integrity_passed"])
        self.assertFalse(native.verify(self.root, out)["integrity_passed"])

    def test_detect_source_tampering_and_duplicate(self):
        out = self.root / "out/report"
        native.build(self.root, out)
        self.write("playbooks/video.md", "# Changed playbook\n")
        self.assertFalse(native.verify(self.root, out)["integrity_passed"])
        self.write(".claude/skills/kosif-superpowers/data/powers/dupe.json",
                   json.dumps([{"id": "BEAT-001"}]))
        with self.assertRaisesRegex(ValueError, "duplicate source ID"):
            native.inventory(self.root)

    def test_refuse_unsafe_code_reference(self):
        x = native._safe_code(self.root, self.skill, "../../../../../outside.py")
        self.assertEqual(x["inspection"], "refused-unsafe-path")


if __name__ == "__main__":
    unittest.main()
