"""KOSIF Visual Fingerprint actual pixel measurement and transfer safety tests."""
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

DIR=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(DIR))
import reference_visual_fingerprint as v


def frame(rgb=(70,130,110)):
    return bytes(rgb)*(v.W*v.H)


def grid(offset=0):
    # Textured deterministic pattern with controlled translation. Non-random.
    rows=[]
    for y in range(v.H):
        for x in range(v.W):
            sx=x-offset
            k=((sx*79)^(y*173)^((sx*y)%59*33))&255
            rows.extend([k,(k*3)%256,(k*7)%256])
    return bytes(rows)


class VisualFingerprintTests(unittest.TestCase):
    def test_observes_known_rgb_and_low_contrast(self):
        x=v.frame_features(frame((240,32,64)))
        self.assertEqual(x["mean_rgb"],[240,32,64])
        self.assertLess(x["contrast"],0.001)
        self.assertGreater(x["saturation_proxy"],0.7)
        self.assertEqual(len(x["palette"]),1)

    def test_reject_malformed_frame(self):
        with self.assertRaises(ValueError):
            v.frame_features(b"bad")

    def test_visual_segments_and_sample_timestamps(self):
        x=v.fingerprints([frame((220,50,50)),frame((20,20,20)),
                          frame((20,140,140)),frame((240,240,240))],2,[1])
        self.assertEqual(x["schema"],"kosif.reference-visual-fingerprint.v1")
        self.assertEqual(x["sample_count"],4)
        self.assertEqual(len(x["sections"]),2)
        self.assertEqual([a["sample_count"] for a in x["sections"]],[2,2])
        self.assertTrue(x["source_video_unchanged"])
        self.assertIn("change_ratio",x["samples"][1])
        self.assertGreater(x["samples"][1]["change_ratio"],0.1)

    def test_segment_under_half_second_gets_nearest_sample(self):
        x=v.fingerprints([frame()],.3,[.12])
        self.assertEqual(len(x["sections"]),2)
        self.assertEqual([x["sample_count"] for x in x["sections"]],[1,1])

    def test_reject_cut_unsorted_and_out_of_range(self):
        for cuts in ((1.1,.7),(-1,),(2,),(.0,)):
            with self.subTest(cuts=cuts),self.assertRaises(ValueError):
                v.fingerprints([frame(),frame(),frame(),frame()],2,cuts)

    def test_coarse_motion_is_not_claimed_camera_tracking(self):
        x=v.fingerprints([grid(0),grid(2),grid(4),grid(6)],2,[])
        section=x["sections"][0]
        self.assertIn(section["possible_translation"],
                      ["horizontal_candidate","vertical_candidate","none"])
        self.assertIn("not verified camera motion",str(x["samples"]))
        self.assertIn("no object/face tracking",x["exclusions"])

    def test_flat_color_has_insufficient_motion_evidence(self):
        x=v.fingerprints([frame((10,10,10)),frame((10,10,10))],1)
        self.assertEqual(x["samples"][1]["translation"]["evidence"],
                         "insufficient texture/change")
        self.assertEqual(x["sections"][0]["possible_translation"],"none")

    def test_input_duration_bounds(self):
        for sec in (0,121,float("nan"),float("inf")):
            with self.subTest(sec=sec),self.assertRaises(ValueError):
                v.fingerprints([frame()],sec)

    def test_subprocess_decodes_fixed_size_frames_without_install(self):
        raw=frame((10,20,30))*3
        with patch.object(v.shutil,"which",return_value="/usr/bin/ffmpeg"),\
             patch.object(v.subprocess,"run",return_value=SimpleNamespace(
                 returncode=0,stdout=raw,stderr=b"")) as run:
            images=v.read_frames(Path("/tmp/local.mp4"),2)
        self.assertEqual(len(images),3)
        args=run.call_args.args[0]
        self.assertIn("fps=2,scale=64:36:flags=bilinear,format=rgb24",args)
        self.assertNotIn("http://",str(args))
        self.assertFalse(run.call_args.kwargs.get("shell",False))

    def test_decoder_rejects_partial_frame(self):
        with patch.object(v.shutil,"which",return_value="ffmpeg"),\
             patch.object(v.subprocess,"run",return_value=SimpleNamespace(
                 returncode=0,stdout=b"\x10\x20\x30",stderr=b"")):
            with self.assertRaises(ValueError):
                v.read_frames(Path("/tmp/local.mp4"),1)

    def test_analyze_fails_on_probe_duration_mismatch(self):
        with tempfile.TemporaryDirectory() as root:
            movie=Path(root)/"user.mp4"
            movie.write_bytes(b"fake")
            cut=Path(root)/"cut.json"
            cut.write_text(json.dumps({"status":"reference_timing_observed_not_animation_reconstructed",
                                       "duration_seconds":14,"cut_detection_run":True,
                                       "cut_candidates_seconds":[2]}))
            with patch.object(v,"probe_video",return_value={"duration_seconds":3}):
                with self.assertRaises(ValueError):
                    v.analyze(movie,cut)

    def test_analyze_calls_video_probe_and_actual_decoder(self):
        with tempfile.TemporaryDirectory() as root:
            movie=Path(root)/"user.mp4";movie.write_bytes(b"fake")
            cut=Path(root)/"cut.json"
            cut.write_text(json.dumps({"status":"reference_timing_observed_not_animation_reconstructed",
                                       "duration_seconds":2,"cut_detection_run":True,
                                       "cut_candidates_seconds":[1]}))
            with patch.object(v,"probe_video",return_value={"duration_seconds":2}) as p,\
                 patch.object(v,"read_frames",return_value=[frame()]*4) as d:
                result=v.analyze(movie,cut)
            self.assertEqual(len(result["sections"]),2)
            p.assert_called_once()
            d.assert_called_once()
            self.assertFalse(result["cut_report_provided"] is False)
            self.assertEqual(result["source_name"],"user.mp4")


if __name__=="__main__":
    unittest.main()
