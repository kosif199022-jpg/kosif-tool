"""Offline tests for the 586-style library (86 Futurepedia-derived + 500 original KOSIF styles)."""
import json
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import style_library as L


class StyleLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = L.load()
        cls.ks = [s for s in cls.lib["styles"] if s["source"] == "ks"]
        cls.fa = [s for s in cls.lib["styles"] if s["source"] == "fa"]

    def test_counts_and_ids(self):
        self.assertEqual(len(self.fa), 86)
        self.assertEqual([s["id"] for s in self.ks], ["KS-%03d" % i for i in range(1, 501)])
        ks_groups = [g for g in self.lib["groups"] if g["source"] == "ks"]
        self.assertEqual(len(ks_groups), 20)
        for g in ks_groups:
            self.assertEqual(sum(1 for s in self.ks if s["group"] == g["id"]), 25, g["id"])

    def test_names_unique_and_distinct_from_the_site(self):
        names = [s["name"].casefold() for s in self.lib["styles"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len({s["name_ar"] for s in self.lib["styles"]}), 586)
        self.assertEqual(len({s["slug"] for s in self.ks}), 500)

    def test_every_record_is_complete(self):
        for s in self.lib["styles"]:
            self.assertIn(s["motif"], L.MOTIFS, s["id"])
            self.assertIn(s["texture"], L.TEXTURES, s["id"])
            self.assertEqual(len(s["palette"]), 5, s["id"])
            self.assertGreater(len(s["look"]), 25, s["id"])
            self.assertGreater(len(s["logic"]), 15, s["id"])
            self.assertIn("{subject}", L.recipe(s), s["id"])
        for s in self.ks:
            self.assertTrue(s["prompt"].startswith("{subject}, rendered in the " + s["name"] + " style"))

    def test_lookup_by_id_slug_english_and_arabic(self):
        self.assertEqual(L.resolve(self.lib, "ks-001")["name"], "Zellige Starfield")
        self.assertEqual(L.resolve(self.lib, "zellige-starfield")["id"], "KS-001")
        self.assertEqual(L.resolve(self.lib, "زليج النجوم")["id"], "KS-001")
        self.assertEqual(L.resolve(self.lib, "FA-23")["slug"], "chalkboard-lesson")
        with self.assertRaises(ValueError):
            L.resolve(self.lib, " ")

    def test_find_ranks_arabic_and_english(self):
        self.assertEqual(L.find(self.lib, "Cyanotype")[0][1]["name"], "Cyanotype Sunprint")
        top = [s["id"] for _, s in L.find(self.lib, "خط عربي نيون", limit=3)]
        self.assertIn(L.resolve(self.lib, "Arabic Neon Script")["id"], top)
        self.assertTrue(any(s["group"] == "edible-media" for _, s in L.find(self.lib, "طعام حلوى", limit=5)))
        self.assertEqual(L.find(self.lib, "qzxvwk"), [])

    def test_prompt_fill_and_mix(self):
        p = L.prompt(L.resolve(self.lib, "KS-100"), "a mosque courtyard at dawn")
        self.assertTrue(p["prompt"].startswith("a mosque courtyard at dawn, rendered in the"))
        m = L.prompt(L.resolve(self.lib, "FA-04"), "photosynthesis", mix=L.resolve(self.lib, "KS-426"))
        self.assertIn("Accent (about 30%", m["prompt"])
        self.assertEqual(m["mix"], "KS-426")
        with self.assertRaises(ValueError):
            L.prompt(L.resolve(self.lib, "KS-100"), "x", mix=L.resolve(self.lib, "KS-100"))
        with self.assertRaises(ValueError):
            L.prompt(L.resolve(self.lib, "KS-100"), "  ")

    def test_every_swatch_is_valid_deterministic_svg(self):
        seen = set()
        for s in self.lib["styles"]:
            svg = L.swatch_svg(s)
            self.assertEqual(svg, L.swatch_svg(s))
            root = ET.fromstring(svg)
            self.assertTrue(root.tag.endswith("svg"))
            self.assertEqual(root.get("viewBox"), "0 0 480 320")
            self.assertNotIn("<image", svg)
            self.assertNotIn("http://", svg.replace("http://www.w3.org/2000/svg", ""))
            seen.add(svg)
        self.assertEqual(len(seen), 586)

    def test_catalog_html_lists_every_style(self):
        out = Path(tempfile.mkdtemp()) / "cat"
        try:
            idx, styles = L.catalog(self.lib, out)
            self.assertEqual(len(styles), 586)
            page = idx.read_text(encoding="utf-8")
            for s in self.lib["styles"]:
                self.assertIn(">%s<" % s["id"], page)
                self.assertTrue((out / "swatches" / (s["id"] + ".svg")).is_file())
            one = Path(tempfile.mkdtemp()) / "g"
            _, part = L.catalog(self.lib, one, groups=["arabic-heritage"])
            self.assertEqual(len(part), 25)
            shutil.rmtree(one.parent)
        finally:
            shutil.rmtree(out.parent)

    def test_cli_refuses_overwrite(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            target = tmp / "a.svg"
            self.assertEqual(L.main(["swatch", "KS-001", "--out", str(target)]), 0)
            with self.assertRaises(SystemExit):
                L.main(["swatch", "KS-001", "--out", str(target)])
            (tmp / "full").mkdir()
            (tmp / "full" / "x").write_text("x")
            with self.assertRaises(SystemExit):
                L.main(["catalog", "--out", str(tmp / "full")])
        finally:
            shutil.rmtree(tmp)

    def test_rights_note_and_no_site_text(self):
        data = json.loads(L.DATA_KS.read_text(encoding="utf-8"))
        self.assertIn("never copied", data["rights_note"])
        site = json.loads(L.DATA_FA.read_text(encoding="utf-8"))
        self.assertEqual(site["scope"], "ALL_86_OF_86")
        self.assertEqual(set(data["site_swatches"]), {s["source_style_id"] for s in site["styles"]})


if __name__ == "__main__":
    unittest.main()
