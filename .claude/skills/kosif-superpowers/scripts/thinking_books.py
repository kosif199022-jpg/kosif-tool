#!/usr/bin/env python3
"""Thinking books / مكتبة كتب التفكير: methods from 40 famous books on how to think, turned into runnable scaffolds.

data/thinking_books.json holds 40 books (Kahneman, Tetlock, Pólya, de Bono, Meadows, Taleb, Minto, Klein, Rumelt,
Galef, Sagan, Ibn Khaldun, Ibn al-Haytham, al-Ghazali, ...) and 64 methods restated in our own words. Each method has
a stage (frame, diverge, converge, forecast, decide, execute, verify, communicate, learn), the situations that
trigger it (Arabic and English), steps, a check that proves it was applied, and the trap it prevents. USIP v5.8
appendix A38 wires them into the protocol's phases.

    python3 scripts/thinking_books.py list [--stage verify]          # books and their methods
    python3 scripts/thinking_books.py show TB25-1                    # one method (or a book: TB25)
    python3 scripts/thinking_books.py search "قرار مخاطرة"
    python3 scripts/thinking_books.py route "<task in the user's words>" [-n 5] [--json]
    python3 scripts/thinking_books.py stack "<task>" [--json]        # one method per stage, mapped to USIP phases
    python3 scripts/thinking_books.py debias report.md [--json]      # bias sweep of a draft; exit 3 = REVISE
    python3 scripts/thinking_books.py hats "<topic>"                 # Six Thinking Hats sequence (TB16-1)
    python3 scripts/thinking_books.py triz --improve speed --worsen quality   # contradiction → inventive principles
    python3 scripts/thinking_books.py forecast --base 0.30 --adjust "+0.10:strong team" --adjust "-0.05:new market"
    python3 scripts/thinking_books.py brier --p 0.7 --outcome 1 [--p 0.2 --outcome 0 ...]
    python3 scripts/thinking_books.py --self-test

Everything here is a scaffold to think with, not proof that thinking happened: fill it, test it, then act.
Python 3.8+ standard library only, deterministic.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
DATA = SK / "data" / "thinking_books.json"
STAGE_ORDER = ["frame", "diverge", "converge", "forecast", "decide", "execute", "verify", "communicate", "learn"]
USIP_PHASE = {
    "frame": "Phase 1 request card + Phase 2 deep read",
    "diverge": "Phase 4 brainstorm (ideas before judgement)",
    "converge": "Phase 4 critique / council",
    "forecast": "Phase 5 scoring (numbers, odds, ranges)",
    "decide": "Phase 6 plans A/B/C and the recommendation",
    "execute": "Phase 9 execution after approval",
    "verify": "Phase 7 pre-send check",
    "communicate": "Phase 7 report format",
    "learn": "after delivery: FusionForge lessons / task history",
}
DEFAULT_BY_STAGE = {"frame": "TB10-1", "diverge": "TB29-1", "converge": "TB16-1", "forecast": "TB01-1",
                    "decide": "TB27-1", "execute": "TB20-2", "verify": "TB25-1", "communicate": "TB13-1",
                    "learn": "TB06-1"}
CODE_WORDS = re.compile(r"\b(code|bug|script|api|function|refactor|repo|test|deploy)\b|كود|برمجة|سكربت|بج|دالة", re.I)

# Altshuller's 40 inventive principles (names are standard; one-line prompts are ours).
TRIZ = [
    ("1", "Segmentation", "split it into independent parts or make it modular"),
    ("2", "Taking out", "extract only the part (or property) that is needed, or remove the troublesome one"),
    ("3", "Local quality", "make each part fit its own job instead of one uniform design"),
    ("4", "Asymmetry", "break a symmetry that is not needed"),
    ("5", "Merging", "combine identical or adjacent operations in space or time"),
    ("6", "Universality", "let one element perform several functions"),
    ("7", "Nesting", "place one thing inside another (layers, progressive disclosure)"),
    ("8", "Counterweight", "compensate a load with an opposing force or context"),
    ("9", "Prior counteraction", "pre-load the opposite effect before it happens"),
    ("10", "Prior action", "do the required change (fully or partly) in advance"),
    ("11", "Beforehand cushioning", "prepare a fallback for the weak point"),
    ("12", "Equipotentiality", "remove the need to raise or lower (keep things at one level)"),
    ("13", "The other way round", "invert the action, the order, or what moves and what stays"),
    ("14", "Curvature", "replace straight with curved, linear with rotary"),
    ("15", "Dynamics", "make characteristics adjustable over time or condition"),
    ("16", "Partial or excessive action", "do slightly less or more than 100% and trim"),
    ("17", "Another dimension", "move into another axis: 2D to 3D, one layer to many, time as a dimension"),
    ("18", "Mechanical vibration", "use oscillation or rhythm"),
    ("19", "Periodic action", "replace continuous action with pulses"),
    ("20", "Continuity of useful action", "remove idle or intermittent steps"),
    ("21", "Skipping", "pass through the harmful stage very fast"),
    ("22", "Blessing in disguise", "use a harmful factor to get a positive effect"),
    ("23", "Feedback", "introduce or adjust feedback"),
    ("24", "Intermediary", "use a mediator object or process"),
    ("25", "Self-service", "make it serve or repair itself, use waste resources"),
    ("26", "Copying", "use a cheap copy, image or model instead of the original"),
    ("27", "Cheap short-living objects", "replace an expensive durable thing with many cheap disposable ones"),
    ("28", "Mechanics substitution", "replace a mechanical means with a sensory/field one (sound, light, signal)"),
    ("29", "Pneumatics and hydraulics", "use fluid or soft parts instead of rigid ones"),
    ("30", "Flexible shells and thin films", "isolate with a thin flexible layer"),
    ("31", "Porous materials", "add holes or gaps that carry something useful"),
    ("32", "Colour changes", "change colour or transparency to show state"),
    ("33", "Homogeneity", "make interacting parts of the same material or format"),
    ("34", "Discarding and recovering", "drop parts after use or restore them in operation"),
    ("35", "Parameter changes", "change state, concentration, flexibility, temperature or scale"),
    ("36", "Phase transitions", "use what happens during a change of state"),
    ("37", "Thermal expansion", "use expansion or contraction with change"),
    ("38", "Strong oxidants", "enrich the environment to accelerate the process"),
    ("39", "Inert atmosphere", "replace the normal environment with a neutral one"),
    ("40", "Composite materials", "combine materials or methods with different strengths"),
]
TRIZ_HINTS = {  # parameter keywords → principles worth trying first
    "speed": ["10", "20", "21", "5", "1"], "time": ["10", "20", "15", "19"], "quality": ["3", "23", "16", "35"],
    "cost": ["27", "26", "2", "25"], "size": ["7", "17", "2", "1"], "weight": ["2", "40", "31", "29"],
    "complexity": ["1", "2", "6", "5"], "detail": ["3", "7", "17", "15"], "file size": ["2", "35", "1", "26"],
    "attention": ["32", "19", "13", "4"], "reliability": ["11", "9", "23", "33"], "flexibility": ["15", "1", "29", "6"],
    "سرعة": ["10", "20", "21", "5"], "جودة": ["3", "23", "16", "35"], "تكلفة": ["27", "26", "2", "25"],
    "حجم": ["7", "17", "2", "1"], "تفاصيل": ["3", "7", "17", "15"], "انتباه": ["32", "19", "13", "4"],
}

DEBIAS_CHECKS = [
    # id, regex that signals the problem (or None), regex whose absence is the problem (or None), message, method
    ("certainty", r"\b(definitely|certainly|guaranteed|always works|100%|no doubt|obviously)\b|أكيد|مضمون|بالتأكيد|مستحيل|حتمًا",
     None, "certainty words with no probability: restate as a percentage and what would change it", "TB06-2"),
    ("no-alternatives", None, r"\b(option|alternative|plan [abc]|instead|or we)\b|خيار|بديل|خطة [أبجABC]|بدلًا",
     "only one option on the table: widen to three before deciding", "TB27-1"),
    ("no-disconfirm", None, r"\b(risk|could fail|downside|however|but|limitation|caveat)\b|مخاطر|خطر|لكن|عيب|قيود|حدود",
     "no risks or counter-evidence named: run a pre-mortem and the double-standard test", "TB25-1"),
    ("no-base-rate", r"\b\d{2,}(?:%|\s?percent\b|\s(?:users|views|sales|followers)\b)|\d+٪", r"\b(base rate|typical|average|median|compared|vs\.?|per)\b|متوسط|معدل|مقارنة|مقابل",
     "numbers without a denominator or comparison: add the base rate or reference class", "TB08-1"),
    ("no-sources", None, r"https?://|\[\d+\]|source|مصدر|المرجع",
     "claims with no source: cite, or mark as unverified", "TB32-1"),
    ("sunk-cost", r"already (spent|invested|built)|too late to|wasted if|صرفنا|استثمرنا كتير|خسارة نسيب", None,
     "sunk-cost reasoning: decide as if starting today", "TB03-1"),
    ("story-only", r"\b(imagine|picture this|once upon)\b|تخيل", r"\d",
     "a story with no numbers: check it survives without the narrative", "TB03-1"),
    ("answer-last", None, None, "conclusion is not in the first lines: lead with the answer (SCQA)", "TB13-1"),
]
ANSWER_WORDS = re.compile(r"\b(recommend\w*|answer|conclusion|in short|bottom line|we should|tl;dr)\b|التوصية|الخلاصة|الإجابة|باختصار|ننصح|القرار", re.I)


def load(path: Path = DATA) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    d["_books"] = {b["id"]: b for b in d["books"]}
    d["_methods"] = {m["id"]: m for m in d["methods"]}
    return d


def resolve(d: dict, ident: str):
    ident = ident.upper()
    if ident in d["_methods"]:
        return "method", d["_methods"][ident]
    if ident in d["_books"]:
        return "book", d["_books"][ident]
    raise ValueError(f"unknown id {ident}; try: thinking_books.py list")


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub("[ً-ْـ]", "", s)  # Arabic diacritics and tatweel
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")


def score_method(m: dict, book: dict, text: str) -> float:
    t = norm(text)
    s = 0.0
    for trig in m["triggers"]:
        if norm(trig) in t:
            s += 2.0 + 0.1 * len(trig.split())
    words = set(re.findall(r"[\w؀-ۿ]{4,}", t))
    blob = norm(" ".join([m["use_when"], m["name_en"], m["name_ar"], book["field"]]))
    s += 0.4 * sum(1 for w in words if w in blob)
    return round(s, 2)


def route(d: dict, task: str, n: int = 5) -> list:
    scored = sorted(((score_method(m, d["_books"][m["book"]], task), m["id"]) for m in d["methods"]),
                    key=lambda x: (-x[0], x[1]))
    out, books = [], set()
    for s, mid in scored:
        m = d["_methods"][mid]
        if s <= 0 or m["book"] in books:
            continue
        out.append(dict(m, score=s, book_title=d["_books"][m["book"]]["title"]))
        books.add(m["book"])
        if len(out) >= n:
            break
    return out


def stack(d: dict, task: str) -> list:
    rows = []
    for st in STAGE_ORDER:
        cands = sorted(((score_method(m, d["_books"][m["book"]], task), m["id"]) for m in d["methods"] if m["stage"] == st),
                       key=lambda x: (-x[0], x[1]))
        mid = cands[0][1] if cands and cands[0][0] > 0 else DEFAULT_BY_STAGE[st]
        m = d["_methods"][mid]
        rows.append({"stage": st, "usip": USIP_PHASE[st], "method": mid, "name_en": m["name_en"], "name_ar": m["name_ar"],
                     "book": d["_books"][m["book"]]["title"], "first_step": m["steps"][0], "check": m["check"],
                     "matched": bool(cands and cands[0][0] > 0)})
    if CODE_WORDS.search(task):
        rows.insert(STAGE_ORDER.index("execute"), {
            "stage": "execute", "usip": USIP_PHASE["execute"], "method": "GP-05", "name_en": "Reuse-first ladder",
            "name_ar": "سلّم إعادة الاستخدام", "book": "GitHub pulse (ponytail, mattpocock/skills)",
            "first_step": "Look for existing project code, then a platform-native feature, then an installed library; write new code last.",
            "check": "the change names what it reused; validation, errors, security and accessibility were not cut", "matched": True})
    return rows


def debias(text: str) -> list:
    issues = []
    head = "\n".join(text.strip().splitlines()[:6])
    for cid, bad, need, msg, method in DEBIAS_CHECKS:
        if cid == "answer-last":
            if len(text) > 400 and not ANSWER_WORDS.search(head):
                issues.append({"check": cid, "message": msg, "method": method})
            continue
        found_bad = re.search(bad, text, re.I) if bad else None
        has_need = re.search(need, text, re.I) if need else None
        if cid in ("no-base-rate", "story-only"):
            if found_bad and not has_need:
                issues.append({"check": cid, "message": msg, "method": method, "evidence": found_bad.group(0)})
        elif bad and found_bad:
            issues.append({"check": cid, "message": msg, "method": method, "evidence": found_bad.group(0)})
        elif need and not has_need and len(text) > 200:
            issues.append({"check": cid, "message": msg, "method": method})
    return issues


def hats(topic: str) -> list:
    seq = [("Blue", "أزرق", "What exactly are we thinking about, and in what order? Define the focus and the goal of this session."),
           ("White", "أبيض", "Facts we have, facts we lack, and how to get the missing ones."),
           ("Green", "أخضر", "At least five alternatives or new ideas, including one provocation (TB17-1)."),
           ("Yellow", "أصفر", "Why each promising idea could work; the value, with evidence."),
           ("Black", "أسود", "Why it could fail: risks, weak points, what must be true (TB25-1)."),
           ("Red", "أحمر", "One-line gut reaction per option, no justification."),
           ("Blue", "أزرق", "Summary, decision or next experiment, and who does what.")]
    return [{"hat": h, "hat_ar": ar, "prompt": f"[{topic}] {p}"} for h, ar, p in seq]


def triz(improve: str, worsen: str) -> list:
    keys = [k for k in TRIZ_HINTS if k in norm(improve) or k in norm(worsen)]
    first = []
    for k in keys:
        for p in TRIZ_HINTS[k]:
            if p not in first:
                first.append(p)
    order = first + [p for p, _, _ in TRIZ if p not in first]
    idx = {p: (n, why) for p, n, why in TRIZ}
    return [{"principle": p, "name": idx[p][0], "prompt": f"To improve {improve} without worsening {worsen}: {idx[p][1]}.",
             "suggested": p in first} for p in order]


def forecast(base: float, adjusts: list) -> dict:
    if not 0 < base < 1:
        raise ValueError("--base must be a probability strictly between 0 and 1 (outside view first, TB01-1)")
    p, steps = base, []
    for a in adjusts:
        m = re.match(r"\s*([+-]\d*\.?\d+)\s*:\s*(.+)", a)
        if not m:
            raise ValueError(f"bad --adjust {a!r}; use +0.10:reason")
        delta = float(m.group(1))
        if abs(delta) > 0.25:
            raise ValueError(f"adjustment {delta:+.2f} is larger than 0.25: inside-view stories rarely justify that; split it or find evidence")
        p = min(0.99, max(0.01, p + delta))
        steps.append({"delta": delta, "reason": m.group(2).strip(), "p": round(p, 3)})
    return {"outside_view": base, "adjustments": steps, "forecast": round(p, 3),
            "record": "write it in a forecast ledger with a date and a resolution rule (TB05-3)"}


def brier(pairs: list) -> dict:
    scores = [(p - o) ** 2 for p, o in pairs]
    return {"n": len(pairs), "brier": round(sum(scores) / len(scores), 4) if scores else None,
            "read_as": "0 = perfect, 0.25 = always saying 50%, lower is better"}


# ---------------------------------------------------------------- printing

def print_method(m: dict, d: dict):
    b = d["_books"][m["book"]]
    print(f"{m['id']}  {m['name_en']} / {m['name_ar']}   [{m['stage']}]")
    print(f"  book: {b['title']} ({b['author']}, {b['year'] if b['year'] > 0 else str(-b['year']) + ' BC (trad.)'})")
    print(f"  use when: {m['use_when']}")
    for i, s in enumerate(m["steps"], 1):
        print(f"  {i}. {s}")
    print(f"  check: {m['check']}")
    print(f"  trap:  {m['trap']}")


def self_test() -> int:
    d = load()
    ok = True

    def expect(c, msg):
        nonlocal ok
        if not c:
            ok = False
            print("FAIL", msg)
    expect(len(d["books"]) >= 40 and len(d["methods"]) >= 60, "counts")
    expect(all(m["stage"] in STAGE_ORDER for m in d["methods"]), "stages")
    expect(all(m["book"] in d["_books"] for m in d["methods"]), "book refs")
    expect(set(DEFAULT_BY_STAGE.values()) <= set(d["_methods"]), "defaults exist")
    expect(len({m["id"] for m in d["methods"]}) == len(d["methods"]), "unique ids")
    expect(route(d, "كام هياخد المشروع ده وقت؟ محتاج تقدير مدة")[0]["id"] == "TB01-1", "route estimate (Arabic)")
    expect(route(d, "write a hook and script for an explainer video")[0]["id"] == "TB36-1", "route hook")
    expect(any(r["id"] == "TB12-1" for r in route(d, "faster render but quality drops, a tradeoff", 5)), "route triz")
    st = stack(d, "fix the login bug in my script")
    expect([r["stage"] for r in st].count("execute") == 2 and any(r["method"] == "GP-05" for r in st), "code stack adds GP-05")
    expect(len(stack(d, "x")) == len(STAGE_ORDER), "stack covers stages")
    bad = "We will definitely win. Sales grew 40% and we already spent the budget so too late to stop. " * 3
    ids = {i["check"] for i in debias(bad)}
    expect({"certainty", "no-alternatives", "no-disconfirm", "no-base-rate", "sunk-cost", "no-sources"} <= ids, f"debias {ids}")
    good = ("Recommendation: plan B. Option A is cheaper but slower; the risk is churn of 5% per month vs a 3% median "
            "in similar shops [1]. Probability of hitting target ~60%; it would drop if the pilot misses 100 orders.") * 2
    expect(debias(good) == [], f"debias clean {debias(good)}")
    expect(triz("speed", "quality")[0]["suggested"] and len(triz("a", "b")) == 40, "triz")
    f = forecast(0.3, ["+0.1:team", "-0.05:market"])
    expect(f["forecast"] == 0.35, f"forecast {f}")
    try:
        forecast(0.3, ["+0.4:hype"])
        expect(False, "big adjustment refused")
    except ValueError:
        pass
    expect(brier([(0.7, 1), (0.2, 0)])["brier"] == 0.065, "brier")
    expect(len(hats("t")) == 7, "hats")
    print("self-test ok" if ok else "self-test FAILED")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    li = sub.add_parser("list")
    li.add_argument("--stage", choices=STAGE_ORDER)
    sh = sub.add_parser("show")
    sh.add_argument("id")
    se = sub.add_parser("search")
    se.add_argument("words", nargs="+")
    ro = sub.add_parser("route")
    ro.add_argument("task")
    ro.add_argument("-n", type=int, default=5)
    ro.add_argument("--json", action="store_true")
    stp = sub.add_parser("stack")
    stp.add_argument("task")
    stp.add_argument("--json", action="store_true")
    db = sub.add_parser("debias")
    db.add_argument("file", type=Path)
    db.add_argument("--json", action="store_true")
    ha = sub.add_parser("hats")
    ha.add_argument("topic")
    tr = sub.add_parser("triz")
    tr.add_argument("--improve", required=True)
    tr.add_argument("--worsen", required=True)
    tr.add_argument("-n", type=int, default=8)
    fc = sub.add_parser("forecast")
    fc.add_argument("--base", type=float, required=True)
    fc.add_argument("--adjust", action="append", default=[])
    br = sub.add_parser("brier")
    br.add_argument("--p", type=float, action="append", required=True)
    br.add_argument("--outcome", type=int, action="append", required=True)
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    d = load()
    try:
        if a.cmd == "list":
            for b in d["books"]:
                ms = [m for m in d["methods"] if m["book"] == b["id"] and (not a.stage or m["stage"] == a.stage)]
                if ms:
                    print(f"{b['id']}  {b['title']} — {b['author']}  ({b['title_ar']})")
                    for m in ms:
                        print(f"      {m['id']:<7} [{m['stage']:<11}] {m['name_en']} / {m['name_ar']}")
            return 0
        if a.cmd == "show":
            kind, obj = resolve(d, a.id)
            if kind == "method":
                print_method(obj, d)
            else:
                print(f"{obj['id']}  {obj['title']} / {obj['title_ar']} — {obj['author']}")
                print(f"  {obj['core_idea_en']}\n  {obj['core_idea_ar']}")
                for m in d["methods"]:
                    if m["book"] == obj["id"]:
                        print(f"  - {m['id']} {m['name_en']} [{m['stage']}]")
            return 0
        if a.cmd == "search":
            q = norm(" ".join(a.words))
            hits = [m for m in d["methods"] if all(w in norm(json.dumps(m, ensure_ascii=False) + json.dumps(
                d["_books"][m["book"]], ensure_ascii=False)) for w in q.split())]
            for m in hits:
                print(f"{m['id']:<7} {m['name_en']} / {m['name_ar']}  — {d['_books'][m['book']]['title']}")
            print(f"{len(hits)} match(es)")
            return 0 if hits else 1
        if a.cmd == "route":
            res = route(d, a.task, a.n)
            if a.json:
                print(json.dumps(res, ensure_ascii=False, indent=1))
            else:
                for m in res:
                    print(f"{m['score']:5.1f}  {m['id']:<7} [{m['stage']:<11}] {m['name_en']} / {m['name_ar']} — {m['book_title']}")
                    print(f"        first step: {m['steps'][0]}")
                if not res:
                    print("no trigger matched; use `stack` for the default one-per-stage set")
            return 0
        if a.cmd == "stack":
            res = stack(d, a.task)
            if a.json:
                print(json.dumps(res, ensure_ascii=False, indent=1))
            else:
                for r in res:
                    flag = "" if r["matched"] else "  (default)"
                    print(f"{r['stage']:<11} {r['method']:<7} {r['name_en']} / {r['name_ar']}{flag}")
                    print(f"            USIP: {r['usip']}\n            do: {r['first_step']}\n            proof: {r['check']}")
            return 0
        if a.cmd == "debias":
            issues = debias(a.file.read_text(encoding="utf-8"))
            if a.json:
                print(json.dumps({"issues": issues, "verdict": "REVISE" if len(issues) >= 3 else "PASS"}, ensure_ascii=False, indent=1))
            else:
                for i in issues:
                    print(f"[{i['method']}] {i['check']}: {i['message']}" + (f"  (e.g. “{i['evidence']}”)" if i.get("evidence") else ""))
                print(f"{len(issues)} issue(s) → {'REVISE' if len(issues) >= 3 else 'PASS'}")
            return 3 if len(issues) >= 3 else 0
        if a.cmd == "hats":
            for h in hats(a.topic):
                print(f"{h['hat']:<6} ({h['hat_ar']}): {h['prompt']}")
            return 0
        if a.cmd == "triz":
            for t in triz(a.improve, a.worsen)[:a.n]:
                print(f"#{t['principle']:<3} {t['name']:<30} {'*' if t['suggested'] else ' '} {t['prompt']}")
            return 0
        if a.cmd == "forecast":
            print(json.dumps(forecast(a.base, a.adjust), ensure_ascii=False, indent=1))
            return 0
        if a.cmd == "brier":
            if len(a.p) != len(a.outcome):
                raise ValueError("give one --outcome per --p")
            print(json.dumps(brier(list(zip(a.p, a.outcome))), indent=1))
            return 0
    except (ValueError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
