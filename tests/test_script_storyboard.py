import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "script_storyboard.py"
spec = importlib.util.spec_from_file_location("script_storyboard", SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# A short original script in the usual Arabic stage layout, with the quirks pdftotext leaves behind:
# bidi marks, a broken lam-alef in the act heading, the act heading repeated above each scene,
# a speech wrapped over two lines, a page number and one name spelled two ways.
ARABIC = """‫الفصل األول‬
‫المشهد الأول‬
سوق شعبي في الصباح، الباعة يرصون الخضار والناس يتزاحمون بين العربات.
نادية: صباح الخير يا عم حسن، هل وصل
الطماطم الجديد؟
حسن (يبتسم): وصل قبل الفجر.
نادية: الحمد لله!
12
الفصل الأول
المشهد الثاني
شرفة بيت قديم عند الغروب.
ناديه: لن أنسى هذا اليوم.
"""

ENGLISH = """ACT ONE
SCENE 1
A crowded station. Two porters push loaded trolleys through the noise.
MAYA: Are we late?
LEO (checking his watch): Not yet.
MAYA: Run!
SCENE 2
INT. TRAIN - NIGHT
LEO: We made it.
"""


class TestParse(unittest.TestCase):
    def setUp(self):
        self.board = m.plan(m.blocks(ARABIC), title="souq")

    def test_structure(self):
        t = self.board["totals"]
        self.assertEqual((t["acts"], t["scenes"]), (1, 2))
        self.assertEqual(self.board["acts"][0]["number"], 1)

    def test_wrapped_speech_is_joined_and_page_number_dropped(self):
        shots = self.board["scenes"][0]["shots"]
        self.assertIn("الطماطم الجديد", shots[1]["text"])
        self.assertFalse(any(sh["text"] == "12" for sh in shots))

    def test_shot_grammar(self):
        shots = self.board["scenes"][0]["shots"]
        self.assertEqual(shots[0]["shot_size"], "wide (establishing)")
        self.assertEqual(shots[2]["character"], "حسن")
        self.assertEqual(shots[2]["direction"], "يبتسم")
        self.assertEqual(shots[2]["shot_size"], "close-up")
        self.assertEqual(shots[3]["shot_size"], "close-up")  # exclamation
        for sh in shots:
            self.assertGreaterEqual(sh["duration"], m.MIN_SHOT)
            self.assertLessEqual(sh["duration"], m.MAX_SHOT)

    def test_alias_warning(self):
        self.assertTrue(any("نادية" in w and "ناديه" in w for w in self.board["warnings"]))

    def test_english_and_screenplay_headings(self):
        b = m.plan(m.blocks(ENGLISH), title="station")
        self.assertEqual(b["totals"]["scenes"], 2)
        self.assertEqual([c["name"] for c in b["characters"]], ["LEO", "MAYA"])
        self.assertEqual(b["scenes"][0]["shots"][2]["direction"], "checking his watch")

    def test_episodes_never_exceed_limit(self):
        b = m.plan(m.blocks(ARABIC * 6), title="long")
        rep = m.pacing(b, 10)
        self.assertTrue(rep["episodes"])
        for e in rep["episodes"]:
            self.assertLessEqual(e["seconds"], 10 + 1e-6)
        covered = sum(e["shots"] for e in rep["episodes"])
        self.assertEqual(covered, b["totals"]["shots"])

    def test_frame_plan_has_no_drift(self):
        self.assertEqual(sum(m.frame_plan([0.33] * 100, 30)), 990)
        self.assertEqual(m.frame_plan([1 / 3] * 3, 30), [10, 10, 10])

    def test_cli_parse_and_bad_color(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "s.txt"
            src.write_text(ARABIC, encoding="utf-8")
            out = Path(td) / "b.json"
            self.assertEqual(m.main(["parse", str(src), "--out", str(out), "--episode-seconds", "8"]), 0)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["schema"], "kosif.storyboard.v1")
            self.assertEqual(len(data["source"]["sha256"]), 64)
            self.assertIn("episodes", data["pacing"])
        with self.assertRaises(ValueError):
            m.valid_color("red; rm -rf /")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg not installed")
class TestRender(unittest.TestCase):
    def test_animatic_follows_master_audio_frame_exact(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            board = td / "b.json"
            self.assertEqual(m.main(["blank", "--out", str(board), "--duration", "9", "--shots", "3"]), 0)
            audio = td / "voice.m4a"
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "sine=d=2",
                            "-c:a", "aac", str(audio)], check=True)
            out = td / "film.mp4"
            self.assertEqual(m.main(["render", "--storyboard", str(board), "--out", str(out), "--audio", str(audio),
                                     "--width", "270", "--height", "480"]), 0)
            probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-of", "json",
                                               str(out)], capture_output=True, text=True, check=True).stdout)
            v = [s for s in probe["streams"] if s["codec_type"] == "video"][0]
            a = [s for s in probe["streams"] if s["codec_type"] == "audio"][0]
            self.assertEqual(int(v["nb_read_frames"]), 60)
            self.assertEqual(v["r_frame_rate"], "30/1")
            self.assertEqual(a["codec_name"], "aac")
            rep = json.loads(out.with_suffix(".report.json").read_text(encoding="utf-8"))
            self.assertEqual(rep["crf"], 17)
            self.assertEqual(sum(rep["shot_frames"].values()), 60)

    def test_crf_never_worse_than_standard(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            board = td / "b.json"
            m.main(["blank", "--out", str(board), "--duration", "0.2", "--shots", "1"])
            out = td / "f.mp4"
            self.assertEqual(m.main(["render", "--storyboard", str(board), "--out", str(out), "--crf", "28",
                                     "--width", "128", "--height", "128"]), 0)
            self.assertEqual(json.loads(out.with_suffix(".report.json").read_text())["crf"], 17)


if __name__ == "__main__":
    unittest.main()
