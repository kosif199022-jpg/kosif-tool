"""Real pixel, animation and negative safety tests for independent paint engine."""
import importlib.util
import json
import math
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"creative_paint.py"
spec=importlib.util.spec_from_file_location("kosif_creative_paint",SCRIPT)
engine=importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

def demo():
    return {"schema":"kosif.paint.v1","width":300,"height":240,
      "background":"#EFE8D7","layers":[
        {"name":"graphic","shapes":[
          {"kind":"rectangle","x":5,"y":8,"width":48,"height":55,"fill":"#005500","stroke_width":0},
          {"kind":"ellipse","x":50,"y":50,"width":90,"height":90,"fill":"#CFA845"},
          {"kind":"polygon","points":[[20,155],[70,100],[120,155]],"fill":"#753F54"},
          {"kind":"brush","points":[[140,30,1],[180,100,2],[220,145,.5]],"stroke":"#17312A","stroke_width":7},
          {"kind":"line","points":[[0,200],[300,200]],"stroke":"#442200","stroke_width":3},
          {"kind":"text","text":"Kosif & paint","x":8,"y":200,"size":18,"fill":"#040404"}]},
        {"name":"moving_circle","shapes":[{"kind":"ellipse","x":0,"y":0,"width":18,"height":18,"fill":"#FF0000","stroke_width":0}],
         "keyframes":[{"time":0,"x":40,"y":160},{"time":1,"x":110,"y":160,"ease":"ease-in-out"}]}
      ]}

class CreativePaintTests(unittest.TestCase):
    def test_invalid_color(self):
        s=demo();s["layers"][0]["shapes"][0]["fill"]="<script>"
        with self.assertRaises(ValueError):engine.validate(s)
    def test_invalid_schema(self):
        s=demo();s["schema"]="bad"
        with self.assertRaises(ValueError):engine.validate(s)
    def test_invalid_keyframe_order(self):
        s=demo();s["layers"][1]["keyframes"][1]["time"]=0
        with self.assertRaises(ValueError):engine.validate(s)
    def test_reject_executable_objects(self):
        s=demo();s["layers"][0]["shapes"].append({"kind":"eval","code":"print('bad')"})
        with self.assertRaises(ValueError):engine.validate(s)
    def test_pixel_positions_and_alpha(self):
        im=engine.paint(demo())
        self.assertEqual(im.size,(300,240))
        self.assertEqual(im.getpixel((10,10))[:3],(0,85,0))
        self.assertEqual(im.getpixel((49,169))[:3],(255,0,0))
    def test_brush_paints(self):
        s=demo();s["layers"][0]["shapes"]=[s["layers"][0]["shapes"][3]]
        self.assertNotEqual(engine.paint(s).getpixel((180,100))[:3],(239,232,215))
    def test_layer_moves_with_timestamps(self):
        s=demo()
        first=engine.paint(s,0);last=engine.paint(s,1)
        self.assertEqual(engine.pose(s["layers"][1],.5)["x"],75)
        self.assertEqual(last.getpixel((119,169))[:3],(255,0,0))
        self.assertNotEqual(first.getpixel((49,169)),last.getpixel((49,169)))
    def test_svg_safe_escaping(self):
        s=demo();s["layers"][0]["shapes"]=[{"kind":"text","text":"<script>alert(1)</script>","x":0,"y":0}]
        result=engine.svg(s)
        self.assertIn("&lt;script&gt;",result)
        self.assertNotIn("<script>",result)
        self.assertIn('data-layer="moving_circle"',result)
    def test_png_svg_outputs_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            png=Path(td)/"drawing.png";svg=Path(td)/"drawing.svg"
            self.assertTrue(engine.render(demo(),png)["verified"])
            with Image.open(png) as im:im.verify()
            self.assertTrue(engine.render(demo(),svg)["verified"])
            with self.assertRaises(ValueError):engine.render(demo(),png)
    def test_gif_frame_count(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"motion.gif"
            self.assertTrue(engine.animate(demo(),out,10,.5)["verified"])
            with Image.open(out) as im:self.assertEqual(im.n_frames,5)
    def test_limit_excessive_frames(self):
        with self.assertRaises(ValueError):engine.animate(demo(),"unused.gif",60,10)
    def test_cli_subprocess(self):
        with tempfile.TemporaryDirectory() as td:
            inp=Path(td)/"input.json";out=Path(td)/"graphic.png";inp.write_text(json.dumps(demo()),encoding="utf-8")
            run=subprocess.run([sys.executable,str(SCRIPT),"render","--scene",str(inp),"--output",str(out)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertTrue(json.loads(run.stdout)["verified"])
    def rotated(self,angle,scale=1,x=0,y=0,size=(640,640),box=(300,300,40,40)):
        return {"schema":"kosif.paint.v1","width":size[0],"height":size[1],"background":"transparent",
                "layers":[{"name":"turn","shapes":[{"kind":"rectangle","x":box[0],"y":box[1],"width":box[2],
                           "height":box[3],"fill":"#FF0000","stroke_width":0}],
                           "keyframes":[{"time":0,"angle":angle,"scale":scale,"x":x,"y":y}]}]}
    def png_centre(self,scene):
        l,t,r,b=engine.paint(scene).getchannel("A").point(lambda a:255 if a>127 else 0).getbbox()
        return ((l+r)/2,(t+b)/2)
    def svg_centre(self,scene,point):
        found=re.search(r'transform="translate\(([-\d.]+) ([-\d.]+)\) rotate\(([-\d.]+) ([-\d.]+) ([-\d.]+)\) scale\(([-\d.]+)\)"',engine.svg(scene))
        tx,ty,angle,cx,cy,k=map(float,found.groups())
        dx,dy=point[0]*k-cx,point[1]*k-cy;r=math.radians(angle)
        return (tx+cx+dx*math.cos(r)-dy*math.sin(r),ty+cy+dx*math.sin(r)+dy*math.cos(r))
    def test_rotation_turns_layer_in_place(self):
        for angle in (8,45,-90):
            with self.subTest(angle=angle):
                cx,cy=self.png_centre(self.rotated(angle))
                self.assertLessEqual(abs(cx-320.5),1.5);self.assertLessEqual(abs(cy-320.5),1.5)
    def test_rotated_layer_lands_in_same_place_in_png_and_svg(self):
        for angle,scale,x,y,size,box in [(90,1,0,0,(200,200),(150,90,20,20)),
                                          (-8,1.3,-30,40,(640,480),(400,100,30,30)),
                                          (30,.6,50,20,(320,240),(200,40,20,30))]:
            with self.subTest(angle=angle,scale=scale):
                scene=self.rotated(angle,scale,x,y,size,box)
                png=self.png_centre(scene);vec=self.svg_centre(scene,(box[0]+box[2]/2,box[1]+box[3]/2))
                self.assertLessEqual(math.dist(png,vec),2,(png,vec))
    def test_cli_accepts_utf8_bom_scene(self):
        with tempfile.TemporaryDirectory() as td:
            inp=Path(td)/"bom.json";out=Path(td)/"bom.png"
            inp.write_text(json.dumps(demo()),encoding="utf-8-sig")
            run=subprocess.run([sys.executable,str(SCRIPT),"render","--scene",str(inp),"--output",str(out)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertTrue(out.exists())
    def test_mp4_render(self):
        if not __import__("shutil").which("ffmpeg"):self.skipTest("FFmpeg unavailable")
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"animated.mp4"
            summary=engine.animate(demo(),out,8,.5)
            self.assertTrue(summary["verified"]);self.assertEqual(summary["frames"],4)
            self.assertGreater(out.stat().st_size,1000)

if __name__=="__main__":unittest.main()
