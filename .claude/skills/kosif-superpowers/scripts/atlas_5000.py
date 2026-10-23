#!/usr/bin/env python3
"""KOSIF Atlas-5000 coverage map — خريطة تغطية «أطلس الـ5000 مهارة».

The "5000-skill atlas" is the safe core of https://github.com/kosif199022-jpg/kosif-atlas: the skills
whose KOSIF inspection verdict is READ_ONLY_OK, whose license is permissive (not copyleft) and that
carry no risk flags. This tool answers, offline and read-only, three questions Claude needs before it
can say what it knows and what it could still learn:

  stats   how many safe Atlas skills exist per theme, and how many are already distilled into a
          KOSIF power (a power whose proof links point at that Atlas folder)
  gaps    which themes have the most safe skills not yet distilled, with the next candidates
  find    which safe Atlas skills match a task, and which KOSIF power already covers each one
  show    one Atlas skill's metadata and its covering powers

  python3 scripts/atlas_5000.py stats --json
  python3 scripts/atlas_5000.py gaps --top 8
  python3 scripts/atlas_5000.py find "storyboard character webtoon" --top 10
  python3 scripts/atlas_5000.py show 2425

Inputs are data/atlas_capability_index.json.gz (metadata of all 14,793 Atlas skills, read as inert
text) and data/powers/*.json. It never opens the network, never reads or runs Atlas code, and a
"covered" mark means only that a power cites the folder, not that the skill was executed.
Python 3.8+ standard library.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
INDEX = SKILL / "data" / "atlas_capability_index.json.gz"
POWERS = SKILL / "data" / "powers"
CITE = re.compile(r"kosif-atlas/(?:tree|blob)/[^/\s\"]+/(skills/[^/\s\"]+/[^/\s\")]+)")
TOKEN = re.compile(r"[a-z0-9]+|[؀-ۿ]+")
# A few Arabic request words mapped to the English vocabulary of Atlas descriptions.
ALIASES = {
    "رسم": "draw drawing illustration sketch", "رسوم": "illustration drawing", "شخصية": "character",
    "ويبتون": "webtoon comic", "قصة": "story storytelling", "مصورة": "comic illustration",
    "أيقونة": "icon", "شعار": "logo brand", "ألوان": "color palette", "خط": "font typography",
    "فيديو": "video", "مونتاج": "video edit ffmpeg", "موشن": "motion animation", "حركة": "motion animation",
    "شيدر": "shader glsl", "لعبة": "game", "ألعاب": "game", "صوت": "audio voice", "ترجمة": "translate",
    "اختبار": "test testing", "أمان": "security", "مراجعة": "review", "توثيق": "documentation docs",
    "كتابة": "writing", "تسويق": "marketing", "سيو": "seo", "منتج": "product", "تخطيط": "planning",
    "بيانات": "data", "واجهة": "ui interface design", "تصميم": "design",
}


def is_safe(s: dict) -> bool:
    return s.get("verdict") == "READ_ONLY_OK" and not s.get("copyleft") and not s.get("risk")


def load_index(path: Path = INDEX) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def coverage_map(powers_dir: Path = POWERS) -> dict:
    """Atlas folder path -> sorted list of power ids whose proof/source text cites it."""
    cov = collections.defaultdict(set)
    for f in sorted(powers_dir.glob("*.json")):
        for rec in json.loads(f.read_text(encoding="utf-8")):
            text = json.dumps([rec.get("proof"), rec.get("source"), rec.get("atlas")], ensure_ascii=False)
            for m in CITE.findall(text):
                cov[m].add(rec["id"])
    return {k: sorted(v) for k, v in cov.items()}


def safe_skills(idx: dict) -> list:
    return [s for s in idx["skills"] if is_safe(s)]


def stats(idx: dict, cov: dict) -> dict:
    safe = safe_skills(idx)
    themes = collections.OrderedDict()
    per = collections.defaultdict(lambda: [0, 0])
    for s in safe:
        per[s["theme"]][0] += 1
        if s["path"] in cov:
            per[s["theme"]][1] += 1
    for t, (n, c) in sorted(per.items(), key=lambda kv: (-kv[1][0], kv[0])):
        themes[t] = {"safe": n, "covered": c, "coverage_pct": round(100.0 * c / n, 1)}
    covered = sum(v["covered"] for v in themes.values())
    powers = sorted({p for s in safe for p in cov.get(s["path"], [])})
    return {
        "atlas_total": idx.get("count", len(idx["skills"])),
        "safe_core": len(safe),
        "safe_rule": "verdict READ_ONLY_OK, permissive license (not copyleft), no risk flags",
        "covered": covered,
        "coverage_pct": round(100.0 * covered / len(safe), 1) if safe else 0.0,
        "powers_citing_safe_core": len(powers),
        "themes": themes,
        "note": "covered = a KOSIF power cites the Atlas folder; it is not an execution receipt.",
    }


def gaps(idx: dict, cov: dict, top: int = 8, per_theme: int = 3) -> list:
    st = stats(idx, cov)["themes"]
    out = []
    rows = sorted(st.items(), key=lambda kv: (-(kv[1]["safe"] - kv[1]["covered"]), kv[0]))[:top]
    safe = safe_skills(idx)
    for theme, v in rows:
        cands = [s for s in safe if s["theme"] == theme and s["path"] not in cov and not s.get("desc_dupes")]
        cands.sort(key=lambda s: (-min(s.get("md_bytes", 0), 20000), s["id"]))
        seen, picks = set(), []
        for s in cands:
            if s["plugin"] in seen:
                continue
            seen.add(s["plugin"])
            picks.append(brief(s, cov))
            if len(picks) >= per_theme:
                break
        out.append({"theme": theme, "uncovered": v["safe"] - v["covered"], **v, "next_candidates": picks})
    return out


def tokens(text: str) -> list:
    words = TOKEN.findall((text or "").lower())
    out = []
    for w in words:
        out.append(w)
        for k, v in ALIASES.items():
            if k in w:
                out.extend(v.split())
    return out


def find(idx: dict, cov: dict, query: str, top: int = 10, uncovered_only: bool = False) -> list:
    q = set(tokens(query))
    if not q:
        return []
    hits = []
    for s in safe_skills(idx):
        if uncovered_only and s["path"] in cov:
            continue
        name = set(tokens(s["skill"] + " " + s["plugin"]))
        desc = set(tokens(s.get("desc", "")))
        theme = set(tokens(s.get("theme", "") + " " + s.get("theme2", "")))
        score = 5 * len(q & name) + 2 * len(q & theme) + len(q & desc)
        if score:
            hits.append((score, s["path"] in cov, -s["id"], s))
    hits.sort(key=lambda h: (-h[0], not h[1], h[2]))
    return [dict(brief(h[3], cov), score=h[0]) for h in hits[:top]]


def brief(s: dict, cov: dict) -> dict:
    return {
        "id": s["id"], "plugin": s["plugin"], "skill": s["skill"], "theme": s["theme"],
        "license": s.get("license"), "desc": (s.get("desc") or "")[:160],
        "url": "https://github.com/kosif199022-jpg/kosif-atlas/tree/main/" + s["path"],
        "covered_by": cov.get(s["path"], []),
    }


def show(idx: dict, cov: dict, atlas_id: int) -> dict:
    for s in idx["skills"]:
        if s["id"] == atlas_id:
            rec = brief(s, cov)
            rec.update(desc=s.get("desc"), verdict=s.get("verdict"), copyleft=s.get("copyleft"),
                       risk=s.get("risk"), safe_core=is_safe(s), source=s.get("source"))
            return rec
    raise KeyError(atlas_id)


def _print(obj, as_json: bool) -> None:
    if as_json:
        print(json.dumps(obj, ensure_ascii=False, indent=1))
        return
    if isinstance(obj, dict) and "themes" in obj:
        print(f"Atlas {obj['atlas_total']:,} skills · safe core {obj['safe_core']:,} · covered "
              f"{obj['covered']:,} ({obj['coverage_pct']}%) by {obj['powers_citing_safe_core']} powers")
        for t, v in obj["themes"].items():
            print(f"  {t:28} {v['safe']:5} safe  {v['covered']:4} covered  {v['coverage_pct']:5}%")
        return
    for row in obj if isinstance(obj, list) else [obj]:
        if "next_candidates" in row:
            print(f"{row['theme']}: {row['uncovered']} uncovered of {row['safe']}")
            for c in row["next_candidates"]:
                print(f"    #{c['id']} {c['plugin']}/{c['skill']} — {c['desc'][:90]}")
        else:
            cov = ", ".join(row["covered_by"]) or "not yet distilled"
            print(f"#{row['id']} {row['plugin']}/{row['skill']} [{row['theme']}] → {cov}\n    {row['desc'][:120]}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--index", type=Path, default=INDEX, help="atlas metadata index (.json.gz)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("stats", help="safe-core size and coverage per theme"); a.add_argument("--json", action="store_true")
    b = sub.add_parser("gaps", help="themes with most undistilled safe skills")
    b.add_argument("--top", type=int, default=8); b.add_argument("--per-theme", type=int, default=3)
    b.add_argument("--json", action="store_true")
    c = sub.add_parser("find", help="safe Atlas skills matching a task")
    c.add_argument("query"); c.add_argument("--top", type=int, default=10)
    c.add_argument("--uncovered", action="store_true", help="only skills no power cites yet")
    c.add_argument("--json", action="store_true")
    d = sub.add_parser("show", help="one Atlas skill by numeric id"); d.add_argument("id", type=int)
    d.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    idx, cov = load_index(args.index), coverage_map()
    if args.cmd == "stats":
        _print(stats(idx, cov), args.json)
    elif args.cmd == "gaps":
        _print(gaps(idx, cov, max(1, min(args.top, 50)), max(1, min(args.per_theme, 10))), args.json)
    elif args.cmd == "find":
        _print(find(idx, cov, args.query, max(1, min(args.top, 50)), args.uncovered), args.json)
    else:
        try:
            _print(show(idx, cov, args.id), args.json)
        except KeyError:
            print(f"unknown Atlas id {args.id}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
