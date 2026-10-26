"""Create a standalone offline dashboard from KOSIF Structural Twin JSON.
Visual geometry is a schematic projection of a verified *input model*, not auto inferred from video.
"""
from __future__ import annotations
import argparse,base64,json
from pathlib import Path

HTML=r'''<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KOSIF Structural Twin • Lab</title>
<style>
:root{color-scheme:dark;--bg:#081213;--glass:#0e2323;--line:#23483f;--mint:#9dffb4;--lime:#d0ff6a;--soft:#99b7aa;--ink:#eaffed;--red:#ff907a;--gold:#ffda77}
*{box-sizing:border-box}body{margin:0;font:14px/1.5 system-ui,'Arial',sans-serif;color:var(--ink);background:radial-gradient(ellipse at 45% -30%,#244841,transparent 75%),var(--bg)}.shell{max-width:1460px;margin:0 auto;padding:18px}.top{display:flex;align-items:center;gap:16px;justify-content:space-between;border:1px solid var(--line);background:#0a1b1ab8;padding:12px 18px;border-radius:16px}.mark{display:flex;align-items:center;gap:10px;font-weight:750;letter-spacing:0.05em}.dot{width:12px;height:12px;border-radius:50%;background:var(--lime);box-shadow:0 0 17px var(--lime)}.mini{font-size:10px;letter-spacing:.17em;text-transform:uppercase;color:var(--soft)}.flag{border:1px solid #4e6449;border-radius:30px;color:var(--lime);padding:4px 12px;font-size:11px}.layout{display:grid;grid-template-columns:minmax(0,1.85fr) minmax(280px,1fr);gap:16px;margin-top:16px}.panel{background:#0b1c1bcc;border:1px solid var(--line);border-radius:18px;overflow:hidden}.stage{min-height:390px;position:relative;background:radial-gradient(circle at 42% 40%,#20403b 0%,#0a1b1a 60%,#081314 100%)}.stage:after{content:'';position:absolute;inset:0;pointer-events:none;background:linear-gradient(transparent 95%,#5ec6a30b 95%) 0 0/100% 24px}.stageHead{position:absolute;top:17px;left:20px;z-index:2}.stageBottom{position:absolute;bottom:15px;left:20px;z-index:2;color:var(--soft);font-size:11px}.viz{width:100%;height:390px}#joint_layer text{fill:#c3fbd6;font-size:14px;font-weight:600}.lines{stroke-linecap:round;filter:drop-shadow(0 0 7px #60eaa33b)}.muted{color:var(--soft)}.pad{padding:22px}.statgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.stat{border:1px solid var(--line);border-radius:12px;padding:12px;background:#0b1e1d}.stat strong{font-size:22px;display:block;margin:5px 0}.hdr{letter-spacing:.1em;text-transform:uppercase;color:#a7debe;font-size:11px}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}.tabs button{font:inherit;padding:9px 12px;border-radius:9px;background:#132b27;color:var(--ink);border:1px solid #365d4e;cursor:pointer}.tabs button.active{background:#caff82;color:#122216;border-color:transparent;font-weight:750}input[type=range]{accent-color:var(--lime);width:100%}.member{display:flex;justify-content:space-between;gap:8px;border-bottom:1px solid #275044;padding:8px 0}.member:last-child{border-bottom:0}.member b{font-variant-numeric:tabular-nums}.pill{font-size:10px;border-radius:18px;padding:2px 9px;background:#304a32;color:#b6ffc7}.warn{color:var(--gold)}.bad{color:var(--red)}.legend{display:flex;justify-content:space-between;margin-top:12px;gap:5px;font-size:11px;color:var(--soft)}.legend i{width:13px;height:13px;display:inline-block;border-radius:50%;vertical-align:middle;margin-right:3px}.notice{margin-top:16px;background:#1c2420;border:1px solid #506444;border-radius:14px;padding:13px 17px;color:#d4dbb8;font-size:12px}.fade{opacity:.7}@media(max-width:850px){.layout{grid-template-columns:1fr}.shell{padding:10px}.stage,.viz{height:310px;min-height:310px}.statgrid{grid-template-columns:repeat(3,minmax(0,1fr))}.stat strong{font-size:17px}}@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style></head><body><main class="shell"><header class="top"><div class="mark"><span class="dot"></span><span>KOSIF <span style="color:var(--lime)">STRUCTURAL TWIN</span></span></div><span class="mini">SHAPE · JOINT · LOAD · BREAK · SWAP · RANK</span><span class="flag">SIMULATION / DEMO</span></header>
<section class="layout"><div><div class="panel stage"><div class="stageHead"><div class="mini">DIGITAL STRUCTURE LAB / AXIAL FORCE</div><h2 id="modelName" style="margin:6px 0 0;font-size:17px">Model</h2></div>
<svg id="scheme" class="viz" viewBox="0 0 660 400" role="img" aria-label="Illustrative pin-jointed truss stress schematic"></svg><div class="stageBottom">MATERIAL RESPONSE · 2D PIN-JOINT TRUSS · NOT CERTIFIED ENGINEERING</div></div>
<div class="statgrid" style="margin-top:12px"><div class="stat"><div class="hdr">First limit</div><strong id="limit">—</strong><span class="muted">× baseline load</span></div><div class="stat"><div class="hdr">Peak utilization</div><strong id="peak">—</strong><span class="muted">at selected load</span></div><div class="stat"><div class="hdr">Displacement</div><strong id="disp">—</strong><span class="muted">max • mm</span></div></div>
<div class="notice"><b>Analysis boundary:</b> a simplified linear-elastic 2D truss; only axial member force. A generated animation or geometry image is not proof of real dimensions, connections or failure resistance. Input material and load values must be independently confirmed before engineering use.</div></div>
<aside class="panel pad"><div class="hdr">Experiment controls</div><h2 style="font-size:21px;margin:8px 0 16px">Change one part. Re-evaluate all.</h2><div class="tabs"><button id="base" class="active" type="button">Baseline</button><button id="swap" type="button">SWAP comparison</button></div>
<div class="hdr" style="margin-top:18px">LOAD · <span id="sval">1.00×</span></div><input id="load" aria-label="Load multiplier" type="range" min="0.10" max="4.00" step="0.05" value="1"><div class="legend"><span>0.10×</span><span>2.00×</span><span>4.00×</span></div>
<div style="border-top:1px solid var(--line);margin:18px 0"></div><div class="hdr">Failure rank / weakest first</div><div id="ranks" style="margin-top:10px"></div>
<div style="border-top:1px solid var(--line);margin:18px 0"></div><div class="hdr">BREAK • conceptual sequence</div><p id="break" class="muted" style="font-size:12px"></p><div class="hdr">SWAP verdict</div><p id="verdict" class="muted" style="font-size:12px"></p>
</aside></section></main><script id="payload" type="application/octet-stream">__EMBEDDED_BASE64__</script><script>
'use strict';
const report=JSON.parse(atob(document.getElementById('payload').textContent.trim()));
const model=report.model;const baseline=report.baseline;const swap=report.swap?.after||null;
let mode='base';let scale=1;
const byId=id=>document.getElementById(id);const n2=v=>Number(v).toFixed(2);const NS='http://www.w3.org/2000/svg';
function svg(tag,attrs,parent){const e=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));parent.appendChild(e);return e}
function projected(xy){const coords=Object.values(model.nodes);const xs=coords.map(x=>x[0]),ys=coords.map(x=>x[1]);const minx=Math.min(...xs),maxx=Math.max(...xs),miny=Math.min(...ys),maxy=Math.max(...ys);let span=Math.max(maxx-minx,maxy-miny,0.1);return [90+480*((xy[0]-minx)/span),315-230*((xy[1]-miny)/span)]}
function color(u){return u>=1?'#ff907a':u>=.72?'#ffe083':u>=.35?'#b4ed88':'#8cffc0'}
function update(){
 const result=mode==='swap'&&swap?swap:baseline;const mp=new Map(result.members.map(m=>[m.id,m]));const s=byId('scheme');s.replaceChildren();
 const defs=svg('defs',{},s);const marker=svg('marker',{id:'arrow',markerWidth:8,markerHeight:8,refX:4,refY:4,orient:'auto'},defs);svg('path',{d:'M0 0 L8 4 L0 8 Z',fill:'#e9e995'},marker);
 for(let i=0;i<=8;i++){let y=85+i*27;svg('line',{x1:40,y1:y,x2:625,y2:y,stroke:'#4a7561','stroke-opacity':0.14},s)}
 model.elements.forEach(e=>{let a=projected(model.nodes[e.a]),b=projected(model.nodes[e.b]);let m=mp.get(e.id);if(!m)return;let util=m.utilization*scale;const l=svg('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:color(util),'stroke-width':11,'stroke-dasharray':util>=1?'12 9':'','stroke-linecap':'round'},s);l.classList.add('lines');l.setAttribute('aria-label',`${e.id}, ${n2(util*100)} percent utilization`);let c=[(a[0]+b[0])/2,(a[1]+b[1])/2];let t=svg('text',{x:c[0],y:c[1]-14,'text-anchor':'middle',fill:'#e3ffc8','font-size':14},s);t.textContent=e.id;});
 const joints=svg('g',{id:'joint_layer'},s);Object.entries(model.nodes).forEach(([id,xy])=>{let [x,y]=projected(xy);svg('circle',{cx:x,cy:y,r:9,fill:'#102a27',stroke:'#d6ffa9','stroke-width':3},joints);let t=svg('text',{x:x+13,y:y-11},joints);t.textContent=id;});
 model.loads.forEach(l=>{let [x,y]=projected(model.nodes[l.node]);let sign=Math.sign(l.fy_n||l.fx_n);let vertical=Math.abs(l.fy_n||0)>=Math.abs(l.fx_n||0);if(vertical)svg('line',{x1:x,y1:y-(sign<0?64:-64),x2:x,y2:y-(sign<0?14:-14),stroke:'#e9e995','stroke-width':3,'marker-end':'url(#arrow)'},s);else svg('line',{x1:x+(sign>0?-64:64),y1:y,x2:x+(sign>0?-14:14),y2:y,stroke:'#e9e995','stroke-width':3,'marker-end':'url(#arrow)'},s)});
 const lim=result.first_failure_multiplier;byId('limit').textContent=lim==null?'∞':n2(lim);byId('peak').textContent=n2(100*Math.max(0,...result.members.map(m=>m.utilization*scale)))+'%';byId('peak').className=result.members.some(m=>m.utilization*scale>=1)?'bad':'';
 let disp=Math.max(...Object.values(result.displacements_m).map(d=>Math.hypot(d.x_m,d.y_m)),0);byId('disp').textContent=n2(disp*1000*scale);
 byId('ranks').replaceChildren();result.ranked_failure_modes.forEach((m,i)=>{const el=document.createElement('div');el.className='member';const label=document.createElement('span');label.textContent=`${i+1}. ${m.id} · ${m.mode}`;const badge=document.createElement('b');badge.className=m.utilization*scale>=1?'bad':'';badge.textContent=m.failure_load_multiplier===null?'—':`${n2(m.failure_load_multiplier/scale)}× remaining`;el.append(label,badge);byId('ranks').append(el)});
 byId('break').textContent=`Scenario ${report.hypothetical_failure_path.load_scale}×: `+report.hypothetical_failure_path.steps.map(x=>x.element?`${x.element}: idealized removal`:(x.status==='unstable_after_removal'?'unstable / mechanism':x.status)).join('  →  ');
 if(report.swap){let d=report.swap.first_failure_multiplier_delta;byId('verdict').textContent=`Changed ${report.swap.element_id}: ${JSON.stringify(report.swap.changes)}. First-limit difference ${d===null?'not available':(d>=0?'+':'')+n2(d)}×. This does not assess buckling or certification.`}
 else byId('verdict').textContent='Run python structural_twin.py --sample --swap AB --area 0.0002 to enable before/after.';
 byId('sval').textContent=n2(scale)+'×';byId('base').classList.toggle('active',mode==='base');byId('swap').classList.toggle('active',mode==='swap');byId('swap').disabled=!swap;
}
byId('modelName').textContent=model.name||'Structure model';byId('base').addEventListener('click',()=>{mode='base';update()});byId('swap').addEventListener('click',()=>{mode='swap';update()});byId('load').addEventListener('input',e=>{scale=Number(e.target.value);update()});update();
</script></body></html>'''

def build(report):
    if report.get('schema')!='kosif.structural-twin.v0.1':
        raise ValueError('Unsupported structural report schema')
    encoded=base64.b64encode(json.dumps(report,ensure_ascii=False,allow_nan=False).encode('utf8')).decode('ascii')
    return HTML.replace('__EMBEDDED_BASE64__',encoded)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('report',type=Path)
    ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args()
    result=json.loads(args.report.read_text(encoding='utf8'))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(build(result),encoding='utf8')
    print(str(args.out))

if __name__=='__main__':main()
