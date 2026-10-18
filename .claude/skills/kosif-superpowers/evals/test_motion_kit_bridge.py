"""Regression tests for the original KOSIF Motion Starter Kit timing bridge."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import motion_kit_bridge as bridge


class MotionKitBridgeTests(unittest.TestCase):
    def test_ten_styles_and_four_executable_routes(self):
        self.assertEqual(len(bridge.STYLE_MAP), 10)
        self.assertEqual(
            {k for k, v in bridge.STYLE_MAP.items() if v[0] == "native_svg"},
            {"doodle", "plotter", "whiteboard", "infographic"})

    def test_demo_all_native_styles_pass_full_director_validation(self):
        timing = bridge.demo_timings()
        self.assertEqual(timing["timing_provenance"], "estimated_no_audio")
        for style in ("doodle", "plotter", "whiteboard", "infographic"):
            with self.subTest(style=style):
                spec = bridge.build_story(timing, style)
                self.assertEqual(bridge.director.validate(spec)["scenes"], 2)
                self.assertEqual(spec["width"], 1080)
                self.assertEqual(spec["height"], 1920)

    def test_strict_audio_alignment_and_arabic_whole_words(self):
        d = {"duration": 4, "audio": "voice.mp3",
             "source": "MMS_FA forced alignment",
             "lines": [{"words": [{"w": "السلام", "start": 0.2, "end": 1.0},
                                   {"w": "عليكم", "start": 1.1, "end": 2.0}]}]}
        parsed = bridge.normalize_timing(d)
        words = bridge.build_story(parsed, "doodle")["scenes"][0]["words"]
        self.assertEqual([w["text"] for w in words], ["السلام", "عليكم"])
        self.assertEqual(words[1]["start"], 1.1)
        self.assertTrue(parsed["audio_claimed"])
        self.assertIn("not_independently_verified", parsed["timing_provenance"])

    def test_estimated_without_audio_rejected_unless_explicit(self):
        d = {"duration": 3, "lines": [{"words": [
            {"w": "test", "start": 0.2, "end": 0.8}]}]}
        with self.assertRaisesRegex(ValueError, "allow-estimated"):
            bridge.normalize_timing(d)
        self.assertEqual(bridge.normalize_timing(d, True)["timing_provenance"],
                         "estimated_no_audio")

    def test_rejects_overlap_and_missing_timestamps(self):
        d = {"duration": 3, "audio": "v.wav", "lines": [
            {"words": [{"w": "a", "start": 0, "end": 2},
                       {"w": "b", "start": 1, "end": 2.5}]}]}
        with self.assertRaisesRegex(ValueError, "overlapping"):
            bridge.normalize_timing(d)
        d["lines"][0]["words"][1].pop("end")
        with self.assertRaises(ValueError):
            bridge.normalize_timing(d)

    def test_non_native_style_never_claimed_executable(self):
        with self.assertRaisesRegex(ValueError, "needs its own adapter"):
            bridge.build_story(bridge.demo_timings(), "fake3d")

    def test_creates_real_html_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            story = base / "story.json"
            html = base / "preview.html"
            spec = bridge.build_story(bridge.demo_timings(), "plotter")
            report = bridge.write_outputs(spec, story, html)
            self.assertEqual(report["storyboard"], str(story))
            self.assertEqual(json.loads(story.read_text(encoding="utf-8"))["version"], 1)
            self.assertIn("id='kosif-data'", html.read_text(encoding="utf-8"))
            with self.assertRaisesRegex(ValueError, "outputs must be new"):
                bridge.write_outputs(spec, story, html)


if __name__ == "__main__":
    unittest.main()
