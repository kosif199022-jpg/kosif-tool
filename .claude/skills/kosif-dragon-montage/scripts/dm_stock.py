#!/usr/bin/env python3
"""Station «مكتبة اللقطات المفتوحة»: search open-licence footage sites (Pexels, Pixabay, Mixkit, Coverr,
Wikimedia Commons, Internet Archive, NASA, Library of Congress…) and bring licensed clips into the job.

Runs only when the owner asks for it (`dragon_montage.py edit … --stock "<english query>"`). It reuses
kosif-superpowers/scripts/free_footage.py (database: data/free_footage_sources.json, the 129-site
catalog data/free_media_catalog.json) so every clip keeps a licence sidecar and ATTRIBUTION.md.
Free sites only: paid stock is never searched, and nothing is bought or uploaded.

  dm_stock.py search --job DIR --query "coffee pouring" [--limit 4] [--commercial] [--orientation portrait]
  dm_stock.py fetch  --job DIR [--top 3 | --ids mixkit:41865,coverr:abc] [--quality 1080] [--max-mb 200]
  dm_stock.py sources [--find WORD]          # list the free sites and their licences (offline)

Pexels/Pixabay need PEXELS_API_KEY / PIXABAY_API_KEY in the environment; the other sites need no key.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402

FF = C.SP / "free_footage.py"
STATION = "stock"
SCHEMA = "kosif.dm.stock.v1"
VIDEO_EXT = {".mp4", ".mov", ".webm", ".m4v", ".mkv"}


def orientation_for(job: Path) -> str | None:
    try:
        aspect = C.read(job, "brief").get("aspect")
    except (FileNotFoundError, C.ContractError):
        return None
    return {"9:16": "portrait", "4:5": "portrait", "16:9": "landscape", "1:1": None}.get(aspect)


def rank(r: dict) -> tuple:
    lic = r.get("licence") or {}
    w, h = r.get("width") or 0, r.get("height") or 0
    return (not lic.get("verified"), lic.get("commercial") is not True, bool(lic.get("attribution_required")),
            "suspicious-licence" in (r.get("flags") or []), -(w * h))


def cmd_search(a) -> int:
    job = C.job_dir(a.job)
    argv = [*C.py(FF), "search", a.query, "--limit", str(a.limit), "--match", "any"]
    orient = a.orientation or orientation_for(job)
    if orient:
        argv += ["--orientation", orient]
    if a.commercial:
        argv += ["--commercial"]
    res = C.run(job, STATION, "free_footage.search", argv, timeout=600, owner_media=False, check=False, cwd=job)
    found = job / "out" / "free-footage" / "last_search.json"
    data = json.loads(found.read_text(encoding="utf-8")) if found.exists() else {"results": []}
    results = sorted(data.get("results", []), key=rank)
    out = {"schema": SCHEMA, "query": a.query, "orientation": orient, "commercial_only": a.commercial,
           "results": results, "searched": data.get("searches") or data.get("sources"),
           "warnings": data.get("warnings", []), "downloaded": [], "rc": res.returncode,
           "note": "licences are what each site declares; the tool records them, it does not grant them"}
    (job / "stock.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"results": len(results), "top": [r["id"] for r in results[:5]]}, ensure_ascii=False))
    return 0 if results or res.returncode == 0 else 1


def cmd_fetch(a) -> int:
    job = C.job_dir(a.job)
    stock = json.loads((job / "stock.json").read_text(encoding="utf-8"))
    ids = [i for i in (a.ids or "").split(",") if i] or [r["id"] for r in stock["results"][:a.top]]
    if not ids:
        print(json.dumps({"downloaded": []}))
        return 0
    dest = job / "stock"
    dest.mkdir(exist_ok=True)
    before = {p.name for p in dest.iterdir()}
    C.run(job, STATION, "free_footage.download",
          [*C.py(FF), "download", *ids, "--out", dest, "--quality", str(a.quality), "--max-mb", str(a.max_mb)],
          timeout=1800, owner_media=False, check=False, cwd=job)
    new = sorted(p for p in dest.iterdir() if p.suffix.lower() in VIDEO_EXT and p.name not in before)
    got = []
    for p in new:
        side = p.with_name(p.name + ".json")
        if not side.exists():
            side = p.with_suffix(".json")
        meta = json.loads(side.read_text(encoding="utf-8")) if side.exists() else {}
        got.append({"path": str(p), "id": meta.get("id"), "licence": meta.get("licence"),
                    "attribution": meta.get("attribution")})
    stock["downloaded"] += got
    stock["attribution_file"] = str((dest / "ATTRIBUTION.md").relative_to(job)) if (dest / "ATTRIBUTION.md").exists() else None
    (job / "stock.json").write_text(json.dumps(stock, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"downloaded": [g["path"] for g in got]}, ensure_ascii=False))
    return 0


def cmd_sources(a) -> int:
    argv = [sys.executable, str(FF), "sources"] + (["--find", a.find] if a.find else [])
    return subprocess.call(argv)


def main(argv=None) -> int:
    C.utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--job", required=True)
    s.add_argument("--query", required=True, help="English words work best on these sites")
    s.add_argument("--limit", type=int, default=4, help="results per site")
    s.add_argument("--orientation", choices=("portrait", "landscape"))
    s.add_argument("--commercial", action="store_true", help="drop NC / restricted / unverified licences")
    f = sub.add_parser("fetch")
    f.add_argument("--job", required=True)
    f.add_argument("--top", type=int, default=3)
    f.add_argument("--ids")
    f.add_argument("--quality", type=int, default=1080)
    f.add_argument("--max-mb", type=int, default=200)
    o = sub.add_parser("sources")
    o.add_argument("--find")
    a = p.parse_args(argv)
    if not shutil.which("ffprobe"):
        sys.stderr.write("note: ffprobe missing; sizes may be unknown\n")
    return {"search": cmd_search, "fetch": cmd_fetch, "sources": cmd_sources}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
