"""Power programs of the code group: atlas-code, code-engineering, api-testing and security-safety.

Every registered program runs through the real dispatcher (`run_program`) in its own temp dir and must
pass all of its known-answer checks. The card catalog must equal programmed + skipped, with a reason for
every skip. Planted-failure tests then break one core helper per case (a realistic bug: a regex that
never matches, a verifier that accepts everything, a formula off by one term) and require the program
that depends on it to fail. That proves the checks measure the technique instead of restating constants.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _black_dragon_power_program as dispatcher  # noqa: E402
import power_programs as pp  # noqa: E402
from power_programs import api_testing as api  # noqa: E402
from power_programs import atlas_code as atlas  # noqa: E402
from power_programs import code_engineering as code  # noqa: E402
from power_programs import security_safety as sec  # noqa: E402

FAMILIES = ["atlas-code", "code-engineering", "api-testing", "security-safety"]
IDS = sorted(pid for fam in FAMILIES for m in pp.modules_for(fam, local=False) for pid in m.PROGRAMS)
SKIPPED = ROOT / ".claude" / "skills" / "kosif-superpowers" / "data" / "power_program_records" / "code-skipped.json"
NEVER = re.compile(r"(?!x)x")


def run(pid):
    with tempfile.TemporaryDirectory() as tmp:
        res = dispatcher.run_program(pid, Path(tmp) / "work")
    return pid, res.get("ok"), [c["name"] for c in res.get("checks", []) if not c["passed"]], (res.get("error") or "")[-400:]


def failed_checks(pid):
    _, ok, failed, err = run(pid)
    return ok, failed, err


class AllProgramsPass(unittest.TestCase):
    def test_every_program_passes_through_the_dispatcher(self):
        self.assertGreater(len(IDS), 300)
        with ProcessPoolExecutor(min(8, os.cpu_count() or 2)) as ex:
            results = list(ex.map(run, IDS))
        bad = [(pid, failed, err) for pid, ok, failed, err in results if not ok]
        self.assertEqual(bad, [])

    def test_catalog_equals_programmed_plus_skipped(self):
        skipped = json.loads(SKIPPED.read_text(encoding="utf-8"))
        cards = {pid for pid, (fam, _) in pp.card_index().items() if fam in FAMILIES}
        self.assertEqual(set(IDS) & set(skipped), set())
        self.assertEqual(cards, set(IDS) | set(skipped))
        self.assertTrue(all(isinstance(v, str) and ":" in v for v in skipped.values()))


class PlantedFailuresAtlasCode(unittest.TestCase):
    def test_wrong_crc16_breaks_redis_slot_card(self):
        with mock.patch.object(atlas, "_crc16_xmodem", lambda data: sum(data) & 0xFFFF):
            ok, failed, _ = failed_checks("ACODE-91")
        self.assertFalse(ok, failed)

    def test_jwt_check_that_accepts_everything_fails(self):
        with mock.patch.object(atlas, "_jwt_check", lambda tok, key, now, aud=None, iss=None: ({"sub": "x"}, "ok")):
            ok, failed, _ = failed_checks("ACODE-30")
        self.assertFalse(ok, failed)

    def test_reversed_rrf_breaks_hybrid_rag(self):
        with mock.patch.object(atlas, "_rrf", lambda rankings, k=60: list(reversed(rankings[0]))):
            ok, failed, _ = failed_checks("ACODE-163")
        self.assertFalse(ok, failed)

    def test_redaction_that_does_nothing_fails(self):
        with mock.patch.object(atlas, "_redact", lambda text: text):
            ok, failed, _ = failed_checks("ACODE-49")
        self.assertFalse(ok, failed)

    def test_backoff_without_exponent_fails_rate_limit_card(self):
        with mock.patch.object(atlas, "_backoff", lambda attempt, base, cap, rng, jitter=1.0: base):
            ok, failed, _ = failed_checks("ACODE-160")
        self.assertFalse(ok, failed)
        self.assertTrue(any("backoff" in n for n in failed), failed)

    def test_secret_regex_that_never_matches_fails_history_audit(self):
        with mock.patch.object(atlas, "SECRET_RE", NEVER):
            ok, failed, _ = failed_checks("ACODE-264")
        self.assertFalse(ok, failed)


class PlantedFailuresCodeEngineering(unittest.TestCase):
    def test_blind_secret_regex_fails_commit_hygiene(self):
        with mock.patch.object(code, "SECRET_RE", NEVER):
            ok, failed, _ = failed_checks("CODE-22")
        self.assertFalse(ok, failed)

    def test_blind_debug_regex_fails_commit_hygiene(self):
        with mock.patch.object(code, "DEBUG_RE", NEVER):
            ok, failed, _ = failed_checks("CODE-22")
        self.assertFalse(ok, failed)

    def test_timer_that_reports_a_constant_fails_optimisation_loop(self):
        with mock.patch.object(code, "_timeit", lambda fn: 1.0):
            ok, failed, _ = failed_checks("CODE-14")
        self.assertFalse(ok, failed)


class PlantedFailuresSecuritySafety(unittest.TestCase):
    def test_blind_secret_regex_fails_leak_scan(self):
        with mock.patch.object(sec, "CARD_SECRET_RE", NEVER):
            ok, failed, _ = failed_checks("SEC-06")
        self.assertFalse(ok, failed)

    def test_blind_injection_regex_fails_untrusted_data_card(self):
        with mock.patch.object(sec, "INJECTION_RE", NEVER):
            ok, failed, _ = failed_checks("SEC-01")
        self.assertFalse(ok, failed)

    def test_url_check_that_allows_everything_fails(self):
        with mock.patch.object(sec, "_url_ok", lambda url, resolver: True):
            ok, failed, _ = failed_checks("SEC-03")
        self.assertFalse(ok, failed)

    def test_command_segmenter_that_never_splits_fails_prefix_rules(self):
        with mock.patch.object(sec, "segment", lambda cmd: [cmd]):
            ok, failed, _ = failed_checks("SEC-21")
        self.assertFalse(ok, failed)


class PlantedFailuresApiTesting(unittest.TestCase):
    def test_parser_that_returns_nothing_fails_bru_card(self):
        with mock.patch.object(api, "parse_bru", lambda text: {}):
            ok, failed, err = failed_checks("API-22")
        self.assertFalse(ok, (failed, err))

    def test_jwt_signer_with_wrong_key_fails_script_libraries(self):
        orig = api.jwt_sign
        with mock.patch.object(api, "jwt_sign", lambda payload, secret, header=None: orig(payload, secret + "x", header)):
            ok, failed, err = failed_checks("API-20")
        self.assertFalse(ok, (failed, err))

    def test_dumper_that_drops_blocks_fails_wsdl_import(self):
        with mock.patch.object(api, "dump_bru", lambda blocks: ""):
            ok, failed, err = failed_checks("API-17")
        self.assertFalse(ok, (failed, err))


if __name__ == "__main__":
    unittest.main()
