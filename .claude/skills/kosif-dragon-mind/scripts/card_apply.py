#!/usr/bin/env python3
"""Apply ONE Black Dragon catalog entry to a task and write the result with a receipt.

Usage: card_apply.py ARTIFACT ENTRY_ID TASK

Works for every kind: power, superpower, style, skill, playbook, protocol rule and
tool. It reads the entry's own source record (verified by SHA-256), turns it into a
task-specific procedure (numbered steps bound to the task), checks the entry's
requirements on THIS machine (binaries, Python modules, npm packages, keys), adds
acceptance checks and the entry's links in the capability graph (upstream,
downstream, peers, owning skill), and writes ARTIFACT as JSON.

Exit codes are honest: 0 = applied (source found, at least one step);
3 = source missing or nothing applicable (the dragon records "failed").
This is a method applier, not media production: running a tool's own command
stays with that tool's reviewed adapter. The status string says which it is.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MIND = HERE.parent
SKILLS = MIND.parent
SUPER = SKILLS / "kosif-superpowers"
REPO = MIND.parents[2]
LINKS = MIND / "data" / "mind_links.json"
WORD = re.compile(r"[\w؀-ۿ]+", re.UNICODE)
SCHEMA = "kosif.dragon-mind.applied.v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text: str) -> set:
    return {w.lower() for w in WORD.findall(text) if len(w) > 2}


def _clip(text, n=400) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= n else text[: n - 1] + "…"


def source_path(kind: str, source: str) -> Path:
    if kind == "skill":
        return SKILLS / source
    if kind in ("style", "playbook"):
        return REPO / source
    return SUPER / source


def headings(path: Path, limit: int = 12) -> list:
    out = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^(#{2,3})\s+(.+)$", line)
            if m:
                out.append(m.group(2).strip())
    except OSError:
        pass
    return out[:limit]


def frontmatter_desc(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if not text.startswith("---"):
        return ""
    block = text[3:text.find("\n---", 3)]
    if block.strip().startswith("{"):
        try:
            return str(json.loads(block).get("description", ""))
        except ValueError:
            return ""
    m = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", block, re.M)
    return " ".join(m.group(1).split()).lstrip(">|-").strip().strip('"') if m else ""


def find_row(path: Path, rid: str, list_keys=("powers", "items", "tools")) -> dict | None:
    obj = json.loads(path.read_text(encoding="utf-8"))
    rows = obj
    if isinstance(obj, dict):
        rows = next((obj[k] for k in list_keys if isinstance(obj.get(k), list)), [])
    return next((r for r in rows if isinstance(r, dict) and str(r.get("id")) == rid), None)


# --------------------------------------------------------------------------- requirements

def _registry() -> dict:
    try:
        data = json.loads((SUPER / "data" / "requirements.json").read_text(encoding="utf-8"))
        return {k: v for k, v in data.items() if not k.startswith("_")}
    except (OSError, ValueError):
        return {}


def _npm(pkg: str) -> bool:
    roots = [REPO / "node_modules", Path.cwd() / "node_modules"]
    npm = shutil.which("npm")
    if npm:  # <prefix>/bin/npm -> <prefix>/lib/node_modules (global installs)
        roots.append(Path(npm).resolve().parents[1] / "lib" / "node_modules")
        roots.append(Path(npm).parent.parent / "lib" / "node_modules")
    roots += [Path(p) for p in os.environ.get("NODE_PATH", "").split(os.pathsep) if p]
    return any((r / pkg).exists() for r in roots) or bool(shutil.which(pkg))


def _pip(mod: str) -> bool:
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


def check_requirements(keys) -> list:
    reg = _registry()
    out = []
    for key in keys or []:
        key = str(key)
        spec = reg.get(key, {})
        kind, detect = spec.get("kind"), spec.get("detect")
        if not kind and ":" in key:
            kind, detect = key.split(":", 1)
        kind = kind or "bin"
        detect = detect or key
        if key == "chromium" or detect == "playwright-chromium":
            pw = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "")
            state = "present" if (shutil.which("chromium") or shutil.which("chromium-browser")
                                  or (pw and Path(pw).is_dir())) else "missing"
        elif detect and detect.isupper() and kind not in ("pip", "model"):  # an env var such as GHIDRA_INSTALL_DIR
            state = "present" if os.environ.get(detect) else "missing"
        elif kind == "key" and not spec.get("detect") and key.endswith("unspecified"):
            state = "unknown"  # the card says a key is needed but names no provider
        elif kind in ("bin", "apt", "os") and detect not in ("network", "darwin"):
            state = "present" if shutil.which(detect) else "missing"
        elif detect == "darwin":
            state = "present" if sys.platform == "darwin" else "missing"
        elif kind in ("pip", "model"):
            state = "present" if _pip(detect.replace("-", "_")) or _pip(detect) else "missing"
        elif kind == "npm":
            state = "present" if _npm(detect) else "missing"
        elif kind == "key":
            state = "unknown" if detect in ("unspecified",) else ("present" if os.environ.get(detect) else "missing")
        elif kind == "font":
            state = "present" if (SUPER / detect).exists() else "missing"
        elif kind in ("claude", "service", "mcp"):
            state = "connector"  # available only through a connected Claude tool, with consent
        else:
            state = "unknown"
        out.append({"requirement": key, "state": state, "install": spec.get("install")})
    return out


# --------------------------------------------------------------------------- procedures per kind

def procedure(key: str, kind: str, src: Path, task: str) -> tuple[str, str, list, list, list]:
    """(name, summary, steps, requirements, acceptance checks) from the entry's own record."""
    rid = key.split(":", 1)[1]
    t = "«%s»" % _clip(task, 120)
    if kind == "power":
        row = find_row(src, rid) or {}
        name = row.get("name_en") or row.get("name_ar") or rid
        steps = []
        if row.get("when"):
            steps.append("Check it fits %s: %s" % (t, _clip(row["when"], 300)))
        if row.get("what"):
            steps.append("Apply to %s: %s" % (t, _clip(row["what"], 400)))
        if row.get("how"):
            steps.append("Do it this way: " + _clip(row["how"], 400))
        if row.get("params"):
            steps.append("Set the parameters: " + _clip(row["params"], 200))
        if row.get("install"):
            steps.append("Prepare the requirement first: " + _clip(row["install"], 200))
        checks = ["proof to compare with: " + p for p in (row.get("proof") or [])[:3]] or \
                 ["the output of each step is saved and measured before any 'done'"]
        return name, _clip(row.get("what"), 300), steps, row.get("requires") or [], checks
    if kind == "superpower":
        row = find_row(src, rid) or {}
        name = row.get("name_en") or rid
        steps = ["Run stage %d on %s with %s (%s, %s)" % (i + 1, t, p.get("id"), _clip(p.get("name_en"), 120), p.get("status"))
                 for i, p in enumerate(row.get("pipeline") or [])]
        checks = ["each stage hands its output to the next one (%d stages)" % len(steps),
                  "best evidence in this fusion: %s" % row.get("best")]
        return name, "fused superpower of %s methods, focus: %s" % (row.get("size"), ", ".join(row.get("focus") or [])), \
            steps, row.get("requires") or [], checks
    if kind == "style":
        rows = json.loads(src.read_text(encoding="utf-8"))
        row = next((r for r in rows if r.get("id") == rid), {})
        skill = REPO / str(row.get("skill") or ("styles/%s/SKILL.md" % rid))
        steps = ["Read the style card %s and its STYLE.json" % skill.relative_to(REPO) if skill.exists() else
                 "Use the style record %s from catalog/styles.json" % rid]
        steps += ["Apply playbook %s to %s" % (p, t) for p in row.get("playbooks") or []]
        steps.append("Match %s to the style's categories: %s" % (t, ", ".join(row.get("category") or []) or "n/a"))
        checks = ["a still frame of %s is compared side by side with the style reference" % t]
        return str(row.get("name") or rid), "motion style reference (%s)" % ", ".join(row.get("category") or []), \
            steps, [], checks
    if kind == "tool":
        row = find_row(src, rid) or {}
        cmds = row.get("commands") or []
        steps = ["Command: %s  # %s" % (c.get("example") or c.get("name"), _clip(c.get("does"), 160)) for c in cmds[:6]]
        req = row.get("requires") or {}
        keys = list(req.get("binaries") or []) + ["pip:" + p for p in req.get("python") or []] + \
            ["npm:" + p for p in req.get("node") or []]
        checks = ["safety: %s, consent: %s" % (row.get("safety"), row.get("consent")),
                  "tests: " + ", ".join(row.get("tests") or ["none listed"])]
        return row.get("title_en") or rid, _clip(row.get("summary_en"), 300), steps, keys, checks
    # skill, playbook, protocol: a readable document with sections
    heads = headings(src)
    desc = frontmatter_desc(src) if kind == "skill" else ""
    steps = ["Follow section «%s» of %s for %s" % (h, src.relative_to(REPO), t) for h in heads] or \
            ["Read %s and apply it to %s" % (src.relative_to(REPO), t)]
    checks = ["every section used is cited by its heading in the work notes"]
    return rid.split("/")[-1], _clip(desc or (heads[0] if heads else rid), 300), steps, [], checks


_LINKS: dict = {}


def apply(key: str, task: str) -> dict:
    if not _LINKS:
        _LINKS.update(json.loads(LINKS.read_text(encoding="utf-8")))
    links = _LINKS
    node = links["nodes"].get(key)
    if node is None:  # links snapshot older than the catalog: ask the live Black Dragon inventory
        if str(HERE) not in sys.path:
            sys.path.insert(0, str(HERE))
        import dragon_mind as dm
        inv, desc, _, _ = dm.load_inventory()
        if key not in inv:
            raise LookupError("unknown entry: " + key)
        row = dm.decompose({key: inv[key]}, desc)[key]
        node = {"kind": row["kind"], "source": inv[key]["source"], "faculties": row["faculties"],
                "inputs": row["inputs"], "outputs": row["outputs"]}
    kind, source = node["kind"], node["source"]
    src = source_path(kind, source)
    if not src.is_file():
        raise FileNotFoundError("source missing: %s" % source)
    name, summary, steps, req, checks = procedure(key, kind, src, task)
    if not steps:
        raise LookupError("no applicable step in the record")
    reqs = check_requirements(req)
    missing = [r["requirement"] for r in reqs if r["state"] == "missing"]
    connectors = [r["requirement"] for r in reqs if r["state"] == "connector"]
    bound = "«%s»" % _clip(task, 120)
    record_words = words(" ".join([key, name, summary] + [x.replace(bound, " ") for x in steps]))
    overlap = sorted(words(task) & record_words)[:12]
    status = ("applied-ready-here" if not missing and not connectors else
              "applied-needs-connector" if not missing else "applied-needs-install")
    return {"schema": SCHEMA, "entry": key, "kind": kind, "name": name, "task": task,
            "source": source, "source_sha256": sha(src), "summary": summary,
            "faculties": node.get("faculties"), "inputs": node.get("inputs"), "outputs": node.get("outputs"),
            "steps": ["%d. %s" % (i + 1, s) for i, s in enumerate(steps)],
            "requirements": reqs, "missing_here": missing, "needs_connector": connectors,
            "acceptance": checks, "task_overlap": overlap,
            "fit": "direct" if len(overlap) >= 2 else "partial" if overlap else "supporting",
            "links": links["edges"].get(key, {}), "status": status,
            "truth": "a task-bound procedure from the entry's own record; not proof that media was produced"}


def main(argv: list) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    artifact, key, task = Path(argv[0]), argv[1], argv[2]
    if not task.strip():
        print("task is empty", file=sys.stderr)
        return 2
    try:
        result = apply(key, task)
    except (LookupError, OSError, ValueError) as exc:
        print("not applied: %s" % exc, file=sys.stderr)
        return 3
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("%s %s (%d steps)" % (result["status"], key, len(result["steps"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
