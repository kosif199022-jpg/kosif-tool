/*
 * KOSIF World Film engine («التنين الأسود»): one big world, one continuous camera, drawn on a canvas.
 *
 * The page sets window.WORLD_PLAN (see world_film.py and SKILL.md) and loads camera.cjs then this file.
 * Every frame is a pure function of t: window.__kosif = { duration, seek(t) } for tools/render_html.cjs.
 *
 * Objects (world coordinates, or "geo": [lat, lon] on the map plus "dx"/"dy"):
 *   desk   the surface everything lies on (wood, dark, lit by one warm pool of light)
 *   map    a paper map: lands/seas polygons and rivers in lat/lon, faint graticule, no filler labels
 *   area   a polygon in lat/lon that lights up (gold) when a hit targets it
 *   pin    a small place marker
 *   route  a path between geo points that draws itself (hit action "draw")
 *   photo  a real photo printed with a white border that drops onto the world at "enter"
 *   text   big type in the world (RTL, real shaping, wiped on, never split into letters)
 *   book   a code-drawn book that opens on a hit; its pages are soft grey lines, not words
 *   stamp  ink stamp that slams onto a target on the beat
 * Beats choose ONE hero; everything else dims back. Hits: circle, glow, lift, open, draw, stamp.
 * Finish: handheld sway, motion blur on fast moves (sub-frame accumulation), film grain, glow, vignette.
 * License: MIT (part of KOSIF TOOL).
 */
(function () {
  'use strict';
  const PLAN = window.WORLD_PLAN;
  const W = PLAN.format.width, H = PLAN.format.height, FPS = PLAN.format.fps || 30;
  const ST = Object.assign({ grain: 0.07, glow: 0.22, vignette: 0.6, handheld: 1, blur: true, dim: 0.62 }, PLAN.style || {});
  const PAL = Object.assign({ desk: '#1a120c', desk2: '#2a1d13', paper: '#efe6d2', land: '#e4d6b8', sea: '#c9d3cf',
    ink: '#3a3226', gold: '#d9a93a', red: '#b3261e', text: '#fff7e6', textInk: '#2b241b', shadow: 'rgba(0,0,0,0.55)' }, PLAN.palette || {});
  const FONT = PLAN.font || 'Cairo';

  const canvas = document.getElementById('film');
  canvas.width = W; canvas.height = H;
  const out = canvas.getContext('2d');
  const scene = document.createElement('canvas'); scene.width = W; scene.height = H;
  const sctx = scene.getContext('2d');
  const acc = document.createElement('canvas'); acc.width = W; acc.height = H;
  const actx = acc.getContext('2d');
  const small = document.createElement('canvas'); small.width = Math.round(W / 6); small.height = Math.round(H / 6);
  const smctx = small.getContext('2d');

  // ------------------------------------------------------------ helpers
  function rng(seed) {
    let a = seed >>> 0 || 1;
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const R = rng(PLAN.seed || 7);
  const NOISE = Array.from({ length: 512 }, () => R() * 2 - 1);
  function noise1(x, ch) { // smooth value noise, deterministic
    const o = (ch || 0) * 97;
    const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f);
    const a = NOISE[(i + o) & 511], b = NOISE[(i + 1 + o) & 511];
    return a + (b - a) * u;
  }
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, s) => a + (b - a) * s;
  const ease = (s) => { s = clamp(s, 0, 1); return s < 0.5 ? 4 * s * s * s : 1 - Math.pow(-2 * s + 2, 3) / 2; };
  const easeOut = (s) => 1 - Math.pow(1 - clamp(s, 0, 1), 3);
  const easeBack = (s) => { s = clamp(s, 0, 1); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(s - 1, 3) + c1 * Math.pow(s - 1, 2); };
  const ramp = (t, a, d) => clamp((t - a) / d, 0, 1);

  // ------------------------------------------------------------ world model
  const objs = PLAN.objects.map((o, i) => Object.assign({ z: i }, o));
  const byId = Object.fromEntries(objs.map((o) => [o.id, o]));
  const map = objs.find((o) => o.kind === 'map');
  function geo(lat, lon) {
    const p = map.projection;
    return [map.x + (lon - p.lon0) * p.k, map.y + (p.lat0 - lat) * p.k * (p.ky || 1)];
  }
  for (const o of objs) {
    if (o.geo) { const g = geo(o.geo[0], o.geo[1]); o.x = g[0] + (o.dx || 0); o.y = g[1] + (o.dy || 0); }
    if (o.kind === 'route') o.pts = o.path.map((q) => geo(q[0], q[1]));
  }
  const hits = {}; // object id -> [{t, action, beat}]
  PLAN.beats.forEach((b, i) => {
    for (const h of (b.hits || (b.hit ? [b.hit] : []))) {
      (hits[h.target || b.hero] = hits[h.target || b.hero] || []).push(Object.assign({ beat: i }, h));
    }
  });
  const KEYS = window.KosifCamera.buildKeys(PLAN);

  // Focus: 1 for the beat's hero (and its text), eased across beat edges so dimming never pops.
  function focusOf(id, t) {
    let f = 0;
    for (const b of PLAN.beats) {
      const on = b.hero === id || b.text === id || (b.also || []).includes(id);
      if (!on) continue;
      const a = ramp(t, b.start - 0.25, 0.45);
      const z = 1 - ramp(t, b.end - 0.2, 0.45);
      f = Math.max(f, Math.min(a, z));
    }
    return f;
  }
  function anyHero(t) { // is a non-world hero active? (world itself dims only then)
    let f = 0;
    for (const b of PLAN.beats) {
      const h = byId[b.hero];
      if (!h || h.kind === 'map' || h.kind === 'area' || h.kind === 'route') continue;
      f = Math.max(f, Math.min(ramp(t, b.start - 0.25, 0.45), 1 - ramp(t, b.end - 0.2, 0.45)));
    }
    return f;
  }

  // ------------------------------------------------------------ assets
  const images = {};
  const loads = [];
  for (const o of objs) if (o.kind === 'photo' && o.src && !images[o.src]) {
    const im = new Image();
    images[o.src] = im;
    loads.push(new Promise((res, rej) => { im.onload = res; im.onerror = () => rej(new Error('image failed: ' + o.src)); im.src = o.src; }));
  }
  for (const f of (PLAN.fonts || [])) {
    const ff = new FontFace(f.family, `url(${f.src})`, { weight: f.weight || '100 900' });
    loads.push(ff.load().then((x) => document.fonts.add(x)));
  }
  function tile(size, seed, fn) {
    const c = document.createElement('canvas'); c.width = c.height = size;
    const g = c.getContext('2d'); const d = g.createImageData(size, size); const r = rng(seed);
    for (let i = 0; i < size * size; i++) { const v = fn(r, i % size, (i / size) | 0); d.data[i * 4] = v[0]; d.data[i * 4 + 1] = v[1]; d.data[i * 4 + 2] = v[2]; d.data[i * 4 + 3] = v[3]; }
    g.putImageData(d, 0, 0); return c;
  }
  const grains = [0, 1, 2, 3, 4, 5].map((s) => tile(256, 100 + s, (r) => { const v = 128 + (r() - 0.5) * 255; return [v, v, v, 255]; }));
  const paperTex = tile(512, 11, (r, x, y) => { const v = (r() - 0.5) * 22 + Math.sin(y * 0.9 + r()) * 3; return [0, 0, 0, clamp(14 + v, 0, 40)]; });
  const woodTex = tile(512, 12, (r, x, y) => { const v = Math.sin(y * 0.11 + Math.sin(x * 0.013) * 3 + noise1(y * 0.05, 3) * 2) * 0.5 + 0.5; return [0, 0, 0, 18 + v * 34 + r() * 10]; });

  // ------------------------------------------------------------ drawing
  function withCam(g, cam) { g.setTransform(cam.zoom, 0, 0, cam.zoom, W / 2 - cam.x * cam.zoom, H / 2 - cam.y * cam.zoom); if (cam.rot) { g.translate(cam.x, cam.y); g.rotate(cam.rot); g.translate(-cam.x, -cam.y); } }
  function poly(g, pts) { g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]))); g.closePath(); }

  function drawDesk(g, o, cam) {
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = PAL.desk; g.fillRect(0, 0, W, H); g.restore();
    const pat = g.createPattern(woodTex, 'repeat');
    pat.setTransform(new DOMMatrix().scale(o.grain_scale || 3, o.grain_scale || 3));
    g.fillStyle = PAL.desk2; g.fillRect(o.x, o.y, o.w, o.h);
    g.fillStyle = pat; g.fillRect(o.x, o.y, o.w, o.h);
    const lc = o.light || [o.x + o.w / 2, o.y + o.h / 2, Math.max(o.w, o.h) * 0.45];
    const rg = g.createRadialGradient(lc[0], lc[1], 0, lc[0], lc[1], lc[2]);
    rg.addColorStop(0, 'rgba(255,200,130,0.16)'); rg.addColorStop(1, 'rgba(0,0,0,0.35)');
    g.fillStyle = rg; g.fillRect(o.x, o.y, o.w, o.h);
  }

  function drawMap(g, o, t) {
    const p = o.projection, w = o.w, h = o.h;
    g.save();
    g.shadowColor = 'rgba(0,0,0,0.6)'; g.shadowBlur = 80; g.shadowOffsetY = 30;
    g.fillStyle = PAL.paper; g.fillRect(o.x, o.y, w, h);
    g.restore();
    g.save(); g.beginPath(); g.rect(o.x, o.y, w, h); g.clip();
    g.fillStyle = PAL.land; g.fillRect(o.x, o.y, w, h);
    for (const s of (o.seas || [])) { poly(g, s.map((q) => geo(q[0], q[1]))); g.fillStyle = PAL.sea; g.fill(); g.strokeStyle = 'rgba(70,80,80,0.55)'; g.lineWidth = 3; g.stroke(); }
    g.strokeStyle = 'rgba(60,50,40,0.10)'; g.lineWidth = 2;
    const step = o.graticule || 5;
    for (let lon = Math.ceil(p.lon0 / step) * step; ; lon += step) { const a = geo(p.lat0, lon); if (a[0] > o.x + w) break; g.beginPath(); g.moveTo(a[0], o.y); g.lineTo(a[0], o.y + h); g.stroke(); }
    for (let lat = Math.floor(p.lat0 / step) * step; ; lat -= step) { const a = geo(lat, p.lon0); if (a[1] > o.y + h) break; g.beginPath(); g.moveTo(o.x, a[1]); g.lineTo(o.x + w, a[1]); g.stroke(); }
    for (const r of (o.rivers || [])) { g.beginPath(); r.forEach((q, i) => { const a = geo(q[0], q[1]); i ? g.lineTo(a[0], a[1]) : g.moveTo(a[0], a[1]); }); g.strokeStyle = 'rgba(80,110,120,0.7)'; g.lineWidth = 6; g.lineJoin = 'round'; g.stroke(); }
    const pat = g.createPattern(paperTex, 'repeat'); g.fillStyle = pat; g.fillRect(o.x, o.y, w, h);
    g.restore();
    g.strokeStyle = 'rgba(60,45,30,0.35)'; g.lineWidth = 4; g.strokeRect(o.x + 24, o.y + 24, w - 48, h - 48);
  }

  function drawArea(g, o, t) {
    const hs = hits[o.id] || [];
    let a = 0;
    for (const h of hs) a = Math.max(a, ramp(t, h.t - 0.1, 0.5) * (1 - ramp(t, PLAN.beats[h.beat].end + 0.3, 1.2)) * 0.9);
    a = Math.max(a, (o.rest || 0.18) * ramp(t, hs.length ? hs[0].t : 0, 0.5));
    if (a <= 0.001) return;
    const pts = o.poly.map((q) => geo(q[0], q[1]));
    g.save(); poly(g, pts); g.fillStyle = `rgba(217,169,58,${0.32 * a})`; g.fill();
    g.lineWidth = 8; g.strokeStyle = `rgba(217,169,58,${0.9 * a})`; g.stroke(); g.restore();
  }

  function drawPin(g, o, t) {
    const a = ramp(t, o.enter || 0, 0.4); if (a <= 0) return;
    const r = (o.r || 20) * easeBack(a);
    g.save(); g.fillStyle = PAL.red; g.beginPath(); g.arc(o.x, o.y, r, 0, Math.PI * 2); g.fill();
    g.lineWidth = r * 0.35; g.strokeStyle = '#fff3dc'; g.stroke(); g.restore();
  }

  function routePoint(pts, s) { // quadratic bezier through an arc control point
    const [a, b] = [pts[0], pts[pts.length - 1]];
    const c = pts.length > 2 ? pts[1] : [(a[0] + b[0]) / 2, Math.min(a[1], b[1]) - Math.hypot(b[0] - a[0], b[1] - a[1]) * 0.25];
    const u = 1 - s; return [u * u * a[0] + 2 * u * s * c[0] + s * s * b[0], u * u * a[1] + 2 * u * s * c[1] + s * s * b[1]];
  }
  function drawRoute(g, o, t) {
    const h = (hits[o.id] || []).find((x) => x.action === 'draw');
    if (!h) return;
    const s = ease((t - h.from) / (h.t - h.from));
    if (s <= 0) return;
    g.save(); g.lineCap = 'round'; g.setLineDash([o.dash || 34, o.gap || 26]);
    g.strokeStyle = PAL.red; g.lineWidth = o.width || 12; g.beginPath();
    const n = 120; for (let i = 0; i <= n * s; i++) { const q = routePoint(o.pts, i / n); i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1]); }
    g.stroke(); g.setLineDash([]);
    if (s < 1) { const q = routePoint(o.pts, s); const gl = g.createRadialGradient(q[0], q[1], 0, q[0], q[1], 60); gl.addColorStop(0, 'rgba(255,220,150,0.95)'); gl.addColorStop(1, 'rgba(255,200,120,0)'); g.fillStyle = gl; g.beginPath(); g.arc(q[0], q[1], 60, 0, 7); g.fill(); }
    g.restore();
  }

  function liftOf(o, t) { let l = 0; for (const h of (hits[o.id] || [])) if (h.action === 'lift') l = Math.max(l, easeOut((t - h.t) / 0.6)); return l; }
  function glowOf(o, t) { let l = 0; for (const h of (hits[o.id] || [])) if (h.action === 'glow') { const d = t - h.t; if (d > -0.1) l = Math.max(l, Math.exp(-Math.max(0, d) * 1.4) * ramp(t, h.t - 0.1, 0.15)); } return l; }

  function drawPhoto(g, o, t, f) {
    const s0 = (t - o.enter) / 0.75; if (s0 <= 0) return;
    const s = easeOut(s0), im = images[o.src];
    const iw = o.w, ih = o.w * im.naturalHeight / im.naturalWidth, pad = o.w * 0.035;
    const lift = liftOf(o, t);
    const sc = lerp(1.3, 1, s) * (1 + 0.05 * lift);
    const fall = (1 - s) * ih * 0.25;
    g.save(); g.translate(o.x, o.y - fall - lift * 18); g.rotate(((o.rot || 0) + (1 - s) * 7 - lift * (o.rot || 0) * 0.5) * Math.PI / 180); g.scale(sc, sc);
    g.globalAlpha = clamp(s0 * 4, 0, 1);
    g.shadowColor = PAL.shadow; g.shadowBlur = 30 + 60 * (1 - s) + 40 * lift; g.shadowOffsetY = 14 + 50 * (1 - s) + 26 * lift;
    g.fillStyle = '#f7f2e8'; g.fillRect(-iw / 2 - pad, -ih / 2 - pad, iw + 2 * pad, ih + 2 * pad * (o.polaroid ? 3 : 1));
    g.shadowColor = 'transparent';
    g.drawImage(im, -iw / 2, -ih / 2, iw, ih);
    const gl = glowOf(o, t);
    if (gl > 0) { g.globalCompositeOperation = 'screen'; g.fillStyle = `rgba(255,214,150,${0.35 * gl})`; g.fillRect(-iw / 2, -ih / 2, iw, ih); g.globalCompositeOperation = 'source-over'; }
    if (f < 1) { g.globalAlpha = 1; g.fillStyle = `rgba(10,7,4,${ST.dim * (1 - f)})`; g.fillRect(-iw / 2 - pad, -ih / 2 - pad, iw + 2 * pad, ih + 2 * pad * (o.polaroid ? 3 : 1)); }
    g.restore();
  }

  function drawText(g, o, t, f) {
    const s0 = (t - o.enter) / (o.wipe || 0.55); if (s0 <= 0) return;
    const lift = liftOf(o, t);
    const fade = o.exit != null ? 1 - ramp(t, o.exit, 0.5) : 1;
    if (fade <= 0) return;
    g.save(); g.translate(o.x, o.y - lift * o.size * 0.25);
    g.direction = 'rtl'; g.textAlign = 'center'; g.textBaseline = 'middle';
    const lines = String(o.text).split('\n');
    g.font = `${o.weight || 800} ${o.size}px "${o.font || FONT}"`;
    const wMax = Math.max(...lines.map((l) => g.measureText(l).width));
    const lh = o.size * 1.25, hTot = lh * lines.length;
    // RTL wipe: reveal from the right edge, whole words keep their shaping.
    const s = ease(s0);
    g.beginPath(); g.rect(wMax / 2 - (wMax + 40) * s - 20, -hTot, wMax + 80, hTot * 2); g.clip();
    g.globalAlpha = fade * (0.35 + 0.65 * f);
    if (o.plate) { g.fillStyle = o.plate; g.fillRect(-wMax / 2 - o.size * 0.5, -hTot / 2 - o.size * 0.25, wMax + o.size, hTot + o.size * 0.5); }
    g.shadowColor = 'rgba(0,0,0,0.55)'; g.shadowBlur = o.size * 0.15; g.shadowOffsetY = o.size * 0.04;
    g.fillStyle = o.color || PAL.text;
    lines.forEach((l, i) => { if (i && o.sub_size) g.font = `${o.sub_weight || 600} ${o.sub_size}px "${o.font || FONT}"`; g.fillText(l, 0, -hTot / 2 + lh * (i + 0.5)); });
    g.restore();
  }

  function drawBook(g, o, t, f) {
    const s0 = (t - (o.enter || 0)) / 0.7; if (s0 <= 0) return;
    const h = (hits[o.id] || []).find((x) => x.action === 'open');
    const op = h ? ease((t - h.t) / 0.9) : 0;
    const w = o.w, hh = o.w * 0.68, a = easeOut(s0);
    g.save(); g.translate(o.x, o.y - (1 - a) * 120); g.rotate((o.rot || 0) * Math.PI / 180); g.globalAlpha = clamp(s0 * 3, 0, 1);
    g.shadowColor = PAL.shadow; g.shadowBlur = 50; g.shadowOffsetY = 26;
    // right page block (always there), left half appears as the cover swings over the spine
    g.fillStyle = '#7a1f1a'; g.fillRect(-6, -hh / 2 - 10, w / 2 + 16, hh + 20);
    g.shadowColor = 'transparent';
    function page(x0, dir) {
      g.fillStyle = '#f6eedb'; g.fillRect(x0, -hh / 2, w / 2, hh);
      const sh = g.createLinearGradient(0, 0, dir * w * 0.12, 0); sh.addColorStop(0, 'rgba(0,0,0,0.22)'); sh.addColorStop(1, 'rgba(0,0,0,0)');
      g.fillStyle = sh; g.fillRect(dir > 0 ? 0 : -w * 0.12, -hh / 2, w * 0.12, hh);
      g.fillStyle = 'rgba(70,60,50,0.22)';
      const r = rng(o.seed || (x0 > 0 ? 3 : 4));
      for (let y = -hh / 2 + hh * 0.12; y < hh / 2 - hh * 0.1; y += hh * 0.075) {
        const len = (w / 2 - w * 0.12) * (0.7 + 0.3 * r());
        g.fillRect(dir > 0 ? w * 0.06 + (w / 2 - w * 0.12 - len) : -w * 0.06 - len, y, len, hh * 0.022);
      }
    }
    page(0, 1);
    if (op > 0) { g.save(); g.globalAlpha *= clamp(op * 2 - 0.4, 0, 1); page(-w / 2, -1); g.restore(); }
    // cover: scales from +1 (closed, over the right page) through 0 to -1 (resting on the left)
    const sx = Math.cos(op * Math.PI);
    if (sx > -0.98) {
      g.save(); g.scale(sx, 1);
      g.fillStyle = sx > 0 ? '#8c2620' : '#6d1a15'; g.fillRect(0, -hh / 2 - 10, w / 2 + 10, hh + 20);
      if (sx > 0) { g.strokeStyle = PAL.gold; g.lineWidth = 6; g.strokeRect(w * 0.06, -hh / 2 + hh * 0.08, w / 2 - w * 0.12, hh * 0.84); }
      g.restore();
    }
    const gl = op > 0 ? Math.sin(clamp(op, 0, 1) * Math.PI) * 0.6 + op * 0.25 : 0;
    if (gl > 0) { const rg = g.createRadialGradient(0, 0, 0, 0, 0, w * 0.6); rg.addColorStop(0, `rgba(255,220,150,${0.45 * gl})`); rg.addColorStop(1, 'rgba(255,220,150,0)'); g.globalCompositeOperation = 'screen'; g.fillStyle = rg; g.fillRect(-w, -w, 2 * w, 2 * w); g.globalCompositeOperation = 'source-over'; }
    if (f < 1) { g.fillStyle = `rgba(10,7,4,${ST.dim * (1 - f)})`; g.fillRect(-w / 2 - 12, -hh / 2 - 12, w + 30, hh + 24); }
    g.restore();
  }

  function stampState(o, t) { const h = (hits[o.id] || []).find((x) => x.action === 'stamp'); if (!h) return null; return { t0: h.t, s: (t - h.t + 0.12) / 0.16 }; }
  function drawStamp(g, o, t, f) {
    const st = stampState(o, t); if (!st || st.s <= 0) return;
    const s = clamp(st.s, 0, 1), sc = lerp(2.4, 1, easeOut(s));
    g.save(); g.translate(o.x, o.y); g.rotate((o.rot || -8) * Math.PI / 180); g.scale(sc, sc);
    g.globalAlpha = clamp(s * 1.5, 0, 1) * (0.55 + 0.45 * f) * 0.92;
    g.font = `900 ${o.size}px "${o.font || FONT}"`; g.direction = 'rtl'; g.textAlign = 'center'; g.textBaseline = 'middle';
    const tw = g.measureText(o.text).width, bw = tw + o.size * 0.9, bh = o.size * 1.55;
    g.strokeStyle = o.color || PAL.red; g.fillStyle = o.color || PAL.red; g.lineWidth = o.size * 0.09;
    g.strokeRect(-bw / 2, -bh / 2, bw, bh); g.lineWidth = o.size * 0.035; g.strokeRect(-bw / 2 + o.size * 0.16, -bh / 2 + o.size * 0.16, bw - o.size * 0.32, bh - o.size * 0.32);
    g.fillText(o.text, 0, o.size * 0.04);
    // worn ink: knock speckles out of the stamp
    g.globalCompositeOperation = 'destination-out';
    const r = rng(o.seed || 21); g.fillStyle = 'rgba(0,0,0,0.5)';
    for (let i = 0; i < 160; i++) { g.beginPath(); g.arc((r() - 0.5) * bw, (r() - 0.5) * bh, r() * o.size * 0.05, 0, 7); g.fill(); }
    g.restore();
  }

  function drawCircle(g, h, o, t) { // hand-drawn ring around the target, drawn as the word is said
    const b = PLAN.beats[h.beat];
    const s = ease((t - h.t + 0.05) / (h.dur || 0.6)); if (s <= 0) return;
    const fade = 1 - ramp(t, b.end, 0.6); if (fade <= 0) return;
    let cx, cy, rx, ry;
    if (o.kind === 'area') { const pts = o.poly.map((q) => geo(q[0], q[1])); const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]); cx = (Math.min(...xs) + Math.max(...xs)) / 2; cy = (Math.min(...ys) + Math.max(...ys)) / 2; rx = (Math.max(...xs) - Math.min(...xs)) * 0.62; ry = (Math.max(...ys) - Math.min(...ys)) * 0.62; }
    else { cx = o.x; cy = o.y; rx = h.r || 140; ry = (h.r || 140) * 0.85; }
    g.save(); g.strokeStyle = h.color || PAL.gold; g.lineCap = 'round'; g.lineWidth = h.width || Math.max(rx, ry) * 0.035; g.globalAlpha = fade;
    g.beginPath(); const n = 90, end = 1.08 * s;
    for (let i = 0; i <= n * end; i++) { const u = i / n, a = -Math.PI * 0.6 - u * Math.PI * 2, w = 1 + noise1(u * 6, 7) * 0.05; const x = cx + Math.cos(a) * rx * w, y = cy + Math.sin(a) * ry * w; i ? g.lineTo(x, y) : g.moveTo(x, y); }
    g.stroke(); g.restore();
  }

  function drawWorld(g, cam, t) {
    withCam(g, cam);
    const heroDim = anyHero(t);
    for (const o of objs) {
      const f = focusOf(o.id, t);
      switch (o.kind) {
        case 'desk': drawDesk(g, o, cam); break;
        case 'map': drawMap(g, o, t); break;
        case 'area': drawArea(g, o, t); break;
        case 'pin': drawPin(g, o, t); break;
        case 'route': drawRoute(g, o, t); break;
        case 'photo': drawPhoto(g, o, t, Math.max(f, 1 - heroDim)); break;
        case 'text': drawText(g, o, t, Math.max(f, 1 - heroDim)); break;
        case 'book': drawBook(g, o, t, Math.max(f, 1 - heroDim)); break;
        case 'stamp': drawStamp(g, o, t, Math.max(f, 1 - heroDim)); break;
        default: break;
      }
      if (o.kind === 'route' || o.kind === 'map') {
        // world dims behind a hero: one veil after the map and route are drawn
        if (o.kind === 'map' && heroDim > 0) { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = `rgba(8,5,3,${ST.dim * 0.75 * heroDim})`; g.fillRect(0, 0, W, H); g.restore(); }
      }
    }
    for (const id in hits) for (const h of hits[id]) if (h.action === 'circle') drawCircle(g, h, byId[id], t);
  }

  // ------------------------------------------------------------ camera with handheld + shake
  function shake(t) {
    let s = 0;
    for (const o of objs) { const st = o.kind === 'stamp' && stampState(o, t); if (st) { const d = t - st.t0 - 0.04; if (d > 0) s += Math.exp(-d * 9) * (o.shake != null ? o.shake : 9); } }
    return s;
  }
  function cameraAt(t) {
    const c = window.KosifCamera.camera(KEYS, t);
    const hh = ST.handheld, sk = shake(t);
    c.x += (noise1(t * 0.55, 1) * 7 + noise1(t * 1.7, 2) * 2.2) * hh / c.zoom + noise1(t * 40, 4) * sk / c.zoom;
    c.y += (noise1(t * 0.5, 5) * 7 + noise1(t * 1.9, 6) * 2.2) * hh / c.zoom + noise1(t * 40, 8) * sk / c.zoom;
    c.rot = (noise1(t * 0.35, 9) * 0.0035) * hh;
    return c;
  }

  // ------------------------------------------------------------ frame
  function frame(t) {
    const dt = 1 / FPS;
    const a = window.KosifCamera.camera(KEYS, t - dt / 2), b = window.KosifCamera.camera(KEYS, t + dt / 2);
    const speed = Math.hypot((b.x - a.x) * b.zoom, (b.y - a.y) * b.zoom) + Math.abs(Math.log(b.zoom / a.zoom)) * W * 0.5; // screen px per frame
    const n = ST.blur ? clamp(Math.ceil(speed / 7), 1, 7) : 1;
    if (n === 1) { sctx.setTransform(1, 0, 0, 1, 0, 0); drawWorld(sctx, cameraAt(t), t); }
    else {
      // 180-degree shutter: n sub-frames across half a frame, averaged.
      for (let i = 0; i < n; i++) {
        const ts = t + (i / (n - 1) - 0.5) * dt * 0.5;
        const target = i === 0 ? sctx : actx;
        target.setTransform(1, 0, 0, 1, 0, 0); drawWorld(target, cameraAt(ts), t);
        if (i > 0) { sctx.setTransform(1, 0, 0, 1, 0, 0); sctx.globalAlpha = 1 / (i + 1); sctx.drawImage(acc, 0, 0); sctx.globalAlpha = 1; }
      }
    }
    out.setTransform(1, 0, 0, 1, 0, 0); out.globalAlpha = 1; out.globalCompositeOperation = 'source-over';
    out.drawImage(scene, 0, 0);
    // soft glow: blurred highlights screened back on
    smctx.filter = 'blur(5px) brightness(1.15)'; smctx.clearRect(0, 0, small.width, small.height); smctx.drawImage(scene, 0, 0, small.width, small.height); smctx.filter = 'none';
    out.globalCompositeOperation = 'screen'; out.globalAlpha = ST.glow; out.drawImage(small, 0, 0, W, H);
    // vignette
    out.globalCompositeOperation = 'source-over'; out.globalAlpha = 1;
    const vg = out.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.35, W / 2, H / 2, Math.hypot(W, H) * 0.62);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, `rgba(0,0,0,${ST.vignette})`);
    out.fillStyle = vg; out.fillRect(0, 0, W, H);
    // film grain: a different seeded tile every frame
    const fi = Math.round(t * FPS);
    const pat = out.createPattern(grains[fi % grains.length], 'repeat');
    pat.setTransform(new DOMMatrix().translate((fi * 37) % 256, (fi * 91) % 256).scale(1.5, 1.5));
    out.globalCompositeOperation = 'overlay'; out.globalAlpha = ST.grain; out.fillStyle = pat; out.fillRect(0, 0, W, H);
    out.globalCompositeOperation = 'source-over'; out.globalAlpha = 1;
    // fade from and to black
    const fin = PLAN.fade_in != null ? PLAN.fade_in : 0.6, fout = PLAN.fade_out != null ? PLAN.fade_out : 1.2;
    const k = Math.min(fin ? ramp(t, 0, fin) : 1, fout ? 1 - ramp(t, PLAN.duration - fout, fout) : 1);
    if (k < 1) { out.fillStyle = `rgba(0,0,0,${1 - ease(k)})`; out.fillRect(0, 0, W, H); }
  }

  window.__kosifReady = Promise.all(loads).then(() => document.fonts.ready).then(() => frame(0));
  window.__kosif = { duration: PLAN.duration, seek: (t) => frame(t), camera: (t) => cameraAt(t) };
})();
