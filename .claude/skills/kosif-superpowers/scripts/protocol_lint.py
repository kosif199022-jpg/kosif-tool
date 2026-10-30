#!/usr/bin/env python3
"""protocol_lint.py: consistency gate for a USIP release folder (KOSIF v5.11).

Every release so far drifted somewhere: a footer that still points at an old version, a quick card
numbered 14, 16, 15, a README that names a step the paste file does not have, an annex range that
stops one short. This reads the release files and fails on that kind of drift. It changes nothing.

  python3 protocol_lint.py <release-dir> --version 5.11 [--project-root /mnt/project-files] [--json]

Checks
  V  version     every main file names the release version in its title line
  S  stale       no link to an older USIP_PORTABLE_v5_X file outside a "what's new" history line
  T  toc         every entry in the FULL file's contents list points at a real heading
  C  card        numbered lists in the quick card / paste steps run 1..N with no gap or swap
  A  annex       the "A1…An" range covers the highest annex named anywhere, and every annex file
                 in the folder is routed from the compact file
  R  readme      every file the README lists exists, and every main file is listed
  P  paths       project-folder paths the text names (living-site/..., protocol/...) exist (needs --project-root)
  Z  size        the compact paste file stays under 40 KB (it is pasted as a first message)
Exit 1 on any failure. Warnings never fail the gate but are printed.
"""
import argparse
import glob
import json
import os
import re
import sys
import unicodedata

ARABIC_DIGITS = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def gh_anchor(heading):
    """GitHub-style anchor: lower case, keep letters, marks (Arabic tanween), digits, '-', '_' and spaces."""
    h = heading.strip().lower()
    h = ''.join(c for c in h if c in '-_ ' or unicodedata.category(c)[0] in 'LMN')
    return h.replace(' ', '-')


def find(rel, pattern):
    hits = sorted(glob.glob(os.path.join(rel, pattern)))
    return hits[0] if hits else None


def lint(rel, version, project_root=None):
    vtag = version.replace('.', '_')
    files = {
        'compact': find(rel, f'USIP_PORTABLE_v{vtag}.md'),
        'full': find(rel, f'USIP_PORTABLE_FULL_v{vtag}.md'),
        'paste': find(rel, 'USIP_PASTE.md'),
        'readme': find(rel, 'README.md'),
    }
    fails, warns = [], []

    def fail(code, msg):
        fails.append(f'{code} {msg}')

    def warn(code, msg):
        warns.append(f'{code} {msg}')

    for k, p in files.items():
        if not p:
            fail('R', f'missing main file: {k}')
    texts = {k: read(p) for k, p in files.items() if p}

    # V: version in the title line
    for k in ('compact', 'full', 'readme'):
        if k in texts:
            first = texts[k].lstrip().splitlines()[0]
            if f'v{version}' not in first:
                fail('V', f'{os.path.basename(files[k])}: title line does not name v{version}: {first[:80]}')
    if 'paste' in texts and f'v{version}' not in texts['paste']:
        fail('V', f'USIP_PASTE.md never names v{version}')

    # S: stale links to older compact/full files
    for k, t in texts.items():
        for n, line in enumerate(t.splitlines(), 1):
            if 'ما الجديد' in line or 'what changed' in line.lower() or 'سجل التغييرات' in line:
                continue
            for m in re.finditer(r'USIP_PORTABLE(?:_FULL)?_v(\d+_\d+)\.md', line):
                if m.group(1) != vtag:
                    fail('S', f'{os.path.basename(files[k])}:{n} points at an older file {m.group(0)}')

    # T: table of contents in the FULL file
    if 'full' in texts:
        t = texts['full']
        heads = {gh_anchor(h) for h in re.findall(r'^#{1,6} (.+)$', t, re.M)}
        for label, anchor in re.findall(r'^- \[([^\]]+)\]\(#([^)]+)\)', t, re.M):
            if anchor not in heads:
                fail('T', f'contents entry "{label}" -> #{anchor} has no heading')

    # C: numbered lists run 1..N
    def numbering(name, block):
        nums = [int(x.translate(ARABIC_DIGITS)) for x in re.findall(r'^(\d+)\. ', block, re.M)]
        if nums and nums != list(range(1, len(nums) + 1)):
            fail('C', f'{name}: numbering {nums} is not 1..{len(nums)}')

    if 'full' in texts:
        card = texts['full'].split('البطاقة المرجعية السريعة')[-1]
        numbering('FULL quick card', card.split('\n---')[0])
    if 'paste' in texts:
        steps = texts['paste'].split('ما ستفعله بالضبط')[-1].split('قواعد لا تُكسر')[0]
        numbering('PASTE steps', steps)
        subs = re.findall(r'^(\d+)([أبجد])\. ', steps, re.M)
        letters = {}
        for num, letter in subs:
            letters.setdefault(num, []).append(letter)
        for num, ls in letters.items():
            if ls != list('أبجد'[:len(ls)]):
                fail('C', f'PASTE sub-steps {num}{ls} are not in order')
        if 'readme' in texts:
            for ref in re.findall(r'البند (\d+[أبجد])', texts['readme']):
                if not re.search(r'^' + re.escape(ref) + r'\. ', steps, re.M):
                    fail('R', f'README names step {ref} but USIP_PASTE.md has no such step')

    # A: annex range and routing
    named = set()
    for t in texts.values():
        named |= {int(x) for x in re.findall(r'\bA(\d{1,2})\b', t)}
    files_annex = {int(m) for m in (re.findall(r'^A(\d+)-', os.path.basename(p))[0]
                   for p in glob.glob(os.path.join(rel, 'A*-*.md')))}
    top = max(named | files_annex) if (named or files_annex) else 0
    for k, t in texts.items():
        current = '\n'.join(l for l in t.splitlines() if 'ما الجديد' not in l)
        for m in re.finditer(r'A1\s*(?:…|\.\.\.|–|-)\s*A(\d+)', current):
            if int(m.group(1)) < top:
                fail('A', f'{os.path.basename(files[k])}: range {m.group(0)} stops before A{top}')
    if 'compact' in texts:
        for a in sorted(files_annex):
            if not re.search(rf'\bA{a}\b', texts['compact']):
                fail('A', f'annex A{a} has a file but the compact file never routes to it')

    # R: README lists every main file and every listed file exists
    if 'readme' in texts:
        table = '\n'.join(l for l in texts['readme'].splitlines() if l.startswith('|'))
        listed = set(re.findall(r'^\| `([\w./-]+\.(?:md|py|sh|js|json))`', table, re.M))
        for name in listed:
            if '/' not in name or name.startswith('scripts/'):
                if not os.path.exists(os.path.join(rel, name)):
                    fail('R', f'README lists {name} but it is not in the folder')
        for p in glob.glob(os.path.join(rel, '*.md')) + glob.glob(os.path.join(rel, 'scripts', '*')):
            relname = os.path.relpath(p, rel)
            if relname != 'README.md' and relname not in listed:
                warn('R', f'{relname} is in the folder but not listed in README')

    # P: project-folder paths exist
    if project_root:
        seen = set()
        for k, t in texts.items():
            for pth in re.findall(r'`((?:living-site|protocol|daily-report|infinite-matrices)/[^`\s]+)`', t):
                pth = pth.rstrip('.,،)')
                if pth in seen or '<' in pth or '*' in pth:
                    continue
                seen.add(pth)
                if not os.path.exists(os.path.join(project_root, pth)):
                    fail('P', f'{os.path.basename(files[k])} names {pth}, which is not in the project folder')

    # Z: size of the compact file
    if files['compact']:
        kb = os.path.getsize(files['compact']) / 1024
        if kb > 40:
            fail('Z', f'compact file is {kb:.1f} KB (limit 40 KB)')
        elif kb > 36:
            warn('Z', f'compact file is {kb:.1f} KB, close to the 40 KB limit')

    return {'release': rel, 'version': version, 'pass': not fails, 'fails': fails, 'warnings': warns,
            'files': {k: os.path.basename(v) if v else None for k, v in files.items()}}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('release')
    p.add_argument('--version', required=True, help='e.g. 5.10')
    p.add_argument('--project-root')
    p.add_argument('--json', action='store_true')
    ns = p.parse_args(argv)
    if not os.path.isdir(ns.release):
        sys.exit(f'not a folder: {ns.release}')
    r = lint(ns.release, ns.version, ns.project_root)
    if ns.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        for f in r['fails']:
            print('FAIL ' + f)
        for w in r['warnings']:
            print('warn ' + w)
        print('PASS' if r['pass'] else f"FAIL ({len(r['fails'])})")
    return 0 if r['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
