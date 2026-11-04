"""Shared deterministic helpers for the mind group's program modules (atlas-strategy, atlas-mind,
mental-models, thinking-core, self-discovery, creativity-engine, strategy-finance,
planning-execution, story-direction-ideas).

Each helper is a real procedure (graph search, scoring, simulation, validation). The cards'
programs call them with the card's own fixture and parameters and check known answers.
The leading underscore keeps this file out of power_programs.all_programs().
"""
from __future__ import annotations
import json
import math
import random
import re
from itertools import product
from pathlib import Path


def save(work: Path, name: str, obj) -> Path:
    p = Path(work) / name
    if isinstance(obj, (dict, list)):
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    else:
        p.write_text(str(obj), encoding="utf-8")
    return p


def eq(name, got, want, tol=None):
    if tol is None:
        ok = got == want
    else:
        ok = abs(float(got) - float(want)) <= tol
    return (name, bool(ok), f"got={got!r} want={want!r}")


def truth(name, cond, observed=""):
    return (name, bool(cond), str(observed))


# ---------- graphs ----------

def topo_order(deps: dict) -> list:
    """deps: node -> list of prerequisites. Kahn's algorithm; raises on a cycle."""
    indeg = {n: 0 for n in deps}
    for n, ps in deps.items():
        for p in ps:
            indeg.setdefault(p, 0)
    for n, ps in deps.items():
        indeg[n] = len(ps)
    users = {n: [] for n in indeg}
    for n, ps in deps.items():
        for p in ps:
            users[p].append(n)
    ready = sorted(n for n, d in indeg.items() if d == 0)
    order = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for u in sorted(users[n]):
            indeg[u] -= 1
            if indeg[u] == 0:
                ready.append(u)
        ready.sort()
    if len(order) != len(indeg):
        raise ValueError("cycle")
    return order


def has_cycle(deps: dict) -> bool:
    try:
        topo_order(deps)
        return False
    except ValueError:
        return True


def critical_path(durations: dict, deps: dict):
    """Longest path through a DAG of tasks. Returns (length, path, earliest_finish, slack)."""
    order = topo_order({k: deps.get(k, []) for k in durations})
    ef, prev = {}, {}
    for n in order:
        start = 0
        prev[n] = None
        for p in deps.get(n, []):
            if ef[p] > start:
                start, prev[n] = ef[p], p
        ef[n] = start + durations[n]
    end = max(ef, key=lambda k: (ef[k], k))
    total = ef[end]
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    # latest finish for slack
    succ = {n: [m for m in durations if n in deps.get(m, [])] for n in durations}
    lf = {}
    for n in reversed(order):
        lf[n] = min([lf[s] - durations[s] for s in succ[n]] or [total])
    slack = {n: lf[n] - ef[n] for n in durations}
    return total, path, ef, slack


def reachable(edges: dict, start) -> set:
    seen, stack = set(), [start]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(edges.get(n, []))
    return seen


def find_cycles_signs(edges: dict):
    """edges: (a,b)->sign(+1/-1). Return simple cycles with their polarity (R or B)."""
    nodes = sorted({a for a, _ in edges} | {b for _, b in edges})
    adj = {n: [b for (a, b) in edges if a == n] for n in nodes}
    cycles = []

    def dfs(start, cur, path):
        for nxt in adj[cur]:
            if nxt == start:
                cycles.append(list(path))
            elif nxt not in path and nxt > start:
                dfs(start, nxt, path + [nxt])
    for s in nodes:
        dfs(s, s, [s])
    out = []
    for c in cycles:
        sign = 1
        for i, a in enumerate(c):
            sign *= edges[(a, c[(i + 1) % len(c)])]
        out.append((c, "R" if sign > 0 else "B"))
    return out


# ---------- decision maths ----------

def weighted_scores(options: dict, weights: dict) -> dict:
    return {o: round(sum(weights[c] * s[c] for c in weights), 6) for o, s in options.items()}


def rank(scores: dict) -> list:
    return sorted(scores, key=lambda k: (-scores[k], k))


def expected_value(outcomes):
    return sum(p * v for p, v in outcomes)


def bayes(prior, p_e_true, p_e_false):
    num = prior * p_e_true
    return num / (num + (1 - prior) * p_e_false)


def ice(impact, confidence, effort):
    return impact * confidence / effort


def rice(reach, impact, confidence, effort):
    return reach * impact * confidence / effort


def monte_carlo(fn, n, seed):
    rng = random.Random(seed)
    return [fn(rng) for _ in range(n)]


def percentile(xs, q):
    s = sorted(xs)
    k = (len(s) - 1) * q / 100.0
    f = math.floor(k)
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


def npv(rate, flows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def irr(flows, lo=-0.99, hi=10.0):
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(mid, flows) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def brier(probs, outcomes):
    return sum((p - o) ** 2 for p, o in zip(probs, outcomes)) / len(probs)


def pareto_front(points: dict, maximize=("a", "b")):
    """points: name -> dict; returns names not dominated on all maximize keys."""
    front = []
    for n, p in points.items():
        dom = False
        for m, q in points.items():
            if m == n:
                continue
            if all(q[k] >= p[k] for k in maximize) and any(q[k] > p[k] for k in maximize):
                dom = True
                break
        if not dom:
            front.append(n)
    return sorted(front)


def minimax_regret(payoff: dict):
    """payoff: option -> {scenario: value}. Returns (best option, regret table)."""
    scen = list(next(iter(payoff.values())).keys())
    best = {s: max(payoff[o][s] for o in payoff) for s in scen}
    reg = {o: max(best[s] - payoff[o][s] for s in scen) for o in payoff}
    return min(reg, key=lambda o: (reg[o], o)), reg


def maximin(payoff: dict):
    worst = {o: min(v.values()) for o, v in payoff.items()}
    return max(worst, key=lambda o: (worst[o], o)), worst


# ---------- text / structure ----------

WORD = re.compile(r"[\w؀-ۿ']+", re.UNICODE)


def words(text: str) -> list:
    return WORD.findall(text.lower())


def sections(md: str) -> list:
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.+)$", md, re.M)]


def mece(items: dict, buckets: dict):
    """items: item -> set of features; buckets: name -> predicate(features). Returns (overlaps, gaps)."""
    overlaps, gaps = [], []
    for it, f in items.items():
        hits = [b for b, pred in buckets.items() if pred(f)]
        if len(hits) > 1:
            overlaps.append((it, hits))
        if not hits:
            gaps.append(it)
    return overlaps, gaps


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 1.0


def require_fields(obj: dict, fields) -> list:
    return [f for f in fields if not str(obj.get(f, "")).strip()]


VAGUE = {"fast", "quick", "easy", "simple", "intuitive", "robust", "scalable", "user-friendly",
         "nice", "clean", "good", "better", "efficient", "seamless", "modern", "soon", "flexible"}


def vague_terms(text: str) -> list:
    return sorted({w for w in words(text) if w in VAGUE})


def has_number(text: str) -> bool:
    return bool(re.search(r"\d", text))


def grid(*axes):
    return list(product(*axes))


def stock_flow(stock0, inflow, outflow_rate, steps):
    s, hist = stock0, [stock0]
    for _ in range(steps):
        s = s + inflow - outflow_rate * s
        hist.append(round(s, 9))
    return hist
