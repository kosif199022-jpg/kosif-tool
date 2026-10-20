"""Privacy, correctness and search tests for KOSIF typography atlas."""
import json
from pathlib import Path
import tempfile
import unittest
from telegram_typography_atlas import scan,find,tag_text,clean_name,enrich_zip_archives

def fixture(root):
    root=Path(root)
    folder=root/"ChatExport_1"
    folder.mkdir()
    (folder/"photos").mkdir()
    (folder/"files").mkdir()
    html="""<html><div class="message service" id="message-1">channel setup</div>
<div class="message default"><div class="from_name">Private Sender</div><div class="text">
خط كوفي هندسي لتصميم شعار — PrivateName phone +966555555555
</div><a href="photos/a.jpg">photo</a></div>
<div class="message default"><div class="from_name">Someone Else</div>
<div class="text">خط رقعة وفرشاة عربي للتحريك</div><a href="files/font.ttf">asset</a></div>
</html>"""
    (folder/"messages.html").write_text(html,encoding="utf8")
    from PIL import Image
    Image.new("RGB",(9,11),(14,55,86)).save(folder/"photos/a.jpg")
    (folder/"files/font.ttf").write_bytes(b"INVALIDTTF")  # robust fallback
    (folder/"files/unused.zip").write_bytes(b"INVALID_ARCHIVE")
    return folder

class TypographyAtlasTests(unittest.TestCase):
    def test_detect_arabic_topics(self):
        tags=tag_text("خط كوفي وخط رقعة لعمل شعار حديث")
        self.assertTrue({"arabic","kufi","ruqah","logo","modern"}.issubset(set(tags)))

    def test_sanitize_names(self):
        self.assertNotIn("someone@example.com",clean_name("Font someone@example.com"))
        self.assertNotIn("+966555555555",clean_name("Logo +966555555555"))

    def test_complete_html_scan_safe_public(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp)/"input";r.mkdir()
            fixture(r)
            public=Path(tmp)/"public.json"
            private=Path(tmp)/"private.json"
            data=scan(r,public,private)
            self.assertEqual(data["scan_scope"]["export_folders"],1)
            self.assertEqual(data["scan_scope"]["messages_parsed"],2)
            self.assertEqual(data["scan_scope"]["font_files_seen"],1)
            self.assertEqual(data["scan_scope"]["images_seen"],1)
            self.assertEqual(data["scan_scope"]["unparsed_font_binaries"],1)
            self.assertEqual(len(data["typography_design_ideas"]),15)
            txt=public.read_text(encoding="utf8")
            self.assertNotIn("Private Sender",txt)
            self.assertNotIn("PrivateName",txt)
            self.assertNotIn("Someone Else",txt)
            self.assertNotIn("phone +966",txt)
            self.assertNotIn(str(r),txt)
            self.assertNotIn("a.jpg",txt)
            self.assertNotIn("font.ttf",txt)
            self.assertIn("font.ttf",private.read_text(encoding="utf8"))
            self.assertFalse(data["fonts"][0]["redistribution_approved"])
            self.assertEqual(data["scan_scope"]["images_semantically_reviewed"],0)
            self.assertEqual(data["scan_scope"]["archives_unpacked"],0)

    def test_search_by_font_metadata_without_sensitive_fields(self):
        catalog={"fonts":[
            {"catalog_id":"type-1","family":"Kufi Geometric","style":"Bold",
             "has_arabic":True,"arabic_codepoints":190,"tags":["kufi","bold"],
             "license_status":"unknown-no-license-proof"},
            {"catalog_id":"type-2","family":"Latin Sans","style":"Regular",
             "has_arabic":False,"arabic_codepoints":0,"tags":["latin"],
             "license_status":"unknown-no-license-proof"}]}
        result=find(catalog,"kufi",has_arabic=True)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]["font_id"],"type-1")
        self.assertEqual(find(catalog,"latin",has_arabic=True),[])

    def test_zip_scan_never_extracts_fonts_and_rejects_traversal(self):
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"input";root.mkdir()
            folder=fixture(root)
            z=folder/"files"/"bundle.zip"
            with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED) as f:
                f.writestr("fonts/invalid.ttf",b"NOT_A_VALID_TTF"*3)
                f.writestr("../escape.ttf",b"NOPE")
                f.writestr("notes.txt",b"Private Sender data - local only")
            original=Path(tmp)/"public.json"
            prv=Path(tmp)/"private.json"
            scan(root,original,prv)
            out=Path(tmp)/"with-archives.json"
            newpriv=Path(tmp)/"with-private.json"
            result=enrich_zip_archives(root,original,prv,out,newpriv)
            self.assertEqual(result["zip_archives_scanned"],2)
            self.assertEqual(result["unreadable_zip"],1)
            self.assertEqual(result["font_added_unique"],1)
            self.assertGreaterEqual(result["excluded"].get("unsafe_or_encrypted_member",0),1)
            d=json.loads(out.read_text(encoding="utf8"))
            self.assertEqual(d["schema"],"kosif.telegram-typography-index.v2")
            self.assertEqual(len(d["fonts"]),2)
            self.assertNotIn("Private Sender",out.read_text(encoding="utf8"))
            self.assertFalse((root/"escape.ttf").exists())
            self.assertIn("bundle.zip",newpriv.read_text(encoding="utf8"))

    def test_reject_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"input";root.mkdir()
            fixture(root)
            existing=Path(tmp)/"exist.json";existing.write_text("KEEP")
            with self.assertRaisesRegex(ValueError,"new files"):
                scan(root,existing,Path(tmp)/"private.json")
            self.assertEqual(existing.read_text(),"KEEP")

if __name__=="__main__":
    unittest.main(verbosity=2)
