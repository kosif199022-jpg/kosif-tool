#!/usr/bin/env python3
"""Generate traceable, deterministic research hypotheses, NOT images or films."""
import argparse, hashlib, json, random
from pathlib import Path
STRUCTURE=set("shape path graph grid geometry mesh panel tessellate topology tile axis point contour chord envelope parametric symbol projection stroke align triangulate voxel volume sdf field type layer mask".split())
DYNAMICS=set("integrate diffuse fluid warp fold transform distort pulse step ease trace particles morph erase accumulate flow deformation drift orbit squash stamp scan flicker periodic decay subdivide floodfill reveal spin deform beat".split())
FINISH=set("noise gradient grain texture halftone glow reflection fog print shadow light density edge blur palette chromatic dither pixel quantize hatch colour pattern misregister refraction foil stitch".split())
def load_catalog(path):
    rows=json.loads(Path(path).read_text(encoding="utf-8"))["styles"]
    if len(rows)!=86 or len({s["style_id"] for s in rows})!=86:
        raise ValueError("Exactly 86 distinct style cards required. No claim without audited source.")
    for s in rows:
        if "operator_tags" not in s or "card_family" not in s: raise ValueError("Incomplete source card")
    return rows
def generate(rows,count,seed):
    rng=random.Random(seed)
    choices=[[s for s in rows if set(s["operator_tags"])&group] for group in (STRUCTURE,DYNAMICS,FINISH)]
    if not all(choices): raise ValueError("No style adapters for at least one requested role")
    result=[];seen=set();attempts=0
    while len(result)<count and attempts<300*count:
        attempts+=1;a,b,c=[rng.choice(p) for p in choices]
        if len({x["style_id"] for x in (a,b,c)})!=3 or len({x["card_family"] for x in (a,b,c)})!=3: continue
        tags=[next(t for t in x["operator_tags"] if t in category) for x,category in zip((a,b,c),(STRUCTURE,DYNAMICS,FINISH))]
        key="|".join([a["style_id"],b["style_id"],c["style_id"]]+tags)
        id="KMX-"+hashlib.sha256(key.encode()).hexdigest()[:16]
        if id in seen:continue
        seen.add(id)
        result.append({"id":id,"status":"UNRENDERED_HYPOTHESIS","parents":[x["style_id"] for x in (a,b,c)],
                       "parent_families":[x["card_family"] for x in (a,b,c)],
                       "roles":{"structure":tags[0],"dynamics":tags[1],"finish":tags[2]},
                       "new_causal_law":"Sample dynamic signal u(t); use clamp(normalize(u(t)),0,1) to drive a structure parameter; render the result with finish. Typed adapter and coupling must be defined before rendering.",
                       "required_evidence":["operator type compatibility","controlled A/B render","semantic check","licence and originality review"]})
    if len(result)!=count:raise RuntimeError("Insufficient diverse triples for requested count")
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--catalog",required=True);p.add_argument("--seed",type=int,default=20261024);p.add_argument("--count",type=int,default=75);p.add_argument("--output");args=p.parse_args()
    if not 1<=args.count<=100000: p.error("count range 1..100000")
    result={"seed":args.seed,"source_count":86,"warning":"Ideas only; not visual renders or globally verified unique styles","hypotheses":generate(load_catalog(args.catalog),args.count,args.seed)}
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:Path(args.output).write_text(text,encoding="utf-8")
    else: print(text)
if __name__=="__main__":main()
