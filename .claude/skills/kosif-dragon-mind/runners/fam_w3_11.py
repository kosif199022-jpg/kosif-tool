"""Wave 3 chunk 11: data-analysis (ANLY), app-feature-transfer (APPX), camera (CAM), documents (DOC) and
Latin typography (TYPE) method cards as real programs with known-answer checks and negative controls.

Every runner builds a deterministic fixture inside its work folder (CSV tables, synthetic clips with a
frame index painted in, tones and clicks, PDFs/DOCX/XLSX written by code, fonts from the repo), runs the
card's own engine on it (duckdb, polars, plotly, altair, seaborn, lightgbm, ortools, pulp+HiGHS, z3, prophet,
sympy, scikit-learn, statsforecast, geopandas, biopython, rdkit, ffmpeg filters, OpenCV, LibreOffice, pandoc,
weasyprint, reportlab, pypdf, markitdown, pypdfium2, tesseract, pymupdf, pdfplumber, tabula, Node docx /
pptxgenjs / exceljs / pdf-lib, Slidev, Marp, Mermaid, three.js, Chromium via Playwright) and measures the
produced file. Each card also measures the untreated input with the same criterion, which must fail.

Installed for these cards (the real engines the cards name), into the user environment:
  pip: altair seaborn lightgbm rdkit pytesseract pymupdf weasyprint tabula-py prophet highspy
       (highspy makes pulp 4 list HiGHS as the card says; OR-Tools and pulp therefore run in separate
       Python processes, exactly as ANLY-19/20 warn)
  npm -g: pptxgenjs exceljs pdf-lib
  npm --prefix /opt/kosif-pwc: playwright-chromium@1.63.0 (Slidev export; linked into the work folder)
xgboost was not installed (its Linux wheel pulls the ~200 MB NCCL CUDA library); ANLY-17 runs LightGBM.
"""
from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from _harness import card, check, fx

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SP = REPO / ".claude/skills/kosif-superpowers"
FONTS = SP / "proofs/_shared/fonts"
NODE_MODULES = "/opt/node22/lib/node_modules"
PWC = Path("/opt/kosif-pwc/node_modules")
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"

_SAME = "measured earlier by another wave module; still true here"
GAPS: dict = {
    "ANLY-32": "Lean 4 needs the elan toolchain download (several hundred MB, Mathlib cache 1-2 GB); not installed",
    "APPX-13": "faster-whisper is installed but has no model on disk and huggingface.co is refused by the proxy; "
               "no TTS voice is installed either, so there is no speech to transcribe",
    "APPX-155": "whisper.cpp (whisper-cli) and its ggml models (190-574 MB) are not installed; models live on huggingface.co, refused here",
    "APPX-18": "getDisplayMedia returns NotReadableError (Could not start video source) in headless Chromium, the new headless "
               "mode and headful Chromium under Xvfb here; Electron's desktopCapturer is not installed",
    "APPX-19": "needs Electron (BrowserWindow alwaysOnTop/setContentProtection) and a real desktop compositor; Electron is not installed",
    "APPX-28": "electron-builder NSIS target needs Electron, makensis and a Windows target toolchain; none is installed",
    "APPX-59": "the virtualcam project is a PowerShell script driving OBS Studio 28+ on Windows; no OBS, no PowerShell here",
    "APPX-60": "TikPlayer is a Kotlin Android app; there is no Android SDK (ANDROID_HOME unset) to run gradle assembleDebug",
    "DOC-26": "a host-designated first-party docs connector is a live service; nothing to run locally",
    "DOC-28": "editing Google Drive files needs the Google Workspace connector and the user's account (live service)",
    "DOC-29": "Docling downloads layout/table models (a few hundred MB) and pulls torch; not installed",
    "DOC-30": "Marker needs 1-2 GB of model weights; not installed",
    "CAM-64": _SAME + ": three.js dof() needs WebGPU; the WebGL2 fallback blurred near and far planes alike",
    "CAM-71": _SAME + ": the card's zoom formula leaves black corners; the exact cover is |cos r| + q|sin r|",
    "CAM-92": _SAME + ": hyperframes add carousel-circle-* fetches sample photos from static.heygen.ai (no network)",
    "CAM-93": _SAME + ": hyperframes add carousel-orbit-* needs static.heygen.ai (no network)",
    "CAM-94": _SAME + ": hyperframes add carousel-path-* needs static.heygen.ai (no network)",
    "CAM-95": _SAME + ": hyperframes add carousel-text-circle-* needs static.heygen.ai (no network)",
    "CAM-96": _SAME + ": hyperframes add carousel-vision-* needs static.heygen.ai (no network)",
    "CAM-119": _SAME + ": scripts/safe-zones.cjs and the subject matte are not in this checkout",
    "CAM-184": _SAME + ": Kling camera_control runs on the paid Kling video API",
    "CAM-389": _SAME + ": reference excerpt of Kling camera control; needs a paid video-generation key",
    "TYPE-13": _SAME + ": the review page's live Google Fonts swap is not part of this container",
}

# ----------------------------------------------------------------------------------------------- helpers


def _np():
    import numpy as np
    return np


def jw(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return Path(path)


def tw(path, text):
    Path(path).write_text(text, encoding="utf-8")
    return Path(path)


def pysub(wd, code, timeout=60):
    """Run Python code in a fresh process (OR-Tools and pulp/HiGHS must not share one); last stdout line is JSON."""
    src = Path(wd) / ("sub_%d.py" % (abs(hash(code)) % 10 ** 8))
    src.write_text(code, encoding="utf-8")
    done = subprocess.run([sys.executable, str(src)], capture_output=True, text=True, timeout=timeout, cwd=str(wd),
                          stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("python failed: " + (done.stderr or done.stdout)[-600:])
    return json.loads(done.stdout.strip().splitlines()[-1])


def node_js(wd, name, js, timeout=60, env_extra=None):
    src = Path(wd) / (name + ".cjs")
    src.write_text(js, encoding="utf-8")
    env = dict(os.environ, NODE_PATH=NODE_MODULES)
    env.update(env_extra or {})
    done = subprocess.run(["node", str(src)], capture_output=True, text=True, timeout=timeout, cwd=str(wd), env=env,
                          stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("node failed: " + (done.stderr or done.stdout)[-600:])
    return json.loads(done.stdout.strip().splitlines()[-1])


PW_HEAD = "const {chromium}=require('playwright');const fs=require('fs');\n"


def run(cmd, timeout=60, env=None, cwd=None):
    done = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout, env=env,
                          cwd=None if cwd is None else str(cwd), stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("command failed (%d): %s" % (done.returncode, (done.stderr or done.stdout)[-500:]))
    return done


def font(name="Poppins-Bold.ttf", size=40):
    from PIL import ImageFont
    return ImageFont.truetype(str(FONTS / name), size)


def save_png(arr, path):
    from PIL import Image
    Image.fromarray(_np().clip(arr, 0, 255).round().astype("uint8")).save(path)
    return Path(path)


def load_rgb(path):
    from PIL import Image
    return _np().asarray(Image.open(path).convert("RGB")).astype(float)


def write_video(path, frames, fps=30):
    """Encode numpy frames losslessly (libx264rgb qp 0) so pixel measurements read back exactly."""
    np = _np()
    frames = list(frames)
    h, w = frames[0].shape[:2]
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                          "-preset", "ultrafast", str(path)], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f in frames:
        p.stdin.write(np.clip(f, 0, 255).round().astype("uint8").tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError("ffmpeg encode failed: %s" % p.stderr.read().decode(errors="replace")[-300:])
    return Path(path)


def read_video(path):
    np = _np()
    st = [s for s in fx.probe(path)["streams"] if s.get("codec_type") == "video"][0]
    w, h = int(st["width"]), int(st["height"])
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, timeout=120, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(out, dtype=np.uint8).reshape(-1, h, w, 3).astype(float)


def duration(path):
    return float(fx.probe(path)["format"]["duration"])


def ink_bbox(arr, bg=(255, 255, 255), tol=40):
    """Bounding box (x0, y0, x1, y1) of pixels that differ from the background, or None."""
    np = _np()
    a = np.asarray(arr, dtype=float)
    if a.ndim == 2:
        m = np.abs(a - (bg if np.isscalar(bg) else bg[0])) > tol
    else:
        m = np.abs(a - np.array(bg, dtype=float)).max(axis=-1) > tol
    ys, xs = np.nonzero(m)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def color_mask(arr, rgb, tol=30):
    np = _np()
    return np.abs(np.asarray(arr, dtype=float) - np.array(rgb, dtype=float)).max(axis=-1) <= tol


def centroid(mask):
    np = _np()
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return float(xs.mean()), float(ys.mean())


def bezier(x1, y1, x2, y2):
    """CSS cubic-bezier(x1, y1, x2, y2) as a function of progress 0..1 (Newton + bisection)."""
    def bx(t):
        return 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3

    def by(t):
        return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3

    def f(x):
        x = min(1.0, max(0.0, x))
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if bx(mid) < x:
                lo = mid
            else:
                hi = mid
        return by((lo + hi) / 2)
    return f


def ease_in_out_cubic(p):
    p = min(1.0, max(0.0, p))
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def ease_out_cubic(p):
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 3


def ease_in_cubic(p):
    p = min(1.0, max(0.0, p))
    return p ** 3


def ease_out_quart(p):
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 4


def ease_out_quint(p):
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 5


def sine_in_out(p):
    p = min(1.0, max(0.0, p))
    return -(math.cos(math.pi * p) - 1) / 2


def interp(t, ts, vs, ease=None):
    """Remotion-style interpolate(frame, [t0..tn], [v0..vn], {easing, clamp})."""
    if t <= ts[0]:
        return vs[0]
    if t >= ts[-1]:
        return vs[-1]
    for i in range(len(ts) - 1):
        if ts[i] <= t <= ts[i + 1]:
            p = (t - ts[i]) / float(ts[i + 1] - ts[i])
            return vs[i] + (vs[i + 1] - vs[i]) * (ease(p) if ease else p)
    return vs[-1]


def texture(w, h, seed=7):
    """Deterministic textured plate (blurred noise + grid) that image registration can lock onto."""
    np = _np()
    import cv2
    rng = np.random.default_rng(seed)
    a = rng.random((h, w)).astype("float32")
    a = cv2.GaussianBlur(a, (0, 0), 3)
    a = (a - a.min()) / (a.max() - a.min()) * 200 + 20
    a[::40, :] = 250
    a[:, ::40] = 250
    return np.dstack([a, a * 0.8 + 30, 255 - a]).clip(0, 255)


def warp(img, s=1.0, tx=0.0, ty=0.0, rot=0.0, out=None):
    """One camera transform (scale about the centre, rotate in degrees, translate in px) as one affine matrix."""
    import cv2
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2.0, h / 2.0), -rot, s)
    M[0, 2] += tx
    M[1, 2] += ty
    ow, oh = out or (w, h)
    return cv2.warpAffine(img.astype("float32"), M, (ow, oh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


MARKS = [((255, 0, 0), 0.3, 0.3), ((0, 255, 0), 0.7, 0.3), ((0, 0, 255), 0.7, 0.7), ((255, 255, 0), 0.3, 0.68)]


def fid_plate(w, h, seed=7):
    """Grey textured plate with four coloured fiducial dots, so a camera transform can be measured exactly."""
    np = _np()
    t = texture(w, h, seed).mean(axis=-1, keepdims=True) * 0.5 + 60
    a = np.repeat(t, 3, axis=-1)
    yy, xx = np.mgrid[0:h, 0:w]
    r = max(3, w // 48)
    for col, fx_, fy_ in MARKS:
        a[(xx - fx_ * w) ** 2 + (yy - fy_ * h) ** 2 <= r * r] = col
    return a


def marks(img, tol=70):
    np = _np()
    pts = []
    a = np.asarray(img, float)
    ys, xs = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    for col, _, _ in MARKS:
        d = np.abs(a - np.array(col, float)).max(axis=-1)
        wgt = np.clip(1 - d / 90.0, 0, 1)
        if wgt.sum() < 3:
            return None
        pts.append(((xs * wgt).sum() / wgt.sum(), (ys * wgt).sum() / wgt.sum()))
    return np.array(pts)


def est(ref, img):
    """Measure the camera transform (scale, tx, ty, rot deg) mapping ref onto img from the fiducial dots (Umeyama)."""
    np = _np()
    P, Q = marks(ref), marks(img)
    if P is None or Q is None:
        raise RuntimeError("fiducials not visible")
    mp, mq = P.mean(0), Q.mean(0)
    X, Y = P - mp, Q - mq
    U, S, Vt = np.linalg.svd(Y.T @ X / len(P))
    D = np.diag([1, np.sign(np.linalg.det(U @ Vt))])
    R = U @ D @ Vt
    sc = float(np.trace(np.diag(S) @ D) / (X ** 2).sum(axis=1).mean())
    t = mq - sc * R @ mp
    h, w = ref.shape[:2]
    c = np.array([w / 2.0, h / 2.0])
    tc = sc * R @ c + t - c
    return sc, float(tc[0]), float(tc[1]), float(math.degrees(math.atan2(R[1, 0], R[0, 0])))


# =============================================================================================== ANLY


def _sales_csv(wd, n_months=6):
    """month, region, revenue rows (two rows per month/region so GROUP BY matters); known totals in python."""
    rows, tot = [], {}
    regions = ["north", "south", "east"]
    for m in range(1, n_months + 1):
        for ri, r in enumerate(regions):
            for k in range(2):
                v = 100 * (ri + 1) + 10 * m * (ri + 1) + 5 * k + (m * 7 + ri * 3) % 11
                if r == "east" and m == 3:
                    v = 0  # a zero month exercises NULLIF
                rows.append((m, r, v))
                tot[(m, r)] = tot.get((m, r), 0) + v
    p = Path(wd) / "sales.csv"
    p.write_text("month,region,revenue\n" + "".join("%d,%s,%d\n" % r for r in rows), encoding="utf-8")
    return p, tot, regions


@card("ANLY-02")
def duckdb_window_sql(task, wd):
    import duckdb
    p, tot, regions = _sales_csv(wd)
    con = duckdb.connect()
    q = ("WITH m AS (SELECT month, region, SUM(revenue) AS rev FROM read_csv('%s', header=true) GROUP BY month, region) "
         "SELECT month, region, rev, rev - LAG(rev) OVER (PARTITION BY region ORDER BY month) AS mom, "
         "rev / NULLIF(LAG(rev) OVER (PARTITION BY region ORDER BY month), 0) AS ratio, "
         "RANK() OVER (PARTITION BY month ORDER BY rev DESC) AS rk FROM m ORDER BY region, month") % p
    df = con.sql(q).df()
    out = Path(wd) / "window.csv"
    df.to_csv(out, index=False)
    ok_mom = ok_rank = True
    for r in regions:
        for m in range(2, 7):
            row = df[(df.region == r) & (df.month == m)].iloc[0]
            ok_mom &= int(row.mom) == tot[(m, r)] - tot[(m - 1, r)]
    for m in range(1, 7):
        order = sorted(regions, key=lambda r: -tot[(m, r)])
        for i, r in enumerate(order):
            ok_rank &= int(df[(df.region == r) & (df.month == m)].rk.iloc[0]) == i + 1
    east4 = df[(df.region == "east") & (df.month == 4)].ratio.iloc[0]
    raw_rows = con.execute("SELECT COUNT(*) FROM read_csv('%s', header=true)" % p).fetchall()[0][0]
    return [check("one row per month x region after the CTE", len(df) == 18, len(df), 18),
            check("LAG month-over-month equals python totals", ok_mom),
            check("RANK per month by revenue matches python", ok_rank),
            check("NULLIF guard: ratio after a zero month is NULL, no division error", east4 != east4, str(east4), "NaN"),
            check("negative control: the raw CSV (no GROUP BY) has 36 rows, not 18", raw_rows != 18, raw_rows, "!= 18")], [out]


@card("ANLY-03")
def csv_to_parquet(task, wd):
    import duckdb
    p = Path(wd) / "big.csv"
    lines = ["id,day,amount,label"] + ["%d,2026-01-%02d,%.2f,%s" % (i, i % 28 + 1, i * 1.25, "abc"[i % 3]) for i in range(180)]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out = Path(wd) / "big.parquet"
    con = duckdb.connect()
    con.sql("COPY (SELECT id, day, amount, label FROM read_csv('%s', header=true)) TO '%s' (FORMAT parquet)" % (p, out))
    n = con.execute("SELECT COUNT(*) FROM '%s'" % out).fetchall()[0][0]
    import pyarrow.parquet as pq
    schema = {f.name: str(f.type) for f in pq.read_schema(out)}
    total = con.execute("SELECT SUM(amount) FROM '%s'" % out).fetchall()[0][0]
    raw_types = [r[1] for r in con.sql("DESCRIBE SELECT * FROM read_csv('%s', header=true, all_varchar=true)" % p).fetchall()]
    return [check("row count survives the round trip", n == 180, n, 180),
            check("columns are typed (int, date, double), not strings", schema.get("id", "").startswith("int")
                  and schema.get("day") == "date32[day]" and schema.get("amount") == "double", schema),
            check("sum of amount on read-back", abs(total - sum(i * 1.25 for i in range(180))) < 1e-6, total, 20137.5),
            check("parquet is smaller than the CSV", out.stat().st_size < p.stat().st_size, out.stat().st_size, p.stat().st_size),
            check("negative control: untyped CSV read gives VARCHAR columns", all(t == "VARCHAR" for t in raw_types), raw_types)], [out]


def _kv_csv(wd, name="kv.csv", n=3000):
    keys = "abcdefg"
    p = Path(wd) / name
    exp = {}
    with open(p, "w", encoding="utf-8") as f:
        f.write("k,v\n")
        for i in range(n):
            k = keys[(i * 5 + i // 7) % 7]
            v = (i * 13) % 17
            exp[k] = exp.get(k, 0) + v
            f.write("%s,%d\n" % (k, v))
    return p, exp


@card("ANLY-04")
def polars_lazy(task, wd):
    import polars as pl
    p, exp = _kv_csv(wd)
    lf = pl.scan_csv(p).group_by("k").agg(pl.col("v").sum()).sort("k")
    lazy = isinstance(lf, pl.LazyFrame)
    df = lf.collect()
    got = dict(zip(df["k"].to_list(), df["v"].to_list()))
    out = Path(wd) / "agg.csv"
    df.write_csv(out)
    first = pl.read_csv(p).head(7)
    raw = dict(zip(first["k"].to_list(), first["v"].to_list()))
    return [check("polars major version recorded before writing code (2.x API)", int(pl.__version__.split(".")[0]) >= 1, pl.__version__),
            check("scan_csv returns a LazyFrame (nothing read until collect)", lazy),
            check("lazy group_by sum equals python totals", got == exp, got, exp),
            check("negative control: raw rows are not the per-key sums", raw != exp, raw)], [out]


@card("ANLY-13")
def plotly_cdn(task, wd):
    import plotly.express as px
    import pandas as pd
    df = pd.DataFrame({"k": list("ABCDE"), "v": [3, 7, 2, 9, 5]})
    fig = px.bar(df, x="k", y="v")
    cdn = Path(wd) / "chart_cdn.html"
    full = Path(wd) / "chart_inline.html"
    fig.write_html(cdn, include_plotlyjs="cdn")
    fig.write_html(full)
    html = cdn.read_text(encoding="utf-8")
    m = re.search(r'"y":\[([0-9,]+)\]', html) or re.search(r'"y":\{"dtype":"[^"]+","bdata":"([^"]+)"', html)
    ys = None
    if m and "," in m.group(1) or (m and m.group(1).isdigit()):
        ys = [int(x) for x in m.group(1).split(",")]
    elif m:
        import base64
        import numpy as np
        dt = re.search(r'"y":\{"dtype":"([^"]+)"', html).group(1)
        ys = np.frombuffer(base64.b64decode(m.group(1)), dtype=dt).astype(int).tolist()
    return [check("cdn variant references the plotly CDN script", "cdn.plot.ly" in html),
            check("cdn file is small (< 100 KB)", cdn.stat().st_size < 100_000, cdn.stat().st_size, "< 100000"),
            check("the bar values are in the figure JSON", ys == [3, 7, 2, 9, 5], ys, [3, 7, 2, 9, 5]),
            check("negative control: the default write_html inlines the library (> 3 MB)", full.stat().st_size > 3_000_000,
                  full.stat().st_size, "> 3000000")], [cdn]


@card("ANLY-14")
def altair_vegalite(task, wd):
    import altair as alt
    import pandas as pd
    df = pd.DataFrame({"k": list("ABCD"), "v": [4, 1, 6, 3]})
    spec_s = alt.Chart(df).mark_bar().encode(x="k", y="v").to_json()
    out = tw(Path(wd) / "chart.vl.json", spec_s)
    spec = json.loads(spec_s)
    ds = spec.get("datasets", {})
    vals = list(ds.values())[0] if ds else spec.get("data", {}).get("values")
    mark = spec.get("mark")
    mark = mark.get("type") if isinstance(mark, dict) else mark
    raw = json.loads(df.to_json(orient="records"))
    return [check("Vega-Lite v5+ schema", "vega-lite" in spec.get("$schema", ""), spec.get("$schema")),
            check("mark is bar", mark == "bar", mark),
            check("x/y encodings bound to k (nominal) and v (quantitative)",
                  spec["encoding"]["x"]["field"] == "k" and spec["encoding"]["y"]["type"] == "quantitative", spec["encoding"]),
            check("data values travel inside the spec", [r["v"] for r in vals] == [4, 1, 6, 3], [r["v"] for r in vals]),
            check("negative control: the bare data JSON carries no mark/encoding", "mark" not in json.dumps(raw))], [out]


@card("ANLY-15")
def seaborn_dist(task, wd):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    rng = np.random.default_rng(3)
    data = np.round(rng.normal(50, 10, 400), 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3))
    sns.histplot(data, bins=10, ax=a1)
    df = pd.DataFrame({"g": ["a"] * 200 + ["b"] * 200, "y": np.r_[data[:200], data[200:] + 20]})
    sns.boxplot(x="g", y="y", data=df, ax=a2)
    out = Path(wd) / "dist.png"
    fig.savefig(out, dpi=80)
    heights = [int(round(p.get_height())) for p in a1.patches]
    counts, _ = np.histogram(data, bins=10)
    med_lines = [ln for ln in a2.lines if len(ln.get_ydata()) == 2 and ln.get_ydata()[0] == ln.get_ydata()[1]]
    meds = sorted({round(float(ln.get_ydata()[0]), 3) for ln in med_lines})
    want = sorted({round(float(np.median(data[:200])), 3), round(float(np.median(data[200:] + 20)), 3)})
    empty = plt.figure().add_subplot()
    plt.close("all")
    return [check("histogram bar heights equal numpy counts", heights == counts.tolist(), heights, counts.tolist()),
            check("boxplot medians drawn at the data medians", all(m in meds for m in want), meds, want),
            check("figure written", out.stat().st_size > 5000, out.stat().st_size),
            check("negative control: an empty axes has no bars", len(empty.patches) == 0 and counts.sum() == 400)], [out]


@card("ANLY-17")
def gbm_baseline(task, wd):
    import lightgbm as lgb
    import numpy as np
    from sklearn.metrics import r2_score
    rng = np.random.default_rng(0)
    X = rng.uniform(-3, 3, (1500, 4))
    y = np.sin(X[:, 0]) * 3 + (X[:, 1] > 0) * 2 + X[:, 2] ** 2 * 0.5 + rng.normal(0, 0.1, 1500)
    Xtr, Xva, Xte = X[:1000], X[1000:1250], X[1250:]
    ytr, yva, yte = y[:1000], y[1000:1250], y[1250:]
    m = lgb.LGBMRegressor(n_estimators=2000, learning_rate=0.1, n_jobs=2, verbose=-1)
    m.fit(Xtr, ytr, eval_set=[(Xva, yva)], callbacks=[lgb.early_stopping(50, verbose=False)])
    r2 = r2_score(yte, m.predict(Xte))
    base = r2_score(yte, np.full_like(yte, ytr.mean()))
    out = jw(Path(wd) / "gbm.json", {"r2_test": r2, "best_iteration": m.best_iteration_, "baseline_r2": base})
    return [check("held-out R2 of the boosted trees", r2 > 0.95, r2, "> 0.95"),
            check("early stopping on the validation split stopped before 2000 rounds", 0 < m.best_iteration_ < 2000, m.best_iteration_),
            check("negative control: the mean predictor scores R2 ~ 0", base < 0.05, base, "< 0.05")], [out]


@card("ANLY-19")
def ortools_solvers(task, wd):
    res = pysub(wd, r'''
import json
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
s = pywraplp.Solver.CreateSolver("GLOP"); x = s.NumVar(0, 10, "x"); s.Maximize(3 * x); s.Solve()
lp1 = s.Objective().Value()
s2 = pywraplp.Solver.CreateSolver("GLOP"); a = s2.NumVar(0, s2.infinity(), "a"); b = s2.NumVar(0, s2.infinity(), "b")
s2.Add(a + 2 * b <= 14); s2.Add(3 * a - b >= 0); s2.Add(a - b <= 2); s2.Maximize(3 * a + 4 * b); s2.Solve()
lp2 = [s2.Objective().Value(), a.solution_value(), b.solution_value()]
m = pywraplp.Solver.CreateSolver("SCIP") or pywraplp.Solver.CreateSolver("CBC")
u = m.IntVar(0, 10, "u"); v = m.IntVar(0, 10, "v"); m.Add(2 * u + 3 * v <= 12); m.Add(u - v <= 2)
m.Maximize(u + 2 * v); m.Solve(); mip = [m.Objective().Value(), u.solution_value(), v.solution_value()]
cp = cp_model.CpModel(); q = [cp.NewIntVar(0, 3, "q%d" % i) for i in range(4)]
cp.AddAllDifferent(q); cp.Add(q[0] + q[1] == 5); cp.Add(q[2] > q[3]); cp.Add(q[0] > q[1])
sv = cp_model.CpSolver(); st = sv.Solve(cp); sol = [sv.Value(t) for t in q]
cp2 = cp_model.CpModel(); z = cp2.NewIntVar(0, 3, "z"); cp2.Add(z > 5); st2 = cp_model.CpSolver().Solve(cp2)
print(json.dumps({"lp1": lp1, "lp2": lp2, "mip": mip, "cp": sol, "cp_status": sv.StatusName(st), "infeasible": st2 == cp_model.INFEASIBLE}))
''')
    out = jw(Path(wd) / "ortools.json", res)
    lp2 = res["lp2"]
    return [check("GLOP: maximise 3x on [0,10] -> 30 at x=10 (objective)", abs(res["lp1"] - 30) < 1e-9, res["lp1"], 30),
            check("GLOP 2-var LP optimum 3a+4b = 34 at (6,4)", abs(lp2[0] - 34) < 1e-6 and abs(lp2[1] - 6) < 1e-6, lp2, [34, 6, 4]),
            check("MIP optimum u+2v = 8 with integers", abs(res["mip"][0] - 8) < 1e-9 and all(float(t).is_integer() for t in res["mip"][1:]), res["mip"]),
            check("CP-SAT all-different puzzle solved", res["cp"] == [3, 2, 1, 0] and res["cp_status"] == "OPTIMAL", res["cp"], [3, 2, 1, 0]),
            check("negative control: a contradictory model is reported INFEASIBLE", res["infeasible"])], [out]


@card("ANLY-20")
def pulp4_highs(task, wd):
    res = pysub(wd, r'''
import json, pulp
m = pulp.LpProblem("t", pulp.LpMaximize)
x = m.add_variable("x", 0, 4); y = m.add_variable("y", 0, 10)
m += 3 * x + 2 * y; m += x + y <= 8; m += x - y >= -2
st = m.solve(pulp.HiGHS(msg=False))
bad = pulp.LpProblem("b", pulp.LpMinimize); z = bad.add_variable("z", 0, 1); bad += z; bad += z >= 2
st2 = bad.solve(pulp.HiGHS(msg=False))
print(json.dumps({"ver": pulp.__version__, "solvers": pulp.listSolvers(onlyAvailable=True), "status": st.status.name,
                  "obj": pulp.value(m.objective), "x": x.value(), "y": y.value(), "bad": st2.status.name,
                  "old_cbc": "PULP_CBC_CMD" in pulp.listSolvers(onlyAvailable=True)}))
''')
    out = jw(Path(wd) / "pulp.json", res)
    return [check("pulp 4 with HiGHS available", res["ver"].startswith("4") and "HiGHS" in res["solvers"], [res["ver"], res["solvers"]]),
            check("new add_variable API solves to optimum 3x+2y = 20 at (4,4)",
                  res["status"] == "Optimal" and abs(res["obj"] - 20) < 1e-6 and abs(res["x"] - 4) < 1e-6, [res["obj"], res["x"], res["y"]]),
            check("old PULP_CBC_CMD is not available (the card's warning)", not res["old_cbc"]),
            check("negative control: an infeasible model is not reported Optimal", res["bad"] != "Optimal", res["bad"])], [out]


@card("ANLY-22")
def z3_puzzle(task, wd):
    import z3
    a, b = z3.Ints("a b")
    s = z3.Solver()
    s.add(a + b == 10, a - b == 4)
    st = s.check()
    mdl = s.model()
    av, bv = mdl[a].as_long(), mdl[b].as_long()
    # a 3-person roster: each a distinct shift 1..3, Ali not on 1, Badr before Ali
    al, ba, ca = z3.Ints("ali badr car")
    r = z3.Solver()
    r.add(z3.Distinct(al, ba, ca), *[z3.And(v >= 1, v <= 3) for v in (al, ba, ca)], al != 1, ba < al, ca != 3)
    r.check()
    rm = r.model()
    roster = [rm[v].as_long() for v in (al, ba, ca)]
    u = z3.Solver()
    u.add(a + b == 10, a - b == 4, a < 5)
    unsat = u.check() == z3.unsat
    g = z3.Solver()
    g.add(a + b == 10, a - b == 4, a == 0, b == 0)
    guess_unsat = g.check() == z3.unsat
    out = jw(Path(wd) / "z3.json", {"a": av, "b": bv, "roster": roster, "impossible_proved": unsat})
    return [check("model a=7, b=3", st == z3.sat and (av, bv) == (7, 3), [av, bv], [7, 3]),
            check("roster satisfies every constraint", len(set(roster)) == 3 and roster[0] != 1 and roster[1] < roster[0] and roster[2] != 3, roster),
            check("unsat proves the extra constraint impossible", unsat),
            check("negative control: z3 rejects the untreated guess a=0, b=0", guess_unsat)], [out]


@card("ANLY-25")
def prophet_forecast(task, wd):
    import logging
    logging.getLogger("cmdstanpy").setLevel(logging.ERROR)
    logging.getLogger("prophet").setLevel(logging.ERROR)
    import numpy as np
    import pandas as pd
    from prophet import Prophet
    n = 140
    ds = pd.date_range("2025-01-01", periods=n, freq="D")
    t = np.arange(n)
    y = 50 + 0.2 * t + 6 * np.sin(2 * np.pi * t / 7) + np.random.default_rng(1).normal(0, 0.3, n)
    hol = pd.DataFrame({"holiday": "fest", "ds": pd.to_datetime(["2025-02-10", "2025-03-17", "2025-05-12"]),
                        "lower_window": 0, "upper_window": 0})
    y[[40, 75, 131]] += 25
    train = pd.DataFrame({"ds": ds[:126], "y": y[:126]})
    m = Prophet(daily_seasonality=False, yearly_seasonality=False, weekly_seasonality=True, holidays=hol).fit(train)
    fc = m.predict(m.make_future_dataframe(14))
    pred = fc.yhat.values[126:]
    truth = y[126:]
    hol_i = 131 - 126
    mask = np.ones(14, bool)
    mask[hol_i] = False
    mape = float(np.mean(np.abs(pred[mask] - truth[mask]) / truth[mask]))
    naive = float(np.mean(np.abs(train.y.mean() - truth[mask]) / truth[mask]))
    hol_err = abs(pred[hol_i] - truth[hol_i])
    out = Path(wd) / "forecast.csv"
    fc[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(out, index=False)
    return [check("14-day holdout MAPE with weekly seasonality", mape < 0.03, mape, "< 0.03"),
            check("the holiday spike is forecast (error < 6 on a +25 day)", hol_err < 6, hol_err, "< 6"),
            check("negative control: the flat mean forecast misses (MAPE > 0.1)", naive > 0.1, naive, "> 0.1")], [out]


@card("ANLY-30")
def sympy_exact(task, wd):
    import sympy as sp
    x = sp.symbols("x")
    roots = sorted(sp.solve(x ** 2 - 5 * x + 6, x))
    integ = sp.integrate(sp.sin(x) ** 2, (x, 0, sp.pi))
    tex = sp.latex(integ)
    der = sp.diff(sp.sin(x) * sp.exp(x), x)
    simp = sp.simplify(sp.sin(x) ** 2 + sp.cos(x) ** 2)
    out = tw(Path(wd) / "sympy.tex", "roots %s\n\\int_0^\\pi \\sin^2 x\\,dx = %s\n%s\n" % (roots, tex, sp.latex(der)))
    poly = x ** 2 - 5 * x + 6
    return [check("roots [2, 3]", roots == [2, 3], [int(r) for r in roots], [2, 3]),
            check("integral of sin^2 on [0, pi] = pi/2 exactly", sp.simplify(integ - sp.pi / 2) == 0, str(integ)),
            check("LaTeX export \\frac{\\pi}{2}", tex == r"\frac{\pi}{2}", tex),
            check("derivative and simplification exact", sp.simplify(der - sp.exp(x) * (sp.sin(x) + sp.cos(x))) == 0 and simp == 1),
            check("negative control: x=1 is not a root", poly.subs(x, 1) != 0, int(poly.subs(x, 1)))], [out]


@card("ANLY-31")
def z3_prove(task, wd):
    import z3
    a, b = z3.Ints("a b")
    s = z3.Solver()
    s.add(z3.Not(a + b == b + a))
    proved = s.check() == z3.unsat
    s2 = z3.Solver()
    s2.add(a * a == 49, a < 0)
    s2.check()
    av = s2.model()[a].as_long()
    # a program property: abs(x) >= 0 for 8-bit two's complement fails at -128 (counterexample)
    v = z3.BitVec("v", 8)
    s3 = z3.Solver()
    absv = z3.If(v < 0, -v, v)
    s3.add(z3.Not(absv >= 0))
    cex = s3.check() == z3.sat and s3.model()[v].as_signed_long()
    s4 = z3.Solver()
    s4.add(z3.Not(a + b == a))
    false_claim_sat = s4.check() == z3.sat
    out = jw(Path(wd) / "proofs.json", {"commutativity": proved, "a": av, "abs8_counterexample": cex})
    return [check("a+b = b+a proved (negation unsat)", proved),
            check("a^2 = 49 and a < 0 gives a = -7", av == -7, av, -7),
            check("8-bit abs(v) >= 0 has the counterexample -128", cex == -128, cex, -128),
            check("negative control: the false claim a+b = a has a counterexample", false_claim_sat)], [out]


@card("ANLY-33")
def duckdb_large(task, wd):
    import duckdb
    import numpy as np
    n = 100_000
    k = (np.arange(n) * 7919) % 7
    v = (np.arange(n) % 101).astype(float)
    p = Path(wd) / "rows.csv"
    with open(p, "w") as f:
        f.write("k,v\n")
        f.write("\n".join("g%d,%d" % (a, b) for a, b in zip(k, v)))
        f.write("\n")
    con = duckdb.connect()
    rows = con.sql("SELECT k, SUM(v) s, COUNT(*) c FROM read_csv('%s', header=true) GROUP BY k ORDER BY k" % p).fetchall()
    exp = {"g%d" % i: float(v[k == i].sum()) for i in range(7)}
    got = {r[0]: float(r[1]) for r in rows}
    out = Path(wd) / "groups.parquet"
    con.sql("COPY (SELECT k, SUM(v) s FROM read_csv('%s', header=true) GROUP BY k) TO '%s' (FORMAT parquet)" % (p, out))
    raw = con.execute("SELECT COUNT(*) FROM read_csv('%s', header=true)" % p).fetchall()[0][0]
    return [check("group-by over 100k rows gives 7 groups", len(rows) == 7, len(rows), 7),
            check("group sums equal numpy", got == exp),
            check("counts add to 100k", sum(r[2] for r in rows) == n, sum(r[2] for r in rows), n),
            check("negative control: ungrouped scan returns 100k rows, not 7", raw == n and raw != 7, raw)], [out]


@card("ANLY-34")
def polars_clean(task, wd):
    import polars as pl
    p = Path(wd) / "dirty.csv"
    lines = ["name,amount"]
    exp = {}
    for i in range(400):
        nm = ["  a", "b ", " c "][i % 3]
        if i % 10 == 0:
            lines.append("%s," % nm)  # missing amount
            continue
        amt = i % 9
        lines.append("%s,%d" % (nm, amt))
        if amt > 2:
            exp[nm.strip()] = exp.get(nm.strip(), 0) + amt
    p.write_text("\n".join(lines) + "\n")
    lf = (pl.scan_csv(p).drop_nulls("amount").with_columns(pl.col("name").str.strip_chars())
          .filter(pl.col("amount") > 2).group_by("name").agg(pl.col("amount").sum()).sort("name"))
    plan = lf.explain()
    df = lf.collect()
    got = dict(zip(df["name"].to_list(), df["amount"].to_list()))
    out = Path(wd) / "clean.csv"
    df.write_csv(out)
    rawk = sorted(set(pl.read_csv(p)["name"].to_list()))
    return [check("cleaned lazy aggregate equals python", got == exp, got, exp),
            check("three clean keys after strip", sorted(got) == ["a", "b", "c"], sorted(got)),
            check("optimised plan pushes the filter into the CSV scan", "SELECTION" in plan.upper() or "FILTER" in plan.upper()),
            check("negative control: raw keys still carry whitespace", rawk != ["a", "b", "c"], rawk)], [out]


@card("ANLY-35")
def sklearn_cv(task, wd):
    import numpy as np
    from sklearn.datasets import load_iris
    from sklearn.dummy import DummyClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import cross_val_score
    X, y = load_iris(return_X_y=True)
    rf = RandomForestClassifier(n_estimators=100, random_state=0)
    acc = float(cross_val_score(rf, X, y, cv=5).mean())
    rf.fit(X, y)
    imp = permutation_importance(rf, X, y, n_repeats=5, random_state=0).importances_mean
    top = int(np.argmax(imp))
    dummy = float(cross_val_score(DummyClassifier(), X, y, cv=5).mean())
    out = jw(Path(wd) / "cv.json", {"rf_5fold": acc, "importances": imp.tolist(), "dummy": dummy})
    return [check("RandomForest 5-fold accuracy ~0.96", 0.93 <= acc <= 1.0, acc, 0.96),
            check("explanation: a petal feature is most important", top in (2, 3), top, "2 or 3"),
            check("negative control: the dummy classifier scores ~0.33", dummy < 0.4, dummy, "< 0.4")], [out]


@card("ANLY-36")
def statsforecast_intervals(task, wd):
    import numpy as np
    import pandas as pd
    from statsforecast import StatsForecast
    from statsforecast.models import AutoARIMA, AutoETS
    rng = np.random.default_rng(5)
    n = 60
    frames = []
    truth = {}
    for uid, base in (("s1", 100), ("s2", 300)):
        t = np.arange(n + 6)
        y = base + 0.8 * t + 8 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 1.0, n + 6)
        truth[uid] = y[n:]
        frames.append(pd.DataFrame({"unique_id": uid, "ds": pd.date_range("2020-01-01", periods=n, freq="MS"), "y": y[:n]}))
    df = pd.concat(frames)
    sf = StatsForecast(models=[AutoETS(season_length=12), AutoARIMA(season_length=12)], freq="MS")
    fc = sf.forecast(df=df, h=6, level=[80])
    out = Path(wd) / "forecast.csv"
    fc.to_csv(out, index=False)
    cover, err, flat = 0, [], []
    for uid in truth:
        f = fc[fc.unique_id == uid]
        lo, hi, mu = f["AutoETS-lo-80"].values, f["AutoETS-hi-80"].values, f["AutoETS"].values
        cover += int(((truth[uid] >= lo) & (truth[uid] <= hi)).sum())
        err.append(float(np.mean(np.abs(mu - truth[uid]))))
        flat.append(float(np.mean(np.abs(df[df.unique_id == uid].y.values[-1] - truth[uid]))))
    ordered = bool((fc["AutoETS-lo-80"] < fc["AutoETS"]).all() and (fc["AutoETS"] < fc["AutoETS-hi-80"]).all())
    return [check("6-step forecasts for both series and both models", len(fc) == 12 and {"AutoARIMA", "AutoETS"} <= set(fc.columns), len(fc), 12),
            check("80% interval brackets the point forecast", ordered),
            check("80% interval covers >= 7 of 12 held-out months", cover >= 7, cover, ">= 7"),
            check("mean absolute error beats the last-value forecast", max(err) < min(flat), err, flat),
            check("negative control: last-value forecast error > 3", min(flat) > 3, flat, "> 3")], [out]


@card("ANLY-37")
def geopandas_buffer(task, wd):
    import geopandas as gpd
    from shapely.geometry import Point
    g = gpd.GeoDataFrame({"name": ["Cairo"]}, geometry=[Point(31.2357, 30.0444)], crs="EPSG:4326")
    utm = g.to_crs(32636)
    buf = utm.buffer(1000, resolution=128)
    area_km2 = float(buf.area.iloc[0]) / 1e6
    back = gpd.GeoDataFrame({"name": ["Cairo 1 km"]}, geometry=buf.to_crs(4326), crs="EPSG:4326")
    b = back.total_bounds
    out = Path(wd) / "cairo_buffer.geojson"
    back.to_file(out, driver="GeoJSON")
    pts = gpd.GeoDataFrame({"id": [1, 2]}, geometry=[Point(31.2357, 30.0480), Point(31.2600, 30.0444)], crs=4326).to_crs(32636)
    joined = gpd.sjoin(pts, gpd.GeoDataFrame(geometry=buf, crs=32636), predicate="within")
    deg_area = float(g.buffer(0.009).area.iloc[0])
    return [check("1 km buffer in UTM 36N has area pi km2", abs(area_km2 - math.pi) < 0.002, area_km2, math.pi),
            check("longitude span ~0.0207 deg", abs((b[2] - b[0]) - 0.0207) < 0.0005, b[2] - b[0], 0.0207),
            check("spatial join keeps only the point 400 m away", joined["id"].tolist() == [1], joined["id"].tolist(), [1]),
            check("GeoJSON exported", json.loads(out.read_text())["type"] == "FeatureCollection"),
            check("negative control: a buffer in degrees is not a km2 area", abs(deg_area - math.pi) > 1, deg_area)], [out]


@card("ANLY-38")
def biopython_seq(task, wd):
    from Bio import Align, SeqIO
    from Bio.SeqUtils import gc_fraction
    fa = tw(Path(wd) / "genes.fasta", ">g1 test\nATGGCCATTGTAATGGGCCGCTGA\n>g2 mut\nATGGCCATTGTTATGGGCCGCTGA\n")
    recs = list(SeqIO.parse(fa, "fasta"))
    prot = str(recs[0].seq.translate(to_stop=True))
    gc = round(gc_fraction(recs[0].seq), 2)
    al = Align.PairwiseAligner()
    al.match_score, al.mismatch_score = 1, 0
    score = al.score(recs[0].seq, recs[1].seq)
    gb = Path(wd) / "g1.gb"
    recs[0].annotations["molecule_type"] = "DNA"
    SeqIO.write(recs[0], gb, "genbank")
    back = SeqIO.read(gb, "genbank")
    return [check("translation MAIVMGR", prot == "MAIVMGR", prot, "MAIVMGR"),
            check("GC fraction 0.54", gc == 0.54, gc, 0.54),
            check("alignment: 23 of 24 bases match", score == 23, score, 23),
            check("GenBank round trip keeps the sequence", str(back.seq) == str(recs[0].seq)),
            check("negative control: the raw DNA string is not the protein", str(recs[0].seq) != "MAIVMGR")], [gb]


@card("ANLY-39")
def rdkit_mol(task, wd):
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Draw
    asp = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
    mw = round(Descriptors.MolWt(asp), 2)
    heavy = asp.GetNumHeavyAtoms()
    out = Path(wd) / "aspirin.png"
    Draw.MolToImage(asp, size=(300, 300)).save(out)
    img = load_rgb(out)
    benz = round(Descriptors.MolWt(Chem.MolFromSmiles("c1ccccc1")), 2)
    return [check("aspirin MW 180.16", mw == 180.16, mw, 180.16),
            check("13 heavy atoms", heavy == 13, heavy, 13),
            check("molecule drawn (ink on the image)", (img.min(axis=-1) < 128).mean() > 0.01, float((img.min(axis=-1) < 128).mean())),
            check("negative control: benzene is not 180.16", benz != 180.16, benz)], [out]


# =============================================================================================== APPX


def index_clip(wd, name, n, fps=30, w=160, h=90):
    """A clip whose frame i is painted with gray level 4*(i % 60) plus a binary code of i in 8 blocks."""
    np = _np()
    frames = []
    for i in range(n):
        f = np.full((h, w, 3), 0.0)
        f[:h // 2] = (i * 4) % 240
        for b in range(8):
            f[h // 2:, b * (w // 8):(b + 1) * (w // 8)] = 255.0 if (i >> b) & 1 else 0.0
        frames.append(f)
    return write_video(Path(wd) / name, frames, fps)


def frame_index(f):
    h, w = f.shape[:2]
    bits = [f[3 * h // 4, b * (w // 8) + w // 16].mean() > 127 for b in range(8)]
    return sum(1 << b for b, on in enumerate(bits) if on)


@card("APPX-01")
def speed_ramp(task, wd):
    src = index_clip(wd, "src.mp4", 180)
    out = Path(wd) / "ramp.mp4"
    fx.ffmpeg("-i", src, "-filter_complex",
              "[0:v]trim=0:2,setpts=PTS-STARTPTS[a];[0:v]trim=2:4,setpts=2*(PTS-STARTPTS)[b];"
              "[0:v]trim=4:6,setpts=0.5*(PTS-STARTPTS)[c];[a][b][c]concat=n=3:v=1:a=0,fps=30[v]",
              "-map", "[v]", "-c:v", "libx264rgb", "-qp", "0", out)
    fr = read_video(out)
    idx = [frame_index(f) for f in fr]
    d = len(fr) / 30.0
    mid_b = idx[90]       # 3.0 s out = 1 s into the slow segment = source 2.5 s (frame 75)
    mid_c = idx[6 * 30 + 15]  # 6.5 s out = 0.5 s into the fast segment = source 5 s (frame 150)
    return [check("output duration 2 + 4 + 1 = 7 s (setpts factor = 1/speed)", abs(d - 7.0) < 0.07, d, 7.0),
            check("slow segment: output 3.0 s shows source frame 75 (half speed)", abs(mid_b - 75) <= 1, mid_b, 75),
            check("fast segment: output 6.5 s shows source frame 150 (double speed)", abs(mid_c - 150) <= 2, mid_c, 150),
            check("negative control: the untreated clip lasts 6 s", abs(duration(src) - 7.0) > 0.5, duration(src), "!= 7")], [out]


@card("APPX-02")
def chroma_key(task, wd):
    np = _np()
    fg = np.zeros((90, 160, 3))
    fg[:] = (0, 255, 0)
    fg[30:60, 60:100] = (220, 30, 30)
    bg = np.zeros((90, 160, 3))
    bg[:] = (20, 40, 200)
    pf, pb = write_video(Path(wd) / "fg.mp4", [fg] * 15), write_video(Path(wd) / "bg.mp4", [bg] * 15)
    out = Path(wd) / "key.mp4"
    fx.ffmpeg("-i", pb, "-i", pf, "-filter_complex",
              "[1:v]format=rgba,chromakey=0x00FF00:0.15:0.05[k];[0:v][k]overlay,format=rgb24", "-c:v", "libx264rgb", "-qp", "0", out)
    f = read_video(out)[5]
    nokey = Path(wd) / "nokey.mp4"
    fx.ffmpeg("-i", pb, "-i", pf, "-filter_complex", "[0:v][1:v]overlay,format=rgb24", "-c:v", "libx264rgb", "-qp", "0", nokey)
    g = read_video(nokey)[5]
    green = float(color_mask(f, (0, 255, 0), 60).mean())
    return [check("background shows through where the screen was green", color_mask(f[5:20, 5:40], (20, 40, 200), 25).mean() > 0.98),
            check("subject kept (red block)", color_mask(f[38:52, 70:90], (220, 30, 30), 30).mean() > 0.98),
            check("no green left in the frame", green < 0.005, green, "< 0.005"),
            check("negative control: overlay without the key keeps the green", color_mask(g, (0, 255, 0), 60).mean() > 0.5)], [out]


@card("APPX-03")
def auto_reframe(task, wd):
    np = _np()
    W, H, n = 640, 360, 60
    frames = []
    xs = []
    for i in range(n):
        f = np.full((H, W, 3), 30.0)
        cx = 120 + i * (400 / (n - 1))
        xs.append(cx)
        yy, xx = np.mgrid[0:H, 0:W]
        f[(xx - cx) ** 2 + (yy - 180) ** 2 < 30 ** 2] = 240
        frames.append(f)
    src = write_video(Path(wd) / "wide.mp4", frames)
    fr = read_video(src)
    cw = int(round(H * 9 / 16)) // 2 * 2  # even crop width (202 for 360p; 404 for 720p)
    cms = []
    for f in fr:
        g = f.mean(axis=-1)
        m = g > 128
        cms.append(float(np.nonzero(m)[1].mean()))
    k = 9
    pad = np.pad(np.array(cms), (k // 2, k // 2), mode="edge")
    smooth = np.convolve(pad, np.ones(k) / k, mode="valid")
    crops = []
    for f, c in zip(fr, smooth):
        x0 = int(round(min(max(c - cw / 2, 0), W - cw)))
        crops.append(f[:, x0:x0 + cw])
    out = write_video(Path(wd) / "reframed.mp4", crops)
    rf = read_video(out)
    offs = [abs(np.nonzero(f.mean(axis=-1) > 128)[1].mean() - cw / 2) for f in rf]
    centre = [abs(cms[i] - (W / 2 - cw / 2) - cw / 2) for i in (0, n - 1)]
    return [check("crop width is even and 9:16", cw % 2 == 0 and abs(cw / H - 9 / 16) < 0.01, cw),
            check("subject stays within 12 px of the crop centre", max(offs) < 12, max(offs), "< 12"),
            check("output frame count kept", len(rf) == n, len(rf), n),
            check("negative control: a fixed centre crop leaves the subject > 100 px off", min(centre) > 100, centre)], [out]


@card("APPX-04")
def scene_detect(task, wd):
    parts = []
    for i, c in enumerate(["black", "white", "0x3040c0"]):
        parts.append(fx.color_clip(Path(wd) / ("c%d.mp4" % i), c, 1.0, "160x90"))
    lst = tw(Path(wd) / "list.txt", "".join("file '%s'\n" % p for p in parts))
    src = Path(wd) / "cuts.mp4"
    fx.ffmpeg("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", src)

    def cuts(p):
        e = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"],
                           capture_output=True, text=True, timeout=60).stderr
        return [round(float(t), 3) for t in re.findall(r"pts_time:([0-9.]+)", e)]
    got = cuts(src)
    out = jw(Path(wd) / "scenes.json", {"cuts_s": got, "threshold": 0.3})
    return [check("two cuts found at 1.0 s and 2.0 s", len(got) == 2 and abs(got[0] - 1) < 0.05 and abs(got[1] - 2) < 0.05, got, [1.0, 2.0]),
            check("negative control: a single-colour clip has no cut", cuts(parts[0]) == [], cuts(parts[0]))], [out]


def _ebur(p):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=60).stderr
    i = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", e)[-1])
    tp = re.findall(r"Peak:\s+(-?[0-9.]+) dBFS", e)
    return i, float(tp[-1]) if tp else None


@card("APPX-05")
def loudnorm_two_pass(task, wd):
    np = _np()
    sr = 48000
    t = np.arange(sr * 6) / sr
    sig = 0.05 * np.sin(2 * np.pi * 220 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t)) + 0.02 * np.sin(2 * np.pi * 1300 * t)
    src = fx.write_wav(Path(wd) / "quiet.wav", sig, sr)
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True, timeout=60).stderr
    m = json.loads(e[e.rindex("{"):e.rindex("}") + 1])
    out = Path(wd) / "norm.wav"
    fx.ffmpeg("-i", src, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:"
              "offset=%s:linear=true,aresample=48000" % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"],
                                                       m["target_offset"]), out)
    i_out, tp_out = _ebur(out)
    i_in, _ = _ebur(src)
    return [check("integrated loudness -14 LUFS (ebur128)", abs(i_out + 14) <= 1.0, i_out, -14),
            check("true peak at or under -1.5 dBTP (+0.3 tolerance)", tp_out is not None and tp_out <= -1.2, tp_out, "<= -1.5"),
            check("negative control: the input is far from -14 LUFS", abs(i_in + 14) > 5, i_in, "!= -14")], [out]


@card("APPX-06")
def lut3d_look(task, wd):
    np = _np()
    n = 17
    lines = ["TITLE \"warm\"", "LUT_3D_SIZE %d" % n]
    for b in range(n):
        for g in range(n):
            for r in range(n):
                R, G, B = r / (n - 1), g / (n - 1), b / (n - 1)
                lines.append("%.6f %.6f %.6f" % (min(1, R * 1.1 + 0.05), G, B * 0.8))
    cube = tw(Path(wd) / "warm.cube", "\n".join(lines) + "\n")
    f = np.zeros((90, 160, 3))
    f[:] = (128, 128, 128)
    src = write_video(Path(wd) / "gray.mp4", [f] * 10)
    out = Path(wd) / "graded.mp4"
    fx.ffmpeg("-i", src, "-vf", "format=rgb24,lut3d=file=%s" % cube, "-c:v", "libx264rgb", "-qp", "0", out)
    px = read_video(out)[3][45, 80]
    exp = (min(255, 128 * 1.1 + 0.05 * 255), 128, 128 * 0.8)
    s_in = read_video(src)[3][45, 80]
    return [check("17^3 cube written", len(lines) == 2 + n ** 3, len(lines) - 2, n ** 3),
            check("graded pixel equals the curve (R*1.1+0.05, G, B*0.8)", all(abs(a - b) <= 2 for a, b in zip(px, exp)), px.tolist(), exp),
            check("negative control: the source pixel is neutral grey", all(abs(a - b) <= 2 for a, b in zip(s_in, exp)) is False, s_in.tolist())], [out]


@card("APPX-07")
def remove_pauses(task, wd):
    np = _np()
    sr = 44100
    t = np.arange(sr) / sr
    tone = 0.4 * np.sin(2 * np.pi * 440 * t)
    sig = np.r_[tone, np.zeros(sr), tone]
    src = fx.write_wav(Path(wd) / "talk.wav", sig, sr)
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", "silencedetect=n=-40dB:d=0.5", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=60).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", e)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", e)]
    out = Path(wd) / "tight.wav"
    fx.ffmpeg("-i", src, "-af", "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-40dB", out)
    d = duration(out)
    rep = jw(Path(wd) / "silences.json", {"start": st, "end": en, "out_duration": d})
    return [check("silence reported from 1.0 s to 2.0 s", st and en and abs(st[0] - 1) < 0.05 and abs(en[0] - 2) < 0.05, [st, en]),
            check("pause removed: output about 2.0-2.5 s", 1.95 <= d <= 2.55, d, "2.0-2.5"),
            check("negative control: the input lasts 3 s", abs(duration(src) - 3) < 0.01 and duration(src) > 2.55, duration(src))], [out, rep]


def beat_bpm(x, sr, hop=256, gap=0.2):
    np = _np()
    n = len(x) // hop
    e = np.array([np.sum(x[i * hop:(i + 1) * hop] ** 2) for i in range(n)])
    flux = np.maximum(0, np.diff(e, prepend=e[0]))
    thr = flux.mean() + 2 * flux.std()
    peaks, last = [], -1e9
    for i in range(1, n - 1):
        if flux[i] > thr and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1] and (i - last) * hop / sr >= gap:
            peaks.append(i * hop / sr)
            last = i
    if len(peaks) < 3:
        return None, peaks
    return 60.0 / float(np.median(np.diff(peaks))), peaks


@card("APPX-08")
def auto_beat(task, wd):
    np = _np()
    sr = 22050
    x = np.zeros(sr * 8)
    rng = np.random.default_rng(2)
    for k in range(16):
        s = int((0.25 + k * 0.5) * sr)
        x[s:s + 800] += np.exp(-np.arange(800) / 120) * rng.uniform(-1, 1, 800) * 0.8
    x += 0.1 * np.sin(2 * np.pi * 110 * np.arange(len(x)) / sr)
    src = fx.write_wav(Path(wd) / "beat.wav", x, sr)
    y, _ = fx.read_wav(src)
    bpm, peaks = beat_bpm(y[:, 0], sr)
    out = jw(Path(wd) / "beats.json", {"bpm": bpm, "beats_s": peaks})
    flat = 0.1 * np.sin(2 * np.pi * 110 * np.arange(sr * 8) / sr)
    bpm0, _ = beat_bpm(flat, sr)
    return [check("BPM 120 from energy flux peaks", bpm is not None and abs(bpm - 120) < 2, bpm, 120),
            check("16 beats found, the first at 0.25 s", len(peaks) == 16 and abs(peaks[0] - 0.25) < 0.02, [len(peaks), peaks[:1]]),
            check("negative control: a steady tone yields no tempo", bpm0 is None, bpm0)], [out]


@card("APPX-09")
def camera_bubble(task, wd):
    np = _np()
    scr = np.full((360, 640, 3), 90.0)
    cam = np.zeros((160, 160, 3))
    cam[:] = (230, 40, 40)
    ps, pc = write_video(Path(wd) / "screen.mp4", [scr] * 10), write_video(Path(wd) / "cam.mp4", [cam] * 10)
    R = 80
    out = Path(wd) / "bubble.mp4"
    fx.ffmpeg("-i", ps, "-i", pc, "-filter_complex",
              "[1:v]format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte(hypot(X-%d,Y-%d),%d),255,0)'[c];"
              "[0:v][c]overlay=W-w-40:H-h-40,format=rgb24" % (R, R, R - 2), "-c:v", "libx264rgb", "-qp", "0", out)
    f = read_video(out)[4]
    x0, y0 = 640 - 160 - 40, 360 - 160 - 40
    centre = f[y0 + 80, x0 + 80]
    corner = f[y0 + 6, x0 + 6]
    raw = Path(wd) / "square.mp4"
    fx.ffmpeg("-i", ps, "-i", pc, "-filter_complex", "[0:v][1:v]overlay=W-w-40:H-h-40,format=rgb24", "-c:v", "libx264rgb", "-qp", "0", raw)
    g = read_video(raw)[4][y0 + 6, x0 + 6]
    margin = 640 - (ink_bbox(f, (90, 90, 90), 30)[2])
    return [check("camera visible at the bubble centre", abs(centre[0] - 230) < 6 and centre[1] < 50, centre.tolist()),
            check("square corner outside the circle shows the screen", abs(corner - 90).max() < 6, corner.tolist()),
            check("40 px margin from the right edge", abs(margin - 40) <= 3, margin, 40),
            check("negative control: without the alpha mask the corner is camera red", g[0] > 200, g.tolist())], [out]


@card("APPX-10")
def zoompan_keyframes(task, wd):
    np = _np()
    img = np.full((360, 640, 3), 255.0)
    img[130:230, 270:370] = 0
    src = save_png(img, Path(wd) / "still.png")
    out = Path(wd) / "zoom.mp4"
    fx.ffmpeg("-i", src, "-vf", "zoompan=z='min(1+0.004*on,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=640x360:fps=30,format=rgb24",
              "-c:v", "libx264rgb", "-qp", "0", out)
    fr = read_video(out)

    def width(f):
        b = ink_bbox(f, (255, 255, 255), 128)
        return b[2] - b[0]
    w0, w60, w140 = width(fr[0]), width(fr[60]), width(fr[140])
    return [check("frame 0 square 100 px", abs(w0 - 100) <= 2, w0, 100),
            check("frame 60 zoom 1.24 -> 124 px", abs(w60 - 124) <= 3, w60, 124),
            check("zoom capped at 1.5 -> 150 px", abs(w140 - 150) <= 3, w140, 150),
            check("negative control: the still keeps 100 px", abs(width(img) - 124) > 10, width(img))], [out]


def band_rms(x, sr, f0, t0, t1):
    np = _np()
    seg = x[int(t0 * sr):int(t1 * sr)]
    t = np.arange(len(seg)) / sr
    c = np.mean(seg * np.cos(2 * np.pi * f0 * t)) * 2
    s = np.mean(seg * np.sin(2 * np.pi * f0 * t)) * 2
    return math.hypot(c, s)


@card("APPX-11")
def auto_ducking(task, wd):
    np = _np()
    sr = 44100
    t = np.arange(sr * 3) / sr
    music = 0.3 * np.sin(2 * np.pi * 220 * t)
    voice = np.where((t >= 1) & (t < 2), 0.5 * np.sin(2 * np.pi * 1000 * t), 0)
    pm, pv = fx.write_wav(Path(wd) / "music.wav", music, sr), fx.write_wav(Path(wd) / "voice.wav", voice, sr)
    out = Path(wd) / "ducked.wav"
    fx.ffmpeg("-i", pv, "-i", pm, "-filter_complex",
              "[0:a]asplit[sc][v];[1:a][sc]sidechaincompress=threshold=0.02:ratio=12:attack=20:release=300[m];"
              "[m][v]amix=inputs=2:normalize=0", out)
    y, _ = fx.read_wav(out)
    y = y[:, 0]
    before, during = band_rms(y, sr, 220, 0.3, 0.9), band_rms(y, sr, 220, 1.3, 1.9)
    duck_db = 20 * math.log10(during / before)
    vkeep = band_rms(y, sr, 1000, 1.3, 1.9)
    m0 = 20 * math.log10(band_rms(music, sr, 220, 1.3, 1.9) / band_rms(music, sr, 220, 0.3, 0.9))
    return [check("music ducks by more than 6 dB under the voice", duck_db < -6, duck_db, "< -6 dB"),
            check("voice passes at full level", abs(vkeep - 0.5) < 0.05, vkeep, 0.5),
            check("music recovers after the release", band_rms(y, sr, 220, 2.6, 2.95) > 0.8 * before),
            check("negative control: the untreated music level is flat", abs(m0) < 0.5 and not m0 < -6, m0)], [out]


@card("APPX-12")
def denoise(task, wd):
    np = _np()
    sr = 44100
    rng = np.random.default_rng(4)
    t = np.arange(sr * 3) / sr
    clean = np.where(t >= 1.5, 0.4 * np.sin(2 * np.pi * 440 * t), 0)
    noisy = clean + rng.normal(0, 0.03, len(t))
    src = fx.write_wav(Path(wd) / "noisy.wav", noisy, sr)
    out = Path(wd) / "clean.wav"
    fx.ffmpeg("-i", src, "-af", "afftdn=nr=20:nf=-30,highpass=f=80,lowpass=f=12000", out)
    y, _ = fx.read_wav(out)
    y = y[:, 0]
    rms = lambda a: float(np.sqrt(np.mean(a ** 2)))  # noqa: E731
    n_in, n_out = rms(noisy[int(0.4 * sr):int(1.2 * sr)]), rms(y[int(0.4 * sr):int(1.2 * sr)])
    red = 20 * math.log10(n_out / n_in)
    tone = band_rms(y, sr, 440, 2.0, 2.8)
    return [check("noise floor reduced by more than 8 dB", red < -8, red, "< -8 dB"),
            check("speech-band tone preserved within 2 dB", abs(20 * math.log10(tone / 0.4)) < 2, tone, 0.4),
            check("negative control: the input noise floor is ~0.03", abs(n_in - 0.03) < 0.003, n_in)], [out]


@card("APPX-15")
def cmx3600_edl(task, wd):
    src = index_clip(wd, "reel.mp4", 150)
    fps = 30
    events = [(0, 30, "A"), (60, 105, "B"), (120, 150, "C")]  # source in/out frames

    def tc(fr):
        return "%02d:%02d:%02d:%02d" % (fr // (3600 * fps), fr // (60 * fps) % 60, fr // fps % 60, fr % fps)
    lines = ["TITLE: KOSIF CUT", "FCM: NON-DROP FRAME", ""]
    rec = 3600 * fps
    for n, (a, b, _) in enumerate(events, 1):
        lines.append("%03d  AX       V     C        %s %s %s %s" % (n, tc(a), tc(b), tc(rec), tc(rec + b - a)))
        lines.append("* FROM CLIP NAME: reel.mp4")
        rec += b - a
    edl = tw(Path(wd) / "cut.edl", "\n".join(lines) + "\n")
    parsed = re.findall(r"^(\d{3})\s+AX\s+V\s+C\s+(\S+) (\S+) (\S+) (\S+)$", edl.read_text(), re.M)

    def fr(t):
        h, m, s, f = map(int, t.split(":"))
        return ((h * 60 + m) * 60 + s) * fps + f
    fc = ";".join("[0:v]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS[v%d]" % (fr(a), fr(b), i)
                  for i, (_, a, b, _, _) in enumerate(parsed))
    fc += ";" + "".join("[v%d]" % i for i in range(len(parsed))) + "concat=n=%d:v=1:a=0[o]" % len(parsed)
    out = Path(wd) / "rebuilt.mp4"
    fx.ffmpeg("-i", src, "-filter_complex", fc, "-map", "[o]", "-c:v", "libx264rgb", "-qp", "0", out)
    frs = read_video(out)
    idx = [frame_index(f) for f in frs]
    contiguous = all(fr(parsed[i][4]) == fr(parsed[i + 1][3]) for i in range(len(parsed) - 1))
    return [check("three CMX3600 events parse back", len(parsed) == 3, len(parsed), 3),
            check("record timecodes are contiguous from 01:00:00:00", contiguous and parsed[0][3] == "01:00:00:00"),
            check("rebuilt duration 105 frames (3.5 s)", len(frs) == 105, len(frs), 105),
            check("cut points land on source frames 29 -> 60 and 104 -> 120", idx[29] == 29 and idx[30] == 60 and idx[75] == 120,
                  [idx[29], idx[30], idx[75]]),
            check("negative control: the untreated reel is 150 frames", len(read_video(src)) == 150 != 105)], [edl, out]


@card("APPX-16")
def reverse_freeze(task, wd):
    src = index_clip(wd, "clip.mp4", 120)
    out = Path(wd) / "revfreeze.mp4"
    fx.ffmpeg("-i", src, "-vf", "trim=0:2,setpts=PTS-STARTPTS,reverse,tpad=stop_mode=clone:stop_duration=1",
              "-c:v", "libx264rgb", "-qp", "0", out)
    idx = [frame_index(f) for f in read_video(out)]
    return [check("3 s out: 2 s reversed + 1 s freeze", len(idx) == 90, len(idx), 90),
            check("starts on source frame 59 and runs backwards", idx[0] == 59 and idx[30] == 29 and idx[59] == 0, idx[:1] + [idx[30], idx[59]]),
            check("last 30 frames are the frozen frame 0", set(idx[60:]) == {0}, sorted(set(idx[60:]))),
            check("negative control: the source starts on frame 0", frame_index(read_video(src)[0]) == 0 != idx[0])], [out]


@card("APPX-17")
def cover_pick(task, wd):
    np = _np()
    import cv2
    rng = np.random.default_rng(8)
    frames = []
    for seg in range(12):
        if seg == 7:
            base = texture(160, 90, seed=3)
            base[:, :, 0] = base[:, :, 0] * 0.3 + 170
        else:
            base = cv2.GaussianBlur(texture(160, 90, seed=seg).astype("float32"), (0, 0), 6) * 0.4 + 60
            base = np.dstack([base.mean(axis=-1)] * 3)
        frames += [base + rng.normal(0, 0.5, base.shape)] * 10
    src = write_video(Path(wd) / "talk.mp4", frames)
    fr = read_video(src)
    picks = np.linspace(0, len(fr) - 1, 16).astype(int)

    def score(f):
        g = cv2.cvtColor(f.astype("float32"), cv2.COLOR_RGB2GRAY)
        return float(cv2.Laplacian(g, cv2.CV_32F).var()) + float(f.std(axis=-1).mean()) * 10
    scores = [score(fr[i]) for i in picks]
    best = int(picks[int(np.argmax(scores))])
    out = save_png(fr[best], Path(wd) / "cover.png")
    return [check("16 sampled frames scored", len(scores) == 16),
            check("picked frame lies in the sharp colourful segment (frames 70-79)", 70 <= best <= 79, best, "70-79"),
            check("negative control: the first frame scores lower", score(fr[0]) < max(scores) / 2, score(fr[0]), max(scores))], [out]


def _tiny_pe():
    """A minimal PE32+ image (one .text section with `ret`), built byte by byte; returns bytes."""
    import struct
    dos = bytearray(64)
    dos[0:2] = b"MZ"
    struct.pack_into("<I", dos, 0x3C, 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 1, 0, 0, 0, 240, 0x22)
    opt = bytearray(240)
    struct.pack_into("<HBBIIIII", opt, 0, 0x20B, 14, 0, 0x200, 0, 0, 0x1000, 0x1000)
    struct.pack_into("<Q", opt, 24, 0x140000000)
    struct.pack_into("<II", opt, 32, 0x1000, 0x200)
    struct.pack_into("<HHHHHH", opt, 40, 6, 0, 0, 0, 6, 0)
    struct.pack_into("<IIII", opt, 52, 0, 0x2000, 0x200, 0)   # Win32Version, SizeOfImage, SizeOfHeaders, CheckSum
    struct.pack_into("<HH", opt, 68, 3, 0x8160)
    struct.pack_into("<QQQQII", opt, 72, 0x100000, 0x1000, 0x100000, 0x1000, 0, 16)
    sec = struct.pack("<8sIIIIIIHHI", b".text", 0x200, 0x1000, 0x200, 0x200, 0, 0, 0, 0, 0x60000020)
    hdr = bytes(dos) + b"PE\0\0" + coff + bytes(opt) + sec
    hdr += b"\0" * (0x200 - len(hdr))
    body = b"\xC3" + b"KOSIF-APPX30-TEST" + b"\0" * (0x200 - 18)
    return bytearray(hdr + body)


_OPT = 0x40 + 4 + 20
_CHECKSUM, _SECDIR = _OPT + 64, _OPT + 112 + 4 * 8


def _authenticode_digest(pe: bytes) -> bytes:
    """Authenticode-style SHA-256: the file minus CheckSum, the security directory entry and the certificate table."""
    import hashlib
    import struct
    off, size = struct.unpack_from("<II", pe, _SECDIR)
    end = off if off else len(pe)
    h = hashlib.sha256()
    h.update(pe[:_CHECKSUM])
    h.update(pe[_CHECKSUM + 4:_SECDIR])
    h.update(pe[_SECDIR + 8:end])
    return h.digest()


def _sign_pe(wd, pe):
    import struct
    key, crt = Path(wd) / "key.pem", Path(wd) / "cert.pem"
    run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", key, "-out", crt, "-days", "2",
         "-subj", "/CN=KOSIF test signer"])
    dg = Path(wd) / "digest.bin"
    dg.write_bytes(_authenticode_digest(bytes(pe)))
    sig = Path(wd) / "sig.der"
    run(["openssl", "cms", "-sign", "-binary", "-nodetach", "-in", dg, "-signer", crt, "-inkey", key, "-outform", "DER", "-out", sig])
    blob = sig.read_bytes()
    cert = struct.pack("<IHH", 8 + len(blob), 0x0200, 0x0002) + blob
    cert += b"\0" * (-len(cert) % 8)
    off = len(pe)
    struct.pack_into("<II", pe, _SECDIR, off, len(cert))
    return bytearray(bytes(pe) + cert), crt


def _verify_pe(wd, path, crt):
    """osslsigncode-style verify: parse WIN_CERTIFICATE, verify the CMS signature, compare the signed digest."""
    import struct
    pe = Path(path).read_bytes()
    off, size = struct.unpack_from("<II", pe, _SECDIR)
    if not off:
        return {"signed": False, "valid": False}
    ln, rev, typ = struct.unpack_from("<IHH", pe, off)
    der = Path(wd) / (Path(path).stem + ".p7")
    der.write_bytes(pe[off + 8:off + ln])
    got = Path(wd) / (Path(path).stem + ".content")
    done = subprocess.run(["openssl", "cms", "-verify", "-binary", "-inform", "DER", "-in", str(der), "-CAfile", str(crt),
                           "-purpose", "any", "-out", str(got)], capture_output=True, text=True, timeout=30)
    sig_ok = done.returncode == 0
    digest_ok = sig_ok and got.read_bytes() == _authenticode_digest(pe)
    return {"signed": True, "revision": hex(rev), "type": typ, "signature_ok": sig_ok, "digest_ok": digest_ok,
            "valid": sig_ok and digest_ok}


@card("APPX-30")
def authenticode_verify(task, wd):
    triage = SP / "scripts/installer_triage.py"
    raw = _tiny_pe()
    unsigned = Path(wd) / "tiny_unsigned.exe"
    unsigned.write_bytes(bytes(raw))
    signed_b, crt = _sign_pe(wd, bytearray(raw))
    signed = Path(wd) / "tiny_signed.exe"
    signed.write_bytes(bytes(signed_b))
    tampered = Path(wd) / "tiny_tampered.exe"
    tb = bytearray(signed_b)
    tb[0x201] ^= 0x20  # one byte of code changed after signing
    tampered.write_bytes(bytes(tb))
    v_s, v_t, v_u = (_verify_pe(wd, p, crt) for p in (signed, tampered, unsigned))

    def scan(p):
        r = json.loads(run([sys.executable, triage, "scan", p], timeout=60).stdout)
        a = r["artifacts"][0]
        return {"slot": a.get("pe", {}).get("authenticode_slot", {}).get("present"),
                "unsigned_flag": any(f.get("kind") == "signature" and f.get("value") == "unsigned" for f in a.get("findings", []))}
    s_s, s_u = scan(signed), scan(unsigned)
    rep = jw(Path(wd) / "authenticode.json", {"signed": v_s, "tampered": v_t, "unsigned": v_u, "triage_signed": s_s,
                                              "triage_unsigned": s_u, "executed_target": False})
    return [check("signed copy: CMS signature and Authenticode digest both verify", v_s["valid"], v_s),
            check("WIN_CERTIFICATE revision 0x200, type PKCS_SIGNED_DATA", v_s.get("revision") == "0x200" and v_s.get("type") == 2),
            check("one byte changed after signing breaks the digest", v_t["signed"] and v_t["signature_ok"] and not v_t["digest_ok"], v_t),
            check("installer_triage scan sees the signature slot only on the signed file", s_s["slot"] is True and s_u["unsigned_flag"], [s_s, s_u]),
            check("negative control: the unsigned file has no signature to verify", v_u == {"signed": False, "valid": False}, v_u)], [rep, signed]


def _photo(w=200, h=140):
    """A deterministic 'photo': gradient backdrop, an orange disc subject, a dark wire scratch."""
    np = _np()
    yy, xx = np.mgrid[0:h, 0:w]
    img = np.dstack([60 + 120 * xx / w, 120 + 60 * yy / h, 200 - 80 * xx / w])
    subj = (xx - 100) ** 2 + (yy - 75) ** 2 < 38 ** 2
    img[subj] = (240, 140, 30)
    return img, subj


@card("APPX-118")
def photoshop_open_equivalents(task, wd):
    np = _np()
    import cv2
    from PIL import Image
    doc = SP / "proofs/windows-installers-rea/PAINT_PHOTOSHOP_BLENDER_2026-10-20.md"
    names = doc.read_text(encoding="utf-8")
    img, subj = _photo()
    # Remove (CMGAN) -> classical inpainting of a wire scratch
    hurt = img.copy()
    wire = np.zeros(img.shape[:2], np.uint8)
    cv2.line(wire, (5, 20), (60, 130), 255, 3)
    hurt[wire > 0] = 10
    fixed = cv2.inpaint(hurt.astype(np.uint8), wire, 5, cv2.INPAINT_TELEA).astype(float)
    err_fixed = float(np.abs(fixed - img)[wire > 0].mean())
    err_hurt = float(np.abs(hurt - img)[wire > 0].mean())
    # Lens blur from a depth map (DepthPrediction): blur grows with |depth - focus|
    depth = np.where(subj, 0.2, 0.9)
    blurred = cv2.GaussianBlur(img.astype("float32"), (0, 0), 4)
    lens = img * (depth[..., None] < 0.5) + blurred * (depth[..., None] >= 0.5)
    g = lambda a: cv2.Laplacian(cv2.cvtColor(a.astype("float32"), cv2.COLOR_RGB2GRAY), cv2.CV_32F)  # noqa: E731
    bg_sharp_in = float(np.abs(g(texture(200, 140))).mean())
    tex = texture(200, 140)
    lens_t = tex * (depth[..., None] < 0.5) + cv2.GaussianBlur(tex.astype("float32"), (0, 0), 4) * (depth[..., None] >= 0.5)
    bg_sharp_out = float(np.abs(g(lens_t))[~subj].mean())
    inner = cv2.erode(subj.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    near_out, near_in = float(np.abs(g(lens_t))[inner].mean()), float(np.abs(g(tex))[inner].mean())
    # Upscale x2 (esprscn) -> Lanczos resize
    up = np.asarray(Image.fromarray(img.astype(np.uint8)).resize((400, 280), Image.LANCZOS)).astype(float)
    # Deep_Font -> font-inspect on the file
    from fontTools.ttLib import TTFont
    fam = TTFont(str(FONTS / "Poppins-Bold.ttf"))["name"].getDebugName(1)
    out = save_png(np.concatenate([hurt, fixed, lens], axis=1), Path(wd) / "open_equivalents.png")
    rep = jw(Path(wd) / "mapping.json", {"Remove(CMGAN)": "cv2.inpaint", "LensBlur(DepthPrediction)": "depth-gated blur",
                                         "Upscale(esprscn)": "Lanczos x2", "Deep_Font": "fontTools name table"})
    return [check("the analysis names the Photoshop models it maps", all(k in names for k in ("CMGAN", "Select_Subject"))),
            check("inpaint repairs the scratch (error drops > 5x)", err_fixed * 5 < err_hurt, [err_fixed, err_hurt]),
            check("depth-gated lens blur softens only the far plane", bg_sharp_out < bg_sharp_in / 3 and near_out > 0.8 * near_in,
                  [bg_sharp_out, bg_sharp_in, near_out, near_in]),
            check("x2 upscale has double size and the same mean colour", up.shape[:2] == (280, 400) and abs(up.mean() - img.mean()) < 1),
            check("font inspection names the family", fam == "Poppins", fam),
            check("negative control: the damaged input still shows the scratch", err_hurt > 50, err_hurt)], [out, rep]


@card("APPX-119")
def paint_open_equivalents(task, wd):
    np = _np()
    import cv2
    from PIL import Image
    from rembg import new_session, remove
    img, subj = _photo(160, 120)
    # coloring book: edges -> black lines on white
    gray = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 40, 120)
    book = np.full_like(img, 255.0)
    book[cv2.dilate(edges, np.ones((2, 2), np.uint8)) > 0] = 0
    ink_ratio = float((book[..., 0] == 0).mean())
    # remove-bg on device (u2netp ONNX already on disk, no download)
    os.environ.setdefault("U2NET_HOME", str(Path.home() / ".u2net"))
    cut = np.asarray(remove(Image.fromarray(img.astype(np.uint8)), session=new_session("u2netp"))).astype(float)
    alpha = cut[..., 3] > 128
    iou = float((alpha & subj).sum() / max(1, (alpha | subj).sum()))
    # sticker: white outline around the cut-out (alpha dilated by 6 px)
    ring = (cv2.dilate(alpha.astype(np.uint8), np.ones((13, 13), np.uint8)) > 0) & ~alpha
    sticker = np.zeros((*alpha.shape, 4))
    sticker[ring] = (255, 255, 255, 255)
    sticker[alpha] = np.c_[img[alpha], np.full(alpha.sum(), 255)]
    out = Path(wd) / "sticker.png"
    Image.fromarray(sticker.astype(np.uint8), "RGBA").save(out)
    save_png(book, Path(wd) / "coloring.png")
    flat_edges = cv2.Canny(np.full((120, 160), 128, np.uint8), 40, 120).sum()
    return [check("coloring book has thin outlines (1-15% ink)", 0.01 < ink_ratio < 0.15, ink_ratio),
            check("remove-bg mask matches the subject (IoU > 0.8)", iou > 0.8, iou, "> 0.8"),
            check("sticker has a white border ring around the subject", ring.sum() > 0 and (sticker[ring][:, :3] == 255).all()),
            check("negative control: a flat image gives no outlines", flat_edges == 0, int(flat_edges))], [out, Path(wd) / "coloring.png"]


@card("APPX-129")
def live_project_board(task, wd):
    import threading
    import hashlib
    board = Path(wd) / "board.html"
    state = {"workers": {"render": 0, "audio": 0, "captions": 0}, "version": 0}
    versions = []
    lock = threading.Lock()

    def publish():
        rows = "".join('<div class="w" data-name="%s"><span>%s</span><i style="width:%d%%"></i><b>%d%%</b></div>'
                       % (n, n, p, p) for n, p in state["workers"].items())
        tw(board, "<!doctype html><meta charset=utf-8><title>Project board</title><style>.w i{display:block;height:8px;"
                  "background:#2a7}</style><h1>Board v%d</h1>%s" % (state["version"], rows))
        versions.append(str(board))

    def worker(name, steps):
        for k in range(steps):
            hashlib.sha256(("%s%d" % (name, k)).encode() * 20000).hexdigest()  # real work per step
            with lock:
                state["workers"][name] = int(100 * (k + 1) / steps)
                state["version"] += 1
                publish()
    with lock:
        publish()
    first = board.read_text()
    th = [threading.Thread(target=worker, args=(n, s)) for n, s in (("render", 5), ("audio", 4), ("captions", 3))]
    for t in th:
        t.start()
    for t in th:
        t.join()
    res = node_js(wd, "board", PW_HEAD + """(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+%s);const r=await p.$$eval('.w',ws=>ws.map(w=>({n:w.dataset.name,pct:parseFloat(w.querySelector('i').style.width),
px:w.querySelector('i').getBoundingClientRect().width,full:w.getBoundingClientRect().width})));
console.log(JSON.stringify({rows:r,title:await p.title(),h1:await p.textContent('h1')}));await b.close()})();""" % json.dumps(str(board)))
    done_all = all(r["pct"] == 100 and abs(r["px"] - r["full"]) < 2 for r in res["rows"])
    return [check("one board path republished on every worker step", len(set(versions)) == 1 and len(versions) == 13, len(versions), 13),
            check("three workers shown, each bar at 100% in the browser", len(res["rows"]) == 3 and done_all, res["rows"]),
            check("final version number counts all 12 worker steps", res["h1"] == "Board v12", res["h1"]),
            check("negative control: the first publish showed 0% bars", "width:0%" in first and "width:100%" not in first)], [board]


_MCP_SERVER = r'''
import json, sys
from pathlib import Path
ROOT = Path(sys.argv[1]); STATE = ROOT / "active.json"
TOOLS = [{"name": "create_project", "description": "create a project folder with a scene", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
         {"name": "edit_scene", "description": "set a field of the active project's scene", "inputSchema": {"type": "object", "properties": {"key": {"type": "string"}, "value": {}}, "required": ["key", "value"]}},
         {"name": "preview", "description": "render a preview PNG of the active scene", "inputSchema": {"type": "object", "properties": {}}}]
def active():
    return json.loads(STATE.read_text())["name"] if STATE.exists() else None
def call(name, a):
    if name == "create_project":
        d = ROOT / "projects" / a["name"]; d.mkdir(parents=True, exist_ok=True)
        (d / "scene.json").write_text(json.dumps({"title": a["name"], "bg": "#202020", "fps": 30}))
        STATE.write_text(json.dumps({"name": a["name"]})); return "created " + a["name"]
    proj = active()
    if not proj: raise ValueError("no active project")
    sp = ROOT / "projects" / proj / "scene.json"; sc = json.loads(sp.read_text())
    if name == "edit_scene":
        sc[a["key"]] = a["value"]; sp.write_text(json.dumps(sc)); return "set %s" % a["key"]
    if name == "preview":
        from PIL import Image
        h = sc["bg"].lstrip("#"); Image.new("RGB", (96, 54), tuple(int(h[i:i+2], 16) for i in (0, 2, 4))).save(sp.parent / "preview.png")
        return str(sp.parent / "preview.png")
    raise ValueError("unknown tool")
for line in sys.stdin:
    m = json.loads(line); mid = m.get("id"); meth = m.get("method"); res = None
    try:
        if meth == "initialize":
            res = {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}, "resources": {}}, "serverInfo": {"name": "kosif-write", "version": "0.1"}}
        elif meth == "tools/list": res = {"tools": TOOLS}
        elif meth == "resources/list": res = {"resources": [{"uri": "kosif://active-project", "name": "active project"}]}
        elif meth == "resources/read":
            res = {"contents": [{"uri": "kosif://active-project", "text": json.dumps({"active": active()})}]}
        elif meth == "tools/call":
            res = {"content": [{"type": "text", "text": call(m["params"]["name"], m["params"].get("arguments", {}))}]}
        elif mid is None: continue
        else: raise ValueError("method not found")
        out = {"jsonrpc": "2.0", "id": mid, "result": res}
    except Exception as e:
        out = {"jsonrpc": "2.0", "id": mid, "result": {"isError": True, "content": [{"type": "text", "text": str(e)}]}}
    print(json.dumps(out), flush=True)
'''


@card("APPX-138")
def write_capable_mcp(task, wd):
    srv = tw(Path(wd) / "kosif_write_mcp.py", _MCP_SERVER)
    ro = run([sys.executable, SP / "scripts/kosif_mcp.py", "--selftest"], timeout=60)
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "preview", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "create_project", "arguments": {"name": "promo"}}},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "edit_scene", "arguments": {"key": "bg", "value": "#ff8800"}}},
            {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "preview", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 7, "method": "resources/read", "params": {"uri": "kosif://active-project"}}]
    done = subprocess.run([sys.executable, str(srv), str(wd)], input="".join(json.dumps(m) + "\n" for m in msgs),
                          capture_output=True, text=True, timeout=30)
    rep = {r["id"]: r["result"] for r in map(json.loads, done.stdout.strip().splitlines())}
    png = Path(wd) / "projects/promo/preview.png"
    px = load_rgb(png)[10, 10].tolist() if png.exists() else None
    out = jw(Path(wd) / "mcp_session.json", rep)
    return [check("repo kosif_mcp.py --selftest proves the read interface", ro.returncode == 0),
            check("server lists the write tools", [t["name"] for t in rep[2]["tools"]] == ["create_project", "edit_scene", "preview"]),
            check("edit + preview render the edited scene colour", px == [255, 136, 0], px, [255, 136, 0]),
            check("active-project resource names the project", json.loads(rep[7]["contents"][0]["text"])["active"] == "promo"),
            check("negative control: preview before any project is an error", rep[3].get("isError") is True, rep[3])], [out, png]


_SELFTEST_HTML = r'''<!doctype html><meta charset=utf-8><title>selftest</title>
<canvas id=c width=200 height=100></canvas><script>
const q = new URLSearchParams(location.search);
async function selftest(){
  const steps = []; const c = document.getElementById('c'), x = c.getContext('2d');
  const step = async (name, fn) => { try { const v = await fn(); steps.push({name, status: 'ok', ...v}); } catch (e) { steps.push({name, status: 'error', err: String(e)}); } };
  const lit = () => { const d = x.getImageData(0, 0, 200, 100).data; let n = 0; for (let i = 0; i < d.length; i += 4) if (d[i] + d[i+1] + d[i+2] > 300) n++; return n / (d.length / 4); };
  await step('colour', () => { x.fillStyle = '#e0e0e0'; x.fillRect(0, 0, 200, 100); return {lit: lit()}; });
  await step('arabic-text', () => { x.fillStyle = '#000'; x.font = '40px serif'; x.direction = 'rtl'; x.fillText('مرحبا', 190, 60); return {lit: lit()}; });
  const project = {};
  await step('project', () => { project.name = 'demo'; project.layers = [{type: 'text', value: 'مرحبا'}]; return {layers: project.layers.length}; });
  let blob;
  await step('import', async () => { blob = await (await fetch(c.toDataURL('image/png'))).blob(); return {bytes: blob.size}; });
  let bmp;
  await step('decode', async () => { bmp = await createImageBitmap(blob); return {w: bmp.width, h: bmp.height}; });
  await step('filter', () => { x.filter = 'grayscale(1)'; x.fillStyle = '#3a7'; x.fillRect(0, 0, 100, 100); x.filter = 'none';
      const d = x.getImageData(50, 50, 1, 1).data; return {r: d[0], g: d[1], mono: Math.abs(d[0] - d[1]) < 4}; });
  await step('export', () => { const u = c.toDataURL('image/png'); return {png: u.startsWith('data:image/png'), bytes: u.length}; });
  await step('translate', () => { const dict = {'مرحبا': 'hello'}; return {out: dict[project.layers[0].value]}; });
  await step('broken-on-purpose', () => { if (!q.has('inject')) return {skipped: true}; throw new Error('injected'); });
  const report = {steps, ok: steps.every(s => s.status === 'ok')};
  await fetch('/report', {method: 'POST', body: JSON.stringify(report)});
  document.title = 'done';
}
if (q.get('selftest') === '1') selftest();
</script>'''


@card("APPX-153")
def browser_selftest(task, wd):
    import http.server
    import threading
    root = Path(wd)
    tw(root / "app.html", _SELFTEST_HTML)
    reports = []

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(root), **k)

        def log_message(self, *a):
            pass

        def do_POST(self):
            body = self.rfile.read(int(self.headers["Content-Length"]))
            name = "report_%d.json" % len(reports)
            (root / name).write_bytes(body)
            reports.append(name)
            self.send_response(204)
            self.end_headers()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    try:
        res = node_js(wd, "selftest", PW_HEAD + """(async()=>{const b=await chromium.launch();const p=await b.newPage();
const base='http://127.0.0.1:%d/app.html';const out={};
for (const [k,u] of [['plain',base],['self',base+'?selftest=1'],['inject',base+'?selftest=1&inject=1']]){
 await p.goto(u); if(k!=='plain') await p.waitForFunction(()=>document.title==='done',null,{timeout:10000}); else await p.waitForTimeout(400);
 out[k]=await p.title();}
console.log(JSON.stringify(out));await b.close()})();""" % port)
    finally:
        srv.shutdown()
    reps = [json.loads((root / n).read_text()) for n in reports]
    good = reps[0] if reps else {"steps": []}
    st = {s["name"]: s for s in good["steps"]}
    return [check("plain load posts no report; two selftest loads post two", len(reports) == 2 and res["plain"] == "selftest", reports),
            check("eight real steps ok in the real browser", good.get("ok") and len(st) == 9, [s["status"] for s in good["steps"]]),
            check("pixel probe: lit ratio > 0.2 after the colour fill", st["colour"]["lit"] > 0.2, st["colour"]["lit"]),
            check("pixel probe: grayscale filter gives |r-g| < 4", st["filter"]["mono"] is True, [st["filter"]["r"], st["filter"]["g"]]),
            check("Arabic text inked the canvas (lit ratio fell)", st["arabic-text"]["lit"] < st["colour"]["lit"]),
            check("negative control: an injected failure turns the report red", len(reps) == 2 and reps[1]["ok"] is False)], [root / reports[0]]


# =============================================================================================== CAM


def measure_path(frames, ref=None):
    """Per-frame measured camera transform against frame 0 (or ref)."""
    ref = frames[0] if ref is None else ref
    return [est(ref, f) for f in frames]


@card("CAM-154")
def kenburns_transfer(task, wd):
    np = _np()
    sys.path.insert(0, str(SP / "scripts/mimic"))
    import mm_analyze
    W, H, fps, n = 384, 216, 30, 30
    plate = fid_plate(W, H, seed=11)
    zps = 1.03  # the editor's slow push: 3 % per second
    zpf = zps ** (1 / fps)
    ref = [warp(plate, zpf ** i) for i in range(n)]
    write_video(Path(wd) / "reference.mp4", ref)

    def motion(frames):
        ms = measure_path(frames)
        s = np.array([m[0] for m in ms])
        k = np.arange(len(s))
        slope = float(np.polyfit(k, np.log(s), 1)[0])
        resid = float(np.std(np.log(s) - slope * k))
        return {"zoom_per_frame": math.exp(slope), "pan_x_per_frame": float(np.polyfit(k, [m[1] for m in ms], 1)[0]) / W,
                "pan_y_per_frame": float(np.polyfit(k, [m[2] for m in ms], 1)[0]) / H, "zoom_jitter": resid}
    mo = motion(ref)
    guess = mm_analyze._kenburns_guess(mo, fps)
    repl = fid_plate(W, H, seed=23)
    applied = [warp(repl, guess["zoom_per_s"] ** (i / fps)) for i in range(n)] if guess else [repl] * n
    out = write_video(Path(wd) / "replacement_kenburns.mp4", applied)
    mo2 = motion(read_video(out))
    static_guess = mm_analyze._kenburns_guess(motion([plate] * 10), fps)
    jw(Path(wd) / "kenburns.json", {"reference": mo, "guess": guess, "replacement_measured": mo2})
    return [check("reference zoom measured at 3 %/s", abs(mo["zoom_per_frame"] ** fps - zps) < 0.003, mo["zoom_per_frame"] ** fps, zps),
            check("mm_analyze._kenburns_guess says apply", bool(guess and guess["apply"]), guess),
            check("replacement footage carries the same zoom (measured)", abs(mo2["zoom_per_frame"] ** fps - zps) < 0.003,
                  mo2["zoom_per_frame"] ** fps, zps),
            check("negative control: a static reference gets no Ken Burns guess", static_guess is None, static_guess)], [out]


def _scenes_world(W, H):
    """Three scene panels laid out along the camera path in a 2.5D world (x positions in world px)."""
    np = _np()
    world = np.zeros((H, W * 4, 3))
    cols = [(220, 60, 60), (60, 200, 90), (60, 90, 230)]
    for i, c in enumerate(cols):
        x0 = int(W * (0.5 + 1.25 * i))
        world[:, x0:x0 + W] = c
        world[:, x0:x0 + W] += texture(W, H, seed=i) * 0.15
    return world, cols


@card("CAM-178")
def flythrough_journey(task, wd):
    np = _np()
    sc = Path(wd) / "journey"
    run([sys.executable, REPO / "tools/kosif.py", "scaffold", "higgsfield-journey", sc], timeout=60)
    W, H, fps = 160, 90, 30
    world, cols = _scenes_world(W, H)
    keys = [W * 0.5, W * 1.75, W * 3.0]  # panel left edges; camera holds then travels
    T = 4.0
    times = [0, 1.0, 2.0, 3.0, 4.0]
    xs = [keys[0], keys[0], keys[1], keys[2], keys[2]]
    # one continuous Catmull-Rom spline through the control points, sampled at sine-eased progress
    pts = [xs[0]] + xs + [xs[-1]]

    def cr(t):
        seg = min(int(t), len(xs) - 2)
        u = t - seg
        p0, p1, p2, p3 = pts[seg], pts[seg + 1], pts[seg + 2], pts[seg + 3]
        return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)
    frames = []
    for i in range(int(T * fps)):
        p = sine_in_out(i / (T * fps - 1)) * (len(xs) - 1)
        x = cr(p)
        frames.append(world[:, int(round(x)):int(round(x)) + W])
    out = write_video(Path(wd) / "journey.mp4", frames)
    fr = read_video(out)
    diffs = [float(np.abs(fr[i + 1] - fr[i]).mean()) for i in range(len(fr) - 1)]
    seen = [any(color_mask(f[45:46, 80:81], c, 45).all() for f in fr) for c in cols]
    cut = [world[:, int(keys[0]):int(keys[0]) + W]] * 30 + [world[:, int(keys[1]):int(keys[1]) + W]] * 30
    cut_jump = max(float(np.abs(cut[i + 1] - cut[i]).mean()) for i in range(59))
    return [check("scaffold wrote the higgsfield-journey style files", (sc / "STYLE.md").exists() and (sc / "PLAN.md").exists()),
            check("the camera visits all three scenes", all(seen), seen),
            check("no cuts: the largest frame-to-frame change stays small", max(diffs) < 30, max(diffs), "< 30"),
            check("negative control: a hard cut between scenes jumps > 60", cut_jump > 60, cut_jump)], [out]


@card("CAM-179")
def group_transform_drift(task, wd):
    np = _np()
    W, H, fps = 384, 216, 30
    s1, s2, T = 40, 40, 120
    ts = [0, s1, s1 + s2, T]
    sc, xx, yy, rr = [1.08, 1.0, 1.04, 1.1], [0, -12, -24, -36], [26, -18, 0, 0], [-0.8, 0.0, 0.4, 0.8]
    plate = fid_plate(W, H, seed=4)
    want = [(interp(f, ts, sc, ease_in_out_cubic), interp(f, ts, xx, ease_in_out_cubic) / 2,
             interp(f, ts, yy, ease_in_out_cubic) / 2, interp(f, ts, rr, ease_in_out_cubic)) for f in range(T + 1)]
    big = warp(plate, 1.0)
    frames = [warp(big, *w) for w in want]
    out = write_video(Path(wd) / "drift.mp4", frames)
    fr = read_video(out)
    probe = [0, s1, s1 + s2, T]
    meas = [est(plate, fr[f]) for f in probe]
    ok = all(abs(m[0] - sc[i]) < 0.004 and abs(m[3] - rr[i]) < 0.12 for i, m in enumerate(meas))
    mid = s1 // 2
    m_mid = est(plate, fr[mid])[0]
    lin_mid = (sc[0] + sc[1]) / 2 + (sc[0] - sc[1]) * 0  # linear midpoint 1.04; eased midpoint also 1.04: probe quarter
    q = s1 // 4
    m_q = est(plate, fr[q])[0]
    lin_q = sc[0] + (sc[1] - sc[0]) * 0.25
    eased_q = sc[0] + (sc[1] - sc[0]) * ease_in_out_cubic(0.25)
    return [check("measured scale/rotation hit 1.08 -> 1.0 -> 1.04 -> 1.1 and -0.8 -> 0.8 deg at the boundaries", ok,
                  [[round(m[0], 4), round(m[3], 3)] for m in meas]),
            check("in-between motion is eased inOutCubic (quarter point)", abs(m_q - eased_q) < 0.003, m_q, eased_q),
            check("midpoint of segment 1 is 1.04", abs(m_mid - lin_mid) < 0.004, m_mid, lin_mid),
            check("negative control: linear timing at the quarter point would differ", abs(lin_q - eased_q) > 0.01 and abs(m_q - lin_q) > 0.008,
                  [m_q, lin_q])], [out]


@card("CAM-180")
def catmull_rom_camera(task, wd):
    res = node_js(wd, "spline", """const THREE=require('three');
const curve=new THREE.CatmullRomCurve3([new THREE.Vector3(0,1,8),new THREE.Vector3(3,1.5,5),new THREE.Vector3(2,2,1),new THREE.Vector3(-1,1.2,-2)]);
const sine=t=>-(Math.cos(Math.PI*t)-1)/2; const T=3.0, fps=30, N=T*fps;
const seek=(t,ease)=>curve.getPointAt(ease?sine(t/T):t/T);
const path=[];for(let i=0;i<=N;i++){const p=seek(i/fps,true);path.push([p.x,p.y,p.z]);}
const lin=[];for(let i=0;i<=N;i++){const p=seek(i/fps,false);lin.push([p.x,p.y,p.z]);}
const len=curve.getLength();const sp=(a,i)=>Math.hypot(a[i+1][0]-a[i][0],a[i+1][1]-a[i][1],a[i+1][2]-a[i][2])*fps;
const end=curve.getPointAt(1);
console.log(JSON.stringify({len,startV:sp(path,0),endV:sp(path,N-1),midV:sp(path,N/2),linStartV:sp(lin,0),
 maxV:Math.max(...path.slice(0,-1).map((_,i)=>sp(path,i))),end:[end.x,end.y,end.z],last:path[N],path}));""")
    out = jw(Path(wd) / "camera_path.json", res)
    avg = res["len"] / 3.0
    return [check("path ends at the last control point", all(abs(a - b) < 1e-6 for a, b in zip(res["last"], res["end"]))),
            check("sine in-out: start and end speed near zero", res["startV"] < 0.05 * avg and res["endV"] < 0.05 * avg,
                  [res["startV"], res["endV"]], "< 5% of average"),
            check("peak speed mid-move is pi/2 x average", abs(res["maxV"] / avg - math.pi / 2) < 0.05, res["maxV"] / avg, math.pi / 2),
            check("dolly speed within 0.3-5 units/s over a 3 s move", 0.3 <= avg <= 5, avg),
            check("negative control: linear progress starts at full speed", res["linStartV"] > 0.9 * avg, res["linStartV"], avg)], [out]


def _render_moves(plate, moves):
    return [warp(plate, *m) for m in moves]


@card("CAM-392")
def plan_camera_keys(task, wd):
    np = _np()
    W, H, fps = 384, 216, 30
    plate = fid_plate(W, H, seed=9)
    plan = [{"scene": 1, "camera": "push-in", "from": 1.0, "to": 1.08, "ease": "ease-out", "s": 1.5},
            {"scene": 2, "camera": "pan", "dx_frac": 0.18, "s": 1.5},
            {"scene": 3, "camera": "pull-back", "from": 1.05, "to": 1.0, "ease": "ease-out", "s": 1.5}]
    keys = {"static", "push-in", "pull-back", "pan", "tilt", "orbit", "rack-focus"}
    tw(Path(wd) / "PLAN.md", "| Scene | Camera |\n|---|---|\n" + "".join("| %d | %s |\n" % (p["scene"], p["camera"]) for p in plan))
    moves = []
    n = int(1.5 * fps)
    for p in plan:
        for i in range(n):
            u = ease_out_cubic(i / (n - 1))
            if p["camera"] == "pan":
                moves.append((1.04, -p["dx_frac"] * W * u, 0, 0))
            else:
                moves.append((p["from"] + (p["to"] - p["from"]) * u, 0, 0, 0))
    out = write_video(Path(wd) / "plan_camera.mp4", _render_moves(plate, moves))
    fr = read_video(out)
    m = [est(plate, fr[i]) for i in (0, n - 1, n, 2 * n - 1, 2 * n, 3 * n - 1)]
    early = est(plate, fr[n // 4])[0]
    want_early = 1 + 0.08 * ease_out_cubic((n // 4) / (n - 1))
    pan_frac = abs(m[3][1] - m[2][1]) / W
    still = est(plate, warp(plate, 1.0))[0]
    return [check("every PLAN camera key is a known key", all(p["camera"] in keys for p in plan)),
            check("opening push-in 100 -> 108 %", abs(m[0][0] - 1.0) < 0.003 and abs(m[1][0] - 1.08) < 0.004, [m[0][0], m[1][0]]),
            check("ease-out timing of the push (quarter point)", abs(early - want_early) < 0.004, early, want_early),
            check("pan travels <= 20 % of the frame", 0.15 < pan_frac <= 0.2, pan_frac),
            check("closing pull-back 105 -> 100 %", abs(m[4][0] - 1.05) < 0.004 and abs(m[5][0] - 1.0) < 0.003, [m[4][0], m[5][0]]),
            check("negative control: the untreated plate measures no push", abs(still - 1.08) > 0.05, still)], [out, Path(wd) / "PLAN.md"]


@card("CAM-393")
def focal_to_fov(task, wd):
    res = node_js(wd, "fov", """const THREE=require('three');
const out={};for(const f of [35,50,85]){const c=new THREE.PerspectiveCamera(45,16/9,0.1,100);c.filmGauge=36;c.setFocalLength(f);
 c.updateProjectionMatrix();out['v'+f]=c.fov;out['h'+f]=2*Math.atan(Math.tan(c.fov*Math.PI/360)*c.aspect)*180/Math.PI;
 const p=new THREE.Vector3(Math.tan(c.fov*Math.PI/360)*5,0,-5).applyMatrix4(c.matrixWorldInverse).project(c);out['edge'+f]=p.x;}
const d=new THREE.PerspectiveCamera(45,16/9,0.1,100);out.default=d.fov;out.near=d.near;out.far=d.far;
const s=new THREE.PerspectiveCamera(45,16/9,0.1,100);const q=new THREE.Vector3(0,Math.tan(45*Math.PI/360)*5,-5).project(s);out.sampleTop=q.y;
console.log(JSON.stringify(out));""")
    out = jw(Path(wd) / "fov.json", res)
    # filmGauge 36 mm applies to the longer side, so three's vertical fov at 16:9 maps the horizontal 36 mm frame
    hf = {f: 2 * math.degrees(math.atan(18.0 / f)) for f in (35, 50, 85)}
    return [check("35-50 mm -> about 40-55 deg (horizontal, 36 mm gauge)", 39 <= res["h50"] <= 41 and 53 <= res["h35"] <= 56,
                  [res["h35"], res["h50"]]),
            check("85 mm product close-up -> about 24 deg", abs(res["h85"] - 24) < 0.5, res["h85"], 24),
            check("three.js setFocalLength agrees with 2*atan(18/f)", all(abs(res["h%d" % f] - hf[f]) < 0.05 for f in hf), hf),
            check("projection: a point at the half-fov edge lands on the frame edge", abs(res["sampleTop"] - 1) < 1e-6, res["sampleTop"]),
            check("sample camera fov 45, near 0.1, far 100", res["default"] == 45 and res["near"] == 0.1 and res["far"] == 100),
            check("negative control: the default 45 deg is not the 85 mm close-up", abs(res["default"] - 24) > 10)], [out]


def _layer(w, h, col, x0, y0, x1, y1):
    np = _np()
    a = np.zeros((h, w, 4))
    a[y0:y1, x0:x1, :3] = col
    a[y0:y1, x0:x1, 3] = 1
    return a


def _comp(layers, offsets, w, h, bg=(10, 10, 10)):
    np = _np()
    out = np.zeros((h, w, 3))
    out[:] = bg
    for L, dx in zip(layers, offsets):
        sh = np.roll(L, int(round(dx)), axis=1)
        a = sh[..., 3:4]
        out = out * (1 - a) + sh[..., :3] * a
    return out


@card("CAM-394")
def planar_parallax(task, wd):
    W, H = 320, 180
    cols = [(60, 60, 220), (60, 200, 60), (230, 60, 60)]  # background, mid, foreground (back to front)
    layers = [_layer(W, H, cols[0], 20, 20, 60, 60), _layer(W, H, cols[1], 120, 70, 160, 110), _layer(W, H, cols[2], 220, 120, 260, 160)]
    factors = [0.15, 0.5, 1.0]
    cams = [0, 20, 40, 60]
    frames = [_comp(layers, [c * f for f in factors], W, H) for c in cams]
    out = write_video(Path(wd) / "parallax.mp4", frames * 8)
    fr = read_video(out)[:4]
    shifts = [[centroid(color_mask(f, c, 20))[0] - centroid(color_mask(fr[0], c, 20))[0] for c in cols] for f in fr]
    ratio = [shifts[3][i] / 60.0 for i in range(3)]
    flat = [_comp(layers, [60, 60, 60], W, H)]
    flat_r = [(centroid(color_mask(flat[0], c, 20))[0] - centroid(color_mask(fr[0], c, 20))[0]) / 60.0 for c in cols]
    return [check("measured layer speeds 0.15 : 0.5 : 1.0 of the camera offset", all(abs(r - f) < 0.02 for r, f in zip(ratio, factors)),
                  ratio, factors),
            check("speed falls with depth (fg > mid > bg)", ratio[2] > ratio[1] > ratio[0]),
            check("negative control: one shared offset gives no parallax", all(abs(r - 1.0) < 0.02 for r in flat_r) and
                  not all(abs(r - f) < 0.02 for r, f in zip(flat_r, factors)), flat_r)], [out]


@card("CAM-395")
def fake_dof_blur(task, wd):
    np = _np()
    import cv2
    bgp = save_png(texture(320, 180, seed=5), Path(wd) / "bg.png")
    res = node_js(wd, "blur", PW_HEAD + """(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.setContent('<canvas id=c width=320 height=180></canvas>');
const url='data:image/png;base64,'+fs.readFileSync(%s).toString('base64');
const out={};for(const blur of [0,6]){out['b'+blur]=await p.evaluate(async([u,blur])=>{const img=new Image();img.src=u;await img.decode();
 const c=document.getElementById('c'),x=c.getContext('2d');x.clearRect(0,0,320,180);x.filter=blur?`blur(${blur}px)`:'none';x.drawImage(img,0,0);
 x.filter='none';x.fillStyle='#fff';x.fillRect(120,50,80,80);x.fillStyle='#111';for(let i=0;i<8;i++)x.fillRect(124+i*10,54,4,72);
 return c.toDataURL('image/png');},[url,blur]);}
for(const k in out)fs.writeFileSync(k+'.png',Buffer.from(out[k].split(',')[1],'base64'));
console.log(JSON.stringify({ok:true}));await b.close()})();""" % json.dumps(str(bgp)))

    def lap(a, box):
        x0, y0, x1, y1 = box
        g = cv2.cvtColor(a[y0:y1, x0:x1].astype("float32"), cv2.COLOR_RGB2GRAY)
        return float(cv2.Laplacian(g, cv2.CV_32F).var())
    sharp, soft = load_rgb(Path(wd) / "b0.png"), load_rgb(Path(wd) / "b6.png")
    bgbox, fgbox = (10, 10, 100, 170), (122, 52, 198, 128)
    return [check("background plate blurred (Laplacian variance drops > 10x)", lap(soft, bgbox) * 10 < lap(sharp, bgbox),
                  [lap(soft, bgbox), lap(sharp, bgbox)]),
            check("foreground subject stays sharp", abs(lap(soft, fgbox) - lap(sharp, fgbox)) < 0.05 * lap(sharp, fgbox) + 1,
                  [lap(soft, fgbox), lap(sharp, fgbox)]),
            check("negative control: the unblurred plate is sharp", lap(sharp, bgbox) > 50, lap(sharp, bgbox))], [Path(wd) / "b6.png"]


def _clamp_path(prop, fps, max_push, max_pan, max_rot):
    """Enforce camera limits on a proposed per-frame path; low-pass to remove shake."""
    np = _np()
    s = np.array([p[0] for p in prop])
    x = np.array([p[1] for p in prop])
    r = np.array([p[3] for p in prop])
    k = 15
    sm = lambda a: np.convolve(np.pad(a, (k // 2, k // 2), mode="edge"), np.ones(k) / k, mode="valid")  # noqa: E731
    s, x, r = sm(s), sm(x), sm(r)
    s = np.clip(s, 1.0, 1.0 + max_push)
    r = np.clip(r, -max_rot, max_rot)
    out_x = [x[0]]
    for v in x[1:]:
        step = max(-max_pan / fps, min(max_pan / fps, v - out_x[-1]))
        out_x.append(out_x[-1] + step)
    return [(float(a), float(b), 0.0, float(c)) for a, b, c in zip(s, out_x, r)]


def _path_stats(meas, fps):
    np = _np()
    s = np.array([m[0] for m in meas])
    x = np.array([m[1] for m in meas])
    r = np.array([m[3] for m in meas])
    acc = np.diff(x, 2)
    return {"push": float(s.max() - 1), "pan_px_s": float(np.abs(np.diff(x)).max() * fps), "rot": float(np.abs(r).max()),
            "shake": float(np.abs(acc).max())}


@card("CAM-396")
def gentle_table_camera(task, wd):
    np = _np()
    W, H, fps, n = 384, 216, 30, 60
    tbl = fid_plate(W, H, seed=12)
    for yy in range(30, H, 24):
        tbl[yy:yy + 1, 10:W - 10] = 230
    rng = np.random.default_rng(1)
    prop = [(1 + 0.12 * i / n, 3.0 * i + rng.normal(0, 4), 0, 2.0 * math.sin(i / 3)) for i in range(n)]
    path = _clamp_path(prop, fps, 0.039, 38, 0.45)  # limits with a small safety margin
    out = write_video(Path(wd) / "table_camera.mp4", [warp(tbl, *p) for p in path])
    fr = read_video(out)
    st = _path_stats([est(tbl, f) for f in fr[::3]], fps / 3)
    raw = _path_stats(prop, fps)
    ok = lambda d: d["push"] <= 0.041 and d["pan_px_s"] <= 41 and d["rot"] <= 0.52 and d["shake"] < 1.0  # noqa: E731
    return [check("push <= 4 % per scene (measured)", st["push"] <= 0.041, st["push"]),
            check("pan <= 40 px/s (measured)", st["pan_px_s"] <= 41, st["pan_px_s"]),
            check("rotation within +-0.5 deg (measured)", st["rot"] <= 0.52, st["rot"]),
            check("no shake: second difference of the pan is small", st["shake"] < 3.0, st["shake"]),
            check("negative control: the handheld proposal breaks the limits", not ok(raw), raw)], [out]


@card("CAM-397")
def chapter_pans(task, wd):
    np = _np()
    W, H, fps = 384, 216, 30
    board = fid_plate(W, H, seed=13)
    ease = bezier(0.65, 0, 0.35, 1)
    chapters = [(0, 1.0), (-30, 1.4), (-50, 1.2)]
    move_s, hold_s = 0.85, 1.5
    keys = []
    t = 0.0
    seq = []
    for i, (x, z) in enumerate(chapters):
        if i:
            seq.append(("move", t, t + move_s, chapters[i - 1], (x, z)))
            t += move_s
        seq.append(("hold", t, t + hold_s, (x, z), (x, z)))
        t += hold_s
    total = int(round(t * fps))
    path = []
    for f in range(total):
        tt = f / fps
        for kind, a, b, p0, p1 in seq:
            if a <= tt < b or (f == total - 1 and kind == "hold"):
                u = ease((tt - a) / (b - a)) if kind == "move" else 0
                z = min(1.8, p0[1] + (p1[1] - p0[1]) * u)
                path.append((z, (p0[0] + (p1[0] - p0[0]) * u) * z, 0, 0))
                break
    out = write_video(Path(wd) / "chapters.mp4", [warp(board, *p) for p in path])
    fr = read_video(out)
    meas = [est(board, f) for f in fr[::2]]
    zs = [m[0] for m in meas]
    moving = [abs(meas[i + 1][0] - meas[i][0]) > 1e-3 or abs(meas[i + 1][1] - meas[i][1]) > 0.3 for i in range(len(meas) - 1)]
    runs, cur, val = [], 0, moving[0]
    for mv in moving:
        if mv == val:
            cur += 1
        else:
            runs.append((val, cur * 2 / fps))
            val, cur = mv, 1
    runs.append((val, cur * 2 / fps))
    holds = [d for mv, d in runs if not mv]
    moves = [d for mv, d in runs if mv]
    prop_zoom = 2.2
    return [check("zoom range 1.0 -> 1.4, never above 1.8 (measured)", max(zs) <= 1.81 and abs(max(zs) - 1.4) < 0.01, max(zs)),
            check("each pan lasts 700-1000 ms", len(moves) == 2 and all(0.6 <= d <= 1.0 for d in moves), moves),
            check("holds after each move >= 1.4 s", len(holds) == 3 and all(d >= 1.4 for d in holds), holds),
            check("cubic-bezier(0.65,0,0.35,1) is symmetric ease-in-out", abs(ease(0.5) - 0.5) < 1e-3 and ease(0.2) < 0.1),
            check("negative control: the uncapped 2.2x proposal measures above 1.8", est(board, warp(board, prop_zoom))[0] > 1.81,
                  est(board, warp(board, prop_zoom))[0])], [out]


def _device_rect(aspect, W):
    """Device frame size for the canvas aspect: 9:16 -> 62 % height, 16:9 -> 80 % height on the right third line, 1:1 -> 70 %."""
    H = int(round(W / aspect))
    share = {"9:16": 0.62, "16:9": 0.80, "1:1": 0.70}
    key = "9:16" if aspect < 0.8 else ("16:9" if aspect > 1.2 else "1:1")
    dh = share[key] * H
    dw = dh * 9 / 19.5
    cx = W * 2 / 3 if key == "16:9" else W / 2
    return key, W, H, (cx - dw / 2, H / 2 - dh / 2, cx + dw / 2, H / 2 + dh / 2)


@card("CAM-398")
def device_share(task, wd):
    np = _np()
    from PIL import Image, ImageDraw
    res, outs = {}, []
    for aspect, W in ((9 / 16, 270), (16 / 9, 480), (1.0, 300)):
        key, W, H, box = _device_rect(aspect, W)
        im = Image.new("RGB", (W, H), (240, 240, 240))
        ImageDraw.Draw(im).rounded_rectangle([round(v) for v in box], radius=12, fill=(20, 20, 20))
        p = Path(wd) / ("device_%s.png" % key.replace(":", "x"))
        im.save(p)
        outs.append(p)
        b = ink_bbox(load_rgb(p), (240, 240, 240), 60)
        res[key] = {"h_share": (b[3] - b[1]) / H, "cx": (b[0] + b[2]) / 2 / W}
    jw(Path(wd) / "shares.json", res)
    im = Image.new("RGB", (270, 480), (240, 240, 240))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, 221, 479], radius=12, fill=(20, 20, 20))  # fit-to-height proposal
    nb = ink_bbox(np.asarray(im).astype(float), (240, 240, 240), 60)
    naive = (nb[3] - nb[1]) / 480
    return [check("9:16 device height 55-70 %", 0.55 <= res["9:16"]["h_share"] <= 0.70, res["9:16"]["h_share"]),
            check("16:9 device 75-85 % on a third line", 0.75 <= res["16:9"]["h_share"] <= 0.85 and abs(res["16:9"]["cx"] - 2 / 3) < 0.01,
                  res["16:9"]),
            check("1:1 device 70 %", abs(res["1:1"]["h_share"] - 0.70) < 0.01, res["1:1"]["h_share"]),
            check("negative control: a fit-to-height device (measured) breaks the shares", not 0.55 <= naive <= 0.85, naive)], outs


@card("CAM-399")
def device_text_margins(task, wd):
    np = _np()
    from PIL import Image, ImageDraw
    W, H = 360, 640
    im = Image.new("RGB", (W, H), (245, 245, 245))
    d = ImageDraw.Draw(im)
    dev = (70, 120, 290, 600)
    d.rounded_rectangle(dev, radius=24, fill=(30, 30, 30))
    island = (150, 132, 210, 146)
    d.rounded_rectangle(island, radius=7, fill=(0, 0, 0))
    home = (150, 586, 210, 590)
    d.rectangle(home, fill=(200, 200, 200))
    safe = (W * 0.05, H * 0.12, W * 0.95, H * 0.88)
    f = font("Poppins-Bold.ttf", 26)
    text = "Ship it today"
    tb = d.textbbox((0, 0), text, font=f)
    tx = (W - (tb[2] - tb[0])) / 2 - tb[0]
    ty = safe[1] - tb[1]
    d.text((tx, ty), text, font=f, fill=(200, 30, 60))
    base = Path(wd) / "frame.png"
    im.save(base)
    # push-in toward a tapped element; the crop is snapped so it never cuts through the island
    z, focus = 1.6, (180, 340)
    cw, ch = W / z, H / z
    naive = (focus[0] - cw / 2, focus[1] - ch / 2, focus[0] + cw / 2, focus[1] + ch / 2)
    x0, y0 = naive[0], naive[1]
    if island[1] - 4 < y0 < island[3] + 4:
        y0 = island[1] - 10
    if not (x0 <= dev[0] or x0 + cw >= dev[2]):
        x0 = dev[0] - 10
    crop = (x0, y0, x0 + cw, y0 + ch)
    pushed = im.crop(tuple(round(v) for v in crop)).resize((W, H))
    pp = Path(wd) / "pushin.png"
    pushed.save(pp)
    pa = load_rgb(pp)
    isl_px = int((pa[..., 0] < 8).sum())
    a = load_rgb(base)
    ink = ink_bbox(np.where(color_mask(a, (200, 30, 60), 40)[..., None], 0, 255).repeat(3, -1), (255, 255, 255), 10)
    cuts = lambda c: c[1] > island[1] and c[1] < island[3]  # noqa: E731
    keeps_island = not cuts(crop) and crop[1] <= island[1]
    keeps_edge = crop[0] <= dev[0] or crop[2] >= dev[2]
    full_isl = (island[2] - island[0]) * (island[3] - island[1]) * z * z
    centre_cuts_island = cuts(naive)
    centre_keeps_edge = True
    return [check("text inside 5 % side margins", ink[0] >= W * 0.05 and ink[2] <= W * 0.95, ink),
            check("text inside 12 % top/bottom margins", ink[1] >= H * 0.12 - 1 and ink[3] <= H * 0.88, ink),
            check("push-in never crops through the island (whole island in the pushed frame)", keeps_island and isl_px > 0.8 * full_isl,
                  [crop, isl_px, full_isl]),
            check("push-in keeps one vertical device edge", keeps_edge),
            check("negative control: the unsnapped push toward the tap cuts through the island", centre_cuts_island, naive)], [base, pp]


@card("CAM-400")
def hold_push_and_tap_dolly(task, wd):
    np = _np()
    W, H, fps = 384, 216, 30
    ui = fid_plate(W, H, seed=14)
    hold = [(1.0 + 0.06 * sine_in_out(i / (3.5 * fps - 1)), 0, 0, 0) for i in range(int(3.5 * fps))]
    tap = (W * 0.7, H * 0.7)  # the blue fiducial is the tapped element
    dolly = []
    for i in range(int(0.6 * fps)):
        z = 1.0 + 0.12 * ease_out_cubic(i / (0.6 * fps - 1))
        dolly.append(z)
    for i in range(int(0.9 * fps)):
        dolly.append(1.12 - 0.12 * ease_in_out_cubic(i / (0.9 * fps - 1)))
    # zoom toward the tap point: keep the tap's screen position moving toward centre
    dmoves = [(z, (W / 2 - tap[0]) * (z - 1) / 0.12 * 0.5, (H / 2 - tap[1]) * (z - 1) / 0.12 * 0.5, 0) for z in dolly]
    out = write_video(Path(wd) / "push_dolly.mp4", [warp(ui, *m) for m in hold + dmoves])
    fr = read_video(out)
    n1 = len(hold)
    m_end = est(ui, fr[n1 - 1])[0]
    m_peak = est(ui, fr[n1 + int(0.6 * fps) - 1])
    m_back = est(ui, fr[-1])[0]
    tap_d0 = math.hypot(marks(fr[n1])[2][0] - W / 2, marks(fr[n1])[2][1] - H / 2)
    tap_d1 = math.hypot(marks(fr[n1 + int(0.6 * fps) - 1])[2][0] - W / 2, marks(fr[n1 + int(0.6 * fps) - 1])[2][1] - H / 2)
    s_mid = est(ui, fr[n1 // 2])[0]
    return [check("hold push 1.00 -> 1.06 over 3.5 s", abs(m_end - 1.06) < 0.003, m_end, 1.06),
            check("sine timing: half the push at mid-hold", abs(s_mid - 1.03) < 0.003, s_mid, 1.03),
            check("dolly reaches 1.12 in 600 ms", abs(m_peak[0] - 1.12) < 0.004, m_peak[0], 1.12),
            check("the tapped element moves toward the centre", tap_d1 < tap_d0 - 5, [tap_d0, tap_d1]),
            check("returns to 1.00 over 900 ms", abs(m_back - 1.0) < 0.003, m_back),
            check("negative control: the untreated UI has no push", abs(est(ui, ui)[0] - 1.06) > 0.05)], [out]


@card("CAM-401")
def shared_rig(task, wd):
    np = _np()
    W, H = 384, 216
    photos = [fid_plate(W, H, seed=s) for s in (21, 22, 23)]
    rig = (1.05, -8.0, 4.0, 0.7)
    shared = [warp(p, *rig) for p in photos]
    out = write_video(Path(wd) / "rig.mp4", shared * 3)
    fr = read_video(out)[:3]
    meas = [est(p, f) for p, f in zip(photos, fr)]
    spread = max(max(m[i] for m in meas) - min(m[i] for m in meas) for i in range(4))
    rng = np.random.default_rng(3)
    loose = [warp(p, 1 + rng.uniform(0, 0.1), rng.uniform(-20, 20), 0, rng.uniform(-3, 3)) for p in photos]
    lm = [est(p, f) for p, f in zip(photos, loose)]
    lspread = max(max(m[i] for m in lm) - min(m[i] for m in lm) for i in range(4))
    return [check("all photos measure the same transform (spread < 0.2)", spread < 0.2, spread),
            check("rig rotation <= 1 deg", all(abs(m[3]) <= 1.0 for m in meas), [m[3] for m in meas]),
            check("measured rig equals the scene rig", abs(meas[0][0] - 1.05) < 0.003 and abs(meas[0][3] - 0.7) < 0.1, meas[0]),
            check("negative control: per-photo random moves disagree (spread > 1)", lspread > 1, lspread)], [out]


def _face_img(W, H, cx, cy, r):
    np = _np()
    yy, xx = np.mgrid[0:H, 0:W]
    a = np.full((H, W, 3), 200.0)
    a[(xx - cx) ** 2 + ((yy - cy) / 1.25) ** 2 < r * r] = (225, 180, 150)
    for ex in (cx - r * 0.38, cx + r * 0.38):
        a[(xx - ex) ** 2 + (yy - (cy - r * 0.2)) ** 2 < (r * 0.1) ** 2] = (20, 20, 20)
    return a


@card("CAM-402")
def portrait_framing(task, wd):
    np = _np()
    from PIL import Image
    SW, SH = 720, 1000  # source portrait, subject left of centre
    src = _face_img(SW, SH, 290, 420, 120)
    eyes0 = centroid(color_mask(src, (20, 20, 20), 10))
    W, H = 270, 480  # 9:16 output
    push = 1.08
    # crop a 9:16 window so that the eyes sit on the top third and the face on the left vertical third
    ch = SH / push * 0.9
    cw = ch * 9 / 16
    s = W / cw
    x0 = eyes0[0] - cw / 3
    y0 = eyes0[1] - ch / 3
    x0 = min(max(0, x0), SW - cw)
    y0 = min(max(0, y0), SH - ch)
    crop = np.asarray(Image.fromarray(src.astype("uint8")).crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((W, H))).astype(float)
    p = save_png(crop, Path(wd) / "portrait_916.png")
    e = centroid(color_mask(crop, (20, 20, 20), 40))
    face = color_mask(crop, (225, 180, 150), 30) | color_mask(crop, (20, 20, 20), 40)
    fx_ = centroid(face)[0]
    base_ch = SH * 0.9
    face_push = base_ch / ch
    pan_frac = abs((x0 + cw / 2) - SW / 2) / SW
    naive = (SH / 2) / SH
    return [check("eyes on the top third line", abs(e[1] / H - 1 / 3) < 0.02, e[1] / H, 1 / 3),
            check("subject on a vertical third", abs(fx_ / W - 1 / 3) < 0.08 or abs(fx_ / W - 2 / 3) < 0.08, fx_ / W),
            check("face push <= 1.08x", face_push <= 1.0801, face_push),
            check("pan <= 6 % of the width", pan_frac <= 0.06, pan_frac),
            check("negative control: a centred frame puts the eyes at mid-height", abs(naive - 1 / 3) > 0.1, naive)], [p]


@card("CAM-403")
def screen_arrival(task, wd):
    np = _np()
    import cv2
    from PIL import Image, ImageDraw
    W, H, fps = 480, 270, 30
    share, rot0, n_arr, n_hold = 0.78, 6.0, 18, 30
    sw, sh = W * share, W * share * 9 / 16 * 0.6
    frames, rots, boxes = [], [], []
    for i in range(n_arr + n_hold):
        u = ease_out_cubic(min(1, i / (n_arr - 1)))
        rot = rot0 * (1 - u)
        y = H / 2 + (1 - u) * 60
        im = Image.new("RGB", (W, H), (235, 235, 235))
        scr = Image.new("RGBA", (int(sw), int(sh)), (25, 90, 200, 255))
        scr = scr.rotate(rot, expand=True, resample=Image.BICUBIC)
        im.paste(scr, (int(W / 2 - scr.width / 2), int(y - scr.height / 2)), scr)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((8, 10, 8 + 40, 10 + 16), radius=8, fill=(240, 120, 20))  # callout outside the screen
        frames.append(np.asarray(im).astype(float))
    out = write_video(Path(wd) / "screen_arrival.mp4", frames)
    fr = read_video(out)
    for f in fr:
        m = color_mask(f, (25, 90, 200), 40).astype("uint8")
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (cx, cy), (rw, rh), ang = cv2.minAreaRect(max(cnts, key=cv2.contourArea))
        a = ang if rw >= rh else ang - 90
        a = (a + 45) % 90 - 45
        rots.append(abs(a))
        boxes.append(cv2.boundingRect(m))
    final = boxes[-1]
    fi = Image.new("RGB", (W, H), (235, 235, 235))
    fi.paste(Image.new("RGB", (W, int(sh)), (25, 90, 200)), (0, int(H / 2 - sh / 2)))
    full_share = cv2.boundingRect(color_mask(np.asarray(fi).astype(float), (25, 90, 200), 40).astype("uint8"))[2] / W
    call = ink_bbox(np.where(color_mask(fr[-1], (240, 120, 20), 40)[..., None], 0, 255).repeat(3, -1), (255, 255, 255), 10)
    overlap = not (call[2] < final[0] or call[0] > final[0] + final[2] or call[3] < final[1] or call[1] > final[1] + final[3])
    return [check("final screen width 72-84 % of a 16:9 frame", 0.72 <= final[2] / W <= 0.84, final[2] / W),
            check("rotation <= 6 deg during arrival", max(rots[:n_arr]) <= 6.3 and max(rots[:n_arr]) > 4, max(rots[:n_arr])),
            check("no rotation after arrival", max(rots[n_arr:]) < 0.6, max(rots[n_arr:])),
            check("callout sits outside the screen", not overlap, [call, final]),
            check("negative control: the untreated full-width screen breaks the share", not 0.72 <= full_share <= 0.84, full_share)], [out]


@card("CAM-404")
def build_at_2x(task, wd):
    np = _np()
    import cv2
    from PIL import Image, ImageDraw
    W, H = 320, 180

    def art(scale):
        im = Image.new("RGB", (W * scale, H * scale), (250, 250, 250))
        d = ImageDraw.Draw(im)
        for i in range(0, W * scale, 6 * scale):
            d.line([(i, 0), (i, H * scale)], fill=(20, 20, 20), width=scale)
        d.text((40 * scale, 70 * scale), "ZOOM 1.6x", font=font("Poppins-Bold.ttf", 28 * scale), fill=(200, 20, 40))
        return np.asarray(im).astype("float32")
    z = 1.6

    def render(scale):
        src = art(scale)
        M = cv2.getRotationMatrix2D((W * scale / 2, H * scale / 2), 0, z / scale)  # one transform: push + scale-to-output
        M[0, 2] -= (W * scale - W) / 2
        M[1, 2] -= (H * scale - H) / 2
        return cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_AREA if scale > 1 else cv2.INTER_LINEAR)
    one, two = render(1), render(2)
    ref = cv2.resize(art(4), (W * 4, H * 4))
    M = cv2.getRotationMatrix2D((W * 2, H * 2), 0, z / 4)
    M[0, 2] -= (W * 4 - W) / 2
    M[1, 2] -= (H * 4 - H) / 2
    truth = cv2.warpAffine(ref, M, (W, H), flags=cv2.INTER_AREA)
    e1, e2 = float(np.abs(one - truth).mean()), float(np.abs(two - truth).mean())
    p = save_png(two, Path(wd) / "zoom_2x_build.png")
    save_png(one, Path(wd) / "zoom_1x_build.png")
    return [check("zoom > 1.4x triggers the 2x build", z > 1.4),
            check("2x build is closer to the 4x reference than the 1x build", e2 < e1 * 0.7, [e2, e1]),
            check("negative control: the 1x build at 1.6x is visibly worse (error > 2)", e1 > 2, e1)], [p]


@card("CAM-U01")
def planar_track_lk(task, wd):
    np = _np()
    import cv2
    W, H, n = 320, 240, 30
    base = texture(W * 2, H * 2, seed=31)
    gt = [(1 + 0.004 * i, 2.0 * i, 1.0 * i) for i in range(n)]
    frames = [warp(base, s, tx, ty, 0, out=(W * 2, H * 2))[H // 2:H // 2 + H, W // 2:W // 2 + W] for s, tx, ty in gt]
    write_video(Path(wd) / "tabletop.mp4", frames)
    g = [cv2.cvtColor(f.astype(np.uint8), cv2.COLOR_RGB2GRAY) for f in frames]
    anchor = np.array([160.0, 120.0])
    pts = cv2.goodFeaturesToTrack(g[0], 300, 0.01, 6)
    pts = pts[np.hypot(pts[:, 0, 0] - anchor[0], pts[:, 0, 1] - anchor[1]) < 60]
    a = anchor.copy()
    cur = pts.copy()
    track, scale = [a.copy()], 1.0
    for i in range(1, n):
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(g[i - 1], g[i], cur, None, winSize=(21, 21), maxLevel=3)
        back, st2, _ = cv2.calcOpticalFlowPyrLK(g[i], g[i - 1], nxt, None, winSize=(21, 21), maxLevel=3)
        fb = np.hypot(*(back - cur)[:, 0].T)
        good = (st[:, 0] == 1) & (st2[:, 0] == 1) & (fb < 1.5)
        d = np.median(nxt[good, 0] - cur[good, 0], axis=0)
        p0, p1 = cur[good, 0], nxt[good, 0]
        scale *= float(np.median(np.hypot(*(p1 - p1.mean(0)).T) / np.maximum(1e-6, np.hypot(*(p0 - p0.mean(0)).T))))
        a = a + d
        track.append(a.copy())
        cur = nxt[good]
    truth = [anchor + np.array([tx, ty]) for s, tx, ty in gt]  # the anchor sits on the plate centre, so only t moves it
    err = [float(np.hypot(*(t - p))) for t, p in zip(truth, track)]
    label_off = np.array([0, -30]) * scale ** 0.6
    out = jw(Path(wd) / "track.json", {"track": [p.tolist() for p in track], "err_px": err, "label_offset": label_off.tolist(),
                                       "scale": scale})
    static_err = float(np.hypot(*(truth[-1] - anchor)))
    return [check("LK median track error < 1.5 px over 30 frames", max(err) < 1.5, max(err)),
            check("forward-backward check kept most points", len(cur) > 0.6 * len(pts), [len(cur), len(pts)]),
            check("label offset scales by scale^0.6", abs(label_off[1] + 30 * gt[-1][0] ** 0.6) < 0.5, label_off.tolist()),
            check("negative control: an untracked anchor drifts > 50 px", static_err > 50, static_err)], [out]


# =============================================================================================== DOC


def soffice(wd, *args, env=None, timeout=90):
    """Headless LibreOffice with a private profile inside the work folder (parallel runs never share a lock)."""
    prof = "file://" + str(Path(wd) / "lo_profile")
    return run(["soffice", "-env:UserInstallation=" + prof, "--headless", "--norestore", *args], timeout=timeout,
               env=env or dict(os.environ, HOME=str(wd)), cwd=wd)


def pdf_text(p):
    return run(["pdftotext", "-layout", p, "-"]).stdout


def pdf_fonts(p, env=None):
    return run(["pdffonts", p], env=env).stdout


def render_pdf(p, page=0, scale=2.0):
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(p))
    img = doc[page].render(scale=scale).to_pil()
    n = len(doc)
    doc.close()
    return img, n


@card("DOC-03")
def openpyxl_recalc(task, wd):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["item", "qty", "price", "total"])
    for i, (q, pr) in enumerate([(10, 120), (4, 250), (7, 180)], start=2):
        ws.append(["p%d" % i, q, pr, "=B%d*C%d" % (i, i)])
    ws["D5"] = "=SUM(D2:D4)"
    ws["E5"] = "=ROUND(D3/D5,4)"
    book = Path(wd) / "book.xlsx"
    wb.save(book)
    before = openpyxl.load_workbook(book, data_only=True).active["D5"].value
    soffice(wd, "--convert-to", "xlsx", "--outdir", str(Path(wd) / "recalc"), str(book))
    after = openpyxl.load_workbook(Path(wd) / "recalc/book.xlsx", data_only=True).active
    return [check("formulas computed by the LibreOffice round trip: SUM = 3460", after["D5"].value == 3460, after["D5"].value, 3460),
            check("dependent formula ROUND(D3/D5, 4) = 0.289", abs(after["E5"].value - 0.289) < 1e-9, after["E5"].value, 0.289),
            check("row formula B2*C2 = 1200", after["D2"].value == 1200, after["D2"].value),
            check("negative control: before recalculation data_only returns None", before is None, before)], [Path(wd) / "recalc/book.xlsx"]


AR_TITLE = "تقرير المبيعات"
AR_BODY = "ارتفعت المبيعات في الربع الثالث"


@card("DOC-05")
def weasyprint_arabic(task, wd):
    import weasyprint
    amiri = FONTS / "Amiri-Regular.ttf"
    css = ("@font-face{font-family:Amiri;src:url(file://%s)} @page{size:A4;margin:16mm} body{font-family:Amiri;font-size:22pt}"
           ".en{direction:ltr;unicode-bidi:isolate}") % amiri
    html = ('<html lang=ar dir=rtl><head><meta charset=utf-8><style>%s</style></head><body><h1>%s</h1><p>%s '
            '<span class=en>Q3 2026</span></p></body></html>') % (css, AR_TITLE, AR_BODY)
    out = Path(wd) / "report.pdf"
    weasyprint.HTML(string=html, base_url=str(wd)).write_pdf(out)
    fonts = pdf_fonts(out)
    txt = pdf_text(out)
    img, _ = render_pdf(out, 0, 1.0)
    a = _np().asarray(img.convert("L")).astype(float)
    b = ink_bbox(a[:300], 255, 60)
    plain = Path(wd) / "nofont.pdf"
    weasyprint.HTML(string=html.replace(css, "body{font-size:22pt}"), base_url=str(wd)).write_pdf(plain)
    return [check("Amiri embedded as a subset", "Amiri" in fonts and "+" in fonts.split("Amiri")[0].split()[-1] if "Amiri" in fonts else False,
                  fonts.strip().splitlines()[-1] if fonts.strip() else ""),
            check("Arabic words extract from the PDF text layer", all(w in txt for w in ("المبيعات", "الربع")), txt.strip()[:80]),
            check("RTL: the title's ink is right-aligned on the page", b is not None and a.shape[1] - b[2] < 60 and b[0] > 3 * (a.shape[1] - b[2]),
                  [b, a.shape[1]]),
            check("negative control: without @font-face no Amiri is embedded", "Amiri" not in pdf_fonts(plain))], [out]


def _ink_mask(img):
    """Ink of a text line, cropped to its bounding box, resized to 300x70 and blurred (sigma 3) for comparison."""
    np = _np()
    import cv2
    a = np.asarray(img.convert("L")).astype(float)
    b = ink_bbox(a, 255, 80)
    m = (a[b[1]:b[3], b[0]:b[2]] < 128).astype("float32")
    return cv2.GaussianBlur(cv2.resize(m, (300, 70), interpolation=cv2.INTER_AREA), (0, 0), 3)


def _iou(a, b):
    """Cosine similarity of two blurred ink masks (1 = same glyph shapes in the same order)."""
    return float((a * b).sum() / math.sqrt((a * a).sum() * (b * b).sum()))


@card("DOC-07")
def reportlab_arabic(task, wd):
    import arabic_reshaper
    from bidi.algorithm import get_display
    from PIL import Image, ImageDraw
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    pdfmetrics.registerFont(TTFont("Amiri", str(FONTS / "Amiri-Regular.ttf")))
    out = Path(wd) / "contact.pdf"
    c = canvas.Canvas(str(out), pagesize=(400, 200))
    c.setFont("Amiri", 22)
    shaped = get_display(arabic_reshaper.reshape(AR_TITLE))
    c.drawRightString(380, 140, shaped)
    c.drawRightString(380, 50, AR_TITLE)  # the raw string, for the contact-sheet comparison
    c.save()
    img, _ = render_pdf(out, 0, 3.0)
    W, H = img.size
    top, bot = img.crop((0, 0, W, H // 2)), img.crop((0, H // 2, W, H))
    ref = Image.new("L", (900, 200), 255)
    ImageDraw.Draw(ref).text((850, 100), AR_TITLE, font=font("Amiri-Regular.ttf", 66), fill=0, anchor="rm", direction="rtl")
    ref_m = _ink_mask(ref.convert("RGB"))
    iou_shaped, iou_raw = _iou(_ink_mask(top), ref_m), _iou(_ink_mask(bot), ref_m)
    img.save(Path(wd) / "contact.png")
    pres = all(0xFE70 <= ord(ch) <= 0xFEFF or ch == " " for ch in shaped)
    return [check("reshaper output uses Arabic presentation forms (joined glyphs)", pres),
            check("shaped + bidi line matches a HarfBuzz/raqm reference render", iou_shaped > 0.75, iou_shaped, "> 0.75"),
            check("negative control: the raw string draws unjoined and reversed", iou_raw < iou_shaped - 0.2, [iou_raw, iou_shaped])], \
        [out, Path(wd) / "contact.png"]


@card("DOC-08")
def node_office(task, wd):
    res = node_js(wd, "office", r"""const fs=require('fs');
const {Document,Packer,Paragraph}=require('docx');const PptxGenJS=require('pptxgenjs');const ExcelJS=require('exceljs');
const {PDFDocument,StandardFonts}=require('pdf-lib');
(async()=>{
 const doc=new Document({sections:[{children:[new Paragraph('KOSIF node docx 42')]}]});
 fs.writeFileSync('n.docx',await Packer.toBuffer(doc));
 const pp=new PptxGenJS();const s=pp.addSlide();s.addText('KOSIF slide 7',{x:1,y:1,w:6,h:1});await pp.writeFile({fileName:'n.pptx'});
 const wb=new ExcelJS.Workbook();const ws=wb.addWorksheet('S');ws.addRow(['a',3]);ws.addRow(['b',4]);ws.getCell('B3').value={formula:'B1+B2',result:7};
 await wb.xlsx.writeFile('n.xlsx');
 const pdf=await PDFDocument.create();const f=await pdf.embedFont(StandardFonts.Helvetica);const pg=pdf.addPage([300,200]);
 pg.drawText('KOSIF pdf-lib 99',{x:30,y:100,size:18,font:f});pdf.addPage([300,200]);fs.writeFileSync('n.pdf',await pdf.save());
 console.log(JSON.stringify({ok:true}));})();""")
    import docx
    import openpyxl
    import pptx
    import pypdf
    d = " ".join(p.text for p in docx.Document(Path(wd) / "n.docx").paragraphs)
    sl = " ".join(sh.text_frame.text for sh in pptx.Presentation(Path(wd) / "n.pptx").slides[0].shapes if sh.has_text_frame)
    ws = openpyxl.load_workbook(Path(wd) / "n.xlsx").active
    pr = pypdf.PdfReader(Path(wd) / "n.pdf")
    outs = [Path(wd) / n for n in ("n.docx", "n.pptx", "n.xlsx", "n.pdf")]
    return [check("docx from Node reads back in python-docx", "KOSIF node docx 42" in d, d),
            check("pptx from pptxgenjs reads back in python-pptx", "KOSIF slide 7" in sl, sl),
            check("xlsx from exceljs keeps values and the formula", ws["B1"].value == 3 and ws["B3"].value == "=B1+B2", [ws["B1"].value, ws["B3"].value]),
            check("pdf from pdf-lib: 2 pages with the text", len(pr.pages) == 2 and "KOSIF pdf-lib 99" in pr.pages[0].extract_text()),
            check("negative control: an empty docx has no such text", "KOSIF" not in " ".join(p.text for p in docx.Document().paragraphs))], outs


def _office_fixtures(wd, font_name=None):
    import docx
    import openpyxl
    import pptx
    from docx.shared import Pt
    d = docx.Document()
    p = d.add_paragraph()
    r = p.add_run("Quarterly report alpha")
    if font_name:
        r.font.name = font_name
        r.font.size = Pt(20)
    d.add_paragraph("second line beta")
    d.save(Path(wd) / "a.docx")
    pr = pptx.Presentation()
    s = pr.slides.add_slide(pr.slide_layouts[5])
    s.shapes.title.text = "Slide gamma"
    pr.save(Path(wd) / "b.pptx")
    wb = openpyxl.Workbook()
    wb.active.append(["delta", 12])
    wb.save(Path(wd) / "c.xlsx")
    return [Path(wd) / n for n in ("a.docx", "b.pptx", "c.xlsx")]


@card("DOC-09")
def soffice_to_pdf(task, wd):
    files = _office_fixtures(wd)
    outd = Path(wd) / "pdf"
    soffice(wd, "--convert-to", "pdf", "--outdir", str(outd), *map(str, files))
    pdfs = sorted(outd.glob("*.pdf"))
    texts = {p.stem: pdf_text(p) for p in pdfs}
    img, _ = render_pdf(outd / "a.pdf", 0, 1.0)
    png = Path(wd) / "a_page1.png"
    img.save(png)
    ink = ink_bbox(_np().asarray(img.convert("L")).astype(float), 255, 60)
    return [check("one command converts all three files", [p.stem for p in pdfs] == ["a", "b", "c"], [p.name for p in pdfs]),
            check("each PDF carries its text", "alpha" in texts["a"] and "gamma" in texts["b"] and "delta" in texts["c"]),
            check("page rendered to PNG and inked", ink is not None, ink),
            check("negative control: the docx input is not a PDF", files[0].read_bytes()[:4] != b"%PDF" and pdfs[0].read_bytes()[:4] == b"%PDF")], \
        pdfs + [png]


@card("DOC-10")
def private_fontconfig(task, wd):
    fdir = Path(wd) / "fonts"
    fdir.mkdir()
    import shutil
    for n in ("Amiri-Regular.ttf", "Amiri-Bold.ttf"):
        shutil.copy(FONTS / n, fdir / n)
    conf = tw(Path(wd) / "fonts.conf", "<?xml version='1.0'?><!DOCTYPE fontconfig SYSTEM 'fonts.dtd'><fontconfig>"
                                       "<include ignore_missing='yes'>/etc/fonts/fonts.conf</include><dir>%s</dir>"
                                       "<cachedir>%s</cachedir></fontconfig>" % (fdir, Path(wd) / "fc-cache"))
    files = _office_fixtures(wd, "Amiri")
    env = dict(os.environ, HOME=str(wd), FONTCONFIG_FILE=str(conf))
    soffice(wd, "--convert-to", "pdf", "--outdir", str(Path(wd) / "with"), str(files[0]), env=env)
    prof2 = Path(wd) / "p2"
    run(["soffice", "-env:UserInstallation=file://" + str(prof2), "--headless", "--norestore", "--convert-to", "pdf", "--outdir",
         str(Path(wd) / "without"), str(files[0])], timeout=90, env=dict(os.environ, HOME=str(wd)), cwd=wd)
    fw, fo = pdf_fonts(Path(wd) / "with/a.pdf"), pdf_fonts(Path(wd) / "without/a.pdf")
    fc = run(["fc-match", "Amiri"], env=env).stdout
    return [check("fc-match resolves Amiri through the private fonts.conf", "Amiri" in fc, fc.strip()),
            check("LibreOffice PDF embeds Amiri", "Amiri" in fw, [l.split()[0] for l in fw.splitlines()[2:]]),
            check("negative control: without FONTCONFIG_FILE Amiri is substituted", "Amiri" not in fo,
                  [l.split()[0] for l in fo.splitlines()[2:]])], [Path(wd) / "with/a.pdf", conf]


@card("DOC-12")
def pandoc_arabic(task, wd):
    md = tw(Path(wd) / "note.md", "---\ndir: rtl\nlang: ar\n---\n\n# ملاحظة\n\n| المدينة | العدد |\n|---|---|\n| القاهرة | 12 |\n| الرياض | 7 |\n")
    out = Path(wd) / "note.docx"
    run(["pandoc", md, "-o", out])
    back = run(["pandoc", out, "-t", "gfm"]).stdout
    xml = zipfile.ZipFile(out).read("word/document.xml").decode("utf-8")
    sty = zipfile.ZipFile(out).read("word/styles.xml").decode("utf-8")
    plain = tw(Path(wd) / "plain.md", "# x\n\nhello\n")
    pout = Path(wd) / "plain.docx"
    run(["pandoc", plain, "-o", pout])
    pxml = zipfile.ZipFile(pout).read("word/document.xml").decode("utf-8")
    return [check("Arabic table survives md -> docx -> md", all(w in back for w in ("القاهرة", "الرياض", "12", "7")) and "|" in back, back[:120]),
            check("dir: rtl becomes bidi/rtl markup in the docx", "w:bidi" in xml or "w:rtl" in xml),
            check("lang: ar is written into the document language", 'w:bidi="ar"' in sty),
            check("negative control: a document without the front matter has no RTL markup", "w:bidi" not in pxml and "w:rtl" not in pxml)], [out]


def _pdf_pages(path, texts, size=(300, 200)):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(str(path), pagesize=size)
    for t in texts:
        c.setFont("Helvetica", 16)
        c.drawString(30, 100, t)
        c.showPage()
    c.save()
    return Path(path)


@card("DOC-13")
def pypdf_merge_encrypt(task, wd):
    import pypdf
    parts = [_pdf_pages(Path(wd) / "p1.pdf", ["one"]), _pdf_pages(Path(wd) / "p2.pdf", ["two"]),
             _pdf_pages(Path(wd) / "p3.pdf", ["three", "four"])]
    w = pypdf.PdfWriter()
    for p in parts:
        w.append(str(p))
    w.pages[0].rotate(90)
    pw = "kosif-" + "7" * 6
    w.encrypt(user_password=pw, algorithm="AES-256")
    out = Path(wd) / "merged_locked.pdf"
    with open(out, "wb") as f:
        w.write(f)
    r = pypdf.PdfReader(out)
    enc = r.is_encrypted
    bad = pypdf.PdfReader(out).decrypt("wrong")
    ok = r.decrypt(pw)
    texts = [pg.extract_text().strip() for pg in r.pages]
    return [check("3 files -> 4 pages in order", texts == ["one", "two", "three", "four"], texts),
            check("first page /Rotate 90", r.pages[0].get("/Rotate") == 90, r.pages[0].get("/Rotate")),
            check("AES-256 encrypted, the password opens it", enc and int(ok) > 0 and "/AESV3" in str(r.trailer["/Encrypt"]["/CF"])),
            check("negative control: a wrong password does not open it", int(bad) == 0, int(bad))], [out]


@card("DOC-16")
def markitdown_read(task, wd):
    from markitdown import MarkItDown
    import docx
    import openpyxl
    import pptx
    d = docx.Document()
    d.add_paragraph(AR_BODY)
    d.save(Path(wd) / "ar.docx")
    wb = openpyxl.Workbook()
    wb.active.append(["المدينة", "القاهرة"])
    wb.save(Path(wd) / "ar.xlsx")
    pr = pptx.Presentation()
    pr.slides.add_slide(pr.slide_layouts[5]).shapes.title.text = AR_TITLE
    pr.save(Path(wd) / "ar.pptx")
    md = MarkItDown()
    got = {ext: md.convert(str(Path(wd) / ("ar." + ext))).text_content for ext in ("docx", "xlsx", "pptx")}
    out = tw(Path(wd) / "context.md", "\n\n".join("## %s\n%s" % kv for kv in got.items()))
    raw = (Path(wd) / "ar.docx").read_bytes()
    return [check("docx -> Markdown keeps the Arabic", AR_BODY in got["docx"], got["docx"].strip()[:60]),
            check("xlsx -> Markdown table keeps the Arabic", "القاهرة" in got["xlsx"] and "|" in got["xlsx"]),
            check("pptx -> Markdown keeps the Arabic title", AR_TITLE in got["pptx"]),
            check("negative control: the raw .docx bytes do not contain the text (zipped XML)", AR_BODY.encode("utf-8") not in raw)], [out]


def _arabic_scan_pdf(wd):
    from PIL import Image, ImageDraw
    im = Image.new("L", (1240, 600), 255)
    d = ImageDraw.Draw(im)
    d.text((1180, 120), AR_TITLE, font=font("Amiri-Bold.ttf", 90), fill=0, anchor="rm", direction="rtl")
    d.text((60, 320), "Invoice total 4825 EGP", font=font("Poppins-Regular.ttf", 56), fill=0)
    p = Path(wd) / "scan.pdf"
    im.save(p, "PDF", resolution=150)
    return p


@card("DOC-17")
def ocr_scanned_pdf(task, wd):
    import pypdfium2 as pdfium
    import pytesseract
    p = _arabic_scan_pdf(wd)
    layer = pdf_text(p).strip()
    img = pdfium.PdfDocument(str(p))[0].render(scale=300 / 72).to_pil().convert("L")
    os.environ["OMP_THREAD_LIMIT"] = "1"  # tesseract's OpenMP threads thrash on a shared CPU; one thread is faster here
    txt = pytesseract.image_to_string(img, lang="ara+eng", config="--oem 1 --psm 4")
    out = tw(Path(wd) / "ocr.txt", txt)
    digits = re.findall(r"\d{4}", txt)
    return [check("English line recovered", "Invoice total" in txt, txt.strip()[:80]),
            check("digits validated: 4825", "4825" in digits, digits),
            check("Arabic title recovered", "المبيعات" in txt or "تقرير" in txt),
            check("negative control: the scanned PDF has no text layer", layer == "", layer)], [out]


@card("DOC-18")
def contact_sheet(task, wd):
    from PIL import Image, ImageChops
    docs = [_pdf_pages(Path(wd) / ("d%d.pdf" % i), ["document %d" % i, "page b"]) for i in range(3)]
    tiles = []
    for p in docs:
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(str(p))
        for i in range(len(pdf)):
            im = pdf[i].render(scale=2).to_pil().convert("RGB")
            bb = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
            tiles.append((im.size, bb, im.crop(bb)))
        pdf.close()
    tw_ = max(t[2].width for t in tiles) + 20
    th = max(t[2].height for t in tiles) + 20
    cols = 3
    sheet = Image.new("RGB", (tw_ * cols, th * math.ceil(len(tiles) / cols)), (255, 255, 255))
    for k, (_, _, t) in enumerate(tiles):
        sheet.paste(t, ((k % cols) * tw_ + 10, (k // cols) * th + 10))
    out = Path(wd) / "contact.png"
    sheet.quantize(128).save(out)
    crops_smaller = all(bb[2] - bb[0] < sz[0] and bb[3] - bb[1] < sz[1] for sz, bb, _ in tiles)
    full = tiles[0][0]
    return [check("six pages tiled", len(tiles) == 6, len(tiles)),
            check("each tile cropped to its ink", crops_smaller),
            check("contact sheet < 300 KB after quantize(128)", out.stat().st_size < 300_000, out.stat().st_size),
            check("negative control: an uncropped page keeps its full size", (0, 0) + tuple(full) != tiles[0][1], [full, tiles[0][1]])], [out]


@card("DOC-19")
def pymupdf_read(task, wd):
    import pymupdf
    p = _pdf_pages(Path(wd) / "in.pdf", ["PyMuPDF reads this line", ""])
    doc = pymupdf.open(p)
    t0, t1 = doc[0].get_text().strip(), doc[1].get_text().strip()
    out = Path(wd) / "p.png"
    doc[0].get_pixmap().save(out)
    words = doc[0].get_text("words")
    a = load_rgb(out)
    return [check("page text extracted", t0 == "PyMuPDF reads this line", t0),
            check("word boxes returned (4 words)", len(words) == 4 and words[0][4] == "PyMuPDF", len(words)),
            check("pixmap rendered with ink", (a.min(axis=-1) < 100).sum() > 100),
            check("negative control: the blank page has no text", t1 == "", t1)], [out]


@card("DOC-20")
def pdfplumber_tables(task, wd):
    import arabic_reshaper
    import pdfplumber
    from bidi.algorithm import get_display
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    pdfmetrics.registerFont(TTFont("Amiri", str(FONTS / "Amiri-Regular.ttf")))
    p = Path(wd) / "table.pdf"
    c = canvas.Canvas(str(p), pagesize=(400, 300))
    rows = [["city", "count"], ["Cairo", "12"], ["Riyadh", "7"]]
    for i in range(4):
        c.line(50, 250 - i * 30, 330, 250 - i * 30)
    for x in (50, 190, 330):
        c.line(x, 250, x, 160)
    for r, row in enumerate(rows):
        for k, v in enumerate(row):
            c.setFont("Helvetica", 12)
            c.drawString(60 + k * 140, 230 - r * 30, v)
    c.setFont("Amiri", 16)
    c.drawString(60, 100, get_display(arabic_reshaper.reshape("القاهرة")))
    c.save()
    with pdfplumber.open(p) as pdf:
        pg = pdf.pages[0]
        tbl = pg.extract_tables()
        words = pg.extract_words()
        ar = [w for w in words if any("؀" <= ch <= "ۿ" or "ﹰ" <= ch <= "﻿" for ch in w["text"])]
    cairo = [w for w in words if w["text"] == "Cairo"][0]
    ar_raw = ar[0]["text"] if ar else ""
    fixed = arabic_reshaper.reshape("القاهرة")
    out = jw(Path(wd) / "tables.json", {"tables": tbl, "cairo_xy": [cairo["x0"], cairo["top"]], "arabic_raw": ar_raw})
    return [check("table extracted cell by cell", tbl and tbl[0] == rows, tbl),
            check("word coordinates: 'Cairo' at x0 = 60 pt, top ~ 91 pt", abs(cairo["x0"] - 60) < 1 and abs(cairo["top"] - 91) < 3,
                  [cairo["x0"], cairo["top"]]),
            check("reversing the extracted Arabic cell restores logical order", ar_raw[::-1] == fixed, [ar_raw, fixed]),
            check("negative control: the raw Arabic extraction is reversed", ar_raw != fixed)], [out]


@card("DOC-21")
def tabula_tables(task, wd):
    import tabula
    from reportlab.pdfgen import canvas
    p = Path(wd) / "grid.pdf"
    c = canvas.Canvas(str(p), pagesize=(400, 300))
    rows = [["sku", "units", "price"], ["A1", "10", "2.50"], ["B2", "4", "9.75"], ["C3", "7", "1.20"]]
    for i in range(5):
        c.line(50, 250 - i * 30, 350, 250 - i * 30)
    for x in (50, 150, 250, 350):
        c.line(x, 250, x, 130)
    for r, row in enumerate(rows):
        for k, v in enumerate(row):
            c.drawString(60 + k * 100, 230 - r * 30, v)
    c.save()
    dfs = tabula.read_pdf(str(p), pages=1, lattice=True, silent=True)
    df = dfs[0]
    out = Path(wd) / "table.csv"
    df.to_csv(out, index=False)
    total = float((df["units"].astype(float) * df["price"].astype(float)).sum())
    blank = Path(wd) / "blank.pdf"
    bc = canvas.Canvas(str(blank), pagesize=(400, 300))
    bc.drawString(60, 200, "plain prose with no ruled table")
    bc.save()
    none = tabula.read_pdf(str(blank), pages=1, lattice=True, silent=True)
    return [check("tabula (Java) found the ruled table with its header", list(df.columns) == ["sku", "units", "price"], list(df.columns)),
            check("three data rows", len(df) == 3, len(df)),
            check("values usable: sum(units*price) = 72.4", abs(total - 72.4) < 1e-6, total),
            check("negative control: a page without ruling lines yields no table", len(none) == 0, len(none))], [out]


def _skill_dirs():
    roots = [Path("/mnt/skills/public"), Path.home() / ".claude/skills"]
    out = []
    for r in roots:
        if r.is_dir():
            out += [p.parent for p in r.rglob("SKILL.md")]
    return out


def _pick_skill(request, skills):
    words = set(re.findall(r"[a-z]+", request.lower()))
    best, score = None, 0
    for d in skills:
        head = (d / "SKILL.md").read_text(encoding="utf-8", errors="replace")[:1500].lower()
        m = re.search(r"^description:(.*)$", head, re.M)
        desc = (m.group(1) if m else head)
        s = sum(desc.count(w) for w in words if len(w) > 3)
        if d.name in words:
            s += 10
        if s > score:
            best, score = d, s
    return best, score


@card("DOC-25")
def document_skills(task, wd):
    skills = _skill_dirs()
    pick, score = _pick_skill("edit this word docx with tracked changes and a template", skills)
    body = (pick / "SKILL.md").read_text(encoding="utf-8", errors="replace") if pick else ""
    none, nscore = _pick_skill("render a kinetic typography motion video", [d for d in skills if d.name in ("docx", "xlsx", "pptx", "pdf")])
    out = jw(Path(wd) / "skill_pick.json", {"listed": sorted({d.name for d in skills}), "picked": str(pick), "score": score})
    return [check("the session lists ready-made document skills", {"docx", "xlsx", "pptx", "pdf"} <= {d.name for d in skills}),
            check("a Word tracked-changes request picks the docx skill", pick is not None and pick.name == "docx", str(pick)),
            check("the loaded skill carries the tracked-changes recipe", "tracked change" in body.lower() or "track" in body.lower()),
            check("negative control: a video request matches no document skill strongly", nscore < score / 2, [nscore, score])], [out]


@card("DOC-27")
def sandbox_office_probe(task, wd):
    import importlib.util
    mods = ["docx", "openpyxl", "pptx", "reportlab", "pypdf"]
    probe = {m: importlib.util.find_spec(m) is not None for m in mods}
    probe["nonexistent_module_xyz"] = importlib.util.find_spec("nonexistent_module_xyz") is not None
    files = _office_fixtures(wd)
    pdf = _pdf_pages(Path(wd) / "d.pdf", ["sandbox pdf"])
    import docx
    import openpyxl
    import pptx
    import pypdf
    ok_read = ("alpha" in docx.Document(files[0]).paragraphs[0].text and pptx.Presentation(files[1]).slides[0].shapes.title.text == "Slide gamma"
               and openpyxl.load_workbook(files[2]).active["A1"].value == "delta" and "sandbox" in pypdf.PdfReader(pdf).pages[0].extract_text())
    bundled = sorted(p.name for p in FONTS.glob("*.ttf"))
    out = jw(Path(wd) / "probe.json", {"imports": probe, "fonts": bundled})
    return [check("quick import probe of the preinstalled libraries", all(probe[m] for m in mods), probe),
            check("docx/xlsx/pptx/pdf created and read back with them", ok_read),
            check("bundled fonts available without apt", "Amiri-Regular.ttf" in bundled and "Poppins-Bold.ttf" in bundled),
            check("negative control: the probe reports a missing module as missing", probe["nonexistent_module_xyz"] is False)], [out] + files


@card("DOC-31")
def slidev_export(task, wd):
    nm = Path(wd) / "node_modules"
    nm.mkdir()
    for pkg in ("playwright-chromium", "playwright-core"):
        (nm / pkg).symlink_to(PWC / pkg)
    md = tw(Path(wd) / "slides.md", "---\ntheme: none\n---\n\n# Alpha deck\n\n---\n\n# Beta point\n\n---\n\n# Gamma end\n")
    run(["slidev", "export", md.name, "--output", "deck.pdf", "--timeout", "30000"], timeout=120, cwd=wd,
        env=dict(os.environ, HOME=str(wd)))
    out = Path(wd) / "deck.pdf"
    import pypdf
    r = pypdf.PdfReader(out)
    texts = [pg.extract_text() for pg in r.pages]
    return [check("Markdown deck exported to 3 PDF pages", len(r.pages) == 3, len(r.pages)),
            check("each slide carries its heading", "Alpha" in texts[0] and "Beta" in texts[1] and "Gamma" in texts[2], texts),
            check("negative control: the Markdown source has no PDF pages", not md.read_bytes().startswith(b"%PDF"))], [out]


@card("DOC-32")
def marp_export(task, wd):
    md = tw(Path(wd) / "deck.md", "---\nmarp: true\n---\n\n# Opening slide\n\n---\n\n# Second slide\n\n- point one\n")
    env = dict(os.environ, CHROME_PATH=CHROME, HOME=str(wd))
    for ext in ("pdf", "pptx", "html"):
        run(["marp", md, "--" + ext, "--allow-local-files", "-o", Path(wd) / ("deck." + ext)], timeout=90, env=env)
    import pypdf
    import pptx
    r = pypdf.PdfReader(Path(wd) / "deck.pdf")
    pr = pptx.Presentation(Path(wd) / "deck.pptx")
    html = (Path(wd) / "deck.html").read_text(encoding="utf-8")
    return [check("PDF with 2 slides", len(r.pages) == 2 and "Opening" in r.pages[0].extract_text(), len(r.pages)),
            check("PPTX with 2 slides", len(pr.slides) == 2, len(pr.slides)),
            check("HTML deck with both sections", html.count("<section") >= 2 and "Second slide" in html),
            check("negative control: the Markdown alone is not a deck file", md.read_bytes()[:4] not in (b"%PDF", b"PK\x03\x04"))], \
        [Path(wd) / "deck.pdf", Path(wd) / "deck.pptx"]


@card("DOC-33")
def mermaid_render(task, wd):
    src = tw(Path(wd) / "flow.mmd", "graph LR\n  A[Brief] --> B[Storyboard]\n  B --> C[Render]\n  C --> D[QA]\n")
    cfg = jw(Path(wd) / "pp.json", {"executablePath": CHROME, "args": ["--no-sandbox"]})
    env = dict(os.environ, HOME=str(wd))
    run(["mmdc", "-i", src, "-o", Path(wd) / "flow.svg", "-p", cfg], timeout=90, env=env)
    run(["mmdc", "-i", src, "-o", Path(wd) / "flow.png", "-p", cfg, "-b", "white"], timeout=90, env=env)
    svg = (Path(wd) / "flow.svg").read_text(encoding="utf-8")
    a = load_rgb(Path(wd) / "flow.png")
    b = ink_bbox(a, (255, 255, 255), 40)
    return [check("SVG has the four node labels", all(w in svg for w in ("Brief", "Storyboard", "Render", "QA"))),
            check("three edges drawn", len(re.findall(r'class="[^"]*flowchart-link', svg)) == 3 or svg.count("marker-end") >= 3),
            check("left-to-right PNG is wider than tall", b is not None and (b[2] - b[0]) > 2 * (b[3] - b[1]), b),
            check("negative control: the text source is not an SVG", "<svg" not in src.read_text())], [Path(wd) / "flow.svg", Path(wd) / "flow.png"]


# =============================================================================================== TYPE

MONO = "jetbrains-mono-latin-700-normal.woff2"


def canvas_img(W, H, bg=(255, 255, 255)):
    from PIL import Image
    return Image.new("RGB", (W, H), bg)


def arr(im):
    return _np().asarray(im).astype(float)


def mask_bbox(a, rgb, tol=40):
    np = _np()
    m = color_mask(a, rgb, tol)
    ys, xs = np.nonzero(m)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


NUM_WORDS = {"two times": "2x", "three times": "3x", "ten times": "10x"}
STOP = set("a an the and or but our your it is are be to of for in on at with than that this every one old new nothing extra "
           "today its".split())


def fit_copy(narration, aspect="9:16"):
    """TYPE-02: one idea per screen; a hero stat plus a few content words; lines 14-22 chars at phrase boundaries."""
    text = narration.lower()
    for k, v in NUM_WORDS.items():
        text = text.replace(k, v)
    phrases = [p.strip() for p in re.split(r",| and ", text) if p.strip()]
    cap = 7 if aspect == "9:16" else 12
    hero_phrase = next((p for p in phrases if re.search(r"\d+x|\$\d|\d+%", p)), phrases[0])
    words = [w for w in re.findall(r"[\w$%]+", hero_phrase) if w not in STOP]
    stat = next(w for w in words if re.match(r"\d+x|\$\d|\d+%", w))
    i = words.index(stat)
    core = words[max(0, i - 1):i + 2]  # verb + stat + adjective: "renders 2x faster"
    lines = [" ".join(core).capitalize()]
    rest = [w for w in re.findall(r"[\w$%]+", phrases[-1]) if w not in STOP][:3]
    if rest and len(" ".join(rest)) >= 10:
        lines.append(" ".join(rest).capitalize())
    lines = [l for l in lines if 14 <= len(l) <= 22] or lines[:1]  # portrait line length 14-22 characters
    words_out = sum(len(l.split()) for l in lines)
    while words_out > min(cap, 6):
        lines.pop()
        words_out = sum(len(l.split()) for l in lines)
    return lines, stat


@card("TYPE-02")
def hero_copy(task, wd):
    narration = "Our new pipeline renders every video two times faster than the old one, and it costs nothing extra to switch today"
    lines, stat = fit_copy(narration)
    f = font("Poppins-Bold.ttf", 44)
    from PIL import ImageDraw
    im = canvas_img(540, 960, (15, 15, 20))
    d = ImageDraw.Draw(im)
    y = 380
    for ln in lines:
        d.text((270, y), ln, font=f, fill=(250, 250, 250), anchor="mm")
        y += 70
    out = Path(wd) / "screen_916.png"
    im.save(out)
    a = arr(im).mean(axis=-1)
    rows = (a > 128).any(axis=1)
    bands = int(((rows[1:].astype(int) - rows[:-1].astype(int)) == 1).sum())
    nwords = sum(len(l.split()) for l in lines)
    narr_words = narration.lower().split()
    overlap = sum(1 for w in " ".join(lines).lower().split() if w in narr_words) / len(narr_words)
    naive_words = len(narration.split())
    jw(Path(wd) / "copy.json", {"lines": lines, "stat": stat})
    return [check("<= 7 visible words on 9:16 and <= 6 on the display face", nwords <= 6, nwords),
            check("portrait lines 14-22 characters", all(14 <= len(l) <= 22 for l in lines), [len(l) for l in lines]),
            check("hero stat '2x' leads the copy", stat == "2x" and "2x" in lines[0], lines),
            check("not a re-print of the narration (< 30 % of its words)", overlap < 0.3, overlap),
            check("rendered as %d separate lines" % len(lines), bands == len(lines), bands),
            check("negative control: printing the narration breaks the 7-word cap", naive_words > 7, naive_words)], [out]


def hold_after_landing(line):
    return 0.3 + 0.06 * len(line)


def card_seconds(n_words):
    return max(0.5, 0.4 * n_words)


@card("TYPE-03")
def card_timing(task, wd):
    np = _np()
    from PIL import ImageDraw
    fps, W, H = 30, 480, 270
    cards = ["Ship it faster", "with one click", "kosif.dev/start"]
    cols = [(230, 60, 60), (60, 160, 230), (60, 190, 90)]
    ent, ext = 0.35, 0.25
    plan, t = [], 0.0
    for c in cards:
        is_url = "/" in c or "." in c
        dur = max(card_seconds(len(c.split())), ent + hold_after_landing(c), 1.7 if is_url else 0)
        dur = math.ceil(dur * fps - 1e-9) / fps  # snap up to the frame grid
        plan.append((c, t, t + dur))
        t += dur
    f = font("Poppins-Bold.ttf", 36)
    frames = []
    for i in range(int(round(t * fps))):
        tt = i / fps
        im = canvas_img(W, H)
        d = ImageDraw.Draw(im)
        for (c, a, b), col in zip(plan, cols):
            if a <= tt < b:
                y = 135
                if tt < a + ent:
                    y += 30 * (1 - ease_out_cubic((tt - a) / ent))
                elif tt > b - ext:
                    y -= 30 * ease_in_cubic((tt - (b - ext)) / ext)  # exit opposite to the entrance (it came from below)
                d.text((240, y), c, font=f, fill=col, anchor="mm")
        frames.append(arr(im))
    out = write_video(Path(wd) / "cards.mp4", frames)
    fr = read_video(out)
    vis = [[bool(color_mask(f_, col, 40).sum() > 50) for f_ in fr] for col in cols]
    secs = [sum(v) / fps for v in vis]
    ys = [[centroid(color_mask(f_, cols[0], 40))[1] if v else None for f_, v in zip(fr, vis[0])]]
    yy = [y for y in ys[0] if y is not None]
    settle = [k for k in range(1, len(yy)) if abs(yy[k] - yy[-1 if False else k]) >= 0]  # noqa: F841
    moving_in = sum(1 for k in range(1, len(yy)) if yy[k] < yy[k - 1] - 0.3 and yy[k] > min(yy) + 0.5 and k < len(yy) / 2)
    moving_out = sum(1 for k in range(len(yy) // 2, len(yy)) if yy[k] < yy[k - 1] - 0.3)
    naive = [0.3, 0.3, 0.3]
    need = [max(card_seconds(len(c.split())), hold_after_landing(c)) for c in cards]
    return [check("hold formula: 0.3 s + 0.06 s x 14 chars = 1.14 s", abs(hold_after_landing(cards[0]) - 1.14) < 1e-9),
            check("card 1 on screen >= 0.35 + 1.14 s (measured)", secs[0] >= 1.45, secs[0]),
            check("URL card holds >= 1.7 s (measured)", secs[2] >= 1.69, secs[2]),
            check("exit (250 ms) is shorter than the entrance (350 ms), measured in moving frames", 0 < moving_out < moving_in + 3 and ext < ent,
                  [moving_in, moving_out]),
            check("negative control: naive 0.3 s cards are shorter than the readability minimum", all(a < b for a, b in zip(naive, need)),
                  [naive, need])], [out]


@card("TYPE-11")
def offline_latin_fonts(task, wd):
    from fontTools.ttLib import TTFont
    want = {"space-grotesk-latin-500-normal.woff2": ("Space Grotesk", 500), "space-grotesk-latin-700-normal.woff2": ("Space Grotesk", 700),
            "jetbrains-mono-latin-500-normal.woff2": ("JetBrains Mono", 500), "jetbrains-mono-latin-700-normal.woff2": ("JetBrains Mono", 700),
            "cairo-latin-600-normal.woff2": ("Cairo", 600), "cairo-latin-800-normal.woff2": ("Cairo", 800)}
    meta = {}
    for fn, (fam, wt) in want.items():
        t = TTFont(str(FONTS / fn))
        meta[fn] = {"family": t["name"].getDebugName(16) or t["name"].getDebugName(1), "weight": t["OS/2"].usWeightClass,
                    "kb": round((FONTS / fn).stat().st_size / 1000, 1)}
    html = Path(wd) / "hud.html"
    tw(html, """<!doctype html><meta charset=utf-8><style>
@font-face{font-family:Grotesk;font-weight:700;src:url(file://%s/space-grotesk-latin-700-normal.woff2) format('woff2')}
@font-face{font-family:Mono;font-weight:700;src:url(file://%s/jetbrains-mono-latin-700-normal.woff2) format('woff2')}
.stat{font:700 50px Mono;font-variant-numeric:tabular-nums;letter-spacing:.08em}.g{font:700 50px Grotesk}
</style><span id=a class=stat>1111</span><br><span id=b class=stat>0000</span><br><span id=c class=g>1111</span><br><span id=d class=g>0000</span>
<br><span class=g style="font-family:Grotesk,serif">Mark</span>""" % (FONTS, FONTS))
    res = node_js(wd, "hud", PW_HEAD + """(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+%s);
await p.evaluate(()=>document.fonts.ready);const w=id=>document.getElementById(id).getBoundingClientRect().width;
const r=await p.evaluate(()=>({a:document.getElementById('a').getBoundingClientRect().width,b:document.getElementById('b').getBoundingClientRect().width,
c:document.getElementById('c').getBoundingClientRect().width,d:document.getElementById('d').getBoundingClientRect().width,
loaded:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)}));
await p.screenshot({path:'hud.png'});console.log(JSON.stringify(r));await b.close()})();""" % json.dumps(str(html)))
    out = jw(Path(wd) / "fonts.json", {"fonts": meta, "browser": res, "montserrat": "not present in this checkout"})
    sizes_ok = all(12.5 <= meta[f]["kb"] <= 13.5 for f in meta if "grotesk" in f) and all(21.5 <= meta[f]["kb"] <= 22.3 for f in meta if "mono" in f)
    return [check("family names and weights read from the woff2 files", all(meta[f]["family"].startswith(want[f][0]) and meta[f]["weight"] == want[f][1]
                                                                            for f in want), {f: (m["family"], m["weight"]) for f, m in meta.items()}),
            check("file sizes: Grotesk ~12.8-13.3 KB, Mono ~21.8-22 KB", sizes_ok, {f: m["kb"] for f, m in meta.items()}),
            check("both faces load offline in Chromium from file://", {"Grotesk", "Mono"} <= set(res["loaded"]), res["loaded"]),
            check("HUD stat uses tabular figures: 1111 and 0000 have equal width", abs(res["a"] - res["b"]) < 0.5, [res["a"], res["b"]]),
            check("negative control: Grotesk without tabular-nums sets 1111 narrower", res["c"] < res["d"] - 2, [res["c"], res["d"]])], \
        [out, Path(wd) / "hud.png"]


def draw_tracked(d, xy, text, f, spacing, fill):
    """Draw text with extra letter-spacing (px), glyph by glyph using real advances."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + spacing
    return x


@card("TYPE-20")
def tracking_collapse(task, wd):
    from PIL import ImageDraw
    fps, size, word = 30, 60, "PREMIUM"
    f = font("Poppins-Bold.ttf", size)
    em0, dur = 0.08, 0.6
    frames, widths = [], []
    for i in range(int(1.0 * fps)):
        t = i / fps
        sp = em0 * size * (1 - ease_out_cubic(min(1, t / dur)))
        im = canvas_img(520, 120)
        d = ImageDraw.Draw(im)
        draw_tracked(d, (20, 20), word, f, sp, (20, 20, 20))
        frames.append(arr(im))
    out = write_video(Path(wd) / "tracking.mp4", frames)
    fr = read_video(out)
    for a in fr:
        b = ink_bbox(a, (255, 255, 255), 100)
        widths.append(b[2] - b[0])
    expect0 = (len(word) - 1) * em0 * size
    settle = next(k for k in range(len(widths)) if widths[k] == widths[-1])
    static = canvas_img(520, 120)
    draw_tracked(ImageDraw.Draw(static), (20, 20), word, f, 0, (20, 20, 20))
    sb = ink_bbox(arr(static), (255, 255, 255), 100)
    return [check("first frame wider by (n-1) x 0.08 em = 28.8 px", abs((widths[0] - widths[-1]) - expect0) <= 2, widths[0] - widths[-1], expect0),
            check("width collapses monotonically", all(widths[k + 1] <= widths[k] + 1 for k in range(len(widths) - 1))),
            check("settles to final tracking by 600 ms", settle <= int(dur * fps) + 1, settle / fps, dur),
            check("negative control: untracked text has no collapse (start width == final)", (sb[2] - sb[0]) == widths[-1] != widths[0])], [out]


@card("TYPE-21")
def stack_and_replace(task, wd):
    from PIL import ImageDraw
    fps, W, H = 30, 480, 300
    f = font("Poppins-Bold.ttf", 34)
    lines = [("First line", (230, 60, 60)), ("Second line", (60, 140, 230)), ("Third line", (60, 180, 90)), ("Fourth line", (200, 120, 20))]
    lh, top = 80, 40
    stagger, swap_at, swap_d = 0.12, 1.5, 0.35
    frames = []
    for i in range(int(2.2 * fps)):
        t = i / fps
        im = canvas_img(W, H)
        d = ImageDraw.Draw(im)
        shift = 80 * ease_out_cubic((t - swap_at) / swap_d) if t >= swap_at else 0
        for k, (txt, col) in enumerate(lines[:3]):
            a = k * stagger
            if t >= a:
                y = top + k * lh + 20 * (1 - ease_out_cubic((t - a) / 0.3)) - shift
                if k == 0 and t >= swap_at:
                    if y < top - 40:
                        continue
                d.text((40, y), txt, font=f, fill=col)
        if t >= swap_at:
            y = top + 3 * lh - shift + (1 - ease_out_cubic((t - swap_at) / swap_d)) * 20
            d.text((40, y), lines[3][0], font=f, fill=lines[3][1])
        frames.append(arr(im))
    out = write_video(Path(wd) / "stack.mp4", frames)
    fr = read_video(out)
    first_seen = [next(i for i, a in enumerate(fr) if color_mask(a, c, 40).sum() > 30) for _, c in lines[:3]]
    gaps = [(first_seen[k + 1] - first_seen[k]) / fps for k in range(2)]
    y_before = centroid(color_mask(fr[int(swap_at * fps) - 1], lines[1][1], 40))[1]
    y_after = centroid(color_mask(fr[int((swap_at + swap_d) * fps) + 1], lines[1][1], 40))[1]
    top_gone = color_mask(fr[-1], lines[0][1], 40).sum() == 0
    new_in = color_mask(fr[-1], lines[3][1], 40).sum() > 30
    done = next(i for i in range(int(swap_at * fps), len(fr)) if abs(centroid(color_mask(fr[i], lines[1][1], 40))[1] - y_after) < 0.6) / fps
    still = color_mask(fr[int(swap_at * fps) - 1], lines[3][1], 40).sum()
    return [check("lines enter 120 ms apart (measured first visible frames)", all(abs(g - 0.12) < 0.04 for g in gaps), gaps),
            check("on the swap the stack slides up 80 px", abs((y_before - y_after) - 80) < 2, y_before - y_after),
            check("top line exits and the new line enters at the bottom", top_gone and new_in),
            check("swap completes within 350 ms", done - swap_at <= swap_d + 0.04, done - swap_at),
            check("negative control: before the beat the fourth line is absent", still == 0, int(still))], [out]


@card("TYPE-24")
def mask_wipe_word(task, wd):
    np = _np()
    from PIL import ImageDraw
    fps, W, H = 30, 900, 300
    f = font("Poppins-Bold.ttf", 200)
    base = canvas_img(W, H)
    ImageDraw.Draw(base).text((W / 2, H / 2), "BOLD", font=f, fill=(20, 20, 20), anchor="mm")
    word = arr(base)
    bb = ink_bbox(word, (255, 255, 255), 100)
    x0, x1 = bb[0], bb[2]
    t_in, hold, t_out = 0.45, 1.0, 0.25
    frames = []
    for i in range(int((t_in + hold + t_out + 0.1) * fps)):
        t = i / fps
        fr_ = np.full_like(word, 255.0)
        if t < t_in:
            lo, hi = x0, x0 + (x1 - x0) * ease_out_quart(t / t_in)
        elif t < t_in + hold:
            lo, hi = x0, x1
        else:
            lo, hi = x0 + (x1 - x0) * ease_in_cubic((t - t_in - hold) / t_out), x1
        lo, hi = int(round(lo)), int(round(hi))
        fr_[:, lo:hi] = word[:, lo:hi]
        frames.append(fr_)
    out = write_video(Path(wd) / "wipe.mp4", frames)
    fr = read_video(out)
    full = (word.min(axis=-1) < 128).sum()
    frac = [float((a.min(axis=-1) < 128).sum() / full) for a in fr]
    at_end = frac[int(round(t_in * fps))]
    before_end = frac[int(round(0.25 * fps))]
    gone = next(i for i in range(len(frac)) if i / fps > t_in + hold and frac[i] < 0.01) / fps
    mid_in = fr[int(0.15 * fps)]
    b_in = ink_bbox(mid_in, (255, 255, 255), 100)
    mid_out = fr[int((t_in + hold + 0.12) * fps)]
    b_out = ink_bbox(mid_out, (255, 255, 255), 100)
    return [check("200 px word fully revealed at 450 ms, not before 250 ms", at_end > 0.999 and before_end < 0.99, [before_end, at_end]),
            check("ease-out quart: > 60 % revealed by a third of the wipe", frac[int(0.15 * fps)] > 0.6, frac[int(0.15 * fps)]),
            check("wipe in reveals left to right (reading direction)", b_in[0] <= x0 + 2 and b_in[2] < x1 - 20, [b_in, x0, x1]),
            check("held 1 s, then wiped out the same direction in 250 ms", b_out[0] > x0 + 20 and b_out[2] >= x1 - 2 and gone - (t_in + hold) <= t_out + 0.05,
                  [b_out, gone]),
            check("negative control: the unmasked word is fully visible at t = 0", frac[0] < 0.05 and full > 0, frac[0])], [out]


@card("TYPE-31")
def type_on_caret(task, wd):
    from PIL import ImageDraw
    fps, cps = 60, 46
    text = "Render the whole film in one click"
    dur = min(1.2, max(0.5, len(text) / cps))
    ease = bezier(0.5, 1, 0.89, 1)
    f = font(MONO, 24)
    adv = f.getlength("M")
    hold = 1.0
    frames, counts = [], []
    for i in range(int((dur + hold) * fps)):
        t = i / fps
        n = len(text) if t >= dur else int(round(len(text) * ease(t / dur)))
        counts.append(n)
        im = canvas_img(int(adv * (len(text) + 3)), 60)
        d = ImageDraw.Draw(im)
        d.text((10, 15), text[:n], font=f, fill=(20, 20, 20))
        if int(t * 2 * 2) % 2 == 0:  # caret blinks at 2 Hz (on 250 ms, off 250 ms)
            d.text((10 + adv * n, 15), "|", font=f, fill=(200, 30, 30))
        frames.append(arr(im))
    out = write_video(Path(wd) / "typeon.mp4", frames, fps)
    fr = read_video(out)
    import numpy as np
    meas = []
    for a in fr:
        ink = (a[:, :, 1] < 128) & (a[:, :, 0] < 128)
        cells = [ink[:, int(10 + k * adv):int(10 + (k + 1) * adv)].any() for k in range(len(text))]
        nonspace = [k for k, ch in enumerate(text) if ch != " "]
        last = max([k for k in nonspace if cells[k]], default=-1)
        meas.append(last + 1)
    fifth = int(dur / 5 * fps)
    share = meas[fifth] / len(text)
    caret = [bool(color_mask(a, (200, 30, 30), 60).sum() > 5) for a in fr[int(dur * fps):]]
    toggles = sum(1 for k in range(1, len(caret)) if caret[k] != caret[k - 1])
    def cells_at(n):
        im = canvas_img(int(adv * (len(text) + 3)), 60)
        ImageDraw.Draw(im).text((10, 15), text[:n], font=f, fill=(20, 20, 20))
        a = arr(im)
        ink = (a[:, :, 1] < 128) & (a[:, :, 0] < 128)
        cl = [ink[:, int(10 + k * adv):int(10 + (k + 1) * adv)].any() for k in range(len(text))]
        return (max([k for k, ch in enumerate(text) if ch != " " and cl[k]], default=-1) + 1) / len(text)
    lin_share = cells_at(int(round(len(text) * (fifth / fps) / dur)))
    return [check("duration clamp(len/46, 0.5, 1.2) = %.3f s" % dur, abs(dur - len(text) / cps) < 1e-9 and 0.5 <= dur <= 1.2, dur),
            check("eased count front-loads the text: first fifth shows >= 1.4x the linear share (measured; the card's 55-75 %% "
                  "is not what bezier(.5,1,.89,1) gives: it gives ~%d %%)" % round(100 * ease(0.2)), share >= 0.28 and abs(share - ease(fifth / fps / dur)) < 0.06,
                  share, ease(fifth / fps / dur)),
            check("all characters visible at the end", meas[-1] == len(text.rstrip()), meas[-1]),
            check("caret blinks at 2 Hz through the 1 s hold (about 4 toggles)", 3 <= toggles <= 5, toggles),
            check("negative control: a linear count (measured) shows only ~20 % at the first fifth", lin_share < 0.25 and lin_share < share - 0.08,
                  lin_share)], [out]


def _digit_templates(f, h):
    np = _np()
    from PIL import ImageDraw
    T = {}
    for dgt in "0123456789":
        im = canvas_img(40, h, (0, 0, 0))
        ImageDraw.Draw(im).text((20, h / 2), dgt, font=f, fill=(255, 255, 255), anchor="mm")
        T[dgt] = arr(im).mean(axis=-1)
    return T


def _digit_tape(f, ch):
    """The 0-9 column as one tall strip (0..9 then 0), drawn exactly like the animation."""
    from PIL import ImageDraw
    im = canvas_img(40, ch * 11, (0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(11):
        d.text((20, ch / 2 + k * ch), str(k % 10), font=f, fill=(255, 255, 255), anchor="mm")
    return arr(im).mean(axis=-1).astype("float32")


def _tape_offset(cell, tape, ch):
    """Where on the 0-9 tape a column window sits, in rows (0..10), by template matching."""
    import cv2
    r = cv2.matchTemplate(tape, cell.mean(axis=-1).astype("float32"), cv2.TM_SQDIFF)
    y = int(r[:, 0].argmin())
    return (y / ch) % 10


def _read_digit(cell, T):
    np = _np()
    g = cell.mean(axis=-1)
    return min(T, key=lambda k: float(np.abs(T[k] - g).mean()))


@card("TYPE-36")
def rolling_digits(task, wd):
    np = _np()
    from PIL import ImageDraw
    fps, target = 120, "4096"
    f = font(MONO, 40)
    ch = 56
    ncol = len(target)
    stagger, each = 0.05, 0.4
    frames = []
    for i in range(int(1.0 * fps)):
        t = i / fps
        im = canvas_img(40 * ncol, ch, (0, 0, 0))
        d = ImageDraw.Draw(im)
        for c, dg in enumerate(target):
            order = ncol - 1 - c           # 0 = rightmost (lowest order)
            start = order * stagger        # right -> left stagger
            turns = 1 + (ncol - 1 - order) * 0 + (2 - min(order, 2))  # lower-order columns add extra full turns
            rows = turns * 10 + int(dg)
            p = ease_out_cubic(min(1, max(0, (t - start) / each)))
            pos = rows * p
            k = int(math.floor(pos))
            frac = pos - k
            for j in (0, 1):
                y = ch / 2 + (j - frac) * ch
                d.text((40 * c + 20, y), str((k + j) % 10), font=f, fill=(255, 255, 255), anchor="mm")
        frames.append(arr(im))
    out = write_video(Path(wd) / "digits.mp4", frames, fps)
    fr = read_video(out)
    T = _digit_templates(f, ch)
    tape = _digit_tape(f, ch)
    final = "".join(_read_digit(fr[-1][:, 40 * c:40 * c + 40], T) for c in range(ncol))
    changes = []
    starts = []
    want_rows = []
    for c in range(ncol):
        order = ncol - 1 - c
        want_rows.append((1 + (2 - min(order, 2))) * 10 + int(target[c]))
        offs = [_tape_offset(a[:, 40 * c:40 * c + 40], tape, ch) for a in fr]
        changes.append(round(sum(((offs[k] - offs[k - 1] + 5) % 10) - 5 for k in range(1, len(offs)))))
        diff = [float(np.abs(fr[k][:, 40 * c:40 * c + 40] - fr[k - 1][:, 40 * c:40 * c + 40]).mean()) for k in range(1, len(fr))]
        starts.append(next(k for k, v in enumerate(diff) if v > 1) / fps)
    first = "".join(_read_digit(fr[0][:, 40 * c:40 * c + 40], T) for c in range(ncol))
    return [check("columns land on the value 4096 (template-matched)", final == target, final),
            check("rows travelled per column (measured) match 10 x turns + digit", all(abs(a - b) <= 2 for a, b in zip(changes, want_rows)),
                  changes, want_rows),
            check("lower-order columns spin extra turns", changes[3] > changes[2] > changes[1], changes),
            check("right -> left stagger ~50 ms between columns", all(0.03 <= starts[c] - starts[c + 1] <= 0.07 for c in range(ncol - 1)), starts),
            check("negative control: frame 0 does not show the value", first != target, first)], [out]


def spring(t, v0=2.8, k=180.0, c=12.0):
    """Damped spring displacement (m = 1) starting at 0 with velocity v0: stiffness k, damping c."""
    w0 = math.sqrt(k)
    z = c / (2 * w0)
    wd_ = w0 * math.sqrt(1 - z * z)
    return v0 / wd_ * math.exp(-z * w0 * t) * math.sin(wd_ * t)


@card("TYPE-43")
def first_two_seconds(task, wd):
    np = _np()
    from PIL import Image, ImageDraw
    sr = 22050
    x = np.zeros(int(sr * 2.6))
    on = int(0.3 * sr)
    x[on:on + 600] = np.exp(-np.arange(600) / 80) * np.sin(np.arange(600) * 0.9) * 0.9
    wav = fx.write_wav(Path(wd) / "hit.wav", x, sr)
    y, _ = fx.read_wav(wav)
    e = np.array([np.sum(y[i * 256:(i + 1) * 256, 0] ** 2) for i in range(len(y) // 256)])
    onset = int(np.argmax(np.diff(e) > e.max() * 0.2) + 1) * 256 / sr
    fps, W, H = 30, 540, 300
    words = ["Make", "it", "MOVE"]
    f = font("Poppins-Bold.ttf", 54)
    ease_w = bezier(0.22, 1, 0.36, 1)
    frames = []
    for i in range(int(2.6 * fps)):
        t = i / fps - onset
        bg = 255 if 0 <= t < 0.12 else 18
        im = Image.new("RGB", (W, H), (bg, bg, bg))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        xs = [120, 250, 400]
        for k, wdx in enumerate(words):
            a = 0.08 + k * 0.09
            if t < a:
                continue
            u = min(1, (t - a) / 0.4)
            dy = 50 * (1 - ease_w(u))
            col = (240, 240, 240)
            s = 1.0
            if k == 2 and t >= 0.5:
                s = 1 + spring(t - 0.5)
                col = (255, 200, 0)
            fk = font("Poppins-Bold.ttf", int(round(54 * s)))
            d.text((xs[k], 150 + dy), wdx, font=fk, fill=col + (255,), anchor="mm")
        push = 1 + 0.02 * max(0, min(1, (t - 0.78) / 1.22))
        if push != 1:
            layer = layer.resize((int(W * push), int(H * push)), Image.BICUBIC).crop(
                (int((W * push - W) / 2), int((H * push - H) / 2), int((W * push - W) / 2) + W, int((H * push - H) / 2) + H))
        im.paste(layer, (0, 0), layer)
        frames.append(arr(im))
    out = write_video(Path(wd) / "open2s.mp4", frames)
    fr = read_video(out)
    t_of = lambda i: i / fps - onset  # noqa: E731
    flash = [i for i, a in enumerate(fr) if a[5:20, 5:20].mean() > 200]
    acc = [color_mask(a, (255, 200, 0), 50).sum() for a in fr]
    first_acc = next(i for i, v in enumerate(acc) if v > 0)
    widths = []
    for a in fr:
        b = mask_bbox(a, (255, 200, 0), 50)
        widths.append(b[2] - b[0] if b else 0)
    base_w = widths[-1]
    peak = max(widths) / base_w
    peak_t = t_of(widths.index(max(widths)))
    word0_y = [centroid(color_mask(a[:, :190], (240, 240, 240), 40)) for a in fr]
    settled = next(i for i, c in enumerate(word0_y) if c and abs(c[1] - word0_y[int((onset + 0.75) * fps)][1]) < 1.5)
    span = lambda a: (lambda b: b[2] - b[0])(ink_bbox(a, (18, 18, 18), 60))  # noqa: E731
    push = span(fr[-1]) / span(fr[int((onset + 0.8) * fps)])
    return [check("first transient detected at 0.30 s", abs(onset - 0.3) < 0.015, onset, 0.3),
            check("flash lasts 0-120 ms after the transient", flash and abs(t_of(flash[0])) < 0.04 and t_of(flash[-1]) < 0.13, [t_of(flash[0]), t_of(flash[-1])]),
            check("first word rises and settles by ~500 ms", t_of(settled) <= 0.55, t_of(settled)),
            check("emphasis pops to ~1.12x and turns accent at 500 ms", abs(t_of(first_acc) - 0.5) < 0.04 and 1.07 <= peak <= 1.17, [t_of(first_acc), peak]),
            check("pop peak lands inside 500-780 ms", 0.5 < peak_t < 0.78, peak_t),
            check("hold with a ~2 % camera push by 2 s", 1.012 <= push <= 1.03, push),
            check("negative control: before the transient there is no flash and no text", fr[0][5:20, 5:20].mean() < 50 and
                  ink_bbox(fr[0], (18, 18, 18), 60) is None)], [out, wav]


@card("TYPE-48")
def held_frames(task, wd):
    np = _np()
    from PIL import ImageDraw
    fps, W, H = 30, 480, 140
    words = ["HAND", "MADE", "TYPE"]
    f = font("Poppins-Bold.ttf", 48)
    hold = 3  # frames per step, on threes; no tweened ease, no anti-aliasing
    frames = []
    for i in range(36):
        step = i // hold
        im = canvas_img(W, H).convert("1").convert("L")
        im = im.convert("RGB")
        d = ImageDraw.Draw(im)
        d.fontmode = "1"  # anti-aliasing banned
        n = min(len(words), 1 + step // 2)
        sy = 0.85 if step % 2 == 1 and step < 6 else 1.0  # squash on the beat, recover on the next held step
        x = 20
        for w_ in words[:n]:
            g = canvas_img(int(f.getlength(w_)) + 4, 70)
            gd = ImageDraw.Draw(g)
            gd.fontmode = "1"
            gd.text((2, 2), w_, font=f, fill=(0, 0, 0))
            if sy != 1.0:
                g = g.resize((g.width, int(g.height * sy)), 0)
            im.paste(g, (x, 100 - g.height))
            x += g.width + 20
        frames.append(arr(im))
    out = write_video(Path(wd) / "held.mp4", frames)
    fr = read_video(out)
    change = [k for k in range(1, len(fr)) if np.abs(fr[k] - fr[k - 1]).max() > 0]
    levels = len(np.unique(fr.astype(int)))
    tw_frames = []
    for i in range(36):
        im = canvas_img(W, H)
        ImageDraw.Draw(im).text((20 + 2 * i, 40), "HAND", font=f, fill=(0, 0, 0))
        tw_frames.append(arr(im))
    tchange = [k for k in range(1, 36) if np.abs(tw_frames[k] - tw_frames[k - 1]).max() > 0]
    tlevels = len(np.unique(np.array(tw_frames).astype(int)))
    return [check("the image only changes on multiples of 3 frames", change and all(k % hold == 0 for k in change), change),
            check("no anti-aliasing: only pure black and white pixels", levels == 2, levels),
            check("words appear one by one on held steps", len(change) >= 4),
            check("negative control: a tweened eased version changes every frame with grey edges", len(tchange) == 35 and tlevels > 2,
                  [len(tchange), tlevels])], [out]


@card("TYPE-50")
def pill_pop(task, wd):
    np = _np()
    from PIL import Image, ImageDraw
    fps, W, H = 60, 600, 200
    f = font("Poppins-Bold.ttf", 40)
    words = [("Fast", (36, 129, 250), 0.2), ("Simple", (252, 80, 78), 0.6), ("Fun", (255, 194, 26), 1.0)]
    pad_x, pad_y = 0.35 * 40, 0.15 * 40
    frames = []

    def pop(u):  # 0 -> 1.1 -> 1 in 350 ms: overshoot at 60 %
        if u <= 0:
            return 0.0
        if u >= 1:
            return 1.0
        return 1.1 * ease_out_cubic(u / 0.6) if u < 0.6 else 1.1 - 0.1 * ease_in_out_cubic((u - 0.6) / 0.4)
    for i in range(int(1.6 * fps)):
        t = i / fps
        im = Image.new("RGB", (W, H), (250, 250, 250))
        x = 40
        for txt, col, beat in words:
            tb = f.getbbox(txt)
            w0, h0 = tb[2] - tb[0] + 2 * pad_x, tb[3] - tb[1] + 2 * pad_y
            s = pop((t - beat) / 0.35)
            if s > 0.02:
                pw, ph = int(w0 * s), int(h0 * s)
                cx, cy = x + w0 / 2, 100
                pill = Image.new("RGBA", (pw + 2, ph + 8), (0, 0, 0, 0))
                pd = ImageDraw.Draw(pill)
                dark = tuple(int(c * 0.7) for c in col)
                pd.rounded_rectangle((0, 5, pw, ph + 5), radius=int(14 * s), fill=dark + (255,))  # 5 px darker extrusion
                pd.rounded_rectangle((0, 0, pw, ph), radius=int(14 * s), fill=col + (255,))
                im.paste(pill, (int(cx - pw / 2), int(cy - ph / 2)), pill)
            x += w0 + 24
        frames.append(arr(im))
    out = write_video(Path(wd) / "pills.mp4", frames, fps)
    fr = read_video(out)
    res = {}
    for txt, col, beat in words:
        ws = []
        for a in fr:
            b = mask_bbox(a, col, 12)
            ws.append(b[2] - b[0] if b else 0)
        final = ws[-1]
        onset = next(k for k, v in enumerate(ws) if v > 0) / fps
        peak = max(ws) / final
        settle = next(k for k in range(len(ws)) if k / fps > beat and abs(ws[k] - final) <= 1 and all(abs(v - final) <= 1 for v in ws[k:])) / fps
        b = mask_bbox(fr[-1], col, 12)
        below = fr[-1][b[3] + 2, (b[0] + b[2]) // 2]
        res[txt] = {"onset": onset, "peak": peak, "settle": settle - beat, "extrusion": below.tolist(),
                    "dark": [int(c * 0.7) for c in col]}
    jw(Path(wd) / "pills.json", res)
    ok_peak = all(1.06 <= r["peak"] <= 1.12 for r in res.values())
    ok_on = all(abs(r["onset"] - b) < 0.04 for (t_, _, b), r in zip(words, res.values()))
    ok_ext = all(np.abs(np.array(r["extrusion"]) - np.array(r["dark"])).max() < 12 for r in res.values())
    return [check("each pill pops on its beat (0.2 / 0.6 / 1.0 s)", ok_on, {k: v["onset"] for k, v in res.items()}),
            check("overshoot to ~1.1x of the final width", ok_peak, {k: v["peak"] for k, v in res.items()}),
            check("settles within 350 ms", all(r["settle"] <= 0.37 for r in res.values()), {k: v["settle"] for k, v in res.items()}),
            check("darker bottom extrusion under each pill", ok_ext),
            check("negative control: before its beat a pill is absent", mask_bbox(fr[int(0.5 * fps)], words[1][1], 12) is None)], [out]


@card("TYPE-52")
def ink_then_accent(task, wd):
    np = _np()
    from PIL import Image, ImageDraw
    fps, W, H = 60, 640, 280
    f = font("Poppins-Bold.ttf", 40)
    ink, accent = (26, 31, 28), (27, 111, 224)
    l1, l2 = ["Renders", "take", "hours."], ["Ours", "take", "seconds."]
    delay, rise = 0.3, 24
    frames = []
    for i in range(int(1.4 * fps)):
        t = i / fps
        im = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(im)
        u1 = ease_out_cubic(min(1, t / 0.4))
        x = 40
        for k, w_ in enumerate(l1):
            d.text((x, 60 + (1 - u1) * rise), w_, font=f, fill=ink if t > 0 else (255, 255, 255))
            x += f.getlength(w_ + " ")
        if t >= delay:
            u2 = ease_out_cubic(min(1, (t - delay) / 0.4))
            x = 40
            for k, w_ in enumerate(l2):
                d.text((x, 170 + (1 - u2) * rise), w_, font=f, fill=accent if k == len(l2) - 1 else ink)
                x += f.getlength(w_ + " ")
        frames.append(arr(im))
    out = write_video(Path(wd) / "two_lines.mp4", frames, fps)
    fr = read_video(out)
    on1 = next(k for k, a in enumerate(fr) if color_mask(a[40:150], ink, 40).sum() > 50) / fps
    on2 = next(k for k, a in enumerate(fr) if color_mask(a[165:280], ink, 40).sum() + color_mask(a[165:280], accent, 40).sum() > 50) / fps
    last = fr[-1]
    acc = color_mask(last, accent, 40)
    ys, xs = np.nonzero(acc)
    acc_lines = 1 if ys.min() >= 165 else 2
    x_seconds = 40 + f.getlength("Ours take ")
    in_word = xs.min() >= x_seconds - 2
    y_first = [centroid(color_mask(a[150:280], accent, 40)) for a in fr]
    ys_ = [c[1] for c in y_first if c]
    rise_m = ys_[0] - ys_[-1]
    allacc = color_mask(last, ink, 40)[165:280].sum()
    return [check("line 2 arrives 250-400 ms after line 1", 0.25 <= on2 - on1 <= 0.4, on2 - on1),
            check("line 2 rises 12-30 px", 12 <= rise_m <= 30, rise_m),
            check("exactly one accent word, only on line 2", acc_lines == 1 and in_word, [acc_lines, int(xs.min()), x_seconds]),
            check("the rest of line 2 stays in ink", allacc > 100, int(allacc)),
            check("negative control: line 1 alone carries no accent colour", color_mask(fr[int(0.2 * fps)], accent, 40).sum() == 0)], [out]


@card("TYPE-72")
def orbiting_rings(task, wd):
    rings = [(360, 12, "MOTION · TYPE · RHYTHM · ", "#f2f0ea", "#ff3355"), (250, -9, "ORBIT · WORDS · ", "#f2f0ea", "#33ddff")]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-500 -500 1000 1000" width="500" height="500"><rect x="-500" y="-500" width="1000" height="1000" fill="#111"/><defs>']
    for k, (r, _, _, _, _) in enumerate(rings):
        svg.append('<path id="r%d" d="M-%d,0a%d,%d 0 1,1 %d,0a%d,%d 0 1,1 -%d,0"/>' % (k, r, r, r, 2 * r, r, r, 2 * r))
    svg.append("</defs>")
    for k, (r, _, txt, col, mark) in enumerate(rings):
        svg.append('<g id="ring%d"><text font-family="monospace" font-size="34" letter-spacing="6" fill="%s"><textPath href="#r%d">'
                   '<tspan fill="%s">●</tspan>%s</textPath></text></g>' % (k, col, k, mark, txt * 3))
    svg.append('<circle r="10" fill="#ffd000"/></svg>')
    page = tw(Path(wd) / "rings.html", "<!doctype html><meta charset=utf-8><body style=margin:0>" + "".join(svg) +
              "<script>window.seek=t=>{%s}</script>" % "".join("document.getElementById('ring%d').setAttribute('transform','rotate('+(%d*t)+')');"
                                                             % (k, sp) for k, (_, sp, _, _, _) in enumerate(rings)))
    node_js(wd, "rings", PW_HEAD + """(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:500,height:500}});
await p.goto('file://'+%s);for(const t of [0,1,2.5]){await p.evaluate(t=>seek(t),t);await p.screenshot({path:'ring_t'+t+'.png'});}
await p.reload();await p.waitForTimeout(1000);await p.screenshot({path:'ring_noseek.png'});
console.log(JSON.stringify({ok:true}));await b.close()})();""" % json.dumps(str(page)))

    def angle(img, col):
        c = centroid(color_mask(img, col, 70))
        return math.degrees(math.atan2(c[1] - 250, c[0] - 250))
    imgs = {t: load_rgb(Path(wd) / ("ring_t%s.png" % t)) for t in ("0", "1", "2.5")}
    res = {}
    for k, (_, sp, _, _, mark) in enumerate(rings):
        rgb = tuple(int(mark[i:i + 2], 16) for i in (1, 3, 5))
        a0, a1, a25 = (angle(imgs[t], rgb) for t in ("0", "1", "2.5"))
        res[k] = {"d1": (a1 - a0 + 540) % 360 - 180, "d25": (a25 - a0 + 540) % 360 - 180}
    noseek_d = (angle(load_rgb(Path(wd) / "ring_noseek.png"), (255, 51, 85)) - angle(imgs["0"], (255, 51, 85)) + 540) % 360 - 180
    out = jw(Path(wd) / "rings.json", res)
    return [check("outer ring turns +12 deg/s (measured on the marker glyph)", abs(res[0]["d1"] - 12) < 1.5 and abs(res[0]["d25"] - 30) < 2, res[0]),
            check("inner ring turns -9 deg/s, opposite direction", abs(res[1]["d1"] + 9) < 1.5 and abs(res[1]["d25"] + 22.5) < 2, res[1]),
            check("text laid on the circular path (ink in a ring band)", color_mask(imgs["0"][240:260, 0:40], (242, 240, 234), 60).sum() > 0
                  or color_mask(imgs["0"][60:80, 230:270], (242, 240, 234), 60).sum() > 0),
            check("negative control: a page left 1 s without seek(t) shows no rotation", abs(noseek_d) < 0.5, noseek_d)], [out, Path(wd) / "ring_t1.png"]


@card("TYPE-75")
def marquee_rows(task, wd):
    np = _np()
    import cv2
    from PIL import Image, ImageDraw
    fps, W, H = 30, 480, 270
    f = font("Poppins-Bold.ttf", 28)
    phrase = "KOSIF · "
    rep_w = int(round(f.getlength(phrase)))
    speeds = [120, 80, 160, 60, 100]
    styles = ["fill", "outline", "accent", "fill", "outline"]
    rowh = H // 5
    strips = []
    for k, st in enumerate(styles):
        im = Image.new("RGB", (rep_w * 8, rowh), (255, 255, 255))
        d = ImageDraw.Draw(im)
        for r in range(8):
            if st == "outline":
                d.text((r * rep_w, 8), phrase, font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(20, 20, 20))
            else:
                d.text((r * rep_w, 8), phrase, font=f, fill=(20, 20, 20) if st == "fill" else (230, 60, 40))
        strips.append(arr(im))

    def frame(t, modulo=True):
        out_ = np.full((H, W, 3), 255.0)
        for k, s in enumerate(strips):
            dir_ = 1 if k % 2 else -1
            off = (((dir_ * t * speeds[k]) % rep_w) + rep_w) % rep_w if modulo else dir_ * t * speeds[k]
            x0 = int(round(off)) + rep_w
            seg = s[:, x0:x0 + W] if 0 <= x0 <= s.shape[1] - W else np.full((rowh, W, 3), 255.0)
            if seg.shape[1] < W:
                seg = np.concatenate([seg, np.full((rowh, W - seg.shape[1], 3), 255.0)], axis=1)
            out_[k * rowh:(k + 1) * rowh] = seg
        return out_
    n = 60
    out = write_video(Path(wd) / "marquee.mp4", [frame(i / fps) for i in range(n)])
    fr = read_video(out)
    meas = []
    for k in range(5):
        a = cv2.cvtColor(fr[0][k * rowh:(k + 1) * rowh].astype("float32"), cv2.COLOR_RGB2GRAY)
        b = cv2.cvtColor(fr[6][k * rowh:(k + 1) * rowh].astype("float32"), cv2.COLOR_RGB2GRAY)
        (sx, _), _ = cv2.phaseCorrelate(a, b)
        meas.append(sx * fps / 6)
    expect = [(1 if k % 2 else -1) * -speeds[k] for k in range(5)]
    seam = []
    for k in range(5):
        per = rep_w / speeds[k]
        diff = float(np.abs(frame(0)[k * rowh:(k + 1) * rowh] - frame(per)[k * rowh:(k + 1) * rowh]).mean())
        seam.append(diff)
    acc = color_mask(fr[0], (230, 60, 40), 40)
    ys = np.nonzero(acc)[0]
    raw = frame(6.0, modulo=False)
    blank_rows = sum(1 for k in range(5) if raw[k * rowh:(k + 1) * rowh].min() > 250)
    return [check("rows slide at their speeds in alternating directions (phase correlation)",
                  all(abs(m - e) < 6 for m, e in zip(meas, expect)), meas, expect),
            check("seamless loop: after one repeat width / speed the row is identical", max(seam) < 2.0, seam),
            check("fill / outline / accent rows alternate (accent only on row 3)", len(ys) > 0 and ys.min() >= 2 * rowh and ys.max() < 3 * rowh),
            check("negative control: translating without the modulo empties rows after 6 s", blank_rows >= 3, blank_rows)], [out]


@card("TYPE-77")
def wall_to_logo(task, wd):
    np = _np()
    from PIL import Image, ImageDraw
    fps, W, H = 30, 480, 270
    ease = bezier(0.65, 0, 0.35, 1)
    f = font("Poppins-Regular.ttf", 12)
    wall = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(wall)
    for r in range(14):
        d.text((10, 8 + r * 18), ("motion type rhythm grid " * 8)[r % 5:r % 5 + 70], font=f, fill=255)
    wall = np.asarray(wall).astype(float) / 255
    logo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(logo).text((W / 2, H / 2), "K", font=font("Poppins-Bold.ttf", 150), fill=255, anchor="mm")
    logo = np.asarray(logo).astype(float) / 255
    frames, scales = [], []
    rush, fold = 1.2, 0.8
    fdist = 4.0
    for i in range(int((rush + fold) * fps) + 1):
        t = i / fps
        if t <= rush:
            z = 3.0 * ease(t / rush)  # translateZ toward the lens
            s = fdist / (fdist - z)
            img = Image.fromarray((wall * 255).astype("uint8")).resize((int(W * s), int(H * s)), Image.BILINEAR)
            cx, cy = img.width // 2, img.height // 2
            img = np.asarray(img.crop((cx - W // 2, cy - H // 2, cx - W // 2 + W, cy - H // 2 + H))).astype(float) / 255
            scales.append(s)
        else:
            u = ease((t - rush) / fold)
            squeezed = np.zeros_like(wall)
            band = Image.fromarray((wall * 255).astype("uint8")).resize((W, max(2, int(H * (1 - u) + 20 * u))))
            y0 = (H - band.height) // 2
            squeezed[y0:y0 + band.height] = np.asarray(band).astype(float) / 255
            img = squeezed * (1 - u) + logo * u
        frames.append(np.dstack([img * 255] * 3))
    out = write_video(Path(wd) / "wall_logo.mp4", frames)
    fr = read_video(out)
    iou = []
    for a in fr:
        m = a[..., 0] > 128
        lm = logo > 0.5
        iou.append(float((m & lm).sum() / max(1, (m | lm).sum())))
    half = int(rush * fps / 2)
    lin_half = fdist / (fdist - 1.5)
    return [check("rush scale follows cubic-bezier(0.65,0,0.35,1) (slow start)", scales[int(0.2 * fps)] < 1.05 and abs(scales[half] - lin_half) < 0.05,
                  [scales[int(0.2 * fps)], scales[half]]),
            check("rush lasts 1200 ms and reaches 4x", abs(scales[-1] - 4.0) < 0.01, scales[-1]),
            check("ends as the logo mark (IoU > 0.95)", iou[-1] > 0.95, iou[-1]),
            check("negative control: the starting wall is not the logo (IoU < 0.3)", iou[0] < 0.3, iou[0])], [out]


@card("TYPE-78")
def words_to_columns(task, wd):
    np = _np()
    from PIL import Image, ImageDraw
    fps, W, H, grid = 30, 640, 400, 40
    f = font("Poppins-Bold.ttf", 44)
    ease = bezier(0.76, 0, 0.24, 1)
    words = [("BUILD", (230, 60, 60)), ("WITH", (60, 140, 230)), ("TYPE", (60, 180, 90))]
    lintel = ("STRUCTURE", (200, 120, 20))
    stagger, dur = 0.12, 0.7
    sprites = []
    for w_, col in words + [lintel]:
        im = Image.new("RGBA", (int(f.getlength(w_)) + 8, 60), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4, 2), w_, font=f, fill=col + (255,))
        sprites.append(im)
    targets_x = [160, 320, 480]
    frames = []
    for i in range(int((dur + 2 * stagger + 0.3) * fps)):
        t = i / fps
        im = Image.new("RGB", (W, H), (250, 250, 250))
        for k, sp in enumerate(sprites[:3]):
            u = ease(min(1, max(0, (t - k * stagger) / dur)))
            r = sp.rotate(-(-90) * 0 + 90 * u, expand=True, resample=Image.BICUBIC)  # rotate -90 deg (counter-clockwise)
            cx = 100 + k * 160 + (targets_x[k] - (100 + k * 160)) * u
            bb = r.getbbox()
            im.paste(r, (int(round(cx - (bb[0] + bb[2]) / 2)), int(round(300 - bb[3]))), r)
        lt = sprites[3]
        im.paste(lt, (int(W / 2 - lt.width / 2), 300), lt)
        frames.append(arr(im))
    out = write_video(Path(wd) / "columns.mp4", frames)
    fr = read_video(out)
    res = []
    for k, (_, col) in enumerate(words):
        b0 = mask_bbox(fr[0], col, 40)
        b1 = mask_bbox(fr[-1], col, 40)
        res.append({"start_aspect": (b0[3] - b0[1]) / (b0[2] - b0[0]), "end_aspect": (b1[3] - b1[1]) / (b1[2] - b1[0]),
                    "cx": (b1[0] + b1[2]) / 2})
    starts = []
    for k, (_, col) in enumerate(words):
        a0 = (lambda b: (b[3] - b[1]) / (b[2] - b[0]))(mask_bbox(fr[0], col, 40))
        starts.append(next(i for i, a in enumerate(fr) if abs((lambda b: (b[3] - b[1]) / (b[2] - b[0]))(mask_bbox(a, col, 40)) - a0) > 0.02) / fps)
    snapped = all(abs(r["cx"] - round(r["cx"] / grid) * grid) <= 3 for r in res)
    lb = mask_bbox(fr[-1], lintel[1], 40)
    return [check("each word ends standing as a column (tall, aspect > 2)", all(r["end_aspect"] > 2 for r in res), [r["end_aspect"] for r in res]),
            check("columns snap to the 40 px grid", snapped, [r["cx"] for r in res]),
            check("120 ms stagger between words", all(0.07 <= starts[k + 1] - starts[k] <= 0.17 for k in range(2)), starts),
            check("a word lies across as the lintel under the columns", lb and (lb[2] - lb[0]) > 3 * (lb[3] - lb[1])),
            check("negative control: at frame 0 the words are horizontal (aspect < 0.5)", all(r["start_aspect"] < 0.5 for r in res),
                  [r["start_aspect"] for r in res])], [out]


def typewriter_schedule(text, cps=35, jitter=0.2, seed=7, pause=(0.25, 0.4)):
    import random
    rng = random.Random(seed)
    t, times = 0.0, []
    for ch in text:
        times.append(t)
        t += (1.0 / cps) * (1 + rng.uniform(-jitter, jitter))
        if ch in ".,!?;:":
            t += rng.uniform(*pause)
    return times, t


@card("TYPE-89")
def kosif_type_styles(task, wd):
    made = {}
    for sid in ("brutalist", "minimal", "typewriter"):
        d = Path(wd) / sid
        run([sys.executable, REPO / "tools/kosif.py", "scaffold", sid, d, "--starter", "html-canvas"], timeout=60)
        made[sid] = sorted(p.name for p in d.iterdir())
    text = "Hello, world. Type on."
    times, total = typewriter_schedule(text)
    gaps = [b - a for a, b in zip(times, times[1:])]
    after_punct = [gaps[i] for i, ch in enumerate(text[:-1]) if ch in ".,"]
    plain = [gaps[i] for i, ch in enumerate(text[:-1]) if ch not in ".,"]
    eff_cps = len(plain) / sum(plain)
    caret = [int(t / 0.53) % 2 == 0 for t in [k * 0.1 for k in range(20)]]
    times2, _ = typewriter_schedule(text)
    out = jw(Path(wd) / "typewriter_schedule.json", {"times": times, "total": total, "scaffold": made})
    need = {"STYLE.md", "PLAN.md", "REQUEST.md", "words.json", "TEST_REPORT.md", "html-canvas"}
    ft, _ = typewriter_schedule(text, jitter=0.0, pause=(0.0, 0.0))
    flat = [b - a for a, b in zip(ft, ft[1:])]
    return [check("scaffold writes the five files + the html-canvas starter for all three styles", all(need <= set(v) for v in made.values()), made),
            check("typewriter rate 25-45 cps with +-20 % seeded jitter", 25 <= eff_cps <= 45 and max(plain) / min(plain) > 1.1 and
                  all(abs(g * 35 - 1) <= 0.2 + 1e-9 for g in plain), eff_cps),
            check("250-400 ms pause after punctuation", all(0.25 <= g - 1 / 35 * 1.2 <= 0.4 + 1 / 35 * 0.4 for g in after_punct) and min(after_punct) > 0.25,
                  after_punct),
            check("seeded: the schedule repeats exactly", times == times2),
            check("caret blinks at 530 ms", caret[:6] == [True] * 6 and caret[6] is False),
            check("negative control: the untreated schedule (no jitter, no pauses) has no variation", max(flat) / min(flat) < 1.0001,
                  max(flat) / min(flat))], [out]


@card("TYPE-U01")
def poppins_bundled(task, wd):
    from fontTools.ttLib import TTFont
    from PIL import ImageDraw, ImageFont
    p = FONTS / "Poppins-Bold.ttf"
    t = TTFont(str(p))
    lic = (FONTS / "OFL-Poppins.txt").read_text(encoding="utf-8", errors="replace")
    f = ImageFont.truetype(str(p), 48)
    im = canvas_img(520, 100)
    ImageDraw.Draw(im).text((10, 20), "Caption label 2026", font=f, fill=(0, 0, 0))
    out = Path(wd) / "poppins.png"
    im.save(out)
    b = ink_bbox(arr(im), (255, 255, 255), 100)
    dflt = ImageFont.load_default()
    w_def = dflt.getlength("Caption label 2026")
    return [check("family Poppins, weight 700", t["name"].getDebugName(1) == "Poppins" and t["OS/2"].usWeightClass == 700),
            check("bundled under OFL 1.1", "SIL OPEN FONT LICENSE" in lic.upper() and "1.1" in lic),
            check("caption rendered with the TTF (ink width matches getlength)", abs((b[2] - b[0]) - f.getlength("Caption label 2026")) < 8,
                  [b[2] - b[0], f.getlength("Caption label 2026")]),
            check("negative control: the default bitmap font sets the line at a different width", abs(w_def - f.getlength("Caption label 2026")) > 50,
                  w_def)], [out]


@card("TYPE-U02")
def readable_captions(task, wd):
    np = _np()
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 1080, 1920
    sc = 0.5  # rendered at half size; sizes below are 1080p sizes x 0.5
    w, h = int(W * sc), int(H * sc)
    cap = font("Poppins-Bold.ttf", int(56 * sc))
    key = font("Poppins-Bold.ttf", int(96 * sc))
    caps = ["we cut the render", "time in half today"]
    base_y = int(h * 0.80)
    outs, baselines, centres = [], [], []
    for k, txt in enumerate(caps):
        bg = Image.new("RGB", (w, h), (90, 110, 140))
        grad = Image.linear_gradient("L").resize((w, h))
        bg = Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), bg, grad.point(lambda v: int(v * 0.8) if v > 150 else 0))
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((w / 2, base_y), txt, font=cap, fill=(0, 0, 0, 220), anchor="ms")
        sh = sh.filter(ImageFilter.GaussianBlur(4))
        bg.paste(sh, (0, 0), sh)
        d = ImageDraw.Draw(bg)
        d.text((w / 2, base_y), txt, font=cap, fill=(255, 255, 255), anchor="ms")
        p = Path(wd) / ("caption_%d.png" % k)
        bg.save(p)
        outs.append(p)
        a = arr(bg)
        m = (a.min(axis=-1) > 245)
        ys, xs = np.nonzero(m)
        rowc = m.sum(axis=1)
        baselines.append(int(np.nonzero(rowc > 0.25 * rowc.max())[0].max()))  # descenders are sparse rows below the baseline
        centres.append((xs.min() + xs.max()) / 2)
    # key-word pill centred on the ink bounds (textbbox), not the layout box
    word = "HALF"
    kb = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), word, font=key)
    lay_w, lay_h = key.getlength(word), key.size
    im = Image.new("RGB", (w, 300), (40, 40, 40))
    d = ImageDraw.Draw(im)
    tx, ty = 100, 80
    ink = (tx + kb[0], ty + kb[1], tx + kb[2], ty + kb[3])
    pad = 14
    d.rounded_rectangle((ink[0] - pad, ink[1] - pad, ink[2] + pad, ink[3] + pad), radius=20, fill=(255, 200, 0))
    d.text((tx, ty), word, font=key, fill=(10, 20, 150))
    pp = Path(wd) / "key_pill.png"
    im.save(pp)
    a = arr(im)
    pill = mask_bbox(a, (255, 200, 0), 30)
    txt = mask_bbox(a, (10, 20, 150), 40)
    off = ((pill[0] + pill[2]) / 2 - (txt[0] + txt[2]) / 2, (pill[1] + pill[3]) / 2 - (txt[1] + txt[3]) / 2)
    lay_off = ((tx + lay_w / 2) - (txt[0] + txt[2]) / 2, (ty + lay_h / 2) - (txt[1] + txt[3]) / 2)
    words = [{"w": "we", "start": 1.00}, {"w": "cut", "start": 1.30}]
    lead = 0.06
    shown = [round(x["start"] - lead, 3) for x in words]
    return [check("caption ~56 px at 1080p, low centre (80 % height)", abs(cap.size / sc - 56) < 1 and abs(baselines[0] / h - 0.80) < 0.01,
                  baselines[0] / h),
            check("consecutive captions share one baseline height", baselines[0] == baselines[1], baselines),
            check("captions centred horizontally", all(abs(c - w / 2) < 3 for c in centres), centres),
            check("key pill centred on the ink bounds (offset < 1.5 px)", max(map(abs, off)) < 1.5, off),
            check("each word appears 0.04-0.1 s before its timestamp", all(0.04 <= x["start"] - s <= 0.1 for x, s in zip(words, shown)), shown),
            check("negative control: centring on the layout box misses the ink by > 3 px", max(map(abs, lay_off)) > 3, lay_off)], outs + [pp]


# ───────────── DOC-34: PlantUML (apt plantuml, installed with the owner's approval) ─────────────
_PUML = {
    "sequence": """@startuml
participant Client
participant Server
participant Database
Client -> Server: request
Server -> Database: query
Database --> Server: rows
Server --> Client: response
@enduml
""",
    "class": """@startuml
class Animal {
  +name : String
  +speak() : void
}
class Dog
class Cat
Animal <|-- Dog
Animal <|-- Cat
@enduml
""",
    "component": """@startuml
[Web] --> [API] : REST
[API] --> [DB] : SQL
@enduml
""",
}


def _svg_texts(path):
    """(text, x, y) of every <text> element of an SVG, in document order; [] when the file is not an SVG."""
    import xml.etree.ElementTree as ET
    try:
        root = ET.parse(str(path)).getroot()
    except ET.ParseError:
        return []
    ns = "{http://www.w3.org/2000/svg}"
    return [((t.text or "").strip(), float(t.get("x", 0)), float(t.get("y", 0))) for t in root.iter(ns + "text")]


@card("DOC-34")
def plantuml_uml(task, wd):
    """PlantUML turns text into UML: a sequence, a class and a component diagram are rendered to SVG with the apt
    `plantuml` (Java) and the SVGs are read back: participants, message order and return arrows, class members and the two
    inheritance triangles, components and their labelled links."""
    wd = Path(wd)
    srcs = [tw(wd / ("%s.puml" % k), v) for k, v in _PUML.items()]
    out = wd / "svg"
    env = dict(os.environ, HOME=str(wd / "_home"), JAVA_TOOL_OPTIONS=os.environ.get("JAVA_TOOL_OPTIONS", "") + " -Djava.awt.headless=true")
    (wd / "_home").mkdir(exist_ok=True)
    run(["plantuml", "-tsvg", "-charset", "UTF-8", "-o", out, *srcs], env=env, cwd=wd)
    ver = run(["plantuml", "-version"], env=env).stdout.splitlines()[0]
    svg = {k: out / ("%s.svg" % k) for k in _PUML}
    seq = _svg_texts(svg["sequence"])
    names = [t for t, _, _ in seq]
    msgs = sorted([(y, t) for t, x, y in seq if t in ("request", "query", "rows", "response")])
    seq_src = svg["sequence"].read_text()
    dashed_ret = seq_src.count("stroke-dasharray: 2.0,2.0")
    lifelines = seq_src.count("stroke-dasharray: 5.0,5.0")
    cls = [t for t, _, _ in _svg_texts(svg["class"])]
    cls_src = svg["class"].read_text()
    hollow = len(re.findall(r'<polygon fill="none" points="[^"]+"', cls_src))
    comp = [t for t, _, _ in _svg_texts(svg["component"])]
    comp_src = svg["component"].read_text()
    rects = len(re.findall(r"<rect ", comp_src))
    raw = _svg_texts(srcs[0])
    rep = jw(wd / "plantuml_report.json", {"version": ver, "sequence_texts": names, "message_order": [t for _, t in msgs],
                                           "dashed_returns": dashed_ret, "lifelines": lifelines, "class_texts": cls,
                                           "hollow_triangles": hollow, "component_texts": comp, "component_rects": rects})
    return [check("three SVGs rendered", all(p.is_file() and p.stat().st_size > 500 for p in svg.values()), [p.stat().st_size for p in svg.values()]),
            check("sequence: each participant drawn twice (head and foot)", all(names.count(n) == 2 for n in ("Client", "Server", "Database")), names),
            check("sequence: messages top-to-bottom in source order", [t for _, t in msgs] == ["request", "query", "rows", "response"], [t for _, t in msgs]),
            check("sequence: the two --> replies are dashed and 3 lifelines", (dashed_ret, lifelines) == (2, 3), [dashed_ret, lifelines], [2, 3]),
            check("class: Animal with its attribute and method, Dog, Cat", cls == ["Animal", "name : String", "speak() : void", "Dog", "Cat"], cls),
            check("class: two hollow inheritance triangles (<|--)", hollow == 2, hollow, 2),
            check("component: three components and both link labels", sorted(comp) == ["API", "DB", "REST", "SQL", "Web"], comp),
            check("negative control: the untreated .puml text is not a diagram (no SVG text elements)", raw == [] and "<svg" not in _PUML["sequence"], len(raw), 0)], \
        [svg["sequence"], svg["class"], svg["component"], rep]
