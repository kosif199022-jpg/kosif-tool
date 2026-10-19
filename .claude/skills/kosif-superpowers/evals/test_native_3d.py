"""KOSIF independent software 3D smoke/regression tests."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from PIL import ImageChops
SK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/"scripts"))
import native_3d as n
EXAMPLE=SK/"templates/native-3d-demo.json"

class Native3D(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads(EXAMPLE.read_text(encoding="utf-8-sig"))
    def test_valid_scene_and_real_pixels(self):
        n.validate(self.s)
        a=n.render(self.s,1)
        self.assertEqual(a.size,(640,360))
        self.assertGreater(len(a.getcolors(640*360)),2)
    def test_animated_objects_change_pixels(self):
        a=n.render(self.s,1)
        b=n.render(self.s,120)
        self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
    def test_pose_interpolates(self):
        p,y=n.pose(self.s["objects"][0],60)
        self.assertGreater(p[0],-1.8)
        self.assertLess(p[0],0)
        self.assertGreater(y,0)
    def test_bad_data_refused(self):
        trials=[{"width":True},{"width":10000},{"objects":[]},
                {"objects":[{"shape":"exec"}]},
                {"objects":[{"shape":"cube","color":"#FFFFFF","scale":[0,1,1]}]},
                {"objects":[{"shape":"cube","location":[float("inf"),0,0]}]},
                {"objects":[{"shape":"cube","keyframes":[
                    {"frame":5,"location":[0,0,0]},{"frame":2,"location":[0,0,0]}]}]}]
        for change in trials:
            with self.subTest(change=str(change)[:60]):
                with self.assertRaises(ValueError):n.validate({**self.s,**change})
    def test_no_import_blender(self):
        txt=(SK/"scripts/native_3d.py").read_text(encoding="utf-8-sig")
        self.assertNotIn("import bpy",txt)
        self.assertNotIn("blender.exe",txt)
    def test_png_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"one.png"
            self.assertEqual(n.export(self.s,out)["frames"],1)
            with self.assertRaisesRegex(ValueError,"overwrite"): n.export(self.s,out)
    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"FFmpeg missing")
    def test_animated_h264_24_frames(self):
        s=copy.deepcopy(self.s)
        s["frames"]=24
        s["fps"]=12
        for x in s["objects"]:
            x["keyframes"]=[k for k in x.get("keyframes",[]) if k["frame"]<=24]
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"two-sec.mp4"
            result=n.export(s,out)
            self.assertFalse(result["uses_blender"])
            self.assertEqual(result["frames"],24)
            data=json.loads(subprocess.check_output(
                ["ffprobe","-v","error","-count_frames","-select_streams","v:0",
                 "-show_entries","stream=codec_name,nb_read_frames",
                 "-of","json",str(out)]))
            self.assertEqual(data["streams"][0]["codec_name"],"h264")
            self.assertEqual(data["streams"][0]["nb_read_frames"],"24")
if __name__=="__main__": unittest.main()
