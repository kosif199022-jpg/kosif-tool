#!/usr/bin/env node
/**
 * «دعاء يوم الأربعاء» text sprites: each item (or each word of a dua line) → a cropped transparent PNG.
 *
 *   node dua-wednesday/sprites.cjs <spec.json> <out-dir>
 *
 * spec: { fonts: {family: ttf-path}, items: [{id, text, font, size, cx, cy, maxW, style: white|gold|cream, words, weight, lh}] }
 * Chromium shapes the Arabic (HarfBuzz); words are separate spans laid out together, so a word sprite sits exactly
 * where it sits in the balanced line. Writes <out-dir>/manifest.json: {id: [{file, x, y, w, h}, ...]}.
 */
'use strict';
const fs = require('fs');
const path = require('path');

function resolvePlaywright() {
  for (const c of [() => require.resolve('playwright', { paths: [process.cwd()] }), () => '/opt/node-tools/node_modules/playwright', () => process.env.KOSIF_PLAYWRIGHT]) {
    try { const s = c(); if (s) { const m = require(s); if (m && m.chromium) return m; } } catch (e) { /* next */ }
  }
  throw new Error('Playwright not found (npm i playwright, or set KOSIF_PLAYWRIGHT)');
}

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const GOLD = 'linear-gradient(176deg,#fff8dc 0%,#f8dc8c 28%,#d9a441 52%,#fbe9b0 70%,#b07a22 100%)';
const PAD = 70;

function itemHtml(it) {
  const words = it.words ? it.text.split(/\s+/) : [it.text];
  const spans = words.map((w, i) => `<span class="w ${it.style}" id="w${i}">${esc(w)}</span>`).join(' ');
  return `<div id="box" style="position:absolute;left:${it.cx - it.maxW / 2}px;width:${it.maxW}px;top:0;text-align:center;direction:rtl;text-wrap:balance;
    font-family:'${it.font}';font-size:${it.size}px;font-weight:${it.weight || 400};line-height:${it.lh || 1.6}">${spans}</div>`;
}

(async () => {
  const [specPath, outDir] = process.argv.slice(2);
  if (!specPath || !outDir) { console.error('usage: node dua-wednesday/sprites.cjs <spec.json> <out-dir>'); process.exit(2); }
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const fontCss = Object.entries(spec.fonts).map(([n, p]) =>
    `@font-face{font-family:"${n}";src:url(data:font/ttf;base64,${fs.readFileSync(p).toString('base64')})}`).join('\n');
  const { chromium } = resolvePlaywright();
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const pg = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const manifest = {};
  for (const it of spec.items) {
    await pg.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}
      html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
      .w{display:inline-block;white-space:nowrap;padding:0 .04em}
      .white{color:#fffaf0}
      .cream{color:#f6e7c1}
      .gold{background-image:${GOLD};-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 3px 0 rgba(70,40,5,.85))}
      </style></head><body>${itemHtml(it)}</body></html>`);
    await pg.evaluate(() => document.fonts.ready);
    const h = await pg.evaluate(() => document.getElementById('box').getBoundingClientRect().height);
    await pg.evaluate(([y]) => { document.getElementById('box').style.top = y + 'px'; }, [it.cy - h / 2]);
    const n = it.words ? it.text.split(/\s+/).length : 1;
    const out = [];
    for (let i = 0; i < n; i++) {
      const r = await pg.evaluate((i) => {
        document.querySelectorAll('.w').forEach((e, k) => { e.style.visibility = k === i ? 'visible' : 'hidden'; });
        const b = document.getElementById('w' + i).getBoundingClientRect();
        return [b.left, b.top, b.width, b.height];
      }, i);
      const x = Math.max(0, Math.floor(r[0] - PAD)), y = Math.max(0, Math.floor(r[1] - PAD));
      const w = Math.min(1080 - x, Math.ceil(r[2] + 2 * PAD)), hh = Math.min(1920 - y, Math.ceil(r[3] + 2 * PAD));
      const file = `${it.id}_${i}.png`;
      await pg.screenshot({ path: path.join(outDir, file), omitBackground: true, clip: { x, y, width: w, height: hh } });
      out.push({ file, x, y, w, h: hh });
    }
    manifest[it.id] = out;
  }
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify(manifest, null, 1));
  await browser.close();
  console.log(`sprites: ${Object.keys(manifest).length} items → ${outDir}`);
})().catch((e) => { console.error(e); process.exit(1); });
