#!/usr/bin/env node
/**
 * wire-kitab-theme.mjs — attach the Kitab Caffe theme to every Kosif surface.
 *
 * Companion to apply-kitab-theme.mjs. That script rewrites colour literals;
 * this one wires the theme layer in: <head> links, the runtime pin in
 * suite-shell.js, the service-worker precache, and the audit shell injection
 * in the edge worker.
 *
 * Every edit is guarded, so running it twice is a no-op and running it after a
 * `git pull` only fills in what is missing.
 *
 * Usage:
 *   node scripts/wire-kitab-theme.mjs           wire it in
 *   node scripts/wire-kitab-theme.mjs --check   report only, exit 1 if unwired
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const CHECK = process.argv.includes('--check');
const CSS = '/kosif-kitab-theme.css?v=1.0.0-kitab';
const PAPER = '#FBF4E1';
const PAPER_DARK = '#171009';

const FONT_FILES = [
  'alexandria-arabic-500', 'alexandria-arabic-700', 'alexandria-arabic-900',
  'alexandria-latin-500', 'alexandria-latin-700', 'alexandria-latin-900',
  'ibm-plex-sans-arabic-arabic-400', 'ibm-plex-sans-arabic-arabic-500',
  'ibm-plex-sans-arabic-arabic-600', 'ibm-plex-sans-arabic-arabic-700',
  'ibm-plex-sans-arabic-latin-400', 'ibm-plex-sans-arabic-latin-500',
  'ibm-plex-sans-arabic-latin-600', 'ibm-plex-sans-arabic-latin-700',
  'amiri-arabic-400', 'amiri-latin-400'
].map(f => `/fonts/${f}-normal.woff2`);

/* The two faces above the fold: body text and headings. The rest stream in. */
const HEAD_BLOCK = [
  '<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2">',
  '<link rel="preload" as="font" type="font/woff2" crossorigin href="/fonts/alexandria-arabic-700-normal.woff2">',
  `<link rel="stylesheet" id="kosif-kitab-theme" href="${CSS}">`,
  '<script src="/kosif-kitab-theme.js" defer></script>'
].join('\n');

const log = [];
let pending = 0;

function edit(rel, fn) {
  const abs = path.join(ROOT, rel);
  if (!fs.existsSync(abs)) { log.push(['—', rel, 'not in this checkout']); return; }
  const src = fs.readFileSync(abs, 'utf8');
  let note = '';
  const out = fn(src, m => { note = m; });
  if (out === src) { log.push(['·', rel, note || 'already wired']); return; }
  pending++;
  if (!CHECK) fs.writeFileSync(abs, out);
  log.push([CHECK ? '!' : '✓', rel, note || 'wired']);
}

/* -- 1. page heads -------------------------------------------------- */
function wireHead(s, note) {
  if (s.includes('kosif-kitab-theme')) return s;
  note('theme block + font preloads added to <head>');
  return s.replace(/<\/head>/i, HEAD_BLOCK + '\n</head>');
}

/* Status-bar colour must follow the sheet, not the retired indigo. */
function wireThemeColour(s) {
  const light = `<meta name="theme-color" content="${PAPER}" media="(prefers-color-scheme: light)">`;
  const dark = `<meta name="theme-color" content="${PAPER_DARK}" media="(prefers-color-scheme: dark)">`;
  if (/<meta name="theme-color"[^>]*media="\(prefers-color-scheme: light\)"/.test(s)) {
    return s
      .replace(/<meta name="theme-color" content="#[0-9A-Fa-f]{6}" media="\(prefers-color-scheme: light\)">/, light)
      .replace(/<meta name="theme-color" content="#[0-9A-Fa-f]{6}" media="\(prefers-color-scheme: dark\)">/, dark);
  }
  return s.replace(/<meta name="theme-color" content="#[0-9A-Fa-f]{6}">/, light + '\n  ' + dark);
}

for (const page of ['public/index.html', 'public/hub.html',
  'public/libraries/reader.html', 'public/standards/index.html',
  'public/libraries/index.html', 'public/sales/index.html', 'frontend/index.html']) {
  edit(page, (s, note) => wireThemeColour(wireHead(s, note)));
}

/* -- 2. runtime theme authority ------------------------------------- */
edit('public/suite-shell.js', (s, note) => {
  if (s.includes('kosif-kitab-theme')) return s;
  note('theme authority handed to Kitab Caffe');
  return s
    .replace("link.href='/v38-user-polish.css?v=38.1.2-unified';", `link.href='${CSS}';`)
    .replace(/kosif-unified-theme-runtime/g, 'kosif-kitab-theme')
    .replace(/canva-navy-gold/g, 'kitab-caffe')
    .replace('pin the approved Canva navy/gold stylesheet after any',
      'pin the Kitab Caffe theme layer after any');
});

/* -- 3. offline precache -------------------------------------------- */
edit('public/sw.js', (s, note) => {
  if (s.includes('kosif-kitab-theme.css')) return s;
  note('theme + fonts precached, theme marked integrity-checked');
  const fonts = FONT_FILES.map(f => `'${f}'`).join(',');
  return s
    .replace("const CORE=['/','/hub.html',",
      `const CORE=['/','/hub.html','/kosif-kitab-theme.css','/kosif-kitab-theme.js',${fonts},`)
    .replace("const INTEGRITY=new Set(['/migrate-v35.js',",
      "const INTEGRITY=new Set(['/kosif-kitab-theme.css','/kosif-kitab-theme.js','/migrate-v35.js',");
});

/* -- 4. audit shell injection + suite metadata ----------------------- */
edit('src/suite-edge.js', (s, note) => {
  if (s.includes('kosif-kitab-theme')) return s;
  note('audit shell serves the theme last; suite metadata updated');
  return s
    .replace('const head=\'<link rel="stylesheet" href="/suite-shell.css">',
      'const head=\'<link rel="stylesheet" href="/suite-shell.css">'
      + '<script src="/kosif-kitab-theme.js"></script>')
    .replace('<script src="/v38-user-polish.js?v=38.1.0" defer></script>\';',
      '<script src="/v38-user-polish.js?v=38.1.0" defer></script>'
      + `<link rel="stylesheet" id="kosif-kitab-theme" href="${CSS}">';`)
    .replace("designAuthority:'KOSIF v38 Canva navy/gold visual system'",
      "designAuthority:'KOSIF Kitab Caffe cream/coffee/gold visual system'")
    .replace("buildId:'2026.08.19-v38.1.1-canva-visual-system'",
      "buildId:'2026.08.20-v38.1.2-kitab-caffe-visual-system'");
});

/* -- 5. keep the Phase-D palette gate meaningful --------------------- *
   The gate asserts "this layer declares an explicit palette rather than
   inheriting one". It named the indigo literals, so it moves with them. */
edit('scripts/check-product-polish-phase-d.mjs', (s, note) => {
  const old = "ok('Aghnam palette is explicit',/#6366f1/i.test(css)&&/#a855f7/i.test(css)&&/#06b6d4/i.test(css)&&/#10b981/i.test(css)&&/#f43f5e/i.test(css));";
  if (!s.includes(old)) return s;
  note('palette assertion re-pointed at the Kitab Caffe literals');
  return s.replace(old,
    "ok('Kitab Caffe palette is explicit',/#B8862B/i.test(css)&&/#D9A441/i.test(css)&&/#3F5D63/i.test(css)&&/#4E6B33/i.test(css)&&/#A8542E/i.test(css));");
});

/* -- report ---------------------------------------------------------- */
for (const [flag, rel, note] of log) console.log(`  ${flag} ${rel.padEnd(42)} ${note}`);
console.log(`\nKitab Caffe wiring: ${pending} file(s) ${CHECK ? 'still need wiring' : 'updated'}`);
if (CHECK && pending) {
  console.error('KITAB_WIRING_INCOMPLETE: run without --check.');
  process.exit(1);
}
