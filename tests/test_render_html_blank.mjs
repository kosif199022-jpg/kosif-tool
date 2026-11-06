// tools/render_html.cjs blank-frame guard: the PNG blank check, the black-run finder, SeekDriver's
// fresh-browser recapture (with a fake page, no Chromium), option errors, and two real renders of
// tests/fixtures/blank_after_seeks.html (a page that turns pure black after 40 seeks per page load),
// which skip unless Playwright, its Chromium and ffmpeg are installed.
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import zlib from 'node:zlib';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPT = join(ROOT, 'tools', 'render_html.cjs');
const FIXTURE = join(ROOT, 'tests', 'fixtures', 'blank_after_seeks.html');
const INTENDED = join(ROOT, 'tests', 'fixtures', 'blank_intended.html');
const require = createRequire(import.meta.url);
const R = require(SCRIPT);
const run = (...args) => spawnSync(process.execPath, [SCRIPT, ...args], { cwd: ROOT, encoding: 'utf8' });

// A small PNG encoder: pixel(x, y) -> [r, g, b(, a)]; filter(y) picks the row filter (0-4).
function crc32(buf) {
  let c, crc = 0xffffffff;
  for (const b of buf) { c = (crc ^ b) & 0xff; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; crc = (crc >>> 8) ^ c; }
  return (crc ^ 0xffffffff) >>> 0;
}
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
  const td = Buffer.concat([Buffer.from(type, 'latin1'), data]);
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td));
  return Buffer.concat([len, td, crc]);
}
function makePng(w, h, pixel, { alpha = false, filter = () => 0 } = {}) {
  const bpp = alpha ? 4 : 3, stride = w * bpp;
  const rows = [];
  let prev = Buffer.alloc(stride);
  for (let y = 0; y < h; y++) {
    const cur = Buffer.alloc(stride);
    for (let x = 0; x < w; x++) { const p = pixel(x, y); for (let k = 0; k < bpp; k++) cur[x * bpp + k] = p[k] ?? 255; }
    const f = filter(y), out = Buffer.alloc(stride + 1); out[0] = f;
    for (let i = 0; i < stride; i++) {
      const a = i >= bpp ? cur[i - bpp] : 0, b = prev[i], c = i >= bpp ? prev[i - bpp] : 0;
      let p = 0;
      if (f === 1) p = a; else if (f === 2) p = b; else if (f === 3) p = (a + b) >> 1;
      else if (f === 4) { const q = a + b - c, pa = Math.abs(q - a), pb = Math.abs(q - b), pc = Math.abs(q - c); p = pa <= pb && pa <= pc ? a : pb <= pc ? b : c; }
      out[i + 1] = (cur[i] - p) & 0xff;
    }
    rows.push(out); prev = cur;
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = alpha ? 6 : 2;
  return Buffer.concat([Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]), chunk('IHDR', ihdr),
    chunk('IDAT', zlib.deflateSync(Buffer.concat(rows))), chunk('IEND', Buffer.alloc(0))]);
}
const BLACK = (w = 40, h = 30, o) => makePng(w, h, () => [0, 0, 0], o);
const GRAIN = (w = 40, h = 30, o) => makePng(w, h, (x, y) => [(x * 7 + y * 13) % 50, 10, 20], o);

test('pngBlankness: black, uniform colour and content, with every row filter and with alpha', () => {
  for (const f of [0, 1, 2, 3, 4]) {
    const o = { filter: () => f };
    assert.deepEqual(R.pngBlankness(BLACK(40, 30, o)), { kind: 'black', rgb: [0, 0, 0] }, `filter ${f}`);
    assert.equal(R.pngBlankness(GRAIN(40, 30, o)), null, `filter ${f}`);
    assert.deepEqual(R.pngBlankness(makePng(20, 10, () => [200, 30, 40], o)), { kind: 'uniform', rgb: [200, 30, 40] }, `filter ${f}`);
  }
  const mixed = { filter: (y) => y % 5 };
  assert.deepEqual(R.pngBlankness(BLACK(64, 48, { ...mixed, alpha: true })), { kind: 'black', rgb: [0, 0, 0] });
  assert.equal(R.pngBlankness(GRAIN(64, 48, { ...mixed, alpha: true })), null);
  // near-black noise counts as black; one bright pixel at the very end does not
  assert.equal(R.pngBlankness(makePng(30, 20, (x, y) => [(x + y) % (R.BLANK_DARK_LEVEL + 1), 0, 1])).kind, 'black');
  assert.equal(R.pngBlankness(makePng(30, 20, (x, y) => (x === 29 && y === 19 ? [255, 255, 255] : [0, 0, 0]))), null);
  // unreadable input is "not blank", never an exception
  for (const bad of [Buffer.alloc(0), Buffer.from('not a png at all, just some bytes here....'), BLACK().subarray(0, 50)]) {
    assert.equal(R.pngBlankness(bad), null);
  }
});

test('captureBlankness decodes only small captures', () => {
  const png = BLACK(40, 30);
  assert.equal(R.captureBlankness(png, 40, 30).kind, 'black');
  // Read as a 1x1 frame, the same bytes are "large" once past the floor: not decoded, so not blank.
  const big = Buffer.concat([png, Buffer.alloc(R.BLANK_SUSPECT_MIN_BYTES)]);
  assert.equal(R.captureBlankness(big, 1, 1), null);
  assert.equal(R.pngBlankness(big).kind, 'black', 'trailing bytes after IEND are ignored by the decoder');
  // 1080x1920: a capture under about 100 KB is decoded, a 2 MB grain frame is not
  assert.equal(Math.round(1080 * 1920 * R.BLANK_SUSPECT_BYTES_PER_PIXEL), 103680);
});

test('signalstats parsing and black runs longer than 2 frames', () => {
  const text = 'frame:0    pts:0  pts_time:0\nlavfi.signalstats.YMAX=16\nframe:1 pts:512\nlavfi.signalstats.YMAX=235.5\n';
  assert.deepEqual(R.parseSignalstatsYmax(text), [16, 235.5]);
  assert.deepEqual(R.blackRuns([16, 16, 200, 16, 16, 16, 40, 17, 17, 17, 17]), [
    { first: 3, last: 5, frames: 3 }, { first: 7, last: 10, frames: 4 }]);
  assert.deepEqual(R.blackRuns([16, 16, 90, 16, 16]), [], 'runs of 2 are allowed (cuts, flashes)');
  assert.deepEqual(R.blackRuns([18, 18, 18, 18]), [], 'a fade with grain is not fully black');
  assert.deepEqual(R.blackRuns([]), []);
  assert.equal(R.blackRunsText([{ first: 53, last: 59, frames: 7 }], { fps: 30, start: 178 }),
    'frames 53-59 (7, t=179.767s-179.967s)');
});

// A fake page: seek() is recorded, captures come from a script of PNGs per browser generation.
function fakeDriver({ blackFrom = Infinity, intendedBlack = () => false, retries = 2, maxFramesPerPage = 0 } = {}) {
  const state = { generation: 0, seeks: 0, reopened: 0 };
  let t = 0;
  const makePage = () => ({ evaluate: async (fn, time) => { t = time; state.seeks += 1; } });
  const makeCdp = () => ({
    send: async () => {
      const black = intendedBlack(t) || state.seeks > blackFrom;
      return { data: (black ? BLACK() : GRAIN()).toString('base64') };
    },
  });
  const reopen = async () => { state.generation += 1; state.reopened += 1; state.seeks = 0; return { page: makePage(), cdp: makeCdp() }; };
  const d = new R.SeekDriver(makePage(), makeCdp(), { width: 40, height: 30, scale: 1, reopen, blankRetries: retries, maxFramesPerPage });
  return { d, state };
}

async function shootAll(d, frames, dir) {
  for (let i = 0; i < frames; i++) await d.shoot(i / 30, join(dir, `f${i}.png`), i);
}

test('SeekDriver.shoot: a page that turns black is recaptured in a fresh browser; the frames are logged', async (t) => {
  const dir = fs.mkdtempSync(join(os.tmpdir(), 'kosif-blank-test-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const { d } = fakeDriver({ blackFrom: 10 });
  await shootAll(d, 25, dir);
  assert.deepEqual(d.stats.recovered, [10, 20]);
  assert.deepEqual(d.stats.kept, []);
  assert.equal(d.stats.reopens, 2);
  for (let i = 0; i < 25; i++) assert.equal(R.pngBlankness(fs.readFileSync(join(dir, `f${i}.png`))), null, `frame ${i}`);

  const sched = fakeDriver({ blackFrom: 10, maxFramesPerPage: 8 }).d;
  await shootAll(sched, 25, dir);
  assert.deepEqual(sched.stats.recovered, [], 'a fresh browser every 8 frames never reaches the failure');
  assert.equal(sched.stats.scheduled_reopens, 3);

  const off = fakeDriver({ blackFrom: 10, retries: 0 }).d;
  await shootAll(off, 15, dir);
  assert.equal(off.stats.reopens, 0, '--blank-retries 0 turns the guard off');
});

test('SeekDriver.shoot: an intended black stretch is retried once, then kept (and looked at again later)', async (t) => {
  const dir = fs.mkdtempSync(join(os.tmpdir(), 'kosif-blank-test-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const n = R.BLANK_RECHECK_FRAMES;
  const { d } = fakeDriver({ intendedBlack: (time) => { const f = Math.round(time * 30); return f >= 30 && f < 30 + n + 5; } });
  await shootAll(d, 30 + n + 10, dir);
  assert.deepEqual(d.stats.recovered, []);
  assert.equal(d.stats.kept.length, n + 5);
  assert.equal(d.stats.reopens, 4, 'two retries at the start of the run, two more after BLANK_RECHECK_FRAMES frames');
});

test('option errors for the guard', () => {
  let r = run('--in', FIXTURE, '--out', 'x.mp4', '--black-check', 'maybe');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--black-check must be warn, fail or off/);
  r = run('--in', FIXTURE, '--out', 'x.mp4', '--max-frames-per-page', '0');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--max-frames-per-page must be a whole number >= 1/);
  r = run('--in', FIXTURE, '--out', 'x.mp4', '--blank-retries', '-1');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--blank-retries must be a whole number >= 0/);
  assert.match(run('--help').stdout, /--max-frames-per-page <n>[\s\S]*--blank-retries <n>[\s\S]*--black-check <m>/);
});

function canRender() {
  try { require('playwright'); } catch (e) { return 'Playwright is not installed'; }
  for (const tool of ['ffmpeg', 'ffprobe']) {
    if (spawnSync(tool, ['-version']).status !== 0) return `${tool} is not installed`;
  }
  return false;
}

test('a 4 s chunk of a page that turns black renders with zero black frames', { skip: canRender(), timeout: 300000 }, (t) => {
  const dir = fs.mkdtempSync(join(os.tmpdir(), 'kosif-blank-render-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const common = ['--width', '270', '--height', '480', '--offline'];
  const out = join(dir, 'ok.mp4'), report = join(dir, 'ok.json');
  let r = run('--in', FIXTURE, '--out', out, '--report', report, '--black-check', 'fail', ...common);
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /blank-guard: recovered frame 40 \(t=1\.333s\) on attempt 1/);
  assert.match(r.stdout, /black-frame check: no run of more than 2 fully black frames in 120 frames/);
  const rep = JSON.parse(fs.readFileSync(report, 'utf8'));
  assert.deepEqual(rep.blank_guard.recovered, [40, 80]);
  assert.equal(rep.black_frames.ok, true);
  assert.equal(R.checkBlackFrames(out).ok, true);

  // Without the guard the same chunk goes black from frame 40, and the post-encode check catches it.
  const bad = join(dir, 'bad.mp4');
  r = run('--in', FIXTURE, '--out', bad, '--blank-retries', '0', '--black-check', 'fail', '--duration', '2', ...common);
  assert.equal(r.status, 3);
  assert.match(r.stderr, /1 run\(s\) of more than 2 fully black frames: frames 40-59 \(20, t=1\.333s-1\.967s\)/);
  r = run('--in', FIXTURE, '--out', bad, '--blank-retries', '0', '--duration', '2', ...common);
  assert.equal(r.status, 0, 'warn is the default');
  assert.match(r.stderr, /black frames: 1 run/);
});

test('--max-frames-per-page keeps the page fresh; an intended black stretch is kept', { skip: canRender(), timeout: 300000 }, (t) => {
  const dir = fs.mkdtempSync(join(os.tmpdir(), 'kosif-blank-render-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const common = ['--width', '270', '--height', '480', '--offline', '--duration', '2'];
  let r = run('--in', FIXTURE, '--out', join(dir, 'a.mp4'), '--max-frames-per-page', '30', ...common);
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /blank-guard: 1 fresh browser\(s\) \(1 scheduled\); recovered frames \[\]; kept blank \[\]/);
  r = run('--in', INTENDED, '--out', join(dir, 'b.mp4'), '--max-frames-per-page', '30', ...common);
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stderr, /frame 30 \(t=1\.000s\) is still black rgb\(0,0,0\) after 2 fresh browser\(s\); kept as intended/);
  assert.match(r.stdout, /kept blank \[30, 31, .*, 44\]/);
});
