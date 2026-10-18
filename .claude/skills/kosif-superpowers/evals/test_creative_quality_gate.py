"""Execute KOSIF logical QA gates on real generated Remotion edit data."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

S=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(S))
import reference_edit_engine as engine
import creative_quality_gate as q


def original(cuts=None):
    return {"status":"reference_timing_observed_not_animation_reconstructed",
            "duration_seconds":5,
            "cut_candidates_seconds":[1,2,4] if cuts is None else cuts}


def audio():
    return {"schema":"kosif.audio-cues.v1","duration":5,"words":[
        {"text":"سلام","start":0.2,"end":0.8},
        {"text":"يا","start":1.1,"end":1.3},
        {"text":"دنيا","start":2.2,"end":2.5}],
        "onset_candidates_seconds":[0.1,1.99,2.5,4.99]}


class ReasoningQualityGates(unittest.TestCase):
    def test_real_validated_edit_passes_structural_checks_only(self):
        obj=engine.plan(original(),audio())
        report=q.inspect_plan(obj)
        self.assertEqual(report["status"],"structurally_verified_render_pending")
        self.assertEqual(report["failures"],[])
        self.assertTrue(all(c["pass"] for c in report["checks"].values()))
        self.assertFalse(report["rendered"])
        self.assertGreater(len(report["unverified"]),2)

    def test_output_project_contains_actual_qa_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            project=Path(d)/"edit"
            result=engine.create_project(project,engine.plan(original(),audio()))
            self.assertEqual(result["status"],"editable_project_created_unrendered")
            audit=json.loads((project/"quality-audit.json").read_text())
            self.assertEqual(audit["metrics"]["totalFrames"],150)
            self.assertEqual(audit["status"],"structurally_verified_render_pending")

    def test_frame_gap_rejected(self):
        obj=engine.plan(original())
        obj["shots"][1]["startFrame"]+=1
        result=q.inspect_plan(obj)
        self.assertIn("continuous_no_gap_no_overlap",result["failures"])

    def test_total_duration_clock_falsification_rejected(self):
        obj=engine.plan(original())
        obj["totalFrames"]=135
        self.assertIn("valid_audio_frame_clock",q.inspect_plan(obj)["failures"])

    def test_audio_word_cannot_cross_cut(self):
        obj=engine.plan(original(),audio())
        obj["alignedWords"].append({"text":"خطأ","start":3.6,"end":4.2})
        report=q.inspect_plan(obj)
        self.assertIn("aligned_words_preserved",report["failures"])

    def test_forged_verification_flags_block(self):
        obj=engine.plan(original())
        obj["evidence"]["renderVerified"]=True
        self.assertIn("truthful_evidence_flags",q.inspect_plan(obj)["failures"])

    def test_out_of_range_pulse_is_blocked(self):
        obj=engine.plan(original(),audio())
        obj["shots"][0]["pulseFrames"]=[-1,5]
        self.assertIn("continuous_no_gap_no_overlap",q.inspect_plan(obj)["failures"])

    def test_media_path_traversal_is_blocked(self):
        obj=engine.plan(original())
        obj["shots"][0]["asset"]="../reference.mp4"
        self.assertIn("user_asset_reference_integrity",q.inspect_plan(obj)["failures"])

    def test_missing_replacement_clip_is_blocked_when_project_provided(self):
        obj=engine.plan(original())
        obj["shots"][0]["asset"]="clip_000.mp4"
        with tempfile.TemporaryDirectory() as d:
            result=q.inspect_plan(obj,d)
            self.assertIn("user_asset_reference_integrity",result["failures"])

    def test_clip_metadata_check_not_photoreal_quality_approval(self):
        obj=engine.plan(original(),audio())
        obj["shots"][1]["asset"]="clip_001.mp4"
        result=q.inspect_plan(obj)
        self.assertEqual(result["status"],"structurally_verified_render_pending")
        self.assertIn("visual quality",str(result["unverified"]))
        self.assertNotIn("accepted_commercial_film",str(result))

    def test_word_preservation_from_external_alignment_ends_with_audio_clock(self):
        obj=engine.plan(original(),audio())
        self.assertEqual(len(obj["alignedWords"]),3)
        self.assertEqual(obj["alignedWords"][2]["end"],2.5)
        self.assertEqual(obj["shots"][-1]["endFrame"],150)
        self.assertEqual(q.inspect_plan(obj)["failures"],[])


if __name__=="__main__":
    unittest.main()
