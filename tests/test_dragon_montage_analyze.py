"""Dragon Montage station 1 «العين الأولى» — dm_analyze.py → analysis.json."""
import json
import math
import struct
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-dragon-montage" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import dm_common as dm  # noqa: E402

ANALYZE = SCRIPTS / "dm_analyze.py"


def click_track(path: Path, bpm: float = 120.0, seconds: float = 20.0, sr: int = 22050):
    """Mono 16-bit click track; every 4th click accented."""
    n = int(sr * seconds)
    buf = [0.0] * n
    period = 60.0 / bpm
    length = int(0.03 * sr)
    i, t = 0, 0.0
    while t < seconds:
        start, amp = int(t * sr), (0.9 if i % 4 == 0 else 0.45)
        for k in range(min(length, n - start)):
            buf[start + k] += amp * math.sin(2 * math.pi * 1000 * k / sr) * math.exp(-k / (0.005 * sr))
        i, t = i + 1, t + period
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 32767)) for x in buf))
    return path


class AnalyzeStation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="dm_analyze_test_")
        base = Path(cls.tmp.name)
        cls.clip = dm.make_test_clip(base / "in.mp4", seconds=6.0)
        cls.music = click_track(base / "click.wav")
        cls.job = base / "job"
        res = subprocess.run([sys.executable, str(ANALYZE), "--job", str(cls.job), "--clip", str(cls.clip),
                              "--music", str(cls.music), "--no-transcribe"],
                             capture_output=True, text=True, timeout=600)
        if res.returncode != 0:
            raise AssertionError(res.stderr[-2000:])
        cls.data = json.loads((cls.job / "analysis.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_schema_valid(self):
        dm.validate("analysis", self.data)
        self.assertEqual(dm.read(self.job, "analysis")["schema"], "kosif.dm.analysis.v1")
        self.assertIn("contact_sheet", self.data)
        self.assertIsInstance(self.data["missing"], list)
        self.assertIn("ffprobe", self.data["tools_used"])

    def test_clip_probe(self):
        c = self.data["clips"][0]
        self.assertEqual(c["id"], "c01")
        self.assertAlmostEqual(c["duration"], 6.0, delta=0.2)
        self.assertEqual((c["width"], c["height"]), (1280, 720))
        self.assertAlmostEqual(c["fps"], 30, delta=0.5)
        self.assertTrue(c["has_audio"])
        self.assertIsNotNone(c["loudness_lufs"])

    def test_shots_near_cut(self):
        shots = self.data["clips"][0]["shots"]
        self.assertGreaterEqual(len(shots), 2)
        self.assertEqual(shots[0]["id"], "c01-s001")
        self.assertAlmostEqual(shots[0]["start"], 0.0, delta=0.01)
        self.assertAlmostEqual(shots[-1]["end"], self.data["clips"][0]["duration"], delta=0.05)
        starts = [s["start"] for s in shots[1:]]
        self.assertTrue(any(abs(s - 3.0) < 0.3 for s in starts), starts)
        for s in shots:
            self.assertGreater(s["end"], s["start"])
            q = s["quality"]
            for k in ("sharpness", "exposure", "shake", "score"):
                self.assertIn(k, q)
                if q[k] is not None:
                    self.assertGreaterEqual(q[k], 0.0)
                    self.assertLessEqual(q[k], 1.0)
            self.assertIn("faces", s)
            self.assertIn("motion_energy", s)
            self.assertIn("mean_rgb", s["color"])

    def test_thumbs_and_contact_sheet(self):
        for s in self.data["clips"][0]["shots"]:
            self.assertTrue(s["thumb"] and (self.job / s["thumb"]).is_file(), s["thumb"])
        if self.data["contact_sheet"]:
            self.assertTrue((self.job / self.data["contact_sheet"]).is_file())

    def test_audio_fields(self):
        c = self.data["clips"][0]
        self.assertIsInstance(c["silences"], list)
        self.assertGreaterEqual(len(c["energy"]), 10)          # 6 s / 0.5 s
        self.assertAlmostEqual(c["energy"][1]["t"] - c["energy"][0]["t"], 0.5, delta=0.01)
        self.assertGreater(max(e["rms"] for e in c["energy"]), 0.01)
        self.assertEqual(c["words"], [])                     # --no-transcribe

    def test_music_beats(self):
        m = self.data["music"]
        self.assertTrue(m["path"])
        self.assertIsNotNone(m["bpm"])
        self.assertLessEqual(abs(m["bpm"] - 120.0), 3.0, m["bpm"])
        self.assertGreaterEqual(len(m["beats"]), 30)
        self.assertTrue(m["downbeats"])
        self.assertTrue(set(m["downbeats"]) <= set(m["beats"]))

    def test_receipts(self):
        rec = dm.receipts(self.job)
        tools = {r["tool"] for r in rec}
        self.assertTrue(all(r["station"] == "analyze" for r in rec))
        for t in ("ffprobe", "ffmpeg.ebur128", "ffmpeg.silencedetect"):
            self.assertIn(t, tools)
        self.assertTrue(all("rc" in r and "seconds" in r for r in rec))


class AnalyzeSilenceAndMissing(unittest.TestCase):
    def test_silence_detected_and_no_music(self):
        with tempfile.TemporaryDirectory(prefix="dm_analyze_sil_") as td:
            td = Path(td)
            clip = td / "quiet.mp4"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=320x240:rate=25:duration=4",
                            "-f", "lavfi", "-i", "sine=frequency=300:duration=1.5", "-f", "lavfi",
                            "-i", "anullsrc=r=44100:cl=mono", "-filter_complex",
                            "[2:a]atrim=0:2.5[s];[1:a][s]concat=n=2:v=0:a=1[a]", "-map", "0:v", "-map", "[a]",
                            "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-t", "4", str(clip)],
                           check=True, timeout=60)
            job = td / "job"
            subprocess.run([sys.executable, str(ANALYZE), "--job", str(job), "--clip", str(clip), "--no-transcribe"],
                           check=True, capture_output=True, timeout=300)
            d = dm.read(job, "analysis")
            sil = d["clips"][0]["silences"]
            self.assertTrue(sil, "expected a silence after 1.5 s")
            self.assertAlmostEqual(sil[0]["start"], 1.5, delta=0.3)
            self.assertEqual(d["music"], {"path": None, "bpm": None, "beats": [], "downbeats": []})


class FaceModel(unittest.TestCase):
    def test_largest_face_normalised(self):
        import dm_analyze as A
        lf = A.largest_face([(10, 10, 20, 20, 0.9), (100, 50, 60, 80, 0.8)], 200, 400)
        self.assertAlmostEqual(lf[0], 0.65)
        self.assertAlmostEqual(lf[1], 0.225)
        self.assertEqual(A.largest_face([], 10, 10), None)

    def test_shot_has_face_center_field(self):
        import numpy as np
        import dm_analyze as A
        ctx = A.Ctx(Path(tempfile.mkdtemp(prefix="dm_face_")))
        m = A.shot_metrics(ctx, [np.zeros((90, 160, 3), np.uint8)] * 3)
        self.assertIn("face_center", m)
        self.assertIn("faces_box", m)

    def test_yunet_used_when_doctor_finds_model(self):
        import dm_doctor
        if not dm_doctor.model_path("yunet-face-model"):
            self.skipTest("YuNet model not downloaded (dm_doctor.py fetch yunet-face-model)")
        import dm_analyze as A
        A._FACE.clear()
        self.assertIsNotNone(A.face_detector())
        self.assertEqual(A._FACE["name"], "yunet")


@unittest.skipUnless(dm.have("ffmpeg") and dm.have_module("cv2") and dm.have_module("numpy"), "ffmpeg/opencv missing")
class StreamingAndWindowsSafety(unittest.TestCase):
    """Frames are streamed per shot (no whole-clip frame list), jpgs go through imencode (non-ASCII
    paths on Windows), and a timed-out ffmpeg pass degrades into `missing` instead of crashing."""

    def test_streamed_metrics_match_collected(self):
        import dm_analyze as A
        with tempfile.TemporaryDirectory(prefix="dm_stream_") as td:
            clip = dm.make_test_clip(Path(td) / "c.mp4", 4.0, size="320x180")
            ctx = A.Ctx(Path(td))
            info = A.probe_clip(ctx, clip)
            times, frames = A.sample_frames(ctx, clip, info)
            self.assertTrue(frames)
            bounds = [(0.0, 2.0), (2.0, info["duration"])]
            for s, e in bounds:
                sel = [f for t, f in zip(times, frames) if s <= t < e]
                self.assertEqual(len(sel), A.expected_samples(s, e))
                acc = A.ShotAcc(A.expected_samples(s, e))
                for t, f in A.iter_frames(ctx, clip, info):
                    if s <= t < e:
                        acc.add(f)
                self.assertEqual(acc.finish(ctx)["quality"], A.shot_metrics(ctx, sel)["quality"])
                self.assertLessEqual(len(acc.kept), 5)

    def test_station_writes_thumbs_under_arabic_path(self):
        with tempfile.TemporaryDirectory(prefix="dm_ar_") as td:
            job = Path(td) / "مونتاج التنين"
            clip = dm.make_test_clip(Path(td) / "فيديو.mp4", 4.0, size="320x180")
            import os
            env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
            r = subprocess.run([sys.executable, str(ANALYZE), "--job", str(job), "--clip", str(clip),
                                "--no-transcribe"], capture_output=True, timeout=300, env=env)
            self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
            d = dm.read(job, "analysis")
            thumbs = [s["thumb"] for s in d["clips"][0]["shots"]]
            self.assertTrue(thumbs and all(thumbs), thumbs)
            self.assertTrue(all((job / t).stat().st_size > 500 for t in thumbs))
            self.assertTrue((job / d["contact_sheet"]).is_file())

    def test_write_jpg_roundtrip(self):
        import numpy as np
        import dm_analyze as A
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "صورة.jpg"
            self.assertTrue(A.write_jpg(f, np.full((20, 30, 3), 200, np.uint8)))
            self.assertEqual(A.read_img(f).shape, (20, 30, 3))

    def test_timeout_degrades_to_missing(self):
        import dm_analyze as A
        with tempfile.TemporaryDirectory() as td:
            clip = dm.make_test_clip(Path(td) / "c.mp4", 2.0, size="160x90")
            ctx = A.Ctx(Path(td))
            old = A.LONG_TIMEOUT
            A.LONG_TIMEOUT = 0.001
            try:
                self.assertIsNone(A.shots_scdet(ctx, clip))
                self.assertIsNone(A.loudness(ctx, clip))
            finally:
                A.LONG_TIMEOUT = old
            self.assertTrue(any("timeout" in m for m in ctx.missing), ctx.missing)


if __name__ == "__main__":
    unittest.main()
