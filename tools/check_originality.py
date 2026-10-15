#!/usr/bin/env python3
"""Flag briefs that reuse long word runs from the source descriptions.

The atlas policy is that BRIEF.md files are original writing. This tool compares
every brief against the creator's public description text (kept outside the
repository, e.g. in a scratch directory) and reports any shared run of N words.

  python3 tools/check_originality.py --briefs <dir-with-batch-json> --texts <dir-with-<slug>.txt> [--ngram 6]

Exit code 1 when any brief shares a run of >= --ngram words with its source.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STOP_RUNS = {"of the", "in the", "to the", "on the", "and the", "for the"}


def words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9']+", text.lower()) if w]


def shared_runs(a: list[str], b: list[str], n: int) -> list[str]:
    grams = {" ".join(b[i:i + n]) for i in range(max(0, len(b) - n + 1))}
    hits = []
    for i in range(max(0, len(a) - n + 1)):
        g = " ".join(a[i:i + n])
        if g in grams and g not in hits:
            hits.append(g)
    return hits


def brief_text(b: dict) -> str:
    parts = [b.get("summary_en", ""), b.get("concept_en", ""), b.get("assumptions_en", "")]
    for k in ("scenes_en", "motion_rules_en", "facts_from_source", "keywords"):
        parts.extend(b.get(k) or [])
    return " ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--briefs", required=True)
    ap.add_argument("--texts", required=True)
    ap.add_argument("--ngram", type=int, default=6)
    args = ap.parse_args()
    texts = Path(args.texts)
    total, flagged = 0, []
    for f in sorted(Path(args.briefs).glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        for b in data.get("briefs", []):
            ident = b.get("id", "")
            if not ident.startswith("pm-"):
                continue
            src = texts / (ident[3:] + ".txt")
            if not src.exists():
                continue
            total += 1
            # skip the TITLE/TAGS header lines of the source file
            body = "\n".join(l for l in src.read_text(encoding="utf-8").splitlines() if not l.startswith(("TITLE:", "TAGS:", "TYPE:")))
            runs = shared_runs(words(brief_text(b)), words(body), args.ngram)
            if runs:
                flagged.append((ident, f.name, runs))
    for ident, fname, runs in flagged:
        print(f"{ident} ({fname}): {len(runs)} shared run(s) of {args.ngram}+ words")
        for r in runs[:5]:
            print("   ·", r)
    print(f"checked {total} briefs, flagged {len(flagged)}")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
