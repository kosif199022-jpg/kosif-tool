#!/usr/bin/env node
// shots.js <url> <outdir> <w>x<h> <shot> [<shot> ...]
//   shot = name=<y>            absolute scrollY
//        | name=#id:<frac>     inside element #id: scrollY = top + frac*(height - innerHeight)
// Scrolls there in small real steps (so lerped scrubs and observers settle like a visitor), then shoots.
// Prints console errors, whether window.__ready fired, and MotionEngine.jank() (p95/max frame time).
// Add ?motion=on|off|xray to the url to shoot each mode of the motion switch.
// Two shots of the same spot (a=0 b=0) are taken about 2 s apart: if they are identical, nothing moves.
// KOSIF v5.10: the browser always closes (even on error), exit 1 on console errors or a missing
// selector, and the "moves?" line compares same-spot shots byte for byte.
const fs = require('fs');
const path = require('path');
const { puppeteer, chromePath } = require('./_browser.js');
const [, , url, outdir, size, ...shots] = process.argv;
if (!url || !outdir || !/^\d+x\d+$/.test(size || '') || !shots.length) {
  console.error('usage: node shots.js <url> <outdir> <w>x<h> name=<y>|name=#id:<frac> ...'); process.exit(1);
}
const [W, H] = size.split('x').map(Number);
(async () => {
  fs.mkdirSync(outdir, { recursive: true });
  const args = ['--hide-scrollbars', '--autoplay-policy=no-user-gesture-required'];
  if (process.platform === 'linux' && process.getuid && process.getuid() === 0) args.push('--no-sandbox');
  const browser = await puppeteer.launch({ executablePath: chromePath(), headless: 'new', args });
  const errs = [];
  const bySpot = {};
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
    // HTTP errors are reported once with their URL (below); a missing favicon is not a page error.
    page.on('console', m => { if (m.type() === 'error' && !/^Failed to load resource/.test(m.text())) errs.push(m.text()); });
    page.on('response', r => { if (r.status() >= 400 && !/\/favicon\.ico$/.test(r.url())) errs.push(`http ${r.status()}: ${r.url()}`); });
    page.on('pageerror', e => errs.push('pageerror: ' + e.message));
    page.on('requestfailed', r => errs.push('reqfail: ' + r.url()));
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
    await page.waitForFunction('window.__ready === true', { timeout: 30000 }).catch(() => errs.push('__ready never true'));
    await new Promise(r => setTimeout(r, 1500));
    const hscroll = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
    if (hscroll) errs.push(`horizontal scroll at ${W}px wide`);
    for (const s of shots) {
      const eq = s.indexOf('=');
      const name = s.slice(0, eq), spec = s.slice(eq + 1);
      const y = await page.evaluate(sp => {
        if (sp.startsWith('#')) {
          const [sel, f] = sp.split(':'); const el = document.querySelector(sel);
          if (!el) return null;
          const r = el.getBoundingClientRect(); const top = r.top + scrollY;
          return Math.round(top + (+f || 0) * Math.max(0, r.height - innerHeight));
        }
        return +sp;
      }, spec);
      if (y === null || Number.isNaN(y)) { errs.push(`shot ${name}: selector not found (${spec})`); continue; }
      await page.evaluate(async ty => { const y0 = scrollY, n = 24; for (let i = 1; i <= n; i++) { scrollTo(0, y0 + (ty - y0) * i / n); await new Promise(r => requestAnimationFrame(r)); } }, y);
      await new Promise(r => setTimeout(r, 1800));
      const file = path.join(outdir, name + '.jpg');
      await page.screenshot({ path: file, type: 'jpeg', quality: 70 });
      console.log('shot', name, 'y=' + y);
      (bySpot[y] = bySpot[y] || []).push(file);
    }
    const jank = await page.evaluate(() => window.MotionEngine ? window.MotionEngine.jank() : null);
    console.log('jank', JSON.stringify(jank));
    for (const [y, files] of Object.entries(bySpot)) {
      if (files.length < 2) continue;
      const same = files.slice(1).every(f => fs.readFileSync(f).equals(fs.readFileSync(files[0])));
      console.log(`moves? y=${y}: ${same ? 'NO (identical shots)' : 'yes'}`);
      if (same) errs.push(`nothing moved at y=${y}`);
    }
  } catch (e) {
    errs.push('fatal: ' + e.message);
  } finally {
    await browser.close();
  }
  console.log(errs.length ? 'ERRORS:\n' + [...new Set(errs)].join('\n') : 'no console errors');
  process.exit(errs.length ? 1 : 0);
})();
