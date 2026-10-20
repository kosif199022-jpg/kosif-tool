#!/usr/bin/env python3
"""KOSIF catalog MCP server — lets any MCP client discover KOSIF tools, powers and guides.

Read-only, stdio, standard library only. It answers questions; it never runs a tool, installs,
writes files or touches the network. (For bounded local file access use the separate, consent-gated
scripts/kosif_remote_superpowers.py.)

    python3 scripts/kosif_mcp.py            # serve MCP over stdio (newline-delimited JSON-RPC 2.0)
    python3 scripts/kosif_mcp.py --selftest # handshake + every tool once, prints a summary, exits 0/1
    python3 scripts/hub.py mcp-config       # client config for this OS

Tools: kosif_find, kosif_tool, kosif_list_tools, kosif_doctor, kosif_search_powers, kosif_power,
kosif_family, kosif_guides, kosif_read_guide. Resources: SKILL.md, references/INDEX.md, manifest.json.
"""
from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
import hub  # noqa: E402
import powers as P  # noqa: E402

VERSION = "1.0.0"
PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")
MAX_DOC_CHARS = 60_000
RESOURCES = {
    "kosif://skill/SKILL.md": ("SKILL.md", "KOSIF Superpowers skill (start here)"),
    "kosif://skill/INDEX.md": ("references/INDEX.md", "Index of every tool, guide and power family"),
    "kosif://skill/manifest.json": ("manifest.json", "Machine-readable manifest: tools, families, guides, counts"),
}


def _schema(name: str, description: str, props: dict = None, required: list = None) -> dict:
    return {"name": name, "description": description,
            "inputSchema": {"type": "object", "properties": props or {}, "required": required or [], "additionalProperties": False},
            "annotations": {"readOnlyHint": True, "openWorldHint": False}}


S = {"type": "string"}
I = {"type": "integer", "minimum": 1, "maximum": 50}
TOOLS = [
    _schema("kosif_find", "Start here. For a task in the user's words (Arabic or English) return the KOSIF tools to run (with a command "
            "and whether this machine has what it needs), the catalog powers that apply, the guides to read and, for motion work, reference styles.",
            {"task": S, "max_tools": I, "max_powers": I}, ["task"]),
    _schema("kosif_tool", "Full card for one KOSIF tool: when to use it, every command with an example, inputs/outputs, requirements and "
            "their presence on this machine, safety and consent, tests and guides.", {"id": S}, ["id"]),
    _schema("kosif_list_tools", "List KOSIF tools, optionally for one area (" + ", ".join(hub.AREAS) + ").",
            {"area": {"type": "string", "enum": list(hub.AREAS)}}),
    _schema("kosif_doctor", "Which KOSIF tools can run on this machine right now, what each is missing, and the installs that unlock the most.",
            {"area": {"type": "string", "enum": list(hub.AREAS)}}),
    _schema("kosif_search_powers", "Keyword search over the ~4,750-record KOSIF capability catalog (techniques, recipes, methods), "
            "with evidence badges. Use kosif_find first for a whole task.", {"query": S, "limit": I}, ["query"]),
    _schema("kosif_power", "One catalog record by ID (e.g. TRANS-12, APPX-99): what, when, how, parameters, requirements, evidence.", {"id": S}, ["id"]),
    _schema("kosif_family", "Summary of one power family (e.g. typography-arabic) and its records' IDs and names.", {"family": S}, ["family"]),
    _schema("kosif_guides", "List or search the skill's reference guides.", {"query": S}),
    _schema("kosif_read_guide", "Read a guide or chapter inside the skill folder (SKILL.md, references/*.md, references/powers/*.md), "
            "optionally from a character offset.", {"path": S, "offset": {"type": "integer", "minimum": 0}}, ["path"]),
]


def _power_index():
    if not hasattr(_power_index, "rows"):
        _power_index.rows = P.load_powers()
    return _power_index.rows


def _registry():
    if not hasattr(_registry, "reg"):
        _registry.reg = hub.load_registry()
    return _registry.reg


def _safe_doc(path: str) -> Path:
    rel = str(path or "").replace("\\", "/").lstrip("/")
    target = (SKILL / rel).resolve()
    if SKILL.resolve() not in target.parents and target != SKILL.resolve():
        raise PermissionError("path must stay inside the skill folder")
    if target.suffix.lower() not in (".md", ".json") or not target.is_file():
        raise FileNotFoundError(f"no guide at {rel} (use kosif_guides to list them)")
    return target


def call(name: str, args: dict):
    args = args or {}
    if name == "kosif_find":
        return hub.find(str(args["task"]), int(args.get("max_tools", 5)), int(args.get("max_powers", 10)), _registry())
    if name == "kosif_tool":
        t = hub.tools_by_id(_registry()).get(str(args["id"]))
        if not t:
            raise KeyError(f"unknown tool id {args['id']!r}; use kosif_list_tools")
        return hub.tool_card(t, _registry())
    if name == "kosif_list_tools":
        return [hub.tool_card(t, _registry(), full=False) for t in _registry()["tools"] if not args.get("area") or t["area"] == args["area"]]
    if name == "kosif_doctor":
        rows = [t for t in _registry()["tools"] if not args.get("area") or t["area"] == args["area"]]
        res = [{"id": t["id"], "area": t["area"], **hub.readiness(t)} for t in rows]
        return {"ready": sum(r["state"] == "ready" for r in res), "tools": res}
    if name == "kosif_search_powers":
        terms = P.expand(str(args["query"]).split(), str(args["query"]))
        ranked = P.rank(_power_index(), terms, inject=False)[: int(args.get("limit", 15))]
        return [dict(P.short(p, s), when=p.get("when", ""), family=p.get("family")) for s, p in ranked]
    if name == "kosif_power":
        pid = str(args["id"]).upper()
        rec = next((p for p in _power_index() if str(p.get("id", "")).upper() == pid), None)
        if not rec:
            raise KeyError(f"unknown power id {args['id']!r}; use kosif_search_powers")
        return {k: rec.get(k) for k in P.SHOW_KEYS if k in rec}
    if name == "kosif_family":
        fam = str(args["family"])
        rows = [p for p in _power_index() if p.get("family") == fam or P.prefix_of(p) == fam.upper()]
        if not rows:
            raise KeyError(f"unknown family {fam!r}; families: " + ", ".join(sorted({p['family'] for p in _power_index()})))
        meta = next(f for f in hub.families_summary() if f["key"] == rows[0]["family"])
        return {**meta, "records": [{"id": p["id"], "status": p["status"], "name_ar": p["name_ar"], "name_en": p["name_en"]} for p in rows]}
    if name == "kosif_guides":
        docs = hub.doc_entries(_registry())
        if args.get("query"):
            docs = [d for _s, d in hub.rank_docs(docs, hub.terms_of(str(args["query"])), limit=15)]
        return [{k: d[k] for k in ("path", "title", "area", "lines")} for d in docs]
    if name == "kosif_read_guide":
        target = _safe_doc(args["path"])
        text = target.read_text(encoding="utf-8", errors="replace")
        off = int(args.get("offset", 0))
        chunk = text[off: off + MAX_DOC_CHARS]
        return {"path": target.relative_to(SKILL).as_posix(), "offset": off, "total_chars": len(text),
                "next_offset": off + len(chunk) if off + len(chunk) < len(text) else None, "text": chunk}
    raise KeyError(f"unknown tool {name}")


def handle(req: dict):
    method = req.get("method", "")
    params = req.get("params") or {}
    if method == "initialize":
        asked = params.get("protocolVersion")
        return {"protocolVersion": asked if asked in PROTOCOLS else PROTOCOLS[0],
                "serverInfo": {"name": "kosif-superpowers", "version": VERSION},
                "capabilities": {"tools": {"listChanged": False}, "resources": {"listChanged": False}},
                "instructions": "KOSIF Superpowers catalog. Call kosif_find with the user's task first, then kosif_tool or kosif_power "
                                "for detail. Evidence badges: claim the lowest true one. This server is read-only."}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        try:
            with redirect_stdout(io.StringIO()):  # library code must never write to the protocol stream
                out = call(params.get("name", ""), params.get("arguments") or {})
            return {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}], "isError": False}
        except Exception as exc:  # tool errors are results, not protocol errors
            return {"content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}], "isError": True}
    if method == "resources/list":
        return {"resources": [{"uri": u, "name": n, "description": d, "mimeType": "application/json" if n.endswith(".json") else "text/markdown"}
                              for u, (n, d) in RESOURCES.items()]}
    if method == "resources/read":
        uri = params.get("uri", "")
        if uri not in RESOURCES:
            raise KeyError(f"unknown resource {uri}")
        rel = RESOURCES[uri][0]
        return {"contents": [{"uri": uri, "mimeType": "application/json" if rel.endswith(".json") else "text/markdown",
                              "text": (SKILL / rel).read_text(encoding="utf-8")}]}
    if method in ("prompts/list",):
        return {"prompts": []}
    raise LookupError(f"method not found: {method}")


def respond(line: str):
    try:
        req = json.loads(line)
    except ValueError:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
    if not isinstance(req, dict) or "id" not in req:
        return None  # notification (e.g. notifications/initialized): no reply
    try:
        return {"jsonrpc": "2.0", "id": req["id"], "result": handle(req)}
    except LookupError as exc:
        return {"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32601, "message": str(exc)[:300]}}
    except Exception as exc:
        return {"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32602, "message": str(exc)[:300]}}


def serve(stdin=None, stdout=None) -> int:
    stdin = stdin or io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    stdout = stdout or sys.stdout
    for line in stdin:
        if not line.strip():
            continue
        if len(line) > 1_000_000:
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "request too large"}}
        else:
            out = respond(line)
        if out is not None:
            stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
            stdout.flush()
    return 0


def selftest() -> int:
    reg = _registry()
    first_tool = reg["tools"][0]["id"]
    script = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "selftest"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "kosif_find", "arguments": {"task": "اعمل فيديو موشن عربي متزامن مع صوتي"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "kosif_tool", "arguments": {"id": first_tool}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "kosif_list_tools", "arguments": {"area": "3d"}}},
        {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "kosif_doctor", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "kosif_search_powers", "arguments": {"query": "kinetic typography", "limit": 3}}},
        {"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "kosif_power", "arguments": {"id": "3D-01"}}},
        {"jsonrpc": "2.0", "id": 9, "method": "tools/call", "params": {"name": "kosif_family", "arguments": {"family": "typography-arabic"}}},
        {"jsonrpc": "2.0", "id": 10, "method": "tools/call", "params": {"name": "kosif_guides", "arguments": {"query": "3D"}}},
        {"jsonrpc": "2.0", "id": 11, "method": "tools/call", "params": {"name": "kosif_read_guide", "arguments": {"path": "references/INDEX.md"}}},
        {"jsonrpc": "2.0", "id": 12, "method": "tools/call", "params": {"name": "kosif_read_guide", "arguments": {"path": "../../../README.md"}}},
        {"jsonrpc": "2.0", "id": 13, "method": "resources/list"},
        {"jsonrpc": "2.0", "id": 14, "method": "nope"},
    ]
    out = io.StringIO()
    serve(io.StringIO("\n".join(json.dumps(r) for r in script) + "\n"), out)
    replies = {r["id"]: r for r in map(json.loads, out.getvalue().splitlines())}
    checks = {
        "initialize": replies[1]["result"]["serverInfo"]["name"] == "kosif-superpowers",
        "notification is silent": len(replies) == len([r for r in script if "id" in r]),
        "tools/list": len(replies[2]["result"]["tools"]) == len(TOOLS),
        **{f"tools/call #{i}": replies[i]["result"]["isError"] is False for i in range(3, 12)},
        "find returns tools": bool(json.loads(replies[3]["result"]["content"][0]["text"])["tools"]),
        "path escape refused": replies[12]["result"]["isError"] is True,
        "resources/list": len(replies[13]["result"]["resources"]) == len(RESOURCES),
        "unknown method → -32601": replies[14].get("error", {}).get("code") == -32601,
    }
    for k, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'}  {k}")
    bad = [k for k, ok in checks.items() if not ok]
    print(f"kosif_mcp selftest: {len(checks) - len(bad)}/{len(checks)} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__); sys.exit(0)
    sys.exit(serve())
