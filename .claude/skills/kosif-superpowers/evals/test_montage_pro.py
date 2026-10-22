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



# ------------------------------------------------------------------ transcribe (fake-model hook: fast and deterministic)
import contextlib, importlib, importlib.util, io, os, types  # noqa: E402,E401
from unittest import mock  # noqa: E402
import audio_cue_mapper  # noqa: E402
import cinematic_cut_planner  # noqa: E402
sys.path.insert(0, str(SK.parents[2] / "tools"))
import words_convert  # noqa: E402

# overlaps, unrounded times, whitespace/empty words, an empty segment and an out-of-order segment on purpose
FAKE = {"language": "ar", "segments": [
    {"text": " اللهم في يوم الخميس ", "start": 0.0, "end": 1.9, "words": [
        {"word": " اللهم", "start": 0.0, "end": 0.6812, "probability": 0.93456},
        {"word": " في", "start": 0.66, "end": 0.92, "probability": 0.9},
        {"word": "  ", "start": 0.92, "end": 0.95, "probability": 0.1},
        {"word": " يوم", "start": 0.92, "end": 1.18, "probability": 0.81},
        {"word": " الخميس", "start": 1.18, "end": 1.9004, "probability": 0.7}]},
    {"text": " ", "start": 1.9, "end": 2.0, "words": []},
    {"text": " اللهم ارزقنا", "start": 2.0, "end": 3.0, "words": [
        {"word": " ارزقنا", "start": 2.4, "end": 3.0, "probability": 0.88},
        {"word": " اللهم", "start": 2.0, "end": 2.45, "probability": 0.95}]}]}
HAVE_NUMPY = importlib.util.find_spec("numpy") is not None  # decode_16k needs it (it ships with faster-whisper)
EXPECTED = [("اللهم", 0.0, 0.66), ("في", 0.66, 0.92), ("يوم", 0.92, 1.18), ("الخميس", 1.18, 1.9),
            ("اللهم", 2.0, 2.4), ("ارزقنا", 2.4, 3.0)]


class TranscribeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.media = cls.tmp / "voice.wav"
        if HAVE:
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=4",
                            "-ac", "1", "-ar", "16000", str(cls.media)], check=True)
        else:  # the fake hook never decodes; without ffprobe the duration falls back to the last word end
            cls.media.write_bytes(b"RIFF-not-really-audio")
        cls.fake = cls.tmp / "fake.json"
        cls.fake.write_text(json.dumps(FAKE, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def cli(self, *args, fake=True, cmd="transcribe"):
        env = {k: v for k, v in os.environ.items() if k != M.FAKE_ENV}
        if fake:
            env[M.FAKE_ENV] = str(fake if isinstance(fake, Path) else self.fake)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, env, clear=True), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                rc = M.main([cmd, *map(str, args)])
            except SystemExit as exc:
                rc = exc.code
        return rc, out.getvalue(), err.getvalue()

    def test_schema_words_and_phrases(self):
        dst = self.tmp / "schema" / "words.json"
        rc, out, err = self.cli(self.media, "--out", dst)
        self.assertEqual(rc, 0, err)
        line = json.loads(out)
        self.assertEqual((line["status"], line["words"], line["phrases"]), ("written", 6, 2))
        self.assertIn("elapsed_s", line)
        d = json.loads(dst.read_text(encoding="utf-8"))
        self.assertEqual(d["schema"], "kosif-words/1")
        self.assertEqual(d["source"], {"file": "voice.wav", "sha256": M.sha256(self.media), "duration": 4.0 if HAVE else 3.0})
        e = d["engine"]
        self.assertEqual((e["name"], e["version"], e["model"], e["compute_type"], e["language"]),
                         ("fake", "fake", "medium", "int8", "ar"))  # the test hook never poses as faster-whisper
        self.assertEqual((e["vad_filter"], e["no_speech_threshold"]), (True, 0.6))
        self.assertNotIn("dropped_segments", d)
        self.assertNotIn("elapsed_s", json.dumps(d))  # the file stays deterministic
        self.assertEqual([(w["word"], w["start"], w["end"]) for w in d["words"]], EXPECTED)
        self.assertEqual(d["words"][0]["prob"], 0.935)
        for a, b in zip(d["words"], d["words"][1:]):
            self.assertLessEqual(a["end"], b["start"])
        for w in d["words"]:
            self.assertLess(w["start"], w["end"])
            self.assertEqual(w["word"], w["word"].strip())
            self.assertEqual((round(w["start"], 3), round(w["end"], 3)), (w["start"], w["end"]))
        self.assertEqual(d["phrases"], [
            {"text": "اللهم في يوم الخميس", "start": 0.0, "end": 1.9, "words": [0, 3]},
            {"text": "اللهم ارزقنا", "start": 2.0, "end": 3.0, "words": [4, 5]}])

    def test_skip_when_unchanged_then_force(self):
        dst = self.tmp / "skip" / "words.json"
        self.assertEqual(self.cli(self.media, "--out", dst)[0], 0)
        first = dst.read_text(encoding="utf-8")
        changed = self.tmp / "fake2.json"
        f2 = json.loads(json.dumps(FAKE))
        f2["segments"][0]["words"][0]["word"] = " يا رب"
        changed.write_text(json.dumps(f2, ensure_ascii=False), encoding="utf-8")
        rc, out, _ = self.cli(self.media, "--out", dst, fake=changed)
        self.assertEqual((rc, json.loads(out)["status"]), (0, "up to date"))
        self.assertEqual(dst.read_text(encoding="utf-8"), first)
        rc, out, _ = self.cli(self.media, "--out", dst, "--force", fake=changed)
        self.assertEqual((rc, json.loads(out)["status"]), (0, "written"))
        self.assertEqual(json.loads(dst.read_text(encoding="utf-8"))["words"][0]["word"], "يا رب")
        rc, out, _ = self.cli(self.media, "--out", dst, "--model", "small")  # another model is not "up to date"
        self.assertEqual(json.loads(out)["status"], "written")
        self.assertEqual(json.loads(dst.read_text(encoding="utf-8"))["engine"]["model"], "small")

    def test_foreign_words_file_needs_force(self):
        dst = self.tmp / "foreign" / "words.json"
        dst.parent.mkdir(parents=True)
        mine = '[{"word": "يدوي", "start": 0.1, "end": 0.5}]\n'
        dst.write_text(mine, encoding="utf-8")
        rc, out, err = self.cli(self.media, "--out", dst)
        self.assertEqual(rc, 2)
        self.assertIn("--force", err)
        self.assertEqual(dst.read_text(encoding="utf-8"), mine)
        self.assertEqual(self.cli(self.media, "--out", dst, "--force")[0], 0)
        self.assertEqual(json.loads(dst.read_text(encoding="utf-8"))["schema"], "kosif-words/1")

    def test_job_writes_words_and_report(self):
        job = self.tmp / "jobT"
        rc, out, err = self.cli(self.media, "--job", job)
        self.assertEqual(rc, 0, err)
        self.assertTrue((job / "words.json").is_file())
        self.assertEqual(json.loads((job / "report.json").read_text(encoding="utf-8"))["transcribe"]["words"], 6)
        self.assertEqual(self.cli(self.media)[0], 2)  # neither --job nor --out

    def test_missing_media_exit_2(self):
        dst = self.tmp / "missing" / "words.json"
        rc, out, err = self.cli(self.tmp / "nope.wav", "--out", dst)
        self.assertEqual(rc, 2)
        self.assertEqual(len(err.strip().splitlines()), 1)
        self.assertIn("no such media file", err)
        self.assertFalse(dst.exists())

    def test_no_faster_whisper_exit_2(self):
        dst = self.tmp / "nofw" / "words.json"
        with mock.patch.dict(sys.modules, {"faster_whisper": None}):  # import faster_whisper → ImportError
            rc, out, err = self.cli(self.media, "--out", dst, fake=False)
        self.assertEqual(rc, 2)
        self.assertEqual(len(err.strip().splitlines()), 1)
        self.assertIn("pip install faster-whisper", err)
        self.assertFalse(dst.exists())

    def test_no_ffmpeg_exit_2(self):
        stub = types.ModuleType("faster_whisper")
        with mock.patch.dict(sys.modules, {"faster_whisper": stub}), mock.patch.object(M.shutil, "which", return_value=None):
            rc, out, err = self.cli(self.media, "--out", self.tmp / "noff" / "words.json", fake=False)
        self.assertEqual(rc, 2)
        self.assertIn("ffmpeg not found", err)

    @unittest.skipUnless(HAVE and HAVE_NUMPY, "ffmpeg/ffprobe or numpy not installed")
    def test_model_not_cached_and_bad_media_exit_2(self):
        stub = types.ModuleType("faster_whisper")

        def not_cached(*a, **k):
            raise FileNotFoundError("LocalEntryNotFoundError: cannot find the requested files in the local cache")
        stub.WhisperModel = not_cached
        bad = self.tmp / "bad.wav"
        bad.write_text("not audio", encoding="utf-8")
        with mock.patch.dict(sys.modules, {"faster_whisper": stub}):
            rc, out, err = self.cli(self.media, "--out", self.tmp / "nc" / "words.json", "--local-only", fake=False)
            self.assertEqual(rc, 2)
            self.assertIn("not cached locally", err)
            rc, out, err = self.cli(bad, "--out", self.tmp / "bad" / "words.json", fake=False)
            self.assertEqual(rc, 2)
            self.assertIn("cannot decode", err)
            self.assertEqual(len(err.strip().splitlines()), 1)

    def test_existing_readers_accept_the_file(self):
        dst = self.tmp / "readers" / "words.json"
        self.assertEqual(self.cli(self.media, "--out", dst)[0], 0)
        d = json.loads(dst.read_text(encoding="utf-8"))
        dur = d["source"]["duration"]
        words = d["words"] if isinstance(d, dict) else d  # cinematic_cut_planner.main unwraps {"words": [...]} like this
        cinematic_cut_planner.validate_words(words, dur)
        self.assertEqual(len(audio_cue_mapper.import_aligned_words(dst, dur)), 6)
        self.assertEqual([w["word"] for w in words_convert.parse_json(dst.read_text(encoding="utf-8"))], [w[0] for w in EXPECTED])
        example = SK.parents[2] / "templates" / "words.example.json"  # the template still reads as before
        ex = json.loads(example.read_text(encoding="utf-8"))
        cinematic_cut_planner.validate_words(ex["words"], ex["duration_s"])
        self.assertEqual(len(audio_cue_mapper.import_aligned_words(example, ex["duration_s"])), len(ex["words"]))
        self.assertEqual(len(words_convert.parse_json(example.read_text(encoding="utf-8"))), len(ex["words"]))

    def test_tidy_words_edge_cases(self):
        segs = [{"text": "a", "words": [{"word": "x", "start": 1.0, "end": 1.0}, {"word": "y", "start": 1.0, "end": 1.2},
                                        {"word": "z", "start": 1.1, "end": 9.0}, {"word": "late", "start": 9.5, "end": 9.9}]}]
        words, phrases = M.tidy_words(segs, limit=5.0)
        self.assertEqual([(w["word"], w["start"], w["end"]) for w in words], [("x", 1.0, 1.001), ("y", 1.001, 1.1), ("z", 1.1, 5.0)])
        self.assertEqual(phrases, [{"text": "x y z", "start": 1.0, "end": 5.0, "words": [0, 2]}])  # "late" was cut: text = kept words
        self.assertEqual(M.tidy_words([{"text": "", "words": []}]), ([], []))

    @unittest.skipUnless(HAVE, "ffmpeg/ffprobe not installed")
    def test_intake_transcribe_is_opt_in(self):
        with mock.patch.dict(os.environ, {M.FAKE_ENV: str(self.fake)}):
            plain = M.intake(self.media, self.tmp / "jobA")
            self.assertNotIn("transcribe", plain)
            self.assertFalse((self.tmp / "jobA" / "words.json").exists())
            it = M.intake(self.media, self.tmp / "jobB", {"model": "medium", "language": "ar"})
        self.assertTrue(it["transcribe"]["ok"], it["transcribe"])
        self.assertTrue((self.tmp / "jobB" / "words.json").is_file())
        self.assertEqual(it["audio_cues"]["aligned_words"], 6)  # the cue mapper ran after transcription and imported them
        self.assertTrue(it["audio_cues"]["ok"])


# ------------------------------------------------------------------ transcribe: review findings (each test would have caught one)
REPO = SK.parents[2]
HAVE_GIT = bool(shutil.which("git"))
SILENT_GUESS = {"text": " اشترك في القناة", "start": 0.0, "end": 2.0, "no_speech_prob": 0.875, "avg_logprob": -0.814,
                "words": [{"word": " اشترك", "start": 0.0, "end": 0.82, "probability": 0.48},
                          {"word": " في", "start": 0.82, "end": 0.82, "probability": 0.11},
                          {"word": " القناة", "start": 0.82, "end": 2.0, "probability": 0.96}]}
SPEECH = {"text": " اللهم ارزقنا", "start": 2.0, "end": 3.0, "no_speech_prob": 0.0832, "avg_logprob": -0.1841,
          "words": [{"word": " اللهم", "start": 2.0, "end": 2.45, "probability": 0.95},
                    {"word": " ارزقنا", "start": 2.45, "end": 3.0, "probability": 0.88}]}


def ns(seg):  # faster-whisper returns objects with attributes, not dicts
    return types.SimpleNamespace(**{**seg, "words": [types.SimpleNamespace(**w) for w in seg["words"]]})


class TranscribeReviewTests(unittest.TestCase):
    setUpClass, tearDownClass, cli = TranscribeTests.__dict__["setUpClass"], TranscribeTests.__dict__["tearDownClass"], TranscribeTests.cli

    def fake_file(self, name, segments):
        f = self.tmp / name
        f.write_text(json.dumps({"language": "ar", "segments": segments}, ensure_ascii=False), encoding="utf-8")
        return f

    def test_no_speech_segments_are_dropped_and_recorded(self):  # finding 1: silence/music hallucination
        dst = self.tmp / "nsp" / "words.json"
        rc, out, err = self.cli(self.media, "--out", dst, fake=self.fake_file("sil.json", [SILENT_GUESS, SPEECH]))
        self.assertEqual(rc, 0, err)
        line = json.loads(out)
        self.assertEqual((line["words"], line["dropped_segments"]), (2, 1))
        self.assertIn("no_speech_prob", line["warning"])
        d = json.loads(dst.read_text(encoding="utf-8"))
        self.assertEqual([w["word"] for w in d["words"]], ["اللهم", "ارزقنا"])
        self.assertEqual(d["dropped_segments"], [{"text": "اشترك في القناة", "start": 0.0, "end": 2.0, "no_speech_prob": 0.875}])
        self.assertEqual(d["phrases"], [{"text": "اللهم ارزقنا", "start": 2.0, "end": 3.0, "words": [0, 1],
                                         "no_speech_prob": 0.083, "avg_logprob": -0.184}])
        rc, out, _ = self.cli(self.media, "--out", dst, "--no-speech-threshold", "1", fake=self.tmp / "sil.json")
        self.assertEqual(json.loads(out)["status"], "written")  # another threshold is not "up to date"; 1 keeps every segment
        self.assertEqual(len(json.loads(dst.read_text(encoding="utf-8"))["words"]), 5)
        rc, out, _ = self.cli(self.media, "--out", self.tmp / "nsp" / "only.json", fake=self.fake_file("sil2.json", [SILENT_GUESS]))
        line = json.loads(out)
        self.assertEqual((rc, line["words"]), (0, 0))
        self.assertIn("no words recognised", line["warning"])
        self.assertEqual(self.cli(self.media, "--out", dst, "--no-speech-threshold", "2")[0], 2)

    @unittest.skipUnless(HAVE and HAVE_NUMPY, "ffmpeg/ffprobe or numpy not installed")
    def test_real_engine_path_vad_version_and_fake_output(self):  # findings 1 (VAD on by default) and 6 (fake never up to date)
        calls = []

        class Model:
            def __init__(self, *a, **k):
                pass

            def transcribe(self, audio, **kw):
                calls.append(kw)
                return iter([ns(SILENT_GUESS), ns(SPEECH)]), types.SimpleNamespace(language="ar")
        stub = types.ModuleType("faster_whisper")
        stub.WhisperModel = Model
        dst = self.tmp / "realstub" / "words.json"
        self.assertEqual(self.cli(self.media, "--out", dst)[0], 0)  # written by the fake hook first
        with mock.patch.dict(sys.modules, {"faster_whisper": stub}), mock.patch.object(M, "_fw_version", return_value="1.2.1"):
            rc, out, err = self.cli(self.media, "--out", dst, fake=False)
            self.assertEqual((rc, json.loads(out)["status"]), (0, "written"), err)  # the fake file is not "up to date"
            self.assertIs(calls[-1]["vad_filter"], True)
            self.assertEqual((calls[-1]["word_timestamps"], calls[-1]["beam_size"], calls[-1]["language"]), (True, 5, "ar"))
            d = json.loads(dst.read_text(encoding="utf-8"))
            self.assertEqual((d["engine"]["name"], d["engine"]["version"], d["engine"]["vad_filter"]), ("faster-whisper", "1.2.1", True))
            self.assertEqual([w["word"] for w in d["words"]], ["اللهم", "ارزقنا"])
            n = len(calls)
            self.assertEqual(json.loads(self.cli(self.media, "--out", dst, fake=False)[1])["status"], "up to date")
            self.assertEqual(len(calls), n)
            rc, out, _ = self.cli(self.media, "--out", dst, "--no-vad", fake=False)
            self.assertEqual(json.loads(out)["status"], "written")
            self.assertIs(calls[-1]["vad_filter"], False)
            # a fake run over a real file is not "up to date" either (the hook's words are never kept as real ones)
            self.assertEqual(json.loads(self.cli(self.media, "--out", dst, "--no-vad")[1])["status"], "written")
        with mock.patch.dict(sys.modules, {"faster_whisper": stub}), mock.patch.object(M, "_fw_version", return_value="1.3.0"):
            self.cli(self.media, "--out", dst, fake=False)
            self.assertEqual(json.loads(self.cli(self.media, "--out", dst, fake=False)[1])["status"], "up to date")
        with mock.patch.dict(sys.modules, {"faster_whisper": stub}), mock.patch.object(M, "_fw_version", return_value="1.4.0"):
            self.assertEqual(json.loads(self.cli(self.media, "--out", dst, fake=False)[1])["status"], "written")  # engine upgraded

    def test_fake_output_does_not_satisfy_a_real_run(self):  # finding 6, without numpy/ffmpeg: the real run is attempted
        dst = self.tmp / "fakeonly" / "words.json"
        self.assertEqual(self.cli(self.media, "--out", dst)[0], 0)
        with mock.patch.dict(sys.modules, {"faster_whisper": None}):
            rc, out, err = self.cli(self.media, "--out", dst, fake=False)
        self.assertEqual(rc, 2)  # previously {"status": "up to date"} with the fake words
        self.assertIn("pip install faster-whisper", err)

    @unittest.skipUnless(HAVE, "ffmpeg/ffprobe not installed")
    def test_word_times_follow_a_late_audio_start(self):  # finding 2: audio stream start_time > 0
        late = self.tmp / "late.mp4"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=64x64:rate=10:duration=2.5",
                        "-itsoffset", "0.8", "-f", "lavfi", "-i", "sine=frequency=440:duration=1.5", "-map", "0:v", "-map", "1:a",
                        "-c:v", "mpeg4", "-c:a", "aac", str(late)], check=True)
        probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=start_time",
                                           "-of", "json", str(late)], capture_output=True, text=True, check=True).stdout)
        start = float(probe["streams"][0]["start_time"])
        self.assertGreater(start, 0.5)
        self.assertAlmostEqual(M.media_timing(late)[1], start, places=6)
        f = self.fake_file("late.json", [{"text": "اللهم", "words": [{"word": "اللهم", "start": 0.0, "end": 0.5}]}])
        dst = self.tmp / "late" / "words.json"
        rc, out, err = self.cli(late, "--out", dst, fake=f)
        self.assertEqual(rc, 0, err)
        d = json.loads(dst.read_text(encoding="utf-8"))
        self.assertEqual(d["source"]["audio_offset"], round(start, 3))
        self.assertEqual((d["words"][0]["start"], d["words"][0]["end"]), (round(start, 3), round(start + 0.5, 3)))
        self.assertEqual(d["source"]["duration"], 2.5)
        if HAVE_NUMPY:  # the premise: decoded sample 0 is the first audio sample, not file time 0
            self.assertLess(len(M.decode_16k(late)) / 16000.0, 1.6)
        # intake --transcribe on the same file: master.wav is padded to the file timeline, so the cue map imports the words
        job = self.tmp / "late_job"
        rc, out, err = self.cli(late, "--job", job, "--transcribe", cmd="intake", fake=f)
        self.assertEqual(rc, 0, err)
        res = json.loads(out)
        self.assertEqual(res["audio_cues"]["aligned_words"], 1, res["audio_cues"])
        self.assertEqual(res["audio_cues"]["audio_offset"], round(start, 3))
        wav_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        str(job / "work" / "master.wav")], capture_output=True, text=True, check=True).stdout)
        self.assertGreater(wav_len, start + 1.4)
        rc, out, err = self.cli(late, "--job", job, "--transcribe", cmd="intake", fake=f)  # re-intake: no stale cues.json
        self.assertEqual(rc, 0, err)
        self.assertEqual(json.loads(out)["audio_cues"]["aligned_words"], 1)

    def test_tidy_words_keeps_segment_order(self):  # finding 3: overlapping phrase ranges / stale phrase text
        segs = [{"text": "a b", "words": [{"word": "a", "start": 0.0, "end": 0.5}, {"word": "b", "start": 1.0, "end": 1.4}]},
                {"text": "c d", "words": [{"word": "c", "start": 0.98, "end": 1.3}, {"word": "d", "start": 1.4, "end": 2.0}]}]
        words, phrases = M.tidy_words(segs)
        self.assertEqual([w["word"] for w in words], ["a", "b", "c", "d"])
        self.assertEqual([p["words"] for p in phrases], [[0, 1], [2, 3]])
        self.assertEqual([p["text"] for p in phrases], ["a b", "c d"])
        for a, b in zip(words, words[1:]):
            self.assertLessEqual(a["end"], b["start"])
            self.assertLess(a["start"], b["start"])
        for p0, p1 in zip(phrases, phrases[1:]):
            self.assertLessEqual(p0["end"], p1["start"])
        words, phrases = M.tidy_words([segs[1], segs[0]])  # segments listed out of order are put back in time order
        self.assertEqual([w["word"] for w in words], ["a", "b", "c", "d"])
        one = [{"text": "one two three", "words": [{"word": "one", "start": 0.0, "end": 0.4}, {"word": "two", "start": 0.5, "end": 0.9},
                                                   {"word": "three", "start": 1.2, "end": 1.5}]}]
        self.assertEqual(M.tidy_words(one, limit=1.0)[1], [{"text": "one two", "start": 0.0, "end": 0.9, "words": [0, 1]}])
        bad = [{"text": "x y", "words": [{"word": "x", "start": 0.0, "end": 0.4}, {"word": "y", "start": None, "end": 0.9}]}]
        self.assertEqual(M.tidy_words(bad)[1][0]["text"], "x")
        self.assertEqual(M.tidy_words(one, offset=0.5)[0][0], {"word": "one", "start": 0.5, "end": 0.9})

    @unittest.skipUnless(HAVE, "ffmpeg/ffprobe not installed")
    def test_intake_transcribe_accepts_force(self):  # finding 4: intake --transcribe had no --force
        job = self.tmp / "jobF"
        job.mkdir()
        (job / "words.json").write_text('[{"word": "يدوي", "start": 0.1, "end": 0.5}]\n', encoding="utf-8")
        rc, out, err = self.cli(self.media, "--job", job, "--transcribe", cmd="intake")
        self.assertEqual(rc, 2)
        self.assertIn("--force", err)
        rc, out, err = self.cli(self.media, "--job", job, "--transcribe", "--force", cmd="intake")
        self.assertEqual(rc, 0, err)
        self.assertEqual(json.loads((job / "words.json").read_text(encoding="utf-8"))["schema"], "kosif-words/1")
        self.assertEqual(json.loads(out)["audio_cues"]["aligned_words"], 6)

    @unittest.skipUnless(HAVE_GIT and (REPO / ".git").exists(), "git checkout needed")
    def test_target_guard_in_this_repository(self):  # finding 5: council condition "outputs under out/, never jobs/"
        for bad, why in ((REPO / "jobs" / "transcribe-guard-test" / "words.json", "inside jobs/"),
                         (REPO / "templates" / "words.example.json", "tracked by git"),
                         (REPO / "transcribe-guard-not-ignored" / "words.json", "not git-ignored"),
                         (SK / "out" / "words.json", "inside the skill folder")):  # git-ignored, still refused
            self.assertIn(why, M.target_problem(bad) or "", bad)
        self.assertIsNone(M.target_problem(REPO / "out" / "transcribe-guard" / "words.json"))
        self.assertIsNone(M.target_problem(self.tmp / "elsewhere" / "words.json"))
        job = REPO / "jobs" / "transcribe-guard-test"
        rc, out, err = self.cli(self.media, "--job", job)
        self.assertEqual(rc, 2)
        self.assertIn("inside jobs/", err)
        self.assertIn("--allow-tracked", err)
        self.assertFalse(job.exists())

    @unittest.skipUnless(HAVE_GIT, "git not installed")
    def test_target_guard_in_a_scratch_repository(self):  # finding 5: --job X --out Y must not rewrite a tracked X/report.json
        repo = self.tmp / "scratchrepo"
        for d in ("jobs/j", "data"):
            (repo / d).mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
        tracked = '{"intake": {"kind": "audio"}}\n'
        for d in ("jobs/j", "data"):
            (repo / d / "report.json").write_text(tracked, encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "jobs/j/report.json", "data/report.json", ".gitignore"], check=True)
        elsewhere = self.tmp / "elsewhere.json"
        for job, why in ((repo / "jobs" / "j", "inside jobs/"), (repo / "data", "tracked by git"), (repo / "loose", "not git-ignored")):
            rc, out, err = self.cli(self.media, "--job", job, "--out", elsewhere)
            self.assertEqual(rc, 2, job)
            self.assertIn(why, err)
            self.assertEqual(len(err.strip().splitlines()), 1)
        self.assertFalse(elsewhere.exists())
        self.assertEqual((repo / "data" / "report.json").read_text(encoding="utf-8"), tracked)
        self.assertFalse((repo / "loose").exists())
        rc, out, err = self.cli(self.media, "--job", repo / "jobs" / "new", "--transcribe", cmd="intake")  # refused before intake work
        self.assertEqual(rc, 2)
        self.assertFalse((repo / "jobs" / "new").exists())
        self.assertEqual(self.cli(self.media, "--job", repo / "out" / "j")[0], 0)  # git-ignored out/ is the place
        rc, out, err = self.cli(self.media, "--job", repo / "data", "--out", elsewhere, "--allow-tracked")
        self.assertEqual(rc, 0, err)
        self.assertIn("transcribe", json.loads((repo / "data" / "report.json").read_text(encoding="utf-8")))

    def test_broken_install_and_decode_timeout_exit_2(self):  # finding 7: OSError at import, ffmpeg timeout
        pkg = self.tmp / "brokenfw" / "faster_whisper"
        pkg.mkdir(parents=True)
        (pkg / "__init__.py").write_text('raise OSError("libctranslate2.so.4: cannot open shared object file")\n', encoding="utf-8")
        importlib.invalidate_caches()
        with mock.patch.dict(sys.modules), mock.patch.object(sys, "path", [str(pkg.parent)] + sys.path):
            for name in [m for m in sys.modules if m == "faster_whisper" or m.startswith("faster_whisper.")]:
                del sys.modules[name]
            rc, out, err = self.cli(self.media, "--out", self.tmp / "broken" / "words.json", fake=False)
        self.assertEqual(rc, 2)
        self.assertEqual(len(err.strip().splitlines()), 1)
        self.assertIn("cannot be imported: OSError", err)
        self.assertFalse((self.tmp / "broken" / "words.json").exists())
        with mock.patch.dict(sys.modules, {"numpy": types.ModuleType("numpy")}), \
                mock.patch.object(M.subprocess, "run", side_effect=subprocess.TimeoutExpired("ffmpeg", 5)):
            with self.assertRaises(M.TranscribeError) as cm:
                M.decode_16k(self.media, timeout=5)
        self.assertIn("timed out", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
