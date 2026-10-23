#!/usr/bin/env python3
"""KOSIF stats lab — A/B tests, sample sizes, column statistics and cost-basis lots (Python stdlib only).

مختبر إحصاء: اختبار A/B وحجم العينة ووصف عمود وحساب أرباح الدفعات — Deterministic statistics for decisions.

Commands (JSON on stdout; --text for a short human summary; a CSV path may be "-" for stdin)
  abtest --a N,CONV --b N,CONV [--alpha 0.05]
        two-proportion z-test (pooled SE), two-sided p-value, 95% (1-alpha) CI of the absolute difference
        (unpooled Wald) and of the relative lift (log risk-ratio method).
        e.g. python3 scripts/stats_lab.py abtest --a 1000,100 --b 1000,130
  samplesize --base 0.10 --mde 0.20 [--absolute] [--alpha 0.05] [--power 0.8]
        visitors per arm for a two-sided two-proportion test; --mde is relative to --base unless --absolute.
        e.g. python3 scripts/stats_lab.py samplesize --base 0.10 --mde 0.20
  describe data.csv --col NAME
        n, skipped (non-numeric) cells, mean, median, sample sd, min/max, quartiles (linear interpolation,
        'inclusive' method), IQR and the outliers outside Q1-1.5*IQR .. Q3+1.5*IQR with their row numbers.
        e.g. python3 scripts/stats_lab.py describe sales.csv --col revenue
  lots trades.csv --method fifo|lifo|hifo
        realized gains per sell from a CSV with columns date,side(buy|sell),qty,price[,fee][,asset];
        buy fees raise the cost basis, sell fees reduce proceeds; exact decimal arithmetic; open lots left.
        e.g. python3 scripts/stats_lab.py lots trades.csv --method fifo
  --self-test   runs a small offline known-answer check and exits 0.

Never uses the network and never writes files. Bad input: exit 2 with one line on stderr.
Not tax or financial advice: lots reports arithmetic, not a jurisdiction's tax rules (wash sales, holding periods).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

ND = statistics.NormalDist()
_THOUSANDS = re.compile(r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?")


class Bad(ValueError):
    pass


def _pair(text: str, name: str):
    try:
        n, c = (int(x) for x in text.split(","))
    except Exception:
        raise Bad(f"--{name} must be N,CONVERSIONS (two integers), got {text!r}")
    if n <= 0 or c < 0 or c > n:
        raise Bad(f"--{name}: need N > 0 and 0 <= CONVERSIONS <= N, got {text!r}")
    return n, c


def _r(x, k=6):
    return None if x is None else round(x, k)


def abtest(a, b, alpha=0.05):
    if not 0 < alpha < 1:
        raise Bad("--alpha must be between 0 and 1")
    (na, ca), (nb, cb) = a, b
    pa, pb = ca / na, cb / nb
    pool = (ca + cb) / (na + nb)
    se0 = math.sqrt(pool * (1 - pool) * (1 / na + 1 / nb))
    diff = pb - pa
    if se0 == 0:
        z, p = 0.0, 1.0
    else:
        z = diff / se0
        p = math.erfc(abs(z) / math.sqrt(2))
    zc = ND.inv_cdf(1 - alpha / 2)
    se1 = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
    ci_diff = [diff - zc * se1, diff + zc * se1]
    lift = (pb - pa) / pa if pa > 0 else None
    ci_lift = None
    if ca > 0 and cb > 0:
        lse = math.sqrt((1 - pa) / ca + (1 - pb) / cb)  # = sqrt((1-pa)/(na*pa) + (1-pb)/(nb*pb))
        lr = math.log(pb / pa)
        ci_lift = [math.exp(lr - zc * lse) - 1, math.exp(lr + zc * lse) - 1]
    return {
        "a": {"n": na, "conversions": ca, "rate": _r(pa)},
        "b": {"n": nb, "conversions": cb, "rate": _r(pb)},
        "difference": _r(diff), "z": _r(z, 4), "p_value": _r(p, 6), "alpha": alpha,
        "confidence": round(1 - alpha, 4),
        "ci_difference": [_r(x) for x in ci_diff],
        "lift": _r(lift), "ci_lift": None if ci_lift is None else [_r(x) for x in ci_lift],
        "significant": p < alpha,
        "verdict": ("B_BETTER" if diff > 0 else "A_BETTER") if p < alpha else "NO_SIGNIFICANT_DIFFERENCE",
        "method": "pooled two-proportion z-test; Wald CI for the difference; log risk-ratio CI for the lift",
    }


def samplesize(base, mde, absolute=False, alpha=0.05, power=0.8):
    if not 0 < base < 1:
        raise Bad("--base must be a rate between 0 and 1")
    if not 0 < alpha < 1 or not 0 < power < 1:
        raise Bad("--alpha and --power must be between 0 and 1")
    p2 = base + mde if absolute else base * (1 + mde)
    if mde == 0 or not 0 < p2 < 1:
        raise Bad("--mde must be non-zero and keep the target rate between 0 and 1")
    za, zb = ND.inv_cdf(1 - alpha / 2), ND.inv_cdf(power)
    pbar = (base + p2) / 2
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(base * (1 - base) + p2 * (1 - p2))) ** 2
    n = math.ceil(num / (p2 - base) ** 2 - 1e-9)
    return {"base": base, "target": _r(p2), "mde_absolute": _r(p2 - base), "mde_relative": _r((p2 - base) / base),
            "alpha": alpha, "power": power, "z_alpha_2": _r(za, 6), "z_beta": _r(zb, 6),
            "n_per_arm": n, "n_total": 2 * n,
            "method": "two-sided two-proportion test, normal approximation (Fleiss without continuity correction)"}


def _read_csv(path):
    if path == "-":
        import io
        rows = list(csv.DictReader(io.StringIO(sys.stdin.read().lstrip("\ufeff"))))
    else:
        p = Path(path)
        if not p.is_file():
            raise Bad(f"file not found: {path}")
        with p.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    if not rows:
        raise Bad(f"{path} has no data rows")
    return rows


def describe(path, col):
    rows = _read_csv(path)
    if col not in rows[0]:
        raise Bad(f"column {col!r} not in {list(rows[0])}")
    vals, idx, skipped = [], [], 0
    for i, r in enumerate(rows, start=2):  # row 1 is the header
        s = (r.get(col) or "").strip()
        if _THOUSANDS.fullmatch(s):
            s = s.replace(",", "")
        try:
            v = float(s)
            if math.isnan(v) or math.isinf(v):
                raise ValueError
            vals.append(v); idx.append(i)
        except ValueError:
            skipped += 1
    if not vals:
        raise Bad(f"column {col!r} has no numeric values")
    n = len(vals)
    if n >= 2:
        q1, q2, q3 = statistics.quantiles(vals, n=4, method="inclusive")
    else:
        q1 = q2 = q3 = vals[0]
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    out = [{"row": i, "value": v} for i, v in zip(idx, vals) if v < lo or v > hi]
    return {"file": str(path), "column": col, "n": n, "skipped_non_numeric": skipped,
            "mean": _r(statistics.fmean(vals)), "median": _r(statistics.median(vals)),
            "sd": _r(statistics.stdev(vals)) if n >= 2 else None,
            "min": min(vals), "max": max(vals), "q1": _r(q1), "q3": _r(q3), "iqr": _r(iqr),
            "fences": [_r(lo), _r(hi)], "outliers": out,
            "method": "sample sd (n-1); quartiles by linear interpolation (statistics.quantiles method='inclusive'); 1.5*IQR fences"}


def _dec(s, what, row):
    try:
        d = Decimal(str(s).strip().replace(",", "")) if str(s).strip() else Decimal(0)
    except InvalidOperation:
        raise Bad(f"row {row}: {what} is not a number: {s!r}")
    if not d.is_finite() or d < 0:
        raise Bad(f"row {row}: {what} must be a non-negative number")
    return d


def _fmt(d: Decimal):
    q = d.quantize(Decimal("0.00000001")).normalize()
    return format(q, "f") if q != 0 else "0"


def lots(path, method="fifo"):
    if method not in ("fifo", "lifo", "hifo"):
        raise Bad("--method must be fifo, lifo or hifo")
    rows = _read_csv(path)
    need = {"date", "side", "qty", "price"}
    cols = {k.strip().lower() for k in rows[0]}
    if not need <= cols:
        raise Bad(f"{path} needs columns {sorted(need)} (optional fee, asset), got {sorted(cols)}")
    recs = []
    for i, r in enumerate(rows, start=2):
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        side = r["side"].lower()
        if side not in ("buy", "sell"):
            raise Bad(f"row {i}: side must be buy or sell, got {r['side']!r}")
        qty = _dec(r["qty"], "qty", i)
        if qty == 0:
            raise Bad(f"row {i}: qty must be > 0")
        recs.append({"row": i, "date": r["date"], "side": side, "qty": qty, "price": _dec(r["price"], "price", i),
                     "fee": _dec(r.get("fee", ""), "fee", i), "asset": r.get("asset") or "-"})
    recs.sort(key=lambda x: (x["date"], x["row"]))  # stable: same date keeps file order
    book, sells, totals = {}, [], {}
    for t in recs:
        q = book.setdefault(t["asset"], [])
        if t["side"] == "buy":
            q.append({"row": t["row"], "date": t["date"], "qty": t["qty"],
                      "unit_cost": (t["qty"] * t["price"] + t["fee"]) / t["qty"]})
            continue
        held = sum(l["qty"] for l in q)
        if t["qty"] > held:
            raise Bad(f"row {t['row']}: sells {_fmt(t['qty'])} {t['asset']} but only {_fmt(held)} held")
        left, basis, used = t["qty"], Decimal(0), []
        while left > 0:
            if method == "fifo":
                k = 0
            elif method == "lifo":
                k = len(q) - 1
            else:  # highest cost first; ties -> earliest lot
                k = max(range(len(q)), key=lambda j: (q[j]["unit_cost"], -j))
            lot = q[k]
            take = min(left, lot["qty"])
            basis += take * lot["unit_cost"]
            used.append({"lot_row": lot["row"], "lot_date": lot["date"], "qty": _fmt(take), "unit_cost": _fmt(lot["unit_cost"])})
            lot["qty"] -= take
            left -= take
            if lot["qty"] == 0:
                q.pop(k)
        proceeds = t["qty"] * t["price"] - t["fee"]
        gain = proceeds - basis
        totals[t["asset"]] = totals.get(t["asset"], Decimal(0)) + gain
        sells.append({"row": t["row"], "date": t["date"], "asset": t["asset"], "qty": _fmt(t["qty"]),
                      "proceeds": _fmt(proceeds), "cost_basis": _fmt(basis), "gain": _fmt(gain), "lots_used": used})
    open_lots = [{"asset": a, "lot_row": l["row"], "date": l["date"], "qty": _fmt(l["qty"]), "unit_cost": _fmt(l["unit_cost"])}
                 for a in sorted(book) for l in book[a]]
    return {"file": str(path), "method": method, "sells": sells,
            "realized_by_asset": {a: _fmt(v) for a, v in sorted(totals.items())},
            "realized_total": _fmt(sum(totals.values(), Decimal(0))), "open_lots": open_lots,
            "note": "Arithmetic only, not tax advice (no wash-sale or holding-period rules)."}


def _text(cmd, r):
    if cmd == "abtest":
        return (f"A {r['a']['rate']:.4f} vs B {r['b']['rate']:.4f}  z={r['z']}  p={r['p_value']}  lift={r['lift']}  "
                f"CI(lift)={r['ci_lift']}  -> {r['verdict']}")
    if cmd == "samplesize":
        return f"{r['base']} -> {r['target']}: n per arm = {r['n_per_arm']} (total {r['n_total']})"
    if cmd == "describe":
        return (f"{r['column']}: n={r['n']} mean={r['mean']} median={r['median']} sd={r['sd']} "
                f"Q1={r['q1']} Q3={r['q3']} outliers={len(r['outliers'])}")
    return f"{r['method']}: realized total {r['realized_total']} over {len(r['sells'])} sells; open lots {len(r['open_lots'])}"


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        print(f"STATS_LAB_ERROR: {message}", file=sys.stderr)
        raise SystemExit(2)


def self_test() -> int:
    import tempfile
    r = abtest((1000, 100), (1000, 130))
    assert abs(r["z"] - 2.1027) < 1e-3 and abs(r["p_value"] - 0.035488) < 1e-5, r
    assert samplesize(0.10, 0.20)["n_per_arm"] == 3841
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "t.csv"
        p.write_text("date,side,qty,price\n2024-01-01,buy,10,100\n2024-02-01,buy,10,200\n2024-03-01,sell,15,300\n", encoding="utf-8")
        assert lots(p, "fifo")["realized_total"] == "2500" and lots(p, "lifo")["realized_total"] == "2000"
        p.write_text("x\n1\n2\n3\n4\n100\n", encoding="utf-8")
        assert describe(p, "x")["outliers"] == [{"row": 6, "value": 100.0}]
    print("self-test: OK")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = _Parser(prog="stats_lab.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true", help="run the offline known-answer check")
    sub = ap.add_subparsers(dest="cmd", required=True, parser_class=_Parser)
    s = sub.add_parser("abtest"); s.add_argument("--a", required=True); s.add_argument("--b", required=True)
    s.add_argument("--alpha", type=float, default=0.05)
    s = sub.add_parser("samplesize"); s.add_argument("--base", type=float, required=True); s.add_argument("--mde", type=float, required=True)
    s.add_argument("--absolute", action="store_true"); s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    s = sub.add_parser("describe"); s.add_argument("file"); s.add_argument("--col", required=True)
    s = sub.add_parser("lots"); s.add_argument("file"); s.add_argument("--method", default="fifo", choices=["fifo", "lifo", "hifo"])
    for p in sub.choices.values():
        p.add_argument("--text", action="store_true", help="one-line human summary instead of JSON")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "abtest":
            r = abtest(_pair(a.a, "a"), _pair(a.b, "b"), a.alpha)
        elif a.cmd == "samplesize":
            r = samplesize(a.base, a.mde, a.absolute, a.alpha, a.power)
        elif a.cmd == "describe":
            r = describe(a.file, a.col)
        else:
            r = lots(a.file, a.method)
    except (Bad, OSError, csv.Error, UnicodeDecodeError, statistics.StatisticsError) as e:
        print(f"STATS_LAB_ERROR: {e}".replace("\n", " "), file=sys.stderr)
        return 2
    print(_text(a.cmd, r) if a.text else json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
