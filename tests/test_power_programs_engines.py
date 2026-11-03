"""Engines group power programs (engines-render-pipeline).

1) Every program passes through _black_dragon_power_program.run_program in a temp dir.
2) Programmed + skipped cards cover the whole family, with no overlap.
3) Planted failures: breaking a core technique (shard plan, rng, codec picker, spring, ffprobe
   stand-in, contract validator, loudness, keyframe sampler ...) makes that card's check fail.
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

MODULE = "engines_render_pipeline"
FAMILY = "engines-render-pipeline"
_CARDS = pp.card_index()


def mod():
    return importlib.import_module(f"power_programs.{MODULE}")


def run(pid):
    with tempfile.TemporaryDirectory() as d, mock.patch.object(pp, "card_index", lambda: _CARDS):
        return bd.run_program(pid, Path(d) / "work")


class AllProgramsPass(unittest.TestCase):
    def test_every_program_passes(self):
        ids = list(mod().PROGRAMS)
        for pid in ids:
            self.assertIn(pid, _CARDS, pid)
            self.assertEqual(_CARDS[pid][0], FAMILY, pid)
        with ThreadPoolExecutor(max_workers=4) as ex:
            results = dict(zip(ids, ex.map(run, ids)))
        bad = {pid: r["problems"] for pid, r in results.items() if not r["ok"]}
        self.assertEqual(bad, {})
        self.assertGreaterEqual(len(ids), 190)

    def test_skipped_and_programmed_cover_every_card(self):
        skipped = json.loads((ROOT / "out" / "power-programs" / "engines-skipped.json").read_text(encoding="utf-8"))
        cards = {pid for pid, (f, _) in _CARDS.items() if f == FAMILY}
        programmed = set(mod().PROGRAMS)
        self.assertEqual(programmed & set(skipped), set())
        self.assertEqual(cards, programmed | set(skipped))
        self.assertTrue(all(":" in why for why in skipped.values()))


class PlantedFailures(unittest.TestCase):
    def broken(self, attr, fake, pid, check):
        with mock.patch.object(mod(), attr, fake):
            r = run(pid)
        self.assertFalse(r["ok"], f"{pid} still passed with {attr} broken")
        self.assertIn(f"check failed: {check}", r["problems"])

    def test_shard_plan_with_gap(self):
        def gappy(frames, n):
            return {"frames": frames, "shards": [{"i0": k * (frames // n) + (1 if k else 0), "i1": (k + 1) * (frames // n)} for k in range(n)]}
        self.broken("shard_plan", gappy, "ENG-15", "no gaps: each i1 == next i0")

    def test_mulberry_wrong_constant(self):
        orig = mod().mulberry32

        def wrong(seed):
            return orig(seed + 1)
        self.broken("mulberry32", wrong, "ENG-34", "mulberry32(1) == JS reference")

    def test_codec_picker_ignores_level(self):
        self.broken("pick_video_codec", lambda w, h, fps, sup: ("avc1.64001F", ["avc1.64001F"]), "ENG-27", "1080p -> High level 4.2 (avc1.64002A)")

    def test_spring_wrong_closed_form(self):
        self.broken("spring", lambda t, k, d, m=1.0: 1 - mod().math.exp(-t * 5), "ENG-81", "closed-form spring matches ODE integration")

    def test_ffprobe_shim_off_by_one(self):
        orig = mod().ffprobe_shim
        self.broken("ffprobe_shim", lambda p: {**orig(p), "frames": orig(p)["frames"] - 1}, "ENG-07", "exact frame count 37")

    def test_contract_validator_accepts_everything(self):
        self.broken("composition_errors", lambda *a, **k: [], "ENG-01", "page without data-fps rejected")

    def test_loudness_not_normalised(self):
        self.broken("normalize_to", lambda src, dst, target: mod().measure_lufs(src)[0], "ENG-08", "sound pass -14 LUFS +-0.5")

    def test_sampler_drops_a_keyframe(self):
        orig = mod().sampled
        self.broken("sampled", lambda fn, t0, t1, fps=60: orig(fn, t0, t1, fps)[:-1], "ENG-75", "60 keyframes per second")

    def test_post_stack_no_vignette(self):
        orig = mod().post_stack
        self.broken("post_stack", lambda img, **k: orig(img, **{**k, "vignette": 0}), "ENG-11", "vignette .42 at corners")

    def test_lint_misses_math_random(self):
        self.broken("lint_js", lambda src, banned: [], "ENG-92", "Math.random is a lint error")

    def test_ssrf_guard_open(self):
        self.broken("blocked_host", lambda h: False, "ENG-162", "every redirect hop re-checked")

    def test_back_out_without_overshoot(self):
        self.broken("back_out", lambda p, c=1.6: 1 - (1 - p) ** 3, "ENG-146", "overshoots: peak matches q* = -2c/(3(c+1))")

    def test_fingerprint_ignores_params(self):
        orig = mod().fingerprint
        self.broken("fingerprint", lambda project, params: orig(project, {}), "ENG-103", "render param (crf) change re-renders")


if __name__ == "__main__":
    unittest.main()
