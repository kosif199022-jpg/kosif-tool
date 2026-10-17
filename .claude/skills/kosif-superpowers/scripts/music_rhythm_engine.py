#!/usr/bin/env python3
"""KOSIF original music rhythm hypotheses from real measured onset candidates.

No audio recognition, chord/emotion identification, generated lyrics, or
"verified BPM" claims. Audio source must first be measured by audio_cue_mapper.
This deterministic heuristic compares many tempo aliases and publishes evidence.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import statistics

def number(x,name,lo,hi):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not lo<=x<=hi:
        raise ValueError(name+" invalid or outside allowed range")
    return float(x)

def rhythm(cues,min_bpm=60,max_bpm=200):
    if not isinstance(cues,dict) or cues.get("schema")!="kosif.audio-cues.v1":
        raise ValueError("expected KOSIF measured audio cues")
    duration=number(cues.get("duration"),"duration",0.1,120)
    events=cues.get("onset_candidates_seconds")
    if not isinstance(events,list) or len(events)>600:
        raise ValueError("onsets must be measured list <=600")
    events=[number(x,"onset",0,duration) for x in events]
    if any(a>=b for a,b in zip(events,events[1:])):
        raise ValueError("onsets must be strictly increasing")
    if not isinstance(min_bpm,int) or not isinstance(max_bpm,int) or not 40<=min_bpm<max_bpm<=240:
        raise ValueError("tempo search out of range")
    values=cues.get("energy_rms",[])
    if not isinstance(values,list) or len(values)>10000:
        raise ValueError("invalid RMS envelope")
    values=[number(x,"RMS",0,1) for x in values]
    window=number(cues.get("window_seconds",0.05),"window seconds",0.001,1)
    sorted_scores=[]
    if len(events)>=4:
        for bpm in range(min_bpm,max_bpm+1):
            period=60/bpm
            best=(0,float('inf'),-1,None)
            for anchor in events[:min(12,len(events))]:
                errs=[min((t-anchor)%period, period-((t-anchor)%period)) for t in events]
                close=sum(err<=0.055 for err in errs)
                expected=max(1,duration/period)
                coverage=min(1,len(events)/expected)
                score=(close/len(events))*(0.60+0.40*coverage)
                # Penalize artificial fast tempos with extra "missing" beats.
                mean_error=statistics.mean(errs)
                if score>best[0]+1e-9 or (abs(score-best[0])<=1e-9 and mean_error<best[1]):
                    best=(score,mean_error,close,anchor)
            sorted_scores.append({"bpm":bpm,"match":round(best[0],5),
                                  "aligned_onsets":best[2],
                                  "mean_error_seconds":round(best[1],6),
                                  "phase_anchor_seconds":best[3]})
    sorted_scores.sort(key=lambda x:(-x["match"],x["mean_error_seconds"],x["bpm"]))
    # Avoid listing near-duplicate tempo hypotheses as meaningfully distinct.
    alternatives=[]
    for x in sorted_scores:
        if all(abs(x["bpm"]-a["bpm"])>=6 for a in alternatives):
            alternatives.append(x)
        if len(alternatives)>=3:break
    winner=alternatives[0] if alternatives else None
    grid=[]
    if winner and winner["match"]>=0.60:
        p=60/winner["bpm"]
        start=winner["phase_anchor_seconds"]
        while start-p>=0:start-=p
        for i in range(min(500,math.ceil(duration/p)+2)):
            tick=start+i*p
            if tick>duration:break
            grid.append(round(tick,4))
    sections=[]
    if values:
        full_median=statistics.median(values)
        for idx in range(math.ceil(duration)):
            a=round(idx/window);b=min(len(values),round((idx+1)/window))
            window_data=values[a:b]
            if not window_data:continue
            rms=statistics.mean(window_data)
            sections.append({"start":idx,"end":min(duration,idx+1),
                             "mean_rms":round(rms,6),
                             "energy_label":"higher_than_track_median" if rms>full_median*1.25 else
                                            "lower_than_track_median" if rms<full_median*0.75 else "middle"})
    return {
        "schema":"kosif.music-rhythm-hypotheses.v1",
        "duration":duration,
        "source":cues.get("source"),
        "tempo_hypotheses":alternatives,
        "candidate_tempo_bpm":winner["bpm"] if winner and winner["match"]>=0.60 else None,
        "estimated_grid_seconds":grid,
        "measured_transients_seconds":events,
        "relative_energy_sections":sections,
        "verified_bpm":False,
        "lyric_understanding":False,
        "emotion_detection":False,
        "notes":["candidate tempo and grid based on onset alignment only; not ground truth",
                 "half/double-time ambiguity is common; user can override",
                 "energy level cannot reliably infer musical mood or semantic meaning",
                 "local original-audio measurements, no model downloads or transcription"]
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("cues",help="JSON from audio_cue_mapper.py")
    p.add_argument("--out",required=True,help="new output JSON, must not already exist")
    args=p.parse_args()
    try:
        src=Path(args.cues)
        if not src.is_file() or src.is_symlink() or src.stat().st_size>2_000_000:
            raise ValueError("invalid cues file")
        cues=json.loads(src.read_text(encoding="utf8"))
        result=rhythm(cues)
        out=Path(args.out)
        if not out.parent.is_dir() or out.is_symlink():
            raise ValueError("output requires an existing parent folder")
        with out.open("x",encoding="utf8") as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
            f.write("\n")
        print(json.dumps({"path":str(out.resolve()),"tempo_candidate":result["candidate_tempo_bpm"],
                          "verified_bpm":False,"beat_grid":len(result["estimated_grid_seconds"])},
                         ensure_ascii=False))
    except (ValueError,TypeError,OSError,json.JSONDecodeError) as exc:
        p.error(str(exc))

if __name__=="__main__":
    main()
