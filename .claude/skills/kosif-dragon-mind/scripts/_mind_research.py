#!/usr/bin/env python3
"""Build the Dragon Mind's research data from raw, measured sources.

Inputs (raw files stay outside the repo; only aggregates and SHA-256 are committed):
  --gh       JSONL of GitHub repository metadata (one search API item per line)
  --readmes  folder of fetched README files named <owner>__<repo>.md (optional)
  --books    folder with goodbooks-10k books.csv, tags.csv, book_tags.csv
  --frameworks  the curated frameworks JSON to annotate with book evidence

Outputs into data/: github_patterns.json, books_thinking.json, frameworks.json
(annotated) and research_receipt.json. Counting is exact and deterministic; the
pattern detector is lexical (regex over description, topics and README text), so
a count means "the repo's own text names this pattern", not "we audited its code".
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# id, name, regex, what the mind does with it, implemented in dragon_mind.py?
PATTERNS = [
    ("planner-executor", "Planner → executor split",
     r"\bplanner\b|plan[- ]and[- ]execute|plan-then-execute|task decomposition|decompos(e|es|ition) (tasks|the task)",
     "think(): cycle stages plan faculties, Black Dragon run executes", True),
    ("reflection-critic", "Reflection / self-critique loop",
     r"\breflect(ion|ive)?\b|self[- ]critique|self[- ]refine|\bcritic\b|self[- ]correct|reviewer agent",
     "think(): critic pass lists gaps, handoff and consent issues", True),
    ("multi-agent-roles", "Role-based multi-agent crews",
     r"multi[- ]agent|\bcrew\b|role[- ]play|agent roles|agent team|swarm",
     "five-voice council in llm_council.py; mind lists faculties as roles", True),
    ("tool-registry", "Tool registry / function calling",
     r"function[- ]calling|tool[- ]use|tool registry|\btools?\b.*\bschema|tool calling",
     "Black Dragon inventory + tiers = tool registry with readiness", True),
    ("mcp", "Model Context Protocol servers",
     r"\bmcp\b|model context protocol",
     "external executors (Higgsfield, Suno) listed as consent-gated MCP routes", True),
    ("memory", "Long-term / vector memory",
     r"long[- ]term memory|\bmemory\b|vector (store|db|database)|embedding",
     "FusionForge project recipes (lexical, not vector)", False),
    ("rag-retrieval", "Retrieval-augmented generation",
     r"\brag\b|retrieval[- ]augmented|retriev(al|er)",
     "frameworks/patterns retrieved by trigger words (lexical)", True),
    ("dag-workflow", "Graph / DAG workflows",
     r"\bdag\b|directed acyclic|state graph|\bgraph\b.*workflow|workflow graph|langgraph|node[s]? and edges",
     "think(): typed handoff graph nodes → edges; Black Dragon Kahn waves", True),
    ("human-in-the-loop", "Human approval gates",
     r"human[- ]in[- ]the[- ]loop|\bhitl\b|human approval|approval (step|gate)|ask (the )?user",
     "consent flag: spend/publish steps wait for the owner's yes", True),
    ("sandbox", "Sandboxed execution",
     r"\bsandbox(ed)?\b|isolat(ed|ion)|container(ized)?|docker",
     "probe runs in job/probes/cwd; no shell strings", True),
    ("evaluation", "Evals and benchmarks",
     r"\beval(s|uation)?\b|benchmark|test suite|llm[- ]as[- ]a[- ]judge|metrics",
     "self-test + unit tests + doctor; receipts for executed work", True),
    ("observability", "Tracing / observability",
     r"observab|tracing|\btrace(s)?\b|telemetry|opentelemetry|langfuse|logging",
     "mind_trace.json with a digest per run", True),
    ("guardrails", "Guardrails / safety filters",
     r"guardrail|safety|content filter|prompt injection|jailbreak",
     "safety-rights faculty always on; untrusted data never instructions", True),
    ("parallel-agents", "Parallel / concurrent agents",
     r"parallel|concurren(t|cy)|async(hronous)? agents|fan[- ]out",
     "Black Dragon bounded parallel dispatch; mind marks parallel build stages", True),
    ("typed-schemas", "Typed / structured outputs",
     r"structured output|json schema|pydantic|typed|type[- ]safe|zod",
     "nodes carry typed input/output media kinds; handoff check", True),
    ("checkpoint-resume", "Checkpoint / resume / replay",
     r"checkpoint|resum(e|able)|replay|persist(ent|ence) state|time[- ]travel",
     "trace + digest make a run replayable; not a live checkpointer", False),
    ("skills-plugins", "Skills / plugins packs",
     r"\bskills?\b|plugin(s)?\b|extension(s)?\b|agent skills",
     "the super-skill folds 470+ skills into faculties", True),
    ("cost-budget", "Cost / token budgeting",
     r"\bcost\b|budget|token usage|pricing|cheap(er)?",
     "framework cost field and bounded framework count", True),
    ("routing", "Model / task routing",
     r"\brout(er|ing)\b|dispatch|model selection|mixture of",
     "faculty routing to champion capabilities", True),
    ("self-improving", "Self-improving / learning agents",
     r"self[- ]improv|self[- ]evolv|learn(s|ing)? from (experience|feedback)|skill library",
     "FusionForge lessons; no weight training", False),
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def github(raw: Path, readmes: Path | None) -> dict:
    rows = [json.loads(l) for l in raw.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = list({r["full_name"]: r for r in rows}.values())
    readme_text = {}
    if readmes and readmes.is_dir():
        for p in readmes.glob("*.md"):
            readme_text[p.stem.replace("__", "/", 1)] = p.read_text(encoding="utf-8", errors="replace")[:60000].lower()
    comp = [(pid, name, re.compile(rx, re.I), feat, impl) for pid, name, rx, feat, impl in PATTERNS]
    hits = defaultdict(list)
    for r in rows:
        text = " ".join([r.get("full_name") or "", r.get("description") or "", " ".join(r.get("topics") or []),
                         readme_text.get(r["full_name"], "")]).lower()
        for pid, _, rx, _, _ in comp:
            if rx.search(text):
                hits[pid].append(r)
    n = len(rows)
    patterns = []
    for pid, name, _, feat, impl in comp:
        hs = sorted(hits[pid], key=lambda r: (-(r.get("stargazers_count") or 0), r["full_name"]))
        patterns.append({"id": pid, "name": name, "repos": len(hs), "share": "%.1f%%" % (100.0 * len(hs) / max(n, 1)),
                         "exemplars": [{"full_name": r["full_name"], "stars": r.get("stargazers_count"),
                                        "license": r.get("license")} for r in hs[:5]],
                         "mind_feature": feat, "implemented": impl})
    patterns.sort(key=lambda p: (-p["repos"], p["id"]))
    # Upgrade candidates: for each faculty, the most-starred repos whose own text names it.
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _mind_vocab as V
    cands = {}
    permissive = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0", "Unlicense", "0BSD"}
    for fid in V.FACULTY_IDS:
        kws = [k for k in V.FACULTY[fid]["kw"] if re.match(r"[a-z0-9]", k) and len(k) >= 4]
        rx = re.compile(r"(?<![a-z0-9])(?:%s)" % "|".join(re.escape(k) for k in kws)) if kws else None
        found = []
        for r in rows:
            text = ((r.get("description") or "") + " " + " ".join(r.get("topics") or [])).lower()
            if rx and len(set(rx.findall(text))) >= 2:
                found.append(r)
        found.sort(key=lambda r: (-(r.get("stargazers_count") or 0), r["full_name"]))
        cands[fid] = {"matching_repos": len(found),
                      "top": [{"full_name": r["full_name"], "stars": r.get("stargazers_count"),
                               "license": r.get("license"), "permissive": r.get("license") in permissive,
                               "description": (r.get("description") or "")[:160]} for r in found[:8]]}
    topics = Counter(t for r in rows for t in (r.get("topics") or []))
    langs = Counter(r.get("language") or "none" for r in rows)
    queries = Counter(r.get("query") for r in rows)
    stars = sorted((r.get("stargazers_count") or 0) for r in rows)
    return {"schema": "kosif.dragon-mind.github.v1", "repos_measured": n,
            "readmes_read": sum(1 for r in rows if r["full_name"] in readme_text),
            "stars_median": stars[len(stars) // 2] if stars else 0,
            "queries": dict(sorted(queries.items())),
            "languages_top": dict(langs.most_common(15)), "topics_top": dict(topics.most_common(60)),
            "patterns": patterns, "faculty_candidates": cands,
            "method": "GitHub search API metadata (description, topics, stars, license) for repos with >=5 stars "
                      "under 30 topic queries, plus README text for the most-starred repos; lexical pattern regexes"}


def _norm(t: str) -> str:
    t = re.sub(r"\(.*?\)", "", t.lower())
    t = t.split(":")[0]
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


DOMAINS = {
    "decision": r"decision|thinking|rational|cognitive|bias|critical-thinking|logic|probab|statistic",
    "psychology": r"psycholog|behavio|neuroscien|brain|mind",
    "product": r"product|design|ux|innovation|startup|entrepreneur",
    "business-strategy": r"business|strategy|management|leadership|economics|finance|marketing|sales",
    "creativity": r"creativ|art|writing|craft",
    "habits-productivity": r"productiv|habit|self-help|self-improvement|personal-development|success|time-management",
    "systems-science": r"science|systems|complexity|physics|biology|evolution",
    "philosophy": r"philosoph|stoic|ethics",
    "communication": r"communicat|persuasion|negotiat|influence|psychology-of-persuasion|rhetoric",
}
CORE = re.compile(r"^(business|psychology|self-help|self-improvement|productivity|leadership|management|"
                  r"entrepreneurship|startup|startups|marketing|economics|philosophy|decision-making|thinking|"
                  r"cognitive-science|creativity|innovation|design|strategy|personal-development|habits|negotiation|"
                  r"persuasion|behavioral-economics|neuroscience|business-books|popular-science|social-science)$")


def books(folder: Path) -> dict:
    tags = {r["tag_id"]: r["tag_name"] for r in csv.DictReader((folder / "tags.csv").open(encoding="utf-8"))}
    meta = {r["goodreads_book_id"]: r for r in csv.DictReader((folder / "books.csv").open(encoding="utf-8"))}
    bt = defaultdict(dict)
    for r in csv.DictReader((folder / "book_tags.csv").open(encoding="utf-8")):
        bt[r["goodreads_book_id"]][tags.get(r["tag_id"], "")] = int(r["count"])
    kept = []
    for gid, tg in bt.items():
        core = {t: c for t, c in tg.items() if CORE.match(t) and c >= 30}
        if not core or gid not in meta:
            continue
        m = meta[gid]
        dom = sorted({d for d, rx in DOMAINS.items() for t, c in tg.items() if c >= 20 and re.search(rx, t)})
        kept.append({"id": int(m["book_id"]), "title": m["original_title"] or m["title"], "author": m["authors"],
                     "year": int(float(m["original_publication_year"])) if m["original_publication_year"] else None,
                     "rating": float(m["average_rating"]), "ratings": int(m["ratings_count"]),
                     "domains": dom, "top_tags": [t for t, _ in sorted(core.items(), key=lambda kv: -kv[1])[:4]]})
    kept.sort(key=lambda b: (-b["ratings"], b["id"]))
    dom_counts = Counter(d for b in kept for d in b["domains"])
    return {"schema": "kosif.dragon-mind.books.v1", "dataset": "goodbooks-10k (Goodreads, zygmuntz/goodbooks-10k)",
            "screened": len(meta), "tagged": len(bt), "kept": len(kept), "domains": dict(dom_counts.most_common()),
            "method": "every one of the 10,000 books screened by its user shelf tags; kept when a core thinking/"
                      "product/business/psychology tag has >=30 shelvings. Metadata only: no book text was read.",
            "books": kept,
            "_all": [{"id": int(m["book_id"]), "title": m["original_title"] or m["title"], "alt": m["title"],
                      "authors": m["authors"], "ratings": int(m["ratings_count"])} for m in meta.values()]}


def annotate(frameworks: dict, bk: dict) -> dict:
    index = defaultdict(list)
    allb = {}
    for b in sorted(bk["_all"], key=lambda b: -b["ratings"]):  # all 10,000, not only the kept subset
        for t in {b["title"], b["alt"]}:
            index[_norm(t)].append(b)
            allb.setdefault(_norm(t), b)
    matched = 0
    for fw in frameworks["frameworks"]:
        ev = []
        for sb in fw.get("source_books", []):
            key = _norm(sb.get("title", ""))
            surname = (sb.get("author") or "").split()[-1:] or [""]

            def same_author(b):
                return surname[0] and surname[0].lower() in b["authors"].lower()
            b = next((v for v in index.get(key, []) if same_author(v)), None)
            if b is None and len(key) >= 8:  # subtitle variants: dataset title = source title + more words
                b = next((v for k, v in allb.items() if k.startswith(key + " ") and same_author(v)), None)
            if b:
                ev.append({"book_id": b["id"], "title": b["title"], "ratings": b["ratings"]})
        fw["book_evidence"] = ev
        matched += bool(ev)
    frameworks["book_matched"] = matched
    return frameworks


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gh", type=Path, required=True)
    ap.add_argument("--readmes", type=Path)
    ap.add_argument("--books", type=Path, required=True)
    ap.add_argument("--frameworks", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=DATA)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    gh = github(a.gh, a.readmes)
    bk = books(a.books)
    fw = annotate(json.loads(a.frameworks.read_text(encoding="utf-8")), bk)
    bk.pop("_all")
    for name, obj in (("github_patterns.json", gh), ("books_thinking.json", bk), ("frameworks.json", fw)):
        (a.out / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    receipt = {"schema": "kosif.dragon-mind.research-receipt.v1",
               "github": {"repos_measured": gh["repos_measured"], "readmes_read": gh["readmes_read"],
                          "raw_sha256": sha(a.gh)},
               "books": {"screened": bk["screened"], "kept": bk["kept"],
                         "files_sha256": {f: sha(a.books / f) for f in ("books.csv", "tags.csv", "book_tags.csv")}},
               "frameworks": {"count": len(fw["frameworks"]), "with_book_evidence": fw["book_matched"]},
               "honesty": "counts are measured from the files hashed here; README/book analysis is lexical metadata analysis"}
    (a.out / "research_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
