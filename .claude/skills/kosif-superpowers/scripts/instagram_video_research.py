#!/usr/bin/env python3
"""KOSIF Instagram Video Research v1 — lawful discovery + provenance-index, stdlib only.

This DOES NOT scrape Instagram or bypass access gates. It plans public search
queries and indexes explicitly supplied/verified public Reel URLs and metadata.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote, urlencode, urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data" / "instagram_video_sources.json"
DEFAULT_DB = Path.home() / ".kosif" / "instagram_video_research.sqlite3"
STATES = ("candidate", "metadata_reviewed", "visually_reviewed")

# Topic labels / synonyms improve multilingual discovery but never assert content.
LEXICON = {
    "motion": ["موشن", "حركة", "motion graphics", "animation", "animasyon", "motion design"],
    "whiteboard": ["سبورة", "رسم سبورة", "whiteboard animation", "tahta çizim", "hand drawn"],
    "drawing": ["رسم", "رسم بالقلم", "drawing", "sketch", "çizim", "illustration"],
    "cinematic": ["سينمائي", "تصوير سينمائي", "cinematic", "sinema", "filmmaking"],
    "3d": ["ثلاثي الأبعاد", "3d animation", "cgi", "blender 3d", "3d modelleme"],
    "editing": ["مونتاج", "انتقالات", "video editing", "transitions", "kurgu"],
    "vfx": ["مؤثرات بصرية", "vfx", "visual effects", "görsel efekt"],
    "typography": ["تايبوجرافي", "كتابة متحركة", "kinetic typography", "tipografi"],
    "ai": ["ذكاء اصطناعي", "ai video", "yapay zeka", "generative video"],
    "product": ["إعلان منتج", "product commercial", "ürün reklam"],
    "stopmotion": ["ستوب موشن", "stop motion", "stopmotion", "kare kare animasyon"],
    "infographic": ["إنفوجرافيك", "information design", "infografik"],
    "particles": ["جسيمات", "particles", "particle simulation", "parçacık"],
    "loop": ["لوب", "seamless loop", "loop animation", "döngü"],
}

def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    value = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", value)
    value = value.translate(str.maketrans("أإآىؤئ", "ااايوي"))
    return re.sub(r"[^\w]+", " ", value).strip()

def tokens(value: str) -> set[str]:
    return set(normalize(value).split())

def expand_topic(topic: str) -> list[str]:
    norm = normalize(topic)
    words = tokens(topic)
    options = [topic.strip()]
    for label, terms in LEXICON.items():
        all_terms = [label] + terms
        if (label in words or any(normalize(term) in norm for term in terms if len(normalize(term)) > 2)):
            options.extend(terms)
    # Ordered uniqueness, capped: overly long queries create false positives.
    out = []
    for t in options:
        if t.strip() and normalize(t) not in {normalize(x) for x in out}:
            out.append(t.strip())
    return out[:8]

def get_sources():
    payload = json.loads(SOURCES.read_text(encoding="utf-8"))
    rows = payload.get("sources", [])
    assert len({x["username"] for x in rows}) == len(rows), "Duplicate source usernames"
    return rows

def canonical_reel(raw: str) -> tuple[str, str]:
    parsed = urlparse(raw.strip())
    host = (parsed.hostname or "").lower()
    if parsed.scheme not in ("http", "https") or host not in ("instagram.com", "www.instagram.com"):
        raise ValueError("Only public Instagram post/Reel URLs are accepted")
    match = re.fullmatch(r"/(reel|p|tv)/([A-Za-z0-9_-]{4,30})/?", parsed.path)
    if not match:
        raise ValueError("Expected https://www.instagram.com/reel/<shortcode>/ (or /p/)")
    kind, shortcode = match.groups()
    return f"https://www.instagram.com/{kind}/{shortcode}/", shortcode

def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS reels(
      shortcode TEXT PRIMARY KEY,
      url TEXT NOT NULL,
      username TEXT NOT NULL DEFAULT '',
      title TEXT NOT NULL DEFAULT '',
      caption TEXT NOT NULL DEFAULT '',
      tags TEXT NOT NULL DEFAULT '[]',
      mechanisms TEXT NOT NULL DEFAULT '[]',
      status TEXT NOT NULL DEFAULT 'candidate'
         CHECK(status IN ('candidate','metadata_reviewed','visually_reviewed')),
      discovery_query TEXT NOT NULL DEFAULT '',
      provenance TEXT NOT NULL DEFAULT 'manual',
      notes TEXT NOT NULL DEFAULT '',
      created_utc TEXT NOT NULL,
      updated_utc TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_reels_user ON reels(username);
    CREATE INDEX IF NOT EXISTS idx_reels_status ON reels(status);
    """)
    return db

def as_list(value: str) -> list[str]:
    return list(dict.fromkeys(x.strip() for x in (value or "").split(",") if x.strip()))

def add_reel(db: sqlite3.Connection, args):
    url, shortcode = canonical_reel(args.url)
    known = {x["username"] for x in get_sources()}
    username = args.account.lstrip("@").lower() if args.account else ""
    if username and not re.fullmatch(r"[a-z0-9._]{1,30}", username):
        raise ValueError("Invalid Instagram username")
    # Metadata status is only a user assertion; never autonomously elevate.
    status = args.status
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    previous = db.execute("SELECT shortcode FROM reels WHERE shortcode=?", (shortcode,)).fetchone()
    db.execute("""
    INSERT INTO reels (shortcode,url,username,title,caption,tags,mechanisms,status,
                       discovery_query,provenance,notes,created_utc,updated_utc)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT(shortcode) DO UPDATE SET url=excluded.url,username=excluded.username,
       title=CASE WHEN excluded.title<>'' THEN excluded.title ELSE reels.title END,
       caption=CASE WHEN excluded.caption<>'' THEN excluded.caption ELSE reels.caption END,
       tags=CASE WHEN excluded.tags<>'[]' THEN excluded.tags ELSE reels.tags END,
       mechanisms=CASE WHEN excluded.mechanisms<>'[]' THEN excluded.mechanisms ELSE reels.mechanisms END,
       status=CASE WHEN reels.status='visually_reviewed' THEN reels.status
                   WHEN reels.status='metadata_reviewed' AND excluded.status='candidate' THEN reels.status
                   ELSE excluded.status END,
       discovery_query=CASE WHEN excluded.discovery_query<>'' THEN excluded.discovery_query ELSE reels.discovery_query END,
       provenance=CASE WHEN excluded.provenance<>'manual' THEN excluded.provenance ELSE reels.provenance END,
       notes=CASE WHEN excluded.notes<>'' THEN excluded.notes ELSE reels.notes END,
       updated_utc=excluded.updated_utc
    """, (shortcode,url,username,args.title or "",args.caption or "",
          json.dumps(as_list(args.tags),ensure_ascii=False),
          json.dumps(as_list(args.mechanisms),ensure_ascii=False),
          status,args.query or "",args.provenance or "manual",
          args.notes or "",now,now))
    db.commit()
    print(json.dumps({"action":"updated" if previous else "added","url":url,
                      "status":status,"known_source":username in known},ensure_ascii=False))

def video_score(row, query: str) -> float:
    q = tokens(query)
    if not q: return 0.0
    text = " ".join([row["title"],row["caption"],row["notes"]])
    tags = " ".join(json.loads(row["tags"]))
    mechanisms = " ".join(json.loads(row["mechanisms"]))
    score = (len(q & tokens(text))*3.0 + len(q & tokens(tags))*5.0
             + len(q & tokens(mechanisms))*6.0 + len(q & tokens(row["username"]))*1.0)
    for w in expand_topic(query):
        if normalize(w) in normalize(" ".join([text,tags,mechanisms])): score += 0.8
    return score

def row_to_dict(row):
    out = dict(row)
    out["tags"] = json.loads(out["tags"])
    out["mechanisms"] = json.loads(out["mechanisms"])
    return out

def search_index(db, query: str, limit: int = 20, account: str = ""):
    rows = db.execute("SELECT * FROM reels").fetchall()
    matches = []
    for row in rows:
        if account and row["username"] != account.lstrip("@"): continue
        rank = video_score(row, query)
        if rank > 0:
            obj = row_to_dict(row)
            obj["relevance"] = round(rank, 2)
            matches.append(obj)
    matches.sort(key=lambda x: (-x["relevance"],
                  -STATES.index(x["status"]), x["shortcode"]))
    return matches[:limit]

def plan(topic: str, account: str = "", limit: int = 12):
    known = get_sources()
    candidates = [s for s in known if not account or account == "all" or
                  s["username"] == account.lstrip("@")]
    if account and account != "all" and not candidates:
        raise ValueError("Account is not present in source registry")
    variants = expand_topic(topic)
    results = []
    seen = set()
    def add(kind, q, url, username=""):
        if url in seen or len(results) >= limit: return
        seen.add(url)
        results.append({"kind":kind,"query":q,"account":username,
                        "url":url,"status":"SEARCH_PLAN_NOT_VERIFIED_RESULT"})
    # Include unrestricted topical discovery alongside searches for seed accounts.
    for w in variants[:2]:
        q = f'site:instagram.com/reel/ "{w}"'
        add("public_web_index", q, "https://www.google.com/search?"+urlencode({"q":q}))
    for source in candidates:
        user = source["username"]
        add("profile_reels", user, source["canonical_url"].rstrip("/") + "/reels/",user)
        for w in variants[:3]:
            q = f'site:instagram.com/reel/ "{user}" "{w}"'
            add("public_web_index",q,"https://www.google.com/search?"+urlencode({"q":q}),user)
            add("public_web_index",q,"https://www.bing.com/search?"+urlencode({"q":q}),user)
    for w in variants:
        q = f'site:instagram.com/reel/ "{w}"'
        add("public_web_index",q,"https://www.google.com/search?"+urlencode({"q":q}))
        # No fabricated Instagram keyword API; direct users to the app.
    return {"topic":topic,"expanded_terms":variants,"source_count":len(candidates),
            "warning":"Plans are links/queries, not found or viewed Reels. Search engines index only a subset of public content.",
            "queries":results}

def export_rows(db, out: Path, fmt: str, reviewed_only: bool):
    rows = [row_to_dict(r) for r in db.execute("SELECT * FROM reels ORDER BY shortcode")]
    if reviewed_only: rows = [r for r in rows if r["status"] == "visually_reviewed"]
    out.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        out.write_text(json.dumps({"records":rows,"reviewed_only":reviewed_only,
            "warning":"Tags/mechanisms are provided annotations; not auto-extracted from videos."},
            ensure_ascii=False,indent=2),encoding="utf-8")
    else:
        with out.open("w",newline="",encoding="utf-8-sig") as f:
            cols = ["shortcode","url","username","title","caption","tags","mechanisms",
                    "status","discovery_query","provenance","notes","created_utc","updated_utc"]
            writer = csv.DictWriter(f,fieldnames=cols)
            writer.writeheader()
            for r in rows:
                r = dict(r)
                r["tags"] = ", ".join(r["tags"])
                r["mechanisms"] = ", ".join(r["mechanisms"])
                writer.writerow({k:r[k] for k in cols})
    return {"exported":len(rows),"path":str(out),"format":fmt}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db",type=Path,default=DEFAULT_DB)
    sub = ap.add_subparsers(dest="command",required=True)
    sub.add_parser("sources",help="Show registered public profile links")
    sp = sub.add_parser("plan",help="Build public web-search links; no scraping")
    sp.add_argument("--topic",required=True)
    sp.add_argument("--account",default="all")
    sp.add_argument("--limit",type=int,default=12)
    sp = sub.add_parser("add",help="Index a manually found Reel with provenance")
    sp.add_argument("--url",required=True)
    sp.add_argument("--account",default="")
    sp.add_argument("--title",default="")
    sp.add_argument("--caption",default="")
    sp.add_argument("--tags",default="")
    sp.add_argument("--mechanisms",default="")
    sp.add_argument("--status",choices=STATES,default="candidate")
    sp.add_argument("--query",default="")
    sp.add_argument("--provenance",default="manual")
    sp.add_argument("--notes",default="")
    sp = sub.add_parser("search",help="Rank saved metadata; not Instagram live search")
    sp.add_argument("--query",required=True)
    sp.add_argument("--account",default="")
    sp.add_argument("--limit",type=int,default=20)
    sp = sub.add_parser("export",help="Export saved references to JSON/CSV")
    sp.add_argument("--out",type=Path,required=True)
    sp.add_argument("--format",choices=("json","csv"),default="json")
    sp.add_argument("--reviewed-only",action="store_true")
    a = ap.parse_args(argv)
    if a.command == "sources": result = get_sources()
    elif a.command == "plan": result = plan(a.topic,a.account,max(1,min(a.limit,100)))
    else:
        with connect(a.db) as db:
            if a.command == "add": return add_reel(db,a)
            if a.command == "search": result = search_index(db,a.query,max(1,a.limit),a.account)
            else: result = export_rows(db,a.out,a.format,a.reviewed_only)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    try: main()
    except (ValueError,AssertionError) as e:
        print("ERROR: "+str(e),file=sys.stderr)
        raise SystemExit(2)
