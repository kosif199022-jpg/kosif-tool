#!/usr/bin/env python3
"""Transfer verified Atlas-mined capabilities into the KOSIF catalog — نقل القدرات المستخرجة من أطلس.

Reads the verifier outputs of the mining run (JSON files written by the verification agents), keeps the
records whose verdict is `keep`, de-duplicates them, validates their fields against the catalog rules
(requirements registry, domains, family prefixes) and writes data/powers/atlas-<domain>.json.

  python3 atlas_transfer.py build --verify DIR [--verify DIR ...] --out data/powers [--date 2026-10-20] [--force]
  python3 atlas_transfer.py report --verify DIR [--verify DIR ...]        # counts only, nothing written

Badges: every record is 📄 documented or 📦 install — the Atlas methods were read, never executed here.
Python 3.8+ stdlib only; it reads JSON, never Atlas code.
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

ATLAS_REPO = "https://github.com/kosif199022-jpg/kosif-atlas"
FAMILY_BY_DOMAIN = {dom: stem for stem, meta in P.FAMILY_META.items() if stem.startswith("atlas-") for dom in [meta[1]]}
DOMAIN_FOLD = {"motion": "media"}   # motion chapters are hand-made; Atlas video recipes live with media
STOP = {"a", "an", "the", "of", "for", "and", "or", "to", "in", "on", "with", "from", "by", "via", "using", "into", "as", "at"}
ID_RE = re.compile(r"^[A-Za-z0-9-]+$")


def req_keys() -> set:
    p = SKILL / "data" / "requirements.json"
    return {k for k in json.loads(p.read_text(encoding="utf-8")) if not k.startswith("_")} if p.exists() else set()


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def word_key(s: str) -> str:
    w = [x[:-1] if x.endswith("s") and len(x) > 3 else x for x in norm(s).split() if x not in STOP and len(x) > 2]
    return " ".join(sorted(set(w)))


def theme_section(theme: str):
    try:
        import atlas_capability_miner as AM
        meta = AM.THEMES.get(theme) or AM.FALLBACK
        return meta[1], meta[2]
    except Exception:  # noqa: BLE001
        return "عام", "General"


def from_extract(c: dict, fname: str) -> dict:
    """Map an extraction-agent capability to the verifier shape (not yet adversarially verified)."""
    ar, en = theme_section(c.get("theme") or "")
    r = dict(c)
    r.update({"verdict": "keep" if c.get("novelty") != "exists" else "covered", "status": "documented",
              "section_ar": ar, "section_en": en, "license": c.get("license_notes") or "",
              "sources_read": [e.get("path") for e in (c.get("examples") or [])][:3], "_stage": "extracted"})
    if "copyleft" in str(c.get("license_notes") or "").lower() and "mit" not in str(c.get("license_notes") or "").lower():
        r["verdict"] = "drop"
    return r


def load_results(dirs) -> list:
    rows = []
    for d in dirs:
        for f in sorted(Path(d).glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                print("skip %s: %s" % (f, exc), file=sys.stderr)
                continue
            items = data.get("results") if isinstance(data, dict) and "results" in data else \
                [from_extract(c, f.name) for c in (data.get("capabilities") or [])] if isinstance(data, dict) else []
            for r in items:
                r = dict(r)
                r["_file"] = f.name
                rows.append(r)
    return rows


def clean_text(s, limit) -> str:
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s[:limit].rstrip()


def atlas_url(path: str) -> str:
    return ATLAS_REPO + "/tree/main/" + path.strip("/")


def build(rows: list, date: str, known_req: set) -> dict:
    """verifier rows → {family stem: [records]} plus a build report."""
    report = collections.Counter()
    kept = []
    seen_name, seen_words = {}, {}
    for r in rows:
        v = r.get("verdict")
        report["verdict:" + str(v)] += 1
        if v != "keep":
            continue
        dom = DOMAIN_FOLD.get(str(r.get("domain") or "").strip(), str(r.get("domain") or "").strip())
        if dom not in FAMILY_BY_DOMAIN:
            report["dropped:unknown-domain"] += 1
            continue
        if not (r.get("name_en") and r.get("name_ar") and r.get("how") and r.get("what_en")):
            report["dropped:missing-fields"] += 1
            continue
        k1 = dom + "|" + norm(r["name_en"])
        k2 = dom + "|" + word_key(r["name_en"])
        prev = seen_name.get(k1) or seen_words.get(k2)
        if prev is not None:
            # merge supporting ids into the earlier record, keep the longer how
            prev["_ids"] |= {str(x) for x in (r.get("atlas_ids") or [])}
            for e in r.get("examples") or []:
                if len(prev["_examples"]) < 6 and not any(x.get("path") == e.get("path") for x in prev["_examples"]):
                    prev["_examples"].append(e)
            if len(str(r.get("how") or "")) > len(str(prev.get("how") or "")):
                prev["how"] = r["how"]
            report["merged-duplicate"] += 1
            continue
        r = dict(r)
        r["_dom"] = dom
        r["_ids"] = {str(x) for x in (r.get("atlas_ids") or [])}
        r["_examples"] = list(r.get("examples") or [])[:6]
        seen_name[k1] = r
        seen_words[k2] = r
        kept.append(r)
    families = collections.OrderedDict((stem, []) for stem in FAMILY_BY_DOMAIN.values())
    by_fam = collections.defaultdict(list)
    for r in kept:
        by_fam[FAMILY_BY_DOMAIN[r["_dom"]]].append(r)
    for stem in families:
        rs = by_fam.get(stem, [])
        rs.sort(key=lambda x: (norm(x.get("section_en") or ""), norm(x.get("name_en"))))
        prefix = P.FAMILY_META[stem][0]
        for i, r in enumerate(rs, 1):
            req = []
            for k in r.get("requires") or []:
                k = str(k).strip()
                if k in known_req:
                    if k not in req:
                        req.append(k)
                else:
                    report["requires-unknown-dropped"] += 1
            status = r.get("status") if r.get("status") in ("documented", "install") else "documented"
            if status == "install" and not (r.get("install") or "").strip():
                status = "documented"
            examples = [e for e in r["_examples"] if e.get("path")]
            ex_txt = "; ".join("%s/%s (#%s)" % (e.get("plugin"), e.get("skill"), e.get("id")) for e in examples[:4])
            section = "%s — %s" % (clean_text(r.get("section_ar") or "عام", 60), clean_text(r.get("section_en") or "General", 60))
            lic = clean_text(r.get("license") or "see Atlas SOURCE.md", 80)
            rec = collections.OrderedDict([
                ("id", "%s-%02d" % (prefix, i)),
                ("family", stem),
                ("domain", P.FAMILY_META[stem][1]),
                ("name_ar", clean_text(r["name_ar"], 90)),
                ("name_en", clean_text(r["name_en"], 90)),
                ("status", status),
                ("what", "%s — %s" % (clean_text(r.get("what_ar"), 300), clean_text(r.get("what_en"), 300))),
                ("when", clean_text(r.get("when"), 300)),
                ("how", clean_text(r.get("how"), 1200)),
                ("params", clean_text(r.get("params"), 300)),
                ("install", clean_text(r.get("install"), 200)),
                ("requires", req),
                ("license", "method paraphrased from Atlas skills under %s; the skills keep their own licenses — see each folder's SOURCE.md" % lic),
                ("proof", [atlas_url(e["path"]) for e in examples[:3]]),
                ("proof_scope", "url"),
                ("styles", []),
                ("tags", [clean_text(t, 40) for t in (r.get("tags") or [])[:8] if str(t).strip()]),
                ("section", section),
                ("source", "KOSIF Atlas mining %s (%s): %s%s · theme %s · %d supporting skills · verifier read: %s"
                 % (date, ATLAS_REPO, ex_txt, " …" if len(examples) > 4 else "", r.get("theme") or "", len(r["_ids"]),
                    ", ".join(str(s) for s in (r.get("sources_read") or [])[:3]) or "—")),
                ("atlas", collections.OrderedDict([
                    ("ids", sorted(r["_ids"], key=lambda x: (len(x), x))[:40]),
                    ("examples", [{"id": str(e.get("id")), "plugin": e.get("plugin"), "skill": e.get("skill"), "url": atlas_url(e["path"])} for e in examples]),
                    ("theme", r.get("theme") or ""),
                    ("risk_notes", clean_text(r.get("risk_notes"), 240)),
                    ("kosif_overlap_ids", [str(x) for x in (r.get("kosif_overlap_ids") or [])[:8]]),
                    ("stage", r.get("_stage") or "verified"),
                    ("verified_by", r.get("_file")),
                ])),
            ])
            families[stem].append(rec)
            report["records:" + stem] += 1
    report["records:total"] = sum(len(v) for v in families.values())
    return {"families": families, "report": dict(report)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "report"):
        s = sub.add_parser(name)
        s.add_argument("--verify", action="append", required=True, help="directory of verifier JSON files (repeatable)")
        if name == "build":
            s.add_argument("--out", type=Path, default=SKILL / "data" / "powers")
            s.add_argument("--date", default="2026-10-20")
            s.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    rows = load_results(a.verify)
    res = build(rows, getattr(a, "date", "2026-10-20"), req_keys())
    if a.cmd == "report":
        print(json.dumps(res["report"], ensure_ascii=False, indent=1))
        return 0
    for stem, recs in res["families"].items():
        out = a.out / (stem + ".json")
        if out.exists() and not a.force:
            print("refusing to overwrite %s (use --force)" % out, file=sys.stderr)
            return 1
    for stem, recs in res["families"].items():
        out = a.out / (stem + ".json")
        if not recs:
            if out.exists():
                out.unlink()
            continue
        out.write_text(json.dumps(recs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("wrote %s: %d records" % (out, len(recs)))
    print(json.dumps(res["report"], ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
