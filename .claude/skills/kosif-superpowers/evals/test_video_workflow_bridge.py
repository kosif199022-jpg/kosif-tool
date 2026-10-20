#!/usr/bin/env python3
"""Deterministic tests for clean-room, non-destructive video workflow adapters."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from video_workflow_bridge import frame_reviews, paper_edit, parse_keep, read_words


WORDS = [
    {"word": "في", "start": 0.13, "end": 0.33},
    {"word": "البداية", "start": 0.40, "end": 0.91},
    {"word": "كان", "start": 1.09, "end": 1.30},
    {"word": "العدد", "start": 1.40, "end": 1.89},
    {"word": "500", "start": 1.91, "end": 2.14},
]


class VideoWorkflowTests(unittest.TestCase):
    def test_arabic_and_numbers_survive(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "words.json"
            p.write_text(json.dumps(WORDS, ensure_ascii=False), encoding="utf-8")
            rows = read_words(p)
            self.assertEqual([x["word"] for x in rows], ["في", "البداية", "كان", "العدد", "500"])

    def test_dict_words_supported(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "w.json"
            p.write_text(json.dumps({"words": WORDS}), encoding="utf-8")
            self.assertEqual(len(read_words(p)), 5)

    def test_overlap_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "w.json"
            p.write_text(json.dumps([WORDS[0], {"word": "x", "start": 0.2, "end": 0.5}]))
            with self.assertRaisesRegex(ValueError, "overlapping"):
                read_words(p)

    def test_empty_text_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "w.json"
            p.write_text(json.dumps([{"word": "", "start": 0.1, "end": 0.2}]))
            with self.assertRaises(ValueError):
                read_words(p)

    def test_range_deduplicates_and_sorts(self):
        self.assertEqual(parse_keep("5,1-2,2,4", 5), [1, 2, 4, 5])

    def test_invalid_ranges_rejected(self):
        for expr in ("0-2", "1-7", "4-2", "1;2", "", "1,,2"):
            with self.subTest(expr=expr), self.assertRaises(ValueError):
                parse_keep(expr, 5)

    def test_paper_edit_has_no_audio_mutation(self):
        w = [{**row, "index": k} for k, row in enumerate(WORDS, 1)]
        plan = paper_edit(w, [1, 2, 4, 5], fps=30)
        self.assertIn("not_processed", plan["audio_policy"])
        self.assertEqual(plan["segments"][0]["word_indices"], [1, 2])
        self.assertEqual(plan["segments"][1]["word_indices"], [4, 5])
        self.assertGreater(plan["output_frames"], 0)
        self.assertEqual(plan["segments"][1]["output_start_frame"], plan["segments"][0]["output_end_frame"])

    def test_word_boundaries_not_clipped(self):
        w = [{**row, "index": k} for k, row in enumerate(WORDS, 1)]
        plan = paper_edit(w, [3], 30)
        seg = plan["segments"][0]
        self.assertLessEqual(seg["source_start_frame"] / 30, WORDS[2]["start"])
        self.assertGreaterEqual(seg["source_end_frame"] / 30, WORDS[2]["end"])

    def test_review_rtl_and_anchor(self):
        data = frame_reviews([{"time": 1.23, "comment": "التشكيل مقصوص", "x": 0.25, "y": 0.6}],
                             duration=5, fps=30, width=1080, height=1920)
        marker = data["markers"][0]
        self.assertEqual(marker["timecode"], "00:00:01:07")
        self.assertEqual(marker["comment"], "التشكيل مقصوص")
        self.assertEqual(marker["point_px"], {"x": 270, "y": 1152})

    def test_review_sorted_and_deterministic(self):
        notes = [{"time": 2.0, "comment": "second"}, {"time": 1.0, "comment": "first"}]
        a = frame_reviews(notes, duration=4)
        b = frame_reviews(notes, duration=4)
        self.assertEqual(a, b)
        self.assertEqual([m["frame"] for m in a["markers"]], [30, 60])

    def test_review_rejects_invalid_data(self):
        for notes in ([{"time": 1.0, "comment": "ok", "x": 1.3, "y": 0.5}],
                      [{"time": -1.0, "comment": "ok"}],
                      [{"time": 2.0, "comment": "ok"}],
                      [{"time": 1.0, "comment": ""}],
                      [{"time": 1.0, "comment": "x", "x": 0.4}]):
            with self.subTest(notes=notes), self.assertRaises(ValueError):
                frame_reviews(notes, duration=2)

    def test_last_frame_clamped(self):
        x = frame_reviews([{"time": 1.999, "comment": "last"}], duration=2, fps=30)
        self.assertEqual(x["markers"][0]["frame"], 59)


if __name__ == "__main__":
    unittest.main()
