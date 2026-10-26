"""v6.2 review layer (review.py + the Motion OS page): reel.json from a timeline spec and from an HTML composition,
feedback saved and applied back into the source, version bumps. Runs in a throwaway KOSIF_MOTION_HOME."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FF = shutil.which("ffmpeg")

HTML = """<!doctype html><html><head><meta charset="utf-8"><title>Night boat</title>
<style>:root{ --sea: #0b2540; --moon: #f4e9c8; }</style></head>
<body><div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-duration="5" data-fps="30">
<h1 id="t"></h1></div>
<script type="application/json" id="kosif-props">{"title": "قارب في الليل", "titleBox": [10, 40, 80, 12]}</script>
<script type="application/json" id="kosif-reel">{"scenes": [
 {"id": "S1", "name": "Open", "t": [0, 2.5], "els": [{"id": "title", "label": "Title", "t": [0.4, 2.4], "box": [10, 40, 80, 12], "boxBind": "titleBox",
  "props": {"text": {"type": "text", "label": "Text", "bind": "title"}}}]},
 {"id": "S2", "name": "Moon", "t": [2.5, 5], "els": []}]}</script>
<script>const P = JSON.parse(document.getElementById('kosif-props').textContent);</script>
</body></html>"""


def run(args, home):
    env = {**os.environ, "KOSIF_MOTION_HOME": str(home), "PYTHONUTF8": "1"}
    r = subprocess.run([sys.executable, str(SCRIPTS / "kmotion.py"), "review", *args], capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode:
        raise AssertionError(r.stderr[-1500:])
    return json.loads(r.stdout[r.stdout.find("{"):])


@unittest.skipUnless(FF, "ffmpeg")
class ReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = Path(tempfile.mkdtemp(prefix="kosif_review_"))
        (cls.home / "projects").mkdir()
        cls.media = cls.home / "media"; cls.media.mkdir()
        for name, src in (("a.mp4", "testsrc2"), ("b.mp4", "smptebars")):
            subprocess.run([FF, "-y", "-v", "error", "-f", "lavfi", "-i", f"{src}=s=540x960:r=30:d=2", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.media / name)], check=True)
        cls.spec = cls.media / "edit.json"
        cls.spec.write_text(json.dumps({"size": "540x960", "fps": 30, "clips": [{"src": "a.mp4", "in": 0, "out": 2, "transition": {"type": "fade", "dur": 0.4}},
                                                                             {"src": "b.mp4", "in": 0, "out": 2}],
                                        "overlays": [{"type": "text", "text": "قبل", "start": 0.2, "end": 1.6, "pos": "center", "size": 60},
                                                     {"type": "lower-third", "title": "اسم", "sub": "دور", "start": 2.0, "end": 3.4}]}, ensure_ascii=False), encoding="utf-8")
        cls.film = cls.media / "a.mp4"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.home, ignore_errors=True)

    def test_timeline_reel_and_apply(self):
        r = run(["init", str(self.spec), "--video", str(self.film), "--name", "edit"], self.home)
        self.assertEqual((r["kind"], r["scenes"], r["elements"], r["version"]), ("timeline", 2, 2, 1))
        folder = Path(r["folder"])
        reel = json.loads((folder / "reel.json").read_text(encoding="utf-8"))
        self.assertTrue((folder / reel["src"]).exists())
        el = reel["scenes"][0]["els"][0]
        self.assertEqual(el["props"]["text"]["v"], "قبل")
        self.assertTrue(all(0 <= v <= 100 for v in el["box"]))
        self.assertEqual(reel["scenes"][1]["els"][0]["id"], "ov1")             # the lower third starts in clip 2
        fb = {"version": 1, "over": {"ov0.text": "بعد", "ov0.@time": [0.5, 1.8], "ov0.@box": [10, 20, 80, el["box"][3]], "ov1.accent": "#ff0000",
                                     "ov0.anim": "pop please"}, "notes": [{"id": "n1", "t": 1.0, "x": 50, "y": 50, "text": "أبطأ"}], "status": {"S2": "approved"}}
        f = self.home / "fb.json"; f.write_text(json.dumps(fb, ensure_ascii=False), encoding="utf-8")
        rep = run(["apply", "edit", "--feedback", str(f)], self.home)
        self.assertEqual(sorted(rep["applied"]), sorted(["ov0.text", "ov0.@time", "ov0.@box", "ov1.accent"]))
        self.assertIn("ov0.anim", rep["left_for_claude"]["edits"])               # a motion-type prop with no binding → Claude
        self.assertEqual(rep["approved_do_not_touch"], ["S2"]); self.assertEqual(len(rep["left_for_claude"]["notes"]), 1)
        spec = json.loads(self.spec.read_text(encoding="utf-8"))
        o = spec["overlays"][0]
        self.assertEqual((o["text"], o["start"], o["end"]), ("بعد", 0.5, 1.8))
        self.assertAlmostEqual(o["x"], 0.5, places=3); self.assertAlmostEqual(o["y"], 0.2 / (1 - el["box"][3] / 100), places=3)
        self.assertEqual(spec["overlays"][1]["accent"], "#ff0000")
        r2 = run(["bump", "edit"], self.home)
        self.assertEqual(r2["version"], 2)
        self.assertEqual(json.loads((folder / "reel.json").read_text(encoding="utf-8"))["scenes"][0]["els"][0]["props"]["text"]["v"], "بعد")

    def test_html_reel_apply_and_feedback(self):
        proj = self.home / "projects" / "night_boat"; proj.mkdir()
        (proj / "index.html").write_text(HTML, encoding="utf-8")
        r = run(["init", str(proj), "--video", str(self.film)], self.home)
        self.assertEqual((r["kind"], r["scenes"], r["elements"]), ("html", 2, 1))
        reel = json.loads((proj / "reel.json").read_text(encoding="utf-8"))
        self.assertEqual(reel["scenes"][0]["els"][0]["props"]["text"]["v"], "قارب في الليل")
        self.assertEqual([c["id"] for c in reel["brand"]["colors"]], ["sea", "moon"])
        sys.path.insert(0, str(SCRIPTS))
        old_home = os.environ.get("KOSIF_MOTION_HOME")
        def restore():                                    # the env back, then the modules that read it at import
            if old_home:
                os.environ["KOSIF_MOTION_HOME"] = old_home
            else:
                os.environ.pop("KOSIF_MOTION_HOME", None)
            import importlib, motion, review                 # noqa: E401
            importlib.reload(motion); importlib.reload(review)
        self.addCleanup(restore)
        os.environ["KOSIF_MOTION_HOME"] = str(self.home)
        import importlib
        import motion
        importlib.reload(motion)
        import review
        importlib.reload(review)
        saved = review.save_feedback("night_boat", {"text": "KOSIF review feedback …", "over": {"title.text": "مركب", "title.@box": [5, 30, 90, 14],
                                                                                              "brand.color.moon": "#ffffff"}, "notes": []})
        self.assertTrue((proj / saved["saved"]).exists())
        self.assertEqual(review.latest_feedback("night_boat")["over"]["title.text"], "مركب")
        rep = review.apply("night_boat")
        self.assertEqual(sorted(rep["applied"]), ["brand.color.moon", "title.@box", "title.text"])
        html = (proj / "index.html").read_text(encoding="utf-8")
        self.assertIn("--moon: #ffffff", html); self.assertIn('"title": "مركب"', html); self.assertIn("[\n  5,", html.replace("[ 5", "[\n  5"))
        self.assertTrue((proj / "index.html.bak").exists())
        self.assertIn("night_boat", {x["name"] for x in review.list_reels()})


class AIPromptTests(unittest.TestCase):
    def test_seven_layers_per_platform(self):
        sys.path.insert(0, str(SCRIPTS))
        import aiprompts
        shots = [{"subject": "a wooden felucca", "action": "rides a swell", "environment": "open sea", "time": "night", "shot": "wide", "lens": "50mm f/2",
                  "camera_move": "slow push-in", "atmosphere": "light haze", "lighting": "moon key from behind upper left at 4100K", "locks": {"style": "quiet night, 35mm film"}, "aspect": "16:9"},
                 {"subject": "a fish breaks the surface", "lighting": "moonlight", "negative": ["boats"]}]
        r = aiprompts.build(shots, "t")
        self.assertEqual(len(r["shots"]), 2)
        a, b = r["shots"]
        self.assertEqual(set(a["layers"]), {"location", "subject", "wardrobe", "lighting", "camera", "atmosphere", "technical"})
        self.assertEqual(set(a["prompts"]), set(aiprompts.PLATFORMS))
        self.assertEqual(a["warnings"], [])
        self.assertIn("[quiet night, 35mm film]", b["prompts"]["veo"]["prompt"])          # the style lock carries into later shots
        self.assertIn("16:9", b["layers"]["technical"])
        self.assertTrue(any("physics" in w for w in b["warnings"]))                       # "moonlight" alone: no direction, no Kelvin
        self.assertIn("boats", b["prompts"]["kling"]["negative_prompt"])
        self.assertLessEqual(b["prompts"]["runway"]["chars"], 1000)


if __name__ == "__main__":
    unittest.main()
