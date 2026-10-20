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
 *        [--width 1080] [--height 1920] [--fps 30] [--duration <s>] [--start 0]
 *        [--audio <file>] [--mode seek|virtual] [--preview] [--frames-dir <dir>]
 *        [--crf 18] [--scale 1] [--seed <n>] [--offline] [--keep-frames]
 *        [--timeout <ms>] [--settle <ms>]
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
  crf: 18,
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

// ---------------------------------------------------------------- CLI parsing

class UsageError extends Error {}

function usage(stream) {
  const text = `
KOSIF render_html — deterministic HTML -> MP4

  node ${require('path').relative(process.cwd(), __filename) || 'render_html.cjs'} --in <file.html|http URL> --out <out.mp4> [options]

Options
  --aspect <spec>     any frame: 9:16, 16:9, 4:5, 21:9, 2.35:1, 1920x816, reel, square, cinema
                      (sets --width/--height; explicit --width/--height still win)
  --width <px>        viewport width in CSS px            (default ${DEFAULTS.width})
  --height <px>       viewport height in CSS px           (default ${DEFAULTS.height})
  --fps <n>           frames per second                   (default ${DEFAULTS.fps})
  --duration <s>      seconds to render (seek mode: defaults to window.__kosif.duration)
  --start <s>         film time of the first frame        (default ${DEFAULTS.start})
  --audio <file>      mux this audio track (AAC 192k, sample timing untouched)
  --mode seek|virtual driver; auto-detected when omitted (seek if window.__kosif exists)
  --preview           render 8 evenly spaced frames into a contact sheet PNG instead of a video,
                      written next to --out as <out name>_preview.png (out/p.mp4 -> out/p_preview.png)
  --frames-dir <dir>  where PNG frames go (kept); default: a temp dir that is deleted
  --keep-frames       keep the temp frames dir
  --crf <n>           libx264 quality, lower = better     (default ${DEFAULTS.crf})
  --scale <n>         device scale factor: output pixels = width*scale x height*scale (default ${DEFAULTS.scale})
  --seed <n>          replace Math.random inside the page with a seeded PRNG
  --offline           abort every http(s) request (system fonts only, fully reproducible)
  --timeout <ms>      page load timeout                   (default ${DEFAULTS.timeout})
  --settle <ms>       extra wall-clock wait after the page is ready (default ${DEFAULTS.settle})
  --help              this text

Exit codes: 0 ok, ${EXIT_USAGE} usage error, ${EXIT_RENDER} render/encode failure, ${EXIT_VERIFY} ffprobe disagrees with the request.
`;
  (stream || process.stdout).write(text.trimStart());
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) { out._.push(a); continue; }
    let key = a.slice(2);
    let val;
    const eq = key.indexOf('=');
    if (eq >= 0) { val = key.slice(eq + 1); key = key.slice(0, eq); }
    else if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) { val = argv[++i]; }
    else { val = true; }
    out[key] = val;
  }
  return out;
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
  constructor(page, cdp) { this.page = page; this.cdp = cdp; this.name = 'seek'; }
  async goTo(t) {
    await this.page.evaluate((time) => window.__kosif.seek(time), t);
  }
  async capture(file) {
    const { data } = await this.cdp.send('Page.captureScreenshot', {
      format: 'png', fromSurface: true, captureBeyondViewport: false,
      optimizeForSpeed: true, // still lossless PNG, faster zlib level (~6x quicker capture)
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

function encodeVideo({ framesDir, fps, out, crf, audio, start, width, height, capWidth, capHeight }) {
  const args = ['-y', '-hide_banner', '-loglevel', 'error', '-nostats',
    '-framerate', String(fps), '-i', path.join(framesDir, 'frame_%06d.png')];
  if (audio) {
    if (start > 0) args.push('-ss', String(start));
    args.push('-i', audio);
  }
  const vf = [];
  if (capWidth && (capWidth !== width || capHeight !== height)) vf.push(`scale=${width}:${height}:flags=lanczos`);
  if (width % 2 || height % 2) {
    warn(`output size ${width}x${height} is odd; padding to even dimensions for yuv420p`);
    vf.push('pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black');
  }
  args.push('-map', '0:v:0');
  if (audio) args.push('-map', '1:a:0');
  if (vf.length) args.push('-vf', vf.join(','));
  args.push('-c:v', 'libx264', '-preset', 'medium', '-crf', String(crf), '-pix_fmt', 'yuv420p',
    '-r', String(fps), '-movflags', '+faststart');
  if (audio) {
    // apad appends silence so -shortest ends exactly at the last video frame;
    // the voice samples themselves are never resampled or retimed.
    args.push('-c:a', 'aac', '-b:a', '192k', '-af', 'apad', '-shortest');
  }
  args.push(out);
  const r = runTool('ffmpeg', args);
  if (r.status !== 0) throw new Error('ffmpeg failed:\n' + (r.stderr || r.stdout));
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

function composeContactSheet({ framesDir, picks, out }) {
  const hasDrawtext = ffmpegHasFilter('drawtext');
  picks.forEach(({ file, t, index }, k) => {
    const tile = path.join(framesDir, `preview_tile_${String(k).padStart(2, '0')}.png`);
    const filters = [];
    if (hasDrawtext) {
      const label = `${t.toFixed(2)}s  #${index}`;
      filters.push(`drawtext=text='${label}':fontcolor=white:fontsize=h/36:box=1:boxcolor=black@0.55:boxborderw=10:x=14:y=14`);
    }
    filters.push('scale=480:540:force_original_aspect_ratio=decrease');
    const r = runTool('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-i', file, '-vf', filters.join(','), '-update', '1', tile]);
    if (r.status !== 0) throw new Error('ffmpeg (preview tile) failed:\n' + r.stderr);
  });
  const r = runTool('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error',
    '-framerate', '1', '-i', path.join(framesDir, 'preview_tile_%02d.png'),
    '-vf', 'tile=4x2:padding=8:margin=12:color=0x101418', '-frames:v', '1', '-update', '1', out]);
  if (r.status !== 0) throw new Error('ffmpeg (contact sheet) failed:\n' + r.stderr);
  return { out, labeled: hasDrawtext };
}

// -------------------------------------------------------------------- main

// Any aspect -> even pixel size; mirrors tools/aspects.py and web/generator.js resolveAspect().
const ASPECT_PRESETS = { '9:16': [1080, 1920], '16:9': [1920, 1080], '1:1': [1080, 1080], '4:5': [1080, 1350] };
const ASPECT_NAMES = { reel: '9:16', story: '9:16', tiktok: '9:16', shorts: '9:16', vertical: '9:16', youtube: '16:9', landscape: '16:9', horizontal: '16:9', square: '1:1', feed: '4:5', portrait: '4:5', instagram: '4:5', classic: '4:3', cinema: '2.39:1', scope: '2.39:1', ultrawide: '21:9', wide: '21:9', flat: '1.85:1' };
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
  if (args.help || args.h) { usage(); return 0; }
  if (!args.in || args.in === true) throw new UsageError('--in <file.html|http URL> is required');
  if (!args.out || args.out === true) throw new UsageError('--out <out.mp4> is required');

  const fromAspect = args.aspect && args.aspect !== true ? aspectSize(String(args.aspect)) : null;
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
  const audio = args.audio && args.audio !== true ? path.resolve(String(args.audio)) : null;
  if (audio && !fs.existsSync(audio)) throw new UsageError(`--audio file not found: ${audio}`);
  if (audio && preview) warn('--audio is ignored in --preview mode');

  const outPath = path.resolve(String(args.out));
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

  requireTool('ffmpeg');
  requireTool('ffprobe');
  const { playwright, from } = resolvePlaywright();
  log(`playwright: ${from}`);

  let framesDir;
  let tempFrames = false;
  if (args['frames-dir'] && args['frames-dir'] !== true) {
    framesDir = path.resolve(String(args['frames-dir']));
    fs.mkdirSync(framesDir, { recursive: true });
    for (const f of fs.readdirSync(framesDir)) {
      if (/^(frame_\d{6}|preview_(raw|tile)_\d{2})\.png$/.test(f)) fs.unlinkSync(path.join(framesDir, f));
    }
  } else {
    framesDir = fs.mkdtempSync(path.join(os.tmpdir(), 'kosif-frames-'));
    tempFrames = true;
  }
  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  const browserOpts = { isFile, width, height, scale: capScale, offline, seed, virtual: mode === 'virtual' };
  let session = await openBrowser(playwright, browserOpts);
  let exitCode = 0;
  try {
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

    if (duration === null) {
      if (hook && Number.isFinite(hook.duration) && hook.duration > 0) duration = hook.duration;
      else throw new UsageError('--duration is required (page has no window.__kosif.duration)');
    }
    const total = Math.round(duration * fps);
    if (total < 1) throw new UsageError('duration * fps must be at least one frame');

    let driver;
    if (useVirtual) { driver = new VirtualDriver(page, cdp, fps); await driver.start(); }
    else driver = new SeekDriver(page, cdp);

    log(`mode: ${driver.name} | ${width}x${height} css px, scale ${scale} -> ${outWidth}x${outHeight} | ${fps} fps | ${total} frames | start ${fmtTime(start)} | duration ${fmtTime(duration)}`);
    const timeOf = (i) => start + i / fps;

    if (preview) {
      const count = Math.min(8, total);
      const indices = [];
      for (let k = 0; k < count; k++) {
        const idx = count === 1 ? 0 : Math.round((k * (total - 1)) / (count - 1));
        if (!indices.includes(idx)) indices.push(idx);
      }
      const picks = [];
      for (let k = 0; k < indices.length; k++) {
        const idx = indices[k];
        const t = timeOf(idx);
        await driver.goTo(t);
        const file = path.join(framesDir, `preview_raw_${String(k).padStart(2, '0')}.png`);
        await driver.capture(file);
        if (k === 0) checkFrameSize(file, capWidth, capHeight);
        picks.push({ file, t, index: idx });
        log(`preview ${k + 1}/${indices.length}: frame ${idx} (t=${fmtTime(t)})`);
      }
      const sheet = path.join(path.dirname(outPath), path.basename(outPath, path.extname(outPath)) + '_preview.png');
      const res = composeContactSheet({ framesDir, picks, out: sheet });
      log(`contact sheet: ${res.out} (${picks.length} frames, ${res.labeled ? 'labeled' : 'unlabeled'})`);
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
      encodeVideo({ framesDir, fps, out: outPath, crf, audio, start, width: outWidth, height: outHeight, capWidth, capHeight });
      const probe = probeVideo(outPath);
      const want = { fps, frames: total, duration: total / fps, width: outWidth + (outWidth % 2), height: outHeight + (outHeight % 2), audio: !!audio };
      const problems = verifyProbe(probe, want);
      log(`VERIFY ${problems.length ? 'FAIL' : 'OK'} duration=${probe.duration.toFixed(3)}s fps=${probe.fps} frames=${probe.frames} size=${probe.width}x${probe.height} audio=${probe.audio ? probe.audioCodec : 'none'} file=${outPath}`);
      if (problems.length) {
        warn('verification problems: ' + problems.join('; '));
        exitCode = EXIT_VERIFY;
      }
    }

    if (errors.length) {
      warn(`page reported ${errors.length} console/page error(s):`);
      for (const e of errors.slice(0, 10)) warn('  ' + e);
    }
  } finally {
    await session.browser.close().catch(() => {});
    if (tempFrames && !keepFrames) fs.rmSync(framesDir, { recursive: true, force: true });
    else log(`frames kept in ${framesDir}`);
  }
  return exitCode;
}

main().then((code) => { process.exitCode = code; }).catch((err) => {
  if (err instanceof UsageError) {
    warn(err.message);
    usage(process.stderr);
    process.exitCode = EXIT_USAGE;
  } else {
    warn(err && err.stack ? err.stack : String(err));
    process.exitCode = EXIT_RENDER;
  }
});
