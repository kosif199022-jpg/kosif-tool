/* character-rig — motion data (pure math, no DOM).
 * Root motion, walk-cycle phase, jump arc, expressions, speech timing and sound events.
 * Shared by index.html and sound.py (`node motion.js > events.json`).
 * Original code, MIT — part of KOSIF TOOL.
 */
(function (root) {
  'use strict';
  const DURATION = 9.5;
  const GROUND = 880;               // world y of the ground line
  const HIP_H = 214;                // standing hip height above ground (legs 2 × 116, slightly bent)
  const STRIDE = 118;               // one step (one foot) in px; a full cycle C = 2 · STRIDE
  const C = 2 * STRIDE;
  const X0 = 260;                   // hip start x (world)
  const VMAX = 290;                 // walking speed px/s  → cadence = VMAX / STRIDE ≈ 2.46 steps/s

  // ---- key times (s) ----
  const T = {
    walkIn: [0.2, 0.75],            // accelerate 0 → VMAX (inOutSine)
    brake: [2.95, 3.55],            // decelerate VMAX → 0 (outCubic-like)
    settle: [3.5, 3.78],            // trailing foot steps next to the planted one
    notice: 3.62,                   // surprised face + "!" pop
    crouch: [4.12, 4.56],           // anticipation: hips drop 62 px, body squashes
    air: [4.56, 5.36],              // ballistic flight (constant g)
    land: [5.36, 5.98],             // squash on impact → spring back (follow-through)
    talk: [6.35, 8.55],             // speech bubble + mouth
  };

  // speed profile v(t) and its integral d(t) (tabulated, 600 Hz) — deterministic for any seek
  const ss = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : 0.5 - 0.5 * Math.cos(Math.PI * x));
  function speed(t) {
    const a = ss((t - T.walkIn[0]) / (T.walkIn[1] - T.walkIn[0]));
    const b = 1 - ss((t - T.brake[0]) / (T.brake[1] - T.brake[0]));
    return VMAX * Math.min(a, b);
  }
  const HZ = 600, NT = Math.ceil(DURATION * HZ) + 2, DT = new Float64Array(NT);
  for (let i = 1; i < NT; i++) DT[i] = DT[i - 1] + (speed((i - 0.5) / HZ)) / HZ;
  function dist(t) { const x = Math.max(0, Math.min(NT - 1.001, t * HZ)), i = Math.floor(x), f = x - i; return DT[i] + (DT[i + 1] - DT[i]) * f; }
  const D_STOP = dist(T.brake[1] + 0.01);

  // jump: take-off/landing hip positions
  const JUMP = { x0: X0 + D_STOP, x1: X0 + D_STOP + 560, apex: 300 };
  const CRATE = { x: JUMP.x0 + 150, w: 170, h: 150 };   // the obstacle sits 150 px ahead of the stop point

  // ---- footsteps (contact = start of a foot's stance) ----
  // foot A cycle c = (d / C) mod 1 (stance 0 … 0.5), foot B is shifted by half a cycle.
  const events = [];
  for (let i = 1; i < NT - 1; i++) {
    const t = i / HZ, d0 = DT[i - 1], d1 = DT[i];
    if (t > T.brake[1]) break;
    for (const [foot, off] of [['A', 0], ['B', 0.5]]) {
      const c0 = Math.floor(d0 / C + off), c1 = Math.floor(d1 / C + off);
      if (c1 > c0 && d1 > 1) events.push({ t: +t.toFixed(4), type: 'step', foot, x: X0 + c1 * C - off * C + STRIDE / 2, v: speed(t) / VMAX });
    }
  }
  events.push({ t: T.settle[1] - 0.04, type: 'step', foot: 'settle', x: JUMP.x0, v: 0.5 });
  events.push({ t: T.notice, type: 'notice', x: JUMP.x0 });
  events.push({ t: T.crouch[0], type: 'crouch', x: JUMP.x0 });
  events.push({ t: T.air[0], type: 'takeoff', x: JUMP.x0 });
  events.push({ t: T.air[1], type: 'land', x: JUMP.x1 });
  events.push({ t: T.talk[0], type: 'bubble', x: JUMP.x1 });

  // speech: whole Arabic words (never split letters), each with its own start
  const SPEECH = [
    { w: 'قفزةٌ', t: 6.62 }, { w: 'واحدة…', t: 6.98 }, { w: 'وصارت', t: 7.5 }, { w: 'العقبةُ', t: 7.86 }, { w: 'خلفي!', t: 8.22 },
  ];
  for (const s of SPEECH) events.push({ t: s.t, type: 'word', w: s.w, x: JUMP.x1 });
  events.sort((a, b) => a.t - b.t);

  const M = { DURATION, GROUND, HIP_H, STRIDE, C, X0, VMAX, CRATE, T, JUMP, SPEECH, speed, dist, D_STOP, events };
  root.RIG_MOTION = M;
  if (typeof window === 'undefined' && typeof process !== 'undefined' && /motion\.js$/.test(process.argv[1] || '')) {
    process.stdout.write(JSON.stringify({ duration: DURATION, events }, null, 1));
  }
})(typeof window !== 'undefined' ? window : globalThis);
