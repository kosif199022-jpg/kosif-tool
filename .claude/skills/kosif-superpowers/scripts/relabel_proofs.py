#!/usr/bin/env python3
"""Set proof_scope on every power record from where its proof paths resolve (repo > session > archive > sibling > receipt > style > url).

    python3 scripts/relabel_proofs.py            # rewrite data/powers/*.json in place
    python3 scripts/relabel_proofs.py --check    # exit 1 when any record would change

repo = file exists in this repository; sibling = path into one of the owner's other repositories (not verifiable here);
session = dated run log; archive = owner upload; receipt = free-text run note. check_skill.py refuses ✅ without a scope.
"""
import glob
import json
import re
import sys
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
REPO = SK.parents[2]
ORDER = ["repo", "session", "archive", "sibling", "receipt", "style", "url", "missing", "none"]
PRE = "kosif-tool/.claude/skills/kosif-superpowers/"


def scope_of(p: str) -> str:
    q = p.split("#")[0]
    if q.startswith(("http://", "https://")):
        return "url"
    if q.startswith("owner-upload:"):
        return "archive"
    if q.startswith("session-"):
        return "session"
    if q.startswith("style:"):
        return "style"
    if q.startswith(PRE):
        return "repo" if (SK / re.sub(r":\d+(-\d+)?$", "", q[len(PRE):])).exists() else "missing"
    if q.startswith("kosif-tool/"):
        return "repo" if (REPO / re.sub(r":\d+(-\d+)?$", "", q[len("kosif-tool/"):])).exists() else "missing"
    head = q.split("/")[0]
    if "/" in q and re.match(r"^[\w.-]+$", head):
        return "sibling"
    return "receipt"


def record_scope(rec: dict) -> str:
    kinds = {scope_of(p) for p in rec.get("proof") or [] if isinstance(p, str) and p.strip()}
    return next((k for k in ORDER if k in kinds), "none")


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report only; exit 1 when any record would change")
    check = ap.parse_args(argv).check
    changed, by_scope = 0, {}
    for f in sorted(glob.glob(str(SK / "data" / "powers" / "*.json"))):
        text = Path(f).read_text(encoding="utf-8")
        rows = json.loads(text)
        dirty = False
        for rec in rows:
            scope = record_scope(rec)
            if rec.get("status") == "proven":
                by_scope[scope] = by_scope.get(scope, 0) + 1
            if rec.get("proof_scope") != scope:
                out = {}
                for k, v in rec.items():
                    if k == "proof_scope":
                        continue
                    out[k] = v
                    if k == "proof":
                        out["proof_scope"] = scope
                out.setdefault("proof_scope", scope)
                rec.clear(); rec.update(out)
                dirty = True; changed += 1
        if dirty and not check:
            indent = 2 if text.startswith("[\n  {") else 1
            Path(f).write_text(json.dumps(rows, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
    print("proven by proof_scope:", dict(sorted(by_scope.items(), key=lambda kv: -kv[1])))
    print(("would change" if check else "relabelled") + f" {changed} record(s)")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
