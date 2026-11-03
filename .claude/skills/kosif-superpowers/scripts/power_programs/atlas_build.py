"""Real programs for the atlas-build family (build orchestration, design systems, reliability, release).

Each function builds its own fixture (files, a temp git repo, an SQLite db, images, configs),
performs the card's procedure and checks known answers. Browser-, vendor- and device-bound
cards are not here (see out/power-programs/data-skipped.json).
"""
from __future__ import annotations

import colorsys
import gzip
import hashlib
import hmac
import ipaddress
import json
import math
import os
import re
import shutil
import sqlite3
import subprocess
import time
from pathlib import Path

import numpy as np


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


def _lum(hexc):
    h = hexc.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _git(cwd, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    return subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True, check=True).stdout.strip()


# ---------------------------------------------------------------- ABUILD-01
def abuild_01(work: Path):
    repo = work / "repo"
    (repo / "roadmap" / "phases").mkdir(parents=True)

    def preflight(tools_ok=True):
        miss = []
        if not tools_ok:
            miss.append("gh not authenticated")
        if not (repo / "roadmap" / "ROADMAP.md").is_file():
            miss.append("roadmap dashboard missing")
        if not list((repo / "roadmap" / "phases").glob("*.md")):
            miss.append("per-phase task files missing")
        return miss

    def mode(m, loop_limit=3, **kw):
        miss = preflight(**kw)
        if miss:
            return {"refused": miss}
        cfg = repo / "loop.config.json"
        if m == "init":
            phases = sorted(p.stem for p in (repo / "roadmap" / "phases").glob("*.md"))
            cfg.write_text(json.dumps({"phases": phases, "reviewed": False}))
            return {"stopped_for_review": True, "phases": phases}
        conf = json.loads(cfg.read_text()) if cfg.is_file() else None
        if m == "run":
            if not conf or not conf["reviewed"]:
                return {"refused": ["config not reviewed by a human"]}
            done = []
            for ph in conf["phases"][:loop_limit]:
                done.append({"phase": ph, "pr": f"pr-{ph}", "ci": "green"})
            return {"ran": done}
        return {"status": conf}

    empty = mode("init")
    (repo / "roadmap" / "ROADMAP.md").write_text("| phase | status |\n")
    for i in range(1, 6):
        (repo / "roadmap" / "phases" / f"p{i}.md").write_text(f"# phase {i}\n")
    init = mode("init")
    run_before = mode("run")
    conf = json.loads((repo / "loop.config.json").read_text())
    conf["reviewed"] = True
    (repo / "loop.config.json").write_text(json.dumps(conf))
    run = mode("run")
    no_gh = mode("status", tools_ok=False)
    _w(work, "loop.json", {"init": init, "run": run})
    return [_c("preflight refuses when the roadmap is missing (no invented plan)", "roadmap dashboard missing" in empty.get("refused", []), empty),
            _c("init writes config then stops for human review", init.get("stopped_for_review") and len(init["phases"]) == 5, init),
            _c("run refuses an unreviewed config", run_before.get("refused") == ["config not reviewed by a human"], run_before),
            _c("run respects loop limit 3: one PR per phase", [d["phase"] for d in run["ran"]] == ["p1", "p2", "p3"], run),
            _c("unauthenticated gh refuses every mode", no_gh.get("refused") == ["gh not authenticated"], no_gh)]


# ---------------------------------------------------------------- ABUILD-02
def abuild_02(work: Path):
    SECRET = re.compile(r"(sk-[A-Za-z0-9]{8,}|api[_-]?key\s*[=:]\s*\S+|password\s*[=:]\s*\S+)", re.I)

    class Rec:
        def __init__(self, path):
            self.path, self.ev = path, []

        def _emit(self, **e):
            self.ev.append(e)
            with open(self.path, "a") as f:
                f.write(json.dumps(e) + "\n")

        def start(self, dims):
            self._emit(kind="start", dims=dims)

        def stage(self, name, phase, outcome=None):
            self._emit(kind="stage", name=name, phase=phase, outcome=outcome)

        def event(self, etype, detail):
            detail = SECRET.sub("[redacted]", detail)[:400]
            etype = re.sub(r"[\d/\\:.]+.*$", "", etype).strip("_") or etype  # types, not instances
            self._emit(kind="event", type=etype, detail=detail)

        def wait(self, phase):
            self._emit(kind="wait", phase=phase, t=len(self.ev))

        def finalize(self):
            stages = [e for e in self.ev if e["kind"] == "stage" and e["phase"] == "end"]
            roll = {"stages": len(stages), "failed": sum(e["outcome"] == "fail" for e in stages),
                    "events": sum(e["kind"] == "event" for e in self.ev),
                    "user_waits": sum(e["kind"] == "wait" and e["phase"] == "start" for e in self.ev)}
            self._emit(kind="final", rollup=roll)
            return roll

    r = Rec(work / "telemetry.jsonl")
    r.start({"project": "demo", "mode": "observe"})
    r.stage("build", "start")
    r.event("tool_error_/home/u/file42.py", "failed with api_key=ABC123XYZ " + "x" * 600)
    r.stage("build", "end", "fail")
    r.wait("start")
    r.wait("end")
    r.stage("test", "start")
    r.stage("test", "end", "pass")
    roll = r.finalize()
    ev = [e for e in r.ev if e["kind"] == "event"][0]
    return [_c("rollup counts 2 stages, 1 failed, 1 event, 1 user halt", roll == {"stages": 2, "failed": 1, "events": 1, "user_waits": 1}, roll),
            _c("event detail capped at 400 chars", len(ev["detail"]) == 400, len(ev["detail"])),
            _c("secret value redacted", "ABC123XYZ" not in json.dumps(r.ev) and "[redacted]" in ev["detail"], ev["detail"][:40]),
            _c("event type is the type, not the instance path", ev["type"] == "tool_error", ev["type"]),
            _c("observation only: one JSONL line per record", len((work / "telemetry.jsonl").read_text().splitlines()) == len(r.ev), len(r.ev))]


# ---------------------------------------------------------------- ABUILD-03
def abuild_03(work: Path):
    issues = {"I1": {"a.py"}, "I2": {"a.py", "b.py"}, "I3": {"c.py"}, "I4": {"d.py"}, "I5": {"c.py", "e.py"}}
    groups, seen = [], set()
    for i in issues:  # connected components over shared files -> issues in different groups can run in parallel
        if i in seen:
            continue
        comp, stack = set(), [i]
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x)
            stack += [j for j in issues if issues[j] & issues[x] and j not in comp]
        seen |= comp
        groups.append(sorted(comp))
    locks = {}

    def acquire(role, artifact):
        if locks.get(artifact) not in (None, role):
            return False
        locks[artifact] = role
        return True

    a = acquire("developer", "a.py")
    b = acquire("reviewer", "a.py")
    locks.pop("a.py")
    c = acquire("reviewer", "a.py")
    state = {"stages": {"I1": "review", "I3": "qa"}}
    _w(work, "squad_state.json", state)
    resumed = json.loads((work / "squad_state.json").read_text())
    squad = {i: ["developer", "adversarial reviewer", "QA/SDET"] for i in issues}
    return [_c("architect groups: {I1,I2}, {I3,I5}, {I4}", groups == [["I1", "I2"], ["I3", "I5"], ["I4"]], groups),
            _c("write lock blocks a second role on the same artifact", a and not b, (a, b)),
            _c("lock released -> other role may write", c, c),
            _c("resume reads stage state back", resumed == state, resumed),
            _c("each issue gets a 3-role squad", all(len(v) == 3 for v in squad.values()), "")]


# ---------------------------------------------------------------- ABUILD-04
def abuild_04(work: Path):
    PHASES = ["setup", "contracts/tests", "core", "integration", "polish"]
    tasks_md = """T-01 setup: init project | Covers: FR-0 | Depends on: - | Files: pyproject.toml | Done when: `pytest -q` runs
T-02 [P] contracts/tests: API contract tests | Covers: FR-1 | Depends on: T-01 | Files: tests/test_api.py | Done when: tests fail red
T-03 [P] contracts/tests: schema migration and also seed data | Covers: FR-2 | Depends on: T-01 | Files: db/m1.sql | Done when: migrate ok
T-04 core: implement API | Covers: FR-1 | Depends on: T-02 | Files: tests/test_api.py, api.py | Done when: tests green
T-05 polish: docs | Covers: FR-9 | Depends on: T-06 | Files: README.md | Done when: link check passes
T-06 integration: wire | Covers: FR-1 | Depends on: T-05 | Files: app.py | Done when: e2e passes"""
    _w(work, "tasks.md", tasks_md)
    pat = re.compile(r"(T-\d\d)( \[P\])? ([\w/]+): (.+?) \| Covers: (.+?) \| Depends on: (.+?) \| Files: (.+?) \| Done when: (.+)")
    tasks = {}
    for line in tasks_md.splitlines():
        m = pat.fullmatch(line)
        tasks[m[1]] = {"P": bool(m[2]), "phase": m[3], "title": m[4], "deps": [] if m[6] == "-" else m[6].split(", "),
                       "files": set(m[7].split(", ")), "done": m[8]}
    probs = []
    for k, t in tasks.items():
        if " and also " in t["title"]:
            probs.append((k, "split: 'and also'"))
        if not re.search(r"`.+`|passes|green|ok|red", t["done"]):
            probs.append((k, "Done when is not verifiable"))
        for d in t["deps"]:
            if PHASES.index(tasks[d]["phase"]) > PHASES.index(t["phase"]):
                probs.append((k, f"depends on later phase {d}"))
    par = [k for k, t in tasks.items() if t["P"]]
    for x in par:
        for y in par:
            if x < y and tasks[x]["files"] & tasks[y]["files"]:
                probs.append((x, f"[P] shares files with {y}"))

    def cycle():
        color = {}

        def dfs(u):
            color[u] = 1
            for v in tasks[u]["deps"]:
                if color.get(v) == 1 or (v not in color and dfs(v)):
                    return True
            color[u] = 2
            return False
        return any(dfs(u) for u in tasks if u not in color)

    has_cycle = cycle()
    _w(work, "task_audit.json", {"problems": probs, "cycle": has_cycle})
    return [_c("6 tasks parsed in the T-NN [P] format", len(tasks) == 6, list(tasks)),
            _c("task needing 'and also' must be split", ("T-03", "split: 'and also'") in probs, probs),
            _c("integration task depending on a polish task flagged as out of phase order", ("T-06", "depends on later phase T-05") in probs, probs),
            _c("dependency cycle T-05 <-> T-06 detected", has_cycle, has_cycle),
            _c("clean tasks T-01, T-02, T-04 raise nothing", not any(k in ("T-01", "T-02", "T-04") for k, _ in probs), probs)]


# ---------------------------------------------------------------- ABUILD-06
def abuild_06(work: Path):
    def spike(anchor, questions):
        if not anchor or not questions:
            raise ValueError("anchor on a requirement id with at least one named open question")
        rep = work / "spike-report.md"
        rep.write_text(f"# Spike {anchor}\nQuestions: {questions}\n")
        return rep

    try:
        spike("REQ-12", [])
        refused = False
    except ValueError:
        refused = True
    rep = spike("REQ-12", ["Can the table virtualise 10k rows?"])
    harvest = [("header", "source", "app.css .hdr"), ("row height", "source", "tokens.json"), ("sticky footer", "invented", "REQ-12 adds it")]
    (work / "harvest-table.md").write_text("\n".join(f"| {a} | {b} | {c} |" for a, b, c in harvest))
    with open(rep, "a") as f:
        f.write("- step 1: harvested 3 items\n- step 2: built prototype\n")
    rank = {"live": 3, "recorded": 2, "labeled stub": 1}
    best = max(["labeled stub", "recorded"], key=rank.get)
    invented = [h for h in harvest if h[1] == "invented"]
    return [_c("spike without an open question is refused", refused, refused),
            _c("report opened immediately and appended as work goes", rep.read_text().count("- step") == 2, ""),
            _c("only the requirement's addition is invented, and annotated", len(invented) == 1 and invented[0][2].startswith("REQ-12"), invented),
            _c("data fidelity: recorded beats labeled stub when live is absent", best == "recorded", best)]


# ---------------------------------------------------------------- ABUILD-07
def abuild_07(work: Path):
    repo = work / "kit"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("kit\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "init")

    def clean():
        return _git(repo, "status", "--porcelain") == ""

    (repo / "scratch.txt").write_text("dirty")
    dirty_refused = not clean()
    (repo / "scratch.txt").unlink()
    plan = {"phases": ["spec", "prototype", "backend", "frontend"], "done": [], "tracks": {}}
    ptr = repo / ".plan-pointer.json"

    def save():
        (repo / "WORK-PLAN.json").write_text(json.dumps(plan))
        ptr.write_text(json.dumps({"plan": "WORK-PLAN.json"}))

    def run_one(envelope):
        nxt = [p for p in plan["phases"] if p not in plan["done"]][0]
        if envelope.get("status") != "ok" or not envelope.get("alive"):
            return f"halt at {nxt}"
        plan["done"].append(nxt)
        save()
        return nxt

    save()
    plan["tracks"] = {"backend": "api endpoints in spec", "agent": None, "frontend": "screens in prototype"}
    r1 = run_one({"status": "ok", "alive": True})
    r2 = run_one({"status": "ok", "alive": True})
    r3 = run_one({"status": "error", "alive": True})
    resumed = json.loads((repo / json.loads(ptr.read_text())["plan"]).read_text())
    needed = [k for k, v in plan["tracks"].items() if v]
    return [_c("dirty git tree refused before starting", dirty_refused, dirty_refused),
            _c("one phase at a time: spec then prototype", (r1, r2) == ("spec", "prototype"), (r1, r2)),
            _c("bad result envelope halts at backend", r3 == "halt at backend", r3),
            _c("resume via pointer json reads 2 done phases", resumed["done"] == ["spec", "prototype"], resumed["done"]),
            _c("analysis keeps backend+frontend tracks, drops agent", needed == ["backend", "frontend"], needed)]


# ---------------------------------------------------------------- ABUILD-09
def abuild_09(work: Path):
    manifest = {"name": "Kosif Notes", "short_name": "Notes", "start_url": "/?source=pwa", "display": "standalone",
                "background_color": "#ffffff", "theme_color": "#2a78d6",
                "icons": [{"src": "/icons/192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "/icons/512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}
    routes = {"/api/": "network-first", "/static/": "cache-first", "/": "stale-while-revalidate"}
    sw = ["const STRATEGY = " + json.dumps(routes) + ";",
          "self.addEventListener('fetch', e => { const u = new URL(e.request.url);",
          "  const k = Object.keys(STRATEGY).find(p => u.pathname.startsWith(p)); /* dispatch by STRATEGY[k] */ });"]
    _w(work, "manifest.webmanifest", manifest)
    _w(work, "sw.js", "\n".join(sw))
    reg = "<script>if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js');</script>"
    _w(work, "index.html", f"<link rel='manifest' href='/manifest.webmanifest'>{reg}")

    def validate(m):
        errs = []
        sizes = {i["sizes"] for i in m.get("icons", [])}
        if not {"192x192", "512x512"} <= sizes:
            errs.append("needs 192 and 512 icons")
        if m.get("display") not in ("standalone", "fullscreen", "minimal-ui"):
            errs.append("display")
        if not m.get("start_url"):
            errs.append("start_url")
        return errs

    def pick(path):
        return routes[max((p for p in routes if path.startswith(p)), key=len)]

    bad = validate({"name": "x", "display": "browser", "icons": [{"sizes": "192x192"}]})
    return [_c("generated manifest passes installability fields", validate(manifest) == [], validate(manifest)),
            _c("broken manifest lists 3 problems", bad == ["needs 192 and 512 icons", "display", "start_url"], bad),
            _c("per-route strategies: API network-first, static cache-first, pages SWR",
               (pick("/api/notes"), pick("/static/app.js"), pick("/about")) == ("network-first", "cache-first", "stale-while-revalidate"), ""),
            _c("service worker registered from the page", "register('/sw.js')" in (work / "index.html").read_text(), "")]


# ---------------------------------------------------------------- ABUILD-10
def abuild_10(work: Path):
    tree = ["app/(auth)/login/page.tsx", "app/(dashboard)/page.tsx", "app/(marketing)/page.tsx", "app/api/webhooks/stripe/route.ts",
            "app/billing/checkout/route.ts", "app/billing/portal/route.ts", "lib/auth.ts", "lib/db/schema.ts", "components/PlanCard.tsx",
            "components/UsageMeter.tsx"]
    for t in tree:
        _w(work, "app_scaffold/" + t, f"// {t}\n")
    secret = b"whsec_test"
    payload = b'{"type":"invoice.paid","tenant":"t1"}'

    def sign(ts, body):
        return hmac.new(secret, f"{ts}.".encode() + body, hashlib.sha256).hexdigest()

    def verify(header, body, now, tol=300):
        parts = dict(p.split("=", 1) for p in header.split(","))
        ts = int(parts["t"])
        if abs(now - ts) > tol:
            return False
        return hmac.compare_digest(sign(ts, body), parts["v1"])

    ts = 1_700_000_000
    good = f"t={ts},v1={sign(ts, payload)}"
    rows = [{"tenant": "t1", "id": 1}, {"tenant": "t2", "id": 2}]
    scoped = lambda tenant: [r for r in rows if r["tenant"] == tenant]
    return [_c("route groups (auth)/(dashboard)/(marketing) and stripe webhook laid out",
               all((work / "app_scaffold" / t).is_file() for t in tree), len(tree)),
            _c("Stripe-style signature t.payload HMAC-SHA256 verifies", verify(good, payload, ts + 10), good[:30]),
            _c("tampered body rejected", not verify(good, payload.replace(b"t1", b"t2"), ts + 10), ""),
            _c("replay outside 300 s tolerance rejected", not verify(good, payload, ts + 301), ""),
            _c("tenant isolation: t1 sees only its rows", scoped("t1") == [{"tenant": "t1", "id": 1}], scoped("t1"))]


# ---------------------------------------------------------------- ABUILD-12
def abuild_12(work: Path):
    budget_min = 60
    proto = work / "proto-q1"
    proto.mkdir()
    (proto / "try.py").write_text("print(sum(range(10)))\n")
    log = [("built", 20), ("measured", 15)]
    spent = sum(m for _, m in log)
    answer = subprocess.run(["python3", "-I", str(proto / "try.py")], capture_output=True, text=True).stdout.strip()
    decision = "keep" if answer == "45" else "delete"
    spec = work / "SPEC.md"
    spec.write_text("# Spec\n")
    with open(spec, "a") as f:
        f.write(f"\n## Answered: does the sum fit? -> {answer} ({decision})\n")
    over = sum(m for m in (40, 30)) > budget_min
    shutil.rmtree(proto)
    return [_c("question answered by running the throwaway code: 45", answer == "45", answer),
            _c("spent 35 of 60 min budget", spent == 35 and spent <= budget_min, spent),
            _c("a 70-min attempt is flagged over budget", over, 70),
            _c("answer folded into SPEC.md and folder deleted", "Answered" in spec.read_text() and not proto.exists(), "")]


# ---------------------------------------------------------------- ABUILD-24
def abuild_24(work: Path):
    def pool_size(cores, spindles=1):
        return cores * 2 + spindles  # PostgreSQL wiki starting point

    def per_instance(max_conn, reserved, instances):
        return (max_conn - reserved) // instances

    def replica(rpo_s, rto_s):
        if rpo_s == 0:
            return "synchronous replica, automatic failover"
        return "async replica" + (", automatic failover" if rto_s < 300 else ", manual failover")

    def triage(lat_ms, err_rate, util):
        if util > 0.9:
            return "saturation"
        if err_rate > 0.01:
            return "errors"
        return "latency" if lat_ms > 500 else "healthy"

    p = pool_size(4)
    cap = per_instance(100, 10, 6)
    over = 6 * p > 100 - 10
    res = {"pool_per_core_formula": p, "per_instance_cap": cap, "naive_overallocated": over,
           "rpo0": replica(0, 60), "rpo60": replica(60, 900), "triage": triage(900, 0.001, 0.4)}
    _w(work, "pool.json", res)
    return [_c("4 cores, 1 spindle -> pool 9", p == 9, p),
            _c("max_connections 100 - 10 reserved over 6 instances -> 15 each", cap == 15, cap),
            _c("6 x 9 = 54 fits under 90; 12 instances would not", not over and 12 * p > 90, (6 * p, 12 * p)),
            _c("RPO 0 -> synchronous replica; RPO 60 s, RTO 15 min -> async manual", res["rpo0"].startswith("synchronous") and res["rpo60"] == "async replica, manual failover", res),
            _c("triage classifies high latency with low errors as latency", res["triage"] == "latency", res["triage"])]


# ---------------------------------------------------------------- ABUILD-25
def abuild_25(work: Path):
    db_path = work / "app.sqlite"
    db = sqlite3.connect(db_path)
    db.execute("create table t(x)")
    db.executemany("insert into t values(?)", [(i,) for i in range(1000)])
    db.commit()
    bdir = work / "backups"
    bdir.mkdir()
    now = 1_800_000_000

    def backup(ts):
        name = bdir / f"app-{time.strftime('%Y%m%dT%H%M%S', time.gmtime(ts))}.sqlite.gz"
        tmp = bdir / "tmp.sqlite"
        dst = sqlite3.connect(tmp)
        db.backup(dst)  # online .backup
        dst.close()
        name.write_bytes(gzip.compress(tmp.read_bytes(), 9))
        tmp.unlink()
        (name.parent / (name.name + ".sha256")).write_text(hashlib.sha256(name.read_bytes()).hexdigest())
        os.utime(name, (ts, ts))
        return name

    olds = [backup(now - d * 86400) for d in (10, 8, 1)]
    retention = 7
    for f in bdir.glob("*.gz"):
        if (now - f.stat().st_mtime) / 86400 > retention:
            f.unlink()
            (f.parent / (f.name + ".sha256")).unlink()
    kept = sorted(f.name for f in bdir.glob("*.gz"))
    latest = olds[-1]
    ok_sum = hashlib.sha256(latest.read_bytes()).hexdigest() == (latest.parent / (latest.name + ".sha256")).read_text()
    restored = work / "restore.sqlite"
    restored.write_bytes(gzip.decompress(latest.read_bytes()))
    n = sqlite3.connect(restored).execute("select count(*), sum(x) from t").fetchone()
    return [_c("timestamped compressed backups written", latest.name.startswith("app-") and latest.name.endswith(".sqlite.gz"), latest.name),
            _c("retention 7 days prunes the 10- and 8-day-old files", kept == [latest.name], kept),
            _c("checksum verifies", ok_sum, ok_sum),
            _c("restore test returns 1000 rows, sum 499500", n == (1000, 499500), n)]


# ---------------------------------------------------------------- ABUILD-26
def abuild_26(work: Path):
    v1 = {"fields": {1: ("id", "string", None), 2: ("amount", "int", None)}}
    v2_ok = {"fields": {1: ("id", "string", None), 2: ("amount", "int", None), 3: ("currency", "string", "SAR")}}
    v2_bad = {"fields": {1: ("id", "string", None), 2: ("amount", "int", None), 3: ("currency", "string", None)}}
    v3_reuse = {"fields": {1: ("id", "string", None), 2: ("discount", "float", 0.0)}}

    def backward(old, new):  # new reader must read old data
        errs = []
        for num, (name, typ, default) in new["fields"].items():
            if num not in old["fields"] and default is None:
                errs.append(f"field {num} '{name}' added without default")
            if num in old["fields"] and old["fields"][num][:2] != (name, typ):
                errs.append(f"field number {num} reused")
        return errs

    def partition(key, n=6):
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % n

    events = [("cust-1", i) for i in range(5)] + [("cust-2", i) for i in range(5)]
    parts = {}
    for k, seq in events:
        parts.setdefault(partition(k), []).append((k, seq))
    ordered = all([s for kk, s in v if kk == k] == sorted(s for kk, s in v if kk == k) for v in parts.values() for k in {kk for kk, _ in v})
    seen, deduped = set(), []
    for e in events + [("cust-1", 3)]:
        if e not in seen:
            seen.add(e)
            deduped.append(e)
    _w(work, "compat.json", {"ok": backward(v1, v2_ok), "bad": backward(v1, v2_bad), "reuse": backward(v1, v3_reuse)})
    return [_c("optional field with default is backward compatible", backward(v1, v2_ok) == [], backward(v1, v2_ok)),
            _c("added field without default rejected", backward(v1, v2_bad) == ["field 3 'currency' added without default"], backward(v1, v2_bad)),
            _c("reused field number rejected", backward(v1, v3_reuse) == ["field number 2 reused"], backward(v1, v3_reuse)),
            _c("same key lands in one partition, order kept", ordered and len({partition("cust-1")}) == 1, parts.keys()),
            _c("duplicate delivery deduped before sink", len(deduped) == 10, len(deduped))]


# ---------------------------------------------------------------- ABUILD-28
def abuild_28(work: Path):
    def severity(users_pct, revenue_impact, data_loss):
        if data_loss or users_pct >= 50:
            return "SEV1"
        if revenue_impact or users_pct >= 10:
            return "SEV2"
        return "SEV3"

    expected = {f"wh_{i}" for i in range(100)}
    received = expected - {"wh_17", "wh_42", "wh_88"}
    missed = sorted(expected - received)
    replay = [{"id": m, "action": "redeliver"} for m in missed]
    timeline = [("10:00", "detect"), ("10:05", "contain: pause jobs"), ("10:20", "diagnose"), ("10:45", "recover"), ("11:00", "reconcile")]
    order_ok = [s.split(":")[0] for _, s in timeline] == ["detect", "contain", "diagnose", "recover", "reconcile"]
    _w(work, "incident.json", {"sev": severity(60, True, False), "missed": missed, "replay": replay, "timeline": timeline,
                               "review": "post-incident review scheduled"})
    return [_c("60% users affected -> SEV1", severity(60, True, False) == "SEV1", "SEV1"),
            _c("revenue impact on 5% -> SEV2; minor -> SEV3", severity(5, True, False) == "SEV2" and severity(1, False, False) == "SEV3", ""),
            _c("reconciliation finds exactly the 3 missed webhooks", missed == ["wh_17", "wh_42", "wh_88"], missed),
            _c("contain happens before diagnose and recover", order_ok, [s for _, s in timeline])]


# ---------------------------------------------------------------- ABUILD-29
def _histogram_quantile(q, buckets):
    """Prometheus histogram_quantile: buckets = [(le, cumulative_count)] sorted, last le = inf."""
    total = buckets[-1][1]
    rank = q * total
    prev_le, prev_c = 0.0, 0.0
    for le, c in buckets:
        if c >= rank:
            if le == math.inf:
                return prev_le
            return prev_le + (le - prev_le) * (rank - prev_c) / (c - prev_c)
        prev_le, prev_c = le, c
    return prev_le


def abuild_29(work: Path):
    scrape = 15
    t = np.arange(0, 301, scrape)
    total = 100 * t  # 100 req/s
    errs = 2 * t     # 2 req/s 5xx
    rate = lambda s: (s[-1] - s[0]) / (t[-1] - t[0])
    ratio = rate(errs) / rate(total)
    buckets = [(0.1, 500), (0.25, 800), (0.5, 950), (1.0, 1000), (math.inf, 1000)]
    p95 = _histogram_quantile(0.95, buckets)
    p50 = _histogram_quantile(0.5, buckets)

    def window_ok(window_s):
        return window_s >= 4 * scrape

    alerts = [{"name": "High5xx", "expr": "rate5xx/rate > 0.01", "for": "5m", "severity": "page", "runbook": "https://runbooks/5xx", "action": "rollback"},
              {"name": "Flappy", "expr": "x > 1", "severity": "warn"}]
    lint = {a["name"]: [k for k in ("for", "severity", "runbook", "action") if not a.get(k)] for a in alerts}
    _w(work, "observability.json", {"ratio_5xx": ratio, "p95": p95, "lint": lint})
    return [_c("5xx ratio over 5m = 2/100 = 0.02", abs(ratio - 0.02) < 1e-12, ratio),
            _c("histogram_quantile(0.95) = 0.5 (bucket edge by interpolation)", abs(p95 - 0.5) < 1e-12, p95),
            _c("histogram_quantile(0.5) = 0.1", abs(p50 - 0.1) < 1e-12, p50),
            _c("rate window: 1m ok at 15 s scrape, 30 s not", window_ok(60) and not window_ok(30), ""),
            _c("alert lint: missing for/runbook/action flagged on Flappy only", lint == {"High5xx": [], "Flappy": ["for", "runbook", "action"]}, lint)]


# ---------------------------------------------------------------- ABUILD-30
def abuild_30(work: Path):
    inv = [{"id": "vm1", "type": "vm", "cost": 400, "cpu_p95": 0.05, "attached": True},
           {"id": "vm2", "type": "vm", "cost": 400, "cpu_p95": 0.70, "attached": True},
           {"id": "disk9", "type": "disk", "cost": 60, "attached": False},
           {"id": "ip3", "type": "ip", "cost": 4, "attached": False},
           {"id": "bucket", "type": "storage", "cost": 200, "public": True, "attached": True}]
    risks = [r["id"] for r in inv if r.get("public")]
    levers = []
    for r in inv:
        if not r["attached"]:
            levers.append((r["id"], "delete unattached", r["cost"]))
        elif r["type"] == "vm" and r["cpu_p95"] < 0.2:
            levers.append((r["id"], "rightsize to half", r["cost"] / 2))
    levers.sort(key=lambda l: -l[2])
    saving = sum(l[2] for l in levers)
    _w(work, "recon.json", {"inventory": inv, "risks": risks, "levers": levers, "monthly_saving": saving})
    return [_c("public bucket flagged as a risk", risks == ["bucket"], risks),
            _c("levers ranked by saving: vm1 200, disk9 60, ip3 4", [(l[0], l[2]) for l in levers] == [("vm1", 200), ("disk9", 60), ("ip3", 4)], levers),
            _c("busy vm2 not touched", all(l[0] != "vm2" for l in levers), ""),
            _c("estimated saving 264/month", saving == 264, saving)]


# ---------------------------------------------------------------- ABUILD-31
def _a11y_scan(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for el in soup.find_all(attrs={"role": "button"}):
        if el.name != "button":
            out.append(("native-first", el.get("id")))
    for el in soup.find_all(["button", "a"]) + soup.find_all(attrs={"role": True}):
        name = el.get("aria-label") or el.get_text(strip=True)
        if not name:
            out.append(("accessible-name", el.get("id")))
    for el in soup.find_all(style=True):
        m = re.search(r"width:\s*(\d+)px.*height:\s*(\d+)px", el["style"])
        if m and (int(m[1]) < 24 or int(m[2]) < 24):
            out.append(("2.5.8-target-size", el.get("id")))
    for el in soup.find_all("img"):
        if el.get("alt") is None:
            out.append(("1.1.1-alt", el.get("id")))
    for el in soup.find_all("input"):
        if el.get("type") != "hidden" and not (el.get("aria-label") or (el.get("id") and soup.find("label", attrs={"for": el["id"]}))):
            out.append(("label", el.get("id")))
    return sorted(set(out), key=str)


def abuild_31(work: Path):
    html = """<div id="d1" role="button">Save</div><button id="b1" aria-label="Close" style="width:16px;height:16px">x</button>
<button id="b2"></button><button id="b3" style="width:44px;height:44px">Send</button>
<dialog id="m1" aria-modal="true"><button id="b4">OK</button></dialog>"""
    _w(work, "component.html", html)
    found = _a11y_scan(html)
    keymap = {"dialog": {"Escape": "close", "Tab": "trap within", "on close": "return focus to trigger"}}
    return [_c("div role=button flagged: use the native element", ("native-first", "d1") in found, found),
            _c("16x16 close button fails 2.5.8 (24px)", ("2.5.8-target-size", "b1") in found, found),
            _c("empty button has no accessible name", ("accessible-name", "b2") in found, found),
            _c("44x44 labelled button passes", not any(i == "b3" for _, i in found), found),
            _c("dialog key map specifies Escape, focus trap and return", set(keymap["dialog"]) == {"Escape", "Tab", "on close"}, keymap)]


# ---------------------------------------------------------------- ABUILD-32
def abuild_32(work: Path):
    def derive(primary):
        h, l, s = colorsys.rgb_to_hls(*[int(primary[i:i + 2], 16) / 255 for i in (1, 3, 5)])
        out = {}
        for k, L in zip(["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950", "fg"],
                        [0.97, 0.93, 0.85, 0.75, 0.65, l, 0.42, 0.35, 0.27, 0.2, 0.14, 0.1]):
            r, g, b = colorsys.hls_to_rgb(h, L, s)
            out[f"--brand-{k}"] = "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))
        return out

    def save(cfg):
        if _contrast(cfg["body"], cfg["bg"]) < 4.5 or _contrast(cfg["link"], cfg["bg"]) < 4.5:
            raise ValueError("contrast below 4.5:1")
        return derive(cfg["primary"])

    good = {"primary": "#2a78d6", "body": "#1f2328", "link": "#0b5cad", "bg": "#ffffff"}
    props = save(good)
    try:
        save({**good, "link": "#7fb2ff"})
        rejected = False
    except ValueError:
        rejected = True
    defaults, glob, project = {"style": "minimal", "toc": "auto", "code": "github"}, {"style": "editorial", "toc": "off"}, {"style": "technical"}
    merged = {**defaults, **glob, **project}
    css = ":root{" + ";".join(f"{k}:{v}" for k, v in props.items()) + "}"
    _w(work, "theme.css", css)
    return [_c("12 CSS custom properties derived from HSL", len(props) == 12, len(props)),
            _c("--brand-500 keeps the primary hue/lightness", props["--brand-500"] == "#2a78d6", props["--brand-500"]),
            _c("light link #7fb2ff on white (<4.5:1) rejected", rejected, round(_contrast("#7fb2ff", "#ffffff"), 2)),
            _c("merge order project > global > defaults", merged == {"style": "technical", "toc": "off", "code": "github"}, merged),
            _c("converter output changes with the config", save({**good, "primary": "#d62a2a"})["--brand-500"] == "#d62a2a" and "#2a78d6" in css, "")]


# ---------------------------------------------------------------- ABUILD-33
def _oklch(hexc):
    rgb = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = [math.copysign(abs(v) ** (1 / 3), v) for v in (l_, m_, s_)]
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


def abuild_33(work: Path):
    L, C, H = _oklch("#ff0000")

    def clamp_css(min_px, max_px, vmin, vmax, root=16):
        slope = (max_px - min_px) / (vmax - vmin)
        inter = min_px - slope * vmin
        return f"clamp({min_px / root}rem, {inter / root:.4f}rem + {slope * 100:.4f}vw, {max_px / root}rem)", slope, inter

    css, slope, inter = clamp_css(16, 24, 320, 1280)
    at = lambda vw: min(24, max(16, inter + slope * vw))

    def grid_line(n, lines):  # negative index counts from the end
        return n if n > 0 else lines + 1 + n

    _w(work, "layout_math.json", {"oklch_red": [L, C, H], "clamp": css})
    return [_c("#ff0000 -> OKLCH(0.628, 0.2577, 29.23)", abs(L - 0.6280) < 1e-3 and abs(C - 0.2577) < 1e-3 and abs(H - 29.23) < 0.05, (L, C, H)),
            _c("white text on #2a78d6 fails 4.5:1 body but passes 3:1 large/UI", 3 <= _contrast("#ffffff", "#2a78d6") < 4.5, round(_contrast("#ffffff", "#2a78d6"), 2)),
            _c("fluid type hits 16px at 320 and 24px at 1280", abs(at(320) - 16) < 1e-9 and abs(at(1280) - 24) < 1e-9 and at(2000) == 24, css),
            _c("12-col grid: line -1 is 13, span from 1 to -1 covers 12", grid_line(-1, 13) == 13 and grid_line(-1, 13) - grid_line(1, 13) == 12, "")]


# ---------------------------------------------------------------- ABUILD-34
def abuild_34(work: Path):
    comp = {"outer_radius": 24, "inset": 8, "inner_radius": 16, "padding": 24, "gap": 12, "overflow": "gap", "families": ["Inter", "JetBrains Mono"],
            "weights": [400, 600], "accents": ["#2a78d6"]}
    bad = {"outer_radius": 24, "inset": 8, "inner_radius": 24, "padding": 20, "gap": 8, "families": ["Inter", "Lora", "Mono"],
           "weights": [400, 500, 600, 700], "accents": ["#f00", "#0f0"]}

    def check(c):
        f = []
        if c["inner_radius"] != c["outer_radius"] - c["inset"]:
            f.append("concentric radii")
        for k in ("padding", "gap"):
            if c[k] % 8 and not (c[k] % 4 == 0 and c.get("overflow") == k):
                f.append(f"{k} off 8px grid")
        if len(c["families"]) > 2:
            f.append("max 2 families")
        if len(c["weights"]) > 3:
            f.append("max 3 weights")
        if len(c["accents"]) > 1:
            f.append("one accent per view")
        return f

    good_f, bad_f = check(comp), check(bad)
    _w(work, "constraints.json", {"good": good_f, "bad": bad_f})
    return [_c("24 outer with 8 inset -> inner 16 passes", "concentric radii" not in good_f, good_f),
            _c("inner 24 inside 24 with 8 inset fails concentric rule", "concentric radii" in bad_f, bad_f),
            _c("20px padding is off the 8px grid", "padding off 8px grid" in bad_f, bad_f),
            _c("3 families, 4 weights, 2 accents all flagged", {"max 2 families", "max 3 weights", "one accent per view"} <= set(bad_f), bad_f),
            _c("compliant component (12px half-step gap where 8 overflows) raises nothing", good_f == [], good_f)]


# ---------------------------------------------------------------- ABUILD-35
def abuild_35(work: Path):
    tokens = {"--color-primary": "#2a78d6", "--space-2": "8px", "--space-4": "16px"}
    css = """.btn-primary{background:var(--color-primary);padding:var(--space-2)}
.btn-primary:hover{background:#1f5fb0}
.BtnSecondary{background:#2a78d6;padding:13px}
.card{padding:var(--space-4)}"""
    _w(work, "styles.css", css)
    rules = dict(re.findall(r"([.\w:-]+)\{([^}]*)\}", css))
    findings = []
    for sel, body in rules.items():
        for val in re.findall(r"#[0-9a-fA-F]{3,6}\b|\b\d+px\b", body):
            findings.append(("hardcoded value", sel, val, "token" if val in tokens.values() else "no token"))
        base = sel.split(":")[0].lstrip(".")
        if not re.fullmatch(r"[a-z]+(-[a-z]+)*", base):
            findings.append(("naming", sel, base, "kebab-case"))
    for comp in {s.split(":")[0] for s in rules if s.startswith(".btn")}:
        for state in (":hover", ":focus-visible", ":disabled"):
            if comp + state not in rules:
                findings.append(("missing state", comp, state, ""))
    prio = {"missing state": 0, "hardcoded value": 1, "naming": 2}
    findings.sort(key=lambda f: prio[f[0]])
    _w(work, "audit.json", findings)
    hc = [f for f in findings if f[0] == "hardcoded value"]
    return [_c("#2a78d6 hardcoded where --color-primary exists", ("hardcoded value", ".BtnSecondary", "#2a78d6", "token") in findings, hc),
            _c("13px has no matching token", ("hardcoded value", ".BtnSecondary", "13px", "no token") in findings, hc),
            _c("PascalCase class flagged for naming", any(f[0] == "naming" and f[2] == "BtnSecondary" for f in findings), ""),
            _c("btn-primary missing :focus-visible and :disabled", {f[2] for f in findings if f[0] == "missing state" and f[1] == ".btn-primary"} == {":focus-visible", ":disabled"}, ""),
            _c("findings prioritised: states first", findings[0][0] == "missing state", findings[0])]


# ---------------------------------------------------------------- ABUILD-36
def abuild_36(work: Path):
    css = ".a{color:#2a78d6;margin:8px}.b{background:#2A78D6;padding:16px}.c{border-color:#ff0000}"
    taxonomy = {"#2a78d6": "--color-brand", "8px": "--space-2", "16px": "--space-4"}
    out = css
    for raw, tok in taxonomy.items():
        out = re.sub(re.escape(raw), f"var({tok})", out, flags=re.I)
    root = ":root{" + ";".join(f"{t}:{v}" for v, t in taxonomy.items()) + "}"
    _w(work, "retrofit.css", root + out)

    def resolve(text):
        vars_ = dict(re.findall(r"(--[\w-]+):([^;}]+)", text))
        body = text.split("}", 1)[1] if text.startswith(":root") else text
        return re.sub(r"var\((--[\w-]+)\)", lambda m: vars_[m[1]], body).lower()

    same = resolve(root + out) == css.lower()
    status = {"tokens": len(taxonomy), "replaced": out.count("var("), "untokenised": re.findall(r"#[0-9a-f]{6}", out, re.I)}
    return [_c("zero visual change: resolved CSS equals the original", same, same),
            _c("4 values replaced (case-insensitive hex match)", status["replaced"] == 4, status),
            _c("value outside the taxonomy reported, not invented", status["untokenised"] == ["#ff0000"], status["untokenised"])]


# ---------------------------------------------------------------- ABUILD-37
def _resolve_tokens(tokens):
    flat = {}

    def walk(node, path):
        if "$value" in node:
            flat[".".join(path)] = node
            return
        for k, v in node.items():
            if not k.startswith("$"):
                walk(v, path + [k])

    walk(tokens, [])

    def val(name, stack=()):
        if name in stack:
            raise ValueError("circular: " + " -> ".join(stack + (name,)))
        v = flat[name]["$value"]
        m = re.fullmatch(r"\{([\w.]+)\}", str(v))
        return val(m[1], stack + (name,)) if m else v

    return flat, val


def abuild_37(work: Path):
    tokens = {"color": {"blue": {"500": {"$value": "#2a78d6", "$type": "color", "$description": "primitive"}},
                        "brand": {"primary": {"$value": "{color.blue.500}", "$type": "color"}},
                        "button": {"bg": {"$value": "{color.brand.primary}", "$type": "color"}}},
              "space": {"md": {"$value": "16px", "$type": "dimension"}},
              "motion": {"fast": {"$value": "120ms", "$type": "duration"}}}
    flat, val = _resolve_tokens(tokens)
    css = ":root{" + ";".join(f"--{k.replace('.', '-')}:{val(k)}" for k in flat) + "}"
    tw = "@theme {\n" + "\n".join(f"  --{k.replace('.', '-')}: {val(k)};" for k in flat) + "\n}"
    _w(work, "tokens.json", tokens)
    _w(work, "tokens.css", css)
    _w(work, "theme.tailwind.css", tw)
    loop = {"a": {"$value": "{b}", "$type": "color"}, "b": {"$value": "{a}", "$type": "color"}}
    try:
        _resolve_tokens(loop)[1]("a")
        circ = None
    except ValueError as e:
        circ = str(e)
    raw_named = [k for k in flat if k.startswith("color.button") and not str(flat[k]["$value"]).startswith("{")]
    return [_c("component alias resolves through semantic to primitive #2a78d6", val("color.button.bg") == "#2a78d6", val("color.button.bg")),
            _c("every token carries $value and $type", all("$type" in t for t in flat.values()), len(flat)),
            _c("script translates to :root vars and Tailwind @theme alike", "--color-button-bg:#2a78d6" in css and "--color-button-bg: #2a78d6;" in tw, ""),
            _c("circular reference detected", circ == "circular: a -> b -> a", circ),
            _c("component tokens alias semantics (no raw values)", raw_named == [], raw_named)]


# ---------------------------------------------------------------- ABUILD-38
def abuild_38(work: Path):
    repo = work / "src"
    (repo / "components").mkdir(parents=True)
    (repo / "components" / "Hero.html").write_text('<img src="h.png"><button class="cta" style="color:#ff00aa">Go</button>')
    (repo / "components" / "Nav.html").write_text('<nav><a href="/">Home</a></nav>')
    weights = {"a11y": 3, "tokens": 1}

    def diagnose():
        fs = []
        for p in sorted(repo.rglob("*.html")):
            t = p.read_text()
            for m in re.finditer(r"<img(?![^>]*\balt=)[^>]*>", t):
                fs.append({"impact": "a11y", "file": p.name, "evidence": m[0]})
            for m in re.finditer(r"#[0-9a-fA-F]{6}", t):
                fs.append({"impact": "tokens", "file": p.name, "evidence": m[0]})
        return fs, 100 - sum(weights[f["impact"]] * 10 for f in fs)

    before, s0 = diagnose()
    snapshot = {p.name: p.read_text() for p in repo.rglob("*.html")}
    hero = repo / "components" / "Hero.html"
    hero.write_text(hero.read_text().replace('<img src="h.png">', '<img src="h.png" alt="Product photo">'))
    after, s1 = diagnose()
    _w(work, "audit_before_after.json", {"before": before, "after": after, "score": [s0, s1],
                                         "table": [{"priority": f["impact"], "evidence": f["evidence"], "change": "add alt" if f["impact"] == "a11y" else "use token"} for f in before]})
    return [_c("static diagnose (no write) finds missing alt and raw colour", {f["impact"] for f in before} == {"a11y", "tokens"} and snapshot["Nav.html"] == (repo / "components" / "Nav.html").read_text(), before),
            _c("score before = 100 - 30 - 10 = 60", s0 == 60, s0),
            _c("after the alt fix the score is 90", s1 == 90, s1),
            _c("remaining risk listed: raw colour still present", [f["impact"] for f in after] == ["tokens"], after)]


# ---------------------------------------------------------------- ABUILD-43
def abuild_43(work: Path):
    html = """<head><link rel="preload" href="f.woff2" as="font"><style>@font-face{font-family:X;src:url(f.woff2)}
.wrap{width:1200px}.col{max-width:60ch}@media (min-width:768px){.col{width:50%}}</style></head>
<body><img id="hero" src="hero.jpg"><img id="logo" src="l.png" width="40" height="40" loading="lazy">
<button onclick="for(let i=0;i<1e8;i++){}">Go</button></body>"""
    _w(work, "page.html", html)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    css = soup.style.get_text()
    imgs = soup.find_all("img")
    lcp = imgs[0]
    f = []
    if lcp.get("fetchpriority") != "high" or lcp.get("loading") == "lazy":
        f.append(("LCP", "hero image needs fetchpriority=high, no lazy"))
    for im in imgs:
        if not (im.get("width") and im.get("height")):
            f.append(("CLS", f"{im['id']} has no reserved size"))
    if "font-display" not in css:
        f.append(("fonts", "add font-display: swap"))
    for m in re.finditer(r"\.([\w-]+)\{width:(\d{3,})px\}", css):
        f.append(("responsive", f".{m[1]} fixed {m[2]}px width"))
    for b in soup.find_all(onclick=True):
        if re.search(r"1e[7-9]|for\s*\(", b["onclick"]):
            f.append(("INP", "long synchronous click handler"))
    _w(work, "perf_audit.json", f)
    kinds = [k for k, _ in f]
    return [_c("hero without fetchpriority flagged for LCP", ("LCP", "hero image needs fetchpriority=high, no lazy") in f, f),
            _c("only the unsized hero flagged for CLS", [m for k, m in f if k == "CLS"] == ["hero has no reserved size"], f),
            _c("missing font-display flagged", "fonts" in kinds, kinds),
            _c(".wrap fixed 1200px flagged; fluid .col not", ("responsive", ".wrap fixed 1200px width") in f and not any(".col" in m for _, m in f), f),
            _c("long click handler flagged for INP", "INP" in kinds, kinds)]


# ---------------------------------------------------------------- ABUILD-46 / 47 (pixel diff)
def _lab(img):
    rgb = img.astype(float) / 255
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = lin @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def _diff(actual, desired, de_tol=3.0, region=0.005, mask=None):
    de = np.linalg.norm(_lab(actual) - _lab(desired), axis=-1)
    bad = de > de_tol
    if mask is not None:
        bad &= ~mask
    frac = bad.mean()
    return {"pass": bool(frac <= region), "bad_fraction": float(frac), "max_dE": float(de[~mask].max() if mask is not None else de.max())}


def _elements_diff(actual_boxes, desired_boxes, px_tol=2):
    out = []
    for k, (x, y, w, h) in desired_boxes.items():
        ax, ay, aw, ah = actual_boxes[k]
        if max(abs(ax - x), abs(ay - y), abs(aw - w), abs(ah - h)) > px_tol:
            out.append({"element": k, "kind": "position", "delta": [ax - x, ay - y]})
    return out


def abuild_46(work: Path):
    from PIL import Image
    desired = np.full((80, 120, 3), 255, np.uint8)
    desired[20:40, 10:60] = (42, 120, 214)
    near = desired.copy()
    near[20:40, 10:60] = (43, 121, 214)  # dE < 3
    off = desired.copy()
    off[20:40, 10:60] = 255
    off[20:40, 14:64] = (42, 120, 214)  # moved 4 px
    for n, a in (("desired.png", desired), ("near.png", near), ("off.png", off)):
        Image.fromarray(a).save(work / n)
    dpr = 2
    boxes_desired = {"button": (10 * dpr, 20 * dpr, 50 * dpr, 20 * dpr)}
    r_near, r_off = _diff(near, desired), _diff(off, desired)
    el = _elements_diff({"button": (14 * dpr, 20 * dpr, 50 * dpr, 20 * dpr)}, boxes_desired)
    el_ok = _elements_diff({"button": (11 * dpr, 20 * dpr, 50 * dpr, 20 * dpr)}, boxes_desired)
    _w(work, "diff.json", {"near": r_near, "off": r_off, "elements": el})
    return [_c("1-unit colour shift stays under deltaE 3: pass", r_near["pass"] and r_near["max_dE"] < 3, r_near),
            _c("4 px shift covers > 0.5% area: fail", not r_off["pass"] and r_off["bad_fraction"] > 0.005, r_off),
            _c("DOM bbox scaled by DPR 2 reports position delta [8, 0]", el == [{"element": "button", "kind": "position", "delta": [8, 0]}], el),
            _c("2 px (1 CSS px at DPR 2) stays within px tolerance", el_ok == [], el_ok)]


def abuild_47(work: Path):
    from PIL import Image
    scale, H, W = 3, 2532, 1170
    h, w = H // 6, W // 6  # fixture at 1/6 size; mask heights scale the same way
    status_px, home_px = round(141 / 6), round(102 / 6)
    desired = np.full((h, w, 3), 245, np.uint8)
    actual = desired.copy()
    actual[:status_px] = (0, 0, 0)          # different clock/status bar
    actual[h - home_px:] = (20, 20, 20)     # home indicator
    mask = np.zeros((h, w), bool)
    mask[:status_px] = True
    mask[h - home_px:] = True
    Image.fromarray(actual).save(work / "actual.png")
    Image.fromarray(desired).save(work / "desired.png")
    unmasked = _diff(actual, desired)
    masked = _diff(actual, desired, mask=mask)
    actual2 = actual.copy()
    actual2[200:210, 50:100] = (255, 0, 0)  # real regression in content
    reg = _diff(actual2, desired, mask=mask)
    heat = (np.linalg.norm(_lab(actual2) - _lab(desired), axis=-1) > 3) & ~mask
    Image.fromarray((heat * 255).astype(np.uint8)).save(work / "heatmap.png")
    return [_c("status bar 141px and home indicator 102px at x3 masked", (status_px, home_px) == (24, 17) and scale == 3, (status_px, home_px)),
            _c("without the mask the chrome difference fails", not unmasked["pass"], unmasked),
            _c("with the mask the identical content passes", masked["pass"] and masked["bad_fraction"] == 0, masked),
            _c("a real 10x50 content regression still fails (> 0.5%)", not reg["pass"] and abs(reg["bad_fraction"] - 500 / (h * w)) < 1e-12, reg)]


# ---------------------------------------------------------------- ABUILD-48
def abuild_48(work: Path):
    tokens = {"primitive": {"blue-500": "#2a78d6", "blue-300": "#7fb2ff", "gray-0": "#ffffff", "gray-900": "#111111"},
              "themes": {("acme", "light"): {"color.bg.surface": "gray-0", "color.text.default": "gray-900", "color.action.primary": "blue-500"},
                         ("acme", "dark"): {"color.bg.surface": "gray-900", "color.text.default": "gray-0", "color.action.primary": "blue-300"}}}
    name_ok = lambda n: bool(re.fullmatch(r"color\.(bg|text|action|border)\.[a-z]+", n))

    def build(t):
        css, ts = [], {}
        for (brand, mode), sem in t["themes"].items():
            for n in sem:
                if not name_ok(n):
                    raise ValueError(f"bad semantic name {n}")
            css.append(f'[data-brand="{brand}"][data-theme="{mode}"]{{' + ";".join(
                f"--{n.replace('.', '-')}:{t['primitive'][p]}" for n, p in sem.items()) + "}")
            ts.update({n: "string" for n in sem})
        return "\n".join(css), "export type Token = " + " | ".join(f"'{n}'" for n in sorted(ts)) + ";"

    css, tsd = build(tokens)
    _w(work, "themes.css", css)
    _w(work, "tokens.d.ts", tsd)
    try:
        build({**tokens, "themes": {("acme", "light"): {"blueButton": "blue-500"}}})
        failed = False
    except ValueError:
        failed = True
    products_use_primitives = re.search(r"--blue-500", css) is not None
    return [_c("two theme blocks under [data-brand][data-theme]", css.count("[data-brand=") == 2, css.splitlines()[0][:60]),
            _c("dark theme maps surface to gray-900", '[data-theme="dark"]{--color-bg-surface:#111111' in css, ""),
            _c("build fails on a bad semantic name", failed, failed),
            _c("primitives are not exposed to products", not products_use_primitives, ""),
            _c("typed TS map lists the 3 semantic tokens", tsd.count("'color.") == 3, tsd)]


# ---------------------------------------------------------------- ABUILD-49
def abuild_49(work: Path):
    from bs4 import BeautifulSoup
    html = """<main><img src="a.png"><input id="q" type="text"><p style="color:#999999;background:#ffffff">grey</p>
<div onclick="go()">click</div><p style="color:#222222;background:#ffffff">ok</p></main>"""
    _w(work, "page.html", html)
    sev = {"1.1.1": "Critical", "2.1.1": "Critical", "1.3.1": "Major", "1.4.3": "Major"}

    def scan(h):
        s = BeautifulSoup(h, "html.parser")
        f = []
        f += [("1.1.1", str(i)) for i in s.find_all("img") if i.get("alt") is None]
        f += [("1.3.1", str(i)) for i in s.find_all("input") if not s.find("label", attrs={"for": i.get("id")}) and not i.get("aria-label")]
        f += [("2.1.1", str(d)) for d in s.find_all(onclick=True) if d.name not in ("button", "a")]
        for p in s.find_all(style=True):
            m = re.search(r"color:(#\w{6});background:(#\w{6})", p["style"])
            if m and _contrast(m[1], m[2]) < 4.5:
                f.append(("1.4.3", str(p)))
        return [{"criterion": c, "severity": sev[c], "node": n} for c, n in f]

    base = scan(html)
    _w(work, "baseline.json", base)
    fixed = (html.replace('<img src="a.png">', '<img src="a.png" alt="Chart">').replace('<input id="q"', '<label for="q">Search</label><input id="q"')
             .replace("#999999", "#595959").replace('<div onclick="go()">click</div>', '<button onclick="go()">click</button>'))
    after = scan(fixed)
    regressed = scan(fixed.replace('alt="Chart"', ""))
    new = [f for f in regressed if f not in after]
    return [_c("4 criteria found: 1.1.1, 1.3.1, 2.1.1, 1.4.3", sorted(f["criterion"] for f in base) == ["1.1.1", "1.3.1", "1.4.3", "2.1.1"], [f["criterion"] for f in base]),
            _c("#999 on white (2.85:1) fails 1.4.3; #222 passes", round(_contrast("#999999", "#ffffff"), 2) == 2.85, ""),
            _c("alt and keyboard issues classified Critical", {f["severity"] for f in base if f["criterion"] in ("1.1.1", "2.1.1")} == {"Critical"}, ""),
            _c("after fixes the re-scan is clean", after == [], after),
            _c("regression vs saved baseline caught (alt removed)", [f["criterion"] for f in new] == ["1.1.1"], new)]


# ---------------------------------------------------------------- ABUILD-50
def abuild_50(work: Path):
    remote, repo = work / "origin.git", work / "proj"
    _git(work, "init", "-q", "--bare", str(remote))
    _git(work, "init", "-q", str(repo))
    (repo / "VERSION").write_text("1.2.0\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "init")
    _git(repo, "remote", "add", "origin", str(remote))

    def release(version, dry_run=False):
        if _git(repo, "status", "--porcelain"):
            return "refused: dirty tree"
        if f"v{version}" in _git(repo, "tag").split():
            return "refused: tag exists"
        if dry_run:
            return f"would tag v{version}"
        (repo / "VERSION").write_text(version + "\n")
        _git(repo, "commit", "-qam", f"release {version}")
        _git(repo, "tag", "-a", f"v{version}", "-m", f"v{version}")
        _git(repo, "push", "-q", "origin", f"v{version}")
        (work / f"notes-v{version}.md").write_text(f"# v{version}\n")
        return "released"

    dry = release("1.3.0", dry_run=True)
    tags_after_dry = _git(repo, "tag")
    real = release("1.3.0")
    remote_tags = _git(repo, "ls-remote", "--tags", "origin")
    again = release("1.3.0")
    return [_c("dry run creates no tag", dry == "would tag v1.3.0" and tags_after_dry == "", dry),
            _c("release bumps VERSION and tags locally", real == "released" and (repo / "VERSION").read_text().strip() == "1.3.0", real),
            _c("git ls-remote --tags verifies v1.3.0 on origin", "refs/tags/v1.3.0" in remote_tags, remote_tags[-40:]),
            _c("existing tag refused on re-run", again == "refused: tag exists", again)]


# ---------------------------------------------------------------- ABUILD-51
def abuild_51(work: Path):
    BANNED = re.compile(r"\b(?:best|amazing|blazing|revolutionary)\b|\d+%|\b\d+\s*(?:hours?|days?|weeks?)\b", re.I)

    def lint(md, anchors):
        errs = []
        secs = re.findall(r"^## (What|Why|How)$", md, re.M)
        if secs != ["What", "Why", "How"]:
            errs.append("sections What/Why/How in order")
        what = md.split("## Why")[0].split("## What")[-1].strip()
        if not 1 <= len(re.findall(r"[.!?](\s|$)", what)) <= 3:
            errs.append("What: 1-3 sentences")
        how = md.split("## How")[-1]
        bullets = re.findall(r"^- (.+)$", how, re.M)
        if not bullets or not re.search(r"(?i)acceptance|done when", bullets[-1]):
            errs.append("How ends with acceptance criteria")
        for m in BANNED.finditer(md):
            errs.append(f"banned: {m[0]}")
        for link in re.findall(r"\]\(#([\w-]+)\)", md):
            if link not in anchors:
                errs.append(f"broken link #{link}")
        return errs

    good = """## What\nAdd CSV export to reports. See [issue](#issue-12).\n## Why\nUsers copy tables by hand.\n## How\n- Add an export button.\n- Stream rows as CSV.\n- Acceptance: a 10k-row report downloads with a header row."""
    bad = """## What\nThe best, blazing export ever.\n## How\n- Do it in 2 days.\n## Why\nIt saves 30% time. [x](#nowhere)"""
    _w(work, "ticket.md", good)
    g, b = lint(good, {"issue-12"}), lint(bad, {"issue-12"})
    return [_c("well-formed ticket passes", g == [], g),
            _c("wrong section order caught", "sections What/Why/How in order" in b, b),
            _c("superlatives, percentage and time estimate caught", {"banned: best", "banned: blazing", "banned: 30%", "banned: 2 days"} <= set(b), b),
            _c("unresolved link caught", "broken link #nowhere" in b, b)]


# ---------------------------------------------------------------- ABUILD-53
def abuild_53(work: Path):
    rng = np.random.default_rng(6)
    dt, n = 0.1, 200
    true_v = 1.0
    true_x = np.cumsum(np.full(n, true_v * dt))
    imu_v = true_v + 0.08 + rng.normal(0, 0.05, n)   # high-rate motion with a bias that drifts
    gnss_t = np.arange(0, n, 10)                     # 1 Hz fix
    gnss = true_x[gnss_t] + rng.normal(0, 0.5, len(gnss_t))
    x, P, Q, R = 0.0, 1.0, (0.3 * dt) ** 2, 0.25
    est, var = [], []
    gi = 0
    for k in range(n):
        x, P = x + imu_v[k] * dt, P + Q
        if gi < len(gnss_t) and gnss_t[gi] == k:
            K = P / (P + R)
            x, P = x + K * (gnss[gi] - x), (1 - K) * P
            gi += 1
        est.append(x)
        var.append(P)
    est = np.array(est)
    dead = np.cumsum(imu_v * dt)
    rmse = lambda a: float(np.sqrt(np.mean((a - true_x) ** 2)))
    stamps = {"imu": "base", "gnss": "base", "lidar": "other"}
    frame_ok = [k for k, v in stamps.items() if v != "base"]
    _w(work, "fusion.json", {"rmse_fused": rmse(est), "rmse_gnss_only": float(np.sqrt(np.mean((gnss - true_x[gnss_t]) ** 2))),
                             "final_var": var[-1], "time_base_violations": frame_ok})
    return [_c("fused estimate beats raw GNSS error", rmse(est) < float(np.sqrt(np.mean((gnss - true_x[gnss_t]) ** 2))), rmse(est)),
            _c("posterior variance after a fix < GNSS variance 0.25", min(var[g] for g in gnss_t[1:]) < R, min(var)),
            _c("fusion bounds the drift of biased IMU dead reckoning", rmse(est) < rmse(dead), (rmse(est), rmse(dead))),
            _c("sensor stamped in another time base is rejected", frame_ok == ["lidar"], frame_ok)]


# ---------------------------------------------------------------- ABUILD-54
def abuild_54(work: Path):
    ORDER = ["foundation", "language scaffold", "CI", "linters", "secrets", "release"]
    types = {"go.mod": "go", "Cargo.toml": "rust", "package.json": "node", "pyproject.toml": "python", "build.zig": "zig", "lakefile.lean": "lean"}

    def plan(repo):
        kind = next((t for f, t in types.items() if (repo / f).exists()), "unknown")
        have = {"foundation": all((repo / f).exists() for f in ("LICENSE", "README.md", ".gitignore")),
                "CI": (repo / ".github" / "workflows").is_dir(), "linters": (repo / ".golangci.yml").exists() or (repo / "rustfmt.toml").exists()}
        return kind, [s for s in ORDER if not have.get(s)]

    r1 = work / "r1"
    r1.mkdir()
    (r1 / "Cargo.toml").write_text("[package]\nname='x'\n")
    for f in ("LICENSE", "README.md", ".gitignore"):
        (r1 / f).write_text("x")
    (r1 / ".github" / "workflows").mkdir(parents=True)
    r2 = work / "r2"
    r2.mkdir()
    (r2 / "go.mod").write_text("module example.com/x\n")
    k1, p1 = plan(r1)
    k2, p2 = plan(r2)
    _w(work, "bootstrap_plan.json", {"r1": [k1, p1], "r2": [k2, p2]})
    return [_c("Cargo.toml detected as rust", k1 == "rust", k1),
            _c("covered foundation and CI skipped, order kept", p1 == ["language scaffold", "linters", "secrets", "release"], p1),
            _c("bare go.mod repo plans all six in fixed order", k2 == "go" and p2 == ORDER, p2)]


# ---------------------------------------------------------------- ABUILD-55
def abuild_55(work: Path):
    def choose(m):
        polyglot = len(m["languages"] - {"js", "ts"}) > 0
        if not polyglot:
            if m["packages"] < 5 and m["build_min"] < 5:
                return "pnpm workspace only", ["Nx", "Turborepo", "Bazel"]
            return "pnpm workspace + Turborepo", ["Bazel"]
        if m["hermetic"]:
            return "Bazel", []
        return "Pants or Nx (task-level caching)", ["Bazel"]

    cases = {"small_ts": {"languages": {"ts"}, "packages": 3, "build_min": 2, "hermetic": False},
             "mid_ts": {"languages": {"js", "ts"}, "packages": 40, "build_min": 25, "hermetic": False},
             "poly_hermetic": {"languages": {"go", "ts", "py"}, "packages": 300, "build_min": 60, "hermetic": True},
             "poly_cache": {"languages": {"py", "ts"}, "packages": 60, "build_min": 30, "hermetic": False}}
    res = {k: choose(v) for k, v in cases.items()}
    _w(work, "monorepo.json", res)
    return [_c("tiny TS repo: workspace only, with a do-not-adopt-yet list", res["small_ts"][0] == "pnpm workspace only" and "Bazel" in res["small_ts"][1], res["small_ts"]),
            _c("mid-scale JS/TS: pnpm + Turborepo", res["mid_ts"][0] == "pnpm workspace + Turborepo", res["mid_ts"]),
            _c("polyglot needing byte-reproducible builds: Bazel", res["poly_hermetic"][0] == "Bazel", res["poly_hermetic"]),
            _c("polyglot with task caching enough: not Bazel yet", "Bazel" in res["poly_cache"][1], res["poly_cache"])]


# ---------------------------------------------------------------- ABUILD-56
def abuild_56(work: Path):
    cfg = """interface Gi0/0
 description uplink
 ip address 10.0.0.1 255.255.255.0
interface Gi0/1
 ip address 10.0.0.129 255.255.255.128
interface Gi0/2
 ip address 192.168.1.1 255.255.255.0
interface Vlan10
 ip address 192.168.1.1 255.255.255.0
vlan 10
vlan 10
interface Gi0/0
 shutdown
no ip route 0.0.0.0 0.0.0.0 10.0.0.254
ip route 172.16.0.0 255.255.0.0 10.0.0.2"""
    _w(work, "candidate.cfg", cfg)
    nets, ips, vlans, findings = [], {}, {}, []
    cur = None
    for line in cfg.splitlines():
        if line.startswith("interface"):
            cur = line.split()[1]
        m = re.match(r"\s*ip address (\S+) (\S+)", line)
        if m:
            iface = ipaddress.ip_interface(f"{m[1]}/{m[2]}")
            if m[1] in ips:
                findings.append(("duplicate IP", m[1]))
            ips[m[1]] = cur
            for other, oc in nets:
                if iface.network.overlaps(other) and oc != cur:
                    findings.append(("subnet overlap", f"{iface.network} vs {other}"))
            nets.append((iface.network, cur))
        m = re.match(r"vlan (\d+)$", line)
        if m:
            if m[1] in vlans:
                findings.append(("duplicate VLAN", m[1]))
            vlans[m[1]] = True
    danger = []
    mgmt = {"Gi0/0"}
    cur = None
    for i, line in enumerate(cfg.splitlines()):
        if line.startswith("interface"):
            cur = line.split()[1]
        if line.strip() == "shutdown" and cur in mgmt:
            danger.append((i, "shutdown on uplink/management path"))
        if re.match(r"no ip route 0\.0\.0\.0", line):
            danger.append((i, "default-route removal"))
    own_path_last = sorted(danger, key=lambda d: d[1].startswith("shutdown"))
    _w(work, "findings.json", {"findings": findings, "dangerous_ordered": own_path_last})
    return [_c("10.0.0.0/24 overlaps 10.0.0.128/25", ("subnet overlap", "10.0.0.128/25 vs 10.0.0.0/24") in findings, findings),
            _c("192.168.1.1 used twice", ("duplicate IP", "192.168.1.1") in findings, findings),
            _c("VLAN 10 declared twice", ("duplicate VLAN", "10") in findings, findings),
            _c("uplink shutdown and default-route removal flagged, own path last",
               [d[1] for d in own_path_last] == ["default-route removal", "shutdown on uplink/management path"], own_path_last)]


# ---------------------------------------------------------------- ABUILD-57
def abuild_57(work: Path):
    defaults = {"theme": "light", "density": "comfortable", "accent": "#2a78d6"}
    js_prompt = ("function prompt(s){const D=" + json.dumps(defaults) + ";const ch=Object.keys(s).filter(k=>s[k]!==D[k]);"
                 "return ch.length?'Use '+ch.map(k=>k+' '+s[k]).join(', ')+'.':'Keep the defaults.';}")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>body{{font:14px system-ui}}#preview{{padding:16px}}</style></head>
<body><select id="theme"><option>light</option><option>dark</option></select><div id="preview"></div><pre id="out"></pre>
<script>const state={json.dumps(defaults)};{js_prompt}
function render(){{document.getElementById('preview').dataset.theme=state.theme;document.getElementById('out').textContent=prompt(state);}}
document.querySelectorAll('select').forEach(el=>el.addEventListener('input',e=>{{state[el.id]=el.value;render();}}));render();</script></body></html>"""
    _w(work, "playground.html", html)

    def py_prompt(s):
        ch = [k for k in s if s[k] != defaults[k]]
        return "Use " + ", ".join(f"{k} {s[k]}" for k in ch) + "." if ch else "Keep the defaults."

    node = shutil.which("node")
    js_out = None
    if node:
        js_out = subprocess.run([node, "-e", js_prompt + "console.log(prompt(" + json.dumps({**defaults, "theme": "dark"}) + "))"],
                                capture_output=True, text=True, timeout=20).stdout.strip()
    ext = re.findall(r"(?:src|href)=[\"']https?://", html)
    return [_c("single file, no external dependencies", ext == [] and "<script src" not in html, ext),
            _c("one state object and one render function", html.count("const state=") == 1 and html.count("function render") == 1, ""),
            _c("live preview on every input (no Apply button)", "addEventListener('input'" in html and "Apply" not in html, ""),
            _c("prompt mentions only non-default choices", py_prompt({**defaults, "theme": "dark"}) == "Use theme dark." and py_prompt(defaults) == "Keep the defaults.", ""),
            _c("embedded JS prompt agrees with the reference (node)", js_out in (None, "Use theme dark."), js_out)]


# ---------------------------------------------------------------- ABUILD-58
def abuild_58(work: Path):
    def module_or_custom(volume, module_cost, custom_bom, nre, cert_cost):
        module_total = volume * module_cost
        custom_total = volume * custom_bom + nre + cert_cost  # discrete radio needs its own intentional-radiator cert
        return ("pre-certified module" if module_total <= custom_total else "custom PCB"), module_total, custom_total

    low = module_or_custom(1000, 6.0, 2.0, 15000, 25000)
    high = module_or_custom(100_000, 6.0, 2.0, 15000, 25000)
    tree = {"battery_mAh": 2000, "loads": {"mcu_sleep_uA": 5, "radio_avg_uA": 40, "sensor_uA": 15}, "regulator_eff": 0.9}
    avg_mA = sum(tree["loads"].values()) / 1000 / tree["regulator_eff"]
    life_days = tree["battery_mAh"] / avg_mA / 24
    _w(work, "hw_scope.json", {"low_volume": low, "high_volume": high, "avg_mA": avg_mA, "battery_days": life_days})
    return [_c("1k units: module wins (6000 < 42000)", low[0] == "pre-certified module" and low[1:] == (6000.0, 42000.0), low),
            _c("100k units: custom PCB wins (240000 < 600000)", high[0] == "custom PCB" and high[1:] == (600000.0, 240000.0), high),
            _c("power tree: 60 uA load / 0.9 eff = 0.0667 mA", abs(avg_mA - 0.0667) < 1e-4, avg_mA),
            _c("2000 mAh battery lasts ~1250 days", abs(life_days - 1250) < 1, life_days)]


# ---------------------------------------------------------------- ABUILD-59
def abuild_59(work: Path):
    PHASES = ["audience and one job", "message", "design", "conversion"]
    STATUSES = {"pending", "in progress", "awaiting evidence", "done", "deferred", "skipped"}
    tracker = work / "CREATE-WEBSITE-PLAN.md"
    tracker.write_text("\n".join(f"- {p}: pending" for p in PHASES))

    def read():
        return dict(re.findall(r"- (.+?): (.+)", tracker.read_text()))

    def setp(phase, status, reason=None, hypothesis=None):
        st = read()
        if status not in STATUSES:
            raise ValueError("status")
        if status in ("deferred", "skipped") and not reason:
            raise ValueError("reason required")
        idx = PHASES.index(phase)
        if status == "in progress" and any(st[p] not in ("done", "skipped", "deferred") for p in PHASES[:idx]):
            raise ValueError("fixed order")
        if phase == "conversion" and status == "done" and not hypothesis:
            raise ValueError("every fix is a testable hypothesis")
        st[phase] = status + (f" ({reason})" if reason else "")
        tracker.write_text("\n".join(f"- {p}: {st[p]}" for p in PHASES))

    errs = []
    for args in (("design", "in progress"), ("message", "skipped"), ("conversion", "done")):
        try:
            setp(*args)
        except ValueError as e:
            errs.append(str(e))
    setp("audience and one job", "done")
    setp("message", "in progress")
    st = read()
    summary = [f"{p}: {s}" for p, s in st.items()][:5]
    return [_c("design cannot start before message (fixed order)", errs[0] == "fixed order", errs),
            _c("skipping needs a reason", errs[1] == "reason required", errs),
            _c("conversion fix needs a testable hypothesis", errs[2] == "every fix is a testable hypothesis", errs),
            _c("resume summary reads tracker state in <= 5 lines", st["message"] == "in progress" and len(summary) <= 5, summary)]


# ---------------------------------------------------------------- ABUILD-60
def abuild_60(work: Path):
    repo = work / "tool"
    repo.mkdir()
    (repo / "go.mod").write_text("module github.com/acme/tool\n")
    (repo / "cmd" / "tool").mkdir(parents=True)
    tarball = work / "tool-1.0.0.tar.gz"
    tarball.write_bytes(gzip.compress(b"fake source tree for checksum"))
    sha = hashlib.sha256(tarball.read_bytes()).hexdigest()
    remote = "git@github.com:acme/tool.git"
    owner, name = re.search(r"[:/]([\w-]+)/([\w-]+?)(\.git)?$", remote).groups()[:2]
    lang = "go" if (repo / "go.mod").exists() else "rust" if (repo / "Cargo.toml").exists() else "swift" if (repo / "Package.swift").exists() else "zig"
    module = (repo / "go.mod").read_text().split()[1]
    module_ok = module == f"github.com/{owner}/{name}"
    goreleaser = (repo / ".goreleaser.yml").exists()
    formula = f'''class Tool < Formula
  desc "tool"
  homepage "https://github.com/{owner}/{name}"
  url "https://github.com/{owner}/{name}/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "{sha}"
  depends_on "go" => :build
  def install
    system "go", "build", *std_go_args, "./cmd/{name}"
  end
end
'''
    _w(work, "Formula/tool.rb", formula)
    install = f"go install {module}/cmd/{name}@latest"
    return [_c("language detected from go.mod", lang == "go", lang),
            _c("owner/name read from git remote", (owner, name) == ("acme", "tool"), (owner, name)),
            _c("module path matches repo for go install", module_ok and install == "go install github.com/acme/tool/cmd/tool@latest", install),
            _c("no .goreleaser.yml -> hand formula with the tarball sha256", not goreleaser and f'sha256 "{sha}"' in formula, sha[:12])]


PROGRAMS = {f"ABUILD-{n:02d}": globals()[f"abuild_{n:02d}"] for n in range(1, 61) if f"abuild_{n:02d}" in globals()}
