import importlib.util
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

SCRIPT=Path(__file__).resolve().parents[1]/'scripts'/'repository_capability_packer.py'
spec=importlib.util.spec_from_file_location('packer',SCRIPT)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class Tests(unittest.TestCase):
 def test_inspect_and_pack_deterministic(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'src';root.mkdir();(root/'pyproject.toml').write_text('[project]\nname="demo"\n');(root/'main.py').write_text('print(1)\n');(root/'LICENSE').write_text('MIT');(root/'.env').write_text('DO_NOT_SHARE=SECRET');(root/'tests').mkdir();(root/'tests'/'test_main.py').write_text('assert True')
   r=p.inspect(root);self.assertEqual(r['safe_files'],4);self.assertFalse(r['runtime_verified']);self.assertTrue(any(x['capability_area']=='python' for x in r['potential_capabilities']))
   a=Path(t)/'a.zip';b=Path(t)/'b.zip';p.pack(root,a);p.pack(root,b);self.assertEqual(a.read_bytes(),b.read_bytes())
   with ZipFile(a) as z:
    self.assertNotIn('.env',z.namelist());self.assertIn('main.py',z.namelist())
 def test_archive_escape_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   z=Path(t)/'attack.zip'
   with ZipFile(z,'w') as out:out.writestr('../escape.py','yes')
   with self.assertRaises(p.UnsafeRepository):p.inspect(z)
 def test_archive_strip_one_root_and_no_duplicate(self):
  with tempfile.TemporaryDirectory() as t:
   z=Path(t)/'github.zip'
   with ZipFile(z,'w') as out:out.writestr('repo-abc/README.md','hello');out.writestr('repo-abc/main.py','pass')
   self.assertIn('main.py',p.inspect(z)['sha256_manifest'])
 def test_destination_inside_src_fails(self):
  with tempfile.TemporaryDirectory() as t:
   d=Path(t)/'repo';d.mkdir();(d/'main.py').write_text('hello')
   with self.assertRaises(p.UnsafeRepository):p.pack(d,d/'export.zip')
if __name__=='__main__':unittest.main()