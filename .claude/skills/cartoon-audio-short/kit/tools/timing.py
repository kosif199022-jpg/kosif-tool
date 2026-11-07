#!/usr/bin/env python3
"""Word timings for a voiceover in Arabic or English -> words.json + phrases.json.

Usage:
  python3 timing.py voice.mp3 [script.txt] [--out work/] [--lang ar|en] [--asr-words file.json]

The script may be the exact text pasted into the voice generator: [tags], tashkeel and
<break> marks are removed before timing, so one copy of the script is enough.

1. Speech recognition, if available (faster-whisper, openai-whisper, or --asr-words with a
   whisper.cpp -oj file or a [{"w","s","e"}] list). With a script, the script's own words are
   mapped onto the recognised timings, so a misheard Arabic or dialect word cannot change the text.
2. Otherwise it needs the script: finds speech segments by silence (ffmpeg silencedetect), splits
   the script into phrases at punctuation (Arabic and Latin), and aligns phrases to segments with
   a DP that matches phrase length (syllables) to segment duration.
Always check phrases.json: pauses should fall at sentence ends.
"""
import difflib, functools, json, os, re, subprocess, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿ]")
TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")  # marks + tatweel
PUNCT = ",.;:!?،؛؟…"
SENT_END = r"[.!?؟…][\"”'»]?$"
PHRASE = re.compile(rf"[^{PUNCT}]+[{PUNCT}\"”'»]*")


def clean_script(text):
    """Remove everything the narrator does not say, plus tashkeel."""
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"<[^>]*>", " ", text)
    text = TASHKEEL.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def norm(w):
    """Compare words loosely: Arabic spelling variants and Iraqi g/k/q count as the same."""
    w = TASHKEEL.sub("", w.lower())
    for a, b in (("أإآٱ", "ا"), ("ة", "ه"), ("ى", "ي"), ("ؤ", "و"), ("ئ", "ي"), ("گقك", "ك"), ("چ", "ج")):
        w = re.sub(f"[{a}]", b, w)
    w = w.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    return re.sub(r"[^\w]", "", w)


def syll(w):
    """Rough syllable count, used only to share time between words."""
    digits = re.findall(r"[0-9٠-٩]", w)
    if digits:
        return 2 * len(digits)
    if ARABIC.search(w):
        # Written Arabic has about one syllable per two letters once tashkeel is removed.
        letters = re.sub(r"[^ء-يٮ-ۓ]", "", TASHKEEL.sub("", w))
        return max(1, round(len(letters) / 2))
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith("le"):
        n -= 1
    return max(1, n)


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)


def speech_segments(path, db=-35, mind=0.12):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=n={db}dB:d={mind}", "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    D = duration(path)
    segs, cur = [], 0.0
    for s, e in zip(starts, ends + [D] * (len(starts) - len(ends))):
        if s - cur > 0.08:
            segs.append([cur, s])
        cur = e
    if D - cur > 0.08:
        segs.append([cur, D])
    return segs, D


def load_asr_file(path):
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, dict) and "transcription" in data:  # whisper.cpp -oj
        out = []
        for t in data["transcription"]:
            w = t["text"].strip()
            if w and not re.fullmatch(r"\[[^\]]*\]", w):
                out.append({"w": w, "s": t["offsets"]["from"] / 1000, "e": t["offsets"]["to"] / 1000})
        return out
    # kosif-voice-studio writes [{"word","start","end"}]; take it as well as [{"w","s","e"}].
    return [{"w": x.get("w", x.get("word", "")), "s": x.get("s", x.get("start")), "e": x.get("e", x.get("end"))}
            for x in data]


def whisper_words(path, lang):
    # English keeps the fast English model. Arabic needs a multilingual one: base.en garbles it.
    name = "base.en" if lang == "en" else "small"
    try:
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel(name, compute_type="int8").transcribe(path, word_timestamps=True, language=lang)
        return [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
    except Exception:
        pass
    try:
        import whisper
        r = whisper.load_model(name).transcribe(path, word_timestamps=True, language=lang)
        return [{"w": w["word"].strip(), "s": round(w["start"], 3), "e": round(w["end"], 3)} for s in r["segments"] for w in s["words"]]
    except Exception:
        return None


def map_script(script, asr):
    """Give each script word a time from the recognised words. Returns (words, match ratio)."""
    ws = script.split()
    a, b = [norm(w) for w in ws], [norm(x["w"]) for x in asr]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    times = [None] * len(ws)
    matched = 0
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            times[i + k] = (asr[j + k]["s"], asr[j + k]["e"])
            matched += 1
    # Unmatched runs share the gap between their neighbours, by syllables.
    i = 0
    while i < len(ws):
        if times[i] is not None:
            i += 1
            continue
        k = i
        while k < len(ws) and times[k] is None:
            k += 1
        start = times[i - 1][1] if i else asr[0]["s"]
        end = times[k][0] if k < len(ws) else asr[-1]["e"]
        end = max(end, start + 0.05 * (k - i))
        total = sum(syll(w) for w in ws[i:k])
        t = start
        for m in range(i, k):
            d = (end - start) * syll(ws[m]) / total
            times[m] = (t, t + d)
            t += d
        i = k
    words = [{"w": w, "s": round(s, 3), "e": round(e, 3)} for w, (s, e) in zip(ws, times)]
    return words, matched / max(1, len(ws))


def phrases_from_words(words):
    phr, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(rf"[{PUNCT}][\"”'»]*$", w["w"]):
            phr.append({"text": " ".join(x["w"] for x in cur), "s": cur[0]["s"], "e": cur[-1]["e"]})
            cur = []
    if cur:
        phr.append({"text": " ".join(x["w"] for x in cur), "s": cur[0]["s"], "e": cur[-1]["e"]})
    return phr


def align(script, segs):
    phrases = [p.strip() for p in PHRASE.findall(script) if p.strip()]
    P, S = len(phrases), len(segs)
    syl = [sum(syll(w) for w in p.split()) for p in phrases]
    rate = sum(syl) / sum(e - s for s, e in segs)
    INF = 1e9

    # dp over (phrase i, segment j): segment j holds phrases [i..k); a phrase may also span several segments
    @functools.lru_cache(None)
    def best(i, j):
        if i == P and j == S:
            return (0.0, ())
        if i == P or j == S:
            return (INF, ())
        out = (INF, ())
        for k in range(i + 1, min(P, i + 4) + 1):
            for l in range(j + 1, min(S, j + 3) + 1):
                if k - i > 1 and l - j > 1:
                    continue
                d = segs[l - 1][1] - segs[j][0]
                s_ = sum(syl[i:k]) / rate
                cost = (d - s_) ** 2 / max(d, 0.3)
                # a sentence end inside a segment is unlikely (speakers pause there); a long gap inside one phrase too
                cost += sum(0.35 for m in range(i, k - 1) if re.search(SENT_END, phrases[m]))
                cost += sum(1.5 * (segs[m + 1][0] - segs[m][1]) for m in range(j, l - 1))
                sub = best(k, l)
                if sub[0] + cost < out[0]:
                    out = (sub[0] + cost, ((i, k, j, l),) + sub[1])
        return out

    sys.setrecursionlimit(max(10000, (P + S) * 20))
    cost, plan = best(0, 0)
    words, phr = [], []
    for i, k, j, l in plan:
        a, b = segs[j][0], segs[l - 1][1]
        text = " ".join(phrases[i:k])
        ws = text.split()
        sy = [syll(w) for w in ws]
        T, t = sum(sy), a
        phr.append({"text": text, "s": round(a, 3), "e": round(b, 3)})
        for w, s_ in zip(ws, sy):
            d = (b - a) * s_ / T
            words.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)})
            t += d
    return words, phr, cost


def opt(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


if __name__ == "__main__":
    skip = {i + 1 for i, a in enumerate(sys.argv) if a in ("--out", "--lang", "--asr-words")}
    args = [a for i, a in enumerate(sys.argv) if i and i not in skip and not a.startswith("--")]
    out = opt("--out") or "."
    os.makedirs(out, exist_ok=True)
    audio = args[0]
    script = None
    if len(args) > 1:
        raw = open(args[1], encoding="utf-8-sig").read() if os.path.exists(args[1]) else args[1]
        script = clean_script(raw)
    lang = opt("--lang") or (("ar" if ARABIC.search(script) else "en") if script else None)

    asr = load_asr_file(opt("--asr-words")) if opt("--asr-words") else whisper_words(audio, lang)
    segs, D = speech_segments(audio)
    words = phr = None
    if asr and script:
        words, ratio = map_script(script, asr)
        if ratio >= 0.4:
            phr, src = phrases_from_words(words), f"speech+script (matched {ratio:.0%})"
        else:
            print(f"WARNING: speech recognition matched only {ratio:.0%} of the script, using silence alignment.")
            words = None
    elif asr:
        words, src = asr, "speech only: check the words"
        phr = phrases_from_words(words)
    if words is None:
        if not script:
            print("NO_ASR: no speech recognition available and no script given. Ask the user for the script text.")
            sys.exit(2)
        words, phr, cost = align(script, segs)
        src = f"silence-align (cost {cost:.2f})"

    with open(os.path.join(out, "words.json"), "w", encoding="utf-8") as f:
        json.dump(words, f, indent=1, ensure_ascii=False)
    with open(os.path.join(out, "phrases.json"), "w", encoding="utf-8") as f:
        json.dump({"duration": D, "frames30": int(round(D * 30)), "language": lang, "source": src, "segments": segs, "phrases": phr}, f, indent=1, ensure_ascii=False)
    print(f"source={src} language={lang} duration={D:.2f}s frames={int(round(D * 30))}")
    for p in phr:
        print(f"{p['s']:6.2f}-{p['e']:6.2f}  f{int(p['s'] * 30):4d}-{int(p['e'] * 30):4d}  {p['text']}")
