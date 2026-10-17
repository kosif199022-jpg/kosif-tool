"""Audio rhythm hypotheses and actual Remotion motion-cue integration tests."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

S=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(S))
import music_rhythm_engine as music
import reference_edit_engine as edit


def cues(events=None):
    events=events if events is not None else [0.25,0.75,1.25,1.75,2.25,2.75]
    return {"schema":"kosif.audio-cues.v1","source":"measured.wav","duration":3.0,
            "onset_candidates_seconds":events,"words":[],
            "window_seconds":0.1,
            "energy_rms":[0.02]*10+[0.2]*10+[0.02]*10}


def probe():
    return {"status":"reference_timing_observed_not_animation_reconstructed",
            "duration_seconds":3.0,"cut_candidates_seconds":[1,2]}


class RhythmEngineTests(unittest.TestCase):
    def test_pure_measured_half_second_onsets_choose_120bpm_candidate(self):
        result=music.rhythm(cues())
        self.assertEqual(result["candidate_tempo_bpm"],120)
        self.assertEqual(result["tempo_hypotheses"][0]["aligned_onsets"],6)
        self.assertIn(.75,result["estimated_grid_seconds"])
        self.assertFalse(result["verified_bpm"])
        self.assertFalse(result["emotion_detection"])
        self.assertFalse(result["lyric_understanding"])

    def test_energy_sections_from_actual_window_samples(self):
        segments=music.rhythm(cues())["relative_energy_sections"]
        self.assertEqual(len(segments),3)
        self.assertEqual(segments[0]["energy_label"],"middle")
        self.assertEqual(segments[1]["energy_label"],"higher_than_track_median")

    def test_ambiguous_short_audio_returns_no_tempo(self):
        result=music.rhythm(cues([0.5,1.0]))
        self.assertIsNone(result["candidate_tempo_bpm"])
        self.assertEqual(result["estimated_grid_seconds"],[])

    def test_deterministic_independent_of_output_environment(self):
        self.assertEqual(music.rhythm(cues()),music.rhythm(cues()))

    def test_disallows_nonfinite_and_reversed_events(self):
        for values in ([1.2,1.1,1.5,2], [0.3,0.3,1.0,2.0],
                       [float("nan"),1.0,1.5,2.0],[-0.1,0.5,1.0,2.0]):
            with self.subTest(values=values),self.assertRaises(ValueError):
                music.rhythm(cues(values))
        x=cues();x["energy_rms"][0]=float("inf")
        with self.assertRaises(ValueError):music.rhythm(x)

    def test_transients_drive_project_movement_not_just_metadata(self):
        plan=edit.plan(probe(),cues(),fps=30)
        self.assertTrue(plan["shots"][0]["pulseFrames"])
        self.assertEqual(plan["shots"][0]["pulseFrames"][:2],[8,22])
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"project"
            edit.create_project(root,plan)
            src=(root/"src"/"Video.jsx").read_text()
            self.assertIn("shot.pulseFrames",src)
            self.assertIn("zoom*pulseScale",src)
            self.assertIn("Math.abs(t-frame)",src)
            on_disk=json.loads((root/"src"/"plan.json").read_text())
            self.assertEqual(on_disk["shots"][0]["pulseFrames"][:2],[8,22])

if __name__=="__main__":
    unittest.main()
