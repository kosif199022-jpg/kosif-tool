#!/usr/bin/env python3
"""KOSIF Reference Edit Engine: editable video timing + original Remotion project.

Converts an authorized reference timing probe (not video pixels) to frame-exact
cuts, checks already aligned words, and produces a fresh runnable Remotion
React project with optional user-owned replacement clips/audio. Standard library
only; does not use/clone Katana or copy source-video frames.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import statistics
from creative_quality_gate import inspect_plan
import sys

FPS=(24,25,30,60)
MAX_SHOTS=80
FILE_LIMIT=350_000_000
ASSET_EXTS={".mp4",".mov",".webm",".m4v"}
AUDIO_EXTS={".mp3",".wav",".m4a",".aac"}
BASENAME=re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_. -]{0,100}$")
PACKAGE={
  "name":"kosif-reference-edit",
  "private":True,"type":"module",
  "scripts":{"studio":"remotion studio src/index.jsx",
             "render":"remotion render src/index.jsx KOSIFReference out.mp4 --codec h264",
             "stills":"remotion still src/index.jsx KOSIFReference still.png"},
  "dependencies":{"remotion":"^4.0.0","@remotion/cli":"^4.0.0",
                  "react":"^19.0.0","react-dom":"^19.0.0"}
}
INDEX='''import {registerRoot} from "remotion";
import {Root} from "./Root.jsx";
registerRoot(Root);
'''
ROOT='''import React from "react";
import {Composition} from "remotion";
import {KOSIFVideo} from "./Video.jsx";
import plan from "./plan.json";
export const Root=()=>(
  <Composition id="KOSIFReference" component={KOSIFVideo}
    durationInFrames={plan.totalFrames} fps={plan.fps}
    width={plan.width} height={plan.height}/>
);
'''
VIDEO='''import React from "react";
import {AbsoluteFill, Audio, OffthreadVideo, Sequence,
  interpolate, staticFile, useCurrentFrame} from "remotion";
import plan from "./plan.json";

// Original KOSIF arrangement engine. Shots are positioned on an integer
// frame clock and never request reference footage or third-party video models.
function Shot({shot}) {
  const frame=useCurrentFrame();
  const progress=Math.max(0,Math.min(1,frame/Math.max(1,shot.frames-1)));
  const floatY=Math.sin(frame*0.035)*18;
  const opacity=interpolate(frame,[0,Math.min(8,shot.frames-1)],
    [0,1],{extrapolateRight:"clamp"});
  const bg=shot.style?.background || (shot.index%2===0?"#f4f0e6":"#172824");
  const ink=shot.style?.ink || (shot.index%2===0?"#172824":"#f4f0e6");
  const accent=shot.style?.accent || ink;
  const zoom=1.04+progress*0.09;
  // Frame-accurate energy-transient responsiveness, not a claimed verified musical beat.
  const nearest=Math.min(999,...(shot.pulseFrames||[]).map(t=>Math.abs(t-frame)));
  const pulseScale=1+0.16*Math.max(0,1-nearest/5);
  return <AbsoluteFill style={{background:bg,overflow:"hidden"}}>
    {shot.asset && <AbsoluteFill style={{transform:"scale("+(zoom*pulseScale)+")"}}>
      <OffthreadVideo src={staticFile("assets/"+shot.asset)}
        muted style={{height:"100%",width:"100%",objectFit:"cover"}} />
    </AbsoluteFill>}
    {!shot.asset && <AbsoluteFill style={{overflow:"hidden"}}>
      <div style={{position:"absolute",left:"10%",top:"20%",
          width:"80%",height:"65%",border:"8px solid "+ink,
          borderRadius:"45%",transform:"translateY("+floatY+"px) rotate("+
            (progress*25)+"deg) scale("+(zoom*pulseScale)+")",opacity:.24}} />
      <div style={{position:"absolute",left:"38%",top:"42%",
          width:160,height:160,borderRadius:"50%",
          background:accent,transform:"translateX("+(progress*220-100)+"px) scale("+pulseScale+")"}} />
    </AbsoluteFill>}
    <AbsoluteFill style={{display:"flex",alignItems:"center",
      justifyContent:"center",padding:100}}>
      <div dir="auto" style={{fontFamily:"sans-serif",textAlign:"center",
        fontSize:58,fontWeight:700,color:ink,
        padding:32,background:shot.asset?"#17282499":"transparent",
        opacity,transform:"translateY("+(40*(1-progress))+"px)"}}>
        {shot.caption}
      </div>
    </AbsoluteFill>
  </AbsoluteFill>;
}
export function KOSIFVideo(){
  return <AbsoluteFill>
    {plan.shots.map(shot=><Sequence key={shot.index}
      from={shot.startFrame} durationInFrames={shot.frames}>
      <Shot shot={shot}/>
    </Sequence>)}
    {plan.audio && <Audio src={staticFile("assets/"+plan.audio)} />}
  </AbsoluteFill>;
}
'''


def scalar(x,label,low=0,high=300):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not low<=x<=high:
        raise ValueError(label+" must be a finite number within range")
    return float(x)


def load(path):
    p=Path(path)
    if not p.is_file() or p.is_symlink() or p.stat().st_size>2_000_000:
        raise ValueError("JSON must be a regular local file under 2 MB")
    return json.loads(p.read_text(encoding="utf8"))


def aligned(words,duration):
    if not isinstance(words,list) or len(words)>1500:raise ValueError("invalid words")
    prev=0
    out=[]
    for row in words:
        if not isinstance(row,dict):raise ValueError("word must be object")
        spelling=row.get("text",row.get("word"))
        if not isinstance(spelling,str) or not spelling.strip() or len(spelling)>120 or any(ord(c)<32 for c in spelling):
            raise ValueError("invalid caption word")
        a=scalar(row.get("start"),"word start",0,duration)
        b=scalar(row.get("end"),"word end",0,duration)
        if a<prev-0.00001 or b<=a:raise ValueError("word alignment overlaps")
        prev=b
        out.append({"text":spelling.strip(),"start":a,"end":b})
    return out


def plan(probe,cues=None,fps=30,mode="original"):
    if fps not in FPS:raise ValueError("unsupported fps")
    if mode not in {"original","pace-only"}:raise ValueError("unsupported mode")
    if probe.get("status")!="reference_timing_observed_not_animation_reconstructed":
        raise ValueError("requires real KOSIF motion_reference_probe report")
    ref_duration=scalar(probe.get("duration_seconds"),"reference duration",0.1,300)
    raw=probe.get("cut_candidates_seconds")
    if not isinstance(raw,list) or len(raw)>=MAX_SHOTS:
        raise ValueError("too many or malformed cut candidates")
    cuts=[];prev=0.0
    for value in raw:
        sec=scalar(value,"reference cut",0,ref_duration)
        if not prev+0.02<sec<ref_duration-0.02:raise ValueError("cuts not ordered and distinct")
        cuts.append(sec)
        prev=sec
    if cues is not None:
        if cues.get("schema")!="kosif.audio-cues.v1":raise ValueError("invalid cue schema")
        duration=scalar(cues.get("duration"),"audio duration",0.1,120)
        words=aligned(cues.get("words",[]),duration)
        candidates=cues.get("onset_candidates_seconds",[])
        if not isinstance(candidates,list) or len(candidates)>600:raise ValueError("invalid transients")
        transients=[scalar(c,"audio transient",0,duration) for c in candidates]
        if transients!=sorted(transients):raise ValueError("transients not ordered")
    else:
        duration=ref_duration;words=[];transients=[]
    total_frames=max(1,round(duration*fps))
    scaled=[t*duration/ref_duration for t in cuts]
    # Quantize all timings to actual integer frames. Keep cuts strictly apart,
    # correcting word splits by preferring a nearby word end when possible.
    boundaries=[0];adjustments=[]
    for i,cut in enumerate(scaled):
        desired=round(cut*fps)
        best=desired
        for w in words:
            if w["start"] < best/fps < w["end"]:
                options=[round(w["start"]*fps),round(w["end"]*fps)]
                best=min(options,key=lambda n:(abs(n-desired),n))
                if abs(best-desired)>round(0.50*fps):
                    raise ValueError("cannot preserve word around cut within 0.5 s")
                break
        best=max(boundaries[-1]+1,min(best,total_frames-1-(len(scaled)-i-1)))
        if best>=total_frames or best<=boundaries[-1]:
            raise ValueError("audio too short for reference cut count at requested FPS")
        if best!=desired:adjustments.append({"cut":i,"requestedFrame":desired,"wordSafeFrame":best})
        boundaries.append(best)
    boundaries.append(total_frames)
    shots=[]
    for i,(start,end) in enumerate(zip(boundaries,boundaries[1:])):
        if end<=start:raise ValueError("zero-length shot")
        a,b=start/fps,end/fps
        utterance=[w["text"] for w in words if w["start"]>=a-0.00001 and w["end"]<=b+0.00001]
        nearby=[round(t,4) for t in transients if a<=t<b]
        shots.append({"index":i,"startFrame":start,"endFrame":end,"frames":end-start,
                      "startSeconds":round(a,6),"endSeconds":round(b,6),
                      "caption":" ".join(utterance[:10])[:140] or ("مشهد "+str(i+1)),
                      "transientCandidates":nearby[:30],
                      "pulseFrames":[max(0,min(end-start-1,round(t*fps)-start)) for t in nearby[:30]],"asset":None,
                      "motion":{"camera":"slow-push" if i%2==0 else "lateral-float",
                                "transition":"hard-cut"}})
    assert sum(s["frames"] for s in shots)==total_frames
    sizes=[s["frames"] for s in shots]
    return {"schema":"kosif.reference-edit.v1","mode":mode,
        "fps":fps,"width":1080,"height":1920,"duration":round(duration,6),
        "totalFrames":total_frames,"audio":None,"shots":shots,"alignedWords":words,
        "evidence":{"referenceSeconds":ref_duration,"referenceCuts":len(cuts),
             "scaleFactor":round(duration/ref_duration,6),
             "frameAdjustmentForWords":adjustments,
             "alignedWordCount":len(words),"wordClock":"audio-timestamps-original",
             "cutTimingSource":"ffmpeg-cut-candidates","cutTimingVerified":False,
             "referenceVideoPixelsCopied":False,
             "medianShotFrames":statistics.median(sizes),
             "onsetCandidatesNotVerifiedBeats":True,
             "semanticUnderstanding":False,"renderVerified":False},
        "licenseNotes":"Source timing only. Use owned/relicensed clips and obey Remotion commercial license."}



def apply_visual_fingerprint(edit,visual):
    """Transfer aggregate color/layout measurements into NEW edit project styles.

    Never copies source pixels, reference shots, captions or audio. The
    palette is quantized from measured 64x36 sampled frames and must not be
    treated as source-faithful color grading or automatic semantic recognition.
    """
    if not isinstance(visual,dict) or visual.get("schema")!="kosif.reference-visual-fingerprint.v1":
        raise ValueError("requires measured KOSIF visual fingerprint")
    ref=scalar(edit["evidence"]["referenceSeconds"],"reference seconds",.1,300)
    observed=scalar(visual.get("duration"),"visual duration",.1,120)
    if abs(ref-observed)>.25:
        raise ValueError("reference and visual fingerprint durations mismatch")
    sections=visual.get("sections")
    if not isinstance(sections,list) or not 1<=len(sections)<=MAX_SHOTS:
        raise ValueError("invalid measured visual sections")
    checked=[]
    previous=0.0
    for idx,s in enumerate(sections):
        if not isinstance(s,dict) or s.get("index")!=idx:
            raise ValueError("sections need ordered indices")
        start=scalar(s.get("start"),"visual start",0,observed)
        end=scalar(s.get("end"),"visual end",0,observed)
        if abs(start-previous)>.1 or end<=start:
            raise ValueError("visual spans must be contiguous and ordered")
        previous=end
        palette=s.get("palette")
        if not isinstance(palette,list) or not 1<=len(palette)<=4:
            raise ValueError("missing measured hex palette")
        if any(not isinstance(col,str) or not re.fullmatch(r"#[0-9a-f]{6}",col) for col in palette):
            raise ValueError("untrusted palette value rejected")
        motion=s.get("possible_translation")
        if motion not in ("none","horizontal_candidate","vertical_candidate"):
            raise ValueError("unknown motion evidence label")
        checked.append(s)
    if abs(previous-observed)>.15:
        raise ValueError("visual sections do not cover reference duration")
    def legible_ink(bg):
        rgb=[int(bg[i:i+2],16) for i in (1,3,5)]
        # WCAG relative luminance estimate, chosen ink from a fixed trusted pair.
        def linear(c):
            v=c/255
            return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
        lum=.2126*linear(rgb[0])+.7152*linear(rgb[1])+.0722*linear(rgb[2])
        return "#172824" if lum>.23 else "#f4f0e6"
    for shot in edit["shots"]:
        middle=(shot["startFrame"]+shot["endFrame"])/(2*edit["fps"])
        sec=middle*ref/edit["duration"]
        source=next((s for s in checked if s["start"]<=sec<s["end"]),checked[-1])
        bg=source["palette"][0]
        accent=source["palette"][1] if len(source["palette"])>1 else "#355b47"
        shot["style"]={
            "background":bg,"ink":legible_ink(bg),"accent":accent,
            "panHint":source["possible_translation"],
            "provenance":"measured 64x36 pixel statistics, inspired design only"
        }
    edit["evidence"]["visualStyleApplied"]=True
    edit["evidence"]["visualSamplingVerifiedByExternalVideo"]=False
    edit["evidence"]["visualSourcePixelsCopied"]=False
    edit["evidence"]["objectTrackingVerified"]=False
    edit["evidence"]["visualSource"]="KOSIF reference-visual-fingerprint.v1"
    return edit

def basename(value,extensions):
    if not isinstance(value,str) or not BASENAME.fullmatch(value) or value.startswith("."):
        raise ValueError("asset must be a simple filename, no subdirectories or traversal")
    if Path(value).suffix.lower() not in extensions:
        raise ValueError("asset extension not permitted")
    return value


def stage_assets(project,root,manifest,shots):
    if not isinstance(manifest,dict) or not isinstance(manifest.get("clips",[]),list):
        raise ValueError("manifest needs clips array")
    clips=manifest.get("clips",[])
    if clips and len(clips)!=len(shots):
        raise ValueError("replacement clips count must match reference shot count")
    audio=manifest.get("audio")
    refs=[(basename(n,ASSET_EXTS),"clip_"+str(i).zfill(3)+Path(n).suffix.lower()) for i,n in enumerate(clips)]
    if audio is not None:refs.append((basename(audio,AUDIO_EXTS),"audio"+Path(audio).suffix.lower()))
    if not refs:return None
    if root is None or not Path(root).is_dir() or Path(root).is_symlink():
        raise ValueError("assets-dir must be existing regular directory")
    src_root=Path(root).resolve()
    total=0;originals=[]
    for a,b in refs:
        src=src_root/a
        if not src.is_file() or src.is_symlink():
            raise ValueError("asset missing, symlink, or not a file")
        size=src.stat().st_size
        if size<1 or size>FILE_LIMIT:raise ValueError("asset too large or empty")
        total+=size
        originals.append((src,b))
    if total>800_000_000:raise ValueError("combined assets exceed 800 MB")
    dest=project/"public"/"assets"
    dest.mkdir(parents=True)
    for src,target in originals:shutil.copyfile(src,dest/target)
    for i,(_,new) in enumerate(originals[:len(clips)]):shots[i]["asset"]=new
    return originals[-1][1] if audio is not None else None


def check_audio_length(path,edit):
    """The replacement audio is the master clock: its length must match the timeline (±1 frame + 50 ms).
    Fails closed on a mismatch; reports honestly when ffprobe is missing and nothing was measured."""
    fps=float(edit.get("fps") or 30);timeline=float(edit.get("duration") or edit.get("totalFrames",0)/fps)
    if not shutil.which("ffprobe"):
        return {"timelineSeconds":timeline,"audioSeconds":None,"lengthVerified":False,"why":"ffprobe not installed"}
    import subprocess
    r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(path)],
                     capture_output=True,text=True,timeout=60)
    try:seconds=float(r.stdout.strip())
    except ValueError:
        return {"timelineSeconds":timeline,"audioSeconds":None,"lengthVerified":False,
                "why":f"ffprobe could not read a duration from {path.name}; check it before rendering"}
    if abs(seconds-timeline)>1/fps+0.05:
        raise ValueError(f"replacement audio is {seconds:.3f} s but the timeline from --cues is {timeline:.3f} s; "
                         "build the cues from this audio so it stays the master clock")
    return {"timelineSeconds":timeline,"audioSeconds":round(seconds,3),"lengthVerified":True}


def create_project(project,edit,manifest=None,assets_dir=None):
    dest=Path(project)
    if dest.exists() or dest.is_symlink() or not dest.parent.is_dir():
        raise ValueError("target must be an unused directory under an existing parent")
    if not isinstance(edit,dict) or edit.get("schema")!="kosif.reference-edit.v1":
        raise ValueError("invalid timeline")
    # Inspect sources and manifest before mkdir so failures do not touch the disk.
    manifest=manifest or {}
    clips=manifest.get("clips",[])
    if not isinstance(clips,list) or (clips and len(clips)!=len(edit["shots"])):
        raise ValueError("clip counts must match shot counts")
    names=list(clips)
    if manifest.get("audio") is not None:names.append(manifest["audio"])
    for i,name in enumerate(names):
        basename(name,AUDIO_EXTS if i==len(clips) else ASSET_EXTS)
        if assets_dir is None or not (Path(assets_dir)/name).is_file() or (Path(assets_dir)/name).is_symlink():
            raise ValueError("replacement asset missing, symlinked or no directory provided")
    audio_check=check_audio_length(Path(assets_dir)/manifest["audio"],edit) if manifest.get("audio") is not None else None
    dest.mkdir()
    try:
        (dest/"src").mkdir()
        e=json.loads(json.dumps(edit))
        e["audio"]=stage_assets(dest,assets_dir,manifest,e["shots"])
        if audio_check is not None:e["evidence"]["replacementAudio"]=audio_check
        (dest/"package.json").write_text(json.dumps(PACKAGE,indent=2)+"\n",encoding="utf8")
        (dest/"src"/"index.jsx").write_text(INDEX,encoding="utf8")
        (dest/"src"/"Root.jsx").write_text(ROOT,encoding="utf8")
        (dest/"src"/"Video.jsx").write_text(VIDEO,encoding="utf8")
        (dest/"src"/"plan.json").write_text(json.dumps(e,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        (dest/"decision-report.json").write_text(json.dumps(e["evidence"],ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        audit=inspect_plan(e,dest)
        if audit["failures"]:
            raise ValueError("creative quality gate blocked project: "+", ".join(audit["failures"]))
        (dest/"quality-audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        (dest/"README.md").write_text(
          "# KOSIF Reference Edit — original editable project\n\n"
          "1. Review src/plan.json cut timings and src/Video.jsx motion styles.\n"
          "2. Review commercial license at https://www.remotion.dev/license before install/render.\n"
          "3. From this directory run npm install, then npm run studio; then npm run render after approval.\n"
          "4. If assets are absent, each shot uses original animated placeholder geometry;\n"
          "   no footage from the reference is copied. Add authorized replacement clips to public/assets.\n"
          "5. Cuts are ffmpeg scene-change candidates, not proven visual/semantic fidelity.\n"
          "6. Inspect rendered frame boundaries, media codecs, clip duration, audio sync and final MP4.\n"
          "7. Audio is a single track; use user-owned audio; no lyrics or emotions inferred.\n",
          encoding="utf8")
    except BaseException:
        shutil.rmtree(dest)
        raise
    return {"status":"editable_project_created_unrendered",
            "project":str(dest.resolve()),"shots":len(edit["shots"]),
            "frames":edit["totalFrames"],"external_packages_not_installed":True,
            "reference_footage_copied":False,
            "assets_copied":len(names)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--probe",required=True,help="saved motion_reference_probe.py JSON")
    ap.add_argument("--cues",help="audio_cue_mapper.py JSON with optional aligned words")
    ap.add_argument("--visual",help="reference_visual_fingerprint.py JSON of same authorized source")
    ap.add_argument("--manifest",help="optional {clips:[...],audio:'...'} owned replacement media")
    ap.add_argument("--assets-dir",help="local authorized replacement media directory")
    ap.add_argument("--fps",type=int,choices=FPS,default=30)
    ap.add_argument("--out",required=True,help="NEW Remotion project directory")
    args=ap.parse_args()
    try:
        ref=load(args.probe); cues=load(args.cues) if args.cues else None
        manifest=load(args.manifest) if args.manifest else None
        edit=plan(ref,cues,args.fps)
        if args.visual:
            apply_visual_fingerprint(edit,load(args.visual))
        print(json.dumps(create_project(args.out,edit,manifest,args.assets_dir),ensure_ascii=False))
    except (ValueError,KeyError,OSError,TypeError,json.JSONDecodeError) as exc:
        ap.error(str(exc))


if __name__=="__main__":
    main()
