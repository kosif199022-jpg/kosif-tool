"""Functional tests for original full-body and facial animation."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from PIL import Image, ImageChops

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL/"scripts"))
import character_fullbody as b
import character_ik as ik
from creative_paint import paint, svg

SCENE = SKILL/"templates/fullbody-demo.json"
WORDS = SKILL/"templates/fullbody-demo-words.json"

class FullbodyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scene = json.loads(SCENE.read_text(encoding="utf-8-sig"))
        cls.words = ik.words_from_file(WORDS)
        cls.p = b.prepare(cls.scene, cls.words)

    def test_actions_resolved_including_exact_word(self):
        self.assertEqual(self.p["actions"][1]["time"], 0.5)
        self.assertEqual(len(self.p["actions"]), 6)

    def test_all_layers_and_character_geometry(self):
        drawing = b.drawing(self.p, 0)
        self.assertEqual([x["name"] for x in drawing["layers"]],
            ["ground","back limbs","torso and head","facial expression","front arm"])
        self.assertGreater(sum(len(x["shapes"]) for x in drawing["layers"]), 18)
        self.assertEqual(paint(drawing).size, (480, 480))

    def test_root_motion_persists_after_walk(self):
        _, d0 = b.motion(self.p, 0)
        _, d1 = b.motion(self.p, 1.0)
        _, d2 = b.motion(self.p, 1.15)
        self.assertEqual(d0, 0)
        self.assertAlmostEqual(d1, 30)
        self.assertAlmostEqual(d2, 30)
        self.assertGreater(b.motion(self.p, 2.4)[1], d2)

    def test_wave_changes_arm_pixels(self):
        before = paint(b.drawing(self.p, 0.3))
        during = paint(b.drawing(self.p, 0.75))
        self.assertIsNotNone(ImageChops.difference(before.convert("RGB"),during.convert("RGB")).getbbox())

    def test_smile_changes_mouth(self):
        p = copy.deepcopy(self.p)
        p["actions"] = [a for a in p["actions"] if a["kind"] == "smile"]
        neutral = paint(b.drawing(p, 0.5))
        happy = paint(b.drawing(p, 1.5))
        self.assertIsNotNone(ImageChops.difference(neutral.convert("RGB"),happy.convert("RGB")).getbbox())

    def test_blink_changes_eyes(self):
        p = copy.deepcopy(self.p)
        p["actions"] = [a for a in p["actions"] if a["kind"] == "blink"]
        before = paint(b.drawing(p, 2.45))
        closed = paint(b.drawing(p, 2.6))
        self.assertIsNotNone(ImageChops.difference(before.convert("RGB"),closed.convert("RGB")).getbbox())

    def test_reject_unverified_word(self):
        scene = copy.deepcopy(self.scene)
        scene["actions"][1]["word"] = "not-there"
        with self.assertRaises(ValueError):
            b.prepare(scene, self.words)

    def test_reject_overlapping_locomotion(self):
        scene = copy.deepcopy(self.scene)
        scene["actions"][3]["time"] = 0.8
        with self.assertRaises(ValueError):
            b.prepare(scene, self.words)

    def test_reject_malicious_dimensions_and_invalid_time(self):
        for bad in (float("nan"), True, 5000):
            scene = copy.deepcopy(self.scene)
            scene["width"] = bad
            with self.assertRaises(ValueError):
                b.prepare(scene, self.words)
        scene = copy.deepcopy(self.scene)
        scene["actions"][0]["duration"] = 99
        with self.assertRaises(ValueError):
            b.prepare(scene, self.words)

    def test_still_png_svg_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp)/"still.png"
            vec = Path(tmp)/"still.svg"
            self.assertTrue(b.export(self.p,png,at=1.55)["verified"])
            self.assertTrue(b.export(self.p,vec,at=1.55)["verified"])
            with Image.open(png) as im:
                self.assertEqual(im.size, (480,480))
            self.assertIn("<svg",vec.read_text(encoding="utf-8"))
            with self.assertRaises(ValueError):
                b.export(self.p,png)

    def test_gif_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"motion.gif"
            result = b.export(self.p,path,fps=8)
            self.assertEqual(result["frames"],24)
            self.assertGreater(path.stat().st_size,100)
            with Image.open(path) as im:
                self.assertGreater(im.n_frames,4)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"FFmpeg missing")
    def test_h264_mp4(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"motion.mp4"
            result = b.export(self.p,path,fps=12)
            self.assertTrue(result["verified"])
            self.assertEqual(result["frames"],36)
            self.assertEqual(ik.probe(path,"v:0")[0]["codec_name"],"h264")

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"FFmpeg missing")
    def test_aac_packet_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp)/"audio.m4a"
            video = Path(tmp)/"with-audio.mp4"
            import subprocess
            subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i",
                           "sine=frequency=440:duration=3","-c:a","aac",
                           "-b:a","128k",str(wav)],check=True,capture_output=True)
            result = b.export(self.p,video,fps=8,audio=wav)
            self.assertTrue(result["audio_packets_preserved"])
            self.assertEqual(ik.packet_hashes(wav), ik.packet_hashes(video))

    def test_mp4_without_ffprobe_fails_before_writing(self):
        from unittest import mock
        real = shutil.which
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
                b.shutil, "which", lambda name: None if name == "ffprobe" else real(name)):
            path = Path(tmp)/"motion.mp4"
            with self.assertRaises(ValueError):
                b.export(self.p, path, fps=8)
            self.assertFalse(path.exists())

    def test_doctor_reports_ffprobe(self):
        import subprocess
        ret = subprocess.run([sys.executable, str(SKILL/"scripts/character_fullbody.py"), "doctor"],
                             text=True, capture_output=True)
        self.assertEqual(ret.returncode, 0, ret.stderr)
        self.assertIn("ffprobe", json.loads(ret.stdout))

    def test_no_executable_shapes(self):
        bad = copy.deepcopy(self.scene)
        bad["actions"].append({"time":2.9,"kind":"exec","duration":0.1})
        with self.assertRaises(ValueError):
            b.prepare(bad,self.words)

if __name__=="__main__":
    unittest.main()
