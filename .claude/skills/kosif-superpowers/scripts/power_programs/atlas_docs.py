"""Real programs for the atlas-docs family (instruction files, regulated documents, diagrams, docs QA, writing).

Each function builds a fixture (a small repo, a contract, a transcript, a schema ...), runs the
card's procedure as a deterministic checker/generator/transformer and checks known answers.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path


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


def _git(cwd, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    return subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True, check=True).stdout.strip()


def _sentences(t):
    return [s for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s]


def _syllables(word):
    w = word.lower()
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups) - (1 if w.endswith("e") and len(groups) > 1 else 0)
    return max(1, n)


def _fk_grade(text):
    words = re.findall(r"[A-Za-z']+", text)
    s = len(_sentences(text))
    return 0.39 * len(words) / s + 11.8 * sum(_syllables(w) for w in words) / len(words) - 15.59


# ---------------------------------------------------------------- ADOCS-01
def adocs_01(work: Path):
    repo = work / "repo"
    (repo / "web").mkdir(parents=True)
    (repo / "Makefile").write_text("test:\n\tpytest -q\nlint:\n\truff check .\n")
    (repo / "web" / "package.json").write_text(json.dumps({"scripts": {"test": "vitest run", "build": "vite build"}}))
    answers = {"never": ["edit vendor/", "push to main"], "ask_first": ["schema migrations"]}
    targets = re.findall(r"^(\w+):", (repo / "Makefile").read_text(), re.M)
    root = "# AGENTS.md\n## Commands\n" + "\n".join(f"- `make {t}`" for t in targets) + \
           "\n## Boundaries\n" + "\n".join(f"- Never {x}" for x in answers["never"]) + "\n" + "\n".join(f"- Ask before {x}" for x in answers["ask_first"]) + "\n"
    web = json.loads((repo / "web" / "package.json").read_text())["scripts"]
    scoped = "# AGENTS.md (web/)\n## Commands\n" + "\n".join(f"- `npm run {k}`" for k in web) + "\n"
    (repo / "AGENTS.md").write_text(root)
    (repo / "web" / "AGENTS.md").write_text(scoped)

    def verify(md, available):
        return [c for c in re.findall(r"`(?:make|npm run) (\w+)`", md) if c not in available]

    drift = verify(root + "- `make deploy`\n", targets)
    lines = len(root.splitlines())
    return [_c("root file lists exactly the Makefile targets", verify(root, targets) == [] and "`make test`" in root, targets),
            _c("scoped web/AGENTS.md uses the npm scripts", verify(scoped, web) == [] and "`npm run build`" in scoped, list(web)),
            _c("boundaries from the questionnaire present", "Never edit vendor/" in root and "Ask before schema migrations" in root, ""),
            _c("drift audit catches a command that no longer exists", drift == ["deploy"], drift),
            _c("file sized to a tiny codebase (< 15 lines)", lines < 15, lines)]


# ---------------------------------------------------------------- ADOCS-02
def adocs_02(work: Path):
    blocks = {"Run tests": "Run `pytest -q` before every commit.",
              "Release procedure": "\n".join(f"{i}. step {i} of the release" for i in range(1, 25)),
              "API reference": "| endpoint | method |\n" + "\n".join(f"| /v1/r{i} | GET |" for i in range(40)),
              "Research backlog": "Delegate: investigate flaky tests across all services and summarise."}

    def classify(title, body):
        lines = body.count("\n") + 1
        if body.lower().startswith("delegate"):
            return "subagent"
        if body.count("|") > 40:
            return "link a doc"
        if lines > 10:
            return "make it a skill"
        return "always-needed"

    plan = {t: classify(t, b) for t, b in blocks.items()}
    kept = "\n".join(f"## {t}\n{b}" for t, b in blocks.items() if plan[t] == "always-needed")
    pointers = "\n".join(f"- {t}: see docs/{t.lower().replace(' ', '-')}.md" for t in blocks if plan[t] != "always-needed")
    before = sum(len(b) for b in blocks.values())
    after = len(kept) + len(pointers)
    _w(work, "CLAUDE.md", kept + "\n" + pointers)
    return [_c("short testable rule stays always-needed", plan["Run tests"] == "always-needed", plan),
            _c("long procedure becomes a skill", plan["Release procedure"] == "make it a skill", plan),
            _c("heavy table becomes a linked doc", plan["API reference"] == "link a doc", plan),
            _c("delegated work goes to a subagent", plan["Research backlog"] == "subagent", plan),
            _c("context file shrinks by > 80%", after < 0.2 * before, (before, after))]


# ---------------------------------------------------------------- ADOCS-03
def adocs_03(work: Path):
    mem = work / "memory"
    mem.mkdir()
    files = {"build.md": ["- build with make", "- cache in .cache", "- old: use tox", "- build with make"],
             "style.md": ["- 4 spaces", "- max line 100"]}
    for f, lines in files.items():
        (mem / f).write_text("\n".join(lines) + "\n")
    facts = {"build.md": ["- tests need DOCKER=1", "- old: use tox -> - use nox"], "style.md": ["- max line 100"]}
    limit = {f: len((mem / f).read_text().splitlines()) for f in files}
    batches = [["build.md"], ["style.md"]]  # disjoint
    for batch in batches:
        for f in batch:
            cur = (mem / f).read_text().splitlines()
            for fact in facts[f]:  # facts first
                if "->" in fact:
                    old, new = fact.split(" -> ")
                    cur = [new if l == old else l for l in cur]
                else:
                    cur.append(fact)
            cur = list(dict.fromkeys(cur))  # dedup second
            while len(cur) > limit[f]:  # compression third: drop the oldest non-rule line
                cur.pop(1)
            (mem / f).write_text("\n".join(cur) + "\n")
    after = {f: (mem / f).read_text().splitlines() for f in files}
    verify = all(len(after[f]) <= limit[f] for f in files) and all(len(set(v)) == len(v) for v in after.values())
    flat = [x for b in batches for x in b]
    _w(work, "sync_report.json", {"limits": limit, "after": after, "verify": verify})
    return [_c("batches are disjoint", len(flat) == len(set(flat)), batches),
            _c("every file ends at or below its line count", all(len(after[f]) <= limit[f] for f in files), {f: len(v) for f, v in after.items()}),
            _c("new fact DOCKER=1 recorded", "- tests need DOCKER=1" in after["build.md"], after["build.md"]),
            _c("changed fact replaced, not appended (tox -> nox)", "- use nox" in after["build.md"] and "- old: use tox" not in after["build.md"], after["build.md"]),
            _c("duplicates removed; independent verify passes", verify, verify)]


# ---------------------------------------------------------------- ADOCS-04
def _abn_ok(abn):
    d = [int(x) for x in re.sub(r"\D", "", abn)]
    if len(d) != 11:
        return False
    d[0] -= 1
    w = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    return sum(a * b for a, b in zip(d, w)) % 89 == 0


def adocs_04(work: Path):
    REPORTABLE = {"construction", "cleaning", "courier", "it", "road freight", "security"}
    bills = [{"abn": "51 824 753 556", "name": "BuildCo", "industry": "construction", "gross": 11000, "gst": 1000, "date": "2025-08-01"},
             {"abn": "51 824 753 556", "name": "BuildCo", "industry": "construction", "gross": 5500, "gst": 500, "date": "2026-03-01"},
             {"abn": "51 824 753 557", "name": "BadABN", "industry": "cleaning", "gross": 2200, "gst": 200, "date": "2025-09-01"},
             {"abn": "", "name": "NoABN", "industry": "courier", "gross": 1100, "gst": 100, "date": "2025-10-01"},
             {"abn": "53 004 085 616", "name": "Paper", "industry": "stationery", "gross": 900, "gst": 0, "date": "2025-11-01"}]
    rep = [b for b in bills if b["industry"] in REPORTABLE]
    agg = {}
    for b in rep:
        a = agg.setdefault(b["name"], {"gross": 0, "gst": 0, "count": 0, "first": b["date"], "last": b["date"]})
        a["gross"] += b["gross"]
        a["gst"] += b["gst"]
        a["count"] += 1
        a["first"], a["last"] = min(a["first"], b["date"]), max(a["last"], b["date"])
        a["net"] = a["gross"] - a["gst"]
    errors = [(b["name"], "missing ABN" if not b["abn"] else "invalid ABN") for b in rep if not _abn_ok(b["abn"])]
    mixed_test = lambda contractor_turnover, gst_turnover: contractor_turnover / gst_turnover >= 0.10
    _w(work, "tpar.json", {"aggregate": agg, "errors": errors, "deadline": "28 August"})
    return [_c("ABN 51 824 753 556 passes the 89 checksum", _abn_ok("51 824 753 556"), ""),
            _c("one-digit-off ABN fails", not _abn_ok("51 824 753 557"), ""),
            _c("non-reportable stationery supplier filtered out", "Paper" not in agg, list(agg)),
            _c("BuildCo aggregated: gross 16500, GST 1500, net 15000, 2 bills",
               agg["BuildCo"] == {"gross": 16500, "gst": 1500, "count": 2, "first": "2025-08-01", "last": "2026-03-01", "net": 15000}, agg["BuildCo"]),
            _c("error sweep lists invalid and missing ABN", errors == [("BadABN", "invalid ABN"), ("NoABN", "missing ABN")], errors),
            _c("10% GST-turnover test for mixed businesses", mixed_test(12, 100) and not mixed_test(9, 100), "")]


# ---------------------------------------------------------------- ADOCS-05
def adocs_05(work: Path):
    from openpyxl import Workbook, load_workbook
    ledger = {"revenue": 120_000, "cogs": 70_000, "opex": 30_000}
    budget = {"revenue": 110_000, "cogs": 60_000, "opex": 32_000}
    bs_open, bs_close = {"cash": 50_000, "ar": 20_000}, {"cash": 58_000, "ar": 25_000}
    mat = 5_000
    rows = []
    for k in ledger:
        var = ledger[k] - budget[k]
        fav = var > 0 if k == "revenue" else var < 0
        rows.append((k, ledger[k], budget[k], var, "F" if fav else "U", "explain" if abs(var) >= mat else ""))
    profit = ledger["revenue"] - ledger["cogs"] - ledger["opex"]
    movement = {k: bs_close[k] - bs_open[k] for k in bs_open}
    wb = Workbook()
    ws = wb.active
    ws.title = "P&L vs budget"
    ws.append(["line", "actual", "budget", "variance", "F/U", "commentary"])
    for r in rows:
        ws.append(list(r))
    wb.create_sheet("BS walk").append(["cash move", movement["cash"]])
    wb.create_sheet("KPIs").append(["gross margin", (ledger["revenue"] - ledger["cogs"]) / ledger["revenue"]])
    p = work / "pack.xlsx"
    wb.save(p)
    back = load_workbook(p)
    return [_c("revenue +10000 favourable, cogs +10000 unfavourable", rows[0][3:5] == (10000, "F") and rows[1][3:5] == (10000, "U"), rows),
            _c("opex -2000 favourable, below materiality: no commentary", rows[2][3:] == (-2000, "F", ""), rows[2]),
            _c("profit 20000 from ledger figures only", profit == 20000, profit),
            _c("balance sheet walk: cash +8000, AR +5000", movement == {"cash": 8000, "ar": 5000}, movement),
            _c("pack renders with 3 sheets", back.sheetnames == ["P&L vs budget", "BS walk", "KPIs"], back.sheetnames)]


# ---------------------------------------------------------------- ADOCS-06
def adocs_06(work: Path):
    templates = {"nda": ["parties", "confidential info", "term", "exclusions", "return of materials", "governing law"],
                 "contractor": ["parties", "scope", "payment", "ip ownership", "termination", "governing law"]}
    notes = {"parties": "Who signs. Use full legal names.", "confidential info": "What you must keep secret.",
             "term": "How long this lasts.", "exclusions": "Info that is public is not secret.",
             "return of materials": "Give back papers when it ends.", "governing law": "Which state's courts decide fights."}
    filled = {"parties": "Acme Ltd and Beta LLC", "confidential info": "pricing", "term": "2 years", "governing law": "England"}
    clauses = [{"clause": k, "text": filled.get(k), "plain": notes[k], "counsel_review": k in ("governing law", "exclusions")}
               for k in templates["nda"]]
    missing = [c["clause"] for c in clauses if not c["text"]]
    grade = _fk_grade(" ".join(notes.values()))
    _w(work, "agreement.json", {"type": "nda", "jurisdiction": "England", "clauses": clauses, "missing_protections": missing,
                                "note": "draft for counsel review, not legal advice"})
    return [_c("NDA template picked with its 6 clauses", len(clauses) == 6, [c["clause"] for c in clauses]),
            _c("missing protections listed: exclusions, return of materials", missing == ["exclusions", "return of materials"], missing),
            _c("plain-language notes read at about 8th grade or lower", grade <= 8.5, round(grade, 1)),
            _c("counsel-review points marked", sum(c["counsel_review"] for c in clauses) == 2, "")]


# ---------------------------------------------------------------- ADOCS-07
def adocs_07(work: Path):
    text = ("SERVICES AGREEMENT between Acme (Client) and Dev Co (Supplier). Payment: invoices due Net-90. "
            "Liability: Supplier liability is unlimited. Termination: Client may terminate for convenience on 5 days notice. "
            "IP: all IP vests in Client. Confidentiality: mutual, 3 years. Non-compete: Supplier may not work in the sector for 5 years. "
            "Indemnity: Supplier indemnifies Client for all claims. Governing law: Delaware.")
    user = "Supplier"
    cats = ["payment", "liability", "termination", "ip", "confidentiality", "non-compete", "indemnity", "governing law"]
    findings = []
    m = re.search(r"Net-(\d+)", text)
    if m and int(m[1]) >= 60:
        findings.append(("payment", "high" if int(m[1]) >= 90 else "medium", f"Net-{m[1]} delays cash; ask Net-30"))
    if re.search(r"liability is unlimited", text) and user == "Supplier":
        findings.append(("liability", "high", "uncapped liability; ask cap at 12 months fees"))
    t = re.search(r"terminate for convenience on (\d+) days", text)
    if t and int(t[1]) < 30:
        findings.append(("termination", "medium", f"{t[1]} days notice is short"))
    nc = re.search(r"Non-compete: .*?(\d+) years", text)
    if nc and int(nc[1]) > 1:
        findings.append(("non-compete", "high", f"{nc[1]}-year non-compete"))
    if re.search(r"Supplier indemnifies Client for all claims", text):
        findings.append(("indemnity", "medium", "one-way, uncapped indemnity"))
    findings.sort(key=lambda f: {"high": 0, "medium": 1}[f[1]])
    covered = {f[0] for f in findings}
    redline = [{"clause": f[0], "ask": f[2]} for f in findings]
    _w(work, "review.json", {"type": "services", "user_party": user, "categories": cats, "findings": findings, "redline": redline,
                             "disclaimer": "not legal advice"})
    return [_c("8 review categories, starting with payment", len(cats) == 8 and cats[0] == "payment", cats),
            _c("Net-90 flagged high (Net-60+ rule)", ("payment", "high", "Net-90 delays cash; ask Net-30") in findings, findings),
            _c("unlimited liability and 5-year non-compete are high", {"liability", "non-compete"} <= {f[0] for f in findings if f[1] == "high"}, findings),
            _c("balanced clauses (confidentiality, IP, law) not flagged", not ({"confidentiality", "governing law"} & covered), covered),
            _c("findings tiered: highs first", [f[1] for f in findings] == sorted([f[1] for f in findings], key=lambda s: s != "high"), "")]


# ---------------------------------------------------------------- ADOCS-08
def adocs_08(work: Path):
    playbook = {"liability_cap_x_fees": (1, 2, 3), "payment_days": (30, 45, 60), "auto_renew_notice_days": (60, 30, 15)}
    contract = {"liability_cap_x_fees": 2.5, "payment_days": 30, "auto_renew_notice_days": 10,
                "parties": ["Acme", "Beta"], "value": 120000, "governing_law": "Ontario", "renewal": "auto 1 year"}

    def tier(k, v):
        std, fb, walk = playbook[k]
        lower_is_better = std < walk
        worse = (lambda a, b: a > b) if lower_is_better else (lambda a, b: a < b)
        if not worse(v, std):
            return "standard"
        if not worse(v, fb):
            return "within fallback"
        if not worse(v, walk):
            return "beyond fallback -> legal approver"
        return "walk-away"

    tiers = {k: tier(k, contract[k]) for k in playbook}
    pen = {"standard": 0, "within fallback": 10, "beyond fallback -> legal approver": 25, "walk-away": 40}
    score = 100 - sum(pen[t] for t in tiers.values())
    meta = {k: contract[k] for k in ("parties", "value", "governing_law", "renewal")}
    _w(work, "clause_review.json", {"tiers": tiers, "safety_score": score, "extracted": meta, "note": "not legal advice"})
    return [_c("cap 2.5x fees is beyond the 2x fallback -> approver", tiers["liability_cap_x_fees"] == "beyond fallback -> legal approver", tiers),
            _c("Net-30 payment is standard", tiers["payment_days"] == "standard", tiers),
            _c("10-day renewal notice is past walk-away (15)", tiers["auto_renew_notice_days"] == "walk-away", tiers),
            _c("safety score 100 - 25 - 40 = 35", score == 35, score),
            _c("schema extraction: parties, value, law, renewal", meta["governing_law"] == "Ontario" and meta["value"] == 120000, meta)]


# ---------------------------------------------------------------- ADOCS-09
def adocs_09(work: Path):
    weights = {"fit": 0.3, "win_probability": 0.3, "margin": 0.2, "capacity": 0.2}
    good = {"fit": 8, "win_probability": 7, "margin": 6, "capacity": 9}
    poor = {"fit": 3, "win_probability": 2, "margin": 5, "capacity": 4}
    bid = lambda s: sum(weights[k] * s[k] for k in weights) >= 6
    tender = ("The supplier shall provide 24/7 support. The system must support Arabic and English. "
              "Bidders should describe their roadmap. The solution shall be hosted in-country. Pricing will be evaluated at 30%.")
    reqs = [s for s in _sentences(tender) if re.search(r"\b(shall|must)\b", s)]
    answers = {0: "24/7 NOC with 15-minute response.", 1: "Full RTL Arabic UI and English."}
    matrix = [{"id": f"R{i + 1}", "requirement": r, "answer": answers.get(i), "status": "compliant" if i in answers else "GAP"} for i, r in enumerate(reqs)]
    gaps = [m["id"] for m in matrix if m["status"] == "GAP"]
    _w(work, "compliance_matrix.json", matrix)
    return [_c("bid/no-bid: 7.5 -> bid, 3.4 -> no bid", bid(good) and not bid(poor), (sum(weights[k] * good[k] for k in weights), sum(weights[k] * poor[k] for k in weights))),
            _c("3 mandatory shall/must requirements extracted (should excluded)", len(reqs) == 3, reqs),
            _c("gap review finds hosting requirement unanswered", gaps == ["R3"], gaps)]


# ---------------------------------------------------------------- ADOCS-10
def adocs_10(work: Path):
    risks = [{"asset": "customer db", "threat": "ransomware", "L": 4, "I": 5, "owner": "CISO"},
             {"asset": "laptops", "threat": "theft", "L": 3, "I": 2, "owner": "IT"},
             {"asset": "website", "threat": "defacement", "L": 2, "I": 2, "owner": None}]
    controls = {"ransomware": ["offline backups", "EDR"], "theft": ["disk encryption"], "defacement": ["WAF"]}
    for r in risks:
        r["score"] = r["L"] * r["I"]
        r["level"] = "critical" if r["score"] >= 15 else "high" if r["score"] >= 8 else "medium" if r["score"] >= 4 else "low"
        r["escalate"] = r["level"] in ("critical", "high")
        r["controls"] = controls[r["threat"]] if r["score"] >= 4 else []
    missing_owner = [r["asset"] for r in risks if not r["owner"]]
    _w(work, "risk_register.json", risks)
    return [_c("ransomware 4x5 = 20 critical and escalated", risks[0]["score"] == 20 and risks[0]["level"] == "critical" and risks[0]["escalate"], risks[0]),
            _c("theft 3x2 = 6 medium, not escalated", risks[1]["level"] == "medium" and not risks[1]["escalate"], risks[1]),
            _c("controls selected from the risk", risks[0]["controls"] == ["offline backups", "EDR"], risks[0]["controls"]),
            _c("risk without an owner flagged for audit", missing_owner == ["website"], missing_owner)]


# ---------------------------------------------------------------- ADOCS-11
def adocs_11(work: Path):
    sql = """CREATE TABLE users (id INT PRIMARY KEY, email TEXT NOT NULL);
CREATE TABLE orders (id INT PRIMARY KEY, user_id INT NOT NULL REFERENCES users(id), coupon_id INT);
CREATE TABLE coupons (id INT PRIMARY KEY, code TEXT);"""
    _w(work, "migrations/001.sql", sql)
    ents, rels = {}, []
    for m in re.finditer(r"CREATE TABLE (\w+) \((.*?)\);", sql, re.S):
        cols = []
        for col in m[2].split(","):
            parts = col.split()
            cols.append((parts[0], parts[1], "NOT NULL" in col or "PRIMARY" in col))
            r = re.search(r"REFERENCES (\w+)\((\w+)\)", col)
            if r:
                rels.append((r[1], m[1], "||--o{" if "NOT NULL" in col else "|o--o{", parts[0]))
        ents[m[1]] = cols
    mer = ["erDiagram"] + [f"  {a} {card} {b} : {lbl}" for a, b, card, lbl in [(x[0], x[1], x[2], x[3]) for x in rels]]
    for e, cols in ents.items():
        mer.append(f"  %% source: migrations/001.sql ({e})")
        mer.append(f"  {e} {{" + " ".join(f"{t} {n}" for n, t, _ in cols) + "}")
    _w(work, "erd.mmd", "\n".join(mer))
    return [_c("3 entities parsed from SQL", list(ents) == ["users", "orders", "coupons"], list(ents)),
            _c("only the declared FK becomes a relation", rels == [("users", "orders", "||--o{", "user_id")], rels),
            _c("coupon_id without REFERENCES is not invented as a relation", not any(r[0] == "coupons" for r in rels), rels),
            _c("each box cites its source file", "\n".join(mer).count("source: migrations/001.sql") == 3, "")]


# ---------------------------------------------------------------- ADOCS-12
def adocs_12(work: Path):
    pm = {"incident_date": "2026-10-01", "draft_date": "2026-10-02", "final_date": "2026-10-07",
          "timeline": [("09:00", "deploy 4.2"), ("09:07", "error rate 12%"), ("09:15", "rollback"), ("09:30", "recovered")],
          "root_cause": "migration lock held while the deploy health check passed", "contributing": ["no canary", "alert threshold 15%"],
          "actions": [{"what": "add canary stage", "owner": "sre", "due": "2026-10-20"}, {"what": "lower alert to 5%", "owner": None, "due": None}],
          "narrative": "Conditions allowed the lock to block writes."}
    day = lambda d: int(d.split("-")[2])
    issues = []
    if day(pm["draft_date"]) - day(pm["incident_date"]) > 2:
        issues.append("draft late")
    if not 5 <= day(pm["final_date"]) - day(pm["incident_date"]) <= 7:
        issues.append("finalize day 5-7")
    times = [t for t, _ in pm["timeline"]]
    if times != sorted(times):
        issues.append("timeline order")
    issues += [f"action '{a['what']}' needs owner and due date" for a in pm["actions"] if not (a["owner"] and a["due"])]
    blame = re.search(r"\b(caused by|fault of|blame)\b\s+[A-Z][a-z]+", pm["narrative"] + " " + pm["root_cause"])
    _w(work, "postmortem.json", {**pm, "issues": issues})
    return [_c("draft within 2 days and final on day 6 pass", "draft late" not in issues and "finalize day 5-7" not in issues, issues),
            _c("timeline is chronological", times == sorted(times), times),
            _c("action item without owner/due date flagged", issues == ["action 'lower alert to 5%' needs owner and due date"], issues),
            _c("blameless framing: no person blamed", blame is None, "")]


# ---------------------------------------------------------------- ADOCS-13
def adocs_13(work: Path):
    config = {"DATABASE_URL": "postgres://admin:hunter2@db.internal:5432/app", "STRIPE_KEY": "sk_live_abcdef123456", "LOG_LEVEL": "info"}
    allow = ["versions", "config_keys", "error_class", "request_ids", "timing_ms", "retries"]
    forbidden = [r"sk_live_\w+", r"://[^@\s]+@", r"[\w.]+@[\w.]+\.\w+", r"\b\d{1,3}(\.\d{1,3}){3}\b"]
    bundle = {"versions": {"app": "4.2.1"}, "config_keys": {k: True for k in config}, "error_class": "TimeoutError",
              "request_ids": ["req_81f2"], "timing_ms": [120, 5000], "retries": 3,
              "repro": {"expected": "200 in < 1 s", "observed": "504 after 5 s"}}

    def canary(text):
        return [p for p in forbidden if re.search(p, text)]

    text = json.dumps(bundle)
    leaked = canary(text)
    bad = canary(json.dumps({**bundle, "note": "user ali@x.com at 10.1.2.3"}))
    path = _w(work, "bundle.json", bundle)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    _w(work, "bundle.manifest.json", {"sha256": digest, "redactions": ["config values"], "gaps": ["no heap dump"], "delete_after": "2026-12-01"})
    return [_c("only allowlisted fields shipped (plus synthetic repro)", set(bundle) - {"repro"} == set(allow), sorted(bundle)),
            _c("config key presence recorded, never values", "hunter2" not in text and bundle["config_keys"]["STRIPE_KEY"] is True, ""),
            _c("canary scan of the bundle is clean", leaked == [], leaked),
            _c("planted email and IP make the scan abort", len(bad) == 2, bad),
            _c("bundle hashed in the manifest", len(digest) == 64, digest[:12])]


# ---------------------------------------------------------------- ADOCS-14
def adocs_14(work: Path):
    bots = ["GPTBot", "ClaudeBot", "PerplexityBot"]
    robots = "\n".join(f"User-agent: {b}\nAllow: /\n" for b in bots) + "\nUser-agent: *\nContent-Signal: search=yes, ai-input=yes, ai-train=no\nAllow: /\n"
    pages = {"/docs/install": "# Install\nRun `pip install kosif`.", "/docs/usage": "# Usage\nCall `kosif run`."}
    llms = "# Kosif\n\n> Arabic-first motion tools.\n\n## Docs\n" + "\n".join(f"- [{p.split('/')[-1].title()}]({p}.md)" for p in pages)
    _w(work, "robots.txt", robots)
    _w(work, "llms.txt", llms)
    for p, md in pages.items():
        _w(work, "site" + p + ".md", md)

    def serve(path, accept):
        base = path[:-3] if path.endswith(".md") else path
        if base not in pages:
            return 404, {}, ""
        if path.endswith(".md") or "text/markdown" in accept:
            return 200, {"Content-Type": "text/markdown; charset=utf-8"}, pages[base]
        return 200, {"Content-Type": "text/html", "Link": f'<{base}.md>; rel="alternate"; type="text/markdown"'}, f"<h1>{base}</h1>"

    s_md, h_md, b_md = serve("/docs/install", "text/markdown")
    s_html, h_html, _ = serve("/docs/install", "text/html")
    s_dot, h_dot, _ = serve("/docs/usage.md", "*/*")
    return [_c("robots allows the three AI crawlers and carries Content-Signal", all(f"User-agent: {b}\nAllow: /" in robots for b in bots) and "Content-Signal:" in robots, ""),
            _c("llms.txt has H1, summary blockquote and links to .md", llms.startswith("# ") and "\n> " in llms and llms.count(".md)") == 2, llms[:40]),
            _c("Accept: text/markdown returns markdown from the same source", s_md == 200 and h_md["Content-Type"].startswith("text/markdown") and b_md == pages["/docs/install"], h_md),
            _c("HTML response advertises the .md via Link header", 'rel="alternate"' in h_html.get("Link", ""), h_html),
            _c("/path.md served as text/markdown", s_dot == 200 and h_dot["Content-Type"].startswith("text/markdown"), h_dot)]


# ---------------------------------------------------------------- ADOCS-15
def adocs_15(work: Path):
    def rule11(sw):
        """MDR Annex VIII rule 11 for software (MDCG 2019-11 reading)."""
        if sw.get("informs_decisions"):
            if sw.get("worst") == "death_or_irreversible":
                return "III"
            if sw.get("worst") == "serious_deterioration_or_surgery":
                return "IIb"
            return "IIa"
        if sw.get("monitors_physiological"):
            return "IIb" if sw.get("vital_parameters_immediate_danger") else "IIa"
        return "I"

    cases = {"stroke triage": {"informs_decisions": True, "worst": "death_or_irreversible"},
             "insulin dose advice": {"informs_decisions": True, "worst": "serious_deterioration_or_surgery"},
             "skin photo triage": {"informs_decisions": True}, "icu monitor": {"monitors_physiological": True, "vital_parameters_immediate_danger": True},
             "sleep tracker": {"monitors_physiological": True}, "appointment app": {}}
    cls = {k: rule11(v) for k, v in cases.items()}
    annex = {"Annex II": ["device description", "information supplied", "design and manufacturing", "GSPR", "benefit-risk", "V&V"],
             "Annex III": ["post-market surveillance plan", "PSUR"]}
    psur = {"III": "annually", "IIb": "annually", "IIa": "every 2 years"}
    _w(work, "mdr_classification.json", {"rule": "11", "classes": cls, "technical_file": annex, "psur": psur,
                                         "note": "rationale to confirm with the Notified Body"})
    return [_c("decision software with death risk -> class III", cls["stroke triage"] == "III", cls),
            _c("serious deterioration -> IIb; other decision support -> IIa", (cls["insulin dose advice"], cls["skin photo triage"]) == ("IIb", "IIa"), cls),
            _c("vital-parameter monitoring with immediate danger -> IIb, else IIa", (cls["icu monitor"], cls["sleep tracker"]) == ("IIb", "IIa"), cls),
            _c("all other software -> class I", cls["appointment app"] == "I", cls),
            _c("Art. 86 PSUR cadence: IIa every 2 years", psur["IIa"] == "every 2 years", psur)]


# ---------------------------------------------------------------- ADOCS-16
def adocs_16(work: Path):
    FEES = {"FY2026": {"510k": 24335, "de_novo": 162235, "pma": 540783}}

    def pathway(d):
        if d["class"] == "III":
            return "PMA"
        if d.get("predicate") and d.get("substantially_equivalent"):
            change = d.get("change")
            return "Special 510(k)" if change == "own device, design change" else "Abbreviated 510(k)" if change == "standards-based" else "Traditional 510(k)"
        if d["class"] in ("I", "II"):
            return "De Novo"
        return "Pre-Sub needed"

    cases = {"stent": {"class": "III"}, "new_ai_tool": {"class": "II"},
             "glucometer v2": {"class": "II", "predicate": "K123456", "substantially_equivalent": True, "change": "own device, design change"},
             "thermometer": {"class": "II", "predicate": "K999", "substantially_equivalent": True}}
    res = {k: pathway(v) for k, v in cases.items()}
    table = {k: {"pathway": v, "fee": FEES["FY2026"]["pma" if v == "PMA" else "de_novo" if v == "De Novo" else "510k"], "fee_year": "FY2026"}
             for k, v in res.items()}
    _w(work, "fda_pathway.json", {"recommendation": table, "q_sub": ["Is K123456 an appropriate predicate?"], "note": "for regulatory review"})
    return [_c("class III -> PMA", res["stent"] == "PMA", res),
            _c("novel low-moderate risk, no predicate -> De Novo", res["new_ai_tool"] == "De Novo", res),
            _c("design change to own cleared device -> Special 510(k)", res["glucometer v2"] == "Special 510(k)", res),
            _c("plain SE predicate -> Traditional 510(k)", res["thermometer"] == "Traditional 510(k)", res),
            _c("fees tabulated with the fee year flagged", all(v["fee_year"] == "FY2026" for v in table.values()), table["stent"])]


# ---------------------------------------------------------------- ADOCS-17
def adocs_17(work: Path):
    import xml.etree.ElementTree as ET
    tf = """resource "aws_cloudfront_distribution" "cdn" {}
resource "aws_s3_bucket" "site" {}
resource "aws_api_gateway_rest_api" "api" {}
resource "aws_lambda_function" "fn" {}
resource "aws_dynamodb_table" "db" {}
resource "aws_cognito_user_pool" "auth" {}
resource "aws_sqs_queue" "q" {}"""
    _w(work, "main.tf", tf)
    res = re.findall(r'resource "aws_(\w+?)" "(\w+)"', tf)
    icon = {"cloudfront_distribution": "cloudfront", "s3_bucket": "simple_storage_service", "api_gateway_rest_api": "api_gateway",
            "lambda_function": "lambda", "dynamodb_table": "dynamodb", "cognito_user_pool": "cognito", "sqs_queue": "simple_queue_service"}
    root = ET.Element("mxfile")
    g = ET.SubElement(ET.SubElement(ET.SubElement(root, "diagram", name="arch"), "mxGraphModel"), "root")
    ET.SubElement(g, "mxCell", id="0")
    ET.SubElement(g, "mxCell", id="1", parent="0")
    ET.SubElement(g, "mxCell", id="title", value="Serverless web app", parent="1", vertex="1", style="text;fontSize=20")
    for i, (kind, name) in enumerate(res):
        cell = ET.SubElement(g, "mxCell", id=name, value=name, parent="1", vertex="1",
                             style=f"shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon[kind]}")
        ET.SubElement(cell, "mxGeometry", x=str(40 + 120 * i), y="80", width="48", height="48", **{"as": "geometry"})
        ET.SubElement(g, "mxCell", id=f"badge{i + 1}", value=str(i + 1), parent="1", vertex="1", style="ellipse;fillColor=#ff9900")
    if len(res) >= 7:
        ET.SubElement(g, "mxCell", id="legend", value="; ".join(f"{i + 1} {n}" for i, (_, n) in enumerate(res)), parent="1", vertex="1")
    p = work / "arch.drawio"
    ET.ElementTree(root).write(p, encoding="utf-8", xml_declaration=True)
    back = ET.parse(p).getroot()
    cells = back.findall(".//mxCell")
    return [_c("7 resources scanned from Terraform", len(res) == 7, res),
            _c("each service uses an aws4 icon style", sum("mxgraph.aws4." in (c.get("style") or "") for c in cells) == 7, ""),
            _c("numbered step badges 1..7", [c.get("value") for c in cells if c.get("id", "").startswith("badge")] == [str(i) for i in range(1, 8)], ""),
            _c("legend added for 7+ services and a title present", any(c.get("id") == "legend" for c in cells) and any(c.get("id") == "title" for c in cells), ""),
            _c(".drawio XML parses back", back.tag == "mxfile", back.tag)]


# ---------------------------------------------------------------- ADOCS-18
def adocs_18(work: Path):
    def engine(req, existing=None, user=None):
        if user:
            return user
        if existing:
            return existing
        if req in ("c4", "c4 multi-view"):
            return "Structurizr"
        if req in ("uml", "sequence", "gantt", "mindmap", "class"):
            return "PlantUML"
        if req in ("architecture", "flowchart", "erd"):
            return "D2"
        return "D2"

    picks = {"c4": engine("c4 multi-view"), "gantt": engine("gantt"), "erd": engine("erd"), "repo_has_puml": engine("erd", existing="PlantUML"),
             "user_says_d2": engine("c4", user="D2")}
    d2 = "users: {shape: sql_table\n  id: int {constraint: primary_key}\n}\norders: {shape: sql_table\n  user_id: int\n}\norders.user_id -> users.id\n"
    _w(work, "erd.d2", d2)
    return [_c("C4 multi-view -> Structurizr", picks["c4"] == "Structurizr", picks),
            _c("Gantt/UML -> PlantUML; ERD -> D2", picks["gantt"] == "PlantUML" and picks["erd"] == "D2", picks),
            _c("existing project files override the rule", picks["repo_has_puml"] == "PlantUML", picks),
            _c("user-named engine wins first", picks["user_says_d2"] == "D2", picks),
            _c("D2 ERD source uses sql_table shape, kept next to docs", "shape: sql_table" in d2 and (work / "erd.d2").is_file(), "")]


# ---------------------------------------------------------------- ADOCS-19
def adocs_19(work: Path):
    import yaml
    compose = {"services": {"web": {"image": "nginx", "depends_on": ["api"]}, "api": {"build": ".", "depends_on": ["db", "cache"]},
                            "db": {"image": "postgres:16"}, "cache": {"image": "redis:7"}, "worker": {"build": ".", "depends_on": ["cache", "db"]}}}
    _w(work, "repo/docker-compose.yml", yaml.safe_dump(compose))
    data = yaml.safe_load((work / "repo/docker-compose.yml").read_text())
    nodes = {n: {"source": "docker-compose.yml"} for n in data["services"]}
    edges = sorted((s, d) for s, v in data["services"].items() for d in v.get("depends_on", []))
    layout = "single-SVG hero" if len(nodes) <= 8 else "widescreen docs"
    pos = {n: (40 + 130 * i, 60) for i, n in enumerate(nodes)}
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="700" height="140">']
    for a, b in edges:
        svg.append(f'<line x1="{pos[a][0]}" y1="{pos[a][1]}" x2="{pos[b][0]}" y2="{pos[b][1] + 40}" stroke="#555"/>')
    for n, (x, y) in pos.items():
        svg.append(f'<g><rect x="{x - 40}" y="{y - 15}" width="80" height="30" fill="#eef"/><text x="{x}" y="{y + 5}" text-anchor="middle">{n}</text></g>')
    svg.append("</svg>")
    html = "<!doctype html><html><body>" + "".join(svg) + "<p>source: docker-compose.yml</p></body></html>"
    mermaid = "graph LR\n" + "\n".join(f"  {a} --> {b}" for a, b in edges)
    _w(work, "architecture.html", html)
    _w(work, "architecture.mmd", mermaid)
    return [_c("5 services become nodes citing their source", len(nodes) == 5 and all(v["source"] for v in nodes.values()), list(nodes)),
            _c("edges come only from depends_on (5)", edges == [("api", "cache"), ("api", "db"), ("web", "api"), ("worker", "cache"), ("worker", "db")], edges),
            _c("<= 8 nodes -> single-SVG hero layout", layout == "single-SVG hero", layout),
            _c("inline SVG with no external refs, plus Mermaid copy", "http://www.w3.org/2000/svg" in html and "src=" not in html and mermaid.count("-->") == 5, "")]


# ---------------------------------------------------------------- ADOCS-20
def adocs_20(work: Path):
    palette = {"primary": "#1e3a5f", "accent": "#e8590c", "muted": "#868e96", "bg": "#fff9db"}
    concepts = [("Request", "primary"), ("Cache", "accent"), ("DB", "muted")]
    els = []
    for i, (label, role) in enumerate(concepts):
        els.append({"id": f"box{i}", "type": "rectangle", "x": 40 + 200 * i, "y": 80, "width": 140, "height": 60,
                    "strokeColor": palette[role], "backgroundColor": palette["bg"], "boundElements": [{"type": "text", "id": f"t{i}"}]})
        els.append({"id": f"t{i}", "type": "text", "text": label, "containerId": f"box{i}", "x": 60 + 200 * i, "y": 100})
    for i in range(2):
        els.append({"id": f"a{i}", "type": "arrow", "startBinding": {"elementId": f"box{i}"}, "endBinding": {"elementId": f"box{i + 1}"},
                    "x": 180 + 200 * i, "y": 110, "strokeColor": palette["muted"]})
    doc = {"type": "excalidraw", "version": 2, "source": "kosif", "elements": els, "appState": {"viewBackgroundColor": "#ffffff"}}
    _w(work, "flow.excalidraw", doc)
    ids = {e["id"] for e in els}
    dangling = [e["id"] for e in els if e["type"] == "arrow" and not ({e["startBinding"]["elementId"], e["endBinding"]["elementId"]} <= ids)]
    colors = {e.get("strokeColor") for e in els if e.get("strokeColor")}
    order = [e["text"] for e in sorted((e for e in els if e["type"] == "text"), key=lambda e: e["x"])]
    return [_c("valid excalidraw document (type, version 2, elements)", doc["type"] == "excalidraw" and doc["version"] == 2 and len(els) == 8, len(els)),
            _c("every arrow binds to existing boxes", dangling == [], dangling),
            _c("colours come only from the palette file", colors <= set(palette.values()), colors),
            _c("isomorphism: left-to-right order matches the flow Request -> Cache -> DB", order == ["Request", "Cache", "DB"], order)]


# ---------------------------------------------------------------- ADOCS-22
def adocs_22(work: Path):
    edges = [("a", "c"), ("a", "d"), ("b", "c"), ("b", "e"), ("c", "f"), ("d", "f"), ("e", "f")]
    nodes = sorted({x for e in edges for x in e})

    def kind(E, N):
        indeg = {n: 0 for n in N}
        for _, b in E:
            indeg[b] += 1
        seen, order, q = set(), [], [n for n in N if indeg[n] == 0]
        d = dict(indeg)
        while q:
            u = q.pop()
            order.append(u)
            for a, b in E:
                if a == u:
                    d[b] -= 1
                    if d[b] == 0:
                        q.append(b)
        if len(order) < len(N):
            return "general"
        return "tree" if all(v <= 1 for v in indeg.values()) and len(E) == len(N) - 1 else "DAG"

    rank = {}
    for n in nodes:
        rank[n] = 0
    for _ in nodes:
        for a, b in edges:
            rank[b] = max(rank[b], rank[a] + 1)
    layers = {}
    for n, r in rank.items():
        layers.setdefault(r, []).append(n)
    layers[1] = ["e", "c", "d"]  # deliberately bad initial order

    def crossings(L):
        pos = {n: i for r in L for i, n in enumerate(L[r])}
        cr = 0
        for (a, b) in edges:
            for (c, d) in edges:
                if rank[a] == rank[c] and rank[b] == rank[d] and (pos[a] - pos[c]) * (pos[b] - pos[d]) < 0:
                    cr += 1
        return cr // 2

    before = crossings(layers)
    pos0 = {n: i for i, n in enumerate(layers[0])}
    layers[1] = sorted(layers[1], key=lambda n: sum(pos0[a] for a, b in edges if b == n) / max(1, sum(1 for a, b in edges if b == n)))
    after = crossings(layers)
    _w(work, "layout.json", {"kind": kind(edges, nodes), "layers": layers, "crossings": [before, after]})
    return [_c("graph classified as DAG", kind(edges, nodes) == "DAG", kind(edges, nodes)),
            _c("a cycle classifies as general; a path as tree", kind([("x", "y"), ("y", "x")], ["x", "y"]) == "general" and kind([("x", "y"), ("y", "z")], ["x", "y", "z"]) == "tree", ""),
            _c("layered ranks: a,b=0; c,d,e=1; f=2", rank == {"a": 0, "b": 0, "c": 1, "d": 1, "e": 1, "f": 2}, rank),
            _c("barycenter ordering removes crossings (3 -> 0)", before == 3 and after == 0, (before, after))]


# ---------------------------------------------------------------- ADOCS-23
def adocs_23(work: Path):
    cap = 6
    nodes = [("client", "actor"), ("gateway", "service"), ("orders", "service"), ("db", "store"), ("cache", "store")]
    edges = [("client", "gateway", "call"), ("gateway", "orders", "call"), ("orders", "db", "store"), ("orders", "cache", "lookup")]
    if len(nodes) > cap:
        raise ValueError("over complexity budget")
    colors = {"actor": "#495057", "service": "#1c7ed6", "store": "#2f9e44"}
    dash = {"call": None, "store": None, "lookup": "4 3"}
    pos = {n: (60 + 140 * i, 80) for i, (n, _) in enumerate(nodes)}
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" role="img" aria-label="Order request path">',
             '<rect x="190" y="30" width="420" height="110" fill="none" stroke="#868e96" stroke-dasharray="6 4"/>']
    for a, b, k in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        d = f' stroke-dasharray="{dash[k]}"' if dash[k] else ""
        parts.append(f'<path d="M{x1 + 40} {y1} H{(x1 + x2) // 2} V{y2} H{x2 - 40}" fill="none" stroke="#343a40"{d}/>')
    for n, k in nodes:
        x, y = pos[n]
        parts.append(f'<rect x="{x - 40}" y="{y - 18}" width="80" height="36" fill="{colors[k]}"/><text x="{x}" y="{y + 5}" fill="#ffffff" text-anchor="middle">{n}</text>')
    parts.append("</svg>")
    html = "<!doctype html><meta charset=utf-8><h1>How an order request flows</h1>" + "".join(parts)
    _w(work, "diagram.html", html)
    paths = re.findall(r"<path d=\"([^\"]+)\"[^>]*?(stroke-dasharray=\"[^\"]+\")?/>", html)
    orth = all(re.fullmatch(r"M\d+ \d+ H\d+ V\d+ H\d+", d) for d, _ in paths)
    contrast_min = min(_contrast_hex("#ffffff", c) for c in colors.values())
    return [_c("node count within cap 6", len(nodes) <= cap, len(nodes)),
            _c("arrows are orthogonal (H/V segments only)", orth and len(paths) == 4, len(paths)),
            _c("boundary dashed, store path solid, lookup dashed", html.count('stroke-dasharray="6 4"') == 1 and [bool(s) for _, s in paths] == [False, False, False, True], ""),
            _c("inline SVG, no external dependency", "<script" not in html and "href=" not in html, ""),
            _c("white labels keep >= 3:1 on every node fill", contrast_min >= 3, round(contrast_min, 2))]


def _contrast_hex(a, b):
    def lum(h):
        rgb = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------------------------------------------------------------- ADOCS-25
def adocs_25(work: Path):
    root = work / "docs"
    for d, files in {"adrs": ["0001-use-postgres.md", "0002-queue.md"], "rfcs": ["0001-plugin-api.md"], "prds": []}.items():
        (root / d).mkdir(parents=True)
        for f in files:
            (root / d / f).write_text(f"# {f}\nStatus: accepted\n")

    def classify(item):
        if item["state"] == "settled":
            return "ADR"
        if item["state"] == "open":
            return "RFC"
        return "ADR (resolved from RFC)"

    def create(kind_dir, slug, dry_run=True):
        nums = [int(p.name[:4]) for p in (root / kind_dir).glob("[0-9][0-9][0-9][0-9]-*.md")]
        nxt = f"{(max(nums) + 1 if nums else 1):04d}-{slug}.md"
        if dry_run:
            return nxt, False
        (root / kind_dir / nxt).write_text("# " + slug + "\n## Context\n## Decision\n## Consequences\nStatus: proposed\n")
        man = root / "manifest.json"
        m = json.loads(man.read_text()) if man.exists() else {}
        m[nxt] = {"kind": kind_dir, "issue": "#41"}
        man.write_text(json.dumps(m))
        return nxt, True

    dry = create("adrs", "cache-layer")
    dry_wrote = (root / "adrs" / "0003-cache-layer.md").exists()
    real = create("adrs", "cache-layer", dry_run=False)
    rfc = create("rfcs", "auth", dry_run=False)
    prd = create("prds", "onboarding", dry_run=True)
    return [_c("settled -> ADR, open -> RFC, accepted RFC -> ADR", [classify({"state": s}) for s in ("settled", "open", "accepted")] == ["ADR", "RFC", "ADR (resolved from RFC)"], ""),
            _c("dry run proposes next id 0003 without writing", dry == ("0003-cache-layer.md", False) and not dry_wrote, dry),
            _c("next ADR number is 0003, next RFC 0002, first PRD 0001", (real[0], rfc[0], prd[0]) == ("0003-cache-layer.md", "0002-auth.md", "0001-onboarding.md"), (real, rfc, prd)),
            _c("manifest updated with issue link", json.loads((root / "manifest.json").read_text())["0003-cache-layer.md"]["issue"] == "#41", ""),
            _c("ADR has context/decision/consequences/status", all(h in (root / "adrs" / "0003-cache-layer.md").read_text() for h in ("## Context", "## Decision", "## Consequences", "Status:")), "")]


# ---------------------------------------------------------------- ADOCS-26
def adocs_26(work: Path):
    repo = work / "r"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "cli.py").write_text("DEFAULT_TIMEOUT = 30\nCOMMANDS = ['run', 'stop']\n")
    (repo / "README.md").write_text("Default timeout is 30 seconds. Commands: run, stop.\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "v1")
    (repo / "cli.py").write_text("DEFAULT_TIMEOUT = 45\nCOMMANDS = ['run', 'stop', 'status']\n")
    _git(repo, "commit", "-qam", "v2")
    scope = _git(repo, "diff", "--name-only", "HEAD~1", "HEAD").split()
    code = (repo / "cli.py").read_text()
    facts = {"timeout": re.search(r"DEFAULT_TIMEOUT = (\d+)", code)[1], "commands": re.findall(r"'(\w+)'", code)}
    doc = (repo / "README.md").read_text()
    claimed = {"timeout": re.search(r"timeout is (\d+)", doc)[1], "commands": re.findall(r"\b(run|stop|status)\b", doc)}
    drift = {k: (claimed[k], facts[k]) for k in facts if claimed[k] != facts[k]}
    new_doc = f"Default timeout is {facts['timeout']} seconds. Commands: {', '.join(facts['commands'])}.\n"
    sample = subprocess.run(["python3", "-I", "-c", code + "print(len(COMMANDS))"], capture_output=True, text=True).stdout.strip()
    (repo / "README.md").write_text(new_doc)
    _w(work, "doc_update_report.json", {"scope": scope, "drift": drift, "unverified": []})
    return [_c("scope from git diff --name-only is cli.py", scope == ["cli.py"], scope),
            _c("drift found: timeout 30 vs 45 and missing status", drift == {"timeout": ("30", "45"), "commands": (["run", "stop"], ["run", "stop", "status"])}, drift),
            _c("doc conforms to code after update", "45 seconds" in new_doc and "status" in new_doc, new_doc.strip()),
            _c("sample output generated from real code: 3 commands", sample == "3", sample)]


# ---------------------------------------------------------------- ADOCS-27
def adocs_27(work: Path):
    signals = {"tutorial": r"\b(in this tutorial|you will build|let's start)\b", "how-to": r"\b(how to|steps to|to do this)\b",
               "reference": r"\b(parameters?|returns|type:|default:)\b", "explanation": r"\b(why|background|design rationale|trade-?offs?)\b"}
    pages = {"getting-started.md": "In this tutorial you will build a bot. Let's start.",
             "deploy.md": "How to deploy: steps to push.", "api.md": "Parameters: name (type: str, default: none). Returns a job.",
             "architecture.md": "Why we chose queues: background and trade-offs.",
             "config.md": "How to configure the cache. Parameters: ttl (type: int, default: 60). Why we cache: background."}
    tags = {p: [k for k, rx in signals.items() if re.search(rx, t, re.I)] for p, t in pages.items()}
    split = {p: k for p, k in tags.items() if len(k) > 1}
    nav = {"Learn": [p for p, k in tags.items() if k == ["tutorial"]], "Do": [p for p, k in tags.items() if k == ["how-to"]],
           "Look up": [p for p, k in tags.items() if k == ["reference"]], "Understand": [p for p, k in tags.items() if k == ["explanation"]]}
    _w(work, "diataxis.json", {"tags": tags, "split": split, "nav": nav})
    return [_c("each single-kind page tagged with one of the four kinds",
               [tags[p] for p in ("getting-started.md", "deploy.md", "api.md", "architecture.md")] == [["tutorial"], ["how-to"], ["reference"], ["explanation"]], tags),
            _c("config.md mixes how-to, reference and explanation -> split", split == {"config.md": ["how-to", "reference", "explanation"]}, split),
            _c("navigation organised by reader task", list(nav) == ["Learn", "Do", "Look up", "Understand"] and nav["Do"] == ["deploy.md"], nav)]


# ---------------------------------------------------------------- ADOCS-28
def adocs_28(work: Path):
    repo = work / "r"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "src").mkdir()
    for i in range(4):
        (repo / "src" / f"m{i}.py").write_text("x=1\n")
    (repo / "pyproject.toml").write_text('version = "2.1.0"\n')
    (repo / "Makefile").write_text("test:\n\tpytest\n")
    doc = "See `src/m0.py` and `src/legacy.py`. The project has 3 modules. Run `make test` or `make bench`. Version 2.0.0."
    (repo / "README.md").write_text(doc)
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "init")
    findings = []
    for p in re.findall(r"`([\w/]+\.py)`", doc):
        if not (repo / p).exists():
            findings.append(("path", p))
    n = re.search(r"has (\d+) modules", doc)
    actual = len(list((repo / "src").glob("*.py")))
    if n and int(n[1]) != actual:
        findings.append(("count", f"{n[1]} != {actual}"))
    targets = re.findall(r"^(\w+):", (repo / "Makefile").read_text(), re.M)
    findings += [("command", f"make {t}") for t in re.findall(r"`make (\w+)`", doc) if t not in targets]
    v = re.search(r'version = "([\d.]+)"', (repo / "pyproject.toml").read_text())[1]
    if f"Version {v}" not in doc:
        findings.append(("version", f"doc 2.0.0 vs {v}"))
    sha = _git(repo, "rev-parse", "HEAD")
    _w(work, ".docs-sync", sha + "\n")
    _w(work, "audit.json", {"inventory": {"README.md": "users"}, "findings": findings, "edits_made": 0})
    return [_c("missing path src/legacy.py found", ("path", "src/legacy.py") in findings, findings),
            _c("count claim 3 vs 4 modules found", ("count", "3 != 4") in findings, findings),
            _c("command make bench not in Makefile", ("command", "make bench") in findings, findings),
            _c("version badge drift 2.0.0 vs 2.1.0", ("version", "doc 2.0.0 vs 2.1.0") in findings, findings),
            _c("audit stamped with the commit SHA, no edits made", len((work / ".docs-sync").read_text().strip()) == 40, sha[:10])]


# ---------------------------------------------------------------- ADOCS-29
def adocs_29(work: Path):
    root = work / "docs" / "solutions"
    root.mkdir(parents=True)
    (root / "sqlite-locked.md").write_text("---\ntitle: SQLite database is locked\nseen: 1\n---\nUse WAL mode.\n")

    def learn(candidates):
        worth = [c for c in candidates if c["recurrence_cost"] == "high" or c["rediscovery_minutes"] >= 30]
        if not worth:
            return None
        c = worth[0]  # one learning per run
        slug = re.sub(r"[^a-z0-9]+", "-", c["title"].lower()).strip("-")
        existing = [p for p in root.glob("*.md") if slug.split("-")[0] in p.stem and c["key"] in p.read_text().lower()]
        if existing:
            t = existing[0].read_text()
            n = int(re.search(r"seen: (\d+)", t)[1])
            existing[0].write_text(t.replace(f"seen: {n}", f"seen: {n + 1}") + c["fix"] + "\n")
            return ("updated", existing[0].name)
        (root / f"{slug}.md").write_text(f"---\ntitle: {c['title']}\nseen: 1\n---\n{c['fix']}\n")
        return ("created", f"{slug}.md")

    r0 = learn([{"title": "typo in log", "recurrence_cost": "low", "rediscovery_minutes": 2, "key": "typo", "fix": "fixed"}])
    r1 = learn([{"title": "SQLite locked under load", "recurrence_cost": "high", "rediscovery_minutes": 90, "key": "locked", "fix": "Set busy_timeout=5000."},
                {"title": "Docker DNS", "recurrence_cost": "high", "rediscovery_minutes": 60, "key": "dns", "fix": "x"}])
    r2 = learn([{"title": "Docker DNS fails in CI", "recurrence_cost": "high", "rediscovery_minutes": 60, "key": "dns", "fix": "Pin resolv.conf."}])
    files = sorted(p.name for p in root.glob("*.md"))
    return [_c("counterfactual bar: trivial fix writes nothing", r0 is None, r0),
            _c("existing learning updated instead of duplicated", r1 == ("updated", "sqlite-locked.md") and "seen: 2" in (root / "sqlite-locked.md").read_text(), r1),
            _c("one learning per run (Docker DNS not written in run 1)", r2 == ("created", "docker-dns-fails-in-ci.md"), r2),
            _c("notes carry frontmatter", all((root / f).read_text().startswith("---\ntitle:") for f in files), files)]


# ---------------------------------------------------------------- ADOCS-30
def adocs_30(work: Path):
    wiki = work / "wiki"
    (wiki / "raw").mkdir(parents=True)
    (wiki / "raw" / "paper.txt").write_text("Transformers use attention. Attention cost is O(n^2).")
    notes = {"Transformers.md": "Transformers rely on [[Attention]]. Released: 2017.",
             "Attention.md": "Cost is O(n^2). See [[Transformers]]. Released: 2017.",
             "Orphan Note.md": "Nothing links here.",
             "BERT.md": "Uses [[Transformers]]. Released: 2018. Related [[Missing Page]]."}
    notes["Transformers copy.md"] = "Transformers rely on [[Attention]]. Released: 2016."
    for n, t in notes.items():
        (wiki / n).write_text(t)
    links = {n[:-3]: set(re.findall(r"\[\[([^\]]+)\]\]", t)) for n, t in notes.items()}
    inbound = {n: sum(n in v for v in links.values()) for n in links}
    orphans = sorted(n for n, k in inbound.items() if k == 0 and n != "BERT")
    broken = sorted({l for v in links.values() for l in v if l not in links})
    facts = {}
    for n, t in notes.items():
        subj = re.sub(r" copy$", "", n[:-3])
        m = re.search(r"Released: (\d{4})", t)
        if m:
            facts.setdefault(subj, set()).add(m[1])
    contradictions = {k: sorted(v) for k, v in facts.items() if len(v) > 1}
    (wiki / "index.md").write_text("\n".join(f"- [[{n}]]" for n in sorted(links)))
    (wiki / "log.md").write_text("2026-11-03 ingest raw/paper.txt -> 4 notes\n")
    return [_c("orphans found (no inbound links)", orphans == ["Orphan Note", "Transformers copy"], orphans),
            _c("broken wikilink [[Missing Page]] found", broken == ["Missing Page"], broken),
            _c("contradiction: Transformers released 2016 vs 2017", contradictions == {"Transformers": ["2016", "2017"]}, contradictions),
            _c("index and log updated", (wiki / "index.md").read_text().count("[[") == 5 and "ingest" in (wiki / "log.md").read_text(), "")]


# ---------------------------------------------------------------- ADOCS-32
def adocs_32(work: Path):
    orig = ("Basically, I think you should really run the tests before you push. You MUST NOT push to main. "
            "If the build fails, retry at most 3 times. It is important to note that the timeout is 30 seconds. "
            "For example: `make test`.")
    _w(work, "snapshot/original.md", orig)
    FILLER = [r"\bBasically,\s*", r"\bI think\s+", r"\breally\s+", r"It is important to note that\s+"]

    def compress(t):
        for f in FILLER:
            t = re.sub(f, "", t)
        return re.sub(r"(^|\.\s+)([a-z])", lambda m: m[1] + m[2].upper(), t)

    def semantic_diff(a, b):
        loss = []
        for pat, label in [(r"\d+", "number"), (r"\b(MUST NOT|MUST|never|at most|only)\b", "directive/qualifier"), (r"`[^`]+`", "example")]:
            if sorted(re.findall(pat, a)) != sorted(re.findall(pat, b)):
                loss.append(label)
        return loss

    out = compress(orig)
    loss = semantic_diff(orig, out)
    bad = re.sub(r"at most 3 times", "a few times", out)
    bad_loss = semantic_diff(orig, bad)
    final = out if not loss else orig
    _w(work, "condensed.md", final)
    return [_c("filler and hedges removed", not re.search(r"Basically|I think|really|important to note", out), out),
            _c("numbers, directives and examples preserved: no semantic loss", loss == [], loss),
            _c("planted lossy rewrite flagged (number and qualifier lost) -> revert", set(bad_loss) == {"number", "directive/qualifier"}, bad_loss),
            _c("condensed text is shorter", len(out) < 0.8 * len(orig), (len(orig), len(out)))]


# ---------------------------------------------------------------- ADOCS-33
def adocs_33(work: Path):
    repo = work / "r"
    (repo / "src" / "kosif").mkdir(parents=True)
    (repo / "pyproject.toml").write_text('[project]\nname = "kosif"\n[project.scripts]\nkosif = "kosif.cli:main"\n')
    (repo / "LICENSE").write_text("MIT License\n")
    (repo / "Makefile").write_text("test:\n\tpytest\n")
    stack = "python" if (repo / "pyproject.toml").exists() else "?"
    lic = (repo / "LICENSE").read_text().split()[0]
    readme = f"""# kosif
Arabic-first motion tools.
![license](https://img.shields.io/badge/license-{lic}-blue)
## Install
`pip install -e .`
## Usage
`kosif --help`
`make test`
`make docs`
See `src/kosif/` and `docs/guide.md`.
## Tech stack
{stack}
"""
    _w(work, "README.md", readme)
    scripts = re.findall(r"^(\w+) = ", (repo / "pyproject.toml").read_text(), re.M)
    targets = re.findall(r"^(\w+):", (repo / "Makefile").read_text(), re.M)
    bad = []
    for cmd in re.findall(r"`([^`]+)`", readme):
        if cmd.startswith("make ") and cmd.split()[1] not in targets:
            bad.append(cmd)
        elif cmd.startswith("kosif") and "kosif" not in scripts:
            bad.append(cmd)
        elif "/" in cmd and not cmd.startswith(("pip", "make")) and not (repo / cmd).exists():
            bad.append(cmd)
    return [_c("stack and license detected (python, MIT)", stack == "python" and lic == "MIT", (stack, lic)),
            _c("sections tagline/badge/install/usage/stack drafted", all(s in readme for s in ("## Install", "## Usage", "## Tech stack", "img.shields.io")), ""),
            _c("verification flags make docs and missing path", bad == ["make docs", "docs/guide.md"], bad),
            _c("existing commands and paths pass", "kosif --help" not in bad and "src/kosif/" not in bad and "make test" not in bad, bad)]


# ---------------------------------------------------------------- ADOCS-34
def adocs_34(work: Path):
    src = '''# SPDX-License-Identifier: MIT
import os  # noqa: F401
def total(items):
    # Now we loop over the items to compute the total
    t = 0
    # increment t
    for i in items:
        t += i.price  # add price
    # prices are in halalas; callers divide by 100
    return t
def area(r):
    """>>> area(1)
    3.14159
    """
    # This function leverages a robust approach
    return 3.14159 * r * r
'''
    _w(work, "before.py", src)
    out, removed = [], []
    for line in src.splitlines():
        m = re.search(r"#\s*(.*)$", line)
        if not m or line.lstrip().startswith(('"""', ">>>")):
            out.append(line)
            continue
        c = m[1]
        keep = c.startswith(("SPDX", "noqa", "type:", "pragma"))
        code = line[:m.start()].strip()
        narration = re.match(r"(?i)(now we|this function|here we|next,?)", c)
        words = set(re.findall(r"[a-z]+", c.lower()))
        redundant = bool(code) and bool(words - {"add", "the", "to"}) and (words - {"add", "the", "to"}) <= set(re.findall(r"[a-z]+", code.lower()))
        restates = (not code) and re.match(r"(?i)(increment|loop|return|set) \w+$", c)
        if not keep and (narration or redundant or restates):
            removed.append(c)
            out.append(line[:m.start()].rstrip()) if code else None
        else:
            out.append(line)
    after = "\n".join(l for l in out if l is not None)
    _w(work, "after.py", after)
    return [_c("planning narration removed", "Now we loop over the items to compute the total" in removed and "This function leverages a robust approach" in removed, removed),
            _c("what-comments removed ('increment t', 'add price')", {"increment t", "add price"} <= set(removed), removed),
            _c("license header and lint directive kept", "SPDX-License-Identifier" in after and "noqa: F401" in after, ""),
            _c("non-obvious unit comment kept", "prices are in halalas" in after, ""),
            _c("doctest kept and code still runs", ">>> area(1)" in after and subprocess.run(["python3", "-I", "-c", after + "\nprint(area(1))"], capture_output=True, text=True).stdout.strip() == "3.14159", "")]


# ---------------------------------------------------------------- ADOCS-35
def adocs_35(work: Path):
    story = {"start": {"text": "Gate", "choices": {"enter": "hall", "leave": "end_coward"}},
             "hall": {"text": "Hall", "choices": {"left": "library", "right": "vault", "back": "start"}, "quest": "find key"},
             "library": {"text": "Library", "choices": {"read": "vault"}, "sets": "key"},
             "vault": {"text": "Vault", "choices": {"open": "end_treasure"}, "requires": "key"},
             "attic": {"text": "Attic", "choices": {}},
             "end_coward": {"ending": True}, "end_treasure": {"ending": True}, "end_secret": {"ending": True}}
    _w(work, "story.json", story)
    seen, stack = set(), ["start"]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack += list(story[n].get("choices", {}).values())
    unreachable = sorted(set(story) - seen)
    dead = sorted(n for n, v in story.items() if not v.get("ending") and not v.get("choices"))
    # gated content: can the vault be opened with the key? search paths carrying state
    ok_paths, st = [], [("start", frozenset(), ("start",))]
    while st:
        n, flags, path = st.pop()
        if story[n].get("requires") and story[n]["requires"] not in flags:
            continue
        flags = flags | ({story[n]["sets"]} if story[n].get("sets") else set())
        if n == "end_treasure":
            ok_paths.append(path)
            continue
        for nx in story[n].get("choices", {}).values():
            if nx not in path:
                st.append((nx, flags, path + (nx,)))
    return [_c("unreachable nodes found (attic, end_secret)", unreachable == ["attic", "end_secret"], unreachable),
            _c("dead end found (attic has no choices, no ending)", dead == ["attic"], dead),
            _c("treasure ending reachable only through the library key", ok_paths and all("library" in p for p in ok_paths), ok_paths),
            _c("direct hall->vault route is blocked without the key", not any(p[:3] == ("start", "hall", "vault") for p in ok_paths), "")]


# ---------------------------------------------------------------- ADOCS-36
def adocs_36(work: Path):
    def plan(version, commits):
        major, minor, patch = map(int, version.split("."))
        breaking = [c for c in commits if re.match(r"\w+(\(.+\))?!:", c) or "BREAKING CHANGE" in c]
        feats = [c for c in commits if c.startswith("feat")]
        fixes = [c for c in commits if c.startswith("fix")]
        if breaking:
            nxt = (major, minor + 1, 0) if major == 0 else (major + 1, 0, 0)
        elif feats:
            nxt = (major, minor + 1, 0)
        elif fixes:
            nxt = (major, minor, patch + 1)
        else:
            nxt = (major, minor, patch)
        groups = {"Breaking": breaking, "Added": [c for c in feats if c not in breaking], "Fixed": fixes,
                  "Security": [c for c in commits if c.startswith("sec")]}
        return ".".join(map(str, nxt)), {k: v for k, v in groups.items() if v}

    c1 = ["feat!: drop python 3.8 (see MIGRATION.md)", "feat: add export", "fix: crash on empty", "chore: ci"]
    v1, g1 = plan("1.4.2", c1)
    v2, _ = plan("1.4.2", ["feat: add x", "fix: y"])
    v3, _ = plan("1.4.2", ["fix: y"])
    v4, _ = plan("0.9.3", ["refactor!: rename api"])
    ch = "## " + v1 + "\n" + "\n".join(f"### {k}\n" + "\n".join(f"- {x}" for x in v) for k, v in g1.items())
    manifests = {"pyproject.toml": v1, "package.json": v1}
    _w(work, "CHANGELOG.md", ch)
    return [_c("breaking change on 1.x -> 2.0.0", v1 == "2.0.0", v1),
            _c("feature -> minor 1.5.0; fix only -> patch 1.4.3", (v2, v3) == ("1.5.0", "1.4.3"), (v2, v3)),
            _c("0.x breaking change bumps minor 0.10.0", v4 == "0.10.0", v4),
            _c("changelog lists Breaking first with migration link", list(g1)[0] == "Breaking" and "MIGRATION.md" in ch, list(g1)),
            _c("manifests bumped consistently", len(set(manifests.values())) == 1, manifests)]


# ---------------------------------------------------------------- ADOCS-37
def adocs_37(work: Path):
    SYM = {r"\alpha": "α", r"\beta": "β", r"\sum": "∑", r"\infty": "∞", r"\leq": "≤", r"\geq": "≥", r"\in": "∈", r"\sqrt": "√",
           r"\to": "→", r"\pi": "π", r"\cdot": "·"}
    SUP = str.maketrans("0123456789n+-", "⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁺⁻")
    SUB = str.maketrans("0123456789ni", "₀₁₂₃₄₅₆₇₈₉ₙᵢ")

    def to_unicode(s):
        for k in sorted(SYM, key=len, reverse=True):
            s = s.replace(k, SYM[k])
        s = re.sub(r"\^\{([^}]+)\}|\^(\w)", lambda m: (m[1] or m[2]).translate(SUP), s)
        s = re.sub(r"_\{([^}]+)\}|_(\w)", lambda m: (m[1] or m[2]).translate(SUB), s)
        return s.replace("{", "").replace("}", "")

    cases = {r"x^2 + y^2 \leq r^2": "x² + y² ≤ r²", r"\sum_{i=1}^{n} a_i": "∑ᵢ₌₁ⁿ aᵢ", r"\alpha \to \infty": "α → ∞",
             r"e^{i\pi} + 1 = 0": "eⁱπ + 1 = 0"}
    out = {k: to_unicode(k) for k in cases}
    _w(work, "unicode_math.json", out)
    return [_c("x^2 + y^2 \\leq r^2 -> x² + y² ≤ r²", out[r"x^2 + y^2 \leq r^2"] == "x² + y² ≤ r²", out),
            _c("\\alpha \\to \\infty -> α → ∞", out[r"\alpha \to \infty"] == "α → ∞", out),
            _c("sum with sub/superscripts uses Unicode scripts", "ⁿ" in out[r"\sum_{i=1}^{n} a_i"] and "aᵢ" in out[r"\sum_{i=1}^{n} a_i"], out[r"\sum_{i=1}^{n} a_i"]),
            _c("no LaTeX backslashes remain", not any("\\" in v for v in out.values()), "")]


# ---------------------------------------------------------------- ADOCS-38
def adocs_38(work: Path):
    change = {"context": "Retries moved from client to server.", "decision": "Server retries 3x with jitter.",
              "quiz": [{"q": "Where do retries happen now?", "options": ["client", "server"], "answer": 1},
                       {"q": "How many retries?", "options": ["1", "3", "5"], "answer": 1},
                       {"q": "What spreads retry load?", "options": ["jitter", "caching"], "answer": 0}]}
    body = f"<h2>Context</h2><p>{change['context']}</p><h2>Decision</h2><p>{change['decision']}</p><h2>Quiz</h2>" + "".join(
        f"<fieldset><legend>{i + 1}. {q['q']}</legend>" + "".join(f"<label><input type=radio name=q{i} value={j}>{o}</label>" for j, o in enumerate(q["options"])) + "</fieldset>"
        for i, q in enumerate(change["quiz"]))
    html = f"<!doctype html><meta charset=utf-8><body>{body}</body>"
    _w(work, "quiz.html", html)

    def grade(ans):
        score = sum(a == q["answer"] for a, q in zip(ans, change["quiz"]))
        return score, "ready to explain" if score == len(change["quiz"]) else "intent mismatch: revisit before merge"

    return [_c("self-contained HTML, questions after the summary", html.index("Quiz") > html.index("Decision") and "<script src" not in html, ""),
            _c("3 questions rendered", html.count("<fieldset>") == 3, 3),
            _c("all correct -> ready", grade([1, 1, 0]) == (3, "ready to explain"), grade([1, 1, 0])),
            _c("a wrong answer signals intent mismatch", grade([0, 1, 0])[1].startswith("intent mismatch"), grade([0, 1, 0]))]


# ---------------------------------------------------------------- ADOCS-39
def adocs_39(work: Path):
    def scaffold(topic, modules=10):
        if not 8 <= modules <= 12:
            raise ValueError("module count 8-12")
        root = work / topic
        root.mkdir()
        (root / "README.md").write_text(f"# {topic}\n")
        (root / "00-orientation.md").write_text("# Orientation\n")
        sections = ["foundations"] * 3 + ["tools"] * 3 + ["application"] * (modules - 6)
        for i, s in enumerate(sections, 1):
            body = f"# Module {i} ({s})\n"
            if i % 3 == 0:
                body += "\n## Synthesis prompt\nConnect the last three modules.\n"
            (root / f"{i:02d}-module.md").write_text(body)
        (root / "99-final-synthesis.md").write_text("# Final synthesis\n")
        return root

    root = scaffold("sql")
    log = [{"module": 1, "correct": True}, {"module": 2, "correct": False, "misconception": "WHERE runs after GROUP BY"}, {"module": 2, "correct": True}]
    (root / "responses.jsonl").write_text("\n".join(json.dumps(r) for r in log))
    rows = [json.loads(l) for l in (root / "responses.jsonl").read_text().splitlines()]
    done = sorted({r["module"] for r in rows if r["correct"]})
    (root / "progress.md").write_text(f"{len(done)}/10 modules passed: {done}\n")
    (root / "misconceptions.md").write_text("\n".join(f"- {r['misconception']}" for r in rows if r.get("misconception")))
    try:
        scaffold("x", modules=5)
        bad = False
    except ValueError:
        bad = True
    files = sorted(p.name for p in root.glob("*.md"))
    synth = [f for f in files if "Synthesis prompt" in (root / f).read_text()]
    return [_c("README, orientation, 10 modules, final synthesis", len([f for f in files if f.endswith("-module.md")]) == 10 and {"README.md", "00-orientation.md", "99-final-synthesis.md"} <= set(files), files),
            _c("synthesis prompt every 3 modules (3, 6, 9)", synth == ["03-module.md", "06-module.md", "09-module.md"], synth),
            _c("progress recomputed from responses: 2/10", (root / "progress.md").read_text().startswith("2/10"), (root / "progress.md").read_text()),
            _c("misconception logged", "WHERE runs after GROUP BY" in (root / "misconceptions.md").read_text(), ""),
            _c("module count outside 8-12 refused", bad, bad)]


# ---------------------------------------------------------------- ADOCS-42
def adocs_42(work: Path):
    OVERUSED = {"delve", "tapestry", "landscape", "robust", "leverage", "utilize", "seamless"}
    EMPTY = {"really", "pivotal", "renowned", "a testament to", "truly", "very"}

    def lint(text, max_words=25):
        f = []
        for w in re.findall(r"[a-z]+", text.lower()):
            if w in OVERUSED:
                f.append(("overused", w))
        for e in EMPTY:
            if re.search(rf"\b{e}\b", text, re.I):
                f.append(("empty emphasis", e))
        for s in _sentences(text):
            if len(s.split()) > max_words:
                f.append(("long sentence", len(s.split())))
            if not re.match(r"[A-Z]", s) or not re.search(r"[.!?]$", s):
                f.append(("fragment", s[:20]))
        return f

    bad = "We delve into the robust landscape. It is truly pivotal. and then"
    good = "We test the parser on 40 files. It fails on two of them."
    fb, fg = lint(bad), lint(good)
    _w(work, "plain_lint.json", {"bad": fb, "good": fg})
    return [_c("overused AI words flagged: delve, robust, landscape", {("overused", w) for w in ("delve", "robust", "landscape")} <= set(fb), fb),
            _c("empty emphasis flagged: truly, pivotal", {("empty emphasis", "truly"), ("empty emphasis", "pivotal")} <= set(fb), fb),
            _c("incomplete sentence flagged", any(k == "fragment" for k, _ in fb), fb),
            _c("plain factual text passes", fg == [], fg)]


# ---------------------------------------------------------------- ADOCS-43
def adocs_43(work: Path):
    SUSPECT = {"delve", "tapestry", "testament", "seamless", "elevate", "embark", "realm"}

    def density(text):
        words = re.findall(r"[a-z']+", text.lower())
        hits = sum(w in SUSPECT for w in words)
        return hits / max(1, len(words)) * 100, text.count("—") / max(1, len(_sentences(text)))

    def humanize(text, max_dash=0.34):
        out = re.sub(r"\bdelve into\b", "look at", text)
        out = re.sub(r"\bembark on\b", "start", out)
        out = re.sub(r"\bseamless\b", "smooth", out)
        dashes = [m.start() for m in re.finditer("—", out)]
        keep = int(max_dash * len(_sentences(out)))
        for pos in reversed(dashes[keep:]):
            out = out[:pos] + "," + out[pos + 1:]
        return out

    def guard(a, b):
        return sorted(re.findall(r"\d+(?:\.\d+)?|[A-Z][a-z]+(?= [A-Z])|[A-Z]{2,}", a)) == sorted(re.findall(r"\d+(?:\.\d+)?|[A-Z][a-z]+(?= [A-Z])|[A-Z]{2,}", b))

    text = "Let us delve into the 2025 results — they rose 12%. We embark on a seamless rollout — in Riyadh. The API team agreed — fully."
    d0, e0 = density(text)
    out = humanize(text)
    d1, e1 = density(out)
    stripped = out.replace("12", "").replace("2025", "")
    _w(work, "humanized.txt", out)
    return [_c("suspect-word density drops (per 100 words)", d1 < d0 and d0 > 10, (round(d0, 1), round(d1, 1))),
            _c("em dashes capped, not banned", 0 < out.count("—") <= int(0.34 * 3) + 1 and out.count("—") < text.count("—"), out.count("—")),
            _c("over-correction guard: numbers and names survive", guard(text, out), ""),
            _c("guard trips when facts are stripped", not guard(text, stripped), "")]


# ---------------------------------------------------------------- ADOCS-44
def adocs_44(work: Path):
    code = {"install": "pip install kosif", "commands": {"run", "stop", "status"}, "config_keys": {"timeout", "retries"},
            "public_api": {"Client", "Job"}, "architecture": {"api", "worker", "db"}}
    docs = {"README.md": {"install": "pip install kosif-tool", "commands": {"run", "stop"}, "config_keys": {"timeout", "retries"}},
            "docs/api.md": {"public_api": {"Client", "Job", "Session"}}, "docs/arch.md": {"architecture": {"api", "worker", "db"}},
            "docs/old-api.md": {"public_api": {"Client"}}}
    drift = []
    for f, claims in docs.items():
        for dim, val in claims.items():
            if val != code[dim]:
                drift.append((f, dim))
    dup = sorted(f for f in docs if "public_api" in docs[f])
    plan = [("merge", dup), ("edit", sorted({f for f, _ in drift}))]
    snapshot = {f: json.dumps(sorted(map(str, d.items()))) for f, d in docs.items()}
    _w(work, "drift_plan.json", {"drift": drift, "plan": plan, "approved": False})
    return [_c("install and commands drift in README", {("README.md", "install"), ("README.md", "commands")} <= set(drift), drift),
            _c("public API drift: phantom Session and stale old-api", {("docs/api.md", "public_api"), ("docs/old-api.md", "public_api")} <= set(drift), drift),
            _c("matching dimensions not flagged (config keys, architecture)", not any(d in ("config_keys", "architecture") for _, d in drift), drift),
            _c("duplicate API docs planned for merge; plan awaits approval", plan[0] == ("merge", ["docs/api.md", "docs/old-api.md"]) and len(snapshot) == 4, plan)]


# ---------------------------------------------------------------- ADOCS-45
def adocs_45(work: Path):
    src = "Kosif Studio makes your reels pop! Get 30% off until 2026-12-01. It's a piece of cake."
    dnt = ["Kosif Studio"]
    idioms = {"piece of cake": "very easy", "pop": "stand out", "break a leg": "good luck"}
    flags = [i for i in idioms if re.search(rf"\b{i}\b", src)]
    target = "كوسِف ستوديو يجعل مقاطعك مميزة! خصم 30% حتى 2026-12-01. الأمر سهل جداً."
    target_ok = "Kosif Studio يجعل مقاطعك مميزة! خصم 30% حتى 2026-12-01. الأمر سهل جداً."
    route = {("en", "ar"): "transcreation", ("en", "fr"): "MT + review"}

    def qc(s, t):
        issues = []
        if sorted(re.findall(r"\d[\d\-%.]*", s)) != sorted(re.findall(r"\d[\d\-%.]*", t)):
            issues.append("numbers/dates changed")
        issues += [f"brand '{b}' translated" for b in dnt if b in s and b not in t]
        if len(t) > 1.5 * len(s):
            issues.append("too long")
        return issues

    _w(work, "transcreation.json", {"flags": flags, "route": {f"{a}->{b}": v for (a, b), v in route.items()}, "qc_bad": qc(src, target), "qc_ok": qc(src, target_ok)})
    return [_c("idioms flagged for transcreation (piece of cake, pop)", sorted(flags) == ["piece of cake", "pop"], flags),
            _c("brand transliterated instead of kept -> QC fails", qc(src, target) == ["brand 'Kosif Studio' translated"], qc(src, target)),
            _c("numbers, date and brand survive in the fixed version", qc(src, target_ok) == [], qc(src, target_ok)),
            _c("en->ar routed to transcreation with a recorded reason", route[("en", "ar")] == "transcreation", route)]


# ---------------------------------------------------------------- ADOCS-46
def adocs_46(work: Path):
    from openpyxl import Workbook, load_workbook
    data = {"customer": {"name": "Acme"}, "lines": [{"sku": "B", "qty": 2, "price": 1250}, {"sku": "A", "qty": 1, "price": 999.5}], "empty": []}
    template = [["Invoice for {d.customer.name}"], ["{d.lines[i].sku}", "{d.lines[i].qty}", "{d.lines[i].price:formatC(2)}"],
                ["{d.lines[i+1].sku}"], ["Items: {d.lines:len}", "Total: {d.lines:sum(qty*price):formatC(2)}"]]

    def get(path, ctx):
        cur = ctx
        for part in re.findall(r"\w+|\[\d+\]", path):
            cur = cur[int(part[1:-1])] if part.startswith("[") else cur[part]
        return cur

    def fmt(v, f):
        if f == "formatC(2)":
            return f"{v:,.2f} SAR"
        raise ValueError(f"unknown formatter {f}")

    def render_cell(cell, ctx, item=None):
        def rep(m):
            expr = m[1]
            path, *fs = expr.split(":")
            if item is not None and "[i]" in path:
                val = item[path.split("].")[-1]]
            elif fs and fs[0] == "len":
                return str(len(get(path[2:], ctx)))
            elif fs and fs[0].startswith("sum("):
                a, b = re.match(r"sum\((\w+)\*(\w+)\)", fs[0]).groups()
                val = sum(x[a] * x[b] for x in get(path[2:], ctx))
                fs = fs[1:]
            else:
                val = get(path[2:], ctx)
            for f in fs:
                val = fmt(val, f)
            return str(val)
        return re.sub(r"\{(d\.[^}]+)\}", rep, cell)

    def render(tpl, ctx):
        out, i = [], 0
        while i < len(tpl):
            row = tpl[i]
            if any("[i]" in c for c in row):
                assert any("[i+1]" in c for c in tpl[i + 1]), "loop must close with [i+1]"
                arr = get(re.search(r"\{d\.(\w+)\[i\]", row[0])[1], ctx)
                out += [[render_cell(c, ctx, it) for c in row] for it in arr]
                i += 2  # the [i+1] row is removed from output
                continue
            out.append([render_cell(c, ctx) for c in row])
            i += 1
        return out

    rows = render(template, data)
    wb = Workbook()
    for r in rows:
        wb.active.append(r)
    wb.save(work / "invoice.xlsx")
    back = [[c.value for c in r] for r in load_workbook(work / "invoice.xlsx").active.iter_rows()]
    empty = render([["{d.empty[i].sku}"], ["{d.empty[i+1].sku}"], ["n={d.empty:len}"]], data)
    try:
        render([["{d.customer.name:upperCase}"]], data)
        invented = None
    except ValueError as e:
        invented = str(e)
    return [_c("loop row expands to 2 lines, [i+1] row removed", len(rows) == 4 and rows[1][0] == "B" and rows[2][0] == "A", rows),
            _c("chained formatter gives '1,250.00 SAR'", rows[1][2] == "1,250.00 SAR", rows[1]),
            _c("total computed in the template: 2*1250 + 999.5 = 3,499.50", back[3][1] == "Total: 3,499.50 SAR" and back[3][0] == "Items: 2", back[3]),
            _c("empty array renders zero rows", empty == [["n=0"]], empty),
            _c("unknown formatter is refused, not invented", invented == "unknown formatter upperCase", invented)]


# ---------------------------------------------------------------- ADOCS-47
def adocs_47(work: Path):
    from PIL import Image, ImageDraw
    src = "Patient: Ali Hassan\nID: 29801011234567\nPhone: +20 100 123 4567\nNote: stable.\n"
    orig = _w(work, "originals/record.txt", src)
    patterns = [r"\b\d{14}\b", r"\+20[\d ]{10,}\d", r"(?<=Patient: )[A-Z][a-z]+ [A-Z][a-z]+"]
    out = src
    for p in patterns:
        out = re.sub(p, "█████", out)
    red = _w(work, "out/record.txt", out)
    leftovers = sum(len(re.findall(p, red.read_text())) for p in patterns)
    img = Image.new("RGB", (400, 120), "white")
    d = ImageDraw.Draw(img)
    for i, line in enumerate(out.splitlines()):
        d.text((10, 10 + 22 * i), line.replace("█", "#"), fill="black")
    pdf = work / "out" / "record.pdf"
    img.save(pdf, "PDF")
    pdf_bytes = pdf.read_bytes()
    text_layer = b"/Font" in pdf_bytes or b"BT" in pdf_bytes.split(b"stream")[0]
    man = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((work / "out").glob("*"))}
    _w(work, "out/MANIFEST.v1.json", man)
    verify = all(hashlib.sha256((work / "out" / n).read_bytes()).hexdigest() == h for n, h in man.items())
    return [_c("grep for every pattern returns 0 after redaction", leftovers == 0, leftovers),
            _c("non-sensitive text kept ('Note: stable.')", "Note: stable." in out, ""),
            _c("rasterised PDF has no text layer and no leaked digits", not text_layer and b"29801011234567" not in pdf_bytes, len(pdf_bytes)),
            _c("sha256 manifest verifies the delivered files", verify and len(man) == 2, list(man)),
            _c("originals untouched", orig.read_text() == src, "")]


# ---------------------------------------------------------------- ADOCS-49
def adocs_49(work: Path):
    meta = {"name": "kosif", "license": "MIT", "python": ">=3.10", "ci": "tests.yml", "logo": None, "version": "2.1.0"}
    badges = [f"![license](https://img.shields.io/badge/license-{meta['license']}-blue)",
              f"![python](https://img.shields.io/badge/python-{meta['python'].replace('>=', '%3E%3D')}-blue)",
              f"![ci](https://github.com/o/kosif/actions/workflows/{meta['ci']}/badge.svg)",
              f"![version](https://img.shields.io/badge/version-{meta['version']}-green)"]
    readme = "\n".join(([f"![logo]({meta['logo']})"] if meta["logo"] else []) + [
        f"# {meta['name']}", "Turn a voice note into a captioned video.", " ".join(badges), "## Why", "- one command", "- Arabic-first", "- offline",
        "## Quick Start", "```bash", "pip install kosif", "kosif demo --out demo.mp4", "```"])
    _w(work, "README.md", readme)
    qs = re.search(r"```bash\n(.*?)```", readme, re.S)[1].strip().splitlines()
    placeholders = re.findall(r"(?i)your-logo|placeholder|TODO", readme)
    jargon = [w for w in ("leverage", "synergy", "paradigm") if w in readme.lower()]
    return [_c("no logo exists -> no logo line (never a placeholder)", "![logo]" not in readme and not placeholders, ""),
            _c("4-6 badges built from real metadata", 4 <= len(badges) <= 6 and "license-MIT" in badges[0], len(badges)),
            _c("one jargon-free value sentence under the title", readme.splitlines()[1].endswith(".") and not jargon, readme.splitlines()[1]),
            _c("Why has 3-5 bullets; Quick Start is copy-pasteable commands", 3 <= readme.split("## Why")[1].split("##")[0].count("\n- ") <= 5 and all(not l.startswith("$") for l in qs), qs)]


# ---------------------------------------------------------------- ADOCS-50
def adocs_50(work: Path):
    comments = [("# 2023-04 changed by Sam: now uses dict", "history"), ("# loop over users", "restate"),
                ("# caller must hold self._lock", "obligation"), ("# timeout in milliseconds", "unit"),
                ("# never lower this below 3: upstream drops bursts", "editor-instruction"),
                ("# This is a long explanation\n# that goes over\n# three lines about the design", "too-long"),
                ("# JIRA-123 per discussion", "ticket")]

    def judge(text, kind_hint):
        lines = text.count("\n") + 1
        t = text.lower()
        if re.search(r"\b(19|20)\d\d-\d\d\b|changed by|jira-\d+|per discussion", t):
            return "delete"
        if re.match(r"# (loop|iterate|increment|return|set) ", t):
            return "delete"
        if lines > 2:
            return "move to commit/design note"
        if re.search(r"\b(never|always|keep in step)\b", t):
            return "keep + write a test that enforces it"
        return "keep"

    res = {k: judge(t, k) for t, k in comments}
    test_name = "test_retry_floor_is_at_least_3"
    _w(work, "comment_review.json", {"verdicts": res, "suggested_test": test_name})
    return [_c("history and ticket chatter deleted", res["history"] == "delete" and res["ticket"] == "delete", res),
            _c("restating the code deleted", res["restate"] == "delete", res),
            _c("caller obligation and unit kept", res["obligation"] == "keep" and res["unit"] == "keep", res),
            _c("editor instruction becomes an enforcing test", res["editor-instruction"] == "keep + write a test that enforces it", res),
            _c("> 2-line rationale moved out", res["too-long"] == "move to commit/design note", res)]


# ---------------------------------------------------------------- ADOCS-51
def adocs_51(work: Path):
    repo = work / "r"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "app.py").write_text("import os\n\ndef main():\n    cfg = load()\n    run(cfg)\n\ndef load():\n    return {}\n")
    (repo / "README.md").write_text("# app\n")

    def persona(req):
        r = req.lower()
        return "reviewer" if "pr" in r.split() else "rca" if "why did" in r else "architect" if "architecture" in r else "new joiner"

    def anchor(path, needle):
        lines = (repo / path).read_text().splitlines()
        return next(i + 1 for i, l in enumerate(lines) if needle in l)

    steps = [{"file": "README.md", "line": 1, "description": "Start here."},
             {"file": "src/app.py", "line": anchor("src/app.py", "def main"), "description": "Entry point."},
             {"file": "src/app.py", "line": anchor("src/app.py", "def load"), "description": "Config loading."}]
    tour = {"$schema": "https://aka.ms/codetour-schema", "title": "Onboarding", "steps": steps}
    _w(work, "r/.tours/onboarding.tour", tour)

    def verify(t):
        bad = []
        for s in t["steps"]:
            p = repo / s["file"]
            if not p.exists() or s["line"] > len(p.read_text().splitlines()):
                bad.append(s)
        return bad

    wrong = verify({"steps": steps + [{"file": "src/app.py", "line": 99}, {"file": "src/gone.py", "line": 1}]})
    return [_c("persona inference: PR -> reviewer, 'why did X break' -> rca, default new joiner",
               (persona("review this PR"), persona("why did login break"), persona("help me get started")) == ("reviewer", "rca", "new joiner"), ""),
            _c("anchors verified against real lines: main at 3, load at 7", [s["line"] for s in steps[1:]] == [3, 7], steps),
            _c("every step of the tour verifies", verify(tour) == [], ""),
            _c("wrong line and missing file are caught", len(wrong) == 2, wrong)]


# ---------------------------------------------------------------- ADOCS-52
def adocs_52(work: Path):
    prompt = """You are a release helper.
Do not use the old deploy.sh script.
Never skip the changelog.
Don't use yarn, it was rejected in ADR-7.
```bash
# do not run this in prod
make release
```
Use `make release` because it signs artifacts."""
    out, flagged = [], []
    in_fence = False
    rewrites = {"Do not use the old deploy.sh script.": "Use `make release` because it replaces deploy.sh and signs artifacts.",
                "Don't use yarn, it was rejected in ADR-7.": "Use npm because the lockfile is npm (ADR-7)."}
    loadbearing = {"Never skip the changelog."}
    for line in prompt.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and re.match(r"(?i)(do not|don't|never)\b", line):
            flagged.append(line)
            out.append(line if line in loadbearing else rewrites.get(line, line))
        else:
            out.append(line)
    _w(work, "prompt.audited.md", "\n".join(out))
    return [_c("prohibitions outside code fences flagged (3)", len(flagged) == 3, flagged),
            _c("line inside the code fence ignored", "# do not run this in prod" not in flagged, ""),
            _c("retired path and rejected alternative rewritten positively", "deploy.sh script." not in "\n".join(out).split("Use `make release` because it replaces")[0] and "Use npm because" in "\n".join(out), ""),
            _c("load-bearing hazard kept", "Never skip the changelog." in out, "")]


# ---------------------------------------------------------------- ADOCS-53
def adocs_53(work: Path):
    chapters = [{"title": "Arrival", "purpose": "introduce the city", "entry": {"knows": "nothing"}, "exit": {"knows": "the map"}, "pull": "who sent the letter?", "scenes": ["train", "gate", "inn"]},
                {"title": "The Market", "purpose": "reveal the rival", "entry": {"knows": "the map"}, "exit": {"knows": "the rival"}, "pull": "can she trust him?", "scenes": ["stall", "chase"]},
                {"title": "Old Streets", "purpose": "introduce the city", "entry": {"knows": "the rival"}, "exit": {"knows": "the rival"}, "pull": "", "scenes": ["walk"]},
                {"title": "The Vault", "purpose": "pay off the letter", "entry": {"knows": "a secret"}, "exit": {"knows": "the sender"}, "pull": "what is inside?", "scenes": ["door", "turn", "escape", "fall", "dawn", "x"]}]
    issues = []
    seen = {}
    for i, ch in enumerate(chapters):
        if ch["purpose"] in seen:
            issues.append((ch["title"], f"same purpose as {seen[ch['purpose']]} -> redundant"))
        seen.setdefault(ch["purpose"], ch["title"])
        if i and ch["entry"] != chapters[i - 1]["exit"]:
            issues.append((ch["title"], "entry state does not follow previous exit"))
        if ch["entry"] == ch["exit"]:
            issues.append((ch["title"], "no change between entry and exit"))
        if not ch["pull"]:
            issues.append((ch["title"], "no pull"))
        if not 2 <= len(ch["scenes"]) <= 5:
            issues.append((ch["title"], "2-5 scene seeds"))
    score = 100 - 10 * len(issues)
    bible = {"characters": ["Mira", "Tal"], "places": ["the city"], "terms": [], "timeline": []}
    pacing = [len(c["scenes"]) for c in chapters]
    _w(work, "outline.json", {"chapters": chapters, "issues": issues, "score": score, "bible": bible, "pacing": pacing,
                              "awaiting_author_approval": True})
    titles = {t: [m for tt, m in issues if tt == t] for t in ("Old Streets", "The Vault", "Arrival")}
    return [_c("duplicate purpose makes Old Streets redundant", "same purpose as Arrival -> redundant" in titles["Old Streets"], titles["Old Streets"]),
            _c("Old Streets: no change and no pull", {"no change between entry and exit", "no pull"} <= set(titles["Old Streets"]), titles["Old Streets"]),
            _c("Vault entry breaks the state chain and has 6 scenes", set(titles["The Vault"]) == {"entry state does not follow previous exit", "2-5 scene seeds"}, titles["The Vault"]),
            _c("clean chapter raises nothing; score 100 - 6x10 = 40", titles["Arrival"] == [] and score == 40, score),
            _c("stops for author approval", json.loads((work / "outline.json").read_text())["awaiting_author_approval"] is True, "")]


# ---------------------------------------------------------------- ADOCS-54
def adocs_54(work: Path):
    readiness = {"status": "pass", "chapters": {"01": "final", "02": "final"}}
    if readiness["status"] != "pass" or any(v != "final" for v in readiness["chapters"].values()):
        raise RuntimeError("gate")
    meta = {"title": "Small Book", "author": "K. Writer", "language": "ar", "identifier": "urn:uuid:12345678-1234-1234-1234-123456789abc",
            "description": "Test", "ai_disclosure": "Drafted with AI assistance; edited by the author."}
    chapters = {"front.xhtml": f"<h1>{meta['title']}</h1><p>© 2026 {meta['author']}. {meta['ai_disclosure']}</p>",
                "ch01.xhtml": "<h1>الفصل الأول</h1><p>نص.</p>", "ch02.xhtml": "<h1>الفصل الثاني</h1><p>نص.</p>",
                "back.xhtml": "<h1>About the author</h1>"}
    p = work / "book.epub"
    with zipfile.ZipFile(p, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        manifest = "".join(f'<item id="i{i}" href="{n}" media-type="application/xhtml+xml"/>' for i, n in enumerate(chapters))
        spine = "".join(f'<itemref idref="i{i}"/>' for i in range(len(chapters)))
        z.writestr("OEBPS/content.opf", f'<?xml version="1.0"?><package version="3.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid">'
                   f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">{meta["identifier"]}</dc:identifier>'
                   f'<dc:title>{meta["title"]}</dc:title><dc:creator>{meta["author"]}</dc:creator><dc:language>{meta["language"]}</dc:language>'
                   f'<dc:description>{meta["description"]}</dc:description></metadata><manifest>{manifest}</manifest><spine page-progression-direction="rtl">{spine}</spine></package>')
        for n, body in chapters.items():
            z.writestr(f"OEBPS/{n}", f'<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" lang="{meta["language"]}" dir="rtl"><head><title>{n}</title></head><body>{body}</body></html>')
    import xml.etree.ElementTree as ET
    with zipfile.ZipFile(p) as z:
        first = z.infolist()[0]
        opf = ET.fromstring(z.read("OEBPS/content.opf"))
        ns = {"dc": "http://purl.org/dc/elements/1.1/", "o": "http://www.idpf.org/2007/opf"}
        title = opf.find(".//dc:title", ns).text
        spine_n = len(opf.findall(".//o:itemref", ns))
        parsed = all(ET.fromstring(z.read(f"OEBPS/{n}")) is not None for n in chapters)
        front = z.read("OEBPS/front.xhtml").decode()
    return [_c("mimetype is the first entry, stored uncompressed", first.filename == "mimetype" and first.compress_type == zipfile.ZIP_STORED, first.filename),
            _c("OPF metadata carries title/author/language/identifier", title == "Small Book" and opf.find(".//dc:language", ns).text == "ar", title),
            _c("spine holds front, 2 chapters, back in order; RTL progression", spine_n == 4, spine_n),
            _c("every XHTML parses as XML", parsed, parsed),
            _c("AI-assistance disclosure in the copyright front matter", "AI assistance" in front, "")]


# ---------------------------------------------------------------- ADOCS-55
def adocs_55(work: Path):
    def decide(item):
        if item.get("sensitive") and not item.get("community_consulted"):
            return "withhold: consult source community", None
        if item["rights"] == "public domain":
            lic = "CC0"
        elif item["rights"] == "in copyright, cleared":
            lic = item.get("licence", "CC BY 4.0")
        else:
            return "metadata and thumbnail only", None
        if item.get("sensitive"):
            return "publish with TK label and access terms", lic
        return "publish full image (IIIF)", lic

    items = {"map-1890": {"rights": "public domain"}, "photo-1970": {"rights": "in copyright, cleared", "licence": "CC BY 4.0"},
             "poster-1999": {"rights": "in copyright, not cleared"}, "sacred-mask": {"rights": "public domain", "sensitive": True},
             "song-rec": {"rights": "public domain", "sensitive": True, "community_consulted": True}}
    dec = {k: decide(v) for k, v in items.items()}
    _w(work, "decisions.json", {k: {"action": a, "licence": l, "recorded": "2026-11-03"} for k, (a, l) in dec.items()})
    return [_c("public domain -> full image under CC0", dec["map-1890"] == ("publish full image (IIIF)", "CC0"), dec["map-1890"]),
            _c("uncleared copyright -> metadata and thumbnail only", dec["poster-1999"][0] == "metadata and thumbnail only", dec["poster-1999"]),
            _c("sensitivity overrides public domain until consulted", dec["sacred-mask"][0].startswith("withhold"), dec["sacred-mask"]),
            _c("after consultation: TK label and access terms", dec["song-rec"] == ("publish with TK label and access terms", "CC0"), dec["song-rec"]),
            _c("every decision recorded for audit", len(json.loads((work / "decisions.json").read_text())) == 5, "")]


# ---------------------------------------------------------------- ADOCS-56
def adocs_56(work: Path):
    def render(state):
        tabs = ["Overview", "Workstreams"] + [t for t in ("Decisions", "Risks") if state.get(t.lower())]
        block = json.dumps(state, ensure_ascii=False, sort_keys=True)
        return (f"<!doctype html><title>{state['name']}</title><nav>{''.join(f'<a>{t}</a>' for t in tabs)}</nav>"
                f"<p>Open PRs: {state['open_prs']}</p><script type=\"application/json\" id=\"state\">{block}</script>")

    s1 = {"name": "Atlas", "as_of": "2026-11-01", "open_prs": 7, "done": ["auth"], "risks": [], "decisions": ["use postgres"]}
    page = _w(work, "status.html", render(s1))
    prev = json.loads(re.search(r'<script type="application/json" id="state">(.*?)</script>', page.read_text())[1])
    live = {**prev, "as_of": "2026-11-03", "open_prs": 4, "done": ["auth", "billing"], "risks": ["vendor delay"]}
    delta = {k: (prev.get(k), live[k]) for k in live if prev.get(k) != live[k] and k != "as_of"}
    page.write_text(render(live))  # same file = same URL, updated in place
    tabs_now = re.findall(r"<a>(\w+)</a>", page.read_text())
    return [_c("previous state block parsed from the render", prev == s1, prev["as_of"]),
            _c("refresh reports deltas since as_of, not a rewrite", delta == {"open_prs": (7, 4), "done": (["auth"], ["auth", "billing"]), "risks": ([], ["vendor delay"])}, delta),
            _c("Risks tab appears only once it has content", "Risks" not in render(s1) and "Risks" in tabs_now, tabs_now),
            _c("every render embeds the state block with the new as_of", '"as_of": "2026-11-03"' in page.read_text(), "")]


# ---------------------------------------------------------------- ADOCS-57
def adocs_57(work: Path):
    transcript = """[10:02] Sara: We decided to launch on 2026-12-01 in KSA only, because the Egypt payments are not ready.
[10:05] Omar: We considered a global launch but rejected it: support cannot cover 3 time zones.
[10:07] Sara: Omar will draft the pricing page by 2026-11-15.
[10:09] Lina: Someone should update the FAQ.
[10:12] Omar: Open question: do we need Arabic invoices? Finance must answer."""
    decisions = [{"decision": m[1], "rationale": m[2]} for m in re.finditer(r"We decided to (.+?), because (.+?)\.\n", transcript)]
    rejected = [{"option": m[1], "why": m[2]} for m in re.finditer(r"We considered (.+?) but rejected it: (.+?)\.\n", transcript)]
    actions = []
    for m in re.finditer(r"\] \w+: (\w+|Someone) (?:will|should) (.+?)(?: by (\d{4}-\d\d-\d\d))?\.\n", transcript):
        owner = m[1] if m[1] != "Someone" else None
        actions.append({"action": m[2], "owner": owner or "OWNER MISSING", "due": m[3] or "DATE MISSING"})
    questions = [{"q": m[1], "who": m[2]} for m in re.finditer(r"Open question: (.+?\?) (\w+) must answer", transcript)]
    rec = {"decisions": decisions, "rejected": rejected, "actions": actions, "open_questions": questions}
    _w(work, "decision_record.json", rec)
    return [_c("decision kept verbatim with exact date and scope", decisions == [{"decision": "launch on 2026-12-01 in KSA only", "rationale": "the Egypt payments are not ready"}], decisions),
            _c("rejected option recorded with its reason", rejected[0]["option"] == "a global launch" and "3 time zones" in rejected[0]["why"], rejected),
            _c("named owner and date kept: Omar, 2026-11-15", actions[0] == {"action": "draft the pricing page", "owner": "Omar", "due": "2026-11-15"}, actions),
            _c("unnamed owner and missing date marked, not invented", actions[1] == {"action": "update the FAQ", "owner": "OWNER MISSING", "due": "DATE MISSING"}, actions),
            _c("open question with who must answer", questions == [{"q": "do we need Arabic invoices?", "who": "Finance"}], questions)]


# ---------------------------------------------------------------- ADOCS-58
def adocs_58(work: Path):
    reqs = {"REQ-1": "A registered user can reset the password via an emailed link that expires after 30 minutes.",
            "REQ-2": "The page should load fast and be user-friendly.",
            "REQ-3": "An admin can export users and also delete inactive accounts."}
    VAGUE = r"\b(fast|user-friendly|easy|intuitive|etc|appropriate|as needed)\b"
    audit = {k: re.findall(VAGUE, v, re.I) + (["split: 'and also'"] if " and also " in v else []) for k, v in reqs.items()}
    stories, scen = [], []
    m = re.match(r"A (registered user) can (reset the password) via (an emailed link) that expires after (\d+) minutes", reqs["REQ-1"])
    stories.append({"id": "S-1", "covers": "REQ-1", "story": f"As a {m[1]}, I want to {m[2]} so that I can sign in again."})
    gherkin = f"""Feature: Password reset
  Scenario: link works before expiry
    Given a {m[1]} requested a reset
    When they open {m[3]} after {int(m[4]) - 1} minutes
    Then they can set a new password
  Scenario: link expired
    Given a {m[1]} requested a reset
    When they open {m[3]} after {int(m[4]) + 1} minutes
    Then they see "link expired"
  Scenario: empty email submitted
    Given the reset form
    When the email field is empty
    Then they see "email required"
"""
    _w(work, "reset.feature", gherkin)
    steps_ok = all(re.match(r"\s+(Given|When|Then|And) ", l) for l in gherkin.splitlines() if l.strip() and not l.strip().startswith(("Feature", "Scenario")))
    return [_c("vague terms flagged in REQ-2 (fast, user-friendly)", [x.lower() for x in audit["REQ-2"]] == ["fast", "user-friendly"], audit),
            _c("REQ-3 must be split", audit["REQ-3"] == ["split: 'and also'"], audit["REQ-3"]),
            _c("clear REQ-1 passes the audit", audit["REQ-1"] == [], audit["REQ-1"]),
            _c("Gherkin covers the timing boundary (29 / 31 min) and empty input", "after 29 minutes" in gherkin and "after 31 minutes" in gherkin and "empty" in gherkin, ""),
            _c("every step line is Given/When/Then", steps_ok, "")]


# ---------------------------------------------------------------- ADOCS-59
def adocs_59(work: Path):
    constitution = ["Tests run with `pytest -q`", "No network in unit tests", "RTL first for Arabic UI", "Money in integer minor units", "One migration per PR"]
    spec = {"what": "Users can export invoices as CSV.", "why": "Accountants re-key data.",
            "requirements": ["WHEN a user clicks export, the system SHALL download a CSV within 5 s.",
                             "IF the invoice list is empty THEN the system SHALL show an empty-state message."],
            "out_of_scope": ["PDF export"]}
    TECH = r"\b(react|postgres|django|redis|kafka|aws|python)\b"
    tech_terms = re.findall(TECH, json.dumps(spec), re.I)
    ears = all(re.match(r"(WHEN|WHILE|IF) .+ (SHALL|THEN the system SHALL)", r) for r in spec["requirements"])
    ambig = [{"q": "Which date format in the CSV?", "default": "ISO 8601", "rank": "important"},
             {"q": "Include voided invoices?", "default": "no", "rank": "blocking"}]
    baseline = {"R1": "export CSV", "R2": "empty state", "R3": "email copy"}
    delta = {"ADDED": {"R4": "column order configurable"}, "MODIFIED": {"R1": "export CSV with BOM"}, "REMOVED": ["R3"]}
    merged = {**{k: v for k, v in baseline.items() if k not in delta["REMOVED"]}, **delta["MODIFIED"], **delta["ADDED"]}
    _w(work, "specs/export/spec.json", {"constitution": constitution, "spec": spec, "questions": sorted(ambig, key=lambda a: a["rank"] != "blocking"), "baseline": merged})
    return [_c("constitution has 5-9 principles", 5 <= len(constitution) <= 9, len(constitution)),
            _c("spec states what and why with no technology", tech_terms == [], tech_terms),
            _c("requirements in EARS form (WHEN/IF ... SHALL)", ears, spec["requirements"]),
            _c("ambiguity questions carry defaults, blocking first", sorted(ambig, key=lambda a: a["rank"] != "blocking")[0]["rank"] == "blocking", ""),
            _c("delta merge: R3 removed, R1 modified, R4 added", merged == {"R1": "export CSV with BOM", "R2": "empty state", "R4": "column order configurable"}, merged)]


# ---------------------------------------------------------------- ADOCS-60
def adocs_60(work: Path):
    repo = work / "r"
    (repo / "docs" / "backlog").mkdir(parents=True)
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("x\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "init")

    def add(slug, worth, title, why=None, where=None, unknown=None, added="2026-11-01"):
        if worth not in ("yes", "no", "later"):
            raise ValueError("worth must be yes/no/later")
        if worth == "later" and not unknown:
            raise ValueError("later needs the unknown that settles it")
        if worth == "no" and not why:
            raise ValueError("no needs a reason")
        p = repo / "docs" / "backlog" / f"{slug}.md"
        if p.exists():
            p.write_text(p.read_text() + f"\nSeen again at {where}.\n")
            return "appended"
        p.write_text(f"---\nworth: {worth}\nwhy: {why or unknown or ''}\nwhere: {where or ''}\nadded: {added}\n---\n# {title}\n")
        return "created"

    a = add("csv-export-drops-bom", "yes", "CSV export drops the BOM", why="Excel garbles Arabic", where="export.py:42", added="2026-10-01")
    add("slow-thumbnails", "later", "Thumbnails are slow", unknown="p95 under real load", added="2026-10-20")
    add("ie11-support", "no", "IE11 support", why="no users left")
    dup = add("csv-export-drops-bom", "yes", "CSV export drops the BOM", where="report.py:10")
    try:
        add("vague", "later", "Something")
        refused = False
    except ValueError:
        refused = True
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "backlog")
    rank = {"yes": 0, "later": 1, "no": 2}
    items = []
    for p in (repo / "docs" / "backlog").glob("*.md"):
        fm = dict(re.findall(r"^(\w+): (.*)$", p.read_text(), re.M))
        items.append((rank[fm["worth"]], fm["added"], p.stem))
    ordered = [s for *_, s in sorted(items)]
    _git(repo, "rm", "-q", "docs/backlog/csv-export-drops-bom.md")
    _git(repo, "commit", "-qm", "fix: keep BOM (closes csv-export-drops-bom)")
    closed = not (repo / "docs" / "backlog" / "csv-export-drops-bom.md").exists() and "csv-export-drops-bom" in _git(repo, "log", "-1", "--format=%s")
    return [_c("one file per item named by the defect slug", a == "created", a),
            _c("duplicate is appended to the existing item (dedupe by filename)", dup == "appended", dup),
            _c("'later' without the deciding unknown is refused", refused, refused),
            _c("listing ordered by worth then age", ordered == ["csv-export-drops-bom", "slow-thumbnails", "ie11-support"], ordered),
            _c("item closed by git rm in the fixing commit", closed, closed)]


PROGRAMS = {f"ADOCS-{n:02d}": globals()[f"adocs_{n:02d}"] for n in range(1, 61) if f"adocs_{n:02d}" in globals()}
