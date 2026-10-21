"""Montage Pro task force: real ffmpeg runs on synthetic media (skipped when ffmpeg is absent)."""
import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import montage_pro as M  # noqa: E402

HAVE = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


@unittest.skipUnless(HAVE, "ffmpeg/ffprobe not installed")
class MontageProTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.clip = cls.tmp / "clip.mp4"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=25:duration=3",
                        "-f", "lavfi", "-i", "smptebars=size=640x360:rate=25:duration=3", "-f", "lavfi", "-i", "sine=frequency=330:duration=6",
                        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]", "-map", "[v]", "-map", "2:a",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(cls.clip)], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_team_and_options(self):
        t = M.team()
        self.assertGreaterEqual(len(t["roles"]), 10)
        for r in t["roles"]:
            self.assertTrue(r["gate"] and r["mission"])

    def test_video_pipeline(self):
        job = self.tmp / "job"
        it = M.intake(self.clip, job)
        self.assertEqual(it["kind"], "video")
        self.assertEqual(it["cuts"]["seconds"], [3.0])
        menu = {m["id"]: m for m in M.options(job)["menu"]}
        self.assertEqual(menu["reframe"]["status"], "ready")
        r = M.build(job, "reframe", "9:16", deliver=True)
        self.assertEqual(r["status"], "rendered")
        self.assertTrue(r["master_unchanged"])
        self.assertEqual(r["delivery_mix"]["verify"]["exit"], 0)
        h = M.build(job, "highlight-reel", "3")
        self.assertEqual(len(h["segments"]), 2)

    def test_acquire_requires_licence(self):
        with self.assertRaises(SystemExit):
            M.acquire("https://example.com/a.mp4", self.tmp / "j2", "", "", False)

    def test_needs_inputs_option_does_not_pretend(self):
        job = self.tmp / "job3"
        M.intake(self.clip, job)
        r = M.build(job, "broll-documentary")
        self.assertEqual(r["status"], "needs-inputs")


if __name__ == "__main__":
    unittest.main()
