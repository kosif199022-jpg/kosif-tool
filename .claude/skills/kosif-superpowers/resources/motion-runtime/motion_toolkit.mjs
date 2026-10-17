/**
 * KOSIF Motion Toolkit — original deterministic vector/timing primitives.
 * A small, directly executable foundation (not a copy of Rough.js/GSAP/Vivus).
 * All operations return immutable values for frame-accurate seek(t) workflows.
 */
export const clamp=(v,min=0,max=1)=>Math.max(min,Math.min(max,Number(v)));
export function ease(u,kind="smooth"){
  const x=clamp(u);
  if(kind==="linear")return x;
  if(kind==="smooth")return x*x*(3-2*x);
  if(kind==="in")return x*x;
  if(kind==="out")return 1-(1-x)*(1-x);
  if(kind==="cubic")return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
  throw new Error("Unknown easing "+kind);
}
export function interpolate(t,a,b,from,to,kind="smooth"){
  if(![t,a,b,from,to].every(Number.isFinite)||b<=a)throw new Error("Invalid keyframes");
  return from+(to-from)*ease((t-a)/(b-a),kind);
}
export function timeline(time, keyframes,kind="smooth"){
  if(!Array.isArray(keyframes)||!keyframes.length||!Number.isFinite(time))
    throw new Error("Empty keyframes or invalid time");
  if(keyframes.some((p,i)=>!Number.isFinite(p.time)||!Number.isFinite(p.value)||
     (i&&p.time<=keyframes[i-1].time)))throw new Error("Keyframe times must increase");
  if(time<=keyframes[0].time)return keyframes[0].value;
  if(time>=keyframes[keyframes.length-1].time)return keyframes[keyframes.length-1].value;
  const next=keyframes.findIndex(k=>k.time>=time);
  return interpolate(time,keyframes[next-1].time,keyframes[next].time,
                     keyframes[next-1].value,keyframes[next].value,kind);
}
export function strokeReveal(t,start,end,length){
  if(!Number.isFinite(length)||length<0||end<=start)throw new Error("Invalid stroke");
  return {strokeDasharray:length,strokeDashoffset:length*(1-ease((t-start)/(end-start)))};
}
export function camera(t,{start=0,end=8,zoomStart=1,zoomEnd=1.08,
  panX=0,panY=0,centerX=540,centerY=960}={}){
  const z=interpolate(t,start,end,zoomStart,zoomEnd);
  const f=ease((t-start)/(end-start));
  return {zoom:z,x:centerX*(1-z)+panX*f,y:centerY*(1-z)+panY*f};
}
export function walkRig(t,{onset=3.3,frequency=6,stride=14,armSwing=12}={}){
  const activation=ease((t-onset)/.5);
  const w=activation===0 ? 0 : Math.sin((t-onset)*frequency)*activation;
  return {leftLegDeg:w*stride,rightLegDeg:-w*stride,
          leftArmDeg:-w*armSwing,rightArmDeg:w*armSwing,active:activation};
}
export function parallax(cameraX,cameraY,depth){
  if(!Number.isFinite(depth)||depth<0||depth>1)throw new Error("depth 0..1");
  return {x:cameraX*depth,y:cameraY*depth};
}
export function seededSketchLine(x1,y1,x2,y2,{seed=7,roughness=1.5,steps=20}={}){
  if(![x1,y1,x2,y2,seed,roughness,steps].every(Number.isFinite)||
     steps<2||steps>500||!Number.isInteger(steps)||roughness<0||roughness>30)
    throw new Error("Invalid seeded path");
  let s=(Math.trunc(seed)>>>0)||1;
  const rand=()=>{s^=s<<13;s^=s>>>17;s^=s<<5;return (s>>>0)/4294967296};
  const points=[];
  for(let i=0;i<=steps;i++){
    const u=i/steps, fade=Math.sin(Math.PI*u);
    points.push({x:x1+(x2-x1)*u+(rand()-.5)*roughness*fade,
                 y:y1+(y2-y1)*u+(rand()-.5)*roughness*fade});
  }
  return points;
}
export function timeCode(seconds,fps=30){
  if(!Number.isFinite(seconds)||seconds<0||!Number.isInteger(fps)||fps<1||fps>240)
    throw new Error("Invalid timecode");
  const frame=Math.floor(seconds*fps+1e-7);
  const h=Math.floor(frame/(fps*3600)),m=Math.floor(frame/(fps*60))%60;
  const s=Math.floor(frame/fps)%60,f=frame%fps;
  return [h,m,s,f].map(x=>String(x).padStart(2,"0")).join(":");
}
export function wordCueState(t,cues){
  if(!Array.isArray(cues))throw new Error("Expected word timing list");
  return cues.map(c=>{
    if(!Number.isFinite(c.start)||!Number.isFinite(c.end)||c.end<=c.start||typeof c.word!=="string")
      throw new Error("Invalid timed word");
    return {word:c.word,active:t>=c.start&&t<c.end,progress:ease((t-c.start)/(c.end-c.start))};
  });
}
export function assertFrameContract(duration,fps,width=1080,height=1920){
  if(!Number.isFinite(duration)||duration<=0||duration>3600||
     ![fps,width,height].every(Number.isInteger)||fps<1||fps>120||
     width<64||height<64||width%2||height%2)throw new Error("Invalid render contract");
  return {duration,fps,width,height,totalFrames:Math.ceil(duration*fps),aspect:width/height};
}
