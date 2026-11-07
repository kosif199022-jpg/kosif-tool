#!/usr/bin/env python3
"""Free media catalog: the montage source list, filterable by kind, licence, credit rule and topic.

قائمة المواقع المجانية التي نستعين بمحتواها في المونتاج: فيديو وصور ومؤثرات وأرشيفات ومتاحف وفضاء وخامات
وموسيقى ومؤثرات صوتية ورسوم، لكل موقع ترخيصه وهل التجاري مسموح وهل النسب لازم.

Subcommands:
  sections                     the sections and topics with their counts (offline)
  list  [--section S] [--topic T] [--commercial] [--no-credit] [--star] [--origin user-100|extra]
        [--reachable] [--json]  filter the catalog (offline)
  find  WORDS... [--json]      match name, id, url, note, licence, section or topic (offline)
  show  ID                     one record in full (offline)
  links QUERY [--topic T] [--section S] [--commercial]
                               ready search links on the sites that have a search URL (offline)
  check                        validate data/free_media_catalog.json (ids, urls, enums, tool references)
  probe [--ids a,b] [--delay S]
                               re-measure reachability with one GET per site (network; prints, never writes)

The searching and downloading with a licence sidecar stays in free_footage.py (video) and free_photos.py (photos);
'tools' on each record names which of them already covers that site. A listed site is not a licence for a file:
'per-item' means read the file's own page. Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
DB_PATH = SK / "data" / "free_media_catalog.json"
FOOTAGE_DB = SK / "data" / "free_footage_sources.json"
SCHEMA = "kosif.free-media-catalog.v1"
TIERS = ("free", "freemium", "free-section", "aggregator")
COMMERCIAL = ("yes", "per-item", "limited", "no")
CREDIT = ("no", "yes", "requested", "per-item")
ORIGINS = ("user-100", "extra")
REACH = ("ok", "blocked-from-cloud", "timeout", "no-dns")
REQUIRED = ("id", "name", "url", "section", "star", "tier", "licence", "commercial", "credit", "topics", "tools",
            "note_ar", "origin", "reach")
PHOTO_SOURCES = ("openverse", "wikimedia", "nasa", "met", "pexels", "pixabay", "unsplash")  # free_photos.SOURCES
CREDIT_AR = {"no": "غير لازم", "yes": "لازم", "requested": "مستحب", "per-item": "حسب الملف"}
COMMERCIAL_AR = {"yes": "مسموح", "per-item": "حسب الملف", "limited": "بقيود", "no": "غير تجاري فقط"}


def load(path: Path = DB_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def url_key(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    host = (p.hostname or "").lower()
    host = host[4:] if host.startswith("www.") else host
    return host + p.path.rstrip("/") + ("?" + p.query if p.query else "")


def problems(db: dict, footage_ids=None) -> list:
    """Every structural problem in the catalog (empty list = valid)."""
    out = []
    if db.get("schema") != SCHEMA:
        out.append(f"schema must be {SCHEMA}")
    sections, topics = db.get("sections") or {}, db.get("topics") or {}
    seen_ids, seen_urls = set(), {}
    srcs = db.get("sources") or []
    if not srcs:
        out.append("sources is empty")
    for i, s in enumerate(srcs):
        where = f"sources[{i}] {s.get('id', '?')}"
        for k in REQUIRED:
            if k not in s:
                out.append(f"{where}: missing {k}")
        if any(k not in s for k in REQUIRED):
            continue
        if s["id"] in seen_ids:
            out.append(f"{where}: duplicate id")
        seen_ids.add(s["id"])
        p = urllib.parse.urlsplit(s["url"])
        if p.scheme != "https" or not p.hostname:
            out.append(f"{where}: url must be https")
        k = url_key(s["url"])
        if k in seen_urls:
            out.append(f"{where}: same url as {seen_urls[k]}")
        seen_urls[k] = s["id"]
        if s["section"] not in sections:
            out.append(f"{where}: unknown section {s['section']}")
        for t in s["topics"]:
            if t not in topics:
                out.append(f"{where}: unknown topic {t}")
        for field, allowed in (("tier", TIERS), ("commercial", COMMERCIAL), ("credit", CREDIT),
                               ("origin", ORIGINS), ("reach", REACH)):
            if s[field] not in allowed:
                out.append(f"{where}: {field} {s[field]!r} not in {allowed}")
        lic = s["licence"]
        if not isinstance(lic, dict) or not lic.get("name"):
            out.append(f"{where}: licence needs a name")
        elif lic.get("url") and not str(lic["url"]).startswith("https://"):
            out.append(f"{where}: licence url must be https")
        su = s.get("search_url")
        if su is not None and ("{q}" not in su or not su.startswith("https://")):
            out.append(f"{where}: search_url must be https and contain {{q}}")
        if not str(s["note_ar"]).strip():
            out.append(f"{where}: note_ar is empty")
        for t in s["tools"]:
            tool, _, ref = t.partition(":")
            if tool == "free_footage" and footage_ids is not None and ref not in footage_ids:
                out.append(f"{where}: {t} is not in free_footage_sources.json")
            elif tool == "free_photos" and ref not in PHOTO_SOURCES:
                out.append(f"{where}: {t} is not a free_photos source")
            elif tool not in ("free_footage", "free_photos", "media_sources"):
                out.append(f"{where}: unknown tool {t}")
    counts = db.get("counts") or {}
    n_user = sum(1 for s in srcs if s.get("origin") == "user-100")
    if counts.get("total") != len(srcs) or counts.get("user_list") != n_user:
        out.append(f"counts out of date: total {len(srcs)}, user_list {n_user}")
    return out


def select(db: dict, section=None, topic=None, commercial=False, no_credit=False, star=False, origin=None,
           reachable=False) -> list:
    rows = []
    for s in db["sources"]:
        if section and s["section"] != section:
            continue
        if topic and topic not in s["topics"]:
            continue
        if commercial and s["commercial"] != "yes":
            continue
        if no_credit and s["credit"] not in ("no", "requested"):
            continue
        if star and not s["star"]:
            continue
        if origin and s["origin"] != origin:
            continue
        if reachable and s["reach"] == "no-dns":
            continue
        rows.append(s)
    return rows


def find(db: dict, words: list) -> list:
    terms = [w.lower() for w in words if w.strip()]
    hits = []
    for s in db["sources"]:
        hay = " ".join([s["id"], s["name"], s["url"], s["note_ar"], s["licence"]["name"], s["section"],
                        db["sections"].get(s["section"], ""), " ".join(s["topics"]),
                        " ".join(db["topics"].get(t, "") for t in s["topics"])]).lower()
        if all(t in hay for t in terms):
            hits.append(s)
    return hits


def line(s: dict) -> str:
    star = "⭐" if s["star"] else "  "
    flag = {"no-dns": "  [النطاق لا يستجيب]", "timeout": "  [لم يستجب من السحابة]"}.get(s["reach"], "")
    return (f"{star} {s['id']:<22} {s['name']:<34} تجاري: {COMMERCIAL_AR[s['commercial']]:<12} "
            f"النسب: {CREDIT_AR[s['credit']]:<9} {s['url']}{flag}")


def print_rows(db: dict, rows: list) -> None:
    by = {}
    for s in rows:
        by.setdefault(s["section"], []).append(s)
    for sec, items in by.items():
        print(f"\n## {db['sections'][sec]} ({len(items)})")
        for s in items:
            print(line(s))
    print(f"\n{len(rows)} موقع / sites. {db['notice']}")


def search_links(db: dict, query: str, rows: list) -> list:
    q = urllib.parse.quote(query.strip())
    return [(s, s["search_url"].replace("{q}", q)) for s in rows if s.get("search_url")]


def probe_one(url: str, timeout: float = 20.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (kosif free_media_catalog probe)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return "ok" if r.status < 400 else f"http-{r.status}"
    except urllib.error.HTTPError as e:
        return "blocked-from-cloud" if e.code in (401, 403, 429, 503) else f"http-{e.code}"
    except urllib.error.URLError as e:
        msg = str(e.reason).lower()
        return "no-dns" if ("name or service" in msg or "nodename" in msg or "getaddrinfo" in msg) else "timeout"
    except (TimeoutError, OSError):
        return "timeout"


def footage_ids() -> set | None:
    try:
        return {s["id"] for s in load(FOOTAGE_DB)["sources"]}
    except (OSError, ValueError, KeyError):
        return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--db", default=str(DB_PATH), help="catalog file (default data/free_media_catalog.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sections")
    li = sub.add_parser("list")
    for name, kw in (("--section", {}), ("--topic", {}), ("--origin", {"choices": ORIGINS})):
        li.add_argument(name, **kw)
    for flag in ("--commercial", "--no-credit", "--star", "--reachable", "--json"):
        li.add_argument(flag, action="store_true")
    fi = sub.add_parser("find")
    fi.add_argument("words", nargs="+")
    fi.add_argument("--json", action="store_true")
    sh = sub.add_parser("show")
    sh.add_argument("id")
    lk = sub.add_parser("links")
    lk.add_argument("query")
    lk.add_argument("--topic")
    lk.add_argument("--section")
    lk.add_argument("--commercial", action="store_true")
    sub.add_parser("check")
    pr = sub.add_parser("probe")
    pr.add_argument("--ids", help="comma-separated ids (default all)")
    pr.add_argument("--delay", type=float, default=0.3)
    a = ap.parse_args(argv)
    db = load(Path(a.db))

    if a.cmd == "sections":
        for sec, label in db["sections"].items():
            print(f"{sec:<10} {sum(s['section'] == sec for s in db['sources']):>3}  {label}")
        print()
        for t, label in db["topics"].items():
            print(f"topic {t:<10} {sum(t in s['topics'] for s in db['sources']):>3}  {label}")
        c = db["counts"]
        print(f"\n{c['total']} موقع: {c['user_list']} من القائمة الأصلية + {c['extras']} إضافة")
        return 0
    if a.cmd == "list":
        if a.section and a.section not in db["sections"]:
            ap.error(f"--section must be one of {', '.join(db['sections'])}")
        if a.topic and a.topic not in db["topics"]:
            ap.error(f"--topic must be one of {', '.join(db['topics'])}")
        rows = select(db, a.section, a.topic, a.commercial, a.no_credit, a.star, a.origin, a.reachable)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            print_rows(db, rows)
        return 0
    if a.cmd == "find":
        rows = find(db, a.words)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        elif rows:
            print_rows(db, rows)
        else:
            print("no match / لا نتيجة")
        return 0 if rows else 1
    if a.cmd == "show":
        rec = next((s for s in db["sources"] if s["id"] == a.id), None)
        if not rec:
            print(f"unknown id {a.id}", file=sys.stderr)
            return 1
        print(json.dumps(rec, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "links":
        rows = select(db, a.section, a.topic, a.commercial)
        links = search_links(db, a.query, rows)
        for s, u in links:
            print(f"{s['name']:<34} تجاري: {COMMERCIAL_AR[s['commercial']]:<12} النسب: {CREDIT_AR[s['credit']]:<9} {u}")
        if not links:
            print("no site with a search URL matches these filters")
        return 0 if links else 1
    if a.cmd == "check":
        errs = problems(db, footage_ids())
        for e in errs:
            print("ERROR " + e)
        if not errs:
            print(f"ok: {len(db['sources'])} sources, ids and urls unique, enums and tool references valid")
        return 1 if errs else 0
    if a.cmd == "probe":
        want = set(a.ids.split(",")) if a.ids else None
        for s in db["sources"]:
            if want and s["id"] not in want:
                continue
            now = probe_one(s["url"])
            mark = "" if now == s["reach"] else f"   (was {s['reach']} on {db['checked_on']})"
            print(f"{s['id']:<22} {now:<20}{mark}")
            time.sleep(max(0.0, a.delay))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
