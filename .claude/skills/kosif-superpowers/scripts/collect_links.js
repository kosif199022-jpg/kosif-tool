#!/usr/bin/env node
// collect_links.js — يجمع الروابط من صفحة أو أكتر بمتصفح Chromium حقيقي (مجاني، بلا تسجيل دخول). USIP v5.12، A42.
// node collect_links.js <url> [url...] [--filter كلمة] [--same-site] [--json] [--wait ms]
// يطبع الروابط (سطر لكل رابط) والعدد على stderr. يرجع 1 لو صفحة ما اتفتحتش أو صفر روابط.
const { chromium } = require('playwright');
const args = process.argv.slice(2);
const opt = { filter: null, same: false, json: false, wait: 0 }, urls = [];
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--filter') opt.filter = args[++i];
  else if (a === '--same-site') opt.same = true;
  else if (a === '--json') opt.json = true;
  else if (a === '--wait') opt.wait = Number(args[++i]) || 0;
  else urls.push(a);
}
if (!urls.length) { console.error('usage: node collect_links.js <url> [url...] [--filter word] [--same-site] [--json] [--wait ms]'); process.exit(2); }
(async () => {
  const browser = await chromium.launch();
  const out = [];
  let bad = 0;
  try {
    const page = await browser.newPage();
    for (const url of urls) {
      try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
        await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
        if (opt.wait) await page.waitForTimeout(opt.wait);
        const host = new URL(page.url()).hostname.replace(/^www\./, '');
        const found = await page.$$eval('a[href]', as => as.map(a => ({ href: a.href, text: (a.innerText || a.title || '').trim().slice(0, 120) })));
        const seen = new Set();
        for (const l of found) {
          if (!/^https?:/.test(l.href)) continue;
          const clean = l.href.split('#')[0];
          if (seen.has(clean)) continue;
          if (opt.same && new URL(clean).hostname.replace(/^www\./, '') !== host) continue;
          if (opt.filter && !(clean + ' ' + l.text).toLowerCase().includes(opt.filter.toLowerCase())) continue;
          seen.add(clean);
          out.push({ source: url, href: clean, text: l.text });
        }
        console.error(`${url}: ${seen.size} links`);
      } catch (e) { bad++; console.error(`${url}: FAILED ${e.message.split('\n')[0]}`); }
    }
  } finally { await browser.close(); }
  if (opt.json) console.log(JSON.stringify({ collected_at: new Date().toISOString(), count: out.length, links: out }, null, 2));
  else console.log(out.map(l => l.href).join('\n'));
  process.exit(bad || !out.length ? 1 : 0);
})();
