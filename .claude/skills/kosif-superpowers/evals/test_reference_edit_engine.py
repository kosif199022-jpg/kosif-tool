"""Regression gates for real KOSIF Reference Edit Engine -> editable Remotion files."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

DIR=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(DIR))
import reference_edit_engine as r


def sample(cuts=(1.0,2.0,3.5),duration=5):
    return {"status":"reference_timing_observed_not_animation_reconstructed",
      "duration_seconds":duration,"cut_candidates_seconds":list(cuts),
      "cut_detection_run":True,"audio_present":True,"segments":[]}


def cues(duration=5,words=None,onsets=None):
    return {"schema":"kosif.audio-cues.v1","duration":duration,
      "words":words or [],"onset_candidates_seconds":onsets or [0.5,1.7,3.8]}


class ReferenceEditEngineTests(unittest.TestCase):
    def test_reference_to_editable_remotion_project(self):
        edit=r.plan(sample(),cues())
        self.assertEqual(edit["totalFrames"],150)
        self.assertEqual(len(edit["shots"]),4)
        self.assertEqual(sum(x["frames"] for x in edit["shots"]),150)
        self.assertTrue(all(x["frames"]>=1 for x in edit["shots"]))
        self.assertTrue(edit["evidence"]["referenceVideoPixelsCopied"] is False)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"remotion"
            report=r.create_project(p,edit)
            self.assertEqual(report["status"],"editable_project_created_unrendered")
            self.assertTrue((p/"src"/"Video.jsx").is_file())
            self.assertEqual(json.loads((p/"src"/"plan.json").read_text())["shots"],edit["shots"])
            source=(p/"src"/"Video.jsx").read_text()
            for symbol in ("OffthreadVideo","Sequence","AbsoluteFill","useCurrentFrame","Audio","staticFile"):
                self.assertIn(symbol,source)
            self.assertEqual(json.loads((p/"package.json").read_text())["dependencies"]["remotion"],"^4.0.0")

    def test_audio_is_master_clock_and_cut_pacing_scales(self):
        edit=r.plan(sample(duration=5),cues(duration=10))
        self.assertEqual(edit["totalFrames"],300)
        self.assertEqual([s["startFrame"] for s in edit["shots"]],[0,60,120,210])
        self.assertEqual(edit["evidence"]["scaleFactor"],2)

    def test_words_crossing_cut_are_not_split(self):
        edit=r.plan(sample(cuts=(2.0,),duration=5),cues(words=[
            {"text":"أول","start":0.1,"end":0.4},
            {"text":"كلمة","start":1.9,"end":2.25},
            {"text":"ثاني","start":2.5,"end":3.0}]))
        self.assertIn(edit["shots"][1]["startFrame"],[57,68])
        self.assertNotEqual(edit["shots"][1]["startFrame"],60)
        self.assertEqual(edit["evidence"]["alignedWordCount"],3)

    def test_too_long_word_across_cut_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"word"):
            r.plan(sample(cuts=(2,),duration=5),cues(words=[
                {"text":"طويل","start":1.0,"end":3.0}]))

    def test_no_fabricated_transcript_or_emotion(self):
        edit=r.plan(sample(),cues())
        self.assertFalse(edit["evidence"]["semanticUnderstanding"])
        self.assertTrue(edit["evidence"]["onsetCandidatesNotVerifiedBeats"])
        self.assertTrue(all(shot["caption"].startswith("مشهد") for shot in edit["shots"]))
        self.assertEqual(edit,r.plan(sample(),cues()))

    def test_bad_cut_input_rejected(self):
        for cuts in [(1.0,1.0),(2.3,1.8),(-0.1,),(6,),tuple(i*.05 for i in range(81))]:
            with self.subTest(cuts=cuts),self.assertRaises(ValueError):
                r.plan(sample(cuts=cuts))

    def test_nan_cues_and_word_overlap_rejected(self):
        with self.assertRaises(ValueError):r.plan(sample(),cues(duration=float("nan")))
        with self.assertRaises(ValueError):r.plan(sample(),cues(words=[
            {"text":"one","start":0.1,"end":2},
            {"text":"two","start":1,"end":3}]))
        with self.assertRaises(ValueError):r.plan(sample(),cues(onsets=[2.0,1.2]))

    def test_safe_asset_copy_exactly_user_owned(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);root=base/"user-assets";root.mkdir()
            for name in ("A.mp4","B.mp4","C.mp4","D.mp4","voice.wav"):
                (root/name).write_bytes(b"content-"+name.encode())
            edit=r.plan(sample(),cues())
            out=base/"edit"
            result=r.create_project(out,edit,{"clips":["A.mp4","B.mp4","C.mp4","D.mp4"],"audio":"voice.wav"},root)
            self.assertEqual(result["assets_copied"],5)
            plan=json.loads((out/"src"/"plan.json").read_text())
            self.assertEqual(plan["audio"],"audio.wav")
            self.assertEqual(plan["shots"][0]["asset"],"clip_000.mp4")
            self.assertEqual((out/"public/assets/clip_000.mp4").read_bytes(),(root/"A.mp4").read_bytes())
            self.assertTrue((root/"A.mp4").is_file())
            with self.assertRaises(ValueError):r.create_project(out,edit)

    def test_reject_path_traversal_and_symlinks(self):
        for name in ("../private.mp4","foo/bar.mp4","/tmp/hidden.mp4","token.env",".secret.mp4"):
            with self.subTest(name=name),self.assertRaises(ValueError):r.basename(name,r.ASSET_EXTS)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);src=p/"assets";src.mkdir()
            (src/"real.mp4").write_bytes(b"abc")
            (src/"linked.mp4").symlink_to(src/"real.mp4")
            with self.assertRaises(ValueError):
                r.create_project(p/"new",r.plan(sample(cuts=(),duration=5)),{"clips":["linked.mp4"]},src)
            self.assertFalse((p/"new").exists())

    def test_invalid_manifest_leaves_destination_absent(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);assets=p/"clips";assets.mkdir()
            (assets/"x.mp4").write_bytes(b"owned")
            edit=r.plan(sample())
            for bad in ({"clips":["x.mp4"]},{"clips":["x.exe"]},{"audio":"../../secret.mp3"}):
                with self.subTest(manifest=bad),self.assertRaises(ValueError):
                    r.create_project(p/"new",edit,bad,assets)
                self.assertFalse((p/"new").exists())

    def test_reject_false_probe_status(self):
        x=sample();x["status"]="reference_timing_observed_not_animation_reconstructed__fake"
        with self.assertRaises(ValueError):r.plan(x)

    @unittest.skipUnless(__import__("shutil").which("ffmpeg") and __import__("shutil").which("ffprobe"), "needs ffmpeg/ffprobe")
    def test_replacement_audio_must_match_the_timeline(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            for secs in (2,6):
                subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i",f"sine=f=440:d={secs}",str(d/f"v{secs}.wav")],check=True)
            edit={"fps":30,"duration":6.0,"totalFrames":180}
            with self.assertRaises(ValueError):r.check_audio_length(d/"v2.wav",edit)
            self.assertTrue(r.check_audio_length(d/"v6.wav",edit)["lengthVerified"])
            (d/"fake.wav").write_bytes(b"not audio")
            self.assertFalse(r.check_audio_length(d/"fake.wav",edit)["lengthVerified"])


if __name__=="__main__":unittest.main()
