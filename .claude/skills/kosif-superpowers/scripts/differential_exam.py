#!/usr/bin/env python3
"""Differential hidden-exam scorer: compare a reference run with a candidate run.

A method distilled (in our own code, no upstream code copied) from the public
codex-clone-hidden-test-kit write-up: write the exam before the work starts and
seal it, run the reference and the candidate against the same scripted inputs,
save what each one sent and did into one folder per scenario, then score file by
file after masking volatile values (ids, timestamps, temp paths). The scorer is
only trusted after a self-check: the reference against itself, or two reference
runs against each other, must score 100%.

Layout of a run folder: <run>/<scenario>/<any files>. JSON files are compared as
data (key order ignored, --skip-key fields dropped); other files as normalised text.

Commands:
  seal EXAM_DIR --out SEAL.json        hash every exam file before the work starts
  verify-seal EXAM_DIR SEAL.json       prove the exam was not edited afterwards
  self-check REF [REF2]                the scorer must give 100% on reference vs reference
  compare REF CAND [--min 95]          score the candidate per scenario and file
Stdlib only; it reads files and runs nothing.
"""
import argparse
import hashlib
import json
import os
import re
import sys

SCHEMA = "kosif.differential-exam.v1"

DEFAULT_RULES = [
    (r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", "<UUID>"),
    (r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:?\d\d)?", "<TS>"),
    (r"\b\d{13}\b", "<EPOCH_MS>"),
    (r"\b1\d{9}\b", "<EPOCH>"),
    (r"\b(?:tmp|temp)[A-Za-z0-9_.-]*[A-Za-z0-9]{6,}\b", "<TMPNAME>"),
    (r"\b[0-9a-f]{24,64}\b", "<HEX>"),
    (r"\b\d+(?:\.\d+)? ?(?:ms|seconds|s)\b", "<DURATION>"),
]


def build_rules(extra, roots, defaults=True):
    rules = [(re.compile(p), t) for p, t in DEFAULT_RULES] if defaults else []
    for root in roots or []:
        rules.insert(0, (re.compile(re.escape(root.rstrip("/"))), "<ROOT>"))
    for spec in extra or []:
        if "=>" not in spec:
            raise SystemExit(f"--rule needs REGEX=>TOKEN, got {spec!r}")
        pattern, token = spec.split("=>", 1)
        rules.append((re.compile(pattern), token))
    return rules


def norm_text(text, rules):
    for rx, token in rules:
        text = rx.sub(token, text)
    return text


def norm_data(obj, rules, skip):
    if isinstance(obj, dict):
        return {k: norm_data(v, rules, skip) for k, v in sorted(obj.items()) if k not in skip}
    if isinstance(obj, list):
        return [norm_data(v, rules, skip) for v in obj]
    if isinstance(obj, str):
        return norm_text(obj, rules)
    return obj


def load_file(path, rules, skip):
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8", errors="replace")
    if path.endswith(".json"):
        try:
            return "json", norm_data(json.loads(text), rules, skip)
        except ValueError:
            pass
    if path.endswith(".jsonl"):
        rows = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(norm_data(json.loads(line), rules, skip))
            except ValueError:
                rows.append(norm_text(line, rules))
        return "jsonl", rows
    return "text", [norm_text(line.rstrip(), rules) for line in text.splitlines()]


def scenario_files(run_dir):
    out = {}
    for name in sorted(os.listdir(run_dir)):
        sdir = os.path.join(run_dir, name)
        if not os.path.isdir(sdir):
            continue
        files = []
        for root, _dirs, names in os.walk(sdir):
            for fname in names:
                files.append(os.path.relpath(os.path.join(root, fname), sdir))
        out[name] = sorted(files)
    return out


def first_difference(a, b):
    if type(a) is not type(b):
        return f"type {type(a).__name__} != {type(b).__name__}"
    if isinstance(a, list):
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                return f"[{i}] " + (first_difference(x, y) if isinstance(x, (dict, list)) else f"{x!r} != {y!r}")[:300]
        return f"length {len(a)} != {len(b)}"
    if isinstance(a, dict):
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b:
                return f"key {key!r} only in {'reference' if key in a else 'candidate'}"
            if a[key] != b[key]:
                return f".{key} " + (first_difference(a[key], b[key]) if isinstance(a[key], (dict, list)) else f"{a[key]!r} != {b[key]!r}")[:300]
    return f"{a!r} != {b!r}"[:300]


def score(ref, cand, rules, skip):
    ref_s, cand_s = scenario_files(ref), scenario_files(cand)
    scenarios, ok_total, all_total = [], 0, 0
    for name in sorted(ref_s):
        checks = []
        cand_files = set(cand_s.get(name, []))
        for rel in ref_s[name]:
            entry = {"file": rel}
            if name not in cand_s:
                entry.update(ok=False, why="scenario missing in candidate")
            elif rel not in cand_files:
                entry.update(ok=False, why="file missing in candidate")
            else:
                kind_a, a = load_file(os.path.join(ref, name, rel), rules, skip)
                _kind_b, b = load_file(os.path.join(cand, name, rel), rules, skip)
                entry["kind"] = kind_a
                entry["ok"] = a == b
                if not entry["ok"]:
                    entry["why"] = first_difference(a, b)
            checks.append(entry)
        for rel in sorted(cand_files - set(ref_s[name])):
            checks.append({"file": rel, "ok": False, "why": "extra file only in candidate"})
        ok = sum(1 for c in checks if c["ok"])
        ok_total += ok
        all_total += len(checks)
        scenarios.append({"scenario": name, "ok": ok, "total": len(checks), "checks": checks})
    extra = sorted(set(cand_s) - set(ref_s))
    pct = round(100.0 * ok_total / all_total, 2) if all_total else 0.0
    return {"schema": SCHEMA, "reference": ref, "candidate": cand, "ok": ok_total,
            "total": all_total, "percent": pct, "scenarios": scenarios,
            "extra_candidate_scenarios": extra}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(exam_dir):
    rows = {}
    for root, _dirs, names in os.walk(exam_dir):
        for fname in names:
            path = os.path.join(root, fname)
            rows[os.path.relpath(path, exam_dir).replace(os.sep, "/")] = sha256(path)
    return dict(sorted(rows.items()))


def print_report(report, as_json):
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return
    for sc in report["scenarios"]:
        print(f"{sc['scenario']}: {sc['ok']}/{sc['total']}")
        for c in sc["checks"]:
            if not c["ok"]:
                print(f"  FAIL {c['file']}: {c.get('why', '')}")
    for name in report["extra_candidate_scenarios"]:
        print(f"note: candidate has extra scenario {name} (not scored)")
    print(f"TOTAL {report['ok']}/{report['total']} = {report['percent']}%")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def scoring_args(p):
        p.add_argument("--rule", action="append", help="extra mask REGEX=>TOKEN (repeatable)")
        p.add_argument("--root", action="append", help="absolute path prefix to mask as <ROOT> (repeatable)")
        p.add_argument("--skip-key", action="append", default=[], help="JSON key to drop everywhere (repeatable)")
        p.add_argument("--no-default-masks", action="store_true", help="use only --rule/--root masks")
        p.add_argument("--json", action="store_true", help="print the full JSON report")

    p = sub.add_parser("seal", help="hash every exam file before the work starts")
    p.add_argument("exam_dir")
    p.add_argument("--out", required=True)
    p = sub.add_parser("verify-seal", help="check the exam files still match the seal")
    p.add_argument("exam_dir")
    p.add_argument("seal")
    p = sub.add_parser("self-check", help="reference vs itself or vs a second reference run must be 100%%")
    p.add_argument("ref")
    p.add_argument("ref2", nargs="?")
    scoring_args(p)
    p = sub.add_parser("compare", help="score a candidate run against the reference run")
    p.add_argument("ref")
    p.add_argument("cand")
    p.add_argument("--min", type=float, default=None, help="exit 1 below this percentage")
    scoring_args(p)
    args = ap.parse_args(argv)

    if args.cmd == "seal":
        if os.path.abspath(args.out).startswith(os.path.abspath(args.exam_dir) + os.sep):
            raise SystemExit("--out must be outside the exam folder")
        rows = manifest(args.exam_dir)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"schema": SCHEMA + ".seal", "files": rows}, fh, indent=1)
        print(f"sealed {len(rows)} file(s) → {args.out}")
        return 0
    if args.cmd == "verify-seal":
        with open(args.seal, encoding="utf-8") as fh:
            sealed = json.load(fh)["files"]
        now = manifest(args.exam_dir)
        changed = sorted(k for k in sealed if k in now and now[k] != sealed[k])
        missing = sorted(set(sealed) - set(now))
        added = sorted(set(now) - set(sealed))
        for label, rows in (("changed", changed), ("missing", missing), ("added", added)):
            for row in rows:
                print(f"{label}: {row}")
        intact = not (changed or missing or added)
        print("seal intact" if intact else "seal BROKEN: the exam changed after it was sealed")
        return 0 if intact else 1

    for d in [args.ref] + [x for x in (getattr(args, "cand", None), getattr(args, "ref2", None)) if x]:
        if not os.path.isdir(d):
            raise SystemExit(f"not a folder: {d}")
    rules = build_rules(args.rule, args.root, not args.no_default_masks)
    skip = set(args.skip_key)
    if args.cmd == "self-check":
        report = score(args.ref, args.ref2 or args.ref, rules, skip)
        report["scorer_trusted"] = report["total"] > 0 and report["ok"] == report["total"]
        print_report(report, args.json)
        if not args.json:
            print("scorer trusted" if report["scorer_trusted"] else
                  "scorer NOT trusted: mask the volatile values above (--rule/--root/--skip-key) and rerun")
        return 0 if report["scorer_trusted"] else 1
    report = score(args.ref, args.cand, rules, skip)
    print_report(report, args.json)
    if args.min is not None and report["percent"] < args.min:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
