#!/usr/bin/env python3
"""Audit capability -> installed SKILL.md ownership and specialist routing.

An explicit, verifiable owner relationship is NOT proof a specialist skill can
execute the power. Candidate specialist routes are lexical hints only.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

import _black_dragon_brain as brain

SCHEMA = "kosif.black-dragon.skill-capability-links.v1"
PRIMARY = "skill:kosif-superpowers"
SKIP = {"kosif", "superpowers", "skill", "skills", "power", "powers", "tool",
        "tools", "general", "system", "agent", "agents", "full", "pro",
        "plugin", "suite", "core", "with", "the", "for", "and", "from"}


def _source(meta: dict, skill_root: Path, repo_root: Path) -> Path:
    if not isinstance(meta, dict):
        raise ValueError("Malformed capability entry")
    src = meta.get("source")
    if not isinstance(src, str) or not src:
        raise ValueError("Capability is missing source metadata")
    rel = Path(src)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Unsafe catalog source path: " + src)
    kind = meta.get("kind")
    base = (skill_root.parent if kind == "skill" else
            repo_root if kind in ("style", "playbook") else skill_root).resolve()
    raw = base / rel
    resolved = raw.resolve()
    if not resolved.is_relative_to(base):
        raise ValueError("Capability source escapes the expected repository root: " + src)
    if any(p.is_symlink() for p in [raw, *raw.parents] if p != base and p != base.parent):
        raise ValueError("Catalog source crosses a symlink: " + src)
    return resolved


def _terms(value: str) -> set[str]:
    return {term for term in re.findall(r"[\w؀-ۿ]{4,}", value.lower())
            if term not in SKIP and not term.isnumeric()}


def build(inventory: dict, skill_root: Path, repo_root: Path,
          descriptions: dict[str, str] | None = None) -> dict:
    """Create a full identity-safe ownership map; NO execution, NO network access.

    Every catalog entry is attached to the genuine kosif-superpowers SKILL.md.
    Installed skills also attach to their own existing SKILL.md. Specialist
    candidates are *hints* based on 2+ overlapping slug tokens, not confirmed
    compatibility, and never overwrite canonical ownership.
    """
    skill_root = skill_root.resolve()
    repo_root = repo_root.resolve()
    if PRIMARY not in inventory or inventory[PRIMARY].get("kind") != "skill":
        raise ValueError("Missing canonical installed kosif-superpowers skill")
    skills = sorted(k for k, v in inventory.items() if v.get("kind") == "skill")
    if not skills:
        raise ValueError("No SKILL.md entries available to link")
    # Explicit existence check, including the central orchestrator.
    sources = {}
    missing = []
    for key, meta in sorted(inventory.items()):
        try:
            file = _source(meta, skill_root, repo_root)
            if key.startswith("skill:") and file.name != "SKILL.md":
                raise ValueError("Skill source is not SKILL.md")
            if not file.is_file():
                missing.append(key)
            sources[key] = file
        except (ValueError, OSError):
            missing.append(key)
    if PRIMARY in missing:
        raise ValueError("Canonical skill source is missing or unsafe")

    descriptions = descriptions or {}
    # Only installed skill identifiers participate; none is fabricated.
    term_index: dict[str, set[str]] = defaultdict(set)
    for key in skills:
        stem = sources.get(key, Path(key)).parent.name
        for term in _terms(stem.replace("-", " ").replace("_", " ")):
            term_index[term].add(key)

    links = {}
    specialist_count = 0
    for key, meta in sorted(inventory.items()):
        kind = meta.get("kind")
        owner = PRIMARY
        linked_skills = [owner]
        if kind == "skill" and key != owner:
            linked_skills.append(key)  # self-identification: genuine installed SKILL.md
        hint = []
        if kind != "skill":
            target = _terms(key.replace(":", " ").replace("-", " ") +
                            " " + descriptions.get(key, ""))
            scores: Counter = Counter()
            for term in target:
                for possible in term_index.get(term, ()):
                    if possible != owner:
                        scores[possible] += 1
            # Require >=2 independent specialist-name matches; weak matches stay unverified.
            hint = [{"skill": skill, "matching_slug_terms": score,
                     "status": "suggested_not_verified"}
                    for skill, score in sorted(scores.items(), key=lambda p: (-p[1], p[0]))
                    if score >= 2][:3]
            if hint:
                specialist_count += 1
        links[key] = {
            "owner_skill": owner,
            "skill_links": linked_skills,
            "specialist_candidates": hint,
            "source_exists": key not in missing,
            "relationship": "central_orchestrator" if kind != "skill" else "skill_identity",
        }

    orphans = [key for key, row in links.items()
               if not row["skill_links"] or any(s not in skills for s in row["skill_links"])]
    if set(links) != set(inventory):
        raise ValueError("Not all capabilities were represented in the skill-link audit")
    counters = Counter(v.get("kind", "unknown") for v in inventory.values())
    summary = {
        "catalog_total": len(inventory), "by_kind": dict(sorted(counters.items())),
        "installed_skills": len(skills),
        "canonical_owner_linked": sum(row["owner_skill"] == PRIMARY for row in links.values()),
        "skill_identity_links": sum(v.get("kind") == "skill" for v in inventory.values()),
        "specialist_candidates": specialist_count,
        "no_evidence_of_specialist_match": len(inventory) - len(skills) - specialist_count,
        "missing_sources": len(missing), "missing_source_examples": missing[:20],
        "orphan_links": len(orphans), "orphan_examples": orphans[:20],
        "all_owned": not orphans and len(links) == len(inventory),
        "all_sources_present": not missing,
        "all_specialist_links_proven": False,
    }
    packet = {"schema": SCHEMA, "summary": summary, "links": links,
              "limits": ("Canonical ownership connects each catalog entry to the actual "
                         "kosif-superpowers SKILL.md; this is not proof the owner can execute "
                         "every power. Specialist candidates use name-token overlap only and "
                         "must be reviewed. An inventory record is not an execution receipt.")}
    text = json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    packet["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return packet
