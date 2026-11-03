"""Power programs of the 'data' group: atlas-data, data-analysis, atlas-build, atlas-docs,
documents-office, atlas-craft, other.

Every program must pass its known-answer checks, and planted breakages of the techniques
(monkeypatched core functions) must make the matching check fail.
"""
from __future__ import annotations

import hashlib
import sys
import tempfile
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _black_dragon_power_program as runner  # noqa: E402
import power_programs as pp  # noqa: E402
from power_programs import (atlas_build, atlas_craft, atlas_data, atlas_docs, data_analysis,  # noqa: E402
                            documents_office, other)

MODULES = {"atlas-data": atlas_data, "data-analysis": data_analysis, "atlas-build": atlas_build, "atlas-docs": atlas_docs,
           "documents-office": documents_office, "atlas-craft": atlas_craft, "other": other}


def run(pid):
    with tempfile.TemporaryDirectory() as tmp:
        return runner.run_program(pid, Path(tmp) / "w")


class Patch:
    """Minimal monkeypatch: set attributes for the duration of a with-block."""

    def __init__(self, *triples):
        self.triples, self.saved = triples, []

    def __enter__(self):
        for obj, name, val in self.triples:
            self.saved.append((obj, name, getattr(obj, name)))
            setattr(obj, name, val)

    def __exit__(self, *exc):
        for obj, name, val in reversed(self.saved):
            setattr(obj, name, val)


class AllProgramsPass(unittest.TestCase):
    def test_every_program_passes_and_belongs_to_its_family(self):
        cards = pp.card_index()
        failures = []
        total = 0
        for fam, mod in MODULES.items():
            self.assertTrue(mod.PROGRAMS, fam)
            for pid in mod.PROGRAMS:
                total += 1
                self.assertEqual(cards[pid][0], fam, pid)
                r = run(pid)
                if not r.get("ok"):
                    failures.append((pid, r.get("problems"), r.get("error", "")[-300:]))
                else:
                    self.assertTrue(r["outputs"] and r["checks"], pid)
        self.assertEqual(failures, [])
        self.assertGreaterEqual(total, 200)


class PlantedFailures(unittest.TestCase):
    def assertBroken(self, pid, check_fragment):
        r = run(pid)
        self.assertFalse(r["ok"], pid)
        failed = [c["name"] for c in r["checks"] if not c["passed"]]
        self.assertTrue(any(check_fragment in n for n in failed) or (not r["checks"] and r["error"]), (pid, failed, r.get("error", "")[-200:]))

    # atlas-data
    def test_atlas_data_iban_checker_broken(self):
        with Patch((atlas_data, "_iban_ok", lambda s: True)):
            self.assertBroken("ADATA-08", "one-digit-off IBAN")

    def test_atlas_data_holm_broken(self):
        with Patch((atlas_data, "_holm", lambda p, alpha=0.05: [x < alpha for x in p])):
            self.assertBroken("ADATA-19", "Holm rejects only")

    def test_atlas_data_wilson_broken(self):
        with Patch((atlas_data, "_wilson", lambda x, n, z=1.96: (x / n, x / n))):
            self.assertBroken("ADATA-27", "Wilson CI")

    def test_atlas_data_sample_size_broken(self):
        with Patch((atlas_data, "_n_two_prop", lambda *a, **k: 1000)):
            self.assertBroken("ADATA-14", "3841")

    # data-analysis
    def test_data_analysis_contrast_broken(self):
        with Patch((data_analysis, "_contrast", lambda a, b: 4.0)):
            self.assertBroken("ANLY-12", "21:1")

    def test_data_analysis_row_loss_detected(self):
        orig = data_analysis._sales
        with Patch((data_analysis, "_sales", lambda seed=7: orig(seed)[:-1])):
            self.assertBroken("ANLY-01", "180 rows")

    def test_data_analysis_derivative_broken(self):
        with Patch((data_analysis._Poly, "diff", lambda self: data_analysis._Poly([0, 1]))):
            self.assertBroken("ANLY-06", "optimal price")

    # atlas-build
    def test_atlas_build_histogram_quantile_broken(self):
        with Patch((atlas_build, "_histogram_quantile", lambda q, b: b[-2][0])):
            self.assertBroken("ABUILD-29", "histogram_quantile(0.95)")

    def test_atlas_build_pixel_diff_broken(self):
        with Patch((atlas_build, "_diff", lambda a, d, de_tol=3.0, region=0.005, mask=None: {"pass": True, "bad_fraction": 0.0, "max_dE": 0.0})):
            self.assertBroken("ABUILD-46", "4 px shift")

    def test_atlas_build_token_resolution_broken(self):
        def no_cycle_check(tokens):
            flat, val = orig(tokens)
            return flat, (lambda name, stack=(): "x")
        orig = atlas_build._resolve_tokens
        with Patch((atlas_build, "_resolve_tokens", no_cycle_check)):
            self.assertBroken("ABUILD-37", "alias resolves")

    def test_atlas_build_a11y_scan_broken(self):
        with Patch((atlas_build, "_a11y_scan", lambda html: [])):
            self.assertBroken("ABUILD-31", "div role=button")

    # atlas-docs
    def test_atlas_docs_abn_broken(self):
        with Patch((atlas_docs, "_abn_ok", lambda s: bool(s))):
            self.assertBroken("ADOCS-04", "one-digit-off ABN")

    def test_atlas_docs_readability_broken(self):
        with Patch((atlas_docs, "_fk_grade", lambda t: 14.0)):
            self.assertBroken("ADOCS-06", "8th grade")

    def test_atlas_docs_contrast_broken(self):
        with Patch((atlas_docs, "_contrast_hex", lambda a, b: 1.5)):
            self.assertBroken("ADOCS-23", ">= 3:1")

    # documents-office
    def test_documents_office_normaliser_broken(self):
        with Patch((documents_office, "_clean_extracted", lambda s: s)):
            self.assertBroken("DOC-14", "recovers the known phrase")

    def test_documents_office_nfkc_broken(self):
        fake = types.SimpleNamespace(normalize=lambda form, s: s)
        with Patch((documents_office, "unicodedata", fake)):
            self.assertBroken("DOC-15", "lam-alef-aware")

    def test_documents_office_bidi_reorder_broken(self):
        import bidi.algorithm
        with Patch((bidi.algorithm, "get_display", lambda s, *a, **k: s)):
            self.assertBroken("DOC-23", "doing both reverses")

    # atlas-craft
    def test_atlas_craft_contrast_broken(self):
        with Patch((atlas_craft, "_contrast", lambda a, b: 2.0)):
            self.assertBroken("ACRAFT-17", "#767676")

    def test_atlas_craft_cvd_simulation_broken(self):
        import numpy as np
        with Patch((atlas_craft, "_DEUTAN", np.eye(3))):
            self.assertBroken("ACRAFT-02", "deuteranopia")

    def test_atlas_craft_ramp_contrast_broken(self):
        with Patch((atlas_craft, "_contrast", lambda a, b: 3.0)):
            self.assertBroken("ACRAFT-16", "700 text on the 50 tint")

    # other
    def test_other_safe_name_regex_broken(self):
        import re
        with Patch((other, "_SAFE", re.compile(r".*"))):
            self.assertBroken("MISC-13", "regex accepts")

    def test_other_base64_broken(self):
        fake = types.SimpleNamespace(b64encode=lambda b: b.hex().encode())
        with Patch((other, "base64", fake)):
            self.assertBroken("MISC-X01", "Base64")

    def test_other_hash_ids_broken(self):
        fake = types.SimpleNamespace(sha256=hashlib.md5)
        with Patch((other, "hashlib", fake)):
            self.assertBroken("MISC-14", "sha256 64-hex")


if __name__ == "__main__":
    unittest.main()
