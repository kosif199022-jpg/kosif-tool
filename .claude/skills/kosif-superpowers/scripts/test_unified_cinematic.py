"""KOSIF cinematic integration regression and actual audio/video acceptance."""
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
from unittest.mock import patch
from PIL import Image, ImageChops
from audio_cue_mapper import measure_wav
from unified_cinematic import camera_frame, fade_frame, plan, produce, pulse_scene
from unified_draw import compile_scene
from unified_media import compose

BASE=Path(__file__).resolve().parent.parent
PHOTO=BASE/"templates/unified-media-demo-photo.png"
SCENE=BASE/"templates/unified-draw-motion-demo.json"

def wav_sample(path,duration=2,rate=22050):
    """Make true PCM WAV with time-localized pulses (not copyrighted material)."""
    samples=[]
    for j in range(round(duration*rate)):
        t=j/rate
        click=any(0<=t-mark<.045 for mark in (.3,.75,1.2,1.65))
        amp=.6 if click else .015
        y=round(amp*math.sin(2*math.pi*440*t)*32767)
        samples.append(max(-32768,min(32767,y)))
    with wave.open(str(path),"wb") as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
        f.writeframes(struct.pack("<"+"h"*len(samples),*samples))
    return path

def drawing():
    return json.loads(SCENE.read_text(encoding="utf8"))

class CinematicIntegration(unittest.TestCase):
    def test_audio_cue_measurement_and_duration(self):
        with tempfile.TemporaryDirectory() as d:
            wav=wav_sample(Path(d)/"a.wav")
            cues=measure_wav(wav)
            self.assertAlmostEqual(cues["duration"],2,places=4)
            self.assertFalse(cues["verified_beats"])
            self.assertIsNone(cues["bpm"])
            self.assertGreater(len(cues["onset_candidates_seconds"]),0)

    def test_keyframes_from_amplitude_do_not_claim_beats(self):
        scene,_=compile_scene(drawing())
        before=copy.deepcopy(scene)
        moved,events=pulse_scene(scene,[.3,.75,1.2,1.65],2,3)
        self.assertEqual(len(events),4)
        self.assertFalse(before["layers"][2].get("keyframes"))
        self.assertEqual(len(moved["layers"][2]["keyframes"]),14)
        with self.assertRaisesRegex(ValueError,"already has keyframes"):
            pulse_scene(scene,[.3],2,1)
        start=compose(Image.open(PHOTO).convert("RGBA"),moved,0)
        animated=compose(Image.open(PHOTO).convert("RGBA"),moved,.3)
        self.assertIsNotNone(ImageChops.difference(start,animated).getbbox())

    def test_camera_transforms(self):
        base=Image.open(PHOTO).convert("RGBA")
        for name in ("static","push-in","pull-back","pan-right"):
            a=camera_frame(base,(640,480),0,name)
            b=camera_frame(base,(640,480),1,name)
            self.assertEqual(a.size,(640,480))
            self.assertEqual(b.size,(640,480))
            if name!="static":
                self.assertIsNotNone(ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox())
        with self.assertRaisesRegex(ValueError,"camera"):
            camera_frame(base,(640,480),0,"unknown")

    def test_fade_entry_exit(self):
        im=Image.new("RGB",(256,256),(250,120,50))
        first=fade_frame(im,0,20,4)
        mid=fade_frame(im,10,20,4)
        last=fade_frame(im,19,20,4)
        self.assertLess(first.getpixel((0,0))[0],mid.getpixel((0,0))[0])
        self.assertLess(last.getpixel((0,0))[0],mid.getpixel((0,0))[0])

    def test_bad_wav_and_frame_limit(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/"invalid.wav";fake.write_bytes(b"not wave")
            out=Path(d)/"out.mp4"
            with self.assertRaises(ValueError):
                plan(PHOTO,drawing(),fake,out)
            with self.assertRaisesRegex(ValueError,"300 frame"):
                plan(PHOTO,drawing(),wav_sample(Path(d)/"long.wav",8),out,fps=60)

    # plan() checks for FFmpeg before it validates pulse keyframes, so without FFmpeg it raises the FFmpeg error first.
    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"FFmpeg required")
    def test_immutable_manual_keyframes(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"out.mp4"
            wav=wav_sample(Path(d)/"a.wav")
            with self.assertRaisesRegex(ValueError,"keyframes"):
                plan(PHOTO,drawing(),wav,out,pulse_element=1)

    def test_invalid_config_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            wav=wav_sample(Path(d)/"a.wav")
            out=Path(d)/"exists.mp4";out.write_bytes(b"KEEP")
            with self.assertRaisesRegex(ValueError,"new MP4"):
                plan(PHOTO,drawing(),wav,out)
            self.assertEqual(out.read_bytes(),b"KEEP")
            with self.assertRaisesRegex(ValueError,"camera"):
                plan(PHOTO,drawing(),wav,Path(d)/"out.mp4",camera="teleport")
            with self.assertRaisesRegex(ValueError,"fade-frames"):
                plan(PHOTO,drawing(),wav,Path(d)/"out.mp4",fade_frames=50)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"FFmpeg required")
    def test_real_h264_aac_both_streams_with_cues(self):
        with tempfile.TemporaryDirectory() as d:
            wav=wav_sample(Path(d)/"a.wav")
            checksum=wav.read_bytes()
            out=Path(d)/"out.mp4"
            receipt=produce(PHOTO,drawing(),wav,out,fps=12,camera="push-in",
                            fade_frames=2,pulse_element=3,effect="develop",exposure=.2)
            self.assertTrue(receipt["verified"])
            self.assertEqual(receipt["frames"],24)
            self.assertEqual(receipt["video_codec"],"h264")
            self.assertEqual(receipt["output_audio_codec"],"aac (re-encoded)")
            self.assertGreater(receipt["pulse_keyframes_added"],0)
            self.assertFalse(receipt["verified_beats"])
            self.assertEqual(wav.read_bytes(),checksum)
            self.assertTrue(out.stat().st_size>2000)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"FFmpeg required")
    def test_cinematic_video_audio_durations(self):
        with tempfile.TemporaryDirectory() as d:
            wav=wav_sample(Path(d)/"a.wav",duration=1.5)
            out=Path(d)/"out.mp4"
            receipt=produce(PHOTO,drawing(),wav,out,fps=8,camera="pan-right",fade_frames=1)
            info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(out)],text=True))
            audio=next(s for s in info["streams"] if s["codec_type"]=="audio")
            video=next(s for s in info["streams"] if s["codec_type"]=="video")
            self.assertEqual(video["codec_name"],"h264")
            self.assertEqual(audio["codec_name"],"aac")
            self.assertEqual(int(video["nb_frames"]),12)
            self.assertAlmostEqual(receipt["audio_master_seconds"],1.5,places=3)


if __name__=="__main__":
    unittest.main(verbosity=2)
