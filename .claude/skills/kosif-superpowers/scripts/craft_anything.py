#!/usr/bin/env python3
"""KOSIF Superpowers: opt-in bridge to Craft Anything (storytold/craft-anything), a pure-Rust
inspection engine with ~320 tools for programs, websites, Android/Apple apps, firmware and files.

    craft_anything.py doctor                     # is craft-anything-cli here? its own doctor, summarised
    craft_anything.py tools [QUERY] [--toolset T]  # list the engine's tools (runs `commands`, read-only)
    craft_anything.py plan TOOL [ARGS...]        # the exact argv, nothing run
    craft_anything.py run TOOL [ARGS...] --output FILE [--deep --authorized]
    craft_anything.py triage FILE --output FILE [--deep --authorized]
    craft_anything.py mcp-config                 # MCP server entry for a client (nothing run)
    craft_anything.py install                    # the build commands to show the user (nothing run)
    craft_anything.py --self-test                # known-answer checks against a stub CLI

The binary is found from CRAFT_ANYTHING_CLI, then `craft-anything-cli` on PATH, then ~/.cargo/bin.
This bridge never installs or builds it, never passes --allow-run, and refuses the commands that
start a coding agent or change the machine (rebuild, chat, setup, uninstall, ai, mcp). Clean room
is Craft Anything's default; --deep (reading a target's code) needs --authorized, the user's
statement that they own the target or may inspect it. A run's stdout goes to a new --output file
(exclusive create) and only its sha256, size and a short summary are printed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

SCHEMA = "kosif.craft-anything-bridge.v1"
SOURCE = "https://github.com/storytold/craft-anything"
BIN_NAME = "craft-anything-cli"
DEFAULT_TIMEOUT = 300
# Commands that start a coding agent, open a server or change the user's apps: not through `run`.
REFUSED = {
    "rebuild": "starts a coding agent that builds a whole project; run it yourself after the user agrees",
    "chat": "asks an AI backend; use the session's own model instead",
    "setup": "registers Craft Anything in the user's agent apps (changes their config)",
    "uninstall": "removes registrations from the user's agent apps",
    "ai": "manages AI backends and keys",
    "mcp": "starts a long-running server; use mcp-config to wire it into a client",
    "help": "use `tools` or `plan`",
}
# Toolsets whose tools run code, attach to a device or trace a process: always need --authorized.
ACTIVE_TOOLSETS = {"runtime", "frida", "adb", "build", "application"}
# Toolsets that change settings, register plugins or drive whole rebuild projects: never through `run`.
REFUSED_TOOLSETS = {"setup": "changes Craft Anything's settings, engines or plugins",
                    "projects": "drives rebuild projects that start a coding agent"}
BUILTINS = {"triage", "report", "capabilities", "doctor", "commands"}
INSTALL = [
    "git clone https://github.com/storytold/craft-anything && cd craft-anything",
    "cargo install --locked --path apps/craft-anything-cli   # needs Rust 1.97+, about 8 min",
    "craft-anything-cli doctor",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def find_binary() -> str | None:
    env = os.environ.get("CRAFT_ANYTHING_CLI")
    if env:
        return env if Path(env).is_file() and os.access(env, os.X_OK) else None
    hit = shutil.which(BIN_NAME)
    if hit:
        return hit
    cargo = Path.home() / ".cargo" / "bin" / BIN_NAME
    return str(cargo) if cargo.is_file() and os.access(cargo, os.X_OK) else None


def _call(argv: list[str], timeout: int) -> subprocess.CompletedProcess:
    return subprocess.run(argv, text=True, capture_output=True, stdin=subprocess.DEVNULL,
                          timeout=timeout, check=False)


def doctor(timeout: int = 120) -> dict:
    binary = find_binary()
    if not binary:
        return {"schema": SCHEMA, "installed": False, "source": SOURCE, "install": INSTALL,
                "note": "craft-anything-cli not found (CRAFT_ANYTHING_CLI, PATH, ~/.cargo/bin)."}
    ver = _call([binary, "--version"], 30)
    out = {"schema": SCHEMA, "installed": True, "binary": binary,
           "version": ver.stdout.strip() or None, "source": SOURCE}
    doc = _call([binary, "doctor"], timeout)
    try:
        report = json.loads(doc.stdout)
    except json.JSONDecodeError:
        out.update(doctor_ok=False, doctor_error=(doc.stderr or doc.stdout)[-400:])
        return out
    checks = report.get("checks") or []
    by = Counter(c.get("status") for c in checks)
    out.update(
        doctor_ok=doc.returncode == 0, healthy=bool(report.get("healthy")),
        status_counts=dict(sorted(by.items())),
        engines_ok=sorted(c["name"].split(":", 1)[1] for c in checks
                          if c.get("name", "").startswith("engine:") and c.get("status") == "ok"),
        mcp_self_test=next((c.get("message") for c in checks if c.get("name") == "mcp:self-test"), None),
        problems=[{"name": c.get("name"), "message": c.get("message")} for c in checks
                  if c.get("status") not in ("ok", "info")],
    )
    return out


def list_tools(query: str = "", toolset: str = "", timeout: int = 60) -> dict:
    binary = find_binary()
    if not binary:
        return {"schema": SCHEMA, "installed": False, "install": INSTALL, "tools": []}
    done = _call([binary, "commands"], timeout)
    rows = json.loads(done.stdout)
    q = query.lower().strip()
    keep = [r for r in rows
            if (not toolset or r.get("toolset") == toolset)
            and (not q or q in (r.get("command", "") + " " + r.get("title", "") + " " + r.get("summary", "")).lower())]
    return {"schema": SCHEMA, "installed": True, "total": len(rows),
            "toolsets": dict(sorted(Counter(r.get("toolset") for r in rows).items())),
            "matched": len(keep),
            "tools": [{"command": r.get("command"), "toolset": r.get("toolset"), "title": r.get("title"),
                       "needs_target": r.get("needs_target"), "summary": (r.get("summary") or "")[:200]}
                      for r in keep]}


def tool_row(binary: str, tool: str, timeout: int = 60) -> dict | None:
    """The engine's own record for TOOL (its toolset decides what it may do), or None if unknown."""
    if tool in BUILTINS:
        return {"command": tool, "toolset": "builtin"}
    try:
        rows = json.loads(_call([binary, "commands"], timeout).stdout)
    except (json.JSONDecodeError, subprocess.TimeoutExpired):
        return None
    return next((r for r in rows if tool in (r.get("command"), r.get("tool"))), None)


def build_argv(binary: str, tool: str, args: list[str], deep: bool) -> list[str]:
    mode = "--deep" if deep else "--clean-room"
    return [binary, "--format", "json", mode, tool, *args]


def plan(tool: str, args: list[str], deep: bool = False) -> dict:
    if tool in REFUSED:
        return {"schema": SCHEMA, "status": "refused", "tool": tool, "reason": REFUSED[tool], "executed": False}
    binary = find_binary()
    row = tool_row(binary, tool) if binary else None
    toolset = (row or {}).get("toolset")
    if toolset in REFUSED_TOOLSETS:
        return {"schema": SCHEMA, "status": "refused", "tool": tool, "reason": REFUSED_TOOLSETS[toolset], "executed": False}
    return {"schema": SCHEMA, "status": "plan_only", "command": build_argv(binary or BIN_NAME, tool, args, deep),
            "toolset": toolset, "known_tool": bool(row) if binary else None,
            "needs_authorized": deep or toolset in ACTIVE_TOOLSETS or (binary is not None and row is None),
            "executed": False}


def run_tool(tool: str, args: list[str], output: str, deep: bool = False, authorized: bool = False,
             timeout: int = DEFAULT_TIMEOUT) -> dict:
    base = {"schema": SCHEMA, "tool": tool, "deep": deep, "executed": False, "verified": False}
    if tool in REFUSED:
        return {**base, "status": "refused", "reason": REFUSED[tool]}
    binary = find_binary()
    if not binary:
        return {**base, "status": "not_installed", "install": INSTALL}
    row = tool_row(binary, tool)
    if row is None:
        return {**base, "status": "unknown_tool", "reason": "not in `craft-anything-cli commands`; see `tools`"}
    toolset = row.get("toolset")
    base["toolset"] = toolset
    if toolset in REFUSED_TOOLSETS:
        return {**base, "status": "refused", "reason": REFUSED_TOOLSETS[toolset]}
    if (deep or toolset in ACTIVE_TOOLSETS) and not authorized:
        return {**base, "status": "authorization_required",
                "reason": "Deep mode or a tool that runs code needs --authorized (the user owns the target or may inspect it)."}
    out = Path(output)
    if not out.parent.is_dir():
        return {**base, "status": "output_folder_missing", "output": str(out)}
    argv = build_argv(binary, tool, args, deep)
    try:
        done = _call(argv, timeout)
    except subprocess.TimeoutExpired:
        return {**base, "status": "timeout", "timeout": timeout}
    data = done.stdout.encode("utf-8")
    try:
        with open(out, "xb") as fh:
            fh.write(data)
    except FileExistsError:
        return {**base, "status": "output_exists", "output": str(out)}
    summary, error = None, None
    try:
        parsed = json.loads(done.stdout)
        if isinstance(parsed, dict):
            summary = parsed.get("summary") or parsed.get("message")
            error = parsed.get("error")
    except json.JSONDecodeError:
        pass
    ok = done.returncode == 0 and not error
    return {**base, "status": "ok" if ok else "tool_error", "executed": True, "exit_code": done.returncode,
            "command": argv, "output": str(out), "bytes": len(data), "sha256": sha256_bytes(data),
            "summary": (str(summary)[:400] if summary else None),
            "error": (error if error else (done.stderr[-400:] if done.returncode else None))}


def mcp_config() -> dict:
    binary = find_binary() or BIN_NAME
    return {"schema": SCHEMA, "executed": False,
            "mcpServers": {"craft-anything": {"command": binary, "args": ["mcp"]}},
            "claude_code": f"claude mcp add craft-anything -- {binary} mcp",
            "note": "Clean room by default; the server lists its tools on connect."}


# --------------------------------------------------------------------------- self-test
STUB = r'''#!/usr/bin/env python3
import json, sys
a = sys.argv[1:]
if a == ["--version"]:
    print("craft-anything-cli 9.9.9"); sys.exit(0)
if a == ["doctor"]:
    print(json.dumps({"healthy": True, "checks": [
        {"name": "binary", "status": "ok", "message": "here"},
        {"name": "engine:gdb", "status": "ok", "message": "GDB"},
        {"name": "engine:ghidra", "status": "info", "message": "missing"},
        {"name": "mcp:self-test", "status": "ok", "message": "MCP server answered (3 tools listed)."}]})); sys.exit(0)
if a == ["commands"]:
    print(json.dumps([
        {"command": "core-target-open", "toolset": "core", "title": "Open", "needs_target": False, "summary": "Open a file"},
        {"command": "core-target-triage", "toolset": "core", "title": "Triage", "needs_target": True, "summary": "First look"},
        {"command": "web-page-show", "toolset": "web", "title": "Page", "needs_target": False, "summary": "Observe a page"},
        {"command": "frida-attach", "toolset": "frida", "title": "Attach", "needs_target": False, "summary": "Trace"},
        {"command": "settings-set", "toolset": "setup", "title": "Set", "needs_target": False, "summary": "Change a setting"}])); sys.exit(0)
if a[:3] == ["--format", "json", "--clean-room"] and a[3] == "triage":
    print(json.dumps({"error": {"kind": "feature_missing"}})); sys.exit(0)
if a[:3] == ["--format", "json", "--deep"] and a[3] == "triage":
    print(json.dumps({"summary": "stub is a program for Linux", "format": "elf"})); sys.exit(0)
print("unknown", a, file=sys.stderr); sys.exit(2)
'''


def self_test() -> int:
    failures = []

    def check(name, cond):
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            failures.append(name)

    with tempfile.TemporaryDirectory() as root:
        stub = Path(root) / BIN_NAME
        stub.write_text(f"#!{sys.executable}\n" + STUB.split("\n", 1)[1], encoding="utf-8")
        stub.chmod(0o755)
        old = os.environ.get("CRAFT_ANYTHING_CLI")
        os.environ["CRAFT_ANYTHING_CLI"] = str(stub)
        try:
            d = doctor()
            check("doctor finds the binary", d["installed"] and d["version"] == "craft-anything-cli 9.9.9")
            check("doctor summarises engines", d["engines_ok"] == ["gdb"] and d["healthy"])
            check("doctor reads the MCP self-test", "3 tools" in (d["mcp_self_test"] or ""))
            t = list_tools("page")
            check("tools counts every row", t["total"] == 5 and t["toolsets"] == {"core": 2, "frida": 1, "setup": 1, "web": 1})
            check("tools filters by text", t["matched"] == 1 and t["tools"][0]["command"] == "web-page-show")
            check("plan runs nothing", plan("triage", ["x"])["executed"] is False)
            check("plan refuses rebuild", plan("rebuild", [])["status"] == "refused")
            r = run_tool("rebuild", [], str(Path(root) / "r.json"))
            check("run refuses rebuild", r["status"] == "refused" and not r["executed"])
            r = run_tool("triage", ["x"], str(Path(root) / "a.json"), deep=True)
            check("deep needs --authorized", r["status"] == "authorization_required")
            r = run_tool("frida-attach", [], str(Path(root) / "f.json"))
            check("active toolset needs --authorized", r["status"] == "authorization_required")
            r = run_tool("settings-set", ["deep_mode", "true"], str(Path(root) / "s.json"), authorized=True)
            check("setup toolset is refused", r["status"] == "refused" and not r["executed"])
            r = run_tool("no-such-tool", [], str(Path(root) / "n.json"), authorized=True)
            check("unknown tool is refused", r["status"] == "unknown_tool")
            check("plan names the toolset", plan("frida-attach", [])["needs_authorized"] is True)
            r = run_tool("triage", ["x"], str(Path(root) / "clean.json"))
            check("clean-room refusal is reported as a tool error", r["status"] == "tool_error" and r["executed"])
            r = run_tool("triage", ["x"], str(Path(root) / "deep.json"), deep=True, authorized=True)
            body = (Path(root) / "deep.json").read_bytes()
            check("deep run writes the output", r["status"] == "ok" and r["sha256"] == sha256_bytes(body))
            check("summary is kept", r["summary"] == "stub is a program for Linux")
            r = run_tool("triage", ["x"], str(Path(root) / "deep.json"), deep=True, authorized=True)
            check("output is never overwritten", r["status"] == "output_exists")
            os.environ["CRAFT_ANYTHING_CLI"] = str(Path(root) / "missing")
            check("missing binary is reported", doctor()["installed"] is False)
        finally:
            if old is None:
                os.environ.pop("CRAFT_ANYTHING_CLI", None)
            else:
                os.environ["CRAFT_ANYTHING_CLI"] = old
    print(json.dumps({"self_test": "pass" if not failures else "fail", "failures": failures}))
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--self-test"]:
        return self_test()
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--self-test", action="store_true", help="known-answer checks against a stub CLI")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor", help="find craft-anything-cli and summarise its doctor")
    t = sub.add_parser("tools", help="list the engine's tools")
    t.add_argument("query", nargs="?", default="")
    t.add_argument("--toolset", default="")
    for name in ("plan", "run"):
        s = sub.add_parser(name, help=f"{name} one engine tool")
        s.add_argument("tool")
        s.add_argument("args", nargs=argparse.REMAINDER)
    tr = sub.add_parser("triage", help="first look at a file")
    tr.add_argument("file")
    for s in (sub.choices["run"], tr, sub.choices["plan"]):
        s.add_argument("--deep", action="store_true", help="Deep mode: read the target's code (needs --authorized)")
    for s in (sub.choices["run"], tr):
        s.add_argument("--output", required=True, help="new JSON file for the tool's stdout")
        s.add_argument("--authorized", action="store_true", help="the user owns the target or may inspect it")
        s.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    sub.add_parser("mcp-config", help="MCP server entry for a client")
    sub.add_parser("install", help="the build commands (nothing is run)")
    a = p.parse_args(argv)
    if a.cmd == "doctor":
        res = doctor()
    elif a.cmd == "tools":
        res = list_tools(a.query, a.toolset)
    elif a.cmd == "plan":
        res = plan(a.tool, a.args, a.deep)
    elif a.cmd == "run":
        res = run_tool(a.tool, a.args, a.output, a.deep, a.authorized, a.timeout)
    elif a.cmd == "triage":
        res = run_tool("triage", [a.file], a.output, a.deep, a.authorized, a.timeout)
    elif a.cmd == "mcp-config":
        res = mcp_config()
    else:
        res = {"schema": SCHEMA, "source": SOURCE, "install": INSTALL, "executed": False}
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("status") in (None, "ok", "plan_only") else 1


if __name__ == "__main__":
    sys.exit(main())
