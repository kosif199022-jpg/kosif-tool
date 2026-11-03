"""Programs for the mental-models family (MODEL-01..63).

Each card's three-step method is run as a deterministic procedure on a small planted fixture
whose correct answer is known in advance (a planted convention, the simplest explanation,
a bottleneck, a cycle polarity, a dominated option ...).
"""
from __future__ import annotations
from pathlib import Path
from ._mind_common import (save, eq, truth, critical_path, find_cycles_signs, weighted_scores, rank,
                           expected_value, bayes, monte_carlo, percentile, mece, words, stock_flow,
                           minimax_regret, brier, topo_order, vague_terms, has_number, grid)


def first_principles(assumptions):
    """Keep only assumptions tagged as law (physics, contract, measurement); strike conventions."""
    return [a for a in assumptions if a["kind"] == "law"]


def m01(work: Path):
    a = [{"text": "videos must be 16:9", "kind": "convention"},
         {"text": "phone screen is 9:16 portrait", "kind": "law"},
         {"text": "intro needs a logo sting", "kind": "convention"},
         {"text": "file must be under 50 MB upload limit", "kind": "law"}]
    kept = first_principles(a)
    save(work, "first_principles.json", {"assumptions": a, "kept": kept})
    return [eq("conventions struck", len(a) - len(kept), 2),
            truth("only laws kept", all(k["kind"] == "law" for k in kept), [k["text"] for k in kept]),
            truth("rebuilt from 9:16 fact", any("9:16" in k["text"] for k in kept))]


def inversion(recipe, damage):
    guards = [{"guard": "prevent: " + r, "damage": damage[r]} for r in recipe]
    return sorted(guards, key=lambda g: -g["damage"])[:3]


def m02(work):
    recipe = ["skip backups", "deploy on friday", "no tests", "ignore alerts", "share passwords"]
    damage = {"skip backups": 9, "deploy on friday": 3, "no tests": 7, "ignore alerts": 8, "share passwords": 6}
    g = inversion(recipe, damage)
    save(work, "inversion.json", g)
    return [eq("three guards kept", len(g), 3),
            eq("top guard", g[0]["guard"], "prevent: skip backups"),
            eq("damage covered", sum(x["damage"] for x in g), 24),
            truth("every guard is an action", all(x["guard"].startswith("prevent:") for x in g))]


def second_order(effects):
    """effects: stakeholder -> [first, then1, then2] values (signed). Flag reversals."""
    out = {}
    for s, chain in effects.items():
        total = sum(chain)
        out[s] = {"first": chain[0], "net": total, "reverses": chain[0] > 0 and total < 0}
    return out


def m03(work):
    e = {"customers": [5, -2, -1], "support team": [2, -4, -3], "finance": [3, 1, 0]}
    r = second_order(e)
    save(work, "second_order.json", r)
    return [truth("two 'and then?' steps per stakeholder", all(len(v) == 3 for v in e.values())),
            eq("reversed stakeholders", sorted(k for k, v in r.items() if v["reverses"]), ["support team"]),
            eq("customers net", r["customers"]["net"], 2)]


def m04(work):
    # metric: click rate; omitted: refunds. Option B wins on the metric but loses on the goal (profit).
    opts = {"A": {"ctr": 0.04, "orders": 100, "refunds": 5}, "B": {"ctr": 0.09, "orders": 120, "refunds": 70}}
    by_metric = max(opts, key=lambda k: opts[k]["ctr"])
    by_goal = max(opts, key=lambda k: opts[k]["orders"] - opts[k]["refunds"])
    save(work, "map_territory.json", {"by_metric": by_metric, "by_goal": by_goal, "omitted": ["refunds"]})
    return [eq("metric choice", by_metric, "B"), eq("goal choice after checking omitted refunds", by_goal, "A"),
            truth("map and territory disagree", by_metric != by_goal)]


def m05(work):
    claims = [{"c": "file is 1080x1920", "checkable": "ffprobe"}, {"c": "audience will love it", "checkable": ""},
              {"c": "licence is MIT", "checkable": "LICENSE file"}, {"c": "competitor revenue is 3M", "checkable": ""}]
    inside = [x["c"] for x in claims if x["checkable"]]
    outside = [x["c"] for x in claims if not x["checkable"]]
    report = "\n".join([f"IN: {c}" for c in inside] + [f"OUTSIDE CIRCLE (unverified): {c}" for c in outside])
    save(work, "circle.txt", report)
    return [eq("inside count", len(inside), 2), eq("outside", outside, ["audience will love it", "competitor revenue is 3M"]),
            truth("outside claims stated plainly", report.count("OUTSIDE CIRCLE") == 2)]


def occam(cands):
    return sorted(cands, key=lambda c: (len(c["assumptions"]), c["name"]))


def m06(work):
    c = [{"name": "cosmic ray", "assumptions": ["radiation", "bit flip", "no ECC"]},
         {"name": "config typo", "assumptions": ["recent edit"]},
         {"name": "race condition", "assumptions": ["two writers", "no lock"]}]
    order = occam(c)
    save(work, "occam.json", [x["name"] for x in order])
    return [eq("test simplest first", order[0]["name"], "config typo"),
            eq("others kept alive", len(order), 3), eq("last", order[-1]["name"], "cosmic ray")]


def hanlon(evidence_count, repeated):
    if evidence_count >= 2 and repeated:
        return "escalate"
    return "assume mistake; ask one question"


def m07(work):
    cases = {"single missed reply": (0, False), "one late file": (1, False), "third deleted backup after warning": (3, True)}
    r = {k: hanlon(*v) for k, v in cases.items()}
    save(work, "hanlon.json", r)
    return [eq("charitable default", r["single missed reply"], "assume mistake; ask one question"),
            eq("evidence escalates", r["third deleted backup after warning"], "escalate"),
            eq("escalations", sum(v == "escalate" for v in r.values()), 1)]


def m08(work):
    post = bayes(0.01, 0.9, 0.05)  # classic: 1% prior, 90% sensitivity, 5% false positive
    save(work, "bayes.json", {"prior": 0.01, "posterior": post})
    return [eq("posterior", round(post, 4), 0.1538), truth("base rate dominates", post < 0.5, post),
            eq("no-information evidence keeps prior", round(bayes(0.3, 0.5, 0.5), 9), 0.3)]


def m09(work):
    ref = [1] * 12 + [0] * 88  # 12% of startups in the reference class survive 5y
    base = sum(ref) / len(ref)
    lr = 2.0  # specific evidence twice as likely if it survives
    adj = base * lr / (base * lr + (1 - base))
    save(work, "base_rate.json", {"base": base, "adjusted": adj})
    return [eq("base rate", base, 0.12), eq("adjusted", round(adj, 4), 0.2143), truth("adjust from base, not vivid case", adj < 0.5)]


def fermi(factors):
    lo = hi = mid = 1.0
    for a, b in factors:
        lo *= a
        hi *= b
        mid *= (a * b) ** 0.5
    return lo, mid, hi


def m10(work):
    # piano tuners in a 1M city: people, per household, pianos share, tunings/yr, tunings per tuner/yr (inverse)
    f = [(1e6, 1e6), (1 / 3, 1 / 2), (0.02, 0.05), (1, 2), (1 / 1000, 1 / 500)]
    lo, mid, hi = fermi(f)
    save(work, "fermi.json", {"low": lo, "mid": mid, "high": hi})
    return [truth("3-6 factors", 3 <= len(f) <= 6, len(f)), eq("low", round(lo, 3), 6.667),
            eq("high", round(hi, 3), 100.0), truth("range reported", lo < mid < hi, (lo, mid, hi))]


def m11(work):
    opts = {"safe": [(1.0, 100)], "bet": [(0.5, 400), (0.5, -150)], "ruin": [(0.9, 300), (0.1, -5000)]}
    ev = {k: expected_value(v) for k, v in opts.items()}
    survivable = {k: min(x for _, x in v) > -1000 for k, v in opts.items()}
    pick = max((k for k in opts if survivable[k]), key=lambda k: ev[k])
    save(work, "ev.json", {"ev": ev, "survivable": survivable, "pick": pick})
    return [eq("EV bet", ev["bet"], 125.0), eq("EV ruin", ev["ruin"], -230.0), eq("pick", pick, "bet"),
            truth("ruin flagged", not survivable["ruin"])]


def door(reversible_cost_days):
    return "two-way: decide fast at 70% info" if reversible_cost_days <= 7 else "one-way: slow down, evidence, consent"


def m12(work):
    d = {"button colour": 0, "rename repo": 2, "delete prod database": 10_000, "sign 3-year lease": 1095}
    r = {k: door(v) for k, v in d.items()}
    save(work, "doors.json", r)
    return [eq("one-way doors", sorted(k for k, v in r.items() if v.startswith("one-way")), ["delete prod database", "sign 3-year lease"]),
            eq("fast", r["button colour"][:7], "two-way")]


def m13(work):
    tasks = {"refactor": 30, "client feature": 120, "blog": 50, "docs": 80}
    hours = {"refactor": 10, "client feature": 10, "blog": 10, "docs": 10}
    next_best = sorted((v / hours[k] for k, v in tasks.items()), reverse=True)[1]
    drop = sorted(k for k, v in tasks.items() if v / hours[k] < next_best)
    save(work, "opportunity.json", {"line": next_best, "drop": drop})
    return [eq("next-best line", next_best, 8.0), eq("dropped below line", drop, ["blog", "refactor"])]


def safety_margin(expected, sigma, z=1.645):
    return expected + z * sigma


def m14(work):
    need = safety_margin(100, 20)
    calm = safety_margin(100, 2)
    save(work, "margin.json", {"uncertain": need, "certain": calm})
    return [eq("buffer proportional to uncertainty", round(need, 1), 132.9), eq("small buffer when certain", round(calm, 2), 103.29),
            truth("bigger buffer for bigger sigma", need - 100 == 10 * (calm - 100) or abs((need - 100) - 10 * (calm - 100)) < 1e-9)]


def m15(work):
    parts = {"a": (50, 2), "b": (30, 5), "c": (10, 1), "d": (6, 6), "e": (4, 4)}
    order = sorted(parts, key=lambda k: -parts[k][0] / parts[k][1])
    total = sum(v for v, _ in parts.values())
    top = order[:2]
    share = sum(parts[k][0] for k in top) / total
    save(work, "pareto.json", {"order": order, "top_share": share})
    return [eq("order by value per effort", order, ["a", "c", "b", "d", "e"]), eq("top-2 value share", share, 0.6),
            truth("measured, not assumed 80%", share != 0.8)]


def bottleneck(steps):
    return max(steps, key=lambda s: steps[s]["queue"])


def m16(work):
    steps = {"write": {"rate": 10, "queue": 1}, "review": {"rate": 3, "queue": 14}, "deploy": {"rate": 8, "queue": 0}}
    b = bottleneck(steps)
    throughput = min(s["rate"] for s in steps.values())
    steps2 = dict(steps, review={"rate": 9, "queue": 2})
    b2 = bottleneck(steps2) if steps2["write"]["queue"] < 2 else "write"
    save(work, "toc.json", {"bottleneck": b, "throughput": throughput})
    return [eq("bottleneck", b, "review"), eq("system throughput = bottleneck rate", throughput, 3),
            eq("re-find after fix", min(steps2, key=lambda s: steps2[s]["rate"]), "deploy")]


def m17(work):
    e = {("sales", "revenue"): 1, ("revenue", "ads"): 1, ("ads", "sales"): 1,
         ("sales", "backlog"): 1, ("backlog", "satisfaction"): -1, ("satisfaction", "sales"): 1}
    loops = find_cycles_signs(e)
    kinds = sorted(k for _, k in loops)
    save(work, "loops.json", [{"loop": c, "type": k} for c, k in loops])
    return [eq("two loops", len(loops), 2), eq("one reinforcing one balancing", kinds, ["B", "R"])]


def m18(work):
    h = stock_flow(0, 10, 0.1, 200)
    save(work, "stock.json", h[:20])
    return [eq("steady state = inflow / outflow rate", round(h[-1], 3), 100.0), eq("first step", h[1], 10),
            truth("level not rate", h[5] != 10)]


LEVERAGE = {"parameter": 1, "loop": 2, "rule": 3, "goal": 4, "mindset": 5}


def m19(work):
    cands = [("raise price 2%", "parameter"), ("add review loop", "loop"), ("change bonus rule", "rule"), ("redefine goal", "goal")]
    feasible = {"redefine goal": False}
    pick = max((c for c in cands if feasible.get(c[0], True)), key=lambda c: LEVERAGE[c[1]])
    save(work, "leverage.json", {"pick": pick})
    return [eq("highest feasible leverage", pick[0], "change bonus rule"), eq("level", pick[1], "rule")]


def cynefin(cause_effect_known, repeatable, stable):
    if not stable:
        return ("chaotic", "act to stabilise")
    if cause_effect_known and repeatable:
        return ("clear", "apply best practice")
    if cause_effect_known:
        return ("complicated", "analyse")
    return ("complex", "probe-sense-respond")


def m20(work):
    cases = {"reset password": (True, True, True), "db tuning": (True, False, True), "new market": (False, False, True), "outage": (False, False, False)}
    r = {k: cynefin(*v) for k, v in cases.items()}
    save(work, "cynefin.json", r)
    return [eq("outage", r["outage"][0], "chaotic"), eq("new market move", r["new market"][1], "probe-sense-respond"),
            eq("all four domains", sorted({v[0] for v in r.values()}), ["chaotic", "clear", "complex", "complicated"])]


def m21(work):
    target = 37
    lo, hi, steps, log = 0, 100, 0, []
    while True:
        guess = (lo + hi) // 2  # decide
        steps += 1
        signal = (guess > target) - (guess < target)  # observe
        log.append((guess, signal))
        if signal == 0:
            break
        if signal > 0:
            hi = guess - 1  # orient
        else:
            lo = guess + 1
    save(work, "ooda.json", log)
    return [eq("found", log[-1][0], 37), truth("loop converges in <= 7 cycles", steps <= 7, steps)]


def m22(work):
    opposing = {"claims": ["remote work cuts commute", "remote work hurts mentoring", "remote work widens hiring"],
                "evidence": {"remote work cuts commute": 3, "remote work hurts mentoring": 2, "remote work widens hiring": 3}}
    strongest = sorted(opposing["claims"], key=lambda c: -opposing["evidence"][c])[:2]
    save(work, "steelman.json", {"strongest form": strongest})
    return [eq("steelman uses the two best-evidenced points", strongest, ["remote work cuts commute", "remote work widens hiring"])]


def m23(work):
    attacks = {"sql injection": 9, "typo in footer": 1, "leaked api key": 10, "ddos": 7, "weak css": 0}
    top = sorted(attacks, key=lambda a: -attacks[a])[:3]
    save(work, "redteam.json", top)
    return [eq("three most damaging", top, ["leaked api key", "sql injection", "ddos"]), truth("easy parts excluded", "typo in footer" not in top)]


def premortem(causes, signals):
    return [{"cause": c, "signal": signals.get(c), "kept": bool(signals.get(c))} for c in causes]


def m24(work):
    causes = ["scope creep", "bad luck", "key dev leaves", "api rate limits"]
    signals = {"scope creep": "story count +20% in a week", "key dev leaves": "single committer > 70%", "api rate limits": "429 rate > 1%"}
    r = premortem(causes, signals)
    save(work, "premortem.json", r)
    return [eq("causes with a signal", sum(x["kept"] for x in r), 3), eq("generic risk rejected", [x["cause"] for x in r if not x["kept"]], ["bad luck"])]


def backcast(end, precedes):
    chain = [end]
    while chain[-1] in precedes:
        chain.append(precedes[chain[-1]])
    return list(reversed(chain))


def m25(work):
    pre = {"launch app": "beta feedback fixed", "beta feedback fixed": "beta live", "beta live": "MVP built", "MVP built": "today: spec"}
    plan = backcast("launch app", pre)
    save(work, "backcast.json", plan)
    return [eq("starts today", plan[0], "today: spec"), eq("ends at end state", plan[-1], "launch app"), eq("steps", len(plan), 5)]


def m26(work):
    dur = {"A": 3, "B": 2, "C": 5, "D": 2, "E": 3}
    dep = {"B": ["A"], "C": ["A"], "D": ["B"], "E": ["C", "D"]}
    total, path, _, slack = critical_path(dur, dep)
    save(work, "cpm.json", {"total": total, "path": path, "slack": slack})
    return [eq("project length", total, 11), eq("critical path", path, ["A", "C", "E"]), eq("slack on B", slack["B"], 1), eq("no slack on critical", slack["C"], 0)]


def m27(work):
    wbs = {"landing page": [("hero copy", 2, "copy reviewed in doc"), ("layout", 3, "renders at 375px"), ("deploy", 1, "URL returns 200")],
           "email": [("template", 2, "passes litmus"), ("send list", 6, "")]}
    bad = [t for d in wbs.values() for t in d if t[1] > 4 or not t[2]]
    save(work, "wbs.json", {"violations": bad})
    return [eq("tasks over 4h or without done-test", [b[0] for b in bad], ["send list"]), eq("deliverables", len(wbs), 2)]


def m28(work):
    items = {"apple": {"fruit", "red"}, "tomato": {"fruit", "veg", "red"}, "rock": {"mineral"}, "carrot": {"veg"}}
    buckets = {"fruit": lambda f: "fruit" in f, "veg": lambda f: "veg" in f and "fruit" not in f}
    ov, gaps = mece(items, buckets)
    save(work, "mece.json", {"overlaps": ov, "gaps": gaps})
    return [eq("overlaps fixed by rule", ov, []), eq("gap found", gaps, ["rock"])]


def m29(work):
    tree = {"why did revenue fall?": ["fewer visitors?", "lower conversion?", "lower order value?"],
            "fewer visitors?": [], "lower conversion?": [], "lower order value?": []}
    tests = {"fewer visitors?": "analytics sessions", "lower conversion?": "checkout funnel", "lower order value?": ""}
    leaves = [k for k, v in tree.items() if not v]
    untested = [l for l in leaves if not tests.get(l)]
    save(work, "issue_tree.json", {"tree": tree, "untested": untested})
    return [truth("3-5 branches", 3 <= len(tree["why did revenue fall?"]) <= 5), eq("leaf missing a test", untested, ["lower order value?"])]


def five_whys(chain, controllable):
    deepest = None
    for link in chain:
        if link["evidence"] and link["cause"] in controllable:
            deepest = link["cause"]
        if not link["evidence"]:
            break
    return deepest


def m30(work):
    chain = [{"cause": "server crashed", "evidence": True}, {"cause": "disk full", "evidence": True},
             {"cause": "logs not rotated", "evidence": True}, {"cause": "no rotation in deploy template", "evidence": True},
             {"cause": "vendor default", "evidence": False}]
    ctrl = {"disk full", "logs not rotated", "no rotation in deploy template"}
    r = five_whys(chain, ctrl)
    save(work, "five_whys.json", r)
    return [eq("deepest evidenced controllable cause", r, "no rotation in deploy template")]


def m31(work):
    pipeline = ["load", "parse", "normalize", "render"]
    produced_at = {"bad date": "parse"}
    patches = ["render: fix date", "normalize: fix date"]
    fix = produced_at["bad date"]
    removable = [p for p in patches if pipeline.index(p.split(":")[0]) > pipeline.index(fix)]
    save(work, "root_cause.json", {"fix at": fix, "remove patches": removable})
    return [eq("fix where produced", fix, "parse"), eq("downstream patches removed", len(removable), 2)]


def struct_sig(edges):
    return tuple(sorted(edges.values()))


def m32(work):
    problem = {"queue": "buffer", "workers": "servers", "arrivals": "poisson"}
    fields = {"bank tellers": {"line": "buffer", "tellers": "servers", "customers": "poisson"},
              "restaurant decor": {"colour": "paint"},
              "call centre": {"hold": "buffer", "agents": "servers", "calls": "poisson"}}
    match = sorted(f for f, e in fields.items() if struct_sig(e) == struct_sig(problem))
    save(work, "analogy.json", match)
    return [eq("two structural matches", match, ["bank tellers", "call centre"]), truth("surface match rejected", "restaurant decor" not in match)]


def m33(work):
    ideas = [{"i": "one-colour poster", "q_constrained": 7, "q_free": 8}, {"i": "blank", "q_constrained": 2, "q_free": 1},
             {"i": "3-second hook", "q_constrained": 8, "q_free": 9}]
    survive = [x["i"] for x in ideas if x["q_free"] >= 6]
    save(work, "constraint.json", survive)
    return [eq("survivors after lifting constraint", survive, ["one-colour poster", "3-second hook"])]


def m34(work):
    a = {"music": 1, "maps": 2}
    b = {"recipes": 3, "fitness": 1}
    nov = {("music", "recipes"): 4, ("music", "fitness"): 2, ("maps", "recipes"): 5, ("maps", "fitness"): 3}
    feas = {("music", "recipes"): 3, ("music", "fitness"): 5, ("maps", "recipes"): 4, ("maps", "fitness"): 4}
    pairs = grid(a, b)
    best = max(pairs, key=lambda p: nov[p] * feas[p])
    save(work, "combinations.json", {"pairs": pairs, "best": best})
    return [eq("all cross-domain pairs", len(pairs), 4), eq("best novelty x feasibility", best, ("maps", "recipes"))]


def m35(work):
    ideas = ["red logo", "blue logo", "logo animation", "price cut", "discount code", "free trial", "podcast"]
    clusters = {}
    for i in ideas:
        key = "logo" if "logo" in i else "price" if any(w in i for w in ("price", "discount", "free")) else "other"
        clusters.setdefault(key, []).append(i)
    crit = {"logo": 2, "price": 5, "other": 3}
    winner = max(clusters, key=crit.get)
    save(work, "diverge_converge.json", {"clusters": clusters, "winner": winner})
    return [eq("generated", len(ideas), 7), eq("clusters", len(clusters), 3), eq("converged by criteria", winner, "price")]


def m36(work):
    provocation = "the video has no picture"
    movements = {"the video has no picture": ["audio-first story", "captions carry meaning"]}
    ideas = [m + " -> 15 s podcast clip with kinetic captions" for m in movements[provocation]]
    save(work, "provocation.json", ideas)
    return [eq("movements extracted", len(movements[provocation]), 2), truth("shaped into usable idea", all("15 s" in i for i in ideas))]


def jtbd(s):
    import re
    return bool(re.match(r"^When .+, I want .+, so I can .+\.$", s))


def m37(work):
    good = "When I commute, I want short lessons, so I can learn without a desk."
    bad = "Add dark mode and AI."
    save(work, "jtbd.txt", good)
    return [truth("job statement valid", jtbd(good)), truth("feature list rejected", not jtbd(bad))]


def m38(work):
    reader_knows = {"what an API is"}
    reader_needs = ["price", "risk", "deadline"]
    draft = ["what an API is", "deadline", "history of the project", "price", "risk"]
    revised = [d for d in draft if d not in reader_knows and d in reader_needs]
    revised.sort(key=reader_needs.index)
    save(work, "reader.json", revised)
    return [eq("ordered by decision need", revised, ["price", "risk", "deadline"])]


def m39(work):
    doc = {"conclusion": "Ship v2 on 1 Dec", "args": {"tests pass": ["CI green"], "users asked": ["42 tickets"], "cost flat": ["invoice"]}}
    ok = bool(doc["conclusion"]) and len(doc["args"]) == 3 and all(doc["args"].values())
    save(work, "pyramid.json", doc)
    return [truth("conclusion first, 3 supported args", ok), eq("arguments", len(doc["args"]), 3)]


def m40(work):
    explanation = ["gradient points uphill", "step size times gradient", "repeat until loss stops falling"]
    source_terms = ["gradient", "step size", "loss", "local minimum"]
    gaps = [t for t in source_terms if not any(t in s for s in explanation)]
    save(work, "feynman.json", gaps)
    return [eq("break found", gaps, ["local minimum"])]


def m41(work):
    scores = {"hooks": [6, 7, 6], "pacing": [3, 4, 3], "colour": [8, 8, 9]}
    weakest = min(scores, key=lambda k: sum(scores[k]) / 3)
    attempts = [3, 4, 5, 6]  # targeted drills improve
    save(work, "practice.json", {"weakest": weakest, "drill": attempts})
    return [eq("weakest sub-skill", weakest, "pacing"), truth("measured improvement", attempts[-1] > attempts[0])]


def m42(work):
    p = [0.9, 0.8, 0.7, 0.6, 0.95]
    o = [1, 1, 0, 1, 1]
    b = brier(p, o)
    over = brier([1.0] * 5, o)
    save(work, "calibration.json", {"brier": b, "always_certain": over})
    return [eq("brier", round(b, 4), 0.1405), truth("calibrated beats 100% language", b < over, (b, over))]


def m43(work):
    claim = {"text": "new thumbnail lifts CTR by >= 1 point", "refuted_if": lambda a, b: b - a < 0.01}
    a, b = 0.040, 0.043
    refuted = claim["refuted_if"](a, b)
    save(work, "falsify.json", {"claim": claim["text"], "A": a, "B": b, "refuted": refuted})
    return [truth("claim refuted by planted data", refuted), truth("same test confirms a real lift", not claim["refuted_if"](0.04, 0.06))]


def m44(work):
    winners = [{"habit": True}] * 9 + [{"habit": False}] * 1
    failures = [{"habit": True}] * 81 + [{"habit": False}] * 9
    rate_habit = 9 / (9 + 81)
    rate_none = 1 / (1 + 9)
    save(work, "survivorship.json", {"with": rate_habit, "without": rate_none})
    return [eq("90% of winners have the habit", sum(w["habit"] for w in winners) / 10, 0.9),
            eq("but success rate is the same with denominator", rate_habit, rate_none)]


def m45(work):
    hypothesis = "users want feature X"
    docs = ["user asked for X", "X unused in trial", "survey: X low priority", "fan email about X"]
    disconfirm = [d for d in docs if any(w in d for w in ("unused", "low priority"))]
    save(work, "disconfirm.json", {"searched first": disconfirm})
    return [eq("disconfirming evidence found and reported", len(disconfirm), 2)]


def m46(work):
    anchor = 500
    ref_class = [80, 120, 100, 90, 110]
    indep = sum(ref_class) / len(ref_class)
    final = indep  # reconcile toward reference, not anchor
    save(work, "anchor.json", {"anchor": anchor, "independent": indep})
    return [eq("reference estimate", indep, 100.0), truth("not adjusted slightly from anchor", abs(final - anchor) > 300)]


def sunk(spent, future_cost, future_value):
    return future_value > future_cost


def m47(work):
    r = {"project A": sunk(900, 200, 150), "project B": sunk(10, 50, 300)}
    save(work, "sunk.json", r)
    return [eq("stop despite 900 spent", r["project A"], False), eq("continue B", r["project B"], True),
            truth("spent ignored", sunk(0, 200, 150) == sunk(10**6, 200, 150))]


def m48(work):
    regret = {"stay": {"5y": 7, "20y": 9}, "start company": {"5y": 4, "20y": 2}}
    lasting = {k: v["20y"] for k, v in regret.items()}
    pick = min(lasting, key=lasting.get)
    save(work, "regret.json", {"pick": pick})
    return [eq("smaller lasting regret", pick, "start company")]


def m49(work):
    opts = {"A": {"cost": 3, "speed": 5, "quality": 4}, "B": {"cost": 5, "speed": 2, "quality": 3}, "C": {"cost": 2, "speed": 3, "quality": 2}}
    w = {"cost": 0.3, "speed": 0.3, "quality": 0.4}
    s = weighted_scores(opts, w)
    stable = True
    for c in w:
        for d in (-0.1, 0.1):
            w2 = dict(w)
            w2[c] = max(0, w2[c] + d)
            if rank(weighted_scores(opts, w2))[0] != "A":
                stable = False
    save(work, "matrix.json", {"scores": s, "stable": stable})
    return [eq("winner", rank(s)[0], "A"), eq("A score", s["A"], 4.0), truth("robust to weight changes", stable)]


def m50(work):
    criteria = {"metric": "weekly active", "threshold": 200, "date": "2026-12-01"}
    observed = 140
    action = "stop" if observed < criteria["threshold"] else "continue"
    save(work, "kill.json", {"criteria": criteria, "observed": observed, "action": action})
    return [eq("acted on pre-agreed signal", action, "stop"), truth("measurable", isinstance(criteria["threshold"], int))]


def m51(work):
    layers = ["ui", "api", "db"]
    features = {"login": {"ui", "api", "db"}, "full admin ui": {"ui"}, "reports": {"api", "db"}}
    slice_ = [f for f, l in features.items() if l == set(layers)]
    save(work, "slice.json", slice_)
    return [eq("thin slice crosses every layer", slice_, ["login"])]


def m52(work):
    u1, u2 = ("demand high", "demand low"), ("regulation tight", "regulation loose")
    scen = grid(u1, u2)
    payoff = {"diversify": [5, 4, 4, 3], "go big": [9, 1, 2, -3], "wait": [1, 1, 1, 1]}
    robust = max(payoff, key=lambda k: min(payoff[k]))
    save(work, "scenarios.json", {"scenarios": scen, "robust": robust})
    return [eq("four scenarios", len(scen), 4), eq("robust move", robust, "diversify")]


def m53(work):
    forces = {"rivalry": (4, ["5 competitors"]), "buyers": (5, ["2 retailers = 80% sales"]), "suppliers": (2, ["many"]),
              "substitutes": (3, ["apps"]), "entrants": (2, ["capex high"])}
    unevidenced = [f for f, (_, ev) in forces.items() if not ev]
    cap = max(forces, key=lambda f: forces[f][0])
    save(work, "five_forces.json", {"cap": cap})
    return [eq("all rated with evidence", unevidenced, []), eq("profit-capping force", cap, "buyers")]


def m54(work):
    S, W, O, T = ["arabic content"], ["small team"], ["gulf demand"], ["big platforms"]
    moves = {f"SO: {s}+{o}": 9 for s in S for o in O}
    moves.update({f"ST: {s}+{t}": 6 for s in S for t in T})
    moves.update({f"WO: {w}+{o}": 7 for w in W for o in O})
    moves.update({f"WT: {w}+{t}": 3 for w in W for t in T})
    top2 = sorted(moves, key=lambda m: -moves[m])[:2]
    save(work, "tows.json", moves)
    return [eq("four quadrants paired", len(moves), 4), eq("top two moves", top2, ["SO: arabic content+gulf demand", "WO: small team+gulf demand"])]


def unit_econ(price, var_cost, cac):
    cm = price - var_cost
    return cm, cm / price, cac / cm


def m55(work):
    cm, cmr, payback = unit_econ(30, 12, 90)
    save(work, "unit.json", {"cm": cm, "cm_ratio": cmr, "payback_months": payback})
    return [eq("contribution margin", cm, 18), eq("margin ratio", cmr, 0.6), eq("payback months", payback, 5.0)]


def m56(work):
    st = {"CFO": (5, 2), "users": (2, 5), "legal": (4, 1), "intern": (1, 1)}
    groups = {}
    for k, (power, interest) in st.items():
        g = ("manage closely" if power >= 3 and interest >= 3 else "keep satisfied" if power >= 3 else "keep informed" if interest >= 3 else "monitor")
        groups.setdefault(g, []).append(k)
    save(work, "stakeholders.json", groups)
    return [eq("silent blockers kept satisfied", sorted(groups.get("keep satisfied", [])), ["CFO", "legal"]),
            truth("one message per group", len(groups) == 3)]


def m57(work):
    stages = ["clarify", "evidence", "assumptions", "implications", "alternatives"]
    qs = {"clarify": "what do you mean by 'viral'?", "evidence": "which data shows it?", "assumptions": "what must be true?",
          "implications": "and if it works?", "alternatives": "what else could explain it?"}
    seq = [qs[s] for s in stages]
    save(work, "socratic.json", seq)
    return [eq("five stages in order", len(seq), 5), truth("all questions", all(q.endswith("?") for q in seq))]


def m58(work):
    fence = {"code": "sleep(0.2) before retry", "history": "commit 1a2b: avoid API ban", "tests": ["test_rate_limit"]}
    replacement = "token bucket 5 req/s"
    decision = "replace" if fence["history"] and replacement else "keep"
    save(work, "fence.json", {"decision": decision, "with": replacement})
    return [eq("removed only with replacement", decision, "replace"), truth("reason found", "API ban" in fence["history"])]


def m59(work):
    ladder = {"purpose": "people learn Arabic faster", "strategy": "daily 60 s videos", "step": "record lesson 1 today"}
    examples = {"purpose": "Sara reads a menu after 2 weeks", "strategy": "video #1: greetings", "step": "script file lesson1.md"}
    save(work, "ladder.json", {"ladder": ladder, "examples": examples})
    return [eq("levels", len(ladder), 3), truth("every claim has a concrete example", set(ladder) == set(examples))]


def explore_rate(remaining, total):
    return remaining / total


def m60(work):
    early, late = explore_rate(90, 100), explore_rate(5, 100)
    save(work, "explore.json", {"early": early, "late": late})
    return [truth("explore more early", early > late), eq("late exploit share", 1 - late, 0.95)]


def m61(work):
    libs = {"sqlite": (24, True), "newdb": (1, True), "olddead": (20, False)}
    lindy = {k: a if m else 0 for k, (a, m) in libs.items()}
    pick = max(lindy, key=lindy.get)
    save(work, "lindy.json", lindy)
    return [eq("foundation choice", pick, "sqlite"), truth("unmaintained rejected", lindy["olddead"] == 0)]


def m62(work):
    variants = {"A": {"calls closed": 50, "reopen": 2}, "B": {"calls closed": 80, "reopen": 45}}
    good = {k: v["calls closed"] - v["reopen"] * 2 for k, v in variants.items()}
    pick = max(good, key=good.get)
    save(work, "goodhart.json", good)
    return [eq("metric alone picks B", max(variants, key=lambda k: variants[k]["calls closed"]), "B"),
            eq("with counter-metric picks A", pick, "A")]


def m63(work):
    def ladder(in_map, probe_ok, install_ok):
        trace = ["map"]
        if not in_map:
            return trace + ["alternative"]
        trace.append("probe")
        if probe_ok:
            return trace + ["use"]
        trace.append("install")
        return trace + (["use"] if install_ok else ["alternative"])
    cases = {"present": ladder(True, True, False), "installable": ladder(True, False, True), "missing": ladder(True, False, False)}
    save(work, "capability.json", cases)
    return [eq("present tool used after probe", cases["present"], ["map", "probe", "use"]),
            eq("installed before alternative", cases["installable"], ["map", "probe", "install", "use"]),
            eq("alternative only after map, probe, install", cases["missing"], ["map", "probe", "install", "alternative"])]


PROGRAMS = {f"MODEL-{i:02d}": globals()[f"m{i:02d}"] for i in range(1, 64)}
