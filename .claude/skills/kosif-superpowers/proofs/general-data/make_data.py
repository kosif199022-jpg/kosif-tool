#!/usr/bin/env python3
"""general-data proof: generate a CSV, analyse it with pandas AND duckdb, reconcile control
totals three ways, chart it with matplotlib (Arabic labels), solve exact maths with sympy,
optimise/test with scipy, and emit an RTL HTML dashboard for a headless-browser screenshot.

Usage:  python -I make_data.py <workdir>      then: node snap.cjs <workdir>/dashboard.html <out.png>
Needs:  numpy pandas duckdb matplotlib sympy scipy arabic-reshaper python-bidi
Writes: <workdir>/sales.csv, sales.parquet, dashboard.html; chart.png, mpl_arabic_modes.png, results.json next to this script.
The data are SYNTHETIC (seeded random), labelled as such on every output.
"""
from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "_shared" / "fonts"
W = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/general-data").resolve()
W.mkdir(parents=True, exist_ok=True)
R: dict = {"workdir": str(W), "checks": [], "numbers": {}, "timings_s": {}}


def check(name, ok, detail=""):
    R["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""))


# ------------------------------------------------------------ 1. synthetic CSV (seeded)
REGIONS = ["القاهرة", "الرياض", "دبي", "عمّان", "الدار البيضاء"]
CHANNELS = ["online", "store", "partner"]
rng = np.random.default_rng(7)
rows = []
for m in range(1, 13):
    for ri, reg in enumerate(REGIONS):
        for ch in CHANNELS:
            orders = int(rng.integers(40, 160) * (1 + 0.04 * m) * (1.6 - 0.15 * ri))
            price = int(rng.integers(90, 130))
            revenue = orders * price  # integer currency units: no float drift in totals
            cost = int(revenue * rng.uniform(0.55, 0.75))
            rows.append({"month": f"2026-{m:02d}", "region": reg, "channel": ch, "orders": orders, "revenue": revenue, "cost": cost})
CSV = W / "sales.csv"
with CSV.open("w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig: Excel opens Arabic correctly
    wr = csv.DictWriter(f, fieldnames=list(rows[0]))
    wr.writeheader()
    wr.writerows(rows)
EXPECTED_ROWS = 12 * len(REGIONS) * len(CHANNELS)

# control total #1: plain csv module (no pandas, no SQL)
with CSV.open(encoding="utf-8-sig") as f:
    raw = list(csv.DictReader(f))
ct_raw = sum(int(r["revenue"]) for r in raw)
check("csv: expected row count", len(raw) == EXPECTED_ROWS, f"{len(raw)} rows")

# ------------------------------------------------------------ 2. pandas
import pandas as pd

t0 = time.time()
df = pd.read_csv(CSV, encoding="utf-8-sig")
df["margin"] = df["revenue"] - df["cost"]
by_region = df.groupby("region", sort=False)[["orders", "revenue", "margin"]].sum().sort_values("revenue", ascending=False)
monthly = df.groupby("month")["revenue"].sum()
pivot = df.pivot_table(index="month", columns="channel", values="revenue", aggfunc="sum")
ct_pd = int(df["revenue"].sum())
R["timings_s"]["pandas"] = round(time.time() - t0, 3)
check("pandas: groupby + pivot built", pivot.shape == (12, 3) and len(by_region) == 5, f"top region {by_region.index[0]} = {int(by_region.revenue.iloc[0]):,}")

# ------------------------------------------------------------ 3. duckdb: SQL straight on the CSV file
import duckdb

t0 = time.time()
con = duckdb.connect()
q = f"""
WITH m AS (                       -- named CTE, explicit columns (no SELECT *)
  SELECT month, region, SUM(revenue) AS rev, SUM(revenue - cost) AS margin
  FROM read_csv('{CSV}', header = true)
  GROUP BY month, region
)
SELECT month, region, rev, margin,
       rev - LAG(rev) OVER (PARTITION BY region ORDER BY month)                    AS mom_change,
       RANK() OVER (PARTITION BY month ORDER BY rev DESC)                          AS rank_in_month,
       ROUND(100.0 * margin / NULLIF(rev, 0), 1)                                   AS margin_pct  -- zero guard
FROM m ORDER BY month, rank_in_month
"""
res = con.sql(q).df()
ct_duck = int(con.sql(f"SELECT SUM(revenue) FROM read_csv('{CSV}', header = true)").fetchone()[0])
winners = res[res.rank_in_month == 1].region.value_counts().to_dict()
con.sql(f"COPY (SELECT month, region, channel, orders, revenue, cost FROM read_csv('{CSV}', header = true)) TO '{W / 'sales.parquet'}' (FORMAT parquet)")
pq_rows = con.sql(f"SELECT COUNT(*) FROM '{W / 'sales.parquet'}'").fetchone()[0]
R["timings_s"]["duckdb"] = round(time.time() - t0, 3)
check("duckdb: CTE + LAG + RANK window query on raw CSV", len(res) == 60 and res.mom_change.isna().sum() == 5, f"month-winners {winners}")
check("duckdb: COPY to Parquet and count back", pq_rows == EXPECTED_ROWS, f"{pq_rows} rows, {(W / 'sales.parquet').stat().st_size} B")

# ------------------------------------------------------------ 4. reconcile control totals 3 ways
check("control total: csv module == pandas == duckdb", ct_raw == ct_pd == ct_duck, f"{ct_raw:,}")
check("control total: region subtotals add back to grand total", int(by_region.revenue.sum()) == ct_raw and int(res.rev.sum()) == ct_raw)
R["numbers"].update(total_revenue=ct_raw, total_margin=int(df.margin.sum()), top_region=by_region.index[0],
                    margin_pct=round(100 * df.margin.sum() / df.revenue.sum(), 2))

# ------------------------------------------------------------ 5. scipy: trend, test, optimisation
from scipy import optimize, stats

x = np.arange(1, 13)
lr = stats.linregress(x, monthly.values)
a = df[df.region == REGIONS[0]].groupby("month").revenue.sum().values
b = df[df.region == REGIONS[3]].groupby("month").revenue.sum().values
tt = stats.ttest_ind(a, b, equal_var=False)  # Welch: does not assume equal variances
# product mix LP: max 40x + 30y  s.t. x + y <= 40, 2x + y <= 60, x,y >= 0  (linprog minimises -> negate)
lp = optimize.linprog(c=[-40, -30], A_ub=[[1, 1], [2, 1]], b_ub=[40, 60], bounds=[(0, None)] * 2, method="highs")
check("scipy.stats.linregress: monthly trend", lr.slope > 0, f"slope {lr.slope:,.0f}/month, r^2 {lr.rvalue**2:.3f}")
check("scipy.stats.ttest_ind (Welch) between two regions", tt.pvalue < 0.05, f"t={tt.statistic:.2f}, p={tt.pvalue:.2e}")
check("scipy.optimize.linprog (HiGHS) product mix", lp.status == 0 and np.allclose(lp.x, [20, 20]) and round(-lp.fun) == 1400, f"x={lp.x.tolist()}, profit={-lp.fun:.0f}")
R["numbers"].update(trend_slope=round(lr.slope, 1), trend_r2=round(lr.rvalue**2, 4), welch_p=float(f"{tt.pvalue:.3e}"), lp_x=lp.x.tolist(), lp_profit=-lp.fun)

# ------------------------------------------------------------ 6. sympy: exact answers, not mental arithmetic
import sympy as sp

Q, p = sp.symbols("Q p", positive=True)
F, price, var = 120_000, 50, 30
be = sp.solve(sp.Eq(price * Q - var * Q - F, 0), Q)
profit = (p - 20) * (1000 - 10 * p)  # demand q = 1000 - 10p, unit cost 20
p_star = sp.solve(sp.diff(profit, p), p)
second = sp.diff(profit, p, 2)
xs = sp.symbols("x")
integral = sp.integrate(sp.exp(-xs**2), (xs, -sp.oo, sp.oo))
check("sympy: break-even units solved exactly", be == [6000], f"Q = {be}")
check("sympy: profit-max price via derivative, 2nd derivative < 0", p_star == [60] and second < 0, f"p* = {p_star}, profit* = {profit.subs(p, 60)}, f'' = {second}")
check("sympy: exact Gaussian integral", integral == sp.sqrt(sp.pi), f"{integral}")
check("sympy cross-checks scipy LP vertex exactly", sp.solve([xs + Q - 40, 2 * xs + Q - 60], [xs, Q]) == {xs: 20, Q: 20})
R["numbers"].update(break_even=int(be[0]), p_star=int(p_star[0]), profit_star=int(profit.subs(p, 60)))

# ------------------------------------------------------------ 7. matplotlib chart with Arabic text
import matplotlib

matplotlib.use("Agg")
import arabic_reshaper
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from matplotlib import font_manager

for fnt in ("Tajawal-Bold.ttf", "Amiri-Regular.ttf"):
    font_manager.fontManager.addfont(str(FONTS / fnt))
plt.rcParams.update({"font.family": ["Tajawal", "DejaVu Sans"], "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8a8984", "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e"})


import logging
import matplotlib.ft2font as ft2font

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # Tajawal ships Bold only
RAQM = getattr(ft2font, "__libraqm_version__", None)  # matplotlib >= 3.11 wheels bundle libraqm


def ar(s: str) -> str:
    """matplotlib with libraqm shapes + orders Arabic itself: pass the RAW string.
    Older builds (no libraqm) need arabic_reshaper + python-bidi. Doing both = reversed, broken text."""
    return s if RAQM else get_display(arabic_reshaper.reshape(s))


check("matplotlib: bundles libraqm -> raw Arabic strings shape correctly (reshaper+bidi would now REVERSE them)", RAQM is not None, f"libraqm {RAQM}")


SERIES, SURF, INK, MUTED = "#2a78d6", "#fcfcfb", "#0b0b0b", "#52514e"
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6), dpi=110, facecolor=SURF)
for ax in (ax1, ax2):
    ax.set_facecolor(SURF)
    ax.grid(axis="y", color="#e6e5e0", linewidth=0.8)
    ax.set_axisbelow(True)
vals = by_region.revenue.values / 1e6
ax1.bar([ar(r) for r in by_region.index], vals, color=SERIES, width=0.6)
for i, v in enumerate(vals):
    ax1.text(i, v + 0.03, f"{v:.2f}", ha="center", va="bottom", color=INK, fontsize=10)
ax1.set_title(ar("الإيرادات حسب المدينة (مليون)"), color=INK, fontsize=14, loc="right")
months = [m[-2:] for m in monthly.index]
ax2.plot(months, monthly.values / 1e6, color=SERIES, linewidth=2, marker="o", markersize=5)
ax2.plot(months, (lr.intercept + lr.slope * x) / 1e6, color=MUTED, linewidth=1.2, linestyle="--")
ax2.annotate(ar("اتجاه خطي") + f"  r²={lr.rvalue**2:.2f}", xy=(11, (lr.intercept + lr.slope * 12) / 1e6), xytext=(6.5, monthly.values.min() / 1e6),
             color=MUTED, fontsize=10, arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})
ax2.set_title(ar("الإيراد الشهري 2026 (مليون)"), color=INK, fontsize=14, loc="right")
ax2.set_xlabel(ar("الشهر"))
fig.text(0.01, 0.01, "Synthetic data (seed 7) - generated by make_data.py", color=MUTED, fontsize=8, family="DejaVu Sans")
fig.tight_layout(rect=(0, 0.03, 1, 1))
CHART = HERE / "chart.png"
fig.savefig(CHART, facecolor=SURF)
check("matplotlib: Arabic chart saved < 300 KB", CHART.stat().st_size < 300_000, f"{CHART.stat().st_size} B")

# side-by-side evidence: raw string vs the old reshaper+bidi recipe on a libraqm build
fig2, ax = plt.subplots(figsize=(7, 1.9), dpi=100, facecolor="white")
ax.axis("off")
demo = "الإيرادات حسب المدينة"
ax.text(0.98, 0.70, demo, ha="right", fontsize=18, color=INK)
ax.text(0.98, 0.18, get_display(arabic_reshaper.reshape(demo)), ha="right", fontsize=18, color="#b00020")
ax.text(0.02, 0.70, "raw string (correct)", fontsize=9, color=MUTED, family="DejaVu Sans")
ax.text(0.02, 0.18, "reshaper+bidi (now reversed)", fontsize=9, color="#b00020", family="DejaVu Sans")
fig2.savefig(HERE / "mpl_arabic_modes.png")

# ------------------------------------------------------------ 7b. Monte Carlo on uncertain assumptions (seeded)
mc = np.random.default_rng(11)
N = 100_000
units = mc.normal(7000, 1200, N)            # demand uncertainty
price_mc = mc.triangular(44, 50, 54, N)     # price pressure skewed down
var_mc = mc.uniform(28, 33, N)              # unit cost range
profit_mc = units * (price_mc - var_mc) - F
p_loss = float((profit_mc < 0).mean())
p5, p50, p95 = np.percentile(profit_mc, [5, 50, 95])
check("Monte Carlo (100k seeded draws): probability of loss and P5/P50/P95 profit", 0 < p_loss < 1, f"P(loss)={p_loss:.3f}, P5={p5:,.0f}, P50={p50:,.0f}, P95={p95:,.0f}")
R["numbers"].update(mc_p_loss=round(p_loss, 4), mc_p5=round(p5), mc_p50=round(p50), mc_p95=round(p95))

# ------------------------------------------------------------ 8. RTL HTML dashboard (no external libs) for screenshot
max_v = by_region.revenue.max()
bars = "".join(
    f'<g><title>{reg}: {int(v):,}</title><rect x="{40 + i * 64}" y="{200 - 170 * v / max_v:.1f}" width="44" height="{170 * v / max_v:.1f}" rx="4" fill="var(--series-1)"/>'
    f'<text x="{62 + i * 64}" y="222" text-anchor="middle" class="lab">{reg}</text></g>'
    for i, (reg, v) in enumerate(by_region.revenue.items()))
table = "".join(f"<tr><td>{reg}</td><td>{int(r.revenue):,}</td><td>{100 * r.margin / r.revenue:.1f}%</td></tr>" for reg, r in by_region.iterrows())
html = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sales Dashboard</title><style>
@font-face {{ font-family: Tajawal; src: url('{(FONTS / 'Tajawal-Bold.ttf').as_uri()}'); }}
:root {{ --surface:#fcfcfb; --card:#ffffff; --ink:#0b0b0b; --muted:#52514e; --line:#e6e5e0; --series-1:#2a78d6; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --surface:#1a1a19; --card:#232322; --ink:#f0efec; --muted:#c3c2b7; --line:#3a3a38; --series-1:#3987e5; }} }}
:root[data-theme="dark"] {{ --surface:#1a1a19; --card:#232322; --ink:#f0efec; --muted:#c3c2b7; --line:#3a3a38; --series-1:#3987e5; }}
* {{ box-sizing: border-box; }} body {{ margin:0; padding:16px; background:var(--surface); color:var(--ink); font-family:Tajawal, system-ui, sans-serif; }}
h1 {{ font-size:22px; margin:0 0 4px; }} .note {{ color:var(--muted); font-size:13px; margin:0 0 16px; }}
.tiles {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:16px; }}
.tile {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px 14px; }}
.tile b {{ display:block; font-size:24px; font-variant-numeric:tabular-nums; }} .tile span {{ color:var(--muted); font-size:13px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px; margin-bottom:16px; overflow-x:auto; }}
svg {{ width:100%; max-width:420px; height:auto; display:block; }} .lab {{ fill:var(--muted); font-size:11px; }}
table {{ width:100%; border-collapse:collapse; font-variant-numeric:tabular-nums; }} td, th {{ padding:6px 8px; border-bottom:1px solid var(--line); text-align:right; }}
</style></head><body>
<h1>لوحة المبيعات ٢٠٢٦</h1><p class="note">بيانات اصطناعية للاختبار (seed 7) · المصدر: sales.csv · المجاميع مطابقة بثلاث طرق</p>
<div class="tiles"><div class="tile"><span>إجمالي الإيراد</span><b>{ct_raw:,}</b></div>
<div class="tile"><span>هامش الربح</span><b>{R['numbers']['margin_pct']}%</b></div>
<div class="tile"><span>أعلى مدينة</span><b>{by_region.index[0]}</b></div></div>
<div class="card"><svg viewBox="0 0 360 230" role="img" aria-label="الإيراد حسب المدينة"><line x1="30" y1="200" x2="350" y2="200" stroke="var(--line)"/>{bars}</svg></div>
<div class="card"><table><tr><th>المدينة</th><th>الإيراد</th><th>الهامش</th></tr>{table}</table></div>
</body></html>"""
(W / "dashboard.html").write_text(html, encoding="utf-8")
check("dashboard.html written (RTL, tokens, dark mode, inline SVG, table view)", (W / "dashboard.html").stat().st_size < 20_000, f"{(W / 'dashboard.html').stat().st_size} B")

from importlib.metadata import version as v
R["versions"] = {k: v(k) for k in ("numpy", "pandas", "duckdb", "scipy", "sympy", "matplotlib", "arabic-reshaper", "python-bidi")}
R["summary"] = f"{sum(c['ok'] for c in R['checks'])}/{len(R['checks'])} checks passed"
print(R["summary"])
(HERE / "results.json").write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
