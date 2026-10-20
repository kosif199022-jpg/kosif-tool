// Fill fonts + data into overlay_src.html → overlay.html; render frames (or stills) as transparent PNGs.
const {chromium}=require('playwright');const fs=require('fs');
const f=(n,p)=>`@font-face{font-family:"${n}";font-weight:700;src:url(data:font/ttf;base64,${fs.readFileSync(p).toString('base64')})}`;
const fonts=f('Jumuah','fonts/KOSIFJumuah-Bold.ttf')+f('Sch','fonts/ScheherazadeNew-Bold.ttf')+`@font-face{font-family:"Bodoni";font-weight:400 900;src:url(data:font/ttf;base64,${fs.readFileSync('fonts/BodoniModa.ttf').toString('base64')})}`;
const data=JSON.parse(fs.readFileSync('text/captions.json','utf8'));
const html=fs.readFileSync('text/overlay_src.html','utf8').replace('/*FONTS*/',fonts).replace('/*DATA*/',JSON.stringify(data));
fs.writeFileSync('text/overlay.html',html);
(async()=>{const mode=process.argv[2]||'stills';const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.setContent(html);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 if(mode==='stills'){for(const t of process.argv.slice(3).map(Number)){await p.evaluate(t=>seek(t),t);await p.screenshot({path:`text/still_${t}.png`,omitBackground:true});}}
 else{const out='build/ov';fs.mkdirSync(out,{recursive:true});const n=Math.round(data.end*60);const a=+(process.argv[3]||0),z=+(process.argv[4]||n);
  for(let i=a;i<z;i++){await p.evaluate(t=>seek(t),i/60);await p.screenshot({path:`${out}/${String(i).padStart(5,'0')}.png`,omitBackground:true});}}
 await b.close();})();
