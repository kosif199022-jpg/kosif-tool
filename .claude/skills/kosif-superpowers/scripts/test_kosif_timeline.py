"""Real FFmpeg tests for multi-track, time edits and immutable project revisions."""
import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw
from kosif_timeline import SCHEMA, edit, filters_and_inputs, render, step_history, validate


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"FFmpeg/FFprobe required")
class TimelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.td=tempfile.TemporaryDirectory(prefix="kosif-timeline-tests-")
        cls.d=Path(cls.td.name)
        cls.video=cls.d/"shot.mp4"
        cls.audio=cls.d/"music.wav"
        cls.overlay=cls.d/"art.png"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",
                        "-f","lavfi","-i","color=c=0x335577:s=320x180:r=10:d=2",
                        "-f","lavfi","-i","sine=frequency=440:sample_rate=44100:duration=2",
                        "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest",
                        str(cls.video)],check=True,timeout=40,capture_output=True)
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",
                        "-f","lavfi","-i","sine=frequency=700:sample_rate=44100:duration=2",
                        "-c:a","pcm_s16le",str(cls.audio)],check=True,timeout=40,capture_output=True)
        pic=Image.new("RGBA",(120,60),(50,175,155,140))
        ImageDraw.Draw(pic).rectangle((20,10,100,50),fill=(245,212,100,255))
        pic.save(cls.overlay)
        cls.project={
          "schema":SCHEMA,"width":320,"height":180,"fps":10,
          "duration":2,"background":"#182623",
          "tracks":[
            {"id":"picture","kind":"video","layer":0,
             "clips":[{"id":"v1","path":str(cls.video),"start":0,"in":0,
                       "duration":1.75,"fade_out":.2,"include_audio":True}]},
            {"id":"overlay","kind":"image","layer":3,
             "clips":[{"id":"g1","path":str(cls.overlay),"start":.25,"duration":1.5,
                       "width":120,"height":60,"x":5,"y":10,
                       "fade_in":.2,"fade_out":.2}]},
            {"id":"music","kind":"audio",
             "clips":[{"id":"a1","path":str(cls.audio),"start":0,"in":.2,
                       "duration":1.7,"volume":.25,"fade_in":.1}]}]}
        cls.original_sha={p:hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (cls.video,cls.audio,cls.overlay)}

    @classmethod
    def tearDownClass(cls):
        cls.td.cleanup()

    def test_clip_and_track_validation(self):
        plan=validate(self.project)
        self.assertEqual(len(plan["clips"]),3)
        self.assertEqual([x["kind"] for x in plan["clips"]],["video","image","audio"])

    def test_actual_h264_aac_multitrack_render(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"movie.mp4"
            receipt=render(self.project,out)
            self.assertTrue(receipt["verified"])
            self.assertEqual(receipt["frames"],20)
            self.assertEqual(receipt["video_layers"],2)
            self.assertEqual(receipt["audio_layers"],2)
            self.assertEqual(receipt["audio_codec"],"aac")
            self.assertEqual(receipt["video_codec"],"h264")
            self.assertTrue(out.stat().st_size>2000)
        for path,sha in self.original_sha.items():
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),sha)

    def test_real_silent_video_without_soundtrack(self):
        with tempfile.TemporaryDirectory() as d:
            project=copy.deepcopy(self.project)
            project["tracks"]=[project["tracks"][1]]
            with tempfile.TemporaryDirectory() as td:
                out=Path(td)/"silent.mp4"
                receipt=render(project,out)
                self.assertIsNone(receipt["audio_codec"])
                self.assertEqual(receipt["frames"],20)

    def test_overlap_alpha_transitions_graph(self):
        doc=copy.deepcopy(self.project)
        doc["tracks"][0]["clips"].append(
            {"id":"v2","path":str(self.video),"start":1.0,"in":0,"duration":1,
             "fade_in":.2})
        valid=validate(doc)
        args,graph,audio=filters_and_inputs(valid)
        self.assertIn("fade=t=out",graph)
        self.assertIn("fade=t=in",graph)
        self.assertIn("overlay=",graph)
        self.assertTrue(audio)

    def test_move_trim_fade_are_non_destructive(self):
        original=copy.deepcopy(self.project)
        moved=edit(original,"move","g1",{"start":.4})
        self.assertEqual(moved["tracks"][1]["clips"][0]["start"],.4)
        self.assertEqual(original["tracks"][1]["clips"][0]["start"],.25)
        trimmed=edit(moved,"trim","v1",{"in":.1,"duration":1.5})
        self.assertEqual(trimmed["tracks"][0]["clips"][0]["in"],.1)
        faded=edit(trimmed,"fade","v1",{"fade_out":.3})
        self.assertEqual(faded["tracks"][0]["clips"][0]["fade_out"],.3)
        self.assertEqual(len(faded["history"]["past"]),3)

    def test_undo_redo_reversibility(self):
        moved=edit(self.project,"move","g1",{"start":.4})
        restored=step_history(moved,"undo")
        self.assertEqual(restored["tracks"],self.project["tracks"])
        redone=step_history(restored,"redo")
        self.assertEqual(redone["tracks"],moved["tracks"])
        self.assertEqual(len(redone["history"]["past"]),1)
        with self.assertRaisesRegex(ValueError,"no redo"):
            step_history(redone,"redo")

    def test_undo_without_prior_edits_fails(self):
        with self.assertRaisesRegex(ValueError,"no edit history"):
            step_history(self.project,"undo")

    def test_overwrite_protection(self):
        with self.assertRaisesRegex(ValueError,"new MP4"):
            render(self.project,self.video)
        self.assertEqual(self.original_sha[self.video],
                         hashlib.sha256(self.video.read_bytes()).hexdigest())

    def test_forbid_missing_source_and_unsupported_type(self):
        doc=copy.deepcopy(self.project)
        doc["tracks"][0]["clips"][0]["path"]=str(self.d/"missing.mp4")
        with self.assertRaisesRegex(ValueError,"missing"):
            validate(doc)
        doc["tracks"][0]["clips"][0]["path"]=str(self.audio)
        with self.assertRaisesRegex(ValueError,"unsupported"):
            validate(doc)

    def test_audio_no_stream_rejected(self):
        doc=copy.deepcopy(self.project)
        doc["tracks"][2]["clips"][0]["path"]=str(self.audio)
        doc["tracks"][0]["clips"][0]["path"]=str(self.video)
        doc["tracks"][0]["clips"][0]["include_audio"]=False
        validate(doc)
        doc["tracks"][2]["clips"][0]["path"]=str(self.d/"bad.wav")
        with self.assertRaisesRegex(ValueError,"missing"):
            validate(doc)

    def test_out_of_range_source_trim_rejected(self):
        doc=copy.deepcopy(self.project)
        doc["tracks"][0]["clips"][0]["in"]=1.9
        with self.assertRaisesRegex(ValueError,"source duration"):
            validate(doc)

    def test_overlap_without_a_track_prohibited(self):
        doc=copy.deepcopy(self.project)
        doc["tracks"][0]["clips"][0]["duration"]=2.1
        with self.assertRaisesRegex(ValueError,"timeline"):
            validate(doc)

    def test_9_16_dimensions_supported(self):
        doc=copy.deepcopy(self.project)
        doc["width"]=1080
        doc["height"]=1920
        doc["fps"]=12
        doc["duration"]=2
        self.assertEqual(validate(doc,do_probe=False)["height"],1920)

    def test_pixel_budget_bounded(self):
        doc=copy.deepcopy(self.project)
        doc.update(width=1920,height=1920,fps=30,duration=10)
        with self.assertRaisesRegex(ValueError,"pixel-frame budget"):
            validate(doc,do_probe=False)

    def test_prevent_invalid_ids_and_excess_tracks(self):
        doc=copy.deepcopy(self.project)
        doc["tracks"][1]["id"]="picture"
        with self.assertRaisesRegex(ValueError,"track ids"):
            validate(doc,do_probe=False)
        doc=copy.deepcopy(self.project)
        doc["tracks"]=doc["tracks"]*5
        with self.assertRaisesRegex(ValueError,"tracks must"):
            validate(doc,do_probe=False)

    def test_no_shell_interpolation_in_source_paths(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/"quote's audio.wav"
            src.write_bytes(self.audio.read_bytes())
            doc=copy.deepcopy(self.project)
            doc["tracks"][2]["clips"][0]["path"]=str(src)
            plan=validate(doc)
            args,_,_=filters_and_inputs(plan)
            self.assertIn(str(src),args)
            self.assertNotIn("cmd.exe",args)

    def test_history_bounded_to_last_ten(self):
        data=copy.deepcopy(self.project)
        for i in range(13):
            data=edit(data,"move","g1",{"start":.25+i*.01})
        self.assertEqual(len(data["history"]["past"]),10)


if __name__=="__main__":
    unittest.main(verbosity=2)
