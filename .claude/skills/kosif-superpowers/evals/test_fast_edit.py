"""Tests for scripts/fast_edit.py: pure planning logic always, real FFmpeg runs when available."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fast_edit as fe  # noqa: E402

HAVE_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


class PlanTests(unittest.TestCase):
    KFS = [0.0, 1.0, 2.0, 3.0]

    def test_on_keyframe_copies(self):
        p = fe.plan_cut(self.KFS, 1.0, 2.5)
        self.assertEqual(p["mode"], "copy")
        self.assertEqual(p["copy_drift"], 0.0)

    def test_between_keyframes_reencodes(self):
        p = fe.plan_cut(self.KFS, 1.45, 2.5, tolerance=0.1)
        self.assertEqual(p["mode"], "exact")
        self.assertAlmostEqual(p["copy_drift"], 0.45, places=6)
        self.assertEqual(p["keyframe_at_or_before"], 1.0)
        self.assertEqual(p["next_keyframe"], 2.0)

    def test_tolerance_allows_copy(self):
        self.assertEqual(fe.plan_cut(self.KFS, 1.05, 2.5, tolerance=0.1)["mode"], "copy")

    def test_forced_copy_reports_drift(self):
        p = fe.plan_cut(self.KFS, 1.45, 2.5, mode="copy")
        self.assertEqual(p["mode"], "copy")
        self.assertAlmostEqual(p["copy_drift"], 0.45, places=6)

    def test_bad_ranges(self):
        for s, e in [(-1, 2), (2, 2), (3, 1), (float("nan"), 1)]:
            with self.assertRaises(ValueError):
                fe.plan_cut(self.KFS, s, e)
        with self.assertRaises(ValueError):
            fe.plan_cut(self.KFS, 0, 1, mode="fast")

    def test_voice_filter_uses_real_rate(self):
        f = fe.voice_filter("chipmunk", 48000)
        self.assertIn("asetrate=64800", f)
        self.assertIn("aresample=48000", f)
        self.assertNotIn("44100", f)
        self.assertIn("highpass", fe.voice_filter("radio", 22050))
        with self.assertRaises(ValueError):
            fe.voice_filter("alien", 48000)
        with self.assertRaises(ValueError):
            fe.voice_filter("deep", 0)

    def test_brighten_filter_bounds(self):
        self.assertIn("curves=", fe.brighten_filter(0.5))
        self.assertIn("hqdn3d", fe.brighten_filter(0.5, denoise=True))
        for bad in (0, -0.2, 1.5):
            with self.assertRaises(ValueError):
                fe.brighten_filter(bad)


def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-y", *args],
                   check=True, capture_output=True, timeout=120)


def zero_cross_hz(path, rate):
    """Estimate the dominant frequency of a mono tone by counting sign changes."""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(rate),
                          "-f", "s16le", "-"], capture_output=True, check=True, timeout=60).stdout
    n = len(raw) // 2
    vals = [int.from_bytes(raw[i * 2:i * 2 + 2], "little", signed=True) for i in range(n)]
    mid = vals[n // 4: 3 * n // 4]
    crossings = sum(1 for x, y in zip(mid, mid[1:]) if (x < 0) != (y < 0))
    return crossings / 2 / (len(mid) / rate)


@unittest.skipUnless(HAVE_FF, "ffmpeg/ffprobe required")
class FFmpegTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.td = tempfile.TemporaryDirectory(prefix="fast-edit-")
        d = cls.d = Path(cls.td.name)
        cls.clip = d / "clip.mp4"      # keyframe every 1 s, AAC audio
        ff("-f", "lavfi", "-i", "testsrc2=s=320x180:r=10:d=4", "-f", "lavfi", "-i", "sine=f=440:r=48000:d=4",
           "-c:v", "libx264", "-g", "10", "-keyint_min", "10", "-sc_threshold", "0", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-shortest", str(cls.clip))
        cls.dark = d / "dark.mp4"
        ff("-f", "lavfi", "-i", "testsrc2=s=320x180:r=10:d=2", "-vf", "eq=brightness=-0.35:contrast=0.5",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.dark))
        cls.bright = d / "bright.mp4"
        ff("-f", "lavfi", "-i", "color=c=0xd0d0d0:s=320x180:r=10:d=1", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           str(cls.bright))

    @classmethod
    def tearDownClass(cls):
        cls.td.cleanup()

    def call(self, *args):
        from io import StringIO
        from contextlib import redirect_stdout
        buf = StringIO()
        with redirect_stdout(buf):
            code = fe.main(list(args))
        self.assertEqual(code, 0)
        return json.loads(buf.getvalue())

    def test_keyframes(self):
        r = self.call("keyframes", "--input", str(self.clip))
        self.assertEqual(r["keyframes"][:4], [0.0, 1.0, 2.0, 3.0])

    def test_cut_on_keyframe_is_copy(self):
        out = self.d / "copy.mp4"
        r = self.call("cut", "--input", str(self.clip), "--output", str(out), "--start", "1", "--end", "3")
        self.assertEqual(r["plan"]["mode"], "copy")
        self.assertEqual(r["start_error"], 0)
        self.assertAlmostEqual(r["output_duration"], 2.0, delta=0.25)

    def test_cut_between_keyframes_is_exact(self):
        out = self.d / "exact.mp4"
        r = self.call("cut", "--input", str(self.clip), "--output", str(out), "--start", "1.5", "--end", "3",
                      "--preset", "ultrafast")
        self.assertEqual(r["plan"]["mode"], "exact")
        self.assertAlmostEqual(r["plan"]["copy_drift"], 0.5, places=3)
        self.assertAlmostEqual(r["output_duration"], 1.5, delta=0.15)

    def test_forced_copy_starts_on_keyframe(self):
        out = self.d / "forced.mp4"
        r = self.call("cut", "--input", str(self.clip), "--output", str(out), "--start", "1.5", "--end", "3",
                      "--mode", "copy")
        self.assertEqual(r["actual_start"], 1.0)
        self.assertAlmostEqual(r["start_error"], -0.5, places=3)
        self.assertAlmostEqual(r["output_duration"], 2.0, delta=0.25)

    def test_refuses_overwrite_and_same_file(self):
        out = self.d / "exists.mp4"
        out.write_bytes(b"x")
        self.assertEqual(fe.main(["cut", "--input", str(self.clip), "--output", str(out), "--start", "1"]), 2)
        self.assertEqual(out.read_bytes(), b"x")
        self.assertEqual(fe.main(["cut", "--input", str(self.clip), "--output", str(self.clip), "--start", "1",
                                  "--force"]), 2)

    def test_voice_chipmunk_raises_pitch_keeps_length_and_rate(self):
        out = self.d / "chip.wav"
        r = self.call("voice", "--input", str(self.clip), "--output", str(out), "--preset", "chipmunk")
        self.assertEqual(r["sample_rate"], 48000)
        info = fe.probe(out)
        self.assertEqual(int(fe.stream(info, "audio")["sample_rate"]), 48000)
        self.assertAlmostEqual(r["output_duration"], r["input_duration"], delta=0.1)
        self.assertAlmostEqual(zero_cross_hz(out, 48000), 440 * 1.35, delta=15)

    def test_voice_keeps_video_untouched(self):
        out = self.d / "radio.mp4"
        r = self.call("voice", "--input", str(self.clip), "--output", str(out), "--preset", "radio")
        self.assertEqual(r["video"], "stream-copied")
        self.assertEqual(fe.stream(fe.probe(out), "video")["codec_name"], "h264")

    def test_brighten_lifts_dark_clip(self):
        out = self.d / "lifted.mp4"
        r = self.call("brighten", "--input", str(self.dark), "--output", str(out), "--denoise",
                      "--preset", "ultrafast")
        self.assertFalse(r["skipped"])
        self.assertGreater(r["luma_gain"], 10)

    def test_brighten_skips_bright_clip(self):
        out = self.d / "nolift.mp4"
        r = self.call("brighten", "--input", str(self.bright), "--output", str(out))
        self.assertTrue(r["skipped"])
        self.assertFalse(out.exists())

    def test_extract_audio_copy_and_encode(self):
        m4a = self.d / "a.m4a"
        r = self.call("extract-audio", "--input", str(self.clip), "--output", str(m4a))
        self.assertTrue(r["copied"])
        wav = self.d / "a.wav"
        r = self.call("extract-audio", "--input", str(self.clip), "--output", str(wav))
        self.assertFalse(r["copied"])
        self.assertEqual(fe.stream(fe.probe(wav), "audio")["codec_name"], "pcm_s16le")


if __name__ == "__main__":
    unittest.main()
