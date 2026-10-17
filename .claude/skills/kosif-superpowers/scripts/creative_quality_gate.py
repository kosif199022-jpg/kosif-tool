#!/usr/bin/env python3
"""KOSIF Creative Quality Gate: verify actual edit decisions, not AI rhetoric.

Hard-gate integer-frame continuity, original word-timing preservation, media
references and the evidence contract of KOSIF reference-edit projects. It NEVER
grades visual beauty, actor identity, audio emotion or final-render fidelity.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import re

SAFE_ASSET=re.compile(r"^(audio|clip_[0-9]{3})\.(wav|mp3|m4a|aac|mp4|m4v|mov|webm)$")
FPS={24,25,30,60}
MAX_SHOTS=80


def valid_number(value,lo,hi):
    return (isinstance(value,(int,float)) and not isinstance(value,bool)
            and math.isfinite(value) and lo<=value<=hi)


def inspect_plan(plan,project_dir=None):
    failures=[]
    checks={}
    def gate(name,ok,detail):
        checks[name]={"pass":bool(ok),"detail":detail}
        if not ok:failures.append(name)
    if not isinstance(plan,dict) or plan.get("schema")!="kosif.reference-edit.v1":
        raise ValueError("expected KOSIF reference edit plan")
    duration=plan.get("duration")
    fps=plan.get("fps")
    frames=plan.get("totalFrames")
    shots=plan.get("shots")
    clock=(valid_number(duration,0.1,300) and type(fps) is int and fps in FPS
           and type(frames) is int and 1<=frames<=18000 and
           abs(round(duration*fps)-frames)<=1)
    gate("valid_audio_frame_clock",clock,"fps and frame duration agree")
    if not clock:
        return {"status":"blocked","checks":checks,"failures":failures,
                "rendered":False,"unverified":["all downstream checks skipped"]}

    shape=isinstance(shots,list) and 1<=len(shots)<=MAX_SHOTS
    gate("shots_shape_valid",shape,"one to 80 ordered shots")
    if not shape:
        return {"status":"blocked","checks":checks,"failures":failures,
                "rendered":False,"unverified":["all downstream checks skipped"]}
    running=0
    boundaries=[]
    clocks_ok=True
    media_refs_ok=True
    active_asset_count=0
    for i,shot in enumerate(shots):
        if not isinstance(shot,dict):
            clocks_ok=False;media_refs_ok=False;continue
        a,b,n=shot.get("startFrame"),shot.get("endFrame"),shot.get("frames")
        if (type(a) is not int or type(b) is not int or type(n) is not int or
             a!=running or b<=a or b-a!=n or b>frames or shot.get("index")!=i):
            clocks_ok=False
            continue
        if i:boundaries.append(a/fps)
        running=b
        pulses=shot.get("pulseFrames",[])
        if not isinstance(pulses,list) or len(pulses)>30 or any(type(p) is not int or not 0<=p<n for p in pulses):
            clocks_ok=False
        asset=shot.get("asset")
        if asset is not None:
            active_asset_count+=1
            if not isinstance(asset,str) or not SAFE_ASSET.fullmatch(asset) or not asset.startswith("clip_"):
                media_refs_ok=False
            if project_dir and not (Path(project_dir)/"public"/"assets"/asset).is_file():
                media_refs_ok=False
    gate("continuous_no_gap_no_overlap",clocks_ok and running==frames,
         "every frame belongs to exactly one shot, with bounded pulse cues")

    words=plan.get("alignedWords")
    valid_words=isinstance(words,list) and len(words)<=1500
    previous=0.0
    if valid_words:
        for word in words:
            if not isinstance(word,dict):
                valid_words=False;break
            a=word.get("start");b=word.get("end");t=word.get("text")
            if (not valid_number(a,0,duration) or not valid_number(b,0,duration) or b<=a
                or a<previous-0.00001 or not isinstance(t,str) or not t.strip()):
                valid_words=False;break
            previous=b
            if any(a+1e-5<cut<b-1e-5 for cut in boundaries):
                valid_words=False;break
    gate("aligned_words_preserved",valid_words,"no verified word may cross a hard cut")

    audio=plan.get("audio")
    if audio is not None:
        if not isinstance(audio,str) or not SAFE_ASSET.fullmatch(audio) or not audio.startswith("audio."):
            media_refs_ok=False
        elif project_dir and not (Path(project_dir)/"public"/"assets"/audio).is_file():
            media_refs_ok=False
    gate("user_asset_reference_integrity",media_refs_ok,
         "only local allowlisted media paths; optional project must contain them")

    evidence=plan.get("evidence")
    unclaimed=(isinstance(evidence,dict)
               and evidence.get("referenceVideoPixelsCopied") is False
               and evidence.get("renderVerified") is False
               and evidence.get("semanticUnderstanding") is False)
    gate("truthful_evidence_flags",unclaimed,
         "cut timing is observable; rendered output, semantic interpretation not yet proved")

    length=[shot.get("frames",0) for shot in shots if isinstance(shot,dict)]
    short=sum(1 for n in length if 0<n<max(1,round(fps*0.25)))
    # A very short shot is a risk, not automatically a technical failure.
    unverified=[
        "user rights and commercial-license approval not machine-verified",
        "Remotion dependencies and codec compatibility not tested by schema",
        "actual rendered MP4 visual quality, cuts, and audio sync not checked",
        "reference video object motion and semantic correspondence not reconstructed"
    ]
    return {"status":"blocked" if failures else "structurally_verified_render_pending",
            "checks":checks,"failures":failures,"rendered":False,
            "metrics":{"shots":len(shots),"totalFrames":frames,"fps":fps,
                       "duration":duration,"shortShotsUnderQuarterSecond":short,
                       "replacementAssetSlots":active_asset_count},
            "unverified":unverified}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("plan",help="plan.json from KOSIF Remotion project")
    p.add_argument("--project-dir",help="optional generated Remotion project to check media files")
    p.add_argument("--out",required=True,help="new output audit JSON, never overwrite")
    a=p.parse_args()
    try:
        original=Path(a.plan)
        if not original.is_file() or original.is_symlink() or original.stat().st_size>2_000_000:
            raise ValueError("invalid plan source")
        model=json.loads(original.read_text(encoding="utf8"))
        report=inspect_plan(model,a.project_dir)
        path=Path(a.out)
        if not path.parent.is_dir() or path.is_symlink():
            raise ValueError("output parent missing")
        with path.open("x",encoding="utf8") as f:
            json.dump(report,f,indent=2,ensure_ascii=False)
            f.write("\n")
        print(json.dumps({"status":report["status"],"failures":report["failures"],
                          "audit":str(path.resolve())},ensure_ascii=False))
        if report["failures"]:raise SystemExit(2)
    except (OSError,TypeError,ValueError,json.JSONDecodeError) as exc:
        p.error(str(exc))


if __name__=="__main__":
    main()
