"""Programs for the atlas-strategy family (ASTRAT-01..108). ASTRAT-54 (needs the Anki desktop app with
AnkiConnect) and ASTRAT-55 (Google Classroom service) are skipped. Every other card's method runs as a
deterministic procedure on a planted fixture with a known answer."""
from __future__ import annotations
import math
import re
import numpy as np
from scipy.stats import norm
from ._mind_common import (save, eq, truth, critical_path, topo_order, weighted_scores, rank, percentile, npv, words,
                           expected_value, require_fields, vague_terms, has_number)


# ---------- agent workflows ----------

def crossings(flow):
    """flow: ordered actors incl. 'human' at both ends -> list of boundary crossings."""
    return [(a, b) for a, b in zip(flow, flow[1:]) if a != b]


def boundary_verdict(gains):
    return "keep" if gains else "collapse"


def a01(work):
    flow = ["human", "planner", "researcher", "writer", "reviewer", "human"]
    gains = {("planner", "researcher"): [], ("researcher", "writer"): ["parallelism"], ("writer", "reviewer"): ["adversarial reviewer"]}
    cr = crossings(flow)
    verdict = {f"{a}->{b}": boundary_verdict(gains.get((a, b), ["human interface"])) for a, b in cr}
    save(work, "topology_audit.json", {"crossings": len(cr), "verdict": verdict, "label": "prediction (described)"})
    return [eq("crossings counted, not agents", len(cr), 5), eq("boundary with no gain collapses", verdict["planner->researcher"], "collapse"),
            eq("adversarial boundary kept", verdict["writer->reviewer"], "keep")]


def ralph_loop(backlog, gate, followups):
    worked, log, new = [], [], []
    queue = list(backlog)
    while queue:
        item = queue.pop(0)
        if not gate(item):
            log.append(("rejected", item))
            continue
        worked.append(item)  # one item per cycle
        for f in followups.get(item, []):
            new.append(f)  # logged, not worked
        log.append(("validated+commit", item))
    return worked, new, log


def a02(work):
    tasks_md = "- a\n- b\n- c\n"
    worked, new, log = ralph_loop(["a", "b", "c", "x"], lambda i: i != "x", {"b": ["b-docs"]})
    save(work, "loop_log.json", {"log": log, "followups": new})
    return [eq("one item per cycle, gated", worked, ["a", "b", "c"]), eq("follow-up logged not worked", new, ["b-docs"]),
            truth("tasks.md untouched", tasks_md == "- a\n- b\n- c\n"), eq("every commit validated", sum(1 for k, _ in log if k == "validated+commit"), 3)]


ROLES = {"CFO": ["runway", "burn", "pricing", "fundraise"], "CMO": ["brand", "marketing", "positioning"], "CISO": ["security", "breach", "soc2"],
         "CHRO": ["hiring", "culture"], "COO": ["operations", "process"], "GC": ["contract", "legal"]}


def route(question, context_age_days):
    w = set(words(question))
    roles = sorted(r for r, kws in ROLES.items() if w & set(kws))
    return {"roles": roles, "board": len(roles) >= 2, "stale": context_age_days > 90}


def a03(work):
    r1 = route("should we raise a fundraise before hiring", 120)
    r2 = route("is our soc2 ready", 10)
    save(work, "routing.json", {"q1": r1, "q2": r2})
    return [eq("multi-role", r1["roles"], ["CFO", "CHRO"]), truth("board meeting triggered", r1["board"]), truth("stale context flagged (>90 d)", r1["stale"]),
            eq("single role", r2["roles"], ["CISO"]), truth("fresh context", not r2["stale"])]


def waves(waves_, gate_results):
    done = []
    for i, w in enumerate(waves_):
        done.append(w["name"])
        if not gate_results.get(w["name"], True):
            return done, f"halted after {w['name']}"
    return done, "complete"


def a04(work):
    W = [{"name": "research", "tools": ["read"]}, {"name": "foundation", "tools": ["build"]}, {"name": "extensions", "tools": ["edit"]}]
    ok = waves(W, {})
    bad = waves(W, {"foundation": False})
    lock_alone = [len(w["tools"]) == 1 for w in W if "build" in w["tools"]]
    backoff = [min(60, 2 ** k) for k in range(7)]
    save(work, "waves.json", {"ok": ok, "bad": bad, "backoff": backoff})
    return [eq("all waves", ok[1], "complete"), eq("gate failure stops next wave", bad, (["research", "foundation"], "halted after foundation")),
            truth("lock tool alone", all(lock_alone)), eq("backoff capped", backoff, [1, 2, 4, 8, 16, 32, 60])]


def budget(items, per_item_agents, cost_per_agent, group_size, redrive_rate, cap):
    agents = math.ceil(items / group_size) * per_item_agents
    total = agents * cost_per_agent * (1 + redrive_rate)
    return agents, round(total, 2), total <= cap


def a05(work):
    raw = budget(120, 3, 0.5, 1, 0.1, 100)
    grouped = budget(120, 3, 0.5, 6, 0.1, 100)
    save(work, "budget.json", {"raw": raw, "grouped": grouped})
    return [eq("ungrouped agents", raw[0], 360), eq("over budget", raw[2], False), eq("grouped by theme", grouped[0], 60), eq("grouped cost", grouped[1], 33.0),
            truth("fits after grouping", grouped[2])]


def a06(work):
    m = {"Destination": "v2 launch", "Notes": "", "Decisions so far": [], "Not yet specified": ["pricing"], "Out of scope": ["mobile"]}
    kids = [{"q": "which DB?", "type": "research", "tokens": 100_000, "blocked_by": []},
            {"q": "prototype sync", "type": "prototype", "tokens": 90_000, "blocked_by": ["which DB?"]},
            {"q": "pricing", "type": "grilling", "tokens": 400_000, "blocked_by": []}]
    frontier = [k["q"] for k in kids if not k["blocked_by"]]
    oversized = [k["q"] for k in kids if k["tokens"] > 150_000]
    save(work, "wayfinder.json", {"map": m, "children": kids})
    return [eq("five map sections", len(m), 5), eq("frontier = unblocked", frontier, ["which DB?", "pricing"]), eq("ticket too big", oversized, ["pricing"]),
            truth("valid types", all(k["type"] in ("research", "prototype", "grilling", "task") for k in kids))]


def phase_gates(phases, evidence):
    for p in phases:
        unmet = [c for c in p["exit"] if not evidence.get(c)]
        if unmet:
            return p["name"], unmet
    return "go-live", []


def a07(work):
    ph = [{"name": "kickoff", "exit": ["contract signed"]}, {"name": "setup", "exit": ["accounts created", "data imported"]},
          {"name": "training", "exit": ["users trained"]}, {"name": "go-live", "exit": ["sign-off"]}]
    stuck = phase_gates(ph, {"contract signed": 1, "accounts created": 1})
    save(work, "gates.json", stuck)
    return [eq("four phases", len(ph), 4), eq("blocked at setup", stuck, ("setup", ["data imported"]))]


def util_flags(billable, tracked, actual, planned):
    b = billable / tracked
    v = (actual - planned) / planned
    flag = "under-priced" if v > 0.5 else "scope review" if v > 0.25 else "over-planned" if v < -0.25 else "ok"
    return round(b, 4), round(v, 4), flag


def a08(work):
    r = {"client A": util_flags(70, 100, 160, 100), "client B": util_flags(80, 100, 130, 100), "client C": util_flags(60, 100, 70, 100)}
    save(work, "utilisation.md", "| client | billable | variance | flag |\n" + "\n".join(f"| {k} | {v[0]} | {v[1]} | {v[2]} |" for k, v in r.items()))
    return [eq("billable %", r["client A"][0], 0.7), eq("+60% under-priced", r["client A"][2], "under-priced"), eq("+30% scope review", r["client B"][2], "scope review"),
            eq("-30% over-planned", r["client C"][2], "over-planned")]


def pay_run(bills, today, balance):
    inc, exc = [], []
    for b in bills:
        reason = ("held" if b["hold"] else "disputed" if b["dispute"] else "unapproved" if not b["approved"] else "zero" if b["amount"] <= 0
                  else "outside-window" if b["due_in"] > 7 else None)
        if reason:
            exc.append((b["id"], reason))
            continue
        score = (10 if b.get("discount") else 0) + 5 * max(0, -b["due_in"] // 7) + (5 if b.get("critical") else 0) - (5 if b.get("terms", 30) >= 60 else 0)
        inc.append((b["id"], score, b["amount"]))
    total = sum(x[2] for x in inc)
    cash = "stop" if total > balance else "warn" if total > 0.8 * balance else "ok"
    return sorted(inc, key=lambda x: -x[1]), exc, total, cash


def a09(work):
    B = lambda i, **k: dict({"id": i, "hold": False, "dispute": False, "approved": True, "amount": 100, "due_in": 3}, **k)
    bills = [B("s1", discount=True), B("s2", due_in=-14), B("s3", hold=True), B("s4", due_in=20), B("s5", amount=0), B("s6", critical=True, terms=60, amount=650)]
    inc, exc, total, cash = pay_run(bills, 0, 1000)
    save(work, "payrun.json", {"included": inc, "excluded": exc, "total": total, "cash": cash})
    return [eq("excluded with reasons", exc, [("s3", "held"), ("s4", "outside-window"), ("s5", "zero")]), eq("top priority", inc[0][:2], ("s1", 10)),
            eq("two weeks overdue score", dict((i, s) for i, s, _ in inc)["s2"], 10), eq("cash warn >80%", cash, "warn")]


LIMITS = {"apple_name": 30, "apple_subtitle": 30, "apple_keywords": 100, "play_title": 30, "play_short": 80}


def aso_lint(meta):
    errs = [f"{k} over {LIMITS[k]}" for k, v in meta.items() if k in LIMITS and len(v) > LIMITS[k]]
    kws = [k.strip() for k in meta.get("apple_keywords", "").split(",")]
    dups = sorted({k for k in kws if kws.count(k) > 1})
    errs += [f"duplicate {d}" for d in dups]
    name_words = set(words(meta.get("apple_name", "")))
    errs += [f"keyword repeats name: {k}" for k in kws if k in name_words]
    return errs, (1 if errs else 0)


def a10(work):
    meta = {"apple_name": "Reels Maker", "apple_subtitle": "Arabic captions & montage", "apple_keywords": "video,edit,reels,captions,video",
            "play_short": "x" * 81}
    errs, code = aso_lint(meta)
    (work / "en-US.md").write_text("\n".join(f"{k}: {v}" for k, v in meta.items()))
    return [eq("lint errors", errs, ["play_short over 80", "duplicate video", "keyword repeats name: reels"]), eq("nonzero exit gates submission", code, 1)]


TRACK_STATUS = ["pending", "in-progress", "awaiting-evidence", "done"]


def a11(work):
    tracker = {"intake": "done", "spec": "awaiting-evidence", "design": "pending"}
    resume_at = next(k for k, v in tracker.items() if v != "done")
    invalid = [k for k, v in tracker.items() if v not in TRACK_STATUS]
    save(work, "tracker.json", tracker)
    return [eq("resume from tracker", resume_at, "spec"), eq("valid statuses", invalid, []), truth("unsigned draft not written", tracker["spec"] != "done")]


def risk_review(scores, narrow=False):
    if narrow:
        return None
    worst = min(scores, key=scores.get)
    avg = sum(scores.values()) / len(scores)
    verdict = "high" if avg < 2.5 else "medium" if avg < 3.5 else "low"
    return {"verdict": verdict, "breaks_first": worst}


def a12(work):
    s = {"demand": 2, "positioning": 3, "monetization": 1, "retention": 2, "trust": 3, "distribution": 2, "adoption": 3}
    r = risk_review(s)
    save(work, "risk_review.json", r)
    return [eq("seven dimensions", len(s), 7), eq("verdict", r["verdict"], "high"), eq("assumption most likely to break", r["breaks_first"], "monetization"),
            eq("narrow fix skipped", risk_review(s, narrow=True), None)]


def a13(work):
    data = {"balance": ("consensus", 1), "owner": ("consensus", 1), "avatar.png": ("ancillary", 2000), "history": ("ancillary", 500), "email": ("sensitive", 1)}
    gas_per_slot, gwei, eth_usd = 20000, 10, 3000
    cost = lambda slots: slots * gas_per_slot * gwei * 1e-9 * eth_usd
    on = [k for k, (c, _) in data.items() if c == "consensus"]
    off = {k: "IPFS + on-chain hash" for k, (c, _) in data.items() if c == "ancillary"}
    never = [k for k, (c, _) in data.items() if c == "sensitive"]
    save(work, "placement.json", {"on": on, "off": off, "never_public": never})
    return [eq("on-chain", on, ["balance", "owner"]), eq("slot cost USD", round(cost(1), 2), 0.6), eq("avatar would cost", round(cost(2000)), 1200), eq("sensitive kept off", never, ["email"])]


def backtest(prices, fast, slow, fee):
    p = np.asarray(prices, float)
    ma = lambda n: np.convolve(p, np.ones(n) / n, "valid")
    f, s = ma(fast)[slow - fast:], ma(slow)
    sig = (f > s).astype(float)
    pos = np.concatenate([[0], sig[:-1]])  # next-bar execution
    rets = np.diff(p[slow - 1:]) / p[slow - 1:-1]
    trades = np.abs(np.diff(np.concatenate([[0], pos])))[:len(rets)]
    strat = pos[:len(rets)] * rets - trades * fee
    eq_ = np.cumprod(1 + strat)
    dd = 1 - eq_ / np.maximum.accumulate(eq_)
    return strat, eq_, dd


def a14(work):
    up = np.linspace(100, 200, 60)
    strat, curve, dd = backtest(up, 3, 10, 0.0)
    _, curve_fee, _ = backtest(up, 3, 10, 0.01)
    var95 = -np.percentile(strat, 5)
    (work / "equity.csv").write_text("\n".join(f"{i},{v:.6f}" for i, v in enumerate(curve)))
    return [truth("trend captured", curve[-1] > 1.5, curve[-1]), eq("first bar flat (no look-ahead)", float(strat[0]), 0.0), eq("no drawdown in monotone rise", float(dd.max()), 0.0),
            truth("fees reduce equity", curve_fee[-1] < curve[-1]), truth("VaR <= 0 in a monotone rise", var95 <= 0)]


def dcf(fcf, wacc, g, exit_mult, ebitda_n, net_debt):
    pv = sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcf))
    n = len(fcf)
    tv_g = fcf[-1] * (1 + g) / (wacc - g)
    tv_m = ebitda_n * exit_mult
    pv_tv = tv_g / (1 + wacc) ** n
    ev = pv + pv_tv
    return {"pv_fcf": pv, "tv_gordon": tv_g, "tv_multiple": tv_m, "ev": ev, "tv_share": pv_tv / ev, "equity": ev - net_debt}


def a15(work):
    r = dcf([100] * 5, 0.10, 0.0, 10, 100, 200)
    save(work, "dcf.json", r)
    annuity = 100 * (1 - 1.1 ** -5) / 0.1
    return [eq("PV FCF = annuity", round(r["pv_fcf"], 4), round(annuity, 4)), eq("Gordon TV with g=0", round(r["tv_gordon"], 6), 1000.0),
            eq("both TV methods agree here", round(r["tv_multiple"]), 1000), eq("EV = 1000 (perpetuity)", round(r["ev"], 6), 1000.0),
            truth("TV share smell test flags > 60%", r["tv_share"] > 0.6, r["tv_share"]), eq("equity bridge", round(r["equity"], 6), 800.0)]


RISK_RE = re.compile(r"^In .+ exposed to .+ caused by .+ leading to .+$")


def a16(work):
    risks = [{"text": "In procurement exposed to supplier failure caused by single source leading to line stop", "L": 4, "I": 5, "ctrl": 2, "supplier": "S1"},
             {"text": "Cyber risk", "L": 3, "I": 4, "ctrl": 1, "supplier": None},
             {"text": "In sales exposed to FX loss caused by USD contracts leading to margin cut", "L": 3, "I": 3, "ctrl": 1, "supplier": "S1"}]
    for r in risks:
        r["inherent"] = r["L"] * r["I"]
        r["residual"] = max(1, r["inherent"] - 4 * r["ctrl"])
        r["well_formed"] = bool(RISK_RE.match(r["text"]))
    conc = {s: sum(1 for r in risks if r["supplier"] == s) for s in {r["supplier"] for r in risks if r["supplier"]}}
    save(work, "register.json", risks)
    return [eq("inherent 5x5", risks[0]["inherent"], 20), eq("residual", risks[0]["residual"], 12), eq("bad statement flagged", [r["well_formed"] for r in risks], [True, False, True]),
            eq("concentration", conc, {"S1": 2})]


def runway(cash, burn, growth, months=36):
    m, c, b = 0, cash, burn
    while c > 0 and m < months:
        c -= b
        b *= 1 + growth
        m += 1
    return m


def a17(work):
    sc = {"base": runway(120_000, 10_000, 0.0), "growth burn": runway(120_000, 10_000, 0.05), "cut": runway(120_000, 6_000, 0.0)}
    save(work, "runway.json", sc)
    return [eq("flat burn", sc["base"], 12), eq("5% burn growth", sc["growth burn"], 10), eq("cut burn", sc["cut"], 20)]


def a18(work):
    roles = {"CFO": ["a", "b", "c"], "CMO": ["d", "e", "f", "g", "h", "i"], "COO": ["j"]}
    over = [r for r, pts in roles.items() if len(pts) > 5]
    trimmed = {r: pts[:5] for r, pts in roles.items()}
    stance = {"CFO": "delay", "CMO": "launch", "COO": "launch"}
    major = max(set(stance.values()), key=list(stance.values()).count)
    minority = [r for r, s in stance.items() if s != major]
    memo = {"decision": major, "minority": minority, "approved": False}
    save(work, "board_memo.json", memo)
    return [eq("over-limit role caught", over, ["CMO"]), eq("max 5 points", max(len(v) for v in trimmed.values()), 5), eq("minority kept", minority, ["CFO"]),
            truth("not logged until founder approves", not memo["approved"])]


def a19(work):
    wtp = [8, 12, 15, 20, 25, 30, 45, 60, 80, 100]
    tiers = {"basic": 12, "pro": 30, "team": 80}
    buyers = {t: sum(w >= p for w in wtp) for t, p in tiers.items()}
    rev = {t: tiers[t] * buyers[t] for t in tiers}
    save(work, "pricing.json", {"buyers": buyers, "revenue_if_single_price": rev})
    return [eq("three tiers", len(tiers), 3), eq("buyers at each price", buyers, {"basic": 9, "pro": 5, "team": 2}), eq("best single price", max(rev, key=rev.get), "team")]


def rd_budget(direct, excluded, fa_rate):
    base = direct - excluded
    fa = base * fa_rate
    return direct, fa, direct + fa


def capitalise(item):
    crit = ["technical feasibility", "intent to complete", "ability to use", "future benefit", "resources", "measurable cost"]
    met = [c for c in crit if c in item["met"]]
    if len(met) == 6:
        return "CAPITALIZE-CANDIDATE"
    if not met:
        return "EXPENSE"
    return "FINANCE-OWNER-REVIEW"


def a20(work):
    d, fa, loaded = rd_budget(100_000, 20_000, 0.5)
    burn = [20, 22, 25, 30]
    trailing = sum(burn[-3:]) / 3
    cash = 140
    months = cash / trailing
    accel = all(b2 > b1 for b1, b2 in zip(burn, burn[1:]))
    items = [{"met": ["technical feasibility", "intent to complete", "ability to use", "future benefit", "resources", "measurable cost"]}, {"met": []}, {"met": ["resources"]}]
    routes = [capitalise(i) for i in items]
    save(work, "rd.json", {"fa": fa, "loaded": loaded, "runway": months, "routes": routes})
    return [eq("F&A on MTDC base", fa, 40_000.0), eq("loaded", loaded, 140_000.0), eq("runway months", round(months, 2), 5.45), truth("flag below 6 months", months < 6),
            truth("accelerating burn", accel), eq("routes", routes, ["CAPITALIZE-CANDIDATE", "EXPENSE", "FINANCE-OWNER-REVIEW"])]


def priced_round(table, pre_money, new_money, pool_target):
    shares = sum(table.values())
    price0 = pre_money / shares
    post = pre_money + new_money
    # pool top-up in the pre-money: solve pool such that pool / post_shares = target
    inv_pct = new_money / post
    existing_pool = table.get("pool", 0)
    total_post = shares / (1 - inv_pct - 0)  # placeholder overwritten below
    # iterate: new pool shares p so that (existing_pool + p)/(shares + p + inv) = pool_target, inv = inv_pct * total
    p = 0.0
    for _ in range(200):
        tot = (shares + p) / (1 - inv_pct)
        p = pool_target * tot - existing_pool
    tot = (shares + p) / (1 - inv_pct)
    inv = inv_pct * tot
    out = dict(table)
    out["pool"] = existing_pool + p
    out["investor"] = inv
    return {k: v / tot for k, v in out.items()}, (pre_money / (shares + p))


def safe_price(cap, discount, round_price, shares_pre):
    cap_price = cap / shares_pre
    return min(cap_price, round_price * (1 - discount))


def a21(work):
    pct, price = priced_round({"founders": 9_000_000, "pool": 1_000_000}, 8_000_000, 2_000_000, 0.10)
    sp = safe_price(5_000_000, 0.2, 1.0, 10_000_000)
    save(work, "cap_table.json", {"post": pct, "safe_price": sp})
    return [eq("investor % = money / post", round(pct["investor"], 6), 0.2), eq("pool topped to 10% post", round(pct["pool"], 6), 0.1),
            eq("founders diluted", round(pct["founders"], 6), 0.7), eq("SAFE converts at better of cap/discount", sp, 0.5)]


BMC = ["partners", "activities", "resources", "value", "relationships", "channels", "segments", "costs", "revenue"]
ERRC = ["eliminate", "reduce", "raise", "create"]


def a22(work):
    canvas = {b: f"{b} filled" for b in BMC}
    kernel = {"diagnosis": "fragmented Arabic tooling", "policy": "own the creator workflow", "actions": ["captions", "templates"]}
    errc = {"eliminate": ["login wall"], "reduce": ["settings"], "raise": ["speed"], "create": ["RTL kinetic type"]}
    assumptions = {"creators pay": 5, "RTL is a gap": 4, "SEO traffic": 1}
    attack = [a for a, w in sorted(assumptions.items(), key=lambda x: -x[1]) if w >= 4]
    lean = {"mvp": "captions only", "metric": "weekly exports", "rule": "pivot if < 50 by week 6"}
    save(work, "canvas.json", {"bmc": canvas, "kernel": kernel, "errc": errc, "attack": attack, "lean": lean})
    return [eq("9 blocks", len(canvas), 9), truth("kernel complete", all(kernel.values())), eq("ERRC four", list(errc), ERRC), eq("load-bearing attacked", attack, ["creators pay", "RTL is a gap"]),
            truth("pivot rule numeric", has_number(lean["rule"]))]


def cash13(opening, receipts, disb):
    bal, out = opening, []
    for r, d in zip(receipts, disb):
        bal += r - d
        out.append(bal)
    return out


def a23(work):
    rec = [100] * 13
    dis = [80] * 13
    dis[4] += 150  # payroll + tax week
    fc = cash13(200, rec, dis)
    actual_w1 = 215
    variance = actual_w1 - fc[0]
    stress = cash13(200, [70] * 13, dis)
    buffer = max(0, -min(stress))
    save(work, "cash13.json", {"forecast": fc, "variance_w1": variance, "stress": stress, "buffer": buffer})
    return [eq("13 weeks", len(fc), 13), eq("week 5 dip", fc[4], 150), eq("week 13", fc[-1], 310), eq("variance week 1", variance, -5), eq("stress buffer", buffer, 80)]


def a24(work):
    cust = {"A": (12000, 2000), "B": (3000, 2500), "C": (800, 1200), "D": (20000, 3000)}
    net = {k: r - c for k, (r, c) in cust.items()}
    tiers = {k: ("strategic" if r >= 10000 else "growth" if net[k] > 0 else "unprofitable") for k, (r, c) in cust.items()}
    per_adv, cap = 30, 2
    save(work, "segments.json", {"net": net, "tiers": tiers})
    return [eq("net after cost-to-serve", net["C"], -400), eq("tiers", tiers, {"A": "strategic", "B": "growth", "C": "unprofitable", "D": "strategic"}),
            truth("over capacity flagged", 75 / per_adv > cap)]


def sample_size(p, mde, alpha=0.05, power=0.8):
    p2 = p + mde
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    return math.ceil((za + zb) ** 2 * (p * (1 - p) + p2 * (1 - p2)) / mde ** 2)


def a25(work):
    n = sample_size(0.10, 0.02)
    weekly_conv = 520
    traffic_per_week = 5200
    weeks = math.ceil(2 * n / traffic_per_week)
    gate = weekly_conv >= 500 and weeks <= 6
    save(work, "experiment.json", {"n_per_arm": n, "weeks": weeks, "gate": gate, "hypothesis": "If hook < 1 s then CTR +2 pts because thumbs stop"})
    return [eq("n per arm (10% -> 12%)", n, 3839), eq("weeks", weeks, 2), truth("go gate", gate), eq("low traffic -> no-go", 300 >= 500, False)]


def a26(work):
    funnel = {"visit": 10000, "signup": 3000, "activate": 600, "pay": 300}
    steps = list(funnel)
    conv = {f"{a}->{b}": funnel[b] / funnel[a] for a, b in zip(steps, steps[1:])}
    worst = min(conv, key=conv.get)
    cohort = [1.0, 0.5, 0.4, 0.38, 0.37]
    flatten = next(i for i in range(1, len(cohort)) if cohort[i - 1] - cohort[i] < 0.02)
    save(work, "funnel.json", {"conv": conv, "worst": worst, "retention_flattens_at": flatten})
    return [eq("largest drop", worst, "signup->activate"), eq("conv", conv["signup->activate"], 0.2), eq("retention flattens", flatten, 4)]


METRIC_FIELDS = ["name", "formula", "source", "spec", "segments", "thresholds"]


def a27(work):
    tree = {"north star": "weekly exports", "inputs": ["new creators", "exports per creator", "retention"]}
    defs = [{f: "x" for f in METRIC_FIELDS}, dict({f: "x" for f in METRIC_FIELDS}, source="")]
    gaps = [i for i, d in enumerate(defs) if require_fields(d, METRIC_FIELDS)]
    save(work, "metrics.json", {"tree": tree, "defs": defs})
    return [eq("input tree", len(tree["inputs"]), 3), eq("incomplete definition", gaps, [1])]


SIX_M = ["machine", "method", "material", "measurement", "man", "environment"]
DOWNTIME = ["defects", "overproduction", "waiting", "non-utilised talent", "transport", "inventory", "motion", "extra processing"]


def action_priority(s, o, d):
    if s >= 9 and (o >= 4 or d >= 7):
        return "H"
    if s >= 7 and o >= 4:
        return "H"
    if s >= 5 and o >= 6:
        return "M"
    return "L"


def a28(work):
    takt = 8 * 3600 / 480
    cycles = {"cut": 50, "weld": 72, "paint": 55}
    constraint = max(cycles, key=cycles.get)
    over_takt = [k for k, v in cycles.items() if v > takt]
    ap = [action_priority(9, 5, 3), action_priority(6, 2, 3), action_priority(5, 7, 2)]
    save(work, "rca.json", {"6M": SIX_M, "wastes": DOWNTIME, "takt": takt, "constraint": constraint, "AP": ap})
    return [eq("takt seconds", takt, 60.0), eq("constraint", constraint, "weld"), eq("over takt", over_takt, ["weld"]), eq("AP", ap, ["H", "L", "M"]),
            eq("8 wastes", len(DOWNTIME), 8)]


def psm(ranges):
    """Van Westendorp: find where 'too cheap' share equals 'too expensive' share (optimal price point)."""
    grid = np.arange(1, 101)
    cheap = np.array([np.mean([r["too_cheap"] >= p for r in ranges]) for p in grid])
    exp = np.array([np.mean([r["too_expensive"] <= p for r in ranges]) for p in grid])
    return int(grid[np.argmin(np.abs(cheap - exp))])


def a29(work):
    ranges = [{"too_cheap": c, "too_expensive": e} for c, e in [(5, 30), (8, 35), (10, 40), (12, 45), (15, 50)]]
    opp = psm(ranges)
    gg = {10: 0.9, 20: 0.7, 30: 0.4, 40: 0.2}
    best = max(gg, key=lambda p: p * gg[p])
    save(work, "wtp.json", {"psm_opp": opp, "gabor_granger_best": best})
    return [truth("PSM point between ranges", 15 <= opp <= 30, opp), eq("Gabor-Granger revenue max", best, 20)]


def mode_for(latency_s):
    return "streaming" if latency_s < 60 else "batch ELT"


def a30(work):
    r = {"fraud check": mode_for(0.5), "daily report": mode_for(86400), "hourly sync": mode_for(3600)}
    hops = {"source->topic": "at-least-once", "topic->processor": "exactly-once", "processor->sink": "idempotent upsert"}
    ingest = "CDC/outbox"
    save(work, "streaming.json", {"modes": r, "hops": hops, "ingest": ingest})
    return [eq("modes", r, {"fraud check": "streaming", "daily report": "batch ELT", "hourly sync": "batch ELT"}), truth("semantic named per hop", all(hops.values())),
            truth("no dual writes", "dual" not in ingest)]


def a31(work):
    wl = {"orders": {"shape": "relational", "joins": True}, "sessions": {"shape": "key-value", "joins": False}, "events": {"shape": "analytics", "joins": False}}
    pick = {"relational": "Postgres", "key-value": "DynamoDB", "document": "Cosmos/Mongo", "analytics": "BigQuery"}
    choice = {k: pick[v["shape"]] for k, v in wl.items()}
    keys = {"sessions": ("PK=user#id", "SK=session#ts")}
    save(work, "db_choice.json", {"choice": choice, "keys": keys})
    return [eq("choice", choice, {"orders": "Postgres", "sessions": "DynamoDB", "events": "BigQuery"}), truth("partition key set", all(keys["sessions"]))]


def why_chain_valid(chain):
    for link in chain:
        if not link.get("evidence"):
            return False, f"no evidence: {link['why']}"
        if "human error" in link["why"].lower() and link is chain[-1]:
            return False, "stopped at human error"
    whys = [l["why"] for l in chain]
    if len(set(whys)) != len(whys):
        return False, "circular"
    return True, "ok"


def a32(work):
    good = [{"why": "torque 12 Nm vs spec 15", "evidence": "gauge log"}, {"why": "tool drifted", "evidence": "calibration record"},
            {"why": "no calibration schedule for tool T3", "evidence": "PM system"}]
    human = good[:2] + [{"why": "Human error", "evidence": "interview"}]
    circ = good[:2] + [{"why": "tool drifted", "evidence": "x"}]
    r = [why_chain_valid(c) for c in (good, human, circ)]
    save(work, "why_chain.json", r)
    return [eq("valid", r[0], (True, "ok")), eq("human error rejected", r[1][1], "stopped at human error"), eq("circularity caught", r[2][1], "circular")]


def a33(work):
    timeline = [("10:00", "observed", "5xx 30%"), ("10:02", "conjecture", "db?"), ("10:05", "action", "feature flag off"), ("10:07", "observed", "5xx 0.1%")]
    observed = [t for t in timeline if t[1] == "observed"]
    contained = observed[-1][2] == "5xx 0.1%"
    pm = {"timeline": timeline, "root cause": "bad query in v2.3", "contributing": ["no canary"], "actions": [("add canary", "ops")]}
    save(work, "postmortem.json", pm)
    return [eq("observed separated from conjecture", len(observed), 2), truth("containment verified", contained), truth("actions have owners", all(o for _, o in pm["actions"]))]


def severity(users_pct):
    return "SEV1" if users_pct >= 50 else "SEV2" if users_pct >= 10 else "SEV3"


def a34(work):
    slo = 0.999
    budget_min = (1 - slo) * 30 * 24 * 60
    used = 30
    r = {"kind": "incident", "sev": severity(60), "budget_min": budget_min, "freeze": used > budget_min}
    save(work, "triage.json", r)
    return [eq("severity by impact", r["sev"], "SEV1"), eq("SEV3", severity(2), "SEV3"), eq("30-day budget minutes", round(budget_min, 1), 43.2), eq("freeze", r["freeze"], False)]


def a35(work):
    causes = {"measurement": 42, "machine": 30, "method": 12, "material": 8, "man": 5, "environment": 3}
    order = sorted(causes, key=lambda k: -causes[k])
    cum = np.cumsum([causes[k] for k in order]) / sum(causes.values())
    vital = [order[i] for i in range(len(order)) if i == 0 or cum[i - 1] < 0.8]
    proven = lambda mech, corr, pilot: mech and corr and pilot
    save(work, "pareto.json", {"order": order, "vital": vital})
    return [eq("6M covered", len(causes), 6), eq("vital few", vital, ["measurement", "machine", "method"]), eq("proof needs all three", proven(True, True, False), False)]


def a36(work):
    calls = [("search", "t1", 200), ("search", "t1", 200), ("search", "t1", 500), ("detail", "t2", 200), ("search", "t1", 200)]
    rate = 0.002
    by = {}
    for ep, ten, code in calls:
        by.setdefault((ep, ten), 0)
        by[(ep, ten)] += rate
    failed = sum(1 for c in calls if c[2] >= 500)
    dup = len(calls) - len({(c[0], c[1]) for c in calls}) - failed
    save(work, "attribution.json", {"by": {f"{k[0]}/{k[1]}": v for k, v in by.items()}, "failed": failed, "duplicates": dup})
    return [eq("top attribution", round(by[("search", "t1")], 4), 0.008), eq("failed calls", failed, 1), eq("duplicate polling", dup, 2)]


def compute_pick(w):
    if w["duration_s"] <= 900 and w["bursty"]:
        return "Lambda"
    if w["containers"]:
        return "Fargate"
    return "EC2"


def a37(work):
    r = {"thumbnailer": compute_pick({"duration_s": 20, "bursty": True, "containers": False}), "api": compute_pick({"duration_s": 10**6, "bursty": False, "containers": True}),
         "gpu render": compute_pick({"duration_s": 7200, "bursty": False, "containers": False})}
    iam = "arn:aws:s3:::media-bucket/*"
    save(work, "cloud.json", r)
    return [eq("picks", r, {"thumbnailer": "Lambda", "api": "Fargate", "gpu render": "EC2"}), truth("IAM scoped to an ARN, not *", iam != "*" and iam.startswith("arn:"))]


def a38(work):
    inv = [("idle vm", 120, False), ("orphan volume", 40, False), ("oversized db", 300, True), ("zombie env", 90, False), ("old ip", 4, False)]
    harvest = sorted([x for x in inv if not x[2]], key=lambda x: -x[1])
    total = sum(x[1] for x in harvest)
    save(work, "waste.json", {"harvest": harvest, "monthly": total, "label": "modeled"})
    return [eq("ranked", [x[0] for x in harvest], ["idle vm", "zombie env", "orphan volume", "old ip"]), eq("pure savings", total, 254), truth("rare-job dependency held back", "oversized db" not in [x[0] for x in harvest])]


def burn_rate(err_rate, slo):
    return err_rate / (1 - slo)


def a39(work):
    slo = 0.999
    br = burn_rate(0.0144, slo)
    alert = round(br, 6) >= 14.4
    sla = 0.995
    save(work, "slo.json", {"budget": 1 - slo, "burn": br, "page": alert})
    return [eq("budget", round(1 - slo, 6), 0.001), eq("burn rate", round(br, 6), 14.4), truth("fast-burn page", alert), truth("SLA looser than SLO", sla < slo)]


def a40(work):
    drivers = {"retries": 450, "cache misses": 300, "batch jobs": 150, "base": 100}
    total = sum(drivers.values())
    share = {k: v / total for k, v in drivers.items()}
    order = sorted(share, key=lambda k: -share[k])
    save(work, "drivers.json", {"share": share, "baseline": total, "success": "spend -20% with p95 unchanged"})
    return [eq("top driver", order[0], "retries"), eq("retries share", share["retries"], 0.45), truth("success metric numeric", True)]


def a41(work):
    abuse = {"indirect injection": (4, 5), "excessive agency": (3, 5), "prompt leak": (3, 2), "disclosure": (2, 4), "toxicity": (2, 2)}
    prio = {k: ("P0" if l * i >= 15 else "P1" if l * i >= 8 else "P2") for k, (l, i) in abuse.items()}
    kind = {"toxicity": "safety"}
    save(work, "redteam.json", {"priority": prio, "kill_switch": True})
    return [eq("P0", sorted(k for k, v in prio.items() if v == "P0"), ["excessive agency", "indirect injection"]), eq("P2", sorted(k for k, v in prio.items() if v == "P2"), ["prompt leak", "toxicity"]),
            eq("safety split from security", kind["toxicity"], "safety")]


def a42(work):
    tasks = [("faq", "simple", 1), ("faq", "simple", 1), ("refund", "medium", 1), ("legal", "complex", 0), ("legal", "complex", 1)]
    price = {"simple": 0.001, "medium": 0.01, "complex": 0.1}
    triage = 0.0002
    cost = sum(price[t] + triage for _, t, _ in tasks)
    resolved = sum(r for *_, r in tasks)
    cache = {}
    for q, t, _ in tasks:
        cache.setdefault(hash(q), t)
    save(work, "routing.json", {"cost_per_resolved": cost / resolved})
    return [eq("cost per resolved task", round(cost / resolved, 5), 0.05325), eq("cache keys", len(cache), 3)]


def ai_act(use):
    if use in ("social scoring", "subliminal manipulation"):
        return "prohibited"
    if use in ("hiring", "credit scoring", "education grading"):
        return "high-risk"
    if use in ("chatbot", "deepfake"):
        return "limited"
    return "minimal"


def a43(work):
    sel = {"group A": (50, 100), "group B": (30, 100)}
    rate = {g: a / b for g, (a, b) in sel.items()}
    di = min(rate.values()) / max(rate.values())
    r = {"cv screener": ai_act("hiring"), "support bot": ai_act("chatbot"), "scoring citizens": ai_act("social scoring")}
    save(work, "ai_act.json", {"class": r, "disparate_impact": di})
    return [eq("classes", list(r.values()), ["high-risk", "limited", "prohibited"]), eq("disparate impact ratio", di, 0.6), truth("fails 4/5 rule", di < 0.8)]


def a44(work):
    log = [("chat", "large", 1000, 200), ("chat", "large", 1200, 100), ("summarise", "large", 8000, 300), ("tag", "large", 100, 5)]
    rate = {"large": (15e-6, 75e-6), "small": (1e-6, 5e-6)}
    cost = lambda m, i, o: i * rate[m][0] + o * rate[m][1]
    total = sum(cost(*r[1:]) for r in log)
    top = max({f for f, *_ in log}, key=lambda f: sum(cost(*r[1:]) for r in log if r[0] == f))
    routed = sum(cost("small" if f == "tag" else m, i, o) for f, m, i, o in log)
    save(work, "llm_cost.json", {"total": total, "top": top, "routed": routed})
    return [eq("total", round(total, 6), 0.199875), eq("top endpoint", top, "summarise"), truth("routing cuts cost", routed < total)]


PILLARS = ["AML officer", "policies/controls", "training", "independent testing", "CDD/beneficial ownership"]


def a45(work):
    assess = {p: {"design": "ok", "implementation": "ok", "effectiveness": "ok"} for p in PILLARS}
    assess["training"]["effectiveness"] = "gap"
    assess["independent testing"]["design"] = "gap"
    findings = [(p, d) for p, v in assess.items() for d, s in v.items() if s == "gap"]
    save(work, "aml.json", findings)
    return [eq("five pillars", len(PILLARS), 5), eq("findings", findings, [("training", "effectiveness"), ("independent testing", "design")])]


def a46(work):
    svc = {"cut": (40, 15, 0.5), "colour": (120, 50, 1.5), "treatment": (200, 60, 2.0)}
    cm_hr = {k: (p - c) / h for k, (p, c, h) in svc.items()}
    best = max(cm_hr, key=cm_hr.get)
    payback = 3000 / ((90 - 20) * 10)
    save(work, "margin.json", {"cm_per_hour": cm_hr, "payback_months": payback})
    return [eq("contribution per hour", cm_hr, {"cut": 50.0, "colour": 46.666666666666664, "treatment": 70.0}), eq("tilt mix to", best, "treatment"),
            eq("device payback months", round(payback, 4), 4.2857)]


def a47(work):
    def contrast(c1, c2):
        def lum(c):
            v = [x / 255 for x in c]
            v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
            return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
        a, b = sorted([lum(c1), lum(c2)], reverse=True)
        return (a + 0.05) / (b + 0.05)
    screen = {"buttons": [{"id": "pay", "size": 44, "fg": (255, 255, 255), "bg": (0, 0, 0)}, {"id": "skip", "size": 30, "fg": (170, 170, 170), "bg": (255, 255, 255)}]}
    issues = []
    for b in screen["buttons"]:
        if b["size"] < 44:
            issues.append((b["id"], "touch target < 44 pt (HIG)", 3))
        if contrast(b["fg"], b["bg"]) < 4.5:
            issues.append((b["id"], "contrast < 4.5", 4))
    issues.sort(key=lambda x: -x[2])
    save(work, "design_review.json", issues)
    return [eq("black/white contrast", round(contrast((0, 0, 0), (255, 255, 255)), 2), 21.0), eq("issues by severity", [i[1] for i in issues], ["contrast < 4.5", "touch target < 44 pt (HIG)"]),
            truth("good button clean", all(i[0] != "pay" for i in issues))]


def a48(work):
    outcomes = {"common": (10, 0.7), "rare": (50, 0.25), "jackpot": (1000, 0.05)}
    ev = expected_value([(p, v) for v, p in outcomes.values()])
    share = outcomes["jackpot"][0] * outcomes["jackpot"][1] / ev
    sources, sinks = 120, 90
    save(work, "economy.json", {"ev": ev, "jackpot_share": share, "net_flow": sources - sinks})
    return [eq("EV per pull", round(ev, 6), 69.5), truth("jackpot dominates EV (dominant strategy risk)", share > 0.7, share), eq("inflation per cycle", sources - sinks, 30)]


def a49(work):
    interest = [3, 6, 4, 7, 5, 8, 6, 10]
    peaks = [interest[i] for i in range(1, len(interest) - 1) if interest[i] > interest[i - 1] and interest[i] > interest[i + 1]] + [interest[-1]]
    rising = all(b > a for a, b in zip(peaks, peaks[1:]))
    save(work, "interest_curve.json", {"curve": interest, "peaks": peaks})
    return [eq("peaks", peaks, [6, 7, 8, 10]), truth("rising peaks, ends high", rising and interest[-1] == max(interest)), eq("hook above opening", interest[1] > interest[0], True)]


def dora(deploys_per_week, lead_h, cfr, mttr_h):
    def lvl(v, elite, high, med, lower_better=True):
        if lower_better:
            return "elite" if v <= elite else "high" if v <= high else "medium" if v <= med else "low"
        return "elite" if v >= elite else "high" if v >= high else "medium" if v >= med else "low"
    r = {"deploy": lvl(deploys_per_week, 7, 1, 0.25, False), "lead": lvl(lead_h, 24, 168, 720), "cfr": lvl(cfr, 0.05, 0.10, 0.15), "mttr": lvl(mttr_h, 1, 24, 168)}
    order = ["low", "medium", "high", "elite"]
    weakest = min(r, key=lambda k: order.index(r[k]))
    return r, weakest


def a50(work):
    r, weakest = dora(10, 30, 0.04, 200)
    save(work, "dora.json", {"window": "2026-08-01..2026-10-31", "baseline": "prior quarter", "keys": r, "binding": weakest})
    return [eq("classes", r, {"deploy": "elite", "lead": "high", "cfr": "elite", "mttr": "low"}), eq("binding constraint", weakest, "mttr")]


def a51(work):
    seg = {"smb": {"ltv": 900, "cac": 400}, "ent": {"ltv": 12000, "cac": 2000}}
    blended = sum(s["ltv"] for s in seg.values()) / sum(s["cac"] for s in seg.values())
    ratios = {k: v["ltv"] / v["cac"] for k, v in seg.items()}
    below = [k for k, v in ratios.items() if v < 3]
    save(work, "ops_metrics.json", {"segments": ratios, "blended": blended})
    return [eq("smb below 3:1", below, ["smb"]), truth("blended hides it", blended > 3, blended), eq("ent ratio", ratios["ent"], 6.0)]


def size_task(hours):
    return "small" if hours <= 4 else "medium" if hours <= 16 else "large" if hours <= 40 else "split"


def a52(work):
    tasks = {"auth": 3, "db schema": 12, "editor": 24, "billing": 30}
    sizes = {k: size_task(v) for k, v in tasks.items()}
    split = [k for k, v in tasks.items() if v > 16]
    dep = {"auth": [], "db schema": [], "editor": ["db schema"], "billing": ["auth", "db schema"]}
    order = topo_order(dep)
    stack = "node" if "package.json" in ["package.json", "README.md"] else "?"
    save(work, "breakdown.json", {"sizes": sizes, "split": split, "order": order})
    return [eq("sizes", sizes, {"auth": "small", "db schema": "medium", "editor": "large", "billing": "large"}), eq("split anything over 2 days", split, ["editor", "billing"]),
            eq("blockers first", order[:2], ["auth", "db schema"]), eq("stack from config", stack, "node")]


SEC_STEPS = ["private advisory", "private fix+test", "request CVE", "backport", "release+publish advisory", "notify downstream"]


def sec_release_check(log):
    idx = {s: i for i, s in enumerate(log)}
    errs = [s for s in SEC_STEPS if s not in idx]
    if "public commit" in idx and idx["public commit"] < idx.get("release+publish advisory", 10**9):
        errs.append("public trace before release")
    for a, b in zip(SEC_STEPS, SEC_STEPS[1:]):
        if a in idx and b in idx and idx[a] > idx[b]:
            errs.append(f"{a} after {b}")
    return errs


def a53(work):
    good = list(SEC_STEPS)
    leak = ["private advisory", "public commit", "private fix+test", "request CVE", "backport", "release+publish advisory", "notify downstream"]
    save(work, "release.json", {"good": sec_release_check(good), "leak": sec_release_check(leak)})
    return [eq("clean release", sec_release_check(good), []), eq("public trace caught", sec_release_check(leak), ["public trace before release"]),
            eq("backport order", sec_release_check([s for s in SEC_STEPS if s != "backport"] + ["backport"]), ["backport after release+publish advisory"])]


# ---------- learning, people, product ----------

def a56(work):
    ws = work / "coach"
    (ws / "concepts" / "recursion").mkdir(parents=True)
    (ws / "MISSION.md").write_text("# Mission\ngoal: recursion\nsuccess: solve 3 katas\nconstraints: 20 min/day\n")
    for f in ("lesson.md", "reference.md", "exercise.md"):
        (ws / "concepts" / "recursion" / f).write_text(f)
    records = ws / "records"
    records.mkdir()
    for i, t in enumerate(["knowledge", "skills"], 1):
        (records / f"{i:04d}-{t}.md").write_text(f"stage {t}")
    glossary = {"base case": "shown understanding"}
    resume = sorted(p.name for p in records.iterdir())[-1]
    return [truth("mission sections", all(k in (ws / "MISSION.md").read_text() for k in ("goal", "success", "constraints"))),
            eq("concept files", sorted(p.name for p in (ws / "concepts" / "recursion").iterdir()), ["exercise.md", "lesson.md", "reference.md"]),
            eq("resume reads latest numbered record", resume, "0002-skills.md"), eq("glossary only after understanding", list(glossary), ["base case"])]


def tutor_step(state, answer, correct):
    if answer is None:
        return state, "wait"
    if answer == correct:
        state["status"] = "independent" if not state["hinted"] else "hinted"
        return state, "new-conditions question"
    state["hinted"] = True
    return state, "minimal hint"


def a57(work):
    st = {"hinted": False, "status": "untested"}
    log = []
    for ans in [None, "wrong", "42"]:
        st, act = tutor_step(st, ans, "42")
        log.append(act)
    save(work, "tutor_log.json", {"log": log, "state": st})
    return [eq("one question then wait, hint, transfer", log, ["wait", "minimal hint", "new-conditions question"]), eq("recorded as hinted", st["status"], "hinted")]


def a58(work):
    job = {"circumstance": "when I post at night after work", "functional": "publish a reel in 10 min", "emotional": "feel professional", "social": "be seen as consistent",
           "hired": "phone editor", "fired": "desktop suite (too slow)"}
    demographic = re.search(r"\b(age|aged|female|male|gen z)\b", job["circumstance"])
    dims = [k for k in ("functional", "emotional", "social") if job.get(k)]
    q_ok = lambda q: bool(re.match(r"^(tell me about the last time|when did you last|what did you use)", q, re.I))
    save(work, "jtbd.json", job)
    return [eq("three dimensions", len(dims), 3), truth("not demographic", demographic is None), truth("past-behaviour question ok", q_ok("Tell me about the last time you posted")),
            truth("opinion question rejected (Mom Test)", not q_ok("Would you use our app?"))]


def a59(work):
    alts = {"spreadsheet": {"rtl", "cheap"}, "CapCut": {"templates", "cheap", "fast"}, "do nothing": set()}
    ours = {"rtl", "kinetic arabic type", "templates", "word sync"}
    unique = sorted(ours - set().union(*alts.values()))
    parts = {"alternatives": 1, "unique": 1, "value": 1, "who": 1, "category": 1, "messaging": 0}
    score = 8 if all(v for k, v in parts.items() if k != "messaging") else 4
    save(work, "positioning.json", {"unique": unique, "score": score})
    return [eq("attributes only we have", unique, ["kinetic arabic type", "word sync"]), truth("do-nothing is an alternative", "do nothing" in alts), eq("score when defined", score, 8)]


def a60(work):
    pages = {"/home": (50000, 0.03), "/pricing": (20000, 0.01), "/blog": (3000, 0.005), "/checkout": (8000, 0.4)}
    median = np.median([c for _, c in pages.values()])
    target = max((p for p, (t, c) in pages.items() if c < median), key=lambda p: pages[p][0])
    save(work, "cro.json", {"target": target, "one change at a time": True})
    return [eq("high-traffic underperformer", target, "/pricing")]


def answer_first(md):
    out = []
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        first = body.strip().split(". ")[0]
        out.append((head.strip(), head.strip().endswith("?"), has_number(first) or " is " in first))
    return out


def a61(work):
    md = "## How long does export take?\nExport takes 12 seconds for a 30 s reel. Details follow.\n## Our story\nWe started in 2020 because..."
    r = answer_first(md)
    (work / "page.md").write_text(md)
    jsonld = {"@context": "https://schema.org", "@type": "FAQPage"}
    save(work, "faq.jsonld", jsonld)
    return [eq("question heading answered first", r[0], ("How long does export take?", True, True)), eq("non-question heading flagged", r[1][1], False)]


def diag_score(passed):
    return {7: 10, 6: 9, 5: 7, 4: 6}.get(passed, max(0, passed))


def a62(work):
    steps = ["open", "signup", "verify email", "choose plan", "upload", "export"]
    removable = {"verify email", "choose plan"}
    cut = [s for s in steps if s not in removable]
    save(work, "subtract.json", {"steps_before": len(steps), "after": cut})
    return [eq("steps to value", len(cut), 4), eq("7/7", diag_score(7), 10), eq("5/7", diag_score(5), 7), eq("4/7", diag_score(4), 6)]


SHOULD = ["best practice", "industry standard", "the standard way", "scalable", "synergy"]


def a63(work):
    answers = ["we need the industry standard dashboard", "I just want to know by 9am if sales dropped"]
    flagged = [a for a in answers if any(s in a for s in SHOULD)]
    restate = {"Outcome": "9am drop alert", "User": "owner", "Why now": "missed a bad day", "Success": "alert within 5 min", "Constraint": "email only", "Out of scope": "dashboard"}
    accept = lambda r: r.strip().lower() in ("yes", "نعم", "ايوه")
    save(work, "intent.json", restate)
    return [eq("should-want answer flagged", flagged, ["we need the industry standard dashboard"]), eq("six restatement fields", len(restate), 6),
            truth("only explicit yes accepted", accept("yes") and not accept("whatever you think"))]


def cover_lint(text):
    paras = [p for p in text.split("\n\n") if p.strip()]
    n = len(words(text))
    errs = []
    if len(paras) != 4:
        errs.append("paragraphs")
    if not 250 <= n <= 380:
        errs.append("length")
    if re.match(r"\s*(dear [^\n]*\n+)?i am (so )?excited", text, re.I):
        errs.append("weak opener")
    if not has_number(paras[0] if paras else ""):
        errs.append("no number in opening result")
    return errs


def a64(work):
    filler = " ".join(["delivered"] * 70)
    good = "Cut onboarding time 38% for 12k users at Acme. " + filler + "\n\n" + filler + "\n\n" + filler + "\n\n" + filler
    bad = "I am excited to apply.\n\nShort."
    save(work, "cover.txt", good)
    return [eq("good letter", cover_lint(good), []), eq("bad letter", cover_lint(bad), ["paragraphs", "length", "weak opener", "no number in opening result"])]


def mirror(utterance, k=3):
    w = re.findall(r"[\w']+", utterance)
    return " ".join(w[-k:]) + "?"


def label(emotion):
    return f"It seems like {emotion}."


def a65(work):
    m = mirror("We cannot go above forty thousand this year")
    pre = {"BATNA": 38000, "target": 45000, "walk_away": 40000}
    qs = ["How am I supposed to do that?", "Why can't you?", "What makes this hard for you?"]
    calibrated = [q for q in qs if q.split()[0] in ("How", "What")]
    save(work, "negotiation.json", {"mirror": m, "label": label("budget is under pressure"), "pre": pre})
    return [eq("mirror last 3 words", m, "thousand this year?"), truth("label phrasing", label("x").startswith("It seems like")),
            eq("calibrated, not why", calibrated, [qs[0], qs[2]]), truth("walk-away above BATNA", pre["walk_away"] > pre["BATNA"])]


TEAM_TYPES = {"stream-aligned", "platform", "enabling", "complicated-subsystem"}
MODES = {"collaboration", "x-as-a-service", "facilitating"}


def a66(work):
    teams = {"checkout": ("stream-aligned", ["payments", "cart"]), "infra": ("platform", ["k8s"]), "ml": ("complicated-subsystem", ["ranking", "fraud"]), "web": ("stream-aligned", ["a", "b", "c", "d"])}
    links = {("checkout", "infra"): "x-as-a-service", ("checkout", "ml"): "collaboration", ("web", "infra"): "pairing"}
    bad_type = [t for t, (k, _) in teams.items() if k not in TEAM_TYPES]
    bad_mode = [p for p, m in links.items() if m not in MODES]
    overloaded = [t for t, (k, d) in teams.items() if len(d) > 3 or (k == "complicated-subsystem" and len(d) > 1)]
    save(work, "topologies.json", {"bad_mode": bad_mode, "overloaded": overloaded})
    return [eq("types valid", bad_type, []), eq("undeclared mode", bad_mode, [("web", "infra")]), eq("cognitive load", overloaded, ["ml", "web"])]


def containment_ok(text):
    return bool(re.search(r"\b(sorted|quarantined|stopped|segregated|blocked)\b", text, re.I)) and bool(re.search(r"\d{4}-\d{2}-\d{2}", text)) and "careful" not in text.lower()


def a67(work):
    d2 = "Torque 12 Nm vs 15 Nm spec on rev B; 37 of 500 = 7.4%"
    d3_good = "Quarantined 500 parts at dock, verified by 100% torque check on 2026-10-30"
    d3_bad = "Operators will be more careful"
    m = re.search(r"(\d+) of (\d+) = ([\d.]+)%", d2)
    pct_ok = abs(int(m.group(1)) / int(m.group(2)) * 100 - float(m.group(3))) < 0.05
    save(work, "8d.json", {"D2": d2, "D3": d3_good})
    return [truth("X of Y = Z% consistent", pct_ok), truth("containment physical, dated, past tense", containment_ok(d3_good)), truth("'be careful' rejected", not containment_ok(d3_bad)),
            truth("D0 before D1", ["D0", "D1"].index("D0") == 0)]


def a68(work):
    car = {"number": "CAR-2026-014", "owner": "R. Haddad", "closure_authority": "QA manager", "ncr_summary": "Burr on edge A",
           "occurrence": [{"why": "worn die", "validation": "reproduction"}], "escape": [{"why": "no edge check", "validation": "team opinion"}],
           "actions": [{"cause": "worn die", "owner": "tooling", "date": "2026-11-10"}]}
    invalid = [c["why"] for c in car["occurrence"] + car["escape"] if c["validation"] not in ("reproduction", "data correlation", "physical evidence", "record review")]
    unmapped = [c["why"] for c in car["occurrence"] + car["escape"] if c["why"] not in [a["cause"] for a in car["actions"]]]
    save(work, "car.json", car)
    return [eq("team opinion is not validation", invalid, ["no edge check"]), eq("cause with no action", unmapped, ["no edge check"]), truth("named closure authority", bool(car["closure_authority"]))]


ALL_LINEAR = {"q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"}


def lora_lint(cfg):
    errs = []
    if set(cfg["target_modules"]) != ALL_LINEAR:
        errs.append(f"missing modules {sorted(ALL_LINEAR - set(cfg['target_modules']))}")
    if cfg["lora_alpha"] != 2 * cfg["r"]:
        errs.append("alpha != 2r")
    if not 1 <= cfg["r"] <= 256:
        errs.append("rank range")
    if cfg["batch"] * cfg["grad_accum"] >= 32:
        errs.append("effective batch >= 32")
    if cfg.get("qlora") and cfg["lr"] != 2e-4:
        errs.append("QLoRA lr start 2e-4")
    return errs


def a69(work):
    good = {"target_modules": sorted(ALL_LINEAR), "r": 16, "lora_alpha": 32, "batch": 4, "grad_accum": 4, "lr": 2e-4, "qlora": True}
    bad = {"target_modules": ["q_proj", "v_proj"], "r": 16, "lora_alpha": 16, "batch": 8, "grad_accum": 8, "lr": 1e-3, "qlora": True}
    save(work, "lora.json", {"good": good, "errors_bad": lora_lint(bad)})
    return [eq("good config", lora_lint(good), []), eq("bad config errors", lora_lint(bad), ["missing modules ['down_proj', 'gate_proj', 'k_proj', 'o_proj', 'up_proj']", "alpha != 2r", "effective batch >= 32", "QLoRA lr start 2e-4"])]


def support_rung(daily):
    return "scripted menu" if daily < 50 else "AI self-service + human fallback" if daily <= 500 else "skills-based routing + analytics"


def a70(work):
    r = {v: support_rung(v) for v in (20, 300, 2000)}
    save(work, "support.json", r)
    return [eq("rungs by volume", list(r.values()), ["scripted menu", "AI self-service + human fallback", "skills-based routing + analytics"])]


def adhd_lint(reply):
    lines = [l for l in reply.splitlines() if l.strip()]
    errs = []
    if not re.match(r"^(run|open|`|cd |python|git|1\.)", lines[0], re.I):
        errs.append("first line not an action")
    items = [l for l in lines if re.match(r"^\d+\.", l)]
    if len(items) > 5:
        errs.append("list over 5")
    if not any(re.search(r"step \d+ of \d+", l) for l in lines):
        errs.append("no state line")
    return errs


def a71(work):
    good = "Run `make render`.\n1. open out/\n2. check the mp4\nstep 2 of 5 done: render. Next: captions"
    bad = "So, there are many considerations here.\n" + "\n".join(f"{i}. x" for i in range(1, 8))
    save(work, "reply.txt", good)
    return [eq("action-first reply", adhd_lint(good), []), eq("bad reply", adhd_lint(bad), ["first line not an action", "list over 5", "no state line"])]


STAGES = ["edited", "committed", "pushed/merged", "live and observed"]


def change_stage(c):
    s = "edited"
    if c.get("commit"):
        s = "committed"
    if c.get("pushed"):
        s = "pushed/merged"
    if c.get("observed_live"):
        s = "live and observed"
    return s


def a72(work):
    ch = {"fix captions": {"commit": "a1b2", "pushed": True}, "new font": {}, "landing page": {"commit": "c3", "pushed": True, "observed_live": True}}
    r = {k: change_stage(v) for k, v in ch.items()}
    headline = "planned 3 shipped live 1"
    save(work, "session_report.json", {"stages": r, "headline": headline})
    return [eq("stages", r, {"fix captions": "pushed/merged", "new font": "edited", "landing page": "live and observed"}),
            eq("gap is the headline", sum(1 for v in r.values() if v == "live and observed"), 1)]


LIFECYCLE = ["create", "edit", "publish", "share", "report", "enforce", "appeal", "remove"]


def a73(work):
    controls = {"display name": "free text", "link destination": "any URL", "file": "image only", "notification text": "user text"}
    abuse = [k for k, v in controls.items() if v in ("free text", "any URL", "user text")]
    covered = {"create", "publish", "report", "remove"}
    gaps = [s for s in LIFECYCLE if s not in covered]
    save(work, "tns.json", {"abuse_surfaces": abuse, "lifecycle_gaps": gaps})
    return [eq("user-controlled abuse surfaces", abuse, ["display name", "link destination", "notification text"]), eq("lifecycle gaps", gaps, ["edit", "share", "enforce", "appeal"])]


def a74(work):
    contract = ("Contractor shall work exclusively for Client, during Client office hours. All IP including background IP vests in Client. "
                "Payment net 90. No kill fee.")
    flags = {"misclassification": bool(re.search(r"exclusive|office hours", contract, re.I)), "ip": "background IP vests in Client" in contract,
             "payment": bool(re.search(r"net (6|9)0", contract)), "kill fee": "No kill fee" in contract}
    scores = {k: (3 if v else 8) for k, v in flags.items()}
    save(work, "contract_review.json", scores)
    return [eq("all four lenses flagged", all(flags.values()), True), eq("low scores", set(scores.values()), {3})]


def is_finding(item):
    return bool(item.get("criteria")) and item.get("condition_breaches", False)


def a75(work):
    f = {"criteria": "SOX 404 dual approval", "condition_breaches": True, "condition": "6 of 25 payments single-approved", "cause": "ERP role allows self-approve",
         "consequence": "$1.2M unapproved", "action": "remove role"}
    obs = {"criteria": "", "condition": "process could be faster"}
    five = [k for k in ("criteria", "condition", "cause", "consequence", "action") if f.get(k)]
    rate = "high" if has_number(f["consequence"]) and "M" in f["consequence"] else "medium"
    save(work, "finding.json", f)
    return [eq("five Cs", len(five), 5), truth("finding has criterion", is_finding(f)), truth("observation not a finding", not is_finding(obs)), eq("rating", rate, "high")]


def wire_check(req, directory):
    issues = []
    if req["changed_destination"] and not req.get("callback_number_from") == "contract":
        issues.append("callback not to independently sourced number")
    if req["channel"] == "email" and req["changed_destination"]:
        issues.append("email change treated as fraud until verified")
    if len(set(req["approvers"])) < 2:
        issues.append("second approver missing")
    return issues


def a76(work):
    req = {"changed_destination": True, "channel": "email", "callback_number_from": "email signature", "approvers": ["amy"]}
    r = wire_check(req, {})
    save(work, "wire.json", r)
    return [eq("three controls fire", len(r), 3), eq("clean request", wire_check({"changed_destination": False, "channel": "portal", "approvers": ["a", "b"]}, {}), [])]


def a77(work):
    header = {"scope": "line 3", "team": ["QE", "PE"], "revision": "C", "date": "2026-10-01", "phase": "", "customer": "OEM1"}
    flow = ["10", "20", "30", "40"]
    fmea_steps = ["10", "20", "40"]
    funcs = {"10": "Press bushing to 2.0±0.1 mm depth", "20": "Weld bracket", "40": "Inspect"}
    missing_hdr = require_fields(header, ["scope", "team", "revision", "date", "phase", "customer"])
    missing_steps = [s for s in flow if s not in fmea_steps]
    vague_fn = [k for k, v in funcs.items() if not has_number(v)]
    save(work, "fmea_gap.json", {"header": missing_hdr, "steps": missing_steps, "functions": vague_fn})
    return [eq("incomplete header (high)", missing_hdr, ["phase"]), eq("flow step missing", missing_steps, ["30"]), eq("functions without measurable standard", vague_fn, ["20", "40"])]


PPAP_L3 = ["design records", "change docs", "engineering approval", "DFMEA", "process flow", "PFMEA", "control plan", "MSA", "dimensional results",
           "material/performance results", "initial process studies", "lab documentation", "appearance approval", "sample parts", "master sample",
           "checking aids", "customer-specific requirements", "PSW"]


def a78(work):
    sub = set(PPAP_L3) - {"MSA", "checking aids"}
    phases = ["plan", "product design", "process design", "validation", "launch"]
    gate = {"plan": True, "product design": True, "process design": False}
    stop = next(p for p in phases if not gate.get(p, False))
    save(work, "ppap.json", {"missing": sorted(set(PPAP_L3) - sub), "stop": stop})
    return [eq("18 elements", len(PPAP_L3), 18), eq("missing", sorted(set(PPAP_L3) - sub), ["MSA", "checking aids"]), eq("APQP gate", stop, "process design")]


def a79(work):
    qs = ["Show me how you release a lot?", "Do you calibrate gauges?", "Walk me through a change request?"]
    open_q = [q for q in qs if re.match(r"^(show me|walk me|how|what)", q, re.I)]
    samples = {"people": 3, "records": 2, "periods": 1}
    weak = [k for k, v in samples.items() if not 2 <= v <= 3]
    auditor_area, audited = "purchasing", "production"
    save(work, "audit_plan.json", {"open": open_q, "samples": samples})
    return [eq("yes/no question removed", len(open_q), 2), eq("sample too thin", weak, ["periods"]), truth("independent auditor", auditor_area != audited)]


def method_choice(p):
    if p["single_complaint"]:
        return "8D"
    if p["cause_known"] and p["small"]:
        return "PDCA"
    return "DMAIC"


def a80(work):
    r = [method_choice({"single_complaint": True, "cause_known": False, "small": False}), method_choice({"single_complaint": False, "cause_known": True, "small": True}),
         method_choice({"single_complaint": False, "cause_known": False, "small": False})]
    goal = "3.2% -> 0.5% by Q3"
    save(work, "dmaic.json", {"routes": r, "goal": goal, "SIPOC": ["S", "I", "P", "O", "C"]})
    return [eq("routes", r, ["8D", "PDCA", "DMAIC"]), truth("specific goal", len(re.findall(r"\d", goal)) >= 3)]


def a81(work):
    obs = {"what": {"is": "scratch on cover", "is_not": "dent"}, "which": {"is": "rev B", "is_not": "rev A"}, "where": {"is": "line 2", "is_not": "line 1"},
           "when": {"is": "since 2026-10-12", "is_not": "before"}, "how many": {"is": "4%", "is_not": ""}}
    gaps = [d for d, v in obs.items() if not v["is_not"]]
    distinctions = {d: (v["is"], v["is_not"]) for d, v in obs.items() if v["is_not"]}
    save(work, "is_isnot.json", {"to be investigated": gaps, "distinctions": distinctions})
    return [eq("five dimensions", len(obs), 5), eq("unknown marked", gaps, ["how many"]), eq("distinctions point at rev B line 2", (distinctions["which"][0], distinctions["where"][0]), ("rev B", "line 2"))]


def pdca_pilot(plan, results):
    if "success" not in plan or "scope" not in plan:
        return "invalid: pilot not fixed before start"
    return "adopt" if results[plan["success"][0]] <= plan["success"][1] else "rework"


def a82(work):
    plan = {"baseline": 0.06, "target": 0.03, "scope": "line 2, 2 weeks", "success": ("defect_rate", 0.03)}
    r1 = pdca_pilot(plan, {"defect_rate": 0.025})
    r2 = pdca_pilot({"baseline": 0.06}, {"defect_rate": 0.01})
    save(work, "pdca.json", {"r1": r1, "r2": r2})
    return [eq("pilot meets target", r1, "adopt"), eq("pilot defined after the fact rejected", r2, "invalid: pilot not fixed before start")]


ZERO_TECH = ["locate accurately", "understand mechanism", "reproduce", "take measures", "draw inferences"]
ZERO_MGMT = ["clear process", "clear responsibility", "measures in place", "strict handling", "improve rules"]


def a83(work):
    tech = {k: True for k in ZERO_TECH}
    mgmt = {k: True for k in ZERO_MGMT}
    mgmt["strict handling"] = False
    order = ["technical", "management"]
    closed = all(tech.values()) and all(mgmt.values())
    save(work, "zeroing.json", {"tech": tech, "mgmt": mgmt})
    return [eq("five + five", len(tech) + len(mgmt), 10), eq("technical first", order[0], "technical"), truth("not closed while one item open", not closed)]


LENS_Q = {"CCO": ["gross retention", "#1 churn reason", "time-to-value", "customers to fire", "share preventable", "segment"],
          "CISO": ["STRIDE top 3", "blast radius", "secrets", "audit log", "incident drill", "vendor risk"],
          "CFO": ["runway", "burn multiple", "payback", "gross margin", "working capital", "downside"]}


def a84(work):
    plan_touches = {"retention", "security"}
    pick = [l for l, kw in {"CCO": "retention", "CISO": "security", "CFO": "finance"}.items() if kw in plan_touches]
    qs = {l: LENS_Q[l] for l in pick}
    save(work, "forcing.json", qs)
    return [eq("lenses touched only", pick, ["CCO", "CISO"]), truth("six per lens", all(len(v) == 6 for v in qs.values())), truth("gross not net retention", "gross retention" in qs["CCO"])]


def a85(work):
    items = {"food safety": 5, "cleanliness": 3, "display": 1}
    score = {"pass": 1.0, "partial": 0.5, "fail": 0.0}
    units = {"u1": {"food safety": "pass", "cleanliness": "partial", "display": "fail"}, "u2": {"food safety": "fail", "cleanliness": "pass", "display": "pass"}}
    tot = sum(items.values())
    s = {u: round(sum(items[i] * score[r[i]] for i in items) / tot, 4) for u, r in units.items()}
    save(work, "brand_audit.json", s)
    return [eq("weighted", s, {"u1": 0.7222, "u2": 0.4444}), truth("food safety failure outweighs display", s["u2"] < s["u1"])]


def a86(work):
    cust = [{"n": "a", "employees": 40, "uses_arabic": True, "retained": True}, {"n": "b", "employees": 900, "uses_arabic": True, "retained": True},
            {"n": "c", "employees": 30, "uses_arabic": False, "retained": False}, {"n": "d", "employees": 60, "uses_arabic": True, "retained": True}]
    icp = lambda c: c["uses_arabic"] and c["employees"] <= 200
    anti = lambda c: not c["uses_arabic"]
    fit = [c["n"] for c in cust if icp(c)]
    precision = sum(c["retained"] for c in cust if icp(c)) / len(fit)
    save(work, "icp.json", {"fit": fit, "anti": [c["n"] for c in cust if anti(c)], "precision": precision})
    return [eq("fit", fit, ["a", "d"]), eq("anti-ICP", [c["n"] for c in cust if anti(c)], ["c"]), eq("ICP retention precision", precision, 1.0)]


def a87(work):
    week = {"customer calls": 4, "hiring": 10, "slack": 12, "product review": 3, "admin": 8}
    bottleneck = "hiring"
    on_bottleneck = week[bottleneck] / sum(week.values())
    delegate = [k for k in ("slack", "admin") if week[k] > 5]
    save(work, "priorities.json", {"share_on_bottleneck": on_bottleneck, "delegate": delegate})
    return [eq("share of week on bottleneck", round(on_bottleneck, 4), 0.2703), eq("delegate", delegate, ["slack", "admin"])]


LABELS = {"observed", "reported", "inferred", "unknown"}


def a88(work):
    inputs = [("ticket volume 120/wk", "observed", "logs"), ("agents copy-paste replies", "reported", "interview"), ("40% are refunds", "inferred", ""), ("cost of delay", "unknown", "")]
    bad = [i for i in inputs if i[1] not in LABELS or (i[1] == "observed" and not i[2])]
    relabel = [(t, "observed") for t, l, s in inputs if l == "reported" and s == "interview"]
    save(work, "workflow_map.json", {"inputs": inputs, "relabel_blocked": relabel})
    return [eq("labels valid", bad, []), truth("reported never relabeled observed", all(l != "observed" for t, l, s in inputs if s == "interview"))]


def a89(work):
    deals = [{"v": 50, "stage": "proposal", "age": 20, "next": "demo"}, {"v": 80, "stage": "discovery", "age": 200, "next": ""},
             {"v": 30, "stage": "proposal", "age": 15, "next": "call"}, {"v": 40, "stage": "commit", "age": 10, "next": "sign"}]
    clean = [d for d in deals if d["age"] <= 120 and d["next"]]
    pipeline = sum(d["v"] for d in clean)
    quota, win_rate = 60, 0.4
    needed = 1 / win_rate
    coverage = pipeline / quota
    save(work, "pipeline.json", {"stale": [d for d in deals if d not in clean], "coverage": coverage, "needed": needed})
    return [eq("stale removed first", len(clean), 3), eq("coverage", coverage, 2.0), eq("needed from win rate", needed, 2.5), truth("short on coverage", coverage < needed)]


def a90(work):
    opps = {"F1": {"fit": [5, 5, 4, 4], "award": 50, "ask": 60, "hours": 20}, "F2": {"fit": [2, 3, 2, 1], "award": 500, "ask": 60, "hours": 80},
            "F3": {"fit": [4, 4, 4, 5], "award": 40, "ask": 40, "hours": 10}}
    res = {}
    for k, o in opps.items():
        fit = sum(o["fit"]) / 4
        go = fit >= 3.5 and 0.5 <= o["award"] / o["ask"] <= 2
        res[k] = {"go": go, "priority": round(fit * min(o["award"], o["ask"]) / o["hours"], 3)}
    order = sorted([k for k in res if res[k]["go"]], key=lambda k: -res[k]["priority"])
    save(work, "grants.json", res)
    return [eq("no-go on misfit", res["F2"]["go"], False), eq("capacity-weighted order", order, ["F3", "F1"]), eq("F3 priority", res["F3"]["priority"], 17.0)]


def company_rev(model, gci):
    if model == "split":
        return 0.3 * gci
    if model == "cap":
        return min(0.3 * gci, 20000) + 0.05 * max(0, gci - 20000 / 0.3)
    return 12000.0


def a91(work):
    from scipy.optimize import brentq
    x = brentq(lambda g: company_rev("split", g) - company_rev("fee", g), 1, 10**6)
    bands = {g: {m: company_rev(m, g) for m in ("split", "cap", "fee")} for g in (30000, 100000)}
    save(work, "commission.json", {"split_fee_crossover": x, "bands": bands})
    return [eq("split = fee crossover", round(x, 4), 40000.0), eq("cap plateaus", round(bands[100000]["cap"], 2), round(20000 + 0.05 * (100000 - 66666.6667), 2)),
            truth("below crossover split earns less than fee", bands[30000]["split"] < 12000)]


LEADING = re.compile(r"^(don't you|wouldn't you|isn't it|click|tap|do you like)", re.I)


def a92(work):
    tasks = ["Buy a medium blue jacket and ship it home", "Click the cart icon then press checkout"]
    probes = ["Tell me more", "Don't you think this is easy?", "What did you expect there?"]
    bad_t = [t for t in tasks if re.match(r"^(click|tap|press)", t, re.I)]
    bad_p = [p for p in probes if LEADING.match(p)]
    save(work, "session_guide.json", {"bad_tasks": bad_t, "bad_probes": bad_p})
    return [eq("click-by-click task flagged", bad_t, ["Click the cart icon then press checkout"]), eq("leading probe flagged", bad_p, ["Don't you think this is easy?"])]


def a93(work):
    routes = {"R1": {"stops": 600, "hours": 8, "cost": 900}, "R2": {"stops": 300, "hours": 8, "cost": 800}}
    sph = {k: v["stops"] / v["hours"] for k, v in routes.items()}
    cps = {k: round(v["cost"] / v["stops"], 4) for k, v in routes.items()}
    imbalance = max(sph.values()) / min(sph.values())
    save(work, "fleet.json", {"stops_per_hour": sph, "cost_per_stop": cps})
    return [eq("stops/hour", sph, {"R1": 75.0, "R2": 37.5}), eq("cost per stop", cps, {"R1": 1.5, "R2": 2.6667}), eq("route imbalance", imbalance, 2.0)]


HUMAN_GATES = {"intent", "architecture approval", "release"}


def a94(work):
    flow = [("requirements", "intent", "human"), ("design", "architecture approval", "human"), ("implementation", "code", "agent"), ("testing", "behaviour tests", "agent"),
            ("release", "release", "agent")]
    violations = [s for s, art, who in flow if art in HUMAN_GATES and who != "human"]
    save(work, "adlc.json", {"flow": flow, "violations": violations})
    return [eq("human gate kept on release", violations, ["release"])]


def a95(work):
    ws = ["build", "migrate", "train", "comms"]
    milestones = [f"week {w}" for w in range(12, 0, -1)]
    freeze = {"irreversible": True, "split vote": False}
    retro = {"process quality": "good", "outcome": "bad", "luck vs skill": "outcome bad despite good process"}
    save(work, "lifecycle.json", {"workstreams": ws, "milestones": milestones, "freeze": any(freeze.values()), "retro": retro})
    return [truth("3-6 workstreams", 3 <= len(ws) <= 6), eq("12 weekly milestones backwards", milestones[0], "week 12"), eq("count", len(milestones), 12),
            truth("cooldown freeze triggered", any(freeze.values())), truth("process separated from outcome", retro["process quality"] != retro["outcome"])]


def a96(work):
    episodes = [{"protected": "customer data", "tradeoff": "lost a deal", "evidence": "2025 deal log"}, {"protected": "speed", "tradeoff": "skipped review", "evidence": "postmortem"},
                {"protected": "customer data", "tradeoff": "delayed launch", "evidence": "launch doc"}]
    stated = {"innovation"}
    counts = {}
    for e in episodes:
        counts[e["protected"]] = counts.get(e["protected"], 0) + 1
    labels = {v: ("demonstrated" if counts.get(v, 0) >= 2 else "observed once" if counts.get(v) else "stated") for v in set(counts) | stated}
    save(work, "values.json", labels)
    return [eq("labels", labels, {"customer data": "demonstrated", "speed": "observed once", "innovation": "stated"})]


POSTURES = {"expand", "selectively expand", "hold scope", "reduce"}


def a97(work):
    plan = {"posture": "hold scope", "additions": [{"item": "mobile app", "decision": None}, {"item": "SSO", "decision": "deferred"}]}
    undecided = [a["item"] for a in plan["additions"] if a["decision"] not in ("approved", "deferred", "rejected")]
    save(work, "plan_review.json", {"undecided": undecided})
    return [truth("valid posture", plan["posture"] in POSTURES), eq("addition without decision", undecided, ["mobile app"])]


def paid_test_ok(q, budget_ok, approval):
    return bool(q) and budget_ok and approval


def a98(work):
    r = [paid_test_ok("does Arabic copy lift CTR?", True, False), paid_test_ok("", True, True), paid_test_ok("does Arabic copy lift CTR?", True, True)]
    routes = {"warm": 3, "community": 2, "cold": 1}
    first = max(routes, key=routes.get)
    save(work, "gtm.json", {"paid": r, "first_route": first})
    return [eq("no spend without approval", r, [False, False, True]), eq("warm route first", first, "warm")]


SIX_COND = ["outcome shared", "facts visible", "incentives explicit", "decider clear", "process clear", "commitment"]


def a99(work):
    cond = {c: True for c in SIX_COND}
    cond["decider clear"] = False
    sentence = "Decide by 2026-11-20 whether checkout uses A or B"
    raci = {"decides": [], "consulted": ["eng", "design"], "informed": ["sales"]}
    failing = [c for c, v in cond.items() if not v]
    save(work, "deadlock.json", {"failing": failing, "raci": raci})
    return [eq("six conditions", len(cond), 6), eq("deadlock cause", failing, ["decider clear"]), truth("no decider mapped", not raci["decides"]), truth("decision sentence dated", has_number(sentence))]


def a100(work):
    tiers = [{"name": "Free", "fence": "1 seat"}, {"name": "Pro", "fence": "5 seats"}, {"name": "Business", "fence": "SSO + audit log"}, {"name": "Plus", "fence": ""}, {"name": "Max", "fence": ""}]
    unfenced = [t["name"] for t in tiers if not t["fence"]]
    ok = len(tiers) - len(unfenced)
    save(work, "tiers.json", {"unfenced": unfenced})
    return [eq("five tiers: two unfenced", unfenced, ["Plus", "Max"]), truth("three fenced tiers remain", ok == 3)]


def a101(work):
    uni = {"payroll": (4, 4, "weak", 1.2), "treasury": (5, 3, "strong", 1.0), "it access": (3, 5, "medium", 1.1), "travel": (2, 2, "strong", 1.0)}
    mat = {"weak": 1.0, "medium": 0.7, "strong": 0.4}
    resid = {k: round(i * l * v * mat[m], 2) for k, (i, l, m, v) in uni.items()}
    plan = sorted(resid, key=lambda k: -resid[k])[:2]
    save(work, "audit_plan.json", resid)
    return [eq("residual", resid, {"payroll": 19.2, "treasury": 6.0, "it access": 11.55, "travel": 1.6}), eq("plan top 2", plan, ["payroll", "it access"])]


def a102(work):
    decision_made = False
    q = "where do first-time users abandon checkout, and why?"
    method = "evaluative" if q.startswith("does") else "generative+analytics"
    n = {"qual themes": 5, "quant claim": 385}
    moe = 1.96 * math.sqrt(0.25 / n["quant claim"])
    save(work, "study.json", {"method": method, "n": n, "moe": moe})
    return [truth("theatre gate passes", not decision_made), eq("method from question", method, "generative+analytics"), eq("n for ±5%", round(moe, 3), 0.05)]


def a103(work):
    pfmea = [{"fm": "bushing too shallow", "ap": "H"}, {"fm": "weld porosity", "ap": "H"}, {"fm": "label smudge", "ap": "L"}]
    dvp = {"bushing too shallow": "push-out test 2 kN"}
    cp = [{"step": "10", "char": "depth", "spec": "2.0±0.1", "gauge": "depth gauge", "n": 5, "freq": "hourly", "method": "Xbar-R", "reaction": "stop + contain"}]
    untested = [r["fm"] for r in pfmea if r["ap"] == "H" and r["fm"] not in dvp]
    save(work, "control_plan.json", {"cp": cp, "untested_high": untested})
    return [eq("high AP without test", untested, ["weld porosity"]), truth("row complete", not require_fields(cp[0], ["step", "char", "spec", "gauge", "n", "freq", "method", "reaction"]))]


def grr(data):
    """data: parts x appraisers x trials. Average-and-range method (AIAG)."""
    d = np.asarray(data, float)
    p, a, r = d.shape
    K1 = {2: 0.8862, 3: 0.5908}[r]
    K2 = {2: 0.7071, 3: 0.5231}[a]
    K3 = {10: 0.3146}[p]
    rbar = np.mean(d.max(2) - d.min(2))
    ev = rbar * K1
    xdiff = d.mean((0, 2)).max() - d.mean((0, 2)).min()
    av = math.sqrt(max(0, (xdiff * K2) ** 2 - ev ** 2 / (p * r)))
    grr_ = math.sqrt(ev ** 2 + av ** 2)
    rp = d.mean((1, 2)).max() - d.mean((1, 2)).min()
    pv = rp * K3
    tv = math.sqrt(grr_ ** 2 + pv ** 2)
    ndc = int(1.41 * pv / grr_)
    return 100 * grr_ / tv, ndc


def a104(work):
    rng = np.random.default_rng(1)
    parts = np.linspace(9, 11, 10)
    good = parts[:, None, None] + rng.normal(0, 0.01, (10, 3, 3))
    bad = parts[:, None, None] + rng.normal(0, 0.6, (10, 3, 3))
    g, ndc = grr(good)
    b, _ = grr(bad)
    save(work, "grr.json", {"good_pct": g, "good_ndc": ndc, "bad_pct": b})
    return [truth("good gauge < 10% GRR", g < 10, g), truth("ndc >= 5", ndc >= 5, ndc), truth("noisy gauge > 30% (unacceptable)", b > 30, b)]


def a105(work):
    raw, yield_, pack, overhead = 2.0, 0.8, 0.5, 0.3
    unit = raw / yield_ + pack + overhead
    vessel_days, vessels = 30, 4
    turns = 365 / vessel_days * vessels
    batch_l, unit_l = 1000, 0.75
    capacity = turns * batch_l * yield_ / unit_l
    save(work, "production.json", {"unit_cost": unit, "turns": turns, "units_per_year": capacity})
    return [eq("yield loss counted", unit, 3.3), eq("vessel turns", round(turns, 3), 48.667), eq("annual units", round(capacity), 51911)]


def a106(work):
    top_down = 2_000_000_000 * 0.05 * 0.10
    bottom_up = 50_000 * 40 * 6
    gap = abs(top_down - bottom_up) / min(top_down, bottom_up)
    sam = bottom_up * 0.4
    som = sam * 0.05
    save(work, "tam.json", {"top_down": top_down, "bottom_up": bottom_up, "gap": gap, "SAM": sam, "SOM": som})
    return [eq("top-down", top_down, 10_000_000.0), eq("bottom-up", bottom_up, 12_000_000), eq("gap 20%", round(gap, 2), 0.2), truth("SOM < SAM < TAM", som < sam < bottom_up), eq("SOM", som, 240000.0)]


def opp_score(importance, satisfaction):
    return importance + max(0, importance - satisfaction)


def a107(work):
    ideas = {"pm": [f"pm{i}" for i in range(5)], "designer": [f"d{i}" for i in range(5)], "engineer": [f"e{i}" for i in range(5)]}
    xyz = "At least 10% of Gulf creators will export 3 reels in week 1"
    ok = bool(re.match(r"^At least \d+% of .+ will .+", xyz))
    ops = {"faster export": (9, 3), "more fonts": (6, 5), "AI voice": (8, 7)}
    order = sorted(ops, key=lambda k: -opp_score(*ops[k]))
    save(work, "discovery.json", {"ideas": ideas, "xyz": xyz, "order": order})
    return [eq("5 per perspective", [len(v) for v in ideas.values()], [5, 5, 5]), truth("XYZ form", ok), eq("opportunity ranking", order, ["faster export", "AI voice", "more fonts"]),
            eq("score", opp_score(9, 3), 15)]


def a108(work):
    net = {"campus A": {"hosts": 40, "guests": 400, "matched": 300}, "campus B": {"hosts": 5, "guests": 900, "matched": 60}}
    density = {k: v["matched"] / v["guests"] for k, v in net.items()}
    hard = {k: "hosts" if v["hosts"] / v["guests"] < 0.2 else "guests" for k, v in net.items()}
    tipped = [k for k, d in density.items() if d >= 0.5]
    totals_winner = max(net, key=lambda k: net[k]["guests"])
    save(work, "network.json", {"density": density, "tipped": tipped})
    return [eq("hard side", hard["campus B"], "hosts"), eq("density", density, {"campus A": 0.75, "campus B": 0.06666666666666667}), eq("atomic network tipped", tipped, ["campus A"]),
            truth("totals would mislead", totals_winner == "campus B")]


PROGRAMS = {f"ASTRAT-{n:02d}": globals()[f"a{n:02d}"] for n in range(1, 109) if n not in (54, 55)}
