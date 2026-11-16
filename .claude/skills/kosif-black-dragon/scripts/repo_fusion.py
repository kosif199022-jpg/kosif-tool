#!/usr/bin/env python3
"""Black Dragon repo fusion: capabilities taken from external repos dissected with REA.

Reads `data/repo_fusion.json` (one record per repository: license, REA evidence,
capabilities with source references, and the native module that re-implements the
most useful ones under `scripts/fusion/`). It never downloads or runs the upstream
repositories; the native modules are our own code.

Commands (run from the repository root):
  repo_fusion.py list                    # repositories and their status
  repo_fusion.py find "مزامنة على الإيقاع" [--stage shots] [--json]
  repo_fusion.py show <repo-or-capability-id> [--json]
  repo_fusion.py modules                 # native modules and their commands
  repo_fusion.py self-test [--module NAME] [--json]   # runs every native module's own self-test
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "repo_fusion.json"
FUSION_DIR = ROOT / "scripts" / "fusion"
STAGES = ("brief", "concept", "color-design", "shots", "produce", "qa-color", "deliver")
_AR_DIACRITICS = re.compile(r"[ً-ْـ]")


def load(path: Path = DATA) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "kosif.black_dragon.repo_fusion.v1":
        raise SystemExit(f"unexpected schema in {path}")
    return data


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "").lower()
    text = _AR_DIACRITICS.sub("", text)
    text = re.sub("[إأآ]", "ا", text).replace("ة", "ه").replace("ى", "ي")
    return text


def _tokens(text: str) -> list[str]:
    out = []
    for tok in re.findall(r"[\w\-]+", _norm(text)):
        out.append(tok)
        for pre in ("وال", "بال", "لل", "ال", "و"):
            if tok.startswith(pre) and len(tok) - len(pre) >= 3:
                out.append(tok[len(pre):])
                break
    return out


def capabilities(data: dict):
    for repo in data["repos"]:
        for cap in repo.get("capabilities", []):
            yield repo, cap


def find(data: dict, query: str, stage: str | None = None, limit: int = 10) -> list[dict]:
    q = set(_tokens(query))
    hits = []
    for repo, cap in capabilities(data):
        if stage and cap.get("dragon_stage") != stage:
            continue
        hay = " ".join(str(cap.get(k, "")) for k in ("id", "title_en", "title_ar", "what", "notes"))
        hay += " " + repo["owner_repo"] + " " + " ".join(repo.get("keywords", []))
        words = set(_tokens(hay))
        score = sum(1 for t in q if t in words) + 0.5 * sum(
            1 for t in q if len(t) >= 4 and any(w.startswith(t) or t.startswith(w) for w in words if len(w) >= 4)
        )
        if cap.get("status") == "native-implemented":
            score += 0.25 if score else 0
        if score > 0:
            hits.append({"score": round(score, 2), "repo": repo["owner_repo"], **cap})
    hits.sort(key=lambda h: (-h["score"], h["id"]))
    return hits[:limit]


def show(data: dict, key: str) -> dict | None:
    k = key.lower()
    for repo in data["repos"]:
        if k in (repo["owner_repo"].lower(), repo["owner_repo"].split("/")[1].lower()):
            return repo
    for repo, cap in capabilities(data):
        if cap["id"].lower() == k:
            return {"repo": repo["owner_repo"], "license": repo["license"], **cap}
    return None


def run_self_tests(data: dict, only: str | None = None) -> list[dict]:
    results = []
    for mod in data["modules"]:
        if only and mod["name"] != only:
            continue
        script = FUSION_DIR / mod["file"]
        if script.suffix == ".py":
            cmd = [sys.executable, "-I", str(script), "self-test"]
        else:
            cmd = ["node", str(script), "--self-test"]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", timeout=mod.get("timeout_s", 300))
            ok, tail = proc.returncode == 0, (proc.stdout + proc.stderr).strip().splitlines()[-3:]
        except FileNotFoundError as exc:
            ok, tail = False, [f"runtime missing: {exc}"]
        except subprocess.TimeoutExpired:
            ok, tail = False, ["timeout"]
        results.append({"module": mod["name"], "file": mod["file"], "ok": ok, "tail": tail})
    return results


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("find"); p.add_argument("query"); p.add_argument("--stage", choices=STAGES)
    p.add_argument("--limit", type=int, default=10); p.add_argument("--json", action="store_true")
    p = sub.add_parser("show"); p.add_argument("key"); p.add_argument("--json", action="store_true")
    sub.add_parser("modules")
    p = sub.add_parser("self-test"); p.add_argument("--module"); p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    data = load()

    if a.cmd == "list":
        for r in data["repos"]:
            caps = r.get("capabilities", [])
            native = sum(1 for c in caps if c.get("status") == "native-implemented")
            print(f"{r['owner_repo']:<38} {r['license']:<12} caps={len(caps):<3} native={native:<2} module={r.get('module') or '-'}")
        return 0
    if a.cmd == "find":
        hits = find(data, a.query, a.stage, a.limit)
        if a.json:
            print(json.dumps(hits, ensure_ascii=False, indent=1))
        else:
            for h in hits:
                print(f"[{h['score']}] {h['id']} ({h['repo']}, {h.get('dragon_stage')}, {h.get('status')})\n    {h.get('title_ar') or h.get('title_en')} — {h.get('source_ref', '')}")
            if not hits:
                print("no match")
        return 0 if hits else 1
    if a.cmd == "show":
        rec = show(data, a.key)
        if rec is None:
            print("not found", file=sys.stderr)
            return 1
        print(json.dumps(rec, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "modules":
        for m in data["modules"]:
            print(f"{m['name']:<22} scripts/fusion/{m['file']}\n    {m['purpose']}\n    e.g. {m['example']}")
        return 0
    if a.cmd == "self-test":
        res = run_self_tests(data, a.module)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            for r in res:
                print(f"{'PASS' if r['ok'] else 'FAIL'} {r['module']}: {' | '.join(r['tail'])}")
        return 0 if res and all(r["ok"] for r in res) else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
