"""atlas_audit_synthesis.py: metadata-only manifest from audit records, and REA results in UTF-16 or UTF-8.

Proposed by the first self-council pass (docs/self-council/FIRST_PASS_20261024.md): the script had no test, and REA
files that were not UTF-16 were silently dropped."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "atlas_audit_synthesis.py"


def rea(n):
    return {"evidence_id": f"E{n}", "normalized_result": {"statistics": {"parsed_javascript_files": n, "visited_ast_nodes": 10 * n,
                                                                         "findings": 1, "parse_failures": 0}}}


class AtlasAuditSynthesisTests(unittest.TestCase):
    def test_manifest_and_both_rea_encodings(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            records = [
                {"skill_id": 7, "skill_name": "demo", "status": "FETCHED", "kind": "skill", "sha256": "a" * 64,
                 "path": "skills/demo/SKILL.md", "details": {"indicators": {"secrets": 1}}},
                {"skill_id": 7, "skill_name": "demo", "status": "FETCHED", "kind": "code", "sha256": "b" * 64, "path": "x.js"},
                {"skill_id": 9, "skill_name": "other", "status": "SKIPPED"},
            ]
            (t / "records.json").write_text(json.dumps(records), encoding="utf-8")
            (t / "rea").mkdir()
            (t / "rea" / "rea_7.json").write_text(json.dumps(rea(2)), encoding="utf-16")   # as REA writes on Windows
            (t / "rea" / "rea_9.json").write_text(json.dumps(rea(3)), encoding="utf-8")    # was silently dropped before
            (t / "rea" / "rea_bad.json").write_text("not json", encoding="utf-8")         # still skipped, never fatal
            r = subprocess.run([sys.executable, str(SCRIPT), "--records", str(t / "records.json"), "--rea-dir", str(t / "rea"),
                                "--manifest-out", str(t / "out" / "manifest.json"), "--report-out", str(t / "out" / "report.md")],
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr[-400:])
            summary = json.loads(r.stdout)
            self.assertEqual((summary["bodies"], summary["code"], summary["rea"], summary["rea_files"]), (1, 1, 2, 5))
            m = json.loads((t / "out" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(m["records"], 2)
            demo = next(s for s in m["skills"] if s["id"] == 7)
            self.assertEqual((demo["status"], demo["content_indicators"], demo["code_files_read"]), ("SKILL_MD_READ_STATIC", ["secrets"], 1))
            self.assertTrue(all(s["runtime_verified"] is False and s["auto_install_allowed"] is False for s in m["skills"]))
            self.assertEqual(sorted(x["skill_id"] for x in m["rea_static_analyses"]), ["7", "9"])
            self.assertTrue((t / "out" / "report.md").read_text(encoding="utf-8").startswith("# KOSIF Atlas source audit"))


if __name__ == "__main__":
    unittest.main()
