"""Offline tests for the incremental KOSIF Instagram/Infinite Matrices bridge."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/"instagram_research.py"
spec=importlib.util.spec_from_file_location("instagram_research",SCRIPT)
research=importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)

class TestReviewedMechanisms(unittest.TestCase):
    def test_compound_multilingual_topic(self):
        expanded=research.expand("موشن سبورة")
        self.assertEqual(expanded[0],"موشن سبورة")
        self.assertIn("motion graphics whiteboard animation", expanded[1])
        jobs=research.plan("موشن سبورة")
        self.assertTrue(any('"asirgokerr"' in j["query"] for j in jobs if j["scope"]=="asirgokerr"))
        self.assertTrue(any('"brkn.land"' in j["query"] for j in jobs if j["scope"]=="brkn.land"))

    def test_human_review_is_separate_from_public_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            db=research.database(Path(td)/"test.sqlite")
            clip="https://www.instagram.com/reel/C12345TEST/"
            try:
                research.import_rows(db,[{"url":clip,"title":"Public indexed caption"}],
                                     source="brave_web_index",search_query="cinematic")
                receipt=research.review_reel(db,clip,"reviewer",
                    "graphite,whiteboard","stroke_reveal,causal_history",
                    "Synthetic test annotation — NOT a real observed video")
                self.assertEqual(receipt["review_status"],"verified_by_authorized_review")
                matches=research.find(db,"stroke_reveal")
                self.assertEqual(len(matches),1)
                self.assertEqual(matches[0]["evidence"],"verified_by_authorized_review")
                research.import_rows(db,[{"url":clip,"title":"Other public snippet"}],
                                     source="brave_web_index",search_query="cloud")
                self.assertEqual(research.find(db,"stroke_reveal")[0]["evidence"],
                                 "verified_by_authorized_review")
                path=Path(td)/"matrix_references.json"
                report=research.export_reviews(db,path)
                self.assertEqual(report["exported"],1)
                payload=json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("causal_history",payload["references"][0]["observed_mechanisms"])
            finally:
                db.close()

    def test_refuses_review_of_unindexed_url(self):
        with tempfile.TemporaryDirectory() as td:
            db=research.database(Path(td)/"test.sqlite")
            try:
                with self.assertRaises(ValueError):
                    research.review_reel(db,"https://instagram.com/reel/NoRecord123/",
                        "reviewer","graphics","stroke","Not indexed")
                with self.assertRaises(ValueError):
                    research.review_reel(db,"https://evil.example/reel/NoRecord123/",
                        "reviewer","graphics","stroke","Invalid host")
            finally:
                db.close()

if __name__=="__main__":
    unittest.main()
