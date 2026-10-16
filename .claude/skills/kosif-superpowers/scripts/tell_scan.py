#!/usr/bin/env python3
"""tell_scan.py - find stock writing habits ("tells") in English and Arabic prose.

An editing aid that shows WHERE to look before a rewrite. It is not an
authorship detector: human journalism, formal and non-native writing trigger
these lists too, so never use the result to judge who wrote a text.

Families
  H1..H25  English, numbered like the pattern catalogue in references/humanizer.md
           (numbering follows blader/humanizer v3.1.0, MIT, (c) 2025 Siqi Chen). Patterns that
           need judgment or the conversation (H6 triads, H10, H11, H14, H24, H26) are manual checks.
  X1       tool artifacts and unfilled templates (oaicite, [cite: 3], utm_source=chatgpt.com, [Your Name]).
  AR1..AR26 Arabic (MSA and Egyptian), each aligned with the nearest English pattern.
Strength
  strong  one sighting justifies an edit     normal  act when it reads badly
  weak    needs company from other families before it means anything
Verdict (strongest first)
  EDIT    any strong tell
  REVIEW  two or more normal families, three or more normal hits, or four or more families
  LOOK    one normal family only
  LEAVE   weak tells only
  CLEAN   nothing found

By default the scanner ignores fenced code, inline code, URLs, blockquote lines and the
inside of quotations, because a quoted or coded phrase is not the writer's own prose
(X1 still reads URLs, where tracking leftovers such as utm_source live).
Arabic is matched on a normalized copy (no tashkeel or tatweel, one alef, ى->ي, ة->ه)
but every match is reported in the writer's original spelling.

Usage
  python3 tell_scan.py FILE [FILE ...]            human report, strongest first ('-' = stdin)
  python3 tell_scan.py FILE --json                machine-readable report
  python3 tell_scan.py FILE --fail-on review      exit 1 when a verdict is REVIEW or EDIT
  python3 tell_scan.py --list-rules               print every rule id, strength and label
Stdlib only, read-only, no network, Python 3.8+.
"""
import argparse
import json
import re
import statistics
import sys
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------- normalization
HARAKAT = re.compile('[ً-ْٰـ]')            # tashkeel, dagger alef, tatweel
FOLD = str.maketrans('أإآٱىة', 'اااايه')
AR_LETTER = 'ء-ي'


def norm_ar(s):
    """Matching form of Arabic text (used for the patterns themselves)."""
    s = HARAKAT.sub('', unicodedata.normalize('NFKC', s))
    return s.translate(FOLD)


def norm_with_map(text):
    """Normalize char by char and keep, for every output char, the index of its source char.
    This lets a match found in the normalized copy be shown in the original spelling."""
    out, idx = [], []
    for i, ch in enumerate(text):
        piece = norm_ar(ch)
        out.append(piece)
        idx.extend([i] * len(piece))
    return ''.join(out), idx


# --------------------------------------------------------------------------- masking
MASKS = [
    re.compile(r'^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?^[ \t]*\1[ \t]*$', re.M | re.S),   # fenced code
    re.compile(r'`[^`\n]+`'),                                                      # inline code
    re.compile(r'(?:https?://|www\.)[^\s<>"\'«»)\]]+', re.I),                      # URLs
    re.compile(r'^[ \t]*>[^\n]*', re.M),                                           # blockquote lines
]
QUOTES = re.compile(r'«[^»\n]{1,400}»|“[^”\n]{1,400}”|"[^"\n]{1,400}"')


def blank(text, rx):
    return rx.sub(lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text)


def blank_inner(text, rx):
    """Blank the inside of each quotation but keep the quote marks themselves."""
    return rx.sub(lambda m: m.group(0)[0] + ' ' * (len(m.group(0)) - 2) + m.group(0)[-1], text)


def mask(text, include_code=False, include_quotes=False, keep_urls=False):
    """Same length as text; masked spans become spaces (newlines kept, so line numbers hold).
    keep_urls leaves URLs visible (used for X1, whose tracking leftovers live inside URLs)."""
    if not include_code:
        for rx in MASKS:
            if keep_urls and rx is MASKS[2]:
                continue
            text = blank(text, rx)
    if not include_quotes:
        text = blank_inner(text, QUOTES)
    return text


# --------------------------------------------------------------------------- rules
# (id, strength, label, pattern). English patterns run case-insensitively on the masked text.
EN = [
    ('H1', 'strong', 'not X but Y',
     r"\b(?:isn'?t|is not|aren'?t|are not|wasn'?t)\s+(?:just|only|merely|simply)\b[^.!?]{1,60}?[,;—–]\s*(?:it'?s|they'?re|it was|but)\b"
     r"|\b(?:it'?s|this is|that'?s)\s+not\s+(?:just|only|merely|simply)?\b[^.;!?]{1,60}?(?:[,;]|\s[—–]|\s--)\s*(?:it'?s|but|rather)\b"
     r"|\bnot\s+(?:just|only|merely)\b[^.;!?]{1,60}?\bbut\b"
     r"|\b(?:does not|doesn't) mean\b[^.]*\.\s+It means\b|,\s*no (?:guessing|fluff|surprises)\b"),
    ('H2', 'strong', 'closer / dramatic fragment',
     r"\b(?:Let that sink in|Read that again|That is the real win|That distinction matters|The message was clear|This shows the importance of|It was a lesson in)\b"
     r"|(?:^|(?<=[.!?])\s)(?:[A-Za-z0-9':]+ ){0,2}[A-Za-z0-9':]+\.\s(?:[A-Za-z0-9':]+ ){0,2}[A-Za-z0-9':]+\.\s(?:[A-Za-z0-9':]+ ){0,2}[A-Za-z0-9':]+\."
     r"|\b[A-Za-z]+\. [A-Za-z]+\. [A-Za-z]+\.(?=\s|$)"
     r"|\b(No|Not|Zero|Never)\s+[A-Za-z']+(?: [A-Za-z']+)?\.\s+\1\s+[A-Za-z']+(?: [A-Za-z']+)?\."),
    ('H3', 'strong', 'saying that sounds deep',
     r"\b(?:the real question is|at its core|what really matters|the heart of the matter|the deeper issue|is the language of|the currency of|the architecture of)\b"),
    ('H4', 'strong', 'staged run-up',
     r"\b(?:Let'?s (?:dive in|dive into|explore|break (?:this|it) down)|here'?s what you need to know|without further ado|Let'?s be honest|Real talk)\b"
     r"|(?:^|(?<=[.!?]\s))(?:Here(?:'?s| is) the thing|The thing is)\b|\b(?:Here(?:'?s| is) the thing|The thing is)\s*[,:]"
     r"|\blet me tell you\b|(?:^|\s)Honestly\?"
     r"|(?:^|(?<=[.!])\s)(?:And |But |So )?(?:the \w+|would I \w+(?: \w+)?|is it \w+(?: \w+)?|why)\?\s+(?:Simply|Absolutely|Yes|No|Definitely|Well)\b"),
    ('H5', 'strong', 'arguing with no one',
     r"\b(?:I'?m not saying|To be clear,|Don'?t get me wrong|This is not to say|A tempting approach would be|One might be tempted to|You might think)\b"),
    ('H8', 'weak', 'dash connector', r"[—–]|\s--\s"),
    ('H9', 'weak', 'stacked qualifiers', r"\b(?:could potentially|might arguably|potentially possibly|it'?s also possible that)\b"),
    ('H12', 'normal', 'overused AI word',
     r"\b(?:delv(?:e|es|ed|ing)|tapestry|testament|pivotal|meticulous(?:ly)?|showcas(?:e|es|ed|ing)|underscor(?:e|es|ed|ing)|intricac(?:y|ies)|intricate"
     r"|interplay|vibrant|garner(?:s|ed)?|bolster(?:s|ed)?|enduring|landscape|crucial|align with|deep dive)\b"),
    ('H13', 'normal', 'inflated significance',
     r"\b(?:stands as a testament|pivotal moment|plays? an? (?:key|crucial|vital|pivotal) role|setting the stage|evolving landscape|indelible mark|continues to thrive"
     r"|future looks bright|exciting times (?:lie )?ahead|step in the right direction|(?:enduring|lasting) legacy)\b"),
    ('H15', 'normal', 'shallow -ing rider',
     r",\s+(?:highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|showcasing)\b"),
    ('H16', 'normal', 'sales language',
     r"\b(?:nestled|in the heart of|breathtaking|must-visit|stunning|renowned|groundbreaking|diverse array|rich cultural heritage|hidden gem|must-see"
     r"|truly special|stole my heart|no trip would be complete|iconic|charming)\b"),
    ('H17', 'normal', 'borrowed authority', r"\b(?:experts (?:argue|believe|say)|observers have (?:cited|noted)|industry reports|some critics)\b"),
    ('H18', 'normal', 'avoiding is/has', r"\b(?:serves as|stands as|functions as|boasts)\b"),
    ('H19', 'normal', 'bold label on a list item', r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]+\*\*[^*\n]{1,60}?(?::\*\*|\*\*[ \t]*:)"),
    ('H19b', 'weak', 'bold in running text', r"\*\*[^*\n]+\*\*"),
    ('H20', 'normal', 'decorated heading or list line', r"^[ \t]*(?:#+[ \t]*|[-*+][ \t]+)?[←-⇿☀-➿\U0001F300-\U0001FAFF]"),
    ('H20b', 'weak', 'decorative emoji', r"[✨⭐\U0001F300-\U0001FAFF]"),
    ('H21', 'weak', 'curly quotes', r"[“”]"),
    ('H22', 'strong', 'chatbot residue',
     r"\b(?:I hope this helps|Great question|Certainly!|Of course!|You'?re absolutely right|Would you like me to|Should I continue\?)"),
    ('H22b', 'normal', 'chat-style sign-off (fine in letters)', r"\b(?:Let me know if|Want me to|Feel free to)\b"),
    ('H23', 'normal', 'knowledge-limit disclaimer',
     r"\b(?:as of my last|up to my last training|based on available information|not publicly available|not widely documented|it is believed that)\b"),
    ('H25', 'weak', 'writing about the document', r"\b(?:the table below (?:compares|shows)|this section (?:is organized|covers)|was added to replace|compiled from)\b"),
]
# X1 runs with URLs left visible, because tracking leftovers sit inside URLs (code and quotes stay masked).
X1 = ('X1', 'strong', 'tool artifact / unfilled template',
      r"contentReference\[oaicite|oai_citation|turn\d+(?:search|news|view)\d+|\[cite: ?\d+\]|\[span_\d+\]\(start_span\)|grok_card"
      r"|utm_source=(?:chatgpt\.com|openai|copilot\.com)|\[(?:Insert|Your|Describe|Add|Company|Name of)\b[^\]\n]{0,60}\]"
      r"|\[(?:اسمك|اسم الشركة|أدخل|ضع)[^\]\n]{0,40}\]")


def W(*words):
    """Arabic whole word(s) with an optional proclitic (و ف ب ل ك + ال, or لل)."""
    return (r"(?<![" + AR_LETTER + r"])(?:[وفبلك]?(?:ال)?|لل)(?:" + "|".join(words) + r")(?![" + AR_LETTER + r"])")


AR = [  # written in plain spelling; compiled after norm_ar, matched on a normalized copy
    ('AR1', 'strong', 'ليس مجرد / لا يقتصر… بل',
     r"(?:ليس|ليست|لم يعد|لم تعد)\s+مجرد|لا (?:يقتصر|تقتصر)\b[^.؟!]{0,80}?\bبل\b|ليس(?:ت)?\s+[^.؟!،]{1,40}?[،,]?\s*(?:بل|وإنما)\s|مش (?:بس|مجرد)\s|الموضوع مش\s"),
    ('AR2', 'strong', 'خاتمة استعراضية',
     r"وفي الختام|ختامًا|خلاصة القول|وهكذا نرى|وبهذا يتضح|و?يبقى السؤال|هل أنت مستعد|وده بالظبط|ودي كانت الحكاية|فكّر فيها|خليها في دماغك|افتكر ده كويس"),
    ('AR3', 'strong', 'حكمة جوفاء',
     r"جوهر (?:الأمر|المسألة)|في حقيقة الأمر|السؤال الحقيقي|ما يهم حقًا|حجر الزاوية|مربط الفرس|بيت القصيد|لغة (?:الثقة|المستقبل|العصر)"),
    ('AR4', 'strong', 'تمهيد مسرحي',
     r"في ظل (?:التطورات|التحديات|التغيرات)|في عالمنا (?:اليوم|المعاصر|المتسارع)|في عصر (?:السرعة|التكنولوجيا|التحول)|مما لا شك فيه|لا يخفى على أحد"
     r"|تجدر الإشارة|من الجدير بالذكر|دعونا نتعرف|دعنا نغوص|هيا بنا|بصراحة\s*[؟?]|خليني أقولك|بص يا|تعالوا نشوف|هل تساءلت يومًا"),
    ('AR5', 'strong', 'جدال مع غائب', r"قد يظن البعض|قد يعتقد البعض|البعض (?:يظن|يعتقد)|لا أقول إن|لا يعني هذا أن|متقولش إن|ممكن تقول"),
    ('AR6', 'normal', 'ثنائيات وثلاثيات جاهزة',
     r"بكفاءة وفاعلية|الأمن والأمان|الأصالة والمعاصرة|الدقة والإتقان|الجهد والعناء|مهم وضروري|سهل وسريع|الابتكار والإبداع"),
    ('AR7', 'normal', 'سلسلة روابط / حيث لاصقة',
     r"علاوة على ذلك|بالإضافة إلى ذلك|فضلًا عن ذلك|من ناحية أخرى|وعلاوة على|ومن هذا المنطلق|في هذا السياق|على صعيد آخر|كما أن"
     r"|،\s*حيث\s+(?:يتيح|تتيح|يمكن|يعمل|تعمل|يقدم|تقدم|يوفر|توفر)"),
    ('AR9', 'weak', 'تحوط متراكم', r"قد يكون من الممكن|ربما يمكن القول|إلى حد ما|نوعًا ما"),
    ('AR11', 'normal', 'تم/قام بـ + مصدر', r"(?<![" + AR_LETTER + r"])[وف]?(?:تمت?\s+\S+|قامت?\s+ب\S+)"),
    ('AR12', 'normal', 'كلمة آلية',
     W('غوص', 'نسيج', 'مشهد', 'رحلة', 'محوري', 'محورية', 'جوهري', 'جوهرية', 'تعزيز', 'يعزز', 'تعزز', 'تمكين', 'سلس', 'سلسة', 'متكامل', 'متكاملة',
       'ديناميكي', 'ديناميكية', 'استكشاف', 'نستكشف', 'الارتقاء', 'بصمة', 'ثري', 'ثرية') + r"|إطلاق العنان|بشكل (?:كبير|فعال|ملحوظ|أساسي)"),
    ('AR13', 'normal', 'تضخيم الأهمية',
     r"نقلة نوعية|قفزة نوعية|دورًا? (?:محوريًا|حيويًا|بارزًا|رئيسيًا|محوري|حيوي|بارز)|يلعب دورًا|بالغ الأهمية|آفاق واعدة|مستقبلًا? مشرقًا?"
     r"|إرث (?:خالد|عريق)|لا تُمحى|غير مسبوق|منقطع النظير|[يت]عكس (?:التزام|حرص)|شاهد على|شهادة على|تحول جذري"),
    ('AR15', 'normal', 'ذيل تفسيري (خبر)',
     r"[،,]\s*(?:مما|ما|الأمر الذي)\s+(?:يعكس|تعكس|يؤكد|تؤكد|يسهم|يساهم|يبرز|يعزز)|في خطوة (?:تهدف|تعكس|تؤكد)|وذلك في إطار|بما يسهم في"),
    ('AR16', 'normal', 'لغة إعلانية', r"يقع في قلب|خلاب|ساحر|آسر|وجهة لا تفوت|تجربة لا تنسى|فريد من نوعه|على الإطلاق|هتنبهر|مش هتصدق"),
    ('AR17', 'normal', 'سلطة مستعارة', r"يرى الخبراء|يؤكد الخبراء|تشير الدراسات|أثبتت الدراسات|وفقًا للخبراء|يرى المراقبون|الخبراء (?:يرون|يؤكدون)"),
    ('AR18', 'normal', 'يُعد/يمثل بدل الجملة الاسمية', W('يعد', 'تعد', 'يعتبر', 'تعتبر', 'يمثل', 'تمثل', 'يشكل', 'تشكل') + r"|بمثابة|يتمثل في"),
    ('AR22', 'strong', 'بقايا الشات',
     r"بالتأكيد!|سؤال رائع|إليك (?:أهم|بعض|ما)|(?:آمل|أتمنى) أن (?:يكون|تكون) (?:هذا |ده |هذه المعلومات )?مفيد|هل تريدني أن|كمساعد ذكي|كنموذج لغوي"),
    ('AR22b', 'normal', 'مجاملة دردشة (طبيعية في الرسائل)', r"بكل سرور|لا تتردد|يسعدني|تحت أمرك|لو حابب|قولي لو|هل تود"),
    ('AR23', 'normal', 'حدود المعرفة', r"حسب آخر (?:تحديث|معلوماتي)|لا تتوفر معلومات|من المرجح أن|يُعتقد أن|وفقًا لمعلوماتي"),
    ('AR25', 'weak', 'كلام عن النص نفسه', r"في هذا المقال|في هذه المقالة|سنتناول|سوف نستعرض|كما هو موضح في الجدول"),
    ('AR26', 'weak', 'ترقيم لاتيني في العربية', r"[" + AR_LETTER + r"][,?;]"),
]
SHADOWED_BY = {'H19b': 'H19', 'H20b': 'H20'}      # drop the weak hit when the stronger one covers it
RANK = {'strong': 0, 'normal': 1, 'weak': 2}
VERDICTS = ['CLEAN', 'LEAVE', 'LOOK', 'REVIEW', 'EDIT']
VERDICT_TEXT = {'LOOK': 'LOOK (one normal tell; fix it if it reads badly)',
                'LEAVE': 'LEAVE (weak tells alone do not justify an edit)'}

_COMPILED = None


def rules():
    global _COMPILED
    if _COMPILED is None:
        _COMPILED = ([(i, s, l, re.compile(p.replace("'?", "['\u2019]?"), re.I | re.M), 'en') for i, s, l, p in EN]   # straight or curly apostrophe
                     + [(X1[0], X1[1], X1[2], re.compile(X1[3], re.I), 'raw')]
                     + [(i, s, l, re.compile(norm_ar(p), re.M), 'ar') for i, s, l, p in AR])
    return _COMPILED


# --------------------------------------------------------------------------- scan
SENT_SPLIT = re.compile(r'(?<=[.!?؟])\s+|\n{2,}')
FIRST_WORD = re.compile(r"[A-Za-z'" + AR_LETTER + r"]+")
AR_DIGIT, EN_DIGIT = re.compile('[٠-٩]'), re.compile('[0-9]')
TITLE_HEADING = re.compile(r'^[ \t]*#{1,6}[ \t]+(.+)$', re.M)


def sentences(text):
    return [x.strip() for x in SENT_SPLIT.split(text) if len(x.split()) >= 2]


def _hit(rid, strength, label, text, start, end):
    return {'id': rid, 'strength': strength, 'label': label, 'line': text.count('\n', 0, start) + 1,
            'start': start, 'end': end, 'match': ' '.join(text[start:end].split())[:60]}


def scan(text, include_code=False, include_quotes=False):
    masked = mask(text, include_code, include_quotes)
    x1_src = mask(text, include_code, include_quotes, keep_urls=True)
    nmasked, nmap = norm_with_map(masked)
    hits = []
    for rid, strength, label, rx, kind in rules():
        src = {'en': masked, 'raw': x1_src, 'ar': nmasked}[kind]
        for m in rx.finditer(src):
            if m.end() <= m.start():
                continue
            if kind == 'ar':                                  # map back to the original spelling
                s, e = nmap[m.start()], nmap[m.end() - 1] + 1
                while e < len(text) and HARAKAT.match(text[e]):   # keep the last letter's own marks
                    e += 1
            else:
                s, e = m.start(), m.end()
            hits.append(_hit(rid, strength, label, text, s, e))
    # weak hits covered by their stronger sibling are dropped (no double counting)
    for weak, strong in SHADOWED_BY.items():
        spans = [(h['start'], h['end']) for h in hits if h['id'] == strong]
        hits = [h for h in hits if h['id'] != weak or not any(a <= h['start'] < b for a, b in spans)]

    # Title Case headings: one is a weak sign, two or more become a normal tell
    tc = 0
    for m in TITLE_HEADING.finditer(masked):
        sig = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", m.group(1)) if len(w) > 3]
        if len(sig) >= 3 and all(w[0].isupper() for w in sig) and not all(w.isupper() for w in sig):
            tc += 1
            hits.append(_hit('H20t', 'weak', 'Title Case heading', text, m.start(1), m.end(1)))
    if tc >= 2:
        hits.append({'id': 'H20+', 'strength': 'normal', 'label': 'Title Case on several headings',
                     'line': 0, 'match': f'{tc} headings'})

    # Arabic typography: Latin and Arabic-Indic digits mixed; tatweel used as decoration
    if AR_DIGIT.search(masked) and EN_DIGIT.search(masked) and re.search('[' + AR_LETTER + ']', masked):
        hits.append({'id': 'AR26d', 'strength': 'weak', 'label': 'two digit systems in one Arabic text',
                     'line': 0, 'match': '٠-٩ and 0-9'})
    for m in re.finditer('ـ{2,}', masked):
        hits.append(_hit('AR26t', 'weak', 'tatweel as decoration', text, max(m.start() - 3, 0), m.end() + 3))

    sents = sentences(masked)
    lens = [len(s.split()) for s in sents]
    firsts = []
    for s in sents:
        w = FIRST_WORD.search(s)
        firsts.append(norm_ar(w.group(0)).lower() if w else '')
    repeats = sum(1 for a, b in zip(firsts, firsts[1:]) if a and a == b)
    if repeats >= 2:
        hits.append({'id': 'H7', 'strength': 'weak', 'label': 'repeated sentence openings',
                     'line': 0, 'match': f'{repeats} adjacent repeats'})
    words = len(masked.split())
    dashes = sum(1 for h in hits if h['id'] == 'H8')
    if dashes >= 3 and dashes * 100 / max(words, 1) >= 1.0:      # one dash is human; a page full of them is not
        hits.append({'id': 'H8+', 'strength': 'normal', 'label': 'dash density',
                     'line': 0, 'match': f'{dashes} dashes in {words} words'})

    fam = {h['id'] for h in hits}
    strong = {h['id'] for h in hits if h['strength'] == 'strong'}
    normal = {h['id'] for h in hits if h['strength'] == 'normal'}
    n_normal_hits = sum(1 for h in hits if h['strength'] == 'normal')
    verdict = ('EDIT' if strong else
               'REVIEW' if len(normal) >= 2 or n_normal_hits >= 3 or len(fam) >= 4 else
               'LOOK' if normal else 'LEAVE' if fam else 'CLEAN')
    hits.sort(key=lambda h: (RANK[h['strength']], h['line'], h['id']))
    for h in hits:
        h.pop('start', None)
        h.pop('end', None)
    return {
        'verdict': verdict, 'verdict_text': VERDICT_TEXT.get(verdict, verdict),
        'words': words, 'sentences': len(lens),
        'mean_sentence_words': round(statistics.mean(lens), 1) if lens else 0,
        'sentence_length_stdev': round(statistics.pstdev(lens), 1) if lens else 0,
        'rhythm_note': ('sentence-length spread is informational only below 150 words' if words < 150 else
                        'low spread with long text can mean uniform rhythm; read it aloud before acting'),
        'tells_per_100_words': round(100 * len(hits) / max(words, 1), 1),
        'families': sorted(fam), 'hits': hits,
        'note': 'Heuristic editing aid. Several tells together are the signal; never use this to judge who wrote a text.',
    }


# --------------------------------------------------------------------------- CLI
def list_rules():
    rows = [(i, s, l) for i, s, l, _ in EN] + [X1[:3]] + [(i, s, l) for i, s, l, _ in AR]
    rows += [('H7', 'weak', 'repeated sentence openings (computed)'), ('H8+', 'normal', 'dash density (computed)'),
             ('H20t', 'weak', 'Title Case heading (computed)'), ('H20+', 'normal', 'Title Case on several headings (computed)'),
             ('AR26d', 'weak', 'two digit systems in one Arabic text (computed)'), ('AR26t', 'weak', 'tatweel as decoration (computed)')]
    for i, s, l in rows:
        print(f'{i:6} {s:6} {l}')


def main(argv=None):
    ap = argparse.ArgumentParser(prog='tell_scan.py', description='Flag stock writing habits in English and Arabic prose (editing aid, not an authorship detector).',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog='Examples:\n  python3 tell_scan.py draft.md\n  python3 tell_scan.py draft.md --json\n'
                                        '  cat reply.txt | python3 tell_scan.py - --fail-on review\n  python3 tell_scan.py --list-rules')
    ap.add_argument('files', nargs='*', help="text or Markdown files; '-' reads stdin")
    ap.add_argument('--json', action='store_true', help='print a JSON report (a list when several files are given)')
    ap.add_argument('--fail-on', choices=['edit', 'review', 'look'], help='exit 1 when any verdict is at or above this level')
    ap.add_argument('--include-code', action='store_true', help='also scan fenced code, inline code, URLs and blockquotes')
    ap.add_argument('--include-quotes', action='store_true', help='also scan the inside of quotations')
    ap.add_argument('--list-rules', action='store_true', help='print every rule id, strength and label, then exit')
    a = ap.parse_args(argv)
    if a.list_rules:
        list_rules()
        return 0
    if not a.files:
        ap.error('give at least one FILE (or - for stdin)')
    reports = []
    for f in a.files:
        try:
            text = sys.stdin.read() if f == '-' else Path(f).read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError) as e:
            ap.error(f'{f}: {e}')
        r = scan(text, a.include_code, a.include_quotes)
        r['file'] = f
        reports.append(r)
    if a.json:
        print(json.dumps(reports[0] if len(reports) == 1 else reports, ensure_ascii=False, indent=2))
    else:
        for r in reports:
            if len(reports) > 1:
                print(f"== {r['file']}")
            print(f"verdict: {r['verdict_text']} | words {r['words']} | sentences {r['sentences']} | "
                  f"mean len {r['mean_sentence_words']} sd {r['sentence_length_stdev']} | tells/100w {r['tells_per_100_words']}")
            for h in r['hits']:
                print(f"  [{h['strength']:6}] {h['id']:6} L{h['line']:<3} {h['label']}: {h['match']}")
    if a.fail_on:
        bar = VERDICTS.index(a.fail_on.upper())
        if any(VERDICTS.index(r['verdict']) >= bar for r in reports):
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
