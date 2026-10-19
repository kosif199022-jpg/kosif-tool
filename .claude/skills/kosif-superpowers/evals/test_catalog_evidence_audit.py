"""Bounded, non-executing tests for full KOSIF capability evidence audit."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import catalog_evidence_audit as audit


class EvidenceAuditTests(unittest.TestCase):
    def test_catalog_all_records_unique(self):
        result = audit.audit(SK)
        self.assertGreaterEqual(result["records_examined"], 4730)
        self.assertEqual(result["unique_ids"], result["records_examined"])
        self.assertEqual(result["families_examined"], 52)
        self.assertEqual(result["record_integrity_errors"], [])
        self.assertFalse(result["executes_external_code"])
        self.assertFalse(result["downloads"])

    def test_reference_directory_and_line(self):
        repo = SK.parents[2]
        self.assertTrue(audit.local_ref("kosif-tool/.claude/skills/kosif-superpowers/scripts/powers.py:6", repo))
        self.assertTrue(audit.local_ref("kosif-tool/.claude/skills/kosif-superpowers", repo))

    def test_cannot_escape_repo(self):
        repo = SK.parents[2]
        self.assertFalse(audit.local_ref("kosif-tool/../secrets.txt", repo))
        self.assertFalse(audit.local_ref("kosif-tool/../../windows/system.ini", repo))

    def test_external_source_remains_unverified(self):
        self.assertIsNone(audit.local_ref("https://github.com/some/project", SK.parents[2]))
        self.assertIsNone(audit.local_ref("kosif-atlas/skills/example", SK.parents[2]))

    def test_empty_fixture_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                audit.audit(Path(td))


if __name__ == "__main__":
    unittest.main()
