#!/usr/bin/env python3
"""KOSIF Capability Atlas: bilingual search, traceability and safe Claude task routing.

Reads only repository data; never executes catalog capabilities, installs packages,
reads secret values, or treats catalog proof as a live-session receipt.
Commands: build, stats, doctor, search "task", plan "task", show ID.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
POWERS = SKILL / "data" / "powers"
ROUTES = SKILL / "data" / "capability_routes.json"
INDEX = SKILL / "data" / "capability_atlas_index.json"
GUIDE = SKILL / "references" / "capability-atlas.md"
VERSION = "kosif.capability-atlas.v1"
STOP = set(("the and for with from that this your make build want need what how "
            "please a an is are of to my can i you me "
            "عايز اعمل عمل من في على عن الى إلى و ال دي ده دول هذا هذه لي هل").split())
ALIASES = {
    "محاسبة": ("accounting", "ledger", "finance"),
    "محاسبي": ("accounting", "ledger"),
    "مخزون": ("inventory", "warehouse"),
    "مستودع": ("warehouse", "inventory"),
    "مراجعة": ("audit", "review", "verification"),
    "تدقيق": ("audit", "verification"),
    "مالية": ("finance", "accounting"),
    "فيديو": ("video", "motion", "montage"),
    "مونتاج": ("montage", "edit", "video"),
    "موسيقى": ("music", "rhythm", "audio"),
    "صور": ("image", "photo", "visual"),
    "صورة": ("image", "photo"),
    "برمجة": ("code", "development"),
    "تطبيق": ("app", "build", "code"),
    "اختبار": ("test", "verification"),
    "تفكير": ("think", "reason", "planning"),
    "بحث": ("research", "search"),
    "كتابة": ("writing", "text"),
    "مستند": ("document", "pdf"),
}


def normalized(value):
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    text = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", text)
    text = text.translate(str.maketrans("أإآٱىةؤئ", "اااايهوي"))
    return re.sub(r"[^\w\u0600-\u06ff+#.-]+", " ", text).strip()


def terms(value):
    base = [s for s in normalized(value).split() if len(s) > 1 and s not in STOP]
    words = base[:]
    for s in base:
        words.extend(ALIASES.get(s, ()))
    return list(dict.fromkeys(words))


def signature():
    h = hashlib.sha256()
    for path in sorted(POWERS.glob("*.json")) + [ROUTES]:
        h.update(path.name.encode("utf-8"))
        h.update(path.read_bytes())
    return h.hexdigest()


def read_raw():
    result = []
    for path in sorted(POWERS.glob("*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            raise ValueError("Invalid capability file: " + str(path))
        for row in rows:
            if isinstance(row, dict):
                obj = dict(row)
                obj.setdefault("domain", "motion")
                obj["_source"] = "data/powers/" + path.name
                result.append(obj)
    return result


def compact(p):
    return {
        "id": p.get("id", ""), "name_ar": p.get("name_ar", ""),
        "name_en": p.get("name_en", ""), "family": p.get("family", ""),
        "domain": p.get("domain", "motion"), "status": p.get("status", "documented"),
        "tags": p.get("tags") or [], "requires": p.get("requires") or [],
        "proof_count": len(p.get("proof") or []), "proof_scope": p.get("proof_scope", ""),
        "source": p["_source"], "summary": str(p.get("what") or "")[:230],
        "when": str(p.get("when") or "")[:150],
    }


def assemble():
    rows = [compact(row) for row in read_raw()]
    duplicates = [id for id, num in Counter(row["id"] for row in rows).items() if num > 1]
    if duplicates:
        raise ValueError("Duplicate capability IDs: " + ", ".join(duplicates[:15]))
    routes = json.loads(ROUTES.read_text(encoding="utf-8")).get("routes", [])
    return {
        "schema": VERSION, "source_sha256": signature(),
        "catalog": {
            "total": len(rows),
            "domains": dict(sorted(Counter(r["domain"] for r in rows).items())),
            "families": dict(sorted(Counter(r["family"] for r in rows).items())),
            "statuses": dict(sorted(Counter(r["status"] for r in rows).items())),
            "routes": len(routes),
        },
        "evidence_note": "Catalog status is NOT proof of availability or execution in this session.",
        "powers": rows, "routes": routes,
    }


def guide_text(atlas):
    c = atlas["catalog"]
    lines = [
        "# KOSIF Capability Atlas — Claude discovery index", "",
        "Generated from real repository data. Catalog evidence is NOT a live execution receipt.", "",
        f"**{c['total']:,} powers / {len(c['families'])} families / {len(c['domains'])} domains / {c['routes']} route descriptions.**", "",
        "## Claude task protocol", "",
        "1. Read this guide and the KOSIF master SKILL.md; do not load all power JSON files into context.",
        "2. Run: python scripts/capability_atlas.py plan \"<exact user task>\" --json",
        "3. Select matching capability IDs, process skills and candidate routes; inspect full entry with show ID.",
        "4. Check requirements, local environment, authorization and licensing before running a tool.",
        "5. Execute the actual task, test results, cite receipts, and report what remains unverified.", "",
        "## Commands", "",
        "    python scripts/capability_atlas.py stats --json",
        "    python scripts/capability_atlas.py search \"جرد مستودع قطع غيار\" --top 10 --json",
        "    python scripts/capability_atlas.py plan \"Build a secure accounting app\" --json",
        "    python scripts/capability_atlas.py show DOC-05 --json",
        "    python scripts/capability_atlas.py doctor --json",
        "    python scripts/capability_atlas.py build", "",
        "## Evidence model", "",
        "- proven: recorded proof only, NOT proof of execution on this host.",
        "- ready: catalog claims readiness; still verify environment.",
        "- install/key: prerequisite or consent required; do not install or retrieve secrets automatically.",
        "- seen/documented/idea: informational, not independently verified execution.",
        "- Requirement detection is local and read-only; npm/API/remote services are not assumed available.",
        "- Rebuild after source catalog edits; index freshness is verified by SHA-256.", "",
        "## Families by domain", "",
    ]
    for dom, n in c["domains"].items():
        lines += [f"### {dom}: {n:,} powers", ""]
        counts = Counter(row["family"] for row in atlas["powers"] if row["domain"] == dom)
        for name, count in sorted(counts.items(), key=lambda p: (-p[1], p[0])):
            lines.append(f"- {name}: {count}")
        lines.append("")
    lines.extend([
        "## Decision flow", "",
        "User task -> bilingual matching -> capability IDs -> exact source & proof -> prerequisites",
        "-> obra Superpowers workflow SKILL.md -> authorized execution -> tests and output receipts.", "",
        "Data: data/capability_atlas_index.json; originals: data/powers/*.json;",
        "routes: data/capability_routes.json; workflows: vendor/obra-superpowers-v7/skills/", ""
    ])
    return "\n".join(lines)


def build(write=True):
    atlas = assemble()
    if write:
        INDEX.write_text(json.dumps(atlas, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")
        GUIDE.write_text(guide_text(atlas), encoding="utf-8")
    return atlas


def load():
    sign = signature()
    if INDEX.is_file():
        try:
            data = json.loads(INDEX.read_text(encoding="utf-8"))
            if data.get("schema") == VERSION and data.get("source_sha256") == sign:
                return data, True
        except (OSError, ValueError):
            pass
    return build(write=False), False


def relevance(row, words):
    name = normalized(row["name_en"] + " " + row["name_ar"])
    fam = normalized(row["family"] + " " + row["domain"])
    tags = normalized(" ".join(str(t) for t in row["tags"]))
    other = normalized(row["summary"] + " " + row["when"])
    score = sum((7 if w in name else 0) + (4 if w in fam else 0)
                + (3 if w in tags else 0) + (1 if w in other else 0) for w in words)
    return score + ({"proven": .6, "ready": .35}.get(row["status"], 0) if score else 0)


def search(atlas, phrase, top=10, domain=None):
    words = terms(phrase)
    ranked = [(relevance(r, words), r) for r in atlas["powers"]
              if not domain or r["domain"] == domain]
    ranked = [(score, row) for score, row in ranked if score > 0]
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [dict(row, score=round(score, 2)) for score, row in ranked[:top]]


def requirement_state(required):
    item = str(required)
    if item in ("python3", "python"):
        return {"name": item, "state": "detected", "basis": "current interpreter"}
    kind, sep, name = item.partition(":")
    if not sep and re.fullmatch(r"[A-Za-z0-9_.+-]+", item):
        return {"name": item, "state": "detected" if shutil.which(item) else "not_detected", "basis": "PATH"}
    if kind == "bin":
        return {"name": item, "state": "detected" if shutil.which(name) else "not_detected", "basis": "PATH"}
    if kind == "pip" and re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", name):
        try:
            found = importlib.util.find_spec(name) is not None
        except (ImportError, ValueError, AttributeError):
            found = False
        return {"name": item, "state": "detected" if found else "not_detected", "basis": "import spec"}
    return {"name": item, "state": "unverified", "basis": "check package, account, API, OS or approval"}


def matching_routes(routes, phrase):
    words = terms(phrase)
    matches = []
    for r in routes:
        val = normalized(r.get("title", "") + " " + r.get("summary", "") + " " +
                         " ".join(str(v) for v in r.get("aliases", [])))
        score = sum(3 for w in words if w in val)
        if score:
            matches.append((score, r))
    matches.sort(key=lambda x: (-x[0], x[1].get("id", "")))
    return [dict(row, score=score) for score, row in matches[:4]]


def plan(atlas, phrase, top=7):
    import superpowers_unified
    selected = search(atlas, phrase, top=top)
    return {
        "task": phrase, "master": "kosif-superpowers",
        "source_sha256": atlas["source_sha256"],
        "process_skills": superpowers_unified.plan(phrase)["process_skills"],
        "capabilities": [{
            "id": row["id"], "name": row["name_en"], "name_ar": row["name_ar"],
            "status": row["status"], "score": row["score"], "family": row["family"],
            "source": row["source"], "proof_count": row["proof_count"],
            "requirements": [requirement_state(req) for req in row["requires"]]
        } for row in selected],
        "routes": [{
            "id": r.get("id"), "script": r.get("script"),
            "subcommand": r.get("subcommand"), "permissions": r.get("permissions", []),
            "requires": r.get("requires", []), "score": r["score"]
        } for r in matching_routes(atlas["routes"], phrase)],
        "next": [
            "Read the matching source entry and selected workflow SKILL.md",
            "Probe environment and confirm approval; do not assume prerequisites",
            "Perform authorized execution and preserve test/output receipts",
        ],
        "notice": "This is planning only. No catalog capability was executed.",
    }


def show(identifier):
    for p in read_raw():
        if str(p.get("id", "")).casefold() == identifier.casefold():
            p["requirement_checks"] = [requirement_state(r) for r in p.get("requires", [])]
            p["notice"] = "Catalog record only; proof is not a receipt from this session."
            return p
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    for cmd in ("build", "stats", "doctor"):
        sub.add_parser(cmd).add_argument("--json", action="store_true")
    for cmd in ("search", "plan"):
        p = sub.add_parser(cmd)
        p.add_argument("task")
        p.add_argument("--top", type=int, default=10 if cmd == "search" else 7)
        p.add_argument("--json", action="store_true")
        if cmd == "search":
            p.add_argument("--domain")
    p = sub.add_parser("show")
    p.add_argument("id")
    p.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.command == "build":
        a = build()
        output = {"index": str(INDEX), "guide": str(GUIDE), "catalog": a["catalog"]}
    else:
        a, fresh = load()
        if args.command == "stats":
            output = dict(a["catalog"], index_fresh=fresh)
        elif args.command == "doctor":
            output = {"status": "ready" if fresh else "stale_index",
                      "index_fresh": fresh, "powers": len(a["powers"]),
                      "routes": len(a["routes"]), "no_external_calls": True}
        elif args.command == "search":
            output = search(a, args.task, max(1, min(args.top, 50)), args.domain)
        elif args.command == "plan":
            output = plan(a, args.task, max(1, min(args.top, 30)))
        else:
            output = show(args.id)
            if output is None:
                print("Unknown capability ID: " + args.id, file=sys.stderr)
                return 2
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
