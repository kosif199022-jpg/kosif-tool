const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const F=['Amiri-Bold','ArefRuqaa-Bold','ArefRuqaaInk-Bold','Ruwudu-Bold','ScheherazadeNew-Bold','KOSIFJumuah-Bold'];
const ff=F.map(f=>`@font-face{font-family:"${f}";src:url(data:font/ttf;base64,${fs.readFileSync('fonts/'+f+'.ttf').toString('base64')})}`).join('');
const rows=F.map(f=>`<div class=r><span class=lab>${f}</span><span style="font-family:'${f}';font-size:90px">الإِثْنَيْن</span><span style="font-family:'${f}';font-size:60px">ورزقاً مباركاً لا يعد</span><span style="font-family:'${f}';font-size:44px">جُمَادَى الأُولَى</span></div>`).join('');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1300}});
await p.setContent(`<html><style>${ff} body{background:#3a2a20;color:#fff;margin:10px} .r{display:flex;gap:40px;align-items:center;direction:rtl;height:200px;border-bottom:1px solid #555} .lab{font:16px sans-serif;width:150px;direction:ltr}</style><body>${rows}</body></html>`);
await p.waitForTimeout(500);await p.screenshot({path:'text/fontcmp.png'});await b.close();})();
