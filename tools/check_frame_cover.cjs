#!/usr/bin/env node
'use strict';
/*
 * KOSIF check_frame_cover — fail when a photo film shows an empty edge.
 *
 * Opens an HTML film (the KOSIF seek contract: window.__kosif = { duration, seek(t) }),
 * renders sample frames for every variant (for example ?style=1..5) and checks,
 * by geometry rather than by looking at colours, that on every sampled frame the
 * visible canvas is fully covered by an opaque photo:
 *
 *   - every drawImage call is recorded with the canvas transform, alpha, blend
 *     mode and blur filter in force;
 *   - a draw "covers" its canvas when the drawn photo, after the transform,
 *     contains all four canvas corners (pushed out by twice the blur radius,
 *     because a blur pulls empty pixels in from outside the photo);
 *   - the photo must be opaque (an image or bitmap with no transparent pixels,
 *     or an offscreen canvas that was itself covered by such a photo), drawn at
 *     full alpha with 'source-over' or 'copy'.
 *
 * Dark photos, vignettes and black-and-white grades therefore never cause false
 * alarms, and a one-pixel gap at the top of a 9:16 frame still fails.
 *
 * Usage:
 *   node tools/check_frame_cover.cjs --in film/index.html
 *        [--variants "style=1;style=2;style=3"]   query strings, ';' separated
 *        [--samples 24] [--times 0,1.5,3]           evenly spaced samples or exact times
 *        [--root <dir>]                             served directory (default: cwd if it holds the page, else the page's dir)
 *        [--canvas <css selector>]                  the visible canvas (default: the largest canvas)
 *        [--frames-dir <dir>]                       save a PNG of every failing frame
 *        [--json <file>] [--timeout 60000]
 *
 * Exit codes: 0 every frame covered, 3 empty edges found, 1 usage, 2 page/render error.
 * Node 22, CommonJS, Playwright resolved at runtime (same as tools/render_html.cjs).
 * License: MIT (part of KOSIF TOOL).
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

const EXIT_USAGE = 1, EXIT_RENDER = 2, EXIT_GAPS = 3;

function parseArgs(argv) {
  const a = { samples: 24, timeout: 60000, variants: [''] };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i], v = () => { const x = argv[++i]; if (x == null) throw new Error(`${k} needs a value`); return x; };
    if (k === '--in') a.in = v();
    else if (k === '--variants') a.variants = v().split(';').map((s) => s.trim().replace(/^\?/, ''));
    else if (k === '--samples') a.samples = Math.max(1, parseInt(v(), 10));
    else if (k === '--times') a.times = v().split(',').map(Number);
    else if (k === '--root') a.root = v();
    else if (k === '--canvas') a.canvas = v();
    else if (k === '--frames-dir') a.framesDir = v();
    else if (k === '--json') a.json = v();
    else if (k === '--timeout') a.timeout = parseInt(v(), 10);
    else if (k === '-h' || k === '--help') a.help = true;
    else throw new Error(`unknown option ${k}`);
  }
  return a;
}

function loadPlaywright() {
  const tries = ['playwright', 'playwright-core', '/opt/node22/lib/node_modules/playwright', '/usr/local/lib/node_modules/playwright', '/usr/lib/node_modules/playwright'];
  for (const t of tries) { try { return require(t); } catch (_) { /* next */ } }
  return null;
}

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.cjs': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif',
  '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf', '.mp3': 'audio/mpeg',
  '.wav': 'audio/wav', '.m4a': 'audio/mp4', '.mp4': 'video/mp4', '.webm': 'video/webm' };

// A static server, so photos are same-origin and their pixels can be read (file:// taints canvases).
function serve(root) {
  const srv = http.createServer((req, res) => {
    const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    const f = path.resolve(root, '.' + p);
    if (!f.startsWith(path.resolve(root))) { res.writeHead(403); return res.end(); }
    fs.stat(f, (err, st) => {
      if (err || !st.isFile()) { res.writeHead(404); return res.end(); }
      res.writeHead(200, { 'content-type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(res);
    });
  });
  return new Promise((ok) => srv.listen(0, '127.0.0.1', () => ok(srv)));
}

// Runs inside the page before any page script.
function probe() {
  const P = CanvasRenderingContext2D.prototype, orig = P.drawImage, origClear = P.clearRect, origFill = P.fillRect;
  const state = new WeakMap();          // canvas -> { covered }
  const opaqueImg = new WeakMap();      // image -> bool
  const st = (cv) => { let s = state.get(cv); if (!s) { s = { covered: false }; state.set(cv, s); } return s; };
  let log = null, scan = null;

  function isOpaqueImage(img) {
    if (opaqueImg.has(img)) return opaqueImg.get(img);
    let ok = false;
    try {
      const w = img.naturalWidth || img.videoWidth || img.width, h = img.naturalHeight || img.videoHeight || img.height;
      if (w > 0 && h > 0) {
        scan = scan || document.createElement('canvas');
        const n = 64; scan.width = n; scan.height = n;
        const g = scan.getContext('2d', { willReadFrequently: true });
        origClear.call(g, 0, 0, n, n);
        orig.call(g, img, 0, 0, n, n);
        const d = g.getImageData(0, 0, n, n).data;
        ok = true;
        for (let i = 3; i < d.length; i += 4) if (d[i] < 250) { ok = false; break; }
      }
    } catch (e) { ok = false; }
    if (img instanceof HTMLImageElement && !img.complete) return ok;   // do not cache a half-loaded image
    opaqueImg.set(img, ok);
    return ok;
  }

  function blurPx(filter) {
    const m = /blur\(\s*([\d.]+)px\s*\)/.exec(filter || '');
    return m ? parseFloat(m[1]) : 0;
  }

  // Is point (x, y) inside the convex quad q (4 points in order)?
  function inQuad(q, x, y) {
    let sign = 0;
    for (let i = 0; i < 4; i++) {
      const [ax, ay] = q[i], [bx, by] = q[(i + 1) % 4];
      const c = (bx - ax) * (y - ay) - (by - ay) * (x - ax);
      if (Math.abs(c) < 1e-6) continue;
      const sgn = c > 0 ? 1 : -1;
      if (sign === 0) sign = sgn; else if (sgn !== sign) return false;
    }
    return true;
  }

  P.drawImage = function (src, ...a) {
    const r = orig.call(this, src, ...a);
    try {
      const cv = this.canvas;
      const sw0 = src.naturalWidth || src.videoWidth || src.width, sh0 = src.naturalHeight || src.videoHeight || src.height;
      let sx = 0, sy = 0, sw = sw0, sh = sh0, dx, dy, dw, dh;
      if (a.length === 2) { [dx, dy] = a; dw = sw0; dh = sh0; }
      else if (a.length === 4) { [dx, dy, dw, dh] = a; }
      else { [sx, sy, sw, sh, dx, dy, dw, dh] = a; }
      // keep only the part of the source rectangle that is really inside the source
      const x0 = Math.max(sx, 0), y0 = Math.max(sy, 0), x1 = Math.min(sx + sw, sw0), y1 = Math.min(sy + sh, sh0);
      const fx = (v) => dx + ((v - sx) / sw) * dw, fy = (v) => dy + ((v - sy) / sh) * dh;
      const rx0 = fx(x0), rx1 = fx(x1), ry0 = fy(y0), ry1 = fy(y1);
      const m = this.getTransform();
      const T = (x, y) => [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f];
      const q = [T(rx0, ry0), T(rx1, ry0), T(rx1, ry1), T(rx0, ry1)];
      const b = 2 * blurPx(this.filter);
      const W = cv.width, H = cv.height;
      const geomCovers = x1 > x0 && y1 > y0 && [[-b, -b], [W + b, -b], [W + b, H + b], [-b, H + b]].every(([x, y]) => inQuad(q, x, y));
      const isCanvas = (typeof HTMLCanvasElement !== 'undefined' && src instanceof HTMLCanvasElement) ||
        (typeof OffscreenCanvas !== 'undefined' && src instanceof OffscreenCanvas);
      const opaqueSrc = isCanvas ? st(src).covered : isOpaqueImage(src);
      const solid = this.globalAlpha >= 0.999 && (this.globalCompositeOperation === 'source-over' || this.globalCompositeOperation === 'copy');
      const covers = geomCovers && opaqueSrc && solid;
      if (covers) st(cv).covered = true;
      if (log && cv === log.canvas) {
        log.draws.push({ src: isCanvas ? 'canvas' : (src.currentSrc || src.src || src.constructor.name || 'image').toString().slice(-60),
          geomCovers, opaqueSrc, alpha: +this.globalAlpha.toFixed(3), op: this.globalCompositeOperation, blur: b / 2,
          quad: q.map(([x, y]) => [+x.toFixed(2), +y.toFixed(2)]) });
      }
    } catch (e) { /* never break the page */ }
    return r;
  };
  // A full clear or a full opaque solid fill replaces what the canvas held (the canvas
  // reports opaque colours as #rrggbb; gradients and see-through colours are overlays).
  P.clearRect = function (x, y, w, h) {
    const r = origClear.call(this, x, y, w, h);
    try { const m = this.getTransform(); if (m.isIdentity && x <= 0 && y <= 0 && x + w >= this.canvas.width && y + h >= this.canvas.height) st(this.canvas).covered = false; } catch (e) { /* */ }
    return r;
  };
  P.fillRect = function (x, y, w, h) {
    const r = origFill.call(this, x, y, w, h);
    try { const m = this.getTransform(); if (m.isIdentity && x <= 0 && y <= 0 && x + w >= this.canvas.width && y + h >= this.canvas.height && this.globalCompositeOperation === 'source-over' && this.globalAlpha >= 0.999 && typeof this.fillStyle === 'string' && this.fillStyle[0] === '#') st(this.canvas).covered = false; } catch (e) { /* */ }
    return r;
  };

  window.__coverProbe = {
    begin(canvas) { st(canvas).covered = false; log = { canvas, draws: [] }; },
    end() { const out = { covered: st(log.canvas).covered, draws: log.draws }; log = null; return out; },
  };
}

async function main() {
  let args;
  try { args = parseArgs(process.argv.slice(2)); } catch (e) { console.error(e.message); return EXIT_USAGE; }
  if (args.help || !args.in) { console.error(fs.readFileSync(__filename, 'utf8').split('*/')[0]); return args.help ? 0 : EXIT_USAGE; }
  const page0 = path.resolve(args.in);
  if (!fs.existsSync(page0)) { console.error(`no such page: ${args.in}`); return EXIT_USAGE; }
  let root = args.root ? path.resolve(args.root) : process.cwd();
  if (!page0.startsWith(root + path.sep)) root = path.dirname(page0);
  const pw = loadPlaywright();
  if (!pw) { console.error('Playwright is not installed (npm i playwright). Cannot render frames.'); return EXIT_RENDER; }

  const srv = await serve(root);
  const base = `http://127.0.0.1:${srv.address().port}/` + path.relative(root, page0).split(path.sep).map(encodeURIComponent).join('/');
  const browser = await pw.chromium.launch();
  const report = { page: args.in, variants: [], ok: true };
  try {
    for (const variant of args.variants) {
      const ctx = await browser.newContext({ viewport: { width: 540, height: 960 } });
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', (e) => errors.push(String(e)));
      await page.addInitScript(probe);
      const url = base + (variant ? '?' + variant : '');
      await page.goto(url, { waitUntil: 'load', timeout: args.timeout });
      await page.waitForFunction(() => window.__kosif && typeof window.__kosif.seek === 'function', null, { timeout: args.timeout })
        .catch(() => { throw new Error(`${url}: page does not expose window.__kosif.seek(t)`); });
      await page.evaluate(() => (window.__kosifReady || Promise.resolve()));
      const duration = await page.evaluate(() => +window.__kosif.duration || 0);
      const times = args.times || Array.from({ length: args.samples }, (_, i) =>
        args.samples === 1 ? 0 : +(Math.min(duration - 1e-3, (i * duration) / (args.samples - 1))).toFixed(3)).filter((t) => t >= 0);
      const v = { variant: variant || '(default)', duration, frames: [], gaps: 0 };
      for (const t of times) {
        const res = await page.evaluate(async ({ t, sel }) => {
          const all = [...document.querySelectorAll(sel || 'canvas')];
          const cv = all.sort((a, b) => b.width * b.height - a.width * a.height)[0];
          if (!cv) return { error: 'no canvas on the page' };
          window.__coverProbe.begin(cv);
          await window.__kosif.seek(t);
          await new Promise((r) => requestAnimationFrame(() => r()));
          const out = window.__coverProbe.end();
          out.size = [cv.width, cv.height];
          return out;
        }, { t, sel: args.canvas });
        if (res.error) throw new Error(`${url}: ${res.error}`);
        const f = { t, covered: res.covered, size: res.size, draws: res.draws.length };
        if (!res.covered) {
          v.gaps++;
          f.why = res.draws.length ? res.draws.map((d) => `${d.src}: ${!d.opaqueSrc ? 'has transparent pixels' : !d.geomCovers ? 'leaves an edge uncovered' : `alpha ${d.alpha} / ${d.op}`}`).slice(0, 4)
            : ['no photo was drawn on the visible canvas'];
          f.quads = res.draws.filter((d) => d.opaqueSrc).map((d) => d.quad).slice(0, 3);
          if (args.framesDir) {
            fs.mkdirSync(args.framesDir, { recursive: true });
            const name = `${(variant || 'default').replace(/[^\w=-]+/g, '_')}_t${t.toFixed(2)}.png`;
            const el = await page.$(args.canvas || 'canvas');
            if (el) await el.screenshot({ path: path.join(args.framesDir, name) }).catch(() => {});
            f.png = path.join(args.framesDir, name);
          }
        }
        v.frames.push(f);
      }
      if (errors.length) v.pageErrors = errors.slice(0, 5);
      report.variants.push(v);
      if (v.gaps) report.ok = false;
      const bad = v.frames.filter((f) => !f.covered);
      console.log(`${v.gaps ? 'FAIL' : 'ok  '} ${v.variant}: ${v.frames.length - bad.length}/${v.frames.length} frames covered` +
        (bad.length ? ` — empty edge at t=${bad.slice(0, 6).map((f) => f.t).join(', ')}${bad.length > 6 ? ' …' : ''}; ${bad[0].why[0]}` : ''));
      await ctx.close();
    }
  } catch (e) {
    console.error(String(e && e.message || e));
    await browser.close(); srv.close();
    return EXIT_RENDER;
  }
  await browser.close(); srv.close();
  if (args.json) fs.writeFileSync(args.json, JSON.stringify(report, null, 2));
  console.log(report.ok ? 'PASS: the photo covers the whole frame in every sampled frame' : 'FAIL: empty edges found (see above)');
  return report.ok ? 0 : EXIT_GAPS;
}

if (require.main === module) main().then((c) => process.exit(c), (e) => { console.error(e); process.exit(EXIT_RENDER); });
module.exports = { parseArgs };
