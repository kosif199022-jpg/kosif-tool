"""Station 7 (يتفرج وينقد) of Dragon Montage: dm_review.py on a synthetic render with known faults."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-dragon-montage/scripts"
sys.path.insert(0, str(SCRIPTS))
import dm_common as C  # noqa: E402

REVIEW = SCRIPTS / "dm_review.py"
HAVE_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
W, H = 360, 640


def build_final(path: Path) -> None:
    """9.5s 9:16 render: 0-3 hook (tone), 3-5 moving but SILENT, 5-6.5 BLACK (tone), 6.5-9.5 moving (tone)."""
    size = f"{W}x{H}"
    inputs = [
        "-f", "lavfi", "-i", f"testsrc2=size={size}:rate=30:duration=3",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
        "-f", "lavfi", "-i", f"testsrc2=size={size}:rate=30:duration=2",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:d=2",
        "-f", "lavfi", "-i", f"color=black:size={size}:rate=30:duration=1.5",
        "-f", "lavfi", "-i", "sine=frequency=550:duration=1.5",
        "-f", "lavfi", "-i", f"testsrc2=size={size}:rate=30:duration=3",
        "-f", "lavfi", "-i", "sine=frequency=660:duration=3",
    ]
    fc = ("[1:a]aformat=sample_rates=44100:channel_layouts=mono,volume=0.3[a0];"
          "[3:a]aformat=sample_rates=44100:channel_layouts=mono[a1];"
          "[5:a]aformat=sample_rates=44100:channel_layouts=mono,volume=0.3[a2];"
          "[7:a]aformat=sample_rates=44100:channel_layouts=mono,volume=0.3[a3];"
          "[0:v][a0][2:v][a1][4:v][a2][6:v][a3]concat=n=4:v=1:a=1[v0][a];[v0]format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-ar", "44100", str(path)],
                   check=True, timeout=120)


def shot(cid, i, a, b, q=0.7):
    return {"id": f"{cid}-s{i:03d}", "start": a, "end": b, "quality": {"score": q}, "faces": 1, "motion_energy": 0.4}


def make_job(root: Path) -> Path:
    job = root / "job"
    (job / "render").mkdir(parents=True)
    src = root / "src"
    clips = []
    for n, tone in ((1, 440), (2, 550), (3, 660)):
        p = C.make_test_clip(src / f"c0{n}.mp4", 6.0, tone=tone, size="320x180")
        clips.append(p)
    build_final(job / "render" / "final.mp4")
    analysis = C.new("analysis", clips=[
        {"id": "c01", "path": str(clips[0]), "duration": 6.0, "width": 320, "height": 180, "fps": 30, "has_audio": True,
         "shots": [shot("c01", 1, 0, 3, 0.8), shot("c01", 2, 3, 6, 0.6)],
         "words": [{"w": "اهلا", "start": 0.1, "end": 0.4, "conf": 0.9}, {"w": "بيكم", "start": 0.5, "end": 0.9, "conf": 0.9},
                   {"w": "النهارده", "start": 1.2, "end": 1.8, "conf": 0.9}],
         "silences": [], "energy": []},
        {"id": "c02", "path": str(clips[1]), "duration": 6.0, "width": 320, "height": 180, "fps": 30, "has_audio": True,
         "shots": [shot("c02", 1, 0, 3, 0.5), shot("c02", 2, 3, 6, 0.9)],
         # a second talking camera: silence under it is dead air (silence under wordless b-roll is not)
         "words": [{"w": "وده", "start": 0.6, "end": 0.9, "conf": 0.9}, {"w": "المهم", "start": 1.0, "end": 1.4, "conf": 0.9}],
         "silences": [], "energy": []},
        {"id": "c03", "path": str(clips[2]), "duration": 6.0, "width": 320, "height": 180, "fps": 30, "has_audio": True,
         "shots": [shot("c03", 1, 0, 3, 0.7), shot("c03", 2, 3, 6, 0.7)], "words": [], "silences": [], "energy": []},
    ], music={"path": None, "bpm": None, "beats": [], "downbeats": []}, tools_used=["test"], missing=[])
    edl = C.new("edl", width=W, height=H, fps=30, events=[
        {"id": "e001", "clip": "c01", "src_in": 0.0, "src_out": 3.0, "rec_in": 0.0, "shot": "c01-s001",
         "reason": "hook: strongest line, face visible"},
        {"id": "e002", "clip": "c02", "src_in": 0.5, "src_out": 2.5, "rec_in": 3.0, "shot": "c02-s001",
         "reason": "setup: wide context"},
        {"id": "e003", "clip": "c01", "src_in": 3.5, "src_out": 5.0, "rec_in": 5.0, "shot": "c01-s002",
         "reason": "turn: reaction"},
        {"id": "e004", "clip": "c03", "src_in": 0.0, "src_out": 3.0, "rec_in": 6.5, "shot": "c03-s001",
         "reason": "payoff"},
    ], audio={"music": {"path": None}, "voice_from": "events", "target_lufs": -14},
        captions={"enabled": True, "style": "karaoke", "words_from": "analysis"}, grade={"id": "cinematic"}, duration=9.5)
    brief = C.new("brief", task="مونتاج ريل", one_truth="test", platform="reel", aspect="9:16", target_seconds=10,
                  feeling="warm", energy=0.5, content_type="talking-head")
    concepts = C.new("concepts", concepts=[{"id": "A", "title": "t", "risks": ["the hook might be weak"]}],
                     decision={"chosen": "A"},
                     premortem=["الفيديو يبقى ممل في النص (dead air)", "the colour feels off", "too long for a reel"])
    (job / "render" / "captions.srt").write_text(
        "1\n00:00:00,050 --> 00:00:01,000\nاهلا بيكم\n\n2\n00:00:01,100 --> 00:00:01,900\nالنهارده\n\n3\n00:00:03,050 --> 00:00:03,950\nوده المهم\n", encoding="utf-8")
    render = C.new("render", final="render/final.mp4", captions="render/captions.srt", verify={"pass": True})
    for kind, data in (("analysis", analysis), ("edl", edl), ("brief", brief), ("concepts", concepts), ("render", render)):
        C.write(job, kind, data)
    return job


def run_review(*args):
    return subprocess.run([sys.executable, str(REVIEW), "review", *map(str, args)], capture_output=True, text=True,
                          timeout=300)


@unittest.skipUnless(HAVE_FF, "ffmpeg/ffprobe needed")
class DragonMontageReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.job = make_job(Path(cls.tmp.name))
        cls.res = run_review("--job", cls.job, "--round", 1)
        assert cls.res.returncode == 0, cls.res.stderr
        cls.review = json.loads((cls.job / "review.json").read_text(encoding="utf-8"))
        cls.checks = {c["id"]: c for c in cls.review["checks"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_schema_validates(self):
        C.validate("review", self.review)
        self.assertEqual(self.review["round"], 1)
        self.assertIn(self.review["verdict"], ("ship", "fix"))
        self.assertTrue(0.0 <= self.review["score"] <= 1.0)
        for c in self.review["checks"]:
            self.assertIn("pass", c)
            self.assertTrue(c["evidence"])

    def test_all_checks_present(self):
        for cid in ("technical", "hook-in-3s", "dead-air", "cuts-on-beat", "shot-length", "caption-coverage",
                    "repetition", "duration", "safe-area", "black-frames", "audio-clipping"):
            self.assertIn(cid, self.checks)

    def test_dead_air_fails_at_the_silent_gap(self):
        c = self.checks["dead-air"]
        self.assertFalse(c["pass"])
        silent = [a for a in c["at"] if abs(a[0] - 3.0) < 0.2 and abs(a[1] - 5.0) < 0.2]
        self.assertTrue(silent, c)

    def test_black_frames_fail_at_the_black_segment(self):
        c = self.checks["black-frames"]
        self.assertFalse(c["pass"])
        self.assertEqual(len(c["at"]), 1, c)
        a, b = c["at"][0]
        self.assertAlmostEqual(a, 5.0, delta=0.15)
        self.assertAlmostEqual(b, 6.5, delta=0.15)

    def test_hook_and_clean_checks_pass(self):
        self.assertTrue(self.checks["hook-in-3s"]["pass"], self.checks["hook-in-3s"])
        self.assertTrue(self.checks["repetition"]["pass"])
        self.assertTrue(self.checks["duration"]["pass"])
        self.assertTrue(self.checks["caption-coverage"]["pass"], self.checks["caption-coverage"])

    def test_fixes_reference_real_events(self):
        ids = {"e001", "e002", "e003", "e004"}
        self.assertTrue(self.review["fixes"])
        for f in self.review["fixes"]:
            self.assertIn(f["action"], ("trim", "drop", "swap", "retime", "regrade", "extend", "add"))
            self.assertTrue(f["event"] in ids or f["event"] == "*", f)
            self.assertTrue(f["detail"])
        by = {(f["event"], f["check"]): f for f in self.review["fixes"]}
        self.assertIn(("e002", "dead-air"), by)
        self.assertEqual(by[("e002", "dead-air")]["action"], "drop")
        self.assertIn(("e003", "black-frames"), by)
        self.assertEqual(self.review["verdict"], "fix")

    def test_frames_written(self):
        frames = self.review["frames"]
        self.assertGreaterEqual(len(frames), 4 + 3)
        for f in frames:
            self.assertRegex(f, r"^review/r1_f\d\d\.jpg$")
            self.assertGreater((self.job / f).stat().st_size, 500)
        vp = (self.job / "review" / "VISION_PROMPT.md").read_text(encoding="utf-8")
        self.assertIn("الهوك", vp)
        self.assertIn("--add-note", vp)
        self.assertIn(frames[0], vp)

    def test_premortem_critique(self):
        crit = self.review["critique"]
        self.assertEqual(len(crit), 4)
        dead = next(c for c in crit if "ممل" in c["risk"])
        self.assertEqual(dead["status"], "happened")
        colour = next(c for c in crit if "colour" in c["risk"])
        self.assertEqual(colour["status"], "needs-eyes")

    def test_receipts_logged(self):
        tools = {r["tool"] for r in C.receipts(self.job) if r["station"] == "review"}
        self.assertIn("ffmpeg.blackdetect", tools)
        self.assertIn("video_eyes.motion", tools)
        self.assertIn("verify_video", tools)

    def test_add_note_and_fix(self):
        job = Path(self.tmp.name) / "job_note"
        shutil.copytree(self.job, job)
        res = run_review("--job", job, "--add-note", "الهوك ضعيف شوية", "--fix", "e004:regrade:warmer skin")
        self.assertEqual(res.returncode, 0, res.stderr)
        rv = C.read(job, "review")
        self.assertEqual(rv["notes"][-1]["text"], "الهوك ضعيف شوية")
        self.assertEqual(rv["fixes"][-1], {"event": "e004", "action": "regrade", "detail": "warmer skin",
                                           "check": "vision", "by": "claude"})
        self.assertEqual(rv["verdict"], "fix")
        bad = run_review("--job", job, "--fix", "e999:drop:x")
        self.assertNotEqual(bad.returncode, 0)
        bad = run_review("--job", job, "--fix", "e001:explode:x")
        self.assertNotEqual(bad.returncode, 0)


if __name__ == "__main__":
    unittest.main()


class SafeAreaMarginTests(unittest.TestCase):
    """The review reads the margin actually burned into the .ass, and the threshold from caption_styles.json."""

    def _ass(self, root: Path, margin_v: int, align: int = 2, extra: str = "") -> dict:
        (root / "render").mkdir(parents=True, exist_ok=True)
        (root / "render" / "captions.ass").write_text(
            "[Script Info]\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
            "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
            "MarginR, MarginV, Encoding\n"
            f"Style: Cap,Cairo,74,&H00FFFFFF,&H0059DEFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,{align},76,76,{margin_v},-1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            f"Dialogue: 0,0:00:00.00,0:00:01.00,Cap,,0,0,0,,{extra}اهلا\n", encoding="utf-8")
        return {"captions_ass": "render/captions.ass"}

    def test_margin_scaled_and_overrides(self):
        import dm_review as R
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            m, a = R.ass_margin(root, self._ass(root, 300), 1920)
            self.assertAlmostEqual(m / 1920, 0.15625, places=4)
            m, _ = R.ass_margin(root, self._ass(root, 423), 960)          # PlayRes 1920 scaled to a 960 render
            self.assertAlmostEqual(m / 960, 423 / 1920, places=4)
            m, _ = R.ass_margin(root, self._ass(root, 423, extra="{\\pos(540,1800)}"), 1920)
            self.assertEqual(m, 120)                                     # \pos pulls the line down
            m, a = R.ass_margin(root, self._ass(root, 0, align=5), 1920)
            self.assertIsNone(m)
            self.assertEqual(a, "5")

    def test_threshold_from_caption_styles(self):
        import dm_review as R
        styles = json.loads((SCRIPTS.parent / "data" / "caption_styles.json").read_text(encoding="utf-8"))
        want = ((styles.get("safe_area") or {}).get("9:16") or {}).get("bottom", 0.20)
        self.assertEqual(R.safe_area("9:16")["bottom"], float(want))
        self.assertGreaterEqual(R.safe_area("9:16")["bottom"], 0.2)
