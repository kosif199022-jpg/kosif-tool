#!/usr/bin/env python3
"""
reel_tools.py - Arabic-first Reel writing tools for KOSIF (stdlib only, offline).

Three commands:
  hook   score a Reel's opening line on five properties, or rank several
  beats  turn a spoken script into a timed beat sheet and flag what kills it
  clean  find (and with --fix strip) the AI fingerprint in a draft

Works on Egyptian Arabic, Modern Standard Arabic and English, and on mixed
lines. Arabic-Indic digits count as numbers.

The idea of the five hook checks, the beat sheet and the humanizer pass comes
from Jake Schincariol's MIT-licensed instagram-agent-skill
(github.com/Jakeschincariol/instagram-agent-skill). Its scripts only read
Latin letters, so an Arabic hook scores zero there. This file is a fresh
implementation with Arabic lexicons, not a copy of that code.

What the hook score is NOT: a view predictor. It catches greetings,
preambles, hooks with nothing concrete in them and hooks that take too long
to say. Which of two decent hooks travels is decided by the face, the edit,
the audio and the feed. Trust the retention graph over this script.

Usage
  python3 reel_tools.py hook --hook "خسرت ٤٠٠٠ جنيه في عقد ناقصه سطر واحد."
  python3 reel_tools.py hook hooks.txt            # one hook per line, ranked
  python3 reel_tools.py hook --hook "..." --screen "٤٠٠٠ جنيه ضاعوا"
  python3 reel_tools.py beats script.txt --target 30
  python3 reel_tools.py clean draft.txt [--fix --out clean.txt]
  add --json to any command for machine output
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

# ---------------------------------------------------------------- text basics

DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
TASHKEEL_RE = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
TOKEN_RE = re.compile(r"[ء-يٱ-ۓA-Za-z0-9$%'’٪٫٬.,-]+")
ARABIC_RE = re.compile(r"[ء-ي]")


def norm(word):
    """Fold the spellings Egyptian writers mix: hamza seats, ta marbuta, ya."""
    w = TASHKEEL_RE.sub("", word.translate(DIGITS)).lower()
    w = re.sub("[إأآٱ]", "ا", w)
    w = w.replace("ة", "ه").replace("ى", "ي").replace("ؤ", "و").replace("ئ", "ي")
    return w.strip(".,'’-")


def tokens(text):
    raw = TOKEN_RE.findall(text.translate(DIGITS))
    out = []
    for t in raw:
        t = t.strip(".,-")
        if t:
            out.append(t)
    return out


def variants(word):
    """A word plus its forms without the attached و / ف / ب / ل / ال."""
    w = norm(word)
    forms = {w}
    for pre in ("و", "ف"):
        if w.startswith(pre) and len(w) > 3:
            forms.add(w[1:])
    for f in list(forms):
        for pre in ("ال", "بال", "لل", "كال"):
            if f.startswith(pre) and len(f) - len(pre) >= 2:
                forms.add(f[len(pre):])
    return forms


def in_lex(word, lex):
    return bool(variants(word) & lex)


def is_arabic(text):
    letters = re.findall(r"[A-Za-zء-ي]", text)
    return bool(letters) and sum(1 for c in letters if ARABIC_RE.match(c)) / len(letters) >= 0.5


def lex(words):
    return {norm(w) for w in words.split()}


# ---------------------------------------------------------------- lexicons

SPOKEN_NUMBERS = lex("""
صفر اتنين اثنين اتنين تلات تلاته ثلاث ثلاثه اربع اربعه خمس خمسه ست سته سبع سبعه
تمن تمنيه تمانيه ثماني ثمانيه تسع تسعه عشر عشره عشرين عشرون تلاتين ثلاثين اربعين
خمسين ستين سبعين تمانين تسعين ميه مية مائه مئه ميتين الف الفين الاف تلاف مليون
ملايين مليار نص نصف ربع تلت ثلث ضعف دوبل
zero two three four five six seven eight nine ten eleven twelve fifteen twenty
thirty forty fifty hundred thousand million billion dozen half twice triple
""")

UNITS = lex("""
ثانيه ثواني دقيقه دقايق دقائق ساعه ساعات يوم يومين ايام اسبوع اسبوعين اسابيع شهر
شهرين شهور سنه سنتين سنين سنوات عام اعوام مره مرات
second seconds minute minutes hour hours day days week weeks month months year years
""")

MONEY = lex("""
جنيه جنيهات دولار دولارات ريال درهم دينار يورو فلوس مرتب راتب ايجار ربح ارباح مكسب
خساره ميزانيه سعر تمن ثمن
dollar dollars bucks grand percent salary rent revenue profit
""")

STAKES = lex("""
خسرت خسرنا خساره بخسر هتخسر غلط غلطه اغلاط اخطاء خطا متعملش ماتعملش متعملوش
مش مفيش محدش ماحدش ماحدّش حد سر اسرار سري ممنوع اوعي اياك بطل وقف اترفدت فشلت فشل
ضيعت ضاع ضاعت ضياع اتسرق سرقه نصب كدب كذب كدبه الحقيقه حقيقه مجاني ببلاش بدل بدون
من غير لكن بس قبل لحد ندمت ندم تحذير خطر اسوا احسن اغلي ارخص وفرت وفرت وفر
مستحيل اول اخر الوحيد دلوقتي بقيت بقت بدلا ضد مقابل بجد فعلا لسه خلاص ابدا عمر عمري
اسرق انسرق
stop never wrong mistake lost lose cost broke failed nobody no not don't can't
quit fired deleted secret truth lie free only without instead but before until
worst regret wasted warning versus vs actually still already first
""")

WEAK_OPENERS = [norm(x) for x in [
    "اهلا", "أهلاً", "مرحبا", "السلام", "ازيكم", "إزيكم", "هاي", "يا جماعه", "يا شباب",
    "النهارده", "النهاردة", "انهارده", "اليوم", "طيب", "بص", "بصوا", "بصراحه",
    "خلونا", "خليني", "قبل ما", "انا عايز", "أنا عايز", "حابب", "في الفيديو", "في فيديو",
    "هل", "يعني", "اولا", "أولاً", "زي ما", "كلنا",
    "so", "ok", "okay", "hey", "hi", "hello", "guys", "welcome", "today",
    "basically", "honestly", "in this", "in today", "have you", "did you", "do you",
]]

IMPERATIVES = lex("""
اسرق انسخ جرب احذف امسح اوعي متعملش ماتعملش بطل استخدم ابدا ابدأ اعمل ابعت شوف اتفرج
اقرا احفظ خد خدوا وقف سيب ركز اكتب اسال اطلب
stop steal copy delete try watch read save use build make write send take start
""")

YOU = lex("""
انت انتي انتو انتم انتَ انتِ ليك ليكي ليكو عليك عليكي بتاعك بتاعتك عندك معاك
you your you're yourself
""")

ME = lex("""
انا احنا نحن عندي عندنا بتاعي بتاعتي معايا ليا مني بتاعنا
i my me we our
""")

STOP = lex("""
في من على علي عن الي إلى لـ و ف ب ال ده دي دا دول اللي الذي التي هو هي هم انا
انت احنا ان أن إن كان كانت يكون مش مع كل بس ما لا او أو ثم يعني عشان علشان لما
لو اذا إذا كده كدا جدا خالص برضه برده بقي بقى هنا هناك
the a an and or but if of to in on for with that this it is are was be you your
i my me we our they so just not no do have has at as by from
""")

GREETING_RE = re.compile(
    r"^\s*(?:اهلا|أهلا|أهلاً|اهلاً|مرحب|السلام عليكم|ازيك|إزيك|هاي|صباح الخير|مساء الخير"
    r"|hey\b|hi\b|hello\b|what'?s up|welcome)", re.IGNORECASE)
PREAMBLE_RE = re.compile(
    r"في (?:الفيديو|الريل|فيديو) (?:ده|دا|هذا|النهارده|النهاردة|اليوم)"
    r"|(?:هوريك|هوريكم|هقولك|هقولكم|هشرحلك|هشرحلكم|خليني اوريك|خلّيني أوريك)"
    r"|النهارد[هة] (?:هنتكلم|هتكلم|حنتكلم)"
    r"|in (?:this|today'?s) (?:video|reel)|i'?m going to show you|i'?ll show you how",
    re.IGNORECASE)
SCROLL_RE = re.compile(
    r"^\s*(?:استني|استنى|متقلبش|ماتقلبش|متعديش|ماتعديش|وقف التقليب|stop scrolling|don'?t scroll)",
    re.IGNORECASE)
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

DEALBREAKERS = [
    (SCROLL_RE, "بيبدأ بـ«استنى/متقلبش». طلب الانتباه معناه إنك لسه ما كسبتهوش."),
    (PREAMBLE_RE, "مقدمة فيديو («في الفيديو ده / هوريكم»). امسحها وابدأ بالنتيجة."),
    (GREETING_RE, "تحية. محدش فاتح الفيد عشان حد يسلّم عليه."),
    (HASHTAG_RE, "هاشتاج في الهوك. مكانه آخر الكابشن لو لازم."),
    (EMOJI_RE, "إيموجي في الهوك. كارت الهوك فيه مكان للكلام أو للإيموجي، مش الاتنين."),
]

NUMBER_RE = re.compile(r"\$?\s?\d[\d,٬.]*\s?(?:%|٪|k\b|x\b)?", re.IGNORECASE)
LATIN_PROPER_RE = re.compile(r"(?<!^)\b[A-Z][a-z]{2,}\b")


def clamp(n):
    return max(0.0, min(100.0, n))


# ---------------------------------------------------------------- hook checks

def speaking_rate(text):
    """Words per second. Arabic words carry their clitics, so fewer per minute."""
    return 140 / 60 if is_arabic(text) else 165 / 60


def check_length(text):
    n = len(tokens(text))
    secs = n / speaking_rate(text)
    chars = len(text.strip())
    lo, hi = (4, 10) if is_arabic(text) else (5, 12)
    if lo <= n <= hi:
        score = 100.0
    elif n < lo:
        score = 100 - (lo - n) * 20
    else:
        score = 100 - (n - hi) * 11
    if chars > 60:
        score -= 12
    return clamp(score), f"{n} كلمة، {chars} حرف، حوالي {secs:.1f} ثانية (المطلوب {lo}-{hi} كلمة)"


def concrete_markers(text):
    nums = [m.strip() for m in NUMBER_RE.findall(text.translate(DIGITS)) if re.search(r"\d", m)]
    names = sorted(set(LATIN_PROPER_RE.findall(text)))
    spoken = [t for t in tokens(text) if in_lex(t, SPOKEN_NUMBERS | MONEY | UNITS)]
    return nums + names + spoken


def check_specificity(text):
    hits = concrete_markers(text)
    score = 15.0 if not hits else clamp(45 + len(hits) * 30)
    found = "، ".join(hits[:4])
    return score, (f"{len(hits)} علامة ملموسة" + (f": {found}" if found
                   else " - مفيش رقم ولا اسم ولا حاجة تتقاس"))


def check_stakes(text):
    marks = sorted({norm(t) for t in tokens(text) if in_lex(t, STAKES)})
    if re.search(r"\$\s?\d|\d[\d,٬]*\s*(?:جنيه|دولار|ريال|درهم)", text.translate(DIGITS)):
        marks.append("سعر")
    score = {0: 20.0, 1: 70.0}.get(len(marks), 100.0)
    return score, (f"{len(marks)} علامة توتر" + (f": {'، '.join(marks[:4])}" if marks
                   else " - مفيش حاجة على المحك في السطر ده"))


def check_frontload(text):
    t = tokens(text)
    if not t:
        return 0.0, "فاضي"
    opener = norm(" ".join(t[:2]))
    weak = next((w for w in WEAK_OPENERS if opener.startswith(w) or norm(t[0]) == w), None)
    payload = None
    for i, tok in enumerate(t):
        if (in_lex(tok, STAKES | SPOKEN_NUMBERS | MONEY) or re.search(r"\d", tok)
                or (i and LATIN_PROPER_RE.fullmatch(tok))):
            payload = i
            break
    if payload is None:
        base, where = 30.0, "مفيش كلمة تقيلة في السطر كله"
    elif payload <= 3:
        base, where = 100.0, f"الكلمة التقيلة في الكلمة رقم {payload + 1}"
    elif payload <= 6:
        base, where = 70.0, f"الكلمة التقيلة في رقم {payload + 1}، قدّمها"
    else:
        base, where = 40.0, f"الكلمة التقيلة في رقم {payload + 1}، متأخرة"
    return clamp(base - (30 if weak else 0)), where + (f"؛ بداية ضعيفة «{weak}»" if weak else "")


def check_address(text):
    t = tokens(text)
    your_nouns = ("حياتك", "شغلك", "فلوسك", "وقتك", "بيتك", "مشروعك", "زباينك", "عملاءك", "مرتبك")
    not_you = {"ذلك", "كذلك", "لذلك", "هناك", "تلك", "ملك", "شك", "بنك", "سمك", "فلك", "مشترك"}

    def to_you(tok):
        w = norm(tok)
        return (ARABIC_RE.match(w[:1] or " ") and len(w) >= 4 and w.endswith("ك")
                and w not in not_you)

    if (any(in_lex(x, YOU) for x in t) or any(norm(x) in {norm(w) for w in your_nouns} for x in t)
            or any(to_you(x) for x in t)):
        return 100.0, "بيكلّم المشاهد"
    first = norm(t[0]) if t else ""
    negative_command = re.fullmatch(r"(?:ما|م)ت\w{2,}ش", first) is not None
    if t and (in_lex(t[0], IMPERATIVES) or negative_command):
        return 90.0, f"بيبدأ بأمر («{t[0]}»)"
    if any(in_lex(x, ME) for x in t) or (t and is_arabic(text) and norm(t[0]).endswith("ت")
                                         and len(norm(t[0])) >= 4):
        return 70.0, "بصيغة المتكلم، من غير ما يكلّم المشاهد"
    return 35.0, "بصيغة الغايب، محدش في الأوضة"


CHECKS = [("LENGTH", "الطول", check_length), ("SPECIFICITY", "التحديد", check_specificity),
          ("STAKES", "المخاطرة", check_stakes), ("FRONTLOAD", "التقديم", check_frontload),
          ("ADDRESS", "المخاطَب", check_address)]


def score_hook(text, screen=None):
    checks = {key: dict(zip(("score", "detail"), fn(text))) for key, _, fn in CHECKS}
    flags = [msg for pat, msg in DEALBREAKERS if pat.search(text)]
    scores = [c["score"] for c in checks.values()]
    # The weakest property caps the hook: one bad property is enough for the thumb.
    overall = clamp(statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15)
    verdict = ("STRONG" if overall >= 70 and min(scores) >= 55 and not flags
               else "OK" if overall >= 50 else "WEAK")
    weakest = min(checks, key=lambda k: checks[k]["score"])
    result = {"hook": text.strip(), "score": round(overall, 1), "verdict": verdict,
              "weakest": weakest, "checks": checks, "flags": flags,
              "language": "ar" if is_arabic(text) else "en"}
    if screen is not None:
        n = len(tokens(screen))
        result["screen"] = {"text": screen, "words": n, "ok": n <= 6,
                            "note": "تمام" if n <= 6 else f"{n} كلمات على الشاشة، خليهم 6 أو أقل"}
    return result


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_hook(r, out):
    names = {k: ar for k, ar, _ in CHECKS}
    print("\nتقييم الهوك / HOOK SCORE\n" + "=" * 62, file=out)
    print(f"  «{r['hook']}»\n", file=out)
    for k, c in r["checks"].items():
        print(f"  {k:<12} {names[k]:<9} {bar(c['score'])} {c['score']:5.1f}", file=out)
        print(f"  {'':<22} {c['detail']}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HOOK SCORE':<22} {bar(r['score'])} {r['score']:5.1f}   {r['verdict']}", file=out)
    for f in r["flags"]:
        print(f"\n  ✗ {f}", file=out)
    if "screen" in r:
        print(f"\n  على الشاشة: «{r['screen']['text']}» - {r['screen']['note']}", file=out)
    if r["verdict"] != "STRONG":
        print(f"\n  أضعف نقطة: {names[r['weakest']]} ({r['weakest']}). صلّحها وأعد التقييم.", file=out)
    print("", file=out)


def render_rank(rows, out):
    print("\nترتيب الهوكات / HOOK RANKING\n" + "=" * 70, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {r['hook'][:60]}", file=out)
        print(f"        أضعف نقطة: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        ✗ {f}", file=out)
    print("\nصوّر الأول. لو الأول تحت 50، يبقى ولا واحد فيهم هو الهوك.\n", file=out)


# ---------------------------------------------------------------- beat sheet

HOOK_WINDOW = 3.0
MAX_BEAT = 4.0
SPLIT_RE = re.compile(r"[^.!?؟\n]+[.!?؟]*")


def tc(sec):
    return f"{int(sec // 60)}:{sec % 60:04.1f}"


def content_words(text):
    out = set()
    for t in tokens(text):
        v = variants(t)
        if not (v & STOP) and len(norm(t)) > 2:
            out |= v
    return out


def beat_sheet(raw, wpm=None, target=None):
    lines = [s.strip() for s in SPLIT_RE.findall(raw) if s.strip() and tokens(s)]
    if wpm is None:
        wpm = 140 if is_arabic(raw) else 165
    wps = wpm / 60
    rows, t = [], 0.0
    for i, line in enumerate(lines):
        n = len(tokens(line))
        dur = n / wps + 0.25          # a breath between beats
        rows.append({"n": i + 1, "start": round(t, 2), "dur": round(dur, 2), "words": n,
                     "text": line, "concrete": bool(concrete_markers(line)), "flags": []})
        t += dur
    flags, notes = [], []
    if not rows:
        return {"beats": [], "total": 0, "wpm": wpm, "flags": ["السكربت فاضي"], "notes": []}
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"الهوك {rows[0]['dur']:.1f} ثانية، أطول من {HOOK_WINDOW:.0f} ثواني")
    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f} ثانية على بيت واحد، اقسمه أو غيّر الكادر")
    run = 0
    for r in rows:
        run = 0 if r["concrete"] else run + 1
        if run == 3:
            r["flags"].append("تالت بيت ورا بعض من غير رقم ولا اسم ولا حاجة ملموسة")
    hook_words = set()
    for r in rows[:-1] or rows:
        if r["start"] < HOOK_WINDOW:
            hook_words |= content_words(r["text"])
    loop = sorted(hook_words & content_words(rows[-1]["text"]))
    if len(rows) > 1 and loop:
        notes.append(f"لوب: آخر بيت بيكرر «{'، '.join(loop[:3])}» من الهوك.")
    elif len(rows) > 1:
        flags.append("مفيش لوب: آخر بيت مفيهوش ولا كلمة من الهوك، فالإعادة مش هتركب.")
    total = round(t, 1)
    if target:
        if total > target * 1.2:
            flags.append(f"المدة {total} ثانية، أطول من الهدف {target} بأكتر من 20%")
        elif total < target * 0.8:
            flags.append(f"المدة {total} ثانية، أقصر من الهدف {target} بأكتر من 20%")
    if total > 45:
        notes.append("أطول من 45 ثانية. المدى الشغّال 15 لـ 45.")
    for r in rows:
        flags.extend(f"بيت {r['n']}: {f}" for f in r["flags"])
    return {"beats": rows, "total": total, "wpm": wpm, "target": target,
            "flags": flags, "notes": notes, "clean": not flags}


def render_beats(a, out):
    print(f"\nجدول البيتات / BEAT SHEET  ({a['wpm']} كلمة/دقيقة)\n" + "=" * 70, file=out)
    for r in a["beats"]:
        mark = "!" if r["flags"] else " "
        print(f"{mark} {tc(r['start'])}  {r['dur']:4.1f}s  {r['text'][:58]}", file=out)
    print("-" * 70, file=out)
    tgt = f" / الهدف {a['target']}s" if a.get("target") else ""
    print(f"  المدة: {a['total']}s عبر {len(a['beats'])} بيت{tgt}", file=out)
    for f in a["flags"]:
        print(f"  ✗ {f}", file=out)
    for n in a["notes"]:
        print(f"  • {n}", file=out)
    print("  " + ("نضيف. صوّر." if a.get("clean") else "صلّح العلامات وأعد التشغيل."), file=out)
    print("", file=out)


# ---------------------------------------------------------------- clean (humanizer)

INVISIBLE_RE = re.compile("[​‌‍‎‏⁠⁡⁢⁣﻿­]")
DASH_RE = re.compile(r"\s*[—–]\s*")
SLOP = [
    ("في عالم اليوم", "افتتاحية عامة"), ("في عالمنا", "افتتاحية عامة"),
    ("في ظل", "صياغة رسمية"), ("مما لا شك فيه", "حشو"), ("لا شك أن", "حشو"),
("في نهاية المطاف", "حشو"), ("علاوة على ذلك", "ربط كتابي"),
    ("بالإضافة إلى ذلك", "ربط كتابي"), ("بالاضافة الى ذلك", "ربط كتابي"),
    ("في الختام", "خاتمة كتابية"), ("دعونا", "صيغة مترجمة"), ("دعنا", "صيغة مترجمة"),
    ("رحلة", "كلمة مستهلكة"), ("عزيزي المشاهد", "خطاب رسمي"), ("بشكل كبير", "حشو"),
    ("يعتبر", "صياغة كتابية"), ("يُعد", "صياغة كتابية"), ("يعد ", "صياغة كتابية"),
    ("ليس فقط", "قالب «ليس فقط... بل»"), ("لا يقتصر", "قالب «لا يقتصر... بل»"),
    ("delve", "slop word"), ("tapestry", "slop word"), ("game-changer", "slop word"),
    ("in today's", "generic opener"), ("let's dive", "generic opener"),
    ("it's not just", "not-just template"), ("unlock", "slop word"),
]


def clean_text(text, fix=False):
    found = []
    inv = INVISIBLE_RE.findall(text)
    if inv:
        found.append({"kind": "invisible", "count": len(inv),
                      "note": "حروف مخفية (علامة مائية محتملة أو بقايا نسخ)"})
    dashes = DASH_RE.findall(text)
    if dashes:
        found.append({"kind": "dash", "count": len(dashes),
                      "note": "شرطة طويلة —، الناس مش بتنطقها ولا بتكتبها في الكلام"})
    low = norm(text)
    for phrase, why in SLOP:
        c = low.count(norm(phrase))
        if c:
            found.append({"kind": "slop", "phrase": phrase, "count": c, "note": why})
    fixed = text
    if fix:
        fixed = INVISIBLE_RE.sub("", fixed)
        fixed = DASH_RE.sub("، " if is_arabic(text) else ", ", fixed)
        fixed = unicodedata.normalize("NFC", fixed)
    sentences = [s for s in SPLIT_RE.findall(text) if tokens(s)]
    lens = [len(tokens(s)) for s in sentences]
    spread = statistics.pstdev(lens) if len(lens) > 1 else 0.0
    if len(lens) >= 4 and spread < 2.0:
        found.append({"kind": "rhythm", "count": len(lens),
                      "note": f"كل الجمل نفس الطول تقريبًا (انحراف {spread:.1f})، نوّع"})
    penalty = sum(min(f["count"], 3) * (10 if f["kind"] == "slop" else 8) for f in found)
    human = clamp(100 - penalty)
    return {"human_score": round(human, 1), "verdict": "PASS" if human >= 70 else "FIX",
            "found": found, "fixed": fixed if fix else None,
            "auto_fixed": [f["kind"] for f in found if f["kind"] in ("invisible", "dash")] if fix else []}


def render_clean(r, out):
    print(f"\nفحص البصمة الآلية / HUMANIZER\n" + "=" * 62, file=out)
    if not r["found"]:
        print("  مفيش حاجة. الكلام شكله بشري.", file=out)
    for f in r["found"]:
        label = f.get("phrase", f["kind"])
        print(f"  ✗ {label} ×{f['count']}: {f['note']}", file=out)
    print("-" * 62, file=out)
    print(f"  درجة البشرية: {r['human_score']}  {r['verdict']}", file=out)
    if r["auto_fixed"]:
        print(f"  اتشال تلقائيًا: {', '.join(r['auto_fixed'])}. الباقي محتاج إعادة صياغة بإيدك.", file=out)
    print("", file=out)


# ---------------------------------------------------------------- CLI

def read_input(path):
    return sys.stdin.read() if path in (None, "-") else open(path, encoding="utf-8").read()


def main(argv=None):
    ap = argparse.ArgumentParser(description="KOSIF Reel tools (Arabic-first).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("hook", help="score or rank hooks")
    h.add_argument("input", nargs="?", default="-")
    h.add_argument("--hook")
    h.add_argument("--screen", help="the on-screen card for a single --hook")
    h.add_argument("--json", action="store_true")
    b = sub.add_parser("beats", help="timed beat sheet")
    b.add_argument("input", nargs="?", default="-")
    b.add_argument("--target", type=float)
    b.add_argument("--wpm", type=float)
    b.add_argument("--json", action="store_true")
    c = sub.add_parser("clean", help="humanizer pass")
    c.add_argument("input", nargs="?", default="-")
    c.add_argument("--fix", action="store_true")
    c.add_argument("--out")
    c.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    out = sys.stdout

    if args.cmd == "hook":
        if args.hook:
            r = score_hook(args.hook, args.screen)
            print(json.dumps(r, ensure_ascii=False, indent=2)) if args.json else render_hook(r, out)
            return 0 if r["verdict"] != "WEAK" else 1
        lines = [l.strip() for l in read_input(args.input).splitlines() if l.strip()]
        rows = sorted((score_hook(l) for l in lines), key=lambda r: -r["score"])
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        elif len(rows) == 1:
            render_hook(rows[0], out)
        else:
            render_rank(rows, out)
        return 0
    if args.cmd == "beats":
        a = beat_sheet(read_input(args.input), args.wpm, args.target)
        print(json.dumps(a, ensure_ascii=False, indent=2)) if args.json else render_beats(a, out)
        return 0 if a.get("clean") else 1
    r = clean_text(read_input(args.input), fix=args.fix)
    if args.fix and args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(r["fixed"])
    print(json.dumps(r, ensure_ascii=False, indent=2)) if args.json else render_clean(r, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
