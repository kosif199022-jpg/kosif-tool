#!/usr/bin/env python3
"""KOSIF Atlas ledger — سجل مراجعة كل مهارات الأطلس (14,793 مهارة).

atlas_5000.py answers "which safe Atlas skills does a power cite?". The ledger answers the wider
question "what happened to every one of the Atlas skills?": each skill gets exactly one status.

  covered           a KOSIF power cites the skill's folder (proof link or atlas.ids)
  pattern           the skill is one instance of a method a KOSIF power already holds (for example
                    one vendor's "rate-limits" stage); vendor specifics stay in the Atlas folder
  duplicate         same description or same normalised name as an earlier Atlas skill
  excluded-review   verdict is not READ_ONLY_OK (the skill ships scripts or install steps); not read
  excluded-copyleft copyleft license; referenced, never copied
  excluded-risk     KOSIF inspection raised risk flags
  pending           safe, unique and not yet decided; the next batches start here

  python3 scripts/atlas_ledger.py build            # write data/atlas_ledger.json.gz
  python3 scripts/atlas_ledger.py build --check    # exit 1 when the committed ledger is stale
  python3 scripts/atlas_ledger.py stats [--json]
  python3 scripts/atlas_ledger.py show 6802
  python3 scripts/atlas_ledger.py list --status pending --theme security --top 20
  python3 scripts/atlas_ledger.py --self-test

Inputs: data/atlas_capability_index.json.gz (inert metadata), data/powers/*.json and the reviewed
rules in data/atlas-ledger-decisions.json. Stdlib only, offline, read-only except `build`. It never
reads or runs Atlas code; a status records a review decision, not an execution receipt.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas_5000  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
POWERS = SKILL / "data" / "powers"
DECISIONS = SKILL / "data" / "atlas-ledger-decisions.json"
OUT = SKILL / "data" / "atlas_ledger.json.gz"
SCHEMA = "kosif.atlas-ledger.v1"
STATUSES = ("covered", "pattern", "duplicate", "excluded-review", "excluded-copyleft",
            "excluded-risk", "pending")


def power_atlas_ids(powers_dir: Path = POWERS) -> dict:
    """Atlas numeric id -> power ids that list it in atlas.ids."""
    out = collections.defaultdict(set)
    for f in sorted(powers_dir.glob("*.json")):
        for rec in json.loads(f.read_text(encoding="utf-8")):
            for i in (rec.get("atlas") or {}).get("ids") or []:
                out[_aid(i)].add(rec["id"])
    return out


def _aid(value):
    """Atlas ids are ints, except the copyleft index's "x…" ids; power files store either as text."""
    text = str(value)
    return int(text) if text.isdigit() else text


def load_decisions(path: Path = DECISIONS) -> list:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get("rules", [])


def rule_matches(rule: dict, s: dict) -> bool:
    m = rule.get("match", {})
    if "ids" in m and s["id"] not in m["ids"]:
        return False
    if "source_prefix" in m and not (s.get("source") or "").startswith(m["source_prefix"]):
        return False
    if "skill_suffix" in m and not any(s["skill"].endswith(x) for x in m["skill_suffix"]):
        return False
    if "plugin" in m and s.get("plugin") not in m["plugin"]:
        return False
    return bool(m)


def classify(idx: dict, cov: dict, ids_map: dict, rules: list) -> list:
    rows, by_hash, by_norm = [], {}, {}
    for s in idx["skills"]:
        powers = sorted(set(cov.get(s["path"], [])) | ids_map.get(s["id"], set()))
        status, why, ref = None, "", None
        if powers:
            status, why = "covered", "cited by a KOSIF power"
        elif s.get("copyleft"):
            status, why = "excluded-copyleft", f"copyleft license {s.get('license')}"
        elif s.get("verdict") != "READ_ONLY_OK":
            status, why = "excluded-review", f"verdict {s.get('verdict')}"
        elif s.get("risk"):
            status, why = "excluded-risk", "risk flags: " + ",".join(map(str, s["risk"]))
        else:
            dup = by_hash.get(s.get("desc_hash")) or by_norm.get(s.get("norm"))
            if dup is not None:
                status, why, ref = "duplicate", f"same as Atlas #{dup}", dup
            else:
                for r in rules:
                    if rule_matches(r, s):
                        status, why, powers = r["status"], r["reason"], list(r.get("powers", []))
                        break
                else:
                    status, why = "pending", "safe and unique; not yet reviewed"
        if atlas_5000.is_safe(s):
            by_hash.setdefault(s.get("desc_hash"), s["id"])
            by_norm.setdefault(s.get("norm"), s["id"])
        rows.append({"id": s["id"], "theme": s.get("theme"), "status": status, "powers": powers,
                     "reason": why, "dup_of": ref})
    return rows


def build(idx=None, powers_dir: Path = POWERS, decisions: Path = DECISIONS) -> dict:
    idx = idx or atlas_5000.load_index()
    rows = classify(idx, atlas_5000.coverage_map(powers_dir), power_atlas_ids(powers_dir),
                    load_decisions(decisions))
    counts = collections.Counter(r["status"] for r in rows)
    return {
        "schema": SCHEMA, "atlas": idx.get("atlas"), "total": len(rows),
        "counts": {k: counts.get(k, 0) for k in STATUSES},
        "note": "Each status is a review decision over inert metadata; nothing in the Atlas was executed.",
        "rows": [[r["id"], r["status"], r["powers"], r["reason"]] for r in rows],
        "themes": {str(r["id"]): r["theme"] for r in rows},
    }


def dump(ledger: dict) -> bytes:
    text = json.dumps(ledger, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return gzip.compress(text.encode("utf-8"), mtime=0)


def load(path: Path = OUT) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def stats(ledger: dict) -> dict:
    per = collections.defaultdict(collections.Counter)
    for i, st, _, _ in ledger["rows"]:
        per[ledger["themes"][str(i)]][st] += 1
    return {"total": ledger["total"], "counts": ledger["counts"],
            "themes": {t: dict(c) for t, c in sorted(per.items(), key=lambda kv: -sum(kv[1].values()))}}


def self_test() -> int:
    idx = {"atlas": "t", "skills": [
        {"id": 1, "path": "skills/a/1-x", "skill": "x", "norm": "x", "desc_hash": "h1", "verdict": "READ_ONLY_OK", "theme": "t"},
        {"id": 2, "path": "skills/a/2-y", "skill": "y", "norm": "y", "desc_hash": "h1", "verdict": "READ_ONLY_OK", "theme": "t"},
        {"id": 3, "path": "skills/a/3-z", "skill": "z", "norm": "z", "desc_hash": "h3", "verdict": "REVIEW_BEFORE_INSTALL", "theme": "t"},
        {"id": 4, "path": "skills/a/4-w", "skill": "w", "norm": "w", "desc_hash": "h4", "verdict": "READ_ONLY_OK", "copyleft": True, "license": "GPL-3.0", "theme": "t"},
        {"id": 5, "path": "skills/b/5-v-rate-limits", "skill": "v-rate-limits", "norm": "v", "desc_hash": "h5", "verdict": "READ_ONLY_OK", "source": "https://x/pack", "theme": "t"},
        {"id": 6, "path": "skills/b/6-u", "skill": "u", "norm": "u", "desc_hash": "h6", "verdict": "READ_ONLY_OK", "risk": ["net"], "theme": "t"},
        {"id": 7, "path": "skills/b/7-q", "skill": "q", "norm": "q", "desc_hash": "h7", "verdict": "READ_ONLY_OK", "theme": "t"},
    ]}
    rules = [{"match": {"source_prefix": "https://x/", "skill_suffix": ["-rate-limits"]}, "status": "pattern",
              "powers": ["P-2"], "reason": "stage"}]
    rows = {r["id"]: r for r in classify(idx, {"skills/a/1-x": ["P-1"]}, {7: {"P-7"}}, rules)}
    checks = [
        rows[1]["status"] == "covered" and rows[1]["powers"] == ["P-1"],
        rows[2]["status"] == "duplicate" and rows[2]["dup_of"] == 1,
        rows[3]["status"] == "excluded-review",
        rows[4]["status"] == "excluded-copyleft",
        rows[5]["status"] == "pattern" and rows[5]["powers"] == ["P-2"],
        rows[6]["status"] == "excluded-risk",
        rows[7]["status"] == "covered" and rows[7]["powers"] == ["P-7"],
        not rule_matches({"match": {}}, idx["skills"][0]),
        set(r["status"] for r in rows.values()) <= set(STATUSES),
    ]
    for n, ok in enumerate(checks, 1):
        print(f"{'ok ' if ok else 'FAIL'} check {n}")
    return 0 if all(checks) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build", help="write data/atlas_ledger.json.gz")
    b.add_argument("--check", action="store_true", help="exit 1 if the committed ledger is stale")
    s = sub.add_parser("stats", help="counts per status and theme"); s.add_argument("--json", action="store_true")
    w = sub.add_parser("show", help="one Atlas skill's status"); w.add_argument("id", type=_aid)
    li = sub.add_parser("list", help="skills with one status")
    li.add_argument("--status", choices=STATUSES, default="pending")
    li.add_argument("--theme"); li.add_argument("--top", type=int, default=20)
    li.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.cmd == "build":
        data = dump(build())
        if args.check:
            fresh = OUT.exists() and OUT.read_bytes() == data
            print("atlas ledger is up to date" if fresh else "atlas ledger is stale: run build", file=sys.stderr)
            return 0 if fresh else 1
        OUT.write_bytes(data)
        print(json.dumps(load(OUT)["counts"]))
        return 0
    if args.cmd is None:
        ap.print_help()
        return 2
    ledger = load()
    if args.cmd == "stats":
        st = stats(ledger)
        if args.json:
            print(json.dumps(st, ensure_ascii=False, indent=1))
        else:
            print(f"Atlas {st['total']:,} skills: " + ", ".join(f"{k} {v:,}" for k, v in st["counts"].items()))
            for t, c in st["themes"].items():
                print(f"  {t:28} " + "  ".join(f"{k} {c[k]}" for k in STATUSES if c.get(k)))
        return 0
    idx = {s["id"]: s for s in atlas_5000.load_index()["skills"]}
    if args.cmd == "show":
        row = next((r for r in ledger["rows"] if r[0] == args.id), None)
        if row is None:
            print(json.dumps({"error": f"unknown Atlas id {args.id}"}), file=sys.stderr)
            return 2
        s = idx[args.id]
        print(json.dumps({"id": row[0], "status": row[1], "powers": row[2], "reason": row[3],
                          "plugin": s["plugin"], "skill": s["skill"], "theme": s.get("theme"),
                          "license": s.get("license"),
                          "url": "https://github.com/kosif199022-jpg/kosif-atlas/tree/main/" + s["path"]},
                         ensure_ascii=False, indent=1))
        return 0
    rows = [r for r in ledger["rows"] if r[1] == args.status
            and (not args.theme or ledger["themes"][str(r[0])] == args.theme)][:max(1, min(args.top, 500))]
    out = [{"id": r[0], "skill": idx[r[0]]["plugin"] + "/" + idx[r[0]]["skill"], "powers": r[2], "reason": r[3]}
           for r in rows]
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        for o in out:
            print(f"#{o['id']} {o['skill']} → {', '.join(o['powers']) or o['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
