#!/usr/bin/env python3
"""KOSIF prompt pack — copyable prompts as one fenced code block each, with a transparent lint that only warns.

From the repository root:
  python3 .claude/skills/kosif-superpowers/scripts/prompt_pack.py build <prompts.json> --out out/<work>/prompts [--engine midjourney|generic-image|generic-video|veo|...] [--strict]
  python3 .claude/skills/kosif-superpowers/scripts/prompt_pack.py lint <prompts.json> [--engine ...]

Input (JSON): a list of prompts [{id, engine?, text, negative?, params?, title_ar?, explain_ar?, refs?}], or an object
{title?, engine?, prompts: [...]} or a scene/story spec {title?, engine?, scenes: [...]}. Accepted aliases:
prompt_en -> text, negatives -> negative (a string or a list), scene -> id.

build writes PACK.md (every prompt in ONE fenced block, English prompt inside, Arabic explanation outside, the block
wrapped in <div dir="ltr"> for RTL pages), pack.json (the same data plus the lint warnings) and, when any prompt
lists refs, START-HERE.md (the files to attach). The per-engine suffix comes from data/prompt_engines.json and is
APPENDED after the user's text; the text itself is copied byte for byte. Version-sensitive syntax (Midjourney V7)
is labelled with its version.

The lint only WARNS (contradictions, several subjects without separation, studio/artist/brand names, quality-hype
tokens, text-in-image requests, Arabic inside an English prompt, missing negative baseline, unknown params). It
never rewrites, substitutes or softens a word: there is deliberately no word-swap or euphemism table here. It is
not a content-policy filter. A prompt that looks like it contains a credential is refused (exit 3) and the value
is never printed or written.

Exit codes: 0 ok · 1 bad input or refused output folder · 2 lint warnings (lint, or build --strict) · 3 secret refused.
Nothing is sent to any engine; prompts are not tested on an engine here. Python stdlib only (3.8+).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REPO = SKILL.parents[2]
ENGINES_FILE = SKILL / "data" / "prompt_engines.json"
SCHEMA = "kosif.prompt_pack.v1"
sys.path.insert(0, str(HERE))
try:
    from _secrets import find_secrets  # noqa: E402  one credential detector for the whole skill
except Exception:  # pragma: no cover - minimal fallback when the shared detector is missing
    _FALLBACK = (("google_api_key", r"AIza[0-9A-Za-z_-]{30,}"), ("openai_api_key", r"sk-[A-Za-z0-9_-]{20,}"),
                 ("github_token", r"gh[pousr]_[A-Za-z0-9]{20,}"), ("private_key_block", r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY"))

    def find_secrets(text):
        return [n for n, rx in _FALLBACK if re.search(rx, text or "")]

ARABIC_RE = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")
NOTE_AR = "لا يُنفَّذ هنا — انسخ كل مطالبة كما هي إلى الأداة المذكورة."
NOTE_EN = "Not executed here: copy each prompt as-is into the named tool. Not tested on any engine."


class PackError(Exception):
    def __init__(self, msg, code=1):
        super().__init__(msg)
        self.code = code


def load_engines(path: Path = ENGINES_FILE) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def resolve_engine(name, engines: dict) -> str:
    key = (name or engines.get("default_engine") or "generic-image").strip().lower()
    key = engines.get("aliases", {}).get(key, key)
    if key not in engines["engines"]:
        known = sorted(set(engines["engines"]) | set(engines.get("aliases", {})))
        raise PackError(f"unknown engine {name!r}; known: {', '.join(known)}")
    return key


def normalize(spec, default_engine=None) -> dict:
    """Return {title, engine, prompts:[{id, engine, text, negative[], params{}, title_ar, explain_ar, refs[]}]}."""
    title, engine = "Prompt pack", default_engine
    if isinstance(spec, dict):
        title = spec.get("title") or spec.get("title_ar") or title
        engine = default_engine or spec.get("engine")
        items = spec.get("prompts") if "prompts" in spec else spec.get("scenes")
    else:
        items = spec
    if not isinstance(items, list) or not items:
        raise PackError("input must be a non-empty list of prompts, or an object with 'prompts' or 'scenes'")
    out, seen = [], set()
    for i, it in enumerate(items, 1):
        if not isinstance(it, dict):
            raise PackError(f"prompt #{i} is not an object")
        text = it.get("text", it.get("prompt_en", it.get("prompt")))
        if not isinstance(text, str) or not text.strip():
            raise PackError(f"prompt #{i} has no 'text' (or 'prompt_en')")
        pid = str(it.get("id") or it.get("scene") or f"P{i:02d}")
        if pid in seen:
            raise PackError(f"duplicate prompt id {pid!r}")
        seen.add(pid)
        neg = it.get("negative", it.get("negatives"))
        neg = [neg] if isinstance(neg, str) else list(neg or [])
        refs = it.get("refs") or []
        out.append({"id": pid, "engine": it.get("engine") or engine, "text": text,
                    "negative": [str(n) for n in neg if str(n).strip()],
                    "params": dict(it.get("params") or {}), "title_ar": it.get("title_ar") or "",
                    "explain_ar": it.get("explain_ar") or it.get("explain") or "",
                    "refs": [str(r) for r in (refs if isinstance(refs, list) else [refs])]})
    return {"title": str(title), "engine": engine, "prompts": out}


def _has(text_l: str, phrase: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(phrase.lower()) + r"(?![a-z0-9])", text_l) is not None


def lint_prompt(p: dict, eng_key: str, engines: dict) -> list:
    """Warnings for one prompt: [{id, code, message, suggestion}]. Reads the text, never changes it."""
    cfg, rules = engines["engines"][eng_key], engines.get("lint", {})
    t = p["text"]
    tl = t.lower()
    w = []

    def add(code, message, suggestion):
        w.append({"id": p["id"], "code": code, "message": message, "suggestion": suggestion})

    for a, b in rules.get("contradictions", []):
        if _has(tl, a) and _has(tl, b):
            add("CONTRADICTION", f"both '{a}' and '{b}' appear", "keep one, or split into two prompts/shots")
    found = [n for n in rules.get("subject_nouns", []) if re.search(r"(?<![a-z])(?:a|an|the|one|two|three)\s+(?:[a-z-]+\s+)?"
                                                                     + re.escape(n) + r"s?(?![a-z])", tl)]
    if len(found) >= 2 and not any(_has(tl, c) for c in rules.get("separation_cues", [])):
        add("SUBJECTS_UNSEPARATED", f"several subjects ({', '.join(found[:4])}) with no placement",
            "say where each one is (left/right, foreground/background) and what each does")
    for n in rules.get("names", []):
        if _has(tl, n):
            add("NAMED_STYLE", f"studio/artist/brand name '{n}'",
                "describe the traits you want instead (shape language, palette, lighting, rendering, mood); "
                "names may be refused by the engine or raise rights questions")
    hype = [h for h in rules.get("hype_tokens", []) if _has(tl, h)]
    if hype:
        add("HYPE_TOKENS", f"quality-hype tokens: {', '.join(hype)}", "describe lens, light, material and detail instead")
    if any(_has(tl, c) for c in rules.get("text_cues", [])) or re.search(r"[\"“«][^\"”»]{2,}[\"”»]", t):
        add("TEXT_IN_IMAGE", "the prompt asks for written text/letters in the frame",
            "generate a clean plate (no text) and add the words in the typography pipeline (playbooks/arabic-typography.md)")
    if ARABIC_RE.search(t):
        add("ARABIC_IN_PROMPT", "Arabic characters inside the prompt block",
            "keep the prompt English and put Arabic in the explanation; Arabic words in frame go through typography")
    if cfg.get("negative") and not p["negative"]:
        add("NO_NEGATIVE_BASELINE", "no negative prompt", "add a short baseline (e.g. the artefacts you do not want)")
    for k in p["params"]:
        if k not in cfg.get("params", {}):
            add("UNKNOWN_PARAM", f"param '{k}' has no documented adapter for {cfg['label']}", "it is listed but not emitted")
    if cfg.get("medium") == "video" and cfg.get("fixed_suffix") and cfg["fixed_suffix"].lower() in tl:
        add("SUFFIX_DUPLICATE", "the text already contains the engine's fixed suffix", "it will be appended once more")
    return w


def secret_hits(norm: dict) -> list:
    """[(prompt id, field, kinds)] — never the value."""
    hits = []
    for p in norm["prompts"]:
        for field in ("text", "negative", "params", "explain_ar", "title_ar", "refs"):
            v = p[field]
            s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
            k = find_secrets(s)
            if k:
                hits.append((p["id"], field, k))
    if find_secrets(norm["title"]):
        hits.append(("-", "title", find_secrets(norm["title"])))
    return hits


def suffix_for(p: dict, eng_key: str, engines: dict) -> str:
    cfg = engines["engines"][eng_key]
    parts = []
    if cfg["negative"] == "flag" and p["negative"]:
        parts.append(f"{cfg['negative_flag']} {', '.join(p['negative'])}")
    for k, v in p["params"].items():
        tpl = cfg.get("params", {}).get(k)
        if tpl is None or v is False or v is None:
            continue
        parts.append(tpl.replace("{v}", str(v)))
    if cfg.get("version_flag"):
        parts.append(cfg["version_flag"])
    if cfg["negative"] == "line" and p["negative"]:
        parts.append(f"{cfg['negative_label']} {', '.join(p['negative'])}")
    if cfg.get("fixed_suffix"):
        parts.append(cfg["fixed_suffix"])
    if not parts:
        return ""
    if eng_key == "midjourney":
        return " " + " ".join(parts)
    lines = [x for x in parts if not x.startswith(cfg.get("negative_label") or "\0")]
    neg = [x for x in parts if cfg.get("negative_label") and x.startswith(cfg["negative_label"])]
    body = " ".join(lines)
    return "".join("\n\n" + x for x in ([body] if body else []) + neg)


def fence_for(block: str) -> str:
    longest = max([len(m) for m in re.findall(r"`{3,}", block)] + [2])
    return "`" * (longest + 1)


def assemble(norm: dict, engines: dict) -> dict:
    items, warnings = [], []
    for p in norm["prompts"]:
        key = resolve_engine(p["engine"], engines)
        cfg = engines["engines"][key]
        block = p["text"] + suffix_for(p, key, engines)
        warnings += lint_prompt(p, key, engines)
        items.append(dict(p, engine=key, engine_label=cfg["label"], engine_version=cfg.get("version"),
                          version_sensitive=bool(cfg.get("version_sensitive")), evidence=cfg.get("evidence", "documented"),
                          block=block, block_sha256=hashlib.sha256(block.encode("utf-8")).hexdigest()))
    return {"schema": SCHEMA, "title": norm["title"], "note": NOTE_EN, "prompts": items, "warnings": warnings,
            "lint_note": "warnings only; no word in any prompt was changed", "created_at": dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0).isoformat()}


def render_md(pack: dict) -> str:
    L = [f"# {pack['title']}", "", f"> {NOTE_AR}", f"> {NOTE_EN}", ""]
    for n, it in enumerate(pack["prompts"], 1):
        head = it["title_ar"] or it["id"]
        ver = f" · syntax V{it['engine_version']} (version-sensitive, {it['evidence']})" if it["version_sensitive"] else ""
        fence = fence_for(it["block"])
        L += [f"## {n}. {head} — `{it['id']}`", "", f"**المحرك / Engine:** {it['engine_label']}{ver}", "",
              '<div dir="ltr">', "", fence + "text", it["block"], fence, "", "</div>", ""]
        if it["explain_ar"]:
            L += [f"**الشرح:** {it['explain_ar']}", ""]
        if it["refs"]:
            L += ["**مراجع تُرفق مع المطالبة:** " + ", ".join(f"`{r}`" for r in it["refs"]), ""]
    if pack["warnings"]:
        L += ["## تنبيهات الفحص (تحذيرات فقط — لم يُغيَّر أي حرف)", "", "| id | code | message | suggestion |", "|---|---|---|---|"]
        for w in pack["warnings"]:
            L.append("| {id} | {code} | {message} | {suggestion} |".format(**{k: str(v).replace("|", "\\|") for k, v in w.items()}))
        L.append("")
    return "\n".join(L)


def render_start_here(pack: dict) -> str:
    L = [f"# START HERE — {pack['title']}", "", f"> {NOTE_AR}", "", "| prompt | engine | attach these files |", "|---|---|---|"]
    for it in pack["prompts"]:
        L.append(f"| {it['id']} | {it['engine_label']} | {', '.join(it['refs']) or '—'} |")
    return "\n".join(L) + "\n"


def _git(args, cwd):
    try:
        r = subprocess.run(["git", "-C", str(cwd)] + args, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=60)
        return r.returncode, r.stdout
    except Exception:
        return 128, ""


def out_problem(out: Path):
    """Why OUT must not receive files, or None (skill folder, jobs/, repo root, git-tracked or un-ignored repo paths)."""
    out = Path(out).resolve()
    try:
        out.relative_to(SKILL)
        return f"{out} is inside the skill folder (write under <repo>/out/...)"
    except ValueError:
        pass
    try:
        in_repo = out.relative_to(REPO).parts
    except ValueError:
        in_repo = None
    if in_repo is not None and in_repo[:1] == ("jobs",):
        return f"{out} is inside jobs/ (tracked sources; outputs go under out/)"
    unchecked = f"{out} is inside this repository and git cannot check it (use out/...)" if in_repo is not None and in_repo[:1] != ("out",) else None
    anc = out
    while not anc.exists() and anc != anc.parent:
        anc = anc.parent
    if not shutil.which("git"):
        return unchecked
    rc, top = _git(["rev-parse", "--show-toplevel"], anc if anc.is_dir() else anc.parent)
    if rc:
        return unchecked
    top = Path(top.strip()).resolve()
    try:
        rel = out.relative_to(top)
    except ValueError:
        return None
    if not rel.parts:
        return f"{out} is the repository root"
    if rel.parts[0] == "jobs":
        return f"{out} is inside jobs/ (tracked sources; outputs go under out/)"
    _rc, files = _git(["--literal-pathspecs", "ls-files", "--", rel.as_posix()], top)
    if files.strip():
        return f"{out} is tracked by git"
    rc, _ = _git(["check-ignore", "-q", rel.as_posix()], top)
    if rc == 1:
        return f"{out} is inside the repository but not git-ignored (use out/...)"
    return None


def read_spec(path: str, engine):
    try:
        spec = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise PackError(f"cannot read {path}: {e.__class__.__name__}")
    norm = normalize(spec, engine)
    hits = secret_hits(norm)
    if hits:
        where = "; ".join(f"{pid}.{field} ({', '.join(k)})" for pid, field, k in hits)
        raise PackError(f"refused: credential-like value in {where} — remove it; nothing was written", 3)
    return norm


def cmd_build(a) -> int:
    engines = load_engines(Path(a.engines))
    norm = read_spec(a.spec, a.engine)
    out = Path(a.out)
    if out.suffix.lower() == ".md":
        out = out.parent
    prob = out_problem(out)
    if prob:
        raise PackError(f"refused output folder: {prob}")
    pack = assemble(norm, engines)
    out.mkdir(parents=True, exist_ok=True)
    (out / "PACK.md").write_text(render_md(pack), encoding="utf-8")
    (out / "pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    files = ["PACK.md", "pack.json"]
    if any(it["refs"] for it in pack["prompts"]):
        (out / "START-HERE.md").write_text(render_start_here(pack), encoding="utf-8")
        files.append("START-HERE.md")
    print(json.dumps({"ok": True, "dir": str(out), "files": files, "prompts": len(pack["prompts"]),
                      "warnings": len(pack["warnings"]), "note": NOTE_EN}, ensure_ascii=False, indent=1))
    return 2 if (a.strict and pack["warnings"]) else 0


def cmd_lint(a) -> int:
    engines = load_engines(Path(a.engines))
    norm = read_spec(a.spec, a.engine)
    warnings = []
    for p in norm["prompts"]:
        warnings += lint_prompt(p, resolve_engine(p["engine"], engines), engines)
    print(json.dumps({"prompts": len(norm["prompts"]), "warnings": warnings,
                      "note": "warnings only; no word was changed"}, ensure_ascii=False, indent=1))
    return 2 if warnings else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "lint"):
        s = sub.add_parser(name)
        s.add_argument("spec", help="prompts JSON (list, {prompts:[...]} or {scenes:[...]})")
        s.add_argument("--engine", help="default engine for prompts that do not name one")
        s.add_argument("--engines", default=str(ENGINES_FILE), help=argparse.SUPPRESS)
        if name == "build":
            s.add_argument("--out", required=True, help="output folder (or a .../PACK.md path) under out/")
            s.add_argument("--strict", action="store_true", help="exit 2 when the lint has warnings")
    a = ap.parse_args(argv)
    try:
        return cmd_build(a) if a.cmd == "build" else cmd_lint(a)
    except PackError as e:
        print(str(e), file=sys.stderr)
        return e.code


if __name__ == "__main__":
    sys.exit(main())
