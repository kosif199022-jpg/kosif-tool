// tools/render_html.cjs: command-line parsing and the aspect table. Nothing here renders,
// so the tests need neither Playwright nor ffmpeg (every CLI run stops at a usage check).
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPT = join(ROOT, 'tools', 'render_html.cjs');
const SKILL_COPY = join(ROOT, '.claude', 'skills', 'kosif-superpowers', 'resources', 'motion-runtime', 'render_html.cjs');
const require = createRequire(import.meta.url);
const { parseArgs, aspectSize, ASPECT_NAMES, ASPECT_PRESETS } = require(SCRIPT);

const MISSING = join(ROOT, 'no-such-dir', 'missing.html');
const run = (...args) => spawnSync(process.execPath, [SCRIPT, ...args], { cwd: ROOT, encoding: 'utf8' });

test('-h and --help print usage on stdout and exit 0', () => {
  for (const flag of ['-h', '--help']) {
    const r = run(flag);
    assert.equal(r.status, 0, flag);
    assert.match(r.stdout, /--in <file\.html\|http URL> --out <out\.mp4>/, flag);
    assert.equal(r.stderr, '', flag);
  }
  assert.equal(run('--help', '--bogus').status, 0, '--help wins over other problems');
});

test('unknown options are usage errors instead of being ignored', () => {
  const r = run('--in', MISSING, '--out', 'x.mp4', '--fsp', '24');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /unknown option: --fsp/);
  assert.match(r.stderr, /Options/, 'usage follows the error');
  assert.doesNotMatch(r.stderr, /not found/, 'the bad flag is reported before anything else');
  assert.deepEqual(parseArgs(['--fsp', '24', '--constructor']).unknown, ['--fsp', '--constructor']);
});

test('stray arguments and value options without a value are usage errors', () => {
  let r = run('--in', MISSING, '--out', 'x.mp4', 'extra');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /unexpected argument: extra/);
  r = run('--in', MISSING, '--out', 'x.mp4', '--fps');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--fps needs a value/);
  // switches never swallow the next token
  const a = parseArgs(['--preview', 'x.mp4', '--offline', '--out', 'y.mp4']);
  assert.equal(a.preview, true);
  assert.equal(a.offline, true);
  assert.equal(a.out, 'y.mp4');
  assert.deepEqual(a._, ['x.mp4']);
  assert.equal(parseArgs(['-h']).help, true);
});

test('a valid command line gets past parsing (stops at the missing --in file)', () => {
  const r = run('--in', MISSING, '--out', 'x.mp4', '--preview', '--offline', '--fps', '24', '--aspect', 'مربع', '--seed', '7');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /--in file not found/);
});

test('the aspect table matches tools/aspects.py (names, presets and pixel sizes)', (t) => {
  const py = spawnSync('python3', ['-c', [
    'import json, sys',
    "sys.path.insert(0, 'tools')",
    'import aspects',
    "specs = sorted(aspects.NAMES) + ['9:16', '16:9', '1:1', '4:5', '4:3', '3:4', '2:3', '21:9', '2.35:1', '2.39:1', '1.85:1', '1920x816', '1081x1351', ' Reel ', 'CINEMA', '1:5', '5:1']",
    'print(json.dumps({"names": aspects.NAMES, "presets": {k: list(v) for k, v in aspects.PRESETS.items()}, "sizes": {s: list(aspects.resolve(s)[1:]) for s in specs}}, ensure_ascii=False))',
  ].join('\n')], { cwd: ROOT, encoding: 'utf8' });
  if (py.error || py.status !== 0) { t.skip('python3 cannot import tools/aspects.py here'); return; }
  const ref = JSON.parse(py.stdout);
  assert.deepEqual({ ...ASPECT_NAMES }, ref.names);
  assert.deepEqual({ ...ASPECT_PRESETS }, ref.presets);
  for (const [spec, [w, h]] of Object.entries(ref.sizes)) {
    assert.deepEqual(aspectSize(spec), { w, h }, spec);
  }
  for (const bad of ['junk', '0:5', '9:0', '1:6', '']) assert.equal(aspectSize(bad), null, bad);
});

test('the skill copy is byte-identical to tools/render_html.cjs', () => {
  assert.ok(readFileSync(SKILL_COPY).equals(readFileSync(SCRIPT)));
});
