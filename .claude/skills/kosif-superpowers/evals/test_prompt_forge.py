"""Offline tests for prompt_forge.py (layered prompts, lint, frame-exact shot lists)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "prompt_forge.py"
sys.path.insert(0, str(SK / "scripts"))
import prompt_forge as P  # noqa: E402

SPEC = {"subject": "an old fisherman", "action": "mends a net", "setting": "a wooden pier at dawn",
        "style": "documentary photograph", "camera": "medium shot, 50 mm, eye level",
        "light": "low warm sun from the left", "constraints": ["no text", "weathered hands visible"],
        "aspect": "4:5", "genre": "ambient folk", "mood": "calm", "tempo_bpm": 72,
        "instruments": ["oud", "soft pads"], "voice": "warm baritone", "pace_wpm": 140,
        "text": "The sea gives back what it takes."}


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class PromptForgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, obj):
        p = self.d / name
        p.write_text(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return str(p)

    def test_forge_still_image_exact(self):
        r = P.forge(SPEC, "still-image")["targets"]["still-image"]
        self.assertEqual(r["prompt"], "documentary photograph, an old fisherman mends a net, in a wooden pier at "
                         "dawn, low warm sun from the left, medium shot, 50 mm, eye level, weathered hands visible, "
                         "aspect ratio 4:5. Avoid: text.")
        self.assertEqual(r["warnings"], [])

    def test_forge_all_targets(self):
        t = P.forge(SPEC, "still-image,video,music,voice")["targets"]
        self.assertEqual(set(t), {"still-image", "video", "music", "voice"})
        self.assertIn("Camera: medium shot, 50 mm, eye level.", t["video"]["prompt"])
        self.assertIn("72 BPM", t["music"]["prompt"])
        self.assertIn("instruments: oud, soft pads", t["music"]["prompt"])
        self.assertIn('Line: "The sea gives back what it takes."', t["voice"]["prompt"])
        self.assertIn("pace: 140 words per minute", t["voice"]["prompt"])

    def test_forge_video_defaults_static_and_arabic(self):
        r = P.build({"subject": "قطة", "action": "تقفز", "constraints": ["بدون نص"]}, "video")
        self.assertIn("الكاميرا: كاميرا ثابتة.", r["prompt"])
        self.assertIn("تجنّب: نص.", r["prompt"])
        self.assertTrue(any("static" in w for w in r["warnings"]))

    def test_forge_cli_and_bad_input(self):
        p = self.write("s.json", SPEC)
        out = run("forge", p, "--targets", "video,music")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(set(json.loads(out.stdout)["targets"]), {"video", "music"})
        txt = run("forge", p, "--targets", "voice", "--text")
        self.assertTrue(txt.stdout.startswith("[voice]"))
        bad = run("forge", p, "--targets", "midjourney")
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(len(bad.stderr.strip().splitlines()), 1)
        nosub = run("forge", self.write("n.json", {"action": "x"}), "--targets", "video")
        self.assertEqual(nosub.returncode, 2)
        self.assertEqual(run("forge", str(self.d / "missing.json")).returncode, 2)

    def test_lint_english(self):
        r = P.lint("A photo of a beautiful cat, masterpiece, 8k, day and night", "still-image")
        codes = [f["code"] for f in r["findings"]]
        for c in ("HYPE", "VAGUE", "OPENER", "CONTRADICTION", "MISSING_CAMERA", "LENGTH"):
            self.assertIn(c, codes)
        # 1 error (contradiction) + hype(masterpiece, 8k)=2 + vague 1 + opener 1 + camera warn 1 + length 1 = 6 warns
        self.assertEqual(r["score"], 100 - 20 - 5 * 6)
        self.assertEqual(r["verdict"], "fail")

    def test_lint_negative_only_and_clean(self):
        self.assertIn("NEGATIVE_ONLY", [f["code"] for f in P.lint("no text, no watermark, without people")["findings"]])
        clean = P.lint("Documentary photograph, an old fisherman mends a net on a wooden pier, low warm sun "
                       "from the left, medium shot, 50 mm lens, eye level, aspect ratio 4:5.", "still-image")
        self.assertEqual(clean["verdict"], "pass")
        self.assertEqual(clean["score"], 100)

    def test_lint_arabic(self):
        r = P.lint("صورة جميلة مذهلة لقطة في النهار والليل")
        codes = [f["code"] for f in r["findings"]]
        self.assertTrue(r["arabic"])
        self.assertIn("HYPE", codes)
        self.assertIn("VAGUE", codes)
        self.assertIn("CONTRADICTION", codes)
        neg = P.lint("بدون نص، بلا أشخاص")
        self.assertIn("NEGATIVE_ONLY", [f["code"] for f in neg["findings"]])

    def test_lint_cli(self):
        p = self.write("p.txt", "masterpiece cat")
        out = run("lint", p, "--target", "video")
        self.assertEqual(out.returncode, 0)
        self.assertIn("MISSING_CAMERA", out.stdout)
        self.assertEqual(run("lint", self.write("e.txt", "  ")).returncode, 2)

    def test_shotlist_exact_sum(self):
        data = {"subject": "a red kite", "shots": [{"action": "rises", "duration": 3},
                                                   {"action": "dips", "duration": 4},
                                                   {"action": "lands", "duration": 3}]}
        r = P.shotlist(data, 24, 7)
        # 168 frames * 3/10, 4/10, 3/10 = 50.4, 67.2, 50.4 -> 50, 67, 50 (+1 to the first 0.4 remainder)
        self.assertEqual([s["frames"] for s in r["shots"]], [51, 67, 50])
        self.assertEqual(r["frames_sum"], 168)
        self.assertTrue(r["exact"])
        self.assertEqual([s["start_frame"] for s in r["shots"]], [0, 51, 118])
        self.assertEqual(r["shots"][-1]["end_frame"], 167)
        self.assertEqual(r["shots"][0]["duration_s"], 2.125)
        self.assertIn("a red kite rises", r["shots"][0]["prompt"])
        self.assertNotIn("open the next shot", r["shots"][-1]["prompt"])

    def test_shotlist_cli_and_refusals(self):
        p = self.write("sh.json", {"subject": "a boat", "shots": [{"weight": 1}, {"weight": 1}]})
        out = run("shotlist", p, "--fps", "30", "--total", "5", "--max-shot", "2")
        self.assertEqual(out.returncode, 0, out.stderr)
        d = json.loads(out.stdout)
        self.assertEqual([s["frames"] for s in d["shots"]], [75, 75])
        self.assertTrue(any("max-shot" in w for w in d["shots"][0]["warnings"]))
        self.assertEqual(run("shotlist", p, "--fps", "24", "--total", "7.01").returncode, 2)
        self.assertEqual(run("shotlist", self.write("z.json", []), "--fps", "24", "--total", "2").returncode, 2)
        self.assertEqual(run("shotlist", self.write("w.json", [{"subject": "x", "weight": -1}]),
                             "--fps", "24", "--total", "2").returncode, 2)

    def test_deterministic_and_self_test(self):
        p = self.write("s.json", SPEC)
        a = run("forge", p, "--targets", "still-image,video,music,voice").stdout
        b = run("forge", p, "--targets", "still-image,video,music,voice").stdout
        self.assertEqual(a, b)
        st = run("--self-test")
        self.assertEqual(st.returncode, 0)
        self.assertIn("OK", st.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
