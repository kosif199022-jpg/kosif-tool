#!/usr/bin/env python3
"""Rebalance the public discovery index so image/photo tools are represented.

    python3 scripts/rebalance_creative_repos.py run   # query GitHub (gh CLI, network) and rewrite public_repos.json

Only GitHub metadata is fetched, never third-party code. The existing catalog is
merged with the new search results and cut to 1,000 rows by category quota
(lowest-star rows beyond a quota are dropped; there is no separate snapshot, so
review the git diff). Nothing is written when every GitHub query fails.
"""
import collections
import json
import re
import sys
from pathlib import Path
import rea_creative_research_atlas as research

ROOT=research.CATALOG
EXTRA=[
    ("topic:image-editing stars:>2","image-photo"),
    ("topic:image-processing stars:>3","image-photo"),
    ("topic:photo-editing stars:>1","image-photo"),
    ("topic:photography stars:>4","image-photo"),
    ("topic:image-generation stars:>10","image-photo"),
    ("topic:image-manipulation stars:>1","image-photo"),
    ("topic:computer-vision stars:>30","computer-vision-creative"),
    ("topic:creative-coding stars:>10","computer-vision-creative"),
]
UNVERIFIED_MODEL_PROMOTION=re.compile(r"(?i)(?:fable|opus|claude)[-_ .]*5[-_ .]*5")

def acceptable(r):
    sample=(r.get('repository') or '')+' '+(r.get('description') or '')
    return UNVERIFIED_MODEL_PROMOTION.search(sample) is None

def main(argv=None):
    import argparse
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command",choices=["run"],help="run: fetch GitHub metadata and rewrite the catalog")
    ap.parse_args(argv)
    old=json.loads((ROOT/"public_repos.json").read_text(encoding="utf-8"))
    rejected=[r['repository'] for r in old if not acceptable(r)]
    combined={r["repository"]:r for r in old if acceptable(r)}
    errors=[]
    for q,family in EXTRA:
        try:
            results=research.gh("search/repositories",{"q":q,"per_page":100,"sort":"stars","order":"desc"})
            for x in results.get("items",[]):
                if x.get("private") or x.get("archived"): continue
                if not acceptable({'repository':x.get('full_name'),'description':x.get('description')}): continue
                if x["full_name"] not in combined:
                    combined[x["full_name"]]={
                      "repository":x["full_name"],"url":x.get("html_url"),
                      "description":str(x.get("description") or "")[:240],
                      "primary_language":x.get("language"),"stars":x.get("stargazers_count",0),
                      "license_spdx":(x.get("license") or {}).get("spdx_id"),
                      "size_kb":x.get("size"),"default_branch":x.get("default_branch"),
                      "discovery_query":q,"category":family,
                      "github_metadata_observed":True,"rea_code_analyzed":False,
                      "feature_implemented_in_kosif":False}
        except Exception as e:
            errors.append({"query":q,"error":str(e)[:150]})
    if len(errors)==len(EXTRA):
        print(json.dumps({"status":"no_changes_written","why":"every GitHub query failed (gh auth or network?)","errors":errors},ensure_ascii=False,indent=2))
        return 1
    groups=collections.defaultdict(list)
    for r in combined.values():
        groups[r["category"]].append(r)
    for rows in groups.values():
        rows.sort(key=lambda x:(-int(x.get("stars") or 0),x["repository"]))
    limits={"video-film":380,"motion-vfx":260,"image-photo":320,
            "computer-vision-creative":40,"speech-typography":40}
    selected=[]
    for category,limit in limits.items():
        selected.extend(groups[category][:limit])
    if len(selected)<1000:
        chosen={r["repository"] for r in selected}
        available=sorted((r for r in combined.values() if r["repository"] not in chosen),
                         key=lambda x:-int(x.get("stars") or 0))
        selected+=available[:1000-len(selected)]
    selected=selected[:1000]
    if len({x["repository"] for x in selected})!=len(selected):
        raise RuntimeError("non-unique catalog")
    research.save_json(ROOT/"public_repos.json",selected)
    research.save_json(ROOT/"rebalance_errors.json",errors)
    print(json.dumps({"unique":len(selected),"categories":dict(collections.Counter(x["category"] for x in selected)),
                      "excluded_unverified_marketing_count":len(rejected),
                      "errors":errors,"status":"GitHub metadata ONLY; not REA source analysis"},ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__":
    sys.exit(main())
