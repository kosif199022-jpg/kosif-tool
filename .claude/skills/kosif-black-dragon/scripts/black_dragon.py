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
import importlib.util
import json
import re
import sys
import unicodedata
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
    """Conservative, deterministic Arabic/English lookup tokens.

    Normalize Arabic hamza forms, diacritics, tatweel and leading definite
    articles while retaining the original token to avoid over-stemming.
    This improves matching between e.g. "الإيقاع" and "والإيقاع".
    """
    value = unicodedata.normalize("NFKC", str(text)).casefold()
    value = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", value)
    value = value.translate(str.maketrans({
        "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي",
        "ؤ": "و", "ئ": "ي",
    }))
    result = set()
    for token in re.findall(r"[a-z0-9_]+|[\u0621-\u064a]+", value):
        if len(token) <= 2:
            continue
        result.add(token)
        if re.fullmatch(r"[\u0621-\u064a]+", token):
            stem = token
            if stem.startswith("وال") and len(stem) > 6:
                stem = stem[1:]
            if stem.startswith("ال") and len(stem) > 5:
                stem = stem[2:]
            elif stem.startswith("لل") and len(stem) > 5:
                stem = stem[2:]
            if len(stem) > 2:
                result.add(stem)
    return result


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
             purpose=description or " ".join(headings[:2]), method=content,
             family=ident.split("/")[0], details={"description": description, "headings": headings,
                                                      "full_text_sha256": digest(content.encode("utf-8"))})

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
             purpose=text[:500], method=text, family="production-playbook")

    protocol = skill_root / "PROTOCOL.md"
    protocol_dir = skill_root / "references/protocol"
    for path in ([protocol] if protocol.is_file() else []) + sorted(protocol_dir.glob("A*.md")):
        text = path.read_text(encoding="utf-8")
        link("protocol", path.stem, path, title=path.stem,
             purpose=text[:500], method=text, family="operating-protocol")
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
    # Group extracted methods across the FULL catalog, not just selected task matches.
    # Knowledge fusion is independent of and distinct from executable capability fusion.
    atlas = native_reasoner().fuse("Unify all source methods",
                                   [items[key] for key in sorted(items)], len(items))
    if not atlas["provenance_preserved"] or atlas["selected_source_count"] != len(items):
        raise ValueError("catalog-wide fusion lost source lineage")
    atlas_file = out / "fusion_atlas.json"
    atlas_file.write_text(json.dumps(atlas, ensure_ascii=False, sort_keys=True) + "\n",
                          encoding="utf-8")
    summary = {
        "schema": SCHEMA, "total_source_linked": len(items),
        "knowledge_fusion": "catalog-wide-native-reasoning-not-tool-execution",
        "fused_source_count": atlas["selected_source_count"],
        "fused_faculty_count": len(atlas["faculties"]),
        "fused_method_fragments": atlas["method_fusion"]["distinct_fragments"],
        "fusion_atlas_sha256": digest(atlas_file.read_bytes()),
        "by_kind": dict(sorted(Counter(x["kind"] for x in items.values()).items())),
        "machine_extracted": len(items), "native_implemented": 0,
        "real_execution_verified": 0,
        "native_thinking_implemented": True,
        "native_thinking_faculties": 26,
        "source_index_sha256": digest(index.read_bytes()),
        "truth": "All extracted source methods are grouped in a native knowledge atlas; not proof of human review, executable reimplementation or real task execution."
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def load_index(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _safe_source(root: Path, value: object) -> Path | None:
    """Never follow manifest paths outside the selected root or via symlinks."""
    if not isinstance(value, str) or not value:
        return None
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        return None
    root = root.resolve()
    candidate = root / rel
    if not candidate.resolve().is_relative_to(root):
        return None
    if any(part.is_symlink() for part in (candidate, *candidate.parents) if part != root):
        return None
    return candidate if candidate.is_file() else None


def verified_catalog_atlas(index: Path, rows: list[dict]) -> dict | None:
    """Refuse to present stale or altered atlas data as verified knowledge.

    Checksums are local integrity checks, not signatures or evidence of
    executable features; independent execution remains unproven.
    """
    atlas_path = index.with_name("fusion_atlas.json")
    if not atlas_path.is_file():
        return None
    summary_path = index.with_name("summary.json")
    if not summary_path.is_file():
        raise ValueError("fusion atlas has no summary; regenerate the index")
    summary = read_json(summary_path)
    atlas = read_json(atlas_path)
    ids = [row["id"] for row in rows]
    lineage = [row["source_id"] for row in atlas.get("affiliation", [])]
    if not (
        digest(index.read_bytes()) == summary.get("source_index_sha256")
        and digest(atlas_path.read_bytes()) == summary.get("fusion_atlas_sha256")
        and len(ids) == summary.get("total_source_linked")
        and len(ids) == len(set(ids))
        and atlas.get("provenance_preserved") is True
        and atlas.get("selected_source_count") == len(ids)
        and len(lineage) == len(ids)
        and set(lineage) == set(ids)
    ):
        raise ValueError("source index or fusion atlas integrity mismatch; regenerate the index")
    return {
        "status": "knowledge-reconciled-not-all-capabilities-implemented",
        "source_count": atlas["selected_source_count"],
        "faculty_count": len(atlas["faculties"]),
        "distinct_method_fragments": atlas["method_fusion"]["distinct_fragments"],
        "atlas_path": str(atlas_path),
        "integrity": "local-digests-and-source-membership-checked-not-signed",
    }


def native_reasoner():
    """Load only the NEW local reasoning module, never the legacy Dragon Mind."""
    path = Path(__file__).with_name("native_mind.py")
    spec = importlib.util.spec_from_file_location("_kosif_black_dragon_native_reasoner", path)
    if spec is None or spec.loader is None:
        raise ValueError("independent native reasoning module unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compose(task: str, path: Path, *, legacy: bool = False, limit: int = 12) -> dict:
    query = words(task)
    if not query:
        raise ValueError("task cannot be empty")
    if not 1 <= limit <= 50:
        raise ValueError("selection limit must be between 1 and 50")
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
    # Internalized Dragon Mind's ideas: 26 faculties, cognitive cycle, native
    # method reconciliation and typed inputs. No old runtime is invoked.
    synthesis = native_reasoner().fuse(task, selected, len(items))
    return {
        "schema": SCHEMA + ".task", "task": task,
        "status": "native-thinking-blueprint-not-execution",
        "phases": list(PHASES),
        "source_count": len(items),
        "native_mind": synthesis,
        "catalog_wide_fusion": verified_catalog_atlas(path, items),
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
        source = _safe_source(root, row.get("source"))
        if source is None or digest(source.read_bytes()) != row.get("source_sha256"):
            changed.append(row["id"])
        code = row.get("code", {})
        if code.get("path"):
            code_file = _safe_source(root, code.get("path"))
            if code_file is None or digest(code_file.read_bytes()) != code.get("sha256"):
                changed.append(row["id"] + ":code")
    atlas_path = folder / "fusion_atlas.json"
    atlas_valid = False
    if atlas_path.is_file():
        atlas = read_json(atlas_path)
        affiliation = [x["source_id"] for x in atlas["affiliation"]]
        atlas_valid = (
            digest(atlas_path.read_bytes()) == summary.get("fusion_atlas_sha256")
            and atlas.get("provenance_preserved") is True
            and atlas.get("selected_source_count") == len(rows)
            and len(affiliation) == len(rows)
            and set(affiliation) == {row["id"] for row in rows})
    ok = (unique and len(rows) == summary["total_source_linked"]
          and digest(path.read_bytes()) == summary["source_index_sha256"]
          and atlas_valid and not changed)
    return {"integrity_passed": ok, "fusion_atlas_integrity_passed": atlas_valid,
            "source_count": len(rows),
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
