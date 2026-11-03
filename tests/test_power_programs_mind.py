"""Mind group power programs (atlas-strategy, atlas-mind, mental-models, thinking-core, self-discovery,
creativity-engine, strategy-finance, planning-execution, story-direction-ideas).

1) Every program passes through _black_dragon_power_program.run_program in a temp dir.
2) Planted failures: breaking a module's core technique makes that card's known-answer check fail.
"""
from __future__ import annotations

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import power_programs as pp  # noqa: E402
import _black_dragon_power_program as bd  # noqa: E402

MODULES = ["atlas_strategy", "atlas_mind", "mental_models", "thinking_core", "self_discovery", "creativity_engine",
           "strategy_finance", "planning_execution", "story_direction_ideas"]
_CARDS = pp.card_index()


def run(pid):
    with tempfile.TemporaryDirectory() as d, mock.patch.object(pp, "card_index", lambda: _CARDS):
        return bd.run_program(pid, Path(d) / "work")


def mod(name):
    return importlib.import_module(f"power_programs.{name}")


class AllProgramsPass(unittest.TestCase):
    def test_every_program_passes(self):
        bad = {}
        total = 0
        for m in MODULES:
            for pid in mod(m).PROGRAMS:
                total += 1
                self.assertIn(pid, _CARDS, pid)
                self.assertEqual(_CARDS[pid][0].replace("-", "_"), m, pid)
                r = run(pid)
                if not r["ok"]:
                    bad[pid] = r["problems"]
        self.assertEqual(bad, {})
        self.assertGreaterEqual(total, 450)

    def test_skipped_and_programmed_cover_every_card(self):
        skipped = json.loads((ROOT / "out" / "power-programs" / "mind-skipped.json").read_text())
        fams = {m.replace("_", "-") for m in MODULES}
        cards = {pid for pid, (f, _) in _CARDS.items() if f in fams}
        programmed = {pid for m in MODULES for pid in mod(m).PROGRAMS}
        self.assertEqual(programmed & set(skipped), set())
        self.assertEqual(cards, programmed | set(skipped))


class PlantedFailures(unittest.TestCase):
    def broken(self, module, attr, fake, pid, check=None):
        with mock.patch.object(mod(module), attr, fake):
            r = run(pid)
        self.assertFalse(r["ok"], f"{pid} still passed with {attr} broken")
        if check:
            self.assertIn(f"check failed: {check}", r["problems"])

    # mental-models
    def test_mm_critical_path(self):
        self.broken("mental_models", "critical_path", lambda d, p: (10, ["A", "B", "D", "E"], {}, {"B": 0, "C": 0}), "MODEL-26", "critical path")

    def test_mm_bayes_ignores_base_rate(self):
        self.broken("mental_models", "bayes", lambda pr, a, b: a, "MODEL-08", "posterior")

    def test_mm_first_principles_keeps_conventions(self):
        self.broken("mental_models", "first_principles", lambda a: a, "MODEL-01", "conventions struck")

    def test_mm_occam_wrong_order(self):
        self.broken("mental_models", "occam", lambda c: sorted(c, key=lambda x: -len(x["assumptions"])), "MODEL-06", "test simplest first")

    # planning-execution
    def test_plan_critical_path(self):
        self.broken("planning_execution", "critical_path", lambda d, p: (9, ["script", "voice", "edit", "deliver"], {}, {"music": 0, "voice": 0}), "PLAN-04")

    def test_plan_wbs_misses_violations(self):
        self.broken("planning_execution", "wbs_check", lambda t, max_hours=4: [], "PLAN-03", "violations")

    def test_plan_spec_trace_blind(self):
        self.broken("planning_execution", "spec_trace", lambda s: [], "PLAN-13", "problems")

    # strategy-finance
    def test_fin_ice_formula(self):
        self.broken("strategy_finance", "ice", lambda i, c, e: i + c - e, "PROD-09", "arabic captions score")

    def test_fin_journal_blind(self):
        self.broken("strategy_finance", "journal_check", lambda e: [], "PROD-12", "unbalanced entry caught")

    def test_fin_model_unbalanced(self):
        good = mod("strategy_finance").model
        self.broken("strategy_finance", "model", lambda i: dict(good(i), balance_check=1.0), "PROD-14", "balance = 0")

    # thinking-core
    def test_think_pivots(self):
        self.broken("thinking_core", "pivots", lambda a, c: ("ads", []), "THINK-11", "pivots")

    def test_think_ledger_averages(self):
        self.broken("thinking_core", "ledger", lambda c, e: [{"claim": x, "status": "supported", "sources": []} for x in c], "THINK-12", "statuses")

    def test_think_borda(self):
        self.broken("thinking_core", "borda", lambda r, n: {"m1": 9, "m3": 1}, "THINK-47", "borda top")

    # self-discovery
    def test_self_network_classifier(self):
        self.broken("self_discovery", "classify_network", lambda r: ({}, "full egress"), "SELF-15", "allowlist")

    def test_self_key_values_leak(self):
        self.broken("self_discovery", "key_names", lambda t: [l for l in t.splitlines() if "=" in l], "SELF-17")

    def test_self_ffprobe_broken(self):
        self.broken("self_discovery", "ffprobe_duration", lambda p: None, "SELF-04", "ffprobe duration")

    # creativity-engine
    def test_idea_scamper_short(self):
        self.broken("creativity_engine", "scamper", lambda d: {"substitute": d, "eliminate": d}, "IDEA-06", "7 verbs -> 7 variants")

    def test_idea_dedupe_off(self):
        self.broken("creativity_engine", "dedupe", lambda i, thr=0.6: list(i), "IDEA-01", "near-duplicate merged")

    def test_idea_spring_never_lands(self):
        self.broken("creativity_engine", "spring", lambda t, *a, **k: 0.5 + 0 * t, "IDEA-20", "bars land on data")

    # atlas-strategy
    def test_astrat_sample_size(self):
        self.broken("atlas_strategy", "sample_size", lambda p, m, alpha=0.05, power=0.8: 1000, "ASTRAT-25", "n per arm (10% -> 12%)")

    def test_astrat_action_priority(self):
        self.broken("atlas_strategy", "action_priority", lambda s, o, d: "L", "ASTRAT-28", "AP")

    def test_astrat_lora_lint_blind(self):
        self.broken("atlas_strategy", "lora_lint", lambda c: [], "ASTRAT-69", "bad config errors")

    def test_astrat_grr_constant(self):
        self.broken("atlas_strategy", "grr", lambda d: (5.0, 10), "ASTRAT-104", "noisy gauge > 30% (unacceptable)")

    # atlas-mind
    def test_amind_unbounded_loop(self):
        good = mod("atlas_mind").bounded_loop
        self.broken("atlas_mind", "bounded_loop", lambda t, r, max_iter=12, max_attempts=3: good(t, r, max_iter, 99), "AMIND-04")

    def test_amind_fence_misses_injection(self):
        self.broken("atlas_mind", "fence", lambda c: {"wrapped": c, "suspicious": False}, "AMIND-22", "injection reported")

    def test_amind_ach_picks_wrong(self):
        self.broken("atlas_mind", "ach", lambda h, e: ("cache bug", {x: 0 for x in h}), "AMIND-46", "least disconfirmed")

    def test_amind_shadow_compare_strict(self):
        self.broken("atlas_mind", "compare", lambda p, s, tol=0.01: [k for k in p if p[k] != s.get(k)], "AMIND-53")

    # story-direction-ideas
    def test_story_lint_blind(self):
        self.broken("story_direction_ideas", "story_lint", lambda s: (100, [], []), "STORY-21")

    def test_story_proplan_cuts(self):
        self.broken("story_direction_ideas", "proplan", lambda s, f, a: ([{"beat": b, "f0": 0, "f1": 0, "audio": "bed"} for b in range(5)], (0, 1)), "STORY-03", "cut frames")

    def test_story_taste_no_window(self):
        self.broken("story_direction_ideas", "taste_keep", lambda e, k: sorted({x[k] for x in e}), "STORY-15")

    def test_story_direct_plan_end(self):
        good = mod("story_direction_ideas").direct_plan
        self.broken("story_direction_ideas", "direct_plan", lambda w: dict(good(w), end=w[-1]["end"]), "STORY-59", "end = last word + 0.35")


if __name__ == "__main__":
    unittest.main()
