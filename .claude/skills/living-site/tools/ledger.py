#!/usr/bin/env python3
"""ledger.py: the credit ledger as a gate (KOSIF v5.10).

The Stage 3 gate says "ledger total matches the quote". This makes it a measurement, not a feeling.

  python3 ledger.py add   <ledger.tsv> <model> <credits> <job-id> <path>   # MCP sessions: one line per paid job
  python3 ledger.py sum   <ledger.tsv> [--quote N] [--budget N] [--json]

ledger.tsv columns (tab separated, no header): ISO time, model, credits, job id, path.
gen_image.sh and gen_clip.sh write it for the CLI; in a Higgsfield MCP session write it with `add`.
sum exits 1 when the total is over --budget, or more than 10% over --quote, or a job id is billed twice.
"""
import argparse
import datetime
import json
import os
import sys
from collections import Counter, defaultdict


def read(path):
    rows, bad = [], []
    if not os.path.exists(path):
        return rows, bad
    with open(path, encoding='utf-8') as fh:
        for n, line in enumerate(fh, 1):
            line = line.rstrip('\n')
            if not line.strip():
                continue
            parts = line.split('\t')
            try:
                rows.append({'time': parts[0], 'model': parts[1], 'credits': float(parts[2]),
                             'job': parts[3] if len(parts) > 3 else '', 'path': parts[4] if len(parts) > 4 else ''})
            except (IndexError, ValueError):
                bad.append(n)
    return rows, bad


def cmd_add(ns):
    if ns.credits < 0:
        sys.exit('credits must be >= 0')
    for v in (ns.model, ns.job, ns.path):
        if '\t' in v or '\n' in v:
            sys.exit('fields cannot contain tabs or newlines')
    rows, _ = read(ns.ledger)
    if ns.job and any(r['job'] == ns.job for r in rows):
        sys.exit(f'job {ns.job} is already in the ledger: not adding it twice')
    t = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    os.makedirs(os.path.dirname(os.path.abspath(ns.ledger)), exist_ok=True)
    with open(ns.ledger, 'a', encoding='utf-8') as fh:
        fh.write(f'{t}\t{ns.model}\t{ns.credits:g}\t{ns.job}\t{ns.path}\n')
    print(f'logged {ns.credits:g} credits for {ns.model} ({ns.job or "no job id"})')
    return 0


def cmd_sum(ns):
    rows, bad = read(ns.ledger)
    total = sum(r['credits'] for r in rows)
    by_model = defaultdict(float)
    for r in rows:
        by_model[r['model']] += r['credits']
    dup = sorted(j for j, c in Counter(r['job'] for r in rows if r['job']).items() if c > 1)
    problems = []
    if bad:
        problems.append(f'unreadable line(s): {bad}')
    if dup:
        problems.append(f'job id billed twice: {dup}')
    if ns.budget is not None and total > ns.budget:
        problems.append(f'over budget: {total:g} > {ns.budget:g}')
    if ns.quote is not None and total > ns.quote * 1.10:
        problems.append(f'more than 10% over the quote: {total:g} vs {ns.quote:g}')
    out = {'ledger': ns.ledger, 'jobs': len(rows), 'total': total, 'by_model': dict(by_model),
           'quote': ns.quote, 'budget': ns.budget, 'problems': problems, 'pass': not problems}
    if ns.json:
        print(json.dumps(out, indent=2))
    else:
        if not rows:
            print(f'{ns.ledger}: empty (no credits spent)')
        for m, c in sorted(by_model.items(), key=lambda x: -x[1]):
            print(f'  {m:24} {c:g}')
        print(f'  {"total":24} {total:g} over {len(rows)} job(s)' + (f' · quote {ns.quote:g}' if ns.quote is not None else ''))
        for p in problems:
            print('  FAIL ' + p)
        print('PASS' if not problems else 'FAIL')
    return 0 if not problems else 1


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('add')
    a.add_argument('ledger'); a.add_argument('model'); a.add_argument('credits', type=float)
    a.add_argument('job'); a.add_argument('path')
    s = sub.add_parser('sum')
    s.add_argument('ledger'); s.add_argument('--quote', type=float); s.add_argument('--budget', type=float)
    s.add_argument('--json', action='store_true')
    ns = p.parse_args(argv)
    return cmd_add(ns) if ns.cmd == 'add' else cmd_sum(ns)


if __name__ == '__main__':
    sys.exit(main())
