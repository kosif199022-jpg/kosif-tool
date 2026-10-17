"""Reference video inspection guards and evidence parsing without running user media."""
import importlib.util
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"motion_reference_probe.py"
spec=importlib.util.spec_from_file_location("motion_reference_probe",SCRIPT)
probe=importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class ProbeTests(unittest.TestCase):
    def test_parse_cut_candidates_deduplicates_close_frames(self):
        stderr="pts_time:0.10\npts_time:1.00\npts_time:1.03\npts_time:3.0\npts_time:9.96\n"
        self.assertEqual(probe.parse_cuts(stderr,10),[1.0,3.0])

    def test_missing_file_blocked(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                probe.probe(Path(root)/"not-here.mp4")

    def test_bounded_file_size(self):
        with tempfile.TemporaryDirectory() as root:
            target=Path(root)/"large.mp4"
            with target.open("wb") as f:
                f.truncate(probe.MAX_BYTES+1)
            with self.assertRaises(ValueError):
                probe.probe(target)

    def test_reports_metadata_without_claiming_visual_reconstruction(self):
        meta={"streams":[{"codec_type":"video","width":1080,"height":1920,"avg_frame_rate":"30/1"},
                         {"codec_type":"audio"}],"format":{"duration":"9.0"}}
        with tempfile.TemporaryDirectory() as root:
            sample=Path(root)/"clip.mp4"
            sample.write_bytes(b"fake")
            fake=SimpleNamespace(returncode=0,stdout=json.dumps(meta),stderr="")
            with patch.object(probe.shutil,"which",return_value="/usr/bin/ffprobe"), \
                 patch.object(probe,"cmd",return_value=fake) as run:
                result=probe.probe(sample)
            self.assertEqual(result["duration_seconds"],9)
            self.assertTrue(result["audio_present"])
            self.assertFalse(result["cut_detection_run"])
            self.assertIn("not_animation_reconstructed",result["status"])
            run.assert_called_once()

    def test_scene_detection_calls_real_ffmpeg_only_when_opted_in(self):
        meta={"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"9.0"}}
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/"clip.mp4"
            path.write_bytes(b"fake")
            answers=[SimpleNamespace(returncode=0,stdout=json.dumps(meta),stderr=""),
                     SimpleNamespace(returncode=0,stdout="",stderr="pts_time: 1.5\npts_time: 4.2\n")]
            with patch.object(probe.shutil,"which",return_value="/usr/bin/ffmpeg"), \
                 patch.object(probe,"cmd",side_effect=answers) as cmd:
                info=probe.probe(path,detect_cuts=True)
            self.assertEqual(info["cut_candidates_seconds"],[1.5,4.2])
            self.assertEqual(len(info["segments"]),3)
            self.assertEqual(cmd.call_count,2)

    def test_invalid_threshold(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/"clip.mp4"
            path.write_bytes(b"fake")
            with patch.object(probe.shutil,"which",return_value="/usr/bin/ffprobe"):
                for bad in (-1,0,1,2):
                    with self.subTest(bad=bad),self.assertRaises(ValueError):
                        probe.probe(path,threshold=bad)


if __name__=="__main__":
    unittest.main()
