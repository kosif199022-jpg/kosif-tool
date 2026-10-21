"""Privacy, correctness and search tests for KOSIF typography atlas."""
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import zipfile

import telegram_typography_atlas as A
from telegram_typography_atlas import scan, find, tag_text, clean_name, enrich_zip_archives, refresh

HAS_FONTTOOLS = importlib.util.find_spec("fontTools") is not None  # scan parses fonts; CI installs it
HAS_SCAN_DEPS = HAS_FONTTOOLS and all(importlib.util.find_spec(m) for m in ("bs4", "PIL"))
ARABIC = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"


def make_font(family=None, style="Regular", license_text=None, chars=ARABIC + "ABC"):
    """A tiny valid TrueType font built in memory (no third-party outlines)."""
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    names = [".notdef"] + [f"g{ord(c):04X}" for c in chars]
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap({ord(c): f"g{ord(c):04X}" for c in chars})
    pen = TTGlyphPen(None)
    pen.moveTo((0, 0)); pen.lineTo((0, 500)); pen.lineTo((400, 500)); pen.closePath()
    box = pen.glyph()
    fb.setupGlyf({n: box for n in names})
    fb.setupHorizontalMetrics({n: (500, 0) for n in names})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    nm = {"styleName": style}
    if family:
        nm["familyName"] = family
    if license_text:
        nm["licenseDescription"] = license_text
    fb.setupNameTable(nm)
    fb.setupOS2()
    fb.setupPost()
    buf = io.BytesIO()
    fb.save(buf)
    return buf.getvalue()


def fixture(root, font_bytes=b"INVALIDTTF"):
    root = Path(root)
    folder = root / "ChatExport_1"
    folder.mkdir()
    (folder / "photos").mkdir()
    (folder / "files").mkdir()
    html = """<html><div class="message service" id="message-1">channel setup</div>
<div class="message default"><div class="from_name">Private Sender</div><div class="text">
خط كوفي هندسي لتصميم شعار — PrivateName phone +966555555555 https://t.me/privatechannel
</div><a href="photos/a.jpg">photo</a></div>
<div class="message default"><div class="from_name">Someone Else</div>
<div class="text">خط رقعة وفرشاة عربي للتحريك</div><a href="files/My Secret Name.ttf">asset</a></div>
</html>"""
    (folder / "messages.html").write_text(html, encoding="utf8")
    from PIL import Image
    Image.new("RGB", (9, 11), (14, 55, 86)).save(folder / "photos/a.jpg")
    (folder / "files/My Secret Name.ttf").write_bytes(font_bytes)
    (folder / "files/Mr. Ahmed notes").write_bytes(b"x")       # text after a dot is not an extension
    (folder / "files/unused.zip").write_bytes(b"INVALID_ARCHIVE")
    return folder


def public_index(fonts, **extra):
    base = {"schema": "kosif.telegram-typography-index.v2", "scan_scope": {"unique_font_binaries": 1},
            "topic_hits_from_message_text": {"kufi": 3}, "fonts": fonts, "limitations": ["ZIP/RAR members were not recursively inspected"]}
    base.update(extra)
    return base


def font_row(i, family, style="Regular", tags=None, lic="unknown-no-license-proof", **kw):
    row = {"sha256": f"{i:064x}", "catalog_id": f"type-{i:016x}", "family": family, "style": style, "parsed": True,
           "tags": tags if tags is not None else tag_text(family + " " + style), "license_status": lic,
           "has_arabic": True, "has_latin": False, "arabic_codepoints": 100 + i, "redistribution_approved": False}
    row.update(kw)
    return row


class TaggingAndCleaning(unittest.TestCase):
    def test_detect_arabic_topics(self):
        tags = tag_text("خط كوفي وخط رقعة لعمل شعار حديث")
        self.assertTrue({"arabic", "kufi", "ruqah", "logo", "modern"}.issubset(set(tags)))

    def test_whole_words_and_arabic_spelling_variants(self):
        self.assertNotIn("latin", tag_text("Medad Platinum"))        # 'latin' inside 'Platinum'
        self.assertNotIn("arabic", tag_text("مخطوطة قديمة"))         # 'خط' inside 'مخطوطة'
        self.assertNotIn("brush", tag_text("Open Sans"))             # 'pen' inside 'Open'
        for spelling in ("رقعة", "رقعه", "الرقعة", "بالرقعة"):
            self.assertIn("ruqah", tag_text(spelling), spelling)
        self.assertIn("kids", tag_text("خط أطفال"))

    def test_second_review_tagging_fixes(self):
        self.assertEqual(tag_text("نسخة تجريبية"), [])            # a copy/version, not Naskh
        self.assertNotIn("arabic", tag_text("خطة تسويق"))           # a plan, not a font
        self.assertIn("thuluth", tag_text("DecoTypeThuluthII"))      # camelCase is split
        self.assertIn("bold", tag_text("SemiBold"))
        self.assertIn("light", tag_text("Arabic_ExtraLight"))
        self.assertNotIn("bold", tag_text("Ultra Light"))
        self.assertIn("display", tag_text("تايبوغرافي"))
        self.assertIn("kufi", tag_text("الخطوط الكوفية"))
        self.assertIn("diwani", tag_text("Diwany Pro"))
        self.assertNotIn("calligraphy", tag_text("خط عربي"))         # 'Arabic font' is not a calligraphy request
        self.assertIn("kufi", tag_text("كوفی"))                      # Persian ی folds to ي

    def test_sanitize_names(self):
        self.assertNotIn("someone@example.com", clean_name("Font someone@example.com"))
        self.assertNotIn("+966555555555", clean_name("Logo +966555555555"))
        self.assertEqual(clean_name("https://www.behance.net/SomeDesigner"), "")
        self.assertEqual(clean_name("Lifta Stencil @behfont"), "Lifta Stencil")
        self.assertEqual(clean_name("Kufi t.me/secretchannel"), "Kufi")
        self.assertEqual(clean_name("Unlicenced font from LucasFonts.com"), "Unlicenced font from")
        self.assertEqual(clean_name("Font.company Bold"), "Font.company Bold")

    def test_license_wording(self):
        self.assertEqual(A.license_from_text("Licensed under the SIL Open Font License, Version 1.1"), "OFL-claimed-unverified")
        self.assertEqual(A.license_from_text("", "ABC Favorit Arabic Unlicensed Trial"), "restricted-or-custom-review")
        self.assertEqual(A.license_from_text("Free for personal use only. OFL"), "restricted-or-custom-review")  # restriction wins
        self.assertFalse(A.restricted_words("Free for personal and commercial use"))
        self.assertTrue(A.restricted_words("Fun Play Arabic_DEMO"))
        self.assertFalse(A.restricted_words("Relic Demotic"))
        self.assertTrue(A.restricted_words("خط نسخة تجريبية"))
        self.assertEqual(A.license_from_text("Licensed under the SIL Open Font License", "Ink Brush Arabic_DEMO"), "restricted-or-custom-review")
        self.assertEqual(A.license_from_text(""), "unknown-no-license-proof")

    def test_negated_license_and_family_keys(self):
        self.assertEqual(A.license_from_text("This font is not licensed for redistribution"), "restricted-or-custom-review")
        self.assertEqual(A.family_key({"family": ".", "parsed": True}), "")
        self.assertEqual(A.family_key({"family": "", "parsed": False}), "")
        self.assertEqual(A.family_key({"family": " Cairo ", "parsed": True}), "cairo")

    def test_extensions_never_carry_file_name_text(self):
        self.assertEqual(A.ext_of("Mr. Ahmed notes"), "(other)")
        self.assertEqual(A.ext_of("A.TTF"), ".ttf")
        self.assertEqual(A.ext_of(".DS_Store"), "")


class Search(unittest.TestCase):
    def setUp(self):
        self.catalog = {"fonts": [
            font_row(1, "Kufi Geometric", "Bold", lic="OFL-claimed-unverified"),
            font_row(2, "Kufi Geometric", "Regular"),
            font_row(3, "Kufi Geometric", "Regular"),
            font_row(4, "Latin Sans", has_arabic=False, arabic_codepoints=0),
            font_row(5, "Aref Ruqaa", lic="OFL-claimed-unverified"),
            font_row(6, "Big Display", "Black"),
            font_row(7, "Somar Rounded", "Medium"),
        ]}

    def test_search_by_font_metadata_without_sensitive_fields(self):
        result = find(self.catalog, "kufi", has_arabic=True)
        self.assertEqual(len(result), 1)                              # one row per family
        self.assertEqual(result[0]["family"], "Kufi Geometric")
        self.assertEqual(result[0]["files"], 3)
        self.assertEqual(result[0]["styles"], ["Bold", "Regular"])
        self.assertEqual(result[0]["license_status"], "OFL-claimed-unverified")  # open-claimed copy represents the family
        self.assertTrue(result[0]["license_mixed"])
        self.assertEqual(find(self.catalog, "latin", has_arabic=True), [])
        self.assertNotIn("relative_source", json.dumps(result))

    def test_arabic_style_words_and_open_filter(self):
        self.assertEqual(find(self.catalog, "خط رقعة")[0]["family"], "Aref Ruqaa")
        self.assertEqual(find(self.catalog, "الرقعه")[0]["family"], "Aref Ruqaa")
        self.assertEqual({r["family"] for r in find(self.catalog, "kufi", license_filter="open")}, {"Kufi Geometric"})
        self.assertEqual(find(self.catalog, "rounded", license_filter="open"), [])

    def test_variable_fonts_can_be_asked_for(self):
        self.catalog["fonts"].append(font_row(8, "Flex Sans", variable=True))
        self.assertEqual([r["family"] for r in find(self.catalog, "variable")], ["Flex Sans"])
        self.assertEqual(find(self.catalog, "خط متغير")[0]["family"], "Flex Sans")

    def test_exact_family_names_rank_first_and_latin_filter(self):
        self.catalog["fonts"] += [font_row(10, "Hafez 1"), font_row(11, "Hafez 2"), font_row(12, "aref_naskh"),
                                  font_row(13, "Noto Naskh Arabic", has_latin=True, lic="OFL-claimed-unverified")]
        self.assertEqual(find(self.catalog, "Hafez 2")[0]["family"], "Hafez 2")
        self.assertEqual(find(self.catalog, "aref naskh")[0]["family"], "aref_naskh")
        self.assertEqual([r["family"] for r in find(self.catalog, "naskh", need_latin=True)], ["Noto Naskh Arabic"])
        row = find(self.catalog, "kufi")[0]
        self.assertEqual(row["styles"][0], row["style"])        # the shown style leads its list

    def test_rare_request_words_borrow_nearby_styles(self):
        self.assertIn("Big Display", [r["family"] for r in find(self.catalog, "شعار")])
        self.assertIn("Somar Rounded", [r["family"] for r in find(self.catalog, "خط أطفال")])


class Refresh(unittest.TestCase):
    def test_refresh_is_deterministic_private_safe_and_consistent(self):
        fonts = [font_row(1, "Medad Platinum", tags=["latin"]),
                 font_row(2, "ABC Favorit Arabic Unlicensed Trial"),
                 font_row(3, "Ramadan Hossam", postscript_name="https://www.behance.net/SomeDesigner"),
                 font_row(4, "Lifta Stencil @behfont"),
                 {"sha256": f"{9:064x}", "catalog_id": "type-9", "family": "", "style": "", "parsed": False,
                  "license_status": "uninspected", "tags": [], "redistribution_approved": False}]
        fonts.append(font_row(5, "Kufi t.me/secretchannel"))
        fonts.append(font_row(6, "Fun Play Arabic_DEMO"))
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "old.json"
            src.write_text(json.dumps(public_index(fonts, visual_sample_review={"sample_size": 80}), ensure_ascii=False), encoding="utf8")
            out1, out2 = Path(tmp) / "a.json", Path(tmp) / "b.json"
            refresh(src, out1)
            refresh(src, out2)
            self.assertEqual(out1.read_bytes(), out2.read_bytes())
            text = out1.read_text(encoding="utf8")
            d = json.loads(text)
            self.assertNotIn("https://", text)
            self.assertNotIn("@behfont", text)
            self.assertNotIn("t.me", text)
            by = {f["catalog_id"]: f for f in d["fonts"]}
            self.assertEqual(by[f"type-{6:016x}"]["license_status"], "restricted-or-custom-review")
            self.assertEqual(d["topic_hits_tagger"], "substring-pre-v3")
            self.assertEqual(d["scan_scope"]["unparsed_font_binaries"], 1)
            self.assertEqual(by[f"type-{1:016x}"]["tags"], [])
            self.assertEqual(by[f"type-{2:016x}"]["license_status"], "restricted-or-custom-review")
            self.assertEqual(d["schema"], A.SCHEMA)
            self.assertEqual(d["scan_scope"]["unique_font_binaries"], 7)
            self.assertEqual(d["script_coverage"]["unique_font_families"], 6)    # the unparsed '' is not a family
            self.assertEqual(len(d["typography_design_ideas"]), len(A.IDEA_PATTERNS))
            self.assertFalse(any("not recursively inspected" in x for x in d["limitations"]))
            self.assertTrue(all(f["redistribution_approved"] is False for f in d["fonts"]))
            with self.assertRaisesRegex(ValueError, "new files|distinct"):
                refresh(src, out1)
            with self.assertRaisesRegex(ValueError, "distinct"):
                refresh(src, src)

    def test_committed_index_is_refreshed_and_private_safe(self):
        idx = sorted((Path(__file__).resolve().parents[1] / "data").glob("telegram-typography-catalog-*.json"))[-1]
        text = idx.read_text(encoding="utf8")
        d = json.loads(text)
        self.assertEqual(d["schema"], A.SCHEMA)
        self.assertEqual(d["scan_scope"]["unique_font_binaries"], len(d["fonts"]))
        self.assertEqual(len({f["sha256"] for f in d["fonts"]}), len(d["fonts"]))
        self.assertFalse(any(f["redistribution_approved"] for f in d["fonts"]))
        for bad in ("https://", "http://", "t.me/", ".com", "C:\\\\Users", "/home/", "\"relative_source\"", "\"zip_member\"", "\"root_path\""):
            self.assertNotIn(bad, text)
        self.assertEqual(sum(d["font_license_status_counts"].values()), len(d["fonts"]))


@unittest.skipUnless(HAS_SCAN_DEPS, "scan needs fontTools, beautifulsoup4 and Pillow")
class ScanAndZips(unittest.TestCase):
    def test_complete_html_scan_safe_public(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = Path(tmp) / "input"; r.mkdir()
            fixture(r, make_font(family=None, license_text=None))          # a valid font with no family name
            public = Path(tmp) / "public.json"
            private = Path(tmp) / "private.json"
            data = scan(r, public, private)
            self.assertEqual(data["scan_scope"]["export_folders"], 1)
            self.assertEqual(data["scan_scope"]["messages_parsed"], 2)
            self.assertEqual(data["scan_scope"]["font_files_seen"], 1)
            self.assertEqual(data["scan_scope"]["images_seen"], 1)
            self.assertEqual(data["scan_scope"]["unparsed_font_binaries"], 0)
            self.assertEqual(len(data["typography_design_ideas"]), len(A.IDEA_PATTERNS))
            self.assertEqual(data["fonts"][0]["family"], "Unnamed font")     # never the private file name
            self.assertTrue(data["fonts"][0]["has_arabic"])
            txt = public.read_text(encoding="utf8")
            for secret in ("Private Sender", "PrivateName", "Someone Else", "phone +966", "t.me", str(r), "a.jpg",
                           "My Secret Name", "secret name", " ahmed notes"):
                self.assertNotIn(secret, txt)
            self.assertIn("My Secret Name.ttf", private.read_text(encoding="utf8"))
            self.assertFalse(data["fonts"][0]["redistribution_approved"])
            self.assertEqual(data["scan_scope"]["images_fully_reviewed"], 0)
            self.assertEqual(data["scan_scope"]["archives_unpacked"], 0)

    def test_symlinked_export_folders_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = Path(tmp) / "input"; r.mkdir()
            fixture(r)
            outside = Path(tmp) / "outside"; outside.mkdir()
            fixture(outside)
            os.symlink(outside / "ChatExport_1", r / "ChatExport_2")
            data = scan(r, Path(tmp) / "p.json", Path(tmp) / "q.json")
            self.assertEqual(data["scan_scope"]["export_folders"], 1)

    def test_zip_scan_never_extracts_fonts_and_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "input"; root.mkdir()
            folder = fixture(root)
            z = folder / "files" / "bundle.ZIP"                               # upper-case extension is still a ZIP
            with zipfile.ZipFile(z, "w", compression=zipfile.ZIP_DEFLATED) as f:
                f.writestr("fonts/valid.ttf", make_font("Zip Kufi", license_text="SIL Open Font License"))
                f.writestr("fonts/invalid.ttf", b"NOT_A_VALID_TTF" * 3)
                f.writestr("../escape.ttf", b"PATH TRAVERSAL MEMBER LONG ENOUGH" * 2)   # ≥16 bytes: only the path check stops it
                f.writestr("C:/abs.ttf", b"ABSOLUTE MEMBER, LONG ENOUGH TOO" * 2)
                f.writestr("notes.txt", b"Private Sender data - local only")
            original = Path(tmp) / "public.json"
            prv = Path(tmp) / "private.json"
            scan(root, original, prv)
            out = Path(tmp) / "with-archives.json"
            newpriv = Path(tmp) / "with-private.json"
            result = enrich_zip_archives(root, original, prv, out, newpriv)
            self.assertEqual(result["zip_archives_scanned"], 2)
            self.assertEqual(result["unreadable_zip"], 1)
            self.assertEqual(result["font_added_unique"], 2)
            self.assertEqual(result["excluded"].get("unsafe_or_encrypted_member", 0), 2)
            d = json.loads(out.read_text(encoding="utf8"))
            self.assertEqual(d["schema"], A.SCHEMA)
            self.assertEqual(len(d["fonts"]), 3)
            self.assertEqual(d["scan_scope"]["unique_font_binaries"], 3)
            self.assertEqual(d["scan_scope"]["loose_unique_font_binaries"], 1)
            zipped = [f for f in d["fonts"] if f.get("family") == "Zip Kufi"][0]
            self.assertEqual(zipped["license_status"], "OFL-claimed-unverified")
            kufi = [i for i in d["typography_design_ideas"] if i["id"] == "kufi-grid"][0]
            self.assertIn(zipped["catalog_id"], kufi["related_font_ids"])  # ideas are rebuilt over ZIP fonts too
            self.assertNotIn("Private Sender", out.read_text(encoding="utf8"))
            self.assertNotIn("escape.ttf", newpriv.read_text(encoding="utf8"))
            self.assertFalse((root / "escape.ttf").exists())
            self.assertIn("bundle.ZIP", newpriv.read_text(encoding="utf8"))

    def test_font_collections_and_zips_outside_exports(self):
        from fontTools.ttLib import TTFont, TTCollection
        with tempfile.TemporaryDirectory() as tmp:
            col = TTCollection()
            col.fonts = [TTFont(io.BytesIO(make_font("Collected Naskh"))), TTFont(io.BytesIO(make_font("Second Face")))]
            buf = io.BytesIO()
            col.save(buf)
            rec = A.font_from_bytes(buf.getvalue(), ".ttf")
            self.assertTrue(rec["parsed"])
            self.assertTrue(rec.get("collection"))
            self.assertEqual(rec["family"], "Collected Naskh")
            root = Path(tmp) / "input"; root.mkdir()
            fixture(root)
            with zipfile.ZipFile(root / "stray.zip", "w") as f:            # outside ChatExport*: not part of the exports
                f.writestr("x.ttf", make_font("Stray"))
            pub, prv = Path(tmp) / "p.json", Path(tmp) / "q.json"
            scan(root, pub, prv)
            res = enrich_zip_archives(root, pub, prv, Path(tmp) / "c.json", Path(tmp) / "d.json")
            self.assertEqual(res["zip_archives_scanned"], 1)                # only files/unused.zip inside the export

    def test_enrich_refuses_shared_or_inside_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "input"; root.mkdir()
            fixture(root)
            pub, prv = Path(tmp) / "p.json", Path(tmp) / "q.json"
            scan(root, pub, prv)
            same = Path(tmp) / "same.json"
            with self.assertRaisesRegex(ValueError, "distinct"):
                enrich_zip_archives(root, pub, prv, same, same)
            with self.assertRaisesRegex(ValueError, "outside"):
                enrich_zip_archives(root, pub, prv, root / "x.json", Path(tmp) / "y.json")

    def test_enrich_refuses_an_already_enriched_catalog_and_private_files_in_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "input"; root.mkdir()
            fixture(root)
            pub, prv = Path(tmp) / "p.json", Path(tmp) / "q.json"
            scan(root, pub, prv)
            enrich_zip_archives(root, pub, prv, Path(tmp) / "c.json", Path(tmp) / "d.json")
            with self.assertRaisesRegex(ValueError, "already enriched"):
                enrich_zip_archives(root, Path(tmp) / "c.json", Path(tmp) / "d.json", Path(tmp) / "e.json", Path(tmp) / "f.json")
            repo = Path(tmp) / "checkout"; (repo / ".git").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "outside any git checkout"):
                scan(root, Path(tmp) / "p2.json", repo / "private.json")

    def test_member_reads_are_bounded_whatever_the_header_says(self):
        with tempfile.TemporaryDirectory() as tmp:
            z = Path(tmp) / "a.zip"
            with zipfile.ZipFile(z, "w", compression=zipfile.ZIP_DEFLATED) as f:
                f.writestr("big.ttf", b"\0" * 5000)
            old = A.MAX_MEMBER
            A.MAX_MEMBER = 1000
            try:
                with zipfile.ZipFile(z) as src:
                    m = src.infolist()[0]
                    self.assertTrue(A._member_unsafe(m))
                    with self.assertRaises(ValueError):
                        A._read_bounded(src, m)
            finally:
                A.MAX_MEMBER = old

    def test_reject_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "input"; root.mkdir()
            fixture(root)
            existing = Path(tmp) / "exist.json"; existing.write_text("KEEP")
            with self.assertRaisesRegex(ValueError, "new files"):
                scan(root, existing, Path(tmp) / "private.json")
            self.assertEqual(existing.read_text(), "KEEP")


if __name__ == "__main__":
    unittest.main(verbosity=2)
