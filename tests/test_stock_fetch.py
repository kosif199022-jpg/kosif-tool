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
        for src in ("pexels", "mixkit"):
            name, url, terms = sf.LICENCES[src]
            self.assertTrue(url.startswith("https://"))
            self.assertTrue(name and terms)

    def test_mixkit_url_is_the_free_720p_file(self):
        self.assertEqual(sf.MIXKIT_FILE.format(id="4312"), "https://assets.mixkit.co/videos/4312/4312-720.mp4")

    def test_cli_requires_a_subcommand(self):
        with self.assertRaises(SystemExit):
            sf.main([])


if __name__ == "__main__":
    unittest.main()
