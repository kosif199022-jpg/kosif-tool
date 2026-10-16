#!/usr/bin/env python3
"""Regression checks for scripts/tell_scan.py and scripts/anchor_gate.py (stdlib only).

Run from anywhere:  python3 -I proofs/general-writing/test_writing.py      (exit 0 = every case passed)
Every sample and pair in this folder is original text written for these tests.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / 'scripts'
sys.dont_write_bytecode = True          # leave no __pycache__ inside the skill
sys.path.insert(0, str(SCRIPTS))
import anchor_gate  # noqa: E402
import tell_scan    # noqa: E402

# file, expected verdict, families that must appear, families that must NOT appear, scan options
SCAN = [
    ('samples/en_ai.txt', 'EDIT', {'H1', 'H2', 'H4', 'H22'}, set(), {}),
    ('samples/en_human.txt', 'CLEAN', set(), set(), {}),
    ('samples/ar_msa_ai.txt', 'EDIT', {'AR1', 'AR2', 'AR4', 'AR13'}, set(), {}),
    ('samples/ar_msa_human.txt', 'CLEAN', set(), set(), {}),
    ('samples/ar_eg_ai.txt', 'EDIT', {'AR1', 'AR2', 'AR4', 'H19'}, set(), {}),
    ('samples/ar_eg_human.txt', 'CLEAN', set(), set(), {}),
    ('samples/artifacts.txt', 'EDIT', {'X1'}, set(), {}),
    ('samples/neutral.txt', 'LOOK', {'H12'}, set(), {}),
    ('samples/markdown_code.md', 'CLEAN', set(), {'H8', 'H13'}, {}),
    ('samples/markdown_code.md', 'REVIEW', {'H8', 'H13', 'H16'}, set(), {'include_code': True, 'include_quotes': True}),
    ('samples/email_signoff.txt', 'LOOK', {'H22b'}, {'H22'}, {}),
    ('samples/ar_letter.txt', 'LOOK', {'AR22b'}, {'AR22'}, {}),
    ('samples/ar_short.txt', 'CLEAN', set(), {'H2'}, {}),
    ('samples/title_case.md', 'LOOK', {'H20+'}, set(), {}),
    ('samples/ar_typography.txt', 'LEAVE', {'AR26', 'AR26d', 'AR26t'}, set(), {}),
    ('pairs/cafe_before.txt', 'EDIT', {'H1', 'H2', 'H16', 'H22'}, set(), {}),
    ('pairs/cafe_after.txt', 'CLEAN', set(), set(), {}),
    ('pairs/ar9_3_before.txt', 'LOOK', {'AR11'}, set(), {}),
    ('pairs/ar9_3_after.txt', 'CLEAN', set(), set(), {}),
    ('pairs/ar9_5_before.txt', 'REVIEW', {'AR7'}, set(), {}),
    ('pairs/ar9_5_after.txt', 'CLEAN', set(), set(), {}),
    ('pairs/ar9_7_before.txt', 'REVIEW', {'AR13', 'AR15'}, set(), {}),
    ('pairs/ar9_7_after.txt', 'CLEAN', set(), set(), {}),
]

# before, after, keep file, mode, expected status, anchors that must be reported as dropped
GATE_FILES = [
    ('pairs/en_before.txt', 'pairs/en_after_good.txt', None, 'rewrite', 'PASS', []),
    ('pairs/en_before.txt', 'pairs/en_after_drift.txt', None, 'rewrite', 'REVIEW_REQUIRED', [('email', 'sales@example.com'), ('version', 'v2.4.1')]),
    ('pairs/ar_before.txt', 'pairs/ar_after_good.txt', None, 'rewrite', 'PASS', []),
    ('pairs/ar_before.txt', 'pairs/ar_after_drift.txt', None, 'rewrite', 'REVIEW_REQUIRED', [('email', 'info@kosif.example'), ('number', '25%')]),
    ('pairs/cafe_before.txt', 'pairs/cafe_after.txt', 'pairs/cafe_keep.txt', 'rewrite', 'PASS', []),
    ('pairs/cafe_before.txt', 'pairs/cafe_after_drift.txt', 'pairs/cafe_keep.txt', 'rewrite', 'REVIEW_REQUIRED', [('keep', 'Yemen'), ('number', '24')]),
    ('pairs/ar_quote_before.txt', 'pairs/ar_quote_after_good.txt', None, 'rewrite', 'PASS', []),
    ('pairs/ar_quote_before.txt', 'pairs/ar_quote_after_bad.txt', None, 'rewrite', 'REVIEW_REQUIRED', [('quote', 'لن نرفع الأسعار قبل رمضان'), ('currency', 'ج.م')]),
    ('pairs/prompt_raw.txt', 'pairs/prompt_good.txt', None, 'prompt', 'PASS', []),
    ('pairs/prompt_raw.txt', 'pairs/prompt_bad.txt', None, 'prompt', 'REVIEW_REQUIRED', [('handle', '@kosif'), ('path', 'src/brand/logo.svg'), ('number', '30')]),
]

# inline probes: the first eight repeat the original regression probes; the rest cover bugs fixed later
GATE_INLINE = [
    ('Write to a@b.com.', 'Write to a@b.com', [], 'PASS'),
    ('في عام ٢٠٢٤م', 'في عام 2024', [], 'PASS'),
    ('افتتحنا ٣ فروع و٥ مكاتب سنة ٢٠٢٤م', 'افتتحنا ٣ فروع و٩ مكاتب سنة ٢٠٢٥م', [], 'REVIEW_REQUIRED'),
    ('1,500,000 ريال', '1500000 ريال', [], 'PASS'),
    ('قابلنا أحمد يوم الخميس', 'قابلنا محمود يوم الجمعة', ['أحمد'], 'REVIEW_REQUIRED'),
    ('costs $40', 'costs €40', [], 'REVIEW_REQUIRED'),
    ('يمارس الرياضة في مارس', 'يمارس الرياضة في أبريل', [], 'REVIEW_REQUIRED'),
    ('قال: «لن نتراجع أبدًا»', 'قال إنهم لن يتراجعوا', [], 'REVIEW_REQUIRED'),
    ('ارتفعت بنسبة ٪١٥', 'ارتفعت بنسبة 15%', [], 'PASS'),                       # prefix percent
    ('hired twelve engineers', 'hired twenty engineers', [], 'REVIEW_REQUIRED'),  # spelled-out numbers
    ('You may need one of these in May 2025.', 'You might need these in May 2025.', [], 'PASS'),  # modal "may", pronoun "one"
    ('‏ارتفعت ‎١١‏ مارس', 'ارتفعت 11 مارس', [], 'PASS'),          # invisible bidi marks from OCR
    ('المبلغ ٥٠٠ ر.س', 'المبلغ ٥٠٠ ج.م', [], 'REVIEW_REQUIRED'),                  # currency abbreviations
    ('وصلنا ٣ دراهم', 'وصلنا ٣ درهم', [], 'PASS'),                                # plural currency folded
    ('سلم علي على أحمد', 'سلم على أحمد', ['علي'], 'REVIEW_REQUIRED'),             # whole-word keep term
    ('closed on Fridays', 'closed every Friday', [], 'PASS'),                     # weekday plural
    ('see src/app/main.py and @kosif at 9:16', 'see main.py and kosif at 16:9', [], 'REVIEW_REQUIRED'),
]


def run_cli(args):
    p = subprocess.run([sys.executable, '-I'] + args, capture_output=True, text=True, cwd=str(HERE))
    return p.returncode


def main():
    rows, failed = [], 0

    def record(name, ok, detail):
        nonlocal failed
        failed += 0 if ok else 1
        rows.append(f"{'PASS' if ok else 'FAIL'}  {name:42} {detail}")

    for rel, verdict, must, must_not, opts in SCAN:
        r = tell_scan.scan((HERE / rel).read_text(encoding='utf-8'), **opts)
        fam = set(r['families'])
        ok = r['verdict'] == verdict and must <= fam and not (must_not & fam)
        tag = rel + (' +code+quotes' if opts else '')
        record('scan ' + tag, ok, f"verdict {r['verdict']} (want {verdict}) families {sorted(fam)}")

    for text, verdict, name in (('Say what the thing is. Then list the parts.', 'CLEAN', 'mid-sentence "the thing is" is not a run-up'),
                                ('Here is the thing: nobody asked for it.', 'EDIT', 'sentence-initial run-up is H4'),
                                ('Docs mention `utm_source=chatgpt.com` as an example.', 'CLEAN', 'artifact inside inline code is not flagged'),
                                ('See https://a.example/x?utm_source=chatgpt.com today.', 'EDIT', 'tracking leftover inside a URL is X1')):
        r = tell_scan.scan(text)
        record('scan inline: ' + name, r['verdict'] == verdict, f"verdict {r['verdict']} (want {verdict}) {r['families']}")

    r = tell_scan.scan((HERE / 'samples/ar_msa_ai.txt').read_text(encoding='utf-8'))
    record('scan shows original Arabic spelling', any(h['match'] == 'تُعزّز' for h in r['hits']),
           'AR12 hit displayed as تُعزّز (normalized match, original spelling)')

    for b, a, keep, mode, status, drops in GATE_FILES:
        keep_terms = [ln.strip() for ln in (HERE / keep).read_text(encoding='utf-8').splitlines() if ln.strip()] if keep else []
        r = anchor_gate.compare((HERE / b).read_text(encoding='utf-8'), (HERE / a).read_text(encoding='utf-8'), keep_terms, mode)
        got = {(d['kind'], d['value']) for d in r['dropped']}
        ok = r['status'] == status and set(drops) <= got
        record(f"gate {Path(b).stem} -> {Path(a).stem}", ok, f"{r['status']} ({mode}) kept {r['kept']} dropped {sorted(got)}")

    for b, a, keep, status in GATE_INLINE:
        r = anchor_gate.compare(b, a, keep)
        ok = r['status'] == status
        drops = [(d['kind'], d['value']) for d in r['dropped']]
        adds = [(d['kind'], d['value']) for d in r['added']]
        record(f'probe [{b[:24]}]', ok, f"{r['status']} - {drops} + {adds}")

    r = anchor_gate.compare('يمارس الرياضة في مارس', 'يمارس الرياضة في أبريل')
    record('probe يمارس is not the month مارس', [(d['kind'], d['value']) for d in r['dropped']] == [('month', 'مارس')], str(r['dropped']))

    gate = str(SCRIPTS / 'anchor_gate.py')
    scan = str(SCRIPTS / 'tell_scan.py')
    for args, want, name in (
        ([gate, '--before', 'pairs/en_before.txt', '--after', 'pairs/en_after_good.txt'], 0, 'cli gate PASS exits 0'),
        ([gate, '--before', 'pairs/en_before.txt', '--after', 'pairs/en_after_drift.txt'], 2, 'cli gate REVIEW exits 2'),
        ([gate, '--before', 'missing.txt', '--after', 'pairs/en_after_good.txt'], 64, 'cli gate usage error exits 64'),
        ([scan, 'samples/en_ai.txt', '--fail-on', 'review'], 1, 'cli scan --fail-on review (EDIT) exits 1'),
        ([scan, 'samples/en_human.txt', '--fail-on', 'look'], 0, 'cli scan --fail-on look (CLEAN) exits 0'),
        ([scan, '--list-rules'], 0, 'cli scan --list-rules exits 0'),
    ):
        code = run_cli(args)
        record(name, code == want, f'exit {code} (want {want})')

    print('\n'.join(rows))
    print(f'\n{len(rows) - failed}/{len(rows)} checks passed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
