"""Test original photo processing + Unified Draw compositing and video exports."""
import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageChops, ImageDraw
from unified_media import checked_image, compose, export, validate_job
from unified_draw import compile_scene

# the "develop" photo effect runs App Studio, which needs OpenCV (opencv-python-headless)
HAVE_CV2=importlib.util.find_spec("cv2") is not None
SCENE=Path(__file__).resolve().parent.parent/"templates"/"unified-draw-motion-demo.json"


def fixture(folder):
    photo=Path(folder)/"source.png"
    image=Image.new("RGB",(640,480),(20,80,120))
    art=ImageDraw.Draw(image)
    art.rectangle((0,0,90,90),fill=(160,30,20))
    art.ellipse((300,320,400,420),fill=(30,175,100))
    image.save(photo)
    doc=json.loads(SCENE.read_text(encoding="utf8"))
    return photo,doc


class MediaIntegration(unittest.TestCase):
    def test_composite_uses_photo_and_drawing(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            scene,_=compile_scene(doc)
            result=compose(checked_image(photo),scene,0)
            self.assertEqual(result.size,(640,480))
            self.assertEqual(result.getpixel((0,0)),(160,30,20))
            self.assertNotEqual(result.getpixel((390,80)),(20,80,120))

    def test_stills_differ_after_keyframes(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            scene,_=compile_scene(doc)
            a=compose(checked_image(photo),scene,0)
            b=compose(checked_image(photo),scene,1.5)
            self.assertIsNotNone(ImageChops.difference(a,b).getbbox())

    def test_raster_output_has_proof_hash(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            output=Path(d)/"output.png"
            receipt=export(photo,doc,output)
            self.assertTrue(receipt["verified"])
            self.assertEqual(receipt["frames"],1)
            with Image.open(output) as img:
                self.assertEqual(img.size,(640,480))
            self.assertEqual(len(receipt["sha256"]),64)

    @unittest.skipUnless(HAVE_CV2,"OpenCV (cv2) required for the App Studio develop effect")
    def test_edited_photo_pipeline_develop(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            out=Path(d)/"developed.png"
            receipt=export(photo,doc,out,effect="develop",exposure=0.5)
            self.assertTrue(receipt["verified"])
            self.assertEqual(receipt["photo_effect"],"develop")
            with Image.open(out) as img:
                self.assertEqual(img.size,(640,480))

    def test_gif_animation(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            output=Path(d)/"animated.gif"
            receipt=export(photo,doc,output,fps=8,duration=1)
            self.assertEqual(receipt["frames"],8)
            with Image.open(output) as gif:
                self.assertGreater(gif.n_frames,1)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"ffmpeg required")
    def test_h264_mp4_animation(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            output=Path(d)/"animated.mp4"
            receipt=export(photo,doc,output,fps=8,duration=1)
            self.assertTrue(receipt["verified"])
            info=json.loads(subprocess.check_output([
                "ffprobe","-v","error","-select_streams","v:0",
                "-show_entries","stream=codec_name,nb_frames,width,height",
                "-of","json",str(output)],text=True))
            stream=info["streams"][0]
            self.assertEqual(stream["codec_name"],"h264")
            self.assertEqual(int(stream["nb_frames"]),8)
            self.assertEqual((stream["width"],stream["height"]),(640,480))

    def test_refuses_overwriting_and_untrusted_formats(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            output=Path(d)/"keep.png"
            output.write_bytes(b"UNCHANGED")
            with self.assertRaisesRegex(ValueError,"overwrite"):
                export(photo,doc,output)
            self.assertEqual(output.read_bytes(),b"UNCHANGED")
            with self.assertRaisesRegex(ValueError,"local JPG"):
                validate_job(Path(d)/"unknown.exe",doc,Path(d)/"out.png")

    def test_no_command_execution_in_photo_effect(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            with self.assertRaisesRegex(ValueError,"unsupported"):
                export(photo,doc,Path(d)/"bad.png",effect="run-any-command")
            with self.assertRaisesRegex(ValueError,"exposure"):
                export(photo,doc,Path(d)/"bad.png",effect="develop",exposure=99)

    def test_missing_ffmpeg_and_max_frames(self):
        with tempfile.TemporaryDirectory() as d:
            photo,doc=fixture(d)
            with self.assertRaisesRegex(ValueError,"300 frame"):
                export(photo,doc,Path(d)/"large.gif",fps=60,duration=10)
            with patch("unified_media.shutil.which",return_value=None):
                with self.assertRaisesRegex(ValueError,"FFmpeg"):
                    export(photo,doc,Path(d)/"mp4.mp4",fps=8,duration=1)


if __name__=="__main__":
    unittest.main(verbosity=2)
