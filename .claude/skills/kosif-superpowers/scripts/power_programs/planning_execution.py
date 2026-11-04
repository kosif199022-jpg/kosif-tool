"""Programs for the planning-execution family (PLAN-02..14; PLAN-01 and PLAN-05 have code proofs run elsewhere)."""
from __future__ import annotations
import re
from ._mind_common import save, eq, truth, critical_path, topo_order, grid, has_cycle


def backcast_plan(end_state, precedes, today):
    chain = [end_state]
    while chain[-1] != today:
        nxt = precedes.get(chain[-1])
        if nxt is None:
            raise ValueError("chain does not reach today")
        chain.append(nxt)
    plan = list(reversed(chain))
    return [{"milestone": m, "done_test": f"evidence that '{m}' holds"} for m in plan]


def p02(work):
    pre = {"1000 subscribers": "weekly videos for 8 weeks", "weekly videos for 8 weeks": "template + 4 scripts",
           "template + 4 scripts": "channel set up", "channel set up": "today"}
    plan = backcast_plan("1000 subscribers", pre, "today")
    save(work, "backcast.json", plan)
    broken = False
    try:
        backcast_plan("1000 subscribers", {"1000 subscribers": "luck"}, "today")
    except ValueError:
        broken = True
    return [eq("first step is today", plan[0]["milestone"], "today"), eq("last is end state", plan[-1]["milestone"], "1000 subscribers"),
            truth("every milestone has a done-test", all(p["done_test"] for p in plan)), truth("gap in chain rejected", broken)]


ACTIVITY = re.compile(r"^(work on|research|look into|think about|explore)\b", re.I)


def wbs_check(tasks, max_hours=4):
    bad = []
    for t in tasks:
        if t["hours"] > max_hours:
            bad.append((t["name"], "over 4 h"))
        if ACTIVITY.match(t["name"]):
            bad.append((t["name"], "activity not deliverable"))
        if not t.get("done"):
            bad.append((t["name"], "no done-test"))
    return bad


def p03(work):
    tasks = [{"name": "storyboard PDF (8 frames)", "hours": 3, "done": "8 frames in PDF"},
             {"name": "work on music", "hours": 2, "done": "track chosen"},
             {"name": "rough cut MP4", "hours": 6, "done": "plays 60 s"},
             {"name": "caption SRT", "hours": 1, "done": ""}]
    bad = wbs_check(tasks)
    save(work, "wbs_check.json", bad)
    return [eq("violations", bad, [("work on music", "activity not deliverable"), ("rough cut MP4", "over 4 h"), ("caption SRT", "no done-test")]),
            eq("clean task passes", wbs_check(tasks[:1]), [])]


def p04(work):
    dur = {"script": 2, "voice": 1, "shoot": 3, "edit": 4, "music": 1, "deliver": 1}
    dep = {"voice": ["script"], "shoot": ["script"], "edit": ["shoot", "voice"], "music": ["script"], "deliver": ["edit", "music"]}
    total, path, ef, slack = critical_path(dur, dep)
    save(work, "critical_path.json", {"total": total, "path": path, "slack": slack})
    return [eq("longest path days", total, 10), eq("critical path", path, ["script", "shoot", "edit", "deliver"]),
            eq("music slack", slack["music"], 6), eq("voice slack", slack["voice"], 2)]


def thin_slice(spec):
    """Cut a request to the 2 s, one-screen, one-record slice."""
    return {"duration_s": min(2, spec["duration_s"]), "screens": spec["screens"][:1], "records": spec["records"][:1]}


def p06(work):
    spec = {"duration_s": 60, "screens": ["home", "list", "detail"], "records": list(range(500))}
    s = thin_slice(spec)
    save(work, "thin_slice.json", s)
    return [eq("2 s render", s["duration_s"], 2), eq("one screen", s["screens"], ["home"]), eq("one record", len(s["records"]), 1)]


DEFAULT_CAUSES = ["scope creep", "missing dependency", "underestimated effort", "unclear owner", "late feedback"]


def premortem(plan_causes):
    causes = list(dict.fromkeys(DEFAULT_CAUSES + plan_causes))
    return [{"cause": c, "warning": f"watch: {c}", "mitigation": f"guard: {c}"} for c in causes]


def p07(work):
    r = premortem(["render farm quota"])
    save(work, "premortem.json", r)
    return [eq("five defaults + one specific", len(r), 6), eq("starts from defaults", [x["cause"] for x in r[:5]], DEFAULT_CAUSES),
            truth("each has a signal", all(x["warning"] for x in r))]


def kill_eval(criteria, observed):
    out = []
    for c in criteria:
        v = observed[c["metric"]]
        hit = v < c["min"] if "min" in c else v > c["max"]
        out.append((c["metric"], "kill" if hit and c["action"] == "kill" else "pivot" if hit else "continue"))
    return out


def p08(work):
    crit = [{"metric": "signups_week4", "min": 100, "action": "kill"}, {"metric": "cac_usd", "max": 40, "action": "pivot"},
            {"metric": "nps", "min": 20, "action": "pivot"}]
    obs = {"signups_week4": 140, "cac_usd": 55, "nps": 31}
    r = kill_eval(crit, obs)
    save(work, "kill_pivot.json", r)
    return [eq("decisions", r, [("signups_week4", "continue"), ("cac_usd", "pivot"), ("nps", "continue")]),
            eq("kill fires below min", kill_eval(crit[:1], {"signups_week4": 50}), [("signups_week4", "kill")])]


def p09(work):
    scen = grid(("budget up", "budget cut"), ("algorithm favours short", "algorithm favours long"))
    moves = {"shorts only": [8, 6, 2, 1], "mixed library": [6, 5, 6, 5], "long only": [2, 1, 8, 6]}
    robust = max(moves, key=lambda m: (min(moves[m]), sum(moves[m])))
    save(work, "scenario_grid.json", {"scenarios": scen, "robust": robust})
    return [eq("2x2 grid", len(scen), 4), eq("robust move", robust, "mixed library"), eq("worst case of robust", min(moves[robust]), 5)]


def lanes(tasks):
    """Group tasks into parallel lanes by dependency depth (independent tasks share a lane)."""
    order = topo_order(tasks)
    depth = {}
    for t in order:
        depth[t] = 1 + max([depth[d] for d in tasks[t]] or [-1])
    out = {}
    for t, d in depth.items():
        out.setdefault(d, []).append(t)
    return [sorted(v) for _, v in sorted(out.items())]


BRIEF_FIELDS = ("goal", "context", "deliverable", "acceptance")


def p10(work):
    t = {"research fonts": [], "research music": [], "research stock": [], "assemble": ["research fonts", "research music", "research stock"], "qa": ["assemble"]}
    L = lanes(t)
    briefs = [{"goal": x, "context": "repo", "deliverable": f"{x}.md", "acceptance": "file exists"} for x in L[0]]
    save(work, "lanes.json", {"lanes": L, "briefs": briefs})
    return [eq("first lane parallel", L[0], ["research fonts", "research music", "research stock"]), eq("lanes", len(L), 3),
            truth("every brief has the 4 fields", all(all(b[f] for f in BRIEF_FIELDS) for b in briefs))]


META = ["goal still right?", "evidence for each claim?", "what was skipped?", "simpler path?", "coverage ledger complete?"]


def phase_review(ledger):
    missing = [k for k, v in ledger.items() if v is None]
    return {"questions": META, "uncovered": missing, "pass": not missing}


def p11(work):
    r = phase_review({"requirement 1": "test_a", "requirement 2": None, "requirement 3": "screenshot.png"})
    save(work, "phase_review.json", r)
    return [eq("uncovered requirement caught", r["uncovered"], ["requirement 2"]), truth("review blocks", not r["pass"]),
            eq("checklist size", len(r["questions"]), 5)]


def receipt(measured, spec):
    return {k: (measured.get(k), v, measured.get(k) == v) for k, v in spec.items()}


def p12(work):
    spec = {"width": 1080, "height": 1920, "fps": 30, "audio": "aac"}
    measured = {"width": 1080, "height": 1920, "fps": 25, "audio": "aac"}
    r = receipt(measured, spec)
    save(work, "TEST_REPORT.json", r)
    return [eq("failed field", [k for k, v in r.items() if not v[2]], ["fps"]), eq("passed fields", sum(v[2] for v in r.values()), 3)]


def spec_trace(spec):
    problems = []
    if not 5 <= len(spec["constitution"]) <= 9:
        problems.append("constitution size")
    for s in spec["stories"]:
        if "[NEEDS CLARIFICATION]" in s["text"]:
            problems.append(f"unclarified: {s['id']}")
    crit = {c for s in spec["stories"] for c in s["criteria"]}
    tasks = spec["tasks"]
    for c in sorted(crit):
        if not any(c in t["covers"] and t["kind"] == "test" for t in tasks):
            problems.append(f"no test for {c}")
    ids = [t["id"] for t in tasks]
    for t in tasks:
        if t["kind"] == "code":
            test = [x for x in tasks if x["kind"] == "test" and set(x["covers"]) & set(t["covers"])]
            if test and ids.index(test[0]["id"]) > ids.index(t["id"]):
                problems.append(f"code before test: {t['id']}")
        if not t["covers"]:
            problems.append(f"untraced task: {t['id']}")
    return problems


def p13(work):
    spec = {"constitution": ["tests first", "no secrets", "accessibility", "RTL", "offline"],
            "stories": [{"id": "US1", "text": "user exports MP4", "criteria": ["AC1", "AC2"]},
                        {"id": "US2", "text": "user picks font [NEEDS CLARIFICATION]", "criteria": ["AC3"]}],
            "tasks": [{"id": "T1", "kind": "test", "covers": ["AC1"]}, {"id": "T2", "kind": "code", "covers": ["AC1"]},
                      {"id": "T3", "kind": "code", "covers": ["AC2"]}, {"id": "T4", "kind": "test", "covers": ["AC2"]},
                      {"id": "T5", "kind": "test", "covers": ["AC3"]}, {"id": "T6", "kind": "code", "covers": []}]}
    p = spec_trace(spec)
    save(work, "spec_trace.json", p)
    return [eq("problems", p, ["unclarified: US2", "code before test: T3", "untraced task: T6"]),
            truth("AC1 is test-first", "code before test: T2" not in p)]


def tdd_cycle(task_minutes, steps):
    ok_size = all(2 <= m <= 5 for m in task_minutes)
    ok_order = all(s == ["red", "green", "refactor", "review"] for s in steps)
    return ok_size, ok_order


def p14(work):
    sizes = [3, 5, 2, 4]
    steps = [["red", "green", "refactor", "review"]] * 3 + [["green", "red", "refactor", "review"]]
    size_ok, order_ok = tdd_cycle(sizes, steps)
    save(work, "tdd.json", {"sizes": sizes, "steps": steps})
    return [truth("tasks 2-5 min", size_ok), truth("out-of-order cycle caught", not order_ok),
            truth("correct cycle accepted", tdd_cycle(sizes, steps[:3])[1]), truth("12-min task rejected", not tdd_cycle([12], steps[:1])[0])]


PROGRAMS = {"PLAN-02": p02, "PLAN-03": p03, "PLAN-04": p04, "PLAN-06": p06, "PLAN-07": p07, "PLAN-08": p08,
            "PLAN-09": p09, "PLAN-10": p10, "PLAN-11": p11, "PLAN-12": p12, "PLAN-13": p13, "PLAN-14": p14}
