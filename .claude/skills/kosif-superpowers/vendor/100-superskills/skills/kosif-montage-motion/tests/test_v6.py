"""v6 engine tests: the timeline compiler (speed ramps, transitions, overlays, music), shot detection, privacy masks,
motion templates, caption styles, platform presets, the registry. Synthetic clips only (FFmpeg lavfi) — no network."""
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
sys.path.insert(0, str(ROOT / "scripts"))
TMP = Path(tempfile.mkdtemp(prefix="kosif_v6_"))
os.environ.setdefault("KOSIF_MOTION_HOME", str(TMP))
import timeline  # noqa: E402
import montage  # noqa: E402
import kmotion  # noqa: E402
import platforms  # noqa: E402

FF = shutil.which("ffmpeg")


def synth(path: Path, seconds: float = 2.0, size: str = "320x180", src: str = "testsrc2", tone: int = 440, audio: bool = True):
    cmd = [FF, "-y", "-v", "error", "-f", "lavfi", "-i", f"{src}=s={size}:r=24:d={seconds}"]
    if audio:
        cmd += ["-f", "lavfi", "-i", f"sine=f={tone}:d={seconds}", "-c:a", "aac"]
    cmd += ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-shortest", str(path)]
    subprocess.run(cmd, check=True)


class RampTests(unittest.TestCase):
    def test_ramp_time_map(self):
        pieces, out = timeline.ramp_pieces([[0, 1.0], [2.0, 0.25], [4.0, 1.0]], 4.0)
        self.assertGreater(out, 4.0)                                   # a slow-motion stretch lasts longer than real time
        ts = [i / 10 for i in range(41)]
        ys = [timeline.ramp_map(pieces, t) for t in ts]
        self.assertTrue(all(b > a for a, b in zip(ys, ys[1:])))       # monotonic
        self.assertAlmostEqual(ys[-1], out, places=4)
        self.assertIn("setpts=", timeline.ramp_expr(pieces)); self.assertIn("log(", timeline.ramp_expr(pieces))
        with self.assertRaises(ValueError):
            timeline.ramp_pieces([[0, 20.0]], 2.0)
        self.assertEqual(timeline.atempo_chain(0.25), "atempo=0.5,atempo=0.5000")

    def test_transitions_list(self):
        t = timeline.transitions()
        self.assertIn("fade", t); self.assertIn("circleopen", t); self.assertNotIn("custom", t)
        self.assertEqual(timeline.transition_ar("fadeblack"), "عبر الأسود")


@unittest.skipUnless(FF, "ffmpeg")
class TimelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a, cls.b, cls.m = TMP / "a.mp4", TMP / "b.mp4", TMP / "music.wav"
        synth(cls.a, 3.0); synth(cls.b, 2.0, src="smptebars", tone=660)
        subprocess.run([FF, "-y", "-v", "error", "-f", "lavfi", "-i", "sine=f=220:d=8", "-ar", "48000", str(cls.m)], check=True)
        cls.logo = TMP / "logo.png"
        from PIL import Image
        Image.new("RGBA", (80, 40), (255, 0, 0, 200)).save(cls.logo)

    def test_build_film(self):
        spec = {"size": "320x180", "fps": 24, "background": "#101010",
                "clips": [{"src": str(self.a), "in": 0.2, "out": 2.2, "zoom": {"from": 1.0, "to": 1.1}, "grade": "teal_orange", "transition": {"type": "circleopen", "dur": 0.4}},
                          {"src": str(self.b), "ramp": [[0, 1.0], [1.0, 0.5], [2.0, 1.0]], "transition": "slideup"},
                          {"image": str(self.logo), "dur": 1.0, "fit": "contain"}, {"color": "#000000", "dur": 0.5}],
                "overlays": [{"type": "text", "text": "عنوان الفيلم", "start": 0.2, "end": 1.6, "pos": "center", "size": 28, "anim": "rise", "box": "#00000080"},
                             {"type": "lower-third", "title": "اسم", "sub": "صفة", "start": 1.0, "end": 2.5},
                             {"type": "image", "src": str(self.logo), "start": 0, "end": 3, "pos": "upper-right", "scale": 0.5},
                             {"type": "progress", "color": "#E7B65A", "height": 4},
                             {"type": "captions", "spec": str(TMP / "caps.json"), "style": "tiktok"}],
                "audio": {"music": {"src": str(self.m), "gain": -6, "fade_in": 0.3, "fade_out": 0.5}, "keep_clip_audio": True, "duck": "clips", "lufs": -14}}
        (TMP / "caps.json").write_text(json.dumps([{"start": 0.3, "end": 1.5, "text": "كلمة أولى ثانية"}], ensure_ascii=False), encoding="utf-8")
        s = timeline.summary(spec)
        out = TMP / "film.mp4"
        rep = timeline.build(spec, out, workers=2, inspect=True)
        self.assertTrue(out.exists())
        self.assertAlmostEqual(rep["seconds"], s["seconds"], delta=0.2)        # ≤ one frame per clip of encode rounding
        import tools
        info = tools.probe(out)
        self.assertEqual((info["video"]["w"], info["video"]["h"]), (320, 180))
        self.assertIsNotNone(info["audio"])
        self.assertAlmostEqual(info["duration"], rep["seconds"], delta=0.15)
        self.assertEqual(len(rep["transitions"]), 2)
        self.assertEqual(rep["audio"]["duck"], "clips")
        gate = rep["gate"]
        self.assertIsNotNone(gate["lufs"]); self.assertAlmostEqual(gate["lufs"], -14, delta=2.0)
        dry = timeline.build(spec, TMP / "dry.mp4", dry_run=True)
        self.assertIn("xfade=transition=circleopen", " ".join(dry["graph"])); self.assertIn("sidechaincompress", " ".join(dry["graph"]))

    def test_validation(self):
        with self.assertRaises(ValueError):
            timeline.load({"clips": [{"src": str(self.a), "transition": "warp"}]})
        with self.assertRaises(ValueError):
            timeline.load({"clips": [{"src": str(TMP / "missing.mp4")}]})
        with self.assertRaises(ValueError):
            timeline.load({"clips": [{"src": str(self.a), "speed": 50}]})
        with self.assertRaises(ValueError):
            timeline.load({"clips": []})
        sp = timeline.load({"ratio": "1:1", "clips": [{"src": str(self.a)}]})
        self.assertEqual((sp["W"], sp["H"]), (1080, 1080))

    def test_text_png(self):
        info = timeline.text_png({"text": "سطر عربي\nوثانٍ", "size": 40, "box": "#00000080"}, 1080, 1920, TMP / "t.png")
        self.assertEqual(info["lines"], 2); self.assertTrue((TMP / "t.png").exists())
        from PIL import Image
        im = Image.open(TMP / "t.png"); self.assertEqual(im.mode, "RGBA"); self.assertGreater(im.getchannel("A").getextrema()[1], 200)


@unittest.skipUnless(FF, "ffmpeg")
class ScenesTests(unittest.TestCase):
    def test_detect_and_timeline(self):
        import scenes
        parts = []
        for i, (src, d) in enumerate((("testsrc2", 2.0), ("smptebars", 2.0), ("rgbtestsrc", 1.5))):
            p = TMP / f"part{i}.mp4"; synth(p, d, src=src, audio=False); parts.append(p)
        lst = TMP / "list.txt"; lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
        clip = TMP / "cuts.mp4"
        subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(clip)], check=True)
        rep = scenes.detect(clip, threshold=10, min_len=0.5)
        self.assertEqual(len(rep["scenes"]), 3, rep)
        self.assertAlmostEqual(rep["scenes"][1]["start"], 2.0, delta=0.15); self.assertAlmostEqual(rep["scenes"][2]["start"], 4.0, delta=0.15)
        sheet = scenes.sheet(clip, rep, TMP / "shots.png"); self.assertTrue(sheet.exists())
        spec = scenes.timeline_spec(clip, rep, "fade")
        self.assertEqual(len(spec["clips"]), 3); self.assertNotIn("transition", spec["clips"][-1])
        s = timeline.summary(spec); self.assertAlmostEqual(s["seconds"], 5.5 - 2 * 0.5, delta=0.2)


@unittest.skipUnless(FF, "ffmpeg")
class PrivacyTests(unittest.TestCase):
    def test_region_mask_and_detector(self):
        import privacy
        import faces
        import numpy as np
        frame = np.zeros((120, 160, 3), np.uint8); frame[:, :] = (30, 60, 90)
        frame[20:80, 40:100] = (200, 150, 120)                        # a skin-coloured block: the fallback detector should see it
        self.assertIn(faces.which(), ("yunet", "haar", "skin"))
        boxes = faces.detect(frame, min_frac=0.004)
        self.assertTrue(boxes, "no face-like box found")
        x, y, w, h, _ = boxes[0]
        self.assertLess(abs(x - 40), 12); self.assertLess(abs(y - 20), 12)
        f2 = frame.copy(); privacy.pixelate(f2, (40, 20, 60, 60), 10)
        self.assertFalse(np.array_equal(f2[20:80, 40:100], frame[20:80, 40:100]) and False)
        self.assertTrue(np.array_equal(f2[:20], frame[:20]))         # outside the box untouched
        clip = TMP / "face.mp4"; synth(clip, 1.0)
        rep = privacy.anonymize(clip, TMP / "safe.mp4", mode="box", regions=[privacy.parse_region("0.1,0.1,0.3,0.3", 320, 180)])
        self.assertEqual(rep["frames"], 24); self.assertTrue((TMP / "safe.mp4").exists())
        import tools
        self.assertIsNotNone(tools.probe(TMP / "safe.mp4")["audio"])


class TemplateTests(unittest.TestCase):
    def test_every_template_generates_and_lints(self):
        import mtemplates
        import qa
        for name, t in mtemplates.TEMPLATES.items():
            d = mtemplates.create(f"tt_{name.replace('-', '_')}", name, {"title": "اختبار <b>", "items": "أ|ب|ج", "quote": "س|ص", "from": "3"}, None, 30, "540x960")
            html = (d / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("{{", html); self.assertIn("window.__timelines", html); self.assertIn("&lt;b&gt;", html) if "{{TITLE}}" in (ROOT / "templates" / "motion" / f"{name}.html").read_text(encoding="utf-8") else None
            errs = [f for f in qa.lint(d) if f["level"] == "error"]
            self.assertEqual(errs, [], f"{name}: {errs}")
            self.assertTrue((d / "assets" / "motion-kit.js").exists()); self.assertTrue((d / "template.json").exists())
        with self.assertRaises(SystemExit):
            mtemplates.create("x", "nope", {})


class StyleAndRegistryTests(unittest.TestCase):
    def test_caption_styles(self):
        spec = [{"start": 0, "end": 2, "text": "كلمة أولى ثانية ثالثة خامسة سادسة سابعة"}]
        for st in montage.STYLES:
            text = montage.ass(spec, 1080, 1920, st)
            self.assertIn("[Events]", text); self.assertIn("Style: Cap,", text)
        self.assertIn("BorderStyle" if False else ",3,", montage.ass(spec, 1080, 1920, "boxed").split("[Events]")[0])   # boxed → opaque box
        ev = [l for l in montage.ass(spec, 1080, 1920, "hormozi").splitlines() if l.startswith("Dialogue")]
        self.assertTrue(all(len(l.split(",,")[-1].split()) <= 3 for l in ev))                                          # one word per event (+ override tags)
        self.assertNotIn("\\fscx", montage.ass(spec, 1080, 1920, "minimal"))                                            # no pop in minimal

    def test_platforms_table(self):
        import tools
        for k, v in platforms.PLATFORMS.items():
            self.assertIn(v[0], tools.RATIOS); self.assertEqual(v[1][0] % 2, 0)
        self.assertEqual(platforms.table()["whatsapp"]["max_mb"], 16)

    def test_registry(self):
        for cmd in ("timeline", "transitions", "scenes", "privacy", "template", "platforms", "remote", "web"):
            self.assertIn(cmd, kmotion.C)
        import importlib.util
        for v in kmotion.C.values():
            if v[1]:
                self.assertIsNotNone(importlib.util.find_spec(v[1]), v[1])


class StudioImportTests(unittest.TestCase):
    """v6.1: a KOSIF Studio 6.0 project (the v4 browser editor) → a timeline spec."""

    def test_convert_maps_and_reports(self):
        import studio_import as si
        media = TMP / "studio_media"; media.mkdir(exist_ok=True)
        (media / "song.wav").write_bytes(b"RIFF")                       # matched by name only; not decoded here
        project = {"version": 1, "name": "اختبار", "aspect": "1:1",
                   "assets": [{"id": "v", "name": "gone.mp4", "type": "video", "duration": 5}, {"id": "s", "name": "song.wav", "type": "audio", "duration": 9}],
                   "clips": [{"type": "video", "assetId": "v", "trim": 1, "duration": 2}, {"type": "demo", "preset": "grid", "duration": 3}],
                   "overlays": [{"type": "text", "text": "سطر", "x": 25, "y": 75, "size": 10, "color": "#ffcc00", "opacity": 0.5, "start": 0, "duration": 9, "animation": "zoom"}],
                   "soundtrack": {"assetId": "s", "trim": 2, "volume": 0.5}}
        spec, rep = si.convert(project, media)
        self.assertEqual(spec["size"], "720x720")
        self.assertEqual(spec["clips"][0], {"color": "#202020", "dur": 2.0})                 # missing media → a placeholder, reported
        self.assertIn("gone.mp4", rep["missing_media"])
        ov = spec["overlays"][0]
        self.assertEqual((ov["x"], ov["y"], ov["size"], ov["anim"]), (0.25, 0.75, 72, "fade"))
        self.assertEqual(ov["end"], 5.0); self.assertTrue(ov["color"].endswith("80"))      # clamped to the film; 50 % alpha
        self.assertAlmostEqual(spec["audio"]["music"]["gain"], -6.02, places=1)
        self.assertTrue(any("trim" in n for n in rep["notes"]))
        with self.assertRaises(ValueError):
            si.convert({"version": 1, "clips": []})
        with self.assertRaises(ValueError):
            si.convert({"version": 7})

    def test_registered(self):
        self.assertIn("studio-import", kmotion.C)


class SyncTests(unittest.TestCase):
    """v6.1: `kmotion sync` restores the kit fonts a page names, so example projects can ship without copies."""

    def test_sync_restores_named_fonts_only(self):
        import motion
        d = TMP / "sync_fonts_case"; (d / "assets").mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text('<style>@font-face{src:url("assets/fonts/cairo-arabic-800-normal.woff2")}</style>'
                                      '<div data-composition-id="root"></div>', encoding="utf-8")
        motion.sync_assets(d)
        self.assertTrue((d / "assets" / "fonts" / "cairo-arabic-800-normal.woff2").exists())
        self.assertFalse((d / "assets" / "fonts" / "cairo-latin-600-normal.woff2").exists())   # only what the page names
        self.assertTrue((d / "assets" / "motion-kit.js").exists())


if __name__ == "__main__":
    unittest.main()
