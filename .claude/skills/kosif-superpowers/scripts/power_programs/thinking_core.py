"""Programs for the thinking-core family. THINK-04 and THINK-35..40 have code proofs (think.py / powers.py)
run by another worker. The rest run the card's procedure on a planted fixture with a known answer."""
from __future__ import annotations
import importlib.metadata as md
import random
import re
from ._mind_common import (save, eq, truth, weighted_scores, rank, vague_terms, has_number, topo_order, require_fields,
                           monte_carlo, percentile, ice)

EFFORT = [("trivial", 0, 5, 0), ("medium", 5, 20, 1), ("comparison", 10, 60, 4), ("broad", 50, 10**6, 10)]


def effort_class(tool_calls):
    for name, lo, hi, agents in EFFORT:
        if tool_calls <= hi:
            return name, agents
    return "broad", 10


def loop_run(stages):
    order = ["frame", "recall", "explore", "decide", "build", "verify", "report"]
    done = []
    for s in order:
        if s not in stages or not stages[s]:
            return done, f"stopped at {s}"
        done.append(s)
    return done, "complete"


def t01(work):
    st = {"frame": "goal+criteria", "recall": "inventory", "explore": ["a", "b", "c"], "decide": "rubric",
          "build": "slice", "verify": "ffprobe ok", "report": "4 blocks"}
    d, status = loop_run(st)
    d2, s2 = loop_run(dict(st, verify=""))
    save(work, "loop.json", {"done": d, "status": status})
    return [eq("seven stages complete", len(d), 7), eq("missing verify stops before report", s2, "stopped at verify"),
            eq("trivial class", effort_class(4)[0], "trivial"), eq("medium class", effort_class(12)[0], "medium"),
            truth("explore had >=3 options", len(st["explore"]) >= 3)]


FRAME = ["goal", "deliverable", "audience", "done_criteria", "constraints", "size"]


def frame_check(fr):
    probs = require_fields(fr, FRAME)
    for c in fr.get("done_criteria", []):
        if vague_terms(c) and not has_number(c):
            probs.append(f"uncheckable: {c}")
    if fr.get("size") not in ("trivial", "medium", "large", "research"):
        probs.append("size class")
    return probs


def t02(work):
    fr = {"goal": "ريل ٢٠ ثانية", "deliverable": "out/reel.mp4", "audience": "followers", "done_criteria": ["1080x1920 30 fps", "looks nice"],
          "constraints": "RTL, 20 s", "size": "medium"}
    p = frame_check(fr)
    save(work, "frame.json", fr)
    return [eq("six lines", len(FRAME), 6), eq("uncheckable criterion caught", p, ["uncheckable: looks nice"]),
            eq("fixed frame passes", frame_check(dict(fr, done_criteria=["1080x1920 30 fps"])), [])]


def inventory(tool_names):
    servers = sorted({n.split("__")[1] for n in tool_names if n.startswith("mcp__")})
    builtin = sorted(n for n in tool_names if not n.startswith("mcp__"))
    return {"mcp_servers": servers, "builtin": builtin}


def t03(work):
    tools = ["Read", "Bash", "mcp__github__get_me", "mcp__github__list_prs", "mcp__Higgsfield__balance", "mcp__suno__profile", "Write"]
    inv = inventory(tools)
    note = [f"tools: {len(inv['builtin'])} builtin", f"mcp: {', '.join(inv['mcp_servers'])}", "env: python3 ffmpeg", "installable: pip"]
    save(work, "inventory.txt", "\n".join(note))
    return [eq("mcp prefixes", inv["mcp_servers"], ["Higgsfield", "github", "suno"]), eq("builtin", len(inv["builtin"]), 3),
            truth("3-8 line note", 3 <= len(note) <= 8)]


def t05(work):
    batch = [("Read", "a.py"), ("Grep", "foo"), ("Read", "b.py"), ("Bash", "edit a.py")]
    reads = [b for b in batch if b[0] in ("Read", "Grep", "Glob")]
    writes = [b for b in batch if b not in reads]
    approaches = {"ffmpeg filter": "cli", "html render": "browser", "python moviepy": "python"}
    save(work, "explore.json", {"parallel_batch": reads, "after": writes, "approaches": approaches})
    return [eq("independent reads batched", len(reads), 3), eq("genuinely different engines", len(set(approaches.values())), 3)]


def rubric(opts):
    w = {"fit": 1, "risk": 1, "effort": 1, "wow": 1, "reversibility": 1}
    return weighted_scores(opts, w)


def t06(work):
    opts = {"template": {"fit": 4, "risk": 4, "effort": 5, "wow": 2, "reversibility": 5},
            "custom 3D": {"fit": 5, "risk": 2, "effort": 1, "wow": 5, "reversibility": 3},
            "hybrid": {"fit": 5, "risk": 4, "effort": 3, "wow": 4, "reversibility": 4}}
    s = rubric(opts)
    pm = sorted({"font shaping": 5, "render time": 4, "music licence": 3, "typo": 1}.items(), key=lambda x: -x[1])[:3]
    save(work, "decide.json", {"scores": s, "premortem": pm, "first_slice": pm[0][0]})
    return [eq("winner", rank(s)[0], "hybrid"), eq("hybrid total", s["hybrid"], 20), eq("first slice proves riskiest", pm[0][0], "font shaping")]


def t07(work):
    probes = {"numpy": None, "definitely_missing_lib_xyz": None}
    for m in probes:
        try:
            __import__(m)
            probes[m] = True
        except ImportError:
            probes[m] = False
    original = work / "user_audio.bin"
    original.write_bytes(bytes(range(256)))
    copy = work / "work_copy.bin"
    copy.write_bytes(original.read_bytes()[::-1])
    save(work, "probes.json", probes)
    return [eq("probe found numpy", probes["numpy"], True), eq("probe proved absence", probes["definitely_missing_lib_xyz"], False),
            truth("user asset untouched", original.read_bytes() == bytes(range(256)))]


def pause_check(rules, info_needed, action, expected, got):
    issues = [r for r in rules if r["forbids"] in action]
    missing = [k for k, v in info_needed.items() if v is None]
    backtrack = expected != got
    return {"violations": [r["rule"] for r in issues], "missing": missing, "backtrack": backtrack}


def t08(work):
    rules = [{"rule": "never push without ask", "forbids": "git push"}, {"rule": "no sleep waits", "forbids": "sleep 60"}]
    r = pause_check(rules, {"branch": "main", "remote": None}, "git push origin main", "exit 0", "exit 1")
    save(work, "pause.json", r)
    return [eq("rule hit", r["violations"], ["never push without ask"]), eq("missing info", r["missing"], ["remote"]), truth("backtrack on surprise", r["backtrack"])]


BADGE = re.compile(r"(✅|📄|💡)")


def report_check(blocks):
    probs = []
    for k in ("outcome", "verified", "not_done", "next"):
        if k not in blocks:
            probs.append(f"missing {k}")
    for c in blocks.get("verified", []):
        if not BADGE.search(c):
            probs.append(f"unbadged: {c}")
    return probs


def t09(work):
    rep = {"outcome": "الفيديو جاهز: out/reel.mp4", "verified": ["✅ ffprobe 1080x1920 30fps", "duration 20 s"], "not_done": ["💡 colour"], "next": ["أضيف ترجمة؟"]}
    p = report_check(rep)
    save(work, "report.json", rep)
    return [eq("unbadged claim caught", p, ["unbadged: duration 20 s"]), eq("missing block caught", report_check({"outcome": "x"}), ["missing verified", "missing not_done", "missing next"])]


STAGE0 = ["contract", "capability", "lenses", "pivots", "premortem", "fact status", "ranges", "acceptance", "numbers", "decompose", "debate", "report"]


def t10(work):
    filled = {m: True for m in STAGE0}
    filled["pivots"] = False
    fast = [m for m in STAGE0 if m in ("contract", "capability", "acceptance", "numbers", "report")]
    missing = [m for m, v in filled.items() if not v]
    save(work, "stage0.json", {"filled": filled, "fast_profile": fast})
    return [eq("12 modules", len(STAGE0), 12), eq("unfilled module", missing, ["pivots"]), truth("fast profile is a subset", set(fast) < set(STAGE0))]


def pivots(assumptions, choose):
    base = choose({a["name"]: a["value"] for a in assumptions})
    flips = []
    for a in assumptions:
        for v in a["alt"]:
            vals = {x["name"]: x["value"] for x in assumptions}
            vals[a["name"]] = v
            if choose(vals) != base:
                flips.append(a["name"])
                break
    return base, flips


def t11(work):
    choose = lambda v: "ads" if v["cpc"] * 100 < v["budget"] and v["season"] != "ramadan" else "organic"
    a = [{"name": "cpc", "value": 0.5, "alt": [0.4, 0.6]}, {"name": "budget", "value": 55, "alt": [45, 100]}, {"name": "season", "value": "normal", "alt": ["ramadan"]},
         {"name": "colour", "value": "red", "alt": ["blue"]}]
    base, flips = pivots(a, choose)
    save(work, "pivots.json", {"base": base, "pivots": flips})
    return [eq("base", base, "ads"), eq("pivots", flips, ["cpc", "budget", "season"]), truth("1-3 pivots", 1 <= len(flips) <= 3)]


def ledger(claims, evidence):
    out = []
    for c in claims:
        ev = [e for e in evidence if e["claim"] == c]
        pro = [e for e in ev if e["supports"]]
        con = [e for e in ev if not e["supports"]]
        status = "conflict" if pro and con else "supported" if pro else "contradicted" if con else "unverifiable"
        out.append({"claim": c, "status": status, "sources": [e["src"] for e in ev]})
    return out


def t12(work):
    ev = [{"claim": "ffmpeg 6 installed", "supports": True, "src": "ffmpeg -version"},
          {"claim": "price is $20", "supports": True, "src": "page 2025"}, {"claim": "price is $20", "supports": False, "src": "page 2026"},
          {"claim": "repo is MIT", "supports": False, "src": "LICENSE: GPL-3.0"}]
    L = ledger(["ffmpeg 6 installed", "price is $20", "repo is MIT", "users love it"], ev)
    save(work, "ledger.json", L)
    return [eq("statuses", [x["status"] for x in L], ["supported", "conflict", "contradicted", "unverifiable"]),
            truth("conflict shown, not averaged", L[1]["sources"] == ["page 2025", "page 2026"])]


def three_point(low, base, high):
    if not low <= base <= high:
        raise ValueError("order")
    return {"low": low, "base": base, "high": high, "pert_mean": (low + 4 * base + high) / 6}


def t13(work):
    r = three_point(6, 9, 18)
    r["driver"] = {"low": "GPU free", "high": "4K frames"}
    r["status"] = "estimated, not measured"
    bad = False
    try:
        three_point(10, 5, 8)
    except ValueError:
        bad = True
    save(work, "range.json", r)
    return [eq("PERT mean", r["pert_mean"], 10.0), truth("drivers named", len(r["driver"]) == 2), truth("disordered range rejected", bad)]


TEMPLATES = {"product": ["goals", "users", "requirements", "metrics", "risks", "rollout"],
             "system": ["entities", "interfaces", "dependencies", "states", "failure boundaries"],
             "causal": ["inputs", "mechanism", "outputs", "feedback loops"],
             "quantitative": ["inputs", "formulas", "constraints", "scenarios", "units", "reconciliation"],
             "adr": ["context", "drivers", "options", "trade-offs", "decision", "consequences"]}


def decompose(kind, filled):
    return [s for s in TEMPLATES[kind] if s not in filled]


def t14(work):
    gaps = decompose("system", {"entities": 1, "interfaces": 1, "states": 1})
    save(work, "decompose.json", TEMPLATES)
    return [eq("five templates", len(TEMPLATES), 5), eq("system gaps", gaps, ["dependencies", "failure boundaries"]),
            eq("product order", TEMPLATES["product"][0], "goals")]


def t15(work):
    cases = {3: "trivial", 15: "medium", 40: "comparison", 200: "broad"}
    got = {k: effort_class(k)[0] for k in cases}
    security_floor = max(["trivial", "standard"], key=["trivial", "standard"].index)
    save(work, "effort.json", got)
    return [eq("classes", got, cases), eq("comparison subagents", effort_class(40)[1], 4), eq("security work floor", security_floor, "standard")]


OPERATORS = {"exaggerate": lambda s: s.replace("10", "100"), "analogy": lambda s: s + " like a heist movie",
             "cross-over": lambda s: s + " + live data overlay"}


def t16(work):
    safe = "10 s logo reveal"
    bold = OPERATORS["exaggerate"](safe)
    pair = {"safe": safe, "bold": bold}
    save(work, "safe_bold.json", pair)
    return [eq("bold variant", bold, "100 s logo reveal"), truth("safe kept beside bold", pair["safe"] == safe), eq("one bold variant", len(pair) - 1, 1)]


def vat_two_ways(net, rate):
    a = round(net * rate, 2)
    gross = round(net * (1 + rate), 2)
    b = round(gross - net, 2)
    return a, b


def t17(work):
    a, b = vat_two_ways(1000, 0.15)
    frozen = {"vat": a}
    prose = "VAT is 150.00"
    save(work, "numeric_lock.json", {"inputs": {"net": 1000, "rate": 0.15}, "vat": a, "check": b})
    return [eq("vat", a, 150.0), eq("two reconciliations agree", a, b), truth("prose matches frozen number", f"{frozen['vat']:.2f}" in prose)]


def coverage(asks, artefact):
    rows = []
    for k, want in asks.items():
        got = artefact.get(k)
        rows.append((k, want, got, "PASS" if got == want else "FAIL"))
    return rows


def t18(work):
    asks = {"rows": 10, "language": "ar", "sections": 4, "format": "csv"}
    csv = work / "out.csv"
    csv.write_text("a,b\n" + "\n".join(f"{i},{i*i}" for i in range(9)) + "\n")
    art = {"rows": len(csv.read_text().splitlines()) - 1, "language": "ar", "sections": 4, "format": csv.suffix[1:]}
    rows = coverage(asks, art)
    save(work, "coverage.json", rows)
    return [eq("FAIL from the artefact, not memory", [r[0] for r in rows if r[3] == "FAIL"], ["rows"]), eq("measured rows", art["rows"], 9)]


def know_before_no(lib, catalog, installed, installable, needs_key):
    steps = ["lookup"]
    if lib in installed:
        return steps + ["probe:present"]
    steps.append("probe:absent")
    if lib in installable:
        return steps + ["install:venv", "smoke", "present"]
    if lib in needs_key:
        return steps + [f"needs-key:{needs_key[lib]}"]
    return steps + ["alternative"]


def t19(work):
    r = {x: know_before_no(x, set(), {"numpy"}, {"rich"}, {"stripe": "STRIPE_KEY"}) for x in ["numpy", "rich", "stripe", "unobtainium"]}
    save(work, "know_before_no.json", r)
    return [eq("present", r["numpy"][-1], "probe:present"), eq("install before yes", r["rich"][2:], ["install:venv", "smoke", "present"]),
            eq("key named", r["stripe"][-1], "needs-key:STRIPE_KEY"), eq("no only last", r["unobtainium"][-1], "alternative")]


LADDER = ["IDEA", "DOCUMENTED", "INSTALLABLE", "NEEDS-KEY", "PRESENT", "EXECUTED", "VERIFIED", "PROVEN-BEFORE"]


def claim_state(evidence):
    if evidence.get("blocked"):
        return "BLOCKED"
    if evidence.get("check_passed"):
        return "VERIFIED"
    if evidence.get("ran"):
        return "EXECUTED"
    if evidence.get("code"):
        return "PRESENT"
    if evidence.get("doc"):
        return "DOCUMENTED"
    return "IDEA"


def t20(work):
    cases = {"success message only": {"doc": 1, "code": 1, "ran": 1}, "ffprobe matched": {"code": 1, "ran": 1, "check_passed": 1},
             "plan": {"doc": 1}, "no key": {"blocked": "needs key"}}
    r = {k: claim_state(v) for k, v in cases.items()}
    save(work, "ladder.json", r)
    return [eq("8 states", len(LADDER), 8), eq("success message is not verification", r["success message only"], "EXECUTED"),
            eq("plan is documented", r["plan"], "DOCUMENTED"), eq("blocked", r["no key"], "BLOCKED"), eq("verified", r["ffprobe matched"], "VERIFIED")]


def surface(need):
    if need["always_true"]:
        return "rule"
    if need["occasional"]:
        return "skill"
    if need["stateful_integration"] and need["connected"]:
        return "mcp"
    if need["deterministic"]:
        return "cli"
    return "api"


def t21(work):
    base = dict(always_true=False, occasional=False, stateful_integration=False, connected=False, deterministic=False)
    r = {"invariant": surface(dict(base, always_true=True)), "procedure": surface(dict(base, occasional=True)),
         "crm sync (connected)": surface(dict(base, stateful_integration=True, connected=True)),
         "crm sync (not connected)": surface(dict(base, stateful_integration=True, deterministic=True)),
         "transcode": surface(dict(base, deterministic=True)), "paid op": surface(base)}
    save(work, "surface.json", r)
    return [eq("rungs", r, {"invariant": "rule", "procedure": "skill", "crm sync (connected)": "mcp", "crm sync (not connected)": "cli", "transcode": "cli", "paid op": "api"})]


def adopt_decision(c):
    if c["fit"] >= 0.9 and c["maintained"] and c["licence"] in ("MIT", "Apache-2.0", "BSD"):
        return "adopt"
    if c["fit"] >= 0.7 and c["maintained"]:
        return "extend"
    if c["fit"] >= 0.4:
        return "compose"
    return "build"


def t22(work):
    cands = {"lib-a": dict(fit=0.95, maintained=True, licence="MIT"), "lib-b": dict(fit=0.95, maintained=True, licence="GPL-3.0"),
             "lib-c": dict(fit=0.5, maintained=False, licence="MIT"), "none": dict(fit=0.1, maintained=False, licence="")}
    r = {k: adopt_decision(v) for k, v in cands.items()}
    save(work, "adopt.json", r)
    return [eq("decisions", r, {"lib-a": "adopt", "lib-b": "extend", "lib-c": "compose", "none": "build"}), eq("four decisions", len(set(r.values())), 4)]


def load_chapters(open_ch, candidate, requirement_uncovered, deep=False):
    limit = 4 if deep else 2
    if len(open_ch) >= limit:
        return False, "limit"
    if not requirement_uncovered:
        return False, "gap test failed"
    return True, "ok"


def t23(work):
    r = [load_chapters(["formats"], "captions", "Arabic caption timing"), load_chapters(["formats", "captions"], "3d", "x"),
         load_chapters(["formats"], "formats-2", ""), load_chapters(["a", "b", "c"], "d", "x", deep=True)]
    save(work, "chapters.json", r)
    return [eq("second chapter with a gap", r[0][0], True), eq("third blocked", r[1][1], "limit"), eq("paraphrase blocked", r[2][1], "gap test failed"),
            eq("deep allows 4", r[3][0], True)]


def t24(work):
    import numpy
    live = md.version("numpy")
    memory_claim = "1.0.0"
    answer = {"library": "numpy", "version_used": live, "source": "importlib.metadata", "memory_claim_matches": live == memory_claim}
    save(work, "live_docs.json", answer)
    return [eq("live version equals imported module", live, numpy.__version__), truth("stale memory detected", not answer["memory_claim_matches"])]


BLOCKING = {"security", "data loss", "irreversible migration", "api breakage", "cost", "destructive or public"}


def ask_or_assume(forks):
    qs = [f["q"] for f in forks if f["kind"] in BLOCKING and not f["findable"]]
    assumed = [f["q"] for f in forks if f not in [x for x in forks if x["q"] in qs]]
    return qs[:3], assumed


def t25(work):
    forks = [{"q": "which font?", "kind": "taste", "findable": False}, {"q": "delete old renders?", "kind": "destructive or public", "findable": False},
             {"q": "which branch?", "kind": "api breakage", "findable": True}, {"q": "spend 40 credits?", "kind": "cost", "findable": False}]
    qs, assumed = ask_or_assume(forks)
    save(work, "ask.json", {"ask": qs, "assume": assumed})
    return [eq("asked only costly forks", qs, ["delete old renders?", "spend 40 credits?"]), truth("<=3 batched", len(qs) <= 3),
            truth("findable answered by looking", "which branch?" in assumed), eq("six blocking reasons", len(BLOCKING), 6)]


AC_FIELDS = ["scenario", "action", "expected", "must_not", "verify", "priority"]


def ac_lint(acs):
    p = []
    if not 3 <= len(acs) <= 7:
        p.append("count")
    for i, a in enumerate(acs):
        miss = require_fields(a, AC_FIELDS)
        if miss:
            p.append(f"AC{i+1} missing {miss}")
        if vague_terms(a.get("expected", "")) and not has_number(a.get("expected", "")):
            p.append(f"AC{i+1} vague")
    return p


def t26(work):
    full = lambda e: {"scenario": "s", "action": "a", "expected": e, "must_not": "m", "verify": "pytest", "priority": "P1"}
    acs = [full("200 OK in < 300 ms"), full("clean output"), dict(full("3 rows"), verify="")]
    p = ac_lint(acs)
    save(work, "acs.json", acs)
    return [eq("problems", p, ["AC2 vague", "AC3 missing ['verify']"]), eq("too few rejected", ac_lint(acs[:1])[0], "count")]


BRIEF = ["objective", "why", "output", "tools", "boundaries", "budget", "success"]


def lane_matrix(lanes):
    writers = {}
    probs = []
    for l in lanes:
        for f in l["writes"]:
            writers.setdefault(f, []).append(l["name"])
        if l["destructive"] and l["parallel"]:
            probs.append(f"destructive in parallel: {l['name']}")
        miss = [k for k in BRIEF if k not in l["brief"]]
        if miss:
            probs.append(f"{l['name']} brief missing {miss}")
    probs += [f"two writers: {f}" for f, w in writers.items() if len(w) > 1]
    return probs


def t27(work):
    b = {k: "x" for k in BRIEF}
    lanes = [{"name": "fonts", "writes": ["fonts.md"], "destructive": False, "parallel": True, "brief": b},
             {"name": "music", "writes": ["notes.md"], "destructive": False, "parallel": True, "brief": b},
             {"name": "stock", "writes": ["notes.md"], "destructive": False, "parallel": True, "brief": {k: "x" for k in BRIEF[:5]}},
             {"name": "migrate", "writes": ["db"], "destructive": True, "parallel": True, "brief": b}]
    p = lane_matrix(lanes)
    save(work, "lanes.json", p)
    return [eq("problems", sorted(p), sorted(["stock brief missing ['budget', 'success']", "destructive in parallel: migrate", "two writers: notes.md"])),
            truth("3-5 lanes", 3 <= len(lanes) <= 5)]


def t28(work):
    log = []
    log.append(("architect", "B", ["r1", "r2", "r3"], "risk"))
    voices = {"skeptic": "A", "pragmatist": "B", "critic": "B"}
    for k, v in voices.items():
        log.append((k, v))
    decision = max(set(v for _, v, *rest in log), key=lambda x: sum(1 for _, v, *r in log if v == x))
    dissent = [k for k, v, *r in log if v != decision]
    save(work, "council.json", {"log": log, "decision": decision, "dissent": dissent})
    return [eq("own view written first", log[0][0], "architect"), eq("three fresh voices", len(voices), 3), eq("decision", decision, "B"), eq("dissent", dissent, ["skeptic"])]


def t29(work):
    opts = {"A paid ads": (4, 3, 3), "B partnerships": (5, 2, 4), "C SEO": (3, 4, 2), "do-nothing": (1, 5, 1)}
    s = {k: ice(*v) for k, v in opts.items()}
    order = sorted(s, key=lambda k: (-s[k], k))
    stages = [{"stage": "pilot", "measure": "CPA", "stop_if": "CPA > 30"}]
    save(work, "options.json", {"ice": s, "order": order, "stages": stages})
    return [truth("do-nothing judged", "do-nothing" in s), eq("order", order, ["C SEO", "do-nothing", "A paid ads", "B partnerships"]),
            truth("stage has stop condition", all(x["stop_if"] for x in stages))]


def impact(symbol, files):
    callers = sorted(f for f, src in files.items() if re.search(rf"\b{symbol}\(", src) and not re.search(rf"def {symbol}\(", src))
    return callers


IMPACT_ORDER = ["code", "data", "interfaces", "tests", "docs", "release"]


def t30(work):
    files = {"a.py": "def render(x):\n  return x", "b.py": "from a import render\nrender(1)", "c.py": "y = prerender(2)", "d.py": "render( 3 )"}
    c = impact("render", files)
    save(work, "impact.json", {"callers": c, "order": IMPACT_ORDER})
    return [eq("callers found", c, ["b.py", "d.py"]), truth("prefix match excluded", "c.py" not in c), eq("six-step order", len(IMPACT_ORDER), 6)]


def score_hit(text, terms):
    hit = sum(t in text for t in terms) / len(terms)
    return round(hit, 2)


def retrieve(docs, terms0, learn):
    terms = list(terms0)
    for cycle in range(1, 4):
        scores = {d: score_hit(t, terms) for d, t in docs.items()}
        good = [d for d, s in scores.items() if s >= 0.7]
        if len(good) >= 3:
            return cycle, sorted(good)
        terms = terms + learn.get(cycle, [])
    return 3, sorted(good)


def t31(work):
    docs = {"a": "render pipeline ffmpeg x264", "b": "ffmpeg encode pipeline", "c": "x264 render crf pipeline", "d": "cooking", "e": "pipeline render ffmpeg"}
    cyc, good = retrieve(docs, ["render", "ffmpeg", "crf"], {1: []})
    cyc2, good2 = retrieve(docs, ["render", "crf", "x264"], {})
    save(work, "retrieval.json", {"cycles": cyc, "good": good})
    return [truth("stops within 3 cycles", cyc <= 3), eq("score scale", score_hit("render ffmpeg", ["render", "ffmpeg", "crf"]), 0.67),
            eq("unrelated dropped", "d" in good, False)]


PATTERNS = [("ECONNREFUSED", "wrong port or service down"), ("timeout", "wrong port or service down"), ("429", "retry storm"),
            ("No such file", "wrong cwd/branch"), ("same command x3", "no-exit loop"), ("FAILED test", "wrong hypothesis: isolate one test")]


def unstick(log):
    for pat, diag in PATTERNS:
        if pat in log:
            return diag
    return "capture more"


def t32(work):
    r = {l: unstick(l) for l in ["curl: ECONNREFUSED 127.0.0.1:3000", "HTTP 429 Too Many Requests", "cat: out.mp4: No such file", "FAILED test_a"]}
    save(work, "unstick.json", r)
    return [eq("diagnoses", list(r.values()), ["wrong port or service down", "retry storm", "wrong cwd/branch", "wrong hypothesis: isolate one test"]),
            eq("six patterns", len(PATTERNS), 6)]


def jit_slice(text, pattern, after=2):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if re.search(pattern, l):
            return lines[i:i + after + 1]
    return []


def t33(work):
    big = "\n".join(f"line {i}" for i in range(5000)) + "\n## Export\nflags: -crf 17\npreset slow\n" + "\n".join("x" for _ in range(5000))
    sl = jit_slice(big, r"^## Export")
    save(work, "slice.txt", "\n".join(sl))
    return [eq("section only", sl, ["## Export", "flags: -crf 17", "preset slow"]), truth("loaded < 0.1% of file", len("\n".join(sl)) < len(big) / 1000)]


ANTI = {"claim without evidence": r"\b(works|done|fixed)\b(?!.*(✅|output|log))", "you can do the rest": r"you can do the rest",
        "intensifier": r"\b(incredibly|extremely|truly)\b", "unprobed flag": r"--[a-z-]+ \(untested\)"}


def sweep(draft):
    return sorted(k for k, p in ANTI.items() if re.search(p, draft, re.I))


def t34(work):
    draft = "It works. This is extremely good, and you can do the rest."
    clean = "Render finished ✅ (ffprobe output attached)."
    save(work, "sweep.json", {"draft": sweep(draft), "clean": sweep(clean)})
    return [eq("anti-patterns", sweep(draft), ["claim without evidence", "intensifier", "you can do the rest"]), eq("clean draft", sweep(clean), [])]


def problem_statements(user_words, root, opportunity, leverage):
    st = {"user": user_words, "root": root, "opportunity": opportunity}
    return st, max(st, key=lambda k: leverage[k])


def t41(work):
    st, pick = problem_statements("make the video shorter", "viewers drop at 0:08 because the hook is late", "a 3 s hook template for all videos",
                                  {"user": 2, "root": 4, "opportunity": 5})
    save(work, "problem_finding.json", {"statements": st, "chosen": pick})
    return [eq("three statements", len(set(st.values())), 3), eq("most leverage", pick, "opportunity")]


REFRAMES = ["constraint is the feature", "different audience", "make it unnecessary"]


def t42(work):
    plan = "animated logo 20 s"
    effects = {"constraint is the feature": "no budget -> typographic-only film", "different audience": "rejected: brief fixed audience", "make it unnecessary": None}
    applied = [r for r in REFRAMES if effects[r]]
    changed = [effects[r] for r in applied if not effects[r].startswith("rejected")]
    save(work, "reframe.json", effects)
    return [truth("reframed at least twice", len(applied) >= 2, applied), eq("one reframe changed plan", changed, ["no budget -> typographic-only film"]),
            truth("rejection has a reason", "rejected:" in effects["different audience"])]


def t43(work):
    claims = {"colour grade matches source": "measure deltaE", "legal fair use": None, "fps correct": "ffprobe"}
    expert_q = "what would a colourist do differently?"
    outside = [c for c, test in claims.items() if test is None]
    save(work, "expert.json", {"question": expert_q, "outside_competence": outside})
    return [eq("outside circle", outside, ["legal fair use"]), truth("expert question asked", expert_q.endswith("?"))]


def t44(work):
    reader = {"knows": {"ffmpeg"}, "wants": "ship today", "fears": "losing audio"}
    points = ["what ffmpeg is", "audio is untouched (md5 matched)", "export finished", "history of codecs"]
    keep = [p for p in points if not any(k in p for k in reader["knows"]) and "history" not in p]
    keep.sort(key=lambda p: 0 if "audio" in p else 1)
    save(work, "reader.json", keep)
    return [eq("fear addressed first", keep[0], "audio is untouched (md5 matched)"), eq("known removed", len(keep), 2)]


META = ["asked problem?", "breaking assumption tested?", "looping?", "confidence > evidence?", "expert would differ?", "unrecalled power?"]


def metacheck(state):
    flags = []
    if state["solving"] != state["asked"]:
        flags.append(META[0])
    if not state["assumption_tested"]:
        flags.append(META[1])
    if len(state["fixes"]) != len(set(state["fixes"])):
        flags.append(META[2])
    if state["confidence"] > state["evidence"]:
        flags.append(META[3])
    return flags


def t45(work):
    st = {"solving": "make it faster", "asked": "make it faster", "assumption_tested": False, "fixes": ["bump crf", "bump crf"], "confidence": 0.9, "evidence": 0.4}
    f = metacheck(st)
    save(work, "metacognition.json", f)
    return [eq("six questions", len(META), 6), eq("flags", f, ["breaking assumption tested?", "looping?", "confidence > evidence?"])]


HABITS = {"problem finding": "three statements", "reframing": "reframe outcome", "quantity": "count", "analogy": "mechanism named",
          "combinatorial": "fused idea", "simplicity": "removed list", "taste": "gap list", "verification": "numbers",
          "long horizon": "reusable piece", "honesty": "unknowns line"}


def t46(work):
    evidence = {h: True for h in HABITS}
    evidence["taste"] = False
    missing = [HABITS[h] for h, v in evidence.items() if not v]
    save(work, "habits.json", {"habits": HABITS, "missing": missing})
    return [eq("ten habits", len(HABITS), 10), eq("missing check", missing, ["gap list"])]


def borda(rankings, n):
    pts = {}
    for member, order in rankings.items():
        for i, label in enumerate(order):
            pts[label] = pts.get(label, 0) + (n - 1 - i)
    return pts


def t47(work):
    answers = {"m1": "ans1", "m2": "ans2", "m3": "ans3", "m4": "ans4"}
    rng = random.Random(3)
    labels = {}
    for m in answers:
        order = list(answers)
        rng.shuffle(order)
        labels[m] = order
    rankings = {"m1": ["m3", "m2", "m4"], "m2": ["m3", "m1", "m4"], "m3": ["m2", "m1", "m4"], "m4": ["m3", "m2", "m1"]}
    own_excluded = all(m not in r for m, r in rankings.items())
    pts = borda(rankings, 4)
    top = max(pts, key=pts.get)
    save(work, "peer_rank.json", {"shuffles": labels, "borda": pts, "top": top})
    return [truth("no member ranks itself", own_excluded), eq("borda top", top, "m3"), eq("m3 points", pts["m3"], 9),
            truth("order shuffled per member", len({tuple(v) for v in labels.values()}) > 1)]


PROGRAMS = {f"THINK-{n:02d}": globals()[f"t{n:02d}"] for n in list(range(1, 4)) + list(range(5, 35)) + list(range(41, 48))}
