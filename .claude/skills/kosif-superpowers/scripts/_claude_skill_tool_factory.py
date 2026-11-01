#!/usr/bin/env python3
"""Static Skill-to-Tool Factory for Claude: inspect, draft, verify, never auto-execute.

Python stdlib only. SKILL.md is untrusted documentation. Code in a skill is
NEVER imported, run, installed, promoted or granted network access here.
Generated proposals are not runnable Black Dragon adapter registries.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
import zipfile
from pathlib import Path

import black_dragon as dragon

REPO = dragon.REPO
SKILLS = dragon.audit.SKILL.parent
SCHEMA = "kosif.skill-tool-factory.v1"
MAX_FILES = 6000
MAX_SCRIPTS = 600
MAX_PARSE_BYTES = 512_000
MAX_ZIP_MEMBERS = 6000
MAX_ZIP_UNCOMPRESSED = 512 * 1024 * 1024
IGNORE = {".git", ".venv", "node_modules", "__pycache__", ".next", "out"}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
RISK_IMPORTS = {"subprocess", "socket", "requests", "httpx", "urllib", "ftplib",
                "paramiko", "shutil", "ctypes", "boto3", "openai", "anthropic"}


def _skill_dir(name: str) -> Path:
    if not isinstance(name, str) or not NAME.fullmatch(name):
        raise ValueError("Invalid skill name")
    root = SKILLS / name
    if root.is_symlink() or not root.is_dir() or root.resolve().parent != SKILLS.resolve():
        raise ValueError("Skill directory is not a direct, non-symlink child")
    md = root / "SKILL.md"
    if md.is_symlink() or not md.is_file():
        raise ValueError("Skill needs a regular SKILL.md")
    return root


def _frontmatter(markdown: str) -> dict:
    if not markdown.startswith("---\n"):
        return {}
    end = markdown.find("\n---", 4)
    if end < 0:
        return {}
    result = {}
    for line in markdown[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() in {"name", "description", "license", "version"}:
            result[key.strip()] = value.strip().strip("\"'")
    return result


def _declared_links(markdown: str, root: Path) -> tuple[list[str], list[str]]:
    missing, outside = [], []
    for match in LINK.finditer(markdown):
        link = match.group(1).strip().split(" ", 1)[0].strip("<>").split("#", 1)[0]
        if not link or ":" in link or link.startswith(("/", "#", "{")):
            continue
        candidate = (root / link).resolve()
        if not candidate.is_relative_to(root.resolve()):
            outside.append(link)
        elif not candidate.is_file() and not candidate.is_dir():
            missing.append(link)
    return sorted(set(missing))[:80], sorted(set(outside))[:80]


def _script(path: Path, root: Path) -> dict:
    rel = path.relative_to(root).as_posix()
    result = {"script": rel, "bytes": path.stat().st_size,
              "sha256": dragon.audit.sha256(path), "executable": False,
              "needs_review": True}
    if path.stat().st_size > MAX_PARSE_BYTES:
        result["reason"] = "Too large for bounded AST scan"
        return result
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=rel)
    except (OSError, UnicodeError, SyntaxError) as exc:
        result["reason"] = "Cannot parse Python source: " + str(exc)[:120]
        return result
    imports = set()
    guard = False
    parser_api = False
    frameworks = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
            if (isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__"
                    and any(isinstance(c, ast.Constant) and c.value == "__main__"
                            for c in node.test.comparators)):
                guard = True
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr in (
                    "ArgumentParser", "add_argument", "add_subparsers", "parse_args", "parse_known_args"):
                parser_api = True
    frameworks = imports & {"argparse", "click", "typer", "fire"}
    cli_candidate = bool(guard and (parser_api or frameworks & {"click", "typer", "fire"}))
    result.update({
        "cli_candidate": cli_candidate,
        "main_guard": guard,
        "frameworks": sorted(frameworks),
        "review_flags": sorted(imports & RISK_IMPORTS),
        "command_example": "python3 " + path.relative_to(REPO).as_posix() + " --help",
        "reason": ("CLI entrypoint candidate; CLI arguments, dependencies and side effects require review"
                   if cli_candidate else "No verified command-line entrypoint detected"),
    })
    return result


def inspect(name: str, script_limit: int = 100) -> dict:
    if type(script_limit) is not int or not 1 <= script_limit <= MAX_SCRIPTS:
        raise ValueError("script_limit must be an integer from 1 to 600")
    root = _skill_dir(name)
    md = (root / "SKILL.md").read_text(encoding="utf-8")
    front = _frontmatter(md)
    missing, outside = _declared_links(md, root)
    warnings = []
    scripts = []
    file_count = 0
    truncated = False
    # os.walk(..., followlinks=False) never descends into symlinks.
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORE and not (Path(base) / d).is_symlink())
        for filename in sorted(files):
            path = Path(base) / filename
            if path.is_symlink():
                warnings.append("Symlinked file ignored: " + str(path.relative_to(root)))
                continue
            file_count += 1
            if file_count > MAX_FILES:
                truncated = True
                break
            if path.suffix.lower() == ".py":
                if len(scripts) >= script_limit:
                    truncated = True
                    continue
                scripts.append(_script(path, root))
        if file_count > MAX_FILES:
            break
    candidates = [r for r in scripts if r.get("cli_candidate")]
    # A compiled proposal does not claim to be a verified executable adapter.
    return {
        "schema": SCHEMA + ".inspection",
        "skill": name, "metadata": front,
        "skill_md_sha256": dragon.audit.sha256(root / "SKILL.md"),
        "source": (root / "SKILL.md").relative_to(REPO).as_posix(),
        "files_scanned": min(file_count, MAX_FILES), "scripts_inspected": len(scripts),
        "cli_candidates": candidates, "candidate_count": len(candidates),
        "missing_local_links": missing, "links_outside_skill": outside,
        "warnings": warnings[:40], "truncated": truncated,
        "tool_ready": False,
        "status": "static-inspection-only",
        "next_step": "Review candidates, supply exact argument/output contract, test in isolated workspace, then separately register an approved adapter",
    }


def draft(name: str, out: Path, script_limit: int = 100) -> dict:
    """Save a non-executable proposal. Never register or execute discovered code."""
    data = inspect(name, script_limit)
    target = out.resolve()
    allowed = (REPO / "out" / "skill-tool-proposals").resolve()
    if not target.is_relative_to(allowed) or target.suffix != ".json" or out.is_symlink():
        raise ValueError("Proposal path must be a JSON file under out/skill-tool-proposals/")
    if target.exists():
        raise FileExistsError("Cannot overwrite an existing proposal")
    proposal = {
        "schema": SCHEMA + ".proposal", "skill": name, "source_sha256": data["skill_md_sha256"],
        "status": "PENDING_HUMAN_REVIEW_NOT_EXECUTABLE", "register_automatically": False,
        "candidate_count": data["candidate_count"],
        "draft_adapters": [
            {"path": row["script"], "source_sha256": row["sha256"],
             "command_example": row["command_example"],
             "args": None, "artifact_contract": None, "permissions_review": "required",
             "tests_required": ["exit-code", "artifact-sha256", "side-effects", "dependencies", "permissions"]}
            for row in data["cli_candidates"]
        ],
        "missing_links": data["missing_local_links"],
        "warnings": data["warnings"],
        "truth": "This file is a proposal, NOT a Black Dragon adapter registry; no scripts were executed.",
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"proposal": str(target), "candidate_count": proposal["candidate_count"],
            "sha256": dragon.audit.sha256(target), "executable": False}


def verify_zip(path: Path) -> dict:
    """Bounded no-extraction audit of a portable skill ZIP exported under out/."""
    raw = Path(path)
    resolved = raw.resolve()
    allowed = (REPO / "out").resolve()
    if raw.is_symlink() or not resolved.is_relative_to(allowed) or not resolved.is_file():
        raise ValueError("ZIP must be a regular file under repository out/")
    if resolved.suffix.lower() != ".zip":
        raise ValueError("Expected .zip package")
    errors = []
    with zipfile.ZipFile(resolved) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_ZIP_MEMBERS:
            raise ValueError("Too many ZIP members")
        names = [i.filename for i in infos]
        if len(names) != len(set(names)):
            errors.append("Duplicate ZIP members")
        if "SKILL.md" not in names or "KOSIF_EXPORT_MANIFEST.json" not in names:
            errors.append("Missing root SKILL.md or KOSIF_EXPORT_MANIFEST.json")
        total = 0
        for item in infos:
            p = Path(item.filename)
            if (p.is_absolute() or ".." in p.parts or "\\" in item.filename or
                    stat.S_ISLNK(item.external_attr >> 16)):
                errors.append("Unsafe archive member: " + item.filename[:100])
            total += item.file_size
            if total > MAX_ZIP_UNCOMPRESSED:
                raise ValueError("Uncompressed ZIP exceeds limit")
        manifest = None
        if not errors:
            manifest = json.loads(archive.read("KOSIF_EXPORT_MANIFEST.json"))
            hashes = manifest.get("files", {})
            if not isinstance(hashes, dict) or set(hashes) != set(names) - {"KOSIF_EXPORT_MANIFEST.json"}:
                errors.append("Manifest entries differ from archive members")
            else:
                for name, expected in hashes.items():
                    with archive.open(name) as stream:
                        h = hashlib.sha256()
                        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                            h.update(chunk)
                    if h.hexdigest() != expected:
                        errors.append("SHA-256 mismatch for " + name[:100])
        return {"schema": SCHEMA + ".zip-verification", "zip": str(resolved),
                "files": len(infos), "uncompressed_bytes": total,
                "verified": not errors, "errors": errors[:50],
                "zip_sha256": dragon.audit.sha256(resolved),
                "note": "Archive content integrity checked without extracting or executing scripts; no runtime or license certification"}


def doctor() -> dict:
    catalog = dragon.full_inventory()
    adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
    unknown = sorted(set(adapters) - set(catalog))
    issues = ["Unknown reviewed adapter: " + k for k in unknown]
    checked = 0
    for key, spec in adapters.items():
        if key in unknown:
            continue
        try:
            dragon._safe_script(spec["script"])
            if not any("{artifact}" in arg for arg in spec.get("args", [])):
                issues.append(key + ": missing artifact output contract")
            for dep in spec.get("depends_on", []):
                if dep not in adapters:
                    issues.append(key + ": prerequisite has no reviewed adapter: " + str(dep))
            checked += 1
        except (OSError, ValueError, TypeError) as exc:
            issues.append(key + ": " + str(exc)[:100])
    return {"schema": SCHEMA + ".doctor",
            "catalog_entries": len(catalog), "reviewed_adapters": len(adapters),
            "adapter_scripts_checked": checked, "passed": not issues,
            "issues": issues[:50], "execution_enabled_in_environment":
                os.environ.get("KOSIF_ALLOW_ADAPTER_EXECUTION") == "1",
            "executions_performed": 0, "network_calls": 0,
            "truth": "Static configuration diagnostics, not host sandbox or runtime verification"}
