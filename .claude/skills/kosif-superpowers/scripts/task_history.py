#!/usr/bin/env python3
"""Task history: one record per finished task, so a later chat can list them and repeat one / سجل المهام.

After an assistant that follows USIP finishes a task (a video, an image, code, a document...) it writes one JSON
record under history/tasks/ at the repository root: what was asked, the mode and plan, the tools with the exact
commands and parameters, the inputs and outputs (with sha256 when the file was at hand), and how to reproduce it.
Later the user asks "what tasks have you done?" (list), picks one (show) and says "repeat it" (replay), and the new
outputs can be checked against the recorded ones (compare). Annex A35 of the protocol says when to do each.

    python3 scripts/task_history.py new --kind video > entry.json        # a template to fill
    python3 scripts/task_history.py add --from entry.json                 # validate, hash outputs, write, rebuild the index
    python3 scripts/task_history.py add --from entry.json --print         # write nothing: the record, a one-line save
                                                                          # command and a GitHub "new file" link
    python3 scripts/task_history.py list [--kind video] [--q "دعاء"] [--json]
    python3 scripts/task_history.py show <id | unique prefix | number from list | last>
    python3 scripts/task_history.py replay <ref> [--format md|sh|json] [--out FILE]
    python3 scripts/task_history.py compare <ref> [--dir DIR]
    python3 scripts/task_history.py build [--check]                       # history/INDEX.md + history/index.json
    python3 scripts/task_history.py validate [--strict]

The history lives on main, which is public, so a record is refused when it holds a credential, a session or
scratchpad path, an e-mail address or a phone number. replay only prints a plan or a script; it never runs a command,
and a step marked needs_permission stays commented out until the user allows it. Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import re
import shlex
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import _secrets
except ImportError:  # the skill copied without its helpers: fall back to the leak and personal-data checks only
    _secrets = None

SCHEMA = "kosif.task-history.v1"
REPO = Path(__file__).resolve().parents[4]
HISTORY = REPO / "history"
DEFAULT_REPO = "kosif199022-jpg/kosif-tool"
SELF = ".claude/skills/kosif-superpowers/scripts/task_history.py"
MAX_BYTES = 64 * 1024

KINDS = ("video", "image", "audio", "motion", "3d", "code", "document", "data", "design", "web", "other")
STATUSES = ("PLAN_ONLY", "BLOCKED", "EXECUTED_UNVERIFIED", "PARTIALLY_VERIFIED", "DONE_VERIFIED")
LEVELS = ("L0", "L1", "L2", "L3")
REQUIRED = ("schema", "id", "date", "title", "request", "kind", "mode", "steps", "outputs", "reproduce")
OPTIONAL = ("level", "plan", "status", "agent", "language", "tags", "tools", "params", "inputs", "evidence",
            "fuse_id", "branch", "commit", "pr", "lessons", "notes")
STEP_KEYS = ("n", "what", "tool", "command", "params", "manual", "needs_permission", "cwd", "output")
FILE_KEYS = ("name", "path", "url", "kind", "sha256", "bytes", "deterministic", "measured", "note")

ID_RE = re.compile(r"^\d{8}-[a-z0-9][a-z0-9-]{0,60}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
LEAK_RE = re.compile(r"/tmp/claude-\d+/|scratchpad/|session_[0-9A-Za-z]{20,}|/root/\.claude/|/mnt/project-files/uploads/")
EMAIL_RE = re.compile(r"(?<![\w.%+-])(?!git@|noreply@|no-reply@)[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]*[A-Za-z]")
PHONE_RE = re.compile(r"(?<![\w.:/-])\+?\d[\d \-]{9,}\d(?![\w.])")
IBAN_RE = re.compile(r"\b(?:[Ss][Aa][0-9]{22}|[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30})\b")
PLACEHOLDER_RE = re.compile(r"^<[^<>]* [^<>]*>$")
ABS_RE = re.compile(r"(?<![\w.:])(?:/home/|/Users/|/mnt/|/tmp/|[A-Za-z]:\\)")


# ---------------------------------------------------------------- paths and loading

def tasks_dir(root: Path) -> Path:
    return root / "tasks"


def load_all(root: Path):
    """[(path, record or None, error)] for every history/tasks/*.json, newest id first."""
    out = []
    d = tasks_dir(root)
    for p in sorted(d.glob("*.json"), reverse=True) if d.is_dir() else []:
        try:
            out.append((p, json.loads(p.read_text(encoding="utf-8")), None))
        except (OSError, ValueError) as e:
            out.append((p, None, f"unreadable JSON: {e}"))
    return out


def records(root: Path):
    return [r for _p, r, err in load_all(root) if r is not None and not err]


def resolve(root: Path, ref: str) -> dict:
    """A record by exact id, unique id prefix or substring, 'last', or its 1-based number in `list` (newest first)."""
    recs = records(root)
    if not recs:
        raise SystemExit(f"no task history yet under {root}/tasks")
    ref = (ref or "").strip()
    if ref.lower() in ("last", "latest", "آخر", "الأخيرة"):
        return recs[0]
    if ref.isdigit() and 1 <= int(ref) <= len(recs) and len(ref) < 8:
        return recs[int(ref) - 1]
    for test in (lambda i: i == ref, lambda i: i.startswith(ref), lambda i: ref in i):
        hits = [r for r in recs if test(str(r.get("id", "")))]
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            raise SystemExit(f"'{ref}' matches {len(hits)} tasks: " + ", ".join(r["id"] for r in hits[:8]))
    raise SystemExit(f"no task matches '{ref}'; run: python3 {SELF} list")


# ---------------------------------------------------------------- validation

def _strings(obj, path="$"):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield f"{path}.{k}", str(k)
            yield from _strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _strings(v, f"{path}[{i}]")


def privacy_problems(rec) -> tuple:
    """(errors, warnings): what must never reach a public main, and what only hurts reproducibility."""
    errors, warnings = [], []
    if _secrets is not None:
        for where, kinds in _secrets.scan_object(rec):
            errors.append(f"{where}: looks like a credential ({', '.join(kinds)}); describe it as <KEY_NAME> instead")
    for where, s in _strings(rec):
        if LEAK_RE.search(s):
            errors.append(f"{where}: a session, scratchpad or upload path; use a repo-relative path or a public URL")
        if EMAIL_RE.search(s):
            errors.append(f"{where}: an e-mail address (personal data on a public branch)")
        if PHONE_RE.search(s):
            errors.append(f"{where}: a phone number (personal data on a public branch)")
        if IBAN_RE.search(s):
            errors.append(f"{where}: an IBAN/bank account number (financial data on a public branch)")
        if not PHONE_RE.search(s) and ABS_RE.search(s):
            warnings.append(f"{where}: an absolute local path; another machine cannot reproduce it, prefer a repo path")
    return errors, warnings


def _check_files(items, field, errors):
    if not isinstance(items, list):
        errors.append(f"{field} must be a list")
        return
    for i, f in enumerate(items):
        w = f"{field}[{i}]"
        if not isinstance(f, dict):
            errors.append(f"{w} must be an object")
            continue
        unknown = set(f) - set(FILE_KEYS)
        if unknown:
            errors.append(f"{w}: unknown keys {sorted(unknown)}")
        if not (f.get("path") or f.get("url") or f.get("name")):
            errors.append(f"{w}: needs a path, a url or a name")
        if "sha256" in f and not SHA_RE.match(str(f["sha256"])):
            errors.append(f"{w}.sha256 must be 64 lowercase hex characters")
        if "bytes" in f and (not isinstance(f["bytes"], int) or f["bytes"] < 0):
            errors.append(f"{w}.bytes must be a non-negative integer")


def validate_record(rec, filename: str | None = None) -> tuple:
    """(errors, warnings) for one record."""
    errors, warnings = [], []
    if not isinstance(rec, dict):
        return ["the record must be a JSON object"], []
    for k in REQUIRED:
        if k not in rec or rec[k] in ("", [], {}, None):
            errors.append(f"missing required field '{k}'")
    unknown = set(rec) - set(REQUIRED) - set(OPTIONAL)
    if unknown:
        errors.append(f"unknown fields {sorted(unknown)} (allowed extras: {', '.join(OPTIONAL)})")
    if rec.get("schema") not in (None, SCHEMA):
        errors.append(f"schema must be {SCHEMA}")
    rid = str(rec.get("id", ""))
    if rid and not ID_RE.match(rid):
        errors.append("id must look like YYYYMMDD-short-name (lowercase ASCII, digits and hyphens)")
    if filename and rid and filename != f"{rid}.json":
        errors.append(f"file name {filename} must be {rid}.json")
    date = str(rec.get("date", ""))
    if date and not DATE_RE.match(date):
        errors.append("date must be YYYY-MM-DD")
    elif date and rid[:8].isdigit() and rid[:8] != date.replace("-", ""):
        warnings.append("the id's date differs from date")
    for key, allowed in (("kind", KINDS), ("status", STATUSES), ("level", LEVELS)):
        if key in rec and rec[key] not in allowed:
            errors.append(f"{key} must be one of {', '.join(allowed)}")
    steps = rec.get("steps")
    if isinstance(steps, list):
        for i, s in enumerate(steps):
            w = f"steps[{i}]"
            if not isinstance(s, dict):
                errors.append(f"{w} must be an object")
                continue
            unknown = set(s) - set(STEP_KEYS)
            if unknown:
                errors.append(f"{w}: unknown keys {sorted(unknown)}")
            if not s.get("what"):
                errors.append(f"{w}: 'what' says what the step did")
            if not (s.get("command") or s.get("tool") or s.get("manual")):
                errors.append(f"{w}: needs a command, a tool or a manual description so it can be repeated")
    elif steps is not None:
        errors.append("steps must be a list")
    for field in ("inputs", "outputs"):
        if field in rec:
            _check_files(rec[field], field, errors)
    rep = rec.get("reproduce")
    if rep is not None and not (isinstance(rep, dict) and rep.get("how")):
        errors.append("reproduce must be an object with 'how' (prerequisites and commands are optional lists)")
    elif isinstance(rep, dict):
        for k in ("prerequisites", "commands"):
            if k in rep and not isinstance(rep[k], list):
                errors.append(f"reproduce.{k} must be a list")
    holes = sorted({w for w, v in _strings(rec) if PLACEHOLDER_RE.match(v)})
    if holes:
        errors.append(f"template placeholders left unfilled at {', '.join(holes[:6])}")
    if len(json.dumps(rec, ensure_ascii=False).encode("utf-8")) > MAX_BYTES:
        errors.append(f"the record is larger than {MAX_BYTES // 1024} KB; link long logs as evidence files instead")
    e2, w2 = privacy_problems(rec)
    return errors + e2, warnings + w2


# ---------------------------------------------------------------- building records

def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:40].strip("-") or "task"


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fill_hashes(rec: dict, base: Path) -> list:
    """Adds sha256 and bytes to every input/output whose path is a local file; returns the paths it hashed."""
    done = []
    for field in ("inputs", "outputs"):
        for f in rec.get(field) or []:
            if not isinstance(f, dict) or not f.get("path") or "sha256" in f:
                continue
            p = Path(f["path"])
            p = p if p.is_absolute() else base / p
            if p.is_file():
                f["sha256"], f["bytes"] = sha256_of(p), p.stat().st_size
                done.append(f["path"])
    return done


def normalise(rec: dict, root: Path, today: str | None = None) -> dict:
    """Fills schema, date and a free id (date-slug, -2, -3...) and orders the keys."""
    rec = dict(rec)
    rec["schema"] = SCHEMA
    rec.setdefault("date", today or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"))
    if not rec.get("id"):
        stem = f"{str(rec['date']).replace('-', '')}-{slugify(rec.get('slug_hint') or rec.get('title', ''))}"
        rid, n = stem, 2
        while (tasks_dir(root) / f"{rid}.json").exists():
            rid, n = f"{stem}-{n}", n + 1
        rec["id"] = rid
    rec.pop("slug_hint", None)
    rec["steps"] = [{"n": s.get("n", i), **{k: v for k, v in s.items() if k != "n"}} if isinstance(s, dict) else s
                    for i, s in enumerate(rec.get("steps") or [], 1)]
    order = {k: i for i, k in enumerate(REQUIRED[:6] + ("level", "plan", "status") + REQUIRED[6:] + OPTIONAL)}
    return {k: rec[k] for k in sorted(rec, key=lambda k: order.get(k, 999))}


def dumps(rec) -> str:
    return json.dumps(rec, ensure_ascii=False, indent=2) + "\n"


def template(kind: str) -> dict:
    return {
        "title": "<short name, e.g. Friday dua reel 23-10>",
        "request": "<the user's request in their own words>",
        "kind": kind,
        "mode": "<the reply that started it: موافق / A / B / C / D / نفّذ مباشرة / كمّل بدوني ...>",
        "level": "L2", "plan": "B", "status": "DONE_VERIFIED",
        "agent": "<the assistant and environment, e.g. Claude Code cloud session>",
        "tools": ["<tool id or program, e.g. montage-pro, ffmpeg 6.1>"],
        "params": {"<param name>": "<value: fps, size, seed, style id, voice, model setting...>"},
        "inputs": [{"name": "<input file name>", "path": "<repo path>", "url": "<or a public link>", "kind": "audio"}],
        "steps": [{"what": "<what this step did>", "tool": "<tool id>",
                   "command": "<the exact command, with every flag>", "params": {}}],
        "outputs": [{"path": "<repo path of the result>", "kind": kind, "deterministic": False,
                     "measured": {"duration_s": 0, "fps": 0}}],
        "reproduce": {"how": "<one paragraph: what to run, in what order, and what will differ>",
                      "prerequisites": ["<installs, keys by name only, fonts>"], "commands": []},
        "evidence": ["<test report or QA file in the repo>"],
        "lessons": ["<what to do differently next time>"],
    }


# ---------------------------------------------------------------- index

def summary(rec: dict) -> dict:
    return {k: rec.get(k) for k in ("id", "date", "kind", "mode", "plan", "status", "title")
            if rec.get(k) not in (None, "")}


def _cell(s) -> str:
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ")


def render_index(recs) -> tuple:
    rows = [summary(r) for r in recs]
    data = json.dumps({"schema": "kosif.task-history-index.v1", "count": len(rows), "tasks": rows},
                      ensure_ascii=False, indent=1) + "\n"
    lines = [
        "# سجل المهام / Task history", "",
        "<!-- generated by task_history.py build; edit the records under tasks/, not this page -->", "",
        f"**{len(rows)}** مهمة مسجّلة، الأحدث أولًا. اطلب «كرر المهمة <المعرّف>» أو «كرر رقم N»، "
        f"أو شغّل `python3 {SELF} replay <id>`. القواعد في "
        "[A35](../.claude/skills/kosif-superpowers/references/protocol/A35-task-history.md).", "",
        f"**{len(rows)}** recorded tasks, newest first. Ask \"repeat task <id>\" or run `replay <id>`.", "",
        "| # | id | date | kind | mode | status | title |", "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | [{r['id']}](tasks/{r['id']}.json) | {_cell(r.get('date'))} | {_cell(r.get('kind'))} | "
                     f"{_cell(r.get('mode'))} | {_cell(r.get('status'))} | {_cell(r.get('title'))} |")
    return "\n".join(lines) + "\n", data


def build(root: Path, check: bool = False) -> int:
    md, data = render_index(records(root))
    targets = ((root / "INDEX.md", md), (root / "index.json", data))
    stale = [p.name for p, text in targets if not p.is_file() or p.read_text(encoding="utf-8") != text]
    if check:
        print("history index: " + ("stale: " + ", ".join(stale) if stale else "current"))
        return 1 if stale else 0
    root.mkdir(parents=True, exist_ok=True)
    for p, text in targets:
        if p.name in stale:
            p.write_text(text, encoding="utf-8")
    print(f"history index: {len(records(root))} tasks" + (f", wrote {', '.join(stale)}" if stale else ", unchanged"))
    return 0


# ---------------------------------------------------------------- output helpers

def save_hints(rec: dict, repo: str) -> str:
    """How to save a record from a chat app that cannot push: a one-line shell command and a GitHub link."""
    text = dumps(rec)
    b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
    rid = rec["id"]
    one_line = (f"echo {b64} | base64 -d | python3 {SELF} add --from - && git add history && "
                f"git commit -m 'history: {rid}' && git push")
    link = (f"https://github.com/{repo}/new/main/history/tasks?filename={urllib.parse.quote(rid + '.json')}"
            f"&value={urllib.parse.quote(text)}")
    parts = [
        f"FILE: history/tasks/{rid}.json", "", "```json", text.rstrip("\n"), "```", "",
        "ONE-LINE SAVE (repo root, with git):", one_line, "",
    ]
    if len(link) <= 8000:
        parts += ["GITHUB LINK (opens a pre-filled new file on main; press Commit):", link]
    else:
        parts += ["GITHUB: the record is too long for a pre-filled link; open "
                  f"https://github.com/{repo}/new/main/history/tasks and paste the JSON above as {rid}.json"]
    return "\n".join(parts)


def show_md(rec: dict) -> str:
    out = [f"# {rec.get('title')}  ({rec.get('id')})", "",
           f"- date: {rec.get('date')} · kind: {rec.get('kind')} · mode: {rec.get('mode')}"
           + "".join(f" · {k}: {rec[k]}" for k in ("level", "plan", "status") if rec.get(k)),
           f"- request: {rec.get('request')}"]
    for k in ("agent", "fuse_id", "branch", "commit", "pr"):
        if rec.get(k):
            out.append(f"- {k}: {rec[k]}")
    if rec.get("tools"):
        out.append("- tools: " + ", ".join(map(str, rec["tools"])))
    if rec.get("params"):
        out.append("- params: " + json.dumps(rec["params"], ensure_ascii=False))
    for field in ("inputs", "outputs"):
        if rec.get(field):
            out += ["", f"## {field}"]
            for f in rec[field]:
                ref = f.get("path") or f.get("url") or f.get("name")
                extra = [f"sha256 {f['sha256'][:12]}…" if f.get("sha256") else "",
                         f"{f['bytes']} bytes" if f.get("bytes") is not None else "",
                         json.dumps(f["measured"], ensure_ascii=False) if f.get("measured") else ""]
                out.append(f"- {ref} ({f.get('kind', '?')}) " + " · ".join(e for e in extra if e))
    out += ["", "## steps"]
    for s in rec.get("steps") or []:
        out.append(f"{s.get('n')}. {s.get('what')}" + (f" [{s['tool']}]" if s.get("tool") else "")
                   + (" ⚠ needs permission" if s.get("needs_permission") else ""))
        if s.get("command"):
            out.append(f"   `{s['command']}`")
        if s.get("manual"):
            out.append(f"   manual: {s['manual']}")
    rep = rec.get("reproduce") or {}
    out += ["", "## reproduce", str(rep.get("how", ""))]
    out += [f"- prerequisite: {p}" for p in rep.get("prerequisites") or []]
    for k in ("evidence", "lessons"):
        if rec.get(k):
            out += ["", f"## {k}"] + [f"- {x}" for x in rec[k]]
    return "\n".join(out) + "\n"


def replay_steps(rec: dict) -> list:
    """The commands to repeat, in order: reproduce.commands when given, else each step's command."""
    rep = rec.get("reproduce") or {}
    if rep.get("commands"):
        return [{"n": i, "what": f"reproduce command {i}", "command": c} for i, c in enumerate(rep["commands"], 1)]
    return list(rec.get("steps") or [])


def replay_sh(rec: dict) -> str:
    rid = rec["id"]
    out = ["#!/usr/bin/env bash", f"# Replay of task {rid}: {rec.get('title')}",
           f"# Request: {rec.get('request')}", f"# Mode: {rec.get('mode')}  plan: {rec.get('plan', '-')}",
           "# Generated by task_history.py replay. Read it before running; it changes nothing by itself.",
           "set -euo pipefail", ""]
    for p in (rec.get("reproduce") or {}).get("prerequisites") or []:
        out.append(f"# prerequisite: {p}")
    checks = [f for f in rec.get("inputs") or [] if f.get("path") and f.get("sha256")]
    if checks:
        out.append("# the inputs must be the same files as last time")
        for f in checks:
            out.append(f"echo {shlex.quote(f['sha256'] + '  ' + f['path'])} | sha256sum -c -")
        out.append("")
    for s in replay_steps(rec):
        out.append(f"# step {s.get('n', '-')}: {s.get('what')}")
        if s.get("needs_permission"):
            out.append("# NEEDS THE USER'S EXPLICIT PERMISSION (spend, publish or send); uncomment only after it:")
            out.append(f"# {s.get('command') or s.get('manual')}")
        elif s.get("command"):
            if s.get("cwd"):
                out.append(f"cd {shlex.quote(s['cwd'])}")
            out.append(s["command"])
        else:
            out.append(f"# MANUAL: {s.get('manual') or s.get('tool')}")
        out.append("")
    outs = [f["path"] for f in rec.get("outputs") or [] if f.get("path")]
    out.append(f"python3 {SELF} compare {shlex.quote(rid)}" if outs else "# no output paths recorded to compare")
    return "\n".join(out) + "\n"


def replay_md(rec: dict) -> str:
    out = [f"# Replay plan: {rec.get('title')} ({rec['id']})", "",
           "Same request, same mode, same tools and parameters. Repeat the steps in order, then compare.", "",
           f"- request: {rec.get('request')}", f"- mode: {rec.get('mode')} · plan: {rec.get('plan', '-')}",
           f"- tools: {', '.join(map(str, rec.get('tools') or [])) or '-'}"]
    if rec.get("params"):
        out.append("- params: " + json.dumps(rec["params"], ensure_ascii=False))
    out += ["", "## before you start"]
    out += [f"- {p}" for p in (rec.get("reproduce") or {}).get("prerequisites") or []] or ["- nothing recorded"]
    for f in rec.get("inputs") or []:
        ref = f.get("path") or f.get("url") or f.get("name")
        out.append(f"- input {ref}" + (f" must have sha256 {f['sha256']}" if f.get("sha256") else " (no hash recorded)"))
    out += ["", "## steps"]
    for i, s in enumerate(replay_steps(rec), 1):
        flag = " — needs the user's explicit permission first" if s.get("needs_permission") else ""
        out.append(f"{i}. {s.get('what')}{flag}")
        if s.get("command"):
            out.append(f"   `{s['command']}`")
        elif s.get("manual") or s.get("tool"):
            out.append(f"   manual: {s.get('manual') or s.get('tool')}")
    out += ["", "## expected result"]
    for f in rec.get("outputs") or []:
        ref = f.get("path") or f.get("url") or f.get("name")
        same = "identical bytes" if f.get("deterministic") and f.get("sha256") else "same measurements"
        out.append(f"- {ref}: {same}" + (f" {json.dumps(f['measured'], ensure_ascii=False)}" if f.get("measured") else ""))
    out += ["", f"Then: `python3 {SELF} compare {rec['id']}`", "",
            str((rec.get("reproduce") or {}).get("how", ""))]
    return "\n".join(out) + "\n"


def compare(rec: dict, base: Path) -> tuple:
    """(rows, ok): each recorded output against the file now at its path."""
    rows, ok = [], True
    for f in rec.get("outputs") or []:
        if not f.get("path"):
            rows.append((f.get("url") or f.get("name"), "skipped", "no local path recorded"))
            continue
        p = Path(f["path"])
        p = p if p.is_absolute() else base / p
        if not p.is_file():
            rows.append((f["path"], "missing", "not produced yet"))
            ok = False
            continue
        size = p.stat().st_size
        if not f.get("sha256"):
            rows.append((f["path"], "present", f"{size} bytes; no hash was recorded"))
            continue
        same = sha256_of(p) == f["sha256"]
        if same:
            rows.append((f["path"], "identical", f"{size} bytes"))
        elif f.get("deterministic"):
            rows.append((f["path"], "DIFFERENT", f"{size} bytes vs {f.get('bytes')} recorded"))
            ok = False
        else:
            rows.append((f["path"], "differs", f"{size} bytes vs {f.get('bytes')} recorded; not deterministic, "
                                               "check the measured values instead: "
                                               + json.dumps(f.get("measured") or {}, ensure_ascii=False)))
    return rows, ok


# ---------------------------------------------------------------- commands

def cmd_add(a) -> int:
    root = Path(a.root)
    raw = sys.stdin.read() if a.source == "-" else Path(a.source).read_text(encoding="utf-8")
    try:
        rec = json.loads(raw)
    except ValueError as e:
        print(f"not JSON: {e}", file=sys.stderr)
        return 2
    rec = normalise(rec, root, a.date)
    if not a.no_hash:
        fill_hashes(rec, Path(a.base))
    errors, warnings = validate_record(rec, f"{rec['id']}.json")
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        print("nothing written", file=sys.stderr)
        return 1
    if a.print:
        print(save_hints(rec, a.repo))
        return 0
    dest = tasks_dir(root) / f"{rec['id']}.json"
    if dest.exists() and not a.replace:
        print(f"{dest.name} exists; pass --replace to overwrite it", file=sys.stderr)
        return 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(dumps(rec), encoding="utf-8")
    print(f"wrote history/tasks/{dest.name}")
    return build(root)


def cmd_list(a) -> int:
    recs = records(Path(a.root))
    if a.kind:
        recs = [r for r in recs if r.get("kind") == a.kind]
    if a.q:
        words = a.q.lower().split()
        recs = [r for r in recs if all(w in json.dumps(r, ensure_ascii=False).lower() for w in words)]
    recs = recs[: a.limit] if a.limit else recs
    if a.json:
        print(json.dumps([summary(r) for r in recs], ensure_ascii=False, indent=1))
        return 0
    if not recs:
        print("no recorded tasks match" if (a.kind or a.q) else "no recorded tasks yet")
        return 0
    for i, r in enumerate(recs, 1):
        print(f"{i:>3}. {r['id']:<40} {r.get('kind', ''):<9} {str(r.get('mode', ''))[:14]:<14} {r.get('title', '')}")
    print(f"\n{len(recs)} task(s). show one: python3 {SELF} show <id or number>; repeat it: replay <id>")
    return 0


def cmd_show(a) -> int:
    rec = resolve(Path(a.root), a.ref)
    print(dumps(rec) if a.json else show_md(rec), end="")
    return 0


def cmd_replay(a) -> int:
    rec = resolve(Path(a.root), a.ref)
    text = {"sh": replay_sh, "md": replay_md, "json": lambda r: dumps({
        "id": r["id"], "request": r.get("request"), "mode": r.get("mode"), "plan": r.get("plan"),
        "params": r.get("params"), "inputs": r.get("inputs"), "steps": replay_steps(r),
        "expected_outputs": r.get("outputs"), "reproduce": r.get("reproduce")})}[a.format](rec)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out}")
    else:
        print(text, end="")
    return 0


def cmd_compare(a) -> int:
    rec = resolve(Path(a.root), a.ref)
    rows, ok = compare(rec, Path(a.dir))
    for path, state, note in rows:
        print(f"{state:<10} {path}  {note}")
    print("same result" if ok else "not the same result yet")
    return 0 if ok else 1


def cmd_validate(a) -> int:
    root = Path(a.root)
    n_err = 0
    for p, rec, err in load_all(root):
        errors, warnings = ([err], []) if err else validate_record(rec, p.name)
        for w in warnings:
            print(f"warning: {p.name}: {w}")
        for e in errors:
            print(f"error: {p.name}: {e}")
        n_err += len(errors)
    stale = build(root, check=True) if (root / "INDEX.md").exists() or records(root) else 0
    if stale and not a.strict:
        print(f"(the index is regenerated by: python3 {SELF} build)")
    total = len(load_all(root))
    print(f"{total} record(s), {n_err} error(s)")
    return 1 if n_err or (stale and a.strict) else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="task_history.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(HISTORY), help="the history folder (default: <repo>/history)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="print a record template to fill")
    p.add_argument("--kind", choices=KINDS, default="other")
    p = sub.add_parser("add", help="validate a record, hash its local files, write it and rebuild the index")
    p.add_argument("--from", dest="source", required=True, help="a JSON file, or - for stdin")
    p.add_argument("--print", action="store_true", help="write nothing; print the record and how to save it")
    p.add_argument("--date", help="YYYY-MM-DD when the record has none (default: today, UTC)")
    p.add_argument("--base", default=".", help="folder that relative input/output paths are hashed from")
    p.add_argument("--no-hash", action="store_true", help="do not add sha256/bytes for local files")
    p.add_argument("--replace", action="store_true", help="overwrite a record with the same id")
    p.add_argument("--repo", default=DEFAULT_REPO, help="owner/name for the GitHub link printed by --print")
    p = sub.add_parser("list", help="the recorded tasks, newest first")
    p.add_argument("--kind", choices=KINDS)
    p.add_argument("--q", help="words that must all appear in the record")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("show", help="one task in full")
    p.add_argument("ref", help="id, unique prefix, number from list, or last")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("replay", help="print the plan or script that repeats a task (runs nothing)")
    p.add_argument("ref")
    p.add_argument("--format", choices=("md", "sh", "json"), default="md")
    p.add_argument("--out", help="write to this file instead of stdout")
    p = sub.add_parser("compare", help="check the new outputs against the recorded ones")
    p.add_argument("ref")
    p.add_argument("--dir", default=".", help="folder the output paths are relative to")
    p = sub.add_parser("build", help="regenerate history/INDEX.md and history/index.json")
    p.add_argument("--check", action="store_true", help="write nothing; exit 1 when stale")
    p = sub.add_parser("validate", help="check every record (and the index with --strict)")
    p.add_argument("--strict", action="store_true", help="a stale index is an error too")
    a = ap.parse_args(argv)

    if a.cmd == "new":
        print(dumps(template(a.kind)), end="")
        return 0
    if a.cmd == "build":
        return build(Path(a.root), a.check)
    return {"add": cmd_add, "list": cmd_list, "show": cmd_show, "replay": cmd_replay,
            "compare": cmd_compare, "validate": cmd_validate}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
