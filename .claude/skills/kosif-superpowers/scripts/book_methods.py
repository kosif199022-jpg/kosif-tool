#!/usr/bin/env python3
"""KOSIF book methods (A20): thinking, talent and craft methods distilled from ten owner-uploaded PDFs.

Registry: data/book_methods.json (our own wording; no book text copied). Sources: a lateral-thinking
course (REST), The Pragmatic Programmer, Jaynes's Bayesian framework (the upload itself was an empty
sales teaser), the Cambridge Handbook of Personality Psychology, an AI accounting skill report
(IFRS/ISA), the owner's KOSIF v8 prompt spec, Shawqi's diwan, two English coursebooks; one
unlicensed fan translation was excluded.

Commands
  sources                       the ten files: what each is and whether it was used
  list [--domain D]             methods (lateral, engineering, bayesian, personality, accounting,
                                prompting, arabic-verse, teaching, drama)
  search "<words>"              Arabic/English search
  show <ID>                     one method with steps and its check
  rest --problem "<p>" [--words N] [--seed S]
                                random-word provocation (LT-02/LT-03), seeded and reproducible
  bayes --h A=0.5 --h B=0.5 --e "name:A=0.9,B=0.2" ...
                                posterior and a decibel evidence ledger (BY-01/BY-02)
  clarity "<prompt>" | --file F prompt clarity/context/specificity score and GENERATE/REVISE (KV-02)
  ledger --file entries.json [--revenue 4101 --receivable 1201]
                                balance, integer-minor-unit, VAT and duplicate/settlement checks (AC-03..06)
  persona --name N --big5 O=4,C=2,E=5,A=2,N=3
                                character card: speech rules, if-then signatures, arc, goal/fear (PS-01..06)
"""
import argparse
import json
import math
import random
import re
import sys
import unicodedata
from decimal import Decimal, InvalidOperation
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
DATA = SKILL / "data" / "book_methods.json"
DOMAINS = {"lateral", "engineering", "bayesian", "personality", "accounting", "prompting",
           "arabic-verse", "teaching", "drama"}
ALIASES = {"تفكير": "lateral thinking", "إبداع": "lateral idea", "أفكار": "idea lateral", "جانبي": "lateral",
           "برمجة": "engineering code", "كود": "code engineering", "اختبار": "test", "تصحيح": "debugging",
           "احتمال": "bayesian probability", "بايز": "bayesian", "أدلة": "evidence", "قرار": "decision",
           "شخصية": "personality character", "نبرة": "tone voice", "حوار": "dialogue", "قصة": "story arc",
           "محاسبة": "accounting", "قيد": "entry ledger", "فاتورة": "invoice", "ضريبة": "vat tax",
           "معايير": "ifrs isa standards", "برومنت": "prompt", "وضوح": "clarity", "صورة": "image prompt",
           "شعر": "verse poem", "قصيدة": "verse poem", "دعاء": "verse", "عربي": "arabic", "درس": "teaching lesson",
           "تعليم": "teaching", "سيناريو": "script"}

# Seeded REST word pool: concrete nouns, deliberately unrelated to any domain.
WORDS = ["مرآة", "بوصلة", "خيمة", "مظلة", "جسر", "قنديل", "ساعة رملية", "سلّم", "مفتاح", "نحلة", "مرساة",
         "طائرة ورقية", "قفل", "بذرة", "موجة", "صدى", "خريطة", "شمعة", "إبرة", "عدسة", "ستارة", "طاحونة",
         "قطار", "بئر", "نافذة", "حبل", "مغناطيس", "فانوس", "ريشة", "صندوق", "عش", "شبكة", "نهر", "قوس قزح",
         "ظل", "جرس", "مصعد", "حديقة", "سوق", "ميزان", "منارة", "قارب", "ثلج", "نار", "خبز", "زجاج", "باب",
         "mirror", "compass", "tent", "umbrella", "bridge", "lantern", "hourglass", "ladder", "key", "bee",
         "anchor", "kite", "lock", "seed", "wave", "echo", "map", "candle", "needle", "lens", "curtain",
         "windmill", "train", "well", "window", "rope", "magnet", "feather", "box", "nest", "net", "river",
         "shadow", "bell", "elevator", "garden", "market", "scale", "lighthouse", "boat", "snow", "bread"]
MODES = [("association", "ما الذي تذكّرك به الكلمة؟ سلسلها ثم اربط كل حلقة بالمشكلة", "What does it remind you of? Chain it, then link each step to the problem."),
         ("function", "ما وظيفة هذا الشيء (يحمي، يخفي، يوصل، يزن)؟ أين تحتاج المشكلة هذه الوظيفة؟", "What does the thing do? Where does the problem need that job?"),
         ("direct", "اقرأ الكلمة أمرًا ونفّذه على المشكلة حرفيًا", "Read the word as a command and apply it literally."),
         ("pun", "جناس أو نكتة أو كلمة قريبة الصوت؛ إلى أين تقودك؟", "A pun, joke or sound-alike: where does it lead?")]
HOLLOW = ["beautiful", "nice", "cool", "amazing", "great", "good", "awesome", "stunning", "epic",
          "جميل", "جميلة", "رائع", "رائعة", "حلو", "حلوة", "مذهل", "مذهلة", "عظيم", "ممتاز"]
CONTEXT = {
    "time": ["morning", "evening", "night", "dawn", "dusk", "noon", "sunset", "sunrise", "winter", "summer", "autumn",
             "spring", "19", "20", "century", "صباح", "مساء", "ليل", "فجر", "غروب", "شروق", "ظهر", "شتاء", "صيف", "خريف",
             "ربيع", "قرن", "الخمسينات", "الثمانينات", "ساعة"],
    "place": ["room", "kitchen", "street", "city", "desert", "forest", "sea", "beach", "house", "office", "market",
              "mountain", "غرفة", "مطبخ", "شارع", "مدينة", "صحراء", "غابة", "بحر", "شاطئ", "منزل", "بيت", "مكتب", "سوق", "جبل"],
    "emotion": ["sad", "happy", "nostalg", "calm", "tense", "fear", "joy", "lonely", "hope", "grief", "anger", "warm",
                "حزن", "حزين", "فرح", "حنين", "هادئ", "توتر", "خوف", "وحدة", "أمل", "غضب", "دافئ", "كآبة", "شوق"],
    "motion": ["slow", "fast", "static", "dolly", "pan", "tilt", "push", "orbit", "handheld", "walk", "run",
               "بطيء", "سريع", "ثابت", "حركة", "تمشي", "يركض", "تدور", "اقتراب", "ابتعاد"],
    "purpose": ["because", "to show", "reveal", "establish", "so that", "turning point", "climax",
                "لأن", "لإظهار", "لتأسيس", "لحظة", "نقطة تحول", "ذروة", "كشف", "ليعرف"],
}
LOCKS = ["hard lock", "medium", "soft latitude", "must", "never", "exactly", "لا تغيّر", "ثابت", "يجب", "بالضبط", "ممنوع"]
B5 = {
    "O": ("Openness", "الانفتاح", "concrete, familiar images; routine words", "metaphors, odd analogies, curious questions"),
    "C": ("Conscientiousness", "الضمير", "loose plans, trails off, late", "lists, precise times, finishes sentences"),
    "E": ("Extraversion", "الانبساط", "short replies, pauses, listens", "talks first, fast, loud, many exclamations"),
    "A": ("Agreeableness", "الوداعة", "blunt, sceptical, interrupts", "warm, hedges, thanks and apologises"),
    "N": ("Neuroticism", "العُصابية", "steady, unbothered, even tone", "worries aloud, catastrophises, quick to hurt"),
}


def load(path=DATA):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if d.get("schema") != "kosif.book.methods.v1":
        raise ValueError("unexpected schema")
    ids = [m["id"] for m in d["methods"]]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate method ids")
    src = {s["id"]: s for s in d["sources"]}
    for m in d["methods"]:
        if m["source"] not in src or m["domain"] not in DOMAINS or not m["steps"] or not m.get("check"):
            raise ValueError("bad method " + m["id"])
    return d


def resolve(d, token):
    t = token.strip().upper()
    for m in d["methods"]:
        if m["id"] == t:
            return m
    raise ValueError("unknown method " + token)


def _norm(s):
    return unicodedata.normalize("NFKC", s).casefold()


def search(d, query):
    q = _norm(query)
    terms = q.split() + [w for k, v in ALIASES.items() if k in q for w in v.split()]
    out = []
    for m in d["methods"]:
        hay = _norm(" ".join([m["id"], m["domain"], m["name_en"], m["name_ar"], m["use_when"], m.get("kosif_hook", "")] + m["steps"]))
        score = sum(hay.count(t) for t in terms if len(t) > 1)
        if score:
            out.append((score, m))
    out.sort(key=lambda x: (-x[0], x[1]["id"]))
    return [m for _, m in out]


def rest(problem, n=3, seed=None):
    if seed is None:
        seed = random.SystemRandom().randrange(10 ** 6)
    rng = random.Random(seed)
    words = rng.sample(WORDS, n)
    return {"method": "LT-02/LT-03", "seed": seed, "problem": problem, "words": words,
            "rule": "exhaust each word (10+ links) before the next; do not swap words; judge only after listing",
            "prompts": [{"word": w, "mode": k, "ar": ar, "en": en} for w in words for k, ar, en in MODES]}


def _parse_kv(s):
    out = {}
    for part in s.split(","):
        k, _, v = part.partition("=")
        if not k.strip() or not v.strip():
            raise ValueError("expected NAME=VALUE in " + s)
        out[k.strip()] = float(v)
    return out


def bayes(hyps, evidence):
    total = sum(hyps.values())
    if total <= 0 or any(p <= 0 for p in hyps.values()):
        raise ValueError("every prior must be > 0 (never rule a hypothesis out with 0)")
    post = {h: p / total for h, p in hyps.items()}
    ledger = []
    for name, like in evidence:
        if set(like) != set(post):
            raise ValueError("evidence %s must give a likelihood for every hypothesis" % name)
        prev = dict(post)
        z = sum(prev[h] * like[h] for h in prev)
        if z <= 0:
            raise ValueError("evidence %s is impossible under every hypothesis" % name)
        post = {h: prev[h] * like[h] / z for h in prev}
        row = {"evidence": name}
        for h in post:
            rest_p = 1 - prev[h]
            other = sum(prev[k] * like[k] for k in prev if k != h) / rest_p if rest_p > 0 else 0
            row[h + "_dB"] = round(10 * math.log10(like[h] / other), 2) if other > 0 and like[h] > 0 else None
        ledger.append(row)

    def db(p):
        return round(10 * math.log10(p / (1 - p)), 2) if 0 < p < 1 else None
    return {"method": "BY-01/BY-02", "posterior": {h: round(p, 6) for h, p in post.items()},
            "evidence_dB": {h: db(p) for h, p in post.items()}, "ledger": ledger}


def clarity(text):
    low = _norm(text)
    hollow = sorted({w for w in HOLLOW if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", low)})
    slots = {k: any(w in low for w in v) for k, v in CONTEXT.items()}
    words = len(low.split())
    c = 10 - 2 * len(hollow) - (3 if words < 8 else 0) - (2 if words > 180 else 0)
    ctx = 2 * sum(slots.values())
    nums = len(re.findall(r"\d", low))
    locks = sum(1 for w in LOCKS if w in low)
    sp = min(10, 3 + min(nums, 3) + 2 * min(locks, 2) + (2 if words >= 25 else 0))
    c, sp = max(0, c), max(0, sp)
    go = c >= 8 and ctx >= 8 and sp >= 7
    fixes = (["replace hollow words: " + ", ".join(hollow)] if hollow else []) + \
            ["add " + k for k, v in slots.items() if not v] + \
            (["mark HARD LOCK / MEDIUM / SOFT LATITUDE or give exact values"] if sp < 7 else [])
    return {"method": "KV-02", "clarity": c, "context": ctx, "specificity": sp, "context_slots": slots,
            "hollow_words": hollow, "verdict": "GENERATE" if go else "REVISE", "fixes": fixes,
            "note": "heuristic word-list score; a human read decides"}


def _minor(v, where):
    if isinstance(v, float):
        raise ValueError(where + ": amounts must be strings or integers, never floats")
    try:
        q = Decimal(str(v))
    except InvalidOperation:
        raise ValueError(where + ": not a number: %r" % (v,))
    m = q * 100
    if m != m.to_integral_value():
        raise ValueError(where + ": more than 2 decimals: %s" % v)
    return int(m)


def ledger(entries, revenue=None, receivable=None, chart=None):
    errors, warnings, keys, invoices = [], [], {}, []
    for e in entries:
        eid = e.get("id", "?")
        dr = cr = 0
        for i, ln in enumerate(e.get("lines", [])):
            if chart is not None and ln.get("account") not in chart:
                errors.append("%s line %d: account %s is not in the chart" % (eid, i, ln.get("account")))
            dr += _minor(ln.get("debit", 0), "%s line %d" % (eid, i))
            cr += _minor(ln.get("credit", 0), "%s line %d" % (eid, i))
        if dr != cr or dr == 0:
            errors.append("%s: unbalanced or empty (debit %d, credit %d minor units)" % (eid, dr, cr))
        vat = e.get("vat")
        if vat:
            net, tax = _minor(vat["net"], eid + " vat.net"), _minor(vat["tax"], eid + " vat.tax")
            want = (Decimal(net) * Decimal(str(vat["rate"]))).quantize(Decimal(1), rounding="ROUND_HALF_UP")
            if tax != int(want):
                errors.append("%s: VAT %d != net x rate %d (minor units)" % (eid, tax, want))
        key = e.get("event_key")
        if key:
            if key in keys:
                errors.append("%s: duplicate event key %s (already %s)" % (eid, key, keys[key]))
            keys.setdefault(key, eid)
        rev_cr = sum(_minor(ln.get("credit", 0), eid) for ln in e.get("lines", []) if revenue and ln.get("account") == revenue)
        if e.get("source") == "invoice" and receivable:
            invoices.append((e.get("party"), sum(_minor(ln.get("debit", 0), eid) for ln in e["lines"] if ln.get("account") == receivable), eid))
        if e.get("source") == "bank" and rev_cr:
            match = [i for p, amt, i in invoices if p == e.get("party") and amt == dr]
            (errors if match else warnings).append(
                "%s: bank movement credited to revenue %s; %s" % (eid, revenue,
                "it matches invoice %s, so it is a settlement (credit receivable), not new revenue" % match[0]
                if match else "establish its nature before treating it as revenue"))
    return {"method": "AC-03..AC-06", "entries": len(entries), "errors": errors, "warnings": warnings,
            "ok": not errors, "note": "draft check only; posting needs approval, privilege and an idempotency key"}


def persona(name, scores):
    for k, v in scores.items():
        if k not in B5 or not 1 <= v <= 5:
            raise ValueError("big5 needs O,C,E,A,N each 1-5")
    rules = []
    for k in "OCEAN":
        v = scores.get(k, 3)
        en, ar, lo, hi = B5[k]
        rules.append({"trait": en, "ar": ar, "score": v,
                      "speech": hi if v >= 4 else lo if v <= 2 else "mixed; choose per scene, keep it consistent"})
    return {"method": "PS-01..PS-06", "name": name, "hard_lock": "trait profile fixed across scenes", "speech_rules": rules,
            "if_then": ["if <situation 1>, then <behaviour>", "if <situation 2>, then <contrasting behaviour>",
                        "if <situation 3>, then <behaviour that reveals the core fear>"],
            "arc": {"type": "redemption | contamination", "turn_scene": "<one concrete scene>",
                    "theme": "agency | communion"},
            "motivation": {"goal": "<approach>", "fear": "<avoidance>", "collision": "<the moment both apply>"},
            "attachment_to_others": "secure | anxious | avoidant",
            "guard": "fiction and tone only; never score or diagnose a real person (PS-07)"}


def _print(x):
    print(json.dumps(x, ensure_ascii=False, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="book_methods.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sources")
    p = sub.add_parser("list")
    p.add_argument("--domain", choices=sorted(DOMAINS))
    p = sub.add_parser("search")
    p.add_argument("query")
    p = sub.add_parser("show")
    p.add_argument("id")
    p = sub.add_parser("rest")
    p.add_argument("--problem", required=True)
    p.add_argument("--words", type=int, default=3)
    p.add_argument("--seed", type=int)
    p = sub.add_parser("bayes")
    p.add_argument("--h", action="append", required=True, help="HYPOTHESIS=PRIOR")
    p.add_argument("--e", action="append", default=[], help="NAME:H1=L1,H2=L2")
    p = sub.add_parser("clarity")
    p.add_argument("text", nargs="?")
    p.add_argument("--file")
    p = sub.add_parser("ledger")
    p.add_argument("--file", required=True)
    p.add_argument("--revenue")
    p.add_argument("--receivable")
    p.add_argument("--chart", help="comma-separated valid account codes")
    p = sub.add_parser("persona")
    p.add_argument("--name", required=True)
    p.add_argument("--big5", required=True, help="O=4,C=2,E=5,A=2,N=3")
    a = ap.parse_args(argv)
    try:
        d = load()
        if a.cmd == "sources":
            _print(d["sources"])
        elif a.cmd == "list":
            _print([{"id": m["id"], "domain": m["domain"], "name_en": m["name_en"], "name_ar": m["name_ar"]}
                    for m in d["methods"] if not a.domain or m["domain"] == a.domain])
        elif a.cmd == "search":
            _print([{"id": m["id"], "name_en": m["name_en"], "name_ar": m["name_ar"]} for m in search(d, a.query)])
        elif a.cmd == "show":
            m = resolve(d, a.id)
            _print(dict(m, source_title=next(s["title"] for s in d["sources"] if s["id"] == m["source"])))
        elif a.cmd == "rest":
            if not 1 <= a.words <= 8:
                raise ValueError("--words must be 1-8")
            _print(rest(a.problem, a.words, a.seed))
        elif a.cmd == "bayes":
            hyps = {}
            for h in a.h:
                hyps.update(_parse_kv(h))
            ev = []
            for e in a.e:
                name, _, rest_ = e.partition(":")
                ev.append((name, _parse_kv(rest_)))
            _print(bayes(hyps, ev))
        elif a.cmd == "clarity":
            text = Path(a.file).read_text(encoding="utf-8") if a.file else a.text
            if not text:
                raise ValueError("give a prompt or --file")
            r = clarity(text)
            _print(r)
            return 0 if r["verdict"] == "GENERATE" else 3
        elif a.cmd == "ledger":
            entries = json.loads(Path(a.file).read_text(encoding="utf-8"))
            chart = set(a.chart.split(",")) if a.chart else None
            r = ledger(entries, a.revenue, a.receivable, chart)
            _print(r)
            return 0 if r["ok"] else 1
        elif a.cmd == "persona":
            _print(persona(a.name, {k: int(v) for k, v in _parse_kv(a.big5).items()}))
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
