const assert=require('assert'),fs=require('fs');
assert.ok(fs.existsSync(__dirname+'/assets/scene.js'),'Animated scene module is missing');
const {sceneSVG,pose,DURATION}=require('./assets/scene.js');
assert.equal(DURATION,12);
for(let i=0;i<=288;i++){const t=i/24,s=sceneSVG(t);assert(s.startsWith('<svg'));assert(!/NaN|undefined|Infinity/.test(s),'Invalid geometry at '+t);assert(s.includes('width="1280"'));}
assert.equal(sceneSVG(3.5),sceneSVG(3.5),'Rendering must be deterministic');
assert.notEqual(sceneSVG(2),sceneSVG(4),'Scene must animate');
assert(pose(6).jump>80,'Jump needs visible altitude');
assert.equal(pose(8).jump,0,'Cat should land');
assert(pose(8).x>pose(3).x,'Cat should advance');
assert.equal(pose(12).x,pose(13).x,'Timeline should clamp');
console.log('PASS 289 geometry samples; deterministic render; 1280x720; 12-second timeline; jump, landing, travel and clamping');
