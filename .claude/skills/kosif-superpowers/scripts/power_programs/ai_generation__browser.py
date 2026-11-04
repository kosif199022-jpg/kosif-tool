"""Wave-2 browser program for ai-generation: GEN-72, the draw-over look on a motion base.

No generated base is needed to test the look: any footage works, so the fixture is a short
ffmpeg clip (a moving bright subject). A hand-written canvas look (film.js renderAt(t)) redraws
every frame as two-ink halftone with a 12/s boil and paper tooth, and places the shot's lyric
type opposite the subject; headless Chromium photographs each frame. Checks are known answers:
two inks plus paper only, frames inside one 1/12 s boil step identical, a new boil step differs,
type on the side opposite the subject.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ._browser_common import browser, ff, img, page

PAPER, INK_A, INK_B = (243, 238, 228), (20, 24, 60), (220, 60, 50)
FILM_JS = """
const shots=SHOTS;const W=96,H=54;const c=document.getElementById('c'),g=c.getContext('2d');const v=document.getElementById('v');
const off=document.createElement('canvas');off.width=W;off.height=H;const og=off.getContext('2d',{willReadFrequently:true});
function hash(i){let h=(i*374761393)|0;h=Math.imul(h^(h>>>13),1274126177);return ((h^(h>>>16))>>>0)/4294967296}
function shotAt(t){return shots.find(s=>t>=s.at&&t<s.at+s.dur)}
async function seekBase(t){const s=shotAt(t);const lt=s.baseStart+(t-s.at);if(Math.abs(v.currentTime-lt)>1e-4){await new Promise(r=>{v.onseeked=r;v.currentTime=lt})}return s}
window.renderAt=async(t)=>{window.__ready=false;const s=await seekBase(t);og.drawImage(v,0,0,W,H);const src=og.getImageData(0,0,W,H).data;
const step=Math.floor(t*12);const jx=Math.floor(hash(step)*3)-1,jy=Math.floor(hash(step+99)*3)-1;
g.fillStyle='rgb(PAPER)';g.fillRect(0,0,W,H);
for(let y=0;y<H;y+=3)for(let x=0;x<W;x+=3){const i=((y*W)+x)*4;const l=(src[i]*.3+src[i+1]*.59+src[i+2]*.11)/255;const r=1.6*(1-l);
 if(r>0.2){g.fillStyle='rgb(INKA)';g.fillRect(x+jx,y+jy,Math.max(1,Math.round(r)),Math.max(1,Math.round(r)));}
 if(src[i]>200&&src[i+1]<120){g.fillStyle='rgb(INKB)';g.fillRect(x+1+jx,y+1+jy,1,1);}}
for(let k=0;k<40;k++){const x=Math.floor(hash(k*7+step)*W),y=Math.floor(hash(k*13+step)*H);g.fillStyle='rgb(INKA)';if(hash(k+step*31)>0.85)g.fillRect(x,y,1,1);}
if(s.type!=='none'){const side=s.side==='left'?'right':'left';g.fillStyle='rgb(INKB)';const w=s.type==='big'?30:14;
 g.fillRect(side==='right'?W-w-4:4,H/2-6,w,s.type==='big'?12:6);window.__typeSide=side;}
window.__ready=true;};
v.addEventListener('loadeddata',()=>{window.__loaded=true},{once:true});v.load();"""


def gen_72(work: Path):
    """Draw-over on a motion base: shots.json, renderAt(t) two-ink halftone, 12/s boil, paper tooth, lyric type opposite the subject."""
    ff("-f", "lavfi", "-i", "color=c=0x303030:s=96x54:r=24:d=2", "-f", "lavfi", "-i", "color=c=0xff3020:s=20x20:r=24:d=2",
       "-filter_complex", "[0][1]overlay=x='5+t*10':y=17", "-c:v", "libvpx", "-g", "1", "-b:v", "500k", str(work / "base.webm"))
    shots = [{"at": 0, "dur": 1, "base": "base.webm", "baseStart": 0, "focus": 0.2, "type": "big", "side": "left"},
             {"at": 1, "dur": 1, "base": "base.webm", "baseStart": 0.5, "focus": 0.8, "type": "none", "side": "left"}]
    (work / "shots.json").write_text(json.dumps(shots, indent=1))
    js = (FILM_JS.replace("SHOTS", json.dumps(shots)).replace("PAPER", ",".join(map(str, PAPER)))
          .replace("INKA", ",".join(map(str, INK_A))).replace("INKB", ",".join(map(str, INK_B))))
    page(work, "film.html", f"<!doctype html><html><body style='margin:0'><video id='v' src='/base.webm' muted preload='auto' style='display:none'></video>"
                            f"<canvas id='c' width='96' height='54'></canvas><script>{js}</script></body></html>")
    times = [0.10, 0.12, 0.20, 1.30]       # 0.10 and 0.12 share boil step 1; 0.20 is step 2
    r = browser(work, {"context": {"viewport": {"width": 96, "height": 54}}, "steps": [
        {"op": "goto", "url": "/film.html"}, {"op": "wait", "js": "window.__loaded===true"},
        {"op": "frames", "times": times, "fps": 100, "indexFromTime": True, "dir": str(work / "frames"), "fast": True,
         "renderJs": "(t)=>window.renderAt(t)", "waitJs": "window.__ready===true", "readyFlag": False},
        {"op": "eval", "js": "window.__typeSide", "as": "side"}]})
    f = {t: img(work / "frames" / f"f_{round(t * 100):04d}.png") for t in times}
    cols = {tuple(c) for c in f[0.2].reshape(-1, 3).tolist()}
    allowed = {PAPER, INK_A, INK_B}
    near_allowed = all(min(sum(abs(a - b) for a, b in zip(c, p)) for p in allowed) <= 6 for c in cols)
    def ink_b_cols(a):
        m = (np.abs(a - np.array(INK_B)).sum(axis=2) < 10)
        return m
    right_type = ink_b_cols(f[0.1])[21:33, 62:92].mean()
    return [("only two inks on paper", near_allowed and len(cols) <= 12, f"{len(cols)} colours"),
            ("same 1/12 s boil step -> identical frames (0.10 vs 0.12 s)", bool((f[0.1] == f[0.12]).all()), ""),
            ("next boil step jitters the drawing (0.20 s)", bool((f[0.1] != f[0.2]).any()), str(int((f[0.1] != f[0.2]).any(axis=2).sum()))),
            ("subject on the left -> big type block on the right", right_type > 0.9 and r["values"]["side"] == "right", f"{right_type:.2f}"),
            ("type 'none' shot draws no type block", ink_b_cols(f[1.3])[21:33, 62:92].mean() < 0.3, f"{ink_b_cols(f[1.3])[21:33, 62:92].mean():.2f}"),
            ("shot 2 reads its base from baseStart 0.5 (subject moved right)", np.argmax(ink_b_cols(f[1.3])[17:37].sum(axis=0)) > np.argmax(ink_b_cols(f[0.2])[17:37, :60].sum(axis=0)), "")]


PROGRAMS = {"GEN-72": gen_72}
