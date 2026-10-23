#!/usr/bin/env python3
"""KOSIF Caption Lines — يقسم كلمات التفريغ إلى سطور ترجمة مقروءة (فكرة من دراسة «مونتاجي»، كود أصلي).

Idea learnt from a read-only study of the Montaji 1.0.0 macOS editor (an Arabic CapCut-style app that runs
whisper.cpp locally): word timings are only half of auto captions; the other half is a set of reading rules that
turns words into short lines, plus a filter for the phrases speech models invent over silence or music. This is
KOSIF's own implementation with its own rules and phrase list; no Montaji code is used.

  python3 caption_lines.py group WORDS.json -o captions.srt [--max-words 4] [--max-chars 32] [--max-dur 3.2]
                                 [--gap 0.6] [--min-dur 0.4] [--bridge 0.3] [--rlm] [--keep-suspect]
  python3 caption_lines.py lint CAPTIONS.json|.srt|.vtt [--max-cps 17] [--json]

WORDS may be the atlas words.json ([{word,start,end}] in seconds), {"words": [...]}, whisper.cpp -oj output
(transcription[].offsets in ms, with -ml 1 for one word per entry), or faster-whisper/openai style
(segments[].words[] with word/start/end). Output follows the -o extension: .srt, .vtt or .json
(schema kosif.caption-lines.v1). Python 3.8+ standard library only; reads and writes local files, no network.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = "kosif.caption-lines.v1"
END_PUNCT = re.compile(r"[.!?؟؛:…]$")       # a sentence or clause ends: always break after it
SOFT_PUNCT = re.compile(r"[،,]$")            # a comma: break only when the line already has two words
RTL = re.compile(r"[֐-ࣿיִ-﷿ﹰ-ﻼ]")
RLM = "‏"

# Phrases speech models write over silence, music or channel outros. Kept short and generic; a line that matches
# is dropped (or marked with --keep-suspect) and listed in the report so a person can restore it.
SUSPECT = [
    (re.compile(r"ترجم(ة|ه)\s+نانسي"), "subtitle-credit"),
    (re.compile(r"(لا\s+تنس(ى|وا)?\s+)?(ال)?اشتراك\s+(في|ب)\s*(ال)?قنا(ة|ه)|اشترك(وا)?\s+(في|ب)\s*(ال)?قنا(ة|ه)"), "outro"),
    (re.compile(r"شكرا\s+(لكم\s+)?(على|علي)\s+(ال)?مشاهد(ة|ه)"), "outro"),
    (re.compile(r"amara\.org|subtitles?\s+(by|made)|transcribed\s+by", re.I), "subtitle-credit"),
    (re.compile(r"thank(s| you)\s+for\s+watching|please\s+subscribe", re.I), "outro"),
    (re.compile(r"^\W*(music|موسيقى|\[.*\]|\(.*\))\W*$", re.I), "sound-tag"),
    (re.compile(r"^[\s.…·\-–—]*$"), "punctuation-only"),
]


# ---------------------------------------------------------------- input

def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load_words(path: Path) -> list[dict]:
    """Normalise any supported word-timing file to [{"text", "start", "end"}] in seconds, sorted by start."""
    data = json.loads(path.read_text(encoding="utf-8"))
    raw: list = []
    if isinstance(data, dict) and isinstance(data.get("transcription"), list):          # whisper.cpp -oj
        for s in data["transcription"]:
            off = s.get("offsets") or {}
            raw.append({"text": s.get("text", ""), "start": (_num(off.get("from")) or 0) / 1000,
                        "end": (_num(off.get("to")) or 0) / 1000})
    elif isinstance(data, dict) and isinstance(data.get("segments"), list):            # faster-whisper / openai
        for seg in data["segments"]:
            for w in seg.get("words") or []:
                raw.append({"text": w.get("word", w.get("text", "")), "start": _num(w.get("start")), "end": _num(w.get("end"))})
    else:
        items = data.get("words") if isinstance(data, dict) else data
        if not isinstance(items, list):
            raise SystemExit(f"caption_lines: {path} has no word list")
        for w in items:
            raw.append({"text": w.get("word", w.get("text", "")), "start": _num(w.get("start")), "end": _num(w.get("end"))})
    words = []
    for w in raw:
        text = str(w["text"] or "").strip()
        if not text or w["start"] is None or w["end"] is None:
            continue
        start, end = float(w["start"]), float(w["end"])
        words.append({"text": text, "start": start, "end": max(end, start)})
    words.sort(key=lambda w: w["start"])
    return words


# ---------------------------------------------------------------- grouping

def group(words: list[dict], max_words=4, max_chars=32, max_dur=3.2, gap=0.6, min_dur=0.4, bridge=0.3) -> list[dict]:
    """Greedy line builder. A new line starts when the next word would break any reading rule."""
    lines: list[dict] = []
    cur = None
    for w in words:
        if cur is not None:
            joined = len(cur["text"]) + 1 + len(w["text"])
            reason = None
            if cur["n"] >= max_words:
                reason = "max-words"
            elif joined > max_chars:
                reason = "max-chars"
            elif w["start"] - cur["end"] > gap:
                reason = "pause"
            elif w["end"] - cur["start"] > max_dur:
                reason = "max-dur"
            elif END_PUNCT.search(cur["text"]):
                reason = "sentence-end"
            elif SOFT_PUNCT.search(cur["text"]) and cur["n"] >= 2:
                reason = "comma"
            if reason:
                cur["break"] = reason
                lines.append(cur)
                cur = None
        if cur is None:
            cur = {"start": w["start"], "end": w["end"], "text": w["text"], "n": 1}
        else:
            cur["text"] += " " + w["text"]
            cur["end"] = w["end"]
            cur["n"] += 1
    if cur is not None:
        cur["break"] = "end"
        lines.append(cur)
    # Close short holes so captions do not flicker, then give each line a readable minimum without overlapping.
    for a, b in zip(lines, lines[1:]):
        if 0 <= b["start"] - a["end"] < bridge:
            a["end"] = b["start"]
    for i, ln in enumerate(lines):
        limit = lines[i + 1]["start"] if i + 1 < len(lines) else None
        want = ln["start"] + min_dur
        if ln["end"] < want:
            ln["end"] = want if limit is None else max(ln["end"], min(want, limit))
    return lines


def screen(lines: list[dict], keep_suspect=False) -> tuple[list[dict], list[dict]]:
    """Drop (or flag) suspected model inventions and runs of three or more identical lines."""
    kept, dropped = [], []
    run = 0
    for i, ln in enumerate(lines):
        run = run + 1 if i and ln["text"] == lines[i - 1]["text"] else 1
        why = next((tag for rx, tag in SUSPECT if rx.search(ln["text"])), None)
        if why is None and run >= 3:
            why = "repeat-loop"
        if why:
            ln["suspect"] = why
            dropped.append(ln)
            if not keep_suspect:
                continue
        kept.append(ln)
    return kept, dropped


# ---------------------------------------------------------------- output

def _ts(t: float, sep: str) -> str:
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def _display(text: str, rlm: bool) -> str:
    return RLM + text if rlm and RTL.search(text) else text


def to_srt(lines, rlm=False) -> str:
    return "".join(f"{i}\n{_ts(ln['start'], ',')} --> {_ts(ln['end'], ',')}\n{_display(ln['text'], rlm)}\n\n"
                   for i, ln in enumerate(lines, 1))


def to_vtt(lines, rlm=False) -> str:
    return "WEBVTT\n\n" + "".join(f"{_ts(ln['start'], '.')} --> {_ts(ln['end'], '.')}\n{_display(ln['text'], rlm)}\n\n"
                                  for ln in lines)


def _round(lines):
    out = []
    for ln in lines:
        row = {"start": round(ln["start"], 3), "end": round(ln["end"], 3), "text": ln["text"], "words": ln["n"]}
        for k in ("break", "suspect"):
            if ln.get(k):
                row[k] = ln[k]
        out.append(row)
    return out


# ---------------------------------------------------------------- lint

def parse_captions(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        return [{"start": float(c["start"]), "end": float(c["end"]), "text": c["text"]}
                for c in (data.get("captions") if isinstance(data, dict) else data)]
    out = []
    rx = re.compile(r"(\d+):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d+):(\d{2}):(\d{2})[,.](\d{3})")
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        rows = block.strip().split("\n")
        for i, row in enumerate(rows):
            m = rx.search(row)
            if m:
                g = [int(x) for x in m.groups()]
                out.append({"start": g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000,
                            "end": g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                            "text": " ".join(rows[i + 1:]).replace(RLM, "").strip()})
                break
    return out


def lint(caps: list[dict], max_cps=17.0, min_dur=0.3) -> list[dict]:
    issues = []
    for i, c in enumerate(caps):
        dur = c["end"] - c["start"]
        if dur <= 0:
            issues.append({"line": i + 1, "issue": "non-positive duration"})
            continue
        if dur < min_dur:
            issues.append({"line": i + 1, "issue": f"shorter than {min_dur}s ({dur:.2f}s)"})
        cps = len(c["text"].replace(" ", "")) / dur
        if cps > max_cps:
            issues.append({"line": i + 1, "issue": f"reading speed {cps:.1f} chars/s > {max_cps}"})
        if i and c["start"] < caps[i - 1]["end"] - 1e-3:
            issues.append({"line": i + 1, "issue": "overlaps the previous line"})
        why = next((tag for rx, tag in SUSPECT if rx.search(c["text"])), None)
        if why:
            issues.append({"line": i + 1, "issue": f"suspected model invention ({why})"})
    return issues


# ---------------------------------------------------------------- CLI

def cmd_group(a) -> int:
    words = load_words(Path(a.words))
    if not words:
        print("caption_lines: no timed words found", file=sys.stderr)
        return 1
    lines = group(words, a.max_words, a.max_chars, a.max_dur, a.gap, a.min_dur, a.bridge)
    kept, dropped = screen(lines, a.keep_suspect)
    out = Path(a.output)
    ext = out.suffix.lower()
    if ext == ".srt":
        body = to_srt(kept, a.rlm)
    elif ext == ".vtt":
        body = to_vtt(kept, a.rlm)
    elif ext == ".json":
        body = json.dumps({"schema": SCHEMA, "source": Path(a.words).name,
                           "rules": {k: getattr(a, k) for k in ("max_words", "max_chars", "max_dur", "gap", "min_dur", "bridge")},
                           "captions": _round(kept), "dropped": _round(dropped)}, ensure_ascii=False, indent=1) + "\n"
    else:
        print("caption_lines: -o must end in .srt, .vtt or .json", file=sys.stderr)
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"{len(words)} words → {len(kept)} lines → {out}" + (f" · {len(dropped)} suspect line(s) "
          f"{'kept and marked' if a.keep_suspect else 'dropped'}: " + "; ".join(f"{d['text']!r} ({d['suspect']})" for d in dropped)
          if dropped else ""))
    return 0


def cmd_lint(a) -> int:
    caps = parse_captions(Path(a.captions))
    issues = lint(caps, a.max_cps, a.min_dur)
    if a.json:
        print(json.dumps({"lines": len(caps), "issues": issues}, ensure_ascii=False, indent=1))
    else:
        print(f"{len(caps)} lines, {len(issues)} issue(s)")
        for it in issues:
            print(f"  line {it['line']}: {it['issue']}")
    return 1 if issues else 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Turn word timings into readable caption lines (SRT/VTT/JSON) and lint caption files.")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("group", help="words.json / whisper JSON → caption lines")
    g.add_argument("words")
    g.add_argument("-o", "--output", required=True, help="captions.srt | .vtt | .json")
    g.add_argument("--max-words", type=int, default=4)
    g.add_argument("--max-chars", type=int, default=32)
    g.add_argument("--max-dur", type=float, default=3.2, help="longest line on screen, seconds")
    g.add_argument("--gap", type=float, default=0.6, help="a pause longer than this starts a new line")
    g.add_argument("--min-dur", type=float, default=0.4, help="shortest line, extended into the following silence only")
    g.add_argument("--bridge", type=float, default=0.3, help="holes shorter than this are closed")
    g.add_argument("--rlm", action="store_true", help="prefix Arabic lines with U+200F so players keep end punctuation on the left")
    g.add_argument("--keep-suspect", action="store_true", help="keep suspected model inventions, marked in JSON")
    g.set_defaults(fn=cmd_group)
    l = sub.add_parser("lint", help="check overlaps, durations, reading speed and suspect phrases")
    l.add_argument("captions")
    l.add_argument("--max-cps", type=float, default=17.0)
    l.add_argument("--min-dur", type=float, default=0.3)
    l.add_argument("--json", action="store_true")
    l.set_defaults(fn=cmd_lint)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
