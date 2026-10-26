#!/usr/bin/env python3
"""GitHub 30-day pulse / نبض GitHub في آخر 30 يومًا: the 1,000 most important repositories active in a 30-day window.

The all-time list (github_top_repos.py) answers "what is famous"; this one answers "what is moving now". It reads the
committed facts snapshot data/github_pulse_snapshot.json (1,000 repositories with their 30-day activity, total stars,
licence, description and domain) and the hand review data/github_pulse_review.json (domain fixes and the ideas the
skill took from them), and writes the tracker data/github_pulse.json plus the readable report
references/github-pulse-30d.md.

    python3 scripts/github_pulse.py build [--check]          # tracker + report from the snapshot and the review
    python3 scripts/github_pulse.py stats [--json]           # counts by domain, licence class and decision
    python3 scripts/github_pulse.py top [--domain motion-animation] [-n 20]
    python3 scripts/github_pulse.py find <words>             # name, description or domain match
    python3 scripts/github_pulse.py show <owner/repo>
    python3 scripts/github_pulse.py ideas [--domain design-ui] [--status transferred]   # what the skill took and where it lives
    python3 scripts/github_pulse.py --self-test

Refreshing (network, each step writes only into --work, never over the committed snapshot):

    python3 scripts/github_pulse.py collect --work /tmp/pulse --end 2026-10-26 --days 30   # GH Archive hourly dumps
    python3 scripts/github_pulse.py enrich  --work /tmp/pulse                             # deps.dev stars/licence + README head
    python3 scripts/github_pulse.py select  --work /tmp/pulse --out /tmp/pulse/snapshot.json

Method: activity comes from GH Archive (https://www.gharchive.org/), the public hourly archive of GitHub events. For
every repository we count, inside the window, stars (WatchEvent), forks, pull requests, issues, comments, releases,
pushes and the number of distinct people who did any of those. Total stars and the SPDX licence come from deps.dev;
descriptions come from deps.dev or the first paragraph of the README (raw.githubusercontent.com). Importance =
distinct people active in the window + 25 * log10(1 + total stars), so a new repository many people touched this
month and an established one that is still moving both rank. A repository counts as updated when it received a push
or a release inside the window. Creative domains (motion, generative media, design, video/audio, 3D, apps) get a
minimum share so the list is not only developer infrastructure. Repositories that ship cheats, cracks, stealth
bot-detection bypasses or similar are kept out (domain "unsafe") and never mined.

Decisions: transferred = an idea from it now lives in a skill tool or protocol appendix (ids listed); mine = relevant
and permissive, eligible for the next batch; reference = relevant but copyleft, unrecognised or no licence (link and
own-words method only); watch = general software, tracked for context; excluded = unsafe. Python 3.8+ stdlib only;
the network steps call curl.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import gzip
import json
import math
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
SNAPSHOT = SK / "data" / "github_pulse_snapshot.json"
REVIEW = SK / "data" / "github_pulse_review.json"
TRACKER = SK / "data" / "github_pulse.json"
REPORT = SK / "references" / "github-pulse-30d.md"

# Domain rules. The first rule ("unsafe") wins outright; the others score: 3 points per hit in name+description,
# half a point per hit (max 6) in the README head; the best score wins, earlier rules break ties.
DOMAINS = [
    ("unsafe", "مستبعد للأمان", False,
     r"\bcrack(ed|s)?\b|\bcheats?\b(?! ?sheet)|aimbot|spoofer|\bexecutor\b|keygen|robux|injector|\bstealer\b"
     r"|free (v-?bucks|nitro)|account generator|premium (free|unlocked)|activator\b|\bhwid\b"
     r"|bypass (cloudflare|captcha|bot detection|anti-?bot)|stealth (headless )?browser"),
    ("agents-skills", "الوكلاء والمهارات", True,
     r"\bagents?\b|agentic|claude code|\bskills?\b|\bmcp\b|\bcodex\b|harness|copilot|coding assistant|\bcursor\b"
     r"|subagent|multi-agent|vibe cod|computer use|browser use|opencode|openclaw"),
    ("generative-media", "التوليد بالذكاء: صور وفيديو وصوت", True,
     r"text-to-(image|video|speech|music|audio)|image generat|video generat|diffusion|comfyui|\btts\b"
     r"|voice (clon|chang|design)|speech synth|lip ?sync|talking head|upscal|flux\.?1|flux (model|dev|schnell|kontext)"
     r"|wan ?2|hunyuan|\bsora\b|\bveo\b|generative (art|video|image)|ai (video|image|art)\b|\bavatar"),
    ("motion-animation", "الموشن والأنيميشن", True,
     r"animat|(?<!from-)\bmotion (graphic|design|video)|manim|lottie|\bgsap\b|keyframe|remotion|\brive\b|\btween"
     r"|hyperframes|kinetic typo|motion graphics|motion design|visual effects|\bvfx\b"),
    ("video-audio", "الفيديو والصوت والمونتاج", True,
     r"\bvideos?\b|\baudio\b|ffmpeg|\bmusic\b|podcast|subtitle|caption|whisper|transcri|non-linear|\bnle\b|\bdaw\b"
     r"|youtube|\bobs\b|screen record|speech-to-text|\bclips?\b"),
    ("design-ui", "التصميم والواجهات والخطوط", True,
     r"\bdesign(er)?s?\b|\bui\b|\bux\b|figma|\bicons?\b|\bfonts?\b|typeface|typograph|tailwind|component librar"
     r"|shadcn|design system|\bcss\b|\bsvg\b|illustrat|vector art|color palette|slides|presentation|diagram|whiteboard"),
    ("3d-graphics-games", "3D والرسوميات والألعاب", True,
     r"\b3d\b|webgl|webgpu|three\.?js|\bgames?\b|shader|blender|godot|unity|unreal|gaussian splat|nerf|\bmesh"
     r"|ray ?trac|voxel|game engine|emulat|\bcad\b"),
    ("apps-mobile-desktop", "التطبيقات (موبايل وسطح مكتب)", True,
     r"\bandroid\b|\bios\b|iphone|mobile app|react native|flutter|\bswift(ui)?\b|kotlin|desktop app|electron|tauri"
     r"|macos app|windows app|menu ?bar|launcher|alternative to|self-hosted"),
    ("llm-models-inference", "النماذج اللغوية والاستدلال والذاكرة", True,
     r"\bllms?\b|language model|\bgpt|inference|\brag\b|retrieval|memory|reasoning|fine-?tun|\blora\b|quantiz|vllm"
     r"|llama|qwen|deepseek|gemma|mistral|embedding|vector (db|database|search)|transformer|tokeni[sz]|benchmark"
     r"|\bmoe\b|\btokens?\b"),
    ("data-viz-ml", "البيانات وتعلم الآلة والرسوم البيانية", True,
     r"\bchart|visuali[sz]|dashboard|\bplot|\bdata\b|dataset|pandas|machine learning|deep learning|pytorch"
     r"|computer vision|\bocr\b|segment|detect|\bml\b|analytics|spreadsheet|\bsql\b"),
    ("web-dev", "تطوير الويب", False,
     r"\breact\b|\bnext\.?js|\bvue\b|svelte|frontend|backend|\bapi\b|framework|typescript|javascript|node\.?js"
     r"|\bbun\b|deno|web ?app|website|browser|http|server|scrap"),
    ("devtools-infra", "أدوات المطورين والبنية التحتية", False,
     r"\bcli\b|terminal|editor|\bide\b|compiler|\bgit\b|docker|kubernetes|\bk8s\b|devops|database|linux|kernel"
     r"|\bshell\b|rust|golang|package manager|build tool|observability|cloud|sandbox|container|\blsp\b|neovim|vscode"),
    ("security", "الأمن", False,
     r"security|vulnerab|pentest|penetration|malware|exploit|\bctf\b|reverse engineer|ghidra|forensic|osint|cve-"
     r"|firewall|encrypt|red ?team"),
    ("knowledge-learning", "المعرفة والتعلم والإنتاجية", True,
     r"awesome|curated|tutorial|course|learn|roadmap|interview|\bbooks?\b|notes|knowledge|obsidian|wiki"
     r"|productivity|guide|from scratch|cheat ?sheet|prompts?\b"),
]
_CRE = [(d, ar, rel, re.compile(rx, re.I)) for d, ar, rel, rx in DOMAINS]
DOMAIN_AR = {d: ar for d, ar, _, _ in DOMAINS}
DOMAIN_AR["other"] = "أخرى"
RELEVANT = {d for d, _, rel, _ in DOMAINS if rel}
HEAD_ONLY = {"motion-animation", "generative-media"}  # README words alone are too noisy for these
CREATIVE_MIN = {"motion-animation": 40, "generative-media": 40, "design-ui": 80, "video-audio": 60,
                "3d-graphics-games": 60, "apps-mobile-desktop": 60, "knowledge-learning": 40, "security": 25,
                "llm-models-inference": 60, "data-viz-ml": 50}
STAT_KEYS = ("stars", "forks", "prs", "issues", "comments", "releases", "pushes")
SECRET_RE = re.compile(r"(gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})")


# ---------------------------------------------------------------- classification

def clean_md(md: str) -> str:
    md = re.sub(r"<[^>]+>", " ", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"[#>*`|_\-=]{2,}", " ", md)
    return re.sub(r"\s+", " ", md).strip()


def readme_desc(md: str) -> str:
    """First real paragraph of a README (skips badges, links-only lines and headings)."""
    for para in re.split(r"\n\s*\n", md or ""):
        t = clean_md(para)
        if len(t) > 40 and not t.lower().startswith(("http", "license", "build", "[")):
            return t[:240]
    return ""


def domain_of(repo: str, desc: str, body: str = "") -> str:
    head = f"{repo.replace('-', ' ').replace('_', ' ')} {desc}"
    if _CRE[0][3].search(head):
        return "unsafe"
    best, dom = 0.0, "other"
    for i, (d, _, _, rx) in enumerate(_CRE[1:]):
        hits = len(rx.findall(head))
        if d in HEAD_ONLY and not hits:
            continue
        score = 3 * hits + 0.5 * min(len(rx.findall(body or "")), 6) - i * 0.01
        if score > best:
            best, dom = score, d
    return dom


def licence_class(spdx: str, text: str = "") -> tuple:
    """(class, spdx-ish id). Class: permissive | copyleft | unrecognised | none."""
    s = (spdx or "").upper()
    if not s and text:
        t = text[:1500].lower()
        s = ("MIT" if "permission is hereby granted, free of charge" in t else
             "AGPL" if "affero" in t else
             "GPL" if "gnu general public" in t or "gnu lesser" in t else
             "APACHE-2.0" if "apache license" in t else
             "BSD" if "redistribution and use in source" in t else
             "MPL" if "mozilla public" in t else
             "CC" if "creative commons" in t else "OTHER")
    if not s:
        return "none", ""
    if any(k in s for k in ("AGPL", "GPL", "LGPL", "MPL", "EUPL", "CC-BY-SA", "SSPL", "OSL")):
        return "copyleft", s
    if any(k in s for k in ("MIT", "APACHE", "BSD", "ISC", "UNLICENSE", "0BSD", "ZLIB", "CC0", "PYTHON", "BOOST")):
        return "permissive", s
    return "unrecognised", s


def importance(actors: int, stars_total) -> float:
    return round(actors + 25 * math.log10(1 + (stars_total or 0)), 2)


def select(pool: list, limit: int = 1000, minimums: dict = None) -> list:
    """Top `limit` by importance with a minimum share per domain; unsafe rows never selected."""
    minimums = CREATIVE_MIN if minimums is None else minimums
    ranked = sorted((r for r in pool if r.get("domain") != "unsafe"), key=lambda r: (-r["score"], r["repo"].lower()))
    chosen, seen = [], set()
    for dom, n in minimums.items():
        for r in [x for x in ranked if x.get("domain") == dom][:n]:
            if r["repo"] not in seen:
                chosen.append(r)
                seen.add(r["repo"])
    for r in ranked:
        if len(chosen) >= limit:
            break
        if r["repo"] not in seen:
            chosen.append(r)
            seen.add(r["repo"])
    chosen = sorted(chosen, key=lambda r: (-r["score"], r["repo"].lower()))[:limit]
    for i, r in enumerate(chosen, 1):
        r["rank"] = i
    return chosen


# ---------------------------------------------------------------- tracker

def load_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def decide(row: dict, review: dict) -> dict:
    over = review.get("overrides", {}).get(row["repo"].lower(), {})
    dom = over.get("domain", row.get("domain", "other"))
    transferred = sorted({i["id"] for i in review.get("ideas", []) if row["repo"].lower() in
                          [s.lower() for s in i.get("sources", [])] and i.get("status") == "transferred"})
    referenced = sorted({i["id"] for i in review.get("ideas", []) if row["repo"].lower() in
                         [s.lower() for s in i.get("sources", [])]})
    lic = row.get("licence_class", "none")
    if dom == "unsafe":
        decision, why = "excluded", over.get("reason", "unsafe: cheats, cracks or bot-detection bypass")
    elif transferred:
        decision, why = "transferred", "idea restated in our own words: " + ", ".join(transferred)
    elif dom in RELEVANT and lic == "permissive":
        decision, why = "mine", "relevant and permissive"
    elif dom in RELEVANT:
        decision, why = "reference", f"relevant, licence {lic}: link and own-words method only"
    else:
        decision, why = "watch", "general software, tracked for context"
    if over.get("decision"):
        decision, why = over["decision"], over.get("reason", why)
    out = dict(row)
    out.update(domain=dom, domain_ar=DOMAIN_AR.get(dom, dom), decision=decision, why=why, ideas=referenced)
    return out


def build_tracker(snapshot: dict, review: dict) -> dict:
    rows = [decide(r, review) for r in snapshot.get("repos", [])]
    ideas = []
    for i in review.get("ideas", []):
        ideas.append(dict(i, sources_in_list=[s for s in i.get("sources", [])
                                              if s.lower() in {r["repo"].lower() for r in rows}]))
    return {"schema": "kosif.github_pulse.v1", "window": snapshot.get("window", {}), "method": snapshot.get("method", {}),
            "counts": counts(rows), "ideas": ideas, "repos": rows}


def counts(rows: list) -> dict:
    def tally(key):
        c = {}
        for r in rows:
            c[r.get(key, "")] = c.get(r.get(key, ""), 0) + 1
        return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))
    return {"repos": len(rows), "domain": tally("domain"), "licence_class": tally("licence_class"),
            "decision": tally("decision")}


def md_cell(s) -> str:
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def fmt_int(n) -> str:
    return "—" if n is None else f"{int(n):,}"


def render_report(tr: dict) -> str:
    w, c = tr["window"], tr["counts"]
    rows = tr["repos"]
    L = ["# نبض GitHub في آخر 30 يومًا — GitHub 30-day pulse", "",
         "Generated by `scripts/github_pulse.py build` from `data/github_pulse_snapshot.json` and "
         "`data/github_pulse_review.json`; do not edit by hand.", "",
         f"النافذة / window: **{w.get('start', '?')} → {w.get('end', '?')}** ({w.get('hours', '?')} hourly GH Archive "
         f"files, {fmt_int(w.get('repos_seen'))} repositories with activity, {fmt_int(w.get('candidates'))} candidates "
         f"enriched). القائمة: **{c['repos']}** مستودعًا نشطًا (دُفع إليها أو صدر لها إصدار داخل النافذة).", "",
         "**القرار / decision:** " + " · ".join(f"`{k}` {v}" for k, v in c["decision"].items()), "",
         "**الترخيص / licence class:** " + " · ".join(f"`{k}` {v}" for k, v in c["licence_class"].items()), "",
         "Importance = distinct people active in the window + 25 × log10(1 + total stars). Creative domains get a "
         "minimum share. `transferred` = an idea now lives in a skill tool or appendix (see the ideas table); `mine` = "
         "relevant and permissive; `reference` = relevant but copyleft/unrecognised/no licence; `watch` = general "
         "software; `excluded` = unsafe, never mined.", "",
         "Limits: " + md_cell(tr["method"].get("limits", "")), "",
         "## الفهرس / contents", "",
         "1. [الأفكار المنقولة / ideas taken into the skill](#الأفكار-المنقولة--ideas-taken-into-the-skill)",
         "2. [حسب المجال / by domain](#حسب-المجال--by-domain)",
         "3. [الأبرز في كل مجال / leaders per domain](#الأبرز-في-كل-مجال--leaders-per-domain)",
         "4. [الجدول الكامل / full table](#الجدول-الكامل--full-table)", "",
         "## الأفكار المنقولة / ideas taken into the skill", "",
         "| id | idea | الفكرة | status | lives in | sources |", "|---|---|---|---|---|---|"]
    for i in tr["ideas"]:
        L.append(f"| `{i['id']}` | {md_cell(i['title_en'])} | {md_cell(i['title_ar'])} | {i['status']} | "
                 f"{md_cell(', '.join(i.get('lives_in', [])))} | {md_cell(', '.join(i.get('sources', [])[:4]))} |")
    L += ["", "## حسب المجال / by domain", "",
          "| domain | المجال | repos | transferred | mine | reference | watch |", "|---|---|---:|---:|---:|---:|---:|"]
    for dom, n in c["domain"].items():
        sub = [r for r in rows if r["domain"] == dom]
        k = lambda d: sum(1 for r in sub if r["decision"] == d)  # noqa: E731
        L.append(f"| `{dom}` | {DOMAIN_AR.get(dom, dom)} | {n} | {k('transferred')} | {k('mine')} | {k('reference')} | {k('watch')} |")
    L += ["", "## الأبرز في كل مجال / leaders per domain", ""]
    for dom in c["domain"]:
        sub = [r for r in rows if r["domain"] == dom][:8]
        L.append(f"- **{DOMAIN_AR.get(dom, dom)}** (`{dom}`): " + ", ".join(
            f"[{r['repo']}](https://github.com/{r['repo']}) ({r['actors']})" for r in sub))
    L += ["", "## الجدول الكامل / full table", "",
          "| # | repo | active people | ★ 30d | ★ total | PRs | releases | last push | licence | domain | decision | description |",
          "|---:|---|---:|---:|---:|---:|---:|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['rank']} | [{r['repo']}](https://github.com/{r['repo']}) | {r['actors']} | {r.get('stars', 0)} | "
                 f"{fmt_int(r.get('stars_total'))} | {r.get('prs', 0)} | {r.get('releases', 0)} | "
                 f"{(r.get('last_push') or '—')[:10]} | {md_cell(r.get('licence') or r.get('licence_class'))} | "
                 f"`{r['domain']}` | {r['decision']} | {md_cell(r.get('desc', ''))[:140]} |")
    return "\n".join(L) + "\n"


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def cmd_build(check: bool) -> int:
    snap = load_json(SNAPSHOT, None)
    if snap is None:
        print(f"missing {SNAPSHOT}", file=sys.stderr)
        return 1
    tr = build_tracker(snap, load_json(REVIEW, {}))
    outs = {TRACKER: dump(tr), REPORT: render_report(tr)}
    stale = [p for p, txt in outs.items() if not p.is_file() or p.read_text(encoding="utf-8") != txt]
    if check:
        for p in stale:
            print(f"stale: {p.relative_to(SK)}")
        print("ok" if not stale else f"{len(stale)} stale file(s); run: python3 scripts/github_pulse.py build")
        return 1 if stale else 0
    for p, txt in outs.items():
        p.write_text(txt, encoding="utf-8")
    print(f"wrote {TRACKER.relative_to(SK)} and {REPORT.relative_to(SK)}: {tr['counts']['repos']} repos, "
          f"{len(tr['ideas'])} ideas")
    return 0


def tracker() -> dict:
    tr = load_json(TRACKER, None)
    if tr is None:
        tr = build_tracker(load_json(SNAPSHOT, {"repos": []}), load_json(REVIEW, {}))
    return tr


def cmd_stats(as_json: bool) -> int:
    tr = tracker()
    if as_json:
        print(json.dumps({"window": tr["window"], "counts": tr["counts"], "ideas": len(tr["ideas"])}, ensure_ascii=False, indent=1))
        return 0
    c = tr["counts"]
    print(f"window {tr['window'].get('start')} → {tr['window'].get('end')}: {c['repos']} repos, {len(tr['ideas'])} ideas")
    for key in ("domain", "decision", "licence_class"):
        print(f"\n{key}:")
        for k, v in c[key].items():
            print(f"  {v:5d}  {k}  {DOMAIN_AR.get(k, '') if key == 'domain' else ''}")
    return 0


def line(r: dict) -> str:
    return (f"#{r['rank']:<4} {r['repo']:<44} people={r['actors']:<5} ★total={fmt_int(r.get('stars_total')):<9} "
            f"{r['domain']:<20} {r['decision']:<11} {r.get('desc', '')[:80]}")


def cmd_top(domain: str, n: int) -> int:
    rows = [r for r in tracker()["repos"] if not domain or r["domain"] == domain]
    if not rows:
        print(f"no repos for domain {domain!r}; domains: {', '.join(DOMAIN_AR)}", file=sys.stderr)
        return 1
    for r in rows[:n]:
        print(line(r))
    return 0


def cmd_find(words: list, limit: int) -> int:
    ws = [w.lower() for w in words]
    hits = [r for r in tracker()["repos"]
            if all(w in f"{r['repo']} {r.get('desc', '')} {r['domain']} {r['domain_ar']}".lower() for w in ws)]
    for r in hits[:limit]:
        print(line(r))
    print(f"{len(hits)} match(es)")
    return 0 if hits else 1


def cmd_show(repo: str) -> int:
    tr = tracker()
    for r in tr["repos"]:
        if r["repo"].lower() == repo.lower():
            print(json.dumps(r, ensure_ascii=False, indent=1))
            for i in tr["ideas"]:
                if r["repo"].lower() in [s.lower() for s in i.get("sources", [])]:
                    print(f"idea {i['id']}: {i['title_en']} → {', '.join(i.get('lives_in', []))} ({i['status']})")
            return 0
    print(f"{repo} is not in the 30-day list", file=sys.stderr)
    return 1


def cmd_ideas(domain: str, status: str, as_json: bool) -> int:
    ideas = [i for i in tracker()["ideas"] if (not domain or i.get("domain") == domain) and (not status or i["status"] == status)]
    if as_json:
        print(json.dumps(ideas, ensure_ascii=False, indent=1))
        return 0
    for i in ideas:
        print(f"{i['id']}  [{i['status']}]  {i['title_en']} / {i['title_ar']}")
        print(f"      how: {i['mechanism']}")
        print(f"      lives in: {', '.join(i.get('lives_in', [])) or '—'}   sources: {', '.join(i.get('sources', []))}")
    print(f"{len(ideas)} idea(s)")
    return 0


# ---------------------------------------------------------------- network refresh (writes only into --work)

KEEP = {"WatchEvent": "stars", "ForkEvent": "forks", "PushEvent": "pushes", "PullRequestEvent": "prs",
        "ReleaseEvent": "releases", "IssuesEvent": "issues", "IssueCommentEvent": "comments"}


def curl(url: str, max_bytes: int = 0, timeout: int = 180) -> bytes:
    cmd = ["curl", "-sSf", "--max-time", str(timeout)]
    if max_bytes:
        cmd += ["-r", f"0-{max_bytes}"]
    return subprocess.run(cmd + [url], capture_output=True, check=True).stdout


def aggregate_hour(lines) -> dict:
    """GH Archive JSON lines → {repo: {counts..., actors: [...], last_push}}; push-only repos are dropped."""
    agg, actors = {}, {}
    for raw in lines:
        try:
            e = json.loads(raw)
        except ValueError:
            continue
        k = KEEP.get(e.get("type"))
        name = (e.get("repo") or {}).get("name") or ""
        if not k or "/" not in name:
            continue
        a = agg.setdefault(name, {})
        a[k] = a.get(k, 0) + 1
        if k == "pushes":
            a["last_push"] = max(a.get("last_push", ""), e.get("created_at", ""))
        else:
            actors.setdefault(name, set()).add((e.get("actor") or {}).get("login", "?"))
    for n, s in actors.items():
        agg[n]["actors"] = sorted(s)
    return {n: a for n, a in agg.items() if set(a) - {"pushes", "last_push"}}


def _hour(job):
    ts, parts = job
    p = Path(parts) / f"{ts}.json"
    if p.is_file():
        return ts, "cached"
    try:
        data = gzip.decompress(curl(f"https://data.gharchive.org/{ts}.json.gz"))
    except Exception as e:  # noqa: BLE001 - report and continue
        return ts, f"fail {str(e)[:120]}"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(aggregate_hour(data.splitlines())), encoding="utf-8")
    os.replace(tmp, p)
    return ts, "ok"


def cmd_collect(work: Path, end: str, days: int, jobs: int) -> int:
    parts = work / "parts"
    parts.mkdir(parents=True, exist_ok=True)
    stop = dt.datetime.strptime(end, "%Y-%m-%d")
    t, hours = stop - dt.timedelta(days=days), []
    while t < stop:
        hours.append((f"{t:%Y-%m-%d}-{t.hour}", str(parts)))
        t += dt.timedelta(hours=1)
    bad = 0
    with cf.ProcessPoolExecutor(jobs) as ex:
        for ts, st in ex.map(_hour, hours):
            if st.startswith("fail"):
                bad += 1
                print(ts, st, flush=True)
    tot, act, last = {}, {}, {}
    for p in sorted(parts.glob("*.json")):
        for n, a in json.loads(p.read_text(encoding="utf-8")).items():
            row = tot.setdefault(n, {k: 0 for k in STAT_KEYS})
            for k, v in a.items():
                if k == "actors":
                    act.setdefault(n, set()).update(v)
                elif k == "last_push":
                    last[n] = max(last.get(n, ""), v)
                elif k in row:
                    row[k] += v
    rows = [dict(repo=n, **c, actors=len(act.get(n, ())), last_push=last.get(n)) for n, c in tot.items()]
    rows.sort(key=lambda r: (-r["actors"], r["repo"]))
    meta = {"start": hours[0][0] if hours else None, "end": end, "hours": len(hours), "failed_hours": bad,
            "repos_seen": len(rows)}
    (work / "activity.json").write_text(json.dumps({"window": meta, "rows": rows[:30000]}), encoding="utf-8")
    print(f"{len(rows)} repos with non-push activity; top 30000 kept in {work / 'activity.json'}; failed hours: {bad}")
    return 1 if bad else 0


def _deps(repo):
    url = "https://api.deps.dev/v3/projects/" + urllib.parse.quote("github.com/" + repo.lower(), safe="")
    try:
        return repo, json.loads(curl(url, timeout=30))
    except Exception:  # noqa: BLE001 - not indexed or network
        return repo, {}


def _readme(job):
    repo, folder, need_lic = job
    base = Path(folder) / repo.replace("/", "__")
    if base.with_suffix(".md").is_file():
        return
    txt = lic = ""
    for name in ("README.md", "readme.md", "README.MD", "README.rst", "README"):
        try:
            txt = curl(f"https://raw.githubusercontent.com/{repo}/HEAD/{name}", 12000, 25).decode("utf-8", "replace")
            break
        except Exception:  # noqa: BLE001
            continue
    if need_lic:
        for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
            try:
                lic = curl(f"https://raw.githubusercontent.com/{repo}/HEAD/{name}", 1500, 20).decode("utf-8", "replace")
                break
            except Exception:  # noqa: BLE001
                continue
    base.with_suffix(".lic").write_text(lic, encoding="utf-8")
    base.with_suffix(".md").write_text(txt, encoding="utf-8")


def cmd_enrich(work: Path, candidates: int, readmes: int, jobs: int) -> int:
    act = json.loads((work / "activity.json").read_text(encoding="utf-8"))
    rows = [r for r in act["rows"] if r["last_push"] or r.get("releases")][:candidates]
    cache_p = work / "deps.json"
    cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.is_file() else {}
    todo = [r["repo"] for r in rows if r["repo"] not in cache]
    with cf.ThreadPoolExecutor(jobs) as ex:
        for repo, d in ex.map(_deps, todo):
            cache[repo] = d
    cache_p.write_text(json.dumps(cache), encoding="utf-8")
    for r in rows:
        d = cache.get(r["repo"], {})
        r.update(stars_total=d.get("starsCount"), license=d.get("license") or None, desc=d.get("description") or "")
        r["score"] = importance(r["actors"], r["stars_total"])
    rows.sort(key=lambda r: (-r["score"], r["repo"]))
    folder = work / "readme"
    folder.mkdir(exist_ok=True)
    with cf.ThreadPoolExecutor(jobs) as ex:
        list(ex.map(_readme, [(r["repo"], str(folder), not r.get("license")) for r in rows[:readmes]]))
    (work / "candidates.json").write_text(json.dumps({"window": act["window"], "rows": rows[:readmes]}), encoding="utf-8")
    print(f"{len(rows)} candidates, {sum(1 for r in rows if r['stars_total'] is not None)} on deps.dev, "
          f"README heads for the top {min(readmes, len(rows))}")
    return 0


def cmd_select(work: Path, out: Path, limit: int) -> int:
    cand = json.loads((work / "candidates.json").read_text(encoding="utf-8"))
    pool = []
    for r in cand["rows"]:
        base = work / "readme" / r["repo"].replace("/", "__")
        md = base.with_suffix(".md").read_text(encoding="utf-8", errors="replace") if base.with_suffix(".md").is_file() else ""
        lic = base.with_suffix(".lic").read_text(encoding="utf-8", errors="replace") if base.with_suffix(".lic").is_file() else ""
        desc = (r.get("desc") or readme_desc(md))[:240]
        lc, spdx = licence_class(r.get("license"), lic)
        pool.append(dict({k: r.get(k, 0) for k in STAT_KEYS}, repo=r["repo"], actors=r["actors"],
                         last_push=r.get("last_push"), stars_total=r.get("stars_total"), licence=spdx or None,
                         licence_class=lc, desc=SECRET_RE.sub("[redacted]", desc),
                         domain=domain_of(r["repo"], desc, clean_md(md)[:2500]), score=r["score"]))
    chosen = select(pool, limit)
    unsafe = sum(1 for r in pool if r["domain"] == "unsafe")
    snap = {"schema": "kosif.github_pulse_snapshot.v1",
            "window": dict(cand["window"], candidates=len(pool), unsafe_excluded=unsafe),
            "method": {"activity": "GH Archive hourly dumps (WatchEvent, ForkEvent, PullRequestEvent, IssuesEvent, "
                                   "IssueCommentEvent, ReleaseEvent, PushEvent)",
                       "stars_and_licence": "https://api.deps.dev/v3/projects/github.com%2F<owner>%2F<repo>",
                       "description": "deps.dev description, else first README paragraph (raw.githubusercontent.com)",
                       "importance": "distinct active people in the window + 25*log10(1+total stars)",
                       "updated": "a push or a release inside the window",
                       "limits": "GH Archive has captured far fewer events since 2026 than before, so 30-day counts are "
                                 "a sample, good for ranking, not absolute numbers; repositories deps.dev has not indexed "
                                 "show no total stars; the domain is a keyword rule (fixes live in the review file)."},
            "repos": chosen}
    out.write_text(dump(snap), encoding="utf-8")
    print(f"wrote {out}: {len(chosen)} repos ({unsafe} unsafe kept out)")
    return 0


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    ok = True

    def expect(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            print("FAIL", msg)
    expect(domain_of("heygen-com/hyperframes", "Write HTML. Render video. Built for agents.") in
           ("agents-skills", "motion-animation", "video-audio"), "hyperframes domain")
    expect(domain_of("x/aimbot-pro", "best aimbot") == "unsafe", "unsafe aimbot")
    expect(domain_of("OWASP/CheatSheetSeries", "cheat sheet series on security") != "unsafe", "cheat sheet is not a cheat")
    expect(domain_of("jo/stealth", "Stealth headless browser to bypass Cloudflare") == "unsafe", "stealth bypass")
    expect(domain_of("remotion-dev/remotion", "Make videos programmatically with React") in ("motion-animation", "video-audio"), "remotion")
    expect(domain_of("colmap/colmap", "Structure-from-Motion and Multi-View Stereo") != "motion-animation", "SfM is not motion graphics")
    expect(domain_of("hyprwm/Hyprland", "dynamic tiling Wayland compositor", "smooth animations everywhere") != "motion-animation",
           "README-only motion words do not make a motion repo")
    expect(domain_of("narwhals-dev/narwhals", "compatibility layer between dataframe libraries") != "motion-animation",
           "'between' is not 'tween'")
    expect(licence_class("MIT")[0] == "permissive" and licence_class("GPL-3.0")[0] == "copyleft", "licence spdx")
    expect(licence_class("", "Permission is hereby granted, free of charge, to any person")[0] == "permissive", "licence text")
    expect(licence_class("", "")[0] == "none", "no licence")
    hour = [json.dumps({"type": "WatchEvent", "repo": {"name": "a/b"}, "actor": {"login": "u1"}}),
            json.dumps({"type": "PushEvent", "repo": {"name": "a/b"}, "actor": {"login": "u2"}, "created_at": "2026-10-01T00:00:00Z"}),
            json.dumps({"type": "PushEvent", "repo": {"name": "only/push"}, "actor": {"login": "u3"}}),
            json.dumps({"type": "WatchEvent", "repo": {}}), "not json"]
    agg = aggregate_hour(hour)
    expect(set(agg) == {"a/b"} and agg["a/b"]["stars"] == 1 and agg["a/b"]["actors"] == ["u1"], f"aggregate {agg}")
    pool = [dict(repo=f"o/r{i}", score=100 - i, domain="web-dev") for i in range(10)] + \
           [dict(repo="o/m", score=1, domain="motion-animation"), dict(repo="o/x", score=999, domain="unsafe")]
    sel = select(pool, 5, {"motion-animation": 1})
    expect(len(sel) == 5 and "o/m" in [r["repo"] for r in sel] and "o/x" not in [r["repo"] for r in sel], "quota select")
    expect([r["rank"] for r in sel] == [1, 2, 3, 4, 5], "ranks")
    snap = {"window": {}, "method": {}, "repos": [dict(repo="a/b", rank=1, actors=3, licence_class="permissive",
                                                         domain="design-ui", desc="d")]}
    review = {"ideas": [{"id": "GP-T", "title_en": "t", "title_ar": "ت", "status": "transferred", "sources": ["A/B"],
                         "mechanism": "m", "lives_in": ["x"]}]}
    tr = build_tracker(snap, review)
    expect(tr["repos"][0]["decision"] == "transferred" and tr["repos"][0]["ideas"] == ["GP-T"], "transferred decision")
    expect("GP-T" in render_report(tr), "report lists ideas")
    print("self-test ok" if ok else "self-test FAILED")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    s = sub.add_parser("stats")
    s.add_argument("--json", action="store_true")
    t = sub.add_parser("top")
    t.add_argument("--domain", default="")
    t.add_argument("-n", type=int, default=20)
    f = sub.add_parser("find")
    f.add_argument("words", nargs="+")
    f.add_argument("--limit", type=int, default=30)
    sh = sub.add_parser("show")
    sh.add_argument("repo")
    i = sub.add_parser("ideas")
    i.add_argument("--domain", default="")
    i.add_argument("--status", default="")
    i.add_argument("--json", action="store_true")
    c = sub.add_parser("collect")
    c.add_argument("--work", type=Path, required=True)
    c.add_argument("--end", default=dt.date.today().isoformat(), help="first day NOT included (YYYY-MM-DD)")
    c.add_argument("--days", type=int, default=30)
    c.add_argument("--jobs", type=int, default=4)
    e = sub.add_parser("enrich")
    e.add_argument("--work", type=Path, required=True)
    e.add_argument("--candidates", type=int, default=20000)
    e.add_argument("--readmes", type=int, default=3000)
    e.add_argument("--jobs", type=int, default=24)
    se = sub.add_parser("select")
    se.add_argument("--work", type=Path, required=True)
    se.add_argument("--out", type=Path, required=True)
    se.add_argument("--limit", type=int, default=1000)
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.cmd == "build":
        return cmd_build(a.check)
    if a.cmd == "stats":
        return cmd_stats(a.json)
    if a.cmd == "top":
        return cmd_top(a.domain, a.n)
    if a.cmd == "find":
        return cmd_find(a.words, a.limit)
    if a.cmd == "show":
        return cmd_show(a.repo)
    if a.cmd == "ideas":
        return cmd_ideas(a.domain, a.status, a.json)
    if a.cmd == "collect":
        return cmd_collect(a.work, a.end, a.days, a.jobs)
    if a.cmd == "enrich":
        return cmd_enrich(a.work, a.candidates, a.readmes, a.jobs)
    if a.cmd == "select":
        if a.out.resolve() == SNAPSHOT.resolve():
            print("refusing to overwrite the committed snapshot; write elsewhere and review the diff", file=sys.stderr)
            return 2
        return cmd_select(a.work, a.out, a.limit)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
