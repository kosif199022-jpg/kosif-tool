"""Source-backed art learning packets and evidence checks (stdlib, offline)."""
import json
import tempfile
import unittest
from pathlib import Path
import sys

SK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/"scripts"))
import drawing_academy as A  # noqa:E402

class AcademyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=A.curriculum()

    def test_lesson_and_source_structure(self):
        self.assertEqual(len(self.data["lessons"]),8)
        self.assertEqual(len(self.data["sources"]),8)
        self.assertEqual(len(set(s["source_url"] for s in self.data["sources"])),8)

    def test_trust_states_are_explicit(self):
        for s in self.data["sources"]:
            self.assertFalse(s["ingested_full_text"])
            self.assertIn("USA",s["rights"])
        for lesson in self.data["lessons"]:
            self.assertEqual(sum(x["weight"] for x in lesson["metrics"]),100)
            self.assertEqual(A.package(self.data,lesson)["status"],"ORIGINAL_EXERCISE_UNEXECUTED")

    def test_reject_unknown_lesson_and_schema(self):
        self.assertIsNone(A.select(self.data,"not-real"))
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/"bad.json"
            fake.write_text('{"schema":"bad"}',encoding="utf-8")
            with self.assertRaises(ValueError): A.curriculum(fake)

    def test_scan_book_extracts_metadata_only(self):
        with tempfile.TemporaryDirectory() as d:
            text=Path(d)/"authorized.txt"
            text.write_text("CHAPTER ONE\nDraw a circle.\nThe outline uses lines.\n",encoding="utf-8")
            packet=A.scan_book(self.data,"lutz-how",text,"own_copy_private")
            self.assertEqual(packet["keyword_hit_lines"],2)
            self.assertEqual(packet["status"],"SOURCE_TEXT_SCANNED_CANDIDATES_ONLY")
            self.assertIn("source_sha256",packet)
            self.assertNotIn("Draw a circle",json.dumps(packet))

    def test_assess_fails_without_artifact(self):
        with tempfile.TemporaryDirectory() as d:
            sc=Path(d)/"scores.json"
            sc.write_text("{}",encoding="utf-8")
            result=A.assessment(self.data,"build_shapes",sc,Path(d)/"missing.svg")
            self.assertEqual(result["status"],"NEEDS_ARTIFACT_EVIDENCE")

    def test_scored_review_cannot_prove_professionalism(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            image=p/"example.svg"
            image.write_text("<svg></svg>",encoding="utf-8")
            scores=p/"scores.json"
            metrics=A.select(self.data,"build_shapes")["metrics"]
            scores.write_text(json.dumps({v["id"]:4 for v in metrics}),encoding="utf-8")
            report=A.assessment(self.data,"build_shapes",scores,image)
            self.assertEqual(report["score_out_of_100"],80)
            self.assertIn("NOT_AUTOMATED_VISUAL_PROOF",report["status"])
            self.assertIn("evidence_sha256",report)

    def test_safe_nonoverwriting_output(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/"result.json"
            A.write_result({"ok":True},str(dest))
            with self.assertRaises(ValueError):
                A.write_result({"ok":False},str(dest))
            self.assertTrue(json.loads(dest.read_text(encoding="utf-8"))["ok"])

if __name__=="__main__":
    unittest.main()
