// Photo cover: the camera never shows an edge of the photo, and the frame checker catches it when one does.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
await import('../tools/photo_cover.js');
const C = globalThis.KosifCover;

function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
const ASPECTS = [[941, 1672], [1080, 1920], [1920, 1080], [1000, 1000], [600, 2000], [3000, 800], [4032, 3024]];

test('cover: exact-cover zoom fills a 9:16 frame for every photo shape (incl. the 941x1672 one-pixel case)', () => {
  for (const [iw, ih] of ASPECTS) {
    const cam = C.camera({ W: 1080, H: 1920, iw, ih });
    assert.ok(C.covers(cam, 2), `${iw}x${ih}`);
    assert.ok(cam.s * ih >= 1920 && cam.s * iw >= 1080, `${iw}x${ih} scale ${cam.s}`);
  }
});

test('camera moves: random zoom / pan / shake / rotation / blur never uncover the frame', () => {
  const R = rng(20261025);
  for (let k = 0; k < 20000; k++) {
    const [iw, ih] = ASPECTS[k % ASPECTS.length];
    const o = { W: 1080, H: 1920, iw, ih, zoom: 0.5 + R() * 1.5, fx: -0.3 + R() * 1.6, fy: -0.3 + R() * 1.6,
      ox: (R() - 0.5) * 600, oy: (R() - 0.5) * 600, rot: (R() - 0.5) * 30, blur: R() * 12, mode: R() < 0.5 ? 'zoom' : 'clamp' };
    const cam = C.camera(o);
    assert.ok(C.covers(cam, 2 * o.blur), JSON.stringify(o));
    assert.ok(cam.zoom >= 1 - 1e-9, 'zoom never drops below cover');
  }
});

test('minimum scale: a pull-out below cover is held at cover, and minZoom raises the floor', () => {
  const a = C.camera({ W: 1080, H: 1920, iw: 1920, ih: 1080, zoom: 0.7, bleed: 0 });
  assert.ok(Math.abs(a.zoom - 1) < 1e-9);
  const b = C.camera({ W: 1080, H: 1920, iw: 1920, ih: 1080, zoom: 1, minZoom: 1.2, bleed: 0 });
  assert.ok(Math.abs(b.zoom - 1.2) < 1e-9);
});

test("mode 'zoom' keeps the requested centre (no sticking at the edge) while 'clamp' moves it", () => {
  const o = { W: 1080, H: 1920, iw: 1080, ih: 1920, fx: 0.2, fy: 0.5 };
  const c = C.camera(o), z = C.camera({ ...o, mode: 'zoom' });
  assert.ok(c.clamped && !z.clamped);
  assert.ok(Math.abs(z.cx - 0.2 * 1080) < 1e-6 && z.zoom > 1);
  assert.ok(C.covers(z, 2));
});

test('checker CLI parses its options', () => {
  const { parseArgs } = require('../tools/check_frame_cover.cjs');
  const a = parseArgs(['--in', 'x.html', '--variants', 'style=1;?style=2', '--samples', '5']);
  assert.deepEqual(a.variants, ['style=1', 'style=2']);
  assert.equal(a.samples, 5);
});

let hasPlaywright = false;
try { require.resolve('playwright'); hasPlaywright = true; } catch { /* skip browser part */ }
const run = (args) => spawnSync(process.execPath, ['tools/check_frame_cover.cjs', ...args], { cwd: ROOT, encoding: 'utf8', timeout: 300000 });
const FIXTURE = 'tests/fixtures/photo-cover/index.html';

test('frame check: five camera styles x six photo shapes render with no empty edge', { skip: !hasPlaywright && 'Playwright not installed' }, () => {
  const variants = [];
  for (const a of ['941x1672', '1080x1920', '1920x1080', '1000x1000', '600x2000', '3000x800']) for (let s = 1; s <= 5; s++) variants.push(`aspect=${a}&style=${s}`);
  const r = run(['--in', FIXTURE, '--variants', variants.join(';'), '--samples', '12']);
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /PASS/);
});

test('frame check: the old width-fit camera FAILS (one-pixel gap, pans, rotation, blur)', { skip: !hasPlaywright && 'Playwright not installed' }, () => {
  for (const s of [1, 2, 4, 5]) {
    const r = run(['--in', FIXTURE, '--variants', `naive=1&style=${s}`, '--samples', '12']);
    assert.equal(r.status, 3, `style ${s} should fail:\n${r.stdout}${r.stderr}`);
    assert.match(r.stdout, /empty edge/);
  }
  const r = run(['--in', FIXTURE, '--variants', 'naive=1&style=1', '--times', '0']);
  assert.equal(r.status, 3, 'the 941x1672 photo at zoom 1 leaves a 1px band: ' + r.stdout);
});
