"""USIP v6.0 layer (appendix A43): receipt validator, capability registry and the Living Site static gate."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "kosif-superpowers"
VALIDATOR = SKILL / "scripts" / "validate_receipt.py"
CHECK = ROOT / ".claude" / "skills" / "living-site" / "check.py"

spec = importlib.util.spec_from_file_location("usip_validate_receipt", VALIDATOR)
receipts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receipts)

GOOD = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>@media (prefers-reduced-motion: reduce){*{animation:none}}</style></head><body>
<section data-xray="رحلة الطلب" data-xray-tool="code">حركة</section>
<p>KOSIF علامة خيالية للعرض.</p>
<script>window.__ready = true; const io = new IntersectionObserver(() => {});</script></body></html>"""


class ReceiptTest(unittest.TestCase):
    def test_verified_needs_file_and_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / "out.md").write_text("x", encoding="utf-8")
            r = {"version": "USIP-6.0", "status": "VERIFIED", "artifact": "out.md",
                 "checks": [{"name": "exists", "result": "PASS", "evidence": "sha256:abc"}], "remote_deployment": False}
            self.assertEqual(receipts.validate(r, base), [])
            r["checks"][0]["evidence"] = ""
            self.assertTrue(receipts.validate(r, base))

    def test_verified_rejects_missing_file_and_unrun_checks(self):
        with tempfile.TemporaryDirectory() as d:
            r = {"version": "USIP-6.0", "status": "VERIFIED", "artifact": "no.md",
                 "checks": [{"name": "browser", "result": "NOT_RUN"}]}
            errors = receipts.validate(r, Path(d))
            self.assertTrue(any("artifact" in e.lower() for e in errors))
            self.assertTrue(any("unrun" in e for e in errors))

    def test_partial_may_list_unrun_checks(self):
        with tempfile.TemporaryDirectory() as d:
            r = {"version": "USIP-6.0", "status": "PARTIAL", "artifact": "later.md",
                 "checks": [{"name": "browser", "result": "NOT_RUN"}]}
            self.assertEqual(receipts.validate(r, Path(d)), [])

    def test_remote_claim_needs_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            r = {"version": "USIP-6.0", "status": "PARTIAL", "artifact": "x", "checks": [], "remote_deployment": True}
            self.assertIn("remote_deployment=true requires remote_evidence", receipts.validate(r, Path(d)))

    def test_countdown_minutes(self):
        with tempfile.TemporaryDirectory() as d:
            r = {"version": "USIP-6.0", "status": "PARTIAL", "artifact": "x", "checks": [],
                 "estimate_minutes": 15, "actual_minutes": 22.5}
            self.assertEqual(receipts.validate(r, Path(d)), [])
            r["actual_minutes"] = -1
            self.assertTrue(any("actual_minutes" in e for e in receipts.validate(r, Path(d))))
            r["actual_minutes"] = "soon"
            self.assertTrue(any("actual_minutes" in e for e in receipts.validate(r, Path(d))))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "receipt.json"
            p.write_text(json.dumps({"version": "USIP-6.0", "status": "BLOCKED", "artifact": "x", "checks": []}), encoding="utf-8")
            self.assertEqual(subprocess.run([sys.executable, str(VALIDATOR), str(p)], capture_output=True).returncode, 0)
            p.write_text(json.dumps({"version": "5.9", "status": "DONE", "artifact": "", "checks": []}), encoding="utf-8")
            self.assertEqual(subprocess.run([sys.executable, str(VALIDATOR), str(p)], capture_output=True).returncode, 1)


class RegistryTest(unittest.TestCase):
    def test_registry_matches_record_schema_basics(self):
        reg = json.loads((SKILL / "data" / "usip_capability_registry_v60.json").read_text(encoding="utf-8"))
        schema = json.loads((SKILL / "schemas" / "usip_capability_record.v1.json").read_text(encoding="utf-8"))
        props = schema["properties"]
        for rec in reg["capabilities"]:
            for key in schema["required"]:
                self.assertIn(key, rec, rec.get("id"))
            self.assertIn(rec["kind"], props["kind"]["enum"])
            self.assertIn(rec["status_here"], props["status_here"]["enum"])
            self.assertIn(rec["evidence"]["level"], props["evidence"]["properties"]["level"]["enum"])
            if rec["status_here"] in ("TESTED", "READY"):
                self.assertTrue(rec["evidence"]["tests"], f"{rec['id']} claims {rec['status_here']} without a test")
            art = rec["source"]["artifact"]
            self.assertTrue((ROOT / art).exists() or (SKILL / art).exists(), f"{rec['id']}: {art} missing")


class LivingSiteCheckTest(unittest.TestCase):
    def run_check(self, html, *args):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "index.html"
            p.write_text(html, encoding="utf-8")
            return subprocess.run([sys.executable, str(CHECK), str(p), *args], capture_output=True, text=True)

    def test_code_level_by_name_and_number(self):
        for lv in ("code", "3"):
            proc = self.run_check(GOOD, "--levels", lv)
            self.assertEqual(proc.returncode, 0, proc.stdout)
            self.assertIn("skip  L1", proc.stdout)

    def test_json_output(self):
        proc = self.run_check(GOOD, "--levels", "code", "--json")
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "PASS")
        self.assertTrue(data["static_only"])
        self.assertEqual(data["levels"], [3])

    def test_3d_and_film_need_their_layer(self):
        self.assertEqual(self.run_check(GOOD, "--levels", "3d").returncode, 1)
        self.assertEqual(self.run_check(GOOD, "--levels", "film").returncode, 1)
        self.assertEqual(self.run_check(GOOD, "--levels", "all").returncode, 1)

    def test_warnings_fail_only_when_strict(self):
        bare = GOOD.replace(' lang="ar" dir="rtl"', "")
        self.assertEqual(self.run_check(bare, "--levels", "code").returncode, 0)
        self.assertEqual(self.run_check(bare, "--levels", "code", "--strict").returncode, 1)

    def test_unknown_level_is_usage_error(self):
        self.assertEqual(self.run_check(GOOD, "--levels", "bogus").returncode, 2)

    def test_missing_asset_fails(self):
        proc = self.run_check(GOOD.replace("<body>", '<body><img alt="" src="img/nope.png">'), "--levels", "code")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("every local asset exists", proc.stdout)


if __name__ == "__main__":
    unittest.main()
