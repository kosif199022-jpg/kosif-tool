#!/usr/bin/env python3
"""KOSIF hub — the one front door to every tool, power and guide in this skill.

One question in, everything relevant out: which tool to run (with a copy-paste command and whether
this machine can run it now), which catalog powers apply, which guide to read and, for motion work,
which reference styles fit. Arabic or English.

    python3 scripts/hub.py find "<task in the user's words>"   # tools + powers + guides (+ styles), ranked
    python3 scripts/hub.py tool <tool-id>                      # one tool: when, commands, requirements, safety, tests, guide
    python3 scripts/hub.py list [--area AREA]                  # every tool, grouped by area
    python3 scripts/hub.py areas                               # the 12 areas and their tools
    python3 scripts/hub.py doctor [--area AREA]                # which tools can run on this machine right now
    python3 scripts/hub.py power <POWER-ID>                    # one catalog record (same data as powers.py show)
    python3 scripts/hub.py docs [words]                        # reference guides, searchable
    python3 scripts/hub.py run <tool-id> [args ...]            # run a tool; asks for --yes first when it needs consent
    python3 scripts/hub.py build [--check]                     # regenerate manifest.json, references/INDEX.md, SKILL.md tool block
    python3 scripts/hub.py mcp-config                          # MCP client config for scripts/kosif_mcp.py on this OS

Add --json to read commands for machine output (apps, agents, the MCP server). Data: data/tools.json
(the curated tool registry, schema kosif.tools.v1) + data/powers/*.json (the catalog). Stdlib only;
read-only except `build` (writes the three generated files) and `run` (runs the chosen tool).
"""
from __future__ import annotations

import argparse
import difflib
import importlib.metadata
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent


def _find_repo():
    """The kosif-tool checkout around this skill, found by a marker file (None for a standalone install)."""
    for cand in list(SKILL.parents)[:4]:
        if (cand / "tools" / "kosif.py").is_file() and (cand / "catalog").is_dir():
            return cand
    return None


REPO = _find_repo()
TOOLS_JSON = SKILL / "data" / "tools.json"
ROUTES_JSON = SKILL / "data" / "capability_routes.json"
MANIFEST = SKILL / "manifest.json"
INDEX_MD = SKILL / "references" / "INDEX.md"
SKILL_MD = SKILL / "SKILL.md"
TOOL_POWERS = SKILL / "data" / "powers" / "runnable-tools.json"
TOOL_FAMILY = "runnable-tools"
POWER_ID_RE = re.compile(r"^TOOL-\d{2,3}$")
SCHEMA = "kosif.tools.v1"
AREAS = ("discover", "think", "motion", "edit", "audio", "draw", "3d", "image", "sources", "investigate", "local-computer", "maintain")
KINDS = ("cli", "library", "mcp-server", "template")
SAFETY = ("read-only", "writes-files", "runs-external-programs", "network")
EVIDENCE = ("tested-here", "tested-elsewhere", "untested")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BLOCK_START, BLOCK_END = "<!-- hub:tools:start -->", "<!-- hub:tools:end -->"
# pip distribution → import name, for the cases where they differ
IMPORT_NAME = {"pillow": "PIL", "opencv-python-headless": "cv2", "opencv-python": "cv2", "python-pptx": "pptx",
               "fonttools": "fontTools", "python-bidi": "bidi", "arabic-reshaper": "arabic_reshaper",
               "faster-whisper": "faster_whisper", "scikit-learn": "sklearn", "pyyaml": "yaml", "beautifulsoup4": "bs4",
               "python-docx": "docx", "openai-whisper": "whisper", "yt-dlp": "yt_dlp", "playwright": "playwright"}

sys.path.insert(0, str(HERE))
import powers as P  # noqa: E402  (catalog loader, Arabic-aware normalisation, suggest())


# ------------------------------------------------------------------ registry
def load_registry(path: Path = TOOLS_JSON, check_files: bool = False) -> dict:
    """Load and validate data/tools.json. File checks are off by default so a standalone
    install (no repo around the skill) still loads; builds and check_skill.py turn them on."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_registry(data, check_files=check_files)
    if errors:
        raise ValueError(f"{path.name}: " + "; ".join(errors[:5]) + (" …" if len(errors) > 5 else ""))
    return data


def validate_registry(data: dict, check_files: bool = True) -> list:
    """Structural checks for data/tools.json; returns a list of problems (empty = valid)."""
    errs = []
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        return [f"schema must be {SCHEMA}"]
    areas = data.get("areas")
    if not isinstance(areas, list) or [a.get("id") for a in areas if isinstance(a, dict)] != list(AREAS):
        errs.append("areas must list exactly: " + ", ".join(AREAS))
    tools = data.get("tools")
    if not isinstance(tools, list) or not tools:
        return errs + ["tools must be a non-empty list"]
    seen = set()
    power_ids = Counter(t.get("power_id") for t in tools if isinstance(t, dict) and t.get("power_id"))
    for pid, n in power_ids.items():
        if not POWER_ID_RE.match(str(pid)):
            errs.append(f"power_id {pid} must look like TOOL-NN")
        if n > 1:
            errs.append(f"power_id {pid} is used by {n} tools")
    for t in tools:
        if not isinstance(t, dict):
            errs.append("tool entry must be an object"); continue
        tid = t.get("id", "?")
        if not isinstance(tid, str) or not ID_RE.match(tid) or tid in seen:
            errs.append(f"{tid}: id must be unique kebab-case")
        seen.add(tid)
        for key in ("title_en", "title_ar", "summary_en", "summary_ar", "inputs", "outputs", "limits"):
            if not isinstance(t.get(key), str) or not t.get(key).strip():
                errs.append(f"{tid}: {key} must be a non-empty string")
        if t.get("root") not in ("skill", "repo"):
            errs.append(f"{tid}: root must be skill or repo")
        for key, allowed in (("kind", KINDS), ("area", AREAS), ("safety", SAFETY), ("evidence", EVIDENCE)):
            if t.get(key) not in allowed:
                errs.append(f"{tid}: {key} must be one of {allowed}")
        for key in ("use_when", "keywords", "commands", "families", "tests", "docs"):
            if not isinstance(t.get(key), list):
                errs.append(f"{tid}: {key} must be a list")
        if isinstance(t.get("use_when"), list) and len(t["use_when"]) < 2:
            errs.append(f"{tid}: use_when needs at least 2 requests")
        if isinstance(t.get("keywords"), list) and len(t["keywords"]) < 4:
            errs.append(f"{tid}: keywords needs at least 4 entries")
        if not t.get("commands"):
            errs.append(f"{tid}: at least one command")
        for c in t.get("commands") or []:
            if not (isinstance(c, dict) and c.get("name") and c.get("example") and c.get("does")):
                errs.append(f"{tid}: every command needs name, example and does")
        req = t.get("requires")
        if not isinstance(req, dict) or not all(isinstance(req.get(k), list) for k in ("python", "binaries", "node", "optional")) \
                or not isinstance(req.get("network"), bool):
            errs.append(f"{tid}: requires needs python/binaries/node/optional lists and a network boolean")
        sc = t.get("safe_commands", [])
        if not isinstance(sc, list) or not all(isinstance(x, str) and re.fullmatch(r"[\w-]+", x) for x in sc):
            errs.append(f"{tid}: safe_commands must be a list of subcommand words")
        if not isinstance(t.get("consent"), str):
            errs.append(f"{tid}: consent must be a string (empty when nothing needs approval)")
        if check_files:
            base = root_dir(t)
            if base is not None and not (base / t.get("path", "")).exists():
                errs.append(f"{tid}: path {t.get('path')} does not exist")
            for rel in (t.get("tests") or []) + (t.get("docs") or []):
                if REPO is not None and not (REPO / rel).exists():
                    errs.append(f"{tid}: listed file {rel} does not exist")
        known = (set(P.FAMILY_META) | {p.stem for p in (SKILL / "data" / "powers").glob("*.json")}) - {TOOL_FAMILY}
        for fam in t.get("families") or []:
            if fam not in known:
                errs.append(f"{tid}: unknown family {fam}")
    return errs


def root_dir(tool: dict):
    return SKILL if tool.get("root") == "skill" else REPO


def tools_by_id(reg: dict) -> "OrderedDict[str, dict]":
    return OrderedDict((t["id"], t) for t in reg["tools"])


def area_title(reg: dict, area: str) -> tuple:
    for a in reg["areas"]:
        if a["id"] == area:
            return a.get("ar", area), a.get("en", area)
    return area, area


# ------------------------------------------------------------------ presence (read-only, no subprocess)
def pip_present(dist: str) -> bool:
    name = dist.split("==")[0].split(">=")[0].strip()
    try:
        importlib.metadata.version(name)
        return True
    except importlib.metadata.PackageNotFoundError:
        pass
    mod = IMPORT_NAME.get(name.lower(), name.replace("-", "_"))
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


def npm_present(pkg: str) -> bool:
    roots = [Path.cwd(), SKILL] + ([REPO] if REPO else [])
    return any((r / "node_modules" / pkg).exists() for r in roots) or bool(shutil.which(pkg))


def bin_present(name: str) -> bool:
    if name in ("chromium", "chrome"):
        pw = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "")
        return bool(shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
                    or (pw and Path(pw).exists()))
    if name in ("python3", "python"):
        return True
    return bool(shutil.which(name))


def readiness(tool: dict) -> dict:
    req = tool.get("requires") or {}
    missing = [f"pip:{d}" for d in req.get("python", []) if not pip_present(d)]
    missing += [f"bin:{b}" for b in req.get("binaries", []) if not bin_present(b)]
    missing += [f"npm:{n}" for n in req.get("node", []) if not npm_present(n)]
    opt_missing = []
    for o in req.get("optional", []):
        kind, _, name = o.partition(":") if ":" in o else ("pip", "", o)
        ok = {"pip": pip_present, "bin": bin_present, "npm": npm_present}.get(kind, lambda _n: False)(name)
        if not ok:
            opt_missing.append(o)
    if root_dir(tool) is None:
        state = "unavailable"  # a repo tool while the skill is installed on its own
    else:
        state = "ready" if not missing else "missing"
    return {"state": state, "missing": missing, "optional_missing": opt_missing}


# ------------------------------------------------------------------ text and ranking
def _norm(s) -> str:
    return P.norm(s if isinstance(s, str) else json.dumps(s, ensure_ascii=False))


def terms_of(brief: str) -> list:
    words = re.findall(r"[\w:+#.-]+", brief)
    out = []
    for w in P.expand(words, brief):
        if w[:1] in "@~!":
            out.append(w)
            continue
        n = _norm(w).strip(".-")
        if len(n) >= 2 and n not in P.STOP:
            out.append(n)
    return list(OrderedDict.fromkeys(out))


def _hit(term: str, text: str) -> bool:
    if len(term) <= 2:
        return re.search(rf"(?<![\w]){re.escape(term)}(?![\w])", text) is not None
    if term in text:
        return True
    for pre in P._AR_PREFIXES:  # Arabic clitics: والرسم → رسم
        if term.startswith(pre) and len(term) - len(pre) >= 3 and term[len(pre):] in text:
            return True
    return False


_TOOL_TEXT = {}


def tool_text(t: dict) -> tuple:
    if t["id"] not in _TOOL_TEXT:
        strong = _norm(" ".join([t["title_en"], t["title_ar"], " ".join(t["keywords"]), " ".join(t["use_when"]), t["id"].replace("-", " ")]))
        normal = _norm(" ".join([t["summary_en"], t["summary_ar"], t["inputs"], t["outputs"], t["area"], " ".join(t["families"]),
                                 " ".join(c["name"] + " " + c["does"] for c in t["commands"])]))
        _TOOL_TEXT[t["id"]] = (strong, normal)
    return _TOOL_TEXT[t["id"]]


def load_routes() -> list:
    try:
        return json.loads(ROUTES_JSON.read_text(encoding="utf-8")).get("routes", [])
    except (OSError, ValueError):
        return []


def rank_tools(reg: dict, brief: str, terms: list, power_families: Counter, limit: int = 6, prefix_family: dict = None) -> list:
    nbrief = " " + _norm(brief) + " "
    route_boost = Counter()
    for r in load_routes():
        script = str(r.get("script", ""))
        if any(len(_norm(a)) >= 3 and _norm(a) in nbrief for a in r.get("aliases", [])):
            route_boost[script] += 1
    fam_intent = {t[1:].upper() for t in terms if t.startswith("@")}
    if prefix_family is None:  # motion prefixes (CHAR, 3D, TRANS …) live only in the catalog data
        prefix_family = {P.prefix_of(p): p["family"] for p in P.load_powers()}
    scored = []
    for t in reg["tools"]:
        strong, normal = tool_text(t)
        s = 0.0
        for w in terms:
            if w[:1] in "@~!":
                continue
            if _hit(w, strong):
                s += 3.0
            elif _hit(w, normal):
                s += 1.0
        if s <= 0:
            continue
        fams = set(t["families"])
        s += min(3.0, 1.0 * sum(1 for f in fams if power_families.get(f)))
        s += 1.5 * sum(1 for p in fam_intent if prefix_family.get(p) in fams)
        if route_boost.get(t["path"]):
            s += 2.0
        s += {"tested-here": 0.3, "tested-elsewhere": 0.1}.get(t["evidence"], 0.0)
        scored.append((round(s, 2), t))
    scored.sort(key=lambda x: (-x[0], x[1]["id"]))
    return scored[:limit]


def explain_tool_match(tool: dict, terms: list) -> dict:
    """Return a compact, deterministic explanation of why a tool matched.

    The scorer used to expose only a number.  Agents could not tell which request
    words produced that number, and therefore could not distinguish a strong
    semantic match from a catalog accident.  Keep this explanation derived from
    the exact same strong/normal fields used by ``rank_tools``.
    """
    strong, normal = tool_text(tool)
    strong_hits, normal_hits = [], []
    for term in terms:
        if term[:1] in "@~!":
            continue
        if _hit(term, strong):
            strong_hits.append(term)
        elif _hit(term, normal):
            normal_hits.append(term)
    return {
        "matched_terms": list(OrderedDict.fromkeys(strong_hits + normal_hits))[:12],
        "strong_terms": list(OrderedDict.fromkeys(strong_hits))[:12],
    }


def execution_plan(tool_results: list) -> dict:
    """Turn ranked tool cards into an honest ready-now / blocked execution plan."""
    ready = [t for t in tool_results if t["readiness"]["state"] == "ready"]
    blocked = [t for t in tool_results if t["readiness"]["state"] != "ready"]
    unlocks = Counter(req for t in blocked for req in t["readiness"].get("missing", []))
    return {
        "primary": ready[0]["id"] if ready else None,
        "ready_now": [t["id"] for t in ready],
        "blocked": [{"id": t["id"], "missing": t["readiness"].get("missing", [])} for t in blocked],
        "best_unlocks": [{"requirement": req, "tools_unlocked": count}
                         for req, count in sorted(unlocks.items(), key=lambda item: (-item[1], item[0]))[:8]],
    }


# ------------------------------------------------------------------ guides
def doc_entries(reg: dict = None) -> list:
    """Every reference guide (references/*.md, not the generated family chapters) with its title and area."""
    curated = {d["path"]: d for d in (reg or {}).get("docs", [])} if reg else {}
    area_votes = {}
    for t in (reg or {}).get("tools", []):
        for d in t.get("docs", []):
            area_votes.setdefault(d, Counter())[t["area"]] += 1
    out = []
    # pathlib path ordering differs between Windows (casefolded) and POSIX; make generated docs deterministic.
    order = lambda p: (p.name.casefold(), p.name)
    files = sorted((SKILL / "references" / "guides").glob("*.md"), key=order) + sorted((SKILL / "references").glob("*.md"), key=order)
    for p in files:
        if p.name == "INDEX.md":
            continue
        rel = p.relative_to(SKILL).as_posix()
        rel_repo = ".claude/skills/kosif-superpowers/" + rel
        text = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"(?m)^#\s+(.+)$", text)
        title = m.group(1).strip() if m else p.stem
        heads = re.findall(r"(?m)^##\s+(.+)$", text)
        cur = curated.get(rel, {})
        votes = area_votes.get(rel_repo)
        area = cur.get("area") or (p.stem if p.parent.name == "guides" and p.stem in AREAS else None) \
            or (votes.most_common(1)[0][0] if votes else "general")
        out.append({"path": rel, "title": title, "area": area, "summary": cur.get("summary", ""),
                    "headings": heads[:40], "lines": text.count("\n") + 1})
    return out


def rank_docs(docs: list, terms: list, limit: int = 4) -> list:
    scored = []
    for d in docs:
        head = _norm(d["title"] + " " + d["summary"] + " " + d["path"])
        body = _norm(" ".join(d["headings"]))
        s = sum(2.0 if _hit(w, head) else 0.7 if _hit(w, body) else 0.0 for w in terms if w[:1] not in "@~!")
        if s > 0:
            scored.append((round(s, 2), d))
    scored.sort(key=lambda x: (-x[0], x[1]["path"]))
    return scored[:limit]


def _guides_for(tools: list, entries: list, terms: list, limit: int = 4) -> list:
    """The guides of the best tools come first (they document exactly what to run); text matches fill the rest."""
    by_path = {d["path"]: d for d in entries}
    out, seen = [], set()
    for s, t in tools:
        for rel in t.get("docs", []):
            key = rel.split("kosif-superpowers/", 1)[-1]
            if key in by_path and key not in seen:
                seen.add(key)
                out.append((s, by_path[key]))
    for s, d in rank_docs(entries, terms, limit=limit + len(seen)):
        if d["path"] not in seen:
            seen.add(d["path"])
            out.append((s, d))
    return out[:limit]


# ------------------------------------------------------------------ command display
SKILL_DIRS = ("scripts", "templates", "resources", "assets", "evals", "data", "references", "examples", "proofs", "vendor")
REPO_DIRS = ("tools", "starters", "styles", "playbooks", "templates", "tests", "catalog", "projects", "docs", "fonts")


def shown(example: str, tool: dict, cwd: Path = None) -> str:
    """Rewrite a registered example (typed from its root) so it runs from the caller's cwd."""
    base = root_dir(tool)
    if base is None:
        return example
    cwd = (cwd or Path.cwd()).resolve()
    if cwd == base.resolve():
        return example
    try:
        prefix = os.path.relpath(base, cwd).replace(os.sep, "/")
    except ValueError:
        prefix = base.as_posix()
    if re.search(r"[^\w./:+@-]", prefix):  # spaces or shell characters: run it from its root instead
        return f"cd {shlex.quote(str(base))} && {example}"
    dirs = SKILL_DIRS if tool["root"] == "skill" else REPO_DIRS
    # one pass, so the inserted prefix (which may itself start with ../) is never rewritten again
    pat = r"(?<![\w./-])(?:(?:\./)?(" + "|".join(dirs) + r")/|((?:\.\./)+))"
    return re.sub(pat, lambda m: f"{prefix}/{m.group(1)}/" if m.group(1) else f"{prefix}/{m.group(2)}", example)


def tool_card(t: dict, reg: dict, full: bool = True) -> dict:
    card = OrderedDict((k, t[k]) for k in ("id", "title_en", "title_ar", "area", "kind", "summary_en", "summary_ar", "path", "root"))
    card["run_from"] = str(root_dir(t)) if root_dir(t) else None
    card["readiness"] = readiness(t)
    card["first_command"] = t["commands"][0]["example"]
    if full:
        for k in ("use_when", "keywords", "commands", "inputs", "outputs", "requires", "safety", "consent", "limits",
                  "evidence", "evidence_note", "tests", "docs", "families"):
            card[k] = t.get(k)
    return card


# ------------------------------------------------------------------ find
AREA_NEEDS_WORDS = {  # matched on the normalised request + --terms
    "3d": r"3d|3-d|ثلاثي|ثري ?دي|تري ?دي|بلندر|blender|\bglb\b|gltf|three|webgl|low.?poly|\bmesh(?:es)?\b|turntable|ray ?trac|مجسم|موديل (?:ثلاثي|ثري|3d)|نموذج ثلاثي",
    "audio": r"صوت|موسيق|مزيك|اغني|اغان|نشيد|اناشيد|تلاوه|قران|بودكاست|ايقاع|بيت|audio|\bsounds?\b|\bvoice(?:over)?s?\b|narrat(?:ion|or)|music|\bsongs?\b|podcast|nasheed|\bbeats?\b|\btracks?\b|\bsfx\b|\bmp3\b|\bwav\b|caption|subtitle|\bsrt\b|\bvtt\b|words\.json|lyric|ترجمه|توقيت|تفريغ",
    "draw": r"رسم|ارسم|رسوم|شخصي|كرتون|كاريكاتير|اسكتش|draw|sketch|paint|illustrat|character|cartoon|doodle|mascot|ماسكوت",
}
TOOL_NEEDS_WORDS = {  # tools that act on third-party sites or need consent: only when the request asks for that
    "web-app-study": r"حلل|ادرس|افحص|استكشف|\bstudy\b|analy[sz]|inspect|built with|tech ?stack|مبني ب|معمول ب|منافس|competitor|reverse",
}


def _norm_ar(s: str) -> str:
    s = re.sub(r"[\u064b-\u0652\u0640]", "", (s or "").lower())
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


def off_request(tool: dict, brief: str) -> bool:
    """A specialised (3D, audio, drawing) or consent-heavy tool that the request does not ask for."""
    text = _norm_ar(brief)
    area_rx = AREA_NEEDS_WORDS.get(tool.get("area"))
    tool_rx = TOOL_NEEDS_WORDS.get(tool.get("id"))
    return bool((area_rx and not re.search(area_rx, text)) or (tool_rx and not re.search(tool_rx, text)))


def find(brief: str, limit_tools: int = 5, limit_powers: int = 10, reg: dict = None, powers: list = None) -> dict:
    reg = reg or load_registry()
    pw = powers if powers is not None else P.load_powers()
    styles = P.load_styles()
    sug = P.suggest(pw, styles, brief, limit=max(limit_powers, 12))
    terms = terms_of(brief)
    power_fams = Counter(p.get("family") for _s, p in sug["picked"])
    tools = rank_tools(reg, brief, terms, power_fams, limit_tools + 6, {P.prefix_of(p): p["family"] for p in pw})
    tools = sorted(tools, key=lambda st: off_request(st[1], brief))[:limit_tools]   # stable: relevant tools first
    entries = doc_entries(reg)
    docs = _guides_for(tools, entries, terms)
    fam_chapters = [f"references/powers/{f}.md" for f in sug["chapters"][:4]]
    out = OrderedDict()
    out["brief"] = brief
    out["tools"] = [dict(tool_card(t, reg, full=False), score=s, **explain_tool_match(t, terms), docs=t["docs"][:2],
                         safety=t["safety"], consent=t["consent"], evidence=t["evidence"]) for s, t in tools]
    out["execution_plan"] = execution_plan(out["tools"])
    out["powers"] = [dict(P.short(p, s), when=p.get("when", ""), family=p.get("family")) for s, p in sug["picked"][:limit_powers]]
    out["guides"] = [{"path": d["path"], "title": d["title"], "score": s} for s, d in docs]
    out["family_chapters"] = fam_chapters
    out["styles"] = [{"id": s.get("id"), "name": s.get("title_ar") or s.get("name") or s.get("title", ""), "genre": s.get("genre", "")}
                     for s in sug["styles"][:5]]
    out["motion"] = sug["motion"]
    out["hints"] = [P.HINTS[h] for h in sug["hints"] if h in P.HINTS]
    out["superskills"] = superskills_for(brief)
    # SEE stays a method layer inside the one existing hub, not another registry.
    try:
        from see_superpower_unifier import fuse as _see_fuse
        _see_mode = ("full_pro" if re.search(r"(?i)full[ -]?pro|وضع البرو|قصيف برو", brief)
                     else "deep" if re.search(r"(?i)\bdeep\b|فكر بعمق|فكّر بعمق", brief)
                     else "standard")
        out["see_fusion"] = _see_fuse(brief, out, mode=_see_mode)
    except (ImportError, TypeError, ValueError) as exc:
        out["see_fusion"] = {"status": "UNAVAILABLE", "reason": type(exc).__name__}
    nxt = []
    if tools:
        nxt.append(f"python3 scripts/hub.py tool {tools[0][1]['id']}")
    if sug["picked"]:
        nxt.append(f"python3 scripts/powers.py show {sug['picked'][0][1]['id']}")
    nxt.append("python3 scripts/requirements.py plan " + shlex.quote(brief))
    out["next"] = nxt
    return out


def superskills_for(brief: str, limit: int = 3, min_score: float = 2.0) -> list:
    """The owner's 114 vendored super skills (vendor/100-superskills) that fit the brief; [] when not vendored."""
    try:
        import superskills as SS  # noqa: E402  (stdlib; reads data/superskills.json)
        if not SS.DATA.is_file():
            return []
        return [{"slug": r["slug"], "title_ar": r["title_ar"], "title_en": r["title_en"], "score": sc,
                 "path": r["path"] + "/SKILL.md", "show": f"python3 scripts/superskills.py show {r['slug']}"}
                for sc, r in SS.find(brief, limit) if sc >= min_score]
    except Exception:   # never let the optional layer break the front door
        return []


# ------------------------------------------------------------------ output helpers
def emit(obj) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")


def state_mark(r: dict) -> str:
    return {"ready": "✓ ready", "missing": "✗ needs " + ", ".join(r["missing"][:4]), "unavailable": "· repo checkout only"}[r["state"]]


def cmd_find(a) -> int:
    reg = load_registry()
    res = find(a.brief, a.tools, a.limit, reg)
    if a.json:
        emit(res); return 0
    by = tools_by_id(reg)
    print(f"KOSIF hub · find: {a.brief}\n")
    print("▶ أدوات للتشغيل / tools to run")
    if not res["tools"]:
        print("  (no executable tool matched — use the powers and guides below, or: python3 scripts/hub.py list)")
    for i, t in enumerate(res["tools"], 1):
        tool = by[t["id"]]
        print(f"  {i}. {t['id']} — {t['title_en']} / {t['title_ar']}  [{t['area']} · {state_mark(t['readiness'])}]")
        print(f"     {t['summary_en']}")
        if t.get("matched_terms"):
            print("     why: " + ", ".join(t["matched_terms"]))
        print(f"     $ {shown(t['first_command'], tool)}")
        extra = []
        if t["docs"]:
            extra.append("guide: " + t["docs"][0].split("kosif-superpowers/")[-1])
        if t["consent"]:
            extra.append("consent: " + t["consent"])
        if extra:
            print("     " + " · ".join(extra))
    print("\n◆ قدرات من الكتالوج / catalog powers")
    for p in res["powers"]:
        print(f"  {p['id']:<10} {P.BADGE.get(p['status'], '·')} {p['name_ar']} — {p['name_en']}")
    if res["guides"] or res["family_chapters"]:
        print("\n📖 أدلة / guides")
        for g in res["guides"]:
            print(f"  {g['path']} — {g['title']}")
        print("  chapters: " + " · ".join(res["family_chapters"]))
    if res["motion"] and res["styles"]:
        print("\n🎨 أساليب مرجعية / reference styles")
        for s in res["styles"]:
            print(f"  {s['id']}  {s['name']}")
    if res.get("superskills"):
        print("\n★ مهارات خارقة كاملة / super skills (100-superskills, read the SKILL.md and follow it)")
        for k in res["superskills"]:
            print(f"  {k['slug']:<34} {k['title_ar']} — {k['title_en']}")
            print(f"     $ {shown(k['show'], {'root': 'skill'})}")
    fusion = res.get("see_fusion") or {}
    if fusion.get("status") == "PLAN_ONLY":
        print("\n🧠 SEE × Superpowers — unified reasoning route")
        print("  lenses: 11 available · SEE domains: 9 mapped · loaded method candidates: "
              + ", ".join(m["name"] for m in fusion["selected_see_methods"]))
        print("  execution: NOT_RUN · verification: NOT_RUN"
              + (" · Full Pro: NOT_FULL_PRO" if fusion["full_pro"]["requested"] else ""))
    for h in res["hints"]:
        print(f"\nhint: {h}")
    plan = res.get("execution_plan", {})
    if plan.get("primary"):
        print(f"\nready now: {plan['primary']} (primary)" +
              (" · alternatives: " + ", ".join(plan["ready_now"][1:]) if len(plan.get("ready_now", [])) > 1 else ""))
    elif plan.get("blocked"):
        print("\nready now: none of the matched tools; inspect best_unlocks in --json before installing anything")
    q = shlex.quote(a.brief)
    print("\nnext: " + " · ".join(shown(n[: -len(q)], {"root": "skill"}) + q if n.endswith(" " + q) else shown(n, {"root": "skill"})
                                   for n in res["next"]))
    print("badges: ✅ proven · 🟢 ready · 📦 install · 🔑 key · 👁 seen · 📄 documented · 💡 idea — claim the lowest true one.")
    return 0


def cmd_tool(a) -> int:
    reg = load_registry()
    by = tools_by_id(reg)
    name = a.id.strip()
    t = by.get(name) or (next((x for x in reg["tools"] if name and (Path(x["path"].rstrip("/")).name == name
                                                                    or Path(x["path"].rstrip("/")).stem == name)), None))
    if not t:
        close = [i for i in by if a.id.lower() in i]
        print(f"no tool '{a.id}'" + (f"; did you mean: {', '.join(close[:6])}" if close else "; see: python3 scripts/hub.py list"), file=sys.stderr)
        return 1
    card = tool_card(t, reg)
    if a.json:
        emit(card); return 0
    ar, en = area_title(reg, t["area"])
    print(f"{t['id']} — {t['title_en']} / {t['title_ar']}")
    print(f"area: {en} / {ar} · kind: {t['kind']} · file: {t['path']} ({t['root']}) · evidence: {t['evidence']}")
    print(f"\n{t['summary_en']}\n{t['summary_ar']}")
    print("\nuse when / استخدمها حين:")
    for u in t["use_when"]:
        print(f"  - {u}")
    print("\ncommands:")
    for c in t["commands"]:
        print(f"  {c['name']}: {c['does']}\n    $ {shown(c['example'], t)}")
    print(f"\ninputs: {t['inputs']}\noutputs: {t['outputs']}")
    r = card["readiness"]
    req = t["requires"]
    print(f"\nrequires: python {req['python'] or '-'} · binaries {req['binaries'] or '-'} · node {req['node'] or '-'}"
          f" · network {'yes' if req['network'] else 'no'}{' · optional ' + str(req['optional']) if req['optional'] else ''}")
    print(f"on this machine: {state_mark(r)}" + (f" (optional missing: {', '.join(r['optional_missing'])})" if r["optional_missing"] else ""))
    print(f"safety: {t['safety']}" + (f" · consent: {t['consent']}" if t["consent"] else ""))
    print(f"limits: {t['limits']}")
    if t.get("evidence_note"):
        print(f"evidence: {t['evidence_note']}")
    if t["tests"]:
        print("tests: " + " · ".join(t["tests"]))
    if t["docs"]:
        print("guides: " + " · ".join(t["docs"]))
    if t["families"]:
        print("powers: " + " · ".join(f"references/powers/{f}.md" for f in t["families"]))
    return 0


def cmd_list(a) -> int:
    reg = load_registry()
    rows = [t for t in reg["tools"] if not a.area or t["area"] == a.area]
    if a.json:
        emit([tool_card(t, reg, full=False) for t in rows]); return 0
    for area in AREAS:
        group = [t for t in rows if t["area"] == area]
        if not group:
            continue
        ar, en = area_title(reg, area)
        print(f"\n## {en} / {ar} ({len(group)})")
        for t in group:
            print(f"  {t['id']:<30} {t['title_en']} — {t['summary_en'][:90]}")
    print(f"\n{len(rows)} tools · details: python3 scripts/hub.py tool <id>")
    return 0


def cmd_areas(a) -> int:
    reg = load_registry()
    out = [{"id": x["id"], "ar": x["ar"], "en": x["en"], "about": x.get("about", ""),
            "tools": [t["id"] for t in reg["tools"] if t["area"] == x["id"]]} for x in reg["areas"]]
    if a.json:
        emit(out); return 0
    for x in out:
        print(f"{x['id']:<15} {x['en']} / {x['ar']} — {', '.join(x['tools'])}")
    return 0


def cmd_doctor(a) -> int:
    reg = load_registry()
    rows = [t for t in reg["tools"] if not a.area or t["area"] == a.area]
    res = [{"id": t["id"], "area": t["area"], **readiness(t)} for t in rows]
    unlock = Counter(m for r in res for m in r["missing"])
    summary = {"tools": len(res), "ready": sum(r["state"] == "ready" for r in res),
               "missing": sum(r["state"] == "missing" for r in res), "unavailable": sum(r["state"] == "unavailable" for r in res),
               "biggest_unlocks": unlock.most_common(8)}
    if a.json:
        emit({"summary": summary, "tools": res}); return 0
    print(f"KOSIF hub doctor · {summary['ready']}/{summary['tools']} tools ready on this machine"
          + (f" · {summary['unavailable']} need the full repository" if summary["unavailable"] else ""))
    for r in res:
        if r["state"] != "ready":
            print(f"  {r['id']:<30} {state_mark(r)}")
    if unlock:
        print("\nbiggest unlocks (ask before installing):")
        for k, n in unlock.most_common(8):
            print(f"  +{n:<3} {k}")
    return 0


def cmd_power(a) -> int:
    return P.main(["show", a.id] + (["--json"] if a.json else []))


def cmd_docs(a) -> int:
    reg = load_registry()
    docs = doc_entries(reg)
    rows = [d for _s, d in rank_docs(docs, terms_of(" ".join(a.words)), limit=20)] if a.words else docs
    if a.json:
        emit(rows); return 0
    for d in rows:
        print(f"{d['path']:<58} [{d['area']}] {d['title']}")
    print(f"\n{len(rows)} guide(s). Family chapters: references/powers/<family>.md · full index: references/INDEX.md")
    return 0


def cmd_run(a, extra: list) -> int:
    reg = load_registry()
    t = tools_by_id(reg).get(a.id)
    if not t:
        print(f"no tool '{a.id}' (python3 scripts/hub.py list)", file=sys.stderr); return 1
    base = root_dir(t)
    if base is None:
        print(f"{t['id']} lives in the full kosif-tool repository, not in a standalone skill install.", file=sys.stderr); return 1
    target = base / t["path"]
    if target.is_dir() or t["kind"] in ("library", "template"):
        print(f"{t['id']} is a {t['kind'] if not target.is_dir() else 'folder'}; run one of its commands directly:", file=sys.stderr)
        for c in t["commands"]:
            print(f"  $ {shown(c['example'], t)}", file=sys.stderr)
        return 2
    # --help, or a subcommand the registry lists as read-only whatever its arguments, needs no approval
    harmless = bool(extra) and (set(extra) <= {"--help", "-h"} or extra[0] in (t.get("safe_commands") or []))
    if (t["consent"] or t["safety"] in ("network", "runs-external-programs")) and not a.yes and not harmless:
        print(f"{t['id']} needs approval first: {t['consent'] or t['safety']}\nRe-run with --yes once the user has agreed.", file=sys.stderr)
        return 3
    runner = {".py": [sys.executable], ".cjs": ["node"], ".mjs": ["node"], ".js": ["node"], ".sh": ["bash"]}.get(target.suffix)
    if not runner:
        print(f"don't know how to run {target.name}", file=sys.stderr); return 2
    return subprocess.call(runner + [str(target)] + extra)


# ------------------------------------------------------------------ generated files
def families_summary() -> list:
    pw = P.load_powers()
    out = []
    for fam, rows in sorted(Counter(p["family"] for p in pw).items()):
        recs = [p for p in pw if p["family"] == fam]
        ttl = P.family_title(fam)
        st = Counter(p.get("status") for p in recs)
        out.append(OrderedDict([("key", fam), ("prefix", P.prefix_of(recs[0])), ("domain", recs[0].get("domain") or P.DEFAULT_DOMAIN),
                                ("title_ar", ttl[0] if isinstance(ttl, tuple) else ""), ("title_en", ttl[1] if isinstance(ttl, tuple) else fam),
                                ("count", rows), ("statuses", dict(sorted(st.items()))),
                                ("chapter", f"references/powers/{fam}.md"), ("data", f"data/powers/{fam}.json")]))
    return out


def frontmatter_description() -> str:
    m = re.search(r"(?m)^description:\s*(.+)$", SKILL_MD.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else ""


def build_manifest(reg: dict) -> str:
    fams = families_summary()
    docs = doc_entries(reg)
    statuses = Counter()
    for f in fams:
        statuses.update(f["statuses"])
    data = OrderedDict()
    data["schema"] = "kosif.manifest.v1"
    data["generated_by"] = "scripts/hub.py build — edit data/tools.json and data/powers/*.json, never this file"
    data["name"] = "kosif-superpowers"
    data["description"] = frontmatter_description()
    data["entrypoints"] = OrderedDict([
        ("boot", "python3 scripts/boot.py"),
        ("find", 'python3 scripts/hub.py find "<task>" --json'),
        ("tool", "python3 scripts/hub.py tool <tool-id> --json"),
        ("doctor", "python3 scripts/hub.py doctor --json"),
        ("power", "python3 scripts/powers.py show <POWER-ID> --json"),
        ("mcp_server", "python3 scripts/kosif_mcp.py"),
        ("skill", "SKILL.md"), ("index", "references/INDEX.md"),
    ])
    data["paths_note"] = "Tool paths and examples are relative to their root: 'skill' = this folder, 'repo' = the kosif-tool repository root."
    data["counts"] = OrderedDict([("powers", sum(f["count"] for f in fams)), ("families", len(fams)),
                                  ("domains", len({f["domain"] for f in fams})), ("tools", len(reg["tools"])),
                                  ("guides", len(docs)), ("statuses", dict(sorted(statuses.items())))])
    data["evidence_badges"] = {s: P.BADGE[s] for s in P.STATUSES}
    data["areas"] = reg["areas"]
    data["domains"] = [{"key": k, "ar": v[0], "en": v[1]} for k, v in P.DOMAINS.items()]
    data["families"] = fams
    data["tools"] = reg["tools"]
    data["guides"] = [{k: d[k] for k in ("path", "title", "area", "summary")} for d in docs]
    return json.dumps(data, ensure_ascii=False, indent=1) + "\n"


def md_cell(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def build_index(reg: dict) -> str:
    fams = families_summary()
    docs = doc_entries(reg)
    total = sum(f["count"] for f in fams)
    L = ["# فهرس المهارة — KOSIF Superpowers index", "",
         "<!-- generated by scripts/hub.py build from data/tools.json, data/powers/*.json and references/*.md — do not edit by hand -->", "",
         f"كل ما في المهارة في صفحة واحدة: {len(reg['tools'])} أداة تُشغَّل في 12 مجالًا، و{len(docs)} دليلًا، و{total:,} قدرة في {len(fams)} عائلة. "
         f"Everything in the skill on one page: {len(reg['tools'])} runnable tools in 12 areas, {len(docs)} guides and {total:,} catalog powers in {len(fams)} families.", "",
         "## الفهرس / contents", "",
         "1. [Find anything in three commands](#find-anything-in-three-commands)",
         "2. [Tools by area](#tools-by-area)",
         "3. [Guides by area](#guides-by-area)",
         "4. [Power families](#power-families)", "",
         "## Find anything in three commands", "",
         "Paths are relative to the skill folder (`.claude/skills/kosif-superpowers/`); `repo` tools run from the repository root.", "",
         "```bash",
         'python3 scripts/hub.py find "<the task in the user\'s words>"   # tools + powers + guides, Arabic or English',
         "python3 scripts/hub.py tool <tool-id>                          # commands, requirements, safety, tests",
         "python3 scripts/hub.py doctor                                  # what runs on this machine now",
         "```", "",
         "Any MCP client can ask the same questions: `python3 scripts/kosif_mcp.py` (read-only stdio server; `python3 scripts/hub.py mcp-config`).",
         "Machine-readable: [manifest.json](../manifest.json) (everything below as JSON) and [data/tools.json](../data/tools.json) (the editable registry).", "",
         "## Tools by area", ""]
    for area in reg["areas"]:
        group = [t for t in reg["tools"] if t["area"] == area["id"]]
        if not group:
            continue
        L += [f"### {area['en']} / {area['ar']}", "", area.get("about", ""), "",
              "| tool | what it does | first command | guide | evidence |", "|---|---|---|---|---|"]
        for t in group:
            guide = ""
            if t["docs"]:
                d = t["docs"][0]
                name = d.split("/")[-1]
                link = d.split("kosif-superpowers/references/")[-1] if "kosif-superpowers/references/" in d else \
                    ("../" + d.split("kosif-superpowers/")[-1] if "kosif-superpowers/" in d else "../../../../" + d)
                guide = f"[{name}]({link})"
            where = "" if t["root"] == "skill" else " (repo)"
            L.append(f"| `{t['id']}`{where} | {md_cell(t['summary_en'])} | `{md_cell(t['commands'][0]['example'])}` | {guide} | {t['evidence']} |")
        L.append("")
    L += ["## Guides by area", ""]
    for area in list(AREAS) + ["general"]:
        group = [d for d in docs if d["area"] == area]
        if not group:
            continue
        en = next((a["en"] for a in reg["areas"] if a["id"] == area), "General")
        L.append(f"- **{en}:** " + " · ".join(f"[{md_cell(d['title'])}]({d['path'].split('/', 1)[1]})" for d in group))
    L += ["", "## Power families", "",
          f"{total:,} records. Search: `python3 scripts/powers.py search <words>` · one record: `python3 scripts/powers.py show <ID>`.", "",
          "| prefix | family | domain | powers | ✅ proven | chapter |", "|---|---|---|---|---|---|"]
    for f in sorted(fams, key=lambda f: (list(P.DOMAINS).index(f["domain"]) if f["domain"] in P.DOMAINS else 99, f["key"])):
        L.append(f"| {f['prefix']} | {md_cell(f['title_en'])} — {md_cell(f['title_ar'])} | {f['domain']} | {f['count']} | "
                 f"{f['statuses'].get('proven', 0)} | [{f['key']}.md](powers/{f['key']}.md) |")
    return "\n".join(L) + "\n"


def build_skill_block(reg: dict) -> str:
    L = [BLOCK_START, "| المجال / area | الأدوات / tools (`hub.py tool <id>`) |", "|---|---|"]
    for area in reg["areas"]:
        ids = [t["id"] for t in reg["tools"] if t["area"] == area["id"]]
        if ids:
            L.append(f"| {area['en']} / {area['ar']} | " + " · ".join(f"`{i}`" for i in ids) + " |")
    L.append(BLOCK_END)
    return "\n".join(L)


def tool_power_records(reg: dict) -> list:
    """Catalog records (family runnable-tools, ids TOOL-NN) for registry tools that carry a power_id.

    Derived only from data/tools.json, so the catalog and the registry cannot disagree. Status is honest:
    ✅ proven only when the registry says its test passed on this checkout (proof = that test file),
    📦 install when it needs third-party packages or programs, otherwise 🟢 ready (proof = the code file)."""
    import requirements as R  # noqa: E402
    import relabel_proofs as RP  # noqa: E402
    pats = R.compiled(R.registry())
    common_bins = {"python3", "python", "ffmpeg", "ffprobe", "node"}
    rows = []
    for t in sorted((t for t in reg["tools"] if t.get("power_id")), key=lambda t: int(t["power_id"].split("-")[1])):
        req = t["requires"]
        code = (".claude/skills/kosif-superpowers/" + t["path"]) if t["root"] == "skill" else t["path"]
        third_party = bool(req["python"] or req["node"] or [b for b in req["binaries"] if b not in common_bins])
        if t["evidence"] == "tested-here" and t["tests"]:
            status, proof = "proven", [f"kosif-tool/{x}" for x in t["tests"]] + [f"kosif-tool/{code.rstrip('/')}"]
        else:
            status, proof = ("install" if third_party else "ready"), [f"kosif-tool/{code.rstrip('/')}"]
        ar = next((u for u in t["use_when"] if re.search(r"[\u0600-\u06FF]", u)), t["use_when"][0])
        en = next((u for u in t["use_when"] if not re.search(r"[\u0600-\u06FF]", u)), t["use_when"][-1])
        install = []
        if req["python"]:
            install.append("pip install " + " ".join(req["python"]))
        if req["node"]:
            install.append("npm install " + " ".join(req["node"]))
        if req["binaries"]:
            install.append("needs on PATH: " + ", ".join(req["binaries"]))
        if req["optional"]:
            install.append("optional: " + ", ".join(req["optional"]))
        ar_area, en_area = area_title(reg, t["area"])
        rec = OrderedDict([
            ("id", t["power_id"]), ("family", TOOL_FAMILY), ("domain", P.FAMILY_META[TOOL_FAMILY][1]),
            ("name_ar", t["title_ar"]), ("name_en", t["title_en"]), ("status", status),
            ("what", f"{t['summary_ar']} — {t['summary_en']}"),
            ("when", f"{ar} / {en}"),
            ("how", "; ".join(f"{c['name']}: `{c['example']}`" for c in t["commands"][:4])
             + f". Full card: `python3 scripts/hub.py tool {t['id']}`. Limits: {t['limits']}"),
            ("params", f"in: {t['inputs']} · out: {t['outputs']}"),
            ("install", " · ".join(install)),
            ("requires", []),
            ("license", ""),
            ("proof", proof), ("proof_scope", ""), ("styles", []),
            ("tags", list(dict.fromkeys([t["id"], *t["keywords"]]))),
            ("section", f"{en_area} / {ar_area}"), ("source", "data/tools.json"),
        ])
        rec["requires"] = R.derive_one(rec, pats)
        rec["proof_scope"] = RP.record_scope(rec)
        rows.append(rec)
    return rows


def build_area_block(reg: dict, area: str) -> str:
    start, end = f"<!-- hub:area:{area}:start -->", f"<!-- hub:area:{area}:end -->"
    group = [t for t in reg["tools"] if t["area"] == area]
    L = [start, "", f"**الأدوات / tools ({len(group)})** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:", "",
         "| tool | what it does | start with | evidence |", "|---|---|---|---|"]
    for t in group:
        where = " (repo root)" if t["root"] == "repo" else ""
        L.append(f"| `{t['id']}`{where} | {md_cell(t['summary_en'])} | `{md_cell(t['commands'][0]['example'])}` | {t['evidence']} |")
    L += ["", end]
    return "\n".join(L)


def _replace_block(text: str, start: str, end: str, block: str) -> str:
    head, rest = text.split(start, 1)
    _old, tail = rest.split(end, 1)
    return head + block + tail


def generated(reg: dict) -> dict:
    out = {MANIFEST: build_manifest(reg), INDEX_MD: build_index(reg)}
    text = SKILL_MD.read_text(encoding="utf-8")
    if BLOCK_START in text and BLOCK_END in text:
        out[SKILL_MD] = _replace_block(text, BLOCK_START, BLOCK_END, build_skill_block(reg))
    for g in sorted((SKILL / "references" / "guides").glob("*.md")):
        gt = g.read_text(encoding="utf-8")
        for area in AREAS:
            start, end = f"<!-- hub:area:{area}:start -->", f"<!-- hub:area:{area}:end -->"
            if start in gt and end in gt:
                gt = _replace_block(gt, start, end, build_area_block(reg, area))
        out[g] = gt
    return out


def cmd_build(a) -> int:
    reg = load_registry(check_files=True)
    tool_json = json.dumps(tool_power_records(reg), ensure_ascii=False, indent=1) + "\n"
    if not a.check and (not TOOL_POWERS.is_file() or TOOL_POWERS.read_text(encoding="utf-8") != tool_json):
        TOOL_POWERS.write_text(tool_json, encoding="utf-8")  # first: the files below count these records
        print(f"hub build: wrote data/powers/{TOOL_POWERS.name} — now run build_chapters.py, capability_graph.py build and capability_atlas.py build")
    outs = generated(reg)
    outs[TOOL_POWERS] = tool_json
    stale = [p for p, txt in outs.items() if not p.is_file() or p.read_text(encoding="utf-8") != txt]
    if a.check:
        if stale:
            print("stale: " + ", ".join(p.relative_to(SKILL).as_posix() for p in stale) + " — run: python3 scripts/hub.py build", file=sys.stderr)
            for p in stale:
                if p in (MANIFEST, INDEX_MD):
                    previous = p.read_text(encoding="utf-8") if p.is_file() else ""
                    lines = list(difflib.unified_diff(previous.splitlines(), outs[p].splitlines(),
                                                     fromfile="committed/" + p.name,
                                                     tofile="generated/" + p.name, n=1))
                    for line in lines[:24]:
                        print(line, file=sys.stderr)
                    if len(lines) > 24:
                        print("... diff truncated", file=sys.stderr)
            return 1
        print(f"hub build --check: manifest.json, references/INDEX.md and the SKILL.md tool block are current ({len(reg['tools'])} tools)")
        return 0
    for p in stale:
        p.write_text(outs[p], encoding="utf-8")
    print(f"hub build: {len(reg['tools'])} tools · wrote " + (", ".join(p.relative_to(SKILL).as_posix() for p in stale) or "nothing (up to date)"))
    return 0


def cmd_mcp_config(a) -> int:
    py = "python" if os.name == "nt" else "python3"
    server = (HERE / "kosif_mcp.py").resolve()
    cfg = {"mcpServers": {"kosif-superpowers": {"command": py, "args": [str(server)]}}}
    if a.json:
        emit(cfg); return 0
    print("Claude Code (any folder):")
    print(f"  claude mcp add kosif-superpowers -- {py} \"{server}\"")
    print("\nClaude Desktop / Cursor / any MCP client (JSON config):")
    print(json.dumps(cfg, indent=2))
    print("\nInside the kosif-tool repository the project file .mcp.json already registers it.")
    return 0


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    argv = list(sys.argv[1:] if argv is None else argv)
    extra = []
    if argv[:1] == ["run"]:
        # hub.py run [--yes] <id> [--yes] [--] <tool args …>: everything after the id goes to the tool,
        # except a --yes before an optional "--" separator.
        rest, yes, i = argv[1:], False, 0
        while i < len(rest) and rest[i] == "--yes":
            yes, i = True, i + 1
        if i < len(rest) and rest[i] != "--":
            tid, tail, j = rest[i], rest[i + 1:], 0
            while j < len(tail) and tail[j] == "--yes":
                yes, j = True, j + 1
            if j < len(tail) and tail[j] == "--":  # "run <id> [--yes] -- args": everything after goes to the tool verbatim
                extra = tail[j + 1:]
            else:  # a --yes before any later "--" is the hub's; a later "--" and what follows belong to the tool
                tail = tail[j:]
                cut = tail.index("--") if "--" in tail else len(tail)
                yes = yes or "--yes" in tail[:cut]
                extra = [x for x in tail[:cut] if x != "--yes"] + tail[cut:]
            argv = ["run", tid] + (["--yes"] if yes else [])
    ap = argparse.ArgumentParser(prog="hub.py", description="KOSIF hub: one front door to tools, powers and guides.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__.split("\n\n", 1)[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("find", help="tools + powers + guides for a task"); p.add_argument("brief")
    p.add_argument("--tools", type=int, default=5); p.add_argument("--limit", type=int, default=10); p.add_argument("--json", action="store_true")
    p = sub.add_parser("tool", help="one tool card"); p.add_argument("id"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("list", help="every tool by area"); p.add_argument("--area", choices=AREAS); p.add_argument("--json", action="store_true")
    p = sub.add_parser("areas", help="the 12 areas"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("doctor", help="what runs here now"); p.add_argument("--area", choices=AREAS); p.add_argument("--json", action="store_true")
    p = sub.add_parser("power", help="one catalog record"); p.add_argument("id"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("docs", help="reference guides"); p.add_argument("words", nargs="*"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("run", help="run a tool (args after the id are passed through)"); p.add_argument("id"); p.add_argument("--yes", action="store_true")
    p = sub.add_parser("build", help="regenerate manifest.json, references/INDEX.md, SKILL.md block"); p.add_argument("--check", action="store_true")
    p = sub.add_parser("mcp-config", help="MCP client config"); p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "run":
        return cmd_run(a, extra)
    return {"find": cmd_find, "tool": cmd_tool, "list": cmd_list, "areas": cmd_areas, "doctor": cmd_doctor, "power": cmd_power,
            "docs": cmd_docs, "build": cmd_build, "mcp-config": cmd_mcp_config}[a.cmd](a)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
