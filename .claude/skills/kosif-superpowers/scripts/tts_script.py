#!/usr/bin/env python3
"""KOSIF TTS script prep — prosody-safe chunks, duration estimates and SSML for Arabic and mixed scripts.

تجهيز نص التعليق الصوتي: تقطيع آمن للنبرة وتقدير المدة وSSML بالعربية — TTS script chunking, timing and SSML.

Commands (JSON on stdout; FILE may be "-" for stdin)
  chunk FILE [--max-chars 250]
        splits the script into chunks of at most N characters for a TTS request: paragraphs are never merged,
        a chunk ends at a sentence end (. ! ? ؟ … ۔) when possible, otherwise at a clause mark (، , ؛ ; : —),
        otherwise between words — never inside a word (a single word longer than N is kept whole and flagged).
        e.g. python3 scripts/tts_script.py chunk script.txt --max-chars 200
  estimate FILE [--wpm 130] [--max-chars 250] [--sentence-pause 0.4] [--clause-pause 0.2] [--paragraph-pause 0.8]
        duration per chunk = words / wpm * 60 + pauses (each sentence end, clause mark and paragraph end).
        Words are whitespace-separated tokens holding a letter or digit, so Arabic clitics written attached
        (وبالكتاب) count as one word and stand-alone punctuation counts as none.
        e.g. python3 scripts/tts_script.py estimate script.txt --wpm 140
  ssml FILE [--lang ar-EG] [--other-lang en-US] [--xml]
        SSML 1.0: <p> per paragraph, <s> per sentence, <break> after clause marks and sentences, and
        <lang xml:lang=...> around runs of the other script (Latin runs in an Arabic script, Arabic runs in a
        Latin one). --xml prints the SSML document instead of JSON.
        e.g. python3 scripts/tts_script.py ssml script.txt --lang ar-EG --xml
  --self-test   runs a small offline check and exits 0.

Never uses the network and never writes files. Bad input: exit 2 with one line on stderr.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

TERM = ".!?؟…۔"
CLOSE = "\"'»”’)]"
_SENT_END = re.compile(rf"[{re.escape(TERM)}]+[{re.escape(CLOSE)}]*(?=\s|$)")
_CLAUSE_END = re.compile(r"[،,؛;:]+[\"'»”’)\]]*(?=\s)|\s[—–](?=\s)")
_PUNCT_TERM = re.compile(rf"[{re.escape(TERM)}]+(?=[{re.escape(CLOSE)}]*(?:\s|$))")
_PUNCT_CLAUSE = re.compile(r"[،,؛;:](?=\S*\s)|\s[—–]\s")
_WORD = re.compile(r"\w", re.UNICODE)
AR = "\u0621-\u0669\u066E-\u06D3\u06D5-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF"  # letters, marks, digits; not ، ؛ ؟ ۔
_LATIN_RUN = re.compile(r"[A-Za-z][A-Za-z0-9'’.\-]*(?:[ \t]+[A-Za-z0-9][A-Za-z0-9'’.\-]*)*")
_AR_RUN = re.compile(rf"[{AR}]+(?:[ \t]+[{AR}]+)*")
_LANG = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")


class Bad(ValueError):
    pass


def read(path) -> str:
    if path == "-":
        text = sys.stdin.read()
    else:
        p = Path(path)
        if not p.is_file():
            raise Bad(f"file not found: {path}")
        text = p.read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        raise Bad("the script is empty")
    return text


def paragraphs(text):
    return [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _cut(text, rx):
    """Split text after each match of rx, keeping the punctuation with the left piece."""
    out, pos = [], 0
    for m in rx.finditer(text):
        piece = text[pos:m.end()].strip()
        if piece:
            out.append(piece)
        pos = m.end()
    rest = text[pos:].strip()
    if rest:
        out.append(rest)
    return out


def sentences(par):
    return _cut(par, _SENT_END)


def _units(par, max_chars):
    """(text, boundary) units of one paragraph, each <= max_chars unless one word is longer."""
    units = []
    for s in sentences(par):
        if len(s) <= max_chars:
            units.append((s, "sentence"))
            continue
        clauses = _cut(s, _CLAUSE_END)
        for k, c in enumerate(clauses):
            last = k == len(clauses) - 1
            if len(c) <= max_chars:
                units.append((c, "sentence" if last else "clause"))
                continue
            words, cur = c.split(" "), ""
            for w in words:
                if cur and len(cur) + 1 + len(w) > max_chars:
                    units.append((cur, "word"))
                    cur = w
                else:
                    cur = f"{cur} {w}" if cur else w
            units.append((cur, "sentence" if last else "clause"))
    return units


def chunk(text, max_chars=250):
    if max_chars < 20:
        raise Bad("--max-chars must be at least 20")
    chunks = []
    pars = paragraphs(text)
    for pi, par in enumerate(pars):
        cur, kind = "", None
        for u, b in _units(par, max_chars):
            if cur and len(cur) + 1 + len(u) <= max_chars and kind != "word":
                cur, kind = f"{cur} {u}", b
            else:
                if cur:
                    chunks.append((pi, cur, kind))
                cur, kind = u, b
        if cur:
            chunks.append((pi, cur, "paragraph"))
    res = []
    for i, (pi, t, b) in enumerate(chunks, start=1):
        long_words = [w for w in t.split(" ") if len(w) > max_chars]
        res.append({"i": i, "paragraph": pi + 1, "chars": len(t), "words": count_words(t), "ends_at": b,
                    "text": t, **({"overlong_word": True} if long_words else {})})
    return {"max_chars": max_chars, "chunks": len(res), "paragraphs": len(pars),
            "all_within_limit": all(c["chars"] <= max_chars for c in res), "items": res}


def count_words(text) -> int:
    return sum(1 for tok in text.split() if _WORD.search(tok.replace("_", "")))


def estimate(text, wpm=130.0, max_chars=250, sp=0.4, cp=0.2, pp=0.8):
    if not 40 <= wpm <= 400:
        raise Bad("--wpm must be between 40 and 400")
    if min(sp, cp, pp) < 0:
        raise Bad("pauses must be >= 0")
    c = chunk(text, max_chars)
    items, total = [], 0.0  # total stays unrounded; only reported values are rounded
    for it in c["items"]:
        t = it["text"]
        n_s = len(_PUNCT_TERM.findall(t))
        n_c = len(_PUNCT_CLAUSE.findall(t))
        speech = it["words"] / wpm * 60
        pause = n_s * sp + n_c * cp + (pp if it["ends_at"] == "paragraph" else 0)
        # a paragraph end already pauses; do not count the final sentence mark twice
        if it["ends_at"] == "paragraph" and n_s and t.rstrip(CLOSE)[-1:] in TERM:
            pause -= sp
        sec = speech + pause
        items.append({"i": it["i"], "words": it["words"], "sentence_marks": n_s, "clause_marks": n_c,
                      "speech_s": round(speech, 2), "pause_s": round(pause, 2), "seconds": round(sec, 2),
                      "start_s": round(total, 2), "text": t})
        total += sec
    words = sum(i["words"] for i in items)
    return {"wpm": wpm, "words": words, "chunks": len(items), "total_seconds": round(total, 2),
            "total_mmss": "%d:%02d" % divmod(int(round(total)), 60),
            "pauses": {"sentence": sp, "clause": cp, "paragraph": pp}, "items": items,
            "note": "Numbers and abbreviations count as one word; spoken length varies by voice and engine."}


def _wrap_runs(text, rx, other):
    out, pos, n = [], 0, 0
    for m in rx.finditer(text):
        out.append(escape(text[pos:m.start()]))
        run = m.group().rstrip(".-")
        tail = m.group()[len(run):]
        out.append(f'<lang xml:lang="{other}">{escape(run)}</lang>{escape(tail)}')
        pos, n = m.end(), n + 1
    out.append(escape(text[pos:]))
    return "".join(out), n


def ssml(text, lang="ar-EG", other=None, cbreak=200, sbreak=400, pbreak=700):
    if not _LANG.match(lang) or (other and not _LANG.match(other)):
        raise Bad("--lang/--other-lang must be BCP-47 tags such as ar-EG or en-US")
    arabic_main = lang.lower().split("-")[0] in ("ar", "fa", "ur", "ps", "ckb")
    other = other or ("en-US" if arabic_main else "ar-SA")
    rx = _LATIN_RUN if arabic_main else _AR_RUN
    lines, runs, n_s = [f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang}">'], 0, 0
    pars = paragraphs(text)
    for pi, par in enumerate(pars):
        lines.append("<p>")
        sents = sentences(par)
        for si, s in enumerate(sents):
            parts = _cut(s, _CLAUSE_END)
            body = []
            for k, part in enumerate(parts):
                r, n = _wrap_runs(part, rx, other)
                runs += n
                body.append(r + (f'<break time="{cbreak}ms"/>' if k < len(parts) - 1 else ""))
            lines.append(f'<s>{" ".join(body)}</s>' + (f'<break time="{sbreak}ms"/>' if si < len(sents) - 1 else ""))
            n_s += 1
        lines.append("</p>" + (f'<break time="{pbreak}ms"/>' if pi < len(pars) - 1 else ""))
    lines.append("</speak>")
    doc = "\n".join(lines)
    return {"lang": lang, "other_lang": other, "paragraphs": len(pars), "sentences": n_s,
            "other_script_runs": runs, "ssml": doc}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        print(f"TTS_SCRIPT_ERROR: {message}", file=sys.stderr)
        raise SystemExit(2)


def self_test() -> int:
    import xml.etree.ElementTree as ET
    t = "مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n\nفقرة ثانية؟"
    c = chunk(t, 30)
    assert c["all_within_limit"] and " ".join(i["text"] for i in c["items"]).split() == t.split(), c
    assert count_words("وبالكتاب ، نقرأ 2026") == 3
    e = estimate("كلمة " * 130, wpm=130)
    assert abs(e["total_seconds"] - 60.8) < 1e-9, e["total_seconds"]
    doc = ssml(t)["ssml"]
    ET.fromstring(doc)
    assert '<lang xml:lang="en-US">KOSIF Studio</lang>' in doc
    print("self-test: OK")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = _Parser(prog="tts_script.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true", help="run the offline check")
    sub = ap.add_subparsers(dest="cmd", required=True, parser_class=_Parser)
    s = sub.add_parser("chunk"); s.add_argument("file"); s.add_argument("--max-chars", type=int, default=250)
    s = sub.add_parser("estimate"); s.add_argument("file"); s.add_argument("--wpm", type=float, default=130.0)
    s.add_argument("--max-chars", type=int, default=250); s.add_argument("--sentence-pause", type=float, default=0.4)
    s.add_argument("--clause-pause", type=float, default=0.2); s.add_argument("--paragraph-pause", type=float, default=0.8)
    s = sub.add_parser("ssml"); s.add_argument("file"); s.add_argument("--lang", default="ar-EG")
    s.add_argument("--other-lang"); s.add_argument("--xml", action="store_true", help="print the SSML document")
    a = ap.parse_args(argv)
    try:
        text = read(a.file)
        if a.cmd == "chunk":
            r = chunk(text, a.max_chars)
        elif a.cmd == "estimate":
            r = estimate(text, a.wpm, a.max_chars, a.sentence_pause, a.clause_pause, a.paragraph_pause)
        else:
            r = ssml(text, a.lang, a.other_lang)
            if a.xml:
                print(r["ssml"])
                return 0
    except (Bad, OSError, UnicodeDecodeError) as e:
        print(f"TTS_SCRIPT_ERROR: {e}".replace("\n", " "), file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
