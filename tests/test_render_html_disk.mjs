// tools/render_html.cjs disk guard: the free-space estimate, the stale kosif-frames-* folder
// selection, --clean-stale, the signal cleanup and the out-of-space stop. No test launches a
// browser or touches the network; every folder lives in a private temp root, never in /tmp itself.
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPT = join(ROOT, 'tools', 'render_html.cjs');
const PAGE = join(ROOT, 'starters', 'html-canvas', 'index.html');
const require = createRequire(import.meta.url);
const R = require(SCRIPT);

const HOUR = 3600 * 1000;

function makeRoot(t) {
  const root = fs.mkdtempSync(join(os.tmpdir(), 'kosif-disk-test-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
}

// A folder with `bytes` bytes of fake frames, last modified `ageH` hours before `now`.
function frameDir(root, name, { ageH, bytes = 0, marker = null, now = Date.now() }) {
  const dir = join(root, name);
  fs.mkdirSync(dir);
  if (bytes) fs.writeFileSync(join(dir, 'frame_000000.png'), Buffer.alloc(bytes));
  if (marker) fs.writeFileSync(join(dir, R.RENDER_MARKER), JSON.stringify(marker));
  const when = new Date(now - ageH * HOUR);
  fs.utimesSync(dir, when, when); // after the writes, which would bump the folder's mtime
  return dir;
}

function deadPid() {
  const r = spawnSync(process.execPath, ['-e', '0']);
  return r.pid; // that process has exited; pid reuse within the test is vanishingly unlikely
}

test('space estimate is frames x width x height x 1.7 plus 10%', () => {
  assert.equal(R.PNG_BYTES_PER_PIXEL, 1.7);
  assert.equal(R.SPACE_MARGIN, 0.1);
  assert.equal(R.estimateFrameBytes(1, 1080, 1920), 3877632); // 1080*1920*1.7*1.1
  assert.equal(R.estimateFrameBytes(300, 1080, 1920), 1163289600); // 10 s at 30 fps, about 1.1 GB
  assert.equal(R.estimateFrameBytes(1, 3, 3), 17); // 16.83 rounded
  for (const bad of [[0, 1080, 1920], [10, 0, 1920], [-1, 10, 10], [NaN, 10, 10]]) {
    assert.equal(R.estimateFrameBytes(...bad), 0, String(bad));
  }
  // the observed failure: 3.4 MB real frames stay under the per-frame estimate
  assert.ok(R.estimateFrameBytes(1, 1080, 1920) > 3.4 * 1024 * 1024);
  assert.equal(R.fmtBytes(512), '512 B');
  assert.equal(R.fmtBytes(3877632), '3.7 MB');
  assert.equal(R.fmtBytes(8 * 1024 ** 3), '8.0 GB');
});

test('space verdict and message: shortfall, reservations by other renders, skipped check', () => {
  const needed = R.estimateFrameBytes(2700, 1080, 1920); // 90 s at 30 fps, about 9.8 GB
  let v = R.spaceVerdict({ needed, free: 4 * 1024 ** 3 });
  assert.equal(v.ok, false);
  assert.equal(v.skipped, false);
  assert.equal(R.spaceVerdict({ needed, free: needed }).ok, true, 'exactly enough is enough');
  v = R.spaceVerdict({ needed, free: needed + 10, reserved: 11 });
  assert.equal(v.ok, false, 'bytes another running render will still write are not free');
  assert.equal(v.available, needed - 1);
  v = R.spaceVerdict({ needed, free: null });
  assert.deepEqual([v.ok, v.skipped], [true, true]);

  const msg = R.spaceMessage({ needed, free: 4 * 1024 ** 3, reserved: 2 * 1024 ** 3, frames: 2700, width: 1080, height: 1920,
    dir: '/tmp/kosif-frames-abc', reclaimable: 7 * 1024 ** 3 });
  assert.match(msg, /not enough disk space for the PNG frames in \/tmp\/kosif-frames-abc/);
  assert.match(msg, /need about 9\.8 GB: 2700 frames x 1080x1920 px x 1\.7 bytes\/px \+ 10% margin/);
  assert.match(msg, /free on that disk: 4\.0 GB; other renders running now still have to write about 2\.0 GB there/);
  assert.match(msg, /--frames-dir <folder on a disk with more free space>/);
  assert.match(msg, /--clean-stale deletes 7\.0 GB/);
  assert.match(msg, /--start <s> --duration <s>/);
  assert.match(msg, /--no-space-check/);
  const plain = R.spaceMessage({ needed, free: 1, frames: 1, width: 2, height: 2, dir: '/x' });
  assert.doesNotMatch(plain, /--clean-stale|other renders/, 'only mentions what applies');
});

test('free space comes from fs.statfsSync and degrades gracefully without it', (t) => {
  const missing = R.freeSpace(os.tmpdir(), null);
  assert.equal(missing.free, null);
  assert.match(missing.reason, /statfsSync is not available/);
  const failing = R.freeSpace('/nowhere', () => { const e = new Error('nope'); e.code = 'ENOENT'; throw e; });
  assert.equal(failing.free, null);
  assert.match(failing.reason, /ENOENT/);
  assert.deepEqual(R.freeSpace('/x', () => ({ bavail: 10, bsize: 4096 })), { free: 40960, reason: null });
  assert.deepEqual(R.freeSpace('/x', () => ({ bavail: 10n, bsize: 4096n })), { free: 40960, reason: null }, 'bigint statfs');
  if (typeof fs.statfsSync !== 'function') { t.skip(`Node ${process.versions.node} has no fs.statfsSync`); return; }
  const real = R.freeSpace(os.tmpdir());
  assert.equal(real.reason, null);
  assert.ok(Number.isFinite(real.free) && real.free >= 0);
});

test('stale selection: only own kosif-frames-* folders older than 6 h, not running, not excluded', (t) => {
  const root = makeRoot(t);
  const now = Date.now();
  const dead = deadPid();
  const old = frameDir(root, 'kosif-frames-old111', { ageH: 30, bytes: 3000, now });
  const older = frameDir(root, 'kosif-frames-old000', { ageH: 50, bytes: 1000, marker: { pid: dead, bytes: 5000 }, now });
  frameDir(root, 'kosif-frames-fresh1', { ageH: 1, bytes: 10, now });
  frameDir(root, 'kosif-frames-edge59', { ageH: 5.9, now });
  const current = frameDir(root, 'kosif-frames-curent', { ageH: 40, bytes: 10, now });
  frameDir(root, 'kosif-frames-alive1', { ageH: 40, bytes: 10, marker: { pid: process.pid, bytes: 99 }, now });
  frameDir(root, 'other-frames-old', { ageH: 40, bytes: 10, now });
  fs.writeFileSync(join(root, 'kosif-frames-file'), 'not a folder');
  const target = frameDir(root, 'outside-target', { ageH: 40, bytes: 10, now });
  try { fs.symlinkSync(target, join(root, 'kosif-frames-link')); } catch { /* no symlinks here */ }
  const nested = join(old, 'sub');
  fs.mkdirSync(nested);
  fs.writeFileSync(join(nested, 'x.png'), Buffer.alloc(500));
  const when = new Date(now - 30 * HOUR);
  fs.utimesSync(old, when, when);

  const stale = R.findStaleFrameDirs({ tmpDir: root, now, exclude: [current] });
  assert.deepEqual(stale.map((d) => d.name), ['kosif-frames-old000', 'kosif-frames-old111'], 'oldest first');
  assert.deepEqual(stale.map((d) => d.bytes), [1000 + fs.statSync(join(older, R.RENDER_MARKER)).size, 3500]);
  assert.ok(stale.every((d) => d.ageMs > 6 * HOUR));

  // the age limit is a parameter; without the exclusion the in-use folder would qualify
  assert.ok(R.findStaleFrameDirs({ tmpDir: root, now }).some((d) => d.path === current));
  assert.equal(R.findStaleFrameDirs({ tmpDir: root, now, maxAgeMs: 100 * HOUR }).length, 0);
  // a marker whose process still runs keeps even an old folder out of the list
  const all = R.findStaleFrameDirs({ tmpDir: root, now, exclude: [current], isAlive: () => true });
  assert.deepEqual(all.map((d) => d.name), ['kosif-frames-old111']);
  assert.deepEqual(R.findStaleFrameDirs({ tmpDir: join(root, 'missing'), now }), [], 'missing temp dir lists nothing');
});

test('removing stale folders deletes exactly those, never the excluded or a non-matching path', (t) => {
  const root = makeRoot(t);
  const now = Date.now();
  const a = frameDir(root, 'kosif-frames-aaaaaa', { ageH: 10, bytes: 100, now });
  const b = frameDir(root, 'kosif-frames-bbbbbb', { ageH: 12, bytes: 100, now });
  const keep = frameDir(root, 'kosif-frames-keep01', { ageH: 2, bytes: 100, now });
  const stray = frameDir(root, 'not-ours', { ageH: 99, bytes: 100, now });
  const stale = R.findStaleFrameDirs({ tmpDir: root, now });
  assert.deepEqual(stale.map((d) => d.path), [b, a]);
  // a hand-made list is re-checked: excluded and non-prefixed paths survive
  const removed = R.removeStaleFrameDirs([...stale, { path: stray }, { path: keep }], { exclude: [a, keep] });
  assert.deepEqual(removed.map((d) => d.path), [b]);
  assert.equal(fs.existsSync(b), false);
  for (const p of [a, keep, stray]) assert.ok(fs.existsSync(p), p);
  assert.deepEqual(R.removeStaleFrameDirs([{ path: b }]), [], 'already gone');
});

test('other running renders reserve what they still have to write on the same disk', (t) => {
  const root = makeRoot(t);
  const now = Date.now();
  const otherPid = 2147480000; // fake pid, declared alive by the stub below
  frameDir(root, 'kosif-frames-run001', { ageH: 0, bytes: 400, marker: { pid: otherPid, bytes: 1000 }, now });
  frameDir(root, 'kosif-frames-run002', { ageH: 0, bytes: 5000, marker: { pid: otherPid, bytes: 1000 }, now });
  frameDir(root, 'kosif-frames-mine01', { ageH: 0, marker: { pid: process.pid, bytes: 777 }, now });
  frameDir(root, 'kosif-frames-nomark', { ageH: 0, bytes: 10, now });
  const alive = () => true;
  const markerSize = fs.statSync(join(root, 'kosif-frames-run001', R.RENDER_MARKER)).size;
  const expected = 1000 - (400 + markerSize); // run002 already wrote more than it reserved: 0
  assert.equal(R.reservedByOtherRenders({ tmpDir: root, isAlive: alive }), expected);
  assert.equal(R.reservedByOtherRenders({ tmpDir: root, isAlive: () => false }), 0, 'finished renders reserve nothing');
  const dev = fs.statSync(root).dev;
  assert.equal(R.reservedByOtherRenders({ tmpDir: root, isAlive: alive, dev }), expected);
  assert.equal(R.reservedByOtherRenders({ tmpDir: root, isAlive: alive, dev: -1 }), 0, 'another filesystem does not count');
  assert.equal(R.reservedByOtherRenders({ tmpDir: root, isAlive: alive, exclude: [join(root, 'kosif-frames-run001')] }), 0);
  assert.equal(R.isPidAlive(process.pid), true);
  assert.equal(R.isPidAlive(deadPid()), false);
  assert.equal(R.isPidAlive(0), false);
});

test('signals remove the temp frames and exit with 130 / 143 / 129', { skip: process.platform === 'win32' && 'POSIX signals' }, async (t) => {
  const root = makeRoot(t);
  assert.deepEqual(R.SIGNAL_EXIT, { SIGINT: 130, SIGTERM: 143, SIGHUP: 129 });
  const child = `
    const fs = require('fs'), path = require('path');
    const R = require(${JSON.stringify(SCRIPT)});
    const dir = fs.mkdtempSync(path.join(${JSON.stringify(root)}, R.FRAMES_PREFIX));
    fs.writeFileSync(path.join(dir, 'frame_000000.png'), Buffer.alloc(1000));
    R.installSignalCleanup(() => fs.rmSync(dir, { recursive: true, force: true }));
    process.stdout.write(dir + '\\n');
    setInterval(() => {}, 1000);`;
  for (const [sig, code] of Object.entries(R.SIGNAL_EXIT)) {
    const p = spawn(process.execPath, ['-e', child], { stdio: ['ignore', 'pipe', 'pipe'] });
    const dir = await new Promise((resolve, reject) => {
      let buf = '';
      p.stdout.on('data', (d) => { buf += d; if (buf.includes('\n')) resolve(buf.trim()); });
      p.on('error', reject);
      p.on('exit', () => reject(new Error('child exited before it was ready')));
    });
    assert.ok(fs.existsSync(join(dir, 'frame_000000.png')));
    const exited = new Promise((resolve) => p.on('exit', (c, s) => resolve([c, s])));
    p.kill(sig);
    assert.deepEqual(await exited, [code, null], sig);
    assert.equal(fs.existsSync(dir), false, `${sig} left ${dir}`);
  }
  // the returned function removes exactly the handlers it added
  const before = Object.keys(R.SIGNAL_EXIT).map((s) => process.listenerCount(s));
  const off = R.installSignalCleanup(() => {}, { exit: () => assert.fail('must not exit') });
  assert.deepEqual(Object.keys(R.SIGNAL_EXIT).map((s) => process.listenerCount(s)), before.map((n) => n + 1));
  off();
  assert.deepEqual(Object.keys(R.SIGNAL_EXIT).map((s) => process.listenerCount(s)), before);
});

test('CLI: stale folders are listed, --clean-stale deletes only them (stops at a missing ffmpeg)', (t) => {
  const root = makeRoot(t);
  const now = Date.now();
  const stale = frameDir(root, 'kosif-frames-stale1', { ageH: 8, bytes: 2048, now });
  const fresh = frameDir(root, 'kosif-frames-fresh1', { ageH: 1, bytes: 2048, now });
  const mine = frameDir(root, 'kosif-frames-mine01', { ageH: 9, bytes: 10, now });
  // PATH without ffmpeg: the run stops at the tool check right after the stale report,
  // before any frames folder is created or Chromium is looked for.
  const env = { ...process.env, TMPDIR: root, PATH: join(root, 'no-bin') };
  const base = [SCRIPT, '--in', PAGE, '--out', join(root, 'out', 'x.mp4'), '--frames-dir', mine];
  let r = spawnSync(process.execPath, base, { cwd: ROOT, env, encoding: 'utf8' });
  assert.equal(r.status, 2, r.stderr);
  assert.match(r.stderr, /1 stale kosif-frames-\* folder older than 6 h/);
  assert.match(r.stderr, /kosif-frames-stale1 {2}2\.0 KB {2}8\.0 h old/);
  assert.doesNotMatch(r.stderr, /fresh1|mine01/, 'fresh and in-use folders are not listed');
  assert.match(r.stderr, /add --clean-stale/);
  assert.match(r.stderr, /ffmpeg is required/);
  assert.ok(fs.existsSync(stale), 'listing deletes nothing');

  r = spawnSync(process.execPath, [...base, '--clean-stale'], { cwd: ROOT, env, encoding: 'utf8' });
  assert.equal(r.status, 2, r.stderr);
  assert.match(r.stdout, /removed stale .*kosif-frames-stale1 \(2\.0 KB, 8\.0 h old\)/);
  assert.equal(fs.existsSync(stale), false);
  assert.ok(fs.existsSync(fresh) && fs.existsSync(mine), 'only the stale folder is deleted');
  assert.deepEqual(fs.readdirSync(root).filter((n) => n.startsWith('kosif-frames-')).sort(),
    ['kosif-frames-fresh1', 'kosif-frames-mine01'], 'no new temp frames folder was left');

  const flags = R.parseArgs(['--clean-stale', 'stray', '--no-space-check', '--out', 'y.mp4']);
  assert.deepEqual([flags['clean-stale'], flags['no-space-check'], flags.out, flags._], [true, true, 'y.mp4', ['stray']]);
  const help = spawnSync(process.execPath, [SCRIPT, '--help'], { encoding: 'utf8' }).stdout;
  assert.match(help, /--no-space-check/);
  assert.match(help, /--clean-stale/);
  assert.match(help, /130\/143\/129 stopped by SIGINT\/SIGTERM\/SIGHUP/);
});

test('CLI: a render that cannot fit stops before Chromium starts and removes its temp folder', (t) => {
  const root = makeRoot(t);
  // 1080x1920 at 60 fps for 100000 s: about 21 TB of frames, more than any test disk.
  const r = spawnSync(process.execPath, [SCRIPT, '--in', PAGE, '--out', join(root, 'big.mp4'), '--offline',
    '--duration', '100000', '--fps', '60'], { cwd: ROOT, env: { ...process.env, TMPDIR: root }, encoding: 'utf8' });
  if (/is required but not runnable|Playwright not found/.test(r.stderr)) { t.skip('needs ffmpeg/ffprobe and the Playwright package (not launched)'); return; }
  if (/free-space check skipped/.test(r.stderr)) { t.skip('no fs.statfsSync on this Node'); return; }
  assert.equal(r.status, 2, r.stderr);
  assert.match(r.stderr, /not enough disk space for the PNG frames/);
  assert.match(r.stderr, /6000000 frames x 1080x1920 px/);
  assert.match(r.stderr, /--frames-dir/);
  assert.doesNotMatch(r.stdout, /loading /, 'the page was never loaded');
  assert.doesNotMatch(r.stderr, /at .*render_html\.cjs/, 'a clear message, not a stack trace');
  assert.deepEqual(fs.readdirSync(root).filter((n) => n.startsWith('kosif-frames-')), [], 'temp frames folder removed');
});
