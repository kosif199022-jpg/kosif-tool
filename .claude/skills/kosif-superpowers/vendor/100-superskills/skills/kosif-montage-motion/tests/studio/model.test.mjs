import test from 'node:test';
import assert from 'node:assert/strict';
import { sanitizeProject, timeline, duration, activeClip, animationProgress, dimensions, assetKey } from '../../scripts/web/static/studio/model.mjs';
const project = (clips = []) => ({version:1, name:'تجربة', aspect:'16:9', clips, overlays:[], assets:[]});
test('normalizes a valid project without retaining executable or remote properties', () => {
 const p=sanitizeProject({...project([{id:'c',type:'demo',duration:5}]),url:'https://bad.test',onload:'evil()',name:'<script>plain text</script>'});
 assert.equal(p.name,'<script>plain text</script>'); assert.equal(p.clips[0].duration,5); assert.equal(p.url,undefined); assert.equal(p.onload,undefined); assert.equal(p.version,1);
});
test('builds a consecutive sequence and resolves exact clip boundaries', () => {
 const clips=[{id:'a',duration:2,trim:3},{id:'b',duration:4,trim:1}];
 assert.deepEqual(timeline(clips).map(c=>[c.start,c.end]),[[0,2],[2,6]]);
 assert.equal(activeClip(clips,1.5).id,'a'); assert.equal(activeClip(clips,2).id,'b'); assert.equal(activeClip(clips,6),null); assert.equal(activeClip(clips,-1),null); assert.equal(duration(clips),6);
});
test('caps full project at 60 seconds, preserves order, ignores unusable asset references', () => {
 const p=sanitizeProject(project([{id:'a',type:'demo',duration:40},{id:'b',type:'demo',duration:40},{id:'c',type:'demo',duration:4},{id:'d',type:'video',assetId:'missing',duration:5}]));
 assert.equal(duration(p.clips),60); assert.deepEqual(p.clips.map(c=>c.duration),[40,20]);
});
test('caps source trim and duration against known media metadata', () => {
 const p=sanitizeProject({...project([{id:'c',type:'video',assetId:'a',trim:9,duration:9,volume:7}]),assets:[{id:'a',type:'video',name:'a.mp4',duration:10,size:30,lastModified:1,url:'javascript:bad'}]});
 assert.equal(p.clips[0].trim,9); assert.equal(p.clips[0].duration,1); assert.equal(p.clips[0].volume,1); assert.equal(p.assets[0].url,undefined);
});
test('sanitizes invalid numbers, enum values, color and overlay bounds', () => {
 const p=sanitizeProject({...project([{id:'a',type:'demo',duration:8}]),aspect:'evil',background:'url(evil)',overlays:[{id:'t',type:'text',text:'Hello',x:200,y:-50,size:NaN,start:2,duration:20,color:'red; evil',animation:'spin-eval'}]});
 assert.equal(p.aspect,'16:9'); assert.equal(p.background,'#07111e'); assert.equal(p.overlays[0].x,100); assert.equal(p.overlays[0].y,0); assert.equal(p.overlays[0].duration,6); assert.equal(p.overlays[0].animation,'fade'); assert.equal(p.overlays[0].color,'#ffffff'); assert.equal(Number.isFinite(p.overlays[0].size),true);
});
test('rejects foreign format and caps array sizes', () => {
 assert.throws(()=>sanitizeProject({version:33}),/version/); assert.throws(()=>sanitizeProject(null));
 const p=sanitizeProject(project(Array.from({length:100},(_,i)=>({id:`c${i}`,type:'demo',duration:1})))); assert.equal(p.clips.length,24);
});
test('animation values are bounded and absent outside overlay window', () => {
 const o={start:2,duration:4}; assert.equal(animationProgress(o,1),0); assert.equal(animationProgress(o,2),0); assert.equal(animationProgress(o,3),1); assert.equal(animationProgress(o,6),0);
});
test('resolves deterministic 720p dimensions and file identity', () => {
 assert.deepEqual(dimensions('16:9'),[1280,720]); assert.deepEqual(dimensions('9:16'),[720,1280]); assert.deepEqual(dimensions('1:1'),[720,720]); assert.equal(assetKey({name:'a.mp4',size:2,lastModified:3}),'a.mp4:2:3');
});
test('preserves long filenames so saved metadata can re-link the original file',()=>{const name='x'.repeat(200)+'.mp4';const p=sanitizeProject({...project(),assets:[{id:'long',name,type:'video',size:2,lastModified:3,duration:5}]});assert.equal(assetKey(p.assets[0]),assetKey({name,size:2,lastModified:3}));});
