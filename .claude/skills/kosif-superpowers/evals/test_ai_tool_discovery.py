"""Tests for original KOSIF discovery ranking; no external web or browser calls."""
import sys
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL/"scripts"))
import ai_tool_discovery as discovery


class DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = discovery.load_index()

    def test_index_full_and_unique(self):
        self.assertGreaterEqual(len(self.records), 4730)
        self.assertEqual(len(self.records), len({r["id"] for r in self.records}))

    def test_english_video_search(self):
        r = discovery.rank("video animation motion", self.records, 8)
        self.assertEqual(r["external_requests"], 0)
        self.assertTrue(r["results"])
        self.assertTrue(any(word in str(r["results"]).lower() for word in ("motion", "video", "animation")))

    def test_arabic_terms(self):
        r = discovery.rank("تحريك شخصيات فيديو", self.records)
        self.assertTrue(r["results"])
        self.assertTrue(all(p["score"] > 0 for p in r["results"]))

    def test_deterministic(self):
        a = discovery.rank("draw sketch image", self.records, 5)
        b = discovery.rank("draw sketch image", self.records, 5)
        self.assertEqual(a, b)

    def test_no_runtime_proof_inflation(self):
        r = discovery.rank("blender 3d geometry", self.records)
        self.assertTrue(all(x["runtime_verified"] is False for x in r["results"]))
        self.assertTrue(all("claimed_catalog_status" in x for x in r["results"]))

    def test_invalid_query_and_limits(self):
        for text in ("", "the and to", "   "):
            with self.assertRaises(ValueError):
                discovery.rank(text, self.records)
        for n in (0, 31, 1.5, True):
            with self.assertRaises(ValueError):
                discovery.rank("draw", self.records, n)

    def test_no_search_result_for_unrelated_nonsense(self):
        r = discovery.rank("zzzxqjvkk", self.records)
        self.assertEqual(r["results"], [])


if __name__ == "__main__":
    unittest.main()
