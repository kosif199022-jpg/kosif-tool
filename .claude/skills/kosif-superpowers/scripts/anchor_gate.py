#!/usr/bin/env python3
"""anchor_gate.py - check that a rewrite kept every factual anchor (English and Arabic).

Anchors compared between BEFORE and AFTER (as multisets, so a lost repeat also counts):
  quote     text inside "…", «…» or “…” (direct speech must not become reported speech)
  email, url, version (v2.4.1), path (src/x.py, logo.svg), handle (@name)
  ratio     9:16, 16:9, 10:30, 00:01:30
  number    Arabic-Indic and Persian digits equal 0-9; 1,500,000 equals 1500000; ٪25 and %25 equal 25%;
            numbers glued to Arabic letters are still seen (و٥ , بـ١٠٠ , ٢٠٢٤م)
  currency  $ € £ ¥ ₹, ISO codes, Arabic names (plural folded) and abbreviations (ر.س ج.م د.إ د.ك ر.ق)
  month     Gregorian (EN and AR, Egyptian and Levantine names) and Hijri
  weekday   EN and AR (أحد only as الأحد)
  numword   spelled-out numbers (EN, MSA, Egyptian); English "one" and ordinals ("first") are skipped
            because they are usually a pronoun or a discourse marker
  keep      every term you list with --keep FILE or --keep-term (names, brands, product codes); counted by
            presence, so naming someone once instead of three times is fine, dropping the name is not
Ambiguous Arabic words are left out on purpose: نص (text/half), ست (six/lady), ضعف (double/weakness).
Invisible bidi marks (LRM, RLM, ALM, isolates) are ignored, so OCR or copy-paste noise does not count.

Modes
  rewrite (default)  PASS only when nothing was dropped AND nothing was added
  prompt             PASS when nothing was dropped; additions are listed for review
                     (use it to check an optimized prompt against the user's raw prompt)
PASS means the anchors survived. It never proves that meaning, tone or attribution survived.

Usage
  python3 anchor_gate.py --before src.txt --after rewrite.txt [--keep names.txt] [--keep-term "Siwa"]
  python3 anchor_gate.py --before-text "costs $40" --after-text "costs €40" --text
  python3 anchor_gate.py --before raw_prompt.txt --after optimized.txt --mode prompt
Exit codes: 0 PASS, 2 REVIEW_REQUIRED, 64 usage error. Stdlib only, read-only, no network, Python 3.8+.
"""
import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

MAX_BYTES = 5 * 1024 * 1024
DIG = str.maketrans('٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹', '01234567890123456789')
HAR = re.compile('[ً-ْٰـ]')                       # tashkeel, dagger alef, tatweel
BIDI = re.compile('[‎‏؜‪-‮⁦-⁩﻿]')  # invisible direction marks, BOM
AL = 'ء-ي'
FOLD = str.maketrans('أإآٱىة', 'اااايه')

QUOTE = re.compile(r'"([^"\n]{3,300})"|«([^»\n]{3,300})»|“([^”\n]{3,300})”')
EMAIL = re.compile(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}(?![A-Za-z0-9-])')
URL = re.compile(r'https?://[^\s<>"\'«»)\]]+', re.I)
VER = re.compile(r'(?<![\w.])v\d+(?:\.\d+){1,4}\b', re.I)
EXT = r'(?:py|js|cjs|mjs|ts|tsx|jsx|json|md|txt|csv|tsv|svg|png|jpe?g|gif|webp|mp4|mov|mp3|wav|html?|css|ya?ml|toml|pdf|docx?|xlsx?|pptx?|sh|srt|ass|vtt|zip)'
PATH = re.compile(r'(?<![\w@/.-])(?:~|\.{1,2})?/?(?:[\w.-]+/)*[\w-][\w.-]*\.' + EXT + r'(?![\w])', re.I)
HANDLE = re.compile(r'(?<![\w.@])@[A-Za-z0-9_][\w.]*[A-Za-z0-9_]|(?<![\w.@])@[A-Za-z0-9_]')
RATIO = re.compile(r'(?<![\d:.,])\d{1,4}:\d{1,4}(?::\d{1,4})?(?![\d:])')
NUM = re.compile(r'(?<![\d.,])(?:[%٪]\s?)?\d+(?:[.,،٫٬]\d+)*(?:\s?[%٪])?(?![\d])')   # Arabic letters may touch it
CUR = re.compile(r'[$€£¥₹]|\b(?:USD|EUR|GBP|SAR|EGP|AED|KWD|QAR|JOD|OMR|BHD|TRY)\b'
                 r'|ر\.س|ج\.م|د\.إ|د\.ك|ر\.ق|ر\.ع|د\.ب|د\.أ'
                 r'|ريال|جنيه|درهم|دراهم|دينار|دنانير|دولار|يورو|ليرة|ليرات')
CUR_FOLD = {'دراهم': 'درهم', 'دنانير': 'دينار', 'ليرات': 'ليرة'}


def ar_words(*words):
    """Arabic whole word with an optional proclitic (و ب ل ف + ال); the bare word is captured as group 'w'."""
    return r'(?<![' + AL + r'])(?:[وبلف]?(?:ال)?)(?P<w>' + '|'.join(words) + r')(?![' + AL + r'])'


EN_WORDS = {
    'month': (r'\b(?:January|February|March|April|June|July|August|September|October|November|December'
              r'|May(?!\s+(?:I|we|you|he|she|it|they|be|not|have|also)\b))\b', 0),
    'weekday': (r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s?\b', 0),
    'numword': (r'\b(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen'
                r'|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion'
                r'|half|quarter|dozen|twice)\b', re.I),
}
AR_LISTS = {
    'month': ('يناير', 'فبراير', 'مارس', 'أبريل', 'ابريل', 'إبريل', 'مايو', 'يونيو', 'يونية', 'يوليو', 'يولية',
                      'أغسطس', 'اغسطس', 'سبتمبر', 'أكتوبر', 'اكتوبر', 'نوفمبر', 'ديسمبر',
                      'كانون', 'شباط', 'آذار', 'نيسان', 'أيار', 'حزيران', 'تموز', 'آب', 'أيلول', 'تشرين',
                      'محرم', 'صفر', 'ربيع', 'جمادى', 'رجب', 'شعبان', 'رمضان', 'شوال', 'القعدة', 'الحجة'),
    'weekday': ('سبت', 'الأحد', 'الاحد', 'اثنين', 'إثنين', 'اتنين', 'تلات', 'ثلاثاء', 'أربعاء', 'اربعاء', 'خميس', 'جمعة'),
    'numword': ('واحد', 'واحدة', 'اثنين', 'اثنان', 'اتنين', 'ثلاث', 'ثلاثة', 'تلات', 'تلاتة', 'أربع', 'أربعة', 'خمس', 'خمسة',
                        'ستة', 'سبعة', 'ثمان', 'ثمانية', 'تمانية', 'تسع', 'تسعة', 'عشر', 'عشرة', 'عشرين', 'عشرون',
                        'مائة', 'مئة', 'مية', 'ألف', 'آلاف', 'مليون', 'ملايين', 'مليار', 'نصف', 'ربع', 'ثلث'),
}
# match on a folded copy (أإآٱ→ا, ى→ي, ة→ه) so informal spellings such as خمسه, الف, الاف count as anchors
AR_WORDS = {k: ar_words(*sorted({w.translate(FOLD) for w in v}, key=len, reverse=True)) for k, v in AR_LISTS.items()}


def clean(text):
    """Matching form: NFKC, no tashkeel/tatweel, no bidi marks, ASCII digits."""
    return BIDI.sub('', HAR.sub('', unicodedata.normalize('NFKC', text))).translate(DIG)


def fold_ar(word):
    w = word.translate(FOLD)
    return w[2:] if w.startswith('ال') and len(w) > 3 else w


def fold_num(t):
    t = t.replace(' ', '').replace('٪', '%').replace('٫', '.').replace('٬', ',').replace('،', ',')
    pct = '%' in t
    core = t.strip('%')
    if re.fullmatch(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?', core):          # 1,500,000 == 1500000
        core = core.replace(',', '')
    return core + ('%' if pct else '')


def keep_regex(term):
    t = re.escape(clean(term))
    return re.compile(r'(?<![^\W_])(?:[وفبلك]|لل|ال)?' + t + r'(?![^\W_])')


SHOWN = {}   # folded Arabic word -> first spelling seen, so reports show the writer's form


def anchors(text, keep=()):
    s = clean(text)
    out = [('quote', next(g for g in m.groups() if g).strip()) for m in QUOTE.finditer(s)]
    for kind, rx in (('email', EMAIL), ('url', URL), ('version', VER), ('path', PATH), ('handle', HANDLE), ('ratio', RATIO)):
        for m in rx.finditer(s):
            out.append((kind, m.group().rstrip('.,;:!?؛،')))
        s = rx.sub(' ', s)
    out += [('number', fold_num(m.group())) for m in NUM.finditer(s)]
    out += [('currency', CUR_FOLD.get(m.group(), m.group().upper())) for m in CUR.finditer(s)]
    for kind, (rx, flags) in EN_WORDS.items():
        out += [(kind, re.sub(r'(day)s$', r'\1', m.group().lower())) for m in re.finditer(rx, s, flags)]   # Fridays == Friday
    sf = s.translate(FOLD)                          # same length as s: FOLD maps one char to one char
    for kind, rx in AR_WORDS.items():
        for m in re.finditer(rx, sf):
            orig = s[m.start('w'):m.end('w')]
            SHOWN.setdefault(fold_ar(orig), orig)
            out.append((kind, fold_ar(orig)))
    for term in keep:                               # names count by presence: mentioning a name once instead of
        if keep_regex(term).search(s):              # three times is not a fact change, losing it entirely is
            out.append(('keep', term))
    return Counter(out)


def compare(before, after, keep=(), mode='rewrite'):
    a, b = anchors(before, keep), anchors(after, keep)
    rows = lambda c: [{'kind': k, 'value': SHOWN.get(v, v), 'count': n} for (k, v), n in sorted(c.items())]
    dropped, added = a - b, b - a
    ok = not dropped and (mode == 'prompt' or not added)
    note = 'Anchor check only. PASS does not prove that meaning, tone or attribution survived.'
    if mode == 'prompt' and added:
        note += ' Prompt mode allows additions; each added anchor must be a stated assumption or come from the user, never an invented fact.'
    return {'status': 'PASS' if ok else 'REVIEW_REQUIRED', 'mode': mode, 'dropped': rows(dropped), 'added': rows(added),
            'kept': sum((a & b).values()), 'note': note}


class Parser(argparse.ArgumentParser):
    def error(self, message):                      # usage errors exit 64 so they never look like REVIEW (2)
        self.print_usage(sys.stderr)
        self.exit(64, f'{self.prog}: error: {message}\n')


def read(path_or_dash):
    if path_or_dash == '-':
        return sys.stdin.read()
    p = Path(path_or_dash)
    if not p.is_file():
        raise ValueError(f'{p}: not a file')
    if p.stat().st_size > MAX_BYTES:
        raise ValueError(f'{p}: larger than 5 MB')
    return p.read_text(encoding='utf-8')


def main(argv=None):
    ap = Parser(prog='anchor_gate.py', description='Compare factual anchors before and after a rewrite (EN + AR). Exit 0 PASS, 2 REVIEW_REQUIRED, 64 usage error.',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog='Examples:\n  python3 anchor_gate.py --before src.txt --after new.txt --keep names.txt\n'
                       '  python3 anchor_gate.py --before-text "قابلنا أحمد يوم الخميس" --after-text "قابلنا محمود يوم الجمعة" --keep-term أحمد --text\n'
                       '  python3 anchor_gate.py --before raw_prompt.txt --after optimized_prompt.txt --mode prompt')
    src = ap.add_argument_group('input (one of each pair)')
    src.add_argument('--before', help="original text file ('-' = stdin)")
    src.add_argument('--after', help='rewritten text file')
    src.add_argument('--before-text', help='original text given inline')
    src.add_argument('--after-text', help='rewritten text given inline')
    ap.add_argument('--keep', help='file with one must-keep term per line (names, brands, codes)')
    ap.add_argument('--keep-term', action='append', default=[], help='a must-keep term; repeat as needed')
    ap.add_argument('--mode', choices=['rewrite', 'prompt'], default='rewrite', help='prompt: additions allowed, drops fail')
    ap.add_argument('--text', action='store_true', help='print a short human summary instead of JSON')
    a = ap.parse_args(argv)
    if (a.before is None) == (a.before_text is None) or (a.after is None) == (a.after_text is None):
        ap.error('give exactly one of --before/--before-text and one of --after/--after-text')
    if a.before == '-' and a.after == '-':
        ap.error('only one side can come from stdin')
    try:
        before = a.before_text if a.before_text is not None else read(a.before)
        after = a.after_text if a.after_text is not None else read(a.after)
        keep = list(a.keep_term)
        if a.keep:
            keep += [ln.strip() for ln in read(a.keep).splitlines() if ln.strip()]
    except (OSError, UnicodeDecodeError, ValueError) as e:
        ap.error(str(e))
    r = compare(before, after, keep, a.mode)
    if a.text:
        fmt = lambda rows: ', '.join(f"{x['kind']}:{x['value']}" + (f" x{x['count']}" if x['count'] > 1 else '') for x in rows) or '-'
        print(f"{r['status']} ({r['mode']}) | kept {r['kept']} | dropped {fmt(r['dropped'])} | added {fmt(r['added'])}")
    else:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r['status'] == 'PASS' else 2


if __name__ == '__main__':
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
