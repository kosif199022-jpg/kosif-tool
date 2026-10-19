"""Safe URL and atlas inventory tests. No network is accessed by unit tests."""
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import urlsplit
SK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/"scripts"))
import browser_scout as b

class BrowserScoutTests(unittest.TestCase):
    def test_catalog_count_unique_ids(self):
        rows=b.entries()
        self.assertEqual(len(rows),26)
        self.assertEqual(len({x["id"] for x in rows}),26)
        self.assertGreaterEqual(len({x["category"] for x in rows}),10)
    def test_curated_https_hosts(self):
        for row in b.entries():
            self.assertEqual(b.check_url(row["url"],urlsplit(row["url"]).hostname),urlsplit(row["url"]).hostname)
    def test_block_unsafe_urls(self):
        for url,host in [
            ("file:///etc/passwd","file"),("http://www.canva.com/draw/","www.canva.com"),
            ("https://localhost/test","localhost"),("https://127.0.0.1/","127.0.0.1"),
            ("https://www.canva.com.evil.example/","www.canva.com"),
            ("https://evil@www.canva.com/","www.canva.com"),
            ("https://www.canva.com:444/","www.canva.com"),
            ("https://www.canva.com/#fragment","www.canva.com"),
            ("https://192.168.1.5/","192.168.1.5")
        ]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                b.check_url(url,host)
    def test_unknown_id_refused(self):
        with self.assertRaises(ValueError):
            b.lookup("not-there")
    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"already.png";path.write_bytes(b"original")
            with self.assertRaisesRegex(ValueError,"unused"):
                b.survey(b.lookup("autodraw"),path)
            self.assertEqual(path.read_bytes(),b"original")
    def test_invalid_output_type_refused(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError,"unused"):
                b.survey(b.lookup("autodraw"),Path(td)/"site.exe")
    def test_invalid_engine_and_timeout_refused(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError,"engine"):
                b.survey(b.lookup("autodraw"),Path(td)/"site.png","evil")
            with self.assertRaisesRegex(ValueError,"timeout"):
                b.survey(b.lookup("autodraw"),Path(td)/"site.png",seconds=200)
    def test_no_website_marked_executed(self):
        for row in b.entries():
            self.assertNotIn("executed",row)
    def test_script_no_auto_installs_or_clones(self):
        script=(SK/"scripts/browser_scout.py").read_text(encoding="utf-8-sig")
        self.assertNotIn("git clone",script)
        self.assertNotIn("playwright install",script)
        self.assertIn('service_workers="block"',script)
        self.assertIn("accept_downloads=False",script)
if __name__=="__main__":
    unittest.main()
