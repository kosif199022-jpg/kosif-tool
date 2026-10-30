#!/usr/bin/env node
/**
 * apply-kitab-theme.mjs — Kosif unified visual theme migration ("كتاب كافيه")
 *
 * Deterministic, idempotent, reversible colour migration. It rewrites every
 * hard-coded colour literal in the Kosif stylesheets (and the inline :root block
 * in public/index.html) from the legacy cold palettes — indigo/violet (v36,
 * suite, sales), navy/gold (v38), rose (canva v8), pine/viridian (audit shell) —
 * onto one warm cream + coffee + gold system derived from kitabcaffe.com.
 *
 * Design rule, same spirit as the accounting engines: the mapping table is the
 * single source of truth. No colour is invented at call sites.
 *
 * Usage:
 *   node scripts/apply-kitab-theme.mjs            apply the migration in place
 *   node scripts/apply-kitab-theme.mjs --check    report only, exit 1 if drift
 *   node scripts/apply-kitab-theme.mjs --revert   restore from .kitab-backup
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const BACKUP_DIR = path.join(ROOT, '.kitab-backup');
const MODE = process.argv.includes('--check') ? 'check'
  : process.argv.includes('--revert') ? 'revert'
    : 'apply';

/* ------------------------------------------------------------------ *
 * 1. Target palette — "كتاب كافيه" (Kitab Caffe)
 *    Anchor: #FBF4E1, the published theme-color of kitabcaffe.com.
 * ------------------------------------------------------------------ */
export const KC = {
  cream: '#FBF4E1', creamDeep: '#F4E9CE', creamBand: '#F5EBD4',
  parchment: '#FFFDF7', parchment2: '#FDF7E8',
  line: '#E8DCBE', line2: '#DFD0AC',
  espresso: '#2B1D0E', espressoDeep: '#1E1409', roast: '#3B2A14', roast2: '#4A3419',
  ink2: '#5A4327', muted: '#7A6647', muted2: '#9C8A66', faint: '#D9C9A4',
  gold: '#B8862B', goldDeep: '#966C1F', goldDeeper: '#7A5716',
  goldLight: '#D9A441', goldLift: '#E0B457',
  goldSoft: '#F9F1D9', goldLine: '#E0C88C', goldTint: '#F7EEDA',
  clay: '#A8542E', claySoft: '#F7E7DC',
  olive: '#4E6B33', oliveSoft: '#EDF0E2',
  verdigris: '#3F5D63', verdigrisSoft: '#E9EFEC',
  fig: '#6B4257', figSoft: '#F3E7EC',
  warn: '#9E6420', warnSoft: '#F9EDD9',
  /* late-night café — dark scheme */
  dBg: '#171009', dSurface: '#211710', dSurface2: '#2A1E14',
  dInk: '#F0E4CB', dMuted: '#B7A17C', dLine: '#3A2C1D', dLine2: '#4C3B27'
};

/* ------------------------------------------------------------------ *
 * 2. Hex mapping — legacy literal -> Kitab Caffe literal
 * ------------------------------------------------------------------ */
export const HEX_MAP = {
  /* neutrals / paper -------------------------------------------------- */
  '#f8fafc': KC.cream, '#f7f8fc': KC.cream, '#f4f6fa': KC.cream,
  '#fffaf9': KC.cream, '#f3f5f1': KC.cream,
  '#f1f5f9': KC.creamDeep, '#fdf5f5': KC.creamDeep, '#e8eef9': KC.creamDeep,
  '#fffefd': KC.parchment, '#fff9f8': KC.parchment2, '#fffaf0': KC.parchment2,
  '#e9f3fb': KC.creamBand, '#f4efe4': KC.creamBand,

  /* hairlines --------------------------------------------------------- */
  '#eef2f7': KC.line, '#e9eef7': KC.line, '#dce2ec': KC.line, '#e6e8ef': KC.line,
  '#dde4dc': KC.line, '#ecdfe1': KC.line, '#e2d5bd': KC.line,
  '#e2e8f0': KC.line2, '#c4cddd': KC.line2, '#c7d2c6': KC.line2, '#e1cdd2': KC.line2,

  /* ink --------------------------------------------------------------- */
  '#1e293b': KC.espresso, '#0e1b2e': KC.espresso, '#182033': KC.espresso,
  '#12211c': KC.espresso, '#49373e': KC.espresso, '#3b3023': KC.espresso,
  '#0f172a': KC.espressoDeep, '#0b1020': KC.espressoDeep, '#0c162c': KC.espressoDeep,
  '#111827': KC.espressoDeep, '#3d2c33': KC.espressoDeep,
  '#475569': KC.ink2, '#776956': KC.ink2,
  '#64748b': KC.muted, '#5a6b82': KC.muted, '#677085': KC.muted,
  '#5c6b62': KC.muted, '#847277': KC.muted,
  '#94a3b8': KC.muted2, '#a49398': KC.muted2,
  '#cbd5e1': KC.faint, '#dbeafe': KC.goldTint, '#edf2ff': KC.goldSoft,

  /* dark surfaces ----------------------------------------------------- */
  '#151b2e': KC.dSurface, '#171e2c': KC.dSurface, '#0f1420': KC.dBg,
  '#182235': KC.dSurface2, '#0b1220': KC.dBg, '#111a2c': KC.dSurface,
  '#243350': KC.dLine, '#31456b': KC.dLine2, '#273449': KC.dLine, '#2a3447': KC.dLine,
  '#aab4c9': KC.dMuted, '#93a2bc': KC.dMuted, '#dce4f2': KC.dInk,

  /* primary accent: indigo / navy / rose -> gold ---------------------- */
  '#6366f1': KC.gold, '#0a1f44': KC.espresso, '#c9a227': KC.gold,
  '#b4894a': KC.gold, '#a97e2f': KC.gold, '#f59e0b': KC.gold,
  '#c87f8d': KC.gold, '#b99a63': KC.gold,
  '#4f46e5': KC.goldDeep, '#a98a1f': KC.goldDeep, '#8c6624': KC.goldDeep,
  '#a96575': KC.goldDeep, '#0e7a5f': KC.goldDeep,
  '#4338ca': KC.goldDeeper, '#0a5f4a': KC.goldDeeper,
  '#818cf8': KC.goldLight, '#d6b274': KC.goldLift,
  '#fbf6e3': KC.goldSoft, '#f7efdc': KC.goldSoft, '#f8f0e3': KC.goldSoft,
  '#e3cf8f': KC.goldLine, '#d9c08a': KC.goldLine,
  '#eef2ff': KC.goldTint, '#f5f3ff': KC.goldTint, '#ede9fe': KC.goldTint,
  '#ddd6fe': KC.goldLine, '#c4b5fd': KC.goldLine, '#93c5fd': KC.goldLine,
  '#f0abfc': KC.goldLift, '#f5dcae': KC.goldLine, '#f4dfe3': KC.goldSoft,

  /* secondary accent: violet / purple -> lighter gold ----------------- */
  '#a855f7': KC.goldLight, '#8b5cf6': '#C99334', '#c084fc': KC.goldLift,
  '#312e81': KC.roast, '#7c3aed': '#6B4A22', '#17325f': KC.roast2,
  '#10294f': KC.roast, '#1f3352': KC.espresso, '#0e1b2f': KC.espresso,

  /* warm pop: pink / magenta -> clay ---------------------------------- */
  '#ec4899': KC.clay, '#d946ef': KC.clay, '#b487a4': KC.clay,
  '#f43f5e': KC.clay, '#a83a2e': KC.clay, '#a3281d': KC.clay,
  '#f8e9e5': KC.claySoft, '#f9e8e5': KC.claySoft, '#f1e5ee': KC.claySoft,
  '#f9eaeb': KC.goldSoft, '#e5a28a': '#C98A56', '#fbece5': '#F9EADB',

  /* success -> olive --------------------------------------------------- */
  '#10b981': KC.olive, '#2e6b4f': KC.olive, '#1e6b4f': KC.olive,
  '#0a5c46': KC.olive, '#86a477': KC.olive,
  '#e4f0e9': KC.oliveSoft, '#e3f2ea': KC.oliveSoft, '#eef4ea': KC.oliveSoft,
  '#e7efea': KC.oliveSoft, '#e2f1ea': KC.oliveSoft, '#e0f1eb': KC.oliveSoft,
  '#0f3d31': KC.espresso, '#155041': KC.roast,

  /* info -> verdigris -------------------------------------------------- */
  '#06b6d4': KC.verdigris, '#33566b': KC.verdigris, '#28527a': KC.verdigris,
  '#315f9b': KC.verdigris, '#809dbf': KC.verdigris,
  '#67e8f9': '#8FB3B8', '#ecfeff': KC.verdigrisSoft, '#e7eff4': KC.verdigrisSoft,
  '#e6eef7': KC.verdigrisSoft, '#eef4fa': KC.verdigrisSoft, '#dbe7f4': KC.verdigrisSoft,
  '#e8eef6': KC.verdigrisSoft,

  /* AI / narrative -> fig ---------------------------------------------- */
  '#5b3e96': KC.fig, '#efeaf8': KC.figSoft, '#c9b8e8': '#D9BFCB',

  /* warning ------------------------------------------------------------ */
  '#b3541e': KC.warn, '#8f5310': KC.warn, '#b45309': KC.warn,
  '#fbefe4': KC.warnSoft, '#faeeda': KC.warnSoft, '#fffbeb': KC.warnSoft
};

/* ------------------------------------------------------------------ *
 * 3. rgb()/rgba() channel mapping — same intent, triplet form
 * ------------------------------------------------------------------ */
export const RGB_MAP = {
  '99,102,241': '184,134,43',    // indigo   -> gold
  '79,70,229': '150,108,31',     // indigo-6 -> gold deep
  '67,56,202': '122,87,22',      // indigo-7 -> gold deeper
  '168,85,247': '217,164,65',    // violet   -> gold light
  '139,92,246': '201,147,52',    // purple   -> gold mid
  '236,72,153': '168,84,46',     // pink     -> clay
  '217,70,239': '168,84,46',     // fuchsia  -> clay
  '244,63,94': '168,84,46',      // rose     -> clay
  '16,185,129': '78,107,51',     // emerald  -> olive
  '6,182,212': '63,93,99',       // cyan     -> verdigris
  '49,46,129': '59,42,20',       // indigo-9 -> roast
  '10,31,68': '43,29,14',        // v38 navy -> espresso
  '15,23,42': '30,20,9',         // slate-9  -> espresso deep
  '18,33,28': '43,29,14',        // pine ink -> espresso
  '31,41,55': '43,29,14',
  '148,163,184': '156,138,102',  // slate-4  -> muted
  '110,76,87': '90,67,39',       // rose v8 shadow
  '125,84,98': '90,67,39',
  '214,178,116': '224,180,87'    // library gold
};

/* ------------------------------------------------------------------ *
 * 4. Files under migration
 * ------------------------------------------------------------------ */
const TARGETS = [
  'public/suite.css', 'public/suite-shell.css',
  'public/v36.css', 'public/v36-motion.css', 'public/v36-continuity.css',
  'public/v36-mobile-phase-b.css', 'public/v36-polish-phase-d.css',
  'public/v36-analytics-3d.css',
  'public/v38-ultimate.css', 'public/v38-user-polish.css',
  'public/kosif-canva-premium-v2.css', 'public/kosif-canva-rose-v8.css',
  'public/wealth-theme-v37.css',
  'public/libraries/libraries.css', 'public/libraries/reader.css',
  'public/sales/sales.css', 'public/sales/sales-motion-v1.css',
  'public/standards/polish-phase-d.css',
  'public/index.html', 'public/hub.html',
  'public/libraries/reader.html', 'public/standards/index.html',
  /* present in a full checkout; absent from a partial one */
  'frontend/index.html', 'public/libraries/index.html', 'public/sales/index.html'
];

/* ------------------------------------------------------------------ *
 * 5. Engine
 * ------------------------------------------------------------------ */
function assertTable() {
  const targets = new Set(Object.values(HEX_MAP).map(v => v.toLowerCase()));
  const collisions = Object.keys(HEX_MAP).filter(k => targets.has(k.toLowerCase()));
  if (collisions.length) {
    throw new Error('KITAB_THEME_NOT_IDEMPOTENT: source hex also used as target -> ' + collisions.join(', '));
  }
}

const HEX_RE = /#([0-9a-fA-F]{6})\b/g;
const RGB_RE = /(rgba?)\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*([,)])/g;

function migrate(text) {
  let hits = 0;
  let out = text.replace(HEX_RE, (m, body) => {
    const key = ('#' + body).toLowerCase();
    const to = HEX_MAP[key];
    if (!to) return m;
    hits++;
    return to;
  });
  out = out.replace(RGB_RE, (m, fn, r, g, b, tail) => {
    const to = RGB_MAP[`${+r},${+g},${+b}`];
    if (!to) return m;
    hits++;
    return `${fn}(${to}${tail}`;
  });
  return { out, hits };
}

function backupPathFor(rel) {
  return path.join(BACKUP_DIR, rel.replace(/[\\/]/g, '__'));
}

function run() {
  assertTable();

  if (MODE === 'revert') {
    if (!fs.existsSync(BACKUP_DIR)) { console.error('no .kitab-backup directory'); process.exit(1); }
    let n = 0;
    for (const rel of TARGETS) {
      const b = backupPathFor(rel);
      if (fs.existsSync(b)) { fs.copyFileSync(b, path.join(ROOT, rel)); n++; }
    }
    console.log(`reverted ${n} file(s) from .kitab-backup`);
    return;
  }

  if (MODE === 'apply') fs.mkdirSync(BACKUP_DIR, { recursive: true });

  let totalHits = 0, changed = 0, missing = 0;
  const report = [];

  for (const rel of TARGETS) {
    const abs = path.join(ROOT, rel);
    if (!fs.existsSync(abs)) { missing++; report.push(['—', 0, rel + '  (not present)']); continue; }
    const src = fs.readFileSync(abs, 'utf8');
    const { out, hits } = migrate(src);
    totalHits += hits;
    if (out !== src) {
      changed++;
      if (MODE === 'apply') {
        const b = backupPathFor(rel);
        if (!fs.existsSync(b)) fs.writeFileSync(b, src);
        fs.writeFileSync(abs, out);
      }
    }
    report.push([out !== src ? '✓' : '·', hits, rel]);
  }

  for (const [flag, hits, rel] of report) {
    console.log(`  ${flag} ${String(hits).padStart(4)}  ${rel}`);
  }
  console.log(`\nKitab Caffe theme: ${totalHits} colour literals mapped across ${changed} file(s)` +
    (missing ? `, ${missing} target(s) absent from this checkout` : ''));

  if (MODE === 'check' && changed > 0) {
    console.error('\nKITAB_THEME_DRIFT: legacy palette literals are still present. Run without --check.');
    process.exit(1);
  }
}

run();
