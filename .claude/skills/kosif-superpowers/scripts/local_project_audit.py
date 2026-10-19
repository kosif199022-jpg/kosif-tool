#!/usr/bin/env python3
"""Read-only triage of a local project, directory or repository.

Collect provenance, file-role evidence, static source indicators and safe next
steps. Never execute inspected content or traverse symlinks, and never claim
runtime behavior from static signatures.
"""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import zipfile

CODE = {".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss",
        ".json", ".md", ".xml", ".yaml", ".yml", ".toml", ".c", ".cpp",
        ".h", ".hpp", ".rs", ".go", ".cs", ".java", ".kt", ".shader",
        ".glsl", ".svg", ".sql", ".vue", ".svelte"}
BIN = {".exe", ".dll", ".so", ".dylib", ".class", ".wasm"}
IMAGE = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tiff", ".ico"}
VIDEO = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".blend", ".glb", ".gltf"}
ARCHIVE = {".zip", ".7z", ".rar", ".tar", ".gz"}
PATTERNS = {"dynamic_code": re.compile(r"\b(?:eval\s*\(|new\s+Function\s*\()", re.I),
            "dom_html": re.compile(r"\.innerHTML\s*=|document\.write\s*\(", re.I),
            "network": re.compile(r"\bfetch\s*\(|https?://", re.I),
            "events": re.compile(r"addEventListener\s*\(|@click|onClick=", re.I),
            "animation": re.compile(r"@keyframes|requestAnimationFrame|\bbpy\.|keyframe_insert", re.I),
            "design": re.compile(r"grid-template|@media|--[a-z][a-z_-]+\s*:|\btransform\s*:", re.I)}
MAX_SAMPLE = 131072
HASH_LIMIT = 4 * 1024 * 1024

def scan(root, limit=100000):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be a directory")
    stats, indicators = collections.Counter(), collections.Counter()
    extensions, routes = collections.Counter(), collections.Counter()
    samples, skipped = [], []
    total_bytes = 0
    count = 0
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(base)/d).is_symlink()
                         and d not in {".git", "node_modules", ".venv", "__pycache__"})
        for name in sorted(files):
            file = Path(base)/name
            rel = file.relative_to(root).as_posix()
            if file.is_symlink():
                skipped.append({"path": rel, "reason": "symlink"})
                continue
            count += 1
            if count > limit:
                skipped.append({"reason": "file_limit", "limit": limit})
                break
            try:
                stat = file.stat()
                ext = file.suffix.lower()
                total_bytes += stat.st_size
                extensions[ext or "[none]"] += 1
                if ext in BIN:
                    route = "ghidra_rea_candidate"
                elif ext in CODE:
                    route = "source_review"
                elif ext in ARCHIVE:
                    route = "archive_metadata_only"
                elif ext in IMAGE:
                    route = "image_asset"
                elif ext in VIDEO:
                    route = "media_or_project"
                else:
                    route = "other"
                routes[route] += 1
                record = {"path": rel, "bytes": stat.st_size, "route": route}
                if stat.st_size <= HASH_LIMIT:
                    record["sha256"] = hashlib.sha256(file.read_bytes()).hexdigest()
                if ext in CODE and stat.st_size <= 2*1024*1024:
                    data = file.read_bytes()[:MAX_SAMPLE]
                    text = data.decode("utf-8-sig", errors="replace")
                    for label, pat in PATTERNS.items():
                        if pat.search(text):
                            indicators[label] += 1
                            record.setdefault("indicators", []).append(label)
                if ext == ".zip":
                    try:
                        with zipfile.ZipFile(file) as z:
                            info = z.infolist()
                            names = [i.filename for i in info]
                            unsafe = [x for x in names if x.startswith("/") or ".." in Path(x).parts or "\\" in x]
                            uncompressed = sum(x.file_size for x in info)
                            record["zip"] = {"entries": len(info), "uncompressed_bytes": uncompressed,
                                             "unsafe_path_count": len(unsafe),
                                             "ratio": round(uncompressed / max(stat.st_size,1), 2)}
                    except (zipfile.BadZipFile, OSError) as err:
                        record["zip_error"] = type(err).__name__
                if len(samples) < 80 or route == "ghidra_rea_candidate":
                    samples.append(record)
            except (OSError, PermissionError) as err:
                stats["unreadable"] += 1
                if len(skipped) < 25:
                    skipped.append({"path": rel, "reason": type(err).__name__})
        if count > limit:
            break
    return {"schema": "kosif.local-project-audit.v1", "root": str(root),
            "files": min(count, limit), "bytes": total_bytes,
            "extensions": dict(extensions.most_common()),
            "routes": dict(routes), "indicators_files": dict(indicators),
            "unreadable": stats["unreadable"],
            "samples": samples[:120], "skipped": skipped[:30],
            "scope": "static file-level triage; no execution, no extracted code or proved application behavior",
            "archive_entries_are_not_executed": True}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("root")
    p.add_argument("--output", help="optional report path, outside input")
    p.add_argument("--limit", type=int, default=100000)
    args = p.parse_args()
    if not 1 <= args.limit <= 1000000:
        p.error("invalid file limit")
    result = scan(args.root, args.limit)
    raw = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        dest = Path(args.output).resolve()
        if dest == Path(args.root).resolve() or Path(args.root).resolve() in dest.parents:
            p.error("refusing to write inside audited input folder")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(raw, encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in {"samples", "skipped"}},
                     ensure_ascii=False))
if __name__ == "__main__":
    main()
