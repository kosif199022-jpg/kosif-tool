#!/usr/bin/env python3
"""Capability mind map & audit — خريطة القدرات الذهنية والتدقيق.

Orders every power by the stage of a task it serves (understand → plan → create → refine → assemble → verify →
deliver), builds mind maps hub → stage → superpowers and ready-made task maps (data/task_maps.json), and audits
the catalog for duplicates, twins, cross-superpower look-alikes and pairs worth developing together.

  python3 capability_mindmap.py build              # data/capability_mindmap.json + references/capability-mindmap.md + references/capability-audit.md
  python3 capability_mindmap.py task "<task>"      # ordered stage-by-stage plan (mind map) for a task, with Mermaid
  python3 capability_mindmap.py task reels-edit    # a ready-made task map by id
  python3 capability_mindmap.py audit              # duplicate / merge / co-develop summary
Stdlib only; deterministic.
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
import superpower_fusion as F  # noqa: E402

MAPS = SKILL / "data" / "task_maps.json"
SP = SKILL / "data" / "superpowers.json"
HUBX = SKILL / "data" / "hubs_index.json"
OUT = SKILL / "data" / "capability_mindmap.json"
DOC = SKILL / "references" / "capability-mindmap.md"
AUD = SKILL / "references" / "capability-audit.md"
RANK = {s: i for i, s in enumerate(P.STATUSES)}


def cfg():
    return json.loads(MAPS.read_text(encoding="utf-8"))


def stage_of(p, stages):
    text = " ".join([str(p.get("name_en")), str(p.get("name_ar")), " ".join(p.get("tags") or []), str(p.get("section")),
                     str(p.get("what")).split(" — ")[-1][:200]]).lower()
    name = (str(p.get("name_en")) + " " + str(p.get("name_ar"))).lower()
    best, score = "create", 0.0
    for st in stages:
        s = sum((2.0 if k in name else 0) + (1.0 if k in text else 0) for k in st["kw"])
        if s > score:
            best, score = st["id"], s
    return best


def build():
    c = cfg()
    stages = c["stages"]
    order = [s["id"] for s in stages]
    atoms = {p["id"]: p for p in P.load_powers()}
    sp = json.loads(SP.read_text(encoding="utf-8"))
    hx = json.loads(HUBX.read_text(encoding="utf-8"))
    sp_hub = {s: h["id"] for h in hx["hubs"] for s in h["superpowers"]}
    atom_stage = {i: stage_of(p, stages) for i, p in atoms.items()}
    sps = {}
    for s in sp["items"]:
        cnt = collections.Counter(atom_stage[m["id"]] for m in s["pipeline"])
        sps[s["id"]] = {"id": s["id"], "name_ar": s["name_ar"], "name_en": s["name_en"], "hub": sp_hub.get(s["id"]),
                        "stage": cnt.most_common(1)[0][0], "stages": dict(cnt), "size": s["size"], "best": s["best"],
                        "ready_now": s["ready_now"], "links": [l["id"] for l in s["links"]],
                        "text": " ".join(" ".join([str(atoms[m["id"]].get("name_en")), str(atoms[m["id"]].get("name_ar")),
                                                   " ".join(atoms[m["id"]].get("tags") or [])]) for m in s["pipeline"]).lower()[:2500]}
    hubs = []
    for h in hx["hubs"]:
        by = collections.OrderedDict((st, []) for st in order)
        for sid in h["superpowers"]:
            by[sps[sid]["stage"]].append(sid)
        for st in by:
            by[st].sort(key=lambda x: (-sps[x]["ready_now"], -sps[x]["size"]))
        hubs.append({"id": h["id"], "ar": h["ar"], "en": h["en"], "stages": {k: v for k, v in by.items() if v}})
    tasks = [task_map(t, sps, hubs, stages) for t in c["tasks"]]
    audit = audit_catalog(atoms, sp, sp_hub)
    data = {"schema": "kosif.mindmap.v1", "stages": stages, "superpowers": sps, "hubs": hubs, "tasks": tasks, "audit": audit,
            "atom_stage_counts": dict(collections.Counter(atom_stage.values()))}
    return data


def task_map(t, sps, hubs, stages, brief=None):
    hub_by = {h["id"]: h for h in hubs}
    words = set(re.findall(r"[a-z0-9:]+|[؀-ۿ]{2,}", (brief or t.get("brief", "")).lower()))
    plan = collections.OrderedDict()
    fallback = {"understand": ["think", "research"], "plan": ["think", "story"], "create": [], "refine": [],
                "assemble": ["render"], "verify": ["render", "think"], "deliver": ["render", "montage"]}

    def ranked(hub_ids, st_id, need_rel):
        out = []
        for hid in hub_ids:
            for sid in hub_by.get(hid, {}).get("stages", {}).get(st_id, []):
                s = sps[sid]
                nm = (s["name_en"] + " " + s["name_ar"]).lower()
                rel = sum(2 for w in words if w in nm) + sum(1 for w in words if w in s.get("text", ""))
                if need_rel and rel == 0:
                    continue
                out.append((-(rel * 20 + min(s["ready_now"], 8) + (3 if s["best"] == "proven" else 0)), hub_ids.index(hid), sid))
        out.sort()
        return [c[2] for c in out]

    for st in stages:
        picks = ranked(t["hubs"], st["id"], True)[:3]
        if not picks:
            picks = ranked([h for h in fallback[st["id"]] if h not in t["hubs"]] or t["hubs"], st["id"], False)[:1]
        if picks:
            plan[st["id"]] = picks
    return {"id": t.get("id", "custom"), "ar": t.get("ar", ""), "en": t.get("en", ""), "hubs": t["hubs"], "plan": plan}


def audit_catalog(atoms, sp, sp_hub):
    norm = lambda s: re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()
    where = {m["id"]: s["id"] for s in sp["items"] for m in s["pipeline"]}
    names = collections.defaultdict(list)
    for i, p in atoms.items():
        names[norm(p.get("name_en"))].append(i)
    same_name = [{"name": n, "ids": ids, "superpowers": sorted({where[i] for i in ids})} for n, ids in names.items() if len(ids) > 1]
    twins = [g for s in sp["items"] for g in s.get("twins") or []]
    # cross-superpower look-alikes: atoms in different superpowers/hubs that are near-identical
    ps = list(atoms.values())
    vec = F.vectors(ps)
    inv = collections.defaultdict(list)
    for k, v in enumerate(vec):
        for w in v:
            inv[w].append(k)
    look = []
    for a, v in enumerate(vec):
        sc = collections.Counter()
        for w, x in v.items():
            if len(inv[w]) > 300:
                continue
            for b in inv[w]:
                if b > a:
                    sc[b] += x * vec[b][w]
        for b, s in sc.items():
            if s >= 0.7 and where[ps[a]["id"]] != where[ps[b]["id"]]:
                look.append({"a": ps[a]["id"], "b": ps[b]["id"], "sim": round(s, 2), "a_sp": where[ps[a]["id"]], "b_sp": where[ps[b]["id"]],
                             "cross_hub": sp_hub.get(where[ps[a]["id"]]) != sp_hub.get(where[ps[b]["id"]]),
                             "name": ps[a]["name_en"], "name_b": ps[b]["name_en"]})
    look.sort(key=lambda x: -x["sim"])
    # co-develop: strongest cross-hub links between superpowers
    co = []
    for s in sp["items"]:
        for l in s["links"]:
            if sp_hub.get(s["id"]) != sp_hub.get(l["id"]) and s["id"] < l["id"]:
                co.append({"a": s["id"], "b": l["id"], "sim": l["sim"], "hubs": [sp_hub.get(s["id"]), sp_hub.get(l["id"])]})
    co.sort(key=lambda x: -x["sim"])
    return {"atoms": len(atoms), "superpowers": sp["superpowers"], "twin_groups": len(twins), "twin_members": sum(len(g) for g in twins),
            "distinct_methods": sp.get("distinct_methods"), "tiny_absorbed": sp.get("tiny_absorbed"),
            "same_name_groups": same_name, "lookalikes_cross_superpower": look[:150], "lookalike_count": len(look),
            "codevelop_pairs": co[:60]}


def mermaid_task(tm, sps, stages):
    lab = {s["id"]: f"{s['ar']} · {s['en']}" for s in stages}
    L = ["```mermaid", "flowchart LR"]
    prev = None
    for n, (st, ids) in enumerate(tm["plan"].items()):
        node = f"S{n}"
        L.append(f'  {node}["{n + 1}. {lab[st]}"]')
        for k, sid in enumerate(ids):
            s = sps[sid]
            nm = re.sub(r'["\[\]()]', " ", f"{sid} {s['name_ar']}")[:60]
            L.append(f'  {node} --- {node}_{k}("{nm}")')
        if prev:
            L.append(f"  {prev} ==> {node}")
        prev = node
    L.append("```")
    return L


def write_docs(d):
    B = P.BADGE
    st = {s["id"]: s for s in d["stages"]}
    order = [s["id"] for s in d["stages"]]
    sps = d["superpowers"]
    L = ["# الخريطة الذهنية للقدرات — Capability mind map", "", "<!-- generated by scripts/capability_mindmap.py build -->", "",
         "كل قدرة مرتبة بحسب **مرحلة المهمة** التي تخدمها، ثم كل بوابة مقسمة بالمراحل، ثم خرائط جاهزة لمهام شائعة. "
         "اتبع المراحل بالترتيب: افهم ← خطّط ← اصنع ← حسّن ← جمّع وارندر ← تحقّق ← سلّم.", "",
         "    python3 scripts/capability_mindmap.py task \"<المهمة>\"     # خريطة مرحلية لأي مهمة",
         "    python3 scripts/capability_mindmap.py task reels-edit      # خريطة جاهزة", "",
         "## الفهرس / contents", "", "- المراحل السبع / the seven stages", "- الخريطة الكبرى / the big map",
         "- خرائط المهام الجاهزة / ready task maps", "- البوابات مرتبة بالمراحل / hubs by stage", "",
         "## المراحل السبع / the seven stages", ""]
    for s in d["stages"]:
        L.append(f"{order.index(s['id']) + 1}. **{s['ar']} — {s['en']}** · {d['atom_stage_counts'].get(s['id'], 0)} قدرة ذرية")
    L += ["", "## الخريطة الكبرى / the big map", "", "```mermaid", "mindmap", "  root((KOSIF Superpowers))"]
    for h in d["hubs"]:
        L.append(f"    {h['ar']}")
        for sid in [x for v in h["stages"].values() for x in v][:0]:
            pass
        for stg, ids in h["stages"].items():
            L.append(f"      {st[stg]['ar']} ({len(ids)})")
    L += ["```", "", "## خرائط المهام الجاهزة / ready task maps", ""]
    for tm in d["tasks"]:
        L += [f"### {tm['ar']} — {tm['en']} (`{tm['id']}`)", "", "البوابات: " + " ← ".join(f"`{h}`" for h in tm["hubs"]), ""]
        L += mermaid_task(tm, sps, d["stages"])
        L.append("")
        for n, (stg, ids) in enumerate(tm["plan"].items(), 1):
            L.append(f"{n}. **{st[stg]['ar']}:** " + " · ".join(f"{i} {B.get(sps[i]['best'], '')} {sps[i]['name_ar']}" for i in ids))
        L.append("")
    L += ["## البوابات مرتبة بالمراحل / hubs by stage", ""]
    for h in d["hubs"]:
        L += [f"### {h['ar']} — {h['en']}", ""]
        for stg, ids in h["stages"].items():
            L.append(f"- **{st[stg]['ar']}** ({len(ids)}): " + " · ".join(f"{i} {sps[i]['name_ar']}" for i in ids[:6]) + (" …" if len(ids) > 6 else ""))
        L.append("")
    L += ["---", "_مولَّد آليًا من data/superpowers.json وdata/hubs_index.json وdata/task_maps.json._", ""]
    DOC.write_text("\n".join(L), encoding="utf-8")
    a = d["audit"]
    A = ["# تدقيق التكرار والدمج — Capability audit", "", "<!-- generated by scripts/capability_mindmap.py build -->", "",
         f"- القدرات الذرية: **{a['atoms']:,}** · الطرق المتمايزة فعلًا: **{a['distinct_methods']:,}** · القدرات الخارقة: **{a['superpowers']}**",
         f"- توائم داخل نفس القدرة الخارقة (تؤدي العمل نفسه): **{a['twin_groups']}** مجموعة تضم {a['twin_members']} قدرة — استخدم الأولى (الأقوى دليلًا).",
         f"- قدرات خارقة صغيرة (≤2) دُمجت في أقرب قدرة: **{a['tiny_absorbed']}**",
         f"- قدرات بالاسم نفسه: **{len(a['same_name_groups'])}** مجموعة · متشابهات قوية عبر قدرات خارقة مختلفة: **{a['lookalike_count']}**", "",
         "## الفهرس / contents", "", "- أسماء مكررة", "- متشابهات عبر القدرات الخارقة", "- أزواج للتطوير المشترك", "",
         "## أسماء مكررة / same-name groups", "", "| الاسم | القدرات | في القدرات الخارقة |", "|---|---|---|"]
    for g in a["same_name_groups"]:
        A.append(f"| {g['name']} | {' = '.join(g['ids'])} | {' · '.join(g['superpowers'])} |")
    A += ["", "## متشابهات عبر القدرات الخارقة / look-alikes (sim ≥ 0.7) — مرشحة للتوحيد", "",
          "| التشابه | القدرة | القدرة | عبر بوابتين؟ |", "|---|---|---|---|"]
    for x in a["lookalikes_cross_superpower"][:80]:
        A.append(f"| {x['sim']} | {x['a']} {x['name'][:40]} ({x['a_sp']}) | {x['b']} {x['name_b'][:40]} ({x['b_sp']}) | {'نعم' if x['cross_hub'] else 'لا'} |")
    A += ["", "## أزواج للتطوير المشترك / develop together (cross-hub links)", "",
          "قدرتان خارقتان من بوابتين مختلفتين تتشاركان المفردات والأدوات: طوّرهما كسلسلة واحدة.", "",
          "| التشابه | القدرة الخارقة | القدرة الخارقة | البوابتان |", "|---|---|---|---|"]
    for x in a["codevelop_pairs"][:40]:
        A.append(f"| {x['sim']} | {x['a']} {sps[x['a']]['name_ar']} | {x['b']} {sps[x['b']]['name_ar']} | {x['hubs'][0]} ↔ {x['hubs'][1]} |")
    A += ["", "---", "_مولَّد آليًا. التوحيد النهائي لأي قدرتين قرار تحريري: راجع الدليل قبل حذف سجل._", ""]
    AUD.write_text("\n".join(A), encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    t = sub.add_parser("task"); t.add_argument("task"); t.add_argument("--mermaid", action="store_true")
    sub.add_parser("audit")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        d = build()
        OUT.write_text(json.dumps(d, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
        write_docs(d)
        au = d["audit"]
        print(f"stages {d['atom_stage_counts']} · {len(d['tasks'])} task maps · twins {au['twin_groups']} · same-name {len(au['same_name_groups'])} · look-alikes {au['lookalike_count']} · co-develop {len(au['codevelop_pairs'])}")
        return 0
    d = json.loads(OUT.read_text(encoding="utf-8"))
    sps, stages = d["superpowers"], d["stages"]
    st = {s["id"]: s for s in stages}
    if a.cmd == "audit":
        au = d["audit"]
        print(f"atoms {au['atoms']} · distinct {au['distinct_methods']} · superpowers {au['superpowers']} · twins {au['twin_groups']} · same-name {len(au['same_name_groups'])} · look-alikes {au['lookalike_count']}")
        for x in au["lookalikes_cross_superpower"][:10]:
            print(f"  {x['sim']} {x['a']} ≈ {x['b']}  {x['name'][:40]} | {x['name_b'][:40]}")
        print("full report: references/capability-audit.md")
        return 0
    tm = next((x for x in d["tasks"] if x["id"] == a.task), None)
    if tm is None:
        import kosif_hubs as H
        idx = json.loads(HUBX.read_text(encoding="utf-8"))
        hubs = [r["hub"]["id"] for r in H.route(idx, a.task, 4)]
        for need in ("render",) if any(h in ("motion", "montage", "draw", "audio", "3d", "type") for h in hubs) else ():
            if need not in hubs:
                hubs.append(need)
        tm = task_map({"id": "custom", "ar": a.task, "en": "", "hubs": hubs}, sps, d["hubs"], stages, brief=a.task)
    print(f"{tm['ar']} {('— ' + tm['en']) if tm['en'] else ''}  · hubs: {' → '.join(tm['hubs'])}")
    for n, (stg, ids) in enumerate(tm["plan"].items(), 1):
        print(f"{n}. {st[stg]['ar']} · {st[stg]['en']}")
        for i in ids:
            s = sps[i]
            print(f"     {i} {P.BADGE.get(s['best'], '')} {s['name_ar']} · {s['name_en']}  ({s['size']}, ready {s['ready_now']})")
    print("details: superpower_fusion.py show <SP>; install: kosif_hubs.py install <hub>")
    if a.mermaid:
        print("\n".join(mermaid_task(tm, sps, stages)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
