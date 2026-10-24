#!/usr/bin/env python3
"""KOSIF Self-Council — five Claude-derived critics review every skill and feature of this repository (appendix A37).

The council has five fixed personas, each a different lens of Claude itself: P1 the Strict Engineer (correctness and
tests), P2 the New Egyptian User (clarity, first minute, Arabic), P3 the Devil's Advocate (failure modes, what is useless
or duplicated), P4 the Architect (overlap, simplification, wiring between skills) and P5 the Innovator (what is missing,
what would make it 10x). The script never calls a model: it inventories the reviewable units, picks the weakest batch,
writes each persona's prompt, validates what each persona returned, and merges the five reviews into a ranked list of
proposals. Claude runs the personas as five parallel subagents (Agent tool or Workflow), or, when no agent tool exists,
as five simulated voices in one context, which the report then labels SIMULATED.

From the repository root:
  python3 .claude/skills/kosif-superpowers/scripts/self_council.py inventory [--kind script] [--summary] [--out inv.json]
  python3 .claude/skills/kosif-superpowers/scripts/self_council.py plan --batch 10 --dir out/self-council/<run> [--kind script] [--revisit]
  python3 .claude/skills/kosif-superpowers/scripts/self_council.py ingest --dir out/self-council/<run> --persona P1 --file p1.json [--simulated]
  python3 .claude/skills/kosif-superpowers/scripts/self_council.py report --dir out/self-council/<run> [--top 10] [--out-md R.md --out-json R.json] [--partial]
  python3 .claude/skills/kosif-superpowers/scripts/self_council.py status
  python3 .claude/skills/kosif-superpowers/scripts/self_council.py personas

Units and ids: skill:<name> (.claude/skills/*/SKILL.md), script:<stem> (this skill's scripts/), app:<name> (apps/*/),
tool:<name> (tools/*), playbook:<stem> (playbooks/*.md), workflow:<name> (workflows/*/). The ledger
(data/self_council_ledger.json, override with --ledger) remembers which units were planned and reviewed, with the content
hash at review time, so successive runs cover the whole app and a unit that changed after its review comes back as stale.
Every option takes --root to point at another checkout (the tests use it). Python stdlib only; exit 2 with one line on
stderr on any refusal.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _secrets  # noqa: E402

SCHEMA = "kosif.self-council.v1"
LEDGER_SCHEMA = "kosif.self-council-ledger.v1"
REVIEW_SCHEMA = "kosif.self-council-review.v1"
REPORT_SCHEMA = "kosif.self-council-report.v1"
DEFAULT_ROOT = HERE.parents[3]  # scripts -> kosif-superpowers -> skills -> .claude -> repository root
SKILL_REL = Path(".claude/skills/kosif-superpowers")
LEDGER_REL = SKILL_REL / "data" / "self_council_ledger.json"
KINDS = ("skill", "script", "app", "tool", "playbook", "workflow")
CODE_EXT = (".py", ".cjs", ".mjs", ".js", ".sh", ".ps1")
SKIP_DIRS = {"__pycache__", "node_modules", ".git", "dist", "build", ".gradle", "vendor", ".venv"}
MAX_HASH_BYTES = 2_000_000
SEVERITY = {"critical": 8, "high": 5, "medium": 3, "low": 1}
EFFORT = {"S": 1, "M": 2, "L": 4}
CATEGORIES = ("bug", "test", "docs", "ux", "arabic", "duplicate", "architecture", "feature", "security", "performance")
MAX_FINDINGS = 8
# weakness weights: the plan reviews the weakest units first
WEIGHTS = {"NO_TEST": 3, "INDIRECT_TEST_ONLY": 1, "NO_DOCSTRING": 2, "NO_USAGE": 1, "UNREGISTERED": 1,
           "LARGE_UNTESTED": 2, "HUGE": 1, "NO_DESCRIPTION": 3, "NO_README": 2, "NO_TEST_REPORT": 1}
LARGE, HUGE = 400, 1500

COMMON_CHECK = (
    "Open the unit's files yourself before you claim anything; every finding cites a repository path you opened "
    "(path, path:line or path#anchor) as evidence.",
    "Propose a concrete change a maintainer can do (what to edit, add or delete), with effort S (<30 min), M (<half a day) "
    "or L (more), and your confidence from 0 to 1.",
    "Do not edit, commit, publish, install, spend money or generate media: you only read and run read-only commands.",
)
PERSONAS = (
    {"id": "P1", "name_ar": "المهندس الصارم", "en": "The Strict Engineer", "lens": "correctness and tests",
     "stance": "لا يصدّق أي سطر بلا اختبار يثبته؛ يبحث عن الخطأ الصامت والمدخل الذي يكسر الأداة",
     "checklist": ("Run its tests (or --help when none exist) and say exactly what you ran.",
                   "Find one input or edge case that breaks it or gives a silent wrong answer.",
                   "Check exit codes, determinism, error messages and that refusals are tested.",
                   "Name the smallest missing test that would catch the worst bug."),
     "field": "test_verdict", "field_doc": '{"status": "covered|partial|none", "ran": "<the command you ran, or \'not run\'>"}'},
    {"id": "P2", "name_ar": "المستخدم المصري الجديد", "en": "The New Egyptian User", "lens": "clarity, first minute, Arabic",
     "stance": "مستخدم مصري أول مرة يشوف الأداة: هل أفهم هي بتعمل إيه في دقيقة؟ هل العربي طبيعي؟ هل الخطأ بيقولّي أعمل إيه؟",
     "checklist": ("Read only what a newcomer sees first (docstring, --help, README, SKILL.md): can you tell what it does and how to run it in 60 seconds?",
                   "Is there a copy-paste example that works from the repository root?",
                   "Would an Egyptian user's natural request (عامية) reach this unit? Is its Arabic natural, not machine-translated?",
                   "Are error messages actionable (what went wrong and what to do next)?"),
     "field": "first_minute", "field_doc": '{"clarity": <1-5>, "would_say": "<the request an Egyptian user would type to reach it>"}'},
    {"id": "P3", "name_ar": "محامي الشيطان", "en": "The Devil's Advocate", "lens": "failure modes, uselessness, duplication",
     "stance": "يفترض أن الوحدة لا لزوم لها حتى يثبت العكس؛ يبحث عن طريقة فشلها وعن نسخة أخرى منها في المستودع",
     "checklist": ("How does this fail in real use (missing dependency, network, wrong platform, stale data)?",
                   "Is it duplicated by another unit? Name it.",
                   "Does any claim in its docs overstate what the code does?",
                   "If it were deleted tomorrow, who would notice?"),
     "field": "keep_or_kill", "field_doc": '{"decision": "keep|merge|rewrite|delete", "why": "<one sentence>"}'},
    {"id": "P4", "name_ar": "المعماري", "en": "The Architect", "lens": "overlap, simplification, wiring between skills",
     "stance": "ينظر للوحدة كقطعة في نظام: من يستدعيها، ومن يجب أن يستدعيها، وما الذي يُدمج أو يُبسَّط",
     "checklist": ("Who calls or documents this unit (grep the repository), and who should but does not?",
                   "What overlaps with it, and what single shape would replace both?",
                   "Is it registered where the hub, protocol and tests expect (data/tools.json, an appendix, an eval)?",
                   "What is the one simplification that removes the most code or steps?"),
     "field": "wiring", "field_doc": '{"overlaps": ["<unit id or path>"], "should_call": ["<unit id or path>"]}'},
    {"id": "P5", "name_ar": "المبتكر", "en": "The Innovator", "lens": "missing capabilities, the 10x version",
     "stance": "يسأل ما الذي ينقص لتصبح الوحدة أفضل بعشرة أضعاف للمستخدم، لا أفضل بعشرة في المئة",
     "checklist": ("What does the user try to do right after using this unit, and could the unit do it?",
                   "What capability from elsewhere in the repository or the session would multiply its value?",
                   "What would the 10x version look like, and what is its first small step?",
                   "Keep ideas grounded: cite the file that shows the gap."),
     "field": "ten_x", "field_doc": '{"idea": "<the 10x version>", "first_step": "<a first step of effort S or M>"}'},
)
PERSONA_IDS = tuple(p["id"] for p in PERSONAS)


class SelfCouncilError(Exception):
    def __init__(self, code: str, msg: str):
        super().__init__(msg)
        self.code = code


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def save(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SelfCouncilError("UNREADABLE", f"{path.name}: {type(exc).__name__}") from None


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def line_count(text: str) -> int:
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


# ------------------------------------------------------------------ inventory

def _walk(d: Path) -> list:
    out = []
    for dp, dns, fns in os.walk(d):
        dns[:] = sorted(x for x in dns if x not in SKIP_DIRS)
        out += [Path(dp) / f for f in sorted(fns)]
    return out


def _hash_files(files: list, root: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(files):
        try:
            data = f.read_bytes()[:MAX_HASH_BYTES]
        except OSError:
            continue
        h.update(f.relative_to(root).as_posix().encode("utf-8") + b"\0" + data + b"\0")
    return h.hexdigest()


_PY_DOC = re.compile(r'\A(?:#[^\n]*\n|\s*\n)*\s*[rRuU]?("""|\'\'\')(.*?)\1', re.S)
_JS_DOC = re.compile(r"\A(?:#![^\n]*\n)?\s*(?:['\"]use strict['\"];?\s*)?(?:/\*(.*?)\*/|((?://[^\n]*\n)+))", re.S)
_SH_DOC = re.compile(r"\A(?:#![^\n]*\n)?((?:#[^\n]*\n)+)")
_USAGE = re.compile(r"usage|python3? |node |\.sh\b|powershell|\$ |(?:^|\s)\w+ --[a-z][\w-]+|الاستخدام|طريقة التشغيل", re.I | re.M)


def docstring_of(path: Path, text: str) -> str:
    head = text[:8000]
    if path.suffix == ".py":
        m = _PY_DOC.match(head)
        return m.group(2).strip() if m else ""
    if path.suffix in (".js", ".cjs", ".mjs"):
        m = _JS_DOC.match(head)
        return (m.group(1) or m.group(2) or "").strip() if m else ""
    if path.suffix in (".sh", ".ps1"):
        m = _SH_DOC.match(head)
        return m.group(1).strip() if m else ""
    return ""


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out = {}
    for ln in text[3:end].splitlines():
        if ":" in ln and not ln.startswith((" ", "\t")):
            k, v = ln.split(":", 1)
            out[k.strip()] = v.strip().strip('"\'')
    return out


def test_index(root: Path) -> tuple:
    """(names, refs): test file names, and {module/file stem: [test files that import or name it]}."""
    files = []
    sk = root / SKILL_REL
    for d, pats in ((sk / "evals", ("test_*",)), (sk / "scripts", ("test_*",)), (root / "tests", ("test_*", "*.test.*", "*smoke*"))):
        if d.is_dir():
            for pat in pats:
                files += [p for p in d.glob(pat) if p.is_file()]
    if (sk / "proofs").is_dir():  # script-style runners next to their proofs (e.g. proofs/general-writing/test_writing.py)
        files += [p for p in (sk / "proofs").rglob("test_*.py") if p.is_file()]
    skills = root / ".claude" / "skills"
    if skills.is_dir():
        for s in skills.iterdir():
            if s.is_dir() and s.name != SKILL_REL.name:
                files += [p for p in s.rglob("test_*") if p.is_file() and not (set(p.parts) & SKIP_DIRS)]
    files = sorted(set(files))
    rx = re.compile(r"(?:^|\s)import\s+([\w, ]+)|from\s+(\w+)\s+import|([\w-]+)\.(?:py|cjs|mjs|js|sh)\b", re.M)
    refs = {}
    for f in files:
        rel = f.relative_to(root).as_posix()
        for m in rx.finditer(read_text(f)):
            names = [part.split()[0] for part in (m.group(1) or "").split(",") if part.split()]  # "import x as y" -> x
            names += [m.group(2) or "", m.group(3) or ""]
            for n in names:
                if n:
                    refs.setdefault(n, set()).add(rel)
    return {f.name for f in files}, {k: sorted(v) for k, v in refs.items()}


def changelog_sections(root: Path) -> list:
    """[(heading, text)] of the protocol CHANGELOG, newest first (as the file orders them)."""
    text = read_text(root / SKILL_REL / "references" / "protocol" / "CHANGELOG.md")
    out, head, buf = [], None, []
    for ln in text.splitlines():
        if ln.startswith("## "):
            if head:
                out.append((head, "\n".join(buf)))
            head, buf = ln[3:].strip(), []
        elif head:
            buf.append(ln)
    if head:
        out.append((head, "\n".join(buf)))
    return [(h.replace("(هذا الإصدار)", "").strip(), t) for h, t in out if not h.startswith(("الفهرس", "خريطة"))]


def last_mention(sections: list, keys: list):
    for head, text in sections:
        for k in keys:
            if k and re.search(r"(?<![\w-])" + re.escape(k) + r"(?![\w-])", text):
                return head
    return None


def registered_paths(root: Path) -> dict:
    """{(root, path): {"evidence", "tests"}} from data/tools.json; its tests list names test files a scan cannot see
    (a test that drives the unit through another script)."""
    try:
        reg = json.loads((root / SKILL_REL / "data" / "tools.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {(t.get("root"), t.get("path", "").rstrip("/")): {"evidence": t.get("evidence"),
                                                             "tests": [x for x in t.get("tests") or [] if (root / x).is_file()]}
            for t in reg.get("tools", []) if isinstance(t, dict)}


def _reg_entry(reg: dict, key: tuple, is_dir: bool):
    if key in reg:
        return reg[key]
    if is_dir:  # a folder tool is registered by a file inside it
        return next((v for (r, p), v in sorted(reg.items()) if r == key[0] and p.startswith(key[1] + "/")), None)
    return None


def _apply_registry(sig: dict, reasons: list, entry) -> None:
    sig["registered"] = entry is not None
    sig["evidence"] = entry["evidence"] if entry else None
    extra = [t for t in (entry or {}).get("tests", []) if Path(t).name not in {Path(x).name for x in sig["tests"]}]
    if extra:
        sig["tests"] = (sig["tests"] + extra)[:4]
        if sig["has_test"] == "none":
            sig["has_test"] = "registered"  # a test the registry names, which drives the unit through something else
            for r in ("NO_TEST", "LARGE_UNTESTED"):
                if r in reasons:
                    reasons.remove(r)
            reasons.insert(0, "INDIRECT_TEST_ONLY")


def _weak(reasons: list) -> int:
    return sum(WEIGHTS.get(r, 0) for r in reasons)


def _code_signals(path: Path, text: str, stem: str, tests: tuple, direct_names: set) -> tuple:
    names, refs = tests
    doc = docstring_of(path, text)
    direct = sorted(n for n in names if n.split(".")[0] in direct_names)
    indirect = [t for t in refs.get(stem, []) if Path(t).name not in direct]
    has_test = "direct" if direct else ("indirect" if indirect else "none")
    sig = {"lines": line_count(text), "docstring": bool(doc), "usage": bool(doc and _USAGE.search(doc)),
           "has_test": has_test, "tests": (direct + indirect)[:4]}
    reasons = []
    if has_test == "none":
        reasons.append("NO_TEST")
        if sig["lines"] > LARGE:
            reasons.append("LARGE_UNTESTED")
    elif has_test == "indirect":
        reasons.append("INDIRECT_TEST_ONLY")
    if not doc:
        reasons.append("NO_DOCSTRING")
    elif not sig["usage"]:
        reasons.append("NO_USAGE")
    if sig["lines"] > HUGE:
        reasons.append("HUGE")
    return sig, reasons


def _unit(kind, name, path, files, root, sig, reasons, sections, keys):
    sig["changelog"] = last_mention(sections, keys)
    return {"id": f"{kind}:{name}", "kind": kind, "path": path, "sha256": _hash_files(files, root),
            "signals": sig, "reasons": reasons, "weakness": _weak(reasons)}


def inventory(root: Path) -> list:
    root = root.resolve()
    tests = test_index(root)
    sections = changelog_sections(root)
    reg = registered_paths(root)
    units = []
    skills = root / ".claude" / "skills"
    for d in sorted(p for p in skills.iterdir() if p.is_dir()) if skills.is_dir() else []:
        sm = d / "SKILL.md"
        if not sm.is_file():
            continue
        text = read_text(sm)
        fm = frontmatter(text)
        own_tests = [p for p in d.rglob("*") if p.is_file() and (p.name.startswith("test_") or ".test." in p.name)
                     and not (set(p.parts) & SKIP_DIRS)] if d.name != SKILL_REL.name else [None]
        sig = {"lines": line_count(text), "description": bool(fm.get("description")), "name": bool(fm.get("name")),
               "has_test": "direct" if own_tests else "none",
               "scripts": sum(1 for p in d.rglob("*") if p.suffix in CODE_EXT and not (set(p.parts) & SKIP_DIRS))
               if d.name != SKILL_REL.name else None}
        reasons = ([] if sig["description"] else ["NO_DESCRIPTION"]) + ([] if own_tests else ["NO_TEST"])
        units.append(_unit("skill", d.name, sm.relative_to(root).as_posix(), [sm], root, sig, reasons, sections, [d.name]))
    sd = root / SKILL_REL / "scripts"
    for f in sorted(sd.iterdir()) if sd.is_dir() else []:
        if f.name.startswith("test_") or f.name in SKIP_DIRS:
            continue
        if f.is_dir():
            files = [p for p in _walk(f) if p.suffix in CODE_EXT]
            if not files:
                continue
            text = "\n".join(read_text(p) for p in files)
            stem, first = f.name, sorted(files)[0]
            sig, reasons = _code_signals(first, read_text(first), stem, tests, {f"test_{stem}"})
            sig["lines"], sig["files"] = line_count(text), len(files)
        elif f.suffix in (".py", ".cjs", ".mjs"):
            text, stem, files = read_text(f), f.stem, [f]
            sig, reasons = _code_signals(f, text, stem, tests, {f"test_{stem}", f"test_{stem.lstrip('_')}"})
        else:
            continue
        _apply_registry(sig, reasons, _reg_entry(reg, ("skill", f"scripts/{f.name}"), f.is_dir()))
        if f.is_file() and not f.name.startswith("_") and not sig["registered"]:
            reasons.append("UNREGISTERED")
        units.append(_unit("script", stem, f.relative_to(root).as_posix(), files, root, sig, reasons, sections, [f.name, stem]))
    for kind, base in (("app", "apps"), ("workflow", "workflows")):
        bd = root / base
        for d in sorted(p for p in bd.iterdir() if p.is_dir()) if bd.is_dir() else []:
            files = _walk(d)
            code = [p for p in files if p.suffix in CODE_EXT + (".kt", ".java", ".html", ".bat")]
            has_tests = any(p.name.startswith("test_") or ".test." in p.name or "/test/" in p.as_posix() for p in files)
            readme = (d / "README.md").is_file() or (d / "README_AR.md").is_file()
            sig = {"lines": sum(line_count(read_text(p)) for p in code), "files": len(files), "readme": readme,
                   "has_test": "direct" if has_tests else "none"}
            reasons = ([] if readme else ["NO_README"]) + ([] if has_tests else ["NO_TEST"])
            if kind == "workflow":
                sig["test_report"] = (d / "TEST_REPORT.md").is_file()
                if sig["test_report"] and "NO_TEST" in reasons:
                    reasons.remove("NO_TEST")  # a measured test report stands in for a unit test here
                elif not sig["test_report"]:
                    reasons.append("NO_TEST_REPORT")
            units.append(_unit(kind, d.name, d.relative_to(root).as_posix() + "/", files, root, sig, reasons, sections, [d.name]))
    td = root / "tools"
    for f in sorted(td.iterdir()) if td.is_dir() else []:
        if f.name in SKIP_DIRS:
            continue
        if f.is_dir():
            files = [p for p in _walk(f) if p.is_file()]
            code = [p for p in files if p.suffix in CODE_EXT]
            first = code[0] if code else (files[0] if files else None)
            if first is None:
                continue
            stem, text = f.name, read_text(first)
        elif f.suffix in CODE_EXT:
            files, first, stem, text = [f], f, f.stem, read_text(f)
        else:
            continue
        sig, reasons = _code_signals(first, text, stem, tests, {f"test_{stem}"})
        _apply_registry(sig, reasons, _reg_entry(reg, ("repo", f"tools/{f.name}"), f.is_dir()))
        units.append(_unit("tool", stem, f.relative_to(root).as_posix() + ("/" if f.is_dir() else ""), files, root, sig, reasons,
                           sections, [f.name, stem]))
    pd = root / "playbooks"
    for f in sorted(pd.glob("*.md")) if pd.is_dir() else []:
        text = read_text(f)
        sig = {"lines": line_count(text), "headings": len(re.findall(r"^#{1,4} ", text, re.M)),
               "examples": text.count("```") // 2, "has_test": "none"}
        reasons = [] if sig["examples"] else ["NO_USAGE"]
        units.append(_unit("playbook", f.stem, f.relative_to(root).as_posix(), [f], root, sig, reasons, sections,
                           [f"playbooks/{f.name}"]))
    return units


def counts_of(units: list) -> dict:
    return {k: sum(1 for u in units if u["kind"] == k) for k in KINDS}


def cmd_inventory(a) -> dict:
    units = inventory(Path(a.root))
    if a.kind:
        units = [u for u in units if u["kind"] == a.kind]
    weak = sorted(units, key=rank_key)
    res = {"schema": SCHEMA + ".inventory", "total": len(units), "counts": counts_of(units),
           "with_test": sum(1 for u in units if u["signals"].get("has_test") != "none"),
           "weakest": [f"{u['id']} w={u['weakness']} {','.join(u['reasons'])}" for u in weak[:10]]}
    if not a.summary:
        res["units"] = units
    if a.out:
        save(Path(a.out), dict(res, units=units))
        res["file"] = a.out
    return res


def rank_key(u: dict):
    return (-u["weakness"], -u["signals"].get("lines", 0), u["id"])


# ------------------------------------------------------------------ ledger

def ledger_path(a) -> Path:
    return Path(a.ledger) if getattr(a, "ledger", None) else Path(a.root) / LEDGER_REL


def load_ledger(p: Path) -> dict:
    if not p.exists():
        return {"schema": LEDGER_SCHEMA, "units": {}, "runs": {}}
    led = load(p)
    if led.get("schema") != LEDGER_SCHEMA:
        raise SelfCouncilError("LEDGER_INVALID", f"{p.name} is not a {LEDGER_SCHEMA} ledger")
    led.setdefault("units", {}), led.setdefault("runs", {})
    return led


def run_key(d: Path, root: Path) -> str:
    """The run folder as stored in the ledger: relative to the repository when inside it (no local paths in a public file)."""
    r = d.resolve()
    try:
        return r.relative_to(root.resolve()).as_posix()
    except ValueError:
        return r.as_posix()


def open_runs(led: dict, root: Path) -> set:
    """Runs that still claim their units: not reported and their folder still exists (a deleted run releases its claims)."""
    out = set()
    for k, r in led["runs"].items():
        p = Path(k) if Path(k).is_absolute() else root / k
        if not r.get("reported_at") and (p / "run.json").is_file():
            out.add(k)
    return out


def unit_state(u: dict, led: dict, open_: set) -> str:
    e = led["units"].get(u["id"])
    if not e:
        return "never"
    if e.get("state") == "planned" and e.get("run") in open_:
        return "claimed"
    if e.get("state") == "reviewed":
        return "fresh" if e.get("sha256") == u["sha256"] else "stale"
    return "pending"  # partial review, or a planned run that was deleted / reported without this unit complete


# ------------------------------------------------------------------ plan

def persona_header(p: dict) -> str:
    return (f"You are {p['id']} «{p['name_ar']}» ({p['en']}), one of five critics in the KOSIF Self-Council (appendix A37): "
            f"five lenses of Claude reviewing this repository's own skills and features. Your lens: {p['lens']}.\n"
            f"Your stance: {p['stance']}.\n"
            "Your checklist for every unit:\n" + "".join(f"  - {c}\n" for c in p["checklist"] + COMMON_CHECK) +
            "Work from the repository root. Never show or ask for another persona's review.\n")


def schema_block(p: dict) -> str:
    return ("Return ONLY JSON, one entry per unit:\n"
            '{"persona": "' + p["id"] + '", "reviews": [{"unit": "<unit id>", "summary": "<one sentence verdict>", '
            '"' + p["field"] + '": ' + p["field_doc"] + ', '
            '"findings": [{"title": "...", "category": "' + "|".join(CATEGORIES) + '", '
            '"severity": "critical|high|medium|low", "evidence": "<repo path you opened>[:line]", '
            '"proposed_change": "<the concrete edit>", "effort": "S|M|L", "confidence": 0.0}], '
            '"no_findings_reason": "<only when findings is empty>"}]}\n'
            f"At most {MAX_FINDINGS} findings per unit, most important first.\n")


def unit_block(u: dict) -> str:
    s = u["signals"]
    return (f"### {u['id']}\nPath: {u['path']}\nStatic signals: " + json.dumps(s, ensure_ascii=False, sort_keys=True) +
            f"\nWhy it was picked: {', '.join(u['reasons']) or 'coverage'} (weakness {u['weakness']}).\n")


def cmd_plan(a) -> dict:
    root = Path(a.root)
    d = Path(a.dir)
    if (d / "run.json").exists() and not a.force:
        raise SelfCouncilError("EXISTS", f"{d}/run.json exists (use --force to replace it)")
    if not 1 <= a.batch <= 50:
        raise SelfCouncilError("BATCH_RANGE", "--batch must be 1–50")
    lp = ledger_path(a)
    led = load_ledger(lp)
    key = run_key(d, root)
    if key in led["runs"] and a.force:  # replacing a run releases its earlier claims first
        for uid in led["runs"][key].get("units", []):
            if led["units"].get(uid, {}).get("run") == key and led["units"][uid].get("state") == "planned":
                led["units"][uid]["state"] = "pending"
        led["runs"].pop(key)
    units = inventory(root)
    if a.kind:
        units = [u for u in units if u["kind"] == a.kind]
    open_ = open_runs(led, root)
    states = {u["id"]: unit_state(u, led, open_) for u in units}
    order = {"never": 0, "pending": 0, "stale": 1}
    pool = sorted((u for u in units if states[u["id"]] in order), key=lambda u: (order[states[u["id"]]],) + rank_key(u))
    if a.revisit and len(pool) < a.batch:
        fresh = sorted((u for u in units if states[u["id"]] == "fresh"),
                       key=lambda u: (led["units"][u["id"]].get("reviewed_at", ""), u["id"]))
        pool += fresh
    batch = pool[:a.batch]
    if not batch:
        raise SelfCouncilError("NOTHING_TO_PLAN", "every unit is reviewed and unchanged or claimed by an open run "
                                                  "(use --revisit to re-review the oldest)")
    personas = []
    prompts = {}
    (d / "prompts").mkdir(parents=True, exist_ok=True)
    (d / "reviews").mkdir(parents=True, exist_ok=True)
    for p in PERSONAS:
        head = persona_header(p)
        batch_text = (head + f"\nThis batch has {len(batch)} units; review every one.\n\n" + "\n".join(unit_block(u) for u in batch)
                      + "\n" + schema_block(p))
        (d / "prompts" / f"{p['id']}.md").write_text(batch_text, encoding="utf-8")
        prompts[p["id"]] = {u["id"]: head + "\n" + unit_block(u) + "\n" + schema_block(p) for u in batch}
        personas.append({k: p[k] for k in ("id", "name_ar", "en", "lens", "field")})
    save(d / "prompts.json", prompts)
    run = {"schema": SCHEMA, "created_at": now_iso(), "ledger": run_key(lp, root), "batch": [u["id"] for u in batch],
           "units": {u["id"]: u for u in batch}, "states_at_plan": {u["id"]: states[u["id"]] for u in batch},
           "personas": personas, "reviews": {p: {} for p in PERSONA_IDS},
           "rules": ["Launch the five personas as five parallel subagents, one prompt file each (prompts/P1.md … P5.md).",
                     "With no agent tool, write the five voices yourself and ingest each with --simulated; the report then says SIMULATED.",
                     "A persona never sees another persona's review; every finding cites a repository path that exists.",
                     "Reviewers read and run read-only commands only: changes happen after the report, one proposal at a time."]}
    save(d / "run.json", run)
    now = now_iso()
    led["runs"][key] = {"created_at": now, "units": run["batch"], "reported_at": None}
    for u in batch:
        e = led["units"].setdefault(u["id"], {"history": []})
        e.update({"state": "planned", "run": key, "planned_at": now})
    led["updated_at"] = now
    save(lp, led)
    return {"dir": str(d), "batch": [f"{u['id']} w={u['weakness']} [{states[u['id']]}] {','.join(u['reasons'])}" for u in batch],
            "prompts": [str(d / "prompts" / f"{p}.md") for p in PERSONA_IDS], "ledger": str(lp),
            "next": "launch 5 parallel subagents (one per prompts/P*.md), save each JSON answer, then: "
                    f"self_council.py ingest --dir {d} --persona P1 --file <answer.json> (add --simulated for voices written in this context)"}


# ------------------------------------------------------------------ ingest

def parse_json_text(raw: bytes, name: str):
    text = raw.decode("utf-8-sig", errors="replace").strip()
    if text.startswith("```"):
        text = text.strip("`").split("\n", 1)[-1]
    start, end = text.find("{"), text.rfind("}")
    try:
        return json.loads(text[start:end + 1])
    except ValueError:
        raise SelfCouncilError("BAD_JSON", f"{name} holds no JSON object") from None


def evidence_ok(ev: str, root: Path) -> bool:
    path = re.split(r"[:#]", ev.strip(), maxsplit=1)[0].strip().strip("`")
    if not path or path.startswith(("/", "~")) or ".." in Path(path).parts or re.match(r"^[A-Za-z]:\\", path):
        return False
    return (root / path).exists()


def check_review(rev: dict, persona: dict, batch: list, root: Path) -> list:
    probs = []
    if not str(rev.get("summary", "")).strip():
        probs.append("missing 'summary'")
    f = rev.get(persona["field"])
    pid = persona["id"]
    if not isinstance(f, dict):
        probs.append(f"missing '{persona['field']}' object")
    elif pid == "P1" and (f.get("status") not in ("covered", "partial", "none") or not str(f.get("ran", "")).strip()):
        probs.append("test_verdict needs status covered|partial|none and 'ran'")
    elif pid == "P2" and (not isinstance(f.get("clarity"), int) or isinstance(f.get("clarity"), bool)
                          or not 1 <= f["clarity"] <= 5 or not str(f.get("would_say", "")).strip()):
        probs.append("first_minute needs clarity 1–5 (integer) and 'would_say'")
    elif pid == "P3" and (f.get("decision") not in ("keep", "merge", "rewrite", "delete") or not str(f.get("why", "")).strip()):
        probs.append("keep_or_kill needs decision keep|merge|rewrite|delete and 'why'")
    elif pid == "P4" and not (isinstance(f.get("overlaps"), list) and isinstance(f.get("should_call"), list)):
        probs.append("wiring needs 'overlaps' and 'should_call' lists")
    elif pid == "P5" and (not str(f.get("idea", "")).strip() or not str(f.get("first_step", "")).strip()):
        probs.append("ten_x needs 'idea' and 'first_step'")
    fs = rev.get("findings")
    if not isinstance(fs, list):
        return probs + ["'findings' must be a list"]
    if not fs and not str(rev.get("no_findings_reason", "")).strip():
        probs.append("empty 'findings' needs 'no_findings_reason'")
    if len(fs) > MAX_FINDINGS:
        probs.append(f"at most {MAX_FINDINGS} findings")
    for i, x in enumerate(fs):
        if not isinstance(x, dict):
            probs.append(f"findings[{i}] is not an object"); continue
        for k in ("title", "proposed_change", "evidence"):
            if not str(x.get(k, "")).strip():
                probs.append(f"findings[{i}] needs '{k}'")
        if x.get("severity") not in SEVERITY:
            probs.append(f"findings[{i}].severity must be one of {', '.join(SEVERITY)}")
        if x.get("effort") not in EFFORT:
            probs.append(f"findings[{i}].effort must be S, M or L")
        if x.get("category") not in CATEGORIES:
            probs.append(f"findings[{i}].category must be one of {', '.join(CATEGORIES)}")
        c = x.get("confidence")
        if not isinstance(c, (int, float)) or isinstance(c, bool) or not 0 <= c <= 1:
            probs.append(f"findings[{i}].confidence must be a number from 0 to 1")
        if str(x.get("evidence", "")).strip() and not evidence_ok(str(x["evidence"]), root):
            probs.append(f"findings[{i}].evidence {str(x['evidence'])[:60]!r} is not an existing repository-relative path")
    return probs


def cmd_ingest(a) -> dict:
    root = Path(a.root)
    d = Path(a.dir)
    run = load(d / "run.json")
    pid = a.persona.upper()
    persona = next((p for p in PERSONAS if p["id"] == pid), None)
    if persona is None:
        raise SelfCouncilError("UNKNOWN_PERSONA", f"{a.persona} is not one of {', '.join(PERSONA_IDS)}")
    raw = Path(a.file).read_bytes()
    obj = parse_json_text(raw, Path(a.file).name)
    if not isinstance(obj, dict):
        raise SelfCouncilError("BAD_JSON", "the answer must be a JSON object")
    found = _secrets.scan_object(obj)
    if found:
        raise SelfCouncilError("SECRET", f"likely credentials at {', '.join(p for p, _ in found[:3])}")
    if obj.get("persona") and str(obj["persona"]).upper() != pid:
        raise SelfCouncilError("PERSONA_MISMATCH", f"the file says persona {obj['persona']}, not {pid}")
    revs = obj.get("reviews")
    if not isinstance(revs, list) or not revs:
        raise SelfCouncilError("REVIEW_INVALID", "'reviews' must be a non-empty list")
    probs, seen = [], set()
    for i, r in enumerate(revs):
        if not isinstance(r, dict):
            probs.append(f"reviews[{i}] is not an object"); continue
        uid = r.get("unit")
        if uid not in run["batch"]:
            probs.append(f"reviews[{i}].unit {uid!r} is not in this batch"); continue
        if uid in seen:
            probs.append(f"{uid} is reviewed twice"); continue
        seen.add(uid)
        probs += [f"{uid}: {p}" for p in check_review(r, persona, run["batch"], root)]
    if probs:
        raise SelfCouncilError("REVIEW_INVALID", f"{pid}: " + "; ".join(probs[:12]) + (f" (+{len(probs) - 12} more)" if len(probs) > 12 else ""))
    receipt = {"sha256": sha256_bytes(raw), "simulated": bool(a.simulated), "ingested_at": now_iso()}
    replaced = []
    for r in revs:
        if r["unit"] in run["reviews"][pid]:
            replaced.append(r["unit"])
        run["reviews"][pid][r["unit"]] = dict(r, _receipt=receipt)
    save(d / "run.json", run)
    save(d / "reviews" / f"{pid}.json", run["reviews"][pid])
    have = len(run["reviews"][pid])
    return {"persona": pid, "units": sorted(seen), "replaced": replaced, "have": have, "of": len(run["batch"]),
            "simulated": bool(a.simulated)}


# ------------------------------------------------------------------ report

_STOP = {"the", "and", "for", "with", "that", "this", "from", "into", "add", "its", "are", "not", "use", "one", "when",
         "في", "من", "على", "إلى", "الى", "عن", "مع", "أو", "او", "لا", "ما", "هذا", "هذه", "التي", "الذي"}


def tokens(text: str) -> set:
    return {t for t in re.findall(r"[\w]{3,}", text.lower()) if t not in _STOP and not t.isdigit()}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


def ev_file(ev: str) -> str:
    return re.split(r"[:#]", ev.strip(), maxsplit=1)[0].strip().strip("`")


def cluster(findings: list) -> list:
    """Greedy, deterministic dedupe of one unit's findings: similar wording, or the same file and category with some overlap."""
    order = sorted(findings, key=lambda f: (-SEVERITY[f["severity"]], -f["confidence"], f["persona"], f["title"]))
    groups = []
    for f in order:
        tk, tt = tokens(f["title"] + " " + f["proposed_change"]), tokens(f["title"])
        for g in groups:
            j, same_cat = jaccard(tk, g["tokens"]), f["category"] == g["category"]
            if (j >= 0.4 or (same_cat and jaccard(tt, g["title_tokens"]) >= 0.4)
                    or (same_cat and ev_file(f["evidence"]) in g["files"] and j >= 0.2)):
                g["members"].append(f); g["tokens"] |= tk; g["title_tokens"] |= tt; g["files"].add(ev_file(f["evidence"]))
                break
        else:
            groups.append({"members": [f], "tokens": set(tk), "title_tokens": set(tt), "files": {ev_file(f["evidence"])},
                           "category": f["category"]})
    return groups


def proposal_of(unit: str, g: dict) -> dict:
    ms = g["members"]
    rep = ms[0]
    personas = sorted({m["persona"] for m in ms})
    efforts = [m["effort"] for m in ms]
    effort = max(set(efforts), key=lambda e: (efforts.count(e), EFFORT[e]))  # most often stated; a tie takes the larger
    sev = rep["severity"]
    conf = round(sum(m["confidence"] for m in ms) / len(ms), 2)
    score = round(SEVERITY[sev] * conf * (1 + 0.5 * (len(personas) - 1)) / EFFORT[effort], 2)
    return {"unit": unit, "title": rep["title"], "proposed_change": rep["proposed_change"], "category": rep["category"],
            "severity": sev, "effort": effort, "confidence": conf, "personas": personas, "agree": len(personas),
            "evidence": sorted({m["evidence"] for m in ms}), "score": score,
            "also": [m["proposed_change"] for m in ms[1:] if m["proposed_change"] != rep["proposed_change"]][:3]}


def merge_across_units(proposals: list) -> list:
    """One proposal that several units share word for word (e.g. one CI step for two scripts) is listed once with all its units."""
    out, seen = [], {}
    for x in sorted(proposals, key=lambda x: (-x["score"], x["unit"], x["title"])):
        k = (" ".join(sorted(tokens(x["title"]))), " ".join(sorted(tokens(x["proposed_change"]))))
        if k in seen:
            y = seen[k]
            y["units"].append(x["unit"])
            y["personas"] = sorted(set(y["personas"]) | set(x["personas"]))
            y["evidence"] = sorted(set(y["evidence"]) | set(x["evidence"]))
            continue
        x = dict(x, units=[x["unit"]])
        seen[k] = x
        out.append(x)
    return out


def coverage(units: list, led: dict, root: Path) -> dict:
    open_ = open_runs(led, root)
    st = {u["id"]: unit_state(u, led, open_) for u in units}
    by_kind = {}
    for k in KINDS:
        ks = [u for u in units if u["kind"] == k]
        if ks:
            by_kind[k] = {"total": len(ks), "reviewed": sum(1 for u in ks if st[u["id"]] in ("fresh", "stale"))}
    reviewed = sum(1 for v in st.values() if v in ("fresh", "stale"))
    return {"total": len(units), "reviewed": reviewed, "fresh": sum(1 for v in st.values() if v == "fresh"),
            "stale": sum(1 for v in st.values() if v == "stale"), "claimed": sum(1 for v in st.values() if v == "claimed"),
            "never": sum(1 for v in st.values() if v == "never"), "pending": sum(1 for v in st.values() if v == "pending"),
            "percent": round(100.0 * reviewed / len(units), 1) if units else 0.0, "by_kind": by_kind,
            "simulated_reviews": sum(1 for e in led["units"].values() if e.get("state") == "reviewed" and e.get("simulated"))}


def cmd_report(a) -> dict:
    root = Path(a.root)
    d = Path(a.dir)
    run = load(d / "run.json")
    batch = run["batch"]
    missing = [f"{p}:{u}" for p in PERSONA_IDS for u in batch if u not in run["reviews"][p]]
    if missing and not a.partial:
        raise SelfCouncilError("INCOMPLETE", f"{len(missing)} persona reviews missing, e.g. {', '.join(missing[:5])} (or pass --partial)")
    simulated = any(r.get("_receipt", {}).get("simulated") for p in PERSONA_IDS for r in run["reviews"][p].values())
    per_unit, proposals = {}, []
    for uid in batch:
        found = []
        voices = {}
        for p in PERSONAS:
            r = run["reviews"][p["id"]].get(uid)
            if not r:
                continue
            voices[p["id"]] = {"summary": r["summary"], p["field"]: r.get(p["field"]),
                               "simulated": bool(r.get("_receipt", {}).get("simulated"))}
            found += [dict(f, persona=p["id"]) for f in r["findings"]]
        props = sorted((proposal_of(uid, g) for g in cluster(found)), key=lambda x: (-x["score"], -x["agree"], x["title"]))
        proposals += props
        per_unit[uid] = {"personas": sorted(voices), "complete": len(voices) == len(PERSONAS), "voices": voices,
                         "findings": len(found), "proposals": len(props),
                         "keep_or_kill": (voices.get("P3") or {}).get("keep_or_kill"),
                         "clarity": ((voices.get("P2") or {}).get("first_minute") or {}).get("clarity")}
    proposals = merge_across_units(proposals)
    proposals.sort(key=lambda x: (-x["score"], -x["agree"], -SEVERITY[x["severity"]], x["unit"], x["title"]))
    for i, x in enumerate(proposals, 1):
        x["rank"] = i
    top = proposals[:a.top]
    status = "SELF_COUNCIL_SIMULATED" if simulated else ("SELF_COUNCIL_PARTIAL" if missing else "SELF_COUNCIL_RUN")
    if simulated and missing:
        status += "+PARTIAL"
    # ledger: complete units become reviewed (with the content hash they were reviewed at); the run releases its claims
    lp = Path(a.ledger) if a.ledger else root / run.get("ledger", LEDGER_REL.as_posix())
    led = load_ledger(lp)
    key = run_key(d, root)
    now = now_iso()
    for uid in batch:
        e = led["units"].setdefault(uid, {"history": []})
        sim = any(run["reviews"][p].get(uid, {}).get("_receipt", {}).get("simulated") for p in PERSONA_IDS)
        state = "reviewed" if per_unit[uid]["complete"] else "partial"
        e.update({"state": state, "run": key, "personas": len(per_unit[uid]["personas"]), "simulated": sim})
        if state == "reviewed":
            e.update({"reviewed_at": now, "sha256": run["units"][uid]["sha256"]})
        e.setdefault("history", []).append({"run": key, "state": state, "at": now, "simulated": sim})
        e["history"] = e["history"][-10:]
    led["runs"].setdefault(key, {"created_at": run["created_at"], "units": batch})["reported_at"] = now
    led["updated_at"] = now
    save(lp, led)
    cov = coverage(inventory(root), led, root)
    receipt = sha256_bytes(json.dumps(run["reviews"], ensure_ascii=False, sort_keys=True).encode("utf-8"))
    rep = {"schema": REPORT_SCHEMA, "status": status, "created_at": now, "run": key, "batch": batch,
           "missing": missing, "units": per_unit, "proposals": proposals, "implement_next": top, "coverage": cov,
           "reviews_sha256": receipt,
           "note": ("SIMULATED: the five personas were written in one Claude context, not run as separate agents"
                    if simulated else "five personas ran as separate agents")}
    md = render_md(rep, run)
    save(d / "report.json", rep)
    (d / "report.md").write_text(md, encoding="utf-8")
    out = {"status": status, "units": len(batch), "proposals": len(proposals), "coverage": f"{cov['reviewed']}/{cov['total']} ({cov['percent']}%)",
           "report": [str(d / "report.md"), str(d / "report.json")],
           "top": [f"#{x['rank']} {'+'.join(x['units'])} [{x['severity']}/{x['effort']}, {x['agree']}p, {x['score']}] {x['title']}" for x in top]}
    if a.out_md:
        Path(a.out_md).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out_md).write_text(md, encoding="utf-8"); out["report"].append(a.out_md)
    if a.out_json:
        save(Path(a.out_json), rep); out["report"].append(a.out_json)
    return out


def _cell(s) -> str:
    return str(s if s is not None else "—").replace("|", "\\|").replace("\n", " ")


def render_md(rep: dict, run: dict) -> str:
    cov = rep["coverage"]
    L = [f"# مجلس المراجعة الذاتية — Self-Council report", "",
         f"**الحالة:** {rep['status']} · **الوحدات:** {len(rep['batch'])} · **المقترحات:** {len(rep['proposals'])} · "
         f"**التغطية:** {cov['reviewed']}/{cov['total']} ({cov['percent']}%) · **الإيصال:** `{rep['reviews_sha256'][:16]}`", ""]
    if "SIMULATED" in rep["status"]:
        L += ["> **SIMULATED:** الشخصيات الخمس كتبها Claude في سياق واحد، لا وكلاء منفصلون. الأدلة مسارات حقيقية فُتحت، "
              "لكن الآراء ليست مستقلة؛ أعد التشغيل بوكلاء متوازين قبل قرار كبير.", ""]
    L += ["## نفّذ التالي / implement next", "",
          "| # | الوحدة | المقترح | الشدة/الجهد | يتفق | الدرجة | الدليل |", "|---|---|---|---|---|---|---|"]
    for x in rep["implement_next"]:
        L.append(f"| {x['rank']} | " + ", ".join(f"`{u}`" for u in x.get("units", [x["unit"]])) + f" | **{_cell(x['title'])}** — {_cell(x['proposed_change'])} | {x['severity']}/{x['effort']} | "
                 f"{x['agree']} ({','.join(x['personas'])}) | {x['score']} | {_cell(', '.join('`' + e + '`' for e in x['evidence'][:2]))} |")
    L += ["", "الدرجة = وزن الشدة × متوسط الثقة × (1 + 0.5 لكل شخصية إضافية تتفق) ÷ الجهد (S=1، M=2، L=4).", "",
          "## الوحدات / units", "", "| الوحدة | الأسباب | الشخصيات | الوضوح (P2) | يبقى/يُدمج (P3) | المقترحات |", "|---|---|---|---|---|---|"]
    for uid in rep["batch"]:
        u, pu = run["units"][uid], rep["units"][uid]
        kk = pu.get("keep_or_kill") or {}
        L.append(f"| `{uid}` | {_cell(', '.join(u['reasons']) or '—')} | {len(pu['personas'])}/5 | {_cell(pu.get('clarity'))} | "
                 f"{_cell(kk.get('decision'))}: {_cell(kk.get('why'))} | {pu['proposals']} |")
    L += ["", "## أصوات الشخصيات / voices", ""]
    names = {p["id"]: f"{p['id']} {p['name_ar']}" for p in PERSONAS}
    for uid in rep["batch"]:
        L.append(f"### `{uid}`")
        for pid, v in sorted(rep["units"][uid]["voices"].items()):
            fld = next(p["field"] for p in PERSONAS if p["id"] == pid)
            L.append(f"- **{names[pid]}:** {_cell(v['summary'])} · `{fld}` {_cell(json.dumps(v.get(fld), ensure_ascii=False))}")
        L.append("")
    L += ["## كل المقترحات / all proposals", "", "| # | الوحدة | المقترح | الفئة | الشدة/الجهد | يتفق | الدرجة |", "|---|---|---|---|---|---|---|"]
    for x in rep["proposals"]:
        L.append(f"| {x['rank']} | " + ", ".join(f"`{u}`" for u in x.get("units", [x["unit"]])) + f" | {_cell(x['title'])} | {x['category']} | {x['severity']}/{x['effort']} | {x['agree']} | {x['score']} |")
    bk = " · ".join(f"{k} {v['reviewed']}/{v['total']}" for k, v in cov["by_kind"].items())
    L += ["", "## التغطية / coverage", "",
          f"راجع المجلس {cov['reviewed']} من {cov['total']} وحدة ({cov['percent']}%): {bk}. لم تُراجع بعد {cov['never'] + cov['pending']}، "
          f"وتغيّرت بعد مراجعتها {cov['stale']}، ومحجوزة لتشغيل مفتوح {cov['claimed']}. الدفعة التالية: "
          "`python3 .claude/skills/kosif-superpowers/scripts/self_council.py plan --batch 10 --dir out/self-council/<run>`."]
    if rep["missing"]:
        L += ["", f"**ناقص:** {len(rep['missing'])} مراجعة: " + ", ".join(rep["missing"][:10])]
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ status / personas

def cmd_status(a) -> dict:
    root = Path(a.root)
    units = inventory(root)
    led = load_ledger(ledger_path(a))
    cov = coverage(units, led, root)
    open_ = open_runs(led, root)
    nxt = sorted((u for u in units if unit_state(u, led, open_) in ("never", "pending", "stale")),
                 key=lambda u: ({"never": 0, "pending": 0, "stale": 1}[unit_state(u, led, open_)],) + rank_key(u))
    return {"coverage": cov, "open_runs": sorted(open_), "ledger": str(ledger_path(a)),
            "next": [f"{u['id']} w={u['weakness']} {','.join(u['reasons'])}" for u in nxt[:5]]}


def cmd_personas(a) -> dict:
    return {"personas": [{"id": p["id"], "name": f"{p['name_ar']} — {p['en']}", "lens": p["lens"], "stance": p["stance"],
                          "checklist": list(p["checklist"]), "required_field": f"{p['field']}: {p['field_doc']}"} for p in PERSONAS],
            "finding_schema": {"title": "str", "category": "|".join(CATEGORIES), "severity": "|".join(SEVERITY),
                               "evidence": "repository-relative path that exists[:line]", "proposed_change": "str",
                               "effort": "S|M|L", "confidence": "0..1"}}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", default=str(DEFAULT_ROOT), help="repository root (default: this checkout)")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("inventory", help="list every reviewable unit with static signals")
    s.add_argument("--kind", choices=KINDS); s.add_argument("--summary", action="store_true"); s.add_argument("--out")
    s = sub.add_parser("plan", help="pick the next batch of weakest unreviewed units and write the five persona prompts")
    s.add_argument("--batch", type=int, default=10); s.add_argument("--dir", required=True); s.add_argument("--kind", choices=KINDS)
    s.add_argument("--revisit", action="store_true", help="when nothing is left, re-review the units reviewed longest ago")
    s.add_argument("--force", action="store_true"); s.add_argument("--ledger")
    s = sub.add_parser("ingest", help="validate and record one persona's review")
    s.add_argument("--dir", required=True); s.add_argument("--persona", required=True); s.add_argument("--file", required=True)
    s.add_argument("--simulated", action="store_true", help="the review was written in Claude's own context, not by a separate agent")
    s = sub.add_parser("report", help="merge the five reviews, rank the proposals and update the ledger")
    s.add_argument("--dir", required=True); s.add_argument("--top", type=int, default=10); s.add_argument("--partial", action="store_true")
    s.add_argument("--out-md"); s.add_argument("--out-json"); s.add_argument("--ledger")
    s = sub.add_parser("status", help="coverage of the whole app")
    s.add_argument("--ledger")
    sub.add_parser("personas", help="show the five personas, their checklists and the review schema")
    a = p.parse_args(argv)
    for k in ("root",):
        setattr(a, k, str(Path(getattr(a, k)).resolve()))
    try:
        res = {"inventory": cmd_inventory, "plan": cmd_plan, "ingest": cmd_ingest, "report": cmd_report,
               "status": cmd_status, "personas": cmd_personas}[a.cmd](a)
    except _secrets.SecretError as exc:
        print(f"self_council: error: SECRET: {exc}", file=sys.stderr)
        return 2
    except SelfCouncilError as exc:
        print(f"self_council: error: {exc.code}: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"self_council: error: IO: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
