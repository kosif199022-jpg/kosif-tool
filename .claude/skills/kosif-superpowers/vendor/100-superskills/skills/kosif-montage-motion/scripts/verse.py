"""KOSIF verse — a kinetic-typography film from sound alone: a song, a poem, a dua, a voice-over.

    python verse.py AUDIO --name NAME [--text lyrics.txt] [--words AUDIO.words.json] [--title "…"] [--sub "…"]
                    [--size 1080x1920] [--mood night|dawn|gold|sea|ink] [--accent "#E7B65A"] [--images a.jpg b.jpg …]
                    [--music none|auto|bed.wav] [--credit "…"] [--model large-v3] [--fix "a=b;c=d"] [--fps 30] [--render]

AUDIO may be a video (its sound is used). What it decides — all written to projects/NAME/verse.json (+ verse.js), so
Claude or you can change any line, keyword, colour or time and re-render:
- timing: Whisper's word times; with --text the true words (lyrics, the poem, the dua) are aligned onto them —
  diacritics, hamza/alef/ta-marbuta variants and ASR misspellings are matched, unmatched words are placed between their
  neighbours by length. Without Whisper and with --text, the lines are spread over the voiced spans and the report says
  "estimated" (never presented as measured);
- lines: the text's own lines, else the sentences, at most 7 words, broken at the longest pause;
- sections: a pause ≥ 3 s starts a new section (a palette step, the next image, a light rule); a pause ≥ 4.5 s is an
  interlude (an eight-point rosette breathing on the beat); a long intro carries the title card;
- one keyword per line (loudness × length + end-focus + the words the text returns to; fillers never, refrains once);
- the payoff: the last time the refrain (a line heard ≥ 2 times) comes back, else the most stressed line in the last
  40 % — set large with a light sweep and a flare;
- the sound drives the light: kicks pulse the halo and send rings, onsets lift the motes, loudness breathes the glow
  (qa.channels, embedded in sound.js);
- music: none added by default (a song carries its own; a recitation should stay unaccompanied); --music auto adds an
  original underscore only when the track has no bed (a spoken poem, a voice-over).
Then `kmotion render projects/NAME --engine studio` (or --render here), `kmotion inspect`, `kmotion sheet`.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"
TEMPLATE = next((p for p in (HERE / "templates" / "verse.html", HERE.parent / "templates" / "verse.html") if p.exists()), None)
MOODS = ("night", "dawn", "gold", "sea", "ink")
DIAC = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")


def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(r.stderr[-1500:])
    return r


def duration_of(p: Path) -> float:
    return float(_run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).stdout.strip())


def norm(t: str) -> str:
    """The comparable form of a word: no diacritics or tatweel, one alef, ya for alef maqsura, ha for ta marbuta."""
    t = DIAC.sub("", t)
    t = re.sub("[أإآٱ]", "ا", t).replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    return re.sub(r"[^\w]", "", t).lower()


def read_text(path: Path) -> list[list[str]]:
    """Lines of the true text (blank lines and [section] headers skipped) → lists of words."""
    out = []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not (ln.startswith("[") and ln.endswith("]")) and not ln.startswith("#"):
            ws = ln.replace("..", " ").split()
            if ws:
                out.append(ws)
    return out


def _fuzzy_pairs(a: list[str], b: list[str], floor: float = 0.55) -> list[tuple[int, int]]:
    """Monotonic pairing of two word lists that maximises total spelling similarity (pairs below `floor` never made)."""
    n, m = len(a), len(b)
    sim = [[difflib.SequenceMatcher(None, x, y).ratio() if x and y else 0.0 for y in b] for x in a]
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            take = sim[i][j] + best[i + 1][j + 1] if sim[i][j] >= floor else -1.0
            best[i][j] = max(take, best[i + 1][j], best[i][j + 1])
    out, i, j = [], 0, 0
    while i < n and j < m:
        if sim[i][j] >= floor and abs(best[i][j] - (sim[i][j] + best[i + 1][j + 1])) < 1e-9:
            out.append((i, j)); i += 1; j += 1
        elif best[i + 1][j] >= best[i][j + 1]:
            i += 1
        else:
            j += 1
    return out


def align(lines: list[list[str]], asr: list[dict]) -> list[list[dict]]:
    """Put the true words on the recognised words' times. Equal blocks and one-to-one replacements take the ASR word's
    time; uneven replacements share the ASR span by length; words the ASR missed sit between their timed neighbours."""
    flat = [(li, w) for li, ws in enumerate(lines) for w in ws]
    a = [norm(w["text"]) for w in asr]
    b = [norm(w) for _, w in flat]
    times: list[tuple[float, float] | None] = [None] * len(flat)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(j2 - j1):
                times[j1 + k] = (asr[i1 + k]["start"], asr[i1 + k]["end"])
        elif op == "replace":
            # uneven block: pair words by spelling (ASR of singing bends endings: سأعود → سأعودوا), in order; what
            # pairs with nothing — a hallucinated "subscribe" at the end, a missed word — is left to the fill below
            pairs = _fuzzy_pairs(a[i1:i2], b[j1:j2])
            for ia, jb in pairs:
                times[j1 + jb] = (asr[i1 + ia]["start"], asr[i1 + ia]["end"])
            if not pairs:                                        # nothing alike: share the span by length
                t0, t1 = asr[i1]["start"], asr[i2 - 1]["end"]
                ln = np.array([len(b[j]) + 1 for j in range(j1, j2)], float)
                edges = t0 + (t1 - t0) * np.concatenate([[0], np.cumsum(ln) / ln.sum()])
                for k in range(j2 - j1):
                    times[j1 + k] = (float(edges[k]), float(edges[k + 1]))
    # fill the words nothing timed: spread them between the neighbours
    j = 0
    while j < len(times):
        if times[j] is not None:
            j += 1
            continue
        k = j
        while k < len(times) and times[k] is None:
            k += 1
        t0 = times[j - 1][1] if j > 0 else max(0.0, (times[k][0] if k < len(times) else 0.0) - 0.4 * (k - j))
        t1 = times[k][0] if k < len(times) else t0 + 0.4 * (k - j)
        step = max(0.05, (t1 - t0) / (k - j))
        for q in range(j, k):
            times[q] = (t0 + (q - j) * step, t0 + (q - j + 1) * step)
        j = k
    out: list[list[dict]] = [[] for _ in lines]
    for (li, w), (s, e) in zip(flat, times):
        out[li].append({"text": w, "start": round(s, 3), "end": round(max(e, s + 0.05), 3)})
    return out


def voiced_spans(wav: Path, floor_db: float = -45.0) -> list[tuple[float, float]]:
    x, sr = _mono(wav)
    hop = int(sr * 0.05)
    lv = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(x) - hop, hop)])
    thr = max(floor_db, float(np.percentile(lv, 20)) + 6)
    on = lv > thr
    spans, start = [], None
    for i, v in enumerate(on):
        t = i * 0.05
        if v and start is None:
            start = t
        if not v and start is not None:
            spans.append([start, t]); start = None
    if start is not None:
        spans.append([start, len(on) * 0.05])
    merged = []
    for s in spans:                                            # a breath inside a phrase is not a pause
        if merged and s[0] - merged[-1][1] < 0.35:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return [(a, b) for a, b in merged if b - a > 0.15]


def estimate(lines: list[list[str]], wav: Path) -> list[list[dict]]:
    """No word times available: the text's words laid over the voiced spans in order, by length. Marked estimated."""
    spans = voiced_spans(wav)
    total = sum(b - a for a, b in spans) or 1.0
    flat = [(li, w) for li, ws in enumerate(lines) for w in ws]
    ln = np.array([len(norm(w)) + 1 for _, w in flat], float)
    cum = np.concatenate([[0], np.cumsum(ln) / ln.sum()]) * total

    def at(v):                                                 # voiced-time → clock time
        for a, b in spans:
            if v <= b - a:
                return a + v
            v -= b - a
        return spans[-1][1] if spans else v
    out: list[list[dict]] = [[] for _ in lines]
    for k, (li, w) in enumerate(flat):
        out[li].append({"text": w, "start": round(at(cum[k]), 3), "end": round(at(cum[k + 1]) - 0.02, 3)})
    return out


PARTICLES = {norm(w) for w in ("في من على الى إلى عن مع ان أن إن لا ما و ف ب ل لي لك له لها يا كل لكل بكل اللي الذي التي "
                                "لو اذا إذا عشان علشان لأن لان هل قد لقد ثم او أو").split()}         # a line never ends on one
OPENERS = {norm(w) for w in ("اللهم يا إلا ثم لكن حتى بل أو إن إذا لما كي لأن ربنا "                       # particles that open a phrase
                              "اجعل اغفر ارحم اهدنا اهدني ارزقنا ارزقني تقبل اكتب اشف احفظ ثبت يسر بارك أعنا").split()}  # a dua's imperatives


# meaning → symbol (Voice2Motion's idea: the picture follows what is said, not only how loud). Roots are compared after
# norm() and after stripping the attached particles و ف ب ل ال; English words by prefix.
CONCEPTS = {
    "sun": "شمس صباح نهار شروق ضوء نور ضحى sun sunny morning light bright dawn",
    "moon": "ليل ليله قمر نجوم نجم مساء سهر night moon star evening dark",
    "heart": "قلب قلوب حب حبيب روح شوق غرام love heart soul",
    "clock": "ساعه وقت لحظه دقيقه زمن عمر ايام time hour minute moment clock",
    "money": "فلوس مال دولار ريال جنيه مليون ميزانيه ثمن سعر money dollar price budget refund cash",
    "trophy": "نجاح ناجح ناجحه فوز فاز حلم احلام هدف قمه انجاز success win dream goal champion",
    "road": "طريق خطوه خطوات درب رحله سفر مشوار طرق path road step journey travel way",
    "question": "ليه ازاي كيف ماذا لماذا سؤال why how what question",
    "check": "تم خلاص اكيد تاكيد مستجاب امين حقق تحقق done confirmed yes ready",
    "home": "بيت وطن دار اهل غربه home house family",
    "rain": "مطر غيم سحاب ماء بحر موج نهر rain cloud water sea river",
    "light": "اللهم يارب رب دعاء الله رحمه فرج جبر prayer pray hope",
}
_ROOTS = {k: v.split() for k, v in CONCEPTS.items()}


def concept_of(word: str) -> str | None:
    w = norm(word)
    cands = {w}
    for pre in ("وال", "فال", "بال", "لل", "ال", "و", "ف", "ب", "ل"):
        if w.startswith(pre) and len(w) - len(pre) >= 2:
            cands.add(w[len(pre):])
    for kind, roots in _ROOTS.items():
        for r in roots:
            if any(c == r or (c.startswith(r) and (len(r) >= 4 or len(c) - len(r) <= 2)) for c in cands):   # قلبي، قلبك، قلبنا
                return kind
    return None


def _break_bonus(words: list[dict], i: int, stopn: set[str]) -> float:
    """How good a line break before words[i] is: a pause, punctuation, a phrase opener (a و/ف-clause, اللهم، يا، إلا, a
    dua's imperative) — large ASR models stretch words over the pauses, so the grammar has to help. Never after a
    particle ("في", "من", "لي"), never between a quantity and its number, never inside "يا حي يا قيوم"."""
    gap = words[i]["start"] - words[i - 1]["end"]
    nxt, prev = norm(words[i]["text"]), words[i - 1]["text"]
    chain = nxt == "يا" and i >= 2 and norm(words[i - 2]["text"]) == "يا"
    b = 8 * min(gap, 1.0) + (1.0 if re.search(r"[،,.؟?!:؛]$", prev) else 0) + (0.8 if nxt in OPENERS and not chain else 0) - (1.0 if chain else 0)
    b += (0.6 if nxt.startswith("و") and len(nxt) >= 4 else 0) + (0.5 if nxt.startswith("ف") and len(nxt) >= 5 else 0)
    num = lambda t: bool(re.search(r"[0-9٠-٩]", t))
    b -= (0.8 if num(words[i]["text"]) or num(prev) else 0) + (0.7 if norm(prev) in PARTICLES else 0)
    return b


def segment(words: list[dict], max_words: int = 7, stopn: set[str] | None = None) -> list[list[dict]]:
    """Lines a reader can take in: dynamic programming over the cut points — each line ~1.1–3.6 s and ≤ max_words,
    each cut paid for by how good a phrase break it is (_break_bonus). Works for sung lines and for fast speech."""
    if stopn is None:
        from direct import STOP
        stopn = {norm(x) for x in STOP}
    N = len(words)
    best, back = [0.0] + [1e9] * N, [0] * (N + 1)
    for j in range(1, N + 1):
        for i in range(max(0, j - max_words - 3), j):
            n, d = j - i, words[j - 1]["end"] - words[i]["start"]
            c = 6 * max(0, n - max_words) + 4 * max(0.0, 1.1 - d) + 1.5 * max(0.0, d - 3.6) + (1.5 if n == 1 else 0)
            v = best[i] + c - (_break_bonus(words, i, stopn) if i > 0 else 0)
            if v < best[j]:
                best[j], back[j] = v, i
    out, j = [], N
    while j > 0:
        out.append(words[back[j]:j])
        j = back[j]
    return out[::-1]


def _mono(wav: Path):
    with wave.open(str(wav)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return (x.reshape(-1, ch).mean(1) if ch > 1 else x), sr


def plan(lines: list[list[dict]], stress: list[float], duration: float, W: int, H: int, title: str | None, n_images: int = 0) -> dict:
    from direct import STOP
    words = [w for ln in lines for w in ln]
    for w, s in zip(words, stress):
        w["stress"] = float(s)
    clean = lambda t: norm(t)
    stop = {norm(s) for s in STOP}
    # sections and interludes from the pauses between lines
    sections, interludes = [{"t": 0.0}], []
    for i in range(1, len(lines)):
        gap = lines[i][0]["start"] - lines[i - 1][-1]["end"]
        if gap >= 3.0:
            sections.append({"t": round(lines[i][0]["start"] - min(0.6, gap / 3), 3)})
        if gap >= 4.5:
            interludes.append({"t": round(lines[i - 1][-1]["end"] + 0.8, 3), "end": round(lines[i][0]["start"] - 0.5, 3)})
    # no pauses long enough (speech, a through-sung song): more sections by time, on line starts — one per picture,
    # else one per ~12 s, so the light (and the pictures) still move with the structure
    want = max(n_images, int(duration // 12) + 1)
    if len(sections) < want and lines:
        starts = [ln[0]["start"] for ln in lines[1:]]
        for q in range(1, want):
            target = duration * q / want
            t = min(starts, key=lambda x: abs(x - target)) if starts else target
            if all(abs(t - x["t"]) > 2.0 for x in sections):
                sections.append({"t": round(t - 0.05, 3)})
        sections.sort(key=lambda x: x["t"])
    for i, s in enumerate(sections):
        s["end"] = sections[i + 1]["t"] if i + 1 < len(sections) else duration
        s["i"] = i
    # the refrain and the payoff
    key_of = lambda ln: " ".join(clean(w["text"]) for w in ln)
    count: dict[str, int] = {}
    for ln in lines:
        count[key_of(ln)] = count.get(key_of(ln), 0) + 1
    refrain = [i for i, ln in enumerate(lines) if count[key_of(ln)] >= 2 and len(ln) >= 2]
    mean_stress = lambda ln: float(np.mean([w["stress"] for w in ln if clean(w["text"]) not in stop] or [-9]))
    seen: dict[str, int] = {}
    for ln in lines:
        for wt in {clean(w["text"]) for w in ln}:
            seen[wt] = seen.get(wt, 0) + 1
    content = {wt: n for wt, n in seen.items() if wt not in stop and len(wt) >= 3}
    theme = max(content, key=lambda wt: (content[wt], len(wt))) if content and max(content.values()) >= 3 else None
    theme_in = lambda ln: bool(theme) and any(clean(w["text"]).endswith(theme) for w in ln)
    if refrain:
        payoff = refrain[-1]
    elif lines:
        # no refrain: the closing argument — a late line that names the theme or a number, the last lines favoured
        late = [i for i, ln in enumerate(lines) if ln[0]["start"] >= 0.6 * duration and len(ln) >= 3] or [len(lines) - 1]
        payoff = max(late, key=lambda i: (mean_stress(lines[i]) + (1.0 if theme_in(lines[i]) else 0)
                                          + (0.8 if any(re.search(r"[0-9٠-٩]", w["text"]) for w in lines[i]) else 0)
                                          + (0.6 if i == len(lines) - 1 else 0.3 if i >= len(lines) - 3 else 0), i))
    else:
        payoff = None
    used: set[str] = set()
    last_key = -9.0
    out_lines = []
    for i, ln in enumerate(lines):
        cand = [w for w in ln if clean(w["text"]) not in stop and len(clean(w["text"])) >= 3 and clean(w["text"]) not in used]
        kw = None
        if cand and len(ln) >= 2:
            score = lambda w: w["stress"] + 0.9 * (ln.index(w) + 1) / len(ln) + (0.5 if 2 <= seen.get(clean(w["text"]), 0) <= 3 else 0)
            kw = max(cand, key=score)
            # a keyword has to earn it (above-average weight) and leave room (≥ 2 s since the last): a colour on every
            # line is no emphasis at all; the payoff line always gets one
            if i != payoff and (score(kw) < 0.75 or kw["start"] - last_key < 2.0):
                kw = None
            else:
                used.add(clean(kw["text"]))                       # a word is the keyword once: repetition dulls it
                last_key = kw["start"]
        nxt = lines[i + 1][0]["start"] if i + 1 < len(lines) else duration
        hold = min(nxt - 0.06, ln[-1]["end"] + (2.2 if i == payoff else 1.4))
        chars = sum(len(w["text"]) for w in ln) + len(ln) - 1
        size = 124 if chars <= 14 else 104 if chars <= 24 else 88 if chars <= 36 else 74
        out_lines.append({"t": round(ln[0]["start"], 3), "end": round(min(nxt - 0.06, max(hold, ln[-1]["end"] + 0.3)), 3), "size": size * (1.22 if i == payoff else 1),
                          "payoff": i == payoff, "section": max(s["i"] for s in sections if s["t"] <= ln[0]["start"] + 1e-6),
                          "words": [{"t": round(w["start"], 3), "text": w["text"], "key": w is kw} for w in ln]})
    # symbols by meaning: the keyword's concept first, else the line's first; a number becomes a counter. Never the same
    # symbol twice in a row, never closer than 2.5 s — a symbol per line would be wallpaper
    last_kind, last_t, last_m = None, -9.0, None
    for ol, ln in zip(out_lines, lines):
        num = next((w for w in ln if re.fullmatch(r"[0-9٠-٩]+([.,][0-9٠-٩]+)?", w["text"].strip("%٪+"))), None)
        kw = next((w for w in ol["words"] if w["key"]), None)
        kind = (concept_of(kw["text"]) if kw else None) or next((k for k in (concept_of(w["text"]) for w in ln) if k), None)
        if num is not None:
            kind = "count"
        strong = kind == "count" or ol["payoff"]                      # a number said, or the payoff: always shown
        if kind and (strong or (kind != last_kind and ol["t"] - last_t >= 2.5)):
            m = {"kind": kind, "t": round(ln[0]["start"], 3), "end": ol["end"]}
            if kind == "count":
                m["value"] = num["text"].translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")).strip("%٪+")
                m["t"] = round(num["start"] - 0.25, 3)
            if strong and last_m is not None and last_m["end"] > m["t"] - 0.4:
                last_m["end"] = round(max(last_m["t"] + 0.4, m["t"] - 0.4), 3)   # the earlier symbol is gone (0.35 s fade) before this one starts
            ol["motif"] = m
            last_kind, last_t, last_m = kind, ol["t"], m
    first = lines[0][0]["start"] if lines else duration
    last = lines[-1][-1]["end"] if lines else 0.0
    cards = {"title": {"t": 0.25, "end": round(first - 0.35, 3)} if title and first >= 1.5 else None,
             "header": {"t": 0.15, "end": round(min(duration * 0.35, 6.0), 3)} if title and first < 1.5 else None,
             "end": {"t": round(last + 0.6, 3), "end": round(duration - 0.45, 3)} if duration - last >= 2.0 else None}
    return {"lines": out_lines, "sections": sections, "interludes": [x for x in interludes if x["end"] - x["t"] >= 1.5], "cards": cards,
            "payoff": payoff, "refrain": " ".join(w["text"] for w in lines[refrain[-1]]) if refrain else None, "end": round(duration - 0.4, 3)}


def text_band(image: Path, W: int, H: int) -> float | None:
    """Where the type may sit over a picture: the face (largest skin region, as `direct` finds it) after the picture is
    fill-cropped to W×H. Returns a y (px) for the line centre — the lower or upper third — when the face is in the
    middle band, None when the middle is free. Type never covers eyes or mouth."""
    try:
        import cv2
    except ImportError:
        return None
    im = cv2.imread(str(image))
    if im is None:
        return None
    h, w = im.shape[:2]
    sc = max(W / w, H / h)
    im = cv2.resize(im, (int(w * sc + 0.5), int(h * sc + 0.5)))
    y0, x0 = (im.shape[0] - H) // 2, (im.shape[1] - W) // 2
    im = im[y0:y0 + H, x0:x0 + W]
    y = cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb)
    m = ((y[..., 1] >= 133) & (y[..., 1] <= 178) & (y[..., 2] >= 80) & (y[..., 2] <= 130) & (y[..., 0] > 60)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(m)
    if n <= 1:
        return None
    j = 1 + int(np.argmax(st[1:, 4]))
    if st[j, 4] < 0.004 * W * H:
        return None
    top, bot = st[j, 1], st[j, 1] + min(st[j, 3], int(0.22 * H))      # the head, not the arms or the whole body
    cy = 0.47 * H if H > W else 0.5 * H
    if bot < cy - 0.10 * H or top > cy + 0.10 * H:
        return None
    return round(0.70 * H) if (top + bot) / 2 < cy else round(0.26 * H)


DISPLAY_DIRS = [Path.home() / ".claude" / "skills" / "kosif-mimic" / "assets" / "fonts", HERE / "kit" / "fonts",
                Path("C:/Windows/Fonts"), Path.home() / "AppData/Local/Microsoft/Windows/Fonts"]


def find_display_font(name: str) -> Path | None:
    """A display face by file path or by name ("Aref Ruqaa", "ElMessiri-700", "Amiri Bold"): the boldest match wins."""
    p = Path(name)
    if p.suffix.lower() in (".ttf", ".otf") and p.exists():
        return p
    key = name.lower().replace(" ", "").replace("-", "")
    hits = [f for d in DISPLAY_DIRS if d.exists() for f in d.iterdir()
            if f.suffix.lower() in (".ttf", ".otf") and key in f.stem.lower().replace("-", "").replace("_", "")]
    rank = lambda f: (("black" in f.stem.lower() or "900" in f.stem) * 3 + ("bold" in f.stem.lower() or "700" in f.stem) * 2)
    return max(hits, key=rank) if hits else None


def sound(wav: Path, fps: int) -> dict:
    """The track as light: per-frame rms / bass / onset (2 decimals) and the kick, onset and beat times."""
    import qa
    tmp = Path(tempfile.mkdtemp(prefix="kosif_verse_"))
    qa.channels(wav, fps, tmp / "channels.json")               # returns a summary; the arrays are in the file
    ch = json.loads((tmp / "channels.json").read_text(encoding="utf-8"))
    r2 = lambda a: [round(float(v), 2) for v in a]
    sec = lambda a: [round(float(v), 3) for v in a]
    return {"fps": fps, "frames": ch.get("frames"), "bpm": ch.get("bpm"), "rms": r2(ch.get("rms", [])), "bass": r2(ch.get("bass", [])),
            "onset": r2(ch.get("onset", [])), "kicks": sec(ch.get("kicks", [])), "onsets": sec(ch.get("onsets", [])), "beats": sec(ch.get("beats", [])), "downbeats": sec(ch.get("downbeats", []))}


def verse(audio: Path, name: str, text: Path | None = None, words_json: Path | None = None, title: str | None = None, sub: str | None = None,
          size=(1080, 1920), mood="night", accent="#E7B65A", images: list[Path] | None = None, music="none", credit: str | None = None,
          model="large-v3", fixes: str | None = None, fps: int = 30, render=False, plate: Path | None = None,
          cuts: list[float] | None = None, brand: str | None = None, brand_side: str = "left", font: str | None = None,
          fx3d: bool = True) -> dict:
    """plate: a finished, muted footage montage (e.g. from songreel) shown under the type for the whole film — all-intra
    so every frame seeks exactly; cuts: its cut times (s), each shot gets its own slow push and a kick on the beat."""
    import motion as MO
    import transcribe as T
    from direct import apply_fixes, word_stress
    audio = Path(audio)
    W, H = size
    proj = MO.PROJECTS / MO.safe_name(name)
    (proj / "assets").mkdir(parents=True, exist_ok=True)
    song = proj / "assets" / "song.wav"
    _run([FF, "-y", "-v", "error", "-i", str(audio), "-vn", "-ac", "2", "-ar", "48000", str(song)])
    dur = duration_of(song)
    true_lines = read_text(text) if text else None
    timing = "words"
    if words_json:
        segs = json.loads(Path(words_json).read_text(encoding="utf-8"))
    else:
        try:
            segs = T.transcribe(audio, model)
            timing = "asr"
        except SystemExit:                                     # transcribe's "no speech model here"
            if not true_lines:
                raise SystemExit("no speech model here: give --text lyrics.txt (timing estimated) or --words NAME.words.json")
            segs, timing = None, "estimated"
    if segs is not None:
        segs = apply_fixes(segs, fixes)
    if true_lines and segs is not None:
        lines = [part for ln in align(true_lines, [w for s in segs for w in s["words"]]) for part in (segment(ln) if len(ln) > 7 else [ln])]
        timing = "aligned"
    elif true_lines:
        lines = estimate(true_lines, song)
    else:
        lines = [part for s in segs for part in segment([dict(w) for w in s["words"]]) if part]
    lines = [ln for ln in lines if ln]
    T.write_all([{"start": ln[0]["start"], "end": ln[-1]["end"], "text": " ".join(w["text"] for w in ln), "words": ln} for ln in lines], proj / "transcript")
    stress = word_stress(song, [w for ln in lines for w in ln])
    pl = plan(lines, stress, dur, W, H, title or None, len(images or []))
    # optional pictures: one per section, in order (cycled)
    imgs = []
    for i, p in enumerate(images or []):
        dst = proj / "assets" / f"img_{i:02d}{Path(p).suffix.lower()}"
        shutil.copy2(p, dst)
        imgs.append("assets/" + dst.name)
    extra_audio, bed_note = "", "none added"
    if music not in ("none", "auto"):
        shutil.copy2(music, proj / "assets" / "music.wav")
        bed_note = Path(music).name
    elif music == "auto":
        import reel as RL
        if RL.has_music_bed(song, [w for ln in lines for w in ln]):
            bed_note = "the track's own bed"
        else:
            import score as SC
            sc = SC.Score(80, dur, "D", "minor", seed=11)
            b = dur / (60 / 80)
            sc.arrange({"sections": [{"from": 1, "to": b, "pad": True}]})
            sc.mix(proj / "assets" / "music.wav")
            bed_note = "original underscore"
    if (proj / "assets" / "music.wav").exists() and bed_note != "none added" and bed_note != "the track's own bed":
        extra_audio = f'\n  <audio id="music" src="assets/music.wav" data-start="0" data-duration="{round(dur, 3)}" data-volume="0.45" data-role="music" data-fade-out="0.6"></audio>'
    plate_tag, plate_rel = "", None
    if plate:
        dst = proj / "assets" / "plate.mp4"
        if Path(plate).resolve() != dst.resolve():
            shutil.copy2(plate, dst)
        plate_rel = "assets/plate.mp4"
        plate_tag = (f'<video id="plate" class="plate" src="{plate_rel}" data-start="0" data-duration="{round(dur, 3)}" '
                     'muted playsinline preload="auto"></video>')
    tmpd = Path(tempfile.mkdtemp(prefix="kosif_verse_band_"))
    for sec in pl["sections"]:                                    # keep the type off the face in each section's picture
        if images:
            ty = text_band(images[sec["i"] % len(images)], W, H)
            if ty:
                sec["ty"] = ty
        elif plate:                                               # the plate: the frame in the middle of the section
            still = tmpd / f"s{sec['i']}.jpg"
            mid = (sec["t"] + sec["end"]) / 2
            subprocess.run([FF, "-y", "-v", "error", "-ss", f"{mid:.3f}", "-i", str(proj / plate_rel), "-frames:v", "1", str(still)])
            ty = text_band(still, W, H) if still.exists() else None
            if ty:
                sec["ty"] = ty
    shutil.rmtree(tmpd, ignore_errors=True)
    disp = find_display_font(font) if font else None
    if disp:
        shutil.copy2(disp, proj / "assets" / "display.ttf")
    spec = {"W": W, "H": H, "fps": fps, "brand": brand, "brand_side": brand_side, "display_font": disp.name if disp else None,
            "fx3d": fx3d, "duration": round(dur, 3), "mood": mood if mood in MOODS else "night", "accent": accent,
            "title": title, "sub": sub, "credit": credit, "images": imgs, "timing": timing, "plate": plate_rel,
            "cuts": [round(float(c), 3) for c in (cuts or [0.0])], **pl}
    (proj / "verse.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    (proj / "verse.js").write_text("window.VERSE = " + MO.json_for_script(spec) + ";\n", encoding="utf-8")
    (proj / "sound.js").write_text("window.SOUND = " + json.dumps(sound(song, fps)) + ";\n", encoding="utf-8")
    html = TEMPLATE.read_text(encoding="utf-8").replace("{{MUSIC}}", extra_audio).replace("{{PLATE}}", plate_tag)
    for k, v in {"{{W}}": W, "{{H}}": H, "{{SECONDS}}": round(dur, 3), "{{FPS}}": fps, "{{TITLE}}": MO.html_text(title or name)}.items():
        html = html.replace(k, str(v))
    (proj / "index.html").write_text(html, encoding="utf-8")
    MO.sync_assets(proj)
    rep = {"project": str(proj), "timing": timing, "seconds": round(dur, 2), "lines": len(pl["lines"]), "sections": len(pl["sections"]),
           "interludes": len(pl["interludes"]), "keywords": [w["text"] for ln in pl["lines"] for w in ln["words"] if w["key"]],
           "payoff": " ".join(w["text"] for w in pl["lines"][pl["payoff"]]["words"]) if pl["payoff"] is not None and pl["lines"] else None,
           "refrain": pl["refrain"], "music": bed_note}
    if timing == "estimated":
        rep["note"] = "word times are estimated from the voiced spans (no Whisper): check transcript.srt, give --words for exact timing"
    if render:
        rep["film"] = str(MO.render(str(proj), "studio", "looks", None, None, 1))
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio"); ap.add_argument("--name", required=True); ap.add_argument("--text", type=Path); ap.add_argument("--words", type=Path)
    ap.add_argument("--title"); ap.add_argument("--sub"); ap.add_argument("--size", default="1080x1920"); ap.add_argument("--mood", default="night", choices=MOODS)
    ap.add_argument("--accent", default="#E7B65A"); ap.add_argument("--images", nargs="*", type=Path); ap.add_argument("--music", default="none")
    ap.add_argument("--credit"); ap.add_argument("--model", default="large-v3"); ap.add_argument("--fix"); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--plate", type=Path, help="a muted footage montage under the type (all-intra; kmotion songreel makes one)")
    ap.add_argument("--cuts", type=Path, help="JSON list of the plate's cut times in seconds")
    ap.add_argument("--brand", help="a brand mark in the top corner (the maker's name)"); ap.add_argument("--brand-side", default="left", choices=["left", "right"])
    ap.add_argument("--font", help="display face for the lyrics: a .ttf path or a name (Aref Ruqaa, El Messiri, Amiri, Reem Kufi…)")
    ap.add_argument("--flat", action="store_true", help="no 3D words, depth dust, light rays or leaks")
    a = ap.parse_args()
    W, H = (int(v) for v in a.size.lower().split("x"))
    cuts = json.loads(a.cuts.read_text(encoding="utf-8")) if a.cuts else None
    rep = verse(Path(a.audio), a.name, a.text, a.words, a.title, a.sub, (W, H), a.mood, a.accent, a.images, a.music, a.credit, a.model, a.fix, a.fps, a.render,
                a.plate, cuts, a.brand, a.brand_side, a.font, not a.flat)
    print(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
