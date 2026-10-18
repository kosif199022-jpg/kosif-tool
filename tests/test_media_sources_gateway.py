"""KOSIF media source registry and download rights gate."""
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/kosif-superpowers/scripts/media_sources.py"
spec = importlib.util.spec_from_file_location("kosif_media_sources", SCRIPT)
media = importlib.util.module_from_spec(spec)
spec.loader.exec_module(media)

class MediaSourceTests(unittest.TestCase):
    def test_exactly_100_unique_https_sites(self):
        rows = media.load_sources()
        self.assertEqual(len(rows), 100)
        self.assertEqual(len({r["domain"] for r in rows}), 100)
        self.assertTrue(all(r["url"].startswith("https://") for r in rows))
        self.assertTrue(all(r["license_policy"].startswith("verify_") for r in rows))
        self.assertTrue(all("license_hint" in r for r in rows))

    def test_important_license_sources_included(self):
        sites = {s["domain"] for s in media.load_sources()}
        for key in ("pexels.com", "pixabay.com", "mixkit.co", "coverr.co",
                    "unsplash.com", "commons.wikimedia.org", "si.edu"):
            self.assertIn(key, sites)

    def test_rights_must_be_explicit(self):
        self.assertTrue(media.validate_license("https://pexels.com/video", None, None, None, None))
        self.assertTrue(media.validate_license("https://example.com/video", "cc0", None, None, None))
        self.assertEqual(media.validate_license("https://example.com/video", "owned", None, None, None), [])

    def test_cc_by_requires_attribution(self):
        self.assertTrue(media.validate_license("https://example.com/video", "cc-by",
                                               "https://example.com/rights", None, None))
        self.assertEqual(media.validate_license("https://example.com/video", "cc-by",
                                               "https://example.com/rights", "A", "A / CC BY"), [])

    def test_non_http_url_rejected(self):
        self.assertTrue(media.validate_license("file:///private/clip", "owned", None, None, None))
        self.assertTrue(media.validate_license("https://name:pass@example.org/v", "owned", None, None, None))

    def test_lookup_subdomains_but_not_suffix_attack(self):
        s = media.load_sources()
        self.assertEqual(media.source_for("https://cdn.pexels.com/v.mp4", s)["domain"], "pexels.com")
        self.assertIsNone(media.source_for("https://pexels.com.evil.org/v.mp4", s))

    def test_search_no_network(self):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = media.main(["search", "pixabay"])
        self.assertEqual(rc, 0)
        self.assertIn("pixabay", out.getvalue().lower())

    def test_dry_run_licensed_without_network(self):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = media.main(["download", "https://example.com/owned.mp4", "--rights", "owned", "--dry-run"])
        self.assertEqual(rc, 0)
        self.assertIn("dry_run_no_download", out.getvalue())
        self.assertIn("fetch_video.py", out.getvalue())

if __name__ == "__main__":
    unittest.main()
