"""quran_text.py, fully offline. Covers references and Arabic matching keys, and fetch against answers shaped like
alquran.cloud (captured once, served by a fake opener: cache, delay, retries, 404, wrong verse, refused translation).
It also covers pauses on synthetic numpy audio (the auto threshold for reverberant, wasl and deep-breath recordings,
and the voice end before a reverb tail), and the alignment of canonical words to recognised words: merges, splits,
misses, mis-hearings, spelled-out opening letters and speech outside the verses, with and without audio pauses,
plus empty voiced stretches, late starts after a breath and the dip refinement of long words.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p test_quran_text.py -v

The whisper times in AN_NAJM and DHARIYAT_VAD are the real faster-whisper output of the two reels made by hand on
2026-10-29 (the second one dropped half the words and wrote «يقول» for «أنكم تنطقون»). The audio is synthetic.
"""
from __future__ import annotations

import http.client
import io
import json
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import wave
from pathlib import Path
from unittest import mock

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "quran_text.py"
sys.path.insert(0, str(SK / "scripts"))
import quran_text as Q  # noqa: E402

FIX = json.loads((SK / "evals" / "fixtures" / "quran_text" / "alquran_cloud.json").read_text(encoding="utf-8"))["answers"]
URL = "https://api.alquran.cloud/v1/ayah/{}/{}"
try:
    import numpy as np
except ImportError:   # pauses and audio alignment tests skip
    np = None

AN_NAJM = [("وأن", 0.0, 0.36), ("ليس", 0.36, 1.32), ("للإنسان", 1.32, 3.54), ("إلا", 3.54, 4.26), ("ما", 4.26, 4.82),
           ("سعى", 4.82, 5.68), ("وأن", 5.68, 7.24), ("سعيه", 7.24, 9.08), ("سوف", 9.08, 10.22), ("يرى", 10.22, 11.14),
           ("ثم", 11.14, 12.44), ("يجزاه", 12.44, 14.14), ("الجزاء", 14.14, 16.32), ("الأوفى", 16.32, 17.72)]
DHARIYAT_VAD = [("وفي", 0.0, 0.32), ("السماء", 0.32, 1.96), ("وما", 4.97, 5.75), ("حق", 22.16, 23.32),
                ("مثل", 23.32, 26.0), ("ما", 26.0, 26.4), ("يقول", 26.4, 27.46)]
# The same recitation without VAD: every word heard, but «فورب» at 14.6 s although the voice says it from 12.5 s.
DHARIYAT_NOVAD = [("وفي", 0.0, 0.32), ("السماء", 0.32, 2.38), ("رزقكم", 2.38, 4.68), ("وما", 4.68, 5.64),
                  ("توعدون", 5.64, 9.16), ("فورب", 14.6, 16.0), ("السماء", 16.0, 17.4), ("والأرض", 17.4, 19.44),
                  ("إنه", 19.44, 21.4), ("لحق", 21.4, 23.24), ("مثل", 23.24, 25.94), ("ما", 25.94, 26.34),
                  ("أنكم", 26.34, 30.08), ("ترطقون", 30.08, 33.66)]
ISTIADHA = [("أعوذ", 0.0, 0.6), ("بالله", 0.6, 1.2), ("من", 1.2, 1.5), ("الشيطان", 1.5, 2.3), ("الرجيم", 2.3, 3.0)]


def R(rows):
    return [{"text": t, "key": Q.norm_ar(t), "start": float(s), "end": float(e)} for t, s, e in rows]


def words_doc(rows):
    return {"schema": "kosif-words/1", "source": {"file": "audio.m4a", "duration": 18.2},
            "engine": {"name": "faster-whisper", "model": "large-v3", "vad_filter": True},
            "words": [{"word": t, "start": s, "end": e, "prob": 0.9} for t, s, e in rows]}


class FakeResp:
    def __init__(self, body: bytes):
        self.body, self.status = body, 200

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(url, code, body, headers=None):
    return urllib.error.HTTPError(url, code, "error", headers or {}, io.BytesIO(json.dumps(body).encode("utf-8")))


class FakeNet:
    """Serves the captured answers by URL, after any scripted failures; records URL, timeout and User-Agent."""

    def __init__(self, script=None, answers=None):
        self.script, self.calls, self.answers = list(script or []), [], answers if answers is not None else FIX

    def __call__(self, req, timeout=None):
        url = req.full_url
        self.calls.append((url, timeout, req.get_header("User-agent")))
        if self.script:
            item = self.script.pop(0)
            if isinstance(item, Exception):
                raise item
            code, body, headers = item
            raise http_error(url, code, body, headers)
        ans = self.answers.get(url)
        if ans is None:
            raise AssertionError(f"unexpected URL {url}")
        if ans["status"] != 200:
            raise http_error(url, ans["status"], ans["body"])
        return FakeResp(json.dumps(ans["body"], ensure_ascii=False).encode("utf-8"))


class Clock:
    def __init__(self):
        self.t, self.sleeps = 100.0, []

    def clock(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(round(s, 6))
        self.t += s


def fetcher(cache, net=None, clock=None, **kw):
    clock = clock or Clock()
    return Q.Fetcher(cache, opener=net or FakeNet(), sleep=clock.sleep, clock=clock.clock,
                     now=lambda: "2026-10-29T07:00:00Z", **kw)


def canonical(tmp: Path, refs: str, edition="quran-simple"):
    doc = Q.fetch_verses(Q.parse_refs([refs])[0], edition, None, fetcher(tmp / "cache"))
    Q.write_json(tmp / "verses.json", doc)
    return Q.load_canonical(tmp / "verses.json")[1]


def synth(voiced, total, sr=16000, seed=7, floor=None):
    """Noise 'voice' at about -12 dBFS inside the voiced intervals; digital near-silence (or `floor` dB below the
    voice) elsewhere."""
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(int(round(total * sr))).astype(np.float32) * 0.25
    gain = np.full(len(x), 4e-4 if floor is None else 10 ** (floor / 20.0), dtype=np.float32)
    for a, b in voiced:
        gain[int(round(a * sr)):int(round(b * sr))] = 1.0
    return x * gain, sr


def shaped(total, level_db, sr=16000, seed=5):
    """Noise whose 50 ms level follows level_db(t) (dB under full scale of the 'voice'), for dips and decays."""
    rng = np.random.default_rng(seed)
    t = np.arange(int(round(total * sr))) / sr
    return (rng.standard_normal(len(t)) * 0.25 * 10 ** (level_db(t) / 20.0)).astype(np.float32), sr


def gaps_of(rep):
    return [(p["start"], p["end"]) for p in rep["pauses"] if p["kind"] == "gap"]


def pauses_doc(gaps, speech, voice_end=None):
    doc = {"schema": Q.SCHEMA_PAUSES, "speech": list(speech),
           "pauses": [{"start": a, "end": b, "dur": round(b - a, 3), "kind": "gap"} for a, b in gaps]}
    if voice_end is not None:
        doc["voice_end"] = voice_end
    return doc


def write_wav(path: Path, x, sr, channels=1):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    if channels == 2:
        pcm = np.repeat(pcm, 2)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


NAJM_VOICED = [(0.05, 5.95), (6.82, 11.15), (11.94, 17.30), (17.40, 17.95)]   # breaths, an in-word dip, then a tail
NAJM_TOTAL = 18.45


def run(*args, cwd=SK):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", timeout=120)


class RefsAndText(unittest.TestCase):
    def test_ayah_table(self):
        self.assertEqual(len(Q.AYAH_COUNTS), 114)
        self.assertEqual(sum(Q.AYAH_COUNTS), 6236)
        self.assertEqual((Q.AYAH_COUNTS[50], Q.AYAH_COUNTS[52], Q.AYAH_COUNTS[1]), (60, 62, 286))

    def test_parse_refs(self):
        self.assertEqual(Q.parse_refs(["51:22-23", "53:39"]), ([(51, 22), (51, 23), (53, 39)], ["51:22-23", "53:39"]))
        self.assertEqual(Q.parse_refs(["٥٣:٣٩-٤١"])[0], [(53, 39), (53, 40), (53, 41)])
        self.assertEqual(Q.parse_refs(["53:39-40", "53:40"])[0], [(53, 39), (53, 40)])
        self.assertEqual(Q.parse_refs(["51:22,51:23"])[0], [(51, 22), (51, 23)])
        for bad in ("115:1", "51:61", "51:23-22", "abc", "0:1", "51:0", "51"):
            with self.subTest(bad=bad), self.assertRaises(Q.Fail) as cm:
                Q.parse_refs([bad])
            self.assertEqual(cm.exception.code, 1)

    def test_matching_keys(self):
        cases = {"وَأَنْ": "وان", "ٱلْكِتَٰبُ": "الكتب", "هُدًۭى": "هدي", "الْأَوْفَىٰ": "الاوفي", "الأوفى": "الاوفي",
                 "رحمة": "رحمه", "الـــله": "الله", "﻿سعى؟": "سعي", "إِنَّهُۥ": "انه", "يَٰٓأَيُّهَا": "يايها",
                 "لِلْإِنْسَانِ": "للانسان", "۞": "", "ۛ": ""}
        for text, key in cases.items():
            with self.subTest(text=text):
                self.assertEqual(Q.norm_ar(text), key)

    def test_stand_alone_marks_join_their_word(self):
        text = FIX[URL.format("2:2", "quran-uthmani")]["body"]["data"]["text"]
        words = Q.split_words(text)
        self.assertEqual(len(words), 7)
        self.assertTrue(words[3].endswith(" ۛ") and words[4].endswith(" ۛ"), words)
        self.assertEqual(" ".join(words), text)
        self.assertEqual(Q.split_words("۞ إِنَّ ٱللَّهَ"), ["۞ إِنَّ", "ٱللَّهَ"])

    def test_basmala_prefix(self):
        text = Q.clean_text(FIX[URL.format("2:1", "quran-uthmani")]["body"]["data"]["text"])
        rest, pre = Q.strip_basmala(2, 1, text)
        self.assertEqual(rest, "الٓمٓ")
        self.assertEqual(Q.norm_ar(pre), "بسماللهالرحمنالرحيم")
        fatiha = Q.clean_text(FIX[URL.format("1:1", "quran-simple")]["body"]["data"]["text"])
        self.assertEqual(Q.strip_basmala(1, 1, fatiha), (fatiha, None))
        self.assertEqual(Q.strip_basmala(2, 2, text), (text, None))


class FetchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_exact_text_receipts_delay_and_cache(self):
        net, clock = FakeNet(), Clock()
        doc = Q.fetch_verses(Q.parse_refs(["51:22-23"])[0], "quran-simple", None, fetcher(self.tmp / "c", net, clock))
        self.assertEqual(doc["schema"], Q.SCHEMA_VERSES)
        self.assertIsNone(doc["translation"])
        self.assertIn("tanzil", doc["text_licence"].lower())
        v = doc["verses"][0]
        api = FIX[URL.format("51:22", "quran-simple")]["body"]["data"]
        self.assertEqual(v["text"], api["text"])
        self.assertEqual(v["sha256"], Q.sha256_text(api["text"]))
        self.assertEqual((v["ayah_ar"], v["surah_ar"], v["ref"]), ("٢٢", "٥١", "51:22"))
        self.assertEqual((v["url"], v["fetched"], v["edition"]), (URL.format("51:22", "quran-simple"),
                                                                  "2026-10-29T07:00:00Z", "quran-simple"))
        # Expected strings always come from the fixture, never retyped: a hand-typed «السَّمَاءِ» can put the shadda
        # and the fatha in the other order, which looks identical and is a different text.
        self.assertEqual(v["words"], api["text"].split())
        self.assertEqual([Q.norm_ar(x) for x in v["words"]], ["وفي", "السماء", "رزقكم", "وما", "توعدون"])
        self.assertNotIn("translation", v)
        self.assertEqual(len(doc["verses"][1]["words"]), 9)
        self.assertEqual([c[0] for c in net.calls], [URL.format("51:22", "quran-simple"), URL.format("51:23", "quran-simple")])
        self.assertTrue(all(c[1] == 20.0 and "kosif-quran-text" in c[2] for c in net.calls))
        self.assertEqual(clock.sleeps, [0.5])          # the second call waited for the delay
        silent = FakeNet(answers={})
        again = Q.fetch_verses(Q.parse_refs(["51:22-23"])[0], "quran-simple", None, fetcher(self.tmp / "c", silent))
        self.assertEqual(again, doc)
        self.assertEqual(silent.calls, [])

    def test_offline_without_cache(self):
        with self.assertRaises(Q.Fail) as cm:
            fetcher(self.tmp / "empty", offline=True).get(51, 22, "quran-simple")
        self.assertEqual(cm.exception.code, 3)

    def test_public_domain_translation(self):
        doc = Q.fetch_verses(Q.parse_refs(["53:39-41"])[0], "quran-simple", "en.pickthall", fetcher(self.tmp / "c"))
        t = doc["verses"][0]["translation"]
        self.assertEqual(t["text"], "And that man hath only that for which he maketh effort,")
        self.assertEqual((t["edition"], t["credit"]), ("en.pickthall", "Translation: M. Pickthall (public domain)"))
        self.assertIn("1930", doc["translation_licence"])

    def test_other_translations_and_editions_refused_without_a_call(self):
        net = FakeNet()
        for tr in ("en.sahih", "en.yusufali", "ar.muyassar"):
            with self.subTest(tr=tr), self.assertRaises(Q.Fail) as cm:
                Q.fetch_verses([(53, 39)], "quran-simple", tr, fetcher(self.tmp / "c", net))
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("public-domain", str(cm.exception))
        with self.assertRaises(Q.Fail):
            Q.fetch_verses([(53, 39)], "quran-tajweed", None, fetcher(self.tmp / "c", net))
        self.assertEqual(net.calls, [])
        proc = run("fetch", "53:39", "--translation", "en.sahih", "--out", self.tmp / "o")
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("refused", proc.stderr)
        self.assertFalse((self.tmp / "o" / "verses.json").exists())

    def test_basmala_and_bom(self):
        doc = Q.fetch_verses([(2, 1)], "quran-uthmani", None, fetcher(self.tmp / "c"))
        self.assertEqual(doc["verses"][0]["text"], "الٓمٓ")
        self.assertIn("بِسْمِ", doc["verses"][0]["basmala_stripped"])
        kept = Q.fetch_verses([(2, 1)], "quran-uthmani", None, fetcher(self.tmp / "c"), keep_basmala=True)
        self.assertTrue(kept["verses"][0]["text"].startswith("بِسْمِ"))
        fatiha = Q.fetch_verses([(1, 1)], "quran-simple", None, fetcher(self.tmp / "c"))["verses"][0]
        self.assertFalse(fatiha["text"].startswith("﻿"))
        self.assertNotIn("basmala_stripped", fatiha)
        self.assertEqual(len(fatiha["words"]), 4)

    def test_retry_after_a_busy_answer(self):
        clock = Clock()
        net = FakeNet(script=[(503, {"code": 503, "data": "busy"}, None), (429, {"code": 429}, {"Retry-After": "3"})])
        data = fetcher(self.tmp / "c", net, clock).get(51, 22, "quran-simple")[0]
        self.assertEqual(data["numberInSurah"], 22)
        self.assertEqual(len(net.calls), 3)
        self.assertEqual(clock.sleeps, [1.0, 3.0])     # back-off, then the server's Retry-After

    def test_failures_have_their_exit_codes(self):
        with self.assertRaises(Q.Fail) as cm:
            fetcher(self.tmp / "c").get(51, 99, "quran-simple")     # a real 404 answer
        self.assertEqual(cm.exception.code, 3)
        self.assertIn("HTTP 404", str(cm.exception))
        wrong = FakeNet(answers={URL.format("51:22", "quran-simple"): FIX[URL.format("51:23", "quran-simple")]})
        with self.assertRaises(Q.Fail) as cm:
            fetcher(self.tmp / "c2", wrong).get(51, 22, "quran-simple")
        self.assertEqual(cm.exception.code, 4)
        down = FakeNet(script=[urllib.error.URLError("down")] * 3)
        clock = Clock()
        with self.assertRaises(Q.Fail) as cm:
            fetcher(self.tmp / "c3", down, clock).get(51, 22, "quran-simple")
        self.assertEqual((cm.exception.code, len(down.calls), clock.sleeps), (3, 3, [1.0, 2.0]))

    def test_a_transfer_cut_off_mid_body_is_retried(self):
        class Cut(FakeResp):
            def read(self):
                raise http.client.IncompleteRead(b'{"code":200', 500)

        class CutNet(FakeNet):
            def __init__(self, cuts):
                super().__init__()
                self.cuts = cuts

            def __call__(self, req, timeout=None):
                if self.cuts:
                    self.cuts -= 1
                    self.calls.append((req.full_url, timeout, req.get_header("User-agent")))
                    return Cut(b"")
                return super().__call__(req, timeout)

        clock = Clock()
        data = fetcher(self.tmp / "c", CutNet(1), clock).get(51, 22, "quran-simple")[0]
        self.assertEqual(data["numberInSurah"], 22)
        self.assertEqual(clock.sleeps, [1.0])          # one back-off, then the whole answer
        net = CutNet(3)
        with self.assertRaises(Q.Fail) as cm:            # not a traceback: exit 3 after the retries
            fetcher(self.tmp / "c2", net).get(51, 22, "quran-simple")
        self.assertEqual((cm.exception.code, len(net.calls)), (3, 3))
        self.assertIn("IncompleteRead", str(cm.exception))

    def test_corrupt_cache_is_fetched_again(self):
        f = fetcher(self.tmp / "c")
        path = f.cache_path(51, 22, "quran-simple")
        path.parent.mkdir(parents=True)
        path.write_text("{not json", encoding="utf-8")
        net = FakeNet()
        fetcher(self.tmp / "c", net).get(51, 22, "quran-simple")
        self.assertEqual(len(net.calls), 1)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["schema"], Q.SCHEMA_CACHE)

    def test_cli_offline_from_a_filled_cache(self):
        f = fetcher(self.tmp / "cache")
        for ref in ("51:22", "51:23"):
            s, a = map(int, ref.split(":"))
            f.store(s, a, "quran-simple", FIX[URL.format(ref, "quran-simple")]["body"], "2026-10-29T07:00:00Z")
        proc = run("fetch", "51:22-23", "--offline", "--cache", self.tmp / "cache", "--out", self.tmp / "o")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("0 network calls, 2 from the cache", proc.stdout)
        lines = (self.tmp / "o" / "verses.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "51:22 | quran-simple | " + FIX[URL.format("51:22", "quran-simple")]["body"]["data"]["text"])
        self.assertEqual(json.loads((self.tmp / "o" / "verses.json").read_text(encoding="utf-8"))["refs"], ["51:22-23"])
        missing = run("fetch", "51:24", "--offline", "--cache", self.tmp / "cache", "--out", self.tmp / "o2")
        self.assertEqual(missing.returncode, 3, missing.stderr)


@unittest.skipIf(np is None, "numpy is not installed")
class PauseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_breaths_found_short_dips_ignored(self):
        x, sr = synth(NAJM_VOICED, NAJM_TOTAL)
        rep = Q.find_pauses(x, sr)
        gaps = [(p["start"], p["end"]) for p in rep["pauses"] if p["kind"] == "gap"]
        self.assertEqual(len(gaps), 2, rep["pauses"])                    # the 0.1 s dip at 17.30 is no pause
        for (s, e), (ws, we) in zip(gaps, [(5.95, 6.82), (11.15, 11.94)]):
            self.assertAlmostEqual(s, ws, delta=0.051)
            self.assertAlmostEqual(e, we, delta=0.051)
        self.assertEqual(rep["pauses"][-1]["kind"], "tail")
        self.assertEqual(rep["speech"], [0.05, 17.95])
        self.assertEqual(rep["rel_db_mode"], "fixed")

    def test_relative_threshold(self):
        x, sr = synth([(0.0, 3.0), (3.5, 6.0)], 6.0, floor=-30)          # a stretch 30 dB under the voice
        self.assertEqual([(p["start"], p["end"]) for p in Q.find_pauses(x, sr, rel_db=-22)["pauses"]], [(3.0, 3.5)])
        self.assertEqual(Q.find_pauses(x, sr, rel_db=-40)["pauses"], [])
        self.assertEqual(Q.find_pauses(x, sr, min_dur=0.6)["pauses"], [])
        with self.assertRaises(Q.Fail):
            Q.find_pauses(x, sr, rel_db=5)

    def test_auto_threshold_for_a_reverberant_recording(self):
        # An-Najm (an old recording): the breaths sit only ~15 dB under the voice, so -22 dB finds nothing.
        x, sr = synth(NAJM_VOICED, NAJM_TOTAL, floor=-15)
        fixed = Q.find_pauses(x, sr)
        self.assertFalse([p for p in fixed["pauses"] if p["kind"] == "gap"])
        self.assertIn("--rel-db auto", fixed["hint"])
        auto = Q.find_pauses(x, sr, rel_db="auto")
        self.assertEqual(auto["rel_db_mode"], "auto")
        self.assertEqual(len([p for p in auto["pauses"] if p["kind"] == "gap"]), 2)
        rep, note = Q.pauses_for_align(x, sr, 0.30, None, 0.05, boundaries_needed=2)
        self.assertEqual(rep["rel_db_mode"], "auto")
        self.assertIn("automatic threshold", note)
        rep, note = Q.pauses_for_align(x, sr, 0.30, -22.0, 0.05, boundaries_needed=2)   # an explicit value is kept
        self.assertEqual((rep["rel_db_mode"], note), ("fixed", None))
        self.assertEqual(auto["auto"]["chosen"], "otsu")
        self.assertTrue(auto["auto"]["quiet_share"] <= Q.AUTO_MAX_SHARE and auto["auto"]["sep_db"] >= Q.AUTO_MIN_SEP)

    def test_wasl_keeps_the_fixed_threshold(self):
        """A reciter who joins the verses without a breath: the level only dips with the syllables (-2 to -16 dB), so
        the frame levels form no quiet class. The Otsu split would run through the voice; -22 dB is kept."""
        x, sr = shaped(12.0, lambda t: -9.0 + 7.0 * np.cos(2 * np.pi * t / 0.8))
        fixed = Q.find_pauses(x, sr)
        self.assertEqual(gaps_of(fixed), [])
        self.assertIn("wasl", fixed["hint"])
        self.assertNotIn("try --rel-db auto", fixed["hint"])
        auto = Q.find_pauses(x, sr, rel_db="auto")
        self.assertEqual((auto["auto"]["chosen"], auto["rel_db"], gaps_of(auto)), ("fixed", -22.0, []))
        self.assertGreater(auto["auto"]["quiet_share"], Q.AUTO_MAX_SHARE)
        self.assertIn("wasl", auto["warning"])
        rep, note = Q.pauses_for_align(x, sr, 0.30, None, 0.05, boundaries_needed=1)
        self.assertEqual((rep["rel_db"], gaps_of(rep)), (-22.0, []))
        self.assertIn("not used", note)

    def test_deep_breaths_keep_the_fixed_threshold_under_auto(self):
        # Adh-Dhariyat: real breaths near -50 dB, and the doubled س of «السَّمَاءِ» dips to -16..-21 dB. The Otsu split
        # (-14 dB there) would call that dip a pause; auto keeps -22 dB once -22 dB finds a pause.
        x, sr = shaped(10.0, lambda t: np.where((t > 4.0) & (t < 4.8), -50.0,
                                                np.where((t > 7.0) & (t < 7.5), -17.0, -2.0)))
        auto = Q.find_pauses(x, sr, rel_db="auto")
        self.assertEqual((auto["auto"]["chosen"], auto["auto"]["fixed_gaps"]), ("fixed", 1))
        self.assertEqual(len(gaps_of(auto)), 1)
        self.assertAlmostEqual(gaps_of(auto)[0][0], 4.0, delta=0.051)

    def test_voice_end_before_the_reverb_tail(self):
        # The voice stops at 5.0 s; reverb stays at -12..-18 dB (above -22) until the file ends at 5.8 s.
        x, sr = shaped(5.8, lambda t: np.where(t < 5.0, -2.0, -12.0 - 7.5 * (t - 5.0)))
        rep = Q.find_pauses(x, sr)
        self.assertEqual(rep["speech"][1], 5.8)
        self.assertAlmostEqual(rep["voice_end"], 5.0, delta=0.051)
        self.assertIn("voice ends 5.0", Q.pauses_text(rep))
        clean, csr = synth(NAJM_VOICED, NAJM_TOTAL)       # no tail: the voice ends with the speech
        self.assertEqual(Q.find_pauses(clean, csr)["voice_end"], 17.95)

    def test_wav_without_ffmpeg_and_the_cli(self):
        x, sr = synth(NAJM_VOICED, NAJM_TOTAL)
        mono, stereo = self.tmp / "a.wav", self.tmp / "b.wav"
        write_wav(mono, x, sr)
        write_wav(stereo, x, sr, channels=2)
        with mock.patch.object(Q.shutil, "which", return_value=None):
            y, ysr, dec = Q.decode_audio(mono)
            self.assertEqual((ysr, dec, len(y)), (sr, "wave", len(x)))
            self.assertEqual(len(Q.read_wav(stereo)[0]), len(x))
            with self.assertRaises(Q.Fail):
                Q.decode_audio(self.tmp / "missing.m4a")
        proc = run("pauses", mono, "--json", "--out", self.tmp / "p.json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        rep = json.loads(proc.stdout)
        self.assertEqual(rep["schema"], Q.SCHEMA_PAUSES)
        self.assertEqual(len([p for p in rep["pauses"] if p["kind"] == "gap"]), 2)
        self.assertEqual(rep["sha256"], Q.sha256_file(mono))
        self.assertEqual(Q.load_pauses(self.tmp / "p.json")["pauses"], rep["pauses"])
        human = run("pauses", mono)
        self.assertIn("pause 5.95-6.80", human.stdout)


class AlignTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.najm = canonical(self.tmp / "najm", "53:39-41")

    def flat(self, res):
        return [w for v in res["verses"] for w in v["words"]]

    def assert_ordered(self, res):
        words = self.flat(res)
        for a, b in zip(words, words[1:]):
            self.assertLessEqual(a["end"], b["start"] + 1e-9, (a, b))
        for w in words:
            self.assertLessEqual(w["start"], w["end"])

    def test_clean_transcript_matches_every_word(self):
        res = Q.align(self.najm, R(AN_NAJM))
        words = self.flat(res)
        self.assertEqual([w["text"] for w in words], [w for v in self.najm for w in v["words"]])
        self.assertEqual(res["stats"]["matched"], 14)
        self.assertEqual([(w["start"], w["end"]) for w in words], [(s, e) for _, s, e in AN_NAJM])
        self.assertEqual([(v["n"], v["start"], v["end"]) for v in res["verses"]], [(39, 0.0, 5.68), (40, 5.68, 11.14),
                                                                                    (41, 11.14, 17.72)])

    def test_merge_split_miss_mishearing_and_extra_words(self):
        rows = list(AN_NAJM)
        rows[2:3] = [("للإن", 1.32, 2.40), ("سان", 2.40, 3.54)]            # the recogniser split one word
        rows = [r for r in rows if r[0] != "إلا"] + [("قال", 3.54, 4.26)]  # misheard: «قال» for «إلا»
        rows = [r for r in rows if r[0] not in ("سوف", "يرى", "الجزاء")]   # «الجزاء» missed entirely
        rows += [("سوفيرى", 9.08, 11.14),                                   # two words merged into one
                 ("صدق", 18.0, 18.4), ("الله", 18.4, 18.8), ("العظيم", 18.8, 19.5)]   # speech after the passage
        res = Q.align(self.najm, R(sorted(rows, key=lambda r: r[1])))
        w = self.flat(res)
        self.assertEqual([Q.norm_ar(x["text"]) for x in (w[2], w[3], w[8], w[9], w[12])],
                         ["للانسان", "الا", "سوف", "يري", "الجزاء"])
        self.assertEqual((w[2]["how"], w[2]["start"], w[2]["end"]), ("split", 1.32, 3.54))
        self.assertEqual((w[3]["source"], w[3]["start"], w[3]["end"]), ("interpolated", 3.54, 4.26))
        self.assertEqual([(x["how"], x["start"], x["end"]) for x in (w[8], w[9])],
                         [("merge", 9.08, 10.11), ("merge", 10.11, 11.14)])
        self.assertEqual((w[12]["source"], w[12]["start"], w[12]["end"]), ("interpolated", 14.14, 16.32))
        st = res["stats"]
        self.assertEqual((st["matched"], st["interpolated"], st["merged"], st["split"]), (12, 2, 2, 1))
        self.assertEqual([u["text"] for u in st["unmatched_recognised"]], ["قال", "صدق", "الله", "العظيم"])
        self.assertEqual(res["verses"][-1]["end"], 17.72)
        self.assert_ordered(res)

    def test_interpolation_follows_letter_count(self):
        verses = [{"surah": 112, "ayah": 1, "ref": "112:1", "ayah_ar": "١", "text": "قُلْ هُوَ اللَّهُ أَحَدٌ",
                   "words": ["قُلْ", "هُوَ", "اللَّهُ", "أَحَدٌ"]}]
        res = Q.align(verses, R([("قل", 0.0, 0.5), ("أحد", 3.0, 3.5)]))
        self.assertEqual([(x["start"], x["end"], x["source"]) for x in self.flat(res)],
                         [(0.0, 0.5, "matched"), (0.5, 1.333, "interpolated"), (1.333, 3.0, "interpolated"),
                          (3.0, 3.5, "matched")])
        res = Q.align(verses, R([("قل", 0.0, 1.0), ("الله", 1.0, 2.0), ("أحد", 2.0, 3.0)]))   # no room for «هو»
        words = self.flat(res)
        self.assertGreater(words[1]["end"] - words[1]["start"], 0.1)
        self.assertTrue(words[0].get("shared") and words[2].get("shared"))
        self.assertEqual((words[0]["start"], words[2]["end"]), (0.0, 2.0))
        self.assert_ordered(res)
        lead = Q.align(verses, R([("الله", 2.0, 2.4), ("أحد", 2.4, 3.0)]))     # nothing before: extend backwards
        self.assertGreaterEqual(self.flat(lead)[0]["start"], 0.0)
        self.assertEqual(self.flat(lead)[1]["how"], "extrapolated")

    def test_nothing_to_anchor_without_audio(self):
        with self.assertRaises(Q.Fail) as cm:
            Q.align(self.najm, R([("hello", 0, 1), ("world", 1, 2)]))
        self.assertEqual(cm.exception.code, 1)

    def test_loader_accepts_kosif_words_and_bare_lists(self):
        p = self.tmp / "w.json"
        Q.write_json(p, words_doc(AN_NAJM + [("...", 18, 18.1)]))
        words, meta = Q.load_recognised(p)
        self.assertEqual(len(words), 14)                   # punctuation-only entries are dropped
        self.assertEqual(meta["engine"]["model"], "large-v3")
        Q.write_json(p, [{"text": "وأن", "start": 0, "end": 0.3}])
        self.assertEqual(Q.load_recognised(p)[0][0]["key"], "وان")


class AlignEdgeTests(unittest.TestCase):
    """Alignment with a measured pauses report (no audio): speech before and after the verses, empty voiced stretches,
    late starts after a breath, the reverb tail and spelled-out opening letters."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def flat(self, res):
        return [w for v in res["verses"] for w in v["words"]]

    def test_istiadha_before_an_unmatched_first_word(self):
        verses = canonical(self.tmp, "51:22")
        rest = [("السماء", 5.0, 6.6), ("رزقكم", 6.6, 8.4), ("وما", 8.4, 9.2), ("توعدون", 9.2, 12.0)]
        pauses = pauses_doc([(3.2, 5.0)], (0.0, 15.0))
        for heard in ([], [("فيه", 5.0, 5.3)]):          # «وفي» dropped, or misheard as «فيه» right after the breath
            rows = ISTIADHA + heard + (rest if not heard else [("السماء", 5.3, 6.6)] + rest[1:])
            with self.subTest(heard=heard):
                res = Q.align(verses, R(rows), pauses)
                words = self.flat(res)
                self.assertEqual(res["verses"][0]["start"], 5.0)             # not 0.0, on top of the isti'adha
                self.assertEqual((Q.norm_ar(words[0]["text"]), words[0]["source"]), ("وفي", "interpolated"))
                self.assertGreaterEqual(words[0]["start"], 5.0)
                out = res["stats"]["outside_speech"]
                self.assertEqual([(o["side"], o["words"]) for o in out], [("before", "أعوذ بالله من الشيطان الرجيم")])
                self.assertIn("pause", out[0]["why"])
                self.assertTrue(res["stats"]["boundaries"][0]["snapped"])
                if heard:
                    self.assertEqual((words[0]["start"], words[0]["end"]), (5.0, 5.3))
        # no pause after the isti'adha: the formula itself says it is not the verse
        res = Q.align(verses, R(ISTIADHA + [("السماء", 3.0, 4.6), ("رزقكم", 4.6, 6.4)]), pauses_doc([], (0.0, 8.0)))
        self.assertEqual(res["verses"][0]["start"], 3.0)
        self.assertIn("formula", res["stats"]["outside_speech"][0]["why"])

    def test_sadaqa_after_a_dropped_last_word(self):
        verses = canonical(self.tmp, "51:22")
        rows = DHARIYAT_NOVAD[:4] + [("صدق", 10.2, 11.0), ("الله", 11.0, 12.0), ("العظيم", 12.0, 16.5)]
        res = Q.align(verses, R(rows), pauses_doc([(9.3, 10.2)], (0.0, 16.5)))
        words = self.flat(res)
        self.assertEqual(res["verses"][0]["end"], 9.3)                      # not 16.5, through «صدق الله العظيم»
        self.assertEqual((Q.norm_ar(words[4]["text"]), words[4]["source"]), ("توعدون", "interpolated"))
        self.assertEqual((words[3]["start"], words[3]["end"], words[4]["start"]), (4.68, 5.64, 5.64))
        self.assertEqual(res["stats"]["outside_speech"][0]["side"], "after")
        # a word misheard right after the last match, with no pause between, is still taken for the verse («يقول»)
        res = Q.align(verses, R(DHARIYAT_NOVAD[:4] + [("يقول", 5.64, 8.0)]), pauses_doc([], (0.0, 9.0)))
        self.assertEqual((res["verses"][0]["end"], res["stats"]["outside_speech"]), (9.0, []))

    def test_an_empty_voiced_stretch_at_a_verse_start_gets_its_word(self):
        """The doubled ب of «فَوَرَبِّ» splits off 12.50-13.50 at a soft threshold; whisper put «فورب» at 14.6 s."""
        verses = canonical(self.tmp, "51:22-23")
        res = Q.align(verses, R(DHARIYAT_NOVAD), pauses_doc([(11.35, 12.5), (13.5, 14.1), (23.3, 23.75)],
                                                            (0.0, 35.969), 35.5))
        v23 = res["verses"][1]["words"]
        self.assertEqual((Q.norm_ar(v23[0]["text"]), v23[0]["start"], v23[0]["end"]), ("فورب", 12.5, 13.5))
        self.assertTrue(v23[0]["moved"])
        self.assertEqual((v23[1]["start"], v23[2]["start"]), (14.1, 17.4))   # «السماء» snapped, «والأرض» kept
        self.assertNotIn("reshared", v23[1])                                 # 3.3 s for 6 letters is plausible
        self.assertFalse([m for m in res["stats"]["warnings"] if "holds no word" in m])
        self.assertEqual(res["verses"][1]["end"], 35.5)                     # the voice end, not the file end

    def test_a_late_start_after_a_breath_is_reshared_and_reported(self):
        verses = canonical(self.tmp, "51:22-23")
        res = Q.align(verses, R(DHARIYAT_NOVAD), pauses_doc([(11.35, 12.5), (23.3, 23.75)], (0.0, 35.969), 35.5))
        v22, v23 = res["verses"][0]["words"], res["verses"][1]["words"]
        self.assertEqual((v23[0]["start"], v23[0]["snap"]["start"], v23[0]["reshared"]), (12.5, -2.1, True))
        # 12.5-17.4 shared by letters (4 : 6) instead of «فورب» 12.5-16.0 (3.5 s for 4 letters) and «السماء» 1.4 s
        self.assertEqual((v23[0]["end"], v23[1]["start"], v23[1]["end"]), (14.46, 14.46, 17.4))
        self.assertEqual(res["stats"]["stretched"], [{"word": verses[1]["words"][0], "pulled_back": 2.1, "to": 12.5,
                                                     "reshared_with": verses[1]["words"][1]}])
        self.assertTrue(any("pulled back 2.10 s" in m for m in res["stats"]["warnings"]))
        self.assertEqual((v22[-1]["end"], v22[-1]["snap"]["end"]), (11.35, 2.19))
        self.assertEqual((v23[-1]["end"], res["voice_end"]), (35.5, 35.5))

    def test_wasl_boundary_from_the_word_timing(self):
        """No breath between the verses: the cut comes from the word timing, and the next verse starts right there
        instead of at whisper's late start (the screen would otherwise show nothing for 1.5 s)."""
        verses = [{"surah": 112, "ayah": 1, "ref": "112:1", "ayah_ar": "١", "text": "قُلْ هُوَ اللَّهُ أَحَدٌ",
                   "words": ["قُلْ", "هُوَ", "اللَّهُ", "أَحَدٌ"]},
                  {"surah": 112, "ayah": 2, "ref": "112:2", "ayah_ar": "٢", "text": "اللَّهُ الصَّمَدُ",
                   "words": ["اللَّهُ", "الصَّمَدُ"]}]
        rows = [("قل", 0.0, 0.6), ("هو", 0.6, 1.2), ("الله", 1.2, 2.4), ("أحد", 2.4, 4.8), ("الله", 7.4, 8.0),
                ("الصمد", 8.0, 11.5)]
        res = Q.align(verses, R(rows), pauses_doc([], (0.0, 12.0)))
        v1, v2 = res["verses"]
        self.assertEqual((v1["end"], v2["start"]), (6.1, 6.1))
        self.assertEqual(v2["words"][0]["snap"]["start"], -1.3)
        self.assertEqual(v2["end"], 12.0)
        self.assertFalse(res["stats"]["boundaries"][0]["snapped"])
        self.assertTrue(any("no pause" in m for m in res["stats"]["warnings"]))

    def test_spelled_out_opening_letters(self):
        verses = canonical(self.tmp, "2:1-2", "quran-uthmani")
        rest = [("ذلك", 9.0, 9.8), ("الكتاب", 9.8, 10.9), ("لا", 10.9, 11.3), ("ريب", 11.3, 12.0), ("فيه", 12.0, 12.8),
                ("هدى", 12.8, 13.5), ("للمتقين", 13.5, 15.0)]
        pauses = pauses_doc([(8.1, 8.9)], (0.0, 15.2))
        for spoken, how in (([("ألف", 0.0, 1.0), ("لام", 1.0, 4.5), ("ميم", 4.5, 8.0)], "spelled"),
                            ([("الم", 0.0, 8.0)], "1:1"), ([("ألف", 0.0, 1.0), ("لاممِيم", 1.0, 8.0)], "spelled")):
            with self.subTest(spoken=spoken):
                res = Q.align(verses, R(spoken + rest), pauses)
                v1, v2 = res["verses"]
                self.assertEqual((v1["start"], v1["end"], v2["start"]), (0.0, 8.1, 8.9))
                self.assertEqual((v1["words"][0]["how"], v1["words"][0]["source"]), (how, "matched"))
                self.assertEqual(v1["words"][0]["heard"], " ".join(t for t, _, _ in spoken))
                self.assertEqual(res["stats"]["unmatched_recognised"], [])
        self.assertEqual(Q.spoken_letters(2, 1, 0, "الم"), ["الف", "لام", "ميم"])
        self.assertEqual(Q.spoken_letters(42, 2, 0, "عسق"), ["عين", "سين", "قاف"])
        self.assertIsNone(Q.spoken_letters(105, 1, 0, "الم"))               # «أَلَمْ تَرَ»: a word, not letters
        self.assertIsNone(Q.spoken_letters(2, 1, 1, "الم"))
        self.assertEqual(len(Q.MUQATTAAT), 30)


@unittest.skipIf(np is None, "numpy is not installed")
class AlignWithAudioTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def flat(self, res):
        return [w for v in res["verses"] for w in v["words"]]

    def assert_no_word_crosses_a_pause(self, res):
        for w in self.flat(res):
            self.assertGreater(w["end"] - w["start"], 0.05, w)
            for p in res["pauses"]:
                overlap = min(w["end"], p["end"]) - max(w["start"], p["start"])
                self.assertLessEqual(overlap, 1e-6, (w, p))

    def test_boundaries_snap_to_breaths(self):
        verses = canonical(self.tmp, "53:39-41")
        x, sr = synth(NAJM_VOICED, NAJM_TOTAL)
        res = Q.align(verses, R(AN_NAJM), Q.find_pauses(x, sr))
        v = res["verses"]
        for got, want in zip([v[0]["start"], v[0]["end"], v[1]["start"], v[1]["end"], v[2]["start"], v[2]["end"]],
                             [0.05, 5.95, 6.82, 11.15, 11.94, 17.95]):
            self.assertAlmostEqual(got, want, delta=0.051)
        self.assertEqual(Q.norm_ar(v[1]["words"][0]["text"]), "وان")   # whisper put it at 5.68-7.24, across the breath
        self.assertEqual(v[1]["words"][0]["start"], v[1]["start"])
        self.assertEqual(sum(b["snapped"] for b in res["stats"]["boundaries"]), 2)
        self.assertEqual(res["stats"]["matched"], 14)
        self.assert_no_word_crosses_a_pause(res)

    def test_dropped_span_and_mishearing(self):
        """Adh-Dhariyat with VAD: 7 of 14 words recognised, «يقول» written for «أنكم تنطقون»."""
        verses = canonical(self.tmp, "51:22-23")
        x, sr = synth([(0.0, 11.35), (12.5, 23.3), (23.75, 33.7)], 35.97)
        res = Q.align(verses, R(DHARIYAT_VAD), Q.find_pauses(x, sr))
        v, words = res["verses"], self.flat(res)
        self.assertEqual([x["text"] for x in words], [x for vv in verses for x in vv["words"]])
        self.assertEqual((v[0]["end"], v[1]["start"]), (11.35, 12.5))
        self.assertEqual(v[1]["end"], 33.7)          # not cut at the misheard word (26.4)
        keys = [Q.norm_ar(x["text"]) for x in words]
        self.assertEqual((keys[4], words[4]["source"], words[4]["end"]), ("توعدون", "interpolated", 11.35))
        self.assertEqual((keys[5], words[5]["start"]), ("فورب", 12.5))
        self.assertEqual((keys[9], words[9]["source"], words[9]["end"]), ("لحق", "matched", 23.3))
        self.assertEqual((keys[10], words[10]["start"]), ("مثل", 23.75))
        self.assertEqual([x["source"] for x in words[12:]], ["interpolated", "interpolated"])
        self.assertEqual([u["text"] for u in res["stats"]["unmatched_recognised"]], ["يقول"])
        self.assertEqual((res["stats"]["matched"], res["stats"]["interpolated"]), (6, 8))
        self.assert_no_word_crosses_a_pause(res)

    def test_isti3adha_before_the_first_verse_is_left_out(self):
        verses = [{"surah": 112, "ayah": 1, "ref": "112:1", "ayah_ar": "١", "text": "قُلْ هُوَ اللَّهُ أَحَدٌ",
                   "words": ["قُلْ", "هُوَ", "اللَّهُ", "أَحَدٌ"]},
                  {"surah": 112, "ayah": 2, "ref": "112:2", "ayah_ar": "٢", "text": "اللَّهُ الصَّمَدُ",
                   "words": ["اللَّهُ", "الصَّمَدُ"]}]
        rows = [("أعوذ", 0.1, 0.6), ("بالله", 0.6, 1.2), ("من", 1.2, 1.4), ("الشيطان", 1.4, 2.0), ("الرجيم", 2.0, 2.4),
                ("قل", 3.1, 3.6), ("هو", 3.6, 4.3), ("الله", 4.3, 5.5), ("أحد", 5.5, 7.9),
                ("الله", 8.7, 9.6), ("الصمد", 9.6, 11.9)]
        x, sr = synth([(0.0, 2.4), (3.0, 8.0), (8.6, 12.0)], 12.5)
        res = Q.align(verses, R(rows), Q.find_pauses(x, sr))
        v = res["verses"]
        self.assertEqual((v[0]["start"], v[0]["end"], v[1]["start"], v[1]["end"]), (3.0, 8.0, 8.6, 12.0))
        self.assertEqual(len(res["stats"]["unmatched_recognised"]), 5)
        self.assertTrue(res["stats"]["boundaries"][0]["snapped"])
        self.assert_no_word_crosses_a_pause(res)

    def dip_case(self, dips, rows):
        verses = [{"surah": 112, "ayah": 1, "ref": "112:1", "ayah_ar": "١", "text": "قُلْ هُوَ اللَّهُ أَحَدٌ",
                   "words": ["قُلْ", "هُوَ", "اللَّهُ", "أَحَدٌ"]}]

        def level(t):
            out = np.full(len(t), -2.0)
            for a, b in dips:
                out[(t >= a) & (t < b)] = -22.0 + 2.0   # a consonant closure 18 dB under the voice, above -22
            return out

        x, sr = shaped(8.0, level)
        return Q.align(verses, R(rows), Q.find_pauses(x, sr), levels=Q.level_contour(x, sr))

    def test_a_long_words_start_moves_to_the_onset_after_a_clear_dip(self):
        rows = [("قل", 0.0, 1.2), ("هو", 1.2, 5.0), ("الله", 5.0, 6.5), ("أحد", 6.5, 8.0)]   # «هو» 3.8 s from 1.2 s
        res = self.dip_case([(2.4, 2.55)], rows)
        w = self.flat(res)
        self.assertEqual((w[1]["how"], w[1]["was"], w[1]["source"]), ("dip-snapped", "1:1", "matched"))
        self.assertAlmostEqual(w[1]["start"], 2.55, delta=0.03)              # where the closure ends
        self.assertAlmostEqual(w[1]["dip"]["shift"], 1.35, delta=0.03)
        self.assertEqual(w[0]["end"], w[1]["start"])
        self.assertEqual(res["stats"]["dip_snapped"][0]["from"], 1.2)
        self.assertEqual(res["stats"]["matched"], 4)
        self.assert_no_word_crosses_a_pause(res)
        plain = self.dip_case([], rows)                                      # no dip: whisper's time stays
        self.assertEqual([(x["start"], x["how"]) for x in self.flat(plain)[:2]], [(0.0, "1:1"), (1.2, "1:1")])
        self.assertEqual(plain["stats"]["dip_snapped"], [])
        inside = self.dip_case([(0.6, 0.75)], rows)                          # inside the matched «قل»: not used
        self.assertEqual(self.flat(inside)[1]["start"], 1.2)

    def test_an_otsu_pause_inside_a_matched_word_does_not_split_it(self):
        # An-Najm at -15 dB breaths, plus a 0.4 s dip inside «يجزاه» (whisper 12.44-14.14): the Otsu split finds it.
        voiced = [(0.05, 5.95), (6.82, 11.15), (11.94, 13.0), (13.4, 17.30), (17.40, 17.95)]
        x, sr = synth(voiced, NAJM_TOTAL, floor=-15)
        pa, note = Q.pauses_for_align(x, sr, 0.30, None, 0.05, boundaries_needed=2)
        self.assertEqual(pa["auto"]["chosen"], "otsu")
        self.assertEqual(len(gaps_of(pa)), 3)
        res = Q.align(canonical(self.tmp, "53:39-41"), R(AN_NAJM), pa)
        ign = res["stats"]["ignored_pauses"]
        self.assertEqual((len(ign), Q.norm_ar(ign[0]["inside"])), (1, "يجزاه"))
        self.assertAlmostEqual(ign[0]["start"], 13.0, delta=0.051)
        w = self.flat(res)
        self.assertEqual((Q.norm_ar(w[11]["text"]), w[11]["start"], w[11]["end"]), ("يجزاه", 12.44, 14.14))
        self.assertEqual(sum(b["snapped"] for b in res["stats"]["boundaries"]), 2)   # the breaths still cut verses
        self.assertEqual(len(res["pauses"]), len(pa["pauses"]) - 1)
        self.assert_no_word_crosses_a_pause(res)

    def test_cli_align_end_to_end_is_deterministic(self):
        canonical(self.tmp, "53:39-41")
        Q.write_json(self.tmp / "words.json", words_doc(AN_NAJM))
        x, sr = synth(NAJM_VOICED, NAJM_TOTAL)
        write_wav(self.tmp / "voice.wav", x, sr)
        outs = []
        for k in (1, 2):
            proc = run("align", "--verses", self.tmp / "verses.json", "--words", self.tmp / "words.json",
                       "--audio", self.tmp / "voice.wav", "--out", self.tmp / f"t{k}.json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            outs.append((self.tmp / f"t{k}.json").read_text(encoding="utf-8"))
        self.assertEqual(outs[0], outs[1])
        doc = json.loads(outs[0])
        self.assertEqual(doc["schema"], Q.SCHEMA_TIMING)
        self.assertEqual([v["n"] for v in doc["verses"]], [39, 40, 41])
        self.assertEqual((doc["stats"]["matched"], doc["stats"]["interpolated"]), (14, 0))
        self.assertEqual(doc["audio"]["sha256"], Q.sha256_file(self.tmp / "voice.wav"))
        self.assertIn("2/2 boundaries on pauses", proc.stdout)
        Q.write_json(self.tmp / "p.json", {**Q.find_pauses(x, sr)})
        proc = run("align", "--verses", self.tmp / "verses.json", "--words", self.tmp / "words.json",
                   "--pauses", self.tmp / "p.json", "--out", self.tmp / "t3.json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads((self.tmp / "t3.json").read_text(encoding="utf-8"))["verses"], doc["verses"])
        Q.write_json(self.tmp / "hand.json", {"schema": Q.SCHEMA_PAUSES, "speech": [0.05, 17.95],   # written by hand
                                             "pauses": [{"start": 11.15, "end": 11.94}, {"start": 5.95, "end": 6.82}]})
        hand = Q.load_pauses(self.tmp / "hand.json")
        self.assertEqual([(p["start"], p["kind"], p["dur"]) for p in hand["pauses"]], [(5.95, "gap", 0.87),
                                                                                       (11.15, "gap", 0.79)])
        proc = run("align", "--verses", self.tmp / "verses.json", "--words", self.tmp / "words.json",
                   "--pauses", self.tmp / "hand.json", "--out", self.tmp / "t5.json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        Q.write_json(self.tmp / "bad.json", {"schema": Q.SCHEMA_PAUSES, "speech": [0, 1], "pauses": [{"start": 2}]})
        with self.assertRaises(Q.Fail):
            Q.load_pauses(self.tmp / "bad.json")
        both = run("align", "--verses", self.tmp / "verses.json", "--words", self.tmp / "words.json",
                   "--audio", self.tmp / "voice.wav", "--pauses", self.tmp / "p.json", "--out", self.tmp / "t4.json")
        self.assertEqual(both.returncode, 1)


class CliTests(unittest.TestCase):
    def test_help_doctor_norm(self):
        self.assertEqual(run("--help").returncode, 0)
        doc = run("doctor", "--json")
        self.assertEqual(doc.returncode, 0, doc.stderr)
        self.assertIn("align", json.loads(doc.stdout)["commands"])
        norm = run("norm", "وَأَنَّ سَعْيَهُ سَوْفَ يُرَىٰ")
        self.assertEqual(norm.stdout.strip(), "وان سعيه سوف يري")


if __name__ == "__main__":
    unittest.main()
