#!/usr/bin/env node
'use strict';
/*
 * KOSIF render_html — deterministic HTML -> MP4 renderer.
 *
 * Renders an HTML film (local file or http URL) frame by frame with headless
 * Chromium (Playwright) and encodes the frames with ffmpeg. Two drivers:
 *
 *   seek    – the page exposes window.__kosif = { duration, seek(t) } and
 *             draws the frame for time t when asked (the KOSIF starters do).
 *   virtual – any page (CSS, WAAPI, requestAnimationFrame, GSAP). The renderer
 *             pauses Chromium's virtual clock, advances it by exactly 1000/fps ms
 *             per frame and asks the compositor for exactly one frame at that
 *             time (HeadlessExperimental.beginFrame with explicit frameTimeTicks),
 *             so CSS/WAAPI animation time, requestAnimationFrame timestamps,
 *             timers and Date.now() are all exact and reproducible.
 *
 * Usage:
 *   node tools/render_html.cjs --in <file.html|http URL> --out <out.mp4>
 *        [--aspect <spec>] [--width 1080] [--height 1920] [--fps 30] [--duration <s>] [--start 0]
 *        [--audio <file>] [--mode seek|virtual] [--preview] [--frames-dir <dir>]
 *        [--stills <t1,t2,...> [--stills-dir <dir>]] [--report <file.json>]
 *        [--crf 17] [--scale 1] [--seed <n>] [--offline] [--keep-frames]
 *        [--timeout <ms>] [--settle <ms>] [--no-space-check] [--clean-stale]
 *
 * Stills: --stills seeks the page to each film time, writes still_<t>.png and one labelled grid
 * (stills_grid.png, times printed on every tile) plus stills.json, and encodes no video.
 *
 * Audio proof: when --audio is stream-copied, the MD5 of the source's and the output's audio
 * packets (ffmpeg -map 0:a:0 -c copy -f md5 -, AAC through aac_adtstoasc as tools/verify_video.py
 * --source-audio does) is compared and the VERIFY line says audio_md5=match, or
 * audio_md5=differs (src N packets, out M packets) with a loud explanation on stderr (a cut at the
 * last video frame is allowed and never fails the render); a re-encoded track says audio_md5=reencoded.
 *
 * Disk guard: PNG frames are big (about 3.4 MB per 1080x1920 frame), so before the first
 * frame the renderer checks that the frames folder's disk can hold them, lists stale
 * kosif-frames-* temp folders left by killed renders (--clean-stale deletes them, never a
 * --frames-dir folder), and removes its own temp folder on SIGINT/SIGTERM/SIGHUP as well
 * as on normal exit.
 *
 * Node 22, CommonJS, no npm dependencies besides Playwright resolved at runtime.
 * License: MIT (part of KOSIF TOOL).
 */

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const { pathToFileURL } = require('url');

const EXIT_USAGE = 1;
const EXIT_RENDER = 2;
const EXIT_VERIFY = 3;

const DEFAULTS = {
  width: 1080,
  height: 1920,
  fps: 30,
  start: 0,
  crf: 17, // KOSIF export standard (playbooks/export-standard.md): never raise it for delivery
  scale: 1,
  timeout: 60000,
  settle: 0,
};

// Fixed epoch for Date.now() under virtual time (2026-01-01T00:00:00Z) so a page
// that reads the wall clock renders identically on every run.
const VIRTUAL_EPOCH_SECONDS = 1767225600;

// Chromium flags that make rendering reproducible in both modes.
const COMMON_FLAGS = [
  '--font-render-hinting=none',
  '--disable-lcd-text',
  '--force-color-profile=srgb',
  '--hide-scrollbars',
  '--disable-partial-raster',
  '--disable-skia-runtime-opts',
  '--autoplay-policy=no-user-gesture-required',
];

// Flags for the virtual driver: the compositor only produces a frame when the
// renderer asks for one (BeginFrame control), on the main thread, fully rastered.
const BEGIN_FRAME_FLAGS = [
  '--enable-begin-frame-control',
  '--run-all-compositor-stages-before-draw',
  '--disable-new-content-rendering-timeout',
  '--disable-threaded-animation',
  '--disable-threaded-scrolling',
  '--disable-checker-imaging',
  '--disable-image-animation-resync',
];

// Disk guard. Two renders at once once filled /tmp with PNG frames (about 3.4 MB per
// 1080x1920 frame), Page.captureScreenshot failed with "Unable to capture screenshot", and
// killed renders left 3-8 GB kosif-frames-* folders behind.
const FRAMES_PREFIX = 'kosif-frames-';
const RENDER_MARKER = '.kosif-render.json'; // {pid, bytes}: written only into temp frames folders this tool creates
const USER_FRAMES_MARKER = '.kosif-user-frames'; // written into every --frames-dir folder: --clean-stale never deletes one
// fs.mkdtempSync(FRAMES_PREFIX) appends six [A-Za-z0-9] characters: only names of that shape can be temp folders.
const TEMP_DIR_NAME = new RegExp(`^${FRAMES_PREFIX}[A-Za-z0-9]{6}$`);
// The only files a render writes into its frames folder (besides the two markers).
const RENDER_FILE = /^(frame_\d{6}|preview_(raw|tile)_\d{2})\.png$/;
const PNG_BYTES_PER_PIXEL = 1.7;            // observed upper end for Chromium PNG frames
const SPACE_MARGIN = 0.10;
const STALE_AGE_HOURS = 6;
const SIGNAL_EXIT = { SIGINT: 130, SIGTERM: 143, SIGHUP: 129 };

// --stills: at most this many times per run (each is a full-size PNG; the grid stays a sane size).
const MAX_STILLS = 64;

// ---------------------------------------------------------------- CLI parsing

class UsageError extends Error {}

function usage(stream) {
  const text = `
KOSIF render_html — deterministic HTML -> MP4

  node ${require('path').relative(process.cwd(), __filename) || 'render_html.cjs'} --in <file.html|http URL> --out <out.mp4> [options]

Options
  --aspect <spec>     any frame: 9:16, 16:9, 4:5, 21:9, 2.35:1, 1920x816 or a name that tools/aspects.py
                      accepts (reel, story, square, cinema, ... and Arabic names such as مربع or سينما)
                      (sets --width/--height; explicit --width/--height still win)
  --width <px>        viewport width in CSS px            (default ${DEFAULTS.width})
  --height <px>       viewport height in CSS px           (default ${DEFAULTS.height})
  --fps <n>           frames per second                   (default ${DEFAULTS.fps})
  --duration <s>      seconds to render (seek mode: defaults to window.__kosif.duration)
  --start <s>         film time of the first frame        (default ${DEFAULTS.start})
  --audio <file>      mux this audio (copied as-is if AAC/MP3/ALAC, else AAC 320k). A copied track is
                      proved by packet MD5: VERIFY ... audio_md5=match | differs (src N packets, out M packets)
                      (differs never fails the render: a cut at the last video frame is allowed, and stderr
                      says which packets were cut or changed); a re-encoded track says audio_md5=reencoded
  --mode seek|virtual driver; auto-detected when omitted (seek if window.__kosif exists)
  --preview           render 8 evenly spaced frames into a contact sheet PNG instead of a video,
                      written next to --out as <out name>_preview.png (out/p.mp4 -> out/p_preview.png)
  --stills <times>    instead of a video, capture the film at these times: seconds or m:ss, comma-separated
                      (--stills 0,1.5,2.25s,1:04), read to the millisecond, sorted, at most ${MAX_STILLS}. Writes
                      still_<t>.png (t with 3 decimals), stills_grid.png (labelled with the times) and stills.json.
                      Seek mode draws the exact time; virtual mode takes the nearest frame at --fps (labelled #n).
                      --start and --audio are ignored; --duration is not needed
  --stills-dir <dir>  where the stills go (created; other files in it are left alone; with it --out may be
                      omitted); default: <out name>_stills/ next to --out (out/p.mp4 -> out/p_stills/)
  --report <file>     also write a JSON report: the VERIFY values and the audio proof (render), the
                      contact sheet (preview) or the stills manifest (stills)
  --frames-dir <dir>  where PNG frames go (kept; a ${USER_FRAMES_MARKER} file marks the folder so --clean-stale never
                      deletes it); default: a temp dir (${FRAMES_PREFIX}XXXXXX) that is deleted at the end, on errors
                      and when the render is stopped with Ctrl+C, SIGTERM or SIGHUP
  --keep-frames       keep the temp frames dir
  --no-space-check    skip the free-space check. By default the render stops before the first frame when the
                      frames folder's disk has less than frames x width x height x ${PNG_BYTES_PER_PIXEL} bytes + ${SPACE_MARGIN * 100}%
                      (about 3.7 MB per 1080x1920 frame) plus what other running renders still have to write
  --clean-stale       delete this tool's own temp folders (${FRAMES_PREFIX}XXXXXX holding only frames) older than
                      ${STALE_AGE_HOURS} h (left by killed renders or --keep-frames) before rendering; without it they are only
                      listed. Never a --frames-dir folder, nor a folder that holds, or lies inside, the one in use.
  --crf <n>           libx264 quality, lower = better     (default ${DEFAULTS.crf})
  --scale <n>         device scale factor: output pixels = width*scale x height*scale (default ${DEFAULTS.scale});
                      above 1 needs seek mode (in virtual mode set --width/--height to the output size)
  --seed <n>          replace Math.random inside the page with a seeded PRNG
  --offline           abort every http(s) request (system fonts only, fully reproducible)
  --timeout <ms>      page load timeout                   (default ${DEFAULTS.timeout})
  --settle <ms>       extra wall-clock wait after the page is ready (default ${DEFAULTS.settle})
  --help, -h          this text

Unknown options and stray arguments are usage errors.
Exit codes: 0 ok, ${EXIT_USAGE} usage error, ${EXIT_RENDER} render/encode failure or not enough disk space,
${EXIT_VERIFY} ffprobe disagrees with the request, ${SIGNAL_EXIT.SIGINT}/${SIGNAL_EXIT.SIGTERM}/${SIGNAL_EXIT.SIGHUP} stopped by SIGINT/SIGTERM/SIGHUP.
`;
  (stream || process.stdout).write(text.trimStart());
}

// Every option the CLI understands. Anything else is reported as a usage error,
// so a typo such as --fsp 24 never renders silently with the default.
const VALUE_OPTIONS = new Set(['in', 'out', 'aspect', 'width', 'height', 'fps', 'duration', 'start',
  'audio', 'mode', 'frames-dir', 'crf', 'scale', 'seed', 'timeout', 'settle', 'stills', 'stills-dir', 'report']);
const FLAG_OPTIONS = new Set(['preview', 'offline', 'keep-frames', 'no-space-check', 'clean-stale', 'help']);

function parseArgs(argv) {
  const out = { _: [], unknown: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h') { out.help = true; continue; }
    if (!a.startsWith('--')) { out._.push(a); continue; }
    let key = a.slice(2);
    let val;
    const eq = key.indexOf('=');
    if (eq >= 0) { val = key.slice(eq + 1); key = key.slice(0, eq); }
    else if (!FLAG_OPTIONS.has(key) && i + 1 < argv.length && !argv[i + 1].startsWith('--')) { val = argv[++i]; }
    else { val = true; }
    if (!VALUE_OPTIONS.has(key) && !FLAG_OPTIONS.has(key)) { out.unknown.push('--' + key); continue; }
    out[key] = val;
  }
  return out;
}

// Rejects what parseArgs could not place (run after --help has been honoured).
function checkArgs(args) {
  if (args.unknown.length) throw new UsageError(`unknown option${args.unknown.length > 1 ? 's' : ''}: ${args.unknown.join(', ')}`);
  if (args._.length) throw new UsageError(`unexpected argument${args._.length > 1 ? 's' : ''}: ${args._.join(' ')} (options take the form --name value)`);
  for (const key of VALUE_OPTIONS) {
    if (args[key] === true) throw new UsageError(`--${key} needs a value`);
  }
}

function numberOpt(args, key, def, { integer = false, min = -Infinity } = {}) {
  if (args[key] === undefined) return def;
  const n = Number(args[key]);
  if (!Number.isFinite(n) || (integer && !Number.isInteger(n)) || n < min) {
    throw new UsageError(`--${key} must be a ${integer ? 'whole ' : ''}number${min > -Infinity ? ` >= ${min}` : ''}, got "${args[key]}"`);
  }
  return n;
}

// ------------------------------------------------------------ Playwright lookup

function resolvePlaywright() {
  const attempts = [];
  const candidates = [
    () => require.resolve('playwright', { paths: [process.cwd()] }),
    () => '/opt/node-tools/node_modules/playwright',
    () => process.env.KOSIF_PLAYWRIGHT,
  ];
  for (const candidate of candidates) {
    let spec;
    try { spec = candidate(); } catch (e) { attempts.push(String(e.message || e)); continue; }
    if (!spec) continue;
    try {
      const mod = require(spec);
      if (mod && mod.chromium) return { playwright: mod, from: spec };
      attempts.push(`${spec}: no chromium export`);
    } catch (e) {
      attempts.push(`${spec}: ${e.message || e}`);
    }
  }
  throw new Error(
    'Playwright not found. Tried: require("playwright") from cwd, ' +
    '/opt/node-tools/node_modules/playwright, $KOSIF_PLAYWRIGHT.\n  ' + attempts.join('\n  '),
  );
}

// ----------------------------------------------------------------- utilities

function log(msg) { process.stdout.write(msg + '\n'); }
function warn(msg) { process.stderr.write('[render_html] ' + msg + '\n'); }
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
function monoMs() { return Number(process.hrtime.bigint()) / 1e6; }
function fmtTime(t) { return t.toFixed(3) + 's'; }
function frameName(i) { return 'frame_' + String(i).padStart(6, '0') + '.png'; }

function withTimeout(promise, ms, label) {
  let timer;
  const t = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`${label} timed out after ${ms} ms`)), ms);
  });
  return Promise.race([promise, t]).finally(() => clearTimeout(timer));
}

function runTool(cmd, args) {
  const r = spawnSync(cmd, args, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.error) throw new Error(`${cmd} could not be started: ${r.error.message}`);
  return r;
}

function requireTool(cmd) {
  const r = spawnSync(cmd, ['-version'], { encoding: 'utf8' });
  if (r.error || r.status !== 0) throw new Error(`${cmd} is required but not runnable on PATH`);
}

function pngSize(file) {
  const fd = fs.openSync(file, 'r');
  try {
    const head = Buffer.alloc(24);
    fs.readSync(fd, head, 0, 24, 0);
    if (head.toString('ascii', 1, 4) !== 'PNG') throw new Error(`${file} is not a PNG`);
    return { width: head.readUInt32BE(16), height: head.readUInt32BE(20) };
  } finally { fs.closeSync(fd); }
}

function ffmpegHasFilter(name) {
  const r = spawnSync('ffmpeg', ['-hide_banner', '-filters'], { encoding: 'utf8' });
  if (r.error || r.status !== 0) return false;
  return new RegExp(`^\\s*[A-Z.]{3}\\s+${name}\\s`, 'm').test(r.stdout);
}

function checkFrameSize(file, outWidth, outHeight) {
  const size = pngSize(file);
  if (size.width !== outWidth || size.height !== outHeight) {
    throw new Error(`screenshot is ${size.width}x${size.height}, expected ${outWidth}x${outHeight}`);
  }
}

// ---------------------------------------------------------------- disk guard
// Pure helpers (no browser); tests/test_render_html_disk.mjs exercises them.

class DiskSpaceError extends Error {}

// Bytes the PNG frames will need: frames x width x height x 1.7, plus a 10% margin.
function estimateFrameBytes(frames, width, height) {
  if (!(frames > 0 && width > 0 && height > 0)) return 0;
  return Math.round(frames * width * height * PNG_BYTES_PER_PIXEL * (1 + SPACE_MARGIN));
}

function fmtBytes(n) {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let v = Math.max(0, Number(n) || 0);
  let u = 0;
  while (v >= 1024 && u < units.length - 1) { v /= 1024; u += 1; }
  return (u === 0 ? String(Math.round(v)) : v.toFixed(1)) + ' ' + units[u];
}

// Symlinks resolved; for a path that does not exist yet, its nearest existing parent is resolved.
function realPath(p) {
  const abs = path.resolve(p);
  try { return fs.realpathSync(abs); } catch (e) { /* not there yet */ }
  const parent = path.dirname(abs);
  return parent === abs ? abs : path.join(realPath(parent), path.basename(abs));
}

// True when a and b are the same folder or one lies inside the other.
function pathsOverlap(a, b) {
  const within = (outer, inner) => {
    const rel = path.relative(outer, inner);
    return rel === '' || (rel !== '..' && !rel.startsWith('..' + path.sep) && !path.isAbsolute(rel));
  };
  return within(a, b) || within(b, a);
}

// The excluded paths (resolved) that p equals, holds or lies inside.
function isExcluded(p, resolvedExclude) {
  if (!resolvedExclude.length) return false;
  const real = realPath(p);
  return resolvedExclude.some((x) => pathsOverlap(real, x));
}

// Free bytes an unprivileged user can write on the filesystem that holds dir.
// fs.statfsSync exists from Node 18.15; without it (or when it fails) free is null and the
// check is skipped with the reason, never guessed.
function freeSpace(dir, statfs = fs.statfsSync) {
  if (typeof statfs !== 'function') {
    return { free: null, reason: `fs.statfsSync is not available in Node ${process.versions.node} (needs 18.15 or newer)` };
  }
  try {
    const s = statfs(dir);
    const free = Number(s.bavail) * Number(s.bsize);
    if (!Number.isFinite(free) || free < 0) return { free: null, reason: `statfs ${dir} returned no usable numbers` };
    return { free, reason: null };
  } catch (e) {
    return { free: null, reason: `statfs ${dir} failed: ${e.code || e.message}` };
  }
}

// reserved = bytes other renders running now on the same disk still have to write.
function spaceVerdict({ needed, free, reserved = 0 }) {
  if (free === null || free === undefined) return { ok: true, skipped: true, needed, free: null, reserved, available: null };
  const available = Math.max(0, free - reserved);
  return { ok: needed <= available, skipped: false, needed, free, reserved, available };
}

function spaceMessage({ needed, free, reserved = 0, frames, width, height, dir, reclaimable = 0 }) {
  return [
    `not enough disk space for the PNG frames in ${dir}`,
    `  need about ${fmtBytes(needed)}: ${frames} frame${frames === 1 ? '' : 's'} x ${width}x${height} px x ${PNG_BYTES_PER_PIXEL} bytes/px + ${Math.round(SPACE_MARGIN * 100)}% margin`,
    `  free on that disk: ${fmtBytes(free)}` +
      (reserved > 0 ? `; other renders running now still have to write about ${fmtBytes(reserved)} there` : ''),
    'do one of these:',
    '  --frames-dir <folder on a disk with more free space> (the frames are kept there)',
    '  free some space' +
      (reclaimable > 0 ? ` (--clean-stale deletes ${fmtBytes(reclaimable)} of ${FRAMES_PREFIX}* folders older than ${STALE_AGE_HOURS} h)` : '') +
      (reserved > 0 ? ' or wait for the other render to finish' : ''),
    '  render a shorter range with --start <s> --duration <s> (or --preview for 8 frames)',
    '  --no-space-check skips this check (the render may then fail with "Unable to capture screenshot")',
  ].join('\n');
}

function isPidAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try { process.kill(pid, 0); return true; } catch (e) { return e.code === 'EPERM'; }
}

function readRenderMarker(dir) {
  try {
    const m = JSON.parse(fs.readFileSync(path.join(dir, RENDER_MARKER), 'utf8'));
    return m && typeof m === 'object' ? m : null;
  } catch (e) { return null; }
}

// Marks a --frames-dir folder as the user's: --clean-stale never deletes a folder holding this file.
function writeUserFramesMarker(dir) {
  try {
    fs.writeFileSync(path.join(dir, USER_FRAMES_MARKER), 'Frames kept by tools/render_html.cjs --frames-dir; --clean-stale never deletes this folder.\n');
  } catch (e) { warn(`could not write ${USER_FRAMES_MARKER} in ${dir}: ${e.code || e.message}`); }
}

// Creates a --frames-dir folder, marks it as the user's and removes the frames an earlier render left in it.
function prepareUserFramesDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
  writeUserFramesMarker(dir);
  for (const f of fs.readdirSync(dir)) {
    if (RENDER_FILE.test(f)) fs.unlinkSync(path.join(dir, f));
  }
}

// Why dir is not one of this tool's own temp frames folders, or null when it is: named like
// fs.mkdtempSync output and holding nothing but files a render writes (frames, previews, the
// render marker). A --frames-dir folder, a subfolder, a link or any other file keeps it.
function notOwnTempReason(dir) {
  if (!TEMP_DIR_NAME.test(path.basename(dir))) return `not named like a temp folder this tool creates (${FRAMES_PREFIX}XXXXXX)`;
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return `unreadable (${e.code || e.message})`; }
  for (const e of entries) {
    if (e.name === USER_FRAMES_MARKER) return 'a --frames-dir folder';
    if (!e.isFile()) return `holds ${e.isDirectory() ? 'a folder' : 'an entry that is not a file'} (${e.name})`;
    if (e.name !== RENDER_MARKER && !RENDER_FILE.test(e.name)) return `holds a file a render does not write (${e.name})`;
  }
  return null;
}

function writeRenderMarker(dir, bytes) {
  try {
    fs.writeFileSync(path.join(dir, RENDER_MARKER), JSON.stringify({ pid: process.pid, bytes: Math.max(0, Math.round(bytes || 0)) }) + '\n');
  } catch (e) { /* the marker only helps other renders plan; never fail a render over it */ }
}

// Total size of the regular files under p; symlinks are not followed, unreadable entries count 0.
function dirBytes(p) {
  let entries;
  try { entries = fs.readdirSync(p, { withFileTypes: true }); } catch (e) { return 0; }
  let total = 0;
  for (const e of entries) {
    const full = path.join(p, e.name);
    try {
      if (e.isDirectory()) total += dirBytes(full);
      else total += fs.lstatSync(full).size;
    } catch (err) { /* vanished while counting */ }
  }
  return total;
}

// Every kosif-frames-* directory directly in tmpDir that this user owns (symlinks, plain files
// and other users' folders are skipped). live = its marker names a process that still runs.
function listFrameDirs(tmpDir, { now = Date.now(), isAlive = isPidAlive } = {}) {
  let names;
  try { names = fs.readdirSync(tmpDir); } catch (e) { return []; }
  const uid = typeof process.getuid === 'function' ? process.getuid() : null;
  const out = [];
  for (const name of names.sort()) {
    if (!name.startsWith(FRAMES_PREFIX)) continue;
    const full = path.join(tmpDir, name);
    let st;
    try { st = fs.lstatSync(full); } catch (e) { continue; }
    if (!st.isDirectory()) continue;
    if (uid !== null && st.uid !== uid) continue;
    const marker = readRenderMarker(full);
    const pid = marker && Number.isInteger(marker.pid) ? marker.pid : null;
    out.push({
      path: full, name, mtimeMs: st.mtimeMs, ageMs: now - st.mtimeMs, dev: st.dev, pid,
      live: pid !== null && (pid === process.pid || isAlive(pid)),
      reservedBytes: marker && Number.isFinite(Number(marker.bytes)) ? Math.max(0, Number(marker.bytes)) : 0,
    });
  }
  return out;
}

// This tool's own temp folders (see notOwnTempReason) not modified for maxAgeMs (default 6 h),
// whose render is not running, minus any folder that equals, holds or lies inside an excluded
// path (the folder this render uses). Oldest first, with their sizes.
function findStaleFrameDirs({ tmpDir = os.tmpdir(), now = Date.now(), maxAgeMs = STALE_AGE_HOURS * 3600 * 1000,
  exclude = [], isAlive = isPidAlive } = {}) {
  const skip = exclude.filter(Boolean).map(realPath);
  return listFrameDirs(tmpDir, { now, isAlive })
    .filter((d) => d.ageMs > maxAgeMs && !d.live && !isExcluded(d.path, skip) && notOwnTempReason(d.path) === null)
    .map((d) => ({ ...d, bytes: dirBytes(d.path) }))
    .sort((a, b) => a.mtimeMs - b.mtimeMs || a.name.localeCompare(b.name));
}

// Deletes the given folders (normally findStaleFrameDirs' result). Re-checks each one: it must
// still be a real directory that is one of this tool's own temp folders and neither equal to,
// nor holding, nor inside an excluded path. Returns what was removed.
function removeStaleFrameDirs(dirs, { exclude = [] } = {}) {
  const skip = exclude.filter(Boolean).map(realPath);
  const removed = [];
  for (const d of dirs) {
    let st;
    try { st = fs.lstatSync(d.path); } catch (e) { continue; }
    if (!st.isDirectory() || isExcluded(d.path, skip) || notOwnTempReason(d.path) !== null) continue;
    try { fs.rmSync(d.path, { recursive: true, force: true }); removed.push(d); }
    catch (e) { warn(`could not remove ${d.path}: ${e.code || e.message}`); }
  }
  return removed;
}

// Bytes that other renders running now (live marker, same filesystem) have still to write.
function reservedByOtherRenders({ tmpDir = os.tmpdir(), dev = null, exclude = [], isAlive = isPidAlive } = {}) {
  const skip = new Set(exclude.filter(Boolean).map(realPath));
  let total = 0;
  for (const d of listFrameDirs(tmpDir, { isAlive })) {
    if (!d.live || d.pid === process.pid || skip.has(realPath(d.path))) continue;
    if (dev !== null && d.dev !== dev) continue;
    total += Math.max(0, d.reservedBytes - dirBytes(d.path));
  }
  return total;
}

// Lists (or with clean, deletes) stale temp frame folders. Returns the bytes still reclaimable.
function reportStaleFrameDirs({ clean, exclude }) {
  const tmpDir = os.tmpdir();
  const stale = findStaleFrameDirs({ tmpDir, exclude });
  const hours = (d) => (d.ageMs / 3600000).toFixed(1) + ' h old';
  if (clean) {
    const removed = removeStaleFrameDirs(stale, { exclude });
    for (const d of removed) log(`removed stale ${d.path} (${fmtBytes(d.bytes)}, ${hours(d)})`);
    log(`--clean-stale: ${removed.length ? `freed about ${fmtBytes(removed.reduce((s, d) => s + d.bytes, 0))}` : `no temp frames folder of this tool (${FRAMES_PREFIX}XXXXXX) older than ${STALE_AGE_HOURS} h in ${tmpDir}`}`);
    return stale.filter((d) => !removed.includes(d)).reduce((s, d) => s + d.bytes, 0);
  }
  if (!stale.length) return 0;
  const total = stale.reduce((s, d) => s + d.bytes, 0);
  warn(`${stale.length} stale ${FRAMES_PREFIX}* folder${stale.length === 1 ? '' : 's'} older than ${STALE_AGE_HOURS} h in ${tmpDir} hold ${fmtBytes(total)} (killed renders or --keep-frames):`);
  for (const d of stale.slice(0, 20)) warn(`  ${d.path}  ${fmtBytes(d.bytes)}  ${hours(d)}`);
  if (stale.length > 20) warn(`  ... and ${stale.length - 20} more`);
  warn('  add --clean-stale to delete exactly these folders before rendering');
  return total;
}

// Runs cleanup(signal) on SIGINT/SIGTERM/SIGHUP, then exits 130/143/129. The finally block of
// main() does not run when a signal ends the process, so temp frames would otherwise stay
// behind. Returns a function that removes the handlers again.
function installSignalCleanup(cleanup, { exit = (code) => process.exit(code) } = {}) {
  const handlers = Object.keys(SIGNAL_EXIT).map((sig) => {
    const handler = () => {
      try { cleanup(sig); } catch (e) { warn(`${sig}: cleanup failed: ${e.message || e}`); }
      exit(SIGNAL_EXIT[sig]);
    };
    process.on(sig, handler);
    return [sig, handler];
  });
  return () => { for (const [sig, handler] of handlers) process.removeListener(sig, handler); };
}

// ------------------------------------------------------------------ browser

async function openBrowser(playwright, opts) {
  const args = COMMON_FLAGS.slice();
  if (opts.isFile) args.push('--allow-file-access-from-files');
  if (opts.virtual) args.push(...BEGIN_FRAME_FLAGS);
  const browser = await playwright.chromium.launch({ headless: true, args });
  const context = await browser.newContext({
    viewport: { width: opts.width, height: opts.height },
    deviceScaleFactor: opts.scale,
    reducedMotion: 'no-preference',
    colorScheme: 'light',
    locale: 'ar',
    timezoneId: 'UTC',
    ignoreHTTPSErrors: true,
  });
  if (opts.offline) {
    await context.route(/^https?:\/\//i, (route) => route.abort('blockedbyclient'));
  }
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message || e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

  // Flags the page can read before any of its own scripts run.
  await page.addInitScript((mode) => {
    window.__KOSIF_RENDER = true;
    window.__KOSIF_MODE = mode;
  }, opts.virtual ? 'virtual' : 'seek');
  if (opts.seed !== null) {
    await page.addInitScript((s) => {
      // mulberry32 — small seeded PRNG so Math.random is reproducible.
      let a = (s >>> 0) || 1;
      Math.random = function () {
        a = (a + 0x6D2B79F5) | 0;
        let t = Math.imul(a ^ (a >>> 15), 1 | a);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
    }, opts.seed);
  }
  const cdp = await context.newCDPSession(page);
  await cdp.send('Page.enable');
  await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: true }).catch(() => {});
  return { browser, context, page, cdp, errors };
}

async function loadPage(page, url, { timeout, settle }) {
  log(`loading ${url}`);
  await page.goto(url, { waitUntil: 'load', timeout });
  await page.waitForLoadState('networkidle', { timeout: Math.min(timeout, 8000) }).catch(() => {});
  await withTimeout(
    page.evaluate(() => (document.fonts ? document.fonts.ready.then(() => true) : true)),
    15000, 'document.fonts.ready',
  ).catch((e) => warn(e.message));
  await withTimeout(
    page.evaluate(() => (window.__kosifReady ? Promise.resolve(window.__kosifReady).then(() => true) : true)),
    timeout, 'window.__kosifReady',
  ).catch((e) => { throw new Error(`page readiness failed: ${e.message}`); });
  if (settle > 0) await sleep(settle);
  return page.evaluate(() => {
    const k = window.__kosif;
    if (!k || typeof k.seek !== 'function') return null;
    return { duration: Number(k.duration) };
  });
}

// ------------------------------------------------------------------ drivers

// seek driver: the page draws the frame for time t when seek(t) is called,
// then a normal screenshot is taken.
class SeekDriver {
  constructor(page, cdp, { width, height, scale }) {
    this.page = page; this.cdp = cdp; this.name = 'seek';
    // Page.captureScreenshot without a clip returns CSS pixels in headless Chromium and
    // ignores deviceScaleFactor, so --scale 2 gave 1080x1920. An explicit clip with
    // scale captures at device pixels (same pixels as Playwright's own page.screenshot).
    this.clip = { x: 0, y: 0, width, height, scale };
  }
  async goTo(t) {
    await this.page.evaluate((time) => window.__kosif.seek(time), t);
  }
  async capture(file) {
    const { data } = await this.cdp.send('Page.captureScreenshot', {
      format: 'png', fromSurface: true, captureBeyondViewport: false,
      optimizeForSpeed: true, // still lossless PNG, faster zlib level (~6x quicker capture)
      clip: this.clip,
    });
    fs.writeFileSync(file, Buffer.from(data, 'base64'));
  }
}

// virtual driver: the virtual clock is paused after load. Film time t maps to
// frame index round(t*fps); every frame is produced by one BeginFrame whose
// frameTimeTicks is exactly base + (index+1) * interval.
class VirtualDriver {
  constructor(page, cdp, fps) {
    this.page = page; this.cdp = cdp; this.fps = fps; this.name = 'virtual';
    this.interval = 1000 / fps;
    this.produced = 0;   // number of frames produced so far
    this.base = 0;       // renderer TimeTicks (ms) at the moment the clock was paused
    this.lastFile = null;
  }
  async start() {
    await this.cdp.send('Emulation.setVirtualTimePolicy', {
      policy: 'pause', initialVirtualTime: VIRTUAL_EPOCH_SECONDS,
    });
    this.base = monoMs();
  }
  async advance(ms) {
    const expired = new Promise((resolve) => this.cdp.once('Emulation.virtualTimeBudgetExpired', resolve));
    await this.cdp.send('Emulation.setVirtualTimePolicy', { policy: 'advance', budget: ms });
    await withTimeout(expired, 30000, 'virtual time budget');
  }
  async produce(withScreenshot) {
    await this.advance(this.interval);
    const ticks = this.base + (this.produced + 1) * this.interval;
    const params = { frameTimeTicks: ticks, interval: this.interval, noDisplayUpdates: false };
    if (withScreenshot) params.screenshot = { format: 'png' };
    const res = await withTimeout(this.cdp.send('HeadlessExperimental.beginFrame', params), 30000, 'beginFrame');
    this.produced += 1;
    return res;
  }
  frameIndex(t) { return Math.round(t * this.fps); }
  // Produces every frame strictly before t (no screenshots) so that capture()
  // yields the frame at t.
  async goTo(t) {
    const target = this.frameIndex(t);
    if (target < this.produced) throw new Error('virtual mode cannot move backwards in time');
    while (this.produced < target) await this.produce(false);
  }
  async capture(file) {
    let res = await this.produce(true);
    let tries = 0;
    while (!res.screenshotData && !this.lastFile && tries < 3) {
      // nothing was drawn yet: ask for the same frame again
      this.produced -= 1;
      res = await this.produce(true);
      tries += 1;
    }
    if (res.screenshotData) {
      fs.writeFileSync(file, Buffer.from(res.screenshotData, 'base64'));
    } else if (this.lastFile) {
      fs.copyFileSync(this.lastFile, file); // no damage: the frame is identical to the previous one
    } else {
      throw new Error('BeginFrame produced no screenshot');
    }
    this.lastFile = file;
  }
}

// ------------------------------------------------------------------ encoding

// Codecs an MP4 carries as-is: the voice is copied byte for byte, never re-encoded.
const MP4_COPY_AUDIO = new Set(['aac', 'mp3', 'alac']);

function audioCodecOf(file) {
  const r = runTool('ffprobe', ['-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name',
    '-of', 'csv=p=0', file]);
  return r.status === 0 ? String(r.stdout || '').trim().split(/\r?\n/)[0] || null : null;
}

// KOSIF export standard (playbooks/export-standard.md, scripts/export_profile.py):
// H.264 High CRF 17 preset slow, yuv420p converted and tagged as BT.709, MP4 +faststart,
// audio stream-copied when MP4 can hold it (AAC 320k 48 kHz only for WAV/FLAC sources).
function encodeVideo({ framesDir, frames, fps, out, crf, audio, start, width, height, capWidth, capHeight }) {
  const args = ['-y', '-hide_banner', '-loglevel', 'error', '-nostats',
    '-framerate', String(fps), '-i', path.join(framesDir, 'frame_%06d.png')];
  if (audio) {
    if (start > 0) args.push('-ss', String(start));
    args.push('-i', audio);
  }
  const vf = [];
  // Chromium frames are sRGB PNGs; convert with the BT.709 matrix (ffmpeg's default is BT.601,
  // which shifts reds and greens slightly on phones).
  if (capWidth && (capWidth !== width || capHeight !== height)) {
    vf.push(`scale=${width}:${height}:flags=lanczos:out_color_matrix=bt709:out_range=tv`);
  } else {
    vf.push('scale=out_color_matrix=bt709:out_range=tv');
  }
  if (width % 2 || height % 2) {
    warn(`output size ${width}x${height} is odd; padding to even dimensions for yuv420p`);
    vf.push('pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black');
  }
  vf.push('format=yuv420p');
  args.push('-map', '0:v:0');
  if (audio) args.push('-map', '1:a:0');
  args.push('-vf', vf.join(','));
  args.push('-c:v', 'libx264', '-preset', 'slow', '-crf', String(crf), '-profile:v', 'high', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-r', String(fps), '-movflags', '+faststart');
  let audioInfo = null;
  if (audio) {
    const codec = audioCodecOf(audio);
    if (MP4_COPY_AUDIO.has(codec)) {
      // Byte-for-byte copy of the user's audio, trimmed at the last video frame.
      args.push('-c:a', 'copy', '-t', (frames / fps).toFixed(6));
      log(`audio: ${codec} stream-copied (not re-encoded)`);
      audioInfo = { handling: 'copy', codec };
    } else {
      // apad appends silence so -shortest ends exactly at the last video frame;
      // the voice samples themselves are never resampled or retimed.
      args.push('-c:a', 'aac', '-b:a', '320k', '-af', 'apad', '-shortest');
      log(`audio: ${codec || 'unknown'} cannot live in MP4 as-is; AAC 320k (keep your master)`);
      audioInfo = { handling: 'reencoded', codec: codec || null };
    }
  }
  args.push(out);
  const r = runTool('ffmpeg', args);
  if (r.status !== 0) throw new Error('ffmpeg failed:\n' + (r.stderr || r.stdout));
  return { audio: audioInfo };
}

// ------------------------------------------------------------- audio proof
// A stream-copied track must reach the MP4 byte for byte. The proof hashes the packets of the first
// audio stream of the source and of the output without decoding them (ffmpeg -c copy into the md5
// and framemd5 muxers). AAC goes through aac_adtstoasc on both sides, as tools/verify_video.py
// --source-audio does: it strips the 7-byte ADTS headers of a raw .aac source the way the MP4 mux
// does and passes MP4-style AAC through unchanged (the filter refuses every other codec).
// Pure helpers below; tests/test_render_html_audio.mjs exercises them.

function audioHashArgs(file, codec, format) {
  return ['-hide_banner', '-v', 'error', '-nostdin', '-i', file, '-map', '0:a:0', '-c', 'copy',
    ...(codec === 'aac' ? ['-bsf:a', 'aac_adtstoasc'] : []), '-f', format, '-'];
}

function parseMd5(text) {
  const m = /MD5=([0-9a-f]{32})/.exec(String(text || ''));
  return m ? m[1] : null;
}

// framemd5 output -> { tb: [num, den] | null, packets: [{ pts, duration, size, hash }] } (one stream).
// A data line is "stream, dts, pts, duration, size, hash[, side data...]".
function parseFrameMd5(text) {
  let tb = null;
  const packets = [];
  for (const line of String(text || '').split(/\r?\n/)) {
    const tbm = /^#tb 0:\s*(\d+)\/(\d+)/.exec(line);
    if (tbm) { tb = [Number(tbm[1]), Number(tbm[2])]; continue; }
    if (!line || line.startsWith('#')) continue;
    const f = line.split(',').map((s) => s.trim());
    if (f.length < 6 || f[0] !== '0' || !/^[0-9a-f]{32}$/.test(f[5])) continue;
    packets.push({ pts: Number(f[2]), duration: Number(f[3]), size: Number(f[4]), hash: f[5] });
  }
  return { tb, packets };
}

// Seconds at which the last packet ends, or null when the time base or the numbers are missing.
function packetsEndSeconds(hashes) {
  if (!hashes || !hashes.tb || !hashes.packets || !hashes.packets.length) return null;
  const last = hashes.packets[hashes.packets.length - 1];
  const end = (last.pts + last.duration) * hashes.tb[0] / hashes.tb[1];
  return Number.isFinite(end) ? Math.round(end * 1000) / 1000 : null;
}

// Compares two hash sets ({ md5, packets }). verdict: 'match' when the whole-stream MD5s and the packet
// counts are equal, else 'differs'. relation says why: 'identical'; 'prefix' (the output is the first M
// source packets byte for byte: the rest was cut at the last video frame); 'run' (a contiguous run from
// packet `offset`: --start cut the head too); 'changed' (some packet's bytes changed; first_mismatch is
// the 0-based output packet).
function compareAudioPackets(src, out) {
  const n = src.packets.length;
  const m = out.packets.length;
  const res = {
    verdict: 'differs', relation: 'changed', src_md5: src.md5, out_md5: out.md5,
    src_packets: n, out_packets: m, offset: null, cut_before: null, cut_after: null, first_mismatch: null,
    src_end_s: packetsEndSeconds(src), out_end_s: packetsEndSeconds(out),
  };
  if (src.md5 && src.md5 === out.md5 && n === m) {
    return { ...res, verdict: 'match', relation: 'identical', offset: 0, cut_before: 0, cut_after: 0 };
  }
  const sh = src.packets.map((p) => p.hash);
  const oh = out.packets.map((p) => p.hash);
  if (m > 0 && m <= n) {
    for (let k = 0; k + m <= n; k++) {
      if (sh[k] !== oh[0]) continue;
      let j = 1;
      while (j < m && sh[k + j] === oh[j]) j++;
      if (j === m) return { ...res, relation: k === 0 ? 'prefix' : 'run', offset: k, cut_before: k, cut_after: n - k - m };
    }
  }
  // No contiguous run matches: align on the first packet (or at 0) and name the first changed one.
  const k0 = Math.max(0, sh.indexOf(oh[0]));
  let j = 0;
  while (j < m && k0 + j < n && sh[k0 + j] === oh[j]) j++;
  return { ...res, offset: k0, first_mismatch: j < m ? j : null };
}

// The audio_md5= value of the VERIFY line.
function audioMd5Token(proof) {
  if (!proof || proof.verdict === 'none') return 'none';
  if (proof.verdict === 'match') return 'match';
  if (proof.verdict === 'reencoded') return 'reencoded';
  if (proof.verdict === 'differs') return `differs (src ${proof.src_packets} packets, out ${proof.out_packets} packets)`;
  return `unknown (${proof.reason || 'not computed'})`;
}

// Lines for stderr when a copied track is not byte-identical: what was cut or changed, and what to do.
function audioProofWarning(proof, { source, output, filmSeconds, start = 0 } = {}) {
  if (!proof || proof.verdict !== 'differs') return [];
  const span = (a, b) => (a === b ? `packet ${a}` : `packets ${a}-${b}`);
  const lines = [
    `AUDIO NOT BYTE-IDENTICAL TO THE SOURCE: audio_md5=${audioMd5Token(proof)}`,
    `  source md5 ${proof.src_md5 || '?'} (${proof.src_packets} packets${proof.src_end_s !== null ? `, ends at ${proof.src_end_s}s` : ''})${source ? ': ' + source : ''}`,
    `  output md5 ${proof.out_md5 || '?'} (${proof.out_packets} packets${proof.out_end_s !== null ? `, ends at ${proof.out_end_s}s` : ''})${output ? ': ' + output : ''}`,
  ];
  const plural = (k) => `${k} packet${k === 1 ? '' : 's'}`;
  if (proof.relation === 'prefix' || proof.relation === 'run') {
    lines.push(`  every output packet is byte-identical to source ${span(proof.offset + 1, proof.offset + proof.out_packets)}: nothing was re-encoded, packets were only cut.`);
    const why = [];
    if (proof.cut_before > 0) why.push(`${plural(proof.cut_before)} before ${start > 0 ? `--start ${start}s` : 'the first video frame'}`);
    if (proof.cut_after > 0) why.push(`${plural(proof.cut_after)} after the last video frame` +
      (filmSeconds ? ` (the film is ${Number(filmSeconds.toFixed(3))}s${proof.src_end_s !== null ? `, the source audio ends at ${proof.src_end_s}s` : ''})` : ''));
    lines.push(`  cut: ${why.join(' and ') || 'nothing'}. This trim is allowed; to keep every packet, render at least as long as the audio (--duration).`);
  } else {
    lines.push(proof.first_mismatch !== null
      ? `  output packet ${proof.first_mismatch + 1} differs from source packet ${proof.offset + proof.first_mismatch + 1}: the audio BYTES CHANGED, not just cut.`
      : '  the output packets do not line up with the source: the audio BYTES CHANGED, not just cut.');
    lines.push('  re-render from the untouched source file.');
  }
  lines.push('  the render is kept (audio_md5 never fails it). Keep the source as the master, and never re-mux the delivery (ffmpeg -shortest drops the last packet).');
  return lines;
}

function audioPacketHashes(file, codec) {
  const md5 = runTool('ffmpeg', audioHashArgs(file, codec, 'md5'));
  if (md5.status !== 0 || !parseMd5(md5.stdout)) {
    return { error: `ffmpeg could not hash the audio packets of ${file}: ${String(md5.stderr || '').trim().split(/\r?\n/).pop() || 'no MD5 line'}` };
  }
  const frames = runTool('ffmpeg', audioHashArgs(file, codec, 'framemd5'));
  if (frames.status !== 0) return { error: `ffmpeg framemd5 failed on ${file}: ${String(frames.stderr || '').trim().split(/\r?\n/).pop()}` };
  const parsed = parseFrameMd5(frames.stdout);
  return { md5: parseMd5(md5.stdout), tb: parsed.tb, packets: parsed.packets };
}

// The proof for one render: 'reencoded' when the track was encoded, else the packet comparison
// (or 'unknown' with a reason when ffmpeg cannot hash a side). Never throws.
function proveAudio({ audioInfo, source, output }) {
  if (!audioInfo) return { verdict: 'none' };
  if (audioInfo.handling !== 'copy') return { verdict: 'reencoded', codec_in: audioInfo.codec, codec_out: 'aac' };
  try {
    const src = audioPacketHashes(source, audioInfo.codec);
    if (src.error) return { verdict: 'unknown', reason: src.error };
    const out = audioPacketHashes(output, audioInfo.codec);
    if (out.error) return { verdict: 'unknown', reason: out.error };
    return compareAudioPackets(src, out);
  } catch (e) {
    return { verdict: 'unknown', reason: String(e.message || e) };
  }
}

function verifyLine({ problems, probe, audioMd5, out }) {
  return `VERIFY ${problems.length ? 'FAIL' : 'OK'} duration=${probe.duration.toFixed(3)}s fps=${probe.fps} frames=${probe.frames} ` +
    `size=${probe.width}x${probe.height} audio=${probe.audio ? probe.audioCodec : 'none'} audio_md5=${audioMd5} file=${out}`;
}

function writeJsonReport(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
}

function probeVideo(file) {
  const r = runTool('ffprobe', ['-v', 'error', '-show_entries',
    'stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames,duration:format=duration',
    '-of', 'json', file]);
  if (r.status !== 0) throw new Error('ffprobe failed:\n' + r.stderr);
  const info = JSON.parse(r.stdout);
  const video = (info.streams || []).find((s) => s.codec_type === 'video');
  const audio = (info.streams || []).find((s) => s.codec_type === 'audio');
  if (!video) throw new Error('ffprobe found no video stream');
  let frames = Number(video.nb_frames);
  if (!Number.isFinite(frames) || frames <= 0) {
    const c = runTool('ffprobe', ['-v', 'error', '-count_frames', '-select_streams', 'v:0',
      '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', file]);
    frames = Number((c.stdout || '').trim());
  }
  const [num, den] = String(video.r_frame_rate || '0/1').split('/').map(Number);
  const fps = den ? num / den : 0;
  const duration = Number(video.duration) || Number(info.format && info.format.duration) || 0;
  return {
    width: video.width, height: video.height, fps, frames, duration,
    formatDuration: Number(info.format && info.format.duration) || 0,
    audio: !!audio, audioCodec: audio ? audio.codec_name : null,
  };
}

function verifyProbe(probe, want) {
  const problems = [];
  const durTol = 1 / want.fps + 0.002;
  if (Math.abs(probe.fps - want.fps) > 0.01) problems.push(`fps ${probe.fps} != ${want.fps}`);
  if (Math.abs(probe.frames - want.frames) > 1) problems.push(`frames ${probe.frames} != ${want.frames}`);
  if (Math.abs(probe.duration - want.duration) > durTol) problems.push(`duration ${probe.duration.toFixed(3)} != ${want.duration.toFixed(3)}`);
  if (probe.width !== want.width || probe.height !== want.height) problems.push(`size ${probe.width}x${probe.height} != ${want.width}x${want.height}`);
  if (probe.audio !== want.audio) problems.push(`audio stream ${probe.audio ? 'present' : 'missing'}, expected ${want.audio ? 'present' : 'none'}`);
  return problems;
}

// ---------------------------------------------------------------- preview

// Grid shape for n tiles: one row up to 4, then 4, 6 or 8 columns.
function gridLayout(n) {
  if (!(n >= 1)) return { cols: 0, rows: 0 };
  const cols = n <= 4 ? n : n <= 8 ? 4 : n <= 24 ? 6 : 8;
  return { cols, rows: Math.ceil(n / cols) };
}

// 3x5 pixel glyphs for tile labels when ffmpeg has no drawtext (built without libfreetype) or
// drawtext finds no font: drawbox is part of every ffmpeg, so the times are always printed.
const BITMAP_FONT = {
  0: ['111', '101', '101', '101', '111'],
  1: ['010', '110', '010', '010', '111'],
  2: ['111', '001', '111', '100', '111'],
  3: ['111', '001', '111', '001', '111'],
  4: ['101', '101', '111', '001', '001'],
  5: ['111', '100', '111', '001', '111'],
  6: ['111', '100', '111', '101', '111'],
  7: ['111', '001', '001', '001', '001'],
  8: ['111', '101', '111', '101', '111'],
  9: ['111', '101', '111', '001', '111'],
  '.': ['000', '000', '000', '000', '010'],
  s: ['011', '100', '010', '001', '110'],
  '#': ['01010', '11111', '01010', '11111', '01010'],
  ' ': ['000', '000', '000', '000', '000'],
};

// drawbox filters that print text (digits, '.', 's', '#', space; anything else is a space) at x,y
// with px-sized pixels on a dark box. One blank column between glyphs; runs of lit pixels in a glyph
// row become one box.
function bitmapLabelFilters(text, { x = 10, y = 10, px = 3 } = {}) {
  const glyphs = [...String(text)].map((ch) => BITMAP_FONT[ch] || BITMAP_FONT[' ']);
  const pad = px * 2;
  const cols = Math.max(1, glyphs.reduce((s, g) => s + g[0].length + 1, 0) - 1);
  const out = [`drawbox=x=${x - pad}:y=${y - pad}:w=${cols * px + 2 * pad}:h=${5 * px + 2 * pad}:color=black@0.6:t=fill`];
  let left = 0;
  for (const glyph of glyphs) {
    glyph.forEach((row, r) => {
      for (let c = 0; c < row.length; c++) {
        if (row[c] !== '1') continue;
        let run = 1;
        while (c + run < row.length && row[c + run] === '1') run++;
        out.push(`drawbox=x=${x + (left + c) * px}:y=${y + r * px}:w=${run * px}:h=${px}:color=white:t=fill`);
        c += run - 1;
      }
    });
    left += glyph[0].length + 1;
  }
  return out;
}

// The label filters for one tile: drawtext when available, else the bitmap digits. The label text
// only ever holds digits, '.', 's', '#' and spaces, so it needs no drawtext escaping.
function labelFilters(text, drawtext) {
  if (drawtext) return [`drawtext=text='${text}':fontcolor=white:fontsize=20:box=1:boxcolor=black@0.6:boxborderw=8:x=10:y=10`];
  return bitmapLabelFilters(text, { x: 12, y: 12, px: 3 });
}

const TILE_SCALE = 'scale=480:540:force_original_aspect_ratio=decrease';

// Tiles picks [{ file, label }] into one PNG (preview contact sheet and --stills grid). The tiles go to
// workDir as preview_tile_NN.png; every tile is labelled after scaling, so labels read the same at any aspect.
function composeGrid({ workDir, picks, out, drawtext = ffmpegHasFilter('drawtext') }) {
  const { cols, rows } = gridLayout(picks.length);
  let useDrawtext = drawtext;
  picks.forEach(({ file, label }, k) => {
    const tile = path.join(workDir, `preview_tile_${String(k).padStart(2, '0')}.png`);
    const run = (withDrawtext) => runTool('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-i', file,
      '-vf', [TILE_SCALE, ...labelFilters(label, withDrawtext)].join(','), '-update', '1', tile]);
    let r = run(useDrawtext);
    if (r.status !== 0 && useDrawtext) {
      warn(`drawtext failed (${String(r.stderr || '').trim().split(/\r?\n/).pop()}); labelling with built-in digits`);
      useDrawtext = false;
      r = run(false);
    }
    if (r.status !== 0) throw new Error('ffmpeg (grid tile) failed:\n' + r.stderr);
  });
  const r = runTool('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error',
    '-framerate', '1', '-i', path.join(workDir, 'preview_tile_%02d.png'),
    '-vf', `tile=${cols}x${rows}:padding=8:margin=12:color=0x101418`, '-frames:v', '1', '-update', '1', out]);
  if (r.status !== 0) throw new Error('ffmpeg (grid) failed:\n' + r.stderr);
  return { out, cols, rows, labels: useDrawtext ? 'drawtext' : 'bitmap' };
}

// ----------------------------------------------------------------- stills

// "0,1.5,2.25s,1:04" -> [0, 1.5, 2.25, 64]: film times in seconds (an optional trailing "s") or m:ss(.fff),
// read to the millisecond, de-duplicated and sorted (the virtual driver cannot move back in time).
function parseStillTimes(spec) {
  const example = 'e.g. --stills 0,1.5,2.25s,1:04';
  if (spec === undefined || spec === null || spec === true) throw new UsageError(`--stills needs a comma-separated list of times in seconds (${example})`);
  const parts = String(spec).split(',').map((s) => s.trim()).filter((s) => s !== '');
  if (!parts.length) throw new UsageError(`--stills needs at least one time (${example})`);
  const times = [];
  for (const p of parts) {
    const sec = /^(\d+(?:\.\d*)?|\.\d+)s?$/i.exec(p);
    const mss = /^(\d+):([0-5]\d(?:\.\d*)?)$/.exec(p);
    if (!sec && !mss) {
      throw new UsageError(`--stills: "${p}" is not a film time (seconds such as 0, 1.5 or 2.25s, or m:ss such as 1:04; ${example})`);
    }
    const t = Math.round((sec ? Number(sec[1]) : Number(mss[1]) * 60 + Number(mss[2])) * 1000) / 1000;
    if (!times.includes(t)) times.push(t);
  }
  if (times.length > MAX_STILLS) throw new UsageError(`--stills takes at most ${MAX_STILLS} times, got ${times.length}`);
  return times.sort((a, b) => a - b);
}

function stillName(t) { return `still_${t.toFixed(3)}.png`; }

// The capture plan for --stills: per time, the file, the frame index at fps and the time actually drawn
// (seek mode: exactly t; virtual mode: the nearest frame, index / fps).
function planStills(times, { fps, driver, dir }) {
  return times.map((t) => {
    const frame = Math.round(t * fps);
    const tActual = driver === 'virtual' ? Math.round((frame / fps) * 1000) / 1000 : t;
    const label = `${tActual.toFixed(3)}s` + (driver === 'virtual' ? ` #${frame}` : '');
    return { t, t_actual: tActual, frame, file: path.join(dir, stillName(t)), label };
  });
}

// Seeks the driver to each pick's time and captures it (the preview and --stills share this). Picks are
// in time order; one that lands on the same virtual frame as the pick before it is a copy of that file.
async function capturePicks(driver, picks, { capWidth, capHeight, describe }) {
  let prev = null;
  for (let k = 0; k < picks.length; k++) {
    const p = picks[k];
    if (prev && driver.name === 'virtual' && driver.frameIndex(p.t) === driver.frameIndex(prev.t)) {
      fs.copyFileSync(prev.file, p.file);
    } else {
      await driver.goTo(p.t);
      await driver.capture(p.file);
      if (k === 0) checkFrameSize(p.file, capWidth, capHeight);
    }
    log(describe(p, k, picks.length));
    prev = p;
  }
}

// -------------------------------------------------------------------- main

// Any aspect -> even pixel size. Same presets, names (Arabic included) and pixel rule as
// PRESETS/NAMES in tools/aspects.py; tests/test_render_html.mjs checks that they stay in step.
const ASPECT_PRESETS = { '9:16': [1080, 1920], '16:9': [1920, 1080], '1:1': [1080, 1080], '4:5': [1080, 1350] };
const ASPECT_NAMES = {
  reel: '9:16', reels: '9:16', story: '9:16', stories: '9:16', tiktok: '9:16', shorts: '9:16',
  vertical: '9:16', 'portrait-full': '9:16', 'ريلز': '9:16', 'ستوري': '9:16', 'طولي': '9:16', 'تيك توك': '9:16',
  youtube: '16:9', landscape: '16:9', horizontal: '16:9', hd: '16:9', 'عرضي': '16:9', 'يوتيوب': '16:9',
  square: '1:1', 'مربع': '1:1',
  feed: '4:5', portrait: '4:5', instagram: '4:5', 'انستجرام': '4:5',
  classic: '4:3', tv: '4:3', 'كلاسيكي': '4:3',
  cinema: '2.39:1', scope: '2.39:1', anamorphic: '2.39:1', 'سينما': '2.39:1', 'سينمائي': '2.39:1',
  ultrawide: '21:9', wide: '21:9', flat: '1.85:1',
};
function aspectSize(spec) {
  const even = (n) => { n = Math.round(n); return n % 2 ? n + 1 : n; };
  let s = spec.trim().toLowerCase();
  s = ASPECT_NAMES[s] || s;
  if (ASPECT_PRESETS[s]) return { w: ASPECT_PRESETS[s][0], h: ASPECT_PRESETS[s][1] };
  let m = s.match(/^(\d{2,5})\s*[x×*]\s*(\d{2,5})$/);
  if (m) return { w: even(+m[1]), h: even(+m[2]) };
  m = s.match(/^(\d+(?:\.\d+)?)\s*[:/]\s*(\d+(?:\.\d+)?)$/);
  if (!m) return null;
  const r = +m[1] / +m[2];
  if (!(r >= 0.2 && r <= 5)) return null;
  if (r >= 9 / 16 && r <= 16 / 9) return r >= 1 ? { w: even(1080 * r), h: 1080 } : { w: 1080, h: even(1080 / r) };
  return r > 1 ? { w: 1920, h: even(1920 / r) } : { w: even(1920 * r), h: 1920 };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { usage(); return 0; }
  checkArgs(args);
  if (!args.in) throw new UsageError('--in <file.html|http URL> is required');
  const stills = args.stills === undefined ? null : parseStillTimes(args.stills);
  if (args['stills-dir'] !== undefined && !stills) throw new UsageError('--stills-dir needs --stills <t1,t2,...>');
  if (stills && args.preview) throw new UsageError('--stills and --preview are separate modes: use one of them');
  if (!args.out && !(stills && args['stills-dir'] !== undefined)) {
    throw new UsageError(`--out <out.mp4> is required${stills ? ' (or give --stills-dir <dir>)' : ''}`);
  }

  const fromAspect = args.aspect ? aspectSize(String(args.aspect)) : null;
  if (args.aspect && !fromAspect) throw new UsageError(`--aspect ${args.aspect} is not a readable ratio (W:H, WxH or a name)`);
  const width = numberOpt(args, 'width', fromAspect ? fromAspect.w : DEFAULTS.width, { integer: true, min: 2 });
  const height = numberOpt(args, 'height', fromAspect ? fromAspect.h : DEFAULTS.height, { integer: true, min: 2 });
  const fps = numberOpt(args, 'fps', DEFAULTS.fps, { min: 1 });
  const start = numberOpt(args, 'start', DEFAULTS.start, { min: 0 });
  const crf = numberOpt(args, 'crf', DEFAULTS.crf, { integer: true, min: 0 });
  const scale = numberOpt(args, 'scale', DEFAULTS.scale, { min: 0.1 });
  const timeout = numberOpt(args, 'timeout', DEFAULTS.timeout, { integer: true, min: 1 });
  const settle = numberOpt(args, 'settle', DEFAULTS.settle, { integer: true, min: 0 });
  let duration = args.duration === undefined ? null : numberOpt(args, 'duration', null, { min: 0 });
  const seed = args.seed === undefined ? null : numberOpt(args, 'seed', null, { integer: true });
  const mode = args.mode === undefined ? 'auto' : String(args.mode);
  if (!['auto', 'seek', 'virtual'].includes(mode)) throw new UsageError('--mode must be seek or virtual');
  const preview = !!args.preview;
  const offline = !!args.offline;
  const keepFrames = !!args['keep-frames'];
  const noSpaceCheck = !!args['no-space-check'];
  const cleanStale = !!args['clean-stale'];
  const audio = args.audio && args.audio !== true ? path.resolve(String(args.audio)) : null;
  if (audio && !fs.existsSync(audio)) throw new UsageError(`--audio file not found: ${audio}`);
  if (audio && (preview || stills)) warn(`--audio is ignored in --${preview ? 'preview' : 'stills'} mode`);
  if (stills && args.start !== undefined) warn('--start is ignored with --stills: the --stills times are film times');
  const reportPath = args.report ? path.resolve(String(args.report)) : null;

  const outPath = args.out ? path.resolve(String(args.out)) : null;
  const stillsDir = !stills ? null : args['stills-dir'] !== undefined ? path.resolve(String(args['stills-dir']))
    : path.join(path.dirname(outPath), path.basename(outPath, path.extname(outPath)) + '_stills');
  const outWidth = Math.round(width * scale);
  const outHeight = Math.round(height * scale);
  // Chromium ignores a device scale below 1 for screenshots: capture at 1x and let ffmpeg downscale.
  const capScale = Math.max(1, scale), capWidth = Math.round(width * capScale), capHeight = Math.round(height * capScale);

  const input = String(args.in);
  let url;
  let isFile = false;
  if (/^https?:\/\//i.test(input)) { url = input; }
  else {
    const abs = path.resolve(input);
    if (!fs.existsSync(abs)) throw new UsageError(`--in file not found: ${abs}`);
    url = pathToFileURL(abs).href;
    isFile = true;
  }

  // Temp frame folders that killed renders left behind: listed, or deleted with --clean-stale.
  const userFramesDir = args['frames-dir'] && args['frames-dir'] !== true ? path.resolve(String(args['frames-dir'])) : null;
  const reclaimable = reportStaleFrameDirs({ clean: cleanStale, exclude: [userFramesDir] });

  requireTool('ffmpeg');
  requireTool('ffprobe');
  const { playwright, from } = resolvePlaywright();
  log(`playwright: ${from}`);

  let framesDir;
  let tempFrames = false;
  if (userFramesDir) {
    framesDir = userFramesDir;
    prepareUserFramesDir(framesDir);
  } else {
    framesDir = fs.mkdtempSync(path.join(os.tmpdir(), FRAMES_PREFIX));
    tempFrames = true;
    writeRenderMarker(framesDir, 0);
  }
  // A signal ends the process without running the finally block below, so the temp
  // frames are removed here too (SIGKILL cannot be caught: --clean-stale handles those).
  const uninstallSignalCleanup = installSignalCleanup((sig) => {
    if (tempFrames && !keepFrames) {
      fs.rmSync(framesDir, { recursive: true, force: true });
      warn(`${sig}: render stopped, temp frames ${framesDir} removed`);
    } else {
      warn(`${sig}: render stopped, frames kept in ${framesDir}`);
    }
  });

  // Free-space pre-flight, once the frame count is known and before the first frame.
  let spaceChecked = false;
  const checkSpace = (total) => {
    if (spaceChecked || total < 1) return;
    spaceChecked = true;
    const frames = preview ? Math.min(8, total) : total;
    const needed = estimateFrameBytes(frames, capWidth, capHeight);
    if (tempFrames) writeRenderMarker(framesDir, needed); // lets renders started later plan for this one
    if (noSpaceCheck) { log(`disk: frames need about ${fmtBytes(needed)}; space check skipped (--no-space-check)`); return; }
    const { free, reason } = freeSpace(framesDir);
    if (free === null) { warn(`free-space check skipped: ${reason}`); return; }
    let dev = null;
    try { dev = fs.statSync(framesDir).dev; } catch (e) { /* compare nothing */ }
    const reserved = reservedByOtherRenders({ dev, exclude: [framesDir] });
    log(`disk: frames need about ${fmtBytes(needed)}; ${fmtBytes(free)} free` +
      (reserved > 0 ? `, about ${fmtBytes(reserved)} still to be written by other running renders` : ''));
    if (!spaceVerdict({ needed, free, reserved }).ok) {
      throw new DiskSpaceError(spaceMessage({ needed, free, reserved, frames, width: capWidth, height: capHeight, dir: framesDir, reclaimable }));
    }
  };

  const browserOpts = { isFile, width, height, scale: capScale, offline, seed, virtual: mode === 'virtual' };
  let session = null;
  let exitCode = 0;
  try {
    if (outPath) fs.mkdirSync(path.dirname(outPath), { recursive: true });
    if (stills) { fs.mkdirSync(stillsDir, { recursive: true }); checkSpace(stills.length); } // the stills: full-size PNGs
    else if (duration !== null) checkSpace(Math.round(duration * fps)); // known now: fail before Chromium starts
    session = await openBrowser(playwright, browserOpts);
    let hook = await loadPage(session.page, url, { timeout, settle });
    let useVirtual = mode === 'virtual';
    if (mode === 'seek' && !hook) throw new Error('--mode seek requested but the page does not define window.__kosif.seek');
    if (mode === 'auto' && !hook) {
      // No seek hook: relaunch with BeginFrame control and reload under the virtual driver.
      log('no window.__kosif hook found, switching to virtual mode');
      await session.browser.close().catch(() => {});
      session = await openBrowser(playwright, { ...browserOpts, virtual: true });
      hook = await loadPage(session.page, url, { timeout, settle });
      useVirtual = true;
    }
    const { page, cdp, errors } = session;

    if (duration === null && hook && Number.isFinite(hook.duration) && hook.duration > 0) duration = hook.duration;
    if (duration === null && !stills) throw new UsageError('--duration is required (page has no window.__kosif.duration)');
    const total = stills ? stills.length : Math.round(duration * fps);
    if (total < 1) throw new UsageError('duration * fps must be at least one frame');

    if (useVirtual && capScale > 1) {
      // HeadlessExperimental.beginFrame screenshots are always taken at CSS pixels.
      throw new UsageError(`--scale ${scale} only works in seek mode; in virtual mode use --width ${outWidth} --height ${outHeight} instead`);
    }
    checkSpace(total);
    let driver;
    if (useVirtual) { driver = new VirtualDriver(page, cdp, fps); await driver.start(); }
    else driver = new SeekDriver(page, cdp, { width, height, scale: capScale });

    if (stills) {
      log(`mode: ${driver.name} | ${width}x${height} css px, capture ${capWidth}x${capHeight} | ${stills.length} still${stills.length === 1 ? '' : 's'} -> ${stillsDir}` +
        (driver.name === 'virtual' ? ` | virtual time: nearest frame at ${fps} fps` : ' | seek: exact times'));
      if (duration !== null) {
        const late = stills.filter((t) => t > duration);
        if (late.length) warn(`--stills ${late.join(', ')} lie${late.length === 1 ? 's' : ''} past the film's duration (${duration}s); the page draws whatever it draws there`);
      }
      const picks = planStills(stills, { fps, driver: driver.name, dir: stillsDir });
      await capturePicks(driver, picks, {
        capWidth, capHeight,
        describe: (p, k, n) => `still ${k + 1}/${n}: t=${fmtTime(p.t)}` +
          (driver.name === 'virtual' ? ` -> frame ${p.frame} (t=${fmtTime(p.t_actual)})` : '') + ` -> ${p.file}`,
      });
      const gridPath = path.join(stillsDir, 'stills_grid.png');
      const grid = composeGrid({ workDir: framesDir, picks, out: gridPath });
      const manifest = {
        schema: 'kosif.render_html.stills.v1', mode: 'stills', in: url, driver: driver.name, fps,
        width: capWidth, height: capHeight, dir: stillsDir, grid: gridPath,
        grid_layout: { cols: grid.cols, rows: grid.rows }, labels: grid.labels,
        film_duration: duration,
        stills: picks.map((p) => ({ t: p.t, t_actual: p.t_actual, frame: p.frame, file: p.file, label: p.label })),
        page_errors: errors.slice(0, 10),
      };
      writeJsonReport(path.join(stillsDir, 'stills.json'), manifest);
      if (reportPath) writeJsonReport(reportPath, manifest);
      log(`stills grid: ${gridPath} (${picks.length} still${picks.length === 1 ? '' : 's'}, ${grid.cols}x${grid.rows}, labels: ${grid.labels === 'drawtext' ? 'drawtext' : 'built-in digits'}); manifest ${path.join(stillsDir, 'stills.json')}`);
      log('STILLS ' + gridPath);
    } else {
      log(`mode: ${driver.name} | ${width}x${height} css px, scale ${scale} -> ${outWidth}x${outHeight} | ${fps} fps | ${total} frames | start ${fmtTime(start)} | duration ${fmtTime(duration)}`);
      const timeOf = (i) => start + i / fps;

      if (preview) {
        const count = Math.min(8, total);
        const indices = [];
        for (let k = 0; k < count; k++) {
          const idx = count === 1 ? 0 : Math.round((k * (total - 1)) / (count - 1));
          if (!indices.includes(idx)) indices.push(idx);
        }
        const picks = indices.map((idx, k) => {
          const t = timeOf(idx);
          return { t, index: idx, file: path.join(framesDir, `preview_raw_${String(k).padStart(2, '0')}.png`), label: `${t.toFixed(2)}s  #${idx}` };
        });
        await capturePicks(driver, picks, {
          capWidth, capHeight, describe: (p, k, n) => `preview ${k + 1}/${n}: frame ${p.index} (t=${fmtTime(p.t)})`,
        });
        const sheet = path.join(path.dirname(outPath), path.basename(outPath, path.extname(outPath)) + '_preview.png');
        const res = composeGrid({ workDir: framesDir, picks, out: sheet });
        log(`contact sheet: ${res.out} (${picks.length} frames, labels: ${res.labels === 'drawtext' ? 'drawtext' : 'built-in digits'})`);
        if (reportPath) {
          writeJsonReport(reportPath, {
            schema: 'kosif.render_html.report.v1', mode: 'preview', in: url, driver: driver.name, fps, sheet: res.out,
            frames: picks.map((p) => ({ t: p.t, frame: p.index })), page_errors: errors.slice(0, 10),
          });
        }
        log('PREVIEW ' + res.out);
      } else {
        const t0 = Date.now();
        for (let i = 0; i < total; i++) {
          const t = timeOf(i);
          await driver.goTo(t);
          const file = path.join(framesDir, frameName(i));
          await driver.capture(file);
          if (i === 0) checkFrameSize(file, capWidth, capHeight);
          if ((i + 1) % 30 === 0 || i + 1 === total) {
            const elapsed = (Date.now() - t0) / 1000;
            log(`frame ${i + 1}/${total} (t=${fmtTime(t)}) ${elapsed.toFixed(1)}s elapsed`);
          }
        }
        log(`encoding ${total} frames -> ${outPath}`);
        const enc = encodeVideo({ framesDir, frames: total, fps, out: outPath, crf, audio, start, width: outWidth, height: outHeight, capWidth, capHeight });
        const probe = probeVideo(outPath);
        const want = { fps, frames: total, duration: total / fps, width: outWidth + (outWidth % 2), height: outHeight + (outHeight % 2), audio: !!audio };
        const problems = verifyProbe(probe, want);
        const proof = proveAudio({ audioInfo: enc.audio, source: audio, output: outPath });
        const audioMd5 = audioMd5Token(proof);
        const line = verifyLine({ problems, probe, audioMd5, out: outPath });
        log(line);
        if (problems.length) {
          warn('verification problems: ' + problems.join('; '));
          exitCode = EXIT_VERIFY;
        }
        if (proof.verdict === 'differs') {
          for (const l of audioProofWarning(proof, { source: audio, output: outPath, filmSeconds: total / fps, start })) warn(l);
        } else if (proof.verdict === 'unknown') {
          warn(`audio packet proof not computed: ${proof.reason}`);
        }
        if (reportPath) {
          writeJsonReport(reportPath, {
            schema: 'kosif.render_html.report.v1', mode: 'render', in: url, out: outPath, driver: driver.name,
            verify: {
              ok: problems.length === 0, problems, duration: probe.duration, fps: probe.fps, frames: probe.frames,
              width: probe.width, height: probe.height, audio: probe.audio ? probe.audioCodec : null,
            },
            audio_md5: audioMd5,
            audio: audio ? { source: audio, handling: enc.audio.handling, codec: enc.audio.codec, proof } : null,
            verify_line: line,
            page_errors: errors.slice(0, 10),
          });
          log(`report: ${reportPath}`);
        }
      }
    }

    if (errors.length) {
      warn(`page reported ${errors.length} console/page error(s):`);
      for (const e of errors.slice(0, 10)) warn('  ' + e);
    }
  } finally {
    if (session) await session.browser.close().catch(() => {});
    if (tempFrames && !keepFrames) fs.rmSync(framesDir, { recursive: true, force: true });
    else log(`frames kept in ${framesDir}`);
    uninstallSignalCleanup();
  }
  return exitCode;
}

if (require.main === module) {
  main().then((code) => { process.exitCode = code; }).catch((err) => {
    if (err instanceof UsageError) {
      warn(err.message);
      usage(process.stderr);
      process.exitCode = EXIT_USAGE;
    } else if (err instanceof DiskSpaceError) {
      warn(err.message);
      process.exitCode = EXIT_RENDER;
    } else {
      warn(err && err.stack ? err.stack : String(err));
      process.exitCode = EXIT_RENDER;
    }
  });
} else {
  // Loaded with require() (tests): expose the pure helpers, render nothing.
  module.exports = {
    parseArgs, checkArgs, aspectSize, ASPECT_PRESETS, ASPECT_NAMES, UsageError,
    // disk guard
    estimateFrameBytes, fmtBytes, freeSpace, spaceVerdict, spaceMessage, isPidAlive, dirBytes,
    listFrameDirs, findStaleFrameDirs, removeStaleFrameDirs, reservedByOtherRenders, installSignalCleanup,
    realPath, pathsOverlap, notOwnTempReason, prepareUserFramesDir,
    FRAMES_PREFIX, RENDER_MARKER, USER_FRAMES_MARKER, PNG_BYTES_PER_PIXEL, SPACE_MARGIN, STALE_AGE_HOURS, SIGNAL_EXIT, DiskSpaceError,
    // --stills and the preview grid
    parseStillTimes, stillName, planStills, gridLayout, bitmapLabelFilters, labelFilters, composeGrid, BITMAP_FONT, MAX_STILLS,
    // audio proof (needs ffmpeg only for audioPacketHashes/proveAudio/encodeVideo)
    audioHashArgs, parseMd5, parseFrameMd5, packetsEndSeconds, compareAudioPackets, audioMd5Token, audioProofWarning,
    audioPacketHashes, proveAudio, verifyLine, encodeVideo, probeVideo, MP4_COPY_AUDIO,
  };
}
