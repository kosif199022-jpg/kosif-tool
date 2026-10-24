#!/usr/bin/env python3
"""KOSIF Instagram reference discovery. Offline-first; never scrapes or downloads Instagram."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
from urllib.parse import quote_plus, urlparse

SOURCES = ("asirgokerr", "brkn.land")
STATES = ("link_only", "metadata_verified", "frames_reviewed")
EVIDENCE_RANK = {"link_only": 0, "metadata_verified": 1, "frames_reviewed": 2}
ALIASES = {"ثري دي":"3d", "ثلاثي الابعاد":"3d", "ثلاثي الأبعاد":"3d",
           "موشن":"motion", "حركة":"animation", "متحرك":"animation",
           "كتابة":"typography", "خط":"typography", "حروف":"typography",
           "انتقال":"transition", "تحول":"morph", "يتحول":"morph",
           "ضوء":"light", "اضاءة":"light", "إضاءة":"light",
           "رسم":"drawing", "يدوي":"handdrawn", "سبورة":"whiteboard",
           "صلصال":"clay", "جسيمات":"particles", "فيزياء":"physics",
           "سينمائي":"cinematic", "واقعي":"realistic"}

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def normalized_text(s):
    s = str(s or "").lower()
    for a,b in ALIASES.items():
        s = s.replace(a, " "+b+" ")
    return set(re.findall(r"[a-z0-9]+|[\u0621-\u064a]+", s))

def video_url(raw):
    p = urlparse(raw.strip())
    if p.scheme != "https" or p.netloc.lower() not in ("instagram.com","www.instagram.com"):
        raise ValueError("Only HTTPS Instagram reel/post URLs are allowed")
    m = re.fullmatch(r"/(reel|p|tv)/([A-Za-z0-9_-]{5,32})/?", p.path)
    if not m or p.username or p.password or p.port:
        raise ValueError("Invalid Instagram reel/post permalink")
    return "https://www.instagram.com/"+m.group(1)+"/"+m.group(2)+"/"

def account(raw):
    a = raw.strip().lstrip("@").lower()
    if a not in SOURCES:
        raise ValueError("Account not in curated sources")
    return a

def db(path):
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(p))
    c.row_factory = sqlite3.Row
    c.executescript("""CREATE TABLE IF NOT EXISTS video_references (
        url TEXT PRIMARY KEY, handle TEXT, topic TEXT NOT NULL,
        caption TEXT NOT NULL DEFAULT '', tags TEXT NOT NULL DEFAULT '',
        motion TEXT NOT NULL DEFAULT '', visual TEXT NOT NULL DEFAULT '',
        state TEXT NOT NULL, evidence_uri TEXT NOT NULL DEFAULT '',
        rights TEXT NOT NULL DEFAULT '', observed_at TEXT NOT NULL,
        note TEXT NOT NULL DEFAULT '');
        CREATE INDEX IF NOT EXISTS ref_handle ON video_references(handle);""")
    return c

def put(c, entry):
    u = video_url(entry["url"])
    state = entry.get("state","link_only")
    if state not in STATES: raise ValueError("Unknown evidence state")
    h = entry.get("handle","").strip().lstrip("@").lower()
    if h and h not in SOURCES: raise ValueError("Register creator before attribution")
    evidence = entry.get("evidence_uri","").strip()
    if state == "frames_reviewed" and not evidence:
        raise ValueError("Reviewed frames require evidence URI/path")
    if state != "link_only" and not (entry.get("caption") or entry.get("note") or evidence):
        raise ValueError("Observed evidence required")
    fields = ("url","handle","topic","caption","tags","motion","visual","state",
              "evidence_uri","rights","observed_at","note")
    payload = {k:str(entry.get(k,"")) for k in fields}
    payload.update(url=u,handle=h,state=state,observed_at=entry.get("observed_at") or now())
    if not payload["topic"].strip(): raise ValueError("Topic is required")
    existing = c.execute("SELECT state FROM video_references WHERE url=?",(u,)).fetchone()
    if existing and EVIDENCE_RANK[state] < EVIDENCE_RANK[existing["state"]]:
        raise ValueError("Cannot downgrade evidence without review")
    c.execute("INSERT OR REPLACE INTO video_references VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              tuple(payload[k] for k in fields))
    c.commit()
    return u

def search_plans(topic, handle=None):
    accounts = [account(handle)] if handle else list(SOURCES)
    variants = [topic.strip(), " ".join(sorted(normalized_text(topic)))]
    seen=set(); out=[]
    for q in variants:
        if not q or q in seen: continue
        seen.add(q)
        for h in accounts:
            for query in (f"site:instagram.com/{h}/reel/ {q}",
                          f'site:instagram.com/reel/ "{h}" {q}',
                          f'"{h}" {q} reels instagram'):
                out.append({"handle":h, "query":query,
                    "google":"https://www.google.com/search?q="+quote_plus(query),
                    "bing":"https://www.bing.com/search?q="+quote_plus(query),
                    "status":"SEARCH_LINK_ONLY"})
    return out

def match(c,query,limit=20,handle=None):
    qt = normalized_text(query)
    rows = c.execute("SELECT * FROM video_references"+(" WHERE handle=?" if handle else ""),
                     (account(handle),) if handle else ()).fetchall()
    ranked=[]
    for row in rows:
        r=dict(row)
        tokens=normalized_text(" ".join(str(r[k]) for k in
             ("topic","caption","tags","motion","visual","note")))
        overlap=qt & tokens
        if qt and not overlap: continue
        r["score"]=round(10*len(overlap)/max(len(qt),1)+1.5*EVIDENCE_RANK[r["state"]],3)
        r["matched_terms"]=sorted(overlap)
        ranked.append(r)
    return sorted(ranked,key=lambda x:(-x["score"],x["url"]))[:limit]

def propose(c,url,catalog=None):
    u = video_url(url)
    row = c.execute("SELECT * FROM video_references WHERE url=?",(u,)).fetchone()
    if row is None: raise ValueError("Reference not indexed")
    r=dict(row)
    verified=r["state"]=="frames_reviewed"
    tags=normalized_text(r["topic"]+" "+r["motion"]+" "+r["visual"])
    candidates=[]
    if catalog:
        styles=json.loads(Path(catalog).read_text(encoding="utf-8"))["styles"]
        for s in styles:
            overlap=sorted(set(s["operator_tags"]) & tags)
            if overlap: candidates.append({"style_id":s["style_id"],
                "family":s["card_family"],"matching_tags":overlap})
        candidates=sorted(candidates,key=lambda x:(-len(x["matching_tags"]),x["style_id"]))[:8]
    return {"schema":"kosif.instagram.to-matrices.v1",
        "id":"KIG-"+hashlib.sha256((u+"|"+r["observed_at"]).encode()).hexdigest()[:12],
        "reference_url":u, "source_account":r["handle"] or "unknown",
        "observed_state":r["state"],
        "status":"EVIDENCE_REVIEWED_PROPOSAL" if verified else "NOT_VERIFIED_REFERENCE",
        "observed_claims":{"topic":r["topic"],"motion":r["motion"],"visual":r["visual"],
                           "evidence_uri":r["evidence_uri"]},
        "causal_bricks":{
            "state":"Define measurable geometry/material variables from observed frames",
            "operation":"Infer transforms only from reviewed observations",
            "rule":"Write new falsifiable coupling; do not infer law from tags alone",
            "time":"Measure real frame/cut timings from authorized footage",
            "memory":"Check if historical state affects future motion",
            "feedback":"Only record validated A/B experiment in KMX research ledger"},
        "candidate_86_style_adapters":candidates,
        "next":"Inspect authorized frames, define typed recipe and run KMX A/B/C experiment",
        "restrictions":["No copying video","No unverified claims",
                        "No automatic learning/ledger promotion"]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db",default=os.environ.get("KOSIF_IG_DB",
                   "out/kosif-instagram/catalog.sqlite3"))
    sp=p.add_subparsers(dest="cmd",required=True)
    sp.add_parser("doctor");sp.add_parser("sources")
    a=sp.add_parser("plan");a.add_argument("topic");a.add_argument("--handle")
    a=sp.add_parser("add");a.add_argument("url");a.add_argument("--topic",required=True)
    for opt in ("handle","caption","tags","motion","visual","evidence_uri","rights","note"):
        a.add_argument("--"+opt.replace("_","-"),default="")
    a.add_argument("--state",choices=STATES,default="link_only")
    a=sp.add_parser("search");a.add_argument("topic");a.add_argument("--handle")
    a.add_argument("--limit",type=int,default=20)
    a=sp.add_parser("propose");a.add_argument("url");a.add_argument("--catalog");a.add_argument("--out")
    a=sp.add_parser("import-json");a.add_argument("file")
    a=p.parse_args(argv)
    if a.cmd=="sources":
        result=[{"handle":h,"url":"https://www.instagram.com/"+h+"/",
                 "state":"unreviewed_source"} for h in SOURCES]
    elif a.cmd=="plan": result=search_plans(a.topic,a.handle)
    else:
        c=db(a.db)
        if a.cmd=="doctor":
            result={"schema":"kosif.ig.discover.v1","db":a.db,"sources":list(SOURCES),
                    "indexed":c.execute("SELECT COUNT(*) FROM video_references").fetchone()[0],
                    "access":"offline metadata only; no Instagram scraping"}
        elif a.cmd=="add":result={"saved":put(c,vars(a))}
        elif a.cmd=="search":result=match(c,a.topic,max(1,min(100,a.limit)),a.handle)
        elif a.cmd=="propose":
            result=propose(c,a.url,a.catalog)
            if a.out:
                target=Path(a.out)
                if target.exists():raise ValueError("Refusing to overwrite proposal")
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        else:
            items=json.loads(Path(a.file).read_text(encoding="utf-8"))
            if not isinstance(items,list): raise ValueError("JSON root must be an array")
            result={"saved":[put(c,x) for x in items]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    try: sys.exit(main())
    except (ValueError,KeyError,sqlite3.Error) as exc:
        print(json.dumps({"error":str(exc)},ensure_ascii=False),file=sys.stderr)
        sys.exit(2)
