"""Real programs for the atlas-data family (data pipelines, statistics, experiments, databases).

Every function builds a small deterministic fixture, performs the card's technique on it and
returns known-answer checks. Offline, stdlib + numpy + scipy + bs4 only.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import re
import sqlite3
from pathlib import Path

import numpy as np
from scipy import stats


def _w(work: Path, name: str, obj) -> Path:
    p = work / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, (bytes, bytearray)):
        p.write_bytes(obj)
    elif isinstance(obj, str):
        p.write_text(obj, encoding="utf-8")
    else:
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return p


def _c(name, cond, obs):
    return (name, bool(cond), str(obs))


# ---------------------------------------------------------------- ADATA-01
def adata_01(work: Path):
    """Overwrite-by-partition writes, bounded exponential backoff with jitter, capped backfill."""
    store = work / "partitions"
    store.mkdir()

    def write_partition(day, rows):  # idempotent: the partition file is replaced, never appended
        (store / f"{day}.json").write_text(json.dumps(rows))

    def run(days):
        for d in days:
            write_partition(d, [{"day": d, "i": i} for i in range(3)])

    days = [f"2026-01-{i:02d}" for i in range(1, 11)]
    run(days)
    run(days)  # re-run must not duplicate
    total = sum(len(json.loads(p.read_text())) for p in store.glob("*.json"))
    naive = []
    for _ in range(2):
        for d in days:
            naive += [{"day": d, "i": i} for i in range(3)]

    rng = random.Random(7)

    def with_retries(fn, limit=4, base=0.5):
        delays, attempt = [], 0
        while True:
            attempt += 1
            try:
                return fn(attempt), attempt, delays
            except RuntimeError:
                if attempt >= limit:
                    raise RuntimeError(f"gave up after {attempt}") from None
                cap = base * 2 ** (attempt - 1)
                delays.append(round(cap / 2 + rng.uniform(0, cap / 2), 4))  # equal jitter

    def flaky(a):
        if a < 3:
            raise RuntimeError("transient")
        return "ok"

    res, attempts, delays = with_retries(flaky)
    try:
        with_retries(lambda a: (_ for _ in ()).throw(RuntimeError("down")))
        gave_up = None
    except RuntimeError as e:
        gave_up = str(e)
    cap, running, peak = 3, 0, 0
    for i in range(0, len(days), cap):  # backfill waves under the concurrency cap
        running = len(days[i:i + cap])
        peak = max(peak, running)
    _w(work, "run.json", {"rows": total, "attempts": attempts, "delays": delays, "peak": peak})
    return [_c("re-run keeps 30 rows (10 partitions x 3)", total == 30, total),
            _c("append mode would duplicate to 60", len(naive) == 60, len(naive)),
            _c("flaky step succeeds on attempt 3", res == "ok" and attempts == 3, attempts),
            _c("backoff delays lie in [cap/2, cap] and grow", 0.25 <= delays[0] <= 0.5 and 0.5 <= delays[1] <= 1.0, delays),
            _c("permanent failure stops at retry limit 4", gave_up == "gave up after 4", gave_up),
            _c("backfill never exceeds concurrency cap 3", peak == 3, peak)]


# ---------------------------------------------------------------- ADATA-02
def adata_02(work: Path):
    sessions = {
        "s1": [{"tool": "Bash", "input": "cat src/a.py", "ok": True, "bytes": 200},
               {"tool": "Read", "input": "src/b.py", "ok": True, "bytes": 300}],
        "s2": [{"tool": "Grep", "input": "foo", "ok": False, "bytes": 0},
               {"tool": "Grep", "input": "foo", "ok": False, "bytes": 0},
               {"tool": "Grep", "input": "foo", "ok": False, "bytes": 0}],
        "s3": [{"tool": "Read", "input": "big.log", "ok": True, "bytes": 900_000}],
        "s4": [{"tool": "Read", "input": "x.py", "ok": True, "bytes": 100},
               {"tool": "Edit", "input": "x.py", "ok": True, "bytes": 50}],
    }
    tdir = work / "transcripts"
    tdir.mkdir()
    for sid, ev in sessions.items():
        (tdir / f"{sid}.jsonl").write_text("\n".join(json.dumps(e) for e in ev))
    db = sqlite3.connect(work / "index.sqlite")
    db.execute("create table ev(session, seq, tool, input, ok, bytes)")
    for f in sorted(tdir.glob("*.jsonl")):
        for i, line in enumerate(f.read_text().splitlines()):
            e = json.loads(line)
            db.execute("insert into ev values(?,?,?,?,?,?)", (f.stem, i, e["tool"], e["input"], e["ok"], e["bytes"]))
    find = set()
    for (s,) in db.execute("select distinct session from ev where ok=0"):
        find.add((s, "tool_error"))
    for s, n in db.execute("select session,count(*) from ev group by session,tool,input having count(*)>=3"):
        find.add((s, "retry_loop"))
    for (s,) in db.execute("select session from ev where tool='Bash' and (input like 'cat %' or input like 'grep %')"):
        find.add((s, "shell_instead_of_tool"))
    for (s,) in db.execute("select session from ev where bytes>100000"):
        find.add((s, "oversized_result"))
    _w(work, "findings.json", sorted(find))
    expected = {("s1", "shell_instead_of_tool"), ("s2", "tool_error"), ("s2", "retry_loop"), ("s3", "oversized_result")}
    return [_c("exactly the four planted anti-patterns are found", find == expected, sorted(find)),
            _c("clean session s4 has no finding", not any(s == "s4" for s, _ in find), "s4"),
            _c("index holds all 8 events", db.execute("select count(*) from ev").fetchone()[0] == 8, 8)]


# ---------------------------------------------------------------- ADATA-03
def adata_03(work: Path):
    def name_ok(n):
        return bool(re.fullmatch(r"[a-z][a-z0-9]*(_[a-z0-9]+)*", n)) and not re.search(r"_v\d+$", n)

    endpoints = [{"name": "weekly_signups", "last_called_days": 2, "rows": 1e3, "cohort": False},
                 {"name": "Weekly-Signups", "last_called_days": 1, "rows": 1e3, "cohort": False},
                 {"name": "revenue_v2", "last_called_days": 5, "rows": 5e6, "cohort": False},
                 {"name": "old_report", "last_called_days": 120, "rows": 2e6, "cohort": True}]
    out = []
    for e in endpoints:
        out.append({**e, "name_ok": name_ok(e["name"]),
                    "materialise": e["rows"] > 1e6 and not e["cohort"],
                    "freshness_s": 3600 if e["rows"] > 1e6 else 300,
                    "stale": e["last_called_days"] > 90})
    _w(work, "endpoints.json", out)
    by = {e["name"]: e for e in out}
    return [_c("snake_case accepted, kebab/Capital rejected", by["weekly_signups"]["name_ok"] and not by["Weekly-Signups"]["name_ok"], ""),
            _c("version suffix rejected", not by["revenue_v2"]["name_ok"], "revenue_v2"),
            _c("heavy query without cohort is materialised, cohort one is not",
               by["revenue_v2"]["materialise"] and not by["old_report"]["materialise"], ""),
            _c("stale audit flags only old_report", [e["name"] for e in out if e["stale"]] == ["old_report"], "")]


# ---------------------------------------------------------------- ADATA-04
def adata_04(work: Path):
    req = ["source", "occurred_at", "status", "responsible", "external_link"]
    crm = [dict(zip(req, r)) for r in [("ads", "2026-01-01", "won", "ali", "L1"), ("seo", "2026-01-02", "open", "mona", "L2"),
                                       ("ads", "2026-01-03", "lost", "ali", "L3")]]
    ana = [dict(zip(req, r)) for r in [("ads", "2026-01-01", "won", "ali", "L1"), ("seo", "2026-01-02", "won", "mona", "L2"),
                                       ("ref", "2026-01-05", "open", "sara", "L9")]]
    for r in crm + ana:
        assert all(k in r for k in req)
    a = {r["external_link"]: r for r in crm}
    b = {r["external_link"]: r for r in ana}
    match, mismatch, only2 = [], {}, []
    for k, rb in b.items():
        if k not in a:
            only2.append(k)
            continue
        diff = {f: (a[k][f], rb[f]) for f in req if a[k][f] != rb[f]}
        (mismatch.__setitem__(k, diff) if diff else match.append(k))
    _w(work, "reconcile.json", {"match": match, "mismatch": mismatch, "only_in_second": only2, "writes": 0})
    return [_c("L1 matches", match == ["L1"], match),
            _c("L2 mismatches on status only", mismatch == {"L2": {"status": ("open", "won")}}, mismatch),
            _c("L9 is only in the second export", only2 == ["L9"], only2),
            _c("inputs left unchanged (read-only)", len(crm) == 3 and crm[1]["status"] == "open", crm[1])]


# ---------------------------------------------------------------- ADATA-05
def adata_05(work: Path):
    fee = 0.001
    rates = {("USD", "BTC"): 1 / 50000, ("BTC", "ETH"): 20.0, ("ETH", "USD"): 2600.0}
    amt = 1000.0
    for leg in [("USD", "BTC"), ("BTC", "ETH"), ("ETH", "USD")]:
        amt = amt * rates[leg] * (1 - fee)
    gross = 1000 * (1 / 50000) * 20 * 2600
    gas = np.arange(1, 101, dtype=float)
    pct = {p: float(np.percentile(gas, p)) for p in (10, 50, 75, 90)}

    def il(r):
        return 2 * math.sqrt(r) / (1 + r) - 1

    _w(work, "crypto.json", {"triangular_out": amt, "gas_pct": pct, "il_4x": il(4)})
    return [_c("triangular gross 1040 before fees", abs(gross - 1040) < 1e-9, gross),
            _c("three 0.1% fees: 1040*0.999^3", abs(amt - 1040 * 0.999 ** 3) < 1e-9, round(amt, 4)),
            _c("gas percentiles 10/50/75/90 of 1..100", np.allclose([pct[k] for k in (10, 50, 75, 90)], [10.9, 50.5, 75.25, 90.1]), pct),
            _c("impermanent loss at 4x price = -20%", abs(il(4) + 0.2) < 1e-12, il(4)),
            _c("no loss when price unchanged", il(1) == 0, il(1))]


# ---------------------------------------------------------------- ADATA-06
def adata_06(work: Path):
    buys = [("2025-01-05", 1, 100.0), ("2025-03-01", 1, 300.0), ("2025-06-01", 1, 200.0)]
    sells = [("2025-09-01", 1, 400.0), ("2024-12-01", 0, 0)]
    staking = [("2025-04-01", "ETH", 50.0), ("2024-04-01", "ETH", 70.0)]

    def gains(method, year=2025):
        lots = [list(b) for b in buys]
        total = 0.0
        for d, q, px in sells:
            if not d.startswith(str(year)) or q == 0:
                continue
            order = {"FIFO": lots, "LIFO": lots[::-1], "HIFO": sorted(lots, key=lambda l: -l[2])}[method]
            lot = order[0]
            total += q * (px - lot[2])
            lots.remove(lot)
        return total

    res = {m: gains(m) for m in ("FIFO", "LIFO", "HIFO")}
    income = sum(v for d, _, v in staking if d.startswith("2025"))
    buf = io.StringIO()
    wr = csv.writer(buf)
    wr.writerow(["method", "gain"])
    for m, g in res.items():
        wr.writerow([m, g])
    _w(work, "gains.csv", buf.getvalue())
    return [_c("FIFO uses the 100 lot: gain 300", res["FIFO"] == 300, res),
            _c("LIFO uses the 200 lot: gain 200", res["LIFO"] == 200, res),
            _c("HIFO uses the 300 lot: gain 100 (lowest)", res["HIFO"] == 100 and res["HIFO"] == min(res.values()), res),
            _c("--year filter keeps only 2025 staking income 50", income == 50, income)]


# ---------------------------------------------------------------- ADATA-07
def adata_07(work: Path):
    items = [{"id": i, "bg": "blue", "hat": "cap" if i % 2 else "none"} for i in range(9)]
    items.append({"id": 9, "bg": "gold", "hat": "crown"})
    freq = {}
    for it in items:
        for k in ("bg", "hat"):
            freq[(k, it[k])] = freq.get((k, it[k]), 0) + 1
    n = len(items)
    score = {it["id"]: sum(n / freq[(k, it[k])] for k in ("bg", "hat")) for it in items}
    ranked = sorted(score, key=lambda i: -score[i])
    txs = [("a", "b", 5), ("w", "x", 5000), ("c", "d", 20), ("w", "y", 12000)]
    whales = [t for t in txs if t[2] >= 1000]
    holdings = {"ETH": (2, 3000), "BTC": (0.1, 60000), "USDC": (1000, 1)}
    val = {k: q * p for k, (q, p) in holdings.items()}
    alloc = {k: v / sum(val.values()) for k, v in val.items()}
    _w(work, "rarity.json", {"score": score, "ranked": ranked, "alloc": alloc})
    return [_c("planted unique gold/crown item ranks rarest", ranked[0] == 9, ranked[:3]),
            _c("its score = 10/1 + 10/1 = 20", score[9] == 20, score[9]),
            _c("two whale transfers >= 1000 found", len(whales) == 2, whales),
            _c("portfolio value 13000 and allocation sums to 1", sum(val.values()) == 13000 and abs(sum(alloc.values()) - 1) < 1e-12, val)]


# ---------------------------------------------------------------- ADATA-08
def _iban_ok(iban):
    s = iban.replace(" ", "").upper()
    s = s[4:] + s[:4]
    return int("".join(str(int(ch, 36)) for ch in s)) % 97 == 1


def adata_08(work: Path):
    docs = [{"vendor": "Acme", "invoice_no": "INV-7", "date": "2026-08-14", "total": 1500.0, "iban": "GB82 WEST 1234 5698 7654 32"},
            {"vendor": "Beta", "invoice_no": "INV-9", "date": "2026-02-03", "total": 300.0, "iban": "GB82 WEST 1234 5698 7654 33"}]
    fiscal_start = 7
    out = []
    for d in docs:
        y, m = int(d["date"][:4]), int(d["date"][5:7])
        fy = y + 1 if m >= fiscal_start else y
        q = ((m - fiscal_start) % 12) // 3 + 1
        out.append({**d, "iban_ok": _iban_ok(d["iban"]),
                    "name": f"{d['date']}_{d['vendor']}_{d['invoice_no']}.pdf",
                    "path": f"FY{fy}/Q{q}", "dry_run": True})
    big = [o["invoice_no"] for o in out if o["total"] > 1000]
    _w(work, "intake.json", out)
    return [_c("valid IBAN GB82WEST... passes mod-97", out[0]["iban_ok"], out[0]["iban"]),
            _c("one-digit-off IBAN fails the check digit", not out[1]["iban_ok"], out[1]["iban"]),
            _c("rename template {date}_{vendor}_{ref}", out[0]["name"] == "2026-08-14_Acme_INV-7.pdf", out[0]["name"]),
            _c("Aug with July fiscal start -> FY2027 Q1; Feb -> FY2026 Q3",
               out[0]["path"] == "FY2027/Q1" and out[1]["path"] == "FY2026/Q3", [o["path"] for o in out]),
            _c("query total>1000 returns INV-7", big == ["INV-7"], big)]


# ---------------------------------------------------------------- ADATA-09
def adata_09(work: Path):
    scen = {"A": {"budget": 100.0, "mu": 1.5, "sd": 0.3}, "B": {"budget": 100.0, "mu": 1.2, "sd": 0.3},
            "C": {"budget": 100.0, "mu": 1.5, "sd": 0.9}}
    sat, target = 0.8, 50.0

    def sim(s, n, seed):
        rng = np.random.default_rng(seed)
        roi = rng.normal(s["mu"], s["sd"], n)
        return s["budget"] ** sat * roi * (s["budget"] ** (1 - sat))  # diminishing returns on budget

    rep = {}
    for k, s in scen.items():
        r = sim(s, 10_000, 1)
        p10, p50, p90 = np.percentile(r, [10, 50, 90])
        rep[k] = {"mean": float(r.mean()), "p10": float(p10), "p50": float(p50), "p90": float(p90),
                  "p_target": float((r >= target + s["budget"]).mean()), "risk_adj": float(r.mean() - r.std())}
    conv = abs(sim(scen["A"], 10_000, 1).mean() - sim(scen["A"], 50_000, 2).mean()) / rep["A"]["mean"]
    rank = sorted(rep, key=lambda k: -rep[k]["risk_adj"])
    _w(work, "montecarlo.json", {"report": rep, "rank_risk_adjusted": rank, "convergence": conv})
    return [_c("A mean ~150 within 3 SE", abs(rep["A"]["mean"] - 150) < 3 * 30 / 100, rep["A"]["mean"]),
            _c("P10 < P50 < P90", rep["A"]["p10"] < rep["A"]["p50"] < rep["A"]["p90"], rep["A"]),
            _c("risk-adjusted ranks low-variance A over wide C", rank.index("A") < rank.index("C"), rank),
            _c("10k vs 50k means converge within 1%", conv < 0.01, conv)]


# ---------------------------------------------------------------- ADATA-10
def adata_10(work: Path):
    st = {"current_assets": 500, "inventory": 200, "current_liabilities": 250, "total_debt": 400, "equity": 800,
          "revenue": 2000, "cogs": 1200, "net_income": 160, "total_assets": 1200, "shares": 100, "price": 24}
    missing = [k for k, v in {**st, "capex": None}.items() if v is None]
    ratios = {"liquidity": {"current": st["current_assets"] / st["current_liabilities"],
                            "quick": (st["current_assets"] - st["inventory"]) / st["current_liabilities"]},
              "profitability": {"gross_margin": (st["revenue"] - st["cogs"]) / st["revenue"], "roe": st["net_income"] / st["equity"]},
              "leverage": {"debt_equity": st["total_debt"] / st["equity"]},
              "efficiency": {"asset_turnover": st["revenue"] / st["total_assets"]},
              "valuation": {"pe": st["price"] / (st["net_income"] / st["shares"])}}
    bp, bv, ap, av = 10.0, 100, 12.0, 90
    vol = (av - bv) * bp
    price = (ap - bp) * av
    acc = abs(1950 - 2000) / 2000
    _w(work, "ratios.json", {"ratios": ratios, "variance": {"volume": vol, "price": price}, "missing": missing})
    return [_c("current ratio 2.0, quick 1.2", ratios["liquidity"] == {"current": 2.0, "quick": 1.2}, ratios["liquidity"]),
            _c("five ratio categories", len(ratios) == 5, list(ratios)),
            _c("P/E = 24 / 1.6 = 15", abs(ratios["valuation"]["pe"] - 15) < 1e-12, ratios["valuation"]),
            _c("variance drivers add back: volume -100 (unfav) + price +180 (fav) = 80",
               vol == -100 and price == 180 and vol + price == ap * av - bp * bv, (vol, price)),
            _c("null field detected before ratios", missing == ["capex"], missing),
            _c("2.5% revenue forecast error within +/-5% target", acc <= 0.05, acc)]


# ---------------------------------------------------------------- ADATA-11
def adata_11(work: Path):
    quota = 1_000_000
    stage_cycle = {"discovery": 10, "proposal": 15}
    deals = [{"id": "d1", "amt": 1_500_000, "stage": "proposal", "days": 40, "acct": "Big"},
             {"id": "d2", "amt": 800_000, "stage": "discovery", "days": 5, "acct": "Small"},
             {"id": "d3", "amt": 1_200_000, "stage": "discovery", "days": 12, "acct": "Mid"}]
    pipe = sum(d["amt"] for d in deals)
    cov = pipe / quota
    win, cycle = 0.25, 60
    velocity = len(deals) * (pipe / len(deals)) * win / cycle
    stuck = [d["id"] for d in deals if d["days"] > 2 * stage_cycle[d["stage"]]]
    conc = [d["acct"] for d in deals if d["amt"] / pipe > 0.4]
    _w(work, "pipeline.json", {"coverage": cov, "velocity_per_day": velocity, "stuck": stuck, "concentration": conc})
    return [_c("coverage 3.5x is in the healthy 3-4x band", cov == 3.5 and 3 <= cov <= 4, cov),
            _c("velocity = 3 x 1.1667M x 0.25 / 60 = 14583.33/day", abs(velocity - 14583.333) < 0.01, velocity),
            _c("d1 at 40 days > 2 x 15 flagged stuck", stuck == ["d1"], stuck),
            _c("Big account at 42.9% > 40% flagged", conc == ["Big"], conc)]


# ---------------------------------------------------------------- ADATA-12
def adata_12(work: Path):
    today = 100
    invoices = [("i1", 90, 500), ("i2", 50, 300), ("i3", 20, 200), ("i4", 5, 50)]
    buckets = {"0-30": [], "31-60": [], "61-90": [], "90+": []}
    for iid, issued, amt in invoices:
        age = today - issued
        key = "0-30" if age <= 30 else "31-60" if age <= 60 else "61-90" if age <= 90 else "90+"
        buckets[key].append(iid)
    pay = [{"gross": 5000, "tax": 1000, "super": 550, "net": 3450}, {"gross": 4000, "tax": 700, "super": 440, "net": 2860}]
    recon = all(p["gross"] - p["tax"] - p["super"] == p["net"] for p in pay)
    principal, r, n = 100_000.0, 0.0877, 7
    myr = principal * r / (1 - (1 + r) ** -n)
    bal = principal
    for _ in range(n):
        bal = bal * (1 + r) - myr
    _w(work, "books.json", {"aging": buckets, "payroll_reconciled": recon, "div7a_myr": myr, "end_balance": bal,
                            "note": "prep for accountant, not tax advice"})
    return [_c("aging buckets by days outstanding: 10/50/80/95 days", buckets == {"0-30": ["i1"], "31-60": ["i2"], "61-90": ["i3"], "90+": ["i4"]}, buckets),
            _c("i4 issued day 5 is in 90+", "i4" in buckets["90+"], buckets["90+"]),
            _c("payroll gross - tax - super == net", recon, pay),
            _c("Div 7A 7-year schedule amortises to zero", abs(bal) < 1e-6, round(myr, 2))]


# ---------------------------------------------------------------- ADATA-13
def adata_13(work: Path):
    n1, x1, n2, x2 = 1000, 100, 1000, 130
    p1, p2 = x1 / n1, x2 / n2
    pp_ = (x1 + x2) / (n1 + n2)
    z = (p2 - p1) / math.sqrt(pp_ * (1 - pp_) * (1 / n1 + 1 / n2))
    p = 2 * stats.norm.sf(abs(z))
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    ci = (p2 - p1 - 1.96 * se, p2 - p1 + 1.96 * se)
    h = 2 * math.asin(math.sqrt(p2)) - 2 * math.asin(math.sqrt(p1))
    chi2, _, _, _ = stats.chi2_contingency([[x1, n1 - x1], [x2, n2 - x2]], correction=False)
    cramer = math.sqrt(chi2 / (n1 + n2))
    a = np.r_[np.full(50, 10.0), np.full(50, 12.0)]
    b = a + 1
    d = (b.mean() - a.mean()) / math.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    _w(work, "abtest.json", {"z": z, "p": p, "ci": ci, "cohen_h": h, "cramers_v": cramer, "cohen_d": d,
                             "answer": ["Bottom line", "What", "Why", "How to act"]})
    return [_c("chi-square equals z^2 for 2x2", abs(chi2 - z * z) < 1e-9, (round(z, 4), round(chi2, 4))),
            _c("p < 0.05 and 95% CI excludes zero", p < 0.05 and ci[0] > 0, (p, ci)),
            _c("Cramer V = |phi| = |z|/sqrt(N)", abs(cramer - abs(z) / math.sqrt(2000)) < 1e-12, cramer),
            _c("Cohen d of a 1-unit shift with sd 1.005 ~ 0.995", abs(d - 1 / a.std(ddof=1)) < 1e-12, d),
            _c("Cohen h positive and small (<0.2)", 0 < h < 0.2, h)]


# ---------------------------------------------------------------- ADATA-14
def _n_two_prop(p1, mde, alpha=0.05, power=0.8):
    p2 = p1 + mde
    pbar = (p1 + p2) / 2
    za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    return math.ceil((za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / mde ** 2)


def adata_14(work: Path):
    n = _n_two_prop(0.10, 0.02)
    traffic = 1000
    days = math.ceil(2 * n / traffic)

    def power_at(nn, p1=0.10, mde=0.02, alpha=0.05):
        p2 = p1 + mde
        se = math.sqrt(p1 * (1 - p1) / nn + p2 * (1 - p2) / nn)
        return stats.norm.cdf(mde / se - stats.norm.ppf(1 - alpha / 2))

    fixed = power_at(1000)
    _w(work, "plan.json", {"n_per_group": n, "total": 2 * n, "days": days, "power_at_1000": fixed,
                           "warn": fixed < 0.8})
    return [_c("n per group for 10% -> 12% at alpha .05 power .8 is 3841", n == 3841, n),
            _c("total 7682 users -> 8 days at 1000/day", 2 * n == 7682 and days == 8, days),
            _c("power at n=3841 ~ 0.80", abs(power_at(n) - 0.80) < 0.01, power_at(n)),
            _c("fixed n=1000 warns: power < 0.80", fixed < 0.8, round(fixed, 3)),
            _c("halving MDE roughly quadruples n", 3.6 < _n_two_prop(0.10, 0.01) / n < 4.2, _n_two_prop(0.10, 0.01))]


# ---------------------------------------------------------------- ADATA-15
def adata_15(work: Path):
    def t_power(n1, d, alpha=0.05, ratio=1.0):
        n2 = n1 * ratio
        df = n1 + n2 - 2
        nc = d / math.sqrt(1 / n1 + 1 / n2)
        tc = stats.t.ppf(1 - alpha / 2, df)
        return stats.nct.sf(tc, df, nc) + stats.nct.cdf(-tc, df, nc)

    n = next(k for k in range(2, 1000) if t_power(k, 0.5) >= 0.8)
    n_unequal = next(k for k in range(2, 1000) if t_power(k, 0.5, ratio=2) >= 0.8)
    rng = np.random.default_rng(3)
    a = rng.normal(0, 1, (2000, n))
    b = rng.normal(0.5, 1, (2000, n))
    sim = float((stats.ttest_ind(a, b, axis=1).pvalue < 0.05).mean())
    curve = {k: round(t_power(k, 0.5), 3) for k in (20, 40, 64, 100)}
    _w(work, "power.json", {"n_per_group": n, "n1_with_2to1": n_unequal, "sim_power": sim, "curve": curve})
    return [_c("d=0.5, alpha .05, power .8 -> 64 per group", n == 64, n),
            _c("2:1 allocation: total exceeds 128", n_unequal * 3 > 128, n_unequal * 3),
            _c("simulation (2000 draws) power ~0.80 +/- 0.03", abs(sim - 0.8) < 0.03, sim),
            _c("power curve increases with n", list(curve.values()) == sorted(curve.values()), curve)]


# ---------------------------------------------------------------- ADATA-16
def adata_16(work: Path):
    root = work / "data"
    root.mkdir()
    rows = [["id", "email", "age", "city"], ["1", "a@x.com", "30", "Cairo"], ["2", "b@x.com", "", "Giza"],
            ["3", "c@x.com", "45", "Cairo"], ["4", "=cmd|' /C calc'!A0", "200", "Cairo"]]
    f = root / "people.csv"
    with open(f, "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    (root / "evil.pkl").write_bytes(b"\x80\x04")

    def allowed(path, root):
        p = Path(path)
        if str(path).startswith(("http://", "https://")) or p.suffix in (".pkl", ".pickle") or p.is_symlink():
            return False
        return root.resolve() in p.resolve().parents

    profile = {}
    with open(f, newline="") as fh:
        data = list(csv.DictReader(fh))
    for col in data[0]:
        vals = [r[col] for r in data]
        nums = [float(v) for v in vals if re.fullmatch(r"-?\d+(\.\d+)?", v)]
        profile[col] = {"missing": sum(v == "" for v in vals), "cardinality": len(set(vals)),
                        "type": "numeric" if len(nums) == sum(v != "" for v in vals) else "text"}
        if profile[col]["type"] == "numeric":
            profile[col]["range"] = [min(nums), max(nums)]
    out = json.dumps(profile)
    _w(work, "profile.json", profile)
    return [_c("URL, pickle and outside-root paths refused", not allowed("https://x/y.csv", root) and not allowed(root / "evil.pkl", root)
               and not allowed("/etc/passwd", root) and allowed(f, root), ""),
            _c("age: 1 missing, range 30..200", profile["age"]["missing"] == 1 and profile["age"]["range"] == [30, 200], profile["age"]),
            _c("city cardinality 2", profile["city"]["cardinality"] == 2, profile["city"]),
            _c("no raw identifier or injected cell in output", "@x.com" not in out and "calc" not in out, len(out))]


# ---------------------------------------------------------------- ADATA-17
def adata_17(work: Path):
    users = {f"u{i}": ("2026-01" if i < 10 else "2026-02", "ads" if i % 2 else "seo") for i in range(20)}
    active = {(u, "2026-02") for u in list(users)[:5]} | {(u, "2026-03") for u in list(users)[10:18]}
    ret = {}
    for cohort, nxt in (("2026-01", "2026-02"), ("2026-02", "2026-03")):
        members = [u for u, (c, _) in users.items() if c == cohort]
        ret[cohort] = sum((u, nxt) in active for u in members) / len(members)
    funnel = {"visit": 1000, "signup": 400, "activate": 300, "pay": 60}
    st = list(funnel)
    conv = {f"{a}->{b}": funnel[b] / funnel[a] for a, b in zip(st, st[1:])}
    worst = min(conv, key=conv.get)
    spend = {"ads": 500, "seo": 200}
    cac = {ch: spend[ch] / sum(1 for _, c in users.values() if c == ch) for ch in spend}
    rfm = {"r": [1, 30, 200], "f": [12, 3, 1], "m": [900, 200, 20]}
    tiers = ["high" if r < 7 and f >= 10 else "mid" if r < 60 else "low" for r, f in zip(rfm["r"], rfm["f"])]
    _w(work, "cohorts.json", {"retention_m1": ret, "conversion": conv, "biggest_drop": worst, "cac": cac, "rfm": tiers})
    return [_c("Jan cohort month-1 retention 50%, Feb 80%", ret == {"2026-01": 0.5, "2026-02": 0.8}, ret),
            _c("biggest funnel drop is activate->pay (20%)", worst == "activate->pay" and conv[worst] == 0.2, conv),
            _c("CAC by channel not blended: ads 50, seo 20", cac == {"ads": 50.0, "seo": 20.0}, cac),
            _c("RFM tiers high/mid/low", tiers == ["high", "mid", "low"], tiers)]


# ---------------------------------------------------------------- ADATA-18
def adata_18(work: Path):
    rows = [{"id": i, "price": float(10 + i % 5), "const": 1, "mix": i if i % 7 else "x", "cat": ("a" if i % 2 else "b") if i < 30 else None}
            for i in range(40)]
    rows[5]["price"] = 999.0
    rows.append(dict(rows[3]))  # exact duplicate

    def audit(rows):
        cols = list(rows[0])
        issues = []
        for c in cols:
            vals = [r[c] for r in rows]
            nn = [v for v in vals if v is not None]
            nullp = 1 - len(nn) / len(vals)
            if nullp > 0.1:
                issues.append(("nulls", c, round(nullp, 3)))
            if len(set(map(str, nn))) == 1:
                issues.append(("constant", c, nn[0]))
            if len({type(v) for v in nn}) > 1:
                issues.append(("mixed_types", c, sorted(t.__name__ for t in {type(v) for v in nn})))
            nums = np.array([v for v in nn if isinstance(v, float)])
            if len(nums) > 4:
                q1, q3 = np.percentile(nums, [25, 75])
                out = nums[(nums < q1 - 1.5 * (q3 - q1)) | (nums > q3 + 1.5 * (q3 - q1))]
                if len(out):
                    issues.append(("outliers", c, out.tolist()))
        dups = len(rows) - len({json.dumps(r, sort_keys=True) for r in rows})
        if dups:
            issues.append(("duplicates", "*", dups))
        return issues, max(0, 100 - 15 * len(issues))

    issues, score = audit(rows)
    clean, cscore = audit([{"id": i, "v": float(i)} for i in range(40)])
    _w(work, "dq.json", {"issues": issues, "score": score, "remediation": sorted(issues, key=lambda t: t[0])})
    kinds = {(k, c) for k, c, _ in issues}
    return [_c("planted nulls/constant/mixed/outlier/duplicate all found",
               kinds == {("nulls", "cat"), ("constant", "const"), ("mixed_types", "mix"), ("outliers", "price"), ("duplicates", "*")}, sorted(kinds)),
            _c("outlier is the planted 999", [v for k, c, v in issues if k == "outliers"] == [[999.0]], ""),
            _c("clean table scores 100, dirty scores lower", cscore == 100 and score < cscore and not clean, (score, cscore))]


# ---------------------------------------------------------------- ADATA-19
def _holm(p, alpha=0.05):
    order = sorted(range(len(p)), key=lambda i: p[i])
    rej = [False] * len(p)
    for k, i in enumerate(order):
        if p[i] <= alpha / (len(p) - k):
            rej[i] = True
        else:
            break
    return rej


def _bh(p, q=0.05):
    m = len(p)
    order = sorted(range(m), key=lambda i: p[i])
    kmax = max([k + 1 for k, i in enumerate(order) if p[i] <= (k + 1) / m * q] or [0])
    return [order.index(i) < kmax for i in range(m)]


def adata_19(work: Path):
    pv = [0.01, 0.04, 0.03, 0.005]
    holm, bh = _holm(pv), _bh(pv)
    # Kidney-stone data (Charig 1986): A wins each stratum, B wins pooled
    strata = {"small": {"A": (81, 87), "B": (234, 270)}, "large": {"A": (192, 263), "B": (55, 80)}}
    pooled = {t: sum(strata[s][t][0] for s in strata) / sum(strata[s][t][1] for s in strata) for t in ("A", "B")}
    per = {s: {t: v[0] / v[1] for t, v in d.items()} for s, d in strata.items()}
    simpson = all(per[s]["A"] > per[s]["B"] for s in per) and pooled["B"] > pooled["A"]
    template = ["Primary", "Decision-relevant", "Guardrails", "Multiplicity", "Pitfall screen", "Verdict"]
    _w(work, "readout.json", {"holm": holm, "bh": bh, "simpson": simpson, "template": template})
    return [_c("Holm rejects only 0.005 and 0.01", holm == [True, False, False, True], holm),
            _c("BH rejects all four (0.04 <= 4/4*0.05)", bh == [True, True, True, True], bh),
            _c("Simpson's paradox detected on kidney-stone data", simpson, (per, pooled)),
            _c("readout template has the 6 sections", len(template) == 6, template)]


# ---------------------------------------------------------------- ADATA-20
def _ses(y, a):
    f = [y[0]]
    for v in y[:-1]:
        f.append(a * v + (1 - a) * f[-1])
    return f


def _holt(y, a, b, h):
    lvl, tr = y[0], y[1] - y[0]
    for v in y[1:]:
        nl = a * v + (1 - a) * (lvl + tr)
        tr = b * (nl - lvl) + (1 - b) * tr
        lvl = nl
    return [lvl + (i + 1) * tr for i in range(h)]


def adata_20(work: Path):
    y = [100 + 5 * t for t in range(18)]
    train, test = y[:-4], y[-4:]
    holt = _holt(train, 0.5, 0.3, 4)
    ses_f = [_ses(train, 0.5)[-1] * 0.5 + 0.5 * train[-1]] * 4
    mape = lambda f: float(np.mean([abs(a - b) / a for a, b in zip(test, f)]))
    bias = lambda f: float(sum(b - a for a, b in zip(test, f)) / sum(test))
    inter = [0, 0, 5, 0, 0, 0, 7, 0, 0, 4, 0, 0]
    cv = np.std(inter) / np.mean(inter)
    method = "Croston" if cv > 0.5 else "SES"
    err = [10, 12, 9, 11, 10, 13]  # forecast persistently below actuals
    ts = sum(err) / (sum(abs(e) for e in err) / len(err))
    seasonal_ok = len(y) >= 12
    _w(work, "forecast.json", {"holt": holt, "ses": ses_f, "mape_holt": mape(holt), "mape_ses": mape(ses_f),
                               "method_intermittent": method, "tracking_signal": ts})
    return [_c("Holt on a linear trend: MAPE ~0 and |bias| <= 5%", mape(holt) < 1e-6 and abs(bias(holt)) <= 0.05, mape(holt)),
            _c("SES lags the trend: worse MAPE than Holt", mape(ses_f) > mape(holt), mape(ses_f)),
            _c("intermittent series (CV>0.5) routes to Croston", method == "Croston", round(cv, 2)),
            _c("one-sided errors: tracking signal 6 > 4 out of control", abs(ts - 6) < 1e-9 and ts > 4, ts),
            _c("18 periods >= 12 allows seasonal models", seasonal_ok, len(y))]


# ---------------------------------------------------------------- ADATA-21
def adata_21(work: Path):
    x = np.arange(1, 101, dtype=float)
    pct = {p: float(np.percentile(x, p)) for p in (1, 5, 25, 50, 75, 90, 95, 99)}
    skew = np.r_[np.ones(90), np.full(10, 100.0)]
    iqr_l, iqr_h = np.percentile(skew, [25, 75])
    cv = float(x.std(ddof=1) / x.mean())
    daily = np.r_[np.zeros(7), np.full(7, 14.0)]
    roll7 = np.convolve(daily, np.ones(7) / 7, mode="valid")
    _w(work, "describe.json", {"pct": pct, "skew_mean": skew.mean(), "skew_median": float(np.median(skew)), "cv": cv,
                               "roll7": roll7.tolist()})
    return [_c("percentiles of 1..100 (linear): p50 50.5, p25 25.75, p99 99.01",
               pct[50] == 50.5 and pct[25] == 25.75 and abs(pct[99] - 99.01) < 1e-9, pct),
            _c("skewed data: mean 10.9 far above median 1", skew.mean() == 10.9 and np.median(skew) == 1, ""),
            _c("skewed spread uses IQR = 0 here, not SD", iqr_h - iqr_l == 0 and skew.std() > 20, ""),
            _c("CV of 1..100 = 29.01/50.5 = 0.5745", abs(cv - 0.5745) < 1e-3, cv),
            _c("rolling 7d mean ramps 0 -> 14", roll7[0] == 0 and roll7[-1] == 14 and abs(roll7[3] - 6) < 1e-9, roll7.tolist())]


# ---------------------------------------------------------------- ADATA-22
def adata_22(work: Path):
    rng = np.random.default_rng(5)
    n = 200
    target = rng.integers(0, 2, n)
    cols = {"customer_id": np.arange(n), "tenure": rng.normal(20, 5, n), "refund_issued_after": target * 1.0,
            "score_from_target": target * 2 + 1, "spend": rng.normal(100, 10, n)}
    post_outcome = re.compile(r"(after|refund|cancel|churned)")
    leaks = []
    for c, v in cols.items():
        r = abs(np.corrcoef(v, target)[0, 1])
        if r > 0.95 or post_outcome.search(c):
            leaks.append((c, "target-derived/post-outcome", round(float(r), 3)))
        elif c.endswith("_id"):
            leaks.append((c, "ID-encoded", round(float(r), 3)))
    dups = int(n - len({tuple(np.round([cols[c][i] for c in cols], 6)) for i in range(n)}))
    report = {"target": "churn", "leakage_candidates": leaks, "duplicates": dups,
              "cleaning_log": [], "findings_as_hypotheses": True}
    _w(work, "eda.json", report)
    names = [c for c, _, _ in leaks]
    return [_c("post-outcome and target-derived columns listed as leakage",
               {"refund_issued_after", "score_from_target"} <= set(names), names),
            _c("ID column flagged as ID-encoded", "customer_id" in names, names),
            _c("genuine features tenure/spend not flagged", "tenure" not in names and "spend" not in names, names),
            _c("no duplicates in fixture", dups == 0, dups)]


# ---------------------------------------------------------------- ADATA-23
def adata_23(work: Path):
    rng = np.random.default_rng(11)
    n = 120
    x1, x2 = rng.normal(0, 1, n), rng.normal(0, 1, n)
    x3 = x1 * 0.98 + rng.normal(0, 0.05, n)
    y = 3 + 2 * x1 - 1 * x2 + rng.normal(0, 0.1, n)
    X = np.c_[np.ones(n), x1, x2]
    tr, te = slice(0, 96), slice(96, n)
    beta = np.linalg.lstsq(X[tr], y[tr], rcond=None)[0]
    rmse = float(np.sqrt(np.mean((X[te] @ beta - y[te]) ** 2)))

    def vif(Z, j):
        o = np.delete(Z, j, axis=1)
        o = np.c_[np.ones(len(Z)), o]
        b = np.linalg.lstsq(o, Z[:, j], rcond=None)[0]
        r2 = 1 - np.var(Z[:, j] - o @ b) / np.var(Z[:, j])
        return 1 / (1 - r2)

    Z = np.c_[x1, x2, x3]
    vifs = [vif(Z, j) for j in range(3)]
    receipts, disb, opening = [50] * 13, [45] * 13, 100
    closing = opening + sum(receipts) - sum(disb)
    _w(work, "drivers.json", {"beta": beta.tolist(), "holdout_rmse": rmse, "vif": vifs, "cash_13w_closing": closing})
    return [_c("recovers intercept 3, slopes 2 and -1 within 0.05", np.allclose(beta, [3, 2, -1], atol=0.05), beta.round(3).tolist()),
            _c("holdout RMSE near noise sd 0.1", 0.05 < rmse < 0.2, rmse),
            _c("collinear driver x3 has VIF > 10, x2 ~1", vifs[2] > 10 and vifs[1] < 2, [round(v, 1) for v in vifs]),
            _c("13-week direct cash roll: 100 + 650 - 585 = 165", closing == 165, closing)]


# ---------------------------------------------------------------- ADATA-24
def adata_24(work: Path):
    def fit(seed):
        rng = np.random.default_rng(seed)
        n = 400
        x = rng.uniform(0, 10, n)
        y = 1 + 0.5 * x + rng.normal(0, 1, n) * x  # heteroskedastic
        X = np.c_[np.ones(n), x]
        b = np.linalg.solve(X.T @ X, X.T @ y)
        e = y - X @ b
        inv = np.linalg.inv(X.T @ X)
        classic = np.sqrt(np.diag(inv * (e @ e) / (n - 2)))
        hc1 = np.sqrt(np.diag(inv @ (X.T * e ** 2) @ X @ inv) * n / (n - 2))
        return b, classic, hc1

    b, classic, hc1 = fit(42)
    b2, _, _ = fit(42)
    table = "| term | coef | SE (HC1) |\n|---|---|---|\n" + "\n".join(
        f"| {t} | {c:.3f} | {s:.3f} |" for t, c, s in zip(["const", "x"], b, hc1))
    _w(work, "regression_table.md", table)
    _w(work, "prereg.json", {"hypothesis": "slope > 0", "outcome": "y", "spec": "OLS y ~ x, HC1"})
    return [_c("slope estimate near true 0.5", abs(b[1] - 0.5) < 0.2, b.round(3).tolist()),
            _c("heteroskedastic data: robust SE of slope > classic SE", hc1[1] > classic[1], (classic[1], hc1[1])),
            _c("top-to-bottom rerun with same seed is identical", np.array_equal(b, b2), "seed 42"),
            _c("table has 2 coefficient rows", table.count("\n| ") == 2, "")]


# ---------------------------------------------------------------- ADATA-25
def adata_25(work: Path):
    def choose(a, b, paired=False):
        normal = stats.shapiro(a).pvalue > 0.05 and stats.shapiro(b).pvalue > 0.05
        if paired:
            return ("paired t", stats.ttest_rel(a, b)) if normal else ("Wilcoxon", stats.wilcoxon(a, b))
        if normal:
            eq = stats.levene(a, b).pvalue > 0.05
            return ("Student t" if eq else "Welch t", stats.ttest_ind(a, b, equal_var=eq))
        return ("Mann-Whitney U", stats.mannwhitneyu(a, b))

    rng = np.random.default_rng(1)
    na, nb = rng.normal(10, 1, 40), rng.normal(11, 1, 40)
    ea, eb = rng.exponential(1, 40) ** 3, rng.exponential(2, 40) ** 3
    hv = rng.normal(10, 1, 40), rng.normal(11, 6, 40)
    picks = {"normal": choose(na, nb)[0], "skewed": choose(ea, eb)[0], "unequal_var": choose(*hv)[0],
             "paired_normal": choose(na, na + rng.normal(0.5, 0.2, 40), paired=True)[0]}
    d = (nb.mean() - na.mean()) / math.sqrt((na.var(ddof=1) + nb.var(ddof=1)) / 2)
    _w(work, "test_choice.json", {"picks": picks, "effect_size_d": d})
    return [_c("normal equal-variance groups -> Student t", picks["normal"] == "Student t", picks),
            _c("heavily skewed -> Mann-Whitney U", picks["skewed"] == "Mann-Whitney U", picks),
            _c("unequal variances -> Welch t", picks["unequal_var"] == "Welch t", picks),
            _c("paired normal -> paired t", picks["paired_normal"] == "paired t", picks),
            _c("effect size d ~ 1 reported", 0.6 < d < 1.4, d)]


# ---------------------------------------------------------------- ADATA-26
def adata_26(work: Path):
    raw = ("﻿name;amount;date\r\nAli;10,5;2026-01-02\r\nMona;7;02/01/2026\r\nBad\x00Row;1;2;3\r\n"
           "\"Sa;ra\";3;2026-01-04\r\nonly_one_field\r\n").encode("utf-8")
    src = work / "messy.csv"
    src.write_bytes(raw)
    checksum = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")  # strict UTF-8 first
    bom = text.startswith("﻿")
    text = text.lstrip("﻿")
    nulls = text.count("\x00")
    text = text.replace("\x00", "")
    dialect = csv.Sniffer().sniff(text[:200], delimiters=";,\t")
    good, quarantine = [], []
    rd = csv.reader(io.StringIO(text, newline=""), dialect)
    header = [h.strip().lower() for h in next(rd)]
    for line_no, row in enumerate(rd, start=2):
        if len(row) != len(header):
            quarantine.append({"line": line_no, "raw": dialect.delimiter.join(row), "fields": len(row), "error": "field count"})
            continue
        rec = dict(zip(header, row))
        rec["amount"] = float(rec["amount"].replace(",", "."))
        m = re.fullmatch(r"(\d\d)/(\d\d)/(\d{4})", rec["date"])
        if m:
            rec["date"] = f"{m[3]}-{m[2]}-{m[1]}"
        good.append(rec)
    _w(work, "clean.json", good)
    _w(work, "quarantine.json", quarantine)
    return [_c("BOM, CRLF and 1 null byte detected", bom and "\r\n" in raw.decode() and nulls == 1, (bom, nulls)),
            _c("dialect sniffed as ';' (regex split avoided: quoted 'Sa;ra' kept)", dialect.delimiter == ";" and good[-1]["name"] == "Sa;ra", dialect.delimiter),
            _c("every row counted: 3 parsed + 2 quarantined = 5", len(good) == 3 and len(quarantine) == 2, (len(good), len(quarantine))),
            _c("quarantine keeps line numbers 4 and 6", [q["line"] for q in quarantine] == [4, 6], quarantine),
            _c("decimal comma and dd/mm/yyyy normalised", good[0]["amount"] == 10.5 and good[1]["date"] == "2026-01-02", good[:2]),
            _c("source checksum recorded", len(checksum) == 64, checksum[:12])]


# ---------------------------------------------------------------- ADATA-27
def _wilson(x, n, z=1.96):
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def adata_27(work: Path):
    def annotate(x1, n1, x2, n2):
        if not n1 or not n2:
            return "insufficient data"
        p1, p2 = x1 / n1, x2 / n2
        se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
        lo, hi = p2 - p1 - 1.96 * se, p2 - p1 + 1.96 * se
        return "within normal variation" if lo <= 0 <= hi else ("real increase" if lo > 0 else "real decrease")

    lo, hi = _wilson(0, 10)
    pois = (stats.chi2.ppf(0.025, 2 * 3) / 2, stats.chi2.ppf(0.975, 2 * 4) / 2)
    days = np.arange(10)
    vals = 5 + 0.0 * days + np.array([0.1, -0.1] * 5)
    sl = stats.linregress(days, vals)
    trend_ci = (sl.slope - 2.306 * sl.stderr, sl.slope + 2.306 * sl.stderr)
    res = {"small": annotate(48, 100, 52, 100), "big": annotate(400, 1000, 500, 1000), "none": annotate(5, 0, 6, 0),
           "wilson_0_10": (lo, hi), "poisson_3": pois, "trend_ci": trend_ci}
    _w(work, "annotations.json", res)
    return [_c("48% vs 52% on n=100: within normal variation", res["small"] == "within normal variation", res["small"]),
            _c("40% vs 50% on n=1000: real increase", res["big"] == "real increase", res["big"]),
            _c("no denominator -> insufficient data", res["none"] == "insufficient data", res["none"]),
            _c("Wilson CI for 0/10 is [0, 0.278]", abs(lo) < 1e-12 and abs(hi - 0.2775) < 1e-3, (lo, hi)),
            _c("exact Poisson CI for count 3 = [0.619, 8.767]", abs(pois[0] - 0.619) < 1e-3 and abs(pois[1] - 8.767) < 1e-3, pois),
            _c("flat noisy trend: slope CI spans zero", trend_ci[0] < 0 < trend_ci[1], trend_ci)]


# ---------------------------------------------------------------- ADATA-28
def adata_28(work: Path):
    def assign(unit, exp="exp1", split=0.5):
        h = int(hashlib.sha256(f"{exp}:{unit}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
        return "treatment" if h < split else "control"

    units = [f"user{i}" for i in range(10000)]
    a1 = [assign(u) for u in units]
    a2 = [assign(u) for u in units]
    obs = [a1.count("control"), a1.count("treatment")]
    p_fair = stats.chisquare(obs, [5000, 5000]).pvalue
    p_srm = stats.chisquare([5000, 5400], [5200, 5200]).pvalue
    exposure = [{"unit": u, "variant": v, "exposed": i % 3 != 0} for i, (u, v) in enumerate(zip(units[:9], a1))]
    _w(work, "assignment.json", {"counts": obs, "p_fair": p_fair, "p_srm": p_srm, "exposure_log": exposure,
                                 "valid": p_srm >= 0.001})
    return [_c("assignment is sticky (same unit, same arm)", a1 == a2, "10000 units"),
            _c("hash split near 50/50: SRM test passes", p_fair > 0.001, (obs, p_fair)),
            _c("5000 vs 5400 on intended 50/50 fails SRM (p<0.001)", p_srm < 0.001, p_srm),
            _c("exposure logged separately from assignment", sum(e["exposed"] for e in exposure) == 6, 6)]


# ---------------------------------------------------------------- ADATA-29
def adata_29(work: Path):
    pats = {"email": r"^[^@\s]+@[^@\s]+\.\w+$", "phone": r"^\+?\d[\d\s-]{7,}$", "national_id": r"^\d{14}$"}
    table = {"user_ref": ["u1", "u2", "u3"], "contact": ["a@x.io", "b@y.org", "c@z.com"], "mobile": ["+20 100 123 4567", "+20 111 222 3333", "01001234567"],
             "nid": ["29801011234567", "30001011234567", "29912121234567"], "amount": ["10", "20", "30"]}
    tags = {}
    for col, vals in table.items():
        for tag, p in pats.items():
            if sum(bool(re.match(p, v)) for v in vals) / len(vals) >= 0.8:
                tags[col] = tag
    runs = [{"job": "stg_users", "reads": ["raw.users"], "writes": ["stg.users"]},
            {"job": "dim_user", "reads": ["stg.users"], "writes": ["mart.dim_user"]}]
    edges = [(r, w) for j in runs for r in j["reads"] for w in j["writes"]]
    upstream = lambda t: {a for a, b in edges if b == t} | {x for a, b in edges if b == t for x in upstream(a)}
    sample = {c: (["<scrubbed>"] * 3 if c in tags else v) for c, v in table.items()}
    _w(work, "catalog.json", {"pii_tags": tags, "lineage": edges, "sample": sample})
    return [_c("contact/mobile/nid tagged email/phone/national_id", tags == {"contact": "email", "mobile": "phone", "nid": "national_id"}, tags),
            _c("amount and user_ref not tagged", "amount" not in tags and "user_ref" not in tags, tags),
            _c("lineage: mart.dim_user traces to raw.users", upstream("mart.dim_user") == {"stg.users", "raw.users"}, edges),
            _c("sample scrubs every classified column", all(sample[c] == ["<scrubbed>"] * 3 for c in tags) and sample["amount"] == ["10", "20", "30"], "")]


# ---------------------------------------------------------------- ADATA-30
def adata_30(work: Path):
    def guard(op, table, consumers, retention_h=None, checkpoint_h=168, time_travel_h=168, replayable=True):
        if consumers is None:
            return "allow-with-warning"  # fails open when consumers cannot be verified
        if op in ("DROP", "CREATE OR REPLACE", "VACUUM") and consumers.get(table):
            return "block: active streaming consumers"
        if op == "VACUUM" and retention_h is not None and retention_h < max(checkpoint_h, time_travel_h):
            return "block: retention below checkpoint/time-travel need"
        if op == "FULL REFRESH" and not replayable:
            return "block: source not replayable"
        return "allow"

    cons = {"events": ["stream_q1"], "dim": []}
    cases = {"drop_live": guard("DROP", "events", cons), "drop_idle": guard("DROP", "dim", cons),
             "vacuum_short": guard("VACUUM", "dim", cons, retention_h=24), "vacuum_ok": guard("VACUUM", "dim", cons, retention_h=200),
             "refresh_unreplayable": guard("FULL REFRESH", "dim", cons, replayable=False), "unknown": guard("DROP", "events", None)}
    merge = "MERGE INTO t USING s ON t.id = s.id AND t.event_date = s.event_date"
    narrowed = "event_date" in merge
    _w(work, "guard.json", {**cases, "merge_narrowed_to_cluster_key": narrowed})
    return [_c("DROP on a table with a live stream is blocked", cases["drop_live"].startswith("block"), cases["drop_live"]),
            _c("DROP on an idle table allowed", cases["drop_idle"] == "allow", cases["drop_idle"]),
            _c("VACUUM 24h < 168h checkpoint blocked; 200h allowed", cases["vacuum_short"].startswith("block") and cases["vacuum_ok"] == "allow", ""),
            _c("full refresh of non-replayable source blocked", cases["refresh_unreplayable"].startswith("block"), ""),
            _c("unverifiable consumers fail open with warning", cases["unknown"] == "allow-with-warning", cases["unknown"]),
            _c("MERGE predicate includes clustering key", narrowed, merge)]


# ---------------------------------------------------------------- ADATA-31
def adata_31(work: Path):
    rules = [("credentials", r"auth|password|401|403|token expired"), ("schema_drift", r"column .* (not found|does not exist)|type mismatch"),
             ("incremental_field", r"incremental|cursor|non-monotonic"), ("rate_limit", r"429|rate limit|too many requests")]
    recovery = {"credentials": "reconnect", "schema_drift": "resync", "incremental_field": "tune config + reload", "rate_limit": "lower frequency, retry"}
    sources = [("stripe", "HTTP 429 Too Many Requests", 3), ("pg", "column \"plan\" does not exist", 30), ("hubspot", "401 token expired", 72),
               ("ga", "ok", 1), ("mysql", "cursor value non-monotonic on updated_at", 10)]
    rows = []
    for name, err, stale_h in sources:
        cls = next((c for c, p in rules if re.search(p, err, re.I)), None)
        rows.append({"source": name, "class": cls, "recovery": recovery.get(cls), "stale_h": stale_h, "degraded": cls is not None})
    degraded = sorted((r for r in rows if r["degraded"]), key=lambda r: -r["stale_h"])
    _w(work, "sync_health.json", degraded)
    cls = {r["source"]: r["class"] for r in rows}
    return [_c("each error mapped to its class", cls == {"stripe": "rate_limit", "pg": "schema_drift", "hubspot": "credentials", "ga": None,
                                                         "mysql": "incremental_field"}, cls),
            _c("credentials -> reconnect, drift -> resync", rows[2]["recovery"] == "reconnect" and rows[1]["recovery"] == "resync", ""),
            _c("degraded ranked by staleness: hubspot, pg, mysql, stripe", [r["source"] for r in degraded] == ["hubspot", "pg", "mysql", "stripe"],
               [r["source"] for r in degraded])]


# ---------------------------------------------------------------- ADATA-32
def adata_32(work: Path):
    proj = work / "dbt_project"
    files = {"models/staging/stg_orders.sql": "select id, cast(amount as int) amount from {{ source('shop','orders') }}",
             "models/intermediate/int_orders_enriched.sql": "select * from {{ ref('stg_orders') }}",
             "models/marts/fct_orders.sql": "select * from {{ ref('int_orders_enriched') }}",
             "models/marts/dim_customer.sql": "select * from {{ source('shop','customers') }}",
             "models/schema.yml": "models:\n  - name: fct_orders\n    description: '{{ doc(\"fct_orders\") }}'\n    columns:\n      - name: id\n        tests: [unique, not_null]\n",
             "profiles.yml.example": "default: {target: dev}\n", ".gitignore": "profiles.yml\ntarget/\n",
             "bi/dashboard.sql": "select * from int_orders_enriched", "seeds/.keep": "", "snapshots/.keep": "", "macros/.keep": "",
             ".github/workflows/ci.yml": "on: pull_request\njobs: {build: {steps: [{run: dbt build}]}}\n"}
    for k, v in files.items():
        (proj / k).parent.mkdir(parents=True, exist_ok=True)
        (proj / k).write_text(v)
    viol = []
    for p in proj.rglob("*.sql"):
        rel, txt = p.relative_to(proj).as_posix(), p.read_text()
        if rel.startswith("models/staging") and "source(" not in txt:
            viol.append((rel, "staging must use source()"))
        if rel.startswith("models/marts") and "source(" in txt:
            viol.append((rel, "marts use ref() only"))
        if rel.startswith("bi/") and re.search(r"\bint_\w+", txt):
            viol.append((rel, "BI reads int_*"))
    viol.sort()
    _w(work, "lint.json", viol)
    return [_c("planted mart reading source() is caught", ("models/marts/dim_customer.sql", "marts use ref() only") in viol, viol),
            _c("planted BI query on int_* is caught", ("bi/dashboard.sql", "BI reads int_*") in viol, viol),
            _c("exactly 2 violations (good files pass)", len(viol) == 2, len(viol)),
            _c("profiles.yml kept out of git, example shipped", not (proj / "profiles.yml").exists() and "profiles.yml" in files[".gitignore"], ""),
            _c("CI runs dbt build on PR; unique/not_null tests present", "dbt build" in files[".github/workflows/ci.yml"] and "not_null" in files["models/schema.yml"], "")]


# ---------------------------------------------------------------- ADATA-34
def adata_34(work: Path):
    def strategy(src):
        if src.get("change_log"):
            return "CDC"
        if src.get("immutable"):
            return "append+dedup"
        if src.get("ordered_cursor"):
            return "incremental with overlap + upsert"
        if src.get("rows", 0) < 1e6 and src.get("stable"):
            return "full refresh with atomic swap"
        return "snapshot diff"

    srcs = {"countries": {"rows": 250, "stable": True}, "orders": {"ordered_cursor": "updated_at"}, "pg_wal": {"change_log": True},
            "clicks": {"immutable": True}, "legacy_ftp": {"rows": 5e6}}
    plan = {k: strategy(v) for k, v in srcs.items()}

    state = {"checkpoint": "2026-01-01"}

    def run(batch_max, valid):
        published = valid
        if published:  # checkpoint only after durable publish + validation
            state["checkpoint"] = batch_max
        return state["checkpoint"]

    after_bad = run("2026-01-05", valid=False)
    after_good = run("2026-01-05", valid=True)
    _w(work, "contract.json", {"strategies": plan, "checkpoint": state})
    return [_c("strategy table maps all five source kinds",
               plan == {"countries": "full refresh with atomic swap", "orders": "incremental with overlap + upsert", "pg_wal": "CDC",
                        "clicks": "append+dedup", "legacy_ftp": "snapshot diff"}, plan),
            _c("failed validation leaves checkpoint at 2026-01-01", after_bad == "2026-01-01", after_bad),
            _c("validated publish advances checkpoint", after_good == "2026-01-05", after_good)]


# ---------------------------------------------------------------- ADATA-35
def adata_35(work: Path):
    stages = [{"id": 1, "task_ms": [100] * 199 + [5000], "spill_mb": 0, "files": 10, "dim_mb": 0, "collect": False},
              {"id": 2, "task_ms": [100] * 50, "spill_mb": 0, "files": 10, "dim_mb": 8, "collect": False},
              {"id": 3, "task_ms": [100] * 50, "spill_mb": 0, "files": 20000, "dim_mb": 0, "collect": False},
              {"id": 4, "task_ms": [100] * 50, "spill_mb": 0, "files": 10, "dim_mb": 0, "collect": True}]
    fixes = {}
    for s in stages:
        t = np.array(s["task_ms"])
        f = []
        if t.max() > 5 * np.median(t):
            f.append("AQE skew join / salting")
        if 0 < s["dim_mb"] <= 10:
            f.append("broadcast small dim")
        if s["files"] > 1000:
            f.append("OPTIMIZE (compact tiny files)")
        if s["collect"]:
            f.append("remove collect() on driver")
        fixes[s["id"]] = f
    keys = ["hot"] * 900 + [f"k{i}" for i in range(100)]
    part = lambda ks, n: np.bincount([int(hashlib.md5(k.encode()).hexdigest(), 16) % n for k in ks], minlength=n)
    before = part(keys, 8).max()
    salted = [f"{k}#{i % 8}" if k == "hot" else k for i, k in enumerate(keys)]
    after = part(salted, 8).max()
    _w(work, "tuning.json", {"fixes": fixes, "max_partition_before": int(before), "after_salting": int(after)})
    return [_c("one long task -> skew fix", fixes[1] == ["AQE skew join / salting"], fixes[1]),
            _c("8 MB dim -> broadcast", fixes[2] == ["broadcast small dim"], fixes[2]),
            _c("20000 files -> OPTIMIZE", fixes[3] == ["OPTIMIZE (compact tiny files)"], fixes[3]),
            _c("driver collect -> remove", fixes[4] == ["remove collect() on driver"], fixes[4]),
            _c("salting the hot key cuts the largest partition (metric moved)", after < before / 3, (int(before), int(after)))]


# ---------------------------------------------------------------- ADATA-36
def adata_36(work: Path):
    src = [(1, "a", 10, "2026-01-01"), (2, "b", None, "2026-01-01"), (2, "b", 5, "2026-01-02"), (3, "c", 7, "2026-01-03"),
           (4, "d", -1, "2026-01-01")]  # duplicate key 2, null, late row, bad record

    def run_incremental(db, rows):
        db.execute("create table if not exists tgt(id primary key, name, amount, ts)")
        db.execute("create table if not exists bad(id, reason)")
        for r in rows:
            if r[2] is not None and r[2] < 0:
                db.execute("insert into bad values(?,?)", (r[0], "negative amount"))
                continue
            db.execute("insert into tgt values(?,?,?,?) on conflict(id) do update set name=excluded.name, amount=excluded.amount, ts=excluded.ts "
                       "where excluded.ts >= tgt.ts", r)

    db = sqlite3.connect(work / "etl.sqlite")
    run_incremental(db, src)
    once = db.execute("select * from tgt order by id").fetchall()
    run_incremental(db, src)
    run_incremental(db, list(reversed(src)))  # replay out of order
    twice = db.execute("select * from tgt order by id").fetchall()
    bad = db.execute("select count(distinct id) from bad").fetchone()[0]
    db.commit()
    good_src = {r[0] for r in src if not (r[2] is not None and r[2] < 0)}
    tsum = db.execute("select sum(amount) from tgt").fetchone()[0]
    return [_c("rerun and out-of-order replay give identical target", once == twice, once),
            _c("dedup keeps latest row for id 2 (amount 5)", dict((r[0], r[2]) for r in twice)[2] == 5, twice),
            _c("count reconciles: 3 distinct good keys", len(twice) == len(good_src) == 3, len(twice)),
            _c("sum reconciles to 22", tsum == 22, tsum),
            _c("bad record routed to failure path", bad == 1, bad)]


# ---------------------------------------------------------------- ADATA-37
def adata_37(work: Path):
    source_cols = {"id": "integer", "updated_at": "timestamp", "email": "text"}

    def validate(cfg, running=False):
        errs = []
        if running:
            errs.append("schema is running: do not tune")
        f = cfg.get("incremental_field")
        if cfg["sync_type"] in ("incremental", "append") and (f not in source_cols or cfg.get("incremental_field_type") != source_cols.get(f)):
            errs.append("incremental_field type mismatch")
        if cfg["sync_type"] == "cdc" and not cfg.get("primary_key_columns"):
            errs.append("CDC needs primary_key_columns")
        return errs

    cases = {"good": validate({"sync_type": "incremental", "incremental_field": "updated_at", "incremental_field_type": "timestamp"}),
             "wrong_type": validate({"sync_type": "incremental", "incremental_field": "updated_at", "incremental_field_type": "integer"}),
             "cdc_no_pk": validate({"sync_type": "cdc"}), "cdc_ok": validate({"sync_type": "cdc", "primary_key_columns": ["id"]}),
             "running": validate({"sync_type": "full"}, running=True)}
    before, after = "2026-11-01T00:00:00", "2026-11-03T10:00:00"
    _w(work, "sync_tune.json", {**cases, "last_synced_advanced": after > before})
    return [_c("matching incremental field passes", cases["good"] == [], cases["good"]),
            _c("type mismatch rejected", cases["wrong_type"] == ["incremental_field type mismatch"], cases["wrong_type"]),
            _c("CDC without primary key rejected, with key accepted", cases["cdc_no_pk"] and not cases["cdc_ok"], cases["cdc_no_pk"]),
            _c("running schema is not tuned", cases["running"] == ["schema is running: do not tune"], cases["running"]),
            _c("last_synced_at advanced after reload", after > before, (before, after))]


# ---------------------------------------------------------------- ADATA-38
def adata_38(work: Path):
    rules = [("query/limit-required", lambda s: s.lstrip().upper().startswith("SELECT") and not re.search(r"\bLIMIT\b", s, re.I)),
             ("query/no-select-star", lambda s: re.search(r"SELECT\s+\*", s, re.I)),
             ("schema/mergetree-order-by", lambda s: re.search(r"ENGINE\s*=\s*MergeTree", s, re.I) and not re.search(r"ORDER BY", s, re.I)),
             ("insert/batch-rows", lambda s: s.upper().startswith("INSERT") and s.upper().count("),(") + 1 < 1000 and "VALUES" in s.upper())]
    stmts = {"q1": "SELECT * FROM events", "q2": "SELECT ts, user FROM events WHERE ts > now() - 3600 LIMIT 100",
             "d1": "CREATE TABLE e (ts DateTime, u String) ENGINE = MergeTree", "d2": "CREATE TABLE e (ts DateTime) ENGINE = MergeTree ORDER BY ts",
             "i1": "INSERT INTO e VALUES (1),(2)"}
    found = {k: [n for n, f in rules if f(s)] for k, s in stmts.items()}
    _w(work, "clickhouse_review.json", found)
    return [_c("SELECT * without LIMIT cites two rules", found["q1"] == ["query/limit-required", "query/no-select-star"], found["q1"]),
            _c("narrow limited query is clean", found["q2"] == [], found["q2"]),
            _c("MergeTree without ORDER BY flagged; with ORDER BY clean", found["d1"] == ["schema/mergetree-order-by"] and found["d2"] == [], ""),
            _c("tiny insert flagged for batching", found["i1"] == ["insert/batch-rows"], found["i1"])]


# ---------------------------------------------------------------- ADATA-40
def adata_40(work: Path):
    db = sqlite3.connect(work / "tune.sqlite")
    db.execute("create table orders(id integer primary key, customer text, status text, total real)")
    db.executemany("insert into orders(customer,status,total) values(?,?,?)",
                   [(f"c{i % 500}", "open" if i % 10 == 0 else "closed", i * 1.0) for i in range(5000)])
    plan = lambda q: " ".join(r[-1] for r in db.execute("EXPLAIN QUERY PLAN " + q))
    q = "select id,total from orders where customer = 'c7'"
    before = plan(q)
    db.execute("create index ix_customer on orders(customer)")
    db.execute("ANALYZE")
    after = plan(q)
    func = plan("select id from orders where lower(customer) = 'c7'")
    db.execute("create index ix_open on orders(total) where status='open'")
    partial = plan("select id from orders where status='open' and total > 10")
    db.commit()
    _w(work, "plans.json", {"before": before, "after": after, "function_on_column": func, "partial": partial})
    return [_c("before index: full SCAN", before.startswith("SCAN"), before),
            _c("after B-tree index: SEARCH USING INDEX ix_customer", "SEARCH" in after and "ix_customer" in after, after),
            _c("function on indexed column defeats the index seek (SCAN, no SEARCH)", "SEARCH" not in func and func.startswith("SCAN"), func),
            _c("partial index used for its subset predicate", "ix_open" in partial, partial)]


# ---------------------------------------------------------------- ADATA-43
def adata_43(work: Path):
    stmts = [{"q": "select * from a", "calls": 10, "mean_ms": 500}, {"q": "select * from b where x=1", "calls": 10000, "mean_ms": 3},
             {"q": "select 1", "calls": 100, "mean_ms": 0.1}]
    ranked = sorted(stmts, key=lambda s: -s["calls"] * s["mean_ms"])
    plan = {"Node Type": "Sort", "Sort Space Type": "Disk", "Plans": [
        {"Node Type": "Seq Scan", "Relation Name": "b", "Plan Rows": 10, "Actual Rows": 50000, "Rows Removed by Filter": 950000}]}
    advice = []

    def walk(n):
        if n.get("Sort Space Type") == "Disk":
            advice.append("raise work_mem")
        if n["Node Type"] == "Seq Scan" and n.get("Rows Removed by Filter", 0) > 100000:
            advice.append(f"index on {n['Relation Name']}")
        if n.get("Plan Rows") and n.get("Actual Rows", 0) / n["Plan Rows"] > 10:
            advice.append(f"ANALYZE {n['Relation Name']}")
        for c in n.get("Plans", []):
            walk(c)

    walk(plan)
    idx = [{"name": "ix_old", "idx_scan": 0, "full_cycle_seen": False}, {"name": "ix_dead", "idx_scan": 0, "full_cycle_seen": True}]
    drop = [i["name"] for i in idx if i["idx_scan"] == 0 and i["full_cycle_seen"]]
    ddl = "CREATE INDEX CONCURRENTLY ix_b_x ON b(x)"
    _w(work, "pg_diag.json", {"ranked": ranked, "advice": advice, "unused": drop, "ddl": ddl})
    return [_c("ranking by total_exec_time puts b (30000 ms) first", ranked[0]["q"].endswith("x=1"), [s["q"] for s in ranked]),
            _c("disk sort -> work_mem; big filter -> index; 5000x row misestimate -> ANALYZE",
               advice == ["raise work_mem", "index on b", "ANALYZE b"], advice),
            _c("idx_scan=0 listed only after a full usage cycle", drop == ["ix_dead"], drop),
            _c("index built CONCURRENTLY", "CONCURRENTLY" in ddl, ddl)]


# ---------------------------------------------------------------- ADATA-44
def adata_44(work: Path):
    END = "9999-12-31 23:59:59"
    db = sqlite3.connect(work / "temporal.sqlite")
    db.execute("create table price(id, value, system_from text not null, system_to text not null, primary key(id, system_to))")
    db.execute("create index ix_from on price(id, system_from)")

    def upsert(i, v, now):
        cur = db.execute("select value from price where id=? and system_to=?", (i, END)).fetchone()
        if cur and cur[0] == v:
            return False  # skip unchanged
        db.execute("update price set system_to=? where id=? and system_to=?", (now, i, END))
        db.execute("insert into price values(?,?,?,?)", (i, v, now, END))
        return True

    upsert(1, 10, "2026-01-01 00:00:00")
    upsert(1, 12, "2026-02-01 00:00:00")
    skipped = not upsert(1, 12, "2026-03-01 00:00:00")
    asof = lambda t: db.execute("select value from price where id=1 and system_from<=? and system_to>?", (t, t)).fetchone()[0]
    jan = asof("2026-01-15 00:00:00")
    upsert(1, jan, "2026-04-01 00:00:00")  # rollback = phase the prior version back in
    rows = db.execute("select value, system_from, system_to from price order by system_from").fetchall()
    contiguous = all(rows[k][2] == rows[k + 1][1] for k in range(len(rows) - 1))
    db.commit()
    return [_c("as-of January returns 10, February returns 12", jan == 10 and asof("2026-02-15 00:00:00") == 12, rows),
            _c("unchanged value is skipped (no new version)", skipped, len(rows)),
            _c("rollback phases in prior value 10 as new current", rows[-1][0] == 10 and rows[-1][2] == END, rows[-1]),
            _c("versions are contiguous (to == next from)", contiguous and len(rows) == 3, rows)]


# ---------------------------------------------------------------- ADATA-45
def adata_45(work: Path):
    db = sqlite3.connect(work / "audit.sqlite")
    db.executescript("""
    create table accounts(id integer primary key, owner text, balance real);
    create table audit_log(table_name, record_id, action, old_values, new_values, changed_by, changed_at default current_timestamp, client_ip);
    create table ctx(user, ip);
    insert into ctx values('alice','10.0.0.5');
    """)
    for act, ref, oldv, newv in (("INSERT", "new", "null", "json_object('owner',new.owner,'balance',new.balance)"),
                                 ("UPDATE", "new", "json_object('owner',old.owner,'balance',old.balance)", "json_object('owner',new.owner,'balance',new.balance)"),
                                 ("DELETE", "old", "json_object('owner',old.owner,'balance',old.balance)", "null")):
        db.execute(f"""create trigger t_{act.lower()} after {act} on accounts begin
          insert into audit_log(table_name,record_id,action,old_values,new_values,changed_by,client_ip)
          select 'accounts', {ref}.id, '{act}', {oldv}, {newv}, user, ip from ctx; end""")
    db.execute("insert into accounts(owner,balance) values('x',100)")
    db.execute("update accounts set balance=80 where id=1")
    db.execute("delete from accounts where id=1")
    log = db.execute("select action, old_values, new_values, changed_by, client_ip from audit_log order by rowid").fetchall()
    db.commit()
    yearly = 1_000_000 * 200
    plan = {"low": yearly * 0.10, "high": yearly * 0.30}
    _w(work, "audit.json", {"log": log, "storage_plan_bytes": plan})
    return [_c("three audit rows: INSERT, UPDATE, DELETE", [r[0] for r in log] == ["INSERT", "UPDATE", "DELETE"], log),
            _c("UPDATE stores old 100 and new 80 as JSON", json.loads(log[1][1])["balance"] == 100 and json.loads(log[1][2])["balance"] == 80, log[1]),
            _c("changed_by and client_ip captured", log[2][3:] == ("alice", "10.0.0.5"), log[2][3:]),
            _c("storage plan is 10-30% of table bytes", plan == {"low": 2e7, "high": 6e7}, plan)]


# ---------------------------------------------------------------- ADATA-46
def adata_46(work: Path):
    rng = np.random.default_rng(0)
    docs = rng.normal(0, 1, (400, 16))
    docs /= np.linalg.norm(docs, axis=1, keepdims=True)
    q = docs[:20] + rng.normal(0, 0.05, (20, 16))
    truth = np.argsort(-(q @ docs.T), axis=1)[:, :5]
    cents = docs[rng.choice(400, 16, replace=False)]
    assign = np.argmax(docs @ cents.T, axis=1)

    def ann(nprobe):
        hits = 0
        for i, v in enumerate(q):
            lists = np.argsort(-(cents @ v))[:nprobe]
            cand = np.where(np.isin(assign, lists))[0]
            top = cand[np.argsort(-(docs[cand] @ v))[:5]]
            hits += len(set(top) & set(truth[i]))
        return hits / (5 * len(q))

    rec = {p: ann(p) for p in (1, 4, 16)}
    shifted = docs + 3
    shifted /= np.linalg.norm(shifted, axis=1, keepdims=True)
    aniso = float(np.mean(shifted[:50] @ shifted[:50].T))
    iso = float(np.mean(docs[:50] @ docs[:50].T))
    rrf = lambda ranks, k=60: sum(1 / (k + r) for r in ranks)
    fused = {"d1": rrf([1, 3]), "d2": rrf([2, 1])}
    raw_sum = {"d1": 0.9 + 12.0, "d2": 0.8 + 15.0}  # incomparable scales would dominate
    _w(work, "retrieval_audit.json", {"recall": rec, "anisotropy": aniso, "rrf": fused})
    return [_c("recall@5 rises with nprobe and is exact at nprobe=all", rec[1] <= rec[4] <= rec[16] == 1.0, rec),
            _c("shifted embeddings are anisotropic (mean cos > 0.8)", aniso > 0.8 and abs(iso) < 0.1, (aniso, iso)),
            _c("RRF(1,3) = 1/61 + 1/63", abs(fused["d1"] - (1 / 61 + 1 / 63)) < 1e-15, fused),
            _c("RRF ranks d2 (ranks 2,1) above d1 (1,3)", fused["d2"] > fused["d1"], fused),
            _c("raw score sum is dominated by the larger-scale leg", raw_sum["d2"] - raw_sum["d1"] > 2, raw_sum)]


# ---------------------------------------------------------------- ADATA-47
def adata_47(work: Path):
    def reconcile(gl, stmt, items):
        adj_bank = stmt + sum(v for k, v in items if k == "deposit_in_transit") - sum(v for k, v in items if k == "outstanding_check")
        var = round(gl - adj_bank, 2)
        return {"adjusted_bank": adj_bank, "variance": var, "status": "reconciled" if var == 0 else "BLOCKED"}

    items = [("outstanding_check", 300.0), ("deposit_in_transit", 500.0), ("outstanding_check", 50.0)]
    ok = reconcile(10_150.0, 10_000.0, items)
    bad = reconcile(10_200.0, 10_000.0, items)
    _w(work, "recon.json", {"cash": ok, "cash_bad": bad, "report_allowed": ok["status"] == "reconciled" and bad["status"] == "reconciled"})
    return [_c("statement 10000 + DIT 500 - checks 350 = GL 10150", ok["adjusted_bank"] == 10_150 and ok["status"] == "reconciled", ok),
            _c("unexplained 50 variance blocks reporting", bad["status"] == "BLOCKED" and bad["variance"] == 50, bad),
            _c("reporting gate closed while any account is open", not (ok["status"] == bad["status"] == "reconciled"), "")]


# ---------------------------------------------------------------- ADATA-48
def adata_48(work: Path):
    conv = [[("system", "be brief"), ("user", "hi"), ("assistant", "hello there")],
            [("user", "2+2?"), ("assistant", "4")], [("user", "name a colour"), ("assistant", "blue")]]

    def template(msgs):
        toks, mask = [], []
        for role, text in msgs:
            seg = [f"<|{role}|>"] + text.split() + ["<|end|>"]
            toks += seg
            mask += [role == "assistant" and t not in (f"<|{role}|>",) for t in seg]
        return toks, mask

    enc = [template(c) for c in conv]
    decoded = [" ".join(t for t, m in zip(tk, mk) if m and t != "<|end|>") for tk, mk in enc]
    L = 16
    padded = sum(L - len(t) for t, _ in enc)
    packs, cur = [], 0
    for t, _ in enc:
        if cur + len(t) > L:
            packs.append(cur)
            cur = 0
        cur += len(t)
    packs.append(cur)
    packed_pad = sum(L - p for p in packs)

    def mix_ok(real, synthetic):
        return real / (real + synthetic) >= 0.25

    card = {k: "..." for k in ("provenance", "license", "method", "template", "filters", "real_fraction", "known_issues")}
    _w(work, "dataset.json", {"decoded_assistant": decoded, "padding_unpacked": padded, "padding_packed": packed_pad, "card": card})
    return [_c("loss mask covers exactly the assistant tokens", decoded == ["hello there", "4", "blue"], decoded),
            _c("packing cuts padding vs one-per-row", packed_pad < padded, (padded, packed_pad)),
            _c("packing changes steps per epoch: 3 rows -> fewer sequences", len(packs) < len(enc), len(packs)),
            _c(">=25% real data rule: 30/70 ok, 20/80 rejected", mix_ok(30, 70) and not mix_ok(20, 80), "")]


# ---------------------------------------------------------------- ADATA-49
def adata_49(work: Path):
    t = np.arange(14 * 24)
    rng = np.random.default_rng(4)
    y = 100 + 20 * np.sin(2 * np.pi * t / 24) + rng.normal(0, 2, len(t))
    y[200] += 25
    y[300] = np.nan  # missing stays missing
    season = np.array([np.nanmedian(y[(t % 24) == h]) for h in range(24)])
    resid = y - season[t % 24]
    med = np.nanmedian(resid)
    mad = np.nanmedian(np.abs(resid - med)) * 1.4826
    score = np.abs(resid - med) / mad
    labels = np.zeros(len(t), bool)
    labels[200] = True

    def f1(th):
        flag = np.nan_to_num(score, nan=0) > th
        tp = (flag & labels).sum()
        return 2 * tp / (flag.sum() + labels.sum()) if flag.sum() else 0

    ths = [2, 3, 4, 5, 6]
    best = max(ths, key=f1)
    flagged = np.where(np.nan_to_num(score) > best)[0].tolist()
    raw_z = np.abs(np.nan_to_num(y, nan=np.nanmean(y)) - np.nanmean(y)) / np.nanstd(y)
    _w(work, "anomalies.json", {"best_threshold": best, "flagged": flagged, "explain": {i: {"value": float(y[i]), "expected": float(season[i % 24])} for i in flagged}})
    return [_c("planted spike at t=200 flagged by seasonal residual + MAD", 200 in flagged, flagged),
            _c("calibrated threshold gives F1 = 1 on the labelled incident", f1(best) == 1.0, best),
            _c("missing value left as NaN, not filled with 0", math.isnan(y[300]) and 300 not in flagged, ""),
            _c("plain z-score without seasonal baseline misses the spike", raw_z[200] < 3, float(raw_z[200]))]


# ---------------------------------------------------------------- ADATA-50
def adata_50(work: Path):
    SECTIONS = ["Task", "Success", "Failure modes", "Assumptions", "Risks and countermeasures", "Verification plan"]

    def premortem(task, success, failures, assumptions, risks, verify, tier="Micro"):
        if not task.strip():
            raise ValueError("empty task")
        if tier not in ("Micro", "Light", "Standard", "Deep"):
            raise ValueError("tier")
        if not re.match(r"(?i)^when .+, then .+", success):
            raise ValueError("success must read 'when X, then Y'")
        if any(re.search(r"could have bugs|might fail|something goes wrong", f, re.I) for f in failures):
            raise ValueError("vague failure mode")
        if not 3 <= len(risks) <= 5 or any(not c for _, c in risks):
            raise ValueError("3-5 risks with countermeasures")
        body = dict(zip(SECTIONS, [task, success, failures, assumptions, risks, verify]))
        return {"tier": tier, **body}

    card = premortem("Migrate invoices table", "when the job finishes, then row counts match source",
                     ["duplicate rows when the job reruns"], ["source has no deletes"],
                     [("timeout", "batch 10k"), ("dupes", "upsert by id"), ("lock", "run off-peak")], "compare counts and sums", tier="Standard")
    _w(work, "premortem.json", card)
    errs = []
    for kw in ({"task": ""}, {"failures": ["it could have bugs"]}, {"success": "it works"}):
        args = dict(task="x", success="when a, then b", failures=["f"], assumptions=[], risks=[("a", "b")] * 3, verify="v")
        args.update(kw)
        try:
            premortem(**args)
            errs.append(None)
        except ValueError as e:
            errs.append(str(e))
    return [_c("card has the 6 listed sections", [k for k in card if k != "tier"] == SECTIONS, list(card)),
            _c("empty task rejected", errs[0] == "empty task", errs[0]),
            _c("'could have bugs' rejected as vague", errs[1] == "vague failure mode", errs[1]),
            _c("success not in 'when ..., then ...' form rejected", errs[2] and "when X" in errs[2], errs[2])]


# ---------------------------------------------------------------- ADATA-51
def adata_51(work: Path):
    def chart_for(n, attr=None):
        if attr:
            return {"defectives_fixed_n": "np", "defectives": "p", "defects_fixed": "c", "defects": "u"}[attr]
        return "I-MR" if n == 1 else "X-bar/R" if n <= 9 else "X-bar/S"

    rng = np.random.default_rng(9)
    sub = rng.normal(10, 0.1, (25, 5))
    xbar, r = sub.mean(1), np.ptp(sub, 1)
    A2, d2 = 0.577, 2.326
    cl, ucl, lcl = xbar.mean(), xbar.mean() + A2 * r.mean(), xbar.mean() - A2 * r.mean()
    new = np.r_[np.full(9, cl + 0.02), [cl + 1.0]]

    def rules(pts):
        sig = []
        if any(p > ucl or p < lcl for p in pts):
            sig.append(1)
        side = np.sign(pts - cl)
        if any(abs(side[i:i + 9].sum()) == 9 for i in range(len(pts) - 8)):
            sig.append(2)
        d = np.sign(np.diff(pts))
        if any(abs(d[i:i + 5].sum()) == 5 for i in range(len(d) - 4)):
            sig.append(3)
        return sig

    trend = cl + np.linspace(-0.05, 0.05, 7)
    sigma = r.mean() / d2
    usl, lsl = 10.5, 9.6
    cp = (usl - lsl) / (6 * sigma)
    cpk = min(usl - cl, cl - lsl) / (3 * sigma)
    _w(work, "spc.json", {"chart": chart_for(5), "limits": [lcl, cl, ucl], "cp": cp, "cpk": cpk, "signals": rules(new)})
    return [_c("chart choice: n=1 I-MR, n=5 X-bar/R, n=12 X-bar/S, defectives p",
               [chart_for(1), chart_for(5), chart_for(12), chart_for(0, "defectives")] == ["I-MR", "X-bar/R", "X-bar/S", "p"], ""),
            _c("limits from 25 subgroups; specs not used as limits", len(sub) == 25 and ucl < usl and lcl > lsl, [lcl, ucl]),
            _c("rule 1 (beyond 3 sigma) and rule 2 (9 on one side) fire on shifted points", rules(new)[:2] == [1, 2], rules(new)),
            _c("rule 3 fires on a steady trend", 3 in rules(trend), rules(trend)),
            _c("off-centre process: Cpk < Cp, both reported", cpk < cp, (round(cp, 2), round(cpk, 2)))]


# ---------------------------------------------------------------- ADATA-52
def adata_52(work: Path):
    from bs4 import BeautifulSoup
    rows = [["id7", "Zed", 120, 100], ["id3", "Amy", 300, 150], ["id9", "Bob", 80, 90]]  # id, name, second_half, first_half
    html = ("<html><body><table><tr><td>1</td><td>Zed</td></tr></table>"
            f"<script id='__NEXT_DATA__' type='application/json'>{json.dumps({'props': {'rows': rows, 'sort': 'name_desc'}})}</script></body></html>")
    _w(work, "page.html", html)
    blob = json.loads(BeautifulSoup(html, "html.parser").find("script", id="__NEXT_DATA__").string)
    recs = [{"id": i, "name": n, "h2": b, "h1": a} for i, n, b, a in blob["props"]["rows"]]  # field order from destructuring
    for r in recs:
        r["total"] = r["h1"] + r["h2"]
        r["velocity"] = (r["h2"] - r["h1"]) / r["h1"] if r["h1"] else None  # halves of the same window
    ranked = sorted(recs, key=lambda r: -r["total"])
    my_rank = {r["id"]: k + 1 for k, r in enumerate(ranked)}
    displayed_rank_zed = 1  # row number under the active sort
    _w(work, "numbers.json", {"by_id": {r["id"]: r for r in recs}, "rank": my_rank, "denominator": len(recs)})
    by = {r["id"]: r for r in recs}
    return [_c("blob found in __NEXT_DATA__ with 3 rows", len(recs) == 3, len(recs)),
            _c("own rank: Amy 1st (450), Zed 2nd (220)", my_rank == {"id3": 1, "id7": 2, "id9": 3}, my_rank),
            _c("displayed '1' for Zed is a row number trap", displayed_rank_zed != my_rank["id7"], "Zed shown 1, real 2 of 3"),
            _c("velocity compares halves: Amy (300-150)/150 = 1.0", by["id3"]["velocity"] == 1.0, by["id3"]),
            _c("matched by stable id, not name", set(by) == {"id7", "id3", "id9"}, "")]


# ---------------------------------------------------------------- ADATA-53
def adata_53(work: Path):
    plan = {"Order Completed": {"order_id": ("string", True), "revenue": ("number", True), "coupon": ("string", False)},
            "Product Viewed": {"product_id": ("string", True)}}
    pii = re.compile(r"(email|phone|name|address)", re.I)
    schemas = {ev: {"type": "object", "required": [k for k, (_, r) in props.items() if r],
                    "properties": {k: {"type": t} for k, (t, _) in props.items()}, "additionalProperties": False}
               for ev, props in plan.items()}
    _w(work, "schemas.json", schemas)
    code = "\n".join(f"def track_{ev.lower().replace(' ', '_')}({', '.join(k for k in props)}): ..." for ev, props in plan.items())
    _w(work, "tracking.py", code)
    pytype = {"string": str, "number": (int, float)}

    def gate(event, payload):
        if event not in schemas:
            return "event not in plan"
        s = schemas[event]
        if any(pii.search(k) for k in payload):
            return "PII in event properties"
        if set(s["required"]) - set(payload):
            return "missing required"
        if set(payload) - set(s["properties"]):
            return "unknown property"
        if any(not isinstance(v, pytype[s["properties"][k]["type"]]) for k, v in payload.items()):
            return "type error"
        return "ok"

    res = {"good": gate("Order Completed", {"order_id": "o1", "revenue": 9.5}), "unplanned": gate("Cart Abandoned", {}),
           "pii": gate("Product Viewed", {"product_id": "p", "email": "a@b"}), "type": gate("Order Completed", {"order_id": "o1", "revenue": "9"}),
           "missing": gate("Order Completed", {"order_id": "o1"})}
    return [_c("valid payload passes the CI schema gate", res["good"] == "ok", res),
            _c("event not in the plan gets no track call", res["unplanned"] == "event not in plan", res["unplanned"]),
            _c("PII in properties rejected (traits only)", res["pii"] == "PII in event properties", res["pii"]),
            _c("string revenue fails typing; missing required fails", res["type"] == "type error" and res["missing"] == "missing required", res),
            _c("typed wrappers generated for both events", code.count("def track_") == 2, code)]


# ---------------------------------------------------------------- ADATA-54
def adata_54(work: Path):
    rng = np.random.default_rng(2)
    items = 50
    log = []
    for day in range(30):  # item popularity drifts over time: future favours higher ids
        pop = np.exp(-np.abs(np.arange(items) - day * 1.5) / 5)
        for u in range(20):
            log.append((day, u, int(rng.choice(items, p=pop / pop.sum()))))
    log.sort()
    cut = int(len(log) * 0.8)
    train_t, test_t = log[:cut], log[cut:]
    idx = rng.permutation(len(log))
    train_r, test_r = [log[i] for i in idx[:cut]], [log[i] for i in idx[cut:]]

    def pop_recall(train, test, k=5):
        top = [i for i, _ in sorted(((i, sum(1 for *_, j in train if j == i)) for i in range(items)), key=lambda t: -t[1])[:k]]
        return float(np.mean([j in top for *_, j in test])), top

    rt, top = pop_recall(train_t, test_t)
    rr, _ = pop_recall(train_r, test_r)

    def ndcg(rel):
        dcg = sum(r / math.log2(i + 2) for i, r in enumerate(rel))
        idcg = sum(r / math.log2(i + 2) for i, r in enumerate(sorted(rel, reverse=True)))
        return dcg / idcg

    coverage = len(set(top)) / items
    _w(work, "recsys_eval.json", {"popularity_recall5_temporal": rt, "popularity_recall5_random": rr, "coverage": coverage})
    return [_c("random split leaks future and inflates recall vs temporal split", rr > rt, (rr, rt)),
            _c("nDCG of an ideal ranking is 1", ndcg([3, 2, 1, 0]) == 1.0, 1.0),
            _c("nDCG of [0,1] = 1/log2(3) / 1 = 0.631", abs(ndcg([0, 1]) - 1 / math.log2(3)) < 1e-12, ndcg([0, 1])),
            _c("catalogue coverage of top-5 popularity = 5/50", coverage == 0.1, coverage)]


# ---------------------------------------------------------------- ADATA-55
def adata_55(work: Path):
    src = '''
def collect(events, metrics):
    for e in events:
        if e["tool"] in ("pytest", "jest"):
            metrics["tests_run"] += 1
        if e["kind"] == "commit":
            metrics["commits"] += 1
    return metrics

def legacy(metrics):
    metrics["deploys"] += 1  # never called
'''
    _w(work, "collector.py", src)
    report = {"tests_run": 0, "commits": 0, "deploys": 0, "reviews": 0}
    my_events = [{"tool": "unittest", "kind": "run"}, {"tool": "git", "kind": "push"}]
    called = set(re.findall(r"^\s+(?:return\s+)?(\w+)\(", src, re.M)) | {"collect"}
    table = []
    for field in report:
        m = re.search(rf"def (\w+)\([^)]*\):(?:(?!\ndef ).)*metrics\[\"{field}\"\] \+=", src, re.S)
        writer = m.group(1) if m else None
        allow = re.findall(r'in \(([^)]*)\)', src) if field == "tests_run" else []
        if writer is None:
            meaning = "no writer: not-applicable/design gap"
        elif writer not in called:
            meaning = "writer unreachable"
        elif allow and not any(e["tool"] in allow[0] for e in my_events):
            meaning = "recogniser gap (hardcoded allowlist)"
        else:
            meaning = "genuine zero"
        table.append({"field": field, "writer": writer, "meaning": meaning})
    _w(work, "zero_provenance.json", table)
    by = {r["field"]: r["meaning"] for r in table}
    return [_c("tests_run 0 is a recogniser gap: unittest not in allowlist", by["tests_run"] == "recogniser gap (hardcoded allowlist)", by),
            _c("commits 0 is genuine (I only pushed)", by["commits"] == "genuine zero", by["commits"]),
            _c("deploys writer exists but is unreachable", by["deploys"] == "writer unreachable", by["deploys"]),
            _c("reviews has no writer at all", by["reviews"].startswith("no writer"), by["reviews"])]


# ---------------------------------------------------------------- ADATA-56
def adata_56(work: Path):
    def classify(c):
        if c.get("consumer_relies_on_producer"):
            return "contract"
        if c.get("rule_known"):
            return "test"
        return "monitor"

    concerns = [{"name": "order_id unique", "rule_known": True}, {"name": "row volume drops", "rule_known": False},
                {"name": "billing feed schema", "consumer_relies_on_producer": True}, {"name": "freshness lag", "rule_known": False, "kind": "freshness"}]
    plan = [(c["name"], classify(c)) for c in concerns]
    order = {"monitor": 0, "contract": 1, "test": 2}
    seq = [n for n, k in sorted(plan, key=lambda t: order[t[1]])]
    inverted = lambda tests, monitors: tests > 50 and monitors == 0
    _w(work, "dq_approach.json", {"plan": plan, "sequence": seq})
    return [_c("known rule -> test, unknown drift -> monitor, producer boundary -> contract",
               dict(plan) == {"order_id unique": "test", "row volume drops": "monitor", "billing feed schema": "contract", "freshness lag": "monitor"}, plan),
            _c("monitors sequenced first, contracts next, tests last", seq[:2] == ["row volume drops", "freshness lag"] and seq[-1] == "order_id unique", seq),
            _c("'200 tests, zero monitors' flagged as inverted", inverted(200, 0) and not inverted(200, 5), "")]


# ---------------------------------------------------------------- ADATA-57
def adata_57(work: Path):
    def engine(ctx):
        if ctx.get("curated_pipeline"):
            return "Nextflow"
        if ctx.get("terra") or ctx.get("gatk_wdl"):
            return "WDL"
        if ctx.get("python_lab"):
            return "Snakemake"
        if ctx.get("cross_institution"):
            return "CWL"
        return "Nextflow"

    picks = {k: engine(v) for k, v in {"rnaseq": {"curated_pipeline": True}, "terra": {"terra": True}, "lab": {"python_lab": True},
                                         "consortium": {"cross_institution": True}}.items()}
    files = {"genome.fa": "GRCh38", "known_sites.vcf": "GRCh38", "intervals.bed": "GRCh37"}

    def build_check(f):
        builds = set(f.values())
        return "ok" if len(builds) == 1 else f"mixed builds: {sorted(builds)}"

    truth = {("chr1", 100, "A", "G"), ("chr1", 200, "C", "T"), ("chr2", 50, "G", "A"), ("chr2", 80, "T", "C")}
    calls = {("chr1", 100, "A", "G"), ("chr1", 200, "C", "T"), ("chr2", 50, "G", "A"), ("chr3", 10, "A", "C")}
    tp = len(truth & calls)
    prec, rec = tp / len(calls), tp / len(truth)
    _w(work, "genomics_plan.json", {"engines": picks, "reference_check": build_check(files), "truth_set": {"precision": prec, "recall": rec}})
    return [_c("engine rules: curated->Nextflow, Terra->WDL, Python lab->Snakemake, portability->CWL",
               picks == {"rnaseq": "Nextflow", "terra": "WDL", "lab": "Snakemake", "consortium": "CWL"}, picks),
            _c("planted GRCh37 interval file flagged: never mix builds", build_check(files).startswith("mixed"), build_check(files)),
            _c("consistent build passes", build_check({"a": "GRCh38", "b": "GRCh38"}) == "ok", ""),
            _c("truth-set validation: precision 0.75, recall 0.75", prec == 0.75 and rec == 0.75, (prec, rec))]


# ---------------------------------------------------------------- ADATA-58
def adata_58(work: Path):
    STEPS = ["understand", "explore", "clean", "split", "features", "baseline", "model", "tune", "evaluate"]

    class Pipeline:
        def __init__(self):
            self.done = []
            self.log = []

        def step(self, name, approval=None, has_dates=False, split_kind=None):
            nxt = STEPS[len(self.done)]
            if name != nxt:
                raise RuntimeError(f"cannot run {name} before {nxt}")
            if self.done and approval not in ("yes", "approved", "go ahead"):
                raise RuntimeError("explicit approval required")
            if name == "split" and has_dates and split_kind != "time":
                raise RuntimeError("time-based split required when dates exist")
            if name == "model" and not any(s == "rationale" for s in self.log):
                raise RuntimeError("record model rationale first")
            self.done.append(name)
            self.log.append(name)

    p = Pipeline()
    errs = {}
    try:
        p.step("model")
    except RuntimeError as e:
        errs["train_first"] = str(e)
    p.step("understand")
    try:
        p.step("explore", approval="hmm")
    except RuntimeError as e:
        errs["hmm"] = str(e)
    p.step("explore", approval="yes")
    p.step("clean", approval="yes")
    try:
        p.step("split", approval="yes", has_dates=True, split_kind="random")
    except RuntimeError as e:
        errs["random_split"] = str(e)
    for s in ["split", "features", "baseline"]:
        p.step(s, approval="yes", has_dates=True, split_kind="time")
    try:
        p.step("model", approval="yes")
    except RuntimeError as e:
        errs["no_rationale"] = str(e)
    p.log.append("rationale")
    p.step("model", approval="yes")
    _w(work, "gates.json", {"done": p.done, "refusals": errs})
    return [_c("training request at step one is refused", errs.get("train_first") == "cannot run model before understand", errs.get("train_first")),
            _c("'hmm' is not a yes", errs.get("hmm") == "explicit approval required", errs.get("hmm")),
            _c("dated data forces a time-based split", "time-based" in errs.get("random_split", ""), errs.get("random_split")),
            _c("model gate needs a recorded rationale", errs.get("no_rationale") == "record model rationale first", errs.get("no_rationale")),
            _c("pipeline reaches model after 6 gated steps", p.done[-1] == "model" and len(p.done) == 7, p.done)]


# ---------------------------------------------------------------- ADATA-59
def adata_59(work: Path):
    def asset(T0, amb, k, n, dt=1.0):
        T, out = T0, []
        for _ in range(n):
            T = T + dt * k * (amb - T)
            out.append(T)
        return np.array(out)

    rng = np.random.default_rng(8)
    signals = {"temp_c": "TwinModel.temperature", "ambient_c": "TwinModel.ambient"}
    real = asset(80, 20, 0.05, 60) + rng.normal(0, 0.2, 60)
    ks = np.linspace(0.01, 0.1, 91)
    k_fit = ks[np.argmin([np.mean((asset(80, 20, k, 40) - real[:40]) ** 2) for k in ks])]
    pred = asset(real[39], 20, k_fit, 20)
    rmse = float(np.sqrt(np.mean((pred - real[40:]) ** 2)))
    drifted = asset(real[39], 20, 0.025, 20)  # fouling halves the cooling rate
    drift_rmse = float(np.sqrt(np.mean((pred - drifted) ** 2)))
    whatif = asset(real[-1], 35, k_fit, 30)[-1]  # from current state, hotter ambient
    _w(work, "twin.json", {"bindings": signals, "k_fit": k_fit, "fidelity_rmse": rmse, "drift_rmse": drift_rmse, "whatif_T": whatif})
    return [_c("calibrated cooling constant k ~ 0.05", abs(k_fit - 0.05) < 0.005, k_fit),
            _c("fidelity on unseen window: RMSE < 0.5 C", rmse < 0.5, rmse),
            _c("drift (k halves) exceeds the fidelity threshold", drift_rmse > 1.0, drift_rmse),
            _c("what-if from current state heads to the new 35 C ambient", real[-1] < whatif < 35, whatif),
            _c("every signal bound to a model property", all(signals.values()), signals)]


# ---------------------------------------------------------------- ADATA-60
def adata_60(work: Path):
    from bs4 import BeautifulSoup
    pages = {
        "a": '<script type="application/ld+json">{"@type":"Product","name":"Lamp","offers":{"price":"1.299,00","priceCurrency":"EUR"},"releaseDate":"03/02/2026"}</script>',
        "b": '<div itemscope itemtype="https://schema.org/Product"><span itemprop="name">Desk</span><meta itemprop="price" content="45.5">'
             '<meta itemprop="priceCurrency" content="USD"><meta itemprop="releaseDate" content="2026-02-04"></div>',
        "c": '<div data-testid="title">Chair</div><span data-testid="price">SAR 120</span><time datetime="2026-02-05"></time>',
        "d": '<div class="x9f">broken</div>'}
    schema = {"name": str, "price": float, "currency": str, "date": str}

    def money(s):
        s = re.sub(r"[^\d,.]", "", s)
        if re.search(r",\d{2}$", s):
            s = s.replace(".", "").replace(",", ".")
        return float(s.replace(",", ""))

    def iso(d):
        m = re.fullmatch(r"(\d\d)/(\d\d)/(\d{4})", d)
        return f"{m[3]}-{m[2]}-{m[1]}" if m else d

    def extract(html):
        soup = BeautifulSoup(html, "html.parser")
        ld = soup.find("script", type="application/ld+json")
        if ld:
            j = json.loads(ld.string)
            return {"name": j["name"], "price": money(j["offers"]["price"]), "currency": j["offers"]["priceCurrency"], "date": iso(j["releaseDate"])}, "json-ld"
        md = soup.find(attrs={"itemscope": True})
        if md:
            g = lambda p: (lambda t: t.get("content") or t.get_text())(md.find(attrs={"itemprop": p}))
            return {"name": g("name"), "price": money(g("price")), "currency": g("priceCurrency"), "date": iso(g("releaseDate"))}, "microdata"
        t, p, d = soup.find(attrs={"data-testid": "title"}), soup.find(attrs={"data-testid": "price"}), soup.find("time")
        if t and p:
            return {"name": t.get_text(), "price": money(p.get_text()), "currency": re.match(r"[A-Z]{3}", p.get_text())[0], "date": d["datetime"]}, "selector"
        return None, "none"

    out, broken = {}, []
    for k, h in pages.items():
        rec, via = extract(h)
        if rec is None or any(not isinstance(rec.get(f), t) for f, t in schema.items()):
            broken.append(k)
            continue
        out[k] = {**rec, "via": via}
    _w(work, "records.json", {"records": out, "broken": broken})
    return [_c("fallback chain: JSON-LD, microdata, then stable data-testid selector",
               [out[k]["via"] for k in "abc"] == ["json-ld", "microdata", "selector"], [out[k]["via"] for k in "abc"]),
            _c("'1.299,00' EUR normalised to 1299.0", out["a"]["price"] == 1299.0 and out["a"]["currency"] == "EUR", out["a"]),
            _c("03/02/2026 normalised to ISO 2026-02-03", out["a"]["date"] == "2026-02-03", out["a"]["date"]),
            _c("page with only generated classes reported broken, not guessed", broken == ["d"], broken)]


# ---------------------------------------------------------------- ADATA-61
def adata_61(work: Path):
    def choose(w):
        if w["latency_s"] < 60:
            return "streaming (Kafka/Flink), not orchestration"
        if w.get("long_running_stateful"):
            return "Temporal"
        if w.get("asset_centric"):
            return "Dagster"
        if w.get("dags", 0) > 200 and w.get("ops_team"):
            return "Airflow"
        if w.get("notebook_team"):
            return "Mage"
        if w.get("dynamic_python"):
            return "Prefect"
        return "cron / managed scheduler"

    cases = {"clickstream": {"latency_s": 5}, "lineage": {"latency_s": 3600, "asset_centric": True},
             "estate": {"latency_s": 3600, "dags": 800, "ops_team": True}, "flows": {"latency_s": 900, "dynamic_python": True},
             "nb": {"latency_s": 86400, "notebook_team": True}, "orders": {"latency_s": 600, "long_running_stateful": True},
             "nightly": {"latency_s": 86400}}
    picks = {k: choose(v) for k, v in cases.items()}
    _w(work, "orchestrator.json", picks)
    return [_c("sub-minute need gated out to streaming first", picks["clickstream"].startswith("streaming"), picks["clickstream"]),
            _c("asset/lineage -> Dagster, big DAG estate with ops -> Airflow", picks["lineage"] == "Dagster" and picks["estate"] == "Airflow", picks),
            _c("dynamic Python -> Prefect, notebook -> Mage, stateful -> Temporal",
               (picks["flows"], picks["nb"], picks["orders"]) == ("Prefect", "Mage", "Temporal"), picks),
            _c("no special need -> minimal scheduler", picks["nightly"] == "cron / managed scheduler", picks["nightly"])]


# ---------------------------------------------------------------- ADATA-62
def adata_62(work: Path):
    verbs = {"Viewed", "Completed", "Started", "Added", "Signed Up"}
    events = ["Order Completed", "Product Viewed Shoes", "Product Viewed Hats", "checkout_started", "Cart Added"]
    issues, merged = [], {}
    for e in events:
        m = re.fullmatch(r"([A-Z][a-z]+) (Viewed|Completed|Started|Added|Signed Up)(?: (.+))?", e)
        if not m:
            issues.append((e, "not Object Action in Title Case"))
            continue
        base = f"{m[1]} {m[2]}"
        if m[3]:
            merged.setdefault(base, []).append(m[3].lower())
        else:
            merged.setdefault(base, [])
    plan = {ev: ({"category": {"type": "string", "required": True, "values": v}} if v else {}) for ev, v in merged.items()}
    identity = {"anonymous_id": "uuid v4 in first-party cookie", "user_id": "db users.id", "merge": "alias at sign-up/login",
                "graph": "CDP"}
    _w(work, "tracking_plan.json", {"events": plan, "identity": identity, "issues": issues, "verbs": sorted(verbs)})
    return [_c("variants collapsed into Product Viewed with a category property",
               plan.get("Product Viewed", {}).get("category", {}).get("values") == ["shoes", "hats"], plan.get("Product Viewed")),
            _c("snake_case event rejected", issues == [("checkout_started", "not Object Action in Title Case")], issues),
            _c("3 canonical events remain", sorted(plan) == ["Cart Added", "Order Completed", "Product Viewed"], sorted(plan)),
            _c("identity model defined before finalising (4 parts)", len(identity) == 4, identity)]


PROGRAMS = {f"ADATA-{n:02d}": globals()[f"adata_{n:02d}"]
            for n in range(1, 63) if f"adata_{n:02d}" in globals()}
