"""Tests for World Film mode of the Black Dragon web-film skill: one world, one continuous camera.

The checker must pass the shipped example and catch each storytelling, readability and camera rule
from the brief when it is broken on purpose.
"""
import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/kosif-web-film/scripts/world_film.py"
spec = importlib.util.spec_from_file_location("world_film", SCRIPT)
wf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wf)
HAS_NODE = shutil.which("node") is not None


def run_check(plan):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "world.plan.json"
        p.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        return wf.check(plan, p if HAS_NODE else None)


class StoryRules(unittest.TestCase):
    def test_example_passes(self):
        errs, stats = run_check(wf.example_plan())
        self.assertEqual(errs, [])
        if HAS_NODE:
            self.assertLess(stats["camera"]["longest_stop_s"], wf.MAX_STOP)

    def test_one_hero_per_beat(self):
        p = wf.example_plan()
        p["beats"][1]["hero"] = ["book", "egypt"]
        self.assertTrue(any("one hero only" in e for e in run_check(p)[0]))

    def test_phrase_appears_once(self):
        p = wf.example_plan()
        p["objects"].append(dict(next(o for o in p["objects"] if o["id"] == "t_place"), id="t_again", enter=1.0))
        p["beats"][0]["text"] = "t_again"
        self.assertTrue(any("already appeared" in e for e in run_check(p)[0]))

    def test_said_and_typed_is_refused_anywhere_in_the_film(self):
        p = wf.example_plan()
        next(o for o in p["objects"] if o["id"] == "t_end")["text"] = "كتاب واحد"  # said in beat 1, typed in beat 3
        self.assertTrue(any("never both" in e for e in run_check(p)[0]))

    def test_small_type_is_refused(self):
        p = wf.example_plan()
        next(o for o in p["objects"] if o["id"] == "t_place")["size"] = 100  # 20 px at zoom 0.205
        self.assertTrue(any("read on a phone" in e for e in run_check(p)[0]))

    def test_unused_decoration_is_refused(self):
        p = wf.example_plan()
        p["objects"].append({"id": "tape", "kind": "stamp", "text": "سري", "x": 0, "y": 0, "size": 200})
        self.assertTrue(any("less is more" in e for e in run_check(p)[0]))

    def test_hit_lands_on_the_word(self):
        p = wf.example_plan()
        p["words"] = [{"w": "كتاب", "start": 3.6, "end": 4.0}]
        p["beats"][1]["hits"][0]["word"] = "كتاب"
        self.assertEqual(run_check(p)[0], [])
        p["beats"][1]["hits"][0]["t"] = 4.5
        self.assertTrue(any("misses the word" in e for e in run_check(p)[0]))

    def test_beats_must_cover_the_voiceover(self):
        p = wf.example_plan()
        p["beats"][2]["start"] = 6.4
        self.assertTrue(any("no gap" in e for e in run_check(p)[0]))
        p = wf.example_plan()
        p["audio_duration"] = 12.5
        self.assertTrue(any("match exactly" in e for e in run_check(p)[0]))


@unittest.skipUnless(HAS_NODE, "node is needed to sample the camera")
class CameraRules(unittest.TestCase):
    def test_camera_never_stops_dead(self):
        p = wf.example_plan()
        # same target twice with no drift: the camera would park for seconds
        p["beats"][2]["camera"] = dict(p["beats"][1]["camera"], drift=0)
        p["beats"][1]["camera"]["drift"] = 0
        errs = run_check(p)[0]
        self.assertTrue(any("stops dead" in e for e in errs), errs)

    def test_cramped_travel_is_caught(self):
        p = wf.example_plan()
        # a huge move squeezed into short beats: no room to ease, so it lurches
        for b, (s, e) in zip(p["beats"], [(0, 3), (3, 3.6), (3.6, 4.2), (4.2, 12)]):
            b["start"], b["end"] = s, e
            for h in b.get("hits", []):
                h["t"] = min(max(h["t"], s), e)
                if "from" in h:
                    h["from"] = s
        p["beats"][2]["camera"]["zoom"] = 1.4
        p["objects"][[o["id"] for o in p["objects"]].index("t_place")]["size"] = 420
        errs = run_check(p)[0]
        self.assertTrue(any("jerks" in e or "cut" in e for e in errs), errs)

    def test_camera_is_continuous(self):
        r = subprocess.run(["node", str(wf.WORLD / "camera.cjs"), "/dev/stdin"], input=json.dumps(wf.example_plan()),
                           capture_output=True, text=True, check=True)
        s = json.loads(r.stdout)["samples"]
        self.assertEqual(len(s), 12 * 30 + 1)
        jumps = [abs(b[1] - a[1]) * b[3] for a, b in zip(s, s[1:])]
        self.assertLess(max(jumps), wf.MAX_JUMP)


class Build(unittest.TestCase):
    def test_build_inlines_engine_and_plan(self):
        with tempfile.TemporaryDirectory() as d:
            plan = Path(d) / "world.plan.json"
            plan.write_text(json.dumps(wf.example_plan(), ensure_ascii=False), encoding="utf-8")
            page = wf.build(plan, Path(d) / "film.html").read_text(encoding="utf-8")
            self.assertIn("window.WORLD_PLAN", page)
            self.assertIn("KosifCamera", page)
            self.assertIn("window.__kosif", page)
            self.assertNotIn("Date.now", page)
            self.assertNotIn("Math.random", page)
            self.assertTrue((Path(d) / "fonts" / "Cairo.ttf").is_file())

    def test_beat_table_lists_every_beat(self):
        md = wf.beats_md(wf.example_plan())
        self.assertEqual(md.count("\n| "), 1 + 1 + 4 - 1)  # header row, divider, four beats (first row has no \n|)
        self.assertIn("رحلة لكل الدنيا", md)

    def test_review_times_cover_every_beat_and_move(self):
        r = wf.review_times(wf.example_plan())
        self.assertGreaterEqual(len(r["beats"]), 4)
        self.assertEqual(len(r["moves"]), 3)


if __name__ == "__main__":
    unittest.main()
