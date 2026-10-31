#!/usr/bin/env python3
"""KOSIF Web Film («التنين الأسود»): plan, scaffold and check a video made as a webpage.

  web_film.py plan "<prompt>" --out film.plan.json [--duration 15] [--ratio 9:16] [--require "..."]...
  web_film.py scaffold film.plan.json --out film.html
  web_film.py check film.plan.json [--html film.html] [--json]

`check` exits 1 on any failure. It proves structure (shots, pacing, requirements, seek API, offline,
determinism), not taste: look at real stills before calling a film good.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

RATIOS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
KINDS = ("title", "words", "shape", "reveal", "outro")
TRANSITIONS = ("cut", "fade", "wipe", "zoom", "slide")
EPS = 1e-6


def default_plan(prompt: str, duration: float = 15.0, ratio: str = "9:16", requirements=None) -> dict:
    if ratio not in RATIOS:
        raise SystemExit(f"--ratio must be one of {', '.join(RATIOS)}")
    reqs = [r for r in (requirements or []) if r.strip()]
    # Uneven cuts on purpose: a short hook, a long middle, a held end.
    weights = [0.14, 0.24, 0.30, 0.18, 0.14]
    shots, t = [], 0.0
    for i, (w, kind, tr) in enumerate(zip(weights, KINDS, ("fade", "wipe", "zoom", "slide", "fade"))):
        end = round(duration if i == len(weights) - 1 else t + duration * w, 3)
        shots.append({"start": round(t, 3), "end": end, "kind": kind, "text": "", "transition_in": tr,
                      "motion": "", "covers": [], "memorable": kind == "shape"})
        t = end
    if reqs:
        shots[0]["covers"] = list(range(len(reqs)))
    w, h = RATIOS[ratio]
    return {"schema": "kosif.web_film.plan.v1", "prompt": prompt, "requirements": reqs,
            "concept": "", "visual_language": {"palette": ["#0b0b0f", "#e8e2d4", "#c8102e"],
                                               "type": "Cairo", "motif": "", "motion_rule": ""},
            "duration": duration, "fps": 30, "width": w, "height": h, "seed": 7, "shots": shots}


def check_plan(plan: dict) -> list[str]:
    errs = []
    dur = plan.get("duration")
    shots = plan.get("shots") or []
    if not isinstance(dur, (int, float)) or dur <= 0:
        return ["duration must be a positive number"]
    if len(shots) < 3:
        errs.append(f"need at least 3 shots, found {len(shots)}")
    if not (plan.get("concept") or "").strip():
        errs.append("concept is empty: write the one idea the film serves")
    t = 0.0
    for i, s in enumerate(shots):
        a, b = s.get("start"), s.get("end")
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or b <= a:
            errs.append(f"shot {i}: start/end invalid")
            continue
        if abs(a - t) > 1e-3:
            errs.append(f"shot {i} starts at {a}, expected {round(t, 3)} (gap or overlap)")
        if s.get("transition_in") not in TRANSITIONS:
            errs.append(f"shot {i}: transition_in must be one of {', '.join(TRANSITIONS)}")
        t = b
    if shots and abs(t - dur) > 1e-3:
        errs.append(f"shots end at {round(t, 3)}, film duration is {dur}")
    lengths = [round(s["end"] - s["start"], 2) for s in shots if isinstance(s.get("end"), (int, float))
               and isinstance(s.get("start"), (int, float))]
    if len(lengths) >= 3 and len(set(lengths)) == 1:
        errs.append("every shot has the same length: vary the pacing")
    for i in range(1, len(shots)):
        if shots[i].get("transition_in") == shots[i - 1].get("transition_in") and shots[i].get("transition_in") != "cut":
            errs.append(f"shots {i - 1} and {i} use the same transition ({shots[i]['transition_in']})")
    if shots and not any(s.get("memorable") for s in shots):
        errs.append("no shot is marked memorable")
    reqs = plan.get("requirements") or []
    covered = {c for s in shots for c in (s.get("covers") or []) if isinstance(c, int)}
    for k, r in enumerate(reqs):
        if k not in covered:
            errs.append(f"requirement {k} has no shot covering it: {r!r}")
    return errs


_NET = re.compile(r"""(?:src|href)\s*=\s*["']\s*(?:https?:)?//|@import\s+url\(\s*["']?(?:https?:)?//|fetch\(\s*["']https?://""", re.I)


def check_html(text: str, plan: dict) -> list[str]:
    errs = []
    if not re.search(r"window\.__kosif\s*=", text):
        errs.append("page does not define window.__kosif (the renderer's seek API)")
    if not re.search(r"\bseek\s*[:(]", text):
        errs.append("window.__kosif has no seek(t)")
    m = re.search(r"""["']?duration["']?\s*:\s*([0-9.]+)""", text)
    if m and abs(float(m.group(1)) - float(plan.get("duration", 0))) > 1e-3:
        errs.append(f"page duration {m.group(1)} differs from plan {plan.get('duration')}")
    if _NET.search(text):
        errs.append("page loads something from the network: keep fonts and images local")
    if re.search(r"\bDate\.now\(|new Date\(|performance\.now\(", text):
        errs.append("page reads the wall clock: every frame must be a function of t")
    if re.search(r"Math\.random\b", text):
        errs.append("unseeded Math.random(): use the seeded rng(seed)")
    if re.search(r"\bset(?:Interval|Timeout)\(", text):
        errs.append("setInterval/setTimeout drive motion: compute from t instead")
    scenes = len(re.findall(r'data-shot="\d+"', text))
    if scenes and scenes != len(plan.get("shots") or []):
        errs.append(f"page has {scenes} scenes, plan has {len(plan['shots'])} shots")
    return errs


ENGINE = r"""
const PLAN = __PLAN__;
function rng(seed){let s=seed>>>0;return()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
const ease = {
  out:(x)=>1-Math.pow(1-x,3), inOut:(x)=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,
  back:(x)=>{const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2);}
};
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const scenes=[...document.querySelectorAll('[data-shot]')];
const R=rng(PLAN.seed||7); const dots=[...Array(40)].map(()=>({x:R(),y:R(),r:2+R()*6}));
const TR=.45;
function enter(el,kind,p){
  const e=ease.out(p);
  el.style.opacity=kind==='cut'?1:(kind==='fade'||kind==='zoom'?e:1);
  el.style.clipPath=kind==='wipe'?`inset(0 ${(1-e)*100}% 0 0)`:'none';
  el.style.transform=kind==='zoom'?`scale(${1.25-.25*e})`:kind==='slide'?`translateY(${(1-e)*12}%)`:'none';
}
function drawShot(i,local,len){
  const s=PLAN.shots[i], el=scenes[i], u=clamp(local/len);
  const words=el.querySelectorAll('.w');
  words.forEach((w,k)=>{const p=clamp((local-.15-k*.12)/.5);w.style.opacity=p;w.style.transform=`translateY(${(1-ease.back(p))*40}px)`;});
  const shape=el.querySelector('.shape');
  if(shape){const a=ease.inOut(u);shape.style.transform=`rotate(${a*180}deg) scale(${.6+.6*a})`;shape.style.borderRadius=`${50-40*a}%`;}
  const field=el.querySelector('.field');
  if(field){field.innerHTML='';dots.forEach(d=>{const n=document.createElement('i');n.style.left=(d.x*100)+'%';n.style.top=((d.y+u*.3)%1*100)+'%';n.style.width=n.style.height=d.r+'px';field.appendChild(n);});}
}
window.__kosif={duration:PLAN.duration,seek(t){
  PLAN.shots.forEach((s,i)=>{
    const el=scenes[i], on=t>=s.start-1e-9&&(t<s.end||i===PLAN.shots.length-1);
    el.style.visibility=on?'visible':'hidden';
    if(on){enter(el,s.transition_in,clamp((t-s.start)/TR));drawShot(i,t-s.start,s.end-s.start);}
  });
}};
window.__kosif.seek(0);
"""


def scaffold(plan: dict) -> str:
    pal = (plan.get("visual_language") or {}).get("palette") or ["#0b0b0f", "#e8e2d4", "#c8102e"]
    bg, fg, accent = (pal + ["#0b0b0f", "#e8e2d4", "#c8102e"])[:3]
    font = (plan.get("visual_language") or {}).get("type") or "Cairo"
    rtl = bool(re.search(r"[؀-ۿ]", json.dumps(plan, ensure_ascii=False)))
    parts = []
    for i, s in enumerate(plan["shots"]):
        text = (s.get("text") or "").strip()
        words = "".join(f'<span class="w">{html.escape(w)}</span> ' for w in text.split())
        extra = {"shape": '<div class="shape"></div>', "reveal": '<div class="field"></div>'}.get(s.get("kind"), "")
        parts.append(f'<section class="scene k-{html.escape(s.get("kind", ""))}" data-shot="{i}">{extra}<h1>{words}</h1></section>')
    data = json.dumps({k: plan[k] for k in ("duration", "seed", "shots")}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="{'ar' if rtl else 'en'}" dir="{'rtl' if rtl else 'ltr'}"><head><meta charset="utf-8">
<title>{html.escape(plan.get('concept') or plan.get('prompt') or 'KOSIF web film')}</title>
<style>
html,body{{margin:0;width:{plan['width']}px;height:{plan['height']}px;overflow:hidden;background:{bg};color:{fg};font-family:'{font}',system-ui,sans-serif}}
.scene{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;visibility:hidden;will-change:transform,opacity}}
h1{{position:relative;margin:0 8%;font-size:{int(plan['width'] * 0.09)}px;line-height:1.25;text-align:center}}
.w{{display:inline-block}}
.shape{{position:absolute;inset:0;margin:auto;width:46%;aspect-ratio:1;background:{accent};opacity:.9}}
.field{{position:absolute;inset:0}} .field i{{position:absolute;border-radius:50%;background:{accent}}}
</style></head><body>
{chr(10).join(parts)}
<script>{ENGINE.replace('__PLAN__', data)}</script>
</body></html>
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("prompt")
    p.add_argument("--out", required=True)
    p.add_argument("--duration", type=float, default=15.0)
    p.add_argument("--ratio", default="9:16")
    p.add_argument("--require", action="append", default=[])
    s = sub.add_parser("scaffold")
    s.add_argument("plan")
    s.add_argument("--out", required=True)
    c = sub.add_parser("check")
    c.add_argument("plan")
    c.add_argument("--html")
    c.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "plan":
        plan = default_plan(a.prompt, a.duration, a.ratio, a.require)
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"plan written: {a.out} (fill concept, visual_language, shot text, motion, covers)")
        return 0
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    if a.cmd == "scaffold":
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(scaffold(plan), encoding="utf-8")
        print(f"page written: {a.out}")
        return 0
    errs = [f"plan: {e}" for e in check_plan(plan)]
    if a.html:
        errs += [f"html: {e}" for e in check_html(Path(a.html).read_text(encoding="utf-8"), plan)]
    if a.json:
        print(json.dumps({"ok": not errs, "errors": errs}, ensure_ascii=False, indent=2))
    else:
        print("\n".join(errs) if errs else "PASS")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
