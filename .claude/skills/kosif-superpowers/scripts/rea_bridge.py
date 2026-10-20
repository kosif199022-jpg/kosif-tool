#!/usr/bin/env python3
"""KOSIF Superpowers: opt-in, evidence-bounded REA CLI bridge.

Never installs tools; an inspection runs only through the `run` subcommand with --authorized.
All stdout payloads stay in a caller-named local file, not the chat log.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

# Only CLI commands documented as static, local inspection in morluto/rea.
STATIC_COMMANDS = {
    "javascript": "analyze-javascript-application",
    "dotnet": "inspect-managed-artifact",
    "dotnet-members": "inspect-managed-members",
    "dotnet-boundaries": "inspect-managed-native-boundaries",
    "sqlite": "inspect-sqlite-database",
    "go": "inspect-go-binary",
    "rust": "inspect-rust-binary",
    "artifact": "inspect-artifact",
    "electron-fuses": "inspect-electron-fuses",
    "android-package": "inspect-android-package",
    "flutter": "identify-flutter-build",
    "dart-aot": "inspect-dart-aot",
    "pe-resources": "inspect-pe-resources",
    "recorded-crash": "inspect-recorded-crash",
}
# Every REA 6.7.0 CLI command (153), MCP-only tool and MCP prompt, plus the KOSIF installer-triage
# additions, is catalogued as a power record; `catalog` lists them all with their status.
CATALOG = Path(__file__).resolve().parent.parent / "data" / "powers" / "software-investigation.json"
DOCUMENTED_ONLY = {
    "native": "docs/native-investigation.md", "apk": "docs/android-analysis.md",
    "website": "docs/browser-observation.md", "wasm": "docs/cli.md",
    "flutter": "docs/flutter-analysis.md", "firmware": "docs/firmware-analysis.md",
    "pcap": "docs/pcap-analysis.md", "android-device": "docs/adb-device-analysis.md",
    "evm": "docs/evm-bytecode.md", "frida": "docs/frida-instrumentation.md", "jeb": "docs/jeb-analysis.md",
    "apple": "docs/apple-application-analysis.md", "harmony": "docs/harmony-analysis.md",
    "process": "docs/process-capture.md", "crash": "docs/recorded-crashes.md", "signal": "docs/signal-recordings.md",
    "electron": "docs/electron-observation.md", "web-captures": "docs/web-network-captures.md",
}
SOURCE = "https://github.com/morluto/rea"
# Windows installers are opaque PEs to REA (no child entries): triage and unpack them first.
TRIAGE_FIRST = {"installer": "installer_triage.py"}
DEFAULT_TIMEOUT = 600   # a 6.7 MB minified Electron main bundle took ~3 min on a laptop (2026-10-18)


def node_ready(version):
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?", version.strip())
    if not match:
        return False
    major, minor, _ = map(int, match.groups())
    return (major == 22 and minor >= 19) or (major == 24 and minor >= 11) or major >= 26


def rea_launcher():
    """argv prefix that runs REA without a shell.

    REA_BIN (absolute path) wins, then `rea` on PATH. On Windows the npm package ships a
    `rea.cmd` shim; batch files re-parse arguments through cmd.exe, so the shim is
    replaced by `node <package>/scripts/rea.mjs` when that file sits beside it.
    """
    env = os.environ.get("REA_BIN")
    found = env if env and Path(env).is_file() else shutil.which("rea")
    if not found:
        return None
    path = Path(found)
    if path.suffix.lower() in (".cmd", ".bat", ".ps1") or os.name == "nt":
        node = shutil.which("node")
        # global prefix: <prefix>/rea.cmd + <prefix>/node_modules/rea-agents; local: node_modules/.bin/rea.cmd
        for mjs in (path.parent / "node_modules" / "rea-agents" / "scripts" / "rea.mjs",
                    path.parent.parent / "rea-agents" / "scripts" / "rea.mjs"):
            if mjs.is_file() and node:
                return [node, str(mjs)]
        if path.suffix.lower() in (".cmd", ".bat", ".ps1"):
            return None   # refuse to pass target paths through cmd.exe
    return [str(path)]


def environment():
    node = shutil.which("node")
    launcher = rea_launcher()
    rea = bool(launcher)
    version = "unknown"
    if node:
        try:
            response = subprocess.run([node, "--version"], capture_output=True,
                                      text=True, stdin=subprocess.DEVNULL, timeout=3, check=False)
            version = response.stdout.strip()[:40] if response.returncode == 0 else "unknown"
        except (OSError, subprocess.TimeoutExpired):
            pass
    return {"rea_installed": bool(rea), "rea_launcher": launcher, "node_version": version,
            "node_compatible": node_ready(version), "verified_analysis": False}


def inspect_plan(kind, target, source_paths=()):
    if kind in TRIAGE_FIRST:
        return {"status": "triage_first", "kind": kind,
                "command": ["python", TRIAGE_FIRST[kind], "scan", str(Path(target).expanduser())],
                "why": "REA reports an NSIS/Inno/UPX installer as one PE with no children; scan, unpack (authorized) and route its payload",
                "analysis_executed": False, "verified": False}
    if kind in STATIC_COMMANDS:
        path = Path(target).expanduser().resolve()
        if not path.exists():
            return {"status": "target_missing", "kind": kind,
                    "analysis_executed": False, "verified": False}
        return {"status": "plan_only", "kind": kind, "target": str(path),
                "command": ["rea", STATIC_COMMANDS[kind], str(path)]
                + [x for sp in (source_paths if kind == "javascript" else ()) for x in ("--source-path", sp)] + ["--json"],
                "analysis_executed": False, "verified": False,
                "required_evidence": ["command_exit_code", "structured_result", "result_file_sha256", "independent_validation"],
                "source": SOURCE}
    if kind in DOCUMENTED_ONLY:
        return {"status": "provider_or_manual_workflow_required", "kind": kind,
                "reference": SOURCE + "/blob/main/" + DOCUMENTED_ONLY[kind],
                "analysis_executed": False, "verified": False}
    return {"status": "unsupported_kind", "kind": kind, "analysis_executed": False, "verified": False}


def run_static(kind, target, output, authorized, timeout=DEFAULT_TIMEOUT, source_paths=()):
    plan = inspect_plan(kind, target, source_paths)
    if plan["status"] != "plan_only":
        return plan
    if not authorized:
        return {"status": "authorization_required", "analysis_executed": False, "verified": False}
    env = environment()
    if not env["rea_installed"] or not env["node_compatible"]:
        return {"status": "rea_runtime_unavailable", "requirements": env,
                "analysis_executed": False, "verified": False}
    if not output:
        return {"status": "output_path_required", "analysis_executed": False, "verified": False}
    dst = Path(output).expanduser()
    if dst.is_symlink() or dst.exists() or not dst.parent.is_dir():
        return {"status": "unsafe_or_existing_output", "analysis_executed": False, "verified": False}
    if dst.resolve() == Path(target).expanduser().resolve():
        return {"status": "output_equals_target", "analysis_executed": False, "verified": False}
    try:
        argv = (env.get("rea_launcher") or ["rea"]) + plan["command"][1:]
        proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": type(exc).__name__, "timeout_s": timeout, "analysis_executed": False, "verified": False}
    if proc.returncode != 0:
        return {"status": "command_failed", "exit_code": proc.returncode,
                "analysis_executed": True, "verified": False}
    try:
        json.loads(proc.stdout)
    except (ValueError, UnicodeDecodeError):
        return {"status": "non_json_response", "analysis_executed": True, "verified": False}
    # Exclusive create: never overwrite existing output and never echo its contents.
    try:
        with dst.open("xb") as f:
            f.write(proc.stdout)
    except OSError:
        return {"status": "output_write_failed", "analysis_executed": True, "verified": False}
    return {"status": "executed_not_verified", "analysis_executed": True,
            "verified": False, "exit_code": proc.returncode,
            "result_file": str(dst.resolve()), "result_sha256": hashlib.sha256(proc.stdout).hexdigest(),
            "result_bytes": len(proc.stdout), "next": "Independently validate findings against the target"}


def catalog(query=""):
    """Read-only listing of the registered REA command powers (no execution, no install)."""
    try:
        rows = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"status": "catalog_missing", "path": str(CATALOG), "analysis_executed": False, "verified": False}
    q = query.lower().strip()
    hits = [{"id": r["id"], "command": r["params"].split("`")[1][4:] if "`rea " in r["params"] else r["name_en"],
             "status": r["status"], "section": r["section"], "needs": r["install"].split("; plus ")[-1] if "; plus " in r["install"] else "REA alone"}
            for r in rows if not q or q in json.dumps(r, ensure_ascii=False).lower()]
    return {"status": "catalog_only", "count": len(hits), "total": len(rows), "powers": hits,
            "analysis_executed": False, "verified": False, "source": SOURCE}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("doctor")
    cat = sub.add_parser("catalog", help="list the catalogued REA commands (status, requirement) without running anything")
    cat.add_argument("query", nargs="?", default="")
    planned = sub.add_parser("plan")
    planned.add_argument("kind", choices=sorted(set(STATIC_COMMANDS) | set(DOCUMENTED_ONLY) | set(TRIAGE_FIRST)))
    planned.add_argument("target")
    planned.add_argument("--source-path", action="append", default=[], help="javascript only: scope REA to these files")
    run = sub.add_parser("run")
    run.add_argument("kind", choices=sorted(STATIC_COMMANDS))
    run.add_argument("target")
    run.add_argument("--output")
    run.add_argument("--authorized", action="store_true")
    run.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="seconds (default %(default)s)")
    run.add_argument("--source-path", action="append", default=[], help="javascript only: scope REA to these files")
    args = parser.parse_args()
    if args.action == "doctor":
        result = {"status": "environment_probe_only", **environment(), "source": SOURCE}
    elif args.action == "catalog":
        result = catalog(args.query)
    elif args.action == "plan":
        result = inspect_plan(args.kind, args.target, args.source_path)
    else:
        result = run_static(args.kind, args.target, args.output, args.authorized, args.timeout, args.source_path)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] not in {"command_failed", "non_json_response", "output_write_failed"} else 1


if __name__ == "__main__":
    sys.exit(main())
