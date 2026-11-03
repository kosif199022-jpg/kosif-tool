"""Language group power programs: every program passes its known-answer checks, and a broken
technique (a patched core function) makes the card's checks fail."""
from __future__ import annotations
import importlib
import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import _black_dragon_power_program as runner  # noqa: E402
import power_programs as pp  # noqa: E402

FAMILIES = ["ai-generation", "prompt-craft", "agent-orchestration", "writing-humanizer", "arabic-language", "voice-tts",
            "web-research", "knowledge-graph", "atlas-research"]


def mod(family):
    return importlib.import_module("power_programs." + family.replace("-", "_"))


def run(pid):
    with tempfile.TemporaryDirectory() as t:
        return runner.run_program(pid, Path(t) / "w")


ALL = [(f, pid) for f in FAMILIES for pid in mod(f).PROGRAMS]

PLANTED = [
    ("atlas-research", "cohen_kappa", lambda a, b: 1.0, "AWEB-04"),
    ("atlas-research", "n_means", lambda d, alpha=0.05, power=0.8: 50, "AWEB-06"),
    ("atlas-research", "needs_browser", lambda html, mode="auto", known_spa=False: {"browser": False, "warnings": []}, "AWEB-02"),
    ("web-research", "claim_ledger", lambda ev: [[c, "fact", "-", "-", ""] for c in ev], "WEB-10"),
    ("web-research", "score_hit", lambda d, q: 1.0, "WEB-12"),
    ("web-research", "licence_rule", lambda t: "reuse with notice", "WEB-19"),
    ("knowledge-graph", "modularity_communities", lambda n, e: ([set(n)], 0.0), "GRAPH-22"),
    ("knowledge-graph", "label", lambda e: ("INFERRED", 0.5), "GRAPH-19"),
    ("knowledge-graph", "bfs_order", lambda edges, start: list(reversed(edges)), "GRAPH-20"),
    ("arabic-language", "agreement_errors", lambda s: ["planted: every sentence flagged"], "ARL-19"),
    ("arabic-language", "dialect_scores", lambda t: ("msa", {}, False), "ARL-17"),
    ("arabic-language", "tashkeel_tells", lambda t: ([], []), "ARL-09"),
    ("writing-humanizer", "act_on", lambda hits: True, "WRITE-01"),
    ("writing-humanizer", "egyptian_check", lambda t: ([], []), "WRITE-19"),
    ("writing-humanizer", "invented_terms", lambda a, b: [], "WRITE-25"),
    ("writing-humanizer", "file_mode", lambda text, edit: edit(text), "WRITE-12"),
    ("prompt-craft", "vote", lambda a: {"answer": "42", "agreement": "5/5", "uncertain": False}, "PROMPT-29"),
    ("prompt-craft", "rubric", lambda s, gates=(): (20, "ship", None), "PROMPT-14"),
    ("prompt-craft", "route", lambda req, authored_by_claude=False: {"mode": "b", "execute": True, "visible_rewrite": False}, "PROMPT-17"),
    ("prompt-craft", "antipatterns", lambda p: [], "PROMPT-13"),
    ("agent-orchestration", "receipt_ok", lambda r: [], "AGENT-05"),
    ("agent-orchestration", "fan_out", lambda lanes, run: ({l: "ok" for l in lanes}, "merge the rest"), "AGENT-07"),
    ("agent-orchestration", "HOOK", "import json\nprint(json.dumps({'hookSpecificOutput': {'additionalContext': 'x'}}))\n", "AGENT-20"),
    ("agent-orchestration", "safe_snippet", lambda code: (True, ""), "AGENT-53"),
    ("agent-orchestration", "run_graph",
     lambda nodes, state, ck, fail_at=None, approve=False, _orig=mod("agent-orchestration").run_graph: _orig(nodes, state, ck, fail_at, True),
     "AGENT-47"),
    ("voice-tts", "word_budget", lambda s, wps=2.5, lang="en": int(s * 3), "VOICE-18"),
    ("voice-tts", "CHAIN39", "anull", "VOICE-39"),
    ("voice-tts", "audiolab", lambda st, sr, mode: st.mean(axis=1), "VOICE-42"),
    ("voice-tts", "word_colour", lambda t, start, lead=0.06, dur=0.12: (0, 0, 0), "VOICE-35"),
    ("ai-generation", "sanitize_svg", lambda s: s, "GEN-33"),
    ("ai-generation", "SDXL", {"1:1": (1024, 1024), "16:9": (1344, 768), "9:16": (720, 1280), "4:5": (896, 1152),
                               "3:2": (1216, 832), "2.39:1": (1536, 640)}, "GEN-10"),
    ("ai-generation", "teal_orange", lambda img, amount=0.3: img, "GEN-30"),
    ("ai-generation", "outlier_action", lambda imgs, thresh=40: ([], "consistent"), "GEN-85"),
]




class LanguagePrograms(unittest.TestCase):
    def test_every_program_passes(self):
        for family, pid in ALL:
            with self.subTest(pid=pid):
                r = run(pid)
                self.assertTrue(r["ok"], (pid, r.get("problems"), r.get("error", "")[-500:]))
                self.assertEqual(r["family"], family)

    def test_planted_failures_fail(self):
        for family, attr, fake, pid in PLANTED:
            with self.subTest(pid=pid, attr=attr):
                with mock.patch.object(mod(family), attr, fake):
                    r = run(pid)
                self.assertFalse(r["ok"], f"{pid} still passed with {attr} broken")
                self.assertTrue(any(p.startswith("check failed") for p in r["problems"]), r["problems"])

    def test_three_planted_failures_per_module(self):
        c = Counter(f for f, *_ in PLANTED)
        self.assertTrue(all(c[f] >= 3 for f in FAMILIES), c)

    def test_skipped_and_programmed_cover_every_card(self):
        path = ROOT / "out" / "power-programs" / "language-skipped.json"
        if not path.exists():
            self.skipTest("skip list lives in the gitignored out/ folder")
        skipped = json.loads(path.read_text(encoding="utf-8"))
        cards = {pid for pid, (fam, _) in pp.card_index().items() if fam in FAMILIES}
        programmed = {pid for _, pid in ALL}
        self.assertFalse(programmed & set(skipped))
        self.assertEqual(programmed | set(skipped), cards)


if __name__ == "__main__":
    unittest.main()
