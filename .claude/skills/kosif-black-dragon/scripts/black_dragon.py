#!/usr/bin/env python3
"""Black Dragon: independent native synthesis and traceable source-linking.

This is a NEW implementation. It never imports or runs legacy Black Dragon
adapters. It reads the original catalog, extracts useful information and source
fingerprints, and composes task-specific capability blueprints. Indexing and
planning do not prove that a power was implemented or executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILLS = Path(".claude/skills")
SUPER = SKILLS / "kosif-superpowers"
SCHEMA = "kosif.black-dragon.native-fusion.v1"
PHASES = ("understand", "research", "design", "produce", "verify", "deliver")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(data: object) -> bytes:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def words(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[\w\u0600-\u06ff]+", text) if len(w) > 2}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_code(root: Path, base: Path, value: object) -> dict:
    if not isinstance(value, str) or not value:
        return {}
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        return {"declared_path": value, "inspection": "refused-unsafe-path"}
    target = base / rel
    resolved = target.resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        return {"declared_path": value, "inspection": "not-a-local-file"}
    if any(p.is_symlink() for p in (target, *target.parents) if p != root):
        return {"declared_path": value, "inspection": "refused-symlink"}
    return {"path": str(resolved.relative_to(root)), "sha256": digest(resolved.read_bytes()),
            "inspection": "bytes-fingerprinted-not-executed"}


def inventory(root: Path = ROOT) -> dict[str, dict]:
    """Read every source and preserve one source-linked record per catalog ID."""
    root = root.resolve()
    skill_root = root / SUPER
    skill_dir = root / SKILLS
    records: dict[str, dict] = {}
    source_hashes: dict[Path, str] = {}

    def link(kind: str, ident: str, path: Path, *, title: str = "", purpose: str = "",
             method: str = "", requirements=None, tags=None, family: str = "",
             code=None, details=None):
        key = kind + ":" + ident
        if key in records:
            raise ValueError("duplicate source ID: " + key)
        if not path.is_file():
            raise ValueError("missing source: " + str(path))
        if path not in source_hashes:
            source_hashes[path] = digest(path.read_bytes())
        text = " ".join(str(x) for x in (title, purpose, method, family, " ".join(map(str, tags or []))))
        source = str(path.relative_to(root))
        records[key] = {
            "id": key, "kind": kind, "source": source,
            "source_sha256": source_hashes[path],
            "extraction_sha256": digest(canonical(details if details is not None else {
                "title": title, "purpose": purpose, "method": method})),
            "title": title or ident, "purpose": purpose, "method": method,
            "requirements": requirements or [], "tags": tags or [],
            "faculty": family or kind,
            "keywords": sorted(words(text))[:200],
            "code": code or {},
            "coverage": {"source_linked": True, "automatically_extracted": True,
                         "native_implemented": False, "real_execution_verified": False}
        }

    # Skills: read the actual Markdown, not just the filenames. Exclude this
    # newly created skill itself to keep the input catalog non-self-referential.
    for path in sorted(skill_dir.rglob("SKILL.md")):
        if path.is_relative_to(skill_dir / "kosif-black-dragon"):
            continue
        content = path.read_text(encoding="utf-8")
        ident = str(path.parent.relative_to(skill_dir))
        description = next((x.split(":", 1)[1].strip().strip('"')
                            for x in content.splitlines()[:40] if x.startswith("description:")), "")
        headings = [x.strip("# ").strip() for x in content.splitlines() if x.startswith("# ")][:25]
        link("skill", ident, path, title=ident.rsplit("/", 1)[-1],
             purpose=description or " ".join(headings[:2]), method="; ".join(headings),
             family=ident.split("/")[0], details={"description": description, "headings": headings})

    power_dir = skill_root / "data/powers"
    if not power_dir.is_dir():
        raise ValueError("missing power catalog")
    for path in sorted(power_dir.glob("*.json")):
        obj = read_json(path)
        rows = obj if isinstance(obj, list) else obj.get("powers", [])
        if not isinstance(rows, list):
            raise ValueError("invalid power family: " + str(path))
        for row in rows:
            if not isinstance(row, dict) or not row.get("id"):
                raise ValueError("power missing ID in " + str(path))
            link("power", row["id"], path,
                 title=" | ".join(filter(None, (row.get("name_ar"), row.get("name_en")))),
                 purpose=str(row.get("what", "")), method=str(row.get("how", "")),
                 requirements=row.get("requires"), tags=row.get("tags"),
                 family=row.get("family", path.stem), details=row)

    tools_path = skill_root / "data/tools.json"
    tools = read_json(tools_path)["tools"]
    for row in tools:
        if not isinstance(row, dict) or not row.get("id"):
            raise ValueError("tool missing ID")
        code_base = skill_root if row.get("root") == "skill" else root
        code = _safe_code(root, code_base, row.get("path"))
        link("tool", row["id"], tools_path, title=row.get("title_ar") or row.get("title_en") or row["id"],
             purpose=row.get("summary_ar") or row.get("summary_en") or "",
             method="; ".join(str(c.get("example", "")) for c in row.get("commands", []) if isinstance(c, dict)),
             requirements=row.get("requires"), family=row.get("area", "tool"),
             code=code, details=row)

    sp_path = skill_root / "data/superpowers.json"
    for row in read_json(sp_path).get("items", []):
        if not isinstance(row, dict) or not row.get("id"):
            raise ValueError("superpower missing ID")
        link("superpower", row["id"], sp_path, title=row.get("name_ar") or row.get("name_en") or row["id"],
             purpose=str(row.get("best", "")), method=" ".join(str(x.get("id", "")) for x in row.get("pipeline", []) if isinstance(x, dict)),
             family=row.get("family", "superpower"), details=row)

    styles_path = root / "catalog/styles.json"
    if styles_path.is_file():
        for row in read_json(styles_path):
            if not isinstance(row, dict) or not row.get("id"):
                raise ValueError("style missing ID")
            link("style", row["id"], styles_path, title=row.get("name_ar") or row.get("name", ""),
                 purpose=str(row.get("source_prompt_words") or ""),
                 method=" ".join(map(str, row.get("tech") or [])),
                 tags=row.get("category") or [], family="visual-style", details=row)

    for path in sorted((root / "playbooks").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        link("playbook", path.stem, path, title=path.stem,
             purpose=text[:500], method="; ".join(line.strip("# ") for line in text.splitlines()
                                                   if line.startswith("# "))[:1500],
             family="production-playbook")

    protocol = skill_root / "PROTOCOL.md"
    protocol_dir = skill_root / "references/protocol"
    for path in ([protocol] if protocol.is_file() else []) + sorted(protocol_dir.glob("A*.md")):
        text = path.read_text(encoding="utf-8")
        link("protocol", path.stem, path, title=path.stem,
             purpose=text[:500], method="; ".join(line.strip("# ") for line in text.splitlines()
                                                   if line.startswith("# "))[:1500],
             family="operating-protocol")
    if not records:
        raise ValueError("empty inventory")
    return records


def build(root: Path, out: Path) -> dict:
    if out.is_symlink() or (out / "sources.jsonl").exists():
        raise ValueError("output path already initialized; choose a new folder")
    items = inventory(root)
    out.mkdir(parents=True, exist_ok=True)
    index = out / "sources.jsonl"
    with index.open("x", encoding="utf-8") as fh:
        for key in sorted(items):
            fh.write(json.dumps(items[key], ensure_ascii=False, sort_keys=True) + "\n")
    summary = {
        "schema": SCHEMA, "total_source_linked": len(items),
        "by_kind": dict(sorted(Counter(x["kind"] for x in items.values()).items())),
        "machine_extracted": len(items), "native_implemented": 0,
        "real_execution_verified": 0,
        "source_index_sha256": digest(index.read_bytes()),
        "truth": "Every source is linked and machine-extracted, NOT individually reviewed, native-implemented or executed."
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def load_index(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def compose(task: str, path: Path, *, legacy: bool = False, limit: int = 12) -> dict:
    query = words(task)
    if not query:
        raise ValueError("task cannot be empty")
    items = load_index(path)
    ranking = []
    for x in items:
        title = words(x["title"])
        purpose = words(x["purpose"])
        score = 7 * len(title & query) + 3 * len(purpose & query) + len(set(x["keywords"]) & query)
        if score:
            ranking.append((score, x["id"], x))
    ranking.sort(key=lambda t: (-t[0], t[1]))
    selected = [x for _, _, x in ranking[:limit]]
    return {
        "schema": SCHEMA + ".task", "task": task,
        "status": "native-thinking-blueprint-not-execution",
        "phases": list(PHASES),
        "source_count": len(items),
        "selected": [{"id": x["id"], "faculty": x["faculty"], "purpose": x["purpose"][:450],
                      "method": x["method"][:800], "requirements": x["requirements"],
                      "code": x["code"], "source_sha256": x["source_sha256"],
                      **({"legacy_entry": x["id"]} if legacy else {})}
                     for x in selected],
        "native_instruction": ("Synthesize a new coherent solution from the selected methods, "
                               "merge redundant steps, preserve unique constraints, then implement "
                               "and verify the required actual output. No legacy tool is executed."),
        "legacy_compatibility": "links-only-opt-in" if legacy else "disabled",
        "proof": "A ranked knowledge blueprint is not a software execution receipt."
    }


def verify(root: Path, folder: Path) -> dict:
    summary = read_json(folder / "summary.json")
    path = folder / "sources.jsonl"
    rows = load_index(path)
    unique = len({r["id"] for r in rows}) == len(rows)
    changed = []
    for row in rows:
        source = root / row["source"]
        if not source.is_file() or digest(source.read_bytes()) != row["source_sha256"]:
            changed.append(row["id"])
        code = row.get("code", {})
        if code.get("path") and (not (root / code["path"]).is_file()
                                 or digest((root / code["path"]).read_bytes()) != code["sha256"]):
            changed.append(row["id"] + ":code")
    ok = (unique and len(rows) == summary["total_source_linked"]
          and digest(path.read_bytes()) == summary["source_index_sha256"] and not changed)
    return {"integrity_passed": ok, "source_count": len(rows),
            "changed_or_missing": changed[:40], "changed_count": len(changed),
            "native_implemented": summary["native_implemented"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    cmd = ap.add_subparsers(dest="command", required=True)
    p = cmd.add_parser("index", help="Extract and link all source entries with checksums")
    p.add_argument("--out", type=Path, required=True)
    m = cmd.add_parser("compose", help="New native thinking blueprint; no legacy execution")
    m.add_argument("task")
    m.add_argument("--index", type=Path, required=True)
    m.add_argument("--legacy-links", action="store_true", help="only return optional legacy entry IDs")
    v = cmd.add_parser("verify", help="Verify the catalog-source fingerprints")
    v.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    try:
        if args.command == "index":
            result = build(args.root, args.out)
        elif args.command == "compose":
            result = compose(args.task, args.index, legacy=args.legacy_links)
        else:
            result = verify(args.root.resolve(), args.out)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 4 if args.command == "verify" and not result["integrity_passed"] else 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("black-dragon-native: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
