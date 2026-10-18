"""Checks for fonts/kosif-jumuah: files, OFL compliance, coverage (via fontTools when installed) and the demo page."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fixture import REAL_ROOT  # noqa: E402

KIT = REAL_ROOT / "fonts" / "kosif-jumuah"
ARABIC = re.compile(r"[؀-ۿ]")
STYLES = ("Regular", "Bold")

try:
    from fontTools.ttLib import TTFont  # type: ignore
except ImportError:  # CI installs no third-party packages; coverage checks then skip with a reason
    TTFont = None


class KitFilesTest(unittest.TestCase):
    def test_files_present(self):
        for rel in ["build_font.py", "OFL.txt", "README.md", "demo/jumuah.html", "demo/compose_title.py", "demo/title-aljumuah.svg", "demo/preview.png"] + [f"KOSIFJumuah-{s}.{ext}" for s in STYLES for ext in ("ttf", "woff2")]:
            with self.subTest(file=rel):
                self.assertTrue((KIT / rel).exists(), rel)

    def test_ofl_carries_both_upstream_notices_and_rfn_statement(self):
        text = (KIT / "OFL.txt").read_text(encoding="utf-8")
        self.assertIn("SIL Open Font License", text)
        self.assertIn("Amiri", text)
        self.assertIn("Bodoni Moda", text)
        self.assertIn("Reserved Font Name", text)
        self.assertIn("NOT used", text)

    def test_readme_is_bilingual_and_credits_sources(self):
        text = (KIT / "README.md").read_text(encoding="utf-8")
        self.assertTrue(ARABIC.search(text))
        for needle in ("github.com/aliftype/amiri", "indestructible-type", "OFL", "build_font.py", "observed", "assumed"):
            self.assertIn(needle, text, needle)

    def test_demo_page_follows_the_renderer_contract_and_references_the_kit(self):
        html = (KIT / "demo" / "jumuah.html").read_text(encoding="utf-8")
        self.assertIn("window.__kosif", html)
        self.assertIn("__kosifReady", html)
        self.assertIn("@font-face", html)
        for url in re.findall(r'url\("([^"]+)"\)', html):
            with self.subTest(url=url):
                self.assertTrue((KIT / "demo" / url).resolve().exists(), url)
        self.assertTrue(ARABIC.search(html))

    def test_composed_title_is_inlined_and_well_formed(self):
        svg = (KIT / "demo" / "title-aljumuah.svg").read_text(encoding="utf-8")
        self.assertIn('viewBox="0 0 ', svg)
        self.assertGreaterEqual(svg.count("<path "), 9, "alef, lam, jeem, meem, ain, taa, kashidas and three marks")
        self.assertIn('id="lettering"', svg)
        self.assertNotIn('id="title"', svg, "must not collide with the demo's #title layer")
        self.assertIn("Amiri", svg, "the OFL source must be credited in the file")
        html = (KIT / "demo" / "jumuah.html").read_text(encoding="utf-8")
        self.assertIn("title-svg:start", html)
        self.assertIn('id="titlesvg"', html)
        self.assertEqual(html.count('id="title"'), 1)


@unittest.skipUnless(TTFont, "fontTools not installed (pip install fonttools)")
class FontBinaryTest(unittest.TestCase):
    REQUIRED = {"alef": 0x0627, "lam": 0x0644, "taa marbuta": 0x0629, "tatweel": 0x0640, "ﷺ": 0xFDFA, "fatha": 0x064E, "shadda": 0x0651,
                "Arabic comma": 0x060C, "0": 0x30, "9": 0x39, "A": 0x41, "z": 0x7A, "@": 0x40, ".": 0x2E, "space": 0x20}

    def test_each_style_is_well_formed_renamed_and_complete(self):
        for style in STYLES:
            for ext in ("ttf", "woff2"):
                with self.subTest(style=style, ext=ext):
                    font = TTFont(KIT / f"KOSIFJumuah-{style}.{ext}")
                    names = font["name"]
                    self.assertEqual(names.getDebugName(1), "KOSIF Jumuah")
                    self.assertEqual(names.getDebugName(2), style)
                    self.assertEqual(names.getDebugName(6), f"KOSIFJumuah-{style}")
                    for nid in (1, 4, 6, 16):
                        value = names.getDebugName(nid) or ""
                        self.assertNotIn("Amiri", value, "Reserved Font Name must not appear in the family name")
                        self.assertNotIn("Bodoni", value, "Reserved Font Name must not appear in the family name")
                    self.assertIn("Open Font License", names.getDebugName(13) or "")
                    self.assertEqual(font["head"].unitsPerEm, 1000)
                    self.assertIn("GSUB", font, "Arabic shaping features must survive the merge")
                    self.assertEqual(font["OS/2"].usWeightClass, 700 if style == "Bold" else 400)
                    self.assertEqual(font["OS/2"].fsType, 0)
                    cmap = font.getBestCmap()
                    missing = [k for k, cp in self.REQUIRED.items() if cp not in cmap]
                    self.assertEqual(missing, [], f"missing code points: {missing}")

    def test_latin_and_arabic_glyphs_come_from_different_masters(self):
        font = TTFont(KIT / "KOSIFJumuah-Regular.ttf")
        cmap = font.getBestCmap()
        glyf = font["glyf"]
        # The Didone "2" has far fewer contours than any Arabic ligature and lives in its own outline; Arabic lam-alef is a two-part glyph.
        two = glyf[cmap[0x32]]
        self.assertGreaterEqual(two.numberOfContours, 1)
        self.assertIn(0xFEFB, cmap, "lam-alef presentation form expected from the Arabic master")


if __name__ == "__main__":
    unittest.main()
