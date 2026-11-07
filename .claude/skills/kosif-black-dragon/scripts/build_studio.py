#!/usr/bin/env python3
"""Black Dragon 3D Build Studio: turn a task into a staged Blender/Unreal brief.

Native, deterministic planning only. It never launches Blender or Unreal, never
downloads assets and never spends money. It reads the local recipe file
(`data/build3d_recipes.json`), which holds 21 build recipes and 18 working
principles studied from a public 3D build library and rewritten in our own
words. Matching is lexical, not semantic.

Commands (run from the repository root):
  build_studio.py list
  build_studio.py principles
  build_studio.py match "اعمل فيديو دوّار لزجاجة عطر"
  build_studio.py brief product-turntable --fill product="زجاجة عطر 50 مل"
  build_studio.py brief "شعار متحرك للقناة" --format md
  build_studio.py lint --text "Make a 3D logo intro in Blender"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "build3d_recipes.json"
STATUS = "PLANNING_BRIEF_NOT_A_RENDER"

_DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_PREFIXES = ("وال", "بال", "فال", "كال", "لل", "ال", "و", "ب", "ل")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", str(text)).lower()
    text = _DIACRITICS.sub("", text)
    text = re.sub("[إأآٱ]", "ا", text).replace("ى", "ي").replace("ة", "ه")
    return text


def tokens(text: str) -> set[str]:
    out: set[str] = set()
    for tok in re.findall(r"[\w؀-ۿ]+", normalize(text)):
        out.add(tok)
        for pre in _PREFIXES:
            if tok.startswith(pre) and len(tok) - len(pre) >= 3:
                out.add(tok[len(pre):])
                break
    return out


def load(path: Path = DATA) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    ids = [r["id"] for r in data["recipes"]]
    pids = {p["id"] for p in data["principles"]}
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate recipe id")
    for r in data["recipes"]:
        missing = set(r["principles"]) - pids
        if missing:
            raise ValueError(f"{r['id']} cites unknown principles {sorted(missing)}")
    return data


def _keyword_hits(task_norm: str, task_toks: set[str], keyword: str) -> bool:
    kw = normalize(keyword)
    if " " in kw:
        return kw in task_norm
    return bool(tokens(kw) & task_toks)


def match(task: str, data: dict, limit: int = 3) -> list[dict]:
    task_norm, task_toks = normalize(task), tokens(task)
    ranked = []
    for r in data["recipes"]:
        hits = [k for k in r["keywords"] if _keyword_hits(task_norm, task_toks, k)]
        if hits:
            ranked.append({"id": r["id"], "title_ar": r["title_ar"], "score": len(hits),
                           "matched_keywords": hits, "engines": r["engines"], "level": r["level"]})
    ranked.sort(key=lambda x: (-x["score"], x["id"]))
    return ranked[:limit]


def _recipe(ref: str, data: dict) -> tuple[dict, list[dict]]:
    by_id = {r["id"]: r for r in data["recipes"]}
    if ref in by_id:
        return by_id[ref], []
    found = match(ref, data)
    if not found:
        raise ValueError("no recipe matched; run `list` and pass a recipe id")
    return by_id[found[0]["id"]], found


def brief(ref: str, data: dict, fills: dict[str, str] | None = None) -> dict:
    fills = dict(fills or {})
    recipe, candidates = _recipe(ref, data)
    known = {i["key"] for i in recipe["inputs"]}
    unknown = sorted(set(fills) - known)
    if unknown:
        raise ValueError(f"unknown input keys for {recipe['id']}: {unknown}; expected {sorted(known)}")
    principles = {p["id"]: p for p in data["principles"]}
    big = recipe["level"] == "advanced" or "unreal" in recipe["engines"]
    applied = list(dict.fromkeys(["P01", "P02", "P05"] + (["P03", "P04"] if big else []) + recipe["principles"]))
    return {
        "status": STATUS,
        "recipe": recipe["id"],
        "title_ar": recipe["title_ar"],
        "engines": recipe["engines"],
        "level": recipe["level"],
        "time_estimate": recipe["time"],
        "candidates": candidates,
        "inputs": [{"key": i["key"], "ar": i["ar"], "value": fills.get(i["key"])} for i in recipe["inputs"]],
        "open_questions": [i["ar"] for i in recipe["inputs"] if not fills.get(i["key"])],
        "stages": (["خطة/مسقط للموافقة"] if big else []) + recipe["steps_ar"],
        "deliverables": recipe["deliverables_ar"],
        "gates": ["رندر لقطات ومراجعتها ذاتياً قبل العرض"] + recipe["gates_ar"],
        "variant_axes": recipe["variants_ar"],
        "principles": [{"id": p, "ar": principles[p]["ar"]} for p in applied],
        "guardrails": data["operator_kit"]["setup_contract_ar"],
        "execution_note": "خطة فقط: لم يُشغَّل Blender أو Unreal ولم يُنزَّل أي أصل. التنفيذ يحتاج البرنامج على جهاز المالك وموافقته.",
    }


def to_markdown(b: dict) -> str:
    lines = [f"# {b['title_ar']} — `{b['recipe']}`", "",
             f"المحرك: {' + '.join(b['engines'])} · المستوى: {b['level']} · الوقت: {b['time_estimate']}", "",
             "## المدخلات"]
    for i in b["inputs"]:
        lines.append(f"- {i['ar']}: {i['value'] if i['value'] else '❓ مطلوب من المالك'}")
    sections = (("مراحل البناء", b["stages"], True), ("المخرجات", b["deliverables"], False),
                ("بوابات الفحص قبل العرض", b["gates"], False), ("محاور تنويع للمتابعة", b["variant_axes"], False),
                ("قواعد التشغيل", b["guardrails"], False))
    for title, items, numbered in sections:
        lines += ["", f"## {title}"]
        lines += [f"{n}. {x}" if numbered else f"- {x}" for n, x in enumerate(items, 1)]
    lines += ["", "## مبادئ مطبقة"] + [f"- **{p['id']}** {p['ar']}" for p in b["principles"]]
    lines += ["", f"> {b['execution_note']}", ""]
    return "\n".join(lines)


_CHECKS = (
    ("self_check", "P02", r"check|verify|look at|review|screenshot|افحص|راجع|تاكد|لقطه"),
    ("output_spec", "P11", r"\d{3,4}\s*[x×]\s*\d{3,4}|\b4k\b|\d+\s*(?:fps|second|sec|ثاني|ثانيه|ثواني|ث)\b|9:16|16:9|1:1"),
    ("rebuildable", "P01", r"script|سكربت|سكريبت|rebuild|re-run|اعاده بناء"),
    ("staged", "P03", r"first|stage|plan|before you|اولا|مرحله|مراحل|خطه|قبل ما"),
    ("free_assets", "P05", r"free|poly haven|ambientcg|مجاني|بدون دفع"),
    ("named_inputs", "P08", r"@\[|@\w|\.(?:csv|svg|png|jpe?g|pdf)\b|ملف"),
    ("variants", "P10", r"variation|versions?|options|pick|خيارات|نسخ|اختار"),
)


def lint(text: str, data: dict) -> dict:
    norm = normalize(text)
    present, missing = [], []
    hints = {p["id"]: p["ar"] for p in data["principles"]}
    for name, pid, pattern in _CHECKS:
        (present if re.search(pattern, norm) else missing).append({"check": name, "principle": pid})
    for m in missing:
        m["suggestion_ar"] = hints[m["principle"]]
    big_words = r"unreal|game|level|world|walkable|لعبه|عالم|قلعه|مستثمر"
    if re.search(big_words, norm) and not any(p["check"] == "staged" for p in present):
        missing.sort(key=lambda m: m["check"] != "staged")
    return {"status": "LEXICAL_PROMPT_LINT_NOT_A_QUALITY_SCORE",
            "coverage": f"{len(present)}/{len(_CHECKS)}", "present": present, "missing": missing,
            "suggested_recipes": match(text, data)}


def _fills(pairs: list[str]) -> dict[str, str]:
    out = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise ValueError(f"--fill expects key=value, got {pair!r}")
        k, v = pair.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Black Dragon 3D Build Studio (planning only)")
    ap.add_argument("--data", type=Path, default=DATA)
    sub = ap.add_subparsers(dest="action", required=True)
    sub.add_parser("list")
    sub.add_parser("principles")
    sub.add_parser("kit", help="Setup contract, live mode and troubleshooting moves")
    m = sub.add_parser("match")
    m.add_argument("task")
    m.add_argument("--limit", type=int, default=3)
    b = sub.add_parser("brief")
    b.add_argument("ref", help="recipe id or free task text")
    b.add_argument("--fill", action="append", default=[], metavar="KEY=VALUE")
    b.add_argument("--format", choices=("json", "md"), default="json")
    b.add_argument("--out", type=Path)
    lt = sub.add_parser("lint")
    g = lt.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file", type=Path)
    args = ap.parse_args(argv)
    try:
        data = load(args.data)
        if args.action == "list":
            result = [{k: r[k] for k in ("id", "order", "title_ar", "category", "engines", "level", "time")}
                      for r in sorted(data["recipes"], key=lambda r: r["order"])]
        elif args.action == "principles":
            result = data["principles"]
        elif args.action == "kit":
            result = data["operator_kit"]
        elif args.action == "match":
            result = match(args.task, data, args.limit)
        elif args.action == "brief":
            result = brief(args.ref, data, _fills(args.fill))
            if args.format == "md":
                text = to_markdown(result)
                if args.out:
                    args.out.parent.mkdir(parents=True, exist_ok=True)
                    args.out.write_text(text, encoding="utf-8")
                print(text)
                return 0
            if args.out:
                args.out.parent.mkdir(parents=True, exist_ok=True)
                args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            text = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
            result = lint(text, data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("build-studio: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
