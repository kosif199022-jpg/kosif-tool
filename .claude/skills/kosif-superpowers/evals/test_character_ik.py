"""Actual analytic IK, timing, pixel and audio-copy regression tests."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import character_ik as rig

SAMPLE=Path(__file__).resolve().parents[1]/"templates"/"ik-wave-demo.json"
WORDS=Path(__file__).resolve().parents[1]/"templates"/"ik-wave-words.json"

class CharacterIKTests(unittest.TestCase):
    def setUp(self):
        self.words=rig.words_from_file(WORDS)
        self.scene=json.loads(SAMPLE.read_text(encoding="utf-8"))
        self.p=rig.resolve(self.scene,self.words)

    def test_lengths_analytic_ik(self):
        arm=rig.solve_ik([320,310],[400,190],120,115,-1)
        a,b,c=arm["shoulder"],arm["elbow"],arm["wrist"]
        self.assertAlmostEqual(__import__("math").dist(a,b),120,places=4)
        self.assertAlmostEqual(__import__("math").dist(b,c),115,places=4)
        self.assertLess(arm["end_error"],.0001)
    def test_elbow_mirror(self):
        left=rig.solve_ik([320,310],[400,260],120,120,-1)
        right=rig.solve_ik([320,310],[400,260],120,120,1)
        self.assertNotEqual(left["elbow"],right["elbow"])
        self.assertEqual(left["wrist"],right["wrist"])
    def test_unreachable_far_clamps_not_fails(self):
        a=rig.solve_ik([320,310],[900,700],120,100)
        self.assertTrue(a["clamped"])
        self.assertAlmostEqual(__import__("math").dist(a["shoulder"],a["elbow"]),120,places=4)
        self.assertAlmostEqual(__import__("math").dist(a["elbow"],a["wrist"]),100,places=4)
    def test_unreachable_near_clamps(self):
        a=rig.solve_ik([320,310],[320,310],120,100)
        self.assertTrue(a["clamped"])
        self.assertGreater(a["end_error"],0)
    def test_malformed_ik_coordinates(self):
        with self.assertRaises(ValueError):rig.solve_ik([float("nan"),5],[10,10],40,40)
        with self.assertRaises(ValueError):rig.solve_ik([10,10],[20,30],40,40,2)
    def test_word_cue_exact_start_and_no_early_motion(self):
        self.assertEqual(self.p["cues"][1]["time"],.6)
        before=rig.target_at(self.p,.59)
        edge=rig.target_at(self.p,.6)
        after=rig.target_at(self.p,.8)
        self.assertEqual(before,edge)
        self.assertNotEqual(edge,after)
        self.assertNotEqual(before,rig.target_at(self.p,1.0))
    def test_zero_gap_between_targets_forbidden(self):
        s=json.loads(SAMPLE.read_text(encoding="utf8"))
        s["targets"].append({"time":.7,"point":[410,275],"travel":.2})
        with self.assertRaises(ValueError):rig.resolve(s,self.words)
    def test_unknown_word_rejected(self):
        s=json.loads(SAMPLE.read_text(encoding="utf8"))
        s["targets"][1]["word"]="not-said"
        with self.assertRaises(ValueError):rig.resolve(s,self.words)
    def test_first_target_requires_time_zero(self):
        s=json.loads(SAMPLE.read_text(encoding="utf8"))
        s["targets"][0]["time"]=.1
        with self.assertRaises(ValueError):rig.resolve(s,self.words)
    def test_invalid_words_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.json";p.write_text(json.dumps({"words":[{"word":"hi","start":1,"end":2},{"word":"hey","start":.1,"end":1}]}))
            with self.assertRaises(ValueError):rig.words_from_file(p)
    def test_figures_preserve_usable_paint_scene(self):
        for t in [0,.6,.9,1.5]:
            scene,arm=rig.figure(self.p,t)
            im=rig.paint(scene)
            self.assertEqual(im.size,(640,640))
            self.assertGreater(sum(im.convert("L").getextrema()),20)
            self.assertIn("wrist",arm)
    def test_raster_vector_export_and_existing_guard(self):
        with tempfile.TemporaryDirectory() as td:
            png=Path(td)/"photo.png";svg=Path(td)/"photo.svg"
            self.assertTrue(rig.export(self.p,png)["verified"])
            with Image.open(png) as im:im.verify()
            self.assertTrue(rig.export(self.p,svg,time=.9)["verified"])
            self.assertIn("<svg",svg.read_text(encoding="utf-8"))
            with self.assertRaises(ValueError):rig.export(self.p,png)
    def test_gif_timing_frame_count(self):
        with tempfile.TemporaryDirectory() as td:
            file=Path(td)/"s.gif";info=rig.export(self.p,file,fps=10)
            self.assertTrue(info["verified"])
            with Image.open(file) as im:
                self.assertGreater(im.n_frames,1)
                self.assertEqual(sum((im.seek(i) or im.info.get("duration",0)) for i in range(im.n_frames)),2000)
    def test_mp4_h264_and_exact_frames(self):
        if not shutil.which("ffmpeg"):self.skipTest("FFmpeg required")
        with tempfile.TemporaryDirectory() as td:
            file=Path(td)/"s.mp4";info=rig.export(self.p,file,fps=10)
            self.assertEqual(info["frames"],20)
            self.assertTrue(info["verified"])
            v=json.loads(subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
                "-show_entries","stream=codec_name,nb_frames","-of","json",str(file)],capture_output=True,check=True,text=True).stdout)
            self.assertEqual(v["streams"][0]["codec_name"],"h264")
            self.assertEqual(int(v["streams"][0]["nb_frames"]),20)
    def test_aac_packet_copy_verified(self):
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):self.skipTest("FFmpeg required")
        with tempfile.TemporaryDirectory() as td:
            src=Path(td)/"narration.m4a";out=Path(td)/"film.mp4"
            cmd=["ffmpeg","-v","error","-y","-f","lavfi","-i","sine=frequency=330:duration=2",
                 "-c:a","aac","-b:a","80k",str(src)]
            subprocess.run(cmd,check=True,capture_output=True)
            data=rig.export(self.p,out,fps=10,audio=src)
            self.assertTrue(data["audio_packet_copy_verified"])
            self.assertTrue(rig.packet_hashes(src))
            self.assertEqual(rig.packet_hashes(src),rig.packet_hashes(out))
    def test_reject_non_aac_audio(self):
        if not shutil.which("ffmpeg"):self.skipTest("FFmpeg required")
        with tempfile.TemporaryDirectory() as td:
            src=Path(td)/"narration.wav"
            subprocess.run(["ffmpeg","-v","error","-y","-f","lavfi","-i","sine=frequency=330:duration=2",str(src)],check=True,capture_output=True)
            with self.assertRaises(ValueError):rig.export(self.p,Path(td)/"no.mp4",fps=10,audio=src)
    def test_cli_with_word_file(self):
        with tempfile.TemporaryDirectory() as td:
            output=Path(td)/"ik.png"
            command=[sys.executable,str(Path(rig.__file__)),"render","--scene",str(SAMPLE),"--words",str(WORDS),
                     "--output",str(output),"--time","0.75"]
            ret=subprocess.run(command,text=True,capture_output=True)
            self.assertEqual(ret.returncode,0,ret.stderr)
            self.assertTrue(json.loads(ret.stdout)["verified"])
    def test_max_frame_guard(self):
        self.p["duration"]=30
        with self.assertRaises(ValueError):rig.export(self.p,"unused.mp4",fps=60)

if __name__=="__main__":unittest.main()
