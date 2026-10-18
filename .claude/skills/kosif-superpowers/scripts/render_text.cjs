// Render text samples with candidate fonts through Chromium (HarfBuzz shaping) for font matching — عرض نصوص بخطوط مرشّحة للمطابقة.
// usage: node render_text.cjs spec.json outdir
// spec: {width, height, background, scale, items:[{id, text, font (path to .ttf/.otf, embedded as data URL), family (CSS fallback when no font),
//        weight, size (px), color, direction (rtl|ltr), letterSpacing, wordSpacing, features ("'liga' 1"), variation ("'wght' 600")}]}
// Each item is screenshotted to outdir/<id>.png (tight clip + 12 px padding); outdir/renders.json lists the boxes.
// Playwright is resolved from the project, /opt/node-tools or KOSIF_PLAYWRIGHT, like tools/render_html.cjs.
const fs = require('fs'); const path = require('path');
function resolvePlaywright() {
  for (const p of [path.join(process.cwd(), 'node_modules', 'playwright'), '/opt/node-tools/node_modules/playwright', process.env.KOSIF_PLAYWRIGHT]) {
    if (p && fs.existsSync(p)) return require(p);
  }
  return require('playwright');
}
(async () => {
  const [specPath, outDir] = process.argv.slice(2);
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const { chromium } = resolvePlaywright();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: spec.width || 1200, height: spec.height || 400 }, deviceScaleFactor: spec.scale || 1 });
  const results = [];
  for (const it of spec.items) {
    const face = it.font ? `@font-face{font-family:"cand";src:url("data:font/ttf;base64,${fs.readFileSync(it.font).toString('base64')}");font-weight:100 900;}` : '';
    const fam = it.font ? '"cand"' : (it.family || 'serif');
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>${face}
      html,body{margin:0;background:${spec.background || '#000'};}
      #t{position:absolute;left:40px;top:40px;white-space:nowrap;direction:${it.direction || 'rtl'};font-family:${fam};font-weight:${it.weight || 400};
         font-size:${it.size}px;color:${it.color || '#fff'};letter-spacing:${it.letterSpacing || 0}px;word-spacing:${it.wordSpacing || 0}px;
         font-feature-settings:${it.features || 'normal'};font-variation-settings:${it.variation || 'normal'};line-height:1.2;}
    </style></head><body><div id="t">${it.text}</div></body></html>`;
    await page.setContent(html);
    await page.evaluate(() => document.fonts.ready);
    const loaded = await page.evaluate(() => [...document.fonts].map(f => f.status));
    if (it.font && !loaded.includes('loaded')) console.error('font not loaded for', it.id, loaded);
    await page.waitForTimeout(50);
    const box = await page.locator('#t').boundingBox();
    const pad = 12;
    const clip = { x: Math.max(0, box.x - pad), y: Math.max(0, box.y - pad), width: box.width + 2 * pad, height: box.height + 2 * pad };
    const out = path.join(outDir, it.id + '.png');
    await page.screenshot({ path: out, clip });
    results.push({ id: it.id, png: out, width: box.width, height: box.height });
  }
  await browser.close();
  fs.writeFileSync(path.join(outDir, 'renders.json'), JSON.stringify(results, null, 1));
  console.log(results.map(r => `${r.id}: ${Math.round(r.width)}x${Math.round(r.height)}`).join('\n'));
})().catch(e => { console.error(e); process.exit(1); });
