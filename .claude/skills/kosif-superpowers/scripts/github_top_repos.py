#!/usr/bin/env python3
"""GitHub top-1000 review tracker / متابعة مراجعة أشهر 1000 مستودع على GitHub.

Reads the facts snapshot data/github_top1000_snapshot.json (rank, repo, stars, language, licence, description of the
1,000 most-starred public repositories) and the hand review data/github_top1000_review.json (per-repo topic or
decision overrides and what was transferred into the skill), classifies every repository by topic and licence, and
writes the tracker data/github_top1000.json plus the readable table references/github-top-1000.md.

    python3 scripts/github_top_repos.py build            # write the tracker and the table (--check: report drift only)
    python3 scripts/github_top_repos.py stats            # counts by topic, licence class and decision
    python3 scripts/github_top_repos.py find <words>     # repos whose name, description or topic match
    python3 scripts/github_top_repos.py show <owner/repo>
    python3 scripts/github_top_repos.py refresh --out <file.json>   # network: fetch a new snapshot (never overwrites the committed one)

The snapshot merges two public sources: the gitstar-ranking.com index of the most-starred repositories (which misses
some large ones) and deps.dev records for the snapshot's "supplement" list; stars and licence ids come from deps.dev.
    python3 scripts/github_top_repos.py --self-test

Decisions: mine = relevant and permissively licensed (methods may be restated and code patterns reused with credit);
reference = relevant but copyleft, unrecognised or missing licence (link and own-words method only, no code copied);
skip = general software with nothing to transfer, or excluded for safety or ethics (the reason says which);
transferred = mined, with the power or tool ids that now carry its methods. Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
SNAPSHOT = SK / "data" / "github_top1000_snapshot.json"
REVIEW = SK / "data" / "github_top1000_review.json"
TRACKER = SK / "data" / "github_top1000.json"
TABLE = SK / "references" / "github-top-1000.md"
POWERS = SK / "data" / "powers"
REPOS_JSON = SK / "repos.json"
GH_RE = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")


def catalog_citations(powers_dir: Path = POWERS, repos_json: Path = REPOS_JSON) -> tuple:
    """({repo_lower: sorted power ids whose source or proof names github.com/<repo>}, {repo_lower} credited in repos.json)."""
    cited = {}
    for f in sorted(powers_dir.glob("*.json")) if powers_dir.is_dir() else []:
        for rec in json.loads(f.read_text(encoding="utf-8")):
            text = f"{rec.get('source', '')} {json.dumps(rec.get('proof', []))}"
            for m in GH_RE.finditer(text):
                key = m.group(1).lower().rstrip(".")
                key = key[:-4] if key.endswith(".git") else key
                cited.setdefault(key, set()).add(rec["id"])
    credited = set()
    if repos_json.is_file():
        credited = {r.get("owner_repo", "").lower() for r in json.loads(repos_json.read_text(encoding="utf-8")).get("repos", [])}
    return {k: sorted(v) for k, v in cited.items()}, credited

# Topic rules, first match wins. Each topic: (id, Arabic label, relevant?, regex over "owner/repo description").
TOPICS = [
    ("prompt-engineering", "هندسة البرومبت", True,
     r"\bprompt|context engineering|\bjailbreak"),
    ("agents-skills", "الوكلاء والمهارات", True,
     r"\bagents?\b|agentic|\bskills?\b|claude|\bcodex\b|copilot|\bmcp\b|harness|autonomous|swarm|\bcursor\b|vibe cod|spec-driven|\bsdd\b|coding assistant|\bn8n\b|workflow automation"),
    ("llm-reasoning-memory", "النماذج اللغوية والاستدلال والذاكرة", True,
     r"\bllms?\b|\bgpt|chatgpt|language model|\brag\b|retrieval|memory|reasoning|knowledge graph|chatbot|ollama|llama|inference|fine-?tun|transformers|deepseek|qwen|gemini|openai|anthropic|\bai\b.*(assistant|chat)|embedding|vector"),
    ("generative-media", "التوليد بالذكاء للصور والصوت والفيديو", True,
     r"stable diffusion|diffusion|text-to-image|image generat|comfyui|voice clon|text-to-speech|\btts\b|video generat|deepfake|face ?swap|generative"),
    ("motion-animation", "الموشن والأنيميشن", True,
     r"animat|\bmotion\b|manim|lottie|gsap|transition|tween|keyframe"),
    ("graphics-3d-games", "الرسوميات و3D والألعاب", True,
     r"\b3d\b|webgl|webgpu|three\.?js|\bgame|shader|render|\bcanvas\b|blender|godot|unity|unreal|opengl|vulkan|ray ?trac|physics engine"),
    ("media-audio-video", "الصوت والفيديو", True,
     r"\bvideo|\baudio|ffmpeg|speech|whisper|\bmusic|media player|streaming|youtube|subtitle|screen record|\bobs\b|podcast|\bimage (processing|editor)|photo"),
    ("design-ui-type", "التصميم والواجهات والخطوط", True,
     r"\bdesign|\bui\b|\bux\b|\bcss|icon|\bfonts?\b|typeface|typograph|component|tailwind|figma|presentation|slides|theme"),
    ("data-viz-diagrams", "الرسوم البيانية والمخططات", True,
     r"\bchart|visuali[sz]|\bd3\b|dashboard|diagram|mermaid|excalidraw|whiteboard|drawio|draw\.io|\bplot|\bgraphs?\b"),
    ("ai-ml-vision", "تعلم الآلة والرؤية", True,
     r"machine learning|deep learning|neural|pytorch|tensorflow|keras|\byolo|segment|\bocr\b|face recog|computer vision|\bml\b|\bai\b|artificial intelligence|data science|jupyter|notebook"),
    ("docs-writing-knowledge", "المستندات والكتابة والمعرفة", True,
     r"markdown|\bdocuments?\b|\bnotes?\b|note-taking|writing|\bwiki|\bpdf\b|translat|knowledge|\bbooks?\b|ebook|documentation|static site|\bblog"),
    ("research-web", "البحث والويب والأتمتة", True,
     r"scrap|crawl|search engine|browser automation|playwright|puppeteer|selenium|headless"),
    ("methods-curricula", "المناهج والطرق وقوائم التحقق", True,
     r"roadmap|interview|system design|algorithm|best practice|style guide|clean code|checklist|design patterns?|\bcourses?\b|tutorial|lessons|\blearn|\bguide|cheat ?sheet|study plan|curriculum|awesome|curated|patterns of|self-taught|education|\bpapers\b|exercises|challenge"),
    ("security", "الأمن", False,
     r"hack|pentest|payload|exploit|\bctf\b|security|malware|reverse engineer|password|vpn|proxy|shadowsocks|v2ray|clash|bypass|censorship"),
]
TOPIC_AR = {t[0]: t[1] for t in TOPICS}
TOPIC_AR["engineering-general"] = "هندسة برمجيات عامة"
RELEVANT = {t[0] for t in TOPICS if t[2]}
COMPILED = [(t[0], re.compile(t[3], re.I)) for t in TOPICS]

PERMISSIVE = {"MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "ISC", "0BSD", "Unlicense", "CC0-1.0", "Zlib",
              "MPL-2.0", "CC-BY-4.0", "BSL-1.0", "WTFPL", "Python-2.0"}
COPYLEFT_RE = re.compile(r"^(A?GPL|LGPL|EUPL|OSL|CC-BY-SA|CC-BY-NC)", re.I)
DECISIONS = ("transferred", "mine", "reference", "skip")
DECISION_AR = {"transferred": "نُقلت قدراته", "mine": "قابل للتعدين", "reference": "مرجع فقط", "skip": "لا يُنقل"}


def licence_class(lic: str) -> str:
    if lic in PERMISSIVE:
        return "permissive"
    if COPYLEFT_RE.match(lic or ""):
        return "copyleft"
    if lic == "non-standard":
        return "unrecognised"
    return lic if lic in ("none", "unknown") else "other"


def topic_of(row: dict) -> str:
    text = f"{row['repo']} {row.get('description', '')}"
    for tid, rx in COMPILED:
        if rx.search(text):
            return tid
    return "engineering-general"


def classify(row: dict, review: dict, cited: dict = None, credited: set = None) -> dict:
    rv = review.get(row["repo"], {})
    cited_by = (cited or {}).get(row["repo"].lower(), [])
    topic = rv.get("topic") or topic_of(row)
    lc = licence_class(row["license"])
    transferred = list(dict.fromkeys(list(rv.get("transferred", [])) + list(cited_by)))
    if rv.get("decision"):
        decision, why = rv["decision"], rv.get("why", "")
    elif topic not in RELEVANT:
        decision = "skip"
        why = "safety: offensive-security or circumvention material is linked, never imported" if topic == "security" else \
            "general software: no method or tool the skill can take over"
    elif lc == "permissive":
        decision, why = "mine", f"relevant ({topic}) and {row['license']}: methods and code patterns may be reused with credit"
    elif lc == "copyleft":
        decision, why = "reference", f"{row['license']} is copyleft: link and own-words method only, no code copied"
    else:
        decision, why = "reference", f"licence {row['license']}: link and own-words method only until the licence is read"
    if transferred and (decision in ("mine", "reference") or (decision == "skip" and not rv.get("decision"))):
        if decision == "skip":
            why = "the catalog already cites it, so it counts as relevant"
        decision = "transferred"
    if rv.get("why") and not rv.get("decision"):
        why = rv["why"]
    return {"rank": row["rank"], "repo": row["repo"], "stars": row["stars"], "language": row.get("language", ""),
            "license": row["license"], "license_class": lc, "topic": topic, "relevant": topic in RELEVANT or decision == "transferred",
            "decision": decision, "why": why, "transferred": transferred,
            "credited_in_repos_json": row["repo"].lower() in (credited or set()),
            "url": f"https://github.com/{row['repo']}", "description": row.get("description", "")}


def load_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def build_tracker(snapshot: dict, review: dict, citations: tuple = None) -> dict:
    cited, credited = citations if citations is not None else catalog_citations()
    rows = [classify(r, review.get("repos", {}), cited, credited) for r in sorted(snapshot["rows"], key=lambda r: r["rank"])]
    known = {r["repo"].lower() for r in rows}
    extra = [classify(dict(e, rank=None, repo=repo), {repo: e}, cited, credited) for repo, e in sorted(review.get("extra", {}).items())
             if repo.lower() not in known]
    return {"schema": "kosif.github-top1000.v1", "fetched": snapshot.get("fetched", ""),
            "sources": snapshot.get("sources", {}), "limits": snapshot.get("limits", ""),
            "generated_by": "scripts/github_top_repos.py build",
            "counts": counts(rows), "rows": rows, "extra": extra}


def counts(rows: list) -> dict:
    def tally(key):
        out = {}
        for r in rows:
            out[r[key]] = out.get(r[key], 0) + 1
        return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))
    return {"total": len(rows), "relevant": sum(r["relevant"] for r in rows), "decision": tally("decision"),
            "topic": tally("topic"), "license_class": tally("license_class"),
            "transferred_ids": sum(len(r["transferred"]) for r in rows)}


def short_ids(ids: list, cap: int = 6) -> str:
    return ", ".join(ids[:cap]) + (f" … (+{len(ids) - cap})" if len(ids) > cap else "")


def md_cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def render_table(tracker: dict) -> str:
    c = tracker["counts"]
    L = ["# أشهر 1000 مستودع على GitHub — GitHub top-1000 review", "",
         "Generated by `scripts/github_top_repos.py build` from `data/github_top1000_snapshot.json` and "
         "`data/github_top1000_review.json`; do not edit by hand.", "",
         f"لقطة {tracker['fetched']}: {c['total']} مستودع، منها {c['relevant']} ذات صلة بقدرات المهارة. "
         f"Snapshot {tracker['fetched']}: {c['total']} repositories reviewed, {c['relevant']} relevant to the skill.", "",
         "**القرار / decision:** " + " · ".join(f"{DECISION_AR.get(k, k)} `{k}` {v}" for k, v in c["decision"].items()), "",
         "**الترخيص / licence class:** " + " · ".join(f"`{k}` {v}" for k, v in c["license_class"].items()), "",
         "- `transferred`: methods restated in our own words as power or tool records (ids in the last column), recorded by hand "
         "or found automatically: every power whose `source` or `proof` names the repository's GitHub URL is listed.",
         "- `·repos.json`: also credited as a link in the motion repository catalogue `repos.json`.",
         "- `mine`: relevant and permissive; eligible for the next mining batch.",
         "- `reference`: relevant, but copyleft or the licence is unrecognised/missing: link and own-words method only.",
         "- `skip`: general software, or excluded for safety (the reason is in `data/github_top1000.json`).", "",
         "Sources: " + "; ".join(f"{k}: {v}" for k, v in tracker["sources"].items()), "",
         f"Limits: {tracker.get('limits', '')}", "",
         "## الفهرس / contents", "", "1. [حسب الموضوع / by topic](#حسب-الموضوع--by-topic)",
         "2. [من خارج الألف / mined from outside the top 1,000](#من-خارج-الألف--mined-from-outside-the-top-1000)",
         "3. [الجدول الكامل / full table](#الجدول-الكامل--full-table)", "",
         "## حسب الموضوع / by topic", "",
         "| topic | الموضوع | repos | transferred | mine | reference | skip |", "|---|---|---:|---:|---:|---:|---:|"]
    for t, n in c["topic"].items():
        sub = [r for r in tracker["rows"] if r["topic"] == t]
        k = {d: sum(r["decision"] == d for r in sub) for d in DECISIONS}
        L.append(f"| `{t}` | {TOPIC_AR.get(t, t)} | {n} | {k['transferred']} | {k['mine']} | {k['reference']} | {k['skip']} |")
    if tracker.get("extra"):
        L += ["", "## من خارج الألف / mined from outside the top 1,000", "",
              "Repositories below the star cut-off that the skill still draws on (named by the user or the best in their niche).", "",
              "| repo | ★ | licence | topic | decision | transferred to |", "|---|---:|---|---|---|---|"]
        for r in tracker["extra"]:
            L.append(f"| [{md_cell(r['repo'])}]({r['url']}) | {r['stars']:,} | {r['license']} | {r['topic']} | {r['decision']} | "
                     f"{short_ids(r['transferred'])} |")
    L += ["", "## الجدول الكامل / full table", "",
          "| # | repo | ★ | licence | topic | decision | transferred to |", "|---:|---|---:|---|---|---|---|"]
    for r in tracker["rows"]:
        L.append(f"| {r['rank']} | [{md_cell(r['repo'])}]({r['url']}) | {r['stars']:,} | {r['license']} | {r['topic']} | "
                 f"{r['decision']}{' ·repos.json' if r['credited_in_repos_json'] else ''} | {short_ids(r['transferred'])} |")
    return "\n".join(L) + "\n"


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def cmd_build(check: bool) -> int:
    tracker = build_tracker(load_json(SNAPSHOT, {"rows": []}), load_json(REVIEW, {}))
    outs = {TRACKER: dump(tracker), TABLE: render_table(tracker)}
    stale = [p for p, txt in outs.items() if not p.is_file() or p.read_text(encoding="utf-8") != txt]
    if check:
        for p in stale:
            print(f"stale: {p.relative_to(SK)}")
        print("github-top-1000: up to date" if not stale else "github-top-1000: run build")
        return 1 if stale else 0
    for p, txt in outs.items():
        p.write_text(txt, encoding="utf-8")
    print(f"wrote {TRACKER.relative_to(SK)} and {TABLE.relative_to(SK)}: {tracker['counts']['total']} repos, "
          f"{tracker['counts']['relevant']} relevant, decisions {tracker['counts']['decision']}")
    return 0


def tracker_rows(extra: bool = False) -> list:
    t = build_tracker(load_json(SNAPSHOT, {"rows": []}), load_json(REVIEW, {}))
    return t["rows"] + (t["extra"] if extra else [])


def cmd_stats(as_json: bool) -> int:
    c = counts(tracker_rows())
    if as_json:
        print(json.dumps(c, ensure_ascii=False, indent=1))
        return 0
    print(f"{c['total']} repos · {c['relevant']} relevant · {c['transferred_ids']} power/tool ids carry transferred methods")
    for key in ("decision", "topic", "license_class"):
        print(f"{key}: " + ", ".join(f"{k} {v}" for k, v in c[key].items()))
    return 0


def cmd_find(words: list, limit: int) -> int:
    terms = [w.lower() for w in words]
    hits = [r for r in tracker_rows(extra=True)
            if all(t in f"{r['repo']} {r['description']} {r['topic']} {r['decision']}".lower() for t in terms)]
    for r in hits[:limit]:
        print(f"#{r['rank'] or '-':<4} {r['repo']:<45} {r['stars']:>7,}  {r['license']:<13} {r['topic']:<22} {r['decision']}"
              + (f"  → {', '.join(r['transferred'])}" if r["transferred"] else ""))
    print(f"{len(hits)} match(es)")
    return 0 if hits else 1


def cmd_show(repo: str) -> int:
    t = build_tracker(load_json(SNAPSHOT, {"rows": []}), load_json(REVIEW, {}))
    for r in t["rows"] + t["extra"]:
        if r["repo"].lower() == repo.lower():
            print(json.dumps(r, ensure_ascii=False, indent=1))
            return 0
    print(f"not in the snapshot: {repo}")
    return 1


def merge_pool(ranked: list, extra: dict, limit: int = 1000) -> list:
    """Merge the ranking site's rows with deps.dev records of the supplement list, drop redirect duplicates
    (same repository name, stars within 1 %), sort by stars and keep the top `limit`, re-ranked from 1."""
    pool = {r["repo"].lower(): dict(r, via="gitstar") for r in ranked}
    for repo, rec in extra.items():
        if not rec or repo.lower() in pool:
            continue
        stars, name = rec.get("starsCount") or 0, repo.split("/")[-1].lower()
        if any(v["repo"].split("/")[-1].lower() == name and abs(v["stars"] - stars) <= 0.01 * max(stars, 1) for v in pool.values()):
            continue
        pool[repo.lower()] = {"repo": repo, "stars": stars, "language": "", "license": rec.get("license") or "none",
                              "description": " ".join((rec.get("description") or "").split()), "via": "supplement"}
    rows = sorted(pool.values(), key=lambda r: (-r["stars"], r["repo"].lower()))[:limit]
    return [dict(r, rank=i) for i, r in enumerate(rows, 1)]


def cmd_refresh(out: Path, pages: int) -> int:  # network; writes only to --out
    import concurrent.futures as cf
    import html as _html
    import urllib.parse
    import urllib.request

    def deps(repo):
        url = "https://api.deps.dev/v3/projects/" + urllib.parse.quote("github.com/" + repo.lower(), safe="")
        try:
            return repo, json.load(urllib.request.urlopen(url, timeout=20))
        except Exception:  # noqa: BLE001 - an unindexed project is a fact, not an error
            return repo, None

    ranked = []
    pat = re.compile(r'<a class="list-group-item paginated_item" href="/([^"]+)">.*?stargazers_count pull-right\'>\s*<i[^>]*></i>\s*(\d+)'
                     r'\s*</span>.*?repo-description\' title=\'(.*?)\'>.*?repo-language\'>\s*<span>(.*?)</span>', re.S)
    for p in range(1, pages + 1):
        page = urllib.request.urlopen(f"https://gitstar-ranking.com/repositories?page={p}", timeout=30).read().decode("utf-8", "replace")
        for m in pat.finditer(page):
            lang = _html.unescape(m.group(4))
            ranked.append({"repo": m.group(1), "stars": int(m.group(2)), "language": "" if lang == "No language available" else lang,
                           "description": " ".join(_html.unescape(m.group(3)).split())})
    snap = load_json(SNAPSHOT, {})
    with cf.ThreadPoolExecutor(16) as ex:
        found = dict(ex.map(deps, [r["repo"] for r in ranked]))
        extra = dict(ex.map(deps, snap.get("supplement", [])))
    for r in ranked:
        rec = found.get(r["repo"])
        r["license"] = "unknown" if rec is None else (rec.get("license") or "none")
        r["stars"] = (rec or {}).get("starsCount") or r["stars"]
    snap["rows"] = [{k: r[k] for k in ("rank", "repo", "stars", "language", "license", "description", "via")}
                    for r in merge_pool(ranked, extra)]
    out.write_text(dump(snap), encoding="utf-8")
    print(f"wrote {out}: {len(snap['rows'])} rows; review the diff, then copy it over {SNAPSHOT.relative_to(SK)} and run build")
    return 0


def self_test() -> int:
    snap = {"fetched": "2000-01-01", "sources": {}, "rows": [
        {"rank": 1, "repo": "a/prompt-guide", "stars": 9, "license": "MIT", "description": "Prompt engineering guide"},
        {"rank": 2, "repo": "b/anim", "stars": 8, "license": "GPL-3.0", "description": "JavaScript animation engine"},
        {"rank": 3, "repo": "c/kernel", "stars": 7, "license": "non-standard", "description": "An operating system kernel"},
        {"rank": 4, "repo": "d/payloads", "stars": 6, "license": "MIT", "description": "Payloads for pentest"},
        {"rank": 5, "repo": "e/agentkit", "stars": 5, "license": "Apache-2.0", "description": "Build AI agents"},
        {"rank": 6, "repo": "f/diagrams", "stars": 4, "license": "none", "description": "Draw diagrams in markdown"}]}
    review = {"repos": {"e/agentkit": {"transferred": ["AGENT-1"]}, "c/kernel": {"decision": "skip", "why": "test"}}}
    rows = {r["repo"]: r for r in build_tracker(snap, review, ({"a/prompt-guide": ["P-1"]}, set()))["rows"]}
    want = {"a/prompt-guide": ("prompt-engineering", "transferred"), "b/anim": ("motion-animation", "reference"),
            "c/kernel": ("engineering-general", "skip"), "d/payloads": ("security", "skip"),
            "e/agentkit": ("agents-skills", "transferred"), "f/diagrams": ("data-viz-diagrams", "reference")}
    bad = [(k, (rows[k]["topic"], rows[k]["decision"]), v) for k, v in want.items() if (rows[k]["topic"], rows[k]["decision"]) != v]
    if build_tracker(snap, review, ({}, set())) != build_tracker(snap, review, ({}, set())):
        bad.append(("determinism", None, None))
    if "| 5 | [e/agentkit]" not in render_table(build_tracker(snap, review, ({}, set()))):
        bad.append(("table", None, None))
    merged = merge_pool([{"repo": "x/a", "stars": 10, "language": "", "description": ""},
                         {"repo": "new/roadmap", "stars": 100, "language": "", "description": ""}],
                        {"old/roadmap": {"starsCount": 100}, "y/b": {"starsCount": 50, "license": "MIT"}, "z/c": None}, limit=2)
    if [(r["rank"], r["repo"], r["via"]) for r in merged] != [(1, "new/roadmap", "gitstar"), (2, "y/b", "supplement")]:
        bad.append(("merge_pool", merged, None))
    for b in bad:
        print("FAIL", b)
    print("self-test OK" if not bad else f"self-test: {len(bad)} failure(s)")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    s = sub.add_parser("stats")
    s.add_argument("--json", action="store_true")
    f = sub.add_parser("find")
    f.add_argument("words", nargs="+")
    f.add_argument("--limit", type=int, default=40)
    sh = sub.add_parser("show")
    sh.add_argument("repo")
    rf = sub.add_parser("refresh")
    rf.add_argument("--out", type=Path, required=True)
    rf.add_argument("--pages", type=int, default=10)
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.cmd == "build":
        return cmd_build(a.check)
    if a.cmd == "stats":
        return cmd_stats(a.json)
    if a.cmd == "find":
        return cmd_find(a.words, a.limit)
    if a.cmd == "show":
        return cmd_show(a.repo)
    if a.cmd == "refresh":
        if a.out.resolve() == SNAPSHOT.resolve():
            print("refusing to overwrite the committed snapshot; write elsewhere and review the diff")
            return 2
        return cmd_refresh(a.out, a.pages)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
