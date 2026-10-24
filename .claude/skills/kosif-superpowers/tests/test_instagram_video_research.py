"""Stdlib-only tests for KOSIF public Instagram research index."""
import argparse
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import instagram_video_research as ivr


class TestInstagramVideoResearch(unittest.TestCase):
    def test_seed_profiles_are_exact_user_supplied_accounts(self):
        sources = ivr.get_sources()
        self.assertEqual({x["username"] for x in sources}, {"asirgokerr", "brkn.land"})
        self.assertTrue(all(x["status"] == "USER_PROVIDED_LINK_UNVERIFIED_CONTENT" for x in sources))

    def test_normalizes_arabic_search(self):
        self.assertEqual(ivr.normalize("إبداع، تحريك، ألـوان"), "ابداع تحريك الوان")
        self.assertIn("whiteboard animation", ivr.expand_topic("سبورة"))

    def test_strict_url_canonicalization(self):
        u, key = ivr.canonical_reel("https://www.instagram.com/reel/C7Example01/?utm_medium=social")
        self.assertEqual((u, key), ("https://www.instagram.com/reel/C7Example01/", "C7Example01"))
        for bad in ("https://evil.example/reel/C7Example01/",
                    "https://instagram.com/private/page/",
                    "file:///etc/passwd", "http://instagram.com.evil.com/reel/C7Example01/"):
            with self.assertRaises(ValueError):
                ivr.canonical_reel(bad)

    def test_query_plan_is_not_misrepresented_as_found_videos(self):
        obj = ivr.plan("موشن سبورة", "all", 12)
        self.assertTrue(any("asirgokerr" in x["url"] for x in obj["queries"]))
        self.assertTrue(any("brkn.land" in x["url"] for x in obj["queries"]))
        self.assertTrue(any("www.google.com" in x["url"] for x in obj["queries"]))
        self.assertTrue(all(x["status"] == "SEARCH_PLAN_NOT_VERIFIED_RESULT" for x in obj["queries"]))

    def test_index_upsert_ranking_and_export(self):
        with tempfile.TemporaryDirectory() as td:
            dbfile = Path(td) / "index.sqlite3"
            with ivr.connect(dbfile) as conn:
                args = argparse.Namespace(
                    url="https://www.instagram.com/reel/C7Example01/?igsh=tracking",
                    account="asirgokerr", title="Whiteboard animation",
                    caption="timed drawing and motion",
                    tags="whiteboard, motion", mechanisms="stroke reveal, path",
                    status="visually_reviewed", query="whiteboard",
                    provenance="human review", notes="sample fixture"
                )
                ivr.add_reel(conn, args)
                results = ivr.search_index(conn, "whiteboard", 5)
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["status"], "visually_reviewed")
                self.assertEqual(results[0]["tags"], ["whiteboard", "motion"])
                # Re-adding only a URL must not erase tags or downgrade reviewed status.
                args.title = args.caption = args.tags = args.mechanisms = args.notes = ""
                args.status = "candidate"
                args.provenance = "manual"
                ivr.add_reel(conn, args)
                result = ivr.search_index(conn, "whiteboard", 5)[0]
                self.assertEqual(result["status"], "visually_reviewed")
                self.assertEqual(result["title"], "Whiteboard animation")
                target = Path(td) / "references.json"
                receipt = ivr.export_rows(conn, target, "json", reviewed_only=True)
                self.assertEqual(receipt["exported"], 1)
                payload = json.loads(target.read_text(encoding="utf-8"))
                self.assertEqual(payload["records"][0]["shortcode"], "C7Example01")


if __name__ == "__main__":
    unittest.main()
