#!/usr/bin/env python3
"""Toolbelt smoke test: make each library do one real, offline task and record the result.

    python3 smoke.py [--json results.json]

Each check is independent; a missing package is reported as "missing", never as a pass.
Nothing is downloaded at run time (no model weights, no network), so this runs in a sandbox.
"""
import importlib
import json
import sys
import time

CHECKS = []


def check(name, module):
    def deco(fn):
        CHECKS.append((name, module, fn))
        return fn
    return deco


@check("sympy: solve and integrate exactly", "sympy")
def _sympy(m):
    x = m.symbols("x")
    roots = m.solve(x**2 - 5*x + 6, x)
    integ = m.integrate(m.sin(x)**2, (x, 0, m.pi))
    assert sorted(roots) == [2, 3] and integ == m.pi / 2
    return f"roots {sorted(roots)}, ∫sin²=π/2, LaTeX {m.latex(integ)}"


@check("z3: prove a property and find a counterexample", "z3")
def _z3(z3):
    a, b = z3.Ints("a b")
    s = z3.Solver(); s.add(z3.Not(a + b == b + a)); proved = s.check() == z3.unsat
    s2 = z3.Solver(); s2.add(a * a == 49, a < 0); s2.check(); cex = s2.model()[a].as_long()
    assert proved and cex == -7
    return "a+b=b+a proved (unsat negation); a²=49 ∧ a<0 → a=-7"


@check("duckdb: SQL over an in-memory table", "duckdb")
def _duck(d):
    con = d.connect()
    con.execute("create table v as select i, i % 7 as k from range(100000) t(i)")
    r = con.execute("select k, count(*) c, avg(i) from v group by k order by k").fetchall()
    assert len(r) == 7 and sum(x[1] for x in r) == 100000
    return f"group-by over 100k rows → {len(r)} groups"


@check("polars: lazy aggregation", "polars")
def _polars(pl):
    df = pl.DataFrame({"g": ["a", "b", "a", "c", "b"], "v": [1, 2, 3, 4, 5]})
    out = df.lazy().group_by("g").agg(pl.col("v").sum()).sort("g").collect()
    assert out["v"].to_list() == [4, 7, 4]
    return "lazy group_by sum a=4 b=7 c=4"


@check("scikit-learn: train and cross-validate", "sklearn")
def _sk(_):
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    X, y = load_iris(return_X_y=True)
    acc = cross_val_score(RandomForestClassifier(n_estimators=50, random_state=0), X, y, cv=5).mean()
    assert acc > 0.9
    return f"iris RandomForest 5-fold accuracy {acc:.3f}"


@check("statsforecast: AutoETS forecast with intervals", "statsforecast")
def _sf(_):
    import pandas as pd
    import numpy as np
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS
    n = 48
    df = pd.DataFrame({"unique_id": "s", "ds": pd.date_range("2020-01-01", periods=n, freq="MS"),
                       "y": 100 + np.arange(n) * 2 + 10 * np.sin(np.arange(n) / 12 * 2 * np.pi)})
    fc = StatsForecast(models=[AutoETS(season_length=12)], freq="MS").forecast(df=df, h=6, level=[80])
    assert len(fc) == 6
    return f"6-month forecast, first {float(fc['AutoETS'].iloc[0]):.1f} with 80% interval"


@check("trafilatura: extract article text from HTML", "trafilatura")
def _traf(t):
    html = "<html><body><nav>menu home about</nav><article><h1>عنوان</h1><p>" + ("هذا نص المقال الرئيسي. " * 20) + "</p></article><footer>copyright</footer></body></html>"
    txt = t.extract(html) or ""
    assert "المقال الرئيسي" in txt and "copyright" not in txt
    return f"kept {len(txt)} chars of Arabic article, dropped nav/footer"


@check("hypothesis: property test finds the shrunk counterexample", "hypothesis")
def _hyp(h):
    from hypothesis import given, settings, strategies as st
    found = {}

    @settings(max_examples=200, database=None)
    @given(st.lists(st.integers()))
    def prop(xs):
        if len(xs) > 2 and sum(xs) > 100:
            found.setdefault("x", xs)
            raise AssertionError
    try:
        prop()
    except AssertionError:
        pass
    assert "x" in found
    return "falsified 'short or small' list property and shrank the input"


@check("pandera: schema rejects bad rows", "pandera")
def _pandera(_):
    import pandas as pd
    import pandera.pandas as pa
    schema = pa.DataFrameSchema({"fps": pa.Column(int, pa.Check.isin([24, 25, 30, 60]))})
    schema.validate(pd.DataFrame({"fps": [30, 60]}))
    try:
        schema.validate(pd.DataFrame({"fps": [30, 29]})); ok = False
    except Exception:
        ok = True
    assert ok
    return "fps column contract: 29 rejected, 30/60 accepted"


@check("music21: build a melody and analyse its key", "music21")
def _m21(m):
    s = m.stream.Stream()
    for p in "C4 E4 G4 C5 B4 G4 F4 E4 D4 C4".split():
        s.append(m.note.Note(p, quarterLength=0.5))
    k = s.analyze("key")
    assert k.tonic.name == "C"
    return f"10-note line analysed as {k.tonic.name} {k.mode}"


@check("OR-Tools CP-SAT: schedule without overlaps", "ortools")
def _ort(_):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel(); H = 20
    durs = [3, 2, 4, 1]
    st_ = [m.NewIntVar(0, H, f"s{i}") for i in range(4)]
    iv = [m.NewIntervalVar(st_[i], durs[i], st_[i] + durs[i], f"i{i}") for i in range(4)]
    m.AddNoOverlap(iv); end = m.NewIntVar(0, H, "end")
    for i in range(4):
        m.Add(end >= st_[i] + durs[i])
    m.Minimize(end); s = cp_model.CpSolver(); r = s.Solve(m)
    assert r == cp_model.OPTIMAL and s.Value(end) == 10
    return "4 jobs on one machine, optimal makespan 10"


@check("PuLP: linear program (budget split)", "pulp")
def _pulp(p):
    prob = p.LpProblem("ads", p.LpMaximize)
    if hasattr(prob, "add_variable"):  # PuLP ≥ 4: variables belong to the problem
        a = prob.add_variable("reels", lowBound=0, upBound=1000, cat="Integer"); b = prob.add_variable("stories", lowBound=0, upBound=1000, cat="Integer")
    else:
        a = p.LpVariable("reels", 0); b = p.LpVariable("stories", 0)
    prob += 3 * a + 2 * b
    prob += a + b <= 100
    prob += a <= 60
    avail = p.listSolvers(onlyAvailable=True)  # PuLP 4 no longer bundles CBC; CP-SAT comes with ortools
    prob.solve(p.getSolver(avail[0], msg=False) if avail else None)
    assert abs(p.value(prob.objective) - 260) < 1e-6
    return f"max 3a+2b s.t. a+b≤100, a≤60 → 260 (a=60, b=40) via {avail[0] if avail else 'default'}"


@check("geopandas: buffer and area in a metric CRS", "geopandas")
def _geo(g):
    from shapely.geometry import Point
    gdf = g.GeoDataFrame(geometry=[Point(31.2357, 30.0444)], crs="EPSG:4326").to_crs(32636)  # UTM 36N: true metres
    area = gdf.buffer(1000, quad_segs=64).area.iloc[0]
    assert abs(area - 3.14159e6) < 2e3
    back = g.GeoSeries(gdf.buffer(1000), crs=32636).to_crs(4326).total_bounds
    return f"1 km buffer around Cairo in UTM 36N → {area/1e6:.4f} km² (π expected); lon span {back[2]-back[0]:.4f}°"


@check("biopython: translate and GC content", "Bio")
def _bio(_):
    from Bio.Seq import Seq
    from Bio.SeqUtils import gc_fraction
    s = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
    prot = str(s.translate(to_stop=True))
    assert prot == "MAIVMGR"
    return f"protein {prot}, GC {gc_fraction(s):.2f}"


@check("rdkit: parse SMILES and compute descriptors", "rdkit")
def _rd(_):
    from rdkit import Chem
    from rdkit.Chem import Descriptors
    mol = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
    mw = Descriptors.MolWt(mol)
    assert abs(mw - 180.16) < 0.1
    return f"aspirin MW {mw:.2f}, {mol.GetNumAtoms()} heavy atoms"


@check("spaCy: blank Arabic tokenizer + rule matcher", "spacy")
def _spacy(spacy):
    nlp = spacy.blank("ar")
    doc = nlp("يوم الجمعة سيصدر الفيديو الجديد في الساعة الثامنة")
    from spacy.matcher import Matcher
    mt = Matcher(nlp.vocab); mt.add("DAY", [[{"TEXT": "يوم"}, {"TEXT": "الجمعة"}]])
    assert len(doc) >= 8 and mt(doc)
    return f"{len(doc)} Arabic tokens; matched 'يوم الجمعة'"


@check("chromadb: in-memory collection with given embeddings", "chromadb")
def _chroma(c):
    cl = c.EphemeralClient()
    col = cl.create_collection("kosif-smoke")
    col.add(ids=["1", "2", "3"], embeddings=[[1, 0, 0], [0, 1, 0], [0.9, 0.1, 0]], documents=["reel", "doc", "reel2"])
    r = col.query(query_embeddings=[[1, 0, 0]], n_results=2)
    assert r["ids"][0] == ["1", "3"]
    return "nearest-neighbour query returned the two reel vectors"


@check("mediapipe: library loads (task models download on demand)", "mediapipe")
def _mp(mp):
    assert hasattr(mp, "tasks")
    return f"mediapipe {mp.__version__} import OK; face/pose tasks need a .task model file"


@check("argos-translate: library loads (language packages ~100 MB on demand)", "argostranslate")
def _argos(_):
    import argostranslate.translate as tr
    assert hasattr(tr, "translate")
    return "import OK; install ar↔en package before translating"


@check("semgrep: CLI present", "semgrep")
def _semgrep(_):
    import shutil, subprocess, os
    exe = shutil.which("semgrep") or os.path.join(os.path.dirname(sys.executable), "semgrep")
    v = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=60).stdout.strip()
    assert v
    return f"semgrep {v}; rule packs are fetched from the registry when scanning"


def main():
    out = []
    for name, module, fn in CHECKS:
        t0 = time.time()
        try:
            m = importlib.import_module(module)
        except Exception as e:  # noqa: BLE001
            out.append({"check": name, "status": "missing", "detail": type(e).__name__}); continue
        try:
            detail = fn(m); status = "pass"
        except Exception as e:  # noqa: BLE001
            detail, status = f"{type(e).__name__}: {e}"[:200], "fail"
        out.append({"check": name, "module": module, "status": status, "detail": detail,
                    "version": getattr(m, "__version__", ""), "seconds": round(time.time() - t0, 2)})
    for r in out:
        print(f"{ {'pass': '✅', 'fail': '❌', 'missing': '·'}[r['status']] } {r['check']}: {r['detail']}")
    print(f"\n{sum(r['status']=='pass' for r in out)}/{len(out)} pass")
    if "--json" in sys.argv:
        path = sys.argv[sys.argv.index("--json") + 1]
        json.dump({"python": sys.version.split()[0], "results": out}, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 0 if all(r["status"] != "fail" for r in out) else 1


if __name__ == "__main__":
    sys.exit(main())
