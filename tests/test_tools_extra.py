import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


class WordsConvertTests(unittest.TestCase):
    def run_convert(self, name, content, *extra):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / name
            src.write_text(content, encoding="utf-8")
            dst = Path(d) / "words.json"
            r = subprocess.run([PY, str(ROOT / "tools/words_convert.py"), str(src), str(dst), *extra], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            return json.loads(dst.read_text(encoding="utf-8"))

    def test_srt_spreads_words_over_cue(self):
        words = self.run_convert("a.srt", "1\n00:00:00,120 --> 00:00:01,920\nمرحبا بكم في <i>أطلس</i>\n\n2\n00:00:02,000 --> 00:00:03,000\nhello world\n")
        self.assertEqual([w["word"] for w in words], ["مرحبا", "بكم", "في", "أطلس", "hello", "world"])
        self.assertAlmostEqual(words[0]["start"], 0.12, places=3)
        self.assertAlmostEqual(words[3]["end"], 1.92, places=2)
        for a, b in zip(words, words[1:]):
            self.assertLessEqual(a["end"], b["start"] + 1e-6)

    def test_vtt_and_offset_and_gap(self):
        words = self.run_convert("b.vtt", "WEBVTT\n\n00:00.500 --> 00:01.500 align:start\none two\n", "--offset", "-0.25", "--min-gap", "0.05")
        self.assertAlmostEqual(words[0]["start"], 0.25, places=3)
        self.assertGreaterEqual(words[1]["start"] - words[0]["end"], 0.05 - 1e-6)

    def test_whisper_json(self):
        words = self.run_convert("c.json", json.dumps({"segments": [{"words": [{"word": " x", "start": 0, "end": 0.3}, {"word": "y", "start": 0.3, "end": 0.6}]}]}))
        self.assertEqual([w["word"] for w in words], ["x", "y"])

    def test_cue_time_is_weighted_by_word_length(self):
        words = self.run_convert("d.srt", "1\n00:00:00,000 --> 00:00:01,000\nab abcdef\n")
        durs = [w["end"] - w["start"] for w in words]
        self.assertAlmostEqual(durs[1] / durs[0], 3.0, places=1)

    def test_missing_paths_give_clean_errors_and_create_destination_folder(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "captions.srt"
            src.write_text("1\n00:00:00,000 --> 00:00:01,000\nhello world\n", encoding="utf-8")
            dst = Path(d) / "nodir" / "sub" / "words.json"
            ok = subprocess.run([PY, str(ROOT / "tools/words_convert.py"), str(src), str(dst)], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertEqual(len(json.loads(dst.read_text(encoding="utf-8"))), 2)
            for bad_src in (Path(d) / "missing.srt", Path(d) / "captions.txt"):
                r = subprocess.run([PY, str(ROOT / "tools/words_convert.py"), str(bad_src), str(Path(d) / "x.json")], capture_output=True, text=True)
                self.assertEqual(r.returncode, 2, bad_src)
                self.assertNotIn("Traceback", r.stderr)
            (Path(d) / "bad.json").write_text("{not json", encoding="utf-8")
            r = subprocess.run([PY, str(ROOT / "tools/words_convert.py"), str(Path(d) / "bad.json"), str(Path(d) / "x.json")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)
            self.assertNotIn("Traceback", r.stderr)
            self.assertFalse((Path(d) / "x.json").exists())


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg not installed")
class VerifyVideoTests(unittest.TestCase):
    def test_synthetic_clip_passes_and_wrong_aspect_fails(self):
        with tempfile.TemporaryDirectory() as d:
            clip = Path(d) / "clip.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=540x960:r=30:d=2", "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(clip)], check=True)
            ok = subprocess.run([PY, str(ROOT / "tools/verify_video.py"), str(clip), "--aspect", "9:16", "--fps", "30", "--duration", "2", "--lufs", "-14", "--json", str(Path(d) / "r.json")], capture_output=True, text=True)
            report = json.loads((Path(d) / "r.json").read_text())
            self.assertEqual(report["width"], 540)
            self.assertIn("[PASS] aspect is 9:16", ok.stdout)
            self.assertIn("[PASS] frame rate is 30", ok.stdout)
            self.assertIn("[PASS] audio stream present", ok.stdout)
            bad = subprocess.run([PY, str(ROOT / "tools/verify_video.py"), str(clip), "--aspect", "16:9"], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1)
            self.assertIn("[FAIL] aspect is 16:9", bad.stdout)

    def test_unreadable_inputs_exit_2_without_traceback(self):
        with tempfile.TemporaryDirectory() as d:
            clip = Path(d) / "clip.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=64x64:r=10:d=0.5", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(clip)], check=True)
            cases = {
                "missing video": [str(Path(d) / "missing.mp4"), "--aspect", "9:16"],
                "missing master": [str(clip), "--audio", str(Path(d) / "nope.wav")],
                "bad aspect": [str(clip), "--aspect", "foo"],
                "zero pixels": [str(clip), "--aspect", "10x00"],
            }
            for name, args in cases.items():
                r = subprocess.run([PY, str(ROOT / "tools/verify_video.py"), *args], capture_output=True, text=True)
                self.assertEqual(r.returncode, 2, name)
                self.assertNotIn("Traceback", r.stderr, name)
                self.assertTrue(r.stderr.strip(), name)


if __name__ == "__main__":
    unittest.main()
