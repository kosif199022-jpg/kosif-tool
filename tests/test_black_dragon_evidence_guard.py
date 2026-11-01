"""Black Dragon v1.4: critical-path and independent post-run evidence audit."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
sys.path.insert(0, str(SCRIPTS))

import black_dragon as dragon
import _black_dragon_evidence_guard as guard
import _black_dragon_pro_max as pro


class EvidenceGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        patcher = patch.object(dragon, "REPO", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "worker.py").write_text(
            "import pathlib,sys\npathlib.Path(sys.argv[1]).write_text('verified evidence')\n",
            encoding="utf-8",
        )
        self.entries = {
            "tool:first": {"kind": "tool", "source": "one.json"},
            "tool:second": {"kind": "tool", "source": "two.json"},
        }
        self.adapters = {
            "tool:first": {"script": "scripts/worker.py", "args": ["{artifact}"]},
            "tool:second": {"script": "scripts/worker.py", "args": ["{artifact}"],
                            "depends_on": ["tool:first"]},
        }
        self.job = self.root / "out" / "dragon-job"

    def run_job(self, adapters=None):
        return dragon.run("audit and verify", self.job,
                          adapters if adapters is not None else self.adapters,
                          workers=2, allow_execution=bool(adapters or self.adapters),
                          timeout=10, entries=self.entries, mode="pro-max")

    def ledger(self):
        return json.loads((self.job / "all_skills_ledger.json").read_text(encoding="utf-8"))

    def save_ledger(self, ledger):
        (self.job / "all_skills_ledger.json").write_text(json.dumps(ledger, indent=2), encoding="utf-8")

    def test_critical_path_and_real_vetted_execution(self):
        report = self.run_job()
        self.assertEqual(report["execution_map"]["critical_path_length"], 2)
        self.assertEqual(report["execution_map"]["critical_path"],
                         ["tool:first", "tool:second"])
        self.assertEqual(report["execution_map"]["execution_adapter_ready"], 2)
        self.assertEqual(report["executed"], 2)
        self.assertTrue(report["pro_max"]["integrity_passed"])
        review = pro.review_job(self.job, self.entries)
        self.assertTrue(review["audit"]["integrity_passed"])
        self.assertTrue(review["audit"]["every_capability_executed"])
        self.assertFalse(review["audit"]["external_full_pro_verified"])

    def test_no_adapters_is_blocked_but_integrity_passes(self):
        report = dragon.run("plan only", self.job, {}, workers=2,
                            allow_execution=False, timeout=5,
                            entries=self.entries, mode="pro-max")
        self.assertEqual(report["blocked"], 2)
        self.assertTrue(report["pro_max"]["integrity_passed"])
        self.assertFalse(report["pro_max"]["every_capability_executed"])
        self.assertFalse(report["execution_map"]["execution_adapter_ready"])
        self.assertTrue(pro.review_job(self.job, self.entries)["audit"]["integrity_passed"])

    def test_receipt_tampering_detected_after_job(self):
        self.run_job()
        ledger = self.ledger()
        path = Path(ledger["items"]["tool:first"]["receipt"]["receipt_path"])
        obj = json.loads(path.read_text(encoding="utf-8"))
        obj["command"] = ["forged"]
        path.write_text(json.dumps(obj), encoding="utf-8")
        review = pro.review_job(self.job, self.entries)["audit"]
        self.assertFalse(review["integrity_passed"])
        self.assertTrue(any("receipt SHA-256" in i for i in review["issues"]))

    def test_modified_artifact_detected(self):
        self.run_job()
        ledger = self.ledger()
        file = Path(ledger["items"]["tool:first"]["receipt"]["artifact"])
        file.write_text("TAMPERED", encoding="utf-8")
        review = pro.review_job(self.job, self.entries)["audit"]
        self.assertFalse(review["integrity_passed"])
        self.assertTrue(any("artifact/digest" in i for i in review["issues"]))

    def test_external_artifact_and_symlink_rejected(self):
        self.run_job()
        ledger = self.ledger()
        proof = ledger["items"]["tool:first"]["receipt"]
        receipt_path = Path(proof["receipt_path"])
        orig = json.loads(receipt_path.read_text(encoding="utf-8"))
        foreign = self.root / "outside.txt"
        foreign.write_text("fake")
        orig["artifact"] = str(foreign)
        receipt_path.write_text(json.dumps(orig), encoding="utf-8")
        proof["receipt_sha256"] = dragon.audit.sha256(receipt_path)
        self.save_ledger(ledger)
        result = pro.review_job(self.job, self.entries)["audit"]
        self.assertFalse(result["integrity_passed"])
        self.assertTrue(any("outside" in i for i in result["issues"]))

    def test_forged_empty_reason_or_attempts_rejected(self):
        dragon.run("plan only", self.job, {}, workers=2,
                   allow_execution=False, timeout=5,
                   entries=self.entries, mode="pro-max")
        ledger = self.ledger()
        ledger["items"]["tool:first"]["reason"] = ""
        ledger["items"]["tool:second"]["attempts"] = 4
        self.save_ledger(ledger)
        audit_result = pro.review_job(self.job, self.entries)["audit"]
        self.assertFalse(audit_result["integrity_passed"])
        self.assertTrue(any("without reason" in i for i in audit_result["issues"]))
        self.assertTrue(any("attempts" in i for i in audit_result["issues"]))

    def test_modified_assignment_brief_rejected(self):
        self.run_job()
        briefs = self.job / "briefs.jsonl"
        lines = briefs.read_text(encoding="utf-8").splitlines()
        obj = json.loads(lines[0])
        obj["application"] = "tampered"
        lines[0] = json.dumps(obj, ensure_ascii=False, sort_keys=True)
        briefs.write_text("\n".join(lines) + "\n", encoding="utf-8")
        result = pro.review_job(self.job, self.entries)["audit"]
        self.assertFalse(result["integrity_passed"])
        self.assertTrue(any("assignment" in i for i in result["issues"]))

    def test_cli_verify_is_read_only_for_execution(self):
        self.run_job()
        with patch.object(dragon, "full_inventory", return_value=self.entries):
            with contextlib.redirect_stdout(io.StringIO()) as out:
                rc = dragon.main(["verify", "--job", str(self.job)])
            self.assertEqual(rc, 0, out.getvalue())
            self.assertIn('"integrity_passed": true', out.getvalue())
        self.assertEqual(len(list((self.job / "artifacts").iterdir())), 2)

    def test_dependency_map_rejects_missing_and_wrong_order(self):
        fake = {"items": {"a": {"depends_on": []},
                          "b": {"depends_on": ["a"]}},
                "waves": [["b"], ["a"]]}
        with self.assertRaisesRegex(ValueError, "topologically"):
            guard.execution_map(fake)
        fake["waves"] = [["a"]]
        with self.assertRaisesRegex(ValueError, "omitted"):
            guard.execution_map(fake)


if __name__ == "__main__":
    unittest.main()
