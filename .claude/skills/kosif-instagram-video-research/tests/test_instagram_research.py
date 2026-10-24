"""Offline tests for KOSIF Instagram Video Research, no live APIs required."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "instagram_research.py"
spec = importlib.util.spec_from_file_location("instagram_research", SCRIPT)
research = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)

class TestInstagramVideoResearch(unittest.TestCase):
    def test_registered_sources(self):
        self.assertEqual({x["handle"] for x in research.creators()}, {"asirgokerr", "brkn.land"})

    def test_arabic_expansion(self):
        self.assertIn("clouds", research.expand("غيوم"))
        self.assertIn("sunset", research.expand("غروب"))

    def test_links_are_not_claimed_results(self):
        jobs = research.plan("شلال")
        self.assertEqual(len(jobs), 7)
        self.assertEqual(jobs[-1]["scope"], "instagram_app")
        self.assertTrue(any(j["scope"] == "brkn.land" for j in jobs))

    def test_canonical_urls_are_safe(self):
        self.assertEqual(
            research.canonical("https://instagram.com/reel/C1234567/?igsh=test"),
            "https://www.instagram.com/reel/C1234567/")
        self.assertEqual(
            research.canonical("https://www.instagram.com/brkn.land/reel/C1234567/?igsh=x"),
            "https://www.instagram.com/reel/C1234567/")
        for url in ["https://instagram.com.example.net/reel/C1234567/",
                    "https://instagram.com/a/b/reel/C1234567/",
                    "file:///etc/passwd", "https://instagram.com/reel/a",
                    "https://instagram.com/private/"]:
            self.assertIsNone(research.canonical(url))

    def test_sqlite_deduplication_and_search(self):
        with tempfile.TemporaryDirectory() as t:
            db = research.database(Path(t) / "clips.sqlite")
            try:
                count = research.import_rows(db, [
                    {"url":"https://instagram.com/reel/C1234567/?igsh=test",
                     "title":"Clouds at sunset", "author":"brkn.land"},
                    {"url":"https://www.instagram.com/reel/C1234567/",
                     "description":"Golden sky"}
                ],source="test",search_query="sunset")
                self.assertEqual(count,2)
                self.assertEqual(db.execute("SELECT count(*) FROM reels").fetchone()[0],1)
                hits=research.find(db,"غروب")
                self.assertEqual(len(hits),1)
                self.assertEqual(hits[0]["evidence"],"public_search_index_unverified")
            finally:
                db.close()

if __name__ == "__main__":
    unittest.main()
