#!/usr/bin/env python3
"""Fold a page-by-page reading of a full book into the Dragon Mind's data.

The book itself is never committed. What is committed is the reading: one gist per
page, every page-cited insight the readers extracted, the thinking operators built
from them, and the SHA-256 of the PDF that was read.

Inputs (raw files stay outside the repo):
  --pdf        the book PDF (only hashed and its page count read)
  --reads      JSON {"chunks": [[first, last], ...], "results": [reader output, ...]}
               reader output = {pages, section, page_summaries[{page, gist}], insights[...]}
  --groups     JSON {"groups": {operator_id: [insight, ...]}, "unassigned": [insight, ...]}
  --operators  JSON list of operator entries (frameworks.json shape + trap, pages, summary, debias)
  --merge      operator_id=existing_framework_id (repeatable): enrich an existing framework
               with page references instead of adding a duplicate

Outputs into data/: book_<slug>.json, frameworks.json (operators added or merged),
research_receipt.json ("full_text_books" entry).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
BOOK_SCHEMA = "kosif.dragon-mind.book-read.v1"
OP_FIELDS = ("id", "name_en", "name_ar", "family", "stage", "source_books", "triggers_en", "triggers_ar",
             "questions_en", "questions_ar", "output", "check", "anti_pattern", "cost", "book_evidence",
             "trap", "summary_en", "summary_ar", "debias_en", "debias_ar", "page_refs", "book_examples", "full_text_read")


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _pdf_pages(path: Path) -> int:
    out = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True).stdout
    return int(next(line.split()[-1] for line in out.splitlines() if line.startswith("Pages:")))


def build(a) -> None:
    reads = json.loads(a.reads.read_text(encoding="utf-8"))
    groups = json.loads(a.groups.read_text(encoding="utf-8"))
    ops = json.loads(a.operators.read_text(encoding="utf-8"))
    merge = dict(m.split("=", 1) for m in a.merge)
    total = _pdf_pages(a.pdf)
    results = [r for r in reads["results"] if r]

    gists = {}
    for r in results:
        for s in r["page_summaries"]:
            if 1 <= s["page"] <= total:
                gists.setdefault(s["page"], {"page": s["page"], "section": r["section"], "gist": s["gist"]})
    missing = sorted(set(range(1, total + 1)) - set(gists))
    if missing:
        raise SystemExit("pages without a reader gist: %s" % missing[:20])

    insights = []
    for oid, items in sorted(groups["groups"].items()):
        for it in items:
            insights.append({"concept": it["concept"], "kind": it["kind"],
                             "pages": sorted(p for p in set(it["pages"]) if 1 <= p <= total),
                             "claim": it["claim"], "evidence": it.get("evidence", ""),
                             "operator": merge.get(oid, oid)})
    for it in groups.get("unassigned", []):
        insights.append({"concept": it["concept"], "kind": it["kind"],
                         "pages": sorted(p for p in set(it["pages"]) if 1 <= p <= total),
                         "claim": it["claim"], "evidence": it.get("evidence", ""), "operator": None})
    insights.sort(key=lambda i: (i["pages"][0] if i["pages"] else 0, i["concept"].lower()))

    lib = json.loads((DATA / "frameworks.json").read_text(encoding="utf-8"))
    src = {"title": a.title, "author": a.author, "year": a.year}
    evidence = next((f["book_evidence"] for f in lib["frameworks"]
                     if any(b.get("title") == a.title for b in f.get("source_books", [])) and f.get("book_evidence")), [])
    own_ids = {merge.get(o["id"], o["id"]) for o in ops}
    lib["frameworks"] = [f for f in lib["frameworks"]
                         if not (f.get("full_text_read") == a.slug and f["id"] not in merge.values())]
    by_id = {f["id"]: f for f in lib["frameworks"]}
    added, merged = 0, 0
    for o in ops:
        pages = sorted(p for p in set(o["pages"]) if 1 <= p <= total)
        extra = {"trap": bool(o["trap"]), "summary_en": o["summary_en"], "summary_ar": o["summary_ar"],
                 "debias_en": o["debias_en"], "debias_ar": o["debias_ar"], "page_refs": pages,
                 "book_examples": o["book_examples"][:3]}
        if o["id"] in merge:
            fw = by_id[merge[o["id"]]]
            fw.update(extra)
            fw["full_text_read"] = a.slug
            if not any(b.get("title") == a.title for b in fw["source_books"]):
                fw["source_books"].append(src)
            merged += 1
            continue
        fw = {k: o[k] for k in ("id", "name_en", "name_ar", "family", "stage", "triggers_en", "triggers_ar",
                                "questions_en", "questions_ar", "output", "check", "anti_pattern", "cost")}
        fw["triggers_en"] = sorted({t.strip().lower() for t in fw["triggers_en"] if t.strip()})
        fw["triggers_ar"] = sorted({t.strip() for t in fw["triggers_ar"] if t.strip()})
        fw.update({"source_books": [src], "book_evidence": evidence, **extra, "full_text_read": a.slug})
        lib["frameworks"].append({k: fw[k] for k in OP_FIELDS if k in fw})
        added += 1
    ids = [f["id"] for f in lib["frameworks"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate framework ids")
    lib["full_text_books"] = sorted(set(lib.get("full_text_books", [])) | {a.slug})
    (DATA / "frameworks.json").write_text(json.dumps(lib, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    book = {"schema": BOOK_SCHEMA, "slug": a.slug, "title": a.title, "author": a.author, "year": a.year,
            "pdf_sha256": _sha(a.pdf), "pages_total": total, "pages_read": len(gists),
            "readers": len(results), "chunks": reads["chunks"],
            "operators": sorted(own_ids), "operators_added": added, "operators_merged": merged,
            "insights_total": len(insights),
            "insights_linked": sum(1 for i in insights if i["operator"]),
            "honesty": "every page was read by one of the readers; gists and claims are paraphrases, "
                       "not quotations; page numbers are PDF pages; the PDF itself is not in the repo",
            "pages": [gists[p] for p in sorted(gists)], "insights": insights}
    out = DATA / ("book_%s.json" % a.slug)
    out.write_text(json.dumps(book, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    rec_path = DATA / "research_receipt.json"
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    rec["frameworks"] = {"count": len(lib["frameworks"]),
                         "with_book_evidence": sum(1 for f in lib["frameworks"] if f.get("book_evidence")),
                         "with_page_refs": sum(1 for f in lib["frameworks"] if f.get("page_refs"))}
    books = {b["slug"]: b for b in rec.get("full_text_books", [])}
    books[a.slug] = {"slug": a.slug, "title": a.title, "pdf_sha256": book["pdf_sha256"],
                     "pages_total": total, "pages_read": len(gists), "readers": len(results),
                     "insights": len(insights), "operators_added": added, "operators_merged": merged,
                     "file": out.name, "file_sha256": _sha(out)}
    rec["full_text_books"] = [books[k] for k in sorted(books)]
    rec_path.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("%s: %d/%d pages, %d insights, %d operators added, %d merged" % (
        out.name, len(gists), total, len(insights), added, merged))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, required=True)
    ap.add_argument("--reads", type=Path, required=True)
    ap.add_argument("--groups", type=Path, required=True)
    ap.add_argument("--operators", type=Path, required=True)
    ap.add_argument("--merge", action="append", default=[])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", required=True)
    ap.add_argument("--year", type=int, required=True)
    build(ap.parse_args(argv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
