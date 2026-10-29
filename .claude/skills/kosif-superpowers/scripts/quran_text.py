#!/usr/bin/env python3
"""KOSIF Quran text: exact verse text, measured pauses and verse/word timing for Quran reels.

نص الآيات بالضبط من مصدر موثّق، والوقفات المقاسة في التلاوة، وتوقيت كل آية وكل كلمة لريلز القرآن.

Written after two reels made by hand on 2026-10-29 (An-Najm 53:39-41 and Adh-Dhariyat 51:22-23). In both, the
verse text was copied and checksummed by hand and the breaths were measured with a 50 ms RMS. The word times were
also fixed by hand, because the speech model merged, split and misheard words (it wrote «يقول» for «تنطقون») and
dropped whole spans.

  python3 quran_text.py fetch 51:22-23 [53:39 ...] [--edition quran-simple|quran-uthmani]
                              [--translation none|en.pickthall] [--out DIR] [--cache DIR] [--offline] [--refresh]
                              [--keep-basmala] [--delay 0.5] [--timeout 20]
  python3 quran_text.py pauses AUDIO [--min 0.30] [--rel-db -22|auto] [--frame 0.05] [--json] [--out FILE]
  python3 quran_text.py align --verses verses.json --words words.json [--audio AUDIO | --pauses pauses.json]
                              [--min 0.30] [--rel-db -22|auto] [--max-dist 0.45] [--no-dip-snap] --out timing.json
  python3 quran_text.py norm TEXT...      # the matching key of Arabic text (tashkeel and Quranic marks removed)
  python3 quran_text.py doctor [--json]

fetch reads https://api.alquran.cloud/v1/ayah/<surah>:<ayah>/<edition> (Tanzil text). It sends a User-Agent, uses
a timeout, waits between calls, retries on 429 and 5xx, and keeps a JSON cache. It writes verses.json
(kosif.quran-verses.v1) and verses.txt. Translation is off by default, and only public-domain editions are accepted
(en.pickthall).
pauses decodes the audio with ffmpeg to 16 kHz mono float32 (a PCM .wav can also be read without ffmpeg). It lists
every stretch whose 50 ms RMS stays below peak + rel-db for at least --min seconds, and voice_end, where the level
falls 8 dB under the final voice level (the reverb after it holds no word). --rel-db auto takes the threshold from the
recording itself (an Otsu split of the frame levels), for old or reverberant recordings whose breaths sit only 12-20 dB
under the voice. The split is believed only when -22 dB finds no pause and the levels form two classes. A wasl
recitation, whose verses join without a breath, keeps -22 dB: a split through its voice finds pauses inside words.
align maps each canonical word to the recogniser's words (kosif-words/1) with an edit-distance alignment that allows
merges, splits, misses, extra words and spelled-out opening letters («الم» said «ألف لام ميم»). It fills in the
unmatched words by letter count. With --audio it also snaps verse boundaries to measured pauses, so that no word
crosses a pause, and keeps the isti'adha and «صدق الله العظيم» out of the verses. It gives every voiced stretch of a
verse a word and moves the start of a long word to the onset after a clear consonant dip. It writes timing.json
(kosif.quran-timing.v1).

Exit codes: 0 done, 1 bad input or refused, 3 network or API failure, 4 the API answered a different verse.
Only pauses and align --audio need numpy; everything else uses the Python standard library.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import http.client
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import wave
from pathlib import Path

SCHEMA_VERSES = "kosif.quran-verses.v1"
SCHEMA_PAUSES = "kosif.quran-pauses.v1"
SCHEMA_TIMING = "kosif.quran-timing.v1"
SCHEMA_CACHE = "kosif.quran-cache.v1"
API_BASE = "https://api.alquran.cloud/v1/ayah/"
USER_AGENT = "kosif-quran-text/1 (+https://github.com/kosif199022-jpg/kosif-tool)"
EDITIONS = ("quran-simple", "quran-uthmani")
TEXT_CREDIT = "Quran text: Tanzil Project (tanzil.net), via api.alquran.cloud"
TEXT_LICENCE = ("Quran text of the Tanzil Project (tanzil.net, Creative Commons Attribution 3.0), served by "
                "api.alquran.cloud: copy it verbatim, never change a letter or a mark, credit Tanzil and link tanzil.net.")
TRANSLATIONS = {
    "en.pickthall": {
        "credit": "Translation: M. Pickthall (public domain)",
        "licence": ("Marmaduke Pickthall, The Meaning of the Glorious Koran (1930). Pickthall died in 1936, so the "
                    "author's life + 70 years ended in 2006, and the 1930 edition is more than 95 years old. It is "
                    "treated here as public domain. Keep the wording unchanged and credit Pickthall."),
    },
}
# Ayat per surah (Hafs, 6236 in all); used to check a reference before any network call.
AYAH_COUNTS = (
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135,
    112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85,
    54, 53, 89, 59, 37, 35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13,
    14, 11, 11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42,
    29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11,
    11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6,
)
ARABIC_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
WESTERN_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")

# Matching key: tashkeel and Quranic annotation marks, superscript alef and tatweel go; alef forms, alef maqsura and
# ta marbuta are unified. The canonical text itself is never changed; only these keys are compared.
_MARKS = re.compile("[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_INVISIBLE = re.compile("[​-‏‪-‮⁦-⁩﻿؜]")
_UNIFY = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
                        "ى": "ي", "ة": "ه"})
BASMALA_KEY = ["بسم", "الله", "الرحمن", "الرحيم"]

DEFAULT_MAX_DIST = 0.45   # a pair counts as the same word when edit distance / longer length <= this
PAIR_SHAPES = ((1, 1), (1, 2), (2, 1), (1, 3), (3, 1))   # canonical words : recognised words
SHAPE_PENALTY = 0.15      # per extra piece: a merge or a split costs a little more than a clean 1:1 match
GAP_COST = 1.0            # a missed canonical word, or an extra recognised word
MAX_CELLS = 1_500_000     # alignment table size limit; split longer passages into verse ranges
MIN_WORD = 0.12           # seconds an interpolated word needs before its matched neighbours lend it time
MIN_LETTER = 0.06
EPS = 1e-6
# With --audio. Measured on Adh-Dhariyat 51:22-23, where whisper put «السَّمَاءِ» (v23) at 16.0 s and the voice says it
# at 14.1 s, after the closure dip of «رَبِّ»; «رِزْقُكُمْ» at 2.38 s, said at about 3.0 s.
LONG_WORD = 2.2           # s: a word this long, or the word after it, has its start refined at a level dip
DIP_WINDOW = 1.8          # s on each side of the start searched for that dip, inside the same pause-free segment
DIP_MARGIN = 6.0          # dB: a dip must be this much quieter than the level at the current start (clearly deeper)
DIP_DIST_DB = 4.0         # dB per second of distance taken off a dip's depth, so a near dip beats a slightly deeper one
DIP_MIN_SCORE = 4.0       # dB: depth minus that distance penalty
DIP_PROM = 3.0            # dB: a local minimum counts as a dip when the level rises this much on both sides ...
DIP_SIDE = 0.25           # ... within this many seconds
DIP_VALLEY = 3.0          # dB: the word starts where the valley (within this much of the minimum) ends: the onset
DIP_MIN_SHARE = 0.5       # neither neighbour may keep less than this share of the passage's seconds per letter
SNAP_RESHARE = 0.5        # s: a start pulled back this far to a pause re-shares the word and the next by letter count
RESHARE_RATE = 1.5        # ... when the stretched word is this much slower per letter than the passage («فَوَرَبِّ»
                          # 3.5 s for 4 letters: 1.9 times; «السَّمَاءِ» pulled back to 14.1 s: 1.2 times, kept)
MIN_SEGMENT = 0.15        # s: a voiced segment at least this long inside a verse must hold a word
SOFT_MARGIN = 0.05        # s: an Otsu pause this far inside a matched word's recognised time does not split it
LETTER_EXCESS = 2.0       # extras with more than this many times the letters of the unmatched words are extra speech
# Speech outside the verses that recitations open or close with; extra words matching two or more of them in a row
# are never taken for mis-hearings of an unmatched verse word.
FORMULAS = {"isti'adha": ["اعوذ", "بالله", "من", "الشيطان", "الرجيم"], "basmala": BASMALA_KEY,
            "sadaqa": ["صدق", "الله", "العظيم"]}
LEAD_FORMULAS, TRAIL_FORMULAS = ("isti'adha", "basmala"), ("sadaqa",)
# Huruf muqatta'at: the opening letters of 29 surahs (and 42:2) are recited by their names, «الم» as «ألف لام ميم».
LETTER_NAMES = {"ا": "الف", "ل": "لام", "م": "ميم", "ص": "صاد", "ر": "را", "ك": "كاف", "ه": "ها", "ي": "يا",
                "ع": "عين", "ط": "طا", "س": "سين", "ح": "حا", "ق": "قاف", "ن": "نون"}
MUQATTAAT = frozenset({(2, 1), (3, 1), (7, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (19, 1),
                       (20, 1), (26, 1), (27, 1), (28, 1), (29, 1), (30, 1), (31, 1), (32, 1), (36, 1), (38, 1),
                       (40, 1), (41, 1), (42, 1), (42, 2), (43, 1), (44, 1), (45, 1), (46, 1), (50, 1), (68, 1)})


class Fail(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


# ------------------------------------------------------------------ text helpers

def norm_ar(text) -> str:
    """The matching key of Arabic text: no tashkeel, Quranic marks, tatweel, punctuation or spaces; unified letters."""
    s = unicodedata.normalize("NFKC", str(text))
    s = _INVISIBLE.sub("", s)
    s = _MARKS.sub("", s)
    s = s.translate(_UNIFY)
    return "".join(ch for ch in s if ch.isalnum())


def clean_text(text: str) -> str:
    """Drop a byte-order mark and repeated whitespace. Letters and marks stay byte for byte (no Unicode normalisation)."""
    return " ".join(str(text).replace("﻿", "").split())


def split_words(text: str) -> list:
    """Words of a verse. A stand-alone mark (waqf sign, ۞, ۩) joins the word before it, or the next word at the start,
    so " ".join(words) == text."""
    words, pending = [], []
    for tok in text.split():
        if not norm_ar(tok):
            if words:
                words[-1] += " " + tok
            else:
                pending.append(tok)
            continue
        if pending:
            tok = " ".join(pending + [tok])
            pending = []
        words.append(tok)
    if pending:
        words.append(" ".join(pending))
    return words


def strip_basmala(surah: int, ayah: int, text: str):
    """alquran.cloud prefixes the basmala to ayah 1 of every surah except 1 and 9. Returns (text, stripped prefix)."""
    if ayah != 1 or surah in (1, 9):
        return text, None
    toks = list(re.finditer(r"\S+", text))
    if len(toks) > 4 and [norm_ar(t.group()) for t in toks[:4]] == BASMALA_KEY:
        return text[toks[4].start():].strip(), text[:toks[3].end()].strip()
    return text, None


def to_arabic_digits(n) -> str:
    return str(n).translate(ARABIC_DIGITS)


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def r3(x) -> float:
    return round(float(x) + 0.0, 3)


def write_json(path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def read_json(path, what: str):
    path = Path(path)
    if not path.is_file():
        raise Fail(1, f"{what} file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, ValueError) as e:
        raise Fail(1, f"{path} is not valid JSON: {e}")


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if f == f else None


# ------------------------------------------------------------------ references

_REF = re.compile(r"^(\d{1,3})[:.](\d{1,3})(?:-(\d{1,3}))?$")


def parse_refs(items) -> tuple:
    """['51:22-23', '53:39'] → ([(51, 22), (51, 23), (53, 39)], ['51:22-23', '53:39']). Arabic-Indic digits work too."""
    out, seen, labels = [], set(), []
    for item in items:
        text = str(item).translate(WESTERN_DIGITS).replace("–", "-").replace("—", "-")
        for part in re.split(r"[,،\s]+", text.strip()):
            if not part:
                continue
            m = _REF.match(part)
            if not m:
                raise Fail(1, f"reference {part!r} is not surah:ayah or surah:first-last (for example 51:22-23)")
            s, a1 = int(m.group(1)), int(m.group(2))
            a2 = int(m.group(3)) if m.group(3) else a1
            if not 1 <= s <= 114:
                raise Fail(1, f"{part}: the surah number must be 1-114")
            count = AYAH_COUNTS[s - 1]
            if not 1 <= a1 <= a2 <= count:
                raise Fail(1, f"{part}: surah {s} has {count} ayat; the range must lie within 1-{count} and run forward")
            labels.append(f"{s}:{a1}" if a1 == a2 else f"{s}:{a1}-{a2}")
            for a in range(a1, a2 + 1):
                if (s, a) not in seen:
                    seen.add((s, a))
                    out.append((s, a))
    if not out:
        raise Fail(1, "give at least one reference, for example 51:22-23")
    return out, labels


# ------------------------------------------------------------------ fetch

def check_answer(body, s: int, a: int, edition: str, url: str) -> dict:
    if not isinstance(body, dict) or body.get("code") != 200 or not isinstance(body.get("data"), dict):
        raise Fail(4, f"{url}: unexpected answer {json.dumps(body, ensure_ascii=False)[:200]}")
    d = body["data"]
    try:
        ok = (int(d["numberInSurah"]) == a and int(d["surah"]["number"]) == s
              and d["edition"]["identifier"] == edition and isinstance(d["text"], str) and d["text"].strip() != "")
    except (KeyError, TypeError, ValueError):
        ok = False
    if not ok:
        raise Fail(4, f"{url}: the answer is not {s}:{a} in {edition}")
    return d


def _http_message(err) -> str:
    try:
        body = json.loads(err.read().decode("utf-8"))
        return str(body.get("data") or body.get("status") or "")[:200]
    except Exception:
        return str(getattr(err, "reason", ""))[:200]


def _retry_after(err):
    try:
        return max(0.0, float(err.headers.get("Retry-After")))
    except (TypeError, ValueError, AttributeError):
        return None


class Fetcher:
    """GET one ayah per call, with a JSON cache, a polite delay between calls, a timeout and retries on 429/5xx."""

    def __init__(self, cache_dir, *, offline=False, refresh=False, delay=0.5, timeout=20.0, retries=3,
                 opener=None, sleep=None, clock=None, now=None):
        self.cache_dir = Path(cache_dir)
        self.offline, self.refresh = offline, refresh
        self.delay, self.timeout, self.retries = max(0.0, float(delay)), float(timeout), max(1, int(retries))
        self.opener = opener or urllib.request.urlopen
        self.sleep = sleep or time.sleep
        self.clock = clock or time.monotonic
        self.now = now or utc_now
        self._last = None
        self.calls = 0
        self.cache_hits = 0

    @staticmethod
    def url(s: int, a: int, edition: str) -> str:
        return f"{API_BASE}{s}:{a}/{edition}"

    def cache_path(self, s: int, a: int, edition: str) -> Path:
        return self.cache_dir / edition / f"{s:03d}_{a:03d}.json"

    def store(self, s: int, a: int, edition: str, body, fetched: str) -> None:
        write_json(self.cache_path(s, a, edition),
                   {"schema": SCHEMA_CACHE, "url": self.url(s, a, edition), "fetched": fetched, "body": body})

    def get(self, s: int, a: int, edition: str):
        """→ (data, url, fetched, from_cache)."""
        url = self.url(s, a, edition)
        path = self.cache_path(s, a, edition)
        if path.is_file() and not self.refresh:
            try:
                rec = json.loads(path.read_text(encoding="utf-8"))
                data = check_answer(rec["body"], s, a, edition, url)
                self.cache_hits += 1
                return data, url, str(rec.get("fetched") or ""), True
            except (Fail, ValueError, KeyError, TypeError, UnicodeDecodeError):
                pass   # an unreadable or wrong cache entry is fetched again
        if self.offline:
            raise Fail(3, f"{s}:{a} ({edition}) is not in the cache {path.parent} and --offline is set")
        body = self._download(url)
        data = check_answer(body, s, a, edition, url)
        fetched = self.now()
        self.store(s, a, edition, body, fetched)
        return data, url, fetched, False

    def _wait(self) -> None:
        if self._last is not None:
            gap = self.clock() - self._last
            if gap < self.delay:
                self.sleep(self.delay - gap)
        self._last = self.clock()

    def _download(self, url: str):
        last_err = ""
        for attempt in range(self.retries):
            self._wait()
            self.calls += 1
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            wait = None
            try:
                with self.opener(req, timeout=self.timeout) as resp:
                    raw = resp.read()
                try:
                    return json.loads(raw.decode("utf-8"))
                except (UnicodeDecodeError, ValueError):
                    raise Fail(3, f"{url} did not answer with JSON")
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code >= 500:
                    last_err, wait = f"HTTP {e.code} {_http_message(e)}".strip(), _retry_after(e)
                else:
                    raise Fail(3, f"HTTP {e.code} from {url}: {_http_message(e)}")
            except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as e:
                # HTTPException: a body cut off mid-transfer (IncompleteRead) or a garbled status line (BadStatusLine)
                last_err = f"{type(e).__name__}: {getattr(e, 'reason', e)}"
            if attempt + 1 < self.retries:
                self.sleep(min(30.0, wait if wait is not None else max(1.0, self.delay) * 2 ** attempt))
        raise Fail(3, f"{url} failed after {self.retries} tries ({last_err}); check the network, "
                      f"or use --offline with a filled cache")


def refusal(tr: str) -> str:
    return (f"translation {tr!r} refused: only public-domain translations are accepted here "
            f"({', '.join(TRANSLATIONS)}). Most modern translations, Saheeh International (en.sahih) among them, are "
            f"copyrighted. Use one only with the rights holder's licence and outside this tool, or keep --translation none.")


def build_verse(fetcher: Fetcher, s: int, a: int, edition: str, translation, keep_basmala: bool) -> dict:
    d, url, fetched, _ = fetcher.get(s, a, edition)
    text = clean_text(d["text"])
    basmala = None
    if not keep_basmala:
        text, basmala = strip_basmala(s, a, text)
    surah = d.get("surah") or {}
    v = {"surah": s, "ayah": a, "ref": f"{s}:{a}", "ayah_ar": to_arabic_digits(a), "surah_ar": to_arabic_digits(s),
         "surah_name_ar": surah.get("name"), "surah_name_en": surah.get("englishName"),
         "text": text, "words": split_words(text), "sha256": sha256_text(text),
         "edition": edition, "url": url, "fetched": fetched}
    if basmala:
        v["basmala_stripped"] = basmala
    if translation:
        td, turl, tf, _ = fetcher.get(s, a, translation)
        tt = clean_text(td["text"])
        v["translation"] = {"edition": translation, "text": tt, "sha256": sha256_text(tt), "url": turl, "fetched": tf,
                            "credit": TRANSLATIONS[translation]["credit"]}
    return v


def fetch_verses(refs, edition="quran-simple", translation=None, fetcher: Fetcher = None, keep_basmala=False,
                 labels=None) -> dict:
    if edition not in EDITIONS:
        raise Fail(1, f"edition {edition!r} is not supported; use {' or '.join(EDITIONS)} (Tanzil Arabic text)")
    tr = None if translation in (None, "", "none", "off", "no") else str(translation)
    if tr is not None and tr not in TRANSLATIONS:
        raise Fail(1, refusal(tr))
    verses = [build_verse(fetcher, s, a, edition, tr, keep_basmala) for s, a in refs]
    doc = {"schema": SCHEMA_VERSES, "refs": labels or [f"{s}:{a}" for s, a in refs], "edition": edition,
           "translation": tr, "source": "https://api.alquran.cloud", "credit": TEXT_CREDIT, "text_licence": TEXT_LICENCE}
    if tr:
        doc["translation_credit"] = TRANSLATIONS[tr]["credit"]
        doc["translation_licence"] = TRANSLATIONS[tr]["licence"]
    doc["verses"] = verses
    return doc


def cmd_fetch(a) -> int:
    tr = (a.translation or "none").strip()
    if tr.lower() in ("none", "off", "no", ""):
        tr = None
    elif tr not in TRANSLATIONS:
        raise Fail(1, refusal(tr))   # refused before any reference parsing or network call
    refs, labels = parse_refs(a.refs)
    out = Path(a.out)
    fetcher = Fetcher(Path(a.cache) if a.cache else out / "cache", offline=a.offline, refresh=a.refresh,
                      delay=a.delay, timeout=a.timeout)
    doc = fetch_verses(refs, a.edition, tr, fetcher, a.keep_basmala, labels)
    lines = []
    for v in doc["verses"]:
        lines.append(f"{v['ref']} | {v['edition']} | {v['text']}")
        if "translation" in v:
            lines.append(f"{v['ref']} | {v['translation']['edition']} | {v['translation']['text']}")
    write_json(out / "verses.json", doc)
    (out / "verses.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    stripped = [v["ref"] for v in doc["verses"] if v.get("basmala_stripped")]
    if stripped:
        print(f"basmala prefix removed from {', '.join(stripped)} (shown only when recited; --keep-basmala keeps it)",
              file=sys.stderr)
    print(f"wrote {out / 'verses.json'} and verses.txt: {len(doc['verses'])} verses, {fetcher.calls} network calls, "
          f"{fetcher.cache_hits} from the cache")
    return 0


# ------------------------------------------------------------------ pauses

def _numpy():
    try:
        import numpy as np
    except ImportError:
        raise Fail(1, "numpy is not installed: pip install numpy (pauses and align --audio need it)")
    return np


def read_wav(path):
    """PCM .wav → (mono float32 samples, sample rate), without ffmpeg."""
    np = _numpy()
    try:
        with wave.open(str(path), "rb") as w:
            ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
            raw = w.readframes(n)
    except (wave.Error, EOFError) as e:
        raise Fail(1, f"{path} is not a PCM .wav that Python can read ({e}); install ffmpeg to decode it")
    if sw == 1:
        x = (np.frombuffer(raw, np.uint8).astype(np.float32) - 128.0) / 128.0
    elif sw == 2:
        x = np.frombuffer(raw, "<i2").astype(np.float32) / 32768.0
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3).astype(np.int32)
        v = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        x = np.where(v >= 1 << 23, v - (1 << 24), v).astype(np.float32) / float(1 << 23)
    elif sw == 4:
        x = np.frombuffer(raw, "<i4").astype(np.float32) / float(1 << 31)
    else:
        raise Fail(1, f"{path}: {sw * 8}-bit samples are not supported; install ffmpeg")
    if ch > 1:
        x = x[: len(x) // ch * ch].reshape(-1, ch).mean(axis=1)
    return x.astype(np.float32), sr


def decode_audio(path):
    """→ (mono float32 samples, sample rate, decoder). ffmpeg gives 16 kHz; without it only PCM .wav is read."""
    path = Path(path)
    if not path.is_file():
        raise Fail(1, f"audio file not found: {path}")
    np = _numpy()
    ff = shutil.which("ffmpeg")
    if ff:
        r = subprocess.run([ff, "-nostdin", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000",
                            "-f", "f32le", "-"], capture_output=True)
        if r.returncode != 0 or not r.stdout:
            raise Fail(1, f"ffmpeg could not decode {path}: {r.stderr.decode('utf-8', 'replace').strip()[-300:]}")
        return np.frombuffer(r.stdout, np.float32).copy(), 16000, "ffmpeg"
    if path.suffix.lower() == ".wav":
        x, sr = read_wav(path)
        return x, sr, "wave"
    raise Fail(1, "ffmpeg is not installed: it is needed to read m4a, mp3 or mp4 (a PCM .wav works without it)")


FIXED_REL_DB = -22.0         # the default threshold: 22 dB under the loudest 50 ms frame
AUTO_RANGE = (-30.0, -6.0)   # the automatic threshold stays within these dB below the peak
# The Otsu split is believed only when the frame levels really form two classes. Measured on the two delivered
# recitations: An-Najm (reverberant, real breaths 12-20 dB under the voice) puts 14% of its frames under the split,
# with the class means 14.1 dB apart (15-18%, 8-12 dB with noise added). Adh-Dhariyat with its two breaths cut out
# (wasl, the verses joined without a breath) puts 36% under the split, 9.3 dB apart. That split runs through the voice
# itself and found 15 "pauses" inside words. With noise added, with or without its breaths, the share stays 36-45%.
AUTO_MAX_SHARE = 0.30        # breaths are a minority of a recitation's frames
AUTO_MIN_SHARE = 0.03        # ... but more than the silence before and after the voice (An-Najm cut: 1%)
AUTO_MIN_SEP = 12.0          # dB between the mean levels of the quiet and the loud class
TAIL_DROP_DB = 8.0           # the voice ends where the level falls this far under its final level (reverb follows)
TAIL_REF_S = 3.0             # seconds before the speech end whose voiced frames give that final level


def otsu_split(db, peak: float) -> dict:
    """Otsu split of the frame levels (digital silence excluded): the level that best separates voice from breaths,
    with the statistics that say whether the levels really form two classes (two_class)."""
    np = _numpy()
    v = np.sort(db[db > peak - 80.0])
    if len(v) < 4:
        return {"rel_db": FIXED_REL_DB, "quiet_share": None, "sep_db": None, "two_class": False}
    c = np.cumsum(v)
    k = np.arange(1, len(v))
    m0 = c[:-1] / k
    m1 = (c[-1] - c[:-1]) / (len(v) - k)
    between = k * (len(v) - k) * (m0 - m1) ** 2
    best = int(np.argmax(between))
    rel = float((v[best] + v[best + 1]) / 2.0 - peak)
    share, sep = (best + 1) / float(len(v)), float(m1[best] - m0[best])
    return {"rel_db": round(min(AUTO_RANGE[1], max(AUTO_RANGE[0], rel)), 1), "quiet_share": round(share, 3),
            "sep_db": round(sep, 1),
            "two_class": AUTO_MIN_SHARE <= share <= AUTO_MAX_SHARE and sep >= AUTO_MIN_SEP}


def _frame_db(samples, sr: int, frame: float):
    np = _numpy()
    x = np.asarray(samples, dtype=np.float64).ravel()
    if sr <= 0 or frame <= 0:
        raise Fail(1, "sample rate and frame must be positive")
    hop = max(1, int(round(sr * frame)))
    n = len(x) // hop
    if n == 0:
        raise Fail(1, "the audio is shorter than one analysis frame")
    fr = x[: n * hop].reshape(n, hop)
    return 20.0 * np.log10(np.maximum(np.sqrt(np.mean(fr * fr, axis=1)), 1e-10)), hop / float(sr), len(x) / float(sr)


def _stretches(quiet, fs: float, duration: float, min_dur: float) -> list:
    n, pauses, i = len(quiet), [], 0
    while i < n:
        if not quiet[i]:
            i += 1
            continue
        j = i
        while j < n and quiet[j]:
            j += 1
        start, end = i * fs, (duration if j == n else j * fs)
        if end - start >= min_dur - 1e-9:
            kind = "lead" if i == 0 else ("tail" if j == n else "gap")
            pauses.append({"start": r3(start), "end": r3(end), "dur": r3(end - start), "kind": kind})
        i = j
    return pauses


def _gap_count(pauses) -> int:
    return sum(p["kind"] == "gap" for p in pauses)


def voice_end_of(db, fs: float, thr: float, first: int, stop: int, duration: float) -> float:
    """Where the voice itself ends: the end of the last frame within TAIL_DROP_DB of the final voice level (the median
    of the voiced frames in the last TAIL_REF_S seconds). The reverb or room tone after it can stay above the pause
    threshold up to the end of the file: Adh-Dhariyat ends at -21.5 dB, its voice at 35.50 s, the file at 35.97 s."""
    np = _numpy()
    first = max(0, min(first, stop - 1))
    tail = db[max(first, stop - int(round(TAIL_REF_S / fs))):stop]
    voiced = tail[tail >= thr]
    if not len(voiced):
        return duration if stop >= len(db) else stop * fs
    lim = float(np.median(voiced)) - TAIL_DROP_DB
    k = stop - 1
    while k > first and db[k] < lim:
        k -= 1
    return duration if k + 1 >= len(db) else (k + 1) * fs


DIP_FRAME, DIP_HOP = 0.05, 0.01   # the level contour used to refine word starts: 50 ms RMS every 10 ms


def level_contour(samples, sr: int, frame: float = DIP_FRAME, hop: float = DIP_HOP) -> dict:
    """50 ms RMS every 10 ms, in dB under the loudest frame: {"db": array, "hop", "offset"} (frame k is centred at
    offset + k * hop). align uses it to refine the start of long words at a consonant dip."""
    np = _numpy()
    x = np.asarray(samples, dtype=np.float64).ravel()
    win, step = max(1, int(round(sr * frame))), max(1, int(round(sr * hop)))
    if sr <= 0 or len(x) < win:
        raise Fail(1, "the audio is shorter than one analysis frame")
    c = np.concatenate(([0.0], np.cumsum(x * x)))
    starts = np.arange(0, len(x) - win + 1, step)
    rms = np.sqrt(np.maximum((c[starts + win] - c[starts]) / win, 0.0))
    db = 20.0 * np.log10(np.maximum(rms, 1e-10))
    return {"db": db - db.max(), "hop": step / float(sr), "offset": win / 2.0 / sr}


def auto_choice(db, peak: float, fs: float, duration: float, min_dur: float) -> dict:
    """What --rel-db auto means: the Otsu split, but only for a recording whose quiet stretches never reach 22 dB under
    the peak AND whose frame levels form two classes. Otherwise the fixed -22 dB, with the reason."""
    split = otsu_split(db, peak)
    fixed_gaps = _gap_count(_stretches(db < peak + FIXED_REL_DB, fs, duration, min_dur))
    info = {"otsu_rel_db": split["rel_db"], "quiet_share": split["quiet_share"], "sep_db": split["sep_db"],
            "fixed_gaps": fixed_gaps}
    if fixed_gaps:
        info.update(chosen="fixed", reason=(
            f"the recording already has {fixed_gaps} pause(s) below {FIXED_REL_DB:g} dB, so its breaths are deep; the "
            f"Otsu split ({split['rel_db']:g} dB) would only add dips inside the voice (a doubled س, a soft consonant, "
            f"a madd), so {FIXED_REL_DB:g} dB was kept"))
    elif not split["two_class"] or split["rel_db"] <= FIXED_REL_DB:
        share = "?" if split["quiet_share"] is None else f"{split['quiet_share'] * 100:.0f}%"
        info.update(chosen="fixed", reason=(
            f"no pause below {FIXED_REL_DB:g} dB and the frame levels form no separate quiet class ({share} of the "
            f"frames under the Otsu split at {split['rel_db']:g} dB, classes {split['sep_db']} dB apart; a breath class "
            f"needs {AUTO_MIN_SHARE * 100:.0f}-{AUTO_MAX_SHARE * 100:.0f}% of the frames, >= {AUTO_MIN_SEP:g} dB apart, "
            f"and a split above {FIXED_REL_DB:g} dB). The reciter probably joins the verses without a breath (wasl), "
            f"so {FIXED_REL_DB:g} dB was kept and verse boundaries come from the word timing; if you hear a breath, "
            f"measure it and pass --rel-db with a number"))
    else:
        info.update(chosen="otsu", reason=(
            f"no pause below {FIXED_REL_DB:g} dB, and the frame levels form two classes ({split['quiet_share'] * 100:.0f}% "
            f"of the frames under the split, {split['sep_db']} dB apart): a reverberant or noisy recording, so the Otsu "
            f"split ({split['rel_db']:g} dB) was used"))
    return info


def find_pauses(samples, sr: int, min_dur: float = 0.30, rel_db=FIXED_REL_DB, frame: float = 0.05) -> dict:
    """Stretches whose frame RMS stays below peak + rel_db for at least min_dur seconds. kind: lead, gap or tail.
    rel_db may be "auto" (auto_choice: the Otsu split or the fixed -22 dB, with the reason in rep["auto"])."""
    auto = isinstance(rel_db, str)
    if auto and rel_db != "auto":
        raise Fail(1, f"--rel-db must be a negative number or auto, not {rel_db!r}")
    if not auto and rel_db >= 0:
        raise Fail(1, "--rel-db must be negative (dB below the loudest frame)")
    db, fs, duration = _frame_db(samples, sr, frame)
    n = len(db)
    peak = float(db.max())
    choice = None
    if auto:
        choice = auto_choice(db, peak, fs, duration, min_dur)
        rel_db = choice["otsu_rel_db"] if choice["chosen"] == "otsu" else FIXED_REL_DB
    thr = peak + rel_db
    quiet = db < thr
    pauses = _stretches(quiet, fs, duration, min_dur)
    loud = _numpy().flatnonzero(~quiet)
    last = int(loud[-1])
    speech = [r3(int(loud[0]) * fs), r3(duration if last == n - 1 else (last + 1) * fs)]
    gaps = [p for p in pauses if p["kind"] == "gap"]
    first = int(round(gaps[-1]["end"] / fs)) if gaps else int(loud[0])
    voice_end = r3(min(speech[1], voice_end_of(db, fs, thr, first, last + 1, duration)))
    rep = {"schema": SCHEMA_PAUSES, "duration": r3(duration), "sample_rate": int(sr), "frame": r3(fs),
           "min": float(min_dur), "rel_db": float(rel_db), "rel_db_mode": "auto" if auto else "fixed",
           "peak_db": round(peak, 1), "threshold_db": round(thr, 1), "speech": speech, "voice_end": voice_end,
           "pauses": pauses}
    if choice:
        rep["auto"] = choice
    if peak < -60:
        rep["warning"] = f"the loudest frame is {peak:.1f} dBFS: the audio is nearly silent"
    elif auto and choice["chosen"] == "fixed" and not choice["fixed_gaps"]:
        rep["warning"] = choice["reason"]
    elif not auto and not _gap_count(pauses):
        split = otsu_split(db, peak)
        if split["two_class"] and split["rel_db"] > rel_db:
            rep["hint"] = (f"no pause below {rel_db:g} dB, and the frame levels form two classes: the quiet stretches of "
                           f"this recording sit higher (room noise or reverb); try --rel-db auto (about "
                           f"{split['rel_db']:g} dB here)")
        else:
            rep["hint"] = (f"no pause below {rel_db:g} dB, and the frame levels form no separate quiet class: the "
                           f"reciter probably joins the verses without a breath (wasl), so --rel-db auto would keep "
                           f"{FIXED_REL_DB:g} dB too. align places such boundaries from the word timing; if you hear a "
                           f"breath, measure it and pass --rel-db with a number")
    return rep


def otsu_pauses(rep) -> bool:
    """True when the report's pauses come from the Otsu split: soft pauses that never split a matched word."""
    return bool(rep) and rep.get("rel_db_mode") == "auto" and (rep.get("auto") or {}).get("chosen") == "otsu"


def pauses_text(rep: dict) -> str:
    mode = " auto" if rep.get("rel_db_mode") == "auto" else ""
    out = [f"dur {rep['duration']:.3f} peak {rep['peak_db']:.1f} dB threshold {rep['threshold_db']:.1f} dB "
           f"(rel{mode} {rep['rel_db']:g}, min {rep['min']:.2f} s, frame {rep['frame']:.2f} s)",
           f"speech {rep['speech'][0]:.2f}-{rep['speech'][1]:.2f}"]
    ve = rep.get("voice_end")
    if ve is not None and ve < rep["speech"][1] - 0.025:
        out[-1] += f", voice ends {ve:.2f} (the level falls {TAIL_DROP_DB:g} dB under its final level; reverb after)"
    for p in rep["pauses"]:
        label = "pause" if p["kind"] == "gap" else p["kind"]
        out.append(f"{label:5} {p['start']:.2f}-{p['end']:.2f} ({p['dur']:.2f} s)")
    for key in ("warning", "hint"):
        if rep.get(key):
            out.append(f"{key}: {rep[key]}")
    return "\n".join(out)


def rel_db_arg(text: str):
    if str(text).strip().lower() == "auto":
        return "auto"
    try:
        return float(text)
    except ValueError:
        raise argparse.ArgumentTypeError("a negative number of dB (e.g. -22) or auto")


def pauses_for_align(samples, sr, min_dur, rel_db, frame, boundaries_needed: int):
    """The fixed threshold (-22 dB unless given). When it is left at its default and finds fewer pauses between words
    than there are verse boundaries, the automatic threshold is used only if auto_choice accepts the Otsu split (no
    pause at -22 dB and two classes of frame levels: a reverberant recording). Fewer pauses than boundaries alone is
    no reason: a reciter who joins the verses without a breath (wasl) gives exactly that, and a split through his
    voice finds dozens of false pauses inside words. The note says what was decided and why."""
    rep = find_pauses(samples, sr, min_dur, FIXED_REL_DB if rel_db is None else rel_db, frame)
    gaps = _gap_count(rep["pauses"])
    note = None
    if rel_db is None and gaps < boundaries_needed:
        alt = find_pauses(samples, sr, min_dur, "auto", frame)
        alt_gaps = _gap_count(alt["pauses"])
        if alt["auto"]["chosen"] == "otsu" and alt_gaps > gaps:
            note = (f"{FIXED_REL_DB:g} dB found {gaps} pause(s) for {boundaries_needed} verse boundaries, so the "
                    f"automatic threshold was used and found {alt_gaps}: {alt['auto']['reason']}. These soft pauses "
                    f"never split a word whose recognised time covers them")
            rep = alt
        else:
            note = (f"{FIXED_REL_DB:g} dB found {gaps} pause(s) for {boundaries_needed} verse boundaries; the automatic "
                    f"threshold was not used: {alt['auto']['reason']}")
    rep.pop("hint", None)
    return rep, note


def cmd_pauses(a) -> int:
    x, sr, decoder = decode_audio(a.audio)
    rep = find_pauses(x, sr, a.min, a.rel_db, a.frame)
    rep = {"schema": rep.pop("schema"), "audio": str(a.audio), "sha256": sha256_file(a.audio), "decoder": decoder, **rep}
    if a.out:
        write_json(a.out, rep)
    print(json.dumps(rep, ensure_ascii=False, indent=1) if a.json else pauses_text(rep))
    return 0


def load_pauses(path) -> dict:
    rep = read_json(path, "pauses")
    if not (isinstance(rep, dict) and rep.get("schema") == SCHEMA_PAUSES and isinstance(rep.get("pauses"), list)
            and isinstance(rep.get("speech"), list) and len(rep["speech"]) == 2):
        raise Fail(1, f"{path}: expected {SCHEMA_PAUSES} from `quran_text.py pauses AUDIO --json --out FILE`")
    clean = []
    for p in rep["pauses"]:
        s, e = (_num(p.get("start")), _num(p.get("end"))) if isinstance(p, dict) else (None, None)
        if s is None or e is None or e < s:
            raise Fail(1, f"{path}: every pause needs a numeric start <= end")
        clean.append({"start": s, "end": e, "dur": r3(e - s), "kind": p.get("kind") or "gap"})
    s0, s1 = _num(rep["speech"][0]), _num(rep["speech"][1])
    if s0 is None or s1 is None:
        raise Fail(1, f"{path}: speech must be [start, end] in seconds")
    ve = _num(rep.get("voice_end"))
    out = {**rep, "pauses": sorted(clean, key=lambda p: p["start"]), "speech": [s0, s1]}
    if ve is None or not s0 < ve <= s1:
        out.pop("voice_end", None)   # older reports have none: the passage then ends at the speech end
    else:
        out["voice_end"] = ve
    return out


# ------------------------------------------------------------------ alignment

def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def word_dist(a: str, b: str, max_dist: float = 1.0, cache=None) -> float:
    """Edit distance / longer length (0 = same key, 1 = nothing shared); 1.0 at once when lengths differ too much."""
    if cache is not None and (a, b) in cache:
        return cache[(a, b)]
    longest = max(len(a), len(b), 1)
    d = 1.0 if abs(len(a) - len(b)) / longest > max_dist else levenshtein(a, b) / longest
    if cache is not None:
        cache[(a, b)] = d
    return d


def _shape_ok(can_len: int, rec_len: int, a: int, b: int) -> bool:
    """A merge or a split must not hide a missing or extra word: a long concatenation would otherwise dilute a
    wrong neighbour below the distance limit («للإن»+«سان»+«قال» is not «لِلْإِنْسَانِ»)."""
    if b > 1 and rec_len > max(can_len + 1, 1.15 * can_len):
        return False
    if a > 1 and rec_len < min(can_len - 1, 0.85 * can_len):
        return False
    return True


def dp_align(ckeys, rkeys, max_dist: float = DEFAULT_MAX_DIST, alts=None) -> list:
    """Monotonic alignment of canonical keys to recognised keys. Each op is (kind, i, j, a, b, dist) with kind 'pair'
    (canonical i..i+a ↔ recognised j..j+b), 'can' (a canonical word nobody said) or 'rec' (an extra recognised word).
    alts {i: (a, key)} lets canonical i..i+a (a word spelled out letter by letter, «الف لام ميم») also pair as a whole
    with one recognised word that is close to key («الم» written as it is): kind 'alt'."""
    alts = alts or {}
    n, m = len(ckeys), len(rkeys)
    if (n + 1) * (m + 1) > MAX_CELLS:
        raise Fail(1, f"{n} canonical x {m} recognised words is too large for one alignment; split the verses into "
                      f"smaller ranges")
    inf = float("inf")
    cost = [[inf] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    cost[0][0] = 0.0
    cache = {}
    for i in range(n + 1):
        row = cost[i]
        for j in range(m + 1):
            c = row[j]
            if c == inf:
                continue
            if i < n and c + GAP_COST < cost[i + 1][j] - 1e-12:
                cost[i + 1][j], back[i + 1][j] = c + GAP_COST, ("can", i, j, 1, 0, 1.0)
            if j < m and c + GAP_COST < row[j + 1] - 1e-12:
                row[j + 1], back[i][j + 1] = c + GAP_COST, ("rec", i, j, 0, 1, 1.0)
            for a, b in PAIR_SHAPES:
                if i + a > n or j + b > m:
                    continue
                ck, rk = "".join(ckeys[i:i + a]), "".join(rkeys[j:j + b])
                if (a, b) != (1, 1) and not _shape_ok(len(ck), len(rk), a, b):
                    continue
                d = word_dist(ck, rk, max_dist, cache)
                if d > (max_dist if (a, b) == (1, 1) else max_dist / 2.0) + 1e-12:
                    continue
                nc = c + 2.0 * d + SHAPE_PENALTY * (a + b - 2)
                if nc < cost[i + a][j + b] - 1e-12:
                    cost[i + a][j + b], back[i + a][j + b] = nc, ("pair", i, j, a, b, d)
            if i in alts and j < m and i + alts[i][0] <= n:
                a, key = alts[i]
                d = word_dist(key, rkeys[j], max_dist, cache)
                if d <= max_dist + 1e-12 and c + 2.0 * d < cost[i + a][j + 1] - 1e-12:
                    cost[i + a][j + 1], back[i + a][j + 1] = c + 2.0 * d, ("alt", i, j, a, 1, d)
    ops, i, j = [], n, m
    while i or j:
        op = back[i][j]
        ops.append(op)
        i, j = op[1], op[2]
    ops.reverse()
    return ops


def _parts(a: float, b: float, segments):
    if segments is None:
        return [(a, b)] if b > a else []
    return [(max(s, a), min(e, b)) for s, e in segments if min(e, b) > max(s, a)]


def voiced_len(a: float, b: float, segments) -> float:
    return sum(e - s for s, e in _parts(a, b, segments))


def distribute(a: float, b: float, weights, segments=None) -> list:
    """Split [a, b] among words in proportion to their weights, counting only voiced time when segments are given,
    so a pause takes no share. A word may still straddle a pause here; clip_to_segments decides its side."""
    parts = _parts(a, b, segments) or ([(a, b)] if b > a else [])
    total = sum(e - s for s, e in parts)
    wsum = float(sum(weights))
    if total <= 1e-9 or wsum <= 0:
        return [(a, a)] * len(weights)

    def at(x: float, start: bool) -> float:
        for k, (s, e) in enumerate(parts):
            span = e - s
            if x < span - 1e-12 or (x <= span + 1e-12 and (not start or k == len(parts) - 1)):
                return s + min(max(x, 0.0), span)
            x -= span
        return parts[-1][1]

    out, acc = [], 0.0
    for w in weights:
        x0, acc = acc, acc + total * w / wsum
        out.append((at(x0, True), at(min(acc, total), False)))
    return out


def load_canonical(path):
    doc = read_json(path, "verses")
    verses = doc.get("verses") if isinstance(doc, dict) else doc
    if not isinstance(verses, list) or not verses:
        raise Fail(1, f"{path}: no verses (expected {SCHEMA_VERSES} from `quran_text.py fetch`)")
    out = []
    for k, v in enumerate(verses):
        if not isinstance(v, dict) or not isinstance(v.get("text"), str) or not v["text"].strip():
            raise Fail(1, f"{path}: verse {k + 1} has no text")
        words = v.get("words") if isinstance(v.get("words"), list) and v.get("words") else split_words(v["text"])
        words = [str(w) for w in words]
        if any(not norm_ar(w) for w in words):
            raise Fail(1, f"{path}: verse {k + 1} has a word with no letters; join marks to their word")
        ayah = v.get("ayah") if isinstance(v.get("ayah"), int) else k + 1
        out.append({"surah": v.get("surah"), "ayah": ayah, "ref": v.get("ref") or (
            f"{v['surah']}:{ayah}" if v.get("surah") else str(ayah)), "ayah_ar": v.get("ayah_ar") or to_arabic_digits(ayah),
            "text": v["text"], "words": words})
    return doc, out


def load_recognised(path):
    """kosif-words/1, {"words": [...]}, a bare list or whisper segments → ([{text, key, start, end}], meta)."""
    doc = read_json(path, "words")
    raw = doc.get("words") if isinstance(doc, dict) else doc
    if isinstance(doc, dict) and raw is None and isinstance(doc.get("segments"), list):
        raw = [w for s in doc["segments"] if isinstance(s, dict) for w in (s.get("words") or [])]
    if not isinstance(raw, list):
        raise Fail(1, f"{path}: no words list (expected kosif-words/1 from montage_pro.py transcribe)")
    words = []
    for w in raw:
        if not isinstance(w, dict):
            continue
        text = w.get("word", w.get("text", w.get("w")))
        s, e = _num(w.get("start", w.get("s"))), _num(w.get("end", w.get("e")))
        if text is None or s is None:
            continue
        key = norm_ar(text)
        if not key:
            continue
        words.append({"text": str(text).strip(), "key": key, "start": s, "end": e if e is not None and e >= s else s})
    words.sort(key=lambda r: (r["start"], r["end"]))
    meta = {}
    if isinstance(doc, dict):
        src, eng = doc.get("source"), doc.get("engine")
        if isinstance(src, dict):
            meta["source"] = {k: src[k] for k in ("file", "sha256", "duration") if k in src}
        if isinstance(eng, dict):
            meta["engine"] = {k: eng[k] for k in ("name", "version", "model", "vad_filter") if k in eng}
    return words, meta


def _rate(anchors, can) -> float:
    """Median seconds per letter of the clean 1:1 matches (used only to extend past the last anchor without audio)."""
    vals = sorted((an["end"] - an["start"]) / can[i]["letters"] for i, an in enumerate(anchors)
                  if an and an["how"] == "1:1" and an["end"] > an["start"])
    if not vals:
        return 0.2
    return min(0.6, max(0.05, vals[len(vals) // 2]))


def place(can, anchors, groups, segments, rate, lower=0.0, upper=None) -> list:
    """Give every word a time. Matched words keep theirs; each run of unmatched words shares the time between its
    neighbours (or a group fence) in proportion to letter count. When that time is too short, the neighbouring
    matched words lend theirs and the whole stretch is shared by letters."""
    words = [dict(an) if an else None for an in anchors]
    for i0, i1, fa, fb in groups:
        i = i0
        while i < i1:
            if words[i] is not None:
                i += 1
                continue
            p = i
            while i < i1 and words[i] is None:
                i += 1
            q = i
            prev = p - 1 if p > i0 else None
            nxt = q if q < i1 else None
            a = words[prev]["end"] if prev is not None else fa
            b = words[nxt]["start"] if nxt is not None else fb
            letters = [can[k]["letters"] for k in range(p, q)]
            if a is None and b is None:
                raise Fail(1, "no recognised word matched the verse text, so nothing anchors the timing; check that "
                              "words.json belongs to this recitation, or pass --audio to place words by measured pauses")
            how = "between" if a is not None and b is not None else "extrapolated"
            if a is None:
                a = max(lower, b - rate * sum(letters))
            if b is None:
                b = a + rate * sum(letters)
                if upper is not None:
                    b = min(b, max(a, upper))
            b = max(a, b)
            idx, weights, shared = list(range(p, q)), list(letters), set()
            need = sum(max(MIN_WORD, MIN_LETTER * n) for n in letters)
            if voiced_len(a, b, segments) < need:
                if prev is not None:
                    a = words[prev]["start"]
                    idx.insert(0, prev)
                    weights.insert(0, can[prev]["letters"])
                    shared.add(prev)
                if nxt is not None:
                    b = words[nxt]["end"]
                    idx.append(nxt)
                    weights.append(can[nxt]["letters"])
                    shared.add(nxt)
            for k, (s, e) in zip(idx, distribute(a, b, weights, segments)):
                if k in shared:
                    words[k]["start"], words[k]["end"], words[k]["shared"] = s, e, True
                else:
                    words[k] = {"start": s, "end": e, "source": "interpolated", "how": how}
    return words


def clip_to_segments(words, segments) -> list:
    """Keep each word inside the voiced segment that holds most of it, so no word crosses a pause."""
    seg_of = []
    for k, w in enumerate(words):
        best, bi = 0.0, None
        for si, (s, e) in enumerate(segments):
            ov = min(e, w["end"]) - max(s, w["start"])
            if ov > best + 1e-9:
                best, bi = ov, si
        if bi is None:
            bi = min(range(len(segments)), key=lambda si: min(abs(segments[si][0] - w["start"]),
                                                              abs(segments[si][1] - w["start"])))
            s, e = segments[bi]
            w["start"] = w["end"] = min(max(w["start"], s), e)
        else:
            s, e = segments[bi]
            w["start"], w["end"] = max(w["start"], s), min(w["end"], e)
        seg_of.append(bi)
    return seg_of


def spoken_letters(surah, ayah, index: int, key: str):
    """The letter names a reciter says for a muqatta'at opening («الم» → الف لام ميم), or None for any other word."""
    if index or (surah, ayah) not in MUQATTAAT or not key or any(ch not in LETTER_NAMES for ch in key):
        return None
    return [LETTER_NAMES[ch] for ch in key]


def formula_hits(keys, names, max_dist: float) -> set:
    """Positions in keys that belong to a run of two or more consecutive words of one of the named formulas, in
    their order (a formula word may be missing: whisper drops words)."""
    hits = set()
    for name in names:
        f = FORMULAS[name]
        for start in range(len(keys)):
            run, fi, k = [], 0, start
            while k < len(keys):
                found = next((fj for fj in range(fi, len(f)) if word_dist(keys[k], f[fj], max_dist) <= max_dist), None)
                if found is None:
                    break
                run.append(k)
                fi, k = found + 1, k + 1
            if len(run) >= 2:
                hits.update(run)
    return hits


def outside_speech(near, rec, anchor, unmatched_letters: int, gaps, names, max_dist: float, backward: bool):
    """Of the extra recognised words before the first matched word (or after the last), ordered from that word outward
    (near[0] is next to it), which are speech outside the verses: the isti'adha, the basmala, «صدق الله العظيم». The
    rest are taken as mis-hearings of the unmatched verse words between them and the match («يقول» for «أنكم
    تنطقون»). → (outside, why). An extra word is outside, with everything beyond it, when a measured pause separates it
    from the word on its inner side, when it is part of a known formula, or when the extras carry far more letters than
    the unmatched verse words could account for."""
    if not near:
        return [], None
    if unmatched_letters == 0:
        return list(near), "the verse's own edge word was matched"

    def mid(r):
        return (r["start"] + r["end"]) / 2.0

    cut, why = None, None
    inner = (anchor[0] + anchor[1]) / 2.0
    for q, j in enumerate(near):
        here = mid(rec[j])
        lo, hi = min(here, inner), max(here, inner)
        if any(lo < (p["start"] + p["end"]) / 2.0 < hi for p in gaps):
            cut, why = q, "a measured pause separates it from the verse"
            break
        inner = here
    keys = [rec[j]["key"] for j in near]   # formulas are matched in time order: near runs backwards before a verse
    hits = formula_hits(keys[::-1] if backward else keys, names, max_dist)
    hits = {len(near) - 1 - h for h in hits} if backward else hits
    if hits and (cut is None or min(hits) < cut):
        cut, why = min(hits), "it is a known formula (" + " / ".join(names) + ")"
    letters = [len(rec[j]["key"]) for j in near]
    if sum(letters) > LETTER_EXCESS * unmatched_letters + 4:
        allow, acc = 1.5 * unmatched_letters + 2, 0
        for q, c in enumerate(letters):
            acc += c
            if acc > allow:
                if cut is None or q < cut:
                    cut, why = q, (f"{sum(letters)} letters against {unmatched_letters} in the unmatched verse words: "
                                   f"far more than a mis-hearing")
                break
    if cut is None:
        return [], None
    return list(near[cut:]), why


def make_segments(gaps, s0: float, s1: float) -> list:
    segments, t = [], s0
    for p in gaps:
        if p["start"] > t:
            segments.append((t, float(p["start"])))
        t = max(t, float(p["end"]))
    if s1 > t:
        segments.append((t, s1))
    return segments or [(s0, max(s0, s1))]


def dip_onset(levels, t_now: float, lo: float, hi: float):
    """The onset after the best clear dip of the level contour in [lo, hi] near t_now, or None. A dip is a local
    minimum DIP_PROM dB under both sides; it must sit DIP_MARGIN dB under the level at t_now, and its depth minus
    DIP_DIST_DB per second of distance must reach DIP_MIN_SCORE. The onset is where its valley ends."""
    db, hop, off = levels["db"], levels["hop"], levels["offset"]
    nfr = len(db)

    def at(t):
        return int(round((t - off) / hop))

    k0, k1 = max(1, at(lo)), min(nfr - 2, at(hi))
    around = db[max(0, at(t_now - 0.06)):max(0, at(t_now + 0.06)) + 1]
    if k1 <= k0 or not len(around):
        return None
    ref = float(around.min())
    side = max(1, int(round(DIP_SIDE / hop)))
    best = None
    for k in range(k0, k1 + 1):
        v = float(db[k])
        if not (v <= db[k - 1] and v < db[k + 1]):
            continue
        if min(float(db[max(0, k - side):k].max()), float(db[k + 1:k + 1 + side].max())) - v < DIP_PROM:
            continue
        depth = ref - v
        t = off + k * hop
        score = depth - DIP_DIST_DB * abs(t - t_now)
        if depth >= DIP_MARGIN and score >= DIP_MIN_SCORE and (best is None or score > best[0]):
            best = (score, k, depth)
    if best is None:
        return None
    score, k, depth = best
    e = k
    while e + 1 < nfr and db[e + 1] <= db[k] + DIP_VALLEY and off + (e + 1) * hop <= hi:
        e += 1
    return {"t": off + e * hop, "dip": off + k * hop, "depth_db": round(depth, 1), "score": round(score, 1)}


def assign_segments(cur, K: int, dist):
    """A monotone assignment of words (current segment positions cur, 0..K-1) to K segments that gives every segment
    at least one word and moves as few words as possible (ties: the nearest in time, dist[j][q]). None if impossible."""
    m, inf = len(cur), float("inf")
    if m < K or K == 0:
        return None
    cost = [[inf] * K for _ in range(m)]
    back = [[None] * K for _ in range(m)]
    cost[0][0] = (cur[0] != 0) * (1.0 + 1e-3 * dist[0][0])
    for j in range(1, m):
        for q in range(K):
            step = (cur[j] != q) * (1.0 + 1e-3 * dist[j][q])
            for pq in (q, q - 1):
                if pq >= 0 and cost[j - 1][pq] + step < cost[j][q] - 1e-12:
                    cost[j][q], back[j][q] = cost[j - 1][pq] + step, pq
    if cost[m - 1][K - 1] == inf:
        return None
    out, q = [0] * m, K - 1
    for j in range(m - 1, -1, -1):
        out[j] = q
        if j:
            q = back[j][q]
    return out


def align(verses, rec, pauses=None, max_dist: float = DEFAULT_MAX_DIST, duration=None, levels=None) -> dict:
    """Canonical verses + recognised words (+ a pauses report, + a level contour for the dip refinement) →
    {verses, stats}. See the module docstring."""
    can, vrange, toks, alts = [], [], [], {}
    for vi, v in enumerate(verses):
        i0 = len(can)
        for wi, w in enumerate(v["words"]):
            key = norm_ar(w)
            ci = len(can)
            can.append({"text": w, "key": key, "letters": max(1, len(key)), "v": vi})
            spoken = spoken_letters(v.get("surah"), v.get("ayah"), wi, key)
            if spoken:
                alts[len(toks)] = (len(spoken), key)   # «الم» may also be written as it is
                can[ci]["spoken"] = len(spoken)
            for part in spoken or [key]:
                toks.append((ci, part))
        vrange.append((i0, len(can)))
    n = len(can)
    warnings, demoted = [], []
    ops = dp_align([t[1] for t in toks], [r["key"] for r in rec], max_dist, alts)

    tanch, paired, extra = [None] * len(toks), set(), []
    for kind, i, j, a, b, d in ops:
        if kind == "rec":
            extra.append(j)
        if kind not in ("pair", "alt"):
            continue
        rs = rec[j:j + b]
        info = {"source": "matched", "sim": r3(1.0 - d), "rj": list(range(j, j + b)), "rs": rs[0]["start"],
                "re": max(rs[-1]["end"], rs[0]["start"])}
        if a == 1:
            tanch[i] = {"start": rs[0]["start"], "end": info["re"], "how": "1:1" if b == 1 else "split", **info}
        else:
            spans = distribute(rs[0]["start"], rs[0]["end"], [len(toks[i + k][1]) or 1 for k in range(a)])
            for k in range(a):
                tanch[i + k] = {"start": spans[k][0], "end": spans[k][1], "how": "alt" if kind == "alt" else "merge",
                                **info}
        paired.update(range(j, j + b))
    anchors = [None] * n
    for t, an in enumerate(tanch):
        if an is None:
            continue
        ci, cur = toks[t][0], anchors[toks[t][0]]
        if cur is None:
            anchors[ci] = dict(an)
            continue
        cur.update(start=min(cur["start"], an["start"]), end=max(cur["end"], an["end"]), rs=min(cur["rs"], an["rs"]),
                   re=max(cur["re"], an["re"]), sim=min(cur["sim"], an["sim"]), how=an["how"] if an["how"] == "alt"
                   else "spelled", rj=sorted(set(cur["rj"]) | set(an["rj"])))
    for ci, an in enumerate(anchors):
        if an:
            an["heard"] = " ".join(rec[j]["text"] for j in an["rj"])
            if an["how"] == "alt":
                an["how"] = "1:1"
            elif can[ci].get("spoken", 1) > 1:
                an["how"] = "spelled"

    def demote(i, why):
        demoted.append({"word": can[i]["text"], "heard": anchors[i]["heard"], "why": why})
        anchors[i] = None

    prev_end = -float("inf")
    for i in range(n):
        an = anchors[i]
        if an is None:
            continue
        if an["start"] < prev_end - EPS:
            an["start"] = prev_end
            if an["end"] < an["start"] + EPS:
                demote(i, "its recognised time runs backwards")
                continue
        prev_end = an["end"]

    rate = _rate(anchors, can)
    segments, boundaries, used_pauses, speech, voice_end = None, [], [], None, None
    stretched, refined, ignored, outside = [], [], [], []
    if pauses:
        used_pauses = list(pauses["pauses"])
        gaps = [p for p in used_pauses if p.get("kind") == "gap"]
        s0, s1 = float(pauses["speech"][0]), float(pauses["speech"][1])
        speech = [r3(s0), r3(s1)]
        ve = _num(pauses.get("voice_end"))
        s1v = ve if ve is not None and s0 < ve < s1 else s1   # the reverb after the voice holds no word
        voice_end = r3(s1v)
        segments = make_segments(gaps, s0, s1v)
        for i in range(n):
            if anchors[i] and voiced_len(anchors[i]["start"], anchors[i]["end"], segments) < 0.02:
                demote(i, "its recognised time lies in silence")

        def voiced(r):
            return voiced_len(r["start"], r["end"], segments) >= max(0.05, 0.5 * (r["end"] - r["start"]))

        def pick(cands, t_b):
            return max(cands, key=lambda p: (p["dur"] / (1.0 + abs((p["start"] + p["end"]) / 2.0 - t_b)), -p["start"]))

        anchored = [i for i in range(n) if anchors[i]]
        first_pair = min(paired) if paired else None
        last_pair = max(paired) if paired else None
        lead = [j for j in extra if first_pair is not None and j < first_pair and voiced(rec[j])]
        trail = [j for j in extra if last_pair is not None and j > last_pair and voiced(rec[j])]
        pre, post = [], []
        if anchored and lead:
            a0 = anchors[anchored[0]]
            pre, why = outside_speech(lead[::-1], rec, (a0["start"], a0["end"]),
                                      sum(can[i]["letters"] for i in range(anchored[0])), gaps, LEAD_FORMULAS, max_dist,
                                      backward=True)
            if pre:
                outside.append({"side": "before", "words": " ".join(rec[j]["text"] for j in sorted(pre)), "why": why})
        if anchored and trail:
            a1 = anchors[anchored[-1]]
            post, why = outside_speech(trail, rec, (a1["start"], a1["end"]),
                                       sum(can[i]["letters"] for i in range(anchored[-1] + 1, n)), gaps,
                                       TRAIL_FORMULAS, max_dist, backward=False)
            if post:
                outside.append({"side": "after", "words": " ".join(rec[j]["text"] for j in sorted(post)), "why": why})

        start0 = s0
        if pre:
            last = rec[max(pre)]
            hi = anchors[anchored[0]]["end"]
            cands = [p for p in gaps if p["start"] >= last["start"] - EPS and p["end"] <= hi + EPS]
            best = pick(cands, last["end"]) if cands else None
            start0 = float(best["end"]) if best else max(s0, last["end"])
            boundaries.append({"before": verses[0]["ref"], "after": "extra speech", "expected": r3(last["end"]),
                               "pause": [best["start"], best["end"]] if best else None, "snapped": bool(best)})
        end_last = s1v
        if post:
            first = rec[min(post)]
            lo = anchors[anchored[-1]]["start"]
            cands = [p for p in gaps if p["start"] >= max(lo, start0) - EPS and p["end"] <= first["end"] + EPS]
            best = pick(cands, first["start"]) if cands else None
            end_last = float(best["start"]) if best else min(s1v, max(start0, first["start"]))
            boundaries.append({"after": verses[-1]["ref"], "before": "extra speech", "expected": r3(first["start"]),
                               "pause": [best["start"], best["end"]] if best else None, "snapped": bool(best)})
        for i in anchored:   # a matched word inside the extra speech is a coincidence, not the verse
            if anchors[i] and (anchors[i]["end"] <= start0 + EPS or anchors[i]["start"] >= end_last - EPS):
                demote(i, "its recognised time lies in the speech before or after the verses")

        prov = place(can, anchors, [(0, n, start0, end_last)], segments, rate)
        anchored = [i for i in range(n) if anchors[i]]
        cuts, used = [], start0
        for k in range(len(verses) - 1):
            i_last, i_next = vrange[k][1] - 1, vrange[k + 1][0]
            lo = next((anchors[i]["start"] for i in reversed(anchored) if i <= i_last), start0)
            hi = next((anchors[i]["end"] for i in anchored if i >= i_next), end_last)
            t_b = (prov[i_last]["end"] + prov[i_next]["start"]) / 2.0
            cands = [p for p in gaps if p["start"] >= max(lo, used) - EPS and p["end"] <= min(hi, end_last) + EPS]
            best = pick(cands, t_b) if cands else None
            if best:
                cut = (float(best["start"]), float(best["end"]))
            else:
                t = min(max(t_b, used), end_last)
                cut = (t, t)
                warnings.append(f"no pause of at least the minimum length between {verses[k]['ref']} and "
                                f"{verses[k + 1]['ref']}; the boundary was placed at {t:.2f} s from the word timing")
            used = cut[1]
            cuts.append(cut)
            boundaries.append({"after": verses[k]["ref"], "before": verses[k + 1]["ref"], "expected": r3(t_b),
                               "pause": [best["start"], best["end"]] if best else None, "snapped": bool(best)})
        if otsu_pauses(pauses):
            # Soft pauses (the Otsu split of a reverberant recording) may be dips inside the voice: one that lies
            # inside a matched word's recognised time is not a pause, unless it is a verse boundary.
            cut_set = {c for c in cuts if c[1] > c[0]}
            keep = []
            for p in gaps:
                inside = None
                if (float(p["start"]), float(p["end"])) not in cut_set:
                    inside = next((i for i in anchored if anchors[i] and anchors[i]["rs"] < p["start"] - SOFT_MARGIN
                                   and anchors[i]["re"] > p["end"] + SOFT_MARGIN), None)
                if inside is None:
                    keep.append(p)
                else:
                    ignored.append({"start": p["start"], "end": p["end"], "inside": can[inside]["text"]})
            if ignored:
                segments = make_segments(keep, s0, s1v)
                gone = {(q["start"], q["end"]) for q in ignored}
                used_pauses = [p for p in used_pauses if (p["start"], p["end"]) not in gone]
        fences = []
        for k in range(len(verses)):
            fa = start0 if k == 0 else cuts[k - 1][1]
            fb = end_last if k == len(verses) - 1 else cuts[k][0]
            fences.append((fa, max(fa, fb)))
        for i in range(n):
            if anchors[i]:
                fa, fb = fences[can[i]["v"]]
                anchors[i]["start"] = max(anchors[i]["start"], fa)
                anchors[i]["end"] = min(anchors[i]["end"], fb)
                if anchors[i]["end"] - anchors[i]["start"] < 0.02:
                    demote(i, "its recognised time lies outside its verse")
        groups = [(vrange[k][0], vrange[k][1], fences[k][0], fences[k][1]) for k in range(len(verses))]
        words = place(can, anchors, groups, segments, rate)
        for w in words:
            if w["source"] == "matched" and not w.get("shared"):
                w["rt"] = (w["start"], w["end"])   # the recogniser's time, inside the verse
        seg_of = clip_to_segments(words, segments)
        extras = [rec[j] for j in extra if voiced(rec[j])]

        def extra_between(t0, t1):
            return any(t0 + EPS < (r["start"] + r["end"]) / 2.0 < t1 - EPS for r in extras)

        def fence_segments(k):
            fa, fb = fences[k]
            return [si for si, (s, e) in enumerate(segments) if min(e, fb) - max(s, fa) >= MIN_SEGMENT - EPS]

        # Every voiced segment inside a verse holds a word: whisper is often late after a breath, so a short segment
        # at the start of a verse (or at its end) is left empty. Words move to fill it, as few as possible.
        for k in range(len(verses)):
            i0, i1 = vrange[k]
            segs = fence_segments(k)
            if not segs or i1 <= i0:
                continue
            pos = {si: q for q, si in enumerate(segs)}
            cur = [pos.get(seg_of[i], min(range(len(segs)), key=lambda q: abs(segs[q] - seg_of[i])))
                   for i in range(i0, i1)]
            if len(set(cur)) == len(segs):
                continue
            dist = [[max(0.0, segments[si][0] - words[i]["end"], words[i]["start"] - segments[si][1]) for si in segs]
                    for i in range(i0, i1)]
            plan = assign_segments(cur, len(segs), dist)
            if plan is None:
                continue
            moved = {i0 + j for j in range(i1 - i0) if plan[j] != cur[j]}
            for q, si in enumerate(segs):
                members = [i0 + j for j in range(i1 - i0) if plan[j] == q]
                if not any(i in moved for i in members):
                    continue
                fa, fb = fences[k]
                local = [None] * n
                for i in members:
                    if i not in moved:
                        local[i] = dict(words[i])
                got = place(can, local, [(members[0], members[-1] + 1, max(segments[si][0], fa),
                                          min(segments[si][1], fb))], [segments[si]], rate)
                for i in members:
                    words[i]["start"], words[i]["end"] = got[i]["start"], got[i]["end"]
                    if i in moved:
                        words[i]["moved"] = True
                    elif got[i].get("shared"):
                        words[i]["shared"] = True
                    seg_of[i] = si

        def snap_start(i, ns):
            w = words[i]
            old = w["start"]
            w["start"] = ns
            w.setdefault("snapped", []).append("start")
            w.setdefault("snap", {})["start"] = r3(ns - old)
            if old - ns > SNAP_RESHARE:
                note = {"word": can[i]["text"], "pulled_back": r3(old - ns), "to": r3(ns)}
                j = i + 1
                slow = (w["end"] - ns) / can[i]["letters"] > RESHARE_RATE * rate
                if slow and j < n and seg_of[j] == seg_of[i] and can[j]["v"] == can[i]["v"] \
                        and words[j]["end"] > w["end"] + EPS:
                    (w["start"], w["end"]), (words[j]["start"], words[j]["end"]) = distribute(
                        ns, words[j]["end"], [can[i]["letters"], can[j]["letters"]])
                    w["reshared"] = words[j]["reshared"] = True
                    note["reshared_with"] = can[j]["text"]
                stretched.append(note)

        def snap_end(i, ne):
            w = words[i]
            w.setdefault("snap", {})["end"] = r3(ne - w["end"])
            w["end"] = ne
            w.setdefault("snapped", []).append("end")

        for si, (s, e) in enumerate(segments):
            members = [i for i in range(n) if seg_of[i] == si]
            if not members:
                continue
            f, last = members[0], members[-1]
            ns = max(s, fences[can[f]["v"]][0])
            if ns < words[f]["start"] - EPS and (f == 0 or words[f - 1]["end"] <= ns + EPS) \
                    and not extra_between(ns, words[f]["start"]):
                snap_start(f, ns)
            ne = min(e, fences[can[last]["v"]][1])
            if ne > words[last]["end"] + EPS and (last == n - 1 or words[last + 1]["start"] >= ne - EPS) \
                    and not extra_between(words[last]["end"], ne):
                snap_end(last, ne)
        for k, (fa, fb) in enumerate(fences):   # a verse cut without a pause (wasl) lies inside a segment
            f, last = vrange[k][0], vrange[k][1] - 1
            ns = max(fa, segments[seg_of[f]][0])
            if ns < words[f]["start"] - EPS and (f == 0 or words[f - 1]["end"] <= ns + EPS) \
                    and not extra_between(ns, words[f]["start"]):
                snap_start(f, ns)
            ne = min(fb, segments[seg_of[last]][1])
            if ne > words[last]["end"] + EPS and (last == n - 1 or words[last + 1]["start"] >= ne - EPS) \
                    and not extra_between(words[last]["end"], ne):
                snap_end(last, ne)

        if levels is not None:
            # Whisper's start of a long word (or of the word after one) is often off by a second or more in a slow
            # recitation: it gives the madd of one word to its neighbour. Move it to the onset after the deepest clear
            # consonant dip nearby, never across a pause and never squeezing either word below half the usual rate.
            def min_len(i):
                return max(MIN_WORD, DIP_MIN_SHARE * rate * can[i]["letters"])

            def heard_time(w):   # the recogniser's own time for this word, unless it was re-shared or moved
                return w.get("rt") if w["source"] == "matched" and not (w.get("reshared") or w.get("moved")) else None

            for si, (s, e) in enumerate(segments):
                members = [i for i in range(n) if seg_of[i] == si]
                for q in range(1, len(members)):
                    i, p = members[q], members[q - 1]
                    w, pw = words[i], words[p]
                    if can[i]["v"] != can[p]["v"] or abs(pw["end"] - w["start"]) > 0.02:
                        continue
                    own_long = w["end"] - w["start"] > LONG_WORD
                    if not own_long and (pw["end"] - pw["start"] <= LONG_WORD or heard_time(w)):
                        continue   # a word long only because of its neighbour keeps its own heard start
                    lo = max(w["start"] - DIP_WINDOW, pw["start"] + min_len(p), s)
                    hi = min(w["start"] + DIP_WINDOW, w["end"] - min_len(i), e)
                    if heard_time(pw):   # never into a matched neighbour's recognised time («مِثْلَ» keeps its end)
                        lo = max(lo, heard_time(pw)[1] - 0.05)
                    d = dip_onset(levels, w["start"], lo, hi) if hi - lo >= 0.05 else None
                    if d is None or abs(d["t"] - w["start"]) < 0.03:
                        continue
                    old = w["start"]
                    w["start"] = pw["end"] = d["t"]
                    w["dip"] = {"from": r3(old), "shift": r3(d["t"] - old), "dip_at": r3(d["dip"]),
                                "depth_db": d["depth_db"]}
                    w["was"], w["how"] = w["how"], "dip-snapped"
                    refined.append({"word": can[i]["text"], "from": r3(old), "to": r3(d["t"]),
                                    "shift": r3(d["t"] - old), "depth_db": d["depth_db"]})
        for k in range(len(verses)):
            held = {seg_of[i] for i in range(*vrange[k])}
            for si in fence_segments(k):
                if si not in held:
                    s, e = segments[si]
                    warnings.append(f"the voiced stretch {max(s, fences[k][0]):.2f}-{min(e, fences[k][1]):.2f} s "
                                    f"inside {verses[k]['ref']} holds no word; check the timing there")
        for note in stretched:
            warnings.append(f"{note['word']}: start pulled back {note['pulled_back']:.2f} s to {note['to']:.2f} s (the "
                            f"recogniser was late after the pause)" + (
                                f"; it and {note['reshared_with']} were re-shared by letter count"
                                if note.get("reshared_with") else ""))
    else:
        if not any(anchors):
            raise Fail(1, "no recognised word matched the verse text, so nothing anchors the timing; check that "
                          "words.json belongs to this recitation, or pass --audio to place words by measured pauses")
        words = place(can, anchors, [(0, n, None, None)], None, rate, 0.0, duration)

    t = -float("inf")
    for w in words:
        w["start"] = max(w["start"], t)
        w["end"] = max(w["end"], w["start"])
        t = w["end"]
    empty = [can[i]["text"] for i, w in enumerate(words) if w["end"] - w["start"] < 0.01]
    if empty:
        warnings.append(f"{len(empty)} word(s) got no time ({' '.join(empty[:6])}); check the audio and words.json")

    out_verses = []
    for k, v in enumerate(verses):
        ws = []
        for i in range(*vrange[k]):
            w = words[i]
            rec_w = {"text": can[i]["text"], "start": r3(w["start"]), "end": r3(w["end"]), "source": w["source"],
                     "how": w["how"]}
            for key in ("was", "sim", "heard", "snapped", "snap", "dip"):
                if key in w:
                    rec_w[key] = w[key]
            for key in ("shared", "reshared", "moved"):
                if w.get(key):
                    rec_w[key] = True
            ws.append(rec_w)
        out_verses.append({"n": v["ayah"], "surah": v.get("surah"), "ayah": v["ayah"], "ref": v["ref"],
                           "ayah_ar": v["ayah_ar"], "text": v["text"], "start": ws[0]["start"], "end": ws[-1]["end"],
                           "words": ws})
    flat = [w for v in out_verses for w in v["words"]]
    stats = {"canonical_words": n, "recognised_words": len(rec),
             "matched": sum(w["source"] == "matched" for w in flat),
             "interpolated": sum(w["source"] == "interpolated" for w in flat),
             "merged": sum(w.get("was", w["how"]) == "merge" for w in flat),
             "split": sum(w.get("was", w["how"]) == "split" for w in flat),
             "spelled": sum(w.get("was", w["how"]) == "spelled" for w in flat),
             "shared": sum(bool(w.get("shared")) for w in flat), "demoted": demoted,
             "unmatched_recognised": [{"text": rec[j]["text"], "start": r3(rec[j]["start"]), "end": r3(rec[j]["end"])}
                                      for j in extra],
             "outside_speech": outside, "boundaries": boundaries, "stretched": stretched, "dip_snapped": refined,
             "ignored_pauses": ignored, "warnings": warnings}
    return {"verses": out_verses, "pauses": used_pauses, "speech": speech, "voice_end": voice_end, "stats": stats}


def cmd_align(a) -> int:
    if a.audio and a.pauses:
        raise Fail(1, "give --audio or --pauses, not both")
    vdoc, verses = load_canonical(a.verses)
    rec, wmeta = load_recognised(a.words)
    pa, audio, levels = None, None, None
    notes = []
    if a.audio:
        x, sr, decoder = decode_audio(a.audio)
        pa, note = pauses_for_align(x, sr, a.min, a.rel_db, a.frame, len(verses) - 1)
        if note:
            notes.append(note)
        if not a.no_dip_snap:
            levels = level_contour(x, sr)
        audio = {"path": str(a.audio), "sha256": sha256_file(a.audio), "duration": pa["duration"], "decoder": decoder}
        wsha = (wmeta.get("source") or {}).get("sha256")
        if wsha and wsha != audio["sha256"]:
            notes.append(f"words.json was made from a different file (sha256 {wsha[:12]}…, audio {audio['sha256'][:12]}…); "
                         f"check that both are the same recitation")
    elif a.pauses:
        pa = load_pauses(a.pauses)
    duration = pa.get("duration") if pa else (wmeta.get("source") or {}).get("duration")
    res = align(verses, rec, pa, a.max_dist, duration, levels)
    res["stats"]["warnings"] = notes + res["stats"]["warnings"]
    doc = {"schema": SCHEMA_TIMING,
           "verses_file": {"path": str(a.verses), "sha256": sha256_file(a.verses),
                           "edition": vdoc.get("edition") if isinstance(vdoc, dict) else None},
           "words_file": {"path": str(a.words), "sha256": sha256_file(a.words), **wmeta},
           "audio": audio, "duration": duration,
           "params": {"max_dist": a.max_dist, "min": pa.get("min") if pa else None,
                      "rel_db": pa.get("rel_db") if pa else None, "rel_db_mode": pa.get("rel_db_mode") if pa else None,
                      "auto": pa.get("auto") if pa else None, "dip_snap": levels is not None},
           **res}
    if a.pauses:
        doc["pauses_file"] = {"path": str(a.pauses), "sha256": sha256_file(a.pauses)}
    write_json(a.out, doc)
    for v in res["verses"]:
        m = sum(w["source"] == "matched" for w in v["words"])
        print(f"{v['ref']:>7}  {v['start']:7.3f} → {v['end']:7.3f}   {len(v['words'])} words, {m} matched")
        for w in v["words"]:
            print(f"         {w['start']:7.3f} {w['end']:7.3f}  {w['source']:12} {w['text']}")
    st = res["stats"]
    snapped = sum(1 for b in st["boundaries"] if b["snapped"])
    for msg in st["warnings"]:
        print("warning: " + msg, file=sys.stderr)
    print(f"wrote {a.out}: {st['canonical_words']} words, {st['matched']} matched, {st['interpolated']} interpolated, "
          f"{len(st['unmatched_recognised'])} extra recognised; {snapped}/{len(st['boundaries'])} boundaries on pauses; "
          f"{len(st['dip_snapped'])} starts moved to a dip, {len(st['stretched'])} pulled back to a pause")
    return 0


# ------------------------------------------------------------------ small commands

def cmd_norm(a) -> int:
    for t in a.text:
        print(" ".join(norm_ar(w) for w in str(t).split()))
    return 0


def cmd_doctor(a) -> int:
    ff = shutil.which("ffmpeg")
    ffv = None
    if ff:
        try:
            ffv = (subprocess.run([ff, "-version"], capture_output=True, text=True, timeout=20).stdout.splitlines()
                   or ["?"])[0]
        except (OSError, subprocess.SubprocessError):
            ffv = "present but did not answer -version"
    try:
        import numpy
        npv = numpy.__version__
    except ImportError:
        npv = None
    audio = "ready" if (npv and ff) else ("PCM .wav only (no ffmpeg)" if npv else "missing numpy (pip install numpy)")
    rep = {"ffmpeg": ff, "ffmpeg_version": ffv, "numpy": npv, "python": sys.version.split()[0],
           "commands": {"fetch": "ready; needs HTTPS to api.alquran.cloud, or --offline with a filled cache (not "
                                 "checked here)",
                        "pauses": audio, "align": "ready (standard library)", "align --audio": audio,
                        "norm": "ready"}}
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        print(f"python {rep['python']}")
        print(f"ffmpeg  {ff or 'missing'}{'  (' + ffv + ')' if ffv else ''}")
        print(f"numpy   {npv or 'missing'}")
        for k, v in rep["commands"].items():
            print(f"  {k:14} {v}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="quran_text.py", description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 done, 1 bad input or refused, 3 network/API failure, "
                                       "4 the API answered a different verse.")
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="exact verse text from api.alquran.cloud → verses.json + verses.txt")
    f.add_argument("refs", nargs="+", metavar="REF", help="surah:ayah or surah:first-last, e.g. 51:22-23 53:39")
    f.add_argument("--edition", default="quran-simple", help="quran-simple (default) or quran-uthmani")
    f.add_argument("--translation", default="none", help="none (default) or en.pickthall (public domain); others refused")
    f.add_argument("--out", default="out/quran-text", help="folder for verses.json and verses.txt")
    f.add_argument("--cache", help="answer cache folder (default OUT/cache)")
    f.add_argument("--offline", action="store_true", help="use the cache only; fail on a missing verse")
    f.add_argument("--refresh", action="store_true", help="ignore the cache and fetch again")
    f.add_argument("--keep-basmala", action="store_true", help="keep the basmala prefix that the API adds to ayah 1")
    f.add_argument("--delay", type=float, default=0.5, help="seconds between network calls (default 0.5)")
    f.add_argument("--timeout", type=float, default=20.0, help="seconds per request (default 20)")
    f.set_defaults(func=cmd_fetch)

    pa = sub.add_parser("pauses", help="measured pauses in a recitation (RMS below peak + rel-db)")
    pa.add_argument("audio", metavar="AUDIO")
    pa.add_argument("--min", type=float, default=0.30, help="shortest pause in seconds (default 0.30)")
    pa.add_argument("--rel-db", type=rel_db_arg, default=-22.0,
                    help="threshold below the loudest frame (default -22), or auto (Otsu split, for noisy or "
                         "reverberant recordings)")
    pa.add_argument("--frame", type=float, default=0.05, help="RMS frame in seconds (default 0.05)")
    pa.add_argument("--json", action="store_true", help="print the kosif.quran-pauses.v1 JSON")
    pa.add_argument("--out", help="also write the JSON report here (align --pauses reads it)")
    pa.set_defaults(func=cmd_pauses)

    al = sub.add_parser("align", help="verse and word timing from verses.json + words.json (+ audio pauses)")
    al.add_argument("--verses", required=True, help="verses.json from fetch")
    al.add_argument("--words", required=True, help="words.json (kosif-words/1) from montage_pro.py transcribe")
    al.add_argument("--audio", help="the recitation: snaps verse boundaries to pauses, no word crosses a pause")
    al.add_argument("--pauses", help="a saved `pauses --json --out` report instead of --audio")
    al.add_argument("--min", type=float, default=0.30)
    al.add_argument("--rel-db", type=rel_db_arg, default=None,
                    help="pause threshold: default -22. When -22 finds fewer pauses than verse boundaries, the Otsu "
                         "split is used only if the recording has no pause at -22 dB and two classes of frame levels "
                         "(reverberant); a wasl recitation keeps -22 and its boundaries come from the word timing. A "
                         "number or auto fixes it")
    al.add_argument("--frame", type=float, default=0.05)
    al.add_argument("--no-dip-snap", action="store_true",
                    help="keep the recogniser's start of long words (by default, with --audio, it is moved to the "
                         "onset after a clear consonant dip nearby)")
    al.add_argument("--max-dist", type=float, default=DEFAULT_MAX_DIST,
                    help="largest edit distance / length that still counts as the same word (default 0.45)")
    al.add_argument("--out", required=True, help="timing.json to write")
    al.set_defaults(func=cmd_align)

    no = sub.add_parser("norm", help="print the matching key of Arabic text")
    no.add_argument("text", nargs="+")
    no.set_defaults(func=cmd_norm)

    do = sub.add_parser("doctor", help="what can run here (ffmpeg, numpy)")
    do.add_argument("--json", action="store_true")
    do.set_defaults(func=cmd_doctor)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except Fail as e:
        print(f"quran_text: {e}", file=sys.stderr)
        return e.code
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
