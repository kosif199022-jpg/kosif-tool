#!/usr/bin/env python3
"""KOSIF Instagram Video Research: public-index search, scoped plans and evidence-labelled SQLite.
Standard library only. No Instagram scraping, private-access bypass, or media downloads.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import unicodedata
from urllib.parse import urlparse, urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "data" / "creator_registry.json"
DB_FILE = ROOT / "data" / "instagram_research.sqlite"
BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
LEXICON = {
    "طبيعة": ["nature", "landscape", "scenery"],
    "مناظر": ["landscape", "nature photography"],
    "غيوم": ["clouds", "cloudscape"],
    "سحاب": ["clouds", "sky"],
    "سماء": ["sky", "skyscape"],
    "غروب": ["sunset", "golden hour"],
    "بحر": ["sea", "ocean"], "زهور": ["flowers", "flower field"],
    "ورود": ["flowers", "roses"], "شلال": ["waterfall", "cascades"],
    "سينمائي": ["cinematic", "film look"],
    "درون": ["drone footage", "aerial"], "نجوم": ["stars", "night sky"],
    "موشن": ["motion graphics", "animation", "animasyon", "hareketli grafik"],
    "سبورة": ["whiteboard animation", "hand drawn", "tahta animasyon", "çizim"],
    "رسم": ["drawing", "sketch", "illustration", "çizim"],
    "مؤثرات": ["vfx", "visual effects", "görsel efekt"],
    "ثلاثي": ["3d animation", "blender", "3d modelleme"],
    "مونتاج": ["video editing", "transitions", "kurgu"],
    "تايبوجرافي": ["kinetic typography", "typography", "tipografi"],
    "ذكاء": ["ai video", "generative video", "yapay zeka"],
    "جسيمات": ["particles", "particle simulation", "parçacık"],
    "لوب": ["seamless loop", "loop animation", "döngü"],
}

def creators():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))["creators"]

def tokens(value):
    s = unicodedata.normalize("NFKC", str(value)).lower()
    s = re.sub("[\u064b-\u065f\u0670]", "", s)
    s = re.sub("[أإآ]", "ا", s).replace("ى", "ي").replace("ة", "ه")
    return re.findall(r"[\w]+", s, flags=re.UNICODE)

def expand(topic):
    words = set(tokens(topic))
    variants = [topic.strip()]
    groups = []
    for label, terms in LEXICON.items():
        candidates = [label] + terms
        if any(set(tokens(term)).issubset(words) for term in candidates if tokens(term)):
            groups.append(terms)
    if groups:
        # Retain all matched concepts in the second translated search phrase.
        variants.append(" ".join(group[0] for group in groups))
        for group in groups:
            variants.extend(group)
    return list(dict.fromkeys(filter(None, variants)))[:12]

def plan(topic, accounts_only=False):
    variants, jobs = expand(topic)[:2], []
    # Round-robin: with a 3-query API budget include BOTH tracked creators.
    for v in variants:
        if not accounts_only:
            jobs.append({"scope":"public", "query":f'site:instagram.com/reel/ "{v}"'})
        for c in creators():
            jobs.append({"scope":c["handle"],
                         "query":f'site:instagram.com/reel/ "{v}" "{c["handle"]}"'})
    for job in jobs:
        job["google_url"] = "https://www.google.com/search?" + urlencode({"q":job["query"]})
        job["brave_url"] = "https://search.brave.com/search?" + urlencode({"q":job["query"]})
    jobs.append({"scope":"instagram_app", "query":topic,
                 "url":"https://www.instagram.com/explore/search/keyword/?" + urlencode({"q":topic}),
                 "note":"May require login and may redirect; not a verified search result."})
    return jobs

def canonical(url):
    try:
        u = urlparse(str(url).strip())
        if u.scheme not in {"https","http"} or u.hostname not in {"instagram.com","www.instagram.com"}:
            return None
        # Also accept profile-scoped links (/<handle>/reel/<id>/), as Instagram now shares them.
        m = re.fullmatch(r"(?:/[A-Za-z0-9._]{1,30})?/(reel|reels|p|tv)/([A-Za-z0-9_-]{5,64})/?",u.path,re.I)
        return f"https://www.instagram.com/{m.group(1).lower()}/{m.group(2)}/" if m else None
    except (ValueError,TypeError):
        return None

def database(path):
    db=sqlite3.connect(str(path))
    db.execute("""CREATE TABLE IF NOT EXISTS reels (
        url TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL,
        author TEXT, search_query TEXT, source TEXT NOT NULL, evidence TEXT NOT NULL,
        discovered_utc TEXT NOT NULL
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS reviewed_reels (
        url TEXT PRIMARY KEY REFERENCES reels(url),
        reviewer TEXT NOT NULL,
        reviewed_utc TEXT NOT NULL,
        observed_tags TEXT NOT NULL,
        observed_mechanisms TEXT NOT NULL,
        observations TEXT NOT NULL
    )""")
    db.execute("PRAGMA foreign_keys=ON")
    db.commit()
    return db

def csv_tags(value):
    return list(dict.fromkeys(t.strip() for t in (value or "").split(",") if t.strip()))

def review_reel(db, url, reviewer, tags, mechanisms, observations):
    """An explicit HUMAN review: never inferred from search snippets."""
    clean=canonical(url)
    if not clean or not db.execute("SELECT 1 FROM reels WHERE url=?", (clean,)).fetchone():
        raise ValueError("Index a real Instagram permalink before reviewing it")
    if not reviewer.strip() or not observations.strip() or not csv_tags(mechanisms):
        raise ValueError("Reviewer, observed mechanisms and evidence notes are required")
    db.execute("""INSERT INTO reviewed_reels VALUES (?,?,?,?,?,?)
        ON CONFLICT(url) DO UPDATE SET reviewer=excluded.reviewer,
          reviewed_utc=excluded.reviewed_utc,
          observed_tags=excluded.observed_tags,
          observed_mechanisms=excluded.observed_mechanisms,
          observations=excluded.observations""",
        (clean,reviewer.strip(),dt.datetime.now(dt.timezone.utc).isoformat(),
         json.dumps(csv_tags(tags),ensure_ascii=False),
         json.dumps(csv_tags(mechanisms),ensure_ascii=False),observations.strip()))
    db.commit()
    return {"url":clean,"review_status":"verified_by_authorized_review",
            "note":"Entered by named reviewer; no automatic media examination performed"}

def export_reviews(db, output_path):
    """Export human-observed mechanism evidence, usable for Infinite Matrices."""
    rows=[]
    sql="""SELECT r.url,r.title,r.description,r.author,v.reviewer,v.reviewed_utc,
       v.observed_tags,v.observed_mechanisms,v.observations
       FROM reels r JOIN reviewed_reels v ON r.url=v.url ORDER BY r.url"""
    for (url,title,description,author,reviewer,when,tags,mechanisms,observations) in db.execute(sql):
        rows.append({"url":url,"title":title,"description":description,"author":author,
                     "reviewer":reviewer,"reviewed_utc":when,
                     "observed_tags":json.loads(tags),
                     "observed_mechanisms":json.loads(mechanisms),
                     "observations":observations,
                     "status":"USER_REVIEWED_REFERENCE_NOT_PROVEN_RENDER_MECHANISM"})
    output_path.parent.mkdir(parents=True,exist_ok=True)
    output_path.write_text(json.dumps({"count":len(rows),"references":rows,
        "warning":"Causal laws must be independently reconstructed and tested; do not reuse copyrighted video without permission."},
        ensure_ascii=False,indent=2),encoding="utf-8")
    return {"exported":len(rows),"output":str(output_path)}

def import_rows(db,rows,source="import",search_query=""):
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    count=0
    for item in rows:
        if not isinstance(item,dict): continue
        url=canonical(item.get("url"))
        if not url: continue
        evidence="url_only_unverified" if source=="manual" else "public_search_index_unverified"
        db.execute("""INSERT INTO reels VALUES(?,?,?,?,?,?,?,?)
            ON CONFLICT(url) DO UPDATE SET
            title=CASE WHEN length(excluded.title)>length(title) THEN excluded.title ELSE title END,
            description=CASE WHEN length(excluded.description)>length(description)
                             THEN excluded.description ELSE description END,
            author=COALESCE(author,excluded.author), search_query=excluded.search_query,
            source=CASE WHEN source='manual' THEN source ELSE excluded.source END,
            evidence=CASE WHEN evidence='url_only_unverified' THEN evidence ELSE excluded.evidence END""",
            (url,str(item.get("title",""))[:400],str(item.get("description",item.get("snippet","")))[:2000],
             item.get("author"),search_query,source,evidence,now))
        count+=1
    db.commit()
    return count

def find(db,topic,limit=30):
    query=set(tokens(topic))
    for variant in expand(topic): query.update(tokens(variant))
    known={c["handle"].lower() for c in creators()}
    results=[]
    for url,title,description,author,search_query,source,evidence,seen in db.execute("SELECT * FROM reels"):
        matching=len(query & set(tokens(" ".join([title,description,search_query or ""]))))
        review=db.execute("SELECT observed_tags,observed_mechanisms,reviewer FROM reviewed_reels WHERE url=?",(url,)).fetchone()
        observed_overlap=0
        reviewer=None
        if review:
            tags,mechanisms,reviewer=review
            observed_overlap=len(query & set(tokens(" ".join(json.loads(tags)+json.loads(mechanisms)))))
        if not matching and not observed_overlap: continue
        score=matching*2 + (2 if author and author.lower().lstrip("@") in known else 0)
        score+=1 if "/reel/" in url or "/reels/" in url else 0
        if review:
            score+=observed_overlap*5+4
            evidence="verified_by_authorized_review"
        results.append(dict(url=url,title=title,description=description,author=author,
                            relevance=score,source=source,evidence=evidence,
                            reviewer=reviewer,discovered_utc=seen))
    return sorted(results,key=lambda x:(-x["relevance"],x["url"]))[:limit]

def public_web_search(key,jobs,max_queries=3,limit=10):
    batches=[]
    for job in [j for j in jobs if j["scope"]!="instagram_app"][:max_queries]:
        params=urlencode({"q":job["query"],"count":min(20,max(1,limit)),
                          "safesearch":"moderate","text_decorations":"false"})
        request=Request(BRAVE_ENDPOINT+"?"+params,headers={
            "X-Subscription-Token":key,"Accept":"application/json",
            "User-Agent":"KOSIF-Instagram-Research/1.0"})
        with urlopen(request,timeout=15) as response: obj=json.load(response)
        results=[{"url":x["url"],"title":x.get("title",""),"description":x.get("description","")}
                 for x in obj.get("web",{}).get("results",[]) if canonical(x.get("url",""))]
        batches.append((job["query"],results))
    return batches

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db",type=Path,default=DB_FILE)
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("sources")
    cmd=sub.add_parser("plan");cmd.add_argument("topic");cmd.add_argument("--accounts-only",action="store_true")
    cmd=sub.add_parser("search");cmd.add_argument("topic");cmd.add_argument("--accounts-only",action="store_true")
    cmd.add_argument("--max-queries",type=int,default=3);cmd.add_argument("--limit",type=int,default=10)
    cmd=sub.add_parser("find");cmd.add_argument("topic");cmd.add_argument("--limit",type=int,default=30)
    cmd=sub.add_parser("import");cmd.add_argument("json_file",type=Path)
    cmd=sub.add_parser("add");cmd.add_argument("url");cmd.add_argument("--title",default="")
    cmd.add_argument("--description",default="");cmd.add_argument("--author",default="")
    cmd=sub.add_parser("review");cmd.add_argument("url");cmd.add_argument("--reviewer",required=True)
    cmd.add_argument("--tags",default="");cmd.add_argument("--mechanisms",required=True)
    cmd.add_argument("--observations",required=True)
    cmd=sub.add_parser("export-reviewed");cmd.add_argument("output",type=Path)
    args=parser.parse_args(argv)
    if args.command=="sources":
        result={"creators":creators()}
    elif args.command=="plan":
        result={"mode":"search_links_not_verified_hits","queries":plan(args.topic,args.accounts_only)}
    else:
        args.db.parent.mkdir(parents=True,exist_ok=True)
        with database(args.db) as db:
            if args.command=="find":
                result={"topic":args.topic,"hits":find(db,args.topic,args.limit)}
            elif args.command=="import":
                rows=json.loads(args.json_file.read_text(encoding="utf-8"))
                if isinstance(rows,dict):rows=rows.get("results",rows.get("reels",[]))
                if not isinstance(rows,list):raise ValueError("JSON must contain a results array")
                result={"indexed":import_rows(db,rows)}
            elif args.command=="add":
                result={"indexed":import_rows(db,[{"url":args.url,"title":args.title,
                    "description":args.description,"author":args.author}],"manual")}
            elif args.command=="review":
                result=review_reel(db,args.url,args.reviewer,args.tags,args.mechanisms,args.observations)
            elif args.command=="export-reviewed":
                result=export_reviews(db,args.output)
            else:
                queries=plan(args.topic,args.accounts_only)
                token=os.environ.get("BRAVE_SEARCH_API_KEY")
                if not token:
                    result={"mode":"search_links_only","queries":queries,
                            "note":"Set BRAVE_SEARCH_API_KEY for automatic public-index lookup."}
                else:
                    try:
                        batches=public_web_search(token,queries,args.max_queries,args.limit)
                        indexed=sum(import_rows(db,items,"brave_web_index",q) for q,items in batches)
                        result={"mode":"public_index","indexed":indexed,"hits":find(db,args.topic,args.limit),
                                "queries":queries,"note":"Not exhaustive; private and unindexed Reels unavailable."}
                    except Exception as exc:
                        result={"mode":"fallback_links","error":str(exc),"queries":queries}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    sys.exit(main())
