import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const source=fs.readFileSync(path.join(here,'../assets/motion_engine.js'),'utf8');
class Svg {
  constructor(tag){this.tag=tag;this.children=[];this.attrs={};this.style={};this.textContent='';}
  appendChild(n){this.children.push(n);return n;}
  setAttribute(k,v){this.attrs[k]=String(v);}
  getTotalLength(){return this.tag==='path'?200:0;}
  getPointAtLength(n){return {x:n/2,y:n/3};}
  replaceChildren(){this.children=[];}
}
const spec={
  version:1,width:1080,height:1920,fps:30,duration:6,
  scenes:[{id:'scene',start:0,end:6,background:'#f4f0e6',
    camera:{fromZoom:1,toZoom:1.1},
    words:[{text:'أهلا',start:0.1,end:0.8}],
    elements:[{type:'actor',x:540,y:960,scale:1.5,start:0,end:2,action:'wave',
      move:{fromX:0,toX:100,start:2,end:6},
      parts:[
        {role:'head',d:'M0 -100 Q40 -120 0 -150 Z',pivot:[0,-100]},
        {role:'body',d:'M-40 -80 L40 -80 L30 80 Z',pivot:[0,0]},
        {role:'arm-left',d:'M-40 -70 L-80 20',pivot:[-40,-70]},
        {role:'arm-right',d:'M40 -70 L80 20',pivot:[40,-70]},
        {role:'leg-left',d:'M-20 70 L-25 180',pivot:[-20,70]},
        {role:'leg-right',d:'M20 70 L25 180',pivot:[20,70]}
      ]}]}]
};
function load(action='wave'){
  spec.scenes[0].elements[0].action=action;
  const nodes={scene:new Svg('svg'),art:new Svg('g'),stage:new Svg('g'),
    captions:new Svg('g'),background:new Svg('rect'),'kosif-data':new Svg('script')};
  nodes['kosif-data'].textContent=JSON.stringify(spec);
  const document={getElementById:(k)=>nodes[k],
    createElementNS:(_ns,t)=>new Svg(t),fonts:{ready:Promise.resolve()}};
  const window={};
  vm.runInNewContext(source,{window,document,Math,JSON,Number,String,Object});
  const outer=nodes.art.children[0].children[0];
  const inner=outer.children[0];
  const body=inner.children[0];
  return {window,body,nodes};
}
test('actor engine compiles and supports deterministic frame stepping',()=>{
  new vm.Script(source);
  const {window}=load();
  assert.equal(window.__kosif.seek(4).time,4);
  assert.equal(window.__kosif.seek(0).time,0);
  assert.equal(window.__kosif.duration,6);
});
test('strokes appear in sequence and drawing tip follows revealed geometry',()=>{
  const {window,body}=load();
  window.__kosif.seek(0.2);
  const first=body.children[0];
  const second=body.children[1];
  assert.ok(Number(first.style.strokeDashoffset)<200);
  assert.equal(Number(second.style.strokeDashoffset),202);
  const nib=body.children.at(-1);
  assert.equal(nib.tag,'circle');
  assert.equal(nib.style.opacity,'1');
  assert.ok(Number(nib.attrs.cx)>0);
  window.__kosif.seek(2.5);
  assert.equal(nib.style.opacity,'0');
});
test('right arm waves and correct shoulder pivot is retained',()=>{
  const {window,body}=load('wave');
  window.__kosif.seek(2.5);
  const right=body.children[3].attrs.transform;
  const left=body.children[2].attrs.transform;
  assert.match(right,/^rotate\(-\d+/);
  assert.ok(right.endsWith(' 40 -70)'));
  assert.equal(left,'rotate(0 -40 -70)');
});
test('walk and run move opposing arms and legs',()=>{
  for(const action of ['walk','run']){
    const {window,body}=load(action);
    window.__kosif.seek(2.3);
    assert.notEqual(body.children[2].attrs.transform,body.children[3].attrs.transform);
    assert.notEqual(body.children[4].attrs.transform,body.children[5].attrs.transform);
  }
});
test('point and sit produce distinct joint angles',()=>{
  const point=load('point');
  point.window.__kosif.seek(3);
  assert.equal(point.body.children[3].attrs.transform,'rotate(-65 40 -70)');
  const sit=load('sit');
  sit.window.__kosif.seek(3);
  assert.equal(sit.body.children[4].attrs.transform,'rotate(-65 -20 70)');
  assert.equal(sit.body.children[5].attrs.transform,'rotate(65 20 70)');
});
test('word captions use provided timestamps',()=>{
  const {window,nodes}=load();
  assert.equal(window.__kosif.seek(0.2).word,'أهلا');
  assert.equal(nodes.captions.children[1].textContent,'أهلا');
  assert.equal(window.__kosif.seek(1.8).word,null);
});

test('matched five-point vector morph changes actual SVG d across frames',()=>{
  const item={type:'morph',start:0,end:4,stroke:'#172824',
    from:[[10,10],[100,10],[100,100],[10,100],[5,50]],
    to:[[20,20],[70,0],[130,80],[20,90],[0,30]]};
  spec.scenes[0].elements.push(item);
  try {
    const {window,nodes}=load('idle');
    const morphOuter=nodes.art.children[0].children[1];
    const curve=morphOuter.children[0].children[0];
    window.__kosif.seek(0);
    const before=curve.attrs.d;
    window.__kosif.seek(2);
    const midway=curve.attrs.d;
    window.__kosif.seek(4);
    assert.notEqual(before,midway);
    assert.ok(midway.includes(' Z'));
    assert.equal(window.__kosif.duration,6);
    assert.equal(curve.tag,'path');
  } finally {
    spec.scenes[0].elements.pop();
  }
});
