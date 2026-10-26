"""v6.2 /brag method on the engine: colour extraction, share-copy rules, readability, the poster baked as frame 0,
timeline sound effects from the CC0 kit, and `brag init` on a small site."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import launch  # noqa: E402

FF = shutil.which("ffmpeg")


class Material(unittest.TestCase):
    def test_colours(self):
        self.assertEqual(launch.to_hex("#abc"), "#aabbcc")
        self.assertEqual(launch.to_hex("rgb(255 0 0 / 50%)"), "#ff0000")
        self.assertEqual(launch.to_hex("hsl(120, 100%, 50%)"), "#00ff00")
        self.assertEqual(launch.to_hex("oklch(100% 0 0)"), "#ffffff")
        self.assertEqual(launch.to_hex("oklch(0.5 0 0)"), "#636363")
        self.assertIsNone(launch.to_hex("oklch(nope)"))

    def test_site_material_and_plan(self):
        d = Path(tempfile.mkdtemp(prefix="kosif_brag_"))
        (d / "index.html").write_text("""<html lang="ar"><head><title>قهوة الصباح</title><meta name="description" content="قهوة مختصة تصل قبل أن تستيقظ">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap" rel="stylesheet"></head>
<body><h1>قهوتك جاهزة</h1><h2>اطلب الليلة</h2><a class="btn" href="#">اطلب الآن</a></body></html>""", encoding="utf-8")
        (d / "styles.css").write_text(":root{ --bean: oklch(38% 0.085 46); --cream: #f5efe6; --display: 'Cairo', sans-serif; } h1{ font-family: var(--display); color: var(--bean); }", encoding="utf-8")
        out = d / "brag-output"
        r = launch.init(str(d), "polished", "vertical", 18, out)
        self.assertEqual(r["title"], "قهوة الصباح")
        m = json.loads((out / "material.json").read_text(encoding="utf-8"))
        self.assertEqual(m["palette"]["cream"], "#f5efe6"); self.assertIn("bean", m["palette"])
        self.assertIn("Cairo", m["fonts"]); self.assertIn("اطلب الآن", m["ctas"]); self.assertEqual(m["lang"], "ar")
        plan = (out / "brag-plan.md").read_text(encoding="utf-8")
        self.assertIn("1080×1920", plan); self.assertIn("ما هو، في جملة واحدة؟", plan); self.assertIn("polished", plan)
        shutil.rmtree(d, ignore_errors=True)


class Rules(unittest.TestCase):
    def test_share_copy(self):
        self.assertEqual(launch.check_copy("مركب واحد وقمر واحد. خمس ثوانٍ من الكود."), [])
        self.assertTrue(any("banned" in i for i in launch.check_copy("Excited to share our new app!")))
        self.assertTrue(any("sentences" in i for i in launch.check_copy("أ. ب. ج. د.")))
        self.assertTrue(launch.check_copy(""))

    def test_readable(self):
        d = Path(tempfile.mkdtemp(prefix="kosif_read_"))
        spec = {"clips": [{"color": "#000", "dur": 6}], "overlays": [
            {"type": "text", "text": "سطر قصير", "start": 0.3, "end": 2.0},
            {"type": "text", "text": "هذا سطر طويل جداً لا يمكن قراءته في هذا الوقت القصير أبداً", "start": 2.5, "end": 3.6}]}
        f = d / "edit.json"; f.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        r = launch.readable(f)
        self.assertEqual(r["items"], 2); self.assertEqual([x["what"] for x in r["too_short"]], ["overlay 1"])
        self.assertTrue(r["hook"]["ok"])
        shutil.rmtree(d, ignore_errors=True)

    def test_sfx_kit(self):
        r = launch.sfx_list()
        self.assertGreaterEqual(len(r["sounds"]), 20)
        cat = json.loads((SCRIPTS / "kit" / "sfx" / "catalog.json").read_text(encoding="utf-8"))
        for v in cat["sounds"].values():
            self.assertTrue((SCRIPTS / "kit" / "sfx" / v["file"]).exists(), v["file"])
        self.assertTrue((SCRIPTS / "kit" / "sfx" / "LICENSE-SFX.md").exists())


@unittest.skipUnless(FF, "ffmpeg")
class Media(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="kosif_poster_"))
        cls.film = cls.tmp / "f.mp4"                        # black, then a settled bright card, then black
        subprocess.run([FF, "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=320x180:r=30:d=1", "-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=2",
                        "-f", "lavfi", "-i", "color=c=black:s=320x180:r=30:d=1", "-f", "lavfi", "-i", "sine=f=330:d=4",
                        "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]", "-map", "[v]", "-map", "3:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-shortest", str(cls.film)], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_poster_pick_and_bake(self):
        import poster
        p = poster.pick(self.film)
        self.assertTrue(1.0 <= p["t"] <= 3.0, p)                 # never the black head or tail
        jpg = poster.extract(self.film, p["t"], self.tmp / "p.jpg")
        out = self.tmp / "baked.mp4"
        before = poster.probe(self.film)
        r = poster.bake(self.film, jpg, out)
        self.assertEqual(r["frames"], before["frames"])
        r0 = subprocess.run([FF, "-v", "error", "-i", str(out), "-frames:v", "1", "-vf", "scale=8:8,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        self.assertGreater(sum(r0) / len(r0), 40)                # frame 0 is the poster now, not black
        a = subprocess.run([shutil.which("ffprobe") or "ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_name", "-of", "csv=p=0", str(out)],
                           capture_output=True, text=True).stdout.strip()
        self.assertEqual(a, "aac")

    def test_timeline_sfx(self):
        import timeline
        spec = {"size": "320x180", "fps": 30, "clips": [{"color": "#223344", "dur": 2}],
                "audio": {"sfx": [{"src": "kit:reveal-1", "at": 0.5}, {"src": "kit:bell-1", "at": 1.2, "gain": -6}]}}
        sp = timeline.load(spec, self.tmp)
        self.assertEqual([round(e["gain"]) for e in sp["audio"]["sfx"]], [-10, -6])
        with self.assertRaises(ValueError):
            timeline.load({**spec, "audio": {"sfx": [{"src": "kit:nope"}]}}, self.tmp)
        out = self.tmp / "sfx.mp4"
        rep = timeline.build(spec, out)
        self.assertEqual(rep["audio"]["sfx"], 2)
        self.assertTrue(out.exists())


if __name__ == "__main__":
    unittest.main()
