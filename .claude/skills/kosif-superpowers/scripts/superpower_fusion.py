#!/usr/bin/env python3
"""KOSIF Superpower Fusion — دمج القدرات في قدرات خارقة أكبر وأقوى ومترابطة.

Fuses the atomic powers of data/powers/*.json into fewer, larger SUPERPOWERS. Every atomic power belongs to
exactly one superpower; superpowers are linked to each other (a connected graph) so one request can travel
from a superpower to its neighbours. Atomic records are not deleted: their IDs, proofs and badges stay the
evidence layer, and each superpower carries the full member list.

  python3 superpower_fusion.py build [--per 12]      # write data/superpowers.json + references/superpowers.md
  python3 superpower_fusion.py stats
  python3 superpower_fusion.py suggest "مونتاج ريلز بإيقاع الموسيقى" [--top 5]
  python3 superpower_fusion.py show SP-0042
  python3 superpower_fusion.py of ID                  # which superpower holds atomic power ID

Method (deterministic, stdlib): TF-IDF over name/tags/section/what → per family spherical k-means
(k = ceil(n/per), farthest-point seeding, 8 iterations, no empty clusters) → Atlas-mined families
(atlas-*) are folded into the closest native superpower of the same domain when similar enough →
links = top-4 most similar superpowers (cosine of centroids) + shared requirements.
Badge honesty: a superpower shows the status mix of its members; `best` is the strongest member badge,
never a claim that every member reaches it.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
import powers as P  # noqa: E402

OUT = SKILL / "data" / "superpowers.json"
DOC = SKILL / "references" / "superpowers.md"
STOP = set("the a an of and or to in on with for from by via as at is are be use using into one each this that when it its "
           "your you per not no all any more less new can how what then than only also over under out up".split())
RANK = {s: i for i, s in enumerate(P.STATUSES)}
FOLD_MIN = 0.18
LINKS = 4
TWIN = 0.62


def toks(s):
    s = str(s or "").lower()
    return [w for w in re.findall(r"[a-z][a-z0-9+#.-]{2,}|[؀-ۿ]{3,}", s) if w not in STOP]


def vectors(ps):
    docs = []
    for p in ps:
        c = collections.Counter()
        for w in toks(p.get("name_en")):
            c[w] += 3
        for w in toks(p.get("name_ar")):
            c[w] += 2
        for t in p.get("tags") or []:
            for w in toks(t):
                c[w] += 2
        for w in toks(p.get("section")):
            c[w] += 1.5
        for w in toks(str(p.get("what") or "").split(" — ")[-1])[:40]:
            c[w] += 1
        docs.append(c)
    df = collections.Counter(w for d in docs for w in d)
    n = len(docs)
    out = []
    for d in docs:
        v = {w: x * math.log(n / (1 + df[w])) for w, x in d.items() if df[w] > 1}
        nv = math.sqrt(sum(x * x for x in v.values())) or 1.0
        out.append({w: x / nv for w, x in v.items()})
    return out


def dot(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())


def centroid(vs):
    c = collections.Counter()
    for v in vs:
        for w, x in v.items():
            c[w] += x
    top = dict(c.most_common(60))
    n = math.sqrt(sum(x * x for x in top.values())) or 1.0
    return {w: x / n for w, x in top.items()}


def kmeans(idx, vec, k):
    if k <= 1 or len(idx) <= 1:
        return [list(idx)]
    # farthest-point seeding from the member closest to the family centroid
    fam_c = centroid([vec[i] for i in idx])
    seeds = [max(idx, key=lambda i: (dot(vec[i], fam_c), -i))]
    best = {i: dot(vec[i], vec[seeds[0]]) for i in idx}
    while len(seeds) < k:
        s = min((i for i in idx if i not in seeds), key=lambda i: (best[i], i))
        seeds.append(s)
        for i in idx:
            best[i] = max(best[i], dot(vec[i], vec[s]))
    cents = [vec[s] for s in seeds]
    assign = {}
    for _ in range(8):
        groups = [[] for _ in cents]
        for i in idx:
            j = max(range(len(cents)), key=lambda j: (dot(vec[i], cents[j]), -j))
            groups[j].append(i)
        # no empty clusters: re-seed with the worst-fitting member of the largest group
        for j, g in enumerate(groups):
            if not g:
                big = max(range(len(groups)), key=lambda x: len(groups[x]))
                worst = min(groups[big], key=lambda i: (dot(vec[i], cents[big]), i))
                groups[big].remove(worst)
                g.append(worst)
        new = {i: j for j, g in enumerate(groups) for i in g}
        cents = [centroid([vec[i] for i in g]) for g in groups]
        if new == assign:
            break
        assign = new
    return [g for g in groups if g]


def name_terms(members, vec_c, ps):
    """Medoid member gives the name; 3 strongest centroid terms give the subtitle."""
    medoid = max(members, key=lambda i: (dot(VEC[i], vec_c), -RANK.get(ps[i].get("status"), 9), -i))
    return medoid


def build(per=12):
    global VEC
    ps = P.load_powers()
    ps.sort(key=lambda p: (p.get("family"), p.get("id")))
    VEC = vectors(ps)
    fam = collections.OrderedDict()
    for i, p in enumerate(ps):
        fam.setdefault(p["family"], []).append(i)
    native = {f: ix for f, ix in fam.items() if not f.startswith("atlas-")}
    atlas = {f: ix for f, ix in fam.items() if f.startswith("atlas-")}
    groups = []
    for f, ix in native.items():
        k = max(1, math.ceil(len(ix) / per))
        for g in kmeans(ix, VEC, k):
            groups.append({"family": f, "members": g})
    for g in groups:
        g["c"] = centroid([VEC[i] for i in g["members"]])
        g["domain"] = ps[g["members"][0]].get("domain") or "motion"
    folded = 0
    for f, ix in atlas.items():
        dom = ps[ix[0]].get("domain")
        cands = [g for g in groups if g["domain"] == dom and not g["family"].startswith("atlas-")]
        rest = []
        for i in ix:
            best = max(cands, key=lambda g: dot(VEC[i], g["c"])) if cands else None
            if best is not None and dot(VEC[i], best["c"]) >= FOLD_MIN:
                best["members"].append(i)
                best.setdefault("atlas_folded", 0)
                best["atlas_folded"] += 1
                folded += 1
            else:
                rest.append(i)
        if rest:
            for g in kmeans(rest, VEC, max(1, math.ceil(len(rest) / per))):
                groups.append({"family": f, "members": g, "domain": dom, "c": centroid([VEC[i] for i in g])})
    for g in groups:
        g["c"] = centroid([VEC[i] for i in g["members"]])
    # stable order: domain order, family, then size
    dom_order = {d: n for n, d in enumerate(P.DOMAINS)}
    groups.sort(key=lambda g: (dom_order.get(g["domain"], 99), g["family"], -len(g["members"]), min(ps[i]["id"] for i in g["members"])))
    sps = []
    for n, g in enumerate(groups, 1):
        mem = sorted(g["members"], key=lambda i: (RANK.get(ps[i].get("status"), 9), -dot(VEC[i], g["c"]), ps[i]["id"]))
        med = max(mem, key=lambda i: (dot(VEC[i], g["c"]), -RANK.get(ps[i].get("status"), 9), ps[i]["id"]))
        terms = [w for w, _ in sorted(g["c"].items(), key=lambda kv: -kv[1]) if re.match(r"[a-z]", w)][:4]
        mix = collections.Counter(ps[i].get("status") for i in mem)
        req = collections.Counter(r for i in mem for r in (ps[i].get("requires") or []))
        fams = collections.Counter(ps[i]["family"] for i in mem)
        proofs = []
        for i in mem:
            for pr in ps[i].get("proof") or []:
                if ps[i].get("status") == "proven" and pr not in proofs and len(proofs) < 4:
                    proofs.append(pr)
        best = min(mix, key=lambda s: RANK.get(s, 9))
        # twins: members that do the same job (near-identical vectors) — use the first (strongest badge), skip the rest
        twins, used = [], set()
        for x in mem:
            if x in used:
                continue
            grp = [y for y in mem if y != x and y not in used and dot(VEC[x], VEC[y]) >= TWIN]
            if grp:
                used.update(grp + [x])
                twins.append([ps[x]["id"]] + [ps[y]["id"] for y in grp])
        sps.append({
            "id": "SP-%04d" % n, "domain": g["domain"], "family": g["family"],
            "name_ar": ps[med].get("name_ar"), "name_en": ps[med].get("name_en"),
            "focus": terms, "size": len(mem), "best": best,
            "status_mix": {s: mix[s] for s in P.STATUSES if mix.get(s)},
            "ready_now": sum(mix[s] for s in ("proven", "ready")),
            "families": dict(fams.most_common()), "atlas_folded": sum(1 for i in mem if ps[i]["family"].startswith("atlas-")),
            "requires": [r for r, _ in req.most_common(8)],
            "pipeline": [{"id": ps[i]["id"], "status": ps[i].get("status"), "name_en": ps[i].get("name_en"), "name_ar": ps[i].get("name_ar")} for i in mem],
            "proof": proofs, "twins": twins, "distinct_methods": len(mem) - sum(len(g) - 1 for g in twins), "_c": g["c"],
        })
    # links: top-N centroid neighbours (any family) + strongest cross-domain neighbour
    for a in sps:
        sims = sorted(((dot(a["_c"], b["_c"]), b["id"], b["domain"]) for b in sps if b is not a), reverse=True)
        links = [(round(s, 3), bid) for s, bid, _d in sims[:LINKS]]
        cross = next(((round(s, 3), bid) for s, bid, d in sims if d != a["domain"]), None)
        if cross and cross[1] not in [l[1] for l in links]:
            links.append(cross)
        a["links"] = [{"id": bid, "sim": s} for s, bid in links]
    for a in sps:
        a.pop("_c")
    atoms = len(ps)
    comp = connected(sps)
    data = {"schema": "kosif.superpowers.v1", "atoms": atoms, "distinct_methods": sum(s["distinct_methods"] for s in sps),
            "twin_groups": sum(len(s["twins"]) for s in sps), "superpowers": len(sps), "per_target": per,
            "fusion_ratio": round(atoms / max(1, len(sps)), 2), "atlas_folded_into_native": folded,
            "graph_components": comp,
            "note": ("Each atomic power belongs to exactly one superpower; atomic IDs, proofs and badges stay the evidence. "
                     "'best' = strongest member badge, status_mix = honest distribution. Built by scripts/superpower_fusion.py."),
            "items": sps}
    return data


def connected(sps):
    adj = collections.defaultdict(set)
    for a in sps:
        for l in a["links"]:
            adj[a["id"]].add(l["id"])
            adj[l["id"]].add(a["id"])
    seen, comps = set(), 0
    for a in sps:
        if a["id"] in seen:
            continue
        comps += 1
        stack = [a["id"]]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(adj[x] - seen)
    return comps


def write_doc(data):
    B = P.BADGE
    L = ["# القدرات الخارقة المدمجة — Fused superpowers", "",
         "<!-- generated by scripts/superpower_fusion.py; edit the power JSON and rebuild, not this file -->", "",
         f"> **{data['atoms']:,}** قدرة ذرية دُمجت في **{data['superpowers']:,}** قدرة خارقة (متوسط {data['fusion_ratio']} قدرة لكل واحدة)، "
         f"وكل قدرة خارقة مرتبطة بأقرب جيرانها؛ الرسم كله {data['graph_components']} مكوّن مترابط. "
         f"{data['atlas_folded_into_native']} قدرة من أطلس انصهرت داخل قدرات KOSIF الأصلية.",
         f"> {data['atoms']:,} atomic powers fused into {data['superpowers']:,} superpowers, each linked to its nearest neighbours.", "",
         "**كيف تستخدمها / how:** `python3 scripts/superpower_fusion.py suggest \"<المهمة>\"` يختار القدرات الخارقة، ثم `show SP-xxxx` "
         "يعرض خط التنفيذ (أعضاؤها مرتبة: ✅ أولًا) وروابطها. الشارة `best` أقوى عضو، و`status_mix` التوزيع الصادق.", "",
         "## الفهرس / contents", ""]
    by_dom = collections.OrderedDict()
    for s in data["items"]:
        by_dom.setdefault(s["domain"], []).append(s)
    for d, rows in by_dom.items():
        ar, en = P.DOMAINS.get(d, (d, d))
        L.append(f"- **{ar} — {en}** ({len(rows)} superpowers, {sum(r['size'] for r in rows)} powers)")
    for d, rows in by_dom.items():
        ar, en = P.DOMAINS.get(d, (d, d))
        L += ["", f"## {ar} — {en}", "", "| id | القدرة الخارقة / superpower | حجم | أفضل | جاهز الآن | يرتبط بـ |", "|---|---|---|---|---|---|"]
        for s in rows:
            mix = " ".join(f"{B[k]}{v}" for k, v in s["status_mix"].items())
            links = " ".join(l["id"] for l in s["links"])
            nm = f"{s['name_ar']} · {s['name_en']} <sub>({', '.join(s['focus'])})</sub>".replace("|", "/")
            L.append(f"| {s['id']} | {nm} | {s['size']} | {B.get(s['best'], '')} {mix} | {s['ready_now']} | {links} |")
    L += ["", "---", "_مولَّد آليًا — Generated by `python3 scripts/superpower_fusion.py build`._", ""]
    return "\n".join(L)


def load():
    return json.loads(OUT.read_text(encoding="utf-8"))


def suggest(data, brief, top=5):
    q = collections.Counter(toks(brief))
    try:
        sp = P.suggest(P.load_powers(), [], brief, 40)
        hit = collections.Counter()
        where = {m["id"]: s["id"] for s in data["items"] for m in s["pipeline"]}
        for rank, (score, p) in enumerate(sp["picked"]):
            if p["id"] in where:
                hit[where[p["id"]]] += max(1.0, float(score)) / (1 + rank * 0.15)
    except Exception:  # noqa: BLE001
        hit = collections.Counter()
    for s in data["items"]:
        t = " ".join(s["focus"]) + " " + str(s["name_en"]).lower()
        hit[s["id"]] += sum(1.5 for w in q if w in t)
    by = {s["id"]: s for s in data["items"]}
    return [by[i] for i, _ in hit.most_common(top) if _ > 0]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--per", type=int, default=12)
    sub.add_parser("stats")
    s = sub.add_parser("suggest"); s.add_argument("brief"); s.add_argument("--top", type=int, default=5); s.add_argument("--json", action="store_true")
    sh = sub.add_parser("show"); sh.add_argument("id"); sh.add_argument("--json", action="store_true")
    o = sub.add_parser("of"); o.add_argument("id")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        data = build(a.per)
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
        DOC.write_text(write_doc(data), encoding="utf-8")
        print(f"{data['atoms']} atomic powers ({data['distinct_methods']} distinct after {data['twin_groups']} twin groups) → {data['superpowers']} superpowers (×{data['fusion_ratio']}), "
              f"{data['atlas_folded_into_native']} Atlas powers folded into native ones, graph components {data['graph_components']}")
        return 0
    data = load()
    if a.cmd == "stats":
        dom = collections.Counter(s["domain"] for s in data["items"])
        print(f"atoms {data['atoms']} · superpowers {data['superpowers']} · ratio {data['fusion_ratio']} · components {data['graph_components']}")
        print("domains: " + " · ".join(f"{d} {dom[d]}" for d in P.DOMAINS if dom.get(d)))
        sz = collections.Counter(min(s["size"], 25) for s in data["items"])
        print("sizes: " + " ".join(f"{k}:{v}" for k, v in sorted(sz.items())))
        return 0
    if a.cmd == "of":
        for s in data["items"]:
            if any(m["id"] == a.id for m in s["pipeline"]):
                print(s["id"], s["name_ar"], "·", s["name_en"]); return 0
        print("not found"); return 1
    if a.cmd == "show":
        s = next((x for x in data["items"] if x["id"] == a.id.upper()), None)
        if not s:
            print("not found"); return 1
        if a.json:
            print(json.dumps(s, ensure_ascii=False, indent=1)); return 0
        print(f"{s['id']} · {s['name_ar']} · {s['name_en']}  [{s['domain']}/{s['family']}]  focus: {', '.join(s['focus'])}")
        print("status: " + " ".join(f"{P.BADGE[k]}{v}" for k, v in s["status_mix"].items()) + f" · ready now {s['ready_now']} · needs: {', '.join(s['requires']) or '—'}")
        for m in s["pipeline"]:
            print(f"  {P.BADGE.get(m['status'], '')} {m['id']:<10} {m['name_en']}")
        for g in s.get("twins") or []:
            print("  twins (same job, keep the first): " + " = ".join(g))
        print("links: " + " · ".join(f"{l['id']} ({l['sim']})" for l in s["links"]))
        return 0
    if a.cmd == "suggest":
        res = suggest(data, a.brief, a.top)
        if a.json:
            print(json.dumps([{k: s[k] for k in ("id", "name_ar", "name_en", "domain", "size", "best", "status_mix", "links")} for s in res], ensure_ascii=False, indent=1)); return 0
        for s in res:
            print(f"{s['id']} {P.BADGE.get(s['best'], '')} {s['name_ar']} · {s['name_en']} ({s['size']} powers) → links {' '.join(l['id'] for l in s['links'][:3])}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
