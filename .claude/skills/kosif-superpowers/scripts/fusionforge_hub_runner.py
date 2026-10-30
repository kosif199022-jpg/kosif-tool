#!/usr/bin/env python3
"""Run the nodes of a CHOSEN FusionForge v2 recipe through KOSIF Hub, in dependency order, and trace every one.

fusionforge.py plans and records but never executes; hub.py runs one registered tool at a time. This bridge
connects them: it reads a recipe whose plan the user already chose (status planned), orders the plan's nodes by
their edges, runs every `tool:<id>` node with `hub.py run`, checks the files each node declared, records each
node in the recipe with `fusionforge.py trace`, stops at the first failure or blocked node and writes a new
JSON receipt.

    python3 scripts/fusionforge_hub_runner.py --recipe out/fusionforge/P/recipes/FUSE-....json --plan-file io.json \\
        --report out/bridge/dry.json                      # dry run: checks everything, launches nothing
    python3 scripts/fusionforge_hub_runner.py --recipe ... --plan-file io.json --report out/bridge/run1.json --execute

--plan-file maps node IDs to what the node needs and makes (a bare list is just the arguments):

    {"C1": {"args": ["--in", "{U1.card}", "--out", "{out.cut}"], "inputs": ["assets/voice.wav"],
            "outputs": {"cut": "out/job/cut.mp4"}},
     "V1": {"args": ["{C1.cut}", "--report", "{out.qa}"], "outputs": {"qa": "out/job/qa/qa.json"},
            "make_dirs": ["out/job/qa"]}}

{N.name} is output `name` of node N (which must run before this node in the plan), {out.name} this node's own.
Before a node runs, its inputs and every referenced upstream output must exist; its own outputs must not exist
yet (nothing earlier is overwritten). After it exits 0, each output must be a new, non-empty regular file
(and parse, when it is .json), or the node FAILS. make_dirs folders are created just before the node runs. A failed node's outputs are moved to <report>.quarantine/
so the next attempt starts clean; nothing is deleted.

Safety: it never chooses a plan and never grants consent. A tool that is not `ready` in `hub.py doctor`, or
whose safety is network / runs-external-programs, or that has a consent note, stays BLOCKED unless the matching
--allow-* flag is passed, and those flags are only for after the user explicitly approved that step.
method: and human nodes are manual: do the step, record it with `fusionforge.py trace ... --result passed`,
then run the bridge again; it resumes after every node the recipe already shows as passed or skipped. bin:
and mcp: executors are BLOCKED.

EXECUTED means every selected command exited 0 and its declared files passed the structural checks; it is not
QA and never `verified` (that stays `fusionforge.py record` after a real QA). The receipt keeps exit codes,
timings and SHA-256 of stdout/stderr and outputs, never their text, and is never overwritten.
Exit 0 ok, 1 a node failed, 2 blocked or invalid input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_HUB = HERE / "hub.py"
DEFAULT_FF = HERE / "fusionforge.py"
DEFAULT_REGISTRY = HERE.parent / "data" / "tools.json"
SCHEMA = "kosif.hub-run.v1"  # not kosif.fusionforge.*: fusionforge.py refuses its own records as evidence
NODE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,23}\Z")  # fusionforge.py NODE_RX: N01, U1, C1, V1 ...
TOOL = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")  # hub.py ID_RE
NAME = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,31}\Z")
REF = re.compile(r"\{([A-Za-z][A-Za-z0-9_-]{0,23})\.([A-Za-z][A-Za-z0-9_-]{0,31})\}")
SAFE = {"read-only", "writes-files"}
DANGEROUS = {"network", "runs-external-programs"}  # hub.py SAFETY minus SAFE; anything else is unknown
DONE = ("passed", "skipped")  # fusionforge node statuses that let the bridge resume after a node


class Blocked(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def save_json_new(path: Path, value: dict) -> None:
    """Create the file; refuse to overwrite evidence or write through an existing symlink."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------ recipe
def ordered_nodes(recipe: dict) -> list:
    """[(node, [dependency ids])] for the chosen plan, producers before consumers; Blocked when unsafe."""
    if not isinstance(recipe, dict) or recipe.get("schema") != "kosif.fusionforge.recipe.v2":
        raise Blocked("unsupported FusionForge recipe schema (need kosif.fusionforge.recipe.v2)")
    if recipe.get("status") != "planned":
        raise Blocked(f"recipe status is {recipe.get('status')!r}, not 'planned': the user chooses a plan first "
                      "(fusionforge.py choose); this bridge never approves one")
    choice = recipe.get("plan_choice")
    if not isinstance(choice, dict) or choice.get("plan") not in ("A", "B", "C", "D"):
        raise Blocked("no valid user-chosen plan")
    plan_ids = choice.get("nodes")
    if not isinstance(plan_ids, list) or not plan_ids or len(set(map(str, plan_ids))) != len(plan_ids):
        raise Blocked("the chosen plan must list unique nodes")
    plans = recipe.get("plans") if isinstance(recipe.get("plans"), dict) else {}
    # choose copies the plan's nodes (plan D included: it is stored under plans.D), so any difference is an edit
    if (plans.get(choice["plan"]) or {}).get("nodes") != plan_ids:
        raise Blocked("plan_choice nodes differ from the stored plan")
    nodes = recipe.get("nodes")
    if not isinstance(nodes, list) or any(not isinstance(n, dict) or not NODE.fullmatch(str(n.get("id", ""))) for n in nodes):
        raise Blocked("malformed nodes (ids must look like N01, U1, C1: fusionforge.py's node ID rule)")
    mapping = {n["id"]: n for n in nodes}
    if len(mapping) != len(nodes) or not set(plan_ids) <= set(mapping):
        raise Blocked("duplicate or unknown node ID")
    edges = recipe.get("edges", [])
    if not isinstance(edges, list):
        raise Blocked("edges must be a list")
    deps = {nid: set() for nid in plan_ids}
    for e in edges:
        if not isinstance(e, dict):
            raise Blocked("invalid edge")
        a, b = e.get("from"), e.get("to")
        if a in deps and b in deps and a != b and e.get("relation") != "refine":  # refine edges point backwards
            deps[b].add(a)
    pending, out = list(plan_ids), []
    while pending:
        ready = [n for n in pending if not (deps[n] & set(pending))]
        if not ready:
            raise Blocked("the chosen plan's edges form a cycle")
        for n in ready:
            out.append((mapping[n], sorted(deps[n])))
            pending.remove(n)
    return out


def ancestors(nid: str, deps: dict) -> set:
    seen, stack = set(), list(deps.get(nid, ()))
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n)
            stack.extend(deps.get(n, ()))
    return seen


# ------------------------------------------------------------------ plan file (args, inputs, outputs)
def allowed_bases(a) -> list:
    """Where files may live: the working directory, its git checkout and the FusionForge root
    (the same places fusionforge.py trace accepts evidence from)."""
    bases = [Path.cwd()]
    root = a.fusionforge_root or os.environ.get("KOSIF_FUSIONFORGE_ROOT")
    if root:
        bases.append(Path(root).expanduser())
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if top.returncode == 0 and top.stdout.strip():
            bases.append(Path(top.stdout.strip()))
    except (OSError, subprocess.SubprocessError):
        pass
    return [b.resolve() for b in bases]


def inside(path: Path, bases: list) -> bool:
    p = path.expanduser().absolute()
    p = p.parent.resolve() / p.name
    return any(p == b or b in p.parents for b in bases)


def load_plan_file(path, selected: list, deps: dict, bases: list) -> dict:
    """{node: {"args", "inputs", "outputs", "make_dirs"}} with every path and reference checked up front."""
    raw = load_json(path) if path else {}
    if not isinstance(raw, dict):
        raise Blocked("plan file must be a JSON object keyed by node ID")
    stray = sorted(set(raw) - set(selected))
    if stray:
        raise Blocked(f"plan file names nodes outside the chosen plan: {', '.join(map(str, stray))}")
    spec = {}
    for nid in selected:
        v = raw.get(nid, [])
        v = {"args": v} if isinstance(v, list) else v
        if not isinstance(v, dict) or set(v) - {"args", "inputs", "outputs", "make_dirs"}:
            raise Blocked(f"{nid}: use a list of arguments or {{args, inputs, outputs, make_dirs}}")
        args, ins, outs, mk = v.get("args", []), v.get("inputs", []), v.get("outputs", {}), v.get("make_dirs", [])
        if not isinstance(args, list) or any(not isinstance(x, str) for x in args):
            raise Blocked(f"{nid}: args must be a list of literal strings")
        if not isinstance(ins, list) or any(not isinstance(x, str) or not x for x in ins):
            raise Blocked(f"{nid}: inputs must be a list of file paths")
        if not isinstance(outs, dict) or any(not NAME.fullmatch(str(k)) or not isinstance(p, str) or not p for k, p in outs.items()):
            raise Blocked(f"{nid}: outputs must map names to file paths")
        if not isinstance(mk, list) or any(not isinstance(x, str) or not x for x in mk):
            raise Blocked(f"{nid}: make_dirs must be a list of folder paths")
        for p in ins + list(outs.values()) + mk:
            if not inside(Path(p), bases):
                raise Blocked(f"{nid}: {p} is outside the working directory, its git checkout and the FusionForge root")
        spec[nid] = {"args": args, "inputs": [Path(p) for p in ins], "outputs": {k: Path(p) for k, p in outs.items()},
                     "make_dirs": [Path(x) for x in mk]}
    claimed = {}
    for nid in selected:
        for p in spec[nid]["outputs"].values():
            key = str(p.expanduser().absolute())
            if key in claimed:
                raise Blocked(f"{nid} and {claimed[key]} declare the same output file {p}")
            claimed[key] = nid
    for nid in selected:
        for arg in spec[nid]["args"]:
            for src, name in REF.findall(arg):
                if src == "out":
                    if name not in spec[nid]["outputs"]:
                        raise Blocked(f"{nid}: {{out.{name}}} is not one of its outputs")
                elif src not in ancestors(nid, deps):
                    raise Blocked(f"{nid}: {{{src}.{name}}} names a node that does not run before it in this plan")
                elif name not in spec[src]["outputs"]:
                    raise Blocked(f"{nid}: {src} declares no output {name!r}")
    return spec


def resolve_args(nid: str, spec: dict) -> tuple:
    """(argument list with {N.name}/{out.name} replaced by paths, upstream files they refer to)."""
    used = []

    def sub(m):
        src, name = m.groups()
        p = spec[nid]["outputs"][name] if src == "out" else spec[src]["outputs"][name]
        if src != "out":
            used.append(p)
        return str(p)
    return [REF.sub(sub, x) for x in spec[nid]["args"]], used


def check_output(p: Path, started: float) -> str | None:
    """None when p is a new, non-empty regular file (valid JSON for .json); otherwise the problem code."""
    if p.is_symlink():
        return "OUTPUT_SYMLINK"
    if not p.exists():
        return "OUTPUT_MISSING"
    if not p.is_file():
        return "OUTPUT_NOT_FILE"
    st = p.stat()
    if st.st_size == 0:
        return "OUTPUT_EMPTY"
    if st.st_mtime < started - 2:
        return "OUTPUT_STALE"
    if p.suffix.lower() == ".json":
        try:
            load_json(p)
        except (ValueError, UnicodeDecodeError):
            return "OUTPUT_INVALID_JSON"
    return None


def quarantine(paths, folder: Path) -> list:
    """Move whatever a failed node left behind out of the way (never delete)."""
    moved = []
    for p in paths:
        if p.exists() or p.is_symlink():
            folder.mkdir(parents=True, exist_ok=True)
            dest = folder / p.name
            i = 1
            while dest.exists():
                dest, i = folder / f"{p.stem}.{i}{p.suffix}", i + 1
            shutil.move(str(p), str(dest))
            moved.append({"from": str(p), "to": str(dest)})
    return moved


# ------------------------------------------------------------------ processes
def _kill_group(proc: subprocess.Popen) -> None:
    try:
        if os.name == "posix":
            os.killpg(proc.pid, signal.SIGKILL)
        else:
            proc.kill()
    except (ProcessLookupError, PermissionError, OSError):
        pass


def run_process(cmd: list, timeout: int, keep_error_line: bool = False) -> dict:
    """Run cmd; on timeout kill its whole process group (hub.py runs the tool as a child process)."""
    started = time.monotonic()
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                                start_new_session=(os.name == "posix"))
    except OSError as e:
        return {"returncode": None, "error": f"PROCESS_START:{type(e).__name__}", "elapsed_seconds": 0.0, "_out": b""}
    try:
        out, err = proc.communicate(timeout=timeout)
        rc, error = proc.returncode, None
    except subprocess.TimeoutExpired:
        _kill_group(proc)
        out, err = proc.communicate()
        rc, error = None, "TIMEOUT"
    row = {"returncode": rc, "stdout_sha256": digest(out or b""), "stderr_sha256": digest(err or b""),
           "stdout_bytes": len(out or b""), "stderr_bytes": len(err or b""),
           "elapsed_seconds": round(time.monotonic() - started, 3), "_out": out or b""}
    if error:
        row["error"] = error
    if keep_error_line:  # fusionforge.py prints one 'fusionforge: error: CODE: message' line (it refuses credentials)
        lines = [l for l in (err or b"").decode("utf-8", "replace").splitlines() if l.startswith("fusionforge: error:")]
        if lines:
            row["error_line"] = lines[-1][:300]
    return row


def public(row: dict) -> dict:
    return {k: v for k, v in row.items() if not k.startswith("_")}


def check_registry_matches_hub(registry: Path, hub: Path) -> None:
    """hub.py always runs from its own data/tools.json: approving against another file would check the wrong rules."""
    own = hub.resolve().parent.parent / "data" / "tools.json"
    if own.is_file() and own.resolve() != registry.resolve():
        raise Blocked(f"--registry is not the tools.json this hub runs from ({own}); pass that file or omit --registry")


def hub_readiness(a) -> dict:
    """tool id -> {state, missing} from `hub.py doctor --json` (the same check hub.py itself reports)."""
    r = run_process([sys.executable, str(a.hub), "doctor", "--json"], min(a.timeout, 120))
    try:
        data = json.loads(r["_out"].decode("utf-8"))
        return {t["id"]: t for t in data["tools"] if isinstance(t, dict) and isinstance(t.get("id"), str)}
    except (ValueError, KeyError, TypeError, UnicodeDecodeError):
        raise Blocked("hub.py doctor --json gave no readable answer: tool readiness unknown") from None


def ff_base(a) -> list:
    cmd = [sys.executable, str(a.fusionforge)]
    if a.fusionforge_root:
        cmd += ["--root", str(a.fusionforge_root)]
    return cmd + ["--tools-file", str(a.registry)]  # executors are checked against the registry the bridge approved


def ff_recipe(a, recipe: dict) -> dict:
    """The recipe as fusionforge.py sees it at this root, so traces land in the same record that was read."""
    r = run_process(ff_base(a) + ["show", "--project", str(recipe.get("project")), "--id", str(recipe.get("id")), "--json"],
                    min(a.timeout, 120), keep_error_line=True)
    try:
        shown = json.loads(r["_out"].decode("utf-8"))["recipe"]
    except (ValueError, KeyError, TypeError, UnicodeDecodeError):
        raise Blocked("fusionforge.py cannot open this recipe (pass --fusionforge-root, the folder that holds <project>/recipes/): "
                      + r.get("error_line", "no answer")) from None
    if shown.get("plan_choice") != recipe.get("plan_choice") or shown.get("status") != recipe.get("status"):
        raise Blocked("fusionforge.py shows a different version of this recipe at that root")
    return shown


def approval_problem(tool: dict, ready: dict, opts) -> str | None:
    safety = tool.get("safety")
    if safety not in SAFE | DANGEROUS:
        return f"unknown safety category {safety!r}: never treated as safe"
    state = (ready.get(tool["id"]) or {}).get("state")
    if state != "ready":
        miss = ", ".join((ready.get(tool["id"]) or {}).get("missing") or []) or "not reported"
        return f"hub.py doctor: tool is {state or 'unknown'} (missing: {miss}); install only with the user's approval"
    if (safety == "network" or (tool.get("requires") or {}).get("network")) and not opts.allow_network:
        return "network tool: needs --allow-network after the user's explicit approval"
    if safety == "runs-external-programs" and not opts.allow_external:
        return "runs external programs: needs --allow-external after the user's explicit approval"
    if tool.get("consent") and not opts.allow_consent:
        return "tool has a consent note: needs --allow-consent after the user's explicit approval"
    return None


def node_problem(ref, by_id: dict, ready: dict, a) -> str | None:
    if isinstance(ref, str) and (ref == "human" or ref.startswith("method:")):
        return ("MANUAL: a person does this step; then record it with fusionforge.py trace --node ... --result passed "
                "--evidence FILE and run the bridge again (it resumes after passed nodes)")
    if not isinstance(ref, str) or not ref.startswith("tool:"):
        return "bin:/mcp: executors are not run by this bridge"
    tid = ref[len("tool:"):]
    tool = by_id.get(tid) if TOOL.fullmatch(tid) else None
    if tool is None:
        return "tool is not in the Hub registry"
    if tool.get("kind", "cli") != "cli":
        return f"Hub entry is a {tool.get('kind')}, not a runnable CLI"
    return approval_problem(tool, ready, a)


# ------------------------------------------------------------------ run
def execute(a) -> tuple:
    check_registry_matches_hub(a.registry, a.hub)
    bases = allowed_bases(a)
    if a.execute and not inside(a.report, bases):
        raise Blocked("--report must sit inside the working directory, its git checkout or the FusionForge root: "
                      "fusionforge.py trace refuses evidence elsewhere (EVIDENCE_OUTSIDE_ALLOWED)")
    recipe_bytes = a.recipe.read_bytes()
    recipe = json.loads(recipe_bytes)
    registry_bytes = a.registry.read_bytes()
    registry = json.loads(registry_bytes)
    ordered = ordered_nodes(recipe)
    deps = {n["id"]: set(d) for n, d in ordered}
    selected = [n["id"] for n, _ in ordered]
    spec = load_plan_file(a.plan_file, selected, deps, bases)
    tools = registry.get("tools") if isinstance(registry, dict) else None
    if not isinstance(tools, list):
        raise Blocked("registry must contain a tools list")
    by_id = {t.get("id"): t for t in tools if isinstance(t, dict) and isinstance(t.get("id"), str)}
    if len(by_id) != len(tools):
        raise Blocked("duplicate or malformed tool ID in the registry")
    ready = hub_readiness(a)
    if a.execute:
        recipe = ff_recipe(a, recipe)
    status_of = {n["id"]: n.get("status") for n in recipe.get("nodes", []) if isinstance(n, dict)}

    receipt = {"schema": SCHEMA, "recipe_id": recipe.get("id"), "project": recipe.get("project"),
               "plan": recipe["plan_choice"]["plan"], "mode": "execute" if a.execute else "dry-run",
               "recipe_sha256": digest(recipe_bytes), "registry_sha256": digest(registry_bytes),
               "approvals": {"network": a.allow_network, "external": a.allow_external, "consent": a.allow_consent},
               "nodes": [], "status": "PLANNED",
               "limits": ["exit code 0 and the file checks are not proof of quality; QA and fusionforge.py record stay separate steps",
                          "stdout/stderr are hashed, not stored", "nothing is published or deployed"]}
    failed = blocked = False
    for node, nd in ordered:
        nid = node["id"]
        ref = (node.get("executor") or {}).get("ref", "")
        row = {"node": nid, "stage": node.get("stage"), "executor": ref, "depends_on": nd}
        receipt["nodes"].append(row)
        if status_of.get(nid) in DONE:
            row.update(status="ALREADY_DONE", reason=f"the recipe already records this node as {status_of[nid]} (resume)")
            continue
        problem = node_problem(ref, by_id, ready, a)
        if problem:
            row.update(status="BLOCKED", reason=problem)
        else:
            row["tool_id"] = ref[len("tool:"):]
            args, used = resolve_args(nid, spec)
            missing = [str(p) for p in spec[nid]["inputs"] + used if not p.is_file()]
            exists = [str(p) for p in spec[nid]["outputs"].values() if p.exists() or p.is_symlink()]
            if a.execute and missing:
                row.update(status="BLOCKED", reason="input files missing: " + ", ".join(missing))
            elif exists:
                row.update(status="BLOCKED", reason="outputs already exist (never overwritten; move them or pick new paths): " + ", ".join(exists))
            elif not a.execute:
                row.update(status="READY", args=args, reason="dry run: not executed"
                           + (f"; inputs not present yet: {', '.join(missing)}" if missing else ""))
            else:
                run_tool(a, spec, nid, row, args, by_id[row["tool_id"]])
        if row["status"] == "BLOCKED":
            blocked = True
        if a.execute:
            trace_node(a, recipe, node, row)
        if row["status"] == "FAIL":
            failed = True
        if a.execute and row["status"] != "PASS":
            break  # fail closed: a later node may consume what this one should have produced
    receipt["status"] = ("FAILED" if failed else "BLOCKED" if blocked else "EXECUTED" if a.execute else "DRY_RUN_READY")
    receipt["covered_nodes"] = len(receipt["nodes"])
    receipt["selected_nodes"] = len(ordered)
    return (1 if failed else 2 if blocked else 0), receipt


def run_tool(a, spec: dict, nid: str, row: dict, args: list, tool: dict) -> None:
    # --yes only reaches hub.py after the matching --allow-* checks passed
    yes = ["--yes"] if (tool.get("consent") or tool.get("safety") in DANGEROUS) else []
    for d in spec[nid]["make_dirs"]:  # some tools refuse a missing output folder, others insist on a new one
        d.mkdir(parents=True, exist_ok=True)
    started = time.time()
    out = run_process([sys.executable, str(a.hub), "run", *yes, row["tool_id"], "--", *args], a.timeout)
    row["execution"] = public(out)
    if out["returncode"] != 0:
        row.update(status="FAIL", error_class="timeout" if out.get("error") == "TIMEOUT" else "tool_error",
                   reason=f"hub.py run exit {out['returncode']}" + (f" ({out['error']})" if out.get("error") else ""))
    else:
        files, bad = {}, []
        for name, p in spec[nid]["outputs"].items():
            why = check_output(p, started)
            if why:
                bad.append(f"{name}={p}: {why}")
            else:
                files[name] = {"path": str(p), "bytes": p.stat().st_size, "sha256": file_sha(p)}
        row["outputs"] = files
        if bad:
            row.update(status="FAIL", error_class="wrong_input_kind", reason="exit 0 but declared outputs failed: " + "; ".join(bad))
        else:
            row["status"] = "PASS"
    if row["status"] == "FAIL":
        moved = quarantine(spec[nid]["outputs"].values(), a.report.parent / f"{a.report.stem}.quarantine" / nid)
        if moved:
            row["quarantined"] = moved


def trace_node(a, recipe: dict, node: dict, row: dict) -> None:
    """Record the node in the recipe with fusionforge.py trace. PASS/FAIL carry --result and hashed evidence;
    BLOCKED is noted without a result. A trace that does not land turns the node into FAIL."""
    nid = node["id"]
    cmd = ff_base(a) + ["trace", "--project", str(recipe.get("project")), "--id", str(recipe.get("id")),
                        "--stage", str(node.get("stage")), "--node", nid]
    if row["status"] in ("PASS", "FAIL"):
        evidence = a.report.parent / f"{a.report.stem}.{nid}.json"
        save_json_new(evidence, {"schema": SCHEMA + ".node", "recipe_id": recipe.get("id"), "node": row,
                                 "note": "Hub exit status and structural file checks only; not deliverable verification"})
        outs = ", ".join(f"{k}={v['path']} sha256:{v['sha256'][:12]}" for k, v in (row.get("outputs") or {}).items())
        cmd += ["--action", f"fusionforge_hub_runner: hub.py run {row.get('tool_id')}", "--tool", row["executor"],
                "--result", "passed" if row["status"] == "PASS" else "failed", "--evidence", str(evidence),
                "--observed", (row.get("reason") or "exit 0; declared outputs present, new and non-empty")[:500]]
        if outs:
            cmd += ["--output", outs[:500]]
        if row["status"] == "FAIL":
            cmd += ["--error-class", row.get("error_class") or "tool_error"]
    else:  # BLOCKED: nothing ran, so no result; the note still lands in the recipe
        cmd += ["--action", "fusionforge_hub_runner: not run", "--observed", f"BLOCKED: {row.get('reason', '')}"[:500]]
    t = run_process(cmd, min(a.timeout, 300), keep_error_line=True)
    row["fusionforge_trace"] = public(t)
    if t["returncode"] != 0:
        row["status"] = "FAIL"
        row["reason"] = "fusionforge.py trace failed: the node is not recorded in the recipe"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="fusionforge_hub_runner.py", description=__doc__.split("\n\n")[0],
                                epilog=__doc__.split("\n\n", 1)[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--recipe", type=Path, required=True, help="a planned FusionForge v2 recipe JSON")
    p.add_argument("--report", type=Path, required=True, help="new JSON receipt path (never overwritten)")
    p.add_argument("--plan-file", "--args-file", dest="plan_file", type=Path,
                   help="JSON per node: argument list, or {args, inputs, outputs}")
    p.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="Hub tools.json (default: this skill's)")
    p.add_argument("--hub", type=Path, default=DEFAULT_HUB, help="hub.py to run tools with (default: this skill's)")
    p.add_argument("--fusionforge", type=Path, default=DEFAULT_FF, help="fusionforge.py that records every node (default: this skill's)")
    p.add_argument("--fusionforge-root", type=Path, help="--root passed to fusionforge.py")
    p.add_argument("--execute", action="store_true", help="actually run (default: dry run)")
    p.add_argument("--allow-network", action="store_true", help="only after the user explicitly approved network use")
    p.add_argument("--allow-external", action="store_true", help="only after the user explicitly approved external programs")
    p.add_argument("--allow-consent", action="store_true", help="only after the user explicitly approved the tools' consent notes")
    p.add_argument("--timeout", type=int, default=900, help="seconds per command, 1-7200 (default 900)")
    a = p.parse_args(argv)
    if not 1 <= a.timeout <= 7200:
        p.error("--timeout must be 1..7200")
    if a.report.exists() or a.report.is_symlink():
        p.error(f"report exists: refusing to overwrite evidence ({a.report})")
    try:
        rc, receipt = execute(a)
    except (ValueError, KeyError, TypeError, OSError) as e:  # Blocked and json.JSONDecodeError are ValueErrors
        rc, receipt = 2, {"schema": SCHEMA, "status": "BLOCKED", "error": f"{type(e).__name__}: {e}"}
    save_json_new(a.report, receipt)
    print(json.dumps({"status": receipt["status"], "receipt": str(a.report), "nodes": receipt.get("covered_nodes", 0),
                      **({"error": receipt["error"]} if "error" in receipt else {})}, ensure_ascii=False))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
