import importlib.util
import tempfile
import unittest
import json
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
SRC=HERE/".claude"/"skills"/"kosif-superpowers"/"scripts"/"cinematic_cut_planner.py"
spec=importlib.util.spec_from_file_location("cinematic_cut_planner",SRC)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

WORDS=[{"word":"مكة","start":0.2,"end":0.7,"emphasis":True},
       {"word":"المكرمة","start":0.72,"end":1.14},
       {"word":"مدينة","start":2.0,"end":2.5},
       {"word":"مقدسة","start":2.51,"end":3.4}]
def footage(id="a", **kw):
    data={"id":id,"path":"local-footage.mp4","duration":5.0,"width":3840,"height":2160,
          "license_verified":True,"reviewed_frames":3,"contains_text":False,
          "contains_excluded_people":False,"is_moving_video":True,
          "tags":["مكة","المكرمة","مدينة","مقدسة"]}
    data.update(kw)
    return data

class TestCinematicCutPlanner(unittest.TestCase):
    def test_complete_frame_cover_and_locked_audio(self):
        result=m.build(WORDS,[footage()],4.0)
        self.assertTrue(result["production_ready"])
        self.assertEqual(result["video"]["frame_count"],120)
        self.assertEqual(result["scenes"][0]["start_frame"],0)
        self.assertEqual(result["scenes"][-1]["end_frame_exclusive"],120)
        self.assertTrue(result["audio"]["preserve_original"])
        self.assertFalse(result["audio"]["audio_editing_allowed"])
    def test_speech_pause_splits(self):
        result=m.build(WORDS,[footage()],4.0)
        self.assertEqual(len(result["scenes"]),2)
        self.assertEqual(result["scenes"][0]["end_frame_exclusive"],60)
        self.assertEqual(result["scenes"][1]["start_frame"],60)
    def test_rejects_unverified_rights(self):
        result=m.build(WORDS,[footage(license_verified=False)],4.0)
        self.assertFalse(result["production_ready"])
        self.assertEqual(len(result["rejected_clips"]),1)
        self.assertEqual(len(result["blockers"]),2)
    def test_rejects_unreviewed_or_existing_text(self):
        for kw in ({"reviewed_frames":2},{"contains_text":True},
                   {"contains_excluded_people":True},{"is_moving_video":False}):
            self.assertFalse(m.build(WORDS,[footage(**kw)],4.0)["production_ready"])
    def test_rejects_incomplete_metadata(self):
        f=footage()
        del f["contains_excluded_people"]
        self.assertFalse(m.build(WORDS,[f],4.0)["production_ready"])
    def test_rejects_too_short_clip(self):
        self.assertFalse(m.build(WORDS,[footage(duration=.5)],4.0)["production_ready"])
    def test_malformed_word_timing(self):
        with self.assertRaises(ValueError):
            m.build([{"word":"x","start":2,"end":1}],[footage()],4)
    def test_repeatable_camera_plan(self):
        a=m.build(WORDS,[footage()],4)
        b=m.build(WORDS,[footage()],4)
        self.assertEqual(a,b)
        self.assertEqual(a["scenes"][0]["camera"]["move"],"slow_push_in")
    def test_rights_flag_must_be_real_boolean(self):
        self.assertFalse(m.build(WORDS,[footage(license_verified="yes")],4.0)["production_ready"])
    def test_unrelated_footage_never_auto_selected(self):
        self.assertFalse(m.build(WORDS,[footage(tags=["cars","roads","vehicles"])],4.0)["production_ready"])
    def test_text_based_relevance(self):
        result=m.build(WORDS,[footage("wrong",tags=["cars"]),footage("right")],4.0)
        self.assertEqual(result["scenes"][0]["footage_id"],"right")

if __name__=="__main__": unittest.main()
