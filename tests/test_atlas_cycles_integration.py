"""REA/Ghidra/Atlas/Cycles additive integration tests; no external software executed."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'.claude'/'skills'/'kosif-superpowers'/'scripts'

def module(name):
    spec=importlib.util.spec_from_file_location(name,SCRIPTS/(name+'.py'))
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

class AtlasCyclesTests(unittest.TestCase):
    def test_atlas_index_shape(self):
        bridge=module('atlas_external_bridge')
        with tempfile.TemporaryDirectory() as temp:
            index=pathlib.Path(temp)/'index.json'
            index.write_text(json.dumps({'skills':[{'id':1,'skill':'cycles render',
               'description':'3D photoreal video','license':'MIT','path':'skills/1',
               'risk_flags':['scripts'],'verdict':'REVIEW_BEFORE_INSTALL'}]}),encoding='utf-8')
            rows=bridge.load(index)
            self.assertEqual(len(rows),1)
            self.assertGreater(bridge.score(rows[0],'render'),0)
            self.assertEqual(rows[0]['risk_flags'],['scripts'])
            self.assertEqual(bridge.inspect_skill(None,rows[0]),'NOT_READ')
    def test_atlas_null_fields_do_not_crash(self):
        bridge=module('atlas_external_bridge')
        row={'id':'N1','skill':'render x','description':None,'plugin':None}
        self.assertGreater(bridge.score(row,'render'),0)
        self.assertEqual(bridge.family({'skill':None,'description':None}),'general')
        with tempfile.TemporaryDirectory() as temp:
            index=pathlib.Path(temp)/'index.json'
            index.write_text(json.dumps([row]),encoding='utf-8')
            result=subprocess.run([sys.executable,str(SCRIPTS/'atlas_external_bridge.py'),'search',
                                   '--index',str(index),'--query','render'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['matches'][0]['description'],'')
    def test_atlas_path_traversal_blocked(self):
        bridge=module('atlas_external_bridge')
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(bridge.inspect_skill(tmp,{'path':'../outside'}),'INVALID_PATH')
    def test_render_cli_doctor(self):
        result=subprocess.run([sys.executable,str(SCRIPTS/'blender_cycles_render.py'),'doctor'],
                              capture_output=True,text=True,check=True)
        data=json.loads(result.stdout)
        self.assertEqual(data['renderer'],'Cycles')
        self.assertIn('blender',data['engines'])
    def test_render_plan_and_bounds(self):
        with tempfile.TemporaryDirectory() as td:
            scene=pathlib.Path(td)/'demo.blend';scene.write_bytes(b'BLENDER_test_dummy')
            outfile=pathlib.Path(td)/'video.mp4'
            base=[sys.executable,str(SCRIPTS/'blender_cycles_render.py'),
                  'plan','--scene',str(scene),'--out',str(outfile),
                  '--frames','150','--fps','30']
            result=subprocess.run(base,capture_output=True,text=True,check=True)
            self.assertEqual(json.loads(result.stdout)['duration_seconds'],5)
            invalid=subprocess.run(base+['--width','641'],capture_output=True,text=True)
            self.assertNotEqual(invalid.returncode,0)
            self.assertFalse(outfile.exists())
    def test_probe_counts_frames_for_mkv_and_mp4(self):
        import shutil
        ffmpeg,ffprobe=shutil.which('ffmpeg'),shutil.which('ffprobe')
        if not (ffmpeg and ffprobe):self.skipTest('ffmpeg/ffprobe not installed')
        render=module('blender_cycles_render')
        with tempfile.TemporaryDirectory() as td:
            for suffix in ('.mkv','.mp4'):
                with self.subTest(suffix=suffix):
                    video=pathlib.Path(td)/('clip'+suffix)
                    subprocess.run([ffmpeg,'-v','error','-f','lavfi','-i','testsrc=size=64x64:rate=24',
                                    '-frames:v','12','-c:v','libx264','-pix_fmt','yuv420p','-an',str(video)],check=True)
                    self.assertEqual(int(render.probe(ffprobe,video,64,64,12)['nb_read_packets']),12)
                    with self.assertRaisesRegex(RuntimeError,'Video QA failure'):
                        render.probe(ffprobe,video,64,64,13)
if __name__=='__main__':unittest.main()
