import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import {fileURLToPath} from "node:url";

const here=path.dirname(fileURLToPath(import.meta.url));
const template=fs.readFileSync(path.join(here,"../resources/motion-runtime/doodle-film.template.html"),"utf8");
const matches=[...template.matchAll(/<path[^>]*class="[^"]*reveal[^"]*"[^>]*data-start="([^"]+)"[^>]*data-end="([^"]+)"/g)];
const makeNode=(start=0,end=1)=>({
  dataset:{start:String(start),end:String(end)},
  style:{},attrs:{},children:[],
  getTotalLength(){return 100;},
  getPointAtLength(d){return {x:d,y:d*.5};},
  setAttribute(k,v){this.attrs[k]=v;},
  appendChild(n){this.children.push(n);},
});
function bootstrap(){
 const nodes=new Map([...["camera","pen","titles","diagram","character","armL","armR","legL","legR"]
   .map(x=>[x,makeNode()])]);
 const lines=matches.map(m=>makeNode(Number(m[1]),Number(m[2])));
 const document={
  fonts:{ready:Promise.resolve()},
  getElementById(id){const node=nodes.get(id);if(!node)throw Error("Missing: "+id);return node;},
  querySelectorAll(selector){assert.equal(selector,".reveal");return lines;}
 };
 const window={};
 const match=template.match(/<script>([\s\S]*?)<\/script>/);
 assert(match,"SVG template script must be inline");
 const code=match[1].replace("__DURATION__","8").replace("__FPS__","30");
 vm.runInNewContext(code,{document,window,console,Math,Number,String});
 return {window,nodes,lines};
}

test("template provides an actually callable seek function",()=>{
 const a=bootstrap();
 assert.equal(a.window.__kosif.duration,8);
 assert.equal(a.window.__kosif.fps,30);
 assert.equal(typeof a.window.__kosif.seek,"function");
 assert.equal(a.lines.length,14);
});
test("first and last frame have different actual SVG stroke geometry",()=>{
 const a=bootstrap();
 a.window.__kosif.seek(0);
 const first=a.lines.map(n=>Number(n.style.strokeDashoffset));
 a.window.__kosif.seek(7);
 const last=a.lines.map(n=>Number(n.style.strokeDashoffset));
 assert.notDeepEqual(first,last);
 assert(last.filter(z=>z===0).length>first.filter(z=>z===0).length);
});
test("character limbs and camera move at nonzero time",()=>{
 const a=bootstrap();
 a.window.__kosif.seek(0);
 const before=a.nodes.get("legL").attrs.transform;
 const camera0=a.nodes.get("camera").attrs.transform;
 a.window.__kosif.seek(4);
 const after=a.nodes.get("legL").attrs.transform;
 const camera1=a.nodes.get("camera").attrs.transform;
 assert.notEqual(before,after);assert.notEqual(camera0,camera1);
});
test("pen is attached inside camera coordinate system and tracked when paths draw",()=>{
 const a=bootstrap();
 assert(a.nodes.get("camera").children.includes(a.nodes.get("pen")));
 a.window.__kosif.seek(.5);
 assert.equal(a.nodes.get("pen").attrs.opacity,"1");
 assert.match(a.nodes.get("pen").attrs.transform,/translate\(/);
 a.window.__kosif.seek(8);
 assert.equal(a.nodes.get("pen").attrs.opacity,"0");
});
test("seeking the same timestamp is reproducible",()=>{
 const a=bootstrap();
 a.window.__kosif.seek(5.3);
 const fst=JSON.stringify({camera:a.nodes.get("camera").attrs,paths:a.lines.map(x=>x.style.strokeDashoffset)});
 a.window.__kosif.seek(5.3);
 const snd=JSON.stringify({camera:a.nodes.get("camera").attrs,paths:a.lines.map(x=>x.style.strokeDashoffset)});
 assert.equal(fst,snd);
});
