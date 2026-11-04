"""skills part 6: catalog SKILL.md files turned into real programs with known-answer checks.

Each runner reads its skill's core procedure, applies it as a deterministic program to a fixture written in
the work folder, and measures the output against planted known answers. Every runner also measures the same
criterion on the untreated input (the negative control), which must fail. Engines: python stdlib, the real
jq / gofmt / go vet / go test / pnpm / vite binaries, TypeScript + React SSR, Vue 3.5 compiler-sfc + SSR,
vue-router 5 (memory history), zod 4 and node for a hand-built stdio MCP server inside an MCPB zip.
Skills that need macOS, Deno, an uninstalled package, the network or a live human dialogue are in GAPS.
"""
import ast
import html
import ipaddress
import json
import math
import os
import re
import shutil
import subprocess
import zipfile
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path

from _harness import card, check, fx

P = "skill:kosif-superpowers/vendor/kosif-atlas/skills/"
NM = Path("/opt/node22/lib/node_modules")
SLIDEV_NM = NM / "@slidev/cli/node_modules"
ZOD = NM / "hyperframes/node_modules/zod"


def K(suffix):
    return P + suffix


GAPS = {
    K("2688-build-macos-apps/10303-liquid-glass"): "macOS SwiftUI Liquid Glass: needs Xcode, the macOS 26 SDK and a visual run on a Mac; none exist on this Linux host",
    K("2688-build-macos-apps/10305-signing-entitlements"): "needs codesign, spctl and security on macOS to read a real signed bundle; Linux has none of them",
    K("2688-build-macos-apps/10308-telemetry"): "needs a macOS build of an app with OSLog Logger and `log stream` / Console.app to verify the event fired",
    K("2898-deno/11715-deno-frontend"): "the deno binary is not installed here and cannot be downloaded (no network)",
    K("2898-deno/11716-deno-sandbox"): "Deno Sandbox runs Firecracker microVMs on Deno Deploy: needs an online Deno Deploy account and token",
    K("2898-deno/11717-deno"): "the deno binary is not installed here and cannot be downloaded (no network)",
    K("2898-deno/11718-migrate-to-deno"): "each rung runs `deno install` / `deno run`; the deno binary is not installed and cannot be downloaded",
    K("2922-pinia/12131-pinia"): "the pinia package is not installed anywhere on this machine (Vue is, pinia is not) and npm has no network",
    K("2940-tanstack/12197-use-tanstack"): "its whole method is `npx @tanstack/intent@latest list/load`, which downloads from npm; no network and no @tanstack/intent here",
    K("2943-tsdown/12203-tsdown"): "the tsdown package is not installed and cannot be fetched from npm (no network)",
    K("2944-turborepo/12208-turborepo"): "turbo is not installed; the skill says the docs ship inside the installed turbo package, so nothing to read or run",
    K("2954-workflow-sdk/12247-migrating-to-workflow-sdk"): "the Workflow SDK package (`workflow`) is not installed, so migrated 'use workflow'/'use step' code cannot be run or verified",
    K("2959-dryforge/12437-ready"): "its deliverable is user-approved intent: an ELICIT dialogue with the human plus explicit approval of the 3-doc; a program cannot stand in for that",
    K("2882-pm-product-discovery/11642-brainstorm-ideas-existing"): "its core deliverable is generative ideation from PM / Designer / Engineer perspectives (judgment); ranking given ideas is covered by the prioritize-features runner",
    K("2650-programming-tasuke/10069-prefer-yq"): "the skill assumes mikefarah/yq (Go: strenv, -i keeping comments, -p=xml, eval-all); only kislyuk/yq (Python jq wrapper) is installed, whose syntax differs as the skill itself warns",
}


def jw(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def wt(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")
    return Path(path)


def node(wd, name, js, node_path=None, timeout=40):
    src = wt(Path(wd) / (name + ".cjs"), js)
    env = dict(os.environ)
    env["NODE_PATH"] = str(node_path or NM)
    done = subprocess.run(["node", str(src)], capture_output=True, text=True, timeout=timeout, cwd=str(wd),
                          env=env, stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("node failed: " + done.stderr[-500:])
    return json.loads(done.stdout.strip().splitlines()[-1])


def sh(cmd, cwd=None, env=None, timeout=60, ok=True, inp=None):
    e = dict(os.environ)
    e.update(env or {})
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(cwd) if cwd else None,
                          env=e, input=inp, stdin=None if inp is not None else subprocess.DEVNULL)
    if ok and done.returncode:
        raise RuntimeError("%s failed (%d): %s" % (cmd[0], done.returncode, (done.stderr or done.stdout)[-400:]))
    return done


# ---------------------------------------------------------------- 9332 resilient extraction and parsing
class _Meta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ld, self.meta, self.itemprop, self.data, self._cap, self._buf = [], {}, {}, {}, None, []
        self.in_ld = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_ld, self._buf = True, []
        if tag == "meta" and a.get("property"):
            self.meta[a["property"]] = a.get("content")
        if tag == "meta" and a.get("itemprop"):
            self.itemprop[a["itemprop"]] = a.get("content")
        elif a.get("itemprop"):
            self._cap = ("itemprop", a["itemprop"])
        for k, v in a.items():
            if k.startswith("data-field"):
                self._cap = ("data", v)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_ld:
            self.in_ld = False
            try:
                self.ld.append(json.loads("".join(self._buf)))
            except ValueError:
                pass
        self._cap = None

    def handle_data(self, d):
        if self.in_ld:
            self._buf.append(d)
        elif self._cap and d.strip():
            kind, name = self._cap
            (self.itemprop if kind == "itemprop" else self.data).setdefault(name, html.unescape(d.strip()))


def _price(s):
    if s is None:
        return None
    m = re.search(r"(\d[\d,]*\.?\d*)", str(s))
    return Decimal(m.group(1).replace(",", "")).quantize(Decimal("0.01")) if m else None


SCHEMA_9332 = {"name": str, "price": Decimal, "currency": str, "sku": str}


@card(K("2407-web-scraping-data-extraction/9332-resilient-extraction-and-parsing"))
def resilient_extraction(task, wd):
    pages = {
        "p1_jsonld.html": '<html><head><script type="application/ld+json">{"@type":"Product","name":" Kettle  ","sku":"K-1",'
                          '"offers":{"price":"1,299.00","priceCurrency":"USD"}}</script></head><body><div class="x9f3a"><div>'
                          '<div>junk</div><div>Wrong 5.00</div></div></div></body></html>',
        "p2_microdata.html": '<html><body><div itemscope itemtype="https://schema.org/Product"><h1 itemprop="name">Toaster &amp; Grill</h1>'
                             '<meta itemprop="sku" content="T-2"><span itemprop="price">49.90</span>'
                             '<meta itemprop="priceCurrency" content="EUR"></div></body></html>',
        "p3_og_data.html": '<html><head><meta property="og:title" content="Blender"><meta property="product:price:amount" content="89">'
                           '<meta property="product:price:currency" content="GBP"></head><body><b data-field="sku">B-3</b></body></html>',
        "p4_redesign.html": '<html><head><script type="application/ld+json">{"@type":"Product","name":"Mixer","sku":"M-4",'
                            '"offers":{"price":"15.5","priceCurrency":"USD"}}</script></head><body><main class="css-1q2w3e">'
                            '<section><article><p>Mixer</p></article></section></main></body></html>',
        "p5_broken.html": '<html><head><meta property="og:title" content="Ghost item"></head><body><p>sold out</p></body></html>',
    }
    for n, t in pages.items():
        wt(wd / "pages" / n, t)

    def extract(text):
        p = _Meta()
        p.feed(text)
        ld = next((x for x in p.ld if x.get("@type") == "Product"), {})
        offers = ld.get("offers") or {}
        tiers = {
            "name": [ld.get("name"), p.itemprop.get("name"), p.meta.get("og:title")],
            "price": [offers.get("price"), p.itemprop.get("price"), p.meta.get("product:price:amount")],
            "currency": [offers.get("priceCurrency"), p.itemprop.get("priceCurrency"), p.meta.get("product:price:currency")],
            "sku": [ld.get("sku"), p.itemprop.get("sku"), p.data.get("sku")],
        }
        rec, src = {}, {}
        for f, opts in tiers.items():
            for i, v in enumerate(opts):
                if v not in (None, ""):
                    rec[f], src[f] = v, i
                    break
        if "name" in rec:
            rec["name"] = " ".join(str(rec["name"]).split())
        if "price" in rec:
            rec["price"] = _price(rec["price"])
        return rec, src

    def validate(rec):
        errs = [f for f, t in SCHEMA_9332.items() if not isinstance(rec.get(f), t)]
        if isinstance(rec.get("price"), Decimal) and rec["price"] <= 0:
            errs.append("price<=0")
        return errs

    good, quarantine = [], []
    for n in sorted(pages):
        rec, src = extract(pages[n])
        errs = validate(rec)
        (quarantine if errs else good).append({"page": n, "errors": errs, "tiers": src,
                                               **{k: str(v) for k, v in rec.items()}})
    fail_rate = len(quarantine) / len(pages)
    run = {"records": good, "quarantine": quarantine, "validation_failure_rate": fail_rate, "alert": fail_rate > 0.05}
    out = jw(wd / "extraction_run.json", run)
    want = {("Kettle", "1299.00", "USD", "K-1"), ("Toaster & Grill", "49.90", "EUR", "T-2"),
            ("Blender", "89.00", "GBP", "B-3"), ("Mixer", "15.50", "USD", "M-4")}
    got = {(r["name"], r["price"], r["currency"], r["sku"]) for r in good}

    # negative control: the brittle positional selector ("second div inside the first div of body") on the same pages
    def positional(text):
        m = re.search(r"<body><div[^>]*><div><div>[^<]*</div><div>([^<]*)</div>", text)
        return m.group(1) if m else None
    naive = {n: positional(t) for n, t in pages.items()}
    naive_ok = sum(1 for n, v in naive.items() if v and v.startswith(("Kettle", "Toaster", "Blender", "Mixer")))
    return [
        check("4 valid records extracted exactly (normalized names, Decimal prices, currency, sku)", got == want, sorted(got), sorted(want)),
        check("broken page quarantined, not written", [q["page"] for q in quarantine] == ["p5_broken.html"],
              [q["page"] for q in quarantine], ["p5_broken.html"]),
        check("fallback tiers used: JSON-LD, microdata, OG/data-*", sorted({r["tiers"]["name"] for r in good}) == [0, 1, 2],
              sorted({r["tiers"]["name"] for r in good}), [0, 1, 2]),
        check("failure-rate alert fires at 20% > 5%", run["alert"] and abs(fail_rate - 0.2) < 1e-9, fail_rate, 0.2),
        check("negative control: positional selector recovers 0 of 4 records", naive_ok == 0, naive_ok, 0),
    ], [out]


# ---------------------------------------------------------------- 780 plan for dummies
VAGUE = ["appropriately", "as needed", "etc.", "similar to", "clean up", "handle edge cases", "best practices",
         "follow the existing pattern", "tbd", "consider", "decide whether", "might", "could"]


def lint_plan(text):
    low = text.lower()
    lines = text.splitlines()
    issues = []
    for w in VAGUE:
        for m in re.finditer(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
            issues.append("vague:" + w)
    if re.search(r"\bline \d+|:\d+\b|\bL\d+\b", text):
        issues.append("line-number reference")
    if re.search(r"Docs:.*\d+\.(x|\*)", text) or re.search(r"\d+\.\d+\.x\b", text):
        issues.append("inexact docs version")
    for sec in ("## Done when", "## Report back"):
        if sec not in text:
            issues.append("missing " + sec)
    cps = len(re.findall(r"Checkpoint:", text))
    if not 2 <= cps <= 4:
        issues.append("checkpoints=%d" % cps)
    if len(lines) > 100:
        issues.append("over 100 lines")
    if re.search(r"^\s*(def |function |\{\s*$)", text, re.M):
        issues.append("function body")
    return issues


@card(K("243-plan-for-dummies/780-plan-for-dummies"))
def plan_for_dummies(task, wd):
    spec = {"title": "Rate-limit uploads", "goal": "Uploads over 10 per minute per user return HTTP 429.",
            "read_first": [["src/api/upload.py", "upload_handler", "the handler to wrap"],
                           ["src/api/search.py", "rate_limited", "the decorator to mirror"]],
            "docs": ["limits", "3.13.0", "RateLimitItemPerMinute", 2],
            "decisions": [["upload_rate_limit_per_min", "10", "matches the search endpoint"]],
            "stop_if": ["`search_handler` does not use `@rate_limited`"],
            "steps": [["Add `upload_rate_limit_per_min: int = 10` to `Settings` in `src/settings.py`.", None, None],
                      ["Decorate `upload_handler` with `@rate_limited(settings.upload_rate_limit_per_min)`.",
                       "putting the decorator below `@router.post` so it never runs",
                       ["pytest tests/test_upload.py -q", "baseline: not measured — record yours before editing"]],
                      ["Add `test_upload_429_after_limit` to `tests/test_upload.py`.", None,
                       ["pytest tests/test_upload.py -q", "1 new test passes"]]],
            "done": [["pytest -q", "all tests pass"]], "files": ["src/settings.py", "src/api/upload.py", "tests/test_upload.py"]}
    L = ["# Plan: " + spec["title"], "", "## Goal", spec["goal"], "", "## Read first"]
    L += ["- `%s` — `%s`, %s." % tuple(r) for r in spec["read_first"]]
    L += ["- Docs: %s %s — `%s`. Read before step %d." % tuple(spec["docs"]), "", "## Decisions"]
    L += ["- `%s` = %s, because it %s." % tuple(d) for d in spec["decisions"]]
    L += ["", "## Stop if"] + ["- " + s for s in spec["stop_if"]] + ["", "## Steps"]
    for i, (s, watch, cp) in enumerate(spec["steps"], 1):
        L.append("%d. %s" % (i, s))
        if watch:
            L.append("   Watch out: " + watch + ".")
        if cp:
            L.append("   Checkpoint: `%s` → `%s`" % tuple(cp))
    L += ["", "## Done when"] + ["- `%s` → `%s`" % tuple(d) for d in spec["done"]]
    L += ["- Only these files changed: " + ", ".join(spec["files"]), "", "## Report back",
          "Files changed / commands run with pasted output / deviations / unsure about."]
    plan = "\n".join(L) + "\n"
    out = wt(wd / "PLAN.md", plan)
    lint = lint_plan(plan)
    selfplan = ("# Plan\nFollow the existing pattern in upload.py around line 120 and handle errors appropriately.\n"
                "Add tests as needed, etc. Docs: limits 3.x\nWe might consider a config flag.\n")
    bad = lint_plan(selfplan)
    jw(wd / "lint.json", {"plan": lint, "self_plan": bad})
    planted = {"vague:follow the existing pattern", "vague:appropriately", "vague:as needed", "vague:etc.",
               "vague:might", "vague:consider", "line-number reference", "inexact docs version",
               "missing ## Done when", "missing ## Report back", "checkpoints=0"}
    return [
        check("generated plan passes every writing rule", lint == [], lint, []),
        check("plan under the ~50-line budget", len(plan.splitlines()) <= 50, len(plan.splitlines()), "<=50"),
        check("every introduced symbol has a literal signature", "`upload_rate_limit_per_min: int = 10`" in plan, True, True),
        check("negative control: a compressed plan-for-yourself trips exactly the planted rules", set(bad) == planted,
              sorted(bad), sorted(planted)),
    ], [out]


# ---------------------------------------------------------------- 9418 pick for the problem
RUNG = {"native": 1, "official": 2, "third-party": 3}
SINS = {"habit": r"\b(i always|we always|my go-to|muscle memory)\b", "availability": r"\b(already (installed|at hand)|handy)\b",
        "incumbency": r"\b(the repo already uses|we already use|existing code uses)\b",
        "preconception": r"\b(i knew|obviously|of course it'?s)\b"}


def pick(problem, candidates):
    need = set(problem["requirements"]) | set(problem["plausible_future"])
    rows = []
    for c in candidates:
        miss = sorted(need - set(c["covers"]))
        coupling = None
        if c["rung"] == "third-party":
            keys = ("maintained", "license", "security", "exit_cost")
            coupling = {k: c.get(k) for k in keys}
            if not all(c.get(k) for k in keys[:3]) or c.get("license") not in ("MIT", "BSD-3-Clause", "Apache-2.0"):
                miss.append("coupling not acceptable")
        rows.append({"name": c["name"], "rung": c["rung"], "missing": miss, "coupling": coupling})
    ok = sorted([r for r in rows if not r["missing"]], key=lambda r: RUNG[r["rung"]])
    return (ok[0]["name"] if ok else None), rows


@card(K("2431-discipline/9418-pick-for-the-problem"))
def pick_for_problem(task, wd):
    problem = {"problem": "parse ISO-8601 timestamps with offsets from a log file and compare them",
               "requirements": ["parse-iso8601", "tz-offsets", "compare"], "plausible_future": ["no-new-dependency-in-cli"]}
    cands = [
        {"name": "datetime.fromisoformat (stdlib)", "rung": "native", "covers": ["parse-iso8601", "tz-offsets", "compare", "no-new-dependency-in-cli"]},
        {"name": "dateutil.parser", "rung": "third-party", "covers": ["parse-iso8601", "tz-offsets", "compare"],
         "maintained": True, "license": "Apache-2.0", "security": "no open advisories (not checked live)", "exit_cost": "low"},
        {"name": "arrow", "rung": "third-party", "covers": ["parse-iso8601", "tz-offsets", "compare"], "maintained": True,
         "license": "Apache-2.0", "security": None},
        {"name": "hand-written regex parser", "rung": "native", "covers": ["parse-iso8601", "compare"]},
    ]
    choice, rows = pick(problem, cands)
    # live check that the native rung really covers the requirements on real input
    from datetime import datetime
    a = datetime.fromisoformat("2026-11-03T10:00:00+02:00")
    b = datetime.fromisoformat("2026-11-03T08:30:00+00:00")
    native_ok = a < b and (b - a).total_seconds() == 1800
    in_flight = {"choice": "arrow", "why": "I always use arrow for dates and the repo already uses it"}
    sins = sorted(s for s, rx in SINS.items() if re.search(rx, in_flight["why"], re.I))
    hand_built = [r["name"] for r in rows if r["name"].startswith("hand-written") and r["missing"]]
    rep = jw(wd / "selection.json", {"problem": problem, "survey": rows, "choice": choice,
                                     "basis": "judgment (local, reversible); maintenance/security not researched live",
                                     "audit_in_flight": {"choice": in_flight, "sins": sins}, "hand_built_rejected": hand_built})
    neg_choice, _ = pick(problem, [c for c in cands if c["name"] == "arrow"])
    return [
        check("ladder picks the native rung that covers today's and future requirements", choice == cands[0]["name"], choice, cands[0]["name"]),
        check("native option measured on real input (offset-aware compare, 1800 s)", native_ok, native_ok, True),
        check("habit + incumbency sins detected in the in-flight choice", sins == ["habit", "incumbency"], sins, ["habit", "incumbency"]),
        check("hand-built parser rejected as building what exists (misses tz-offsets)", hand_built == ["hand-written regex parser"], hand_built, ["hand-written regex parser"]),
        check("negative control: the reflex pick (arrow, no security weighing) does not pass the ladder", neg_choice is None, neg_choice, None),
    ], [rep]


# ---------------------------------------------------------------- 9420 reason, don't recite (detect half)
INCUMBENT = r"(that'?s how (this repo|we|it)|always been|the existing code does|it just is|we'?ve always|because it'?s there|legacy says|match(es)? the existing)"
PURPOSE = r"(so that|to prevent|in order to|required by|ensures?|because .*(fail|break|leak|cost|latency|security|spec)|guarantees?)"


def recite_audit(records):
    out = []
    for r in records:
        inc = bool(re.search(INCUMBENT, r["why"], re.I))
        pur = bool(re.search(PURPOSE, r["why"], re.I))
        out.append({"id": r["id"], "incumbency_only": inc and not pur, "names_purpose": pur,
                    "status": "candidate: re-derive from purpose (verdict stays judgment)" if inc and not pur else "live rationale or no precedent claim"})
    return out


@card(K("2431-discipline/9420-reason-dont-recite"))
def reason_dont_recite(task, wd):
    recs = [
        {"id": "D1", "rule": "all timestamps stored in UTC", "why": "in order to compare events across regions without DST bugs"},
        {"id": "D2", "rule": "services talk through a shared DB table", "why": "that's how this repo does it, it has always been like this"},
        {"id": "D3", "rule": "migrations are reviewed by two people", "why": "required by the SOC2 change-management control"},
        {"id": "D4", "rule": "config lives in an XML file", "why": "the existing code does it, so match the existing style"},
        {"id": "D5", "rule": "retry 3 times", "why": "we've always used 3, and it ensures transient 503s from the upstream do not fail the job"},
    ]
    res = recite_audit(recs)
    flagged = [r["id"] for r in res if r["incumbency_only"]]
    naive = [r["id"] for r in recs if re.search(INCUMBENT, r["why"], re.I)]
    out = jw(wd / "recite_audit.json", {"records": recs, "audit": res, "note": "flags are candidates; confirming or challenging is reasoning"})
    return [
        check("decisions coasting only on precedent are flagged", flagged == ["D2", "D4"], flagged, ["D2", "D4"]),
        check("precedent plus a live purpose (D5) is not flagged", "D5" not in flagged, "D5" in flagged, False),
        check("negative control: a precedent-keyword match without the purpose test mis-flags D5",
              naive != ["D2", "D4"] and "D5" in naive, naive, ["D2", "D4"]),
    ], [out]


# ---------------------------------------------------------------- 9424 script the deterministic work
@card(K("2431-discipline/9424-script-the-deterministic-work"))
def script_deterministic(task, wd):
    import random
    rnd = random.Random(9424)
    files = {}
    todo_total = 0
    for i in range(3):
        lines = []
        for j in range(60):
            if rnd.random() < 0.2:
                lines.append("    # TODO: item %d.%d" % (i, j))
                todo_total += 1
            else:
                lines.append("x_%d_%d = %d" % (i, j, j))
        files["m%d.py" % i] = "\n".join(lines) + "\n"
        wt(wd / "src" / ("m%d.py" % i), files["m%d.py" % i])
    old = ["alpha", "beta", "gamma", "delta", "eps", "zeta"]
    new = ["alpha", "gamma", "delta", "eta", "zeta", "theta"]
    wt(wd / "old.txt", "\n".join(old) + "\n")
    wt(wd / "new.txt", "\n".join(new) + "\n")
    hand = {"todo_count": todo_total + 3, "removed": ["beta"], "added": ["eta"]}  # an eyeballed tally carries silent errors
    counted = sum(len(re.findall(r"#\s*TODO", (wd / "src" / f).read_text())) for f in files)
    grep = sh(["grep", "-rc", "TODO", str(wd / "src")]).stdout
    grep_total = sum(int(l.rsplit(":", 1)[1]) for l in grep.split())
    o = set((wd / "old.txt").read_text().split())
    n = set((wd / "new.txt").read_text().split())
    diff = {"removed": sorted(o - n), "added": sorted(n - o)}
    pr = ("## Summary\n<!-- judgment: why this change -->\n\n## Counts (generated)\n- TODO markers: %d\n- removed: %s\n- added: %s\n"
          % (counted, ", ".join(diff["removed"]), ", ".join(diff["added"])))
    out = jw(wd / "scripted.json", {"todo": counted, "grep_cross_check": grep_total, "diff": diff, "hand_tally": hand})
    wt(wd / "PR_BODY.md", pr)
    return [
        check("scripted TODO count equals the planted total", counted == todo_total, counted, todo_total),
        check("independent grep -c agrees", grep_total == counted, grep_total, counted),
        check("set diff exact", diff == {"removed": ["beta", "eps"], "added": ["eta", "theta"]}, diff,
              {"removed": ["beta", "eps"], "added": ["eta", "theta"]}),
        check("PR scaffold generated with one judgment slot", pr.count("judgment") == 1, pr.count("judgment"), 1),
        check("negative control: the hand tally is wrong on count and diff", hand["todo_count"] != counted and hand["removed"] != diff["removed"],
              hand, {"todo_count": counted, **diff}),
    ], [out, wd / "PR_BODY.md"]


# ---------------------------------------------------------------- 9514 name it better (merge filters + shaping + scoring)
def snake(s):
    s = re.sub(r"[-\s]+", "_", s)
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", s)
    return s.lower()


def name_merge(pool, siblings, rejects, user_block, agent_block, affix="", reshape=True):
    def words(s):
        return set(snake(s).split("_"))
    keep, dropped = [], []
    seen = set()
    for c in pool:
        reason = None
        key = c.lower()
        if key in seen:
            reason = "duplicate"
        elif snake(c) in {snake(r) for r in rejects}:
            reason = "rejected incumbent"
        elif words(c) & set(user_block):
            reason = "user blocklist"
        elif snake(c) in {snake(s) for s in siblings}:
            reason = "collision"
        seen.add(key)
        (dropped if reason else keep).append({"name": c, "reason": reason})
    if reshape:
        shaped, out = set(), []
        for k in keep:
            s = snake(k["name"]) + affix
            reason = None
            if s in shaped:
                reason = "duplicate after shaping"
            elif s in {snake(r) for r in rejects}:
                reason = "rejected after shaping"
            elif s in {snake(x) for x in siblings}:
                reason = "collision after shaping"
            elif set(s.split("_")) & set(user_block):
                reason = "blocklist after shaping"
            shaped.add(s)
            if reason:
                dropped.append({"name": k["name"], "reason": reason})
            else:
                out.append({"name": k["name"], "shaped": s})
        keep = out
    for k in keep:
        k["flag"] = sorted(set(snake(k["name"]).split("_")) & set(agent_block))
    return keep, dropped


@card(K("2457-naming/9514-name-it-better"))
def name_it_better(task, wd):
    brief = {"modality": "python class", "responsibility": "keeps a user's login session between requests",
             "siblings": ["token_cache", "user_repository"], "user_block": ["manager"], "agent_block": ["store"],
             "rejects": ["SessionHandler"]}
    lenses = {"responsibility-literal": ["SessionStore", "LoginSessionKeeper", "SessionManager"],
              "moment-of-use": ["session-store", "ActiveSession", "TokenCache"],
              "domain-lore": ["SessionRegistry", "session handler", "ActiveSession"]}
    pool = [c for v in lenses.values() for c in v]
    keep, dropped = name_merge(pool, brief["siblings"], brief["rejects"], brief["user_block"], brief["agent_block"])
    # score by tiered criteria: accuracy (mentions session), scope fit (2-3 words), comprehensibility (no abbreviations)
    def score(k):
        w = k["shaped"].split("_")
        return ("session" in w, 2 <= len(w) <= 3, all(len(x) > 2 for x in w), -len(k["shaped"]))
    ranked = sorted(keep, key=score, reverse=True)
    out = jw(wd / "shortlist.json", {"brief": brief, "shortlist": ranked, "dropped": dropped,
                                     "recommended": ranked[0]["name"] if ranked else None, "human_picks": True})
    reasons = {d["name"]: d["reason"] for d in dropped}
    names = [k["name"] for k in ranked]
    naive, _ = name_merge(pool, brief["siblings"], brief["rejects"], brief["user_block"], brief["agent_block"], reshape=False)
    naive_shaped = [snake(k["name"]) for k in naive]
    return [
        check("survivors after merge + post-shaping filters", sorted(names) == sorted(["SessionStore", "LoginSessionKeeper", "ActiveSession", "SessionRegistry"]),
              sorted(names), sorted(["SessionStore", "LoginSessionKeeper", "ActiveSession", "SessionRegistry"])),
        check("each planted disqualification has the right reason",
              reasons == {"SessionManager": "user blocklist", "TokenCache": "collision", "session handler": "rejected incumbent",
                          "ActiveSession": "duplicate", "session-store": "duplicate after shaping"}, reasons, "5 planted reasons"),
        check("agent-inferred blocklist word only flags, never drops", [k["flag"] for k in ranked if k["name"] == "SessionStore"] == [["store"]],
              [k["flag"] for k in ranked if k["name"] == "SessionStore"], [["store"]]),
        check("recommended pick is the accurate, scope-fit, short one", ranked[0]["name"] == "SessionStore", ranked[0]["name"], "SessionStore"),
        check("negative control: without the post-shaping re-run two candidates normalize to session_store",
              naive_shaped.count("session_store") == 2, naive_shaped.count("session_store"), 2),
    ], [out]


# ---------------------------------------------------------------- 9955 write a skill (scaffold + review checklist)
def review_skill(d):
    d = Path(d)
    issues = []
    text = (d / "SKILL.md").read_text(encoding="utf-8") if (d / "SKILL.md").exists() else ""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    desc = fm.get("description", "")
    if not fm.get("name") or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm.get("name", "")):
        issues.append("name")
    if not desc or len(desc) > 1024:
        issues.append("description length")
    if "Use when" not in desc:
        issues.append("no 'Use when' trigger")
    if re.search(r"\b(I|you|my|your)\b", desc):
        issues.append("not third person")
    if len(text.splitlines()) >= 100:
        issues.append("SKILL.md over 100 lines")
    if re.search(r"\b(as of|currently|this year|20\d\d-\d\d)\b", text, re.I):
        issues.append("time-sensitive")
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if "/" in link.strip("./") and not link.startswith("http") and not link.startswith("scripts/"):
            issues.append("reference deeper than one level: " + link)
        elif not link.startswith("http") and not (d / link).exists():
            issues.append("broken link: " + link)
    if "```" not in text:
        issues.append("no concrete example")
    return issues


@card(K("2588-write-a-skill/9955-write-a-skill"))
def write_a_skill(task, wd):
    spec = {"name": "csv-dedupe", "what": "Remove duplicate rows from CSV files by a key column and report how many were dropped.",
            "triggers": "deduplicating CSV exports, cleaning repeated rows, or when the user mentions duplicate records in a CSV"}
    d = wd / spec["name"]
    helper = ("import csv, sys\nsrc, key, dst = sys.argv[1:4]\nseen, kept, dropped = set(), [], 0\n"
              "with open(src, newline='') as f:\n    r = csv.DictReader(f)\n    fields = r.fieldnames\n    for row in r:\n"
              "        if row[key] in seen:\n            dropped += 1\n            continue\n        seen.add(row[key]); kept.append(row)\n"
              "with open(dst, 'w', newline='') as f:\n    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(kept)\n"
              "print(dropped)\n")
    wt(d / "scripts" / "dedupe.py", helper)
    wt(d / "REFERENCE.md", "# Reference\n\nKey column matching is exact and case-sensitive.\n")
    wt(d / "SKILL.md", "---\nname: %s\ndescription: %s Use when %s.\n---\n\n# CSV dedupe\n\n## Quick start\n\n```bash\n"
       "python3 scripts/dedupe.py in.csv id out.csv\n```\n\n## Workflow\n\n- [ ] Pick the key column\n- [ ] Run the script\n"
       "- [ ] Report the dropped count\n\nDetails: [REFERENCE.md](REFERENCE.md)\n" % (spec["name"], spec["what"], spec["triggers"]))
    wt(wd / "in.csv", "id,v\n1,a\n2,b\n1,c\n3,d\n2,e\n")
    dropped = int(sh(["python3", str(d / "scripts/dedupe.py"), str(wd / "in.csv"), "id", str(wd / "out.csv")]).stdout)
    rows = (wd / "out.csv").read_text().strip().splitlines()
    issues = review_skill(d)
    bad = wd / "bad-skill"
    wt(bad / "SKILL.md", "---\nname: Docs Helper\ndescription: Helps with documents.\n---\n\nI help you as of 2026-01.\n"
       "See [x](refs/deep/x.md)\n" + "line\n" * 100)
    bad_issues = review_skill(bad)
    jw(wd / "review.json", {"skill": issues, "bad": bad_issues})
    return [
        check("scaffolded skill passes the review checklist", issues == [], issues, []),
        check("bundled script runs: 2 duplicates dropped, 3 rows kept", dropped == 2 and len(rows) == 4, [dropped, len(rows) - 1], [2, 3]),
        check("negative control: 'Helps with documents.' skill fails name, trigger, length, time, depth checks",
              {"name", "no 'Use when' trigger", "SKILL.md over 100 lines", "time-sensitive"} <= set(bad_issues)
              and any(i.startswith("reference deeper") for i in bad_issues), bad_issues, "planted 6 issues"),
    ], [d / "SKILL.md", wd / "review.json"]


# ---------------------------------------------------------------- 9958 net-config pre-deployment validation
def netcheck(cfg, existing, mgmt_if):
    lines = [l.rstrip() for l in cfg.splitlines()]
    finds = []
    iface = None
    ips = []
    acl = {}
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith("interface "):
            iface = s.split(None, 1)[1]
        if s == "shutdown" and iface == mgmt_if:
            finds.append(("dangerous", i, "shutdown on management interface " + mgmt_if))
        if re.match(r"(write erase|erase startup-config|reload|no aaa new-model)", s):
            finds.append(("dangerous", i, s))
        m = re.match(r"ip address (\S+) (\S+)", s)
        if m:
            net = ipaddress.ip_interface("%s/%s" % m.groups())
            ips.append((i, iface, net))
        if re.match(r"switchport trunk allowed vlan all", s):
            finds.append(("template", i, "trunk allows all VLANs"))
        m = re.match(r"access-list (\d+) (permit|deny) (\S+)(?: (\S+))?", s)
        if m:
            acl.setdefault(m.group(1), []).append((i, m.group(2), m.group(3), m.group(4)))
    seen = {}
    for i, f, net in ips:
        if str(net.ip) in seen or str(net.ip) in existing["ips"]:
            finds.append(("duplicate-ip", i, str(net.ip)))
        seen[str(net.ip)] = i
        for e in existing["subnets"]:
            if net.network.overlaps(ipaddress.ip_network(e)):
                finds.append(("overlap", i, "%s overlaps %s" % (net.network, e)))
    for n, rules in acl.items():
        for k, (i, act, src, wc) in enumerate(rules):
            for (j, act2, src2, wc2) in rules[:k]:
                if src2 == "any":
                    finds.append(("acl-shadowed", i, "rule under 'access-list %s %s any' is dead" % (n, act2)))
                    break
    if not any(re.match(r"(write memory|copy run(ning-config)? start(up-config)?)", l.strip()) for l in lines):
        finds.append(("incomplete", len(lines), "no write memory / copy run start"))
    return finds


@card(K("2591-bertram/9958-net-config"))
def net_config(task, wd):
    existing = {"subnets": ["10.10.0.0/24", "10.20.0.0/24"], "ips": ["10.30.0.1"]}
    raw = """interface Vlan30
 ip address 10.30.0.1 255.255.255.0
interface Vlan40
 ip address 10.10.0.129 255.255.255.128
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan all
interface GigabitEthernet0/0
 shutdown
access-list 110 permit any
access-list 110 deny 10.99.0.0 0.0.0.255
"""
    fixed = """interface Vlan30
 ip address 10.30.1.1 255.255.255.0
interface Vlan40
 ip address 10.40.0.1 255.255.255.0
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 30,40
access-list 110 deny 10.99.0.0 0.0.0.255
access-list 110 permit any
write memory
"""
    wt(wd / "raw.cfg", raw)
    wt(wd / "fixed.cfg", fixed)
    fr = netcheck(raw, existing, "GigabitEthernet0/0")
    ff = netcheck(fixed, existing, "GigabitEthernet0/0")
    kinds = sorted(k for k, *_ in fr)
    out = jw(wd / "findings.json", {"vendor": "Cisco IOS-style (syntax to verify via net-reference)", "raw": fr, "fixed": ff})
    want = sorted(["duplicate-ip", "overlap", "template", "dangerous", "acl-shadowed", "incomplete"])
    return [
        check("validated config has zero findings", ff == [], ff, []),
        check("negative control: the raw config shows exactly the 6 planted findings", kinds == want, kinds, want),
        check("overlap names the existing /24", any("10.10.0.128/25 overlaps 10.10.0.0/24" in f[2] for f in fr), True, True),
    ], [out, wd / "fixed.cfg"]


# ---------------------------------------------------------------- 10067 naming rule
MEANINGLESS = {"common", "util", "utils", "helper", "helpers", "misc", "result", "data", "stuff"}


def naming_lint(root):
    root = Path(root)
    finds = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        stem = p.stem if p.is_file() else p.name
        parts = set(re.split(r"[_\-.]", stem.lower()))
        if parts & MEANINGLESS:
            finds.append(("meaningless-path", rel))
        elif p.suffix == ".py" and re.search(r"[a-z]{3,}s$", stem) and not stem.endswith(("ss", "us", "is")):
            finds.append(("plural-module", rel))
        if p.suffix == ".py":
            tree = ast.parse(p.read_text())
            for n in ast.walk(tree):
                nm = None
                if isinstance(n, ast.FunctionDef):
                    nm = n.name
                elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                    nm = n.id
                elif isinstance(n, ast.ClassDef) and n.name.endswith("s") and not n.name.endswith("ss"):
                    finds.append(("plural-type", "%s:%s" % (rel, n.name)))
                if nm and set(nm.lower().split("_")) & MEANINGLESS:
                    finds.append(("meaningless-name", "%s:%s" % (rel, nm)))
    return sorted(set(finds))


@card(K("2650-programming-tasuke/10067-naming-rule"))
def naming_rule(task, wd):
    bad, good = wd / "bad", wd / "good"
    wt(bad / "common" / "util.py", "def format_util(x):\n    result = x * 2\n    return result\n")
    wt(bad / "users.py", "class Users:\n    pass\n")
    wt(bad / "invoice.py", "total = 3\n")
    wt(good / "price" / "format.py", "def format_price(cents):\n    doubled_cents = cents * 2\n    return doubled_cents\n")
    wt(good / "user.py", "class User:\n    pass\n")
    wt(good / "invoice.py", "total = 3\n")
    fb, fg = naming_lint(bad), naming_lint(good)
    out = jw(wd / "naming.json", {"bad": fb, "good": fg})
    want = sorted([("meaningless-path", "common"), ("meaningless-path", "common/util.py"), ("meaningless-name", "common/util.py:format_util"),
                   ("meaningless-name", "common/util.py:result"), ("plural-module", "users.py"), ("plural-type", "users.py:Users")])
    return [
        check("renamed tree follows the rule (0 findings)", fg == [], fg, []),
        check("negative control: original tree trips exactly the 6 planted names", fb == want, fb, want),
    ], [out]


# ---------------------------------------------------------------- 10068 prefer jq
@card(K("2650-programming-tasuke/10068-prefer-jq"))
def prefer_jq(task, wd):
    doc = {"items": [{"name": "alpha", "active": True, "size": 10}, {"name": "beta", "active": False, "size": 32},
                     {"name": "gamma", "active": True, "size": 7}]}
    f = jw(wd / "api.json", doc)
    first = sh(["jq", "-r", ".items[0].name", str(f)]).stdout.strip()
    active = sh(["jq", "-r", ".items[] | select(.active) | .name", str(f)]).stdout.split()
    total = int(sh(["jq", "[.items[].size] | add", str(f)]).stdout)
    tricky = 'O"Brien \\ x'
    safe = sh(["jq", "--arg", "name", tricky, ".name = $name", str(f)]).stdout
    safe_val = json.loads(safe)["name"]
    concat = sh(["jq", '.name = "%s"' % tricky, str(f)], ok=False)
    e_false = sh(["jq", "-e", ".items[1].active", str(f)], ok=False).returncode
    e_none = sh(["jq", "-e", ".items[] | select(.size > 100)", str(f)], ok=False).returncode
    e_true = sh(["jq", "-e", ".items[0].active", str(f)], ok=False).returncode
    out = jw(wd / "jq_results.json", {"first": first, "active": active, "total": total, "arg_value": safe_val,
                                      "concat_exit": concat.returncode, "exit_codes": [e_true, e_false, e_none]})
    return [
        check("extract / filter / aggregate match the known values", [first, active, total] == ["alpha", ["alpha", "gamma"], 49],
              [first, active, total], ["alpha", ["alpha", "gamma"], 49]),
        check("--arg passes a value with quote and backslash intact", safe_val == tricky, safe_val, tricky),
        check("-e exit statuses: true 0, false 1, no output 4", [e_true, e_false, e_none] == [0, 1, 4], [e_true, e_false, e_none], [0, 1, 4]),
        check("negative control: string-concatenated filter breaks on the same value", concat.returncode != 0, concat.returncode, "non-zero"),
    ], [out]


# ---------------------------------------------------------------- React: TypeScript AST lint + react-dom/server render
_TSX_TOOL = r"""
const ts = require(%(ts)s); const fs = require('fs');
const React = require(%(react)s); const RDS = require(%(rds)s);
function analyse(file){
  const src = fs.readFileSync(file,'utf8');
  const sf = ts.createSourceFile(file, src, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TSX);
  const order=[]; const comps=[]; const effects=[]; const refs=[]; const derived=[];
  const hasJsx = n => { let f=false; (function w(x){ if(ts.isJsxElement(x)||ts.isJsxSelfClosingElement(x)||ts.isJsxFragment(x)) f=true; else ts.forEachChild(x,w);})(n); return f; };
  const firstJsxLine = n => { let l=null; (function w(x){ if(l===null && (ts.isJsxElement(x)||ts.isJsxSelfClosingElement(x)||ts.isJsxFragment(x))) l=sf.getLineAndCharacterOfPosition(x.getStart()).line; else ts.forEachChild(x,w);})(n); return l; };
  for (const st of sf.statements){
    if (ts.isImportDeclaration(st)) continue;
    let kind='other', name=null, body=null;
    if (ts.isTypeAliasDeclaration(st)||ts.isInterfaceDeclaration(st)) { kind = /Props$/.test(st.name.text)?'props':'type'; name=st.name.text; }
    else if (ts.isFunctionDeclaration(st) && st.name && /^[A-Z]/.test(st.name.text) && hasJsx(st)) { kind='component'; name=st.name.text; body=st; }
    else if (ts.isVariableStatement(st)) {
      const d = st.declarationList.declarations[0]; name = d.name.getText();
      if (d.initializer && ts.isCallExpression(d.initializer) && /^(sva|cva|css)$/.test(d.initializer.expression.getText())) kind='design';
      else if (/^[A-Z]/.test(name) && d.initializer && hasJsx(d.initializer)) { kind='component'; body=d.initializer; }
      else if (/^use[A-Z]/.test(name)) kind='hook';
    }
    if (kind==='component') {
      const start = sf.getLineAndCharacterOfPosition(body.getStart()).line; const j = firstJsxLine(body);
      const c = {name, linesBeforeJsx: j - start, precededByRenderPropComment: /render prop|renderRow|render に|に渡す/.test(src.slice(Math.max(0, st.getFullStart()), st.getStart()))};
      comps.push(c);
      (function w(x){
        if (ts.isCallExpression(x)) {
          const callee = x.expression.getText();
          if (callee==='useEffect'||callee==='React.useEffect') {
            const fn = x.arguments[0]; const txt = fn ? fn.getText() : '';
            const onlySet = fn && fn.body && ts.isBlock(fn.body) && fn.body.statements.length===1 && /^set[A-Z]\w*\(/.test(fn.body.statements[0].getText());
            effects.push({component:name, derivedState: !!onlySet});
          }
          if (callee==='useRef'||callee==='React.useRef'||/^useRef</.test(callee)) {
            const decl = x.parent && ts.isVariableDeclaration(x.parent) ? x.parent.name.getText() : '?';
            const uses = (src.match(new RegExp(decl+'\\.current','g'))||[]).length;
            const pattern = /\.current\.open\s*=/.test(src) && decl.startsWith('details') ? 'use <details>' :
                            new RegExp(decl+'\\.current\\s*\\+=').test(src) ? 'use useState' :
                            new RegExp(decl+'\\.current\\s*=\\s*window\\.setInterval').test(src) ? 'local variable inside the effect' : 'review';
            refs.push({component:name, ref:decl, uses, suggest:pattern});
          }
        }
        ts.forEachChild(x,w);
      })(body);
    }
    order.push({kind, name});
  }
  return {order, comps, effects, refs};
}
function render(file, props){
  const src = fs.readFileSync(file,'utf8');
  const js = ts.transpileModule(src,{compilerOptions:{module:ts.ModuleKind.CommonJS, jsx:ts.JsxEmit.React, target:ts.ScriptTarget.ES2020, esModuleInterop:true}}).outputText;
  const m={exports:{}}; const req = (n)=> n==='react'?React : n.startsWith('./') ? load(require('path').join(require('path').dirname(file), n)) : require(n);
  function load(p){ const f = fs.existsSync(p+'.ts')?p+'.ts':p+'.tsx'; const s = fs.readFileSync(f,'utf8');
    const j = ts.transpileModule(s,{compilerOptions:{module:ts.ModuleKind.CommonJS, jsx:ts.JsxEmit.React, target:ts.ScriptTarget.ES2020, esModuleInterop:true}}).outputText;
    const mm={exports:{}}; new Function('require','module','exports',j)(req,mm,mm.exports); return mm.exports; }
  new Function('require','module','exports',js)(req,m,m.exports);
  const C = Object.values(m.exports).find(v=>typeof v==='function');
  return RDS.renderToStaticMarkup(React.createElement(C, props||{}));
}
const files = JSON.parse(process.argv[2]); const out={};
for (const [k,v] of Object.entries(files)) { out[k] = analyse(v.file); if (v.render) out[k].html = render(v.file, v.props); }
console.log(JSON.stringify(out));
"""


def _react_dir():
    nested = NM / "react-dom/node_modules/react"  # react-dom must share its own React copy or hooks break
    return nested if nested.exists() else NM / "react"


def tsx_tool(wd, files):
    js = _TSX_TOOL % {"ts": json.dumps(str(NM / "typescript")), "react": json.dumps(str(_react_dir())),
                      "rds": json.dumps(str(NM / "react-dom/server"))}
    src = wt(Path(wd) / "tsx_tool.cjs", js)
    done = sh(["node", str(src), json.dumps(files)], cwd=wd, timeout=40)
    return json.loads(done.stdout.strip().splitlines()[-1])


def react_conv_findings(a):
    f = []
    kinds = [o["kind"] for o in a["order"] if o["kind"] in ("design", "props", "component")]
    rank = {"design": 0, "props": 1, "component": 2}
    if any(rank[x] > rank[y] for x, y in zip(kinds, kinds[1:])):
        f.append("structure order")
    extra = [c for c in a["comps"][1:] if not c["precededByRenderPropComment"]]
    if extra:
        f.append("more than one component per file")
    if any(c["linesBeforeJsx"] > 30 for c in a["comps"]):
        f.append("30+ lines before JSX")
    return f


@card(K("2654-web-tasuke/10085-react-component-convention"))
def react_component_convention(task, wd):
    logic = "\n".join("  const v%d = props.n + %d;" % (i, i) for i in range(32))
    bad = wt(wd / "bad/DeviceList.tsx", "import React from 'react';\n\nexport function DeviceList(props: Props) {\n" + logic +
             "\n  return <ul>{props.items.map((d) => <Row key={d.id} d={d} />)}</ul>;\n}\n\ntype Props = { n: number; items: {id:string;name:string}[] };\n\n"
             "const Row = ({ d }: { d: { id: string; name: string } }) => <li>{d.name}</li>;\n")
    wt(wd / "good/DeviceRow.tsx", "import React from 'react';\n\ntype DeviceRowProps = { d: { id: string; name: string } };\n\n"
       "export const DeviceRow: React.FC<DeviceRowProps> = ({ d }) => <li>{d.name}</li>;\n")
    wt(wd / "good/useDeviceTotal.ts", "export function useDeviceTotal(n: number): number {\n  return n + 1;\n}\n")
    good = wt(wd / "good/DeviceList.tsx", "import React from 'react';\nimport { DeviceRow } from './DeviceRow';\nimport { useDeviceTotal } from './useDeviceTotal';\n\n"
              "const listStyle = css({ padding: 0 });\n\ntype Props = { n: number; items: { id: string; name: string }[] };\n\n"
              "export function DeviceList(props: Props): React.ReactElement {\n  const total = useDeviceTotal(props.n);\n"
              "  return <ul data-total={total}>{props.items.map((d) => <DeviceRow key={d.id} d={d} />)}</ul>;\n}\n\n"
              "function css(o: object) { return o; }\n")
    res = tsx_tool(wd, {"bad": {"file": str(bad)}, "good": {"file": str(good), "render": True,
                                                            "props": {"n": 4, "items": [{"id": "a", "name": "Router"}, {"id": "b", "name": "Switch"}]}}})
    fb, fg = react_conv_findings(res["bad"]), react_conv_findings(res["good"])
    out = jw(wd / "react_convention.json", {"bad": fb, "good": fg, "html": res["good"]["html"]})
    want_html = '<ul data-total="5"><li>Router</li><li>Switch</li></ul>'
    return [
        check("refactored file: design -> props -> component, one component, no findings", fg == [], fg, []),
        check("refactored component renders the same list via react-dom/server", res["good"]["html"] == want_html, res["good"]["html"], want_html),
        check("negative control: original file breaks order, has 2 components and 30+ lines before JSX",
              fb == ["structure order", "more than one component per file", "30+ lines before JSX"], fb, "3 planted findings"),
    ], [out, good]


@card(K("2654-web-tasuke/10087-react-use-effect"))
def react_use_effect(task, wd):
    bad = wt(wd / "bad/Profile.tsx", "import React, { useState, useEffect } from 'react';\n\ntype Props = { first: string; last: string };\n\n"
             "export function Profile({ first, last }: Props) {\n  const [fullName, setFullName] = useState('');\n"
             "  useEffect(() => {\n    setFullName(first + ' ' + last);\n  }, [first, last]);\n  return <h1>{fullName}</h1>;\n}\n")
    wt(wd / "good/useDocumentTitle.ts", "import { useEffect } from 'react';\nexport function useDocumentTitle(title: string): void {\n"
       "  useEffect(() => {\n    if (typeof document !== 'undefined') document.title = title;\n  }, [title]);\n}\n")
    good = wt(wd / "good/Profile.tsx", "import React from 'react';\nimport { useDocumentTitle } from './useDocumentTitle';\n\n"
              "type Props = { first: string; last: string };\n\nexport function Profile({ first, last }: Props) {\n"
              "  const fullName = first + ' ' + last;\n  useDocumentTitle(fullName);\n  return <h1>{fullName}</h1>;\n}\n")
    props = {"first": "Ada", "last": "Lovelace"}
    res = tsx_tool(wd, {"bad": {"file": str(bad), "render": True, "props": props}, "good": {"file": str(good), "render": True, "props": props}})
    out = jw(wd / "use_effect.json", res)
    return [
        check("refactor has no useEffect in the component body", res["good"]["effects"] == [], res["good"]["effects"], []),
        check("derived value computed during render: SSR shows the full name", res["good"]["html"] == "<h1>Ada Lovelace</h1>", res["good"]["html"], "<h1>Ada Lovelace</h1>"),
        check("negative control: the effect-driven version is flagged as derived state", res["bad"]["effects"] == [{"component": "Profile", "derivedState": True}],
              res["bad"]["effects"], [{"component": "Profile", "derivedState": True}]),
        check("negative control: the effect-driven version renders an empty heading on first render", res["bad"]["html"] == "<h1></h1>", res["bad"]["html"], "<h1></h1>"),
    ], [out, good]


@card(K("2654-web-tasuke/10088-react-use-ref"))
def react_use_ref(task, wd):
    bad = wt(wd / "bad/Panel.tsx", "import React, { useRef, useEffect } from 'react';\n\nexport function Panel() {\n"
             "  const detailsRef = useRef<HTMLDetailsElement>(null);\n  const countRef = useRef(0);\n  countRef.current += 1;\n"
             "  const timerIdRef = useRef<number>();\n  useEffect(() => {\n    timerIdRef.current = window.setInterval(() => {}, 1000);\n"
             "    return () => clearInterval(timerIdRef.current);\n  }, []);\n"
             "  const toggle = () => { if (detailsRef.current) { detailsRef.current.open = !detailsRef.current.open; } };\n"
             "  return <div><button onClick={toggle}>more</button><details ref={detailsRef}><p>body</p></details><span>{countRef.current}</span></div>;\n}\n")
    good = wt(wd / "good/Panel.tsx", "import React, { useState } from 'react';\n\nexport function Panel() {\n  const [count] = useState(0);\n"
              "  return <div><details><summary>more</summary><p>body</p></details><span>{count}</span></div>;\n}\n")
    res = tsx_tool(wd, {"bad": {"file": str(bad)}, "good": {"file": str(good), "render": True}})
    sugg = sorted(r["suggest"] for r in res["bad"]["refs"])
    out = jw(wd / "use_ref.json", res)
    want = '<div><details><summary>more</summary><p>body</p></details><span>0</span></div>'
    return [
        check("refactor uses no useRef", res["good"]["refs"] == [], res["good"]["refs"], []),
        check("declarative <details> renders server-side with state value", res["good"]["html"] == want, res["good"]["html"], want),
        check("negative control: original has 3 refs, each mapped to its standard alternative",
              sugg == ["local variable inside the effect", "use <details>", "use useState"], sugg, "3 alternatives"),
    ], [out, good]


# ---------------------------------------------------------------- 10339 CircleCI config
def circle_audit(cfg):
    import yaml
    c = yaml.safe_load(cfg)
    f = []
    for jn, job in (c.get("jobs") or {}).items():
        for st in job.get("steps", []):
            if isinstance(st, dict):
                for k in ("save_cache", "restore_cache"):
                    if k in st:
                        keys = [st[k].get("key")] if st[k].get("key") else st[k].get("keys", [])
                        for key in keys:
                            if "{{ epoch }}" in key or "{{ .BuildNum }}" in key or "{{ .Revision }}" in key:
                                f.append((jn, "cache key rotates every run"))
                            if "checksum" in key and not re.search(r'checksum "[^"]*(lock|\.sum)', key):
                                f.append((jn, "cache key not on a lockfile"))
                if "run" in st and isinstance(st["run"], dict) and re.search(r"(retry|\|\| true|for i in)", st["run"].get("command", "")):
                    f.append((jn, "blanket retry hides failures"))
        if jn.startswith("test") and not any(isinstance(s, dict) and "store_test_results" in s for s in job.get("steps", [])):
            f.append((jn, "no store_test_results"))
    for wn, wf in (c.get("workflows") or {}).items():
        if not isinstance(wf, dict):
            continue
        names = [list(j)[0] if isinstance(j, dict) else j for j in wf.get("jobs", [])]
        for n in set(names):
            if names.count(n) > 1:
                f.append((wn, "duplicate job " + n))
        reqs = {list(j)[0]: j[list(j)[0]].get("requires", []) for j in wf.get("jobs", []) if isinstance(j, dict)}
        types = {list(j)[0]: j[list(j)[0]].get("type") for j in wf.get("jobs", []) if isinstance(j, dict)}
        if "deploy" in reqs and not any(types.get(r) == "approval" for r in reqs["deploy"]):
            f.append((wn, "deploy without approval gate"))
    return sorted(set(f))


@card(K("2691-circleci/10339-circleci-config"))
def circleci_config(task, wd):
    raw = """version: 2.1
jobs:
  build:
    docker: [{image: cimg/node:20.11}]
    steps:
      - checkout
      - restore_cache: {keys: ['deps-{{ checksum "package.json" }}-{{ epoch }}']}
      - run: npm ci
      - save_cache: {key: 'deps-{{ checksum "package.json" }}-{{ epoch }}', paths: [~/.npm]}
  test:
    docker: [{image: cimg/node:20.11}]
    steps:
      - checkout
      - run: {command: 'for i in 1 2 3; do npm test && break; done'}
  deploy:
    docker: [{image: cimg/node:20.11}]
    steps: [checkout, {run: ./deploy.sh}]
workflows:
  main:
    jobs:
      - build
      - test
      - test
      - hold: {type: approval, requires: [test]}
      - deploy: {requires: [hold], filters: {branches: {only: main}}}
"""
    fixed = """version: 2.1
jobs:
  build:
    docker: [{image: cimg/node:20.11}]
    steps:
      - checkout
      - restore_cache: {keys: ['v1-npm-{{ checksum "package-lock.json" }}', 'v1-npm-']}
      - run: npm ci
      - save_cache: {key: 'v1-npm-{{ checksum "package-lock.json" }}', paths: [~/.npm]}
      - persist_to_workspace: {root: ., paths: [node_modules]}
  test:
    docker: [{image: cimg/node:20.11}]
    parallelism: 2
    steps:
      - checkout
      - attach_workspace: {at: .}
      - run: {command: 'npx jest --ci --reporters=default --reporters=jest-junit'}
      - store_test_results: {path: reports/junit}
  deploy:
    docker: [{image: cimg/node:20.11}]
    steps: [checkout, {run: ./deploy.sh}]
workflows:
  main:
    jobs:
      - build
      - test: {requires: [build]}
      - hold: {type: approval, requires: [test]}
      - deploy: {requires: [hold], filters: {branches: {only: main}}}
"""
    wt(wd / "config.raw.yml", raw)
    out_cfg = wt(wd / ".circleci/config.yml", fixed)
    fr, ff = circle_audit(raw), circle_audit(fixed)
    import yaml
    parsed = yaml.safe_load(fixed)
    gate = parsed["workflows"]["main"]["jobs"][2]["hold"]["type"] == "approval"
    rep = jw(wd / "circleci_report.json", {"baseline_findings": fr, "after": ff, "deploy_gate_preserved": gate,
                                           "rollback": "git revert of .circleci/config.yml", "expected": "cache restores on unchanged lockfile; one test run"})
    want = sorted([("build", "cache key rotates every run"), ("build", "cache key not on a lockfile"),
                   ("test", "blanket retry hides failures"), ("test", "no store_test_results"), ("main", "duplicate job test")])
    return [
        check("optimized config has zero findings", ff == [], ff, []),
        check("deployment approval gate preserved", gate, gate, True),
        check("negative control: original config shows exactly the 5 planted problems", fr == want, fr, want),
    ], [out_cfg, rep]


# ---------------------------------------------------------------- 901 Claude automation recommender (read-only)
def _tree_hash(root):
    import hashlib
    h = hashlib.sha256()
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            h.update(p.relative_to(root).as_posix().encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def recommend(root):
    root = Path(root)
    pkg = json.loads((root / "package.json").read_text()) if (root / "package.json").exists() else {}
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    sig = {
        "react": "react" in deps, "frontend": bool({"react", "vue", "@angular/core", "next"} & set(deps)),
        "prisma": "prisma" in deps or "@prisma/client" in deps, "github": (root / ".github").is_dir(),
        "prettier": "prettier" in deps or (root / ".prettierrc").exists(), "eslint": "eslint" in deps,
        "typescript": (root / "tsconfig.json").exists(), "tests": (root / "tests").is_dir() or (root / "__tests__").is_dir(),
        "env": any(root.glob(".env*")), "auth": any(re.search(r"auth|payment", p.relative_to(root).as_posix()) for p in root.rglob("*.ts")),
        "claude": (root / ".claude").exists(),
    }
    rec = {"mcp": [], "skills": [], "hooks": [], "subagents": [], "plugins": []}
    if sig["react"]:
        rec["mcp"].append(("context7", "React is a popular library: live docs lookup"))
    if sig["frontend"]:
        rec["mcp"].append(("Playwright", "frontend with UI testing needs"))
    if sig["prisma"] and len(rec["mcp"]) < 2:
        rec["mcp"].append(("Database MCP", "Prisma schema"))
    if sig["prettier"]:
        rec["hooks"].append(("PostToolUse: auto-format on edit", "Prettier configured"))
    if sig["env"]:
        rec["hooks"].append(("PreToolUse: block .env edits", ".env files present"))
    elif sig["typescript"]:
        rec["hooks"].append(("PostToolUse: type-check on edit", "TypeScript project"))
    if sig["auth"]:
        rec["subagents"].append(("security-reviewer", "auth/payments code"))
    if sig["tests"]:
        rec["skills"].append(("gen-test", "test suite present"))
    if sig["frontend"]:
        rec["plugins"].append(("frontend-design", "frontend development"))
    rec = {k: v[:2] for k, v in rec.items() if v}
    return sig, rec


@card(K("278-claude-code-setup/901-claude-automation-recommender"))
def automation_recommender(task, wd):
    repo = wd / "repo"
    wt(repo / "package.json", json.dumps({"dependencies": {"react": "19.0.0", "@prisma/client": "6.0.0"},
                                          "devDependencies": {"prettier": "3.3.0", "typescript": "5.6.0"}}))
    wt(repo / "tsconfig.json", "{}")
    wt(repo / ".env.local", "X=1\n")
    wt(repo / "src/auth/session.ts", "export const a = 1;\n")
    wt(repo / "tests/a.test.ts", "test('x',()=>{});\n")
    wt(repo / ".github/workflows/ci.yml", "on: push\n")
    before = _tree_hash(repo)
    sig, rec = recommend(repo)
    after = _tree_hash(repo)
    md = ["## Claude Code Automation Recommendations", "", "### Codebase Profile", "- **Type**: TypeScript / Node",
          "- **Framework**: React", ""]
    for k, items in rec.items():
        md.append("### " + k)
        md += ["#### %s\n**Why**: %s" % it for it in items]
    md.append("\nAsk for more recommendations in any category.")
    out = wt(wd / "recommendations.md", "\n".join(md) + "\n")
    empty = wd / "empty"
    empty.mkdir()
    _, rec_empty = recommend(empty)
    names = {k: [n for n, _ in v] for k, v in rec.items()}
    want = {"mcp": ["context7", "Playwright"], "hooks": ["PostToolUse: auto-format on edit", "PreToolUse: block .env edits"],
            "subagents": ["security-reviewer"], "skills": ["gen-test"], "plugins": ["frontend-design"]}
    return [
        check("recommendations follow the signal table, 1-2 per category", names == want, names, want),
        check("analysis is read-only: repo tree hash unchanged", before == after, after[:12], before[:12]),
        check("negative control: a repo with no signals gets no framework-based recommendations", rec_empty == {}, rec_empty, {}),
    ], [out]


# ---------------------------------------------------------------- 11336 review SystemVerilog
def sv_review(path):
    src = Path(path).read_text().splitlines()
    finds = []
    block = None
    depth = 0
    for i, line in enumerate(src, 1):
        s = re.sub(r"//.*", "", line).strip()
        if re.match(r"`define\s", s):
            finds.append(("P2", i, "`define for a constant: use localparam/parameter in a package"))
        if re.search(r"\b(reg|wire)\b", s) and not s.startswith("//"):
            finds.append(("P2", i, "legacy reg/wire: use logic"))
        m = re.match(r"always\s*@\s*\((posedge|negedge)", s)
        if m:
            finds.append(("P1", i, "always @(edge): use always_ff"))
            block = "ff"
        elif re.match(r"always\s*@\s*(\(\*\)|\*)", s):
            finds.append(("P1", i, "always @*: use always_comb"))
            block = "comb"
        elif s.startswith("always_ff"):
            block = "ff"
        elif s.startswith("always_comb"):
            block = "comb"
        if block == "ff" and re.search(r"(?<![<=!>])=(?!=)", s) and "<=" not in s and not s.startswith(("always", "case")):
            finds.append(("P0", i, "blocking assignment in a sequential block: use <="))
        if block == "comb" and re.match(r"if\s*\(", s):
            rest = "\n".join(src[i:i + 4])
            if not re.search(r"\belse\b", rest):
                finds.append(("P0", i, "if without else in combinational logic infers a latch"))
        if re.match(r"case\s*\(", s):
            finds.append(("P1", i, "bare case: use unique case / priority case"))
        if re.match(r"\w+\s+\w+\s*\(\s*\w+\s*,", s) and not s.startswith(("module", "function", "task")):
            finds.append(("P1", i, "positional port connection: use .port(signal)"))
        if s.startswith("end") and s in ("end", "endcase"):
            depth = 0
        if s.startswith(("endmodule", "assign")):
            block = None
    return finds


@card(K("2807-hdl/11336-review-systemverilog"))
def review_systemverilog(task, wd):
    legacy = wt(wd / "legacy.v", """`define WIDTH 8
module counter(clk, rst, en, q, sel, y);
  input clk, rst, en;
  output reg [7:0] q;
  input [1:0] sel;
  output reg y;
  always @(posedge clk) begin
    if (rst) q = 0;
    else q = q + 1;
  end
  always @* begin
    if (en)
      y <= q[0];
  end
  always @* begin
    case (sel)
      2'd0: y = 1'b0;
    endcase
  end
  sub u0 (clk, q);
endmodule
""")
    clean = wt(wd / "counter.sv", """package counter_pkg;
  localparam int unsigned Width = 8;
endpackage
module counter import counter_pkg::*; (
  input  logic             clk_i,
  input  logic             rst_ni,
  input  logic             en_i,
  input  logic [1:0]       sel_i,
  output logic [Width-1:0] q_o,
  output logic             y_o
);
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) q_o <= '0;
    else q_o <= q_o + 1'b1;
  end
  always_comb begin
    y_o = 1'b0;
    unique case (sel_i)
      2'd0: y_o = q_o[0];
      default: y_o = en_i;
    endcase
  end
  sub u_sub (.clk_i(clk_i), .q_i(q_o));
endmodule
""")
    fl, fc = sv_review(legacy), sv_review(clean)
    table = ["| Pri | Line | Finding |", "|---|---|---|"] + ["| %s | %d | %s |" % f for f in sorted(fl)]
    out = wt(wd / "review.md", "# SystemVerilog review: legacy.v\n\n" + "\n".join(table) + "\n")
    jw(wd / "review.json", {"legacy": fl, "clean": fc})
    got = sorted((p, l) for p, l, _ in fl)
    want = sorted([("P2", 1), ("P2", 4), ("P2", 6), ("P1", 7), ("P0", 8), ("P0", 9), ("P1", 11), ("P0", 12),
                   ("P1", 15), ("P1", 16), ("P1", 20)])
    return [
        check("idiomatic SystemVerilog file audits clean", fc == [], fc, []),
        check("negative control: legacy file yields the 11 planted findings at the right lines and priorities", got == want, got, want),
        check("P0 count (blocking in seq x2, latch)", sum(1 for f in fl if f[0] == "P0") == 3, sum(1 for f in fl if f[0] == "P0"), 3),
    ], [out]


# ---------------------------------------------------------------- 11567 effective Go
GO_ERR_RULES = [
    (r'fmt\.Errorf\("[^"%]*"\)', "fmt.Errorf with no directive: use errors.New"),
    (r'(fmt\.Errorf|errors\.New)\("[A-Z][a-z]', "capitalized error string"),
    (r"'%s'", "'%s' instead of %q"),
    (r'Errorf\("%w', "%w first: wrapped error goes last"),
    (r'\.Error\(\)\s*==', "err.Error() compared to a string: use errors.Is/As"),
    (r'(fmt\.Errorf|errors\.New)\("[^"]*\.\s*"', "trailing period in error string"),
    (r'Errorf\("(opening|open|error)\b', "operational message not in 'failed to <verb> <object>' form"),
    (r'^package (utils?|common)$', "meaningless package name"),
]


def go_err_lint(text):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        for rx, msg in GO_ERR_RULES:
            if re.search(rx, line):
                out.append((i, msg))
    return out


@card(K("2858-effective-go/11567-effective-go"))
def effective_go(task, wd):
    if not fx.which("go"):
        raise RuntimeError("go toolchain missing")
    good = wd / "good"
    wt(good / "go.mod", "module example.com/config\n\ngo 1.24\n")
    wt(good / "config.go", '''// Package config loads key=value settings files.
package config

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strings"
)

// ErrMissingKey is returned when a required key is absent.
var ErrMissingKey = errors.New("required key not found")

// Load reads path and returns its key=value pairs.
func Load(path string) (map[string]string, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("failed to open config file %q: %w", path, err)
	}
	defer f.Close()
	out := map[string]string{}
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		k, v, ok := strings.Cut(sc.Text(), "=")
		if !ok {
			continue
		}
		out[strings.TrimSpace(k)] = strings.TrimSpace(v)
	}
	if err := sc.Err(); err != nil {
		return nil, fmt.Errorf("failed to read config file %q: %w", path, err)
	}
	return out, nil
}

// Require returns the value of key or ErrMissingKey.
func Require(cfg map[string]string, key string) (string, error) {
	v, ok := cfg[key]
	if !ok {
		return "", fmt.Errorf("failed to look up %q: %w", key, ErrMissingKey)
	}
	return v, nil
}
''')
    wt(good / "config_test.go", '''package config

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func TestRequire(t *testing.T) {
	t.Parallel()
	dir := t.TempDir()
	path := filepath.Join(dir, "app.conf")
	if err := os.WriteFile(path, []byte("bucket = logs\\nregion=eu\\n"), 0o600); err != nil {
		t.Fatalf("WriteFile() = %v", err)
	}
	cfg, err := Load(path)
	if err != nil {
		t.Fatalf("Load(%q) error = %v", path, err)
	}
	tests := []struct {
		name    string
		key     string
		want    string
		wantErr error
	}{
		{name: "present", key: "bucket", want: "logs"},
		{name: "trimmed", key: "region", want: "eu"},
		{name: "missing", key: "zone", wantErr: ErrMissingKey},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Require(cfg, tt.key)
			if !errors.Is(err, tt.wantErr) {
				t.Errorf("Require(%q) error = %v, want %v", tt.key, err, tt.wantErr)
			}
			if got != tt.want {
				t.Errorf("Require(%q) = %q, want %q", tt.key, got, tt.want)
			}
		})
	}
	if _, err := Load(filepath.Join(dir, "absent.conf")); !errors.Is(err, os.ErrNotExist) {
		t.Errorf("Load(absent) error = %v, want os.ErrNotExist", err)
	}
}
''')
    bad_src = '''package utils

import (
	"errors"
	"fmt"
)

func Check(err error) error {
	if err.Error() == "boom" {
		return fmt.Errorf("Failed to check")
	}
	if err != nil {
		return fmt.Errorf("%w: opening '%s'", err, "x")
	}
	return errors.New("bad input.")
}
'''
    wt(wd / "bad/utils.go", bad_src)
    env = {"GOFLAGS": "-mod=mod", "GOTOOLCHAIN": "local", "GOPROXY": "off", "CGO_ENABLED": "0"}
    fmt_out = sh(["gofmt", "-l", "."], cwd=good, env=env).stdout.strip()
    vet = sh(["go", "vet", "./..."], cwd=good, env=env, timeout=60)
    test = sh(["go", "test", "-count=1", "./..."], cwd=good, env=env, timeout=90)
    lint_good = go_err_lint((good / "config.go").read_text() + (good / "config_test.go").read_text())
    lint_bad = go_err_lint(bad_src)
    rep = jw(wd / "go_gates.json", {"gofmt_l": fmt_out, "vet_rc": vet.returncode, "test_stdout": test.stdout.strip(),
                                    "house_errors_good": lint_good, "house_errors_bad": lint_bad})
    want_bad = sorted({"fmt.Errorf with no directive: use errors.New", "capitalized error string", "'%s' instead of %q",
                       "%w first: wrapped error goes last", "err.Error() compared to a string: use errors.Is/As",
                       "trailing period in error string", "meaningless package name"})
    return [
        check("gofmt -l lists nothing", fmt_out == "", fmt_out, ""),
        check("go vet and go test pass (table test, errors.Is, t.TempDir)", vet.returncode == 0 and test.stdout.startswith("ok"),
              test.stdout.strip()[:60], "ok example.com/config"),
        check("house error form: no red flags in the written package", lint_good == [], lint_good, []),
        check("negative control: the unreviewed file trips the 7 planted red flags", sorted({m for _, m in lint_bad}) == want_bad,
              sorted({m for _, m in lint_bad}), want_bad),
    ], [rep, good / "config.go"]


# ---------------------------------------------------------------- 11568 implement-plan: item-by-item conformance review
def conformance(plan, repo):
    rows = []
    for it in plan["items"]:
        done = subprocess.run(it["check"], shell=True, capture_output=True, text=True, cwd=str(repo), timeout=30,
                              stdin=subprocess.DEVNULL, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        got = done.stdout.strip()
        rows.append({"id": it["id"], "spec": it["spec"], "command": it["check"], "observed": got, "expected": it["expect"],
                     "status": "conforms" if done.returncode == 0 and got == it["expect"] else "gap"})
    actual = sorted(p.relative_to(repo).as_posix() for p in repo.rglob("*") if p.is_file())
    drift = sorted(set(actual) - set(plan["only_files"]))
    return rows, drift


@card(K("2859-implement-plan/11568-implement-plan"))
def implement_plan(task, wd):
    plan = {"title": "Add slugify + CLI flag", "only_files": ["slug.py", "cli.py", "test_slug.py"],
            "items": [
                {"id": "1", "spec": "slugify('Hello World!') returns 'hello-world'",
                 "check": "python3 -c \"import slug;print(slug.slugify('Hello World!'))\"", "expect": "hello-world"},
                {"id": "2", "spec": "slugify collapses repeated separators", "check": "python3 -c \"import slug;print(slug.slugify('a  --  b'))\"",
                 "expect": "a-b"},
                {"id": "3", "spec": "cli.py --max 5 truncates to 5 chars", "check": "python3 cli.py --max 5 'Hello World'",
                 "expect": "hello"},
                {"id": "4", "spec": "tests pass", "check": "python3 -m unittest -q test_slug 2>&1 | tail -1", "expect": "OK"},
            ]}
    repo = wd / "repo"
    wt(repo / "slug.py", "import re\n\ndef slugify(s):\n    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')\n")
    wt(repo / "cli.py", "import sys, slug\nprint(slug.slugify(sys.argv[-1]))\n")  # executor forgot --max
    wt(repo / "test_slug.py", "import unittest, slug\n\nclass T(unittest.TestCase):\n    def test_basic(self):\n"
       "        self.assertEqual(slug.slugify('Hello World!'), 'hello-world')\n")
    wt(repo / "notes_debug.txt", "scratch\n")  # out-of-plan file
    jw(wd / "plan.json", plan)
    rows, drift = conformance(plan, repo)
    rep = jw(wd / "conformance.json", {"plan": plan["title"], "items": rows, "files_outside_plan": drift})
    status = {r["id"]: r["status"] for r in rows}
    looks_right = all((repo / f).exists() for f in plan["only_files"])
    return [
        check("item-by-item verdicts: 1,2,4 conform, 3 is a gap", status == {"1": "conforms", "2": "conforms", "3": "gap", "4": "conforms"},
              status, {"1": "conforms", "2": "conforms", "3": "gap", "4": "conforms"}),
        check("gap evidence is the observed output", [r["observed"] for r in rows if r["id"] == "3"] == ["hello-world"],
              [r["observed"] for r in rows if r["id"] == "3"], ["hello-world"]),
        check("drift: file outside 'only these files' caught", drift == ["notes_debug.txt"], drift, ["notes_debug.txt"]),
        check("negative control: a 'does it look right' check (planned files exist) passes and misses the gap",
              looks_right and status["3"] == "gap", looks_right, True),
    ], [rep]


# ---------------------------------------------------------------- 11569 planning-flow: the plan file contract
PLAN_SECTIONS = ["The ask", "Summary", "The problem", "The solution", "Technical context", "Tickets", "Decisions",
                 "Gotchas and caveats", "Out of scope", "Open questions"]
HISTORY = r"\b(previously|earlier version|we changed|was changed|in the last revision|v\d of (this|the) plan|updated:|no longer|now we)\b"


def plan_contract(md):
    issues = []
    heads = re.findall(r"^## (.+)$", md, re.M)
    top = [h for h in heads if h in PLAN_SECTIONS]
    if top != PLAN_SECTIONS:
        issues.append("sections missing or out of order")
    secs = re.split(r"^## ", md, flags=re.M)
    for s in secs[1:]:
        name, _, body = s.partition("\n")
        if name in PLAN_SECTIONS and not body.strip():
            issues.append("empty section without a one-line note: " + name)
        if name == "Summary" and re.search(r"`|\b\w+_\w+\b|\w+\(\)", body):
            issues.append("identifier in Summary")
    for m in re.finditer(HISTORY, md, re.I):
        issues.append("history narration: " + m.group(0))
    if not md.startswith("# "):
        issues.append("no imperative title")
    tickets = re.findall(r"^### Ticket: (.+?) \(depends on: (.*?)\)$", md, re.M)
    seen = set()
    for t, dep in tickets:
        for d in [x.strip() for x in dep.split(",") if x.strip() and x.strip() != "none"]:
            if d not in seen:
                issues.append("ticket before its dependency: " + t)
        seen.add(t)
    return issues


@card(K("2860-planning-flow/11569-planning-flow"))
def planning_flow(task, wd):
    spec = {"title": "Add a per-supplier switch for the drop-off check", "ask": "Let ops turn off the drop-off check for one supplier.",
            "quote": "we need to switch the drop-off check off for Acme without touching the others",
            "summary": "Today the drop-off check runs for every supplier. We add a per-supplier switch, on by default. Afterwards ops can turn it off for one supplier.",
            "problem": "The drop-off check (the step that rejects orders with no drop-off address) blocks Acme orders that carry the address in a free-text note.",
            "solution": "Each supplier record gets a yes/no setting, read when the check starts; when it is off the check is skipped and logged.",
            "context": "Supplier records live in the `suppliers` table (columns `id`, `name`); the check is `check_dropoff(order)` in `orders/checks.py`.",
            "tickets": [("Add the supplier setting", "none"), ("Skip the check when the setting is off", "Add the supplier setting")],
            "decisions": "Default on — chosen over default off, because existing suppliers must keep today's behaviour.",
            "gotchas": "A supplier switched off loses the check entirely; the log line is the only trace."}
    L = ["# " + spec["title"], "", "## The ask", "", spec["ask"], "", "> " + spec["quote"], "", "## Summary", "", spec["summary"], "",
         "## The problem", "", spec["problem"], "", "## The solution", "", spec["solution"], "", "## Technical context", "", spec["context"], "",
         "## Tickets", ""]
    for t, dep in spec["tickets"]:
        L += ["### Ticket: %s (depends on: %s)" % (t, dep), "#### Acceptance Criteria", "- observable outcome for: " + t, ""]
    L += ["## Decisions", "", spec["decisions"], "", "## Gotchas and caveats", "", spec["gotchas"], "", "## Out of scope", "",
          "Nothing ruled out.", "", "## Open questions", "", "No open questions.", ""]
    md = "\n".join(L)
    out = wt(wd / "PLAN.md", md)
    issues = plan_contract(md)
    revised = md.replace(spec["summary"], "Previously we planned a global flag; we changed it. `check_dropoff()` now reads supplier_flag.")
    revised = revised.replace("### Ticket: Add the supplier setting (depends on: none)", "### Ticket: Add the supplier setting (depends on: Skip the check when the setting is off)")
    bad = plan_contract(revised)
    jw(wd / "contract.json", {"plan": issues, "revised_with_history": bad})
    kinds = sorted({b.split(":")[0] for b in bad})
    return [
        check("plan file meets the template contract (fixed order, timeless, identifiers kept out of Summary)", issues == [], issues, []),
        check("tickets ordered dependencies-first", md.index("Add the supplier setting (") < md.index("Skip the check"), True, True),
        check("negative control: a revision that narrates its past fails history, identifier and ordering rules",
              kinds == ["history narration", "identifier in Summary", "ticket before its dependency"], kinds,
              ["history narration", "identifier in Summary", "ticket before its dependency"]),
    ], [out]


# ---------------------------------------------------------------- 11572 use Claude limits efficiently
def parse_usage(text):
    out = {}
    for line in text.splitlines():
        m = re.search(r"(Current session|Current week \(all models\)|Current week \(Opus\))\D*(\d+(?:\.\d+)?)%.*?[Rr]esets? (?:at |in )?(.+)$", line)
        if m:
            out[m.group(1)] = {"pct": float(m.group(2)), "reset": m.group(3).strip()}
    return out


def limits_decision(usage, now_s, reset_s, threshold=95.0, wave=3):
    over = sorted(k for k, v in usage.items() if v["pct"] >= threshold)
    if not over:
        return {"action": "launch next wave", "max_parallel": wave, "over": []}
    secs = max(0, reset_s - now_s)
    chain = []
    left = secs
    while left > 0:
        step = min(3600, left)
        chain.append(step)
        left -= step
    return {"action": "pause", "over": over, "wake_in_s": chain[0], "chain": chain, "max_parallel": 0}


@card(K("2863-use-claude-limits-efficiently/11572-use-claude-limits-efficiently"))
def claude_limits(task, wd):
    usage_txt = ("Current session  ████████████████████ 96% used · Resets at 3:40pm (Europe/Berlin)\n"
                 "Current week (all models)  ███████ 41% used · Resets Nov 9, 9am\n"
                 "Current week (Opus)  ██ 12% used · Resets Nov 9, 9am\n")
    wt(wd / "usage.txt", usage_txt)
    usage = parse_usage(usage_txt)
    now, reset = 12 * 3600 + 5 * 60, 15 * 3600 + 40 * 60  # 12:05 → 15:40 = 12900 s
    dec = limits_decision(usage, now, reset)
    prompt = ("Resume: remaining plan = waves 3-4 of the migration. Rule: run `claude -p \"/usage\"`; if session or weekly >= 95%% "
              "reschedule min(3600, seconds until reset) and stop; else launch at most 3 parallel subagents. Previous session reset: %s. "
              "Next verification: pytest -q. Next wave handoff packets: tickets 7-9 (scope, verify command, stop conditions)."
              % usage["Current session"]["reset"])
    need = ["remaining plan", "95%", "3 parallel", "/usage", "Previous session reset", "Next verification", "handoff packets"]
    missing = [n for n in need if n not in prompt]
    rep = jw(wd / "limits_decision.json", {"usage": usage, "decision": dec, "wake_prompt": prompt, "missing_fields": missing})
    calm = limits_decision({"Current session": {"pct": 60.0, "reset": "x"}}, now, reset)
    naive_wake = reset - now  # a single long sleep: hosts clamp wake delays to 3600 s
    return [
        check("usage figures read from the host report", [usage[k]["pct"] for k in sorted(usage)] == [96.0, 12.0, 41.0],
              [usage[k]["pct"] for k in sorted(usage)], [96.0, 12.0, 41.0]),
        check("95% rule pauses on the session window only", dec["action"] == "pause" and dec["over"] == ["Current session"], dec["over"], ["Current session"]),
        check("chained wakeups: 3600 + 3600 + 3600 + 2100 s = 12900 s", dec["chain"] == [3600, 3600, 3600, 2100], dec["chain"], [3600, 3600, 3600, 2100]),
        check("wake prompt is self-contained (all 7 fields)", missing == [], missing, []),
        check("below threshold: launch a wave of at most 3", calm == {"action": "launch next wave", "max_parallel": 3, "over": []}, calm, "launch 3"),
        check("negative control: one unchained wake would exceed the 3600 s clamp", naive_wake > 3600, naive_wake, ">3600"),
    ], [rep]


# ---------------------------------------------------------------- 11600 intended vs implemented
def intent_audit(docs_md, app_src):
    claims = {}
    for m in re.finditer(r"^\|\s*`(\w+)\s+(/[^`]*)`\s*\|\s*([\w-]+)\s*\|\s*(\w+)\s*\|", docs_md, re.M):
        claims[(m.group(1), m.group(2))] = {"role": m.group(3), "tenant_scoped": m.group(4) == "yes"}
    tree = ast.parse(app_src)
    impl = {}
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        route, role = None, None
        for d in fn.decorator_list:
            if isinstance(d, ast.Call) and getattr(d.func, "attr", getattr(d.func, "id", "")) in ("get", "post", "delete"):
                route = (d.func.attr.upper(), d.args[0].value)
            if isinstance(d, ast.Call) and getattr(d.func, "id", "") == "require_role":
                role = d.args[0].value
        if route:
            src = ast.get_source_segment(app_src, fn)
            impl[route] = {"role": role, "tenant_filter": "tenant_id" in src and "query(" in src
                           and bool(re.search(r"tenant_id\s*=\s*user\.tenant_id", src)), "line": fn.lineno, "name": fn.name}
    finds = []
    for r, c in claims.items():
        i = impl.get(r)
        if not i:
            finds.append({"route": " ".join(r), "kind": "documented route missing in code"})
            continue
        if c["role"] != "public" and i["role"] != c["role"]:
            finds.append({"route": " ".join(r), "kind": "documented-but-unenforced role", "intent": c["role"], "implemented": i["role"],
                          "evidence": "app.py:%d %s" % (i["line"], i["name"]), "fix": "add @require_role(%r)" % c["role"]})
        if c["tenant_scoped"] and not i["tenant_filter"]:
            finds.append({"route": " ".join(r), "kind": "tenant boundary not enforced", "evidence": "app.py:%d %s" % (i["line"], i["name"]),
                          "fix": "filter query by tenant_id=user.tenant_id"})
    for r, i in impl.items():
        if r not in claims:
            finds.append({"route": " ".join(r), "kind": "undocumented (docs stale)"})
    return claims, impl, finds


@card(K("2876-pm-ai-shipping/11600-intended-vs-implemented"))
def intended_vs_implemented(task, wd):
    docs = """# permissions.md
| route | role | tenant scoped |
|---|---|---|
| `GET /invoices` | member | yes |
| `GET /admin/export` | admin | no |
| `POST /invoices` | member | yes |
| `GET /health` | public | no |
"""
    app = '''app = App()

@app.get("/invoices")
@require_role("member")
def list_invoices(user):
    return db.query(Invoice, tenant_id=user.tenant_id)

@app.get("/admin/export")
def export_all(user):  # "admin only" per comment, but no check
    return db.query(Invoice)

@app.post("/invoices")
@require_role("member")
def create_invoice(user, body):
    return db.query(Invoice).insert(body)

@app.get("/health")
def health(user):
    return "ok"

@app.get("/debug/env")
def debug_env(user):
    return dict(os.environ)
'''
    wt(wd / "documentation/permissions.md", docs)
    wt(wd / "app.py", app)
    claims, impl, finds = intent_audit(docs, app)
    rep = jw(wd / "gap_audit.json", {"claims": {" ".join(k): v for k, v in claims.items()}, "findings": finds})
    got = sorted((f["route"], f["kind"]) for f in finds)
    want = sorted([("GET /admin/export", "documented-but-unenforced role"), ("POST /invoices", "tenant boundary not enforced"),
                   ("GET /debug/env", "undocumented (docs stale)")])
    safe_app = app.replace('def export_all', '@require_role("admin")\ndef export_all').replace(
        "db.query(Invoice).insert(body)", "db.query(Invoice, tenant_id=user.tenant_id).insert(body)").split("@app.get(\"/debug/env\")")[0]
    _, _, after = intent_audit(docs, safe_app)
    _, _, nodoc = intent_audit("", app)
    return [
        check("the 3 planted intent gaps found with doc + code evidence", got == want, got, want),
        check("every role finding cites file:line and a concrete fix", all("evidence" in f and "fix" in f for f in finds if "role" in f["kind"]), True, True),
        check("after the fixes the audit is clean", after == [], after, []),
        check("negative control: the same scan without documented intent finds none of the role/tenant gaps",
              [f for f in nodoc if f["kind"] != "undocumented (docs stale)"] == [], [f["kind"] for f in nodoc], "only 'undocumented' rows"),
    ], [rep]


# ---------------------------------------------------------------- 11619 user stories / 11620 WWA: generator + INVEST lint
VAGUE_AC = r"\b(fast|easy|user-friendly|intuitive|properly|appropriately|etc|nice|good)\b"


def story_lint(s):
    issues = []
    if not re.fullmatch(r"As an? [^,]+, I want to [^,]+, so that .+\.", s.get("description", "")):
        issues.append("description not 'As a…, I want to…, so that…'")
    n = len(s.get("ac", []))
    if not 4 <= n <= 6:
        issues.append("acceptance criteria count %d" % n)
    for a in s.get("ac", []):
        if re.search(VAGUE_AC, a, re.I):
            issues.append("untestable criterion: " + a)
    if re.search(r"\b(after|depends on|requires) story\b", json.dumps(s), re.I):
        issues.append("not independent")
    if not s.get("design", "").startswith("http"):
        issues.append("no design link")
    return issues


@card(K("2878-pm-execution/11619-user-stories"))
def user_stories(task, wd):
    feat = {"product": "ShopX", "design": "https://figma.example/recent", "roles": ["online shopper"],
            "journeys": [{"action": "see a 'Recently viewed' section on the product page", "benefit": "I can revisit items I considered",
                          "ac": ["The section shows at the bottom of the product page for users who viewed at least 1 product.",
                                 "It is not shown on the first product page of a session.",
                                 "The current product is excluded from the items shown.",
                                 "Each card shows image, title, price and 'Viewed N minutes ago'.",
                                 "Clicking a card opens that product page."]},
                         {"action": "clear my recently viewed list", "benefit": "my browsing stays private on a shared device",
                          "ac": ["A 'Clear' link appears in the section header.", "Clicking it removes every item from the section.",
                                 "After clearing, the section is hidden until a new product is viewed.",
                                 "The clear action is reachable by keyboard and has an accessible name."]}]}
    stories = []
    for j in feat["journeys"]:
        stories.append({"title": j["action"][0].upper() + j["action"][1:], "design": feat["design"], "ac": j["ac"],
                        "description": "As an %s, I want to %s, so that %s." % (feat["roles"][0], j["action"], j["benefit"])})
    md = "\n\n".join("**Title:** %s\n\n**Description:** %s\n\n**Design:** %s\n\n**Acceptance Criteria:**\n%s" %
                     (s["title"], s["description"], s["design"], "\n".join("%d. %s" % (i, a) for i, a in enumerate(s["ac"], 1))) for s in stories)
    out = wt(wd / "stories.md", md + "\n")
    lints = [story_lint(s) for s in stories]
    bad = {"title": "Recent", "description": "Recently viewed should be fast and easy", "design": "", "ac": ["Works properly", "Depends on story 3"]}
    bl = story_lint(bad)
    jw(wd / "lint.json", {"stories": lints, "bad": bl})
    return [
        check("2 stories generated, each passes the 3C/INVEST lint", lints == [[], []], lints, [[], []]),
        check("negative control: the vague story fails template, count, testability, independence, design", len(bl) == 5, bl, "5 issues"),
    ], [out]


def wwa_lint(it):
    issues = []
    why = [x for x in re.split(r"(?<=\.)\s+", it.get("why", "").strip()) if x]
    if not 1 <= len(why) <= 2:
        issues.append("why must be 1-2 sentences")
    if not re.search(r"\b(goal|objective|OKR|strategy|supports)\b", it.get("why", ""), re.I):
        issues.append("why not tied to an objective")
    if len([p for p in it.get("what", "").split("\n\n") if p.strip()]) > 2 or "http" not in it.get("what", ""):
        issues.append("what over 2 paragraphs or no design link")
    acs = it.get("ac", [])
    if not 3 <= len(acs) <= 6:
        issues.append("acceptance count %d" % len(acs))
    for a in acs:
        if re.search(VAGUE_AC, a, re.I) or not re.search(r"\d|visible|shown|displays|can |updates|rejects|handles", a, re.I):
            issues.append("not observable: " + a)
    return issues


@card(K("2878-pm-execution/11620-wwas"))
def wwas(task, wd):
    items = [{"title": "Implement Real-Time Spending Tracker",
              "why": "Users need immediate feedback on spending to make budget decisions. This supports our goal to reduce overspending.",
              "what": "Add a tracker that updates as users log expenses, showing this week's spend against budget. Designs: https://figma.example/tracker",
              "ac": ["Spending totals update within 2 seconds of logging an expense", "Budget progress is shown as a progress bar",
                     "Remaining budget is visible at a glance", "System handles multiple expense categories correctly"]},
             {"title": "Weekly budget reset reminder", "why": "Supports the retention objective by bringing users back each Monday.",
              "what": "Send a push reminder on Monday 9:00 local time. Design: https://figma.example/reminder",
              "ac": ["Reminder displays at 09:00 local time on Mondays", "Users can turn the reminder off in settings",
                     "Tapping it opens the weekly budget screen within 1 second"]}]
    md = "\n\n".join("**Title:** %s\n\n**Why:** %s\n\n**What:** %s\n\n**Acceptance Criteria:**\n%s" %
                     (i["title"], i["why"], i["what"], "\n".join("- " + a for a in i["ac"])) for i in items)
    out = wt(wd / "wwa.md", md + "\n")
    lints = [wwa_lint(i) for i in items]
    bad = {"title": "Tracker", "why": "Because. It is cool. Everyone wants it.", "what": "Build it.", "ac": ["It is fast", "Nice UI"]}
    bl = wwa_lint(bad)
    jw(wd / "lint.json", {"items": lints, "bad": bl})
    return [
        check("both WWA items pass the Why/What/Acceptance lint", lints == [[], []], lints, [[], []]),
        check("negative control: the vague item fails all five rules", len(bl) == 6, bl, "6 issues"),
    ], [out]


# ---------------------------------------------------------------- 11630 market sizing
def size_market(m):
    td = m["industry_revenue"] * m["segment_share"]
    bu = m["target_customers"] * m["price"] * m["purchases_per_year"]
    gap = abs(td - bu) / max(td, bu)
    tam = (td + bu) / 2
    sam = tam * m["serviceable_share"]
    som = sam * m["obtainable_share"]
    proj = {k: v * (1 + m["cagr"]) ** m["years"] for k, v in (("TAM", tam), ("SAM", sam), ("SOM", som))}
    return {"top_down": td, "bottom_up": bu, "divergence": gap, "reconciled_TAM": tam, "SAM": sam, "SOM": som,
            "projection": proj, "wide_interval": gap > 0.25}


@card(K("2880-pm-market-research/11630-market-sizing"))
def market_sizing(task, wd):
    m = {"market": "B2B invoice-automation SaaS, DACH SMEs", "industry_revenue": 2_000_000_000, "segment_share": 0.10,
         "target_customers": 50_000, "price": 300.0, "purchases_per_year": 12, "serviceable_share": 0.40, "obtainable_share": 0.05,
         "cagr": 0.10, "years": 3,
         "assumptions": [{"n": 1, "text": "10% of EU AP-software spend is DACH SME", "confidence": "low", "kind": "estimate"},
                         {"n": 2, "text": "50k SMEs with >20 invoices/month", "confidence": "medium", "kind": "estimate"},
                         {"n": 3, "text": "EUR 300 per month list price", "confidence": "high", "kind": "data (price list)"}]}
    r = size_market(m)
    table = "| Metric | Current | %d-year |\n|---|---|---|\n" % m["years"] + "\n".join(
        "| %s | %.0f | %.0f |" % (k, r["reconciled_TAM"] if k == "TAM" else r[k], r["projection"][k]) for k in ("TAM", "SAM", "SOM"))
    out = wt(wd / "market_size.md", "# Market size: %s\n\n%s\n\nTop-down %.0f vs bottom-up %.0f (divergence %.1f%%).\n" %
             (m["market"], table, r["top_down"], r["bottom_up"], 100 * r["divergence"]))
    jw(wd / "market_size.json", {"inputs": m, "result": r})
    one_sided = {"top_down": r["top_down"]}
    return [
        check("top-down 200M and bottom-up 180M", (r["top_down"], r["bottom_up"]) == (200_000_000, 180_000_000), [r["top_down"], r["bottom_up"]], [2e8, 1.8e8]),
        check("reconciled TAM 190M, SAM 76M, SOM 3.8M", [round(r["reconciled_TAM"]), round(r["SAM"]), round(r["SOM"])] == [190_000_000, 76_000_000, 3_800_000],
              [round(r["reconciled_TAM"]), round(r["SAM"]), round(r["SOM"])], [190000000, 76000000, 3800000]),
        check("3-year TAM at 10% CAGR = 252.89M", abs(r["projection"]["TAM"] - 252_890_000) < 1, r["projection"]["TAM"], 252890000),
        check("divergence 10% < 25%: no wide-interval flag", abs(r["divergence"] - 0.10) < 1e-9 and not r["wide_interval"], r["divergence"], 0.10),
        check("every assumption labelled estimate vs data with confidence", all(a["confidence"] and a["kind"] for a in m["assumptions"]), True, True),
        check("negative control: a top-down-only estimate has no triangulation", "bottom_up" not in one_sided, list(one_sided), ["top_down"]),
    ], [out]


# ---------------------------------------------------------------- 11640 / 11641 experiments
def two_prop_z(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se
    pval = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return z, pval


def wilson(x, n, z=1.96):
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


OPINION = r"\b(would you|said they|survey says|liked|interested|rated)\b"
METHOD = {"desirability": "fake door test", "usability": "first-click test on a prototype", "feasibility": "technical spike",
          "value": "A/B test on production"}


@card(K("2882-pm-product-discovery/11640-brainstorm-experiments-existing"))
def experiments_existing(task, wd):
    assumptions = [
        {"id": "A1", "type": "desirability", "belief": "users want CSV export", "metric": "clicks on the Export button / dashboard visitors", "threshold": 0.05},
        {"id": "A2", "type": "usability", "belief": "users find export in the menu", "metric": "first click lands on Export within 10 s", "threshold": 0.80},
        {"id": "A3", "type": "feasibility", "belief": "export of 100k rows runs under 5 s", "metric": "p95 export seconds", "threshold": 5.0},
        {"id": "A4", "type": "value", "belief": "export raises weekly retention", "metric": "week-2 retention, control vs variant", "threshold": 0.02,
         "mitigation": "5% traffic, kill switch, no data loss path"},
    ]
    plan = []
    for a in assumptions:
        e = {"assumption": a["belief"], "experiment": METHOD[a["type"]], "metric": a["metric"], "success_threshold": a["threshold"]}
        if e["experiment"].startswith("A/B"):
            e["risk_mitigation"] = a.get("mitigation")
        plan.append(e)
    # analyse the A/B result: control 400/2000 retained, variant 470/2000
    z, p = two_prop_z(400, 2000, 470, 2000)
    lift = 470 / 2000 - 400 / 2000
    verdict = "validated" if lift >= 0.02 and p < 0.05 else "not validated"
    md = "| Assumption | Experiment | Metric | Threshold |\n|---|---|---|---|\n" + "\n".join(
        "| %s | %s | %s | %s |" % (e["assumption"], e["experiment"], e["metric"], e["success_threshold"]) for e in plan)
    out = wt(wd / "experiments.md", md + "\n\nA/B result: lift %.3f, z=%.3f, p=%.4f → %s\n" % (lift, z, p, verdict))
    jw(wd / "experiments.json", {"plan": plan, "ab": {"z": z, "p": p, "lift": lift, "verdict": verdict}})
    behaviour = all(not re.search(OPINION, e["metric"], re.I) for e in plan)
    opinion_plan = {"metric": "share of surveyed users who said they would use export"}
    return [
        check("one experiment per assumption, method fits the assumption type",
              [e["experiment"] for e in plan] == ["fake door test", "first-click test on a prototype", "technical spike", "A/B test on production"],
              [e["experiment"] for e in plan], "4 methods"),
        check("production A/B carries risk mitigation", plan[3].get("risk_mitigation") is not None, plan[3].get("risk_mitigation"), "present"),
        check("A/B analysis: lift 3.5 pts, z = 2.683, p < 0.01 → validated", abs(z - 2.683) < 0.005 and p < 0.01 and verdict == "validated",
              [round(z, 3), round(p, 4), verdict], [2.683, "<0.01", "validated"]),
        check("all metrics measure behaviour, not opinion", behaviour, behaviour, True),
        check("negative control: an opinion-survey metric is rejected", bool(re.search(OPINION, opinion_plan["metric"], re.I)), True, True),
    ], [out]


@card(K("2882-pm-product-discovery/11641-brainstorm-experiments-new"))
def experiments_new(task, wd):
    hyp = "At least 10% of mid-size luxury sedan buyers will pre-order the rental-subscription plan"
    m = re.fullmatch(r"At least (\d+(?:\.\d+)?)% of (.+?) will (.+)", hyp)
    x, y, zz = float(m.group(1)) / 100, m.group(2), m.group(3)
    pretotypes = [
        {"method": "Landing Page", "metric": "sign-ups / visitors", "hits": 132, "n": 1000, "skin_in_game": False},
        {"method": "Pre-Order / Waitlist", "metric": "refundable 50 EUR deposits / visitors", "hits": 64, "n": 1000, "skin_in_game": True},
        {"method": "Explainer Video", "metric": "watched to end / viewers", "hits": 410, "n": 1000, "skin_in_game": False},
    ]
    for p in pretotypes:
        p["rate"] = p["hits"] / p["n"]
        p["ci95"] = wilson(p["hits"], p["n"])
        p["meets_X"] = p["ci95"][0] >= x
    decisive = [p for p in pretotypes if p["skin_in_game"]]
    verdict = "supported" if decisive and all(p["meets_X"] for p in decisive) else "not supported (YODA: own data says no)"
    rep = jw(wd / "xyz.json", {"hypothesis": {"X": x, "Y": y, "Z": zz}, "pretotypes": pretotypes, "verdict": verdict})
    lo, hi = pretotypes[1]["ci95"]
    interest_only = pretotypes[0]["rate"] >= x
    return [
        check("XYZ hypothesis parsed", (x, y, zz) == (0.10, "mid-size luxury sedan buyers", "pre-order the rental-subscription plan"), [x, y, zz], [0.1, y, zz]),
        check("deposit rate 6.4%, Wilson 95% CI [5.04%, 8.10%]", abs(lo - 0.0504) < 0.0005 and abs(hi - 0.0810) < 0.0005, [round(lo, 4), round(hi, 4)], [0.0504, 0.0810]),
        check("skin-in-the-game result decides: hypothesis not supported", verdict.startswith("not supported"), verdict, "not supported"),
        check("negative control: the interest-only landing-page rate (13.2%) would wrongly pass X", interest_only, pretotypes[0]["rate"], ">=0.10"),
    ], [rep]


# ---------------------------------------------------------------- 11650 prioritize features
@card(K("2882-pm-product-discovery/11650-prioritize-features"))
def prioritize_features(task, wd):
    feats = [  # importance/satisfaction on 1-10, customers, confidence 0-1, ease 1-10
        ("Bulk edit", 9, 2, 800, 0.8, 6), ("Dark mode", 4, 6, 3000, 0.9, 9), ("SSO", 8, 3, 400, 0.7, 4),
        ("CSV export", 7, 2, 1000, 0.9, 8), ("Offline mode", 6, 1, 300, 0.5, 2), ("Audit log", 8, 4, 500, 0.8, 7),
        ("Emoji reactions", 2, 5, 2000, 0.9, 9),
    ]
    rows = []
    for name, imp, sat, cust, conf, ease in feats:
        opp = (imp / 10) * (1 - sat / 10)
        impact = opp * cust
        rows.append({"feature": name, "opportunity": round(opp, 4), "ice": round(impact * conf * ease, 2)})
    ranked = sorted(rows, key=lambda r: r["ice"], reverse=True)
    top, rest = ranked[:5], ranked[5:]
    md = "| Rank | Feature | Opportunity | ICE |\n|---|---|---|---|\n" + "\n".join(
        "| %d | %s | %.3f | %.1f |" % (i, r["feature"], r["opportunity"], r["ice"]) for i, r in enumerate(top, 1))
    md += "\n\nDeprioritized: " + ", ".join("%s (ICE %.1f)" % (r["feature"], r["ice"]) for r in rest) + "\n"
    out = wt(wd / "priorities.md", md)
    jw(wd / "priorities.json", {"ranked": ranked})
    order = [r["feature"] for r in top]
    by_reach = [f[0] for f in sorted(feats, key=lambda f: f[3], reverse=True)][:5]
    return [
        check("Opportunity Score bulk edit = 0.9 x 0.8 = 0.72", rows[0]["opportunity"] == 0.72, rows[0]["opportunity"], 0.72),
        check("ICE top 5 in order", order == ["CSV export", "Dark mode", "Bulk edit", "Emoji reactions", "Audit log"], order,
              ["CSV export", "Dark mode", "Bulk edit", "Emoji reactions", "Audit log"]),
        check("CSV export ICE = 0.56*1000*0.9*8 = 4032", ranked[0]["ice"] == 4032.0, ranked[0]["ice"], 4032.0),
        check("deprioritized list with reasons", [r["feature"] for r in rest] == ["SSO", "Offline mode"], [r["feature"] for r in rest], ["SSO", "Offline mode"]),
        check("negative control: ranking by raw customer count gives a different top 5", by_reach != order, by_reach, "!= ICE order"),
    ], [out]


# ---------------------------------------------------------------- 12141 pnpm workspace (offline, workspace protocol)
@card(K("2926-pnpm/12141-pnpm"))
def pnpm_workspace(task, wd):
    if not fx.which("pnpm"):
        raise RuntimeError("pnpm missing")
    ws = wd / "ws"
    wt(ws / "pnpm-workspace.yaml", 'packages:\n  - "packages/*"\nlinkWorkspacePackages: true\n')
    wt(ws / "package.json", json.dumps({"name": "root", "private": True}))
    wt(ws / "packages/core/package.json", json.dumps({"name": "@w/core", "version": "1.0.0", "main": "index.js",
                                                       "scripts": {"build": "node build.js"}}))
    wt(ws / "packages/core/index.js", "module.exports = (s) => s.toUpperCase();\n")
    wt(ws / "packages/core/build.js", "require('fs').writeFileSync('built.txt', String(Date.now()));\n")
    wt(ws / "packages/app/package.json", json.dumps({"name": "@w/app", "version": "1.0.0", "dependencies": {"@w/core": "workspace:*"},
                                                      "scripts": {"build": "node run.js"}}))
    wt(ws / "packages/app/run.js", "const fs=require('fs');const up=require('@w/core');\n"
       "fs.writeFileSync('out.txt', up('ok') + ' core-built-first=' + fs.existsSync('../core/built.txt'));\n")
    pre = sh(["node", "run.js"], cwd=ws / "packages/app", ok=False)
    env = {"npm_config_offline": "true", "CI": "1"}
    sh(["pnpm", "install", "--offline"], cwd=ws, env=env, timeout=60)
    sh(["pnpm", "-r", "run", "build"], cwd=ws, env=env, timeout=60)
    lock = (ws / "pnpm-lock.yaml").read_text()
    link = os.readlink(ws / "packages/app/node_modules/@w/core")
    result = (ws / "packages/app/out.txt").read_text()
    lsd = sh(["pnpm", "-r", "list", "--json", "--depth", "0"], cwd=ws, env=env, ok=False)
    try:
        lst = json.loads(lsd.stdout or "[]")
    except ValueError:
        lst = []
    rep = jw(wd / "pnpm_report.json", {"lock_has_link": "link:../core" in lock, "symlink": link, "app_output": result,
                                       "projects": sorted(p.get("name") for p in lst), "pnpm": sh(["pnpm", "--version"]).stdout.strip()})
    return [
        check("workspace:* resolved to a link in the shared lockfile", "version: link:../core" in lock, "link:../core" in lock, True),
        check("app's node_modules symlinks the sibling package", link.endswith("core"), link, "../../core"),
        check("pnpm -r ran builds in dependency order (core before app)", result == "OK core-built-first=true", result, "OK core-built-first=true"),
        check("negative control: before pnpm install the app cannot resolve @w/core", pre.returncode != 0 and "Cannot find module" in pre.stderr,
              pre.returncode, "non-zero"),
    ], [rep, ws / "pnpm-lock.yaml"]


# ---------------------------------------------------------------- 12220 vite library build
@card(K("2948-vite/12220-vite"))
def vite_build(task, wd):
    proj = wd / "lib"
    wt(proj / "package.json", json.dumps({"name": "mini-lib", "version": "0.0.1"}))
    wt(proj / "src/math.ts", "export const add = (a: number, b: number): number => a + b\nexport const neverUsed = (): string => 'tree-shake-me'\n")
    wt(proj / "src/main.ts", "import { add } from './math'\nexport const sum3 = (a: number, b: number, c: number): number => add(add(a, b), c)\n"
       "export const mode: string = import.meta.env.MODE\n")
    vite_js = NM / "vite/dist/node/index.js"
    wt(proj / "vite.config.ts", "import { defineConfig } from %s\nexport default defineConfig({\n  build: {\n"
       "    lib: { entry: 'src/main.ts', formats: ['es', 'cjs'], fileName: (f) => (f === 'es' ? 'mini.mjs' : 'mini.cjs') },\n    minify: false,\n  },\n})\n"
       % json.dumps(str(vite_js)))
    sh(["node", str(NM / "vite/bin/vite.js"), "build", "--logLevel", "error"], cwd=proj, timeout=90)
    es = (proj / "dist/mini.mjs").read_text()
    cjs = proj / "dist/mini.cjs"
    val = sh(["node", "-e", "const m=require(%s);console.log(JSON.stringify([m.sum3(1,2,3),m.mode]))" % json.dumps(str(cjs))]).stdout
    esm = sh(["node", "--input-type=module", "-e", "import {sum3} from %s; console.log(sum3(2,2,2))" % json.dumps((proj / "dist/mini.mjs").as_uri())]).stdout
    rep = jw(wd / "vite_report.json", {"files": sorted(p.name for p in (proj / "dist").iterdir()), "cjs_result": json.loads(val), "esm_result": esm.strip()})
    src_has = "tree-shake-me" in (proj / "src/math.ts").read_text()
    return [
        check("CJS build runs: sum3(1,2,3)=6 and import.meta.env.MODE replaced with 'production'", json.loads(val) == [6, "production"], json.loads(val), [6, "production"]),
        check("ESM build runs: sum3(2,2,2)=6", esm.strip() == "6", esm.strip(), "6"),
        check("unused export tree-shaken out of the bundle", "tree-shake-me" not in es, "tree-shake-me" in es, False),
        check("negative control: the unbundled source still holds the dead code", src_has, src_has, True),
    ], [rep, cjs]


# ---------------------------------------------------------------- Vue (3.5 compiler-sfc + server-renderer, vue-router 5)
_VUE_TOOL = r"""
const {parse, compileScript} = require('@vue/compiler-sfc'); const ts = require(%(ts)s);
const {createSSRApp, h} = require('vue'); const {renderToString} = require('@vue/server-renderer'); const fs = require('fs'); const path = require('path');
const cache = {};
function load(file){
  if (cache[file]) return cache[file];
  const src = fs.readFileSync(file,'utf8'); const {descriptor, errors} = parse(src, {filename: path.basename(file)});
  if (errors.length) throw new Error(String(errors[0]));
  const s = compileScript(descriptor, {id: path.basename(file), inlineTemplate: true});
  const js = ts.transpileModule(s.content, {compilerOptions:{module:ts.ModuleKind.CommonJS, target:ts.ScriptTarget.ES2020}}).outputText;
  const m = {exports:{}}; const req = (n) => n.endsWith('.vue') ? {__esModule: true, default: load(path.join(path.dirname(file), n)).comp} : n.startsWith('./') ? loadTs(path.join(path.dirname(file), n)) : require(n);
  new Function('require','module','exports', js)(req, m, m.exports);
  const order = [...src.matchAll(/^<(script|template|style)\b([^>]*)>/gm)].map(x=>x[1]);
  const info = {order, setupTs: /<script setup lang="ts">/.test(src), propsType: (s.content.match(/props:[\s\S]*?(?=\n  emits:|\n  setup\()/)||[''])[0],
    vhtml: /v-html=/.test(src), vforNoKey: /v-for="[^"]*"(?![^>]*:key)/.test(src), watchToState: /(watch\s*:\s*\{[\s\S]{0,120}this\.\w+\s*=)|(watch\([^)]*\)[\s\S]{0,80}\.value\s*=)/.test(src),
    propsDestructure: /const \{[^}]*\} = defineProps/.test(src), sections: (src.match(/<section\b/g)||[]).length, emits: s.content.includes('emits:'),
    model: /defineModel/.test(src), bindings: s.bindings};
  cache[file] = {comp: m.exports.default, info}; return cache[file];
}
function loadTs(p){ const f = fs.existsSync(p) ? p : p + '.ts'; const js = ts.transpileModule(fs.readFileSync(f,'utf8'), {compilerOptions:{module:ts.ModuleKind.CommonJS, target:ts.ScriptTarget.ES2020}}).outputText;
  const m = {exports:{}}; new Function('require','module','exports', js)(require, m, m.exports); return m.exports; }
(async () => {
  const job = JSON.parse(process.argv[2]); const out = {};
  for (const [k, v] of Object.entries(job)) { const L = load(v.file); out[k] = {info: L.info};
    if (v.render) out[k].html = await renderToString(createSSRApp({render: () => h(L.comp, v.props || {})})); }
  console.log(JSON.stringify(out));
})().catch(e => { console.error(e && e.stack || e); process.exit(1); });
"""


def vue_tool(wd, job):
    src = wt(Path(wd) / "vue_tool.cjs", _VUE_TOOL % {"ts": json.dumps(str(NM / "typescript"))})
    done = sh(["node", str(src), json.dumps(job)], cwd=wd, env={"NODE_PATH": str(SLIDEV_NM)}, timeout=40)
    return json.loads(done.stdout.strip().splitlines()[-1])


def vue_findings(i):
    f = []
    if i["order"] != ["script", "template", "style"][:len(i["order"])] or (i["order"] and i["order"][0] != "script"):
        f.append("SFC order")
    if not i["setupTs"]:
        f.append("not <script setup lang=ts>")
    if i["vhtml"]:
        f.append("v-html")
    if i["vforNoKey"]:
        f.append("v-for without :key")
    if i["watchToState"]:
        f.append("derived state via watch")
    if i["sections"] >= 3:
        f.append("3+ UI sections in one component")
    return f


@card(K("2951-vue/12229-vue-best-practices"))
def vue_best_practices(task, wd):
    if not (SLIDEV_NM / "vue").exists():
        raise RuntimeError("vue runtime missing")
    mega = wt(wd / "bad/TodoApp.vue", """<template>
  <section><input v-model="draft" /><button @click="add">add</button></section>
  <section><ul><li v-for="t in todos">{{ t.text }}</li></ul></section>
  <section><p v-html="footer"></p></section>
</template>
<script>
export default { data(){ return { draft: '', todos: [], left: 0, footer: '' } },
  watch: { todos(v){ this.left = v.filter(t => !t.done).length } }, methods: { add(){ this.todos.push({text:this.draft}) } } }
</script>
<style>p{color:red}</style>
""")
    wt(wd / "good/TodoList.vue", """<script setup lang="ts">
defineProps<{ todos: { id: number; text: string; done: boolean }[] }>()
</script>

<template>
  <ul><li v-for="t in todos" :key="t.id">{{ t.text }}</li></ul>
</template>
""")
    wt(wd / "good/TodoFooter.vue", """<script setup lang="ts">
defineProps<{ left: number }>()
</script>

<template>
  <p>{{ left }} left</p>
</template>
""")
    feat = wt(wd / "good/TodoFeature.vue", """<script setup lang="ts">
import { computed } from 'vue'
import TodoList from './TodoList.vue'
import TodoFooter from './TodoFooter.vue'
const props = defineProps<{ todos: { id: number; text: string; done: boolean }[] }>()
const left = computed(() => props.todos.filter((t) => !t.done).length)
</script>

<template>
  <div><TodoList :todos="props.todos" /><TodoFooter :left="left" /></div>
</template>

<style scoped>
div { display: grid; }
</style>
""")
    todos = [{"id": 1, "text": "write", "done": True}, {"id": 2, "text": "ship", "done": False}, {"id": 3, "text": "rest", "done": False}]
    res = vue_tool(wd, {"good": {"file": str(feat), "render": True, "props": {"todos": todos}}, "bad": {"file": str(mega)}})
    fg, fb = vue_findings(res["good"]["info"]), vue_findings(res["bad"]["info"])
    html_out = re.sub(r' data-v-[^\s>=]+(="")?', "", re.sub(r"<!--.*?-->", "", res["good"]["html"]))
    out = jw(wd / "vue_review.json", {"good": fg, "bad": fb, "ssr": html_out})
    want_html = '<div><ul><li>write</li><li>ship</li><li>rest</li></ul><p>2 left</p></div>'
    return [
        check("feature split into container + list + footer passes every rule", fg == [], fg, []),
        check("SSR render: list items and computed 'left' count", html_out == want_html, html_out, want_html),
        check("negative control: the mega Options-API component trips 6 rules",
              fb == ["SFC order", "not <script setup lang=ts>", "v-html", "v-for without :key", "derived state via watch", "3+ UI sections in one component"],
              fb, "6 planted"),
    ], [out, feat]


@card(K("2951-vue/12232-vue"))
def vue_macros(task, wd):
    if not (SLIDEV_NM / "vue").exists():
        raise RuntimeError("vue runtime missing")
    comp = wt(wd / "Rating.vue", """<script setup lang="ts">
import { computed, shallowRef } from 'vue'
const props = defineProps<{ title: string; max?: number }>()
const emit = defineEmits<{ change: [value: number] }>()
const model = defineModel<number>({ default: 3 })
const history = shallowRef<number[]>([])
const stars = computed(() => '*'.repeat(model.value) + '-'.repeat((props.max ?? 5) - model.value))
function set(v: number) { model.value = v; history.value = [...history.value, v]; emit('change', v) }
defineExpose({ set })
</script>

<template>
  <p :title="props.title">{{ props.title }}: {{ stars }}</p>
</template>
""")
    bad = wt(wd / "Old.vue", """<template><p>{{ title }}</p></template>
<script setup>
const { title } = defineProps(['title'])
</script>
""")
    res = vue_tool(wd, {"rating": {"file": str(comp), "render": True, "props": {"title": "Food", "max": 5, "modelValue": 4}},
                        "old": {"file": str(bad)}})
    info = res["rating"]["info"]
    html_out = re.sub(r"<!--.*?-->", "", res["rating"]["html"])
    out = jw(wd / "vue_macros.json", res)
    pt = info["propsType"]
    typed = "title: { type: String, required: true }" in pt and "max: { type: Number, required: false }" in pt
    old = res["old"]["info"]
    return [
        check("defineProps<T>() compiled to runtime props with types and required flags", typed, pt[:160], "title String required, max Number optional"),
        check("defineModel + defineEmits compiled (modelValue prop, emits list)", "modelValue" in pt and info["emits"], ["modelValue" in pt, info["emits"]], [True, True]),
        check("SSR render from props + v-model value: 4 of 5 stars", html_out == '<p title="Food">Food: ****-</p>', html_out, '<p title="Food">Food: ****-</p>'),
        check("negative control: legacy file is not <script setup lang=ts> and destructures props",
              (not old["setupTs"]) and old["propsDestructure"], [old["setupTs"], old["propsDestructure"]], [False, True]),
    ], [out, comp]


@card(K("2951-vue/12230-vue-router-best-practices"))
def vue_router_bp(task, wd):
    if not (SLIDEV_NM / "vue-router").exists():
        raise RuntimeError("vue-router missing")
    js = r"""
const {createRouter, createMemoryHistory} = require('vue-router'); const {h} = require('vue');
const C = {render: () => h('div')};
const routes = [{path:'/', component:C}, {path:'/login', name:'login', component:C}, {path:'/dash', component:C, meta:{auth:true}},
  {path:'/profile', component:C}, {path:'/user/:id', component:C}];
async function go(guard, target){ const r = createRouter({history: createMemoryHistory(), routes}); r.beforeEach(guard);
  const warns = []; const w = console.warn; console.warn = (...a) => warns.push(a.join(' ')); let err = null;
  try { await r.push(target); } catch (e) { err = String(e.message || e); } console.warn = w;
  return {path: r.currentRoute.value.path, err, warned: warns.some(x => /infinite redirection/.test(x))}; }
const authed = false;
(async () => {
  const out = {};
  out.wrongAlways = await go(() => { if (!authed) return '/login'; }, '/dash');
  out.fixedExclude = await go((to) => { if (!authed && to.name !== 'login') return {name: 'login'}; }, '/dash');
  out.fixedMeta = await go((to) => { if (to.meta.auth && !authed) return {name: 'login', query: {redirect: to.fullPath}}; }, '/profile');
  let hops = 0;  // Vue Router does not detect an A<->B redirect cycle by itself: cap it so the probe terminates
  out.circular = await go((to) => { if (++hops > 50) return false; if (to.path === '/dash') return '/profile'; if (to.path === '/profile') return '/dash'; }, '/dash');
  out.circular.hops = hops;
  const r = createRouter({history: createMemoryHistory(), routes}); let enters = 0; r.beforeEach((to) => { if (to.path.startsWith('/user')) enters++; });
  await r.push('/user/1'); await r.push('/user/2'); out.paramChange = {path: r.currentRoute.value.path, guardRuns: enters};
  console.log(JSON.stringify(out));
})();
"""
    res = node(wd, "router_guards", js, node_path=SLIDEV_NM)
    guards_src = wt(wd / "guards.ts", "router.beforeEach((to, from, next) => {\n  if (!isAuthenticated()) next('/login')\n  else next()\n})\n")
    next_used = bool(re.search(r"beforeEach\(\s*\(\s*\w+\s*,\s*\w+\s*,\s*next\s*\)", guards_src.read_text()))
    out = jw(wd / "router_report.json", {**res, "deprecated_next_in_guards_ts": next_used})
    return [
        check("guard that excludes the target lands on /login with no loop", res["fixedExclude"] == {"path": "/login", "err": None, "warned": False},
              res["fixedExclude"], {"path": "/login", "err": None, "warned": False}),
        check("meta-scoped guard leaves unprotected /profile alone", res["fixedMeta"]["path"] == "/profile", res["fixedMeta"]["path"], "/profile"),
        check("global guard still runs on param change /user/1 -> /user/2", res["paramChange"] == {"path": "/user/2", "guardRuns": 2}, res["paramChange"], {"path": "/user/2", "guardRuns": 2}),
        check("deprecated next() guard detected in source", next_used, next_used, True),
        check("negative control: the unconditional redirect is aborted by Vue Router as an infinite redirection",
              res["wrongAlways"]["warned"] and res["wrongAlways"]["path"] == "/", res["wrongAlways"], "warned, stays on /"),
        check("negative control: the circular dashboard/profile guard redirects without end (stopped only by the probe's 50-hop cap)",
              res["circular"]["hops"] == 51 and res["circular"]["path"] == "/", res["circular"], "51 hops, never lands"),
    ], [out]


# ---------------------------------------------------------------- 12256 use zod (installed version first)
@card(K("2955-zod/12256-use-zod"))
def use_zod(task, wd):
    if not ZOD.exists():
        raise RuntimeError("zod missing")
    pkg = json.loads((ZOD / "package.json").read_text())
    js = r"""
const z = require(%(zod)s);
const Order = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  qty: z.coerce.number().int().positive(),
  sku: z.string().regex(/^[A-Z]{3}-\d{3}$/),
  note: z.string().trim().optional(),
  placed: z.string().transform((s) => new Date(s).toISOString()),
}).refine((o) => !(o.qty > 10 && !o.note), {message: 'bulk orders need a note', path: ['note']});
const good = Order.safeParse({id: '3f2b6f4e-8a1d-4c2b-9e1a-2b3c4d5e6f70', email: 'a@b.co', qty: '4', sku: 'ABC-123', note: '  hi  ', placed: '2026-11-03T10:00:00Z'});
const bad = Order.safeParse({id: 'nope', email: 'x', qty: '-2', sku: 'abc', placed: '2026-11-03T10:00:00Z'});
const bulk = Order.safeParse({id: '3f2b6f4e-8a1d-4c2b-9e1a-2b3c4d5e6f70', email: 'a@b.co', qty: 12, sku: 'ABC-123', placed: '2026-11-03T10:00:00Z'});
const tree = z.treeifyError(bad.error);
console.log(JSON.stringify({symbols: ['treeifyError','prettifyError','flattenError','codec'].map(k => typeof z[k]),
  good: good.success ? good.data : null, badPaths: bad.error.issues.map(i => i.path.join('.')).sort(),
  treeKeys: Object.keys(tree.properties || {}).sort(), pretty: z.prettifyError(bad.error).split('\n').length,
  bulk: bulk.success ? 'ok' : bulk.error.issues.map(i => i.path.join('.') + ':' + i.message)}));
""" % {"zod": json.dumps(str(ZOD))}
    res = node(wd, "zod_schema", js)
    out = jw(wd / "zod_report.json", {"installed_version": pkg["version"], "exports": sorted(pkg.get("exports", {}))[:12], **res})
    major = int(pkg["version"].split(".")[0])
    return [
        check("installed version read first: zod 4.x (v4 API branch)", major == 4, pkg["version"], "4.x"),
        check("v4 top-level helpers exist in the installed build", res["symbols"] == ["function"] * 4, res["symbols"], ["function"] * 4),
        check("valid input parsed with coercion, trim and transform",
              res["good"] == {"id": "3f2b6f4e-8a1d-4c2b-9e1a-2b3c4d5e6f70", "email": "a@b.co", "qty": 4, "sku": "ABC-123", "note": "hi",
                              "placed": "2026-11-03T10:00:00.000Z"}, res["good"], "coerced/trimmed/ISO"),
        check("refinement reports on its path", res["bulk"] == ["note:bulk orders need a note"], res["bulk"], ["note:bulk orders need a note"]),
        check("negative control: invalid input rejected on exactly the 4 bad fields, treeified",
              res["badPaths"] == ["email", "id", "qty", "sku"] and res["treeKeys"] == ["email", "id", "qty", "sku"], res["badPaths"], ["email", "id", "qty", "sku"]),
    ], [out]


# ---------------------------------------------------------------- 912 build an MCPB bundle (stdio MCP server + manifest + zip)
MCP_SERVER_JS = r"""
const fs = require('fs'); const path = require('path'); const readline = require('readline');
const ROOT = process.env.ROOT_DIR;
const rl = readline.createInterface({input: process.stdin});
const send = (o) => process.stdout.write(JSON.stringify(o) + '\n');
rl.on('line', (line) => {
  let m; try { m = JSON.parse(line); } catch { return; }
  if (m.method === 'initialize') return send({jsonrpc: '2.0', id: m.id, result: {protocolVersion: m.params.protocolVersion,
    capabilities: {tools: {}}, serverInfo: {name: 'local-files', version: '0.1.0'}}});
  if (m.method === 'notifications/initialized') return;
  if (m.method === 'tools/list') return send({jsonrpc: '2.0', id: m.id, result: {tools: [{name: 'list_files',
    description: 'List files in the configured root directory.', inputSchema: {type: 'object', properties: {}}}]}});
  if (m.method === 'tools/call') {
    const real = fs.realpathSync(ROOT);
    const names = fs.readdirSync(real).filter((n) => fs.statSync(path.join(real, n)).isFile()).sort();
    return send({jsonrpc: '2.0', id: m.id, result: {content: [{type: 'text', text: names.join('\n')}]}});
  }
  send({jsonrpc: '2.0', id: m.id, error: {code: -32601, message: 'Method not found'}});
});
"""


def mcpb_validate(manifest, names):
    issues = []
    for k in ("manifest_version", "name", "version", "description", "author", "server"):
        if k not in manifest:
            issues.append("missing " + k)
    srv = manifest.get("server", {})
    if srv.get("type") not in ("node", "python", "binary"):
        issues.append("server.type")
    ep = srv.get("entry_point")
    if not ep or ep not in names:
        issues.append("entry_point not in bundle")
    cfg = srv.get("mcp_config", {})
    for a in cfg.get("args", []):
        if a.startswith("/") or re.match(r"[A-Za-z]:\\", a):
            issues.append("absolute path in args: " + a)
    for v in list(cfg.get("env", {}).values()) + cfg.get("args", []):
        for ref in re.findall(r"\$\{user_config\.(\w+)\}", v):
            if ref not in manifest.get("user_config", {}):
                issues.append("undeclared user_config." + ref)
    for k, uc in manifest.get("user_config", {}).items():
        if re.search(r"(token|key|secret|password)", k, re.I) and not uc.get("sensitive"):
            issues.append("secret %s not sensitive" % k)
    return issues


@card(K("297-mcp-server-dev/912-build-mcpb"))
def build_mcpb(task, wd):
    src = wd / "src"
    wt(src / "server/index.js", MCP_SERVER_JS)
    manifest = {"manifest_version": "0.4", "name": "local-files", "version": "0.1.0", "description": "List files in a local folder.",
                "author": {"name": "KOSIF"}, "server": {"type": "node", "entry_point": "server/index.js",
                "mcp_config": {"command": "node", "args": ["${__dirname}/server/index.js"], "env": {"ROOT_DIR": "${user_config.rootDir}"}}},
                "user_config": {"rootDir": {"type": "directory", "title": "Root directory", "required": True, "default": "${HOME}/Documents"}},
                "compatibility": {"platforms": ["darwin", "win32", "linux"]}}
    jw(src / "manifest.json", manifest)
    bundle = wd / "local-files.mcpb"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(src).as_posix())
    inst = wd / "installed"
    with zipfile.ZipFile(bundle) as z:
        names = z.namelist()
        z.extractall(inst)
    man = json.loads((inst / "manifest.json").read_text())
    issues = mcpb_validate(man, names)
    folder = wd / "userdocs"
    for n in ("b.txt", "a.md"):
        wt(folder / n, "x")
    sub = {"__dirname": str(inst), "user_config.rootDir": str(folder)}
    expand = lambda s: re.sub(r"\$\{([\w.]+)\}", lambda m: sub.get(m.group(1), m.group(0)), s)
    cfg = man["server"]["mcp_config"]
    cmd = [cfg["command"]] + [expand(a) for a in cfg["args"]]
    env = {k: expand(v) for k, v in cfg["env"].items()}
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                                                           "clientInfo": {"name": "t", "version": "0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"}, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "list_files", "arguments": {}}}]
    done = sh(cmd, env=env, inp="\n".join(json.dumps(m) for m in msgs) + "\n", timeout=20)
    replies = {r["id"]: r for r in map(json.loads, done.stdout.strip().splitlines())}
    listing = replies[3]["result"]["content"][0]["text"].split("\n")
    rep = jw(wd / "mcpb_report.json", {"bundle": bundle.name, "entries": names, "validation": issues,
                                       "tools": [t["name"] for t in replies[2]["result"]["tools"]], "call": listing})
    broken = json.loads(json.dumps(man))
    broken["server"]["mcp_config"]["args"] = ["/Users/me/dev/server/index.js"]
    broken["server"]["entry_point"] = "dist/index.js"
    broken["user_config"]["apiToken"] = {"type": "string"}
    bad_issues = mcpb_validate(broken, names)
    return [
        check("bundle holds manifest + server entry", sorted(names) == ["manifest.json", "server/index.js"], sorted(names), ["manifest.json", "server/index.js"]),
        check("manifest validates (relative ${__dirname} args, declared user_config)", issues == [], issues, []),
        check("bundled server answers initialize and tools/list over stdio", replies[1]["result"]["serverInfo"]["name"] == "local-files"
              and [t["name"] for t in replies[2]["result"]["tools"]] == ["list_files"], [t["name"] for t in replies[2]["result"]["tools"]], ["list_files"]),
        check("tools/call uses the install-time user_config dir", listing == ["a.md", "b.txt"], listing, ["a.md", "b.txt"]),
        check("negative control: absolute path, wrong entry point and unflagged secret are rejected",
              sorted(i.split(":")[0].split(" apiToken")[0] for i in bad_issues) == ["absolute path in args", "entry_point not in bundle", "secret"],
              bad_issues, "3 issues"),
    ], [bundle, rep]


# ---------------------------------------------------------------- 12640 internal audit guide (classification + report)
def classify(f):
    if f["element_exists"] is False:
        cls = "Major NC" if f.get("systemic") or f.get("affects_qms_results") else "Major NC"
    elif f.get("partial"):
        cls = "Major NC" if f.get("systemic") else "Minor NC"
    elif f.get("risk"):
        cls = "OFI"
    else:
        cls = "Conforming"
    return cls


def audit_report(meta, findings):
    problems = []
    if meta["auditor_area"] == meta["audited_area"]:
        problems.append("auditor not independent")
    by_clause = {}
    for f in findings:
        f["class"] = classify(f)
        by_clause.setdefault((f["clause"], f["class"]), []).append(f)
        if f["class"] != "Conforming" and (f.get("records_sampled", 0) < 2 or f.get("people", 0) < 2):
            problems.append("sampling below 2-3 records/people: " + f["id"])
        if re.search(r"\b(not good|some|bad|poor|they said)\b", f["observation"], re.I) or not re.search(r"\d", f["observation"]):
            problems.append("observation not specific/factual: " + f["id"])
        if f.get("evidence_type") == "verbal":
            problems.append("verbal confirmation is not objective evidence: " + f["id"])
    for (clause, cls), fs in by_clause.items():  # the same minor NC in several records → systemic → Major
        if cls == "Minor NC" and len(fs) >= 2:
            for f in fs:
                f["class"] = "Major NC"
                f["reclassified"] = "repeated minor NC on §%s indicates systemic failure" % clause
    actions = [{"ref": f["id"], "class": f["class"], "owner": f.get("owner"), "target": f.get("target"), "car": f.get("car")}
               for f in findings if f["class"] == "Major NC"]
    for a in actions:
        if not (a["owner"] and a["target"] and a["car"]):
            problems.append("Major NC without CAR owner/date: " + a["ref"])
    counts = {c: sum(1 for f in findings if f["class"] == c) for c in ("Major NC", "Minor NC", "OFI")}
    return counts, actions, problems


@card(K("2989-quality-engineering-skills/12640-audit-guide"))
def audit_guide(task, wd):
    meta = {"standard": "ISO 9001:2015", "scope": "Station 3 machining", "auditor_area": "Purchasing", "audited_area": "Production"}
    finds = [
        {"id": "F1", "clause": "7.1.5.2", "element_exists": True, "partial": True, "records_sampled": 5, "people": 2,
         "observation": "Calibration records requested for 5 gauges at Station 3; 2 (G-045, G-067) had no record.", "owner": "Q. Lead", "target": "2026-12-01", "car": "CAR-17"},
        {"id": "F2", "clause": "7.1.5.2", "element_exists": True, "partial": True, "records_sampled": 3, "people": 2,
         "observation": "Gauge G-102 at Station 3 overdue by 41 days on 2026-11-02.", "owner": "Q. Lead", "target": "2026-12-01", "car": "CAR-18"},
        {"id": "F3", "clause": "8.5.1", "element_exists": True, "risk": True, "records_sampled": 3, "people": 3,
         "observation": "Work instruction WI-33 rev 4 at point of use; operators keep a rev 3 copy in drawer 2."},
        {"id": "F4", "clause": "9.1.3", "element_exists": True, "partial": True, "records_sampled": 3, "people": 2,
         "observation": "KPI review minutes for 2 of 3 months (Aug, Oct) list no actions for scrap above 4%.", "owner": None, "target": None, "car": None},
    ]
    counts, actions, problems = audit_report(meta, finds)
    lines = ["INTERNAL AUDIT REPORT", "", "Standard: " + meta["standard"], "Scope: " + meta["scope"], "Auditor: confirmed independent of audited area", "",
             "FINDINGS SUMMARY:"] + ["%s: %d" % kv for kv in counts.items()] + ["", "FINDINGS:"]
    for f in finds:
        lines += ["%s — Clause §%s" % (f["class"].upper(), f["clause"]), "Observation: " + f["observation"],
                  "Evidence: %d records, %d people" % (f["records_sampled"], f["people"]), ""]
    lines += ["REQUIRED ACTIONS:", "| Finding | Class | Owner | Target | CAR |"] + ["| %s | %s | %s | %s | %s |" % tuple(a.values()) for a in actions]
    out = wt(wd / "audit_report.txt", "\n".join(lines) + "\n")
    jw(wd / "audit.json", {"counts": counts, "actions": actions, "problems": problems})
    weak = [{"id": "W1", "clause": "7.2", "element_exists": False, "records_sampled": 1, "people": 1, "evidence_type": "verbal",
             "observation": "Training is not good, they said some records exist."}]
    _, _, weak_problems = audit_report({**meta, "auditor_area": "Production"}, weak)
    return [
        check("classes: repeated calibration minor NCs reclassified to Major, F3 OFI, F4 Minor",
              [f["class"] for f in finds] == ["Major NC", "Major NC", "OFI", "Minor NC"], [f["class"] for f in finds], ["Major NC", "Major NC", "OFI", "Minor NC"]),
        check("summary counts", counts == {"Major NC": 2, "Minor NC": 1, "OFI": 1}, counts, {"Major NC": 2, "Minor NC": 1, "OFI": 1}),
        check("every Major NC has a CAR with owner and target date", problems == [], problems, []),
        check("negative control: own-area, single-record, verbal, vague, no-CAR finding fails 5 rules", len(weak_problems) == 5, weak_problems, "5 problems"),
    ], [out]


# ---------------------------------------------------------------- 12641 control plan builder
def cp_validate(rows, pfmea):
    gaps = []
    for r in rows:
        rid = "%s/%s" % (r["step"], r["characteristic"])
        if not re.fullmatch(r"\d+( pcs)?", str(r["sample_size"])):
            gaps.append(rid + ": sample size must be a number")
        if re.search(r"as required", r["frequency"], re.I):
            gaps.append(rid + ": frequency 'as required'")
        if re.fullmatch(r"\s*(notify supervisor|quarantine parts)\.?\s*", r["reaction"], re.I):
            gaps.append(rid + ": reaction plan stops before the next step")
        if r.get("special") in ("SC", "CC") and r["method"] == "visual" and r["type"] == "variable":
            gaps.append(rid + ": visual-only control for a variable special characteristic")
        if r.get("special") in ("SC", "CC") and r["type"] == "variable" and (r.get("grr") is None or r["grr"] > 30):
            gaps.append(rid + ": MSA missing or %GRR > 30")
        if r.get("special") in ("SC", "CC") and r["frequency"] != "100%" and (r.get("cpk") or 0) < 1.67:
            gaps.append(rid + ": special characteristic without 100% or Cpk >= 1.67")
    covered = {(r["step"], r["characteristic"]) for r in rows}
    for fm in pfmea:
        if fm["ap"] == "H":
            if (fm["step"], fm["characteristic"]) not in covered:
                gaps.append("PFMEA %s: H-AP failure mode has no Control Plan row" % fm["id"])
            elif fm.get("controls") == "inspection" and not any(r.get("poka_yoke") for r in rows if (r["step"], r["characteristic"]) == (fm["step"], fm["characteristic"])):
                gaps.append("PFMEA %s: H-AP controlled by inspection only, add poka-yoke" % fm["id"])
    return gaps


@card(K("2989-quality-engineering-skills/12641-control-plan-builder"))
def control_plan_builder(task, wd):
    pfmea = [{"id": "FM-1", "step": "20 Drill", "characteristic": "hole dia 6.00±0.02", "ap": "H", "controls": "inspection"},
             {"id": "FM-2", "step": "30 Press", "characteristic": "press force 2-3 kN", "ap": "M"},
             {"id": "FM-3", "step": "40 Crimp", "characteristic": "crimp height 1.2±0.05", "ap": "H"}]
    good = [
        {"step": "20 Drill", "machine": "CNC-4", "characteristic": "hole dia 6.00±0.02", "type": "variable", "special": "CC", "spec": "6.00±0.02",
         "method": "air gauge + SPC X-bar/R", "grr": 12.0, "sample_size": "5", "frequency": "100%", "poka_yoke": "drill-break sensor",
         "reaction": "stop machine, quarantine since last good check, 100% sort, notify QE, open 8D"},
        {"step": "30 Press", "machine": "P-2", "characteristic": "press force 2-3 kN", "type": "variable", "spec": "2-3 kN", "method": "load cell monitor",
         "grr": 8.0, "sample_size": "1", "frequency": "every part", "reaction": "machine interlock rejects part to red bin; setter adjusts and re-verifies first-off"},
        {"step": "40 Crimp", "machine": "CR-1", "characteristic": "crimp height 1.2±0.05", "type": "variable", "special": "SC", "spec": "1.2±0.05",
         "method": "micrometer + SPC", "grr": 18.0, "cpk": 1.9, "sample_size": "5", "frequency": "every 2 hours",
         "reaction": "quarantine lot, re-measure 5 pcs, adjust tooling, release by QE"},
    ]
    gaps_good = cp_validate(good, pfmea)
    cols = ["step", "machine", "characteristic", "type", "special", "spec", "method", "sample_size", "frequency", "reaction"]
    md = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n" + "\n".join("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in good)
    out = wt(wd / "control_plan.md", "# Control Plan — part 4711 rev C (Production)\n\n" + md + "\n\nGap list: none\n")
    draft = [
        {"step": "20 Drill", "characteristic": "hole dia 6.00±0.02", "type": "variable", "special": "CC", "method": "visual", "grr": None,
         "sample_size": "as required", "frequency": "as required", "reaction": "notify supervisor"},
        {"step": "30 Press", "characteristic": "press force 2-3 kN", "type": "variable", "method": "load cell", "grr": 8.0, "sample_size": "1",
         "frequency": "every part", "reaction": "quarantine parts"},
    ]
    gaps_draft = cp_validate(draft, pfmea)
    jw(wd / "cp_gaps.json", {"final": gaps_good, "draft": gaps_draft})
    want = sorted(["20 Drill/hole dia 6.00±0.02: sample size must be a number", "20 Drill/hole dia 6.00±0.02: frequency 'as required'",
                   "20 Drill/hole dia 6.00±0.02: reaction plan stops before the next step",
                   "20 Drill/hole dia 6.00±0.02: visual-only control for a variable special characteristic",
                   "20 Drill/hole dia 6.00±0.02: MSA missing or %GRR > 30",
                   "20 Drill/hole dia 6.00±0.02: special characteristic without 100% or Cpk >= 1.67",
                   "30 Press/press force 2-3 kN: reaction plan stops before the next step",
                   "PFMEA FM-1: H-AP controlled by inspection only, add poka-yoke",
                   "PFMEA FM-3: H-AP failure mode has no Control Plan row"])
    return [
        check("final Control Plan: every row specific, every H-AP linked, no gaps", gaps_good == [], gaps_good, []),
        check("10 columns populated on every row", all(all(str(r.get(c, "x")) for c in cols) for r in good), True, True),
        check("negative control: the draft shows exactly the 9 planted gaps", sorted(gaps_draft) == want, sorted(gaps_draft), want),
    ], [out]
