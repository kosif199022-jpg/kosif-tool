"""Tests for the differential hidden-exam scorer; temp folders only, nothing is executed."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import differential_exam as exam


def write(root, rel, content):
    path = Path(root) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")


class DifferentialExamTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_pair(self, ref_files, cand_files):
        for rel, body in ref_files.items():
            write(self.root / "ref", rel, body)
        for rel, body in cand_files.items():
            write(self.root / "cand", rel, body)
        rules = exam.build_rules(None, [str(self.root)])
        return exam.score(str(self.root / "ref"), str(self.root / "cand"), rules, {"id"})

    def test_volatile_values_are_masked(self):
        ref = {"s1/request.json": {"id": "a", "model": "m", "at": "2026-10-23T09:00:00Z",
                                   "trace": "123e4567-e89b-12d3-a456-426614174000"},
               "s1/stdout.txt": "done in 12 ms\n"}
        cand = {"s1/request.json": {"trace": "00000000-1111-2222-3333-444444444444", "model": "m",
                                    "at": "2027-01-01T00:00:00.5Z", "id": "b"},
                "s1/stdout.txt": "done in 900 ms\n"}
        report = self.run_pair(ref, cand)
        self.assertEqual((report["ok"], report["total"], report["percent"]), (2, 2, 100.0))

    def test_real_difference_is_reported(self):
        report = self.run_pair({"s1/request.json": {"tools": ["a", "b"]}},
                               {"s1/request.json": {"tools": ["a"]}})
        self.assertEqual(report["ok"], 0)
        self.assertIn("length", report["scenarios"][0]["checks"][0]["why"])

    def test_missing_and_extra_files_count_as_failures(self):
        report = self.run_pair({"s1/a.txt": "x", "s2/b.txt": "y"}, {"s1/a.txt": "x", "s1/extra.txt": "z"})
        self.assertEqual(report["ok"], 1)
        self.assertEqual(report["total"], 3)
        whys = [c.get("why", "") for s in report["scenarios"] for c in s["checks"]]
        self.assertIn("scenario missing in candidate", whys)
        self.assertIn("extra file only in candidate", whys)

    def test_jsonl_events_compared_as_data(self):
        report = self.run_pair({"s1/events.jsonl": '{"type":"turn.started","b":1}\n{"type":"done"}\n'},
                               {"s1/events.jsonl": '{"b":1,"type":"turn.started"}\n\n{"type":"done"}\n'})
        self.assertEqual(report["percent"], 100.0)

    def test_self_check_flags_untrusted_scorer(self):
        write(self.root / "r1", "s1/out.txt", "run 7f3a")
        write(self.root / "r2", "s1/out.txt", "run 91bc")
        self.assertEqual(exam.main(["self-check", str(self.root / "r1"), str(self.root / "r2")]), 1)
        self.assertEqual(exam.main(["self-check", str(self.root / "r1"), str(self.root / "r2"),
                                    "--rule", r"run [0-9a-f]{4}=>run <RUN>"]), 0)
        self.assertEqual(exam.main(["self-check", str(self.root / "r1")]), 0)

    def test_compare_min_threshold_exit_code(self):
        write(self.root / "ref", "s1/a.txt", "x")
        write(self.root / "cand", "s1/a.txt", "y")
        self.assertEqual(exam.main(["compare", str(self.root / "ref"), str(self.root / "cand")]), 0)
        self.assertEqual(exam.main(["compare", str(self.root / "ref"), str(self.root / "cand"), "--min", "50"]), 1)

    def test_seal_detects_edits_after_sealing(self):
        write(self.root / "exam", "scenarios/s1.json", {"prompt": "say hi"})
        seal = str(self.root / "seal.json")
        self.assertEqual(exam.main(["seal", str(self.root / "exam"), "--out", seal]), 0)
        self.assertEqual(exam.main(["verify-seal", str(self.root / "exam"), seal]), 0)
        write(self.root / "exam", "scenarios/s1.json", {"prompt": "say hello"})
        self.assertEqual(exam.main(["verify-seal", str(self.root / "exam"), seal]), 1)

    def test_seal_refuses_output_inside_exam(self):
        write(self.root / "exam", "a.txt", "x")
        with self.assertRaises(SystemExit):
            exam.main(["seal", str(self.root / "exam"), "--out", str(self.root / "exam" / "seal.json")])

    def test_no_default_masks(self):
        rules = exam.build_rules(None, None, defaults=False)
        self.assertEqual(exam.norm_text("2026-10-23T09:00:00Z", rules), "2026-10-23T09:00:00Z")


if __name__ == "__main__":
    unittest.main()
