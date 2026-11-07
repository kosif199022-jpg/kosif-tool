/*
 * KOSIF World Film camera («التنين الأسود», one continuous camera over one world).
 *
 * The camera is a pure function of time built from the plan's beats:
 *   - every beat has a target {x, y, zoom}; the camera arrives a little after the beat starts,
 *   - during the hold it keeps drifting at a constant slow speed toward the next target (never a dead stop),
 *   - each travel eases out of that drift and back into the next one (quintic Hermite: velocity AND
 *     acceleration are continuous, so every start and stop eases in and out),
 *   - long moves pull back to travel and dive in again (an automatic mid key),
 *   - a travel gets at least the time it needs to stay under a set acceleration, so nothing lurches.
 * Handheld sway and stamp shake are added on top by the engine, not here, so the checker measures
 * the designed move itself.
 *
 * Used by engine.js in the page (inlined) and by world_film.py through Node:
 *   node camera.cjs PLAN.json [--fps 30]   -> JSON {keys, samples:[[t,x,y,zoom],...]}
 * License: MIT (part of KOSIF TOOL).
 */
(function (root) {
  'use strict';

  // travel: minimum seconds per move; drift: share of the way to the next target covered during a hold;
  // split: share of a travel before the beat boundary (default 0.55); pullback: screens of distance that trigger the pull-back; pull_depth: how far it pulls back (share of
  // the closer shot's zoom); max_accel: screen px per frame^2 a move may reach.
  const DEF = { travel: 1.3, drift: 0.07, pullback: 1.6, pull_depth: 0.33, max_accel: 1.6 };

  function buildKeys(plan) {
    const W = plan.format.width;
    const H = plan.format.height;
    const fps = plan.format.fps || 30;
    const beats = plan.beats;
    const cam = Object.assign({}, DEF, plan.camera || {});
    const P = (c) => [c.x, c.y, Math.log(c.zoom)];
    const T = beats.map(() => 0); // travel time from beat i to beat i+1
    // share of each travel spent before the beat boundary (camera.split on the arriving beat)
    const S = beats.map((b, i) => (beats[i + 1] && beats[i + 1].camera.split != null ? beats[i + 1].camera.split : 0.55));
    const mids = beats.map(() => null);
    for (let i = 0; i + 1 < beats.length; i++) {
      const a = P(beats[i].camera), b = P(beats[i + 1].camera);
      const zA = Math.exp(a[2]), zB = Math.exp(b[2]);
      const dx = b[0] - a[0], dy = b[1] - a[1], dist = Math.hypot(dx, dy);
      const zFit = Math.min(W * 0.92 / (Math.abs(dx) + W / Math.min(zA, zB) * 0.55),
        H * 0.92 / (Math.abs(dy) + H / Math.min(zA, zB) * 0.55));
      const pull = beats[i + 1].camera.pullback != null ? beats[i + 1].camera.pullback : cam.pullback;
      const screens = Math.hypot(dx * zA / W, dy * zA / H);
      let delta; // screen px the move covers (pan at the zoom it travels at, plus zoom change)
      if (pull && screens > pull && zFit < Math.min(zA, zB) * 0.85) {
        const zMid = Math.max(zFit, Math.min(zA, zB) * cam.pull_depth);
        mids[i] = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, Math.log(zMid)];
        delta = dist * zMid + (Math.abs(a[2] - mids[i][2]) + Math.abs(b[2] - mids[i][2])) * W * 0.5;
        delta *= 1.6; // three legs (pull back, pan, dive in) in the same time
      } else {
        delta = dist * Math.sqrt(zA * zB) + Math.abs(b[2] - a[2]) * W * 0.5;
      }
      const need = Math.sqrt(6 * delta / cam.max_accel) / fps; // quintic peak acceleration ~ 5.8 * delta / T^2
      const asked = beats[i + 1].camera.travel != null ? beats[i + 1].camera.travel : cam.travel;
      const room = Math.min(beats[i].end - beats[i].start, beats[i + 1].end - beats[i + 1].start) * 0.9 + 0.5;
      T[i] = Math.max(asked, Math.min(need, room));
    }
    const keys = [];
    for (let i = 0; i < beats.length; i++) {
      const b = beats[i];
      const next = beats[i + 1];
      const p = P(b.camera);
      let tIn = i === 0 ? 0 : b.start + T[i - 1] * (1 - S[i - 1]);
      const tOut = next ? b.end - T[i] * S[i] : plan.duration;
      if (i === 0 && b.camera.from) {
        keys.push({ t: 0, p: P(b.camera.from), beat: 0, kind: 'from' });
        tIn = Math.min(b.start + (b.camera.from_time || 1.2), (b.start + b.end) / 2);
      }
      const drift = b.camera.drift != null ? b.camera.drift : cam.drift;
      let pOut;
      if (next) {
        const q = P(next.camera);
        pOut = [0, 1, 2].map((j) => p[j] + (q[j] - p[j]) * drift);
      } else {
        // last beat: keep gliding the way the camera arrived (a slow settle) and push in
        const prev = i > 0 ? P(beats[i - 1].camera) : p;
        pOut = [p[0] + (p[0] - prev[0]) * drift * 0.6, p[1] + (p[1] - prev[1]) * drift * 0.6, p[2] + Math.log(b.camera.end_push || 1.08)];
      }
      if (tOut - tIn < 0.3) {
        keys.push({ t: (tIn + tOut) / 2, p: [0, 1, 2].map((j) => (p[j] + pOut[j]) / 2), beat: i, kind: 'hold' });
      } else {
        keys.push({ t: tIn, p: p, beat: i, kind: 'arrive' });
        keys.push({ t: tOut, p: pOut, beat: i, kind: 'leave' });
      }
      if (next && mids[i]) {
        // pull back first, pan while wide, dive in last: two keys at the pulled-back zoom
        const nIn = next.start + T[i] * (1 - S[i]);
        const q = P(next.camera);
        const at = (u) => [p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u, mids[i][2]];
        keys.push({ t: tOut + (nIn - tOut) * 0.36, p: at(0.2), beat: i, kind: 'travel', u: 0.36 });
        keys.push({ t: tOut + (nIn - tOut) * 0.64, p: at(0.8), beat: i, kind: 'travel', u: 0.64 });
      }
    }
    keys.sort((u, v) => u.t - v.t);
    // a pull-back sits halfway (in time) between the keys it really joins
    for (let k = 1; k + 2 < keys.length; k++) {
      if (keys[k].kind === 'travel' && keys[k + 1].kind === 'travel') {
        const a = keys[k - 1].t, b = keys[k + 2].t;
        keys[k].t = a + (b - a) * 0.36; keys[k + 1].t = a + (b - a) * 0.64; k++;
      }
    }
    // Velocities: at a hold's two keys the hold's own constant drift (so the hold is a steady glide and
    // each travel eases out of it and back into the next); elsewhere a centred difference.
    for (let k = 0; k < keys.length; k++) {
      const b = keys[k];
      const a = keys[Math.max(0, k - 1)];
      const c = keys[Math.min(keys.length - 1, k + 1)];
      if (b.kind === 'arrive' && c.kind === 'leave' && c.beat === b.beat) b.m = slope(b, c);
      else if (b.kind === 'leave' && a.kind === 'arrive' && a.beat === b.beat) b.m = slope(a, b);
      else b.m = [0, 1, 2].map((j) => (c.p[j] - a.p[j]) / ((c.t - a.t) || 1));
    }
    return keys;
  }

  function slope(a, b) { return [0, 1, 2].map((j) => (b.p[j] - a.p[j]) / ((b.t - a.t) || 1)); }

  // Quintic Hermite with zero end accelerations: C1 position, continuous velocity, eased acceleration.
  function hermite5(p0, p1, m0, m1, dt, s) {
    const s3 = s * s * s, s4 = s3 * s, s5 = s4 * s;
    const h0 = 1 - 10 * s3 + 15 * s4 - 6 * s5;
    const h1 = s - 6 * s3 + 8 * s4 - 3 * s5;
    const h4 = -4 * s3 + 7 * s4 - 3 * s5;
    const h5 = 10 * s3 - 15 * s4 + 6 * s5;
    return [0, 1, 2].map((j) => h0 * p0[j] + h1 * dt * m0[j] + h4 * dt * m1[j] + h5 * p1[j]);
  }

  function at(keys, t) {
    if (t <= keys[0].t) { const k = keys[0]; return k.p.map((v, j) => v + k.m[j] * (t - k.t)); }
    const last = keys[keys.length - 1];
    if (t >= last.t) return last.p.map((v, j) => v + last.m[j] * (t - last.t));
    let i = 0;
    while (i < keys.length - 2 && keys[i + 1].t <= t) i++;
    const a = keys[i], b = keys[i + 1];
    const dt = b.t - a.t;
    return hermite5(a.p, b.p, a.m, b.m, dt, (t - a.t) / dt);
  }

  function camera(keys, t) {
    const v = at(keys, t);
    return { x: v[0], y: v[1], zoom: Math.exp(v[2]) };
  }

  function samples(plan, fps) {
    const keys = buildKeys(plan);
    const out = [];
    const n = Math.round(plan.duration * fps);
    for (let f = 0; f <= n; f++) {
      const t = f / fps;
      const c = camera(keys, t);
      out.push([+t.toFixed(4), +c.x.toFixed(3), +c.y.toFixed(3), +c.zoom.toFixed(5)]);
    }
    return { keys: keys.map((k) => ({ t: +k.t.toFixed(3), kind: k.kind, beat: k.beat })), samples: out };
  }

  const api = { buildKeys, camera, samples };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.KosifCamera = api;

  if (typeof require !== 'undefined' && typeof module !== 'undefined' && require.main === module) {
    const fs = require('fs');
    const argv = process.argv.slice(2);
    const plan = JSON.parse(fs.readFileSync(argv[0], 'utf8'));
    const i = argv.indexOf('--fps');
    const fps = i >= 0 ? Number(argv[i + 1]) : (plan.format.fps || 30);
    process.stdout.write(JSON.stringify(samples(plan, fps)));
  }
})(typeof window !== 'undefined' ? window : globalThis);
