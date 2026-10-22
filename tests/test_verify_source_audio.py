"""verify_video.py --source-audio: packet-MD5 gate for untouched source audio (contract §3).

Fixtures are generated at runtime (ffmpeg lavfi sine + testsrc, 2 s, 160x120); every ffmpeg test skips without ffmpeg.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
TOOL = ROOT / "tools" / "verify_video.py"
SKILL_COPY = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts" / "verify_video.py"
HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
MD5_LABEL = "audio identical to source (packet MD5)"


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", *args], check=True, timeout=60)


class SkillCopyTests(unittest.TestCase):
    def test_skill_copy_is_byte_identical(self):
        if not (TOOL.is_file() and SKILL_COPY.is_file()):
            self.skipTest("one of the two verify_video.py copies is not in this checkout")
        self.assertEqual(TOOL.read_bytes(), SKILL_COPY.read_bytes(), "tools/verify_video.py and the skill copy drifted")


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe not installed")
class SourceAudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        d = Path(cls._tmp.name)
        cls.d = d
        cls.src = d / "voice.m4a"  # quiet sine: about -22 LUFS, far from the -14 target on purpose
        ff("-f", "lavfi", "-i", "sine=frequency=440:duration=2:sample_rate=48000", "-c:a", "aac", "-b:a", "96k", str(cls.src))
        video = ["-f", "lavfi", "-i", "testsrc=size=160x120:rate=30:duration=2"]
        cls.copy = d / "copy.mp4"  # -c:a copy keeps the source packets
        ff(*video, "-i", str(cls.src), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", str(cls.copy))
        cls.reenc = d / "reenc.mp4"  # AAC -> AAC re-encode: same sound, different packets
        ff(*video, "-i", str(cls.src), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", str(cls.reenc))
        cls.mute = d / "mute.mp4"  # no audio stream at all
        ff(*video, "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.mute))
        # raw ADTS .aac (a common voice export): the MP4 mux strips its 7-byte headers, the sound is untouched
        cls.adts = d / "voice.aac"
        ff("-f", "lavfi", "-i", "sine=frequency=440:duration=2:sample_rate=48000", "-c:a", "aac", "-b:a", "96k", str(cls.adts))
        cls.adts_copy = d / "adts_copy.mp4"
        ff(*video, "-i", str(cls.adts), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", str(cls.adts_copy))
        # the source carried untouched as stream 1 plus a loud stereo bed as stream 2, flagged default so that
        # ffmpeg's own stream choice would measure the bed rather than the hashed source
        cls.two = d / "two.mp4"
        ff(*video, "-i", str(cls.src), "-f", "lavfi", "-i", "sine=frequency=220:duration=2:sample_rate=48000",
           "-filter_complex", "[2:a]volume=8,pan=stereo|c0=c0|c1=c0[bed]", "-map", "0:v", "-map", "1:a", "-map", "[bed]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a:0", "copy", "-c:a:1", "aac",
           "-disposition:a:0", "0", "-disposition:a:1", "default", str(cls.two))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def verify(self, video, *extra, name="r.json", timing=True):
        out = self.d / name
        if out.exists():
            out.unlink()
        base = ["--fps", "30", "--duration", "2"] if timing else ["--fps", "30"]
        r = subprocess.run([PY, str(TOOL), str(video), *base, *extra, "--json", str(out)], capture_output=True, text=True, timeout=120)
        report = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
        return r, report

    def assert_status_field(self, rep):
        """With --source-audio every JSON check has a status, and "pass" is false exactly for FAIL."""
        for c in rep["checks"]:
            self.assertEqual(list(c), ["check", "pass", "value", "status"], c)
            self.assertIn(c["status"], ("PASS", "FAIL", "INFO"), c)
            self.assertIs(c["pass"], c["status"] != "FAIL", c)

    def mux_copy(self, source, out, *encode_source, rate=48000):
        """Encode a 2 s sine as `source`, then mux it with -c:a copy (no -shortest: it may drop the last packet) into `out`."""
        ff("-f", "lavfi", "-i", f"sine=frequency=440:duration=2:sample_rate={rate}", *encode_source, str(source))
        ff("-f", "lavfi", "-i", "testsrc=size=160x120:rate=30:duration=2", "-i", str(source), "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", str(out))

    def test_copy_mux_matches_and_loudness_becomes_info(self):
        r, rep = self.verify(self.copy, "--source-audio", str(self.src), "--lufs", "-14")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f"[PASS] {MD5_LABEL}", r.stdout)
        self.assertRegex(r.stdout, r"\[INFO\] integrated loudness -14 LUFS ±1\.5 +source preserved: -?[\d.]+ LUFS \(not normalised by design\)")
        self.assertRegex(r.stdout, r"\[INFO\] true peak ≤ -1 dBFS +source preserved: -?[\d.]+ dBFS \(not normalised by design\)")
        self.assertNotIn("[FAIL]", r.stdout)
        self.assertRegex(r.stdout.strip().splitlines()[-1], r"^(\d+)/\1 checks passed, 2 info \(not scored\)$")
        sa = rep["source_audio"]
        self.assertEqual(set(sa), {"md5_match", "video_md5", "source_md5"})
        self.assertIs(sa["md5_match"], True)
        self.assertEqual(sa["video_md5"], sa["source_md5"])
        self.assertRegex(sa["source_md5"], r"^[0-9a-f]{32}$")
        info = [c for c in rep["checks"] if c.get("status") == "INFO"]
        self.assertEqual(len(info), 2)
        self.assertTrue(all(c["pass"] is True for c in info), info)  # a consumer counting falsy "pass" sees no failure
        self.assertEqual([c for c in rep["checks"] if not c["pass"]], [])
        self.assert_status_field(rep)
        self.assertRegex(r.stdout, r"\[PASS\] one audio stream \(nothing beside the source\) +1 audio stream\n")
        # the same file without the flag is scored against -14 LUFS and fails: INFO is what turned that into a pass
        plain, plain_rep = self.verify(self.copy, "--lufs", "-14", name="plain.json")
        self.assertEqual(plain.returncode, 1)
        self.assertIn("[FAIL] integrated loudness -14 LUFS ±1.5", plain.stdout)
        self.assertNotIn("source_audio", plain_rep)

    def test_reencoded_audio_fails_and_loudness_stays_scored(self):
        r, rep = self.verify(self.reenc, "--source-audio", str(self.src), "--lufs", "-14")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(f"[FAIL] {MD5_LABEL}", r.stdout)
        self.assertIn("[FAIL] integrated loudness -14 LUFS ±1.5", r.stdout)
        self.assertNotIn("[INFO]", r.stdout)
        self.assertNotIn("info (not scored)", r.stdout)
        sa = rep["source_audio"]
        self.assertIs(sa["md5_match"], False)
        self.assertNotEqual(sa["video_md5"], sa["source_md5"])
        self.assert_status_field(rep)
        self.assertNotIn("INFO", {c["status"] for c in rep["checks"]})
        md5 = next(c for c in rep["checks"] if c["check"] == MD5_LABEL)
        self.assertEqual((md5["pass"], md5["status"]), (False, "FAIL"))

    def test_adts_aac_source_muxed_with_copy_matches(self):
        # fixture sanity: the raw packet hashes really differ (ADTS headers stripped by the mux), so this test exercises the bsf
        raw = [re.search(r"MD5=(\w+)", subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"],
                                                      capture_output=True, text=True, timeout=60).stdout).group(1) for p in (self.adts, self.adts_copy)]
        self.assertNotEqual(raw[0], raw[1])
        r, rep = self.verify(self.adts_copy, "--source-audio", str(self.adts), "--lufs", "-14", timing=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f"[PASS] {MD5_LABEL}", r.stdout)
        self.assertNotIn("[FAIL]", r.stdout)
        self.assertRegex(r.stdout, r"\[INFO\] integrated loudness -14 LUFS ±1\.5 +source preserved: ")
        sa = rep["source_audio"]
        self.assertIs(sa["md5_match"], True)
        self.assertEqual(sa["video_md5"], sa["source_md5"])
        self.assertEqual(sa["video_md5"], raw[1])  # MP4-style AAC passes through aac_adtstoasc unchanged
        self.assert_status_field(rep)
        # an ADTS re-encode of the same sound is still caught
        r2, rep2 = self.verify(self.reenc, "--source-audio", str(self.adts), name="adts_reenc.json")
        self.assertEqual(r2.returncode, 1)
        self.assertIn(f"[FAIL] {MD5_LABEL}", r2.stdout)
        self.assertIs(rep2["source_audio"]["md5_match"], False)

    def test_preserved_pcm_keeps_the_codec_check_failing(self):
        # PCM is hashed without the AAC filter (it would make ffmpeg exit 234); carried untouched it still is no delivery codec
        src, mov = self.d / "voice.wav", self.d / "pcm.mov"
        self.mux_copy(src, mov, "-c:a", "pcm_s16le")
        r, rep = self.verify(mov, "--source-audio", str(src), "--lufs", "-14", name="pcm.json", timing=False)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(f"[PASS] {MD5_LABEL}", r.stdout)
        self.assertIn("[FAIL] audio codec is AAC", r.stdout)
        self.assertIn("pcm_s16le: source preserved, but only AAC or MP3 is accepted for delivery", r.stdout)
        self.assertRegex(r.stdout, r"\[INFO\] integrated loudness -14 LUFS ±1\.5 +source preserved: ")
        self.assertEqual([c["check"] for c in rep["checks"] if c["status"] == "FAIL"], ["audio codec is AAC"])
        self.assert_status_field(rep)

    def test_preserved_low_rate_mp3_is_info_not_failure(self):
        src, mp4 = self.d / "voice22.mp3", self.d / "mp3.mp4"
        try:
            self.mux_copy(src, mp4, "-c:a", "libmp3lame", "-b:a", "64k", rate=22050)
        except subprocess.CalledProcessError:
            self.skipTest("this ffmpeg has no MP3 encoder or cannot put MP3 in MP4")
        r, rep = self.verify(mp4, "--source-audio", str(src), "--lufs", "-14", name="mp3.json", timing=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f"[PASS] {MD5_LABEL}", r.stdout)
        self.assertRegex(r.stdout, r"\[INFO\] audio codec is AAC +source preserved: mp3 \(not re-encoded by design\)")
        self.assertRegex(r.stdout, r"\[INFO\] sample rate ≥ 44\.1 kHz +source preserved: 22050 \(not resampled by design\)")
        self.assertRegex(r.stdout.strip().splitlines()[-1], r"^(\d+)/\1 checks passed, 4 info \(not scored\)$")
        self.assert_status_field(rep)
        # without the flag the same file fails on codec and rate: the preserved source is what turns them into INFO
        plain, _ = self.verify(mp4, "--lufs", "-14", name="mp3_plain.json", timing=False)
        self.assertEqual(plain.returncode, 1)
        self.assertIn("[FAIL] audio codec is AAC", plain.stdout)
        self.assertIn("[FAIL] sample rate ≥ 44.1 kHz", plain.stdout)

    def test_extra_audio_stream_fails_and_loudness_is_scored_on_the_source(self):
        r, rep = self.verify(self.two, "--source-audio", str(self.src), "--lufs", "-14", name="two.json")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(f"[PASS] {MD5_LABEL}", r.stdout)  # the first stream is the untouched source …
        self.assertRegex(r.stdout, r"\[FAIL\] one audio stream \(nothing beside the source\) +2 audio streams")  # … but not alone
        self.assertNotIn("[INFO]", r.stdout)
        self.assertIs(rep["source_audio"]["md5_match"], True)
        # loudness is measured on the hashed stream 0:a:0 (quiet, about -22 LUFS), not on the loud default bed
        self.assertLess(rep["loudness"]["integrated_lufs"], -15, rep["loudness"])
        self.assertIn("[FAIL] integrated loudness -14 LUFS ±1.5", r.stdout)
        self.assert_status_field(rep)

    def test_video_without_audio_fails_the_md5_check(self):
        r, rep = self.verify(self.mute, "--source-audio", str(self.src))
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"[FAIL] {MD5_LABEL}", r.stdout)
        self.assertEqual(rep["source_audio"], {"md5_match": False, "video_md5": None, "source_md5": rep["source_audio"]["source_md5"]})

    def test_unreadable_source_exits_2_without_traceback(self):
        text = self.d / "timeline.json"
        text.write_text('{"scenes": []}', encoding="utf-8")
        cases = {"missing source": ["--source-audio", str(self.d / "nope.m4a")],
                 "not media": ["--source-audio", str(text)],
                 "source without audio": ["--source-audio", str(self.mute)],
                 "contradicts --no-audio": ["--source-audio", str(self.src), "--no-audio"]}
        for name, extra in cases.items():
            r, rep = self.verify(self.copy, *extra, name="bad.json")
            self.assertEqual(r.returncode, 2, name)
            self.assertNotIn("Traceback", r.stderr, name)
            self.assertTrue(r.stderr.strip(), name)
            self.assertIsNone(rep, name)
        r, _ = self.verify(self.copy, "--source-audio", str(self.mute), name="bad.json")
        self.assertIn("no audio stream", r.stderr)

    def test_without_flag_output_shape_is_unchanged(self):
        r, rep = self.verify(self.copy, "--aspect", "4:3", "--audio", str(self.src))
        self.assertNotIn("[INFO]", r.stdout)
        self.assertNotIn(MD5_LABEL, r.stdout)
        self.assertRegex(r.stdout.strip().splitlines()[-1], r"^\d+/\d+ checks passed$")
        self.assertNotIn("source_audio", rep)
        for c in rep["checks"]:
            self.assertEqual(list(c), ["check", "pass", "value"])
            self.assertIsInstance(c["pass"], bool)
        lines = [l for l in r.stdout.splitlines() if l.startswith("[")]
        self.assertTrue(lines and all(re.match(r"^\[(PASS|FAIL)\] ", l) for l in lines), lines)


if __name__ == "__main__":
    unittest.main()
