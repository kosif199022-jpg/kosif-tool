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
