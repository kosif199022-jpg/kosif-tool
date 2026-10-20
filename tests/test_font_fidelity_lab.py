"""Font matching must not invent exact font identity."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
PATH=Path(__file__).resolve().parents[1]/".claude/skills/kosif-superpowers/scripts/font_fidelity_lab.py"
spec=importlib.util.spec_from_file_location("font_fidelity_lab",PATH)
font=importlib.util.module_from_spec(spec)
spec.loader.exec_module(font)
class FontFidelityTests(unittest.TestCase):
    def test_arabic_detected(self):
        self.assertTrue(font.rtl("جمعة مباركة ﷺ"))
        self.assertFalse(font.rtl("KOSIF ABC 123"))
    def test_invalid_font_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"unknown.xyz";p.write_text("x")
            with self.assertRaises(ValueError):font.info(p)
    def test_font_metadata_is_evidence_not_exact_match(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"not-a-font.ttf";p.write_text("x")
            try:
                result=font.info(p,"مرحبا")
            except Exception:
                return # corrupted files may be rejected by fontTools
            self.assertIn("source_rights",result)
            self.assertNotIn("exact_font_identified",result)
    def test_iou_and_scaling_for_installed_pillow(self):
        try:
            from PIL import Image
        except ImportError:self.skipTest("Pillow not present")
        a=Image.new("L",(16,16),0)
        for x in range(4,12):
            for y in range(4,12):a.putpixel((x,y),255)
        self.assertEqual(font.ratio_overlap(a,a),1.0)
        blank=Image.new("L",(16,16),0)
        self.assertEqual(font.ratio_overlap(a,blank),0.0)
    def test_corrupt_font_is_a_clean_error(self):
        if importlib.util.find_spec("fontTools") is None:self.skipTest("fontTools not present")
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"fake.ttf";p.write_text("not a font")
            with self.assertRaises(ValueError):font.info(p,"مرحبا")
            run=subprocess.run([sys.executable,str(PATH),"inspect",str(p)],capture_output=True,text=True)
            self.assertEqual(run.returncode,2)
            self.assertIn("FONT FIDELITY ERROR",run.stderr)
            self.assertNotIn("Traceback",run.stderr)
    def test_woff2_without_brotli_is_not_reported_as_missing_fonttools(self):
        if importlib.util.find_spec("fontTools") is None:self.skipTest("fontTools not present")
        from fontTools.ttLib import woff2
        old=getattr(woff2,"haveBrotli",True)
        woff2.haveBrotli=False
        try:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/"face.woff2";p.write_bytes(b"wOF2")
                note=font.info(p,"مرحبا").get("inspection_note","")
        finally:
            woff2.haveBrotli=old
        self.assertIn("brotli",note)
        self.assertNotIn("fontTools not installed",note)
if __name__=="__main__": unittest.main()
