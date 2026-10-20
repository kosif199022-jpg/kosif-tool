#!/usr/bin/env python3
"""Convert subtitle or transcription files into the atlas words.json format.

words.json is the master timing file the starters and playbooks use:
  [{"word": "مرحبا", "start": 0.12, "end": 0.48}, ...]   (seconds, floats)

Supported inputs (detected by extension unless --format is given):
  .srt / .vtt      subtitle cues; each cue's words fill its time span, each word getting a share
                   proportional to its letter count (longer words get more time)
  .json            whisper-style output ({"segments":[{"words":[{"word","start","end"}]}]}
                   or a flat list of {"word","start","end"}, or {"words":[...]})
  .csv / .tsv      columns word,start,end (header optional; times in seconds or hh:mm:ss.mmm)

Usage:
  python3 tools/words_convert.py captions.srt words.json
  python3 tools/words_convert.py whisper.json words.json --offset -0.08
  python3 tools/words_convert.py cues.vtt words.json --min-gap 0.02 --format vtt
  python3 tools/words_convert.py words.json starters/html-canvas/words.js   # .js output = window.KOSIF_WORDS

The destination's folder is created when missing. Exit code 2 for an unreadable or unsupported
source, 1 when the source holds no timed words.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

TIME_RE = re.compile(r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{1,3})|(\d{1,2}):(\d{2})[.,](\d{1,3})")


def parse_time(s: str) -> float:
    s = s.strip()
    m = TIME_RE.fullmatch(s)
    if m:
        if m.group(1) is not None:
            h, mi, se, ms = m.group(1, 2, 3, 4)
            return int(h) * 3600 + int(mi) * 60 + int(se) + int(ms.ljust(3, "0")) / 1000
        mi, se, ms = m.group(5, 6, 7)
        return int(mi) * 60 + int(se) + int(ms.ljust(3, "0")) / 1000
    return float(s)


def split_words(text: str) -> list[str]:
    text = re.sub(r"<[^>]+>", " ", text)          # strip inline tags (<i>, <c>, <00:00:01.000>)
    text = re.sub(r"\{[^}]*\}", " ", text)        # strip ASS-style tags
    return [w for w in re.split(r"\s+", text) if w and not re.fullmatch(r"[-–—♪]+", w)]


def from_cues(cues: list[tuple[float, float, str]]) -> list[dict]:
    out = []
    for start, end, text in cues:
        words = split_words(text)
        if not words or end <= start:
            continue
        # weight each word by its length so long words get a little more time
        weights = [max(1, len(re.sub(r"[^\w]", "", w))) for w in words]
        total = sum(weights)
        t = start
        for w, wt in zip(words, weights):
            dur = (end - start) * wt / total
            out.append({"word": w, "start": round(t, 3), "end": round(t + dur, 3)})
            t += dur
    return out


def parse_srt_vtt(text: str) -> list[tuple[float, float, str]]:
    cues = []
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip())
    for block in blocks:
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        if lines[0].strip().upper().startswith(("WEBVTT", "NOTE", "STYLE", "REGION")):
            continue
        idx = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if idx is None:
            continue
        a, b = lines[idx].split("-->")
        b = b.strip().split(" ")[0]  # drop VTT cue settings
        try:
            start, end = parse_time(a), parse_time(b)
        except ValueError:
            continue
        cues.append((start, end, " ".join(lines[idx + 1:])))
    return cues


def parse_json(text: str) -> list[dict]:
    data = json.loads(text)
    words: list[dict] = []
    if isinstance(data, dict) and "segments" in data:
        for seg in data["segments"]:
            if seg.get("words"):
                words.extend(seg["words"])
            elif seg.get("text") and "start" in seg and "end" in seg:
                words.extend(from_cues([(float(seg["start"]), float(seg["end"]), seg["text"])]))
    elif isinstance(data, dict) and "words" in data:
        words = data["words"]
    elif isinstance(data, list):
        words = data
    else:
        raise ValueError("unrecognised JSON layout")
    out = []
    for w in words:
        word = (w.get("word") or w.get("text") or "").strip()
        if not word or "start" not in w or "end" not in w:
            continue
        out.append({"word": word, "start": float(w["start"]), "end": float(w["end"])})
    return out


def parse_csv(text: str, delimiter: str) -> list[dict]:
    rows = list(csv.reader(text.splitlines(), delimiter=delimiter))
    out = []
    for row in rows:
        if len(row) < 3:
            continue
        if row[0].strip().lower() == "word":
            continue
        try:
            out.append({"word": row[0].strip(), "start": parse_time(row[1]), "end": parse_time(row[2])})
        except ValueError:
            continue
    return out


def normalise(words: list[dict], offset: float, min_gap: float) -> list[dict]:
    words = sorted(words, key=lambda w: (w["start"], w["end"]))
    out = []
    for w in words:
        start = round(max(0.0, w["start"] + offset), 3)
        end = round(max(start + 0.02, w["end"] + offset), 3)
        if out and start < out[-1]["end"] + min_gap:
            start = round(out[-1]["end"] + min_gap, 3)
            end = max(end, round(start + 0.02, 3))
        out.append({"word": w["word"], "start": start, "end": end})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--format", choices=["srt", "vtt", "json", "csv", "tsv"])
    ap.add_argument("--offset", type=float, default=0.0, help="seconds added to every timestamp (negative = earlier)")
    ap.add_argument("--min-gap", type=float, default=0.0, help="minimum gap enforced between consecutive words")
    args = ap.parse_args()
    src = Path(args.src)
    fmt = args.format or src.suffix.lower().lstrip(".")
    if fmt not in ("srt", "vtt", "json", "csv", "tsv"):
        print(f"unsupported format: {fmt or '(no extension)'}; use --format srt|vtt|json|csv|tsv", file=sys.stderr)
        return 2
    if not src.is_file():
        print(f"source file not found: {src}", file=sys.stderr)
        return 2
    try:
        text = src.read_text(encoding="utf-8-sig")
        if fmt in ("srt", "vtt"):
            words = from_cues(parse_srt_vtt(text))
        elif fmt == "json":
            words = parse_json(text)
        else:
            words = parse_csv(text, "\t" if fmt == "tsv" else ",")
    except (OSError, ValueError, TypeError, AttributeError) as exc:  # unreadable, not UTF-8, malformed JSON or layout
        print(f"cannot read {src} as {fmt}: {exc}", file=sys.stderr)
        return 2
    words = normalise(words, args.offset, args.min_gap)
    if not words:
        print("no words found", file=sys.stderr)
        return 1
    payload = json.dumps(words, ensure_ascii=False, indent=1)
    if args.dst.lower().endswith(".js"):
        payload = "// Generated by tools/words_convert.py — same data as words.json\nwindow.KOSIF_WORDS = " + payload + ";"
    dst = Path(args.dst)
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(payload + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"cannot write {dst}: {exc}", file=sys.stderr)
        return 2
    print(f"wrote {len(words)} words to {args.dst} ({words[0]['start']:.2f}s → {words[-1]['end']:.2f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
