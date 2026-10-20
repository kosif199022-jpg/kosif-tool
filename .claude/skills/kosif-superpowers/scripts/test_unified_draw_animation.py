"""Integration regressions for keyframed mixed drawing to GIF/MP4."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageChops
from creative_paint import paint
from unified_draw import animate, compile_scene, render

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "templates" / "unified-draw-demo.json"


def animated_data():
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))
    data["elements"][0]["keyframes"] = [
        {"time":0, "x":0, "y":0, "angle":0},
        {"time":1, "x":20, "y":20, "angle":0}
    ]
    data["elements"][1]["keyframes"] = [
        {"time":0, "x":0, "y":0, "opacity":1},
        {"time":1, "x":75, "y":0, "opacity":0.7}
    ]
    return data


class UnifiedDrawAnimationTests(unittest.TestCase):
    def test_both_stroke_and_shape_receive_keyframes(self):
        scene, detail = compile_scene(animated_data())
        self.assertEqual(len(detail), 5)
        self.assertEqual(len(scene["layers"][0]["keyframes"]), 2)
        self.assertEqual(len(scene["layers"][1]["keyframes"]), 2)
        before = paint(scene, 0)
        after = paint(scene, .75)
        difference = ImageChops.difference(before.convert("RGB"), after.convert("RGB"))
        self.assertIsNotNone(difference.getbbox(), "keyframe transform must change rendered pixels")

    def test_still_render_at_selected_time(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = [str(Path(d)/f"frame{n}.png") for n in (0,1)]
            render(animated_data(), png=a, time=0)
            render(animated_data(), png=b, time=1)
            with Image.open(a) as x, Image.open(b) as y:
                self.assertNotEqual(x.convert("RGB").tobytes(), y.convert("RGB").tobytes())

    def test_gif_frame_sequence(self):
        with tempfile.TemporaryDirectory() as d:
            out = str(Path(d)/"sample.gif")
            result = animate(animated_data(), out, fps=8, duration=1)
            self.assertEqual(result["animation"]["frames"], 8)
            self.assertTrue(result["animation"]["verified"])
            with Image.open(out) as im:
                self.assertGreater(im.n_frames, 1)
                self.assertEqual(im.size, (640,480))

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "requires FFmpeg and FFprobe")
    def test_mp4_video_is_frame_verified(self):
        with tempfile.TemporaryDirectory() as d:
            out = str(Path(d)/"sample.mp4")
            result = animate(animated_data(), out, fps=8, duration=1)
            self.assertEqual(result["animation"]["frames"], 8)
            info = json.loads(subprocess.check_output([
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=codec_name,nb_frames,width,height,r_frame_rate",
                "-of", "json", out], text=True))
            stream = info["streams"][0]
            self.assertEqual(stream["codec_name"], "h264")
            self.assertEqual(int(stream["nb_frames"]), 8)
            self.assertEqual((stream["width"], stream["height"]), (640,480))

    def test_invalid_keyframe_order_is_rejected(self):
        data = animated_data()
        data["elements"][0]["keyframes"][1]["time"] = -1
        with self.assertRaises(ValueError):
            compile_scene(data)

    def test_output_and_dependency_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)/"sample.gif"
            target.write_bytes(b"KEEP")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                animate(animated_data(), str(target))
            self.assertEqual(target.read_bytes(), b"KEEP")
            with self.assertRaisesRegex(ValueError, ".gif or .mp4"):
                animate(animated_data(), str(Path(d)/"bad.exe"))
            with patch("creative_paint.shutil.which", return_value=None):
                with self.assertRaisesRegex(ValueError, "FFmpeg unavailable"):
                    animate(animated_data(), str(Path(d)/"video.mp4"), fps=8, duration=1)

    def test_bounded_frames(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, "300 frame"):
                animate(animated_data(), str(Path(d)/"long.gif"), fps=60, duration=10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
