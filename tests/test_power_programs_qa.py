"""QA group power programs (qa-verification, verification-evals).

1) Every program passes through _black_dragon_power_program.run_program in a temp dir (4 threads;
   the programs spend most of their time in ffmpeg subprocesses).
2) Planted failures: breaking a module's core technique makes that card's known-answer check fail.
3) Programmed + skipped cover every card of both families, with no overlap.
"""
from __future__ import annotations

import importlib
import json
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import power_programs as pp  # noqa: E402
import _black_dragon_power_program as bd  # noqa: E402

MODULES = ["qa_verification", "verification_evals"]
_CARDS = pp.card_index()


def run(pid):
    with tempfile.TemporaryDirectory() as d:
        return bd.run_program(pid, Path(d) / "work")


def mod(name):
    return importlib.import_module(f"power_programs.{name}")


def failed_checks(pid):
    r = run(pid)
    return r["ok"], [c["name"] for c in r.get("checks", []) if not c["passed"]], r.get("problems", [])


class AllProgramsPass(unittest.TestCase):
    def test_every_program_passes(self):
        pids = []
        for m in MODULES:
            for pid in mod(m).PROGRAMS:
                self.assertIn(pid, _CARDS, pid)
                self.assertEqual(_CARDS[pid][0].replace("-", "_"), m, pid)
                pids.append(pid)
        with mock.patch.object(pp, "card_index", lambda: _CARDS), ThreadPoolExecutor(4) as ex:
            results = dict(zip(pids, ex.map(run, pids)))
        bad = {pid: r.get("problems") for pid, r in results.items() if not r["ok"]}
        self.assertEqual(bad, {})
        self.assertGreaterEqual(len(pids), 318)

    def test_skipped_and_programmed_cover_every_card(self):
        skipped = json.loads((ROOT / "out" / "power-programs" / "qa-skipped.json").read_text())
        fams = {m.replace("_", "-") for m in MODULES}
        cards = {pid for pid, (f, _) in _CARDS.items() if f in fams}
        programmed = {pid for m in MODULES for pid in mod(m).PROGRAMS}
        self.assertEqual(programmed & set(skipped), set())
        self.assertEqual(cards, programmed | set(skipped))
        self.assertTrue(all(isinstance(v, str) and v for v in skipped.values()))


class PlantedFailuresQA(unittest.TestCase):
    q = mod("qa_verification")

    def test_broken_contrast_fails_wcag_floor_card(self):
        with mock.patch.object(self.q, "contrast", lambda a, b: 1.0):
            ok, failed, _ = failed_checks("QA-275")
        self.assertFalse(ok)
        self.assertTrue(any("767676" in n for n in failed), failed)

    def test_broken_loudness_meter_fails_loudness_gate(self):
        with mock.patch.object(self.q, "ebur128", lambda p: {"I": -30.0, "LRA": 0.0, "TP": -20.0}):
            ok, failed, _ = failed_checks("QA-256")
        self.assertFalse(ok)
        self.assertTrue(any("-14 LUFS" in n for n in failed), failed)

    def test_blind_frame_scanner_fails_planted_defect_card(self):
        empty = {"outlier": [], "jump": [], "freeze": [], "dead_air_s": 0.0, "timing": [], "median_mad": 0.0}
        with mock.patch.object(self.q, "frame_scan", lambda *a, **k: empty):
            ok, failed, _ = failed_checks("QA-X01")
        self.assertFalse(ok)
        self.assertEqual(len(failed), 5, failed)

    def test_broken_wilson_interval_fails(self):
        with mock.patch.object(self.q, "wilson", lambda x, n, z=1.96: (0.0, 1.0)):
            ok, failed, _ = failed_checks("QA-283")
        self.assertFalse(ok)
        self.assertTrue(any("Wilson" in n for n in failed), failed)

    def test_receipt_validator_that_accepts_everything_fails(self):
        with mock.patch.object(self.q, "validate_receipt", lambda r: (0, [])):
            ok, failed, _ = failed_checks("QA-P01")
        self.assertFalse(ok)
        self.assertGreaterEqual(len(failed), 2, failed)


class PlantedFailuresEvals(unittest.TestCase):
    v = mod("verification_evals")

    def test_wrong_pass_at_k_formula_fails(self):
        with mock.patch.object(self.v, "pass_at_k", lambda p, k: p):
            ok, failed, _ = failed_checks("CHECK-12")
        self.assertFalse(ok)
        self.assertTrue(any("pass@2 0.91" in n for n in failed), failed)

    def test_record_gate_that_never_fails_is_caught_by_mutations(self):
        with mock.patch.object(self.v, "record_gate", lambda sk, home: (0, 0, [])):
            ok, failed, _ = failed_checks("CHECK-23")
        self.assertFalse(ok)
        self.assertTrue(any("10/10" in n for n in failed), failed)

    def test_weak_secret_regex_in_strong_slot_is_caught(self):
        with mock.patch.object(self.v, "STRONG_SECRET", self.v.WEAK_SECRET):
            ok, failed, _ = failed_checks("CHECK-20")
        self.assertFalse(ok)
        self.assertTrue(any("10/10" in n for n in failed), failed)

    def test_receipt_check_that_trusts_untyped_evidence_fails(self):
        with mock.patch.object(self.v, "validate_receipt", lambda r: (0, [])), mock.patch.object(self.v, "typed_receipt", lambda r: (0, [])):
            ok, failed, _ = failed_checks("CHECK-09")
        self.assertFalse(ok)
        self.assertTrue(any("error can never be verified" in n for n in failed), failed)

    def test_classifier_that_knows_nothing_fails(self):
        with mock.patch.object(self.v, "classify_failure", lambda m: ("UNCLASSIFIED", "")):
            ok, failed, _ = failed_checks("CHECK-27")
        self.assertFalse(ok)
        self.assertTrue(any("MISSING_DEP" in n for n in failed), failed)


if __name__ == "__main__":
    unittest.main()
