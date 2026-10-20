#!/usr/bin/env python3
"""Audit *evidence coverage* for every KOSIF catalog entry without executing them.

A catalog row is documentation, not proof of a working capability. Only local
references under kosif-tool are checked for existence; sibling/URL/archives are
unverified in this repository, never silently counted as present.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import re


def local_ref(proof: str, repo: Path):
    if not isinstance(proof, str) or not proof.startswith("kosif-tool/"):
        return None
    raw = proof[len("kosif-tool/"):].split("#", 1)[0]
    # Strip a line suffix: ":12", ":12:4" (line:column) or ":15-16" (line range).
    raw = re.sub(r":\d+(?:[-:]\d+)?$", "", raw)
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or not raw:
        return False
    root = repo.resolve()
    candidate = root.joinpath(*path.parts).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return candidate.exists()


def audit(skill: Path):
    skill = skill.resolve()
    repo = skill.parents[2] if len(skill.parents)>2 else skill
    records = sorted((skill / "data" / "powers").glob("*.json"))
    if not records:
        raise ValueError("powers catalog absent")
    ids = set()
    statuses = Counter()
    scopes = Counter()
    links = Counter()
    families = Counter()
    bad_entries = []
    missing_samples = []
    for file in records:
        data = json.loads(file.read_text(encoding="utf-8-sig"))
        if not isinstance(data, list):
            raise ValueError("family must contain a JSON array: " + file.name)
        for item in data:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                bad_entries.append(f"{file.name}:invalid-record")
                continue
            ident = item["id"]
            if ident in ids:
                bad_entries.append("duplicate:" + ident)
            ids.add(ident)
            statuses[item.get("status", "unknown")] += 1
            scopes[item.get("proof_scope", "unknown")] += 1
            families[file.stem] += 1
            proofs = item.get("proof", [])
            if not isinstance(proofs, list):
                bad_entries.append("proof-not-array:" + ident)
                continue
            if not proofs:
                links["no_evidence_links"] += 1
            for proof in proofs:
                if not isinstance(proof, str):
                    bad_entries.append("non-string-proof:" + ident)
                    continue
                result = local_ref(proof, repo)
                if result is None:
                    links["outside_this_repo_unverified"] += 1
                elif result is True:
                    links["local_reference_exists"] += 1
                else:
                    links["local_reference_missing"] += 1
                    if len(missing_samples) < 12:
                        missing_samples.append({"id": ident, "reference": proof})
    return {"schema": "kosif.catalog.evidence-audit.v1",
            "records_examined": sum(statuses.values()), "unique_ids": len(ids),
            "families_examined": len(families), "statuses_claimed": dict(statuses),
            "proof_scopes_claimed": dict(scopes), "proof_links": dict(links),
            "record_integrity_errors": bad_entries[:30],
            "missing_local_samples": missing_samples,
            "assessment": "Static catalog/link audit only. Existence, claimed proof status, or badge never verifies operational behavior, source integrity or license suitability.",
            "executes_external_code": False, "downloads": False}


def main():
    ap = argparse.ArgumentParser(
        description="Static evidence-coverage audit of the KOSIF powers catalog. "
                    "Exit 0 = clean, 1 = record integrity errors found, "
                    "2 = catalog missing or unreadable.")
    ap.add_argument("--skill", type=Path,
                    default=Path(__file__).resolve().parent.parent,
                    help="skill folder that holds data/powers/*.json (default: this skill)")
    args = ap.parse_args()
    try:
        result = audit(args.skill)
    except (OSError, ValueError) as exc:
        # json.JSONDecodeError is a ValueError. Exit 2 keeps "cannot audit"
        # distinct from exit 1 ("audited, integrity errors found").
        ap.exit(2, f"{ap.prog}: error: {exc} ({args.skill})\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["record_integrity_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
