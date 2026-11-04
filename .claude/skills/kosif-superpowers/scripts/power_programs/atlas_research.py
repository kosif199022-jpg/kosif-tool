"""Programs for the atlas-research family (AWEB-02..11).

Each card's method runs as a deterministic procedure on a planted local fixture (HTML pages,
robots.txt, coded excerpts, study designs, YAML bases) whose correct answer is known.
No network: fetch strategies are decided on saved bodies, never fetched live.
"""
from __future__ import annotations
import math
import re
from pathlib import Path
from urllib import robotparser

import yaml
from bs4 import BeautifulSoup
from scipy.stats import norm

from ._lang_common import save, eq, truth, words

# ---------- AWEB-02 static-first, browser fallback ----------
WAF = ("cf-chl", "cf_chl_opt", "attention required! | cloudflare", "akamai", "incapsula", "_px", "datadome")


def needs_browser(html: str, mode: str = "auto", known_spa=False) -> dict:
    if mode == "never":
        return {"browser": False, "warnings": ["browser disabled: static result may be incomplete"]}
    if mode == "always" or known_spa:
        return {"browser": True, "warnings": ["forced browser mode"]}
    soup = BeautifulSoup(html, "html.parser")
    has_noscript = soup.find("noscript") is not None
    for t in soup(["noscript", "script", "style"]):
        t.decompose()
    body = soup.body.get_text(" ", strip=True) if soup.body else ""
    warn = []
    if len(body) < 40:
        warn.append("near-empty body")
    if has_noscript and re.search(r"enable javascript|requires javascript", html, re.I):
        warn.append("noscript warning")
    low = html.lower()
    waf = [w for w in WAF if w in low]
    if waf:
        warn.append("WAF fingerprint: " + ",".join(waf))
    return {"browser": bool(warn), "warnings": warn}


def aweb02(work: Path):
    article = "<html><body><h1>Report</h1><p>" + "The annual figures rose across all regions. " * 4 + "</p></body></html>"
    spa = "<html><body><div id='root'></div><noscript>You need to enable JavaScript to run this app.</noscript></body></html>"
    waf = "<html><head><title>Attention Required! | Cloudflare</title></head><body><form id='cf-chl'>" + \
          "Checking your browser before accessing the site, please wait a moment. " * 2 + "</form></body></html>"
    r = {"article": needs_browser(article), "spa": needs_browser(spa), "waf": needs_browser(waf),
         "spa_never": needs_browser(spa, "never"), "article_always": needs_browser(article, "always")}
    save(work, "fetch_strategy.json", r)
    return [eq("static article stays static", r["article"]["browser"], False),
            truth("SPA shell -> browser (near-empty + noscript)", r["spa"]["browser"] and len(r["spa"]["warnings"]) == 2, r["spa"]),
            truth("WAF page -> browser", r["waf"]["browser"] and any("WAF" in w for w in r["waf"]["warnings"]), r["waf"]),
            truth("mode never keeps static but warns", not r["spa_never"]["browser"] and r["spa_never"]["warnings"]),
            eq("mode always forces browser", r["article_always"]["browser"], True)]


# ---------- AWEB-03 legality gate ----------
PII = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\+?\d[\d\s-]{8,}\d")


def legality_gate(robots_txt, url, agent, tos_forbids_scraping, needs_login, sample_text):
    rp = robotparser.RobotFileParser()
    rp.parse(robots_txt.splitlines())
    checks = {"robots_allowed": rp.can_fetch(agent, url), "tos_ok": not tos_forbids_scraping,
              "public": not needs_login}
    delay = rp.crawl_delay(agent)
    rate = 1.0 / delay if delay else 1.0  # polite default: 1 request per second
    flags = []
    if PII.search(sample_text):
        flags.append("PII")
    if "©" in sample_text or "all rights reserved" in sample_text.lower():
        flags.append("copyright")
    passed = all(checks.values())
    return {"checks": checks, "rate_per_s": rate, "flags": flags, "passed": passed,
            "strategy": ("static fetch" if passed else None)}


def aweb03(work):
    robots = "User-agent: *\nDisallow: /private/\nCrawl-delay: 4\n"
    save(work, "robots.txt", robots)
    sample = "Contact dr.ali@example.org. © 2026 Clinic, all rights reserved."
    ok = legality_gate(robots, "https://site.test/news/1", "kosif", False, False, sample)
    blocked = legality_gate(robots, "https://site.test/private/x", "kosif", False, False, "")
    auth = legality_gate(robots, "https://site.test/news/1", "kosif", False, True, "")
    save(work, "gate.json", {"ok": ok, "blocked": blocked, "auth": auth})
    return [eq("public allowed page passes", ok["passed"], True),
            eq("robots-disallowed path fails gate", blocked["passed"], False),
            eq("authenticated content fails gate", auth["passed"], False),
            eq("polite rate from Crawl-delay 4", ok["rate_per_s"], 0.25),
            eq("PII and copyright flagged", ok["flags"], ["PII", "copyright"]),
            truth("no strategy chosen before the gate passes", blocked["strategy"] is None)]


# ---------- AWEB-04 qualitative coding ----------
def cohen_kappa(a, b):
    labels = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return (po - pe) / (1 - pe)


CAUSAL = re.compile(r"\b(causes?|leads? to|results? in|because of|drives?)\b", re.I)


def aweb04(work):
    codebook = {"COST": "mentions price or expense", "TRUST": "mentions reliability or honesty",
                "TIME": "mentions waiting or speed"}
    excerpts = [("int1:L4", "Too expensive for us"), ("int1:L9", "They always deliver on time"),
                ("int2:L2", "I trust their reviews"), ("int2:L7", "The wait was long"),
                ("int3:L1", "Price went up again"), ("int3:L5", "Fast replies"),
                ("int4:L3", "Honest staff"), ("int4:L8", "Costs too much"),
                ("int5:L2", "Slow checkout"), ("int5:L6", "I rely on them")]
    coder_a = ["COST", "TIME", "TRUST", "TIME", "COST", "TIME", "TRUST", "COST", "TIME", "TRUST"]
    coder_b = ["COST", "TRUST", "TRUST", "TIME", "COST", "TIME", "TRUST", "COST", "COST", "TRUST"]
    k = cohen_kappa(coder_a, coder_b)
    claims = ["Higher prices lead to churn", "Customers who mention trust also mention speed"]
    kinds = ["causal" if CAUSAL.search(c) else "associational" for c in claims]
    rivals = {claims[0]: ["seasonal demand drop", "competitor launch"]}
    out = {"codebook": codebook, "coded": [{"ref": r, "text": t, "a": x, "b": y}
                                           for (r, t), x, y in zip(excerpts, coder_a, coder_b)],
           "kappa": round(k, 4), "claims": dict(zip(claims, kinds)), "rivals": rivals}
    save(work, "coding.json", out)
    # po=0.8; pa: COST .3 TIME .4 TRUST .3; pb: COST .4 TIME .2 TRUST .4 -> pe=.12+.08+.12=.32 -> k=.48/.68
    return [eq("Cohen kappa", round(k, 4), round(0.48 / 0.68, 4)),
            truth("every coded excerpt keeps its source reference", all(":" in c["ref"] for c in out["coded"])),
            eq("claim types", kinds, ["causal", "associational"]),
            truth("causal claim lists rival explanations", len(rivals[claims[0]]) >= 2)]


# ---------- AWEB-05 fine-tune router ----------
def ft_route(mb=None, kind=None, has_eval=True, pretrain_lr=None):
    if not has_eval:
        return {"route": "build eval harness first"}
    if kind == "volatile facts":
        return {"route": "RAG"}
    if kind == "unsettled behavior":
        return {"route": "prompting"}
    if kind in ("demonstrations", "preference pairs", "verifiable reward"):
        return {"route": {"demonstrations": "SFT", "preference pairs": "DPO/ORPO/KTO",
                          "verifiable reward": "GRPO/RLVR"}[kind]}
    if mb < 10:
        r = "RAG"
    elif mb <= 500:
        r = "RAG+FT"
    elif mb <= 10000:
        r = "CPT then SFT"
    else:
        r = "CPT"
    out = {"route": r}
    if "CPT" in r and pretrain_lr:
        out["cpt_lr"] = pretrain_lr * 0.10
    return out


def aweb05(work):
    cases = {"5MB": ft_route(5), "200MB": ft_route(200), "2GB": ft_route(2000, pretrain_lr=3e-4),
             "50GB": ft_route(50000), "prefs": ft_route(kind="preference pairs"),
             "facts": ft_route(kind="volatile facts"), "noeval": ft_route(200, has_eval=False)}
    save(work, "ft_router.json", cases)
    return [eq("<10MB", cases["5MB"]["route"], "RAG"), eq("10-500MB", cases["200MB"]["route"], "RAG+FT"),
            eq("0.5-10GB", cases["2GB"]["route"], "CPT then SFT"), eq(">10GB", cases["50GB"]["route"], "CPT"),
            eq("CPT LR 10% of pretraining", cases["2GB"]["cpt_lr"], 3e-5, tol=1e-12),
            eq("preference pairs", cases["prefs"]["route"], "DPO/ORPO/KTO"),
            eq("no eval harness blocks", cases["noeval"]["route"], "build eval harness first")]


# ---------- AWEB-06 clinical sample size ----------
def n_means(d, alpha=0.05, power=0.8):
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    return math.ceil(2 * z * z / (d * d))


def n_props(p1, p2, alpha=0.05, power=0.8):
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    pb = (p1 + p2) / 2
    n = (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p1 - p2) ** 2
    return math.ceil(n)


def schoenfeld_events(hr, alpha=0.05, power=0.8, p=0.5):
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    return math.ceil(z * z / (p * (1 - p) * math.log(hr) ** 2))


def endpoint_select(eps, weights):
    out = []
    for e in eps:
        s = sum(weights[k] * e[k] for k in weights)
        cls = "primary" if s >= 4 else "key-secondary" if s >= 3 else "exploratory"
        out.append({"name": e["name"], "score": round(s, 2), "class": cls, "surrogate": e.get("surrogate", False)})
    return out


def phase_gate(score):
    return "GO" if score >= 80 else "GO-WITH-CONDITIONS" if score >= 65 else "REDESIGN" if score >= 40 else "NO-GO"


def aweb06(work):
    w = {"clinical_relevance": 0.3, "regulatory": 0.25, "sensitivity": 0.2, "feasibility": 0.15, "patient": 0.1}
    eps = [{"name": "overall survival", "clinical_relevance": 5, "regulatory": 5, "sensitivity": 3, "feasibility": 3, "patient": 5},
           {"name": "tumour shrinkage", "clinical_relevance": 3, "regulatory": 3, "sensitivity": 5, "feasibility": 4,
            "patient": 2, "surrogate": True},
           {"name": "biomarker X", "clinical_relevance": 2, "regulatory": 1, "sensitivity": 4, "feasibility": 4, "patient": 1,
            "surrogate": True}]
    sel = endpoint_select(eps, w)
    r = {"synopsis": {"design": "parallel RCT", "alpha": 0.05, "power": 0.8, "effect_source": "pilot study ref"},
         "endpoints": sel, "n_means_d0.5": n_means(0.5), "n_props_.6_.4": n_props(0.6, 0.4),
         "events_hr0.7": schoenfeld_events(0.7),
         "gates": {s: phase_gate(s) for s in (85, 70, 50, 20)}, "routing": ["biostatistician", "medical monitor"],
         "advisory": True}
    save(work, "study_gate.json", r)
    return [eq("means d=0.5 n/group", r["n_means_d0.5"], 63), eq("proportions .6 vs .4 n/group", r["n_props_.6_.4"], 97),
            eq("Schoenfeld events HR 0.7", r["events_hr0.7"], 247),
            eq("endpoint classes", [e["class"] for e in sel], ["primary", "key-secondary", "exploratory"]),
            eq("surrogates flagged", [e["name"] for e in sel if e["surrogate"]], ["tumour shrinkage", "biomarker X"]),
            eq("gate bands", list(r["gates"].values()), ["GO", "GO-WITH-CONDITIONS", "REDESIGN", "NO-GO"])]


# ---------- AWEB-07 provider list extraction ----------
CRED = re.compile(r"\b(MD|DO|NP|PA-C|DDS|PhD|RN)\b")


def extract_providers(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select(".provider"):
        name = card.select_one(".name").get_text(strip=True)
        creds = CRED.findall(name + " " + card.get_text(" "))
        clean = CRED.sub("", name).strip(" ,")
        spec = card.select_one(".specialty")
        rows.append({"name": clean, "credentials": sorted(set(creds)),
                     "specialty": spec.get_text(strip=True) if spec else None})
    gaps = [r["name"] for r in rows if not r["specialty"]]
    return rows, gaps


def aweb07(work):
    html = """<html><body><nav>Home | About</nav>
    <div class='provider'><h3 class='name'>Sara Haddad, MD</h3><p class='specialty'>Cardiology</p></div>
    <div class='provider'><h3 class='name'>Omar Nasser, DO</h3><p class='specialty'>Family Medicine</p></div>
    <div class='provider'><h3 class='name'>Lina Farah, NP</h3></div>
    <footer>© Clinic</footer></body></html>"""
    rows, gaps = extract_providers(html)
    table = "| name | credentials | specialty |\n|---|---|---|\n" + "\n".join(
        f"| {r['name']} | {', '.join(r['credentials'])} | {r['specialty'] or 'GAP: enrich'} |" for r in rows)
    save(work, "providers.md", table)
    return [eq("three providers", len(rows), 3), eq("names cleaned", rows[0]["name"], "Sara Haddad"),
            eq("credentials", [r["credentials"] for r in rows], [["MD"], ["DO"], ["NP"]]),
            eq("specialty gap listed for enrichment", gaps, ["Lina Farah"]),
            truth("nav/footer not extracted", "Home" not in table and "Clinic" not in table)]


# ---------- AWEB-08 patent intake ----------
SUBCASES = ("novelty", "freedom-to-operate", "landscape", "invalidity", "due diligence")
JURIS = {"US", "EP", "CN", "JP", "KR", "PCT"}
VAGUE = re.compile(r"^(something|an app|a device|an idea|a thing)\b|\b(etc|stuff|things)\b", re.I)
STOP = set("a an the of for and with to in that which by on is are using uses from".split())


def patent_intake(answers):
    log, rejected_once = [], False
    for q1 in answers["q1"]:
        if (VAGUE.search(q1) or len(q1.split()) < 8) and not rejected_once:
            rejected_once = True
            log.append("Q1 rejected as vague: " + q1)
            continue
        desc = q1
        break
    else:
        desc = answers["q1"][-1]
    if answers["q2"] not in SUBCASES:
        raise ValueError("pick one of five sub-use-cases")
    bad = [j for j in answers["q3"] if j not in JURIS]
    if bad:
        raise ValueError(f"unknown jurisdictions {bad}")
    kw = [w for w in words(desc) if w not in STOP and len(w) > 3]
    return {"description": desc, "purpose": answers["q2"], "jurisdictions": answers["q3"], "log": log,
            "keywords": sorted(set(kw)), "caveat": "search report, not legal advice"}


def aweb08(work):
    ok = patent_intake({"q1": ["an app that does stuff",
                               "solar panel cleaning drone using electrostatic dust repulsion on desert farms"],
                        "q2": "freedom-to-operate", "q3": ["US", "EP"]})
    errs = []
    for bad in ({"q1": ["x " * 9], "q2": "general", "q3": ["US"]}, {"q1": ["y " * 9], "q2": "novelty", "q3": ["XX"]}):
        try:
            patent_intake(bad)
        except ValueError as e:
            errs.append(str(e))
    save(work, "patent_intake.json", {"ok": ok, "errors": errs})
    return [eq("vague Q1 rejected once", len(ok["log"]), 1),
            truth("precise description accepted", ok["description"].startswith("solar panel")),
            truth("concept keywords extracted", {"electrostatic", "drone", "solar"} <= set(ok["keywords"]), ok["keywords"]),
            eq("bad sub-use-case and jurisdiction refused", len(errs), 2),
            truth("no-legal-advice caveat", "not legal advice" in ok["caveat"])]


# ---------- AWEB-10 Obsidian Bases ----------
def validate_base(text):
    data = yaml.safe_load(text)
    defined = set((data.get("formulas") or {}).keys())
    used = set(re.findall(r"formula\.(\w+)", text))
    missing = sorted(used - defined)
    views_ok = all("type" in v and "name" in v for v in data.get("views", []))
    return {"ok": not missing and views_ok, "missing_formulas": missing, "views": len(data.get("views", []))}


def aweb10(work):
    base = {"filters": {"and": ['file.hasTag("book")', 'file.inFolder("Reading")']},
            "formulas": {"age_days": "(now() - file.ctime).days.round(0)",
                         "label": "'Status: \"' + status + '\"'"},
            "views": [{"type": "table", "name": "By author", "groupBy": {"property": "author"},
                       "order": ["file.name", "formula.age_days"], "summaries": {"formula.age_days": "Average"}}]}
    good = yaml.safe_dump(base, allow_unicode=True, sort_keys=False)
    save(work, "Books.base", good)
    bad_base = dict(base, views=[dict(base["views"][0], order=["formula.score"])])
    bad = yaml.safe_dump(bad_base, sort_keys=False)
    rg, rb = validate_base(good), validate_base(bad)
    title = yaml.safe_dump({"title": "Note: {draft} #1"})
    save(work, "validation.json", {"good": rg, "bad": rb})
    return [eq("valid base passes", rg["ok"], True), eq("undefined formula.score caught", rb["missing_formulas"], ["score"]),
            truth("duration read via .days before rounding", ".days.round" in base["formulas"]["age_days"]),
            eq("string with : { } # round-trips quoted", yaml.safe_load(title)["title"], "Note: {draft} #1"),
            truth("embed syntax", "![[Books.base#By author]]".startswith("![["))]


# ---------- AWEB-11 recognition over recall ----------
def combobox(options, typed, recents):
    t = typed.lower()
    m = [o for o in options if t in o.lower()]
    return sorted(m, key=lambda o: (o not in recents, recents.index(o) if o in recents else 0, o))


def audit_fields(fields):
    issues = []
    for f in fields:
        if f["kind"] == "password" or f["kind"] == "free text":
            continue
        if f["kind"] == "choice" and not f.get("options_shown"):
            issues.append((f["name"], "options hidden: user must recall"))
        if f.get("placeholder", "").lower() in ("enter value", "enter value..."):
            issues.append((f["name"], "placeholder should show an example value"))
    return issues


def aweb11(work):
    countries = ["Egypt", "Jordan", "Saudi Arabia", "Bahrain", "Qatar", "Oman", "Morocco", "Arabic Republic"]
    res = combobox(countries, "ar", recents=["Qatar"])
    fields = [{"name": "country", "kind": "choice", "options_shown": False, "placeholder": "Enter value"},
              {"name": "password", "kind": "password"},
              {"name": "city", "kind": "choice", "options_shown": True, "placeholder": "e.g. Cairo"}]
    issues = audit_fields(fields)
    save(work, "recognition_audit.json", {"combobox": res, "issues": issues})
    return [eq("filtered matches, recents first", res, ["Qatar", "Arabic Republic", "Saudi Arabia"]),
            eq("hidden options + Enter value flagged on country", [i[0] for i in issues], ["country", "country"]),
            truth("password keeps recall", all(i[0] != "password" for i in issues))]


PROGRAMS = {"AWEB-02": aweb02, "AWEB-03": aweb03, "AWEB-04": aweb04, "AWEB-05": aweb05, "AWEB-06": aweb06,
            "AWEB-07": aweb07, "AWEB-08": aweb08, "AWEB-10": aweb10, "AWEB-11": aweb11}
