#!/usr/bin/env python3
"""Validate the kosif-superpowers skill / افحص سلامة المهارة.

Checks (errors fail the run, warnings do not unless --strict):
  frontmatter   name (≤64, lowercase-hyphen, no reserved words), description (≤1024, no angle
                brackets, third person), upload-safe keys, SKILL.md body < 500 lines, one SKILL.md
  records       every data/powers/*.json is a list; required keys; valid status; ID format and
                uniqueness; family = file stem; known domain; 👁 seen only for motion; ✅ has proof
  proofs        proof paths exist (relative to /home/user, i.e. the folder that holds the repo);
                style: owner-upload: session- http(s): and free-text receipts are skipped
  links         relative Markdown links in SKILL.md, references/ and proofs/ resolve
  toc           Markdown files over 100 lines have a contents heading (warning)
  chapters      generated chapters (scripts/build_chapters.py) are up to date
  counts        the counts marker in SKILL.md matches the catalog (see below)
  names         no model names or versions inside skill files (pre-existing motion data: warning)
  secrets       no API keys or tokens committed in skill files
  evals         evals/evals.json parses and has at least 3 well-formed cases

Counts marker — put this HTML comment anywhere in SKILL.md (it is invisible when rendered) and
keep the human-readable numbers next to it in sync; print a fresh one with --print-counts:

  <!-- counts: powers=4159 families=44 domains=8 proven=... ready=... install=... key=...
       seen=... documented=... idea=... styles=288 watched=253 -->

Any subset of keys is allowed; each key present must equal the live value from powers.py.

  python3 check_skill.py                # all checks
  python3 check_skill.py --strict       # warnings fail too
  python3 check_skill.py --json         # machine-readable report
  python3 check_skill.py --print-counts # the marker line for SKILL.md
  python3 check_skill.py --evals        # all checks, then routing evals (powers.py suggest per eval query)

Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import powers as P  # noqa: E402
import build_chapters as BC  # noqa: E402

SK = P.ROOT
REPO = SK.parents[2] if len(SK.parents) >= 3 else SK
BASE = REPO.parent  # proof paths are relative to this folder (/home/user)
IN_REPO = (REPO / ".claude" / "skills" / SK.name).resolve() == SK.resolve() and (REPO / "tools").is_dir()
SKIP_DIRS = {"dist", "__pycache__", "node_modules", ".git", "vendor"}  # Licensed third-party skills are separate packages, not nested KOSIF SKILL.md files.
UPLOAD_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
PACKAGE_ONLY_KEYS = {"claude_ai_description"}  # stripped by package_skill.py
BASE_KEYS = ("id", "family", "name_ar", "name_en", "status", "what", "how", "params", "install", "license",
             "proof", "styles", "tags")
GENERAL_KEYS = BASE_KEYS + ("domain", "when", "section", "source")
LIST_KEYS = ("proof", "styles", "tags")
ID_RE = re.compile(r"^[A-Z0-9]+-[A-Z]?\d{2,3}$")  # motion add-on series use one letter (GLOW-P01, CAM-X01)
TOC_RE = re.compile(r"^#{1,4}\s.*(الفهرس|المحتويات|contents|table of contents|\bTOC\b)", re.I | re.M)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
MODEL_RE = re.compile(r"claude-(?:opus|sonnet|haiku|fable)[\w.-]*|\b(?:Opus|Sonnet|Haiku)\s?[3-9](?:\.\d)?\b(?!\d|\s?k)"
                      r"|\bClaude (?:Opus|Sonnet|Haiku|Fable)\b|\bFable\b")  # the audio codec "Opus 96k" is not a model
SECRET_RE = re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}"
                       r"|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
COUNT_KEYS = ("powers", "families", "domains", "styles", "watched") + P.STATUSES
LEAK_RE = re.compile(r"/tmp/claude-\d+/|scratchpad/[^\s\"']*[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
                     r"|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/scratchpad|session_[0-9A-Za-z]{20,}")
TEXT_EXT = {".md", ".json", ".py", ".html", ".js", ".cjs", ".mjs", ".css", ".txt", ".sh", ".yml", ".yaml"}


class Report:
    def __init__(self):
        self.items = []  # (level, check, message)
        self.checks = Counter()

    def add(self, level, check, msg):
        self.items.append((level, check, msg))

    def err(self, check, msg):
        self.add("error", check, msg)

    def warn(self, check, msg):
        self.add("warn", check, msg)

    def info(self, check, msg):
        self.add("info", check, msg)

    def count(self, level):
        return sum(1 for i in self.items if i[0] == level)


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(SK))
    except ValueError:
        return str(p)


def skill_files(exts=None):
    for p in sorted(SK.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(SK).parts):
            continue
        if exts is None or p.suffix.lower() in exts:
            yield p


# ------------------------------------------------------------------ frontmatter

def parse_frontmatter(text: str):
    """Tiny YAML subset: key: value, quoted values, and > or | block scalars."""
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return None, text
    fm, lines, i = {}, m.group(1).splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", ln)
        if not km:
            i += 1
            continue
        key, val = km.group(1), km.group(2).strip()
        if val in (">", "|", ">-", "|-", ">+", "|+"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            fm[key] = (" " if val.startswith(">") else "\n").join(b for b in block if b).strip()
            continue
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        elif val and (re.search(r":\s|\s#", val) or val[0] in "[{&*!|>'\"%@`"):
            fm.setdefault("__unsafe__", []).append(key)
        fm[key] = val
        i += 1
    return fm, text[m.end():]


def check_frontmatter(r: Report):
    r.checks["frontmatter"] += 1
    sm = SK / "SKILL.md"
    if not sm.is_file():
        r.err("frontmatter", "SKILL.md is missing")
        return
    text = sm.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm is None:
        r.err("frontmatter", "SKILL.md has no YAML frontmatter between --- lines")
        return
    for k in fm.pop("__unsafe__", []):
        r.err("frontmatter", f"{k}: unquoted value contains ': ' or ' #' or starts with a YAML indicator; "
                             "a real YAML loader rejects it — quote the value or use a > block")
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        r.err("frontmatter", "name is missing")
    else:
        if len(name) > 64:
            r.err("frontmatter", f"name is {len(name)} chars (max 64)")
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", name):
            r.err("frontmatter", f"name '{name}' must be lowercase letters, digits and single hyphens")
        if re.search(r"anthropic|claude", name):
            r.err("frontmatter", f"name '{name}' contains a reserved word (anthropic / claude)")
        if name != SK.name:
            r.warn("frontmatter", f"name '{name}' differs from the folder name '{SK.name}'")
    if not desc:
        r.err("frontmatter", "description is missing or empty")
    else:
        if len(desc) > 1024:
            r.err("frontmatter", f"description is {len(desc)} chars (max 1024)")
        if "<" in desc or ">" in desc:
            r.err("frontmatter", "description contains angle brackets / XML tags")
        if re.match(r"^\s*(I|I'm|We|You|Your)\b", desc) or re.search(r"\b(I can|I will|I'm|my skills)\b", desc):
            r.warn("frontmatter", "description should be written in the third person (no I / you openings)")
        if len(desc) > 200:
            r.info("frontmatter", f"description is {len(desc)} chars; claude.ai uploads use a short description — "
                                  "package_skill.py writes the frontmatter `claude_ai_description` (≤200) into the package")
    short = fm.get("claude_ai_description", "")
    if short and len(short) > 200:
        r.err("frontmatter", f"claude_ai_description is {len(short)} chars (max 200)")
    extra = sorted(set(fm) - UPLOAD_KEYS - PACKAGE_ONLY_KEYS)
    if extra:
        r.warn("frontmatter", f"frontmatter keys {extra} are accepted by Claude Code but rejected by zip upload validators")
    if len(fm.get("compatibility", "")) > 500:
        r.err("frontmatter", "compatibility is longer than 500 chars")
    n = len(body.splitlines())
    if n >= 500:
        r.warn("frontmatter", f"SKILL.md body is {n} lines (keep it under 500; move detail to references/)")
    extras = [rel(p) for p in skill_files({".md"}) if p.name == "SKILL.md" and p != sm
              and not rel(p).startswith("evals/")]
    if extras:
        r.err("frontmatter", f"more than one SKILL.md in the package: {extras}")


# ------------------------------------------------------------------ records

def load_records(r: Report):
    rows = []
    for f in sorted((P.DATA / "powers").glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            r.err("records", f"{rel(f)} does not parse: {e}")
            continue
        if not isinstance(data, list):
            r.err("records", f"{rel(f)} must be a JSON list")
            continue
        for i, rec in enumerate(data):
            if not isinstance(rec, dict):
                r.err("records", f"{rel(f)}[{i}] is not an object")
                continue
            rows.append((f, i, rec))
    return rows


def check_records(r: Report, rows):
    r.checks["records"] += 1
    ids = Counter(str(rec.get("id")) for _f, _i, rec in rows)
    for dup, n in ids.items():
        if n > 1:
            r.err("records", f"duplicate id {dup} ({n}×)")
    bad = Counter()
    for f, i, rec in rows:
        rid = rec.get("id", f"{f.stem}[{i}]")
        dom = rec.get("domain") or P.DEFAULT_DOMAIN
        general = dom != P.DEFAULT_DOMAIN and f.stem not in BC.MOTION_STEMS
        need = GENERAL_KEYS if general else BASE_KEYS
        missing = [k for k in need if k not in rec]
        if missing:
            r.err("records", f"{rid}: missing keys {missing}")
        for k in LIST_KEYS:
            if k in rec and not isinstance(rec[k], list):
                r.err("records", f"{rid}: {k} must be a list")
        for k in ("id", "family", "name_ar", "name_en", "status", "what"):
            if k in rec and not (isinstance(rec[k], str) and rec[k].strip()):
                r.err("records", f"{rid}: {k} must be a non-empty string")
        st = rec.get("status")
        if st not in P.STATUSES:
            r.err("records", f"{rid}: invalid status {st!r}")
        if not ID_RE.match(str(rec.get("id", ""))):
            r.err("records", f"{rid}: id must look like PREFIX-NN (2 digits, 3 above 99; motion add-ons PREFIX-XNN)")
        if rec.get("family") != f.stem:
            r.err("records", f"{rid}: family {rec.get('family')!r} differs from file {f.name}")
        if rec.get("domain") and rec["domain"] not in P.DOMAINS:
            r.err("records", f"{rid}: unknown domain {rec['domain']!r} (known: {', '.join(P.DOMAINS)})")
        if general:
            meta = P.FAMILY_META.get(f.stem)
            if meta and not re.match(r"^%s-\d{2,3}$" % re.escape(meta[0]), str(rec.get("id", ""))):
                r.err("records", f"{rid}: ids in {f.stem} must be {meta[0]}-NN")
            if meta and dom != meta[1]:
                r.err("records", f"{rid}: domain {dom!r} but {f.stem} belongs to {meta[1]!r}")
            if st == "seen":
                r.err("records", f"{rid}: 👁 seen is for motion powers only")
        if st == "proven" and not rec.get("proof"):
            r.err("records", f"{rid}: ✅ proven needs at least one proof entry")
        req = rec.get("requires")
        if req is not None:
            if not isinstance(req, list):
                r.err("records", f"{rid}: requires must be a list")
            else:
                for k in req:
                    if k not in REQ_KEYS:
                        r.err("records", f"{rid}: requires names unknown requirement {k!r} (add it to data/requirements.json)")
        scope = rec.get("proof_scope")
        if scope is not None and scope not in PROOF_SCOPES:
            r.err("records", f"{rid}: proof_scope {scope!r} must be one of {PROOF_SCOPES}")
        if st == "proven" and scope in (None, "none", "missing"):
            r.err("records", f"{rid}: ✅ proven needs proof_scope repo/session/archive/sibling/receipt (run scripts/relabel_proofs.py)")
        if rec.get("name_ar") and not re.search(r"[؀-ۿ]", rec["name_ar"]):
            bad["name_ar without Arabic letters"] += 1
        if rec.get("name_en") and not re.search(r"[A-Za-z]", rec["name_en"]):
            bad["name_en without Latin letters"] += 1
    for k, n in bad.items():
        r.warn("records", f"{n} record(s) with {k}")
    r.info("records", f"{len(rows)} records · {len(ids)} unique ids · {len({rec.get('family') for _f, _i, rec in rows})} families")


# ------------------------------------------------------------------ proofs

PROOF_SKIP = ("style:", "owner-upload:", "session-", "http://", "https://")
# proof_scope: where a record's best proof lives. repo = a file in this repository (verifiable here);
# session = a dated run log; archive = an owner upload; sibling = a file in one of the owner's other repositories;
# receipt = a free-text run receipt; style/url = reference only; none/missing = not a valid state for ✅.
REQ_KEYS = {k for k in json.loads((SK / "data" / "requirements.json").read_text(encoding="utf-8")) if not k.startswith("_")} if (SK / "data" / "requirements.json").exists() else set()
PROOF_SCOPES = ("repo", "session", "archive", "sibling", "receipt", "style", "url", "missing", "none")


def resolve_proof(p: str):
    """Return (path or None, reason) for a proof entry relative to BASE."""
    q = p.strip().split("#")[0]
    q = re.sub(r":\d+(?:-\d+)?$", "", q)
    if q.startswith("/"):
        return Path(q), "absolute"
    head = q.split("/")[0]
    skill_prefix = f"kosif-tool/.claude/skills/{SK.name}/"
    if q.startswith(skill_prefix):
        return SK / q[len(skill_prefix):], "skill"
    if head == "kosif-tool":
        return (REPO / q[len("kosif-tool/"):], "repo") if IN_REPO else (None, "repo not present")
    root = BASE / head
    if not root.exists():
        return None, f"{head}/ not on this machine"
    return BASE / q, "other"


def check_proofs(r: Report, rows):
    r.checks["proofs"] += 1
    checked, skipped, free, absent = 0, Counter(), 0, Counter()
    for f, _i, rec in rows:
        for p in rec.get("proof") or []:
            if not isinstance(p, str) or not p.strip():
                r.warn("proofs", f"{rec.get('id')}: empty proof entry")
                continue
            if p.startswith(PROOF_SKIP):
                skipped[p.split(":")[0] + ":"] += 1
                continue
            first = p.split("/")[0]
            if " " in first or (":" in first and not re.match(r"^[\w.-]+$", first.split(":")[0])) or "/" not in p:
                free += 1  # free-text receipt such as "run here 2026-10-16: ..."
                continue
            path, why = resolve_proof(p)
            if path is None:
                absent[why] += 1
                continue
            checked += 1
            if not path.exists():
                level = r.err if why in ("skill", "repo") or f.stem not in BC.MOTION_STEMS else r.warn
                level("proofs", f"{rec.get('id')}: proof path not found: {p}")
    unbacked = []
    for f, _i, rec in rows:
        if rec.get("status") != "proven":
            continue
        ok = False
        for p in rec.get("proof") or []:
            if not isinstance(p, str):
                continue
            path, why = resolve_proof(p)
            if why in ("skill", "repo") and path is not None and path.exists():
                ok = True
                break
        if not ok:
            unbacked.append((f.stem in BC.MOTION_STEMS, rec.get("id")))
    if unbacked:
        gen = [i for m, i in unbacked if not m]
        mot = [i for m, i in unbacked if m]
        for label, ids in (("general", gen), ("motion", mot)):
            if ids:
                r.warn("proofs", f"{len(ids)} {label} ✅ record(s) have no proof file under kosif-tool/ "
                                 f"(session/owner/other-repo receipts only; not verifiable from this copy): "
                                 + ", ".join(ids[:8]) + (" …" if len(ids) > 8 else ""))
    note = f"{checked} proof paths checked"
    if skipped:
        note += " · skipped " + ", ".join(f"{k} {v}" for k, v in skipped.most_common())
    if free:
        note += f" · {free} free-text receipts"
    if absent:
        note += " · not verifiable here: " + ", ".join(f"{k} ({v})" for k, v in absent.most_common(6))
    r.info("proofs", note)


# ------------------------------------------------------------------ links, toc, names, secrets

def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def link_files():
    files = [SK / "SKILL.md"] if (SK / "SKILL.md").is_file() else []
    for sub in ("references", "proofs"):
        d = SK / sub
        if d.is_dir():
            files += [p for p in sorted(d.rglob("*.md")) if not any(x in SKIP_DIRS for x in p.parts)]
    return files


def check_links(r: Report):
    r.checks["links"] += 1
    n = 0
    for f in link_files():
        text = strip_code(f.read_text(encoding="utf-8", errors="replace"))
        for target in LINK_RE.findall(text):
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|//)", target, re.I):
                continue
            path = urllib.parse.unquote(target.split("#")[0].split("?")[0])
            if not path:
                continue
            n += 1
            if not (f.parent / path).exists():
                r.err("links", f"{rel(f)}: broken link → {target}")
    r.info("links", f"{n} relative links checked")


def check_toc(r: Report):
    r.checks["toc"] += 1
    for f in skill_files({".md"}):
        if rel(f).startswith("evals/"):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        n = text.count("\n") + 1
        if n > 100 and not TOC_RE.search(text):
            r.warn("toc", f"{rel(f)} has {n} lines but no contents heading (## الفهرس / contents)")


def check_names(r: Report):
    r.checks["names"] += 1
    for f in skill_files(TEXT_EXT):
        if f.name in ("check_skill.py",):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        hits = sorted(set(m.group(0) for m in MODEL_RE.finditer(text)))
        if not hits:
            continue
        legacy = f.stem in BC.MOTION_STEMS and rel(f).startswith(("data/powers/", "references/powers/"))
        (r.warn if legacy else r.err)("names", f"{rel(f)} names a model or version: {', '.join(hits[:5])}"
                                      + (" (pre-existing motion data)" if legacy else ""))


def check_secrets(r: Report):
    r.checks["secrets"] += 1
    for f in skill_files(TEXT_EXT):
        if f.name == "check_skill.py":
            continue
        m = SECRET_RE.search(f.read_text(encoding="utf-8", errors="replace"))
        if m:
            r.err("secrets", f"{rel(f)} contains something that looks like a credential ({m.group(0)[:8]}…)")
        m = LEAK_RE.search(f.read_text(encoding="utf-8", errors="replace"))
        if m:
            r.err("secrets", f"{rel(f)} leaks a session or scratchpad path ({m.group(0)[:24]}…); use a relative or <placeholder> path")


# ------------------------------------------------------------------ chapters & counts

def check_chapters(r: Report):
    r.checks["chapters"] += 1
    fams, errors = BC.general_families()
    for e in errors:
        r.err("chapters", e)
    for stem, _path, rows in fams:
        out = BC.OUT / f"{stem}.md"
        if not out.is_file():
            r.err("chapters", f"references/powers/{stem}.md is missing — run python3 scripts/build_chapters.py")
            continue
        old = out.read_text(encoding="utf-8")
        if BC.MARKER not in old:
            r.err("chapters", f"references/powers/{stem}.md exists without the generated marker (hand-written?)")
        elif old != BC.render(stem, rows):
            r.err("chapters", f"references/powers/{stem}.md is out of date — run python3 scripts/build_chapters.py")
    r.info("chapters", f"{len(fams)} general famil{'y' if len(fams) == 1 else 'ies'}; motion chapters are hand-made and not compared")


def live_counts() -> dict:
    powers, styles = P.load_powers(), P.load_styles()
    st = Counter(p.get("status") for p in powers)
    c = {"powers": len(powers), "families": len({p.get("family") for p in powers}),
         "domains": len({p.get("domain") for p in powers}), "styles": len(styles),
         "watched": sum(1 for s in styles if s.get("watched"))}
    c.update({s: st.get(s, 0) for s in P.STATUSES})
    return c


def marker_line(c: dict) -> str:
    return "<!-- counts: " + " ".join(f"{k}={c[k]}" for k in COUNT_KEYS) + " -->"


def check_counts(r: Report):
    r.checks["counts"] += 1
    sm = SK / "SKILL.md"
    text = sm.read_text(encoding="utf-8") if sm.is_file() else ""
    m = re.search(r"<!--\s*counts:(.*?)-->", text, re.S)
    live = live_counts()
    if not m:
        r.warn("counts", "SKILL.md has no <!-- counts: ... --> marker; add the line from --print-counts next to the numbers")
        return
    pairs = dict(re.findall(r"([a-z]+)\s*=\s*([\d,]+)", m.group(1)))
    if not pairs:
        r.err("counts", "counts marker has no key=value pairs")
    for k, v in pairs.items():
        if k not in live:
            r.warn("counts", f"counts marker key {k!r} is unknown (known: {', '.join(COUNT_KEYS)})")
        elif int(v.replace(",", "")) != live[k]:
            r.err("counts", f"SKILL.md says {k}={v} but the catalog has {live[k]} — update the marker and the visible numbers")


# ------------------------------------------------------------------ evals

def load_evals(r: Report = None):
    f = SK / "evals" / "evals.json"
    if not f.is_file():
        if r:
            r.warn("evals", "evals/evals.json is missing (add at least 3 cases)")
        return []
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        if r:
            r.err("evals", f"evals/evals.json does not parse: {e}")
        return []
    cases = data.get("evals") if isinstance(data, dict) else data
    return cases if isinstance(cases, list) else []


def check_evals(r: Report):
    r.checks["evals"] += 1
    cases = load_evals(r)
    if not cases:
        return
    if len(cases) < 3:
        r.warn("evals", f"only {len(cases)} eval case(s); add at least 3")
    seen = Counter()
    for i, c in enumerate(cases):
        if not isinstance(c, dict):
            r.err("evals", f"case {i} is not an object")
            continue
        seen[c.get("id")] += 1
        if not (c.get("query") or c.get("prompt")):
            r.err("evals", f"case {c.get('id', i)} has no query/prompt")
        if not (c.get("expected_behavior") or c.get("expectations") or c.get("expected_output")):
            r.err("evals", f"case {c.get('id', i)} has no expected_behavior")
        rt = c.get("routing")
        if rt is not None and not (isinstance(rt, dict) and isinstance(rt.get("expect_any"), list) and rt["expect_any"]):
            r.err("evals", f"case {c.get('id', i)}: routing.expect_any must be a non-empty list of prefixes")
    for k, n in seen.items():
        if n > 1:
            r.err("evals", f"duplicate eval id {k}")
    r.info("evals", f"{len(cases)} eval cases ({sum(1 for c in cases if isinstance(c, dict) and c.get('routing'))} with routing checks)")


def run_evals(min_pass: float, as_json: bool) -> int:
    if not (SK / "evals" / "evals.json").is_file():
        print("routing evals: evals/evals.json is not in this copy (packages leave it out) — skipped")
        return 0
    cases = load_evals()
    powers, styles = P.load_powers(), P.load_styles()
    prefixes = {P.prefix_of(p) for p in powers}
    results = []
    for c in cases:
        rt = c.get("routing") if isinstance(c, dict) else None
        if not rt:
            continue
        q = c.get("query") or c.get("prompt") or ""
        want = [x.upper() for x in rt.get("expect_any", [])]
        k = int(rt.get("top_k", 8))
        res = P.suggest(powers, styles, q, limit=max(k, 3))
        picks = [p for _s, p in res["picked"]]
        top = [P.prefix_of(p) for p in picks[:k]]
        row = {"id": c.get("id"), "query": q, "expect_any": want, "top": [p.get("id") for p in picks[:k]], "why": ""}
        if not any(w in prefixes for w in want):
            row["result"] = "SKIP"
            row["why"] = "expected families not in the catalog yet: " + ", ".join(want)
        else:
            fails = []
            if not any(w in top for w in want):
                fails.append(f"none of {want} in top {k}")
            need = [x.upper() for x in rt.get("expect_all", [])]
            miss = [w for w in need if w not in top]
            if miss:
                fails.append(f"{miss} missing from top {k} (expect_all)")
            dom = rt.get("expect_domain")
            if dom and dom not in [p.get("domain") for p in picks[:3]]:
                fails.append(f"domain {dom} not in top 3")
            mo = rt.get("motion_output")
            if mo is not None and bool(res["motion"]) != bool(mo):
                fails.append(f"motion mode {res['motion']} (expected {mo})")
            row["result"] = "FAIL" if fails else "PASS"
            row["why"] = "; ".join(fails)
        results.append(row)
    ran = [x for x in results if x["result"] != "SKIP"]
    passed = sum(1 for x in ran if x["result"] == "PASS")
    rate = passed / len(ran) if ran else 0.0
    if as_json:
        print(json.dumps({"cases": results, "ran": len(ran), "passed": passed, "skipped": len(results) - len(ran),
                          "pass_rate": round(rate, 3), "min_pass": min_pass}, ensure_ascii=False, indent=1))
    else:
        for x in results:
            print(f"{x['result']:<4} #{x['id']:<3} {x['query'][:60]:<60} → {' '.join(x['top'][:5])}" + (f"  [{x['why']}]" if x["why"] else ""))
        print(f"\nrouting evals: {passed}/{len(ran)} passed ({rate:.0%}) · {len(results) - len(ran)} skipped · "
              f"threshold {min_pass:.0%} · these check routing only; expected_behavior needs a real run and a grader")
    return 0 if ran and rate >= min_pass else 1


# ------------------------------------------------------------------ main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate the kosif-superpowers skill")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--json", action="store_true", help="JSON report")
    ap.add_argument("--print-counts", action="store_true", help="print the counts marker for SKILL.md and exit")
    ap.add_argument("--evals", action="store_true", help="run all checks AND the routing evals (both must pass)")
    ap.add_argument("--min-pass", type=float, default=0.8, help="routing pass rate needed with --evals (default 0.8)")
    ap.add_argument("-v", "--verbose", action="store_true", help="also print info lines")
    a = ap.parse_args(argv)
    if a.print_counts:
        print(marker_line(live_counts()))
        return 0
    r = Report()
    check_frontmatter(r)
    rows = load_records(r)
    check_records(r, rows)
    check_proofs(r, rows)
    check_links(r)
    check_toc(r)
    check_chapters(r)
    check_counts(r)
    check_names(r)
    check_secrets(r)
    check_evals(r)
    errors, warns = r.count("error"), r.count("warn")
    failed = errors > 0 or (a.strict and warns > 0)
    if a.json:
        print(json.dumps({"ok": not failed, "errors": errors, "warnings": warns, "checks": list(r.checks),
                          "items": [{"level": lv, "check": c, "message": m} for lv, c, m in r.items]},
                         ensure_ascii=False, indent=1))
        if a.evals:
            return max(1 if failed else 0, run_evals(a.min_pass, a.json))
        return 1 if failed else 0
    for lv, c, m in r.items:
        if lv == "info" and not a.verbose:
            continue
        print(f"{lv.upper():<5} [{c}] {m}")
    print(f"check_skill: {len(r.checks)} checks · {errors} error(s) · {warns} warning(s) → {'FAIL' if failed else 'OK'}")
    if a.evals:
        print()
        return max(1 if failed else 0, run_evals(a.min_pass, a.json))
    return 1 if failed else 0


if __name__ == "__main__":
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError, ImportError):
        pass
    sys.exit(main())
