"""Original shape snapping, drawing output, and Blender AST evidence tests."""
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
import unittest.mock

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import smart_draw as sd
import blender_api_audit as ba

def circle(cx=80,cy=80,r=40):
    return [[cx+r*math.cos(i*math.pi/8),cy+r*math.sin(i*math.pi/8)] for i in range(17)]

class SmartDrawTests(unittest.TestCase):
    def test_shape_assist(self):
        rect=[[20,20],[130,20],[130,100],[20,100],[20,20]]
        self.assertEqual(sd.classify(rect),"rectangle")
        self.assertEqual(sd.classify(circle()),"ellipse")
        self.assertEqual(sd.classify([[15,20],[50,20.3],[95,21],[150,20]]),"line")
        self.assertEqual(sd.classify([[20,20],[80,75],[135,28],[190,90]]),"freehand")

    def test_uses_original_paint_layers(self):
        doc={"schema":"kosif.smartdraw.v1","width":256,"height":256,
             "strokes":[{"points":circle(),"assist":True,"brush":"highlighter"},
                        {"points":[[15,15],[100,100]],"brush":"marker"}]}
        scene,matches=sd.to_scene(doc)
        self.assertEqual(matches[0]["recognized"],"ellipse")
        self.assertEqual(len(scene["layers"]),2)
        self.assertEqual(scene["layers"][0]["opacity"],.32)
        from creative_paint import paint,svg
        self.assertEqual(paint(scene).size,(256,256))
        self.assertIn("<ellipse",svg(scene))

    def test_malformed_input_rejected(self):
        good={"schema":"kosif.smartdraw.v1","width":256,"height":256,
              "strokes":[{"points":[[20,20],[80,90]]}]}
        for bad in [{"width":0},{"strokes":[{"points":[[20,20],[1e9,90]]}]},
                    {"strokes":[{"points":[[20,20],[80,90]],"brush":"eval"}]},
                    {"strokes":[{"points":[[20,20],[80,90]],"color":"url(javascript:xx)"}]}]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):sd.to_scene({**good,**bad})

    def test_blender_ast_fixtures_without_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"animation";p.mkdir()
            (p/"rig_ops.py").write_text("import bpy\nclass Apply(bpy.types.Operator):\n    pass\n\ndef run():\n    bpy.ops.mesh.primitive_cube_add()\n")
            r=ba.audit(temp)
            self.assertEqual(r["files_found"],1)
            self.assertEqual(r["parsed_files"],1)
            self.assertEqual(r["operator_class_types"]["bpy.types.Operator"],1)
            self.assertIn("bpy.ops.mesh.primitive_cube_add",r["bpy_ops_calls"])
            self.assertTrue(r["source_not_executed"])

    def test_blender_audit_cli_bad_inputs_are_usage_errors(self):
        import subprocess
        script=str(ROOT/"scripts"/"blender_api_audit.py")
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp);(base/"src").mkdir()
            (base/"src"/"ops.py").write_text("import bpy\nbpy.ops.mesh.primitive_cube_add()\n")
            run=lambda *a:subprocess.run([sys.executable,script,*a],capture_output=True,text=True,cwd=temp)
            for args,why in ((["nope"],"source folder not found"),
                             (["src","--output","missing/r.json"],"output folder does not exist"),
                             (["src","--output","src/r.json"],"inside inspected tree")):
                with self.subTest(args=args):
                    done=run(*args)
                    self.assertEqual(done.returncode,2)
                    self.assertIn(why,done.stderr)
                    self.assertNotIn("Traceback",done.stderr)
            self.assertEqual(run("src","--output","r.json").returncode,0)
            self.assertIn("bpy.ops.mesh.primitive_cube_add",json.loads((base/"r.json").read_text())["bpy_ops_calls"])
            with unittest.mock.patch.object(ba,"MAX_FILES",0):
                with self.assertRaisesRegex(ValueError,"more than 0"):ba.audit(base/"src")

if __name__=="__main__":unittest.main()
