#!/usr/bin/env node
/**
 * «الدعاء» text layers → transparent 1080×1920 PNGs (one per layer) + layers.json with each layer's box.
 *
 *   node styles/dua/kit/layers.cjs <request.json> <out-dir>
 *
 * request.json: { "date": "22.08.2025", "subtitle": "ليلة جمعة مبـــاركة", "lines": ["…", "سطر أول\nسطر ثان"], "show_title": true }
 * Fonts: the composed Thuluth title SVG and KOSIF Jumuah come from fonts/kosif-jumuah (repo root);
 * Marhey and Scheherazade New Bold ship in styles/dua/kit/fonts (OFL, unmodified). Geometry and the halo
 * come from styles/dua/dua.style.json (measured from the reference). Chromium shapes Arabic (HarfBuzz).
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

function resolvePlaywright() {
  for (const c of [() => require.resolve('playwright', { paths: [process.cwd()] }), () => '/opt/node-tools/node_modules/playwright', () => process.env.KOSIF_PLAYWRIGHT]) {
    try { const s = c(); if (s) { const m = require(s); if (m && m.chromium) return m; } } catch (e) { /* next */ }
  }
  throw new Error('Playwright not found (npm i playwright, or set KOSIF_PLAYWRIGHT)');
}

const KIT = __dirname;
const STYLE = path.resolve(KIT, '..');
const REPO = path.resolve(STYLE, '..', '..');
const spec = JSON.parse(fs.readFileSync(path.join(STYLE, 'dua.style.json'), 'utf8'));
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const dataUrl = (p, mime) => `data:${mime};base64,${fs.readFileSync(p).toString('base64')}`;

function page(req) {
  const L = spec.layers;
  const titleSvg = fs.readFileSync(path.join(REPO, 'fonts/kosif-jumuah/demo/title-aljumuah.svg'), 'utf8')
    .replace(/<svg /, '<svg id="titlesvg" preserveAspectRatio="xMaxYMid meet" ');
  const fonts = `
    @font-face{font-family:"KOSIF Jumuah";font-weight:400;src:url(${dataUrl(path.join(REPO, 'fonts/kosif-jumuah/KOSIFJumuah-Regular.ttf'), 'font/ttf')})}
    @font-face{font-family:"Marhey";font-weight:300 700;src:url(${dataUrl(path.join(KIT, 'fonts/Marhey-VF.ttf'), 'font/ttf')})}
    @font-face{font-family:"Scheherazade New";font-weight:700;src:url(${dataUrl(path.join(KIT, 'fonts/ScheherazadeNew-Bold.ttf'), 'font/ttf')})}`;
  const halo = spec.shadow.css;
  const [tx0, ty0, tx1, ty1] = L.title.bbox_px;
  const [dx0, dy0, dx1, dy1] = L.date.bbox_px;
  const [gx0, gy0, gx1, gy1] = L.subtitle_gold.bbox_px;
  const day = (req.date || '22.08.2025').split('.')[0];
  const rest = (req.date || '22.08.2025').slice(day.length);
  const lines = (req.lines || []).map((t, i) => `<div class="dua L" id="dua_${i}" style="display:none">${esc(t).replace(/\n/g, '<br>')}</div>`).join('');
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fonts}
  html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
  .L{position:absolute;white-space:nowrap}
  #title{left:${tx0}px;top:${ty0}px;width:${tx1 - tx0}px;height:${ty1 - ty0}px;color:${L.title.fill};filter:drop-shadow(0 0 2px rgba(12,8,5,.95)) drop-shadow(0 0 5px rgba(12,8,5,.7))}
  #titlesvg{width:100%;height:100%;display:block;overflow:visible}
  #titlesvg path{stroke:currentColor;stroke-width:6;stroke-linejoin:round;stroke-linecap:round;fill:currentColor}
  #date{right:${1080 - dx1}px;top:${dy0}px;font-family:"KOSIF Jumuah";font-weight:400;color:${L.date.fill};direction:ltr;text-shadow:${halo};line-height:1}
  #gold{top:${gy0}px;left:0;width:1080px;text-align:center;font-family:"Marhey";font-weight:700;color:${L.subtitle_gold.fill};direction:rtl;text-shadow:${halo};line-height:1;word-spacing:${L.subtitle_gold.word_spacing_em}em}
  .dua{left:0;width:1080px;text-align:center;font-family:"Scheherazade New";font-weight:700;color:${L.dua.fill};direction:rtl;text-shadow:${halo};line-height:1.25;font-size:${L.dua.size_px}px}
  </style></head><body>
  <div class="L" id="title">${titleSvg}</div>
  <div class="L" id="date"><span id="day">${esc(day)}</span><span id="rest">${esc(rest)}</span></div>
  <div class="L" id="gold">${esc(req.subtitle || 'ليلة جمعة مبـــاركة')}</div>
  ${lines}
  <script>
  function fitWidth(el, target, start){ let s=start; el.style.fontSize=s+'px'; for(let k=0;k<8;k++){ const w=el.getBoundingClientRect().width; s=s*target/w; el.style.fontSize=s+'px'; } return s; }
  window.__layout = async () => {
    await document.fonts.ready;
    const date=document.getElementById('date'); date.style.display='inline-block';
    fitWidth(date, ${dx1 - dx0}, 150);
    const gold=document.getElementById('gold'); const inner=document.createElement('span'); inner.textContent=gold.textContent; gold.textContent=''; gold.appendChild(inner);
    const gs=fitWidth(inner, ${gx1 - gx0}, 100); gold.style.fontSize=gs+'px'; gold.style.top=(${(gy0 + gy1) / 2} - inner.getBoundingClientRect().height/2)+'px';
    for (const d of document.querySelectorAll('.dua')) {
      d.style.display='block'; const sp=document.createElement('span'); sp.innerHTML=d.innerHTML; d.innerHTML=''; d.appendChild(sp);
      let fs=${L.dua.size_px}; d.style.fontSize=fs+'px'; const w=sp.getBoundingClientRect().width; if (w>${L.dua.max_width_px}) { fs=fs*${L.dua.max_width_px}/w; d.style.fontSize=fs+'px'; }
      const h=d.getBoundingClientRect().height; const two=d.querySelector('br'); d.style.top=((two?${L.dua.two_line_y_center}:${L.dua.single_line_y_center})-h/2)+'px'; d.style.display='none';
    }
    const box=(el)=>{const r=el.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)];};
    return { title: box(document.getElementById('title')), day: box(document.getElementById('day')), rest: box(document.getElementById('rest')), gold: box(gold.firstChild) };
  };
  window.__only = (id) => {
    const ids=['title','date','gold'];
    for (const i of ids) document.getElementById(i).style.visibility = (id===i || (id.startsWith('date') && i==='date')) ? 'visible':'hidden';
    document.getElementById('day').style.visibility = (id==='date_day') ? 'visible':'hidden';
    document.getElementById('rest').style.visibility = (id==='date_rest') ? 'visible':'hidden';
    for (const d of document.querySelectorAll('.dua')) d.style.display = (d.id===id) ? 'block':'none';
  };
  </script></body></html>`;
}

(async () => {
  const [reqPath, outDir] = process.argv.slice(2);
  if (!reqPath || !outDir) { console.error('usage: node layers.cjs <request.json> <out-dir>'); process.exit(2); }
  const req = JSON.parse(fs.readFileSync(reqPath, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const html = path.join(outDir, '_layers.html'); fs.writeFileSync(html, page(req));
  const { chromium } = resolvePlaywright();
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const pg = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await pg.goto(pathToFileURL(html).href);
  const boxes = await pg.evaluate(() => window.__layout());
  const ids = ['title', 'date_day', 'date_rest', 'gold'].concat((req.lines || []).map((_, i) => `dua_${i}`));
  if (req.show_title === false) ids.shift();
  const out = { size: [1080, 1920], boxes, layers: {} };
  for (const id of ids) {
    await pg.evaluate((i) => window.__only(i), id);
    const file = path.join(outDir, `${id}.png`);
    await pg.screenshot({ path: file, omitBackground: true });
    out.layers[id] = path.basename(file);
  }
  fs.writeFileSync(path.join(outDir, 'layers.json'), JSON.stringify(out, null, 1));
  await browser.close();
  console.log(`layers → ${outDir} (${ids.length} PNG) boxes ${JSON.stringify(boxes)}`);
})().catch((e) => { console.error(e); process.exit(1); });
