"""v6.2 video breakdown: beats from hard cuts, dissolves and entrances; palette and background hex; the brief that must
be filled; the Omni Flash block (10 s compression, ≥1080, overrides, no questions, removal guard); shard planning."""
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
FF = shutil.which("ffmpeg")


@unittest.skipUnless(FF, "ffmpeg")
class Breakdown(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="kosif_an_"))
        cls.film = cls.tmp / "ref.mp4"
        # 0–4 s red, hard cut to blue (4–8 s, with a white box entering at 6 s), 1 s dissolve to green (8–12 s); a tone
        g = ("color=c=0xc03020:s=640x360:r=30:d=4[a];color=c=0x2040c0:s=640x360:r=30:d=4[b0];color=c=white:s=160x90:r=30:d=2[box];"
             "[b0][box]overlay=x='if(lt(t,2),-200,240)':y=135[b];color=c=0x20a040:s=640x360:r=30:d=5[c];"
             "[b][c]xfade=transition=fade:duration=1:offset=3[bc];[a][bc]concat=n=2:v=1:a=0[v]")
        subprocess.run([FF, "-y", "-v", "error", "-filter_complex", g, "-f", "lavfi", "-i", "sine=f=440:d=12", "-map", "[v]", "-map", "0:a",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(cls.film)], check=True)
        import analyze
        cls.rep = analyze.analyze(cls.film, cls.tmp / "bd")
        cls.an = json.loads((cls.tmp / "bd" / "analysis.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_specs_and_beats(self):
        a = self.an
        self.assertEqual((a["width"], a["height"], a["aspect"]), (640, 360, "16:9"))
        self.assertAlmostEqual(a["duration"], 12.0, delta=0.15)
        starts = [b["t0"] for b in a["beats"]]
        self.assertTrue(any(abs(s - 4.0) < 0.25 for s in starts), starts)          # the hard cut
        self.assertTrue(any(7.4 <= s <= 8.6 for s in starts), starts)              # the dissolve
        self.assertTrue(any(5.6 <= s <= 6.4 for s in starts), starts)              # the white box entering
        self.assertTrue(all(b["t1"] - b["t0"] <= 3.05 for b in a["beats"]))
        self.assertGreaterEqual(a["scenes"], 3)

    def test_colour(self):
        first, = [b for b in self.an["beats"] if b["t0"] == 0]
        bg = [int(first["background"][i:i + 2], 16) for i in (1, 3, 5)]
        self.assertTrue(all(abs(x - y) <= 8 for x, y in zip(bg, (0xc0, 0x30, 0x20))), first["background"])
        blue = next(b for b in self.an["beats"] if 4.2 < (b["t0"] + b["t1"]) / 2 < 5.8)
        top = [int(blue["palette"][0]["hex"][i:i + 2], 16) for i in (1, 3, 5)]
        self.assertTrue(all(abs(x - y) <= 8 for x, y in zip(top, (0x20, 0x40, 0xc0))), blue["palette"])

    def test_files(self):
        bd = self.tmp / "bd"
        for f in ("overview.jpg", "timeline.jpg", "brief.json"):
            self.assertTrue((bd / f).exists(), f)
        self.assertEqual(len(list((bd / "frames").glob("*.jpg"))), 3 * self.an["beat_count"])
        self.assertIsNotNone(self.an["audio"]); self.assertLess(self.an["audio"]["lufs"], 0)

    def test_omniprompt(self):
        import omniprompt
        brief = json.loads((self.tmp / "bd" / "brief.json").read_text(encoding="utf-8"))
        with self.assertRaises(SystemExit):                                       # an unfilled breakdown is refused
            omniprompt.build(brief)
        for k in omniprompt.TOP:
            brief[k] = f"{k} text with #2040c0."
        for b in brief["beats"]:
            for k in omniprompt.FIELDS:
                b[k] = "a blue card with a white box" if k == "subjects" else f"{k} of beat {b['i']}"
        out = omniprompt.build(brief)
        self.assertIn("640x360" if False else "1920x1080", out)                    # ≥ 1080 on the short side
        self.assertIn("10.0 s", out); self.assertIn("×0.83", out); self.assertNotIn("?", out)
        self.assertTrue(out.splitlines()[0].startswith("STYLE:")); self.assertIn("FINAL FRAME", out)
        ov = {"palette": {"#2040c0": "#0f766e"}, "aspect": "9:16", "duration": 8, "tone": "calm", "add": ["grain"], "remove": ["confetti"]}
        o2 = omniprompt.build(brief, ov=ov)
        self.assertIn("1080x1920", o2); self.assertIn("8.0 s", o2); self.assertNotIn("#2040c0", o2); self.assertIn("#0f766e", o2)
        self.assertIn("no confetti", o2); self.assertIn("ADD: grain", o2)
        with self.assertRaises(SystemExit):                                       # removing what the scenes are built on
            omniprompt.build(brief, ov={"remove": ["box"]})


class Shards(unittest.TestCase):
    def test_plan_covers_every_frame(self):
        import shard
        p = shard.plan(str(SCRIPTS / "projects" / "night_boat"), 7)
        s = p["shards"]
        self.assertEqual(s[0]["i0"], 0); self.assertEqual(s[-1]["i1"], p["frames"])
        self.assertTrue(all(a["i1"] == b["i0"] for a, b in zip(s, s[1:])))


if __name__ == "__main__":
    unittest.main()
