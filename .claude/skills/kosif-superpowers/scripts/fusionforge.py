#!/usr/bin/env python3
"""KOSIF FusionForge v2 — project-scoped composite workflow recipes for USIP v5.6.

A recipe (schema kosif.fusionforge.recipe.v2) turns a USIP brief into typed workflow nodes — stage, catalog
capabilities fingerprinted by their atom IDs, input/output artifact kinds, an executor reference — joined by
typed handoff edges, with plans A/B/C taken from the brief. It then records what really happened: the plan the
user chose and why, per-node traces with hashed evidence, and status changes through an enforced state machine
(candidate -> planned -> tested -> verified | failed; verified and failed are final, start again with fork).
FusionForge does not rank capabilities itself: skill_intelligence's brief is the single ranker.

Every subcommand (19), one example each (`<subcommand> --help` lists all options):
  python3 scripts/fusionforge.py propose     "<goal>" --project P [--from-brief brief.json] [--terms "english words"]
  python3 scripts/fusionforge.py show        --project P --id FUSE-...
  python3 scripts/fusionforge.py catalog     --project P
  python3 scripts/fusionforge.py set-graph   --project P --id FUSE-... --file graph.json
  python3 scripts/fusionforge.py bind        --project P --id FUSE-... --node N02 --executor tool:montage-pro
  python3 scripts/fusionforge.py validate    --project P --id FUSE-...
  python3 scripts/fusionforge.py choose      --project P --id FUSE-... --plan B --why "..."   (plan D also needs --nodes)
  python3 scripts/fusionforge.py trace       --project P --id FUSE-... --stage create --node N02 --action "..." \\
                                             --result passed --tool tool:montage-pro --observed "..." --evidence out/job/qa.json
  python3 scripts/fusionforge.py record      --project P --id FUSE-... --status tested --evidence out/job/qa.json
  python3 scripts/fusionforge.py record      --project P --id FUSE-... --status verified --evidence out/job/qa.json --qa-pass
  python3 scripts/fusionforge.py fork        --project P --id FUSE-... [--new-id FUSE-...]
  python3 scripts/fusionforge.py lessons     --project P
  python3 scripts/fusionforge.py reuse       "<goal>" --project P [--from-brief brief.json] [--top 3]
  python3 scripts/fusionforge.py card        --project P --id FUSE-... --out out/cards/recipe.md
  python3 scripts/fusionforge.py import-card out/cards/recipe.md --project P [--new-id FUSE-...]
  python3 scripts/fusionforge.py export      --project P --out out/fusionforge-P.json [--include-candidates]
  python3 scripts/fusionforge.py import      out/fusionforge-P.json --project P
  python3 scripts/fusionforge.py migrate     --project P
  python3 scripts/fusionforge.py promote     --project P --id FUSE-...

Global options: --root DIR (else $KOSIF_FUSIONFORGE_ROOT, else <git top of cwd>/out/fusionforge, else
<git checkout holding this skill>/out/fusionforge; with none of these the command stops with NO_ROOT), --catalog-file,
--tools-file, --now ISO8601. Every command takes --json (full JSON, always with "root"); the default output is a
short summary. Errors are one line "fusionforge: error: CODE: message"; exit 2 = usage/validation/state,
3 = NO_MATCH on propose, 4 = validate errors.

Evidence must be a regular, non-empty, non-symlink file inside the working directory, its git checkout, the
FusionForge root or the skill's git checkout; never a FusionForge record (by place, hard link or content), a
credential store (.env, .ssh/, id_rsa, ...) or a text file holding a credential pattern. It is hashed, files up to
5 MB are copied to <project>/evidence/<sha256><suffix>, and records keep only relative paths. Every written text
field (paths and --project included) is scanned for credentials (scripts/_secrets.py) and refused when one is
found. Node results (trace --result) count only after choose; writes are atomic under a lock; a malformed sibling
record is listed as invalid and never breaks commands on the others.

What it does NOT do: it never executes a power or tool, installs anything, contacts the network, publishes or
commits records, edits the catalog, or trains or fine-tunes a model. "verified" means the caller's own QA, with
evidence, passed this engine's gate (tested state, --qa-pass, every node of the chosen plan passed or skipped, a
verify node passed with evidence, evidence unlike any failure evidence and not already used to verify another
recipe, clean validate); the engine checks the records, not the quality of the work itself. "Learning" means
lessons and rankings computed from recorded traces of the same project (lessons, reuse, recall in propose);
nothing is learned across projects and nothing is swapped automatically. Records live under <root>/<project>/
(out/ is git-ignored) and do not survive a new machine or cloud session unless the user exports and imports
them. Python stdlib only.
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import secrets as pysecrets
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows
    fcntl = None
try:
    import msvcrt
except ImportError:
    msvcrt = None

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
CATALOG = SKILL / "data" / "superpowers.json"
TOOLS = SKILL / "data" / "tools.json"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from _secrets import SecretError, find_secrets, refuse_secrets, scan_object  # noqa: E402

ENGINE = "FusionForge v2"
PROTOCOL = "USIP v5.6"
SCHEMA = "kosif.fusionforge.recipe.v2"
SCHEMA_V1 = "kosif.fusionforge.recipe.v1"
CARD_SCHEMA = "kosif.fusionforge.card.v2"
BUNDLE_SCHEMA = "kosif.fusionforge.bundle.v2"
INDEX_SCHEMA = "kosif.fusionforge.index.v2"
LESSONS_SCHEMA = "kosif.fusionforge.lessons.v2"
PROMOTION_SCHEMA = "kosif.fusionforge.promotion.v2"

STAGES = ("understand", "research", "plan", "build", "create", "refine", "assemble", "verify", "deliver")
STATUSES = ("candidate", "planned", "tested", "verified", "failed")
TRANSITIONS = {"candidate": ("planned", "failed"), "planned": ("tested", "failed"),
               "tested": ("tested", "verified", "failed"), "verified": (), "failed": ()}
TERMINAL = ("verified", "failed")
KINDS = ("brief", "spec", "plan", "sources", "code", "dataset", "report", "document", "image", "audio", "video",
         "model3d", "font", "prompt", "evidence", "package", "any")
RELATIONS = ("sequence", "parallel", "complement", "substitute", "verify", "refine", "fallback")
NODE_STATUSES = ("pending", "passed", "failed", "skipped")
RESULTS = ("passed", "failed", "skipped")
ERROR_CLASSES = ("missing_dependency", "wrong_input_kind", "quality_below_threshold", "timeout",
                 "permission_denied", "license_blocked", "tool_error", "other")
PLAN_LETTERS = ("A", "B", "C", "D")
PLAN_LABELS = {"A": "simplest path that meets every must-have",
               "B": "balanced professional with cross-domain integration",
               "C": "different engine, source or verification method (not B plus extras)",
               "D": "user-approved merge of named nodes from A/B/C"}
DELIVERABLE_KIND = {"video": "video", "audio": "audio", "image": "image", "drawing": "image", "3d": "model3d",
                    "code": "code", "app": "code", "web": "code", "reverse": "report", "data": "dataset",
                    "document": "document", "text": "document", "research": "report", "font": "font"}
ATOM_RANK = ("proven", "ready", "install", "documented", "seen", "key", "idea")
CODES = {"SCHEMA": "V01", "STATE_LOG_INVALID": "V02", "HANDOFF_KIND_MISMATCH": "V03", "NO_FINAL_VERIFY": "V04",
         "EXECUTOR_UNKNOWN": "V05", "EVIDENCE_MISSING": "V06", "EVIDENCE_HASH_MISMATCH": "V07", "SECRET": "V08",
         "SELF_EVIDENCE": "V09", "VERIFIED_WITHOUT_RUN": "V10", "CATALOG_DRIFT": "V11", "UNKNOWN_CAPABILITY": "V12"}
SLUG_RX = re.compile(r"[A-Za-z0-9_-]{1,70}")
ID_RX = re.compile(r"FUSE-[0-9]{8}-[0-9a-f]{10}")
NODE_RX = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,23}")
STORED_RX = re.compile(r"evidence/[0-9a-f]{64}(?:\.[a-z0-9]{1,10})?")
SHA_RX = re.compile(r"[0-9a-f]{64}")
EVIDENCE_COPY_MAX = 5 * 1024 * 1024
SIM_MIN = 0.15        # goal text only (cross-language paraphrases score ~0.17-0.2)
SIM_MIN_BLEND = 0.2   # goal + brief capabilities
REMAP_MIN = 0.6
FIELD_MAX = 4000
QA_TOOL_RX = re.compile(r"verify|check|qa|audit|lint|test|scan|gate|validat")
FORBIDDEN_EVIDENCE = ("recipes", "legacy", "cards", "exports", "promotions")
FORBIDDEN_EVIDENCE_FILES = ("index.json", "lessons.json", ".lock")
FORBIDDEN_OUT = ("recipes", "legacy", "evidence")  # card/export --out may never land here
SENSITIVE_DIRS = (".ssh", ".aws", ".gnupg", ".gpg", ".azure", ".kube", ".docker", ".password-store", ".gcloud")
SENSITIVE_NAME_RX = re.compile(r"(?i)(?:\.env(?:\..+)?|\.npmrc|\.pypirc|\.netrc|_netrc|\.git-credentials|\.htpasswd|\.pgpass|credentials"
                               r"|id_(?:rsa|dsa|ecdsa|ed25519)|.+\.(?:p12|pfx|jks|keystore|kdbx))")
SIM_W_GOAL, SIM_W_CAPS = 0.5, 0.5
TEMPLATE_MIN = 0.05


class FFError(Exception):
    def __init__(self, code: str, message: str, rc: int = 2, data=None):
        super().__init__(message)
        self.code, self.rc, self.data = code, rc, data


class Parser(argparse.ArgumentParser):
    def error(self, message):  # one line, never argparse's multi-line usage dump
        raise FFError("USAGE", message)


# ------------------------------------------------------------------ small helpers
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_text(s: str) -> str:
    return sha256_bytes(s.encode("utf-8"))


def hash_file(path: Path) -> tuple:
    h, n = hashlib.sha256(), 0
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


def dump(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def write_atomic(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = data.encode("utf-8") if isinstance(data, str) else data
    fd, tmp = tempfile.mkstemp(prefix="." + path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


@contextlib.contextmanager
def locked(space: Path):
    """Exclusive project lock (fcntl, msvcrt fallback, no-op when neither exists)."""
    space.mkdir(parents=True, exist_ok=True)
    fh = open(space / ".lock", "a+b")
    try:
        if fcntl is not None:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        elif msvcrt is not None:  # pragma: no cover - Windows
            while True:
                try:
                    fh.seek(0)
                    msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 1)
                    break
                except OSError:
                    time.sleep(0.05)
        yield
    finally:
        with contextlib.suppress(OSError):
            if fcntl is not None:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
            elif msvcrt is not None:  # pragma: no cover - Windows
                fh.seek(0)
                msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
        fh.close()


def as_dict(x) -> dict:
    return x if isinstance(x, dict) else {}


def strset(x) -> set:
    return {v for v in x if isinstance(v, str)} if isinstance(x, (list, tuple, dict)) else set()


def edges_of(r: dict) -> list:
    return [e for e in r.get("edges") or [] if isinstance(e, dict) and isinstance(e.get("from"), str) and isinstance(e.get("to"), str)]


def jaccard(a, b) -> float:
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0


def clip(s, n=90) -> str:
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


_PATH_CH = r"[^\s/\\\"'<>|()\[\]]"


def redact_text(s: str) -> str:
    """Hide absolute local paths (file:// URLs, POSIX, Windows drive and UNC, home) inside free text."""
    s = re.sub(r"(?i)\bfile://[^\s\"'<>|()\[\]]*", "<abs-path>", s)
    s = re.sub(r"\\\\" + _PATH_CH + r"+\\[^\s\"'<>|()\[\]]+", "<abs-path>", s)
    s = re.sub(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s\"'<>|()\[\]]+", "<abs-path>", s)
    s = re.sub(r"(?<![\w.~/\\-])/(?!/)(?:" + _PATH_CH + r"+/)+" + _PATH_CH + "*", "<abs-path>", s)
    return re.sub(r"(?<![\w])~/[^\s\"'<>|()\[\]]+", "<home-path>", s)


def redact_obj(obj):
    if isinstance(obj, dict):
        return {k: redact_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_obj(v) for v in obj]
    if isinstance(obj, str):
        return redact_text(obj)
    return obj


def refuse(_limit: bool = True, **fields) -> None:
    """Refuse credentials in any written text field (and over-long fields unless _limit is False)."""
    try:
        refuse_secrets(**fields)
    except SecretError as exc:
        raise FFError("SECRET", str(exc)) from None
    for k, v in fields.items() if _limit else ():
        for s in (v if isinstance(v, (list, tuple)) else [v]):
            if isinstance(s, str) and len(s) > FIELD_MAX:
                raise FFError("TOO_LONG", f"field '{k}' is longer than {FIELD_MAX} characters; summarise it or attach a file as evidence")


_SI = None


def si():
    """skill_intelligence (same scripts dir): the one tokenizer/ranker shared with the USIP brief."""
    global _SI
    if _SI is None:
        try:
            import skill_intelligence as mod
        except Exception as exc:  # noqa: BLE001
            raise FFError("SKILL_INTELLIGENCE_UNAVAILABLE", f"cannot import skill_intelligence.py ({type(exc).__name__}: {exc})") from None
        _SI = mod
    return _SI


# ------------------------------------------------------------------ context: root, clock, catalog, tools
def git_toplevel(cwd: Path):
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(cwd), capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return Path(r.stdout.strip()).resolve()
    except (OSError, subprocess.SubprocessError):
        pass
    return None


_SKILL_REPO = []


def skill_repo():
    """The git checkout that holds this skill, or None (e.g. a copy under ~/.claude/skills is not a repository)."""
    if not _SKILL_REPO:
        _SKILL_REPO.append(git_toplevel(SKILL))
    return _SKILL_REPO[0]


def parse_now(value):
    if not value:
        return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    if not isinstance(value, str):
        raise FFError("BAD_NOW", "--now must be ISO 8601, e.g. 2026-10-21T12:00:00Z")
    try:
        d = dt.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        raise FFError("BAD_NOW", "--now must be ISO 8601, e.g. 2026-10-21T12:00:00Z") from None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.astimezone(dt.timezone.utc).replace(microsecond=0)


def iso(d) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    try:
        return parse_now(s) if s else None
    except FFError:
        return None


class Ctx:
    def __init__(self, a):
        self.cwd = Path.cwd().resolve()
        self.git_top = git_toplevel(self.cwd)
        if getattr(a, "root", None):
            self.root, self.root_source = Path(a.root).expanduser().resolve(), "--root"
        elif os.environ.get("KOSIF_FUSIONFORGE_ROOT"):
            self.root, self.root_source = Path(os.environ["KOSIF_FUSIONFORGE_ROOT"]).expanduser().resolve(), "env"
        elif self.git_top:
            self.root, self.root_source = self.git_top / "out" / "fusionforge", "git"
        elif skill_repo():
            self.root, self.root_source = skill_repo() / "out" / "fusionforge", "skill-repo"
        else:
            raise FFError("NO_ROOT", "no FusionForge root: run inside a git checkout, or pass --root DIR or set "
                                     "KOSIF_FUSIONFORGE_ROOT (the skill itself is not inside a git checkout)")
        self.fixed_now = bool(getattr(a, "now", None))
        self.now = parse_now(getattr(a, "now", None))
        self.now_s = iso(self.now)
        self.catalog_file = Path(getattr(a, "catalog_file", None) or CATALOG)
        self.tools_file = Path(getattr(a, "tools_file", None) or TOOLS)
        self._catalog = self._tools = self._vocab = None

    @property
    def catalog(self) -> dict:
        if self._catalog is None:
            try:
                raw = self.catalog_file.read_bytes()
                data = json.loads(raw.decode("utf-8-sig"))
            except (OSError, ValueError) as exc:
                raise FFError("CATALOG_UNREADABLE", f"{self.catalog_file.name}: {exc}") from None
            items = data.get("items") if isinstance(data, dict) else None
            if not isinstance(items, list):
                raise FFError("CATALOG_UNREADABLE", f"{self.catalog_file.name} has no items list")
            by_id, owner = {}, {}
            for it in items:
                if isinstance(it, dict) and isinstance(it.get("id"), str):
                    by_id[it["id"]] = it
                    for m in it.get("pipeline") or []:
                        if isinstance(m, dict) and m.get("id"):
                            owner[m["id"]] = it["id"]
            self._catalog = {"sha256": sha256_bytes(raw), "by_id": by_id, "atom_owner": owner}
        return self._catalog

    @property
    def tools(self) -> dict:
        if self._tools is None:
            try:
                data = json.loads(self.tools_file.read_text(encoding="utf-8-sig"))
                rows = data.get("tools") if isinstance(data, dict) else None
                if not isinstance(rows, list):
                    raise ValueError("no tools list")
            except (OSError, ValueError) as exc:
                raise FFError("TOOLS_UNREADABLE", f"{self.tools_file.name}: {exc}") from None
            self._tools = {t["id"]: t for t in rows if isinstance(t, dict) and isinstance(t.get("id"), str)}
        return self._tools

    @property
    def vocab(self) -> collections.Counter:
        """Catalog vocabulary so skill_intelligence.expand can strip Arabic clitics against real words."""
        if self._vocab is None:
            S = si()
            df = collections.Counter()
            for it in self.catalog["by_id"].values():
                text = " ".join([str(it.get("name_en", "")), str(it.get("name_ar", "")), " ".join(map(str, it.get("focus") or []))]
                                + [str(m.get("name_en", "")) + " " + str(m.get("name_ar", "")) for m in it.get("pipeline") or [] if isinstance(m, dict)])
                df.update(set(S.tokens(text)))
            self._vocab = df
        return self._vocab

    def base_path(self, label):
        if not isinstance(label, str):
            return None
        if label == "repo":
            return skill_repo()
        return {"git": self.git_top, "root": self.root, "cwd": self.cwd}.get(label)


def fingerprint(item: dict) -> dict:
    atoms = sorted({m["id"] for m in item.get("pipeline") or [] if isinstance(m, dict) and m.get("id")})
    return {"name_en": item.get("name_en", ""), "name_ar": item.get("name_ar", ""), "atoms": atoms,
            "atoms_sha256": sha256_text(",".join(atoms)) if atoms else None, "known": True}


def cap_entry(ctx, cid: str, meta=None) -> dict:
    it = ctx.catalog["by_id"].get(cid)
    if it:
        return fingerprint(it)
    meta = meta or {}
    return {"name_en": meta.get("name_en", ""), "name_ar": meta.get("name_ar", ""), "atoms": [], "atoms_sha256": None, "known": False}


def drift(ctx, recipe: dict) -> dict:
    """Map each remembered capability to the current catalog by atom fingerprints (SP ids are positional)."""
    cat = ctx.catalog
    same = as_dict(recipe.get("catalog")).get("file_sha256") == cat["sha256"]
    out = {"same_catalog": same, "current": {}, "remapped": {}, "stale": [], "unknown": []}
    for cid in sorted(as_dict(recipe.get("capabilities"))):
        fp = as_dict(recipe["capabilities"][cid])
        atoms = fp.get("atoms") or []
        cur = cat["by_id"].get(cid)
        if not atoms:
            (out["unknown"] if not cur or not fp.get("known") else out["stale"]).append(cid)
            continue
        if cur and fingerprint(cur)["atoms_sha256"] == fp.get("atoms_sha256"):
            out["current"][cid] = cid
            continue
        votes = collections.Counter(cat["atom_owner"][a] for a in atoms if a in cat["atom_owner"])
        best, best_j = None, 0.0
        for sid, inter in sorted(votes.items()):
            size = len(fingerprint(cat["by_id"][sid])["atoms"])
            j = inter / (len(atoms) + size - inter)
            if j > best_j:
                best, best_j = sid, j
        if best and best_j >= REMAP_MIN:
            out["remapped"][cid] = best
        else:
            out["stale"].append(cid)
    return out


def current_caps(dr: dict) -> set:
    return set(dr["current"].values()) | set(dr["remapped"].values())


# ------------------------------------------------------------------ project space and recipe files
def space_of(ctx, project: str, must_exist: bool = False) -> Path:
    if not SLUG_RX.fullmatch(project or ""):
        raise FFError("BAD_PROJECT", "project must be 1-70 letters, digits, '_' or '-'")
    space = ctx.root / project
    for p in (space, space / "recipes"):
        if p.is_symlink():
            raise FFError("SYMLINK_REFUSED", f"{p.name} is a symlink; FusionForge refuses symlinked project folders")
    if must_exist and not space.is_dir():
        raise FFError("NOT_FOUND", f"project '{project}' has no records under {ctx.root}")
    return space


def recipe_path(space: Path, rid: str) -> Path:
    if not ID_RX.fullmatch(rid or ""):
        raise FFError("BAD_ID", "recipe id must look like FUSE-YYYYMMDD-<10 hex>")
    return space / "recipes" / f"{rid}.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_recipe(space: Path, rid: str, allow_v1: bool = False) -> dict:
    path = recipe_path(space, rid)
    if path.is_symlink():
        raise FFError("SYMLINK_REFUSED", f"{path.name} is a symlink")
    if not path.is_file():
        raise FFError("NOT_FOUND", f"no recipe {rid} in project '{space.name}'")
    try:
        r = read_json(path)
    except (OSError, ValueError) as exc:
        raise FFError("RECIPE_UNREADABLE", f"{path.name}: {type(exc).__name__}") from None
    if not isinstance(r, dict) or r.get("id") != rid:
        raise FFError("RECIPE_UNREADABLE", f"{path.name} is not a recipe object for {rid}")
    if r.get("schema") == SCHEMA_V1 and not allow_v1:
        raise FFError("LEGACY_RECIPE", f"{rid} is a v1 recipe; run: fusionforge.py migrate --project {space.name}")
    if r.get("schema") not in (SCHEMA, SCHEMA_V1):
        raise FFError("RECIPE_UNREADABLE", f"{path.name} has unknown schema {r.get('schema')!r}")
    return r


def _opt(x, t) -> bool:
    return x is None or isinstance(x, t)


def _strs(x, optional: bool = False) -> bool:
    return (optional and x is None) or (isinstance(x, list) and all(isinstance(v, str) for v in x))


def _evidence_ok(e) -> bool:
    return (isinstance(e, dict) and isinstance(e.get("sha256"), str) and _opt(e.get("size"), int)
            and all(_opt(e.get(k), str) for k in ("stored", "source", "source_base", "root_rel", "suffix", "status", "note", "at")))


def malformed(r) -> list:
    """Strict structural check: every field a command reads has the type it expects. A recipe with problems here is
    listed as invalid (never mined, ranked or exported) and refused by writing commands; validate reports details."""
    if not isinstance(r, dict):
        return ["recipe"]
    types = {"schema": str, "id": str, "goal": str, "status": str, "nodes": list, "edges": list, "plans": dict,
             "capabilities": dict, "traces": list, "evidence": list, "status_log": list}
    optional = {"project": str, "created_at": str, "updated_at": str, "plan_choice": dict, "baseline": dict, "brief": dict,
                "catalog": dict, "recall": dict, "tool_states": dict, "warnings": list, "provenance": dict, "forked_from": str,
                "import_receipt": dict, "suggested_plan": str, "graph_log": list, "similar_unverified": list, "self_reported": list}
    bad = [k for k, t in types.items() if not isinstance(r.get(k), t)] + [k for k, t in optional.items() if not _opt(r.get(k), t)]
    if bad:
        return bad
    if r["status"] not in STATUSES:
        bad.append("status")
    if not all(isinstance(w, str) for w in r.get("warnings") or []):
        bad.append("warnings")
    for i, n in enumerate(r["nodes"]):
        ok = (isinstance(n, dict) and isinstance(n.get("id"), str) and isinstance(n.get("stage"), str) and isinstance(n.get("status"), str)
              and isinstance(n.get("executor"), dict) and isinstance(n["executor"].get("ref"), str) and _strs(n.get("capability_ids"))
              and all(isinstance(n.get(s), list) and all(isinstance(p, dict) and isinstance(p.get("kind"), str) for p in n[s])
                      for s in ("inputs", "outputs"))
              and _opt(n.get("last_trace"), int) and _opt(n.get("memory"), dict))
        if not ok:
            bad.append(f"nodes[{i}]")
            break
    for i, e in enumerate(r["edges"]):
        if not isinstance(e, dict) or not all(isinstance(e.get(k), str) for k in ("id", "from", "to", "kind", "relation")):
            bad.append(f"edges[{i}]")
            break
    for k, v in sorted(r["plans"].items()):
        if not isinstance(v, dict) or not _strs(v.get("nodes")):
            bad.append(f"plans.{k}")
            break
    pc = r.get("plan_choice")
    if pc is not None and (not isinstance(pc.get("plan"), str) or not _strs(pc.get("nodes")) or not _opt(pc.get("why"), str)):
        bad.append("plan_choice")
    for i, t in enumerate(r["traces"]):
        ok = (isinstance(t, dict) and isinstance(t.get("seq"), int) and not isinstance(t.get("seq"), bool)
              and all(_opt(t.get(k), str) for k in ("node", "result", "tool", "stage", "action", "observed", "input", "output", "error_class", "at"))
              and _strs(t.get("capabilities"), optional=True) and (t.get("evidence") is None or _evidence_ok(t["evidence"]))
              and _opt(t.get("substitution"), dict))
        if not ok:
            bad.append(f"traces[{i}]")
            break
    for i, e in enumerate(r["evidence"]):
        if not _evidence_ok(e):
            bad.append(f"evidence[{i}]")
            break
    if r.get("baseline") is not None and not _evidence_ok(r["baseline"]):
        bad.append("baseline")
    for i, s in enumerate(r["status_log"]):
        if not isinstance(s, dict) or not all(_opt(s.get(k), str) for k in ("from", "to", "at", "cmd", "note", "evidence_sha256")):
            bad.append(f"status_log[{i}]")
            break
    for k, v in sorted(r["capabilities"].items()):
        if not isinstance(v, dict) or not _strs(v.get("atoms"), optional=True) or not _opt(v.get("atoms_sha256"), str):
            bad.append(f"capabilities.{k}")
            break
    rc = r.get("recall") or {}
    if not all(isinstance(rc.get(k) or [], list) and all(isinstance(m, dict) for m in rc.get(k) or []) for k in ("matches", "avoid")):
        bad.append("recall")
    ir = r.get("import_receipt")
    if ir is not None and not all(_opt(ir.get(k), int) and not isinstance(ir.get(k), bool) for k in ("trace_seq", "log_len")):
        bad.append("import_receipt")
    return bad


def require_wellformed(r: dict) -> dict:
    bad = malformed(r)
    if bad:
        raise FFError("RECIPE_INVALID", f"{r.get('id')} has malformed {', '.join(bad)}; run validate for details, fix the file by hand "
                                        "or start again with propose")
    return r


def list_recipes(space: Path) -> tuple:
    """(v2 recipes, v1 recipes, invalid files) — a corrupt sibling never breaks the listing."""
    good, legacy, invalid = [], [], []
    rdir = space / "recipes"
    if not rdir.is_dir() or rdir.is_symlink():
        return good, legacy, invalid
    for p in sorted(rdir.glob("FUSE-*.json")):
        if not ID_RX.fullmatch(p.stem):
            continue
        try:
            if p.is_symlink():
                raise ValueError("symlink")
            r = read_json(p)
            if not isinstance(r, dict) or r.get("id") != p.stem:
                raise ValueError("id does not match file name")
            if r.get("schema") == SCHEMA_V1:
                legacy.append(r)
            elif r.get("schema") == SCHEMA:
                bad = malformed(r)
                if bad:
                    raise ValueError("malformed " + ", ".join(bad[:4]) + "; run validate on it")
                good.append(r)
            else:
                raise ValueError(f"unknown schema {clip(repr(r.get('schema')), 40)}")
        except (OSError, ValueError) as exc:
            invalid.append({"file": f"recipes/{p.name}", "error": clip(f"{type(exc).__name__}: {exc}", 160)})
    return good, legacy, invalid


def index_row(r: dict) -> dict:
    count = lambda k: len(r[k]) if isinstance(r.get(k), list) else 0  # noqa: E731
    return {"id": r.get("id"), "status": r.get("status"), "goal": clip(r.get("goal"), 120),
            "nodes": count("nodes"), "traces": count("traces"),
            "evidence": count("evidence"), "plan": as_dict(r.get("plan_choice")).get("plan"),
            "imported": bool(r.get("imported")), "legacy_unproven": bool(r.get("legacy_unproven")),
            "updated_at": r.get("updated_at")}


def refresh_index(space: Path) -> dict:
    good, legacy, invalid = list_recipes(space)
    rows = [index_row(r) for r in good]
    index = {"schema": INDEX_SCHEMA, "project": space.name, "total": len(rows),
             "by_status": {s: sum(1 for r in rows if r["status"] == s) for s in STATUSES},
             "recipes": rows, "legacy_v1": [r.get("id") for r in legacy], "invalid_files": invalid}
    write_atomic(space / "index.json", dump(index))
    return index


def save_recipe(space: Path, r: dict) -> Path:
    path = recipe_path(space, r["id"])
    write_atomic(path, dump(r))
    refresh_index(space)
    return path


def new_id(ctx, space: Path, seed: str, wanted=None) -> str:
    if wanted:
        if not ID_RX.fullmatch(wanted):
            raise FFError("BAD_ID", "--id/--new-id must look like FUSE-YYYYMMDD-<10 hex>")
        if recipe_path(space, wanted).exists():
            raise FFError("ID_EXISTS", f"{wanted} already exists in project '{space.name}'")
        return wanted
    day = ctx.now.strftime("%Y%m%d")
    for i in range(1000):
        tail = sha256_text(f"{seed}|{ctx.now_s}|{i}")[:10] if ctx.fixed_now else pysecrets.token_hex(5)
        rid = f"FUSE-{day}-{tail}"
        if not recipe_path(space, rid).exists():
            return rid
    raise FFError("ID_EXHAUSTED", "could not find a free recipe id")


def log_entry(ctx, frm, to, cmd, note="", evidence_sha=None, **extra) -> dict:
    e = {"from": frm, "to": to, "at": ctx.now_s, "cmd": cmd, "note": note or "", "evidence_sha256": evidence_sha}
    e.update(extra)
    return e


# ------------------------------------------------------------------ evidence policy
def ff_record_kind(data: bytes):
    """'card' or the kosif.fusionforge.* schema when the bytes are a FusionForge record or card, else None."""
    if b"```json fusionforge-card-v2" in data:
        return "card"
    if data.lstrip()[:1] != b"{" or b"kosif.fusionforge." not in data:
        return None
    try:
        obj = json.loads(data.decode("utf-8-sig"))
    except ValueError:
        return None
    schema = obj.get("schema") if isinstance(obj, dict) else None
    return schema if isinstance(schema, str) and schema.startswith("kosif.fusionforge.") else None


def hard_link_of_record(space: Path, rp: Path) -> bool:
    try:
        st = rp.stat()
    except OSError:
        return False
    if st.st_nlink < 2:
        return False
    for f in [*(space / "recipes").glob("*"), space / "index.json", space / "lessons.json"]:
        with contextlib.suppress(OSError):
            o = f.stat()
            if (o.st_dev, o.st_ino) == (st.st_dev, st.st_ino):
                return True
    return False


def evidence_receipt(ctx, space: Path, raw: str, role: str = "evidence", store: bool = True) -> dict:
    if not raw or not str(raw).strip():
        raise FFError("EVIDENCE_REQUIRED", f"{role} needs a file path")
    refuse(**{role: str(raw)})
    p = Path(str(raw)).expanduser()
    if not p.is_absolute():
        p = ctx.cwd / p
    if p.is_symlink():
        raise FFError("EVIDENCE_SYMLINK", f"{role} must be a regular file, not a symlink ({p.name})")
    try:
        rp = p.resolve(strict=True)
    except (OSError, RuntimeError):
        raise FFError("EVIDENCE_MISSING", f"{role} file not found: {p.name}") from None
    if not rp.is_file():
        raise FFError("EVIDENCE_NOT_FILE", f"{role} must be a regular file ({p.name})")
    with contextlib.suppress(ValueError):
        parts = rp.relative_to(ctx.root).parts
        if (len(parts) >= 2 and parts[1] in FORBIDDEN_EVIDENCE) or (len(parts) == 2 and parts[1] in FORBIDDEN_EVIDENCE_FILES):
            raise FFError("SELF_EVIDENCE", f"{role} cannot be a FusionForge record ({'/'.join(parts[1:])}); use the artifact or QA report itself")
    low = [x.lower() for x in rp.parts]
    if any(x in SENSITIVE_DIRS for x in low) or any(a == ".config" and b in ("gcloud", "gh") for a, b in zip(low, low[1:])) \
            or SENSITIVE_NAME_RX.fullmatch(rp.name):
        raise FFError("EVIDENCE_SENSITIVE", f"{role} looks like a credential store ({rp.name}); never use secrets as evidence")
    if hard_link_of_record(space, rp):
        raise FFError("SELF_EVIDENCE", f"{role} is a hard link to a FusionForge record; use the artifact or QA report itself")
    base = None
    for label in ("git", "repo", "root", "cwd"):
        b = ctx.base_path(label)
        if b is None:
            continue
        with contextlib.suppress(ValueError):
            rel = rp.relative_to(b)
            base = (label, rel.as_posix())
            break
    if base is None:
        raise FFError("EVIDENCE_OUTSIDE_ALLOWED", f"{role} must live inside the working directory, its git checkout, "
                                                  "the FusionForge root or the skill's git checkout")
    size = rp.stat().st_size
    if size == 0:
        raise FFError("EVIDENCE_EMPTY", f"{role} file is empty ({p.name})")
    suffix = rp.suffix.lower() if re.fullmatch(r"\.[a-z0-9]{1,10}", rp.suffix.lower()) else ""
    stored, data, root_rel = None, None, None
    if size <= EVIDENCE_COPY_MAX:
        data = rp.read_bytes()
        sha, size = sha256_bytes(data), len(data)
        if size == 0:
            raise FFError("EVIDENCE_EMPTY", f"{role} file is empty ({p.name})")
        if ff_record_kind(data):
            raise FFError("SELF_EVIDENCE", f"{role} is a copy of a FusionForge record or card ({p.name}); use the artifact or QA report itself")
        if b"\x00" not in data[:8192]:
            kinds = find_secrets(data.decode("utf-8", errors="replace"))
            if kinds:
                raise FFError("SECRET", f"{role} file {p.name} contains a credential pattern ({', '.join(kinds)}); "
                                        "redact it and save the result again — nothing was written")
        stored = f"evidence/{sha}{suffix}"
    else:
        sha, size = hash_file(rp)
        root_rel = Path(os.path.relpath(rp, ctx.root)).as_posix()  # large files are not copied: a second locator
    refuse(_limit=False, **{role: [base[1], root_rel or ""]})
    rec = {"sha256": sha, "size": size, "suffix": suffix, "stored": stored, "source": base[1], "source_base": base[0]}
    if root_rel:
        rec["root_rel"] = root_rel
    if store:
        persist_evidence(space, rec, data)
    else:
        rec["_data"] = data
    return rec


def persist_evidence(space: Path, rec: dict, data=None) -> dict:
    """Copy small evidence into the content-addressed store <space>/evidence/<sha256><suffix>."""
    data = rec.pop("_data", None) if data is None else data
    rec.pop("_data", None)
    if rec.get("stored") and data is not None:
        dest = space / rec["stored"]
        if not dest.is_file() or hash_file(dest)[0] != rec["sha256"]:
            write_atomic(dest, data)
    return rec


def evidence_location(ctx, space: Path, rec: dict):
    """(state, path) where state is ok | mismatch | missing."""
    def check(f: Path):
        try:
            if f.is_file() and not f.is_symlink():
                return ("ok" if hash_file(f)[0] == rec.get("sha256") else "mismatch"), f
        except OSError:
            pass
        return None
    stored = rec.get("stored")
    if isinstance(stored, str) and STORED_RX.fullmatch(stored):
        hit = check(space / stored)
        if hit:
            return hit
    base = ctx.base_path(rec.get("source_base"))
    src = rec.get("source")
    if base is not None and isinstance(src, str) and src and not src.startswith("/") and ".." not in Path(src).parts:
        hit = check(base / src)
        if hit:
            return hit
    rr = rec.get("root_rel")
    if not stored and isinstance(rr, str) and rr and not Path(rr).is_absolute():
        hit = check(ctx.root / rr)
        if hit:
            return hit
    return "missing", None


def evidence_records(r: dict):
    """Yield (where, record, with_failure) for every evidence record in a recipe."""
    for i, e in enumerate(r.get("evidence") or []):
        if isinstance(e, dict):
            yield f"evidence[{i}]", e, e.get("status") == "failed"
    for t in r.get("traces") or []:
        if isinstance(t, dict) and isinstance(t.get("evidence"), dict):
            yield f"trace#{t.get('seq')}", t["evidence"], t.get("result") == "failed"
    if isinstance(r.get("baseline"), dict):
        yield "baseline", r["baseline"], False


# ------------------------------------------------------------------ executors
def ref_problem(ctx, ref) -> str:
    """'' when the executor reference resolves; otherwise why it does not."""
    if not isinstance(ref, str) or not ref:
        return "empty executor reference"
    if ref == "human":
        return ""
    m = re.fullmatch(r"(tool|bin|mcp|method):(.+)", ref)
    if not m:
        return f"{ref!r} is not tool:<id>, bin:<name>, mcp:<server/tool>, method:<atom id> or human"
    kind, val = m.groups()
    if kind == "tool":
        return "" if val in ctx.tools else f"tool '{val}' is not in {ctx.tools_file.name}"
    if kind == "bin":
        return "" if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,63}", val) else f"bad binary name '{val}'"
    if kind == "mcp":
        return "" if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}/[A-Za-z0-9_.-]{1,96}", val) else f"mcp ref must be mcp:<server>/<tool>, got '{val}'"
    return "" if val in ctx.catalog["atom_owner"] else f"atom '{val}' is not in {ctx.catalog_file.name}"


def normalize_ref(ctx, raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        raise FFError("EXECUTOR_UNKNOWN", "empty executor reference")
    if s != "human" and not re.fullmatch(r"(tool|bin|mcp|method):.+", s):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,63}", s):  # v1 compatibility: bare names
            raise FFError("EXECUTOR_UNKNOWN", f"{s!r} is not tool:<id>, bin:<name>, mcp:<server/tool>, method:<atom id> or human")
        s = f"tool:{s}" if s in ctx.tools else (f"tool:{s.replace('_', '-')}" if s.replace("_", "-") in ctx.tools else f"bin:{s}")
    why = ref_problem(ctx, s)
    if why:
        raise FFError("EXECUTOR_UNKNOWN", why)
    return s


def runnable_of(ctx, ref: str, tool_states=None) -> str:
    if ref == "human":
        return "human"
    kind, _, val = ref.partition(":")
    if kind == "tool":
        st = str((tool_states or {}).get(val) or "")
        return "ready" if st.startswith("ready") else ("missing" if st else "unknown")
    if kind == "bin":
        return "ready" if shutil.which(val) else "missing"
    return "method" if kind == "method" else "unknown"


def method_executor(ctx, caps) -> dict:
    """Default executor: the best-evidenced catalog method of the node's first known capability, else a human."""
    for c in caps:
        it = ctx.catalog["by_id"].get(c)
        atom = best_atom(it) if it else None
        if atom:
            return {"ref": f"method:{atom}", "runnable": "method", "source": "catalog_method"}
    return {"ref": "human", "runnable": "human", "source": "default"}


def best_atom(item: dict):
    atoms = [m for m in item.get("pipeline") or [] if isinstance(m, dict) and m.get("id")]
    if not atoms:
        return None
    rank = {s: i for i, s in enumerate(ATOM_RANK)}
    return min(enumerate(atoms), key=lambda x: (rank.get(x[1].get("status"), 99), x[0]))[1]["id"]


# ------------------------------------------------------------------ graph construction
def stage_io(stage: str, d: str) -> tuple:
    table = {
        "understand": (["brief"], ["spec"], "request card names every must-have, constraint and success measure"),
        "research": (["spec", "brief"], ["sources"], "every claim used later has a source and a licence note"),
        "plan": (["spec", "sources"], ["plan"], "each step names its input, output, executor and check"),
        "build": (["plan", "spec", "sources"], ["code"], "the code builds and its own tests pass"),
        "create": (["plan", "spec", "sources", "code"], [d], "the deliverable exists, opens and matches the spec"),
        "refine": ([d], [d], "a measured improvement over the previous version"),
        "assemble": ([d, "code"], [d], "every part is present in one deliverable"),
        "verify": ([d], ["evidence", d], "a QA report with measured checks and pass/fail is written"),
        "deliver": ([d, "evidence"], ["package"], "the user receives the deliverable with its QA receipt"),
    }
    ins, outs, check = table[stage]
    ins, outs = list(dict.fromkeys(ins)), list(dict.fromkeys(outs))
    return ([{"name": f"in_{k}", "kind": k} for k in ins],
            [{"name": f"out_{k}", "kind": k, "check": check} for k in outs], check)


def compatible(a: str, b: str) -> bool:
    return a == b or a == "any" or b == "any"


def pick_kind(src: dict, dst: dict) -> str:
    outs = [p.get("kind") for p in src.get("outputs") or []]
    ins = [p.get("kind") for p in dst.get("inputs") or []]
    for o in outs:
        for i in ins:
            if compatible(o, i):
                return i if o == "any" else o
    return outs[0] if outs else "any"


def edge_relation(dst: dict) -> str:
    return "verify" if dst.get("stage") == "verify" else "sequence"


def add_chain_edges(nodes: list, edges: list, order: list) -> None:
    """Join consecutive stage groups of a stage-ordered node list (nodes of one stage run in parallel)."""
    by = {n["id"]: n for n in nodes}
    groups = []
    for nid in order:
        if groups and groups[-1][0] == by[nid]["stage"]:
            groups[-1][1].append(nid)
        else:
            groups.append((by[nid]["stage"], [nid]))
    have = {(e["from"], e["to"]) for e in edges}
    for (_s1, g1), (_s2, g2) in zip(groups, groups[1:]):
        for a in g1:
            for b in g2:
                if (a, b) not in have:
                    edges.append({"id": "", "from": a, "to": b, "kind": pick_kind(by[a], by[b]), "relation": edge_relation(by[b])})
                    have.add((a, b))
    renumber_edges(edges)


def renumber_edges(edges: list) -> None:
    for i, e in enumerate(edges, 1):
        e["id"] = f"E{i:02d}"


def plan_order(r: dict, node_ids: list) -> list:
    pos = {s: i for i, s in enumerate(STAGES)}
    by = {n["id"]: n for n in r["nodes"]}
    idx = {n: i for i, n in enumerate(node_ids)}
    return sorted(dict.fromkeys(node_ids), key=lambda n: (pos.get(by.get(n, {}).get("stage"), 99), idx[n]))


def induced_edges(r: dict, node_ids) -> list:
    s = set(node_ids)
    return [e for e in edges_of(r) if e.get("from") in s and e.get("to") in s]


def build_graph(ctx, brief: dict, max_caps: int) -> tuple:
    """Nodes (one per plan stage, shared when identical), plans A/B/C and chain edges from the brief."""
    plans_in = brief.get("plans") if isinstance(brief.get("plans"), dict) else {}
    meta = {}
    for x in brief.get("shortlist") if isinstance(brief.get("shortlist"), list) else []:
        if isinstance(x, dict) and isinstance(x.get("id"), str):
            meta[x["id"]] = x
    for p in plans_in.values():
        for x in as_dict(p).get("superpowers") or []:
            if isinstance(x, dict) and isinstance(x.get("id"), str):
                meta.setdefault(x["id"], x)
    order = []
    for letter in "ABC":
        for st in STAGES:
            for c in as_dict(as_dict(plans_in.get(letter)).get("stages")).get(st) or []:
                if isinstance(c, str) and c not in order:
                    order.append(c)
    allowed = set(order[:max_caps])
    d = DELIVERABLE_KIND.get(str(as_dict(brief.get("analysis")).get("primary")), "any")
    nodes, key2id, plans, warnings, node_tools = [], {}, {}, [], collections.defaultdict(list)
    tool_states = {}
    for t in brief.get("tools") if isinstance(brief.get("tools"), list) else []:
        if isinstance(t, dict) and isinstance(t.get("id"), str):
            tool_states[t["id"]] = t.get("state")
    for letter in "ABC":
        p = plans_in.get(letter)
        if not isinstance(p, dict):
            continue
        stages = p.get("stages") if isinstance(p.get("stages"), dict) else {}
        for st in stages:
            if st not in STAGES:
                warnings.append(f"UNKNOWN_STAGE:{letter}:{st}")
        ids = []
        for st in STAGES:
            caps = list(dict.fromkeys(c for c in stages.get(st) or [] if isinstance(c, str) and c in allowed)) if isinstance(stages.get(st), list) else []
            if not caps:
                continue
            key = (st, tuple(sorted(caps)))
            if key not in key2id:
                ins, outs, check = stage_io(st, d)
                nid = f"N{len(nodes) + 1:02d}"
                key2id[key] = nid
                nodes.append({"id": nid, "stage": st, "capability_ids": caps,
                              "label": clip(f"{st}: " + ", ".join(str(meta.get(c, {}).get("name_en") or cap_entry(ctx, c)["name_en"] or c) for c in caps), 100),
                              "inputs": ins, "outputs": outs, "acceptance": check, "contract_source": "default_unconfirmed",
                              "owner": "claude", "permission": "local-files", "rollback": "discard this stage's output and rerun it",
                              "optional": False, "status": "pending", "last_trace": None})
            ids.append(key2id[key])
        if not ids:
            continue
        if not any(n["stage"] == "verify" for n in nodes if n["id"] in ids):
            key = ("verify", ())
            if key not in key2id:
                ins, outs, check = stage_io("verify", d)
                key2id[key] = f"N{len(nodes) + 1:02d}"
                nodes.append({"id": key2id[key], "stage": "verify", "capability_ids": [], "label": "verify: manual QA (the brief named no verifier)",
                              "inputs": ins, "outputs": outs, "acceptance": check, "contract_source": "default_unconfirmed",
                              "owner": "claude", "permission": "local-files", "rollback": "discard the QA report and rerun it",
                              "optional": False, "status": "pending", "last_trace": None})
            ids.append(key2id[key])
            warnings.append(f"NO_BRIEF_VERIFIER:{letter}")
        for t in p.get("tools") if isinstance(p.get("tools"), list) else []:
            if isinstance(t, dict) and isinstance(t.get("id"), str):
                tool_states.setdefault(t["id"], t.get("state"))
                for nid in ids:
                    if t not in node_tools[nid]:
                        node_tools[nid].append(t)
        plans[letter] = {"name": letter, "label": PLAN_LABELS[letter], "idea": str(p.get("idea") or p.get("name") or ""),
                         "nodes": ids, "tools": [{"id": t["id"], "state": t.get("state")} for t in (p.get("tools") if isinstance(p.get("tools"), list) else [])
                                                 if isinstance(t, dict) and isinstance(t.get("id"), str)]}
    r = {"nodes": nodes, "edges": []}
    for letter, p in plans.items():
        p["nodes"] = plan_order(r, p["nodes"])
        add_chain_edges(nodes, r["edges"], p["nodes"])
    for n in nodes:
        fams = set()
        for c in n["capability_ids"]:
            it = ctx.catalog["by_id"].get(c) or {}
            fams |= strset(it.get("families"))
            fams |= strset(as_dict(meta.get(c)).get("families"))
        n["executor"] = {"ref": "human", "runnable": "human", "source": "default"}
        for t in node_tools.get(n["id"], []):
            tf = strset(t.get("families")) | strset(as_dict(ctx.tools.get(t["id"])).get("families"))
            if t["id"] in ctx.tools and tool_fits(n["stage"], t["id"], tf, fams):
                n["executor"] = {"ref": f"tool:{t['id']}", "runnable": runnable_of(ctx, f"tool:{t['id']}", tool_states), "source": "brief_tool_family_match"}
                break
        else:
            n["executor"] = method_executor(ctx, n["capability_ids"])
    caps = {c: cap_entry(ctx, c, meta.get(c)) for n in nodes for c in n["capability_ids"]}
    for c in sorted(caps):
        if not caps[c]["known"]:
            warnings.append(f"UNKNOWN_CAPABILITY:{c}")
    return nodes, r["edges"], plans, caps, tool_states, warnings, d


def tool_fits(stage: str, tid: str, tool_fams: set, node_fams: set) -> bool:
    """Draft binding only: QA tools go to verify nodes; understand/plan nodes need >=2 shared families; other nodes
    need >=2 shared families (1 for narrow tools)."""
    shared = tool_fams & node_fams
    if stage == "verify":
        return bool(QA_TOOL_RX.search(tid)) and bool(shared)
    if QA_TOOL_RX.search(tid):
        return False
    if stage in ("understand", "plan"):
        return len(shared) >= 2
    return len(shared) >= 2 or (len(shared) == 1 and len(tool_fams) <= 2)


def similar_unverified(ctx, caps: dict) -> list:
    best = {}
    for c in sorted(caps):
        for link in (ctx.catalog["by_id"].get(c) or {}).get("links") or []:
            to = link.get("id") if isinstance(link, dict) else None
            if not to or to in caps or to not in ctx.catalog["by_id"]:
                continue
            try:
                sim = round(float(link.get("sim", 0)), 3)
            except (TypeError, ValueError):
                continue
            if to not in best or sim > best[to]["sim"]:
                best[to] = {"from": c, "to": to, "sim": sim, "name_en": ctx.catalog["by_id"][to].get("name_en", ""),
                            "relation": "similar_unverified"}
    return sorted(best.values(), key=lambda x: (-x["sim"], x["to"]))[:12]


# ------------------------------------------------------------------ validate (V01–V12)
def issue(name: str, message: str, where: str = "", level: str = "error") -> dict:
    return {"code": CODES.get(name, name), "name": name, "level": level, "message": message, "where": where}


def validate_recipe(ctx, space: Path, r: dict, extra_plans=None) -> dict:
    errs, warns, notes = [], [], []
    E = lambda name, msg, where="": errs.append(issue(name, msg, where))  # noqa: E731
    W = lambda name, msg, where="": warns.append(issue(name, msg, where, "warning"))  # noqa: E731
    if not isinstance(r, dict):
        E("SCHEMA", "a recipe must be a JSON object")
        return {"errors": errs, "warnings": warns, "notes": notes}
    legacy = bool(r.get("migrated_from"))
    # V01 schema and graph structure
    req = {"schema": str, "id": str, "project": str, "goal": str, "status": str, "status_log": list, "nodes": list,
           "edges": list, "plans": dict, "capabilities": dict, "traces": list, "evidence": list}
    for k, t in req.items():
        if not isinstance(r.get(k), t):
            E("SCHEMA", f"'{k}' must be {t.__name__}", k)
    if errs:
        return {"errors": errs, "warnings": warns, "notes": notes}
    if r["schema"] != SCHEMA:
        E("SCHEMA", f"schema must be {SCHEMA}", "schema")
    if not ID_RX.fullmatch(r["id"]):
        E("SCHEMA", "bad recipe id", "id")
    if r["status"] not in STATUSES:
        E("SCHEMA", f"status {r['status']!r} is not one of {', '.join(STATUSES)}", "status")
    nodes, ids = {}, []
    for i, n in enumerate(r["nodes"]):
        w = f"nodes[{i}]"
        if not isinstance(n, dict) or not isinstance(n.get("id"), str) or not NODE_RX.fullmatch(n["id"]):
            E("SCHEMA", "node needs an id like N01", w)
            continue
        if n["id"] in nodes:
            E("SCHEMA", f"duplicate node id {n['id']}", w)
        nodes[n["id"]] = n
        ids.append(n["id"])
        if n.get("stage") not in STAGES:
            E("SCHEMA", f"stage {n.get('stage')!r} is not one of {', '.join(STAGES)}", n["id"])
        if n.get("status") not in NODE_STATUSES:
            E("SCHEMA", f"node status {n.get('status')!r} is not one of {', '.join(NODE_STATUSES)}", n["id"])
        if not isinstance(n.get("capability_ids"), list) or not all(isinstance(c, str) for c in n["capability_ids"]):
            E("SCHEMA", "capability_ids must be a list of ids", n["id"])
        for side in ("inputs", "outputs"):
            ports = n.get(side)
            if not isinstance(ports, list) or (side == "outputs" and not ports):
                E("SCHEMA", f"{side} must be a{' non-empty' if side == 'outputs' else ''} list of {{name, kind}}", n["id"])
                continue
            for p in ports:
                if not isinstance(p, dict) or p.get("kind") not in KINDS or not isinstance(p.get("name"), str):
                    E("SCHEMA", f"{side} port {p!r} needs a name and a kind from {', '.join(KINDS)}", n["id"])
        if not isinstance(n.get("executor"), dict) or not isinstance(n["executor"].get("ref"), str):
            E("SCHEMA", "executor must be {ref, runnable}", n["id"])
    edge_ids = set()
    for i, e in enumerate(r["edges"]):
        w = f"edges[{i}]"
        if not isinstance(e, dict) or not all(isinstance(e.get(k), str) for k in ("id", "from", "to")):
            E("SCHEMA", "edge must be an object with string id, from and to", w)
            continue
        if e.get("id") in edge_ids:
            E("SCHEMA", f"duplicate edge id {e.get('id')}", w)
        edge_ids.add(e.get("id"))
        if e.get("from") not in nodes or e.get("to") not in nodes or e.get("from") == e.get("to"):
            E("SCHEMA", f"edge {e.get('from')}->{e.get('to')} must join two different existing nodes", w)
        if e.get("kind") not in KINDS:
            E("SCHEMA", f"edge kind {e.get('kind')!r} is not one of {', '.join(KINDS)}", w)
        if e.get("relation") not in RELATIONS:
            E("SCHEMA", f"edge relation {e.get('relation')!r} is not one of {', '.join(RELATIONS)}", w)
    # cycles (refine edges may loop back)
    succ = collections.defaultdict(set)
    indeg = {n: 0 for n in nodes}
    for e in r["edges"]:
        if e in edges_of(r) and e.get("relation") != "refine" and e.get("from") in nodes and e.get("to") in nodes and e["to"] not in succ[e["from"]]:
            succ[e["from"]].add(e["to"])
            indeg[e["to"]] += 1
    queue, seen = [n for n, k in indeg.items() if k == 0], 0
    while queue:
        cur = queue.pop()
        seen += 1
        for nx in succ[cur]:
            indeg[nx] -= 1
            if indeg[nx] == 0:
                queue.append(nx)
    if seen != len(nodes):
        E("SCHEMA", "the graph has a cycle outside refine edges", "edges")
    plans = dict(r["plans"])
    plans.update(extra_plans or {})
    for letter, p in sorted(plans.items()):
        if letter not in PLAN_LETTERS or not isinstance(p, dict) or not isinstance(p.get("nodes"), list) or not p["nodes"]:
            E("SCHEMA", "plans are A/B/C/D objects with a non-empty node list", f"plans.{letter}")
            continue
        missing = [n for n in p["nodes"] if not isinstance(n, str) or n not in nodes]
        if missing:
            E("SCHEMA", f"plan {letter} names unknown nodes {', '.join(map(str, missing))}", f"plans.{letter}")
    pc = r.get("plan_choice")
    if pc is not None:
        if not isinstance(pc, dict) or pc.get("plan") not in PLAN_LETTERS or not isinstance(pc.get("nodes"), list):
            E("SCHEMA", "plan_choice must be {plan, why, nodes, at}", "plan_choice")
        elif [n for n in pc["nodes"] if not isinstance(n, str) or n not in nodes]:
            E("SCHEMA", "plan_choice names unknown nodes", "plan_choice")
        elif pc["plan"] not in plans:
            plans[pc["plan"]] = {"nodes": pc["nodes"]}
    # V02 status log replay
    log, prev, broken = r["status_log"], None, False
    for i, s in enumerate(log):
        if not isinstance(s, dict):
            E("STATE_LOG_INVALID", "status_log entries must be objects", f"status_log[{i}]")
            broken = True
            break
        if s.get("from") != prev or (prev is None and s.get("to") != "candidate") or (prev is not None and s.get("to") not in TRANSITIONS.get(prev, ())):
            E("STATE_LOG_INVALID", f"illegal step {s.get('from')} -> {s.get('to')} after {prev}", f"status_log[{i}]")
            broken = True
            break
        if s.get("to") in ("tested", "verified", "failed") and not s.get("evidence_sha256") and s.get("cmd") != "migrate":
            E("STATE_LOG_INVALID", f"{s.get('to')} was recorded without evidence", f"status_log[{i}]")
        prev = s.get("to")
    if not log:
        E("STATE_LOG_INVALID", "status_log is empty", "status_log")
    elif prev != r["status"] and not broken:
        E("STATE_LOG_INVALID", f"status is {r['status']} but the log ends at {prev}", "status")
    # V08 secrets anywhere in the record (keys, values and "key": "value" pairs)
    for path, kinds in scan_object(r):
        E("SECRET", f"looks like a credential ({', '.join(kinds)})", path)
    bad = malformed(r)
    if bad:
        E("SCHEMA", f"malformed {', '.join(bad[:6])}: fix the types first (V03-V07 and V09-V12 were skipped)", bad[0])
        return {"errors": errs, "warnings": warns, "notes": notes}
    # V03 handoff kinds
    for e in edges_of(r):
        a, b = nodes.get(e.get("from")), nodes.get(e.get("to"))
        if not a or not b or e.get("kind") not in KINDS:
            continue
        outs = [p.get("kind") for p in a.get("outputs") or [] if isinstance(p, dict)]
        ins = [p.get("kind") for p in b.get("inputs") or [] if isinstance(p, dict)]
        if not any(compatible(e["kind"], o) for o in outs) or not any(compatible(e["kind"], i) for i in ins):
            E("HANDOFF_KIND_MISMATCH", f"{a['id']} outputs {outs} and {b['id']} accepts {ins}; edge carries '{e['kind']}'", e.get("id", ""))
    # V04 every plan ends in verification; isolated plan nodes
    for letter, p in sorted(plans.items()):
        pn = [n for n in as_dict(p).get("nodes") or [] if isinstance(n, str) and n in nodes]
        if not pn:
            continue
        sub = induced_edges(r, pn)
        if len(pn) > 1:
            touched = {e["from"] for e in sub} | {e["to"] for e in sub}
            lonely = [n for n in pn if n not in touched]
            if lonely:
                E("SCHEMA", f"plan {letter} has nodes with no handoff edge: {', '.join(lonely)}", f"plans.{letter}")
        verify = {n for n in pn if nodes[n].get("stage") == "verify"}
        outgoing = {e["from"] for e in sub}
        sinks = [n for n in pn if n not in outgoing]
        ok = bool(verify) and all(n in verify or (nodes[n].get("stage") == "deliver" and any(e["to"] == n and e["from"] in verify for e in sub)) for n in sinks)
        if not ok:
            E("NO_FINAL_VERIFY", f"plan {letter} must end in a verify node (or a deliver node fed by one)", f"plans.{letter}")
    # V05 executors
    for nid in ids:
        ref = (nodes[nid].get("executor") or {}).get("ref")
        why = ref_problem(ctx, ref)
        if why:
            E("EXECUTOR_UNKNOWN", why, nid)
    # V06/V07/V09 evidence
    for where, rec, _f in evidence_records(r):
        if not SHA_RX.fullmatch(str(rec.get("sha256", ""))):
            E("SCHEMA", "evidence needs a sha256", where)
            continue
        if rec.get("stored") and not STORED_RX.fullmatch(str(rec["stored"])):
            E("SCHEMA", "evidence 'stored' must be evidence/<sha256><suffix>", where)
        src = rec.get("source")
        if isinstance(src, str) and (src.startswith(("/", "~", "\\")) or re.match(r"[A-Za-z]:[\\/]", src) or ".." in Path(src).parts):
            E("SCHEMA", "evidence source must be a relative path", where)
        rr = rec.get("root_rel")
        if isinstance(rr, str) and (rr.startswith(("/", "~", "\\")) or re.match(r"[A-Za-z]:[\\/]", rr)):
            E("SCHEMA", "evidence root_rel must be relative to the FusionForge root", where)
        base = ctx.base_path(rec.get("source_base"))
        if base is not None and isinstance(src, str) and src:
            with contextlib.suppress(ValueError, OSError, RuntimeError):
                parts = (base / src).resolve().relative_to(ctx.root).parts
                if (len(parts) >= 2 and parts[1] in FORBIDDEN_EVIDENCE) or (len(parts) == 2 and parts[1] in FORBIDDEN_EVIDENCE_FILES):
                    E("SELF_EVIDENCE", "evidence points at a FusionForge record", where)
        state, _p = evidence_location(ctx, space, rec)
        if state == "mismatch":
            E("EVIDENCE_HASH_MISMATCH", f"stored evidence {rec['sha256'][:12]}… no longer matches its hash", where)
        elif state == "missing":
            if rec.get("imported") or rec.get("legacy") or (r.get("imported") and not r.get("import_receipt")):
                W("EVIDENCE_NOT_LOCAL", f"evidence {rec['sha256'][:12]}… is not on this machine", where)
            else:
                E("EVIDENCE_MISSING", f"evidence {rec['sha256'][:12]}… is missing", where)
    # V10 verified must rest on a run
    if r["status"] == "verified":
        chosen = {n for n in as_dict(pc).get("nodes") or [] if isinstance(n, str)}
        ran = [t for t in r["traces"] if isinstance(t, dict) and t.get("result") == "passed" and t.get("evidence")
               and nodes.get(t.get("node"), {}).get("stage") == "verify" and (not chosen or t.get("node") in chosen)]
        if not ran:
            (W if legacy else E)("VERIFIED_WITHOUT_RUN", "verified without a passed verify-node trace with evidence"
                                 + (" (legacy v1 recipe)" if legacy else ""), "status")
    # V11/V12 catalog drift and unknown capabilities
    used = sorted({c for n in nodes.values() for c in n.get("capability_ids") or [] if isinstance(c, str)})
    for c in used:
        fp = r["capabilities"].get(c)
        if not isinstance(fp, dict) or not fp.get("known"):  # noqa: SIM102
            W("UNKNOWN_CAPABILITY", f"{c} is not a catalog superpower (or was unknown when recorded)", c)
    dr = drift(ctx, r)
    for old, new in sorted(dr["remapped"].items()):
        W("CATALOG_DRIFT", f"{old} now lives at {new} (same atoms)", old)
    for c in dr["stale"]:
        W("CATALOG_DRIFT", f"{c} no longer matches any catalog superpower by its atoms", c)
    defaults = [n for n in ids if nodes[n].get("contract_source") == "default_unconfirmed"]
    if defaults:
        notes.append(f"{len(defaults)} node(s) still carry default_unconfirmed contracts: refine with set-graph")
    return {"errors": errs, "warnings": warns, "notes": notes, "drift": dr}


# ------------------------------------------------------------------ lessons and reuse
def lesson(rid, typ, node, stage, **fields) -> dict:
    key = json.dumps([rid, typ, node, fields.get("key")], ensure_ascii=False, sort_keys=True)
    d = {"id": "LSN-" + sha256_text(key)[:10], "type": typ, "recipe": rid, "node": node, "stage": stage}
    d.update({k: v for k, v in fields.items() if k != "key"})
    return d


def trace_executor(t: dict, planned):
    """(executor, reported): the tool the caller named with --tool, else the node's planned executor (assumed)."""
    tool = t.get("tool") if isinstance(t.get("tool"), str) and t.get("tool") != "not_reported" else None
    reported = t.get("tool_reported")
    if not isinstance(reported, bool):  # traces written before tool_reported: a tool equal to the plan is assumed
        reported = bool(tool) and tool != planned
    return (tool if reported and tool else planned or tool), bool(reported and tool)


def extract_lessons(r: dict) -> list:
    """Pure and idempotent: WORKED, FAILED, REPLACED, HANDOFF and RECIPE_FAILED lessons from traces and the log.
    'capabilities' holds only what a trace reported; 'node_capabilities' is the node's planned list (context, not proof);
    'assumed_executor' marks lessons whose executor is the planned one because the trace named no --tool."""
    rid, out = r.get("id"), []
    nodes = {n.get("id"): n for n in r.get("nodes") or [] if isinstance(n, dict) and isinstance(n.get("id"), str)}
    per = collections.defaultdict(list)
    for t in r.get("traces") or []:
        if isinstance(t, dict) and isinstance(t.get("node"), str) and t.get("result") in RESULTS and isinstance(t.get("seq"), int):
            per[t["node"]].append(t)
    used_by = {}
    for nid in sorted(per):
        ts = sorted(per[nid], key=lambda t: t["seq"])
        n = nodes.get(nid, {})
        stage = n.get("stage") or ts[-1].get("stage")
        planned = as_dict(n.get("executor")).get("ref")
        ncaps = sorted(c for c in n.get("capability_ids") or [] if isinstance(c, str))
        for t in ts:
            if t["result"] == "failed":
                ex, rep = trace_executor(t, planned)
                out.append(lesson(rid, "FAILED", nid, stage, key=t.get("seq"), executor=ex, assumed_executor=not rep,
                                  error_class=t.get("error_class") or "unspecified", observed=clip(t.get("observed"), 200),
                                  evidence_sha256=as_dict(t.get("evidence")).get("sha256"), node_capabilities=ncaps))
        last = ts[-1]
        if last["result"] == "passed":
            used, rep = trace_executor(last, planned)
            used_by[nid] = used
            out.append(lesson(rid, "WORKED", nid, stage, key=used, executor=used, assumed_executor=not rep,
                              with_evidence=bool(last.get("evidence")),
                              capabilities=sorted(c for c in last.get("capabilities") or [] if isinstance(c, str)), node_capabilities=ncaps,
                              inputs=[p.get("kind") for p in n.get("inputs") or [] if isinstance(p, dict)],
                              outputs=[p.get("kind") for p in n.get("outputs") or [] if isinstance(p, dict)]))
            for bad in dict.fromkeys(trace_executor(t, planned)[0] for t in ts if t["result"] == "failed"):
                if bad and bad != used:
                    out.append(lesson(rid, "REPLACED", nid, stage, key=f"{bad}->{used}", executor=bad, replaced_by=used, node_capabilities=ncaps))
    for e in edges_of(r):
        a, b = nodes.get(e.get("from"), {}), nodes.get(e.get("to"), {})
        if a.get("status") == "passed" and b.get("status") == "passed":
            out.append(lesson(rid, "HANDOFF", e.get("to"), b.get("stage"), key=e.get("id"), outcome="worked", edge=e.get("id"),
                              kind=e.get("kind"), from_stage=a.get("stage"),
                              from_executor=used_by.get(e.get("from")) or as_dict(a.get("executor")).get("ref"),
                              to_executor=used_by.get(e.get("to")) or as_dict(b.get("executor")).get("ref")))
        bad = [t for t in per.get(e.get("to"), []) if t["result"] == "failed" and t.get("error_class") == "wrong_input_kind"]
        if bad and a:
            out.append(lesson(rid, "HANDOFF", e.get("to"), b.get("stage"), key=f"{e.get('id')}:mismatch", outcome="mismatch",
                              edge=e.get("id"), kind=e.get("kind"), from_stage=a.get("stage"), observed=clip(bad[-1].get("observed"), 200)))
    for i, s in enumerate(r.get("status_log") or []):
        if isinstance(s, dict) and s.get("to") == "failed":  # recipe-level failure with its note
            out.append(lesson(rid, "RECIPE_FAILED", None, None, key=i, note=clip(s.get("note"), 300), at=s.get("at")))
    return sorted(out, key=lambda x: (x["type"], str(x["node"]), x["id"]))


def goal_set(ctx, text: str) -> set:
    return set(si().expand(text or "", ctx.vocab))


def recipe_strength(r: dict) -> float:
    chosen = [n for n in as_dict(r.get("plan_choice")).get("nodes") or [] if isinstance(n, str)]
    nodes = {n.get("id"): n for n in r.get("nodes") or [] if isinstance(n, dict)}
    passed = sum(1 for t in r.get("traces") or [] if isinstance(t, dict) and t.get("result") == "passed")
    if r.get("status") == "verified" and r.get("legacy_unproven"):
        s = 0.3                     # v1 verified with no trace: weight x0.3
    elif r.get("status") == "verified" and r.get("migrated_from"):
        s = 0.5                     # v1 verified with v1 traces (no per-node results)
    elif r.get("status") == "verified":
        s = min(1.0, 0.8 + 0.1 * passed)
    elif r.get("status") == "tested":
        all_ok = bool(chosen) and all(nodes.get(n, {}).get("status") in ("passed", "skipped") for n in chosen)
        s = (0.4 if all_ok else 0.2) * min(1.0, 0.8 + 0.1 * passed)
    else:
        return 0.0
    return round(s * (0.8 if r.get("imported") else 1.0), 4)


def recency(ctx, r: dict) -> float:
    stamps = [parse_iso(s.get("at")) for s in r.get("status_log") or [] if isinstance(s, dict) and isinstance(s.get("at"), str)]
    stamps = [s for s in stamps if s]
    if not stamps:
        return 0.25
    age = max(0.0, (ctx.now - max(stamps)).total_seconds() / 86400)
    return round(max(0.25, 0.5 ** (age / 90)), 4)


def validate_errors(ctx, space: Path, r: dict, cache=None) -> list:
    """Names of validate errors for a prior recipe (memoised per command run)."""
    if cache is not None and r.get("id") in cache:
        return cache[r["id"]]
    names = sorted({e["name"] for e in validate_recipe(ctx, space, r)["errors"]})
    if cache is not None:
        cache[r.get("id")] = names
    return names


def rank_prior(ctx, space: Path, goal: str, cap_ids=(), exclude=(), vcache=None) -> dict:
    """Same-project ranking: score = sim x strength x recency x freshness; failed recipes go to avoid.
    With brief capabilities sim = 0.5 goal + 0.5 capability overlap and a recipe sharing no capability is not similar;
    without them sim is goal text only (sim_basis says which)."""
    good, legacy, invalid = list_recipes(space)
    gq = goal_set(ctx, goal)
    matches, avoid, considered = [], [], 0
    for r in good:
        if r["id"] in exclude:
            continue
        considered += 1
        dr = drift(ctx, r)
        sim_goal = jaccard(gq, goal_set(ctx, r.get("goal", "")))
        caps_now = current_caps(dr)
        if cap_ids and caps_now:
            cap_j = jaccard(cap_ids, caps_now)
            if cap_j == 0:
                continue
            sim, basis = round(SIM_W_GOAL * sim_goal + SIM_W_CAPS * cap_j, 4), "goal+capabilities"
        else:
            sim, basis = round(sim_goal, 4), "goal_text_only"
        if sim < (SIM_MIN_BLEND if basis == "goal+capabilities" else SIM_MIN):
            continue
        if r["status"] == "failed":
            avoid.append({"id": r["id"], "goal": clip(r.get("goal"), 100), "sim": sim, "sim_basis": basis,
                          "lessons": [{"type": l["type"], "node": l["node"], "executor": l.get("executor"),
                                       "error_class": l.get("error_class"), "note": l.get("note") or l.get("observed")}
                                      for l in extract_lessons(r) if l["type"] in ("FAILED", "RECIPE_FAILED", "REPLACED")]})
            continue
        if r["status"] not in ("verified", "tested"):
            continue
        errors = validate_errors(ctx, space, r, vcache)
        fresh = 0.0 if errors else (0.5 if dr["stale"] or dr["unknown"] else (0.75 if dr["remapped"] else 1.0))
        strength, rec = recipe_strength(r), recency(ctx, r)
        matches.append({"id": r["id"], "status": r["status"], "goal": clip(r.get("goal"), 100),
                        "score": round(sim * strength * rec * fresh, 4), "sim_basis": basis,
                        "factors": {"sim": sim, "strength": strength, "recency": rec, "freshness": fresh},
                        "plan": as_dict(r.get("plan_choice")).get("plan"), "imported": bool(r.get("imported")),
                        "legacy_unproven": bool(r.get("legacy_unproven")),
                        "reusable": r["status"] == "verified" and not errors,
                        "drift": {"remapped": dr["remapped"], "stale": dr["stale"]},
                        "validate_errors": errors})
    matches.sort(key=lambda m: (-m["score"], m["id"]))
    avoid.sort(key=lambda m: (-m["sim"], m["id"]))
    return {"matches": matches, "avoid": avoid, "considered": considered, "legacy_v1": [r.get("id") for r in legacy], "invalid_files": invalid}


def annotate_memory(ctx, nodes: list, priors: list) -> int:
    """Attach same-project evidence of what worked or failed to each node; never swaps anything.
    Exact memory is keyed on (stage, executor); stage memory lists other executors that worked, failed or replaced one
    another in the same stage on overlapping capabilities (after drift mapping), so a paraphrased goal still sees them.
    proven_capabilities come only from capabilities a passed trace reported with evidence."""
    exact = collections.defaultdict(lambda: {"worked": set(), "ran": set(), "failed": [], "repl": collections.Counter()})
    stage_mem, proven = collections.defaultdict(list), collections.defaultdict(set)
    for p in priors:
        dr = drift(ctx, p)
        cmap = {**dr["current"], **dr["remapped"]}
        for l in extract_lessons(p):
            st, ex = l.get("stage"), l.get("executor")
            caps = {cmap[c] for c in l.get("node_capabilities") or [] if c in cmap}
            e = exact[(st, ex)]
            if l["type"] == "WORKED":
                (e["ran"] if l.get("assumed_executor") else e["worked"]).add(p["id"])
                if l.get("with_evidence"):
                    proven[st] |= {cmap[c] for c in l.get("capabilities") or [] if c in cmap}
                if not l.get("assumed_executor"):
                    stage_mem[st].append(("worked", ex, caps, None))
            elif l["type"] == "FAILED":
                e["failed"].append((p["id"], l.get("error_class")))
                stage_mem[st].append(("failed", ex, caps, None))
            elif l["type"] == "REPLACED":
                e["repl"][l.get("replaced_by")] += 1
                stage_mem[st].append(("replaced", ex, caps, l.get("replaced_by")))
    touched = 0
    for n in nodes:
        ref, mine = n["executor"]["ref"], set(n["capability_ids"])
        e = exact.get((n["stage"], ref))
        mem = {}
        if e and e["worked"]:
            mem["worked_in"] = sorted(e["worked"])
        if e and e["ran"]:
            mem["ran_in"] = sorted(e["ran"])
        if e and e["failed"]:
            mem["failed_in"] = sorted({rid for rid, _ in e["failed"]})
            mem["error_classes"] = sorted({c for _, c in e["failed"] if c})
        if e and e["repl"]:
            mem["replacement_hint"] = sorted(e["repl"].items(), key=lambda kv: (-kv[1], str(kv[0])))[0][0]
        pc = sorted(mine & proven.get(n["stage"], set()))
        if pc:
            mem["proven_capabilities"] = pc
        sw, sf, sr = set(), set(), set()
        for typ, ex, caps, to in stage_mem.get(n["stage"], []):
            if not (caps & mine) or (ex == ref and typ != "replaced"):
                continue
            if typ == "worked":
                sw.add(ex)
            elif typ == "failed":
                sf.add(ex)
            elif ex != ref:
                sr.add(f"{ex} -> {to}")
        if sw:
            mem["stage_worked"] = sorted(map(str, sw))
        if sf:
            mem["stage_failed"] = sorted(map(str, sf))
        if sr:
            mem["stage_replacements"] = sorted(sr)
        if mem:
            n["memory"] = mem
            touched += 1
    return touched


def template_executors(r: dict) -> dict:
    """Stage -> executors that actually ran the template's chosen plan (planned ones when no trace named a tool)."""
    chosen = set(as_dict(r.get("plan_choice")).get("nodes") or [])
    used = {l["node"]: l.get("executor") for l in extract_lessons(r) if l["type"] == "WORKED"}
    out = collections.defaultdict(set)
    for n in r.get("nodes") or []:
        if n["id"] in chosen:
            out[n["stage"]].add(used.get(n["id"]) or n["executor"]["ref"])
    return {st: sorted(map(str, out[st])) for st in STAGES if st in out}


# ------------------------------------------------------------------ commands
def load_brief(ctx, a, goal: str) -> tuple:
    if a.from_brief:
        p = Path(a.from_brief).expanduser()
        try:
            raw = p.read_bytes()
            brief = json.loads(raw.decode("utf-8-sig"))
        except (OSError, ValueError) as exc:
            raise FFError("BRIEF_UNREADABLE", f"{p.name}: {type(exc).__name__}") from None
        source = "file"
    else:
        try:
            brief = si().build_brief(goal, terms=a.terms or "")
        except FFError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise FFError("BRIEF_FAILED", f"skill_intelligence.build_brief failed ({type(exc).__name__}: {clip(exc, 160)}); "
                                          "pass --from-brief out/<job>/brief.json") from None
        if ctx.fixed_now and isinstance(brief, dict):  # wall-clock fields: replays with --now must be byte-identical
            brief["elapsed_s"] = None
            if isinstance(brief.get("coverage"), dict):
                brief["coverage"]["scanned_at"] = ctx.now_s
        raw = dump(brief).encode("utf-8")
        source = "in_process"
    if not isinstance(brief, dict) or not str(brief.get("schema", "")).startswith("kosif.skill-intelligence"):
        raise FFError("BRIEF_SCHEMA", "the brief must be a skill_intelligence brief (schema kosif.skill-intelligence.*)")
    if as_dict(brief.get("coverage")).get("complete") is not True:
        raise FFError("BRIEF_INCOMPLETE", "the brief's coverage receipt is not complete (coverage.complete must be true); fix the catalog first")
    hits = scan_object(brief)
    if hits:
        raise FFError("SECRET", f"the brief contains something that looks like a credential ({', '.join(hits[0][1])}) at {hits[0][0]}")
    return brief, raw, source


def _name_key(s) -> str:
    return " ".join(str(s or "").lower().split())


def reconcile_brief(ctx, brief: dict) -> tuple:
    """SP ids are positional: check every id the brief names against the current catalog by its name_en. A renamed
    position is remapped when exactly one catalog item has the brief's name; otherwise BRIEF_CATALOG_MISMATCH."""
    names = {}
    pools = [brief.get("shortlist")] + [as_dict(p).get("superpowers") for p in as_dict(brief.get("plans")).values()]
    for pool in pools:
        for x in pool if isinstance(pool, list) else []:
            if isinstance(x, dict) and isinstance(x.get("id"), str) and isinstance(x.get("name_en"), str) and x["name_en"].strip():
                names.setdefault(x["id"], x["name_en"])
    by_name = collections.defaultdict(list)
    for cid, it in ctx.catalog["by_id"].items():
        by_name[_name_key(it.get("name_en"))].append(cid)
    mapping, bad = {}, []
    for cid, nm in sorted(names.items()):
        cur = ctx.catalog["by_id"].get(cid)
        if cur and _name_key(cur.get("name_en")) == _name_key(nm):
            continue
        cands = by_name.get(_name_key(nm), [])
        if len(cands) == 1:
            mapping[cid] = cands[0]
        elif cur:
            bad.append(cid)
    if bad:
        raise FFError("BRIEF_CATALOG_MISMATCH", f"the brief's ids {', '.join(bad[:5])}{' …' if len(bad) > 5 else ''} now name other "
                                                "superpowers in the catalog (it was rebuilt); make a fresh brief with skill_intelligence.py "
                                                "or pass the brief's own catalog with --catalog-file")
    if not mapping:
        return brief, []
    b = json.loads(json.dumps(brief))
    for p in as_dict(b.get("plans")).values():
        st = as_dict(as_dict(p).get("stages"))
        for k, ids in st.items():
            if isinstance(ids, list):
                st[k] = [mapping.get(c, c) if isinstance(c, str) else c for c in ids]
        for x in as_dict(p).get("superpowers") or []:
            if isinstance(x, dict) and x.get("id") in mapping:
                x["id"] = mapping[x["id"]]
    for x in b.get("shortlist") or []:
        if isinstance(x, dict) and x.get("id") in mapping:
            x["id"] = mapping[x["id"]]
    return b, [f"BRIEF_ID_REMAPPED:{k}->{v}" for k, v in sorted(mapping.items())]


def cmd_propose(ctx, a) -> dict:
    goal = (a.goal or "").strip()
    if not goal:
        raise FFError("USAGE", "goal is empty")
    if not 1 <= a.max_capabilities <= 60:
        raise FFError("USAGE", "--max-capabilities must be 1..60")
    refuse(goal=goal, terms=a.terms or "")
    space = space_of(ctx, a.project)
    if a.id and not ID_RX.fullmatch(a.id):
        raise FFError("BAD_ID", "--id must look like FUSE-YYYYMMDD-<10 hex>")
    brief, raw, source = load_brief(ctx, a, goal)
    an = as_dict(brief.get("analysis"))
    graph_brief, remapped = reconcile_brief(ctx, brief)
    nodes, edges, plans, caps, tool_states, warnings, deliv = build_graph(ctx, graph_brief, a.max_capabilities)
    warnings += remapped
    substantive = [n for n in nodes if n["stage"] not in ("verify", "deliver") and n["capability_ids"]]
    if not plans or not substantive or brief.get("shortlist") == []:
        raise FFError("NO_MATCH", f"the brief matched no catalog capability beyond generic checks for this goal (level {an.get('level', '?')}); "
                                  "retry with --terms \"english keywords\" or answer directly without a recipe", rc=3)
    if a.from_brief and str(an.get("request", "")).strip() and str(an.get("request")).strip() != goal:
        warnings.append("BRIEF_GOAL_DIFFERS")
    with locked(space):
        rid = new_id(ctx, space, f"propose|{a.project}|{goal}", a.id)
        good, _legacy, _invalid = list_recipes(space)
        vcache = {}
        all_caps = sorted(caps)
        recall = rank_prior(ctx, space, goal, all_caps, vcache=vcache)
        clean = [p for p in good if not validate_errors(ctx, space, p, vcache)]
        touched = annotate_memory(ctx, nodes, clean)
        if not good:
            warnings.append("LEARNING_INDEX_EMPTY")
        elif len(clean) < len(good):
            warnings.append(f"MEMORY_SKIPPED_INVALID_PRIORS:{len(good) - len(clean)}")
        tpl = next((m["id"] for m in recall["matches"] if m["score"] >= TEMPLATE_MIN), None)
        tpl_rec = next((p for p in clean if p["id"] == tpl), None)
        rec = brief.get("recommended") if isinstance(brief.get("recommended"), str) else None
        r = {"schema": SCHEMA, "engine": ENGINE, "protocol": PROTOCOL, "id": rid, "project": a.project,
             "goal": goal, "goal_terms": list(dict.fromkeys(si().tokens(goal))),
             "created_at": ctx.now_s, "updated_at": ctx.now_s, "status": "candidate",
             "status_log": [log_entry(ctx, None, "candidate", "propose")],
             "provenance": {"kind": "brief", "forked_from": None},
             "brief": {"source": source, "file": f"recipes/{rid}.brief.json", "sha256": sha256_bytes(raw),
                       "schema": brief.get("schema"), "terms": a.terms or "", "level": an.get("level"), "primary": an.get("primary"),
                       "deliverables": an.get("deliverables") or [], "recommended": rec,
                       "catalog_sha256": (brief.get("coverage") or {}).get("catalog_sha256"),
                       "must_haves": [m.get("need") for m in brief.get("must_have_coverage") or [] if isinstance(m, dict)]},
             "catalog": {"file_sha256": ctx.catalog["sha256"], "items": len(ctx.catalog["by_id"])},
             "deliverable_kind": deliv, "capabilities": caps, "nodes": nodes, "edges": edges, "plans": plans,
             "suggested_plan": rec if rec in plans else (sorted(plans)[0] if plans else None), "plan_choice": None,
             "tool_states": {k: tool_states[k] for k in sorted(tool_states)},
             "similar_unverified": similar_unverified(ctx, caps),
             "recall": {"matches": recall["matches"][:3], "avoid": recall["avoid"][:3], "nodes_with_memory": touched,
                        "template": tpl, "template_executors": template_executors(tpl_rec) if tpl_rec else {}},
             "traces": [], "evidence": [], "baseline": None, "imported": False, "legacy_unproven": False,
             "warnings": sorted(set(warnings)),
             "next_step": "validate; refine contracts with set-graph or bind if needed; then choose --plan X --why \"...\""}
        write_atomic(space / "recipes" / f"{rid}.brief.json", raw)
        path = save_recipe(space, r)
    return {"recipe": r, "path": str(path), "validate": summarize_validate(validate_recipe(ctx, space, r))}


def summarize_validate(v: dict) -> dict:
    return {"ok": not v["errors"], "errors": v["errors"], "warnings": v["warnings"], "notes": v["notes"]}


def cmd_show(ctx, a) -> dict:
    space = space_of(ctx, a.project, must_exist=True)
    return {"recipe": load_recipe(space, a.id, allow_v1=True)}


def cmd_catalog(ctx, a) -> dict:
    space = space_of(ctx, a.project)
    good, legacy, invalid = list_recipes(space)
    rows = [dict(index_row(r), reusable=r["status"] == "verified" and not validate_errors(ctx, space, r)) for r in good]
    return {"project": a.project, "exists": space.is_dir(), "total": len(good),
            "by_status": {s: sum(1 for r in good if r["status"] == s) for s in STATUSES},
            "recipes": rows, "legacy_v1": [r.get("id") for r in legacy], "invalid_files": invalid}


def cmd_validate(ctx, a) -> dict:
    space = space_of(ctx, a.project, must_exist=True)
    r = load_recipe(space, a.id)
    v = validate_recipe(ctx, space, r)
    out = {"id": r["id"], "status": r.get("status"), **summarize_validate(v), "drift": v.get("drift"),
           "reusable": r.get("status") == "verified" and not v["errors"]}
    if v["errors"]:
        raise FFError("VALIDATE_ERRORS", "; ".join(f"{e['code']} {e['name']} {e['where']}".strip() for e in v["errors"][:6]), rc=4, data=out)
    return out


def mutate(ctx, a, fn, allowed=None) -> dict:
    """Load, check state, apply fn(recipe, space) and save — all under the project lock."""
    space = space_of(ctx, a.project, must_exist=True)
    with locked(space):
        r = require_wellformed(load_recipe(space, a.id))
        if allowed is not None and r["status"] not in allowed:
            raise FFError("ILLEGAL_STATE" if r["status"] not in TERMINAL else "TERMINAL_RECIPE",
                          f"{r['id']} is {r['status']}; this command needs {' or '.join(allowed)}"
                          + ("; start a new experiment with fork" if r["status"] in TERMINAL else ""))
        result = fn(r, space)
        r["updated_at"] = ctx.now_s
        path = save_recipe(space, r)
    if isinstance(result, dict):
        result.setdefault("path", str(path))
    return result


def cmd_set_graph(ctx, a) -> dict:
    p = Path(a.file).expanduser()
    try:
        text = p.read_text(encoding="utf-8-sig")
        g = json.loads(text)
    except (OSError, ValueError) as exc:
        raise FFError("GRAPH_UNREADABLE", f"{p.name}: {type(exc).__name__}") from None
    refuse(_limit=False, graph=text)
    if not isinstance(g, dict) or not isinstance(g.get("nodes"), list) or not isinstance(g.get("edges"), list):
        raise FFError("GRAPH_INVALID", "graph.json must be {\"nodes\": [...], \"edges\": [...], \"plans\": {...}?}")

    for i, raw in enumerate(g["nodes"]):
        where = f"nodes[{i}]"
        if not isinstance(raw, dict) or not isinstance(raw.get("id"), str) or not isinstance(raw.get("stage"), str):
            raise FFError("GRAPH_INVALID", f"{where} must be an object with string id and stage")
        if not _strs(raw.get("capability_ids"), optional=True):
            raise FFError("GRAPH_INVALID", f"{where}.capability_ids must be a list of id strings")
        for side in ("inputs", "outputs"):
            ports = raw.get(side)
            if not isinstance(ports, list) or not all(isinstance(q, dict) and isinstance(q.get("kind"), str) and isinstance(q.get("name"), str) for q in ports):
                raise FFError("GRAPH_INVALID", f"{where}.{side} must be a list of {{\"name\": ..., \"kind\": ...}} objects")
        ex = raw.get("executor")
        if not (ex is None or isinstance(ex, str) or (isinstance(ex, dict) and isinstance(ex.get("ref"), str))):
            raise FFError("GRAPH_INVALID", f"{where}.executor must be a reference string or {{\"ref\": ...}}")
    for i, e in enumerate(g["edges"]):
        if not isinstance(e, dict) or not all(isinstance(e.get(k), str) for k in ("from", "to", "kind")) or not _opt(e.get("relation"), str):
            raise FFError("GRAPH_INVALID", f"edges[{i}] must be an object with string from, to, kind (and relation)")
    if g.get("plans") is not None:
        if not isinstance(g["plans"], dict) or not all(isinstance(v, dict) and _strs(v.get("nodes")) and v["nodes"] for v in g["plans"].values()):
            raise FFError("GRAPH_INVALID", "plans must be {\"A\": {\"nodes\": [\"N01\", ...]}, ...}")

    def apply(r, space):
        new_nodes = []
        for raw in g["nodes"]:
            ex = raw.get("executor") or "human"
            ref = ex.get("ref") if isinstance(ex, dict) else ex
            n = {"id": raw.get("id"), "stage": raw.get("stage"), "capability_ids": list(raw.get("capability_ids") or []),
                 "label": str(raw.get("label") or f"{raw.get('stage')}: model-designed node"),
                 "inputs": raw.get("inputs"), "outputs": raw.get("outputs"), "acceptance": str(raw.get("acceptance") or ""),
                 "contract_source": "model", "owner": str(raw.get("owner") or "claude"), "permission": str(raw.get("permission") or ""),
                 "rollback": str(raw.get("rollback") or ""), "optional": bool(raw.get("optional", False)),
                 "executor": {"ref": ref, "runnable": runnable_of(ctx, ref, r.get("tool_states")) if not ref_problem(ctx, ref) else "unknown",
                              "source": "set-graph"},
                 "status": "pending", "last_trace": None}
            new_nodes.append(n)
        edges = [{"id": "", "from": e.get("from"), "to": e.get("to"), "kind": e.get("kind"), "relation": e.get("relation") or "sequence"}
                 for e in g["edges"]]
        renumber_edges(edges)
        trial = dict(r, nodes=new_nodes, edges=edges)
        if isinstance(g.get("plans"), dict):
            trial["plans"] = {k: {"name": k, "label": PLAN_LABELS.get(k, ""), "idea": str(v.get("idea") or ""),
                                  "nodes": list(v["nodes"])} for k, v in g["plans"].items()}
        else:
            known = {n.get("id") for n in new_nodes}
            stale = [k for k, v in r["plans"].items() if any(x not in known for x in v.get("nodes") or [])]
            if stale:
                raise FFError("GRAPH_PLANS_STALE", f"plans {', '.join(sorted(stale))} name nodes that are gone; include \"plans\" in graph.json")
        caps = dict(r["capabilities"])
        for n in new_nodes:
            for c in n["capability_ids"]:
                if isinstance(c, str) and c not in caps:
                    caps[c] = cap_entry(ctx, c)
        trial["capabilities"] = caps
        v = validate_recipe(ctx, space, trial)
        if v["errors"]:
            raise FFError("GRAPH_INVALID", "; ".join(f"{e['code']} {e['name']} {e['where']}: {e['message']}" for e in v["errors"][:5]))
        r.update(nodes=new_nodes, edges=edges, plans=trial["plans"], capabilities=caps)
        if r.get("suggested_plan") not in r["plans"]:
            r["suggested_plan"] = sorted(r["plans"])[0]
        r.setdefault("graph_log", []).append({"at": ctx.now_s, "cmd": "set-graph", "sha256": sha256_text(text)})
        return {"id": r["id"], "nodes": len(new_nodes), "edges": len(edges), "plans": sorted(r["plans"]), "warnings": v["warnings"]}
    return mutate(ctx, a, apply, allowed=("candidate",))


def cmd_bind(ctx, a) -> dict:
    refuse(executor=a.executor, node=a.node)

    def apply(r, space):
        n = next((x for x in r["nodes"] if x["id"] == a.node), None)
        if not n:
            raise FFError("UNKNOWN_NODE", f"{a.node} is not a node of {r['id']}")
        ref = normalize_ref(ctx, a.executor)
        old = n["executor"].get("ref")
        n["executor"] = {"ref": ref, "runnable": runnable_of(ctx, ref, r.get("tool_states")), "source": "bind"}
        r.setdefault("graph_log", []).append({"at": ctx.now_s, "cmd": "bind", "node": a.node, "from": old, "to": ref})
        return {"id": r["id"], "node": a.node, "executor": n["executor"], "previous": old}
    return mutate(ctx, a, apply, allowed=("candidate", "planned"))


def cmd_choose(ctx, a) -> dict:
    refuse(why=a.why, nodes=a.nodes or "")
    if not (a.why or "").strip():
        raise FFError("USAGE", "--why must say why this plan was chosen")
    want = [x.strip() for x in (a.nodes or "").split(",") if x.strip()]
    if a.plan == "D" and not want:
        raise FFError("USAGE", "plan D needs --nodes N01,N02,... (named nodes from A/B/C)")
    if a.plan != "D" and want:
        raise FFError("USAGE", "--nodes is only for plan D")

    def apply(r, space):
        if r["status"] != "candidate":
            raise FFError("ILLEGAL_TRANSITION", f"{r['id']} is {r['status']}; choose moves candidate -> planned only")
        extra = {}
        if a.plan == "D":
            known = {n["id"] for n in r["nodes"]}
            bad = [n for n in want if n not in known]
            if bad:
                raise FFError("UNKNOWN_NODE", f"unknown nodes for plan D: {', '.join(bad)}")
            order = plan_order(r, want)
            edges = [dict(e) for e in r["edges"]]
            add_chain_edges(r["nodes"], edges, order)
            trial = dict(r, edges=edges)
            extra = {"D": {"name": "D", "label": PLAN_LABELS["D"], "idea": "user-approved merge of named nodes", "nodes": order, "tools": []}}
            v = validate_recipe(ctx, space, trial, extra_plans=extra)
        else:
            if a.plan not in r["plans"]:
                raise FFError("UNKNOWN_PLAN", f"{r['id']} has plans {', '.join(sorted(r['plans']))}, not {a.plan}")
            v = validate_recipe(ctx, space, r)
        if v["errors"]:
            raise FFError("VALIDATE_ERRORS", "fix these first: " + "; ".join(f"{e['code']} {e['name']} {e['where']}" for e in v["errors"][:6]))
        if extra:
            r["edges"] = trial["edges"]
            r["plans"].update(extra)
        nodes = list(r["plans"][a.plan]["nodes"])
        for n in r["nodes"]:  # results count only after the plan is approved
            n.update(status="pending", last_trace=None)
        r["plan_choice"] = {"plan": a.plan, "why": a.why.strip(), "nodes": nodes, "at": ctx.now_s,
                            "label": PLAN_LABELS[a.plan], "suggested_was": r.get("suggested_plan")}
        r["status_log"].append(log_entry(ctx, "candidate", "planned", "choose", note=a.why.strip()))
        r["status"] = "planned"
        r["next_step"] = "run each node of plan " + a.plan + " and trace it with --node and --result; then record tested"
        return {"id": r["id"], "status": "planned", "plan_choice": r["plan_choice"], "warnings": v["warnings"]}
    return mutate(ctx, a, apply)


def cmd_trace(ctx, a) -> dict:
    caps = [c.strip() for x in (a.capabilities or []) for c in str(x).split(",") if c.strip()]
    refuse(action=a.action, tool=a.tool or "", input=a.input or "", output=a.output or "", observed=a.observed or "",
           capabilities=caps, node=a.node or "", evidence=a.evidence or "")
    if not (a.action or "").strip():
        raise FFError("USAGE", "--action must describe what was actually done")
    if a.result == "skipped" and not (a.observed or "").strip():
        raise FFError("SKIP_NEEDS_OBSERVED", "a skipped node needs --observed explaining why it was not needed")
    if a.error_class and a.result != "failed":
        raise FFError("USAGE", "--error-class only goes with --result failed")

    def apply(r, space):
        if r["status"] in TERMINAL:
            raise FFError("TERMINAL_RECIPE", f"{r['id']} is {r['status']} (final); start a new experiment with fork")
        if a.result and r["status"] == "candidate":
            raise FFError("PLAN_NOT_CHOSEN", "a node result counts only after the plan is approved: choose --plan X --why \"...\" first "
                                             "(a trace without --result can still note preparatory work)")
        nodes = {n["id"]: n for n in r["nodes"]}
        chosen = (r.get("plan_choice") or {}).get("nodes")
        node = a.node
        if node is None and a.result:
            pool = [n for n in (chosen or list(nodes)) if nodes.get(n, {}).get("stage") == a.stage]
            if len(pool) != 1:
                raise FFError("NODE_REQUIRED", f"--result needs --node (stage {a.stage} has {len(pool)} candidate nodes)")
            node = pool[0]
        if node is not None:
            if node not in nodes:
                raise FFError("UNKNOWN_NODE", f"{node} is not a node of {r['id']}")
            if nodes[node]["stage"] != a.stage:
                raise FFError("STAGE_MISMATCH", f"{node} is a {nodes[node]['stage']} node, not {a.stage}")
            if chosen and node not in chosen:
                raise FFError("NODE_NOT_IN_PLAN", f"{node} is not in the chosen plan {r['plan_choice']['plan']}; fork to try another plan")
        known = set(r["capabilities"]) | {c for n in r["nodes"] for c in n["capability_ids"]}
        unknown = [c for c in caps if c not in known]
        if unknown:
            raise FFError("UNKNOWN_CAPABILITY", f"not capabilities of this recipe: {', '.join(unknown)}")
        planned = nodes[node]["executor"]["ref"] if node else None
        tool = normalize_ref(ctx, a.tool) if a.tool else planned
        entry = {"seq": max([t["seq"] for t in r["traces"]] + [0]) + 1, "at": ctx.now_s, "stage": a.stage, "node": node,
                 "result": a.result, "action": a.action.strip(), "tool": tool or "not_reported", "tool_reported": bool(a.tool),
                 "input": a.input or "", "output": a.output or "", "observed": a.observed or "",
                 "capabilities": caps, "error_class": a.error_class, "evidence": None, "substitution": None}
        if a.evidence:
            entry["evidence"] = evidence_receipt(ctx, space, a.evidence)
        if node and tool and planned and tool != planned:
            entry["substitution"] = {"planned": planned, "used": tool}
        r["traces"].append(entry)
        if node and a.result:
            nodes[node]["status"] = a.result
            nodes[node]["last_trace"] = entry["seq"]
        return {"id": r["id"], "trace": entry, "node_status": nodes[node]["status"] if node else None}
    return mutate(ctx, a, apply)


def verified_shas(r: dict) -> set:
    """Evidence that verified a recipe: its verified record evidence and its passed verify-stage trace evidence."""
    if r.get("status") != "verified":
        return set()
    nodes = {n["id"]: n for n in r.get("nodes") or []}
    out = {e["sha256"] for e in r.get("evidence") or [] if e.get("status") == "verified"}
    out |= {t["evidence"]["sha256"] for t in r.get("traces") or [] if t.get("result") == "passed" and t.get("evidence")
            and (nodes.get(t.get("node"), {}).get("stage") == "verify" or t.get("stage") == "verify")}
    return out


def verified_gate(ctx, space, r, ev: dict) -> None:
    pc = r.get("plan_choice")
    if not pc:
        raise FFError("PLAN_NOT_CHOSEN", "verified needs a chosen plan (choose --plan X --why ...)")
    nodes = {n["id"]: n for n in r["nodes"]}
    not_ok = [n for n in pc["nodes"] if nodes.get(n, {}).get("status") not in ("passed", "skipped")]
    if not_ok:
        raise FFError("GATE_NODE_NOT_PASSED", f"nodes of plan {pc['plan']} without a passed/skipped latest result: {', '.join(not_ok)}")
    traces = {t["seq"]: t for t in r["traces"]}
    after = as_dict(r.get("import_receipt")).get("trace_seq") if r.get("imported") else None
    if r.get("imported") and not isinstance(after, int):
        after = max(traces, default=0)  # imported before receipts existed: only traces added here count
    verify_ok, remote = [], []
    for n in pc["nodes"]:
        t = traces.get(nodes[n].get("last_trace")) or {}
        if nodes[n]["stage"] != "verify" or nodes[n]["status"] != "passed" or not t.get("evidence"):
            continue
        if (after is not None and t["seq"] <= after) or evidence_location(ctx, space, t["evidence"])[0] != "ok":
            remote.append(n)
            continue
        verify_ok.append(t)
    if not verify_ok:
        if remote:
            raise FFError("GATE_EVIDENCE_NOT_LOCAL", f"verify node(s) {', '.join(remote)} passed with evidence that is not on this machine "
                                                     "(imported or missing); run the QA here and trace it again")
        raise FFError("GATE_NO_VERIFY_EVIDENCE", "no verify node of the chosen plan passed with evidence")
    mine = {ev["sha256"]} | {t["evidence"]["sha256"] for t in verify_ok}
    others, _legacy, _invalid = list_recipes(space)
    others = [o for o in others if o["id"] != r["id"]]
    failure_shas = {rec["sha256"] for o in [r] + others for _w, rec, failed in evidence_records(o) if failed}
    if failure_shas & mine:
        raise FFError("GATE_FAILURE_EVIDENCE_REUSED", "this evidence was already recorded with a failure in this project "
                                                      "(this recipe, its parent or a sibling); produce a new QA result")
    for o in others:
        if verified_shas(o) & mine:
            raise FFError("GATE_EVIDENCE_REUSED", f"this QA evidence already verified {o['id']}; each verified recipe needs its own QA result")
    v = validate_recipe(ctx, space, r)
    if v["errors"]:
        raise FFError("GATE_VALIDATE_ERRORS", "validate must be clean: " + "; ".join(f"{e['code']} {e['name']}" for e in v["errors"][:6]))


def cmd_record(ctx, a) -> dict:
    refuse(note=a.note or "", evidence=a.evidence or "", baseline=a.baseline or "")
    if a.qa_pass and a.status != "verified":
        raise FFError("USAGE", "--qa-pass only goes with --status verified")
    if a.status == "planned":
        raise FFError("USE_CHOOSE", "planned is set only by: choose --plan A|B|C|D --why \"...\" (it records the approved plan)")

    def apply(r, space):
        cur = r["status"]
        if a.status not in TRANSITIONS.get(cur, ()):
            raise FFError("ILLEGAL_TRANSITION", f"{cur} -> {a.status} is not allowed (allowed: {', '.join(TRANSITIONS.get(cur, ())) or 'none; final state, use fork'})")
        if a.status == "failed" and not (a.note or "").strip():
            raise FFError("NOTE_REQUIRED", "failed needs --note saying what went wrong and how to avoid it next time")
        if a.status in ("tested", "failed", "verified") and not a.evidence:
            raise FFError("EVIDENCE_REQUIRED", f"{a.status} needs --evidence FILE")
        if a.status in ("tested", "verified") and not any(t.get("result") in ("passed", "failed") for t in r["traces"]):
            raise FFError("NO_RUN", "tested needs at least one trace with --result passed or failed")
        if a.status == "verified" and not a.qa_pass:
            raise FFError("QA_PASS_REQUIRED", "verified needs --qa-pass (your QA passed); never infer it from prose")
        ev = evidence_receipt(ctx, space, a.evidence, store=False) if a.evidence else None
        base = None
        if a.baseline:
            base = evidence_receipt(ctx, space, a.baseline, role="baseline", store=False)
            if ev and base["sha256"] == ev["sha256"]:
                raise FFError("BASELINE_SAME_AS_EVIDENCE", "the baseline must be a different file from the evidence")
        if a.status == "verified":
            verified_gate(ctx, space, r, ev)
        for rec in (ev, base):
            if rec:
                persist_evidence(space, rec)
        if ev:
            r["evidence"].append(dict(ev, status=a.status, qa_pass=bool(a.qa_pass), note=a.note or "", at=ctx.now_s))
        if base:
            r["baseline"] = dict(base, at=ctx.now_s)
        r["status_log"].append(log_entry(ctx, cur, a.status, "record", note=a.note or "", evidence_sha=ev["sha256"] if ev else None))
        r["status"] = a.status
        r["next_step"] = {"planned": "run and trace the chosen plan's nodes", "tested": "fix and trace again, then record verified with --qa-pass",
                          "verified": "reusable in this project (reuse/propose recall); promote only proposes, a human approves",
                          "failed": "run lessons; fork to try again"}[a.status]
        return {"id": r["id"], "status": a.status, "from": cur, "evidence_sha256": ev["sha256"] if ev else None}
    return mutate(ctx, a, apply)


def cmd_fork(ctx, a) -> dict:
    space = space_of(ctx, a.project, must_exist=True)
    with locked(space):
        src = require_wellformed(load_recipe(space, a.id))
        rid = new_id(ctx, space, f"fork|{src['id']}", a.new_id)
        r = json.loads(json.dumps(src))
        for n in r["nodes"]:
            n.update(status="pending", last_trace=None)
            n.pop("memory", None)
        r.update(id=rid, created_at=ctx.now_s, updated_at=ctx.now_s, status="candidate",
                 status_log=[log_entry(ctx, None, "candidate", "fork", note=f"forked from {src['id']} ({src['status']})")],
                 provenance={"kind": "fork", "forked_from": src["id"]}, forked_from=src["id"], plan_choice=None,
                 traces=[], evidence=[], baseline=None, imported=False, legacy_unproven=False,
                 next_step="validate; adjust with set-graph/bind; choose --plan X --why \"...\"")
        for k in ("graph_log", "migrated_from", "imported_at", "import_bundle_sha256", "import_receipt", "plan_choice_at_export", "self_reported"):
            r.pop(k, None)
        r["warnings"] = [w for w in r.get("warnings") or [] if not w.startswith(("MIGRATED_FROM_V1", "IMPORTED_FROM_CARD", "LEARNING_INDEX_EMPTY"))]
        bsrc = space / "recipes" / f"{src['id']}.brief.json"
        if bsrc.is_file():
            write_atomic(space / "recipes" / f"{rid}.brief.json", bsrc.read_bytes())
            r["brief"] = dict(r.get("brief") or {}, file=f"recipes/{rid}.brief.json")
        path = save_recipe(space, r)
    return {"recipe": r, "path": str(path), "forked_from": src["id"]}


def cmd_lessons(ctx, a) -> dict:
    space = space_of(ctx, a.project, must_exist=True)
    with locked(space):
        good, legacy, invalid = list_recipes(space)
        lessons = [l for r in good for l in extract_lessons(r)]
        agg = collections.defaultdict(lambda: {"passed": 0, "failed": 0, "assumed_passed": 0, "assumed_failed": 0,
                                               "replaced_by": collections.Counter(), "error_classes": collections.Counter()})
        for l in lessons:
            ex = l.get("executor")
            if not ex:
                continue
            pre = "assumed_" if l.get("assumed_executor") else ""  # the trace named no --tool: kept apart from reported runs
            if l["type"] == "WORKED":
                agg[ex][pre + "passed"] += 1
            elif l["type"] == "FAILED":
                agg[ex][pre + "failed"] += 1
                agg[ex]["error_classes"][l.get("error_class")] += 1
            elif l["type"] == "REPLACED":
                agg[ex]["replaced_by"][l.get("replaced_by")] += 1
        by_ex = {k: {"passed": v["passed"], "failed": v["failed"], "assumed_passed": v["assumed_passed"], "assumed_failed": v["assumed_failed"],
                     "replaced_by": dict(sorted(v["replaced_by"].items())),
                     "error_classes": dict(sorted(v["error_classes"].items()))} for k, v in sorted(agg.items())}
        doc = {"schema": LESSONS_SCHEMA, "project": a.project, "generated_at": ctx.now_s, "recipes_scanned": len(good),
               "legacy_v1": [r.get("id") for r in legacy], "invalid_files": invalid,
               "counts": dict(sorted(collections.Counter(l["type"] for l in lessons).items())),
               "lessons": lessons, "by_executor": by_ex}
        write_atomic(space / "lessons.json", dump(doc))
    doc["path"] = str(space / "lessons.json")
    return doc


def cmd_reuse(ctx, a) -> dict:
    goal = (a.goal or "").strip()
    if not goal:
        raise FFError("USAGE", "goal is empty")
    space = space_of(ctx, a.project)
    caps, brief_used = [], "none"
    if not space.is_dir():
        return {"project": a.project, "goal": goal, "brief": "skipped (no records in this project)",
                "formula": "score = sim x strength x recency x freshness",
                "matches": [], "avoid": [], "considered": 0, "legacy_v1": [], "invalid_files": []}
    if a.from_brief:
        brief, _raw, _src = load_brief(ctx, argparse.Namespace(from_brief=a.from_brief, terms=""), goal)
        brief_used = "file"
    elif not a.no_brief:
        try:
            brief, _raw, _src = load_brief(ctx, argparse.Namespace(from_brief=None, terms=a.terms or ""), goal)
            brief_used = "in_process"
        except FFError as exc:
            if exc.code not in ("BRIEF_FAILED", "BRIEF_INCOMPLETE", "BRIEF_SCHEMA"):
                raise
            brief_used = f"none ({exc.code}; goal-text similarity only)"
    if brief_used in ("file", "in_process"):
        try:
            brief, _remapped = reconcile_brief(ctx, brief)
        except FFError as exc:
            brief, brief_used = {}, f"none ({exc.code}; goal-text similarity only)"
        caps = sorted({c for p in as_dict(brief.get("plans")).values() for st in as_dict(as_dict(p).get("stages")).values()
                       for c in (st if isinstance(st, list) else []) if isinstance(c, str)}
                      | {x["id"] for x in (brief.get("shortlist") if isinstance(brief.get("shortlist"), list) else [])[:30]
                         if isinstance(x, dict) and isinstance(x.get("id"), str)})
    res = rank_prior(ctx, space, goal, caps)
    res["matches"] = res["matches"][: max(1, a.top)]
    return {"project": a.project, "goal": goal, "brief": brief_used, "formula": "score = sim x strength x recency x freshness", **res}


def card_payload(ctx, r: dict) -> dict:
    lessons = extract_lessons(r)
    return redact_obj({
        "schema": CARD_SCHEMA, "engine": ENGINE, "protocol": PROTOCOL, "source_recipe": r["id"], "project": r["project"],
        "status_at_export": r["status"], "goal": r["goal"], "deliverable_kind": r.get("deliverable_kind", "any"),
        "brief": {k: (r.get("brief") or {}).get(k) for k in ("sha256", "level", "primary", "recommended", "catalog_sha256")},
        "catalog": r.get("catalog"), "capabilities": r.get("capabilities"),
        "nodes": [{k: v for k, v in n.items() if k not in ("last_trace", "memory")} for n in r["nodes"]],
        "edges": r["edges"], "plans": r["plans"], "suggested_plan": r.get("suggested_plan"), "plan_choice": r.get("plan_choice"),
        "self_reported": [{"seq": t.get("seq"), "node": t.get("node"), "stage": t.get("stage"), "result": t.get("result"),
                           "tool": t.get("tool"), "observed": clip(t.get("observed"), 200),
                           "evidence_sha256": (t.get("evidence") or {}).get("sha256")} for t in r["traces"]],
        "evidence_sha256": sorted({rec["sha256"] for _w, rec, _f in evidence_records(r) if rec.get("sha256")}),
        "lessons": [{"type": l["type"], "node": l["node"], "executor": l.get("executor")} for l in lessons],
        "generated_at": ctx.now_s})


def render_card(payload: dict) -> str:
    pc = payload.get("plan_choice") or {}
    L = [f"# FusionForge card — {payload['source_recipe']} ({payload['status_at_export']})", "",
         f"<!-- {CARD_SCHEMA} · import: fusionforge.py import-card <this file> --project <slug> (always imports as candidate) -->", "",
         f"**Goal:** {payload['goal']}", "",
         f"**Plan:** {pc.get('plan') or '—'} {('— ' + str(pc.get('why') or '')) if pc else '(not chosen; suggested ' + str(payload.get('suggested_plan')) + ')'}", "",
         "**Plans:** " + " · ".join(f"{k}: {' '.join(v.get('nodes') or [])}" for k, v in sorted((payload.get("plans") or {}).items())), "",
         "| node | stage | executor | in → out | status | capabilities |", "|---|---|---|---|---|---|"]
    for n in payload["nodes"]:
        L.append(f"| {n['id']} | {n['stage']} | {n['executor']['ref']} | {', '.join(p['kind'] for p in n['inputs'])} → "
                 f"{', '.join(p['kind'] for p in n['outputs'])} | {n['status']} | {', '.join(n['capability_ids']) or '—'} |")
    L += ["", "**Edges:** " + (" · ".join(f"{e['from']}→{e['to']} ({e['kind']})" for e in payload["edges"]) or "—"),
          "", "**Evidence (sha256):** " + (" · ".join(s[:16] + "…" for s in payload["evidence_sha256"]) or "none"),
          "", "Results below are self-reported in this card; only a local FusionForge run with evidence can verify them.",
          "Written by hand without a shell? Mark it UNSAVED and say MEMORY_RUNTIME_UNAVAILABLE.", "",
          "```json fusionforge-card-v2", json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")), "```", ""]
    return "\n".join(L)


def guard_out(ctx, out: Path, suffix: str) -> Path:
    """card/export --out: the right file type, never inside FusionForge's own records and never over one of them."""
    if out.suffix.lower() != suffix:
        raise FFError("OUT_REFUSED", f"--out must be a {suffix} file")
    rp = out.resolve()
    with contextlib.suppress(ValueError):
        parts = rp.relative_to(ctx.root).parts
        if len(parts) >= 2 and (parts[1] in FORBIDDEN_OUT or (len(parts) == 2 and parts[1] in FORBIDDEN_EVIDENCE_FILES)):
            raise FFError("OUT_REFUSED", f"--out cannot be inside FusionForge records ({'/'.join(parts[1:])}); write the {suffix} elsewhere")
    kind = None
    with contextlib.suppress(OSError):
        if rp.is_file() and rp.stat().st_size <= 64 * 1024 * 1024:
            kind = ff_record_kind(rp.read_bytes())
    if kind and kind != {".md": "card", ".json": BUNDLE_SCHEMA}[suffix]:
        raise FFError("OUT_REFUSED", f"--out would overwrite a FusionForge record ({rp.name}, {kind})")
    return out


def cmd_card(ctx, a) -> dict:
    space = space_of(ctx, a.project, must_exist=True)
    r = require_wellformed(load_recipe(space, a.id))
    payload = card_payload(ctx, r)
    text = render_card(payload)
    hits = find_secrets(text)
    if hits:
        raise FFError("SECRET", f"card would contain a credential pattern ({', '.join(hits)}); fix the recipe first")
    out = Path(a.out).expanduser() if a.out else space / "cards" / f"{r['id']}.md"
    if not out.is_absolute():
        out = ctx.cwd / out
    guard_out(ctx, out, ".md")
    if a.out:
        write_atomic(out, text)
    else:
        with locked(space):
            write_atomic(out, text)
    return {"id": r["id"], "path": str(out), "card_sha256": sha256_text(text), "status_at_export": r["status"],
            "nodes": len(payload["nodes"]), "markdown": text}


CARD_RX = re.compile(r"```json[ \t]+fusionforge-card-v2[ \t]*\r?\n(.*?)\r?\n```", re.S)


def cmd_import_card(ctx, a) -> dict:
    p = Path(a.file).expanduser()
    try:
        text = p.read_text(encoding="utf-8-sig")
    except (OSError, ValueError) as exc:
        raise FFError("CARD_UNREADABLE", f"{p.name}: {type(exc).__name__}") from None
    refuse(_limit=False, card=text)
    blocks = CARD_RX.findall(text) or re.findall(r"```json[^\n]*\n(.*?)\n```", text, re.S)
    card = None
    for b in blocks:
        with contextlib.suppress(ValueError):
            obj = json.loads(b)
            if isinstance(obj, dict) and obj.get("schema") == CARD_SCHEMA:
                card = obj
                break
    if card is None:
        raise FFError("CARD_INVALID", f"no ```json fusionforge-card-v2 block with schema {CARD_SCHEMA}")
    space = space_of(ctx, a.project)
    with locked(space):
        rid = new_id(ctx, space, f"card|{sha256_text(text)}", a.new_id)
        nodes = []
        for n in card.get("nodes") if isinstance(card.get("nodes"), list) else []:
            if isinstance(n, dict):
                nodes.append(dict({k: v for k, v in n.items() if k != "memory"}, status="pending", last_trace=None))
        r = {"schema": SCHEMA, "engine": ENGINE, "protocol": PROTOCOL, "id": rid, "project": a.project,
             "goal": str(card.get("goal") or ""), "goal_terms": list(dict.fromkeys(si().tokens(str(card.get("goal") or "")))),
             "created_at": ctx.now_s, "updated_at": ctx.now_s, "status": "candidate",
             "status_log": [log_entry(ctx, None, "candidate", "import-card", note=f"card of {card.get('source_recipe')} ({card.get('status_at_export')})")],
             "provenance": {"kind": "card", "card_sha256": sha256_text(text), "source_recipe": card.get("source_recipe"),
                            "status_at_export": card.get("status_at_export"), "forked_from": None},
             "brief": dict(as_dict(card.get("brief")), source="card", file=None), "catalog": as_dict(card.get("catalog")),
             "deliverable_kind": card.get("deliverable_kind") or "any", "capabilities": card.get("capabilities") or {},
             "nodes": nodes, "edges": card.get("edges") or [], "plans": {k: v for k, v in as_dict(card.get("plans")).items() if k in PLAN_LETTERS},
             "suggested_plan": card.get("suggested_plan") if isinstance(card.get("suggested_plan"), str) else None,
             "plan_choice": None, "plan_choice_at_export": card.get("plan_choice"),
             "tool_states": {}, "similar_unverified": [], "recall": {"matches": [], "avoid": [], "nodes_with_memory": 0, "template": None},
             "self_reported": card.get("self_reported") if isinstance(card.get("self_reported"), list) else [],
             "traces": [], "evidence": [], "baseline": None,
             "imported": False, "legacy_unproven": False, "warnings": ["IMPORTED_FROM_CARD: results are self-reported, not evidence"],
             "next_step": "validate; choose --plan X --why \"...\"; run and trace locally to earn tested/verified"}
        mal = malformed(r)
        if mal:
            raise FFError("CARD_INVALID", f"the card's graph is malformed ({', '.join(mal[:5])})")
        v = validate_recipe(ctx, space, r)
        bad = [e for e in v["errors"] if e["name"] in ("SCHEMA", "STATE_LOG_INVALID", "SECRET")]
        if bad:
            raise FFError("CARD_INVALID", "; ".join(f"{e['code']} {e['where']}: {e['message']}" for e in bad[:5]))
        path = save_recipe(space, r)
    return {"recipe": r, "path": str(path), "validate": summarize_validate(v)}


def export_recipe(r: dict) -> dict:
    x = json.loads(json.dumps(r))
    for _w, rec, _f in evidence_records(x):
        rec["source"], rec["source_base"] = None, None
        rec.pop("root_rel", None)
    if isinstance(x.get("brief"), dict):
        x["brief"]["file"] = None
    return redact_obj(x)


def cmd_export(ctx, a) -> dict:
    space = space_of(ctx, a.project, must_exist=True)
    with locked(space):
        good, _legacy, invalid = list_recipes(space)
        keep = [r for r in good if a.include_candidates or r["status"] in ("tested", "verified", "failed")]
        recipes = [export_recipe(r) for r in keep]
        bundle = {"schema": BUNDLE_SCHEMA, "engine": ENGINE, "project": a.project, "exported_at": ctx.now_s,
                  "include_candidates": bool(a.include_candidates), "recipes": recipes,
                  "lessons": [l for r in keep for l in extract_lessons(r)],
                  "skipped_invalid_files": [i["file"] for i in invalid],
                  "note": "redacted: no absolute paths, evidence by sha256 only; opt-in persistence, never auto-committed"}
        text = dump(bundle)
        hits = find_secrets(text)
        if hits:
            raise FFError("SECRET", f"bundle would contain a credential pattern ({', '.join(hits)})")
        out = Path(a.out).expanduser() if a.out else space / "exports" / f"{a.project}-{ctx.now.strftime('%Y%m%d')}.json"
        if not out.is_absolute():
            out = ctx.cwd / out
        guard_out(ctx, out, ".json")
        write_atomic(out, text)
    return {"path": str(out), "recipes": len(recipes), "lessons": len(bundle["lessons"]), "sha256": sha256_text(text),
            "by_status": dict(sorted(collections.Counter(r["status"] for r in recipes).items()))}


def cmd_import(ctx, a) -> dict:
    p = Path(a.file).expanduser()
    try:
        text = p.read_text(encoding="utf-8-sig")
        bundle = json.loads(text)
    except (OSError, ValueError) as exc:
        raise FFError("BUNDLE_UNREADABLE", f"{p.name}: {type(exc).__name__}") from None
    refuse(_limit=False, bundle=text)
    if not isinstance(bundle, dict) or bundle.get("schema") != BUNDLE_SCHEMA or not isinstance(bundle.get("recipes"), list):
        raise FFError("BUNDLE_INVALID", f"not a {BUNDLE_SCHEMA} bundle")
    if bundle.get("project") != a.project:
        raise FFError("PROJECT_MISMATCH", f"the bundle belongs to project '{bundle.get('project')}', not '{a.project}' (projects stay isolated)")
    space = space_of(ctx, a.project)
    done = {"imported": [], "skipped_existing": [], "conflicts": [], "invalid": []}
    with locked(space):
        for r in bundle["recipes"]:
            rid = r.get("id") if isinstance(r, dict) else None
            if not rid or not ID_RX.fullmatch(str(rid)) or r.get("schema") != SCHEMA or r.get("project") != a.project:
                done["invalid"].append(str(rid))
                continue
            if malformed(r):
                done["invalid"].append(rid)
                continue
            x = json.loads(json.dumps(r))
            for _w, rec, _f in evidence_records(x):  # paths of another machine mean nothing here; only the hash travels
                rec.update(source=None, source_base=None, imported=True)
                rec.pop("root_rel", None)
            x.update(imported=True, imported_at=ctx.now_s, import_bundle_sha256=sha256_text(text),
                     import_receipt={"at": ctx.now_s, "bundle_sha256": sha256_text(text), "status": r.get("status"),
                                     "trace_seq": max([t["seq"] for t in r["traces"]] + [0]), "log_len": len(r["status_log"])})
            v = validate_recipe(ctx, space, x)
            if [e for e in v["errors"] if e["name"] in ("SCHEMA", "STATE_LOG_INVALID", "SECRET")]:
                done["invalid"].append(rid)
                continue
            path = recipe_path(space, rid)
            if path.exists():
                skip = ("imported", "imported_at", "import_bundle_sha256", "import_receipt")
                try:
                    same = {k: val for k, val in as_dict(read_json(path)).items() if k not in skip} == \
                           {k: val for k, val in x.items() if k not in skip}
                except (OSError, ValueError):
                    same = False
                done["skipped_existing" if same else "conflicts"].append(rid)
                continue
            write_atomic(path, dump(x))
            done["imported"].append(rid)
        refresh_index(space)
    return {"project": a.project, **done, "note": "imported recipes keep their status with imported: true; reuse weighs them x0.8"}


def _s(x):
    return x if isinstance(x, str) else None


def migrate_v1(ctx, space: Path, old: dict) -> dict:
    same_cat = old.get("catalog_sha256") == ctx.catalog["sha256"]
    caps = {}
    for c in old.get("capabilities") if isinstance(old.get("capabilities"), list) else []:
        cid = c.get("id") if isinstance(c, dict) else None
        if not isinstance(cid, str) or not cid:
            continue
        if same_cat and cid in ctx.catalog["by_id"]:
            caps[cid] = fingerprint(ctx.catalog["by_id"][cid])
        else:
            caps[cid] = {"name_en": str(c.get("name") or ""), "name_ar": "", "atoms": [], "atoms_sha256": None,
                         "known": bool(same_cat and cid in ctx.catalog["by_id"])}
    nodes = []
    for st in old.get("workflow") if isinstance(old.get("workflow"), list) else []:
        if isinstance(st, dict) and st.get("stage") in STAGES and isinstance(st.get("capability_ids"), list) and st["capability_ids"]:
            ins, outs, check = stage_io(st["stage"], "any")
            nodes.append({"id": f"N{len(nodes) + 1:02d}", "stage": st["stage"], "capability_ids": [c for c in st["capability_ids"] if isinstance(c, str) and c in caps],
                          "label": f"{st['stage']} (migrated from v1)", "inputs": ins, "outputs": outs, "acceptance": check,
                          "contract_source": "migrated_default", "owner": "claude", "permission": "", "rollback": "",
                          "optional": False, "executor": method_executor(ctx, [c for c in st["capability_ids"] if isinstance(c, str) and c in caps and caps[c]["known"]]),
                          "status": "pending", "last_trace": None})
    if not any(n["stage"] == "verify" for n in nodes):
        ins, outs, check = stage_io("verify", "any")
        nodes.append({"id": f"N{len(nodes) + 1:02d}", "stage": "verify", "capability_ids": [], "label": "verify: manual QA (added by migrate)",
                      "inputs": ins, "outputs": outs, "acceptance": check, "contract_source": "migrated_default", "owner": "claude",
                      "permission": "", "rollback": "", "optional": False, "executor": {"ref": "human", "runnable": "human", "source": "migrated"},
                      "status": "pending", "last_trace": None})
    r = {"nodes": nodes, "edges": []}
    order = plan_order(r, [n["id"] for n in nodes])
    add_chain_edges(nodes, r["edges"], order)
    stage_node = {n["stage"]: n["id"] for n in nodes}

    def legacy_evidence(path, sha):
        if isinstance(path, str) and path and Path(path).is_file():
            with contextlib.suppress(FFError):
                rec = evidence_receipt(ctx, space, path)
                if rec["sha256"] == sha:
                    return dict(rec, legacy=True)
        return {"sha256": sha, "size": None, "suffix": "", "stored": None, "source": None, "source_base": None, "legacy": True}
    traces = []
    for i, t in enumerate(old.get("execution_trace") or [], 1):
        if not isinstance(t, dict):
            continue
        ev = t.get("evidence") if isinstance(t.get("evidence"), dict) else None
        traces.append({"seq": i, "at": _s(t.get("logged_at")) or _s(old.get("updated_at")), "stage": _s(t.get("stage")),
                       "node": stage_node.get(_s(t.get("stage"))), "result": None, "action": str(t.get("action") or ""),
                       "tool": str(t.get("tool") or "not_reported"), "input": str(t.get("input_summary") or ""),
                       "output": str(t.get("output_summary") or ""), "observed": str(t.get("observed") or ""),
                       "capabilities": [c for c in t.get("reported_capability_ids") or [] if isinstance(c, str)] if isinstance(t.get("reported_capability_ids"), list) else [],
                       "error_class": None, "substitution": None, "legacy": True,
                       "evidence": legacy_evidence(ev.get("local_path"), ev["sha256"]) if ev and isinstance(ev.get("sha256"), str) else None})
    evidence = []
    for e in old.get("evidence") if isinstance(old.get("evidence"), list) else []:
        if isinstance(e, dict) and isinstance(e.get("sha256"), str):
            evidence.append(dict(legacy_evidence(e.get("file_local"), e["sha256"]), status=_s(e.get("status")),
                                 qa_pass=bool(e.get("qa_pass_asserted")), note=str(e.get("comment") or ""), at=_s(e.get("recorded_at"))))
    status = old.get("status") if old.get("status") in STATUSES else "candidate"
    path = {"candidate": ["candidate"], "planned": ["candidate", "planned"], "tested": ["candidate", "planned", "tested"],
            "verified": ["candidate", "planned", "tested", "verified"], "failed": ["candidate", "failed"]}[status]
    log, prev = [], None
    for st in path:
        sha = next((e["sha256"] for e in reversed(evidence) if e.get("status") == st), None)
        log.append({"from": prev, "to": st, "at": _s(old.get("created_at")) if prev is None else _s(old.get("updated_at")),
                    "cmd": "migrate", "note": "reconstructed from v1", "evidence_sha256": sha})
        prev = st
    plans = {"A": {"name": "A", "label": PLAN_LABELS["A"], "idea": "v1 workflow (migrated)", "nodes": order, "tools": []}}
    return {"schema": SCHEMA, "engine": ENGINE, "protocol": PROTOCOL, "id": old["id"], "project": space.name,
            "goal": str(old.get("goal") or ""), "goal_terms": list(dict.fromkeys(si().tokens(str(old.get("goal") or "")))),
            "created_at": _s(old.get("created_at")) or ctx.now_s, "updated_at": ctx.now_s, "status": status, "status_log": log,
            "provenance": {"kind": "migrated", "forked_from": None}, "migrated_from": SCHEMA_V1,
            "brief": {"source": "none", "file": None}, "catalog": {"file_sha256": _s(old.get("catalog_sha256")), "items": None},
            "deliverable_kind": "any", "capabilities": caps, "nodes": nodes, "edges": r["edges"], "plans": plans,
            "suggested_plan": "A", "plan_choice": {"plan": "A", "why": "migrated v1 recipe", "nodes": order, "at": _s(old.get("updated_at")),
                                                   "label": PLAN_LABELS["A"]} if status in ("planned", "tested", "verified") else None,
            "tool_states": {}, "similar_unverified": [], "recall": {"matches": [], "avoid": [], "nodes_with_memory": 0, "template": None},
            "traces": traces, "evidence": evidence, "baseline": None, "imported": False,
            "legacy_unproven": status == "verified" and not traces,
            "warnings": ["MIGRATED_FROM_V1: contracts are defaults and v1 traces carry no result"],
            "next_step": "fork to run this workflow again under v2 rules"}


def cmd_migrate(ctx, a) -> dict:
    space = space_of(ctx, a.project, must_exist=True)
    done = {"migrated": [], "already_v2": [], "skipped": []}
    with locked(space):
        for p in sorted((space / "recipes").glob("FUSE-*.json")):
            if not ID_RX.fullmatch(p.stem) or p.is_symlink():
                continue
            try:
                raw = p.read_bytes()
                old = json.loads(raw.decode("utf-8"))
            except (OSError, ValueError) as exc:
                done["skipped"].append({"id": p.stem, "reason": f"unreadable ({type(exc).__name__})"})
                continue
            if not isinstance(old, dict) or old.get("id") != p.stem:
                done["skipped"].append({"id": p.stem, "reason": "not a recipe object"})
                continue
            if old.get("schema") == SCHEMA:
                done["already_v2"].append(p.stem)
                continue
            if old.get("schema") != SCHEMA_V1:
                done["skipped"].append({"id": p.stem, "reason": f"unknown schema {old.get('schema')!r}"})
                continue
            hits = scan_object(old)
            if hits:
                done["skipped"].append({"id": p.stem, "reason": f"contains a credential pattern ({', '.join(hits[0][1])}) — clean it by hand"})
                continue
            backup = space / "legacy" / f"{p.stem}.v1.json"
            if not backup.exists():
                write_atomic(backup, raw)
            new = migrate_v1(ctx, space, old)
            write_atomic(p, dump(new))
            done["migrated"].append({"id": p.stem, "status": new["status"], "legacy_unproven": new["legacy_unproven"],
                                     "backup": f"legacy/{p.stem}.v1.json"})
        refresh_index(space)
    return {"project": a.project, **done}


def proven_here(ctx, space: Path, r: dict, v: dict) -> None:
    """Promotion needs a recipe verified under v2 rules on this machine: not migrated, not legacy_unproven, an imported
    one only when it was verified here after the import, and a passed verify-node trace with local evidence."""
    if r.get("legacy_unproven") or r.get("migrated_from"):
        raise FFError("NOT_PROVEN", f"{r['id']} is a migrated v1 recipe; fork it, run it and verify it under v2 rules before proposing it")
    if any(w["name"] == "VERIFIED_WITHOUT_RUN" for w in v["warnings"]):
        raise FFError("NOT_PROVEN", f"{r['id']} is verified without a recorded verify run")
    after = None
    if r.get("imported"):
        rc = as_dict(r.get("import_receipt"))
        log_len, after = rc.get("log_len"), rc.get("trace_seq")
        if not isinstance(log_len, int) or not isinstance(after, int) or \
                not any(s.get("to") == "verified" for s in r["status_log"][log_len:]):
            raise FFError("NOT_PROVEN", f"{r['id']} was imported{' already verified' if rc.get('status') == 'verified' else ''}; "
                                        "only a recipe verified on this machine can be proposed (fork it and run it here)")
    chosen = set(as_dict(r.get("plan_choice")).get("nodes") or [])
    nodes = {n["id"]: n for n in r["nodes"]}
    local = [t for t in r["traces"] if t.get("result") == "passed" and t.get("evidence") and t.get("node") in chosen
             and nodes.get(t["node"], {}).get("stage") == "verify" and (after is None or t["seq"] > after)
             and evidence_location(ctx, space, t["evidence"])[0] == "ok"]
    if not local:
        raise FFError("NOT_PROVEN", f"{r['id']} has no passed verify-node trace with evidence on this machine")


def cmd_promote(ctx, a) -> dict:
    space = space_of(ctx, a.project, must_exist=True)
    with locked(space):
        r = require_wellformed(load_recipe(space, a.id))
        if r["status"] != "verified":
            raise FFError("NOT_VERIFIED", f"{r['id']} is {r['status']}; only verified recipes can be proposed for promotion")
        v = validate_recipe(ctx, space, r)
        if v["errors"]:
            raise FFError("VALIDATE_ERRORS", "; ".join(f"{e['code']} {e['name']}" for e in v["errors"][:6]))
        proven_here(ctx, space, r, v)
        out = space / "promotions" / f"{r['id']}.proposal.json"
        if out.is_file():
            with contextlib.suppress(OSError, ValueError):
                prev = read_json(out)
                return {"path": str(out), "approval": prev.get("approval"), "graph_signature": prev.get("graph_signature"), "existing": True}
        chosen = (r.get("plan_choice") or {}).get("nodes") or [n["id"] for n in r["nodes"]]
        nodes = {n["id"]: n for n in r["nodes"]}
        snodes = [{"stage": nodes[n]["stage"], "executor": nodes[n]["executor"]["ref"],
                   "capabilities": [{"name_en": (r["capabilities"].get(c) or {}).get("name_en"), "atoms_sha256": (r["capabilities"].get(c) or {}).get("atoms_sha256")}
                                    for c in nodes[n]["capability_ids"]],
                   "inputs": sorted(p["kind"] for p in nodes[n]["inputs"]), "outputs": sorted(p["kind"] for p in nodes[n]["outputs"]),
                   "acceptance": nodes[n].get("acceptance", "")} for n in chosen]
        sedges = sorted([nodes[e["from"]]["stage"], nodes[e["to"]]["stage"], e["kind"], e["relation"]] for e in induced_edges(r, chosen))
        sig = sha256_text(json.dumps([sorted([n["stage"], n["executor"], n["inputs"], n["outputs"]] for n in snodes), sedges], sort_keys=True))
        proposal = {"schema": PROMOTION_SCHEMA, "recipe_id": r["id"], "created_at": ctx.now_s, "graph_signature": sig,
                    "sanitized": {"nodes": snodes, "edges": sedges,
                                  "lesson_keys": sorted({f"{l['type']}:{l.get('stage')}:{l.get('executor')}" for l in extract_lessons(r)})},
                    "excluded_fields": ["goal", "project", "observed", "notes", "evidence paths", "traces"],
                    "requirements": ["verified in at least two independent projects with the same graph_signature",
                                     "secrets and tenant review by a human", "collision test against the existing catalog",
                                     "the maintain.md chain (build, validate, check_skill) after a human approves"],
                    "approval": {"state": "pending_human", "approved_by": None,
                                 "note": "set only by a human through references/guides/maintain.md; this engine never approves or edits the catalog"}}
        write_atomic(out, dump(proposal))
    return {"path": str(out), "approval": proposal["approval"], "graph_signature": sig, "existing": False}


# ------------------------------------------------------------------ human summaries (default output)
def summary(cmd: str, res: dict, ctx) -> str:
    try:
        return _summary(cmd, res)
    except (KeyError, TypeError, AttributeError, ValueError, IndexError):  # a malformed record degrades, never crashes
        r = as_dict(res.get("recipe"))
        return "\n".join([f"{ENGINE} · {clip(r.get('id') or res.get('id'), 40)} · {clip(r.get('status') or res.get('status'), 20)}",
                          "this record does not have the expected shape (malformed); run validate for details or use --json"])


def _summary(cmd: str, res: dict) -> str:
    L = []
    r = res.get("recipe")
    if cmd in ("propose", "show", "fork", "import-card") and r:
        L.append(f"{ENGINE} · {r['id']} · {r.get('status')} · project {r.get('project')}")
        L.append(f"goal: {clip(r.get('goal'), 100)}")
        if r.get("schema") == SCHEMA_V1:
            L.append("legacy v1 recipe — run migrate to use it with v2 commands")
            return "\n".join(L)
        b = r.get("brief") or {}
        if b.get("level"):
            L.append(f"brief: {b.get('level')} {b.get('primary')} · recommended {b.get('recommended')} · sha {str(b.get('sha256'))[:12]}")
        pc = r.get("plan_choice")
        L.append("plans: " + " · ".join(f"{k} {len(p['nodes'])} nodes" for k, p in sorted(r["plans"].items()))
                 + (f" · chosen {pc['plan']}" if pc else f" · suggested {r.get('suggested_plan')}"))
        for n in r["nodes"][:12]:
            mem = " · memory" if n.get("memory") else ""
            L.append(f"  {n['id']} {n['stage']:<10} {n['status']:<7} {n['executor']['ref']:<28} "
                     f"{'/'.join(p['kind'] for p in n['inputs'])}→{'/'.join(p['kind'] for p in n['outputs'])} "
                     f"[{', '.join(n['capability_ids'][:3])}{'…' if len(n['capability_ids']) > 3 else ''}]{mem}")
        if len(r["nodes"]) > 12:
            L.append(f"  … {len(r['nodes']) - 12} more nodes (--json)")
        L.append(f"edges {len(r['edges'])} · traces {len(r.get('traces') or [])} · evidence {len(r.get('evidence') or [])}"
                 + (" · imported" if r.get("imported") else "") + (" · legacy_unproven" if r.get("legacy_unproven") else ""))
        rc = r.get("recall") or {}
        if rc.get("matches") or rc.get("avoid"):
            L.append("recall: " + " · ".join(f"{m['id']} {m['score']}" for m in rc.get("matches", [])) +
                     (" · avoid " + ", ".join(m["id"] for m in rc.get("avoid", [])) if rc.get("avoid") else ""))
        if r.get("warnings"):
            L.append("warnings: " + ", ".join(r["warnings"][:6]))
        v = res.get("validate")
        if v:
            L.append(f"validate: {'clean' if v['ok'] else 'ERRORS ' + ', '.join(e['code'] + ' ' + e['name'] for e in v['errors'][:4])}"
                     + (f" · {len(v['warnings'])} warning(s)" if v["warnings"] else ""))
        L.append(f"next: {r.get('next_step')}")
        if res.get("path"):
            L.append(f"file: {res['path']}")
    elif cmd == "catalog":
        L.append(f"project {res['project']} · {res['total']} recipe(s) · " + " ".join(f"{k} {v}" for k, v in res["by_status"].items() if v))
        for row in res["recipes"][:18]:
            L.append(f"  {row['id']} {row['status']:<9} nodes {row['nodes']:<2} traces {row['traces']:<3} {clip(row['goal'], 60)}"
                     + (" · reusable" if row.get("reusable") else ""))
        if res["legacy_v1"]:
            L.append(f"legacy v1: {', '.join(res['legacy_v1'][:4])} (run migrate)")
        if res["invalid_files"]:
            L.append(f"invalid files skipped: {', '.join(i['file'] for i in res['invalid_files'][:4])}")
    elif cmd == "validate":
        L.append(f"{res['id']} · {res['status']} · validate {'clean' if res['ok'] else 'ERRORS'}" + (" · reusable" if res.get("reusable") else ""))
        for e in (res["errors"] + res["warnings"])[:16]:
            L.append(f"  {e['level']:<7} {e['code']} {e['name']} {e['where']}: {clip(e['message'], 90)}")
        for n in res["notes"][:3]:
            L.append(f"  note    {n}")
    elif cmd == "lessons":
        L.append(f"lessons for {res['project']}: {res['recipes_scanned']} recipe(s) · " + " ".join(f"{k} {v}" for k, v in res["counts"].items()))
        for l in res["lessons"][:14]:
            L.append(f"  {l['id']} {l['type']:<13} {l['recipe']} {l['node'] or '-'} {l.get('executor') or ''} "
                     f"{l.get('error_class') or l.get('replaced_by') or l.get('outcome') or ''}".rstrip())
        L.append(f"file: {res['path']}")
    elif cmd == "reuse":
        L.append(f"reuse for '{clip(res['goal'], 60)}' in {res['project']} · {res['considered']} recipe(s) considered · brief {res['brief']}")
        L.append(f"  {res['formula']}")
        for m in res["matches"]:
            f = m["factors"]
            L.append(f"  {m['id']} {m['status']:<8} score {m['score']} = sim {f['sim']} x strength {f['strength']} x recency {f['recency']} x freshness {f['freshness']}"
                     + (" · drift" if m["drift"]["remapped"] or m["drift"]["stale"] else "") + (" · reusable" if m.get("reusable") else "")
                     + (" · goal text only" if m.get("sim_basis") == "goal_text_only" else ""))
        for m in res["avoid"][:4]:
            L.append(f"  avoid {m['id']} sim {m['sim']}: " + "; ".join(clip(f"{l['type']} {l.get('executor') or ''} {l.get('note') or l.get('error_class') or ''}", 60) for l in m["lessons"][:2]))
        if not res["matches"] and not res["avoid"]:
            L.append("  no similar recipe in this project (LEARNING_INDEX_EMPTY or no match)")
    elif cmd == "card":
        L.append(f"card {res['id']} ({res['status_at_export']}) · {res['nodes']} nodes · sha {res['card_sha256'][:12]}")
        L.append(f"file: {res['path']}")
    elif cmd == "export":
        L.append(f"bundle: {res['recipes']} recipe(s), {res['lessons']} lesson(s) · " + " ".join(f"{k} {v}" for k, v in res["by_status"].items()))
        L.append(f"file: {res['path']} (redacted; not committed)")
    elif cmd in ("import", "migrate"):
        for k, v in res.items():
            if isinstance(v, list):
                L.append(f"{k}: {len(v)}" + (f" — {', '.join(str(x.get('id') if isinstance(x, dict) else x) for x in v[:5])}" if v else ""))
    elif cmd == "promote":
        L.append(f"promotion proposal: {res['path']}")
        L.append(f"approval: {res['approval'].get('state')} (a human decides; the catalog was not touched) · signature {str(res['graph_signature'])[:12]}")
    elif cmd == "trace":
        t = res["trace"]
        L.append(f"{res['id']} trace #{t['seq']} · {t['stage']} {t['node'] or '-'} {t['result'] or 'noted'} · tool {t['tool']}"
                 + ("" if t.get("tool_reported") or not t.get("node") else " (planned, assumed: pass --tool to report what ran)")
                 + (f" · substitution {t['substitution']['planned']} -> {t['substitution']['used']}" if t.get("substitution") else "")
                 + (f" · evidence {t['evidence']['sha256'][:12]}" if t.get("evidence") else ""))
    else:
        for k, v in res.items():
            if k not in ("root", "markdown") and not isinstance(v, (dict, list)):
                L.append(f"{k}: {v}")
        if res.get("plan_choice"):
            L.append(f"plan {res['plan_choice']['plan']}: {', '.join(res['plan_choice']['nodes'])} — {clip(res['plan_choice']['why'], 80)}")
        if res.get("executor"):
            L.append(f"executor: {res['executor']['ref']} ({res['executor']['runnable']})")
    return "\n".join(L[:25])


# ------------------------------------------------------------------ CLI
WRITING = ("propose", "set-graph", "bind", "choose", "trace", "record", "fork", "lessons", "card", "import-card",
           "export", "import", "migrate", "promote")


def warn_if_tracked(ctx) -> None:
    """Records belong in a git-ignored folder; say so when the root sits inside the checkout without being ignored."""
    if not ctx.git_top or not ctx.root.exists():
        return
    try:
        ctx.root.relative_to(ctx.git_top)
        r = subprocess.run(["git", "check-ignore", "-q", str(ctx.root)], cwd=str(ctx.git_top), capture_output=True, timeout=10)
    except (ValueError, OSError, subprocess.SubprocessError):
        return
    if r.returncode == 1:
        print(f"fusionforge: warning: ROOT_NOT_GITIGNORED: {ctx.root} is inside the git checkout but not ignored; "
              "add it to .gitignore so project records are never committed", file=sys.stderr)


COMMANDS = {"propose": cmd_propose, "show": cmd_show, "catalog": cmd_catalog, "set-graph": cmd_set_graph, "bind": cmd_bind,
            "validate": cmd_validate, "choose": cmd_choose, "trace": cmd_trace, "record": cmd_record, "fork": cmd_fork,
            "lessons": cmd_lessons, "reuse": cmd_reuse, "card": cmd_card, "import-card": cmd_import_card, "export": cmd_export,
            "import": cmd_import, "migrate": cmd_migrate, "promote": cmd_promote}


def build_parser() -> Parser:
    p = Parser(prog="fusionforge.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    common = Parser(add_help=False)
    common.add_argument("--json", action="store_true", help="print the full JSON result")
    for flag, helptext in (("--root", "FusionForge root folder"), ("--catalog-file", "superpowers.json to use"),
                           ("--tools-file", "tools.json to use"), ("--now", "fixed ISO 8601 clock (tests, replays)")):
        p.add_argument(flag, help=helptext)
        common.add_argument(flag, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=Parser)

    def add(name, helptext):
        return sub.add_parser(name, parents=[common], help=helptext, description=helptext)

    def pid(s, rid=True):
        s.add_argument("--project", required=True)
        if rid:
            s.add_argument("--id", required=True)
    s = add("propose", "build a candidate v2 recipe from the USIP brief")
    s.add_argument("goal")
    s.add_argument("--project", required=True)
    s.add_argument("--from-brief")
    s.add_argument("--terms", default="")
    s.add_argument("--max-capabilities", type=int, default=24)
    s.add_argument("--id")
    pid(add("show", "print one recipe (read-only)"))
    pid(add("catalog", "list the project's recipes (read-only)"), rid=False)
    s = add("set-graph", "replace nodes/edges/plans of a candidate after validation")
    pid(s)
    s.add_argument("--file", required=True)
    s = add("bind", "set a node's executor (tool:/bin:/mcp:/method:/human)")
    pid(s)
    s.add_argument("--node", required=True)
    s.add_argument("--executor", required=True)
    pid(add("validate", "check V01-V12; exit 4 on errors"))
    s = add("choose", "record the chosen plan (candidate -> planned)")
    pid(s)
    s.add_argument("--plan", required=True, choices=PLAN_LETTERS)
    s.add_argument("--why", required=True)
    s.add_argument("--nodes")
    s = add("trace", "append one executed step; updates the node status")
    pid(s)
    s.add_argument("--stage", required=True, choices=STAGES)
    s.add_argument("--action", required=True)
    s.add_argument("--node")
    s.add_argument("--result", choices=RESULTS)
    s.add_argument("--tool")
    s.add_argument("--input")
    s.add_argument("--output")
    s.add_argument("--observed")
    s.add_argument("--capabilities", nargs="*")
    s.add_argument("--evidence")
    s.add_argument("--error-class", choices=ERROR_CLASSES)
    s = add("record", "move the recipe status (enforced transitions and verified gate)")
    pid(s)
    s.add_argument("--status", required=True, choices=("planned", "tested", "verified", "failed"))
    s.add_argument("--evidence")
    s.add_argument("--qa-pass", action="store_true")
    s.add_argument("--note")
    s.add_argument("--baseline")
    s = add("fork", "new candidate from any recipe, statuses reset")
    pid(s)
    s.add_argument("--new-id")
    pid(add("lessons", "rebuild <project>/lessons.json from every recipe's traces"), rid=False)
    s = add("reuse", "rank same-project prior recipes for a goal (read-only)")
    s.add_argument("goal")
    s.add_argument("--project", required=True)
    s.add_argument("--top", type=int, default=3)
    s.add_argument("--no-brief", action="store_true")
    s.add_argument("--from-brief")
    s.add_argument("--terms", default="")
    s = add("card", "Markdown card with an embedded kosif.fusionforge.card.v2 JSON block")
    pid(s)
    s.add_argument("--out")
    s = add("import-card", "new candidate from a card")
    s.add_argument("file")
    s.add_argument("--project", required=True)
    s.add_argument("--new-id")
    s = add("export", "redacted bundle for opt-in persistence")
    pid(s, rid=False)
    s.add_argument("--out")
    s.add_argument("--include-candidates", action="store_true")
    s = add("import", "import a bundle of the same project")
    s.add_argument("file")
    s.add_argument("--project", required=True)
    pid(add("migrate", "convert v1 recipes to v2 (backups under legacy/)"), rid=False)
    pid(add("promote", "write a pending_human promotion proposal; never edits the catalog"))
    return p


def main(argv=None) -> int:
    a = ctx = None
    try:
        a = build_parser().parse_args(argv)
        if getattr(a, "project", None) is not None and not SLUG_RX.fullmatch(a.project):
            raise FFError("BAD_PROJECT", "project must be 1-70 letters, digits, '_' or '-'")
        if getattr(a, "project", None) is not None:
            refuse(project=a.project)
        for flag in ("id", "new_id"):
            if getattr(a, flag, None) and not ID_RX.fullmatch(getattr(a, flag)):
                raise FFError("BAD_ID", f"--{flag.replace('_', '-')} must look like FUSE-YYYYMMDD-<10 hex>")
        ctx = Ctx(a)
        res = COMMANDS[a.cmd](ctx, a)
        res = {"root": str(ctx.root), **res}
        if a.cmd in WRITING:
            warn_if_tracked(ctx)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True))
        else:
            print(summary(a.cmd, res, ctx))
        return 0
    except FFError as exc:
        msg = " ".join(str(exc).split())
        if exc.data is not None and ctx is not None:
            exc.data = {"root": str(ctx.root), **exc.data}
        if exc.data is not None and a is not None and getattr(a, "json", False):
            print(json.dumps(exc.data, ensure_ascii=False, indent=1, sort_keys=True))
        elif exc.data is not None and a is not None:
            print(summary(a.cmd, exc.data, None))
        print(f"fusionforge: error: {exc.code}: {msg}", file=sys.stderr)
        return exc.rc
    except KeyboardInterrupt:
        print("fusionforge: error: INTERRUPTED: stopped by the user", file=sys.stderr)
        return 2
    except BrokenPipeError:  # the reader (e.g. | head) closed stdout early; the command itself finished
        with contextlib.suppress(OSError):
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0
    except Exception as exc:  # noqa: BLE001 - one line, never a traceback
        print(f"fusionforge: error: INTERNAL: {type(exc).__name__}: {' '.join(str(exc).split())[:300]}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
