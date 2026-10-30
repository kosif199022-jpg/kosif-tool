"""Cinema C V34 regression tests: portrait selection and iOS-safe media."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fetch_video as fv


class CinemaIntakeTests(unittest.TestCase):
    def test_portrait_resolution_uses_short_side(self):
        fmt, extra = fv.selector("1080")
        self.assertIn("-S", extra)
        sort = extra[extra.index("-S") + 1]
        self.assertIn("res:1080", sort)
        self.assertNotIn("[height<=1080]", fmt)
        self.assertIn("h264", sort)

    def test_audio_retains_audio_only_behavior(self):
        fmt, extra = fv.selector("audio")
        self.assertEqual(fmt, "ba/b")
        self.assertIn("--audio-format", extra)

    def test_best_and_4k_sort(self):
        for quality in ("best", "2160"):
            fmt, extra = fv.selector(quality)
            self.assertTrue(fmt)
            self.assertIn("--merge-output-format", extra)
            self.assertIn("res", extra[extra.index("-S") + 1])

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe missing")
    def test_compatible_h264_is_remuxed_without_reencode(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "portrait.mp4"
            p = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                                "-f", "lavfi", "-i", "color=c=black:s=160x280:d=1:r=10",
                                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                                "-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                                "-c:a", "aac", "-shortest", str(src)], capture_output=True)
            if p.returncode:
                self.skipTest("this ffmpeg has no libx264")
            out = fv.edit_safe(src)
            self.assertIsNotNone(out)
            self.assertTrue(src.exists(), "original must be preserved")
            self.assertTrue(out.exists())
            check = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(out)],
                                   capture_output=True, text=True, check=True)
            streams = json.loads(check.stdout)["streams"]
            video = next(s for s in streams if s["codec_type"] == "video")
            self.assertEqual(video["codec_name"], "h264")
            self.assertEqual((video["width"], video["height"]), (160, 280))
            self.assertEqual(video["pix_fmt"], "yuv420p")

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe missing")
    def test_mpeg4_falls_back_to_h264(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "old.mp4"
            p = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                                "-f", "lavfi", "-i", "color=c=black:s=160x280:d=1:r=10",
                                "-t", "1", "-c:v", "mpeg4", str(src)], capture_output=True)
            if p.returncode:
                self.skipTest("mpeg4 encoding unavailable")
            out = fv.edit_safe(src)
            if out is None:
                self.skipTest("this ffmpeg has no libx264")
            check = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                    "-show_entries", "stream=codec_name", "-of", "json", str(out)],
                                   capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(check.stdout)["streams"][0]["codec_name"], "h264")

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg missing")
    def test_bad_media_is_not_marked_safe(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "bad.mp4"
            src.write_text("not an MP4")
            self.assertIsNone(fv.edit_safe(src))
            self.assertFalse(src.with_name("bad.safe.mp4").exists())
            self.assertEqual(src.read_text(), "not an MP4")


if __name__ == "__main__":
    unittest.main()
