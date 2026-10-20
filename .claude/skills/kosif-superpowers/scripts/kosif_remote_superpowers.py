#!/usr/bin/env python3
"""KOSIF Superpowers Local Remote Commander (self-contained MCP stdio).

Local-only and permission-gated. No cloud listener, authentication bypass,
background persistence, screen control, or credential harvesting.
"""
import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = "0.2.0"
MAX_FILE = 512_000
SKIP = {".git", "node_modules", ".venv", "__pycache__", ".next"}


def workspace():
    p = Path(os.environ.get("KOSIF_REMOTE_ROOT", os.getcwd())).resolve()
    if not p.is_dir():
        raise ValueError("KOSIF_REMOTE_ROOT must be a directory")
    return p


def resolve(path=".", require=False):
    base = workspace()
    p = (base / str(path)).resolve()
    if os.path.normcase(os.path.commonpath([str(base), str(p)])) != os.path.normcase(str(base)):
        raise PermissionError("Access beyond approved workspace")
    if require and not p.exists():
        raise FileNotFoundError(path)
    return p


def relative(path):
    return path.relative_to(workspace()).as_posix() or "."


def consent(name):
    if os.environ.get(name) != "1":
        raise PermissionError(name + "=1 must be explicitly enabled")


def execute(name, args=None):
    a = args or {}
    if name == "health":
        return {"version": VERSION, "mode": "local-stdio", "workspace": str(workspace()),
                "allow_writes": os.environ.get("KOSIF_ALLOW_WRITES") == "1",
                "allow_exec": os.environ.get("KOSIF_ALLOW_EXEC") == "1"}
    if name == "system_info":
        return {"system": platform.system(), "arch": platform.machine(), "python": platform.python_version()}
    if name == "list_directory":
        p = resolve(a.get("path", "."), True)
        if not p.is_dir():
            raise NotADirectoryError(str(p))
        max_depth = max(1, min(int(a.get("depth", 1)), 2))
        found = []
        def walk(folder, depth):
            for item in sorted(folder.iterdir(), key=lambda f: f.name.lower()):
                if len(found) >= 150:
                    break
                if item.is_symlink() or item.name in SKIP:
                    continue
                found.append({"path": relative(item), "type": "dir" if item.is_dir() else "file"})
                if depth < max_depth and item.is_dir():
                    walk(item, depth + 1)
        walk(p, 1)
        return {"items": found, "truncated": len(found) >= 150}
    if name == "file_info":
        p = resolve(a["path"], True)
        return {"path": relative(p), "bytes": p.stat().st_size, "is_file": p.is_file(), "is_dir": p.is_dir()}
    if name == "read_file":
        p = resolve(a["path"], True)
        if not p.is_file() or p.stat().st_size > MAX_FILE:
            raise ValueError("Only text files under 512 KB")
        lines = p.read_text(encoding="utf-8").splitlines()
        offset = max(0, min(int(a.get("offset", 0)), len(lines)))
        length = max(1, min(int(a.get("length", 100)), 300))
        return {"path": relative(p), "total_lines": len(lines), "lines": lines[offset:offset+length]}
    if name == "search_text":
        p = resolve(a.get("path", "."), True)
        q = a.get("query", "")
        if not isinstance(q, str) or not 1 <= len(q) <= 200:
            raise ValueError("query length must be 1..200")
        hits, scanned = [], 0
        roots = [p] if p.is_file() else None
        def files():
            if roots is not None:
                yield from roots
            else:
                for base, dirs, names in os.walk(p):
                    dirs[:] = [d for d in dirs if d not in SKIP and not (Path(base)/d).is_symlink()]
                    for fn in names:
                        yield Path(base)/fn
        for f in files():
            if f.is_symlink() or f.suffix.lower() in {".exe", ".dll", ".zip", ".pdf", ".db", ".png", ".jpg"}:
                continue
            scanned += 1
            if scanned > 500:
                return {"hits": hits, "files_scanned": 500, "truncated": True}
            try:
                if f.stat().st_size > MAX_FILE:
                    continue
                with f.open(encoding="utf-8", errors="replace") as stream:
                    for n, line in enumerate(stream, 1):
                        if q.casefold() in line.casefold():
                            hits.append({"path": relative(f), "line": n, "preview": line.strip()[:240]})
                            if len(hits) >= 35:
                                return {"hits": hits, "files_scanned": scanned, "truncated": True}
            except (OSError, UnicodeError):
                continue
        return {"hits": hits, "files_scanned": scanned, "truncated": False}
    if name == "create_directory":
        consent("KOSIF_ALLOW_WRITES")
        p = resolve(a["path"])
        p.mkdir(parents=True, exist_ok=True)
        return {"created": relative(p)}
    if name == "write_file":
        consent("KOSIF_ALLOW_WRITES")
        p = resolve(a["path"])
        data = a["content"]
        if not isinstance(data, str) or len(data.encode("utf-8")) > MAX_FILE:
            raise ValueError("Text must be at most 512 KB")
        if not p.parent.is_dir():
            raise FileNotFoundError("Parent directory missing")
        temp = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=p.parent, delete=False) as handle:
                temp = Path(handle.name)
                handle.write(data)
            os.replace(str(temp), str(p))
        finally:
            if temp is not None:
                temp.unlink(missing_ok=True)
        return {"written": relative(p), "characters": len(data)}
    if name == "replace_block":
        consent("KOSIF_ALLOW_WRITES")
        p = resolve(a["path"], True)
        old, new = a["old_string"], a["new_string"]
        if not old:
            raise ValueError("old_string is empty")
        body = p.read_text(encoding="utf-8")
        expected = int(a.get("expected_replacements", 1))
        if body.count(old) != expected:
            raise ValueError("Unexpected replacement count")
        return execute("write_file", {"path": relative(p), "content": body.replace(old, new)})
    if name == "move_file":
        consent("KOSIF_ALLOW_WRITES")
        src, dst = resolve(a["source"], True), resolve(a["destination"])
        if dst.exists() or not dst.parent.is_dir():
            raise ValueError("Target exists or destination parent missing")
        src.rename(dst)
        return {"from": relative(src), "to": relative(dst)}
    if name == "run_command":
        consent("KOSIF_ALLOW_EXEC")
        argv = a.get("argv")
        approved = {("git", "status"), ("git", "diff"), ("git", "rev-parse"),
                    ("python", "--version"), ("node", "--version"), ("npm", "--version")}
        if not isinstance(argv, list) or len(argv) < 2 or not all(isinstance(x, str) for x in argv):
            raise PermissionError("Command must be an argument array")
        if tuple(argv[:2]) not in approved:
            raise PermissionError("Command not allowlisted")
        if argv[0] != "git" and len(argv) != 2:
            raise PermissionError("Version checks take no extra arguments")
        if argv[0] == "git" and (len(argv) > 3 or (len(argv) == 3 and argv[2] not in {"--short", "--stat", "--show-toplevel", "--branch"})):
            raise PermissionError("Only read-only git arguments")
        p = resolve(a.get("cwd", "."), True)
        if not p.is_dir():
            raise NotADirectoryError(str(p))
        r = subprocess.run(argv, cwd=p, shell=False, capture_output=True, text=True, errors="replace", timeout=10)
        return {"returncode": r.returncode, "stdout": r.stdout[:6000], "stderr": r.stderr[:1500]}
    raise KeyError("Unknown tool: " + name)


def schema(name, description, props=None, required=None):
    return {"name": name, "description": description, "inputSchema": {"type": "object", "properties": props or {}, "required": required or [], "additionalProperties": False}}


P = {"path": {"type": "string"}}
TOOLS = [
    schema("health", "Inspect local execution permissions"),
    schema("system_info", "Read system platform"),
    schema("list_directory", "List bounded workspace entries", {**P, "depth": {"type": "integer"}}),
    schema("file_info", "Inspect workspace entry", P, ["path"]),
    schema("read_file", "Read bounded UTF-8 file", {**P, "offset": {"type": "integer"}, "length": {"type": "integer"}}, ["path"]),
    schema("search_text", "Search text within workspace", {**P, "query": {"type": "string"}}, ["query"]),
    schema("create_directory", "Create a directory if write permission enabled", P, ["path"]),
    schema("write_file", "Write UTF-8 text if write permission enabled", {**P, "content": {"type": "string"}}, ["path", "content"]),
    schema("replace_block", "Perform an exact replacement if allowed", {**P, "old_string": {"type": "string"}, "new_string": {"type": "string"}, "expected_replacements": {"type": "integer"}}, ["path", "old_string", "new_string"]),
    schema("move_file", "Move one workspace item if write permission enabled", {"source": {"type": "string"}, "destination": {"type": "string"}}, ["source", "destination"]),
    schema("run_command", "Run only a short read-only command allowlist", {"argv": {"type": "array", "items": {"type": "string"}}, "cwd": {"type": "string"}}, ["argv"]),
]


def serve():
    for line in sys.stdin:
        req = None
        try:
            if len(line) > 2_000_000:
                raise ValueError("Request exceeded 2MB")
            req = json.loads(line)
            if "id" not in req:
                continue
            method = req.get("method", "")
            if method == "initialize":
                result = {"protocolVersion": req.get("params", {}).get("protocolVersion", "2024-11-05"),
                          "serverInfo": {"name": "kosif-remote-superpowers", "version": VERSION}, "capabilities": {"tools": {}}}
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                args = req.get("params", {})
                try:
                    output = execute(args["name"], args.get("arguments", {}))
                    result = {"content": [{"type": "text", "text": json.dumps(output, ensure_ascii=False)}]}
                except Exception as exc:
                    result = {"content": [{"type": "text", "text": type(exc).__name__ + ": " + str(exc)}], "isError": True}
            else:
                raise KeyError("Unsupported MCP method")
            response = {"jsonrpc": "2.0", "id": req["id"], "result": result}
        except Exception as exc:
            response = {"jsonrpc": "2.0", "id": req.get("id") if isinstance(req, dict) else None,
                        "error": {"code": -32602, "message": str(exc)[:300]}}
        print(json.dumps(response, ensure_ascii=False), flush=True)


def demo():
    with tempfile.TemporaryDirectory() as d:
        old = {k: os.environ.get(k) for k in ("KOSIF_REMOTE_ROOT", "KOSIF_ALLOW_WRITES", "KOSIF_ALLOW_EXEC")}
        try:
            os.environ.update({"KOSIF_REMOTE_ROOT": d, "KOSIF_ALLOW_WRITES": "0", "KOSIF_ALLOW_EXEC": "0"})
            denied = False
            try:
                execute("write_file", {"path": "sample.txt", "content": "hello"})
            except PermissionError:
                denied = True
            os.environ["KOSIF_ALLOW_WRITES"] = "1"
            execute("write_file", {"path": "sample.txt", "content": "KOSIF local MCP demo\n"})
            found = execute("search_text", {"query": "KOSIF"})["hits"]
            read = execute("read_file", {"path": "sample.txt"})
            print(json.dumps({"status": "PASS" if denied and found and read["lines"] else "FAIL",
                              "tools": len(TOOLS), "default_write_denied": denied,
                              "search_hits": len(found), "read_lines": read["lines"], "workspace": "temporary"}, ensure_ascii=False))
            return 0 if denied and found and read["lines"] else 1
        finally:
            for key, val in old.items():
                if val is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = val


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("doctor", "demo", "serve"), nargs="?", default="doctor")
    mode = parser.parse_args().mode
    if mode == "doctor":
        print(json.dumps({"name": "kosif-remote-superpowers", "version": VERSION, "tools": len(TOOLS),
                          "transport": "stdio", "permissions": execute("health")}, ensure_ascii=False))
        return 0
    if mode == "demo":
        return demo()
    serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
