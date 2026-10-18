#!/usr/bin/env python3
"""KOSIF Superpowers: opt-in, evidence-bounded REA CLI bridge.

Never installs tools or executes inspections without --authorized and --run.
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
# Every REA command (153 in v6.7.0) is catalogued as a power record; `catalog` lists them with their status.
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


def node_ready(version):
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?", version.strip())
    if not match:
        return False
    major, minor, _ = map(int, match.groups())
    return (major == 22 and minor >= 19) or (major == 24 and minor >= 11) or major >= 26


def environment():
    node = shutil.which("node")
    rea = shutil.which("rea")
    version = "unknown"
    if node:
        try:
            response = subprocess.run([node, "--version"], capture_output=True,
                                      text=True, stdin=subprocess.DEVNULL, timeout=3, check=False)
            version = response.stdout.strip()[:40] if response.returncode == 0 else "unknown"
        except (OSError, subprocess.TimeoutExpired):
            pass
    return {"rea_installed": bool(rea), "node_version": version,
            "node_compatible": node_ready(version), "verified_analysis": False}


def inspect_plan(kind, target):
    if kind in STATIC_COMMANDS:
        path = Path(target).expanduser().resolve()
        if not path.exists():
            return {"status": "target_missing", "kind": kind,
                    "analysis_executed": False, "verified": False}
        return {"status": "plan_only", "kind": kind, "target": str(path),
                "command": ["rea", STATIC_COMMANDS[kind], str(path), "--json"],
                "analysis_executed": False, "verified": False,
                "required_evidence": ["command_exit_code", "structured_result", "result_file_sha256", "independent_validation"],
                "source": SOURCE}
    if kind in DOCUMENTED_ONLY:
        return {"status": "provider_or_manual_workflow_required", "kind": kind,
                "reference": SOURCE + "/blob/main/" + DOCUMENTED_ONLY[kind],
                "analysis_executed": False, "verified": False}
    return {"status": "unsupported_kind", "kind": kind, "analysis_executed": False, "verified": False}


def run_static(kind, target, output, authorized):
    plan = inspect_plan(kind, target)
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
        proc = subprocess.run(plan["command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL, timeout=120, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": type(exc).__name__, "analysis_executed": False, "verified": False}
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
    planned.add_argument("kind", choices=sorted(set(STATIC_COMMANDS) | set(DOCUMENTED_ONLY)))
    planned.add_argument("target")
    run = sub.add_parser("run")
    run.add_argument("kind", choices=sorted(STATIC_COMMANDS))
    run.add_argument("target")
    run.add_argument("--output")
    run.add_argument("--authorized", action="store_true")
    args = parser.parse_args()
    if args.action == "doctor":
        result = {"status": "environment_probe_only", **environment(), "source": SOURCE}
    elif args.action == "catalog":
        result = catalog(args.query)
    elif args.action == "plan":
        result = inspect_plan(args.kind, args.target)
    else:
        result = run_static(args.kind, args.target, args.output, args.authorized)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] not in {"command_failed", "non_json_response", "output_write_failed"} else 1


if __name__ == "__main__":
    sys.exit(main())
