import test from "node:test";
import assert from "node:assert/strict";
import {clamp,ease,interpolate,timeline,strokeReveal,camera,walkRig,parallax,
        seededSketchLine,timeCode,wordCueState,assertFrameContract}
 from "../resources/motion-runtime/motion_toolkit.mjs";

test("linear clamp and smooth ease have stable exact endpoints",()=>{
 assert.equal(clamp(-3),0);assert.equal(clamp(2),1);
 for(const kind of ["linear","smooth","in","out","cubic"]){
  assert.equal(ease(0,kind),0);assert.equal(ease(1,kind),1);
 }
 assert.equal(ease(.5),.5);
});
test("interpolate reproduces exact keyframe endpoints",()=>{
 assert.equal(interpolate(-10,1,3,4,8),4);
 assert.equal(interpolate(3,1,3,4,8),8);
 assert.equal(interpolate(2,1,3,4,8),6);
 assert.throws(()=>interpolate(2,2,1,3,4));
});
test("timeline handles multi-keyframes and rejects unordered input",()=>{
 const k=[{time:0,value:0},{time:1,value:10},{time:3,value:20}];
 assert.equal(timeline(1,k),10);
 assert.equal(timeline(2,k),15);
 assert.throws(()=>timeline(1,[k[1],k[0]]));
});
test("stroke reveal reaches full path and clamps",()=>{
 assert.deepEqual(strokeReveal(0,0,1,100),{strokeDasharray:100,strokeDashoffset:100});
 assert.deepEqual(strokeReveal(1,0,1,100),{strokeDasharray:100,strokeDashoffset:0});
 assert.throws(()=>strokeReveal(1,1,1,100));
});
test("camera has deterministic pan/zoom semantics",()=>{
 const c=camera(8,{end:8,zoomEnd:1.1,panX:20});
 assert(Math.abs(c.zoom-1.1)<1e-10);
 assert(Math.abs(c.x-(-54+20))<1e-8);
});
test("walkRig stationary before onset and moving after",()=>{
 assert.equal(walkRig(0).active,0);
 assert.equal(walkRig(0).leftLegDeg,0);
 assert.equal(walkRig(4).leftLegDeg,-walkRig(4).rightLegDeg);
});
test("parallax fixed response",()=>{
 assert.deepEqual(parallax(10,20,.5),{x:5,y:10});
 assert.throws(()=>parallax(10,20,2));
});
test("sketch line seeded jitter is deterministic, bounded, and endpoints exact",()=>{
 const a=seededSketchLine(0,0,100,100,{seed:55,steps:20,roughness:2});
 const b=seededSketchLine(0,0,100,100,{seed:55,steps:20,roughness:2});
 const c=seededSketchLine(0,0,100,100,{seed:56,steps:20,roughness:2});
 assert.deepEqual(a,b);assert.notDeepEqual(a,c);
 assert.deepEqual(a[0],{x:0,y:0});
 assert(Math.abs(a.at(-1).x-100)<1e-8);
 assert.throws(()=>seededSketchLine(0,0,1,1,{steps:9999}));
});
test("timecode and audio word cues do not split Arabic words",()=>{
 assert.equal(timeCode(2.5,30),"00:00:02:15");
 const w=wordCueState(.5,[{word:"قصيف",start:0,end:1},{word:"يرسم",start:1,end:2}]);
 assert.equal(w[0].word,"قصيف");assert.equal(w[0].active,true);
 assert.equal(w[1].active,false);
});
test("assertFrameContract locks portrait resolution and frame count",()=>{
 assert.deepEqual(assertFrameContract(8,30),{duration:8,fps:30,width:1080,height:1920,totalFrames:240,aspect:1080/1920});
 assert.throws(()=>assertFrameContract(0,30));
 assert.throws(()=>assertFrameContract(8,30,1079,1920));
});
