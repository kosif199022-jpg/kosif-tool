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
