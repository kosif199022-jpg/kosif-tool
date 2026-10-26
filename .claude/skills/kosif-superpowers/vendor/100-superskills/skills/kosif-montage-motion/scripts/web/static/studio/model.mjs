export const LIMITS = Object.freeze({ duration: 60, clips: 24, overlays: 24, assets: 48 });
export const clamp = (n, min, max, fallback = min) => Math.min(max, Math.max(min, Number.isFinite(Number(n)) ? Number(n) : fallback));
const text = (x, max, fallback = '') => typeof x === 'string' ? x.slice(0, max) : fallback;
const color = (x, fallback) => /^#[0-9a-f]{6}$/i.test(x) ? x : fallback;
const oneOf = (x, choices, fallback) => choices.includes(x) ? x : fallback;
const list = (x, cap) => Array.isArray(x) ? x.slice(0, cap).filter(v => v && typeof v === 'object') : [];
export const assetKey = (f) => `${f.name}:${f.size}:${f.lastModified}`;
export const dimensions = (aspect) => aspect === '9:16' ? [720, 1280] : aspect === '1:1' ? [720, 720] : [1280, 720];
export function timeline(clips) { let start = 0; return clips.map(c => { const row = {...c, start, end:start+c.duration}; start=row.end; return row; }); }
export const duration = (clips) => clips.reduce((s,c) => s+c.duration,0);
export const activeClip = (clips, time) => timeline(clips).find(c => time >= c.start && time < c.end) || null;
export function animationProgress(o, time) { if(time < o.start || time >= o.start+o.duration) return 0; return Math.min(1,(time-o.start)/Math.min(.6,o.duration/3),(o.start+o.duration-time)/Math.min(.4,o.duration/3)); }
export function sanitizeProject(raw) {
 if(!raw || typeof raw !== 'object' || Array.isArray(raw)) throw new Error('Invalid project');
 if(raw.version !== 1) throw new Error('Unsupported project version');
 const used = new Set();
 const id = (value,prefix,i) => { let next=text(value,80,`${prefix}${i}`); if(!next || used.has(next)) next=`${prefix}${i}-${used.size}`; used.add(next); return next; };
 const assets=list(raw.assets,LIMITS.assets).map((a,i)=>({id:id(a.id,'asset',i),name:text(a.name,1024,'ملف'),type:oneOf(a.type,['image','video','audio'],'image'),size:clamp(a.size,0,2e9),lastModified:clamp(a.lastModified,0,9e15),duration:clamp(a.duration,0,86400)}));
 let remaining=LIMITS.duration;
 const clips=[];
 for(const [i,c] of list(raw.clips,LIMITS.clips).entries()) {
  if(remaining < .1) break;
  const type=oneOf(c.type,['image','video','demo'],'demo');
  const asset=assets.find(a=>a.id===c.assetId);
  if(type!=='demo' && (!asset || asset.type!==type)) continue;
  const trim=type==='video'?clamp(c.trim,0,Math.max(0,asset.duration-.1)):0;
  const max=Math.min(remaining,type==='video'?Math.max(.1,asset.duration-trim):60);
  const d=clamp(c.duration,.1,max,5);
  clips.push({id:id(c.id,'clip',i),type,assetId:type==='demo'?null:asset.id,trim,duration:d,volume:clamp(c.volume,0,1,1),fit:oneOf(c.fit,['contain','cover'],'cover'),preset:oneOf(c.preset,['aurora','sunset','grid'],'aurora')}); remaining-=d;
 }
 const total=duration(clips);
 const overlays=list(raw.overlays,LIMITS.overlays).map((o,i)=>{ const start=clamp(o.start,0,Math.max(0,total-.1)); return {id:id(o.id,'layer',i),type:oneOf(o.type,['text','shape'],'text'),text:text(o.text,180,'نص جديد'),shape:oneOf(o.shape,['circle','rectangle'],'circle'),x:clamp(o.x,0,100,50),y:clamp(o.y,0,100,50),size:clamp(o.size,2,60,8),color:color(o.color,'#ffffff'),opacity:clamp(o.opacity,0,1,1),start,duration:clamp(o.duration,.1,Math.max(.1,total-start),Math.min(4,total||4)),animation:oneOf(o.animation,['none','fade','rise','zoom'],'fade')}; });
 const soundAsset=assets.find(a=>a.id===raw.soundtrack?.assetId && a.type==='audio');
 return {version:1,name:text(raw.name,100,'مشروعي الجديد'),aspect:oneOf(raw.aspect,['16:9','9:16','1:1'],'16:9'),background:color(raw.background,'#07111e'),assets,clips,overlays,soundtrack:soundAsset?{assetId:soundAsset.id,trim:clamp(raw.soundtrack.trim,0,Math.max(0,soundAsset.duration-.1)),volume:clamp(raw.soundtrack.volume,0,1,.6)}:null};
}
