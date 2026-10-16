# إثبات الكتابة واللغة العربية / Writing and Arabic-language proofs

Real runs, in a Claude Code cloud container on 2026-10-16, of the two writing scripts (`scripts/tell_scan.py`, `scripts/anchor_gate.py`) and of the Arabic language-processing stack. Open this when you need to know what the writing and Arabic powers (WRITE, PROMPT-02, ARL) can really do, or to re-run the checks on a new machine.

Every sample and pair in this folder is original text written for these tests (no upstream or Wikipedia examples).

## Re-run (from the skill folder)

```bash
python3 -I proofs/general-writing/test_writing.py        # 58 checks, exit 0 when all pass (stdlib only)
python3 -I proofs/general-writing/arabic_probe.py        # PASS / SKIP / FAIL per Arabic capability on this machine
```

`arabic_probe.py` imports optional libraries only if present. To test them all, use a throwaway venv:
`python3 -m venv /tmp/arl && /tmp/arl/bin/pip install pillow arabic-reshaper python-bidi pyarabic && /tmp/arl/bin/pip install --no-deps camel-tools emoji`, then run the probe with `/tmp/arl/bin/python -I`.
OCR needs `apt-get install -y tesseract-ocr tesseract-ocr-ara` (root).

## Results on 2026-10-16

| Check | Result |
|---|---|
| `test_writing.py` (23 scans, 10 file pairs, 18 probes, 6 CLI exit codes, 1 display check) | **58/58 pass**, exit 0 |
| `arabic_probe.py`, system Python 3.13.16 | 7 pass, 3 skip (reshaper, camel-tools, pyarabic not installed), 0 fail |
| `arabic_probe.py`, venv with the optional libraries | **10 pass**, 0 skip, 0 fail |
| Café rewrite (English, worked example in `references/humanizer.md`) | scan EDIT (23 hits) → CLEAN; anchor gate PASS with 15 anchors kept |
| Arabic OCR (tesseract 5.3.4, `ara`) | words read correctly; digits misread; anchor gate flags every misread number |

## What the folder holds

| Path | Purpose |
|---|---|
| `samples/en_ai.txt`, `en_human.txt` | the same caption-tool content written with and without tells |
| `samples/ar_msa_ai.txt`, `ar_msa_human.txt`, `ar_eg_ai.txt`, `ar_eg_human.txt` | the same content in MSA and Egyptian, with and without tells |
| `samples/artifacts.txt` | tool leftovers: `[Your Name]`, `[cite: 3]`, `utm_source=chatgpt.com`, `[اسم الشركة]` |
| `samples/neutral.txt` | one dash and one "crucial" in a human sentence (must not be EDIT) |
| `samples/markdown_code.md` | tells hidden inside code, a URL and a blockquote (must be CLEAN by default) |
| `samples/email_signoff.txt`, `ar_letter.txt` | human letters with "Let me know if" / "يسعدني، لا تتردد" (must not be EDIT) |
| `samples/ar_short.txt` | short Arabic sentences "نعم. لا. ربما." (must not trigger the English fragment rule) |
| `samples/title_case.md` | three Title Case headings |
| `samples/ar_typography.txt` | Latin comma and question mark in Arabic, two digit systems, decorative tatweel (weak only: LEAVE) |
| `pairs/cafe_*` | English before / good rewrite / drifted rewrite, plus `cafe_keep.txt` names |
| `pairs/en_*`, `pairs/ar_*` | anchor pairs (versions, dates, money, percent, email, URL; Arabic-Indic digits) |
| `pairs/ar_quote_*` | direct quote, weekday, Hijri month, clitic numbers, currency abbreviation |
| `pairs/ar9_*` | the three Arabic before/after examples from the humanizer reference (تمّ passive, connector chain, wire-copy rider) |
| `pairs/prompt_*` | an Egyptian-Arabic reel request and two "optimized" versions (for `--mode prompt`) |

## Run log (verbatim excerpts)

```text
$ python3 -I proofs/general-writing/test_writing.py
PASS  scan samples/en_ai.txt                     verdict EDIT (want EDIT) families ['H1', 'H12', 'H13', 'H15', 'H16', 'H17', 'H18', 'H2', 'H22', 'H22b', 'H4', 'H7', 'H8']
PASS  scan samples/en_human.txt                  verdict CLEAN (want CLEAN) families []
PASS  scan samples/ar_msa_ai.txt                 verdict EDIT (want EDIT) families ['AR1', 'AR11', 'AR12', 'AR13', 'AR17', 'AR18', 'AR2', 'AR4', 'AR7']
PASS  scan samples/ar_msa_human.txt              verdict CLEAN (want CLEAN) families []
PASS  scan samples/ar_eg_ai.txt                  verdict EDIT (want EDIT) families ['AR1', 'AR13', 'AR16', 'AR2', 'AR22b', 'AR4', 'H19', 'H19b', 'H20']
PASS  scan samples/ar_eg_human.txt               verdict CLEAN (want CLEAN) families []
PASS  scan samples/artifacts.txt                 verdict EDIT (want EDIT) families ['X1']
PASS  scan samples/neutral.txt                   verdict LOOK (want LOOK) families ['H12', 'H8']
PASS  scan samples/markdown_code.md              verdict CLEAN (want CLEAN) families []
PASS  scan samples/markdown_code.md +code+quotes verdict REVIEW (want REVIEW) families ['H12', 'H13', 'H16', 'H8', 'H8+']
PASS  scan samples/email_signoff.txt             verdict LOOK (want LOOK) families ['H22b']
PASS  scan samples/ar_letter.txt                 verdict LOOK (want LOOK) families ['AR22b']
PASS  scan samples/ar_short.txt                  verdict CLEAN (want CLEAN) families []
PASS  scan samples/title_case.md                 verdict LOOK (want LOOK) families ['H20+', 'H20t']
PASS  scan samples/ar_typography.txt             verdict LEAVE (want LEAVE) families ['AR26', 'AR26d', 'AR26t']
PASS  scan pairs/cafe_before.txt                 verdict EDIT (want EDIT) families ['H1', 'H12', 'H13', 'H15', 'H16', 'H17', 'H18', 'H19', 'H19b', 'H2', 'H22', 'H22b', 'H7', 'H8']
PASS  scan pairs/cafe_after.txt                  verdict CLEAN (want CLEAN) families []
PASS  scan pairs/ar9_3_before.txt                verdict LOOK (want LOOK) families ['AR11']
PASS  scan pairs/ar9_3_after.txt                 verdict CLEAN (want CLEAN) families []
PASS  scan pairs/ar9_5_before.txt                verdict REVIEW (want REVIEW) families ['AR7']
PASS  scan pairs/ar9_5_after.txt                 verdict CLEAN (want CLEAN) families []
PASS  scan pairs/ar9_7_before.txt                verdict REVIEW (want REVIEW) families ['AR13', 'AR15']
PASS  scan pairs/ar9_7_after.txt                 verdict CLEAN (want CLEAN) families []
PASS  scan shows original Arabic spelling        AR12 hit displayed as تُعزّز (normalized match, original spelling)
PASS  gate en_before -> en_after_good            PASS (rewrite) kept 10 dropped []
PASS  gate en_before -> en_after_drift           REVIEW_REQUIRED (rewrite) kept 4 dropped [('email', 'sales@example.com'), ('number', '12'), ('number', '1200000'), ('number', '3'), ('number', '37.5%'), ('version', 'v2.4.1')]
PASS  gate ar_before -> ar_after_good            PASS (rewrite) kept 5 dropped []
PASS  gate ar_before -> ar_after_drift           REVIEW_REQUIRED (rewrite) kept 2 dropped [('email', 'info@kosif.example'), ('number', '1500000'), ('number', '25%')]
PASS  gate cafe_before -> cafe_after             PASS (rewrite) kept 15 dropped []
PASS  gate cafe_before -> cafe_after_drift       REVIEW_REQUIRED (rewrite) kept 7 dropped [('keep', 'Shagaret El Dor'), ('keep', 'Yemen'), ('number', '12'), ('number', '2019'), ('number', '24'), ('number', '45'), ('ratio', '18:00'), ('weekday', 'friday')]
PASS  gate ar_quote_before -> ar_quote_after_good PASS (rewrite) kept 8 dropped []
PASS  gate ar_quote_before -> ar_quote_after_bad REVIEW_REQUIRED (rewrite) kept 4 dropped [('currency', 'ج.م'), ('number', '2024'), ('number', '5'), ('quote', 'لن نرفع الأسعار قبل رمضان')]
PASS  gate prompt_raw -> prompt_good             PASS (prompt) kept 5 dropped []
PASS  gate prompt_raw -> prompt_bad              REVIEW_REQUIRED (prompt) kept 1 dropped [('handle', '@kosif'), ('number', '30'), ('path', 'src/brand/logo.svg'), ('url', 'https://example.com/brief')]
PASS  probe [Write to a@b.com.]                  PASS - [] + []
PASS  probe [في عام ٢٠٢٤م]                       PASS - [] + []
PASS  probe [افتتحنا ٣ فروع و٥ مكاتب ]           REVIEW_REQUIRED - [('number', '2024'), ('number', '5')] + [('number', '2025'), ('number', '9')]
PASS  probe [1,500,000 ريال]                     PASS - [] + []
PASS  probe [قابلنا أحمد يوم الخميس]             REVIEW_REQUIRED - [('keep', 'أحمد'), ('weekday', 'خميس')] + [('weekday', 'جمعة')]
PASS  probe [costs $40]                          REVIEW_REQUIRED - [('currency', '$')] + [('currency', '€')]
PASS  probe [يمارس الرياضة في مارس]              REVIEW_REQUIRED - [('month', 'مارس')] + [('month', 'أبريل')]
PASS  probe [قال: «لن نتراجع أبدًا»]             REVIEW_REQUIRED - [('quote', 'لن نتراجع أبدا')] + []
PASS  probe [ارتفعت بنسبة ٪١٥]                   PASS - [] + []
PASS  probe [hired twelve engineers]             REVIEW_REQUIRED - [('numword', 'twelve')] + [('numword', 'twenty')]
PASS  probe [You may need one of thes]           PASS - [] + []
PASS  probe [‏ارتفعت ‎١١‏ مارس]                  PASS - [] + []
PASS  probe [المبلغ ٥٠٠ ر.س]                     REVIEW_REQUIRED - [('currency', 'ر.س')] + [('currency', 'ج.م')]
PASS  probe [وصلنا ٣ دراهم]                      PASS - [] + []
PASS  probe [سلم علي على أحمد]                   REVIEW_REQUIRED - [('keep', 'علي')] + []
PASS  probe [closed on Fridays]                  PASS - [] + []
PASS  probe [see src/app/main.py and ]           REVIEW_REQUIRED - [('handle', '@kosif'), ('path', 'src/app/main.py'), ('ratio', '9:16')] + [('path', 'main.py'), ('ratio', '16:9')]
PASS  probe يمارس is not the month مارس          [{'kind': 'month', 'value': 'مارس', 'count': 1}]
PASS  cli gate PASS exits 0                      exit 0 (want 0)
PASS  cli gate REVIEW exits 2                    exit 2 (want 2)
PASS  cli gate usage error exits 64              exit 64 (want 64)
PASS  cli scan --fail-on review (EDIT) exits 1   exit 1 (want 1)
PASS  cli scan --fail-on look (CLEAN) exits 0    exit 0 (want 0)
PASS  cli scan --list-rules exits 0              exit 0 (want 0)

58/58 checks passed
```

```text
$ python3 -I scripts/tell_scan.py proofs/general-writing/pairs/cafe_before.txt
verdict: EDIT | words 136 | sentences 13 | mean len 10.5 sd 7.2 | tells/100w 16.9
  [strong] H1     L1   not X but Y: isn't just a coffee shop — it's
  [strong] H2     L10  closer / dramatic fragment: No reservations. No compromises.
  [strong] H22    L12  chatbot residue: I hope this helps
  [normal] H12    L1   overused AI word: meticulously
  ... (17 more normal and weak hits: H12 H13 H15 H16 H17 H18 H19 H22b H7 H8 H19b)
$ python3 -I scripts/tell_scan.py proofs/general-writing/pairs/cafe_after.txt
verdict: CLEAN | words 69 | sentences 6 | mean len 11.5 sd 5.0 | tells/100w 0.0
$ python3 -I scripts/anchor_gate.py --before pairs/cafe_before.txt --after pairs/cafe_after.txt --keep pairs/cafe_keep.txt --text
PASS (rewrite) | kept 15 | dropped - | added -
$ python3 -I scripts/anchor_gate.py --before pairs/cafe_before.txt --after pairs/cafe_after_drift.txt --keep pairs/cafe_keep.txt --text
REVIEW_REQUIRED (rewrite) | kept 7 | dropped keep:Shagaret El Dor, keep:Yemen, number:12, number:2019, number:24, number:45, ratio:18:00, weekday:friday | added number:2018, number:30, number:50
$ python3 -I scripts/anchor_gate.py --before pairs/prompt_raw.txt --after pairs/prompt_good.txt --mode prompt --text
PASS (prompt) | kept 5 | dropped - | added number:1080, number:1920, number:3 x3, number:30 x2, number:4
$ python3 -I scripts/tell_scan.py proofs/general-writing/samples/markdown_code.md --include-code --include-quotes
verdict: REVIEW | words 56 | sentences 6 | mean len 9.3 sd 2.7 | tells/100w 14.3
  [normal] H8+    L0   dash density: 4 dashes in 56 words
  [normal] H12    L11  overused AI word: pivotal
  [normal] H13    L11  inflated significance: pivotal moment
  [normal] H16    L11  sales language: groundbreaking
```

In prompt mode the gate lists additions without failing: `1080`, `1920`, `3 x3` and the extra `30`s are the frame size, scene count and fps the optimized brief added. Each must be a stated assumption or come from the user.

```text
$ <venv>/bin/python -I proofs/general-writing/arabic_probe.py
python 3.13.16 at <scratch venv>/bin/python
PASS  normalize for matching             "ختامًا إلى مُستشفى المدينةِ" -> "ختاما الي مستشفي المدينه" (equals the bare spelling)
PASS  report in original spelling        matched on normalized text, shown as ['وفي الختامِ', 'تُعزّز']
PASS  numbers glued to clitics           و٥ / بـ١٠٠ / ٢٠٢٤م / ٪١٥ -> ['100', '15%', '2024', '5']
PASS  Pillow RAQM shaping                Pillow RAQM on; Amiri shaped "سلام" width 82px from raw logical text
PASS  arabic-reshaper + python-bidi      reshape -> ['0xfeb3', '0xfefc', '0xfee1', '0x20'], visual order "2024 ﻡﻼﺳ" (only for renderers that do not shape)
PASS  camel-tools utils (no models)      ar2bw "muHama~dN yaqora>u Alquro|na" (round trip exact); dediac "محمد يقرأ القرآن"; alef "احمد ابراهيم"
PASS  pyarabic (GPL)                     strip_tashkeel "محمد", strip_tatweel "عربي", tokenize ['قال', ':«', 'لن', 'نتراجع', '»،', 'ثم', 'مضى', '.']
PASS  mojibake repair                    "Ø³Ù„Ø§Ù… Ø¹Ù„ÙŠÙƒÙ…" -> "سلام عليكم"; cp1256 bytes d3e1c7e3 -> "سلام"
PASS  Arabic fonts                       bundled (OFL): Amiri-Bold.ttf, Amiri-Regular.ttf, ArefRuqaa-Regular.ttf, Cairo[slnt,wght].ttf, Lalezar-Regular.ttf, ReemKufi[wght].ttf, Tajawal-Bold.ttf; system families covering Arabic (fc-list :lang=ar): DejaVu Sans, DejaVu Sans Mono, FreeMono, FreeSerif, Unifont, Unifont Sample, Unifont\-JP
PASS  tesseract Arabic OCR               OCR "ارتفعت المبيعات بنسبة 10 في عام ع١‏ | وتواصل معنا يوم الخميس ‎١١‏ مارس"; words read; anchor gate REVIEW_REQUIRED dropped [('number', '12'), ('number', '2024'), ('number', '25%')]

10 pass, 0 skip, 0 fail
```

Installs used for that venv (all wheels, under a minute): `pip install pillow arabic-reshaper python-bidi pyarabic emoji` and `pip install --no-deps camel-tools`. A plain `pip install camel-tools` also pulls `transformers` and `torch`; the character utilities above work without them. The `emoji` package is needed because `camel_tools.utils.charsets` imports it.

### OCR detail (manual run, same day)

Test image: two lines rendered with Pillow + RAQM at 56 px, black on white, 1400×260, fonts from `proofs/_shared/fonts`. Command: `tesseract img.png out -l ara --psm 6` (psm 3, 4 and 6 gave identical text).

| Image | Truth | OCR output |
|---|---|---|
| Amiri, Arabic-Indic digits | `…بنسبة ٢٥٪ في عام ٢٠٢٤` / `…يوم الخميس ١٢ مارس` | `…بنسبة ه5./ في عام ٠١74` / `…يوم اميس ١١ مارس` |
| Cairo, Arabic-Indic digits | same | `…بنسبة 10 في عام ع١` / `…يوم الخميس ١١ مارس` |
| Amiri, Western digits | `…بنسبة 25% في عام 2024` / `…يوم الخميس 12 مارس` | `…بنسبة 9625 في عام 2024` and the **second line was missing** |
| Amiri, Arabic-Indic, upscaled ×2 | same | still wrong digits (`ه9./:`, `174١م`) |

Lessons: Arabic words come back well (Cairo better than Amiri, whose الخ ligature became `اميس`); digits and `%` are not trustworthy; a whole line can vanish; the output carries invisible LRM/RLM marks (`anchor_gate.py` strips them). Always diff OCR numbers against a second source, and look at the image.

## Bugs fixed while porting the prototypes

The 2026-10-16 humanizer distillation shipped prototypes of both scripts. These defects were found and fixed here; each has a regression check above.

| Script | Defect | Fix |
|---|---|---|
| anchor_gate | Arabic prefix percent `٪١٥` vs `15%` gave a false REVIEW (also in the owner's older `writing_fact_gate.py`) | percent accepted before or after the number, folded to a suffix |
| anchor_gate | `--keep` counted substrings, so `علي` matched inside `عليها`; terms with tashkeel or Arabic digits never matched | whole-word match with optional proclitic; terms normalized like the text; names counted by presence |
| anchor_gate | English months matched case-insensitively, so the modal "may" was a month; "one" (pronoun) was a number word | case-sensitive months with a "May I/we/you…" guard; "one" and ordinals skipped |
| anchor_gate | invisible bidi marks from OCR or copy-paste split numbers | LRM, RLM, ALM, isolates and BOM removed before matching |
| anchor_gate | no file paths, @handles or ratios (`9:16`), so it could not guard a prompt rewrite | new anchor kinds plus `--mode prompt` (drops fail, additions listed) |
| anchor_gate | currency abbreviations (`ر.س`, `ج.م`) and plural names (`دراهم`) unseen; `Fridays` ≠ `Friday` | added and folded |
| anchor_gate | usage errors exited 2, the same code as REVIEW | usage errors exit 64 |
| tell_scan | Arabic matches were printed in normalized spelling (رحله) | char-level offset map; matches shown in the writer's spelling, with their tashkeel |
| tell_scan | dashes and phrases inside code, URLs, blockquotes and quotations were counted | masked by default (`--include-code`, `--include-quotes` to scan them) |
| tell_scan | the fragment rule used `\w`, so short Arabic sentences (نعم. لا. ربما.) were a strong tell | fragment rule limited to Latin text; plus "No X. No Y." anaphora |
| tell_scan | "It's not just X — it's Y" (dash form) and curly apostrophes were missed | dash form added; straight or curly apostrophes |
| tell_scan | letter sign-offs ("Let me know if", "يسعدني", "لا تتردد", "تحت أمرك") were strong chatbot tells | moved to normal (H22b, AR22b); "predates chatbots" rule |
| tell_scan | any bold counted as a normal tell; emoji counted twice | bold labels on list items normal, other bold weak; weak hit dropped when its stronger sibling covers it |
| tell_scan | no Title Case, mixed-digit or tatweel checks | H20t/H20+, AR26d, AR26t; plus AR6 stock pairs and the حيث glue |

## Honest limits

- Both scripts match surface patterns. A fluent text without stock phrases scans CLEAN; a human news report in MSA scans like "AI". The scanner tells you where to look, never who wrote the text.
- Sentence-length spread is not a human signal on short texts (`ar_eg_human` is human with sd 0.8).
- PASS from the anchor gate means the anchors survived, not the meaning. A reversed claim with the same numbers passes.
- Nothing here was checked against a real Arabic corpus; the Arabic lists come from the method in `references/humanizer.md` §9 and these samples.
