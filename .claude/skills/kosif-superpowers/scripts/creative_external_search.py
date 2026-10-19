#!/usr/bin/env python3
"""Offline evidence-index search over researched creative repositories and sites.

This tool never downloads source, executes third-party code, or equates public
metadata with working KOSIF capabilities. Private GitHub inventories are outside
its directory and are intentionally inaccessible here.
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent/"data"/"rea-creative-research"
TOPICS={
    "audio-sync": ("audio","whisper","transcrib","caption","subtitl","speech","alignment","music","sound"),
    "motion-graphics": ("motion","animation","kinetic","typography","keyframe","lottie","svg","canvas","transition"),
    "video-editing": ("video","film","editor","timeline","footage","render","ffmpeg","composit","crop"),
    "image-editing": ("image","photo","retouch","enhanc","upscal","restor","background","mask","raw"),
    "3d-vfx": ("3d","vfx","particles","shader","webgl","blender","houdini","rigging","tracking"),
    "asset-licensing": ("stock","footage","copyright","public domain","creative commons","licens"),
    "creative-ai": ("generat","diffusion","segment","vision","multimodal","captioning"),
}
AR={
 "مونتاج":("video","editing","timeline"),"فيديو":("video","film","footage"),
 "صور":("image","photo"),"صورة":("image","photo"),"موسيقى":("music","audio"),
 "موشن":("motion","animation"),"تحريك":("animation","motion"),
 "ترجمة":("subtitle","caption"),"صوت":("audio","speech"),
 "قص":("cut","editing"),"كاميرا":("camera","tracking"),
 "تتبع":("tracking","motion"),"خطوط":("typography","fonts"),
 "خلفية":("background","removal"),"تلوين":("color","grading"),
 "تفريغ":("transcript","whisper"),"مزامنة":("sync","alignment"),
}

def terms(text):
    raw=re.findall(r"[\w\u0600-\u06ff-]+",text.lower())
    out=list(raw)
    for a,translations in AR.items():
        if a in text:out.extend(translations)
    for category,keywords in TOPICS.items():
        if category in text.lower():out.extend(keywords)
    return list(dict.fromkeys(x for x in out if len(x)>1))


def load():
    repo=json.loads((ROOT/"public_repos.json").read_text(encoding="utf-8"))
    sites=json.loads((ROOT/"creative_websites.json").read_text(encoding="utf-8"))
    return repo,sites


def rank(item,query,source):
    keywords=terms(query)
    title=(item["repository"] if source=="repo" else item["site"]).lower()
    description=(item.get("description","")+" "+item.get("category","")+" "+
                 item.get("topic","")).lower()
    score=sum((6 if word in title else 0)+(2 if word in description else 0)
              for word in keywords)
    if score<=0:return 0
    return score+min(1.2,int(item.get("stars") or 0)/20000)


def search(query,kind="all",top=15):
    repos,sites=load()
    candidates=[]
    for source,rows in (("repo",repos),("site",sites)):
        if kind not in ("all",source):continue
        for r in rows:
            score=rank(r,query,source)
            if score:
                candidates.append((score,source,r))
    candidates.sort(key=lambda p:(-p[0],p[2].get("repository",p[2].get("site",""))))
    output=[]
    for score,source,r in candidates[:top]:
        if source=="repo":
            item={"type":"github_repository","name":r["repository"],
                  "url":r["url"],"summary":r.get("description"),
                  "category":r["category"],"stars":r["stars"],
                  "license_spdx_metadata_only":r.get("license_spdx"),
                  "evidence_query":r.get("discovery_query"),
                  "rea_analysis":"not_performed_on_this_public_repo_by_catalog",
                  "feature_status":"DISCOVERED_METADATA_ONLY"}
        else:
            item={"type":"creative_website","name":r["site"],
                  "url":r["sample_url"],"topic":r["topic"],
                  "evidence_curated_source":r["source_list"],
                  "rea_analysis":"not_performed_on_this_website_by_catalog",
                  "feature_status":"CURATED_LINK_ONLY"}
        item["relevance_score"]=round(score,2)
        output.append(item)
    return output


def report():
    repos,sites=load()
    return {"repositories":len(repos),"websites":len(sites),
            "repo_category_counts":dict(collections.Counter(r["category"] for r in repos)),
            "REA_broad_analysis_claim":False,
            "KOSIF_implemented_new_features_from_catalog":0,
            "status":"public index discovery only; use REA separately for supported artifacts"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=["search","stats"])
    p.add_argument("query",nargs="?")
    p.add_argument("--kind",choices=["all","repo","site"],default="all")
    p.add_argument("--top",type=int,default=15)
    a=p.parse_args()
    if a.command=="search" and not a.query:p.error("search query required")
    result=search(a.query,a.kind,max(1,min(a.top,100))) if a.command=="search" else report()
    print(json.dumps(result,ensure_ascii=True,indent=2))
if __name__=="__main__":main()
