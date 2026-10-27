/**
 * Dependency-free easing helpers. Every function maps t in [0, 1] to [0, 1]
 * and can be passed straight to Remotion's `interpolate(..., { easing })`.
 */
export type Ease = (t: number) => number;

export const clamp01 = (t: number): number => (t < 0 ? 0 : t > 1 ? 1 : t);

export const linear: Ease = (t) => t;

export const easeOutCubic: Ease = (t) => 1 - Math.pow(1 - t, 3);

export const easeInOutCubic: Ease = (t) =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

export const easeOutExpo: Ease = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));

export const easeInOutSine: Ease = (t) => -(Math.cos(Math.PI * t) - 1) / 2;

/** Overshoots slightly past 1 before settling; good for pops and pills. */
export const easeOutBack: Ease = (t) => {
  const c = 1.70158;
  const u = t - 1;
  return 1 + (c + 1) * u * u * u + c * u * u;
};

/**
 * Eased progress (0 -> 1) of a window that starts at `start` and lasts
 * `length` frames. Frames before the window give 0, after it give 1.
 */
export const progress = (
  frame: number,
  start: number,
  length: number,
  ease: Ease = easeOutCubic,
): number => ease(clamp01((frame - start) / Math.max(1, length)));

/** Frame at which the i-th member of a staggered group should start. */
export const staggerStart = (index: number, step: number, offset = 0): number =>
  offset + index * step;

/* ------------------------------------------------------------------------ *
 * After Effects style eases and the overlapping null-camera rig.
 * Technique credit: Fares Toson ("Fares Motion" / pro-motion, see
 * playbooks/overlap-camera.md). Code written fresh for KOSIF.
 * ------------------------------------------------------------------------ */

/**
 * An After Effects two-key ease with speed 0 at both keys.
 * `out` is the first key's outgoing influence and `inf` the last key's
 * incoming influence, both 0..1 (AE shows them as 0..100%).
 * Same curve as CSS `cubic-bezier(out, 0, 1 - inf, 1)`.
 */
export const aeEase = (out: number, inf: number): Ease => {
  const x1 = out;
  const x2 = 1 - inf;
  const bez = (a: number, b: number, t: number): number =>
    3 * (1 - t) * (1 - t) * t * a + 3 * (1 - t) * t * t * b + t * t * t;
  return (p) => {
    if (p <= 0) return 0;
    if (p >= 1) return 1;
    let lo = 0;
    let hi = 1;
    for (let k = 0; k < 40; k++) {
      const t = (lo + hi) / 2;
      if (bez(x1, x2, t) < p) lo = t;
      else hi = t;
    }
    return bez(0, 1, (lo + hi) / 2);
  };
};

/** The five speed graphs: where the peak speed sits decides the feel. */
export const GRAPHS = {
  /** Slow start, charges up, peak near 78% of the time. */
  sharpEnd: aeEase(1, 0.35),
  /** Soft at both ends, a whip in the middle. Section-to-section camera moves. */
  sharpMid: aeEase(0.7, 0.75),
  /** Fires from frame 0 then glides to rest. Element entrances, the opening camera move. */
  sharpStartHard: aeEase(0.0001, 1),
  /** Quick start without the hit, long settle. */
  sharpStartSoft: aeEase(0.32, 1),
  /** Slow all the way, then slams into place. The closing camera move. */
  sharpEndHard: aeEase(1, 0.0001),
} as const;

export type Axis = "x" | "y" | "z";

/** One camera move: a null that shifts the camera `d` px on one axis between frames f0 and f1. */
export interface RigNull {
  axis: Axis;
  d: number;
  f0: number;
  f1: number;
  /** [out, in] influence, 0..1. */
  graph: [number, number];
}

export type Vec3 = { x: number; y: number; z: number };

/**
 * The overlapping camera: the camera never moves by itself, its position is
 * `base` plus the eased offset of every null. Start each null while the one
 * before it is 83–95% done so the combined speed never reaches zero.
 */
export const overlapRig = (base: Vec3, nulls: RigNull[]) => {
  const eases = nulls.map((n) => aeEase(n.graph[0], n.graph[1]));
  return (frame: number): Vec3 => {
    const c = { ...base };
    nulls.forEach((n, i) => {
      c[n.axis] += n.d * eases[i](clamp01((frame - n.f0) / Math.max(1, n.f1 - n.f0)));
    });
    return c;
  };
};

/** Frame where a null moves fastest. Start that section's elements here so camera and elements settle together. */
export const peakFrame = (n: RigNull): number => {
  const e = aeEase(n.graph[0], n.graph[1]);
  const len = Math.max(1, n.f1 - n.f0);
  let best = -1;
  let at = n.f0;
  for (let f = n.f0; f < n.f1; f += 0.25) {
    const v = Math.abs(e((f + 0.25 - n.f0) / len) - e((f - n.f0) / len));
    if (v > best) {
      best = v;
      at = f;
    }
  }
  return Math.round(at);
};

/** Reference rig measured from a 4 s, 1080×1920 comp: opening hit, two whips, closing slam. */
export const REFERENCE_RIG: RigNull[] = [
  { axis: "x", d: -544, f0: 0, f1: 40, graph: [0.0001, 1] },
  { axis: "x", d: -1290, f0: 20, f1: 73, graph: [0.747, 0.793] },
  { axis: "x", d: -1470, f0: 60, f1: 109, graph: [0.727, 0.822] },
  { axis: "x", d: -447, f0: 89, f1: 119, graph: [1, 0.0001] },
];

/** 3D-to-2D projection for an AE one-node camera: scale = zoom / (z - camZ). */
export const project = (cam: Vec3, p: Vec3, zoom: number, w: number, h: number) => {
  const dz = p.z - cam.z;
  if (dz <= 1) return null;
  const s = zoom / dz;
  return { x: w / 2 + (p.x - cam.x) * s, y: h / 2 + (p.y - cam.y) * s, scale: s };
};
