// Stateful JS motion engine test using a minimal SVG DOM fixture.
// This executes the real source, not just a text search. No third-party modules.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const script=fs.readFileSync(path.join(here,'../assets/motion_engine.js'),'utf8');

class Node {
  constructor(tag){this.tag=tag;this.attrs={};this.style={};this.children=[];this.textContent='';}
  setAttribute(name,value){this.attrs[name]=String(value);}
  appendChild(node){this.children.push(node);return node;}
  replaceChildren(){this.children=[];}
  getTotalLength(){return this.tag==='path'||this.tag==='circle'?120:0;}
}
const data={
  version:1,width:1080,height:1920,fps:30,duration:4,
  scenes:[{
    id:'first',start:0,end:4,background:'#f4f0e6',
    camera:{fromZoom:1,toZoom:1.2,start:0,end:4},
    words:[{text:'مرحبا',start:0,end:1},{text:'بالعالم',start:1,end:4}],
    elements:[
      {type:'path',d:'M100 500 L980 500',start:0,end:2,move:{fromX:0,toX:100,start:2,end:4}},
      {type:'character',x:540,y:1000,start:0,end:1,move:{fromX:0,toX:100,start:1,end:4}}
    ]
  }]
};
function load(){
  const nodes={scene:new Node('svg'),background:new Node('rect'),art:new Node('g'),
    stage:new Node('g'),captions:new Node('g'),'kosif-data':new Node('script')};
  nodes['kosif-data'].textContent=JSON.stringify(data);
  const document={getElementById:(id)=>nodes[id],createElementNS:(_ns,tag)=>new Node(tag),
    fonts:{ready:Promise.resolve()}};
  const window={};
  vm.runInNewContext(script,{document,window,Math,JSON,Number,String,Object});
  return {nodes,window};
}
test('real runtime exposes frame-seek and updates SVG strokes and caption content',()=>{
  const {nodes,window}=load();
  assert.equal(window.__kosif.duration,4);
  assert.equal(window.__kosif.seek(0).word,'مرحبا');
  const layer=nodes.art.children[0];
  const line=layer.children[0].children[0].children[0];
  const offset0=Number(line.style.strokeDashoffset);
  assert.equal(window.__kosif.seek(1.8).word,'بالعالم');
  const offset1=Number(line.style.strokeDashoffset);
  assert.ok(offset1<offset0);
  assert.ok(nodes.captions.children.some(c=>c.textContent==='بالعالم'));
  assert.equal(nodes.captions.children.length,2);
});
test('camera transforms and character arms/legs change at different frames',()=>{
  const {nodes,window}=load();
  window.__kosif.seek(1);
  const before=nodes.stage.attrs.transform;
  const layer=nodes.art.children[0];
  const puppet=layer.children[1].children[0].children[0].children;
  const armBefore=puppet[2].attrs.transform;
  window.__kosif.seek(1.43);
  const after=nodes.stage.attrs.transform;
  assert.notEqual(after,before);
  assert.notEqual(puppet[2].attrs.transform,armBefore);
  assert.equal(parseFloat(puppet[4].attrs.transform.slice(7)),
    parseFloat(puppet[3].attrs.transform.slice(7)));
  assert.ok(puppet[4].attrs.transform.endsWith(' 0 94)'));
  assert.ok(puppet[3].attrs.transform.endsWith(' 0 8)'));
});
test('time clamping, blank captions outside intervals and determinism',()=>{
  const {nodes,window}=load();
  assert.equal(window.__kosif.seek(-4).time,0);
  const state1=window.__kosif.seek(3);
  const transform=nodes.stage.attrs.transform;
  const state2=window.__kosif.seek(3);
  assert.deepEqual(JSON.parse(JSON.stringify(state1)),JSON.parse(JSON.stringify(state2)));
  assert.equal(transform,nodes.stage.attrs.transform);
  assert.equal(window.__kosif.seek(99).time,4);
});
