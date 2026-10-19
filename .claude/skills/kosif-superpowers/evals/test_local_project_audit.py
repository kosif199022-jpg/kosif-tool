"""Safe read-only project and archive triage tests."""
import json
import pathlib
import sys
import tempfile
import unittest
import zipfile

SK=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/'scripts'))
import local_project_audit as a

class LocalProjectAuditTests(unittest.TestCase):
    def test_complete_small_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp)
            (p/'theme.js').write_text('document.querySelector("x").innerHTML="safe"; addEventListener("load",()=>{});',encoding='utf-8')
            (p/'reference.png').write_bytes(b'\x89PNG'+b'0'*70)
            (p/'library.dll').write_bytes(b'MZ'+b'0'*60)
            with zipfile.ZipFile(p/'pack.zip','w') as z:
                z.writestr('inner/theme.css','body{color:red}')
            report=a.scan(p)
            self.assertEqual(report['files'],4)
            self.assertEqual(report['routes']['ghidra_rea_candidate'],1)
            self.assertEqual(report['routes']['source_review'],1)
            self.assertEqual(report['routes']['image_asset'],1)
            self.assertEqual(report['routes']['archive_metadata_only'],1)
            self.assertEqual(report['unreadable'],0)
            self.assertEqual(next(r for r in report['samples'] if r['path']=='pack.zip')['zip']['entries'],1)
            self.assertEqual(report['indicators_files']['dom_html'],1)

    def test_zip_traversal_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=pathlib.Path(tmp)/'evil.zip'
            with zipfile.ZipFile(path,'w') as z:
                z.writestr('../outside.exe',b'MZ')
            record=next(r for r in a.scan(tmp)['samples'] if r['path']=='evil.zip')
            self.assertEqual(record['zip']['unsafe_path_count'],1)
            self.assertFalse((pathlib.Path(tmp).parent/'outside.exe').exists())

    def test_symlinks_not_followed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)
            (root/'target.txt').write_text('x')
            try: (root/'link.txt').symlink_to(root/'target.txt')
            except OSError: self.skipTest('Windows no symlink permission')
            report=a.scan(root)
            self.assertEqual(report['files'],1)
            self.assertTrue(any(r['reason']=='symlink' for r in report['skipped']))

    def test_reject_file_and_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp)/'file.txt';p.write_text('x')
            with self.assertRaises(ValueError):a.scan(p)
            with self.assertRaises(FileNotFoundError):a.scan(pathlib.Path(tmp)/'not-here')

if __name__=='__main__':unittest.main()
