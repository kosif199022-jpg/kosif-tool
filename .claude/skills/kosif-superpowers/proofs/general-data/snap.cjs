#!/usr/bin/env node
'use strict';
// Screenshot (and print to PDF) a local HTML page with Playwright's bundled headless Chromium.
// Usage: node snap.cjs <page.html> <out.png> [width=390] [height=844] [out.pdf]
// Playwright is resolved from the global install (/opt/node-tools in Claude Code cloud) or NODE_PATH.
const path = require('path');
const { pathToFileURL } = require('url');
let pw;
try { pw = require('playwright'); } catch { pw = require('/opt/node-tools/node_modules/playwright'); }
(async () => {
  const [inp, out, w = '390', h = '844', pdf] = process.argv.slice(2);
  const t0 = Date.now();
  const browser = await pw.chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.resolve(inp)).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  await page.screenshot({ path: out, fullPage: true });
  if (pdf) await page.pdf({ path: pdf, format: 'A4', printBackground: true });
  await browser.close();
  console.log(JSON.stringify({ out, pdf: pdf || null, viewport: [+w, +h], horizontal_overflow: overflow, ms: Date.now() - t0 }));
})().catch((e) => { console.error(e); process.exit(2); });
