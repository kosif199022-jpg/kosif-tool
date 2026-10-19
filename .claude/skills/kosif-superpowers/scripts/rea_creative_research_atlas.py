#!/usr/bin/env python3
"""Build evidence-backed large-scale creative-repo/site discovery catalogs.

This tool uses *public GitHub metadata and curated markdown links*, not REA.
REA is invoked separately on authorized accessible source/browsers. Discovery
must not be mislabeled as code analysis. Private owner metadata remains local.
"""
from __future__ import annotations
import argparse
import base64
import collections
import json
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import date
from pathlib import Path

SKILL=Path(__file__).resolve().parent.parent
CATALOG=SKILL/"data"/"rea-creative-research"
REPO_QUERIES=[
    "topic:video-editing stars:>5",
    "topic:video-processing stars:>5",
    "topic:motion-graphics stars:>5",
    "topic:video-editor stars:>5",
    "topic:animation stars:>30",
    "topic:video-generation stars:>10",
    "topic:video-effects stars:>3",
    "topic:image-editing stars:>5",
    "topic:image-processing stars:>20",
    "topic:computer-vision stars:>30",
    "topic:photo-editing stars:>2",
    "topic:image-generation stars:>5",
    "topic:motion-design stars:>1",
    "topic:creative-coding stars:>5",
    "topic:visual-effects stars:>1",
    "topic:compositing stars:>1",
    "topic:video-transcoding stars:>1",
    "topic:ffmpeg stars:>20",
    "topic:photography stars:>15",
    "topic:subtitles stars:>3",
    "topic:arabic-nlp stars:>1",
]
CURATED=[
    "beast-ofcourse/awesome-motion-graphics",
    "Supersynergy/awesome-ai-video-editing",
    "ad-si/awesome-video-production",
    "AaronAust1n/awesome-video-skills",
    "iRajatDas/awesome-image-tools",
    "stimQQ/awesome-ai-image-tools",
    "eric-erki/awesome-creative-coding",
    "sergey-pimenov/awesome-web-animation",
    "goabstract/Awesome-Design-Tools",
    "kidhack/tools",
    "pipeabellos/thetoolforthat",
    "atakanaltok/awesome-useful-websites",
    "tmapp747/awesome-design-tools",
    "GagnDeep/awesome-best-ai-tools-for-video-editors-2026",
    "GagnDeep/awesome-best-ai-tools-for-photographers-2026",
]
KEYWORDS=("video","image","photo","photograph","animation","motion","graphics","visual","film",
          "effects","typograph","3d","render","picture","shader","generat","media","edit",
          "design","svg","canvas","subtitle","caption","footage","color","camera","frame")
DENY_DOMAINS={"github.com","raw.githubusercontent.com","githubusercontent.com","gitlab.com",
              "youtube.com","youtu.be","reddit.com","twitter.com","x.com",
              "linkedin.com","facebook.com","instagram.com","discord.com","discord.gg",
              "t.me","wikipedia.org","example.com","localhost","127.0.0.1",
              "img.shields.io","cdn.rawgit.com","rawgit.com","imgur.com","i.imgur.com",
              "badge.fury.io","travis-ci.org","circleci.com","app.codecov.io"}
URL=re.compile(r"https?://[^\s<>)\]\"']+",re.I)


def gh(endpoint,params=None,timeout=40):
    cmd=["gh","api","-X","GET",endpoint]
    for k,v in (params or {}).items():
        cmd.extend(["-f",f"{k}={v}"])
    result=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,encoding="utf-8",errors="replace")
    if result.returncode:
        raise RuntimeError(result.stderr.strip()[:350])
    return json.loads(result.stdout)


def readme(repo):
    data=gh("repos/"+repo+"/readme")
    return base64.b64decode(data["content"]).decode("utf-8",errors="replace")


def owner_inventory(local: Path):
    owned=gh("user/repos",{"per_page":100,"type":"owner"})
    # Only public info for the second account; do not bypass authorization.
    other=gh("users/elkosif0-cmd/repos",{"per_page":100,"type":"owner"})
    entries=[]
    for value in owned+other:
        if not value or not value.get("full_name"): continue
        rec={"repository":value["full_name"],"private":bool(value.get("private")),
             "default_branch":value.get("default_branch"),
             "language":value.get("language"),"size_kb":value.get("size"),
             "url":value.get("html_url"),"description":value.get("description")}
        if rec["repository"] not in [v["repository"] for v in entries]:
            entries.append(rec)
    local.mkdir(parents=True,exist_ok=True)
    (local/"owner_repositories_PRIVATE_LOCAL.json").write_text(
        json.dumps(entries,ensure_ascii=False,indent=2),encoding="utf-8")
    return {"owned_repository_count":len(entries),
            "public_count":sum(not v["private"] for v in entries),
            "private_count":sum(v["private"] for v in entries),
            "accounts":["kosif199022-jpg","elkosif0-cmd"],
            "private_metadata_publication":False}


def classify(query):
    s=query.casefold()
    if "image" in s or "photo" in s: return "image-photo"
    if "animation" in s or "motion" in s or "effect" in s or "compositing" in s: return "motion-vfx"
    if "vision" in s or "coding" in s: return "computer-vision-creative"
    if "subtitle" in s or "arabic" in s: return "speech-typography"
    return "video-film"


def public_repos(limit=1000,pages=2,delay=2.1):
    result,issues={},[]
    for i,q in enumerate(REPO_QUERIES):
        if len(result)>=limit: break
        for page in range(1,pages+1):
            try:
                data=gh("search/repositories",{"q":q,"per_page":100,"page":page,"sort":"stars",
                                               "order":"desc"},timeout=60)
                rows=data.get("items",[])
                for x in rows:
                    if not x.get("full_name") or x.get("private") or x.get("archived"): continue
                    name=x["full_name"]
                    if name not in result:
                        result[name]={
                            "repository":name,"url":x.get("html_url"),
                            "description":str(x.get("description") or "")[:240],
                            "primary_language":x.get("language"),"stars":x.get("stargazers_count",0),
                            "license_spdx":(x.get("license") or {}).get("spdx_id"),
                            "size_kb":x.get("size"),"default_branch":x.get("default_branch"),
                            "discovery_query":q,"category":classify(q),
                            "github_metadata_observed":True,"rea_code_analyzed":False,
                            "feature_implemented_in_kosif":False}
                    if len(result)>=limit: break
                if len(rows)<100 or len(result)>=limit: break
                time.sleep(delay)
            except Exception as e:
                issues.append({"query":q,"page":page,"error":str(e)[:180]})
                break
        time.sleep(delay)
    return list(result.values()),issues


def extract_sites(markdown,source):
    results=[]
    heading="general"
    for line in markdown.splitlines():
        if line.startswith("#"):
            heading=re.sub(r"^#+\s*","",line).strip()[:140]
        urls=URL.findall(line)
        if not urls: continue
        for url in urls:
            url=url.rstrip(".,;:*_!")
            p=urllib.parse.urlparse(url)
            host=(p.hostname or "").lower().removeprefix("www.")
            if p.scheme not in ("https","http") or not host or host in DENY_DOMAINS: continue
            if host.endswith((".github.io",".readthedocs.io")):
                # useful hosted docs can count as a media web source but not license evidence
                pass
            context=(heading+" "+line[:450]).casefold()
            if not any(s in context for s in KEYWORDS): continue
            if re.search(r"(terms-of-service|privacy-policy|donate|sponsor|license)",url,re.I): continue
            if re.search(r"\.(png|svg|gif|jpg|jpeg|webp|ico)(?:\?|$)",p.path,re.I): continue
            results.append({"site":host,"sample_url":url[:350],
                            "topic":heading,"source_list":source,
                            "status":"curated_link_only_NOT_REA_ANALYZED",
                            "rea_browser_analyzed":False,"source_verified_live":False,
                            "feature_implemented_in_kosif":False})
    return results


def public_sites(limit=1000):
    result,issues={},[]
    for source in CURATED:
        try:
            txt=readme(source)
            for row in extract_sites(txt,source):
                if row["site"] not in result:
                    result[row["site"]]=row
                if len(result)>=limit: break
        except Exception as e:
            issues.append({"source":source,"error":str(e)[:180]})
        if len(result)>=limit: break
    return list(result.values()),issues


def save_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def study_own_trees(local):
    path=local/"owner_repositories_PRIVATE_LOCAL.json"
    if not path.exists(): raise FileNotFoundError("run owner-inventory first")
    rows=json.loads(path.read_text(encoding="utf-8"))
    findings=[]
    for row in rows:
        repo=row["repository"]
        try:
            meta=gh("repos/"+repo)
            branch=meta.get("default_branch")
            if not branch or meta.get("size",0)==0:
                findings.append({"repository":repo,"status":"empty","tree_files":0,
                                 "language":row["language"],"private":row["private"]})
                continue
            tree=gh("repos/"+repo+"/git/trees/"+urllib.parse.quote(branch,safe=""),
                    {"recursive":1},timeout=60)
            paths=[x["path"] for x in tree.get("tree",[])
                   if x.get("type")=="blob"]
            extension=collections.Counter(Path(f).suffix.lower() for f in paths)
            important=[x for x in paths if any(k in x.lower()
                for k in ("video","motion","render","audio","captions","image","photo",
                          "frame","subtitle","transcript","animation","ffmpeg","timeline"))]
            findings.append({"repository":repo,"status":"github_tree_metadata_inspected",
                "private":row["private"],"language":row["language"],"tree_files":len(paths),
                "tree_truncated":bool(tree.get("truncated")),
                "source_type_counts":dict(extension.most_common(12)),
                "media_related_paths_count":len(important),
                "media_related_path_examples":important[:18],
                "rea_source_code_analyzed":False})
        except Exception as e:
            findings.append({"repository":repo,"status":"tree_failed",
                             "error":str(e)[:190],"private":row["private"],
                             "rea_source_code_analyzed":False})
        save_json(local/"owner_tree_inspection_PRIVATE_LOCAL.json",findings)
    return {"inspected_metadata":sum(v["status"]=="github_tree_metadata_inspected" for v in findings),
            "empty":sum(v["status"]=="empty" for v in findings),
            "failed":sum(v["status"]=="tree_failed" for v in findings),
            "rea_analyzed":0,"total":len(findings),
            "private_details_kept_local":True}


def report():
    repos=json.loads((CATALOG/"public_repos.json").read_text(encoding="utf-8")) if (CATALOG/"public_repos.json").exists() else []
    sites=json.loads((CATALOG/"creative_websites.json").read_text(encoding="utf-8")) if (CATALOG/"creative_websites.json").exists() else []
    return {"public_repo_cataloged":len(repos),"website_domains_cataloged":len(sites),
            "rea_repo_source_inspected":sum(bool(x.get("rea_code_analyzed")) for x in repos),
            "rea_website_browser_inspected":sum(bool(x.get("rea_browser_analyzed")) for x in sites),
            "research_implemented_features":0,
            "status":"discovery_catalog; NOT 1000 deep REA inspections"}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("action",choices=["own","repos","sites","trees","report"])
    ap.add_argument("--limit",type=int,default=1000)
    ap.add_argument("--pages",type=int,default=2)
    ap.add_argument("--private-output",type=Path,required=False)
    a=ap.parse_args()
    if a.action=="own":
        if not a.private_output: ap.error("--private-output required; outside git repo")
        out=owner_inventory(a.private_output)
    elif a.action=="trees":
        if not a.private_output: ap.error("--private-output required")
        out=study_own_trees(a.private_output)
    elif a.action=="repos":
        rec,err=public_repos(limit=a.limit,pages=a.pages)
        save_json(CATALOG/"public_repos.json",rec)
        save_json(CATALOG/"repository_discovery_errors.json",err)
        out={"cataloged":len(rec),"target":a.limit,"errors":len(err),
             "status":"metadata_index_not_rea_analysis"}
    elif a.action=="sites":
        rows,err=public_sites(a.limit)
        save_json(CATALOG/"creative_websites.json",rows)
        save_json(CATALOG/"website_discovery_errors.json",err)
        out={"cataloged":len(rows),"target":a.limit,"errors":len(err),
             "status":"curated_links_not_rea_site_inspection"}
    else: out=report()
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
