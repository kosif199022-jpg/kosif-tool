#!/usr/bin/env python3
"""رياضيات القرار: مونت كارلو ونقطة التعادل وترتيب ICE والقيمة الحالية ونقطة انقلاب القرار.
Decision math: Monte Carlo profit ranges, break-even, ICE ranking, NPV/IRR and decision flip thresholds.

Serves the atlas-strategy and strategy-finance power families ("show the probability of loss and the
P5-P95 range instead of one expected profit", "compute the threshold of the assumptions that would change
the decision in code, not by guessing"). Python standard library only, offline, deterministic.

Model file (montecarlo, flip):
  {"inputs": {"price": {"dist": "triangular", "low": 8, "mode": 10, "high": 13},
              "units": {"dist": "uniform", "low": 800, "high": 1200},
              "cost":  {"dist": "normal", "mean": 6, "sd": 0.5},
              "fixed": 2500},
   "profit": "(price - cost) * units - fixed",
   "target": 0}
  An input is a number (constant) or a distribution: triangular(low, mode, high), uniform(low, high),
  normal(mean, sd). "profit" is an arithmetic expression over the inputs (+ - * / ** parentheses,
  min/max/abs/round). "target" is the profit the decision needs (default 0). An optional "base" key on a
  distribution overrides its base value (triangular=mode, uniform=midpoint, normal=mean) used by flip.

Commands
  montecarlo MODEL.json [--runs N] [--seed S]
      P5/P10/P50/P90/P95, mean, sd and probability that profit < target.
      e.g. python3 scripts/decision_math.py montecarlo model.json --runs 20000 --seed 7
  breakeven --price P --fixed F --variable V
      break-even units (exact and rounded up), revenue and contribution margin.
      e.g. python3 scripts/decision_math.py breakeven --price 25 --fixed 10000 --variable 15
  ice BACKLOG.csv
      ICE ranking (impact x confidence x ease, each 1-10) of a CSV with columns name,impact,confidence,ease.
      e.g. python3 scripts/decision_math.py ice backlog.csv
  npv --rate R --flows CF0,CF1,...
      NPV at rate R (CF0 at t=0, undiscounted) and IRR by bisection when the flows change sign.
      e.g. python3 scripts/decision_math.py npv --rate 0.1 --flows -1000,300,400,500
  flip MODEL.json --var X [--lo A --hi B]
      With every other input at its base value, the value of X where profit crosses the target
      (bisection), and on which side the decision is go / no-go.
      e.g. python3 scripts/decision_math.py flip model.json --var price
  --self-test   run a small offline check and exit 0

Output is JSON on stdout (--text for a short human summary). File arguments accept '-' for stdin. Bad input: exit 2 with one line on stderr.
"""
import argparse
import ast
import csv
import io
import json
import math
import operator
import random
import sys
from pathlib import Path


def read_text(path):
    """Read a UTF-8 file, or stdin when path is '-'."""
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8-sig")


class BadInput(ValueError):
    pass


# ---------------------------------------------------------------- safe expression
_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
_UN = {ast.USub: operator.neg, ast.UAdd: operator.pos}
_FN = {"min": min, "max": max, "abs": abs, "round": round}


def compile_expr(text):
    try:
        tree = ast.parse(str(text), mode="eval")
    except SyntaxError as e:
        raise BadInput("profit expression does not parse: %s" % e.msg)
    names = set()

    def check(n):
        if isinstance(n, ast.Expression):
            check(n.body)
        elif isinstance(n, ast.BinOp) and type(n.op) in _BIN:
            check(n.left); check(n.right)
        elif isinstance(n, ast.UnaryOp) and type(n.op) in _UN:
            check(n.operand)
        elif isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            pass
        elif isinstance(n, ast.Name):
            names.add(n.id)
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FN and not n.keywords:
            for a in n.args:
                check(a)
        else:
            raise BadInput("profit expression uses a disallowed element: %s" % type(n).__name__)
    check(tree)
    names -= set(_FN)
    return tree.body, names


def eval_expr(node, env):
    if isinstance(node, ast.BinOp):
        try:
            return _BIN[type(node.op)](eval_expr(node.left, env), eval_expr(node.right, env))
        except ZeroDivisionError:
            return float("nan")
    if isinstance(node, ast.UnaryOp):
        return _UN[type(node.op)](eval_expr(node.operand, env))
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, ast.Call):
        return _FN[node.func.id](*[eval_expr(a, env) for a in node.args])
    raise BadInput("unexpected expression node")


# ---------------------------------------------------------------- model
def _num(v, what):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise BadInput("%s must be a finite number" % what)
    return float(v)


def load_model(path):
    try:
        d = json.loads(read_text(path))
    except FileNotFoundError:
        raise BadInput("model file not found: %s" % path)
    except json.JSONDecodeError as e:
        raise BadInput("model is not valid JSON: %s" % e.msg)
    return parse_model(d)


def parse_model(d):
    if not isinstance(d, dict) or not isinstance(d.get("inputs"), dict) or not d["inputs"]:
        raise BadInput("model needs a non-empty 'inputs' object")
    if not isinstance(d.get("profit"), str):
        raise BadInput("model needs a 'profit' expression string")
    inputs = {}
    for name, spec in d["inputs"].items():
        if not name.isidentifier():
            raise BadInput("input name is not an identifier: %s" % name)
        if isinstance(spec, (int, float)) and not isinstance(spec, bool):
            inputs[name] = {"dist": "const", "value": _num(spec, name)}
            continue
        if not isinstance(spec, dict):
            raise BadInput("input %s must be a number or a distribution object" % name)
        dist = spec.get("dist")
        if dist == "triangular":
            lo, mo, hi = (_num(spec.get(k), "%s.%s" % (name, k)) for k in ("low", "mode", "high"))
            if not lo <= mo <= hi or lo == hi:
                raise BadInput("input %s needs low <= mode <= high and low < high" % name)
            s = {"dist": dist, "low": lo, "mode": mo, "high": hi, "base": mo}
        elif dist == "uniform":
            lo, hi = (_num(spec.get(k), "%s.%s" % (name, k)) for k in ("low", "high"))
            if not lo < hi:
                raise BadInput("input %s needs low < high" % name)
            s = {"dist": dist, "low": lo, "high": hi, "base": (lo + hi) / 2}
        elif dist == "normal":
            mu, sd = _num(spec.get("mean"), name + ".mean"), _num(spec.get("sd"), name + ".sd")
            if sd <= 0:
                raise BadInput("input %s needs sd > 0" % name)
            s = {"dist": dist, "mean": mu, "sd": sd, "base": mu}
        else:
            raise BadInput("input %s: dist must be triangular, uniform or normal" % name)
        if "base" in spec:
            s["base"] = _num(spec["base"], name + ".base")
        inputs[name] = s
    expr, names = compile_expr(d["profit"])
    missing = sorted(names - set(inputs))
    if missing:
        raise BadInput("profit expression uses undefined inputs: %s" % ", ".join(missing))
    target = _num(d.get("target", 0), "target")
    return {"inputs": inputs, "expr": expr, "profit": d["profit"], "target": target}


def base_env(model):
    return {k: (s["value"] if s["dist"] == "const" else s["base"]) for k, s in model["inputs"].items()}


def draw(s, rng):
    if s["dist"] == "const":
        return s["value"]
    if s["dist"] == "triangular":
        return rng.triangular(s["low"], s["high"], s["mode"])
    if s["dist"] == "uniform":
        return rng.uniform(s["low"], s["high"])
    return rng.gauss(s["mean"], s["sd"])


def percentile(sorted_xs, p):
    """Linear interpolation between closest ranks (numpy 'linear', Excel PERCENTILE.INC)."""
    n = len(sorted_xs)
    if n == 1:
        return sorted_xs[0]
    pos = (n - 1) * p
    i = int(math.floor(pos))
    j = min(i + 1, n - 1)
    return sorted_xs[i] + (sorted_xs[j] - sorted_xs[i]) * (pos - i)


def montecarlo(model, runs=10000, seed=1):
    if runs < 10 or runs > 2_000_000:
        raise BadInput("--runs must be between 10 and 2000000")
    rng = random.Random(seed)
    names = sorted(model["inputs"])
    out = []
    for _ in range(runs):
        env = {k: draw(model["inputs"][k], rng) for k in names}
        v = eval_expr(model["expr"], env)
        if isinstance(v, (int, float)) and math.isfinite(v):
            out.append(float(v))
    if not out:
        raise BadInput("the profit expression produced no finite values")
    out.sort()
    n = len(out)
    mean = sum(out) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in out) / (n - 1)) if n > 1 else 0.0
    loss = sum(1 for x in out if x < model["target"])
    r = lambda x: round(x, 4)
    return {"command": "montecarlo", "runs": runs, "valid_runs": n, "seed": seed, "target": model["target"],
            "profit": model["profit"], "mean": r(mean), "sd": r(sd), "min": r(out[0]), "max": r(out[-1]),
            "p5": r(percentile(out, .05)), "p10": r(percentile(out, .10)), "p50": r(percentile(out, .50)),
            "p90": r(percentile(out, .90)), "p95": r(percentile(out, .95)),
            "prob_below_target": round(loss / n, 4),
            "base_case_profit": r(eval_expr(model["expr"], base_env(model)))}


def breakeven(price, fixed, variable):
    for v, w in ((price, "--price"), (fixed, "--fixed"), (variable, "--variable")):
        if not math.isfinite(v) or v < 0:
            raise BadInput("%s must be a non-negative number" % w)
    margin = price - variable
    if margin <= 0:
        raise BadInput("price must exceed variable cost per unit (no break-even exists)")
    units = fixed / margin
    return {"command": "breakeven", "price": price, "fixed": fixed, "variable": variable,
            "contribution_margin": round(margin, 6), "margin_ratio": round(margin / price, 6),
            "units_exact": round(units, 6), "units": int(math.ceil(units - 1e-9)),
            "revenue": round(units * price, 4)}


def ice(path):
    try:
        rows = list(csv.DictReader(io.StringIO(read_text(path))))
    except FileNotFoundError:
        raise BadInput("backlog file not found: %s" % path)
    if not rows:
        raise BadInput("backlog CSV has no rows")
    cols = {c.strip().lower(): c for c in rows[0].keys() if c}
    need = ["name", "impact", "confidence", "ease"]
    miss = [c for c in need if c not in cols]
    if miss:
        raise BadInput("backlog CSV is missing columns: %s" % ", ".join(miss))
    items = []
    for i, row in enumerate(rows, 2):
        sc = {}
        for c in need[1:]:
            try:
                v = float(row[cols[c]])
            except (TypeError, ValueError):
                raise BadInput("line %d: %s is not a number" % (i, c))
            if not 1 <= v <= 10:
                raise BadInput("line %d: %s must be between 1 and 10" % (i, c))
            sc[c] = v
        items.append({"name": (row[cols["name"]] or "").strip(), **sc,
                      "ice": round(sc["impact"] * sc["confidence"] * sc["ease"], 4),
                      "ice_mean": round((sc["impact"] + sc["confidence"] + sc["ease"]) / 3, 4), "line": i})
    items.sort(key=lambda x: (-x["ice"], -x["impact"], x["line"]))
    for k, x in enumerate(items, 1):
        x["rank"] = k
    return {"command": "ice", "formula": "impact*confidence*ease (each 1-10, max 1000)",
            "count": len(items), "items": items}


def npv_value(rate, flows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def irr(flows, lo=-0.9999, hi=10.0, tol=1e-10):
    if not (any(f < 0 for f in flows) and any(f > 0 for f in flows)):
        return None
    flo, fhi = npv_value(lo, flows), npv_value(hi, flows)
    if flo * fhi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = npv_value(mid, flows)
        if abs(fm) < tol or hi - lo < tol:
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def npv(rate, flows_text):
    try:
        flows = [float(x) for x in flows_text.split(",") if x.strip()]
    except ValueError:
        raise BadInput("--flows must be comma-separated numbers")
    if len(flows) < 2 or not all(math.isfinite(x) for x in flows):
        raise BadInput("--flows needs at least two finite numbers")
    if not math.isfinite(rate) or rate <= -1:
        raise BadInput("--rate must be greater than -1 (e.g. 0.1 for 10%)")
    r = irr(flows)
    changes = sum(1 for a, b in zip(flows, flows[1:]) if a * b < 0)
    return {"command": "npv", "rate": rate, "flows": flows, "npv": round(npv_value(rate, flows), 4),
            "irr": None if r is None else round(r, 6),
            "irr_note": ("no sign change in flows, IRR undefined" if r is None else
                         ("flows change sign %d times: IRR may not be unique" % changes if changes > 1 else "unique")),
            "decision": "accept" if npv_value(rate, flows) > 0 else "reject"}


def flip(model, var, lo=None, hi=None):
    if var not in model["inputs"]:
        raise BadInput("--var %s is not an input of the model" % var)
    s = model["inputs"][var]
    if lo is None or hi is None:
        if s["dist"] in ("triangular", "uniform"):
            dlo, dhi = s["low"], s["high"]
        elif s["dist"] == "normal":
            dlo, dhi = s["mean"] - 4 * s["sd"], s["mean"] + 4 * s["sd"]
        else:
            v = s["value"]
            dlo, dhi = (v - 10 * abs(v) - 1, v + 10 * abs(v) + 1)
        lo = dlo if lo is None else lo
        hi = dhi if hi is None else hi
    if not lo < hi:
        raise BadInput("--lo must be below --hi")
    env = base_env(model)
    tgt = model["target"]

    def f(x):
        e = dict(env); e[var] = x
        return eval_expr(model["expr"], e) - tgt
    base = f(env[var]) + tgt
    flo, fhi = f(lo), f(hi)
    res = {"command": "flip", "var": var, "range": [lo, hi], "target": tgt, "base_value": env[var],
           "base_profit": round(base, 4), "base_decision": "go" if base >= tgt else "no-go",
           "profit_at_lo": round(flo + tgt, 4), "profit_at_hi": round(fhi + tgt, 4)}
    if flo == 0 or fhi == 0:
        res.update(threshold=lo if flo == 0 else hi, flips=True)
    elif flo * fhi > 0:
        res.update(threshold=None, flips=False,
                   note="profit stays on one side of the target across the range; the decision does not flip on %s" % var)
        return res
    else:
        a, b, fa = lo, hi, flo
        for _ in range(200):
            m = (a + b) / 2
            fm = f(m)
            if fm == 0 or (b - a) < 1e-12 * max(1, abs(m)):
                break
            if fa * fm < 0:
                b = m
            else:
                a, fa = m, fm
        res.update(threshold=round((a + b) / 2, 6), flips=True)
    t = res["threshold"]
    res["go_side"] = "above" if fhi >= 0 else "below"
    res["headroom"] = round(env[var] - t, 6)
    res["headroom_pct"] = round((env[var] - t) / abs(t) * 100, 3) if t else None
    return res


def text_summary(r):
    c = r["command"]
    if c == "montecarlo":
        return ("P10 %.2f | P50 %.2f | P90 %.2f | P(profit < %g) = %.1f%% over %d runs (seed %s)"
                % (r["p10"], r["p50"], r["p90"], r["target"], r["prob_below_target"] * 100, r["valid_runs"], r["seed"]))
    if c == "breakeven":
        return "break-even: %d units (%.4f exact), revenue %.2f" % (r["units"], r["units_exact"], r["revenue"])
    if c == "ice":
        return "\n".join("%d. %s  ICE=%g" % (x["rank"], x["name"], x["ice"]) for x in r["items"])
    if c == "npv":
        return "NPV %.4f at %g | IRR %s" % (r["npv"], r["rate"], r["irr"])
    if c == "flip":
        if not r["flips"]:
            return r["note"]
        return "%s flips the decision at %g (base %g, %s side is go)" % (r["var"], r["threshold"], r["base_value"], r["go_side"])
    return json.dumps(r)


def self_test():
    m = parse_model({"inputs": {"p": 10, "u": {"dist": "uniform", "low": 0, "high": 200}, "c": 6, "f": 400},
                     "profit": "(p - c) * u - f"})
    mc = montecarlo(m, runs=20000, seed=3)
    assert abs(mc["prob_below_target"] - 0.5) < 0.02, mc  # loss when u < 100, u ~ U(0,200)
    assert mc == montecarlo(m, runs=20000, seed=3)
    assert breakeven(25, 10000, 15)["units"] == 1000
    assert abs(npv(0.1, "-100,110")["irr"] - 0.1) < 1e-6
    fl = flip(m, "u")
    assert abs(fl["threshold"] - 100) < 1e-6 and fl["go_side"] == "above"
    return {"self_test": "ok", "checks": 5}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--self-test", action="store_true", help="run a small offline check and exit 0")
    p.add_argument("--text", action="store_true", help="short human summary instead of JSON")
    sub = p.add_subparsers(dest="cmd")
    a = sub.add_parser("montecarlo"); a.add_argument("model"); a.add_argument("--runs", type=int, default=10000)
    a.add_argument("--seed", type=int, default=1)
    a = sub.add_parser("breakeven"); a.add_argument("--price", type=float, required=True)
    a.add_argument("--fixed", type=float, required=True); a.add_argument("--variable", type=float, required=True)
    a = sub.add_parser("ice"); a.add_argument("backlog")
    a = sub.add_parser("npv"); a.add_argument("--rate", type=float, required=True); a.add_argument("--flows", required=True)
    a = sub.add_parser("flip"); a.add_argument("model"); a.add_argument("--var", required=True)
    a.add_argument("--lo", type=float); a.add_argument("--hi", type=float)
    for s in sub.choices.values():
        s.add_argument("--text", action="store_true", default=argparse.SUPPRESS)
    raw, argv, i = list(sys.argv[1:] if argv is None else argv), [], 0
    while i < len(raw):  # allow "--flows -1000,300" (a leading minus number is a value, not an option)
        nxt = raw[i + 1] if i + 1 < len(raw) else ""
        if raw[i] in ("--flows", "--rate", "--lo", "--hi") and nxt[:1] == "-" and (nxt[1:2].isdigit() or nxt[1:2] == "."):
            argv.append("%s=%s" % (raw[i], nxt)); i += 2
        else:
            argv.append(raw[i]); i += 1
    args = p.parse_args(argv)
    try:
        if args.self_test:
            r = self_test()
        elif args.cmd == "montecarlo":
            r = montecarlo(load_model(args.model), args.runs, args.seed)
        elif args.cmd == "breakeven":
            r = breakeven(args.price, args.fixed, args.variable)
        elif args.cmd == "ice":
            r = ice(args.backlog)
        elif args.cmd == "npv":
            r = npv(args.rate, args.flows)
        elif args.cmd == "flip":
            r = flip(load_model(args.model), args.var, args.lo, args.hi)
        else:
            p.print_help(sys.stderr)
            return 2
    except BadInput as e:
        print("decision_math: %s" % e, file=sys.stderr)
        return 2
    except AssertionError as e:
        print("decision_math: self-test failed: %s" % e, file=sys.stderr)
        return 1
    if getattr(args, "text", False) and not args.self_test:
        print(text_summary(r))
    else:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
