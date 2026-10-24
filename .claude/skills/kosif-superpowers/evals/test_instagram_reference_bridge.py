import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import instagram_reference_bridge as ig

class InstagramReferenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.c=ig.db(Path(self.tmp.name)/"references.sqlite3")
    def tearDown(self):
        self.c.close()
        self.tmp.cleanup()
    def test_search_plans_for_two_accounts(self):
        self.assertEqual(len(ig.search_plans("موشن سينمائي")),12)
        self.assertIn("asirgokerr",str(ig.search_plans("light")))
    def test_rejects_wrong_hosts_and_unsafe_urls(self):
        for u in ("http://instagram.com/reel/ABC123/","https://evil.com/reel/ABC123/",
                  "https://www.instagram.com/reel/../","https://www.instagram.com/profile/"):
            with self.assertRaises(ValueError): ig.video_url(u)
    def test_canonical_permalink(self):
        self.assertEqual(ig.video_url("https://www.instagram.com/reel/ABC123/?igsh=abc"),
                         "https://www.instagram.com/reel/ABC123/")
    def test_add_search_and_research_handoff(self):
        url=ig.put(self.c,{"url":"https://instagram.com/reel/ABC123/",
                            "handle":"brkn.land","topic":"3d animation",
                            "visual":"clay","motion":"morph","state":"link_only"})
        self.assertEqual(len(ig.match(self.c,"3d animation")),1)
        proposal=ig.propose(self.c,url)
        self.assertEqual(proposal["status"],"NOT_VERIFIED_REFERENCE")
        self.assertIn("causal_bricks",proposal)
    def test_review_requires_evidence(self):
        with self.assertRaises(ValueError):
            ig.put(self.c,{"url":"https://instagram.com/reel/ABC123/",
                           "topic":"particles","state":"frames_reviewed"})
    def test_evidence_cannot_downgrade(self):
        entry={"url":"https://instagram.com/reel/ABC123/","topic":"light",
               "state":"frames_reviewed","evidence_uri":"out/frame-analysis.json"}
        ig.put(self.c,entry)
        with self.assertRaises(ValueError):
            ig.put(self.c,{**entry,"state":"link_only"})
    def test_kmx_operator_lookup(self):
        u=ig.put(self.c,{"url":"https://instagram.com/reel/ABC123/",
                          "topic":"جسيمات", "state":"frames_reviewed",
                          "evidence_uri":"out/frame-analysis.json"})
        f=Path(self.tmp.name)/"catalog.json"
        f.write_text(json.dumps({"styles":[{"style_id":"flow-field",
              "card_family":"Data & Information","operator_tags":["particles","field"]}]}))
        proposal=ig.propose(self.c,u,str(f))
        self.assertEqual(proposal["status"],"EVIDENCE_REVIEWED_PROPOSAL")
        self.assertEqual(proposal["candidate_86_style_adapters"][0]["style_id"],"flow-field")

if __name__=="__main__":
    unittest.main()
