#!/usr/bin/env python3
"""Import creative briefs into the atlas.

Reads every *.json file in a directory (each `{"briefs": [...]}`), validates the
brief objects against the brief shape documented in catalog/SCHEMA.md ("Brief
objects"), writes styles/<id>/BRIEF.md, catalog/briefs.json and copies the
brief-derived summary fields (name_ar, summary_ar, summary_en, keywords,
difficulty, duration_s, stack, brief) into catalog/styles.json and
styles/<id>/STYLE.json. Every file is parsed before anything is written.

Without --strict, files that are not valid JSON or not shaped {"briefs": [...]},
unknown ids, and briefs with missing keys, wrong types or an unreadable aspect
are skipped; briefs that only fail a value check (difficulty 1-5, known stack
names, 6-20 keywords, 3-8 scenes_en, numeric duration_s, ISO revised_from_video,
title_ar up to 80 chars) are still imported, and every issue is printed.
With --strict, any brief with an issue is skipped, the rest are imported and the
exit code is 1; an unreadable or wrongly shaped file stops the run with exit 1
before anything is written.

Usage:
  python3 tools/import_briefs.py <dir-with-batch-json> [--strict]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "styles.json"
BRIEFS = ROOT / "catalog" / "briefs.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aspects import is_valid as aspect_ok  # noqa: E402  (any W:H such as 2.35:1, WxH or name)
STACKS = {"Remotion", "React", "HTML Canvas", "SVG", "CSS", "GSAP", "Three.js", "WebGL", "Web Audio", "Lottie"}
STR = ("id", "title_ar", "summary_ar", "summary_en", "concept_ar", "concept_en", "aspect", "assumptions_en")
LISTS = ("scenes_en", "scenes_ar", "motion_rules_en", "motion_rules_ar", "stack", "keywords", "facts_from_source")
KEYS = STR + LISTS + ("duration_s", "difficulty")


def problems(b: dict) -> list[str]:
    out = []
    for k in KEYS:
        if k not in b:
            out.append(f"missing {k}")
    for k in STR:
        if k in b and not isinstance(b[k], str):
            out.append(f"{k} not a string")
    for k in LISTS:
        if k in b and (not isinstance(b[k], list) or any(not isinstance(x, str) for x in b[k])):
            out.append(f"{k} not a list of strings")
    if not isinstance(b.get("aspect"), str) or not aspect_ok(b["aspect"]):
        out.append(f"aspect {b.get('aspect')!r} is not a readable ratio (W:H, WxH or a name)")
    d = b.get("difficulty")
    if not isinstance(d, int) or not 1 <= d <= 5:
        out.append("difficulty must be an integer 1-5")
    if b.get("duration_s") is not None and not isinstance(b.get("duration_s"), (int, float)):
        out.append("duration_s must be a number or null")
    if isinstance(b.get("stack"), list) and any(s not in STACKS for s in b["stack"]):
        out.append(f"stack has unknown values: {[s for s in b['stack'] if s not in STACKS]}")
    if isinstance(b.get("keywords"), list) and not 6 <= len(b["keywords"]) <= 20:
        out.append(f"keywords count {len(b['keywords'])} outside 6-20")
    if isinstance(b.get("scenes_en"), list) and not 3 <= len(b["scenes_en"]) <= 8:
        out.append("scenes_en should have 3-8 beats")
    rv = b.get("revised_from_video")
    if rv is not None and not (isinstance(rv, str) and len(rv) == 10 and rv[4] == "-" and rv[7] == "-"):
        out.append("revised_from_video must be an ISO date string (YYYY-MM-DD)")
    if isinstance(b.get("title_ar"), str) and len(b["title_ar"]) > 80:
        out.append("title_ar longer than 80 chars")
    return out


def bullets(items: list[str]) -> str:
    return "\n".join("- " + x.strip() for x in items) or "- —"


def provenance(b: dict) -> str:
    """Provenance note: unwatched draft by default, or revised against sampled video frames."""
    when = b.get("revised_from_video")
    if when:
        return (f"ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع ({when})؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.\n"
                f"Original KOSIF brief, revised against frames sampled from the reference video ({when}); timings and colours are approximate readings from those frames, so check the reference for fine detail.")
    return ("ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.\n"
            "Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.")


def render_md(rec: dict, b: dict) -> str:
    facts = b.get("facts_from_source") or []
    return f"""# {b['title_ar']} — {rec['name']}

> {b['summary_ar']}
>
> {b['summary_en']}

{provenance(b)}

- المرجع / Reference: {rec.get('page')}
- التصنيفات / Categories: {', '.join(rec.get('category') or []) or '—'}
- النسبة المقترحة / Aspect: {b['aspect']} · المدة / Duration: {b.get('duration_s') if b.get('duration_s') is not None else 'حسب المادة / per material'} s · الصعوبة / Difficulty: {b['difficulty']}/5
- التقنية المقترحة / Stack: {', '.join(b.get('stack') or []) or 'choose per material'}

## الفكرة
{b['concept_ar']}

## Concept
{b['concept_en']}

## المشاهد المقترحة
{bullets(b.get('scenes_ar') or [])}

## Proposed scenes
{bullets(b.get('scenes_en') or [])}

## قواعد الحركة
{bullets(b.get('motion_rules_ar') or [])}

## Motion rules
{bullets(b.get('motion_rules_en') or [])}

## Facts stated by the source (rewritten in our words)
{bullets(facts) if facts else '- The public description states nothing specific beyond the title.'}

## Assumptions
{b['assumptions_en']}

## Keywords
{', '.join(b.get('keywords') or [])}
"""


def load_batches(files: list[Path]) -> tuple[list[tuple[Path, list]], list[str]]:
    """Parse every batch file up front, so a bad file is found before anything is written."""
    batches, errors = [], []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except OSError as e:
            errors.append(f"{f.name}: cannot read ({e})")
            continue
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            errors.append(f"{f.name}: invalid JSON ({e})")
            continue
        if not isinstance(data, dict) or not isinstance(data.get("briefs"), list):
            got = 'an object without a "briefs" list' if isinstance(data, dict) else f"a JSON {type(data).__name__}"
            errors.append(f'{f.name}: expected an object {{"briefs": [...]}}, got {got}')
            continue
        batches.append((f, data["briefs"]))
    return batches, errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("directory")
    ap.add_argument("--strict", action="store_true",
                    help="skip every brief with any issue (not only missing keys or wrong types) and exit 1 if any "
                         "brief was skipped or any id is unknown; an unreadable file stops the run before anything is written")
    args = ap.parse_args()
    src = Path(args.directory)
    files = sorted(src.glob("*.json"))
    if not files:
        print("no *.json files in", src, file=sys.stderr)
        return 2
    batches, file_errors = load_batches(files)
    for e in file_errors:
        print(e, file=sys.stderr)
    if args.strict and file_errors:
        print("--strict: nothing was written", file=sys.stderr)
        return 1
    records = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in records}
    existing = json.loads(BRIEFS.read_text(encoding="utf-8")) if BRIEFS.exists() else {}
    imported, skipped, unknown = 0, [], []
    for f, briefs in batches:
        for n, b in enumerate(briefs, 1):
            if not isinstance(b, dict):
                skipped.append((f"{f.name} item {n}", ["not a JSON object"], True))
                continue
            ident = b.get("id")
            if not isinstance(ident, str) or ident not in by_id:
                unknown.append(ident)
                continue
            errs = problems(b)
            fatal = bool(errs) and (args.strict or any(e.startswith("missing") or "not a" in e for e in errs))
            if errs:
                skipped.append((ident, errs, fatal))
            if fatal:
                continue
            rec = by_id[ident]
            existing[ident] = b
            d = ROOT / "styles" / ident
            d.mkdir(parents=True, exist_ok=True)
            (d / "BRIEF.md").write_text(render_md(rec, b), encoding="utf-8")
            rec.update({
                "name_ar": b["title_ar"],
                "summary_ar": b["summary_ar"],
                "summary_en": b["summary_en"],
                "keywords": b["keywords"],
                "difficulty": b["difficulty"],
                "duration_s": b.get("duration_s"),
                "stack": b.get("stack") or [],
                "brief": f"styles/{ident}/BRIEF.md",
            })
            (d / "STYLE.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            imported += 1
    CATALOG.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "catalog" / "prompts_motion.json").write_text(
        json.dumps([r for r in records if r["origin"] == "PromptsMotion"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BRIEFS.write_text(json.dumps(dict(sorted(existing.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"imported {imported} briefs; {len(existing)} total in catalog/briefs.json")
    if unknown:
        print("unknown ids:", unknown, file=sys.stderr)
    for ident, errs, fatal in skipped:
        print(f"issues in {ident} ({'skipped' if fatal else 'imported anyway'}): {'; '.join(errs)}", file=sys.stderr)
    if args.strict and (skipped or unknown):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
