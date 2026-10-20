"""Executable and negative regression tests for KOSIF Code Drawing Master."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"code_drawing_master.py"
spec=importlib.util.spec_from_file_location("code_drawing_master",SCRIPT)
drawing=importlib.util.module_from_spec(spec)
spec.loader.exec_module(drawing)


class CodeDrawingMasterTests(unittest.TestCase):
    def test_all_casts_produce_valid_detailed_actors(self):
        for cast in ("human","cat","human+cat"):
            with self.subTest(cast=cast):
                scene=drawing.make_story(cast=cast)["scenes"][0]
                actors=[x for x in scene["elements"] if x["type"]=="actor"]
                self.assertEqual(len(actors),2 if cast=="human+cat" else 1)
                self.assertTrue(all(len(x["parts"])>=14 for x in actors))
                self.assertTrue(all(x["end"]<scene["end"] for x in actors))
                self.assertTrue(any(part["role"]=="head" for a in actors for part in a["parts"]))

    def test_six_actions_and_three_moods(self):
        for action in ("idle","walk","run","wave","point","sit"):
            for expression in ("happy","sad","determined"):
                with self.subTest(action=action,mood=expression):
                    s=drawing.make_story(cast="human",action=action,expression=expression)
                    actor=next(e for e in s["scenes"][0]["elements"] if e["type"]=="actor")
                    self.assertEqual(actor["action"],action)
                    self.assertTrue(any(x["role"]=="mouth" for x in actor["parts"]))

    def test_parks_and_streets_are_unique(self):
        a=drawing.make_story(location="park")
        b=drawing.make_story(location="street")
        paths=lambda s:[i["d"] for i in s["scenes"][0]["elements"] if i["type"]=="path"]
        self.assertNotEqual(paths(a),paths(b))
        self.assertGreaterEqual(len(paths(a)),5)

    def test_morph_exists_with_checked_corresponding_vertices(self):
        model=drawing.make_story()
        morph=next(x for x in model["scenes"][0]["elements"] if x["type"]=="morph")
        self.assertEqual(len(morph["from"]),len(morph["to"]))
        self.assertNotEqual(morph["from"],morph["to"])
        self.assertTrue(morph["end"]>morph["start"])

    def test_morph_vertex_injection_rejected(self):
        model=drawing.make_story()
        morph=next(x for x in model["scenes"][0]["elements"] if x["type"]=="morph")
        morph["to"][0][1]='eval(alert(1))'
        with self.assertRaises(ValueError):
            drawing.director.validate(model)

    def test_staged_path_drawing_and_post_draw_motion(self):
        scene=drawing.make_story()["scenes"][0]
        for actor in (i for i in scene["elements"] if i["type"]=="actor"):
            self.assertEqual(actor["move"]["start"],actor["end"])
            self.assertEqual(actor["move"]["end"],scene["end"])
            self.assertGreater(len(actor["parts"]),3)

    def test_compile_actual_editable_html_without_runtime(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"film.html"
            result=drawing.director.compile_spec(drawing.make_story(),path)
            self.assertEqual(result["status"],"html_compiled_not_rendered")
            body=path.read_text(encoding="utf-8")
            self.assertIn('"type":"actor"',body)
            self.assertIn("strokeDashoffset",body)
            self.assertIn("window.__kosif",body)

    def test_word_timestamps_from_whisperx_are_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"aligned.json"
            path.write_text(json.dumps({"segments":[{"words":[
                {"word":"أهلاً","start":0.15,"end":0.65},
                {"word":"بكم","start":0.72,"end":1.23}]}]},ensure_ascii=False),encoding="utf8")
            words=drawing.load_words(path,9)
            self.assertEqual(words[0]["start"],0.15)
            self.assertEqual(words[1]["end"],1.23)
            self.assertEqual(drawing.make_story(words=words)["scenes"][0]["words"],words)

    def test_missing_alignment_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"aligned.json"
            path.write_text('{"words":[{"word":"hello"}]}',encoding="utf8")
            with self.assertRaises(ValueError):
                drawing.load_words(path,9)

    def test_overlapping_alignment_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"aligned.json"
            path.write_text('{"words":[{"word":"one","start":1,"end":2},'
                            '{"word":"two","start":1.9,"end":2.5}]}',encoding="utf8")
            with self.assertRaises(ValueError):
                drawing.load_words(path,9)

    def test_malicious_path_in_actor_is_rejected(self):
        spec=drawing.make_story()
        actor=next(x for x in spec["scenes"][0]["elements"] if x["type"]=="actor")
        actor["parts"][0]["d"]='M0 0" onload="alert(1)'
        with self.assertRaises(ValueError):
            drawing.director.validate(spec)

    def test_unsupported_cast_or_action_fails(self):
        for kw in ({"cast":"dragon"},{"action":"attack"},{"location":"moon"},
                   {"expression":"unknown"},{"duration":3}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):
                drawing.make_story(**kw)

    def test_cli_generates_json_and_html_as_new_artifacts(self):
        with tempfile.TemporaryDirectory() as folder:
            spec=Path(folder)/"scene.json"
            html=Path(folder)/"scene.html"
            cmd=[sys.executable,str(SCRIPT),"--cast","human+cat","--action","wave",
                 "--out",str(spec),"--html",str(html)]
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=12)
            self.assertEqual(p.returncode,0,p.stderr)
            result=json.loads(p.stdout)
            self.assertEqual(result["status"],"editable_storyboard_created")
            self.assertTrue(html.exists())
            self.assertTrue(spec.exists())
            self.assertEqual(result["actors"],"human+cat")
            p2=subprocess.run(cmd,capture_output=True,text=True,timeout=12)
            self.assertNotEqual(p2.returncode,0)
            self.assertIn("failed",p2.stderr)

    def test_failed_html_step_leaves_no_storyboard(self):
        with tempfile.TemporaryDirectory() as folder:
            spec=Path(folder)/"partial.json"
            html=Path(folder)/"story.html"
            html.write_text("existing",encoding="utf-8")
            cmd=[sys.executable,str(SCRIPT),"--cast","cat","--out",str(spec),"--html",str(html)]
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=12)
            self.assertEqual(p.returncode,2)
            self.assertIn("failed",p.stderr)
            self.assertFalse(spec.exists())
            self.assertEqual(html.read_text(encoding="utf-8"),"existing")
            html.unlink()
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=12)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertTrue(spec.exists() and html.exists())

    def test_word_file_with_utf8_bom_is_accepted(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"aligned.json"
            path.write_text('{"words":[{"word":"hello","start":0.2,"end":0.6}]}',encoding="utf-8-sig")
            self.assertEqual(drawing.load_words(path,9)[0]["start"],0.2)

    def test_no_external_downloads_or_shell(self):
        s=SCRIPT.read_text(encoding="utf8")
        self.assertNotIn("subprocess.run(",s)
        self.assertNotIn("shell=True",s)
        self.assertNotIn("pip install",s)


if __name__=="__main__":
    unittest.main()
