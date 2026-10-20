"""check_skill.py --json --evals prints exactly one JSON document (report + routing evals).

The 12 skill checks are stubbed out so this stays fast; only the output shape is under test."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import check_skill  # noqa: E402


def stub_checks():
    """Patch every check_* function to a no-op and load_records to an empty list."""
    stack = contextlib.ExitStack()
    for name in dir(check_skill):
        if name.startswith("check_") and callable(getattr(check_skill, name)):
            stack.enter_context(mock.patch.object(check_skill, name, lambda *a, **k: None))
    stack.enter_context(mock.patch.object(check_skill, "load_records", lambda r: []))
    return stack


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = check_skill.main(argv)
    return rc, buf.getvalue()


class CheckSkillJsonTests(unittest.TestCase):
    def test_json_evals_is_one_document(self):
        ev = {"available": True, "cases": [], "ran": 3, "passed": 3, "skipped": 0,
              "pass_rate": 1.0, "min_pass": 0.8, "ok": True}
        with stub_checks(), mock.patch.object(check_skill, "routing_evals", return_value=ev):
            rc, out = run_main(["--json", "--evals"])
        doc = json.loads(out)          # raises on two documents back to back
        self.assertEqual(set(doc), {"ok", "report", "evals"})
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["evals"]["passed"], 3)
        self.assertIn("items", doc["report"])
        self.assertEqual(rc, 0)

    def test_failing_evals_fail_the_document(self):
        ev = {"available": True, "cases": [], "ran": 4, "passed": 1, "skipped": 0,
              "pass_rate": 0.25, "min_pass": 0.8, "ok": False}
        with stub_checks(), mock.patch.object(check_skill, "routing_evals", return_value=ev):
            rc, out = run_main(["--json", "--evals"])
        doc = json.loads(out)
        self.assertFalse(doc["ok"])
        self.assertTrue(doc["report"]["ok"])
        self.assertEqual(rc, 1)

    def test_missing_evals_file_stays_json(self):
        with tempfile.TemporaryDirectory() as td, stub_checks(), \
                mock.patch.object(check_skill, "SK", Path(td)):
            rc, out = run_main(["--json", "--evals"])
        doc = json.loads(out)          # no plain-text "skipped" line in JSON mode
        self.assertFalse(doc["evals"]["available"])
        self.assertIn("evals.json", doc["evals"]["reason"])
        self.assertEqual(rc, 0)

    def test_json_without_evals_keeps_report_shape(self):
        with stub_checks():
            rc, out = run_main(["--json"])
        doc = json.loads(out)
        self.assertEqual(set(doc), {"ok", "errors", "warnings", "checks", "items"})
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
