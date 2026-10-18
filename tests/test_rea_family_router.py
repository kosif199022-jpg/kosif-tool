"""KOSIF source/full REA capability router contracts."""
import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/".claude/skills/kosif-superpowers/scripts/rea_family_router.py"
s=importlib.util.spec_from_file_location("rea_family_router",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class FamilyTests(unittest.TestCase):
 def test_all_families_supported_as_guidance(self):
  self.assertGreaterEqual(len(m.FAMILIES),16)
  self.assertEqual(m.route("apk")["family"],"android")
  self.assertEqual(m.route("javascript")["family"],"javascript")
  self.assertEqual(m.route("qlog")["family"],"captures")
 def test_does_not_claim_runtime_success(self):
  for intent in m.INTENT:
   res=m.route(intent)
   self.assertFalse(res["verified"])
   self.assertFalse(res["executed"])
   self.assertIn("route_only",res["status"])
 def test_font_not_hijacked_by_rea(self):
  self.assertEqual(m.route("identify Arabic font")["status"],"not_an_rea_target")
 def test_no_setup_execution(self):
  import inspect
  src=inspect.getsource(m)
  self.assertNotIn("shell=True",src)
  self.assertNotIn("subprocess.run",src)
if __name__=="__main__":unittest.main()
