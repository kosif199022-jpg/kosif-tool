#!/usr/bin/env node
/* Browser smoke test for the website (manual / optional: needs Playwright + Chromium).
 *   npx http-server -p 8765 -s -c-1 . &
 *   node tests/site_smoke.cjs http://127.0.0.1:8765/
 * Exits 1 on any failed step or page error. Not part of CI (CI runners have no browser by default).
 */
'use strict';
function resolvePlaywright() {
  for (const c of ['playwright', '/opt/node-tools/node_modules/playwright', process.env.KOSIF_PLAYWRIGHT].filter(Boolean)) {
    try { return require(c); } catch (e) { /* next */ }
  }
  throw new Error('playwright not found; npm i -D playwright or set KOSIF_PLAYWRIGHT');
}
const BASE = process.argv[2] || 'http://127.0.0.1:8765/';
const errors = [];
let failed = 0;
(async () => {
  const { chromium } = resolvePlaywright();
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1380, height: 900 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const p = await ctx.newPage();
  p.on('pageerror', e => errors.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errors.push('console: ' + m.text()); });
  const step = async (name, fn) => { try { const r = await fn(); console.log('OK  ', name, r === undefined ? '' : JSON.stringify(r)); } catch (e) { failed++; console.log('FAIL', name, e.message.split('\n')[0]); } };
  const noOverflow = async (page) => { const w = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth })); if (w.sw > w.iw + 1) throw new Error('horizontal overflow ' + JSON.stringify(w)); return w; };

  await p.goto(BASE, { waitUntil: 'networkidle' });
  await step('library renders cards', async () => { await p.waitForSelector('.card', { timeout: 15000 }); return { cards: await p.locator('.card').count() }; });
  await step('default is Arabic RTL', async () => { const d = await p.evaluate(() => [document.documentElement.dir, document.documentElement.lang]); if (d[0] !== 'rtl') throw new Error(d.join()); return d; });
  await step('search finds a style by name', async () => { await p.fill('#q', 'negroni'); await p.waitForTimeout(400); const n = await p.locator('.card').count(); if (!n) throw new Error('no results'); return n; });
  await step('category chip filters', async () => { await p.fill('#q', ''); await p.waitForTimeout(300); await p.locator('.chip').nth(1).click(); await p.waitForTimeout(300); return await p.locator('.status-row span').first().innerText(); });
  await p.goto(BASE + '#/style/pm-ror-fly-9950f1', { waitUntil: 'networkidle' });
  await step('style page + copy request', async () => { await p.waitForSelector('.detail h1'); await p.locator('.detail .btn.primary').first().click(); await p.waitForFunction(() => document.querySelector('.detail .btn.primary').textContent.includes('✓'), null, { timeout: 15000 }); const txt = await p.evaluate(() => navigator.clipboard.readText()); if (!txt.includes('pm-ror-fly-9950f1') || /\{\w+\}/.test(txt)) throw new Error('bad request text'); return { chars: txt.length }; });
  await step('brief panel renders', async () => { await p.waitForTimeout(500); const t = await p.locator('.brief').innerText(); return t.slice(0, 40); });
  await p.goto(BASE + '#/generator?style=pm-ror-fly-9950f1', { waitUntil: 'networkidle' });
  await step('generator output has no placeholders', async () => { await p.waitForSelector('.output'); await p.waitForTimeout(400); const txt = await p.locator('.output').innerText(); if (/\{\w+\}/.test(txt) || !txt.includes('pm-ror-fly-9950f1')) throw new Error('bad output'); return { chars: txt.length }; });
  await p.goto(BASE + '#/playbooks', { waitUntil: 'networkidle' });
  await step('playbooks list', async () => ({ cards: await p.locator('.pb-card').count() }));
  const first = await p.locator('.pb-card a').first().getAttribute('href').catch(() => null);
  if (first) {
    await p.goto(BASE + first, { waitUntil: 'networkidle' });
    await step('playbook reader renders markdown', async () => { await p.waitForSelector('.article h2', { timeout: 10000 }); return { h2: await p.locator('.article h2').count(), toc: await p.locator('.toc a').count() }; });
  }
  await p.goto(BASE + '#/guide', { waitUntil: 'networkidle' });
  await step('guide + language toggle', async () => { await p.click('#langToggle'); await p.waitForTimeout(300); const dir = await p.evaluate(() => document.documentElement.dir); if (dir !== 'ltr') throw new Error(dir); return { h1: await p.locator('#view h1').innerText() }; });
  await step('theme toggle', async () => { await p.click('#themeToggle'); return await p.evaluate(() => document.documentElement.getAttribute('data-theme')); });
  await p.evaluate(() => { try { localStorage.clear(); } catch (e) { /* ignore */ } });
  const m = await ctx.newPage(); await m.setViewportSize({ width: 390, height: 844 });
  m.on('pageerror', e => errors.push('mobile pageerror: ' + e.message));
  for (const h of ['#/', '#/style/pm-ror-fly-9950f1', '#/generator?style=pm-ror-fly-9950f1', '#/playbooks', '#/guide']) {
    await m.goto(BASE + h, { waitUntil: 'networkidle' }); await m.waitForTimeout(400);
    await step('mobile no overflow ' + h, () => noOverflow(m));
  }
  await b.close();
  console.log(errors.length ? 'PAGE ERRORS: ' + errors.join(' | ') : 'no page errors');
  process.exit(failed || errors.length ? 1 : 0);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
