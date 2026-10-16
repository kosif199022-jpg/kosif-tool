/* whiteboard-draw — scene data + schedule (pure math, no DOM).
 * Shared by index.html (picture) and sound.py (via `node scene.js > schedule.json`).
 * Every stroke is a centre-line polyline in stage px (1080×1920). Timing is derived from
 * arc length, so editing a shape re-times the whole film automatically.
 * Original code, MIT — part of KOSIF TOOL.
 */
(function (root) {
  'use strict';
  const INK = { black: '#1e2330', blue: '#1f5fd1', red: '#d6332b' };

  /* ---- seeded randomness (mulberry32) + smooth 1D noise ---- */
  function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let z = s; z = Math.imul(z ^ (z >>> 15), z | 1); z ^= z + Math.imul(z ^ (z >>> 7), z | 61); return ((z ^ (z >>> 14)) >>> 0) / 4294967296; }; }
  const R = rng(20261016);
  function noise1(seed) { const k = Array.from({ length: 64 }, () => R() * 2 - 1); return (x) => { const i = Math.floor(x), f = x - i, a = k[((i % 64) + 64) % 64], b = k[(((i + 1) % 64) + 64) % 64], u = f * f * (3 - 2 * f); return a + (b - a) * u; }; }

  /* ---- path generators (dense centre lines) ---- */
  const line = (a, b, n = 40) => Array.from({ length: n + 1 }, (_, i) => [a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n]);
  const arc = (cx, cy, rx, ry, a0, a1, n = 90) => Array.from({ length: n + 1 }, (_, i) => { const a = a0 + (a1 - a0) * i / n; return [cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]; });
  function bez(p0, p1, p2, p3, n = 60) {
    return Array.from({ length: n + 1 }, (_, i) => { const t = i / n, u = 1 - t; return [u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0], u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]]; });
  }
  const join = (...parts) => parts.reduce((acc, p) => acc.concat(acc.length ? p.slice(1) : p), []);

  /* hand wobble: low-frequency perpendicular offset, amplitude in px */
  function wobble(pts, amp = 1.6, freq = 0.012) {
    const nz = noise1(), off = R() * 50;
    let s = 0; const out = [];
    for (let i = 0; i < pts.length; i++) {
      if (i) s += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1]; const l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l;
      const d = nz(off + s * freq) * amp;
      out.push([pts[i][0] - ty * d, pts[i][1] + tx * d]);
    }
    return out;
  }
  /* resample to equal spacing; returns {pts, s (cumulative), L} */
  function resample(pts, step = 2.5) {
    const out = [pts[0]], s = [0]; let acc = 0, carry = 0;
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1], b = pts[i], seg = Math.hypot(b[0] - a[0], b[1] - a[1]);
      let d = step - carry;
      while (d <= seg) { const f = d / seg; out.push([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]); acc += step; s.push(acc); d += step; }
      carry = seg - (d - step);
    }
    const last = pts[pts.length - 1], pl = out[out.length - 1], tail = Math.hypot(last[0] - pl[0], last[1] - pl[1]);
    if (tail > 0.2) { out.push(last); acc += tail; s.push(acc); }
    return { pts: out, s, L: acc };
  }

  /* ---- hatching: parallel wavy lines across a shape's bbox, alternating direction (zig-zag like a hand) ---- */
  function hatch(shape, angleDeg, spacing, extend = 14) {
    const xs = shape.map((p) => p[0]), ys = shape.map((p) => p[1]);
    const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cy = (Math.min(...ys) + Math.max(...ys)) / 2;
    const r = Math.hypot(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)) / 2 + extend;
    const a = angleDeg * Math.PI / 180, dx = Math.cos(a), dy = Math.sin(a), nx = -dy, ny = dx;
    const lines = [];
    // keep only the chords that actually cross the shape: measure each chord against the polygon
    for (let o = -r, k = 0; o <= r; o += spacing, k++) {
      const c = [cx + nx * o, cy + ny * o];
      const hits = chordHits(shape, c, [dx, dy]);
      if (hits.length < 2) continue;
      const t0 = Math.min(...hits) - extend, t1 = Math.max(...hits) + extend;
      let A = [c[0] + dx * t0, c[1] + dy * t0], B = [c[0] + dx * t1, c[1] + dy * t1];
      if (k % 2) [A, B] = [B, A];
      lines.push(line(A, B, 24));
    }
    // one continuous zig-zag (the pen never lifts while hatching), wobbled as a whole
    return wobble(lines.reduce((acc, l) => acc.concat(l), []), 1.2, 0.02);
  }
  function chordHits(poly, c, d) {
    const out = [];
    for (let i = 0; i < poly.length - 1; i++) {
      const p = poly[i], q = poly[i + 1], ex = q[0] - p[0], ey = q[1] - p[1];
      const den = d[0] * ey - d[1] * ex; if (Math.abs(den) < 1e-9) continue;
      const t = ((p[0] - c[0]) * ey - (p[1] - c[1]) * ex) / den;
      const u = ((p[0] - c[0]) * d[1] - (p[1] - c[1]) * d[0]) / den;
      if (u >= 0 && u <= 1) out.push(t);
    }
    return out;
  }
  /* arrow head as one "V" gesture: wing → tip → wing */
  function arrowHead(tip, from, len = 38, spread = 0.5) {
    const a = Math.atan2(tip[1] - from[1], tip[0] - from[0]);
    return join(line([tip[0] - Math.cos(a - spread) * len, tip[1] - Math.sin(a - spread) * len], tip, 12),
      line(tip, [tip[0] - Math.cos(a + spread) * len, tip[1] - Math.sin(a + spread) * len], 12));
  }

  /* ---------------- the drawing, in human order ---------------- */
  const items = [];   // {type:'stroke'|'text', ink, size, pts?, clip?, group, ...}
  const clips = {};
  const S = (pts, ink, size, group, extra = {}) => items.push({ type: 'stroke', ink, size, group, pts: wobble(pts, extra.wob ?? 1.6), ...extra });
  const T = (text, x, y, px, ink, group, dur) => items.push({ type: 'text', text, x, y, px, ink, group, dur });

  // 1 · title (written right → left) + red underline drawn right → left
  T('كيف تنمو النبتة؟', 540, 300, 128, 'black', 'title', 1.0);
  S(bez([930, 362], [700, 346], [400, 380], [150, 356]), 'red', 11, 'title');

  // 2 · sun (cause 1): circle with overshoot, 8 rays, red hatching clipped to the disc
  const SUN = [770, 650], SR = 100;
  const sunShape = arc(SUN[0], SUN[1], SR, SR, 0, Math.PI * 2, 120);
  clips.sun = sunShape;
  S(arc(SUN[0], SUN[1], SR + 2, SR - 2, -2.2, -2.2 + Math.PI * 2 * 1.06, 140), 'red', 10, 'sun');
  S(hatch(sunShape, -35, 19), 'red', 5.5, 'sun', { clip: 'sun', hatch: true, wob: 0 });
  for (let i = 0; i < 8; i++) {
    const a = -Math.PI / 2 + i * Math.PI / 4;
    S(line([SUN[0] + Math.cos(a) * 128, SUN[1] + Math.sin(a) * 128], [SUN[0] + Math.cos(a) * 178, SUN[1] + Math.sin(a) * 178], 14), 'red', 9, 'sun', { wob: 0.8 });
  }
  T('شمس', 770, 905, 84, 'red', 'sun', 0.35);

  // 3 · water drop (cause 2): one continuous outline, blue hatching clipped to it
  const D = [310, 690], DR = 92;
  const dropShape = join(bez([D[0], 515], [D[0] + 30, 575], [D[0] + DR, 625], [D[0] + DR, D[1]]), arc(D[0], D[1], DR, DR, 0, Math.PI, 70), bez([D[0] - DR, D[1]], [D[0] - DR, 625], [D[0] - 30, 575], [D[0], 515]));
  clips.drop = dropShape;
  S(dropShape, 'blue', 10, 'drop');
  S(hatch(dropShape, 35, 19), 'blue', 5.5, 'drop', { clip: 'drop', hatch: true, wob: 0 });
  T('ماء', 310, 905, 84, 'blue', 'drop', 0.35);

  // 4 · cause → effect arrows (curved, black)
  const a1 = bez([735, 960], [720, 1030], [665, 1080], [610, 1110], 50);
  S(a1, 'black', 9, 'arrows'); S(arrowHead(a1[a1.length - 1], a1[a1.length - 6]), 'black', 9, 'arrows', { wob: 0.6 });
  const a2 = bez([345, 960], [360, 1030], [415, 1080], [470, 1110], 50);
  S(a2, 'black', 9, 'arrows'); S(arrowHead(a2[a2.length - 1], a2[a2.length - 6]), 'black', 9, 'arrows', { wob: 0.6 });

  // 5 · plant (effect): pot rim, pot body + cross-hatching, stem, two leaves with blue hatching
  const rim = [[402, 1318], [678, 1318], [672, 1360], [408, 1360], [402, 1318]];
  const pot = [[420, 1360], [660, 1360], [628, 1520], [452, 1520], [420, 1360]];
  clips.pot = pot;
  S(join(line(rim[0], rim[1], 30), line(rim[1], rim[2], 6), line(rim[2], rim[3], 30), line(rim[3], rim[4], 6)), 'black', 9, 'plant');
  S(join(line(pot[0], pot[3], 20), line(pot[3], pot[2], 20), line(pot[2], pot[1], 20)), 'black', 9, 'plant');
  S(hatch(pot, 45, 24), 'black', 4.5, 'plant', { clip: 'pot', hatch: true, wob: 0 });
  S(hatch(pot, -45, 24), 'black', 4.5, 'plant', { clip: 'pot', hatch: true, wob: 0 });
  S(bez([540, 1318], [536, 1260], [552, 1200], [546, 1130], 50), 'black', 9, 'plant');
  const leafL = join(bez([540, 1250], [500, 1205], [450, 1195], [418, 1178], 30), bez([418, 1178], [440, 1236], [492, 1262], [540, 1250], 30));
  const leafR = join(bez([548, 1196], [588, 1150], [630, 1136], [668, 1124], 30), bez([668, 1124], [650, 1180], [600, 1210], [548, 1196], 30));
  clips.leafL = leafL; clips.leafR = leafR;
  S(leafL, 'black', 8, 'plant'); S(hatch(leafL, 70, 15, 8), 'blue', 4.5, 'plant', { clip: 'leafL', hatch: true, wob: 0 });
  S(leafR, 'black', 8, 'plant'); S(hatch(leafR, 110, 15, 8), 'blue', 4.5, 'plant', { clip: 'leafR', hatch: true, wob: 0 });

  // 6 · result: arrow down, «النتيجة: نمو», red loop around «نمو»
  const a3 = line([540, 1550], [540, 1630], 20);
  S(a3, 'black', 9, 'result'); S(arrowHead(a3[a3.length - 1], a3[0], 30), 'black', 9, 'result', { wob: 0.6 });
  T('النتيجة:', 650, 1760, 92, 'black', 'result', 0.45);
  T('نمو', 350, 1760, 104, 'red', 'result', 0.3);
  S(arc(352, 1728, 128, 74, -1.2, -1.2 + Math.PI * 2 * 1.08, 120), 'red', 10, 'result');

  /* ---------------- schedule: arc-length timing ---------------- */
  const SPEED = 3000, HATCH_SPEED = 5600;     // px/s centre-line speed (hatching is a fast scribble)
  const GAP = 0.055, SHORT_GAP = 0.03, GROUP_GAP = 0.17;
  let t = 0.3, prev = null;
  for (const it of items) {
    if (it.type === 'stroke') {
      const r = resample(it.pts); it.pts = r.pts; it.s = r.s; it.L = r.L;
      it.dur = Math.max(0.07, it.L / (it.hatch ? HATCH_SPEED : SPEED));
    }
    const gap = !prev ? 0 : prev.group !== it.group ? GROUP_GAP : (it.L || 99) < 60 && (prev.L || 99) < 60 ? SHORT_GAP : GAP;
    t += gap; it.t0 = t; it.t1 = t + it.dur; t = it.t1; prev = it;
  }
  const END = t;
  const DURATION = 10;   // drawing ends at END ≈ 9.23 s, then a short hold

  /* stroke progress easing: humans accelerate then brake. e(u) = 0.55·inOutSine + 0.45·u ; e'(u) is the pen speed */
  const ease = (u) => 0.55 * (0.5 - 0.5 * Math.cos(Math.PI * u)) + 0.45 * u;
  const easeVel = (u) => 0.55 * 0.5 * Math.PI * Math.sin(Math.PI * u) + 0.45;   // max ≈ 1.314

  const SCENE = { INK, items, clips, DURATION, END, ease, easeVel, rng };
  root.WB_SCENE = SCENE;
  // `node scene.js` (the repo is "type": "module", so this runs as ESM): print the schedule as JSON for sound.py
  if (typeof window === 'undefined' && typeof process !== 'undefined' && /scene\.js$/.test(process.argv[1] || '')) {
    const out = { duration: DURATION, end: END, items: items.map((i) => ({ type: i.type, ink: i.ink, group: i.group, hatch: !!i.hatch, t0: +i.t0.toFixed(4), t1: +i.t1.toFixed(4), L: i.L ? +i.L.toFixed(1) : 0, x0: Math.round(i.pts ? i.pts[0][0] : i.x + 150), x1: Math.round(i.pts ? i.pts[i.pts.length - 1][0] : i.x - 150), text: i.text })) };
    process.stdout.write(JSON.stringify(out, null, 1));
  }
})(typeof window !== 'undefined' ? window : globalThis);
