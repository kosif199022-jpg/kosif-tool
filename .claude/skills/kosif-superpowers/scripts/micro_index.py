#!/usr/bin/env python3
"""KOSIF micro index — الفهرس الدقيق: سطر واحد لكل قدرة وأداة وقدرة خارقة، مع كل ما يربطها.

The finest-grained map of the skill. Every atomic power, every runnable tool and every fused superpower gets one
line that says where it lives and what it connects to: group → domain → family → superpower → power, its badge,
its requirements, the tools of its family, its chapter and its library card. Generated, never hand-edited.

  python3 micro_index.py build [--check]        # data/micro_index.json + references/micro-index/*.md
  python3 micro_index.py stats                  # counts per group, domain, status and kind
  python3 micro_index.py find "<words>" [--kind power|tool|superpower] [--top 20] [--json]
  python3 micro_index.py show <ID>              # any power id, TOOL-NN, tool id or SP-NNNN, with its neighbours

Deterministic and stdlib only. It reads data/powers/*.json, data/tools.json, data/superpowers.json and
data/smart_capability_index.json, so run it after those builders (references/guides/maintain.md).
A line here is an address, not a proof: the badge is the record's own, and ✅ still needs a real run.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
import powers as P  # noqa: E402

DATA = SKILL / "data"
OUT = DATA / "micro_index.json"
DOCS = SKILL / "references" / "micro-index"
SCHEMA = "kosif.micro-index.v1"
REPO_CARDS = "usip-library/cards"
RANK = {s: i for i, s in enumerate(P.STATUSES)}


def jload(p, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def toks(s):
    return [w for w in re.findall(r"[a-z][a-z0-9+#.-]{1,}|[؀-ۿ]{2,}", str(s or "").lower())]


def english(s):
    """The English half of a bilingual 'AR — EN' text (the whole text when it has no Arabic half)."""
    s = str(s or "").strip()
    return s.split(" — ", 1)[1] if re.match(r"[؀-ۿ]", s) and " — " in s else s


def short(s, n=110):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def build_index():
    ps = sorted(P.load_powers(), key=lambda p: (p.get("family", ""), p.get("id", "")))
    reg = jload(DATA / "tools.json", {}) or {}
    tools = reg.get("tools", reg) if isinstance(reg, dict) else reg
    sp = (jload(DATA / "superpowers.json", {}) or {}).get("items", [])
    smart = jload(DATA / "smart_capability_index.json", {}) or {}
    group_of = {r["id"]: r.get("group") for r in smart.get("powers", [])}
    groups = {g["id"]: g for g in smart.get("groups", [])}
    sp_of = {m["id"]: s["id"] for s in sp for m in s.get("pipeline", [])}
    tool_by_pid = {t["power_id"]: t["id"] for t in tools if t.get("power_id")}
    fam_tools = collections.defaultdict(list)
    for t in tools:
        for f in t.get("families") or []:
            fam_tools[f].append(t["id"])
    repo = SKILL.parents[2]
    card_dir = repo / REPO_CARDS

    def card(group, fam):
        rel = f"{REPO_CARDS}/{group}/{fam}.md"
        return rel if (card_dir / group / f"{fam}.md").exists() else None

    fams, rows = {}, []
    for p in ps:
        f, g = p.get("family", ""), group_of.get(p["id"]) or "misc"
        if f not in fams:
            fams[f] = {"domain": p.get("domain") or P.DEFAULT_DOMAIN, "group": g,
                       "chapter": f"references/powers/{f}.md" if (SKILL / "references" / "powers" / f"{f}.md").exists() else None,
                       "card": card(g, f), "tools": sorted(fam_tools.get(f, []))}
        row = {"id": p["id"], "kind": "power", "family": f, "group": g, "status": p.get("status"), "sp": sp_of.get(p["id"]),
               "name_en": p.get("name_en"), "name_ar": p.get("name_ar"), "what": short(english(p.get("what")), 90)}
        for k, v in (("domain", p.get("domain") if p.get("domain") != fams[f]["domain"] else None),
                     ("requires", p.get("requires")), ("tool", tool_by_pid.get(p["id"])),
                     ("proof_scope", p.get("proof_scope")), ("tags", (p.get("tags") or [])[:4])):
            if v:
                row[k] = v
        rows.append(row)
    trows = []
    for t in sorted(tools, key=lambda t: t["id"]):
        cmd = (t.get("commands") or [{}])[0]
        trows.append({
            "id": t["id"], "kind": "tool", "power_id": t.get("power_id"), "area": t.get("area"), "path": t.get("path"),
            "name_en": t.get("title_en"), "name_ar": t.get("title_ar"), "what": short(t.get("summary_en")),
            "families": t.get("families") or [], "requires": t.get("requires") or [],
            "command": cmd.get("example") or cmd.get("run"), "tests": t.get("tests") or [], "evidence": t.get("evidence"),
            "sp": sp_of.get(t.get("power_id")),
        })
    srows = []
    for s in sp:
        srows.append({
            "id": s["id"], "kind": "superpower", "domain": s.get("domain"), "family": s.get("family"),
            "name_en": s.get("name_en"), "name_ar": s.get("name_ar"), "focus": s.get("focus") or [],
            "size": s.get("size"), "best": s.get("best"), "ready_now": s.get("ready_now"),
            "members": [m["id"] for m in s.get("pipeline", [])], "links": [l["id"] for l in s.get("links", [])],
            "requires": s.get("requires") or [],
        })
    gcount = collections.Counter(r["group"] for r in rows)
    return {
        "schema": SCHEMA,
        "note": "Generated by scripts/micro_index.py build. One entry per power, tool and superpower; an address, not a proof.",
        "counts": {"powers": len(rows), "tools": len(trows), "superpowers": len(srows), "groups": len(gcount),
                   "families": len(fams), "domains": len({r.get("domain") or fams[r["family"]]["domain"] for r in rows}),
                   "status": {s: n for s, n in sorted(collections.Counter(r["status"] for r in rows).items(), key=lambda kv: RANK.get(kv[0], 9))}},
        "groups": [{"id": gid, "ar": (groups.get(gid) or {}).get("ar", gid), "en": (groups.get(gid) or {}).get("en", gid), "powers": n}
                   for gid, n in sorted(gcount.items(), key=lambda kv: (-kv[1], kv[0]))],
        "families": fams, "powers": rows, "tools": trows, "superpowers": srows,
    }


def slug(title):
    """GitHub's heading anchor."""
    import unicodedata
    t = str(title).strip().lower()
    return "".join(c for c in t if c in " -_" or unicodedata.category(c)[0] in "LMN").replace(" ", "-")


def contents(heads):
    return ["## الفهرس / contents", ""] + [f"- [{h}](#{slug(h)})" for h in heads] + [""]


def cell(s):
    return str(s or "").replace("|", "/").replace("\n", " ")


def render(idx):
    """{relative path: markdown} for the README and one page per group."""
    c = idx["counts"]
    sp_name = {s["id"]: s["name_en"] for s in idx["superpowers"]}
    by_group = collections.defaultdict(list)
    fams = idx["families"]
    for r in idx["powers"]:
        by_group[r["group"]].append(r)
    pages = {}
    head = ["# الفهرس الدقيق / Micro index", "",
            "سطر واحد لكل قدرة وأداة وقدرة خارقة: أين تعيش، وشارتها، ومستلزماتها، وقدرتها الخارقة، وأدوات عائلتها، وفصلها وبطاقتها. "
            "مولَّد بأمر `python3 scripts/micro_index.py build`؛ لا تحرره يدويًا.",
            "One line per power, tool and superpower: where it lives, its badge, requirements, superpower, its family's tools, "
            "chapter and library card. Generated by `python3 scripts/micro_index.py build`; do not edit by hand. "
            "A line is an address, not a proof: ✅ still needs a real run.", "",
            f"**{c['powers']:,}** powers · **{c['tools']}** tools · **{c['superpowers']}** superpowers · "
            f"{c['groups']} groups · {c['families']} families · {c['domains']} domains", "",
            "حالات / status: " + " · ".join(f"{P.BADGE.get(s, s)} {n:,}" for s, n in c["status"].items()), "",
            "## البحث / search", "", "```bash",
            'python3 scripts/micro_index.py find "قص على الإيقاع"          # any words, Arabic or English',
            "python3 scripts/micro_index.py find \"lufs\" --kind tool",
            "python3 scripts/micro_index.py show SP-0001                  # a superpower with its members and links",
            "python3 scripts/micro_index.py show TRANS-12                 # a power with its superpower, tools and chapter",
            "```", "", "## المجموعات / groups", "", "| المجموعة / group | القدرات / powers | الصفحة / page |", "|---|---:|---|"]
    for g in idx["groups"]:
        head.append(f"| {cell(g['ar'])} — {cell(g['en'])} | {g['powers']:,} | [{g['id']}.md]({g['id']}.md) |")
    head += ["| الأدوات القابلة للتشغيل — Runnable tools | " + f"{c['tools']} | [tools.md](tools.md) |",
             "| القدرات الخارقة — Superpowers | " + f"{c['superpowers']} | [superpowers.md](superpowers.md) |", ""]
    pages["README.md"] = "\n".join(head)
    for g in idx["groups"]:
        rows = sorted(by_group[g["id"]], key=lambda r: (fams[r["family"]]["domain"], r["family"], r["sp"] or "", RANK.get(r["status"], 9), r["id"]))
        out = [f"# {g['ar']} — {g['en']}", "", f"[← الفهرس الدقيق / micro index](README.md) · {g['powers']:,} powers", ""]
        out += contents(list(dict.fromkeys(f"{r['family']} ({fams[r['family']]['domain']})" for r in rows)))
        fam = None
        for r in rows:
            if r["family"] != fam:
                fam = r["family"]
                fi = fams[fam]
                tools_ = " · ".join(f"`{t}`" for t in fi["tools"][:8]) + (" …" if len(fi["tools"]) > 8 else "") or "—"
                where = f"[{fam}](../powers/{fam}.md)" if fi["chapter"] else f"`{fam}`"
                out += ["", f"## {fam} ({fi['domain']})", "", f"chapter: {where} · card: `{fi['card'] or '—'}` · tools: {tools_}", "",
                        "| ID | | القدرة / power | SP | يحتاج / requires |", "|---|---|---|---|---|"]
            sp = f"{r['sp']} {cell(short(sp_name.get(r['sp']), 40))}" if r["sp"] else "—"
            rq = r.get("requires") or []
            req = ", ".join(rq[:4]) + (" …" if len(rq) > 4 else "")
            name = f"{cell(r['name_ar'])} · {cell(r['name_en'])}" + (f" → `{r['tool']}`" if r.get("tool") else "")
            out.append(f"| {r['id']} | {P.BADGE.get(r['status'], '')} | {name} | {sp} | {cell(req) or '—'} |")
        pages[f"{g['id']}.md"] = "\n".join(out) + "\n"
    out = ["# الأدوات القابلة للتشغيل / Runnable tools", "", "[← الفهرس الدقيق / micro index](README.md)", ""]
    tools_by = collections.defaultdict(list)
    for t in idx["tools"]:
        tools_by[t["area"] or "other"].append(t)
    out += contents(sorted(tools_by))
    for area in sorted(tools_by):
        out += [f"## {area}", "", "| tool | ID | الأداة / tool | أمر أول / first command | tests |", "|---|---|---|---|---|"]
        for t in tools_by[area]:
                out.append(f"| `{t['id']}` | {t['power_id'] or '—'} | {cell(t['name_ar'])} · {cell(t['name_en'])} | "
                       f"`{cell(short(t['command'], 70)) or '—'}` | {len(t['tests'])} |")
        out.append("")
    pages["tools.md"] = "\n".join(out) + "\n"
    out = ["# القدرات الخارقة / Superpowers", "", "[← الفهرس الدقيق / micro index](README.md)", ""]
    sp_by = collections.defaultdict(list)
    for s in idx["superpowers"]:
        sp_by[s["domain"] or "motion"].append(s)
    doms = [d for d in P.DOMAINS if d in sp_by] + sorted(d for d in sp_by if d not in P.DOMAINS)
    out += contents(doms)
    for d in doms:
        out += [f"## {d}", "", "| SP | | القدرة الخارقة / superpower | size | ready | links |", "|---|---|---|---:|---:|---|"]
        for s in sp_by[d]:
            out.append(f"| {s['id']} | {P.BADGE.get(s['best'], '')} | {cell(s['name_ar'])} · {cell(s['name_en'])} | "
                       f"{s['size']} | {s['ready_now']} | {' '.join(s['links'])} |")
        out.append("")
    pages["superpowers.md"] = "\n".join(out) + "\n"
    return pages


def dump(idx):
    return json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + "\n"


def cmd_build(check):
    idx = build_index()
    want = {OUT: dump(idx)} | {DOCS / k: v for k, v in render(idx).items()}
    stale = [p for p, txt in want.items() if not p.exists() or p.read_text(encoding="utf-8") != txt]
    orphans = [p for p in DOCS.glob("*.md") if p not in want] if DOCS.exists() else []
    if check:
        for p in stale + orphans:
            print(f"stale: {p.relative_to(SKILL)}")
        print("micro index up to date" if not (stale or orphans) else "run: python3 scripts/micro_index.py build")
        return 1 if stale or orphans else 0
    DOCS.mkdir(parents=True, exist_ok=True)
    for p in stale:
        p.write_text(want[p], encoding="utf-8")
    for p in orphans:
        p.unlink()
    c = idx["counts"]
    print(f"{c['powers']} powers · {c['tools']} tools · {c['superpowers']} superpowers → {OUT.relative_to(SKILL)} + {len(want) - 1} pages")
    return 0


def load():
    idx = jload(OUT)
    if not idx or idx.get("schema") != SCHEMA:
        print("data/micro_index.json missing or stale; run: python3 scripts/micro_index.py build", file=sys.stderr)
        sys.exit(2)
    return idx


def entries(idx, kind=None):
    for k in ("powers", "tools", "superpowers"):
        for r in idx[k]:
            if kind in (None, r["kind"]):
                yield r


def score(r, q):
    hay = " ".join(str(x) for x in (r["id"], r.get("name_en"), r.get("name_ar"), r.get("what"), " ".join(r.get("tags") or []),
                                     " ".join(r.get("focus") or []), r.get("family"), r.get("area")) if x)
    words = collections.Counter(toks(hay))
    name = set(toks(f"{r.get('name_en')} {r.get('name_ar')}"))
    s = 0.0
    for w in q:
        if w in words:
            s += 1 + (2 if w in name else 0)
        elif len(w) >= 4 and any(x.startswith(w) or w.startswith(x) for x in words if len(x) >= 4):
            s += 0.5
    if s and r["kind"] == "power":
        s += (len(P.STATUSES) - RANK.get(r.get("status"), 9)) * 0.05
    return s


def line(r, sp_name=None):
    if r["kind"] == "power":
        sp = f" · {r['sp']}" + (f" {short(sp_name.get(r['sp']), 40)}" if sp_name and r["sp"] else "") if r["sp"] else ""
        return f"{r['id']:<10} {P.BADGE.get(r['status'], '')} {r['name_ar']} · {r['name_en']}  [{r['group']}/{r['family']}{sp}]"
    if r["kind"] == "tool":
        return f"{r['id']:<10} 🛠 {r['name_ar']} · {r['name_en']}  [{r['area']} · {r['power_id'] or '—'}]  {r['command'] or ''}"
    return f"{r['id']:<10} {P.BADGE.get(r['best'], '')} {r['name_ar']} · {r['name_en']}  [{r['domain']} · {r['size']} powers]"


def cmd_find(q, kind, top, as_json):
    idx = load()
    words = [w for w in toks(q) if len(w) >= 2]
    hits = sorted(((score(r, words), r) for r in entries(idx, kind)), key=lambda x: (-x[0], x[1]["id"]))
    hits = [r for s, r in hits if s > 0][:top]
    if as_json:
        print(json.dumps(hits, ensure_ascii=False, indent=1))
        return 0
    sp_name = {s["id"]: s["name_en"] for s in idx["superpowers"]}
    for r in hits:
        print(line(r, sp_name))
    if not hits:
        print("no match; try fewer or other words, or: python3 scripts/hub.py find \"<task>\"")
    return 0


def cmd_show(key):
    idx = load()
    allr = {r["id"]: r for r in entries(idx)}
    r = allr.get(key) or allr.get(key.upper())
    if not r:
        print(f"unknown id: {key}")
        return 2
    sp_name = {s["id"]: s["name_en"] for s in idx["superpowers"]}
    print(line(r, sp_name))
    if r.get("what"):
        print(f"  what: {r['what']}")
    if r["kind"] == "power":
        fi = idx["families"][r["family"]]
        print(f"  domain {r.get('domain') or fi['domain']} · family {r['family']} · proof_scope {r.get('proof_scope') or '—'}")
        print(f"  requires: {', '.join(r.get('requires') or []) or '—'}")
        if r.get("tool"):
            print(f"  tool: {r['tool']}  → python3 scripts/hub.py tool {r['tool']}")
        print(f"  family tools: {' · '.join(fi['tools']) or '—'}")
        print(f"  chapter: {fi['chapter'] or '—'} · card: {fi['card'] or '—'}")
        if r["sp"]:
            print(f"  superpower: {r['sp']} {sp_name.get(r['sp'], '')}  → micro_index.py show {r['sp']}")
    elif r["kind"] == "tool":
        print(f"  path {r['path']} · families {', '.join(r['families']) or '—'} · evidence {r.get('evidence') or '—'}")
        print(f"  requires: {', '.join(r['requires']) or '—'} · tests: {', '.join(r['tests']) or '—'}")
        print(f"  catalog: {r['power_id'] or '—'}" + (f" in {r['sp']} {sp_name.get(r['sp'], '')}" if r.get("sp") else ""))
    else:
        print(f"  focus: {', '.join(r['focus'])} · ready now {r['ready_now']} · requires {', '.join(r['requires']) or '—'}")
        print("  links: " + " · ".join(f"{l} {short(sp_name.get(l), 40)}" for l in r["links"]))
        for m in r["members"]:
            if m in allr:
                print("   " + line(allr[m]))
    return 0


def cmd_stats():
    idx = load()
    c = idx["counts"]
    print(f"{c['powers']:,} powers · {c['tools']} tools · {c['superpowers']} superpowers · {c['groups']} groups · "
          f"{c['families']} families · {c['domains']} domains")
    print("status: " + " · ".join(f"{P.BADGE.get(s, s)} {n:,}" for s, n in c["status"].items()))
    for g in idx["groups"]:
        print(f"  {g['id']:<12} {g['powers']:>5}  {g['ar']} — {g['en']}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--check", action="store_true")
    sub.add_parser("stats")
    f = sub.add_parser("find"); f.add_argument("query"); f.add_argument("--kind", choices=["power", "tool", "superpower"])
    f.add_argument("--top", type=int, default=20); f.add_argument("--json", action="store_true")
    s = sub.add_parser("show"); s.add_argument("id")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        return cmd_build(a.check)
    if a.cmd == "find":
        return cmd_find(a.query, a.kind, a.top, a.json)
    if a.cmd == "show":
        return cmd_show(a.id)
    return cmd_stats()


if __name__ == "__main__":
    sys.exit(main())
