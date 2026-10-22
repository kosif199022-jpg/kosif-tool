// KOSIF Atlas Harness — original deterministic canvas toolkit for style explainers.
// Written for kosif-superpowers (A15). Not derived from any third-party source file.
// Contract: every frame is a pure function of time t -> same t, same pixels.
// Never call Math.random() inside a frame: use KH.rng(seed) / KH.noise(seed).
(function (root) {
  "use strict";
  const KH = (root.KH = root.KH || {});
  KH.W = 1280; KH.H = 720;

  // ---------- hashing + seeded random ----------
  KH.hash = function (s) {
    s = String(s); let h = 2166136261 >>> 0;
    for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    return h >>> 0;
  };
  // xorshift128+ style generator returning [0,1)
  KH.rng = function (seed) {
    let a = (typeof seed === "number" ? seed >>> 0 : KH.hash(seed)) || 0x9e3779b9;
    let b = (a ^ 0x85ebca6b) >>> 0 || 1;
    const r = function () {
      let x = a, y = b; a = y; x ^= x << 23; x ^= x >>> 17; x ^= y ^ (y >>> 26); b = x >>> 0;
      return ((a + b) >>> 0) / 4294967296;
    };
    r.range = (lo, hi) => lo + (hi - lo) * r();
    r.int = (lo, hi) => Math.floor(lo + (hi - lo + 1) * r());
    r.pick = (arr) => arr[Math.floor(r() * arr.length) % arr.length];
    r.chance = (p) => r() < p;
    r.gauss = () => { let u = 0, v = 0; while (u === 0) u = r(); v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(6.283185307 * v); };
    r.sign = () => (r() < 0.5 ? -1 : 1);
    return r;
  };

  // ---------- value-gradient noise (2D/3D) + fbm ----------
  KH.noise = function (seed) {
    const r = KH.rng(seed === undefined ? 11 : seed), P = new Uint8Array(512), G = [];
    const perm = Array.from({ length: 256 }, (_, i) => i);
    for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [perm[i], perm[j]] = [perm[j], perm[i]]; }
    for (let i = 0; i < 512; i++) P[i] = perm[i & 255];
    for (let i = 0; i < 256; i++) { const a = r() * Math.PI * 2, z = r() * 2 - 1, s = Math.sqrt(1 - z * z); G.push([Math.cos(a) * s, Math.sin(a) * s, z]); }
    const fade = (t) => t * t * t * (t * (t * 6 - 15) + 10);
    const lerp = (a, b, t) => a + (b - a) * t;
    function n3(x, y, z) {
      const X = Math.floor(x), Y = Math.floor(y), Z = Math.floor(z);
      const fx = x - X, fy = y - Y, fz = z - Z, u = fade(fx), v = fade(fy), w = fade(fz);
      const g = (i, j, k) => { const q = G[P[(P[(P[(X + i) & 255] + Y + j) & 255] + Z + k) & 255]]; return q[0] * (fx - i) + q[1] * (fy - j) + q[2] * (fz - k); };
      return lerp(lerp(lerp(g(0, 0, 0), g(1, 0, 0), u), lerp(g(0, 1, 0), g(1, 1, 0), u), v),
                  lerp(lerp(g(0, 0, 1), g(1, 0, 1), u), lerp(g(0, 1, 1), g(1, 1, 1), u), v), w) * 1.4;
    }
    const n2 = (x, y) => n3(x, y, 0.5);
    const fbm3 = (x, y, z, oct = 4) => { let s = 0, a = 0.5, f = 1, n = 0; for (let i = 0; i < oct; i++) { s += a * n3(x * f, y * f, z * f); n += a; a *= 0.5; f *= 2.03; } return s / n; };
    const fbm2 = (x, y, oct = 4) => fbm3(x, y, 0.5, oct);
    // curl of a 2D noise field: divergence-free flow (flow-field, ink, smoke)
    const curl = (x, y, z = 0, e = 0.01) => [(n3(x, y + e, z) - n3(x, y - e, z)) / (2 * e), -(n3(x + e, y, z) - n3(x - e, y, z)) / (2 * e)];
    return { n2, n3, fbm2, fbm3, curl };
  };

  // ---------- math + easing + timeline ----------
  KH.lerp = (a, b, t) => a + (b - a) * t;
  KH.clamp = (v, lo = 0, hi = 1) => (v < lo ? lo : v > hi ? hi : v);
  KH.map = (v, a, b, c, d) => c + ((v - a) / (b - a)) * (d - c);
  KH.smooth = (a, b, x) => { const t = KH.clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  KH.ease = {
    linear: (t) => t,
    in: (t) => t * t * t,
    out: (t) => 1 - Math.pow(1 - t, 3),
    inOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
    sine: (t) => 0.5 - 0.5 * Math.cos(Math.PI * t),
    expoOut: (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t)),
    back: (t, s = 1.7) => 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2),
    elastic: (t) => (t <= 0 ? 0 : t >= 1 ? 1 : Math.pow(2, -9 * t) * Math.sin((t * 10 - 0.75) * 2.0944) + 1),
    // damped spring settle (overshoot then rest) — pop-ins, stamps
    spring: (t, k = 7, d = 5) => 1 - Math.exp(-d * t) * Math.cos(k * t),
    steps: (t, n) => Math.floor(KH.clamp(t) * n) / n, // stop-motion / on-twos feel
  };
  // progress of t inside [a,b] with optional easing name
  KH.span = (t, a, b, ease) => { const p = KH.clamp((t - a) / (b - a)); return ease ? KH.ease[ease](p) : p; };
  // hold the time on "twos"/"threes" etc.: quantise t to a frame rate (12 fps -> on twos at 24)
  KH.onFps = (t, fps) => Math.floor(t * fps) / fps;
  // beat helper: list of {at, dur} -> active index and local progress
  KH.beats = function (list) {
    return (t) => { let i = 0; while (i + 1 < list.length && t >= list[i + 1].at) i++; const b = list[i]; return { i, b, p: KH.clamp((t - b.at) / (b.dur || 1)) }; };
  };

  // ---------- colour ----------
  KH.hex = (h) => { h = String(h).replace("#", ""); if (h.length === 3) h = h.split("").map((c) => c + c).join(""); const n = parseInt(h, 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
  KH.rgba = (c, a = 1) => { const [r, g, b] = Array.isArray(c) ? c : KH.hex(c); return "rgba(" + (r | 0) + "," + (g | 0) + "," + (b | 0) + "," + a + ")"; };
  KH.mix = (c1, c2, t) => { const a = Array.isArray(c1) ? c1 : KH.hex(c1), b = Array.isArray(c2) ? c2 : KH.hex(c2); return [0, 1, 2].map((i) => a[i] + (b[i] - a[i]) * t); };
  KH.palette = (list) => (i) => list[((i % list.length) + list.length) % list.length];

  // ---------- canvas layers + finishing passes ----------
  const cache = new Map();
  KH.layer = (w = KH.W, h = KH.H) => { const c = typeof OffscreenCanvas !== "undefined" ? new OffscreenCanvas(w, h) : Object.assign(document.createElement("canvas"), { width: w, height: h }); return c; };
  // cached static texture: build once per key (safe: static pixels only)
  KH.cached = (key, w, h, paint) => { if (!cache.has(key)) { const c = KH.layer(w, h); paint(c.getContext("2d"), w, h); cache.set(key, c); } return cache.get(key); };

  // grain: a few pre-baked noise tiles cycled by frame -> animated but deterministic
  KH.grain = function (ctx, t, amount = 0.07, fps = 24, mono = true) {
    const idx = Math.floor(t * fps) % 6;
    const tile = KH.cached("grain" + idx + mono, 256, 256, (g, w, h) => {
      const img = g.createImageData(w, h), r = KH.rng("grain" + idx);
      for (let i = 0; i < img.data.length; i += 4) { const v = r() * 255; img.data[i] = v; img.data[i + 1] = mono ? v : r() * 255; img.data[i + 2] = mono ? v : r() * 255; img.data[i + 3] = 255; }
      g.putImageData(img, 0, 0);
    });
    ctx.save(); ctx.globalAlpha = amount; ctx.globalCompositeOperation = "overlay";
    ctx.fillStyle = ctx.createPattern(tile, "repeat"); ctx.fillRect(0, 0, KH.W, KH.H); ctx.restore();
  };
  // paper: base colour + fibre streaks + mottling (cached per base colour)
  KH.paper = function (ctx, base = "#f2ead8", seed = 3, strength = 0.07) {
    const tex = KH.cached("paper" + base + seed + strength, KH.W, KH.H, (g, w, h) => {
      g.fillStyle = base; g.fillRect(0, 0, w, h);
      const n = KH.noise(seed), r = KH.rng(seed + 1), [br, bg, bb] = KH.hex(base);
      const img = g.getImageData(0, 0, w, h);
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const m = n.fbm2(x / 180, y / 180, 3) * 0.6 + n.n2(x / 9, y / 9) * 0.25 + (r() - 0.5) * 0.35;
        const k = 1 + m * strength, i = (y * w + x) * 4;
        img.data[i] = br * k; img.data[i + 1] = bg * k; img.data[i + 2] = bb * k;
      }
      g.putImageData(img, 0, 0);
      g.globalAlpha = strength * 1.6; g.strokeStyle = KH.rgba(KH.mix(base, "#000", 0.25));
      for (let i = 0; i < 900; i++) { const x = r() * w, y = r() * h, a = r() * Math.PI, l = 4 + r() * 18; g.lineWidth = 0.4 + r() * 0.6; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
    });
    ctx.drawImage(tex, 0, 0);
  };
  KH.vignette = function (ctx, strength = 0.45, color = "0,0,0") {
    const g = ctx.createRadialGradient(KH.W / 2, KH.H / 2, KH.H * 0.35, KH.W / 2, KH.H / 2, KH.H * 0.95);
    g.addColorStop(0, "rgba(" + color + ",0)"); g.addColorStop(1, "rgba(" + color + "," + strength + ")");
    ctx.save(); ctx.fillStyle = g; ctx.fillRect(0, 0, KH.W, KH.H); ctx.restore();
  };
  // additive bloom: blur a copy of the bright layer and add it back
  KH.bloom = function (ctx, src, radius = 12, strength = 0.8) {
    ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = strength; ctx.filter = "blur(" + radius + "px)";
    ctx.drawImage(src, 0, 0); ctx.filter = "none"; ctx.restore();
  };
  // misregistration: draw a layer several times with offsets + multiply (riso, screenprint, newsprint)
  KH.misregister = function (ctx, layers, t, seed = 5, maxPx = 4) {
    const r = KH.rng(seed); ctx.save(); ctx.globalCompositeOperation = "multiply";
    for (const L of layers) ctx.drawImage(L, r.range(-maxPx, maxPx), r.range(-maxPx, maxPx));
    ctx.restore();
  };
  // halftone dots of a scalar field (0..1) -> comics, newsprint, pop
  KH.halftone = function (ctx, field, x0, y0, w, h, cell = 9, color = "#111", angle = 0.26) {
    ctx.save(); ctx.fillStyle = color; ctx.translate(x0 + w / 2, y0 + h / 2); ctx.rotate(angle);
    const R = Math.hypot(w, h) / 2;
    for (let y = -R; y < R; y += cell) for (let x = -R; x < R; x += cell) {
      const ca = Math.cos(-angle), sa = Math.sin(-angle), px = x * ca - y * sa + w / 2, py = x * sa + y * ca + h / 2;
      if (px < 0 || py < 0 || px > w || py > h) continue;
      const v = KH.clamp(field(px, py)); if (v < 0.02) continue;
      ctx.beginPath(); ctx.arc(x, y, (cell / 2) * Math.sqrt(v) * 1.05, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  };

  // ---------- drawing vocabulary used by every style ----------
  // hand wobble a polyline (deterministic): pen, chalk, marker, pencil
  KH.wobble = function (pts, amp = 1.5, seed = 1) {
    const n = KH.noise(seed);
    return pts.map(([x, y], i) => [x + n.n2(i * 0.31, 0.7) * amp, y + n.n2(i * 0.31, 9.1) * amp]);
  };
  KH.sample = function (fn, steps = 64) { const out = []; for (let i = 0; i <= steps; i++) out.push(fn(i / steps)); return out; };
  KH.lineTo = (a, b, steps = 24) => KH.sample((u) => [KH.lerp(a[0], b[0], u), KH.lerp(a[1], b[1], u)], steps);
  KH.arcPts = (cx, cy, r, a0, a1, steps = 48) => KH.sample((u) => [cx + Math.cos(KH.lerp(a0, a1, u)) * r, cy + Math.sin(KH.lerp(a0, a1, u)) * r], steps);
  KH.quadPts = (a, c, b, steps = 40) => KH.sample((u) => { const v = 1 - u; return [v * v * a[0] + 2 * v * u * c[0] + u * u * b[0], v * v * a[1] + 2 * v * u * c[1] + u * u * b[1]]; }, steps);
  // draw-on: stroke only the first fraction p (0..1) of a polyline; returns tip point
  KH.drawOn = function (ctx, pts, p) {
    if (p <= 0 || pts.length < 2) return null;
    const L = []; let tot = 0;
    for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(d); tot += d; }
    let left = tot * KH.clamp(p); ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); let tip = pts[0];
    for (let i = 1; i < pts.length; i++) {
      if (left >= L[i - 1]) { ctx.lineTo(pts[i][0], pts[i][1]); left -= L[i - 1]; tip = pts[i]; }
      else { const u = left / L[i - 1]; tip = [KH.lerp(pts[i - 1][0], pts[i][0], u), KH.lerp(pts[i - 1][1], pts[i][1], u)]; ctx.lineTo(tip[0], tip[1]); break; }
    }
    ctx.stroke(); return tip;
  };
  // textured stroke: many thin passes with alpha jitter (chalk / dry brush / pencil)
  KH.roughStroke = function (ctx, pts, p, opt = {}) {
    const passes = opt.passes || 4, w = opt.width || 4, seed = opt.seed || 1, r = KH.rng(seed);
    ctx.save(); ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = opt.color || "#fff";
    let tip = null;
    for (let k = 0; k < passes; k++) {
      ctx.globalAlpha = (opt.alpha || 0.9) * (0.45 + r() * 0.55); ctx.lineWidth = w * (0.45 + r() * 0.6);
      tip = KH.drawOn(ctx, KH.wobble(pts, (opt.wobble || 1.2) * (0.6 + r()), seed * 7 + k), p);
    }
    ctx.restore(); return tip;
  };
  KH.arrowHead = function (ctx, tip, from, size = 18) {
    if (!tip || !from) return; const a = Math.atan2(tip[1] - from[1], tip[0] - from[0]);
    ctx.beginPath(); ctx.moveTo(tip[0] - Math.cos(a - 0.45) * size, tip[1] - Math.sin(a - 0.45) * size);
    ctx.lineTo(tip[0], tip[1]); ctx.lineTo(tip[0] - Math.cos(a + 0.45) * size, tip[1] - Math.sin(a + 0.45) * size); ctx.stroke();
  };
  // typewriter / write-on text; works for Arabic (whole-string shaping preserved by slicing graphemes)
  KH.typeOn = function (ctx, text, x, y, p) {
    const g = Array.from(text), n = Math.round(g.length * KH.clamp(p));
    if (n > 0) ctx.fillText(g.slice(0, n).join(""), x, y); return n;
  };
  // counter that ticks at most ~12 times/s and eases into its final value
  KH.counter = (t, t0, t1, from, to, fps = 12) => { const tq = KH.onFps(t, fps); return Math.round(KH.lerp(from, to, KH.ease.out(KH.span(tq, t0, t1)))); };
  // fit a font size so text fits width w (never below minPx)
  KH.fitText = function (ctx, text, family, w, maxPx, minPx = 28, weight = "700") {
    let s = maxPx; for (; s > minPx; s -= 2) { ctx.font = weight + " " + s + "px " + family; if (ctx.measureText(text).width <= w) break; }
    ctx.font = weight + " " + s + "px " + family; return s;
  };
  // 2D camera: world transform with pan/zoom/rotate around the frame centre
  KH.camera = function (ctx, cam) {
    ctx.translate(KH.W / 2, KH.H / 2); ctx.rotate(cam.rot || 0); ctx.scale(cam.zoom || 1, cam.zoom || 1); ctx.translate(-(cam.x || KH.W / 2), -(cam.y || KH.H / 2));
  };
  KH.camAt = function (t, keys, ease = "inOut") { // keys: [{t, x, y, zoom}]
    if (t <= keys[0].t) return keys[0]; for (let i = 1; i < keys.length; i++) if (t <= keys[i].t) {
      const a = keys[i - 1], b = keys[i], u = KH.ease[ease]((t - a.t) / (b.t - a.t));
      return { x: KH.lerp(a.x, b.x, u), y: KH.lerp(a.y, b.y, u), zoom: KH.lerp(a.zoom || 1, b.zoom || 1, u), rot: KH.lerp(a.rot || 0, b.rot || 0, u) };
    } return keys[keys.length - 1];
  };
  // simple perspective projection for "own 3D" styles (low-poly, wireframe, voxel, papercraft)
  KH.project = function (p, cam) {
    const [x, y, z] = [p[0] - cam.x, p[1] - cam.y, p[2] - cam.z], cy = Math.cos(cam.yaw || 0), sy = Math.sin(cam.yaw || 0), cp = Math.cos(cam.pitch || 0), sp = Math.sin(cam.pitch || 0);
    const x1 = x * cy - z * sy, z1 = x * sy + z * cy, y1 = y * cp - z1 * sp, z2 = y * sp + z1 * cp;
    if (z2 <= 0.01) return null; const f = (cam.focal || 900) / z2; return [KH.W / 2 + x1 * f, KH.H / 2 - y1 * f, z2];
  };

  // ---------- player glue ----------
  // Fonts are loaded before the first frame; returns a promise.
  KH.ready = async function (families) {
    if (!root.document || !document.fonts) return;
    await Promise.all((families || []).map((f) => document.fonts.load("700 40px " + f).catch(() => null)));
    await document.fonts.ready;
  };
})(typeof window !== "undefined" ? window : globalThis);
