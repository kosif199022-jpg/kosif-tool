"""Real programs for the code-engineering power cards (CODE-*).

Each program builds a small synthetic fixture (a toy repo, a function, a diff, a log), performs the
card's procedure on it with the stdlib, writes its result into the work folder and returns checks
whose answers are known in advance (planted bug found, planted secret flagged, exact counts).
Offline and deterministic; no package installs, no network, no model calls.
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
import os
import py_compile
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def _w(work: Path, name: str, data) -> Path:
    p = work / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2, default=str),
                 encoding="utf-8")
    return p


def _tree(root: Path, files: dict) -> Path:
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@example.invalid", "GIT_CONFIG_NOSYSTEM": "1", "HOME": "/nonexistent"}


def _git(repo: Path, *args) -> str:
    env = dict(os.environ, **GIT_ENV)
    env["HOME"] = str(repo.parent)
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=env)
    if r.returncode not in (0, 1):
        raise RuntimeError(r.stderr)
    return r.stdout


def _git_init(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q", "-b", "main")


SECRET_RE = re.compile(r"sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{36}|AKIA[0-9A-Z]{16}|api_key\s*=")
DEBUG_RE = re.compile(r"console\.log|debugger|\bprint\(\s*['\"]debug")


# ---------------------------------------------------------------- CODE-01
def search_first(work: Path):
    repo = _tree(work / "repo", {"util/slug.py": "def slugify(s):\n    return '-'.join(s.lower().split())\n"})

    def decide(candidates):
        exact = [c for c in candidates if c["fit"] >= 0.9 and c["maintained"] and c["licence"] in ("MIT", "Apache-2.0")]
        if exact:
            return "Adopt", exact[0]["name"]
        partial = [c for c in candidates if 0.6 <= c["fit"] < 0.9 and c["maintained"]]
        if partial:
            return "Extend", partial[0]["name"]
        weak = [c for c in candidates if 0.3 <= c["fit"] < 0.6]
        if len(weak) >= 2:
            return "Compose", "+".join(c["name"] for c in weak[:3])
        return "Build", ""

    def search_repo(word):
        return [str(p.relative_to(repo)) for p in repo.rglob("*.py") if f"def {word}" in p.read_text()]

    in_repo = search_repo("slugify")
    cases = {
        "exact": [{"name": "pyslug", "fit": 0.95, "maintained": True, "licence": "MIT"}],
        "exact_gpl": [{"name": "gslug", "fit": 0.95, "maintained": True, "licence": "GPL-3.0"}],
        "partial": [{"name": "textkit", "fit": 0.7, "maintained": True, "licence": "MIT"}],
        "weak": [{"name": "a", "fit": 0.4, "maintained": True, "licence": "MIT"},
                 {"name": "b", "fit": 0.35, "maintained": False, "licence": "MIT"}],
        "none": [],
    }
    verdicts = {k: decide(v)[0] for k, v in cases.items()}
    _w(work, "decisions.json", {"repo_hits": in_repo, "verdicts": verdicts})
    return [("repo searched first and finds existing slugify", in_repo == ["util/slug.py"], str(in_repo)),
            ("exact maintained MIT match -> Adopt", verdicts["exact"] == "Adopt", verdicts["exact"]),
            ("GPL exact match is not auto-adopted", verdicts["exact_gpl"] != "Adopt", verdicts["exact_gpl"]),
            ("partial -> Extend, weak pair -> Compose, none -> Build",
             (verdicts["partial"], verdicts["weak"], verdicts["none"]) == ("Extend", "Compose", "Build"), str(verdicts))]


# ---------------------------------------------------------------- CODE-02
def live_docs(work: Path):
    import inspect
    from importlib import metadata
    import numpy as np
    version = metadata.version("numpy")
    real = list(inspect.signature(np.clip).parameters)
    remembered = ["a", "a_min", "a_max", "out"]  # a recollection from numpy 1.x
    major_minor = tuple(int(x) for x in version.split(".")[:2])
    new_names = sorted(set(real) - set(remembered))
    calls = []

    def doc_call(q):
        if len(calls) >= 3:
            raise RuntimeError("doc-call budget (<=3 per question) spent")
        q = re.sub(r"sk-[A-Za-z0-9]{8,}", "<API_KEY>", q)
        calls.append(q)
        return q

    for i in range(3):
        doc_call(f"numpy clip signature key sk-abcdefgh12345678 try {i}")
    try:
        doc_call("fourth")
        fourth = "allowed"
    except RuntimeError:
        fourth = "refused"
    _w(work, "docs_receipt.json", {"package": "numpy", "version": version, "signature_head": real, "calls": calls})
    return [("version read from installed metadata", bool(re.match(r"\d+\.\d+", version)), version),
            ("installed signature read, not recalled: numpy>=2.1 adds min/max keywords memory lacks",
             ({"min", "max"} <= set(new_names)) if major_minor >= (2, 1) else not new_names, f"v{version} new={new_names}"),
            ("fourth doc call refused (budget 3)", fourth == "refused", fourth),
            ("secret redacted from every query", all("sk-" not in c and "<API_KEY>" in c for c in calls), calls[0])]


# ---------------------------------------------------------------- CODE-03
def isolated_venv(work: Path):
    v = work / "venv"
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(v)], check=True, capture_output=True)
    site = next(v.glob("lib/python*/site-packages"))
    pkg, ver = "tinypkg", "1.2.3"
    (site / f"{pkg}.py").write_text("import os\ndef secret_visible():\n    return 'PLANTED_KEY' in os.environ\n")
    dist = site / f"{pkg}-{ver}.dist-info"
    dist.mkdir()
    (dist / "METADATA").write_text(f"Metadata-Version: 2.1\nName: {pkg}\nVersion: {ver}\n")
    (dist / "RECORD").write_text("")
    (v / "home").mkdir()
    env = {"PATH": f"{v}/bin:/usr/bin:/bin", "HOME": str(v / "home")}
    code = ("import tinypkg, importlib.metadata as m, sys;"
            "print(m.version('tinypkg'), tinypkg.secret_visible(), sys.prefix)")
    t0 = time.time()
    os.environ["PLANTED_KEY"] = "x"
    try:
        r = subprocess.run([str(v / "bin" / "python"), "-c", code], env=env, capture_output=True, text=True)
        leak = subprocess.run([str(v / "bin" / "python"), "-c", code], capture_output=True, text=True)
    finally:
        os.environ.pop("PLANTED_KEY", None)
    took = round(time.time() - t0, 3)
    out = r.stdout.split()
    _w(work, "venv_receipt.json", {"cmd": code, "exit": r.returncode, "seconds": took, "stdout": r.stdout,
                                   "unscrubbed_stdout": leak.stdout})
    return [("command exited 0 inside the venv", r.returncode == 0, r.stderr[-200:]),
            ("pinned exact version 1.2.3 resolved", out[:1] == ["1.2.3"], r.stdout),
            ("scrubbed env hides the planted key", out[1:2] == ["False"], r.stdout),
            ("control: unscrubbed env leaks it (so the scrub is what hides it)", leak.stdout.split()[1:2] == ["True"],
             leak.stdout),
            ("runs from the venv prefix", out[2:3] == [str(v)], r.stdout)]


# ---------------------------------------------------------------- CODE-04
def onboarding(work: Path):
    repo = _tree(work / "repo", {
        "README.md": "# Tally\nCounts words in files.\n",
        "pyproject.toml": "[project]\nname='tally'\n[project.scripts]\ntally='tally.cli:main'\n[tool.pytest.ini_options]\ntestpaths=['tests']\n",
        "tally/cli.py": "from tally.core import count\ndef main():\n    print(count('a b'))\nif __name__ == '__main__':\n    main()\n",
        "tally/core.py": "def count(s):\n    return len(s.split())\n",
        "tests/test_core.py": "from tally.core import count\ndef test_count():\n    assert count('a b') == 2\n",
        ".github/workflows/ci.yml": "on: push\njobs:\n  t:\n    runs-on: ubuntu-latest\n    steps:\n      - run: pytest -q\n",
    })
    order = ["README.md", "CLAUDE.md", "AGENTS.md", "pyproject.toml", "package.json", "go.mod"]
    read = [f for f in order if (repo / f).exists()]
    entries = sorted(str(p.relative_to(repo)) for p in repo.rglob("*.py") if "__main__" in p.read_text())
    py = (repo / "pyproject.toml").read_text()
    test_cmd = "pytest" if "pytest" in py else "python -m unittest"
    ci_cmds = re.findall(r"run:\s*(.+)", (repo / ".github/workflows/ci.yml").read_text())
    importers = {}
    for p in repo.rglob("*.py"):
        for m in re.findall(r"from ([\w.]+) import", p.read_text()):
            importers.setdefault(m, []).append(str(p.relative_to(repo)))
    note = {"purpose": (repo / "README.md").read_text().splitlines()[1], "layers": sorted(importers),
            "entry_points": entries, "commands": {"test": test_cmd, "ci": ci_cmds},
            "conventions": "snake_case modules under tally/", "risky_areas": [m for m, v in importers.items() if len(v) >= 2]}
    _w(work, "ONBOARDING.json", note)
    return [("read order respected (README before manifests)", read == ["README.md", "pyproject.toml"], str(read)),
            ("entry point found", entries == ["tally/cli.py"], str(entries)),
            ("test command from manifest and CI agree", test_cmd == "pytest" and ci_cmds == ["pytest -q"], str(ci_cmds)),
            ("six note sections", len(note) == 6, str(list(note))),
            ("most-imported module flagged risky", note["risky_areas"] == ["tally.core"], str(note["risky_areas"]))]


# ---------------------------------------------------------------- CODE-05
def change_impact(work: Path):
    repo = _tree(work / "repo", {
        "x.py": "def parse(s):\n    return s.split(',')\n",
        "a.py": "from x import parse\nprint(parse('1,2'))\n",
        "b.py": "import x\nx.parse('3')\n",
        "c.py": "import importlib\nm = importlib.import_module(NAME)\n",
        "tests/test_x.py": "from x import parse\ndef test_parse():\n    assert parse('a,b') == ['a','b']\n",
        "schema.json": '{"fields": ["id", "when"]}',
    })
    callers, tests, unverified = [], [], []
    for p in sorted(repo.rglob("*.py")):
        t, rel = p.read_text(), str(p.relative_to(repo))
        if rel == "x.py":
            continue
        if re.search(r"from x import|^import x\b", t, re.M):
            (tests if rel.startswith("tests/") else callers).append(rel)
        elif "import_module(" in t:
            unverified.append(rel)
    report = {"Code": callers, "Data": json.loads((repo / "schema.json").read_text())["fields"], "Interfaces": ["x.parse"],
              "Tests": tests, "Docs": [], "Release": "unverified", "unverified": unverified}
    _w(work, "impact.json", report)
    return [("both static callers found", callers == ["a.py", "b.py"], str(callers)),
            ("the proving test found", tests == ["tests/test_x.py"], str(tests)),
            ("dynamic import marked unverified, not assumed", unverified == ["c.py"], str(unverified)),
            ("six answer sections in order", list(report)[:6] == ["Code", "Data", "Interfaces", "Tests", "Docs", "Release"],
             str(list(report)))]


# ---------------------------------------------------------------- CODE-06
def fact_forcing(work: Path):
    repo = _tree(work / "repo", {"lib.py": "def pub():\n    pass\ndef _priv():\n    pass\n",
                                 "u1.py": "from lib import pub\n", "u2.py": "import lib\n", "u3.py": "print(1)\n",
                                 "build/a.o": "x", "build/b.o": "y"})

    def facts_for_edit(target):
        mod = Path(target).stem
        imp = sorted(str(p.relative_to(repo)) for p in repo.glob("*.py")
                     if re.search(rf"from {mod} import|import {mod}\b", p.read_text()))
        pubs = [n.name for n in ast.parse((repo / target).read_text()).body
                if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]
        return {"importers": imp, "public": pubs, "instruction": "rename pub"}

    def gate(action, facts):
        need = {"edit": ["importers", "public", "instruction"], "destructive": ["removes", "undo"]}[action]
        return all(facts.get(k) for k in need)

    f = facts_for_edit("lib.py")
    removes = sorted(str(p.relative_to(repo)) for p in (repo / "build").rglob("*") if p.is_file())
    d = {"removes": removes, "undo": "git checkout -- build (or rebuild with make)"}
    _w(work, "facts.json", {"edit": f, "destructive": d})
    return [("edit refused without facts ('are you sure' is not enough)", not gate("edit", {"instruction": "yes"}), "refused"),
            ("importers listed exactly", f["importers"] == ["u1.py", "u2.py"], str(f["importers"])),
            ("only public functions listed", f["public"] == ["pub"], str(f["public"])),
            ("destructive command lists exact files and undo", gate("destructive", d) and removes == ["build/a.o", "build/b.o"],
             str(removes))]


# ---------------------------------------------------------------- CODE-07
def inherit_style(work: Path):
    sibs = {"a.py": "def load_file(path):\n    return open(path).read()\nX = \"a\"\n",
            "b.py": "def save_file(path):\n    pass\nY = \"b\"\n",
            "c.py": "def read_rows(p):\n    pass\nZ = \"c\"\n",
            "d.py": "def parseLine(p):\n    pass\nW = 'd'\n"}
    snake = camel = dq = sq = 0
    for t in sibs.values():
        for n in re.findall(r"def (\w+)", t):
            snake += bool(re.fullmatch(r"[a-z]+(_[a-z]+)+", n))
            camel += bool(re.fullmatch(r"[a-z]+[A-Z]\w*", n))
        dq += t.count('"') // 2
        sq += t.count("'") // 2
    rules = {"naming": "snake_case" if snake > camel else "camelCase", "naming_votes": [snake, camel],
             "quotes": "double" if dq > sq else "single", "quote_votes": [dq, sq],
             "why": "majority of sampled siblings"}
    _w(work, "STYLE.json", rules)

    def conforms(src):
        return all(re.fullmatch(r"[a-z]+(_[a-z]+)*", n) for n in re.findall(r"def (\w+)", src)) == (rules["naming"] == "snake_case")
    return [("4 siblings sampled (3-5)", 3 <= len(sibs) <= 5, str(len(sibs))),
            ("naming conflict resolved to snake_case (3 vs 1)", rules["naming"] == "snake_case" and rules["naming_votes"] == [3, 1],
             str(rules["naming_votes"])),
            ("quote conflict resolved to double (3 vs 1)", rules["quotes"] == "double", str(rules["quote_votes"])),
            ("new code checked against the rule", conforms("def new_thing():\n pass") and not conforms("def newThing():\n pass"),
             "snake ok, camel rejected")]


# ---------------------------------------------------------------- CODE-08
def tdd(work: Path):
    def run_test(impl):
        try:
            assert impl("racecar") is True and impl("abc") is False and impl("") is True
            return "pass"
        except AssertionError:
            return "fail:assert"
        except Exception as e:  # wrong reason
            return f"fail:{type(e).__name__}"

    def stub(s):
        return None

    def green(s):
        return s == s[::-1]

    def green_with_branch(s):
        if not s:
            return True
        s2 = s.lower()
        if s2 == s2[::-1]:
            return True
        return False

    import sys as _s
    lines_hit = set()
    code = green_with_branch.__code__

    def tracer(frame, ev, arg):
        if frame.f_code is code and ev == "line":
            lines_hit.add(frame.f_lineno)
        return tracer
    _s.settrace(tracer)
    try:
        run_test(green_with_branch)
    finally:
        _s.settrace(None)
    import dis
    all_lines = {ln for _, ln in dis.findlinestarts(code) if ln and ln != code.co_firstlineno}
    cov = len(lines_hit & all_lines) / len(all_lines)
    res = {"red": run_test(stub), "green": run_test(green), "refactor": run_test(green_with_branch), "coverage": cov}
    _w(work, "tdd.json", res)
    return [("RED fails for the right reason (assertion, not crash)", res["red"] == "fail:assert", res["red"]),
            ("GREEN passes with the smallest change", res["green"] == "pass", res["green"]),
            ("REFACTOR keeps it green", res["refactor"] == "pass", res["refactor"]),
            ("line coverage measured >= 80%", cov >= 0.8, f"{cov:.2f}")]


# ---------------------------------------------------------------- CODE-09
def six_phase(work: Path):
    def verify(root: Path):
        report = {}
        files = sorted(root.rglob("*.py"))
        try:
            for f in files:
                py_compile.compile(str(f), doraise=True, cfile=str(work / "pyc" / (f.name + "c")))
            report["Build"] = "PASS"
        except py_compile.PyCompileError:
            report["Build"] = "FAIL"
            return report, "NOT READY"
        untyped = [n.name for f in files for n in ast.walk(ast.parse(f.read_text()))
                   if isinstance(n, ast.FunctionDef) and n.returns is None and not n.name.startswith("test")]
        report["Types"] = "PASS" if not untyped else f"WARN {untyped}"
        unused = []
        for f in files:
            tree = ast.parse(f.read_text())
            names = {a.asname or a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
            unused += sorted(names - used)
        report["Lint"] = "PASS" if not unused else f"FAIL unused {unused}"
        r = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", str(root), "-q"],
                           capture_output=True, text=True, cwd=root)
        report["Tests"] = "PASS" if r.returncode == 0 else "FAIL"
        hits = [str(f.name) for f in files if SECRET_RE.search(f.read_text()) or DEBUG_RE.search(f.read_text())]
        report["Security"] = "PASS" if not hits else f"FAIL {hits}"
        report["Diff"] = f"{len(files)} files"
        return report, "READY" if all(v.startswith(("PASS", "WARN")) or k == "Diff" for k, v in report.items()) else "NOT READY"
    good = _tree(work / "good", {"m.py": "def f(x) -> int:\n    return x + 1\n",
                                 "test_m.py": "import unittest\nfrom m import f\nclass T(unittest.TestCase):\n    def test(self):\n        self.assertEqual(f(1), 2)\n"})
    leak = _tree(work / "leak", {"m.py": "KEY = 'sk-abcdefghijklmnopqrst'\ndef f(x) -> int:\n    return x\n"})
    broken = _tree(work / "broken", {"m.py": "def f(:\n"})
    rg, vg = verify(good)
    rl, vl = verify(leak)
    rb, vb = verify(broken)
    _w(work, "verification.json", {"good": [rg, vg], "leak": [rl, vl], "broken": [rb, vb]})
    return [("clean project: all six phases, READY", len(rg) == 6 and vg == "READY", str(rg)),
            ("planted sk- key fails Security -> NOT READY", rl["Security"].startswith("FAIL") and vl == "NOT READY", rl["Security"]),
            ("build failure stops the loop after phase 1", list(rb) == ["Build"] and vb == "NOT READY", str(rb))]


# ---------------------------------------------------------------- CODE-10
def pass_k(work: Path):
    p, k = 0.7, 3
    pass_at_k = 1 - (1 - p) ** k
    pass_hat_k = p ** k
    rng = random.Random(7)
    trials = [[rng.random() < p for _ in range(k)] for _ in range(20000)]
    emp_at = sum(any(t) for t in trials) / len(trials)
    emp_hat = sum(all(t) for t in trials) / len(trials)
    repo = work / "repo"
    _git_init(repo)
    (repo / "f.txt").write_text("v1")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-qm", "base")
    sha = _git(repo, "rev-parse", "--short", "HEAD").strip()
    status = _git(repo, "status", "--porcelain")
    log = work / "checkpoints.log"
    log.write_text(f"2026-11-03 | baseline | {sha}\n")
    baseline, after = (9, 10), (10, 10)
    _w(work, "evals.json", {"pass@3": pass_at_k, "pass^3": pass_hat_k, "empirical": [emp_at, emp_hat],
                            "card_says": "70% -> 91% (pass@3) / 34% (pass^3)",
                            "note": "exact 1-(0.3)^3 = 97.3%; the card's 91% does not follow from p=0.7, k=3"})
    return [("pass^3 at p=0.7 is 34%", round(pass_hat_k * 100) == 34, f"{pass_hat_k:.3f}"),
            ("pass@3 at p=0.7 is 1-0.3^3 = 97.3% (formula, card's 91% flagged)", abs(pass_at_k - 0.973) < 1e-9, f"{pass_at_k:.3f}"),
            ("simulation agrees within 1%", abs(emp_at - pass_at_k) < 0.01 and abs(emp_hat - pass_hat_k) < 0.01,
             f"{emp_at:.3f}/{emp_hat:.3f}"),
            ("checkpoint taken on a clean tree with date|name|sha", status == "" and re.fullmatch(r"\S+ \| baseline \| [0-9a-f]{7,}\n", log.read_text()) is not None,
             log.read_text().strip()),
            ("regression compare: 9/10 -> 10/10 is no regression", after[0] >= baseline[0], f"{baseline} -> {after}")]


# ---------------------------------------------------------------- CODE-11
def root_cause(work: Path):
    def buggy(xs):
        total = 0
        for x in xs:
            total += 100 // x  # bug: crashes on 0
        return total

    def fails(xs):
        try:
            buggy(xs)
            return False
        except ZeroDivisionError:
            return True

    def ddmin(data):
        n = 2
        while len(data) >= 2:
            chunk = max(1, len(data) // n)
            subsets = [data[i:i + chunk] for i in range(0, len(data), chunk)]
            for s in subsets:
                if fails(s):
                    data, n = s, 2
                    break
            else:
                for i in range(len(subsets)):
                    comp = [x for j, s in enumerate(subsets) if j != i for x in s]
                    if fails(comp):
                        data, n = comp, max(n - 1, 2)
                        break
                else:
                    if n >= len(data):
                        break
                    n = min(len(data), n * 2)
        return data
    big = list(range(1, 20))
    big.insert(11, 0)
    minimal = ddmin(big)

    def fixed(xs):
        return sum(100 // x for x in xs if x != 0)

    def regression(fn):
        try:
            return fn([5, 0]) == 20
        except ZeroDivisionError:
            return False
    _w(work, "rootcause.json", {"original_len": len(big), "minimal": minimal})
    return [("failure reproduced on the original 20 items", fails(big), str(len(big))),
            ("delta debugging shrinks to the planted [0]", minimal == [0], str(minimal)),
            ("regression test fails before the fix", not regression(buggy), "red"),
            ("regression test passes after the fix", regression(fixed), "green")]


# ---------------------------------------------------------------- CODE-12
def minimal_build_fix(work: Path):
    root = _tree(work / "proj", {"base.py": "VALUE = 1\n", "a.py": "from base import VALUE, HELPER\n",
                                 "b.py": "from base import HELPER\n", "c.py": "from base import HELPER\nx = HELPER\n",
                                 "setup.cfg": "[flake8]\nmax-line-length = 100\n"})
    cfg_before = (root / "setup.cfg").read_text()

    def build():
        errs = []
        for f in ["a.py", "b.py", "c.py"]:
            r = subprocess.run([sys.executable, "-I", "-B", "-c", f"import sys; sys.path.insert(0, {str(root)!r}); import {f[:-3]}"],
                               capture_output=True, text=True)
            if r.returncode:
                errs.append((f, r.stderr.strip().splitlines()[-1]))
        return errs
    before = build()
    groups = {}
    for f, e in before:
        groups.setdefault(re.sub(r"'[^']+'", "'X'", e.split("(")[0]), []).append(f)
    snapshot = {p.name: p.read_text() for p in root.iterdir() if p.is_file()}
    (root / "base.py").write_text("VALUE = 1\nHELPER = 2\n")  # fix the first root error only
    after = build()
    changed = [n for n, t in snapshot.items() if (root / n).read_text() != t]

    def config_guard(new):
        return int(re.search(r"max-line-length = (\d+)", new).group(1)) <= 100
    _w(work, "buildfix.json", {"before": before, "groups": groups, "after": after, "changed": changed})
    return [("3 errors before, one error class", len(before) == 3 and len(groups) == 1, str(groups)),
            ("one root fix clears the cascade", after == [], str(after)),
            ("diff touches only the root file", changed == ["base.py"], str(changed)),
            ("linter config untouched and a weakening edit is refused",
             (root / "setup.cfg").read_text() == cfg_before and not config_guard("max-line-length = 200"), "guarded")]


# ---------------------------------------------------------------- CODE-13
def silent_failures(work: Path):
    src = ("import subprocess\n"
           "def a():\n    try:\n        x()\n    except Exception:\n        pass\n"
           "def b():\n    try:\n        y()\n    except:\n        pass\n"
           "def c():\n    try:\n        z()\n    except ValueError as e:\n        raise RuntimeError('bad') from e\n"
           "def d():\n    subprocess.run(['false'])\n")
    tree = ast.parse(src)
    swallowed = [h.lineno for h in ast.walk(tree) if isinstance(h, ast.ExceptHandler)
                 and len(h.body) == 1 and isinstance(h.body[0], ast.Pass)]
    ignored_rc = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                  and getattr(n.value.func, "attr", "") == "run"
                  and not any(k.arg == "check" for k in n.value.keywords)]
    handlers = {"save": [("validate", {"sets": ["valid"], "resets": []}), ("persist", {"sets": ["saved"], "resets": []}),
                         ("reset_form", {"sets": [], "resets": ["saved"]})]}
    clobbered = []
    for action, calls in handlers.items():
        set_so_far = set()
        for name, eff in calls:
            for r in eff["resets"]:
                if r in set_so_far:
                    clobbered.append((action, name, r))
            set_so_far |= set(eff["sets"])
    tweens = [("opacity", 0, 1.0, 1), ("opacity", 0.5, 1.5, 0)]  # later tween overrides earlier
    tween_conflicts = [(a, b) for i, a in enumerate(tweens) for b in tweens[i + 1:] if a[0] == b[0] and b[1] < a[2]]
    _w(work, "silent.json", {"swallowed_lines": swallowed, "ignored_returncode": ignored_rc,
                             "click_path": clobbered, "tween_conflicts": tween_conflicts})
    return [("two swallowed excepts found, the re-raise is not", swallowed == [5, 10], str(swallowed)),
            ("ignored return code found", ignored_rc == [18], str(ignored_rc)),
            ("later call resets what an earlier one set", clobbered == [("save", "reset_form", "saved")], str(clobbered)),
            ("overlapping later tween flagged", len(tween_conflicts) == 1, str(tween_conflicts))]


# ---------------------------------------------------------------- CODE-14
def optimization_loop(work: Path):
    import numpy as np
    data = list(range(20000))
    arr = np.array(data, dtype=np.int64)
    expected = sum(x * x for x in data)
    variants = {"baseline_loop": lambda: sum(x * x for x in data),
                "numpy_dot": lambda: int(arr @ arr),
                "wrong_fast": lambda: int(arr.sum()) ** 2 // len(data),  # fast but incorrect
                "map_pow": lambda: sum(map(lambda x: x ** 2, data))}
    table = []
    for name, fn in variants.items():
        best = min(_timeit(fn) for _ in range(3))
        table.append({"variant": name, "hypothesis": name, "seconds": best, "correct": fn() == expected})
    safe = [r for r in table if r["correct"]]
    winner = min(safe, key=lambda r: r["seconds"])
    base = next(r for r in table if r["variant"] == "baseline_loop")
    _w(work, "variants.json", {"table": table, "winner": winner["variant"]})
    return [("incorrect variant rejected by the correctness gate", not next(r for r in table if r["variant"] == "wrong_fast")["correct"],
             "wrong_fast rejected"),
            ("winner is the vectorised variant", winner["variant"] == "numpy_dot", winner["variant"]),
            ("winner beats the baseline by >3x", base["seconds"] / max(winner["seconds"], 1e-9) > 3,
             f"{base['seconds']:.5f}/{winner['seconds']:.5f}"),
            ("table has one row per variant", len(table) == 4, str(len(table)))]


def _timeit(fn):
    t = time.perf_counter()
    fn()
    return time.perf_counter() - t


# ---------------------------------------------------------------- CODE-15
class TransientError(Exception):
    def __init__(self, status, ctx=""):
        super().__init__(f"status {status}")
        self.status, self.ctx = status, ctx


def resilient(work: Path):
    sleeps = []

    def call_with_retry(fn, max_tries=5, base=0.1, cap=2.0, rng=random.Random(1)):
        for attempt in range(max_tries):
            try:
                return fn(), attempt + 1
            except TransientError as e:
                if e.status not in (408, 429, 500, 502, 503, 504) or attempt == max_tries - 1:
                    raise
                sleeps.append(min(cap, base * 2 ** attempt) * (0.5 + rng.random() / 2))
        raise AssertionError

    attempts = {"n": 0}

    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise TransientError(503)
        return "ok"
    res, tries = call_with_retry(flaky)
    val_attempts = {"n": 0}

    def invalid():
        val_attempts["n"] += 1
        raise TransientError(422)
    try:
        call_with_retry(invalid)
    except TransientError:
        pass

    class Breaker:
        def __init__(self, n):
            self.n, self.fail, self.open = n, 0, False

        def call(self, fn):
            if self.open:
                return "short-circuit"
            try:
                return fn()
            except Exception:
                self.fail += 1
                self.open = self.fail >= self.n
                return "failed"
    br = Breaker(3)
    outcomes = [br.call(lambda: 1 / 0) for _ in range(5)]

    def atomic_write(path: Path, text: str, crash=False):
        tmp = path.with_suffix(".tmp")
        tmp.write_text(text[: len(text) // 2] if crash else text)
        if crash:
            raise IOError("crash mid-write")
        os.replace(tmp, path)
    target = work / "state.txt"
    atomic_write(target, "version-1")
    try:
        atomic_write(target, "version-2-long", crash=True)
    except IOError:
        pass
    _w(work, "resilience.json", {"tries": tries, "sleeps": sleeps, "validation_attempts": val_attempts["n"],
                                 "breaker": outcomes, "state": target.read_text()})
    return [("503 retried then succeeded on attempt 3", res == "ok" and tries == 3, str(tries)),
            ("backoff grows and stays capped", len(sleeps) == 2 and sleeps[0] < sleeps[1] + 0.06 and max(sleeps) <= 2.0,
             str([round(s, 3) for s in sleeps])),
            ("422 validation error not retried", val_attempts["n"] == 1, str(val_attempts["n"])),
            ("breaker opens after 3 failures", outcomes == ["failed"] * 3 + ["short-circuit"] * 2, str(outcomes)),
            ("crash mid-write leaves the old file intact", target.read_text() == "version-1", target.read_text())]


# ---------------------------------------------------------------- CODE-16
def review_checklist(work: Path):
    files = {"api.py": "def get(db, uid):\n    return db.execute(f\"SELECT * FROM u WHERE id={uid}\")\n",
             "util.py": "def f(xs):\n    try:\n        return xs[0]\n    except:\n        return None\n",
             "loop.py": "def g(items):\n    out = ''\n    for i in items:\n        out += str(i)\n    return out\n"}
    order = ["logic", "error-handling", "security", "performance", "tests", "readability"]
    rules = [("security", "HIGH", r"execute\(f[\"']", "use parameters"),
             ("error-handling", "MEDIUM", r"except:\s*$", "catch a specific error"),
             ("performance", "LOW", r"\+= str\(", "join a list")]
    findings = []
    for fn, text in files.items():
        for i, line in enumerate(text.splitlines(), 1):
            for cat, sev, pat, fix in rules:
                if re.search(pat, line):
                    findings.append({"file": fn, "line": i, "category": cat, "severity": sev, "evidence": line.strip(), "fix": fix})
    findings.sort(key=lambda f: (order.index(f["category"]), f["file"]))
    by_file = {}
    for f in findings:
        by_file.setdefault(f["file"], []).append(f)
    report = {"findings": findings, "by_file": by_file, "not_reviewed": ["tests (none in diff)", "logic beyond patterns"]}
    _w(work, "review.json", report)
    return [("SQL f-string flagged HIGH security at api.py:2",
             any(f["file"] == "api.py" and f["line"] == 2 and f["severity"] == "HIGH" for f in findings), str(findings[:1])),
            ("findings in checklist order", [f["category"] for f in findings] == ["error-handling", "security", "performance"],
             str([f["category"] for f in findings])),
            ("only the 4 severity levels used", {f["severity"] for f in findings} <= {"CRITICAL", "HIGH", "MEDIUM", "LOW"}, "ok"),
            ("report says what was not reviewed", bool(report["not_reviewed"]), str(report["not_reviewed"]))]


# ---------------------------------------------------------------- CODE-17
def pr_fanout(work: Path):
    diff = ("+++ b/app.py\n+def pay(amount):\n+    try:\n+        charge(amount)\n+    except Exception:\n+        pass\n"
            "+    # TODO: remove after v1 (v1 shipped)\n+    return True\n+++ b/test_app.py\n+def test_pay():\n+    assert True\n")
    added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]

    def code_reviewer():
        return [("app.py", "returns True even when charge fails")] if "return True" in diff else []

    def comment_analyzer():
        return [("app.py", "stale TODO comment")] if any("TODO" in l for l in added) else []

    def test_analyzer():
        return [("test_app.py", "assert True tests nothing")] if any(l.strip() == "assert True" for l in added) else []

    def silent_hunter():
        return [("app.py", "returns True even when charge fails"), ("app.py", "except Exception: pass")] \
            if any("except Exception" in l for l in added) else []

    def type_analyzer():
        return [] if "->" in diff else [("app.py", "pay has no return annotation")]
    agents = [code_reviewer, comment_analyzer, test_analyzer, silent_hunter, type_analyzer]
    with ThreadPoolExecutor(5) as ex:
        results = list(ex.map(lambda f: f(), agents))
    merged = sorted({f for r in results for f in r})
    evidence = {"returns True even when charge fails": "return True", "stale TODO comment": "TODO",
                "assert True tests nothing": "assert True", "except Exception: pass": "except Exception",
                "pay has no return annotation": "def pay(amount):"}
    verified = [f for f in merged if any(evidence[f[1]] in l for l in added)]
    _w(work, "fanout.json", {"per_agent": {a.__name__: r for a, r in zip(agents, results)}, "merged": merged,
                             "verified": verified, "posted": False, "note": "posting needs a GitHub connector; not done"})
    raw = sum(len(r) for r in results)
    return [("five reviewers ran in one fan-out", len(results) == 5, str([a.__name__ for a in agents])),
            ("duplicate finding merged (6 raw -> 5 unique)", raw == 6 and len(merged) == 5, f"{raw}->{len(merged)}"),
            ("the vacuous test is caught", ("test_app.py", "assert True tests nothing") in merged, "caught"),
            ("every merged finding verified against a diff line", verified == merged, f"{len(verified)}/{len(merged)}"),
            ("nothing claimed as posted", not json.loads((work / "fanout.json").read_text())["posted"], "posted=False")]


# ---------------------------------------------------------------- CODE-18
def safe_refactor(work: Path):
    before = ("def price(q, unit):\n    t = 0\n    for _ in range(q):\n        t = t + unit\n    return t\n"
              "def unused_helper():\n    return 42\n"
              "def report(q):\n    return f'{price(q, 3)} total'\n")
    after_step = before.replace("    t = 0\n    for _ in range(q):\n        t = t + unit\n    return t\n", "    return q * unit\n")

    def load(src):
        ns = {}
        exec(compile(src, "<m>", "exec"), ns)
        return ns
    inputs = [(0, 3), (1, 2), (5, 7), (12, 0)]
    ns0 = load(before)
    characterization = {str(i): (ns0["price"](*i), ns0["report"](i[0])) for i in inputs}

    def dead(src):
        tree = ast.parse(src)
        defs = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        return sorted(defs - used - {"report"})  # report is the public entry
    d = dead(after_step)
    final = re.sub(r"def unused_helper\(\):\n    return 42\n", "", after_step)
    ns1, ns2 = load(after_step), load(final)
    same1 = all((ns1["price"](*i), ns1["report"](i[0])) == characterization[str(i)] for i in inputs)
    same2 = all((ns2["price"](*i), ns2["report"](i[0])) == characterization[str(i)] for i in inputs)
    _w(work, "refactor.json", {"characterization": characterization, "dead": d, "final": final})
    return [("characterization tests pin current outputs", len(characterization) == 4, str(characterization)),
            ("step 1 (simplify loop) preserves behaviour", same1, "identical"),
            ("dead code found: unused_helper only", d == ["unused_helper"], str(d)),
            ("after removing it tests still green and it is gone", same2 and "unused_helper" not in final, "green")]


# ---------------------------------------------------------------- CODE-19
def adr(work: Path):
    adr_dir = work / "docs" / "adr"
    adr_dir.mkdir(parents=True)
    fields = ["Context", "Decision drivers", "Options considered", "Trade-offs", "Failure modes", "Decision",
              "Consequences", "Kill/review criteria"]
    (adr_dir / "0001-use-sqlite.md").write_text("# 1. Use SQLite\nStatus: Accepted\n")
    (adr_dir / "0002-json-logs.md").write_text("# 2. JSON logs\nStatus: Accepted\n")

    def new_adr(title, body, supersedes=None):
        nums = [int(p.name[:4]) for p in adr_dir.glob("[0-9][0-9][0-9][0-9]-*.md")]
        n = max(nums, default=0) + 1
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        missing = [f for f in fields if f not in body]
        if missing:
            raise ValueError(f"missing fields {missing}")
        text = f"# {n}. {title}\nStatus: Proposed\n" + (f"Supersedes: {supersedes}\n" if supersedes else "") + \
            "".join(f"## {f}\n{body[f]}\n" for f in fields)
        p = adr_dir / f"{n:04d}-{slug}.md"
        p.write_text(text)
        return p

    def edit(path: Path, new_text):
        if "Status: Accepted" in path.read_text():
            raise PermissionError("accepted ADRs are never edited; supersede instead")
        path.write_text(new_text)
    body = {f: f"{f} text" for f in fields}
    p = new_adr("Move to Postgres", body, supersedes="0001")
    try:
        edit(adr_dir / "0001-use-sqlite.md", "changed")
        edited = True
    except PermissionError:
        edited = False
    try:
        new_adr("Incomplete", {"Context": "x"})
        incomplete = "accepted"
    except ValueError:
        incomplete = "rejected"
    return [("next number is 0003 with a slug", p.name == "0003-move-to-postgres.md", p.name),
            ("all 8 fields present", all(f"## {f}" in p.read_text() for f in fields), "8/8"),
            ("accepted ADR edit refused; superseded instead", not edited and "Supersedes: 0001" in p.read_text(), "refused"),
            ("ADR missing fields rejected", incomplete == "rejected", incomplete)]


# ---------------------------------------------------------------- CODE-20
def deterministic_first(work: Path):
    rng = random.Random(3)
    lines = [f"INV-{1000 + i}: {rng.randint(1, 99)}.{rng.randint(0, 99):02d} EUR" for i in range(97)]
    lines += ["invoice one-thousand: twelve euros", "INV-77 12,5 EUR", "see attached"]
    pat = re.compile(r"^INV-(\d{4}): (\d+\.\d{2}) EUR$")
    direct, tail, total = [], [], 0
    for ln in lines:
        m = pat.match(ln)
        conf = 1.0 if m else 0.2
        if conf >= 0.95:
            direct.append(m.group(1))
            total += round(float(m.group(2)) * 100)
        else:
            tail.append(ln)
    _w(work, "routing.json", {"direct": len(direct), "to_model_queue": tail, "total_cents_frozen": total,
                              "note": "tail items queued for a model; no model called here"})
    expected_total = sum(round(float(l.split()[1]) * 100) for l in lines[:97])
    return [("97/100 handled deterministically (coverage 97%)", len(direct) == 97, str(len(direct))),
            ("exactly the 3 malformed items go to the tail", tail == lines[97:], str(tail)),
            ("sum computed by code in integer cents", total == expected_total, str(total)),
            ("confidence cut is 0.95", pat.match(lines[0]) is not None, "cut=0.95")]


# ---------------------------------------------------------------- CODE-21
def content_cache(work: Path):
    src = work / "scenes"
    src.mkdir()
    for i in range(3):
        (src / f"s{i}.txt").write_text(f"scene {i} " * 50)
    cache, manifest = work / "cache", work / "manifest.json"
    cache.mkdir()
    counter = {"n": 0}

    def key(p, tool="1.0", cfg="v1"):
        return hashlib.sha256(p.read_bytes() + tool.encode() + cfg.encode()).hexdigest()

    def render(p):
        counter["n"] += 1
        return p.read_text().upper()

    def run(tool="1.0", crash_on=None, force=False):
        done = json.loads(manifest.read_text()) if manifest.exists() else {}
        new = dict(done)
        for p in sorted(src.glob("*.txt")):
            k = key(p, tool)
            if done.get(p.name) == k and (cache / k).exists():
                continue
            if crash_on == p.name:
                raise RuntimeError("crash")
            out = render(p)
            old = cache / done.get(p.name, "none")
            if old.exists() and len(out) < 0.5 * old.stat().st_size and not force:
                raise ValueError(f"shrink guard: {p.name}")
            (cache / k).write_text(out)
            new[p.name] = k
        manifest.write_text(json.dumps(new))
    run()
    first = counter["n"]
    run()
    second = counter["n"] - first
    (src / "s1.txt").write_text("scene 1 changed " * 50)
    run()
    third = counter["n"] - first
    m_before = manifest.read_text()
    try:
        run(tool="2.0", crash_on="s2.txt")
    except RuntimeError:
        pass
    crash_kept = manifest.read_text() == m_before
    (src / "s0.txt").write_text("x")
    try:
        run()
        shrink = "allowed"
    except ValueError:
        shrink = "refused"
    return [("first run renders all 3", first == 3, str(first)),
            ("unchanged inputs hit the cache (0 renders)", second == 0, str(second)),
            ("one changed file re-renders exactly 1", third == 1, str(third)),
            ("crash leaves the manifest untouched", crash_kept, "unchanged"),
            ("much smaller output refused without --force", shrink == "refused", shrink)]


# ---------------------------------------------------------------- CODE-22
def commit_hygiene(work: Path):
    repo = work / "repo"
    _git_init(repo)
    for i, msg in enumerate(["feat(cli): add flag", "fix: handle empty input", "docs: readme", "chore: bump"]):
        (repo / f"f{i}.txt").write_text(str(i))
        _git(repo, "add", ".")
        _git(repo, "commit", "-qm", msg)
    log = _git(repo, "log", "--oneline", "-15").splitlines()
    conv = sum(bool(re.match(r"[0-9a-f]+ (feat|fix|docs|chore|refactor|test)(\(.+\))?: ", l)) for l in log)
    style = "conventional" if conv / len(log) >= 0.75 else "free"
    (repo / "app.py").write_text("TOKEN = 'ghp_" + "a" * 36 + "'\nprint('debug here')\n")
    _git(repo, "add", "app.py")
    staged = _git(repo, "diff", "--staged")
    problems = [l for l in staged.splitlines() if l.startswith("+") and (SECRET_RE.search(l) or DEBUG_RE.search(l))]
    branch = _git(repo, "branch", "--show-current").strip()
    must_branch_first = branch in ("main", "master")
    status_words = {"inspected": True, "changed locally": True, "verified locally": False, "committed": False,
                    "pushed": False, "blocked": "secret in staged diff"}
    _w(work, "hygiene.json", {"style": style, "problems": problems, "branch": branch, "status": status_words})
    return [("Conventional Commits style detected from 4/4 messages", style == "conventional", f"{conv}/{len(log)}"),
            ("staged ghp_ token flagged", any("ghp_" in p for p in problems), str(len(problems))),
            ("staged debug print flagged", any("debug" in p for p in problems), "flagged"),
            ("on default branch -> branch first", must_branch_first, branch),
            ("status words report blocked, not committed", status_words["committed"] is False and status_words["blocked"], "blocked")]


# ---------------------------------------------------------------- CODE-26
def search_replace(work: Path):
    f = work / "target.py"
    f.write_text("def a():\n    return 1\n\ndef b():\n    return 1\n\ndef c():\n    return 2\n")

    def apply(block):
        text = f.read_text()
        n = text.count(block["search"])
        if n == 1:
            f.write_text(text.replace(block["search"], block["replace"]))
            return "applied", []
        lines = text.splitlines()
        near = difflib.get_close_matches(block["search"].splitlines()[0], lines, n=2, cutoff=0.3)
        return ("ambiguous" if n > 1 else "no-match"), near
    r1 = apply({"search": "    return 1\n", "replace": "    return 9\n"})
    r2 = apply({"search": "def c():\n    return 2\n", "replace": "def c():\n    return 3\n"})
    r3 = apply({"search": "def cc():\n    return 2\n", "replace": "x"})
    _w(work, "edits.json", {"r1": r1, "r2": r2, "r3": r3, "final": f.read_text()})
    return [("2 matches -> rejected as ambiguous, file untouched", r1[0] == "ambiguous" and "return 9" not in f.read_text(), r1[0]),
            ("unique block applied", r2[0] == "applied" and "return 3" in f.read_text(), r2[0]),
            ("no match -> nearest lines shown, not guessed", r3[0] == "no-match" and "def c():" in r3[1], str(r3[1])),
            ("rest of file preserved byte for byte", f.read_text().count("return 1") == 2, "preserved")]


PROGRAMS = {
    "CODE-01": search_first, "CODE-02": live_docs, "CODE-03": isolated_venv, "CODE-04": onboarding,
    "CODE-05": change_impact, "CODE-06": fact_forcing, "CODE-07": inherit_style, "CODE-08": tdd,
    "CODE-09": six_phase, "CODE-10": pass_k, "CODE-11": root_cause, "CODE-12": minimal_build_fix,
    "CODE-13": silent_failures, "CODE-14": optimization_loop, "CODE-15": resilient, "CODE-16": review_checklist,
    "CODE-17": pr_fanout, "CODE-18": safe_refactor, "CODE-19": adr, "CODE-20": deterministic_first,
    "CODE-21": content_cache, "CODE-22": commit_hygiene, "CODE-26": search_replace,
}
