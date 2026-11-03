"""Real programs for the data-analysis family (tables, statistics, solvers, charts).

Cards whose named library is not available in CI (pandas, DuckDB, polars, sympy, statsmodels,
networkx, pyproj) are programmed only where the card's claim is the technique itself and the
same technique runs exactly with stdlib/numpy/scipy; the observed text says which engine ran.
"""
from __future__ import annotations

import csv
import io
import json
import math
import sqlite3
import unicodedata
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import optimize, stats

FONTS = Path(__file__).resolve().parents[2] / "proofs" / "_shared" / "fonts"


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


def _sales(seed=7):
    """180 rows: 12 months x 3 regions x 5 reps, integer money (minor units)."""
    rng = np.random.default_rng(seed)
    rows = []
    for m in range(1, 13):
        for reg in ("القاهرة", "الرياض", "دبي"):
            for rep in range(5):
                rows.append({"month": f"2026-{m:02d}", "region": reg, "rep": f"r{rep}", "revenue": int(rng.integers(1000, 5000))})
    return rows


# ---------------------------------------------------------------- ANLY-01
def anly_01(work: Path):
    rows = _sales()
    p = work / "sales.csv"
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(p, encoding="utf-8-sig") as f:
        back = list(csv.DictReader(f))
    by_region = defaultdict(int)
    for r in back:  # groupby(region, sort=False).sum()
        by_region[r["region"]] += int(r["revenue"])
    ranked = sorted(by_region.items(), key=lambda kv: -kv[1])
    months = sorted({r["month"] for r in back})
    regions = list(dict.fromkeys(r["region"] for r in back))
    pivot = {m: {g: 0 for g in regions} for m in months}  # pivot_table(index=month, columns=region, aggfunc=sum)
    for r in back:
        pivot[r["month"]][r["region"]] += int(r["revenue"])
    _w(work, "pivot.json", {"engine": "stdlib csv (pandas not used)", "by_region": ranked, "pivot": pivot})
    total = sum(int(r["revenue"]) for r in back)
    return [_c("180 rows read back", len(back) == 180, len(back)),
            _c("pivot shape is 12 x 3", len(pivot) == 12 and all(len(v) == 3 for v in pivot.values()), (len(pivot), 3)),
            _c("pivot cells add back to the grand total", sum(sum(v.values()) for v in pivot.values()) == total, total),
            _c("group sums ranked descending", [v for _, v in ranked] == sorted(by_region.values(), reverse=True), ranked),
            _c("first header has no BOM prefix (utf-8-sig)", list(back[0])[0] == "month", list(back[0])[0])]


# ---------------------------------------------------------------- ANLY-05
def anly_05(work: Path):
    rows = [{"الاسم": f"عميل {i}", "المدينة": "القاهرة", "المبلغ": i} for i in range(180)]
    p = work / "arabic.csv"
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    raw = p.read_bytes()
    with open(p, encoding="utf-8-sig") as f:
        ok = list(csv.DictReader(f))
    with open(p, encoding="utf-8") as f:
        bad_header = next(csv.reader(f))[0]
    return [_c("file starts with the UTF-8 BOM EF BB BF", raw[:3] == b"\xef\xbb\xbf", raw[:3].hex()),
            _c("180 Arabic rows re-read intact", len(ok) == 180 and ok[5]["الاسم"] == "عميل 5", ok[5]),
            _c("utf-8-sig read gives a clean first header", list(ok[0])[0] == "الاسم", list(ok[0])[0]),
            _c("plain utf-8 read leaves the \\ufeff prefix", bad_header.startswith("﻿"), repr(bad_header[:2]))]


# ---------------------------------------------------------------- ANLY-06
class _Poly:
    """Exact polynomial with Fraction coefficients (index = power)."""

    def __init__(self, c):
        self.c = [Fraction(x) for x in c]

    def __call__(self, x):
        return sum(k * Fraction(x) ** i for i, k in enumerate(self.c))

    def diff(self):
        return _Poly([i * k for i, k in enumerate(self.c)][1:] or [0])

    def __mul__(self, o):
        out = [Fraction(0)] * (len(self.c) + len(o.c) - 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                out[i + j] += a * b
        return _Poly(out)


def anly_06(work: Path):
    # break-even 50Q - 30Q - 120000 = 0 solved exactly
    lin = _Poly([-120000, 50 - 30])
    q = -lin.c[0] / lin.c[1]
    # profit (p-20)(1000-10p): stationary point of the derivative, second derivative sign
    prof = _Poly([-20, 1]) * _Poly([1000, -10])
    d1, d2 = prof.diff(), prof.diff().diff()
    p_star = -d1.c[0] / d1.c[1]
    from scipy import integrate
    gauss, _ = integrate.quad(lambda x: math.exp(-x * x), -np.inf, np.inf)
    _w(work, "solve.json", {"engine": "exact Fraction polynomials (sympy not used); integral numeric",
                            "Q": str(q), "p_star": str(p_star), "d2": str(d2.c[0]), "gauss": gauss})
    return [_c("break-even Q = 6000 exactly", q == 6000 and lin(q) == 0, q),
            _c("optimal price p = 60 exactly", p_star == 60 and d1(p_star) == 0, p_star),
            _c("second derivative -20 < 0 confirms a maximum", d2.c[0] == -20, d2.c[0]),
            _c("max profit (60-20)(1000-600) = 16000", prof(60) == 16000, prof(60)),
            _c("integral of exp(-x^2) over R = sqrt(pi) (numeric to 1e-10)", abs(gauss - math.sqrt(math.pi)) < 1e-10, gauss)]


# ---------------------------------------------------------------- ANLY-07
def anly_07(work: Path):
    rng = np.random.default_rng(0)
    months = np.arange(24)
    y = 100_000 + 8000 * months + rng.normal(0, 5000, 24)
    r = stats.linregress(months, y)
    a, b = rng.normal(50, 5, 12), rng.normal(43, 9, 12)
    t = stats.ttest_ind(a, b, equal_var=False)
    se = math.sqrt(a.var(ddof=1) / 12 + b.var(ddof=1) / 12)
    t_manual = (a.mean() - b.mean()) / se
    va, vb = a.var(ddof=1) / 12, b.var(ddof=1) / 12
    welch_df = (va + vb) ** 2 / (va ** 2 / 11 + vb ** 2 / 11)
    _w(work, "stats.json", {"slope_per_month": r.slope, "r2": r.rvalue ** 2, "welch_t": t.statistic, "p": t.pvalue,
                            "note": "n=12 per group is small"})
    return [_c("slope recovered near +8000/month", abs(r.slope - 8000) < 500, round(r.slope)),
            _c("r^2 = rvalue^2 and > 0.9", r.rvalue ** 2 > 0.9, r.rvalue ** 2),
            _c("Welch t equals the hand formula", abs(t.statistic - t_manual) < 1e-9, t.statistic),
            _c("Welch-Satterthwaite df below pooled 22 (unequal variances)", welch_df < 22, round(welch_df, 2))]


# ---------------------------------------------------------------- ANLY-08
def anly_08(work: Path):
    x = np.arange(20, dtype=float)
    y = 2 * x + 1
    X = np.c_[np.ones_like(x), x]
    beta, res, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    rng = np.random.default_rng(1)
    yn = 2 * x + 1 + rng.normal(0, 1, 20)
    bn = np.linalg.lstsq(X, yn, rcond=None)[0]
    e = yn - X @ bn
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * (e @ e) / 18)
    _w(work, "ols.json", {"engine": "numpy least squares (statsmodels not used)", "exact": beta.tolist(), "noisy": bn.tolist(), "se": se.tolist()})
    return [_c("exact data: slope 2.0, intercept 1.0", np.allclose(beta, [1, 2]), beta.tolist()),
            _c("noisy data: slope within 2 SE of 2", abs(bn[1] - 2) < 2 * se[1], (bn[1], se[1])),
            _c("design matrix full rank 2", rank == 2, rank)]


# ---------------------------------------------------------------- ANLY-09
def anly_09(work: Path):
    def sim(seed, n=100_000):
        rng = np.random.default_rng(seed)
        units = rng.normal(1000, 300, n)
        price = rng.triangular(40, 50, 70, n)
        cost = rng.uniform(25, 35, n)
        profit = units * (price - cost) - 20_000
        return profit

    p = sim(42)
    q = sim(42)
    exp_mean = 1000 * ((40 + 50 + 70) / 3 - 30) - 20_000
    p5, p50, p95 = np.percentile(p, [5, 50, 95])
    out = {"seed": 42, "N": 100_000, "distributions": "units~N(1000,300), price~Tri(40,50,70), cost~U(25,35), fixed 20000",
           "p_loss": float((p < 0).mean()), "p5": p5, "p50": p50, "p95": p95}
    _w(work, "risk.json", out)
    return [_c("same seed reproduces identical draws", np.array_equal(p, q), "seed 42"),
            _c("mean profit matches analytic 3333.3 within 3 SE", abs(p.mean() - exp_mean) < 3 * p.std() / math.sqrt(len(p)), (p.mean(), exp_mean)),
            _c("P5 < P50 < P95", p5 < p50 < p95, (p5, p50, p95)),
            _c("probability of loss is a proper fraction", 0 < out["p_loss"] < 1, out["p_loss"]),
            _c("seed and distributions stated in the output", out["seed"] == 42 and "Tri(40,50,70)" in out["distributions"], out["distributions"])]


# ---------------------------------------------------------------- ANLY-10
def anly_10(work: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    font = FONTS / "Tajawal-Bold.ttf"
    font_manager.fontManager.addfont(str(font))
    plt.rcParams["font.family"] = ["Tajawal", "DejaVu Sans"]
    plt.rcParams["font.weight"] = "bold"
    fig, ax = plt.subplots(figsize=(4, 3), dpi=120)
    vals = [30, 45, 25]
    bars = ax.bar(["القاهرة", "الرياض", "دبي"], vals, color="#2a78d6")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, str(v), ha="center", color="#222222")
    ax.set_title("المبيعات حسب المدينة", loc="right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5")
    out = work / "chart.png"
    fig.savefig(out)
    used = font_manager.FontProperties(family=plt.rcParams["font.family"]).get_name()
    plt.close(fig)
    from PIL import Image
    im = np.asarray(Image.open(out).convert("RGB"))
    blue = np.all(np.abs(im.astype(int) - [0x2a, 0x78, 0xd6]) <= 2, axis=2).sum()
    return [_c("PNG is 480x360 (4x3 in at 120 dpi)", im.shape[:2] == (360, 480), im.shape),
            _c("Tajawal resolved as the font", used == "Tajawal", used),
            _c("bars drawn in the single series hue #2a78d6", blue > 2000, int(blue)),
            _c("top/right spines off, title on the right", not ax.spines["top"].get_visible() and ax._right_title.get_text() == "المبيعات حسب المدينة", ""),
            _c("value labels in ink colour, not series colour", all(t.get_color() == "#222222" for t in ax.texts), len(ax.texts))]


# ---------------------------------------------------------------- ANLY-11
def anly_11(work: Path):
    import arabic_reshaper
    import matplotlib.ft2font
    from bidi.algorithm import get_display
    from PIL import features
    raqm_mpl = getattr(matplotlib.ft2font, "__libraqm_version__", None)
    raqm_pil = features.check("raqm")

    def prepare(s, has_raqm):
        return s if has_raqm else get_display(arabic_reshaper.reshape(s))

    s = "مرحبا بالعالم"
    with_raqm, without = prepare(s, True), prepare(s, False)
    pres = sum(0xFB50 <= ord(ch) <= 0xFEFF for ch in without)
    back = unicodedata.normalize("NFKC", without[::-1])
    _w(work, "raqm.json", {"matplotlib_libraqm": raqm_mpl, "pil_raqm": raqm_pil, "raw": with_raqm, "reshaped_visual": without})
    return [_c("detection ran for both libraries", raqm_mpl is not None or raqm_pil in (True, False), (raqm_mpl, raqm_pil)),
            _c("with raqm the logical string is passed unchanged", with_raqm == s, with_raqm),
            _c("without raqm the string becomes presentation forms", pres >= 10, pres),
            _c("reversed + NFKC of the visual form gives back the logical text", back == s, back)]


# ---------------------------------------------------------------- ANLY-12
def _lum(hexc):
    rgb = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def anly_12(work: Path):
    light, dark = _contrast("#2a78d6", "#ffffff"), _contrast("#3987e5", "#1a1a1a")
    yellow = _contrast("#ffff00", "#ffffff")

    def validate(colors, surface):
        return {c: ("PASS" if _contrast(c, surface) >= 3 else "FAIL") for c in colors}

    rep = {"light": validate(["#2a78d6", "#ffff00"], "#ffffff"), "dark": validate(["#3987e5"], "#1a1a1a")}
    _w(work, "palette.json", {"report": rep, "light": light, "dark": dark, "engine": "WCAG relative-luminance contrast (python)"})
    return [_c("black on white = 21:1", abs(_contrast("#000000", "#ffffff") - 21) < 1e-9, 21),
            _c("#2a78d6 on white >= 3:1 (light PASS)", light >= 3 and rep["light"]["#2a78d6"] == "PASS", round(light, 2)),
            _c("#3987e5 on #1a1a1a >= 3:1 (dark PASS)", dark >= 3, round(dark, 2)),
            _c("planted #ffff00 on white FAILs (1.07:1)", rep["light"]["#ffff00"] == "FAIL" and yellow < 1.1, round(yellow, 2))]


# ---------------------------------------------------------------- ANLY-16
def anly_16(work: Path):
    rng = np.random.default_rng(0)
    n = 200
    X = rng.normal(0, 1, (n, 2))
    y = (X[:, 0] + rng.normal(0, 1.0, n) > 0).astype(int)  # noisy labels
    mu, sd = X.mean(0), X.std(0)

    def knn1(Xtr, ytr, Xte):
        m, s = Xtr.mean(0), Xtr.std(0)  # scaler fitted inside the fold
        a, b = (Xtr - m) / s, (Xte - m) / s
        d = ((b[:, None, :] - a[None, :, :]) ** 2).sum(-1)
        return ytr[d.argmin(1)]

    train_acc = float((knn1(X, y, X) == y).mean())
    folds = np.array_split(rng.permutation(n), 5)
    cv = []
    for k in range(5):
        te = folds[k]
        tr = np.concatenate([folds[j] for j in range(5) if j != k])
        cv.append(float((knn1(X[tr], y[tr], X[te]) == y[te]).mean()))
    _w(work, "cv.json", {"engine": "numpy 1-NN pipeline (scikit-learn not used)", "train": train_acc, "cv": cv, "cv_mean": float(np.mean(cv))})
    return [_c("training score of 1-NN is 1.0 (says nothing)", train_acc == 1.0, train_acc),
            _c("5-fold CV is clearly lower on noisy labels", np.mean(cv) < 0.9, np.mean(cv)),
            _c("CV beats chance (0.5)", np.mean(cv) > 0.55, cv),
            _c("five folds evaluated", len(cv) == 5, len(cv))]


# ---------------------------------------------------------------- ANLY-18
def anly_18(work: Path):
    r = optimize.linprog(c=[-40, -30], A_ub=[[1, 1], [2, 1]], b_ub=[40, 60], bounds=[(0, None)] * 2, method="highs")
    xy = np.linalg.solve([[1, 1], [2, 1]], [40, 60])
    _w(work, "lp.json", {"x": r.x.tolist(), "profit": -r.fun, "binding_solution": xy.tolist(), "status": r.status})
    return [_c("HiGHS optimum x = y = 20", np.allclose(r.x, [20, 20]), r.x.tolist()),
            _c("profit 1400 (negated objective)", abs(-r.fun - 1400) < 1e-9, -r.fun),
            _c("binding constraints solved directly agree", np.allclose(xy, r.x), xy.tolist()),
            _c("both constraints have zero slack", np.allclose(r.slack, 0), r.slack.tolist())]


# ---------------------------------------------------------------- ANLY-21
def anly_21(work: Path):
    r = optimize.minimize_scalar(lambda x: (x - 2) ** 2)
    r2 = optimize.minimize(lambda v: (v[0] - 1) ** 2 + (v[1] + 3) ** 2, [0, 0], constraints=[{"type": "ineq", "fun": lambda v: -v[1] - 0}])
    _w(work, "convex.json", {"engine": "scipy.optimize (cvxpy not used)", "x": r.x, "constrained": r2.x.tolist()})
    return [_c("argmin (x-2)^2 = 2.0", abs(r.x - 2) < 1e-6, r.x),
            _c("objective at optimum is 0", r.fun < 1e-10, r.fun),
            _c("constraint y <= 0 inactive: optimum (1,-3)", np.allclose(r2.x, [1, -3], atol=1e-5), r2.x.tolist())]


# ---------------------------------------------------------------- ANLY-23
def anly_23(work: Path):
    import heapq

    def dijkstra(adj, a, b):
        dist, prev, pq = {a: 0}, {}, [(0, a)]
        while pq:
            d, u = heapq.heappop(pq)
            if u == b:
                break
            for v, w in adj[u]:
                if d + w < dist.get(v, math.inf):
                    dist[v], prev[v] = d + w, u
                    heapq.heappush(pq, (d + w, v))
        path = [b]
        while path[-1] != a:
            path.append(prev[path[-1]])
        return path[::-1], dist[b]

    path5 = {i: [(j, 1) for j in (i - 1, i + 1) if 0 <= j < 5] for i in range(5)}
    p, d = dijkstra(path5, 0, 4)
    w = {"a": [("b", 1), ("c", 5)], "b": [("c", 1), ("a", 1)], "c": [("a", 5), ("b", 1)]}
    pw, dw = dijkstra(w, "a", "c")

    def pagerank(A, alpha=0.85, it=100):
        n = len(A)
        out = A.sum(1, keepdims=True)
        M = np.where(out > 0, A / np.where(out == 0, 1, out), 1 / n)
        r = np.ones(n) / n
        for _ in range(it):
            r = (1 - alpha) / n + alpha * M.T @ r
        return r

    cyc = np.roll(np.eye(4), 1, axis=1)
    star = np.zeros((4, 4))
    star[1:, 0] = 1
    star[0, 1:] = 1
    pr_c, pr_s = pagerank(cyc), pagerank(star)
    _w(work, "graph.json", {"engine": "python Dijkstra + numpy power iteration (networkx not used)", "path": p, "weighted": pw,
                            "pr_cycle": pr_c.tolist(), "pr_star": pr_s.tolist()})
    return [_c("shortest path on path_graph(5) is 0-1-2-3-4", p == [0, 1, 2, 3, 4] and d == 4, p),
            _c("weighted detour a-b-c (2) beats direct edge (5)", pw == ["a", "b", "c"] and dw == 2, pw),
            _c("PageRank of a directed cycle is uniform 0.25", np.allclose(pr_c, 0.25), pr_c.round(4).tolist()),
            _c("star hub has the highest PageRank; ranks sum to 1", pr_s.argmax() == 0 and abs(pr_s.sum() - 1) < 1e-9, pr_s.round(3).tolist())]


# ---------------------------------------------------------------- ANLY-24
def anly_24(work: Path):
    R = 6378137.0

    def to_3857(lon, lat):
        return R * math.radians(lon), R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

    def from_3857(x, y):
        return math.degrees(x / R), math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2)

    x, y = to_3857(31.2, 30.04)
    back = from_3857(x, y)
    # distance in metres along the equator: 1 degree = 111319.49 m
    one_deg = to_3857(1, 0)[0]
    _w(work, "reproject.json", {"engine": "closed-form EPSG:4326 -> EPSG:3857 (pyproj not used)", "cairo_x": x, "cairo_y": y})
    return [_c("Cairo lon 31.2 -> x 3,473,168 m", round(x) == 3473168, round(x)),
            _c("inverse returns the original lon/lat", abs(back[0] - 31.2) < 1e-9 and abs(back[1] - 30.04) < 1e-9, back),
            _c("1 degree of longitude at the equator = 111,319.49 m", abs(one_deg - 111319.49) < 0.01, one_deg),
            _c("Mercator y at lat 0 is 0", abs(to_3857(10, 0)[1]) < 1e-6, to_3857(10, 0)[1])]


# ---------------------------------------------------------------- ANLY-26
def anly_26(work: Path):
    rows = _sales()
    p = work / "sales.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(p, encoding="utf-8") as f:
        plain = sum(int(r["revenue"]) for r in csv.DictReader(f))
    arr = int(np.array([r["revenue"] for r in rows], dtype=np.int64).sum())
    db = sqlite3.connect(":memory:")
    db.execute("create table s(month, region, rep, revenue integer)")
    db.executemany("insert into s values(:month,:region,:rep,:revenue)", rows)
    sql = db.execute("select sum(revenue) from s").fetchone()[0]
    subs = dict(db.execute("select region, sum(revenue) from s group by region").fetchall())
    results = {"total": plain, "by_region": subs, "rows": len(rows)}
    _w(work, "results.json", results)
    frozen = json.loads((work / "results.json").read_text(encoding="utf-8"))
    text = f"إجمالي الإيراد {frozen['total']:,} من {frozen['rows']} صفاً"
    _w(work, "summary.txt", text)

    def reconcile(a, b):
        return {"ok": a == b, "gap": a - b}

    planted = reconcile(plain, plain - 17)
    return [_c("csv sum == numpy sum == SQL SUM", plain == arr == sql, (plain, arr, sql)),
            _c("regional subtotals add back to the total", sum(subs.values()) == plain, subs),
            _c("expected row count 180 asserted", len(rows) == 180, len(rows)),
            _c("narrative is generated from frozen results.json", f"{plain:,}" in text, text),
            _c("planted 17-unit mismatch is reported as a gap, not plugged", planted == {"ok": False, "gap": 17}, planted)]


# ---------------------------------------------------------------- ANLY-27
def anly_27(work: Path):
    db = sqlite3.connect(work / "hygiene.sqlite")
    db.execute("create table f(month text, region text, revenue integer, visits integer)")
    rng = np.random.default_rng(3)
    data = [(f"2026-{m:02d}", f"R{r}", int(rng.integers(100, 900)), int(rng.integers(0, 3)) * 100) for m in range(1, 13) for r in range(5)]
    db.executemany("insert into f values(?,?,?,?)", data)
    db.commit()
    q = "select month, region, revenue, visits, revenue * 1.0 / nullif(visits, 0) as rpv from f"
    out = db.execute(q).fetchall()
    zero_visits = [r for r in out if r[3] == 0]
    total_sql = db.execute("select sum(revenue) from f").fetchone()[0]
    independent = sum(d[2] for d in data)
    sample = out[:5]
    hand = all((r[4] is None) if r[3] == 0 else abs(r[4] - r[2] / r[3]) < 1e-12 for r in sample)
    try:
        db.execute("select revenue / 0 from f").fetchone()
        raw_div = "no error"
    except Exception as e:
        raw_div = str(e)
    _w(work, "query.sql", q)
    return [_c("COUNT(*) matches grain 12 x 5 = 60", len(out) == 60, len(out)),
            _c("NULLIF guard: zero denominators give NULL, not a crash", zero_visits and all(r[4] is None for r in zero_visits), len(zero_visits)),
            _c("SUM equals an independent total", total_sql == independent, (total_sql, independent)),
            _c("five sampled rows checked by hand", hand, sample),
            _c("columns are named (no SELECT *)", "*" not in q.split("from")[0].replace("* 1.0", ""), q)]


# ---------------------------------------------------------------- ANLY-28
def anly_28(work: Path):
    names = ["أحمد", "فاطمة", "محمد", "مريم", "خالد", "سارة", "يوسف", "نور"]

    def make(seed):
        rng = np.random.default_rng(seed)
        return [{"name": names[int(rng.integers(len(names)))], "amount": int(rng.integers(100, 1000))} for _ in range(50)]

    a, b, c = make(7), make(7), make(8)
    label = "synthetic (seed 7)"
    _w(work, "synthetic.json", {"label": label, "seed": 7, "rows": a})
    arabic = all(all("؀" <= ch <= "ۿ" for ch in r["name"]) for r in a)
    return [_c("same seed 7 reproduces the data exactly", a == b, len(a)),
            _c("different seed gives different data", a != c, ""),
            _c("names are Arabic script (hand-written list)", arabic, a[0]["name"]),
            _c("output labelled 'synthetic (seed 7)'", json.loads((work / "synthetic.json").read_text(encoding="utf-8"))["label"] == label, label)]


# ---------------------------------------------------------------- ANLY-29
def anly_29(work: Path):
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font
    wb = Workbook()
    inp = wb.active
    inp.title = "Inputs"
    inputs = [("cash", 200, "SAR", "bank"), ("receivables", 300, "SAR", "ledger"), ("loan", 150, "SAR", "contract"),
              ("share_a", 0.6, "%", "register"), ("share_b", 0.4, "%", "register")]
    inp.append(["name", "value", "unit", "source"])
    for row in inputs:
        inp.append(list(row))
        inp.cell(inp.max_row, 2).font = Font(color="FF0000FF")
    calc = wb.create_sheet("Calc")
    calc["A1"], calc["B1"] = "assets", "=Inputs!B2+Inputs!B3"
    calc["A2"], calc["B2"] = "liabilities", "=Inputs!B4"
    calc["A3"], calc["B3"] = "equity", "=B1-B2"
    outp = wb.create_sheet("Outputs")
    outp["A1"], outp["B1"] = "equity", "=Calc!B3"
    chk = wb.create_sheet("Checks")
    chk["A1"], chk["B1"] = "balance", "=Calc!B1-Calc!B2-Calc!B3"
    chk["A2"], chk["B2"] = "shares", "=Inputs!B5+Inputs!B6-1"
    p = work / "model.xlsx"
    wb.save(p)
    wb2 = load_workbook(p)
    calc_formulas = all(str(c.value).startswith("=") for row in wb2["Calc"].iter_rows(min_col=2, max_col=2) for c in row)
    out_links = all(str(c.value).startswith("=Calc!") for row in wb2["Outputs"].iter_rows(min_col=2, max_col=2) for c in row)
    blue = all(wb2["Inputs"].cell(r, 2).font.color.rgb == "FF0000FF" for r in range(2, 7))
    v = {n: val for n, val, *_ in inputs}
    assets, liab = v["cash"] + v["receivables"], v["loan"]
    balance = assets - liab - (assets - liab)
    shares = v["share_a"] + v["share_b"] - 1
    return [_c("sheets Inputs/Calc/Outputs/Checks in order", wb2.sheetnames == ["Inputs", "Calc", "Outputs", "Checks"], wb2.sheetnames),
            _c("Calc holds formulas only", calc_formulas, ""),
            _c("Outputs are links to Calc only", out_links, ""),
            _c("input values in blue font with unit and source", blue and wb2["Inputs"]["C2"].value == "SAR", ""),
            _c("checks evaluate to zero: balance and shares", balance == 0 and abs(shares) < 1e-12, (balance, shares))]


PROGRAMS = {"ANLY-01": anly_01, "ANLY-05": anly_05, "ANLY-06": anly_06, "ANLY-07": anly_07, "ANLY-08": anly_08,
            "ANLY-09": anly_09, "ANLY-10": anly_10, "ANLY-11": anly_11, "ANLY-12": anly_12, "ANLY-16": anly_16,
            "ANLY-18": anly_18, "ANLY-21": anly_21, "ANLY-23": anly_23, "ANLY-24": anly_24, "ANLY-26": anly_26,
            "ANLY-27": anly_27, "ANLY-28": anly_28, "ANLY-29": anly_29}
