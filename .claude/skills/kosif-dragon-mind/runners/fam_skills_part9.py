"""skills part 9: HOTL / atlas engineering workflows and obra superpowers v7 skills as real programs.

Each registered skill runs its core procedure on a deterministic fixture built in the work folder:
the skill's own shipped scripts where it has them (obra executing-plans task-start/task-done, the SDD
workspace scripts, the brainstorm companion server, find-polluter.sh, render-graphs.js), the real
toolchains that work offline (git, go, cargo, gofmt, ruby -c, prettier, eslint, the TypeScript parser),
and otherwise a program that implements the procedure's documented rules (selection algorithm, lint,
audit checklist) and is checked by known answers. Every card carries a negative control: the same
measurement fails on input where the method was not applied. Nothing here touches the network.
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from _harness import card, check, fx

REPO = Path(__file__).resolve().parents[4]
SK = REPO / ".claude/skills"
ATLAS = SK / "kosif-superpowers/vendor/kosif-atlas/skills"
OBRA = SK / "kosif-superpowers/vendor/obra-superpowers-v7/skills"
NODE_PATH = "/opt/node22/lib/node_modules"


def KA(rel):
    return "skill:kosif-superpowers/vendor/kosif-atlas/skills/" + rel


def KO(rel):
    return "skill:kosif-superpowers/vendor/obra-superpowers-v7/skills/" + rel


GAPS: dict = {
    KA("891-codex-tui-proof/2013-validate-tui-in-codex"):
        "needs the Codex in-app browser plus the plugin's scripts/tui-proof.mjs (not shipped here) and an "
        "npm ci of its locked runtime; the skill forbids any fallback surface",
    KA("972-scaffold-lean-library/2256-scaffold-lean-library"):
        "Lean 4 / lake toolchain is not installed and Mathlib cannot be fetched offline; the scaffold's "
        "verification step (lake build) cannot run, so a rendered tree would be unproven",
    KA("975-scaffold-zig-cli/2259-scaffold-zig-cli"):
        "zig compiler is not installed here; without zig build / zig fmt the scaffolded sources cannot be "
        "parsed or built, so a rendered tree would be unproven",
}

GIT_ENV = {"GIT_AUTHOR_NAME": "Fixture Dev", "GIT_AUTHOR_EMAIL": "dev@example.test",
           "GIT_COMMITTER_NAME": "Fixture Dev", "GIT_COMMITTER_EMAIL": "dev@example.test",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}


def env(**extra):
    e = dict(os.environ)
    e.update(GIT_ENV)
    e["NODE_PATH"] = NODE_PATH
    e.update({k: str(v) for k, v in extra.items()})
    return e


def sh(cmd, cwd, ok=True, timeout=60, **extra):
    """Run a command (list) in cwd; ok=True raises on non-zero exit."""
    p = subprocess.run([str(c) for c in cmd], cwd=str(cwd), capture_output=True, text=True, timeout=timeout,
                       env=env(**extra), stdin=subprocess.DEVNULL)
    if ok and p.returncode:
        raise RuntimeError("%s failed (%d): %s %s" % (cmd[0], p.returncode, p.stdout[-300:], p.stderr[-300:]))
    return p


def git(cwd, *args, ok=True):
    return sh(["git", *args], cwd, ok=ok)


def git_repo(d, files: dict, msg="init"):
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    git(d, "init", "-q", "-b", "main")
    git(d, "config", "user.name", "Fixture Dev")
    git(d, "config", "user.email", "dev@example.test")
    git(d, "config", "commit.gpgsign", "false")
    write_tree(d, files)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg)
    return d


def write_tree(d, files: dict):
    for rel, text in files.items():
        p = Path(d) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def jw(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def tw(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")
    return Path(path)


def tmpl(ref: Path, repl: dict = None, idx: int = 0) -> str:
    """The idx-th fenced block of a reference template, with placeholders replaced."""
    text = Path(ref).read_text(encoding="utf-8")
    blocks = [m.group(2) for m in re.finditer(r"^(`{3,})[\w-]*\n(.*?)^\1[ \t]*$", text, flags=re.S | re.M)]
    body = blocks[idx]
    for k, v in (repl or {}).items():
        body = body.replace(k, v)
    return body


def frontmatter(text: str) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        return {}
    import yaml
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        out = {}
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"')
        return out


def tree_digest(d):
    import hashlib
    h = hashlib.sha256()
    for p in sorted(Path(d).rglob("*")):
        if p.is_file() and ".git" not in p.relative_to(d).parts:
            h.update(str(p.relative_to(d)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


# =====================================================================================================
# HOTL brainstorming: design doc with the three contracts + document-lint (structure + leakage)
# =====================================================================================================
HOTL_SECTIONS = ["Intent Contract", "Verification Contract", "Governance Contract", "Scope", "Decisions",
                 "Surface", "Risks & Open Questions"]


def hotl_document_lint(text: str):
    """Reimplementation of the documented document-lint contract (warning-only, exit 0)."""
    fm = frontmatter(text)
    dtype = fm.get("design_type")
    if not dtype and not fm.get("hotl_managed"):
        return "SKIP", []
    if dtype not in ("feature", "phase"):
        return "OK", []
    warns = []
    heads = re.findall(r"^## (.+?)\s*$", text, flags=re.M)
    for s in HOTL_SECTIONS:
        if s not in heads:
            warns.append('category=structure severity=warning design_type=%s message="missing required section: ## %s"'
                         % (dtype, s))
    lines = text.splitlines()
    in_fence, fence_start, fence_n, quoted = False, 0, 0, False
    for i, line in enumerate(lines, 1):
        if line.startswith("```"):
            if in_fence and fence_n > 10:
                warns.append('category=implementation-leakage severity=warning design_type=%s line=%d message='
                             '"long fenced code block (%d lines)"' % (dtype, fence_start, fence_n))
            in_fence, fence_start, fence_n = not in_fence, i, 0
            continue
        if in_fence:
            fence_n += 1
            continue
        if line.startswith(">"):
            continue
        if re.search(r"\b[\w/.-]+\.(py|ts|js|go|rs|tsx|java):\d+\b", line):
            warns.append('category=implementation-leakage severity=warning design_type=%s line=%d message='
                         '"file:line reference"' % (dtype, i))
        if len(re.findall(r"(?<!\S)--[\w-]+", line)) >= 6:
            warns.append('category=implementation-leakage severity=warning design_type=%s line=%d message='
                         '"dense flag line"' % (dtype, i))
    return "OK", warns


def hotl_design(slug, date, intent, risk):
    contracts = {
        "Intent Contract": "```\nintent: %s\nconstraints: public CSV export API must not change\n"
                           "success_criteria: export of 10k rows completes under 2 s in the benchmark\n"
                           "risk_level: %s\n```" % (intent, risk),
        "Verification Contract": "```\nverify_steps:\n  - run tests: make test\n  - check: benchmark output\n"
                                 "  - confirm: p95 under 2 s\n```",
        "Governance Contract": "```\napproval_gates: [design approval, merge review]\nrollback: revert the merge "
                               "commit\nownership: data-platform team\n```",
        "Scope": "| In | Out |\n|---|---|\n| streaming CSV writer | new formats |",
        "Decisions": "| # | Decision | Choice | Rejected |\n|---|---|---|---|\n| 1 | buffering | stream rows | "
                     "build whole file in memory |",
        "Surface": "Export service streams rows to the response; storage untouched.",
        "Risks & Open Questions": "Large exports may hold a DB cursor open; confirm cursor timeout.",
    }
    body = "---\ndesign_type: feature\ncreated_at: %s\n---\n\n# %s design\n\n" % (date, slug)
    body += "\n\n".join("## %s\n\n%s" % (k, contracts[k]) for k in HOTL_SECTIONS) + "\n"
    return body


@card(KA("3606-hotl/14485-brainstorming"))
def hotl_brainstorming(task, wd):
    date = "2026-11-03"
    slug = "streaming-csv-export"
    approaches = [{"name": "stream rows", "tradeoff": "low memory, needs cursor"},
                  {"name": "background job + download link", "tradeoff": "async UX"},
                  {"name": "paginate client side", "tradeoff": "many requests"}]
    path = wd / "docs/designs" / ("%s-%s-design.md" % (date, slug))
    tw(path, hotl_design(slug, date, "Stream CSV exports instead of buffering them", "medium"))
    status, warns = hotl_document_lint(path.read_text())
    jw(wd / "approaches.json", {"scope": "feature", "approaches": approaches, "recommended": approaches[0]["name"]})
    # negative control: a doc written without the discipline (missing two sections, leakage)
    bad = ("---\ndesign_type: feature\ncreated_at: %s\n---\n\n## Intent Contract\n\nSee export.py:16 and "
           "auth.ts:204.\n\n## Scope\n\n```python\n" % date + "\n".join("x%d = %d" % (i, i) for i in range(12))
           + "\n```\n\ndocker run --network=none --cap-drop=ALL --read-only --tmpfs /tmp --pids-limit 5 --rm img\n")
    bstatus, bwarns = hotl_document_lint(bad)
    tw(wd / "bad-design.md", bad)
    struct_bad = sum("category=structure" in w for w in bwarns)
    leak_bad = sum("implementation-leakage" in w for w in bwarns)
    ustatus, _ = hotl_document_lint("# ad hoc notes\n\n## Intent Contract\n")
    ok_name = re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+-design\.md", path.name) is not None
    fm = frontmatter(path.read_text())
    return [
        check("design doc path follows feature scope pattern docs/designs/YYYY-MM-DD-<slug>-design.md", ok_name, path.name),
        check("frontmatter carries design_type: feature and created_at", fm.get("design_type") == "feature"
              and str(fm.get("created_at")) == date, fm),
        check("all three HOTL contracts present with their fields",
              all(k in path.read_text() for k in ["intent:", "risk_level:", "verify_steps:", "approval_gates:",
                                                   "rollback:", "ownership:"]), True, True),
        check("2-3 approaches proposed with a recommendation", 2 <= len(approaches) <= 3, len(approaches), "2..3"),
        check("document-lint on the saved doc: zero warnings", status == "OK" and not warns, len(warns), 0),
        check("negative control: undisciplined doc -> 5 missing-section warnings", struct_bad == 5, struct_bad, 5),
        check("negative control: file:line line + long fence + dense flag line -> 3 leakage warnings", leak_bad == 3, leak_bad, 3),
        check("unmarked doc is skipped (frontmatter is the deterministic signal)", ustatus == "SKIP", ustatus, "SKIP"),
    ], [path, wd / "approaches.json", jw(wd / "lint.json", {"good": warns, "bad": bwarns})]


# =====================================================================================================
# HOTL executing-plans: linear executor, batches of 3, typed verification, persisted state
# =====================================================================================================
def hotl_parse_workflow(text):
    steps = []
    for m in re.finditer(r"^### Step (\d+): (.+?)\n```yaml\n(.*?)```", text, flags=re.S | re.M):
        import yaml
        spec = yaml.safe_load(m.group(3))
        steps.append({"n": int(m.group(1)), "title": m.group(2), **spec})
    return steps


def hotl_verify(v, root):
    if isinstance(v, str):
        v = {"type": "shell", "command": v}
    if isinstance(v, list):
        res = [hotl_verify(x, root) for x in v]
        return ("pass" if all(r[0] == "pass" for r in res) else
                next(r for r in res if r[0] != "pass")[0]), [r[1] for r in res]
    t = v.get("type")
    if t == "shell":
        p = subprocess.run(v["command"], shell=True, cwd=root, capture_output=True, text=True, timeout=20)
        return ("pass" if p.returncode == 0 else "fail"), {"exit": p.returncode, "stdout": p.stdout[-200:]}
    if t == "human-review":
        return "blocked", {"reason": "human review required: " + v.get("check", "")}
    if t == "browser":
        return "blocked", {"reason": "human review required (browser unavailable, downgraded): " + v.get("check", "")}
    if t == "artifact":
        p = Path(root) / v["path"]
        kind = v.get("assert", {}).get("kind", "exists")
        val = v.get("assert", {}).get("value", "")
        if kind == "exists":
            return ("pass" if p.exists() else "fail"), {"path": v["path"]}
        if kind == "contains":
            return ("pass" if p.is_file() and val in p.read_text() else "fail"), {"path": v["path"]}
        if kind == "matches-glob":
            if "/" in val:
                return "invalid", {"reason": "matches-glob value must be a filename glob only: " + val}
            return ("pass" if p.is_dir() and any(p.glob(val)) else "fail"), {"path": v["path"], "glob": val}
    return "invalid", {"reason": "unknown verify type %r" % t}


def hotl_execute(steps, root, state_path, approvals=None):
    approvals = approvals or {}
    state = {"status": "running", "steps": {}, "batches": []}
    order = sorted(steps, key=lambda s: s["n"])
    for b in range(0, len(order), 3):
        batch = order[b:b + 3]
        state["batches"].append([s["n"] for s in batch])
        for s in batch:
            state["steps"][s["n"]] = {"status": "running"}
            jw(state_path, state)
            if s.get("action"):
                subprocess.run(s["action"], shell=True, cwd=root, capture_output=True, timeout=20)
            verdict, detail = hotl_verify(s["verify"], root)
            if verdict == "blocked" and approvals.get(s["n"]) == "approved":
                verdict = "pass"
                detail = {"gate": "approved", "mode": "human"}
            state["steps"][s["n"]] = {"status": {"pass": "done"}.get(verdict, verdict), "detail": detail}
            jw(state_path, state)
            if verdict != "pass":
                state["status"] = "paused" if verdict == "blocked" else "stopped"
                state["stopped_at"] = s["n"]
                jw(state_path, state)
                return state
        state.setdefault("checkpoints", []).append("review after batch %d" % len(state["batches"]))
    state["status"] = "ready_to_finish"
    jw(state_path, state)
    return state


@card(KA("3606-hotl/14489-executing-plans"))
def hotl_executing_plans(task, wd):
    root = wd / "proj"
    root.mkdir(parents=True, exist_ok=True)
    wf = """# Workflow

### Step 1: create package
```yaml
action: mkdir -p src && printf 'def add(a, b):\\n    return a + b\\n' > src/calc.py
verify: {type: artifact, path: src/calc.py, assert: {kind: exists}}
```
### Step 2: export symbol
```yaml
action: printf '__all__ = ["add"]\\n' >> src/calc.py
verify: {type: artifact, path: src/calc.py, assert: {kind: contains, value: __all__}}
```
### Step 3: test file
```yaml
action: printf 'import sys; sys.path.insert(0, "src"); import calc; assert calc.add(2, 3) == 5\\n' > test_calc.py
verify: python3 test_calc.py
```
### Step 4: glob check
```yaml
verify: {type: artifact, path: src, assert: {kind: matches-glob, value: "*.py"}}
```
### Step 5: design sign-off
```yaml
verify: {type: human-review, check: "Confirm the add() signature"}
```
### Step 6: docs
```yaml
action: echo '# calc' > README.md
verify: [{type: artifact, path: README.md, assert: {kind: contains, value: calc}}, "test -s README.md"]
```
"""
    tw(root / "docs/plans/calc-workflow.md", wf)
    steps = hotl_parse_workflow(wf)
    st1 = hotl_execute(steps, root, wd / ".hotl/state/run-1.json")
    st2 = hotl_execute(steps, root, wd / ".hotl/state/run-2.json", approvals={5: "approved"})
    broken = [dict(s) for s in steps]
    broken[2] = dict(broken[2], action="printf 'assert 1 == 2\\n' > test_calc.py")
    st3 = hotl_execute(broken, root, wd / ".hotl/state/run-3.json")
    inv, _ = hotl_verify({"type": "artifact", "path": ".", "assert": {"kind": "matches-glob", "value": "src/*"}}, root)
    persisted = json.loads((wd / ".hotl/state/run-2.json").read_text())
    return [
        check("6 steps parsed from the workflow file", len(steps) == 6, len(steps), 6),
        check("tasks run 3 at a time", st2["batches"] == [[1, 2, 3], [4, 5, 6]], st2["batches"], [[1, 2, 3], [4, 5, 6]]),
        check("human-review gate pauses the run at step 5 (never auto-approved)",
              st1["status"] == "paused" and st1["stopped_at"] == 5, [st1["status"], st1.get("stopped_at")], ["paused", 5]),
        check("step 6 not started while gate is pending", "6" not in {str(k) for k in st1["steps"]}, list(st1["steps"]), "no 6"),
        check("with recorded human approval the run reaches ready_to_finish", st2["status"] == "ready_to_finish",
              st2["status"], "ready_to_finish"),
        check("state persisted to .hotl/state/<run>.json with all 6 steps done",
              persisted["status"] == "ready_to_finish" and len(persisted["steps"]) == 6, len(persisted["steps"]), 6),
        check("negative control: failing shell verify stops at step 3, nothing silently skipped",
              st3["status"] == "stopped" and st3["stopped_at"] == 3 and "4" not in {str(k) for k in st3["steps"]},
              [st3["status"], st3.get("stopped_at")], ["stopped", 3]),
        check("matches-glob with a path in value (src/*) is rejected as invalid", inv == "invalid", inv, "invalid"),
    ], [wd / ".hotl/state/run-1.json", wd / ".hotl/state/run-2.json", wd / ".hotl/state/run-3.json"]


# =====================================================================================================
# HOTL skill-authoring: trigger-only description lint + routing/mirror index checks
# =====================================================================================================
def skill_author_lint(root: Path):
    findings = []
    index = (root / "skills/using-hotl/SKILL.md").read_text() if (root / "skills/using-hotl/SKILL.md").exists() else ""
    docs = (root / "docs/skills.md").read_text() if (root / "docs/skills.md").exists() else ""
    for sk in sorted((root / "skills").glob("*/SKILL.md")):
        name_dir = sk.parent.name
        fm = frontmatter(sk.read_text())
        name, desc = str(fm.get("name", "")), str(fm.get("description", ""))
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            findings.append((name_dir, "name-not-kebab-case"))
        if not desc.lower().startswith("use when") and not desc.lower().startswith("use before"):
            findings.append((name_dir, "description-not-trigger"))
        workflow_words = re.findall(r"\b(then|dispatches|reviews every|finalizes|runs|step \d)\b", desc.lower())
        if len(workflow_words) >= 2 or re.search(r"\s-\s\w+.*,\s*then\b", desc.lower()):
            findings.append((name_dir, "description-summarizes-workflow"))
        if name_dir != "using-hotl" and name not in index:
            findings.append((name_dir, "not-indexed-in-using-hotl"))
        if name_dir != "using-hotl" and name not in docs:
            findings.append((name_dir, "missing-from-docs-skills"))
    return findings


@card(KA("3606-hotl/14498-skill-authoring"))
def hotl_skill_authoring(task, wd):
    src = (ATLAS / "3606-hotl/14498-skill-authoring/SKILL.md").read_text()
    bad_desc = re.search(r"Bad:\s*```yaml\s*description: (.+?)\n```", src, flags=re.S).group(1).strip()
    good_desc = re.search(r"Good:\s*```yaml\s*description: (.+?)\n```", src, flags=re.S).group(1).strip()
    root = wd / "hotl"
    fx_files = {
        "skills/using-hotl/SKILL.md": "---\nname: using-hotl\ndescription: Use when starting any HOTL session.\n---\n"
                                      "- executing-plans\n",
        "skills/executing-plans/SKILL.md": "---\nname: executing-plans\ndescription: %s\n---\nbody\n" % good_desc,
        "skills/subagent-exec/SKILL.md": "---\nname: subagent-exec\ndescription: %s\n---\nbody\n" % bad_desc,
        "skills/Bad_Name/SKILL.md": "---\nname: Bad_Name\ndescription: Use when testing names.\n---\nbody\n",
        "docs/skills.md": "| executing-plans | ... |\n| Bad_Name | ... |\n",
    }
    write_tree(root, fx_files)
    f1 = skill_author_lint(root)
    rep = jw(wd / "skill_lint.json", [{"skill": a, "rule": b} for a, b in f1])
    got = sorted(set(f1))
    expected = sorted({("subagent-exec", "description-summarizes-workflow"), ("subagent-exec", "not-indexed-in-using-hotl"),
                       ("subagent-exec", "missing-from-docs-skills"),
                       ("Bad_Name", "name-not-kebab-case"), ("Bad_Name", "not-indexed-in-using-hotl")})
    # fix: rewrite per the skill's rules, update routing and mirrors, re-lint
    write_tree(root, {"skills/subagent-exec/SKILL.md": "---\nname: subagent-exec\ndescription: %s\n---\nbody\n" % good_desc,
                      "skills/using-hotl/SKILL.md": fx_files["skills/using-hotl/SKILL.md"] + "- subagent-exec\n",
                      "docs/skills.md": "| executing-plans |\n| subagent-exec |\n"})
    shutil.rmtree(root / "skills/Bad_Name")
    f2 = skill_author_lint(root)
    return [
        check("Bad/Good examples extracted from the skill text", bool(bad_desc) and bool(good_desc), [bad_desc[:40], good_desc[:40]]),
        check("lint finds exactly the seeded problems", got == expected, got, expected),
        check("the skill's own Good description passes the trigger-only rule",
              ("executing-plans", "description-summarizes-workflow") not in f1, True, True),
        check("after fixing description, index and mirror: zero findings", f2 == [], f2, []),
        check("negative control: the Bad description is flagged as a workflow summary",
              ("subagent-exec", "description-summarizes-workflow") in f1, True, True),
    ], [rep]


# =====================================================================================================
# zagrosi-plan: spec -> compact canonical plan (sections/index.md) + postflight coverage validator
# =====================================================================================================
def zagrosi_postflight(pdir: Path):
    errs = []
    idx = (pdir / "sections/index.md").read_text() if (pdir / "sections/index.md").exists() else ""
    spec = (pdir / "spec.md").read_text().splitlines()
    for blk in ("PROJECT_CONFIG", "SECTION_MANIFEST", "FORGE_META"):
        if "<!-- " + blk not in idx:
            errs.append("missing block " + blk)
    m = re.search(r"<!-- FORGE_META\n(.*?)\nEND_FORGE_META -->", idx, flags=re.S)
    if m:
        meta = json.loads(m.group(1))
        if meta.get("artifact_type") != "compact_plan" or meta.get("source") != "spec.md":
            errs.append("bad FORGE_META")
    for h in ("## Contract", "## Owned files", "## Evidence", "## Review"):
        if h not in idx:
            errs.append("missing heading " + h)
    covered = set()
    body = re.sub(r"```.*?```", "", idx, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    for rq in re.finditer(r"^### (REQ-\d{3})\n(.*?)(?=^### |^## )", body + "\n## END", flags=re.S | re.M):
        fields = dict(re.findall(r"^(Source|Behavior|Expected|Command): (.+)$", rq.group(2), flags=re.M))
        for f in ("Source", "Behavior", "Expected", "Command"):
            if not fields.get(f) or "<" in fields.get(f, ""):
                errs.append("%s missing %s" % (rq.group(1), f))
        sm = re.match(r"spec\.md#L(\d+)(?:-L(\d+))?", fields.get("Source", ""))
        if sm:
            a, b = int(sm.group(1)), int(sm.group(2) or sm.group(1))
            covered.update(range(a, b + 1))
    visible = {i for i, line in enumerate(spec, 1) if line.strip()}
    if visible - covered:
        errs.append("uncovered spec lines: %s" % sorted(visible - covered))
    if not re.search(r"^Verdict: pass$", idx, flags=re.M):
        errs.append("review verdict not pass")
    return errs


@card(KA("3612-zagrosi-forge/14531-zagrosi-plan"))
def zagrosi_plan(task, wd):
    pdir = wd / "planning"
    spec = ("Trim leading and trailing spaces from labels.\nPreserve case and internal spaces.\n\n"
            "Reject labels longer than 64 characters with ValueError.\n")
    tw(pdir / "spec.md", spec)
    lines = spec.splitlines()
    reqs, groups, cur = [], [], []
    for i, line in enumerate(lines, 1):            # group consecutive non-blank lines into requirements
        if line.strip():
            cur.append(i)
        elif cur:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    tests = ["test_trim_edges", "test_long_label_rejected"]
    for n, g in enumerate(groups, 1):
        src = "spec.md#L%d" % g[0] + ("-L%d" % g[-1] if len(g) > 1 else "")
        text = " ".join(lines[i - 1] for i in g)
        reqs.append("### REQ-%03d\nSource: %s\nBehavior: %s\nExpected: %s passes; current code fails it.\n"
                    "Command: python3 -m pytest tests/test_labels.py -k %s\n" % (n, src, text, tests[n - 1], tests[n - 1]))
    idx = ("<!-- PROJECT_CONFIG\nruntime: python3.11\ntest_command: python3 -m pytest\nEND_PROJECT_CONFIG -->\n"
           "<!-- SECTION_MANIFEST\nsection-01-labels\nEND_MANIFEST -->\n"
           "<!-- FORGE_META\n%s\nEND_FORGE_META -->\nDependencies: none.\nExecution order: section-01-labels.\n"
           "Parallel: no siblings.\n\n## Contract\n%s\n## Owned files\n- src/labels.py\n- tests/test_labels.py\n\n"
           "## Evidence\nInspected the label helper and its two callers; no external contract.\n\n"
           "## Review\nVerdict: pass\nReviewed: source coverage of all spec lines, edge cases, ownership.\n"
           % (json.dumps({"artifact_type": "compact_plan", "depth_mode": "lean", "source": "spec.md"}), "\n".join(reqs)))
    tw(pdir / "sections/index.md", idx)
    errs = zagrosi_postflight(pdir)
    # negative control: drop REQ-002 (the 64-char constraint) -> postflight must report uncovered line 4
    neg = wd / "planning-neg"
    shutil.copytree(pdir, neg)
    tw(neg / "sections/index.md", re.sub(r"### REQ-002\n.*?(?=## Owned)", "", idx, flags=re.S))
    nerrs = zagrosi_postflight(neg)
    return [
        check("spec saved unchanged as spec.md", (pdir / "spec.md").read_text() == spec, True, True),
        check("one REQ per requirement block (2)", len(reqs) == 2, len(reqs), 2),
        check("postflight passes: blocks, 4 headings, REQ fields, full source coverage", errs == [], errs, []),
        check("negative control: dropping a requirement leaves spec line 4 uncovered",
              any("uncovered spec lines: [4]" in e for e in nerrs), nerrs, "uncovered [4]"),
    ], [pdir / "sections/index.md", jw(wd / "postflight.json", {"plan": errs, "negative": nerrs})]


# =====================================================================================================
# React: Vercel best-practice rules as TypeScript-AST detectors, proven on the rules' own examples
# =====================================================================================================
REACT_RULES = ATLAS / "42-react-development/63-react-best-practices/rules"
REACT_DETECTOR = r"""
const ts = require('typescript'); const fs = require('fs');
const files = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const isComp = n => /^[A-Z]/.test(n || '');
function fnName(node){ if (node.name && node.name.text) return node.name.text;
  if (node.parent && ts.isVariableDeclaration(node.parent) && node.parent.name.text) return node.parent.name.text; return null; }
function names(node, acc){ if (ts.isIdentifier(node)) acc.add(node.text); ts.forEachChild(node, c => names(c, acc)); return acc; }
function inUseMemo(node){ for (let p = node.parent; p; p = p.parent){ if (ts.isCallExpression(p) && ts.isIdentifier(p.expression)
  && ['useMemo','useCallback'].includes(p.expression.text)) return true; if (ts.isFunctionDeclaration(p) && isComp(fnName(p))) return false; } return false; }
function enclosingComp(node){ for (let p = node.parent; p; p = p.parent){ if ((ts.isFunctionDeclaration(p)||ts.isArrowFunction(p)||ts.isFunctionExpression(p)) && isComp(fnName(p))) return p; } return null; }
const out = {};
for (const [name, src] of Object.entries(files)) {
  const sf = ts.createSourceFile(name, src, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const hits = []; const line = n => sf.getLineAndCharacterOfPosition(n.getStart()).line + 1;
  function stmtList(stmts){ // async-parallel: consecutive awaited declarations with no data dependency
    let prev = [];
    for (const st of stmts) {
      const d = ts.isVariableStatement(st) && st.declarationList.declarations.length === 1 ? st.declarationList.declarations[0] : null;
      if (d && d.initializer && ts.isAwaitExpression(d.initializer) && ts.isIdentifier(d.name)) {
        const used = names(d.initializer, new Set());
        const indep = prev.length && prev.every(p => !used.has(p.n));
        if (indep && !ts.isArrayLiteralExpression(d.initializer.expression)) hits.push({rule: 'async-parallel', line: line(st)});
        prev = indep || !prev.length ? prev.concat([{n: d.name.text}]) : [{n: d.name.text}];
      } else prev = [];
    }
  }
  function visit(node){
    if (ts.isSourceFile(node) || ts.isBlock(node)) stmtList(node.statements);
    if (ts.isVariableDeclaration(node) && ts.isIdentifier(node.name) && isComp(node.name.text) && node.initializer
        && (ts.isArrowFunction(node.initializer) || ts.isFunctionExpression(node.initializer)) && enclosingComp(node))
      hits.push({rule: 'rerender-no-inline-components', line: line(node)});
    if (ts.isNewExpression(node) && ts.isIdentifier(node.expression) && node.expression.text === 'RegExp' && enclosingComp(node) && !inUseMemo(node))
      hits.push({rule: 'js-hoist-regexp', line: line(node)});
    ts.forEachChild(node, visit);
  }
  visit(sf); out[name] = hits;
}
console.log(JSON.stringify(out));
"""


def react_detect(wd, files: dict):
    js = tw(Path(wd) / "react_detector.cjs", REACT_DETECTOR)
    inp = jw(Path(wd) / "react_input.json", files)
    return json.loads(sh(["node", js, inp], wd).stdout.strip().splitlines()[-1])


def rule_examples(rule):
    text = (REACT_RULES / (rule + ".md")).read_text()
    bad = re.search(r"\*\*Incorrect[^\n]*\n+```\w*\n(.*?)```", text, flags=re.S).group(1)
    good = re.search(r"\*\*Correct[^\n]*\n+```\w*\n(.*?)```", text, flags=re.S).group(1)
    return bad, good


RULES3 = ["async-parallel", "rerender-no-inline-components", "js-hoist-regexp"]


@card(KA("42-react-development/63-react-best-practices"))
def react_best_practices(task, wd):
    files = {}
    for r in RULES3:
        bad, good = rule_examples(r)
        files[r + ".incorrect.tsx"] = ("async function f(){\n" + bad + "\n}\n") if r == "async-parallel" else bad
        files[r + ".correct.tsx"] = ("async function f(){\n" + good + "\n}\n") if r == "async-parallel" else good
    res = react_detect(wd, files)
    rep = jw(wd / "react_rules_report.json", res)
    checks = []
    for r in RULES3:
        b = [h for h in res[r + ".incorrect.tsx"] if h["rule"] == r]
        g = [h for h in res[r + ".correct.tsx"] if h["rule"] == r]
        checks.append(check("%s: rule file's Correct example is clean" % r, not g, len(g), 0))
        checks.append(check("negative control %s: rule file's Incorrect example is flagged" % r, len(b) >= 1, len(b), ">=1"))
    nb = len([h for h in res["async-parallel.incorrect.tsx"] if h["rule"] == "async-parallel"])
    checks.append(check("async-parallel: 3 sequential independent awaits -> 2 flagged follow-ups", nb == 2, nb, 2))
    ni = len([h for h in res["rerender-no-inline-components.incorrect.tsx"] if h["rule"] == "rerender-no-inline-components"])
    checks.append(check("inline components Avatar + Stats both flagged", ni == 2, ni, 2))
    return checks, [rep]


@card(KA("82-react-development/164-review-react-workflow"))
def review_react(task, wd):
    root = wd / "app"
    base_files = {"src/App.jsx": "import Profile from './Profile';\nexport default function App(){ return <Profile/>; }\n",
                  "src/Profile.jsx": "export default function Profile(){ return <div/>; }\n",
                  "src/Search.jsx": "export default function Search(){ return <input/>; }\n",
                  "src/styles.css": "body{margin:0}\n",
                  "eslint.config.cjs": "module.exports=[{files:['**/*.jsx'],languageOptions:{ecmaVersion:2022,"
                                       "sourceType:'module',parserOptions:{ecmaFeatures:{jsx:true}}},"
                                       "rules:{'no-unused-vars':'error'}}];\n"}
    git_repo(root, base_files)
    tw(root / "src/Profile.jsx", "export default function Profile({ user, theme }) {\n  const unused = 1;\n"
       "  const Avatar = () => <img src={user.avatarUrl} className={theme} />;\n"
       "  const regex = new RegExp(user.q, 'gi');\n  return <div><Avatar /></div>;\n}\n")
    tw(root / "src/styles.css", "body{margin:1px}\n")
    changed = sorted({l for l in git(root, "diff", "HEAD", "--name-only").stdout.split() if re.search(r"\.(tsx|jsx)$", l)})
    mode = "diff" if changed else "full"
    es = sh(["eslint", "--format", "json", *changed], root, ok=False)
    lint = json.loads(es.stdout or "[]")
    eslint_rules = sorted({m["ruleId"] for f in lint for m in f["messages"] if m.get("ruleId")})
    det = react_detect(wd, {f: (root / f).read_text() for f in changed})
    findings = [{"file": f, **h} for f, hs in det.items() for h in hs]
    score = max(0, 10 - 3 * len(findings) - len(eslint_rules))
    md = ["# React review (%s mode)" % mode, "", "Score: %d/10" % score, "", "## Findings", ""]
    md += ["- [ ] %s:%d Violates %s" % (x["file"], x["line"], x["rule"]) for x in findings]
    md += ["", "## Linter (ESLint, ground truth)", ""] + ["- %s" % r for r in eslint_rules]
    rep = tw(root / ".react-review/report.md", "\n".join(md) + "\n")
    rules = sorted({x["rule"] for x in findings})
    full = sorted(str(p.relative_to(root)) for p in (root / "src").rglob("*.jsx"))
    return [
        check("diff mode: only changed React files reviewed (CSS ignored)", mode == "diff" and changed == ["src/Profile.jsx"],
              changed, ["src/Profile.jsx"]),
        check("ESLint ran for real and reported no-unused-vars", eslint_rules == ["no-unused-vars"], eslint_rules, ["no-unused-vars"]),
        check("rule-ID findings in report", rules == ["js-hoist-regexp", "rerender-no-inline-components"], rules,
              ["js-hoist-regexp", "rerender-no-inline-components"]),
        check("report cites every finding with its rule id", all("Violates " + r in rep.read_text() for r in rules), True, True),
        check("negative control: full-mode set would include unchanged files (diff mode narrowed it)", len(full) == 3, len(full), 3),
    ], [rep]


# =====================================================================================================
# Dependency audit: discovery + real offline tool runs + honest coverage gaps + supply-chain signals
# =====================================================================================================
def npm_lock(pkgs: dict, scripts: set):
    lock = {"name": "shop", "version": "1.0.0", "lockfileVersion": 3, "requires": True,
            "packages": {"": {"name": "shop", "version": "1.0.0", "dependencies": {k: "^" + v for k, v in pkgs.items()}}}}
    for k, v in pkgs.items():
        e = {"version": v, "resolved": "https://registry.npmjs.org/%s/-/%s-%s.tgz" % (k, k, v), "integrity": "sha512-x"}
        if k in scripts:
            e["hasInstallScript"] = True
        lock["packages"]["node_modules/" + k] = e
    return lock


def deps_audit(root: Path):
    root = Path(root)
    eco, facts, gaps = {}, [], []
    if (root / "package.json").exists():
        flavor = next((f for f, n in [("package-lock.json", "npm"), ("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"),
                                      ("bun.lockb", "bun")] if (root / f).exists()), None)
        eco["npm"] = {"manifest": "package.json", "lockfile": flavor}
        p = sh(["npm", "ls", "--json", "--package-lock-only", "--offline"], root, ok=False)
        deps = json.loads(p.stdout or "{}").get("dependencies", {})
        for k, v in sorted(deps.items()):
            facts.append({"ecosystem": "npm", "package": k, "installed": v.get("version"), "tier": "TOOL-REPORTED",
                          "source": "npm ls --package-lock-only"})
        lock = json.loads((root / "package-lock.json").read_text())
        for path, e in lock["packages"].items():
            if e.get("hasInstallScript"):
                facts.append({"ecosystem": "npm", "signal": "install script", "package": path.split("node_modules/")[-1],
                              "tier": "INFERRED", "derivation": "hasInstallScript: true in package-lock.json",
                              "verify": "npm view %s scripts" % path.split("node_modules/")[-1]})
        gaps.append("npm: vulnerabilities and outdated not checked: registry/advisory database unreachable offline")
    if (root / "requirements.txt").exists():
        eco["python"] = {"manifest": "requirements.txt"}
        for line in (root / "requirements.txt").read_text().splitlines():
            if line.strip() and not line.startswith("#") and "==" not in line:
                facts.append({"ecosystem": "python", "signal": "unpinned requirement", "package": re.split(r"[<>=~! ]", line)[0],
                              "tier": "INFERRED", "derivation": "no == pin in requirements.txt"})
        gaps.append("python: pip-audit not installed (pipx install pip-audit); advisory DB unreachable")
    if (root / "go.mod").exists():
        eco["go"] = {"manifest": "go.mod"}
        p = sh(["go", "list", "-m", "-json", "all"], root, ok=False, GOFLAGS="-mod=mod", GOPROXY="off", GOTOOLCHAIN="local")
        mods = [json.loads("{" + c) for c in ("\n" + p.stdout).split("\n{")[1:]]
        for m in mods:
            facts.append({"ecosystem": "go", "package": m["Path"], "main": bool(m.get("Main")), "tier": "TOOL-REPORTED",
                          "source": "go list -m -json all"})
        gaps.append("go: govulncheck not installed; vuln.go.dev unreachable")
    if (root / "Cargo.toml").exists():
        eco["rust"] = {"manifest": "Cargo.toml"}
        p = sh(["cargo", "metadata", "--offline", "--format-version", "1", "--no-deps"], root, ok=False)
        for pk in json.loads(p.stdout or '{"packages":[]}')["packages"]:
            facts.append({"ecosystem": "rust", "package": pk["name"], "installed": pk["version"], "tier": "TOOL-REPORTED",
                          "source": "cargo metadata --offline"})
        gaps.append("rust: cargo-audit not installed (cargo install cargo-audit)")
    return eco, facts, gaps


@card(KA("63-dependency-audit/103-deps-audit-workflow"))
def deps_audit_workflow(task, wd):
    root = wd / "repo"
    pkgs = {"left-pad": "1.3.0", "esbuild": "0.19.2"}
    write_tree(root, {"package.json": json.dumps({"name": "shop", "version": "1.0.0",
                                                  "dependencies": {k: "^" + v for k, v in pkgs.items()}}),
                      "package-lock.json": json.dumps(npm_lock(pkgs, {"esbuild"})),
                      "requirements.txt": "requests==2.31.0\nflask>=2\n",
                      "go.mod": "module example.test/svc\n\ngo 1.22\n", "main.go": "package main\n\nfunc main() {}\n",
                      "Cargo.toml": '[package]\nname = "tool"\nversion = "0.2.0"\nedition = "2021"\n',
                      "src/lib.rs": "pub fn f() {}\n"})
    before = tree_digest(root)
    eco, facts, gaps = deps_audit(root)
    after = tree_digest(root)
    md = ["# Dependency Audit: repo", "", "**Ecosystems audited:** %s | **Coverage gaps:** %s" % (", ".join(sorted(eco)), "; ".join(gaps)),
          "", "## Vulnerabilities (TOOL-REPORTED)", "", "None reported: no advisory source reachable (see coverage gaps).", "",
          "## Supply-chain signals (require human verification)", ""]
    md += ["- %s: %s (%s) -> %s" % (f["package"], f["signal"], f["tier"], f.get("verify", f.get("derivation"))) for f in facts if "signal" in f]
    md += ["", "## Remediation plan", "", "No update has been applied. Approve specific rows to proceed (--update-pr).", "",
           "## Evidence ledger", ""] + ["- %s %s: %s" % (f["tier"], f["package"], f.get("source") or f.get("derivation")) for f in facts]
    rep = tw(wd / "deps-audit.md", "\n".join(md) + "\n")
    npm_pk = sorted(f["package"] for f in facts if f["ecosystem"] == "npm" and "signal" not in f)
    signals = sorted((f["package"], f["signal"]) for f in facts if "signal" in f)
    # negative control: same signal scan on a lockfile without install scripts finds nothing
    neg = wd / "neg"
    write_tree(neg, {"package.json": json.dumps({"name": "n", "version": "1.0.0", "dependencies": {"left-pad": "^1.3.0"}}),
                     "package-lock.json": json.dumps(npm_lock({"left-pad": "1.3.0"}, set()))})
    _, nf, _ = deps_audit(neg)
    return [
        check("ecosystems discovered with npm lockfile flavor", sorted(eco) == ["go", "npm", "python", "rust"]
              and eco["npm"]["lockfile"] == "package-lock.json", sorted(eco), ["go", "npm", "python", "rust"]),
        check("npm ls (real tool) reports both lockfile packages", npm_pk == ["esbuild", "left-pad"], npm_pk),
        check("go list / cargo metadata (real tools) report the main modules",
              any(f["package"] == "example.test/svc" for f in facts) and any(f["package"] == "tool" for f in facts), True, True),
        check("supply-chain + pin signals found", signals == [("esbuild", "install script"), ("flask", "unpinned requirement")], signals),
        check("every claim carries an evidence tier", all(f["tier"] in ("TOOL-REPORTED", "INFERRED", "UNKNOWN") for f in facts), len(facts)),
        check("no invented advisories: no CVE/GHSA ids in report, gaps stated per ecosystem",
              not re.search(r"CVE-|GHSA-", rep.read_text()) and len(gaps) == 4, len(gaps), 4),
        check("non-destructive: repo bytes unchanged by the audit", before == after, True, True),
        check("negative control: lockfile without install scripts yields no install-script signal",
              not any(f.get("signal") == "install script" for f in nf), True, True),
    ], [rep]


# =====================================================================================================
# Static auditors (libGDX, OpenTelemetry, platform, PWA): seeded fixtures with known findings
# =====================================================================================================
def libgdx_audit(root: Path):
    out = []
    gradle = (root / "build.gradle").read_text() if (root / "build.gradle").exists() else ""
    gp = (root / "gradle.properties").read_text() if (root / "gradle.properties").exists() else ""
    m = re.search(r"gdxVersion\s*=\s*['\"]?([\d.]+)", gradle + "\n" + gp)
    if m and tuple(int(x) for x in m.group(1).split(".")) < (1, 14, 0):
        out.append(("project-setup", "libGDX version %s < 1.14.0" % m.group(1), "gradle.properties"))
    for f in sorted(root.rglob("*.java")):
        src = f.read_text()
        rel = str(f.relative_to(root))
        cls = re.search(r"class (\w+)", src)
        cname = cls.group(1) if cls else ""
        ctor = re.search(r"public %s\s*\([^)]*\)\s*\{(.*?)\n    \}" % cname, src, flags=re.S)
        if ctor and "setInputProcessor" in ctor.group(1):
            out.append(("screen-lifecycle", "setInputProcessor in constructor (belongs in show())", rel))
        if "implements Screen" in src and "setInputProcessor(null)" not in src:
            out.append(("screen-lifecycle", "no setInputProcessor(null) in hide()", rel))
        if re.search(r"static\s+(final\s+)?AssetManager", src):
            out.append(("assets", "static AssetManager", rel))
        if re.search(r"static\s+(final\s+)?(Texture|SpriteBatch|BitmapFont)\b", src):
            out.append(("disposal", "static field holding an OpenGL resource", rel))
        if re.search(r"new Texture\(", src):
            out.append(("assets", "direct new Texture() instead of AssetManager", rel))
        render = re.search(r"void render\([^)]*\)\s*\{(.*?)\n    \}", src, flags=re.S)
        if render:
            body = render.group(1)
            b0, b1 = body.find("batch.begin()"), body.find("batch.end()")
            if 0 <= b0 < b1 and "shapes.begin" in body[b0:b1]:
                out.append(("rendering", "ShapeRenderer used inside SpriteBatch begin/end", rel))
            if re.search(r"new (Texture|Pixmap|FrameBuffer|Vector2)\(", body):
                out.append(("performance", "per-frame allocation in render()", rel))
        for res in re.findall(r"(?:private|public)?\s*(?:SpriteBatch|ShapeRenderer|BitmapFont|Stage)\s+(\w+)\s*[;=]", src):
            if not re.search(r"\b%s\.dispose\(\)" % res, src):
                out.append(("disposal", "%s never disposed" % res, rel))
    return sorted(set(out))


GDX_BAD = {"gradle.properties": "gdxVersion=1.12.1\n", "build.gradle": "allprojects { }\n",
           "core/src/main/java/demo/GameScreen.java": """package demo;
import com.badlogic.gdx.*;
public class GameScreen implements Screen {
    static AssetManager assets = new AssetManager();
    private SpriteBatch batch = new SpriteBatch();
    private ShapeRenderer shapes = new ShapeRenderer();
    public GameScreen() {
        Gdx.input.setInputProcessor(new InputAdapter());
    }
    public void render(float delta) {
        Texture t = new Texture("hero.png");
        batch.begin();
        shapes.begin();
        shapes.end();
        batch.end();
    }
    public void dispose() {
        batch.dispose();
    }
}
"""}
GDX_GOOD = {"gradle.properties": "gdxVersion=1.14.0\n", "build.gradle": "allprojects { }\n",
            "core/src/main/java/demo/GameScreen.java": """package demo;
import com.badlogic.gdx.*;
public class GameScreen implements Screen {
    private final AssetManager assets;
    private SpriteBatch batch = new SpriteBatch();
    private ShapeRenderer shapes = new ShapeRenderer();
    public GameScreen(AssetManager assets) {
        this.assets = assets;
    }
    public void show() { Gdx.input.setInputProcessor(new InputAdapter()); }
    public void hide() { Gdx.input.setInputProcessor(null); }
    public void render(float delta) {
        batch.begin();
        batch.end();
        shapes.begin();
        shapes.end();
    }
    public void dispose() {
        batch.dispose();
        shapes.dispose();
    }
}
"""}


@card(KA("71-libgdx-development/125-libgdx-audit-workflow"))
def libgdx_audit_workflow(task, wd):
    write_tree(wd / "bad", GDX_BAD)
    write_tree(wd / "good", GDX_GOOD)
    fb, fg = libgdx_audit(wd / "bad"), libgdx_audit(wd / "good")
    cats = sorted({c for c, _, _ in fb})
    rep = ["# libGDX audit", ""] + ["- [%s] %s (%s)" % f for f in fb]
    r = tw(wd / "libgdx-audit.md", "\n".join(rep) + "\n")
    return [
        check("8 seeded defects found in the bad project", len(fb) == 8, len(fb), 8),
        check("findings span setup, lifecycle, assets, disposal, rendering, performance",
              cats == ["assets", "disposal", "performance", "project-setup", "rendering", "screen-lifecycle"], cats),
        check("shapes never disposed is caught", any("shapes never disposed" in m for _, m, _ in fb), True, True),
        check("negative control: corrected project yields zero findings", fg == [], fg, []),
    ], [r]


def otel_audit(path: Path):
    tree = ast.parse(path.read_text())
    out = []
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    for fn in funcs:
        for n in ast.walk(fn):
            if isinstance(n, ast.Call):
                name = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
                if name in ("TracerProvider",):
                    out.append(("sdk", "TracerProvider created inside %s() (per call)" % fn.name, n.lineno))
                if name == "TraceContextTextMapPropagator":
                    out.append(("propagation", "per-call propagator instantiation in %s()" % fn.name, n.lineno))
                if name == "start_span":
                    out.append(("span", "raw start_span instead of start_as_current_span", n.lineno))
                if name in ("start_as_current_span", "start_span") and n.args and isinstance(n.args[0], ast.JoinedStr):
                    out.append(("span", "high-cardinality span name (f-string)", n.lineno))
                if name == "set_status" and n.args and "OK" in ast.unparse(n.args[0]):
                    out.append(("span", "status explicitly set to OK on inner span", n.lineno))
                if name == "set_attribute" and n.args and isinstance(n.args[0], ast.Constant):
                    key = n.args[0].value
                    if re.search(r"email|password|ssn|phone", key):
                        out.append(("attributes", "PII attribute %s" % key, n.lineno))
                    elif re.search(r"[A-Z]", key):
                        out.append(("attributes", "non-semconv attribute %s" % key, n.lineno))
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            name = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
            if name == "SimpleSpanProcessor":
                out.append(("exporter", "SimpleSpanProcessor in production", n.lineno))
            if name == "JaegerExporter":
                out.append(("exporter", "Jaeger exporter (removed; use OTLP)", n.lineno))
            if name == "Resource" or (name == "create" and "Resource" in ast.unparse(n.func)):
                txt = ast.unparse(n)
                if "service.version" not in txt:
                    out.append(("sdk", "resource missing service.version", n.lineno))
    src = path.read_text()
    if "TracerProvider" in src and not re.search(r"atexit\.register|signal\.signal", src):
        out.append(("sdk", "no shutdown registered to flush spans", 0))
    return sorted(set(out), key=lambda x: (x[2], x[1]))


OTEL_BAD = '''from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

resource = Resource.create({"service.name": "orders"})


def handle(req):
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("orders")
    with tracer.start_as_current_span(f"order {req.id}") as span:
        span.set_attribute("user.email", req.email)
        span.set_attribute("httpMethod", "GET")
        span.set_status(trace.Status(trace.StatusCode.OK))
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
'''
OTEL_GOOD = '''import atexit
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

resource = Resource.create({"service.name": "orders", "service.version": "1.4.0"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(exporter))
atexit.register(provider.shutdown)
tracer = provider.get_tracer("orders")
PROPAGATOR = TraceContextTextMapPropagator()


def handle(req):
    with tracer.start_as_current_span("order.handle") as span:
        span.set_attribute("http.request.method", "GET")
        carrier = {}
        PROPAGATOR.inject(carrier)
'''


@card(KA("75-opentelemetry/138-otel-audit-workflow"))
def otel_audit_workflow(task, wd):
    b, g = tw(wd / "bad/app.py", OTEL_BAD), tw(wd / "good/app.py", OTEL_GOOD)
    fb, fg = otel_audit(b), otel_audit(g)
    sec = {"correctness": [f for f in fb if f[0] in ("propagation", "attributes", "span")],
           "performance": [f for f in fb if f[0] == "exporter" or "per call" in f[1]],
           "production-readiness": [f for f in fb if f[0] == "sdk"]}
    rep = jw(wd / "otel-audit.json", {"current_state": {"tracer_provider": True, "processor": "SimpleSpanProcessor"},
                                      **{k: [list(x) for x in v] for k, v in sec.items()}})
    msgs = [m for _, m, _ in fb]
    return [
        check("9 seeded OTel defects found", len(fb) == 9, len(fb), 9),
        check("PII attribute user.email flagged", any("user.email" in m for m in msgs), True, True),
        check("SimpleSpanProcessor + per-call TracerProvider + per-call propagator flagged",
              sum(any(k in m for m in msgs) for k in ("SimpleSpanProcessor", "TracerProvider created", "per-call propagator")) == 3, True, True),
        check("report has correctness/performance/production-readiness sections",
              all(sec[k] for k in sec), {k: len(v) for k, v in sec.items()}),
        check("negative control: corrected module yields zero findings", fg == [], fg, []),
    ], [rep]


def detect_platforms(root: Path):
    pkg = json.loads((root / "package.json").read_text()) if (root / "package.json").exists() else {}
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    found = []
    has_sw = bool(list(root.rglob("sw.js")) or list(root.rglob("service-worker.js")))
    has_manifest = bool(list(root.rglob("manifest.webmanifest")) or list(root.rglob("manifest.json")))
    if any(k in deps for k in ("react", "vue", "svelte")) and not has_sw:
        found.append("SPA")
    if has_manifest and has_sw:
        found.append("PWA")
    if any(k in deps for k in ("expo", "react-native", "@capacitor/core")):
        found.append("Mobile")
    if "electron" in deps:
        found.append("Electron")
    if "@tauri-apps/api" in deps and (root / "src-tauri").is_dir():
        found.append("Tauri")
    return found


def platform_findings(root: Path):
    out = []
    for f in sorted(p for p in root.rglob("*") if p.suffix in (".js", ".ts", ".json", ".html") and "node_modules" not in p.parts):
        rel = str(f.relative_to(root))
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if re.search(r"localStorage\.setItem\(['\"](jwt|token|access_token)", line):
                out.append(("CRITICAL", rel, i, "JWT stored in localStorage", "auth-tokens"))
            if re.search(r"nodeIntegration:\s*true", line):
                out.append(("CRITICAL", rel, i, "Electron nodeIntegration enabled", "platform-security"))
            if re.search(r"contextIsolation:\s*false", line):
                out.append(("CRITICAL", rel, i, "Electron contextIsolation disabled", "platform-security"))
            if re.search(r'"csp":\s*null', line):
                out.append(("HIGH", rel, i, "Tauri CSP disabled", "xss-csp"))
            if re.search(r"dangerouslySetInnerHTML", line):
                out.append(("HIGH", rel, i, "unsanitized HTML injection", "xss-csp"))
            if re.search(r"(API_KEY|SECRET)\s*=\s*['\"][A-Za-z0-9_-]{12,}", line):
                out.append(("CRITICAL", rel, i, "secret embedded in client bundle", "secrets-management"))
            if re.search(r"fetch\([^)]*\)\s*\.then", line) and "catch" not in line:
                out.append(("MEDIUM", rel, i, "fetch without error handling", "api-design"))
    return out


@card(KA("77-platform-engineering/142-platform-review-workflow"))
def platform_review(task, wd):
    root = wd / "repo"
    write_tree(root, {
        "package.json": json.dumps({"dependencies": {"react": "18.3.1", "@tauri-apps/api": "2.0.0"},
                                    "devDependencies": {"electron": "31.0.0"}}),
        "src-tauri/tauri.conf.json": '{\n  "app": {\n    "security": {\n      "csp": null\n    }\n  }\n}\n',
        "src/auth.js": "export function save(t){\n  localStorage.setItem('jwt', t);\n}\nconst API_KEY = 'sk_live_abcdef123456789';\n",
        "src/Feed.js": "export const Feed = ({html}) => <div dangerouslySetInnerHTML={{__html: html}} />;\n"
                       "fetch('/api/feed').then(r => r.json());\n",
        "electron/main.js": "new BrowserWindow({ webPreferences: { nodeIntegration: true, contextIsolation: false } });\n"})
    before = tree_digest(root)
    plats = detect_platforms(root)
    fnd = platform_findings(root)
    sev = {s: sum(1 for f in fnd if f[0] == s) for s in ("CRITICAL", "HIGH", "MEDIUM")}
    md = ["# Platform Review: repo (2026-11-03)", "", "## Detected platforms"] + ["- " + p for p in plats]
    md += ["", "## Summary", "- Critical issues: %d" % sev["CRITICAL"], "- High: %d" % sev["HIGH"], "- Medium: %d" % sev["MEDIUM"],
           "", "## Findings"]
    for s in ("CRITICAL", "HIGH", "MEDIUM"):
        md += ["### [%s]" % s] + ["- %s:%d %s. Rule: %s. Fix: see references/%s.md" % (f[1], f[2], f[3], f[4], f[4])
                                  for f in fnd if f[0] == s]
    md += ["", "## Auth posture", "- [%s] No JWT in localStorage" % ("x" if not any("JWT" in f[3] for f in fnd) else " ")]
    rep = tw(root / ".platform-review/REPORT.md", "\n".join(md) + "\n")
    shutil.copytree(root, wd / "after", ignore=shutil.ignore_patterns(".platform-review"))
    src_unchanged = tree_digest(wd / "after") == before
    # negative control: a hardened copy yields no findings
    hard = wd / "hard"
    write_tree(hard, {"package.json": json.dumps({"dependencies": {"react": "18.3.1"}}),
                      "src/auth.js": "export async function save(t){ await fetch('/session',{method:'POST',body:t}); }\n",
                      "electron/main.js": "new BrowserWindow({ webPreferences: { nodeIntegration: false, contextIsolation: true } });\n"})
    nf = platform_findings(hard)
    txt = rep.read_text()
    return [
        check("platform mix detected before reviewing", plats == ["SPA", "Electron", "Tauri"], plats, ["SPA", "Electron", "Tauri"]),
        check("severity counts: 4 critical, 2 high, 1 medium", sev == {"CRITICAL": 4, "HIGH": 2, "MEDIUM": 1}, sev),
        check("every finding cites file:line and rule", len(re.findall(r"^- \S+:\d+ .+ Rule: ", txt, flags=re.M)) == len(fnd), len(fnd)),
        check("report written to .platform-review/REPORT.md, sources never auto-fixed",
              rep.exists() and src_unchanged, True, True),
        check("negative control: hardened project has zero findings", nf == [], nf, []),
    ], [rep]


# ---------------------------------------------------------------------------------------------- PWA
PWA_BAD = {
    "public/manifest.webmanifest": json.dumps({"name": "Shop", "start_url": "/", "display": "standalone",
                                               "icons": [{"src": "/i192.png", "sizes": "192x192", "type": "image/png"}]}, indent=1),
    "src/sw.js": "self.addEventListener('install', e => {\n  self.skipWaiting();\n"
                 "  e.waitUntil(caches.open('static').then(c => c.addAll(['/', '/app.js'])));\n});\n"
                 "self.addEventListener('fetch', e => {\n  e.respondWith(fetch(e.request));\n});\n",
    "src/main.js": "navigator.serviceWorker.register('/sw.js');\nlocalStorage.setItem('catalog', JSON.stringify(bigCatalog));\n",
    "index.html": "<html><head><meta name=\"viewport\" content=\"width=device-width\"></head><body></body></html>\n",
    "nginx.conf": "add_header Content-Security-Policy \"script-src 'self' 'unsafe-inline'\";\n",
    "dist/sw.js": "self.skipWaiting();\n",
}
PWA_GOOD = {
    "public/manifest.webmanifest": json.dumps({"id": "/", "name": "Shop", "short_name": "Shop", "start_url": "/?source=pwa",
                                               "display": "standalone", "theme_color": "#123456", "icons": [
        {"src": "/i192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "/i512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, indent=1),
    "src/sw.js": "const V = 'static-v3';\nself.addEventListener('install', e => {\n"
                 "  e.waitUntil(caches.open(V).then(c => c.addAll(['/', '/offline.html'])));\n});\n"
                 "self.addEventListener('message', e => { if (e.data === 'SKIP_WAITING') self.skipWaiting(); });\n"
                 "self.addEventListener('fetch', e => {\n  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));\n});\n",
    "src/main.js": "navigator.serviceWorker.register('/sw.js');\nnavigator.serviceWorker.addEventListener('controllerchange', () => location.reload());\n",
    "index.html": "<html><head><meta name=\"viewport\" content=\"width=device-width\"><meta name=\"theme-color\" content=\"#123456\">"
                  "<meta name=\"apple-mobile-web-app-capable\" content=\"yes\"><meta name=\"apple-mobile-web-app-status-bar-style\" "
                  "content=\"default\"><meta name=\"apple-mobile-web-app-title\" content=\"Shop\"><link rel=\"apple-touch-icon\" "
                  "href=\"/a180.png\"></head><body></body></html>\n",
    "nginx.conf": "add_header Content-Security-Policy \"script-src 'self' 'nonce-abc'\";\nadd_header Strict-Transport-Security max-age=63072000;\n",
}


def _line(text, pat):
    for i, l in enumerate(text.splitlines(), 1):
        if re.search(pat, l):
            return i
    return 0


def pwa_audit(root: Path):
    srcs = {str(p.relative_to(root)): p.read_text() for p in sorted(root.rglob("*")) if p.is_file()
            and not ({"dist", "build", ".next"} & set(p.relative_to(root).parts))}
    crit, imp = [], []
    man_path = next(k for k in srcs if k.endswith(("manifest.webmanifest", "manifest.json")))
    man = json.loads(srcs[man_path])
    sw_path = next(k for k in srcs if re.search(r"(sw|service-worker)\.js$", k))
    sw = srcs[sw_path]
    allsrc = "\n".join(srcs.values())
    if "skipWaiting()" in sw and "controllerchange" not in allsrc:
        crit.append(("skipWaiting() without coordinated client reload", sw_path, _line(sw, r"skipWaiting")))
    m = re.search(r"caches\.open\('([^']+)'\)", sw)
    if m and "addAll" in sw and not re.search(r"v\d+|[0-9a-f]{8}", m.group(1)):
        crit.append(("precache list without version suffix", sw_path, _line(sw, r"addAll")))
    icons = man.get("icons", [])
    mask = {i["sizes"] for i in icons if "maskable" in i.get("purpose", "")}
    if man.get("display") == "standalone" and not {"192x192", "512x512"} <= mask:
        crit.append(("standalone manifest without maskable 192 and 512 icons", man_path, _line(srcs[man_path], r"icons")))
    for k, t in srcs.items():
        if re.search(r"script-src[^;\"]*'unsafe-inline'", t) and "nonce-" not in t:
            crit.append(("CSP allows 'unsafe-inline' for script-src", k, _line(t, r"unsafe-inline")))
    if re.search(r"respondWith\(fetch\(e(vent)?\.request\)\)", sw):
        imp.append(("fetch handler passes every request to network", sw_path, _line(sw, r"respondWith")))
    if "source=" not in str(man.get("start_url", "")):
        imp.append(("start_url lacks a tracking parameter", man_path, _line(srcs[man_path], r"start_url")))
    for k, t in srcs.items():
        if re.search(r"localStorage\.setItem\([^)]*JSON\.stringify", t):
            imp.append(("localStorage used for large data", k, _line(t, r"localStorage")))
    html = srcs.get("index.html", "")
    missing = [t for t in ("apple-mobile-web-app-capable", "apple-mobile-web-app-title", "apple-touch-icon", "theme-color") if t not in html]
    if missing:
        imp.append(("iOS meta block incomplete: " + ", ".join(missing), "index.html", 1))
    return crit, imp


@card(KA("79-pwa-expert/145-pwa-audit-workflow"))
def pwa_audit_workflow(task, wd):
    write_tree(wd / "bad", PWA_BAD)
    write_tree(wd / "good", PWA_GOOD)
    c, i = pwa_audit(wd / "bad")
    gc, gi = pwa_audit(wd / "good")
    md = ["# PWA Audit Report", "**Target:** bad", "**Mode:** local", "**Date:** 2026-11-03", "", "## Critical findings"]
    md += ["### C%d: %s\n- **Location:** %s:%d" % (n, t, f, l) for n, (t, f, l) in enumerate(c, 1)]
    md += ["", "## Important findings"] + ["### I%d: %s\n- **Location:** %s:%d" % (n, t, f, l) for n, (t, f, l) in enumerate(i, 1)]
    rep = tw(wd / "pwa-audit.md", "\n".join(md) + "\n")
    txt = rep.read_text()
    return [
        check("4 critical defects (skipWaiting, unversioned precache, maskable icons, unsafe-inline CSP)", len(c) == 4, [x[0] for x in c]),
        check("4 important defects", len(i) == 4, [x[0] for x in i]),
        check("stable numbering C1..C4, I1..I4 with file:line", all("### C%d:" % n in txt for n in range(1, 5))
              and all("### I%d:" % n in txt for n in range(1, 5)) and "src/sw.js:2" in txt, True, True),
        check("build artifact dist/ never audited", "dist/" not in txt, True, True),
        check("negative control: corrected PWA has zero findings", gc == [] and gi == [], [gc, gi], [[], []]),
    ], [rep]


PWA_ITEMS = [
    ("Manifest", "id is explicit", lambda s: '"id"' in s["man"]),
    ("Manifest", "name and short_name present", lambda s: all(k in json.loads(s["man"]) for k in ("name", "short_name"))),
    ("Manifest", "display is not browser", lambda s: json.loads(s["man"]).get("display") not in (None, "browser")),
    ("Manifest", "192 and 512 PNG icons", lambda s: {"192x192", "512x512"} <= {i["sizes"] for i in json.loads(s["man"]).get("icons", [])}),
    ("Manifest", "maskable icon present", lambda s: any("maskable" in i.get("purpose", "") for i in json.loads(s["man"]).get("icons", []))),
    ("iOS-specific", "apple-touch-icon link", lambda s: "apple-touch-icon" in s["html"]),
    ("iOS-specific", "apple-mobile-web-app-title", lambda s: "apple-mobile-web-app-title" in s["html"]),
    ("Service Worker", "registered", lambda s: "serviceWorker.register" in s["js"]),
    ("Service Worker", "has fetch handler", lambda s: "'fetch'" in s["sw"]),
    ("Service Worker", "versioned cache name", lambda s: bool(re.search(r"v\d+", s["sw"]))),
    ("Security", "HSTS header", lambda s: "Strict-Transport-Security" in s["conf"]),
    ("Security", "CSP without unsafe-eval", lambda s: "Content-Security-Policy" in s["conf"] and "unsafe-eval" not in s["conf"]),
    ("Push", "pushsubscriptionchange handled", lambda s: None if "pushManager" not in s["js"] else "pushsubscriptionchange" in s["sw"]),
]


def pwa_checklist(root: Path):
    s = {"man": (root / "public/manifest.webmanifest").read_text(), "html": (root / "index.html").read_text(),
         "js": (root / "src/main.js").read_text(), "sw": (root / "src/sw.js").read_text(), "conf": (root / "nginx.conf").read_text()}
    rows = []
    for cat, item, fn in PWA_ITEMS:
        r = fn(s)
        rows.append((cat, item, "N/A" if r is None else ("PASS" if r else "FAIL")))
    cats = []
    for cat in dict.fromkeys(c for c, _, _ in rows):
        p = sum(1 for c, _, r in rows if c == cat and r == "PASS")
        f = sum(1 for c, _, r in rows if c == cat and r == "FAIL")
        n = sum(1 for c, _, r in rows if c == cat and r == "N/A")
        cats.append((cat, p, f, n))
    P, F, N = (sum(x[i] for x in cats) for i in (1, 2, 3))
    md = ["# Production Checklist Report", "**Target:** %s" % root.name, "**Date:** 2026-11-03", "", "## Summary", "",
          "| Category | Pass | Fail | N/A | Score |", "|---|---|---|---|---|"]
    md += ["| %s | %d | %d | %d | %d / %d |" % (c, p, f, n, p, p + f) for c, p, f, n in cats]
    md += ["| **Overall** | %d | %d | %d | %d / %d |" % (P, F, N, P, P + F), ""]
    for cat in dict.fromkeys(c for c, _, _ in rows):
        md += ["## " + cat] + ["- [%s] %s" % (r, i) + ("" if r != "FAIL" else ". See references/manifest.md" if cat in
                               ("Manifest", "iOS-specific") else ". See references/%s.md" % cat.lower().replace(" ", "-"))
                               for c, i, r in rows if c == cat] + [""]
    return "\n".join(md), (P, F, N)


@card(KA("79-pwa-expert/146-pwa-checklist-workflow"))
def pwa_checklist_workflow(task, wd):
    write_tree(wd / "bad", PWA_BAD)
    write_tree(wd / "good", PWA_GOOD)
    r1, t1 = pwa_checklist(wd / "bad")
    r2, _ = pwa_checklist(wd / "bad")
    rg, tg = pwa_checklist(wd / "good")
    rep = tw(wd / "pwa-checklist.md", r1 + "\n")
    tw(wd / "pwa-checklist-good.md", rg + "\n")
    no_emoji = not re.search("[\U0001F300-\U0001FAFF✅❌]", r1)
    return [
        check("every checklist item walked once", len(re.findall(r"^- \[(PASS|FAIL|N/A)\]", r1, flags=re.M)) == len(PWA_ITEMS),
              len(PWA_ITEMS)),
        check("bad target totals: 4 pass / 8 fail / 1 N/A", t1 == (4, 8, 1), t1, (4, 8, 1)),
        check("deterministic: two runs byte-identical", r1 == r2, True, True),
        check("overall score row X / (X+Y)", "| **Overall** | 4 | 8 | 1 | 4 / 12 |" in r1, True, True),
        check("no emojis; text status only", no_emoji, True, True),
        check("negative control: corrected target has zero FAIL", tg[1] == 0, tg, "fail=0"),
    ], [rep]


# =====================================================================================================
# repo-hygiene tidy: detect C1/C2/C3/C5/C7, reversible apply (quarantine, explicit-path staging)
# =====================================================================================================
GARBAGE = re.compile(r"(^|/)(\.DS_Store|Thumbs\.db|nohup\.out|=|[0-9]|npm-debug\.log)$")
NEEDED_IGNORES = [".DS_Store", "node_modules/", "*.log"]


def tidy_detect(root: Path):
    tracked = git(root, "ls-files").stdout.split("\n")
    untracked = git(root, "ls-files", "--others", "--exclude-standard").stdout.split("\n")
    f = []
    for p in filter(None, tracked):
        if GARBAGE.search(p):
            f.append({"check": "C1", "path": p, "tracked": True, "evidence": "git ls-files: " + p})
    for p in filter(None, untracked):
        if GARBAGE.search(p):
            f.append({"check": "C1", "path": p, "tracked": False, "evidence": "git ls-files --others: " + p})
        elif p.split("/")[0] in ("tmp", "scratch", "out"):
            f.append({"check": "C5", "path": p, "tracked": False, "evidence": "git ls-files --others: " + p})
    pkg = json.loads((root / "package.json").read_text()) if (root / "package.json").exists() else {}
    for d in sorted({p.split("/")[0] for p in tracked if p.split("/")[0] in ("dist", "build", "coverage")}):
        published = d in pkg.get("files", []) or str(pkg.get("main", "")).startswith(d + "/")
        f.append({"check": "C2", "path": d + "/", "tracked": True, "published": published,
                  "disposition": "keep (publication check: package.json files/main)" if published else "untrack",
                  "evidence": "git ls-files %s/" % d})
    gi = (root / ".gitignore").read_text().splitlines() if (root / ".gitignore").exists() else []
    for pat in NEEDED_IGNORES:
        if pat not in gi:
            f.append({"check": "C3", "path": ".gitignore", "pattern": pat, "evidence": "pattern absent from .gitignore"})
    stashes = [s for s in git(root, "stash", "list").stdout.splitlines() if s]
    if stashes:
        f.append({"check": "C7", "path": "refs/stash", "count": len(stashes), "disposition": "detection-only",
                  "evidence": "git stash list: %d entries" % len(stashes)})
    return f


def tidy_apply(root: Path, findings, quarantine: Path):
    applied = []
    for x in findings:
        if x["check"] == "C1" and x["tracked"]:
            git(root, "rm", "-q", "--", x["path"])
            applied.append(("git rm", x["path"]))
        elif x["check"] in ("C1", "C5") and not x["tracked"]:
            dst = quarantine / x["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(root / x["path"]), str(dst))
            applied.append(("quarantine", x["path"]))
    pats = [x["pattern"] for x in findings if x["check"] == "C3"]
    if pats:
        with open(root / ".gitignore", "a", encoding="utf-8") as fh:
            fh.write("\n".join(pats) + "\n")
        applied.append(("append .gitignore", ",".join(pats)))
    for x in findings:
        if x["check"] == "C2" and not x.get("published"):
            git(root, "rm", "-r", "-q", "--cached", "--", x["path"])
            applied.append(("git rm --cached", x["path"]))
    return applied


@card(KA("83-repo-hygiene/166-tidy-workflow"))
def tidy_workflow(task, wd):
    root = git_repo(wd / "repo", {"src/app.py": "print(1)\n", ".DS_Store": "x", ".gitignore": "*.pyc\n",
                                  "dist/bundle.js": "var a;\n", "coverage/lcov.info": "TN:\n",
                                  "package.json": json.dumps({"name": "lib", "files": ["dist"], "main": "dist/bundle.js"})})
    tw(root / "src/app.py", "print(2)\n")
    git(root, "stash", "-q")
    tw(root / "nohup.out", "log\n")
    tw(root / "=", "")
    tw(root / "tmp/scratch.txt", "notes\n")
    before = tree_digest(root)
    found = tidy_detect(root)
    after_detect = tree_digest(root)
    applied = tidy_apply(root, found, wd / "quarantine")
    staged_cmds = [a for a, _ in applied]
    stash_after = len([s for s in git(root, "stash", "list").stdout.splitlines() if s])
    cats = sorted({x["check"] for x in found})
    rep = jw(wd / "tidy-report.json", {"findings": found, "applied": applied,
                                       "deliberately_kept": [x["path"] for x in found if x.get("published")]})
    post = tidy_detect(root)
    return [
        check("detect finds C1, C2, C3, C5, C7", cats == ["C1", "C2", "C3", "C5", "C7"], cats),
        check("detection is the default: tree unchanged after detect", before == after_detect, True, True),
        check("every finding quotes its evidence", all(x.get("evidence") for x in found), len(found)),
        check("published dist/ kept by the publication check; coverage/ untracked",
              ("git rm --cached", "coverage/") in applied and not any(p == "dist/" for _, p in applied), applied),
        check("untracked garbage quarantined, never deleted",
              (wd / "quarantine/nohup.out").exists() and (wd / "quarantine/tmp/scratch.txt").exists(), True, True),
        check("git-state (C7) never applied: stash still present", stash_after == 1, stash_after, 1),
        check("negative control: after apply, rerun finds no C1/C3/C5", not [x for x in post if x["check"] in ("C1", "C3", "C5")],
              [x["check"] for x in post], "only C2(kept)/C7"),
    ], [rep]


# =====================================================================================================
# bootstrap-project / refresh-project-scaffolding: detection tables, overlap rules, template checks
# =====================================================================================================
def detect_project_type(root: Path):
    has = lambda p: (root / p).exists()
    files = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
             and not ({"node_modules", "vendor", ".lake", ".yarn"} & set(p.relative_to(root).parts))]
    types = []
    if has("go.mod"):
        types.append("Go CLI" if has("main.go") or has("cmd") else "Go library")
    if has("package.json") and any(f.endswith((".js", ".ts", ".tsx", ".jsx")) for f in files):
        types.append("JavaScript/TypeScript")
    if any(has(p) for p in ("pyproject.toml", "setup.py", "requirements.txt")):
        types.append("Python")
    if has("Cargo.toml"):
        cargo = (root / "Cargo.toml").read_text()
        types.append("Rust CLI" if has("src/main.rs") or list(root.glob("src/bin/*.rs")) or "[[bin]]" in cargo else "Rust library")
    if has("build.zig"):
        types.append("Zig CLI")
    return types or ["New/empty repo"]


BOOT_ORDER = ["scaffold-new-repo", "scaffold-go-cli", "scaffold-go-library", "scaffold-rust-cli", "set-up-ci", "set-up-linters",
              "set-up-secret-scanning", "add-goreleaser-homebrew", "add-community-files", "set-up-installers",
              "add-scrut-cli-tests", "set-up-review-config", "pin-everything"]


def bootstrap_plan(root: Path):
    types = detect_project_type(root)
    has = lambda p: (root / p).exists()
    plan = {}
    plan["scaffold-new-repo"] = "full" if not (has("LICENSE") and has("README.md")) else "skip (exists)"
    lang = {"Go CLI": "scaffold-go-cli", "Go library": "scaffold-go-library", "Rust CLI": "scaffold-rust-cli"}
    scaff = next((lang[t] for t in types if t in lang), None)
    if scaff and not has(".github/workflows/ci.yml"):
        plan[scaff] = "run"
        plan["scaffold-new-repo"] = "scoped: agent config only"
    ci_covered = scaff in ("scaffold-go-cli", "scaffold-go-library", "scaffold-rust-cli") and plan.get(scaff) == "run"
    plan["set-up-ci"] = "skip (included in %s)" % scaff if ci_covered else ("skip (exists)" if has(".github/workflows/ci.yml") else "run")
    plan["set-up-linters"] = {"scaffold-go-library": "scoped: cross-language only", "scaffold-rust-cli": "scoped: cross-language only",
                              "scaffold-go-cli": "scoped: .golangci.yml + cross-language"}.get(scaff if ci_covered else None, "run")
    plan["set-up-secret-scanning"] = "run"
    is_cli = any(t.endswith("CLI") for t in types)
    if "Go CLI" in types:
        plan["add-goreleaser-homebrew"] = "skip (included in scaffold-go-cli)" if ci_covered else "run"
    else:
        plan["add-goreleaser-homebrew"] = "n/a"
    plan["add-community-files"] = "skip (exists)" if has("CONTRIBUTING.md") else "run"
    plan["set-up-installers"] = "run" if is_cli else "n/a (not a CLI)"
    plan["add-scrut-cli-tests"] = "run" if is_cli else "n/a (not a CLI)"
    plan["set-up-review-config"] = "run"
    plan["pin-everything"] = "scoped: --scope dependabot"
    order = [t for t in BOOT_ORDER if t in plan]
    return types, order, plan


ACTION_TARGET = {"actions/checkout": "v6", "actions/setup-go": "v6", "actions/setup-node": "v6",
                 "actions/upload-artifact": "v7", "golangci/golangci-lint-action": "v9", "goreleaser/goreleaser-action": "v7"}


def refresh_audit(root: Path):
    import yaml
    has = lambda p: (root / p).exists()
    tools = []
    if has("LICENSE") and has("README.md") and has(".gitignore"):
        tools.append("scaffold-new-repo")
    if has(".github/workflows/ci.yml"):
        tools.append("set-up-ci")
    if has(".editorconfig") or has(".prettierrc.json") or has(".golangci.yml"):
        tools.append("set-up-linters")
    out = []
    if "set-up-ci" in tools:
        raw = (root / ".github/workflows/ci.yml").read_text()
        ci = yaml.safe_load(raw)
        for i, line in enumerate(raw.splitlines(), 1):
            m = re.search(r"uses:\s*([\w./-]+)@([\w.]+)", line)
            if m and m.group(1) in ACTION_TARGET and not re.fullmatch(r"[0-9a-f]{40}", m.group(2)):
                want = ACTION_TARGET[m.group(1)]
                if int(re.sub(r"\D", "", m.group(2)) or 0) < int(want[1:]):
                    out.append(("set-up-ci", "ci.yml:%d" % i, "%s@%s -> %s" % (m.group(1), m.group(2), want)))
        if "permissions" not in ci:
            out.append(("set-up-ci", "ci.yml", "missing top-level permissions"))
        if "concurrency" not in ci:
            out.append(("set-up-ci", "ci.yml", "missing concurrency block"))
        for j, spec in (ci.get("jobs") or {}).items():
            if "timeout-minutes" not in spec:
                out.append(("set-up-ci", "ci.yml", "job %s missing timeout-minutes" % j))
    if has("Makefile"):
        mk = (root / "Makefile").read_text()
        if ".PHONY" not in mk:
            out.append(("set-up-ci", "Makefile", "no .PHONY declarations"))
        if not re.search(r"^help:", mk, flags=re.M):
            out.append(("set-up-ci", "Makefile", "no help target"))
    if "scaffold-new-repo" in tools:
        gi = (root / ".gitignore").read_text().split()
        for pat in ("*.exe", "*.test", "*.out", "bin/", "dist/"):
            if has("go.mod") and pat not in gi:
                out.append(("scaffold-new-repo", ".gitignore", "missing Go pattern " + pat))
    if not has(".github/dependabot.yml") and not has(".github/dependabot.yaml"):
        out.append(("pin-everything", ".github/dependabot.yml", "missing Dependabot config (SHA pins go stale)"))
    return tools, out


CI_OLD = """name: ci
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with: {go-version-file: go.mod}
"""
CI_NEW = """name: ci
on: [push]
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-go@v6
        with: {go-version-file: go.mod}
"""


@card(KA("943-bootstrap-project/2228-bootstrap-project"))
def bootstrap_project(task, wd):
    write_tree(wd / "gocli", {"go.mod": "module x\n", "main.go": "package main\n"})
    write_tree(wd / "golib", {"go.mod": "module y\n", "lib.go": "package y\n"})
    write_tree(wd / "rslib", {"Cargo.toml": "[package]\nname='z'\n", "src/lib.rs": ""})
    write_tree(wd / "web", {"package.json": "{}", "src/index.ts": "", "node_modules/a/x.go": "", "LICENSE": "MIT", "README.md": "#",
                            ".github/workflows/ci.yml": "on: push\n"})
    res = {n: bootstrap_plan(wd / n) for n in ("gocli", "golib", "rslib", "web")}
    rep = jw(wd / "bootstrap-plans.json", {n: {"types": t, "order": o, "plan": p} for n, (t, o, p) in res.items()})
    t, o, p = res["gocli"]
    naive = {k: "run" for k in BOOT_ORDER}
    violations = lambda pl: [k for k in ("set-up-ci", "add-goreleaser-homebrew") if pl.get(k) == "run"
                             and pl.get("scaffold-go-cli") == "run"]
    return [
        check("project types detected (node_modules excluded)",
              [res[n][0] for n in ("gocli", "golib", "rslib", "web")] == [["Go CLI"], ["Go library"], ["Rust library"],
                                                                         ["JavaScript/TypeScript"]],
              [res[n][0] for n in ("gocli", "golib", "rslib", "web")]),
        check("Go CLI: set-up-ci and goreleaser skipped (included), new-repo scoped to agent config",
              p["set-up-ci"].startswith("skip") and p["add-goreleaser-homebrew"].startswith("skip")
              and p["scaffold-new-repo"] == "scoped: agent config only", p),
        check("Go library: installers n/a, linters cross-language only",
              res["golib"][2]["set-up-installers"].startswith("n/a") and res["golib"][2]["set-up-linters"] == "scoped: cross-language only",
              res["golib"][2]),
        check("execution order: foundation first, review-config then pin-everything last",
              o[0] == "scaffold-new-repo" and o[-2:] == ["set-up-review-config", "pin-everything"], o),
        check("existing infra respected (web: LICENSE/README/CI exist)",
              res["web"][2]["scaffold-new-repo"] == "skip (exists)" and res["web"][2]["set-up-ci"] == "skip (exists)", res["web"][2]),
        check("negative control: naive run-everything plan violates the overlap rules", violations(dict(naive, **{"scaffold-go-cli": "run"}))
              == ["set-up-ci", "add-goreleaser-homebrew"] and violations(p) == [], True, True),
    ], [rep]


@card(KA("963-refresh-project-scaffolding/2247-refresh-project-scaffolding"))
def refresh_scaffolding(task, wd):
    base = {"go.mod": "module x\n", "main.go": "package main\n", "LICENSE": "MIT", "README.md": "#", ".editorconfig": "root = true\n"}
    write_tree(wd / "old", {**base, ".gitignore": "*.exe\n", ".github/workflows/ci.yml": CI_OLD, "Makefile": "build:\n\tgo build\n"})
    write_tree(wd / "new", {**base, ".gitignore": "*.exe\n*.test\n*.out\nbin/\ndist/\n", ".github/workflows/ci.yml": CI_NEW,
                            ".github/dependabot.yml": "version: 2\n",
                            "Makefile": ".PHONY: help build\nhelp:\n\t@echo help\nbuild:\n\tgo build\n"})
    tools, out = refresh_audit(wd / "old")
    tn, on = refresh_audit(wd / "new")
    rep = jw(wd / "refresh-plan.json", {"detected_tools": tools, "updates": out, "already_up_to_date": tn if not on else []})
    whats = [w for _, _, w in out]
    return [
        check("tools detected from signature artifacts", tools == ["scaffold-new-repo", "set-up-ci", "set-up-linters"], tools),
        check("outdated actions flagged against the version table",
              "actions/checkout@v4 -> v6" in whats and "actions/setup-go@v5 -> v6" in whats, whats[:2]),
        check("ci.yml structure checks: permissions, concurrency, timeout", all(any(k in w for w in whats) for k in
              ("permissions", "concurrency", "timeout-minutes")), True, True),
        check("12 update items in total", len(out) == 12, len(out), 12),
        check("negative control: an up-to-date repo needs no updates", on == [], on, []),
    ], [rep]


# =====================================================================================================
# review-dependabot-config: offline coverage matrix (manifests/workflows/actions vs configured entries)
# =====================================================================================================
MANIFEST_ECO = {"package-lock.json": "npm", "yarn.lock": "npm", "pnpm-lock.yaml": "npm", "uv.lock": "uv",
                "requirements.txt": "pip", "go.mod": "gomod", "Cargo.toml": "cargo", "Gemfile": "bundler", "Dockerfile": "docker"}
EXCL = {".git", "node_modules", "vendor", "dist", "build", "target", ".venv", ".yarn", "testdata"}


def dependabot_review(root: Path):
    import yaml
    inv = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if not p.is_file() or EXCL & set(rel.parts):
            continue
        d = "/" if str(rel.parent) == "." else "/" + str(rel.parent)
        if p.name in MANIFEST_ECO:
            inv.setdefault(MANIFEST_ECO[p.name], set()).add(d)
        if (rel.parts[:2] == (".github", "workflows") and p.suffix in (".yml", ".yaml")) or p.name in ("action.yml", "action.yaml"):
            if "uses:" in p.read_text():
                inv.setdefault("github-actions", set()).add("/" if rel.parts[:2] == (".github", "workflows") else d)
    cfgp = next((root / ".github" / n for n in ("dependabot.yml", "dependabot.yaml") if (root / ".github" / n).exists()), None)
    cfg = yaml.safe_load(cfgp.read_text()) if cfgp else {"updates": []}
    conf = {}
    for u in cfg.get("updates", []):
        dirs = u.get("directories") or [u.get("directory", "/")]
        conf.setdefault(u["package-ecosystem"], set()).update(dirs)
    findings, matrix = [], []
    for eco in sorted(set(inv) | set(conf)):
        found, have = inv.get(eco, set()), conf.get(eco, set())
        status = "covered" if found and found <= have else ("missing" if not have else ("stale" if not found else "partial"))
        matrix.append({"ecosystem": eco, "found": sorted(found), "configured": sorted(have), "status": status})
        if status == "missing":
            findings.append(("Errors", "Coverage", "%s not configured; manifests at %s" % (eco, ", ".join(sorted(found)))))
        elif status == "partial":
            findings.append(("Errors", "Coverage", "%s directories not listed: %s" % (eco, ", ".join(sorted(found - have)))))
        elif status == "stale":
            findings.append(("Errors", "Coverage", "%s entry targets %s but no manifest exists" % (eco, ", ".join(sorted(have)))))
    for u in cfg.get("updates", []):
        if "reviewers" in u:
            findings.append(("Warnings", "Validity", "%s uses deprecated reviewers; use CODEOWNERS" % u["package-ecosystem"]))
        if not u.get("groups"):
            findings.append(("Suggestions", "Grouping", "%s has no groups" % u["package-ecosystem"]))
    untracked = [str(p.relative_to(root)) for n in (".tool-versions", ".nvmrc", ".python-version") for p in root.glob(n)]
    return matrix, findings, untracked


@card(KA("968-review-dependabot-config/2252-review-dependabot-config"))
def review_dependabot(task, wd):
    root = wd / "repo"
    files = {"package-lock.json": "{}", "uv.lock": "", "web/package-lock.json": "{}", "node_modules/x/package-lock.json": "{}",
             ".github/workflows/ci.yml": "jobs: {t: {steps: [{uses: actions/checkout@v6}]}}\n",
             ".github/actions/setup/action.yml": "runs:\n  steps:\n    - uses: actions/cache@v4\n", ".nvmrc": "22\n",
             ".github/dependabot.yml": "version: 2\nupdates:\n  - package-ecosystem: npm\n    directory: /\n    schedule: {interval: weekly}\n"
                                      "  - package-ecosystem: pip\n    directory: /\n    schedule: {interval: weekly}\n"
                                      "    reviewers: [octo]\n  - package-ecosystem: github-actions\n    directory: /\n"
                                      "    schedule: {interval: weekly}\n    groups: {actions: {patterns: ['*']}}\n"}
    write_tree(root, files)
    matrix, findings, untracked = dependabot_review(root)
    st = {m["ecosystem"]: m["status"] for m in matrix}
    md = ["## Dependabot config review: repo (2026-11-03)", "", "Settings: UNKNOWN (GitHub API not reachable offline)", "",
          "### Coverage", "| Ecosystem | Found | Configured | Status |", "|---|---|---|---|"]
    md += ["| %s | %s | %s | %s |" % (m["ecosystem"], ", ".join(m["found"]), ", ".join(m["configured"]), m["status"]) for m in matrix]
    for sev in ("Errors", "Warnings", "Suggestions"):
        md += ["", "### " + sev] + ["%d. **%s**: %s" % (n, c, t) for n, (s, c, t) in enumerate(findings, 1) if s == sev]
    md += ["", "### Untracked surfaces"] + ["- " + u for u in untracked]
    rep = tw(wd / "dependabot-review.md", "\n".join(md) + "\n")
    # negative control: fix the config per the findings and re-review
    tw(root / ".github/dependabot.yml", "version: 2\nupdates:\n" + "".join(
        "  - package-ecosystem: %s\n    directories: %s\n    schedule: {interval: weekly}\n    groups: {all: {patterns: ['*']}}\n"
        % (e, json.dumps(d)) for e, d in [("npm", ["/", "/web"]), ("uv", ["/"]), ("github-actions", ["/", "/.github/actions/setup"])]))
    m2, f2, _ = dependabot_review(root)
    return [
        check("coverage statuses: npm partial (/web), uv missing, pip stale, actions partial (composite action)",
              st == {"npm": "partial", "uv": "missing", "pip": "stale", "github-actions": "partial"}, st),
        check("node_modules manifests excluded from inventory",
              all("/node_modules" not in d for m in matrix for d in m["found"]), True, True),
        check("deprecated reviewers flagged; ungrouped ecosystems suggested",
              sum(1 for s, _, _ in findings if s == "Warnings") == 1 and sum(1 for s, _, _ in findings if s == "Suggestions") == 2,
              [s for s, _, _ in findings]),
        check("untracked runtime pin .nvmrc listed", untracked == [".nvmrc"], untracked),
        check("negative control: corrected config -> all covered, zero findings",
              all(m["status"] == "covered" for m in m2) and f2 == [], [m["status"] for m in m2]),
    ], [rep]


# =====================================================================================================
# review-plan: deterministic target selection (branch/plan subject normalisation, done/ exclusion)
# =====================================================================================================
def norm_subject(s):
    s = re.sub(r"[^a-z0-9]+", "-", re.sub(r"[A-Z]", lambda m: m.group(0).lower(), s))
    return s.strip("-")


def branch_subject(b):
    b = re.sub(r"^(feature|feat|fix|chore|docs)/", "", b, count=1)
    b = re.sub(r"^(issue-)?[0-9]+-", "", b, count=1)
    return norm_subject(b)


def plan_subject(name):
    n = re.sub(r"\.md$", "", name)
    n = re.sub(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-", "", n, count=1)
    n = re.sub(r"^(issue-)?[0-9]+-", "", n, count=1)
    return norm_subject(n)


def select_plan(repo: Path, branch):
    repo = repo.resolve()
    todo = repo / "docs/plans/todo"
    done_dirs = [p.resolve() for p in (repo / "docs/plans").rglob("done") if p.is_dir()]
    cands, excluded = [], []
    for p in sorted(todo.rglob("*.md")) if todo.exists() else []:
        r = p.resolve()
        if repo not in r.parents or any(d == r or d in r.parents for d in done_dirs) or "done" in p.relative_to(todo).parts:
            excluded.append(str(p.relative_to(repo)))
            continue
        cands.append(p)
    if not cands:
        return None, "Blocked: no readable Markdown plan", excluded
    if branch:
        bs = branch_subject(branch)
        m = [p for p in cands if plan_subject(p.name) == bs]
        if len(m) == 1:
            return m[0].relative_to(repo), "unique subject match '%s'" % bs, excluded
    newest = sorted(cands, key=lambda p: (-p.stat().st_mtime, str(p.relative_to(repo))))[0]
    return newest.relative_to(repo), "no unique match; newest by mtime (ties by path)", excluded


@card(KA("969-review-plan/2253-review-plan"))
def review_plan(task, wd):
    repo = git_repo(wd / "repo", {"README.md": "#\n", "src/cache.py": "x = 1\n"})
    t = 1_700_000_000
    plans = {"docs/plans/todo/2026-10-01-123-add-cache.md": t, "docs/plans/todo/2026-10-20-rate-limit.md": t + 100,
             "docs/plans/todo/zeta.md": t + 50, "docs/plans/done/2026-11-01-add-cache-old.md": t + 500,
             "docs/plans/todo/b-tie.md": t + 900, "docs/plans/todo/a-tie.md": t + 900}
    for rel, mt in plans.items():
        tw(repo / rel, "# Plan\n\nTouches `src/cache.py`.\n")
        os.utime(repo / rel, (mt, mt))
    os.symlink(repo / "docs/plans/done/2026-11-01-add-cache-old.md", repo / "docs/plans/todo/link-to-done.md")
    git(repo, "checkout", "-q", "-b", "feature/123-add-cache")
    b1 = git(repo, "branch", "--show-current").stdout.strip()
    s1, why1, ex1 = select_plan(repo, b1)
    s2, why2, _ = select_plan(repo, "hotfix/123-add-cache")
    s3, why3, _ = select_plan(repo, None)
    empty = git_repo(wd / "empty", {"README.md": "#\n"})
    s4, why4, _ = select_plan(empty, "main")
    rep = jw(wd / "selection.json", {"branch": b1, "selected": str(s1), "reason": why1, "excluded": ex1,
                                     "hotfix": [str(s2), why2], "detached": [str(s3), why3], "empty": why4})
    return [
        check("normalisation examples from the skill", branch_subject("feature/123-foo") == "foo"
              and branch_subject("hotfix/123-foo") == "hotfix-123-foo", [branch_subject("feature/123-foo"), branch_subject("hotfix/123-foo")]),
        check("unique subject match wins even though newer plans exist",
              str(s1) == "docs/plans/todo/2026-10-01-123-add-cache.md", str(s1)),
        check("symlink into done/ is excluded and disclosed", ex1 == ["docs/plans/todo/link-to-done.md"], ex1),
        check("negative control: unlisted category keeps its prefix -> no match -> newest with path tie-break",
              str(s2) == "docs/plans/todo/a-tie.md" and "newest" in why2, [str(s2), why2]),
        check("no branch info -> newest fallback", str(s3) == "docs/plans/todo/a-tie.md", str(s3)),
        check("no candidates -> Blocked (never searches done/)", s4 is None and why4.startswith("Blocked"), why4),
    ], [rep]


# =====================================================================================================
# Scaffolders: render the skills' own reference templates, then prove the tree with real toolchains
# =====================================================================================================
PLACEHOLDER_RE = re.compile(r"\b(PROJECT-NAME|PROJECT-DESCRIPTION|GITHUB-USERNAME|COPYRIGHT-HOLDER|PACKAGE-NAME|PROJECT-TITLE|"
                            r"SHORT-DESCRIPTION|INSTALLATION-PLACEHOLDER)\b|\bYEAR\b")
IDENT = {"PROJECT-NAME": "tally", "PROJECT-DESCRIPTION": "count lines in files", "GITHUB-USERNAME": "octo-dev",
         "COPYRIGHT-HOLDER": "Fixture Dev", "PACKAGE-NAME": "tally", "PROJECT-TITLE": "Tally", "YEAR": "2026",
         "SHORT-DESCRIPTION": "count lines in files", "INSTALLATION-PLACEHOLDER": "go install github.com/octo-dev/tally@latest"}


def render(skill_dir: Path, mapping: dict, out: Path, extra: dict = None):
    files = {}
    for dest, (ref, idx) in mapping.items():
        files[dest] = tmpl(skill_dir / "references" / ref, IDENT, idx)
    files.update(extra or {})
    write_tree(out, files)
    return files


def leftover_placeholders(root: Path):
    hits = []
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.relative_to(root).parts and p.suffix not in (".sum",):
            for m in PLACEHOLDER_RE.finditer(p.read_text(errors="replace")):
                hits.append("%s:%s" % (p.relative_to(root), m.group(0)))
    return hits


def yaml_ok(paths):
    import yaml
    bad = []
    for p in paths:
        try:
            yaml.safe_load(Path(p).read_text())
        except Exception as exc:
            bad.append("%s: %s" % (Path(p).name, str(exc)[:80]))
    return bad


def make_targets(mk: Path):
    return set(re.findall(r"^([A-Za-z][\w-]*):", mk.read_text(), flags=re.M))


GO_ENV = {"GOFLAGS": "-mod=mod", "GOPROXY": "off", "GOTOOLCHAIN": "local", "GOWORK": "off"}


@card(KA("970-scaffold-go-cli/2254-scaffold-go-cli"))
def scaffold_go_cli(task, wd):
    sd = ATLAS / "970-scaffold-go-cli/2254-scaffold-go-cli"
    root = wd / "tally"
    mapping = {"main.go": ("main-go.md", 0), "cmd/root.go": ("root-go-without-viper.md", 0), "Makefile": ("makefile.md", 0),
               ".gitignore": ("gitignore.md", 0), ".goreleaser.yml": ("goreleaser.md", 0),
               ".github/workflows/ci.yml": ("ci-workflow.md", 0), ".github/workflows/release.yml": ("release-workflow.md", 0),
               "LICENSE": ("license.md", 0), "README.md": ("readme.md", 0)}
    render(sd, mapping, root, {"CHANGELOG.md": "# Changelog\n\n## [Unreleased]\n", "internal/.gitkeep": "",
                               "docs/plans/.gitkeep": "", "tests/.gitkeep": ""})
    git(root, "init", "-q", "-b", "main")
    sh(["go", "mod", "init", "github.com/octo-dev/tally"], root, **GO_ENV)
    gof = sh(["gofmt", "-l", "-e", "."], root, ok=False)
    build = sh(["go", "build", "./..."], root, ok=False, **GO_ENV)
    missing = sorted(set(re.findall(r"(github\.com/[\w./-]+)", build.stderr)) - {"github.com/octo-dev/tally/cmd"})
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "feat: scaffold tally CLI")
    files = git(root, "ls-files").stdout.split()
    tg = make_targets(root / "Makefile")
    raw = tmpl(sd / "references/main-go.md")
    note = tw(wd / "BUILD_NOTE.md", "go build stops only at the network dependency: %s (module cache empty, GOPROXY off).\n"
              % ", ".join(missing))
    return [
        check("every template placeholder substituted", leftover_placeholders(root) == [], leftover_placeholders(root)[:5], []),
        check("negative control: raw template still holds placeholders", bool(PLACEHOLDER_RE.search(raw)), True, True),
        check("gofmt parses and accepts main.go and cmd/root.go", gof.returncode == 0 and gof.stdout.strip() == "", gof.stdout + gof.stderr, ""),
        check("YAML files parse (goreleaser, ci, release)", yaml_ok([root / ".goreleaser.yml", root / ".github/workflows/ci.yml",
                                                                     root / ".github/workflows/release.yml"]) == [], True, True),
        check("Makefile has the Go CLI targets", {"build", "test", "lint", "vet", "fmt", "vuln", "clean", "help"} <= tg, sorted(tg)),
        check("go build fails only on the cobra download (scaffold itself consistent)",
              build.returncode != 0 and missing == ["github.com/spf13/cobra"], missing, ["github.com/spf13/cobra"]),
        check("initial commit holds the scaffold", {"main.go", "cmd/root.go", "go.mod", "LICENSE"} <= set(files), len(files)),
    ], [root / "main.go", root / "cmd/root.go", note]


@card(KA("971-scaffold-go-library/2255-scaffold-go-library"))
def scaffold_go_library(task, wd):
    sd = ATLAS / "971-scaffold-go-library/2255-scaffold-go-library"
    root = wd / "tally"
    mapping = {"doc.go": ("doc-go.md", 0), "tally.go": ("package-file.md", 0), "Makefile": ("makefile.md", 0),
               ".gitignore": ("gitignore.md", 0), ".golangci.yml": ("golangci.md", 0), ".editorconfig": ("editorconfig.md", 0),
               ".github/workflows/ci.yml": ("ci-workflow.md", 0), "LICENSE": ("license.md", 0), "README.md": ("readme.md", 0)}
    render(sd, mapping, root, {"tally_test.go": "package tally\n\nimport \"testing\"\n\nfunc TestVersion(t *testing.T) {\n"
                                                "\tif Version != \"0.0.0-dev\" {\n\t\tt.Fatalf(\"got %q\", Version)\n\t}\n}\n"})
    git(root, "init", "-q", "-b", "main")
    sh(["go", "mod", "init", "github.com/octo-dev/tally"], root, **GO_ENV)
    b = sh(["go", "build", "./..."], root, ok=False, **GO_ENV)
    v = sh(["go", "vet", "./..."], root, ok=False, **GO_ENV)
    t = sh(["go", "test", "./..."], root, ok=False, **GO_ENV)
    fmt_ok = sh(["make", "fmt"], root, ok=False, **GO_ENV)
    doc = sh(["go", "doc", "."], root, ok=False, **GO_ENV)
    tw(root / "bad.go", "package tally\nfunc  Bad( ) {}\n")
    fmt_bad = sh(["make", "fmt"], root, ok=False, **GO_ENV)
    (root / "bad.go").unlink()
    return [
        check("placeholders substituted", leftover_placeholders(root) == [], leftover_placeholders(root)[:5], []),
        check("go build ./... succeeds", b.returncode == 0, b.stderr[-200:], 0),
        check("go vet ./... clean", v.returncode == 0, v.stderr[-200:], 0),
        check("go test ./... passes", t.returncode == 0 and "ok" in t.stdout, t.stdout[-120:]),
        check("template's make fmt target passes on the scaffold", fmt_ok.returncode == 0, fmt_ok.returncode, 0),
        check("package doc from doc.go is the godoc package comment", "count lines in files" in doc.stdout, doc.stdout[:80]),
        check("negative control: make fmt fails on an unformatted file", fmt_bad.returncode != 0, fmt_bad.returncode, "!=0"),
        check("YAML parses (ci, golangci)", yaml_ok([root / ".github/workflows/ci.yml", root / ".golangci.yml"]) == [], True, True),
    ], [root / "doc.go", root / "tally.go", root / "Makefile"]


@card(KA("974-scaffold-rust-cli/2258-scaffold-rust-cli"))
def scaffold_rust_cli(task, wd):
    sd = ATLAS / "974-scaffold-rust-cli/2258-scaffold-rust-cli"
    root = wd / "tally"
    mapping = {"Cargo.toml": ("cargo-toml.md", 0), "src/main.rs": ("main-rs.md", 0), "Makefile": ("makefile.md", 0),
               ".gitignore": ("gitignore.md", 0), "rustfmt.toml": ("rustfmt.md", 0), "deny.toml": ("deny.md", 0),
               "typos.toml": ("typos.md", 0), "cliff.toml": ("cliff.md", 0), ".github/workflows/ci.yml": ("ci-workflow.md", 0),
               "LICENSE": ("license.md", 0), "README.md": ("readme.md", 0)}
    render(sd, mapping, root)
    git(root, "init", "-q", "-b", "main")
    import tomllib
    toml_bad = []
    for n in ("Cargo.toml", "rustfmt.toml", "deny.toml", "typos.toml", "cliff.toml"):
        try:
            tomllib.loads((root / n).read_text())
        except Exception as exc:
            toml_bad.append("%s: %s" % (n, exc))
    b = sh(["cargo", "build", "--offline", "--quiet"], root, ok=False, timeout=120)
    exe = root / "target/debug/tally"
    out = sh([exe], root, ok=False).stdout if exe.exists() else ""
    fmtc = sh(["cargo", "fmt", "--check"], root, ok=False) if shutil.which("rustfmt") else None
    tw(root / "src/main.rs", "fn main(){println!(\"x\");}\n")
    fmtn = sh(["cargo", "fmt", "--check"], root, ok=False) if shutil.which("rustfmt") else None
    tw(root / "src/main.rs", tmpl(sd / "references/main-rs.md"))
    checks = [
        check("placeholders substituted", leftover_placeholders(root) == [], leftover_placeholders(root)[:5], []),
        check("all TOML configs parse", toml_bad == [], toml_bad, []),
        check("cargo build --offline succeeds (edition 2024)", b.returncode == 0, b.stderr[-200:], 0),
        check("binary runs and prints the template greeting", out.strip() == "Hello, world!", out.strip(), "Hello, world!"),
        check("Cargo package name/description substituted", tomllib.loads((root / "Cargo.toml").read_text())["package"]["name"] == "tally",
              True, True),
    ]
    if fmtc is not None:
        checks += [check("cargo fmt --check clean with the template rustfmt.toml", fmtc.returncode == 0, fmtc.stdout[-120:], 0),
                   check("negative control: cargo fmt --check fails on unformatted main.rs", fmtn.returncode != 0, fmtn.returncode, "!=0")]
    else:
        checks.append(check("negative control: raw Cargo template keeps placeholders",
                            bool(PLACEHOLDER_RE.search(tmpl(sd / "references/cargo-toml.md"))), True, True))
    return checks, [root / "Cargo.toml", root / "src/main.rs"]


@card(KA("973-scaffold-new-repo/2257-scaffold-new-repo"))
def scaffold_new_repo(task, wd):
    sd = ATLAS / "973-scaffold-new-repo/2257-scaffold-new-repo"
    root = wd / "tally"
    gi_text = (sd / "references/gitignore-templates.md").read_text()
    gi_idx = [m.start() for m in re.finditer(r"^## ", gi_text, flags=re.M)]
    titles = re.findall(r"^## (.+)$", gi_text, flags=re.M)
    go_idx = titles.index("Go CLI")
    mapping = {"LICENSE": ("license.md", 0), "AGENTS.md": ("agents-md.md", 0), "CHANGELOG.md": ("changelog.md", 0),
               ".github/copilot-instructions.md": ("copilot-instructions.md", 0), ".gitignore": ("gitignore-templates.md", go_idx),
               "README.md": ("readme.md", 0)}
    render(sd, mapping, root, {".claude/settings.json": json.dumps({"$schema": "https://json.schemastore.org/claude-code-settings.json",
                                                                   "permissions": {"allow": [], "deny": []}}, indent=2) + "\n",
                               "docs/plans/todo/.gitkeep": "", "docs/plans/done/.gitkeep": ""})
    git(root, "init", "-q", "-b", "main")
    os.symlink("AGENTS.md", root / "CLAUDE.md")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "feat: scaffold new repository")
    tracked = set(git(root, "ls-files").stdout.split())
    mode = git(root, "ls-files", "-s", "CLAUDE.md").stdout.split()[0]
    lic = (root / "LICENSE").read_text()
    ign = git(root, "check-ignore", "-q", "x.exe", ok=False).returncode
    status = git(root, "status", "--porcelain").stdout.strip()
    return [
        check("placeholders substituted (YEAR, holder, name, description)", leftover_placeholders(root) == [],
              leftover_placeholders(root)[:5], []),
        check("LICENSE carries year and holder", "Copyright (c) 2026 Fixture Dev" in lic, lic.splitlines()[2:3]),
        check("CLAUDE.md is a git symlink to AGENTS.md", mode == "120000" and os.readlink(root / "CLAUDE.md") == "AGENTS.md", mode, "120000"),
        check(".claude/settings.json valid JSON with permissions", json.loads((root / ".claude/settings.json").read_text())
              ["permissions"] == {"allow": [], "deny": []}, True, True),
        check("Go CLI .gitignore section applied (git ignores x.exe)", ign == 0, ign, 0),
        check("initial commit contains all files, tree clean", {"LICENSE", "README.md", "CHANGELOG.md", "AGENTS.md", ".gitignore",
              "docs/plans/todo/.gitkeep", "docs/plans/done/.gitkeep"} <= tracked and status == "", sorted(tracked)),
        check("negative control: raw README template has placeholders",
              bool(PLACEHOLDER_RE.search(tmpl(sd / "references/readme.md"))), True, True),
    ], [root / "AGENTS.md", root / "README.md", root / "LICENSE"]


# =====================================================================================================
# set-up-installers: Homebrew formula from the template (ruby -c), go install path, README section
# =====================================================================================================
def camel(name):
    return "".join(w.capitalize() for w in re.split(r"[-_]", name))


def installers_plan(root: Path, owner, repo):
    gomod = (root / "go.mod").read_text()
    warn = ["go.mod has replace directives: go install will not work"] if re.search(r"^replace\s", gomod, flags=re.M) else []
    mod = re.search(r"^module\s+(\S+)", gomod, flags=re.M).group(1)
    if not re.match(r"[a-z0-9.-]+\.[a-z]+/", mod):
        warn.append("module path is not a domain-qualified import path")
    if (root / "main.go").exists():
        path = "github.com/%s/%s@latest" % (owner, repo)
    else:
        mains = sorted(p.parent.relative_to(root) for p in root.glob("cmd/*/main.go"))
        path = "github.com/%s/%s/%s@latest" % (owner, repo, mains[0]) if mains else None
    return path, warn


@card(KA("977-set-up-installers/2261-set-up-installers"))
def set_up_installers(task, wd):
    root = wd / "tally"
    write_tree(root, {"go.mod": "module github.com/octo-dev/tally\n\ngo 1.22\n", "cmd/tally/main.go": "package main\n\nfunc main() {}\n",
                      "README.md": "# tally\n"})
    src = (ATLAS / "977-set-up-installers/2261-set-up-installers/SKILL.md").read_text()
    formula_t = re.search(r"#### Cross-Platform Homebrew Formula.*?```ruby\n(.*?)```", src, flags=re.S).group(1)
    formula = (formula_t.replace("ProjectName", camel("tally")).replace("PROJECT-NAME", "tally").replace("PROJECT-DESCRIPTION",
               "Count lines in files").replace("OWNER/REPO", "octo-dev/tally"))
    fpath = tw(root / "Formula/tally.rb", formula)
    rb = sh(["ruby", "-c", fpath], root, ok=False)
    rb_raw = tw(wd / "raw_template.rb", formula_t)
    gpath, warns = installers_plan(root, "octo-dev", "tally")
    readme = (root / "README.md").read_text() + ("\n## Installation\n\n### Homebrew\n\n```sh\nbrew install octo-dev/tap/tally\n```\n\n"
                                                 "### go install\n\n```sh\ngo install %s\n```\n" % gpath)
    tw(root / "README.md", readme)
    urls = re.findall(r'url "([^"]+)"', formula)
    tw(wd / "neg/go.mod", "module tally\n\nreplace example.com/x => ../x\n")
    tw(wd / "neg/main.go", "package main\n")
    _, nwarn = installers_plan(wd / "neg", "octo-dev", "tally")
    return [
        check("formula class name is the CamelCase project name", "class Tally < Formula" in formula, formula.splitlines()[0]),
        check("ruby -c: formula is valid Ruby", rb.returncode == 0 and "Syntax OK" in rb.stdout, rb.stdout.strip()),
        check("4 platform URLs (darwin/linux x amd64/arm64), all substituted",
              len(urls) == 4 and all(u.startswith("https://github.com/octo-dev/tally/releases/download/v0.1.0/tally-0.1.0-") for u in urls), urls),
        check("go install path uses cmd/ subdirectory", gpath == "github.com/octo-dev/tally/cmd/tally@latest", gpath),
        check("README gains Installation section", "## Installation" in readme and gpath in readme, True, True),
        check("negative control: replace directive + non-domain module path are flagged", len(nwarn) == 2 and warns == [], nwarn),
        check("negative control: raw template keeps placeholders", "PROJECT-NAME" in rb_raw.read_text(), True, True),
    ], [fpath, root / "README.md"]


# =====================================================================================================
# set-up-linters: detect, recommend, write Prettier/EditorConfig from the references, run prettier
# =====================================================================================================
@card(KA("978-set-up-linters/2262-set-up-linters"))
def set_up_linters(task, wd):
    ref = ATLAS / "978-set-up-linters/2262-set-up-linters/references"
    root = wd / "web"
    write_tree(root, {"package.json": json.dumps({"name": "web", "scripts": {}}), "src/index.js": 'const a = "x";\nexport default a;\n',
                      "src/styles.css": "a{color:red}\n", "README.md": "# web\n", "Dockerfile": "FROM node:22\n",
                      ".github/workflows/ci.yml": "on: push\n", "dist/out.js": 'var  x = "y";;\n', "Makefile": "all:\n\techo\n"})
    files = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()]
    rec = [("JavaScript", "ESLint + Prettier"), ("Formatting", "Prettier, EditorConfig")]
    if any(f.endswith(".md") for f in files):
        rec.append(("Markdown", "markdownlint-cli2"))
    if any(f.endswith(".css") and "node_modules" not in f for f in files):
        rec.append(("CSS", "Stylelint"))
    if "Dockerfile" in files:
        rec.append(("Docker", "Hadolint"))
    if any(f.startswith(".github/workflows/") for f in files):
        rec.append(("CI", "Actionlint"))
    rec.append(("Spelling", "cspell"))
    table = ["| Category | Tools | Status |", "| --- | --- | --- |"] + ["| %s | %s | New |" % r for r in rec]
    tw(root / ".prettierrc.json", tmpl(ref / "tools/prettier.md", None, 2))
    tw(root / ".prettierignore", tmpl(ref / "tools/prettier.md", None, 4))
    tw(root / ".editorconfig", tmpl(ref / "tools/editorconfig.md", None, 0))
    pc = json.loads((root / ".prettierrc.json").read_text())
    pre = sh(["prettier", "--check", "src"], root, ok=False)
    sh(["prettier", "--write", "."], root, ok=False)
    post = sh(["prettier", "--check", "."], root, ok=False)
    dist_untouched = (root / "dist/out.js").read_text() == 'var  x = "y";;\n'
    ec = (root / ".editorconfig").read_text()
    rep = tw(wd / "linter-plan.md", "\n".join(table) + "\n")
    return [
        check("recommendation covers JS, formatting, Markdown, CSS, Docker, CI, spelling",
              [c for c, _ in rec] == ["JavaScript", "Formatting", "Markdown", "CSS", "Docker", "CI", "Spelling"], [c for c, _ in rec]),
        check(".prettierrc.json from the reference passes refresh checks",
              pc.get("printWidth") == 10000 and pc.get("proseWrap") == "preserve" and pc.get("semi") is False
              and pc.get("singleQuote") is True and pc.get("trailingComma") == "all", pc),
        check(".editorconfig base settings", all(k in ec for k in ("root = true", "charset = utf-8", "end_of_line = lf",
                                                                    "insert_final_newline = true")), True, True),
        check("negative control: prettier --check fails before formatting", pre.returncode != 0, pre.returncode, "!=0"),
        check("prettier --check passes after --write", post.returncode == 0, post.stdout[-150:] + post.stderr[-150:], 0),
        check("formatted to the config (single quotes, no semicolons)", (root / "src/index.js").read_text().startswith("const a = 'x'\n"),
              (root / "src/index.js").read_text()[:30]),
        check(".prettierignore keeps dist/ untouched", dist_untouched, True, True),
    ], [rep, root / ".prettierrc.json", root / ".editorconfig"]


# =====================================================================================================
# set-up-review-config: managed blocks + verbatim checklists, validation, idempotent rerun
# =====================================================================================================
RC = ATLAS / "979-set-up-review-config/2263-set-up-review-config/references"
BEGIN, END = "<!-- BEGIN set-up-review-config -->", "<!-- END set-up-review-config -->"


def marker_state(text):
    lines = text.splitlines()
    b = [i for i, l in enumerate(lines) if l == BEGIN]
    e = [i for i, l in enumerate(lines) if l == END]
    if not b and not e:
        return "none"
    if len(b) == 1 and len(e) == 1 and b[0] < e[0]:
        return "one"
    return "broken"


def put_block(text, block, heading=None):
    blk = block[block.index(BEGIN):block.index(END) + len(END)]
    if marker_state(text) == "one":
        return re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda m: blk, text, flags=re.S)
    if heading and heading in text:
        return text.rstrip("\n") + "\n\n" + blk + "\n"
    return text.rstrip("\n") + "\n\n" + (heading + "\n\n" if heading else "") + blk + "\n"


def important_rules(checklist):
    m = re.search(r"^## Important\n(.*?)(?=^## )", checklist, flags=re.S | re.M)
    return re.findall(r"^- \*\*(.+?)\*\*", m.group(1), flags=re.M) if m else []


def review_config(root: Path):
    tracked = git(root, "ls-files").stdout.split()
    for f in (".github/skills/code-review/SKILL.md", "AGENTS.md", "REVIEW.md"):
        if (root / f).exists() and marker_state((root / f).read_text()) == "broken":
            return {"error": "broken markers in " + f}
    guides = []
    if "go.mod" in tracked:
        guides.append(("write-go-code", "Go files", "`**/*.go`"))
    if any(f.endswith(".md") for f in tracked):
        guides.append(("write-markdown", "Markdown files", "`**/*.md`"))
    ci = " ".join((root / f).read_text() for f in tracked if f.startswith(".github/workflows/"))
    checks_run = [c for c in ("gofmt", "go vet", "golangci-lint", "markdownlint") if c in ci]
    skips = [f for f in ("go.sum", "package-lock.json") if f in tracked] + [".github/skills/code-review/*.md` except `SKILL.md"]
    cite = None
    routing = []
    imp_lines = []
    for g, label, globs in guides:
        body = (RC / "checklists" / (g + ".md")).read_text()
        tw(root / ".github/skills/code-review" / (g + ".md"), "<!-- Managed by set-up-review-config (unpinned) -->\n\n" + body)
        rules = important_rules(body)
        cite = cite or "`%s: %s`" % (g, rules[0])
        routing.append("- %s (%s): `%s.md`. Full guide: [%s style guide](https://github.com/cboone/agent-harness-plugins/blob/main/"
                       "plugins/%s/skills/%s/SKILL.md)." % (label, globs, g, g, g, g))
        imp_lines += ["- %s: %s" % (g, r) for r in rules]
    fill = {"ROUTING": "\n".join(routing), "CITATION-EXAMPLE": cite, "CI-CHECKS": ", ".join("`%s`" % c for c in checks_run),
            "SKIP-PATHS": ", ".join("`%s`" % s for s in skips), "IMPORTANT-RULES": "\n".join(imp_lines)}
    entry = tmpl(RC / "code-review-skill.md", fill).replace("SHEBANG-LINE\n", "")
    agents = tmpl(RC / "agents-md-section.md", fill)
    review = tmpl(RC / "review-md.md", fill)
    sk = root / ".github/skills/code-review/SKILL.md"
    tw(sk, put_block(sk.read_text(), entry) if sk.exists() else entry)
    am = root / "AGENTS.md"
    tw(am, put_block(am.read_text(), agents, "## Code Review Rules") if am.exists() else "# repo\n\n" + agents)
    rm = root / "REVIEW.md"
    tw(rm, put_block(rm.read_text(), review) if rm.exists() else review)
    return {"guides": [g for g, _, _ in guides], "ci_checks": checks_run, "skips": skips}


@card(KA("979-set-up-review-config/2263-set-up-review-config"))
def set_up_review_config(task, wd):
    root = git_repo(wd / "repo", {"go.mod": "module x\n", "go.sum": "", "main.go": "package main\n", "docs/guide.md": "# g\n",
                                  "AGENTS.md": "# repo\n\nHouse rule: keep PRs small.\n",
                                  ".github/workflows/ci.yml": "steps: [{run: gofmt -l .}, {run: go vet ./...}]\n"})
    r1 = review_config(root)
    snap1 = {p: (root / p).read_text() for p in ("AGENTS.md", "REVIEW.md", ".github/skills/code-review/SKILL.md",
                                                  ".github/skills/code-review/write-go-code.md")}
    r2 = review_config(root)
    snap2 = {p: (root / p).read_text() for p in snap1}
    fm = frontmatter(snap1[".github/skills/code-review/SKILL.md"])
    verbatim = snap1[".github/skills/code-review/write-go-code.md"].split("\n", 2)[2] == (RC / "checklists/write-go-code.md").read_text()
    states = {p: marker_state(t) for p, t in snap1.items() if not p.endswith("write-go-code.md")}
    leftover = [p for p, t in snap1.items() if re.search(r"\b(ROUTING|CITATION-EXAMPLE|CI-CHECKS|SKIP-PATHS|IMPORTANT-RULES)\b", t)
                and not p.endswith("write-go-code.md")]
    broken = git_repo(wd / "broken", {"go.mod": "module x\n", "REVIEW.md": BEGIN + "\n\n" + BEGIN + "\n"})
    rb = review_config(broken)
    return [
        check("guides detected from tracked files", r1["guides"] == ["write-go-code", "write-markdown"], r1["guides"]),
        check("CI checks read from workflows", r1["ci_checks"] == ["gofmt", "go vet"], r1["ci_checks"]),
        check("citation example built from the first Important rule", "`write-go-code: Checked errors`" in snap1["REVIEW.md"], True, True),
        check("entry skill frontmatter name: code-review + description", fm.get("name") == "code-review" and fm.get("description"), fm),
        check("exactly one BEGIN..END block in SKILL.md, AGENTS.md, REVIEW.md", set(states.values()) == {"one"}, states),
        check("checklist installed verbatim after the managed first line", verbatim, True, True),
        check("repository text outside the block preserved", "House rule: keep PRs small." in snap1["AGENTS.md"], True, True),
        check("all template placeholders filled", leftover == [], leftover, []),
        check("rerun changes nothing (idempotent)", snap1 == snap2, True, True),
        check("negative control: duplicated BEGIN marker is refused", rb.get("error", "").startswith("broken markers"), rb),
    ], [root / ".github/skills/code-review/SKILL.md", root / "REVIEW.md", root / "AGENTS.md"]


# =====================================================================================================
# write-go-code: a go/ast style checker (essential checklist rules) + gofmt + go vet
# =====================================================================================================
GO_CHECKER = r'''package main

import (
	"encoding/json"
	"go/ast"
	"go/parser"
	"go/token"
	"os"
	"regexp"
	"strconv"
	"strings"
	"unicode"
)

type finding struct {
	Rule string `json:"rule"`
	Line int    `json:"line"`
}

func main() {
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, os.Args[1], nil, parser.ParseComments)
	if err != nil {
		panic(err)
	}
	var out []finding
	add := func(rule string, p token.Pos) { out = append(out, finding{rule, fset.Position(p).Line}) }
	if strings.Contains(f.Name.Name, "_") || f.Name.Name != strings.ToLower(f.Name.Name) {
		add("package-name", f.Name.Pos())
	}
	for _, bad := range []string{"util", "common", "misc"} {
		if f.Name.Name == bad {
			add("meaningless-package-name", f.Name.Pos())
		}
	}
	initialism := regexp.MustCompile(`(Url|Http|Id)([A-Z]|$)`)
	ast.Inspect(f, func(n ast.Node) bool {
		switch x := n.(type) {
		case *ast.FuncDecl:
			if x.Recv != nil && len(x.Recv.List) > 0 && len(x.Recv.List[0].Names) > 0 {
				if r := x.Recv.List[0].Names[0].Name; r == "this" || r == "self" || len(r) > 2 {
					add("receiver-name", x.Recv.Pos())
				}
			}
			if strings.HasPrefix(x.Name.Name, "Get") && x.Recv != nil {
				add("getter-prefix", x.Name.Pos())
			}
			if x.Name.IsExported() && x.Doc == nil {
				add("undocumented-export", x.Pos())
			}
			if strings.Contains(x.Name.Name, "_") {
				add("mixed-caps", x.Name.Pos())
			}
			if initialism.MatchString(x.Name.Name) {
				add("initialism", x.Name.Pos())
			}
		case *ast.CallExpr:
			if sel, ok := x.Fun.(*ast.SelectorExpr); ok && len(x.Args) > 0 {
				pkg, _ := sel.X.(*ast.Ident)
				if pkg != nil && ((pkg.Name == "errors" && sel.Sel.Name == "New") || (pkg.Name == "fmt" && sel.Sel.Name == "Errorf")) {
					if lit, ok := x.Args[0].(*ast.BasicLit); ok {
						s, _ := strconv.Unquote(lit.Value)
						if s != "" && (unicode.IsUpper([]rune(s)[0]) || strings.HasSuffix(s, ".") || strings.HasSuffix(s, "!")) {
							add("error-string", lit.Pos())
						}
					}
				}
			}
		case *ast.IfStmt:
			if x.Else != nil && len(x.Body.List) > 0 {
				if _, ok := x.Body.List[len(x.Body.List)-1].(*ast.ReturnStmt); ok {
					add("else-after-return", x.Else.Pos())
				}
			}
		}
		return true
	})
	if out == nil {
		out = []finding{}
	}
	json.NewEncoder(os.Stdout).Encode(out)
}
'''
GO_BAD = '''package string_utils

import (
	"errors"
	"fmt"
)

type Client struct{ name string }

func (this *Client) GetName() string { return this.name }

func Parse_Url(s string) (string, error) {
	if s == "" {
		return "", errors.New("Empty input.")
	} else {
		return fmt.Sprintf("%s", s), nil
	}
}
'''
GO_GOOD = '''// Package strutil parses identifiers.
package strutil

import "errors"

// Client holds a name.
type Client struct{ name string }

// Name returns the client name.
func (c *Client) Name() string { return c.name }

// ParseURL validates s.
func ParseURL(s string) (string, error) {
	if s == "" {
		return "", errors.New("empty input")
	}
	return s, nil
}
'''


@card(KA("987-write-go-code/2271-write-go-code"))
def write_go_code(task, wd):
    tool = wd / "gostyle"
    write_tree(tool, {"go.mod": "module gostyle\n\ngo 1.22\n", "main.go": GO_CHECKER})
    sh(["go", "build", "-o", "gostyle", "."], tool, **GO_ENV)
    bad = tw(wd / "bad/strutil.go", GO_BAD)
    good = tw(wd / "good/strutil.go", GO_GOOD)
    tw(wd / "good/go.mod", "module strutil\n\ngo 1.22\n")
    fb = json.loads(sh([tool / "gostyle", bad], wd).stdout)
    fg = json.loads(sh([tool / "gostyle", good], wd).stdout)
    rules = sorted({x["rule"] for x in fb})
    gofmt_good = sh(["gofmt", "-l", good], wd).stdout.strip()
    vet = sh(["go", "vet", "./..."], wd / "good", ok=False, **GO_ENV)
    rep = jw(wd / "go-style-report.json", {"bad": fb, "good": fg})
    expected = sorted(["package-name", "receiver-name", "getter-prefix", "undocumented-export", "mixed-caps", "initialism",
                       "error-string", "else-after-return"])
    return [
        check("checker compiled with go build (stdlib go/ast)", (tool / "gostyle").exists(), True, True),
        check("all 8 seeded checklist violations found", rules == expected, rules, expected),
        check("rewritten code: zero findings", fg == [], fg, []),
        check("rewritten code is gofmt-clean and go vet passes", gofmt_good == "" and vet.returncode == 0, [gofmt_good, vet.stderr[-100:]]),
        check("negative control: original code fails the same checker", len(fb) >= 8, len(fb), ">=8"),
    ], [rep]


# =====================================================================================================
# obra superpowers v7
# =====================================================================================================
BS = OBRA / "brainstorming/scripts"


def http_get(port, path, cookie=None):
    import http.client
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    c.request("GET", path, headers={"Cookie": cookie} if cookie else {})
    r = c.getresponse()
    body = r.read().decode("utf-8", "replace")
    return r.status, body, r.getheader("Set-Cookie")


def ws_send(port, key, msg, origin=None):
    import base64
    import socket
    s = socket.create_connection(("127.0.0.1", port), timeout=5)
    hdr = ("GET /?key=%s HTTP/1.1\r\nHost: localhost:%d\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
           "Sec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n" % (key, port, base64.b64encode(os.urandom(16)).decode()))
    if origin:
        hdr += "Origin: %s\r\n" % origin
    s.sendall((hdr + "\r\n").encode())
    resp = s.recv(1024).decode("latin1")
    ok = resp.startswith("HTTP/1.1 101")
    if ok:
        data = json.dumps(msg).encode()
        mask = os.urandom(4)
        frame = bytes([0x81, 0x80 | len(data)]) + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        s.sendall(frame)
        time.sleep(0.3)
    s.close()
    return ok


@card(KO("brainstorming"))
def obra_brainstorming(task, wd):
    proj = wd / "proj"
    proj.mkdir(parents=True, exist_ok=True)
    git(proj, "init", "-q", "-b", "main")
    p = sh(["bash", BS / "start-server.sh", "--project-dir", proj, "--background"], proj, timeout=20,
           SUPERPOWERS_DISABLE_TELEMETRY="1", DISABLE_TELEMETRY="1")
    info = json.loads(p.stdout.strip().splitlines()[-1])
    session = Path(info["state_dir"]).parent
    try:
        port, key = info["port"], re.search(r"key=([0-9a-f]+)", info["url"]).group(1)
        approaches = [("a", "Shared family calendar", "one feed, everyone edits"),
                      ("b", "Per-person calendars + overlay", "privacy per member, merged view"),
                      ("c", "Chore-first planner", "tasks drive the schedule")]
        screen = "<h2>Which direction fits?</h2>\n<div class=\"options\">\n" + "".join(
            '  <div class="option" data-choice="%s" onclick="toggleSelect(this)"><h3>%s</h3><p>%s</p></div>\n' % a
            for a in approaches) + "</div>\n"
        tw(Path(info["screen_dir"]) / "approaches.html", screen)
        slog = Path(info["state_dir"]) / "server.log"
        for _ in range(60):  # the server's watcher announces the screen (and clears stale events) after a 100 ms debounce
            if "screen-added" in slog.read_text():
                break
            time.sleep(0.05)
        s_nokey, _, _ = http_get(port, "/")
        s_key, _, cookie = http_get(port, "/?key=" + key)
        s_scr, body, _ = http_get(port, "/", cookie.split(";")[0])
        ws_ok = ws_send(port, key, {"type": "click", "choice": "b", "text": approaches[1][1]})
        ws_bad = ws_send(port, key, {"type": "click", "choice": "a"}, origin="http://evil.example")
        events = [json.loads(l) for l in (Path(info["state_dir"]) / "events").read_text().splitlines()] \
            if (Path(info["state_dir"]) / "events").exists() else []
        slog_text = slog.read_text()
    finally:
        stop = sh(["bash", BS / "stop-server.sh", session], proj, ok=False, timeout=20)
    chosen = next((a for a in approaches if events and a[0] == events[-1]["choice"]), None)
    spec = proj / "docs/superpowers/specs/2026-11-03-family-calendar-design.md"
    tw(spec, "# Family calendar design\n\n## Chosen approach\n\n%s: %s\n\n## Alternatives considered\n\n%s\n"
       % (chosen[1], chosen[2], "\n".join("- %s: %s" % (a[1], a[2]) for a in approaches if a != chosen)))
    git(proj, "add", spec)
    git(proj, "commit", "-q", "-m", "docs: family calendar design")
    committed = spec.relative_to(proj).as_posix() in git(proj, "ls-files").stdout
    return [
        check("companion server started (127.0.0.1, JSON connection info)", info["host"] == "127.0.0.1" and info["port"] > 1023, info["host"]),
        check("negative control: request without session key is refused (403)", s_nokey == 403, s_nokey, 403),
        check("keyed bootstrap 200, then the newest screen is served with all 3 approaches",
              s_key == 200 and s_scr == 200 and all(a[1] in body for a in approaches), [s_key, s_scr]),
        check("browser click over WebSocket recorded in state/events", ws_ok and len(events) == 1 and events[0]["choice"] == "b", events),
        check("cross-origin WebSocket rejected (no event injected)", ws_bad is False and len(events) == 1, ws_bad, False),
        check("server announced the new screen (screen-added)", "screen-added" in slog_text, True, True),
        check("server stopped cleanly", '"stopped"' in stop.stdout, stop.stdout.strip()),
        check("design written to docs/superpowers/specs/<date>-<topic>-design.md and committed", committed, spec.name),
    ], [spec, tw(wd / "events.json", json.dumps(events))]


EP = OBRA / "executing-plans/scripts"
SDD = OBRA / "subagent-driven-development/scripts"
PLAN_MD = """# Slugify Implementation Plan

**Goal:** add slugify().

### Task 1: slugify lowercases

```markdown
### Task 9: example inside a fence must not be extracted
```

- [ ] Write test, implement, run `python3 test_slug.py`

### Task 2: slugify joins words with hyphens

- [ ] Extend test and implementation
"""


@card(KO("executing-plans"))
def obra_executing_plans(task, wd):
    repo = git_repo(wd / "repo", {"docs/plans/slug.md": PLAN_MD, "README.md": "#\n"})
    out = sh(["bash", EP / "task-start", "docs/plans/slug.md", "1"], repo).stdout
    brief = Path(re.search(r"^brief: (.+)$", out, flags=re.M).group(1))
    base = re.search(r"^base: ([0-9a-f]{40})$", out, flags=re.M).group(1)
    tw(repo / "slug.py", "def slugify(s):\n    return s.lower()\n")
    tw(repo / "test_slug.py", "from slug import slugify\nassert slugify('AB') == 'ab'\nprint('1 passed')\n")
    git(repo, "add", "slug.py", "test_slug.py")
    git(repo, "commit", "-q", "-m", "feat: slugify lowercases")
    done1 = sh(["bash", EP / "task-done", "docs/plans/slug.md", "1", base, "--", "python3", "test_slug.py"], repo, ok=False)
    out2 = sh(["bash", EP / "task-start", "docs/plans/slug.md", "2"], repo).stdout
    base2 = re.search(r"^base: ([0-9a-f]{40})$", out2, flags=re.M).group(1)
    tw(repo / "test_slug.py", "from slug import slugify\nassert slugify('A B') == 'a-b'\nprint('1 passed')\n")
    git(repo, "commit", "-q", "-am", "test: hyphens (red)")
    done2 = sh(["bash", EP / "task-done", "docs/plans/slug.md", "2", base2, "--", "python3", "test_slug.py"], repo, ok=False)
    ws = Path(sh(["bash", SDD / "sdd-workspace", "docs/plans/slug.md"], repo).stdout.strip())
    ledger = (ws / "progress.md").read_text()
    btxt = brief.read_text()
    return [
        check("task-start extracted Task 1 brief and recorded BASE", btxt.startswith("### Task 1") and "Task 2" not in btxt
              and len(base) == 40, btxt.splitlines()[0]),
        check("fenced 'Task 9' example ignored by the extractor", "Task 9" in btxt and btxt.count("### Task") == 2, btxt.count("### Task")),
        check("task-done with passing tests records Task 1 in the ledger", done1.returncode == 0 and "Task 1: complete" in ledger,
              done1.returncode, 0),
        check("negative control: failing tests exit non-zero and Task 2 is NOT recorded",
              done2.returncode != 0 and "Task 2" not in ledger, [done2.returncode, "Task 2" in ledger], ["!=0", False]),
        check("full test log kept in the workspace", (ws / "task-2-tests.log").exists() and "AssertionError" in (ws / "task-2-tests.log").read_text(),
              True, True),
    ], [ws / "progress.md", brief]


@card(KO("subagent-driven-development"))
def obra_sdd(task, wd):
    repo = git_repo(wd / "repo", {"docs/alpha/plan.md": PLAN_MD, "docs/beta/plan.md": PLAN_MD.replace("Slugify", "Beta"), "a.txt": "1\n"})
    w1 = sh(["bash", SDD / "sdd-workspace", "docs/alpha/plan.md"], repo).stdout.strip()
    w2 = sh(["bash", SDD / "sdd-workspace", "docs/beta/plan.md"], repo).stdout.strip()
    w1b = sh(["bash", SDD / "sdd-workspace", "./docs/../docs/alpha/plan.md"], repo).stdout.strip()
    tb = sh(["bash", SDD / "task-brief", "docs/alpha/plan.md", "2"], repo).stdout
    base = git(repo, "rev-parse", "HEAD").stdout.strip()
    tw(repo / "a.txt", "2\n")
    git(repo, "commit", "-q", "-am", "task 2 step a")
    tw(repo / "b.txt", "new\n")
    git(repo, "add", "b.txt")
    git(repo, "commit", "-q", "-m", "task 2 step b")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    rp = sh(["bash", SDD / "review-package", "docs/alpha/plan.md", base, head], repo).stdout
    pkg = Path(re.search(r"wrote (.+?): ", rp).group(1)).read_text()
    empty = sh(["bash", SDD / "review-package", "docs/alpha/plan.md", head, head], repo, ok=False)
    rev = sh(["bash", SDD / "review-package", "docs/alpha/plan.md", head, base], repo, ok=False)
    missing = sh(["bash", SDD / "task-brief", "docs/alpha/plan.md", "7"], repo, ok=False)
    status = git(repo, "status", "--porcelain").stdout
    return [
        check("same basename plans get distinct workspaces (parent-dir disambiguation)",
              w1.endswith(".superpowers/sdd/plan") and w2.endswith(".superpowers/sdd/plan-beta"), [w1[-20:], w2[-20:]]),
        check("different spellings of one plan resolve to the same workspace", w1 == w1b, True, True),
        check("task-brief wrote Task 2 only", "wrote" in tb and "Task 2" in (Path(w1) / "task-2-brief.md").read_text()
              and "Task 1" not in (Path(w1) / "task-2-brief.md").read_text(), tb.strip()),
        check("review package spans both task commits with stat and diff",
              "2 commit(s)" in rp and "b.txt" in pkg and "## Diff" in pkg, rp.strip()),
        check("negative control: empty range and reversed range refused (exit 3)", empty.returncode == 3 and rev.returncode == 3,
              [empty.returncode, rev.returncode], [3, 3]),
        check("missing task number refused (exit 3)", missing.returncode == 3, missing.returncode, 3),
        check("workspace self-ignored: git status clean", status.strip() == "", status, ""),
    ], [Path(w1) / "task-2-brief.md", Path(re.search(r"wrote (.+?): ", rp).group(1))]


@card(KO("systematic-debugging"))
def obra_systematic_debugging(task, wd):
    proj = wd / "proj"
    runner = ("const f = process.argv[2]; require('./' + f);\n")
    write_tree(proj, {"package.json": json.dumps({"name": "p", "version": "1.0.0", "scripts": {"test": "node run.js"}}),
                      "run.js": runner,
                      "src/a.test.js": "console.log('a ok');\n",
                      "src/b.test.js": "require('fs').mkdirSync('.git', {recursive: true}); console.log('b');\n",
                      "src/c.test.js": "console.log('c ok');\n"})
    script = OBRA / "systematic-debugging/find-polluter.sh"
    r = sh(["bash", script, ".git", "src/*.test.js"], proj, ok=False, timeout=60)
    shutil.rmtree(proj / ".git")
    tw(proj / "src/b.test.js", "console.log('b fixed');\n")
    clean = sh(["bash", script, ".git", "src/*.test.js"], proj, ok=False, timeout=60)
    log = tw(wd / "bisect.log", r.stdout + "\n---- after fix ----\n" + clean.stdout)
    hyp = jw(wd / "root-cause.json", {"phase1_evidence": "'.git' appears after the suite", "hypothesis": "one test creates .git",
                                      "test": "find-polluter bisection", "root_cause": "src/b.test.js mkdirSync('.git')",
                                      "fix": "remove the side effect", "verified": clean.returncode == 0})
    return [
        check("find-polluter.sh (shipped script) identifies src/b.test.js", r.returncode == 1 and "Test: ./src/b.test.js" in r.stdout,
              re.findall(r"Test: (\S+)", r.stdout)),
        check("it ran tests in order and stopped at the polluter", "[2/3]" in r.stdout and "[3/3]" not in r.stdout, True, True),
        check("after the root-cause fix the same bisection reports clean", clean.returncode == 0 and "No polluter found" in clean.stdout,
              clean.returncode, 0),
        check("negative control: the polluted run was not clean", r.returncode != 0, r.returncode, "!=0"),
    ], [log, hyp]


@card(KO("test-driven-development"))
def obra_tdd(task, wd):
    proj = wd / "proj"
    proj.mkdir(parents=True, exist_ok=True)
    run = lambda: sh(["python3", "-m", "unittest", "-q", "test_retry"], proj, ok=False)
    tw(proj / "retry.py", "def retry(fn, attempts):\n    raise NotImplementedError\n")
    tw(proj / "test_retry.py", "import unittest\nfrom retry import retry\n\nclass T(unittest.TestCase):\n"
       "    def test_retries_until_success(self):\n        calls = []\n        def fn():\n            calls.append(1)\n"
       "            if len(calls) < 3:\n                raise IOError('flaky')\n            return 'ok'\n"
       "        self.assertEqual(retry(fn, 3), 'ok')\n        self.assertEqual(len(calls), 3)\n")
    red = run()
    red_reason = "NotImplementedError" in red.stderr
    tw(proj / "retry.py", "def retry(fn, attempts):\n    for i in range(attempts):\n        try:\n            return fn()\n"
       "        except Exception:\n            if i == attempts - 1:\n                raise\n")
    green = run()
    # second cycle: a test that passes immediately proves nothing -> must be rewritten
    tw(proj / "test_retry2.py", "import unittest\nfrom retry import retry\n\nclass T2(unittest.TestCase):\n"
       "    def test_returns_value(self):\n        self.assertEqual(retry(lambda: 5, 1), 5)\n")
    pre = sh(["python3", "-m", "unittest", "-q", "test_retry2"], proj, ok=False)
    verdict2 = "testing existing behavior: fix test" if pre.returncode == 0 else "red"
    log = jw(wd / "tdd-log.json", {"cycle1": {"red_exit": red.returncode, "red_reason": "NotImplementedError" if red_reason else "",
                                              "green_exit": green.returncode}, "cycle2": {"first_run_exit": pre.returncode,
                                                                                         "verdict": verdict2}})
    return [
        check("RED: test run before implementation fails", red.returncode != 0, red.returncode, "!=0"),
        check("RED fails for the right reason (feature missing, not a typo)", red_reason, True, True),
        check("GREEN: minimal implementation makes the test pass", green.returncode == 0, green.stderr[-120:], 0),
        check("negative control: a test that passes on first run is flagged as testing existing behavior",
              verdict2 == "testing existing behavior: fix test", verdict2),
    ], [log, proj / "retry.py"]


def finishing_menu(root: Path, test_cmd):
    t = subprocess.run(test_cmd, cwd=root, capture_output=True, text=True, timeout=30)
    if t.returncode:
        return {"stage": "tests-failed", "menu": None, "output": t.stdout[-200:] + t.stderr[-200:]}
    branch = git(root, "branch", "--show-current").stdout.strip()
    if branch:
        menu = ["Merge back to main locally", "Push and create a Pull Request", "Keep the branch as-is (I'll handle it later)"]
    else:
        menu = ["Push as new branch and create a Pull Request", "Keep as-is (I'll handle it later)"]
    return {"stage": "menu", "branch": branch or None, "menu": menu}


@card(KO("finishing-a-development-branch"))
def obra_finishing(task, wd):
    repo = git_repo(wd / "repo", {"calc.py": "def add(a, b):\n    return a + b\n",
                                  "test_calc.py": "from calc import add\nassert add(1, 2) == 3\n"})
    test = ["python3", "test_calc.py"]
    git(repo, "checkout", "-q", "-b", "feature/mul")
    with open(repo / "calc.py", "a") as fh:
        fh.write("\n\ndef mul(a, b):\n    return a * b\n")
    with open(repo / "test_calc.py", "a") as fh:
        fh.write("from calc import mul\nassert mul(2, 3) == 6\n")
    git(repo, "commit", "-q", "-am", "feat: mul")
    m1 = finishing_menu(repo, test)
    # option 1: merge locally, verify tests on the merged result, then delete the branch
    git(repo, "checkout", "-q", "main")
    git(repo, "merge", "-q", "--no-ff", "-m", "merge feature/mul", "feature/mul")
    merged = subprocess.run(test, cwd=repo, capture_output=True, timeout=30).returncode
    git(repo, "branch", "-d", "feature/mul")
    branches = git(repo, "branch", "--format=%(refname:short)").stdout.split()
    git(repo, "checkout", "-q", "--detach", "HEAD")
    m2 = finishing_menu(repo, test)
    git(repo, "checkout", "-q", "main")
    tw(repo / "calc.py", "def add(a, b):\n    return a - b\n")
    m3 = finishing_menu(repo, test)
    rep = jw(wd / "finish.json", {"named": m1, "detached": m2, "failing": m3, "merged_tests_exit": merged, "branches": branches})
    return [
        check("tests verified first; named branch gets exactly the 3 options", m1["stage"] == "menu" and len(m1["menu"]) == 3, m1["menu"]),
        check("detached HEAD gets exactly the 2 options", m2["menu"] is not None and len(m2["menu"]) == 2 and m2["branch"] is None, m2["menu"]),
        check("option 1 executed: merged, tests pass on merged result, branch deleted",
              merged == 0 and branches == ["main"] and "def mul" in (git(repo, "show", "HEAD:calc.py").stdout), branches),
        check("negative control: failing suite -> stop, no menu offered", m3["stage"] == "tests-failed" and m3["menu"] is None, m3["stage"]),
        check("no discard option is ever offered", not any("discard" in o.lower() for o in m1["menu"] + m2["menu"]), True, True),
    ], [rep]


def worktree_step0(path: Path):
    gd = Path(git(path, "rev-parse", "--git-dir").stdout.strip())
    gc = Path(git(path, "rev-parse", "--git-common-dir").stdout.strip())
    gd = (path / gd).resolve() if not gd.is_absolute() else gd.resolve()
    gc = (path / gc).resolve() if not gc.is_absolute() else gc.resolve()
    sup = git(path, "rev-parse", "--show-superproject-working-tree", ok=False).stdout.strip()
    return "linked-worktree" if gd != gc and not sup else "normal"


@card(KO("using-git-worktrees"))
def obra_worktrees(task, wd):
    repo = git_repo(wd / "repo", {"app.py": "print(1)\n", ".gitignore": "*.pyc\n"})
    s0 = worktree_step0(repo)
    ignored_before = git(repo, "check-ignore", "-q", ".worktrees/", ok=False).returncode == 0
    if not ignored_before:  # safety verification: add to .gitignore and commit before creating
        with open(repo / ".gitignore", "a") as fh:
            fh.write(".worktrees/\n")
        git(repo, "add", ".gitignore")
        git(repo, "commit", "-q", "-m", "chore: ignore .worktrees")
    ignored_after = git(repo, "check-ignore", "-q", ".worktrees/", ok=False).returncode == 0
    git(repo, "worktree", "add", "-q", "-b", "feature/x", ".worktrees/feature-x")
    wt = repo / ".worktrees/feature-x"
    s1 = worktree_step0(wt)
    branch = git(wt, "branch", "--show-current").stdout.strip()
    status = git(repo, "status", "--porcelain").stdout.strip()
    lst = git(repo, "worktree", "list", "--porcelain").stdout
    rep = jw(wd / "worktree.json", {"main_checkout": s0, "ignored_before": ignored_before, "ignored_after": ignored_after,
                                    "worktree": str(wt), "inside_worktree": s1, "branch": branch})
    return [
        check("step 0 in the main checkout: GIT_DIR == GIT_COMMON (normal)", s0 == "normal", s0, "normal"),
        check("negative control: .worktrees was not ignored before the safety fix", ignored_before is False, ignored_before, False),
        check("safety verification: .worktrees ignored before creating the worktree", ignored_after, ignored_after, True),
        check("worktree created on its own branch", branch == "feature/x" and "feature-x" in lst, branch),
        check("step 0 inside the worktree detects isolation (no nested worktree)", s1 == "linked-worktree", s1),
        check("main checkout stays clean (worktree dir not tracked)", status == "", status, ""),
    ], [rep]


def verify_claims(root, claims):
    out = []
    for c in claims:
        if not c.get("command"):
            out.append({**c, "allowed": False, "status": "no verification command identified"})
            continue
        p = subprocess.run(c["command"], cwd=root, shell=True, capture_output=True, text=True, timeout=30)
        txt = p.stdout + p.stderr
        ok = p.returncode == 0 and re.search(c["success"], txt) is not None
        fails = re.search(r"failures=(\d+)|(\d+) failed", txt)
        out.append({**c, "exit": p.returncode, "allowed": ok,
                    "status": ("claim confirmed: " if ok else "actual status: ") + txt.strip().splitlines()[-1][:120],
                    "failures": int(next(g for g in fails.groups() if g)) if fails else 0})
    return out


@card(KO("verification-before-completion"))
def obra_verification(task, wd):
    root = wd / "proj"
    write_tree(root, {"m.py": "def inc(x):\n    return x + 1\n",
                      "test_m.py": "import unittest\nfrom m import inc\nclass T(unittest.TestCase):\n"
                                   "    def test_a(self): self.assertEqual(inc(1), 2)\n    def test_b(self): self.assertEqual(inc(-1), 0)\n"
                                   "    def test_c(self): self.assertEqual(inc(1.5), 3)\n",
                      "build.sh": "python3 -m py_compile m.py && echo build ok\n"})
    claims = [{"claim": "all tests pass", "command": "python3 -m unittest test_m 2>&1", "success": r"\nOK"},
              {"claim": "build succeeds", "command": "bash build.sh", "success": "build ok"},
              {"claim": "linter clean", "command": None, "success": ""}]
    res = verify_claims(root, claims)
    tw(root / "m.py", "def inc(x):\n    return int(x) + 1 if x != 1.5 else 3\n")
    res2 = verify_claims(root, claims[:1])
    rep = jw(wd / "verification.json", {"first": res, "after_fix": res2})
    return [
        check("negative control: 'all tests pass' refused, actual status reports 1 failure",
              res[0]["allowed"] is False and res[0]["failures"] == 1, [res[0]["allowed"], res[0]["failures"]], [False, 1]),
        check("build claim confirmed with fresh evidence", res[1]["allowed"] and res[1]["exit"] == 0, res[1]["status"]),
        check("claim with no proving command is never allowed", res[2]["allowed"] is False, res[2]["status"]),
        check("after the fix the fresh run confirms the test claim", res2[0]["allowed"] and res2[0]["exit"] == 0, res2[0]["status"]),
    ], [rep]


# ------------------------------------------------------------------ receiving / requesting code review
FORBIDDEN = [r"you'?re absolutely right", r"great point", r"excellent feedback", r"let me implement that now", r"\bthanks?\b"]


def receive_review(repo: Path, items):
    out = []
    for it in items:
        kind, ev = it["kind"], ""
        if kind == "unclear":
            out.append({**it, "decision": "clarify", "order": 0, "response": "Which function in utils.py does this refer to?"})
            continue
        if kind == "remove-unused":
            uses = [l for l in git(repo, "grep", "-n", it["symbol"], ok=False).stdout.splitlines() if "def " + it["symbol"] not in l]
            if uses:
                out.append({**it, "decision": "push back", "evidence": uses, "order": 9,
                            "response": "%s is still called at %s; removing it breaks the report." % (it["symbol"], uses[0].split(":")[0] + ":" + uses[0].split(":")[1])})
                continue
        if kind == "yagni":
            callers = git(repo, "grep", "-n", it["symbol"], ok=False).stdout.strip()
            out.append({**it, "decision": "push back (YAGNI)", "evidence": callers or "no callers", "order": 9,
                        "response": "Nothing calls %s today, so a cache adds code without a user; skipping unless needed." % it["symbol"]})
            continue
        if kind == "security":
            src = (repo / it["file"]).read_text()
            valid = bool(re.search(r"execute\(f?['\"].*\{|%s|\+ ", src))
            out.append({**it, "decision": "fix" if valid else "push back", "order": 1,
                        "response": "Fixed: query() now binds name as a parameter."})
            continue
        out.append({**it, "decision": "fix", "order": {"typo": 2, "complex": 3}.get(kind, 3), "response": "Fixed: " + it["text"]})
    return sorted(out, key=lambda x: x["order"])


@card(KO("receiving-code-review"))
def obra_receiving_review(task, wd):
    repo = git_repo(wd / "repo", {
        "db.py": "def query(cur, name):\n    \"\"\"Recieve rows for name.\"\"\"\n    return cur.execute(f\"SELECT * FROM t WHERE n = '{name}'\")\n",
        "util.py": "def fmt_date(d):\n    return d.isoformat()\n",
        "report.py": "from util import fmt_date\n\ndef line(d):\n    return fmt_date(d)\n",
        "test_all.py": "import datetime, sqlite3\nfrom report import line\nfrom db import query\n"
                       "assert line(datetime.date(2026, 1, 2)) == '2026-01-02'\n"
                       "c = sqlite3.connect(':memory:').cursor(); c.execute('create table t(n)'); c.execute(\"insert into t values ('a')\")\n"
                       "assert query(c, \"a' OR '1'='1\").fetchall() == []\n"})
    items = [{"id": 1, "kind": "remove-unused", "symbol": "fmt_date", "text": "fmt_date is unused, delete it"},
             {"id": 2, "kind": "yagni", "symbol": "cached_query", "text": "add a professional caching layer (cached_query)"},
             {"id": 3, "kind": "typo", "file": "db.py", "text": "typo 'Recieve' in docstring"},
             {"id": 4, "kind": "security", "file": "db.py", "text": "SQL injection in query()"},
             {"id": 5, "kind": "unclear", "text": "fix the thing in utils"}]
    pre = subprocess.run(["python3", "test_all.py"], cwd=repo, capture_output=True, timeout=20).returncode
    plan = receive_review(repo, items)
    for p in plan:  # implement one at a time, test each
        if p["decision"] == "fix" and p["kind"] == "security":
            tw(repo / "db.py", (repo / "db.py").read_text().replace("f\"SELECT * FROM t WHERE n = '{name}'\")",
                                                                   "\"SELECT * FROM t WHERE n = ?\", (name,))"))
        if p["decision"] == "fix" and p["kind"] == "typo":
            tw(repo / "db.py", (repo / "db.py").read_text().replace("Recieve", "Receive"))
        p["test_exit"] = subprocess.run(["python3", "test_all.py"], cwd=repo, capture_output=True, timeout=20).returncode \
            if p["decision"] == "fix" else None
    post = subprocess.run(["python3", "test_all.py"], cwd=repo, capture_output=True, timeout=20).returncode
    # negative control: blindly accepting item 1 (delete fmt_date) breaks the suite
    naive = wd / "naive"
    shutil.copytree(repo, naive)
    tw(naive / "util.py", "")
    naive_exit = subprocess.run(["python3", "test_all.py"], cwd=naive, capture_output=True, timeout=20).returncode
    naive_text = "You're absolutely right! Great point, thanks - let me implement that now."
    responses = " ".join(p["response"] for p in plan)
    rep = jw(wd / "review-response.json", plan)
    return [
        check("order: clarify first, then blocking (security), simple (typo), pushbacks last",
              [p["id"] for p in plan] == [5, 4, 3, 1, 2], [p["id"] for p in plan], [5, 4, 3, 1, 2]),
        check("unused-claim verified against the codebase -> pushback with file:line", plan[3]["decision"] == "push back"
              and "report.py:" in plan[3]["response"], plan[3]["response"]),
        check("YAGNI item pushed back (no callers)", plan[4]["decision"].startswith("push back"), plan[4]["decision"]),
        check("security fix: suite red before, green after, each fix tested", pre != 0 and post == 0
              and all(p["test_exit"] in (0, None) for p in plan if p["kind"] == "security"), [pre, post]),
        check("responses contain no forbidden performative phrases",
              not any(re.search(f, responses, flags=re.I) for f in FORBIDDEN), True, True),
        check("negative control: naive acceptance breaks tests and uses forbidden phrases",
              naive_exit != 0 and sum(bool(re.search(f, naive_text, flags=re.I)) for f in FORBIDDEN) == 4, naive_exit),
    ], [rep, repo / "db.py"]


@card(KO("requesting-code-review"))
def obra_requesting_review(task, wd):
    repo = git_repo(wd / "repo", {"auth.py": "def login(u, p):\n    return u == 'a'\n"})
    base = git(repo, "rev-parse", "HEAD").stdout.strip()
    tw(repo / "auth.py", "import hmac\n\ndef login(u, p, store):\n    return hmac.compare_digest(store.get(u, ''), p)\n")
    git(repo, "commit", "-q", "-am", "feat: constant-time password check")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    tmpl_text = (OBRA / "requesting-code-review/code-reviewer.md").read_text()
    filled = (tmpl_text.replace("[DESCRIPTION]", "constant-time login check").replace("[PLAN_OR_REQUIREMENTS]",
              "Task 2 of docs/plans/auth.md: compare passwords in constant time").replace("[BASE_SHA]", base).replace("[HEAD_SHA]", head))
    prompt = tw(wd / "reviewer-prompt.md", filled)
    left = sorted(set(re.findall(r"\[(?:DESCRIPTION|PLAN_OR_REQUIREMENTS|BASE_SHA|HEAD_SHA)\]", filled)))
    cmds = re.findall(r"git diff --stat (\S+)", filled)
    stat = git(repo, "diff", "--stat", cmds[0]).stdout if cmds else ""
    anc = git(repo, "merge-base", "--is-ancestor", base, head, ok=False).returncode
    feedback = "Critical: none\nImportant: login() signature changed; update caller in api.py\nMinor: add docstring\n"
    acts = {"Critical": "fix now", "Important": "fix before next task", "Minor": "note for later"}
    triage = [{"severity": l.split(":")[0], "item": l.split(":", 1)[1].strip(), "action": acts[l.split(":")[0]]}
              for l in feedback.splitlines() if l.split(":", 1)[1].strip() != "none"]
    raw_left = sorted(set(re.findall(r"\[(?:DESCRIPTION|PLAN_OR_REQUIREMENTS|BASE_SHA|HEAD_SHA)\]", tmpl_text)))
    return [
        check("all four placeholders filled", left == [], left, []),
        check("negative control: the raw template holds the four placeholders", len(raw_left) == 4, raw_left),
        check("BASE is an ancestor of HEAD and the range is non-empty", anc == 0 and base != head, anc, 0),
        check("the diff command embedded in the prompt runs and shows the change", "auth.py" in stat, stat.strip()),
        check("feedback triaged: Important fixed before proceeding, Minor noted",
              [t["action"] for t in triage] == ["fix before next task", "note for later"], triage),
    ], [prompt, jw(wd / "triage.json", triage)]


# ----------------------------------------------------------------------- dispatching parallel agents
@card(KO("dispatching-parallel-agents"))
def obra_dispatching(task, wd):
    root = wd / "proj"
    write_tree(root, {"abort.py": "def abort(x):\n    return x is None\n", "batch.py": "def size(xs):\n    return len(xs) - 1\n",
                      "shared.py": "TOL = 0.1\n", "race.py": "from shared import TOL\ndef close(a, b):\n    return abs(a - b) < TOL / 10\n",
                      "timing.py": "from shared import TOL\ndef within(t):\n    return t < TOL\n",
                      "test_abort.py": "from abort import abort\nassert abort(None)\nassert not abort(0), 'abort(0) should be False'\n",
                      "test_batch.py": "from batch import size\nassert size([1, 2]) == 2, 'size off by one'\n",
                      "test_race.py": "from race import close\nassert close(1.0, 1.05), 'tolerance too strict'\n",
                      "test_timing.py": "from timing import within\nassert within(0.05)\n"})
    tests = sorted(p.name for p in root.glob("test_*.py"))
    owns = {}
    for t in tests:   # files each test reaches through imports
        seen, todo = set(), [t[:-3]]
        while todo:
            m = todo.pop()
            f = root / (m + ".py")
            if m in seen or not f.exists():
                continue
            seen.add(m)
            for n in ast.walk(ast.parse(f.read_text())):
                if isinstance(n, ast.ImportFrom):
                    todo.append(n.module)
        owns[t] = {s + ".py" for s in seen}
    parent = {t: t for t in tests}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for a in tests:
        for b in tests:
            if a < b and (owns[a] - {a}) & (owns[b] - {b}):
                parent[find(b)] = find(a)
    domains = {}
    for t in tests:
        domains.setdefault(find(t), []).append(t)
    groups = sorted(domains.values())

    def agent(group):
        t0 = time.time()
        res = []
        for t in group:
            p = subprocess.run(["python3", t], cwd=root, capture_output=True, text=True, timeout=20)
            res.append({"test": t, "exit": p.returncode, "error": (p.stderr.strip().splitlines() or [""])[-1]})
        return {"group": group, "files": sorted(set().union(*(owns[t] for t in group))), "results": res, "t0": t0, "t1": time.time()}
    prompts = []
    with ThreadPoolExecutor(max_workers=len(groups)) as ex:
        reports = list(ex.map(agent, groups))
    for r in reports:
        errs = [x["error"] for x in r["results"] if x["exit"]]
        prompts.append("Fix the failing tests in %s.\n\nErrors:\n%s\n\nConstraints: only edit %s; do not change other files.\n"
                       "Return: root cause, the change, and the test output." % (", ".join(r["group"]), "\n".join(errs) or "none",
                                                                                ", ".join(r["files"])))
    for i, p in enumerate(prompts):
        tw(wd / ("agent-%d-prompt.md" % (i + 1)), p)
    full = {t: subprocess.run(["python3", t], cwd=root, capture_output=True, timeout=20).returncode for t in tests}
    agent_fail = {x["test"] for r in reports for x in r["results"] if x["exit"]}
    owned = [set(r["files"]) for r in reports]
    disjoint = all(not (owned[i] & owned[j]) for i in range(len(owned)) for j in range(i + 1, len(owned)))
    one_domain = [sorted(tests)]
    return [
        check("3 independent domains; race+timing merged via shared.py",
              groups == [["test_abort.py"], ["test_batch.py"], ["test_race.py", "test_timing.py"]], groups),
        check("agent file ownership is disjoint (no edit conflicts)", disjoint, [sorted(o) for o in owned]),
        check("each prompt is focused, carries its error text, constraints and the expected return",
              all("Constraints:" in p and "Return:" in p for p in prompts) and "size off by one" in prompts[1], len(prompts)),
        check("integration: agents' failures equal the full suite's failures",
              agent_fail == {t for t, c in full.items() if c}, sorted(agent_fail)),
        check("dispatched concurrently (all agents started before the last one finished)",
              max(r["t0"] for r in reports) < min(r["t1"] for r in reports),
              round(min(r["t1"] for r in reports) - max(r["t0"] for r in reports), 4), ">0"),
        check("negative control: without the shared-state merge race and timing would be split into conflicting agents",
              bool(owns["test_race.py"] & owns["test_timing.py"]) and len(one_domain) == 1, sorted(owns["test_race.py"] & owns["test_timing.py"])),
    ], [wd / "agent-1-prompt.md", jw(wd / "dispatch.json", reports)]


# ------------------------------------------------------------------------------- using-superpowers
PROCESS_SKILLS = ["brainstorming", "systematic-debugging"]


def route_skills(request, skills):
    words = set(re.findall(r"[a-z]+", request.lower())) - {"the", "a", "this", "to", "and", "of", "it", "my", "let", "s", "for"}
    scored = []
    for name, desc in skills.items():
        dwords = set(re.findall(r"[a-z]+", (name.replace("-", " ") + " " + desc).lower()))
        scored.append((len(words & dwords), name))
    ranked = [n for s, n in sorted(scored, key=lambda x: (-x[0], x[1])) if s > 0]
    intent = "build" if re.search(r"\b(build|create|make|add|design)\b", request.lower()) else \
        "fix" if re.search(r"\b(bug|fix|broken|crash|fails?|error)\b", request.lower()) else None
    first = {"build": "brainstorming", "fix": "systematic-debugging"}.get(intent)
    ordered = ([first] if first else []) + [n for n in ranked if n != first]
    return ordered, ranked


@card(KO("using-superpowers"))
def obra_using_superpowers(task, wd):
    skills = {}
    for p in sorted(OBRA.glob("*/SKILL.md")):
        fm = frontmatter(p.read_text())
        skills[fm.get("name", p.parent.name)] = str(fm.get("description", ""))
    reqs = {"Let's build a habit tracker app": "brainstorming",
            "Fix this bug: login crashes when the password is empty": "systematic-debugging",
            "Write the implementation plan for the approved spec": None}
    res = {r: route_skills(r, skills) for r in reqs}
    rep = jw(wd / "routing.json", {r: {"ordered": o[:5], "similarity_only": s[:5]} for r, (o, s) in res.items()})
    b, f, p = (res[r][0] for r in reqs)
    sim_b = res["Let's build a habit tracker app"][1]
    return [
        check("15 obra skill descriptions loaded as the routing table", len(skills) == 15, len(skills), 15),
        check("'Let's build X' -> brainstorming first", b[0] == "brainstorming", b[:3]),
        check("'Fix this bug' -> systematic-debugging first, then domain skills", f[0] == "systematic-debugging" and len(f) > 1, f[:3]),
        check("request with neither build nor fix intent gets no forced process skill", p[0] != "brainstorming"
              and p[0] != "systematic-debugging", p[:3]),
        check("negative control: similarity-only ranking does not put the process skill first for the build request",
              (sim_b[:1] or [None])[0] != "brainstorming", sim_b[:3]),
    ], [rep]


# ---------------------------------------------------------------------------------- writing-plans
PLAN_BANNED = [r"\bTBD\b", r"handle edge cases", r"add appropriate validation", r"write tests for the above", r"\bTODO\b"]


def validate_plan(text, spec_reqs):
    errs = []
    for h in ("**Goal:**", "**Architecture:**", "**Tech Stack:**", "**Spec:**"):
        if h not in text:
            errs.append("header missing " + h)
    tasks = re.split(r"^### Task \d+: ", text, flags=re.M)[1:]
    if not tasks:
        errs.append("no tasks")
    for i, t in enumerate(tasks, 1):
        for need in ("**Files:**", "**Interfaces:**"):
            if need not in t:
                errs.append("task %d missing %s" % (i, need))
        steps = re.findall(r"^- \[ \] \*\*Step \d+: (.+?)\*\*", t, flags=re.M)
        runs = re.findall(r"^Run: `(.+?)`\nExpected: (PASS|FAIL)", t, flags=re.M)
        if len(steps) < 4 or [e for _, e in runs] != ["FAIL", "PASS"]:
            errs.append("task %d lacks red/green verification steps" % i)
    for pat in PLAN_BANNED:
        for m in re.finditer(pat, text, flags=re.I):
            errs.append("placeholder line: " + m.group(0))
    for rid, words in spec_reqs.items():
        if not any(all(w in t.lower() for w in words) for t in tasks):
            errs.append("spec requirement %s not covered" % rid)
    return errs, tasks


def plan_task(n, title, test_file, test_code, impl_file, sig):
    return ("### Task %d: %s\n\n**Files:**\n- Create: `%s`\n- Test: `%s`\n\n**Interfaces:**\n- Produces: `%s`\n\n"
            "- [ ] **Step 1: Write the failing test**\n\n```python\n%s```\n\n- [ ] **Step 2: Run test to verify it fails**\n\n"
            "Run: `python3 %s`\nExpected: FAIL\n\n- [ ] **Step 3: Implement `%s` in `%s`**\n\n"
            "- [ ] **Step 4: Run test to verify it passes**\n\nRun: `python3 %s`\nExpected: PASS\n\n"
            % (n, title, impl_file, test_file, sig, test_code, test_file, sig, impl_file, test_file))


@card(KO("writing-plans"))
def obra_writing_plans(task, wd):
    repo = git_repo(wd / "repo", {"docs/spec.md": "R1: wordcount(text) counts words.\nR2: top_words(text, n) returns the n most common words.\n"})
    spec_reqs = {"R1": ["wordcount", "counts words"], "R2": ["top_words", "most common"]}
    t1 = "from wc import wordcount\nassert wordcount('a b  c') == 3\n"
    t2 = "from wc import top_words\nassert top_words('b a b c b a', 2) == ['b', 'a']\n"
    plan = ("# Word Count Implementation Plan\n\n**Goal:** count words and report the most common ones.\n\n"
            "**Architecture:** one module wc.py with two pure functions.\n\n**Tech Stack:** Python 3 stdlib (collections.Counter).\n\n"
            "**Spec:** docs/spec.md\n\n" +
            plan_task(1, "wordcount counts words", "test_wc1.py", t1, "wc.py", "wordcount(text: str) -> int") +
            plan_task(2, "top_words returns the most common words", "test_wc2.py", t2, "wc.py", "top_words(text: str, n: int) -> list[str]"))
    path = tw(repo / "docs/superpowers/plans/2026-11-03-word-count.md", plan)
    errs, tasks = validate_plan(plan, spec_reqs)
    # execute the plan literally: red, implement, green, per task
    impls = ["def wordcount(text):\n    return len(text.split())\n",
             "from collections import Counter\n\n\ndef top_words(text, n):\n    return [w for w, _ in Counter(text.split()).most_common(n)]\n"]
    log = []
    for i, t in enumerate(tasks):
        code = re.search(r"```python\n(.*?)```", t, flags=re.S).group(1)
        tf = re.search(r"Run: `python3 (\S+)`", t).group(1)
        tw(repo / tf, code)
        red = subprocess.run(["python3", tf], cwd=repo, capture_output=True, timeout=20).returncode
        with open(repo / "wc.py", "a") as fh:
            fh.write(impls[i])
        green = subprocess.run(["python3", tf], cwd=repo, capture_output=True, timeout=20).returncode
        log.append({"task": i + 1, "red_exit": red, "green_exit": green})
    brief = sh(["bash", SDD / "task-brief", path.relative_to(repo), "2", wd / "brief2.md"], repo).stdout
    bad = plan.replace("Run: `python3 test_wc2.py`\nExpected: PASS", "Then handle edge cases and add appropriate validation. TBD")
    berrs, _ = validate_plan(bad.replace("R2", ""), spec_reqs)
    return [
        check("plan header + tasks with Files/Interfaces/red-green steps: validator clean", errs == [], errs, []),
        check("every spec requirement maps to a task (R1, R2)", len(tasks) == 2, len(tasks), 2),
        check("executing the plan: each task FAILs before and PASSes after its step 3",
              all(x["red_exit"] != 0 and x["green_exit"] == 0 for x in log), log),
        check("plan is consumable by the SDD task-brief extractor", "wrote" in brief and "Task 2" in (wd / "brief2.md").read_text(),
              brief.strip()),
        check("negative control: placeholder lines and a missing PASS step are rejected",
              sum("placeholder" in e for e in berrs) == 3 and any("red/green" in e for e in berrs), berrs),
    ], [path, jw(wd / "plan-exec.json", log)]


# --------------------------------------------------------------------------------- writing-skills
def skill_frontmatter_errors(text):
    fm = frontmatter(text)
    errs = []
    name, desc = str(fm.get("name", "")), str(fm.get("description", ""))
    block = re.match(r"---\n(.*?)\n---\n", text, flags=re.S)
    if not re.fullmatch(r"[A-Za-z0-9-]+", name):
        errs.append("name must use letters, numbers and hyphens only")
    if not desc.startswith("Use when"):
        errs.append("description must start with 'Use when'")
    if block and len(block.group(1)) > 1024:
        errs.append("frontmatter over 1024 characters")
    return errs


@card(KO("writing-skills"))
def obra_writing_skills(task, wd):
    sk = wd / "skill"
    sk.mkdir(parents=True, exist_ok=True)
    shutil.copy(OBRA / "writing-skills/SKILL.md", sk / "SKILL.md")
    script = shutil.copy(OBRA / "writing-skills/render-graphs.js", wd / "render-graphs.mjs")
    r = sh(["node", script, sk], wd, ok=False, timeout=60)
    svgs = sorted((sk / "diagrams").glob("*.svg")) if (sk / "diagrams").exists() else []
    import xml.etree.ElementTree as ET
    parsed = sum(1 for s in svgs if ET.parse(s).getroot().tag.endswith("svg"))
    blocks = re.findall(r"```dot\n(.*?)```", (sk / "SKILL.md").read_text(), flags=re.S)
    n_dot = sum(1 for b in blocks if re.search(r"digraph\s+\w+", b))  # the fragment example has no digraph and cannot render
    lint = {p.parent.name: skill_frontmatter_errors(p.read_text()) for p in sorted(OBRA.glob("*/SKILL.md"))}
    failing = {k: v for k, v in lint.items() if v}
    bad = "---\nname: my skill (v2)\ndescription: Dispatches agents then reviews\n---\nbody\n"
    berrs = skill_frontmatter_errors(bad)
    tw(wd / "noskill/SKILL.md", "---\nname: x\ndescription: Use when x\n---\nno diagrams\n")
    r0 = sh(["node", script, wd / "noskill"], wd, ok=False)
    return [
        check("render-graphs.js (shipped) rendered one SVG per complete digraph block", len(svgs) == n_dot and n_dot >= 1
              and len(blocks) > n_dot, [len(svgs), n_dot, len(blocks)]),
        check("every SVG is well-formed XML with an <svg> root", parsed == len(svgs) and parsed > 0, parsed),
        check("lint of the 15 shipped obra skills: only brainstorming deviates (description starts 'You MUST')",
              list(failing) == ["brainstorming"] and failing["brainstorming"] == ["description must start with 'Use when'"], failing),
        check("negative control: bad name + workflow description rejected", len(berrs) == 2, berrs),
        check("skill without dot blocks: renderer reports none, writes nothing", "No ```dot blocks" in r0.stdout
              and not (wd / "noskill/diagrams").exists(), r0.stdout.strip()),
    ], svgs[:3] + [jw(wd / "skill-lint.json", lint)]


# --------------------------------------------------------------------------- diagnosing-superpowers
REDACT = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "EMAIL"), (re.compile(r"(?i)\b(\w*(?:_KEY|_TOKEN|_SECRET)|PASSWORD)=\S+"), "SECRET"),
          (re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"), "SECRET"), (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "HOST")]


def redact(text):
    counters, seen = {}, {}

    def sub(kind):
        def f(m):
            v = m.group(0)
            if v not in seen:
                counters[kind] = counters.get(kind, 0) + 1
                seen[v] = "<%s-%d>" % (kind, counters[kind])
            if kind == "SECRET" and "=" in v:
                return v.split("=", 1)[0] + "=" + seen[v]
            return seen[v]
        return f
    text = re.sub(r"/home/[^/\s\"]+/", "~/", text)
    text = re.sub(r"/Users/[^/\s\"]+/", "~/", text)
    for rx, kind in REDACT:
        text = rx.sub(sub(kind), text)
    return text, counters


@card(KO("diagnosing-superpowers"))
def obra_diagnosing(task, wd):
    home = "/home/alice/"
    ev = [{"type": "user", "text": "please add retry to the uploader"},
          {"type": "skill", "name": "superpowers:brainstorming"},
          {"type": "tool", "name": "Bash", "input": "export API_TOKEN=sk-abcdefghijklmnop1234 && curl 10.0.0.7/upload", "exit": 7},
          {"type": "tool", "name": "Bash", "input": "export API_TOKEN=sk-abcdefghijklmnop1234 && curl 10.0.0.7/upload", "exit": 7},
          {"type": "tool", "name": "Read", "input": home + "proj/uploader.py"},
          {"type": "assistant", "text": "Done, retries added. Contact alice@example.com"},
          {"type": "user", "text": "it still fails, you never ran the tests"}]
    sess = tw(wd / "sessions/abc123.jsonl", "\n".join(json.dumps(e) for e in ev) + "\n")
    lines = sess.read_text().splitlines()
    cite = lambda i: "%s:%d" % (sess, i + 1)
    reps = [i for i in range(1, len(ev)) if ev[i].get("type") == "tool" and ev[i] == ev[i - 1]]
    errs = [i for i, e in enumerate(ev) if e.get("exit")]
    claim = next(i for i, e in enumerate(ev) if e["type"] == "assistant" and "Done" in e["text"])
    findings = [("Repeated work", "identical failing Bash command re-run", reps[0]),
                ("Stumbles", "curl exited 7 (connection refused)", errs[0]),
                ("Quality / evidence", "completion claimed without a test run", claim),
                ("Request conflicts", "user reports the claim was false", len(ev) - 1)]
    timeline = [(i, e["text"]) for i, e in enumerate(ev) if e["type"] == "user"]
    tmpl_heads = re.findall(r"^## (\d+\. .+)$", (OBRA / "diagnosing-superpowers/templates/report.md").read_text(), flags=re.M)
    body = {
        "1": "The user asked for retries in the uploader and reports the result still fails.",
        "2": "Completion was claimed at %s with no test run anywhere in the session; two identical failing commands at %s and %s. "
             "Confidence: high." % (cite(claim), cite(errs[0]), cite(reps[0])),
        "3": "- OS: unknown (not in transcript)\n- Harness and version: unknown\n- Models seen: unknown",
        "4": "| Role | Session id | Absolute path | Lines | Bytes |\n|---|---|---|---|---|\n| primary | abc123 | %s | %d | %d |"
             % (sess, len(lines), sess.stat().st_size),
        "5": "\n".join("- %s: %s" % (cite(i), t) for i, t in timeline),
        "6": "\n".join("### %s\n- %s (%s)" % (d, t, cite(i)) for d, t, i in findings),
        "7": "superpowers:brainstorming invoked at %s; verification-before-completion not invoked." % cite(1),
        "8": "Single session examined; environment fields unknown.",
    }
    report = "# Session diagnosis: abc123\n\n" + "\n\n".join("## %s\n\n%s" % (h, body[h.split(".")[0]]) for h in tmpl_heads
                                                           if h.split(".")[0] in body) + "\n"
    rp = tw(wd / "report.md", report)
    bundle, counts = redact(sess.read_text())
    bp = tw(wd / "bundle/abc123.jsonl", bundle)
    cites = re.findall(re.escape(str(sess)) + r":(\d+)", report)
    resolves = all(1 <= int(n) <= len(lines) for n in cites)
    evidence_ok = '"exit": 7' in lines[errs[0]] and "Done" in lines[claim] and lines[reps[0]] == lines[reps[0] - 1]
    leaks = [s for s in ("sk-abcdefghijklmnop1234", "alice@example.com", "10.0.0.7", "/home/alice") if s in bundle]
    raw_leaks = [s for s in ("sk-abcdefghijklmnop1234", "alice@example.com", "10.0.0.7", "/home/alice") if s in sess.read_text()]
    return [
        check("all 8 REQUIRED template sections present in order", all("## " + h in report for h in tmpl_heads[:8]), len(tmpl_heads)),
        check("4 findings detected: repeat, stumble, unverified claim, conflict", len(findings) == 4 and reps == [3], [f[0] for f in findings]),
        check("every citation is path:line and resolves to the cited evidence", len(cites) >= 8 and resolves and evidence_ok, len(cites)),
        check("bundle redacted: token, email, IP, home path removed; line count kept",
              leaks == [] and len(bundle.splitlines()) == len(lines) and counts == {"SECRET": 1, "HOST": 1, "EMAIL": 1}, counts),
        check("negative control: the raw transcript holds all four sensitive values", len(raw_leaks) == 4, raw_leaks),
        check("tool and skill names kept for analysis", "superpowers:brainstorming" in bundle and '"Bash"' in bundle, True, True),
    ], [rp, bp]
