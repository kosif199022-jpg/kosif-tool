"""Wave-2 "remotion" power programs (engines-render-pipeline, Remotion starter + esbuild).

1) Every program in engines_render_pipeline__remotion passes through
   _black_dragon_power_program.run_program in a temp dir.
2) data/power_program_records/remotion-done.json lists exactly these cards, each was a wave-1 skip,
   and no other module of the family also programs them.
3) Planted failures: breaking the technique (Math.random instead of random(seed), an ES2021
   target, a wrong keyframe, a mock component instead of the product one, a browser picker that
   keeps the oldest build) makes that card's check fail.
Needs starters/remotion/node_modules (`npm ci` there) and a Playwright Chromium headless shell.
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

MODULE = "engines_render_pipeline__remotion"
FAMILY = "engines-render-pipeline"
_CARDS = pp.card_index()


def mod():
    return importlib.import_module(f"power_programs.{MODULE}")


def run(pid):
    with tempfile.TemporaryDirectory() as d, mock.patch.object(pp, "card_index", lambda: _CARDS):
        return bd.run_program(pid, Path(d) / "work")


def failed(result):
    return [p for p in result["problems"] if p.startswith("check failed")]


@unittest.skipUnless((ROOT / "starters" / "remotion" / "node_modules" / "remotion").is_dir(),
                     "starters/remotion/node_modules missing (run npm ci there)")
class AllProgramsPass(unittest.TestCase):
    def test_every_program_passes(self):
        ids = list(mod().PROGRAMS)
        for pid in ids:
            self.assertEqual(_CARDS[pid][0], FAMILY, pid)
        with ThreadPoolExecutor(max_workers=4) as ex:
            results = dict(zip(ids, ex.map(run, ids)))
        bad = {pid: (r["problems"] + [f"{c['name']} -> {c['observed']}" for c in r.get("checks", []) if not c["passed"]])
                   or r["error"][-300:] for pid, r in results.items() if not r["ok"]}
        self.assertEqual(bad, {})
        for pid, r in results.items():
            self.assertTrue(r["program"].endswith(f"{MODULE}.py"), (pid, r["program"]))
            self.assertLess(r["seconds"], 10, pid)
        self.assertGreaterEqual(len(ids), 14)


class Bookkeeping(unittest.TestCase):
    def test_done_file_and_no_overlap(self):
        done = json.loads((ROOT / ".claude" / "skills" / "kosif-superpowers" / "data" / "power_program_records" / "remotion-done.json").read_text())
        skipped = json.loads((ROOT / ".claude" / "skills" / "kosif-superpowers" / "data" / "power_program_records" / "engines-skipped.json").read_text())
        ids = set(mod().PROGRAMS)
        self.assertEqual(set(done), ids)
        self.assertTrue(all(v == MODULE for v in done.values()))
        self.assertTrue(ids <= set(skipped), sorted(ids - set(skipped)))
        for other in pp.modules_for(FAMILY):
            if other.__name__.endswith(MODULE):
                continue
            self.assertEqual(ids & set(getattr(other, "PROGRAMS", {})), set(), other.__name__)


@unittest.skipUnless((ROOT / "starters" / "remotion" / "node_modules" / "remotion").is_dir(),
                     "starters/remotion/node_modules missing (run npm ci there)")
class PlantedFailures(unittest.TestCase):
    def test_math_random_breaks_seeded_placement(self):
        with mock.patch.object(mod(), "RANDOM_EXPR", "Math.random()"):
            r = run("ENG-130")
        self.assertFalse(r["ok"])
        self.assertTrue(any("random(seed)" in p for p in failed(r)), r["problems"])

    def test_es2021_target_keeps_logical_assignment(self):
        with mock.patch.object(mod(), "ES_TARGET", "es2021"):
            r = run("ENG-309")
        self.assertFalse(r["ok"])
        self.assertTrue(any("es2020" in p for p in failed(r)), r["problems"])

    def test_wrong_keyframe_moves_the_box(self):
        with mock.patch.object(mod(), "TRANSLATE_END", "60px 100px"):
            r = run("ENG-124")
        self.assertFalse(r["ok"])
        self.assertTrue(any("frame 100" in p for p in failed(r)), r["problems"])

    def test_mock_component_is_not_the_product_component(self):
        with mock.patch.object(mod(), "SCENE_IMPORT", "./mock/Button.jsx"):
            r = run("ENG-350")
        self.assertFalse(r["ok"])
        self.assertTrue(any("product primary tone" in p for p in failed(r)), r["problems"])

    def test_oldest_headless_shell_picker_is_caught(self):
        m = mod()
        real = m.cloud_paths

        def oldest(node_roots, browser_roots):
            pw, _ = real(node_roots, browser_roots)
            shells = sorted(str(p) for r in browser_roots if Path(r).is_dir()
                            for p in Path(r).glob("chromium_headless_shell-*/chrome-linux/headless_shell"))
            return pw, (shells[0] if shells else None)

        with mock.patch.object(m, "cloud_paths", oldest):
            r = run("ENG-430")
        self.assertFalse(r["ok"])
        self.assertTrue(any("newest" in p for p in failed(r)), r["problems"])


if __name__ == "__main__":
    unittest.main()
