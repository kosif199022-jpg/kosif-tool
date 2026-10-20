#!/usr/bin/env python3
"""Flag briefs that reuse long word runs from the source descriptions.

The atlas policy is that BRIEF.md files are original writing. This tool compares
every brief against the creator's public description text (kept outside the
repository, e.g. in a scratch directory) and reports any shared run of N words.

  python3 tools/check_originality.py --briefs <dir-with-batch-json> --texts <dir-with-<slug>.txt> [--ngram 6]

Exit codes: 0 clean, 1 when any brief shares a run of >= --ngram words with its
source, 2 when --briefs or --texts is not a folder, --briefs holds no *.json
file, or a batch file is not valid JSON shaped {"briefs": [...]} (2 wins over
1; the other files are still checked and reported). Only briefs
whose id starts with pm- and that have a matching <slug>.txt are compared; the
number of pm- briefs without a source text is reported on stderr.
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
        v = b.get(k) or []
        parts.extend(v if isinstance(v, list) else [v])
    return " ".join(x for x in parts if isinstance(x, str))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--briefs", required=True, help="folder of batch *.json files, each {\"briefs\": [...]}")
    ap.add_argument("--texts", required=True, help="folder of <slug>.txt source descriptions (kept outside the repo)")
    ap.add_argument("--ngram", type=int, default=6, help="shared run length, in words, that counts as reuse (default 6)")
    args = ap.parse_args()
    briefs_dir, texts = Path(args.briefs), Path(args.texts)
    for flag, d in (("--briefs", briefs_dir), ("--texts", texts)):
        if not d.is_dir():
            ap.error(f"{flag} {d} is not a folder")
    if args.ngram < 1:
        ap.error("--ngram must be at least 1")
    files = sorted(briefs_dir.glob("*.json"))
    if not files:
        ap.error(f"--briefs {briefs_dir} has no *.json files")
    total, flagged, no_text, bad = 0, [], 0, []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
            bad.append(f"{f.name}: invalid JSON ({e})")
            continue
        if not isinstance(data, dict) or not isinstance(data.get("briefs"), list):
            bad.append(f'{f.name}: expected an object {{"briefs": [...]}}')
            continue
        for b in data["briefs"]:
            ident = b.get("id") if isinstance(b, dict) else None
            if not isinstance(ident, str) or not ident.startswith("pm-"):
                continue
            src = texts / (ident[3:] + ".txt")
            if not src.exists():
                no_text += 1
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
    if no_text:
        print(f"note: {no_text} pm- brief(s) have no <slug>.txt in {texts} and were not checked", file=sys.stderr)
    for msg in bad:
        print(msg, file=sys.stderr)
    if bad:
        return 2
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
