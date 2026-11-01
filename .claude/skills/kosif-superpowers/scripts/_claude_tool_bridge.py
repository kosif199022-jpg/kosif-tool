#!/usr/bin/env python3
"""Claude Skill-to-Tool bridge: discovery, honest planning and opt-in MCP execution.

Skills become Claude-discoverable instructions, NOT arbitrary executable code.
MCP exposes four stable tools rather than advertising thousands of unverified
catalog cards as runtime tools. Python stdlib only; no network listener.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import zipfile
from pathlib import Path

import black_dragon as dragon
import _black_dragon_brain as brain
import _claude_reviewed_router as reviewed
import _claude_skill_tool_factory as factory

REPO = dragon.REPO
SKILLS = dragon.audit.SKILL.parent
SERVER_NAME = "kosif-superpowers-bridge"
VERSION = "1.2.0"


def inventory():
    return dragon.full_inventory()


def search(query: str, limit: int = 10) -> dict:
    if not isinstance(query, str) or not query.strip() or len(query) > 1000:
        raise ValueError("query must contain 1..1000 characters")
    if not 1 <= limit <= 30:
        raise ValueError("limit must be 1..30")
    entries = inventory()
    details = brain.metadata(entries, dragon.audit.SKILL)
    words = brain.tokens(query)
    found = []
    for key, meta in entries.items():
        description = details.get(key, str(meta.get("text", "")))
        exact = key.casefold() == query.strip().casefold()
        overlap = len(words & brain.tokens(key + " " + description))
        if overlap or exact or query.casefold() in key.casefold():
            found.append({"id": key, "kind": meta.get("kind"),
                          "source": meta.get("source"), "score": overlap + (100 if exact else 0),
                          "description": description[:220]})
    found.sort(key=lambda x: (-x["score"], x["id"]))
    return {"total_catalogued": len(entries), "matching": len(found),
            "results": found[:limit], "meaning": "discoverable; not necessarily executable"}


def describe(identifier: str, max_chars: int = 8000) -> dict:
    if not isinstance(identifier, str) or not 1 <= len(identifier) <= 200:
        raise ValueError("invalid catalog ID")
    if not 500 <= max_chars <= 16000:
        raise ValueError("max_chars must be 500..16000")
    entries = inventory()
    if identifier not in entries:
        raise ValueError("Unknown catalog ID")
    meta = entries[identifier]
    path = dragon._source_path(identifier, meta).resolve()
    if not dragon._inside(path, REPO) or not path.is_file() or path.is_symlink():
        raise ValueError("Source not a safe repository file")
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        excerpt = handle.read(max_chars + 1)
    return {"id": identifier, "kind": meta.get("kind"),
            "source": meta.get("source"), "sha256": dragon.audit.sha256(path),
            "excerpt": excerpt[:max_chars], "truncated": len(excerpt) > max_chars,
            "execution": "This is reference material; execution needs a reviewed adapter and approval"}


def plan(task: str, limit: int = 15) -> dict:
    if not isinstance(task, str) or not task.strip() or len(task) > 4000:
        raise ValueError("task must contain 1..4000 characters")
    if not 1 <= limit <= 30:
        raise ValueError("limit must be 1..30")
    entries = inventory()
    adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
    strategy = brain.plan(task, entries, adapters, skill_root=dragon.audit.SKILL)
    picked = sorted(strategy["items"], key=lambda k: (-strategy["items"][k]["priority"], k))
    return {"task": task, "mode": "pro-max", "inventory_total": len(entries),
            "assigned": strategy["scheduled"], "excluded": strategy["selected_out"],
            "reviewed_adapters": len(adapters), "waves": len(strategy["waves"]),
            "parts": strategy["parts"], "roles": strategy["roles"],
            "candidates": [{"id": k, **strategy["items"][k]} for k in picked[:limit]],
            "truth": "All items assigned; this is planning, not runtime execution"}


def run_pro_max(task: str, job_name: str, allow_execution: bool = False,
                workers: int = 8) -> dict:
    if not isinstance(job_name, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,48}", job_name):
        raise ValueError("job_name must be 1..48 letters, digits, underscores or hyphens")
    if not isinstance(task, str) or not task.strip() or len(task) > 4000:
        raise ValueError("invalid task")
    if not 1 <= workers <= 16:
        raise ValueError("workers must be 1..16 for MCP")
    job = REPO / "out" / "black-dragon-mcp" / job_name
    approved = bool(allow_execution and os.environ.get("KOSIF_ALLOW_ADAPTER_EXECUTION") == "1")
    if allow_execution and not approved:
        raise PermissionError("Set KOSIF_ALLOW_ADAPTER_EXECUTION=1 and launch with --allow-execution")
    # The reviewed registry is inert until BOTH explicit gates are satisfied.
    adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
    result = dragon.run(task, job, adapters, workers, approved, timeout=45, mode="pro-max")
    return {"job": str(job), "report": result, "execution_approved": approved}


def export_skill(name: str, destination: Path, max_mb: int = 128) -> dict:
    """Portable ZIP for Claude's skill uploader, with sources + SHA manifest.

    Never silently omit supporting files; fail rather than generate a broken
    package. This exports one installed native skill at a time.
    """
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}", name):
        raise ValueError("invalid skill name")
    root = (SKILLS / name).resolve()
    if root.parent != SKILLS.resolve() or not (root / "SKILL.md").is_file():
        raise ValueError("Unknown native SKILL.md directory")
    if not 1 <= max_mb <= 512:
        raise ValueError("max_mb must be 1..512")
    destination = destination.resolve()
    if not dragon._inside(destination, REPO / "out"):
        raise ValueError("ZIP destination must be inside repository out/")
    files = []
    size = 0
    for path in sorted(root.rglob("*")):
        if any(p in {"__pycache__", ".git", ".venv", "node_modules", "out"} for p in path.parts):
            continue
        if path.is_symlink():
            raise ValueError("Cannot export symlinked file: " + str(path))
        if not path.is_file():
            continue
        size += path.stat().st_size
        if size > max_mb * 1024 * 1024:
            raise ValueError("Skill exceeds max_mb; no partial ZIP created")
        files.append(path)
    if not files:
        raise ValueError("No files found")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError("Refusing to overwrite existing export")
    manifest = {"skill": name, "files": {}, "format": "claude-skill-zip-v1"}
    # Claude custom skill ZIP: SKILL.md at root, references remain relative.
    try:
        with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                rel = path.relative_to(root).as_posix()
                manifest["files"][rel] = hashlib.sha256(path.read_bytes()).hexdigest()
                archive.write(path, rel)
            archive.writestr("KOSIF_EXPORT_MANIFEST.json",
                             json.dumps(manifest, indent=2, ensure_ascii=False))
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    return {"skill": name, "zip": str(destination), "files": len(files),
            "source_bytes": size, "zip_sha256": dragon.audit.sha256(destination)}


TOOLS = [
    {"name": "kosif_search", "description": "Search installed skills, powers, methods and tool registry by task. Discovery is NOT execution.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"},
                     "limit": {"type": "integer", "minimum": 1, "maximum": 30}},
                     "required": ["query"], "additionalProperties": False}},
    {"name": "kosif_describe", "description": "Read verified source excerpt and SHA-256 for one existing capability ID.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"},
                     "max_chars": {"type": "integer", "minimum": 500, "maximum": 16000}},
                     "required": ["id"], "additionalProperties": False}},
    {"name": "kosif_plan_pro_max", "description": "Exhaustive, evidence-aware Black Dragon Pro Max plan; no executors started.",
     "inputSchema": {"type": "object", "properties": {"task": {"type": "string"},
                     "limit": {"type": "integer", "minimum": 1, "maximum": 30}},
                     "required": ["task"], "additionalProperties": False}},
    {"name": "kosif_toolify_skill", "description": "Statically inspect one installed SKILL.md and find possible CLI tool entrypoints with SHA receipts, missing references and explicit human review requirements. Never imports or executes skill scripts.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"},
                     "script_limit": {"type": "integer", "minimum": 1, "maximum": 600}},
                     "required": ["name"], "additionalProperties": False}},
    {"name": "kosif_verify_skill_package", "description": "Read-only integrity audit of a generated skill ZIP under repository out/ (SHA-256 manifest, unsafe members, bounded size), no extraction or code execution.",
     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}},
                     "required": ["path"], "additionalProperties": False}},
    {"name": "kosif_bridge_doctor", "description": "Read-only check of the reviewed adapter registry, artifact contracts and permission gates; does not run any adapter.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "kosif_route_reviewed", "description": "Find task-matching reviewed adapters and their explicit prerequisites without executing anything.",
     "inputSchema": {"type": "object", "properties": {"task": {"type": "string"},
                     "limit": {"type": "integer", "minimum": 1, "maximum": 20}},
                     "required": ["task"], "additionalProperties": False}},
    {"name": "kosif_execute_reviewed", "description": "Run ONLY explicitly selected reviewed tool IDs; requires server opt-in, environment opt-in, and per-call approval. Writes independently verifiable receipts.",
     "inputSchema": {"type": "object", "properties": {"task": {"type": "string"},
                     "ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 8, "uniqueItems": True},
                     "job_name": {"type": "string"}, "workers": {"type": "integer", "minimum": 1, "maximum": 4},
                     "allow_execution": {"type": "boolean"}},
                     "required": ["task", "ids", "job_name", "allow_execution"], "additionalProperties": False}},
    {"name": "kosif_review_execution", "description": "Independently revalidate a prior selected-tool job and detect tampered or missing receipts.",
     "inputSchema": {"type": "object", "properties": {"job_name": {"type": "string"}},
                     "required": ["job_name"], "additionalProperties": False}},
    {"name": "kosif_run_pro_max", "description": "Write exhaustive Black Dragon assignment/QA report. Reviewed executors run only with both process and environment approvals.",
     "inputSchema": {"type": "object", "properties": {"task": {"type": "string"},
                     "job_name": {"type": "string"}, "workers": {"type": "integer", "minimum": 1, "maximum": 16},
                     "allow_execution": {"type": "boolean"}},
                     "required": ["task", "job_name"], "additionalProperties": False}},
]


def call_tool(name: str, params: dict, process_execution: bool = False) -> dict:
    if not isinstance(params, dict):
        raise ValueError("arguments must be an object")
    definitions = {x["name"]: x for x in TOOLS}
    if name not in definitions:
        raise ValueError("Unknown MCP tool")
    schema = definitions[name]["inputSchema"]
    if set(params) - set(schema["properties"]) or set(schema.get("required", [])) - set(params):
        raise ValueError("Invalid tool arguments")
    if name == "kosif_search":
        return search(params["query"], params.get("limit", 10))
    if name == "kosif_describe":
        return describe(params["id"], params.get("max_chars", 8000))
    if name == "kosif_plan_pro_max":
        return plan(params["task"], params.get("limit", 15))
    if name == "kosif_toolify_skill":
        return factory.inspect(params["name"], params.get("script_limit", 100))
    if name == "kosif_verify_skill_package":
        return factory.verify_zip(Path(params["path"]))
    if name == "kosif_bridge_doctor":
        return factory.doctor()
    if name == "kosif_route_reviewed":
        return reviewed.route(params["task"], params.get("limit", 8))
    if name == "kosif_review_execution":
        return reviewed.review(params["job_name"])
    if name == "kosif_execute_reviewed":
        if params.get("allow_execution") is not True or not process_execution:
            raise PermissionError("Reviewed execution requires per-call allow_execution=true and server --allow-execution")
        return reviewed.execute(params["task"], params["ids"], params["job_name"],
                                permission=True, workers=params.get("workers", 2))
    if params.get("allow_execution") is True and not process_execution:
        raise PermissionError("MCP server started read-only: restart with --allow-execution")
    return run_pro_max(params["task"], params["job_name"],
                       process_execution and params.get("allow_execution") is True,
                       params.get("workers", 8))


def respond(req: dict, process_execution: bool = False) -> dict | None:
    if not isinstance(req, dict) or req.get("jsonrpc") != "2.0":
        return {"jsonrpc": "2.0", "id": req.get("id") if isinstance(req, dict) else None,
                "error": {"code": -32600, "message": "Invalid Request"}}
    if "id" not in req:
        return None  # notifications/initialized, etc.
    rid = req["id"]
    try:
        method = req.get("method")
        if method == "initialize":
            version = req.get("params", {}).get("protocolVersion", "2025-11-25")
            result = {"protocolVersion": version, "capabilities": {"tools": {"listChanged": False}},
                      "serverInfo": {"name": SERVER_NAME, "version": VERSION}}
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = req.get("params", {})
            value = call_tool(params["name"], params.get("arguments", {}), process_execution)
            result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}]}
        else:
            return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
        return {"jsonrpc": "2.0", "id": rid, "result": result}
    except (ValueError, TypeError, KeyError, OSError, PermissionError, zipfile.BadZipFile) as exc:
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32602, "message": str(exc)[:400]}}


def serve(process_execution: bool = False) -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            reply = respond(req, process_execution)
        except json.JSONDecodeError:
            reply = {"jsonrpc": "2.0", "id": None,
                     "error": {"code": -32700, "message": "Parse error"}}
        if reply is not None:
            print(json.dumps(reply, ensure_ascii=False, separators=(",", ":")), flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("inventory")
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=10)
    d = sub.add_parser("describe")
    d.add_argument("id")
    p = sub.add_parser("plan")
    p.add_argument("task")
    si = sub.add_parser("inspect-skill")
    si.add_argument("name")
    si.add_argument("--script-limit", type=int, default=100)
    sf = sub.add_parser("draft-skill-tool")
    sf.add_argument("name")
    sf.add_argument("--out", required=True, type=Path)
    vv = sub.add_parser("verify-skill-zip")
    vv.add_argument("path", type=Path)
    sub.add_parser("doctor")
    rr = sub.add_parser("route-reviewed")
    rr.add_argument("task")
    rr.add_argument("--limit", type=int, default=8)
    rv = sub.add_parser("review-execution")
    rv.add_argument("job_name")
    e = sub.add_parser("export-skill")
    e.add_argument("name")
    e.add_argument("--out", required=True, type=Path)
    e.add_argument("--max-mb", type=int, default=128)
    m = sub.add_parser("serve")
    m.add_argument("--allow-execution", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "serve":
            serve(args.allow_execution)
            return 0
        result = ({"total": len(inventory())} if args.command == "inventory" else
                  search(args.query, args.limit) if args.command == "search" else
                  describe(args.id) if args.command == "describe" else
                  plan(args.task) if args.command == "plan" else
                  factory.inspect(args.name, args.script_limit) if args.command == "inspect-skill" else
                  factory.draft(args.name, args.out) if args.command == "draft-skill-tool" else
                  factory.verify_zip(args.path) if args.command == "verify-skill-zip" else
                  factory.doctor() if args.command == "doctor" else
                  reviewed.route(args.task, args.limit) if args.command == "route-reviewed" else
                  reviewed.review(args.job_name) if args.command == "review-execution" else
                  export_skill(args.name, args.out, args.max_mb))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, PermissionError, zipfile.BadZipFile) as exc:
        print("claude-tool-bridge: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
