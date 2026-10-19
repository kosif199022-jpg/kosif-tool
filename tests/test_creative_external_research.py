"""Validate creative research catalogs without network or external execution."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/".claude"/"skills"/"kosif-superpowers"/"scripts"
sys.path.insert(0,str(SCRIPTS))
import creative_external_search as searcher
import rea_creative_research_atlas as atlas

class ResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repos,cls.sites=searcher.load()

    def test_one_thousand_public_repo_metadata(self):
        self.assertEqual(len(self.repos),1000)
        self.assertEqual(len({r["repository"] for r in self.repos}),1000)
        self.assertTrue(all(r["github_metadata_observed"] for r in self.repos))
        self.assertTrue(all(r["rea_code_analyzed"] is False for r in self.repos))
        self.assertTrue(all(r["feature_implemented_in_kosif"] is False for r in self.repos))

    def test_diverse_repo_topics(self):
        from collections import Counter
        c=Counter(r["category"] for r in self.repos)
        self.assertGreaterEqual(c["image-photo"],250)
        self.assertGreaterEqual(c["video-film"],300)
        self.assertGreaterEqual(c["motion-vfx"],150)

    def test_sites_from_named_curated_sources_not_infra(self):
        self.assertEqual(len(self.sites),1000)
        self.assertEqual(len({s["site"] for s in self.sites}),1000)
        self.assertTrue(all(s["source_list"] and s["sample_url"] for s in self.sites))
        self.assertTrue(all(not s["rea_browser_analyzed"] for s in self.sites))
        self.assertNotIn("img.shields.io",{s["site"] for s in self.sites})

    def test_user_private_repo_names_are_not_in_public_catalog(self):
        alltext=str(self.repos)+str(self.sites)
        self.assertNotIn("kosif199022-jpg/app",alltext)
        self.assertNotIn("kosif199022-jpg/kosif-atlas-private",alltext)
        self.assertNotIn("PRIVATE_LOCAL",alltext)

    def test_search_distinguishes_discovery_from_execution(self):
        matches=searcher.search("video editing",kind="repo",top=5)
        self.assertTrue(matches)
        self.assertTrue(all(m["feature_status"]=="DISCOVERED_METADATA_ONLY" for m in matches))
        self.assertTrue(all("rea_analysis" in m for m in matches))

    def test_arabic_expansion(self):
        results=searcher.search("صور",kind="repo",top=10)
        self.assertTrue(results)

    def test_site_extraction_filters_badges(self):
        m="# Motion tools\n* [Example](https://video.example.org/tool)\n* [Badge](https://img.shields.io/badge/help.svg)\n"
        rows=atlas.extract_sites(m,"test/example")
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["site"],"video.example.org")

    def test_readonly_registry(self):
        r=searcher.report()
        self.assertEqual(r["REA_broad_analysis_claim"],False)
        self.assertEqual(r["KOSIF_implemented_new_features_from_catalog"],0)

if __name__=="__main__":
    unittest.main()
