"""montage_pro transcribe: --no-vad / --no-recover plumbing, recovery of spans the no-speech filter dropped, and the
ffmpeg → PyAV decode fallback. Offline: the whisper model is a stub (no model download, no network); the decode
functions are mocked except one real PyAV decode of a stdlib-written WAV, skipped when PyAV or numpy is missing."""
import contextlib
import importlib.util
import io
import json
import math
import os
import shutil
import struct
import sys
import tempfile
import types
import unittest
import wave
from pathlib import Path
from unittest import mock

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import montage_pro as M  # noqa: E402
import audio_cue_mapper  # noqa: E402
import cinematic_cut_planner  # noqa: E402

HAVE_NUMPY = importlib.util.find_spec("numpy") is not None
HAVE_AV = importlib.util.find_spec("av") is not None


def W(word, s, e, p=0.9):
    return {"word": " " + word, "start": s, "end": e, "probability": p}


# first pass (decoded timeline): one kept line, two touching dropped verse segments, one dropped "subscribe" guess
KEPT = {"text": " قل إن الأمر كله لله", "start": 0.0, "end": 2.0, "no_speech_prob": 0.059, "avg_logprob": -0.343,
        "words": [W("قل", 0.0, 0.4), W("إن", 0.4, 0.8), W("الأمر", 0.8, 1.3), W("كله", 1.3, 1.6), W("لله", 1.6, 2.0)]}
DROP_B = {"text": " يقولون لو كان لنا من الأمر شيء", "start": 2.0, "end": 6.0, "no_speech_prob": 0.94, "avg_logprob": -0.151,
          "words": [W("يقولون", 2.0, 2.7), W("شيء", 4.9, 6.0)]}
DROP_C = {"text": " ما قتلنا ها هنا", "start": 6.0, "end": 8.0, "no_speech_prob": 0.94, "avg_logprob": -0.151,
          "words": [W("ما", 6.0, 6.5)]}
DROP_D = {"text": " اشتركوا في القناة", "start": 10.0, "end": 12.0, "no_speech_prob": 0.95, "avg_logprob": -0.618,
          "words": [W("اشتركوا", 10.2, 10.9), W("في", 10.9, 11.1), W("القناة", 11.1, 11.9)]}
# the no-VAD re-run (decoded timeline; the fake hook and the stub hand them back timed from the window start)
R1 = {"text": " لله يقولون لو كان لنا من الأمر شيء", "start": 1.75, "end": 5.9, "no_speech_prob": 0.511,
      "avg_logprob": -0.155, "compression_ratio": 1.51,
      "words": [W("لله", 1.75, 1.95), W("-", 1.95, 2.1, 0.032), W("يقولون", 2.1, 2.7, 0.97), W("لو", 2.7, 3.0), W("كان", 3.0, 3.4),
                W("لنا", 3.4, 3.9), W("من", 3.9, 4.2), W("الأمر", 4.2, 4.9), W("شيء", 4.9, 5.9)]}
# "لله" repeats a kept word (never doubled); "-" is what medium left of a verse number on the real recitation (dropped)
R2 = {"text": " ما قتلنا ها هنا", "start": 6.1, "end": 7.9, "no_speech_prob": 0.838, "avg_logprob": -0.223, "compression_ratio": 1.43,
      "words": [W("ما", 6.1, 6.5), W("قتلنا", 6.5, 7.1), W("ها", 7.1, 7.4), W("هنا", 7.4, 7.9)]}
R3 = {"text": " هنا", "start": 8.02, "end": 8.25, "no_speech_prob": 0.5, "avg_logprob": -0.3,
      "words": [W("هنا", 8.02, 8.25)]}  # inside the 0.3 s context pad only, not inside a dropped span
R5 = {"text": " اشتركوا في القناة", "start": 10.2, "end": 11.9, "no_speech_prob": 0.945, "avg_logprob": -0.618,
      "compression_ratio": 0.74, "words": DROP_D["words"]}  # what medium really wrote over pink noise and digital silence
R6 = {"text": " همهمة", "start": 11.0, "end": 11.5, "no_speech_prob": 0.9, "avg_logprob": -1.4, "words": [W("همهمة", 11.0, 11.5)]}
R7 = {"text": " لا لا لا لا لا لا", "start": 10.0, "end": 10.9, "no_speech_prob": 0.9, "avg_logprob": -0.3, "compression_ratio": 3.1,
      "words": [W("لا", 10.0 + i * 0.15, 10.15 + i * 0.15) for i in range(6)]}
KEPT_WORDS = ["قل", "إن", "الأمر", "كله", "لله"]
BACK = ["يقولون", "لو", "كان", "لنا", "من", "الأمر", "شيء", "ما", "قتلنا", "ها", "هنا"]


def ns(seg):  # faster-whisper yields objects with attributes
    return types.SimpleNamespace(**{**seg, "words": [types.SimpleNamespace(**w) for w in seg["words"]]})


def relative(seg, a):  # what the model returns for samples a..b: times from the chunk start
    return ns(M._shifted(seg, -a))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.media = self.tmp / "verse.m4a"
        self.media.write_bytes(b"not decoded: load_audio is mocked")

    def cli(self, *args, fake=None, cmd="transcribe"):
        env = {k: v for k, v in os.environ.items() if k != M.FAKE_ENV}
        if fake is not None:
            f = self.tmp / "fake.json"
            f.write_text(json.dumps(fake, ensure_ascii=False), encoding="utf-8")
            env[M.FAKE_ENV] = str(f)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, env, clear=True), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                rc = M.main([cmd, *map(str, args)])
            except SystemExit as exc:
                rc = exc.code
        return rc, out.getvalue(), err.getvalue()

    def read(self, p):
        return json.loads(Path(p).read_text(encoding="utf-8"))


class RecoveryMergeTests(Base):
    """The merge itself, through the KOSIF_TRANSCRIBE_FAKE hook ("recover" = what a no-VAD re-run returns)."""
    FAKE = {"language": "ar", "segments": [KEPT, DROP_B, DROP_C, DROP_D], "recover": [R1, R2, R3, R5, R6, R7]}

    def run_fake(self, offset=0.0, *extra):
        dst = self.tmp / "out" / "words.json"
        with mock.patch.object(M, "media_timing", return_value=(14.0 + offset, offset)):
            rc, out, err = self.cli(self.media, "--out", dst, *extra, fake=self.FAKE)
        self.assertEqual(rc, 0, err)
        return json.loads(out), self.read(dst), dst

    def test_recovered_words_are_merged_in_order_and_marked(self):
        line, d, dst = self.run_fake()
        self.assertEqual([w["word"] for w in d["words"]], KEPT_WORDS + BACK)
        self.assertEqual([bool(w.get("recovered")) for w in d["words"]], [False] * 5 + [True] * 11)
        self.assertEqual([(w["start"], w["end"]) for w in d["words"][5:8]], [(2.1, 2.7), (2.7, 3.0), (3.0, 3.4)])
        for a, b in zip(d["words"], d["words"][1:]):
            self.assertLess(a["start"], b["start"])
            self.assertLessEqual(a["end"], b["start"])
        self.assertEqual(d["phrases"][0], {"text": "قل إن الأمر كله لله", "start": 0.0, "end": 2.0, "words": [0, 4],
                                           "no_speech_prob": 0.059, "avg_logprob": -0.343})  # first-pass phrase unchanged
        self.assertEqual(d["phrases"][1], {"text": "يقولون لو كان لنا من الأمر شيء", "start": 2.1, "end": 5.9, "words": [5, 11],
                                           "no_speech_prob": 0.511, "avg_logprob": -0.155, "recovered": True})
        self.assertEqual(d["phrases"][2], {"text": "ما قتلنا ها هنا", "start": 6.1, "end": 7.9, "words": [12, 15],
                                           "no_speech_prob": 0.838, "avg_logprob": -0.223, "recovered": True})
        self.assertEqual(len(d["phrases"]), 3)
        # dropped_segments keeps every first-pass drop (old readers see the same list) and marks the recovered ones
        self.assertEqual([(x["text"], x["start"], x["end"], x["no_speech_prob"], x.get("recovered")) for x in d["dropped_segments"]],
                         [("يقولون لو كان لنا من الأمر شيء", 2.0, 6.0, 0.94, True), ("ما قتلنا ها هنا", 6.0, 8.0, 0.94, True),
                          ("اشتركوا في القناة", 10.0, 12.0, 0.95, None)])
        win = d["recovery"]["windows"]
        self.assertEqual([(x["start"], x["end"], x["segments"], x["recovered_words"]) for x in win], [(2.0, 8.0, 3, 11), (10.0, 12.0, 3, 0)])
        self.assertNotIn("rejected", win[0])  # R3 (pad only) and R1's repeated "لله" are trimmed, not rejected
        self.assertEqual([r["why"] for r in win[1]["rejected"]],
                         ["outro", "avg_logprob -1.400 < -1", "compression_ratio 3.10 > 2.4"])
        self.assertEqual((d["recovery"]["min_avg_logprob"], d["recovery"]["max_compression_ratio"], d["recovery"]["min_level_dbfs"]),
                         (-1.0, 2.4, -50.0))
        self.assertEqual((d["engine"]["recover_dropped"], d["engine"]["condition_on_previous_text"], d["engine"]["vad_filter"]),
                         (True, True, True))
        self.assertEqual((line["words"], line["dropped_segments"], line["recovered_segments"], line["recovered_words"]), (16, 3, 2, 11))
        self.assertIn("no_speech_prob", line["warning"])  # the old warning stays, the recovery note follows it
        self.assertIn("recovered 11 word(s) in 2 phrase(s)", line["warning"])
        # the readers that take words.json accept the merged file
        cinematic_cut_planner.validate_words(d["words"], d["source"]["duration"])
        self.assertEqual(len(audio_cue_mapper.import_aligned_words(dst, d["source"]["duration"])), 16)

    def test_times_follow_the_audio_offset(self):
        line, d, _ = self.run_fake(0.776)
        self.assertEqual((d["words"][5]["word"], d["words"][5]["start"]), ("يقولون", round(2.1 + 0.776, 3)))
        self.assertEqual(d["dropped_segments"][0]["start"], round(2.0 + 0.776, 3))
        self.assertEqual(d["recovery"]["windows"][0]["start"], round(2.0 + 0.776, 3))
        self.assertEqual(len(d["words"]), 16)

    def test_no_vad_re_checks_the_first_pass_drops(self):  # the 24-10 case: --no-vad still dropped 15 sung lines
        line, d, _ = self.run_fake(0.0, "--no-vad")
        self.assertEqual([w["word"] for w in d["words"]], KEPT_WORDS + ["يقولون", "شيء", "ما"])  # the hook's "recover" is unused
        self.assertEqual([x.get("recovered") for x in d["dropped_segments"]], [True, True, None])
        self.assertEqual([r["why"] for r in d["recovery"]["windows"][1]["rejected"]], ["outro"])
        self.assertEqual((d["engine"]["vad_filter"], d["engine"]["condition_on_previous_text"]), (False, False))

    def test_no_recover_keeps_the_old_output(self):
        line, d, _ = self.run_fake(0.0, "--no-recover")
        self.assertEqual([w["word"] for w in d["words"]], KEPT_WORDS)
        self.assertNotIn("recovery", d)
        self.assertNotIn("recovered_words", line)
        self.assertFalse(any("recovered" in x for x in d["dropped_segments"]))
        self.assertIs(d["engine"]["recover_dropped"], False)

    def test_an_old_file_with_drops_is_up_to_date_under_no_recover(self):
        _, d, dst = self.run_fake(0.0, "--no-recover")
        for k in ("recover_dropped", "condition_on_previous_text", "decoder"):  # what transcribe wrote before them
            d["engine"].pop(k, None)
        self.assertTrue(d["dropped_segments"])
        dst.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        with mock.patch.object(M, "media_timing", side_effect=AssertionError("the model must not run again")):
            rc, out, err = self.cli(self.media, "--out", dst, "--no-recover", fake=self.FAKE)
        self.assertEqual((rc, json.loads(out)["status"]), (0, "up to date"), err)  # --no-recover = the old output
        self.assertEqual(self.read(dst), d)
        line, d2, _ = self.run_fake()  # with recovery on, the dropped spans can change the result: redone
        self.assertEqual(line["status"], "written")
        self.assertIs(d2["engine"]["recover_dropped"], True)

    def test_nothing_dropped_means_nothing_re_run(self):
        dst = self.tmp / "clean" / "words.json"
        rc, out, err = self.cli(self.media, "--out", dst, fake={"language": "ar", "segments": [KEPT], "recover": [R1]})
        self.assertEqual(rc, 0, err)
        d = self.read(dst)
        self.assertNotIn("recovery", d)
        self.assertNotIn("dropped_segments", d)
        self.assertNotIn("warning", json.loads(out))

    def test_recover_dropped_windows_limits_and_failures(self):
        seen = []

        def rerun(a, b):
            seen.append((round(a, 3), round(b, 3)))
            return []
        # touching spans form one window; a 0.5 s gap starts another; the last window is clipped to the audio end
        _, rec = M.recover_dropped([(2.0, 6.0), (6.0, 8.0), (8.5, 9.9)], [], rerun, None, limit=10.0)
        self.assertEqual(seen, [(1.7, 8.3), (8.2, 10.0)])
        self.assertEqual([(r["start"], r["end"], r["segments"], r["recovered_words"]) for r in rec], [(2.0, 8.0, 0, 0), (8.5, 9.9, 0, 0)])

        def boom(a, b):
            raise RuntimeError("CUDA out of memory\nsecond line")
        found, rec = M.recover_dropped([(2.0, 6.0)], [], boom)
        self.assertEqual(found, [])
        self.assertEqual(rec[0]["skipped"], "re-run failed: RuntimeError: CUDA out of memory")
        # a word the first pass already kept (overlapping segments) is never written twice
        kept = [{"text": "x", "words": [{"word": "x", "start": 3.0, "end": 3.5}]}]
        again = {"text": " x y", "avg_logprob": -0.2, "words": [W("x", 3.1, 3.4), W("y", 4.0, 4.5)]}
        found, rec = M.recover_dropped([(2.0, 6.0)], kept, lambda a, b: [M._shifted(again, -a)])
        self.assertEqual([(w["word"].strip(), round(w["start"], 3)) for g in found for w in g["words"]], [("y", 4.0)])
        self.assertEqual((found[0]["text"], found[0]["recovered"]), ("y", True))
        # a recovered word that starts or ends inside a kept word is trimmed to it, so the kept word keeps its length
        edge = {"text": " a b", "avg_logprob": -0.2, "words": [W("a", 3.3, 4.1), W("b", 4.5, 5.2)]}
        kept2 = kept + [{"text": "z", "words": [{"word": "z", "start": 5.0, "end": 5.6}]}]
        found, _ = M.recover_dropped([(2.0, 6.0)], kept2, lambda a, b: [M._shifted(edge, -a)])
        self.assertEqual([(round(w["start"], 3), round(w["end"], 3)) for w in found[0]["words"]], [(3.5, 4.1), (4.5, 5.0)])


@unittest.skipUnless(HAVE_NUMPY, "numpy not installed")
class EnginePlumbingTests(Base):
    """CLI flags → WhisperModel.transcribe keyword arguments, with a stub model and a synthetic numpy signal."""

    def setUp(self):
        super().setUp()
        import numpy as np
        t = np.arange(14 * M.SR, dtype=np.float32) / M.SR
        self.audio = (0.3 * np.sin(2 * math.pi * 220 * t)).astype(np.float32)
        self.audio[10 * M.SR:12 * M.SR] = 0.0  # digital silence under the "subscribe" guess: that span is never re-run
        self.calls = []
        self.fail_rerun = False
        test = self

        class Model:
            def __init__(self, *a, **k):
                pass

            def transcribe(self, audio, **kw):
                test.calls.append((audio, kw))
                info = types.SimpleNamespace(language="ar")
                if len(audio) == len(test.audio):  # the first pass over the whole file
                    return iter([ns(KEPT), ns(DROP_B), ns(DROP_C), ns(DROP_D)]), info
                if test.fail_rerun:
                    raise RuntimeError("re-run exploded")
                return iter([relative(R1, 1.7), relative(R2, 1.7), relative(R3, 1.7)]), info  # the 2.0-8.0 s window
        self.stub = types.ModuleType("faster_whisper")
        self.stub.WhisperModel = Model
        self.patches = [mock.patch.dict(sys.modules, {"faster_whisper": self.stub}),
                        mock.patch.object(M, "_fw_version", return_value="1.2.1"),
                        mock.patch.object(M, "load_audio", side_effect=lambda media, timeout=3600: (self.audio, "ffmpeg")),
                        mock.patch.object(M, "media_timing", return_value=(14.0, 0.0))]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def test_default_pass_then_one_no_vad_re_run_of_the_loud_window(self):
        import numpy as np
        dst = self.tmp / "d" / "words.json"
        rc, out, err = self.cli(self.media, "--out", dst)
        self.assertEqual(rc, 0, err)
        self.assertEqual(len(self.calls), 2)  # the silent 10-12 s span is not re-run
        (a0, k0), (a1, k1) = self.calls
        for a in (a0, a1):
            self.assertIsInstance(a, np.ndarray)  # the model never gets a path (PyAV metadata_errors TypeError)
        self.assertEqual(len(a0), 14 * M.SR)
        self.assertEqual((k0["vad_filter"], k0["condition_on_previous_text"], k0["language"], k0["word_timestamps"], k0["beam_size"]),
                         (True, True, "ar", True, 5))
        self.assertEqual(len(a1), int(6.6 * M.SR))  # 2.0-8.0 s with 0.3 s of context each side
        self.assertEqual((k1["vad_filter"], k1["condition_on_previous_text"], k1["language"], k1["word_timestamps"]),
                         (False, False, "ar", True))
        d, line = self.read(dst), json.loads(out)
        self.assertEqual([w["word"] for w in d["words"]], KEPT_WORDS + BACK)
        self.assertEqual(d["words"][5]["start"], 2.1)
        win = d["recovery"]["windows"]
        self.assertGreater(win[0]["level_dbfs"], -20)
        self.assertEqual((win[1]["level_dbfs"], win[1]["skipped"]), (-120.0, "silent (below -50 dBFS)"))
        self.assertEqual((d["engine"]["decoder"], line["decoder"], line["condition_on_previous_text"]), ("ffmpeg", "ffmpeg", True))
        # loud stretches with no word at all (what VAD cuts from a song) are measured and reported, never re-run
        self.assertEqual([(g["start"], g["end"]) for g in d["vad_gaps"]], [(8.0, 10.0), (12.0, 14.0)])
        self.assertGreater(min(g["level_dbfs"] for g in d["vad_gaps"]), -20)
        self.assertEqual(line["vad_gaps"], 2)
        self.assertIn("4.0 s, have no words", line["warning"])
        self.assertIn("try --no-vad", line["warning"])
        self.assertEqual(json.loads(self.cli(self.media, "--out", dst)[1])["status"], "up to date")
        self.assertEqual(len(self.calls), 2)

    def test_loud_gaps_measures_only_long_loud_holes(self):
        cover = [(0.0, 2.0), (2.0, 8.0), (9.0, 9.5), (10.0, 12.0)]
        self.assertEqual([(a, b) for a, b, _ in M.loud_gaps(self.audio, cover, 14.0)], [(12.0, 14.0)])  # 8-9 and 9.5-10 are short
        # the level is the RMS of the whole hole: 9.9-14 s holds the 10-12 s silence but is loud on average (about -16 dBFS)
        (a, b, lv), = M.loud_gaps(self.audio, [(0.0, 9.9)], 14.0)
        self.assertEqual((a, b), (9.9, 14.0))
        self.assertLess(abs(lv - 20 * math.log10(0.3 / math.sqrt(2) * math.sqrt(2.1 / 4.1))), 0.2)
        self.assertEqual(M.loud_gaps(self.audio, [(0.0, 10.0)], 12.0), [])  # digital silence is not a gap
        self.assertEqual(M.loud_gaps(None, [], 14.0), [])

    def test_no_vad_decodes_once_without_conditioning(self):
        dst = self.tmp / "nv" / "words.json"
        rc, out, err = self.cli(self.media, "--out", dst, "--no-vad")
        self.assertEqual(rc, 0, err)
        self.assertEqual(len(self.calls), 1)  # the first pass already is the no-VAD decode: its drops are re-checked, not re-run
        self.assertEqual((self.calls[0][1]["vad_filter"], self.calls[0][1]["condition_on_previous_text"]), (False, False))
        d, line = self.read(dst), json.loads(out)
        self.assertEqual((d["engine"]["vad_filter"], d["engine"]["condition_on_previous_text"], d["engine"]["recover_dropped"]),
                         (False, False, True))
        self.assertTrue(d["recovery"]["method"].startswith("first pass already without VAD"))
        self.assertEqual([w["word"] for w in d["words"] if w.get("recovered")], ["يقولون", "شيء", "ما"])
        self.assertEqual(d["recovery"]["windows"][1]["skipped"], "silent (below -50 dBFS)")
        self.assertIs(line["condition_on_previous_text"], False)
        self.assertIn("by re-checking 2 span(s)", line["warning"])
        rc, out, err = self.cli(self.media, "--out", dst, "--no-vad", "--no-recover")
        d = self.read(dst)
        self.assertEqual(([w["word"] for w in d["words"]], d["engine"]["recover_dropped"]), (KEPT_WORDS, False))
        self.assertNotIn("recovery", d)

    def test_no_recover_and_auto_language(self):
        rc, out, err = self.cli(self.media, "--out", self.tmp / "nr" / "words.json", "--no-recover")
        self.assertEqual((rc, len(self.calls), self.calls[0][1]["vad_filter"]), (0, 1, True), err)
        rc, out, err = self.cli(self.media, "--out", self.tmp / "auto" / "words.json", "--language", "auto")
        self.assertEqual(rc, 0, err)
        self.assertIsNone(self.calls[1][1]["language"])
        self.assertEqual(self.calls[2][1]["language"], "ar")  # the re-run keeps the detected language (no re-detection)

    def test_failed_re_run_keeps_the_first_pass(self):
        self.fail_rerun = True
        dst = self.tmp / "f" / "words.json"
        rc, out, err = self.cli(self.media, "--out", dst)
        self.assertEqual(rc, 0, err)
        d = self.read(dst)
        self.assertEqual([w["word"] for w in d["words"]], KEPT_WORDS)
        self.assertEqual(d["recovery"]["windows"][0]["skipped"], "re-run failed: RuntimeError: re-run exploded")
        self.assertIn("no words recovered from 2 dropped span(s)", json.loads(out)["warning"])

    def test_files_from_before_the_new_engine_fields(self):
        dst = self.tmp / "old" / "words.json"

        def make_old(*drop):  # what the previous transcribe wrote: none of the new engine fields
            d = self.read(dst)
            for k in ("condition_on_previous_text", "recover_dropped", "decoder"):
                d["engine"].pop(k, None)
            for k in ("recovery",) + drop:
                d.pop(k, None)
            dst.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(self.cli(self.media, "--out", dst, "--no-recover")[0], 0)
        make_old()  # it dropped segments: recovery can change the result, so it is redone
        self.assertEqual(json.loads(self.cli(self.media, "--out", dst)[1])["status"], "written")
        make_old("dropped_segments")  # it dropped nothing: recovery changes nothing, still up to date
        n = len(self.calls)
        self.assertEqual(json.loads(self.cli(self.media, "--out", dst)[1])["status"], "up to date")
        self.assertEqual(len(self.calls), n)
        self.assertEqual(self.cli(self.media, "--out", dst, "--no-vad")[0], 0)
        make_old("dropped_segments")  # an old --no-vad file was decoded with the previous text: not today's --no-vad
        self.assertEqual(json.loads(self.cli(self.media, "--out", dst, "--no-vad")[1])["status"], "written")

    def test_intake_and_job_pass_the_flags_through(self):
        seen = {}

        def fake_intake(media, job, topts=None):
            seen.update(topts or {})
            return {"kind": "audio", "transcribe": {"ok": True}}
        with mock.patch.object(M, "intake", side_effect=fake_intake):
            rc, out, err = self.cli(self.media, "--job", self.tmp / "j", "--transcribe", "--no-recover", "--no-vad", cmd="intake")
        self.assertEqual(rc, 0, err)
        self.assertEqual((seen["recover"], seen["vad"]), (False, False))
        rc, out, err = self.cli(self.media, "--job", self.tmp / "job")
        self.assertEqual(rc, 0, err)
        rep = self.read(self.tmp / "job" / "report.json")["transcribe"]
        self.assertEqual((rep["recovered_words"], rep["decoder"]), (11, "ffmpeg"))


class DecodeFallbackTests(Base):
    """load_audio: the ffmpeg pipe first, PyAV (without metadata_errors) when ffmpeg is missing or fails."""
    SAMPLES = [0.0] * 160

    def test_no_ffmpeg_uses_pyav(self):
        with mock.patch.object(M.shutil, "which", return_value=None), \
                mock.patch.object(M, "decode_16k", side_effect=AssertionError("ffmpeg must not run")), \
                mock.patch.object(M, "decode_pyav", return_value=self.SAMPLES) as pyav:
            self.assertEqual(M.load_audio(self.media), (self.SAMPLES, "pyav"))
        pyav.assert_called_once_with(self.media)

    def test_ffmpeg_failure_falls_back_to_pyav(self):
        with mock.patch.object(M.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                mock.patch.object(M, "decode_16k", side_effect=M.TranscribeError("cannot decode verse.m4a: Invalid data")), \
                mock.patch.object(M, "decode_pyav", return_value=self.SAMPLES):
            self.assertEqual(M.load_audio(self.media)[1], "pyav")
        with mock.patch.object(M.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                mock.patch.object(M, "decode_16k", return_value=self.SAMPLES), \
                mock.patch.object(M, "decode_pyav", side_effect=AssertionError("PyAV must not run")):
            self.assertEqual(M.load_audio(self.media), (self.SAMPLES, "ffmpeg"))

    def test_both_fail_one_line_naming_each(self):
        bad = TypeError("open() got an unexpected keyword argument 'metadata_errors'\nTraceback line")
        with mock.patch.object(M.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                mock.patch.object(M, "decode_16k", side_effect=M.TranscribeError("cannot decode verse.m4a: Invalid data")), \
                mock.patch.object(M, "decode_pyav", side_effect=bad):
            with self.assertRaises(M.TranscribeError) as cm:
                M.load_audio(self.media)
        msg = str(cm.exception)
        self.assertEqual(len(msg.splitlines()), 1)
        self.assertIn("cannot decode verse.m4a", msg)
        self.assertIn("PyAV fallback: TypeError: open() got an unexpected keyword argument 'metadata_errors'", msg)

    def test_timeout_is_not_retried_and_missing_av_is_named(self):
        with mock.patch.object(M.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                mock.patch.object(M, "decode_16k", side_effect=M.DecodeStop("decoding verse.m4a timed out after 5 s")), \
                mock.patch.object(M, "decode_pyav") as pyav:
            with self.assertRaises(M.TranscribeError):
                M.load_audio(self.media, timeout=5)
        pyav.assert_not_called()
        # a file whose name says "numpy" or "timed out" is still retried: only DecodeStop stops the fallback
        with mock.patch.object(M.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                mock.patch.object(M, "decode_16k", side_effect=M.TranscribeError("cannot decode numpy timed out.m4a: bad")), \
                mock.patch.object(M, "decode_pyav", return_value=self.SAMPLES):
            self.assertEqual(M.load_audio(self.media)[1], "pyav")
        if HAVE_NUMPY:  # the real decode_16k raises DecodeStop on its own timeout
            with mock.patch.object(M.subprocess, "run", side_effect=M.subprocess.TimeoutExpired("ffmpeg", 5)):
                with self.assertRaises(M.DecodeStop):
                    M.decode_16k(self.media, timeout=5)
        with mock.patch.object(M.shutil, "which", return_value=None), mock.patch.dict(sys.modules, {"av": None}):
            with self.assertRaises(M.TranscribeError) as cm:
                M.load_audio(self.media)
        self.assertIn("ffmpeg not found", str(cm.exception))
        self.assertIn("is not installed", str(cm.exception))

    @unittest.skipUnless(HAVE_NUMPY, "numpy not installed")
    def test_transcribe_without_ffmpeg_records_the_pyav_decoder(self):
        import numpy as np
        calls = []

        class Model:
            def __init__(self, *a, **k):
                pass

            def transcribe(self, audio, **kw):
                calls.append(type(audio))
                return iter([ns(KEPT)]), types.SimpleNamespace(language="ar")
        stub = types.ModuleType("faster_whisper")
        stub.WhisperModel = Model
        dst = self.tmp / "pyav" / "words.json"
        with mock.patch.dict(sys.modules, {"faster_whisper": stub}), mock.patch.object(M.shutil, "which", return_value=None), \
                mock.patch.object(M, "decode_pyav", return_value=np.zeros(3 * M.SR, dtype=np.float32)):
            rc, out, err = self.cli(self.media, "--out", dst)
        self.assertEqual(rc, 0, err)
        self.assertEqual(calls, [np.ndarray])
        line, d = json.loads(out), self.read(dst)
        self.assertEqual((line["decoder"], d["engine"]["decoder"], d["source"]["duration"]), ("pyav", "pyav", 3.0))

    @unittest.skipUnless(HAVE_NUMPY and HAVE_AV, "PyAV or numpy not installed")
    def test_real_pyav_decode_of_a_stdlib_wav(self):  # the av 19 path faster-whisper 1.2.1's decode_audio cannot open
        wav = self.tmp / "tone.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(44100)
            w.writeframes(b"".join(struct.pack("<hh", v, v) for v in
                                   (int(9000 * math.sin(2 * math.pi * 330 * i / 44100)) for i in range(44100))))
        x = M.decode_pyav(wav)
        self.assertEqual((str(x.dtype), x.ndim), ("float32", 1))
        self.assertLess(abs(len(x) - M.SR), M.SR // 50)  # 1 s at 16 kHz (resampler edges aside)
        self.assertGreater(M.level_dbfs(x, 0.1, 0.9), -20)
        self.assertLessEqual(float(abs(x).max()), 1.0)


if __name__ == "__main__":
    unittest.main()
