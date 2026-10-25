"""Keyless stock fetcher: id parsing, licence table and CLI parsing (offline)."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/kosif-superpowers/scripts/stock_fetch.py"
spec = importlib.util.spec_from_file_location("kosif_stock_fetch", SCRIPT)
sf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sf)


class StockFetchTests(unittest.TestCase):
    def test_parse_id_from_bare_id_and_page_urls(self):
        self.assertEqual(sf.parse_id("35155732"), "35155732")
        self.assertEqual(sf.parse_id("https://www.pexels.com/video/breathtaking-view-of-kaaba-in-mecca-35155732/"), "35155732")
        self.assertEqual(sf.parse_id("https://mixkit.co/free-stock-video/mosque-in-the-mountain-at-dawn-9998/"), "9998")
        self.assertEqual(sf.parse_id("https://www.pexels.com/video/clip-9112700/?utm=x"), "9112700")

    def test_parse_id_rejects_text_without_id(self):
        with self.assertRaises(ValueError):
            sf.parse_id("https://www.pexels.com/search/videos/kaaba/")

    def test_every_source_has_a_licence(self):
        for src in ("pexels", "mixkit", "pixabay"):
            name, url, terms = sf.LICENCES[src]
            self.assertTrue(url.startswith("https://"))
            self.assertTrue(name and terms)

    def test_mixkit_url_is_the_free_720p_file(self):
        self.assertEqual(sf.MIXKIT_FILE.format(id="4312"), "https://assets.mixkit.co/videos/4312/4312-720.mp4")

    def test_router_maps_stock_pages_and_direct_files_offline(self):
        orig = sf.resolve_pexels
        sf.resolve_pexels = lambda cid: f"https://videos.pexels.com/video-files/{cid}/x.mp4"
        try:
            self.assertEqual(sf.stock_file_url("https://www.pexels.com/video/waves-9112700/"),
                             ("pexels", "https://videos.pexels.com/video-files/9112700/x.mp4", "9112700"))
        finally:
            sf.resolve_pexels = orig
        self.assertEqual(sf.stock_file_url("https://mixkit.co/free-stock-video/mosque-4312/"),
                         ("mixkit", "https://assets.mixkit.co/videos/4312/4312-720.mp4", "4312"))
        direct = "https://cdn.coverr.co/videos/coverr-walk-8360/1080p.mp4"
        self.assertEqual(sf.stock_file_url(direct), ("cdn.coverr.co", direct, None))
        self.assertIsNone(sf.stock_file_url("https://www.tiktok.com/@a/video/123456"))
        self.assertIsNone(sf.stock_file_url("https://www.pexels.com/search/videos/kaaba/".replace("videos", "photos")))
        self.assertIsNone(sf.stock_file_url("https://evilpexels.com/video/1234/"))

    def test_pixabay_without_key_says_what_is_missing(self):
        import os
        old = os.environ.pop("PIXABAY_API_KEY", None)
        try:
            with self.assertRaisesRegex(RuntimeError, "PIXABAY_API_KEY"):
                sf.stock_file_url("https://pixabay.com/videos/ocean-waves-1854/")
        finally:
            if old is not None:
                os.environ["PIXABAY_API_KEY"] = old

    def test_cli_requires_a_subcommand(self):
        with self.assertRaises(SystemExit):
            sf.main([])


if __name__ == "__main__":
    unittest.main()
