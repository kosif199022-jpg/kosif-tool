"""Synthetic tests for the strict one-attempt-per-skill cinema coverage contract."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / ".claude/skills/kosif-superpowers/scripts/cinema_all_skills.py"
spec = importlib.util.spec_from_file_location("cinema_all_skills", MODULE)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.skill = root / ".claude/skills/kosif-superpowers"
        (self.skill / "data/powers").mkdir(parents=True)
        (self.skill / "data/powers/basic.json").write_text(
            json.dumps([{"id": "P-A"}, {"id": "P-B"}]))
        (self.skill / "data/tools.json").write_text(
            json.dumps({"tools": [{"id": "one"}]}))
        (self.skill / "SKILL.md").write_text("Skill content")
        self.job = root / "out/test"
        self.entries = c.catalog(self.skill)

    def tearDown(self):
        self.temp.cleanup()

    def receipt(self, key):
        artifact = self.job / (key.replace(":", "-") + ".mp4")
        artifact.write_bytes(b"real-output-bytes")
        receipt = self.job / (key.replace(":", "-") + ".json")
        receipt.write_text(json.dumps({
            "entry": key, "exit_code": 0, "command": ["python3", "test.py"],
            "artifact": str(artifact), "artifact_sha256": c.sha256(artifact),
        }))
        return receipt

    def test_inventories_every_type_and_defaults_to_unexecuted(self):
        self.assertEqual(len(self.entries), 4)
        self.assertEqual(set(k.split(":")[0] for k in self.entries),
                         {"skill", "power", "tool"})
        c.init(self.job, self.entries)
        result = c.report(self.job, self.entries)
        self.assertEqual(result["not_executed"], 4)
        self.assertFalse(result["fully_executed"])

    def test_receipt_required_and_each_entry_exactly_once(self):
        c.init(self.job, self.entries)
        key = next(iter(self.entries))
        with self.assertRaises(ValueError):
            c.record(self.job, self.entries, key, "executed", None, "")
        c.record(self.job, self.entries, key, "executed", self.receipt(key), "")
        with self.assertRaises(ValueError):
            c.record(self.job, self.entries, key, "executed", self.receipt(key), "")
        self.assertFalse(c.report(self.job, self.entries)["fully_executed"])

    def test_all_receipts_prove_coverage_until_artifact_changed(self):
        c.init(self.job, self.entries)
        for key in self.entries:
            c.record(self.job, self.entries, key, "executed", self.receipt(key), "")
        self.assertTrue(c.report(self.job, self.entries)["fully_executed"])
        (self.job / (next(iter(self.entries)).replace(":", "-") + ".mp4")).write_bytes(b"tamper")
        result = c.report(self.job, self.entries)
        self.assertFalse(result["fully_executed"])
        self.assertEqual(len(result["invalid_evidence"]), 1)

    def test_blockers_do_not_count_as_execution(self):
        c.init(self.job, self.entries)
        key = next(iter(self.entries))
        c.record(self.job, self.entries, key, "blocked", None, "Requires API credits")
        self.assertEqual(c.report(self.job, self.entries)["blocked"], 1)

    def test_catalog_change_invalidates_coverage(self):
        c.init(self.job, self.entries)
        changed = {**self.entries, "power:NEW": {"kind": "power", "source": "x"}}
        with self.assertRaises(ValueError):
            c.load(self.job, changed)

    def test_unrecognized_power_format_cannot_be_silently_skipped(self):
        (self.skill / "data/powers/basic.json").write_text('{"unknown": []}')
        with self.assertRaises(ValueError):
            c.catalog(self.skill)


if __name__ == "__main__":
    unittest.main()
