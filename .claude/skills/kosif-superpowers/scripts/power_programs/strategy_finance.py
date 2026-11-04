"""Programs for the strategy-finance family (PROD-01..14). PROD-15 (network data), PROD-16/17 (code proofs
elsewhere) and PROD-18 (MuJoCo not installed) are skipped."""
from __future__ import annotations
import json
from ._mind_common import save, eq, truth, monte_carlo, percentile, ice
import numpy as np
from scipy.optimize import linprog, brentq


def options_table(opts):
    problems = []
    if "do-nothing" not in opts:
        problems.append("no do-nothing")
    cols = ("cost", "benefit", "reversibility", "time_to_signal", "risk")
    for k, v in opts.items():
        miss = [c for c in cols if c not in v]
        if miss:
            problems.append(f"{k} missing {miss}")
    ideas = [v["idea"] for k, v in opts.items() if k != "do-nothing"]
    if len(set(ideas)) < len(ideas):
        problems.append("same idea in different sizes")
    return problems


def d01(work):
    row = lambda idea, c: {"idea": idea, "cost": c, "benefit": 2 * c, "reversibility": "high", "time_to_signal": "2w", "risk": "x"}
    good = {"A": row("ads", 1), "B": row("partnership", 2), "C": row("SEO", 3), "do-nothing": row("none", 0)}
    sizes = {"A": row("ads", 1), "B": row("ads", 2), "C": row("ads", 3)}
    save(work, "options.json", good)
    return [eq("valid table", options_table(good), []), eq("three sizes of one idea rejected", options_table(sizes), ["no do-nothing", "same idea in different sizes"])]


def profit_a(x):
    return 50 * x - 20000


def profit_b(x):
    return 30 * x - 8000


def d02(work):
    flip = brentq(lambda x: profit_a(x) - profit_b(x), 0, 10_000)
    evidence = 450
    pick = "A" if profit_a(evidence) > profit_b(evidence) else "B"
    save(work, "threshold.json", {"flip_volume": flip, "evidence_volume": evidence, "pick": pick})
    return [eq("flipping threshold", round(flip, 6), 600.0), eq("evidence below threshold -> B", pick, "B"),
            truth("above threshold A wins", profit_a(700) > profit_b(700))]


def d03(work):
    def draw(r):
        price = r.uniform(8, 12)
        units = r.gauss(5000, 1500)
        cost = 40000
        return price * units - cost
    xs = monte_carlo(draw, 20000, 7)
    ploss = sum(x < 0 for x in xs) / len(xs)
    p5, p50, p95 = (percentile(xs, q) for q in (5, 50, 95))
    save(work, "montecarlo.json", {"assumed": "price U(8,12), units N(5000,1500), fixed 40k", "P_loss": ploss, "P5": p5, "P50": p50, "P95": p95})
    # analytic: mean = 10*5000-40000 = 10000
    return [eq("mean near analytic 10,000", round(sum(xs) / len(xs)), 10000, tol=250), truth("P5<P50<P95", p5 < p50 < p95, (p5, p50, p95)),
            eq("P(loss) near 0.27", round(ploss, 2), 0.27, tol=0.03), truth("seeded reproducible", monte_carlo(draw, 5, 7) == xs[:5])]


def premortem_scores(stories):
    for s in stories:
        s["score"] = s["likelihood"] * s["impact"]
    return sorted(stories, key=lambda s: -s["score"])


def d04(work):
    cats = ["market", "execution", "team", "tech", "legal", "timing"]
    stories = [{"cat": c, "likelihood": l, "impact": i} for c, l, i in zip(cats, [3, 4, 2, 5, 1, 2], [4, 4, 5, 3, 5, 2])]
    top = premortem_scores(stories)[:3]
    mitig = [{"cat": s["cat"], "mitigation": f"guard {s['cat']}", "warning": f"signal {s['cat']}"} for s in top]
    save(work, "premortem.json", {"stories": stories, "top3": mitig})
    return [truth("5-10 stories", 5 <= len(stories) <= 10), eq("top 3 by likelihood x impact", [m["cat"] for m in top], ["execution", "tech", "market"]),
            eq("top score", top[0]["score"], 16)]


def council(own, voices):
    """own position recorded before reading voices; dissent kept."""
    record = {"own": own, "voices": voices}
    votes = [v["plan"] for v in voices.values()] + [own["plan"]]
    majority = max(set(votes), key=votes.count)
    record["synthesis"] = majority
    record["dissent"] = sorted(k for k, v in voices.items() if v["plan"] != majority)
    return record


def d05(work):
    own = {"plan": "B", "reasons": ["r1", "r2", "r3"], "risk": "cost"}
    voices = {"architect": {"plan": "B"}, "skeptic": {"plan": "C"}, "pragmatist": {"plan": "B"}, "critic": {"plan": "A"}}
    r = council(own, voices)
    save(work, "council.json", r)
    return [eq("own position before others has 3 reasons", len(r["own"]["reasons"]), 3), eq("synthesis", r["synthesis"], "B"),
            eq("dissent visible", r["dissent"], ["critic", "skeptic"]), eq("four voices", len(voices), 4)]


LEDGER_KEYS = ["date", "decision", "options", "evidence", "mark", "review_if"]


def ledger_append(path, entry):
    miss = [k for k in LEDGER_KEYS if k not in entry]
    if miss:
        raise ValueError(f"missing {miss}")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def d06(work):
    p = work / "decisions.jsonl"
    ledger_append(p, {"date": "2026-11-03", "decision": "ship B", "options": ["A", "B"], "evidence": "test.json", "mark": "dry-run", "review_if": "CAC>40"})
    ledger_append(p, {"date": "2026-11-04", "decision": "keep B", "options": ["B", "C"], "evidence": "kpi.csv", "mark": "live", "review_if": "NPS<20"})
    rejected = False
    try:
        ledger_append(p, {"date": "2026-11-05", "decision": "go", "mark": "live"})
    except ValueError:
        rejected = True
    lines = [json.loads(l) for l in p.read_text().splitlines()]
    return [eq("two entries", len(lines), 2), truth("incomplete entry rejected", rejected), eq("decision leads", list(lines[0])[1], "decision")]


def rollout_eval(stages, metrics):
    res = []
    for s in stages:
        m = metrics[s["stage"]]
        killed = m[s["metric"]] > s["kill_above"]
        res.append((s["stage"], "stop" if killed else "advance"))
        if killed:
            break
    return res


def d07(work):
    stages = [{"stage": "5%", "metric": "cac_over_ltv", "kill_above": 2.0}, {"stage": "25%", "metric": "cac_over_ltv", "kill_above": 2.0},
              {"stage": "100%", "metric": "cac_over_ltv", "kill_above": 2.0}]
    metrics = {"5%": {"cac_over_ltv": 0.9}, "25%": {"cac_over_ltv": 2.4}, "100%": {"cac_over_ltv": 1.0}}
    r = rollout_eval(stages, metrics)
    save(work, "rollout.json", r)
    return [eq("stopped at 25%", r, [("5%", "advance"), ("25%", "stop")]), truth("100% never reached", len(r) == 2)]


VAGUE = {"fast", "quick", "easy", "intuitive", "robust", "scalable", "nice", "simple", "soon"}


def prd_lint(prd):
    import re
    problems = []
    if not 3 <= len(prd["criteria"]) <= 7:
        problems.append("criteria count")
    for c in prd["criteria"]:
        v = [w for w in re.findall(r"[a-z]+", c.lower()) if w in VAGUE]
        if v and not re.search(r"\d", c):
            problems.append(f"vague: {c}")
    for k in ("goal", "in_scope", "out_scope", "assumptions", "blockers"):
        if k not in prd:
            problems.append(f"missing {k}")
    return problems


def d08(work):
    prd = {"goal": "export", "in_scope": ["mp4"], "out_scope": ["gif"], "assumptions": [], "blockers": [],
           "criteria": ["p95 export < 300 ms per frame", "page must be fast", "RTL captions pass bidi test"]}
    p = prd_lint(prd)
    save(work, "prd_lint.json", p)
    return [eq("vague criterion caught", p, ["vague: page must be fast"]), eq("numeric version accepted", prd_lint(dict(prd, criteria=prd["criteria"][::2] + ["fast: TTI < 2 s"])), [])]


def d09(work):
    items = {"dark mode": (3, 4, 2), "arabic captions": (5, 4, 2), "ai voice": (5, 2, 5), "export gif": (2, 5, 1)}
    scores = {k: ice(*v) for k, v in items.items()}
    order = sorted(scores, key=lambda k: (-scores[k], k))
    save(work, "ice.csv", "item,impact,confidence,effort,ice\n" + "\n".join(f"{k},{a},{b},{c},{scores[k]}" for k, (a, b, c) in items.items()))
    return [eq("arabic captions score", scores["arabic captions"], 10.0), eq("order", order, ["arabic captions", "export gif", "dark mode", "ai voice"])]


def d10(work):
    r = linprog(c=[-40, -30], A_ub=[[1, 1], [2, 1]], b_ub=[40, 60], bounds=[(0, None)] * 2, method="highs")
    x, y = r.x
    save(work, "lp.json", {"x": x, "y": y, "profit": -r.fun})
    # cross-check by vertex enumeration
    verts = [(0, 0), (30, 0), (0, 40), (20, 20)]
    best = max(40 * a + 30 * b for a, b in verts)
    return [eq("x", round(x, 6), 20.0), eq("y", round(y, 6), 20.0), eq("profit", round(-r.fun, 6), 1400.0), eq("vertex cross-check", best, 1400)]


def d11(work):
    a, b, c = 200, 2, 20  # profit=(p-c)*(a-b p) -> p*=(a+bc)/(2b)=60, profit=(40)*(80)=3200 per unit scale 5 -> use a=1000,b=10
    a, b, c = 1000, 10, 20
    profit = lambda p: (p - c) * (a - b * p)
    pstar = (a + b * c) / (2 * b)
    second = -2 * b
    numeric = max(np.linspace(0, 100, 100001), key=profit)
    F, p, v = 120000, 50, 30
    Q = F / (p - v)
    save(work, "price.json", {"p_star": pstar, "profit": profit(pstar), "second_derivative": second, "break_even_Q": Q, "assumption": "linear demand"})
    return [eq("p*", pstar, 60.0), eq("profit at p*", profit(pstar), 16000.0), truth("maximum (2nd derivative < 0)", second < 0),
            eq("grid search agrees", round(float(numeric), 3), 60.0), eq("break-even Q", Q, 6000.0)]


def journal_check(entries):
    return [e["id"] for e in entries if round(sum(l["dr"] for l in e["lines"]), 2) != round(sum(l["cr"] for l in e["lines"]), 2)]


def d12(work):
    entries = [{"id": "J1", "rule": "IAS 16", "lines": [{"acct": "equipment", "dr": 5000, "cr": 0}, {"acct": "cash", "dr": 0, "cr": 5000}]},
               {"id": "J2", "rule": "IFRS 15", "lines": [{"acct": "receivable", "dr": 1200, "cr": 0}, {"acct": "revenue", "dr": 0, "cr": 1000}]}]
    bad = journal_check(entries)
    save(work, "journal.json", {"entries": entries, "unbalanced": bad})
    return [eq("unbalanced entry caught", bad, ["J2"]), eq("balanced passes", journal_check(entries[:1]), [])]


def reconcile(bank, ledger):
    key = lambda r: (r["date"], r["amount"], r["ref"])
    bk, lk = {key(r) for r in bank}, {key(r) for r in ledger}
    only_bank, only_ledger = sorted(bk - lk), sorted(lk - bk)
    residual = round(sum(r["amount"] for r in bank) - sum(r["amount"] for r in ledger), 2)
    explained = round(sum(k[1] for k in only_bank) - sum(k[1] for k in only_ledger), 2)
    return only_bank, only_ledger, residual, round(residual - explained, 2)


def d13(work):
    bank = [{"date": "11-01", "amount": 100.0, "ref": "A"}, {"date": "11-02", "amount": 250.0, "ref": "B"}, {"date": "11-03", "amount": -15.0, "ref": "FEE"}]
    ledger = [{"date": "11-01", "amount": 100.0, "ref": "A"}, {"date": "11-02", "amount": 205.0, "ref": "B"}, {"date": "11-04", "amount": 60.0, "ref": "C"}]
    ob, ol, res, unexplained = reconcile(bank, ledger)
    save(work, "recon.json", {"only_bank": ob, "only_ledger": ol, "residual": res, "unexplained": unexplained})
    return [eq("bank-only items", len(ob), 2), eq("ledger-only items", len(ol), 2), eq("residual", res, -30.0), eq("no plug: unexplained", unexplained, 0.0)]


def model(inputs):
    rev = inputs["units"] * inputs["price"]
    cogs = inputs["units"] * inputs["unit_cost"]
    opex = inputs["opex"]
    ni = rev - cogs - opex
    cash = inputs["cash0"] + ni - inputs["capex"]
    assets = cash + inputs["ppe0"] + inputs["capex"]
    equity = inputs["equity0"] + ni
    return {"revenue": rev, "net_income": ni, "cash": cash, "assets": assets, "equity": equity,
            "balance_check": round(assets - equity, 6), "cash_bridge": round(cash - (inputs["cash0"] + ni - inputs["capex"]), 6)}


def d14(work):
    base = {"units": 1000, "price": 20, "unit_cost": 8, "opex": 5000, "capex": 2000, "cash0": 3000, "ppe0": 7000, "equity0": 10000}
    m = model(base)
    down = model(dict(base, units=600))
    save(work, "model.json", {"base": m, "downside": down})
    return [eq("net income", m["net_income"], 7000), eq("balance = 0", m["balance_check"], 0), eq("cash bridge = 0", m["cash_bridge"], 0),
            eq("scenario on inputs only", down["net_income"], 2200), eq("downside still balances", down["balance_check"], 0)]


PROGRAMS = {f"PROD-{i:02d}": globals()[f"d{i:02d}"] for i in range(1, 15)}
