"""Tests for scripts/cinema_lab.py: pure planning logic always, real FFmpeg runs when available."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cinema_lab as cl  # noqa: E402

try:
    import numpy as np  # noqa: F401
    HAVE_NP = True
except ImportError:
    HAVE_NP = False
HAVE_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
HAVE_FILTERS = HAVE_FF and all(cl.has_filter(f) for f in ("scdet", "silencedetect", "lut3d", "zoompan", "sendcmd"))


def ffgen(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-nostdin", *args, "-y"], check=True, timeout=300)


class PlanTests(unittest.TestCase):
    def test_pick_cuts_threshold_and_min_length(self):
        times = [0, 0.5, 1.0, 1.1, 2.0, 3.0]
        scores = [0, 2, 40, 50, 1, 30]
        self.assertEqual(cl.pick_cuts(times, scores, 10, 0.6), [1.0, 3.0])

    def test_cuts_to_segments_cover_duration(self):
        segs = cl.cuts_to_segments([2.0, 4.0], 6.0)
        self.assertEqual([(s["start"], s["end"]) for s in segs], [(0.0, 2.0), (2.0, 4.0), (4.0, 6.0)])

    def test_keep_segments_margin_and_frame_grid(self):
        segs = cl.keep_segments([(2.0, 3.5)], 6.0, margin=0.1, min_keep=0.2, fps=30)
        self.assertEqual(len(segs), 2)
        self.assertAlmostEqual(segs[0]["start"], 0.0)
        self.assertAlmostEqual(segs[0]["end"], 2.1, places=3)
        self.assertAlmostEqual(segs[1]["start"], 3.4, places=3)
        for s in segs:  # every boundary sits on a frame
            for t in (s["start"], s["end"]):
                self.assertAlmostEqual(t * 30, round(t * 30), places=3)

    def test_keep_segments_merges_short_gaps_and_drops_blips(self):
        segs = cl.keep_segments([(1.0, 1.1), (3.0, 3.05)], 5.0, margin=0.12, min_keep=0.2)
        self.assertEqual(len(segs), 1)  # tiny silences vanish inside the margins
        self.assertEqual(cl.keep_segments([(0.0, 2.0), (2.1, 5.0)], 5.0, margin=0.0, min_keep=0.2), [])

    def test_plan_validation(self):
        good = {"schema": cl.PLAN_SCHEMA, "source": "/x/a.mp4", "fps": 30,
                "segments": [{"start": 0, "end": 1}, {"start": 1, "end": 2}]}
        cl.normalize_plan(good)
        for bad in ({**good, "schema": "x"}, {**good, "segments": []},
                    {**good, "segments": [{"start": 1, "end": 0.5}]},
                    {**good, "segments": [{"start": 1, "end": 2}, {"start": 0, "end": 0.5}]}):
            with self.assertRaises(ValueError):
                cl.normalize_plan(bad)

    def test_edl_and_otio_shapes(self):
        plan = {"schema": cl.PLAN_SCHEMA, "source": "/x/My Clip.mp4", "fps": 30,
                "segments": [{"start": 1, "end": 2, "label": "a"}, {"start": 5, "end": 5.5}]}
        edl = cl.to_edl(plan, "T")
        self.assertIn("FCM: NON-DROP FRAME", edl)
        self.assertIn("001  MYCLIP   AA/V  C        00:00:01:00 00:00:02:00 00:00:00:00 00:00:01:00", edl)
        self.assertIn("002  MYCLIP   AA/V  C        00:00:05:00 00:00:05:15 00:00:01:00 00:00:01:15", edl)
        doc = cl.to_otio(plan)
        self.assertEqual(doc["OTIO_SCHEMA"], "Timeline.1")
        v = doc["tracks"]["children"][0]
        self.assertEqual(v["kind"], "Video")
        self.assertEqual(v["children"][1]["source_range"]["duration"]["value"], 15.0)

    def test_timecode(self):
        self.assertEqual(cl.tc(30 * 3661 + 7, 30), "01:01:01:07")

    def test_move_expressions(self):
        for m in cl.MOVES:
            z, x, y = cl.move_exprs(m, 1.3)
            self.assertTrue(all(isinstance(e, str) and e for e in (z, x, y)))
        with self.assertRaises(SystemExit):
            cl.move_exprs("spin", 1.3)

    def test_parse_size(self):
        self.assertEqual(cl.parse_size("1080x1920"), (1080, 1920))
        self.assertEqual(cl.parse_size("keep", 1281, 721), (1280, 720))
        for bad in ("1081x1920", "big"):
            with self.assertRaises(SystemExit):
                cl.parse_size(bad)

    def test_export_defaults(self):
        args = cl.encode_args()
        self.assertEqual(args[args.index("-crf") + 1], "17")
        self.assertEqual(args[args.index("-r") + 1], "30")
        self.assertIn("+faststart", args)
        self.assertIn("yuv420p", args)
        self.assertEqual(cl.VERTICAL, (1080, 1920))
        self.assertEqual(args[args.index("-preset") + 1], "slow")  # follows export_profile.py
        self.assertIn("bt709", args)


@unittest.skipUnless(HAVE_NP, "numpy not installed")
class NumpyTests(unittest.TestCase):
    def test_cube_identity_at_zero_strength(self):
        text = cl.make_cube("teal-orange", 0.0, size=5)
        rows = [list(map(float, l.split())) for l in text.splitlines() if l and l[0].isdigit()]
        self.assertEqual(len(rows), 125)
        self.assertEqual(rows[1], [0.25, 0.0, 0.0])  # red changes fastest
        self.assertEqual(rows[5], [0.0, 0.25, 0.0])

    def test_every_look_stays_in_range(self):
        for look in cl.LOOKS:
            rows = [list(map(float, l.split())) for l in cl.make_cube(look, 1.0, 9).splitlines() if l and l[0].isdigit()]
            self.assertEqual(len(rows), 729, look)
            self.assertTrue(all(0 <= v <= 1 for r in rows for v in r), look)

    def test_noir_is_monochrome(self):
        rows = [list(map(float, l.split())) for l in cl.make_cube("noir", 1.0, 5).splitlines() if l and l[0].isdigit()]
        self.assertTrue(all(abs(r[0] - r[1]) < 1e-6 and abs(r[1] - r[2]) < 1e-6 for r in rows))

    def test_phase_shift_finds_translation(self):
        import numpy as np
        rng = np.random.default_rng(1)
        a = rng.random((64, 96)).astype(np.float32)
        b = np.roll(a, (3, 4), axis=(0, 1))
        self.assertAlmostEqual(cl.phase_shift(b, a), 5.0, places=3)

    def test_smooth_path_caps_speed(self):
        import numpy as np
        xs = np.array([0.0] * 5 + [100.0] * 5)
        out = cl.smooth_path(xs, fps=5, max_speed=50, alpha=1.0, median=1)
        self.assertLessEqual(float(np.abs(np.diff(out)).max()), 10.0 + 1e-9)

    def test_subject_path_follows_bright_mover(self):
        import numpy as np
        frames = np.zeros((6, 40, 160), dtype=np.float32)
        for i in range(6):
            frames[i, 15:25, 20 + i * 20: 30 + i * 20] = 255
        left = cl.subject_path(frames, 40)
        centres = left + 20
        for i in range(1, 6):  # crop centre near the box centre (box centre = 25 + 20 i)
            self.assertLess(abs(centres[i] - (25 + 20 * i)), 12, (i, centres[i]))


@unittest.skipUnless(HAVE_FILTERS and HAVE_NP, "ffmpeg with scdet/silencedetect/lut3d/zoompan/sendcmd and numpy needed")
class FFmpegTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="cinema_lab_test_"))
        cls.three = cls.tmp / "three.mp4"
        ffgen("-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=2", "-f", "lavfi", "-i", "color=c=0x2050a0:s=320x180:r=30:d=2",
              "-f", "lavfi", "-i", "mandelbrot=s=320x180:r=30", "-f", "lavfi", "-i", "sine=f=440:d=6:sample_rate=48000",
              "-filter_complex", "[2]trim=duration=2,setpts=PTS-STARTPTS[m];[0][1][m]concat=n=3[v];"
              "[3]volume='if(between(t,2,3.5),0,1)':eval=frame[a]", "-map", "[v]", "-map", "[a]",
              "-c:v", "libx264", "-c:a", "aac", str(cls.three))
        cls.box = cls.tmp / "box.mp4"
        ffgen("-f", "lavfi", "-i", "color=black:s=640x360:r=30:d=4", "-f", "lavfi", "-i", "color=white:s=40x40:r=30:d=4",
              "-f", "lavfi", "-i", "sine=f=300:d=4", "-filter_complex", "[0][1]overlay=x='60+t*120':y=160[v]",
              "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-c:a", "aac", str(cls.box))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run_cmd(self, *argv):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(cl.main(list(argv)), 0)
        return json.loads(buf.getvalue())

    def test_scenes_ffmpeg_engine(self):
        out = self.tmp / "sc"
        r = self.run_cmd("scenes", "--input", str(self.three), "--out", str(out), "--engine", "ffmpeg",
                         "--sheet", "--timeline")
        self.assertEqual(len(r["cuts"]), 2)
        for got, want in zip(r["cuts"], (2.0, 4.0)):
            self.assertLess(abs(got - want), 0.07)
        self.assertTrue((out / "storyboard.jpg").is_file())
        self.assertTrue(Path(r["timeline"]["edl"]).read_text().count("AA/V  C") == 3)

    def test_silence_cut_keeps_sync(self):
        out = self.tmp / "sc.mp4"
        r = self.run_cmd("silence-cut", "--input", str(self.three), "--output", str(out), "--force")
        self.assertEqual(r["segments"], 2)
        self.assertAlmostEqual(r["output"]["duration"], 6.0 - 1.5 + 0.24, delta=0.1)
        self.assertLess(abs(r["av_duration_gap_s"]), 0.05)

    def test_grade_changes_colour_and_copies_audio(self):
        out = self.tmp / "g.mp4"
        r = self.run_cmd("grade", "--input", str(self.three), "--output", str(out), "--look", "noir", "--strength", "1",
                         "--force")
        self.assertLess(r["after"]["saturation"], r["before"]["saturation"] * 0.2)
        self.assertEqual(r["output"]["acodec"], "aac")

    def test_reframe_vertical_follows_box(self):
        out = self.tmp / "rf.mp4"
        r = self.run_cmd("reframe", "--input", str(self.box), "--output", str(out), "--force")
        self.assertEqual((r["output"]["width"], r["output"]["height"]), (1080, 1920))
        self.assertGreater(r["camera_travel_px"], 50)
        import numpy as np
        for t in (1.0, 3.0):
            p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(out), "-frames:v", "1", "-vf",
                                "scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True)
            a = np.frombuffer(p.stdout, np.uint8).reshape(96, 54)
            self.assertTrue((a > 128).any(), f"subject left the frame at t={t}")

    def test_camera_on_still(self):
        img = self.tmp / "still.png"
        ffgen("-f", "lavfi", "-i", "testsrc2=s=640x360", "-frames:v", "1", str(img))
        out = self.tmp / "cam.mp4"
        r = self.run_cmd("camera", "--input", str(img), "--output", str(out), "--move", "push-in", "--duration", "1",
                         "--supersample", "1", "--force")
        self.assertTrue(r["still"])
        self.assertEqual((r["output"]["width"], r["output"]["height"], r["output"]["fps"]), (1080, 1920, 30.0))
        self.assertAlmostEqual(r["output"]["duration"], 1.0, delta=0.05)

    def test_review_metrics_identical(self):
        out = self.tmp / "rv.mp4"
        r = self.run_cmd("review", "--a", str(self.box), "--b", str(self.box), "--output", str(out), "--height", "180",
                         "--metrics", "--force")
        self.assertGreater(r["metrics"]["ssim"], 0.999)

    def test_never_overwrites_without_force(self):
        out = self.tmp / "exists.mp4"
        out.write_bytes(b"keep")
        with self.assertRaises(SystemExit):
            cl.main(["grade", "--input", str(self.three), "--output", str(out)])
        self.assertEqual(out.read_bytes(), b"keep")


if __name__ == "__main__":
    unittest.main()
