#!/usr/bin/env python3
"""Requirements layer: what every power needs before it can run, and what each install unlocks.

    python3 scripts/requirements.py derive            # fill `requires` on every record from install/how text (data/requirements.json patterns)
    python3 scripts/requirements.py derive --check    # exit 1 if any record would change
    python3 scripts/requirements.py index [--probe]   # write references/requirements.md (requirement → powers unlocked); --probe marks present/missing here
    python3 scripts/requirements.py for <POWER-ID>    # the checklist for one power: present now / install command / key needed
    python3 scripts/requirements.py plan "<task>"     # suggest powers for a task, then the merged checklist with install commands
    python3 scripts/requirements.py present [--json]  # which registered requirements this machine satisfies (fast, read-only)

Stdlib only. Detection is presence, not quality: ✅ still needs a real run. Keys are reported by name only, never by value.
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import signal
import sys
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REG = SKILL / "data" / "requirements.json"
POWERS = SKILL / "data" / "powers"
OUT = SKILL / "references" / "requirements.md"
KINDS_AR = {"bin": "أداة", "pip": "حزمة بايثون", "npm": "حزمة npm", "apt": "حزمة نظام", "key": "مفتاح/حساب", "service": "خدمة/موصل", "os": "منصة", "font": "خطوط", "model": "نموذج/أوزان"}


def registry() -> "OrderedDict[str, dict]":
    data = json.loads(REG.read_text(encoding="utf-8"))
    return OrderedDict((k, v) for k, v in data.items() if not k.startswith("_"))


def compiled(reg):
    return {k: [re.compile(p, re.I) for p in v.get("patterns", [])] for k, v in reg.items()}


def record_text(rec: dict) -> str:
    parts = [str(rec.get(k, "")) for k in ("install", "how", "params", "name_en", "what")]
    parts.append(" ".join(rec.get("tags") or []))
    return " ".join(parts)


def derive_one(rec: dict, pats) -> list:
    text = record_text(rec)
    hits = [k for k, ps in pats.items() if any(p.search(text) for p in ps)]
    # python3/node are implied by any pip/npm requirement; keep them only when nothing more specific is named
    if any(h.startswith("pip:") for h in hits) and "python3" in hits:
        hits.remove("python3")
    if any(h.startswith("npm:") for h in hits) and "node" in hits:
        hits.remove("node")
    if rec.get("status") == "key" and not any(reg_kind(h) in ("key", "service") for h in hits):
        hits.append("key:unspecified")
    return hits


_REG = None


def reg_kind(key: str) -> str:
    global _REG
    if _REG is None:
        _REG = registry()
    return (_REG.get(key) or {}).get("kind", "")


def load_records():
    rows = []
    for f in sorted(glob.glob(str(POWERS / "*.json"))):
        text = Path(f).read_text(encoding="utf-8")
        rows.append((Path(f), text, json.loads(text)))
    return rows


def cmd_derive(check: bool) -> int:
    reg = registry(); pats = compiled(reg)
    changed = 0; per = Counter()
    for path, text, recs in load_records():
        dirty = False
        for rec in recs:
            req = derive_one(rec, pats)
            for k in req:
                per[k] += 1
            if rec.get("requires") != req:
                items = list(rec.items()); out = OrderedDict()
                for k, v in items:
                    if k == "requires":
                        continue
                    out[k] = v
                    if k == "install":
                        out["requires"] = req
                if "requires" not in out:
                    out["requires"] = req
                rec.clear(); rec.update(out); dirty = True; changed += 1
        if dirty and not check:
            indent = 2 if text.startswith("[\n  {") else 1
            path.write_text(json.dumps(recs, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
    print(("would change" if check else "derived requires on") + f" {changed} record(s); requirements used: {len(per)}/{len(reg)}")
    for k, n in per.most_common(12):
        print(f"  {n:5d}  {k}")
    return 1 if (check and changed) else 0


# ---------------------------------------------------------------- presence
def which(name: str) -> bool:
    return bool(shutil.which(name))


def py_import(mod: str) -> bool:
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


def npm_present(pkg: str) -> bool:
    for root in (Path.cwd(), SKILL.parents[2]):
        if (root / "node_modules" / pkg).exists():
            return True
    return False


def present(reg) -> dict:
    """requirement key → 'present' | 'missing' | 'unknown' (read-only, ~1 s)."""
    out = {}
    for k, v in reg.items():
        d = v.get("detect", ""); kind = v.get("kind")
        if not d:
            out[k] = "unknown"; continue
        if kind in ("bin", "apt") and not d.isupper():
            out[k] = "present" if which(d) else "missing"
        elif kind == "pip" or kind == "model":
            out[k] = "present" if py_import(d) else "missing"
        elif kind == "npm":
            out[k] = "present" if (npm_present(d) or which(d)) else "missing"
        elif kind == "key":
            out[k] = "present" if os.environ.get(d) else "missing"
        elif kind == "font":
            out[k] = "present" if (SKILL / d).exists() else "missing"
        elif kind == "os":
            if d == "darwin":
                out[k] = "present" if sys.platform == "darwin" else "missing"
            elif d == "network":
                out[k] = "unknown"
            else:
                out[k] = "present" if which(d) else "missing"
        else:
            out[k] = "present" if (os.environ.get(d) or which(d)) else "unknown"
        if k == "chromium":
            pw = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "")
            out[k] = "present" if (which("chromium") or which("chromium-browser") or (pw and Path(pw).exists())) else out[k]
    return out


def cmd_present(as_json: bool) -> int:
    reg = registry(); p = present(reg)
    if as_json:
        print(json.dumps(p, ensure_ascii=False, indent=1)); return 0
    for state, mark in (("present", "🟢"), ("missing", "📦"), ("unknown", "❔")):
        ks = [k for k, s in p.items() if s == state]
        if ks:
            print(f"{mark} {state} ({len(ks)}): " + ", ".join(ks))
    return 0


# ---------------------------------------------------------------- per power / plan
def all_powers():
    return [rec for _p, _t, recs in load_records() for rec in recs]


def checklist(keys, reg, pres) -> list:
    rows = []
    for k in keys:
        v = reg.get(k) or {}
        st = pres.get(k, "unknown")
        mark = {"present": "🟢", "missing": "📦" if v.get("kind") not in ("key", "service") else "🔑", "unknown": "❔"}[st]
        rows.append((mark, k, KINDS_AR.get(v.get("kind", ""), v.get("kind", "")), v.get("ar", ""), v.get("en", ""), v.get("install", "")))
    return rows


def print_checklist(rows):
    if not rows:
        print("  (no external requirement recorded — needs only Claude and this skill)"); return
    for mark, k, kind, ar, en, inst in rows:
        print(f"  {mark} {k:22s} {kind:12s} {en} / {ar}")
        if mark != "🟢" and inst:
            print(f"       → {inst}")


def cmd_for(pid: str) -> int:
    reg = registry(); pres = present(reg)
    for rec in all_powers():
        if str(rec.get("id", "")).upper() == pid.upper():
            print(f"{rec['id']} · {rec.get('name_ar','')} — {rec.get('name_en','')} · status {rec.get('status')}")
            print_checklist(checklist(rec.get("requires") or [], reg, pres))
            return 0
    print(f"unknown power id {pid}"); return 1


def cmd_plan(task: str, limit: int, as_json: bool = False) -> int:
    sys.path.insert(0, str(HERE))
    import powers as P  # noqa: E402
    reg = registry(); pres = present(reg)
    pw = P.load_powers()
    try:
        styles = P.load_styles()
    except Exception:
        styles = []
    r = P.suggest(pw, styles, task, limit)
    chosen = [p for _s, p in r["picked"]][:limit]
    need = Counter(k for rec in chosen for k in (rec.get("requires") or []))
    rows = checklist([k for k, _n in need.most_common()], reg, pres)
    if as_json:
        print(json.dumps({"task": task, "powers": [{"id": p["id"], "status": p.get("status"), "name_en": p.get("name_en"),
                                                     "requires": p.get("requires") or []} for p in chosen],
                          "requirements": [{"key": k, "state": pres.get(k, "unknown"), "install": (reg.get(k) or {}).get("install", ""),
                                            "used_by": need[k]} for k in need],
                          "ready_now": [p["id"] for p in chosen if all(pres.get(k) == "present" for k in (p.get("requires") or []))]},
                         ensure_ascii=False, indent=1))
        return 0
    print(f"task: {task}\npowers considered: {len(chosen)}")
    for rec in chosen:
        ok = all(pres.get(k) == "present" for k in (rec.get("requires") or []))
        print(f"  {'▶' if ok else '·'} {rec['id']:10s} {P.BADGE.get(rec.get('status'), '')} {rec.get('name_en', '')[:70]}")
    print("\nrequirements (most shared first) — 🟢 present · 📦 install · 🔑 key/account · ❔ unknown:")
    print_checklist(rows)
    missing = [x for x in rows if x[0] != "🟢" and x[5]]
    if missing:
        print("\ninstall plan / خطة التثبيت (ask before paid or system-wide installs):")
        for x in missing:
            print(f"  - {x[1]}: {x[5]}")
    print("\n▶ = every requirement present now: start with these.")
    return 0


# ---------------------------------------------------------------- index
def cmd_index(probe: bool) -> int:
    reg = registry(); pres = present(reg) if probe else {}
    pw = all_powers()
    unlock = {k: [] for k in reg}
    for rec in pw:
        for k in rec.get("requires") or []:
            if k in unlock:
                unlock[k].append(rec)
    L = ["# المستلزمات — Requirements: ماذا تحتاج كل قدرة وماذا يفتح كل تثبيت", "",
         "<!-- generated by scripts/requirements.py index; edit data/requirements.json and the records, then regenerate -->", "",
         "لكل قدرة في الكتالوج حقل `requires` يسمّي ما تحتاجه قبل أن تعمل: أداة على المسار، حزمة pip أو npm، مفتاح أو حساب، منصة، خطوط، نموذج. هذا الفهرس يقلب العلاقة: لكل مستلزم، كم قدرة يفتح وأي عائلات وأمر التثبيت. "
         "`python3 $SKILL_DIR/scripts/requirements.py for <ID>` يعطي قائمة قدرة واحدة، و`plan \"<المهمة>\"` يجمع مستلزمات مهمة كاملة مع ما هو حاضر الآن. — Every power carries `requires`; this index inverts it: for each requirement, how many powers it unlocks, their families and the install command. Presence here is read-only detection, not proof of quality.", "",
         "## الفهرس / contents", "- [الملخص / summary](#summary)", "- [المستلزمات / requirements](#requirements)", "- [قدرات بلا مستلزمات خارجية / no external requirement](#none)", "",
         "<a id=\"summary\"></a>", "## الملخص / summary", "",
         "| # | requirement | kind | powers unlocked | families | here now |", "|---|---|---|---|---|---|"]
    order = sorted(reg, key=lambda k: -len(unlock[k]))
    for i, k in enumerate(order, 1):
        v = reg[k]; recs = unlock[k]
        fams = Counter(r.get("family") for r in recs)
        here = {"present": "🟢", "missing": "📦", "unknown": "❔"}.get(pres.get(k), "")
        L.append(f"| {i} | [`{k}`](#req-{re.sub(r'[^a-z0-9]+', '-', k.lower())}) | {v.get('kind')} | {len(recs)} | {', '.join(f for f, _ in fams.most_common(5))} | {here} |")
    L += ["", "<a id=\"requirements\"></a>", "## المستلزمات / requirements", ""]
    for k in order:
        v = reg[k]; recs = unlock[k]
        anchor = re.sub(r"[^a-z0-9]+", "-", k.lower())
        L += [f"<a id=\"req-{anchor}\"></a>", f"### `{k}` — {v.get('ar','')} / {v.get('en','')}", "",
              f"- **النوع / kind:** {v.get('kind')} ({KINDS_AR.get(v.get('kind',''), '')})",
              f"- **التثبيت / install:** `{v.get('install','')}`",
              f"- **يفتح / unlocks:** {len(recs)} powers"]
        if recs:
            by_status = Counter(r.get("status") for r in recs)
            L.append("- **بالحالة / by status:** " + " · ".join(f"{s} {n}" for s, n in by_status.most_common()))
            fams = Counter(r.get("family") for r in recs)
            L.append("- **العائلات / families:** " + ", ".join(f"{f} ({n})" for f, n in fams.most_common(8)))
            ex = sorted(recs, key=lambda r: (r.get("status") != "proven", r.get("id")))[:6]
            L.append("- **أمثلة / examples:** " + " · ".join(f"`{r['id']}` {r.get('name_en','')[:48]}" for r in ex))
        L.append("")
    none = [r for r in pw if not r.get("requires")]
    L += ["<a id=\"none\"></a>", "## قدرات بلا مستلزمات خارجية / no external requirement", "",
          f"{len(none)} powers need only Claude and this skill (thinking, writing, planning, review protocols). The rest name at least one requirement above.", ""]
    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {OUT.relative_to(SKILL)} · {len(reg)} requirements · {len(pw) - len(none)} powers with requirements · {len(none)} without")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("derive"); d.add_argument("--check", action="store_true")
    i = sub.add_parser("index"); i.add_argument("--probe", action="store_true")
    f = sub.add_parser("for"); f.add_argument("id")
    p = sub.add_parser("plan"); p.add_argument("task"); p.add_argument("--limit", type=int, default=12); p.add_argument("--json", action="store_true")
    pr = sub.add_parser("present"); pr.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "derive":
        return cmd_derive(a.check)
    if a.cmd == "index":
        return cmd_index(a.probe)
    if a.cmd == "for":
        return cmd_for(a.id)
    if a.cmd == "plan":
        return cmd_plan(a.task, a.limit, a.json)
    return cmd_present(a.json)


if __name__ == "__main__":
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
