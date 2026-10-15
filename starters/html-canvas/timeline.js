/* KOSIF html-canvas starter — deterministic timeline engine.
 * No dependencies. Every frame is a pure function of time `t`, so the same
 * `seek(t)` call always draws the same pixels: that is what makes
 * tools/render_html.cjs output reproducible and lets you jump anywhere.
 * MIT — part of KOSIF TOOL.
 */
(function (global) {
  'use strict';

  /* ---------- easing (all map [0,1] → [0,1]) ---------- */
  const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
  const Ease = {
    linear: (x) => x,
    outCubic: (x) => 1 - Math.pow(1 - x, 3),
    inOutCubic: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    outExpo: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
    outQuint: (x) => 1 - Math.pow(1 - x, 5),
    outBack: (x, s = 1.70158) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
    inBack: (x, s = 1.70158) => (s + 1) * x * x * x - s * x * x,
    // Damped spring approximation: stiffness → how fast, damping → how much overshoot.
    spring: (x, stiffness = 170, damping = 18) => {
      if (x >= 1) return 1;
      const w = Math.sqrt(stiffness), z = damping / (2 * w);
      if (z >= 1) return 1 - Math.exp(-w * x) * (1 + w * x);
      const wd = w * Math.sqrt(1 - z * z);
      return 1 - Math.exp(-z * w * x) * (Math.cos(wd * x) + (z * w / wd) * Math.sin(wd * x));
    },
  };
  /** progress of t inside [t0, t1], eased */
  function prog(t, t0, t1, ease = Ease.outCubic) { return ease(clamp01((t - t0) / Math.max(1e-6, t1 - t0))); }
  /** 0→1 then 1→0 with an "in" and "out" window; useful for entrance + exit in one call */
  function window01(t, t0, t1, tin = 0.4, tout = 0.4, easeIn = Ease.outCubic, easeOut = Ease.inOutCubic) {
    if (t < t0 || t > t1) return 0;
    const a = prog(t, t0, t0 + tin, easeIn);
    const b = 1 - prog(t, t1 - tout, t1, easeOut);
    return Math.min(a, b);
  }
  const lerp = (a, b, p) => a + (b - a) * p;

  /* ---------- seeded randomness (mulberry32) ---------- */
  function rng(seed) {
    let s = seed >>> 0;
    return function () {
      s = (s + 0x6D2B79F5) >>> 0;
      let z = s;
      z = Math.imul(z ^ (z >>> 15), z | 1);
      z ^= z + Math.imul(z ^ (z >>> 7), z | 61);
      return ((z ^ (z >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* ---------- camera ---------- */
  // Keyframes: [{t, x, y, scale, rot}] ; values are interpolated with easing between keys.
  function cameraAt(keys, t, ease = Ease.inOutCubic) {
    if (!keys.length) return { x: 0, y: 0, scale: 1, rot: 0 };
    if (t <= keys[0].t) return { ...keys[0] };
    for (let i = 1; i < keys.length; i++) {
      if (t <= keys[i].t) {
        const a = keys[i - 1], b = keys[i], p = prog(t, a.t, b.t, ease);
        return { x: lerp(a.x, b.x, p), y: lerp(a.y, b.y, p), scale: lerp(a.scale, b.scale, p), rot: lerp(a.rot, b.rot, p) };
      }
    }
    return { ...keys[keys.length - 1] };
  }
  function applyCamera(el, cam, w, h) {
    // rotate/scale around the stage centre, then pan.
    el.style.transform = `translate(${-cam.x}px, ${-cam.y}px) translate(${w / 2}px, ${h / 2}px) scale(${cam.scale}) rotate(${cam.rot}deg) translate(${-w / 2}px, ${-h / 2}px)`;
  }

  /* ---------- captions from words.json ---------- */
  // words: [{word, start, end}] ; returns {index, word, p (progress inside the word)}
  function activeWord(words, t) {
    for (let i = 0; i < words.length; i++) {
      const w = words[i];
      if (t >= w.start && t < w.end) return { index: i, word: w, p: (t - w.start) / Math.max(1e-6, w.end - w.start) };
    }
    return null;
  }
  // phrase = words between pauses larger than `gap` seconds; used to show a whole line with the current word highlighted
  function phrases(words, gap = 0.45) {
    const out = [];
    let cur = [];
    for (const w of words) {
      if (cur.length && w.start - cur[cur.length - 1].end > gap) { out.push(cur); cur = []; }
      cur.push(w);
    }
    if (cur.length) out.push(cur);
    return out.map((ws) => ({ words: ws, start: ws[0].start, end: ws[ws.length - 1].end }));
  }

  /* ---------- the timeline ---------- */
  class Timeline {
    /**
     * @param {object} o
     * @param {number} o.duration seconds
     * @param {number} o.fps
     * @param {Array<{id:string,t0:number,t1:number,draw:(t:number,p:number,local:number)=>void}>} o.scenes
     * @param {(t:number)=>void} [o.always] runs every frame after scenes (captions, progress bar)
     */
    constructor(o) {
      this.duration = o.duration; this.fps = o.fps || 30; this.scenes = o.scenes; this.always = o.always || (() => {});
      this.t = 0; this.playing = false; this._raf = 0; this._last = 0; this.onFrame = o.onFrame || (() => {});
    }
    seek(t) {
      this.t = Math.max(0, Math.min(this.duration, t));
      for (const s of this.scenes) {
        const active = this.t >= s.t0 && this.t < s.t1;
        if (s.el) s.el.style.display = active ? '' : 'none';
        if (active) s.draw(this.t, clamp01((this.t - s.t0) / (s.t1 - s.t0)), this.t - s.t0);
      }
      this.always(this.t);
      this.onFrame(this.t);
    }
    play() {
      if (this.playing) return;
      this.playing = true; this._last = performance.now();
      const step = (now) => {
        if (!this.playing) return;
        const dt = (now - this._last) / 1000; this._last = now;
        let t = this.t + dt;
        if (t >= this.duration) t = 0; // loop
        this.seek(t);
        this._raf = requestAnimationFrame(step);
      };
      this._raf = requestAnimationFrame(step);
    }
    pause() { this.playing = false; cancelAnimationFrame(this._raf); }
    toggle() { this.playing ? this.pause() : this.play(); }
  }

  global.KOSIF = { Ease, prog, window01, lerp, clamp01, rng, cameraAt, applyCamera, activeWord, phrases, Timeline };
})(window);
