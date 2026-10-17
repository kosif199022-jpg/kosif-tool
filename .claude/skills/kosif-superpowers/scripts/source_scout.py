#!/usr/bin/env python3
"""KOSIF Community Source Scout: local, deterministic, no network or executors.

Source registry is curated from external GitHub README and repository metadata;
each result is a reference to investigate, not an installed skill or capability.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "community_sources.json"
LICENSE_COPY_SAFE = {"MIT", "Apache-2.0", "BSD-3-Clause"}
VALID_DOMAINS = {"research", "learning", "operations", "engineering", "agents",
                 "prompts", "finance", "creative", "collaboration", "architecture", "python", "media", "data"}
STOP = {"the", "and", "for", "with", "from", "your", "any", "one", "can",
        "how", "what", "this", "that", "you", "app", "tool", "tools",
        "في", "من", "على", "الى", "الي", "عن", "عايز", "محتاج", "اريد",
        "ابغى", "كيف", "ايه", "عمل", "اعمل", "هذه", "هذا", "لي", "على"}


def norm(s):
    s = unicodedata.normalize("NFKC", str(s or "")).lower()
    s = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", s)
    for frm, to in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"),
                    ("ى", "ي"), ("ة", "ه")):
        s = s.replace(frm, to)
    return s


def words(text):
    return {w for w in re.findall(r"[\w]+", norm(text), flags=re.UNICODE)
            if len(w) >= 3 and w not in STOP}


def load(path=DATA):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    validate(obj)
    return obj["sources"]


def validate(obj):
    if not isinstance(obj, dict) or obj.get("schema") != "kosif.community-sources.v1":
        raise ValueError("invalid source schema")
    items = obj.get("sources")
    if not isinstance(items, list) or len(items) != 31:
        raise ValueError("source registry must contain exactly 31 reviewed repos")
    ids, repos = set(), set()
    for row in items:
        if not isinstance(row, dict):
            raise ValueError("source row is not an object")
        fields = ("id", "repo", "url", "license", "domain", "idea_ar",
                  "signals", "caution", "status", "source_checked")
        if any(not row.get(k) for k in fields):
            raise ValueError("incomplete row")
        if row["id"] in ids or row["repo"].lower() in repos:
            raise ValueError("duplicate source or ID")
        ids.add(row["id"])
        repos.add(row["repo"].lower())
        if row["url"] != "https://github.com/" + row["repo"]:
            raise ValueError("source URL does not match repository")
        if row["domain"] not in VALID_DOMAINS or row["status"] != "reference_only":
            raise ValueError("unknown domain or executable status")
        if not isinstance(row["signals"], list) or not all(isinstance(s, str) for s in row["signals"]):
            raise ValueError("invalid signals")
    top = obj.get("python_top10")
    if not isinstance(top, dict) or not isinstance(top.get("items"), list) or len(top["items"]) != 10:
        raise ValueError("missing ranked top 10 Python source snapshot")
    if top.get("method") != "public GitHub repositories with primary language Python ordered by stars":
        raise ValueError("ranking methodology drift")
    if not top.get("observed_date") or not top.get("rank_reference"):
        raise ValueError("ranking provenance missing")
    ranks = top["items"]
    if any(x.get("rank") != i + 1 or x.get("language") != "Python" or
           not isinstance(x.get("stars"), int) or x["stars"] <= 0 or
           x.get("repo", "").lower() not in repos
           for i, x in enumerate(ranks)):
        raise ValueError("ranking rows inconsistent with source catalog")
    if len({x["repo"].lower() for x in ranks}) != 10:
        raise ValueError("duplicate ranked repos")
    if any(ranks[i]["stars"] < ranks[i+1]["stars"] for i in range(9)):
        raise ValueError("Python ranking not sorted by stars descending")
    return True


def suggest(query, sources, limit=5, domain=None, code_reuse=False):
    q=words(query)
    ranked = []
    for row in sources:
        if domain and row["domain"] != domain:
            continue
        full=norm(row["repo"])
        slug=norm(row["repo"].split("/")[-1])
        # Exact repository names are authoritative; partial noun overlap is only a recommendation.
        exact = (full in norm(query)) or (len(slug) >= 7 and slug not in {"python", "tools", "platform"} and
                  re.search(r"(?<![\\w])" + re.escape(slug) + r"(?![\\w])", norm(query)) is not None)
        terms=words(" ".join(row["signals"])+" "+row["repo"])
        common=q & terms
        if not common and not exact:
            continue
        score = len(common) * 2 + (15 if exact else 0)
        if len(common) >= 2:
            score += 3
        if code_reuse and row["license"] not in LICENSE_COPY_SAFE:
            # Nonstandard licenses are never treated as reusable merely because GitHub is public.
            reuse="check_rights_first"
        elif code_reuse:
            reuse="check_file_and_dependency_licenses"
        else:
            reuse="reference_only"
        ranked.append((score, row["repo"].lower(), {
            "id": row["id"], "repo": row["repo"], "url": row["url"],
            "domain": row["domain"], "why": row["idea_ar"], "license": row["license"],
            "matching_terms": sorted(common), "score": score,
            "reuse_gate": reuse, "execution": "not_installed_or_executed",
            "caution": row["caution"],
        }))
    ranked.sort(key=lambda x: (-x[0], x[1]))
    return [r for _, _, r in ranked[:max(1, min(limit, 10))]]


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    sub=cli.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("python-top")
    listed=sub.add_parser("list")
    listed.add_argument("--domain", choices=sorted(VALID_DOMAINS))
    shown=sub.add_parser("show")
    shown.add_argument("repo_or_id")
    task=sub.add_parser("suggest")
    task.add_argument("query", nargs="+")
    task.add_argument("--limit", type=int, default=5)
    task.add_argument("--domain", choices=sorted(VALID_DOMAINS))
    task.add_argument("--code-reuse", action="store_true")
    a=cli.parse_args(argv)
    try:
        rows=load()
        if a.cmd=="check":
            result={"status":"catalog_valid", "source_count":len(rows), "python_rank_count":10,
                    "domains":sorted({x["domain"] for x in rows}), "runtime_proven":False}
        elif a.cmd=="python-top":
            snapshot = json.loads(DATA.read_text(encoding="utf-8"))["python_top10"]
            result = {"status":"rank_snapshot", **snapshot, "live_star_counts":False,
                      "execution":"reference_only"}
        elif a.cmd=="list":
            result={"sources":[{"id":r["id"], "repo":r["repo"], "domain":r["domain"],
                                "license":r["license"]} for r in rows
                                if not a.domain or r["domain"]==a.domain],
                    "execution":"reference_only"}
        elif a.cmd=="show":
            result=next((r for r in rows if r["id"].lower()==a.repo_or_id.lower()
                         or r["repo"].lower()==a.repo_or_id.lower()), None)
            if not result:
                raise ValueError("source not found")
        else:
            result={"query":" ".join(a.query), "results":suggest(" ".join(a.query), rows,
                       limit=a.limit, domain=a.domain, code_reuse=a.code_reuse),
                    "disclaimer":"Source suggestions are not installed tools or tested executions."}
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(json.dumps({"status":"catalog_error", "error_type":type(e).__name__},
                         ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
