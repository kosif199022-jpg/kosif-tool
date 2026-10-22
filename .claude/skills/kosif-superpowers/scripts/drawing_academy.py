#!/usr/bin/env python3
"""KOSIF Drawing Academy: source-aware exercise/compiler, not model finetuning.

Pure stdlib; no network, no external credits, no book/illustration redistribution.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "drawing_academy_curriculum.json"
KEYWORDS = {
    "observation": ["observation", "outline", "proportion", "nature", "sketch"],
    "construction": ["construction", "circle", "shape", "drawing", "lines"],
    "gesture_and_values": ["gesture", "line", "mass", "light", "shade"],
    "perspective": ["vanishing", "horizon", "perspective", "distance", "plane"],
    "anatomy": ["bone", "joint", "muscle", "skeleton", "movement"],
    "linework": ["outline", "line", "form", "design", "movement"],
    "composition": ["composition", "line", "notan", "color", "balance"],
    "color": ["hue", "value", "chroma", "color", "sphere"],
}

def curriculum(path=DEFAULT):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != "kosif.drawing.academy.v1":
        raise ValueError("unsupported curriculum schema")
    sources = {s["id"]: s for s in data["sources"]}
    ids = set()
    for lesson in data["lessons"]:
        if lesson["id"] in ids or lesson["source_id"] not in sources:
            raise ValueError("duplicate lesson or unknown source")
        ids.add(lesson["id"])
        if sum(m["weight"] for m in lesson["metrics"]) != 100:
            raise ValueError("rubric weights must equal 100")
        if len({m["id"] for m in lesson["metrics"]}) != len(lesson["metrics"]):
            raise ValueError("duplicate rubric metric")
    return data

def select(data, lesson_id):
    return next((v for v in data["lessons"] if v["id"] == lesson_id), None)

def write_result(data, output):
    blob = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if output:
        p = Path(output)
        if p.exists():
            raise ValueError("refusing to overwrite existing output")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(blob, encoding="utf-8")
    else:
        print(blob, end="")

def package(data, lesson):
    source = next(s for s in data["sources"] if s["id"] == lesson["source_id"])
    return {
        "schema": "kosif.drawing.lesson.v1",
        "status": "ORIGINAL_EXERCISE_UNEXECUTED",
        "lesson_id": lesson["id"],
        "title_ar": lesson["title_ar"],
        "book": {"title": source["title"], "author": source["author"],
                 "url": source["source_url"], "review_status": source["review_status"],
                 "anchor": lesson["source_anchor"]},
        "concept_ar": lesson["concept_ar"],
        "draw_order": lesson["steps"],
        "original_exercise_ar": lesson["exercise_ar"],
        "engine_candidate": lesson["engine"],
        "rubric": lesson["metrics"],
        "delivery": ["editable_artifact", "staged_preview", "evidence_path",
                     "manual_or_external_visual_review"],
        "warnings": ["No original book images reproduced.",
                     "Practice plan does not prove that a drawing was rendered."]
    }

def scan_book(data, book_id, path, rights):
    source = next((s for s in data["sources"] if s["id"] == book_id), None)
    if source is None:
        raise ValueError("unknown book id")
    p = Path(path)
    if not p.is_file() or p.suffix.lower() not in (".txt", ".md"):
        raise ValueError("supply a real local .txt or .md copy, with appropriate rights")
    raw = p.read_bytes()
    if len(raw) > 20_000_000:
        raise ValueError("book file exceeds 20MB safe limit")
    body = raw.decode("utf-8-sig")
    words = KEYWORDS[source["domain"]]
    hits = []
    for line_no, line in enumerate(body.splitlines(), 1):
        found = sorted({w for w in words if re.search(r"\b" + re.escape(w) + r"\b", line, re.I)})
        if found:
            hits.append({"line": line_no, "concepts": found})
    # Metadata only: zero source prose and zero copyrighted illustrations copied into the result.
    return {
        "schema": "kosif.drawing.source_audit.v1",
        "book_id": book_id, "source_url": source["source_url"],
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "rights_basis_user_supplied": rights,
        "text_lines_examined": len(body.splitlines()),
        "keyword_hit_lines": len(hits),
        "source_positions": hits[:25],
        "status": "SOURCE_TEXT_SCANNED_CANDIDATES_ONLY",
        "manual_followup": "Read source at recorded line anchors; check diagrams, derive original method cards; verify rights, render, and score independently.",
    }

def assessment(data, lesson_id, score_file, evidence):
    lesson = select(data, lesson_id)
    if lesson is None:
        raise ValueError("unknown lesson id")
    p = Path(evidence)
    if not p.is_file():
        return {"status": "NEEDS_ARTIFACT_EVIDENCE", "lesson_id": lesson_id}
    scores = json.loads(Path(score_file).read_text(encoding="utf-8"))
    metrics = lesson["metrics"]
    names = {m["id"] for m in metrics}
    if set(scores) != names:
        raise ValueError("every rubric metric must have a scored value, no extras")
    for v in scores.values():
        if type(v) not in (int, float) or not 0 <= v <= 5:
            raise ValueError("numeric rubric scores must be between 0 and 5")
    return {
        "status": "REVIEW_SCORES_RECORDED_NOT_AUTOMATED_VISUAL_PROOF",
        "lesson_id": lesson_id, "score_out_of_100": round(
            sum(m["weight"] * scores[m["id"]] / 5 for m in metrics), 2),
        "evidence_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "evidence_filename": p.name,
        "scores": scores,
        "warning": "The scorer supplies values. This CLI does not see image quality or certify professional skill."
    }

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalog", type=Path, default=DEFAULT)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("index")
    ls = sub.add_parser("lesson")
    ls.add_argument("--id", required=True)
    ls.add_argument("--out")
    sc = sub.add_parser("scan-book")
    sc.add_argument("--book-id", required=True)
    sc.add_argument("--input", required=True)
    sc.add_argument("--rights", choices=["public_domain_checked", "licensed", "own_copy_private"], required=True)
    sc.add_argument("--out")
    ev = sub.add_parser("assess")
    ev.add_argument("--id", required=True)
    ev.add_argument("--scores", required=True)
    ev.add_argument("--evidence", required=True)
    ev.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        data = curriculum(args.catalog)
        if args.cmd == "index":
            write_result({"schema":data["schema"],"sources":[{"id":x["id"],"title":x["title"],"review_status":x["review_status"],"ingested_full_text":x["ingested_full_text"]} for x in data["sources"]],
                          "lessons":[{"id":x["id"],"level":x["level"],"title_ar":x["title_ar"]} for x in data["lessons"]]},None)
        elif args.cmd == "lesson":
            item = select(data,args.id)
            if item is None:
                raise ValueError("unknown lesson id")
            write_result(package(data,item),args.out)
        elif args.cmd == "scan-book":
            write_result(scan_book(data,args.book_id,args.input,args.rights),args.out)
        else:
            write_result(assessment(data,args.id,args.scores,args.evidence),args.out)
        return 0
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print("DRAWING_ACADEMY_ERROR: "+str(exc),file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
