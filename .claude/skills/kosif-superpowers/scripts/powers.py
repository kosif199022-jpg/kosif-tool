#!/usr/bin/env python3
"""KOSIF Superpowers — search the power catalog / ابحث في قدراتك.

Python 3 standard library only. Paths resolve from this file.

  python3 powers.py stats                       # counts per family and status
  python3 powers.py search glow neon            # free text (Arabic or English)
  python3 powers.py show GLOW-03                # one power in full
  python3 powers.py family light-glow-bloom     # every power in a family
  python3 powers.py suggest "دعاء هادئ بصوت رجل 9:16"   # powers + styles for a brief
  python3 powers.py styles --genre explainer    # watched reference styles
  python3 powers.py search glow --status proven ready   # filter by status
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
STATUSES = ("proven", "ready", "install", "key", "seen", "documented", "idea")
BADGE = {"proven": "✅", "ready": "🟢", "install": "📦", "key": "🔑", "seen": "👁", "documented": "📄", "idea": "💡"}
RANK = {s: i for i, s in enumerate(STATUSES)}

# Arabic/English intent words → extra search terms, so a brief written in
# plain words still reaches the right families.
INTENT = {
    "دعاء": ["calm", "arabic", "calligraphy", "glow", "particles", "slow"],
    "قرآن": ["calm", "arabic", "calligraphy", "no-music", "glow"],
    "شعر": ["kinetic", "arabic", "calligraphy", "typography"],
    "أغنية": ["beat", "lyrics", "karaoke", "music"],
    "اغنية": ["beat", "lyrics", "karaoke", "music"],
    "موسيقى": ["beat", "audio-reactive", "music"],
    "إعلان": ["ad", "product", "hook", "cta", "logo"],
    "اعلان": ["ad", "product", "hook", "cta", "logo"],
    "منتج": ["product", "ui", "phone", "3d"],
    "تطبيق": ["app", "ui", "phone", "cursor"],
    "بيانات": ["chart", "counter", "data", "infographic"],
    "أرقام": ["chart", "counter", "data"],
    "خريطة": ["map", "route", "geo"],
    "تعليمي": ["explainer", "diagram", "whiteboard"],
    "شرح": ["explainer", "diagram", "whiteboard"],
    "أطفال": ["character", "cartoon", "playful"],
    "قصة": ["story", "character", "narrative"],
    "بودكاست": ["podcast", "captions", "waveform", "talking-head"],
    "مونتاج": ["montage", "cuts", "transitions", "ffmpeg", "grade"],
    "ريلز": ["9:16", "reel", "captions", "hook"],
    "توهج": ["glow", "bloom", "neon"],
    "نيون": ["neon", "glow"],
    "خط": ["typography", "font"],
    "ألوان": ["palette", "color", "grade"],
    "ثلاثي": ["3d", "three"],
    "هادئ": ["calm", "slow", "ease"],
    "سريع": ["fast", "beat", "punch"],
    "فخم": ["luxury", "gold", "serif"],
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[ً-ْـ]", "", s)  # tashkeel and tatweel
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


def load_powers() -> list[dict]:
    out = []
    for p in sorted((DATA / "powers").glob("*.json")):
        try:
            out.extend(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as e:
            print(f"warning: {p.name}: {e}", file=sys.stderr)
    return out


def load_styles() -> list[dict]:
    p = DATA / "styles.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else []


def text_of(p: dict) -> str:
    keys = ("id", "family", "name_ar", "name_en", "what", "how", "params", "tags", "styles")
    return norm(" ".join(json.dumps(p.get(k, ""), ensure_ascii=False) for k in keys))


def score(p: dict, terms: list[str]) -> float:
    t = text_of(p)
    name = norm(f"{p.get('name_ar', '')} {p.get('name_en', '')} {' '.join(p.get('tags') or [])}")
    s = 0.0
    for w in terms:
        w = norm(w)
        if not w:
            continue
        hits = t.count(w)
        if hits:
            s += 1 + min(hits, 5) * 0.3 + (2 if w in name else 0)
    return s - RANK.get(p.get("status"), 6) * 0.05  # prefer proven/ready on ties


def line(p: dict) -> str:
    return f"{p.get('id', '?'):<10} {BADGE.get(p.get('status'), '·')} {p.get('name_ar', '')} — {p.get('name_en', '')}"


def expand(words: list[str]) -> list[str]:
    out = list(words)
    for w in words:
        for k, extra in INTENT.items():
            if norm(k) in norm(w):
                out += extra
    return out


def cmd_stats(powers, styles, _a) -> int:
    fam = Counter(p.get("family") for p in powers)
    st = Counter(p.get("status") for p in powers)
    print(f"powers: {len(powers)} · families: {len(fam)} · watched styles: {sum(1 for s in styles if s.get('watched'))}")
    print("status: " + "  ".join(f"{BADGE[s]} {s} {st.get(s, 0)}" for s in STATUSES))
    for f, n in fam.most_common():
        print(f"  {n:4d}  {f}")
    return 0


def filtered(powers, a):
    if getattr(a, "status", None):
        powers = [p for p in powers if p.get("status") in a.status]
    return powers


def cmd_search(powers, _styles, a) -> int:
    terms = expand(a.words)
    ranked = sorted(((score(p, terms), p) for p in filtered(powers, a)), key=lambda x: -x[0])
    ranked = [(s, p) for s, p in ranked if s > 0][: a.limit]
    if not ranked:
        print("no match / لا نتائج")
        return 1
    for _s, p in ranked:
        print(line(p))
    return 0


def cmd_show(powers, _styles, a) -> int:
    want = a.id.upper()
    for p in powers:
        if str(p.get("id", "")).upper() == want:
            for k in ("id", "family", "name_ar", "name_en", "status", "what", "how", "params", "install", "license", "proof", "styles", "tags"):
                v = p.get(k)
                if v:
                    print(f"{k}: {v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}")
            return 0
    print(f"unknown power id {a.id}")
    return 1


def cmd_family(powers, _styles, a) -> int:
    rows = [p for p in filtered(powers, a) if p.get("family") == a.family]
    if not rows:
        print("families: " + ", ".join(sorted({p.get('family') for p in powers})))
        return 1
    for p in rows:
        print(line(p))
    return 0


def cmd_suggest(powers, styles, a) -> int:
    brief = " ".join(a.brief)
    words = expand(re.findall(r"[\w:]+", brief))
    ranked = sorted(((score(p, words), p) for p in powers), key=lambda x: -x[0])
    picked, fams = [], Counter()
    for s, p in ranked:
        if s <= 0 or len(picked) >= a.limit:
            break
        if fams[p.get("family")] >= 3:  # spread across families
            continue
        fams[p.get("family")] += 1
        picked.append(p)
    print(f"# powers for: {brief}")
    for p in picked:
        print(line(p))
    if styles:
        st = sorted(styles, key=lambda s: -sum(norm(json.dumps(s, ensure_ascii=False)).count(norm(w)) for w in words))[:8]
        print("\n# reference styles to study")
        for s in st:
            print(f"{s.get('id'):<28} {s.get('title_ar', '')} — {s.get('proves_ar', '')}"[:160])
    aspect = re.search(r"\b(9:16|16:9|1:1|4:5)\b", brief)
    print(f"\nformat: {aspect.group(1) if aspect else '9:16 default'} · then: python3 tools/kosif.py scaffold <style> <dir>")
    return 0


def cmd_styles(_powers, styles, a) -> int:
    rows = [s for s in styles if not a.genre or norm(a.genre) in norm(s.get("genre", ""))]
    for s in rows[: a.limit]:
        print(f"{s.get('id'):<28} {s.get('genre', ''):<16} {s.get('title_ar', '')}")
    return 0 if rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="KOSIF Superpowers catalog search / بحث في قدراتك")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats")
    p = sub.add_parser("search"); p.add_argument("words", nargs="+"); p.add_argument("--limit", type=int, default=25); p.add_argument("--status", nargs="+", choices=STATUSES)
    p = sub.add_parser("show"); p.add_argument("id")
    p = sub.add_parser("family"); p.add_argument("family"); p.add_argument("--status", nargs="+", choices=STATUSES)
    p = sub.add_parser("suggest"); p.add_argument("brief", nargs="+"); p.add_argument("--limit", type=int, default=18)
    p = sub.add_parser("styles"); p.add_argument("--genre", default=""); p.add_argument("--limit", type=int, default=300)
    a = ap.parse_args(argv)
    powers, styles = load_powers(), load_styles()
    return {"stats": cmd_stats, "search": cmd_search, "show": cmd_show, "family": cmd_family, "suggest": cmd_suggest, "styles": cmd_styles}[a.cmd](powers, styles, a)


if __name__ == "__main__":
    sys.exit(main())
