#!/usr/bin/env python3
"""Black Dragon structural card validation: a separate evidence tier, never execution.

Every catalog entry (power, superpower, tool, skill, style, playbook, protocol)
is checked against its own source with real, kind-specific structural checks:
required fields, cross references to other catalog IDs, files that the card
names, frontmatter, headings and relative links. Each entry gets one receipt
line in ``validation.jsonl`` (entry, source SHA-256, card SHA-256, checks run,
problems, result) and the job gets ``validation_summary.json`` carrying the
SHA-256 of that file.

"validated" means the card is internally consistent and everything it points
at exists on this machine. It does NOT mean the method was run, that a proof
is correct or that a sibling repository / URL proof is real: those are counted
as ``external_refs_not_checkable`` and never upgrade a card. Validation never
changes the executed count and never makes ``full_coverage`` true.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
from collections import Counter
from pathlib import Path

SCHEMA = "kosif.black-dragon.card-validation.v1"
VALIDATION_FILE = "validation.jsonl"
SUMMARY_FILE = "validation_summary.json"
STATUSES = ("proven", "ready", "install", "key", "seen", "documented", "idea")
PROOF_SCOPES = ("repo", "session", "archive", "sibling", "receipt", "style", "url", "missing", "none")
POWER_REQUIRED = ("id", "family", "name_ar", "name_en", "status", "what", "how", "params",
                  "install", "requires", "license", "proof", "proof_scope", "styles", "tags", "when")
POWER_NONEMPTY = ("id", "family", "name_ar", "name_en", "status", "what")
SP_NONEMPTY = ("id", "domain", "family", "name_ar", "name_en", "best")
TOOL_NONEMPTY = ("id", "path", "root", "kind", "area", "title_en", "title_ar", "summary_en", "safety")
TOOL_KINDS = ("cli", "library", "mcp-server", "template")
STYLE_ORIGINS = ("PromptsMotion", "KOSIF original style")
STYLE_TYPES = ("Prompt", "Skill", "Style")
TRUTH = ("Structural card validation only: required fields, cross references and referenced files "
         "were checked. It is not execution, never counted as executed and never makes "
         "full_coverage true.")

_FENCE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.S | re.M)
_INLINE = re.compile(r"`[^`\n]*`")
_LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^)]*[\"'])?\s*\)")
_HEADING = re.compile(r"^#{1,6}\s+\S", re.M)
_LINE_REF = re.compile(r":\d[\d,\-]*$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canon(obj) -> str:
    return sha256_bytes(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":")).encode("utf-8"))


class _Ctx:
    """Everything the validators cross-reference, loaded once from the given roots."""

    def __init__(self, skill: Path, repo: Path):
        self.skill, self.repo = skill, repo
        self._sha, self._text, self._lines = {}, {}, {}
        self.powers, self.power_files, self.power_dupes = {}, {}, Counter()
        for path in sorted((skill / "data" / "powers").glob("*.json")):
            rows = json.loads(path.read_text(encoding="utf-8"))
            rows = rows if isinstance(rows, list) else rows.get("powers", [])
            for row in rows:
                if isinstance(row, dict) and isinstance(row.get("id"), str):
                    self.power_dupes[row["id"]] += 1
                    self.powers[row["id"]] = row
                    self.power_files[row["id"]] = path
        self.families = {p.stem for p in self.power_files.values()}
        sp = self._json(skill / "data" / "superpowers.json", {})
        self.superpowers = {r["id"]: r for r in sp.get("items", []) if isinstance(r, dict) and r.get("id")}
        tools = self._json(skill / "data" / "tools.json", {})
        self.tools = {r["id"]: r for r in tools.get("tools", []) if isinstance(r, dict) and r.get("id")}
        styles = self._json(repo / "catalog" / "styles.json", [])
        self.styles = {r["id"]: r for r in styles if isinstance(r, dict) and r.get("id")}
        reqs = self._json(skill / "data" / "requirements.json", {})
        self.requirements = {k for k in reqs if not k.startswith("_")}
        self.categories = set()
        for row in self._json(repo / "catalog" / "categories.json", []):
            if isinstance(row, dict) and isinstance(row.get("key"), str):
                self.categories.add(row["key"])
                self.categories.update(x for x in row.get("legacy") or [] if isinstance(x, str))

    @staticmethod
    def _json(path: Path, default):
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return default

    def sha(self, path: Path) -> str | None:
        if path not in self._sha:
            self._sha[path] = sha256_bytes(path.read_bytes()) if path.is_file() else None
        return self._sha[path]

    def text(self, path: Path) -> str | None:
        if path not in self._text:
            try:
                self._text[path] = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                self._text[path] = None
        return self._text[path]

    def line_count(self, path: Path) -> int:
        if path not in self._lines:
            txt = self.text(path)
            self._lines[path] = 0 if txt is None else txt.count("\n") + (0 if txt.endswith("\n") else 1)
        return self._lines[path]

    def repo_path(self, rel: str) -> Path:
        return self.repo / rel.rstrip("/")

    # -- evidence references --------------------------------------------------
    def proof_problem(self, proof, external: Counter) -> str | None:
        """Return a problem for a broken local proof; count references that cannot be checked here."""
        if not isinstance(proof, str) or not proof.strip():
            return "empty_proof: an empty proof entry"
        p = proof.strip()
        if p.startswith("style:"):
            return None if p[6:] in self.styles else "style_ref_missing: " + p
        if p.startswith(("http://", "https://")):
            external["url"] += 1
            return None
        head = p.split("/")[0]
        if (" " in head or "/" not in p or p.startswith(("owner-upload:", "session-"))
                or (":" in head and not re.match(r"^[\w.-]+$", head.split(":")[0]))):
            external["receipt_or_upload"] += 1
            return None
        if head != "kosif-tool":
            external["sibling_repo"] += 1
            return None
        rel = p.split("#")[0][len("kosif-tool/"):]
        m = _LINE_REF.search(rel)
        line = None
        if m:
            nums = [int(n) for n in re.findall(r"\d+", m.group(0))]
            line = max(nums) if nums else None
            rel = rel[:m.start()]
        target = self.repo_path(rel)
        if not target.exists():
            return "proof_path_missing: " + p
        if line is not None and target.is_file() and line > self.line_count(target):
            return f"proof_line_out_of_range: {p} (file has {self.line_count(target)} lines)"
        return None

    def md_problems(self, path: Path, text: str) -> tuple[list, int]:
        """Relative markdown links outside code that do not resolve."""
        body = _INLINE.sub("", _FENCE.sub("", text))
        problems, checked = [], 0
        for target in _LINK.findall(body):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith(("#", "{", "$")):
                continue
            clean = urllib.parse.unquote(target.split("#")[0].split("?")[0])
            if not clean:
                continue
            checked += 1
            base = self.repo if clean.startswith("/") else path.parent
            if not (base / clean.lstrip("/")).exists():
                problems.append("broken_link: " + target)
        return problems, checked


def _require(card: dict, fields, problems: list, nonempty=()) -> None:
    for key in fields:
        if key not in card:
            problems.append("missing_field: " + key)
    for key in nonempty:
        if key in card and not (isinstance(card[key], str) and card[key].strip()):
            problems.append("empty_field: " + key)


def _list(card: dict, key: str) -> list:
    value = card.get(key)
    return value if isinstance(value, list) else []


def _power(key: str, ctx: _Ctx):
    pid = key.split(":", 1)[1]
    card = ctx.powers.get(pid)
    if card is None:
        return {}, None, ["fields"], ["card_missing: no record with this id"], Counter()
    problems, external = [], Counter()
    _require(card, POWER_REQUIRED, problems, POWER_NONEMPTY)
    for k in ("proof", "styles", "tags", "requires"):
        if k in card and not isinstance(card[k], list):
            problems.append("bad_type: " + k + " must be a list")
    if ctx.power_dupes[pid] > 1:
        problems.append(f"duplicate_id: {pid} appears {ctx.power_dupes[pid]} times")
    if card.get("status") not in STATUSES:
        problems.append(f"bad_status: {card.get('status')!r}")
    if card.get("family") != ctx.power_files[pid].stem:
        problems.append(f"family_mismatch: {card.get('family')!r} in {ctx.power_files[pid].name}")
    scope = card.get("proof_scope")
    if scope not in PROOF_SCOPES:
        problems.append(f"bad_proof_scope: {scope!r}")
    if card.get("status") == "proven" and (not card.get("proof") or scope in ("none", "missing")):
        problems.append("proven_without_proof: proven needs a proof and a proof_scope")
    for proof in _list(card, "proof"):
        bad = ctx.proof_problem(proof, external)
        if bad:
            problems.append(bad)
    for req in _list(card, "requires"):
        if req not in ctx.requirements:
            problems.append(f"unknown_requirement: {req}")
    for style in _list(card, "styles"):
        if str(style).removeprefix("style:") not in ctx.styles:
            problems.append(f"style_ref_missing: {style}")
    checks = ["fields", "types", "unique_id", "status", "family_file", "proof_scope",
              "proof_refs", "requirements", "style_refs"]
    return card, ctx.power_files[pid], checks, problems, external


def _superpower(key: str, ctx: _Ctx):
    sid = key.split(":", 1)[1]
    card = ctx.superpowers.get(sid)
    path = ctx.skill / "data" / "superpowers.json"
    if card is None:
        return {}, path, ["fields"], ["card_missing: no record with this id"], Counter()
    problems, external = [], Counter()
    _require(card, ("pipeline", "size", "status_mix", "families", "requires", "proof", "twins", "links"),
             problems, SP_NONEMPTY)
    pipeline = card.get("pipeline") if isinstance(card.get("pipeline"), list) else []
    if not pipeline:
        problems.append("empty_pipeline: a fused superpower needs component powers")
    ids = [p.get("id") for p in pipeline if isinstance(p, dict)]
    for comp in pipeline:
        cid = comp.get("id") if isinstance(comp, dict) else None
        power = ctx.powers.get(cid)
        if power is None:
            problems.append(f"component_missing: power {cid} does not exist")
        elif comp.get("status") != power.get("status"):
            problems.append(f"component_status_drift: {cid} is {power.get('status')!r}, card says {comp.get('status')!r}")
    if len(set(ids)) != len(ids):
        problems.append("duplicate_component: a power is fused twice")
    if card.get("size") != len(pipeline):
        problems.append(f"size_mismatch: size {card.get('size')} but {len(pipeline)} components")
    known = [ctx.powers[c] for c in ids if c in ctx.powers]
    mix = card.get("status_mix") if isinstance(card.get("status_mix"), dict) else {}
    if mix != dict(Counter(p.get("status") for p in known)) and len(known) == len(ids):
        problems.append("status_mix_mismatch: counts differ from the component powers")
    fams = card.get("families") if isinstance(card.get("families"), dict) else {}
    for fam in fams:
        if fam not in ctx.families:
            problems.append(f"unknown_family: {fam}")
    if fams != dict(Counter(p.get("family") for p in known)) and len(known) == len(ids):
        problems.append("families_mismatch: family counts differ from the component powers")
    if card.get("best") not in STATUSES:
        problems.append(f"bad_status: best={card.get('best')!r}")
    for pair in _list(card, "twins"):
        for tid in pair if isinstance(pair, list) else [pair]:
            if tid not in ctx.powers:
                problems.append(f"component_missing: twin {tid} does not exist")
    for link in _list(card, "links"):
        lid = link.get("id") if isinstance(link, dict) else link
        if lid not in ctx.superpowers:
            problems.append(f"link_missing: superpower {lid} does not exist")
    for req in _list(card, "requires"):
        if req not in ctx.requirements:
            problems.append(f"unknown_requirement: {req}")
    for proof in _list(card, "proof"):
        bad = ctx.proof_problem(proof, external)
        if bad:
            problems.append(bad)
    checks = ["fields", "components_exist", "component_status", "unique_components", "size",
              "status_mix", "families",
              "best_status", "twins_exist", "links_exist", "requirements", "proof_refs"]
    return card, path, checks, problems, external


def _tool(key: str, ctx: _Ctx):
    tid = key.split(":", 1)[1]
    card = ctx.tools.get(tid)
    path = ctx.skill / "data" / "tools.json"
    if card is None:
        return {}, path, ["fields"], ["card_missing: no record with this id"], Counter()
    problems = []
    _require(card, ("commands", "tests", "docs", "requires", "families"), problems, TOOL_NONEMPTY)
    if card.get("kind") not in TOOL_KINDS:
        problems.append(f"bad_kind: {card.get('kind')!r}")
    root = card.get("root")
    if root not in ("skill", "repo"):
        problems.append(f"bad_root: {root!r}")
    else:
        rel = str(card.get("path", "")).rstrip("/")
        target = (ctx.skill if root == "skill" else ctx.repo) / rel
        if not rel or not target.exists():
            problems.append("tool_path_missing: " + str(card.get("path")))
    if card.get("kind") == "cli" and not card.get("commands"):
        problems.append("no_commands: a CLI tool documents no command")
    for k in ("tests", "docs"):
        for rel in _list(card, k):
            if not isinstance(rel, str) or not ctx.repo_path(rel).exists():
                problems.append(f"{k[:-1]}_missing: {rel}")
    if card.get("power_id") and card["power_id"] not in ctx.powers:
        problems.append(f"power_ref_missing: {card['power_id']}")
    for fam in _list(card, "families"):
        if fam not in ctx.families:
            problems.append(f"unknown_family: {fam}")
    checks = ["fields", "kind", "path_exists", "commands", "tests_exist", "docs_exist",
              "power_ref", "families"]
    return card, path, checks, problems, Counter()


def _frontmatter(text: str) -> tuple[dict | None, str | None]:
    """Return (fields, yaml_error) for the leading frontmatter block, or (None, None) when absent.

    With PyYAML installed the block must be valid YAML (as a strict skill loader needs);
    the fields are still read leniently so a missing name/description is reported too.
    """
    if not text.startswith("---"):
        return None, None
    lines = text.splitlines()
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, None
    block = "\n".join(lines[1:end])
    error = None
    try:
        import yaml  # optional
        try:
            data = yaml.safe_load(block)
            if isinstance(data, dict):
                return data, None
            error = "frontmatter is not a mapping"
        except yaml.YAMLError as exc:
            error = " ".join(str(exc).split())[:160]
    except ImportError:
        pass
    try:
        data = json.loads(block)
        if isinstance(data, dict):
            return data, None
    except ValueError:
        pass
    meta, current = {}, None
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            current = m.group(1)
            value = m.group(2).strip()
            meta[current] = "" if value in (">", ">-", "|", "|-", ">+", "|+") else value.strip("'\"")
        elif current and line.startswith((" ", "\t")) and line.strip():
            meta[current] = (meta[current] + " " + line.strip()).strip()
    return meta, error


def _skill(key: str, meta: dict, ctx: _Ctx):
    path = ctx.skill.parent / str(meta.get("source", ""))
    text = ctx.text(path)
    if text is None:
        return {}, path, ["readable"], ["source_missing: SKILL.md cannot be read"], Counter()
    problems = []
    if not text.strip():
        problems.append("empty_file: SKILL.md is empty")
    fm, yaml_error = _frontmatter(text)
    if yaml_error:
        problems.append("frontmatter_invalid_yaml: " + yaml_error)
    if fm is None:
        problems.append("no_frontmatter: SKILL.md has no YAML frontmatter block")
    else:
        for field in ("name", "description"):
            if not (isinstance(fm.get(field), str) and fm[field].strip()):
                problems.append("frontmatter_missing: " + field)
    links, n = ctx.md_problems(path, text)
    problems += links
    return {"frontmatter": fm}, path, ["readable", "frontmatter", f"relative_links({n})"], problems, Counter()


def _https(value) -> bool:
    return isinstance(value, str) and value.startswith("https://") and len(value) > 8


def _style(key: str, ctx: _Ctx):
    """Mirror the repository's own style schema (tools/validate.py) for one record."""
    sid = key.split(":", 1)[1]
    card = ctx.styles.get(sid)
    path = ctx.repo / "catalog" / "styles.json"
    if card is None:
        return {}, path, ["fields"], ["card_missing: no record with this id"], Counter()
    problems = []
    _require(card, ("category", "playbooks", "skill", "page"), problems, ("id", "name"))
    if card.get("origin") not in STYLE_ORIGINS:
        problems.append(f"bad_origin: {card.get('origin')!r}")
    if card.get("type") not in STYLE_TYPES:
        problems.append(f"bad_type: type={card.get('type')!r}")
    cats = card.get("category")
    if not isinstance(cats, list) or not all(isinstance(c, str) for c in cats):
        problems.append("bad_type: category must be a list of strings")
    elif ctx.categories:
        for cat in cats:
            if cat not in ctx.categories:
                problems.append(f"unknown_category: {cat}")
    if not _https(card.get("page")):
        problems.append("bad_url: page must be https")
    for field in ("video", "poster", "creator_url"):
        if card.get(field) is not None and not _https(card.get(field)):
            problems.append(f"bad_url: {field} must be null or https")
    if card.get("skill") != f"styles/{sid}/SKILL.md":
        problems.append(f"bad_skill_path: {card.get('skill')!r}")
    if not (ctx.repo / "styles" / sid / "SKILL.md").is_file():
        problems.append(f"style_file_missing: styles/{sid}/SKILL.md")
    style_json = ctx.repo / "styles" / sid / "STYLE.json"
    if not style_json.is_file():
        problems.append(f"style_file_missing: styles/{sid}/STYLE.json")
    else:
        try:
            data = json.loads(style_json.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("id") != sid:
                problems.append("style_json_id_mismatch: STYLE.json id differs from the record")
            elif _canon(data) != _canon(card):
                diff = sorted(k for k in set(data) | set(card) if data.get(k) != card.get(k))
                problems.append("style_json_drift: STYLE.json differs from catalog in " + ", ".join(diff))
        except (OSError, ValueError) as exc:
            problems.append("style_json_invalid: " + str(exc)[:120])
    for rel in _list(card, "playbooks"):
        if not ctx.repo_path(str(rel)).is_file():
            problems.append("playbook_missing: " + str(rel))
    brief = card.get("brief")
    if brief is not None:
        if brief != f"styles/{sid}/BRIEF.md":
            problems.append(f"bad_brief_path: {brief!r}")
        elif not ctx.repo_path(brief).is_file():
            problems.append("brief_missing: " + brief)
    checks = ["fields", "origin_type_enums", "categories_known", "urls", "skill_md",
              "style_json_equals_record", "playbooks_exist", "brief_exists"]
    return card, path, checks, problems, Counter()


def _document(key: str, meta: dict, ctx: _Ctx, kind: str):
    path = (ctx.repo if kind == "playbook" else ctx.skill) / str(meta.get("source", ""))
    text = ctx.text(path)
    if text is None:
        return {}, path, ["readable"], ["source_missing: file cannot be read"], Counter()
    problems = []
    if not text.strip():
        problems.append("empty_file: no content")
    if not _HEADING.search(_FENCE.sub("", text)):
        problems.append("no_heading: no markdown heading")
    links, n = ctx.md_problems(path, text)
    problems += links
    checks = ["readable", "nonempty", "heading", f"relative_links({n})"]
    if kind == "protocol" and path.name == "PROTOCOL.md":
        listed = sorted(set(re.findall(r"\]\((references/protocol/A\d+[^)#\s]*\.md)", text)))
        for rel in listed:
            if not (ctx.skill / rel).is_file():
                problems.append("appendix_missing: " + rel)
        if not listed:
            problems.append("no_trigger_table: the core lists no protocol appendices")
        checks.append(f"trigger_table_appendices({len(listed)})")
    return {}, path, checks, problems, Counter()


def validate_entry(key: str, meta: dict, ctx: _Ctx) -> dict:
    kind = meta.get("kind")
    if kind == "power":
        card, path, checks, problems, external = _power(key, ctx)
    elif kind == "superpower":
        card, path, checks, problems, external = _superpower(key, ctx)
    elif kind == "tool":
        card, path, checks, problems, external = _tool(key, ctx)
    elif kind == "skill":
        card, path, checks, problems, external = _skill(key, meta, ctx)
    elif kind == "style":
        card, path, checks, problems, external = _style(key, ctx)
    elif kind in ("playbook", "protocol"):
        card, path, checks, problems, external = _document(key, meta, ctx, kind)
    else:
        card, path, checks, problems, external = {}, None, [], [f"unknown_kind: {kind!r}"], Counter()
    source_sha = ctx.sha(path) if path is not None else None
    if path is not None and source_sha is None and not any(p.startswith("source_missing") for p in problems):
        problems.append("source_missing: " + str(meta.get("source")))
    if kind in ("skill", "playbook", "protocol"):
        card_sha = source_sha
    else:
        card_sha = _canon(card) if card else None
    return {"entry": key, "kind": kind, "source": meta.get("source"),
            "source_sha256": source_sha, "card_sha256": card_sha,
            "checks": checks, "external_refs_not_checkable": dict(sorted(external.items())),
            "problems": problems, "status": "invalid" if problems else "validated"}


def validate_catalog(inventory: dict, skill: Path, repo: Path) -> list:
    ctx = _Ctx(skill, repo)
    return [validate_entry(key, inventory[key], ctx) for key in sorted(inventory)]


def summarize(rows: list, inventory: dict) -> dict:
    by_kind, categories, external = {}, Counter(), Counter()
    for row in rows:
        k = by_kind.setdefault(row["kind"], {"total": 0, "validated": 0, "invalid": 0})
        k["total"] += 1
        k[row["status"]] += 1
        for category in sorted({p.split(":", 1)[0] for p in row["problems"]}):
            categories[(row["kind"], category)] += 1
        external.update(row["external_refs_not_checkable"])
    validated = sum(r["status"] == "validated" for r in rows)
    return {"schema": SCHEMA, "total": len(inventory), "validated": validated,
            "invalid": len(rows) - validated, "covered_all": {r["entry"] for r in rows} == set(inventory),
            "by_kind": dict(sorted(by_kind.items())),
            "problem_categories": [{"kind": k, "category": c, "entries": n}
                                   for (k, c), n in sorted(categories.items(), key=lambda x: (-x[1], x[0]))],
            "external_refs_not_checkable": dict(sorted(external.items())),
            "yaml_parser": _yaml_parser(), "counts_as_executed": False, "truth": TRUTH}


def _yaml_parser() -> str:
    try:
        import yaml  # noqa: F401
        return "pyyaml (strict frontmatter)"
    except ImportError:
        return "lenient key: value reader (PyYAML not installed; invalid YAML is not detected)"


def write(job: Path, rows: list, inventory: dict) -> dict:
    """Write validation.jsonl (one receipt per entry) and its summary into the job."""
    path = job / VALIDATION_FILE
    if path.exists() or (job / SUMMARY_FILE).exists():
        raise ValueError("Job already has card validation receipts; use a new folder")
    lines = [json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows]
    path.write_text("".join(line + "\n" for line in lines), encoding="utf-8")
    summary = summarize(rows, inventory)
    summary["validation_file"] = str(path)
    summary["validation_sha256"] = sha256_bytes(path.read_bytes())
    (job / SUMMARY_FILE).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def verify_job(job: Path, inventory: dict, skill: Path, repo: Path) -> dict:
    """Re-hash the validation receipts and each validated source; nothing is re-trusted from the report."""
    path, spath = job / VALIDATION_FILE, job / SUMMARY_FILE
    if not path.is_file() or not spath.is_file() or path.is_symlink() or spath.is_symlink():
        return {"present": False, "integrity_passed": True,
                "note": "job has no card validation receipts"}
    summary = json.loads(spath.read_text(encoding="utf-8"))
    errors = []
    digest = sha256_bytes(path.read_bytes())
    if summary.get("validation_sha256") != digest:
        errors.append("validation.jsonl SHA-256 differs from the summary")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    entries = [r.get("entry") for r in rows]
    if len(entries) != len(set(entries)):
        errors.append("duplicate validation receipts")
    if set(entries) != set(inventory):
        errors.append("validation receipts do not cover exactly the catalog")
    validated = sum(r.get("status") == "validated" for r in rows)
    if summary.get("validated") != validated or summary.get("invalid") != len(rows) - validated:
        errors.append("summary counts disagree with the receipts")
    if any(r.get("status") == "validated" and r.get("problems") for r in rows):
        errors.append("a receipt is marked validated while listing problems")
    ctx = _Ctx(skill, repo)
    changed = []
    for row in rows:
        meta = inventory.get(row.get("entry"))
        if meta is None:
            continue
        fresh = validate_entry(row["entry"], meta, ctx)
        if fresh["source_sha256"] != row.get("source_sha256") or fresh["card_sha256"] != row.get("card_sha256"):
            changed.append(row["entry"])
    if changed:
        errors.append(f"{len(changed)} validated source(s) changed since validation, e.g. {changed[0]}")
    return {"present": True, "integrity_passed": not errors, "errors": errors,
            "receipts": len(rows), "validated": validated, "invalid": len(rows) - validated,
            "validation_sha256": digest, "sources_changed": len(changed),
            "counts_as_executed": False}
