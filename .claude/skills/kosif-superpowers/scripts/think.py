#!/usr/bin/env python3
"""Thinking engine: turn the cognition procedures into concrete, checkable artefacts.

    python3 scripts/think.py ladder "<task>"            # pick the reasoning level the task needs (L0 recall … L6 wisdom) and its procedure
    python3 scripts/think.py frame  "<task>"            # contract: goal, reader, done-criteria, constraints, unknowns, first probe
    python3 scripts/think.py models "<problem>" [-n 5]  # rank mental models (data/mental_models.json) for this problem; print their questions and steps
    python3 scripts/think.py plan   "<goal>" [--weeks N] # backcast milestones, WBS skeleton, pre-mortem prompts, kill criteria
    python3 scripts/think.py ideas  "<seed>" [-n 12] [--seed 7]  # idea matrix: creative operators × powers from distant catalog domains
    python3 scripts/think.py decide decision.json        # weighted decision matrix + sensitivity (does the winner flip at ±1 weight?)
    python3 scripts/think.py fermi  "a*b*c" --range a=1:3 b=10:20 c=0.1:0.3   # Monte-Carlo range for a factor tree
    python3 scripts/think.py critic file.md             # anti-pattern sweep on a draft (hedges, unverifiable claims, missing numbers)

Stdlib only, deterministic with --seed. The output is a scaffold to think with, not the thinking itself: fill it, test it, then act.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import statistics
import signal
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
MODELS = SKILL / "data" / "mental_models.json"

AR = re.compile(r"[؀-ۿ]")


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[ً-ْـ]", "", s)
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


PREFIXES = ("وبال", "فال", "بال", "كال", "وال", "لل", "ال", "و", "ب", "ل", "ف")


def words(s: str) -> set:
    out = set()
    for w in re.findall(r"[\w\u0600-\u06FF]+", norm(s)):
        if len(w) < 2:
            continue
        out.add(w)
        if AR.search(w):
            for pre in PREFIXES:
                if w.startswith(pre) and len(w) - len(pre) >= 3:
                    out.add(w[len(pre):])
                    break
    return out


# ------------------------------------------------------------------ ladder
LADDER = [
    ("L0", "استرجاع / recall", "a fact, a definition, a known command",
     ["Answer from the catalog or docs", "Cite where it came from", "Badge it (lowest true)"],
     ["what is", "define", "ما هو", "ما هي", "تعريف", "command", "اسم"]),
    ("L1", "فهم / understand", "explain, summarise, translate a concept",
     ["Restate in the reader's words", "Give one concrete example", "Check one misunderstanding"],
     ["explain", "summar", "اشرح", "لخص", "وضح", "translate", "ترجم"]),
    ("L2", "تطبيق / apply", "run a known procedure to get an output",
     ["Pick the matching power (powers.py suggest)", "Check requirements (requirements.py for <ID>)", "Run, then verify the artefact"],
     ["make", "convert", "render", "اعمل", "حول", "اصنع", "نفذ", "build", "create"]),
    ("L3", "تحليل / analyse", "diagnose, compare, find causes or structure",
     ["Issue tree or five whys", "Gather evidence per branch", "Rank causes by evidence, not by vividness"],
     ["why", "cause", "compare", "analy", "debug", "لماذا", "سبب", "قارن", "حلل", "مشكلة", "bug"]),
    ("L4", "تركيب وتصميم / synthesise", "design a system, plan a project, combine parts into something new",
     ["Backcast from the goal", "Work breakdown with done-tests", "Thin end-to-end slice first"],
     ["design", "plan", "architecture", "system", "صمم", "خطة", "خطط", "نظام", "هيكل", "roadmap"]),
    ("L5", "تقييم وقرار / evaluate", "choose among options under uncertainty",
     ["Three real options + do-nothing", "Weighted matrix with sensitivity (think.py decide)", "Pre-mortem and kill criteria"],
     ["choose", "decide", "best", "which", "اختر", "قرر", "افضل", "أفضل", "ايهما", "أيهما", "should"]),
    ("L6", "إبداع وحكمة / create & judge", "original work, strategy, open-ended problems with people in them",
     ["Diverge widely (think.py ideas), then converge with criteria", "Reframe the problem twice before solving", "Model every stakeholder and the second-order effects", "Say what you do not know"],
     ["idea", "creative", "strategy", "vision", "فكرة", "ابداع", "إبداع", "استراتيجية", "رؤية", "عبقري", "جديد", "مبتكر", "innovate"]),
]


def cmd_ladder(task: str) -> int:
    w = norm(task)
    scores = []
    for i, (lvl, name, what, steps, keys) in enumerate(LADDER):
        s = sum(1 for k in keys if norm(k) in w)
        scores.append((s, i))
    best = max(scores)[1] if max(scores)[0] > 0 else 2
    # long, multi-clause tasks climb at least to L4
    if len(task.split()) > 25 and best < 4:
        best = 4
    lvl, name, what, steps, _ = LADDER[best]
    print(f"level {lvl} — {name}: {what}")
    for j, s in enumerate(steps, 1):
        print(f"  {j}. {s}")
    print("\nalways: frame the contract first (think.py frame), verify the artefact last, badge every claim.")
    if best >= 4:
        print("models worth running: " + ", ".join(m["name_en"] for m in rank_models(task, 4)))
    return 0


# ------------------------------------------------------------------ frame
def cmd_frame(task: str) -> int:
    arabic = bool(AR.search(task))
    nums = re.findall(r"\d+(?:\.\d+)?\s*(?:s|sec|ث|ثانية|ثواني|min|دقيقة|%|px|fps|k|م)?", task)
    print("# contract / العقد" if arabic else "# contract")
    print(f"request (verbatim): {task}")
    print("goal (one sentence, outcome not activity): …")
    print("reader / user: who receives it, what they already know, what they will do with it: …")
    print("done-criteria (3–7, observable): ")
    for i in range(1, 4):
        print(f"  AC{i}: … (how to check: file/frame/number/test)")
    print("constraints: " + (", ".join(nums) if nums else "… (time, size, format, budget, language)"))
    print("non-goals: …")
    print("unknowns → assumption (cheap) or question (costly fork): …")
    print("first probe (≤5 min, reduces the biggest unknown): …")
    print("powers: python3 scripts/powers.py suggest \"" + task.replace('"', "'") + "\"")
    print("requirements: python3 scripts/requirements.py plan \"" + task.replace('"', "'") + "\"")
    return 0


# ------------------------------------------------------------------ models
def load_models():
    return json.loads(MODELS.read_text(encoding="utf-8"))


def rank_models(problem: str, n: int):
    ws = words(problem)
    text = norm(problem)
    out = []
    for m in load_models():
        s = 0.0
        for t in m["triggers"]:
            nt = norm(t)
            if " " in nt:
                s += 2.0 if nt in text else 0
            elif nt in ws or any(w.startswith(nt) or nt.startswith(w) and len(w) > 3 for w in ws):
                s += 1.5
        s += 0.3 * len(ws & words(m["question"] + " " + m["name_en"]))
        out.append((s, m))
    out.sort(key=lambda x: (-x[0], x[1]["id"]))
    picked = [m for s, m in out if s > 0][:n]
    if len(picked) < n:  # always give a balanced default kit
        for mid in ("MODEL-01", "MODEL-02", "MODEL-24", "MODEL-49", "MODEL-03"):
            m = next(x for x in load_models() if x["id"] == mid)
            if m not in picked and len(picked) < n:
                picked.append(m)
    return picked


def cmd_models(problem: str, n: int, as_json: bool) -> int:
    ms = rank_models(problem, n)
    if as_json:
        print(json.dumps(ms, ensure_ascii=False, indent=1)); return 0
    for m in ms:
        print(f"{m['id']}  {m['name_en']} / {m['name_ar']}  [{m['discipline']}]")
        print(f"   ask: {m['question']}")
        for i, s in enumerate(m["steps"], 1):
            print(f"   {i}. {s}")
        print(f"   → output: {m['output']}   ✗ pitfall: {m['pitfall']}\n")
    return 0


# ------------------------------------------------------------------ plan
def cmd_plan(goal: str, weeks: int) -> int:
    print(f"# plan: {goal}\n")
    print("## end state (backcast from here)")
    print("  - what exists when done (artefacts, numbers, who uses it): …")
    print("  - evidence it works (the check you will run): …\n")
    print("## milestones (reverse order of preconditions, then read top→down)")
    span = max(1, weeks)
    marks = sorted({max(1, round(span * f)) for f in (0.15, 0.4, 0.7, 1.0)})
    labels = ["thin end-to-end slice shown to the user", "core path complete + tests", "edge cases, polish, docs", "delivery + verification receipt"]
    for wk, lab in zip(marks, labels[-len(marks):]):
        print(f"  - week {wk}: {lab} — done-test: …")
    print("\n## work breakdown (deliverables → tasks ≤ a few hours, each with a done-test)")
    print("  D1 …  → T1.1 … (test: …)  T1.2 …")
    print("  D2 …  → T2.1 …")
    print("\n## critical path: tasks whose delay moves the finish date → protect them; parallelise the rest")
    print("\n## pre-mortem: it failed — the top causes were:")
    for c in ("requirement missing on the machine (run requirements.py plan)", "misread the user's goal (confirm the contract)",
              "quality bar unmeasured (define the numeric check)", "scope creep (non-goals list)", "single point of failure (tool, key, person)"):
        print(f"  - {c} → mitigation: … · early signal: …")
    print("\n## kill / pivot criteria: stop or change course if <signal> by <date>: …")
    print("## first action in the next 10 minutes: …")
    return 0


# ------------------------------------------------------------------ ideas
OPERATORS = [
    ("Invert", "اقلب", "do the opposite of the convention"),
    ("Fuse", "ادمج", "combine with the picked power from another domain"),
    ("Constrain", "قيّد", "add one hard limit (3 s, one colour, no words)"),
    ("Exaggerate", "ضخّم", "10× one property"),
    ("Minimise", "صغّر", "0.1× — what is left when almost everything is removed?"),
    ("Swap audience", "بدّل الجمهور", "make it for a child, an expert, a blind user"),
    ("Transplant", "انقل", "borrow the mechanism of a distant field"),
    ("Personify", "شخصن", "give the object a voice or a goal"),
    ("Time-shift", "زمن آخر", "set it 100 years earlier or later"),
    ("Interactive", "تفاعلي", "let the viewer change the outcome"),
    ("Data-driven", "بالبيانات", "drive the form by a real number"),
    ("Arabic-first", "عربي أولًا", "start from Arabic letterforms, calligraphy or idiom"),
]


def cmd_ideas(seed_text: str, n: int, seed: int) -> int:
    sys.path.insert(0, str(HERE))
    import powers as P  # noqa: E402
    pw = P.load_powers()
    rng = random.Random(seed)
    by_dom = {}
    for p in pw:
        by_dom.setdefault(p.get("domain") or P.DEFAULT_DOMAIN, []).append(p)
    doms = sorted(by_dom)
    print(f"# idea matrix for: {seed_text}  (seed {seed}; change --seed for a new spread)\n")
    rows = []
    try:
        styles = P.load_styles()
    except Exception:
        styles = []
    near = [p for _s, p in P.suggest(pw, styles, seed_text, max(6, n))["picked"]]
    near_doms = {p.get("domain") for p in near}
    far_doms = [d for d in doms if d not in near_doms] or doms
    for i in range(n):
        op = OPERATORS[i % len(OPERATORS)] if i < len(OPERATORS) else rng.choice(OPERATORS)
        if i % 2 == 0 and near:          # even rows: a power that fits the brief
            pick = near[(i // 2) % len(near)]; dom = pick.get("domain") or P.DEFAULT_DOMAIN
        else:                            # odd rows: a distant domain, for real cross-over
            dom = far_doms[(i * 7 + seed) % len(far_doms)]
            pick = rng.choice(by_dom[dom])
        rows.append((op, dom, pick))
        print(f"{i + 1:2d}. {op[0]} / {op[1]} — {op[2]}")
        print(f"    + {pick['id']} ({dom}) {pick.get('name_en', '')[:80]}")
        print(f"    idea: …   novelty 1–5: …   feasibility 1–5: …   requires: {', '.join(pick.get('requires') or []) or '—'}\n")
    print("converge: keep the top 3 by novelty × feasibility; for each, write the one-line pitch and the first slice.")
    return 0


# ------------------------------------------------------------------ decide
def decide(spec: dict) -> dict:
    crit = spec["criteria"]          # {"impact": 3, "cost": -2}
    scores = spec["scores"]          # {"A": {"impact": 4, "cost": 2}, ...}
    def total(weights):
        return {o: sum(weights[c] * float(s.get(c, 0)) for c in weights) for o, s in scores.items()}
    base = total(crit)
    winner = max(base, key=base.get)
    flips = []
    for c in crit:
        for d in (-1, 1):
            w = dict(crit); w[c] = crit[c] + d
            t = total(w); win = max(t, key=t.get)
            if win != winner:
                flips.append({"criterion": c, "delta": d, "new_winner": win})
    ranked = sorted(base.items(), key=lambda kv: -kv[1])
    margin = ranked[0][1] - ranked[1][1] if len(ranked) > 1 else None
    return {"totals": base, "winner": winner, "margin": margin, "robust": not flips, "flips": flips}


def cmd_decide(path: str) -> int:
    spec = json.loads(Path(path).read_text(encoding="utf-8"))
    r = decide(spec)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    if not r["robust"]:
        print("\n⚠ the winner flips under a ±1 weight change: the choice depends on these weights — confirm them with the user or gather evidence.", file=sys.stderr)
    return 0


# ------------------------------------------------------------------ fermi
def cmd_fermi(expr: str, ranges: list, n: int, seed: int) -> int:
    rng = random.Random(seed)
    bounds = {}
    for r in ranges:
        k, v = r.split("=", 1); lo, hi = (float(x) for x in v.split(":"))
        bounds[k] = (lo, hi)
    names = set(re.findall(r"[A-Za-z_]\w*", expr))
    missing = names - set(bounds)
    if missing:
        print(f"missing --range for {sorted(missing)}"); return 2
    if not re.fullmatch(r"[\w\s\.\*\+\-/\(\)]+", expr):
        print("expression may only use names, numbers and + - * / ( )"); return 2
    vals = []
    import math
    for _ in range(n):
        env = {}
        for k, (lo, hi) in bounds.items():
            env[k] = math.exp(rng.uniform(math.log(lo), math.log(hi))) if lo > 0 else rng.uniform(lo, hi)
        vals.append(eval(expr, {"__builtins__": {}}, env))  # noqa: S307 - validated arithmetic only
    vals.sort()
    q = lambda p: vals[int(p * (len(vals) - 1))]
    print(json.dumps({"expr": expr, "p10": q(0.10), "p50": q(0.50), "p90": q(0.90), "mean": statistics.fmean(vals), "samples": n}, indent=1))
    return 0


# ------------------------------------------------------------------ critic
CRITIC = [
    (r"\b(very|really|extremely|incredibly|super)\b|جدا|للغاية", "intensifier — replace with a number or cut"),
    (r"\b(should work|probably fine|seems to|I think)\b|غالبا|ربما يعمل", "unverified claim — test it or badge it"),
    (r"\b(best|perfect|guaranteed|always|never)\b|الأفضل|مضمون|دائما|أبدا", "absolute — needs evidence or softer, calibrated wording"),
    (r"\b(etc|and so on)\b|إلخ|وغيرها", "vague list — name the items or cut"),
    (r"\b(leverage|utilize|robust|seamless|cutting-edge|delve)\b", "AI-tell vocabulary — say the plain thing"),
    (r"\bdone\b|تم\b|انتهى", "completion claim — attach the check that proves it"),
]


def cmd_critic(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    hits = 0
    for i, line in enumerate(text.splitlines(), 1):
        for pat, why in CRITIC:
            for m in re.finditer(pat, line, re.I):
                hits += 1
                print(f"{path}:{i}: '{m.group(0)}' — {why}")
    nums = len(re.findall(r"\d", text))
    print(f"\n{hits} flag(s); digits in text: {nums}" + (" — no numbers at all: is anything measurable?" if nums == 0 else ""))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ladder").add_argument("task")
    sub.add_parser("frame").add_argument("task")
    m = sub.add_parser("models"); m.add_argument("problem"); m.add_argument("-n", type=int, default=5); m.add_argument("--json", action="store_true")
    p = sub.add_parser("plan"); p.add_argument("goal"); p.add_argument("--weeks", type=int, default=4)
    i = sub.add_parser("ideas"); i.add_argument("seed_text"); i.add_argument("-n", type=int, default=12); i.add_argument("--seed", type=int, default=7)
    sub.add_parser("decide").add_argument("path")
    f = sub.add_parser("fermi"); f.add_argument("expr"); f.add_argument("--range", nargs="+", default=[]); f.add_argument("--samples", type=int, default=20000); f.add_argument("--seed", type=int, default=7)
    sub.add_parser("critic").add_argument("path")
    a = ap.parse_args(argv)
    if a.cmd == "ladder": return cmd_ladder(a.task)
    if a.cmd == "frame": return cmd_frame(a.task)
    if a.cmd == "models": return cmd_models(a.problem, a.n, a.json)
    if a.cmd == "plan": return cmd_plan(a.goal, a.weeks)
    if a.cmd == "ideas": return cmd_ideas(a.seed_text, a.n, a.seed)
    if a.cmd == "decide": return cmd_decide(a.path)
    if a.cmd == "fermi": return cmd_fermi(a.expr, a.range, a.samples, a.seed)
    return cmd_critic(a.path)


if __name__ == "__main__":
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
