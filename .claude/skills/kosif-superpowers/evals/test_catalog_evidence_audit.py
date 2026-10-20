"""Bounded, non-executing tests for full KOSIF capability evidence audit."""
import json
from pathlib import Path
import subprocess
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
        # The family count changes as the catalog grows: derive it from the
        # family files instead of hard-coding a number.
        families = sorted((SK / "data" / "powers").glob("*.json"))
        self.assertEqual(result["families_examined"], len(families))
        self.assertEqual(result["record_integrity_errors"], [])
        self.assertFalse(result["executes_external_code"])
        self.assertFalse(result["downloads"])

    def test_reference_directory_and_line(self):
        repo = SK.parents[2]
        self.assertTrue(audit.local_ref("kosif-tool/.claude/skills/kosif-superpowers/scripts/powers.py:6", repo))
        self.assertTrue(audit.local_ref("kosif-tool/.claude/skills/kosif-superpowers", repo))

    def test_reference_line_range_and_column(self):
        repo = SK.parents[2]
        base = "kosif-tool/.claude/skills/kosif-superpowers/scripts/powers.py"
        self.assertTrue(audit.local_ref(base + ":15-16", repo))
        self.assertTrue(audit.local_ref(base + ":6:2", repo))
        self.assertFalse(audit.local_ref(base + "-missing.py:15-16", repo))

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

    def test_cli_missing_catalog_is_clean_error(self):
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [sys.executable, str(SK / "scripts" / "catalog_evidence_audit.py"), "--skill", td],
                capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("powers catalog absent", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertEqual(proc.stdout, "")


if __name__ == "__main__":
    unittest.main()
