"""Reproducible Blender 5.2 scene-upgrade tests, with real Blender when installed."""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from blender_cycles_render import executable

HERE=Path(__file__).resolve().parent


def launch(blender, script, parameters):
    cmd=[blender,"--background","--factory-startup","--disable-autoexec",
         "--python-exit-code","7","--python",str(script),"--",*map(str,parameters)]
    return subprocess.run(cmd,capture_output=True,text=True,timeout=55,errors="replace")


@unittest.skipUnless(executable(None,"blender"),"Blender not present locally")
class BlenderFurIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blender=executable(None,"blender")
        cls.dir=tempfile.TemporaryDirectory(prefix="kosif-fur-tests-")
        cls.path=Path(cls.dir.name)
        cls.original=cls.path/"original.blend"
        cls.upgraded=cls.path/"upgraded.blend"
        made=launch(cls.blender,HERE/"blender_rescue_scene.py",[cls.original])
        if made.returncode:
            raise AssertionError("base scene failed: "+(made.stdout+made.stderr)[-1000:])
        result=launch(cls.blender,HERE/"blender_cat_fur_upgrade.py",
                      ["--source",cls.original,"--output",cls.upgraded,
                       "--fur-count",320,"--seed",2307])
        if result.returncode:
            raise AssertionError("fur upgrade failed: "+(result.stdout+result.stderr)[-1500:])
        cls.render_log=result.stdout
        cls.properties=cls.inspect()

    @classmethod
    def tearDownClass(cls):
        cls.dir.cleanup()

    @classmethod
    def inspect(cls):
        script=cls.path/"inspect.py"
        script.write_text(
            """import bpy,json
s=bpy.context.scene
cat=bpy.data.objects['CAT_ANIMATED_GROUP']
tor=bpy.data.objects['KOSIF_CAT_FUR_TORSO']
head=bpy.data.objects['KOSIF_CAT_FUR_HEAD']
assert tor.parent.name=='cat torso' and head.parent.name=='cat head'
s.frame_set(1); z1=cat.location.z; x1=cat.location.x
s.frame_set(24);z24=cat.location.z;x24=cat.location.x
print('KOSIF_FUR_INSPECTION',json.dumps({
'fur_torso':len(tor.data.splines),
'fur_head':len(head.data.splines),
'whiskers':len(bpy.data.objects['KOSIF_CAT_WHISKERS'].data.splines),
'camera':s.camera.name,
'cycles_engine':s.render.engine,
'objects':len(bpy.data.objects),
'eye_shines':len([o for o in bpy.data.objects if o.name.startswith('KOSIF-eye-shine')]),
'human_eye_details':len([o for o in bpy.data.objects if o.name.startswith('KOSIF_RESCUER_EYE')]),
'road_bump':any(n.bl_idname=='ShaderNodeBump' for n in bpy.data.materials['charcoal asphalt'].node_tree.nodes),
'fur_noise':any(n.bl_idname=='ShaderNodeTexNoise' for n in bpy.data.materials['cat orange-gold fur'].node_tree.nodes),
'root_z1':z1,'root_z24':z24,'root_x1':x1,'root_x24':x24
}),flush=True)
""",encoding="utf-8")
        cmd=[cls.blender,"--background","--factory-startup","--disable-autoexec",
             str(cls.upgraded),"--python-exit-code","7","--python",str(script)]
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=30,errors="replace")
        if r.returncode:raise AssertionError("inspection failed: "+(r.stdout+r.stderr)[-1400:])
        line=next((x for x in r.stdout.splitlines() if x.startswith("KOSIF_FUR_INSPECTION ")),"")
        if not line:raise AssertionError("No inspection proof: "+r.stdout[-1200:])
        return json.loads(line.split(" ",1)[1])

    def test_correct_strand_count(self):
        self.assertEqual(self.properties["fur_torso"]+self.properties["fur_head"],320)
        self.assertEqual(self.properties["whiskers"],6)

    def test_physically_shaded_materials(self):
        self.assertTrue(self.properties["road_bump"])
        self.assertTrue(self.properties["fur_noise"])
        self.assertEqual(self.properties["cycles_engine"],"CYCLES")

    def test_geometry_and_character_details(self):
        self.assertGreaterEqual(self.properties["objects"],64)
        self.assertEqual(self.properties["eye_shines"],2)
        self.assertEqual(self.properties["human_eye_details"],2)

    def test_motion_preserved_and_paws_grounded(self):
        self.assertAlmostEqual(self.properties["root_z1"],.066,places=3)
        self.assertAlmostEqual(self.properties["root_z24"],.066,places=3)
        self.assertNotEqual(self.properties["root_x1"],self.properties["root_x24"])

    def test_blend_is_real_editable_asset(self):
        self.assertTrue(self.upgraded.is_file())
        self.assertGreater(self.upgraded.stat().st_size,100000)
        self.assertIn("KOSIF_FUR_UPGRADE_VERIFIED",self.render_log)

    def test_duplicate_upgrade_denied_without_overwrite(self):
        original=self.upgraded.read_bytes()
        result=launch(self.blender,HERE/"blender_cat_fur_upgrade.py",
                      ["--source",self.original,"--output",self.upgraded])
        self.assertNotEqual(result.returncode,0)
        self.assertIn("Output must be new",result.stdout+result.stderr)
        self.assertEqual(original,self.upgraded.read_bytes())

    def test_invalid_fur_density_rejected(self):
        result=launch(self.blender,HERE/"blender_cat_fur_upgrade.py",
                      ["--source",self.original,"--output",self.path/"bad.blend",
                       "--fur-count",20000])
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.path/"bad.blend").exists())


if __name__=="__main__":
    unittest.main(verbosity=2)
