#!/usr/bin/env node
/* Measured word-sync audit for a seekable KOSIF page.
 * Seeks every frame exactly like tools/render_html.cjs, reads each `.w` element's
 * computed opacity, and reports the first frame where the word is visible (>= 0.05)
 * against its spoken start from window.KOSIF_WORDS.
 * usage: node sync_probe.cjs index.html [fps=30] [threshold_ms=100]
 */
const path = require('path');
const { pathToFileURL } = require('url');
let playwright;
for (const p of ['playwright', '/opt/node-tools/node_modules/playwright', process.env.KOSIF_PLAYWRIGHT]) {
  try { if (p) { playwright = require(p); break; } } catch (_) { /* try next */ }
}
(async () => {
  const [file, fpsArg, thrArg] = process.argv.slice(2);
  const fps = +(fpsArg || 30), thr = +(thrArg || 100);
  const browser = await playwright.chromium.launch({ headless: true, args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto(pathToFileURL(path.resolve(file)).href, { waitUntil: 'load' });
  await page.evaluate(() => window.__kosifReady);
  const res = await page.evaluate(async (fps) => {
    const words = window.KOSIF_WORDS, els = [...document.querySelectorAll('.w')];
    const first = new Array(els.length).fill(null);
    const n = Math.round(window.__kosif.duration * fps);
    for (let f = 0; f < n; f++) {
      await window.__kosif.seek(f / fps);
      els.forEach((el, i) => { if (first[i] === null && +getComputedStyle(el).opacity >= 0.05) first[i] = f; });
    }
    return words.map((w, i) => ({ word: w.word, start: w.start, frame: first[i], shown: first[i] === null ? null : first[i] / fps }));
  }, fps);
  await browser.close();
  let worst = 0, early = 0;
  for (const r of res) {
    const d = r.shown === null ? Infinity : (r.shown - r.start) * 1000;
    worst = Math.max(worst, Math.abs(d)); if (d < 0) early++;
    console.log(`${r.word.padStart(10)}  spoken ${r.start.toFixed(3)} s  first visible frame ${r.frame} (${r.shown?.toFixed(3)} s)  delta ${d.toFixed(0)} ms`);
  }
  const ok = worst <= thr && early === 0;
  console.log(`SYNC ${ok ? 'OK' : 'FAIL'} words=${res.length} max|delta|=${worst.toFixed(0)} ms (limit ${thr} ms, frame=${(1000 / fps).toFixed(1)} ms) early=${early}`);
  process.exit(ok ? 0 : 1);
})();
