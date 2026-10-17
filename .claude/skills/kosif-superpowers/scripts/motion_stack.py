#!/usr/bin/env python3
"""Build original, editable starters for installed third-party motion engines.

No network, installation, downloads, execution, tokens or automatic commercial
license agreement. Backend-specific source is an original scaffold invoking a
package that the user must obtain and authorize separately.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys
from textwrap import dedent

ROOT=Path(__file__).resolve().parent.parent
REGISTRY=ROOT/"data"/"motion_sources.json"

GSAP_PACKAGE={"name":"kosif-gsap-timeline","private":True,"type":"module",
 "scripts":{"dev":"vite --host 127.0.0.1","build":"vite build"},
 "dependencies":{"gsap":"^3.14.0","roughjs":"^4.6.0","vivus":"^0.4.6"},
 "devDependencies":{"vite":"^6.0.0"}}
GSAP_HTML="""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>KOSIF GSAP</title>
<style>body{margin:0;background:#f4f0e6}svg{display:block;height:100vh;width:auto;max-width:100vw;margin:auto;background:#f4f0e6}</style>
</head><body><svg id="art" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">
<text id="title" x="540" y="450" text-anchor="middle" font-size="70" fill="#172824" font-family="Arial,sans-serif">الخط يتحرك</text>
<path id="line" d="M180 800 C330 540 710 1150 900 800" stroke="#355b47" stroke-width="12"
fill="none" stroke-linecap="round"/><circle id="sun" cx="540" cy="1260" r="120" fill="#355b47"/>
</svg><script type="module" src="/src/main.js"></script></body></html>
"""
GSAP_SOURCE=dedent("""
    // Independent KOSIF adapter using GSAP public APIs; no third-party code included.
    import {gsap} from 'gsap';
    import rough from 'roughjs';
    import Vivus from 'vivus';

    const svg=document.querySelector('#art');
    const line=document.querySelector('#line');
    // Rough.js makes a drawable, editable hand-sketch using local SVG geometry.
    const roughLayer=rough.svg(svg);
    const sketch=roughLayer.circle(360,1420,250,{stroke:'#172824',
      strokeWidth:4,roughness:1.5,fill:'none'});
    svg.appendChild(sketch);
    // Vivus provides the separately optional stroke-reveal player.
    const vivus=new Vivus('art',{type:'sync',duration:90,start:'manual'});
    const t=gsap.timeline({paused:true,defaults:{ease:'power2.out'}});
    t.from('#title',{opacity:0,y:75,duration:1},0)
     .from('#sun',{scale:0.2,transformOrigin:'50% 50%',duration:2},0.2)
     .to('#sun',{x:250,rotation:90,duration:3},1.5);
    const duration=6;
    window.__kosif={duration,fps:30,seek(sec) {
      const time=Math.max(0,Math.min(duration,sec));
      t.time(time,false);
      // Stroke reveal remains seekable regardless of playback speed.
      const progress=time/duration;
      const length=line.getTotalLength();
      line.style.strokeDasharray=String(length);
      line.style.strokeDashoffset=String(length*(1-progress));
      vivus.setFrameProgress(progress);
    }};
    window.__kosifReady=document.fonts.ready;
    window.__kosif.seek(0);
""").strip()+"\n"

REMOTION_PACKAGE={"name":"kosif-remotion-video","private":True,"type":"module",
 "scripts":{"studio":"remotion studio src/index.jsx","render":"remotion render src/index.jsx KOSIFVideo out.mp4"},
 "dependencies":{"@remotion/cli":"^4.0.0","remotion":"^4.0.0",
                 "react":"^19.0.0","react-dom":"^19.0.0"}}
REMOTION_INDEX=dedent("""
    import {registerRoot} from 'remotion';
    import {Root} from './root.jsx';
    registerRoot(Root);
""").strip()+"\n"
REMOTION_ROOT=dedent("""
    import React from 'react';
    import {Composition} from 'remotion';
    import {Video} from './video.jsx';
    export const Root=()=> <Composition id="KOSIFVideo" component={Video}
      durationInFrames={270} fps={30} width={1080} height={1920}/>;
""").strip()+"\n"
REMOTION_VIDEO=dedent("""
    import React from 'react';
    import {useCurrentFrame, useVideoConfig, interpolate, Easing} from 'remotion';
    // Original KOSIF composition, no source or assets copied from Remotion examples.
    export const Video=()=>{
      const frame=useCurrentFrame();
      const {fps,width,height}=useVideoConfig();
      const x=interpolate(frame,[0,135,270],[-80,120,260],
        {extrapolateLeft:'clamp',extrapolateRight:'clamp'});
      const opacity=interpolate(frame,[0,28],[0,1],
        {extrapolateRight:'clamp',easing:Easing.out(Easing.cubic)});
      const pathLength=Math.max(0,Math.min(1,frame/210));
      return <div style={{background:'#f4f0e6',width,height,position:'relative'}}>
        <svg viewBox="0 0 1080 1920" width={width} height={height}>
          <text x="540" y="430" textAnchor="middle" direction="rtl"
            fontSize="72" fill="#172824" opacity={opacity}>KOSIF موشن بالكود</text>
          <path d="M190 850 Q540 560 890 850" fill="none" stroke="#355b47"
            strokeWidth="12" strokeLinecap="round" pathLength="1"
            strokeDasharray="1" strokeDashoffset={1-pathLength}/>
          <circle cx={500+x} cy="1230" r="135" fill="#355b47"/>
        </svg>
      </div>;
    };
""").strip()+"\n"

MANIM_SOURCE=dedent("""
    # Original KOSIF scene using public Manim imports. Requires an installed Manim.
    from manim import *
    class KOSIFExplain(Scene):
        def construct(self):
            self.camera.background_color = "#f4f0e6"
            title = Text("KOSIF Motion", color="#172824").scale(0.85).to_edge(UP)
            path = VMobject(stroke_color="#355b47",stroke_width=7)
            path.set_points_smoothly([LEFT*3+DOWN,LEFT+UP*0.2,RIGHT*3+DOWN])
            dot = Circle(radius=0.5,color="#355b47").set_fill("#355b47",opacity=1)
            self.play(Write(title),Create(path),run_time=3)
            self.play(MoveAlongPath(dot,path),run_time=3)
            self.play(FadeOut(dot),FadeOut(path),run_time=1)
    """).strip()+"\n"


def validate_registry():
    obj=json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources=obj.get("sources")
    if obj.get("schema")!="kosif.motion-toolbox.v1" or not isinstance(sources,list) or len(sources)!=25:
        raise ValueError("motion manifest missing or invalid")
    if len({x["repo"].lower() for x in sources})!=25:
        raise ValueError("duplicate motion source")
    if any(x.get("runtime_state")!="not_probed" for x in sources):
        raise ValueError("manually altered runtime claims")
    return sources


def recipes():
    return {
        "gsap": {"package.json":json.dumps(GSAP_PACKAGE,indent=2)+"\n",
                 "index.html":GSAP_HTML,"src/main.js":GSAP_SOURCE},
        "remotion": {"package.json":json.dumps(REMOTION_PACKAGE,indent=2)+"\n",
                    "src/index.jsx":REMOTION_INDEX,"src/root.jsx":REMOTION_ROOT,
                    "src/video.jsx":REMOTION_VIDEO},
        "manim":{"main.py":MANIM_SOURCE},
    }


def scaffold(backend, out):
    layouts=recipes()
    if backend not in layouts:
        raise ValueError("unsupported backend")
    p=Path(out).expanduser()
    if p.exists() or not p.parent.is_dir() or p.is_symlink():
        raise ValueError("scaffold requires a fresh directory in an existing parent")
    # Create all files exclusively; packages stay declarative until user installs them.
    p.mkdir()
    for name,content in layouts[backend].items():
        target=p/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(content,encoding="utf-8")
    return {"status":"scaffold_created_not_installed", "backend":backend,
            "folder":str(p.resolve()),"files":sorted(layouts[backend]),
            "runtime_ready":False,"installation_requires_user_approval":True}


def doctor():
    # Presence of an executable is not proof of package/import/runtime.
    return {"status":"tool_presence_only", "node":bool(shutil.which("node")),
            "npm":bool(shutil.which("npm")), "ffmpeg":bool(shutil.which("ffmpeg")),
            "ffprobe":bool(shutil.which("ffprobe")), "manim_cli":bool(shutil.which("manim")),
            "third_party_motion_engines_verified":False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("list")
    sub.add_parser("doctor")
    s=sub.add_parser("scaffold")
    s.add_argument("backend",choices=sorted(recipes()))
    s.add_argument("--out",required=True)
    args=p.parse_args()
    try:
        if args.cmd=="list":
            sources=validate_registry()
            result={"sources":[{k:x.get(k) for k in ("name","repo","role","npm","license_hint")}
                               for x in sources],"count":len(sources),
                    "runtime_status":"not_probed"}
        elif args.cmd=="doctor":
            result=doctor()
        else:
            validate_registry()
            result=scaffold(args.backend,args.out)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError,json.JSONDecodeError) as error:
        print(json.dumps({"status":"failed","error":str(error)}),file=sys.stderr)
        return 2
    return 0


if __name__=="__main__":
    sys.exit(main())
