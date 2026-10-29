// tools/render_html.cjs --stills: time parsing, the capture plan, usage errors, the grid layout and its
// labels. The argument tests stop before Chromium; the grid test needs only ffmpeg (synthetic frames) and
// skips without it; the last test runs the real CLI (--offline, no network) and skips unless Playwright
// and its Chromium are installed.
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPT = join(ROOT, 'tools', 'render_html.cjs');
const SKILL_COPY = join(ROOT, '.claude', 'skills', 'kosif-superpowers', 'resources', 'motion-runtime', 'render_html.cjs');
const PAGE = join(ROOT, 'starters', 'html-canvas', 'index.html');
const require = createRequire(import.meta.url);
const R = require(SCRIPT);

const MISSING = join(ROOT, 'no-such-dir', 'missing.html');
const run = (...args) => spawnSync(process.execPath, [SCRIPT, ...args], { cwd: ROOT, encoding: 'utf8' });

function workDir(t) {
  const dir = fs.mkdtempSync(join(os.tmpdir(), 'kosif-stills-test-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}

test('--stills times: seconds, a trailing s or m:ss, read to the millisecond, sorted and de-duplicated', () => {
  assert.deepEqual(R.parseStillTimes('0,1.5,3'), [0, 1.5, 3]);
  assert.deepEqual(R.parseStillTimes(' 3 , 0.5s ,1:04, 1:04.25 ,.25, 2.'), [0.25, 0.5, 2, 3, 64, 64.25]);
  assert.deepEqual(R.parseStillTimes('2,1,2,1.0004'), [1, 2], 'duplicates (after rounding to the ms) collapse');
  assert.deepEqual(R.parseStillTimes('1.23456'), [1.235]);
  assert.deepEqual(R.parseStillTimes('0:00,10:59.5'), [0, 659.5]);
  assert.deepEqual(R.parseStillTimes('1,,2,'), [1, 2], 'empty items are skipped');
  for (const bad of ['-1', 'abc', '1e3', '1:5', '1:60', '1:2:03', 'NaN', '2ms', ' ', ',']) {
    assert.throws(() => R.parseStillTimes(bad), (e) => e instanceof R.UsageError && /--stills/.test(e.message), bad);
  }
  assert.throws(() => R.parseStillTimes(true), /--stills needs/);
  const many = Array.from({ length: R.MAX_STILLS + 1 }, (_, i) => i).join(',');
  assert.throws(() => R.parseStillTimes(many), new RegExp(`at most ${R.MAX_STILLS}`));
  assert.equal(R.parseStillTimes(Array.from({ length: R.MAX_STILLS }, (_, i) => i).join(',')).length, R.MAX_STILLS);
});

test('still file names and the capture plan (seek: exact time; virtual: the nearest frame)', () => {
  assert.equal(R.stillName(0), 'still_0.000.png');
  assert.equal(R.stillName(1.5), 'still_1.500.png');
  assert.equal(R.stillName(64.125), 'still_64.125.png');
  const seek = R.planStills([0.51, 2], { fps: 30, driver: 'seek', dir: '/s' });
  assert.deepEqual(seek[0], { t: 0.51, t_actual: 0.51, frame: 15, file: join('/s', 'still_0.510.png'), label: '0.510s' });
  const virt = R.planStills([0.51, 2], { fps: 30, driver: 'virtual', dir: '/s' });
  assert.deepEqual(virt[0], { t: 0.51, t_actual: 0.5, frame: 15, file: join('/s', 'still_0.510.png'), label: '0.500s #15' });
  assert.equal(virt[1].label, '2.000s #60');
  assert.equal(R.planStills([1 / 3], { fps: 24, driver: 'virtual', dir: '/s' })[0].t_actual, 0.333);
});

test('CLI: --stills usage errors stop before anything renders', () => {
  let r = run('--in', MISSING, '--out', 'x.mp4', '--stills');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--stills needs a value/);
  r = run('--in', MISSING, '--out', 'x.mp4', '--stills', '1,abc');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--stills: "abc" is not a film time/);
  r = run('--in', MISSING, '--out', 'x.mp4', '--stills-dir', 'shots');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--stills-dir needs --stills/);
  r = run('--in', MISSING, '--out', 'x.mp4', '--stills', '1', '--preview');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--stills and --preview are separate modes/);
  r = run('--in', MISSING, '--stills', '1');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--out <out\.mp4> is required \(or give --stills-dir <dir>\)/);
  r = run('--in', MISSING, '--out', 'x.mp4', '--report');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--report needs a value/);
  // valid stills command lines get past parsing (they stop at the missing --in file)
  for (const args of [['--stills', '0,1:02', '--stills-dir', 'shots'], ['--out', 'x.mp4', '--stills', '2.5s', '--report', 'r.json']]) {
    r = run('--in', MISSING, ...args);
    assert.equal(r.status, 1, args.join(' '));
    assert.match(r.stderr, /--in file not found/, args.join(' '));
  }
  assert.deepEqual(R.parseArgs(['--stills', '1,2', '--stills-dir', 'd', '--report', 'r.json']),
    { _: [], unknown: [], stills: '1,2', 'stills-dir': 'd', report: 'r.json' });
});

test('--help documents --stills, --stills-dir, --report and audio_md5', () => {
  const r = run('--help');
  assert.equal(r.status, 0);
  for (const re of [/--stills <times>/, /--stills-dir <dir>/, /--report <file>/, /still_<t>\.png/, /stills_grid\.png/,
    /audio_md5=match \| differs \(src N packets, out M packets\)/, /audio_md5=reencoded/]) {
    assert.match(r.stdout, re);
  }
});

test('grid layout: one row up to 4 tiles, then 4, 6 or 8 columns', () => {
  const shape = (n) => { const g = R.gridLayout(n); return `${g.cols}x${g.rows}`; };
  assert.deepEqual([1, 2, 4, 5, 8, 9, 12, 24, 25, 64].map(shape), ['1x1', '2x1', '4x1', '4x2', '4x2', '6x2', '6x2', '6x4', '8x4', '8x8']);
  assert.deepEqual(R.gridLayout(0), { cols: 0, rows: 0 });
});

test('built-in bitmap labels: one drawbox per run of lit pixels on a dark box, every label character known', () => {
  for (const ch of '0123456789.s# ') {
    const g = R.BITMAP_FONT[ch];
    assert.ok(g && g.length === 5 && g.every((row) => /^[01]+$/.test(row) && row.length === g[0].length), JSON.stringify(ch));
  }
  const one = R.bitmapLabelFilters('1', { x: 10, y: 20, px: 2 });
  assert.equal(one[0], 'drawbox=x=6:y=16:w=14:h=18:color=black@0.6:t=fill'); // 3 columns x 2 px + 2 x 4 px padding
  // '1' = 010 / 110 / 010 / 010 / 111 -> five rows, the second and last a single 2- or 3-pixel run
  assert.deepEqual(one.slice(1), [
    'drawbox=x=12:y=20:w=2:h=2:color=white:t=fill',
    'drawbox=x=10:y=22:w=4:h=2:color=white:t=fill',
    'drawbox=x=12:y=24:w=2:h=2:color=white:t=fill',
    'drawbox=x=12:y=26:w=2:h=2:color=white:t=fill',
    'drawbox=x=10:y=28:w=6:h=2:color=white:t=fill',
  ]);
  const label = R.bitmapLabelFilters('0.5s #15', { x: 0, y: 0, px: 1 });
  assert.ok(label.every((f) => /^drawbox=x=-?\d+:y=-?\d+:w=\d+:h=\d+:color=(white|black@0\.6):t=fill$/.test(f)));
  // advance = glyph width + 1: '#' is five pixels wide, so the '1' after it starts at column 6 and its top pixel is column 7
  const hash = R.bitmapLabelFilters('#1', { x: 0, y: 0, px: 1 });
  assert.ok(hash.includes('drawbox=x=7:y=0:w=1:h=1:color=white:t=fill'), "the '1' after '#' starts at column 6");
  assert.equal(hash[0], 'drawbox=x=-2:y=-2:w=13:h=9:color=black@0.6:t=fill', '5 + 1 + 3 columns plus padding');
  assert.equal(R.bitmapLabelFilters('?', { px: 1 }).length, 1, 'an unknown character prints as a space');
  assert.deepEqual(R.labelFilters('1.000s', true), ["drawtext=text='1.000s':fontcolor=white:fontsize=20:box=1:boxcolor=black@0.6:boxborderw=8:x=10:y=10"]);
  assert.deepEqual(R.labelFilters('1.000s', false), R.bitmapLabelFilters('1.000s', { x: 12, y: 12, px: 3 }));
});

const HAVE_FFMPEG = ['ffmpeg', 'ffprobe'].every((b) => {
  const r = spawnSync(b, ['-version'], { encoding: 'utf8' });
  return !r.error && r.status === 0;
});
const pngSize = (file) => { const b = fs.readFileSync(file); return [b.readUInt32BE(16), b.readUInt32BE(20)]; };

test('composeGrid tiles any count with labels, with drawtext or the built-in digits', { skip: !HAVE_FFMPEG && 'needs ffmpeg' }, (t) => {
  const dir = workDir(t);
  const r = spawnSync('ffmpeg', ['-hide_banner', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=s=108x192:r=1:d=5',
    '-start_number', '0', join(dir, 'src_%02d.png')], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  const picks = [0, 1, 2, 3, 4].map((k) => ({ file: join(dir, `src_0${k}.png`), label: `${k}.000s #${k * 30}` }));
  const bitmap = R.composeGrid({ workDir: dir, picks, out: join(dir, 'grid_bitmap.png'), drawtext: false });
  assert.deepEqual([bitmap.cols, bitmap.rows, bitmap.labels], [4, 2, 'bitmap']);
  // tiles of 108x192 scaled into 480x540 -> 304x540; 4 columns x 2 rows + 8 px padding + 12 px margin
  assert.deepEqual(pngSize(bitmap.out), [4 * 304 + 3 * 8 + 2 * 12, 2 * 540 + 8 + 2 * 12]);
  const one = R.composeGrid({ workDir: dir, picks: picks.slice(0, 1), out: join(dir, 'grid_one.png') });
  assert.deepEqual([one.cols, one.rows], [1, 1]);
  assert.ok(['drawtext', 'bitmap'].includes(one.labels));
  assert.deepEqual(pngSize(one.out), [304 + 24, 540 + 24]);
});

function chromiumReady() {
  for (const spec of [() => require.resolve('playwright', { paths: [ROOT] }), () => '/opt/node-tools/node_modules/playwright', () => process.env.KOSIF_PLAYWRIGHT]) {
    try {
      const s = spec();
      if (!s) continue;
      const pw = require(s);
      if (pw.chromium && fs.existsSync(pw.chromium.executablePath())) return true;
    } catch (e) { /* try the next one */ }
  }
  return false;
}
const CAN_RENDER = HAVE_FFMPEG && chromiumReady();

test('CLI: --stills writes each still, a labelled grid and stills.json, and no video', { skip: !CAN_RENDER && 'needs Playwright Chromium and ffmpeg' }, (t) => {
  const dir = workDir(t);
  const out = join(dir, 'film.mp4');
  const report = join(dir, 'report.json');
  const r = run('--in', PAGE, '--out', out, '--width', '270', '--height', '480', '--offline', '--stills', '2,0.5,1:00', '--report', report);
  assert.equal(r.status, 0, r.stderr);
  const stillsDir = join(dir, 'film_stills');
  assert.match(r.stdout, new RegExp(`^STILLS ${join(stillsDir, 'stills_grid.png').replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`, 'm'));
  assert.match(r.stderr, /--stills 60 lies past the film's duration \(12s\)/);
  assert.ok(!fs.existsSync(out), 'no video is encoded');
  for (const name of ['still_0.500.png', 'still_2.000.png', 'still_60.000.png']) assert.deepEqual(pngSize(join(stillsDir, name)), [270, 480], name);
  const manifest = JSON.parse(fs.readFileSync(join(stillsDir, 'stills.json'), 'utf8'));
  assert.equal(manifest.schema, 'kosif.render_html.stills.v1');
  assert.equal(manifest.driver, 'seek');
  assert.deepEqual(manifest.stills.map((s) => [s.t, s.t_actual, s.frame, s.label]), [[0.5, 0.5, 15, '0.500s'], [2, 2, 60, '2.000s'], [60, 60, 1800, '60.000s']]);
  assert.deepEqual(manifest.grid_layout, { cols: 3, rows: 1 });
  assert.deepEqual(JSON.parse(fs.readFileSync(report, 'utf8')), manifest, '--report gets the same manifest');
  // seek mode draws exactly the requested time: the stills differ, and a second run of the same list
  // (given in another order, without --out, through the skill's bundled copy) gives byte-identical files
  assert.ok(!fs.readFileSync(join(stillsDir, 'still_0.500.png')).equals(fs.readFileSync(join(stillsDir, 'still_2.000.png'))));
  const again = spawnSync(process.execPath, [SKILL_COPY, '--in', PAGE, '--stills-dir', join(dir, 'again'), '--width', '270', '--height', '480',
    '--offline', '--stills', '1:00,2,0.5'], { cwd: dir, encoding: 'utf8' });
  assert.equal(again.status, 0, again.stderr);
  for (const name of ['still_0.500.png', 'still_2.000.png', 'still_60.000.png']) {
    assert.ok(fs.readFileSync(join(dir, 'again', name)).equals(fs.readFileSync(join(stillsDir, name))), `${name} is deterministic`);
  }
  assert.deepEqual(fs.readdirSync(join(dir, 'again')).sort(), ['still_0.500.png', 'still_2.000.png', 'still_60.000.png', 'stills.json', 'stills_grid.png']);
});
