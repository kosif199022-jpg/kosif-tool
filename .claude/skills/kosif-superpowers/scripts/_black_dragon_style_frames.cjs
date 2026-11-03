#!/usr/bin/env node
'use strict';
/*
 * Black Dragon style adapter helper: open one local HTML film in headless Chromium
 * (Playwright), seek it to fixed film times through the KOSIF renderer contract
 * (window.__kosif.seek), screenshot each frame and read a few DOM facts.
 *
 * Usage: node _black_dragon_style_frames.cjs SPEC.json
 *   SPEC = {"html": "<abs path>", "width": W, "height": H, "times": [t, ...], "out_dir": "<abs dir>"}
 * Prints one JSON object on stdout:
 *   {"errors": [...], "contract": {...}|null, "frames": [{"t", "png", "dom"}], "playwright": "<from>"}
 *
 * Every http(s) request is aborted (offline, reproducible); only file:// loads.
 * The helper never judges a frame: the Python adapter does every check. Exit 0
 * when the page could be opened and every requested frame was written, 2 otherwise.
 * Node 22, CommonJS, no npm dependencies besides Playwright resolved at runtime.
 */
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

function resolvePlaywright() {
  const candidates = [
    () => require.resolve('playwright', { paths: [process.cwd()] }),
    () => '/opt/node-tools/node_modules/playwright',
    () => process.env.KOSIF_PLAYWRIGHT,
  ];
  const tried = [];
  for (const candidate of candidates) {
    let spec;
    try { spec = candidate(); } catch (e) { tried.push(String(e.message || e)); continue; }
    if (!spec) continue;
    try {
      const mod = require(spec);
      if (mod && mod.chromium) return { playwright: mod, from: spec };
    } catch (e) { tried.push(`${spec}: ${e.message || e}`); }
  }
  throw new Error('Playwright not found: ' + tried.join(' | '));
}

const WATCHDOG_MS = 40000; // a stuck browser ends the helper (exit 2) instead of hanging the adapter

async function main() {
  const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  setTimeout(() => {
    process.stdout.write(JSON.stringify({ fatal: `watchdog: no result after ${WATCHDOG_MS} ms` }) + '\n');
    process.exit(2);
  }, WATCHDOG_MS).unref();
  const { playwright, from } = resolvePlaywright();
  const result = { errors: [], blocked_requests: [], contract: null, frames: [], playwright: from };
  fs.mkdirSync(spec.out_dir, { recursive: true });
  const browser = await playwright.chromium.launch({
    headless: true,
    timeout: 20000,
    args: ['--font-render-hinting=none', '--disable-lcd-text', '--force-color-profile=srgb', '--hide-scrollbars'],
  });
  try {
    const context = await browser.newContext({ viewport: { width: spec.width, height: spec.height }, deviceScaleFactor: 1 });
    const page = await context.newPage();
    page.on('pageerror', (e) => result.errors.push('pageerror: ' + String(e.message || e)));
    page.on('console', (m) => { if (m.type() === 'error') result.errors.push('console: ' + m.text()); });
    await page.route('**/*', (route) => {
      const url = route.request().url();
      if (url.startsWith('file:') || url.startsWith('data:')) return route.continue();
      result.blocked_requests.push(url);
      return route.abort();
    });
    await page.goto(pathToFileURL(spec.html).href, { waitUntil: 'load', timeout: 20000 });
    result.contract = await page.evaluate(async () => {
      const k = window.__kosif;
      if (!k || typeof k.seek !== 'function') return null;
      try { await Promise.race([window.__kosifReady, new Promise((r) => setTimeout(r, 3000))]); } catch (e) { /* recorded by pageerror */ }
      return { duration: k.duration, fps: k.fps };
    });
    for (let i = 0; i < spec.times.length; i++) {
      const t = spec.times[i];
      const dom = await page.evaluate(async (time) => {
        if (window.__kosif && typeof window.__kosif.seek === 'function') window.__kosif.seek(time);
        await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
        const title = document.querySelector('#title');
        const counter = document.querySelector('#counter');
        return {
          title_words: title ? [...title.children].map((s) => s.textContent) : null,
          title_opacity: title ? [...title.children].map((s) => parseFloat(getComputedStyle(s).opacity)) : null,
          counter: counter ? counter.textContent : null,
        };
      }, t);
      const png = path.join(spec.out_dir, `frame_${String(i).padStart(2, '0')}_${t.toFixed(3)}.png`);
      await page.screenshot({ path: png, type: 'png' });
      result.frames.push({ t, png, dom });
    }
  } finally {
    await browser.close();
  }
  process.stdout.write(JSON.stringify(result) + '\n');
  return result.frames.length === spec.times.length ? 0 : 2;
}

main().then((code) => process.exit(code), (err) => {
  process.stdout.write(JSON.stringify({ fatal: String((err && err.stack) || err).slice(0, 800) }) + '\n');
  process.exit(2);
});
