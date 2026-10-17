"""Integration of measured reference frame color with the actual editable KOSIF Remotion project."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

DIR=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(DIR))
import reference_visual_fingerprint as vf
import reference_edit_engine as edit


def reference(duration=2,cuts=None):
    return {"status":"reference_timing_observed_not_animation_reconstructed",
            "duration_seconds":duration,"cut_candidates_seconds":cuts or [1],
            "cut_detection_run":True,"audio_present":True,"segments":[]}


def fingerprint():
    return vf.fingerprints([
        bytes((235,120,35))*(vf.W*vf.H),
        bytes((235,120,35))*(vf.W*vf.H),
        bytes((12,18,55))*(vf.W*vf.H),
        bytes((12,18,55))*(vf.W*vf.H)
    ],2,[1])


class VisualStyleTransferTests(unittest.TestCase):
    def test_measured_palette_applied_to_editable_project(self):
        base=edit.plan(reference())
        edit.apply_visual_fingerprint(base,fingerprint())
        self.assertEqual(len(base["shots"]),2)
        self.assertTrue(all("style" in shot for shot in base["shots"]))
        self.assertNotEqual(base["shots"][0]["style"]["background"],
                            base["shots"][1]["style"]["background"])
        self.assertFalse(base["evidence"]["referenceVideoPixelsCopied"])
        self.assertFalse(base["evidence"]["visualSourcePixelsCopied"])
        self.assertFalse(base["evidence"]["objectTrackingVerified"])
        with tempfile.TemporaryDirectory() as td:
            result=edit.create_project(Path(td)/"new-remotion",base)
            self.assertEqual(result["status"],"editable_project_created_unrendered")
            source=(Path(td)/"new-remotion"/"src"/"Video.jsx").read_text(encoding="utf-8")
            self.assertIn("shot.style?.background",source)
            self.assertIn("shot.style?.accent",source)
            documented=json.loads((Path(td)/"new-remotion"/"src"/"plan.json").read_text())
            self.assertEqual(documented["shots"][0]["style"],base["shots"][0]["style"])

    def test_color_ink_legibility_follows_background(self):
        base=edit.plan(reference())
        edit.apply_visual_fingerprint(base,fingerprint())
        bg=[shot["style"]["background"] for shot in base["shots"]]
        ink=[shot["style"]["ink"] for shot in base["shots"]]
        self.assertEqual(len(ink),2)
        self.assertTrue(all(s in ("#172824","#f4f0e6") for s in ink))
        self.assertNotEqual(bg[0],bg[1])

    def test_untrusted_visual_source_is_rejected(self):
        visual=fingerprint()
        visual["schema"]="source_video_pixels_copied"
        with self.assertRaises(ValueError):
            edit.apply_visual_fingerprint(edit.plan(reference()),visual)

    def test_duration_mismatch_rejected(self):
        visual=fingerprint();visual["duration"]=1.0
        with self.assertRaises(ValueError):
            edit.apply_visual_fingerprint(edit.plan(reference()),visual)

    def test_injected_style_rejected_before_video_template(self):
        visual=fingerprint()
        visual["sections"][0]["palette"]=['#121212"; window.alert(1)']
        with self.assertRaises(ValueError):
            edit.apply_visual_fingerprint(edit.plan(reference()),visual)

    def test_missing_section_range_rejected(self):
        visual=fingerprint()
        visual["sections"][0]["end"]=.45
        with self.assertRaises(ValueError):
            edit.apply_visual_fingerprint(edit.plan(reference()),visual)

    def test_no_compulsory_visual_data_keeps_previous_workflow(self):
        base=edit.plan(reference())
        self.assertFalse(any("style" in shot for shot in base["shots"]))
        self.assertEqual(base["totalFrames"],60)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                         "Real local ffmpeg integration requires installed ffmpeg/ffprobe")
    def test_real_encoded_video_is_measured_without_copying_frames(self):
        # An independently generated synthetic clip is fed through actual
        # ffprobe/ffmpeg, not faked Python outputs or external video assets.
        with tempfile.TemporaryDirectory() as td:
            clip=Path(td)/"synthetic.mp4"
            create=subprocess.run(["ffmpeg","-nostdin","-v","error",
                                   "-f","lavfi","-i","color=c=red:s=64x36:d=1:r=2",
                                   "-c:v","mpeg4","-q:v","3",str(clip)],
                                  stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                  timeout=25,check=False)
            self.assertEqual(create.returncode,0,create.stderr[:300])
            result=vf.analyze(clip)
            self.assertEqual(result["schema"],"kosif.reference-visual-fingerprint.v1")
            self.assertGreaterEqual(result["sample_count"],1)
            self.assertEqual(result["source_name"],"synthetic.mp4")
            self.assertTrue(result["source_video_unchanged"])
            self.assertGreater(result["samples"][0]["mean_rgb"][0],
                               result["samples"][0]["mean_rgb"][1])


if __name__=="__main__":
    unittest.main()
