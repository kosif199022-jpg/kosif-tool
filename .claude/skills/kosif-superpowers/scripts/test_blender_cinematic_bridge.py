"""Regression tests of Blender-Cycles-video to KOSIF overlay/audio integration.

Tests use fresh synthesized silent video; separately record Blender's real Cycles
production acceptance against a generated .blend in the checked-in receipt.
"""
from __future__ import annotations
import copy
import json
import math
import shutil
import struct
import subprocess
import tempfile
import unittest
import wave
from pathlib import Path

from PIL import Image, ImageDraw

from blender_cinematic_bridge import compose_video, pipeline, validate
from unified_draw import compile_scene

ROOT=Path(__file__).resolve().parent.parent
OVERLAY=ROOT/"templates"/"blender-rescue-overlay.json"


def frames_fixture(folder,fps=12,number=6,width=384,height=216,with_audio=True):
    path=Path(folder)
    scene=json.loads(OVERLAY.read_text(encoding="utf-8"))
    scene["width"]=width;scene["height"]=height
    frames=path/"frames";frames.mkdir()
    for i in range(number):
        im=Image.new("RGB",(width,height),(55,120,145))
        pen=ImageDraw.Draw(im)
        pen.ellipse((int(15+i*11),20,int(80+i*11),85),fill=(205,125,62))
        im.save(frames/f"{i:05d}.png")
    raw=path/"silent.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",
                    "-framerate",str(fps),"-i",str(frames/"%05d.png"),
                    "-c:v","libx264","-pix_fmt","yuv420p",str(raw)],
                   check=True,capture_output=True,timeout=45)
    audio=path/"master.wav"
    if with_audio:
        rate=16000
        count=round(number/fps*rate)
        values=[round(8000*math.sin(2*math.pi*440*i/rate))
                for i in range(count)]
        with wave.open(str(audio),"wb") as out:
            out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate)
            out.writeframes(struct.pack("<"+"h"*len(values),*values))
    return raw,audio,scene


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                     "requires FFmpeg and FFprobe")
class BlenderCinematicBridgeTests(unittest.TestCase):
    def test_valid_input_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            raw,audio,scene=frames_fixture(d)
            native,detail,cues,_,count=validate(raw,scene,audio,Path(d)/"new.mp4",12)
            self.assertEqual(count,6)
            self.assertEqual(len(detail),4)
            self.assertAlmostEqual(cues["duration"],.5,places=2)
            self.assertEqual(native["width"],384)

    def test_real_3d_video_compositing_with_audio(self):
        with tempfile.TemporaryDirectory() as d:
            raw,audio,scene=frames_fixture(d)
            before=(raw.read_bytes(),audio.read_bytes())
            final=Path(d)/"composited.mp4"
            report=compose_video(raw,scene,audio,final,fps=12,fade_frames=1,pulse_element=2)
            self.assertTrue(report["verified"])
            self.assertEqual((report["video_codec"],report["audio_codec"]),("h264","aac"))
            self.assertEqual(report["frame_count"],6)
            self.assertEqual(report["2d_layer_elements"],4)
            self.assertTrue(report["source_audio_unchanged"])
            self.assertEqual((raw.read_bytes(),audio.read_bytes()),before)
            self.assertEqual(len(report["output_sha256"]),64)

    def test_rejects_mismatched_scene_dimensions(self):
        with tempfile.TemporaryDirectory() as d:
            raw,audio,scene=frames_fixture(d)
            scene["width"]=512
            with self.assertRaisesRegex(ValueError,"size mismatch"):
                validate(raw,scene,audio,Path(d)/"new.mp4",12)

    def test_rejects_audio_video_frame_count_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            raw,audio,scene=frames_fixture(d,number=5)
            with self.assertRaisesRegex(ValueError,"frame count"):
                validate(raw,scene,audio,Path(d)/"out.mp4",12)

    def test_wrong_frame_rate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            raw,audio,scene=frames_fixture(d)
            with self.assertRaisesRegex(ValueError,"fps must match"):
                validate(raw,scene,audio,Path(d)/"out.mp4",10)

    def test_rejects_existing_output(self):
        with tempfile.TemporaryDirectory() as d:
            raw,audio,scene=frames_fixture(d)
            target=Path(d)/"keep.mp4";target.write_bytes(b"KEEP")
            with self.assertRaisesRegex(ValueError,"new MP4"):
                compose_video(raw,scene,audio,target)
            self.assertEqual(target.read_bytes(),b"KEEP")

    def test_respects_manual_animation_and_unsupported_format(self):
        with tempfile.TemporaryDirectory() as d:
            raw,audio,scene=frames_fixture(d)
            with self.assertRaisesRegex(ValueError,"already has keyframes"):
                compose_video(raw,scene,audio,Path(d)/"new.mp4",
                              pulse_element=4)
            with self.assertRaisesRegex(ValueError,"new MP4"):
                compose_video(raw,scene,audio,Path(d)/"new.avi")

    def test_pipeline_checks_before_expensive_render(self):
        with tempfile.TemporaryDirectory() as d:
            raw,audio,scene=frames_fixture(d)
            source=Path(d)/"placeholder.blend";source.write_bytes(b"HEADER")
            with self.assertRaisesRegex(ValueError,"overlay dimensions"):
                pipeline(source,scene,audio,Path(d)/"new.mp4",width=512,height=216)
            with self.assertRaisesRegex(ValueError,"samples"):
                pipeline(source,scene,audio,Path(d)/"new.mp4",samples=0)
            with self.assertRaisesRegex(ValueError,"existing"):
                pipeline(Path(d)/"missing.blend",scene,audio,Path(d)/"new.mp4")
            with self.assertRaisesRegex(ValueError,"new MP4"):
                pipeline(source,scene,audio,source.with_suffix(".avi"))


if __name__=="__main__":
    unittest.main(verbosity=2)
