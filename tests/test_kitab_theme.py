"""starters/kitab-theme: every @font-face points at a shipped font, the palette anchor holds, fonts carry the OFL."""
import re
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[1] / "starters" / "kitab-theme"


class KitabThemeTest(unittest.TestCase):
    def test_font_faces_resolve(self):
        css = (KIT / "public" / "kosif-kitab-theme.css").read_text(encoding="utf-8")
        urls = set(re.findall(r"url\(/fonts/([^)]+\.woff2)\)", css))
        shipped = {p.name for p in (KIT / "public" / "fonts").glob("*.woff2")}
        self.assertTrue(urls)
        self.assertEqual(urls, shipped, "each @font-face file ships, and no font ships unused")
        for name in shipped:
            self.assertEqual((KIT / "public" / "fonts" / name).read_bytes()[:4], b"wOF2", name)

    def test_palette_anchor_and_dark_mode(self):
        css = (KIT / "public" / "kosif-kitab-theme.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"--kc-cream\s*:\s*#FBF4E1")
        self.assertIn("prefers-color-scheme: dark", css.replace("prefers-color-scheme:dark", "prefers-color-scheme: dark"))
        self.assertNotRegex(css, r"@import\s+url\(https?:", "fonts stay self-hosted")

    def test_licence_names_each_family(self):
        lic = (KIT / "public" / "fonts" / "OFL.txt").read_text(encoding="utf-8")
        for family in ("Alexandria", "IBM Plex Sans Arabic", "Amiri", "SIL OPEN FONT LICENSE"):
            self.assertIn(family.upper(), lic.upper())


if __name__ == "__main__":
    unittest.main()
