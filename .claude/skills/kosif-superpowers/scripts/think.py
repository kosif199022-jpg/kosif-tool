#!/usr/bin/env python3
"""Thinking engine: turn the cognition procedures into concrete, checkable artefacts.

    python3 scripts/think.py ladder "<task>"            # pick the reasoning level the task needs (L0 recall … L6 wisdom) and its procedure
    python3 scripts/think.py frame  "<task>"            # contract: goal, reader, done-criteria, constraints, unknowns, first probe
    python3 scripts/think.py models "<problem>" [-n 5] [--plain]  # rank mental models (data/mental_models.json): diverse disciplines, question + do-now step + misuse warning
    python3 scripts/think.py plan   "<goal>" [--weeks N] # backcast milestones, WBS skeleton, pre-mortem prompts, kill criteria
    python3 scripts/think.py ideas  "<seed>" [-n 12] [--seed 7]  # idea matrix: creative operators × powers from distant catalog domains
    python3 scripts/think.py decide decision.json        # weighted decision matrix + sensitivity (does the winner flip at ±1 weight?)
    python3 scripts/think.py fermi  "a*b*c" --range a=1:3 b=10:20 c=0.1:0.3   # Monte-Carlo range for a factor tree
    python3 scripts/think.py critic file.md             # anti-pattern sweep on a draft (hedges, unverifiable claims, missing numbers)
    python3 scripts/think.py modes  "<task>" [-n 3]     # rank reasoning modes (data/reasoning_modes.json): procedure, trap, check
    python3 scripts/think.py bayes  --prior 0.2 --lr "tests fail on main=4" "only one report=0.5" [--threshold 0.7]
                                                        # Bayesian update by likelihood ratios + sensitivity (or --json spec.json)
    python3 scripts/think.py gate   gate.json           # decision gate: GO / PIVOT / KILL / HOLD from pre-written thresholds
    python3 scripts/think.py audit  report.md [--strict] # self-audit: claim → evidence ledger + calibration questions
    python3 scripts/think.py intake "<request>" [--level L2]  # deliverable kind, filled / assumed / asked / blocking slots (A25)
    python3 scripts/think.py decompose plan.json         # task DAG check: order, critical path range, one-way doors (A26)
    python3 scripts/think.py qa [<kind>] [--answers a.json]   # quality bar per deliverable kind; PASS / FAIL / INCOMPLETE (A27)
    python3 scripts/think.py recover [<class>] [--attempts N] [--message "<error>"]   # recovery ladder (A29)
    python3 scripts/think.py pro "<task>" [--depth standard|deep|max] [--json]   # Pro intelligence passes + fitted council + modes + models (A30)

Stdlib only, deterministic with --seed. The output is a scaffold to think with, not the thinking itself: fill it, test it, then act.
"""
from __future__ import annotations

import argparse
import ast
import json
import operator
import random
import re
import statistics
import signal
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
MODELS = SKILL / "data" / "mental_models.json"
MODES = SKILL / "data" / "reasoning_modes.json"
INTEL = SKILL / "data" / "usip_intelligence.json"

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
# Cues that make the two "always worth it" lenses relevant: Inversion for anything that can fail, second-order effects for
# anything that changes a system, a policy or people. They are reserved a slot when the problem shows the cue.
INVERSION_ID, SECOND_ORDER_ID = "MODEL-02", "MODEL-03"
DECISION_CUES = ("decide", "choose", "should", "launch", "plan", "strategy", "risk", "fail", "commit", "invest", "migrate", "bet",
                 "قرار", "قرر", "اختر", "اختيار", "خطة", "خطط", "اطلاق", "إطلاق", "مخاطر", "فشل", "استراتيجية", "نستثمر", "ايهما", "أيهما")
CHANGE_CUES = ("change", "policy", "price", "pricing", "launch", "strategy", "team", "users", "market", "growth", "remove", "migrate",
               "تغيير", "سياسة", "سعر", "تسعير", "اطلاق", "إطلاق", "فريق", "مستخدم", "سوق", "نمو", "حذف", "استراتيجية", "عملاء")
DEFAULT_KIT = ("MODEL-01", "MODEL-02", "MODEL-24", "MODEL-49", "MODEL-03")


def load_models():
    return json.loads(MODELS.read_text(encoding="utf-8"))


def _score_models(problem: str, models: list) -> list:
    """(score, matched triggers, model) for every model; deterministic."""
    ws = words(problem)
    text = norm(problem)
    out = []
    for m in models:
        s, hit = 0.0, []
        for t in m["triggers"]:
            nt = norm(t)
            if " " in nt:
                if nt in text:
                    s += 2.0; hit.append(t)
            elif nt in ws or any(w.startswith(nt) or nt.startswith(w) and len(w) > 3 for w in ws):
                s += 1.5; hit.append(t)
        s += 0.3 * len(ws & words(m["question"] + " " + m["name_en"]))
        out.append((round(s, 2), hit, m))
    out.sort(key=lambda x: (-x[0], x[2]["id"]))
    return out


def _has_cue(problem: str, cues) -> bool:
    text, ws = norm(problem), words(problem)
    return any((norm(c) in text) if " " in c else (norm(c) in ws or any(w.startswith(norm(c)) for w in ws if len(norm(c)) > 3))
               for c in cues)


def rank_models(problem: str, n: int, diverse: bool = True, exclude=()):
    """The n most fitting models. diverse=True: at most one model per discipline (two only when the matches run out),
    Inversion and Second-order effects get a reserved slot when the problem shows a decision/failure or a change cue,
    and the balanced default kit fills what is left. diverse=False keeps the plain score order (the v1 behaviour)."""
    models = [m for m in load_models() if m["id"] not in set(exclude)]
    byid = {m["id"]: m for m in models}
    scored = _score_models(problem, models)
    info = {m["id"]: (s, hit) for s, hit, m in scored}
    relevant = [m for s, _h, m in scored if s > 0]
    if not diverse:
        picked = relevant[:n]
    else:
        reserve = []
        if n >= 3 and _has_cue(problem, DECISION_CUES) and INVERSION_ID in byid:
            reserve.append(INVERSION_ID)
        if n >= 4 and _has_cue(problem, CHANGE_CUES) and SECOND_ORDER_ID in byid:
            reserve.append(SECOND_ORDER_ID)
        picked, per = [], {}
        for cap in (1, 2):  # first pass: one per discipline; second pass: allow a second one
            for m in relevant:
                if len(picked) >= n - sum(1 for r in reserve if byid[r] not in picked):
                    break
                if m in picked or m["id"] in reserve or per.get(m["discipline"], 0) >= cap:
                    continue
                if cap == 1 and not info[m["id"]][1]:
                    continue  # the one-per-discipline pass takes trigger matches only, not a shared word in the question
                picked.append(m); per[m["discipline"]] = per.get(m["discipline"], 0) + 1
        for r in reserve:
            if byid[r] not in picked and len(picked) < n:
                picked.append(byid[r])
        picked.sort(key=lambda m: (-info[m["id"]][0], m["id"]))
    if len(picked) < n:  # always give a balanced default kit
        for mid in DEFAULT_KIT:
            m = byid.get(mid)
            if m and m not in picked and len(picked) < n:
                picked.append(m)
    for m in models:  # still short (a large n or an exclude list): the next models by score, diverse first
        if len(picked) >= n:
            break
        if m not in picked and (not diverse or m["discipline"] not in {x["discipline"] for x in picked}):
            picked.append(m)
    for _s, _h, m in scored:
        if len(picked) >= n:
            break
        if m not in picked:
            picked.append(m)
    return picked[:n]


def lens(m: dict, problem: str = "") -> dict:
    """A model as a usable lens: the concrete question, one action step, the output, and a misuse warning."""
    s, hit = (_score_models(problem, [m])[0][:2] if problem else (0.0, []))
    return {"id": m["id"], "name_en": m["name_en"], "name_ar": m["name_ar"], "discipline": m["discipline"],
            "question": m["question"], "action": m["steps"][0], "output": m["output"],
            "misuse": f"Misuse warning: {m['pitfall']}",
            "score": s, "matched": hit,
            "why": ("matched: " + ", ".join(hit)) if hit else ("reserved lens" if problem and _reserved(m["id"], problem)
                                                             else "related wording" if s > 0 else "default kit")}


def _reserved(mid: str, problem: str) -> bool:
    return ((mid == INVERSION_ID and _has_cue(problem, DECISION_CUES)) or (mid == SECOND_ORDER_ID and _has_cue(problem, CHANGE_CUES)))


def lenses(problem: str, n: int = 5, exclude=()) -> list:
    return [lens(m, problem) for m in rank_models(problem, n, exclude=exclude)]


def cmd_models(problem: str, n: int, as_json: bool, plain: bool = False) -> int:
    ms = rank_models(problem, n, diverse=not plain)
    if as_json:
        print(json.dumps([dict(m, lens=lens(m, problem)) for m in ms], ensure_ascii=False, indent=1)); return 0
    for m in ms:
        L = lens(m, problem)
        print(f"{m['id']}  {m['name_en']} / {m['name_ar']}  [{m['discipline']}]  ({L['why']})")
        print(f"   ask: {m['question']}")
        for i, s in enumerate(m["steps"], 1):
            print(f"   {i}. {s}")
        print(f"   ▶ do now: {L['action']}")
        print(f"   → output: {m['output']}")
        print(f"   ⚠ {L['misuse']}\n")
    if not plain:
        cats = sorted({m["discipline"] for m in ms})
        print(f"disciplines covered: {len(cats)} ({', '.join(cats)})")
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
_ARITH_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow}
_ARITH_UN = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _arith_tree(expr: str):
    """Parse an arithmetic expression and refuse anything else (attributes, calls, subscripts …)."""
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"not an expression ({exc.msg})") from None
    for node in ast.walk(tree):
        if isinstance(node, (ast.Expression, ast.Name, ast.Load)) or type(node) in _ARITH_BIN or type(node) in _ARITH_UN:
            continue
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            continue
        if isinstance(node, (ast.BinOp, ast.UnaryOp)):
            continue
        raise ValueError(f"{type(node).__name__} is not allowed")
    return tree


def _arith_eval(node, env: dict) -> float:
    """Evaluate a tree from _arith_tree with plain numbers; no eval(), no builtins, no attribute access."""
    if isinstance(node, ast.Expression):
        return _arith_eval(node.body, env)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, ast.BinOp):
        return _ARITH_BIN[type(node.op)](_arith_eval(node.left, env), _arith_eval(node.right, env))
    if isinstance(node, ast.UnaryOp):
        return _ARITH_UN[type(node.op)](_arith_eval(node.operand, env))
    raise ValueError(f"{type(node).__name__} is not allowed")


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
    try:
        tree = _arith_tree(expr)
    except ValueError as exc:
        print(f"expression may only use names, numbers and + - * / ** ( ): {exc}"); return 2
    vals = []
    import math
    for _ in range(n):
        env = {}
        for k, (lo, hi) in bounds.items():
            env[k] = math.exp(rng.uniform(math.log(lo), math.log(hi))) if lo > 0 else rng.uniform(lo, hi)
        vals.append(_arith_eval(tree, env))
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
    for i, raw in enumerate(text.splitlines(), 1):
        line = re.sub("[\u064B-\u0652\u0640]", "", raw)  # جدًا → جدا, دائمًا → دائما: tanween and tatweel never hide a flag
        for pat, why in CRITIC:
            for m in re.finditer(pat, line, re.I):
                hits += 1
                print(f"{path}:{i}: '{m.group(0)}' — {why}")
    nums = len(re.findall(r"\d", text))
    print(f"\n{hits} flag(s); digits in text: {nums}" + (" — no numbers at all: is anything measurable?" if nums == 0 else ""))
    return 0


# ------------------------------------------------------------------ modes (USIP v5.4, appendix A24)
def rank_modes(task: str, n: int) -> list:
    ws, text = words(task), norm(task)
    out = []
    for m in json.loads(MODES.read_text(encoding="utf-8"))["modes"]:
        s = 0.0
        for k in m["keywords"]:
            nk = norm(k)
            if " " in nk or "/" in nk:
                s += 2.0 if nk in text else 0
            elif nk in ws or any(len(w) > 3 and len(nk) > 3 and (w.startswith(nk) or nk.startswith(w)) for w in ws):
                s += 1.5
        out.append((s, m))
    out.sort(key=lambda x: -x[0])   # stable: ties keep the file order
    picked = [m for s, m in out if s > 0][:n]
    for mid in ("abductive", "causal", "bayesian"):   # a balanced default when the words say little
        if len(picked) >= n:
            break
        m = next(x for _s, x in out if x["id"] == mid)
        if m not in picked:
            picked.append(m)
    return picked


def cmd_modes(task: str, n: int, as_json: bool) -> int:
    ms = rank_modes(task, n)
    if as_json:
        print(json.dumps(ms, ensure_ascii=False, indent=1)); return 0
    for m in ms:
        print(f"{m['id']}  {m['en']} / {m['ar']} — {m['use_when']}")
        for i, st in enumerate(m["procedure"], 1):
            print(f"   {i}. {st}")
        print(f"   ✗ trap: {m['trap']}\n   ✓ check: {m['check']}\n")
    print("Use at most two modes per decision (A24); the ranking is a keyword hint, the choice is yours.")
    return 0


# ------------------------------------------------------------------ bayes
def _prob(x, name: str) -> float:
    v = float(x)
    if not 0.0 < v < 1.0:
        raise ValueError(f"{name} must be strictly between 0 and 1, got {x}")
    return v


def bayes_binary(prior: float, lrs: list, threshold=None) -> dict:
    """prior P(H), lrs [(name, P(E|H)/P(E|¬H))] → posterior with per-item log-odds and a halve/double sensitivity."""
    import math
    prior = _prob(prior, "prior")
    steps, odds = [], prior / (1 - prior)
    for name, lr in lrs:
        lr = float(lr)
        if lr <= 0:
            raise ValueError(f"likelihood ratio for {name!r} must be > 0")
        odds *= lr
        steps.append({"evidence": name, "lr": lr, "bits": round(math.log2(lr), 3), "posterior": round(odds / (1 + odds), 4)})
    post = odds / (1 + odds)
    def post_with(i, f):
        o = prior / (1 - prior)
        for j, (_n, lr) in enumerate(lrs):
            o *= float(lr) * (f if j == i else 1)
        return o / (1 + o)
    sens = [{"evidence": n, "if_halved": round(post_with(i, 0.5), 4), "if_doubled": round(post_with(i, 2), 4)} for i, (n, _l) in enumerate(lrs)]
    r = {"mode": "binary", "prior": prior, "steps": steps, "posterior": round(post, 4), "sensitivity": sens}
    if threshold is not None:
        t = _prob(threshold, "threshold")
        r["threshold"] = t
        r["decision"] = "ACT" if post >= t else "DO_NOT_ACT"
        r["flips"] = [s["evidence"] for s in sens if (s["if_halved"] >= t) != (post >= t) or (s["if_doubled"] >= t) != (post >= t)]
        r["robust"] = not r["flips"]
    return r


def bayes_multi(priors: dict, evidence: list) -> dict:
    """priors {H: p} (normalised), evidence [{"name", "likelihood": {H: P(E|H)}}] → posterior per hypothesis."""
    tot = sum(float(v) for v in priors.values())
    if tot <= 0:
        raise ValueError("priors must sum to more than 0")
    cur = {h: float(v) / tot for h, v in priors.items()}
    steps = []
    for e in evidence:
        lk = e["likelihood"]
        missing = [h for h in cur if h not in lk]
        if missing:
            raise ValueError(f"evidence {e.get('name')!r} has no likelihood for {', '.join(missing)}")
        z = sum(cur[h] * float(lk[h]) for h in cur)
        if z <= 0:
            raise ValueError(f"evidence {e.get('name')!r} is impossible under every hypothesis")
        cur = {h: cur[h] * float(lk[h]) / z for h in cur}
        steps.append({"evidence": e.get("name", "?"), "posterior": {h: round(v, 4) for h, v in cur.items()}})
    best = max(cur, key=cur.get)
    ranked = sorted(cur.values(), reverse=True)
    return {"mode": "multi", "priors": {h: round(float(v) / tot, 4) for h, v in priors.items()}, "steps": steps,
            "posterior": {h: round(v, 4) for h, v in cur.items()}, "leader": best,
            "margin": round(ranked[0] - ranked[1], 4) if len(ranked) > 1 else None}


def cmd_bayes(prior, lr_items: list, threshold, spec_path) -> int:
    try:
        if spec_path:
            spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
            if "priors" in spec:
                r = bayes_multi(spec["priors"], spec.get("evidence", []))
            else:
                r = bayes_binary(spec["prior"], [(e["name"], e["lr"]) for e in spec.get("evidence", [])], spec.get("threshold"))
        else:
            if prior is None:
                raise ValueError("give --prior (binary) or --json spec.json")
            lrs = []
            for it in lr_items:
                name, _, val = it.rpartition("=")
                if not name:
                    raise ValueError(f"--lr item {it!r} must be NAME=RATIO")
                lrs.append((name.strip(), float(val)))
            r = bayes_binary(prior, lrs, threshold)
    except (ValueError, KeyError) as e:
        print(f"think.py bayes: {e}", file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=1))
    if r.get("robust") is False:
        print(f"\n⚠ the decision flips if {', '.join(r['flips'])} is halved or doubled: get better evidence on it before acting.", file=sys.stderr)
    return 0


# ------------------------------------------------------------------ gate
GATE_OPS = {"<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "==": operator.eq, "!=": operator.ne}
GATE_TEMPLATE = {
    "decision": "ship the reorganised skill layout",
    "reversible": True,
    "go": [{"name": "check_skill errors", "op": "==", "threshold": 0, "observed": None},
           {"name": "protocol tests failing", "op": "==", "threshold": 0, "observed": None}],
    "pivot": [{"name": "files without a section", "op": ">", "threshold": 0, "observed": None}],
    "kill": [{"name": "links broken by the move", "op": ">", "threshold": 20, "observed": None}],
}


def _gate_rows(rows: list) -> list:
    out = []
    for c in rows:
        op = c.get("op", ">=")
        if op not in GATE_OPS:
            raise ValueError(f"criterion {c.get('name')!r}: unknown op {op!r}")
        obs = c.get("observed")
        met = None if obs is None else bool(GATE_OPS[op](float(obs), float(c["threshold"])))
        out.append({"name": c.get("name", "?"), "rule": f"{op} {c['threshold']}", "observed": obs, "met": met})
    return out


def gate(spec: dict) -> dict:
    """Pre-written thresholds → verdict. KILL beats PIVOT beats GO; any unobserved go-criterion holds the gate, and an
    irreversible (one-way door) decision also holds while any criterion at all is unobserved."""
    go, pivot, kill = _gate_rows(spec.get("go", [])), _gate_rows(spec.get("pivot", [])), _gate_rows(spec.get("kill", []))
    if not go:
        raise ValueError("a gate needs at least one go criterion written before the result is known")
    reversible = bool(spec.get("reversible", True))
    unknown = [r["name"] for r in go + pivot + kill if r["met"] is None]
    if any(r["met"] for r in kill):
        verdict = "KILL"
    elif any(r["met"] for r in pivot):
        verdict = "PIVOT"
    elif any(r["met"] is None for r in go) or (not reversible and unknown):
        verdict = "HOLD"
    elif all(r["met"] for r in go):
        verdict = "GO"
    else:
        verdict = "HOLD"
    return {"decision": spec.get("decision", ""), "door": "two-way" if reversible else "one-way",
            "verdict": verdict, "unobserved": unknown, "go": go, "pivot": pivot, "kill": kill,
            "needs_explicit_approval": (not reversible) and verdict == "GO"}


def cmd_gate(path, template: bool) -> int:
    if template or not path:
        print(json.dumps(GATE_TEMPLATE, ensure_ascii=False, indent=1)); return 0
    try:
        r = gate(json.loads(Path(path).read_text(encoding="utf-8")))
    except (ValueError, KeyError) as e:
        print(f"think.py gate: {e}", file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=1))
    if r["needs_explicit_approval"]:
        print("\n⚠ one-way door: GO only means the thresholds are met; the step still needs the user's explicit permission (law 17).", file=sys.stderr)
    return 0 if r["verdict"] in ("GO", "HOLD") else 1


# ------------------------------------------------------------------ audit
CLAIM_PATTERNS = [
    (r"\d", "number"),
    (r"\b(verified|passed|works|fixed|tested|proven|complete[d]?|all|every|never|always|guaranteed)\b", "strong claim"),
    (r"(تم|نجح|يعمل|مثبت|مختبر|اكتمل|كل|جميع|أبدا|ابدا|دائما|مضمون)", "strong claim"),
    (r"\b(best|fastest|first|only|unique)\b|(أفضل|أسرع|الوحيد|الأول)", "superlative"),
]
EVIDENCE_RE = re.compile(r"`[^`]+`|\]\([^)]+\)|https?://|\b[\w./-]+\.(?:py|json|md|txt|log|mp4|csv|html)\b|\(evidence:|دليل:|←")
CALIBRATION = [
    "How confident am I in the headline result (0–100%), and what reference class is that number from?",
    "What single observation would change my mind?",
    "What is the strongest version of the opposite view (steelman), in one sentence?",
    "Which assumption did I not test, and what would a five-minute test be?",
    "What did I not open, run or measure, and does the report say so?",
]


def audit(text: str) -> dict:
    rows, fence = [], False
    for i, raw in enumerate(text.splitlines(), 1):
        if raw.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        line = re.sub("[ً-ْـ]", "", raw).strip()
        if fence or not line or line.startswith("#") or set(line) <= set("|-: "):
            continue
        kinds = sorted({k for pat, k in CLAIM_PATTERNS if re.search(pat, line, re.I)})
        if not kinds:
            continue
        rows.append({"line": i, "kinds": kinds, "evidence": bool(EVIDENCE_RE.search(line)), "text": line[:140]})
    unsupported = [r for r in rows if not r["evidence"]]
    return {"claims": len(rows), "with_evidence": len(rows) - len(unsupported), "unsupported": unsupported,
            "calibration": CALIBRATION}


def cmd_audit(path: str, strict: bool) -> int:
    r = audit(Path(path).read_text(encoding="utf-8"))
    for u in r["unsupported"]:
        print(f"{path}:{u['line']}: [{', '.join(u['kinds'])}] no evidence on the line — {u['text']}")
    print(f"\nclaims {r['claims']} · with evidence {r['with_evidence']} · unsupported {len(r['unsupported'])}")
    print("evidence = a `command`, a link, a file path, '(evidence: …)' or '← tool' on the same line")
    print("\ncalibration — answer each in the report before sending:")
    for q in r["calibration"]:
        print(f"  - {q}")
    return 1 if strict and r["unsupported"] else 0


# ------------------------------------------------------------------ intake (USIP v5.5, appendix A25)
def intel() -> dict:
    return json.loads(INTEL.read_text(encoding="utf-8"))


def detect_kinds(request: str, data: dict) -> list:
    """Deliverable kinds whose keywords occur in the request, best first; [] when none does."""
    ws, text = words(request), norm(request)
    scored = []
    for kid, k in data["kinds"].items():
        s = 0
        for kw in k["keywords"]:
            nk = norm(kw)
            if " " in nk:
                s += 2 if nk in text else 0
            elif nk in ws or (AR.search(nk) and len(nk) > 2 and any(w.startswith(nk) for w in ws)) or (not AR.search(nk) and re.search(rf"\b{re.escape(nk)}", text)):
                s += 1
        if s:
            scored.append((s, kid))
    scored.sort(key=lambda x: -x[0])   # stable: ties keep the file order
    return [kid for _s, kid in scored]


def intake(request: str, level: str = "L2", data: dict = None) -> dict:
    """Slots of the detected deliverable kind(s): filled, assumed (with default), asked (within the level's budget), blocking."""
    data = data or intel()
    level = level.upper()
    if level not in data["question_budget"]:
        raise ValueError(f"level must be one of {', '.join(data['question_budget'])}")
    budget = data["question_budget"][level]
    kinds = detect_kinds(request, data)
    text = norm(request)
    sensitive = any(norm(m) in text for m in data["safe_default_markers"])
    filled, assumed, asked, blockers = [], [], [], []
    for kid in kinds[:2]:   # a request with more deliverables gets one card per deliverable (core, stage 1)
        for s in data["kinds"][kid]["slots"]:
            row = {"kind": kid, "slot": s["id"], "ar": s["ar"], "default": s["default"]}
            if re.search(s["present"], request, re.I) or re.search(s["present"], text, re.I):
                filled.append(row)
            elif s["severity"] == "blocker":
                blockers.append(row)
            elif s["severity"] == "ask" and len(asked) < budget:
                asked.append(row)
            else:
                assumed.append(row)
    if level == "L0":
        assumed += asked
        asked = []
    return {"level": level, "kinds": kinds, "question_budget": budget, "filled": filled, "assumed": assumed,
            "questions": asked, "blockers": blockers, "sensitive": sensitive,
            "rule": "ask only what changes the result; every question carries its suggested default; a spend, publish, "
                    "personal-data or rights question gets the safe default only" + (" (sensitive words found)" if sensitive else "")}


def cmd_intake(request: str, level: str, as_json: bool) -> int:
    try:
        r = intake(request, level)
    except ValueError as e:
        print(f"think.py intake: {e}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=1)); return 0
    print(f"level {r['level']} · kinds: {', '.join(r['kinds']) or 'none detected (write the card by hand)'} · question budget {r['question_budget']}")
    for title, key in (("filled", "filled"), ("assume (write in the assumptions line)", "assumed"),
                       ("ask (inside the one report, with the suggested default)", "questions"), ("BLOCKING input", "blockers")):
        if r[key]:
            print(f"\n{title}:")
            for x in r[key]:
                print(f"  - [{x['kind']}] {x['ar']}" + ("" if key == "filled" else f" → {x['default']}"))
    if r["sensitive"]:
        print("\n⚠ sensitive step words found: the suggested default is the safe one (no spend, no publish, no sharing); the step itself needs explicit permission.")
    print(f"\n{r['rule']}")
    return 0


# ------------------------------------------------------------------ decompose (appendix A26)
DECOMPOSE_TEMPLATE = {
    "goal": "Arabic 30-second reel from the uploaded voice",
    "tasks": [
        {"id": "T1", "title": "measure the audio (duration, loudness, words)", "deps": [], "est": [0.2, 0.5], "risk": 2,
         "done": "words.json + duration known", "verify": "ffprobe + ebur128", "reversible": True},
        {"id": "T2", "title": "storyboard 6 shots", "deps": ["T1"], "est": [0.5, 1], "risk": 1,
         "done": "6 keyframes approved", "verify": "contact sheet", "reversible": True},
        {"id": "T3", "title": "build the scene and preview", "deps": ["T2"], "est": [1, 3], "risk": 2,
         "done": "5-second preview renders", "verify": "render_html --preview", "reversible": True},
        {"id": "T4", "title": "final render and QA", "deps": ["T3"], "est": [0.5, 1.5], "risk": 1,
         "done": "verify_video passes", "verify": "tools/verify_video.py", "reversible": True},
        {"id": "T5", "title": "publish to the account", "deps": ["T4"], "est": [0.1, 0.2], "risk": 1,
         "done": "posted", "verify": "post URL", "reversible": False}
    ]
}


def decompose(spec: dict) -> dict:
    """Check a task DAG and compute order, critical path (optimistic and pessimistic) and risk-first advice."""
    tasks = spec.get("tasks") or []
    if not tasks:
        raise ValueError("no tasks")
    ids = [t.get("id") for t in tasks]
    problems = []
    if len(ids) != len(set(ids)) or None in ids:
        raise ValueError("every task needs a unique id")
    by = {t["id"]: t for t in tasks}
    for t in tasks:
        for d in t.get("deps", []):
            if d not in by:
                problems.append(f"{t['id']}: depends on unknown task {d}")
        if not str(t.get("done", "")).strip():
            problems.append(f"{t['id']}: no done-criterion")
        if not str(t.get("verify", "")).strip():
            problems.append(f"{t['id']}: no verify step (how will you know it is done?)")
        est = t.get("est", [1, 1])
        if not (isinstance(est, list) and len(est) == 2 and 0 <= est[0] <= est[1]):
            problems.append(f"{t['id']}: est must be [low, high] with 0 ≤ low ≤ high")
    indeg = {i: 0 for i in ids}
    for t in tasks:
        for d in t.get("deps", []):
            if d in by:
                indeg[t["id"]] += 1
    order, ready = [], sorted([i for i in ids if indeg[i] == 0], key=ids.index)
    while ready:
        n = ready.pop(0)
        order.append(n)
        for t in tasks:
            if n in t.get("deps", []):
                indeg[t["id"]] -= 1
                if indeg[t["id"]] == 0:
                    ready.append(t["id"])
        ready.sort(key=ids.index)
    if len(order) != len(ids):
        raise ValueError("the dependencies have a cycle: " + ", ".join(i for i in ids if i not in order))

    def path(k: int):
        finish, prev = {}, {}
        for n in order:
            t = by[n]
            est = t.get("est", [1, 1])
            est = est if isinstance(est, list) and len(est) == 2 else [1, 1]
            start, p = 0.0, None
            for d in t.get("deps", []):
                if d in finish and finish[d] > start:
                    start, p = finish[d], d
            finish[n], prev[n] = start + float(est[k]), p
        end = max(finish, key=finish.get)
        chain = [end]
        while prev[chain[-1]]:
            chain.append(prev[chain[-1]])
        return round(finish[end], 3), chain[::-1]

    lo, lo_chain = path(0)
    hi, hi_chain = path(1)
    one_way = [t["id"] for t in tasks if t.get("reversible") is False]
    roots = [i for i in order if not by[i].get("deps")]
    risky = sorted(tasks, key=lambda t: (-int(t.get("risk", 0)), order.index(t["id"])))
    advice = []
    top = risky[0]
    if int(top.get("risk", 0)) >= 2 and order.index(top["id"]) > len(order) // 2:
        advice.append(f"{top['id']} carries the highest risk ({top.get('risk')}) but runs late: probe it earlier with a cheap spike")
    for i in one_way:
        advice.append(f"{i} cannot be undone: gate it on the user's explicit permission and put it last")
    if hi > 0 and lo > 0 and hi / lo >= 3:
        advice.append(f"the estimate spreads ×{hi / lo:.1f}: the largest unknown deserves the first probe")
    return {"goal": spec.get("goal", ""), "order": order, "roots": roots, "critical_path": {"optimistic": [lo, lo_chain], "pessimistic": [hi, hi_chain]},
            "one_way_doors": one_way, "problems": problems, "advice": advice,
            "verdict": "OK" if not problems else "FIX"}


def cmd_decompose(path, template: bool) -> int:
    if template or not path:
        print(json.dumps(DECOMPOSE_TEMPLATE, ensure_ascii=False, indent=1)); return 0
    try:
        r = decompose(json.loads(Path(path).read_text(encoding="utf-8")))
    except (ValueError, KeyError, TypeError) as e:
        print(f"think.py decompose: {e}", file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0 if r["verdict"] == "OK" else 1


# ------------------------------------------------------------------ qa (appendix A27)
def qa(kind: str, answers: dict = None, data: dict = None) -> dict:
    """The quality bar of a deliverable kind; with answers {check id: true|false|"n/a"} a PASS / FAIL / INCOMPLETE verdict."""
    data = data or intel()
    if kind not in data["kinds"]:
        raise ValueError(f"unknown kind {kind!r}; one of: {', '.join(data['kinds'])}")
    checks = data["kinds"][kind]["quality"]
    if answers is None:
        return {"kind": kind, "checks": checks, "verdict": "UNANSWERED"}
    unknown = sorted(set(answers) - {c["id"] for c in checks})
    if unknown:
        raise ValueError(f"unknown check id(s) for {kind}: {', '.join(unknown)}")
    rows, hard_fail, soft_fail, missing = [], [], [], []
    for c in checks:
        a = answers.get(c["id"])
        if a is None:
            missing.append(c["id"])
        elif a is False:
            (hard_fail if c["hard"] else soft_fail).append(c["id"])
        elif a not in (True, "n/a"):
            raise ValueError(f"{c['id']}: answer must be true, false or \"n/a\"")
        elif a == "n/a" and c["hard"]:
            missing.append(c["id"])   # a hard check cannot be waived by "n/a": measure it or report the gap
        rows.append({**c, "answer": a})
    verdict = "FAIL" if hard_fail else ("INCOMPLETE" if missing else "PASS")
    return {"kind": kind, "checks": rows, "hard_fail": hard_fail, "soft_fail": soft_fail, "missing": missing, "verdict": verdict}


def cmd_qa(kind, answers_path, as_json: bool) -> int:
    data = intel()
    if not kind:
        for kid, k in data["kinds"].items():
            print(f"{kid:12} {k['en']} / {k['ar']} ({len(k['quality'])} checks)")
        return 0
    try:
        answers = json.loads(Path(answers_path).read_text(encoding="utf-8")) if answers_path else None
        r = qa(kind, answers, data)
    except (ValueError, OSError) as e:
        print(f"think.py qa: {e}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(f"quality bar — {kind}: {data['kinds'][kind]['ar']}")
        for c in r["checks"]:
            mark = {True: "✅", False: "❌", "n/a": "—", None: "○"}.get(c.get("answer"), "○")
            print(f"  {mark} {'HARD' if c['hard'] else 'soft'} {c['id']}: {c['ar']}  ← {c['tool']}")
        print(f"\nverdict: {r['verdict']}" + (f" · hard fail {r['hard_fail']}" if r.get("hard_fail") else "")
              + (f" · unmeasured {r['missing']}" if r.get("missing") else ""))
    return {"FAIL": 1, "INCOMPLETE": 1}.get(r["verdict"], 0)


# ------------------------------------------------------------------ recover (appendix A29)
def recover(error_class: str = None, attempts: int = 0, message: str = "", data: dict = None) -> dict:
    """The recovery ladder for an error class (guessed from the message when not given) and whether to stop."""
    data = data or intel()
    rec = data["recovery"]
    guessed = False
    if not error_class:
        guessed = True
        low = message.lower()
        error_class = next((c for c, r in rec.items() if c != "other" and any(s.lower() in low for s in r["signals"])), "other")
    if error_class not in rec:
        raise ValueError(f"unknown error class {error_class!r}; one of: {', '.join(rec)}")
    r = rec[error_class]
    stop = attempts >= r["budget"]
    return {"error_class": error_class, "guessed": guessed, **r, "attempts": attempts,
            "next": ("STOP: budget spent — use the fallback once, then report with the reproduction and the numbers"
                     if stop else f"attempt {attempts + 1} of {r['budget']}: diagnose, fix one proven cause, re-measure"),
            "trace": f"fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action \"<what was tried>\" --result failed --error-class {error_class} --evidence <file>"}


def cmd_recover(error_class, attempts: int, message: str, as_json: bool) -> int:
    try:
        r = recover(error_class, attempts, message)
    except ValueError as e:
        print(f"think.py recover: {e}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=1)); return 0
    print(f"{r['error_class']} — {r['ar']}" + (" (guessed from the message)" if r["guessed"] else ""))
    for title, key in (("diagnose", "diagnose"), ("fix", "fix")):
        print(f"\n{title}:")
        for i, s in enumerate(r[key], 1):
            print(f"  {i}. {s}")
    print(f"\nfallback: {r['fallback']}\nescalate: {r['escalate']}\n\n→ {r['next']}\nrecord: {r['trace']}")
    return 1 if r["next"].startswith("STOP") else 0


# ------------------------------------------------------------------ pro (USIP v5.5, appendix A30)
DEPTHS = ("standard", "deep", "max")


def pro(task: str, depth: str = "deep", data: dict = None) -> dict:
    """The Pro intelligence scaffold: the passes of a depth, a task-fitted council, two reasoning modes and three models."""
    if depth not in DEPTHS:
        raise ValueError(f"depth must be one of {', '.join(DEPTHS)}")
    data = data or intel()
    upto = DEPTHS.index(depth)
    passes = [x for x in data["pro_passes"] if DEPTHS.index(x["depth"]) <= upto]
    seats = data["pro_depths"][depth]["seats"]
    council = []
    try:
        sys.path.insert(0, str(HERE))
        import council as cn  # same folder
        pool = cn.load_personas(cn.DEFAULT_PERSONAS)
        primary = cn.primary_of(task, None)
        council = [f"{p['id']} {p['name_ar']} — {p['title_ar']} [{p['lane']}]" for p in cn.select_personas(pool, task, primary, seats)]
    except Exception as exc:  # the scaffold still works without the roster
        council = [f"roster unavailable: {type(exc).__name__}"]
    cmd = ("council.py plan \"<task>\" --dir out/<job>/council" + ("" if seats == 5 else f" --seats {seats}"))
    return {"task": task, "depth": depth, "label": data["pro_depths"][depth]["ar"], "passes": passes,
            "council": {"seats": seats, "members": council, "command": cmd,
                        "note": "personas are stance prompts; the council counts only as real agents (else COUNCIL_SIMULATED)"},
            "modes": [{"id": m["id"], "en": m["en"], "check": m["check"]} for m in rank_modes(task, 2)],
            "models": [{"id": m["id"], "name_en": m["name_en"], "question": m["question"]} for m in rank_models(task, 3)],
            "gate": "Every pass leaves its artifact; a pass whose falsifier holds is redone, not reported as done."}


def cmd_pro(task: str, depth: str, as_json: bool) -> int:
    try:
        r = pro(task, depth)
    except ValueError as exc:
        print(f"think pro: error: {exc}", file=sys.stderr); return 2
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=1)); return 0
    print(f"PRO · {r['label']} · {len(r['passes'])} passes · council of {r['council']['seats']}\n")
    for x in r["passes"]:
        print(f"{x['id']} {x['en']} / {x['ar']}\n   ask: {x['question']}\n   → {x['artifact']}\n   ✗ redo if: {x['falsifier']}\n   tool: {x['tool']}")
    print(f"\ncouncil ({r['council']['command']}):")
    for m in r["council"]["members"]:
        print(f"   {m}")
    print("\nmodes: " + " · ".join(f"{m['id']} {m['en']}" for m in r["modes"]))
    print("models: " + " · ".join(f"{m['id']} {m['name_en']}" for m in r["models"]))
    print(f"\n{r['gate']}\n{r['council']['note']}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ladder").add_argument("task")
    sub.add_parser("frame").add_argument("task")
    m = sub.add_parser("models"); m.add_argument("problem"); m.add_argument("-n", type=int, default=5); m.add_argument("--json", action="store_true")
    m.add_argument("--plain", action="store_true", help="plain score order, no discipline diversity or reserved lenses")
    p = sub.add_parser("plan"); p.add_argument("goal"); p.add_argument("--weeks", type=int, default=4)
    i = sub.add_parser("ideas"); i.add_argument("seed_text"); i.add_argument("-n", type=int, default=12); i.add_argument("--seed", type=int, default=7)
    sub.add_parser("decide").add_argument("path")
    f = sub.add_parser("fermi"); f.add_argument("expr"); f.add_argument("--range", nargs="+", default=[]); f.add_argument("--samples", type=int, default=20000); f.add_argument("--seed", type=int, default=7)
    sub.add_parser("critic").add_argument("path")
    mo = sub.add_parser("modes"); mo.add_argument("task"); mo.add_argument("-n", type=int, default=3); mo.add_argument("--json", action="store_true")
    b = sub.add_parser("bayes"); b.add_argument("--prior", type=float); b.add_argument("--lr", nargs="*", default=[]); b.add_argument("--threshold", type=float); b.add_argument("--json", dest="spec")
    g = sub.add_parser("gate"); g.add_argument("path", nargs="?"); g.add_argument("--template", action="store_true")
    au = sub.add_parser("audit"); au.add_argument("path"); au.add_argument("--strict", action="store_true")
    it = sub.add_parser("intake"); it.add_argument("request"); it.add_argument("--level", default="L2"); it.add_argument("--json", action="store_true")
    de = sub.add_parser("decompose"); de.add_argument("path", nargs="?"); de.add_argument("--template", action="store_true")
    q = sub.add_parser("qa"); q.add_argument("kind", nargs="?"); q.add_argument("--answers"); q.add_argument("--json", action="store_true")
    rc = sub.add_parser("recover"); rc.add_argument("error_class", nargs="?"); rc.add_argument("--attempts", type=int, default=0); rc.add_argument("--message", default=""); rc.add_argument("--json", action="store_true")
    pr = sub.add_parser("pro"); pr.add_argument("task"); pr.add_argument("--depth", choices=DEPTHS, default="deep"); pr.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "ladder": return cmd_ladder(a.task)
    if a.cmd == "frame": return cmd_frame(a.task)
    if a.cmd == "models": return cmd_models(a.problem, a.n, a.json, a.plain)
    if a.cmd == "plan": return cmd_plan(a.goal, a.weeks)
    if a.cmd == "ideas": return cmd_ideas(a.seed_text, a.n, a.seed)
    if a.cmd == "decide": return cmd_decide(a.path)
    if a.cmd == "fermi": return cmd_fermi(a.expr, a.range, a.samples, a.seed)
    if a.cmd == "modes": return cmd_modes(a.task, a.n, a.json)
    if a.cmd == "bayes": return cmd_bayes(a.prior, a.lr, a.threshold, a.spec)
    if a.cmd == "gate": return cmd_gate(a.path, a.template)
    if a.cmd == "audit": return cmd_audit(a.path, a.strict)
    if a.cmd == "intake": return cmd_intake(a.request, a.level, a.json)
    if a.cmd == "decompose": return cmd_decompose(a.path, a.template)
    if a.cmd == "qa": return cmd_qa(a.kind, a.answers, a.json)
    if a.cmd == "recover": return cmd_recover(a.error_class, a.attempts, a.message, a.json)
    if a.cmd == "pro": return cmd_pro(a.task, a.depth, a.json)
    return cmd_critic(a.path)


if __name__ == "__main__":
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
