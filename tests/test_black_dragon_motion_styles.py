"""Tests for the Black Dragon code-motion style studio (no rendering)."""
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-black-dragon/scripts"


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ms = _load("motion_styles", "motion_styles.py")
dragon = _load("black_dragon_native_m", "black_dragon.py")

SRT = """1
00:00:00,000 --> 00:00:02,000
ab abcd

2
00:00:02,500 --> 00:00:03,000
x
"""


class MotionStylesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = ms.load()

    def test_catalog_shape(self):
        self.assertEqual(len(self.data["styles"]), 7)
        self.assertEqual(len(self.data["principles"]), 16)

    def test_match_routes(self):
        self.assertEqual(ms.match("شرح برنامج خطوة بخطوة tutorial", self.data)[0]["id"], "software-walkthrough")
        self.assertEqual(ms.match("درس على السبورة بالطباشير", self.data)[0]["id"], "chalk-talk")

    def test_brief_without_topic_asks(self):
        b = ms.brief("data-story", self.data)
        self.assertEqual(b["status"], "STYLE_BRIEF_NOT_A_RENDER")
        self.assertTrue(b["open_questions"])
        self.assertIn("M05", [p["id"] for p in b["principles"]])
        self.assertNotIn("M05", [p["id"] for p in ms.brief("data-story", self.data, "x", storyboard=False)["principles"]])

    def test_vo_timeline_spreads_by_length_and_adds_tail(self):
        tl = ms.vo_timeline(ms.parse_srt(SRT))
        w = tl["words"]
        self.assertEqual([x["w"] for x in w], ["ab", "abcd", "x"])
        self.assertAlmostEqual(w[0]["end"], 2 * 2 / 6, places=3)
        self.assertAlmostEqual(w[1]["end"], 2.0, places=3)
        self.assertAlmostEqual(tl["duration"], 3.0 + 1.2, places=3)
        self.assertEqual(tl["idea_boundaries"], [0.0, 2.5])

    def test_cue_check_mix_rules(self):
        crowded = [{"t": 1.0, "name": n} for n in ("slam", "pop", "whoosh", "marker")]
        self.assertIn("max_3_simultaneous", [i["rule"] for i in ms.cue_check(crowded)["issues"]])
        ticks = [{"t": i / 20, "name": "tick"} for i in range(20)]
        self.assertIn("ticks_max_12_per_second", [i["rule"] for i in ms.cue_check(ticks)["issues"]])
        good = [{"t": 0.5, "name": "slam"}, {"t": 3.0, "name": "boom"}]
        self.assertTrue(ms.cue_check(good)["passed"])
        speech = [{"w": "hi", "start": 1.0, "end": 1.5}]
        bad_vo = [{"t": 0.8, "name": "riser", "dur": 1.0}, {"t": 2.0, "name": "pop"}]
        rules = [i["rule"] for i in ms.cue_check(bad_vo, speech)["issues"]]
        self.assertIn("no_riser_under_speech", rules)
        self.assertIn("small_sounds_soft_under_voiceover", rules)

    def test_clone_plan_has_five_steps_and_guardrail(self):
        c = ms.clone_plan(self.data)
        self.assertEqual(len(c["steps"]), 5)
        self.assertIn("لا", c["guardrail_ar"])

    def test_dragon_cli_motion_and_srt_file(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "v.srt"
            f.write_text(SRT, encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = dragon.main(["motion", "vo-timeline", "--srt", str(f)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(buf.getvalue())["source_granularity"], "line-spread-by-length")

    def test_no_verbatim_source_text(self):
        raw = (SCRIPTS.parent / "data/motion_styles.json").read_text(encoding="utf-8")
        for phrase in ("Every frame is a pure function of t", "STORYBOARD FIRST", "Recreate the STYLE, not the content"):
            self.assertNotIn(phrase, raw)


if __name__ == "__main__":
    unittest.main()
