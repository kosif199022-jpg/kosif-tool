#!/usr/bin/env python3
"""يحوّل كلمات بطوابع زمنية (Whisper/whisper.cpp JSON أو SRT) إلى صفحات ترجمة بأسلوب تيك توك + SRT + VTT + ASS كاريوكي.

usage: python captions_pages.py words.json [--page-ms 1200] [--max-chars 42] [--out captions] [--rtl]
words.json يقبل: [{"text":" كلمة","start":0.12,"end":0.40}, …] أو مخرج whisper.cpp ({"transcription":[{"timestamps":…,"offsets":{"from":ms,"to":ms},"text":…}]})
أو ملف SRT (يُقسَّم إلى كلمات بتوزيع زمني متساوٍ داخل كل سطر).
المخرج: captions.json (pages بتوكنات fromMs/toMs)، captions.srt، captions.vtt، captions.ass (إبراز الكلمة بـ \\k).
"""
import argparse
import json
import re
import sys


def ms(t):
    return int(round(float(t) * 1000))


def parse_srt(text):
    words = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", lines[1] if "-->" in lines[1] else lines[0])
        if not m:
            continue
        h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, m.groups())
        a = ((h1 * 60 + m1) * 60 + s1) * 1000 + ms1; b = ((h2 * 60 + m2) * 60 + s2) * 1000 + ms2
        txt = " ".join(l for l in lines[2:] if "-->" not in l) if "-->" in lines[1] else " ".join(lines[1:])
        toks = txt.split()
        if not toks:
            continue
        step = (b - a) / len(toks)
        for i, w in enumerate(toks):
            words.append({"text": (" " if words else "") + w, "fromMs": int(a + i * step), "toMs": int(a + (i + 1) * step)})
    return words


def load_words(path):
    raw = open(path, encoding="utf-8").read()
    if path.lower().endswith(".srt"):
        return parse_srt(raw)
    data = json.loads(raw)
    words = []
    if isinstance(data, dict) and "transcription" in data:  # whisper.cpp
        for seg in data["transcription"]:
            for tok in seg.get("tokens", []) or [seg]:
                off = tok.get("offsets") or seg.get("offsets") or {}
                t = tok.get("text", "")
                if t.strip() and not t.startswith("[_"):
                    words.append({"text": t, "fromMs": int(off.get("from", 0)), "toMs": int(off.get("to", 0))})
    elif isinstance(data, dict) and "segments" in data:  # openai-whisper with word_timestamps
        for seg in data["segments"]:
            for w in seg.get("words", []):
                words.append({"text": (" " if words else "") + w["word"].strip(), "fromMs": ms(w["start"]), "toMs": ms(w["end"])})
    else:
        for w in data:
            words.append({"text": w["text"] if w["text"].startswith(" ") or not words else " " + w["text"], "fromMs": ms(w["start"]), "toMs": ms(w["end"])})
    return words


def make_pages(words, page_ms, max_chars):
    pages, cur = [], None
    for w in words:
        if cur is None or (w["fromMs"] - cur["startMs"] >= page_ms) or (len(cur["text"]) + len(w["text"]) > max_chars * 2):
            cur = {"startMs": w["fromMs"], "text": "", "tokens": []}; pages.append(cur)
        cur["tokens"].append(w); cur["text"] += w["text"]
    for i, p in enumerate(pages):
        nxt = pages[i + 1]["startMs"] if i + 1 < len(pages) else None
        p["endMs"] = min(nxt, p["tokens"][-1]["toMs"] + 150) if nxt else p["tokens"][-1]["toMs"] + 150
        p["text"] = p["text"].strip()
    return pages


def tc(msv, sep=","):
    h, r = divmod(msv, 3600000); m, r = divmod(r, 60000); s, r = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{r:03d}"


def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > max_chars and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return "\n".join(lines[:2]) if len(lines) <= 2 else "\n".join([" ".join(lines[:-1]), lines[-1]])[:max_chars * 2 + 1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("words"); ap.add_argument("--page-ms", type=int, default=1200); ap.add_argument("--max-chars", type=int, default=42)
    ap.add_argument("--out", default="captions"); ap.add_argument("--rtl", action="store_true")
    a = ap.parse_args()
    words = load_words(a.words)
    if not words:
        sys.exit("لا كلمات")
    pages = make_pages(words, a.page_ms, a.max_chars)
    open(a.out + ".json", "w", encoding="utf-8").write(json.dumps({"pages": pages, "rtl": a.rtl}, ensure_ascii=False))
    srt, vtt = [], ["WEBVTT", ""]
    for i, p in enumerate(pages, 1):
        body = wrap(p["text"], a.max_chars)
        srt += [str(i), f"{tc(p['startMs'])} --> {tc(p['endMs'])}", body, ""]
        vtt += [f"{tc(p['startMs'], '.')} --> {tc(p['endMs'], '.')}", body, ""]
    open(a.out + ".srt", "w", encoding="utf-8").write("\n".join(srt)); open(a.out + ".vtt", "w", encoding="utf-8").write("\n".join(vtt))
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "",
           "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Karaoke,Cairo,64,&H00FFFFFF,&H0008E539,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,0,2,60,60,320,1", "",
           "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for p in pages:
        parts, t0 = [], p["startMs"]
        for tok in p["tokens"]:
            dur_cs = max(1, int(round((tok["toMs"] - max(tok["fromMs"], t0)) / 10)))
            parts.append(f"{{\\k{dur_cs}}}{tok['text']}"); t0 = tok["toMs"]
        ass.append(f"Dialogue: 0,{tc(p['startMs'], '.')[:-1]},{tc(p['endMs'], '.')[:-1]},Karaoke,,0,0,0,,{''.join(parts).strip()}")
    open(a.out + ".ass", "w", encoding="utf-8").write("\n".join(ass))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps({"words": len(words), "pages": len(pages), "files": [a.out + e for e in (".json", ".srt", ".vtt", ".ass")],
                      "check": "تزامن الكلمة المبرزة ±1 إطار على 5 عينات؛ لا تغطية للوجوه"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
